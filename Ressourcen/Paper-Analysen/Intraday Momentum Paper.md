---
tags:
  - ressource/paper
  - trading/momentum
erstellt: 2026-07-06
---
# 📄 Intraday Momentum / Continuation Paper (SSRN)

Belegen den Fund aus [[Backtest-Engine]]: Continuation an Stretches ist real, **stärker an Trend-/Volatilitäts-/News-Tagen** (genau was unser Regime-Filter zeigt).

## Kern-Belege
- **Gao, Han, Li, Zhou — "Market Intraday Momentum"** (SSRN 2440866) & **"Intraday Momentum: First Half-Hour Predicts Last Half-Hour"** (SSRN 2552752): erste Halbstunde sagt letzte Halbstunde voraus. **Prädiktabilität stärker an volatileren Tagen, High-Volume-Tagen, Rezessions- und Makro-News-Tagen.** Kanonisch, seriös (Guofu Zhou). → https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2552752
- **Zarattini, Aziz, Barbon — "Beat the Market: Intraday Momentum SPY"** (SSRN 4824172): praktische Umsetzung, Sharpe 1,33. *(Achtung: niedrige Win-Rate ~40%, konvex — RR>1, nicht dein Wunschprofil.)*
- **Zarattini & Aziz — "VWAP: The Holy Grail for Day Trading"** (SSRN 4631351): long über VWAP, short darunter.
- **Maróy — "Improvements to Intraday Momentum Strategies"** (SSRN 5095349): Noise-Boundary-Momentum mit VWAP/Ladder-Exits. *(Sharpe >3 = optimistisch, kritisch prüfen.)*

## Was das für dich heißt
- Momentum/Continuation ist der real belegte Effekt (nicht Reversion, siehe [[ORB Fast-Retest Review]] & Logbuch).
- **ABER:** Momentum hat naturgemäß **niedrige Win-Rate + RR>1** — das Gegenteil deines High-Winrate-Profils. Spannungsfeld ehrlich anerkennen.
- Unser Test bestätigt: +1,6% Edge über Baseline an Trendtagen (RR2), aber < Transaktionskosten bei hoher Frequenz. Fix = weniger, größere Trades.
