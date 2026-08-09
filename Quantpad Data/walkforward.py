"""
Walk-forward validation + parameter-robustness heatmaps + return-concentration
analysis for the combined ORB + Fast-Retest strategy on NQ futures.

Walk-forward: rolling 24-month in-sample optimisation (grid search, objective =
SQN so we favour a *smooth* edge over a few outliers) -> 6-month out-of-sample,
rolled forward 6 months. The stitched OOS equity curve is the honest, overfit-
resistant performance estimate.
"""
import os
import json
import itertools
import numpy as np
import pandas as pd

from orb_retest_backtest import (fetch_1m, run_backtest, to_ms, RTH_START,
                                 RISK_PCT, START_EQ)
import quantpad_data as qpd

SYMBOL = "NQ.FUT"
START = "2016-01-01"
END = "2026-01-01"
CACHE = "nq_rth_1m.parquet"

FIXED = dict(EXCURSION_PCT=0.20, TOL_PCT=0.05)
GRID = dict(
    OR_MIN=[5, 15],
    RETEST_MAX_MIN=[10, 20],
    STOP_FRAC=[0.25, 0.5],
    TARGET_R=[3.0, 5.0, None],
    STOP_MODE=["tight"],
)


def load_rth():
    if os.path.exists(CACHE):
        df = pd.read_parquet(CACHE)
        return df
    raw = fetch_1m(SYMBOL, to_ms(START), to_ms(END))
    rth = raw.tz_convert("America/New_York").between_time(RTH_START, "15:59")
    rth.to_parquet(CACHE)
    return rth


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
        return dict(total=0.0, cagr=0.0, sharpe=0.0, maxdd=0.0,
                    trades=0, win=0.0, pf=np.nan), pd.Series(start_eq, index=idx)
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
    wins = r[r > 0]
    losses = r[r <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else np.nan
    return dict(total=total, cagr=cagr, sharpe=sharpe, maxdd=maxdd,
                trades=len(r), win=(r > 0).mean(), pf=pf), eq_full


def main():
    rth = load_rth()
    date_index = rth.index.tz_localize(None).normalize()
    all_dates = pd.DatetimeIndex(sorted(pd.unique(date_index)))
    print(f"Loaded {len(rth):,} RTH bars, {len(all_dates)} days "
          f"({all_dates[0].date()}..{all_dates[-1].date()})")

    # ---------------- WALK-FORWARD ----------------
    is_len = pd.DateOffset(months=24)
    oos_len = pd.DateOffset(months=6)
    step = pd.DateOffset(months=6)
    data_start = all_dates[0].normalize()
    data_end = all_dates[-1].normalize() + pd.Timedelta(days=1)

    grid = list(combos(GRID))
    oos_parts = []
    choices = []
    cursor = data_start
    while True:
        is_s = cursor
        is_e = is_s + is_len
        oos_s = is_e
        oos_e = min(oos_s + oos_len, data_end)
        if oos_s >= data_end:
            break
        is_df = slice_dates(rth, date_index, is_s, is_e)
        best_p, best_score = None, -1e18
        for p in grid:
            tr, _ = run_backtest(is_df, p)
            sc = sqn(tr)
            if sc > best_score:
                best_score, best_p = sc, p
        oos_df = slice_dates(rth, date_index, oos_s, oos_e)
        otr, _ = run_backtest(oos_df, best_p)
        oos_parts.append(otr)
        choices.append(dict(oos_start=oos_s, n_oos=len(otr),
                            OR=best_p["OR_MIN"], tmax=best_p["RETEST_MAX_MIN"],
                            stop=best_p["STOP_FRAC"], tgt=best_p["TARGET_R"]))
        cursor = cursor + step

    oos_trades = pd.concat(oos_parts).sort_values("date").reset_index(drop=True)
    oos_cal = all_dates[all_dates >= choices[0]["oos_start"]]
    m, eq = eq_metrics(oos_trades, oos_cal)

    print("\n=== WALK-FORWARD out-of-sample (stitched) ===")
    for k, v in m.items():
        print(f"  {k:8s}: {v:.4f}" if isinstance(v, float) else f"  {k:8s}: {v}")

    print("\n--- chosen params per OOS window ---")
    ch = pd.DataFrame(choices)
    ch["oos_start"] = ch["oos_start"].dt.date
    print(ch.to_string(index=False))

    # buy & hold benchmark over the OOS span
    bench = qpd.get_bars_with_retry(SYMBOL, "1d", to_ms(START), to_ms(END),
                                    roll_adjust="ratio")
    bench = bench[~bench.index.duplicated()].sort_index()
    bench.index = bench.index.tz_convert("America/New_York").tz_localize(None).normalize()
    bench = bench[~bench.index.duplicated()]
    b = bench["c"].reindex(oos_cal).ffill()
    bench_eq = b / b.iloc[0] * START_EQ
    print(f"\n  Buy&Hold NQ over OOS span: {bench_eq.iloc[-1]/START_EQ-1:.2%}")

    # ---------------- RETURN CONCENTRATION ----------------
    r = oos_trades["r"]
    wins = r[r > 0].sort_values(ascending=False)
    total_pos = wins.sum()
    top1 = wins.iloc[0] / total_pos if len(wins) else np.nan
    top5 = wins.iloc[:5].sum() / total_pos if len(wins) >= 5 else np.nan
    top10pct_n = max(1, int(len(wins) * 0.10))
    top10 = wins.iloc[:top10pct_n].sum() / total_pos
    # net-profit concentration by day (largest winning day vs total net R)
    net_total = r.sum()
    largest_day = r.max()
    print("\n=== RETURN CONCENTRATION (OOS) ===")
    print(f"  winning trades: {len(wins)} / {len(r)} ({len(wins)/len(r):.1%})")
    print(f"  largest single win as % of gross wins : {top1:.1%}")
    print(f"  top-5 wins as % of gross wins         : {top5:.1%}")
    print(f"  top-10% of wins as % of gross wins    : {top10:.1%}")
    print(f"  largest single day as % of NET profit : {largest_day/net_total:.1%}")
    print(f"  mean R {r.mean():.3f} | median R {r.median():.3f} | "
          f"max R {r.max():.2f} | std R {r.std():.2f}")

    # ---------------- PARAMETER HEATMAPS (full sample) ----------------
    def grid_metric(or_min, tmax, stop_list, tgt_list, vary="stop_tgt"):
        rows = []
        for a in stop_list:
            row = []
            for b2 in tgt_list:
                p = dict(OR_MIN=or_min, RETEST_MAX_MIN=tmax, STOP_FRAC=a,
                         TARGET_R=b2, STOP_MODE="tight", **FIXED)
                tr, _ = run_backtest(rth, p)
                mm, _ = eq_metrics(tr, all_dates)
                row.append(round(mm["sharpe"], 2))
            rows.append(row)
        return rows

    stop_list = [0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.75, 1.0]
    tgt_list = [2.0, 3.0, 5.0, 8.0, None]
    hm1 = grid_metric(5, 20, stop_list, tgt_list)
    print("\n=== Heatmap Sharpe: STOP_FRAC (rows) x TARGET_R (cols), OR=5 tmax=20 ===")
    print("        " + "  ".join(f"{('EoD' if t is None else t):>5}" for t in tgt_list))
    for a, row in zip(stop_list, hm1):
        print(f"  {a:>4}: " + "  ".join(f"{v:>5}" for v in row))

    # OR x RETEST heatmap at stop0.25 target3
    or_list = [5, 10, 15, 30, 60]
    tmax_list = [5, 10, 15, 20, 30]
    hm2 = []
    for om in or_list:
        row = []
        for tm in tmax_list:
            p = dict(OR_MIN=om, RETEST_MAX_MIN=tm, STOP_FRAC=0.25,
                     TARGET_R=3.0, STOP_MODE="tight", **FIXED)
            tr, _ = run_backtest(rth, p)
            mm, _ = eq_metrics(tr, all_dates)
            row.append(round(mm["sharpe"], 2))
        hm2.append(row)
    print("\n=== Heatmap Sharpe: OR_MIN (rows) x RETEST_MAX (cols), stop0.25 tgt3 ===")
    print("        " + "  ".join(f"{t:>5}" for t in tmax_list))
    for om, row in zip(or_list, hm2):
        print(f"  {om:>4}: " + "  ".join(f"{v:>5}" for v in row))

    # ---------------- WIDGETS ----------------
    eq_dates = [d.strftime("%Y-%m-%d") for d in eq.index]
    payload = json.dumps({
        "dates": eq_dates,
        "strat": [round(x, 1) for x in eq.tolist()],
        "bench": [round(x, 1) for x in bench_eq.reindex(eq.index).ffill().tolist()],
    })
    wf_html = f"""
<div style="position:relative;width:100%"><canvas id="wf"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d = {payload};
const step = Math.max(1, Math.ceil(d.dates.length/600));
const idx = d.dates.map((_,i)=>i).filter(i=>i%step===0);
new Chart(document.getElementById('wf'), {{type:'line',
  data:{{labels:idx.map(i=>d.dates[i]),datasets:[
    {{label:'Walk-forward OOS (re-optimised, 1% risk)',data:idx.map(i=>d.strat[i]),
      borderColor:'#22c55e',borderWidth:2,pointRadius:0,fill:false}},
    {{label:'Buy & Hold NQ',data:idx.map(i=>d.bench[i]),
      borderColor:'#94a3b8',borderWidth:1.5,pointRadius:0,fill:false,borderDash:[5,4]}}
  ]}},
  options:{{responsive:true,aspectRatio:1.9,
    plugins:{{legend:{{labels:{{color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
      title:{{display:true,text:'Walk-forward out-of-sample equity (start $25,000, log)',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{type:'logarithmic',ticks:{{color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8',maxTicksLimit:10}}}}}}}}
}});
</script>"""
    save_widget(wf_html, "walkforward_equity")

    def heatmap_widget(rows, row_labels, col_labels, title, name):
        flat = [v for row in rows for v in row]
        vmin, vmax = min(flat), max(flat)
        def color(v):
            t = (v - vmin) / (vmax - vmin) if vmax > vmin else 0.5
            r_ = int(220 * (1 - t) + 34 * t)
            g_ = int(70 * (1 - t) + 197 * t)
            b_ = int(70 * (1 - t) + 94 * t)
            return f"rgb({r_},{g_},{b_})"
        cells = ""
        header = "<td style='padding:4px'></td>" + "".join(
            f"<td style='padding:4px;text-align:center;font-size:11px;color:var(--color-text-primary)'>{c}</td>"
            for c in col_labels)
        cells += f"<tr>{header}</tr>"
        for rl, row in zip(row_labels, rows):
            tds = f"<td style='padding:4px;font-size:11px;color:var(--color-text-primary)'>{rl}</td>"
            for v in row:
                tds += (f"<td style='padding:8px 10px;text-align:center;font-size:11px;"
                        f"background:{color(v)};color:#0b1220;font-weight:600'>{v:.2f}</td>")
            cells += f"<tr>{tds}</tr>"
        html = f"""
<div style="font-family:monospace">
<div style="color:var(--color-text-primary);margin-bottom:6px;font-size:13px">{title}</div>
<table style="border-collapse:collapse">{cells}</table>
<div style="color:#94a3b8;font-size:11px;margin-top:6px">red = weak Sharpe, green = strong Sharpe</div>
</div>"""
        save_widget(html, name)

    heatmap_widget(hm1, [str(s) for s in stop_list],
                   ["EoD" if t is None else str(t) for t in tgt_list],
                   "Sharpe: stop fraction (rows) x profit target R (cols) | OR=5, retest<=20",
                   "heatmap_stop_target")
    heatmap_widget(hm2, [str(s) for s in or_list], [str(s) for s in tmax_list],
                   "Sharpe: opening range min (rows) x fast-retest window min (cols) | stop0.25, tgt3",
                   "heatmap_or_retest")

    # concentration Pareto widget
    r_sorted = r.sort_values(ascending=False).to_numpy()
    cum = np.cumsum(r_sorted)
    cum_share = (cum / cum[-1] * 100).tolist() if cum[-1] != 0 else []
    pareto = json.dumps({"x": list(range(1, len(r_sorted) + 1)),
                         "cum": [round(v, 1) for v in cum_share]})
    par_html = f"""
<div style="position:relative;width:100%"><canvas id="pc"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d = {pareto};
new Chart(document.getElementById('pc'), {{type:'line',
  data:{{labels:d.x,datasets:[{{label:'Cumulative % of net profit (trades sorted best->worst)',
    data:d.cum,borderColor:'#f59e0b',borderWidth:2,pointRadius:0,fill:false}}]}},
  options:{{responsive:true,aspectRatio:2.2,
    plugins:{{legend:{{labels:{{color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
      title:{{display:true,text:'Return concentration (Pareto of OOS trades)',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}},title:{{display:true,text:'% of net profit',color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8',maxTicksLimit:12}},title:{{display:true,text:'trade rank',color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(par_html, "concentration_pareto")

    # save OOS trades for prop analysis
    oos_trades.to_parquet("oos_trades.parquet")
    print("\nSaved OOS trades -> oos_trades.parquet")


if __name__ == "__main__":
    main()