import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_consistency_passquote as F
from qm_kern import kern
cpl = F.cpl
C, W, apy, days, legs, pbl = F.load_book()
dc1_all, dw1_all = C.sum(1), W.sum(1)
H = int(round(36 * apy / 12.0)); m12 = 12 * apy / 12.0
for label, tier, k in (("FN 50k", "50k", 1), ("FN 150k", "150k", 3)):
    tg, dd = F.FN[tier]["target"], F.FN[tier]["dd"]
    for rg in ("IS", "shrink058", "recent3y", "shrink_recent", "null"):
        d1, w1 = F.regime(dc1_all, dw1_all, days, rg); dc, dw = d1 * k, w1 * k
        d36, d12 = [], []
        for s in F.SEEDS:
            P = cpl.draw_paths(len(dc), F.N_SIMS, H, s, F.BLOCK)
            a = kern(P, np.minimum(dc, 0.36 * tg), dw, tg, dd, H, 0.40)
            b = kern(P, np.minimum(dc, 0.40 * tg), dw, tg, dd, H, 0.40)
            d36.append((np.isfinite(b).mean() - np.isfinite(a).mean()) * 100)
            d12.append(((b <= m12).mean() - (a <= m12).mean()) * 100)
        print(f"{label} k{k} {rg:13s} Ausloeser 0.40T vs 0.36T: 36M {np.mean(d36):+.2f}±{np.std(d36, ddof=1):.2f}  12M {np.mean(d12):+.2f}±{np.std(d12, ddof=1):.2f}")
