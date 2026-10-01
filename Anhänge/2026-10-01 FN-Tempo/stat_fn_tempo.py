"""Statistiker 01.10.: gepaarte Deltas + Rauschmass auf den gespeicherten Pro-Sim-Daten (fnrun/*.json). Nur lesen."""
import json, sys
import numpy as np
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
REG = [("IS",600),("shrink058",400),("recent3y",400),("shrink_recent",400)]
PAIRS = [("B_d036","C_d040"),("E_d040_fcap","C_d040"),("D_d040_lock","C_d040"),("C3_d040_k3","C_d040"),
         ("D3_lock_k3","D_d040_lock"),("D3_lock_k3","C3_d040_k3"),("A_heute","C_d040")]
TMAX = 120.0
rng = np.random.default_rng(2026)
def arr(r, v):
    x = np.array([np.nan if t is None else t for t in r["T_m"][v]], float)
    reach = np.isfinite(x)
    return np.where(reach, np.minimum(x, TMAX), TMAX), reach
out = {}
for rg, n in REG:
    r = json.load(open(f"{SP}/fnrun/fn_tempo_{rg}_{n}.json"))
    print(f"\n### {rg} n={n}")
    print(f"{'Paar':28s} dRMST  SE    90%-CI           z    | 5-Chunk-SD/sqrt5 | dReach pp  SE    z   | b(X schneller) c(X langsamer)")
    for x, ref in PAIRS:
        tx, rx = arr(r, x); tr, rr = arr(r, ref)
        d = tx - tr
        bs = d[rng.integers(n, size=(4000, n))].mean(1)
        se = bs.std(); lo, hi = np.percentile(bs, [5, 95])
        ch = np.array([c.mean() for c in np.array_split(d, 5)])
        chse = ch.std(ddof=1)/np.sqrt(5)
        b = int((rx & ~rr).sum()); c = int((~rx & rr).sum())
        dr = (b - c)/n*100
        se_r = np.sqrt((b + c) - (b - c)**2/n)/n*100
        zr = dr/se_r if se_r > 0 else float('nan')
        fast = (d < 0).mean()*100; slow = (d > 0).mean()*100
        print(f"{x+'-'+ref:28s} {d.mean():+6.2f} {se:4.2f} [{lo:+6.2f};{hi:+6.2f}] {d.mean()/se:+5.1f} | {chse:4.2f} (chunks {np.round(ch,1)}) | {dr:+5.1f} {se_r:4.1f} {zr:+5.1f} | {b} {c} | schneller {fast:.0f}% langsamer {slow:.0f}%")
        out[f"{rg}|{x}-{ref}"] = dict(d=float(d.mean()), se=float(se), ci90=[float(lo), float(hi)], dreach=dr, se_reach=se_r)
json.dump(out, open(f"{SP}/stat_fn_tempo_pairs.json","w"), indent=1)
