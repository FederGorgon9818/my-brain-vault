"""PreToolUse(Bash): harte Waechter fuer Regeln, die bisher "Claude muss dran denken" waren.

1. Box-Sync (-SyncOnly) nur, wenn engine-regression-tester seit der letzten
   Kern-Aenderung "Sync frei" gemeldet hat (Marker regression_ok).
2. hypothesis_bank.py --enqueue nur, wenn pipeline-auditor seit der letzten
   Aenderung an hypothesis_bank.py freigegeben hat (Marker pipeline_ok).
3. Dauerlaeufer nie als Kind der Claude-Session (Job-Object-Falle, Regel 18.08.).
4. runner.log / results/*.json nie komplett einlesen (Token-Disziplin).
Nebenbei: Marker setzen, wenn --push-next / funded_finalize gelaufen sind.

AP151 Punkt 6 (14.09.2026, drei Fehlalarme am 10./11.09.): die Regex liefen
vorher auf dem ganzen rohen Kommandotext, also feuerten sie auch auf
Heredoc-INHALT (Dateiinhalt, keine Kommandozeile), auf `discovery_runner.py
--dry` (Kurzlaeufer, kein Dauerlaeufer) und auf Dateinamen in `grep`/`ls`/
`find`/`diff` (die durchsuchen/listen nur, sie fuehren nichts aus). Deshalb
jetzt: Heredoc-Koerper vor der Pruefung rausschneiden, Kommando in einzelne
Segmente (Trenner `; && || |` / Zeilenumbruch) zerlegen und je Segment pruefen
-- ein Segment, dessen erstes Wort ein reiner Such-/Listbefehl ist, zaehlt fuer
Rule 1-3 nicht als Ausfuehrung, und `--dry` beim Runner ist ausdruecklich frei.

AP398 (15.10.2026): Rule 1 laeuft jetzt auch fuer das PowerShell-Tool (Matcher
`Bash|PowerShell`), sonst war das PowerShell-Tool der ungesperrte Weg zum Box-Sync
(Box-Sync-Teil von AP362; Rule 2-4 bleiben vorerst Bash-only). Und sie feuert nur noch,
wenn das Segment das Skript wirklich STARTET: das Wort direkt vor dem Skriptpfad ist ein
Starter (&, ., -File, powershell, pwsh, /c, iex, Start-Process ...) oder der Pfad steht vorne,
und es ist kein reiner -Stop/-DryRun/-RemoteBase-Testlauf (auch ohne Schalter = Vollmodus
zaehlt, PowerShell-Praefixe wie -Sy auch). Vorher reichte der Skriptname plus irgendein
"-sync" danach: ein Ticket-Text mit "Teil-Sync" im --why wurde am 15.10. als Box-Sync
geblockt, und umgekehrt kamen Vollmodus, `time powershell ...` und `& $p` frei durch. Eine Bash-Umleitung aufs
PowerShell-Tool gibt es bewusst NICHT: die Git-Bash-Falle (MSYS-scp) ist im Skript selbst
behoben (fester Pfad aufs Windows-OpenSSH), eine Umleitung haette ohne diese Aenderung nur
auf das damals ungesperrte PowerShell-Tool geschoben.
"""
from _common import *  # noqa

_INSPECT_CMDS = {"grep", "rg", "ls", "find", "diff", "select-string", "get-childitem",
                 "dir", "wc", "head", "tail"}

# Rule 1 (AP398): wer startet das Sync-Skript wirklich?
# verdict-auditor 16.10.: die erste Fassung (Allowlist fuers ERSTE Wort plus Pflicht-Schalter -Sync)
# liess den gefaehrlichsten Aufruf durch, den Vollmodus OHNE Schalter (synct und startet den Runner),
# dazu `time`/`timeout`/`VAR=1`/`( )` vor powershell, `Measure-Command {& ...}`, `Start-Job`, `& $p`
# und die PowerShell-Praefix-Kuerzung `-Sy`. Jetzt: entscheidend ist das Wort DIREKT VOR dem
# Skriptpfad (oder der Pfad steht vorne), und frei ist nur, was nichts in den Box-Code schreibt.
_SYNC_SCRIPT = re.compile(r"box_provision_discovery\.ps1\b", re.I)
_STARTER_PREV = {"&", ".", "-file", "-filepath", "powershell", "powershell.exe", "pwsh", "pwsh.exe",
                 "/c", "/k", "invoke-expression", "iex", "start-process", "saps", "start"}
