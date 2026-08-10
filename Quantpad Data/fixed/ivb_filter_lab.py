"""
IVB filter lab: can orderflow-PROXY filters turn the IVB breakout skeleton
(net ~breakeven) into a real edge?

Skeleton (fixed, from ivb_test.py variant A):
  OR = 09:30-10:00 ET. First 5m close outside OR after 10:00. Entry next 1m
  open. Stop = opposite OR level. Target = 1R. Flat 15:00 ET. 1 trade/day.
  Costs 0.87 NQ pts per round turn. Baseline win rate ~50%.

Honesty design:
  - Trade outcomes are computed ONCE (filters only subset the trade table),
    all features known strictly before entry (signal bar is closed; trailing
    stats use prior days only).
  - Filter selection on IS 2016-2021, validation on OOS 2022-2025.
  - Multiple-testing count is printed. A filter only "survives" if it beats
    the unfiltered skeleton net Sharpe on IS AND OOS and keeps n reasonable.

Proxy features (1m OHLCV+V only -- real bid/ask delta NOT available):
  d_delta   tick-rule delta of 5m signal bar, direction-aligned
  d_ratio   d_delta / signal bar volume
  cum_d     session cumulative tick-rule delta through signal bar, aligned
  or_d      tick-rule delta inside the OR window, aligned
  relvol    signal 5m volume / mean same-slot 5m volume prior 20 days
  clv       close location of signal bar, aligned (1 = closed at extreme)
  disp      (5m close - level) / OR width, in breakout direction
  vwap_ok   entry side of session VWAP at signal close
  sig_t     minutes after 09:30 of signal bar start
  orw_rel   OR width / trailing 20-day median OR width
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

rows = []
or_widths = {}
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
    or_widths[d] = orw

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
    exit_price, exit_kind = c[-1], "eod"
    for j in range(ei, len(tm)):
        if tm[j] >= FLAT_MIN:
            exit_price, exit_kind = o[j], "eod"
            break
        hit_stop = lw[j] <= stop if dirn == 1 else h[j] >= stop
        hit_tgt = h[j] >= target if dirn == 1 else lw[j] <= target
        if hit_stop:
            exit_price, exit_kind = stop, "stop"
            break
        if hit_tgt:
            exit_price, exit_kind = target, "target"
            break
    r = (exit_price - entry) * dirn / R

    sig_delta = np.sum(np.sign(c[sidx] - o[sidx]) * v[sidx])
    sig_vol = v[sidx].sum()
    upto = np.where(tm < b + 5)[0]
    cum_delta = np.sum(np.sign(c[upto] - o[upto]) * v[upto])
    or_idx = np.where(orm)[0]
    or_delta = np.sum(np.sign(c[or_idx] - o[or_idx]) * v[or_idx])
    tp = (h[upto] + lw[upto] + c[upto]) / 3
    vwap = np.sum(tp * v[upto]) / max(v[upto].sum(), 1)
    h5, l5 = h[sidx].max(), lw[sidx].min()
    clv_raw = (c5 - l5) / (h5 - l5) if h5 > l5 else 0.5
    rows.append({
        "date": d, "dir": dirn, "r": r, "R_pts": R, "exit": exit_kind,
        "slot": b, "sig_vol": sig_vol, "orw": orw,
        "d_delta": dirn * sig_delta,
        "d_ratio": dirn * sig_delta / max(sig_vol, 1),
        "cum_d": dirn * cum_delta,
        "or_d": dirn * or_delta,
        "clv": clv_raw if dirn == 1 else 1 - clv_raw,
        "disp": dirn * (c5 - level) / orw,
        "vwap_ok": dirn * (c5 - vwap) > 0,
        "sig_t": b,
    })

tr = pd.DataFrame(rows).set_index("date").sort_index()
tr["r_net"] = tr["r"] - COST_PTS_RT / tr["R_pts"]

# trailing stats (prior days only -- shift(1))
oww = pd.Series(or_widths).sort_index()
tr["orw_rel"] = tr["orw"] / oww.rolling(20).median().shift(1).reindex(tr.index)
# same-slot relative volume, prior 20 days
slot_vol = tr.pivot_table(index=tr.index, columns="slot", values="sig_vol")
base = slot_vol.rolling(20, min_periods=10).mean().shift(1)
tr["relvol"] = np.array([
    tr.loc[d, "sig_vol"] / base.loc[d, s] if (d in base.index and not np.isnan(base.loc[d, s])) else np.nan
    for d, s in zip(tr.index, tr["slot"])])

cal = pd.DatetimeIndex(sorted(df["day"].unique()))


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
    yearly = rc.groupby(rc.index.year).sum()
    return {"n": len(rc), "win": 100 * (rc > 0).mean(), "avgR": rc.mean(),
            "pf": pf, "sharpe": sharpe,
            "tot": 100 * (eq_full.iloc[-1] / START_EQ - 1),
            "posyrs": f"{(yearly > 0).sum()}/{len(yearly)}"}


FILTERS = {
    "—— ungefiltert": lambda t: pd.Series(True, index=t.index),
    "delta>0": lambda t: t["d_delta"] > 0,
    "d_ratio>=0.15": lambda t: t["d_ratio"] >= 0.15,
    "d_ratio>=0.30": lambda t: t["d_ratio"] >= 0.30,
    "cum_delta>0": lambda t: t["cum_d"] > 0,
    "or_delta>0": lambda t: t["or_d"] > 0,
    "relvol>=1.2": lambda t: t["relvol"] >= 1.2,
    "relvol>=1.5": lambda t: t["relvol"] >= 1.5,
    "clv>=0.7": lambda t: t["clv"] >= 0.7,
    "disp>=0.10": lambda t: t["disp"] >= 0.10,
    "disp>=0.25": lambda t: t["disp"] >= 0.25,
    "vwap_side": lambda t: t["vwap_ok"],
    "sig<=11:00": lambda t: t["sig_t"] <= 90,
    "sig<=12:00": lambda t: t["sig_t"] <= 150,
    "orw_rel<=1.0": lambda t: t["orw_rel"] <= 1.0,
    "orw_rel>=1.0": lambda t: t["orw_rel"] >= 1.0,
    "long only": lambda t: t["dir"] == 1,
    "short only": lambda t: t["dir"] == -1,
}

is_mask = tr.index <= IS_END
cal_is, cal_oos = cal[cal <= IS_END], cal[cal > IS_END]


def fmt(s):
    if s is None:
        return "n<30".ljust(58)
    return (f"n={s['n']:4d} win={s['win']:4.1f}% avgR={s['avgR']:+.3f} "
            f"PF={s['pf']:4.2f} Sh={s['sharpe']:+5.2f} tot={s['tot']:+7.1f}% posJ={s['posyrs']}")


print(f"IVB-Filter-Lab | Skelett fixiert | IS 2016-2021, OOS 2022-2025 | "
      f"{len(FILTERS)} Einzelfilter (Multiple-Testing beachten!)\n")
print(f"{'Filter':16s} | {'IS (Selektion)':58s} | OOS (Validierung)")
results = {}
for name, f in FILTERS.items():
    m = f(tr).fillna(False)
    s_is = stats(tr[m & is_mask], cal_is)
    s_oos = stats(tr[m & ~is_mask], cal_oos)
    results[name] = (s_is, s_oos, m)
    print(f"{name:16s} | {fmt(s_is)} | {fmt(s_oos)}")

# combos of the top IS single filters (exclude trivial/ungefiltert)
ranked = sorted(((n, r) for n, r in results.items()
                 if r[0] is not None and n != "—— ungefiltert"),
                key=lambda x: -x[1][0]["sharpe"])
top = [n for n, _ in ranked[:4]]
print(f"\nTop-4 IS-Filter: {top} -> paarweise Kombos + Triple")
import itertools
for combo in list(itertools.combinations(top, 2)) + list(itertools.combinations(top, 3)):
    m = np.logical_and.reduce([results[n][2] for n in combo])
    m = pd.Series(m, index=tr.index)
    s_is = stats(tr[m & is_mask], cal_is)
    s_oos = stats(tr[m & ~is_mask], cal_oos)
    label = "+".join(c[:10] for c in combo)
    print(f"{label:34s} | {fmt(s_is)} | {fmt(s_oos)}")

n_configs = len(FILTERS) + len(list(itertools.combinations(top, 2))) + len(list(itertools.combinations(top, 3)))
print(f"\nGetestete Konfigurationen gesamt: {n_configs}")
print("Survivor-Kriterium: netto IS-Sharpe UND OOS-Sharpe > ungefiltert, n>=150, posJahre stabil.")
