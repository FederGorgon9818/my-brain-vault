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
