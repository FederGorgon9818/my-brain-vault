"""K1-Zerlegung auf Konto-Ebene: Eval Regel (A) vs Deckel 0,40 (C), Funded alte vs korrigierte Formel. Nur Kernel."""
import os, sys, numpy as np
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
os.environ.pop("VSET", None); sys.path.insert(0, SP)
import fn_tempo_check as fc
tp = fc.tp
dc0, dw0, apy, days, C, W = tp.build_cells(None)
TM = apy/12
dsf = tp.day_stop_fn("rg")
for rg in ("IS", "shrink_recent"):
    dc, dw = tp.apply_regime(dc0, dw0, days, rg)
    P = tp.L.draw_paths(len(dc), 3000, 1250, 5, 10)
    print(f"\n### {rg}")
    for tier, k in (("50k", 1), ("150k", 2)):
        T = tp.FN[tier]; ds = dsf(("FN", tier, k))
        tA = fc.fn_type(tier); tC = fc.fn_type(tier, eval_cap=0.40, fix=True)
        sA, dA = fc._cal_eval(P, dc, dw, ("FN", tA, k), ds=ds)
        sC, dC = fc._cal_eval(P, dc, dw, ("FN", tC, k), ds=ds)
        print(f"  FN {tier} k{k} Eval: Pass Regel {100*(sA==1).mean():.1f}% (Median {np.median(dA[sA==1])/TM:.1f} M)  "
              f"Deckel0,40 {100*(sC==1).mean():.1f}% (Median {np.median(dC[sC==1])/TM:.1f} M)")
        fo = fc.run_funded_fn_x(P, dc, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds, fix=False)
        fn = fc.run_funded_fn_x(P, dc, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds, fix=True)
        fd = fc.run_funded_fn_x(P, dc, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds, fix=True, theta=1.0, lock_first=True)
        for nm, f in (("alt", fo), ("korr", fn), ("korr+volleCaps", fd)):
            # Netto in den ersten 24 Monaten je Funded-Konto
            H24 = int(24*TM)
            print(f"    Funded {nm:15s}: Netto/Konto {f['netsum'].mean():7.0f} $  davon in 24 M {f['flow'][:, :H24].sum(1).mean():7.0f} $  "
                  f"P(>=1 Payout) {100*np.isfinite(f['t1']).mean():5.1f}%  Median t1 {np.nanmedian(f['t1'])/TM:4.1f} M  Ruin {100*f['ruin'].mean():5.1f}%  "
                  f"Payouts {f['npay'].mean():.2f}")
