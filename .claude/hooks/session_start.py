"""SessionStart: Inbox + Stale-State + Vault-Kurzbriefing deterministisch in den Kontext geben.

Vault-Kurzbriefing (Regel Max, 09.09.2026): "Bei Session-Start Daily Notes/Projekte
lesen" stand bis dahin nur als Text in der CLAUDE.md - eine Session konnte das
befolgen oder vergessen. Damit der Kontext wirklich, wirklich da ist (nicht nur
"sollte gelesen werden"), spielt der Hook ab jetzt eine Kurzfassung der letzten
2 Daily Notes, der aktiven Projekte und des neuesten Logbuch-Eintrags IMMER mit
ein - bewusst kompakt (Titel + Kurzfassung, nicht der volle Text), damit es nicht
gegen die Token-Disziplin läuft. Ersetzt nicht "Kontext bei Bedarf" (volles
Briefing auf Zuruf), sondern stellt eine Mindest-Grundlage sicher, die keine
Session mehr übersehen kann.
"""
import re

from _common import *  # noqa


def _strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n?", text, re.S)
    return text[m.end():] if m else text


def _frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    return m.group(1) if m else ""


def _daily_note_files():
    d = VAULT / "Daily Notes"
    try:
        files = [p for p in d.glob("*.md") if re.match(r"^\d{4}-\d{2}-\d{2}$", p.stem)]
    except Exception:
        return []
    return sorted(files, key=lambda p: p.stem, reverse=True)


def _daily_note_digest(path, limit=450):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    body = _strip_frontmatter(text)
    title, summary, started = "", [], False
    for l in body.splitlines():
        s = l.strip()
        if not started:
            if s.startswith("# "):
                title = s.lstrip("#").strip()
                started = True
            continue
        if s.startswith("#"):
            break
        if not s or s.startswith(("⬅️", ">", "!")):
            continue
        summary.append(s)
    txt = " ".join(summary).strip()
    if len(txt) > limit:
        txt = txt[:limit].rsplit(" ", 1)[0] + "…"
    label = path.stem + (f" — {title}" if title else "")
    return f"{label}: {txt}" if txt else label


def _active_projects():
    d = VAULT / "Projekte"
    out = []
    try:
        files = sorted(d.glob("*.md"))
    except Exception:
        return out
    for p in files:
        if p.name.startswith("_"):
            continue
        try:
            fm = _frontmatter(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        m = re.search(r"^status:\s*(.+)$", fm, re.M)
        status = m.group(1).strip() if m else "?"
        out.append(f"{p.stem} ({status})")
    return out


def _last_logbook_entry():
    p = VAULT / "Bereiche" / "Strategie-Logbuch.md"
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return None
    matches = re.findall(r"^## (#\d+ — .+)$", text, re.M)
    return matches[-1] if matches else None


def _recent_sessions_digest(exclude_sid):
    """Regel Max, 09.09.2026: grober Ueberblick ueber die zuletzt aktiven anderen
    Sessions auf DIESEM Geraet (Transkripte sind lokal, nicht geraeteuebergreifend -
    das leistet die Daily Note). Nur zur Einordnung moeglicher Ueberschneidungen,
    kein Ersatz fuer session-guard vor einer echten gemeinsamen Datei-Aenderung."""
    sessions = recent_local_sessions(exclude_sid=exclude_sid, limit=5)
    if not sessions:
        return None
    lines = []
    for m in sessions:
        proj = Path(m["cwd"]).name if m["cwd"] else "?"
        bit = f"{fmt_age(m['last_activity'])} — {proj}"
        if m["title"]:
            bit += f": {m['title']}"
        elif m["last_prompt"]:
            bit += f": {m['last_prompt'][:80]}"
        if m["made_changes"]:
            bit += " (hat Dateien geaendert)"
        lines.append(bit)
    return "Andere Sessions auf diesem Geraet, zuletzt aktiv (nur dieses Geraet, kein Ersatz fuer session-guard):\n" + "\n".join(lines)


def main():
    inp = read_input()
    notes = []
    # Inbox: Brain Dump ohne Vorlagenzeilen
    bd = VAULT / "Inbox" / "Brain Dump.md"
    try:
        body = bd.read_text(encoding="utf-8").split("---")[-1]
        content = []
        for l in body.splitlines():
            s = l.strip()
            if not s or s in ("-", "#") or s.startswith(("#", ">", "⬅️")):
                continue
            content.append(l.rstrip())
        if content:
            notes.append("Inbox (Brain Dump) hat Eintraege:\n" + "\n".join(content[:40]))
        else:
            notes.append("Inbox (Brain Dump): leer.")
    except Exception:
        pass
    others = [p.name for p in (VAULT / "Inbox").glob("*.md") if p.name != "Brain Dump.md"]
    if others:
        notes.append("Weitere Inbox-Notizen: " + ", ".join(others))

    if ENGINE:
        stale = book_newer_than_marker("push_next_at")
        if stale:
            notes.append(f"Stale-State: {', '.join(stale)} neuer als letzter push-next "
                         f"({fmt_age(marker_time('push_next_at'))}). Erst finalize + push-next.")
        core_t, core_f = newest_engine_core()
        ok_t = marker_time("regression_ok")
        if core_t and (ok_t is None or ok_t < core_t):
            notes.append(f"Engine-Kern ({core_f}) geaendert {fmt_age(core_t)}, kein Regressions-OK seitdem. "
                         "Vor einem Box-Sync: engine-regression-tester.")
        if not marker_time("push_next_at"):
            # Erststart auf diesem Geraet: ab jetzt zaehlen
            touch_marker("push_next_at")
    else:
        notes.append("Hooks: kein lokaler Engine-Ordner (Laptop / PC aus). Buch- und Sync-Waechter sind hier "
                     "passiv, Kommando-Waechter (Dauerlaeufer, Log-Reads, Enqueue) aktiv.")

    # Vault-Kurzbriefing: deterministisch, nicht davon abhaengig ob eine Session
    # dran denkt, Daily Notes/Projekte/Logbuch von sich aus zu lesen.
    digests = [d for d in (_daily_note_digest(p) for p in _daily_note_files()[:2]) if d]
    if digests:
        notes.append("Letzte Daily Notes (Kurzfassung, bei Bedarf volle Datei lesen):\n" + "\n".join(digests))
    projects = _active_projects()
    if projects:
        notes.append("Projekte/ (Status): " + "; ".join(projects))
    last_entry = _last_logbook_entry()
    if last_entry:
        notes.append("Neuester Strategie-Logbuch-Eintrag: " + last_entry)

    # Research-Wiedervorlage (Regel Max, 28.09.2026, Anlass Logbuch #074): Negativbefunde
    # und Firmenregeln altern. Nur eine Zeile, und nur wenn etwas faellig ist.
    try:
        import sys as _sys
        _sys.path.insert(0, str(VAULT / ".claude" / "scripts"))
        from research_cache_expiry import summary_line
        line = summary_line()
        if line:
            notes.append(line)
    except Exception:
        pass  # ein Hinweis-Hook darf nie die Session blockieren

    sessions_digest = _recent_sessions_digest(exclude_sid=inp.get("session_id"))
    if sessions_digest:
        notes.append(sessions_digest)

    context("\n".join(notes), "SessionStart")


run(main)