_LIVE_BASE = "c:/users/maxlk/projects/trading-data"


def _sync_writes_live(tail):
    """Schalter hinter dem Skriptpfad: -Stop, -DryRun und -RemoteBase auf ein Nicht-Live-Ziel
    schreiben nichts in den Box-Code. Alles andere (auch ganz ohne Schalter = Vollmodus) schon.
    PowerShell nimmt eindeutige Praefixe (-St, -Dr, -R), also per Praefix vergleichen."""
    low = tail.lower()
    toks = re.findall(r"(?<![\w-])-([a-z]+)", low)
    if any(len(t) >= 2 and "stop".startswith(t) for t in toks):
        return False
    if any("dryrun".startswith(t) for t in toks):
        return False
    rb = re.search(r"(?<![\w-])-r[a-z]*\s+[\"']?([^\s\"']+)", low)
    if rb and "remotebase".startswith(re.match(r"-([a-z]+)", rb.group(0)).group(1)) \
            and rb.group(1).rstrip("/") != _LIVE_BASE:
        return False
    return True


def _runs_box_sync(seg, whole=""):
    """True, wenn das Segment box_provision_discovery.ps1 so STARTET, dass es in den Live-Box-Code
    schreibt. Nur erwaehnt (Ticket-Text, Get-Content, Write-Host, Array, Zuweisung) zaehlt nicht."""
    for m in _SYNC_SCRIPT.finditer(seg):
        i = m.start()
        while i > 0 and seg[i - 1] not in " \t{(,=":
            i -= 1
        delim = seg[i - 1] if i > 0 else ""
        before = seg[:i].rstrip(" \t")
        if delim in (",", "="):
            continue                                  # Array-Element oder Zuweisung
        if delim == "(" and before[:-1][-1:].isalnum():
            continue                                  # Methodenaufruf, z.B. ParseFile('...')
        prev = before.split()[-1].strip("\"'({").lower() if before.split() else ""
        first = not before or before.endswith(("{", "("))
        if (first or prev in _STARTER_PREV) and _sync_writes_live(seg[m.end():]):
            return True
    # Pfad in einer Variablen: `$p = '...box_provision_discovery.ps1'; & $p -SyncOnly`
    mv = re.match(r"^\s*[&.]\s*\$\w+", seg)
    if mv and _SYNC_SCRIPT.search(whole) and _sync_writes_live(seg[mv.end():]):
        return True
    return False


def _strip_heredocs(c):
    """Heredoc-Koerper (`<<EOF ... EOF`, `<<'EOF' ... EOF`, `<<-EOF ... EOF`) sind
    Dateiinhalt, keine Kommandozeile -- raus, bevor irgendeine Regex laeuft."""
    return re.sub(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?\n\s*\1\s*(?=\n|$)",
                  "<<HEREDOC>>", c, flags=re.S)


def _segments(c):
    """Einzelne Kommandos aus einer Kette (`;`, `&&`, `||`, `|`, Zeilenumbruch) --
    ein Muster, das nur auf einer ECHTEN Ausfuehrung feuern soll, darf nicht ueber
    diese Grenzen hinweg zwei unabhaengige Fundstellen zusammenlesen."""
    return [s.strip() for s in re.split(r"&&|\|\||[;|\n]", c) if s.strip()]


def _first_word(seg):
    m = re.match(r"^\s*([^\s]+)", seg)
    w = (m.group(1) if m else "").lower()
    return w.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]


