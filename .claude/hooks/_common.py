"""Gemeinsame Helfer für die Claude-Code-Hooks (Max' Vault).

Alle Hooks lesen das Hook-JSON von stdin, prüfen etwas Deterministisches
und antworten per JSON auf stdout. Sie müssen schnell sein (ein Python-Start
pro Tool-Aufruf) und dürfen NIE selbst crashen: jeder Fehler → stiller Exit 0,
damit ein kaputter Hook nie die Arbeit blockiert.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

# Der Harness schickt/erwartet UTF-8 auf stdin/stdout. Ohne das hier faellt
# Python auf Windows auf die Konsolen-Codepage zurueck (hier cp1252) - jeder
# Umlaut, Gedankenstrich oder jedes Emoji im Hook-Payload (staendig im Vault:
# Daily Notes, Inbox, Logbuch, auch in Bash-Kommandos) macht dann entweder die
# stdout-JSON ungueltig (Kontext geht verloren) oder laesst read_input() beim
# Decodieren scheitern - der Fehler wird dort still geschluckt und liefert {}
# zurueck, also laufen Bash/Read-Waechter leer, ohne dass irgendwo ein Fehler
# auftaucht. Fund + Fix: 09.09.2026, Anlass war "Kontext ist teilweise nicht
# da" (Max). Vor jedem Hook-Import fest auf UTF-8 stellen, nicht raten lassen.
for _stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

# Engine-Ordner: PC-Pfad, per Env überschreibbar (Tests, Laptop, spätere Umzüge).
# Umzug nach C:\Claude (31.10.2026): neuer Ort zuerst, der alte Pfad ist danach nur noch eine Brücke.
_ENGINE_CANDIDATES = [
    os.environ.get("MAXLAB_ENGINE"),
    r"C:\Claude\projekte\trading-data\engine",
    r"C:\Users\maxlk\Projects\trading-data\engine",
]
ENGINE = next((Path(p) for p in _ENGINE_CANDIDATES if p and Path(p).is_dir()), None)
HUB = next((Path(p) for p in [os.environ.get("MAXLAB_HUB"), r"C:\Claude\projekte\hub", r"C:\Users\maxlk\Projects\hub"]
            if p and Path(p).is_dir()), None)

# Marker-Dateien: im Engine-Ordner (nicht versioniert, gilt für alle Sessions auf
# dem Gerät). Ohne Engine (Laptop) im Vault unter .claude/hooks/.state (gitignored).
STATE = (ENGINE / ".claude_hooks") if ENGINE else (VAULT / ".claude" / "hooks" / ".state")

# Engine-Kern: Änderung hier → engine-regression-tester vor jedem Box-Sync.
ENGINE_CORE = ["sigcore.py", "discovery/controls.py", "overfit.py", "qbt.py", "tsmom.py", "maband.py",
               "discovery/hypothesis_bank.py",
               # Gate v4 (AP278, 01.10.2026): Gate-, Runner- und Uebernahme-Code entscheidet genauso
               # ueber das Buch wie die Engine selbst.
               "discovery/discovery_lib.py", "discovery/discovery_runner.py", "discovery/promote_next.py",
               "discovery/job_generator.py", "developer_run.py", "weekend_check.py",
               # AP246 (15.10.2026): Betriebspunkt + Passquote der Gate-v4-Leitplanke (evaluate_v2-Kernel).
               "operating_point.py", "eval_plan.py", "cage_policy_lib.py",
               # AP411 (18.10.2026): die Rechen-Bremse liegt im Rechenweg von weekend_check/account_card;
               # ein Fehler dort stoppt oder verfaelscht jeden Lauf, deshalb gleiche Regression-Pflicht.
               "rechen_bremse.py"]
# Discovery-Code, den der laufende Runner nur nach Neustart neu lädt.
RUNNER_CODE_DIR = "discovery"
BOOK_FILES = ["book_state.json", "book_state_next.json"]
# Letzter bekannter Box-Stand je Buch-Datei (md5), geschrieben von inbox_tool.py bei --pull und
# --push-next (AP366, 14.10.2026). Liegt im Engine-Ordner, weil auch Pulls ausserhalb von
# Claude (auto_check, Lab) ihn pflegen muessen.
BOOK_SYNC = "book_sync_state.json"


def read_input():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def mtime(p):
    try:
        return Path(p).stat().st_mtime
    except Exception:
        return None


def marker_path(name):
    return STATE / name


def marker_time(name):
    return mtime(marker_path(name))


def touch_marker(name, when=None):
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        p = marker_path(name)
        p.touch(exist_ok=True)
        if when is not None:
            os.utime(p, (when, when))
    except Exception:
        pass


def engine_file(rel):
    return (ENGINE / rel) if ENGINE else None


def newest_engine_core():
    """(mtime, relpath) der jüngsten Kern-Datei, oder (None, None)."""
    best = (None, None)
    if not ENGINE:
        return best
    for rel in ENGINE_CORE:
        t = mtime(ENGINE / rel)
        if t and (best[0] is None or t > best[0]):
            best = (t, rel)
    return best


def book_in_sync(rel):
    """True, wenn der Inhalt von rel dem letzten bekannten Box-Stand entspricht (vom Pull
    geholt oder per --push-next geschrieben). Fehlt der Stand oder ist er kaputt: False,
    dann gilt wie vorher nur die Dateizeit."""
    try:
        import hashlib
        st = json.loads((ENGINE / BOOK_SYNC).read_text(encoding="utf-8"))
        want = (st.get(rel) or {}).get("md5")
        return bool(want) and hashlib.md5((ENGINE / rel).read_bytes()).hexdigest() == want
    except Exception:
        return False


def book_newer_than_marker(marker):
    """Liste der Buch-Dateien, die jünger sind als der Marker UND inhaltlich vom letzten
    bekannten Box-Stand abweichen. Nur die Dateizeit reichte nicht (AP366, 12./13.10.2026):
    jeder `inbox_tool.py --pull` schreibt book_state_next.json mit gleichem Inhalt neu, danach
    meldete der Hook in jeder Session einen fehlenden --push-next, und der Marker wurde zum
    Reflex von Hand gesetzt."""
    if not ENGINE:
        return []
    mt = marker_time(marker)
    out = []
    for rel in BOOK_FILES:
        t = mtime(ENGINE / rel)
        if t and (mt is None or t > mt + 1) and not book_in_sync(rel):
            out.append(rel)
    return out


def fmt_age(ts):
    if not ts:
        return "nie"
    d = time.time() - ts
    if d < 3600:
        return f"vor {int(d // 60)} min"
    if d < 86400:
        return f"vor {d / 3600:.1f} h"
    return f"vor {d / 86400:.1f} Tagen"


def norm(s):
    return (s or "").replace("\\", "/").lower()


def any_re(patterns, text, flags=re.I):
    return any(re.search(p, text, flags) for p in patterns)


# ---- Rechen-Bremse (AP411, Regel Max 18.10.2026) -----------------------------
# Jedes Skript mit mehreren Prozessen laeuft ueber engine/rechen_bremse.py (niedrige Prioritaet, PC-weit
# hoechstens 4 Worker). Anlass 16.10.2026: zwei Sessions mit je eigenem mp.Pool(cpu_count()-1) auf normaler
# Prioritaet legten den 6-Thread-PC lahm. Der Hook weist nur darauf hin, er blockt nie.
_POOL_RE = re.compile(
    r"\b(?:mp|multiprocessing)\s*\.\s*(?:get_context\([^)]*\)\s*\.\s*)?Pool\s*\("   # mp.Pool( / mp.get_context("spawn").Pool(
    r"|\bProcessPoolExecutor\s*\("
    r"|\bfrom\s+multiprocessing(?:\.pool)?\s+import\s+[^\n]*\bPool\b")               # from multiprocessing import Pool
_PY_RUN_RE = re.compile(
    r"""(?:^|\s)(?:python[\d.]*(?:\.exe)?|py)\s+(?:-[WX]\s+\S+\s+|-{1,2}[\w-]+(?:=\S+)?\s+)*"""
    r"""(?:"([^"]+\.py)"|'([^']+\.py)'|([^\s"']+\.py))(?=\s|$)""", re.I)


