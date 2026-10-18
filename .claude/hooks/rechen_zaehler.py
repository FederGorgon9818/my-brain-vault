"""Wirkungsmessung fuer den Rechen-Hinweis (Auftrag Max, 18.10.2026).

rechen_hinweis.py erinnert beim Prompt an "Rechnen nur in Code". Ob das wirkt, misst dieses Modul:
on_stop.py Teil 7 schreibt je Zug (ein Max-Prompt samt Antwort) eine Zeile nach
STATE/rechen_hinweis_log.jsonl, in dieselbe Datei, in die rechen_hinweis.py seine Treffer schreibt.

  rechen_ohne_code  die finale Antwort enthaelt Zahlen, die nicht nur Datum, Uhrzeit, Ticketnummer,
                    Commit, Dateiverweis oder Code sind, UND im Zug lief kein Bash/PowerShell-Aufruf mit python
  hinweis           fuer den Prompt kam ein Rechen-Hinweis (Zeile derselben Datei, gleiche sid, gleicher Prompt)
  python / agent    Rohwerte dahinter (Python lief, Agent oder Workflow lief), damit der Report sie trennen kann
  zahlen / beleg    Anzahl der gezaehlten Zahlen und die ersten drei samt Umfeld (damit die Stichprobe nachpruefbar ist)

Ein Proxy, in beide Richtungen schief: Zahlen, die unveraendert aus einer Datei oder einem Agent-Ergebnis
zitiert werden, zaehlen mit (zu viel). Jeder python-Aufruf im Zug nimmt das Flag weg, auch ein Test oder ein
Pull, Kopfrechnen in so einem Zug bleibt unsichtbar (zu wenig). Aussagekraft hat der Vergleich mit der Basis
vor dem Hinweis und der Verlauf, nicht der Absolutwert. Die Erkennung des Hinweises bleibt absichtlich eng
("gerechnet" heisst bei Max meist "Backtest gelaufen"). Zwischenmeldungen (Hintergrund-Agent offen) und
Agent-Rueckmeldungen zaehlen nicht, das regelt schlusszeilen.turn_info. Je Zug zaehlt in der Auswertung die
erste Zeile (nach einem Stop-Hook-Block folgt oft nur noch eine kurze Nachmeldung). Blockt nie: Fehler werden
verschluckt und in hook_errors.log geloggt.
Auswertung: python .claude/scripts/rechen_report.py --days 7. Tests: python .claude/scripts/test_rechen_zaehler.py
"""
import hashlib
import json
import re
import time
from pathlib import Path

import schlusszeilen as SZ
from rechen_hinweis import LOG_NAME

AGENT_TOOLS = {"Agent", "Task", "Workflow"}
TAIL_BYTES = 400_000   # so weit hinten im Log wird nach dem Hinweis zum Prompt gesucht

# --- Zahlen zaehlen ------------------------------------------------------------------------------
# Erst wegschneiden, was keine Rechengroesse ist, dann die uebrigen Zahlen zaehlen.
_DATEIEN = r"py|md|json|jsonl|js|ts|tsx|cs|ps1|sh|txt|html|css|ya?ml|toml|log|csv|exe|pdf|png|xlsx?"
_MONATE = r"jan|feb|m(?:ä|ae)r|apr|mai|jun|jul|aug|sep|okt|nov|dez"
_LABEL = (r"schritt|punkt|teil|stufe|abschnitt|option|fall|variante|phase|kapitel|nr|nummer|lehre|regel|"
          r"ticket|sprint|kw|version")
