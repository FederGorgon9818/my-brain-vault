"""Verdichtet fnrun/fn_tempo_<regime>_<nsim>.json zu einer Tabelle (Median, RMST, p3y, p10y, Auslage p90,
gepaarte RMST-Deltas gegen A_heute und gegen C_d040 mit 90-%-CI)."""
import glob
import json
import sys
from pathlib import Path

D = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "fnrun")
ORDER = ["IS", "shrink058", "recent3y", "shrink_recent", "null"]
files = {json.load(open(f))["regime"]: json.load(open(f)) for f in glob.glob(str(D / "fn_tempo_*_*.json"))
         if not f.endswith("_4.json")}
for rg in [r for r in ORDER if r in files]:
    r = files[rg]
    print(f"\n### {rg} (n={r['nsim']}, {r['sec']} s, Stempel {r['stempel']})")
    print("| Variante | Median M | RMST M | p3y % | p10y % | Auslage p90 | dRMST vs A [90-%-CI] | dRMST vs C [90-%-CI] | schneller vs C % |")
    print("|---|---|---|---|---|---|---|---|---|")
    for n, s in r["summ"].items():
        pa = r["paired_vs_A"].get(n); pc = r["paired_vs_C"].get(n)
        fa = f"{pa['d_rmst_m']:+.2f} [{pa['ci90'][0]:+.2f}; {pa['ci90'][1]:+.2f}]" if pa else "Referenz"
        fc = f"{pc['d_rmst_m']:+.2f} [{pc['ci90'][0]:+.2f}; {pc['ci90'][1]:+.2f}]" if pc else "Referenz"
        sc = f"{pc['share_faster']:.0f} / {pc['share_slower']:.0f}" if pc else ""
        print(f"| {n} | {s['med_m']} | {s['rmst_m']} | {s['p_3y']} | {s['p_10y']} | {s['outlay_p90']} | {fa} | {fc} | {sc} |")
