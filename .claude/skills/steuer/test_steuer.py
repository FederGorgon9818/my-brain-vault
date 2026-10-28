#!/usr/bin/env python3
"""Selbsttest Steuer-Skill mit erfundenen Daten (keine echten Konten). python test_steuer.py"""
import datetime as dt
import subprocess
import sys
import tempfile
from pathlib import Path

HIER = Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import steuerlib as L  # noqa: E402
import fristen as F  # noqa: E402
import homeoffice as HO  # noqa: E402
import werbungskosten as WK  # noqa: E402

D = dt.date.fromisoformat
fehler = []


def check(name, ist, soll):
    if ist != soll:
        fehler.append("%s: ist %r, soll %r" % (name, ist, soll))


def lauf(*args):
    r = subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, encoding="utf-8", cwd=HIER)
    if r.returncode != 0:
        fehler.append("%s: Exit %d %s" % (args[0], r.returncode, r.stderr.strip()[-300:]))
    return r.stdout


def kopf(out, n=3):
    return [z.strip() for z in out.splitlines()[:n]]


# --- Feiertage, Werktage, Monate, Zahlen ------------------------------------
check("Ostern 2026", L.ostersonntag(2026), D("2026-04-05"))
check("Ostern 2027", L.ostersonntag(2027), D("2027-03-28"))
check("Fronleichnam 2026", D("2026-06-04") in L.feiertage_bayern(2026), True)
check("Fronleichnam 2027", D("2027-05-27") in L.feiertage_bayern(2027), True)
check("31.12.2028 So -> 02.01.2029", L.naechster_werktag(D("2028-12-31")), D("2029-01-02"))
check("31.01. + 1 Monat", L.plus_monate(D("2027-01-31"), 1), D("2027-02-28"))
check("zahl deutsch", L.zahl("-1.234,56"), -1234.56)
check("zahl englisch", L.zahl("-1,234.56"), -1234.56)
check("zahl revolut", L.zahl("-107.10", False), -107.10)
check("zahl mit Waehrung", L.zahl("113,00 USD"), 113.0)
check("zahl USD mit Punkt", L.zahl("69.99 USD"), 69.99)

