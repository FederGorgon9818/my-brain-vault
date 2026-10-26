"""Auswertung der Wirkungsmessung fuer den Rechen-Hinweis (Auftrag Max, 18.10.2026).

Liest <STATE>/rechen_hinweis_log.jsonl: die Treffer von rechen_hinweis.py (Hinweis pro Prompt) und die
Zug-Zeilen von rechen_zaehler.py (on_stop.py Teil 7). Zeigt je Tag die Hinweise, die Quote der Zuege mit
Zahlen ohne Code (mit und ohne Hinweis) und eine kleine Stichprobe der Prompts.

  python .claude/scripts/rechen_report.py [--days 7] [--n 8]

Die Quote ist ein Proxy, in beide Richtungen schief: Zahlen, die unveraendert aus einer Datei oder einem
Agent-Ergebnis zitiert werden, zaehlen mit (zu viel). Jeder python-Aufruf im Zug nimmt das Flag weg, auch ein
Test oder ein Pull, Kopfrechnen in so einem Zug bleibt unsichtbar (zu wenig). Die Gruppen mit und ohne Hinweis
sind nicht gleich gebaut (Hinweis-Prompts sind Rechen-Prompts), deshalb wird die Quote mit Hinweis gegen die
Basis vor dem Hinweis gehalten, nicht gegen die uebrigen Zuege. Je Zug gilt die erste Zeile: nach einem
Stop-Hook-Block folgt oft nur noch eine kurze Nachmeldung, die den Zug sonst verfaelschen wuerde.
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from _common import STATE  # noqa: E402

LOG_NAME = "rechen_hinweis_log.jsonl"
MIN_N = 30        # ab so vielen Zuegen ist eine Quote halbwegs lesbar (Gruppe ohne Hinweis)
URTEIL_N = 100    # Zuege mit Hinweis, ab denen ein Urteil ueber die Wirkung traegt (Rechnung unten)
# Basis vor dem Hinweis, am 18.10.2026 aus den Transkripten bis 17.10.2026 nachgerechnet (1184 Zuege in 319 Dateien,
# gleiche Zaehl-Logik wie der Live-Zaehler, je Zug die erste Antwort). Fest eingetragen, weil die Transkripte irgendwann
# aufgeraeumt werden. "mit" = Prompts, bei denen der Hinweis gezuendet haette (im Schnitt 15,1 je Woche).
# Power fuer URTEIL_N: Zwei-Stichproben-Test, einseitig 5 %, Basis als Zufallsgroesse, wahre Quote nach dem Hinweis =
# halbe Basis: n=30 0,46, n=60 0,68, n=100 0,81, n=150 0,89 (ohne Wirkung bleibt der Fehlalarm bei 5 %).
BASIS_STAND = "Transkripte bis 17.10.2026"
BASIS_MIT = (38, 149)     # Zuege mit Zahlen ohne Code, Zuege
BASIS_OHNE = (333, 1035)


def lade(pfad, ab):
    """-> (Hinweis-Zeilen, Zug-Zeilen) seit `ab` (Zeitstempel-String). Kaputte Zeilen werden uebergangen, Zeilen von
    Selbsttests (Session-ID beginnt mit "test", echte IDs sind Hex) ebenso. Ein Zug kann mehrfach stehen (Stop-Hook
    blockte, danach kam eine Nachmeldung): es zaehlt die ERSTE Zeile je Session und Prompt-Eintrag, denn die
    Nachmeldung ist meist kurz, zitiert die Antwort nicht mehr und kommt oft mit einem python-Aufruf (Marker setzen)."""
    hinweise, zuege = [], {}
    with open(pfad, encoding="utf-8", errors="replace") as f:
        for zeile in f:
            try:
                r = json.loads(zeile)
            except Exception:
                continue
            if not isinstance(r, dict) or str(r.get("ts", "")) < ab or str(r.get("sid", "")).startswith("test"):
                continue
            if "rechen_ohne_code" in r:
                zuege.setdefault((r.get("sid"), r.get("ph")), r)
            else:
                hinweise.append(r)
    return hinweise, list(zuege.values())


def wilson(k, n, z=1.96):
    """95-%-Bereich der Quote k/n (Wilson), als Anteile 0 bis 1."""
    p = k / n
    d = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / d
    breite = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return max(0.0, mitte - breite), min(1.0, mitte + breite)


def quote(k, n):
    if not n:
        return "keine Zuege"
    lo, hi = wilson(k, n)
    return f"{k} von {n} = {100 * k / n:.0f} % (95 %-Bereich {100 * lo:.0f} bis {100 * hi:.0f})"


def _zelle(zeilen):
    n = len(zeilen)
    return f"{sum(1 for r in zeilen if r.get('rechen_ohne_code'))}/{n}" if n else "-"


def bericht(hinweise, zuege, tage, ab, n_probe=8):
    """-> Berichtstext."""
    out = [f"Rechen-Hinweis, Wirkung seit {ab} ({tage:g} Tage)",
           f"Hinweise: {len(hinweise)} in {len({r.get('sid') for r in hinweise})} Sessions | "
           f"Zuege mit Antwort: {len(zuege)} in {len({r.get('sid') for r in zuege})} Sessions"]
    mit = [r for r in zuege if r.get("hinweis")]
    ohne = [r for r in zuege if not r.get("hinweis")]

    tage_liste = sorted({str(r.get("ts", ""))[:10] for r in hinweise + zuege})
    if tage_liste:
        out += ["", "Tag         Hinweise  Zuege  mit Hinweis: Zahlen ohne Code  ohne Hinweis: Zahlen ohne Code"]
        for t in tage_liste:
            h = sum(1 for r in hinweise if str(r.get("ts", "")).startswith(t))
            z = [r for r in zuege if str(r.get("ts", "")).startswith(t)]
            out.append(f"{t}  {h:8}  {len(z):5}  {_zelle([r for r in z if r.get('hinweis')]):>26}  "
                       f"{_zelle([r for r in z if not r.get('hinweis')]):>28}")

    k_mit, k_ohne = (sum(1 for r in g if r.get("rechen_ohne_code")) for g in (mit, ohne))
    out += ["", "Zuege mit Zahlen ohne Code (Proxy: zitierte Zahlen aus Dateien und Agents zaehlen mit, Kopfrechnen in Zuegen "
                "mit irgendeinem python-Aufruf bleibt unsichtbar):",
            f"  mit Hinweis : {quote(k_mit, len(mit))}",
            f"  ohne Hinweis: {quote(k_ohne, len(ohne))}  <- toter Winkel"]
    roc = [r for r in zuege if r.get("rechen_ohne_code")]
    if roc:
        out.append(f"  darunter mit Agent oder Workflow im Zug: {sum(1 for r in roc if r.get('agent'))} von {len(roc)} "
                   "(die Zahlen koennen aus dessen Python stammen)")
    out += ["", f"Basis vor dem Hinweis ({BASIS_STAND}, gleiche Zaehl-Logik):",
            f"  Prompts, bei denen der Hinweis gezuendet haette: {quote(*BASIS_MIT)}",
            f"  uebrige Zuege                                  : {quote(*BASIS_OHNE)}"]
    if len(mit) < URTEIL_N:
        out.append(f"  Noch kein Urteil ueber die Wirkung: {len(mit)} von {URTEIL_N} Zuegen mit Hinweis "
                   "(bei halbierter Quote traegt der Vergleich ab etwa 100 Zuegen mit Power 0,81, das sind rund 7 Wochen).")
    if mit:
        lo, hi = wilson(k_mit, len(mit))
        p0 = BASIS_MIT[0] / BASIS_MIT[1]
        lage = ("ganz unter der Basis" if hi < p0 else "ganz ueber der Basis" if lo > p0
                else "schliesst die Basis ein, noch kein Unterschied zu erkennen")
        out.append(f"  Grober Vergleich: der Bereich mit Hinweis liegt {lage} (die Basis hat selbst einen Fehlerbalken).")
    if len(ohne) < MIN_N:
        out.append(f"  Gruppe ohne Hinweis: unter {MIN_N} Zuege, die Quote ist noch nicht lesbar.")

    def probe(zeilen):
        for r in zeilen[-n_probe:]:
            tag = "Zahlen ohne Code" if r.get("rechen_ohne_code") else ("Code" if r.get("python") else "keine Zahlen")
            beleg = " | ".join(r.get("beleg") or [])[:150]
            out.append(f"  {str(r.get('ts', ''))[5:16]} [{tag}, {r.get('zahlen', 0)} Zahlen] {str(r.get('prompt', ''))[:110]!r}"
                       + (f"\n      Belege: {beleg}" if beleg else ""))

    out += ["", f"Stichprobe Prompts mit Hinweis (Fehlalarm-Check), die letzten {min(n_probe, len(mit))}:"]
    probe(mit)
    blind = [r for r in ohne if r.get("rechen_ohne_code")]
    out += ["", f"Stichprobe Zuege mit Zahlen ohne Code und ohne Hinweis (toter Winkel), die letzten {min(n_probe, len(blind))}:"]
    probe(blind)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Wirkung des Rechen-Hinweises")
    ap.add_argument("--days", type=float, default=7)
    ap.add_argument("--n", type=int, default=8, help="Groesse der Stichproben")
    a = ap.parse_args(argv)
    pfad = STATE / LOG_NAME
    if not pfad.is_file():
        print(f"kein Log unter {pfad}")
        return 0
    ab = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - a.days * 86400))
    hinweise, zuege = lade(pfad, ab)
    print(bericht(hinweise, zuege, a.days, ab, a.n))
    err = STATE / "hook_errors.log"
    if err.is_file():
        fehler = [l for l in err.read_text(encoding="utf-8", errors="replace").splitlines()
                  if l[:19] >= ab and ("rechen_zaehler" in l or "rechen_hinweis" in l)]
        print(f"\nHook-Fehler (rechen_*) seit {ab}: {len(fehler)}")
        for l in fehler[-5:]:
            print("  " + l[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
