---
name: ticket
description: Ticket aus dem Tracker tasks.json lesen, anlegen, verschieben oder die offenen Tickets nach Dringlichkeit listen. Aufruf /ticket AP150 (eine AP-Nummer), /ticket <id> (Slug wie riskguard-eod-telegram-report), /ticket ohne Argument (Liste), /ticket neu "Titel" … oder /ticket AP150 nach doing. Nutzen auch, wenn Max fragt "was steht in AP…?", "welche Tickets sind offen?", "leg ein Ticket an", "schieb AP… auf erledigt".
---

# Skill: Ticket lesen, anlegen, verwalten

Tracker: `C:\Users\maxlk\Projects\trading-data\engine\tasks.json`. **Die Box ist die Quelle der Wahrheit** (Regel Max, 06.09.2026). Seit 28.09.2026 gibt es dazu das Ticket-Board im Jira-Stil ([[Ticket-Board (Jira-Stil)]]): Boards, Sprints, Schätzung in Stunden.

**Alles läuft über `engine/ticket_tool.py`**, nie tasks.json von Hand editieren (das Tool hält die Sperre, schreibt Backup + Verlauf und gleicht mit der Box ab). Aufruf im Engine-Ordner mit `PYTHONIOENCODING=utf-8`.

## Lesen

1. Läuft die Session nicht auf der Box (Hostname ungleich `vmd202078`): zuerst `python discovery/inbox_tool.py --pull`. Auf der Box entfällt das.
2. Argument `$ARGUMENTS`:
   - leer → `python ticket_tool.py find "" --n 60` (offene Tickets nach Dringlichkeit: Stufe, nicht blockiert vor blockiert, Faellig-Datum, Rang). Eine Zeile je Ticket: AP | Prio | Spalte | Board | Stunden | Sprint | Titel.
   - `AP123` oder Slug → `python ticket_tool.py show AP123` (alle Felder, Schritte mit Haken, wartet auf / blockiert, letzte Notizen).
   - Suche → `python ticket_tool.py find "board:trading prio:rot sprint:aktuell"`. Filter: `board: prio: status:offen|erledigt|alle col:todo|doing|review|waiting|done sprint:aktuell|backlog|S2026-41 type: label: who:max|claude epic:AP… auto:ja blockiert:ja` plus freier Text.
   - Board-Überblick → `python ticket_tool.py board [--board lab]`.

## Ändern (nur nach Ansage von Max, oder wenn eine Regel es verlangt)

- Anlegen: `python ticket_tool.py new "Titel" --board trading|infra|lab|privat --prio kritisch|rot|datum|gelb|gruen [--due JJJJ-MM-TT] [--type story|task|bug|epic|subtask] [--hours 3] [--why "..."] [--epic AP198] [--assignee max|claude] [--guide "Schritt"]…`. Prio-Skala seit 02.10.2026 (Max): `kritisch` = Sehr hoch (gefaehrdet den Live-Betrieb innerhalb von 3 Tagen), `rot` = Hoch, `datum` = Wichtig mit Datum (nicht sofort, immer mit `--due`), `gelb` = Mittel, `gruen` = Niedrig; `orange` ist Alt-Alias fuer Hoch, in der Suche gehen auch `prio:hoch|sehrhoch|mittel|niedrig`. Das Tool pullt vorher selbst (Nummernkollision 03./06.09.2026) und pusht danach.
- Verschieben: `python ticket_tool.py move AP123 doing` (Spalten: todo, doing, review, waiting, done).
- Felder: `python ticket_tool.py edit AP123 --hours 5 --spent 4 --labels gate,v3 --epic AP198` (`-` löscht ein Feld).
- Notiz: `python ticket_tool.py note AP123 "Zwischenstand"`.
- Abhängigkeit: `python ticket_tool.py link AP123 blocks AP124` (auch `blocked_by`, `relates`, `duplicates`, `--remove`).
- **Löschen** (seit 14.10.2026, nur auf Ansage von Max): `python ticket_tool.py delete AP123 [AP124 review-2026-38 …] [--force]`. Schreibt einen Grabstein in den Verlauf, den der Box-Abgleich auf beiden Seiten respektiert: das Ticket kommt beim nächsten Pull nicht zurück, die AP-Nummer wird nie neu vergeben, ein gelöschtes Auto-Ticket (Wochen-Review, Belege des Monats, Wiedervorlage) wird für denselben Schlüssel nicht neu angelegt. Verweise anderer Tickets (blocked_by, links, epic, parent) werden mit entfernt und angezeigt. Offene Unter-Tickets sperren das Löschen, `--force` leert dann deren Verweis. Erledigt bleibt der Normalfall, Löschen ist für Doppel, Irrtümer und Erledigtes, das niemand mehr sehen soll.
- Zurückholen: `python ticket_tool.py restore AP123` (aus der Kopie im Grabstein, entfernte Verweise bleiben weg). `show` auf ein gelöschtes Ticket sagt, wann und von wem es gelöscht wurde.
- Alles mit `--who max`, wenn Max die Änderung diktiert hat, sonst steht `claude` im Verlauf.

## Board-Zuordnung

| Board | Inhalt |
|---|---|
| `trading` | Alpha, Discovery, Buch, Gates, Strategien, Evals |
| `infra` | Box, Runner, NT8, Deploy, RiskGuard, Telegram |
| `lab` | Hub, Strategy Lab, Workbench, Agents, Hooks, Tools |
| `privat` | Gründung, Steuer, BOS, Finanzen, Social Media |

Sprints plant der Skill `/sprint`.
