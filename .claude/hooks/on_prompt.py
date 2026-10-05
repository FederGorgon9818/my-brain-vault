"""UserPromptSubmit: Auftrags-Typ festlegen lassen, dann Agent-Reflex (Max, 21.09.2026).

Vorher (11.09.2026) stand hier nur der Agent-Reflex: Regex ueber den Prompt, passende
Agents als Kontext hinlegen, Entscheidung bei Claude. Das Audit vom 21.09. hat gezeigt,
dass das nicht traegt (logbook-distiller 3 Aufrufe / 30 ausgelassene Sessions), und
Max' Befund dazu war: "ich muss immer selbst ansagen, dass die Agents laufen sollen".

Deshalb steht jetzt der Typ-Router davor:
  1. Quittung fuer diese Session anlegen (receipt.py) -- eine je Session, parallel-sicher.
  2. Typ vorschlagen (work_types.suggest), aber NICHT entscheiden.
  3. Claude schreibt den Typ fest; erst damit steht die Pflichtkette.
Die Kurz-ID steht in der Meldung, damit der CLI-Aufruf bei mehreren offenen Sessions
die richtige Quittung trifft.

Der alte Agent-Reflex bleibt als zweite Spur erhalten: er kennt Trigger, die der
Typ-Router nicht abdeckt (Datei-/Kommando-Trigger, session-guard, alpha-scout).
Slash-Kommandos und sehr kurze Prompts werden weiter ignoriert.
"""
from _common import *  # noqa

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from agent_triggers import match  # noqa: E402
import receipt as R  # noqa: E402
import work_types as WT  # noqa: E402


def main():
    inp = read_input()
    prompt = str(inp.get("prompt") or "")

    # --- 0. Wissens-Router (Plan 05.10.2026) --------------------------------
    # Laeuft VOR dem Laengen-Filter: "Juli-Modus" oder "AP73" sind kurz und
    # muessen trotzdem zuenden. Subagent-Rueckmeldungen und System-Benachrichtigungen
    # kommen ebenfalls als Prompt an, sind aber nicht von Max: die routen nicht und
    # loesen auch den Agent-Reflex unten nicht aus (05.10.: sechs Fehlalarme).
    router_text = ""
    try:
        import knowledge_router as KR
        if KR.is_not_max(prompt):
            sys.exit(0)
        _, _, _, router_text = KR.route(prompt, inp.get("session_id"))
    except SystemExit:
        raise
    except Exception:
        router_text = ""

    if len(prompt.strip()) < 12 or prompt.lstrip().startswith("/"):
        context(router_text, "UserPromptSubmit")

    sugg = [t for t, _ in WT.suggest(prompt)]
    rec, _ = R.ensure(inp.get("session_id"), prompt_hint=prompt, suggested=sugg)
    sid = rec["sid"]
    tp = inp.get("transcript_path")

    lines = [router_text] if router_text else []

    # --- 1. Typ-Router ----------------------------------------------------
    if not rec.get("type"):
        lines.append(f"Hook (Auftrags-Typ): fuer diesen Auftrag ist noch kein Typ gesetzt. "
                     f"Bevor gerechnet, gebaut oder geurteilt wird, den Typ festschreiben:")
        lines.append(f"  python .claude/hooks/receipt.py --sid {sid} --type <typ>")
        if sugg:
            for tid in sugg[:3]:
                chain = " -> ".join(WT.step_name(s) for s in WT.chain_of(tid)) or "keine Kette"
                lines.append(f"  Vorschlag `{tid}`: {WT.label_of(tid)} | Kette: {chain}")
            lines.append("  Vorschlaege sind Regex, keine Entscheidung -- passt keiner, "
                         "`--types` zeigt alle.")
        else:
            lines.append("  Kein Vorschlag getroffen (haeufig bei diktierten Prompts). "
                         "`--types` zeigt die Liste; reine Fragen bekommen `frage`.")
    else:
        miss = R.missing_steps(rec, tp)
        if miss:
            names = ", ".join(WT.step_name(s) for s in miss)
            lines.append(f"Hook (Auftrags-Typ): laufende Quittung {sid}, Typ `{rec['type']}`, "
                         f"offen in der Kette: {names}. Aendert sich die Aufgabe, Typ neu setzen "
                         f"(`receipt.py --sid {sid} --type <typ>`).")

    # --- 2. Agent-Reflex (zweite Spur, deckt Datei-/Kommando-Trigger ab) ---
    hits = match("user", prompt)
    if hits:
        lines.append("Hook (Agent-Reflex): der Prompt trifft zusaetzlich Einschalt-Regeln aus der CLAUDE.md.")
        seen = set()
        for tid, agents, why, snippet in hits:
            key = tuple(agents)
            if key in seen:
                continue
            seen.add(key)
            lines.append(f"- {' + '.join(agents)}: {why} (Fundstelle: \"{snippet[:80]}\")")
        lines.append("Passt ein Agent hier nicht, kurz sagen warum; sonst einschalten, bevor "
                     "gebaut/gerechnet/geurteilt wird.")

    context("\n".join(lines), "UserPromptSubmit")


run(main)
