"""PostToolUse(Edit|Write|Bash): Folgepflichten ansagen, die bisher nur im Kopf lagen.

Erkennt anhand des bearbeiteten Pfads bzw. des Bash-Kommandos, welche Regel
jetzt greift, und gibt Claude den Hinweis als Kontext zurueck. Dateizustaende
(book_state neuer als letzter push-next) werden nur EINMAL pro Aenderung gemeldet.
"""
from _common import *  # noqa


def main():
    inp = read_input()
    tool = inp.get("tool_name") or ""
    ti = inp.get("tool_input") or {}
    path = norm(ti.get("file_path"))
    cmd = norm(ti.get("command"))
    # Bei Bash zaehlt ein Dateiname nur, wenn das Kommando auch schreibt (sonst feuert
    # der Hook schon bei `ls sigcore.py` oder einem grep).
    writes = tool != "Bash" or bool(re.search(
        r"(>|\bsed\s+-i|\bcp\b|\bcopy\b|\bmv\b|\btee\b|robocopy|set-content|out-file|"
        r"git\s+(pull|checkout|merge|stash|reset)|--push-next|\bscp\b)", cmd))
    touched = (path or cmd) if writes else ""
    notes = []

    # Buch-Dateien: funded_finalize + push-next im selben Zug (Vorfall 21.08.2026)
    stale = book_newer_than_marker("push_next_at")
    if stale:
        last = marker_time("book_reported")
        newest = max(mtime(ENGINE / r) or 0 for r in stale)
        if last is None or newest > last + 1:
            touch_marker("book_reported", newest)
            notes.append(
                f"Hook: {', '.join(stale)} ist neuer als der letzte `inbox_tool.py --push-next`. "
                "Regel 10.08./21.08.2026: im selben Zug `python funded_finalize.py` (bei _next: --next, "
                "plus live_finalize) und `python discovery/inbox_tool.py --push-next`, sonst rechnet "
                "die Box gegen ein altes Buch. Der Stop-Hook laesst die Session sonst nicht enden."
            )
    elif re.search(r"book_state(_next)?\.json", touched) and not ENGINE:
        notes.append("Hook: book_state*.json angefasst (Engine hier nicht lokal, vermutlich Box per SSH). "
                     "Denk an funded_finalize (+--next) und `inbox_tool.py --push-next`.")

    # Engine-Kern: Regressionstest vor Sync; Discovery-Code: Runner-Neustart
    if any_re([r"/(sigcore|controls|overfit|qbt|tsmom|maband)\.py\b", r"/discovery/hypothesis_bank\.py\b"], touched):
        notes.append("Hook: Engine-Kern geaendert. Vor dem naechsten `box_provision_discovery.ps1 -SyncOnly` "
                     "laeuft `engine-regression-tester` (der Sync-Hook blockt sonst). Danach Runner neu starten.")
    elif re.search(r"/discovery/[a-z_]+\.py\b", touched) or re.search(r"/(job_generator|vix_bias)\.py\b", touched):
        notes.append("Hook: Discovery-Code geaendert. Der laufende Runner laedt das nicht nach: "
                     "Stop, Sync, Start (Vorfall 28.08.2026).")

    # Hypothesen-Bank: variant-scout + strategy-auditor Batch davor, pipeline-auditor vor --enqueue
    if re.search(r"hypothesen-bank", touched) or re.search(r"/discovery/hypothesis_bank\.py\b", touched):
        notes.append("Hook: Hypothesen-Bank angefasst. 'Der EINE Weg': variant-scout + strategy-auditor "
                     "(Batch) VOR dem Eintrag (Workflow `ein-weg`), pipeline-auditor vor `--enqueue` "
                     "(der Enqueue-Hook blockt sonst).")

    # Oberflaechen: design-guard
    if any_re([r"/hub/static/", r"hub_config\.json", r"/hub/[^/]+\.(html|js|css)$",
               r"/engine/(app_server|report)\.py\b", r"/engine/[^/]+\.(html|js|css)$"], touched) and tool != "Bash":
        notes.append("Hook: Oberflaeche geaendert (Hub/Lab/Report). Regel 30.08.2026: `design-guard` "
                     "einschalten, danach hot_reload.ps1 bzw. Lab-Server-Neustart.")

    # Neuer Agent / neue Automatik: Hub-Roster + CLAUDE.md
    if re.search(r"/\.claude/agents/[^/]+\.md$", path) and tool == "Write":
        notes.append("Hook: neuer Agent. Regel 27.08.2026: in hub_config.json (mock_agents) + "
                     "CLAUDE.md-Roster eintragen, dann hot_reload.ps1.")
    if re.search(r"/\.claude/(workflows|hooks)/", path) and tool == "Write":
        notes.append("Hook: neue Automatik. Regel 27.08.2026: in hub_config.json (mock_loops) eintragen.")

    # Logbuch: logbook-distiller
    if re.search(r"strategie-logbuch\.md$", path):
        notes.append("Hook: Strategie-Logbuch geaendert. Neue Lehre? Dann `logbook-distiller`: "
                     "ist sie als Gate codiert oder bleibt sie Text?")

    # Neue NinjaScript-Klasse: NS_MAP
    if re.search(r"/strategies/[^/]+\.cs$", touched) and tool == "Write":
        notes.append("Hook: neue NinjaScript-Klasse. Regel 01.09.2026: NS_MAP in gen_edge_ref.py ergaenzen, "
                     "sonst sieht der Edge-Health-Monitor das Bein nicht.")

    context("\n".join(notes), "PostToolUse")


run(main)
