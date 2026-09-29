"""Statistiker 29.09.: Jahres-Jackknife + Leave-one-big-day-out fuer die FN-Deltas, gleiche MC wie das Original
(Seeds 11/23/37, 6000 Sims, Block 10, CRN). Plus MC-Standardfehler des gepaarten Deltas aus der Diskordanz
(McNemar) ueber alle 18.000 Pfade statt Seed-sd mit df=2."""
import json, sys, time
from pathlib import Path
import numpy as np
SCR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCR))
from stat_outer import load, shift, CONFIGS
import cage_policy_lib as cpl
from fn_consistency_passquote import run_account_cons, FN, CAP_FRAC_LIVE, RULE_FRAC

SEEDS = (11, 23, 37); NS = 6000


def run(dc1, dw1, horizon, apy):
    """Gepoolte Ergebnisse ueber 3 Seeds (18.000 Pfade), CRN ueber A/B/C."""
    acc = {}
    lims = {"all": None, "6m": 6 * apy / 12.0, "12m": 12 * apy / 12.0}
    per_seed = {}
    for s in SEEDS:
        P = cpl.draw_paths(len(dc1), NS, horizon, s, 10)
        for tier, k in CONFIGS:
            target, dd = FN[tier]["target"], FN[tier]["dd"]
            cap = CAP_FRAC_LIVE * target
            dc, dw = dc1 * k, dw1 * k
            dcC = np.minimum(dc, cap)
            neg = np.abs(dw[dw < 0]); risk = float(np.percentile(neg, 50))
            a = cpl.run_account(P, dc, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon)
            b = run_account_cons(P, dc, dw, risk, 0.01, target, dd, 40, horizon, RULE_FRAC)
            c = cpl.run_account(P, dcC, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon)
            key = f"{tier}_k{k}"
            acc.setdefault(key, {"a": [], "b": [], "c": []})
            acc[key]["a"].append(a); acc[key]["b"].append(b); acc[key]["c"].append(c)
    out = {}
    for key, v in acc.items():
        a, b, c = (np.concatenate(v[x]) for x in "abc")
        n = len(a); r = {}
        for lab, lim in lims.items():
            f = (lambda x: np.isfinite(x)) if lim is None else (lambda x, L=lim: x <= L)
            pa, pb, pc = f(a), f(b), f(c)
            for vv, x in (("A", pa), ("B", pb), ("C", pc)):
                r[f"{vv}_{lab}"] = float(x.mean() * 100)
            for nm, x, y in (("CA", pc, pa), ("CB", pc, pb), ("BA", pb, pa)):
                d = x.mean() - y.mean()
                r[f"d{nm}_{lab}"] = float(d * 100)
                r[f"se{nm}_{lab}"] = float(np.sqrt(((x != y).mean() - d * d) / n) * 100)
                # Seed-sd zum Vergleich
                ds = [(f(cc) .mean() - f(yy).mean()) * 100 for cc, yy in zip(
                    *( (v["c"] if nm[0] == "C" else v["b"]), (v["a"] if nm[1] == "A" else v["b"]) ))]
                r[f"seedsd{nm}_{lab}"] = float(np.std(ds, ddof=1))
        out[key] = r
    return out


def main():
    dc1, dw1, apy, days = load()
    horizon = int(round(36 * apy / 12.0))
    years = np.array([d[:4] for d in days])
    res = {"base": {}, "jack": {}, "loo_bigday": {}}
    t0 = time.time()
    for rg in ("IS", "shrink058"):
        f = (lambda d, w: (d, w)) if rg == "IS" else (lambda d, w: shift(d, w, 0.58 * d.mean()))
        res["base"][rg] = run(*f(dc1, dw1), horizon, apy)
        print("base", rg, round(time.time() - t0, 1), flush=True)
        res["jack"][rg] = {}
        for y in sorted(set(years)):
            m = years != y
            res["jack"][rg][y] = run(*f(dc1[m], dw1[m]), horizon, apy)
            print("jack", rg, y, round(time.time() - t0, 1), flush=True)
    for i in np.flatnonzero(dc1 > 900):
        m = np.ones(len(dc1), bool); m[i] = False
        res["loo_bigday"][str(days[i])] = run(dc1[m], dw1[m], horizon, apy)
        print("loo", days[i], round(time.time() - t0, 1), flush=True)
    (SCR / "jack.json").write_text(json.dumps(res))
    print("fertig", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