def pool_ohne_bremse(src):
    """True, wenn der Quelltext einen eigenen Prozess-Pool baut und rechen_bremse nirgends erwaehnt
    (auch ein Kommentar `# rechen_bremse: nicht noetig` schaltet den Hinweis fuer die Datei ab)."""
    return bool(_POOL_RE.search(src or "")) and "rechen_bremse" not in src


def py_ziele(segment):
    """Python-Dateien, die ein Kommando-Segment startet (`python -B pfad/x.py ...`), Anfuehrungszeichen entfernt."""
    return [next(g for g in m.groups() if g) for m in _PY_RUN_RE.finditer(segment or "")]


def bremse_hinweis_text(path):
    name = Path(path).name
    return (f"Hook: `{name}` baut einen eigenen Prozess-Pool ohne `rechen_bremse` (Regel Max 18.10.2026, AP411). "
            "Ohne die Bremse laufen die Worker auf normaler Prioritaet und mehrere Sessions zusammen legen den "
            "6-Thread-PC lahm (16.10.2026). Besser: `import rechen_bremse as RB` und `RB.pool_map(fn, aufgaben, wunsch=4)` "
            "bzw. `RB.pool_imap_unordered(...)` (Engine-Ordner im sys.path; Anleitung Projekte/Backtest-Engine.md, "
            "Abschnitt Rechen-Bremse). Bewusst ohne: einen Kommentar `# rechen_bremse: nicht noetig` in die Datei.")