_WEG = [re.compile(p, f) for p, f in [
    (r"```.*?```", re.S),                                    # Codebloecke
    (r"`[^`\n]*`", 0),                                       # Inline-Code
    (r"\]\([^)\s]*\)", 0),                                   # Linkziel von [Text](pfad:12)
    (r"https?://\S+", 0),
    (rf"[\w./\\-]*\.(?:{_DATEIEN})\b(?::\d+(?:-\d+)?)?", re.I),   # Dateiverweise, auch datei.py:42
    (rf"\b\d{{1,2}}\.\d{{1,2}}\.(?:\d{{2,4}}\b)?|\b\d{{4}}-\d{{2}}-\d{{2}}\b|"
     rf"\b\d{{1,2}}\.\s?(?:{_MONATE})\w*(?:\s\d{{4}})?", re.I),  # Datum
    (r"\b(?:19|20)\d{2}\b(?![.,]\d)(?!\s?(?:€|\$|eur\b|euro\b|usd\b|dollar\b|%|k\b|x\b))", re.I),   # nackte Jahreszahl
    (r"\b\d{1,2}:\d{2}(?::\d{2})?\b|\b\d{1,2}\s?uhr\b", re.I),   # Uhrzeit
    (r"(?<!\w)#\d+(?:\s?/\s?#?\d+)*", 0),                    # #136, #067/#068
    (r"\b[A-Za-z]+[-_]?\d+(?:-\d+)*[A-Za-z]*\b", 0),          # AP411, KF-61, S2026-41, E8, k1, v4
    (r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b", 0),   # Commit-Hash
    (r"(?m)^[ \t>]*(?:[-*+][ \t]+)?(?:#{1,6}[ \t]*)?\*{0,2}\d+[.)][ \t]", 0),   # "1. " am Zeilenanfang
    (rf"\b(?:{_LABEL})\.?\s*\d+[a-z]?\b", re.I),             # "Teil 6", "Stufe 2", "Abschnitt 0b"
]]
_ZAHL = re.compile(r"\d+(?:[.,]\d+)*")


def _bereinigt(text):
    t = text or ""
    for rx in _WEG:
        t = rx.sub(" ", t)
    return t


def zahlen(text):
    """-> Liste der Zahlen im Text, die keine Datums-, Uhrzeit-, Ticket-, Commit-, Datei- oder Code-Zahl sind."""
    return _ZAHL.findall(_bereinigt(text))


def belege(text, n=3, umfeld=25):
    """-> die ersten n gezaehlten Zahlen mit je `umfeld` Zeichen Text davor und danach (aus dem bereinigten Text)."""
    t = _bereinigt(text)
    out = []
    for m in _ZAHL.finditer(t):
        out.append(" ".join(t[max(0, m.start() - umfeld):m.end() + umfeld].split()))
        if len(out) >= n:
            break
    return out


# --- Lief im Zug Python? -------------------------------------------------------------------------
_TRENNER = re.compile(r"&&|\|\||[;|\n]")
_ERSTES = re.compile(r"""\s*&?\s*("[^"]*"|'[^']*'|\S+)""")
_UMGEBUNG = re.compile(r"^\w+=")
_PYTHON = re.compile(r"python[\d.]*w?(?:\.exe)?|py(?:\.exe)?")
_VORSATZ = {"do", "then", "else", "time", "nohup", "sudo", "exec", "command"}   # `for ..; do python x.py`
_HUELLE = {"ssh", "powershell", "powershell.exe", "pwsh", "bash", "sh", "cmd", "cmd.exe"}
_IN_HUELLE = re.compile(r"""["']\s*(?:python[\d.]*w?(?:\.exe)?|py)\s+(?:-\S|\S+\.py\b)""", re.I)   # ssh box "python -c 1"


def ruft_python(cmd):
    """True, wenn ein Teilkommando mit einem Python-Interpreter beginnt (python, python3, py, voller Pfad,
    PowerShell-Aufrufoperator `&`, davor Umgebungsvariablen, `timeout N`, `do`) oder ein ssh/powershell/bash-Aufruf
    ihn direkt nach dem Anfuehrungszeichen startet. `grep python x` oder `cat a.py` zaehlen nicht."""
    for seg in _TRENNER.split(cmd or ""):
        rest = seg
        while True:
            m = _ERSTES.match(rest)
            if not m:
                break
            tok = m.group(1).strip("\"'")
            low = tok.lower()
            rest = rest[m.end():]
            if _UMGEBUNG.match(tok) or low in _VORSATZ:
                continue
            if low == "timeout":   # `timeout 300 python a.py`: die Sekundenangabe ueberspringen
                rest = _ERSTES.sub("", rest, count=1)
                continue
            base = low.replace("\\", "/").rsplit("/", 1)[-1]
            if _PYTHON.fullmatch(base) or (base in _HUELLE and _IN_HUELLE.search(rest)):
                return True
            break
    return False


# --- Zug auswerten und mitschreiben --------------------------------------------------------------
def _norm(s):
    return " ".join(str(s or "").split())


def hinweis_kam(state_dir, sid, prompt):
    """True, wenn rechen_hinweis.py fuer genau diesen Prompt dieser Session einen Treffer ins Log geschrieben hat.
    Der Prompt im Transkript kann Zusatzbloecke vor Max' Text tragen (IDE-Kontext), deshalb Teilstring statt Gleichheit."""
    key, s8 = _norm(prompt), str(sid or "")[:8]
    try:
        with (Path(state_dir) / LOG_NAME).open("rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - TAIL_BYTES))
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return False
    for line in data.splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if "rechen_ohne_code" in r or r.get("sid") != s8:
            continue
        frag = _norm(r.get("prompt"))[:60]
        if frag and frag in key:
            return True
    return False


def _fehler(state_dir, e):
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        with open(state_dir / "hook_errors.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} on_stop.py rechen_zaehler: {e!r}\n")
    except Exception:
        pass


def zaehle(state_dir, sid, lines, last_msg=None):
    """Den letzten Zug des Transkripts auswerten und eine Zeile ins Log haengen.
    -> geschriebene Zeile oder None (keine finale Antwort im Zug). Wirft nie."""
    try:
        state_dir = Path(state_dir)
        t = SZ.turn_info(lines)
        prompt, final = t["prompt"], t["final"]
        if not prompt or not final:   # kein Zug oder Zwischenmeldung (Hintergrund-Agent offen)
            return None
        final = str(last_msg or final)
        py = any(ruft_python(c) for c in t["cmds"])
        nums = zahlen(final)
        # ph: je Prompt-Eintrag eindeutig (uuid), sonst Hash des Textes; gleichlautende Prompts ("ja") fallen so nicht zusammen
        row = {"ts": time.strftime("%Y-%m-%d %H:%M:%S"), "sid": str(sid or "")[:8],
               "ph": hashlib.md5(str(t.get("pid") or prompt).encode("utf-8", "replace")).hexdigest()[:10],
               "prompt": prompt[:120], "hinweis": hinweis_kam(state_dir, sid, prompt),
               "python": py, "agent": bool(t["tools"] & AGENT_TOOLS), "zahlen": len(nums),
               "beleg": belege(final), "rechen_ohne_code": bool(nums) and not py}
        state_dir.mkdir(parents=True, exist_ok=True)
        with open(state_dir / LOG_NAME, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return row
    except Exception as e:
        _fehler(Path(state_dir), e)
        return None
