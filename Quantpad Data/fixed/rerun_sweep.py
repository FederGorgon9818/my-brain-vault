"""
Full parameter sweep with the FIXED (real-touch-fill) engine, same grid as the
original sweep.py, on the cached 2019-2025 NQ data. Answers: does ANY
combination in this family have a real edge once fills are honest?
"""
import sys
import pandas as pd

sys.path.insert(0, r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\fixed")
import orb_core_v2 as core

CACHE = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
START, END = "2019-01-01", "2025-01-01"


def main():
    df = pd.read_parquet(CACHE).loc[START:END]
    cal = pd.DatetimeIndex(sorted(pd.unique(df.index.tz_localize(None).normalize())))
    print(f"Loaded {len(df):,} bars, {len(cal)} days")

    grid = []
    for or_min in (5, 15, 30):
        for tmax in (10, 20):
            for stop_mode, stop_frac in (("opposite", None), ("tight", 0.25), ("tight", 0.5)):
                for target_r in (None, 3, 5, 10):
                    grid.append(dict(OR_MIN=or_min, EXCURSION_PCT=0.20, TOL_PCT=0.05,
                                     RETEST_MAX_MIN=tmax, TARGET_R=target_r,
                                     STOP_MODE=stop_mode, STOP_FRAC=stop_frac))

    rows = []
    for p in grid:
        trades, _ = core.run_backtest(df, p, collect_diag=False)
        if len(trades) < 30:
            continue
        m, _ = core.metrics(trades, cal=cal)
        rows.append({
            "OR": p["OR_MIN"], "tmax": p["RETEST_MAX_MIN"],
            "stop": p["STOP_MODE"] + (f"{p['STOP_FRAC']}" if p["STOP_MODE"] == "tight" else ""),
            "tgt": "EoD" if p["TARGET_R"] is None else p["TARGET_R"],
            "N": m["trades"], "totRet": m["total_return"], "CAGR": m["cagr"],
            "Sharpe": m["sharpe"], "MaxDD": m["max_dd"], "win": m["win_rate"],
            "avgR": m["avg_r"], "PF": m["profit_factor"],
        })
    res = pd.DataFrame(rows).sort_values("Sharpe", ascending=False)
    pd.set_option("display.width", 200, "display.max_rows", 200)
    print("\n=== FIXED-engine sweep, ranked by Sharpe (best first) ===")
    print(res.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    n_positive_sharpe = (res["Sharpe"] > 0).sum()
    n_positive_pf = (res["PF"] > 1).sum()
    print(f"\n  Combos with Sharpe > 0: {n_positive_sharpe} / {len(res)}")
    print(f"  Combos with PF > 1    : {n_positive_pf} / {len(res)}")
    print(f"\n  Best combo: OR={res.iloc[0]['OR']} tmax={res.iloc[0]['tmax']} "
          f"stop={res.iloc[0]['stop']} tgt={res.iloc[0]['tgt']} "
          f"-> Sharpe {res.iloc[0]['Sharpe']:.2f}, CAGR {res.iloc[0]['CAGR']:.1%}, "
          f"PF {res.iloc[0]['PF']:.2f}, N={int(res.iloc[0]['N'])}")


if __name__ == "__main__":
    main()
