"""Wissens-Router: Stichwort im Prompt -> passende Notiz/Skill (Plan Max, 05.10.2026).

Ziel: die CLAUDE.md schlank machen, ohne dass eine Session etwas nicht mehr weiss.
Was nur bei einem Thema gebraucht wird, steht in der Heimat-Notiz; dieser Router
erkennt das Thema in Max' Prompt und legt Kernzeilen + "lies X" hin. Volle Doku:
Projekte/CLAUDE.md Verschlankung.md.

Gebaut fuer Max' echte Sprache (Auswertung von 945 Prompts, 30 Tage):
- diktiert, voller Fuellwoerter -> Fuellwoerter stoeren nicht, Muster sind locker
- "Cloud" heisst fast immer Claude -> nie GitHub, sondern Thema claude
- "hab" heisst "habe" -> nie Hub
- "Juni-Modus" als Verhoerer fuer Juli-Modus
- Einstieg oft ueber Ticketnummern ("AP 72", "AP73") -> Tickettitel wird mitgeroutet
- kurze Folge-Prompts ("ja", "mach weiter") treffen nichts, das ist ok: je Thema
  feuert der Router nur beim ERSTEN Auftauchen in einer Session.

MODE: "schatten" = nur loggen, nichts einblenden (CLAUDE.md ist noch voll geladen).
      "live"     = Kernzeilen einblenden. Umschalten erst nach der Abnahme (Max).
Log: <STATE>/router_log.jsonl, Auswertung: python .claude/scripts/router_report.py
Tests: python .claude/scripts/test_router.py (muss gruen sein vor jeder Aenderung hier).
"""
import json
import re
import time
from pathlib import Path

try:
    from _common import STATE, ENGINE
except Exception:  # Tests / Import ausserhalb der Hooks
    STATE, ENGINE = Path("."), None

MODE = "schatten"

