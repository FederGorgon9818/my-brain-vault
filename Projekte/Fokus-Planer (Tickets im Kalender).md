---
date: 2026-10-27
tags: [projekt, kalender, tickets, automatisierung, fokus]
status: Konzept entschieden (27.10.2026), Bau offen
---

# 🗓️ Fokus-Planer: deine wichtigsten Tickets automatisch im Kalender

Auftrag Max 27.10.2026: Der Google-Kalender ist verbunden. Alles, was Max selbst tun muss, wird in Aufgaben aufgeschlüsselt und automatisch in seine festen Ticket-Blöcke gelegt. Nur das Wichtigste, je 15 Minuten oder so lange wie nötig, gerne parallel, von oben nach unten abzuarbeiten. Kommen neue Tickets, rutschen sie je nach Prio von selbst rein und der Rest verschiebt sich, ohne dass Max etwas sagen muss. Die Blöcke sind die Zeit für die bisherigen Probleme und Tickets. Verwandt: [[Ticket-Board (Jira-Stil)]], [[Hooks-Referenz]].

> ## Kurzfassung (entschieden 27.10.)
> - **Ticket-Blöcke:** Mi 21:30 bis 23:00 und Sa 14:30 bis 17:30 (die Samstag-Serie steht seit 27.10. im Kalender). **Donnerstag ist Kreativ-Tag für neue Alpha-Suche, dort kommen keine Tickets hin.**
> - **Nur das Wichtigste:** kritisch, rot, datum (fällig in 14 Tagen oder überfällig) und alles, worauf Claude wartet.
> - **Vollautomatisch:** Ein Skript auf der Box prüft alle 30 Minuten Tickets und Kalender. Ändert sich etwas, plant es neu und verschiebt die Termine im eigenen Kalender „Tickets“. Es braucht keine Tokens und läuft auch, wenn der PC aus ist.
> - **Aufschlüsseln beim Anlegen:** Jede Session schreibt Max-Arbeit als einzelne Schritte mit Dauer und Zeitfenster ins Ticket. Der Planer legt jeden Schritt als eigenen Termin.
> - **Dein Sprint bleibt deiner.** Der Planer schiebt nichts in einen Sprint und ändert keine Prio.

---

## 1. Kalender (gelesen 27.10., Zeitraum 27.10. bis 09.11.)

| Tag | Zeit | Länge | Rolle |
|---|---|---|---|
| Mi „Deep Work Fokus Time“ (Serie) | 21:30 bis 23:00. Der Termin beginnt um 21:15, bis 21:30 läuft „gemeinsames wachsen“ | 90 min | Ticket-Block |
| Do „Deep Work Fokus Time“ (Serie) | 21:00 bis 23:00 | 120 min | **Kreativ-Tag, neue Alpha-Suche, keine Tickets** |
| Sa „Deep Work Fokus Time“ (Serie ab 31.10., von Claude angelegt) | 14:30 bis 17:30 | 180 min | Ticket-Block |

Ticket-Zeit je Woche: 270 Minuten, also 18 Posten zu 15 Minuten.

Liegt ein anderer Termin im Block, plant der Planer drumherum. Beispiel 31.10.: „großes meeting“ geht bis 15:00, „Risk Guard Update verfügbarkeit“ beginnt um 16:00.

## 2. Was in den Kalender kommt

Ein **Posten** ist eine Sache, die du selbst tun musst. Drei Quellen (Stand 27.10.):

1. Tickets mit dir als Bearbeiter: 12 offen, davon 2 wichtig (AP440 MFFU-Support, fällig 05.11., und AP415 Auto-Login).
2. Tickets in den Board-Spalten „Max“ und „Entscheidung Max“ (z. B. AP258, AP204).
3. Max-Schritte in Claude-Tickets: 21 offen. Ein Teil davon ist längst erledigt, aber nie abgehakt worden (Häkchen sind bei 0 von 194 offenen Tickets gesetzt). Das wird vor dem Start einmal bereinigt.

