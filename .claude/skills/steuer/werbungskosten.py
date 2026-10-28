#!/usr/bin/env python3
"""Werbungskosten eines Jahres zusammenrechnen und gegen den Arbeitnehmer-Pauschbetrag stellen.

Eingabe: C:/Users/maxlk/Documents/Steuer/<jahr>/werbungskosten.csv
Kopf:    art;beschreibung;menge;wert;anteil;beleg;mittel;kauf
  pendeln       menge = Arbeitstage am Betrieb, wert = km einfache Strecke (Entfernungspauschale,
                egal welches Verkehrsmittel). Jobticket/Zuschuss vom Betrieb: --z17/--z18
  berufsschule  Auswaertstaetigkeit, menge = Fahrtage, mittel Pflicht:
                pkw (2 x km x 0,30) | moped/motorrad (2 x km x 0,20) | oepnv (wert = Kosten je Fahrtag)
                | mitfahrer/fahrrad/fuss (0)
  verpflegung   menge = Tage mit mehr als 8 h Abwesenheit (Berufsschule), wert leer = 14 EUR
  erstattung    wert = steuerfrei erstattete Reisekosten vom Betrieb (§ 3 Nr. 16), wird abgezogen
  homeoffice    menge = Tage, oder leer: GEWO-Tage aus homeoffice.csv
  kontofuehrung wert leer = 16 EUR Pauschale
  afa           menge = Nutzungsdauer in Jahren, wert = Bruttopreis, anteil %, kauf = JJJJ-MM-TT
  arbeitsmittel / fachliteratur / sonstiges   wert = Bruttopreis, anteil = beruflicher Anteil in %
Ausgabe: werbungskosten.md daneben. Optional grobe Einordnung der Erstattung aus der
Lohnsteuerbescheinigung (Zeilen 3, 4, 5, 6, 23a, 25, 26).

    python werbungskosten.py --jahr 2024
    python werbungskosten.py --jahr 2024 --z17 120 --brutto 11800 --lst 120 --rv 1097 --kv 960 --pv 200
"""
import argparse
import csv
from pathlib import Path

import steuerlib as L
import homeoffice as HO

COMPUTER = ("laptop", "notebook", "computer", "pc", "tablet", "monitor", "bildschirm", "drucker", "tastatur",
            "maus", "software", "dockingstation", "headset")
KM_SATZ = {"pkw": 0.30, "auto": 0.30, "moped": 0.20, "motorrad": 0.20, "roller": 0.20, "mofa": 0.20}
OHNE_KOSTEN = ("mitfahrer", "fahrrad", "fuss", "zu fuss")
VERPFLEGUNG_8H = 14


def pendel_satz(km, w):
    return min(km, 20) * w["pendel_bis20"] + max(km - 20, 0) * w["pendel_ab21"]


def afa_im_jahr(preis, nd_jahre, kauf, jahr):
    """Linear, monatsgenau ab dem Kaufmonat (§ 7 Abs. 1 Satz 4 EStG)."""
    start = kauf.year * 12 + kauf.month - 1
    ende = start + int(nd_jahre * 12)
    monate = max(0, min(ende, jahr * 12 + 12) - max(start, jahr * 12))
    return preis / (nd_jahre * 12) * monate, monate


