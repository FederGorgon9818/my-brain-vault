"""AP412 night_cpos_NQ: Vorab-Kriterien kill_1 bis kill_3 als Code (festgelegt 27.10.2026 VOR dem Runner-Lauf,
pipeline-auditor Auflage A3). md5 dieser Datei steht im Job-Feld vorab.skript_md5 -- nach dem Lauf nicht mehr aendern.

Die Kriterien entscheiden nicht im Runner, sondern beim Urteil (Wochenend-Pruefung / Stempel). Rechnet alle
12 Gridzellen und die drei None-Naechte lokal neu (gleiche Params wie der Job, Engine S-NACHT-GATE).

  Zelle      = schluss_profile der deploy_config des Runners. Ohne Kandidat: alle vier, Urteil nur Info.
  Einheit    = r_net (Punkte je 0,25 Tages-ATR, vol-normiert) UND Dollar je Micro; Lehre 182: beide muessen halten.
  kill_1     = Zuwachs gegen die None-Nacht im Fenster 18:15-03:00: einseitiger Permutationstest, Mittel der Zelle
               gegen 20.000 Zufallsauswahlen gleicher Groesse aus den None-Naechten (Saat 412), p <= 0,05.
  kill_2     = ganzes Fenster 18:15-09:25 ohne Montag-Sessions (d.dayofweek 0 = Sonntagabend-Nacht):
               Per-Trade-t >= 1,3, und Di/Do/Fr-Sessions zusammen nicht negativ.
  kill_3     = ganzes Fenster: Mittel 2016-2020 und 2021-2026 beide positiv, in bp (Punkte / RTH-Close von x) UND in r.
  info       = ATR-Terzile (as_f_atr20 je Trade) und Wochentage, nur Anzeige.

Aufruf: python _scratch_ap412/vorab_auswertung.py [--zelle cpos0.2|cpos0.4|l45_0|l45_-0.15pct] [--selbsttest]
"""
import sys, os, json, argparse
from pathlib import Path
ENG = Path(r"C:\Users\maxlk\Projects\trading-data\engine")
os.chdir(ENG); sys.path.insert(0, str(ENG)); sys.path.insert(0, str(ENG / "discovery"))
import numpy as np
import pandas as pd

P_MAX, T_MIN, N_PERM, SEED = 0.05, 1.3, 20000, 412
EPOCHS = (("2016-2020", 2016, 2020), ("2021-2026", 2021, 2026))


def perm_p(cell, none):
    """Einseitig: Anteil der Zufallsauswahlen (Groesse len(cell) aus none, ohne Zuruecklegen) mit Mittel >= Zelle."""
    cell, none = np.asarray(cell, float), np.asarray(none, float)
    k = len(cell)
    if k == 0 or k > len(none):
        return np.nan
    rng = np.random.default_rng(SEED)
    means = np.array([none[rng.choice(len(none), k, replace=False)].mean() for _ in range(N_PERM)])
    return float((np.sum(means >= cell.mean()) + 1) / (N_PERM + 1))


def t_stat(x):
    x = np.asarray(x, float)
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan


def kill_1(cell, none, col):
    p = perm_p(cell[col], none[col])
    return dict(p=round(p, 4), ok=bool(p <= P_MAX))


def kill_2(tr, col):
    dow = pd.to_datetime(tr["date"]).dt.dayofweek
    t = t_stat(tr.loc[dow != 0, col])
    s_dtf = float(tr.loc[dow.isin([1, 3, 4]), col].sum())
    return dict(t_ohne_mo=round(t, 2), sum_di_do_fr=round(s_dtf, 2), ok=bool(t >= T_MIN and s_dtf >= 0))


def kill_3(tr, cols):
    y = pd.to_datetime(tr["date"]).dt.year
    out, ok = {}, True
    for lab, a, b in EPOCHS:
        m = (y >= a) & (y <= b)
        for c in cols:
            v = float(tr.loc[m, c].mean()) if m.any() else np.nan
            out[f"{lab}_{c}"] = round(v, 4)
            ok &= bool(v > 0)
    out["ok"] = ok
    return out


