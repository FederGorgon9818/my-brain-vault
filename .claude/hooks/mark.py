"""Marker von Hand oder aus Agents setzen: python .claude/hooks/mark.py <name> [<name> ...]

Namen:
  regression_ok  engine-regression-tester hat 'Sync frei' gemeldet (gibt -SyncOnly frei)
  pipeline_ok    pipeline-auditor: keine Blocker fuer den Hypothesen-Job (gibt --enqueue frei)
  push_next_at   Push bewusst nicht noetig (loest den Stop-Hook)
  finalize_at    funded_finalize ist gelaufen
  hypothese_ok   Edit an einer Hypothesen-Bank ist KEINE neue Hypothese (Formatierung,
                 Status-/Ergebnis-Update) -- gibt Edit/Write auf die Bank-Datei frei,
                 bis sie das naechste Mal angefasst wird (guard_write.py)
"""
import sys
from _common import touch_marker, marker_path

names = sys.argv[1:]
if not names:
    print(__doc__)
    sys.exit(1)
for n in names:
    touch_marker(n)
    print(f"Marker gesetzt: {marker_path(n)}")
