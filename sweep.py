"""Parameter sweep for the combined ORB + fast-retest strategy on NQ.

Fetches 1m data once, then evaluates a grid of configurations and prints a
ranked table so we can lock in a robust, simple default.
"""
import numpy as np
import pandas as pd
import quantpad_data as qpd
from orb_retest_backtest import (fetch_1m, run_backtest, metrics, to_ms,
                                 SYMBOL, START, END, RISK_PCT, START_EQ)


def main():
    s_ms, e_ms = to_ms(START), to_ms(END)
    raw = fetch_1m(SYMBOL, s_ms, e_ms)
    rth = raw.tz_convert("America/New_York").between_time("09:30", "15:59")
    bench = qpd.get_bars_with_retry(SYMBOL, "1d", s_ms, e_ms, roll_adjust="ratio")
    bench = bench[~bench.index.duplicated()].sort_index()
    bench.index = (bench.index.tz_convert("America/New_York")
                   .tz_localize(None).normalize())
    bench = bench[~bench.index.duplicated()]
    bh_ret = bench["c"].iloc[-1] / bench["c"].iloc[0] - 1
    bh_rets = bench["c"].pct_change().fillna(0)
    bh_sharpe = bh_rets.mean() / bh_rets.std() * np.sqrt(252)
    bh_dd = (bench["c"] / bench["c"].cummax() - 1).min()
    print(f"Buy&Hold NQ: total {bh_ret:.1%} | Sharpe {bh_sharpe:.2f} | MaxDD {bh_dd:.1%}\n")

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
        trades, _ = run_backtest(rth, p, collect_diag=False)
        if len(trades) < 30:
            continue
        m, _ = metrics(trades, bench, RISK_PCT, START_EQ)
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
    print(res.to_string(index=False, float_format=lambda x: f"{x:.3f}"))


if __name__ == "__main__":
    main()