#!/usr/bin/env python3
"""
session_conflicts.py - findet Schreib-Kollisionen zwischen parallel laufenden Claude-Sessions.

Datenquelle sind die Session-Transkripte unter ~/.claude/projects/<projekt>/<session-id>.jsonl.
Jeder Edit/Write/NotebookEdit steht dort mit absolutem file_path und UTC-Timestamp drin,
Bash-Aufrufe mit dem kompletten Kommando. Daraus laesst sich exakt rekonstruieren,
welche Session wann welche Datei angefasst hat.

Gemeldet werden vier Dinge:
  1. aktive Sessions im Zeitfenster (wer laeuft ueberhaupt gerade)
  2. COLLISION  - dieselbe Datei von mehreren Sessions geschrieben
  3. CLOBBER    - eine Session hat nach einer anderen auf dieselbe Datei geschrieben
                  (das ist der Fall "meine Aenderung ist weg")
  4. RISK       - parallele Bash-Kommandos, die ausserhalb der Tool-Ebene schreiben
                  (git commit, python-Laeufe, Redirects, Deploys)

Aufruf:
    python session_conflicts.py [--window-min 120] [--self <session-id>] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

# Bash-Kommandos, die am Tool-Layer vorbei schreiben. Die Engine-Skripte stehen mit drin,
# weil zwei parallele funded_finalize.py-Laeufe portfolio.json zerlegen wuerden.
RISKY_BASH = [
    (r"\bgit\s+(commit|checkout|switch|reset|stash|pull|merge|rebase|restore|clean)\b", "git-state"),
    # nur echte Ausfuehrung, nicht jede Erwaehnung des Dateinamens (sonst matcht "wc -l developer_run.py")
    (r"\bpython[\w.]*\s+(?:-\S+\s+)*\S*(funded_finalize|live_finalize|developer_run|portfolio_tab)\.py\b",
     "engine-write"),
    (r"\bbox_deploy\.ps1\b", "deploy"),
    (r"(?<![0-9&])>{1,2}\s*(?!/dev/null|\$null|&)", "redirect"),
    (r"\b(mv|cp|rm)\s+-", "fileop"),
    (r"\b(Set-Content|Out-File|Add-Content|New-Item|Remove-Item|Copy-Item|Move-Item)\b", "fileop"),
]
RISKY_BASH = [(re.compile(p, re.I), tag) for p, tag in RISKY_BASH]


def norm(path: str) -> str:
    """Windows-Pfade case-insensitiv und Trenner-neutral vergleichbar machen."""
    return os.path.normcase(os.path.normpath(path))


def to_epoch(ts: str) -> float:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


def ago(epoch: float, now: float) -> str:
    if not epoch:
        return "?"
    m = (now - epoch) / 60.0
    if m < 1:
        return "gerade eben"
    if m < 90:
        return f"vor {int(m)} min"
    return f"vor {m / 60:.1f} h"


def scan_session(path: Path, cutoff: float):
    """Ein Transkript streamen. Gibt Session-Meta + Schreibzugriffe + riskante Bash-Calls zurueck."""
    meta = {
        "sid": path.stem,
        "file": str(path),
        "cwd": None,
        "branch": None,
        "title": None,
        "last_prompt": None,
        "last_activity": 0.0,
        "mtime": path.stat().st_mtime,
    }
    writes = []   # (epoch, file_path, tool)
    risky = []    # (epoch, tag, command)

    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"tool_use"' not in line and '"cwd"' not in line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue

            ts = to_epoch(rec.get("timestamp", ""))
            if ts > meta["last_activity"]:
                meta["last_activity"] = ts
            if rec.get("cwd"):
                meta["cwd"] = rec["cwd"]
            if rec.get("gitBranch"):
                meta["branch"] = rec["gitBranch"]
            for key in ("customTitle", "aiTitle"):
                if rec.get(key):
                    meta["title"] = rec[key]
            if rec.get("lastPrompt"):
                meta["last_prompt"] = str(rec["lastPrompt"])[:120]

            if ts < cutoff:
                continue
            content = rec.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name")
                inp = block.get("input") or {}
                if name in WRITE_TOOLS:
                    fp = inp.get("file_path") or inp.get("notebook_path")
                    if fp:
                        writes.append((ts, fp, name))
                elif name in ("Bash", "PowerShell"):
                    cmd = (inp.get("command") or "")[:300]
                    for pat, tag in RISKY_BASH:
                        if pat.search(cmd):
                            risky.append((ts, tag, cmd))
                            break

    return meta, writes, risky


def recover(target: str, limit: int = 12) -> int:
    """
    Vorversionen einer Datei in ~/.claude/file-history finden.

    Claude Code legt dort vor jeder Aenderung eine Volltextkopie ab, aber der Dateiname
    ist ein Hash ohne Index. Zuordnung deshalb ueber Zeilen-Ueberlappung mit dem
    aktuellen Stand: dieselbe Datei in einer anderen Version teilt fast alle Zeilen,
    eine fremde Datei so gut wie keine.
    """
    hist = Path.home() / ".claude" / "file-history"
    if not hist.is_dir():
        print("Keine file-history vorhanden.", file=sys.stderr)
        return 2

    tpath = Path(target)
    if not tpath.exists():
        print(f"{target} existiert nicht mehr - Zuordnung per Ueberlappung nicht moeglich.")
        print("Kandidaten muessen ueber den Inhalt gesucht werden, z.B.:")
        print(f'  grep -rl "<charakteristischer String>" "{hist}"')
        return 2

    cur = set(l.strip() for l in tpath.read_text(encoding="utf-8", errors="replace").splitlines()
              if len(l.strip()) > 8)
    if not cur:
        print("Zieldatei hat zu wenig verwertbaren Inhalt.", file=sys.stderr)
        return 2

    now = time.time()
    hits = []
    for cand in hist.glob("*/*"):
        if not cand.is_file() or cand.stat().st_size > 4_000_000:
            continue
        try:
            lines = set(l.strip() for l in cand.read_text(encoding="utf-8", errors="replace").splitlines()
                        if len(l.strip()) > 8)
        except Exception:
            continue
        if not lines:
            continue
        overlap = len(cur & lines) / max(len(cur), len(lines))
        if overlap >= 0.35:
            hits.append((overlap, cand.stat().st_mtime, cand))

    if not hits:
        print(f"Keine Vorversion von {target} in der file-history gefunden.")
        newest = max((c.stat().st_mtime for c in hist.glob("*/*") if c.is_file()), default=0)
        if newest:
            print(f"Juengster Eintrag der gesamten file-history: {ago(newest, now)}.")
            if now - newest > 6 * 3600:
                print("Die Historie wird offenbar nicht mehr befuellt - als Backup nicht verlassbar.")
        print("Ohne Git im betroffenen Ordner gibt es dann keinen Wiederherstellungspfad.")
        return 1

    hits.sort(key=lambda h: h[1], reverse=True)
    print(f"Vorversionen von {target} (neueste zuerst, Ueberlappung mit aktuellem Stand):\n")
    for ov, mt, cand in hits[:limit]:
        same = " == identisch zum aktuellen Stand" if ov > 0.999 else ""
        print(f"  {ov * 100:5.1f}%  {ago(mt, now):>14}  {cand}{same}")
        print(f"           Session {cand.parent.name[:8]}")
    print(f'\nUnterschied ansehen:  diff "<kandidat>" "{target}"')
    print(f'Zuruecksichern     :  cp "<kandidat>" "{target}"   (vorher aktuellen Stand wegsichern!)')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--recover", metavar="PATH", default=None,
                    help="Vorversionen dieser Datei in der file-history suchen")
    ap.add_argument("--window-min", type=int, default=120,
                    help="Zeitfenster in Minuten, das als 'parallel' gilt (Default 120)")
    ap.add_argument("--self", dest="self_sid", default=None,
                    help="Session-ID der eigenen Session (steht im Scratchpad-Pfad)")
    ap.add_argument("--projects-dir", default=str(Path.home() / ".claude" / "projects"))
    ap.add_argument("--json", action="store_true", help="Maschinenlesbare Ausgabe")
    args = ap.parse_args()

    if args.recover:
        return recover(args.recover)

    now = time.time()
    cutoff = now - args.window_min * 60
    root = Path(args.projects_dir)
    if not root.is_dir():
        print(f"Kein Projekte-Verzeichnis unter {root}", file=sys.stderr)
        return 2

    sessions, writes_by_sid, risky_by_sid = {}, {}, {}
    for jsonl in root.glob("*/*.jsonl"):
        # Transkripte, die im Fenster gar nicht angefasst wurden, koennen nichts beigetragen haben.
        if jsonl.stat().st_mtime < cutoff:
            continue
        meta, writes, risky = scan_session(jsonl, cutoff)
        sessions[meta["sid"]] = meta
        writes_by_sid[meta["sid"]] = writes
        risky_by_sid[meta["sid"]] = risky

    # Datei -> Session -> (erster, letzter) Schreibzugriff
    per_file: dict[str, dict[str, dict]] = defaultdict(dict)
    display_name: dict[str, str] = {}
    for sid, writes in writes_by_sid.items():
        for ts, fp, tool in writes:
            key = norm(fp)
            display_name.setdefault(key, fp)
            e = per_file[key].setdefault(sid, {"first": ts, "last": ts, "n": 0, "tools": set()})
            e["first"] = min(e["first"], ts)
            e["last"] = max(e["last"], ts)
            e["n"] += 1
            e["tools"].add(tool)

    collisions, clobbers = [], []
    for key, by_sid in per_file.items():
        if len(by_sid) < 2:
            continue
        order = sorted(by_sid.items(), key=lambda kv: kv[1]["last"])
        # Ein voller Write ersetzt die Datei blind. Ein Edit kann nur greifen, wenn die Session
        # vorher gelesen hat, faellt bei Fremdaenderung also meist von selbst durch -> weniger scharf.
        blind = any("Write" in d["tools"] for _, d in order)
        collisions.append({
            "file": display_name[key],
            "severity": "hoch" if blind else "mittel",
            "sessions": [{"sid": s, "n": d["n"], "first": d["first"], "last": d["last"],
                          "tools": sorted(d["tools"])} for s, d in order],
        })
        # Clobber: wer zuletzt geschrieben hat, haelt den Stand. Alle frueheren Sessions
        # arbeiten auf einem ueberholten Bild. Pro Datei ein Eintrag, nicht jedes Paar.
        winner_sid, winner = order[-1]
        stale = [{"sid": s, "last": d["last"],
                  "gap_min": round((winner["last"] - d["last"]) / 60.0, 1)}
                 for s, d in order[:-1] if d["last"] < winner["last"]]
        if stale:
            clobbers.append({
                "file": display_name[key],
                "severity": "hoch" if blind else "mittel",
                "writer": winner_sid, "writer_last": winner["last"], "stale": stale,
            })

    # Riskante Bash-Kommandos, die zeitlich ueberlappen (gleicher Tag, verschiedene Sessions)
    risk_pairs = []
    by_tag: dict[str, list] = defaultdict(list)
    for sid, items in risky_by_sid.items():
        for ts, tag, cmd in items:
            by_tag[tag].append((ts, sid, cmd))
    for tag, items in by_tag.items():
        sids = {s for _, s, _ in items}
        if len(sids) < 2:
            continue
        items.sort()
        risk_pairs.append({
            "tag": tag,
            "sessions": sorted(sids),
            "samples": [{"sid": s, "ts": t, "cmd": c} for t, s, c in items[-6:]],
        })

    active = sorted(sessions.values(), key=lambda m: m["last_activity"], reverse=True)

    if args.json:
        out = {
            "generated": now, "window_min": args.window_min, "self": args.self_sid,
            "sessions": active, "collisions": collisions,
            "clobbers": clobbers, "risk_pairs": risk_pairs,
        }
        print(json.dumps(out, indent=2, default=str))
        return 0

    def tag_self(sid: str) -> str:
        return f"{sid[:8]}{' (ICH)' if args.self_sid and sid == args.self_sid else ''}"

    print(f"=== Session-Kollisionscheck | Fenster {args.window_min} min | "
          f"{len(active)} aktive Session(s) ===\n")

    for m in active:
        w = writes_by_sid.get(m["sid"], [])
        files = {norm(fp) for _, fp, _ in w}
        print(f"[{tag_self(m['sid'])}] {m.get('title') or '(ohne Titel)'}")
        print(f"    zuletzt aktiv : {ago(m['last_activity'], now)}")
        print(f"    cwd / branch  : {m.get('cwd')} @ {m.get('branch') or '-'}")
        print(f"    Schreibzugriffe: {len(w)} auf {len(files)} Datei(en)")
        if m.get("last_prompt"):
            print(f"    letzter Prompt: {m['last_prompt']}")
        print()

    if not collisions:
        print("KEINE KOLLISION: keine Datei wurde im Fenster von mehr als einer Session geschrieben.\n")
    else:
        print(f"--- {len(collisions)} KOLLISION(EN): Datei von mehreren Sessions geschrieben ---")
        for c in collisions:
            print(f"\n  [{c['severity']}] {c['file']}")
            for s in c["sessions"]:
                print(f"    {tag_self(s['sid']):>16}  {s['n']}x {'/'.join(s['tools'])}, "
                      f"zuletzt {ago(s['last'], now)}")
        print()

    if clobbers:
        print(f"--- {len(clobbers)} DATEI(EN) MIT UEBERHOLTEM STAND ---")
        for c in clobbers:
            mtime = os.path.getmtime(c["file"]) if os.path.exists(c["file"]) else 0
            print(f"  {c['file']}")
            print(f"    Stand haelt : {tag_self(c['writer'])} (schrieb {ago(c['writer_last'], now)}"
                  f"{', Datei-mtime ' + ago(mtime, now) if mtime else ''})")
            for s in c["stale"]:
                print(f"    ueberholt   : {tag_self(s['sid'])} (letzter Schreibzugriff "
                      f"{ago(s['last'], now)}, {s['gap_min']} min vorher)")
        print()

    if risk_pairs:
        print("--- PARALLELE SCHREIBER AUSSERHALB DER TOOL-EBENE ---")
        for r in risk_pairs:
            print(f"  [{r['tag']}] Sessions: {', '.join(tag_self(s) for s in r['sessions'])}")
            for s in r["samples"][-3:]:
                print(f"      {tag_self(s['sid'])} {ago(s['ts'], now):>14}: {s['cmd'][:110]}")
        print()

    # Exit-Code als Ampel, damit ein Hook oder Skript darauf reagieren kann.
    if clobbers:
        return 1
    if collisions or risk_pairs:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
