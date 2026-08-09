---
tags:
  - bereich/trading
  - trading/refine
erstellt: 2026-07-07
---
# 🧠 Refine-Lab Ergebnisse

⬅️ [[Strategie-Logbuch]] · Lauf: 2026-07-07 17:22

> [!info] Explorer statt Curve-Fitter
> Viele *strukturell verschiedene* Ideen, dann gezielt verschärft. Eine Verschärfung wird nur behalten, wenn sie **in-sample UND out-of-sample** (2021-2026) hilft. So entsteht die Edge ohne Overfitting.

## 🏆 Diverse Finalisten (mit Report im Lab)

| Report | Familie | Verschärfungs-Pfad | OOS-Edge | OOS-expR | Sharpe | Tr/J | P(pass) | Speedpass |
|---|---|---|--:|--:|--:|--:|--:|--:|
| `REFINE_ORB_1` | ORB | vol1.7 → tgtNone → vwap | +10.6% | +0.605 | +2.59 | 19 | 72% | 0.190 |
| `REFINE_ORB_2` | ORB | tgtNone → nr7 → vol1.3 → cutoff60 | +13.3% | +0.586 | +3.48 | 14 | 77% | 0.207 |
| `REFINE_ORB-fade_3` | ORB-fade | tgtNone → nr7 → stop0.4 | +6.3% | +0.373 | +0.34 | 40 | 49% | 0.364 |
| `REFINE_Momentum_4` | Momentum | er0.4 → stop0.75 | +13.6% | +0.260 | +2.04 | 26 | 56% | 0.215 |
| `REFINE_Momentum_5` | Momentum | stop0.75 → thr0.003 | +7.4% | +0.213 | +1.83 | 76 | 42% | 0.424 |
| `REFINE_VWAP-Trend_6` | VWAP-Trend | regime_trend → stop4 | +1.9% | +0.031 | +0.01 | 133 | 30% | 0.303 |

## Beste Config je Finalist (Parameter)

- **REFINE_ORB_1** (`orb` NQ): `or_min=15, orb_side=breakout, stop_frac=0.5, target_mult=None, vol_filter=True, vol_mult=1.7, vwap_filter=True`
- **REFINE_ORB_2** (`orb` NQ): `or_min=30, orb_side=breakout, stop_frac=0.5, target_mult=None, nr7_filter=True, vol_filter=True, vol_mult=1.3, orb_cutoff_min=60`
- **REFINE_ORB-fade_3** (`orb` NQ): `or_min=15, orb_side=fade, stop_frac=0.4, target_mult=None, nr7_filter=True`
- **REFINE_Momentum_4** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=30, rev_exit=eod, rev_er_min=0.4, rev_stop_mult=0.75`
- **REFINE_Momentum_5** (`ts_reversal` NQ): `rev_side=momentum, rev_base=open, rev_signal_min=15, rev_exit=eod, rev_stop_mult=0.75, rev_thr=0.003`
- **REFINE_VWAP-Trend_6** (`vwap_trend` NQ): `stop_mult=4.0, regime=trend`

## Alle robusten Überlebenden (auch ohne Report)

| Familie | Pfad | OOS-expR | robust |
|---|---|--:|:--:|
| ORB | vol1.7 → tgtNone → vwap | +0.605 | ✅ |
| ORB | tgtNone → nr7 → vol1.3 → cutoff60 | +0.586 | ✅ |
| ORB-fade | tgtNone → nr7 → stop0.4 | +0.373 | ✅ |
| Momentum | er0.4 → stop0.75 | +0.260 | ✅ |
| ORB | tgtNone → nr7 → vol1.5 | +0.252 | ✅ |
| Momentum | stop0.75 → thr0.003 | +0.213 | ✅ |
| VWAP-Trend | regime_trend → stop4 | +0.031 | ✅ |
| ORB | tgtNone → vol1.7 → vwap | +0.432 | ⚠️ |
| Fade | er0.4 | +0.035 | ⚠️ |
| Overnight | roh | +0.007 | ⚠️ |
| VWAP-Cont | regime_trend → tgt2 | -0.042 | ⚠️ |
| ORB-fade | tgtNone → stop0.6 → trend | -0.089 | ⚠️ |
| VWAP-Rev | roh | -0.104 | ⚠️ |