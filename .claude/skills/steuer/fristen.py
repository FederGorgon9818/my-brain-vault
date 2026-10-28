#!/usr/bin/env python3
"""Steuerfristen rechnen, Feiertage Bayern (Finanzamt Erding) eingerechnet.

rueckblick: freiwillige Erklaerung (Antragsveranlagung, § 46 Abs. 2 Nr. 8 EStG) geht bis Ende
            des 4. Folgejahres. Gilt nur, wenn fuer das Jahr keine Abgabepflicht bestand.
bescheid:   Bekanntgabe = Bescheiddatum + 4 Tage (ab 2025, davor 3; § 122 Abs. 2, § 122a AO),
            verschoben auf den naechsten Werktag; Einspruchsfrist 1 Monat ab Bekanntgabe
            (§ 355 AO, § 108 AO mit §§ 187 bis 188 BGB), Ende wieder auf den naechsten Werktag.

    python fristen.py rueckblick --ab 2023
    python fristen.py bescheid --datum 2027-05-10 [--zugang 2027-05-20]
"""
import argparse
import datetime as dt
import json

import steuerlib as L


def rueckblick(ab, heute, bis=None):
    jahre = []
    for jahr in range(ab, min(bis + 1, heute.year) if bis else heute.year):
        regulaer = dt.date(jahr + 4, 12, 31)
        ende = L.naechster_werktag(regulaer)
        jahre.append(dict(jahr=jahr, frist=ende.isoformat(), verschoben=ende != regulaer,
                          tage_uebrig=(ende - heute).days, abgelaufen=ende < heute))
    return jahre


def bescheid(datum, zugang=None):
    tage = 4 if datum >= dt.date(2025, 1, 1) else 3
    fiktion = datum + dt.timedelta(days=tage)
    bekannt = L.naechster_werktag(fiktion)
    hinweis = []
    if zugang and zugang > bekannt:
        hinweis.append("Spaeterer Zugang (%s) belegt: Bekanntgabe erst dann. Im Zweifel muss das Finanzamt "
                       "den Zugang beweisen, trotzdem besser die fruehere Frist halten." % L.de(zugang))
        bekannt = zugang
    regulaer = L.plus_monate(bekannt, 1)
    ende = L.naechster_werktag(regulaer)
    # Fuer den Kalender: ohne jede Verschiebung gerechnet, liegt nie spaeter als die echte Frist
    sicher = L.plus_monate(fiktion, 1)
    return dict(bescheid=datum.isoformat(), tage_fiktion=tage, fiktion=fiktion.isoformat(),
                bekanntgabe=bekannt.isoformat(), frist_regulaer=regulaer.isoformat(), frist=ende.isoformat(),
                frist_sicher=sicher.isoformat(), hinweis=hinweis)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("rueckblick")
    r.add_argument("--ab", type=int, required=True, help="erstes Jahr mit Lohn, z.B. 2023")
    r.add_argument("--bis", type=int, help="letztes freiwillige Jahr (Max: 2025, ab 2026 Gewerbe)")
    r.add_argument("--heute")
    r.add_argument("--json", action="store_true")
    b = sub.add_parser("bescheid")
    b.add_argument("--datum", required=True, help="Datum auf dem Bescheid (JJJJ-MM-TT)")
    b.add_argument("--zugang", help="tatsaechlicher Zugang, nur wenn spaeter als die Fiktion")
    b.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.cmd == "rueckblick":
        heute = dt.date.fromisoformat(a.heute) if a.heute else dt.date.today()
        jahre = rueckblick(a.ab, heute, a.bis)
        if a.json:
            print(json.dumps(jahre, ensure_ascii=False, indent=2))
            return
        print("Freiwillige Erklaerung, Stichtag %s (nur ohne Abgabepflicht im Jahr):" % L.de(heute))
        for j in jahre:
            ende = dt.date.fromisoformat(j["frist"])
            txt = "ABGELAUFEN" if j["abgelaufen"] else "%d Tage" % j["tage_uebrig"]
            extra = " (31.12. faellt auf Wochenende/Feiertag)" if j["verschoben"] else ""
            print("  %d  bis %s  %s%s" % (j["jahr"], L.de(ende), txt, extra))
        return

    d = bescheid(dt.date.fromisoformat(a.datum), dt.date.fromisoformat(a.zugang) if a.zugang else None)
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    f = lambda k: L.de(dt.date.fromisoformat(d[k]))
    print("Bescheid vom %s" % f("bescheid"))
    print("  Bekanntgabe: %s (Datum + %d Tage = %s, auf Werktag geschoben)" % (f("bekanntgabe"), d["tage_fiktion"], f("fiktion")))
    print("  Einspruch bis: %s (1 Monat = %s)" % (f("frist"), f("frist_regulaer")))
    print("  Fuer den Kalender (ohne Verschiebungen, sicher): %s" % f("frist_sicher"))
    for h in d["hinweis"]:
        print("  Hinweis: " + h)
    print("  Einspruch per ELSTER reicht, muss bis 24 Uhr am letzten Tag eingegangen sein. Datum auf dem Bescheid gegenlesen.")


if __name__ == "__main__":
    main()
