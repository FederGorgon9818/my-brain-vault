---
tags:
  - system/inbox
  - gründung
erstellt: 2026-09-29
status: auszuführen in der nächsten PC- oder Laptop-Session
---
# 🎫 Gründungs-Tickets in die Sprints (Auftrag Max, 29.09.2026)

⬅️ [[Brain Dump]] · [[Unternehmensgründung Entscheidung]] · [[Gründung Zeitplan]] · [[Ticket-Board (Jira-Stil)]]

> [!important] Auftrag von Max, schon freigegeben
> Max am 29.09.2026: die nächsten Gründungsschritte jeweils in den Sprint der passenden Woche eintragen, damit sie automatisch in Arbeit kommen. Die Cloud-Session kam weder auf den PC noch auf die Box und konnte es deshalb nicht selbst tun. **Die nächste Session mit Engine-Zugriff führt das aus, ohne nochmal zu fragen.** Nur die Stundenschätzungen sind Vorschläge, die darf Max im Lab ändern. Danach diese Notiz löschen, die Zeile im [[Brain Dump]] entfernen und das Ergebnis in die Daily Note schreiben.

**Zur Sprint-Regel vom 29.09. (CLAUDE.md, „Max plant seine Sprints selbst“):** Das hier ist kein Planning von Claude aus eigenem Antrieb. Max hat ausdrücklich angesagt, diese Schritte in die Sprints der jeweiligen Woche einzutragen, das ist also auf Zuruf. Ist S2026-41 inzwischen von Max selbst gefüllt, nur ergänzen und nichts herausnehmen.

**Voraussetzung:** AP267 (Box-Migration des Ticket-Boards) ist erledigt, sonst gibt es S2026-41 noch nicht. Ist AP267 offen, zuerst Max fragen, ob jetzt migriert wird. Alles läuft über `ticket_tool.py` mit `--who max`, nie `tasks.json` von Hand bearbeiten. Vorher `sprint list` und `show` für jedes AP, damit nichts doppelt entsteht. Weicht ein Ticket von dieser Beschreibung ab, kurz Max fragen.

## Stand
- Gewerbeanmeldung (GewA 1) am 29.09.2026 per Mail an die VG Oberneuching geschickt, Beginn 01.10.2026, Nebenerwerb. Empfangsbestätigung und Gebührenrechnung kommen noch.
- Das Beginndatum ist damit entschieden. Aus AP235 ist noch offen: Kleinunternehmer oder Regelbesteuerung, Einkunftsart, Rücklage.

## Plan je Woche

| Woche | Sprint | Ticket | Was | Start / Fällig | h (Vorschlag) |
|---|---|---|---|---|---|
| bis So 04.10. | noch keiner (erster Sprint ab 05.10.) | AP34 | nach „Wartet“: Empfangsbestätigung und Gebührenrechnung der VG abwarten, sonst anrufen (08123 9326-60). Bestätigung ablegen, Gebühr zahlen. Erledigt, sobald die Bestätigung da ist | fällig Fr 02.10. | 0,5 |
| bis So 04.10. | noch keiner | AP214 | E8 150k kaufen (Ticket besteht). Notiz: Beleg sofort in `_Eingang`, erste Ausgabe im laufenden Gewerbe | fällig Fr 02.10. | wie gehabt |
| 05. bis 11.10. | S2026-41 | AP251 | Belege September einsortieren, dazu Gewerbe-Gebühr und E8 150k | fällig Mi 07.10. | 0,5 |
| 05. bis 11.10. | S2026-41 | AP235 | Termin mit der Freundin: Kleinunternehmer oder Regelbesteuerung, Einkunftsart, Rücklage | fällig So 11.10. | 2 |
| 05. bis 11.10. | S2026-41 | AP37 | Geschäftskonto und Rücklagenkonto, wartet auf den Gewerbeschein (AP34) | fällig So 11.10. | 1,5 |
| 05. bis 11.10. | S2026-41 | AP34 | nur falls die Bestätigung bis dahin noch fehlt | | |
| 12. bis 18.10. | S2026-42 | AP35 | ELSTER-Fragebogen zur steuerlichen Erfassung, wartet auf AP235. Zwei Wochen Puffer bis zur Frist | Start 12.10., fällig Fr 30.10. (Frist rechnerisch Mo 02.11., weil der 01.11. Sonntag und Allerheiligen ist) | 1,5 |

S2026-42 anlegen, falls es ihn noch nicht gibt. Ziel und Kapazität vorläufig setzen und im Planning am So 11.10. mit Max festlegen.

**Backlog mit Datum (das Sonntags-Planning holt sie in die richtige Woche):**

