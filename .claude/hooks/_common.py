"""Gemeinsame Helfer für die Claude-Code-Hooks (Max' Vault).

Alle Hooks lesen das Hook-JSON von stdin, prüfen etwas Deterministisches
und antworten per JSON auf stdout. Sie müssen schnell sein (ein Python-Start
pro Tool-Aufruf) und dürfen NIE selbst crashen: jeder Fehler → stiller Exit 0,
damit ein kaputter Hook nie die Arbeit blockiert.
"""
import json
import os
import re
import sys
import time
from pathlib import Path

# Der Harness schickt/erwartet UTF-8 auf stdin/stdout. Ohne das hier faellt
# Python auf Windows auf die Konsolen-Codepage zurueck (hier cp1252) - jeder
# Umlaut, Gedankenstrich oder jedes Emoji im Hook-Payload (staendig im Vault:
# Daily Notes, Inbox, Logbuch, auch in Bash-Kommandos) macht dann entweder die
# stdout-JSON ungueltig (Kontext geht verloren) oder laesst read_input() beim
# Decodieren scheitern - der Fehler wird dort still geschluckt und liefert {}
# zurueck, also laufen Bash/Read-Waechter leer, ohne dass irgendwo ein Fehler
# auftaucht. Fund + Fix: 09.09.2026, Anlass war "Kontext ist teilweise nicht
# da" (Max). Vor jedem Hook-Import fest auf UTF-8 stellen, nicht raten lassen.
for _stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

VAULT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

# Engine-Ordner: PC-Pfad, per Env überschreibbar (Tests, Laptop, spätere Umzüge).
_ENGINE_CANDIDATES = [
    os.environ.get("MAXLAB_ENGINE"),
    r"C:\Users\maxlk\Projects\trading-data\engine",
]
ENGINE = next((Path(p) for p in _ENGINE_CANDIDATES if p and Path(p).is_dir()), None)
HUB = next((Path(p) for p in [os.environ.get("MAXLAB_HUB"), r"C:\Users\maxlk\Projects\hub"] if p and Path(p).is_dir()), None)

# Marker-Dateien: im Engine-Ordner (nicht versioniert, gilt für alle Sessions auf
# dem Gerät). Ohne Engine (Laptop) im Vault unter .claude/hooks/.state (gitignored).
STATE = (ENGINE / ".claude_hooks") if ENGINE else (VAULT / ".claude" / "hooks" / ".state")

# Engine-Kern: Änderung hier → engine-regression-tester vor jedem Box-Sync.
# EINE Liste für die Sync-Sperre (newest_engine_core) und den Hinweis in after_change.py. Deckt die
# fingerprint_files aus discovery/golden_masters.json ab plus die Mess-/Käfig-Schicht (AP246,
# pipeline-auditor 29.09.2026: eval_plan, cage_policy_lib, operating_point fehlten, und "controls.py"
# lag nie im Engine-Root, der Eintrag griff also nie).
ENGINE_CORE = ["sigcore.py", "overfit.py", "qbt.py", "tsmom.py", "maband.py", "vwap_pullback.py",
               "asian.py", "rv.py", "developer_run.py", "developer/firstbar_core.py",
               "discovery/controls.py", "discovery/hypothesis_bank.py", "discovery/discovery_lib.py",
               "discovery/discovery_runner.py",
               "eval_plan.py", "cage_policy_lib.py", "operating_point.py"]
# Discovery-Code, den der laufende Runner nur nach Neustart neu lädt.
RUNNER_CODE_DIR = "discovery"
BOOK_FILES = ["book_state.json", "book_state_next.json"]


def read_input():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def mtime(p):
    try:
        return Path(p).stat().st_mtime
    except Exception:
        return None


def marker_path(name):
    return STATE / name


def marker_time(name):
    return mtime(marker_path(name))


def touch_marker(name, when=None):
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        p = marker_path(name)
        p.touch(exist_ok=True)
        if when is not None:
            os.utime(p, (when, when))
    except Exception:
        pass


def engine_file(rel):
    return (ENGINE / rel) if ENGINE else None


def newest_engine_core():
    """(mtime, relpath) der jüngsten Kern-Datei, oder (None, None)."""
    best = (None, None)
    if not ENGINE:
        return best
    for rel in ENGINE_CORE:
        t = mtime(ENGINE / rel)
        if t and (best[0] is None or t > best[0]):
            best = (t, rel)
    return best


def book_newer_than_marker(marker):
    """Liste der Buch-Dateien, die jünger sind als der Marker."""
    if not ENGINE:
        return []
    mt = marker_time(marker)
    out = []
    for rel in BOOK_FILES:
        t = mtime(ENGINE / rel)
        if t and (mt is None or t > mt + 1):
            out.append(rel)
    return out


def fmt_age(ts):
    if not ts:
        return "nie"
    d = time.time() - ts
    if d < 3600:
        return f"vor {int(d // 60)} min"
    if d < 86400:
        return f"vor {d / 3600:.1f} h"
    return f"vor {d / 86400:.1f} Tagen"