# Thema -> (Muster auf normalisiertem Text, Ausschluss-Muster, Kernzeilen, Heimat)
# Muster laufen auf norm(): klein, Umlaute ausgeschrieben, - _ / . als Leerzeichen.
TOPICS = [
    ("juli",
     [r"\b(juli|july|juni)\s?modus", r"\bjulimodus", r"testphase\s+juli", r"frueher mehr gefunden",
      r"gespraech vom 22\s?09", r"\b22\s?09\b.{0,40}(vorschlag|gespraech)"],
     [],
     ["Juli-Modus = Projekte/Testphase Juli-Modus.md, sofort dort weitermachen, keine Rueckfrage."],
     "Projekte/Testphase Juli-Modus.md"),
    ("developer",
     [r"\bdevelop\w*", r"\bworkbench\b", r"\bwork bench\b", r"\blab ui\b", r"\bstrategy lab\b", r"\blab selftest\b"],
     [],
     ["\"Developer\" bei einer Strategie-Idee = Developer-Workflow ohne Rueckfrage, nach JEDER Aenderung developer_run.py.",
      "mode=\"orb\" braucht orb_exec=\"close\" oder \"stop_honest\" (Look-ahead #066/#067). Lab-UI liegt in engine/lab_ui/, danach lab_selftest.py; Tests mit Trades per workbench.publish."],
     "Bereiche/Strategy Developer.md"),
    ("hub",
     [r"\bhub\b", r"\bhubs\b", r"\bhub exe\b", r"\bhub config\b", r"\bhot reload\b", r"\bcockpit\b"],
     [],
     ["\"Baue im Hub\" = Projekt C:\\Users\\maxlk\\Projects\\hub, ohne Rueckfrage, nur exakt das Angesagte aendern.",
      "Hub.exe nie fuer Kleinkram neu starten: static/ oder hub_config.json -> hot_reload.ps1; build_exe.ps1 nur bei hub_app.py/hub_server.py. Neuer Agent/Automatik -> hub_config.json."],
     "C:/Users/maxlk/Projects/hub/README.md"),
    ("gate",
     [r"\bgate\b", r"\bgate\s?v\s?\d", r"\bwochenend\w*", r"\bnext\s?week\w*", r"\bweekend check\b",
      r"\bstufe 2\b", r"\buebernehm\w*.{0,30}\b(buch|bein\w*)", r"\bins buch\b"],
     [],
     ["Gate v4: Stufe 1 Discovery-Gate (Box, automatisch) -> nur Next-Week-Buch; Stufe 2 Wochenend-Pruefung (/wochenende) -> echtes Buch, Max entscheidet.",
      "Stufe 2 mit RiskGuard-Stopp je Konto (E8 50k 900 $, FN 600 $, E8 150k 1.500 $ bei k1), Nulldrift-Zwilling, Auslage p90."],
     "Projekte/Latte-Audit (25.09.2026).md"),
    ("discovery",
     [r"\bdiscover\w*", r"\bqueue\b", r"\brunner\b", r"\binbox tool\b", r"\bkandidat\w*", r"\bpromote next\b",
      r"\bjob generator\b", r"\balpha suche\b", r"\bqueue empty\b"],
     [],
     ["Discovery: neue Suchidee = Job in der Queue (inbox_tool.py --add-job), Funde selbst einreihen nach Dry-Run + pipeline-auditor.",
      "Nach Engine-/job_generator-Aenderung Runner neu starten (NSSM MaxLabDiscovery, start_runner.ps1, nie WMI daneben). Nie runner.log oder volle results lesen."],
     "Bereiche/Discovery-Runner v2.md"),
    ("riskguard",
     [r"\brisk\s?guard\w*", r"\briskgard\b", r"\btelegram\b", r"\btages\s?stopp\w*", r"\bkontowechsel\b",
      r"\bwatchdog\b", r"\bstrategie instanz\b"],
     [],
     ["RiskGuard neu/entfernt/neue Instanz/Box-Reboot/Kontowechsel -> TelegramToken + TelegramChatId erinnern, Werte per SSH aus maxlab_watchdog.json holen (Skill riskguard)."],
     ".claude/skills/riskguard/SKILL.md"),
    ("konto",
     [r"\b(neue[snrm]?|weitere[snrm]?|zweite[snrm]?|naechste[snrm]?)\s+(konto|account|eval|challenge)",
      r"\b(gekauft|kaufen|kaufe|kauf|holen)\b.{0,40}\b(konto|account|eval|challenge|e8|ffn|fn|fundednext|150\s?k|50\s?k|100\s?k)\b",
      r"\b(konto|account|eval|challenge|e8|ffn|fn|fundednext|150\s?k|50\s?k|100\s?k)\b.{0,40}\b(gekauft|kaufen|kaufe)\b",
      r"\b(e8|ffn|fn|fundednext|funded next)\s?(150|100|50)\s?k\b", r"\bneue firma\b",
      r"\b(150|100|50)\s?k\b.{0,20}\b(account|konto|eval|challenge)",
      r"\b(account|konto)\s+(von|bei)\s+(ffn|e8|fn|fundednext)\b", r"\bprop\s?firm\w*",
      r"\bfunded wechsel\b", r"\bfirm regeln\b", r"\bconsistency\b"],
     [],
     ["Neues Konto/Firma/Phase -> vor dem ersten Trade Regeln aus der Primaerquelle, gegen RiskGuard-cfg/k/Kaefig abgleichen, in Firm-Regeln je Konto eintragen (Skill neues-konto)."],
     ".claude/skills/neues-konto/SKILL.md"),
    ("github",
     [r"\bgit\s?hub\b", r"\bgit\b", r"\brepos?\b", r"\bremote\b", r"\blaptop\b", r"\bpushen\b", r"\bgepusht\b",
      r"\bgit pull\b", r"\bclone\b", r"\bregistry backup\b", r"\bdeploy key\b"],
     [],
     ["GitHub-Account FederGorgon9818 (Vault master, hub master, trading-data main), alter Account mkmeboss als Remote alt. trading-data ist nur Backup-Repo."],
     "Ressourcen/GitHub & Repos.md"),
    ("mail",
     [r"\be?\s?mails?\b", r"\bpostfach\b", r"\bweb de\b", r"\bwebde\b", r"\brechnung\w*", r"\bbeleg\w*",
      r"\binbox\b(?!.{0,10}(tool|discovery))"],
     [],
     ["web.de: lesen ok, SENDEN nur nach Max' ausdruecklichem OK (auch per CLI webde_mail.py send). Kauf erwaehnt -> Rechnung direkt anfordern und in Belegordner 2026 einsortieren."],
     "Ressourcen/web.de-Postfach.md"),
    ("sprint",
     [r"\bsprints?\b", r"\bbacklog\b", r"\bplanning\b", r"\bboard\b"],
     [],
     ["Sprints plant Max selbst. Neue Tickets immer ins Backlog, nie selbst in einen Sprint, kein Planning vorschlagen, /sprint nur auf Zuruf."],
     "Projekte/Ticket-Board (Jira-Stil).md"),
    ("tot",
     [r"\btot\b", r"\btote[nr]?\b", r"\bfriedhof\w*", r"\btodesurteil\w*", r"\bbeerdig\w*", r"\burteil\w*", r"\bbegraben\b"],
     [],
     ["Todesurteil braucht Reichweite, Kategorie, Wiedervorlage, Stempel; strukturell-tot nur mit zitierter Rechnung."],
     "Ressourcen/Todesurteil-Regel.md"),
    ("box",
     [r"\bbox\b", r"\bvps\b", r"\bssh\b", r"\bnt8\b", r"\bninja\w*", r"\bdeploy\w*", r"\bvmd202078\b",
      r"\b100 127 89 9\b", r"\bserver\b", r"\brdp\b"],
     [],
     ["Box: ssh Administrator@100.127.89.9 selbst nutzen, nie behaupten, kein Zugriff. Deploy nur ueber box_deploy.ps1 (vorher NT8-Log + _check_compile.ps1), danach Max Bescheid geben (RDP, AP86)."],
     "Ressourcen/VPS-Einrichtung Schritt für Schritt.md"),
    ("buch",
     [r"\bbuch\b", r"\bbuchs\b", r"\bportfolio\w*", r"\bbook state\w*", r"\bbein(e|en|s)?\b", r"\bfunded finalize\b",
      r"\bpush next\b", r"\bsizing\b", r"\bk[1-4]\b", r"\bbetriebspunkt\b"],
     [],
     ["Buch: book_state.json ist die Quelle; jede Aenderung -> funded_finalize.py -> inbox_tool.py --push-next im selben Zug. Neues nie direkt live, immer erst Next-Week-Buch + Ticket."],
     "Bereiche/Buch-Workflow.md"),
    ("claude",
     [r"\bclaude\w*", r"\bcloud\b", r"\bcloud\s?(md|desktop|code)\b", r"\b(md|d)\s?(file|fall|datei)\b",
      r"\bhooks?\b", r"\bskills?\b", r"\bsubagent\w*", r"\bworkflows?\b", r"\btokens?\b", r"\bkontext\w*"],
     [],
     ["Prozess-Arbeit: Hooks-Referenz und Arbeits-Workflow (Auftrags-Typen) sind die Quellen; neue Reflex-Regel zuerst als Hook pruefen."],
     "Ressourcen/Hooks-Referenz.md"),
    ("gruendung",
     [r"\bgewerbe\w*", r"\bsteuer\w*", r"\bkleinunternehmer\w*", r"\beuer\b", r"\bbos\b", r"\bgehalt\w*",
      r"\bfreundin\b", r"\bgruend\w*", r"\bfinanzamt\b", r"\bselbststaendig\w*"],
     [],
     ["Gewerbe/Steuer: Unternehmensgruendung Entscheidung + Gruendung Zeitplan. Ab 04.07.2027 kein Gehalt, bei Kaeufen BOS-Reserve mitdenken."],
     "Projekte/Unternehmensgründung Entscheidung.md"),
    ("ziel",
     [r"\bmentorship\b", r"\bsocial media\b", r"\bwissensprodukt\b", r"\bvermoegen\b", r"\bimmobilie\w*",
      r"\btrack record\b", r"\breich werden\b", r"\bgrosses ziel\b", r"\bquant\b(?! team)", r"\bwerdegang\b"],
     [],
     ["Grosses Ziel: erst Live-Beweis, dann Kapital, dann Produkt; nie vor dem Beleg verkaufen; verkaufbar ist der Prozess, nie die Edge."],
     "Kontext/Großes Ziel.md"),
    ("werkzeug",
     [r"\bpyright\b", r"\blsp\b", r"\bvenv\w*", r"\bpyfolio\b", r"\bpypbo\b", r"\boverfit\w*", r"\bnssm\b", r"\bplugins?\b"],
     [],
     ["Werkzeuge: pyright nach Python-Aenderung, overfit_crosscheck.py nach overfit.py, .venv-analysis nie ins System-Python."],
     "Ressourcen/Werkzeug-Einsatz.md"),
]

