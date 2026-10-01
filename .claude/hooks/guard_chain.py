"""PreToolUse: die Pflichtkette des Auftrags-Typs durchsetzen (Regel Max, 21.09.2026).

Max' Entscheidung: "blocken, Override moeglich". Dieser Hook ist die harte Haelfte
des Typ-Routers aus work_types.py. Er greift auf ZWEI Wegen, weil beide Wege je
eine Luecke des anderen schliessen:

A) AKTIONS-GATE -- unabhaengig von der Quittung
   Manche Aktionen verraten ihren Typ selbst: ein Write auf eine Hub-Datei IST
   UI-Arbeit, ein neuer Logbuch-Eintrag IST eine Lehre, ein WebSearch IST externe
   Recherche. Fuer die gilt die Kette auch dann, wenn niemand einen Typ gesetzt hat.
   Das sind genau die drei schlechtesten Quoten im Audit vom 21.09.2026:
       logbook-distiller 3/30, design-guard 8/22, research-scout 30/25.

B) QUITTUNGS-GATE -- wenn ein Typ gesetzt ist
   Typen wie `urteil`, `buch` oder `rechnen` erkennt man NICHT am Tool: ein Urteil
   ist ein Sprechakt, der am Ende irgendwo als Text landet. Sobald die Quittung
   (receipt.py) so einen Typ traegt und die Kette noch offen ist, sind schreibende
   Aktionen gesperrt, bis die Kette lief. Das ist der Punkt, an dem aus "ich haette
   den Agent nehmen sollen" ein "ich komme ohne ihn nicht weiter" wird.

Freiliste fuer B: was zum Protokollieren und zum Bedienen des Prozesses selbst
gehoert (Daily Note, .claude/**, Ticket-Tracker, Scratchpad). Sonst koennte der
Hook verhindern, dass man ihn ueberhaupt bedient oder die Session sauber abschliesst.

Override (Max' Entscheidung, mit Begruendungspflicht):
    python .claude/hooks/receipt.py --sid <id> --skip <schritt> --why "<ein Satz>"
Der Grund steht danach in der Quittung und taucht im Retro auf. Eine Ausnahme
ohne Grund gibt es nicht -- genau das hat die alte Text-Erinnerung nicht geschafft.
"""
from _common import *  # noqa

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

import receipt as R  # noqa: E402
import work_types as WT  # noqa: E402

# --- A) Aktionen, die ihren Typ selbst verraten ----------------------------
UI_FILE = [r"/hub/.*\.(js|css|html)$", r"/hub/static/",
           r"/engine/[^/]+\.(html|js|css)$", r"/static/.*\.(js|css|html)$"]
# app_server.py / lab_app.py / report.py sind Backend UND Oberflaeche in einer Datei.
# Sie pauschal als UI zu werten haette im Nachspiel ueber 14 Tage 19 von 30 UI-Blockaden
# allein wegen reiner Backend-Edits erzeugt (Messung verdict-auditor, 21.09.2026) --
# ein Gate, das oefter falsch als richtig blockt, macht den Override zum Normalweg und
# entwertet sich selbst. Deshalb nur UI, wenn der Diff wirklich Oberflaeche anfasst.
MIXED_FILE = r"/engine/(app_server|lab_app|report)\.py$"
_MARKUP = re.compile(
    r"(<(div|span|table|tr|td|th|button|input|form|style|script|h[1-6]|ul|li)\b"
    r"|</(div|span|table|button|form|style|script)>"
    r"|style\s*=\s*[\"']|class\s*=\s*[\"']|innerhtml|render_template|<!doctype"
    r"|background(-color)?:|font-(size|family|weight):)", re.I)
UI_CMD = [r"hot_reload\.ps1", r"build_exe\.ps1"]
# hub_config.json ist Oberflaeche UND Datenhaltung in einer Datei. Ein Eintrag im
# Agent-/Automatik-Roster (mock_agents/mock_loops/mock_tokens) aendert nichts am
# Aussehen -- den design-guard dafuer zu verlangen, waere ein Fehlalarm, der bei
# jeder Pflege des Rosters auftritt (gefunden im Eigentest beim Bau, 21.09.2026).
# Die Layout-/App-Schluessel derselben Datei bleiben dagegen UI-Arbeit.
_ROSTER_ONLY = re.compile(r"mock_(agents|loops|tokens)", re.I)
_UI_KEYS = re.compile(r"\"(apps|port|layout|theme|windows|panels)\"", re.I)


