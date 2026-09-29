"""Statistiker 29.09.: aeusserer Block-Bootstrap fuer E[Zeit bis funded] mit Nachkauf nach Bust (Wald: E[D]/p),
B (40-%-Regel) vs. C (Deckel 0,36). Kern tempo_plan.run_eval_fn, CRN B/C."""
import argparse, json, sys
from pathlib import Path
import numpy as np
SCR = Path(__file__).resolve().parent; sys.path.insert(0, str(SCR))
from stat_outer import load, shift
import cage_policy_lib as cpl
import tempo_plan as tp
from fn_consistency_passquote import FN, RECENT
CONF = [("50k", 1), ("150k", 3), ("150k", 2)]

def ET(dc1, dw1, P, apy):
    out = {}
    for tier, k in CONF:
        T = FN[tier]; cap = 0.36 * T["target"]; dc, dw = dc1 * k, dw1 * k
        stB, dB = tp.run_eval_fn(P, dc, dw, T["target"], T["dd"], k=1, day_cap_frac=0.40)
        stC, dC = tp.run_eval_fn(P, np.minimum(dc, cap), dw, T["target"], T["dd"], k=1, day_cap_frac=None)
        pB, pC = (stB == 1).mean(), (stC == 1).mean()
        eB = dB.mean() / pB / apy * 12 if pB > 0 else np.nan
        eC = dC.mean() / pC / apy * 12 if pC > 0 else np.nan
        out[f"{tier}_k{k}"] = dict(ETB=eB, ETC=eC, d=eC - eB, pB=pB, pC=pC)
    return out

ap = argparse.ArgumentParser(); ap.add_argument("--R", type=int, default=100); ap.add_argument("--start", type=int, default=0)
ap.add_argument("--out", default="outerT.json"); a = ap.parse_args()
dc1, dw1, apy, days = load(); rec = days >= RECENT; H = int(round(36 * apy / 12.0))
N, Nr = len(dc1), int(rec.sum()); reps = []
for r in range(a.start, a.start + a.R):
    res = {}
    idx = cpl.draw_paths(N, 1, N, 50000 + r, 10)[0]; d1, w1 = dc1[idx], dw1[idx]
    P = cpl.draw_paths(N, 4000, H, 90000 + r, 10)
    res["IS"] = ET(d1, w1, P, apy)
    res["shrink058"] = ET(*shift(d1, w1, 0.58 * d1.mean()), P, apy)
    idr = cpl.draw_paths(Nr, 1, Nr, 70000 + r, 10)[0]; d2, w2 = dc1[rec][idr], dw1[rec][idr]
    P2 = cpl.draw_paths(Nr, 4000, H, 110000 + r, 10)
    res["recent3y"] = ET(d2, w2, P2, apy)
    res["shrink_recent"] = ET(*shift(d2, w2, 0.58 * d2.mean()), P2, apy)
    reps.append(res)
(SCR / a.out).write_text(json.dumps(reps)); print("fertig")