**Filter (entschieden): nur das Wichtigste.** Das sind kritisch, rot, datum (fällig in den nächsten 14 Tagen oder überfällig) und jeder Schritt, auf den Claude wartet. Gelb und grün kommen nicht in den Kalender.

## 3. Reihenfolge, von oben nach unten

Fester Sortierschlüssel im Skript:

1. überfällig oder bis zum Blocktag fällig
2. kritisch
3. Claude wartet darauf (der Schritt blockiert ein Claude-Ticket)
4. im aktuellen Sprint
5. rot, dann datum nach Fälligkeit
6. bei Gleichstand dein Board-Rang

Jeder Termin heißt z. B. **„1 · AP440 MFFU-Support nachhaken (30 min)“**. Die Nummer zeigt die Reihenfolge. In der Beschreibung steht, was genau zu tun ist (der Schritt aus dem Ticket), woran du merkst, dass es fertig ist, und der Befehl oder Link, falls es einen gibt.

## 4. Aufschlüsseln und Dauer

- **Beim Anlegen, in jeder Session:** Max-Arbeit steht als einzelne Schritte im Ticket. Jeder Schritt hat eine Dauer im 15-Minuten-Raster und, falls nötig, ein Zeitfenster-Kürzel, z. B. `Max [30m][box-flat]: NT8 Historical Data laden …`. `ticket_tool` prüft das beim Anlegen und warnt, wenn etwas fehlt.
- Fehlt die Angabe trotzdem: 15 Minuten, bei RDP/NT8 30 Minuten.
- Alles über 60 Minuten wird schon beim Anlegen in Teilschritte zerlegt.
- Ist ein Ticket ohne Schritte auf dich geschrieben, wird es ein einzelner Posten mit der Ticket-Schätzung (heute nur bei 18 von 194 offenen Tickets gesetzt, sonst 15 Minuten).

## 5. Parallel: zwei Spuren

- **Hauptspur:** aktive Arbeit, nacheinander ab Blockbeginn.
- **Nebenspur:** Dinge, die nach dem Anstoßen allein laufen (NT8-Download, Bulk Export, großer Upload). Der Start (z. B. 10 min) steht in der Hauptspur, daneben ein Termin „läuft: …“ für die Laufzeit. In der Hauptspur geht es währenddessen mit dem nächsten Posten weiter.

Die Tickets liegen in einem eigenen Kalender, deshalb zeigt Google sie neben deinem Deep-Work-Termin. Der Block selbst bleibt, wie er ist.

## 6. Zeitfenster

| Kürzel | Bedeutung | Regel im Skript |
|---|---|---|
| `box-flat` | RDP, NT8, Deploy | frühestens 10 min nach dem Zwangs-Flat (15:55 ET), spätestens vor dem Asia-Start (19:00 ET). Im Mi-Block heißt das normal ab 22:05, also 55 min am Blockende. Diese Woche (USA stellen erst am 01.11. um) geht schon ab 21:05 der ganze Block. Samstag ganztägig |
| `werktags` | Support-Mails, Anrufe | nur im Mi-Block |
| `ab DATUM` | frühestens ab | Ticket-Feld Start |
| leer | jederzeit | |

Das Skript rechnet die Uhrzeiten je Datum selbst um, Sommer- und Winterzeit eingeschlossen.

## 7. Automatisch neu planen und verschieben

- **Alle 30 Minuten** bildet das Skript auf der Box einen Fingerabdruck aus den wichtigen Posten und deinen Block-Terminen. Ist er unverändert, passiert nichts. Hat er sich geändert, wird neu geplant, und es werden nur die Unterschiede geschrieben.
- **Neues wichtiges Ticket:** rutscht nach Prio rein, weniger Wichtiges rückt nach hinten oder in den nächsten Block.
- **Erledigt** (Ticket zu oder Schritt abgehakt): Der Termin verschwindet und der Rest rückt auf.
- **✅ vor dem Titel:** Der Planer hakt den Schritt im Ticket ab (auf der Box, der Quelle der Wahrheit) und schreibt eine Notiz dazu.
- **Termin gelöscht** heißt „heute nicht“, der Posten kommt im nächsten Block wieder.
- **Von Hand verschoben oder verlängert:** Der Termin bleibt, wo du ihn hingelegt hast, der Planer plant drumherum.
- **Läuft gerade ein Block,** wird nur noch das verschoben, was noch nicht begonnen hat.
- Vergangene Termine bleiben stehen (Verlauf).
- Was nicht mehr in den Block passt, steht am Blockende in einem Termin **„Rest: AP…, AP…“** und rutscht in den nächsten Block.