# Nachrichten, die nicht von Max getippt wurden (Subagent-Rueckmeldungen, System-
# Benachrichtigungen). Fund 05.10.2026: der Agent-Reflex feuerte darauf sechsmal.
NOT_MAX = [r"^\s*<agent-message", r"^\s*another claude session sent a message", r"^\s*<task-notification",
           r"^\s*\[system notification", r"^\s*<system-reminder"]

# Diktier-Verhoerer aus dem Korpus (05.10.2026), werden vor dem Matching ersetzt.
ALIASES = [
    (r"\b(i8|e 8|ee8|e acht)\b", "e8"),
    (r"\b(funnet|fundet|fanned|funded|founded)\s?next\b", "fundednext"),
    (r"\bstereo\s?lab\b|\bstrategie\s?lab\b", "strategy lab"),
    (r"\brisiko\s?guard\b", "riskguard"),
]

TICKET_RX = re.compile(r"\bap\s?-?\s?(\d{1,3})\b", re.I)


def norm(text):
    t = (text or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    t = re.sub(r"[-_/.,;:!?()\[\]\"'`]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    for rx, rep in ALIASES:
        t = re.sub(rx, rep, t)
    return t


def is_not_max(prompt):
    head = (prompt or "")[:400].lower()
    return any(re.search(p, head) for p in NOT_MAX)


def ticket_titles(prompt):
    """AP-Nummern im Prompt -> [(AP-ID, Titel)] aus engine/tasks.json."""
    ids = {f"AP{int(m.group(1))}" for m in TICKET_RX.finditer(prompt or "")}
    if not ids or not ENGINE:
        return [(i, "") for i in sorted(ids)]
    try:
        tasks = json.loads((ENGINE / "tasks.json").read_text(encoding="utf-8"))
        by = {str(t.get("ap_id")): str(t.get("title") or "") for t in tasks if isinstance(t, dict)}
        return [(i, by.get(i, "")) for i in sorted(ids)]
    except Exception:
        return [(i, "") for i in sorted(ids)]


def match(prompt):
    """Themen-IDs, die der Prompt trifft (inkl. Stichworte aus Tickettiteln)."""
    tickets = ticket_titles(prompt)
    text = norm(prompt + " " + " ".join(t for _, t in tickets))
    hits = []
    for tid, pats, excl, _lines, _home in TOPICS:
        if any(re.search(p, text) for p in pats) and not any(re.search(p, text) for p in excl):
            hits.append(tid)
    return hits, tickets


def _seen_path(sid):
    return STATE / "router" / f"{re.sub(r'[^A-Za-z0-9_-]', '', str(sid))[:40] or 'nosid'}.json"


def route(prompt, sid):
    """-> (neu_getroffene_themen, alle_treffer, tickets, kontext_text_oder_leer)."""
    if is_not_max(prompt):
        return [], [], [], ""
    hits, tickets = match(prompt)
    p = _seen_path(sid)
    try:
        seen = set(json.loads(p.read_text(encoding="utf-8")))
    except Exception:
        seen = set()
    fresh = [h for h in hits if h not in seen]
    if fresh:
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(sorted(seen | set(fresh))), encoding="utf-8")
        except Exception:
            pass
    _log(sid, prompt, hits, fresh, tickets)
    if MODE != "live" or not (fresh or tickets):
        return fresh, hits, tickets, ""
    lines = ["Hook (Wissens-Router): Themen erkannt, Kernregeln dazu:"]
    by = {t[0]: t for t in TOPICS}
    for tid in fresh:
        _, _, _, kl, home = by[tid]
        lines += [f"- {k}" for k in kl] + [f"  Details: {home}"]
    for ap, title in tickets:
        if title:
            lines.append(f"- Ticket {ap}: {title[:120]} (Details: /ticket {ap})")
    return fresh, hits, tickets, "\n".join(lines)


def _log(sid, prompt, hits, fresh, tickets):
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        rec = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "sid": str(sid)[:8], "mode": MODE,
               "hits": hits, "fresh": fresh, "tickets": [a for a, _ in tickets],
               "len": len(prompt or ""), "prompt": (prompt or "")[:300]}
        with open(STATE / "router_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass
