"""
Overlap check: is the IVB-Long candidate (long breakout + or_delta>0 +
d_ratio>=0.30) just a duplicate of the existing NQ_Momentum book leg?

NQ_Momentum (Portfolio-Simulator config): first 15 min from RTH open,
|ret| >= 0.3% -> continuation to EOD in that direction (stop ignored here --
approximation, we only need signal days + direction + rough daily PnL sign
for overlap/correlation, not exact leg PnL).
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
OR_MIN, FLAT_MIN = 30, 330
COST_PTS_RT = 0.87
MOM_THR = 0.003

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())

ivb, mom = {}, {}
for d, g in df.groupby("day", sort=True):
    tm = g["tmin"].to_numpy()
    o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))

    # --- NQ_Momentum signal: first 15 min displacement ---
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

    # --- IVB-Long candidate ---
    orm = tm < OR_MIN
    if orm.sum() < 15:
        continue
    orh, orl = h[orm].max(), lw[orm].min()
    orw = orh - orl
    if orw <= 0:
        continue
    or_idx = np.where(orm)[0]
    or_delta = np.sum(np.sign(c[or_idx] - o[or_idx]) * v[or_idx])
    if or_delta <= 0:
        continue
    sig = None
    for b in range(OR_MIN, FLAT_MIN, 5):
        m = (tm >= b) & (tm < b + 5)
        if not m.any():
            continue
        idx = np.where(m)[0]
        c5 = c[idx[-1]]
        if c5 > orh:
            sig = (b, idx, c5)
            break
        if c5 < orl:
            break  # first breakout is short -> no long trade
    if sig is None:
        continue
    b, sidx, c5 = sig
    sig_delta = np.sum(np.sign(c[sidx] - o[sidx]) * v[sidx])
    if sig_delta / max(v[sidx].sum(), 1) < 0.30:
        continue
    after = np.where(tm >= b + 5)[0]
    if after.size == 0:
        continue
    ei = after[0]
    entry = o[ei]
    stop = orl
    R = entry - stop
    if R <= 0:
        continue
    target = entry + R
    exit_price = c[-1]
    for j in range(ei, len(tm)):
        if tm[j] >= FLAT_MIN:
            exit_price = o[j]
            break
        if lw[j] <= stop:
            exit_price = stop
            break
        if h[j] >= target:
            exit_price = target
            break
    ivb[d] = {"r_net": (exit_price - entry) / R - COST_PTS_RT / R}

ivb_days = set(ivb)
mom_days = set(mom)
mom_long_days = {d for d in mom if mom[d]["dir"] == 1}

print(f"IVB-Long-Tage: {len(ivb_days)} | NQ_Momentum-Tage: {len(mom_days)} "
      f"(davon long: {len(mom_long_days)})")
inter_any = ivb_days & mom_days
inter_long = ivb_days & mom_long_days
print(f"Überlappung IVB ∩ Momentum (beliebige Richtung): {len(inter_any)} "
      f"= {100*len(inter_any)/len(ivb_days):.0f}% der IVB-Tage")
print(f"Überlappung IVB ∩ Momentum-LONG: {len(inter_long)} "
      f"= {100*len(inter_long)/len(ivb_days):.0f}% der IVB-Tage")

# daily PnL correlation on the union of active days (0 when inactive)
all_days = sorted(ivb_days | mom_days)
a = pd.Series({d: ivb[d]["r_net"] if d in ivb else 0.0 for d in all_days})
b_ = pd.Series({d: np.sign(mom[d]["pnl_pts"]) * min(abs(mom[d]["pnl_pts"]), 1e9) if d in mom else 0.0
                for d in all_days})
print(f"Tages-PnL-Korrelation (Union, inaktiv=0): {a.corr(b_):+.2f}")
both = sorted(inter_any)
if len(both) > 20:
    a2 = pd.Series({d: ivb[d]["r_net"] for d in both})
    b2 = pd.Series({d: mom[d]["pnl_pts"] for d in both})
    print(f"Tages-PnL-Korrelation (nur gemeinsame Tage, n={len(both)}): {a2.corr(b2):+.2f}")

# IVB performance split: with vs without concurrent momentum signal
w = pd.Series({d: ivb[d]["r_net"] for d in inter_long})
wo = pd.Series({d: ivb[d]["r_net"] for d in ivb_days - mom_days})
print(f"\nIVB-Trades AUF Momentum-Long-Tagen:  n={len(w):4d}  avgR={w.mean():+.3f}  "
      f"win={100*(w>0).mean():.1f}%  sumR={w.sum():+.1f}")
print(f"IVB-Trades OHNE Momentum-Signal:     n={len(wo):4d}  avgR={wo.mean():+.3f}  "
      f"win={100*(wo>0).mean():.1f}%  sumR={wo.sum():+.1f}")
