"""Statistiker 01.10.: Master-Pfade (Seed 101) nachbauen, realisierte Drift je Sim, Deltas nach Drift-Terzil. Nur lesen."""
import json, os, sys
import numpy as np
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
ENG = "/home/user/trading-data/engine"
os.chdir(ENG); sys.path.insert(0, ENG)
import tempo_plan as tp
dc0, dw0, apy, days, C, W = tp.build_cells(None)
TM = apy/12.0; NT0 = int(np.ceil(120*TM)) + 1; H = tp.CAL_H
print("TM", round(TM,3), "NT0", NT0, "H", H, "n_days", len(dc0), "mu", round(dc0.mean(),2), "sd", round(dc0.std(),1))
# Unsicherheit des historischen Mittels (Block-Bootstrap der Tagesreihe, Block 10)
rng = np.random.default_rng(1)
idx = tp.L.draw_paths(len(dc0), 4000, len(dc0), 77, 10)
bm = dc0[idx].mean(1)
print(f"Hist. Mittel {dc0.mean():.2f} $/Tag, Block-Bootstrap-SE {bm.std():.2f}, 90%-CI [{np.percentile(bm,5):.2f}; {np.percentile(bm,95):.2f}]")
half = len(dc0)//2
print(f"H1 {dc0[:half].mean():.2f}  H2 {dc0[half:].mean():.2f}")
V = ["C_d040","D_d040_lock","C3_d040_k3","D3_lock_k3","A_heute"]
TMAX = 120.0
out = {}
for rg, n in [("IS",600),("shrink058",400),("recent3y",400),("shrink_recent",400)]:
    dc, dw = tp.apply_regime(dc0, dw0, days, rg)
    masters = tp.L.draw_paths(len(dc), n, NT0 + H, 101, 10)
    mu_all = dc[masters[:, :NT0]].mean(1)
    mu_24 = dc[masters[:, :int(24*TM)]].mean(1)
    r = json.load(open(f"{SP}/fnrun/fn_tempo_{rg}_{n}.json"))
    T = {v: np.array([TMAX if t is None else min(t, TMAX) for t in r["T_m"][v]]) for v in V}
    Rch = {v: np.array([t is not None for t in r["T_m"][v]]) for v in V}
    # Plausibilitaet: Korrelation realisierte Drift vs Zeit
    print(f"\n### {rg} n={n}  mu_regime {dc.mean():.2f}  realisierte Pfad-Drift (120 M): p10 {np.percentile(mu_all,10):.1f} p50 {np.median(mu_all):.1f} p90 {np.percentile(mu_all,90):.1f}"
          f"  corr(mu120, T_C) {np.corrcoef(mu_all, T['C_d040'])[0,1]:+.2f}  corr(mu24, T_C) {np.corrcoef(mu_24, T['C_d040'])[0,1]:+.2f}")
    q = np.quantile(mu_all, [1/3, 2/3])
    terc = np.digitize(mu_all, q)
    for a, b in [("D_d040_lock","C_d040"),("C3_d040_k3","C_d040"),("D3_lock_k3","D_d040_lock"),("A_heute","C_d040")]:
        row = []
        for g in range(3):
            m = terc == g
            d = T[a][m] - T[b][m]; nn = m.sum()
            bs = d[rng.integers(nn, size=(2000, nn))].mean(1)
            dr = (Rch[a][m].mean() - Rch[b][m].mean())*100
            row.append(f"T{g+1} (mu {mu_all[m].mean():5.1f}): dRMST {d.mean():+5.2f} [{np.percentile(bs,5):+5.2f};{np.percentile(bs,95):+5.2f}] dReach {dr:+5.1f}pp reachC {Rch[b][m].mean()*100:4.0f}%")
        print(f"  {a}-{b}:\n     " + "\n     ".join(row))
    # Regression: dRMST ~ mu_all (Steigung je 10 $/Tag Drift)
    for a, b in [("D_d040_lock","C_d040"),("C3_d040_k3","C_d040")]:
        d = T[a] - T[b]; X = np.c_[np.ones(n), mu_all - mu_all.mean()]
        beta, *_ = np.linalg.lstsq(X, d, rcond=None)
        res = d - X @ beta; s2 = res @ res/(n-2); cov = s2*np.linalg.inv(X.T @ X)
        print(f"  Steigung {a}-{b}: {beta[1]*10:+.2f} M je +10 $/Tag Pfad-Drift (SE {np.sqrt(cov[1,1])*10:.2f})")
    out[rg] = dict(mu_all=mu_all.round(3).tolist(), mu_24=mu_24.round(3).tolist())
json.dump(out, open(f"{SP}/stat_fn_drift.json", "w"))
