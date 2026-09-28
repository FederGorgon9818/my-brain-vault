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

## Laufend (AP251, erstmals 07.10.2026, dann monatlich um den 7.)
- [ ] Contabo September (kommt Monatsende)
- [ ] Claude Zahlungsbeleg September (nur Rechnung da)
- [ ] E8 150k vom 02.10. (AP214)
- danach jeden Monat: Contabo, Claude, neue Evals, Payouts → `_Eingang/`, Claude sortiert ein

**Warum:** vorweggenommene Betriebsausgaben vor der Gewerbeanmeldung — realistisch vierstelliger Betrag, verfällt ohne Beleg.
