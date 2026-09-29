"""quant-mathematician Gegenrechnung 29.09.: Lock +100, Status (pass/bust/offen), Nachkauf-Sicht B vs C."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fn_consistency_passquote as F
cpl = F.cpl

def kern(paths, dc, dw, target, dd, horizon, rule_frac=None, lock=0.0):
    """Min-Size (sz=1), Intraday-Bust gegen EOD-Floor, Lock bei `lock`. Rueckgabe status (1/-1/0), tag (1-basiert)."""
    n = paths.shape[0]
    bal = np.zeros(n); peak = np.zeros(n); floor = np.full(n, -float(dd)); cmax = np.zeros(n)
    alive = np.ones(n, bool); st = np.zeros(n, np.int8); day = np.full(n, float(horizon))
    for t in range(horizon):
        idx = np.flatnonzero(alive)
        if idx.size == 0: break
        k = paths[idx, t]
        br = (bal[idx] + dw[k]) <= floor[idx]
        if br.any():
            b = idx[br]; st[b] = -1; alive[b] = False; day[b] = t + 1
            idx, k = idx[~br], k[~br]
            if idx.size == 0: continue
        pnl = dc[k]; bal[idx] += pnl; cmax[idx] = np.maximum(cmax[idx], pnl)
        br = bal[idx] <= floor[idx]
        if br.any():
            b = idx[br]; st[b] = -1; alive[b] = False; day[b] = t + 1
            idx = idx[~br]
            if idx.size == 0: continue
        peak[idx] = np.maximum(peak[idx], bal[idx]); floor[idx] = np.minimum(peak[idx] - dd, lock)
        ok = bal[idx] >= target
        if rule_frac is not None:
            ok &= cmax[idx] <= rule_frac * np.maximum(bal[idx], 1e-9)
        w = idx[ok]
        if w.size: st[w] = 1; alive[w] = False; day[w] = t + 1
    return st, day

def chain(st, day, apy, months_list, n_chain=200000, seed=5):
    """Sequentieller Nachkauf: Versuche iid aus (st, day) ziehen, bis bestanden. Offen bei H = Abbruch + Neukauf."""
    rng = np.random.default_rng(seed)
    n = st.size
    T = np.zeros(n_chain); done = np.zeros(n_chain, bool); buys = np.zeros(n_chain)
    for _ in range(60):
        j = rng.integers(n, size=n_chain)
        live = ~done
        T[live] += day[j][live]; buys[live] += 1
        done |= live & (st[j] == 1)
        if done.all(): break
    Tm = T / apy * 12.0
    return {m: float(((Tm <= m) & done).mean() * 100) for m in months_list}, float(np.mean(Tm)), float(buys.mean())

C, W, apy, days, legs, pbl = F.load_book()
dc1_all, dw1_all = C.sum(1), W.sum(1)
H = int(round(36 * apy / 12.0))
neg = np.abs(dw1_all[dw1_all < 0])
print("risk k1 (median |dw|<0):", round(float(np.percentile(neg, 50)), 1), " -> sz>1 erst ab bal-floor >=", round(2 * float(np.percentile(neg, 50)) / 0.01))
print("Tage mit dc1 > 900:", int((dc1_all > 900).sum()), " > 1000:", int((dc1_all > 1000).sum()), " von", len(dc1_all))
res = {}
for label, tier, k in [("FN 50k", "50k", 1), ("FN 150k", "150k", 3)]:
    tg, dd = F.FN[tier]["target"], F.FN[tier]["dd"]; cap = 0.36 * tg
    for rg in ["IS", "shrink058", "recent3y", "shrink_recent", "null"]:
        d1, w1 = F.regime(dc1_all, dw1_all, days, rg)
        dc, dw = d1 * k, w1 * k; dcC = np.minimum(dc, cap)
        row = {}
        for lock in (0.0, 100.0):
            acc = {v: [] for v in "ABC"}
            for s in F.SEEDS:
                P = cpl.draw_paths(len(dc), F.N_SIMS, H, s, F.BLOCK)
                acc["A"].append(kern(P, dc, dw, tg, dd, H, None, lock))
                acc["B"].append(kern(P, dc, dw, tg, dd, H, 0.40, lock))
                acc["C"].append(kern(P, dcC, dw, tg, dd, H, None, lock))
            for v in "ABC":
                st = np.concatenate([a[0] for a in acc[v]]); dy = np.concatenate([a[1] for a in acc[v]])
                ps = [float((a[0] == 1).mean() * 100) for a in acc[v]]
                row[(v, lock)] = dict(p=np.mean(ps), ps=ps, bust=float((st == -1).mean() * 100), open=float((st == 0).mean() * 100),
                                      ED=float(dy.mean() / apy * 12))
                if lock == 100.0:
                    within, ET, buys = chain(st, dy, apy, (6, 12, 24))
                    row[(v, lock)].update(w6=within[6], w12=within[12], w24=within[24], ET=ET, buys=buys)
        res[(label, k, rg)] = row
        r0 = row
        dCB0 = np.mean(np.array(r0[("C", 0.0)]["ps"]) - np.array(r0[("B", 0.0)]["ps"]))
        dCB1 = np.mean(np.array(r0[("C", 100.0)]["ps"]) - np.array(r0[("B", 100.0)]["ps"]))
        print(f"{label} k{k} {rg:13s} lock0: A {r0[('A',0.0)]['p']:.2f} B {r0[('B',0.0)]['p']:.2f} C {r0[('C',0.0)]['p']:.2f} C-B {dCB0:+.2f} | "
              f"lock100: A {r0[('A',100.0)]['p']:.2f} B {r0[('B',100.0)]['p']:.2f} C {r0[('C',100.0)]['p']:.2f} C-B {dCB1:+.2f}")
        for v in "BC":
            q = r0[(v, 100.0)]
            print(f"    {v} lock100: bust {q['bust']:.2f} offen {q['open']:.2f} E[Dauer] {q['ED']:.2f} M | Nachkauf: P(funded<=6M) {q['w6']:.2f} <=12M {q['w12']:.2f} <=24M {q['w24']:.2f}  E[T] {q['ET']:.2f} M  E[Kaeufe] {q['buys']:.2f}")