def _is_ui_config(tool, ti, path):
    if not re.search(r"hub_config\.json$", path or ""):
        return False
    if tool == "Write":
        return True  # komplette Neuanlage: im Zweifel UI
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    for e in edits or []:
        blob = (e.get("old_string") or "") + (e.get("new_string") or "")
        if _UI_KEYS.search(blob) or not _ROSTER_ONLY.search(blob):
            return True
    return False
LOGBOOK_FILE = r"strategie-logbuch\.md$"
BOOK_FILE = r"book_state(_next)?\.json$"

# Subagents, die SELBST ins Web duerfen (Gate 1 greift fuer sie nicht). research-scout
# und alpha-scout tragen die Cache-Pflicht in ihrer eigenen Definition (Research-Cache
# zuerst, neue Claims zurueckschreiben) -- das Gate schuetzt dort nichts, es blockt nur.
# claude-code-guide recherchiert Claude-Code-Doku, nichts fuer den Research-Cache.
# Entscheidung Max 26.09.2026 (bestaetigt 28.09.), Anlass: research-scout in den Ad-hoc-
# Workflows eval-vs-funded (25.09.) und bulenox-check (26.09.) sowie alpha-scout (21.09.)
# bekamen JEDEN WebSearch/WebFetch geblockt und lieferten nur Cache-Wissen.
WEB_AGENTS = {"research-scout", "alpha-scout", "claude-code-guide"}
# Ihr Rueckschreib-Ziel. Das Quittungs-Gate (B) hat den research-scout am 23.09.2026
# (Session d954c57e, Typ `buch`, Kette offen) genau beim Eintrag in den Cache gesperrt --
# die Cache-Pflicht, fuer die Gate 1 existiert, war damit unerfuellbar.
CACHE_FILE = r"/ressourcen/research-cache\.md$"
_NEW_ENTRY = re.compile(r"^#{1,4}\s*#?\d{1,4}\b|^\|\s*#?\d{1,4}\s*\|", re.M)

# --- B) Freiliste: das darf auch bei offener Kette geschrieben werden ------
ALWAYS_FREE = [r"/daily notes/", r"/\.claude/", r"tasks\.json$", r"/scratchpad/",
               r"/temp/", r"/tmp/", r"\.claude_hooks/"]


def _free(path):
    return any_re(ALWAYS_FREE, path)


def _touches_markup(tool, ti):
    """Fasst dieser Edit an einer gemischten Backend/UI-Datei wirklich Oberflaeche an?"""
    if tool == "Write":
        return bool(_MARKUP.search(ti.get("content") or ""))
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    for e in edits or []:
        if _MARKUP.search((e.get("old_string") or "") + (e.get("new_string") or "")):
            return True
    return False


_PATHISH = re.compile(r"[\w./\\:-]+\.(?:json|md|py|js|css|html|cs|ps1|txt|csv)", re.I)
# Ein Pfad in Anfuehrungszeichen darf Leerzeichen haben ("My Brain", "ADX Wege-Karte.md").
_QUOTED = r"""(?:"([^"]+)"|'([^']+)'|([\w./\\:-]+\.\w+))"""


