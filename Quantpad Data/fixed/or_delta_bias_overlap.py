"""
Overlap-Check FINAL: OR_DELTA_BIAS_NQ (smul=0.75, tmul=None, win=30, LONG delta>0)
gegen NQ_Momentum (Book-Leg). Analog ivb_overlap_check.py, aber mit dem finalen
Kandidaten-Setup statt dem alten IVB-Breakout-Skelett.
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
FLAT_MIN = 385
COST_PTS_RT = 0.87
MOM_THR = 0.003

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())

sig, mom = {}, {}
for d, g in df.groupby("day", sort=True):
    tm = g["tmin"].to_numpy()
    o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))

    m15 = tm < 15
    if m15.sum() >= 10:
        o0 = o[m15][0]
        c15 = c[m15][-1]
        r15 = (c15 - o0) / o0
        if abs(r15) >= MOM_THR:
            dirn = 1 if r15 > 0 else -1
            entry_idx = np.where(tm >= 15)[0]
            if entry_idx.size:
                e = o[entry_idx[0]]
                mom[d] = {"dir": dirn, "pnl_pts": (c[-1] - e) * dirn}

    wm = tm < 30
    if wm.sum() < 10:
        continue
    wh, wl = h[wm].max(), lw[wm].min()
    ww = wh - wl
    if ww <= 0:
        continue
    w_idx = np.where(wm)[0]
    delta = np.sum(np.sign(c[w_idx] - o[w_idx]) * v[w_idx])
    if delta <= 0:
        continue
    after = np.where(tm >= 30)[0]
    if after.size == 0:
        continue
    ei = after[0]
    entry = o[ei]
    R = 0.75 * ww
    stop = entry - R
    exit_price, exit_kind = c[-1], "eod"
    for j in range(ei, len(tm)):
        if tm[j] >= FLAT_MIN:
            exit_price, exit_kind = o[j], "time"
            break
        if lw[j] <= stop:
            exit_price, exit_kind = stop, "stop"
            break
    r_net = (exit_price - entry) / R - COST_PTS_RT / R
    sig[d] = {"r_net": r_net}

sig_days = set(sig)
mom_days = set(mom)
mom_long_days = {d for d in mom if mom[d]["dir"] == 1}

print("OR_DELTA_BIAS_NQ-Tage: %d | NQ_Momentum-Tage: %d (davon long: %d)" %
      (len(sig_days), len(mom_days), len(mom_long_days)))
inter_any = sig_days & mom_days
inter_long = sig_days & mom_long_days
print("Ueberlappung Signal n Momentum (beliebige Richtung): %d = %.0f%% der Signal-Tage" %
      (len(inter_any), 100 * len(inter_any) / len(sig_days)))
print("Ueberlappung Signal n Momentum-LONG: %d = %.0f%% der Signal-Tage" %
      (len(inter_long), 100 * len(inter_long) / len(sig_days)))

all_days = sorted(sig_days | mom_days)
a = pd.Series({d: sig[d]["r_net"] if d in sig else 0.0 for d in all_days})
b_ = pd.Series({d: np.sign(mom[d]["pnl_pts"]) * min(abs(mom[d]["pnl_pts"]), 1e9) if d in mom else 0.0
                for d in all_days})
print("Tages-PnL-Korrelation (Union, inaktiv=0): %+.2f" % a.corr(b_))
both = sorted(inter_any)
if len(both) > 20:
    a2 = pd.Series({d: sig[d]["r_net"] for d in both})
    b2 = pd.Series({d: mom[d]["pnl_pts"] for d in both})
    print("Tages-PnL-Korrelation (nur gemeinsame Tage, n=%d): %+.2f" % (len(both), a2.corr(b2)))

w = pd.Series({d: sig[d]["r_net"] for d in inter_long})
wo = pd.Series({d: sig[d]["r_net"] for d in sig_days - mom_days})
print("\nSignal-Trades AUF Momentum-Long-Tagen:  n=%4d  avgR=%+.3f  win=%.1f%%  sumR=%+.1f" %
      (len(w), w.mean(), 100 * (w > 0).mean(), w.sum()))
print("Signal-Trades OHNE Momentum-Signal:     n=%4d  avgR=%+.3f  win=%.1f%%  sumR=%+.1f" %
      (len(wo), wo.mean(), 100 * (wo > 0).mean(), wo.sum()))
print("\nFERTIG.")
