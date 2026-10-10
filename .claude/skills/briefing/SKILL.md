---
name: briefing
description: Kurz-Briefing "was steht an / wo war ich stehengeblieben" aus den letzten Daily Notes, aktiven Projekten und den dringendsten Tickets. Nutzen, wenn Max /briefing aufruft oder sinngemäß fragt "was steht an?", "wo war ich?", "gib mir ein Briefing".
---

# Skill: Briefing

Die „Kontext bei Bedarf"-Regel aus der CLAUDE.md als fester Ablauf. Nur lesen, nichts ändern.

## Schritte

1. **Daily Notes:** die letzten 3 Dateien in `Daily Notes/` (nach Dateiname sortiert, neueste zuerst) vollständig lesen. Nicht nur die Kurzfassung aus dem Session-Start-Hook.
2. **Projekte:** in `Projekte/*.md` das Frontmatter (`status`) lesen; nur aktive Projekte zählen. `Ticket-Epics.md` nur dann, wenn es jünger als 14 Tage ist (sonst als „veraltet" markieren).
3. **Tickets:** aus `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (JSON-Liste) alle mit `status` nicht `done`/`erledigt`/`closed` und `prio` in `kritisch`/`rot`/`orange` (Prio-Skala 02.10.2026: kritisch = Sehr hoch, rot/orange = Hoch), dazu alle `datum`-Tickets mit `due` in den nächsten 7 Tagen oder überfällig, dazu maximal 5 gelbe mit dem nächsten `when`. Läuft die Session NICHT auf der Box (Hostname `vmd202078`), vorher `python discovery/inbox_tool.py --pull` im Engine-Ordner, weil die Box die Quelle der Wahrheit ist.
4. **Strategie-Logbuch:** nur den neuesten Eintrag (letzte `#NNN`-Überschrift) in `Bereiche/Strategie-Logbuch.md` per Grep, nicht die ganze Datei.

## Ausgabe

Kurz und in dieser Reihenfolge, Deutsch, keine Textwand:

- **Stand:** 3 bis 5 Sätze, was zuletzt lief (aus den Daily Notes).
- **Dringend:** Sehr hoch zuerst (eigens markieren), dann Hoch und fällige Datum-Tickets, je mit `when`/`due` und einem Halbsatz.
- **Nächste Schritte:** was die letzten Notes als „offen" markiert haben.
- **Blocker:** was gerade auf Max wartet (Support-Antworten, Entscheidungen, PC an).
- Zum Schluss der übliche Modell-/`/clear`-Hinweis.

Keine Änderungen an Dateien, keine Agents starten. Wenn Max danach eine Aufgabe nennt, gelten die normalen Regeln (Offene Fragen zuerst).
