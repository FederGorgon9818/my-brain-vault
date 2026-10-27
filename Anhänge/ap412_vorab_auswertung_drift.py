"""AP412 night_drift_NQ: Vorab-Kriterien als Code (festgelegt 27.10.2026 VOR dem Runner-Lauf, Einreihung auf
Entscheidung Max gegen die Story-Empfehlung des strategy-auditor). md5 dieser Datei steht im Job-Feld vorab.skript_md5
-- nach dem Lauf nicht mehr aendern.

Gleiches Lineal wie night_cpos_NQ: kill_2, kill_3 und die Einheiten (r_net, Dollar je Micro, bp) kommen unveraendert
aus vorab_auswertung.py (md5 df1cc148be53c169b8322ea790674f49, wird beim Laden geprueft).

  Zelle      = deploy_config des Runners (tr_start/tr_end). Ohne Kandidat: alle 9, Urteil nur Info.
  kill_1     = entfaellt: der Job IST die None-Nacht, ein Zuwachs gegen sich selbst ist nicht messbar.
               Die Vor-Gates des Runners (sharpe_t >= 2 nach Kosten, Trim) und Walk-Forward gelten wie immer.
  kill_2     = Fenster der Zelle ohne Montag-Sessions (Sonntagabend-Nacht): Per-Trade-t >= 1,3 und Di/Do/Fr-Sessions
               zusammen nicht negativ, in r UND in $.
  kill_3     = Fenster der Zelle: Mittel 2016-2020 und 2021-2026 beide positiv, in bp UND in r (Lehre 182).
  info       = Anteil Montag-Sessions an Naechten und an der Dollar-Summe, Dollar je Wochentag der Session,
               schlechteste Nacht je Micro, ATR-Terzile.
  bekannt    = kill_2 der Basiszelle 18:15-09:25 ist vor der Festlegung schon gemessen (pipeline-auditor 27.10.:
               ohne Montag t 1,26 in r und 0,59 in $, Di/Do/Fr -2.786,5 $) und damit kein offener Test.

Aufruf: python _scratch_ap412/vorab_auswertung_drift.py [--zelle 18:15-09:25] [--selbsttest]
"""
import sys, json, argparse, hashlib, importlib.machinery, importlib.util
from pathlib import Path
ENG = Path(r"C:\Users\maxlk\Projects\trading-data\engine")
VA_PATH, VA_MD5 = ENG / "_scratch_ap412" / "vorab_auswertung.py", "df1cc148be53c169b8322ea790674f49"
assert hashlib.md5(VA_PATH.read_bytes()).hexdigest() == VA_MD5, "vorab_auswertung.py wurde veraendert"
_ld = importlib.machinery.SourceFileLoader("vorab_auswertung", str(VA_PATH))
VA = importlib.util.module_from_spec(importlib.util.spec_from_loader(_ld.name, _ld))
_ld.exec_module(VA)
import numpy as np
import pandas as pd


def verdict(tr):
    k2 = {c: VA.kill_2(tr, c) for c in ("r_net", "usd")}
    k3 = VA.kill_3(tr, ("bp", "r_net"))
    ok = all(v["ok"] for v in k2.values()) and k3["ok"]
    return dict(kill_2=k2, kill_3=k3, alle_ok=ok)


def info(tr):
    dow = pd.to_datetime(tr["date"]).dt.dayofweek
    s = float(tr["usd"].sum())
    terc = pd.qcut(tr["as_f_atr20"], 3, labels=["tief", "mittel", "hoch"])
    return dict(n=len(tr), usd_summe=round(s, 0),
                anteil_mo_naechte=round(float((dow == 0).mean()), 3),
                anteil_mo_usd=round(float(tr.loc[dow == 0, "usd"].sum()) / s, 3) if s else None,
                schlechteste_nacht_usd=round(float(tr["usd"].min()), 0),
                atr_terzile_usd=tr.groupby(terc, observed=True)["usd"].mean().round(2).to_dict(),
                wochentag_usd=tr.groupby(dow)["usd"].sum().round(0).to_dict())


def selbsttest():
    VA.selbsttest()
    rng = np.random.default_rng(7)
    d = pd.bdate_range("2016-01-04", "2026-10-01", freq="B")
    tr = pd.DataFrame({"date": d, "r_net": rng.normal(0.3, 1, len(d))})
    tr["usd"], tr["bp"], tr["as_f_atr20"] = tr["r_net"] * 100, tr["r_net"] * 10, rng.uniform(50, 400, len(d))
    assert verdict(tr)["alle_ok"], "klar positive Nacht muss tragen"
    mo_only = tr.assign(r_net=np.where(tr["date"].dt.dayofweek == 0, 2.0, -0.2))
    mo_only = mo_only.assign(usd=mo_only["r_net"] * 100, bp=mo_only["r_net"] * 10)
    assert not verdict(mo_only)["alle_ok"], "reiner Montag-Effekt darf nicht tragen"
    assert 0.15 < info(tr)["anteil_mo_naechte"] < 0.25
    print("Selbsttest drift ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zelle", default=None, help="tr_start-tr_end, z.B. 18:15-09:25")
    ap.add_argument("--selbsttest", action="store_true")
    a = ap.parse_args()
    if a.selbsttest:
        return selbsttest()
    import qbt
    job = json.loads((ENG / "_scratch_ap412" / "night_drift_NQ.json").read_text(encoding="utf-8"))
    rth = qbt.load_rth("NQ")
    close_x = rth["c"].groupby(rth.index.normalize().tz_localize(None)).last()
    for s in job["grid"]["tr_start"]:
        for e in job["grid"]["tr_end"]:
            if a.zelle not in (None, f"{s}-{e}"):
                continue
            p = dict(job["base"], tr_start=s, tr_end=e)
            tr = VA.add_units(qbt.run_strategy(p, verbose=False), close_x)
            v = dict(verdict(tr), info=info(tr))
            print(f"{s}-{e}", json.dumps(v, ensure_ascii=False, default=str))
    print("Zelle des Urteils = deploy_config des Runners. Ohne Kandidat: nur Info.")


if __name__ == "__main__":
    main()
