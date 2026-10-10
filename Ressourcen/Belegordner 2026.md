---
tags: [gewerbe, steuern, belege]
created: 2026-08-11
---

# Belegordner 2026 (AP36 erledigt, laufend AP251)

Zentraler Ablageort für alle Gewerbe-Belege: `C:\Users\maxlk\Documents\Gewerbe\Belege\2026\`

## Struktur
| Ordner | Inhalt |
| --- | --- |
| `_Eingang/` | Reinwerfen ohne Sortieren, Claude sortiert ein (seit 24.09.26) |
| `Challenges/` | Prop-Firm-Fees (E8, Bulenox, ...), auch verlorene |
| `Infrastruktur/` | VPS, TradingView, Datenfeeds, Software, Kurse |
| `Hardware/` | PC, Monitore, Peripherie |
| `Payouts/` | Auszahlungsnachweise |

Dazu: `EUeR-2026.csv` (eine Zeile pro Beleg) und `README.md` mit Namenskonvention `YYYY-MM-DD_Anbieter_Betrag.pdf`.

## Workflow
Wenn Max einen Beleg gibt (Datei/Screenshot), sortiert Claude ihn **automatisch** ein: umbenennen nach Konvention, in den passenden Unterordner legen, Zeile in die EÜR-CSV schreiben (USD → EUR zum Tageskurs, Kurs in Notiz-Spalte).

## Rückwirkend gesammelt (AP36, erledigt 24.09.26)
10 Zeilen in `EUeR-2026.csv`, zusammen **666,47 €** (Juni bis Sept.). Liegt komplett für den Termin mit Freundin ([[Gespräch mit Freundin (Steuer & Gründung)]], AP235).
- [x] E8 Signature 50k, 113 USD (Liste 150, Rabatt), 28.07.2026 → `Challenges/` (24.09.)
- [x] FundedNext Flex 50k, 2x 69,99 USD (Coupon AUGFLEX, nicht 79,99), 02.09.2026 → `Challenges/` (24.09.)
- [x] Bulenox EOD 50k, 43,75 USD (Liste 175, Rabatt), 24.07.2026 → `Challenges/` (24.09.), Sunk Cost aus [[Strategie-Logbuch]] #042
- [x] Contabo Juli (41,08 €, ab 21.07.) + August (31,06 €) → `Infrastruktur/` (24.09.). Real 31,06 €/Monat, nicht 38 €. Offen: Rechnung Ende September. Prüfen, woher das Guthaben kam (im Sept. nur 16,06 € abgebucht)
- [x] Claude Pro Juni + Max 5x Juli/Aug/Sept → `Infrastruktur/` (24.09.). Offen: Zahlungsbeleg Sept. (nur Rechnung da), Geschäftsanteil mit Freundin klären
- Hardware, Kurse, TradingView 2026: nichts abgegeben. Falls doch etwas war, nachreichen.

## Oktober-Nachtrag (AP251, einmalig bis 07.10.2026, danach löschen)
- [x] Contabo September (Rechnung 30.09., abgelegt 02.10.)
- [ ] Claude Zahlungsbeleg September (nur Rechnung da)
- [ ] Funded Futures Network 05.10.2026 (292,50 $): PayPal-Beleg liegt, **Rechnung von FFN fehlt** (Plan/Kontogröße unklar)
- [ ] E8 150k (AP214): noch nicht gekauft, Kauf nach E8-Antwort. Rechnung geht an `Max.Kho@web.de`.
- danach jeden Monat: Contabo, Claude, neue Evals, Payouts → `_Eingang/`, Claude sortiert ein

## Soll-Plan: was jeden Monat reinkommen muss (Stand 05.10.2026)
Abgleich am 28. jedes Monats: steht für jede Zeile ein Beleg im Ordner? Dafür kommt automatisch ein Ticket „Belege des Monats sammeln“ (Prio Hoch, `wiedervorlagen.json` → `auto_check.py`, seit 05.10.2026).

| Posten | Betrag | Kommt am | Mail an | Ordner |
| --- | --- | --- | --- | --- |
| Anthropic Claude Max 5x | 107,10 € (90,00 netto) | ~6. | ? | Infrastruktur (Rechnung + Zahlungsbeleg) |
| Contabo VPS 6 | 31,06 € (26,10 netto) | Rechnung ~30./31., Einzug ~5. | ? | Infrastruktur |
| TradingView Essential | 17,79 € (14,95 netto), PayPal | 11. (nächste 11.10.) | maxlkho4@gmail | Infrastruktur, **nur wenn geschäftlich** (siehe unten) |
| Neue Evals / Resets | je nach Kauf | beim Kauf | Max.Kho@web.de | Challenges |
| Payouts | je nach Auszahlung | bei Auszahlung | Firma | Payouts (Einnahmen!) |
| Databento (geplant) | noch offen | ab Account | ? | Infrastruktur |

## Fehlende Belege aus dem Gmail (Fund 05.10.2026, maxlkho4@gmail.com)
Alles Trading-Werkzeuge, die bisher **nicht** im Ordner liegen. Ob sie als vorweggenommene Betriebsausgaben zählen, klärt Max mit Freundin (AP235). PDFs hängen jeweils an der Mail.

| Datum | Anbieter | Was | Betrag | Status |
| --- | --- | --- | --- | --- |
| 10.01., 10.02., 10.03., 10.04. | TradingView | Abo (Kaufbeleg) | je ? (Sept. war 17,79 €) | fehlt, Mai nicht in der Mail gefunden |
| 11.06., 11.07., 11.08., 11.09. | TradingView | Essential | 17,79 € (Sept. geprüft) | fehlt |
| 21.06., 19.07. | TradingView | CME-Echtzeitdaten | 8,33 € | fehlt, Aug. Zahlung gescheitert, Abo am 21.08. deaktiviert |
| 04.06. | Deepcharts | Bestellung DPC-00AF79-0010 | ? | fehlt |
| 21.06. | Deepcharts (Paddle) | Full, 3 Monate | 349,03 $ | fehlt, Abo am 21.09. ausgelaufen |
| 04.06. | Volumetrica (Paddle) | dxFeed CME Datenfeed | 34,51 $ | fehlt |
| 10.06. | Bookmap | 2 Zahlungen (#EJDCC, #44JSY) | 58,31 $ + 40,46 $ | fehlt |
| 06.09. | Anthropic | Zahlungsbeleg Claude Sept. | 107,10 € | fehlt (Rechnung liegt) |

**Zu klären (eher privat?):** LinkedIn Premium Career (31.08.), Amazon USB-C-Dockingstation (26.06., Hardware?). QuantPad (Stripe) und Quant Data LLC: nur gescheiterte Abbuchungen gefunden (QuantPad Aug. ~152 €, Quant Data Juni ~68 €). Falls vorher erfolgreich bezahlt wurde, liegen die Belege in einem anderen Postfach.

**Nicht durchsuchbar:** `Max.Kho@web.de` (dorthin gehen die Prop-Rechnungen) und das Postfach der Claude-/Contabo-Rechnungen. Dort selbst nach Rechnungen 2026 schauen. *(Überholt seit 05.10.2026, siehe unten: das web.de-Postfach ist angebunden und durchsuchbar, siehe [[web.de-Postfach]]. Das Postfach der Claude-/Contabo-Rechnungen ist davon nicht berührt.)*

**Warum:** vorweggenommene Betriebsausgaben vor der Gewerbeanmeldung — realistisch vierstelliger Betrag, verfällt ohne Beleg.

## Aus der CLAUDE.md (05.10.2026): Monats-Ticket und Beleg-Regel

Aus dem Abschnitt „Belege: jeden Monat ein Sammel-Ticket" (Regel Max, 05.10.2026) übernommen.

- **Am 28. jedes Monats legt der Auto-Check automatisch ein Ticket „Belege des Monats sammeln" an:** Prio Hoch, Board Privat, im Backlog. Quelle: Eintrag `belege_monatsende` in `engine/wiedervorlagen.json`, ausgelöst von `auto_check.py` (läuft am PC alle 30 Min).
- **PC am 28. aus:** das Ticket kommt beim nächsten Lauf im selben Monat.
- **Ticket löschen, wenn der Monat vollständig ist.** Ein gelöschtes Ticket kommt im selben Monat nicht wieder, der nächste Monat kommt von selbst.
- **Soll-Plan** (was jeden Monat reinkommen muss, was noch fehlt): Abschnitt „Soll-Plan" weiter oben und die Fehlliste.
- **Bei jedem Kauf, den Max erwähnt, die Rechnung direkt mit anfordern und einsortieren, nicht erst am Monatsende.**
