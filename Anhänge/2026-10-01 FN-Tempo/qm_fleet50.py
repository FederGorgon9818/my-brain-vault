"""50 Flotten-Sims (IS, Seed 101, Aufbau wie fn_tempo_check): Split 80 %, FN max. 5 aktive Funded, Formel-Effekt isoliert (Acap).
Engine nur gelesen; Kernel-Patches leben in diesem Prozess."""
import sys, os, inspect, json, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad")
import fn_tempo_check as F
tp = F.tp

# --- Split als Typ-Option
def mk(tier, split=0.95, **o):
    name = F.fn_type(tier, **o)
    if split != 0.95:
        nm2 = name + f"|s{split}"
        if nm2 not in tp.FN:
            tp.FN[nm2] = dict(tp.FN[tier]); F.OPTS[nm2] = dict(F.OPTS[name], split=split)
        name = nm2
    return name

def _cal_fund2(win, dc, dw, tk, ds=None):
    firm, tier, k = tk
    o = F.OPTS.get(tier) if firm == "FN" else None
    if o is None:
        return F._orig_fund(win, dc, dw, tk, ds=ds)
    T = tp.FN[tier]
    dcf = dc if o["fund_cap"] is None else np.minimum(dc, o["fund_cap"]*T["target"]/k)
    return F.run_funded_fn_x(win, dcf, dw, T["dd"], T["cap"], T["bench"], k=k, max_pays=tp.FN_MAX_PAYS, ds=ds,
                             split=o.get("split", 0.95), fix=o["fix"], theta=o["theta"], lock_first=o["lock_first"])
tp._cal_fund = _cal_fund2

# --- Flotte: FN max. 5 aktive Funded (Option je Politik ueber Lane-Flag), plus Zaehler wie viele FN-Funded gleichzeitig
src = inspect.getsource(tp._fleet_one_cal)
src = src.replace("def _fleet_one_cal(", "def _fleet_one_cal_x(")
src = src.replace("    def is_active():",
"""    FNMAX = 5 if any(ln.get("fnmax") for ln in lanes) else None
    def fn_nf():
        return sum(l["nf"] for l in Ls if l["P"]["firm"] == "FN") + sum(1 for a in INIT if a["fu"] and a["P"]["firm"] == "FN")
    def fn_ok(P):
        return FNMAX is None or P["firm"] != "FN" or fn_nf() < FNMAX
    TR = dict(mx=0, t6=0.0, last=0.0, c=0)
    def is_active():""", 1)
src = src.replace("""                if P["firm"] == "E8" and e8_nf() + l["wait"] + len(l["ev"]) >= e8_max_funded + l["m"]:
                    break""", """                if P["firm"] == "E8" and e8_nf() + l["wait"] + len(l["ev"]) >= e8_max_funded + l["m"]:
                    break
                if FNMAX is not None and P["firm"] == "FN" and fn_nf() + l["wait"] + len(l["ev"]) >= FNMAX + l["m"]:
                    break""", 1)
src = src.replace("""                    if l["nf"] < l["n_max"] and (P["firm"] != "E8" or e8_nf() < e8_max_funded):""",
                  """                    if l["nf"] < l["n_max"] and (P["firm"] != "E8" or e8_nf() < e8_max_funded) and fn_ok(P):""", 1)
src = src.replace("""                if l["wait"] > 0 and l["nf"] < l["n_max"] and (P["firm"] != "E8" or e8_nf() < e8_max_funded):""",
                  """                if l["wait"] > 0 and l["nf"] < l["n_max"] and (P["firm"] != "E8" or e8_nf() < e8_max_funded) and fn_ok(P):""", 1)
src = src.replace("""        t = tn
""", """        if TR["c"] >= 6: TR["t6"] += tn - TR["last"]
        t = tn
""", 1)
src = src.replace("""        if hit is not None and (G2 is None or hit2 is not None):
            break""", """        TR["c"] = fn_nf(); TR["mx"] = max(TR["mx"], TR["c"]); TR["last"] = t
        if hit is not None and (G2 is None or hit2 is not None):
            break""", 1)
src = src.replace("""                net_end=pay - spend)""", """                net_end=pay - spend, fnmx=TR["mx"], t6=TR["t6"])""", 1)
print("patch-check", src.count("fn_ok(P)"), "fnmx" in src, "FNMAX + l[" in src, "TR[\"t6\"] +=" in src, "TR[\"mx\"] = max" in src); assert src.count("fn_ok(P)") == 3
_ORIG_FLEET = tp._fleet_one_cal
exec(compile(src, "fleet_x", "exec"), tp.__dict__)
tp._fleet_one_cal = tp._fleet_one_cal_x

