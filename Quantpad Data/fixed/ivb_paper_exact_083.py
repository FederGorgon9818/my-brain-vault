"""
IVB / "Fabervaale Opening Range Breakout" -- EXACT-SPEC retest against the
Matteo-Conti-PDF ("The Institutional Protocol", 2026), which Max supplied
as screenshots on 11.08.2026.

Why a second test after ivb_test.py (#079): the PDF's EasyLanguage source
differs materially from the Medium-article interpretation we tested:
  - Opening range = 08:30-09:00 NY (PRE-market incl. 8:30 macro prints),
    NOT the 09:30-10:00 RTH range.
  - LONG ONLY, one entry per session.
  - Entry: first 5m bar with Close > ORB_High, bar close time in (09:00, 14:00].
    Filter on the SAME bar: BarDelta (upticks-downticks) >= 200.
  - SL = ORB_Low, TP = entry + 1.0 * (entry - ORB_Low), orders live while long.
  - Flat at 14:00 NY per tested inputs (prose says 15:00 -> both tested).

Their claims (823 trades, 2021-01-05..2026-04-14, 1 NQ):
  WR 58.3%, PF 1.31 gross / 1.28 net, avg trade $201 gross / $183 net,
  net profit $151k after $4.50/ct comm + 1 tick slippage.

Honesty rules (engine standard):
  - 1m full-session data (NQ_full.parquet, tz America/New_York).
  - Signal on CLOSED 5m bar (built from 1m), entry at NEXT 1m open (F1).
  - Same-bar stop+target = STOP (F4). No look-ahead (F5).
  - Costs net = 0.87 NQ pts per round turn (1 tick/side + comm), $20/pt.
  - True bid/ask delta unavailable -> tick-rule proxy sign(c-o)*v per 1m,
    summed over the 5m signal bar. Filters tested:
      none | proxy > 0 | proxy >= q-quantile calibrated to their ~62% day-rate.
  - Windows: THEIR window 2021-01-01..2026-04-16, pre-sample 2016..2020,
    and full 2016..2026-07.
"""
import numpy as np
import pandas as pd

DATA = r"C:/Users/maxlk/Projects/trading-data/engine/cache/NQ_full.parquet"
COST_PTS_RT = 0.87
DPP = 20.0  # $ per NQ point

df = pd.read_parquet(DATA)
et = df.index.tz_localize(None)
df = df.assign(day=et.normalize(), mins=et.hour * 60 + et.minute)

OR_START, OR_END = 8 * 60 + 30, 9 * 60  # [08:30, 09:00)


def run(trade_end_min, delta_mode, delta_thr=None):
    """delta_mode: None | 'pos' | 'thr' (needs delta_thr on proxy scale)"""
    trades = []
    for d, g in df.groupby("day", sort=True):
        m = g["mins"].to_numpy()
        o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))
        orm = (m >= OR_START) & (m < OR_END)
        if orm.sum() < 20:
            continue
        orh, orl = h[orm].max(), lw[orm].min()
        if orh <= orl:
            continue
        # 5m bars: close times 09:05 .. trade_end (bar covers [t-5, t))
        entry_i = None
        for b_close in range(OR_END + 5, trade_end_min + 1, 5):
            bm = (m >= b_close - 5) & (m < b_close)
            if not bm.any():
                continue
            idx = np.where(bm)[0]
            close5 = c[idx[-1]]
            if close5 <= orh:
                continue
            if delta_mode is not None:
                delta = float(np.sum(np.sign(c[idx] - o[idx]) * v[idx]))
                if delta_mode == "pos" and delta <= 0:
                    continue
                if delta_mode == "thr" and delta < delta_thr:
                    continue
            after = np.where(m >= b_close)[0]
            if after.size == 0:
                break
            entry_i = after[0]
            break
        if entry_i is None:
            continue
        entry = o[entry_i]
        stop = orl
        R = entry - stop
        if R <= 0:
            continue
        target = entry + R
        exit_price = exit_kind = None
        for j in range(entry_i, len(m)):
            if m[j] >= trade_end_min:
                exit_price, exit_kind = o[j], "eod"
                break
            if lw[j] <= stop:      # F4: stop wins same-bar conflict
                exit_price, exit_kind = stop, "stop"
                break
            if h[j] >= target:
                exit_price, exit_kind = target, "target"
                break
        if exit_price is None:
            exit_price, exit_kind = c[-1], "eod"
        trades.append({"date": d, "entry": entry, "R_pts": R,
                       "pts": exit_price - entry, "exit": exit_kind})
    return pd.DataFrame(trades).set_index("date").sort_index()


def report(tr, label):
    if len(tr) == 0:
        print(f"{label}: 0 trades")
        return
    windows = [("2021-2026/04 (deren Fenster)", "2021-01-01", "2026-04-16"),
               ("2016-2020 (Pre-Sample)", "2016-01-01", "2020-12-31"),
               ("2016-2026 (voll)", "2016-01-01", "2026-12-31")]
    print(f"\n=== {label} ===")
    for wname, a, b in windows:
        t = tr.loc[a:b]
        if len(t) == 0:
            print(f"  {wname}: 0 trades")
            continue
        for kind, pts in (("BRUTTO", t["pts"]),
                          ("NETTO ", t["pts"] - COST_PTS_RT)):
            r = pts / t["R_pts"]
            wins, losses = pts[pts > 0], pts[pts <= 0]
            pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("inf")
            usd = pts * DPP
            print(f"  {wname} {kind} n={len(t):4d} win={100*(pts>0).mean():5.1f}% "
                  f"avgTrade=${usd.mean():+7.2f} avgR={r.mean():+.3f} PF={pf:4.2f} "
                  f"NetP=${usd.sum():+10.0f}")
        ex = t["exit"].value_counts(normalize=True)
        yr = (t["pts"] - COST_PTS_RT).groupby(t.index.year).sum() * DPP
        print("    exits: " + ", ".join(f"{k}={100*p:.0f}%" for k, p in ex.items())
              + " | netto $/Jahr: " + "  ".join(f"{y}:{s:+,.0f}" for y, s in yr.items()))


# calibrate 'thr' so their window trades ~ 823 (62% of days)
base = run(14 * 60, None)
print(f"Basis ohne Filter, flat 14:00 -> Trades in deren Fenster: "
      f"{len(base.loc['2021-01-01':'2026-04-16'])}")

report(base, "A exakt, KEIN Delta-Filter, flat 14:00")
report(run(14 * 60, "pos"), "B exakt, Delta-Proxy > 0, flat 14:00")

# threshold: match ~823 trades in their window via quantile search on proxy
tw = None
for thr in (200, 500, 1000, 2000, 4000):
    t = run(14 * 60, "thr", thr)
    n = len(t.loc["2021-01-01":"2026-04-16"])
    print(f"[Kalibrierung] thr={thr}: n(deren Fenster)={n}")
    if tw is None and n <= 830:
        tw = (thr, t)
if tw is not None:
    report(tw[1], f"C exakt, Delta-Proxy >= {tw[0]} (n~deren 823), flat 14:00")

report(run(15 * 60, "pos"), "D wie B, aber flat 15:00 (Prosa-Variante)")
