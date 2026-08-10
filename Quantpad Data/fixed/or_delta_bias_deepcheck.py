"""
Vertiefungs-Check auf dem besten Grid-Kandidaten aus or_delta_bias_lab.py
(smul=0.75, tmul=None, win=30, LONG delta>0): Jahres-Tabelle, Tail-Konzentration,
Vergleich gegen naiven Long-Kontroll-Check bei GLEICHEM Stop, sowie SHORT-Pendant.
"""
import numpy as np
import pandas as pd

DATA = r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain\Quantpad Data\nq_rth_1m.parquet"
FLAT_MIN = 385
COST_PTS_RT = 0.87
IS_END = pd.Timestamp("2021-12-31")

df = pd.read_parquet(DATA)[["o", "h", "l", "c", "v"]]
et = df.index.tz_localize(None)
day = et.normalize()
tmin = ((et - day - pd.Timedelta(hours=9, minutes=30)) / pd.Timedelta(minutes=1)).astype(int)
df = df.assign(day=day, tmin=tmin.to_numpy())


def build_trades(win_min, smul, tmul, side):
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
        rows.append({"date": d, "dir": tdir, "r": r, "R_pts": R, "exit": exit_kind, "delta": delta})
    tr = pd.DataFrame(rows).set_index("date").sort_index()
    if len(tr):
        tr["r_net"] = tr["r"] - COST_PTS_RT / tr["R_pts"]
    return tr


def yearly(tr, label):
    yy = tr["r_net"].groupby(tr.index.year).agg(["sum", "count", lambda x: 100 * (x > 0).mean()])
    yy.columns = ["sumR", "n", "win_pct"]
    print("\n--- %s ---" % label)
    print(yy.round(2).to_string())
    tot = tr["r_net"].sum()
    print("Summe NetR gesamt: %+.1f  (n=%d)" % (tot, len(tr)))
    return yy, tot


print("=" * 110)
print("Bester Grid-Kandidat: smul=0.75, tmul=None, win=30, LONG delta>0")
print("=" * 110)
cand = build_trades(30, 0.75, None, "long_only_signal")
yy, tot = yearly(cand, "smul=0.75 LONG Jahre")

rc = cand["r_net"]
wins = rc[rc > 0]
top5 = wins.nlargest(5).sum() / wins.sum() * 100
top_trade = rc.max() / tot * 100 if tot > 0 else float("nan")
top_year = yy["sumR"].max() / tot * 100 if tot > 0 else float("nan")
streak = mx = 0
for x in rc:
    streak = streak + 1 if x <= 0 else 0
    mx = max(mx, streak)
print("Top-5-Gewinntrades = %.1f%% der Bruttogewinne | groesster Einzeltrade = %.1f%% des Gesamt-NetR | "
      "staerkstes Jahr = %.1f%% des Gesamt-NetR | maxLoseStreak=%d" % (top5, top_trade, top_year, mx))

print("\n--- Kontrolle: naiver unconditional Long bei GLEICHEM Stop (smul=0.75, kein Target) ---")
naive = build_trades(30, 0.75, None, "naive_long")
yearly(naive, "naive Long smul=0.75")

print("\n" + "=" * 110)
print("SHORT-Pendant: smul=0.75, tmul=None, win=30, SHORT delta<0")
print("=" * 110)
cands = build_trades(30, 0.75, None, "short_only_signal")
yys, tots = yearly(cands, "smul=0.75 SHORT Jahre")
print("\n--- Kontrolle: naiver unconditional Short bei GLEICHEM Stop (smul=0.75, kein Target) ---")
naives = build_trades(30, 0.75, None, "naive_short")
yearly(naives, "naive Short smul=0.75")

print("\nIS(2016-21) vs OOS(2022-25) Split fuer smul=0.75 LONG:")
is_r = cand[cand.index <= IS_END]["r_net"]
oos_r = cand[cand.index > IS_END]["r_net"]
print("IS : n=%d sumR=%+.1f avgR=%+.3f" % (len(is_r), is_r.sum(), is_r.mean()))
print("OOS: n=%d sumR=%+.1f avgR=%+.3f" % (len(oos_r), oos_r.sum(), oos_r.mean()))

print("\nFERTIG.")