## 8. Technik (entschieden: Skript auf der Box)

- `engine/fokus_planer.py` läuft auf der Box alle 30 Minuten als Windows-Aufgabe, fensterlos und ohne Dauerläufer.
- Es liest `tasks.json` auf der Box und deine Blöcke im Hauptkalender, geschrieben wird nur in den Kalender „Tickets“.
- Jeder Posten bekommt je Block eine feste Termin-ID. So gibt es keine doppelten Termine, und es wird nur geschrieben, was sich wirklich geändert hat.
- **Google-Zugang:** Das Skript bekommt einen eigenen Zugang (Schlüsseldatei auf der Box, nie im Vault). Du gibst ihm einmal Lesezugriff auf deinen Hauptkalender und Schreibzugriff auf „Tickets“. Ob dafür bei einem privaten Gmail-Konto ein Dienstkonto reicht oder ein OAuth-Zugang mit Dauer-Token nötig ist, prüft `research-scout` beim Bau. Danach bekommst du eine genaue Klick-Anleitung.
- Mit `--dry-run` zeigt das Skript den Plan an, ohne etwas zu schreiben.
- Ist das Skript selbst kaputt, blockiert es nichts: Es schreibt ins Log und meldet sich per Telegram (maxbot), wenn es zweimal hintereinander scheitert.

## 9. Einmalig von dir

1. Den Kalender „Tickets“ anlegen: Google Kalender, links bei „Weitere Kalender“ auf „+“, dann „Neuen Kalender erstellen“.
2. Den Google-Zugang fürs Skript nach der Klick-Anleitung einrichten, die beim Bau kommt.

Danach läuft alles von allein.

## 10. Bau-Reihenfolge

1. `ticket_tool`: Schritte abhaken können (das Feld `guide_done` gibt es, ein Befehl fehlt), Dauer und Zeitfenster je Schritt, Prüfung beim Anlegen. Dazu eine Zeile in der CLAUDE.md und ein Hinweis im Prompt-Hook, damit jede Session Max-Arbeit gleich so anlegt.
2. Aufräumen: die 21 offenen Max-Schritte durchgehen und Erledigtes abhaken.
3. `research-scout`: Google-Zugang für ein Skript auf einem privaten Konto klären, dann die Klick-Anleitung für Max schreiben.
4. `engine/fokus_planer.py` mit Probelauf und Selbsttest (Reihenfolge, Zeitfenster, Sommerzeit, Überlauf, Verschieben, Handänderung, fremder Termin im Block).
5. Probelauf auf echten Daten, Max zeigen, dann scharf schalten.
6. Windows-Aufgabe auf der Box alle 30 Minuten, Hub-Eintrag (Automatiken), [[Hooks-Referenz]], diese Notiz auf „gebaut“. Abnahme durch den `verdict-auditor`.

## 11. Entscheidungen Max (27.10.2026)

1. Samstag 14:30 bis 17:30 als wöchentliche Serie: ja. Am 27.10. von Claude eingetragen („Deep Work Fokus Time“, ab 31.10.).
2. In Aufgaben aufschlüsseln, aber nur das Wichtigste. Alles soll vollautomatisch laufen: Neue Tickets werden je nach Prio eingetragen oder verschoben, ohne dass Max etwas sagen muss.
3. Mittwoch ab 21:30.
4. Technik: Skript auf der Box (Weg B). Der geplante Claude-Task am PC (Weg A) fällt weg.
5. **Donnerstag ist ein Kreativ-Tag, an dem Max neues Alpha sucht.** Dort plant der Planer keine Tickets ein.
