---
date: 2026-10-27
tags: [projekt, kalender, tickets, automatisierung, fokus]
status: Konzept, Entscheidungen bei Max
---

# 🗓️ Fokus-Planer: deine Tickets automatisch in den Fokus-Blöcken

Auftrag Max 27.10.2026: Der Google-Kalender ist verbunden. Claude soll zu festen Zeiten alles, was Max selbst tun muss, in Tickets aufschlüsseln und automatisch in die festen Fokus-Zeiten legen (Mi und Do Deep Work, Sa 14:30 bis 17:30 jede Woche). Je Aufgabe 15 Minuten oder so lange wie nötig, gerne parallel, in einer Reihenfolge, die er von oben nach unten abarbeiten kann und bei der das Wichtigste immer zuerst drankommt. Erst Konzept, gebaut wird nach seinem OK. Verwandt: [[Ticket-Board (Jira-Stil)]], [[Hooks-Referenz]].

> ## Kurzfassung
> - **Ein eigener Kalender „Tickets“** liegt über deinen Blöcken. Je Aufgabe ein Termin mit Nummer, Ticket und Dauer. Deine eigenen Termine fasst der Planer nie an.
> - **Zweimal pro Woche** (Di 20:00 für Mi und Do, Fr 20:00 für Sa) sammelt Claude ein, was du tun musst, legt fehlende Tickets an, schätzt die Dauer, und ein festes Skript füllt die Blöcke. Kurz vor jedem Block gibt es einen Abgleich.
> - **Reihenfolge immer gleich:** fällig zuerst, dann kritisch, dann „Claude wartet auf dich“, dann rot und datum. Gelb nur als Auffüller.
> - **NT8/RDP-Aufgaben** landen nur in der Zeit, in der alle Konten flat sind.
> - **Dein Sprint bleibt deiner.** Der Planer schiebt nichts in einen Sprint und ändert keine Prio.

---

## 1. Was dein Kalender zeigt (gelesen 27.10., Zeitraum 27.10. bis 09.11.)

| Block | Zeit | Länge | Was auffällt |
|---|---|---|---|
| Mi „Deep Work Fokus Time“ (Serie) | 21:15 bis 23:00 | 105 min | „gemeinsames wachsen“ läuft bis 21:30, ab da 90 min frei |
| Do „Deep Work Fokus Time“ (Serie) | 21:00 bis 23:00 | 120 min | frei |
| Sa Fokus-Block | 14:30 bis 17:30 (Annahme) | 180 min | **steht noch nicht im Kalender.** Am 31.10. überlappen „großes meeting“ (bis 15:00) und „Risk Guard Update verfügbarkeit“ (ab 16:00) |

Zusammen 390 bis 405 Minuten pro Woche, das sind rund 26 Aufgaben zu 15 Minuten.

Du legst dir abends schon selbst Aufgaben-Termine an (z. B. „MaxBookHost Algo“ und „Max T2“ am 27.10.). Der Planer macht genau das, nur automatisch und sortiert.

## 2. Was in den Kalender kommt

Ein **Posten** ist eine Sache, die du selbst tun musst. Drei Quellen (Stand 27.10.):

1. Tickets mit dir als Bearbeiter: 12 offen, davon 2 wichtig (AP440 MFFU-Support, fällig 05.11., und AP415 Auto-Login).
2. Tickets in den Board-Spalten „Max“ und „Entscheidung Max“ (z. B. AP258, AP204).
3. Max-Schritte in Claude-Tickets: 21 offen (z. B. AP288 Schritt 1, Kontonummer nennen). Ein Teil davon ist längst erledigt, weil Schritte nie abgehakt werden (Häkchen bei 0 von 194 offenen Tickets gesetzt). Das muss vor dem Start bereinigt werden.

**Filter „wichtig“:** kritisch, rot, datum (fällig in den nächsten 14 Tagen oder überfällig) und jeder Schritt, auf den Claude wartet. Gelb nur, wenn danach noch Platz ist (Frage 2). Grün nie.

