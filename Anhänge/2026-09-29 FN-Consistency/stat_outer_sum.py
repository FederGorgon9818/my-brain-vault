import json, sys
import numpy as np
orig = {(r["konto"].split()[1] + "_k" + str(r["k"]), r["regime"]): r for r in json.load(open("fn_consistency_results.json"))["rows"]}
def pt(key, rg, m):
    r = orig[(key, rg)]
    nm, lab = m.split("_")
    base = f"d_{nm[1:]}" if lab == "all" else f"d_{nm[1:]}_{lab}"
    if base in r: return r[base]
    # B-A 6m/12m und C-A 6m nicht im Original: aus Niveaus
    v1, v2 = nm[1], nm[2]
    suf = "" if lab == "all" else f"_{lab}"
    return round(r[f"{v1}_pass{suf}"] - r[f"{v2}_pass{suf}"], 2)
sets = {"L10": ["outer_L10_a.json", "outer_L10_b.json"], "L30": ["outer_L30.json"]}
mets = ["dCA_all", "dCA_12m", "dBA_all", "dCB_all", "dCB_6m", "dCB_12m"]
for tag, files in sets.items():
    reps = sum((json.load(open(f))["reps"] for f in files), [])
    print(f"\n######## Outer-Bootstrap {tag}, R={len(reps)}")
    for rg in ("IS", "shrink058", "recent3y", "shrink_recent"):
        for key in ("50k_k1", "150k_k3", "150k_k2"):
            X = [r[rg][key] for r in reps]
            ngt = np.array([x["n_gt_cap"] for x in X])
            line = f"{rg:13s} {key:8s} n>Deckel p10/50/90 {np.percentile(ngt,10):.0f}/{np.percentile(ngt,50):.0f}/{np.percentile(ngt,90):.0f} |"
            for m in mets:
                th = np.array([x[m] for x in X]); vmc = np.array([x["v" + m[1:]] for x in X])
                sdt = th.std(ddof=1); sdh = np.sqrt(max(sdt**2 - vmc.mean(), 0.0))
                adj = th.mean() + (th - th.mean()) * (sdh / sdt if sdt > 0 else 0)
                p = pt(key, rg, m)
                lo, hi = np.percentile(adj, [5, 95])
                same = (np.sign(th) == np.sign(p)).mean() * 100 if p != 0 else float("nan")
                line += f" {m} {p:+.2f} [{lo:+.1f},{hi:+.1f}] sdH {sdh:.2f} sign {same:.0f}% |"
            print(line)