def _is_inspect(seg):
    """Segment durchsucht/listet nur (grep/ls/find/diff/...) -- zaehlt fuer
    Rule 1-3 nicht als Ausfuehrung, auch wenn der gesuchte Text zufaellig wie
    ein gefaehrliches Kommando aussieht."""
    return _first_word(seg) in _INSPECT_CMDS


def _exec_segments(c):
    return [s for s in _segments(c) if not _is_inspect(s)]


def _pool_hinweise(inp, exec_segs):
    """AP411 (Regel Max 18.10.2026): startet ein Kommando ein Python-Skript mit eigenem Prozess-Pool ohne
    rechen_bremse, kommt einmal je Datei ein Hinweis (blockt nie). Gilt fuer Bash- und PowerShell-Tool."""
    out_notes = []
    cwd = inp.get("cwd")
    for seg in exec_segs:
        for ziel in py_ziele(seg):
            for basis in [b for b in (cwd, ENGINE) if b]:
                p = Path(ziel) if Path(ziel).is_absolute() else Path(basis) / ziel
                try:
                    if p.is_file() and p.stat().st_size < 600_000 and pool_ohne_bremse(p.read_text(encoding="utf-8", errors="replace")):
                        if hinweis_einmal("pool:" + str(p).lower()):
                            out_notes.append(bremse_hinweis_text(p))
                        break
                except OSError:
                    pass
    return out_notes


