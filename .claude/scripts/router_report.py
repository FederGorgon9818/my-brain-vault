"""Auswertung Schattenbetrieb Wissens-Router (Plan 05.10.2026).

Liest <STATE>/router_log.jsonl und zeigt je Thema, wie oft es feuerte, dazu die
Prompts ohne Thema (Kandidaten fuer verpasste Themen) und den Hook-Fehler-Log.
Abnahme vor dem Kuerzen der CLAUDE.md: ohne-Thema-Liste durchgehen, jede Luecke
als Fall in test_router.py ergaenzen.

  python .claude/scripts/router_report.py [--days 3] [--ohne 30]
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from _common import STATE  # noqa: E402


def main():
    days = float(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 3
    n_ohne = int(sys.argv[sys.argv.index("--ohne") + 1]) if "--ohne" in sys.argv else 30
    cut = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - days * 86400))
    log = STATE / "router_log.jsonl"
    rows = []
    try:
        for line in log.open(encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("ts", "") >= cut:
                rows.append(r)
    except FileNotFoundError:
        print(f"kein Log unter {log}")
        return
    hits, fresh = Counter(), Counter()
    for r in rows:
        hits.update(r.get("hits") or [])
        fresh.update(r.get("fresh") or [])
    sessions = len({r.get("sid") for r in rows})
    print(f"{len(rows)} Prompts aus {sessions} Sessions seit {cut} (Modus {rows[-1]['mode'] if rows else '?'})")
    print("Thema       Treffer  neu je Session")
    for k, v in hits.most_common():
        print(f"  {k:10} {v:6}  {fresh[k]:6}")
    ohne = [r for r in rows if not r.get("hits") and not r.get("tickets") and r.get("len", 0) >= 40]
    print(f"\nohne Thema (>= 40 Zeichen): {len(ohne)}, die letzten {min(n_ohne, len(ohne))}:")
    for r in ohne[-n_ohne:]:
        print(f"  {r['ts'][5:16]} {r['prompt'][:140]!r}")
    err = STATE / "hook_errors.log"
    if err.is_file():
        errs = [l for l in err.read_text(encoding="utf-8", errors="replace").splitlines() if l[:19] >= cut]
        print(f"\nHook-Fehler seit {cut}: {len(errs)}")
        for l in errs[-10:]:
            print("  " + l[:200])


if __name__ == "__main__":
    main()
