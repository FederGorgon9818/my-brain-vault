---
tags:
  - bereich/trading
  - trading/phase-eval
erstellt: 2026-07-07
---
# 🎯 Phase 1 – Eval-Passing (AKTUELLER FOKUS)

⬅️ [[Day Trading]] · ➡️ [[Funded-Phase]]

> [!important] Einziges Ziel dieser Phase
> **Die Prop-Eval bestehen.** Nichts anderes zählt hier. Optimiert wird ausschließlich auf: **hohe Passchance in kürzester Zeit.** Payouts, Profit-Split, Funded-Management = spätere Phase ([[Funded-Phase]]), spielen für die Strategie-Wahl HIER keine Rolle.
>
> **Ziel-Firma: algo-freundlich + EOD-Drawdown** (Tradeify oder MyFundedFutures). **NICHT Apex** (kein Voll-Algo + intraday trailing = härtestes Modell).

## 📌 Ehrlicher Stand (07.07.2026)
Von allen Seiten geprüft (3 Objektiv-Läufe + Portfolio + Sizing): **70% in 3 Wochen ist mit den aktuellen Edges nicht erreichbar.** ABER der Firmen-Pivot half stark. Multi-Markt-Buch (5 robuste Zellen, 3 Instrumente):

| Tempo | Apex (intraday) | **EOD-Firma (Tradeify/MFFU)** |
|---|---|---|
| ~3-4 Wochen | 33% | **~49%** |
| ~2 Monate | 40% | **~54%** |
| Decke (langsam) | 68% | **72%** |

→ **Realistischer Plan:** EOD-Firma + schnelles Buch (~49% in ~4 Wochen) + Cheap-Resets = in ~2 Monaten funded, günstig. Parallel weiter **stärkeres Alpha** ([[Alpha-Suche]]).

## 🧰 Werkzeuge
- [[Backtest-Engine]] – lokale ehrliche Engine (real fills, OOS, Prop-MC)
- [[Portfolio-Simulator]] – mehrere Beine auf 1 Apex (Korrelation + kombinierte P(pass))
- [[Strategie-Logbuch]] – jede getestete Strategie + Verdict

## 📊 Detailergebnisse (Historie)
- [[Wochenreport 2026-W31 (27.07-31.07)]] – aktuellster Stand: 9 Beine, NetLiq +2,8%, Live-Monitor-Bugfixes
- [[Portfolio-Simulator]] – Kombinationen, Empfehlung `PORTFOLIO_balance`
- [[Refine-Lab-Ergebnisse (apex)]] – 20 Strategien auf Apex-Speed optimiert
- [[Refine-Lab-Ergebnisse (prop)]] · [[Refine-Lab-Ergebnisse]] – Explorer-Läufe
- [[Overnight-Lab-Ergebnisse]] – erster breiter Sweep

## ✅ Aktueller Kandidat für den echten Versuch (Update 21.07.2026)
`PORTFOLIO_optimized` (5 Beine: NQ Momentum + NQ Power-Hour + NQ ORB-Breakout + NQ ORB-Fade + RTY Gap-Fade):
- **EOD-Trailing-Firma: 54-58% in ~43-70 Tagen** (frac 0.22-0.18)
- **Static-DD-Firma (falls verfügbar): 63% in ~45 Tagen** — Firmenwahl = größter Hebel, siehe [[Portfolio-Simulator]]
- |Korr| 0,08 · RoDD 9,2 · 402 Trades/Jahr · Report im Strategy Lab (Portfolio-Tab)

## 🚀 Umsetzung live
→ **[[Live-Setup (Algo auf Prop)]]** — komplette Anleitung: Firmenwahl (MFFU/Tradeify, Algo-Regeln geprüft), Setup-Vergleich (Empfehlung: NinjaTrader 8 + NinjaScript auf Tradovate-Konto), 4-Phasen-Plan (Konto → C#-Port → Sim-Validierung → Eval).
