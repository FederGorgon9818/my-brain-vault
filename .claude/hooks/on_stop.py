"""Stop: Session darf nicht enden, solange offene Pflichten stehen.

1. book_state*.json geaendert, aber kein push-next seitdem (nur mit lokalem
   Engine-Ordner, also PC/Box).
2. Regel Max, 09.09.2026: diese Session hat Dateien geaendert, aber die heutige
   Daily Note nicht angefasst - Kontextverlust soll "quasi nicht moeglich" sein.
   Greift ueberall (auch Laptop ohne Engine-Ordner), da die Daily Note die
   geraeteuebergreifende Garantie ist (Git-synchronisiert, anders als die
   lokalen Session-Transkripte).

`stop_hook_active` verhindert eine Endlosschleife: nach einem Block wird nur
noch erinnert, nicht mehr blockiert (Cap des Harness liegt bei 8 Blocks/Session).
"""
from _common import *  # noqa


def main():
    inp = read_input()
    issues = []

    # --- 1. Buch geaendert, nicht gepusht ------------------------------------
    if ENGINE:
        stale = book_newer_than_marker("push_next_at")
        if stale:
            issues.append(
                f"{', '.join(stale)} wurde geaendert, aber seitdem kein `inbox_tool.py --push-next` "
                f"(letzter Push {fmt_age(marker_time('push_next_at'))}). Regel 21.08.2026: "
                "funded_finalize (+--next) laufen lassen und pushen, sonst promotet die Box in einen alten Stand. "
                "Wenn der Push bewusst nicht gewollt ist (Datei nur neu formatiert o.ae.): "
                "`python .claude/hooks/mark.py push_next_at` setzt den Marker von Hand."
            )

    # --- 2. Diese Session hat geaendert, Daily Note nicht --------------------
    tp = inp.get("transcript_path")
    if tp and Path(tp).is_file():
        meta = scan_transcript_light(Path(tp))
        if meta["made_changes"] and meta["first_activity"]:
            today = VAULT / "Daily Notes" / f"{time.strftime('%Y-%m-%d')}.md"
            note_t = mtime(today)
            if note_t is None or note_t < meta["first_activity"]:
                issues.append(
                    f"diese Session hat Dateien geaendert, aber die heutige Daily Note "
                    f"({today.name}) wurde seitdem nicht angefasst. Regel 09.09.2026: kurz "
                    "nachtragen was gemacht/entschieden wurde (Stichpunkte reichen), danach "
                    "erneut beenden. Betrifft nur diese Session - eine andere Session kann die "
                    "Note zwischenzeitlich schon aktualisiert haben, dann greift das hier nicht."
                )

    if not issues:
        sys.exit(0)
    msg = "Hook: " + " | ".join(issues)
    if inp.get("stop_hook_active"):
        out({"systemMessage": msg})
        sys.exit(0)
    block_stop(msg)


run(main)
