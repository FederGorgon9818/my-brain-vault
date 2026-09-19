---
name: queue
description: Discovery-Stand kompakt - Inbox von der Box holen, Runner-Status, Queue-Vorrat, ungelesene Kandidaten mit Buch-Lücke je Kandidat. Nutzen, wenn Max /queue aufruft oder fragt "was hat die Discovery gefunden?", "wie voll ist die Queue?", "gibt es Kandidaten?".
---

# Skill: Discovery-Queue und Inbox

## Schritte

1. Im Engine-Ordner `C:\Users\maxlk\Projects\trading-data\engine`: auf der Box (Hostname `vmd202078`) `python discovery/inbox_tool.py --local`, sonst `python discovery/inbox_tool.py --pull` (holt Inbox, Register, Next-Buch, Tickets von der Box). Nie `runner.log` oder volle `results/*.json` lesen; bei Bedarf `python summarize_results.py <results.json>`.
2. Aus `discovery/queue.json` zählen: pending / running / done / skipped, davon `tag` = `variant_*` und `generator_coverage`, handgebaute Jobs mit `priority` ≥ 60. Vorrat in Tagen grob aus pending ÷ ~41 Slots/Tag (Messung 09.09.2026).
3. Heartbeat-Alter des Runners; älter als 30 Minuten bei pending-Jobs = steht (Neustart per WMI-Zeile in `box_provision_discovery.ps1`, nur nach Ansage).

## Ausgabe

- **Runner:** läuft/steht, aktueller Job, Heartbeat-Alter.
- **Queue:** pending/running, Vorrat in Tagen, Anteil Varianten. Bei `_mt/_hf/_tf/_tfm/_gegen/_spaet`-Jobs ist „0 Kandidaten" das erwartete Ergebnis (CLAUDE.md, Queue-Stand Urlaub), kein Filter-Bug.
- **Kandidaten:** je ungelesenem Kandidaten eine Zeile mit Job, Bein, Marginal-Ergebnis und der **Buch-Lücke** (Regel 21.08.2026): an welcher Stufe hängt er (Prämisse → Gates → PBO → Zufallsdecke → Marginal „besser" → Next-Week-Buch + Ticket → Wochenend-Review → Deploy) und was fehlt konkret.
- **Leerlauf-Warnung:** steht `queue_empty` in der Inbox oder ist der Vorrat unter 2 Tagen, `alpha-scout` vorschlagen (Regel 21.08.2026), nicht mehr Grid auf altem Mechanismus.

`--seen-all` nur, wenn Max die Kandidaten abgehakt hat. Kandidaten mit „besser" gehen den normalen Weg (Quant-Team + `strategy-auditor`, dann Next-Week-Buch + Ticket), nicht aus diesem Skill heraus.
