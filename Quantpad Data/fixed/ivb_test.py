"""
IVB ("Initial Value Breakout", Fabio Valentini / Fabervaale) -- honest skeleton test.

Source of the only fully mechanical rule set: Medium article (untrusted, see
Research-Cache). Rules translated to RTH ET:
  - Opening Range = first 30 min of RTH (09:30-10:00 ET), OR-high / OR-low.
  - Signal: first 5-minute bar closing outside the OR (after 10:00 ET).
  - Stop: opposite OR level. Target: 1R (entry-to-stop distance).
  - Flat at 15:00 ET. One trade per day (first signal).
  - Article's delta filter (bar delta >= 200) needs bid/ask data we don't have.
    Proxy here: sign(close-open)*volume summed over the 5m signal bar, must be
    aligned with breakout direction (> 0 for longs, < 0 for shorts).
    This is a CRUTCH, not a replication of real orderflow delta.

Honesty rules (engine standard):
  - Signals on CLOSED 5m bars only; market entry at NEXT 1m bar open (F1).
  - Retest variant: limit at broken OR level, fills ONLY on real touch
    (later 1m low <= level for longs), fill price = level (F2). Window: 30 min
    after signal bar close (assumption -- not specified in source).
  - Same-bar stop+target = STOP (F4). No look-ahead (F5).
  - Gross AND net. Net = 0.87 NQ points per round turn (1 tick/side + comm),
    same cost model as all prior studies.
  - Baseline: 1R target vs 1R stop => random-walk breakeven win rate ~50%
    (EOD exits dilute this slightly; reported anyway).

Variants:
  A  breakout            (no filter)
  B  breakout + delta-proxy filter
  C  retest              (no filter)
  D  retest + delta-proxy filter
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
OR_MIN = 30
FLAT_MIN = 330            # 15:00 ET = minute 330 after 09:30
RETEST_WINDOW = 30        # minutes after signal close (assumption)
COST_PTS_RT = 0.87
RISK_PCT = 0.01
START_EQ = 25_000

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())


def simulate_day(g, variant):
    tm = g["tmin"].to_numpy()
    o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))
    orm = tm < OR_MIN
    if orm.sum() < 15:
        return None
    orh, orl = h[orm].max(), lw[orm].min()
    if orh <= orl:
        return None

    # closed 5m bars from 1m data, aligned to 09:30
    sig_bar = None
    direction = 0
    for b_start in range(OR_MIN, FLAT_MIN, 5):
        m = (tm >= b_start) & (tm < b_start + 5)
        if not m.any():
            continue
        idx = np.where(m)[0]
        close5 = c[idx[-1]]
        if close5 > orh:
            direction = 1
        elif close5 < orl:
            direction = -1
        else:
            continue
        sig_bar = (b_start, idx)
        break
    if sig_bar is None:
        return None
    b_start, sig_idx = sig_bar

    if variant in ("B", "D"):
        delta = np.sum(np.sign(c[sig_idx] - o[sig_idx]) * v[sig_idx])
        if direction * delta <= 0:
            return None

    level = orh if direction == 1 else orl
    stop = orl if direction == 1 else orh
    after = np.where(tm >= b_start + 5)[0]
    if after.size == 0:
        return None

    if variant in ("A", "B"):
        entry_i = after[0]
        entry = o[entry_i]
    else:  # retest: limit at level, real touch only (F2)
        entry_i = None
        sig_close_t = b_start + 5
        for j in after:
            if tm[j] >= FLAT_MIN or tm[j] - sig_close_t > RETEST_WINDOW:
                break
            touched = lw[j] <= level if direction == 1 else h[j] >= level
            if touched:
                entry_i = j
                break
        if entry_i is None:
            return None
        entry = level

    R = (entry - stop) if direction == 1 else (stop - entry)
    if R <= 0:
        return None
    target = entry + R if direction == 1 else entry - R

    exit_price, exit_kind = None, None
    start_j = entry_i if variant in ("C", "D") else entry_i  # entry bar can hit stop/target
    for j in range(start_j, len(tm)):
        if tm[j] >= FLAT_MIN:
            exit_price, exit_kind = o[j], "eod"
            break
        hit_stop = lw[j] <= stop if direction == 1 else h[j] >= stop
        hit_tgt = h[j] >= target if direction == 1 else lw[j] <= target
        if j == entry_i and variant in ("A", "B"):
            # entry bar: entry at open; both hits -> stop (F4)
            pass
        if hit_stop:                      # F4: stop wins same-bar conflicts
            exit_price, exit_kind = stop, "stop"
            break
        if hit_tgt:
            exit_price, exit_kind = target, "target"
            break
    if exit_price is None:
        exit_price, exit_kind = c[-1], "eod"

    r = (exit_price - entry) / R if direction == 1 else (entry - exit_price) / R
    return {"r": r, "dir": direction, "exit": exit_kind, "R_pts": R}


def report(trades, label, cal):
    if len(trades) == 0:
        print(f"{label}: 0 trades")
        return
    tr = pd.DataFrame(trades).set_index("date").sort_index()
    for kind, rcol in (("BRUTTO", tr["r"]), ("NETTO ", tr["r"] - COST_PTS_RT / tr["R_pts"])):
        eq = (1 + RISK_PCT * rcol).cumprod() * START_EQ
        eq_full = eq.reindex(cal).ffill().fillna(START_EQ)
        rets = eq_full.pct_change().fillna(0)
        years = (cal[-1] - cal[0]).days / 365.25
        sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
        dd = (eq_full / eq_full.cummax() - 1).min()
        wins, losses = rcol[rcol > 0], rcol[rcol <= 0]
        pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("inf")
        streak = mx = 0
        for x in rcol:
            streak = streak + 1 if x <= 0 else 0
            mx = max(mx, streak)
        print(f"  {kind} n={len(rcol):4d}  win={100*(rcol>0).mean():5.1f}%  "
              f"avgR={rcol.mean():+.3f}  PF={pf:4.2f}  Sharpe={sharpe:+.2f}  "
              f"TotRet={100*(eq_full.iloc[-1]/START_EQ-1):+7.1f}%  MaxDD={100*dd:5.1f}%  "
              f"maxLoseStreak={mx}")
    ex = tr["exit"].value_counts(normalize=True)
    net_r = tr["r"] - COST_PTS_RT / tr["R_pts"]
    yearly = net_r.groupby(tr.index.year).agg(["sum", "count"])
    ys = "  ".join(f"{y}:{s:+.1f}R/{int(n)}" for y, (s, n) in yearly.iterrows())
    print(f"  exits: " + ", ".join(f"{k}={100*p:.0f}%" for k, p in ex.items())
          + f"  |  long={100*(tr['dir']==1).mean():.0f}%  medR_pts={tr['R_pts'].median():.1f}")
    print(f"  netto R/Jahr: {ys}")


cal = pd.DatetimeIndex(sorted(df["day"].unique()))
groups = list(df.groupby("day", sort=True))
NAMES = {"A": "A breakout pur", "B": "B breakout+delta-proxy",
         "C": "C retest (echter Touch)", "D": "D retest+delta-proxy"}
print(f"IVB-Skelett NQ 1m RTH {cal[0].date()} .. {cal[-1].date()}  "
      f"(OR=30min, Stop=Gegenseite, Target=1R, flat 15:00 ET, Baseline-Win ~50%)")
for variant in ("A", "B", "C", "D"):
    trades = []
    for d, g in groups:
        res = simulate_day(g, variant)
        if res is not None:
            res["date"] = d
            trades.append(res)
    print(f"\n{NAMES[variant]}")
    report(trades, NAMES[variant], cal)
