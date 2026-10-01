"""FN-Varianten gegen die Zeit bis 50.000 $ (Cloud-Session 01.10.2026, Scratch, aendert keine Engine-Datei).

Auftrag Max 01.10.: "alles mal durchrechnen". Drei Fragen, alle an der Messlatte Zeit bis 50k (Kalender-Modus AP245,
genau wie weekend_check.py: Bestand E8 50k + FN1/FN2, Lanes E8 150k k2 + FN 150k, n_max 4, m 2, Deckel 2.500 $
Netto-Auslage, B 600 $/Monat, Master-Pfade Seed 101, RiskGuard-Tages-Stopp 'rg', Nulldrift per path_demean):
  1. FN-Funded: Deckel aus (FN schriftlich 01.10. erlaubt) und Auszahlungs-Politik "sofort" gegen "erst nach
     Floor-Lock, dann nur volle Caps".
  2. FN-Challenge: Deckel 0,36 (live) gegen 0,40 (beschlossen 29.09.) gegen reine 40-%-Regel (heutiges Modell).
  3. FN 150k Lane: k2 gegen k3 (AP248).
Korrektur gegenueber tempo_plan.run_funded_fn (Befund 26.09.): FN zahlt bis 50 % des Gewinns SEIT DER LETZTEN
Auszahlung (Research-Cache, Support-Mails 20./21.08.), nicht 50 % des ganzen Kontogewinns. Schalter fix=True.
Technik: FN-Varianten als eigene Tier-Namen in tp.FN (gleiche Zahlen), tp._cal_eval/_cal_fund per Monkeypatch nur
fuer diese Tiers ersetzt. Alles andere ist der Original-Kernel. Bit-Gleichheit bei ausgeschalteten Optionen wird
vor dem Lauf geprueft.
Aufruf: python fn_tempo_check.py <regime> <nsim> [--check]   (regime: IS|null|shrink058|recent3y|shrink_recent)
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ENG = Path(os.environ.get("MAXLAB_ENGINE", "/home/user/trading-data/engine"))
os.chdir(ENG); sys.path.insert(0, str(ENG))
import tempo_plan as tp  # noqa: E402

G, BUDGET, CAP_OUT, SEED, TMAX_M = 50000.0, 600.0, 2500.0, 101, 120
MARKS = (9, 12, 24, 36)
POOL_N = 50
OUT = Path(os.environ.get("OUTDIR", Path(__file__).parent))

# ---------------------------------------------------------------- FN-Varianten-Typen
OPTS = {}


def fn_type(tier, eval_cap=None, fix=False, theta=None, lock_first=False, fund_cap=None):
    name = f"{tier}|ec{eval_cap}|fx{int(fix)}|th{theta}|lf{int(lock_first)}|fc{fund_cap}"
    if name not in tp.FN:
        tp.FN[name] = dict(tp.FN[tier])
        OPTS[name] = dict(base=tier, eval_cap=eval_cap, fix=fix, theta=theta, lock_first=lock_first, fund_cap=fund_cap)
    return name


def run_funded_fn_x(paths, dc, dw, dd, cap, bench, k=1, split=0.95, need_days=5, lock_level=100.0, max_pays=5,
                    min_gross=250.0, ds=None, fix=False, theta=None, lock_first=False):
    """tp.run_funded_fn Zeile fuer Zeile, plus drei Schalter (alle aus = bit-gleich):
    fix        Auszahlung bis 50 % des Gewinns seit der letzten Auszahlung (statt des ganzen Kontogewinns)
    theta      Slot erst abrufen, wenn abrufbar >= theta x Cap (1.0 = nur volle Caps)
    lock_first erste Auszahlung erst, wenn der Floor eingerastet ist (peak - dd >= lock_level)"""
    n, H = paths.shape
    bal = np.zeros(n); peak = np.zeros(n); floor = np.full(n, -float(dd)); base = np.zeros(n)
    alive = np.ones(n, bool); npay = np.zeros(n, np.int64); netsum = np.zeros(n)
    cg = np.zeros(n, np.int64); life = np.full(n, float(H)); t1 = np.full(n, np.nan)
    ruin = np.zeros(n, bool); done5 = np.zeros(n, bool); flow = np.zeros((n, H))
    for t in range(H):
        idx = np.flatnonzero(alive)
        if idx.size == 0: break
        j = paths[idx, t]
        if ds is None:
            br = (bal[idx]+dw[j]*k) <= floor[idx]
        else:
            c_, w_ = tp._stop_day(dc[j], dw[j], k, bal[idx], floor[idx], ds)
            br = (bal[idx] + w_) <= floor[idx]
        if br.any():
            b = idx[br]; ruin[b] = True; alive[b] = False; life[b] = t+1
            idx = idx[~br]; j = j[~br]
            if ds is not None: c_ = c_[~br]
            if idx.size == 0: continue
        pnl = dc[j]*k if ds is None else c_; bal[idx] += pnl
        br = bal[idx] <= floor[idx]
        if br.any():
            b = idx[br]; ruin[b] = True; alive[b] = False; life[b] = t+1
            idx = idx[~br]; pnl = pnl[~br]
            if idx.size == 0: continue
        peak[idx] = np.maximum(peak[idx], bal[idx]); floor[idx] = np.minimum(peak[idx]-dd, lock_level)
        cg[idx] += (pnl >= bench)
        prof = bal[idx] - base[idx] if fix else bal[idx]
        w = np.minimum(0.5*np.maximum(prof, 0.0), cap)
        w = np.minimum(w, bal[idx]-lock_level)
        ok = (w >= min_gross) & (cg[idx] >= need_days)
        if theta is not None:
            ok &= w >= theta*cap
        if lock_first:
            ok &= (npay[idx] > 0) | (floor[idx] >= lock_level)
        pay = idx[ok]
        if pay.size:
            wp = w[ok]; amt = wp*split
            netsum[pay] += amt; bal[pay] -= wp; flow[pay, t] += amt
            if fix: base[pay] = bal[pay]
            newf = pay[npay[pay] == 0]
            if newf.size: t1[newf] = t+1
            npay[pay] += 1; cg[pay] = 0
            fin = pay[npay[pay] >= max_pays]
            if fin.size: done5[fin] = True; alive[fin] = False; life[fin] = t+1
    return dict(netsum=netsum, life=life, t1=t1, npay=npay, ruin=ruin, done5=done5, flow=flow)


_orig_eval, _orig_fund = tp._cal_eval, tp._cal_fund


def _cal_eval(win, dc, dw, tk, bal0=0.0, peak0=0.0, ds=None):
    firm, tier, k = tk
    o = OPTS.get(tier) if firm == "FN" else None
    if o is None:
        return _orig_eval(win, dc, dw, tk, bal0=bal0, peak0=peak0, ds=ds)
    T = tp.FN[tier]
    dce = dc if o["eval_cap"] is None else np.minimum(dc, o["eval_cap"]*T["target"]/k)
    return tp.run_eval_fn(win, dce, dw, T["target"], T["dd"], k=k, bal0=bal0, peak0=peak0, ds=ds)


def _cal_fund(win, dc, dw, tk, ds=None):
    firm, tier, k = tk
    o = OPTS.get(tier) if firm == "FN" else None
    if o is None:
        return _orig_fund(win, dc, dw, tk, ds=ds)
    T = tp.FN[tier]
    dcf = dc if o["fund_cap"] is None else np.minimum(dc, o["fund_cap"]*T["target"]/k)
    return run_funded_fn_x(win, dcf, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds,
                           fix=o["fix"], theta=o["theta"], lock_first=o["lock_first"])


tp._cal_eval, tp._cal_fund = _cal_eval, _cal_fund

# ---------------------------------------------------------------- Varianten
VARIANTS = {
    # name: (fn-Optionen, FN-150k-k)
    "A_heute":      (dict(), 2),                                          # Modell wie heute (Regel, Auszahlungsfehler)
    "B_d036":       (dict(eval_cap=0.36, fix=True), 2),                   # live heute, Formel korrigiert
    "C_d040":       (dict(eval_cap=0.40, fix=True), 2),                   # Deckel 0,40 (beschlossen)
    "D_d040_lock":  (dict(eval_cap=0.40, fix=True, theta=1.0, lock_first=True), 2),  # + erst Lock, dann volle Caps
    "E_d040_fcap":  (dict(eval_cap=0.40, fix=True, fund_cap=0.40), 2),    # Deckel auch im Funded an
    "C3_d040_k3":   (dict(eval_cap=0.40, fix=True), 3),                   # wie C, FN 150k mit k3
    "D3_lock_k3":   (dict(eval_cap=0.40, fix=True, theta=1.0, lock_first=True), 3),  # wie D, FN 150k mit k3
}


if os.environ.get("VSET") == "decomp":     # Zerlegung der Auszahlungs-Politik D (nur k2)
    VARIANTS = {
        "C_d040":       (dict(eval_cap=0.40, fix=True), 2),
        "D_d040_lock":  (dict(eval_cap=0.40, fix=True, theta=1.0, lock_first=True), 2),
        "Dl_lockonly":  (dict(eval_cap=0.40, fix=True, lock_first=True), 2),
        "Dc_capsonly":  (dict(eval_cap=0.40, fix=True, theta=1.0), 2),
        "Dh_half_lock": (dict(eval_cap=0.40, fix=True, theta=0.5, lock_first=True), 2),
    }


def policies(dc, dw, tag):
    pf = lambda firm, tier, k, **kw: tp.make_pool(dc, dw, firm, tier, k, n=POOL_N, tag=tag, **kw)
    out = {}
    for name, (o, k_fn) in VARIANTS.items():
        t50, t150 = fn_type("50k", **o), fn_type("150k", **o)
        init = [dict(pool=pf("E8", "50k", 1, **tp.E8_START), stage="eval", fresh=pf("E8", "50k", 1)),
                dict(pool=pf("FN", t50, 1), stage="eval"), dict(pool=pf("FN", t50, 1), stage="eval")]
        lanes = [dict(pool=pf("E8", "150k", 2), n_max=4, m=2, start_m=0),
                 dict(pool=pf("FN", t150, k_fn), n_max=4, m=2, start_m=0)]
        out[name] = dict(lanes=lanes, init=init)
    return out


def check_bitgleich():
    """Optionen aus -> Kernel bit-gleich zu tempo_plan (mit und ohne RiskGuard-Stopp)."""
    dc, dw, apy, days, C, W = tp.build_cells(None)
    rng = np.random.default_rng(5)
    paths = rng.integers(len(dc), size=(300, 400))
    res = {}
    for ds_mode in (None, "rg"):
        dsf = tp.day_stop_fn(ds_mode)
        for tier, k in (("50k", 1), ("150k", 2), ("150k", 3)):
            ds = dsf(("FN", tier, k)) if dsf else None
            T = tp.FN[tier]
            a = tp.run_funded_fn(paths, dc, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds)
            b = run_funded_fn_x(paths, dc, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds)
            same = all(np.array_equal(a[x], b[x], equal_nan=True) for x in a)
            t_off = fn_type(tier)
            e1 = _orig_eval(paths, dc, dw, ("FN", tier, k), ds=ds)
            e2 = _cal_eval(paths, dc, dw, ("FN", t_off, k), ds=ds)
            same_e = np.array_equal(e1[0], e2[0]) and np.array_equal(e1[1], e2[1])
            res[f"{tier}_k{k}_{ds_mode}"] = dict(funded=same, eval=same_e)
    return res


def paired(raw, TM, ref):
    """Gepaarte Unterschiede je Sim (gleiche Master-Pfade): RMST-120-Delta und Erreichungs-Delta, Bootstrap-SE."""
    def tarr(name):
        return np.minimum(np.array([r["T"] for r in raw[name]], float) / TM, TMAX_M)
    out = {}
    rng = np.random.default_rng(7)
    a = tarr(ref)
    for n in raw:
        if n == ref: continue
        b = tarr(n); d = b - a
        idx = rng.integers(len(d), size=(2000, len(d)))
        bs = d[idx].mean(1)
        reach_d = float(((b < TMAX_M).mean() - (a < TMAX_M).mean()) * 100)
        out[n] = dict(d_rmst_m=round(float(d.mean()), 2), se=round(float(bs.std()), 2),
                      ci90=[round(float(np.percentile(bs, 5)), 2), round(float(np.percentile(bs, 95)), 2)],
                      d_reach_pp=round(reach_d, 1), share_faster=round(float((d < 0).mean())*100, 1),
                      share_slower=round(float((d > 0).mean())*100, 1))
    return out


def main():
    rg = sys.argv[1]; nsim = int(sys.argv[2])
    t0 = time.time()
    res = dict(regime=rg, nsim=nsim, check=None)
    if "--check" in sys.argv:
        res["check"] = check_bitgleich(); print("Bitgleich:", res["check"], flush=True)
    dc0, dw0, apy, days, C, W = tp.build_cells(None)
    TM = apy / 12.0
    reg = "IS" if rg == "null" else rg
    dc, dw = tp.apply_regime(dc0, dw0, days, reg)
    pol = policies(dc, dw, f"fncheck|{rg}")
    sims = tp.simulate_fleet_calendar(pol, G, TM, B=BUDGET, Tmax_m=TMAX_M, nsim=nsim, seed=SEED, max_outlay=CAP_OUT,
                                      marks_m=MARKS, return_raw=True, path_demean=(rg == "null"),
                                      day_stop=tp.day_stop_fn("rg"))
    raw = {n: v.pop("_raw") for n, v in sims.items()}
    res["summ"] = sims
    res["paired_vs_A"] = paired(raw, TM, "A_heute") if "A_heute" in raw else {}
    res["paired_vs_C"] = paired(raw, TM, "C_d040")
    res["T_m"] = {n: [None if not np.isfinite(r["T"]) else round(float(r["T"])/TM, 2) for r in v] for n, v in raw.items()}
    res["sec"] = round(time.time() - t0, 1)
    res["stempel"] = dict(n_days=len(dc0), span=[str(days[0]), str(days[-1])], mu_IS=round(float(dc0.mean()), 3),
                          apy=round(apy, 2), TM=round(TM, 3))
    f = OUT / f"fn_tempo_{os.environ.get('VSET', 'main')}_{rg}_{nsim}.json"
    f.write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"{rg}: fertig in {res['sec']} s -> {f}", flush=True)
    for n, s in sims.items():
        print(f"  {n:13s} med {s['med_m']}  rmst {s['rmst_m']}  p10y {s['p_10y']}  p3y {s['p_3y']}  out_p90 {s['outlay_p90']}",
              flush=True)


if __name__ == "__main__":
    main()
