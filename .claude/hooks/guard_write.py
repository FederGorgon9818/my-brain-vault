"""PreToolUse(Edit|Write|MultiEdit): harter Waechter fuer neue Hypothesen-Zeilen.

Bisher gab's fuer "variant-scout + strategy-auditor VOR dem Bank-Eintrag" (Regel
01.09.2026) nur Erinnerungen (after_change.py direkt nach dem Schreiben, on_stop.py
am Sessionende) -- keine Sperre wie bei Box-Sync (regression_ok) oder Enqueue
(pipeline_ok). Ergebnis (Audit 21.09.2026): mehrere Hypothesen-Baenke (Momentum &
Averages, PCA & Faktorstruktur) blieben ueber Sessions hinweg ohne die beiden Agents,
weil eine reine Text-Erinnerung bei viel parallelem Arbeiten untergeht. Dieser Hook
macht daraus dieselbe Art harten Gate wie guard_bash.py.

Deckt ZWEI Zugaenge ab, weil #166 zeigte, dass die Bank monatelang direkt im Code
wuchs und die Vault-`.md` nur ein nachgezogener Snapshot war (logbook-distiller-Fund
21.09.2026, selber Tag wie der Hook-Bau -- die erste Fassung deckte nur die `.md` ab):
1. `Hypothesen-Bank (*).md` im Vault: neue Tabellenzeile mit ID-Praefix.
2. `discovery/hypothesis_bank.py`: neuer `H("ID-XX", ...)`-Aufruf (Modulebene,
   kein Einzug -- so steht jede bestehende Zeile in der Datei).

Blockt NUR bei einer echten NEUEN Hypothese (neue Tabellenzeile bzw. neuer H(-Aufruf,
der im old_string noch nicht so vorkam, oder ein kompletter Write/Neuanlage der Datei)
-- reine Status-/Buch-Luecke-/Formatierungs-Aenderungen an Bestehendem loesen nichts
aus, sonst waere jede Korrektur blockiert.

Pruefung: im TRANSKRIPT DIESER SESSION muessen variant-scout UND strategy-auditor
(oder die Workflows ein-weg/konzept-weg, die beide intern aufrufen) schon vorgekommen
sein. Override fuer echte False Positives (Formatierung, die zufaellig wie eine neue
ID-Zeile/ein neuer H(-Aufruf aussieht): `python .claude/hooks/mark.py hypothese_ok`
-- gilt nur, solange die betroffene Datei seitdem nicht wieder neu angefasst wurde
(gleiches Muster wie regression_ok/pipeline_ok).
"""
from _common import *  # noqa

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

_ID_ROW = re.compile(r"^\s*\|\s*[A-Z]{1,4}-?\d{1,3}\s*\|", re.M)
_H_CALL = re.compile(r"^H\(\s*[\"']([A-Z]{1,4}-?\d{1,3}[a-z]?)[\"']", re.M)
_BANK_PATH = re.compile(r"hypothesen-bank \([^)]*\)\.md$|discovery/hypothesis_bank\.py$", re.I)


def _new_row_added(tool, ti):
    """True, wenn der Edit eine neue Hypothese einfuehrt -- Tabellenzeile mit
    ID-Praefix (Vault-`.md`) oder H("ID-XX", ...)-Aufruf (hypothesis_bank.py) --,
    die im alten Text so noch nicht stand. Bestehende Zeilen umformulieren/mit
    Ergebnis markieren loest nichts aus."""
    if tool == "Write":
        return True  # komplette Neuanlage/Ueberschreiben der Datei
    edits = ti.get("edits") if tool == "MultiEdit" else [ti]
    for e in edits or []:
        old_s, new_s = e.get("old_string") or "", e.get("new_string") or ""
        old_ids = set(_ID_ROW.findall(old_s)) | set(_H_CALL.findall(old_s))
        new_ids = set(_ID_ROW.findall(new_s)) | set(_H_CALL.findall(new_s))
        if new_ids - old_ids:
            return True
    return False


def main():
    inp = read_input()
    tool = inp.get("tool_name") or ""
    ti = inp.get("tool_input") or {}
    path = norm(ti.get("file_path"))
    if not path or not _BANK_PATH.search(path):
        sys.exit(0)
    if not _new_row_added(tool, ti):
        sys.exit(0)

    # Override: bewusst gesetzt und juenger als die Datei selbst.
    override_t = marker_time("hypothese_ok")
    file_t = mtime(ti.get("file_path"))
    if override_t and (file_t is None or override_t > file_t):
        sys.exit(0)

    tp = inp.get("transcript_path")
    used = set()
    if tp and Path(tp).is_file():
        try:
            from agent_usage_audit import scan, used_agent_names
            used = used_agent_names(scan(Path(tp)))
        except Exception:
            sys.exit(0)  # Hook darf nie kaputt blockieren

    missing = [a for a in ("variant-scout", "strategy-auditor") if a not in used]
    if missing:
        deny(
            "STOP (Hook): neue Hypothesen-Zeile in "
            f"'{Path(path).name}', aber {' und '.join(missing)} sind in dieser Session "
            "noch nicht gelaufen. Regel 01.09.2026: variant-scout (Varianten je Hypothese) "
            "dann strategy-auditor (Batch-Story-Check), BEVOR die Zeile in die Bank geht "
            "-- am einfachsten ueber den Skill/Workflow `ein-weg`. Falsch erkannt (keine "
            "echte neue Hypothese, nur Formatierung/Status-Update)? "
            "`python .claude/hooks/mark.py hypothese_ok` setzt den Marker von Hand."
        )
    sys.exit(0)


run(main)