def _bash_write_targets(cmd):
    """Pfade, auf die ein Bash-Kommando SCHREIBEND zeigt.

    Notwendig, weil das Quittungs- und das book_state-Gate vorher nur Edit/Write/
    MultiEdit sahen: `>>`, `sed -i`, `Set-Content` oder `python -c "open(...,'w')"`
    gingen daran vorbei (Fund verdict-auditor, 21.09.2026) -- genau die Wege, die man
    nimmt, wenn einen ein Gate nervt.

    Bewusst nur ZIELE, nicht jeder Pfad im Kommando: `python calc.py > out.json`
    schreibt nach out.json, nicht nach calc.py. Jeden Pfad zu nehmen hiesse, jedes
    ausgefuehrte Skript als Schreibziel zu werten -- der erste Selbsttest ist genau
    darueber gestolpert.
    """
    if not cmd:
        return []
    t = []

    def _add(matches):
        for m in matches:
            v = next((x for x in (m if isinstance(m, tuple) else (m,)) if x), None)
            if v:
                t.append(v)

    # Umleitung: > / >>
    _add(re.findall(r">>?\s*" + _QUOTED, cmd))
    # tee / Set-Content / Out-File / Add-Content (auch mit -Path)
    _add(re.findall(r"(?:\btee\b|set-content|out-file|add-content)\s+(?:-path\s+)?" + _QUOTED, cmd, re.I))
    # sed -i: Ziel steht im selben Segment
    for m in re.finditer(r"sed\s+-i[^\n;|&]*", cmd, re.I):
        t += _PATHISH.findall(m.group(0))
    # cp/mv/copy/move: alles ab dem zweiten Pfad ist Ziel
    for m in re.finditer(r"\b(?:cp|mv|copy|move|robocopy)\b[^\n;|&]*", cmd, re.I):
        t += _PATHISH.findall(m.group(0))[1:]
    # Python: open(..., "w"/"a")
    _add(re.findall(r"open\(\s*[\"']([^\"']+)[\"']\s*,\s*[\"'][wa]", cmd))
    return t


# --- Urteils-Pflichtfelder (Regel Max, 22.09.2026) -------------------------
# Anlass: Max' Einwand, dass wir Dinge "tot" nennen, von denen wir nur einen
# winzigen Teil des Konstruktionsraums gemessen haben. Der verdict-auditor hat
# es nachgezaehlt: 82 Todesurteile im Logbuch, davon 46 ohne jede Bedingung UND
# ohne Reichweite. Klarster Fall #163 -- Titel "endgueltig tot", Koerper sagt
# "braeuchte 27-29 Jahre Historie", also unentscheidbar.
# Der Hook erzwingt, dass die Felder DA sind, nicht dass sie stimmen. Genau das
# haette gereicht: #163 haette `unentscheidbar` setzen muessen und konnte dann
# nicht mehr "endgueltig tot" im Titel tragen.
_VERDICT_BLOCK = re.compile(
    r"^[^\S\n]*[*_]{0,2}(?:Verdikt|Urteil|Fazit)[*_]{0,2}\s*:.*(?:\n(?![^\S\n]*#{1,4}\s).*)*",
    re.M | re.I)
_TOD = re.compile(r"\b(?:tot|erledigt|friedhof|verworfen|begraben|gestorben|"
                  r"endg[uü]ltig|kein\s+kandidat)\b", re.I)
_KATEGORIEN = ("strukturell-tot", "empirisch-nichts-gefunden",
               "echt-aber-zu-klein", "unentscheidbar")


def _urteil_felder_fehlen(text):
    """Fehlende Pflichtfelder, wenn ein URTEILSBLOCK ein Todesurteil traegt.

    Bewusst nur der Urteilsblock, nicht der Fliesstext: Eintraege wie #171 oder
    die Friedhof-Analyse reden staendig ueber fremde Todesurteile, ohne selbst
    eines zu faellen (Fehlalarm-Quelle 1 des verdict-auditor)."""
    bloecke = [m.group(0) for m in _VERDICT_BLOCK.finditer(text or "")]
    if not any(_TOD.search(b) for b in bloecke):
        return []
    low = (text or "").lower()
    fehlt = []
    if not any(k in low for k in _KATEGORIEN):
        fehlt.append("KATEGORIE: eine von " + " | ".join(_KATEGORIEN))
    if "reichweite:" not in low:
        fehlt.append("REICHWEITE: Rolle, Frequenz, Markt, Kaefig, Kostenstruktur "
                     "-- 'tot' ohne Objekt ist verboten")
    if "wiedervorlage:" not in low:
        fehlt.append("WIEDERVORLAGE: Datum oder pruefbare Bedingung "
                     "('nur auf Ansage' nur bei strukturell-tot)")
    if "stempel:" not in low:
        fehlt.append("STEMPEL: Engine-Fingerprint, Datenstand, Kriterium/Betriebspunkt")
    # Umlaute UND ASCII-Transliteration: der Vault schreibt ueberwiegend "ue"/"oe".
    _UE = r"(?:u|ü|ue)"
    if "strukturell-tot" in low and not re.search(
            rf"h{_UE}llkurve|kostenh{_UE}rde|kostenschwelle|algebra|verbietet die klasse", low):
        fehlt.append("BELEG fuer strukturell-tot: die Rechnung zitieren, die die ganze "
                     "Klasse verbietet (Huellkurve, Kostenhuerde, Algebra). Ohne sie ist "
                     "es empirisch-nichts-gefunden mit N")
    return fehlt


