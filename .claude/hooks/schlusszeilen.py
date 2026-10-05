"""Schlusszeilen-Check (beschlossen Max, 05.10.2026).

Jede Antwort auf eine Aufgabe endet mit den Schlusszeilen aus der CLAUDE.md:
Modell-Empfehlung, /clear ja/nein und, wenn im Zug etwas geaendert wurde, die
Daily-Note-Bestaetigung. Bisher reine Erinnerung, ab jetzt prueft on_stop.py Teil 6.

Locker erkannt (Max' Antworten sind frei formuliert), einmal je Prompt geblockt,
nie zweimal hintereinander (stop_hook_active). Zwischenmeldungen ("laeuft, ich
warte auf die Agents") bleiben frei. Tests: python .claude/scripts/test_schlusszeilen.py
"""
import json
import re

EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
BASH_WRITE = re.compile(r">>|set-content|add-content|out-file|"
                        r"sed\s+-i|git\s+commit|\bmv\s|\bcp\s|move-item|copy-item|remove-item|\brm\s", re.I)
NOT_MAX = re.compile(r"^\s*(<agent-message|<task-notification|<system-reminder|\[system notification|"
                     r"another claude session sent a message)", re.I)

# Locker, weil Max' Schlussbloecke frei formuliert sind (Gegenprobe 251 echte Zuege, 05.10.):
# "wuerde ich sonnet nehmen und vorher /clear", "Clear: nein", "Kontext kann bleiben",
# "aktuelle Session kann weiterlaufen", "in die heutige Notiz eingetragen".
RX_MODEL_NAME = re.compile(r"\b(sonnet|haiku|opus|fable)\b", re.I)
RX_CLEAR = re.compile(r"/?\bclear\b|frische[nr]? session|neue[nr]? session|sessionwechsel|"
                      r"kontext\w* (weiter|behalten|bleib|kann bleiben|weiterverw)|session (kann |darf )?weiter|"
                      r"gleiche[nr]? session|aktuelle[nr]? session|weiterverwend|weiter(machen|arbeiten) (hier|in)", re.I)
RX_DAILY = re.compile(r"daily[\s-]?note|tagesnotiz|heutige[nr]? notiz|in die notiz (vom|von heute)", re.I)
RX_WAITING = re.compile(r"\b(warte|wartet|läuft noch|laeuft noch|melde mich|sobald .{0,40}(zurück|fertig|da ist))", re.I)

RX_WAITING2 = re.compile(r"\b(fehlt (nur )?noch|noch auf (den|die|das))\b", re.I)
RX_LAUNCHED = re.compile(r"Async agent launched", re.I)
RX_DONE_ID = re.compile(r"<tool-use-id>\s*(\S+?)\s*</tool-use-id>")

MIN_LEN_NO_CHANGE = 600   # reine Antworten: erst ab hier ist es eine "Aufgabe"
TAIL = 1500               # Schlusszeilen stehen am Ende
LOG_NAME = "schluss_log.jsonl"


def log(state_dir, sid, prompt, missing_parts, blocked):
    """Jeden Treffer mitschreiben, damit die Fehlalarm-Quote abnehmbar ist."""
    try:
        import time
        state_dir.mkdir(parents=True, exist_ok=True)
        with open(state_dir / LOG_NAME, "a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "sid": str(sid)[:8],
                                "prompt": (prompt or "")[:120], "missing": missing_parts,
                                "blocked": blocked}, ensure_ascii=False) + "\n")
    except Exception:
        pass


def _user_text(rec):
    c = (rec.get("message") or {}).get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
            return None
        return " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    return None


def last_turn(lines):
    """Aus Transkript-Zeilen: (Max-Prompt, finaler Antworttext, Aenderung_im_Zug).

    Laufen im Zug noch Hintergrund-Agents (gestartet, aber keine task-notification
    zurueck), ist die Antwort eine Zwischenmeldung: dann kommt als Text "" zurueck
    und der Check greift nicht (Live-Fund 05.10.2026, erster Tag)."""
    prompt, texts, changed = None, [], False
    agent_ids, launched, done = set(), set(), set()
    for line in lines:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if rec.get("isSidechain"):
            continue
        typ = rec.get("type")
        if typ == "user" and not rec.get("isMeta"):
            c = (rec.get("message") or {}).get("content")
            for b in c if isinstance(c, list) else []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in agent_ids:
                    if RX_LAUNCHED.search(json.dumps(b.get("content"), ensure_ascii=False)):
                        launched.add(b.get("tool_use_id"))
            done.update(RX_DONE_ID.findall(line))
            t = _user_text(rec)
            if t and t.strip() and not NOT_MAX.search(t[:400]):
                prompt, texts, changed = t.strip(), [], False
                agent_ids, launched, done = set(), set(), set()
            continue
        if typ == "assistant" and prompt is not None:
            for b in (rec.get("message") or {}).get("content") or []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and b.get("text", "").strip():
                    texts.append(b["text"])
                elif b.get("type") == "tool_use":
                    name = b.get("name")
                    inp = b.get("input") or {}
                    if name == "Agent":
                        agent_ids.add(b.get("id"))
                    if name in EDIT_TOOLS:
                        changed = True
                    elif name in ("Bash", "PowerShell") and BASH_WRITE.search(str(inp.get("command", ""))):
                        changed = True
    if launched - done:
        return prompt, "", changed
    return prompt, (texts[-1] if texts else ""), changed


def missing(final_text, changed):
    """-> Liste fehlender Schlusszeilen (leer = alles da oder Check greift nicht)."""
    text = final_text or ""
    if not text.strip():
        return []
    if not changed and len(text) < MIN_LEN_NO_CHANGE:
        return []
    if len(text) < 900 and (RX_WAITING.search(text) or RX_WAITING2.search(text)):
        return []
    tail = text[-TAIL:]
    out = []
    if not changed and text.rstrip().endswith("?"):
        return []   # Rueckfrage vor dem Handeln ("Offene Fragen zuerst"), keine Aufgabe erledigt
    if not RX_MODEL_NAME.search(tail):
        out.append("Modell-Empfehlung (sonnet/haiku/opus/fable)")
    if not RX_CLEAR.search(tail):
        out.append("/clear ja oder nein")
    if changed and not RX_DAILY.search(tail):
        out.append("Daily-Note-Bestaetigung (was eingetragen wurde)")
    return out
