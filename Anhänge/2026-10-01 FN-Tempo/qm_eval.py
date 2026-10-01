"""Eval-Seite: Regel allein vs. Deckel 0,36/0,40 (FN 50k k1, FN 150k k2/k3), RiskGuard-Stopp rg. Plus Drift-Verlust der Kappung."""
import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad")
import fn_tempo_check as F
tp = F.tp; L = tp.L
dc0, dw0, apy, days, C, W = tp.build_cells(None); TM = apy/12
for c in (900, 1000, 1440, 1600):
    print(f"cap {c}: P(dc>c) {100*(dc0>c).mean():.2f}%  drift loss E[(dc-c)+] {np.maximum(dc0-c,0).mean():.2f} $/Tag = {100*np.maximum(dc0-c,0).mean()/dc0.mean():.1f}% von mu")
N, H = 3000, 1250
for reg in ("IS", "shrink058"):
    dc, dw = tp.apply_regime(dc0, dw0, days, reg)
    pe = L.draw_paths(len(dc), N, H, 31, 10)
    print(f"## {reg}")
    for tier, k in (("50k", 1), ("150k", 2), ("150k", 3)):
        T = tp.FN[tier]; ds = tp.day_stop_fn("rg")(("FN", tier, k))
        out = []
        for lab, ec in (("Regel", None), ("d036", 0.36), ("d040", 0.40)):
            dce = dc if ec is None else np.minimum(dc, ec*T["target"]/k)
            st, d = tp.run_eval_fn(pe, dce, dw, T["target"], T["dd"], k=k, ds=ds)
            ok = st == 1
            out.append(f"{lab}: pass {100*ok.mean():.1f}% med {np.median(d[ok])/TM:.2f}M")
        print(f"  FN{tier} k{k}: " + " | ".join(out))