**Dein Sprint bleibt deiner.** Was in deinem aktuellen Sprint liegt, rückt nach vorn. Sonst plant der Planer nichts in Sprints und startet keinen.

## 3. Reihenfolge, von oben nach unten

Fester Sortierschlüssel im Skript:

1. überfällig oder bis zum Blocktag fällig
2. kritisch
3. Claude wartet darauf (Schritt blockiert ein Claude-Ticket)
4. im aktuellen Sprint
5. rot, dann datum nach Fälligkeit, dann gelb
6. bei Gleichstand dein Board-Rang

Jeder Termin heißt z. B. **„1 · AP440 MFFU-Support nachhaken (30 min)“**. Die Nummer zeigt die Reihenfolge. In der Beschreibung steht, was genau zu tun ist (der Schritt aus dem Ticket), woran du merkst, dass es fertig ist, und der Befehl oder Link, falls es einen gibt.

## 4. Dauer

- Claude schätzt jeden Posten im 15-Minuten-Raster (15, 30, 45, 60) und schreibt die Schätzung ins Ticket. Heute ist sie nur bei 18 von 194 offenen Tickets gesetzt.
- Ohne Schätzung: 15 Minuten, RDP/NT8-Aufgaben 30 Minuten.
- Alles über 60 Minuten wird in Teilschritte zerlegt, die einzeln in den Kalender kommen. Das ist das „Aufschlüsseln“.

## 5. Parallel: zwei Spuren

- **Hauptspur:** aktive Arbeit, nacheinander ab Blockbeginn.
- **Nebenspur:** Dinge, die nach dem Anstoßen allein laufen (NT8-Download, Bulk Export, großer Upload). Der Start (z. B. 10 min) steht in der Hauptspur, daneben ein Termin „läuft: …“ für die Laufzeit. Die Hauptspur geht währenddessen mit dem nächsten Posten weiter.

Weil die Tickets in einem eigenen Kalender liegen, zeigt Google sie neben deinem Deep-Work-Termin. Der Block selbst bleibt, wie er ist.

## 6. Zeitfenster

Manche Posten gehen nur zu bestimmten Zeiten. Das Ticket-Feld „wann“ ist heute Freitext (bei 88 von 194 gesetzt). Claude übersetzt es beim Einsammeln in ein festes Kürzel:

| Kürzel | Bedeutung | Regel im Skript |
|---|---|---|
| `box-flat` | RDP, NT8, Deploy | frühestens 10 min nach dem Zwangs-Flat (15:55 ET), spätestens vor dem Asia-Start (19:00 ET). Diese Woche (USA stellen erst am 01.11. um) heißt das 21:05 bis 00:00, danach wieder 22:05 bis 01:00. Samstag ganztägig |
| `werktags` | Support-Mails, Anrufe | nur Mi- und Do-Block |
| `ab DATUM` | frühestens ab | Ticket-Feld Start |
| leer | jederzeit | |

Die Uhrzeiten rechnet das Skript je Datum selbst um, nie im Kopf. Folge: Im Mi- und Do-Block passen NT8-Aufgaben in normalen Wochen nur ans Ende (ab 22:05), am Samstag überall.

## 7. Überlauf und „erledigt“

- Was nicht mehr in den Block passt, rutscht in den nächsten. Am Blockende steht ein Termin **„Rest: AP…, AP…“** mit den übrigen Posten.
- **Erledigt melden:** Ticket schließen wie bisher, oder im Kalender ein ✅ vor den Titel setzen. Dann hakt der nächste Lauf den Schritt im Ticket ab und schreibt eine Notiz dazu.
- **Termin gelöscht** heißt „heute nicht“. Der Posten kommt beim nächsten Lauf wieder.
- **Von Hand verschoben oder verlängert:** Der Planer lässt den Termin in Ruhe und plant drumherum.
- Vergangene Termine bleiben stehen (Verlauf). Neu geplant wird nur, was noch kommt.

