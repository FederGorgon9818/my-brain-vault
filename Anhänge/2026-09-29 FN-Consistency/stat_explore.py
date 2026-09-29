import json, sys, time
from pathlib import Path
import numpy as np, pandas as pd
ENG = Path("/home/user/trading-data/engine"); sys.path.insert(0, str(ENG))
import cage_policy_lib as cpl
st = json.loads((ENG / "book_state.json").read_text(encoding="utf-8"))
legs = [l["name"] for l in st["legs"]]; pbl = {l["name"]: l["params"] for l in st["legs"]}
C, W, apy, legs2, days = cpl.load_pool(legs, pbl, None, True)
dc1, dw1 = C.sum(1), W.sum(1)
days = pd.to_datetime([str(d) for d in days])
print("n", len(dc1), "apy", apy, "mean", dc1.mean(), "sd", dc1.std(), "skew", pd.Series(dc1).skew(), "kurt", pd.Series(dc1).kurt())
print("max dc1", dc1.max(), "top10", np.sort(dc1)[-10:])
print("min dw1", dw1.min(), "min dc1", dc1.min())
for thr in (900, 960, 1000, 1440, 2880):
    m = dc1 > thr
    print(f"> {thr}: n={m.sum()}", [(str(d.date()), round(v)) for d, v in zip(days[m], dc1[m])])
rec = days >= pd.Timestamp("2023-08-06")
print("recent n", rec.sum(), "mean", dc1[rec].mean())
s = pd.Series(dc1, index=days)
print(s.groupby(s.index.year).agg(["count", "sum", "mean", "max"]))
# per-leg on big days
for i in np.flatnonzero(dc1 > 900):
    print(str(days[i].date()), np.round(C[i], 0), "dw", round(dw1[i]))
# share of total PnL from days >900
print("share PnL > 900 days:", dc1[dc1 > 900].sum() / dc1.sum(), " excess over 900:", np.maximum(dc1 - 900, 0).sum() / dc1.sum())
t0 = time.time()
horizon = int(round(36 * apy / 12.0))
P = cpl.draw_paths(len(dc1), 6000, horizon, 11, 10)
t1 = time.time()
risk = float(np.percentile(np.abs(dw1[dw1 < 0]), 50))
a = cpl.run_account(P, dc1, dw1, risk, 0, 0.01, 2500.0, 1500.0, 40, "intraday", horizon)
t2 = time.time()
print("risk", risk, "horizon", horizon, "draw", t1 - t0, "run", t2 - t1, "pass", np.isfinite(a).mean())
