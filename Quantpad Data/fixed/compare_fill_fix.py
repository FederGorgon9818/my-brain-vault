"""
Direct A/B comparison: OLD (buggy tolerance-fill) vs NEW (real-touch fill),
same data (2019-01-01..2025-01-01, matching the original headline test),
same parameters (OR=5, retest<=20, stop=0.25 tight, target=3R).
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed")
import orb_core_v2 as core

CACHE = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
START, END = "2019-01-01", "2025-01-01"

PARAMS = dict(OR_MIN=5, EXCURSION_PCT=0.20, TOL_PCT=0.05, RETEST_MAX_MIN=20,
              TARGET_R=3.0, STOP_MODE="tight", STOP_FRAC=0.25)


# ---- OLD (buggy) simulate_day, verbatim logic from orb_retest_backtest.py ----
def simulate_day_old(tmin, o, h, lw, c, params):
    or_min = params["OR_MIN"]
    exc = params["EXCURSION_PCT"] / 100.0
    tol = params["TOL_PCT"] / 100.0
    tmax = params["RETEST_MAX_MIN"]
    target_r = params["TARGET_R"]

    or_mask = tmin < or_min
    if or_mask.sum() < max(3, or_min * 0.5):
        return None
    orh = h[or_mask].max()
    orl = lw[or_mask].min()
    if orh <= orl:
        return None
    post = np.where(tmin >= or_min)[0]
    if post.size == 0:
        return None
    i0 = None
    direction = 0
    for i in post:
        up = h[i] > orh
        dn = lw[i] < orl
        if up and dn:
            return None
        if up:
            i0, direction = i, 1
            break
        if dn:
            i0, direction = i, -1
            break
    if i0 is None:
        return None
    level = orh if direction == 1 else orl
    stop_frac = params.get("STOP_FRAC", 0.25)
    or_size = orh - orl
    stop = level - stop_frac * or_size if direction == 1 else level + stop_frac * or_size
    R = level - stop if direction == 1 else stop - level
    if R <= 0:
        return None
    t0 = tmin[i0]
    idx = np.arange(i0, tmin.size)
    exc_done = False
    exc_bar = None
    retest_bar = None
    for j in idx:
        if direction == 1:
            fav = (h[j] - level) / level
            if not exc_done and fav >= exc:
                exc_done, exc_bar = True, j
            # THE BUG: tolerance band, not a real touch
            if exc_done and j > exc_bar and lw[j] <= level * (1 + tol):
                retest_bar = j
                break
        else:
            fav = (level - lw[j]) / level
            if not exc_done and fav >= exc:
                exc_done, exc_bar = True, j
            if exc_done and j > exc_bar and h[j] >= level * (1 - tol):
                retest_bar = j
                break
    if retest_bar is None:
        return None
    mins_to_retest = int(tmin[retest_bar] - t0)
    if mins_to_retest > tmax:
        return None
    entry = level  # <- assumed fill at exact level even if never touched
    target = entry + target_r * R if direction == 1 else entry - target_r * R
    exit_price = c[-1]
    for j in range(retest_bar + 1, tmin.size):
        if direction == 1:
            if lw[j] <= stop:
                exit_price = stop
                break
            if h[j] >= target:
                exit_price = target
                break
        else:
            if h[j] >= stop:
                exit_price = stop
                break
            if lw[j] <= target:
                exit_price = target
                break
    r_mult = (exit_price - entry) / R if direction == 1 else (entry - exit_price) / R
    return {"r": r_mult, "dir": direction, "mins_to_retest": mins_to_retest}


def run_old(df_et, params):
    et_naive = df_et.index.tz_localize(None) if df_et.index.tz is not None else df_et.index
    day_norm = et_naive.normalize()
    tmin_all = ((et_naive - day_norm - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).to_numpy().astype(int)
    o, h, lw, c = (df_et[col].to_numpy() for col in ("o", "h", "l", "c"))
    day_key = (et_naive.year * 10000 + et_naive.month * 100 + et_naive.day).to_numpy()
    uniq, starts = np.unique(day_key, return_index=True)
    starts = list(starts) + [len(day_key)]
    trades = []
    for k in range(len(uniq)):
        s, e = starts[k], starts[k + 1]
        res = simulate_day_old(tmin_all[s:e], o[s:e], h[s:e], lw[s:e], c[s:e], params)
        if res is not None:
            res["date"] = day_norm[s]
            trades.append(res)
    return pd.DataFrame(trades)


def metrics_simple(trades, cal, risk_pct=0.01, start_eq=25_000):
    tr = trades.set_index("date").sort_index()
    r = tr["r"]
    eq = (1 + risk_pct * r).cumprod() * start_eq
    eq_full = eq.reindex(cal).ffill().fillna(start_eq)
    rets = eq_full.pct_change().fillna(0)
    n_years = (cal[-1] - cal[0]).days / 365.25
    total = eq_full.iloc[-1] / start_eq - 1
    cagr = (eq_full.iloc[-1] / start_eq) ** (1 / n_years) - 1
    sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
    dd = (eq_full / eq_full.cummax() - 1).min()
    wins, losses = r[r > 0], r[r <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("nan")
    return dict(trades=len(tr), total_return=total, cagr=cagr, sharpe=sharpe,
                max_dd=dd, win_rate=(r > 0).mean(), avg_r=r.mean(), profit_factor=pf)


def main():
    print(f"Loading cached NQ 1m RTH data, slicing {START}..{END} ...")
    df = pd.read_parquet(CACHE)
    df = df.loc[START:END]
    print(f"  bars: {len(df):,}")

    cal = pd.DatetimeIndex(sorted(pd.unique(df.index.tz_localize(None).normalize())))

    print("\nRunning OLD (buggy tolerance-fill) ...")
    old_trades = run_old(df, PARAMS)
    old_m = metrics_simple(old_trades, cal)

    print("Running NEW (real-touch fill + MAE) ...")
    new_trades, _ = core.run_backtest(df, PARAMS, collect_diag=False)
    new_m, _ = core.metrics(new_trades, cal=cal)

    print("\n=== OLD (buggy) vs NEW (fixed fill) -- NQ 2019-2025, same params ===")
    keys = ["trades", "total_return", "cagr", "sharpe", "max_dd", "win_rate", "profit_factor", "avg_r"]
    print(f"  {'metric':16s} {'OLD':>12s} {'NEW':>12s}")
    for k in keys:
        ov, nv = old_m[k], new_m[k]
        if isinstance(ov, float):
            print(f"  {k:16s} {ov:>12.4f} {nv:>12.4f}")
        else:
            print(f"  {k:16s} {ov:>12} {nv:>12}")

    pct_removed = 1 - len(new_trades) / len(old_trades)
    print(f"\n  Trades removed by fix: {len(old_trades) - len(new_trades)} "
          f"({pct_removed:.1%} of old trade count -- these were phantom / optimistic fills)")

    new_trades.to_parquet(r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed\core_fixed_2019_2025.parquet")
    print("\nSaved fixed-core trades -> fixed/core_fixed_2019_2025.parquet")


if __name__ == "__main__":
    main()
