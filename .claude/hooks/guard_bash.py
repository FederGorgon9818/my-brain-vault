"""PreToolUse(Bash): harte Waechter fuer Regeln, die bisher "Claude muss dran denken" waren.

1. Box-Sync (-SyncOnly) nur, wenn engine-regression-tester seit der letzten
   Kern-Aenderung "Sync frei" gemeldet hat (Marker regression_ok).
2. hypothesis_bank.py --enqueue nur, wenn pipeline-auditor seit der letzten
   Aenderung an hypothesis_bank.py freigegeben hat (Marker pipeline_ok).
3. Dauerlaeufer nie als Kind der Claude-Session (Job-Object-Falle, Regel 18.08.).
4. runner.log / results/*.json nie komplett einlesen (Token-Disziplin).
Nebenbei: Marker setzen, wenn --push-next / funded_finalize gelaufen sind.
"""
from _common import *  # noqa


def main():
    inp = read_input()
    cmd = (inp.get("tool_input") or {}).get("command") or ""
    c = cmd.replace("\\", "/")

    # --- Marker aus dem Kommando ableiten (vor allen Blocks) -----------------
    if re.search(r"inbox_tool\.py.*--push-next", c):
        touch_marker("push_next_at")
    if re.search(r"(funded_finalize|live_finalize)\.py", c):
        touch_marker("finalize_at")

    # --- 1. Box-Sync ohne Regressionstest -----------------------------------
    if re.search(r"box_provision_discovery\.ps1.*-Sync", c, re.I):
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

    # --- 2. Enqueue ohne pipeline-auditor -----------------------------------
    if re.search(r"hypothesis_bank\.py.*--enqueue", c):
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
    long_runner = any_re([
        r"start-process",
        r"start_discovery\.ps1",
        r"python[^\n|;&]*\b(app_server|lab_app|hub_app|discovery_runner)\.py",
        r"\bHub\.exe",
        r"\bnohup\b",
    ], c)
    escaped = any_re([r"invoke-cimmethod", r"job_escape", r"^\s*ssh\s", r"hot_reload\.ps1",
                      r"build_exe\.ps1", r"box_provision_discovery\.ps1", r"box_deploy\.ps1",
                      r"claude_unlock", r"--help", r"-Stop\b"], c)
    if long_runner and not escaped:
        deny(
            "STOP (Hook): Das sieht nach einem Dauerlaeufer aus, der als Kind der Claude-Session "
            "starten wuerde (Hub, Lab-Server, Discovery-Runner). Regel 18.08.2026: der Prozess "
            "erbt das Claude-Job-Object und blockiert danach Claude Desktop (0x80070020). Richtig: "
            "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments "
            "@{ CommandLine = '\"<exe>\" <args>'; CurrentDirectory = '<ordner>' } "
            "bzw. aus Python job_escape.spawn([...]). Kurzlaeufer (Backtest, Build) sind ok."
        )

    # --- 4. Volle Logs / Results einlesen -----------------------------------
    reads_full = any_re([
        r"(cat|type|get-content|gc)\s+[^\n|;&]*runner\.log(?![^\n|;&]*(-tail|-head|-totalcount|\|\s*(tail|head|grep|select-string)))",
        r"(cat|type|get-content|gc)\s+[^\n|;&]*results/[^\s]*\.json",
        r"(cat|type|get-content|gc)\s+[^\n|;&]*\.claude/projects/[^\s]*\.jsonl",
    ], c)
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
    if re.search(r"box_provision_discovery\.ps1.*-Sync", c, re.I):
        notes.append("Hook: nach dem Sync den Runner neu starten (Stop, Sync, Start), sonst laeuft "
                     "er mit altem Code weiter (Vorfall 28.08.2026, 5,5 h Leerlauf).")
    context("\n".join(notes), "PreToolUse")


run(main)
