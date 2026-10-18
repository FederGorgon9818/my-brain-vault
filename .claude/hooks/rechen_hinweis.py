"""Rechen-Hinweis im Prompt-Hook (Regel Max, 18.10.2026).

Jede Berechnung mit Zahlen und Zeiten laeuft in Python, nie frei im Modell (CLAUDE.md,
Abschnitt "Rechnen nur in Code"). Eine Regel, die nur als Text dasteht, traegt laut
Audit vom 21.09. in 9 bis 56 % der Faelle. Deshalb legt on_prompt.py bei Rechen-Prompts
eine Zeile Erinnerung in den Kontext. Reiner Hinweis, blockt nie.

Locker erkannt, weil Max diktiert ("wie viel", "Prozent", "3600 Euro"). Ein Hinweis zu
viel kostet eine Zeile, einer zu wenig eine falsche Zahl. Jeder Treffer landet in
STATE/rechen_hinweis_log.jsonl, damit die Fehlalarm-Quote abnehmbar ist. Ob der Hinweis wirkt,
misst rechen_zaehler.py (Stop-Hook, on_stop.py Teil 7) in dieselbe Datei, ausgewertet von
.claude/scripts/rechen_report.py.
Tests: python .claude/scripts/test_rechen_hinweis.py
"""
import json
import re
import time

# "Rechnung" (Beleg) und "Rechner" bewusst NICHT, nur das Verb und "Berechnung".
_MUSTER = [
    r"\b(?:be|aus|nach|um|durch|hoch|zusammen|gegen)?rechne(?:n|t|st)?\b",
    r"\bberechnung",
    r"\bkalkul\w*",
    r"\b(?:ü|ue)berschlag\w*",
    r"\bwie ?viel(?:e|en|es)?\b",
    r"\bwie (?:lange|hoch|teuer|gro(?:ß|ss)|weit|oft)\b",
    r"\b(?:summe|durchschnitt\w*|mittelwert|differenz|prozentsatz|zinseszins|rendite|brutto|netto|"
    r"mwst|mehrwertsteuer|umsatzsteuer|einkommensteuer|gewerbesteuer)\b",
    r"\bprozent\w*|\d\s*%",
    r"\d\s*(?:€|eur\b|euro\b)|€\s*\d|\$\s*\d|\d\s*\$|\d\s*(?:usd|dollar)\b|\b(?:euro|dollar)\b",
    r"\b(?:tage|wochen|monate|jahre|stunden|minuten)\s+(?:bis|seit|zwischen)\b",
    r"\d\s*[+*/×]\s*\d|\d\s+x\s+\d",
]
RX = re.compile("|".join(f"(?:{m})" for m in _MUSTER), re.I)

LOG_NAME = "rechen_hinweis_log.jsonl"
# Zusammenfassung nach Kontext-Ueberlauf kommt als Prompt an, ist aber nicht von Max
# (Gegenprobe 18.10. ueber 545 echte Prompts: 73 Treffer, 13 %, einziger klarer Fehlgriff dieser Art).
_NICHT_MAX = re.compile(r"^\s*this session is being continued", re.I)


def fundstelle(prompt):
    """-> kurzer Ausschnitt um den ersten Treffer, oder None."""
    if _NICHT_MAX.search(prompt or ""):
        return None
    m = RX.search(prompt or "")
    if not m:
        return None
    a, b = max(0, m.start() - 20), min(len(prompt), m.end() + 20)
    return " ".join(prompt[a:b].split())


def text(snippet):
    return (f"Hook (Rechnen nur in Code, Regel Max 18.10.2026): der Prompt klingt nach Rechnen "
            f"(Fundstelle: \"{snippet[:70]}\"). Jede Zahl, die nicht unveraendert aus einer Quelle kommt, "
            f"in Python rechnen, alle Zahlen der Antwort in EINEM Aufruf buendeln, Eingaben im Output mit "
            f"anzeigen. Nichts im Kopf rechnen oder umrechnen, auch keine Ueberschlaege.")


def hinweis(prompt, sid=None, state_dir=None):
    """-> Hinweis-Text fuer den Kontext oder "" (kein Rechen-Prompt)."""
    snippet = fundstelle(prompt)
    if not snippet:
        return ""
    if state_dir is not None:
        try:
            state_dir.mkdir(parents=True, exist_ok=True)
            with open(state_dir / LOG_NAME, "a", encoding="utf-8") as f:
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "sid": str(sid or "")[:8],
                                    "prompt": (prompt or "")[:120], "fund": snippet[:70]},
                                   ensure_ascii=False) + "\n")
        except Exception:
            pass
    return text(snippet)
