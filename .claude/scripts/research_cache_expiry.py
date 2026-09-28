"""Wiedervorlage fuer Recherche-Befunde, die altern (Max' Vault, 28.09.2026).

Anlass: Strategie-Logbuch #074 hielt am 10.08.2026 fest, es gebe "kein Paper zu
Prop-Firm-First-Passage-Sizing". Am 28.09.2026 lagen fuenf Preprints genau dazu vor.
Entweder gab es sie zum Suchdatum noch nicht, oder die Suche hat sie nicht gesehen
(Lim 2026a ist von Juli, SSRN war damals wie heute oft gesperrt) -- in beiden Faellen
ist ein Negativbefund eine Momentaufnahme. Die Research-Cache-Regel "gueltig Stand ->
nach 60 Tagen neu pruefen" galt nur fuer Preise/Firmenregeln und wurde nirgends
geprueft (logbook-distiller, 28.09.2026).

Dieses Skript ist der Verbraucher der Regel. Es listet, was aelter als die Schwelle ist:
  1. Negativbefunde ("kein Paper / keine Studie / nicht gefunden") im Research-Cache
     und Recherche-Negativbefunde im Strategie-Logbuch,
  2. zeitkritische Cache-Zeilen (Firmenregeln, Preise, Kosten, Termine).
Bewusst nur Meldeliste, kein Blocker: SessionStart zeigt eine Zeile, der retro-agent
liest sonntags die volle Liste. Ein Blocker wuerde jede Recherche-Session ausbremsen.
Der eigentliche Schutz sitzt beim Leser (research-scout, konzept-weg): Negativbefund
aelter als 60 Tage -> neu suchen statt zitieren.

Datum einer Zeile = das spaeteste aus: `##`-Ueberschrift, aktueller `###`-Unterabschnitt,
Pruef-Marker in der Zeile ("geprueft TT.MM.JJJJ", "gueltig Stand ..."), im Logbuch ein
direkt folgender "> **Nachtrag TT.MM.JJJJ"-Block. Bei Negativbefunden zaehlen Daten im
Fliesstext bewusst nicht (das sind meist Paper-Daten); bei Firmenregel-Zeilen schon
(Support-Mail vom ..., AP-Klaerung vom ...). Ein ganzer Abschnitt gilt als neu geprueft,
wenn seine Ueberschrift ein spaeteres Datum traegt ("... geprueft 25.10.2026").

Nutzung (Vault-Root):
    python .claude/scripts/research_cache_expiry.py [--today JJJJ-MM-TT] [--all] [--json] [--days N]
    python .claude/scripts/research_cache_expiry.py --quiet      # eine Zeile, leer wenn nichts faellig
    python .claude/scripts/research_cache_expiry.py --selftest   # synthetische Faelle + echte Dateien
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
# Schwellen (Max, 28.09.2026): Negativbefunde 45 Tage (60 haetten #074 nicht gefangen, der
# Fund kam nach 49 Tagen), Firmenregeln/Preise weiter 60 Tage wie die alte Cache-Regel.
NEG_DAYS = 45
ZEIT_DAYS = 60
SOON_DAYS = 14
# Die SessionStart-Zeile zaehlt Firmenregeln nur fuer die aktiven Firmen (Max, 28.09.2026),
# alle anderen stehen in der vollen Liste (Sonntags-Retro). Neue Firma gekauft -> hier ergaenzen
# (gehoert zur CLAUDE.md-Regel "Neues Konto oder neue Firma -> Regeln pruefen").
ACTIVE_FIRMS = "E8, FundedNext"
ACTIVE_FIRMS_RX = re.compile(r"\bE8\b|SimFi|fundednext|\bFN\b", re.I)
SHOW = 25  # je Kategorie, Rest per --all (nie still kappen: der Rest wird gezaehlt)

DATE = r"(\d{1,2})\.(\d{1,2})\.(\d{4})"
_DATE_RX = re.compile(DATE)
# Marker, die eine Zeile als (neu) geprueft datieren.
_MARK_RX = re.compile(r"(?:g(?:ü|ue)ltig\s+Stand|gepr(?:ü|ue)ft|Stand|recherchiert|Nachtrag)\s*:?\s*" + DATE, re.I)
_NACHTRAG_RX = re.compile(r"Nachtrag\s*:?\s*" + DATE, re.I)

# Negativbefund = "wir haben gesucht und nichts gefunden".
# Stark: die Suche selbst ist ausgesprochen ("... gefunden", "existiert kein").
NEG_STRONG_RX = re.compile(
    r"negativbefund"
    r"|\bkein(?:e|en|er|es)?\b[^|]{0,150}?\b(?:gefunden\w*|auffindbar|identifiziert)"
    r"|\b(?:nicht|nirgends)\s+(?:gefunden|auffindbar)\b"
    r"|\bexistiert\s+(?:in\s+)?(?:kein\w*|nicht)\b",
    re.I)
# Schwach: "keine (akademische) Studie ...". Dieselbe Form steht aber oft als Qualitaetsnotiz
# zu einer GEFUNDENEN Quelle ("kein Peer-Review", "keine Primaerquelle", "kein OOS-Split im
# Paper", "keine Quelle noetig") -- die sind ausgeschlossen (verdict-auditor, Runde 1 und 2).
NEG_WEAK_RX = re.compile(
    r"\bkein(?:e|en|er)?\s+(?:[\w-]+\s+){0,2}?(?:paper|studie|studien|arbeit|quelle|treffer|beleg\w*|evidenz)\b", re.I)
_WEAK_EXCL_RX = re.compile(
    r"n(?:ö|oe)tig|im\s+paper|direkt\s+gelesen|im\s+volltext|von\s+\w+\s+selbst|externe\s+quelle|peer-?review", re.I)


def is_neg(line):
    if NEG_STRONG_RX.search(line):
        return True
    for m in NEG_WEAK_RX.finditer(line):
        if not _WEAK_EXCL_RX.search(line[m.start():m.end() + 40]):
            return True
    return False
# Literatur-Bezug: im Logbuch Pflicht (sonst ist es ein Trading-Negativbefund, den die
# Todesurteil-Pflicht in guard_chain.py regelt), in Firmenabschnitten entscheidet er, ob
# eine "kein ... gefunden"-Zeile ein Recherche-Negativbefund oder eine Firmenregel ist.
LIT_RX = re.compile(r"\b(?:paper|papers|studie|studien|literatur|akademisch\w*|ssrn|arxiv|journal|peer-?review\w*)\b", re.I)
# Abschnitte, deren Inhalt von selbst veraltet (Regeln, Preise, Kosten, Termine).
FIRM_HDR_RX = re.compile(
    r"g(?:ü|ue)ltig\s+Stand|prop-?firm|\bE8\b|fundednext|ftmo|bulenox|tradeify|topstep|\bapex\b|mffu"
    r"|take\s+profit\s+trader|kommission|databento|algo-?erlaubnis|handelszeiten|payout|\bpreise?\b(?!-)|kosten"
    r"|makro-kalender|k(?:ä|ae)fig",
    re.I)
# Literatur-Abschnitte ueber Prop Firms (z.B. "Prop-Firm-Paper: akademische Literatur") sind
# keine Firmenregeln, auch wenn der Firmenname in der Ueberschrift steht.
_LIT_HDR_RX = re.compile(r"\b(?:literatur|akademisch\w*)\b", re.I)
_SEP_RX = re.compile(r"^\|\s*:?-{3}")


def _is_firm_hdr(h):
    return bool(FIRM_HDR_RX.search(h)) and not _LIT_HDR_RX.search(h)


def _date(m):
    try:
        return dt.date(int(m[2]), int(m[1]), int(m[0]))
    except (ValueError, TypeError):
        return None


def _dates(rx, text):
    return [d for d in (_date(g) for g in rx.findall(text or "")) if d]


def _clean(line, width=120):
    s = line.strip()
    if s.startswith("|"):
        s = s.strip("|").split(" | ")[0]  # nur die Claim-Spalte
    s = re.sub(r"[*_`]+", "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return s if len(s) <= width else s[:width].rsplit(" ", 1)[0] + " …"


def scan_cache(text, label="Research-Cache.md"):
    """Zeilen des Research-Caches, die altern koennen."""
    lines = text.splitlines()
    out = []
    h2 = h3 = ""
    h2_date = h3_date = None
    firm2 = firm3 = False
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            h2, h3 = line[3:].strip(), ""
            d = _dates(_DATE_RX, h2)
            h2_date, h3_date = (max(d) if d else None), None
            firm2, firm3 = _is_firm_hdr(h2), False
            continue
        if line.startswith("### "):
            h3 = line[4:].strip()
            d = _dates(_DATE_RX, h3)
            h3_date = max(d) if d else None
            firm3 = _is_firm_hdr(h3)
            continue
        s = line.lstrip()
        if not h2 or not s or s.startswith(("#", ">", "---")):
            continue  # Vorspann/Regeln, Ueberschriften, Ausloeser-Bloecke, Trenner
        is_row = s.startswith("|")
        if is_row:
            if _SEP_RX.match(s):
                continue
            if i < len(lines) and _SEP_RX.match(lines[i].lstrip()):
                continue  # Kopfzeile einer Tabelle (naechste Zeile ist der |---|-Trenner)
            if re.match(r"^\|\s*~~", s):
                continue  # durchgestrichen = schon ersetzt, der Nachfolger steht darunter
        firm = firm2 or firm3 or bool(re.search(r"g(?:ü|ue)ltig\s+Stand", line, re.I))
        neg = is_neg(line)
        if not is_row:
            # Fliesstext nur mit ausdruecklichem "Negativbefund" oder Negativbefund MIT
            # Literaturbezug ("Ehrliche Kernluecke: kein gefundenes Paper ..."), sonst wuerde
            # jede Erlaeuterung mit "kein" gemeldet.
            if not (re.search(r"negativbefund", line, re.I) or (neg and LIT_RX.search(line))):
                continue
        if neg and (not firm or LIT_RX.search(line)):
            kind = "neg"
            marks = _dates(_MARK_RX, line)  # nur Pruef-Marker, Paper-Daten zaehlen nicht
        elif firm:
            kind = "zeit"
            marks = _dates(_DATE_RX, line)  # Bestaetigungsdaten (Support-Mail, AP-Klaerung) zaehlen
        else:
            continue
        cand = [d for d in (h2_date, h3_date, *marks) if d]
        sec = f"{h2} / {h3}" if h3 else h2
        out.append(dict(kind=kind, file=label, line=i, date=max(cand) if cand else None, dates=cand,
                        section=sec, text=_clean(line), raw=line))
    return out


# "keine Arbeit quantifiziert ..." ist selbst ein Literaturbezug, auch ohne "Paper"/"Studie"
# (sonst fiele der Momentum-Korrelations-Befund aus #074 durch, verdict-auditor Runde 2).
_LIT_NEG_RX = re.compile(r"\bkein\w*\s+(?:[\w-]+\s+){0,2}?(?:paper|studie|studien|arbeit|arbeiten)\b", re.I)


def _threshold(it, days=None):
    return days if days is not None else (NEG_DAYS if it["kind"] == "neg" else ZEIT_DAYS)


def _is_active(it):
    return bool(ACTIVE_FIRMS_RX.search(it.get("raw", "")) or ACTIVE_FIRMS_RX.search(it.get("section", "")))


def scan_logbook(text, label="Strategie-Logbuch.md"):
    """Recherche-Negativbefunde im Logbuch (Negativbefund UND Literatur-Bezug)."""
    lines = text.splitlines()
    out, sec, sec_date = [], "", None
    for i, line in enumerate(lines, 1):
        if line.startswith("## "):
            sec = line[3:].strip()
            d = _dates(_DATE_RX, sec)
            sec_date = max(d) if d else None
            continue
        if line.lstrip().startswith(">"):
            continue  # Nachtrag-Bloecke sind die Erledigung, nicht der Befund
        if not (is_neg(line) and (LIT_RX.search(line) or _LIT_NEG_RX.search(line))):
            continue
        marks = _dates(_MARK_RX, line)
        for nxt in lines[i:i + 3]:  # direkt folgender Nachtrag-Block (bis 3 Zeilen, Leerzeile erlaubt)
            if nxt.lstrip().startswith(">"):
                marks += _dates(_NACHTRAG_RX, nxt)
            elif nxt.strip():
                break
        cand = [d for d in (sec_date, *marks) if d]
        out.append(dict(kind="neg", file=label, line=i, date=max(cand) if cand else None, dates=cand,
                        section=sec, text=_clean(line), raw=line))
    return out


def evaluate(items, today, days=None):
    """days=None: Schwelle je Art (Negativbefund NEG_DAYS, Firmenregel ZEIT_DAYS); sonst fuer alle."""
    due, soon, undated = [], [], []
    for it in items:
        # Nur Daten bis heute zaehlen: ein Termin in der Zukunft ("FOMC 08.12.2027 TENTATIVE")
        # ist kein Pruefdatum und wuerde die Zeile sonst bis 2028 stummschalten (Runde 2).
        past = [d for d in it.get("dates", [it["date"]]) if d and d <= today]
        it["date"] = max(past) if past else None
        if it["date"] is None:
            undated.append(it)
            continue
        age = (today - it["date"]).days
        it["age"] = age
        thr = _threshold(it, days)
        if age > thr:
            due.append(it)
        elif age > thr - SOON_DAYS:
            soon.append(it)
    due.sort(key=lambda x: -x["age"])
    return due, soon, undated


def collect(today, days=None, files=None):
    """(due, soon, undated, errors). Eine fehlende oder unlesbare Datei ist ein FEHLER,
    kein 'nichts faellig' -- sonst waere das Gate still blind (verdict-auditor 28.09.)."""
    items, errors = [], []
    for path, fn in (files or ((CACHE, scan_cache), (LOGBOOK, scan_logbook))):
        try:
            items += fn(Path(path).read_text(encoding="utf-8"), Path(path).name)
        except Exception as e:  # FileNotFoundError, UnicodeDecodeError, ...
            errors.append(f"{Path(path).name}: {type(e).__name__}")
    due, soon, undated = evaluate(items, today, days)
    return due, soon, undated, errors


def summary_from(due, undated, errors, days=None):
    """Text der SessionStart-Zeile (rein, damit der Selbsttest ihn pruefen kann).
    Zaehlt Negativbefunde und Firmenregeln AKTIVER Firmen; andere Firmen nur als Zahl
    (volle Liste im Retro), damit die Zeile kein Dauerrauschen wird (Max, 28.09.2026)."""
    if errors:
        return ("Research-Wiedervorlage BLIND: " + ", ".join(errors) +
                " -- Datei fehlt oder ist unlesbar, das Gate meldet nichts (python .claude/scripts/research_cache_expiry.py).")
    neg = [x for x in due if x["kind"] == "neg"]
    act = [x for x in due if x["kind"] == "zeit" and _is_active(x)]
    other = [x for x in due if x["kind"] == "zeit" and not _is_active(x)]
    n = lambda k, one, many: f"{k} {one if k == 1 else many}"
    bits = []
    if neg:
        bits.append(f"{n(len(neg), 'Negativbefund', 'Negativbefunde')} (aelter als {days or NEG_DAYS} Tage)")
    if act:
        bits.append(f"{n(len(act), 'Regel-Zeile', 'Regel-Zeilen')} aktiver Firmen {ACTIVE_FIRMS} (aelter als {days or ZEIT_DAYS} Tage)")
    if undated:
        bits.append(f"{len(undated)} ohne Datum")
    if not bits:
        return ""
    tail = f", dazu {n(len(other), 'Zeile', 'Zeilen')} anderer Firmen nur im Retro" if other else ""
    return (f"Research-Wiedervorlage: {' und '.join(bits)}{tail}. Vor Wiederverwendung in einer Entscheidung "
            f"neu pruefen (Liste: python .claude/scripts/research_cache_expiry.py).")


def summary_line(today=None, days=None):
    """Eine Zeile fuer den SessionStart-Hook; leer, wenn nichts Relevantes faellig ist."""
    today = today or dt.date.today()
    due, _soon, undated, errors = collect(today, days)
    return summary_from(due, undated, errors, days)


def _fmt(it):
    age = f"{it['age']} T" if "age" in it else "ohne Datum"
    d = it["date"].strftime("%d.%m.%Y") if it["date"] else "?"
    sec = _clean(it["section"], 70)
    tag = " [aktive Firma]" if it["kind"] == "zeit" and _is_active(it) else ""
    return f"  {it['file']}:{it['line']}{tag}  ({age}, {d}, „{sec}“)\n      {it['text']}"


def report(today, days=None, show_all=False):
    due, soon, undated, errors = collect(today, days)
    neg = [x for x in due if x["kind"] == "neg"]
    zeit = sorted([x for x in due if x["kind"] == "zeit"], key=lambda x: (not _is_active(x), -x["age"]))
    P = print
    thr = f"{days} Tage fuer alles" if days is not None else f"Negativbefunde {NEG_DAYS} Tage, Firmenregeln {ZEIT_DAYS} Tage"
    P(f"Research-Wiedervorlage, Stand {today.strftime('%d.%m.%Y')}, Schwelle {thr}")
    for e in errors:
        P(f"  !! BLIND: {e} (Datei fehlt oder ist unlesbar, Ergebnis unvollstaendig)")
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
        P("\nErledigen: Befund neu pruefen (research-scout), dann in der Zeile „geprüft TT.MM.JJJJ“ ergaenzen, "
          "oder den ganzen Abschnitt ueber seine Ueberschrift („… geprüft TT.MM.JJJJ“). Im Logbuch: "
          "„> **Nachtrag TT.MM.JJJJ:** …“ direkt unter die Zeile.")
    elif not errors:
        P("\nNichts faellig.")
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Selbsttest: synthetische Faelle UND Anker in den echten Dateien. Der erste Bau hatte
# nur synthetische Faelle, die genau auf die Regex zugeschnitten waren -- die echten
# Dateien haetten die ###-Datierung und "kein Peer-Review" sofort entlarvt.
# ---------------------------------------------------------------------------
def _synthetic():
    today = dt.date(2026, 9, 28)
    cache = "\n".join([
        "## ORB (recherchiert 28.07.2026)",                                                          # 1
        "| Claim | Quelle | Status |",                                                               # 2
        "|---|---|---|",                                                                             # 3
        "| Keine akademische Studie zu X gefunden | [a](u) | praktiker/Negativbefund |",            # 4 neg, faellig
        "| Kein Paper zu Y gefunden | [b](u) | praktiker · geprüft 20.09.2026 |",                   # 5 neg, erledigt
        "| Effekt Z ist signifikant (Paper vom 20.04.2026) | [c](u) | bestätigt |",                # 6 ignoriert
        "| Effekt Q belegt | [c](u) | bestätigt (Preprint, kein Peer-Review) |",                   # 7 ignoriert
        "### #070 Nachbarschaft, recherchiert 09.08.2026",                                           # 8
        "| Kein dediziertes Paper zu einem Cross-Market-VWAP-Spread zwischen zwei Index-Futures als Signal gefunden | u | x |",  # 9 neg, Datum 09.08
        "## Prop-Firmen (gültig Stand 28.07.2026 — nach 60 Tagen neu prüfen!)",                     # 10
        "| E8 Target 6 % | [d](u) | bestätigt |",                                                    # 11 zeit, faellig
        "| Firma | Preis |",                                                                         # 12 Kopfzeile
        "|---|---|",                                                                                 # 13
        "| ~~E8 Regel alt~~ | ersetzt |",                                                            # 14 durchgestrichen
        "| E8 Support-Chat (11.09.2026) bestaetigt DD | x |",                                        # 15 zeit, 11.09
        "| OneUp Trader 100k (kein 50k gefunden) | x |",                                             # 16 zeit (Firma, kein Lit-Bezug)
        "**Negativbefund:** Payout-Grenze je Tier nicht belegt.",                                    # 17 Fliesstext, zeit
        "## Tradeify Mails (Mails 20.07.2026, eingearbeitet 01.09.2026)",                           # 18
        "| Support bestaetigt Regel | [e](u) | bestätigt |",                                         # 19 zeit, 01.09
        "## Bulenox (gültig Stand 28.07.2026, geprüft 25.09.2026)",                                  # 20
        "| VPS verboten | x | bestätigt |",                                                          # 21 zeit, 25.09
        "## Methodik (recherchiert 28.07.2026)",                                                     # 22
        "| Effekt A | u | praktiker, keine Primärquelle |",                                          # 23 ignoriert (Qualitaetsnotiz)
        "| Effekt B, kein OOS-Split im Paper | u | bestätigt |",                                     # 24 ignoriert (Qualitaetsnotiz)
        "**Ehrliche Kernlücke:** kein gefundenes Paper testet PCA auf N=4.",                         # 25 neg (Fliesstext mit Lit-Bezug)
        "## Makro-Kalender 2027 (recherchiert 23.08.2026)",                                          # 26
        "| FOMC 2027: 27.01.2027, 08.12.2027 (TENTATIVE) | u | bestätigt |",                        # 27 zeit, Zukunftsdaten zaehlen nicht
        "## Prop-Firm-Paper: akademische Literatur zu Prop Firms (recherchiert 28.09.2026)",        # 28
        "| Lim 2026a bewertet Challenges | u | bestätigt (kein Peer-Review) |",                     # 29 ignoriert (Literatur, keine Firmenregel)
        "## Gamma (recherchiert 16.08.2026)",                                                        # 30
        "### Gamma-Flip als diskrete Preis-Schwelle (recherchiert 16.08.2026)",                      # 31
        "| Studie zeigt Z | u | bestätigt |",                                                        # 32 ignoriert ('Preis-Schwelle' ist kein Preis)
    ])
    log = "\n".join([
        "## #074 — Alpha durch Fehlersuche (10.08.2026)",                                            # 1
        "Negativbefunde: **kein Paper zu Prop-Firm-Sizing** existiert (nur Blog-Rechner)",          # 2 erledigt durch Nachtrag
        "",                                                                                          # 3
        "> **Nachtrag 28.09.2026:** ueberholt, fuenf Preprints.",                                    # 4
        "## #050 — Volumen (20.07.2026)",                                                            # 5
        "Negativbefund: keine akademische Studie zu Volumen-Filtern gefunden",                       # 6 faellig
        "Negativbefund: kein Kandidat im Grid gefunden",                                             # 7 Trading, ignoriert
        "- **keine Arbeit quantifiziert Korrelation X↔Y**",                                         # 8 neg ("keine Arbeit" = Lit-Bezug)
    ])
    c = {x["line"]: x for x in scan_cache(cache)}
    l = {x["line"]: x for x in scan_logbook(log)}
    due, _s, _u = evaluate(list(c.values()) + list(l.values()), today)
    dk = {(x["file"], x["line"]) for x in due}
    C, L = "Research-Cache.md", "Strategie-Logbuch.md"
    return [
        ("syn Cache: alter Negativbefund faellig", (C, 4) in dk and c[4]["kind"] == "neg"),
        ("syn Cache: 'geprüft' in der Zeile erledigt sie", (C, 5) not in dk and c[5]["kind"] == "neg"),
        ("syn Cache: normaler Claim nicht gemeldet", 6 not in c),
        ("syn Cache: 'kein Peer-Review' ist kein Negativbefund", 7 not in c),
        ("syn Cache: ###-Unterabschnitt datiert (09.08., nicht 28.07.)", c.get(9, {}).get("date") == dt.date(2026, 8, 9)),
        ("syn Cache: 'Kein dediziertes Paper ... gefunden' (>80 Zeichen) erkannt", c.get(9, {}).get("kind") == "neg"),
        ("syn Cache: gültig-Stand-Abschnitt zeitkritisch und faellig", c.get(11, {}).get("kind") == "zeit" and (C, 11) in dk),
        ("syn Cache: Tabellen-Kopfzeile nicht gemeldet", 12 not in c),
        ("syn Cache: durchgestrichene Zeile nicht gemeldet", 14 not in c),
        ("syn Cache: Bestaetigungsdatum in Firmenregel-Zeile zaehlt", c.get(15, {}).get("date") == dt.date(2026, 9, 11) and (C, 15) not in dk),
        ("syn Cache: Firmenzeile 'kein 50k gefunden' ist Firmenregel, kein Negativbefund", c.get(16, {}).get("kind") == "zeit"),
        ("syn Cache: Fliesstext-Negativbefund wird gelesen", 17 in c),
        ("syn Cache: Ueberschrift mit zwei Daten nimmt das spaetere", c.get(19, {}).get("date") == dt.date(2026, 9, 1) and (C, 19) not in dk),
        ("syn Cache: 'geprüft' in der Ueberschrift erledigt den Abschnitt", c.get(21, {}).get("date") == dt.date(2026, 9, 25) and (C, 21) not in dk),
        ("syn Cache: 'keine Primärquelle' als Qualitaetsnotiz ignoriert", 23 not in c),
        ("syn Cache: 'kein OOS-Split im Paper' ignoriert", 24 not in c),
        ("syn Cache: Fliesstext 'kein gefundenes Paper' mit Lit-Bezug ist Negativbefund", c.get(25, {}).get("kind") == "neg"),
        ("syn Cache: Zukunftsdaten schalten nicht stumm (FOMC 2027 am 23.10.2026 faellig)",
         c.get(27, {}).get("kind") == "zeit" and bool(evaluate([dict(c[27])], dt.date(2026, 10, 23))[0])
         and not evaluate([dict(c[27])], dt.date(2026, 9, 28))[0]),
        ("syn Cache: Literatur-Abschnitt ueber Prop Firms ist keine Firmenregel", 29 not in c),
        ("syn Cache: 'Preis-Schwelle' macht keinen Preis-Abschnitt", 32 not in c),
        ("syn Logbuch: Nachtrag darunter erledigt den Befund", l.get(2, {}).get("date") == dt.date(2026, 9, 28) and (L, 2) not in dk),
        ("syn Logbuch: offener Recherche-Negativbefund faellig", (L, 6) in dk),
        ("syn Logbuch: Trading-Negativbefund ohne Literaturbezug ignoriert", 7 not in l),
        ("syn Logbuch: 'keine Arbeit quantifiziert ...' wird erkannt", 8 in l),
        ("syn Schwellen: Negativbefund 45 Tage (46 T faellig, 45 T nicht)",
         bool(evaluate([dict(l[8])], dt.date(2026, 9, 4))[0]) and not evaluate([dict(l[8])], dt.date(2026, 9, 3))[0]),
        ("syn Schwellen: Firmenregel 60 Tage (Zeile vom 28.07. am 26.09. nicht, am 27.09. faellig)",
         not evaluate([dict(c[11])], dt.date(2026, 9, 26))[0] and bool(evaluate([dict(c[11])], dt.date(2026, 9, 27))[0])),
        ("syn Sessionzeile: zaehlt Negativbefunde + aktive Firmen, andere Firmen nur als Zahl", _summary_case()),
        ("syn Logbuch: Nachtrag-Block selbst nicht gemeldet", 4 not in l),
    ]


def _summary_case():
    t = dt.date(2026, 9, 28)
    mk = lambda kind, raw, sec: dict(kind=kind, raw=raw, section=sec, date=dt.date(2026, 7, 1),
                                     dates=[dt.date(2026, 7, 1)], file="x", line=1, text=raw)
    due, _s, und = evaluate([mk("neg", "kein Paper zu X gefunden", "Research"),
                             mk("zeit", "E8 Target 6 %", "Prop-Firmen"),
                             mk("zeit", "Apex 50k EOD", "Prop-Firmen Runde 2")], t)
    line = summary_from(due, und, [])
    only_other = summary_from([x for x in due if "Apex" in x["raw"]], [], [])
    return ("1 Negativbefund " in line and "1 Regel-Zeile aktiver Firmen" in line
            and "1 Zeile anderer Firmen nur im Retro" in line and only_other == "")


def _real():
    """Anker in den echten Dateien, ueber Inhalt statt Zeilennummer gesucht."""
    res = []
    try:
        ctext = CACHE.read_text(encoding="utf-8")
        ltext = LOGBOOK.read_text(encoding="utf-8")
    except Exception as e:
        return [(f"echt: Dateien lesbar ({type(e).__name__})", False)]
    cache = scan_cache(ctext)

    def one(needle):
        hits = [x for x in cache if needle in x["raw"]]
        return hits[0] if hits else None

    # 1. Logbuch #074: mit Nachtrag erledigt; ohne Nachtrag am 10.10. faellig, am 09.10. noch nicht
    lb = [x for x in scan_logbook(ltext) if "Prop-Firm-First-Passage-Sizing" in x["raw"]]
    res.append(("echt Logbuch: #074-Zeile erkannt, Nachtrag datiert sie auf 28.09.", bool(lb) and lb[0]["date"] == dt.date(2026, 9, 28)))
    stripped = "\n".join(l for l in ltext.splitlines() if not re.match(r"^>\s*\*\*Nachtrag 28\.09\.2026", l))
    lb2 = [x for x in scan_logbook(stripped) if "Prop-Firm-First-Passage-Sizing" in x["raw"]]
    ok = False
    if lb2:
        d24, *_ = evaluate([dict(lb2[0])], dt.date(2026, 9, 24))
        d25, *_ = evaluate([dict(lb2[0])], dt.date(2026, 9, 25))
        ok = not d24 and bool(d25)
    res.append(("echt Logbuch: #074 ohne Nachtrag am 25.09. faellig (45 T), am 24.09. nicht", ok))
    mom = [x for x in scan_logbook(ltext) if "Momentum↔Alternative" in x["raw"]]
    res.append(("echt Logbuch: #074 Momentum-Korrelation eigene Zeile, nicht vom Prop-Firm-Nachtrag erledigt",
                bool(mom) and mom[0]["date"] == dt.date(2026, 8, 10)))
    # 2. ###-Datierung an echten Abschnitten (#070 recherchiert 09.08., #073 recherchiert 10.08.)
    t = one("Turtle Soup")
    res.append(("echt Cache: 'Turtle Soup' (### #070) datiert 09.08.", bool(t) and t["date"] == dt.date(2026, 8, 9)))
    b = one("Bulenox 50k Option 2")
    res.append(("echt Cache: 'Bulenox 50k Option 2' (### #073) datiert 10.08.", bool(b) and b["date"] == dt.date(2026, 8, 10)))
    # 3. Klassifikation
    lim = [x for x in cache if "7178078" in x["raw"] or "Price of a Funded Account" in x["raw"]]
    res.append(("echt Cache: Lim 2026a wird weder als Negativbefund noch als Firmenregel gemeldet", not lim))
    pca = one("kein gefundenes Paper testet PCA")
    res.append(("echt Cache: PCA-Kernluecke (Fliesstext) ist Negativbefund", bool(pca) and pca["kind"] == "neg"))
    fomc = one("FOMC-Statement-Tage 2027")
    res.append(("echt Cache: FOMC 2027 (TENTATIVE) am 23.10.2026 faellig, nicht durch Zukunftsdaten stumm",
                bool(fomc) and bool(evaluate([dict(fomc)], dt.date(2026, 10, 23))[0])))
    v = one("Cross-Market-VWAP-Spread")
    res.append(("echt Cache: 'Kein dediziertes Paper ... VWAP-Spread' ist Negativbefund", bool(v) and v["kind"] == "neg"))
    g = one("keine gefundene Studie")
    res.append(("echt Cache: 'keine gefundene Studie' ist Negativbefund", bool(g) and g["kind"] == "neg"))
    e8 = one("E8 Signature Futures 50k: $150")
    due = evaluate([dict(e8)], dt.date(2026, 9, 28))[0] if e8 else []
    res.append(("echt Cache: E8-Kernregel-Zeile vom 28.07. ist am 28.09. faellig", bool(e8) and e8["kind"] == "zeit" and bool(due)))
    # 4. fehlende Datei ist laut, nicht 'nichts faellig'
    errs = collect(dt.date(2026, 9, 28), files=((VAULT / "gibt-es-nicht.md", scan_cache),))[3]
    res.append(("echt: fehlende Datei wird als Fehler gemeldet", bool(errs)))
    return res


def selftest():
    checks = _synthetic() + _real()
    for name, ok in checks:
        print(("OK   " if ok else "FAIL ") + name)
    n = sum(1 for _, ok in checks if ok)
    print(f"\n{n}/{len(checks)} bestanden")
    return 0 if n == len(checks) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=None, help="eine Schwelle fuer alles (Standard: %d Negativbefunde, %d Firmenregeln)" % (NEG_DAYS, ZEIT_DAYS))
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
        due, soon, undated, errors = collect(today, a.days)
        conv = lambda xs: [{**{k: v for k, v in x.items() if k not in ("raw", "dates")},
                            "date": x["date"].isoformat() if x["date"] else None} for x in xs]
        print(json.dumps({"today": today.isoformat(), "days": a.days or {"neg": NEG_DAYS, "zeit": ZEIT_DAYS}, "errors": errors, "due": conv(due),
                          "soon": conv(soon), "undated": conv(undated)}, ensure_ascii=False, indent=1))
        return 1 if errors else 0
    return report(today, a.days, a.all)


if __name__ == "__main__":
    sys.exit(main())
