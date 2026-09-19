---
name: ticket
description: Ticket aus dem Tracker tasks.json lesen oder die offenen Tickets nach Dringlichkeit listen. Aufruf /ticket AP150 (eine AP-Nummer), /ticket <id> (Slug wie riskguard-eod-telegram-report) oder /ticket ohne Argument (Liste). Nutzen auch, wenn Max fragt "was steht in AP…?" oder "welche Tickets sind offen?".
---

# Skill: Ticket lesen / listen

Tracker: `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (JSON-Liste, Felder u.a. `ap_id`, `id`, `prio`, `status`, `when`, `title`, `why`, `guide`, `blocked_by`, `progress_notes`, `auto_notes`, `done_when`). **Die Box ist die Quelle der Wahrheit** (Regel Max, 06.09.2026).

## Schritte

1. Läuft die Session nicht auf der Box (Hostname ungleich `vmd202078`): zuerst im Engine-Ordner `python discovery/inbox_tool.py --pull`. Auf der Box entfällt das.
2. Argument `$ARGUMENTS`:
   - leer → Liste aller Tickets mit `status` nicht in `done`/`erledigt`/`closed`, sortiert nach `prio` (rot, orange, gelb, gruen) und dann `when`. Je Ticket eine Zeile: `AP-Nr | prio/status | when | Titel (gekürzt)`. Tickets ohne `ap_id` mit ihrer `id` zeigen.
   - `AP123` → das Ticket mit dieser `ap_id`; sonst Slug-Match auf `id`.
3. Für ein einzelnes Ticket alle gefüllten Felder ausgeben, in dieser Reihenfolge: Titel, Prio/Status, When (+ `when_note`), Why, Guide (als nummerierte Liste), Blocked_by, Progress-/Auto-Notes (neueste zuletzt), Done_when, Files, Source, Created.

Lesen per kurzem Python-Snippet mit `encoding="utf-8"` und `PYTHONIOENCODING=utf-8`, nicht die ganze Datei (230 KB) in den Kontext ziehen.

## Wenn Max danach etwas ändern will

Status/Notes ändern nur nach Ansage. Vorher `.bak` anlegen (Muster `tasks.json.bak-YYYYMMDD-<ap>`), dann schreiben, dann außerhalb der Box `python discovery/inbox_tool.py --push-tasks`. Neue Nummer nur nach `--pull` vergeben (Kollisions-Vorfall 03./06.09.2026).
