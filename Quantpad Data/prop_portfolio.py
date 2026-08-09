"""
Portfolio simulation of running MULTIPLE prop accounts on the combined ORB+Retest
strategy.  Key realism: if every account trades the SAME instrument (NQ) with the
SAME automated signals, their daily P&L is PERFECTLY CORRELATED -> accounts bust
together.  Running N identical accounts is leverage, not diversification.

We contrast two worlds:
  (A) CORRELATED  : all accounts share the same daily R each day (same NQ signal).
  (B) INDEPENDENT : each account draws its own R (proxy for spreading the same
                    rules across 4 uncorrelated instruments NQ/ES/YM/RTY).

A bust only costs the eval subscription/reset fee (not real capital), so we also
let busted accounts auto-restart and we optimise contract size for portfolio net $.
"""
import numpy as np
import pandas as pd

PV = 2.0                     # MNQ $ per point
STOP_FRAC = 0.25
TRADES_PER_YEAR = 64
TRADES_PER_MONTH = TRADES_PER_YEAR / 12.0

# Apex-style 50k template (representative -- verify current terms)
TMPL = dict(B=50_000, target=3_000, dd=2_500, payout_min=500,
            min_eval_days=1, min_payout_days=8, fee_mo=35.0)


def load_pairs():
    tr = pd.read_parquet("oos_trades.parquet")
    rth = pd.read_parquet("nq_rth_1m.parquet")
    et = rth.index.tz_convert("America/New_York")
    d = et.tz_localize(None).normalize()
    tmin = ((et - et.normalize() - pd.Timedelta(hours=9, minutes=30))
            / pd.Timedelta(minutes=1)).astype(int)
    df = pd.DataFrame({"date": d, "tmin": tmin,
                       "h": rth["h"].to_numpy(), "l": rth["l"].to_numpy()})
    or5 = df[df["tmin"] < 5].groupby("date").agg(h=("h", "max"), l=("l", "min"))
    or5["Rpts"] = STOP_FRAC * (or5["h"] - or5["l"])
    tr["date"] = pd.to_datetime(tr["date"]).dt.normalize()
    tr = tr.join(or5["Rpts"], on="date").dropna(subset=["Rpts"])
    # net-of-cost R (1 tick/side slippage + $0.74 comm on MNQ)
    cost_pts = 2 * 1.0 * 0.25 + 0.74 / PV
    tr["r_net"] = tr["r"] - cost_pts / tr["Rpts"]
    return tr[["r_net", "Rpts"]].to_numpy()


def new_acct(tmpl):
    return {"phase": "eval", "bal": tmpl["B"], "peak": tmpl["B"],
            "floor": tmpl["B"] - tmpl["dd"], "days": 0, "dsl": 0}


def step_acct(a, pnl, tmpl):
    """Advance one account by one trade-day. Returns ('payout', amt) / ('bust', 0) / (None,0)."""
    B, dd = tmpl["B"], tmpl["dd"]
    a["bal"] += pnl
    a["days"] += 1
    a["dsl"] += 1
    a["peak"] = max(a["peak"], a["bal"])
    a["floor"] = min(a["peak"] - dd, B)          # trailing, locks at start balance
    if a["bal"] <= a["floor"]:
        return ("bust", 0.0)
    if a["phase"] == "eval":
        if a["bal"] >= B + tmpl["target"] and a["days"] >= tmpl["min_eval_days"]:
            a["phase"] = "funded"
            a["bal"] = B
            a["peak"] = B
            a["floor"] = B - dd
            a["days"] = 0
            a["dsl"] = 0
    else:
        if a["bal"] >= B + dd + tmpl["payout_min"] and a["dsl"] >= tmpl["min_payout_days"]:
            amt = a["bal"] - (B + dd)
            a["bal"] = B + dd
            a["peak"] = a["bal"]
            a["floor"] = B
            a["dsl"] = 0
            return ("payout", amt)
    return (None, 0.0)


def run_portfolio(rng, pairs, size, n_acc, horizon, tmpl, gap, correlated):
    n = len(pairs)
    accts = []
    onboarded = 0
    next_on = 0
    tot_pay = 0.0
    tot_fee = 0.0
    payouts = 0
    busts = 0
    fee_day = tmpl["fee_mo"] / TRADES_PER_MONTH
    max_simul_bust = 0
    for d in range(horizon):
        if onboarded < n_acc and d >= next_on:
            accts.append(new_acct(tmpl))
            onboarded += 1
            next_on = d + gap
        shared = pairs[rng.integers(n)]
        day_bust = 0
        for a in accts:
            pair = shared if correlated else pairs[rng.integers(n)]
            pnl = pair[0] * pair[1] * PV * size
            if a["phase"] == "eval":
                tot_fee += fee_day
            res, amt = step_acct(a, pnl, tmpl)
            if res == "payout":
                tot_pay += amt
                payouts += 1
            elif res == "bust":
                busts += 1
                day_bust += 1
                accts[accts.index(a)] = new_acct(tmpl)   # auto-restart eval
        max_simul_bust = max(max_simul_bust, day_bust)
    years = horizon / TRADES_PER_YEAR
    return dict(net=(tot_pay - tot_fee) / years, pay=tot_pay / years,
                fee=tot_fee / years, payouts=payouts / years,
                busts=busts / years, max_simul_bust=max_simul_bust)


