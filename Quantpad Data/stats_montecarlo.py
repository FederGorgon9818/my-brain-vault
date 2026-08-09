"""
Full performance statistics + Monte-Carlo risk analysis for the ORB Fast-Retest
strategy, using the walk-forward OUT-OF-SAMPLE trades (oos_trades.parquet).

Adds realistic costs (slippage + commission), reports the complete metric set
(gross & net), and runs a Monte-Carlo bootstrap to estimate the distribution of
  - maximum drawdown (in R and in $ for MNQ),
  - the longest losing streak (max consecutive losses),
  - terminal equity,
  - and the probability of breaching each prop-firm trailing drawdown.
"""
import json
import numpy as np
import pandas as pd

# ------------------------------ cost model --------------------------------
SLIP_TICKS   = 1.0     # slippage per side, in ticks (NQ tick = 0.25 pt)
TICK_PTS     = 0.25
COMMISSION_RT_USD = 0.74   # round-turn commission, MNQ via Tradovate-style prop
MNQ_POINTVALUE    = 2.0    # $ per point, Micro Nasdaq (MNQ)
RISK_PCT     = 0.01
START_EQ     = 25_000

PROP = {                    # firm: (trailing_DD_$, profit_target_$)
    "Topstep 50k":  (2000, 3000),
    "Apex 50k":     (2500, 3000),
    "Apex 100k":    (3000, 6000),
    "Apex/MFF 150k":(5000, 9000),
}


def max_run(mask):
    best = cur = 0
    for v in mask:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best


def metric_block(r, cal_days):
    """Full metric dict from a chronological R-series `r` (pd.Series indexed by date)."""
    eq = (1 + RISK_PCT * r).cumprod() * START_EQ
    eq_full = eq.reindex(cal_days).ffill().fillna(START_EQ)
    rets = eq_full.pct_change().fillna(0)
    yrs = (cal_days[-1] - cal_days[0]).days / 365.25
    downside = rets[rets < 0].std()
    wins = r[r > 0]
    losses = r[r <= 0]
    lose_mask = (r <= 0).to_numpy()
    win_mask = (r > 0).to_numpy()
    return {
        "trades": int(len(r)),
        "trades/yr": len(r) / yrs,
        "win_rate": win_mask.mean(),
        "avg_R": r.mean(),
        "avg_win_R": wins.mean() if len(wins) else 0.0,
        "avg_loss_R": losses.mean() if len(losses) else 0.0,
        "expectancy_R": r.mean(),
        "profit_factor": wins.sum() / abs(losses.sum()) if losses.sum() != 0 else np.nan,
        "sharpe": rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0,
        "sortino": rets.mean() / downside * np.sqrt(252) if downside and downside > 0 else 0,
        "cagr": (eq_full.iloc[-1] / START_EQ) ** (1 / yrs) - 1,
        "total_return": eq_full.iloc[-1] / START_EQ - 1,
        "max_dd_%": (eq_full / eq_full.cummax() - 1).min(),
        "max_win_streak": max_run(win_mask),
        "max_loss_streak": max_run(lose_mask),
        "best_R": r.max(),
        "worst_R": r.min(),
    }, eq_full


