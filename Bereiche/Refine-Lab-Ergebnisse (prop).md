---
tags:
  - bereich/trading
  - trading/refine
erstellt: 2026-07-07
---
# 🧠 Refine-Lab Ergebnisse

⬅️ [[Strategie-Logbuch]] · Lauf: 2026-07-07 17:56

> [!info] Explorer statt Curve-Fitter
> Viele *strukturell verschiedene* Ideen, dann gezielt verschärft. Eine Verschärfung wird nur behalten, wenn sie **in-sample UND out-of-sample** (2021-2026) hilft. So entsteht die Edge ohne Overfitting.

## 🏆 Diverse Finalisten (mit Report im Lab)

| Report | Familie | Verschärfungs-Pfad | OOS-Edge | OOS-expR | Sharpe | Tr/J | P(pass) | Speedpass |
|---|---|---|--:|--:|--:|--:|--:|--:|
| `REFINEPROP_ORB_1` | ORB | vol1.3 → tgtNone → stop0.4 → cutoff90 | +5.3% | +0.326 | +1.20 | 59 | 56% | 0.447 |
| `REFINEPROP_ORB_2` | ORB | vol1.5 → tgtNone → cutoff60 → stop0.6 | +6.9% | +0.228 | +1.62 | 62 | 45% | 0.452 |
| `REFINEPROP_Momentum_3` | Momentum | stop0.75 → er0.3 | +6.7% | +0.187 | +1.65 | 83 | 43% | 0.430 |
| `REFINEPROP_Momentum_4` | Momentum | sig15 → stop0.75 → er0.3 | +6.7% | +0.187 | +1.65 | 83 | 43% | 0.430 |

## Beste Config je Finalist (Parameter)

- **REFINEPROP_ORB_1** (`orb` NQ): `or_min=15, orb_side=breakout, stop_frac=0.4, target_mult=None, vol_filter=True, vol_mult=1.3, orb_cutoff_min=90`
- **REFINEPROP_ORB_2** (`orb` NQ): `or_min=30, orb_side=breakout, stop_frac=0.6, target_mult=None, vol_filter=True, vol_mult=1.5, orb_cutoff_min=60`
- **REFINEPROP_Momentum_3** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=15, rev_exit=eod, rev_stop_mult=0.75, rev_er_min=0.3`
- **REFINEPROP_Momentum_4** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=15, rev_exit=eod, rev_stop_mult=0.75, rev_er_min=0.3`

## Alle robusten Überlebenden (auch ohne Report)

| Familie | Pfad | OOS-expR | robust |
|---|---|--:|:--:|
| ORB | vol1.3 → tgtNone → stop0.4 → cutoff90 | +0.326 | ✅ |
| ORB | vol1.5 → tgtNone → cutoff60 → stop0.6 | +0.228 | ✅ |
| Momentum | stop0.75 → er0.3 | +0.187 | ✅ |
| Momentum | sig15 → stop0.75 → er0.3 | +0.187 | ✅ |
| Overnight | roh | +0.007 | ⚠️ |
| VWAP-Trend | roh | -0.004 | ⚠️ |
| Fade | roh | -0.088 | ⚠️ |
| ORB-fade | roh | -0.043 | ⚠️ |
| ORB | roh | -0.088 | ⚠️ |
| VWAP-Cont | roh | -0.097 | ⚠️ |
| ORB-fade | roh | -0.182 | ⚠️ |
| VWAP-Rev | roh | -0.104 | ⚠️ |