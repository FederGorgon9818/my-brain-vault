"""Selbsttest Rechen-Hinweis (.claude/hooks/rechen_hinweis.py), Regel Max 18.10.2026.

  python .claude/scripts/test_rechen_hinweis.py

Prueft die Erkennung (diktierte Rechen-Fragen zuenden, typische Nicht-Rechen-Prompts nicht)
und einmal den echten Hook-Aufruf ueber on_prompt.py mit Stdin-JSON.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
sys.path.insert(0, str(HOOKS))
import rechen_hinweis as RH  # noqa: E402

ZUENDET = [
    "rechne mal aus was mich das im Jahr kostet",
    "Kannst du berechnen, wie viel Puffer FFN2 noch hat?",
    "wie viel sind 3 Prozent von 3600",
    "Wieviel Geld bleibt nach Steuern übrig?",
    "was kostet Claude Max im Jahr, 107,10 € im Monat",
    "Das Konto liegt bei 52.300 $, wie weit ist es bis zum Ziel?",
    "wie viele Tage bis zum 03.07.2027",
    "Wie lange brauchen wir bis 50k?",
    "Monate bis zur BOS, und was bleibt netto",
    "Mach einen Überschlag für die Gründungskosten",
    "Ueberschlag reicht mir",
    "ist 0,0147 * 1,2 richtig?",
    "3600 x 12",
    "rechne 5*7",
    "Durchschnitt der letzten 20 Trades",
    "was heißt das in Euro?",
    "Rendite vom ETF-Sparplan nach 10 Jahren",
    "umrechnen in USD bitte, 333 Dollar",
    "Die Passquote ist 34 %, was heißt das?",
    "Kalkulation für die Kaufrunde",
]

STILL = [
    "lies die Datei Brain Dump",
    "Leg ein Ticket für die Contabo-Rechnung an",
    "Rechnung vom Oktober einsortieren",
    "Bau im Hub einen neuen Button",
    "check die Box",
    "Push das bitte auf master",
    "was steht in AP411?",
    "Commit 52d4136 ansehen",
    "Datum der Daily Note 2026-10-18 prüfen",
    "Termin um 12:30 eintragen",
    "Schreib die Regel in die CLAUDE.md",
    "Der Rechner ist kaputt, schau mal in den Hub-Logs",
    "This session is being continued from a previous conversation. Konto bei 52.300 $, wie viel fehlt?",
]


def hook_lauf(prompt):
    """on_prompt.py echt aufrufen, State in ein Wegwerf-Verzeichnis."""
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, MAXLAB_ENGINE=tmp)
        r = subprocess.run([sys.executable, str(HOOKS / "on_prompt.py")],
                           input=json.dumps({"prompt": prompt, "session_id": "test-rh-0000"}),
                           capture_output=True, text=True, encoding="utf-8", env=env, timeout=60)
        return r.stdout


def main():
    fails = 0
    for p in ZUENDET:
        if not RH.fundstelle(p):
            fails += 1
            print(f"FAIL  zuendet nicht: {p!r}")
    for p in STILL:
        f = RH.fundstelle(p)
        if f:
            fails += 1
            print(f"FAIL  Fehlalarm: {p!r} (Fund {f!r})")
    if RH.hinweis("lies X") != "" or "Python" not in RH.hinweis("wie viel kostet das"):
        fails += 1
        print("FAIL  hinweis() liefert falschen Text")
    with tempfile.TemporaryDirectory() as tmp:
        RH.hinweis("wie viel kostet das", "abcdef123", Path(tmp))
        log = (Path(tmp) / RH.LOG_NAME).read_text(encoding="utf-8")
        if json.loads(log.splitlines()[0]).get("sid") != "abcdef12":
            fails += 1
            print("FAIL  Log-Zeile fehlt oder falsch")
    out = hook_lauf("rechne 5*7")   # kurzer Prompt, laeuft vor dem Laengen-Filter
    if "Rechnen nur in Code" not in out:
        fails += 1
        print(f"FAIL  on_prompt.py gibt den Hinweis bei kurzem Prompt nicht aus: {out[:200]!r}")
    out = hook_lauf("Wie viele Tage sind es noch bis zum Vertragsende am 03.07.2027?")
    if "Rechnen nur in Code" not in out:
        fails += 1
        print(f"FAIL  on_prompt.py gibt den Hinweis bei langem Prompt nicht aus: {out[:200]!r}")
    out = hook_lauf("lies bitte die Datei Brain Dump und fass sie zusammen")
    if "Rechnen nur in Code" in out:
        fails += 1
        print("FAIL  on_prompt.py gibt den Hinweis ohne Rechen-Prompt aus")
    # Negativfall: Modul fehlt -> Typ-Router laeuft weiter, Fehler steht in hook_errors.log
    with tempfile.TemporaryDirectory() as tmp:
        kopie, eng = Path(tmp) / "hooks", Path(tmp) / "engine"
        shutil.copytree(HOOKS, kopie, ignore=shutil.ignore_patterns("__pycache__", ".state"))
        (kopie / "rechen_hinweis.py").unlink()
        eng.mkdir()
        r = subprocess.run([sys.executable, str(kopie / "on_prompt.py")],
                           input=json.dumps({"prompt": "wie viel kostet das im Jahr", "session_id": "test-rh-0001"}),
                           capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, MAXLAB_ENGINE=str(eng)), timeout=60)
        err = eng / ".claude_hooks" / "hook_errors.log"
        if r.returncode != 0 or "Auftrags-Typ" not in r.stdout or not err.exists() or "rechen_hinweis" not in err.read_text(encoding="utf-8"):
            fails += 1
            print(f"FAIL  fehlendes Modul: exit {r.returncode}, Router-Text {'Auftrags-Typ' in r.stdout}, Log {err.exists()}")
    n = len(ZUENDET) + len(STILL) + 6
    print(f"{n - fails}/{n} gruen")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
