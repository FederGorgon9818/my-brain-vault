"""
ORB + Fast-Retest core backtest engine -- FIXED version.

Changes vs. the original orb_retest_backtest.py:

1. FILL FIX (the big one): the retest/fill condition used to accept a "touch"
   within a tolerance band (level*(1+/-tol), ~9 pts on NQ) but then assumed a
   fill at the exact `level`. That let trades count -- and fill at a better
   price -- even when the level was never actually reached. Fixed: fill only
   fires when the bar's low/high actually reaches the level (real touch).
   Everything else (OR calc, breakout detection, minimum-excursion
   requirement, fast-retest window, stop, target, EoD exit) is UNCHANGED --
   this only fixes whether a fill would really have happened.

2. MAE TRACKING: every trade now also returns `mae_r`, the worst adverse
   excursion (in R) reached at any point between entry and exit -- even for
   trades that end up winners. This lets the risk / prop-sizing layer see the
   real intra-trade drawdown instead of just the closed-trade result.

3. R_PTS returned per trade so cost application downstream is exact (not an
   approximation via a separately re-joined daily OR size).

No dependency on quantpad_data -- reads local cached parquet only.
"""
import numpy as np
import pandas as pd

# ----------------------------- parameters ---------------------------------
OR_MIN = 5
EXCURSION_PCT = 0.20
TOL_PCT = 0.05          # still used for the *excursion* check (paper logic),
                        # NOT for the fill/touch check anymore (that's the fix)
RETEST_MAX_MIN = 20
TARGET_R = 3.0
STOP_MODE = "tight"
STOP_FRAC = 0.25
RISK_PCT = 0.01
START_EQ = 25_000
RTH_START = "09:30"


def simulate_day(tmin, o, h, lw, c, params, diag=None):
    """Return (r, direction, mins_to_retest, exit_kind, mae_r, R_pts) or None."""
    or_min = params["OR_MIN"]
    exc = params["EXCURSION_PCT"] / 100.0
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

    # --- first breakout ---
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
    stop_mode = params.get("STOP_MODE", "tight")
    stop_frac = params.get("STOP_FRAC", 0.25)
    or_size = orh - orl
    if stop_mode == "opposite":
        stop = orl if direction == 1 else orh
    else:
        stop = level - stop_frac * or_size if direction == 1 else level + stop_frac * or_size
    R = level - stop if direction == 1 else stop - level
    if R <= 0:
        return None
    t0 = tmin[i0]

    # --- require min favourable excursion, then a REAL retest touch ---
    idx = np.arange(i0, tmin.size)
    exc_done = False
    exc_bar = None
    mfe_pre = 0.0
    retest_bar = None
    for j in idx:
        if direction == 1:
            fav = (h[j] - level) / level
            if fav > mfe_pre:
                mfe_pre = fav
            if not exc_done and fav >= exc:
                exc_done, exc_bar = True, j
            # FIX: real touch only (was: lw[j] <= level * (1 + tol))
            if exc_done and j > exc_bar and lw[j] <= level:
                retest_bar = j
                break
        else:
            fav = (level - lw[j]) / level
            if fav > mfe_pre:
                mfe_pre = fav
            if not exc_done and fav >= exc:
                exc_done, exc_bar = True, j
            # FIX: real touch only (was: h[j] >= level * (1 - tol))
            if exc_done and j > exc_bar and h[j] >= level:
                retest_bar = j
                break
    if retest_bar is None:
        return None

    mins_to_retest = int(tmin[retest_bar] - t0)

    if diag is not None:
        _classify_outcome(tmin, h, lw, retest_bar, direction, level, orl if direction == 1 else orh,
                          mfe_pre, mins_to_retest, diag)

    if mins_to_retest > tmax:
        return None

    entry = level
    target = None
    if target_r is not None:
        target = entry + target_r * R if direction == 1 else entry - target_r * R

    exit_price = c[-1]
    exit_kind = "eod"
    # MAE: worst adverse price from the entry bar through the exit bar (inclusive)
    mae_price = lw[retest_bar] if direction == 1 else h[retest_bar]
    for j in range(retest_bar + 1, tmin.size):
        if direction == 1:
            mae_price = min(mae_price, lw[j])
            if lw[j] <= stop:
                exit_price, exit_kind = stop, "stop"
                break
            if target is not None and h[j] >= target:
                exit_price, exit_kind = target, "target"
                break
        else:
            mae_price = max(mae_price, h[j])
            if h[j] >= stop:
                exit_price, exit_kind = stop, "stop"
                break
            if target is not None and lw[j] <= target:
                exit_price, exit_kind = target, "target"
                break

    r_mult = (exit_price - entry) / R if direction == 1 else (entry - exit_price) / R
    mae_r = (entry - mae_price) / R if direction == 1 else (mae_price - entry) / R
    return r_mult, direction, mins_to_retest, exit_kind, mae_r, R


