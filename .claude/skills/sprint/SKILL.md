---
name: sprint
description: Sprint Planning und Sprint-Abschluss fürs Ticket-Board (Jira-Stil) - Backlog lesen, Sprint für die kommende Woche vorschlagen (Ziel, Tickets, Stunden gegen Kapazität), nach Max' OK einplanen und starten; am Sprint-Ende Report, Übertrag, Daily-Note-Zeile. Nutzen, wenn Max /sprint aufruft oder sagt "Sprint Planning", "plan die Woche", "welche Tickets diese Woche?", "Sprint abschließen", "wie lief der Sprint?". Sonntags zum Wochenend-Review von selbst anbieten.
---

# Skill: Sprint Planning (Wochen-Sprint Mo bis So)

Regeln von Max (28.09.2026, [[Ticket-Board (Jira-Stil)]]): Sprint = 1 Woche, **Mo bis So**, Planning **sonntags** nach dem Wochenend-Review fürs Buch. **Schätzung in Stunden.** Auto-Tickets der Box landen immer im Backlog und kommen nur über dieses Planning in einen Sprint.

Werkzeug: `engine/ticket_tool.py` (Engine-Ordner, `PYTHONIOENCODING=utf-8`). Außerhalb der Box vorher `python discovery/inbox_tool.py --pull`.

## A. Planning (Standard, sonntags)

1. **Stand holen:** `python ticket_tool.py sprint list`, `python ticket_tool.py backlog --n 60`, `python ticket_tool.py find "prio:rot"`, `python ticket_tool.py find "auto:ja"`.
2. **Läuft noch ein Sprint?** Dann zuerst Teil B (Abschluss), dann weiter.
3. **Kapazität bestimmen:** Schnitt der gebrauchten Stunden der letzten 2 bis 3 Sprints (`sprint list` bzw. Report). In den ersten Sprints ohne Historie Max fragen, wie viele Stunden die Woche realistisch sind (Vollzeitjob bis 03.07.2027).
4. **Vorschlag bauen** (nicht schreiben):
   - Pflicht zuerst: rot, Fristen in der Woche (`when`), Tickets mit Datum im Sprintzeitraum, Handelsfenster beachten.
   - Nie ein Ticket einplanen, das auf ein offenes Ticket außerhalb des Sprints wartet (`⛔wartet`), außer der Blocker kommt mit rein.
   - Tickets ohne Schätzung: Stunden vorschlagen, Max bestätigt.
   - Summe Stunden ≤ Kapazität, Puffer ~20 %.
   - Ein Satz Sprint-Ziel, das zum großen Ziel passt (Zeit bis 50k, CLAUDE.md), nicht nur eine Liste.
   - Ausgabe als Tabelle: AP | Titel | Board | Prio | h | warum diese Woche. Darunter: was bewusst NICHT reinkommt und warum.
5. **Nach OK von Max:**
   - Sprint anlegen, falls es ihn noch nicht gibt: `python ticket_tool.py sprint new --start <Montag> --goal "..." --capacity <h>`
   - Schätzungen setzen: `python ticket_tool.py edit AP… --hours <h>`
   - Einplanen: `python ticket_tool.py sprint plan <Sprint-ID> AP… AP…`
   - Montags oder direkt: `python ticket_tool.py sprint start <Sprint-ID>`
6. **Daily Note:** Sprint-ID, Ziel, Tickets, Summe Stunden eintragen.

## B. Abschluss (Sonntag vor dem Planning, oder auf Ansage)

1. `python ticket_tool.py report <Sprint-ID>` zeigen: zugesagt, geschafft, gebraucht, offen.
2. Mit Max durchgehen, was wirklich fertig ist (Erledigt-Pflicht: Max bestätigt, nie still auf erledigt setzen).
3. `python ticket_tool.py sprint close <Sprint-ID>` (Unfertiges wandert in den nächsten geplanten Sprint, `--carry backlog` schiebt es zurück in den Backlog).
4. Report-Markdown in die Daily Note, eine Zeile Retro: was hat die Woche gebremst.

## Im Lab

Dasselbe geht per Hand im Strategy Lab → Tickets → **Backlog** (Ziehen in den Sprint, Starten/Abschließen) und **Sprints** (Burndown, Velocity, Report zum Kopieren).
