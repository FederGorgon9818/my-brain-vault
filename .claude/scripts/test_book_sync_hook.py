"""Selbsttest AP366 (14.10.2026): Buch-Waechter vergleicht den Inhalt, nicht nur die Dateizeit.

Vorher meldete der Stop-Hook nach jedem `inbox_tool.py --pull` "book_state_next.json geaendert,
aber kein --push-next", weil der Pull die Datei mit gleichem Inhalt neu schreibt. Jetzt merkt
sich inbox_tool beim Pull und beim Push den Box-Stand (md5 in engine/book_sync_state.json),
und der Hook schweigt, solange die Datei genau diesem Stand entspricht.

Laeuft gegen einen Wegwerf-Engine-Ordner (MAXLAB_ENGINE), fasst nichts Echtes an.

    python .claude/scripts/test_book_sync_hook.py
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

ENG = Path(tempfile.mkdtemp(prefix="hook_book_"))
os.environ["MAXLAB_ENGINE"] = str(ENG)
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
import _common as C  # noqa: E402

assert C.ENGINE == ENG, "MAXLAB_ENGINE greift nicht"
fails = []


def check(name, cond, info=""):
    print(("OK   " if cond else "FAIL ") + name + (f"  [{info}]" if info and not cond else ""))
    if not cond:
        fails.append(name)


def write_book(rel, obj, age_s=0):
    p = ENG / rel
    p.write_text(json.dumps(obj), encoding="utf-8")
    t = time.time() - age_s
    os.utime(p, (t, t))
    return p


def note_sync(rel, path):
    """Wie inbox_tool._note_book_sync: Box-Stand merken."""
    f = ENG / C.BOOK_SYNC
    st = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    st[rel] = {"md5": hashlib.md5(Path(path).read_bytes()).hexdigest(), "via": "test"}
    f.write_text(json.dumps(st), encoding="utf-8")


NEXT, LIVE = "book_state_next.json", "book_state.json"
write_book(LIVE, {"legs": ["a"]}, age_s=3600)
C.touch_marker("push_next_at", time.time() - 600)          # letzter Push vor 10 Minuten

# 1. Pull schreibt den gleichen Inhalt neu (frische Dateizeit), Box-Stand gemerkt -> still
p = write_book(NEXT, {"legs": ["a", "b"]})
note_sync(NEXT, p)
check("gleicher Inhalt nach Pull, frische Dateizeit: kein Alarm", C.book_newer_than_marker("push_next_at") == [])

# 2. Inhalt danach am PC geaendert -> Alarm
write_book(NEXT, {"legs": ["a", "b", "c"]})
check("anderer Inhalt: Alarm", C.book_newer_than_marker("push_next_at") == [NEXT])

# 3. Ohne gemerkten Box-Stand gilt wie vorher die Dateizeit
(ENG / C.BOOK_SYNC).unlink()
write_book(NEXT, {"legs": ["a", "b"]})
check("ohne Box-Stand: Dateizeit entscheidet wie vorher", C.book_newer_than_marker("push_next_at") == [NEXT])

# 4. Kaputte Stand-Datei blockiert nichts und schweigt nicht falsch
(ENG / C.BOOK_SYNC).write_text("{kaputt", encoding="utf-8")
check("kaputter Box-Stand: kein Absturz, Dateizeit entscheidet", C.book_newer_than_marker("push_next_at") == [NEXT])

# 5. Datei aelter als der letzte Push -> still, egal welcher Inhalt
write_book(NEXT, {"legs": ["x"]}, age_s=3600)
check("Datei aelter als letzter Push: kein Alarm", C.book_newer_than_marker("push_next_at") == [])

# 6. Live-Buch: Pull merkt den Box-Stand von book_state.json (Drift-Check), gleicher Inhalt -> still
p = write_book(LIVE, {"legs": ["a"]})
(ENG / C.BOOK_SYNC).unlink()
note_sync(LIVE, p)
check("Live-Buch gleich Box-Stand: kein Alarm", LIVE not in C.book_newer_than_marker("push_next_at"))

# 7. Echter Schreiber (inbox_tool._note_book_sync) gegen den Leser im Hook: gleicher Dateiname, gleiche
#    Schluessel (verdict-auditor 15.10.2026). Nur wo die Engine liegt (PC), sonst uebersprungen.
REAL = Path(r"C:\Users\maxlk\Projects\trading-data\engine")
try:
    sys.path.insert(0, str(REAL / "discovery"))
    import inbox_tool as IT  # noqa: E402
except Exception as e:
    IT = None
    print(f"(inbox_tool nicht ladbar: {type(e).__name__}, Fall 7 uebersprungen)")
if IT is not None:
    (ENG / C.BOOK_SYNC).unlink(missing_ok=True)
    p = write_book(NEXT, {"legs": ["echt"]})
    old_eng = IT.L.ENG
    try:
        IT.L.ENG = ENG
        IT._note_book_sync(NEXT, p, "test")
    finally:
        IT.L.ENG = old_eng
    check("echter Schreiber + Hook-Leser passen zusammen: kein Alarm", NEXT not in C.book_newer_than_marker("push_next_at"))
    write_book(NEXT, {"legs": ["echt", "neu"]})
    check("... und danach geaenderter Inhalt: Alarm", NEXT in C.book_newer_than_marker("push_next_at"))

shutil.rmtree(ENG, ignore_errors=True)
print(f"\n{'ALLES OK' if not fails else f'{len(fails)} FEHLER'}")
sys.exit(1 if fails else 0)
