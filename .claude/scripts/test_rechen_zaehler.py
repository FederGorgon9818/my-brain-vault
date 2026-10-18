"""Selbsttest Wirkungsmessung Rechen-Hinweis (rechen_zaehler.py, rechen_report.py), Auftrag Max 18.10.2026.

  python .claude/scripts/test_rechen_zaehler.py

Prueft die Zahlen-Erkennung (Datum, Uhrzeit, Ticket, Commit, Datei, Code zaehlen nicht), die Python-Erkennung,
den Zug-Eintrag auf synthetischen Transkripten, den echten Aufruf von on_stop.py (auch mit fehlendem Modul)
und die Auswertung.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOKS))
sys.path.insert(0, str(SCRIPTS))
import rechen_hinweis as RH  # noqa: E402
import rechen_report as RR  # noqa: E402
import rechen_zaehler as RZ  # noqa: E402
import schlusszeilen as SZ  # noqa: E402

N = {"ok": 0, "fail": 0}


def check(cond, msg):
    N["ok" if cond else "fail"] += 1
    if not cond:
        print(f"FAIL  {msg}")


# Text, erwartete gezaehlte Zahlen
ZAHLEN = [
    ("Erledigt am 18.10.2026 um 14:30, siehe AP411, #136 und KF-61.", []),
    ("Commit c8c59f0 und 52d4136 sind drin.", []),
    ("Siehe [schlusszeilen.py:62](.claude/hooks/schlusszeilen.py:62) und `python -c \"print(3*7)\"`.", []),
    ("Lauf:\n```\npython x.py --days 7\n12 passed\n```\nFertig.", []),
    ("1. Erst das\n2. Dann das\n3) Zuletzt das", []),
    ("Teil 6 plus Stufe 2, Abschnitt 0b und Schritt 3.", []),
    ("Stand Mitte 2026, Daten ab 2024.", []),
    ("Datei Daily Notes/2026-10-18.md, Sprint S2026-41, Konto E8, k1, Gate v4.", []),
    ("Am 3. Oktober 2026 und um 12 Uhr.", []),
    ("Quelle https://example.com/a/2026/10/5 steht drin.", []),
    ("Das sind 3.600 € brutto im Monat.", ["3.600"]),
    ("Die Quote liegt bei 34 %, nach 12,5 Monaten.", ["34", "12,5"]),
    ("Bis 50k fehlen 0,0147 je Tag.", ["50", "0,0147"]),
    ("Konto bei $52.300, davon 2000 $ Puffer.", ["52.300", "2000"]),
    ("Das waren 959 Trades in 3 Jahren.", ["959", "3"]),
    ("", []),
]

PY_JA = [
    'python -c "print(1)"',
    'cd "C:/x y" && python .claude/scripts/a.py --days 7',
    "PYTHONIOENCODING=utf-8 python - <<'EOF'\nprint(1)\nEOF",
    '& "C:\\Python312\\python.exe" x.py',
    "py -3 x.py",
    "echo 1 | python3 -c 'import sys'",
    "$env:X=1; python a.py",
    "C:/Users/maxlk/AppData/Local/Programs/Python/Python312/python.exe a.py",
    "'C:/Program Files/Python/python.exe' a.py",
    "timeout 300 python a.py",
    "for f in a b; do python x.py $f; done",
    'ssh Administrator@100.127.89.9 "python -c 1"',
    'powershell -Command "python a.py"',
    'bash -c "cd x && python a.py"',
]
PY_NEIN = [
    'ssh box "dir"',
    'ssh box "grep python x.log"',
    "grep -n 'python' a.txt",
    "Get-Process python",
    "grep -rn python .claude/hooks",
    "cat rechen_zaehler.py",
    'git commit -m "python fix"',
    "pip list",
    "node x.js",
    "ls .venv/Scripts/python-docs",
    "echo python",
    "",
]


def turn(prompt, text, cmds=(), tools=()):
    rows = [{"type": "user", "message": {"content": prompt}}]
    blocks = [{"type": "tool_use", "id": f"t{i}", "name": "Bash", "input": {"command": c}} for i, c in enumerate(cmds)]
    blocks += [{"type": "tool_use", "id": f"x{i}", "name": n, "input": {}} for i, n in enumerate(tools)]
    rows.append({"type": "assistant", "message": {"content": blocks + [{"type": "text", "text": text}]}})
    return [json.dumps(r) for r in rows]


def zeilen(path):
    p = Path(path) / RH.LOG_NAME
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()] if p.is_file() else []


def on_stop(engine, tp, sid, hooks=HOOKS, aktiv=False, letzte=None):
    inp = {"session_id": sid, "transcript_path": str(tp), "stop_hook_active": aktiv}
    if letzte:
        inp["last_assistant_message"] = letzte
    # CLAUDE_PROJECT_DIR auf den Wegwerf-Ordner: sonst findet on_stop (Teil 4 haengt VAULT/.claude/hooks vorne an den
    # Suchpfad) das Modul im echten Vault, auch wenn der Negativtest es aus der Kopie geloescht hat.
    return subprocess.run([sys.executable, str(hooks / "on_stop.py")], input=json.dumps(inp), capture_output=True,
                          text=True, encoding="utf-8", timeout=120,
                          env=dict(os.environ, MAXLAB_ENGINE=str(engine), CLAUDE_PROJECT_DIR=str(Path(engine).parent)))


def main():
    # --- Zahlen-Erkennung -------------------------------------------------------------------
    for text, want in ZAHLEN:
        got = RZ.zahlen(text)
        check(got == want, f"zahlen({text[:50]!r}) = {got}, erwartet {want}")
    for c in PY_JA:
        check(RZ.ruft_python(c), f"python nicht erkannt: {c[:60]!r}")
    for c in PY_NEIN:
        check(not RZ.ruft_python(c), f"Fehlalarm python: {c[:60]!r}")

    # --- turn_info: Kommandos und Tools des Zugs ----------------------------------------------
    t = SZ.turn_info(turn("rechne", "Ergebnis 42.", cmds=["python -c 1"], tools=["Agent", "Read"]))
    check(t["cmds"] == ["python -c 1"] and {"Agent", "Read", "Bash"} <= t["tools"] and t["final"] == "Ergebnis 42.",
          f"turn_info: {t}")
    p, f, c = SZ.last_turn(turn("bau", "ok", tools=["Edit"]))
    check((p, f, c) == ("bau", "ok", True), f"last_turn nach Umbau: {(p, f, c)}")

    # --- Zug-Eintrag auf synthetischen Transkripten ---------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        st = Path(tmp) / ".claude_hooks"
        r = RZ.zaehle(st, "aaaaaaaa11", turn("wie lang noch", "Das sind noch 3.600 Minuten."))
        check(r and r["rechen_ohne_code"] and not r["python"] and not r["hinweis"] and r["zahlen"] == 1, f"Zahlen ohne Code: {r}")
        r = RZ.zaehle(st, "aaaaaaaa11", turn("wie lang noch 2", "Das sind noch 3.600 Minuten.", cmds=['cd x && python -c "print(60*60)"']))
        check(r and not r["rechen_ohne_code"] and r["python"] and r["zahlen"] == 1, f"Zahlen mit Code: {r}")
        r = RZ.zaehle(st, "aaaaaaaa11", turn("leg ab", "Erledigt, die Datei liegt im Vault, siehe AP411."))
        check(r and not r["rechen_ohne_code"] and r["zahlen"] == 0, f"keine Zahlen: {r}")
        r = RZ.zaehle(st, "aaaaaaaa11", turn("mach", "Fertig.", tools=["Agent"]))
        check(r and r["agent"], f"agent-Feld: {r}")
        r = RZ.zaehle(st, "aaaaaaaa11", turn("zahl", "ohne Zahl im Text"), last_msg="Es sind 42 Stueck.")
        check(r and r["rechen_ohne_code"], f"last_assistant_message hat Vorrang: {r}")
        # Hinweis kam: Log-Zeile von rechen_hinweis.py, gleiche Session, gleicher Prompt (auch mit Zusatzbloecken davor)
        RH.hinweis("wie viel kostet das im Jahr", "bbbbbbbb22", st)
        r = RZ.zaehle(st, "bbbbbbbb22", turn("<ide_opened_file>x.md</ide_opened_file> wie viel kostet das im Jahr", "Das sind 1.285 Euro."))
        check(r and r["hinweis"] and r["rechen_ohne_code"], f"Hinweis erkannt: {r}")
        r = RZ.zaehle(st, "cccccccc33", turn("wie viel kostet das im Jahr", "Das sind 1.285 Euro."))
        check(r and not r["hinweis"], f"fremde Session bekommt den Hinweis nicht zugeschrieben: {r}")
        # Zwischenmeldung: Hintergrund-Agent gestartet, noch nicht zurueck -> nichts geschrieben
        offen = [json.dumps(x) for x in [
            {"type": "user", "message": {"content": "Go"}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "toolu_A", "name": "Agent", "input": {}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "toolu_A",
                                                      "content": [{"type": "text", "text": "Async agent launched successfully."}]}]}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "Laeuft, 3 Agents, ich warte."}]}}]]
        n0 = len(zeilen(st))
        check(RZ.zaehle(st, "dddddddd44", offen) is None and len(zeilen(st)) == n0, "Zwischenmeldung darf nicht zaehlen")
        # Agent-Rueckmeldung ueberschreibt den Max-Prompt nicht, Python aus dem ersten Teil des Zugs bleibt gezaehlt
        lang = turn("rechne das", "Zwischenstand", cmds=["python a.py"]) + [
            json.dumps({"type": "user", "message": {"content": "<agent-message from=\"x\">fertig</agent-message>"}}),
            json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": "Endergebnis 7 Dateien."}]}})]
        r = RZ.zaehle(st, "eeeeeeee55", lang)
        check(r and r["prompt"] == "rechne das" and r["python"] and not r["rechen_ohne_code"], f"Agent-Rueckmeldung: {r}")
        # kaputte Eingabe: wirft nie, schreibt in hook_errors.log
        check(RZ.zaehle(st, "ffffffff66", None) is None, "kaputte Eingabe muss None geben")
        err = st / "hook_errors.log"
        check(err.is_file() and "rechen_zaehler" in err.read_text(encoding="utf-8"), "Fehler fehlt in hook_errors.log")
        # Mehrfach-Stop zum selben Prompt (Hook blockte, danach kam eine Nachmeldung mit python-Aufruf): es zaehlt die erste Zeile
        a1 = RZ.zaehle(st, "gggggggg77", turn("gleicher Prompt", "Es sind 12 Stueck."))
        a2 = RZ.zaehle(st, "gggggggg77", turn("gleicher Prompt", "Es sind 12 Stueck.", cmds=["python x.py"]))
        h, z = RR.lade(st / RH.LOG_NAME, "2000-01-01 00:00:00")
        gleiche = [x for x in z if x["sid"] == "gggggggg" and x["prompt"] == "gleicher Prompt"]
        check(len(gleiche) == 1 and gleiche[0]["rechen_ohne_code"] and not a2["hinweis"] and not a1["hinweis"],
              f"Dedupe im Report (erste Zeile zaehlt): {gleiche}")
        check(all("rechen_ohne_code" not in x for x in h) and len(h) == 1, f"Hinweis-Zeilen getrennt: {len(h)}")
        # Reset je Prompt: python im ersten Zug darf den zweiten nicht entlasten
        zwei = turn("erster Prompt", "Ergebnis 5.", cmds=["python a.py"]) + turn("zweiter Prompt", "Das sind 7 Dateien.")
        for i, line in enumerate(zwei):
            if '"user"' in line:
                rec = json.loads(line)
                rec["uuid"] = f"uuid-{i}"
                zwei[i] = json.dumps(rec)
        r = RZ.zaehle(st, "hhhhhhhh88", zwei)
        check(r and r["prompt"] == "zweiter Prompt" and not r["python"] and r["rechen_ohne_code"], f"python aus frueherem Zug: {r}")
        # gleichlautende Prompts ("ja") mit verschiedener uuid sind verschiedene Zuege
        def ja(uuid, text):
            return [json.dumps({"type": "user", "uuid": uuid, "message": {"content": "ja"}}),
                    json.dumps({"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}})]
        RZ.zaehle(st, "iiiiiiii99", ja("u-1", "Erster Lauf: 12 Dateien."))
        RZ.zaehle(st, "iiiiiiii99", ja("u-2", "Zweiter Lauf: 40 Dateien."))
        h, z = RR.lade(st / RH.LOG_NAME, "2000-01-01 00:00:00")
        check(len([x for x in z if x["sid"] == "iiiiiiii"]) == 2, "gleichlautende Prompts duerfen nicht zusammenfallen")
        # Belege: erste Zahlen samt Umfeld, ohne Datum und Code
        b = RZ.belege("Am 18.10.2026 waren es `42` Trades, davon 12 im Plus und 3,5 % Verlust, dazu 99 Stueck.", n=3)
        check(len(b) == 3 and "12" in b[0] and "3,5" in b[1] and all(len(x) <= 60 for x in b), f"belege: {b}")
        check(r["beleg"] == ["Das sind 7 Dateien."], f"beleg-Feld: {r['beleg']}")

    # --- Report ---------------------------------------------------------------------------------
    jetzt = time.strftime("%Y-%m-%d %H:%M:%S")

    def zug(sid, ph, hin, roc, py=False, ts=jetzt, prompt="p"):
        return {"ts": ts, "sid": sid, "ph": ph, "prompt": f"{prompt} {ph}", "hinweis": hin, "python": py,
                "agent": False, "zahlen": 2 if roc else 0, "rechen_ohne_code": roc}

    mit = [zug("s1", f"m{i}", True, i == 0) for i in range(4)]
    ohne = [zug("s2", f"o{i}", False, i < 3) for i in range(6)]
    dup_alt, dup_neu = zug("s3", "dup", False, True), zug("s3", "dup", False, False, py=True)
    hin = [{"ts": jetzt, "sid": "s1", "prompt": "wie viel", "fund": "wie viel"}] * 5
    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / RH.LOG_NAME
        alt = zug("s9", "alt", False, True, ts="2000-01-01 00:00:00")
        selbsttest = [zug("testsess", "t1", True, True), {"ts": jetzt, "sid": "testsess", "prompt": "Rechne", "fund": "Rechne"}]
        log.write_text("\n".join([json.dumps(x) for x in [alt, *mit, *ohne, dup_alt, dup_neu, *hin, *selbsttest]]
                                 + ["{kaputt", "[1, 2]", ""]), encoding="utf-8")
        h, z = RR.lade(log, "2001-01-01 00:00:00")
        check(len(h) == 5 and len(z) == 11, f"lade: {len(h)} Hinweise, {len(z)} Zuege (erwartet 5 und 11, Selbsttest-Zeilen raus)")
        txt = RR.bericht(h, z, 7, "2001-01-01 00:00:00", 3)
        check("Hinweise: 5" in txt and "Zuege mit Antwort: 11" in txt, "Kopfzeile")
        check("1 von 4 = 25 %" in txt and "4 von 7 = 57 %" in txt, f"Quoten mit und ohne Hinweis (erste Zeile je Zug):\n{txt}")
        check(jetzt[:10] in txt and "1/4" in txt and "4/7" in txt, "Tagestabelle")
        check("toter Winkel" in txt and "Gruppe ohne Hinweis: unter" in txt, "Hinweise im Bericht")
        check("Basis vor dem Hinweis" in txt and "Noch kein Urteil ueber die Wirkung: 4 von 100" in txt
              and "schliesst die Basis ein" in txt, f"Basis und Urteilsgrenze im Bericht:\n{txt}")
        check(txt.count("'p o") == 2 and "'p dup'" in txt,
              f"Stichprobe der Zuege ohne Hinweis (die letzten 3 von 4: o1, o2, dup): {txt.count(chr(39) + 'p o')}")
        # Vergleich mit der Basis: 100 Zuege mit Hinweis, 5 mit Zahlen ohne Code (5 %) liegen ganz unter der Basis (26 %)
        viele = [zug("s5", f"v{i}", True, i < 5) for i in range(100)]
        txt2 = RR.bericht([], viele, 7, "2001-01-01 00:00:00", 3)
        check("ganz unter der Basis" in txt2 and "Noch kein Urteil" not in txt2, f"Vergleich ganz unter der Basis:\n{txt2}")
        # Belege erscheinen in der Stichprobe
        mit_beleg = [dict(zug("s6", "b1", True, True), beleg=["Das sind 7 Dateien."])]
        check("Belege: Das sind 7 Dateien." in RR.bericht([], mit_beleg, 7, "2001-01-01 00:00:00", 3), "Belege in der Stichprobe")
        env = dict(os.environ, MAXLAB_ENGINE=tmp)
        os.makedirs(Path(tmp) / ".claude_hooks", exist_ok=True)
        shutil.copy(log, Path(tmp) / ".claude_hooks" / RH.LOG_NAME)
        r = subprocess.run([sys.executable, str(SCRIPTS / "rechen_report.py"), "--days", "7"], capture_output=True, text=True,
                           encoding="utf-8", env=env, timeout=60)
        check(r.returncode == 0 and "Hinweise: 5" in r.stdout, f"CLI: exit {r.returncode} {r.stdout[:120]!r} {r.stderr[-200:]!r}")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([sys.executable, str(SCRIPTS / "rechen_report.py")], capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, MAXLAB_ENGINE=tmp), timeout=60)
        check(r.returncode == 0 and "kein Log" in r.stdout, f"CLI ohne Log: {r.stdout[:120]!r}")
    check(RR.quote(0, 0) == "keine Zuege" and "0 von 3 = 0 %" in RR.quote(0, 3), "quote() Randfaelle")

    # --- echter Aufruf on_stop.py -----------------------------------------------------------------
    lang = "Das ist die Auswertung. " + "Viel Inhalt zur Aufgabe, 3.600 Euro im Monat. " * 20   # >= 600 Zeichen, ohne Schlusszeilen
    with tempfile.TemporaryDirectory() as tmp:
        eng, tp = Path(tmp) / "engine", Path(tmp) / "t.jsonl"
        eng.mkdir()
        tp.write_text("\n".join(turn("erklaer mir kurz den Unterschied", lang)) + "\n", encoding="utf-8")
        r = on_stop(eng, tp, "tst-" + uuid.uuid4().hex)
        rows = zeilen(eng / ".claude_hooks")
        check(r.returncode == 0 and len(rows) == 1 and rows[0]["rechen_ohne_code"], f"on_stop schreibt die Zug-Zeile: exit {r.returncode} {rows}")
        check('"decision": "block"' in r.stdout and "Schlusszeilen" in r.stdout, f"Teil 6 blockt weiter: {r.stdout[:200]!r}")
        # Negativfall: Modul fehlt -> Teil 6 blockt trotzdem, Fehler steht in hook_errors.log, nichts geschrieben
        kopie, eng2 = Path(tmp) / "hooks", Path(tmp) / "engine2"
        shutil.copytree(HOOKS, kopie, ignore=shutil.ignore_patterns("__pycache__", ".state"))
        (kopie / "rechen_zaehler.py").unlink()
        eng2.mkdir()
        r = on_stop(eng2, tp, "tst-" + uuid.uuid4().hex, hooks=kopie)
        err = eng2 / ".claude_hooks" / "hook_errors.log"
        check(r.returncode == 0 and '"decision": "block"' in r.stdout and err.is_file() and "rechen_zaehler" in err.read_text(encoding="utf-8")
              and not zeilen(eng2 / ".claude_hooks"),
              f"fehlendes Modul: exit {r.returncode}, block {'block' in r.stdout}, Log {err.is_file()}")
        # Python lief im Zug -> Zeile ohne Flag
        tp.write_text("\n".join(turn("rechne es", lang, cmds=["python rechne.py"])) + "\n", encoding="utf-8")
        eng3 = Path(tmp) / "engine3"
        eng3.mkdir()
        on_stop(eng3, tp, "tst-" + uuid.uuid4().hex, aktiv=True)
        rows = zeilen(eng3 / ".claude_hooks")
        check(len(rows) == 1 and rows[0]["python"] and not rows[0]["rechen_ohne_code"], f"on_stop mit python im Zug: {rows}")
        # Teil 7 blockt nie: kurze Antwort mit Zahl, nichts zu beanstanden -> keine Ausgabe, Zeile trotzdem geschrieben
        tp.write_text("\n".join(turn("sag kurz Hallo", "Hallo, das waren 3 Sachen.")) + "\n", encoding="utf-8")
        eng4 = Path(tmp) / "engine4"
        eng4.mkdir()
        r = on_stop(eng4, tp, "tst-" + uuid.uuid4().hex)
        rows = zeilen(eng4 / ".claude_hooks")
        check(r.returncode == 0 and r.stdout.strip() == "" and len(rows) == 1 and rows[0]["rechen_ohne_code"],
              f"Teil 7 darf allein nie ausgeben oder blocken: exit {r.returncode} {r.stdout[:150]!r} {rows}")

    total = N["ok"] + N["fail"]
    print(f"{N['ok']}/{total} gruen")
    return N["fail"]


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
