import json, glob, numpy as np
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
rng = np.random.default_rng(11)
for f in sorted(glob.glob(f"{SP}/fnrun_decomp/fn_tempo_decomp_*.json")):
    r = json.load(open(f)); n = r["nsim"]; rg = r["regime"]
    if rg == "null":
        continue
    print(f"\n### {rg} n={n}")
    T = {v: np.array([120.0 if t is None else min(t, 120.0) for t in r["T_m"][v]]) for v in r["T_m"]}
    R = {v: np.array([t is not None for t in r["T_m"][v]]) for v in r["T_m"]}
    for v, s in r["summ"].items():
        line = f"  {v:13s} RMST {s['rmst_m']:6.1f} p10y {s['p_10y']:5.1f} econ {s['p_econ_dead']:5.1f} (t_med {s['econ_dead_med_m']}) net24 {s['net_med_24m']:6d} net36 {s['net_med_36m']:6d}"
        if v != "C_d040":
            d = T[v] - T["C_d040"]; bs = d[rng.integers(n, size=(3000, n))].mean(1)
            b = int((R[v] & ~R["C_d040"]).sum()); c = int((~R[v] & R["C_d040"]).sum())
            ser = np.sqrt((b + c) - (b - c) ** 2 / n) / n * 100
            line += f" | vs C dRMST {d.mean():+5.2f} [{np.percentile(bs,5):+5.2f};{np.percentile(bs,95):+5.2f}] z {d.mean()/bs.std():+5.1f}  dReach {(b-c)/n*100:+5.1f}pp (SE {ser:.1f})"
        print(line)
    if "Dc_capsonly" in T:
        print("  D == Dc (alle Sims gleich)?", bool(np.array_equal(T["D_d040_lock"], T["Dc_capsonly"])))
