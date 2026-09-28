"""Wiedervorlage fuer Recherche-Befunde, die altern (Max' Vault, 28.09.2026).

Anlass: Strategie-Logbuch #074 hielt am 10.08.2026 fest, es gebe "kein Paper zu
Prop-Firm-First-Passage-Sizing". Sieben Wochen spaeter lagen fuenf Preprints genau dazu
vor (Nachtrag 28.09.2026) -- das Feld existierte zum Suchdatum schlicht noch nicht.
Die Research-Cache-Regel "gueltig Stand -> nach 60 Tagen neu pruefen" galt nur fuer
Preise/Firmenregeln und wurde nirgends geprueft (logbook-distiller, 28.09.2026).

Dieses Skript ist der Verbraucher der Regel. Es listet, was aelter als die Schwelle ist:
  1. Negativbefunde ("kein Paper / keine Studie / nicht gefunden") im Research-Cache
     und Recherche-Negativbefunde im Strategie-Logbuch,
  2. zeitkritische Cache-Zeilen (gueltig Stand, Firmenregeln, Preise, Kosten).
Bewusst nur Meldeliste, kein Blocker: SessionStart zeigt eine Zeile, der retro-agent
liest sonntags die volle Liste. Ein Blocker wuerde jede Recherche-Session ausbremsen.

Erledigt ist eine Zeile, wenn sie nach erneuter Pruefung "geprueft TT.MM.JJJJ" traegt
(auch "gueltig Stand TT.MM.JJJJ"; im Logbuch zaehlt ein direkt folgender
"> **Nachtrag TT.MM.JJJJ" -Block). Das Datum einer Zeile ist das spaeteste aus
Abschnitts-Ueberschrift und diesen Markern -- Paper-Datumsangaben im Text zaehlen nicht.

Nutzung (Vault-Root):
    python .claude/scripts/research_cache_expiry.py [--days 60] [--today JJJJ-MM-TT] [--all] [--json]
    python .claude/scripts/research_cache_expiry.py --quiet      # eine Zeile, leer wenn nichts faellig
    python .claude/scripts/research_cache_expiry.py --selftest
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT = Path(__file__).resolve().parents[2]
CACHE = VAULT / "Ressourcen" / "Research-Cache.md"
LOGBOOK = VAULT / "Bereiche" / "Strategie-Logbuch.md"
DEFAULT_DAYS = 60
SOON_DAYS = 14
SHOW = 25  # je Kategorie, Rest per --all (nie still kappen: der Rest wird gezaehlt)

DATE = r"(\d{1,2})\.(\d{1,2})\.(\d{4})"
_DATE_RX = re.compile(DATE)
# Marker, die eine Zeile als (neu) geprueft datieren. Paper-Daten im Fliesstext
# ("SSRN, 20.04.2026") sind KEIN Marker, sonst wuerde ein altes Paper einen Befund
# kuenstlich altern oder verjuengen lassen.
_MARK_RX = re.compile(r"(?:g(?:ü|ue)ltig\s+Stand|gepr(?:ü|ue)ft|Stand|recherchiert|Nachtrag)\s*:?\s*" + DATE, re.I)
_GUELTIG_RX = re.compile(r"g(?:ü|ue)ltig\s+Stand\s*:?\s*" + DATE, re.I)

# Negativbefund = "wir haben gesucht und nichts gefunden". Bewusst eng, damit die
# Liste nicht jede Zeile mit dem Wort "kein" meldet.
NEG_RX = re.compile(
    r"negativbefund"
    r"|\bkein(?:e|en|er)?\b[^|]{0,80}?\b(?:gefunden|auffindbar|identifiziert)\b"
    r"|\b(?:nicht|nirgends)\s+(?:gefunden|auffindbar)\b"
    r"|\bexistiert\s+(?:keine?|nicht)\b"
    r"|\bkein(?:e|en)?\s+(?:einzig\w*\s+)?(?:paper|studie|arbeit|prim(?:ä|ae)rquelle|akademisch\w*|peer-?review\w*)\b",
    re.I)
# Im Logbuch nur RECHERCHE-Negativbefunde; Trading-Negativbefunde ("kein Kandidat")
# regelt die Todesurteil-Pflicht (guard_chain.py), nicht diese Liste.
LIT_RX = re.compile(r"\b(?:paper|papers|studie|studien|literatur|akademisch\w*|ssrn|arxiv|journal|peer-?review\w*)\b", re.I)
# Abschnitte, deren Inhalt von selbst veraltet (Regeln, Preise, Kosten, Termine).
FIRM_HDR_RX = re.compile(
    r"g(?:ü|ue)ltig\s+Stand|prop-?firm|\bE8\b|fundednext|ftmo|bulenox|tradeify|topstep|\bapex\b|mffu"
    r"|take\s+profit\s+trader|kommission|databento|algo-?erlaubnis|handelszeiten|payout|\bpreise?\b|kosten"
    r"|makro-kalender",
    re.I)


def _date(m):
    try:
        return dt.date(int(m[2]), int(m[1]), int(m[0]))
    except (ValueError, TypeError):
        return None


def _dates(rx, text):
    return [d for d in (_date(g) for g in rx.findall(text or "")) if d]


def _clean(line, width=120):
    s = line.strip().strip("|").strip()
    s = s.split(" | ")[0] if line.lstrip().startswith("|") else s  # nur die Claim-Spalte
    s = re.sub(r"[*_`]+", "", s)
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= width else s[:width].rsplit(" ", 1)[0] + " …"


def scan_cache(text, label="Research-Cache.md"):
    """Zeilen des Research-Caches, die altern koennen: (kind, label, zeile, datum, abschnitt, text)."""
    lines = text.splitlines()
    out, sec, sec_date, sec_firm = [], "", None, False
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            sec = line[3:].strip()
            g = _dates(_GUELTIG_RX, sec)
            allh = _dates(_DATE_RX, sec)
            sec_date = (g[-1] if g else (max(allh) if allh else None))
            sec_firm = bool(FIRM_HDR_RX.search(sec))
            continue
        if not line.startswith("|") or re.match(r"^\|\s*:?-{3}", line):
            continue
        if i < len(lines) and re.match(r"^\|\s*:?-{3}", lines[i]):
            continue  # Kopfzeile einer Tabelle (die naechste Zeile ist der |---|-Trenner)
        if re.match(r"^\|\s*~~", line):
            continue  # durchgestrichen = schon ersetzt, der Nachfolger steht darunter
        if NEG_RX.search(line):
            kind = "neg"
            marks = _dates(_MARK_RX, line)  # nur Pruef-Marker, Paper-Daten zaehlen nicht
        elif sec_firm or _GUELTIG_RX.search(line):
            kind = "zeit"
            marks = _dates(_DATE_RX, line)  # Bestaetigungsdaten (Support-Mail, AP-Klaerung) zaehlen
        else:
            continue
        cand = [d for d in [sec_date] + marks if d]
        when = max(cand) if cand else None
        out.append(dict(kind=kind, file=label, line=i, date=when, section=sec, text=_clean(line)))
    return out


def scan_logbook(text, label="Strategie-Logbuch.md"):
    """Recherche-Negativbefunde im Logbuch (Negativbefund UND Literatur-Bezug)."""
    lines = text.splitlines()
    out, sec, sec_date = [], "", None
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            sec = line[3:].strip()
            allh = _dates(_DATE_RX, sec)
            sec_date = max(allh) if allh else None
            continue
        if line.lstrip().startswith(">"):
            continue  # Nachtrag-Bloecke sind die Erledigung, nicht der Befund
        if not (NEG_RX.search(line) and LIT_RX.search(line)):
            continue
        marks = _dates(_MARK_RX, line)
        for nxt in lines[i:i + 3]:  # direkt folgender Nachtrag-Block (bis 3 Zeilen, Leerzeile erlaubt)
            if nxt.lstrip().startswith(">"):
                marks += _dates(re.compile(r"Nachtrag\s*:?\s*" + DATE, re.I), nxt)
            elif nxt.strip():
                break
        cand = [d for d in [sec_date] + marks if d]
        out.append(dict(kind="neg", file=label, line=i, date=max(cand) if cand else None,
                        section=sec, text=_clean(line)))
    return out


def evaluate(items, today, days=DEFAULT_DAYS):
    due, soon, undated = [], [], []
    for it in items:
        if it["date"] is None:
            undated.append(it)
            continue
        age = (today - it["date"]).days
        it["age"] = age
        if age > days:
            due.append(it)
        elif age > days - SOON_DAYS:
            soon.append(it)
    due.sort(key=lambda x: -x["age"])
    return due, soon, undated


def collect(today, days=DEFAULT_DAYS):
    items = []
    for path, fn in ((CACHE, scan_cache), (LOGBOOK, scan_logbook)):
        try:
            items += fn(path.read_text(encoding="utf-8"), path.name)
        except FileNotFoundError:
            pass
    return evaluate(items, today, days)


def summary_line(today=None, days=DEFAULT_DAYS):
    """Eine Zeile fuer den SessionStart-Hook; leer, wenn nichts faellig ist."""
    today = today or dt.date.today()
    due, _soon, undated = collect(today, days)
    n_neg = sum(1 for x in due if x["kind"] == "neg")
    n_zeit = len(due) - n_neg
    if not due and not undated:
        return ""
    bits = []
    if n_neg:
        bits.append(f"{n_neg} Negativbefunde")
    if n_zeit:
        bits.append(f"{n_zeit} Firmenregel-/Preis-Zeilen")
    if undated:
        bits.append(f"{len(undated)} ohne Datum")
    return (f"Research-Wiedervorlage: {' und '.join(bits)} aelter als {days} Tage. Vor Wiederverwendung in "
            f"einer Entscheidung neu pruefen (Liste: python .claude/scripts/research_cache_expiry.py).")


def _fmt(it):
    age = f"{it['age']} T" if "age" in it else "ohne Datum"
    d = it["date"].strftime("%d.%m.%Y") if it["date"] else "?"
    sec = _clean(it["section"], 60)
    return f"  {it['file']}:{it['line']}  ({age}, {d}, „{sec}“)\n      {it['text']}"


def report(today, days=DEFAULT_DAYS, show_all=False):
    due, soon, undated = collect(today, days)
    neg = [x for x in due if x["kind"] == "neg"]
    zeit = [x for x in due if x["kind"] == "zeit"]
    P = print
    P(f"Research-Wiedervorlage, Stand {today.strftime('%d.%m.%Y')}, Schwelle {days} Tage")
    P(f"  faellig: {len(neg)} Negativbefunde, {len(zeit)} Firmenregel-/Preis-Zeilen | "
      f"ohne Datum: {len(undated)} | in den naechsten {SOON_DAYS} Tagen faellig: {len(soon)}")
    for title, rows in (("Negativbefunde (gesucht, nichts gefunden)", neg),
                        ("Zeitkritisch (Firmenregeln, Preise, Kosten, Termine)", zeit),
                        ("Ohne Datum (Abschnitt oder Zeile datieren)", undated)):
        if not rows:
            continue
        P(f"\n{title}:")
        lim = rows if show_all else rows[:SHOW]
        for it in lim:
            P(_fmt(it))
        if len(rows) > len(lim):
            P(f"  (+{len(rows) - len(lim)} weitere, --all zeigt alle)")
    if due or undated:
        P("\nErledigen: Befund neu pruefen (research-scout), dann in der Zeile „geprüft TT.MM.JJJJ“ ergaenzen "
          "oder eine neue Zeile anhaengen und die alte so markieren. Im Logbuch: „> **Nachtrag TT.MM.JJJJ:** …“ "
          "direkt unter die Zeile.")
    else:
        P("\nNichts faellig.")


def selftest():
    today = dt.date(2026, 9, 28)
    cache = "\n".join([
        "## ORB (recherchiert 28.07.2026)",
        "| Claim | Quelle | Status |",
        "|---|---|---|",
        "| Keine akademische Studie zu X gefunden | [a](u) | praktiker/Negativbefund |",            # 4: neg, faellig
        "| Kein Paper zu Y gefunden | [b](u) | praktiker · geprüft 20.09.2026 |",                   # 5: neg, erledigt
        "| Effekt Z ist signifikant (Paper vom 20.04.2026) | [c](u) | bestätigt |",                # 6: normal, ignoriert
        "## Prop-Firmen (gültig Stand 28.07.2026 — nach 60 Tagen neu prüfen!)",
        "| E8 Target 6 % | [d](u) | bestätigt |",                                                  # 8: zeit, faellig
        "| Firma | Preis |",
        "|---|---|",
        "| ~~E8 Regel alt~~ | ersetzt |",
        "| E8 Support-Chat (11.09.2026) bestaetigt DD | x |",
        "## Tradeify Mails (Mails 20.07.2026, eingearbeitet 01.09.2026)",
        "| Support bestaetigt Regel | [e](u) | bestätigt |",                                       # 14: zeit, Datum = spaeteres
        "## Neue Recherche (recherchiert 20.09.2026)",
        "| Kein Paper zu W gefunden (SSRN, 01.01.2020) | [f](u) | Negativbefund |",               # 16: neg, frisch
    ])
    log = "\n".join([
        "## #074 — Alpha durch Fehlersuche (10.08.2026)",
        "Negativbefunde: **kein Paper zu Prop-Firm-Sizing** existiert (nur Blog-Rechner)",        # 2: neg+lit, erledigt durch Nachtrag
        "",
        "> **Nachtrag 28.09.2026:** ueberholt, fuenf Preprints.",
        "## #050 — Volumen (20.07.2026)",
        "Negativbefund: keine akademische Studie zu Volumen-Filtern gefunden",                     # 6: neg+lit, faellig
        "Negativbefund: kein Kandidat im Grid gefunden",                                           # 7: Trading, ignoriert
    ])
    c = {x["line"]: x for x in scan_cache(cache)}
    l = {x["line"]: x for x in scan_logbook(log)}
    due, _s, _u = evaluate(list(c.values()) + list(l.values()), today)
    due_keys = {(x["file"], x["line"]) for x in due}
    checks = [
        ("Cache: alter Negativbefund faellig", ("Research-Cache.md", 4) in due_keys),
        ("Cache: 'geprüft' erledigt die Zeile", ("Research-Cache.md", 5) not in due_keys and c[5]["kind"] == "neg"),
        ("Cache: normaler Claim wird nicht gemeldet", 6 not in c),
        ("Cache: gültig-Stand-Abschnitt ist zeitkritisch und faellig", c.get(8, {}).get("kind") == "zeit" and ("Research-Cache.md", 8) in due_keys),
        ("Cache: Tabellen-Kopfzeile wird nicht gemeldet", 9 not in c),
        ("Cache: durchgestrichene Zeile wird nicht gemeldet", 11 not in c),
        ("Cache: Bestaetigungsdatum in Firmenregel-Zeile zaehlt", c.get(12, {}).get("date") == dt.date(2026, 9, 11) and ("Research-Cache.md", 12) not in due_keys),
        ("Cache: Header mit zwei Daten nimmt das spaetere", c.get(14, {}).get("date") == dt.date(2026, 9, 1) and ("Research-Cache.md", 14) not in due_keys),
        ("Cache: Paper-Datum im Text zaehlt nicht als Pruefdatum", c[16]["date"] == dt.date(2026, 9, 20) and ("Research-Cache.md", 16) not in due_keys),
        ("Logbuch: Nachtrag darunter erledigt den Befund", l[2]["date"] == dt.date(2026, 9, 28) and ("Strategie-Logbuch.md", 2) not in due_keys),
        ("Logbuch: offener Recherche-Negativbefund faellig", ("Strategie-Logbuch.md", 6) in due_keys),
        ("Logbuch: Trading-Negativbefund ohne Literaturbezug ignoriert", 7 not in l),
        ("Logbuch: Nachtrag-Block selbst wird nicht als Befund gemeldet", 4 not in l),
    ]
    ok = True
    for name, res in checks:
        print(("OK   " if res else "FAIL ") + name)
        ok &= bool(res)
    print(f"\n{sum(1 for _, r in checks if r)}/{len(checks)} bestanden")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=DEFAULT_DAYS)
    ap.add_argument("--today", help="JJJJ-MM-TT (Test/Rueckblick)")
    ap.add_argument("--all", action="store_true", help="alle faelligen Zeilen statt der ersten %d je Kategorie" % SHOW)
    ap.add_argument("--quiet", action="store_true", help="eine Zeile fuer Hooks, leer wenn nichts faellig")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    if a.quiet:
        line = summary_line(today, a.days)
        if line:
            print(line)
        return 0
    if a.json:
        due, soon, undated = collect(today, a.days)
        conv = lambda xs: [{**x, "date": x["date"].isoformat() if x["date"] else None} for x in xs]
        print(json.dumps({"today": today.isoformat(), "days": a.days, "due": conv(due),
                          "soon": conv(soon), "undated": conv(undated)}, ensure_ascii=False, indent=1))
        return 0
    report(today, a.days, a.all)
    return 0


if __name__ == "__main__":
    sys.exit(main())
