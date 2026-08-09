"""
Combined ORB + Retest strategy backtest on Nasdaq-100 futures (NQ).

Paper 1 (Zarattini & Aziz 2023): 5-min Opening Range Breakout, direction of the
break, stop at opposite extreme, target = R-multiple or end-of-day, 1% risk.
Paper 2 (Pineda 2026): after the breakout, wait for a *fast* retest of the broken
level (<= RETEST_MAX_MIN) -> high continuation probability.

Combined rules (kept deliberately simple):
  - Opening Range = first OR_MIN minutes of RTH (09:30 ET).
  - Breakout      = first bar breaking OR high (long) or OR low (short).
  - Entry         = retest of the broken level, only if it happens fast and only
                    after a minimum favourable excursion (Paper 2 "valid retest").
  - Stop          = opposite OR boundary (= 1R = OR size).
  - Exit          = TARGET_R * R  OR  end-of-day close, whichever first.
  - Sizing        = risk RISK_PCT of equity per trade (1R = RISK_PCT).
"""
import time
import numpy as np
import pandas as pd
import quantpad_data as qpd

# ----------------------------- parameters ---------------------------------
SYMBOL        = "NQ.FUT"
START         = "2019-01-01"
END           = "2025-01-01"
OR_MIN        = 5       # opening-range length in minutes
EXCURSION_PCT = 0.20    # min favourable excursion (% of level) before a retest counts
TOL_PCT       = 0.05    # retest touch tolerance (% of level)
RETEST_MAX_MIN = 20     # fast-retest filter: skip if retest slower than this
TARGET_R      = 3.0     # profit target in R; None -> end-of-day exit only
STOP_MODE     = "tight" # "tight" -> stop STOP_FRAC*OR beyond the level; "opposite" -> other OR boundary
STOP_FRAC     = 0.25    # tight-stop distance as a fraction of the opening-range size
RISK_PCT      = 0.01    # risk per trade (1R)
START_EQ      = 25_000
RTH_START     = "09:30"
RTH_END       = "16:00"

one_day = 86_400_000


def to_ms(date_str):
    return int(pd.Timestamp(date_str, tz="UTC").timestamp() * 1000)


def fetch_1m(sym, start_ms, end_ms):
    chunks, cur, step = [], start_ms, 180 * one_day
    while cur < end_ms:
        nxt = min(cur + step, end_ms)
        d = qpd.get_bars_with_retry(sym, "1m", cur, nxt, roll_adjust="none",
                                    retries=4, sleep_seconds=8)
        if len(d):
            chunks.append(d)
        cur = nxt
    df = pd.concat(chunks)
    df = df[~df.index.duplicated()].sort_index()
    return df


def simulate_day(tmin, o, h, lw, c, params, diag=None):
    """Return (r_multiple, direction, mins_to_retest, exit_kind) or None.

    tmin: minutes from 09:30 (int array), arrays aligned & sorted.
    If diag is a dict, also record the *unfiltered* first-retest outcome for the
    Paper-2 validation (continuation/failure) regardless of the fast filter.
    """
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

    # --- first breakout ---
    i0 = None
    direction = 0
    for i in post:
        up = h[i] > orh
        dn = lw[i] < orl
        if up and dn:
            return None            # ambiguous outside bar -> skip
        if up:
            i0, direction = i, 1
            break
        if dn:
            i0, direction = i, -1
            break
    if i0 is None:
        return None

    level = orh if direction == 1 else orl
    stop_mode = params.get("STOP_MODE", "opposite")
    stop_frac = params.get("STOP_FRAC", 0.5)
    or_size = orh - orl
    if stop_mode == "opposite":
        stop = orl if direction == 1 else orh
    else:  # "tight": stop a fraction of the OR beyond the broken level
        stop = level - stop_frac * or_size if direction == 1 else level + stop_frac * or_size
    R = level - stop if direction == 1 else stop - level
    if R <= 0:
        return None
    t0 = tmin[i0]

    # --- require min favourable excursion, then a retest of the level ---
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
            if exc_done and j > exc_bar and lw[j] <= level * (1 + tol):
                retest_bar = j
                break
        else:
            fav = (level - lw[j]) / level
            if fav > mfe_pre:
                mfe_pre = fav
            if not exc_done and fav >= exc:
                exc_done, exc_bar = True, j
            if exc_done and j > exc_bar and h[j] >= level * (1 - tol):
                retest_bar = j
                break
    if retest_bar is None:
        return None

    mins_to_retest = int(tmin[retest_bar] - t0)

    # --- Paper-2 diagnostic: unfiltered outcome classification ---
    if diag is not None:
        _classify_outcome(tmin, h, lw, c, retest_bar, direction, level, orh, orl,
                          mfe_pre, mins_to_retest, diag)

    # --- fast-retest filter ---
    if mins_to_retest > tmax:
        return None

    entry = level
    target = None
    if target_r is not None:
        target = entry + target_r * R if direction == 1 else entry - target_r * R

    exit_price = c[-1]
    exit_kind = "eod"
    for j in range(retest_bar + 1, tmin.size):
        if direction == 1:
            if lw[j] <= stop:
                exit_price, exit_kind = stop, "stop"
                break
            if target is not None and h[j] >= target:
                exit_price, exit_kind = target, "target"
                break
        else:
            if h[j] >= stop:
                exit_price, exit_kind = stop, "stop"
                break
            if target is not None and lw[j] <= target:
                exit_price, exit_kind = target, "target"
                break

    r_mult = (exit_price - entry) / R if direction == 1 else (entry - exit_price) / R
    return r_mult, direction, mins_to_retest, exit_kind


