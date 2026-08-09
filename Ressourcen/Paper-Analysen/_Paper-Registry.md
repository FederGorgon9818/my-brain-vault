---
tags:
  - ressource/paper
  - system/index
erstellt: 2026-07-06
---
# 🗂️ Paper-Registry (Such-Index)

⬅️ [[_Ressourcen]]

> [!info] Zweck
> Zentrale Registry: **unter welcher Bedingung / mit welchem Ziel** wurden welche SSRN-Paper gesucht, was kam raus, und warum. Damit nichts doppelt gesucht wird und Max jederzeit die Herkunft nachvollziehen kann. Bei neuem Suchlauf: hier zuerst schauen, dann gezielt ergänzen.

---

## Suchbedingung A — Opening Range Breakout (ORB), intraday, Prop
**Ziel:** ORB-Strategie für Prop-Intraday. **Ergebnis:** getestet, NO-GO (Fill-Bug). Details [[ORB Fast-Retest Review]], Logbuch #001.
| SSRN | Titel | Rolle |
|---|---|---|
| 4416622 | Zarattini/Aziz — Can Day Trading Be Profitable (ORB QQQ) | Fundament ORB |
| 6745958 | Pineda — Anatomy of the Retest (QQQ ORB) | Retest-Entry |
| 4729284 | Zarattini/Barbon/Aziz — Profitable Day Trading (Stocks in Play) | ORB 7000+ Aktien |
| 4824172 | Zarattini — Beat the Market (SPY Intraday Momentum) | verwandt |
Datei: [[ORB Paper (Zarattini, Aziz, Pineda)]]

## Suchbedingung B — High-Winrate Mean Reversion (RR≤1, viele Trades, Prop)
**Ziel:** hohe Win-Rate, hohe Frequenz, RR<1. **Ergebnis:** VWAP-Reversion getestet, NO-GO (Continuation statt Reversion). Logbuch #002/#003.
| SSRN | Titel | Rolle |
|---|---|---|
| 5807282 | Intraday Time Series Reversal (Index) | bester Single-Index-Fit, noch offen |
| 2730304 | Overnight-Intraday Reversal Everywhere (Guofu Zhou) | seriös, noch offen |
| 6454659 | Bhatti — Momentum Exhaustion & Fair Value Reversion | Regime-Reversion |
| 6087107 | Bhatti — Regime-Conditioned Mean Reversion FX | Regime-Framework + MQL5 |
| 6438039 | Lee — VWAP Regime Classification | Regime-Filter-Baustein |
| 4878676 | Vu & Bhattacharyya — Mean Reversion QuantConnect | Stop-Loss-Impact |
| 4708400 | Requejo — Mean Reversion via TSI (SPY/QQQ) | ❌ getestet 29.07., NO-GO → [[TSI Mean Reversion (Requejo 4708400)]] |
Dateien: [[Mean-Reversion Paper (High-Winrate Fokus)]]

## Suchbedingung C — Intraday Momentum / Continuation
**Ziel:** ehrliches Gegenteil der Reversion (Continuation an Stretches). **Ergebnis:** Momentum real (+1,6% Edge über Baseline an Trendtagen) aber < Kosten. Logbuch #004.
| SSRN | Titel | Rolle |
|---|---|---|
| 2552752 | Gao/Han/Li/Zhou — Intraday Momentum (1st→last half hour) | kanonisch, belegt Trend-Filter |
| 2440866 | Gao/Han/Li/Zhou — Market Intraday Momentum | kanonisch |
| 4824172 | Zarattini — Beat the Market (SPY Momentum) | praktisch, aber RR>1/niedrige Win |
| 4631351 | Zarattini — VWAP Holy Grail | VWAP-Trend, getestet #005 |
| 5095349 | Maróy — Improvements to Intraday Momentum | Noise-Boundary + Exits |
Datei: [[Intraday Momentum Paper]]

## Suchbedingung D — Prop-Eval-Passing (niedriger DD, schnell passen, ≥70%)
**Ziel:** Evals mit höchster Wahrscheinlichkeit in kürzester Zeit bestehen. **Ergebnis:** Fokus + Eval-Optimizer gebaut. Datei [[Prop-Eval-Passing (Fokus)]].
| SSRN | Titel | Rolle |
|---|---|---|
| 6672818 | Leo Ng — Pass-First-Pay-Later (Deferred-Fee) | Eval-Ökonomie (Kosten↓) |
| 4631351 | Zarattini — VWAP Holy Grail | niedriger-DD-Kandidat → getestet #005, NO-GO auf NQ |
| 5761402 | Huber — MaxAI (RL/GA Index-Futures) | zu wackelig |
| 6722841 | Wong — MC Evaluation of Strategy | MC-Methodik |

---

## Noch nicht getestet (offene Kandidaten)
- 5807282 Intraday Time Series Reversal (Index)
- 2730304 Overnight-Intraday Reversal
- 5095349 Maróy Noise-Boundary Momentum (mit VWAP/Ladder-Exits)
