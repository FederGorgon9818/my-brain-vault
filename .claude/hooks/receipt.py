"""Prozess-Quittung je Session: welcher Auftrags-Typ, welche Kette, was lief schon.

Regel Max, 21.09.2026 ("ich muss immer selbst ansagen, dass die Agents laufen").

Das Problem mit der alten Loesung: agent_triggers.py hat per Regex ERINNERT, und
on_stop.py hat rueckblickend per Heuristik geprueft, ob ein Agent gelaufen ist.
Beides ist raten. Wenn Max diktiert ("rechne mir das mal durch"), trifft kein
Muster sauber, und eine Erinnerung im Kontext geht bei paralleler Arbeit unter.

Die Quittung macht daraus etwas Deterministisches:
  1. on_prompt.py legt bei jedem Auftrag eine OFFENE Quittung an (Typ unbestimmt)
     und schlaegt Typen vor.
  2. Claude schreibt den Typ fest:  receipt.py --sid <id> --type <typ>
     Damit steht die Pflichtkette, und zwar unabhaengig von der Formulierung.
  3. guard_chain.py blockt die typischen Aktionen des Typs, solange die Kette
     nicht gelaufen ist.
  4. on_stop.py laesst die Session nicht enden, solange eine Quittung offen ist.

Parallel-sicher: eine Datei je Session (Max faehrt regelmaessig 5+ Sessions).
Die Kurz-ID (<sid8>) steht in jeder Hook-Meldung, damit der CLI-Aufruf immer die
RICHTIGE Quittung trifft und nicht die der Nachbarsession.

Bewusste Ausnahme statt Blockade:
    receipt.py --sid <id> --skip <schritt> --why "<ein Satz>"
Das ist der Override aus Max' Entscheidung "blocken, aber Override moeglich".
Der Grund landet in der Quittung und damit im Retro -- eine Ausnahme ohne Grund
gibt es nicht.

CLI (aus dem Vault-Root):
    python .claude/hooks/receipt.py --types
    python .claude/hooks/receipt.py --sid a1b2c3d4 --type rechnen
    python .claude/hooks/receipt.py --sid a1b2c3d4 --show
    python .claude/hooks/receipt.py --sid a1b2c3d4 --skip design-guard --why "reiner Text-Fix"
    python .claude/hooks/receipt.py --sid a1b2c3d4 --close
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import STATE, mtime  # noqa: E402
import work_types as WT  # noqa: E402

RECEIPTS = STATE / "receipts"
# Aelter als das hier -> die Quittung gehoert zu einer alten Aufgabe, nicht mehr
# zur laufenden Session. Verhindert, dass eine vergessene Quittung von gestern
# heute blockiert.
MAX_AGE_H = 12


def sid8(session_id):
    return (str(session_id or "").replace("-", "") or "unknown")[:8]


def path_for(session_id):
    return RECEIPTS / f"{sid8(session_id)}.json"


def load(session_id):
    """Quittung dieser Session, oder None.

    Kollisionsschutz: die Datei heisst nach den ersten 8 Zeichen der Session-ID.
    Wird die VOLLE ID uebergeben (so rufen die Hooks es auf), muss sie zu der in
    der Datei passen -- sonst wuerde eine zweite Session mit gleichem Praefix die
    fremde Quittung erben und gegen deren Kette geprueft (im Selbsttest am Bautag
    genau so passiert). Der CLI-Aufruf uebergibt nur die Kurz-ID; dort greift die
    Pruefung bewusst nicht, weil sie dort nichts pruefen koennte.
    """
    p = path_for(session_id)
    try:
        if not p.is_file():
            return None
        rec = json.loads(p.read_text(encoding="utf-8"))
        # Verfall gegen die LETZTE Aktivitaet, nicht gegen die Anlagezeit: eine lange
        # Session verlor sonst nach 12 h stillschweigend ihren Typ und damit das Gate
        # (Fund verdict-auditor, 21.09.2026 -- Alter des Auftrags ist nicht Alter der
        # Arbeit daran).
        last = float(rec.get("last_seen") or rec.get("set_at") or rec.get("created") or 0)
        if time.time() - last > MAX_AGE_H * 3600:
            return None
        sid_in = str(session_id or "")
        known = str(rec.get("sid_full") or "")
        if len(sid_in) > 8 and len(known) > 8 and known != sid_in:
            return None
        return rec
    except Exception:
        return None


def save(rec):
    try:
        RECEIPTS.mkdir(parents=True, exist_ok=True)
        path_for(rec.get("sid")).write_text(
            json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        return True
    except Exception:
        return False


def ensure(session_id, prompt_hint=None, suggested=None):
    """Offene Quittung anlegen, falls noch keine da ist. Gibt (rec, neu?) zurueck."""
    rec = load(session_id)
    if rec:
        # Neuer Auftrag in derselben Session: Hinweis mitfuehren, Typ bleibt stehen
        # (Claude setzt ihn aktiv um, wenn sich die Aufgabe wirklich aendert).
        rec["last_seen"] = time.time()
        if prompt_hint:
            rec["last_prompt"] = prompt_hint[:200]
            rec["prompts"] = int(rec.get("prompts") or 1) + 1
        save(rec)
        return rec, False
    rec = {
        "sid": sid8(session_id), "sid_full": str(session_id or ""),
        "created": time.time(), "last_seen": time.time(), "type": None, "set_at": None,
        "chain": [], "skipped": {}, "note": None, "closed": False,
        "last_prompt": (prompt_hint or "")[:200], "prompts": 1,
        "suggested": list(suggested or []),
    }
    save(rec)
    return rec, True


def set_type(session_id, tid, note=None, why=None):
    """Typ festschreiben.

    Verplombt gegen den billigsten Ausweg (Fund verdict-auditor, 21.09.2026): wer von
    einem Typ MIT Pflichtkette auf einen ohne Kette (`frage`, `vault`) wechselt, hat
    das Gate umgangen, ohne je eine Ausnahme begruenden zu muessen -- der Block-Text
    bewarb diesen Weg sogar selbst. Deshalb braucht genau dieser Wechsel dieselbe
    Begruendungspflicht wie `--skip`, und jeder Wechsel landet in `type_history`.
    Hochstufen (keine Kette -> Kette) bleibt frei: das macht den Prozess strenger.
    """
    if tid not in WT.BY_ID:
        return None, f"Unbekannter Typ '{tid}'. Bekannt:\n{WT.overview()}"
    rec = load(session_id) or ensure(session_id)[0]
    old = rec.get("type")
    if old and old != tid and WT.chain_of(old) and not WT.chain_of(tid):
        if not why or len(why.strip()) < 8:
            return None, (
                f"Wechsel von `{old}` (Kette: "
                f"{', '.join(WT.step_name(s) for s in WT.chain_of(old))}) auf `{tid}` "
                f"(keine Kette) wuerde die Pflichtkette aufheben. Das ist eine Ausnahme "
                f"und braucht einen Grund:\n"
                f"  --type {tid} --why \"<warum der Auftrag doch kein {old} ist>\"\n"
                f"Geht es nur um EINEN Schritt der Kette, ist `--skip <schritt> --why ...` "
                f"das richtige Werkzeug."
            )
        rec.setdefault("downgrades", []).append(
            {"from": old, "to": tid, "why": why.strip(), "at": time.time()})
    if old and old != tid:
        rec.setdefault("type_history", []).append({"type": old, "at": rec.get("set_at")})
    rec["type"] = tid
    rec["set_at"] = time.time()
    rec["last_seen"] = time.time()
    rec["chain"] = WT.chain_of(tid)
    rec["closed"] = False
    if note:
        rec["note"] = note
    save(rec)
    return rec, None


def skip(session_id, step, why):
    rec = load(session_id)
    if not rec:
        return None, "Keine offene Quittung fuer diese Session."
    if not why or len(why.strip()) < 8:
        return None, "Ausnahme braucht einen Grund (--why \"<ein Satz>\"), sonst ist sie keine."
    rec.setdefault("skipped", {})[step] = {"why": why.strip(), "at": time.time()}
    save(rec)
    return rec, None


def close(session_id):
    rec = load(session_id)
    if not rec:
        return None, "Keine offene Quittung fuer diese Session."
    rec["closed"] = True
    rec["closed_at"] = time.time()
    save(rec)
    return rec, None


# ---------------------------------------------------------------------------
# Kettenstand: was fehlt noch?
# ---------------------------------------------------------------------------

def _session_usage(transcript_path):
    """(Agent-Namen, Workflow-Namen) aus dem Transkript dieser Session."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
        from agent_usage_audit import scan, used_agent_names
        s = scan(Path(transcript_path))
        return used_agent_names(s), set(s["workflows"])
    except Exception:
        return set(), set()


