"""Statistiker 29.09.: Stichproben-Unsicherheit der Historie fuer die FN-Deltas (C-A, C-B, B-A).
Aeusserer stationaerer Block-Bootstrap der Tageshistorie (bzw. der juengsten 455 Tage fuer recent-Regime),
innen dieselbe MC wie fn_consistency_passquote.py (CRN ueber A/B/C und ueber Konten), 1 Seed je Replikat.
Nur lesen, keine Engine-Datei."""
import argparse, json, sys, time
from pathlib import Path
import numpy as np, pandas as pd
SCR = Path(__file__).resolve().parent
ENG = Path("/home/user/trading-data/engine"); sys.path.insert(0, str(ENG)); sys.path.insert(0, str(SCR))
import cage_policy_lib as cpl
from fn_consistency_passquote import run_account_cons, FN, CAP_FRAC_LIVE, RULE_FRAC, RECENT

CONFIGS = [("50k", 1), ("150k", 2), ("150k", 3)]


def load():
    st = json.loads((ENG / "book_state.json").read_text(encoding="utf-8"))
    legs = [l["name"] for l in st["legs"]]; pbl = {l["name"]: l["params"] for l in st["legs"]}
    C, W, apy, _, days = cpl.load_pool(legs, pbl, None, True)
    return C.sum(1), W.sum(1), float(apy), np.array([str(d) for d in days])


def shift(dc1, dw1, mu):
    d = mu - dc1.mean()
    return dc1 + d, np.minimum(dw1 + d, 0.0)


def eval_abc(dc1, dw1, P, horizon, apy):
    out = {}
    n = P.shape[0]
    lims = {"all": None, "6m": 6 * apy / 12.0, "12m": 12 * apy / 12.0}
    for tier, k in CONFIGS:
        target, dd = FN[tier]["target"], FN[tier]["dd"]
        cap = CAP_FRAC_LIVE * target
        dc, dw = dc1 * k, dw1 * k
        dcC = np.minimum(dc, cap)
        neg = np.abs(dw[dw < 0]); risk = float(np.percentile(neg, 50)) if neg.size else 1.0
        a = cpl.run_account(P, dc, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon)
        b = run_account_cons(P, dc, dw, risk, 0.01, target, dd, 40, horizon, RULE_FRAC)
        c = cpl.run_account(P, dcC, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon)
        res = {"n_gt_cap": int((dc > cap).sum()), "n_gt_rule": int((dc > RULE_FRAC * target).sum()),
               "kapp": float(np.maximum(dc - cap, 0).mean()), "mean": float(dc.mean())}
        for lab, lim in lims.items():
            f = (lambda x: np.isfinite(x)) if lim is None else (lambda x, L=lim: x <= L)
            pa, pb, pc = f(a), f(b), f(c)
            for v, x in (("A", pa), ("B", pb), ("C", pc)):
                res[f"{v}_{lab}"] = float(x.mean() * 100)
            for nm, x, y in (("CA", pc, pa), ("CB", pc, pb), ("BA", pb, pa)):
                d = x.mean() - y.mean()
                res[f"d{nm}_{lab}"] = float(d * 100)
                res[f"v{nm}_{lab}"] = float(((x != y).mean() - d * d) / n * 1e4)  # MC-Varianz des gepaarten Deltas in pp^2
        out[f"{tier}_k{k}"] = res
    return out


def one_rep(dc1, dw1, rec, apy, horizon, r, L, ninner):
    N, Nr = len(dc1), int(rec.sum())
    res = {}
    idx = cpl.draw_paths(N, 1, N, 50000 + r, L)[0]
    d1, w1 = dc1[idx], dw1[idx]
    P = cpl.draw_paths(N, ninner, horizon, 90000 + r, 10)
    res["IS"] = eval_abc(d1, w1, P, horizon, apy)
    s1, sw = shift(d1, w1, 0.58 * d1.mean())
    res["shrink058"] = eval_abc(s1, sw, P, horizon, apy)
    dcr, dwr = dc1[rec], dw1[rec]
    idr = cpl.draw_paths(Nr, 1, Nr, 70000 + r, L)[0]
    d2, w2 = dcr[idr], dwr[idr]
    P2 = cpl.draw_paths(Nr, ninner, horizon, 110000 + r, 10)
    res["recent3y"] = eval_abc(d2, w2, P2, horizon, apy)
    s2, sw2 = shift(d2, w2, 0.58 * d2.mean())
    res["shrink_recent"] = eval_abc(s2, sw2, P2, horizon, apy)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=float, default=10.0)
    ap.add_argument("--R", type=int, default=10)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--ninner", type=int, default=4000)
    ap.add_argument("--out", default="outer.json")
    a = ap.parse_args()
    dc1, dw1, apy, days = load()
    rec = days >= RECENT
    horizon = int(round(36 * apy / 12.0))
    reps = []
    t0 = time.time()
    for r in range(a.start, a.start + a.R):
        reps.append(one_rep(dc1, dw1, rec, apy, horizon, r, a.L, a.ninner))
        if (r - a.start) % 10 == 0:
            print(r, round(time.time() - t0, 1), flush=True)
            (SCR / a.out).write_text(json.dumps({"L": a.L, "ninner": a.ninner, "reps": reps}))
    (SCR / a.out).write_text(json.dumps({"L": a.L, "ninner": a.ninner, "reps": reps}))
    print("fertig", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