def _classify_outcome(tmin, h, lw, c, retest_bar, direction, level, orh, orl,
                      mfe_pre, mins_to_retest, diag):
    """Paper-2 outcome within 60 min of the retest: continuation / failure / neutral."""
    t_r = tmin[retest_bar]
    mfe_level = level * (1 + mfe_pre) if direction == 1 else level * (1 - mfe_pre)
    fail_level = orl if direction == 1 else orh
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
    et_naive = df_et.index.tz_localize(None)          # ET wall-clock, tz-naive
    day_norm = et_naive.normalize()
    tmin_all = ((et_naive - day_norm
                 - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1))
    o = df_et["o"].to_numpy()
    h = df_et["h"].to_numpy()
    lw = df_et["l"].to_numpy()
    c = df_et["c"].to_numpy()
    tmin_all = tmin_all.to_numpy().astype(int)
    day_key = (et_naive.year * 10000 + et_naive.month * 100
               + et_naive.day).to_numpy()

    diag = {"rows": []} if collect_diag else None
    trades = []
    uniq, starts = np.unique(day_key, return_index=True)
    starts = list(starts) + [len(day_key)]
    for k in range(len(uniq)):
        s, e = starts[k], starts[k + 1]
        res = simulate_day(tmin_all[s:e], o[s:e], h[s:e], lw[s:e], c[s:e],
                           params, diag=diag)
        if res is not None:
            r_mult, direction, mtr, exit_kind = res
            trades.append({"date": day_norm[s],
                           "r": r_mult, "dir": direction,
                           "mins_to_retest": mtr, "exit": exit_kind})
    return pd.DataFrame(trades), diag


def metrics(trades, bench_daily, risk_pct, start_eq):
    tr = trades.set_index("date").sort_index()
    daily_r = tr["r"]
    eq = (1 + risk_pct * daily_r).cumprod() * start_eq
    # align to full benchmark calendar, forward fill equity
    cal = bench_daily.index
    eq_full = pd.Series(start_eq, index=cal, dtype=float)
    eq_on = eq.reindex(cal, method=None)
    eq_full = eq_on.ffill().fillna(start_eq)
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
        "trades": len(tr),
        "years": n_years,
        "total_return": total_ret,
        "cagr": cagr,
        "sharpe": sharpe,
        "max_dd": dd,
        "win_rate": (daily_r > 0).mean(),
        "avg_r": daily_r.mean(),
        "expectancy_r": daily_r.mean(),
        "profit_factor": pf,
        "pct_long": (tr["dir"] == 1).mean(),
        "final_eq": eq_full.iloc[-1],
    }, eq_full


