"""
Final honest report:
1. Net-of-costs metrics on the FIXED walk-forward OOS trades (using the
   per-trade R_pts already computed by the fixed engine -- no re-fetch needed).
2. MAE stats: how far against the position did trades move before resolving,
   even the winners.
3. Re-run the Paper-2 continuation-rate validation with the FIXED (real-touch)
   retest detection, over the full 2016-2025 cached range, to check whether
   that finding survives the same fill fix.
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed")
import orb_core_v2 as core

FIXED_DIR = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed"
CACHE = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"

SLIP_TICKS = 1.0
TICK_PTS = 0.25
COMMISSION_RT_USD = 0.74
MNQ_POINTVALUE = 2.0
RISK_PCT = 0.01
START_EQ = 25_000


def part1_costs():
    tr = pd.read_parquet(f"{FIXED_DIR}\\oos_trades_fixed.parquet").sort_values("date").reset_index(drop=True)
    cost_pts = 2 * SLIP_TICKS * TICK_PTS + COMMISSION_RT_USD / MNQ_POINTVALUE
    tr["r_net"] = tr["r"] - cost_pts / tr["R_pts"]

    print("=== 1) NET-OF-COSTS on fixed-engine walk-forward OOS trades ===")
    print(f"  cost per round-turn: {cost_pts:.2f} pts (1 tick/side slip + $0.74 comm)")
    print(f"  median R_pts: {tr['R_pts'].median():.1f}  ->  median cost = "
          f"{(cost_pts / tr['R_pts'].median()):.3f} R per trade\n")

    all_days = pd.DatetimeIndex(sorted(pd.unique(tr['date'])))
    for label, col in [("gross", "r"), ("net", "r_net")]:
        r = tr.set_index("date")[col]
        eq = (1 + RISK_PCT * r).cumprod() * START_EQ
        eq_full = eq.reindex(all_days).ffill().fillna(START_EQ)
        rets = eq_full.pct_change().fillna(0)
        yrs = (all_days[-1] - all_days[0]).days / 365.25
        cagr = (eq_full.iloc[-1] / START_EQ) ** (1 / yrs) - 1
        sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
        dd = (eq_full / eq_full.cummax() - 1).min()
        wins, losses = r[r > 0], r[r <= 0]
        pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("nan")
        print(f"  [{label:5s}] total {eq_full.iloc[-1]/START_EQ-1:>8.1%}  CAGR {cagr:>7.1%}  "
              f"Sharpe {sharpe:>6.2f}  MaxDD {dd:>7.1%}  win {r.gt(0).mean():>6.1%}  PF {pf:>5.2f}")

    print("\n=== 2) MAE (max adverse excursion) stats, ALL trades incl. winners ===")
    print(f"  mean MAE  : {tr['mae_r'].mean():.2f} R")
    print(f"  median MAE: {tr['mae_r'].median():.2f} R")
    print(f"  95th pct  : {tr['mae_r'].quantile(0.95):.2f} R")
    print(f"  max MAE   : {tr['mae_r'].max():.2f} R")
    winners = tr[tr["r"] > 0]
    print(f"\n  Winning trades only (n={len(winners)}):")
    print(f"    mean MAE: {winners['mae_r'].mean():.2f} R | median: {winners['mae_r'].median():.2f} R | "
          f"max: {winners['mae_r'].max():.2f} R")
    print(f"  -> even winning trades often dipped meaningfully against the position first;")
    print(f"     a trailing-DD prop check that includes unrealised P&L would see this,")
    print(f"     not just the closed-trade R the naive equity curve uses.")


def part2_paper2_check():
    print("\n\n=== 3) Paper-2 continuation-rate check, FIXED retest detection, full 2016-2025 ===")
    df = pd.read_parquet(CACHE)
    params = dict(OR_MIN=5, EXCURSION_PCT=0.20, TOL_PCT=0.05, RETEST_MAX_MIN=10_000,  # no fast filter -> capture all retests for the diagnostic
                  TARGET_R=3.0, STOP_MODE="tight", STOP_FRAC=0.25)
    _, diag = core.run_backtest(df, params, collect_diag=True)
    diag_df = pd.DataFrame(diag["rows"], columns=["mtr", "outcome"])
    bins = [0, 10, 20, 30, 45, 60, 10_000]
    labels = ["0-10", "10-20", "20-30", "30-45", "45-60", ">60"]
    diag_df["bucket"] = pd.cut(diag_df["mtr"], bins=bins, labels=labels, right=True)
    val = diag_df.groupby("bucket", observed=True)["outcome"].apply(
        lambda s: pd.Series({"n": len(s), "cont": (s == "cont").mean(), "fail": (s == "fail").mean()})).unstack()
    print(val.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n  (compare to original/buggy-retest table: 0-10min 63.3% cont, >60min 21.0% cont)")


if __name__ == "__main__":
    part1_costs()
    part2_paper2_check()
