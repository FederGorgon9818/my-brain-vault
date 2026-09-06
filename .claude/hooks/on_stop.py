"""Stop: Session darf nicht enden, solange book_state*.json ungepusht ist.

Greift nur auf dem Geraet mit lokalem Engine-Ordner (PC). `stop_hook_active`
verhindert eine Endlosschleife: nach einem Block wird nur noch erinnert.
"""
from _common import *  # noqa


def main():
    inp = read_input()
    if not ENGINE:
        sys.exit(0)
    stale = book_newer_than_marker("push_next_at")
    if not stale:
        sys.exit(0)
    msg = (f"Hook: {', '.join(stale)} wurde geaendert, aber seitdem kein `inbox_tool.py --push-next` "
           f"(letzter Push {fmt_age(marker_time('push_next_at'))}). Regel 21.08.2026: "
           "funded_finalize (+--next) laufen lassen und pushen, sonst promotet die Box in einen alten Stand. "
           "Wenn der Push bewusst nicht gewollt ist (Datei nur neu formatiert o.ae.): "
           "`python .claude/hooks/mark.py push_next_at` setzt den Marker von Hand.")
    if inp.get("stop_hook_active"):
        out({"systemMessage": msg})
        sys.exit(0)
    block_stop(msg)


run(main)