def _classify_outcome(tmin, h, lw, retest_bar, direction, level, fail_level,
                      mfe_pre, mins_to_retest, diag):
    t_r = tmin[retest_bar]
    mfe_level = level * (1 + mfe_pre) if direction == 1 else level * (1 - mfe_pre)
    outcome = "neutral"
    for j in range(retest_bar + 1, tmin.size):
        if tmin[j] - t_r > 60:
            break
        if direction == 1:
            if h[j] >= mfe_level:
                outcome = "cont"
                break
            if lw[j] <= fail_level:
                outcome = "fail"
                break
        else:
            if lw[j] <= mfe_level:
                outcome = "cont"
                break
            if h[j] >= fail_level:
                outcome = "fail"
                break
    diag["rows"].append((mins_to_retest, outcome))


def run_backtest(df_et, params, collect_diag=False):
    params = params.copy()
    et_naive = df_et.index.tz_localize(None) if df_et.index.tz is not None else df_et.index
    day_norm = et_naive.normalize()
    tmin_all = ((et_naive - day_norm - pd.Timedelta(hours=9, minutes=30))
                / pd.Timedelta(minutes=1))
    o = df_et["o"].to_numpy()
    h = df_et["h"].to_numpy()
    lw = df_et["l"].to_numpy()
    c = df_et["c"].to_numpy()
    tmin_all = tmin_all.to_numpy().astype(int)
    day_key = (et_naive.year * 10000 + et_naive.month * 100 + et_naive.day).to_numpy()

    diag = {"rows": []} if collect_diag else None
    trades = []
    uniq, starts = np.unique(day_key, return_index=True)
    starts = list(starts) + [len(day_key)]
    for k in range(len(uniq)):
        s, e = starts[k], starts[k + 1]
        res = simulate_day(tmin_all[s:e], o[s:e], h[s:e], lw[s:e], c[s:e], params, diag=diag)
        if res is not None:
            r_mult, direction, mtr, exit_kind, mae_r, r_pts = res
            trades.append({"date": day_norm[s], "r": r_mult, "dir": direction,
                           "mins_to_retest": mtr, "exit": exit_kind,
                           "mae_r": mae_r, "R_pts": r_pts})
    return pd.DataFrame(trades), diag


def metrics(trades, bench_daily=None, risk_pct=RISK_PCT, start_eq=START_EQ, cal=None):
    if len(trades) == 0:
        return None, None
    tr = trades.set_index("date").sort_index()
    daily_r = tr["r"]
    eq = (1 + risk_pct * daily_r).cumprod() * start_eq
    if cal is None:
        cal = bench_daily.index if bench_daily is not None else eq.index
    eq_full = eq.reindex(cal).ffill().fillna(start_eq)
    rets = eq_full.pct_change().fillna(0)
    n_years = (cal[-1] - cal[0]).days / 365.25
    total_ret = eq_full.iloc[-1] / start_eq - 1
    cagr = (eq_full.iloc[-1] / start_eq) ** (1 / n_years) - 1
    sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
    dd = (eq_full / eq_full.cummax() - 1).min()
    wins = daily_r[daily_r > 0]
    losses = daily_r[daily_r <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else np.nan
    return {
        "trades": len(tr), "years": n_years, "total_return": total_ret, "cagr": cagr,
        "sharpe": sharpe, "max_dd": dd, "win_rate": (daily_r > 0).mean(),
        "avg_r": daily_r.mean(), "profit_factor": pf,
        "pct_long": (tr["dir"] == 1).mean(), "final_eq": eq_full.iloc[-1],
    }, eq_full
