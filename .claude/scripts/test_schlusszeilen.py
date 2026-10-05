"""Selbsttest Schlusszeilen-Check (.claude/hooks/schlusszeilen.py), Max 05.10.2026.

  python .claude/scripts/test_schlusszeilen.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
import schlusszeilen as SZ  # noqa: E402

LANG = "Hier ist die Auswertung. " + "Viel Inhalt zur Aufgabe. " * 40

OK_AENDERUNG = LANG + """
---
- **Modell:** für den Umbau opus.
- **/clear:** ja, frische Session.
- **Daily Note:** Nachtrag eingetragen."""

OK_FRAGE = LANG + """
---
- **Modell:** sonnet reicht.
- **/clear:** nein, Kontext weiterverwenden."""

OK_FREI = LANG + "\n\nModell: haiku reicht dafür. Kein /clear nötig. Daily Note: nichts eingetragen."

# Echte Schlussformulierungen aus alten Antworten (Gegenprobe 05.10.)
ECHT = [
    ("**Modell:** sonnet reicht. **/clear:** vor `/wochenende` ja.\n**Daily Note:** nichts nachgetragen, nur der Push-Marker wurde gesetzt.", True),
    ("**Modell/Session:** sonnet passt. Session kannst du weiterlaufen lassen, kein `/clear` nötig.", False),
    ("Für die Doku-Arbeit würde ich sonnet nehmen und vorher `/clear`.", False),
    ("Modell: haiku reicht, Kontext kann bleiben.", False),
    ("Modell: opus. Clear: nein, die aktuelle Session kann weiterlaufen. In die heutige Notiz eingetragen.", True),
    ("*Modell-Tipp: reine Ablage-Arbeit, sonnet reicht locker. `/clear` vorher sinnvoll.*\nDaily Note: Eintrag ergänzt.", True),
]

# (Text, Aenderung im Zug, erwartete fehlende Teile)
CASES = [
    (OK_AENDERUNG, True, []),
    (OK_FRAGE, False, []),
    (OK_FREI, True, []),
    (OK_FRAGE, True, ["Daily"]),
    (LANG, False, ["Modell", "/clear"]),
    (LANG, True, ["Modell", "/clear", "Daily"]),
    (LANG + "\nModell: opus.", False, ["/clear"]),
    ("Kurz: erledigt.", False, []),                      # kurze Antwort ohne Aenderung
    ("Läuft. Ich warte auf die drei Agents und melde mich.", True, []),  # Zwischenmeldung
    ("Erledigt, Datei angepasst.", True, ["Modell", "/clear", "Daily"]),
    ("", True, []),
    (LANG + "\nSoll ich das so umsetzen oder lieber erst die Box prüfen?", False, []),   # Rueckfrage
] + [(LANG + "\n---\n" + t, ch, []) for t, ch in ECHT]


def transcript(prompt, text, tool=None):
    rows = [{"type": "user", "message": {"content": prompt}}]
    content = []
    if tool:
        content.append({"type": "tool_use", "name": tool[0], "input": tool[1]})
    content.append({"type": "text", "text": text})
    rows.append({"type": "assistant", "message": {"content": content}})
    rows.append({"type": "user", "message": {"content": "<agent-message from=\"x\">fertig</agent-message>"}})
    return [json.dumps(r) for r in rows]


def main():
    fails = 0
    for text, changed, want in CASES:
        got = SZ.missing(text, changed)
        ok = all(any(w in g for g in got) for w in want) and len(got) == len(want)
        if not ok:
            fails += 1
            print(f"FAIL  changed={changed} text={text[-60:]!r}\n      fehlt {got}, erwartet {want}")
    # Transkript: Agent-Rueckmeldung darf den Max-Prompt nicht ueberschreiben
    p, final, ch = SZ.last_turn(transcript("bau das", "fertig", ("Edit", {"file_path": "x"})))
    if not (p == "bau das" and final == "fertig" and ch):
        fails += 1
        print(f"FAIL  last_turn Edit: {p!r} {final!r} {ch}")
    p, final, ch = SZ.last_turn(transcript("lies X", "steht drin", ("Bash", {"command": "grep -n foo x.md 2>/dev/null | head"})))
    if ch:
        fails += 1
        print("FAIL  grep/2>/dev/null als Aenderung gewertet")
    p, final, ch = SZ.last_turn(transcript("trag ein", "ok", ("Bash", {"command": "printf 'x' >> 'Daily Notes/a.md'"})))
    if not ch:
        fails += 1
        print("FAIL  >> nicht als Aenderung erkannt")
    # Hintergrund-Agent offen -> Zwischenmeldung, kein Check (Live-Fund 05.10.)
    rows = [{"type": "user", "message": {"content": "Go, bau es"}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "toolu_A", "name": "Agent", "input": {}},
                                                          {"type": "tool_use", "id": "toolu_E", "name": "Edit", "input": {}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_A",
                                                      "content": [{"type": "text", "text": "Async agent launched successfully."}]}]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "Jetzt fehlt nur noch der Gegenleser."}]}}]
    p, final, ch = SZ.last_turn([json.dumps(r) for r in rows])
    if final or SZ.missing(final, ch):
        fails += 1
        print("FAIL  offener Hintergrund-Agent nicht erkannt")
    rows.append({"type": "user", "message": {"content": "<task-notification><tool-use-id>toolu_A</tool-use-id></task-notification>"}})
    rows.append({"type": "assistant", "message": {"content": [{"type": "text", "text": "Fertig, alles gebaut."}]}})
    p, final, ch = SZ.last_turn([json.dumps(r) for r in rows])
    if not SZ.missing(final, ch):
        fails += 1
        print("FAIL  nach Agent-Rueckkehr greift der Check nicht")
    n = len(CASES) + 5
    print(f"{n - fails}/{n} gruen")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
