"""50 Flotten-Sims IS: Auszahlungs-Verzoegerung delta (Buchtage) auf ALLE Payouts (E8 + FN), C vs D."""
import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad")
import fn_tempo_check as F
tp = F.tp; L = tp.L
DEL = int(sys.argv[2]) if len(sys.argv) > 2 else 4
def shift(fl, d):
    out = np.zeros_like(fl); out[:, d:] = fl[:, :-d]; return out
_f = tp._cal_fund
def _cal_fund_w(win, dc, dw, tk, ds=None):
    firm, tier, k = tk
    if tier.endswith("|w"):
        base = tier[:-2]; r = _f(win, dc, dw, (firm, base, k), ds=ds); r = dict(r); r["flow"] = shift(r["flow"], DEL); return r
    return _f(win, dc, dw, tk, ds=ds)
_e = tp._cal_eval
def _cal_eval_w(win, dc, dw, tk, bal0=0.0, peak0=0.0, ds=None):
    firm, tier, k = tk
    if tier.endswith("|w"): tier = tier[:-2]
    return _e(win, dc, dw, (firm, tier, k), bal0=bal0, peak0=peak0, ds=ds)
tp._cal_fund, tp._cal_eval = _cal_fund_w, _cal_eval_w
for t in ("50k", "150k"):
    tp.E8[t + "|w"] = tp.E8[t]; L.CAPS[t + "|w"] = L.CAPS[t]
G, BUDGET, CAP_OUT, SEED, TMAX_M = 50000.0, 600.0, 2500.0, 101, 120
nsim = int(sys.argv[1])
dc0, dw0, apy, days, C, W = tp.build_cells(None); TM = apy/12
dc, dw = tp.apply_regime(dc0, dw0, days, "IS")
pf = lambda firm, tier, k, **kw: tp.make_pool(dc, dw, firm, tier, k, n=50, tag="qmw", **kw)
OPT = {"C": dict(eval_cap=0.40, fix=True), "D": dict(eval_cap=0.40, fix=True, theta=1.0, lock_first=True)}
pol = {}
for o in ("C", "D"):
    for w in ("", "|w"):
        t50, t150 = F.fn_type("50k", **OPT[o]), F.fn_type("150k", **OPT[o])
        if w:
            for tn in (t50, t150):
                tp.FN[tn + w] = tp.FN[tn]
        init = [dict(pool=pf("E8", "50k" + w, 1, **tp.E8_START), stage="eval", fresh=pf("E8", "50k" + w, 1)),
                dict(pool=pf("FN", t50 + w, 1), stage="eval"), dict(pool=pf("FN", t50 + w, 1), stage="eval")]
        lanes = [dict(pool=pf("E8", "150k" + w, 2), n_max=4, m=2, start_m=0), dict(pool=pf("FN", t150 + w, 2), n_max=4, m=2, start_m=0)]
        pol[o + ("_wait" if w else "")] = dict(lanes=lanes, init=init)
sims = tp.simulate_fleet_calendar(pol, G, TM, B=BUDGET, Tmax_m=TMAX_M, nsim=nsim, seed=SEED, max_outlay=CAP_OUT,
                                  marks_m=(9, 12, 24, 36), return_raw=True, day_stop=tp.day_stop_fn("rg"))
raw = {n: v.pop("_raw") for n, v in sims.items()}
Tm = {n: np.minimum(np.array([r["T"] for r in v], float)/TM, TMAX_M) for n, v in raw.items()}
print(f"n={nsim} IS, Verzoegerung {DEL} Buchtage = {DEL/TM:.2f} M")
for n in sims: print(f"{n:7s} rmst {sims[n]['rmst_m']:6.1f} dead {sims[n]['p_econ_dead']:5.1f}")
for a, b in (("C_wait", "C"), ("D_wait", "D"), ("D", "C"), ("D_wait", "C_wait")):
    d = Tm[a] - Tm[b]; print(f"  {a} - {b}: {d.mean():+.2f} (SE {d.std(ddof=1)/np.sqrt(len(d)):.2f}) M")