def summarize(rng, pairs, size, n_acc, horizon, tmpl, gap, correlated, mc=1500):
    nets, payouts, busts, msb = [], [], [], []
    for _ in range(mc):
        r = run_portfolio(rng, pairs, size, n_acc, horizon, tmpl, gap, correlated)
        nets.append(r["net"])
        payouts.append(r["payouts"])
        busts.append(r["busts"])
        msb.append(r["max_simul_bust"])
    nets = np.array(nets)
    return dict(net_med=np.median(nets), net_p5=np.percentile(nets, 5),
                net_p95=np.percentile(nets, 95), p_loss=float((nets < 0).mean()),
                payouts=np.mean(payouts), busts=np.mean(busts),
                max_simul_bust=int(np.max(msb)))


def main():
    pairs = load_pairs()
    print(f"Loaded {len(pairs)} trade pairs | $/R per MNQ = {np.median(pairs[:,1])*PV:.0f}")
    rng = np.random.default_rng(7)
    n_acc = 10
    horizon = 128          # ~2 years of trade-days
    gap = 6                # onboard 1 new account every ~6 trade-days

    print(f"\n=== Portfolio of {n_acc} x Apex-50k, staggered onboarding, per-size sweep ===")
    for corr, tag in [(True, "CORRELATED (all on NQ, same signal)"),
                      (False, "INDEPENDENT (proxy: 4 uncorrelated instruments)")]:
        print(f"\n--- {tag} ---")
        print(f"{'size':>4} {'net$/yr(med)':>12} {'p5':>9} {'p95':>9} "
              f"{'P(loss yr)':>10} {'payouts/yr':>11} {'busts/yr':>9} {'maxSimulBust':>12}")
        for size in [3, 4, 5, 6, 8]:
            s = summarize(rng, pairs, size, n_acc, horizon, TMPL, gap, corr)
            print(f"{size:>4} {s['net_med']:>12,.0f} {s['net_p5']:>9,.0f} "
                  f"{s['net_p95']:>9,.0f} {s['p_loss']:>10.1%} {s['payouts']:>11.1f} "
                  f"{s['busts']:>9.1f} {s['max_simul_bust']:>12}")

    # ---- widget: income distribution for the recommended setup (correlated, 5 MNQ) ----
    import json
    rng2 = np.random.default_rng(11)
    nets_corr = [run_portfolio(rng2, pairs, 5, n_acc, horizon, TMPL, gap, True)["net"]
                 for _ in range(3000)]
    rng3 = np.random.default_rng(11)
    nets_ind = [run_portfolio(rng3, pairs, 5, n_acc, horizon, TMPL, gap, False)["net"]
                for _ in range(3000)]
    payload = json.dumps({"corr": [round(x) for x in nets_corr],
                          "ind": [round(x) for x in nets_ind]})
    html = f"""
<div style="position:relative;width:100%"><canvas id="pf"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d = {payload};
function hist(a, lo, hi, nb){{const w=(hi-lo)/nb, c=new Array(nb).fill(0);
  a.forEach(v=>{{let b=Math.min(nb-1,Math.max(0,Math.floor((v-lo)/w)));c[b]++;}});
  return c.map(x=>x/a.length*100);}}
const lo=-3000, hi=25000, nb=40, w=(hi-lo)/nb;
const labels=[]; for(let k=0;k<nb;k++) labels.push(Math.round(lo+k*w));
new Chart(document.getElementById('pf'),{{type:'bar',
  data:{{labels:labels,datasets:[
    {{label:'Correlated (all NQ)',data:hist(d.corr,lo,hi,nb),backgroundColor:'rgba(239,68,68,0.55)'}},
    {{label:'Independent (4 instruments)',data:hist(d.ind,lo,hi,nb),backgroundColor:'rgba(34,197,94,0.55)'}}
  ]}},
  options:{{responsive:true,aspectRatio:2.0,
    plugins:{{legend:{{labels:{{color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
      title:{{display:true,text:'Annual portfolio net income: 10 x 50k @ 5 MNQ (3,000 MC runs)',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}},title:{{display:true,text:'% of runs',color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8',maxTicksLimit:12}},title:{{display:true,text:'net $ / year',color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(html, "portfolio_income")


if __name__ == "__main__":
    main()