def missing_steps(rec, transcript_path):
    """Schritte der Kette, die weder gelaufen noch bewusst uebersprungen sind."""
    if not rec or not rec.get("type"):
        return []
    agents, workflows = _session_usage(transcript_path) if transcript_path else (set(), set())
    skipped = set((rec.get("skipped") or {}).keys())
    missing = []
    for step in rec.get("chain") or []:
        name = WT.step_name(step)
        if name in skipped or step in skipped:
            continue
        if WT.step_is_workflow(step):
            # Workflow-Namen tragen im Transkript teils ein Run-Suffix.
            if any(w == name or str(w).startswith(name + "-") for w in workflows):
                continue
        elif name in agents:
            continue
        missing.append(step)
    return missing


def state_line(rec, transcript_path=None):
    """Einzeiler fuer Hook-Meldungen."""
    if not rec:
        return "keine Quittung"
    if not rec.get("type"):
        return f"Quittung {rec['sid']}: Typ noch nicht gesetzt"
    miss = missing_steps(rec, transcript_path)
    chain = " -> ".join(WT.step_name(s) for s in rec.get("chain") or []) or "(keine Kette)"
    if miss:
        return (f"Quittung {rec['sid']}: Typ `{rec['type']}` ({WT.label_of(rec['type'])}), "
                f"Kette {chain}, OFFEN: {', '.join(WT.step_name(s) for s in miss)}")
    return f"Quittung {rec['sid']}: Typ `{rec['type']}`, Kette {chain} vollstaendig"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Prozess-Quittung je Session")
    ap.add_argument("--sid", help="Kurz-ID aus der Hook-Meldung")
    ap.add_argument("--type", dest="tid", help="Auftrags-Typ setzen")
    ap.add_argument("--note", help="Freitext, was konkret die Aufgabe ist")
    ap.add_argument("--skip", help="Schritt bewusst auslassen (braucht --why)")
    ap.add_argument("--why", help="Grund fuer die Ausnahme")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--close", action="store_true", help="Aufgabe abgeschlossen")
    ap.add_argument("--types", action="store_true", help="Alle Typen + Ketten zeigen")
    a = ap.parse_args(argv)

    if a.types or not (a.sid or a.tid):
        print("Auftrags-Typen und Pflichtketten:\n")
        print(WT.overview())
        print("\nSetzen:  python .claude/hooks/receipt.py --sid <id> --type <typ>")
        return 0

    if not a.sid:
        print("Fehlt: --sid <Kurz-ID>. Die steht in der Hook-Meldung dieser Session.")
        return 1

    if a.tid:
        rec, err = set_type(a.sid, a.tid, a.note, a.why)
        if err:
            print(err)
            return 1
        chain = " -> ".join(WT.step_name(s) for s in rec["chain"]) or "(keine Kette)"
        print(f"Quittung {rec['sid']}: Typ `{a.tid}` ({WT.label_of(a.tid)})")
        print(f"Pflichtkette: {chain}")
        if rec["chain"]:
            print(f"Warum: {WT.what_of(a.tid)}")
        return 0

    if a.skip:
        rec, err = skip(a.sid, a.skip, a.why or "")
        if err:
            print(err)
            return 1
        print(f"Ausnahme vermerkt: {a.skip} -- {a.why}")
        return 0

    if a.close:
        rec, err = close(a.sid)
        if err:
            print(err)
            return 1
        print(f"Quittung {rec['sid']} geschlossen.")
        return 0

    rec = load(a.sid)
    print(state_line(rec))
    if rec and rec.get("skipped"):
        for k, v in rec["skipped"].items():
            print(f"  Ausnahme {k}: {v.get('why')}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
