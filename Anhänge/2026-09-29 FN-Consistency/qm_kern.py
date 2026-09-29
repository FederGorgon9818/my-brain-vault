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
