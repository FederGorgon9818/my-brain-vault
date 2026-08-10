"""
OR_DELTA_BIAS_NQ: eigenstaendige Session-Bias-Strategie (Beifang aus der
IVB-Filter-Lab-Runde 10.08.2026, siehe Strategie-Logbuch #077/#078).

Signal: tick-rule delta des Opening-Range-Fensters 09:30-10:00 ET auf NQ.
  or_delta = sum(sign(close-open) * volume) ueber die 1m-Bars im OR-Fenster.
  or_delta > 0 -> Long-Bias Rest des Tages, or_delta < 0 -> Short-Bias.

Anatomie (Kandidat, analog asian.py us_dir-Bauweise):
  Entry:    Open der ersten Bar nach OR-Fensterende (10:00 ET), Richtung = sign(or_delta)
  Stop:     entry -/+ smul * OR_width  (OR_width = OR-High - OR-Low)
  Target:   optional entry +/- tmul * R (R = smul*OR_width), sonst nur Zeit-Exit
  Notausgang: flat 15:55 ET (tmin=385)
  Sizing:   1R Risiko in R-Multiples gemessen

Pruefpunkte:
  (a) Kontroll-Check gegen naiven unconditional Long-Hold
  (b) Stop/Target-Grid smul in 0.25/0.5/0.75/1.0, tmul in None/1/1.5/2
  (c) Jahres-Stabilitaet IS 2016-2021 vs OOS 2022-2025
  (d) Fensterlaenge-Sweep als cum_delta-Gegenrechnung
  (g) Short-Seite separat
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
FLAT_MIN = 385
COST_PTS_RT = 0.87
RISK_PCT, START_EQ = 0.01, 25000
IS_END = pd.Timestamp("2021-12-31")

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())

cal = pd.DatetimeIndex(sorted(df["day"].unique()))
is_cal, oos_cal = cal[cal <= IS_END], cal[cal > IS_END]


def build_trades(win_min, smul, tmul, side="both"):
    rows = []
    for d, g in df.groupby("day", sort=True):
        tm = g["tmin"].to_numpy()
        o, h, lw, c, v = (g[k].to_numpy() for k in ("o", "h", "l", "c", "v"))
        wm = tm < win_min
        if wm.sum() < max(3, win_min // 3):
            continue
        wh, wl = h[wm].max(), lw[wm].min()
        ww = wh - wl
        if ww <= 0:
            continue
        w_idx = np.where(wm)[0]
        delta = np.sum(np.sign(c[w_idx] - o[w_idx]) * v[w_idx])

        if side == "naive_long":
            tdir = 1
        elif side == "naive_short":
            tdir = -1
        elif side == "long_only_signal":
            if delta <= 0:
                continue
            tdir = 1
        elif side == "short_only_signal":
            if delta >= 0:
                continue
            tdir = -1
        else:
            if delta == 0:
                continue
            tdir = 1 if delta > 0 else -1

        after = np.where(tm >= win_min)[0]
        if after.size == 0:
            continue
        ei = after[0]
        entry = o[ei]
        R = smul * ww
        if R <= 0:
            continue
        stop = entry - tdir * R
        target = entry + tdir * tmul * R if tmul else None
        exit_price, exit_kind = c[-1], "eod"
        for j in range(ei, len(tm)):
            if tm[j] >= FLAT_MIN:
                exit_price, exit_kind = o[j], "time"
                break
            hit_stop = lw[j] <= stop if tdir == 1 else h[j] >= stop
            hit_tgt = (h[j] >= target if tdir == 1 else lw[j] <= target) if target is not None else False
            if hit_stop:
                exit_price, exit_kind = stop, "stop"
                break
            if hit_tgt:
                exit_price, exit_kind = target, "target"
                break
        r = (exit_price - entry) * tdir / R
        rows.append({"date": d, "dir": tdir, "r": r, "R_pts": R, "exit": exit_kind,
                     "delta": delta, "win_min": win_min})
    tr = pd.DataFrame(rows).set_index("date").sort_index()
    if len(tr):
        tr["r_net"] = tr["r"] - COST_PTS_RT / tr["R_pts"]
    return tr


def stats(tr, cal_seg):
    if tr is None or len(tr) < 30:
        return None
    rc = tr["r_net"]
    eq = (1 + RISK_PCT * rc).cumprod() * START_EQ
    eq_full = eq.reindex(cal_seg).ffill().fillna(START_EQ)
    rets = eq_full.pct_change().fillna(0)
    sharpe = rets.mean() / rets.std() * np.sqrt(252) if rets.std() > 0 else 0
    wins, losses = rc[rc > 0], rc[rc <= 0]
    pf = wins.sum() / abs(losses.sum()) if losses.sum() != 0 else float("inf")
    dd = 100 * (eq_full / eq_full.cummax() - 1).min()
    yearly = rc.groupby(rc.index.year).sum()
    return {"n": len(rc), "win": 100 * (rc > 0).mean(), "avgR": rc.mean(),
            "pf": pf, "sharpe": sharpe, "dd": dd,
            "tot": 100 * (eq_full.iloc[-1] / START_EQ - 1), "posyrs": str((yearly > 0).sum()) + "/" + str(len(yearly))}


def fmt(s):
    if s is None:
        return "n<30".ljust(66)
    return ("n=%4d win=%4.1f%% avgR=%+.3f PF=%4.2f Sh=%+5.2f DD=%5.1f%% tot=%+7.1f%% posJ=%s" %
            (s["n"], s["win"], s["avgR"], s["pf"], s["sharpe"], s["dd"], s["tot"], s["posyrs"]))


def report(tr, label):
    s_is = stats(tr[tr.index <= IS_END] if len(tr) else tr, is_cal)
    s_oos = stats(tr[tr.index > IS_END] if len(tr) else tr, oos_cal)
    print("%-42s | IS %-66s | OOS %s" % (label, fmt(s_is), fmt(s_oos)))
    return s_is, s_oos


print("=" * 130)
print("(a) KONTROLL-CHECK: or_delta-Signal vs naiver unconditional Hold (win=30, smul=0.5, kein Target)")
print("=" * 130)
for side, label in (("long_only_signal", "delta>0 -> LONG (Signal)"),
                     ("naive_long", "IMMER long (Kontrolle)"),
                     ("short_only_signal", "delta<0 -> SHORT (Signal)"),
                     ("naive_short", "IMMER short (Kontrolle)"),
                     ("both", "sign(delta) beide Richtungen")):
    tr = build_trades(30, 0.5, None, side=side)
    report(tr, label)

print()
print("=" * 130)
print("(b) STOP/TARGET-GRID LONG (win=30, delta>0->long)")
print("=" * 130)
for smul in (0.25, 0.5, 0.75, 1.0):
    for tmul in (None, 1, 1.5, 2):
        tr = build_trades(30, smul, tmul, side="long_only_signal")
        report(tr, "smul=%s tmul=%s" % (smul, tmul))

print()
print("=" * 130)
print("(b2) STOP/TARGET-GRID SHORT (win=30, delta<0->short)")
print("=" * 130)
for smul in (0.25, 0.5, 0.75, 1.0):
    for tmul in (None, 1, 1.5, 2):
        tr = build_trades(30, smul, tmul, side="short_only_signal")
        report(tr, "smul=%s tmul=%s" % (smul, tmul))

print()
print("=" * 130)
print("(c) JAHRES-STABILITAET (smul=0.5, tmul=None, LONG delta>0)")
print("=" * 130)
tr = build_trades(30, 0.5, None, side="long_only_signal")
yearly = tr["r_net"].groupby(tr.index.year).agg(["sum", "count", lambda x: 100 * (x > 0).mean()])
yearly.columns = ["sumR", "n", "win_pct"]
print(yearly.round(2).to_string())

print()
print("=" * 130)
print("(c2) JAHRES-STABILITAET SHORT (smul=0.5, tmul=None, delta<0)")
print("=" * 130)
trs = build_trades(30, 0.5, None, side="short_only_signal")
yearlys = trs["r_net"].groupby(trs.index.year).agg(["sum", "count", lambda x: 100 * (x > 0).mean()])
yearlys.columns = ["sumR", "n", "win_pct"]
print(yearlys.round(2).to_string())

print()
print("=" * 130)
print("(d) FENSTERLAENGE-SWEEP (cum_delta-Gegenrechnung): Entry am Fensterende, smul=0.5, kein Target")
print("=" * 130)
for w in (15, 30, 45, 60, 90, 120):
    tr = build_trades(w, 0.5, None, side="long_only_signal")
    report(tr, "win=%dmin LONG (delta>0)" % w)
for w in (15, 30, 45, 60, 90, 120):
    tr = build_trades(w, 0.5, None, side="short_only_signal")
    report(tr, "win=%dmin SHORT (delta<0)" % w)

print("\nFERTIG.")