## 8. Ablauf der Automatik

| Wann | Was |
|---|---|
| Di 20:00 | voller Lauf für Mi und Do |
| Fr 20:00 | voller Lauf für Sa |
| 2 Stunden vor jedem Block | Abgleich: Erledigtes raus, neue dringende Posten rein |

Ein voller Lauf hat fünf Schritte:

1. **Einsammeln (Claude):** Tickets von der Box holen, Daily Notes der letzten Tage und Session-Übergaben nach „Max muss …“ durchsuchen. Fehlt ein Ticket, legt Claude es im Backlog an, nie in einem Sprint.
2. **Aufschlüsseln (Claude):** Posten über 60 Minuten in Teilschritte zerlegen, Dauer und Zeitfenster-Kürzel setzen.
3. **Planen (Skript `engine/fokus_planer.py`):** liest Tickets und deine Blöcke und rechnet Reihenfolge, Uhrzeiten, Spuren und Überlauf. Es gibt einen Probelauf, der nur anzeigt und nichts schreibt.
4. **Schreiben:** Termine im Kalender „Tickets“ anlegen, ändern oder löschen. Nur dort.
5. **Melden:** eine Zeile in die Daily Note, dazu ein Eintrag im Hub (Automatiken).

## 9. Technik: zwei Wege

| | **Weg A: geplanter Claude-Task** (Empfehlung zum Start) | **Weg B: Skript auf der Box** |
|---|---|---|
| Läuft | in der Desktop-App am PC. Ist sie zu, läuft der Task beim nächsten Start nach | immer, auch bei PC aus |
| Kalender | über den Connector, den du gerade verbunden hast | direkt über die Google-Kalender-Schnittstelle. Braucht einmalig einen Zugang für das Skript (Schlüssel auf der Box) |
| Einsammeln und Aufschlüsseln | ja | nein, das kann nur Claude |
| Tokens | ein sonnet-Lauf je Zeile der Tabelle oben | keine |
| Dein Aufwand | einmal den Kalender „Tickets“ anlegen | zusätzlich den Google-Zugang einrichten |

**Empfehlung:** Weg A jetzt bauen. Kommen die Läufe zu oft verspätet, weil der PC aus war, wandern nur Planen und Schreiben auf die Box. Das Einsammeln bleibt bei Claude.

**Einmalig von dir:** Der Connector kann keinen neuen Kalender anlegen. Den Kalender „Tickets“ legst du selbst an: Google Kalender, links bei „Weitere Kalender“ auf „+“, dann „Neuen Kalender erstellen“. Danach liest Claude die ID über den Connector.

## 10. Bau-Reihenfolge nach deinem OK

1. `ticket_tool`: Schritte abhaken können (das Feld dafür gibt es, ein Befehl fehlt) und die Felder Dauer und Zeitfenster-Kürzel.
2. Einmal aufräumen: die 21 offenen Max-Schritte durchgehen und Erledigtes abhaken.
3. `engine/fokus_planer.py` mit Probelauf und Selbsttest.
4. Probelauf auf echten Daten, dir zeigen, erst danach in den Kalender schreiben.
5. Geplante Tasks anlegen (Di 20:00, Fr 20:00, Abgleich vor den Blöcken).
6. Hub-Eintrag, [[Hooks-Referenz]], diese Notiz auf „gebaut“. Abnahme durch den verdict-auditor.

## 11. Offene Fragen an Max

1. Samstag 14:30 bis 17:30 als wöchentliche Serie eintragen?
2. Nur wichtige Posten, oder gelb als Auffüller dazu?
3. Mittwoch ab 21:15 (Blockbeginn) oder ab 21:30 (nach „gemeinsames wachsen“)?
4. Weg A (geplanter Claude-Task am PC) zum Start?
