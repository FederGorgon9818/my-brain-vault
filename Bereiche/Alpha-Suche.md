---
tags:
  - bereich/trading
  - trading/alpha
erstellt: 2026-07-07
---
# 🔎 Alpha-Suche (für Eval-Passing)

⬅️ [[Eval-Passing]]

> [!important] Kern-Reframe
> **Eine Eval zu passen ist NICHT dasselbe wie eine gute Trading-Strategie.** Es ist ein **First-Passage-Problem** (Gambler's Ruin): erreiche +3.000$ bevor du -2.500$ Trailing-DD reißt, schnell. Varianz ist hier nicht der Feind, nur der Ruin ist es. Deshalb ist öffentliches Quant-Alpha (auf Echtgeld/Sharpe/Langfrist optimiert) für uns das **falsche Objektiv**.

## Die zwei Hebel (in Reihenfolge des Impacts)

### 1. Bet-Sizing / Staking — ✅ GETESTET (07.07.2026)
Ergebnis: **hebt die Passquote NICHT** (Gambler's Ruin: kleine Einsätze = höchste Passquote, aber langsam). Sizing ist ein **besserer Speed↔Pass-Regler**, kein Ceiling-Lifter. Bester Regler `cushion_frac ~0,10` (Portfolio: 62% in ~111 statt 66% in ~222 Tagen). Die **Decke ~65-66% ist durch die Edge gesetzt.** Details: [[Strategie-Logbuch]] #011. → Deshalb ist der eigentliche Hebel Nummer 2.

### 2. Neues Signal-Alpha (was wir noch nicht angezapft haben)
Priorisiert nach Machbarkeit:
- **Cross-Asset / Intermarket** (VIX, Bonds/ZN, DXY, Sektor-Breadth sagen Index-Intraday voraus). Daten verfügbar, noch nie getestet. → **bester nächster Schritt.**
- **Event-/Zeitstruktur:** Opening-Auction-Imbalance, FOMC/CPI-Tage, Month-End, OpEx/Gamma. Strukturell, dokumentiert, buildbar.
- **Volatilitäts-Regime-Conditioning** der bestehenden Edges (nur an den richtigen Tagen handeln).
- **Order Flow / Microstructure** (L2, Footprint, CVD, Absorption): DA sitzt die echte Ex-Institutional-Edge. Braucht aber **Tick/L2-Daten**, die wir bewusst weggelassen haben. → nur wenn wir ernst machen und Daten holen.

## Zu Social-Media / Ex-Institutional-Tradern (Max' Frage)
- Ihre Strategien sind auf **Echtgeld** optimiert (langer Horizont, Overnight, Kapazität) → falsches Ziel für Eval-Sprint. Deine Prop-Situation ist für die eigentlich ideal, aber ihre Rezepte passen nicht 1:1.
- **Wert liegt in den Prinzipien, nicht den Rezepten:** Liquidität/Order-Flow lesen, wann Momentum vs Mean-Reversion dominiert, Session-Struktur, Auktions-Logik. Das übernehmen, nicht die exakte Strategie.
- **Skepsis:** die meisten öffentlichen "Strategien" sind schlecht (oder gar nicht) ehrlich backgetestet (Fill-Bug-Lektion). **Unser Moat = ehrliches Backtesting.** Alles was wir abschauen, läuft durch die [[Backtest-Engine]].

## Konkreter Plan
1. **Sizing-Optimierung** auf bestehende Edges (First-Passage-Sizing) → schneller, günstiger Gewinn.
2. **Cross-Asset-Signale** bauen (Intermarket-Features) → das aussichtsreichste neue Alpha mit vorhandenen Daten.
3. **Event/Time-Struktur** als Filter/Signal.
4. Order-Flow nur wenn wir Tick/L2-Daten beschaffen.

*Alles gegen das Eval-Objektiv (P(pass) schnell), nicht gegen Sharpe.*

## Offene Fäden (Max, 21.08.2026)

### Volumen als eigenständiges Signal (horizontal + vertikal, einseitig)
- **Idee (Max):** Volumen nicht nur als Filter (RVOL, `vol_filter`), sondern als **einseitiges Signal** für einzelne Strategien denken — in zwei Achsen: **vertikal** (Volumen pro Zeit: wann kommt Beteiligung, wann fehlt sie) und **horizontal** (Volumen pro Preis: Volume Profile, POC/Value Area, wo wurde Position aufgebaut).
- **Was schon gilt:** Minuten-Delta/CVD ist tot ([[Strategie-Logbuch]] #021, [[Alpha-Konzepte]] Punkt 6) — das war Richtungs-Orderflow mit Look-ahead. Roh-Volumen (unsigniert) pro Zeit und pro Preis ist davon **nicht** abgedeckt und wurde bisher nur als ORB-Filter genutzt.
- **Vorarbeit vor jedem Test:** zuerst das Why — wie bringen Institutionen große Positionen in den Future-Markt und welche Volumen-Spur hinterlässt das. Recherche-Ergebnis: [[Institutionelle Order-Execution (Theorie)]]. Erst wenn der Mechanismus steht, Hypothesen im Idee-Engine-Format ([[Idee-Generierung (wie Institutionen)]] Abschnitt 6) formulieren, dann Discovery-Jobs.
- **Stand 21.08.2026:** 478 Hypothesen in 8 Blöcken abgelegt in [[Hypothesen-Bank (Volumen & Flows)]] (192 davon ohne neuen Code als Discovery-Job formulierbar). Nächster Schritt: Kontroll-/Nullhypothesen zuerst, dann Jobs in die Queue.
- **Stand 23.08.2026 (Pairs):** 100 Hypothesen zu Pairs Trading / Relative Value in [[Hypothesen-Bank (Pairs Trading & Relative Value)]] — alle kaefigtauglich gefiltert (intraday only, nur ES/NQ/RTY/YM, doppelte Kosten), 40 davon Ein-Bein. Einstieg laut Rangfolge: SM-01 (Messung), LL-01 (leadlag sauber nachtesten), KO-02/03 (Limit-Entry).
- **Stand 23.08.2026:** 200 Hypothesen zu Time-Series-Momentum und Averages in [[Hypothesen-Bank (Momentum & Averages)]], dazu 100 Hypothesen zu TWAP in [[Hypothesen-Bank (TWAP)]] (Preis um die TWAP-Linie plus Algo-Fingerabdruck). Beide noch ungetestet. Reihenfolge laut Max: erst der Momentum-Schub in die Queue, danach TWAP.

### Momentum in allen Richtungen (TSM, Cross-Section, Way of Dumb)
- **Idee (Max, 21.08.):** Momentum nicht nur als Breakout über den Ort, sondern in allen Richtungen des Futures-Markts denken: Time-Series-Momentum (Preis, Vola, Volumen/Hedging-Demand, Carry, Cross-Asset, Acceleration, Residual, Overnight-vs-Intraday), Cross-Sectional Momentum (Rank über Instrumente) und „Way of Dumb" (Zwangsflows großer Institutionen ausnutzen).
- **Stand:** Teil 1 (TSM-Theorie) recherchiert und verdichtet in [[Momentum-Theorie (Futures)]] mit 7 ungetesteten Hypothesen-Kandidaten (Vol-Targeting-Overlay, Acceleration, idiosynkratisches NQ-Momentum, Tug-of-War-Filter, Multi-Speed-Konsens, Bond-Gate, Basis-Momentum). Teil 2 und 3 als Backlog-Karten in der Idee-Engine (`ideas.json`).
- **Nächster Schritt:** Kandidaten 1 bis 5 als Discovery-Jobs formulieren (Why vorab, Register prüfen), Quant-Team vor dem Vol-Targeting-Overlay.