def _neuer_text(tool, ti):
    if tool == "Write":
        return ti.get("content") or ""
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    return "\n".join((e.get("new_string") or "") for e in (edits or []))


def _adds_new_entry(tool, ti):
    """Neuer Logbuch-Eintrag (nicht bloss Formatierung an bestehenden)."""
    if tool == "Write":
        return True
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    for e in edits or []:
        old_n = set(_NEW_ENTRY.findall(e.get("old_string") or ""))
        new_n = set(_NEW_ENTRY.findall(e.get("new_string") or ""))
        if new_n - old_n:
            return True
    return False


def _log_error(where, e):
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        with open(STATE / "hook_errors.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} guard_chain.{where}: {e!r}\n")
    except Exception:
        pass


def _used(transcript_path):
    """(Agents dieser Session, in dieser Session geaenderte Dateien).
    None = unbekannt -> nie blockieren."""
    try:
        sys.path.insert(0, str(VAULT / ".claude" / "scripts"))
        from agent_usage_audit import scan, used_agent_names
        s = scan(Path(transcript_path))
        return used_agent_names(s), {norm(p) for p in s.get("changed") or ()}
    except Exception as e:
        # NICHT still schlucken: ein Import-/Encoding-/Pfadfehler wuerde sonst das
        # komplette Gate abschalten, ohne dass es jemand merkt ("das Gate ist tot und
        # niemand weiss es" -- Fund verdict-auditor, 21.09.2026). Der Hook laesst die
        # Aktion weiterhin durch (er darf nie kaputt blockieren), sagt es aber laut.
        _log_error("_used", e)
        return "ERROR"


def _caller(inp, transcript_path):
    """Agent-Typ des Aufrufers, None = Hauptthread.

    Gemessen 26.09.2026 (Claude Code 2.1.281, Dump-Hook): in einem Subagent traegt die
    Hook-Eingabe `agent_id` + `agent_type`, `session_id` und `transcript_path` sind die
    der ELTERN-Session. Deshalb sah Gate 1 bisher nur das Haupt-Transkript und hielt den
    research-scout fuer "nicht gelaufen", waehrend er selbst anfragte. Workflow-Agents
    (agent(..., {agentType})) tragen dieselben Felder -- live gemessen 28.09.2026 mit
    Mini-Workflow (research-scout + Explore). Fehlt agent_type (aeltere Version), kommt
    der Typ aus der meta.json des Subagents."""
    typ = inp.get("agent_type")
    if typ or not inp.get("agent_id"):
        return typ or None
    try:
        sys.path.insert(0, str(VAULT / ".claude" / "scripts"))
        from agent_usage_audit import subagent_type
        return subagent_type(Path(transcript_path), inp["agent_id"]) if transcript_path else None
    except Exception as e:
        _log_error("_caller", e)
        return None


def _sid(inp):
    return R.sid8(inp.get("session_id"))


def _skipped(rec, name):
    return name in (rec.get("skipped") or {}) if rec else False


