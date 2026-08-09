---
tags:
  - ressource/paper
  - trading/katalog
erstellt: 2026-07-06
---
# 📋 Strategie-Katalog (Backlog zum Testen)

⬅️ [[_Paper-Registry]] · [[Strategie-Logbuch]]

> [!info] Zweck
> Master-Liste aller Kandidaten-Strategien mit je einem Research-Paper. Reihenfolge zum Durchtesten via [[Backtest-Engine]]. **"Warum/Analyse" kommt später** — hier erstmal nur sammeln. Status: 🟢 offen · ✅ getestet · ⚠️ braucht Daten (Tick/L2/Options) · 🚫 nicht Single-Instrument.

## Reversion
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 1 | Intraday Time Series Reversal (overnight → 1. Halbstunde) | 5807282 | ✅ Reversal NO-GO, **Momentum-Spiegel A-Note** (#008) |
| 2 | Overnight-Intraday Reversal Everywhere | 2730304 | 🟢 |
| 3 | VWAP / Z-Score Mean Reversion (regime-gefiltert) | 6454659 / 6087107 | ✅ NO-GO (#002/#003) |
| 4 | Mean Reversion via True Strength Index (SPY/QQQ) | 4708400 | 🟢 |
| 5 | Intraday Residual Reversal | 4731947 | ⚠️/🚫 (cross-sectional) |
| 6 | Gap Fade / Gap Reversal (große Gaps drehen) | 4834097 | 🟢 |

## Momentum / Trend
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 7 | Intraday Momentum (1. → letzte Halbstunde) | 2552752 / 2440866 | ✅ **A-Note validiert** (#008, sig15-Momentum) |
| 8 | Beat the Market — Intraday Momentum SPY | 4824172 | 🟢 |
| 9 | VWAP Trend "Holy Grail" | 4631351 | ✅ NO-GO (#005) |
| 10 | Noise-Boundary Momentum (VWAP/Ladder Exits) | 5095349 | 🟢 |
| 11 | Opening Range Breakout (ORB) | 4416622 | ✅ NO-GO (#001) |
| 12 | ORB + Fast Retest | 6745958 | ✅ NO-GO (#001) |
| 13 | Cross-Market Intraday TS Momentum | 4651331 | 🟢 |
| 14 | TS Momentum + Reversal (Realized Semivariance) | 3584014 | 🟢 |

## Breakout / Volatilität
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 15 | Gap-and-Go Opening Range Breakout | 5198458 | 🟢 |
| 16 | Opening Gap Surge (Swing+Intraday) | 4834097 | 🟢 |
| 17 | Volatility / Range-Expansion Breakout | (suchen) | 🟢 |
| 18 | VWAP Regime Classification (Filter-Baustein) | 6438039 | 🟢 |

## Seasonality / Time-of-Day
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 19 | Intraday Seasonality (U-Shape, Time-of-Day) | 3021533 | 🟢 |
| 20 | Intra-day Seasonality Crude (Brent) | 5037563 | 🟢 (anderes Instrument) |
| 21 | Power Hour / Last-Hour Momentum | 2552752 | 🟢 |

## Microstructure / Order Flow (braucht Tick/L2)
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 22 | Order Flow Imbalance / Book Pressure | (suchen) | ⚠️ L2 |
| 23 | Options Dealer Hedging / Gamma | (suchen) | ⚠️ Options |
| 24 | Footprint / Delta / CVD | (suchen) | ⚠️ Tick |

## Stock-Selection (nicht Single-Instrument)
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 25 | Stocks in Play (ORB auf High-RVOL) | 4729284 | 🚫 Multi-Stock |
| 26 | Small-Cap Retail Strategien | 5921742 | 🚫 Multi-Stock |

## Regime-conditioned Reversion (Filter zentral)
| # | Strategie | Paper (SSRN) | Status |
|---|---|---|---|
| 27 | Momentum Exhaustion & Fair Value Reversion | 6454659 | 🟢 |
| 28 | Regime-Conditioned Mean Reversion FX | 6087107 | 🟢 (FX) |

## Meta / Realitäts-Check (was NICHT geht)
| # | Thema | Quelle | Status |
|---|---|---|---|
| 29 | Falsifikation OHLCV-Signale MNQ | arXiv 2605.04004 | ⚠️ Pflichtlektüre |
| 30 | Simple Intraday Strategien "funktionieren nicht" | SSRN 2488539 (Donninger) | ⚠️ Pflichtlektüre |
| 31 | RL/GA Optimierung (MaxAI) | 5761402 | 🟢 Methodik |

---
**Nächste zum Testen:** #1 Intraday Time Series Reversal, dann #2, #4, #6, #10.