# --- Fristen -----------------------------------------------------------------
r = {j["jahr"]: j["frist"] for j in F.rueckblick(2023, D("2026-10-28"))}
check("Rueckblick", r, {2023: "2027-12-31", 2024: "2029-01-02", 2025: "2029-12-31"})
check("Rueckblick --bis 2025 ab 2027", [j["jahr"] for j in F.rueckblick(2023, D("2027-03-01"), 2025)], [2023, 2024, 2025])
b = F.bescheid(D("2026-10-28"))
check("Bescheid 28.10.26 Bekanntgabe (So + Allerheiligen)", b["bekanntgabe"], "2026-11-02")
check("Bescheid 28.10.26 Frist", b["frist"], "2026-12-02")
check("Bescheid 28.10.26 sicher", b["frist_sicher"], "2026-12-01")
b = F.bescheid(D("2024-06-10"))
check("Bescheid 2024 drei Tage", b["bekanntgabe"], "2024-06-13")
check("Bescheid 2024 Frist Sa -> Mo", b["frist"], "2024-07-15")
check("Fiktion auf Hl. Drei Koenige", F.bescheid(D("2027-01-02"))["bekanntgabe"], "2027-01-07")
check("Frist danach So -> Mo", F.bescheid(D("2027-01-02"))["frist"], "2027-02-08")
check("Fiktion auf Maria Himmelfahrt", F.bescheid(D("2025-08-11"))["frist"], "2025-09-18")
check("Monatsfrist ins Schaltjahr", F.bescheid(D("2028-01-27"))["frist"], "2028-02-29")
check("Bescheid spaeterer Zugang", F.bescheid(D("2026-10-28"), D("2026-11-10"))["frist"], "2026-12-10")

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    # --- Abgleich ------------------------------------------------------------
    euer = tmp / "EUeR-2026.csv"
    dateien = {"c1": "Infrastruktur/c1.pdf", "f1": "Challenges/f1.pdf", "f2": "Challenges/f2.pdf",
               "fs": "Challenges/fs.pdf", "a1": "Infrastruktur/a1.pdf", "c2": "Infrastruktur/c2.pdf",
               "ffn": "Challenges/ffn.pdf", "mffu": "Challenges/mffu.pdf"}
    euer.write_text("\n".join([
        "Datum;Kategorie;Anbieter;Beschreibung;Betrag_Original;Betrag_EUR;Beleg_Datei;Notiz",
        "2026-08-31;Infrastruktur;Contabo;VPS Sept;31,06 EUR;31,06;%s;" % dateien["c1"],
        "2026-09-02;Challenges;FundedNext;Flex A;69,99 USD;60,45;%s;" % dateien["f1"],
        "2026-09-02;Challenges;FundedNext;Flex B;69,99 USD;60,45;%s;" % dateien["f2"],
        "2026-09-03;Challenges;FundedNext;Stellar 100k;470,00 EUR;470,00;%s;" % dateien["fs"],
        "2026-09-06;Infrastruktur;Anthropic;Claude Max;107,10 EUR;107,10;%s;" % dateien["a1"],
        "2026-09-30;Infrastruktur;Contabo;VPS Okt;31,06 EUR;31,06;%s;" % dateien["c2"],
        "2026-10-05;Challenges;Funded Futures Network;150k per PayPal;292,50 USD;261,07;%s;" % dateien["ffn"],
        "2026-10-15;Challenges;My Funded Futures;Core 50k;100,00 EUR;100,00;%s;" % dateien["mffu"],
        "2026-10-20;Challenges;Bulenox;ohne Datei;40,00 USD;35,00;;",
    ]) + "\n", encoding="utf-8")
    for f in dateien.values():
        (tmp / f).parent.mkdir(exist_ok=True)
        (tmp / f).write_text("x")
    rz = lambda typ, tag, text, betrag, waehrung="EUR", status="COMPLETED", fee="0.00": \
        "%s,Current,%s 10:00:00,%s 11:00:00,%s,%s,%s,%s,%s,1" % (typ, tag, tag, text, betrag, fee, waehrung, status)
    rev = tmp / "revolut.csv"
    rev.write_text("\n".join([
        "Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance",
        rz("CARD_PAYMENT", "2026-09-04", "FundedNext", "-69.99", "USD"),
        rz("CARD_PAYMENT", "2026-09-04", "Fundednext.com", "-60.90", fee="0.20"),
        rz("CARD_PAYMENT", "2026-09-03", "Fundednext.com", "-60.45"),
        rz("CARD_PAYMENT", "2026-09-03", "Fundednext.com", "-60.45"),        # echter Doppelkauf
        rz("CARD_PAYMENT", "2026-09-05", "Contabo GmbH", "-16.06"),          # 48 % daneben -> kein Paar
        rz("CARD_PAYMENT", "2026-09-07", "Anthropic", "-100.00"),            # 7 % daneben -> weicht ab
        rz("CARD_PAYMENT", "2026-09-08", "Anthropic", "-107.10", status="REVERTED"),
        rz("CARD_PAYMENT", "2026-09-08", "Anthropic", "-5.00", status="PENDING"),
        rz("EXCHANGE", "2026-09-09", "Exchanged to USD", "-100.00"),
        rz("CARD_PAYMENT", "2026-09-12", "REWE Markt", "-23.40"),
        rz("CARD_PAYMENT", "2026-09-13", "CAFE8 Muenchen", "-4.50"),
        rz("CARD_PAYMENT", "2026-09-14", "Amazon Marketplace", "-129.00"),
        rz("CARD_PAYMENT", "2026-10-05", "Contabo GmbH", "-31.06"),
        rz("CARD_PAYMENT", "2026-10-06", "Funded Futures Network", "-261.07"),
        rz("CARD_PAYMENT", "2026-10-06", "PayPal Europe", "-260.00"),        # darf FFN nicht wegnehmen
        rz("CARD_PAYMENT", "2026-10-14", "PayPal Europe", "-101.50"),
        rz("CARD_PAYMENT", "2026-10-15", "MyFundedFutures", "-100.00"),      # MFFU, nicht FFN
        rz("CARD_PAYMENT", "2026-10-20", "PayPal Europe", "-35.50"),         # nur ueber Betrag -> Bulenox
        rz("CARD_PAYMENT", "2026-10-10", "Databento", "-50.00"),
        rz("CARD_PAYMENT", "2026-10-11", "PayPal *TradingView", "-17.79"),
        rz("CARD_PAYMENT", "2026-10-12", "PayPal Europe", "-9.99"),
        rz("TRANSFER", "2026-10-20", "Payment from RiseWorks Inc", "500.00"),
        rz("CARD_REFUND", "2026-10-22", "Anthropic", "107.10"),
    ]) + "\n", encoding="utf-8")
    bericht = tmp / "bericht.md"
    soll_kopf = ["Zeitraum 2026-09-01 bis 2026-10-31: 17 Gewerbe-Umsaetze, 5 zugeordnet, 1 nur ueber Betrag",
                 "ohne Beleg 5 | Eingang ohne Beleg 2 | Zahlungsdienst unklar 3 | Betrag weicht ab 1",
                 "Beleg ohne Abbuchung 1 | EUeR-Zeile ohne Datei 1"]
    out = lauf("abgleich.py", rev, "--euer", euer, "--von", "2026-09-01", "--bis", "2026-10-31", "--out", bericht,
               "--ohne-regel-ab", "100")
    check("Abgleich Zusammenfassung", kopf(out), soll_kopf)
    text = bericht.read_text(encoding="utf-8") if bericht.exists() else ""
    check("privater Kleinbetrag bleibt draussen", "REWE" in text or "CAFE8" in text, False)
    check("ohne Regel ab 100 sichtbar", "Amazon Marketplace" in text, True)
    check("REVERTED und PENDING gezaehlt", "2 Umsaetze uebersprungen" in text, True)
    check("TradingView vor PayPal erkannt", "PayPal *TradingView | 17,79 EUR | Infrastruktur" in text, True)
    check("MFFU nicht als FFN", "| 15.10.2026 | 15.10.2026 | My Funded Futures |" in text, True)
    check("PayPal nimmt FFN-Beleg nicht weg", "| 06.10.2026 | 05.10.2026 | Funded Futures Network |" in text, True)
    check("Bulenox nur ueber Betrag", "PayPal Europe | 35,50 | 20.10.2026 Bulenox" in text, True)
    check("Stellar 470 nicht als weicht ab", "Stellar" not in text and "| 03.09.2026 | FundedNext | 470,00 |" in text, True)
    check("Erstattung erkannt", "Anthropic | 107,10 EUR | Erstattung" in text, True)
    out = lauf("abgleich.py", rev, rev, "--euer", euer, "--von", "2026-09-01", "--bis", "2026-10-31", "--out", bericht)
    check("Gleiche Datei zweimal zaehlt einmal", kopf(out), soll_kopf)

    de_csv = tmp / "bank.csv"
    de_csv.write_text("Kontoauszug\nZeitraum;01.10.2026 bis 31.10.2026\n\n"
                      "Buchungstag;Name Zahlungsbeteiligter;Verwendungszweck;Betrag (€)\n"
                      "05.10.2026;Contabo GmbH;Rechnung 2868070003;-31,06\n"
                      "06.10.2026;Media Markt;Laptop;-1.234,56\n", encoding="cp1252")
    out = lauf("abgleich.py", de_csv, "--euer", euer, "--out", tmp / "b2.md")
    check("Deutsche Bank-CSV mit Vorspann", kopf(out, 1),
          ["Zeitraum 2026-10-05 bis 2026-10-06: 1 Gewerbe-Umsaetze, 1 zugeordnet, 0 nur ueber Betrag"])

    # Jahreswechsel: Beleg 30.12.2025 im Ordner 2025, Abbuchung 05.01.2026, EUeR automatisch beide Jahre
    for j, zeile in ((2025, "2025-12-30;Infrastruktur;Contabo;VPS Jan;31,06 EUR;31,06;c.pdf;"), (2026, "")):
        (tmp / "belege" / str(j)).mkdir(parents=True)
        (tmp / "belege" / str(j) / ("EUeR-%d.csv" % j)).write_text(
            "Datum;Kategorie;Anbieter;Beschreibung;Betrag_Original;Betrag_EUR;Beleg_Datei;Notiz\n" + zeile + "\n",
            encoding="utf-8")
    (tmp / "belege" / "2025" / "c.pdf").write_text("x")
    jw = tmp / "jw.csv"
    jw.write_text("Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance\n"
                  + rz("CARD_PAYMENT", "2026-01-05", "Contabo GmbH", "-31.06") + "\n", encoding="utf-8")
    out = lauf("abgleich.py", jw, "--ordner", tmp / "belege", "--out", tmp / "jw.md")
    check("Jahreswechsel zugeordnet", kopf(out, 1),
          ["Zeitraum 2026-01-05 bis 2026-01-05: 1 Gewerbe-Umsaetze, 1 zugeordnet, 0 nur ueber Betrag"])
    check("Jahreswechsel-Hinweis", "§ 11 EStG" in (tmp / "jw.md").read_text(encoding="utf-8"), True)

    # --- Homeoffice ----------------------------------------------------------
    ho = tmp / "homeoffice.csv"
    lauf("homeoffice.py", "--datei", ho, "fill", "--von", "2026-07-01", "--bis", "2026-10-28", "--wochentag", "mi",
         "--seite", "gewo", "--ausser", "2026-08-12")
    lauf("homeoffice.py", "--datei", ho, "add", "2026-07-01", "gewerbe")    # Mi, auch GEWO -> beide
    lauf("homeoffice.py", "--datei", ho, "add", "2026-10-31", "gewerbe")    # Sa -> klar
    lauf("homeoffice.py", "--datei", ho, "add", "2026-10-31", "gewerbe")    # doppelt
    lauf("homeoffice.py", "--datei", ho, "add", "2026-10-27", "gewerbe")    # Di, Buerotag -> strittig
    lauf("homeoffice.py", "--datei", ho, "add", "2026-10-29", "gewerbe", "--notiz", "Urlaub")  # Do frei -> klar
    mittwoche = sum(1 for i in range(120) if D("2026-07-01") + dt.timedelta(i) <= D("2026-10-28")
                    and (D("2026-07-01") + dt.timedelta(i)).weekday() == 2) - 1
    s = HO.summe(HO.lies(ho), 2026)
    check("HO gewo-Tage", (s["gewo"], s["beide"], s["wk_tage"]), (mittwoche - 1, 1, mittwoche))
    check("HO gewerbe klar/strittig", (s["gewerbe_klar"], s["gewerbe_strittig"]), (2, 1))
    check("HO Euro ohne strittige Tage", s["euro"], (mittwoche + 2) * 6)

    # --- Werbungskosten ------------------------------------------------------
    wk = tmp / "werbungskosten.csv"
    wk.write_text("art;beschreibung;menge;wert;anteil;beleg;mittel;kauf\n"
                  "pendeln;Wohnung - Betrieb;200;25;;;;\n"
                  "berufsschule;Bus;30;6,00;;;oepnv;\n"
                  "berufsschule;Roller;10;18;;;moped;\n"
                  "berufsschule;ohne Angabe;5;18;;;;\n"
                  "verpflegung;Berufsschule ueber 8 h;20;;;;;\n"
                  "erstattung;Betrieb zahlt Busticket;;50;;;;\n"
                  "arbeitsmittel;Laptop;1;1200,00;50;laptop.pdf;;\n"
                  "arbeitsmittel;Schreibtisch;1;1100,00;100;;;\n"
                  "afa;Schreibtisch;13;1100,00;100;;;2024-10-15\n"
                  "kontofuehrung;Girokonto;;;;;;\n", encoding="utf-8")
    out = lauf("werbungskosten.py", "--jahr", "2024", "--datei", wk, "--z17", "100",
               "--brutto", "11800", "--lst", "120", "--kist", "60", "--rv", "1097", "--kv", "960", "--pv", "200")
    pendel = 200 * (20 * 0.30 + 5 * 0.38)
    teile = [pendel, 30 * 6.0, 10 * 2 * 18 * 0.20, 0.0, 20 * 14, -50.0, 1200 * 50 / 100, 0.0, 1100 / 156 * 3, 16, -100.0]
    check("WK Summe", "**Summe: %s**" % L.euro(sum(teile)) in out, True)
    check("WK AfA erstes Jahr", WK.afa_im_jahr(1100, 13, D("2024-10-15"), 2024), (1100 / 156 * 3, 3))
    check("WK AfA Folgejahr", WK.afa_im_jahr(1100, 13, D("2024-10-15"), 2025)[1], 12)
    check("WK Schreibtisch nicht voll", "als Zeile art=afa eintragen" in out, True)
    check("WK Verkehrsmittel fehlt", "Verkehrsmittel fehlt" in out and "2 Zeile(n) nicht gerechnet" in out, True)
    check("WK Sonderausgaben max(36, KiSt)", "| minus Sonderausgaben (36 EUR oder gezahlte Kirchensteuer) | 60,00 € |" in out, True)
    check("WK Einordnung alles zurueck", "voraussichtlich kommt alles Einbehaltene zurueck" in out, True)
    out = lauf("werbungskosten.py", "--jahr", "2024", "--datei", wk, "--brutto", "30000", "--lst", "3000")
    check("WK Einordnung teilweise", "Erstattung nur teilweise" in out, True)
    out = lauf("werbungskosten.py", "--jahr", "2024", "--datei", wk, "--brutto", "9000", "--lst", "0")
    check("WK Einordnung nichts einbehalten", "Nichts einbehalten" in out, True)
    wk26 = tmp / "wk26.csv"
    wk26.write_text("art;beschreibung;menge;wert;anteil;beleg;mittel;kauf\npendeln;GEWO;20;10;;;;\n", encoding="utf-8")
    out = lauf("werbungskosten.py", "--jahr", "2026", "--datei", wk26)
    check("WK 2026 0,38 ab km 1", "**Summe: %s**" % L.euro(20 * 10 * 0.38) in out, True)

if fehler:
    print("FEHLER (%d):" % len(fehler))
    for f in fehler:
        print("  " + f)
    sys.exit(1)
print("Steuer-Skill Selbsttest: alles gruen")