def _sub_hint(caller):
    # Ein Subagent kann den Override meist nicht selbst setzen (oft ohne Bash) und hat am
    # 25.09.2026 dann still nur Cache-Wissen geliefert. Er soll die Sperre zurueckmelden.
    return (f"\n\nDu laeufst als Subagent `{caller}`: den Override setzt der Hauptthread. "
            f"Melde zurueck, welche Aktion gesperrt war und wofuer du sie gebraucht haettest, "
            f"statt still ohne sie weiterzuarbeiten.") if caller else ""


def _deny_action(tid, agent, sid, detail, caller=None):
    deny(
        f"STOP (Hook, Kette `{tid}`): {detail} "
        f"`{agent}` ist in dieser Session noch nicht gelaufen. {WT.what_of(tid)} "
        f"\n\nEntweder jetzt `{agent}` einschalten und die Aktion wiederholen -- oder die "
        f"Ausnahme begruenden:\n"
        f"  python .claude/hooks/receipt.py --sid {sid} --skip {agent} --why \"<ein Satz>\""
        + _sub_hint(caller)
    )


def main():
    inp = read_input()
    tool = inp.get("tool_name") or ""
    ti = inp.get("tool_input") or {}
    path = norm(ti.get("file_path"))
    cmd = norm(ti.get("command"))
    sid = _sid(inp)
    tp = inp.get("transcript_path")
    rec = R.load(inp.get("session_id"))
    caller = _caller(inp, tp)

    # Gate 1 gilt nicht fuer den, der die Cache-Pflicht selbst traegt -- vor dem
    # Transkript-Scan, damit ihn auch ein Scan-Fehler nicht trifft.
    if tool in ("WebSearch", "WebFetch") and caller in WEB_AGENTS:
        sys.exit(0)

    scanned = _used(tp) if tp and Path(tp).is_file() else None
    if scanned == "ERROR":
        context("Hook-WARNUNG (guard_chain): der Transkript-Scan ist fehlgeschlagen, die "
                "Ketten-Gates sind in diesem Aufruf BLIND (Details in hook_errors.log). "
                "Die Aktion laeuft durch -- ein Hook darf nie kaputt blockieren -- aber "
                "die Pflichtkette ist hier gerade nicht durchgesetzt. Kurz pruefen: "
                "`python .claude/scripts/test_chain.py`.", "PreToolUse")
    if scanned is None:
        sys.exit(0)  # ohne Transkript kein Urteil -- Hook blockiert nie ins Blaue
    used, changed = scanned

    # ---------------- A) Aktions-Gates ------------------------------------
    # 1. Externe Recherche ohne research-scout (Cache-Pflicht)
    if tool in ("WebSearch", "WebFetch") and "research-scout" not in used and not _skipped(rec, "research-scout"):
        _deny_action("research", "research-scout", sid,
                     f"{tool} ist ein direkter Zugriff aufs Web, aber", caller)

    # 2. Oberflaeche ohne design-guard
    # Beim Neuladen (hot_reload/build_exe) nur blocken, wenn diese Session wirklich
    # eine Oberflaechen-Datei angefasst hat. Sonst traefe es auch das blosse Neuladen
    # nach fremder Aenderung -- und dort waere design-guard zu Recht nie gelaufen.
    # Faengt zugleich den Umgehungsweg ab, eine UI-Datei per Bash (sed) zu aendern,
    # weil das Datei-Gate darunter nur Edit/Write sieht.
    reload_after_ui = (tool == "Bash" and any_re(UI_CMD, cmd)
                       and any(any_re(UI_FILE, p) for p in changed))
    is_ui = (tool != "Bash" and path and (
        any_re(UI_FILE, path)
        or _is_ui_config(tool, ti, path)
        or (re.search(MIXED_FILE, path) and _touches_markup(tool, ti))
    )) or reload_after_ui
    if is_ui and "design-guard" not in used and not _skipped(rec, "design-guard"):
        was = "Oberflaechen-Datei geaendert" if tool != "Bash" else "Hub/Lab wird neu geladen"
        _deny_action("ui", "design-guard", sid, f"{was}, aber", caller)

    # 3. Neue Lehre im Logbuch ohne logbook-distiller (schlechteste Quote: 3 von 33)
    if tool != "Bash" and path and re.search(LOGBOOK_FILE, path) and _adds_new_entry(tool, ti) \
            and "logbook-distiller" not in used and not _skipped(rec, "logbook-distiller"):
        _deny_action("logbuch", "logbook-distiller", sid, "Neuer Logbuch-Eintrag, aber", caller)

    # 3b. Todesurteil ohne Pflichtfelder (Regel Max, 22.09.2026)
    if tool != "Bash" and path and re.search(LOGBOOK_FILE, path) and _adds_new_entry(tool, ti):
        try:
            ov = marker_time("urteil_ok")
        except Exception:
            ov = None
        if not ov:
            fehlt = _urteil_felder_fehlen(_neuer_text(tool, ti))
            if fehlt:
                deny(
                    "STOP (Hook): der Urteilsblock faellt ein Todesurteil, aber es fehlen "
                    "Pflichtangaben:\n  - " + "\n  - ".join(fehlt) +
                    "\n\nRegel vom 22.09.2026: ein Todesurteil ohne Reichweite, Kategorie, "
                    "Wiedervorlage und Stempel ist kein Urteil, sondern eine Notiz. Anlass war "
                    "der Befund, dass 46 von 82 Todesurteilen im Logbuch weder Bedingung noch "
                    "Reichweite tragen -- und dass #163 'endgueltig tot' im Titel fuehrt, "
                    "waehrend im Koerper steht, man braeuchte 27-29 Jahre Historie.\n\n"
                    "Faellt der Eintrag in Wahrheit gar kein Todesurteil (Rueckblick, Zitat, "
                    "Prozess-/Werkzeug-Eintrag):\n"
                    "  python .claude/hooks/mark.py urteil_ok"
                )

    # 4. Buch-Datei ohne Quant-Team + Gegenleser
    book_touched = (tool != "Bash" and path and re.search(BOOK_FILE, path)) or \
        (tool == "Bash" and any(re.search(BOOK_FILE, norm(x)) for x in _bash_write_targets(cmd)))
    if book_touched:
        for agent in ("quant-statistician", "strategy-auditor"):
            if agent not in used and not _skipped(rec, agent):
                _deny_action("buch", agent, sid,
                             "Das aendert direkt, was live gehandelt wird, aber", caller)

    # ---------------- B) Quittungs-Gate -----------------------------------
    # Typ gesetzt, Kette offen, Gate-Typ -> schreibende Aktionen gesperrt.
    if rec and rec.get("type") and WT.has_gate(rec["type"]):
        def free(p):
            return _free(p) or (caller in WEB_AGENTS and bool(re.search(CACHE_FILE, p or "")))

        # Bash zaehlt mit, aber nur wenn es wirklich ausserhalb der Freiliste schreibt --
        # sonst waere jede Rechnung ins Scratchpad blockiert.
        if tool == "Bash":
            gated = next((x for x in (norm(y) for y in _bash_write_targets(cmd)) if not free(x)), None)
        elif tool in ("Edit", "Write", "MultiEdit"):
            gated = None if free(path) else path
        else:
            gated = None
        if gated:
            miss = R.missing_steps(rec, tp)
            if miss:
                tid = rec["type"]
                names = ", ".join(WT.step_name(s) for s in miss)
                deny(
                    f"STOP (Hook, Quittung {sid}): Auftrags-Typ ist `{tid}` "
                    f"({WT.label_of(tid)}), die Pflichtkette ist aber noch offen: {names}. "
                    f"{WT.what_of(tid)}"
                    f"\n\nErst die Kette laufen lassen, dann schreiben. Passt der Typ nicht mehr "
                    f"zur Aufgabe, Typ neu setzen:\n"
                    f"  python .claude/hooks/receipt.py --sid {sid} --type <typ>   "
                    f"(Liste: --types)\n"
                    f"Schritt bewusst auslassen:\n"
                    f"  python .claude/hooks/receipt.py --sid {sid} --skip {WT.step_name(miss[0])} "
                    f"--why \"<ein Satz>\""
                    + _sub_hint(caller)
                )
    sys.exit(0)


run(main)