def norm(s):
    return (s or "").replace("\\", "/").lower()


def any_re(patterns, text, flags=re.I):
    return any(re.search(p, text, flags) for p in patterns)


# ---- Session-Transkripte (Cross-Session-Ueberblick, Daily-Note-Pflicht) ----
# Regel Max, 09.09.2026: jede Session soll grob wissen, was in anderen lokalen
# Sessions lief, und jede Session soll die Daily Note verlaesslich pflegen.
# Grenze: Transkripte liegen lokal unter ~/.claude/projects/, nicht im Git-Repo -
# das erfasst nur Sessions auf DEMSELBEN Geraet, nicht geraeteuebergreifend.
# Die Daily Note selbst ist die geraeteuebergreifende Garantie (Git-synchronisiert).

CLAUDE_PROJECTS = Path.home() / ".claude" / "projects"


def to_epoch(ts):
    """ISO-8601-Timestamp (wie in den Transkripten, mit 'Z') zu Unix-Epoch."""
    try:
        from datetime import datetime
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
    except Exception:
        return None


def scan_transcript_light(path):
    """Kompakter Scan eines Session-Transkripts: Titel, letzter echter User-Text,
    erste/letzte Aktivitaet, ob Dateien geaendert wurden. Bewusst schlank (kein
    Datei-Kollisions-Abgleich - das macht session_conflicts.py fuer session-guard)
    und schnell genug fuer einen Hook-Aufruf (< 0.1s auch fuer grosse Transkripte)."""
    meta = {
        "sid": path.stem, "cwd": None, "branch": None, "title": None,
        "last_prompt": None, "first_activity": None, "last_activity": None,
        "made_changes": False, "mtime": mtime(path),
    }
    try:
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not any(s in line for s in ('"tool_use"', '"cwd"', '"aiTitle"')):
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                ts = to_epoch(rec.get("timestamp"))
                if ts:
                    if meta["first_activity"] is None or ts < meta["first_activity"]:
                        meta["first_activity"] = ts
                    if meta["last_activity"] is None or ts > meta["last_activity"]:
                        meta["last_activity"] = ts
                if rec.get("cwd"):
                    meta["cwd"] = rec["cwd"]
                if rec.get("gitBranch"):
                    meta["branch"] = rec["gitBranch"]
                if rec.get("aiTitle"):
                    meta["title"] = rec["aiTitle"]
                if rec.get("type") == "user" and not rec.get("isMeta"):
                    content = rec.get("message", {}).get("content")
                    if isinstance(content, str) and content.strip():
                        meta["last_prompt"] = content.strip()[:160]
                if not meta["made_changes"]:
                    content = rec.get("message", {}).get("content")
                    if isinstance(content, list):
                        for block in content:
                            if (isinstance(block, dict) and block.get("type") == "tool_use"
                                    and block.get("name") in ("Edit", "Write", "MultiEdit", "NotebookEdit")):
                                meta["made_changes"] = True
                                break
    except Exception:
        pass
    return meta


def recent_local_sessions(exclude_sid=None, limit=5, max_scan=15):
    """Die zuletzt aktiven Sessions auf DIESEM Geraet, projektuebergreifend
    (alle Ordner unter ~/.claude/projects/), neueste zuerst. Erst per Datei-Mtime
    vorsortieren (billig), dann nur die Top-Kandidaten wirklich parsen (teurer)."""
    try:
        files = [p for p in CLAUDE_PROJECTS.glob("*/*.jsonl") if p.stem != exclude_sid]
    except Exception:
        return []
    files.sort(key=lambda p: mtime(p) or 0, reverse=True)
    out = []
    for p in files[:max_scan]:
        meta = scan_transcript_light(p)
        if meta["last_activity"]:
            out.append(meta)
        if len(out) >= limit * 2:  # genug Kandidaten, Rest per echter Aktivitaet sortieren
            break
    out.sort(key=lambda m: m["last_activity"] or 0, reverse=True)
    return out[:limit]


# ---- Antworten -------------------------------------------------------------

def out(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.stdout.flush()


def deny(reason, event="PreToolUse"):
    out({"hookSpecificOutput": {"hookEventName": event,
                                "permissionDecision": "deny",
                                "permissionDecisionReason": reason}})
    sys.exit(0)


def context(text, event):
    if text:
        out({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}})
    sys.exit(0)


def block_stop(reason):
    out({"decision": "block", "reason": reason})
    sys.exit(0)


def run(main):
    """Hook-Hauptfunktion absichern: jeder Fehler → still durchlassen."""
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # nie die Arbeit blockieren
        try:
            (STATE).mkdir(parents=True, exist_ok=True)
            with open(STATE / "hook_errors.log", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {Path(sys.argv[0]).name}: {e!r}\n")
        except Exception:
            pass
        sys.exit(0)
