"""Gepaarte SE fuer Plan-Tod-Differenzen: Differenz aus Vollzaehlung (summ), Diskordanz aus Nachlauf (exakt oder Stichprobe)."""
import json, sys, numpy as np
from math import sqrt
SP = "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad"
NS = {"IS": 600, "shrink058": 400, "recent3y": 400, "shrink_recent": 400}
for rg in sys.argv[1:]:
    e = json.load(open(f"{SP}/stat_rerun/econ_{rg}.json")); s = json.load(open(f"{SP}/fnrun/fn_tempo_{rg}_{NS[rg]}.json"))["summ"]
    n0, nu, ns = e["n_orig"], e["n_union"], len(e["sel"]); V = e["var"]
    print(f"\n### {rg}: {'exakt' if nu == ns else f'Stichprobe {ns}/{nu}'}")
    for a, b in [("D_d040_lock","C_d040"),("C3_d040_k3","C_d040"),("D3_lock_k3","D_d040_lock"),("D3_lock_k3","C_d040")]:
        ka = round(s[a]["p_econ_dead"] * n0 / 100); kb = round(s[b]["p_econ_dead"] * n0 / 100)
        d = (ka - kb) / n0
        ea = np.array([x["econ"] for x in V[a]]); eb = np.array([x["econ"] for x in V[b]])
        disc = ((ea != eb).sum() / ns) * (nu / n0)
        var = max(disc - d * d, 1e-12); se = sqrt(var / n0)
        # Unsicherheit der Diskordanz selbst (Poisson auf Zaehlung) -> SE-Spanne
        m = (ea != eb).sum()
        lo_m, hi_m = max(m - 1.645*sqrt(m), 0.5), m + 1.645*sqrt(m)
        se_lo = sqrt(max(lo_m/ns*nu/n0 - d*d, 1e-12)/n0); se_hi = sqrt(max(hi_m/ns*nu/n0 - d*d, 1e-12)/n0)
        print(f"  {a}-{b}: {100*d:+5.1f} pp  gepaarte SE {100*se:4.2f} (Spanne {100*se_lo:.2f}-{100*se_hi:.2f})  z {d/se:+4.1f}  "
              f"90%-CI [{100*(d-1.645*se):+5.1f}; {100*(d+1.645*se):+5.1f}]  Diskordanz {m}/{ns}")
