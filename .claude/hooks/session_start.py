"""SessionStart: Inbox + Stale-State deterministisch in den Kontext geben."""
from _common import *  # noqa


def main():
    notes = []
    # Inbox: Brain Dump ohne Vorlagenzeilen
    bd = VAULT / "Inbox" / "Brain Dump.md"
    try:
        body = bd.read_text(encoding="utf-8").split("---")[-1]
        content = []
        for l in body.splitlines():
            s = l.strip()
            if not s or s in ("-", "#") or s.startswith(("#", ">", "⬅️")):
                continue
            content.append(l.rstrip())
        if content:
            notes.append("Inbox (Brain Dump) hat Eintraege:\n" + "\n".join(content[:40]))
        else:
            notes.append("Inbox (Brain Dump): leer.")
    except Exception:
        pass
    others = [p.name for p in (VAULT / "Inbox").glob("*.md") if p.name != "Brain Dump.md"]
    if others:
        notes.append("Weitere Inbox-Notizen: " + ", ".join(others))

    if ENGINE:
        stale = book_newer_than_marker("push_next_at")
        if stale:
            notes.append(f"Stale-State: {', '.join(stale)} neuer als letzter push-next "
                         f"({fmt_age(marker_time('push_next_at'))}). Erst finalize + push-next.")
        core_t, core_f = newest_engine_core()
        ok_t = marker_time("regression_ok")
        if core_t and (ok_t is None or ok_t < core_t):
            notes.append(f"Engine-Kern ({core_f}) geaendert {fmt_age(core_t)}, kein Regressions-OK seitdem. "
                         "Vor einem Box-Sync: engine-regression-tester.")
        if not marker_time("push_next_at"):
            # Erststart auf diesem Geraet: ab jetzt zaehlen
            touch_marker("push_next_at")
    else:
        notes.append("Hooks: kein lokaler Engine-Ordner (Laptop / PC aus). Buch- und Sync-Waechter sind hier "
                     "passiv, Kommando-Waechter (Dauerlaeufer, Log-Reads, Enqueue) aktiv.")
    context("\n".join(notes), "SessionStart")


run(main)