| Ticket | Was | Start / Fällig | h |
|---|---|---|---|
| AP236 | arbeitsuchend melden bei der Agentur für Arbeit, dabei die ALG-Frage für Juli/August klären | Start 01.03.2027, fällig 03.04.2027 | 1 |
| **neu** | Steuererklärung 2026 mit Anlage EÜR (Verlust gegen Gehalt verrechnen). Board privat, Prio orange | fällig 31.03.2027 | 4 |
| AP249 | Anbieter auf Firmenkunde umstellen, wartet auf AP235 und die USt-IdNr. | kein Datum | 1 |
| **neu** | GEWO HR informieren, bevor Content oder Coaching Geld bringt (die Genehmigung vom 23.09. deckt das nicht, gilt solange der Job läuft, also bis 03.07.2027). Board privat, Prio gelb | Auslöser: erste Einnahme absehbar | 0,5 |
| AP258 | Schritt ergänzen: W-8BEN im E8-Payout-Bereich vor dem ersten Payout | kein Datum | |

**Verknüpfungen:** AP34 blocks AP37 · AP235 blocks AP35 · AP235 blocks AP249

## Notiz für AP35 (Werte für den Fragebogen)
Mein ELSTER → Formulare & Leistungen → Alle Formulare → „Fragebogen zur steuerlichen Erfassung“ für Einzelunternehmen. Finanzamt Erding. Tätigkeit, Beginn (01.10.2026) und Adresse wie in der Gewerbeanmeldung. Gewinnermittlung EÜR. Gewinn 2026: Verlust, ohne Hardware grob 2.000 bis 2.500 €, mit Hardware im Dezember eher 4.500 bis 5.000 €. Gewinn 2027: 0 €. Umsatz 2026 und 2027: 0 €. Gehalt, falls gefragt: Werte aus der Lohnabrechnung. Kleinunternehmer: Entscheidung aus AP235. Ist-Versteuerung: ja. USt-IdNr.: ja. Bankverbindung: Geschäftskonto aus AP37, sonst erst Privatkonto.

Tätigkeitstext wortgleich zur Anmeldung (ohne die Markierung „Schwerpunkt“):
> Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten und zur Erstellung von Handelsstrategien; Bereitstellung der daraus gewonnenen Daten und damit verbundene Dienstleistungen für ausländische Auftraggeber; Softwareentwicklung und IT-Dienstleistungen; Erstellung und Vermarktung digitaler Inhalte sowie Schulungen und Coaching zu Softwareentwicklung, KI-Automatisierung und systematischer Finanzmarktanalyse

## Befehle (Engine-Ordner, `PYTHONIOENCODING=utf-8`)
Flags vorher mit `--help` prüfen. `start` und `due` gibt es seit dem Jira-2.0-Umbau als Felder, falls die Kommandozeile sie nicht setzt, im Lab-Panel eintragen.
```
python ticket_tool.py sprint list
python ticket_tool.py show AP34        # ebenso AP35 AP37 AP214 AP235 AP236 AP249 AP251 AP258
python ticket_tool.py move AP34 waiting
python ticket_tool.py note AP34 "29.09. per Mail an VG Oberneuching, Beginn 01.10.2026. Wartet auf Empfangsbestätigung und Gebührenrechnung, Fr 02.10. sonst anrufen"
python ticket_tool.py note AP214 "Beleg sofort in _Eingang, erste Ausgabe im laufenden Gewerbe (Beginn 01.10.)"
python ticket_tool.py link AP34 blocks AP37
python ticket_tool.py link AP235 blocks AP35
python ticket_tool.py link AP235 blocks AP249
python ticket_tool.py edit AP251 --hours 0.5
python ticket_tool.py edit AP235 --hours 2
python ticket_tool.py edit AP37 --hours 1.5
python ticket_tool.py edit AP35 --hours 1.5
python ticket_tool.py edit AP236 --hours 1
python ticket_tool.py sprint plan S2026-41 AP251 AP235 AP37
python ticket_tool.py sprint new --start 2026-10-12 --goal "<mit Max>" --capacity <h>
python ticket_tool.py sprint plan S2026-42 AP35
python ticket_tool.py note AP35 "<Werte aus dem Abschnitt oben>"
python ticket_tool.py note AP258 "Schritt: W-8BEN im E8-Payout-Bereich vor dem ersten Payout"
python ticket_tool.py new "Steuererklärung 2026 mit Anlage EÜR" --board privat --prio orange --hours 4 --why "Verlust 2026 gegen Gehalt verrechnen, erste Erklärung mit Gewerbe"
python ticket_tool.py new "GEWO HR informieren vor ersten Einnahmen aus Content/Coaching" --board privat --prio gelb --hours 0.5 --why "Tätigkeit seit 29.09. inkl. Content/Coaching, Nebentätigkeits-Genehmigung deckt das nicht"
```
Danach Fällig/Start je Tabelle setzen, `python ticket_tool.py find "board:privat sprint:aktuell"` zur Kontrolle, Ergebnis in die Daily Note.
