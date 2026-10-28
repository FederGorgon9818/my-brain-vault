#!/usr/bin/env python3
"""Homeoffice-Tage als Nachweis fuehren und die Tagespauschale je Seite zaehlen.

Datei je Jahr: C:/Users/maxlk/Documents/Steuer/<jahr>/homeoffice.csv (datum;seite;notiz).
Seite gewo = Homeoffice fuer den Job (Werbungskosten, wirkt erst ueber dem Pauschbetrag),
Seite gewerbe = Tag, an dem zu Hause am Gewerbe gearbeitet wurde (Betriebsausgabe, ob das
neben einem GEWO-Tag zaehlt, klaert der Steuerberater). Pauschale nur einmal je Kalendertag.

    python homeoffice.py fill --von 2026-07-01 --bis 2026-10-28 --wochentag mi --seite gewo --ausser 2026-08-12
    python homeoffice.py add 2026-10-28 gewerbe --notiz "Abends Discovery ausgewertet"
    python homeoffice.py entferne 2026-08-19
    python homeoffice.py summe --jahr 2026
"""
import argparse
import csv
import datetime as dt
from pathlib import Path

import steuerlib as L

SEITEN = ("gewo", "gewerbe")
TAGE = {"mo": 0, "di": 1, "mi": 2, "do": 3, "fr": 4, "sa": 5, "so": 6}


def pfad(jahr, datei):
    return Path(datei) if datei else L.STEUER / str(jahr) / "homeoffice.csv"


def lies(p):
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return [z for z in csv.DictReader(f, delimiter=";") if z.get("datum")]


def schreib(p, zeilen):
    p.parent.mkdir(parents=True, exist_ok=True)
    zeilen = sorted(zeilen, key=lambda z: (z["datum"], z["seite"]))
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["datum", "seite", "notiz"], delimiter=";")
        w.writeheader()
        w.writerows({k: z.get(k, "") for k in ("datum", "seite", "notiz")} for z in zeilen)


def eintragen(zeilen, tag, seite, notiz=""):
    if any(z["datum"] == tag.isoformat() and z["seite"] == seite for z in zeilen):
        return False
    zeilen.append(dict(datum=tag.isoformat(), seite=seite, notiz=notiz))
    return True


