---
tags:
  - bereich/trading
  - trading/refine
erstellt: 2026-07-07
---
# 🧠 Refine-Lab Ergebnisse

⬅️ [[Strategie-Logbuch]] · Lauf: 2026-07-07 18:31

> [!info] Explorer statt Curve-Fitter
> Viele *strukturell verschiedene* Ideen, dann gezielt verschärft. Eine Verschärfung wird nur behalten, wenn sie **in-sample UND out-of-sample** (2021-2026) hilft. So entsteht die Edge ohne Overfitting.

## 🏆 Diverse Finalisten (mit Report im Lab)

| Report | Familie | Verschärfungs-Pfad | OOS-Edge | OOS-expR | Sharpe | Tr/J | P(pass) | Speedpass |
|---|---|---|--:|--:|--:|--:|--:|--:|
| `REFINEAPEX_ORB_1` | ORB | tgtNone → trend | +3.5% | +0.159 | +0.81 | 130 | 37% | 0.372 |
| `REFINEAPEX_ORB_2` | ORB | tgtNone → stop0.6 → cutoff60 | +5.3% | +0.156 | +0.86 | 214 | 36% | 0.360 |
| `REFINEAPEX_Momentum_3` | Momentum | stop0.75 | +5.1% | +0.116 | +1.12 | 146 | 36% | 0.356 |
| `REFINEAPEX_Momentum_4` | Momentum | roh | +6.3% | +0.148 | +1.15 | 122 | 39% | 0.393 |
| `REFINEAPEX_Overnight_5` | Overnight | tgt2 → hold90 | +2.7% | +0.037 | +0.63 | 217 | 31% | 0.310 |
| `REFINEAPEX_PowerHour_6` | PowerHour | ref300 | +1.9% | +0.008 | +0.19 | 166 | 28% | 0.283 |
| `REFINEAPEX_PowerHour_7` | PowerHour | roh | +1.9% | +0.008 | +0.19 | 166 | 28% | 0.283 |

## Beste Config je Finalist (Parameter)

- **REFINEAPEX_ORB_1** (`orb` NQ): `or_min=15, orb_side=breakout, stop_frac=0.5, target_mult=None, trend_filter=True`
- **REFINEAPEX_ORB_2** (`orb` NQ): `or_min=30, orb_side=breakout, stop_frac=0.6, target_mult=None, orb_cutoff_min=60`
- **REFINEAPEX_Momentum_3** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=30, rev_exit=eod, rev_stop_mult=0.75`
- **REFINEAPEX_Momentum_4** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=15, rev_exit=eod`
- **REFINEAPEX_Overnight_5** (`overnight_reversal` NQ): `on_side=fade, target_mult=2.0, hold_min=90`
- **REFINEAPEX_PowerHour_6** (`last_hour` NQ): `lh_ref_min=300, lh_thr=0.003`
- **REFINEAPEX_PowerHour_7** (`last_hour` NQ): `lh_ref_min=300, lh_thr=0.003`

## Alle robusten Überlebenden (auch ohne Report)

| Familie | Pfad | OOS-expR | robust |
|---|---|--:|:--:|
| ORB | tgtNone → trend | +0.159 | ✅ |
| ORB | tgtNone → stop0.6 → cutoff60 | +0.156 | ✅ |
| Momentum | stop0.75 | +0.116 | ✅ |
| Momentum | roh | +0.148 | ✅ |
| Overnight | tgt2 → hold90 | +0.037 | ✅ |
| PowerHour | ref300 | +0.008 | ✅ |
| PowerHour | roh | +0.008 | ✅ |
| Momentum | sig30 | +0.029 | ✅ |
| VWAP-Trend | roh | -0.004 | ⚠️ |
| Fade | roh | -0.088 | ⚠️ |
| Gap-Mom | roh | -0.017 | ⚠️ |
| ORB-fade | roh | -0.043 | ⚠️ |
| PowerHour | roh | -0.004 | ⚠️ |
| Gap-Mom | roh | -0.058 | ⚠️ |
| VWAP-Cont | roh | -0.097 | ⚠️ |
| VWAP-Rev | roh | -0.104 | ⚠️ |
| ORB | roh | -0.119 | ⚠️ |
| ORB | roh | -0.032 | ⚠️ |
| ORB-fade | roh | -0.182 | ⚠️ |
| ORB | roh | -0.144 | ⚠️ |