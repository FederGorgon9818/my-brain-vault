"""Agent-Nutzungs-Audit ueber die Session-Transkripte dieses Geraets (Max' Vault, 11.09.2026).

Frage: wo haben Sessions einen Trigger aus der CLAUDE.md getroffen (Backtest ausgewertet,
Hypothese gebaut, Engine-Kern geaendert, Konzept genannt ...), aber den zustaendigen
Subagent NIE aufgerufen? Regeln kommen aus .claude/hooks/agent_triggers.py (eine Quelle
fuer Prompt-Hook, Stop-Hook und dieses Audit).

Nutzung (Vault-Root):  python .claude/scripts/agent_usage_audit.py [--days 14] [--md]
Liest die Transkripte nur zeilenweise und gibt eine Zusammenfassung aus, nie Inhalte.
Grenze: nur dieses Geraet (Transkripte liegen lokal). Retro-Agent-Futter.
"""
import argparse
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "hooks"))
from agent_triggers import DIRECT_TOOL_BYPASS, match  # noqa: E402

PROJECTS = Path.home() / ".claude" / "projects"


def to_epoch(ts):
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def scan(path):
    """Ein Transkript: Titel, Zeitraum, benutzte Agents/Workflows/Skills, Trigger-Treffer je Scope."""
    s = {"sid": path.stem, "project": path.parent.name, "title": None, "first_prompt": None,
         "start": None, "end": None, "agents": Counter(), "workflows": Counter(), "skills": Counter(),
         "direct_tools": Counter(), "hits": {}, "turns": 0, "changed": set(),
         "workflow_types": set(), "workflow_agents": Counter()}
    try:
        fh = path.open("r", encoding="utf-8", errors="replace")
    except Exception:
        return s
    with fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            ts = to_epoch(rec.get("timestamp"))
            if ts:
                s["start"] = ts if s["start"] is None else min(s["start"], ts)
                s["end"] = ts if s["end"] is None else max(s["end"], ts)
            if rec.get("aiTitle"):
                s["title"] = rec["aiTitle"]
            typ = rec.get("type")
            msg = rec.get("message") or {}
            content = msg.get("content")
            if typ == "user" and not rec.get("isMeta"):
                texts = []
                if isinstance(content, str):
                    texts.append(content)
                elif isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "text":
                            texts.append(b.get("text") or "")
                for t in texts:
                    if t.strip() and not t.startswith("<"):
                        s["turns"] += 1
                        if s["first_prompt"] is None:
                            s["first_prompt"] = re.sub(r"\s+", " ", t.strip())[:120]
                        _collect(s, "user", t)
            elif typ == "assistant" and isinstance(content, list):
                for b in content:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "text":
                        _collect(s, "assistant", b.get("text") or "")
                    elif b.get("type") == "tool_use":
                        name = b.get("name") or ""
                        inp = b.get("input") or {}
                        if name == "Agent":
                            s["agents"][inp.get("subagent_type") or "general-purpose"] += 1
                        elif name == "Workflow":
                            wfn = inp.get("name") or Path(str(inp.get("scriptPath") or "?")).stem
                            # Inline-Skripte tragen keinen Namen; dann aus meta.name im
                            # Skripttext lesen, sonst landet der Lauf als '?' und zaehlt nirgends.
                            if wfn in ("?", "", None):
                                m = re.search(r"name:\s*['\"]([\w-]+)['\"]", str(inp.get("script") or ""))
                                wfn = m.group(1) if m else "?"
                            s["workflows"][wfn] += 1
                            # Der generische Workflow `kette` faehrt die Kette EINES Typs.
                            # Ohne den Typ waere nicht erkennbar, welche Agents er abgedeckt
                            # hat -- dann bliebe die Kette nach einem vollstaendigen Lauf
                            # offen und das Gate wuerde weiter blocken (verdict-auditor,
                            # 21.09.2026: genau dieser Bug haette --skip zum Normalweg gemacht).
                            a = inp.get("args") or {}
                            t = a.get("type") if isinstance(a, dict) else None
                            if wfn == "kette" and t:
                                s["workflow_types"].add(str(t))
                        elif name == "Skill":
                            s["skills"][inp.get("skill") or "?"] += 1
                        elif name in DIRECT_TOOL_BYPASS:
                            s["direct_tools"][name] += 1
                        elif name in ("Bash", "PowerShell"):
                            cmd = inp.get("command") or ""
                            # Nur schreibende/ausfuehrende Kommandos zaehlen, sonst feuert
                            # `grep sigcore.py` oder `--help` als Engine-Aenderung.
                            if re.search(r"(>|\bsed\s+-i|\bcp\b|\bmv\b|\btee\b|robocopy|set-content|out-file|--enqueue|--add-job|-SyncOnly|-Sync\b|\bpython\b)", cmd, re.I) \
                                    and not re.search(r"--help|--dry|\bgrep\b|\bcat\b|\bhead\b|\bls\b", cmd):
                                _collect(s, "bash", cmd)
                        elif name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                            p = str(inp.get("file_path") or inp.get("notebook_path") or "").replace("\\", "/")
                            s["changed"].add(p)
                            _collect(s, "file", p)
    s["workflow_agents"] = workflow_agents(path)
    return s


