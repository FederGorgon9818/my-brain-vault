---
tags:
  - ressource/paper
  - trading/gap
erstellt: 2026-07-07
---
# 🕳️ Gap-Fill Research (Synthese)

⬅️ [[_Paper-Registry]] · [[Strategie-Katalog]] · [[Alpha-Konzepte]]

> [!important] Kern-Ergebnis vorweg
> **Reines Gap-Fade auf dem Index (NQ/ES) ist KEINE Edge.** Akademisch auf MNQ falsifiziert + deckt sich mit unserem schwachen Overnight-Fade. Die ~60% Fill-Rate ist eine Illusion (ungefüllte Gaps laufen weit davon). Die Edge, wenn überhaupt, liegt in der **Konditionierung**: Gap-Größe, Richtung (Continuation statt Fade), Wochentag, Overnight-Kontext.

## Gelesene Quellen
1. **Mesfin, "Structural Limits of OHLCV Intraday Signals in MNQ" (arXiv 2605.04004)** ⭐ wichtigster. 5-Min MNQ, 2021-2025, 14 Signal-Familien, institutioneller Standard (T>2, N≥30, netto nach Kosten, Walk-Forward).
2. **tradingstats.net** – 2.791 NQ-Tage (2014-24) + 2.646 ES-Tage: Fill-Raten nach Größe/Richtung/Wochentag/Timing.
3. **Della Corte & Kosowski, "Overnight-Intraday Reversal Everywhere" (SSRN)** – CO-OC-Reversal ~0,29%/Woche in Index-Futures (wöchentlich, nicht intraday-Gap).
4. **MDPI "Stat-Arb Mean-Reverting Overnight Gaps S&P 500"** – Gap-MR signifikant ~120 Min nach Open, aber auf **Einzelaktien** (cross-sectional, Korb nötig).
5. **"Filling Open Price Gap Intraday: DJIA Index Stocks" (ResearchGate)** – Fill-Timing auf Einzelaktien.
6. **"Profitable Mean Reversion After Large Price Drops" (SSRN)** – Contrarian nach großen Drops, Index-Ebene, längerer Horizont.

## Die harten Zahlen (profit-relevant)
**Fill-Raten (NQ, tradingstats):**
- Gesamt nur **~60%** füllen 100% bis Close (kaum über Zufall). Gap-Down füllt etwas öfter (62%) als Gap-Up (59%).
- **Größe ist alles:** winzige Gaps (<0,3×ATR) **78-93%** Fill · große Gaps (>1,2×ATR) nur **~8%** Fill.
- **Timing:** Median NQ-Fill 18 Min · winzig 7 Min · klein 74 Min. Erste 5-Min-Bar füllt 1/3 der NQ-Gaps. Erste 2,5h = 82-86% aller Fills. **Nachmittags kaum noch.**
- **Wochentag:** Mi 63,5% · Di 62,8% · Do 62,4% · **Mo 53,9% (schlechtester, Wochenend-Sentiment).**
- **Kontext:** Gap-Down + Overnight-Rally → **83%** Fill (aber selten, 30 Fälle). Winzig-Gap + 15-Min-Bestätigung → **93%** (773 Fälle).

**Falsifikation MNQ (Mesfin, Table 5) – der Realitäts-Check:**
| Strategie | Entry | N | Netto (pts) | T-Stat | Win | Verdict |
|---|---|---|--:|--:|--:|---|
| Gap-Fill Fade | 09:30 | 238-245/J | −1,92 | −0,44 | 48,1% | ❌ FAIL (Rauschen) |
| Gap-Fill Fade | 09:45 | 238-245/J | −1,31 | −0,32 | 47,2% | ❌ FAIL |
| Gap-Fill Fade | 10:00 | 238-245/J | −2,24 | −0,59 | 47,9% | ❌ FAIL |
| **Gap-Continuation Short** (Kalman v>2,5) | 09:30 | 22 | **+14,52** | **+3,23** | **68,2%** | ⚠️ nur N<30 |

→ **Fade scheitert bei jedem Einstieg.** Das einzige positive Signal war **Continuation (mit dem Gap gehen)**, short auf Gap-Downs, mit **Momentum-/Velocity-Filter** — aber selten (~7/J) und **abnehmend** (12/6/4 Trades in 22/23/24, wohl 2022-Vola-Artefakt).

## Was das bedeutet (nutzbar für uns)
1. **Nicht faden auf dem Index.** Deckt sich mit unserer Insight-Regel #1 (NQ = continuation).
2. **Größen-Split ist der Hebel:** kleine Gaps neigen zum Fill (fade-bar), große laufen weiter (continuation-bar). Ein **größen-konditioniertes** Setup ist der einzig ehrliche Weg.
3. **Continuation + Velocity-Filter** ist die aussichtsreichste Richtung, aber Frequenz ist das Problem (selten).
4. **Wochentag- & Timing-Filter** (Di/Mi, erste 30-60 Min) heben die Qualität.
5. Echtes Gap-MR lebt auf **Einzelaktien** (Korb) und **wöchentlich** — nicht unser Single-Index-Intraday-Spiel.

## Strategie-Bauplan (für [[Backtest-Engine]], neuer Modus `gap`)
Zwei testbare, dekorrelierte Hypothesen:
- **H1 Small-Gap-Fade:** nur wenn |Gap| klein (~0,1-0,5×ATR), nach 15-Min-Bestätigung Richtung Vortages-Close faden, Ziel = Fill, enger Stop, Cutoff 60 Min, optional Di/Mi + Gap-Down-Bias.
- **H2 Large-Gap-Continuation:** wenn |Gap| groß (>1×ATR), mit dem Gap gehen, Bestätigung durch starke erste Bar (Velocity), intraday halten. Deckt sich mit Mesfins einzigem Positiv-Signal + unserer Momentum-Edge.

## Datenbedarf
- **Reicht schon:** unsere **1-Min RTH-Daten** (Gap = heutiger 09:30-Open vs gestriger 15:59-Close), Daily-ATR für die Größen-Buckets, erste-Bar-Bestätigung, Wochentag. 1-Min ist fein genug (Paper nutzte 5-Min).
- **Wäre besser (optional):** die **Overnight/Globex-Session** (für den „Gap-Down + Overnight-Rally"-Filter mit 83% Fill) — die haben wir aktuell NICHT (nur RTH). Bei Bedarf Extra-Export aus QuantPad (Full-Session-Bars).
- Keine L2/Tick nötig.

## Quellen
[Mesfin MNQ Falsifikation (arXiv)](https://arxiv.org/pdf/2605.04004) · [tradingstats NQ Gap-Fill](https://tradingstats.net/gap-fill-strategy/) · [tradingstats Timing](https://tradingstats.net/when-do-gaps-fill/) · [Overnight-Intraday Reversal Everywhere](https://assets.super.so/e46b77e7-ee08-445e-b43f-4ffd88ae0a0e/files/c953a0e6-e93e-4bf7-b839-45a90cedced4.pdf) · [MDPI Overnight Gaps S&P500](https://www.mdpi.com/1911-8074/12/2/51)
