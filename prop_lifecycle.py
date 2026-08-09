"""
Prop-firm lifecycle Monte-Carlo for the ORB Fast-Retest strategy on MNQ.

Simulates the full path a prop trader walks:
  1. EVALUATION: start at balance B, reach +profit_target before the trailing
     drawdown (locks at the starting balance) is breached.
  2. FUNDED: fresh account at B, trade for a 12-month horizon, taking payouts
     whenever profit clears one full trailing buffer (conservative: we keep a
     full drawdown buffer as cushion so we never withdraw ourselves into a bust).

Trades are bootstrap-resampled (r_net, R_points) pairs from the walk-forward
out-of-sample sequence, so drawdowns/streaks match the real strategy.

RULES ARE REPRESENTATIVE (Apex-style, EoD trailing that locks at start).
Prop-firm terms change frequently -- verify the exact numbers before committing.
"""
import numpy as np
import pandas as pd
import json

PV = 2.0            # MNQ point value ($ per point)
TICK = 0.25
SLIP_TICKS = 1.0
COMM_RT_USD = 0.74
STOP_FRAC = 0.25
N_MC = 4000
FUNDED_HORIZON = 64     # trade-days ~ 1 year of this strategy (~64 trades/yr)
MAX_EVAL_DAYS = 80      # give up an eval attempt after this many trade-days


def load_pairs():
    tr = pd.read_parquet("oos_trades.parquet")
    rth = pd.read_parquet("nq_rth_1m.parquet")
    idx = rth.index.tz_convert("America/New_York") if rth.index.tz is not None else rth.index
    dt = idx.tz_localize(None)
    date = dt.normalize()
    tmin = ((dt - date) - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)
    or5 = pd.DataFrame({"date": date, "tmin": tmin.values,
                        "h": rth["h"].values, "l": rth["l"].values})
    or5 = or5[(or5["tmin"] >= 0) & (or5["tmin"] < 5)]
    g = or5.groupby("date").agg(hi=("h", "max"), lo=("l", "min"))
    g["R_pts"] = STOP_FRAC * (g["hi"] - g["lo"])
    tr = tr.copy()
    tr["date"] = pd.to_datetime(tr["date"]).dt.normalize()
    tr = tr.merge(g["R_pts"], left_on="date", right_index=True, how="left").dropna(subset=["R_pts"])
    cost_pts = 2 * SLIP_TICKS * TICK + COMM_RT_USD / PV
    tr["r_net"] = tr["r"] - cost_pts / tr["R_pts"]
    return tr["r_net"].to_numpy(), tr["R_pts"].to_numpy()


def sim_eval(rng, r, rp, n, contracts, B, target, dd, min_days):
    bal = B
    peak = B
    days = 0
    while days < MAX_EVAL_DAYS:
        k = rng.integers(n)
        bal += r[k] * rp[k] * PV * contracts
        days += 1
        peak = max(peak, bal)
        floor = min(peak - dd, B)
        if bal <= floor:
            return "bust", days
        if bal >= B + target and days >= min_days:
            return "pass", days
    return "timeout", days


def sim_funded(rng, r, rp, n, contracts, B, dd, payout_min, min_pdays):
    bal = B
    peak = B
    days = 0
    dsl = 0
    payouts = []
    while days < FUNDED_HORIZON:
        k = rng.integers(n)
        bal += r[k] * rp[k] * PV * contracts
        days += 1
        dsl += 1
        peak = max(peak, bal)
        floor = min(peak - dd, B)
        if bal <= floor:
            return payouts, "bust", days
        if bal >= B + dd + payout_min and dsl >= min_pdays:
            payouts.append(bal - (B + dd))   # withdraw, keep full dd buffer
            bal = B + dd
            peak = bal
            dsl = 0
    return payouts, "survived", days


