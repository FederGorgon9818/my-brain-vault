"""FN-Passquote mit Consistency-Regel (Cloud-Session 29.09.2026, Scratch, aendert keine Engine-Datei).

Frage (Max 29.09.): Wie stark ueberschaetzen Workbench-P(Pass) und Buch-Rechnung (cage_policy_lib.evaluate_v2,
beide OHNE Consistency-Regel) die FN-Passquote, und was kostet der Live-Deckel (MaxRiskGuard 0,36 x Target)?

Varianten je Konto:
  A  ohne Regel            = heutiger Stand evaluate_v2 / Workbench ("FN ohne 40-%-Regel, also zu hoch")
  B  40-%-Regel ohne Deckel = FN Help Center 14298275: Ziel steigt auf "hoechster Tagesgewinn / 0,40"
                              (identisch zu tempo_plan.run_eval_fn day_cap_frac=0.40: bal >= target UND cmax <= 0,4*bal)
  C  Live-Deckel            = MaxRiskGuard: Tagesgewinn >= 0,36 x Target -> flat, Rest der Session keine Entries.
                              Tagesebene: dc -> min(dc, Deckel), dw bleibt (konservativ: ein Dip NACH dem Deckel
                              waere live nicht passiert, Beruehrungen nur ueber offenen PnL fehlen ebenfalls).
Kern: cage_policy_lib.run_account (Min-Size, Intraday-Bust, EOD-Trailing, Lock bei 0) fuer A und C,
fuer B dieselbe Schleife plus Consistency-Pruefung (Gleichheit mit run_account bei ausgeschalteter Regel geprueft,
B gegen tempo_plan.run_eval_fn gegengeprueft). Pfade: cage_policy_lib.draw_paths, Block-Bootstrap Mittel 10,
Seeds 11/23/37 (wie eval_plan.evaluate_v2), 6000 Sims, 36 Monate. Regime: Verschiebung VOR dem Deckel
(mu_ref = ungekappte Drift, Regel Statistiker 21.09.).
Validierung Tagesebene vs. Trade-Ebene: tempo_cells_cache (Gewinnstopp 1000 / 1500 je Kontraktsatz, Trades nach dem
Stopp entfallen, flat=True) gegen min(dc, Deckel) auf denselben Pfaden.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ENG = Path(os.environ.get("MAXLAB_ENGINE", "/home/user/trading-data/engine"))
sys.path.insert(0, str(ENG))
import cage_policy_lib as cpl  # noqa: E402

SEEDS = (11, 23, 37)
N_SIMS = 6000
H_MONTHS = 36
BLOCK = 10
CAP_FRAC_LIVE = 0.36   # maxlab_riskguard.cfg seit 24.09.2026 (dailyprofitcap=0.36, margin 0)
RULE_FRAC = 0.40       # FN Flex Challenge
FN = {"50k": dict(target=2500.0, dd=1500.0), "150k": dict(target=8000.0, dd=4000.0)}  # Help Center 14878751
CONFIGS = [("FN 50k", "50k", 1), ("FN 150k", "150k", 1), ("FN 150k", "150k", 2), ("FN 150k", "150k", 3)]
RECENT = "2023-08-06"


def load_book():
    st = json.loads((ENG / "book_state.json").read_text(encoding="utf-8"))
    legs = [l["name"] for l in st["legs"]]
    pbl = {l["name"]: l["params"] for l in st["legs"]}
    C, W, apy, legs2, days = cpl.load_pool(legs, pbl, None, True)
    assert list(legs2) == legs
    return C, W, apy, days, legs, pbl


def tempo_cells(legs, pbl, pstop):
    key = hashlib.sha1((json.dumps({n: pbl[n] for n in legs}, sort_keys=True)
                        + f"|pstop={pstop}|v1").encode()).hexdigest()[:12]
    f = ENG / f"tempo_cells_cache_{key}.npz"
    if not f.exists():
        return None
    z = np.load(f, allow_pickle=True)
    return z["C"], z["W"], [str(d) for d in z["days"]]


def run_account_cons(paths, dc, dw, risk, frac, target, dd, cap, horizon, rule_frac=None):
    """cage_policy_lib.run_account (dd_mode intraday, start 0, ohne Endspurt) + FN-Consistency:
    bestanden erst bei bal >= max(target, hoechster Tagesgewinn / rule_frac)."""
    n = paths.shape[0]
    bal = np.zeros(n); peak = np.zeros(n); floor = np.full(n, -float(dd))
    cmax = np.zeros(n)
    alive = np.ones(n, bool); passday = np.full(n, np.inf)
    for t in range(0, horizon):
        idx = np.flatnonzero(alive)
        if idx.size == 0:
            break
        k = paths[idx, t]
        raw = (bal[idx] - floor[idx]) * frac
        sz = np.clip((raw / risk).astype(np.int64), 1, cap)
        breach = (bal[idx] + dw[k] * sz) <= floor[idx]
        if breach.any():
            alive[idx[breach]] = False
            keep = ~breach
            idx, k, sz = idx[keep], k[keep], sz[keep]
            if idx.size == 0:
                continue
        pnl = dc[k] * sz
        bal[idx] += pnl
        cmax[idx] = np.maximum(cmax[idx], pnl)
        busted = bal[idx] <= floor[idx]
        if busted.any():
            alive[idx[busted]] = False
            keep = ~busted
            idx, pnl = idx[keep], pnl[keep]
            if idx.size == 0:
                continue
        peak[idx] = np.maximum(peak[idx], bal[idx])
        floor[idx] = np.minimum(peak[idx] - dd, 0.0)
        ok = bal[idx] >= target
        if rule_frac is not None:
            ok &= cmax[idx] <= rule_frac * np.maximum(bal[idx], 1e-9)
        won = idx[ok]
        if won.size:
            passday[won] = t
            alive[won] = False
    return passday


def regime(dc1, dw1, days, name):
    """Zellen je 1 Kontraktsatz. Verschiebung auf die UNGEKAPPTEN Zellen, Deckel kommt danach."""
    m = np.ones(len(dc1), bool)
    if name in ("recent3y", "shrink_recent"):
        m = np.array([str(d) >= RECENT for d in days])
    dc, dw = dc1[m], dw1[m]
    mu = {"IS": None, "recent3y": None, "shrink058": 0.58 * dc1.mean(),
          "shrink_recent": 0.58 * dc.mean(), "null": 0.0}[name]
    if mu is None:
        return dc, dw
    d = mu - dc.mean()
    return dc + d, np.minimum(dw + d, 0.0)


def within(pd_list, apy, months):
    lim = months * apy / 12.0
    return np.array([(x <= lim).mean() * 100 for x in pd_list])


def summarize(pd_list, apy):
    p = np.array([np.isfinite(x).mean() * 100 for x in pd_list])
    med = [np.median(x[np.isfinite(x)]) / apy * 365.25 for x in pd_list if np.isfinite(x).any()]
    return p, (float(np.mean(med)) if med else None)


def main():
    C, W, apy, days, legs, pbl = load_book()
    dc1_all, dw1_all = C.sum(1), W.sum(1)
    horizon = int(round(H_MONTHS * apy / 12.0))
    out = {"book": legs, "n_days": len(days), "span": [str(days[0]), str(days[-1])], "apy": apy,
           "mean_dc_IS": float(dc1_all.mean()), "settings": dict(seeds=SEEDS, n_sims=N_SIMS, horizon_m=H_MONTHS,
           block_mean=BLOCK, cap_frac_live=CAP_FRAC_LIVE, rule_frac=RULE_FRAC), "rows": [], "checks": {}}
    regimes = ["IS", "shrink058", "recent3y", "shrink_recent", "null"]

    # --- Pruefung 1: eigener Kern ohne Regel == cage_policy_lib.run_account (bit-gleich)
    paths = cpl.draw_paths(len(dc1_all), 2000, horizon, 11, BLOCK)
    risk = float(np.percentile(np.abs(dw1_all[dw1_all < 0]), 50))
    a_ref = cpl.run_account(paths, dc1_all, dw1_all, risk, 0, 0.01, 2500.0, 1500.0, 40, "intraday", horizon)
    a_own = run_account_cons(paths, dc1_all, dw1_all, risk, 0.01, 2500.0, 1500.0, 40, horizon, None)
    out["checks"]["kern_gleich_run_account"] = bool(np.array_equal(a_ref, a_own))

    # --- Pruefung 2: Variante B gegen tempo_plan.run_eval_fn (gleiche Pfade)
    try:
        import tempo_plan as tp
        st_tp, _ = tp.run_eval_fn(paths, dc1_all, dw1_all, 2500.0, 1500.0, k=1, day_cap_frac=0.40)
        b_own = run_account_cons(paths, dc1_all, dw1_all, risk, 0.01, 2500.0, 1500.0, 40, horizon, RULE_FRAC)
        out["checks"]["B_vs_tempo_plan_pp"] = [round(float((st_tp == 1).mean() * 100), 2),
                                               round(float(np.isfinite(b_own).mean() * 100), 2)]
    except Exception as e:  # tempo_plan nicht importierbar -> nur vermerken
        out["checks"]["B_vs_tempo_plan_pp"] = f"nicht geprueft: {e!r}"

    for label, tier, k in CONFIGS:
        target, dd = FN[tier]["target"], FN[tier]["dd"]
        cap_usd = CAP_FRAC_LIVE * target
        for rg in regimes:
            dc1, dw1 = regime(dc1_all, dw1_all, days, rg)
            dc, dw = dc1 * k, dw1 * k
            dcC = np.minimum(dc, cap_usd)
            neg = np.abs(dw[dw < 0]); risk = float(np.percentile(neg, 50)) if neg.size else 1.0
            res = {"A": [], "B": [], "C": []}
            for s in SEEDS:
                P = cpl.draw_paths(len(dc), N_SIMS, horizon, s, BLOCK)
                res["A"].append(cpl.run_account(P, dc, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon))
                res["B"].append(run_account_cons(P, dc, dw, risk, 0.01, target, dd, 40, horizon, RULE_FRAC))
                res["C"].append(cpl.run_account(P, dcC, dw, risk, 0, 0.01, target, dd, 40, "intraday", horizon))
            row = {"konto": label, "k": k, "regime": rg, "deckel_usd": cap_usd,
                   "tage_ueber_deckel_pct": round(float((dc > cap_usd).mean() * 100), 2),
                   "tage_ueber_40pct_pct": round(float((dc > RULE_FRAC * target).mean() * 100), 2),
                   "kappung_usd_je_tag": round(float(np.maximum(dc - cap_usd, 0).mean()), 2),
                   "mean_dc": round(float(dc.mean()), 2)}
            ps = {}
            for v in "ABC":
                p, med = summarize(res[v], apy)
                ps[v] = p
                row[f"{v}_pass"] = round(float(p.mean()), 2)
                row[f"{v}_sd"] = round(float(p.std(ddof=1)), 2)
                row[f"{v}_med_tage"] = round(med, 1) if med else None
                for mo in (6, 12):
                    w = within(res[v], apy, mo)
                    ps[f"{v}{mo}"] = w
                    row[f"{v}_pass_{mo}m"] = round(float(w.mean()), 2)
            for a, b in (("C", "A"), ("B", "A"), ("C", "B")):
                d = ps[a] - ps[b]
                row[f"d_{a}{b}"] = round(float(d.mean()), 2)
                row[f"d_{a}{b}_sd"] = round(float(d.std(ddof=1)), 2)
            for mo in (6, 12):
                for a, b in (("C", "A"), ("C", "B")):
                    d = ps[f"{a}{mo}"] - ps[f"{b}{mo}"]
                    row[f"d_{a}{b}_{mo}m"] = round(float(d.mean()), 2)
                    row[f"d_{a}{b}_{mo}m_sd"] = round(float(d.std(ddof=1)), 2)
            # Sanity: C mit eingeschalteter Regel muss identisch sein (Deckel < 40 %-Linie)
            if rg == "IS":
                P = cpl.draw_paths(len(dc), N_SIMS, horizon, SEEDS[0], BLOCK)
                cc = run_account_cons(P, dcC, dw, risk, 0.01, target, dd, 40, horizon, RULE_FRAC)
                row["C_regel_redundant"] = bool(np.array_equal(cc, res["C"][0]))
            out["rows"].append(row)
            print(f"{label} k{k} {rg:13s} A {row['A_pass']:6.2f}  B {row['B_pass']:6.2f}  C {row['C_pass']:6.2f}"
                  f"  C-A {row['d_CA']:+6.2f}±{row['d_CA_sd']:.2f}  C-B {row['d_CB']:+6.2f}±{row['d_CB_sd']:.2f}"
                  f"  Tage>Deckel {row['tage_ueber_deckel_pct']:5.2f}%", flush=True)

    # --- Validierung Tagesebene vs. Trade-Ebene (gleiche Pfade, IS)
    val = []
    for pstop, label, tier, k in ((1000, "FN 50k", "50k", 1), (1500, "FN 150k", "150k", 2), (500, "FN 50k", "50k", 1)):
        tc = tempo_cells(legs, pbl, pstop)
        if tc is None:
            val.append({"pstop": pstop, "status": "Cache fehlt"}); continue
        Ct, Wt, dts = tc
        if [str(d) for d in days] != dts:
            val.append({"pstop": pstop, "status": "Tage passen nicht"}); continue
        target, dd = FN[tier]["target"], FN[tier]["dd"]
        cap_usd = pstop * k
        dc, dw = dc1_all * k, dw1_all * k
        dct, dwt = np.minimum(Ct.sum(1) * k, cap_usd), Wt.sum(1) * k
        neg = np.abs(dw[dw < 0]); risk = float(np.percentile(neg, 50))
        pday, ptr = [], []
        for s in SEEDS:
            P = cpl.draw_paths(len(dc), N_SIMS, horizon, s, BLOCK)
            pday.append(np.isfinite(cpl.run_account(P, np.minimum(dc, cap_usd), dw, risk, 0, 0.01, target, dd, 40,
                                                   "intraday", horizon)).mean() * 100)
            ptr.append(np.isfinite(cpl.run_account(P, dct, dwt, risk, 0, 0.01, target, dd, 40,
                                                  "intraday", horizon)).mean() * 100)
        d = np.array(ptr) - np.array(pday)
        val.append({"konto": label, "k": k, "deckel_usd": cap_usd, "tagesebene": round(float(np.mean(pday)), 2),
                    "tradeebene": round(float(np.mean(ptr)), 2), "diff_trade_minus_tag": round(float(d.mean()), 2),
                    "diff_sd": round(float(d.std(ddof=1)), 2)})
        print("Validierung", val[-1], flush=True)
    out["validierung_tag_vs_trade"] = val
    print("Checks:", out["checks"])
    dst = Path(os.environ.get("OUT", "fn_consistency_results.json"))
    dst.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("geschrieben:", dst)


if __name__ == "__main__":
    main()