def hinweis_einmal(key, ttl=6 * 3600):
    """True, wenn zu `key` in den letzten `ttl` Sekunden noch kein Hinweis kam (und merkt sich den Zeitpunkt).
    Haelt Hinweise bei vielen Edits derselben Datei ruhig. Fehler → True (lieber ein Hinweis zu viel)."""
    try:
        p = STATE / "hinweis_einmal.json"
        d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        now = time.time()
        if now - float(d.get(key, 0)) < ttl:
            return False
        d = {k: v for k, v in d.items() if now - float(v) < 24 * 3600}
        d[key] = now
        STATE.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d), encoding="utf-8")
        return True
    except Exception:
        return True


# ---- Session-Transkripte (Cross-Session-Ueberblick, Daily-Note-Pflicht) ----
# Regel Max, 09.09.2026: jede Session soll grob wissen, was in anderen lokalen
# Sessions lief, und jede Session soll die Daily Note verlaesslich pflegen.
# Grenze: Transkripte liegen lokal unter ~/.claude/projects/, nicht im Git-Repo -
# das erfasst nur Sessions auf DEMSELBEN Geraet, nicht geraeteuebergreifend.
# Die Daily Note selbst ist die geraeteuebergreifende Garantie (Git-synchronisiert).

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"


def to_epoch(ts):
    """ISO-8601-Timestamp (wie in den Transkripten, mit 'Z') zu Unix-Epoch."""
    try:
        from datetime import datetime
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def scan_transcript_light(path):
    """Kompakter Scan eines Session-Transkripts: Titel, letzter echter User-Text,
    erste/letzte Aktivitaet, ob Dateien geaendert wurden. Bewusst schlank (kein
    Datei-Kollisions-Abgleich - das macht session_conflicts.py fuer session-guard)
    und schnell genug fuer einen Hook-Aufruf (< 0.1s auch fuer grosse Transkripte)."""
    meta = {
        "sid": path.stem, "cwd": None, "branch": None, "title": None,
        "last_prompt": None, "first_activity": None, "last_activity": None,
        "made_changes": False, "mtime": mtime(path),
    }
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not any(s in line for s in ('"tool_use"', '"cwd"', '"aiTitle"')):
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                ts = to_epoch(rec.get("timestamp"))
                if ts:
                    if meta["first_activity"] is None or ts < meta["first_activity"]:
                        meta["first_activity"] = ts
                    if meta["last_activity"] is None or ts > meta["last_activity"]:
                        meta["last_activity"] = ts
                if rec.get("cwd"):
                    meta["cwd"] = rec["cwd"]
                if rec.get("gitBranch"):
                    meta["branch"] = rec["gitBranch"]
                if rec.get("aiTitle"):
                    meta["title"] = rec["aiTitle"]
                if rec.get("type") == "user" and not rec.get("isMeta"):
                    content = rec.get("message", {}).get("content")
                    if isinstance(content, str) and content.strip():
                        meta["last_prompt"] = content.strip()[:160]
                if not meta["made_changes"]:
                    content = rec.get("message", {}).get("content")
                    if isinstance(content, list):
                        for block in content:
                            if (isinstance(block, dict) and block.get("type") == "tool_use"
                                    and block.get("name") in ("Edit", "Write", "MultiEdit", "NotebookEdit")):
                                meta["made_changes"] = True
                                break
    except Exception:
        pass
    return meta


def recent_local_sessions(exclude_sid=None, limit=5, max_scan=15):
    """Die zuletzt aktiven Sessions auf DIESEM Geraet, projektuebergreifend
    (alle Ordner unter ~/.claude/projects/), neueste zuerst. Erst per Datei-Mtime
    vorsortieren (billig), dann nur die Top-Kandidaten wirklich parsen (teurer)."""
    try:
        files = [p for p in CLAUDE_PROJECTS.glob("*/*.jsonl") if p.stem != exclude_sid]
    except Exception:
        return []
    files.sort(key=lambda p: mtime(p) or 0, reverse=True)
    out = []
    for p in files[:max_scan]:
        meta = scan_transcript_light(p)
        if meta["last_activity"]:
            out.append(meta)
        if len(out) >= limit * 2:  # genug Kandidaten, Rest per echter Aktivitaet sortieren
            break
    out.sort(key=lambda m: m["last_activity"] or 0, reverse=True)
    return out[:limit]


# ---- Antworten -------------------------------------------------------------

def out(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()


def deny(reason, event="PreToolUse"):
    out({"hookSpecificOutput": {"hookEventName": event,
                                "permissionDecision": "deny",
                                "permissionDecisionReason": reason}})
    sys.exit(0)


def context(text, event):
    if text:
        out({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}})
    sys.exit(0)


def block_stop(reason):
    out({"decision": "block", "reason": reason})
    sys.exit(0)


def run(main):
    """Hook-Hauptfunktion absichern: jeder Fehler → still durchlassen."""
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # nie die Arbeit blockieren
        try:
            (STATE).mkdir(parents=True, exist_ok=True)
            with open(STATE / "hook_errors.log", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {Path(sys.argv[0]).name}: {e!r}\n")
        except Exception:
            pass
        sys.exit(0)
