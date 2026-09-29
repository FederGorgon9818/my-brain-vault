import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_consistency_passquote as F
cpl = F.cpl
def kern(paths, dc, dw, target, dd, horizon, rule_frac=None, lock=100.0):
    n = paths.shape[0]
    bal = np.zeros(n); peak = np.zeros(n); floor = np.full(n, -float(dd)); cmax = np.zeros(n)
    alive = np.ones(n, bool); pday = np.full(n, np.inf)
    for t in range(horizon):
        idx = np.flatnonzero(alive)
        if idx.size == 0: break
        k = paths[idx, t]
        br = (bal[idx] + dw[k]) <= floor[idx]
        if br.any():
            alive[idx[br]] = False; idx, k = idx[~br], k[~br]
            if idx.size == 0: continue
        pnl = dc[k]; bal[idx] += pnl; cmax[idx] = np.maximum(cmax[idx], pnl)
        br = bal[idx] <= floor[idx]
        if br.any():
            alive[idx[br]] = False; idx = idx[~br]
            if idx.size == 0: continue
        peak[idx] = np.maximum(peak[idx], bal[idx]); floor[idx] = np.minimum(peak[idx] - dd, lock)
        ok = bal[idx] >= target
        if rule_frac is not None: ok &= cmax[idx] <= rule_frac * np.maximum(bal[idx], 1e-9)
        w = idx[ok]
        if w.size: pday[w] = t; alive[w] = False
    return pday
C, W, apy, days, legs, pbl = F.load_book()
dc1_all, dw1_all = C.sum(1), W.sum(1)
H = int(round(36 * apy / 12.0)); m12 = 12 * apy / 12.0
for label, tier, k, os_list in (("FN 50k", "50k", 1, (100, 200, 400)), ("FN 150k", "150k", 3, (320, 640, 1200))):
    tg, dd = F.FN[tier]["target"], F.FN[tier]["dd"]; trig = 0.36 * tg
    for rg in ("IS", "shrink_recent"):
        d1, w1 = F.regime(dc1_all, dw1_all, days, rg); dc, dw = d1 * k, w1 * k
        out = {}
        for s in F.SEEDS:
            P = cpl.draw_paths(len(dc), F.N_SIMS, H, s, F.BLOCK)
            out.setdefault("C", []).append(kern(P, np.minimum(dc, trig), dw, tg, dd, H, 0.40))
            for o in os_list:
                out.setdefault(o, []).append(kern(P, np.minimum(dc, trig + o), dw, tg, dd, H, 0.40))
        base36 = np.array([np.isfinite(x).mean() * 100 for x in out["C"]]); base12 = np.array([(x <= m12).mean() * 100 for x in out["C"]])
        s = f"{label} k{k} {rg:13s} C(lock100) 36M {base36.mean():.2f} 12M {base12.mean():.2f} |"
        for o in os_list:
            p36 = np.array([np.isfinite(x).mean() * 100 for x in out[o]]); p12 = np.array([(x <= m12).mean() * 100 for x in out[o]])
            s += f" o={o}: {(p36 - base36).mean():+.2f}/{(p12 - base12).mean():+.2f}"
        print(s)
