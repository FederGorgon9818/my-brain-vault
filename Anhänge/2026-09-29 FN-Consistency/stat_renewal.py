"""Statistiker 29.09.: grobe Zeit-bis-funded-Pruefung fuer K2 (B Regel vs. C Deckel), sequentieller Nachkauf
sofort nach Bust, Versuche i.i.d. aus dem simulierten Versuchs-Pool (ignoriert Regime-Kontinuitaet zwischen
Versuchen, also nur Richtung). Kern: tempo_plan.run_eval_fn (k fest = Min-Size, wie im Original gegengeprueft)."""
import sys
from pathlib import Path
import numpy as np
SCR = Path(__file__).resolve().parent; sys.path.insert(0, str(SCR))
from stat_outer import load, shift
import cage_policy_lib as cpl
import tempo_plan as tp
from fn_consistency_passquote import FN, RECENT

dc1, dw1, apy, days = load()
H = int(round(36 * apy / 12.0))
rec = days >= RECENT
regs = {"IS": (dc1, dw1), "shrink_recent": shift(dc1[rec], dw1[rec], 0.58 * dc1[rec].mean()),
        "null": shift(dc1, dw1, 0.0), "recent3y": (dc1[rec], dw1[rec])}
rng = np.random.default_rng(5)
for tier, k in (("50k", 1), ("150k", 3), ("150k", 2)):
    T = FN[tier]; cap = 0.36 * T["target"]
    for rg, (d1, w1) in regs.items():
        dc, dw = d1 * k, w1 * k
        row = []
        for v in "ABC":
            sts, dys = [], []
            for s in (11, 23, 37):
                P = cpl.draw_paths(len(dc), 6000, H, s, 10)
                if v == "A":
                    st, dd_ = tp.run_eval_fn(P, dc, dw, T["target"], T["dd"], k=1, day_cap_frac=None)
                elif v == "B":
                    st, dd_ = tp.run_eval_fn(P, dc, dw, T["target"], T["dd"], k=1, day_cap_frac=0.40)
                else:
                    st, dd_ = tp.run_eval_fn(P, np.minimum(dc, cap), dw, T["target"], T["dd"], k=1, day_cap_frac=None)
                sts.append(st); dys.append(dd_)
            st = np.concatenate(sts); dd_ = np.concatenate(dys)
            p = (st == 1).mean(); ED = dd_.mean()
            # sequentielle Nachkauf-Simulation
            M = 20000; lim12 = 12 * apy / 12; lim6 = 6 * apy / 12
            t = np.zeros(M); done = np.full(M, np.inf); buys12 = np.zeros(M)
            active = np.ones(M, bool)
            for _ in range(60):
                ia = np.flatnonzero(active)
                if ia.size == 0: break
                j = rng.integers(len(st), size=ia.size)
                buys12[ia] += (t[ia] < lim12)
                fin = st[j] == 1
                done[ia[fin]] = t[ia[fin]] + dd_[j[fin]]
                t[ia] += dd_[j]
                active[ia[fin]] = False
                active &= t < 2 * lim12  # nach 24 M abbrechen
            row.append((v, p * 100, ED / apy * 12, ED / p / apy * 12, (done <= lim6).mean() * 100, (done <= lim12).mean() * 100,
                        buys12.mean(), (st == 0).mean() * 100))
        print(f"{tier} k{k} {rg:13s} " + " | ".join(
            f"{v}: p36 {p:5.1f} E[D] {ed:4.1f}M E[T]{et:5.1f}M F6 {f6:5.1f} F12 {f12:5.1f} buys12 {b:4.2f} offen36 {o:4.1f}"
            for v, p, ed, et, f6, f12, b, o in row), flush=True)