def load_symbol(sym):
    s_ms, e_ms = to_ms(START), to_ms(END)
    raw = fetch_1m(sym, s_ms, e_ms)
    rth = raw.tz_convert("America/New_York").between_time(RTH_START, "15:59")
    bench = qpd.get_bars_with_retry(sym, "1d", s_ms, e_ms, roll_adjust="ratio")
    bench = bench[~bench.index.duplicated()].sort_index()
    bench.index = (bench.index.tz_convert("America/New_York")
                   .tz_localize(None).normalize())
    bench = bench[~bench.index.duplicated()]
    return rth, bench


def main():
    params = dict(OR_MIN=OR_MIN, EXCURSION_PCT=EXCURSION_PCT, TOL_PCT=TOL_PCT,
                  RETEST_MAX_MIN=RETEST_MAX_MIN, TARGET_R=TARGET_R,
                  STOP_MODE=STOP_MODE, STOP_FRAC=STOP_FRAC)
    print(f"Fetching 1m {SYMBOL} {START}..{END} ...")
    t0 = time.time()
    rth, bench = load_symbol(SYMBOL)
    print(f"  RTH bars: {len(rth):,} in {time.time()-t0:.0f}s")
    bench_eq = bench["c"] / bench["c"].iloc[0] * START_EQ

    trades, diag = run_backtest(rth, params, collect_diag=True)
    print(f"\nTrades taken: {len(trades)}")
    m, eq = metrics(trades, bench, RISK_PCT, START_EQ)
    print("\n=== Combined ORB + Fast-Retest strategy (NQ) ===")
    for k, v in m.items():
        if isinstance(v, float):
            print(f"  {k:14s}: {v:,.4f}")
        else:
            print(f"  {k:14s}: {v}")

    bench_ret = bench_eq.iloc[-1] / START_EQ - 1
    print(f"\n  Buy&Hold NQ total return: {bench_ret:.2%}")

    # --- yearly breakdown (strategy R-return vs buy&hold) ---
    ty = trades.copy()
    ty["year"] = ty["date"].dt.year
    yearly = ty.groupby("year")["r"].agg(["count", "sum", "mean"])
    yearly["strat_ret%"] = ty.groupby("year")["r"].apply(
        lambda s: ((1 + RISK_PCT * s).prod() - 1) * 100)
    bh_year = bench["c"].groupby(bench.index.year).apply(
        lambda s: (s.iloc[-1] / s.iloc[0] - 1) * 100)
    yearly["buyhold_ret%"] = bh_year
    print("\n=== Yearly breakdown ===")
    print(yearly.to_string(float_format=lambda x: f"{x:.2f}"))

    # --- ES robustness check (different instrument, same rules) ---
    print("\nFetching ES for robustness check ...")
    es_rth, es_bench = load_symbol("ES.FUT")
    es_trades, _ = run_backtest(es_rth, params, collect_diag=False)
    es_m, _ = metrics(es_trades, es_bench, RISK_PCT, START_EQ)
    es_bh = es_bench["c"].iloc[-1] / es_bench["c"].iloc[0] - 1
    print("=== Same strategy on ES (out-of-sample instrument) ===")
    print(f"  trades {es_m['trades']} | totRet {es_m['total_return']:.1%} | "
          f"CAGR {es_m['cagr']:.1%} | Sharpe {es_m['sharpe']:.2f} | "
          f"MaxDD {es_m['max_dd']:.1%} | win {es_m['win_rate']:.1%} | "
          f"PF {es_m['profit_factor']:.2f}  || Buy&Hold ES {es_bh:.1%}")

    # --- Paper-2 validation: continuation rate by mins-to-retest ---
    diag_df = pd.DataFrame(diag["rows"], columns=["mtr", "outcome"])
    bins = [0, 10, 20, 30, 45, 60, 10_000]
    labels = ["0-10", "10-20", "20-30", "30-45", "45-60", ">60"]
    diag_df["bucket"] = pd.cut(diag_df["mtr"], bins=bins, labels=labels, right=True)
    val = diag_df.groupby("bucket", observed=True)["outcome"].apply(
        lambda s: pd.Series({"n": len(s),
                             "cont": (s == "cont").mean(),
                             "fail": (s == "fail").mean()})).unstack()
    print("\n=== Paper-2 validation on NQ: continuation rate by mins-to-retest ===")
    print(val.to_string(float_format=lambda x: f"{x:.3f}"))

    # ------------------------- widgets -------------------------
    eq_dates = [d.strftime("%Y-%m-%d") for d in eq.index]
    bench_al = bench_eq.reindex(eq.index).ffill()
    import json
    payload = json.dumps({
        "dates": eq_dates,
        "strat": [round(x, 1) for x in eq.tolist()],
        "bench": [round(x, 1) for x in bench_al.tolist()],
    })
    equity_html = f"""
<div style="position:relative;width:100%">
<canvas id="eqc"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const d = {payload};
const step = Math.ceil(d.dates.length/600);
const idx = d.dates.map((_,i)=>i).filter(i=>i%step===0);
new Chart(document.getElementById('eqc'), {{
  type:'line',
  data:{{labels:idx.map(i=>d.dates[i]),datasets:[
    {{label:'ORB + Fast-Retest (1% risk)',data:idx.map(i=>d.strat[i]),
      borderColor:'#22c55e',borderWidth:2,pointRadius:0,fill:false}},
    {{label:'Buy & Hold NQ',data:idx.map(i=>d.bench[i]),
      borderColor:'#94a3b8',borderWidth:1.5,pointRadius:0,fill:false,borderDash:[5,4]}}
  ]}},
  options:{{responsive:true,aspectRatio:1.9,
    plugins:{{legend:{{labels:{{color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
      title:{{display:true,text:'Equity curve (start $25,000, log scale)',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{type:'logarithmic',ticks:{{color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8',maxTicksLimit:10}}}}}}}}
}});
</script>"""
    save_widget(equity_html, "equity_curve")

    # R-distribution
    rvals = trades["r"].round(2).tolist()
    rpayload = json.dumps(rvals)
    hist_html = f"""
<div style="position:relative;width:100%"><canvas id="rh"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const r = {rpayload};
const lo=-1.5, hi=Math.max(...r), nb=30, w=(hi-lo)/nb;
const counts=new Array(nb).fill(0), labels=[];
for(let k=0;k<nb;k++) labels.push((lo+k*w).toFixed(1));
r.forEach(v=>{{let b=Math.min(nb-1,Math.max(0,Math.floor((v-lo)/w)));counts[b]++;}});
new Chart(document.getElementById('rh'),{{type:'bar',
  data:{{labels:labels,datasets:[{{label:'Trades',data:counts,backgroundColor:'#3b82f6'}}]}},
  options:{{responsive:true,aspectRatio:2.2,
    plugins:{{legend:{{display:false}},title:{{display:true,text:'Distribution of trade outcomes (in R)',
      color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}}}},x:{{ticks:{{color:'#94a3b8',maxTicksLimit:12}}}}}}}}
}});
</script>"""
    save_widget(hist_html, "r_distribution")

    # Paper-2 validation bar chart
    vlab = json.dumps(list(val.index.astype(str)))
    vcont = json.dumps([round(x * 100, 1) for x in val["cont"].tolist()])
    vn = json.dumps([int(x) for x in val["n"].tolist()])
    val_html = f"""
<div style="position:relative;width:100%"><canvas id="vc"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('vc'),{{type:'bar',
  data:{{labels:{vlab},datasets:[{{label:'Continuation rate %',data:{vcont},
    backgroundColor:'#22c55e'}}]}},
  options:{{responsive:true,aspectRatio:2.2,
    plugins:{{legend:{{display:false}},
      title:{{display:true,text:'Paper-2 check on NQ: continuation rate by minutes-to-retest (n per bar: {vn})',
        color:getComputedStyle(document.body).getPropertyValue('--color-text-primary')}}}},
    scales:{{y:{{ticks:{{color:'#94a3b8'}},title:{{display:true,text:'% continuation',color:'#94a3b8'}}}},
      x:{{ticks:{{color:'#94a3b8'}},title:{{display:true,text:'minutes from breakout to retest',color:'#94a3b8'}}}}}}}}
}});
</script>"""
    save_widget(val_html, "paper2_validation")


if __name__ == "__main__":
    main()
