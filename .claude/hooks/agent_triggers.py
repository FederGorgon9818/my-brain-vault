"""Einschalt-Regeln der Subagents als Daten (Max' Vault, 11.09.2026).

EINE Quelle fuer zwei Verbraucher:
  - on_prompt.py (UserPromptSubmit): erinnert beim Tippen, welcher Agent laut CLAUDE.md
    dran waere, sobald ein Trigger im Prompt steht.
  - on_stop.py (Stop): meldet am Session-Ende, wenn ein Trigger in der Session gefeuert
    hat, der Agent aber nie aufgerufen wurde.
  - .claude/scripts/agent_usage_audit.py: Rueckblick ueber die Transkripte, wo Agents
    ausgelassen wurden (Retro-Futter).

Jede Regel: id, agent(s), wo gesucht wird (user = Prompt-Text, assistant = Antwort-Text,
bash = Bash-Kommandos, file = geaenderte Dateipfade), Regex, Kurzgrund. Die Regeln sind
bewusst grob (Heuristik, nie Sperre): lieber eine Erinnerung zu viel als ein vergessener
Agent. Die verbindliche Formulierung steht in der CLAUDE.md, hier nur der Reflex.
"""
import re

# (id, agents, scopes, pattern, warum)
TRIGGERS = [
    ("konzept", ["familien-scout"], ("user",),
     r"\b(vwap|fibonacci|fib-?level|volumenprofil|volume profile|opening range|gap-?(fill|fade|strateg)|"
     r"konzept|wie (k[oö]nnte|kann|w[uü]rde) man .{0,60}(handeln|traden)|edge (bei|aus|mit|in) )\b",
     "Konzept/grobe Edge genannt: familien-scout zerlegt in Preis-Wege, BEVOR eine Hypothese gebaut wird (Regel 11.09.2026)"),
    ("hypothese", ["variant-scout", "strategy-auditor"], ("user", "file"),
     r"(\b(neue hypothese|hypothese[n]? (bauen|anlegen|eintragen|formulieren)|in die (hypothesen-?)?bank)\b|Hypothesen-Bank \([^)]*\)\.md$)",
     "Neue Hypothese: variant-scout vermisst die Arten, dann strategy-auditor Batch, BEVOR sie in Bank/H() geht (Regel 01.09.2026)"),
    ("alpha", ["quant-mathematician", "quant-statistician"], ("user",),
     r"\b(backtest-?ergebnis|discovery-?(batch|lauf|auswert)|kandidat(en)? (aus|in) der (inbox|queue)|buch-?beitrag|ins buch|"
     r"developer-?version|passquote|sizing|frac-?(paar|wahl)|k[aä]fig-?(vergleich|wahl)|parameter-?wahl|edge (real|echt|gr[oö][sß]e)|"
     r"auswerten|ergebnis(se)? (an(schauen|sehen)|bewerten|pr[uü]fen))\b",
     "Neues Alpha / Eval-Optimierung: Quant-Team (Mathematiker + Statistiker) parallel im Background (Regel 16.08.2026)"),
    ("urteil", ["verdict-auditor"], ("assistant",),
     r"\b(urteil:?\**\s*(tot|gut|neutral|besser|schlechter|fertig)|ist (damit )?tot\b|f[uü]r tot erkl|tot als buch-?bein|"
     r"(strategie|hypothese|variante|bein|modul|skript|gate|vorlage|workflow|agent) (ist|gilt als) fertig|fertig gebaut)\b",
     "Ein Stempel (tot/gut/fertig) steht an: verdict-auditor prueft, ob die Beweislage ihn traegt (Regel 30.08.2026)"),
    ("deploy", ["strategy-auditor"], ("user",),
     r"\b(nt8-?deploy|box_deploy|auf die eval|ins live-?buch|book_state\.json .{0,30}(übernehmen|uebernehmen)|next-?week.{0,20}(übernehmen|uebernehmen))\b",
     "Vor Eval-Deploy/Buch-Uebernahme: strategy-auditor Vollmodus als Gegenleser"),
    ("enqueue", ["pipeline-auditor"], ("bash", "user"),
     r"(--enqueue\b|--add-job\b|\b(neuen?|den) (hypothesen-?)?job (bauen|einreihen|in die queue)|in die queue (legen|packen|stellen|tun))",
     "Job geht auf die Box: pipeline-auditor prueft die Pipeline (setzt pipeline_ok, Regel 25.08.2026)"),
    ("engine_core", ["engine-regression-tester"], ("file", "bash"),
     r"(/(sigcore|controls|hypothesis_bank|overfit|qbt|tsmom|maband)\.py$|-SyncOnly|box_provision_discovery\.ps1 -Sync)",
     "Engine-Kern geaendert oder Box-Sync: engine-regression-tester vor dem Sync (Regel 27.08.2026)"),
    ("ui", ["design-guard"], ("file",),
     r"(/hub/.*\.(js|css|html|json)$|/engine/(app_server|lab_app|report)\.py$|/hub/hub_app\.py$|/static/.*\.(js|css|html)$)",
     "Oberflaeche geaendert (Hub/Lab/Report): design-guard prueft gegen die Charta (Regel 30.08.2026)"),
    ("logbuch", ["logbook-distiller"], ("file",),
     r"Strategie-Logbuch\.md$",
     "Neue Lehre im Logbuch: logbook-distiller fragt, ob sie als Gate codiert ist (Regel 27.08.2026)"),
    ("shared_files", ["session-guard"], ("file",),
     r"/engine/((app_server|developer_run|report)\.py|book_state\.json|portfolio\.json|developer/state\.json)$",
     "Sammel-Datei angefasst: session-guard prueft parallele Sessions (Regel 16.08.2026)"),
    ("research", ["research-scout"], ("user",),
     r"\b(paper|ssrn|arxiv|studie[n]?|literatur|recherchier|websuche|was sagt die forschung|such mal im (netz|web|internet))\b",
     "Externe Recherche: research-scout mit Cache-Pflicht statt direkter Websuche"),
    ("queue_empty", ["alpha-scout"], ("user", "assistant"),
     r"\b(queue_empty|queue (ist|l[aä]uft) leer|was testen wir als n[aä]chstes|neue ideen|n[aä]chste mechanismen)\b",
     "Queue leer / naechste Ideen: alpha-scout macht Inventar + gerankte Jobs (Regel 21.08.2026)"),
    ("box", ["box-ops"], ("user",),
     r"\b(l[aä]uft alles|check die box|box-?status|runner (steht|h[aä]ngt|l[aä]uft)|heartbeat)\b",
     "Box-Frage: box-ops macht den Rundgang"),
    ("live", ["live-reconciler"], ("user",),
     r"\b(passt das konto|kontostand|live vs\.? backtest|fills? (heute|gestern)|wie lief der tag live)\b",
     "Live-Abgleich: live-reconciler vergleicht NT8-Fills mit dem Backtest"),
    ("ninja", ["ninja-coder"], ("file", "user"),
     r"(\.cs$|\b(ninjascript (schreiben|anpassen|bauen|fixen)|nt8-?strategie (bauen|anpassen)|compile-?fehler)\b)",
     "NinjaScript-Arbeit: ninja-coder"),
]

# Direkte Tool-Nutzung, die einen Agent umgeht (fuer Audit + Stop-Erinnerung).
DIRECT_TOOL_BYPASS = {
    "WebSearch": ("research", ["research-scout"], "Websuche direkt statt ueber research-scout (Cache-Pflicht)"),
    "WebFetch": ("research", ["research-scout"], "WebFetch direkt statt ueber research-scout (Cache-Pflicht)"),
}

_COMPILED = [(tid, agents, scopes, re.compile(pat, re.I | re.S), why) for tid, agents, scopes, pat, why in TRIGGERS]


def match(scope, text):
    """Liefert [(id, agents, why, snippet)] fuer alle Regeln, die in diesem Scope auf den Text passen."""
    hits = []
    if not text:
        return hits
    for tid, agents, scopes, rx, why in _COMPILED:
        if scope not in scopes:
            continue
        m = rx.search(text)
        if m:
            s = max(0, m.start() - 30)
            snippet = re.sub(r"\s+", " ", text[s:m.end() + 30]).strip()
            hits.append((tid, agents, why, snippet))
    return hits


def agents_for(tid):
    for t, agents, _, _, _ in TRIGGERS:
        if t == tid:
            return agents
    return []
