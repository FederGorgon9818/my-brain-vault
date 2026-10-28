#!/usr/bin/env python3
"""Kontoauszug gegen Belegordner: welche Gewerbe-Abbuchung hat keinen Beleg, welcher Beleg keine Abbuchung?

Liest einen oder mehrere Bank-Exporte (Revolut CSV englisch oder deutsch, deutsche Banken),
erkennt Gewerbe-Zahlungen ueber regeln.json und gleicht sie mit EUeR-<jahr>.csv ab.
Zuordnung in zwei Stufen: erst echte Anbieter (Anbieter + Datum +- Tage + Betrag mit Toleranz,
USD gegen Originalbetrag, Revolut-Gebuehr addiert), danach Zahlungsdienste wie PayPal nur noch
gegen uebrige Belege und nur ueber den Betrag (eigener Abschnitt, immer pruefen).
Private Umsaetze ohne Regel-Treffer tauchen im Bericht nicht auf (ausser mit --ohne-regel-ab).

    python abgleich.py C:/Users/maxlk/Documents/Steuer/Kontoauszuege/revolut_2026-10.csv
    python abgleich.py auszug.csv --von 2026-08-09 --bis 2026-10-31 --euer EUeR-2026.csv --out bericht.md
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

import steuerlib as L

HIER = Path(__file__).resolve().parent

COL_DATUM = ["completed date", "datum des abschlusses", "abschlussdatum", "abgeschlossen am", "buchungstag",
             "buchungsdatum", "datum", "date", "started date", "startdatum", "valuta", "wertstellung"]
COL_TEXT = ["description", "beschreibung", "name zahlungsbeteiligter", "zahlungsempfänger*in", "zahlungsempfänger",
            "zahlungsempfaenger", "empfänger", "auftraggeber/empfänger", "begünstigter/zahlungspflichtiger",
            "beguenstigter/zahlungspflichtiger", "verwendungszweck", "buchungstext"]
COL_BETRAG = ["amount", "betrag", "betrag (eur)", "betrag (€)", "betrag in eur", "umsatz"]
COL_GEBUEHR = ["fee", "gebühr", "gebuehr", "gebühren"]
COL_WAEHRUNG = ["currency", "währung", "waehrung"]
COL_STATUS = ["state", "status"]
COL_TYP = ["type", "typ"]
STATUS_OK = {"", "completed", "abgeschlossen", "ausgeführt", "ausgefuehrt", "gebucht", "erledigt"}
TYP_INTERN = {"exchange", "umtausch", "wechsel", "währungsumtausch"}
MAX_ABWEICHUNG = 0.25    # darueber kein Paar "Betrag weicht ab", sondern zwei getrennte Meldungen


def passt(muster, text):
    if len(muster) <= 4:
        return re.search(r"(?<![a-z0-9])" + re.escape(muster) + r"(?![a-z0-9])", text) is not None
    return muster in text


def regel_fuer(text, regeln):
    t = text.lower()
    for r in regeln:
        if any(passt(m, t) for m in r["muster"]):
            return r
    return None


def lies_auszug(pfad, regeln, info):
    """Alle abgeschlossenen Umsaetze einer Datei, regel=None fuer Umsaetze ohne Treffer."""
    kopf, zeilen = L.lies_csv(pfad)
    i_dat, i_bet = L.spalte(kopf, COL_DATUM), L.spalte(kopf, COL_BETRAG)
    if i_dat is None or i_bet is None:
        raise SystemExit("%s: Datum oder Betrag nicht erkannt. Spalten: %s (Namen in abgleich.py ergaenzen)"
                         % (Path(pfad).name, ", ".join(kopf)))
    i_txt = [kopf.index(n) for n in COL_TEXT if n in kopf]
    i_geb, i_wae = L.spalte(kopf, COL_GEBUEHR), L.spalte(kopf, COL_WAEHRUNG)
    i_sta, i_typ = L.spalte(kopf, COL_STATUS), L.spalte(kopf, COL_TYP)
    feld = lambda z, i: z[i].strip() if i is not None and i < len(z) else ""
    deutsch = any(re.search(r",\d{2}$", feld(z, i_bet)) for z in zeilen)
    out = []
    for z in zeilen:
        if feld(z, i_sta).lower() not in STATUS_OK:
            info["status_uebersprungen"] += 1
            continue
        typ = feld(z, i_typ).lower()
        if typ in TYP_INTERN:
            continue
        tag, betrag = L.datum(feld(z, i_dat)), L.zahl(feld(z, i_bet), deutsch)
        if tag is None or betrag is None or betrag == 0:
            continue
        info["zeilen"] += 1
        info["von"] = min(info.get("von") or tag, tag)
        info["bis"] = max(info.get("bis") or tag, tag)
        text = " ".join(feld(z, i) for i in i_txt if feld(z, i))
        out.append(dict(datum=tag, text=text, betrag=betrag, gebuehr=abs(L.zahl(feld(z, i_geb), deutsch) or 0.0),
                        waehrung=(feld(z, i_wae) or "EUR").upper(), typ=typ, regel=regel_fuer(text, regeln),
                        quelle=Path(pfad).name))
    return out


def zusammenfuehren(dateien):
    """Ueberlappende Exporte nicht doppelt zaehlen, echte Doppelkaeufe in einer Datei aber behalten:
    je Schluessel (Datum, Text, Betrag) zaehlt die hoechste Anzahl in einer einzelnen Datei."""
    schluessel = lambda s: (s["datum"], s["text"], s["betrag"])
    maxn = Counter()
    for zeilen in dateien:
        for k, n in Counter(schluessel(s) for s in zeilen).items():
            maxn[k] = max(maxn[k], n)
    genommen, out = Counter(), []
    for zeilen in dateien:
        for s in zeilen:
            k = schluessel(s)
            if genommen[k] < maxn[k]:
                genommen[k] += 1
                out.append(s)
    return out


def lies_euer(pfad):
    kopf, zeilen = L.lies_csv(pfad)
    sp = {n: L.spalte(kopf, [n]) for n in ("datum", "kategorie", "anbieter", "beschreibung",
                                            "betrag_original", "betrag_eur", "beleg_datei")}
    if sp["datum"] is None or sp["betrag_eur"] is None:
        raise SystemExit("%s: Spalten Datum/Betrag_EUR nicht gefunden" % pfad)
    feld = lambda z, n: z[sp[n]].strip() if sp[n] is not None and sp[n] < len(z) else ""
    out = []
    for z in zeilen:
        tag = L.datum(feld(z, "datum"))
        eur = L.zahl(feld(z, "betrag_eur"))
        if tag is None or eur is None:
            continue
        orig = feld(z, "betrag_original")
        out.append(dict(datum=tag, kategorie=feld(z, "kategorie"), anbieter=feld(z, "anbieter"),
                        beschreibung=feld(z, "beschreibung"), eur=abs(eur),
                        orig=abs(L.zahl(orig) or eur), orig_waehrung=L.waehrung(orig) or "EUR",
                        beleg=feld(z, "beleg_datei"), ordner=Path(pfad).parent))
    return out


def vergleich(s, e):
    """Referenzbetrag passend zur Waehrung des Umsatzes, Differenz, ob in Toleranz."""
    ist = abs(s["betrag"]) + (s["gebuehr"] if s["betrag"] < 0 else 0)
    if s["waehrung"] == "EUR":
        soll = e["eur"]
    elif s["waehrung"] == e["orig_waehrung"]:
        soll = e["orig"]
    else:
        soll = e["eur"]
    diff = abs(ist - soll)
    return ist, soll, diff, diff <= max(1.0, 0.03 * soll)


def paare(umsaetze, belege, tage, frei_s, frei_e, dienst):
    out = []
    for i in frei_s:
        s = umsaetze[i]
        r = s["regel"]
        if bool(r.get("zahlungsdienst")) != dienst:
            continue
        for j in frei_e:
            e = belege[j]
            if (s["betrag"] > 0) != ("payout" in e["kategorie"].lower()):
                continue
            if not dienst and not any(sub in e["anbieter"].lower() for sub in r.get("euer", [])):
                continue
            d = (s["datum"] - e["datum"]).days
            if abs(d) > tage:
                continue
            ist, soll, diff, ok = vergleich(s, e)
            if not ok and (dienst or diff > MAX_ABWEICHUNG * soll):
                continue
            out.append((0 if ok else 1, abs(d), diff, i, j, ist, soll))
    return sorted(out)


def zuordnen(kandidaten, frei_s, frei_e, durchgang):
    treffer = []
    for ok, d, diff, i, j, ist, soll in kandidaten:
        if ok != durchgang or i not in frei_s or j not in frei_e:
            continue
        frei_s.discard(i)
        frei_e.discard(j)
        treffer.append((i, j, ist, soll))
    return treffer


def abgleich(umsaetze, belege, tage):
    """Stufe 1: Anbieter-Treffer (erst passend, dann abweichend bis 25 %). Stufe 2: Zahlungsdienste
    nur gegen die uebrigen Belege, nur passend."""
    frei_s, frei_e = set(range(len(umsaetze))), set(range(len(belege)))
    k = paare(umsaetze, belege, tage, frei_s, frei_e, dienst=False)
    passt_ = zuordnen(k, frei_s, frei_e, 0)
    weicht = zuordnen(k, frei_s, frei_e, 1)
    nur_betrag = zuordnen(paare(umsaetze, belege, tage, frei_s, frei_e, dienst=True), frei_s, frei_e, 0)
    expand = lambda liste: [(umsaetze[i], belege[j], ist, soll) for i, j, ist, soll in liste]
    return expand(passt_), expand(weicht), expand(nur_betrag), [umsaetze[i] for i in sorted(frei_s)], frei_e


def tabelle(kopf, zeilen):
    if not zeilen:
        return ["_keine_", ""]
    return ["| " + " | ".join(kopf) + " |", "|" + " --- |" * len(kopf)] + \
           ["| " + " | ".join(str(x).replace("|", "/") for x in z) + " |" for z in zeilen] + [""]


def betrag_txt(s):
    t = ("%.2f %s" % (abs(s["betrag"]), s["waehrung"])).replace(".", ",")
    if s["gebuehr"] and s["betrag"] < 0:
        t += (" + %.2f Gebuehr" % s["gebuehr"]).replace(".", ",")
    return t


def art_eingang(s):
    if "refund" in s["typ"] or "erstatt" in s["typ"] or "erstatt" in s["text"].lower():
        return "Erstattung: in der EUeR als Minderung gegen den Ursprungsbeleg"
    if s["regel"]["kategorie"] == "Payouts":
        return "Payout: Eigenbeleg, Zertifikat, Kurs am Gutschrifttag"
    return "Payout oder Erstattung: im Dashboard nachsehen"


def zahl_txt(x):
    return ("%.2f" % x).replace(".", ",")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("auszug", nargs="+")
    ap.add_argument("--euer", action="append",
                    help="EUeR-CSV (mehrfach erlaubt). Standard: alle EUeR-<jahr>.csv, die der Zeitraum +- Tage beruehrt")
    ap.add_argument("--ordner", default=str(L.GEWERBE_BELEGE), help="Belegordner-Basis (darin <jahr>/EUeR-<jahr>.csv)")
    ap.add_argument("--von")
    ap.add_argument("--bis")
    ap.add_argument("--tage", type=int, default=10, help="Datumsfenster Beleg gegen Abbuchung (Standard 10)")
    ap.add_argument("--ohne-regel-ab", type=float, help="zusaetzlich Abbuchungen ohne Regel ab diesem Betrag zeigen")
    ap.add_argument("--regeln", default=str(HIER / "regeln.json"))
    ap.add_argument("--out")
    a = ap.parse_args()

    regeln = json.loads(Path(a.regeln).read_text(encoding="utf-8"))
    info = {"zeilen": 0, "status_uebersprungen": 0}
    alle = zusammenfuehren([lies_auszug(p, regeln, info) for p in a.auszug])
    if not alle:
        raise SystemExit("Keine lesbaren Umsaetze gefunden.")
    # Standard-Zeitraum: was der Auszug abdeckt (alle Umsaetze, nicht nur die Gewerbe-Treffer)
    von = L.datum(a.von) if a.von else min(s["datum"] for s in alle)
    bis = L.datum(a.bis) if a.bis else max(s["datum"] for s in alle)
    alle = [s for s in alle if von <= s["datum"] <= bis]
    umsaetze = [s for s in alle if s["regel"]]
    ohne_regel = [s for s in alle if not s["regel"] and a.ohne_regel_ab is not None
                  and s["betrag"] < 0 and abs(s["betrag"]) >= a.ohne_regel_ab]

    rand = L.dt.timedelta(days=a.tage)
    if a.euer:
        euer_pfade = [Path(p) for p in a.euer]
    else:
        euer_pfade = [Path(a.ordner) / str(j) / ("EUeR-%d.csv" % j) for j in range((von - rand).year, (bis + rand).year + 1)]
        euer_pfade = [p for p in euer_pfade if p.exists()]
        if not euer_pfade:
            raise SystemExit("Keine EUeR-CSV fuer %s bis %s unter %s" % (von, bis, a.ordner))
    belege = []
    for p in euer_pfade:
        belege += lies_euer(p)
    fenster = [e for e in belege if von - rand <= e["datum"] <= bis + rand]
    passt_, weicht, nur_betrag, offen_s, offen_e = abgleich(umsaetze, fenster, a.tage)

    ohne_beleg = [s for s in offen_s if s["betrag"] < 0 and not s["regel"].get("zahlungsdienst")]
    dienst = [s for s in offen_s if s["betrag"] < 0 and s["regel"].get("zahlungsdienst")]
    eingang = [s for s in offen_s if s["betrag"] > 0]
    beleg_offen = [fenster[j] for j in sorted(offen_e) if von <= fenster[j]["datum"] <= bis]
    ohne_datei = [e for e in fenster if von <= e["datum"] <= bis
                  and (not e["beleg"] or not (e["ordner"] / e["beleg"]).exists())]
    jahr_hinweis = lambda s, e: "Jahreswechsel: § 11 EStG beachten" if s["datum"].year != e["datum"].year else ""
    d_ = lambda x: x.strftime("%d.%m.%Y")

    z = ["# Beleg-Abgleich %s bis %s" % (d_(von), d_(bis)), "",
         "Auszug: %s · %d Umsaetze gelesen, %d davon Gewerbe-Treffer · EUeR: %s · Fenster +-%d Tage"
         % (", ".join(Path(p).name for p in a.auszug), info["zeilen"], len(umsaetze),
            ", ".join(p.name for p in euer_pfade), a.tage), ""]
    if info["status_uebersprungen"]:
        z += ["%d Umsaetze uebersprungen (Status nicht abgeschlossen, z.B. storniert, abgelehnt, ausstehend)."
              % info["status_uebersprungen"], ""]
    z += ["## Abbuchung ohne Beleg (%d)" % len(ohne_beleg), ""]
    z += tabelle(["Datum", "Text", "Betrag", "Ordner", "Hinweis"],
                 [(d_(s["datum"]), s["text"], betrag_txt(s), s["regel"]["kategorie"], s["regel"].get("hinweis", ""))
                  for s in ohne_beleg])
    z += ["## Eingang ohne Beleg (%d)" % len(eingang), ""]
    z += tabelle(["Datum", "Text", "Betrag", "Was tun"],
                 [(d_(s["datum"]), s["text"], betrag_txt(s), art_eingang(s)) for s in eingang])
    z += ["## Nur ueber den Betrag zugeordnet, pruefen (%d)" % len(nur_betrag), "",
          "Zahlungsdienst ohne Haendler im Text, Beleg nur wegen passendem Betrag und Datum gewaehlt. "
          "Im Dienst nachsehen, ob es wirklich dieser Kauf war.", ""]
    z += tabelle(["Abbuchung", "Text", "Ist", "Beleg", "Soll"],
                 [(d_(s["datum"]), s["text"], zahl_txt(ist), "%s %s" % (d_(e["datum"]), e["anbieter"]), zahl_txt(soll))
                  for s, e, ist, soll in nur_betrag])
    z += ["## Zahlungsdienst ohne erkennbaren Haendler (%d)" % len(dienst), "",
          "Nicht zuordenbar. Im Dienst nachsehen, was gekauft wurde; privat ist ok, dann ignorieren.", ""]
    z += tabelle(["Datum", "Text", "Betrag", "Hinweis"],
                 [(d_(s["datum"]), s["text"], betrag_txt(s), s["regel"].get("hinweis", "")) for s in dienst])
    z += ["## Betrag weicht ab (%d)" % len(weicht), "",
          "Anbieter und Datum passen, Betrag weicht 3 bis 25 %% ab (Kurs, Gutschrift, Teilzahlung?).", ""]
    z += tabelle(["Abbuchung", "Text", "Ist", "Beleg", "Soll"],
                 [(d_(s["datum"]), s["text"], zahl_txt(ist), "%s %s" % (d_(e["datum"]), e["anbieter"]), zahl_txt(soll))
                  for s, e, ist, soll in weicht])
    z += ["## Beleg ohne Abbuchung im Auszug (%d)" % len(beleg_offen), "",
          "Anderes Konto (vor Revolut, PayPal-Guthaben) oder Abbuchung nach Auszugsende.", ""]
    z += tabelle(["Belegdatum", "Anbieter", "EUR", "Notiz"],
                 [(d_(e["datum"]), e["anbieter"], zahl_txt(e["eur"]),
                   "Abbuchung evtl. nach Auszugsende" if (bis - e["datum"]).days < a.tage else "")
                  for e in beleg_offen])
    z += ["## EUeR-Zeile ohne Datei im Ordner (%d)" % len(ohne_datei), ""]
    z += tabelle(["Belegdatum", "Anbieter", "Beleg_Datei"],
                 [(d_(e["datum"]), e["anbieter"], e["beleg"] or "(leer)") for e in ohne_datei])
    if a.ohne_regel_ab is not None:
        z += ["## Abbuchungen ohne Regel ab %s (%d)" % (L.euro(a.ohne_regel_ab), len(ohne_regel)), "",
              "Neuer Gewerbe-Haendler dabei? Dann Regel in regeln.json ergaenzen.", ""]
        z += tabelle(["Datum", "Text", "Betrag"], [(d_(s["datum"]), s["text"], betrag_txt(s)) for s in ohne_regel])
    z += ["## Zugeordnet (%d)" % len(passt_), ""]
    z += tabelle(["Abbuchung", "Beleg", "Anbieter", "Ist", "Soll", "Hinweis"],
                 [(d_(s["datum"]), d_(e["datum"]), e["anbieter"], zahl_txt(ist), zahl_txt(soll), jahr_hinweis(s, e))
                  for s, e, ist, soll in passt_])

    out = Path(a.out) if a.out else Path(a.ordner) / str(bis.year) / "_Abgleich" / ("abgleich_%s.md" % bis.isoformat())
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(z) + "\n", encoding="utf-8")
    print("Zeitraum %s bis %s: %d Gewerbe-Umsaetze, %d zugeordnet, %d nur ueber Betrag"
          % (von, bis, len(umsaetze), len(passt_), len(nur_betrag)))
    print("  ohne Beleg %d | Eingang ohne Beleg %d | Zahlungsdienst unklar %d | Betrag weicht ab %d"
          % (len(ohne_beleg), len(eingang), len(dienst), len(weicht)))
    print("  Beleg ohne Abbuchung %d | EUeR-Zeile ohne Datei %d" % (len(beleg_offen), len(ohne_datei)))
    print("-> %s" % out)


if __name__ == "__main__":
    main()
