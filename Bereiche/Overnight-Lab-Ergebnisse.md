---
tags:
  - bereich/trading
  - trading/overnight
erstellt: 2026-07-06
---
# 🌙 Overnight-Lab Ergebnisse

⬅️ [[Strategie-Logbuch]] · Lauf: 2026-07-06 23:36

> [!info] Fast-Pass-Ranking
> Sortiert nach **robust** (OOS-Edge positiv) + **Speedpass** (P(pass) gewichtet mit Passgeschwindigkeit, volle Punkte bei Pass in ≤90 Tagen).
> Reports mit `NIGHT_...` liegen im Strategy Lab.

| # | Familie | robust | Win | Edge | expR | OOS-expR | Sharpe | Tr/J | P(pass) | ~Tage | Speedpass | Report |
|---|---|:--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|---|
| 1 | Momentum | ✅ | 40% | +6.7% | +0.189 | +0.213 | +1.83 | 76 | 42% | 74 | 0.424 | `NIGHT_Momentum_1` |
| 2 | Momentum | ✅ | 41% | +8.0% | +0.220 | +0.222 | +2.15 | 60 | 45% | 99 | 0.411 | `NIGHT_Momentum_2` |
| 3 | Momentum | ✅ | 49% | +8.4% | +0.169 | +0.191 | +2.23 | 51 | 50% | 120 | 0.378 | `NIGHT_Momentum_3` |
| 4 | Momentum | ✅ | 52% | +10.9% | +0.217 | +0.229 | +2.91 | 34 | 53% | 141 | 0.338 | `NIGHT_Momentum_4` |
| 5 | Overnight | ✅ | 50% | +1.7% | +0.015 | +0.015 | +0.42 | 100 | 32% | 64 | 0.324 | `NIGHT_Overnight_5` |
| 6 | Overnight | ✅ | 50% | +1.6% | +0.010 | +0.010 | +0.39 | 100 | 31% | 64 | 0.313 | `NIGHT_Overnight_6` |
| 7 | Overnight | ✅ | 50% | +1.9% | +0.020 | +0.019 | +0.48 | 148 | 30% | 52 | 0.303 | `NIGHT_Overnight_7` |
| 8 | VWAP-Trend | ✅ | 13% | +0.0% | +0.001 | +0.031 | +0.01 | 133 | 30% | 65 | 0.303 | `NIGHT_VWAP-Trend_8` |
| 9 | Overnight | ✅ | 50% | +1.8% | +0.014 | +0.015 | +0.44 | 148 | 29% | 6 | 0.293 | `NIGHT_Overnight_9` |
| 10 | ORB | ✅ | 36% | +9.3% | +0.361 | +0.229 | +2.46 | 23 | 52% | 263 | 0.178 | `NIGHT_ORB_10` |
| 11 | ORB | ✅ | 27% | +6.7% | +0.352 | +0.455 | +2.03 | 14 | 61% | 445 | 0.124 |  |
| 12 | ORB | ✅ | 28% | +6.7% | +0.328 | +0.139 | +1.90 | 23 | 38% | 287 | 0.119 |  |
| 13 | ORB | ✅ | 21% | +5.0% | +0.335 | +0.401 | +1.65 | 14 | 60% | 472 | 0.115 |  |

## Beste Config je Familie (Parameter)

- **Momentum** (`ts_reversal`): `{'symbol': 'NQ', 'rev_side': 'momentum', 'rev_base': 'open', 'rev_exit': 'eod', 'rev_signal_min': 15, 'rev_thr': 0.003, 'rev_stop_mult': 0.75, 'rev_er_min': 0.0}`
- **Overnight** (`overnight_reversal`): `{'symbol': 'NQ', 'entry_thr': 0.005, 'hold_min': 90, 'target_mult': 2.0, 'stop_mult': 1.5}`
- **VWAP-Trend** (`vwap_trend`): `{'symbol': 'NQ', 'stop_mult': 4.0, 'regime': 'trend'}`
- **ORB** (`orb`): `{'symbol': 'NQ', 'orb_cutoff_min': 120, 'trend_filter': True, 'vwap_filter': True, 'vol_filter': True, 'or_min': 30, 'stop_frac': 0.5, 'vol_mult': 1.7, 'target_mult': None}`