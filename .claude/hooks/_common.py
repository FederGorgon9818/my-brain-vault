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
ENGINE_CORE = ["sigcore.py", "controls.py", "overfit.py", "qbt.py", "tsmom.py", "maband.py",
               "discovery/hypothesis_bank.py"]
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