def add_units(tr, close_x):
    import qbt
    pv = qbt.POINT_VALUE[tr.attrs.get("micro", "MNQ")]
    pts = tr["r_net"] * tr["R_pts"]
    tr = tr.assign(usd=pts * pv)
    sd = pd.DatetimeIndex(pd.to_datetime(tr["date"])).tz_localize(None).normalize()
    pos = np.searchsorted(close_x.index.values, sd.values, side="left") - 1
    px = np.where(pos >= 0, close_x.to_numpy()[np.clip(pos, 0, None)], np.nan)
    return tr.assign(bp=pts.to_numpy() / px * 1e4)


def verdict(cell_full, cell_abend, none_abend):
    k1 = {c: kill_1(cell_abend, none_abend, c) for c in ("r_net", "usd")}
    k2 = {c: kill_2(cell_full, c) for c in ("r_net", "usd")}
    k3 = kill_3(cell_full, ("bp", "r_net"))
    ok = all(v["ok"] for v in k1.values()) and all(v["ok"] for v in k2.values()) and k3["ok"]
    return dict(kill_1=k1, kill_2=k2, kill_3=k3, alle_ok=ok)


def selbsttest():
    rng = np.random.default_rng(1)
    d = pd.bdate_range("2016-01-04", "2026-10-01", freq="B")
    none = pd.DataFrame({"date": d, "r_net": rng.normal(0, 1, len(d))})
    none["usd"] = none["r_net"] * 100
    good = none.sample(400, random_state=2).assign(r_net=lambda x: x.r_net + 0.5)
    good["usd"] = good["r_net"] * 100
    good["bp"] = good["r_net"] * 10
    assert kill_1(good, none, "r_net")["ok"], "starke Zelle muss kill_1 bestehen"
    assert not kill_1(none.sample(400, random_state=3), none, "r_net")["ok"], "Zufallszelle darf kill_1 nicht bestehen"
    assert kill_2(good, "r_net")["ok"] and kill_3(good, ("bp", "r_net"))["ok"]
    bad = good.assign(r_net=good["r_net"] - 1.0, bp=good["bp"] - 10)
    assert not kill_2(bad, "r_net")["ok"] and not kill_3(bad, ("bp", "r_net"))["ok"]
    print("Selbsttest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zelle", default=None)
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args()
    if a.selbsttest:
        return selbsttest()
    import qbt
    job = json.loads((ENG / "_scratch_ap412" / "night_cpos_NQ.json").read_text(encoding="utf-8"))
    rth = qbt.load_rth("NQ")
    close_x = rth["c"].groupby(rth.index.normalize().tz_localize(None)).last()
    win = {f["_label"]: f for f in job["grid"]["fenster_profile"]}

    def run(extra, w):
        p = dict(job["base"], **{k: v for k, v in extra.items() if k != "_label"})
        p.update(tr_start=win[w]["tr_start"], tr_end=win[w]["tr_end"])
        return add_units(qbt.run_strategy(p, verbose=False), close_x)

    none_ab = run({}, "abend_1815_0300")
    cells = [c for c in job["grid"]["schluss_profile"] if a.zelle in (None, c["_label"])]
    out = {}
    for c in cells:
        full, abend = run(c, "ganz_1815_0925"), run(c, "abend_1815_0300")
        v = verdict(full, abend, none_ab)
        atr = full["as_f_atr20"]
        terc = pd.qcut(atr, 3, labels=["tief", "mittel", "hoch"])
        v["info_atr_terzile_usd"] = full.groupby(terc, observed=True)["usd"].mean().round(2).to_dict()
        v["info_wochentag_usd"] = full.groupby(pd.to_datetime(full["date"]).dt.dayofweek)["usd"].sum().round(0).to_dict()
        v["n_ganz"], v["n_abend"] = len(full), len(abend)
        out[c["_label"]] = v
        print(c["_label"], json.dumps(v, ensure_ascii=False, default=str))
    print("Zelle des Urteils = schluss_profile der deploy_config (Runner). Ohne Kandidat: nur Info.")


if __name__ == "__main__":
    main()