G, BUDGET, CAP_OUT, SEED, TMAX_M = 50000.0, 600.0, 2500.0, 101, 120
nsim = int(sys.argv[1]) if len(sys.argv) > 1 else 50
dc0, dw0, apy, days, C, W = tp.build_cells(None); TM = apy/12
dc, dw = tp.apply_regime(dc0, dw0, days, "IS")
pf = lambda firm, tier, k, **kw: tp.make_pool(dc, dw, firm, tier, k, n=50, tag="qm50", **kw)
OPT = {"C": dict(eval_cap=0.40, fix=True), "D": dict(eval_cap=0.40, fix=True, theta=1.0, lock_first=True),
       "A": dict(), "Acap": dict(eval_cap=0.40)}
VAR = {"C": ("C", 0.95, False), "D": ("D", 0.95, False), "A": ("A", 0.95, False), "Acap": ("Acap", 0.95, False),
       "C_s80": ("C", 0.80, False), "D_s80": ("D", 0.80, False), "C_max5": ("C", 0.95, True), "D_max5": ("D", 0.95, True)}
pol = {}
for name, (o, sp, mx) in VAR.items():
    t50, t150 = mk("50k", sp, **OPT[o]), mk("150k", sp, **OPT[o])
    init = [dict(pool=pf("E8", "50k", 1, **tp.E8_START), stage="eval", fresh=pf("E8", "50k", 1)),
            dict(pool=pf("FN", t50, 1), stage="eval"), dict(pool=pf("FN", t50, 1), stage="eval")]
    lanes = [dict(pool=pf("E8", "150k", 2), n_max=4, m=2, start_m=0),
             dict(pool=pf("FN", t150, 2), n_max=4, m=2, start_m=0, fnmax=mx)]
    pol[name] = dict(lanes=lanes, init=init)
if os.environ.get("CHECK"):
    sub = {k: pol[k] for k in ("C", "D", "A")}
    tp._fleet_one_cal = _ORIG_FLEET
    a = tp.simulate_fleet_calendar(sub, G, TM, B=BUDGET, Tmax_m=TMAX_M, nsim=4, seed=SEED, max_outlay=CAP_OUT, marks_m=(9, 12, 24, 36), return_raw=True, day_stop=tp.day_stop_fn("rg"))
    tp._fleet_one_cal = tp._fleet_one_cal_x
    b = tp.simulate_fleet_calendar(sub, G, TM, B=BUDGET, Tmax_m=TMAX_M, nsim=4, seed=SEED, max_outlay=CAP_OUT, marks_m=(9, 12, 24, 36), return_raw=True, day_stop=tp.day_stop_fn("rg"))
    for k in sub:
        ra, rb = a[k]["_raw"], b[k]["_raw"]
        print(k, "bitgleich:", all(all((x[f] == y[f]) or (x[f] != x[f] and y[f] != y[f]) for f in x) for x, y in zip(ra, rb)), [round(x["T"]/TM, 2) for x in ra])
    sys.exit(0)
sims = tp.simulate_fleet_calendar(pol, G, TM, B=BUDGET, Tmax_m=TMAX_M, nsim=nsim, seed=SEED, max_outlay=CAP_OUT,
                                  marks_m=(9, 12, 24, 36), return_raw=True, day_stop=tp.day_stop_fn("rg"))
raw = {n: v.pop("_raw") for n, v in sims.items()}
Tm = {n: np.minimum(np.array([r["T"] for r in v], float)/TM, TMAX_M) for n, v in raw.items()}
def pd_(a, b):
    d = Tm[a] - Tm[b]; return f"{d.mean():+.2f} (SE {d.std(ddof=1)/np.sqrt(len(d)):.2f})"
print(f"n={nsim} IS")
for n in sims:
    s = sims[n]; fm = np.array([r["fnmx"] for r in raw[n]]); t6 = np.array([r["t6"] for r in raw[n]])/TM
    print(f"{n:7s} rmst {s['rmst_m']:6.1f} med {s['med_m']} dead {s['p_econ_dead']:5.1f} | FN-Funded max>=6 in {100*(fm>=6).mean():.0f}% Sims, Zeit>=6 Mittel {t6.mean():.1f} M")
for a, b in (("A", "C"), ("Acap", "C"), ("A", "Acap"), ("D", "C"), ("C_s80", "C"), ("D_s80", "D"), ("D_s80", "C_s80"),
             ("C_max5", "C"), ("D_max5", "D"), ("D_max5", "C_max5")):
    print(f"  {a:7s} - {b:7s}: dRMST {pd_(a, b)} M")
