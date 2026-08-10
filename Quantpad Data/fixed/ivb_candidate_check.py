"""
Robustness check for the one surviving IVB-lab candidate:
  LONG breakouts only + OR-window tick-delta > 0 + signal-bar delta ratio >= X.

Checks: neighbour thresholds, yearly stability, tail concentration, streaks,
plus a PROPERLY computed relative-volume feature (the lab version had too few
same-slot observations because it only used trade days; here the baseline uses
ALL days' 5m volumes).
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
OR_MIN, FLAT_MIN = 30, 330
COST_PTS_RT = 0.87
RISK_PCT, START_EQ = 0.01, 25_000
IS_END = pd.Timestamp("2021-12-31")

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())

# 5m volume matrix over ALL days (for honest relvol baseline)
df["slot"] = (df["tmin"] // 5) * 5
vol5 = df.pivot_table(index="day", columns="slot", values="v", aggfunc="sum")
vol5_base = vol5.rolling(20, min_periods=10).mean().shift(1)

rows = []
for d, g in df.groupby("day", sort=True):
    tm = g["tmin"].to_numpy()
    o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))
    orm = tm < OR_MIN
    if orm.sum() < 15:
        continue
    orh, orl = h[orm].max(), lw[orm].min()
    orw = orh - orl
    if orw <= 0:
        continue
    sig = None
    for b in range(OR_MIN, FLAT_MIN, 5):
        m = (tm >= b) & (tm < b + 5)
        if not m.any():
            continue
        idx = np.where(m)[0]
        c5 = c[idx[-1]]
        if c5 > orh:
            dirn = 1
        elif c5 < orl:
            dirn = -1
        else:
            continue
        sig = (b, idx, dirn, c5)
        break
    if sig is None:
        continue
    b, sidx, dirn, c5 = sig
    level = orh if dirn == 1 else orl
    stop = orl if dirn == 1 else orh
    after = np.where(tm >= b + 5)[0]
    if after.size == 0:
        continue
    ei = after[0]
    entry = o[ei]
    R = (entry - stop) * dirn
    if R <= 0:
        continue
    target = entry + dirn * R
    exit_price = c[-1]
    mae_px = entry
    for j in range(ei, len(tm)):
        if tm[j] >= FLAT_MIN:
            exit_price = o[j]
            break
        mae_px = min(mae_px, lw[j]) if dirn == 1 else max(mae_px, h[j])
        hit_stop = lw[j] <= stop if dirn == 1 else h[j] >= stop
        hit_tgt = h[j] >= target if dirn == 1 else lw[j] <= target
        if hit_stop:
            exit_price = stop
            break
        if hit_tgt:
            exit_price = target
            break
    r = (exit_price - entry) * dirn / R
    mae_r = (entry - mae_px) * dirn / R if dirn == 1 else (mae_px - entry) / R

    sig_delta = np.sum(np.sign(c[sidx] - o[sidx]) * v[sidx])
    sig_vol = v[sidx].sum()
    or_idx = np.where(orm)[0]
    or_delta = np.sum(np.sign(c[or_idx] - o[or_idx]) * v[or_idx])
    or_vol = v[or_idx].sum()
    rv = np.nan
    if d in vol5_base.index and b in vol5_base.columns:
        base = vol5_base.loc[d, b]
        if not np.isnan(base) and base > 0:
            rv = sig_vol / base
    rows.append({"date": d, "dir": dirn, "r": r, "R_pts": R, "mae_r": mae_r,
                 "d_ratio": dirn * sig_delta / max(sig_vol, 1),
                 "or_d": dirn * or_delta,
                 "or_d_ratio": dirn * or_delta / max(or_vol, 1),
                 "relvol": rv})

tr = pd.DataFrame(rows).set_index("date").sort_index()
tr["r_net"] = tr["r"] - COST_PTS_RT / tr["R_pts"]
cal = pd.DatetimeIndex(sorted(df["day"].unique()))
is_mask = tr.index <= IS_END


def stats(sub, cal_seg):
    if len(sub) < 30:
        return None
    rc = sub["r_net"]
    eq = (1 + RISK_PCT * rc).cumprod() * START_EQ
    eq_full = eq.reindex(cal_seg).ffill().fillna(START_EQ)
    rets = eq_full.pct_change().fillna(0)
    sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
    wins, losses = rc[rc > 0], rc[rc <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("inf")
    return {"n": len(rc), "win": 100 * (rc > 0).mean(), "avgR": rc.mean(),
            "pf": pf, "sharpe": sharpe, "dd": 100 * (eq_full / eq_full.cummax() - 1).min()}


def fmt(s):
    if s is None:
        return "n<30"
    return (f"n={s['n']:4d} win={s['win']:4.1f}% avgR={s['avgR']:+.3f} "
            f"PF={s['pf']:4.2f} Sh={s['sharpe']:+5.2f} DD={s['dd']:5.1f}%")


print("=== 1) Nachbar-Robustheit d_ratio-Schwelle (long & or_d>0 fix) ===")
print(f"{'d_ratio >=':12s} | {'IS 2016-21':52s} | OOS 2022-25")
for x in (0.0, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50):
    m = (tr["dir"] == 1) & (tr["or_d"] > 0) & (tr["d_ratio"] >= x)
    print(f"{x:12.2f} | {fmt(stats(tr[m & is_mask], cal[cal <= IS_END])):52s} | "
          f"{fmt(stats(tr[m & ~is_mask], cal[cal > IS_END]))}")

print("\n=== 2) Nachbar-Robustheit or_delta (long & d_ratio>=0.30 fix) ===")
for cond, lab in ((tr["or_d"] > -1e18, "kein or_d-Filter"),
                  (tr["or_d"] > 0, "or_d > 0"),
                  (tr["or_d_ratio"] >= 0.05, "or_d_ratio >= 0.05"),
                  (tr["or_d_ratio"] >= 0.10, "or_d_ratio >= 0.10"),
                  (tr["or_d_ratio"] >= 0.20, "or_d_ratio >= 0.20")):
    m = (tr["dir"] == 1) & cond & (tr["d_ratio"] >= 0.30)
    print(f"{lab:20s} | {fmt(stats(tr[m & is_mask], cal[cal <= IS_END])):52s} | "
          f"{fmt(stats(tr[m & ~is_mask], cal[cal > IS_END]))}")

print("\n=== 3) relvol (korrekt berechnet) auf dem Kandidaten (long & or_d>0 & d_ratio>=0.30) ===")
cand = (tr["dir"] == 1) & (tr["or_d"] > 0) & (tr["d_ratio"] >= 0.30)
print(f"relvol verfügbar: {tr['relvol'].notna().mean()*100:.0f}% der Trades")
for cond, lab in ((tr["relvol"].notna(), "ohne relvol-Filter"),
                  (tr["relvol"] >= 1.0, "relvol >= 1.0"),
                  (tr["relvol"] >= 1.3, "relvol >= 1.3"),
                  (tr["relvol"] < 1.0, "relvol < 1.0")):
    m = cand & cond
    print(f"{lab:20s} | {fmt(stats(tr[m & is_mask], cal[cal <= IS_END])):52s} | "
          f"{fmt(stats(tr[m & ~is_mask], cal[cal > IS_END]))}")

print("\n=== 4) Kandidat (long & or_d>0 & d_ratio>=0.30): Jahres-Stabilität, netto ===")
sub = tr[cand]
yearly = sub["r_net"].groupby(sub.index.year).agg(["sum", "count", lambda x: 100 * (x > 0).mean()])
yearly.columns = ["sumR", "n", "win%"]
print(yearly.round(2).to_string())

print("\n=== 5) Tail/Konzentration/Streaks (Kandidat, gesamter Zeitraum, netto) ===")
rc = sub["r_net"]
wins = rc[rc > 0]
top5 = wins.nlargest(5).sum() / wins.sum() * 100
net_total = rc.sum()
top_day = rc.max() / net_total * 100 if net_total > 0 else np.nan
streak = mx = 0
for x in rc:
    streak = streak + 1 if x <= 0 else 0
    mx = max(mx, streak)
print(f"Trades={len(rc)}  NetR gesamt={net_total:+.1f}  Top-5-Gewinne={top5:.1f}% der Bruttogewinne  "
      f"größter Trade={top_day:.1f}% des NetR  maxLoseStreak={mx}")
print(f"MAE: avg={sub['mae_r'].mean():.2f}R  p95={sub['mae_r'].quantile(0.95):.2f}R  "
      f"max={sub['mae_r'].max():.2f}R  |  median R_pts={sub['R_pts'].median():.1f}")

print("\n=== 6) Referenz: long only OHNE Delta-Filter (Drift-Kontrolle) ===")
m = tr["dir"] == 1
print(f"{'long pur':20s} | {fmt(stats(tr[m & is_mask], cal[cal <= IS_END])):52s} | "
      f"{fmt(stats(tr[m & ~is_mask], cal[cal > IS_END]))}")