def run_template(name, B, target, dd, fee_mo, r, rp, sizes,
                 min_eval_days=1, payout_min=500, min_pdays=8):
    n = len(r)
    rows = []
    for c in sizes:
        rng = np.random.default_rng(12345 + c)
        passes = 0
        eval_days = []
        funded_busts = 0
        n_payouts = []
        payout_usd = []
        for _ in range(N_MC):
            res, d = sim_eval(rng, r, rp, n, c, B, target, dd, min_eval_days)
            if res != "pass":
                continue
            passes += 1
            eval_days.append(d)
            po, fres, fd = sim_funded(rng, r, rp, n, c, B, dd, payout_min, min_pdays)
            if fres == "bust":
                funded_busts += 1
            n_payouts.append(len(po))
            payout_usd.append(sum(po))
        p_pass = passes / N_MC
        avg_eval_days = np.mean(eval_days) if eval_days else np.nan
        # months to resolve an eval attempt ~ trade-days / (64/12)
        months_per_attempt = (avg_eval_days / (64 / 12)) if eval_days else 3.0
        attempts_to_fund = 1 / p_pass if p_pass > 0 else np.nan
        eval_cost = fee_mo * months_per_attempt * attempts_to_fund if p_pass > 0 else np.nan
        gross_payout_yr = np.mean(payout_usd) if payout_usd else 0.0
        net_yr = gross_payout_yr - eval_cost if p_pass > 0 else -np.inf
        rows.append(dict(size=c, p_pass=p_pass, eval_days=avg_eval_days,
                         funded_bust=(funded_busts / passes) if passes else np.nan,
                         payouts_yr=(np.mean(n_payouts) if n_payouts else 0.0),
                         gross_yr=gross_payout_yr, eval_cost=eval_cost, net_yr=net_yr))
    return pd.DataFrame(rows)


def main():
    r, rp = load_pairs()
    print(f"Loaded {len(r)} OOS trades | median R = {np.median(rp):.1f} pts "
          f"= ${np.median(rp)*PV:.0f}/R per MNQ | net expectancy {r.mean():.3f} R")

    sizes = [1, 2, 3, 4, 5, 6, 8]
    templates = [
        ("Apex 50k", 50000, 3000, 2500, 35),
        ("Apex 100k", 100000, 6000, 3000, 85),
        ("Apex 150k", 150000, 9000, 5000, 85),
    ]
    all_res = {}
    for name, B, target, dd, fee in templates:
        df = run_template(name, B, target, dd, fee, r, rp, sizes)
        all_res[name] = df
        print(f"\n=== {name}  (target ${target}, trailing DD ${dd}, fee ${fee}/mo) ===")
        show = df.copy()
        show["p_pass"] = (show["p_pass"] * 100).round(1)
        show["funded_bust"] = (show["funded_bust"] * 100).round(1)
        show["eval_days"] = show["eval_days"].round(0)
        for col in ["gross_yr", "eval_cost", "net_yr"]:
            show[col] = show[col].round(0)
        print(show.to_string(index=False))
        best = df.loc[df["net_yr"].idxmax()]
        print(f"  -> best size: {int(best['size'])} MNQ | pass {best['p_pass']*100:.0f}% "
              f"| funded-bust {best['funded_bust']*100:.0f}% | "
              f"payouts/yr {best['payouts_yr']:.1f} | net ${best['net_yr']:,.0f}/yr")

    # ---- widget: 50k, net $/yr and bust vs size ----
    df50 = all_res["Apex 50k"]
    payload = json.dumps(dict(
        sizes=[int(x) for x in df50["size"]],
        ppass=[round(x * 100, 1) for x in df50["p_pass"]],
        bust=[round(x * 100, 1) for x in df50["funded_bust"]],
        net=[round(x, 0) for x in df50["net_yr"]],
        pyr=[round(x, 2) for x in df50["payouts_yr"]],
    ))
    html = f"""
<div style="position:relative;width:100%"><canvas id="pc"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d = {payload};
new Chart(document.getElementById('pc'), {{
  data:{{labels:d.sizes.map(s=>s+' MNQ'),datasets:[
    {{type:'bar',label:'Net $/yr',data:d.net,backgroundColor:'#22c55e',yAxisID:'y'}},
    {{type:'line',label:'Pass eval %',data:d.ppass,borderColor:'#3b82f6',yAxisID:'y1',pointRadius:3}},
    {{type:'line',label:'Funded bust %',data:d.bust,borderColor:'#ef4444',yAxisID:'y1',borderDash:[5,4],pointRadius:3}}
  ]}},
  options:{{responsive:true,aspectRatio:1.8,
    plugins:{{legend:{{labels:{{color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
      title:{{display:true,text:'Apex 50k: net $/yr, pass-rate & bust-rate vs contract size',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{position:'left',title:{{display:true,text:'Net $/yr',color:'#94a3b8'}},ticks:{{color:'#94a3b8'}}}},
      y1:{{position:'right',min:0,max:100,title:{{display:true,text:'%',color:'#94a3b8'}},ticks:{{color:'#94a3b8'}},grid:{{drawOnChartArea:false}}}},
      x:{{ticks:{{color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(html, "prop_lifecycle")


if __name__ == "__main__":
    main()
