"""Statistiker 01.10.: Plan-Tod-Flags je Sim gepaart nachrechnen, NUR fuer Sims, die in mind. einer von C/D/C3/D3 das Ziel
verfehlt haben (nur dort ist oekonomischer Tod moeglich). Exakt die Master-Zeilen des Original-Laufs (Seed 101, volle
Matrix erzeugen, Zeilen SEL rechnen). Validierung: T je Sim muss mit fnrun/*.json uebereinstimmen. Aendert nichts an der Engine."""
import json, os, sys, time
import numpy as np
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
os.environ["VSET"] = "decomp"
sys.path.insert(0, SP)
import fn_tempo_check as fc   # chdir ENG, Monkeypatch _cal_eval/_cal_fund
tp = fc.tp
rg, n_orig, nsub = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
V = ["C_d040", "D_d040_lock", "Dh_half_lock"]
fc.VARIANTS = {k: fc.VARIANTS[k] for k in V}
r = json.load(open(f"{SP}/fnrun_decomp/fn_tempo_decomp_{rg}_{n_orig}.json"))
nr = np.zeros(n_orig, bool)
for v in V:
    nr |= np.array([t is None for t in r["T_m"][v]])
U = np.flatnonzero(nr)
SEL = U if len(U) <= nsub else np.sort(np.random.default_rng(3).choice(U, nsub, replace=False))
dc0, dw0, apy, days, C, W = tp.build_cells(None)
TM = apy / 12.0; NT0 = int(np.ceil(fc.TMAX_M * TM)) + 1
dc, dw = tp.apply_regime(dc0, dw0, days, rg)
_orig = tp.L.draw_paths
def _patched(n_days, n_sims, horizon, seed, block_mean=10):
    if seed == fc.SEED and horizon == NT0 + tp.CAL_H:
        return _orig(n_days, n_orig, horizon, seed, block_mean)[SEL]
    return _orig(n_days, n_sims, horizon, seed, block_mean)
tp.L.draw_paths = _patched
t0 = time.time()
pol = fc.policies(dc, dw, f"fncheck|{rg}")
sims = tp.simulate_fleet_calendar(pol, fc.G, TM, B=fc.BUDGET, Tmax_m=fc.TMAX_M, nsim=len(SEL), seed=fc.SEED,
                                  max_outlay=fc.CAP_OUT, marks_m=fc.MARKS, return_raw=True, path_demean=False,
                                  day_stop=tp.day_stop_fn("rg"))
out = dict(regime=rg, n_orig=n_orig, n_union=int(len(U)), sel=SEL.tolist(), TM=TM, var={})
mism = 0
for v in V:
    raw = sims[v]["_raw"]; rows = []
    for i, s in enumerate(SEL):
        x = raw[i]
        Tm = None if not np.isfinite(x["T"]) else round(float(x["T"]) / TM, 2)
        if Tm != r["T_m"][v][s]:
            mism += 1
        rows.append(dict(s=int(s), T_m=Tm, econ=bool(x["econ"]),
                         t_econ_m=None if x["t_econ"] is None else round(float(x["t_econ"]) / TM, 2),
                         t_idle_m=None if x["t_idle"] is None else round(float(x["t_idle"]) / TM, 2),
                         zombie=bool(x["zombie"]), net_end=round(float(x["net_end"])), out=round(float(x["out"])),
                         nfund=int(x["nfund"]), nevb=int(x["nevb"]), nfr=int(x["nfr"]), marks=[round(m) for m in x["marks"]]))
    out["var"][v] = rows
out["mismatch_T"] = mism; out["sec"] = round(time.time() - t0, 1)
json.dump(out, open(f"{SP}/stat_rerun/econDh_{rg}.json", "w"), indent=0)
print(f"{rg}: n_union {len(U)} gerechnet {len(SEL)} in {out['sec']} s, T-Abweichungen {mism}", flush=True)
