"""Pool-Mechanik FN Funded: C (sofort) vs D (Lock + volle Caps) vs Zerlegung, plus MLL-Reset-Lesarten.
Nur Lesen aus der Engine, rechnet im Scratchpad."""
import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad")
import fn_tempo_check as F
tp = F.tp; L = tp.L

def fund_reset(paths, dc, dw, dd, cap, bench, k=1, split=0.95, need_days=5, lock_level=100.0, max_pays=4,
               min_gross=250.0, ds=None, theta=None, lock_first=False, reset=None):
    """wie run_funded_fn_x(fix=True), plus MLL-Lesart nach der 1. Auszahlung:
    reset='lock'  -> Floor springt auf Start+100 und bleibt dort (ungünstige Lesart R2)
    reset='fresh' -> Trailing startet neu ab Saldo nach Auszahlung (peak := bal), Lock bei +100 (günstige Lesart R1)"""
    n, H = paths.shape
    bal = np.zeros(n); peak = np.zeros(n); floor = np.full(n, -float(dd)); base = np.zeros(n)
    alive = np.ones(n, bool); npay = np.zeros(n, np.int64); netsum = np.zeros(n); hardlock = np.zeros(n, bool)
    cg = np.zeros(n, np.int64); life = np.full(n, float(H)); t1 = np.full(n, np.nan)
    ruin = np.zeros(n, bool); gross = np.zeros(n)
    for t in range(H):
        idx = np.flatnonzero(alive)
        if idx.size == 0: break
        j = paths[idx, t]
        c_, w_ = tp._stop_day(dc[j], dw[j], k, bal[idx], floor[idx], ds)
        br = (bal[idx] + w_) <= floor[idx]
        if br.any():
            b = idx[br]; ruin[b] = True; alive[b] = False; life[b] = t+1
            idx = idx[~br]; c_ = c_[~br]
            if idx.size == 0: continue
        pnl = c_; bal[idx] += pnl
        br = bal[idx] <= floor[idx]
        if br.any():
            b = idx[br]; ruin[b] = True; alive[b] = False; life[b] = t+1
            idx = idx[~br]; pnl = pnl[~br]
            if idx.size == 0: continue
        peak[idx] = np.maximum(peak[idx], bal[idx])
        floor[idx] = np.where(hardlock[idx], lock_level, np.minimum(peak[idx]-dd, lock_level))
        cg[idx] += (pnl >= bench)
        prof = bal[idx] - base[idx]
        w = np.minimum(np.minimum(0.5*np.maximum(prof, 0.0), cap), bal[idx]-lock_level)
        ok = (w >= min_gross) & (cg[idx] >= need_days)
        if theta is not None: ok &= w >= theta*cap
        if lock_first: ok &= (npay[idx] > 0) | (floor[idx] >= lock_level)
        pay = idx[ok]
        if pay.size:
            wp = w[ok]; netsum[pay] += wp*split; gross[pay] += wp; bal[pay] -= wp; base[pay] = bal[pay]
            newf = pay[npay[pay] == 0]
            if newf.size:
                t1[newf] = t+1
                if reset == "lock":
                    hardlock[newf] = True; floor[newf] = lock_level
                elif reset == "fresh":
                    peak[newf] = bal[newf]; floor[newf] = np.minimum(peak[newf]-dd, lock_level)
            npay[pay] += 1; cg[pay] = 0
            fin = pay[npay[pay] >= max_pays]
            if fin.size: alive[fin] = False; life[fin] = t+1
    return dict(netsum=netsum, life=life, t1=t1, npay=npay, ruin=ruin, gross=gross)

def stats(r, TM):
    np1 = r["npay"] >= 1
    return dict(p_pay1=round(100*np1.mean(), 1), net=round(r["netsum"].mean()), net_if=round(r["netsum"][np1].mean()) if np1.any() else 0,
                t1_med_m=round(float(np.nanmedian(r["t1"]))/TM, 1) if np1.any() else None,
                npay=round(r["npay"].mean(), 2), gross_per_pay=round(r["gross"].sum()/max(r["npay"].sum(), 1)),
                p_ruin=round(100*r["ruin"].mean(), 1), ruin_before_1=round(100*(r["ruin"] & ~np1).mean(), 1),
                life_m=round(r["life"].mean()/TM, 1), net_per_slotyear=round(r["netsum"].mean()/(r["life"].mean()/TM/12)))

if __name__ == "__main__":
    dc0, dw0, apy, days, C, W = tp.build_cells(None)
    TM = apy/12
    print("dc IS: mean %.2f sd %.1f | P(dc>=125) %.3f P(dc>=83.3) %.3f P(dc>=200) %.3f P(dc>=1000) %.4f P(dc>=1440) %.4f P(dc>=1600) %.4f max %.0f" % (
        dc0.mean(), dc0.std(), (dc0>=125).mean(), (dc0>=250/3).mean(), (dc0>=200).mean(), (dc0>=1000).mean(), (dc0>=1440).mean(), (dc0>=1600).mean(), dc0.max()))
    N, H = 2000, 1250
    for reg in sys.argv[1].split(","):
        dc, dw = tp.apply_regime(dc0, dw0, days, reg)
        pf = L.draw_paths(len(dc), N, H, 23, 10)
        print(f"\n### {reg}  mu {dc.mean():.2f}")
        for tier, k in (("50k", 1), ("150k", 2), ("150k", 3)):
            T = tp.FN[tier]; ds = tp.day_stop_fn("rg")(("FN", tier, k))
            for name, kw in (("C", {}), ("D", dict(theta=1.0, lock_first=True)), ("Dl", dict(lock_first=True)),
                             ("Dc", dict(theta=1.0)), ("C_R2lock", dict(reset="lock")), ("D_R2lock", dict(theta=1.0, lock_first=True, reset="lock")),
                             ("C_R1fresh", dict(reset="fresh"))):
                r = fund_reset(pf, dc, dw, T["dd"], T["cap"], T["bench"], k=k, ds=ds, **kw)
                print(f"  FN{tier} k{k} {name:10s}", stats(r, TM))