def session_dir(path):
    """Ordner mit den Nebendaten einer Session (<projekt>/<sid>/: subagents/, workflows/).

    Der Hook bekommt auch in einem Subagent das HAUPT-Transkript (gemessen 26.09.2026,
    Claude Code 2.1.281; fuer Workflow-Agents 28.09.2026). Kaeme doch einmal ein Subagent-Transkript
    (<sid>/subagents/.../agent-*.jsonl), fuehrt das hier zum selben Ordner."""
    p = Path(path)
    low = [x.lower() for x in p.parts]
    if "subagents" in low:
        return Path(*p.parts[:low.index("subagents")])
    return p.with_suffix("")


def workflow_agents(path):
    """Agent-Typen, die ein Workflow dieser Session gestartet hat (Regel Max, 21.09.2026:
    Agents in Workflows sind die durchgesetzte Form der Pflichtkette).

    Das Haupt-Transkript kennt nur den `Workflow`-Aufruf. Fuer ein-weg/konzept-weg/kette
    gibt es in used_agent_names eine feste Zuordnung, ein Ad-hoc-Workflow (inline, eigener
    meta.name) blieb dagegen unsichtbar. Folge am 25./26.09.2026: der research-scout in
    `eval-vs-funded` und `bulenox-check` bekam bei jedem WebSearch "research-scout ist in
    dieser Session noch nicht gelaufen". Quelle ist deshalb das Workflow-Journal
    (<sid>/subagents/workflows/<wf>/journal.jsonl) plus agent-<id>.meta.json (agentType).

    Gezaehlt wird erst ab `result` (Agent hat geliefert). `started` allein reicht nicht:
    es gibt abgebrochene Laeufe ohne `result` und ohne `failed` (strategy-auditor b2317f99,
    quant-statistician 4accbffd), und die wuerden sonst Gate 4 (book_state) und das
    Quittungs-Gate freigeben (Fund verdict-auditor, 26.09.2026). Der laufende Scout selbst
    braucht das nicht, den erkennt guard_chain am agent_type."""
    out = Counter()
    try:
        root = session_dir(path) / "subagents" / "workflows"
        journals = list(root.glob("*/journal.jsonl")) if root.is_dir() else []
    except Exception:
        return out
    for j in journals:
        done = set()
        try:
            with j.open("r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    if rec.get("type") == "result" and rec.get("agentId"):
                        done.add(rec["agentId"])
        except Exception:
            continue
        for aid in done:
            typ = _meta_agent_type(j.parent / f"agent-{aid}.meta.json")
            if typ:
                out[typ] += 1
    return out


def _meta_agent_type(meta_path):
    try:
        return json.loads(Path(meta_path).read_text(encoding="utf-8")).get("agentType") or None
    except Exception:
        return None


def subagent_type(path, agent_id):
    """agentType eines Subagents dieser Session aus seiner meta.json (Agent-Tool oder
    Workflow). Rueckfall fuer Hooks, falls die Hook-Eingabe kein agent_type traegt."""
    if not agent_id:
        return None
    sub = session_dir(path) / "subagents"
    for cand in [sub / f"agent-{agent_id}.meta.json", *sub.glob(f"workflows/*/agent-{agent_id}.meta.json")]:
        typ = _meta_agent_type(cand)
        if typ:
            return typ
    return None


def _collect(s, scope, text):
    for tid, agents, why, snippet in match(scope, text):
        h = s["hits"].setdefault(tid, {"agents": agents, "why": why, "n": 0, "scopes": set(), "snippet": snippet})
        h["n"] += 1
        h["scopes"].add(scope)


def used_agent_names(s):
    """Agents, die in dieser Session wirklich gearbeitet haben -- inklusive derer,
    die ein Workflow INTERN aufgerufen hat.

    Wichtig: Workflow-interne Agent-Aufrufe stehen NICHT im Haupt-Transkript (dort
    steht nur der eine `Workflow`-Aufruf). Wer das vergisst, sieht nach einem
    vollstaendigen Workflow-Lauf eine leere Agent-Liste -- und ein Gate, das darauf
    prueft, blockt danach weiter. Genau dieser Bug steckte am 21.09.2026 im neuen
    `kette`-Workflow (Fund: verdict-auditor), deshalb hier die Zuordnung fuer alle drei.
    Seit 26.09.2026 zaehlen zusaetzlich alle fertigen Agents aus dem Workflow-Journal
    (workflow_agents), das deckt auch Ad-hoc-Workflows ab. Die feste Zuordnung oben
    bleibt unveraendert.
    """
    names = set(s["agents"]) | set(s.get("workflow_agents") or ())
    if "ein-weg" in s["workflows"]:
        names |= {"variant-scout", "strategy-auditor"}
    if "konzept-weg" in s["workflows"]:
        names |= {"familien-scout", "verdict-auditor", "research-scout", "variant-scout", "strategy-auditor"}
    # `kette` faehrt die Pflichtkette EINES Typs -> genau deren Glieder gutschreiben.
    # Die Ketten kommen aus work_types.py, damit hier keine zweite Hardcode-Tabelle
    # entsteht, die auseinanderdriften kann.
    if s.get("workflow_types"):
        try:
            sys.path.insert(0, str(HERE.parents[1] / "hooks"))
            import work_types as _WT
            for t in s["workflow_types"]:
                names |= {_WT.step_name(x) for x in _WT.chain_of(t)}
        except Exception:
            pass
    return names


def gaps(s):
    """Trigger gefeuert, Agent nie aufgerufen -> Liste (tid, fehlende Agents, n, scopes, why, snippet)."""
    used = used_agent_names(s)
    out = []
    for tid, h in s["hits"].items():
        missing = [a for a in h["agents"] if a not in used]
        # Quant-Team: beide sollen laufen, einer allein ist halb.
        if missing:
            out.append((tid, missing, h["n"], sorted(h["scopes"]), h["why"], h["snippet"]))
    for tool, (tid, agents, why) in DIRECT_TOOL_BYPASS.items():
        if s["direct_tools"].get(tool) and not any(a in used for a in agents):
            out.append((tid + ":" + tool, agents, s["direct_tools"][tool], ["tool"], why, f"{tool} x{s['direct_tools'][tool]}"))
    return out


def fmt_day(ts):
    return datetime.fromtimestamp(ts).strftime("%d.%m. %H:%M") if ts else "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--min-turns", type=int, default=2, help="Sessions mit weniger echten Prompts ignorieren")
    ap.add_argument("--md", action="store_true", help="Markdown-Ausgabe (fuer Vault-Notiz)")
    ap.add_argument("--sid", default=None, help="nur diese Session (Stem der .jsonl)")
    a = ap.parse_args()

    cutoff = time.time() - a.days * 86400
    files = [p for p in PROJECTS.glob("*/*.jsonl") if p.stat().st_mtime >= cutoff]
    if a.sid:
        files = [p for p in files if p.stem == a.sid]
    sessions = [scan(p) for p in sorted(files, key=lambda p: p.stat().st_mtime)]
    sessions = [s for s in sessions if s["turns"] >= a.min_turns and s["start"]]

    total_gap = Counter()
    total_used = Counter()
    rows = []
    for s in sessions:
        for n, c in (s["agents"] + s["workflow_agents"]).items():
            total_used[n] += c
        g = gaps(s)
        for tid, missing, n, scopes, why, snip in g:
            for m in missing:
                total_gap[m] += 1
        rows.append((s, g))

    P = print
    P(f"# Agent-Nutzungs-Audit, letzte {a.days} Tage, {len(sessions)} Sessions mit >= {a.min_turns} Prompts (nur dieses Geraet)\n")
    P("## Aufrufe je Agent (gesamt)")
    if total_used:
        for n, c in total_used.most_common():
            P(f"- {n}: {c}")
    else:
        P("- keine Agent-Aufrufe gefunden")
    P("\n## Ausgelassen (Trigger gefeuert, Agent nie aufgerufen), Sessions je Agent")
    for n, c in total_gap.most_common():
        P(f"- {n}: {c} Session(s)")
    P("\n## Je Session")
    for s, g in rows:
        title = s["title"] or s["first_prompt"] or "(ohne Titel)"
        used = ", ".join(f"{k}x{v}" for k, v in s["agents"].most_common()) or "keine"
        wf = ", ".join(f"{k}x{v}" for k, v in s["workflows"].items())
        wfa = ", ".join(f"{k}x{v}" for k, v in s["workflow_agents"].most_common())
        P(f"\n### {fmt_day(s['start'])} bis {fmt_day(s['end'])} | {title[:90]}")
        P(f"- Prompts: {s['turns']}, Agents: {used}{(', Workflows: ' + wf) if wf else ''}"
          f"{(' (darin: ' + wfa + ')') if wfa else ''}, Dateien geaendert: {len(s['changed'])}")
        if not g:
            P("- Luecken: keine")
        for tid, missing, n, scopes, why, snip in g:
            P(f"- **{'/'.join(missing)}** fehlt ({tid}, {n}x in {'/'.join(scopes)}): {why}. Fundstelle: \"{snip[:100]}\"")


if __name__ == "__main__":
    main()