def main():
    tr = pd.read_parquet("oos_trades.parquet").sort_values("date").reset_index(drop=True)
    rth = pd.read_parquet("nq_rth_1m.parquet")

    # per-day 5-min opening-range size -> R in points (stop = 0.25 * OR)
    et = rth.index.tz_convert("America/New_York")
    day = et.tz_localize(None).normalize()
    mins = ((et - et.normalize() - pd.Timedelta(hours=9, minutes=30))
            / pd.Timedelta(minutes=1)).astype(int)
    df = pd.DataFrame({"day": day, "mins": mins,
                       "h": rth["h"].to_numpy(), "l": rth["l"].to_numpy()})
    or5 = df[df["mins"] < 5].groupby("day").agg(orh=("h", "max"), orl=("l", "min"))
    or5["R_pts"] = 0.25 * (or5["orh"] - or5["orl"])

    tr["date"] = pd.to_datetime(tr["date"])
    tr = tr.join(or5["R_pts"], on="date")
    tr = tr.dropna(subset=["R_pts"])
    tr = tr[tr["R_pts"] > 0]

    # ---- apply costs: reduce each trade's realised R by cost/R_pts ----
    cost_pts = 2 * SLIP_TICKS * TICK_PTS + COMMISSION_RT_USD / MNQ_POINTVALUE
    tr["r_net"] = tr["r"] - cost_pts / tr["R_pts"]
    print(f"Cost per round-turn: {cost_pts:.2f} pts "
          f"({SLIP_TICKS} tick/side slippage + ${COMMISSION_RT_USD} comm)")
    print(f"Median R = {tr['R_pts'].median():.1f} pts  ->  "
          f"median cost = {(cost_pts / tr['R_pts'].median()):.3f} R per trade\n")

    # full trading calendar (all RTH days in the OOS span) -> correct daily Sharpe
    all_days = pd.DatetimeIndex(sorted(day.unique()))
    cal = all_days[(all_days >= tr["date"].min()) & (all_days <= tr["date"].max())]
    gr = tr.set_index("date")["r"]
    nr = tr.set_index("date")["r_net"]
    mg, eqg = metric_block(gr, cal)
    mn, eqn = metric_block(nr, cal)
    for d in (mg, mn):
        d.pop("sortino", None)

    print("=== FULL METRICS  (gross  ->  net of costs) ===")
    for k in mg:
        vg, vn = mg[k], mn[k]
        if isinstance(vg, float):
            print(f"  {k:16s}: {vg:>10.3f}  ->  {vn:>10.3f}")
        else:
            print(f"  {k:16s}: {vg:>10}  ->  {vn:>10}")

    # ------------------------- Monte-Carlo -------------------------
    r_net = tr["r_net"].to_numpy()
    rpts = tr["R_pts"].to_numpy()
    n = len(r_net)
    rng = np.random.default_rng(7)
    B = 5000
    mdd_R = np.empty(B)
    streak = np.empty(B, dtype=int)
    term_R = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        s = r_net[idx]
        cum = np.cumsum(s)
        peak = np.maximum.accumulate(cum)
        mdd_R[b] = (cum - peak).min()
        streak[b] = max_run(s <= 0)
        term_R[b] = cum[-1]

    def pct(a, p):
        return np.percentile(a, p)

    print("\n=== MONTE-CARLO (5,000 bootstrap resamples of the OOS trade sequence) ===")
    print(f"  Max drawdown (R):   median {-np.median(mdd_R):.1f} | "
          f"95th pct {-pct(mdd_R,5):.1f} | worst {-mdd_R.min():.1f}")
    print(f"  Longest losing run: median {int(np.median(streak))} | "
          f"95th pct {int(pct(streak,95))} | worst {int(streak.max())}")
    print(f"  Terminal (R):       median {np.median(term_R):.0f} | "
          f"5th pct {pct(term_R,5):.0f} | prob(net loss) {(term_R<0).mean():.1%}")

    # $ drawdown per MNQ contract (resample (r,R_pts) jointly)
    mdd_usd_per_ctr = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, size=n)
        pnl = r_net[idx] * rpts[idx] * MNQ_POINTVALUE
        cum = np.cumsum(pnl)
        peak = np.maximum.accumulate(cum)
        mdd_usd_per_ctr[b] = (cum - peak).min()
    mdd95 = -pct(mdd_usd_per_ctr, 5)
    print(f"\n  Max $ drawdown per 1 MNQ contract: median ${-np.median(mdd_usd_per_ctr):.0f} | "
          f"95th pct ${mdd95:.0f}")

    print("\n=== Prob. of breaching prop trailing DD (95th-pct MC drawdown basis) ===")
    prop_rows = []
    for firm, (dd, tgt) in PROP.items():
        max_ctr = int(dd / mdd95) if mdd95 > 0 else 0
        breach = (-mdd_usd_per_ctr * max(max_ctr, 1) > dd).mean()
        prop_rows.append((firm, dd, max_ctr, breach))
        print(f"  {firm:14s} DD ${dd:<5} -> max {max_ctr} MNQ @ <5% breach "
              f"(breach prob at that size: {breach:.1%})")

    # ------------------------- widgets -------------------------
    # 1) metrics table (gross vs net)
    rows = "".join(
        f"<tr><td style='padding:3px 10px'>{k}</td>"
        f"<td style='text-align:right;padding:3px 10px'>{(f'{mg[k]:.3f}' if isinstance(mg[k],float) else mg[k])}</td>"
        f"<td style='text-align:right;padding:3px 10px;color:#22c55e'>{(f'{mn[k]:.3f}' if isinstance(mn[k],float) else mn[k])}</td></tr>"
        for k in mg)
    table_html = f"""
<div style="font-family:monospace;font-size:13px;color:var(--color-text-primary)">
<table style="border-collapse:collapse;width:100%">
<thead><tr style="border-bottom:1px solid #64748b">
<th style="text-align:left;padding:4px 10px">Metric</th>
<th style="text-align:right;padding:4px 10px">Gross</th>
<th style="text-align:right;padding:4px 10px">Net of costs</th></tr></thead>
<tbody>{rows}</tbody></table></div>"""
    save_widget(table_html, "metrics_table")

    # 2) Monte-Carlo equity fan (200 sample paths + net historical)
    paths = []
    for _ in range(200):
        idx = rng.integers(0, n, size=n)
        paths.append(np.cumsum(r_net[idx]).tolist())
    hist_path = np.cumsum(r_net).tolist()
    fan_payload = json.dumps({"paths": [[round(v, 1) for v in p] for p in paths],
                              "hist": [round(v, 1) for v in hist_path]})
    fan_html = f"""
<div style="position:relative;width:100%"><canvas id="fan"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d={fan_payload};
const ds=d.paths.map(p=>({{data:p,borderColor:'rgba(59,130,246,0.10)',borderWidth:1,pointRadius:0,fill:false}}));
ds.push({{label:'Actual OOS path',data:d.hist,borderColor:'#22c55e',borderWidth:2.5,pointRadius:0,fill:false}});
new Chart(document.getElementById('fan'),{{type:'line',
  data:{{labels:d.hist.map((_,i)=>i),datasets:ds}},
  options:{{responsive:true,aspectRatio:1.9,animation:false,
    plugins:{{legend:{{display:false}},title:{{display:true,
      text:'Monte-Carlo: 200 reshuffled equity paths (cumulative R) vs actual',
      color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{title:{{display:true,text:'cumulative R',color:'#94a3b8'}},ticks:{{color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8',maxTicksLimit:10}},title:{{display:true,text:'trade #',color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(fan_html, "montecarlo_fan")

    # 3) distribution of max drawdown (R) and losing streak
    def hist(arr, nb):
        lo, hi = float(np.min(arr)), float(np.max(arr))
        w = (hi - lo) / nb if hi > lo else 1
        c = [0] * nb
        labs = [round(lo + k * w, 1) for k in range(nb)]
        for v in arr:
            b = min(nb - 1, int((v - lo) / w)) if w else 0
            c[b] += 1
        return labs, c
    ddlab, ddc = hist(-mdd_R, 30)
    slab, sc = hist(streak.astype(float), int(streak.max() - streak.min()) + 1)
    dd_payload = json.dumps({"ddlab": ddlab, "ddc": ddc,
                             "slab": [int(x) for x in slab], "sc": sc})
    dist_html = f"""
<div style="position:relative;width:100%"><canvas id="ddh"></canvas></div>
<div style="position:relative;width:100%;margin-top:14px"><canvas id="stk"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d={dd_payload};
new Chart(document.getElementById('ddh'),{{type:'bar',
  data:{{labels:d.ddlab,datasets:[{{data:d.ddc,backgroundColor:'#ef4444'}}]}},
  options:{{responsive:true,aspectRatio:2.4,plugins:{{legend:{{display:false}},
    title:{{display:true,text:'MC distribution of MAX DRAWDOWN (in R)',
      color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}}}},x:{{ticks:{{color:'#94a3b8',maxTicksLimit:12}}}}}}}}
}});
new Chart(document.getElementById('stk'),{{type:'bar',
  data:{{labels:d.slab,datasets:[{{data:d.sc,backgroundColor:'#f59e0b'}}]}},
  options:{{responsive:true,aspectRatio:2.4,plugins:{{legend:{{display:false}},
    title:{{display:true,text:'MC distribution of LONGEST LOSING STREAK (consecutive losses)',
      color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}}}},x:{{ticks:{{color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(dist_html, "montecarlo_distributions")


if __name__ == "__main__":
    main()