def summe(zeilen, jahr):
    """Gewerbe-Tage an Werktagen ohne Vermerk frei/urlaub/krank sind vermutlich GEWO-Buerotage: dann
    zaehlt die Pauschale nur, wenn § 4 Abs. 5 Nr. 6c Satz 3 EStG traegt (Steuerberater). Sie werden
    deshalb getrennt als strittig gezeigt und nicht eingerechnet."""
    w = L.werte(jahr)
    tage, notiz = {}, {}
    for z in zeilen:
        d = dt.date.fromisoformat(z["datum"])
        if d.year == jahr:
            tage.setdefault(d, set()).add(z["seite"])
            notiz[d] = notiz.get(d, "") + " " + (z.get("notiz") or "").lower()
    frei = lambda d: not L.ist_werktag(d) or any(k in notiz[d] for k in ("frei", "urlaub", "krank"))
    gewo = sum(1 for s in tage.values() if s == {"gewo"})
    beide = sum(1 for s in tage.values() if len(s) > 1)
    gewerbe = [d for d, s in tage.items() if s == {"gewerbe"}]
    klar = sum(1 for d in gewerbe if frei(d))
    strittig = len(gewerbe) - klar
    gesamt = gewo + beide + klar
    max_tage = w["ho_max"] // w["ho_tag"]
    return dict(jahr=jahr, gewo=gewo, beide=beide, gewerbe_klar=klar, gewerbe_strittig=strittig,
                wk_tage=gewo + beide, gesamt=gesamt, angesetzt_tage=min(gesamt, max_tage),
                euro=min(gesamt, max_tage) * w["ho_tag"], strittig_euro=strittig * w["ho_tag"],
                ho_tag=w["ho_tag"], ho_max=w["ho_max"], gekappt=gesamt > max_tage)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datei", help="statt Standardpfad je Jahr")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fill")
    f.add_argument("--von", required=True)
    f.add_argument("--bis", required=True)
    f.add_argument("--wochentag", required=True, choices=TAGE)
    f.add_argument("--seite", required=True, choices=SEITEN)
    f.add_argument("--ausser", default="", help="Urlaub/Krank, Daten mit Komma")
    f.add_argument("--trocken", action="store_true")
    ad = sub.add_parser("add")
    ad.add_argument("datum")
    ad.add_argument("seite", choices=SEITEN)
    ad.add_argument("--notiz", default="")
    rm = sub.add_parser("entferne")
    rm.add_argument("datum")
    rm.add_argument("--seite", choices=SEITEN)
    s = sub.add_parser("summe")
    s.add_argument("--jahr", type=int, required=True)
    a = ap.parse_args()

    if a.cmd == "summe":
        p = pfad(a.jahr, a.datei)
        r = summe(lies(p), a.jahr)
        print("Homeoffice %d (%s)" % (a.jahr, p))
        print("  GEWO-Homeoffice: %d Tage (davon %d auch Gewerbe) | Gewerbe an freien Tagen: %d"
              % (r["wk_tage"], r["beide"], r["gewerbe_klar"]))
        print("  angesetzt %d x %d EUR = %s%s" % (r["angesetzt_tage"], r["ho_tag"], L.euro(r["euro"]),
                                               " (auf %d EUR gekappt)" % r["ho_max"] if r["gekappt"] else ""))
        if r["gewerbe_strittig"]:
            print("  strittig, NICHT eingerechnet: %d Gewerbe-Tage an Werktagen (%s), zaehlen nur nach "
                  "§ 4 Abs. 5 Nr. 6c Satz 3 EStG (Steuerberater). Urlaubstag? Notiz 'urlaub' setzen."
                  % (r["gewerbe_strittig"], L.euro(r["strittig_euro"])))
        if r["beide"]:
            print("  Tage mit GEWO und Gewerbe zaehlen nur einmal, hier auf der GEWO-Seite. Ob sie beim Gewerbe "
                  "mehr bringen (wirkt dort ohne Pauschbetrag), klaert der Steuerberater.")
        print("  GEWO-Tage wirken nur, wenn alle Werbungskosten zusammen ueber %s liegen (werbungskosten.py)."
              % L.euro(L.werte(a.jahr)["pauschbetrag"]))
        return

    tag0 = dt.date.fromisoformat(a.von if a.cmd == "fill" else a.datum)
    p = pfad(tag0.year, a.datei)
    zeilen = lies(p)

    if a.cmd == "add":
        neu = eintragen(zeilen, tag0, a.seite, a.notiz)
        print(("eingetragen: %s %s" if neu else "schon da: %s %s") % (L.de(tag0), a.seite))
    elif a.cmd == "entferne":
        vorher = len(zeilen)
        zeilen = [z for z in zeilen if not (z["datum"] == tag0.isoformat() and (not a.seite or z["seite"] == a.seite))]
        print("entfernt: %d Zeile(n)" % (vorher - len(zeilen)))
    else:
        bis = dt.date.fromisoformat(a.bis)
        if bis.year != tag0.year:
            raise SystemExit("fill nur innerhalb eines Jahres (eine Datei je Jahr).")
        ausser = {dt.date.fromisoformat(x.strip()) for x in a.ausser.split(",") if x.strip()}
        neu, feiertag = [], []
        d = tag0
        while d <= bis:
            if d.weekday() == TAGE[a.wochentag] and d not in ausser:
                if d in L.feiertage_bayern(d.year):
                    feiertag.append(d)
                elif eintragen(zeilen, d, a.seite, "fill %s" % a.wochentag):
                    neu.append(d)
            d += dt.timedelta(days=1)
        print("%s %d Tage (%s): %s" % ("wuerde eintragen" if a.trocken else "eingetragen", len(neu), a.seite,
                                      ", ".join(x.strftime("%d.%m.") for x in neu)))
        if feiertag:
            print("Feiertag, uebersprungen: " + ", ".join(L.de(x) for x in feiertag))
        if a.trocken:
            return
    schreib(p, zeilen)
    print("-> %s" % p)


if __name__ == "__main__":
    main()
