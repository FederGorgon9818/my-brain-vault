"""Gemeinsame Bausteine fuer den Steuer-Skill (nur Standardbibliothek).

Feiertage Bayern (Finanzamt Erding), Werktag-Verschiebung nach § 108 Abs. 3 AO,
Zahlen- und Datumsleser fuer Bank-CSVs (Revolut englisch/deutsch, deutsche Banken),
Pfade der Steuer-Ablage und die Werte je Jahr.

Idee und Teile der Struktur aus github.com/neubauerwilli/steuer-skill (MIT, Willi Neubauer),
fuer Max' Lage neu gebaut (28.10.2026).
"""
import csv
import datetime as dt
import io
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# Ablage: persoenliche Daten liegen NIE im Vault (der wird gepusht), nur hier.
STEUER = Path(r"C:\Users\maxlk\Documents\Steuer")
KONTOAUSZUEGE = STEUER / "Kontoauszuege"
GEWERBE_BELEGE = Path(r"C:\Users\maxlk\Documents\Gewerbe\Belege")

# Werte je Steuerjahr, Stand 28.10.2026 (Wissen Claude, vor Abgabe gegen bmf/elster pruefen).
# pendel_bis20 / pendel_ab21: Entfernungspauschale je km einfache Strecke und Arbeitstag.
WERTE = {
    2023: dict(pauschbetrag=1230, pendel_bis20=0.30, pendel_ab21=0.38, ho_tag=6, ho_max=1260, grundfreibetrag=10908),
    2024: dict(pauschbetrag=1230, pendel_bis20=0.30, pendel_ab21=0.38, ho_tag=6, ho_max=1260, grundfreibetrag=11784),
    2025: dict(pauschbetrag=1230, pendel_bis20=0.30, pendel_ab21=0.38, ho_tag=6, ho_max=1260, grundfreibetrag=12096),
    2026: dict(pauschbetrag=1230, pendel_bis20=0.38, pendel_ab21=0.38, ho_tag=6, ho_max=1260, grundfreibetrag=12348),
}
REISE_KM = 0.30          # Dienstreise/Auswaertstaetigkeit mit eigenem Pkw je gefahrenem km (Berufsschule)
KONTOFUEHRUNG = 16       # Verwaltungspraxis, ohne Nachweis
GWG_BRUTTO = 952         # 800 netto + 19 %, darueber verteilen (ausser Computer/Software: 1 Jahr)
SONDERAUSGABEN_PAUSCH = 36


def werte(jahr):
    if jahr not in WERTE:
        sys.exit("Keine Werte fuer %s hinterlegt (steuerlib.WERTE). Erst Jahr nachtragen und pruefen." % jahr)
    return WERTE[jahr]


# --- Feiertage und Werktage -------------------------------------------------

def ostersonntag(jahr):
    """Gregorianisch (anonymer Algorithmus)."""
    a, b, c = jahr % 19, jahr // 100, jahr % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    monat = (h + l - 7 * m + 114) // 31
    tag = (h + l - 7 * m + 114) % 31 + 1
    return dt.date(jahr, monat, tag)


def feiertage_bayern(jahr):
    """Gesetzliche Feiertage Bayern inkl. Maria Himmelfahrt (Erding ist ueberwiegend katholisch)."""
    o = ostersonntag(jahr)
    tage = {
        dt.date(jahr, 1, 1): "Neujahr",
        dt.date(jahr, 1, 6): "Heilige Drei Koenige",
        o - dt.timedelta(days=2): "Karfreitag",
        o + dt.timedelta(days=1): "Ostermontag",
        dt.date(jahr, 5, 1): "Tag der Arbeit",
        o + dt.timedelta(days=39): "Christi Himmelfahrt",
        o + dt.timedelta(days=50): "Pfingstmontag",
        o + dt.timedelta(days=60): "Fronleichnam",
        dt.date(jahr, 8, 15): "Maria Himmelfahrt",
        dt.date(jahr, 10, 3): "Tag der Deutschen Einheit",
        dt.date(jahr, 11, 1): "Allerheiligen",
        dt.date(jahr, 12, 25): "1. Weihnachtstag",
        dt.date(jahr, 12, 26): "2. Weihnachtstag",
    }
    return tage


def ist_werktag(tag):
    return tag.weekday() < 5 and tag not in feiertage_bayern(tag.year)


def naechster_werktag(tag):
    """§ 108 Abs. 3 AO: faellt das Ende auf Sa, So oder Feiertag, endet es am naechsten Werktag."""
    while not ist_werktag(tag):
        tag += dt.timedelta(days=1)
    return tag


def plus_monate(tag, n):
    """§ 188 Abs. 2/3 BGB: gleicher Tag im Zielmonat, sonst dessen letzter Tag."""
    m = tag.month - 1 + n
    jahr, monat = tag.year + m // 12, m % 12 + 1
    for t in (tag.day, 30, 29, 28):
        try:
            return dt.date(jahr, monat, t)
        except ValueError:
            continue


WOCHENTAG = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def de(tag):
    return "%s %s" % (WOCHENTAG[tag.weekday()], tag.strftime("%d.%m.%Y"))


# --- Zahlen und Daten aus CSVs ----------------------------------------------

def zahl(text, deutsch=None):
    """'-1.234,56', '-1234.56', '107,10 EUR', '113.00 USD' -> float. deutsch=None: am Text erkennen."""
    t = (text or "").strip()
    t = re.sub(r"[A-Za-z€$\s]", "", t)
    if not t:
        return None
    if "," in t and "." in t:
        deutsch = t.rfind(",") > t.rfind(".")
    elif deutsch is None:
        deutsch = bool(re.search(r",\d{1,2}$", t))
    if deutsch:
        t = t.replace(".", "").replace(",", ".")
    else:
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def waehrung(text):
    m = re.search(r"\b([A-Z]{3})\b", text or "")
    return m.group(1) if m else None


def datum(text):
    t = (text or "").strip()[:19]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d.%m.%Y %H:%M", "%d.%m.%Y", "%d.%m.%y",
                "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return dt.datetime.strptime(t if " " in fmt else t[:10], fmt).date()
        except ValueError:
            continue
    return None


def euro(x):
    s = "{:,.2f}".format(x)
    return s.replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def lies_csv(pfad):
    """Liest eine CSV, erkennt Trenner und Kopfzeile (Banken schreiben oft Vorspann davor).
    Gibt (kopf_klein, zeilen) zurueck."""
    roh = Path(pfad).read_bytes()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            text = roh.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    zeilen = [z for z in text.splitlines() if z.strip()]
    if not zeilen:
        return [], []
    probe = "\n".join(zeilen[:20])
    trenner = max((";", ",", "\t"), key=probe.count)
    reader = list(csv.reader(io.StringIO("\n".join(zeilen)), delimiter=trenner))
    for start, kopf in enumerate(reader[:30]):
        klein = [k.strip().lower() for k in kopf]
        if any(k in klein for k in ("amount", "betrag", "betrag (eur)", "betrag (€)", "umsatz", "betrag_eur")):
            return klein, reader[start + 1:]
    return [k.strip().lower() for k in reader[0]], reader[1:]


def spalte(kopf, namen):
    """Index der ersten passenden Spalte in Reihenfolge der Namensliste (Vorrang zaehlt)."""
    for n in namen:
        if n in kopf:
            return kopf.index(n)
    return None
