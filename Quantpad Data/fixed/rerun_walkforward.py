"""
Walk-forward re-validation with the FIXED (real-touch-fill) engine.

Grid focused (for runtime) on what the fixed-engine sweep flagged as
promising (OR=30, fast retest, EoD exit) plus the original guess (OR=5,
retest 20, target 3R) as a reference point -- so we can see honestly whether
EITHER survives out-of-sample re-optimization, not just in-sample.
"""
import sys
import itertools
import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed")
import orb_core_v2 as core

CACHE = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
RISK_PCT = 0.01
START_EQ = 25_000

FIXED = dict(EXCURSION_PCT=0.20, TOL_PCT=0.05, STOP_MODE="tight")
GRID = dict(
    OR_MIN=[5, 15, 30],
    RETEST_MAX_MIN=[10, 20],
    STOP_FRAC=[0.25, 0.5],
    TARGET_R=[3.0, None],
)


def combos(grid):
    keys = list(grid.keys())
    for vals in itertools.product(*[grid[k] for k in keys]):
        p = dict(zip(keys, vals))
        p.update(FIXED)
        yield p


def sqn(trades):
    if len(trades) < 15:
        return -1e9
    r = trades["r"].to_numpy()
    sd = r.std()
    if sd == 0:
        return -1e9
    return r.mean() / sd * np.sqrt(len(r))


def slice_dates(rth, date_index, start, end):
    mask = (date_index >= start) & (date_index < end)
    return rth[mask]


def eq_metrics(trades, cal, risk_pct=RISK_PCT, start_eq=START_EQ):
    if len(trades) == 0:
        idx = pd.DatetimeIndex(cal)
        return dict(total=0.0, cagr=0.0, sharpe=0.0, maxdd=0.0, trades=0, win=0.0, pf=np.nan), pd.Series(start_eq, index=idx)
    tr = trades.set_index("date").sort_index()
    r = tr["r"]
    eq = (1 + risk_pct * r).cumprod() * start_eq
    eq_full = eq.reindex(cal).ffill().fillna(start_eq)
    rets = eq_full.pct_change().fillna(0)
    n_years = max((cal[-1] - cal[0]).days / 365.25, 1e-9)
    total = eq_full.iloc[-1] / start_eq - 1
    cagr = (eq_full.iloc[-1] / start_eq) ** (1 / n_years) - 1
    sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0.0
    maxdd = (eq_full / eq_full.cummax() - 1).min()
    wins, losses = r[r > 0], r[r <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else np.nan
    return dict(total=total, cagr=cagr, sharpe=sharpe, maxdd=maxdd,
                trades=len(r), win=(r > 0).mean(), pf=pf), eq_full


def main():
    print("Loading cached NQ RTH 1m data ...")
    rth = pd.read_parquet(CACHE)
    date_index = rth.index.tz_localize(None).normalize()
    all_dates = pd.DatetimeIndex(sorted(pd.unique(date_index)))
    print(f"  {len(rth):,} bars, {len(all_dates)} days ({all_dates[0].date()}..{all_dates[-1].date()})")

    is_len = pd.DateOffset(months=24)
    oos_len = pd.DateOffset(months=6)
    step = pd.DateOffset(months=6)
    data_start = all_dates[0].normalize()
    data_end = all_dates[-1].normalize() + pd.Timedelta(days=1)

    grid = list(combos(GRID))
    print(f"  grid size: {len(grid)} combos/window")

    oos_parts = []
    choices = []
    cursor = data_start
    win_n = 0
    while True:
        is_s = cursor
        is_e = is_s + is_len
        oos_s = is_e
        oos_e = min(oos_s + oos_len, data_end)
        if oos_s >= data_end:
            break
        win_n += 1
        is_df = slice_dates(rth, date_index, is_s, is_e)
        best_p, best_score = None, -1e18
        for p in grid:
            tr, _ = core.run_backtest(is_df, p)
            sc = sqn(tr)
            if sc > best_score:
                best_score, best_p = sc, p
        oos_df = slice_dates(rth, date_index, oos_s, oos_e)
        otr, _ = core.run_backtest(oos_df, best_p)
        oos_parts.append(otr)
        choices.append(dict(oos_start=oos_s, n_oos=len(otr),
                            OR=best_p["OR_MIN"], tmax=best_p["RETEST_MAX_MIN"],
                            stop=best_p["STOP_FRAC"], tgt=best_p["TARGET_R"]))
        print(f"  window {win_n}: IS {is_s.date()}..{is_e.date()} -> best "
              f"OR={best_p['OR_MIN']} tmax={best_p['RETEST_MAX_MIN']} "
              f"stop={best_p['STOP_FRAC']} tgt={best_p['TARGET_R']} "
              f"| OOS trades={len(otr)}")
        cursor = cursor + step

    oos_trades = pd.concat(oos_parts).sort_values("date").reset_index(drop=True)
    oos_cal = all_dates[all_dates >= choices[0]["oos_start"]]
    m, eq = eq_metrics(oos_trades, oos_cal)

    print("\n=== FIXED-engine WALK-FORWARD out-of-sample (stitched) ===")
    for k, v in m.items():
        print(f"  {k:8s}: {v:.4f}" if isinstance(v, float) else f"  {k:8s}: {v}")

    print("\n--- chosen params per OOS window ---")
    ch = pd.DataFrame(choices)
    ch["oos_start"] = ch["oos_start"].dt.date
    print(ch.to_string(index=False))

    oos_trades.to_parquet(r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed\oos_trades_fixed.parquet")
    print(f"\nSaved {len(oos_trades)} fixed-engine OOS trades -> fixed/oos_trades_fixed.parquet")
    print(f"(original buggy-engine OOS had 506 trades, CAGR 36.4%, Sharpe 2.02 -- for comparison)")


if __name__ == "__main__":
    main()