def main():
    inp = read_input()
    tool = inp.get("tool_name") or "Bash"
    cmd = (inp.get("tool_input") or {}).get("command") or ""
    if tool == "PowerShell":
        cmd = re.sub(r"`\r?\n", " ", cmd)   # Backtick-Zeilenfortsetzung = eine Zeile
    c_raw = cmd.replace("\\", "/")
    c = _strip_heredocs(c_raw)
    exec_segs = _exec_segments(c)
    sync_run = any(_runs_box_sync(s, c) for s in exec_segs)

    # --- Marker aus dem Kommando ableiten (vor allen Blocks) -----------------
    if re.search(r"inbox_tool\.py.*--push-next", c):
        touch_marker("push_next_at")
    if re.search(r"(funded_finalize|live_finalize)\.py", c):
        touch_marker("finalize_at")

    # --- 1. Box-Sync ohne Regressionstest (Bash UND PowerShell, AP398) ------
    if sync_run:
        core_t, core_f = newest_engine_core()
        ok_t = marker_time("regression_ok")
        if core_t and (ok_t is None or ok_t < core_t):
            deny(
                "STOP (Hook): Box-Sync ohne Regressionstest. Kern-Datei "
                f"'{core_f}' geaendert ({fmt_age(core_t)}), letzte Freigabe durch "
                f"engine-regression-tester: {fmt_age(ok_t)}. Regel 27.08.2026: erst "
                "Agent `engine-regression-tester` laufen lassen. Meldet er 'Sync frei', "
                "setzt er selbst den Marker (python .claude/hooks/mark.py regression_ok), "
                "danach den Sync erneut starten. Meldet er 'Sync STOPPEN': nicht syncen."
            )

    # PowerShell-Tool: bisher nur Rule 1 (Rest von AP362 offen), keine Bash-Regeln auf PS-Syntax.
    if tool != "Bash":
        ps_notes = []
        if sync_run:
            ps_notes.append("Hook: nach dem Sync den Runner neu starten (Stop, Sync, Start), sonst laeuft "
                            "er mit altem Code weiter (Vorfall 28.08.2026, 5,5 h Leerlauf).")
        context("\n".join(ps_notes + _pool_hinweise(inp, exec_segs)), "PreToolUse")

    # --- 2. Enqueue ohne pipeline-auditor -----------------------------------
    if any(re.search(r"hypothesis_bank\.py.*--enqueue", s) for s in exec_segs):
        hb = engine_file("discovery/hypothesis_bank.py")
        hb_t = mtime(hb) if hb else None
        ok_t = marker_time("pipeline_ok")
        if hb_t and (ok_t is None or ok_t < hb_t):
            deny(
                "STOP (Hook): Hypothesen-Jobs gehen auf die Box, aber pipeline-auditor hat "
                f"den aktuellen Stand von hypothesis_bank.py (geaendert {fmt_age(hb_t)}) nicht "
                f"freigegeben (letzte Freigabe {fmt_age(ok_t)}). Regel 25.08.2026: erst Dry-Run + "
                "Agent `pipeline-auditor`. Bei 'keine Blocker' setzt er den Marker "
                "(python .claude/hooks/mark.py pipeline_ok), dann --enqueue erneut."
            )

    # --- 3. Dauerlaeufer als Kind der Session -------------------------------
    # discovery_runner.py mit --dry ist ein Kurzlaeufer (baut/prueft nur Configs,
    # startet keinen 24/7-Loop) -- AP151 P6 gibt das ausdruecklich frei.
    long_runner = any(
        any_re([
            r"start-process",
            r"start_discovery\.ps1",
            r"python[^\n|;&]*\b(app_server|lab_app|hub_app)\.py",
            r"\bHub\.exe",
            r"\bnohup\b",
        ], s)
        or (re.search(r"python[^\n|;&]*\bdiscovery_runner\.py", s) and "--dry" not in s)
        for s in exec_segs
    )
    escaped = any(any_re([r"invoke-cimmethod", r"job_escape", r"^\s*ssh\s", r"hot_reload\.ps1",
                         r"build_exe\.ps1", r"box_provision_discovery\.ps1", r"box_deploy\.ps1",
                         r"claude_unlock", r"--help", r"-Stop\b"], s) for s in exec_segs)
    if long_runner and not escaped:
        deny(
            "STOP (Hook): Das sieht nach einem Dauerlaeufer aus, der als Kind der Claude-Session "
            "starten wuerde (Hub, Lab-Server, Discovery-Runner). Regel 18.08.2026: der Prozess "
            "erbt das Claude-Job-Object und blockiert danach Claude Desktop (0x80070020). Richtig: "
            "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments "
            "@{ CommandLine = '\"<exe>\" <args>'; CurrentDirectory = '<ordner>' } "
            "bzw. aus Python job_escape.spawn([...]). Kurzlaeufer (Backtest, Build, --dry) sind ok."
        )

    # --- 4. Volle Logs / Results einlesen -----------------------------------
    reads_full = any(
        any_re([
            r"(cat|type|get-content|gc)\s+[^\n|;&]*runner\.log(?![^\n|;&]*(-tail|-head|-totalcount|\|\s*(tail|head|grep|select-string)))",
            r"(cat|type|get-content|gc)\s+[^\n|;&]*results/[^\s]*\.json",
            r"(cat|type|get-content|gc)\s+[^\n|;&]*\.claude/projects/[^\s]*\.jsonl",
        ], s)
        for s in exec_segs
    )
    if reads_full:
        deny(
            "STOP (Hook): runner.log, results/*.json und Session-Transkripte werden nie komplett "
            "eingelesen (Token-Disziplin, CLAUDE.md). Stattdessen: `python discovery/inbox_tool.py --pull`, "
            "`python summarize_results.py <results.json>`, Logs nur per `-Tail N` / gezieltem "
            "Select-String, Transkripte nur ueber `.claude/scripts/session_conflicts.py`."
        )

    # --- Hinweise (nicht blockierend) ---------------------------------------
    notes = []
    if re.search(r"(funded_finalize|live_finalize|developer_run)\.py", c):
        notes.append("Hook: paralleler Schreiber (finalize/developer_run). Regel session-guard: "
                     "erst pruefen, ob eine andere Session gerade dasselbe JSON schreibt "
                     "(trading-data ist kein Git-Repo, ein Ueberschreiber ist endgueltig).")
    if sync_run:
        notes.append("Hook: nach dem Sync den Runner neu starten (Stop, Sync, Start), sonst laeuft "
                     "er mit altem Code weiter (Vorfall 28.08.2026, 5,5 h Leerlauf).")
    notes += _pool_hinweise(inp, exec_segs)
    context("\n".join(notes), "PreToolUse")


run(main)