def posten(z, jahr, ordner):
    w = L.werte(jahr)
    art = (z.get("art") or "").strip().lower()
    mittel = (z.get("mittel") or "").strip().lower()
    menge = L.zahl(z.get("menge"), True)
    wert = L.zahl(z.get("wert"), True)
    anteil = L.zahl(z.get("anteil"), True)
    anteil = 100.0 if anteil is None else anteil
    hinweis = ""
    if art == "pendeln":
        km = int(wert or 0)
        betrag = (menge or 0) * pendel_satz(km, w)
        rechnung = "%d Tage x %d km (bis 20: %.2f, ab 21: %.2f)" % (menge or 0, km, w["pendel_bis20"], w["pendel_ab21"])
    elif art == "berufsschule":
        tage = menge or 0
        if mittel in KM_SATZ:
            betrag = tage * 2 * (wert or 0) * KM_SATZ[mittel]
            rechnung = "%d Fahrtage x 2 x %g km x %.2f (%s)" % (tage, wert or 0, KM_SATZ[mittel], mittel)
        elif mittel in ("oepnv", "bus", "bahn"):
            betrag = tage * (wert or 0)
            rechnung = "%d Fahrtage x %s Ticket" % (tage, L.euro(wert or 0))
            hinweis = "tatsaechliche Ticketkosten, Belege aufheben"
        elif mittel in OHNE_KOSTEN:
            betrag, rechnung = 0.0, "keine Kosten (%s)" % mittel
        else:
            betrag, rechnung = 0.0, "nicht gerechnet"
            hinweis = "Verkehrsmittel fehlt (Spalte mittel: pkw, moped, oepnv, mitfahrer)"
        if betrag:
            hinweis = (hinweis + "; " if hinweis else "") + "nur wenn der Betrieb erste Taetigkeitsstaette ist"
    elif art == "verpflegung":
        satz = VERPFLEGUNG_8H if wert is None else wert
        betrag = (menge or 0) * satz
        rechnung = "%d Tage x %s" % (menge or 0, L.euro(satz))
        hinweis = "nur Tage mit mehr als 8 h weg, Dreimonatsfrist nur bei mehr als 2 Schultagen pro Woche"
    elif art == "erstattung":
        betrag = -abs(wert or 0)
        rechnung = "steuerfrei vom Betrieb erstattet"
    elif art == "homeoffice":
        if menge is None:
            menge = HO.summe(HO.lies(ordner / "homeoffice.csv"), jahr)["wk_tage"]
            hinweis = "GEWO-Tage aus homeoffice.csv"
        tage = min(int(menge), w["ho_max"] // w["ho_tag"])
        betrag = tage * w["ho_tag"]
        rechnung = "%d Tage x %d EUR (max %d EUR)" % (tage, w["ho_tag"], w["ho_max"])
    elif art == "kontofuehrung":
        betrag = L.KONTOFUEHRUNG if wert is None else wert
        rechnung = "Pauschale ohne Nachweis" if wert is None else "laut Nachweis"
    elif art == "afa":
        kauf = L.datum(z.get("kauf"))
        if kauf is None or not menge:
            betrag, rechnung = 0.0, "nicht gerechnet"
            hinweis = "afa braucht menge = Nutzungsdauer (Jahre) und kauf = Datum"
        else:
            betrag, monate = afa_im_jahr((wert or 0) * anteil / 100, menge, kauf, jahr)
            rechnung = "%s x %g %% / %g Jahre, %d Monate in %d" % (L.euro(wert or 0), anteil, menge, monate, jahr)
            hinweis = "Nutzungsdauer laut AfA-Tabelle"
    else:
        text = (z.get("beschreibung") or "").lower()
        if (wert or 0) > L.GWG_BRUTTO and not any(k in text for k in COMPUTER):
            betrag, rechnung = 0.0, "nicht gerechnet"
            hinweis = "ueber %d EUR brutto: als Zeile art=afa eintragen (menge = Nutzungsdauer, kauf = Datum)" % L.GWG_BRUTTO
        else:
            betrag = (wert or 0) * anteil / 100
            rechnung = "%s x %g %%" % (L.euro(wert or 0), anteil)
            if (wert or 0) > L.GWG_BRUTTO:
                hinweis = "Computer/Software: Nutzungsdauer 1 Jahr, voll im Kaufjahr"
    return dict(art=art, beschreibung=z.get("beschreibung", ""), rechnung=rechnung, betrag=betrag,
                beleg=z.get("beleg", ""), hinweis=hinweis)


def einordnung(jahr, wk, a):
    """Grob: zvE unter Grundfreibetrag -> Lohnsteuer kommt komplett zurueck. Nur zum Priorisieren."""
    w = L.werte(jahr)
    vorsorge = (a.rv or 0) + 0.96 * (a.kv or 0) + (a.pv or 0)
    sonderausgaben = max(L.SONDERAUSGABEN_PAUSCH, a.kist or 0)     # § 10c: Pauschbetrag oder mehr
    zve = a.brutto - max(wk, w["pauschbetrag"]) - sonderausgaben - vorsorge
    einbehalten = (a.lst or 0) + (a.soli or 0) + (a.kist or 0)
    z = ["", "## Grobe Einordnung (Lohnsteuerbescheinigung)", "",
         "| Wert | Betrag |", "| --- | --- |",
         "| Bruttolohn | %s |" % L.euro(a.brutto),
         "| minus Werbungskosten (mind. Pauschbetrag) | %s |" % L.euro(max(wk, w["pauschbetrag"])),
         "| minus Sonderausgaben (36 EUR oder gezahlte Kirchensteuer) | %s |" % L.euro(sonderausgaben),
         "| minus Vorsorge (RV + 96 %% KV + PV, ohne AV) | %s |" % L.euro(vorsorge),
         "| = zu versteuern, grob | %s |" % L.euro(zve),
         "| Grundfreibetrag %d | %s |" % (jahr, L.euro(w["grundfreibetrag"])),
         "| einbehalten (LSt + Soli + KiSt) | %s |" % L.euro(einbehalten), ""]
    if einbehalten == 0:
        z.append("**Nichts einbehalten: die Erklaerung bringt fuer dieses Jahr kein Geld zurueck.**")
    elif zve <= w["grundfreibetrag"]:
        z.append("**Unter dem Grundfreibetrag: voraussichtlich kommt alles Einbehaltene zurueck, rund %s.**"
                 % L.euro(einbehalten))
    else:
        z.append("**Ueber dem Grundfreibetrag: Erstattung nur teilweise. Genaue Zahl liefert die ELSTER-Vorschau.**")
    z.append("Grob gerechnet (Arbeitslosenversicherung nicht abgezogen, also eher vorsichtig), ersetzt nicht ELSTER.")
    return z


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--jahr", type=int, required=True)
    ap.add_argument("--datei")
    ap.add_argument("--z17", type=float, default=0, help="LSB Zeile 17: steuerfreie Fahrtkosten-Leistungen (Jobticket)")
    ap.add_argument("--z18", type=float, default=0, help="LSB Zeile 18: pauschal besteuerte Fahrtkosten-Zuschuesse")
    for k in ("brutto", "lst", "soli", "kist", "rv", "kv", "pv"):
        ap.add_argument("--" + k, type=float)
    a = ap.parse_args()
    w = L.werte(a.jahr)
    p = Path(a.datei) if a.datei else L.STEUER / str(a.jahr) / "werbungskosten.csv"
    if not p.exists():
        raise SystemExit("%s fehlt. Kopf: art;beschreibung;menge;wert;anteil;beleg;mittel;kauf" % p)
    with p.open(encoding="utf-8-sig", newline="") as f:
        zeilen = [z for z in csv.DictReader(f, delimiter=";") if (z.get("art") or "").strip()]
    pos = [posten(z, a.jahr, p.parent) for z in zeilen]
    if a.z17 or a.z18:
        pendel = sum(x["betrag"] for x in pos if x["art"] == "pendeln")
        abzug = min(a.z17 + a.z18, pendel)
        pos.append(dict(art="abzug", beschreibung="Fahrtkosten vom Betrieb (LSB Z. 17/18)",
                        rechnung="mindert die Entfernungspauschale, hoechstens bis 0", betrag=-abzug, beleg="LSB",
                        hinweis=""))
    summe = sum(x["betrag"] for x in pos)
    mehr = summe - w["pauschbetrag"]

    md = ["# Werbungskosten %d" % a.jahr, "", "Werte Stand 28.10.2026, vor Abgabe gegen bmf/elster pruefen.", "",
          "| Art | Posten | Rechnung | Betrag | Beleg | Hinweis |", "| --- | --- | --- | --- | --- | --- |"]
    md += ["| %s | %s | %s | %s | %s | %s |" % (x["art"], x["beschreibung"], x["rechnung"], L.euro(x["betrag"]),
                                               x["beleg"], x["hinweis"]) for x in pos]
    md += ["", "**Summe: %s** · Pauschbetrag %d: %s" % (L.euro(summe), a.jahr, L.euro(w["pauschbetrag"])), ""]
    md.append("Ueber dem Pauschbetrag um %s, das senkt das zu versteuernde Einkommen." % L.euro(mehr) if mehr > 0 else
              "Unter dem Pauschbetrag: die Einzelposten bringen nichts extra, der Pauschbetrag gilt automatisch.")
    offen = [x for x in pos if x["rechnung"] == "nicht gerechnet"]
    if offen:
        md.append("**%d Zeile(n) nicht gerechnet, Hinweis-Spalte lesen.**" % len(offen))
    if a.brutto is not None:
        md += einordnung(a.jahr, summe, a)
    out = p.parent / "werbungskosten.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print("\n-> %s" % out)


if __name__ == "__main__":
    main()
