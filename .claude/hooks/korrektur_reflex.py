"""Korrektur-Reflex (Max, 11.11.2026): korrigiert Max einen Fakt, landet er SOFORT in der Stand-Datei.

Anlass: Max musste "die FFN-Konten sind weg" und "NT8-Properties gehen nur per RDP" mehrfach sagen.
Ein Hinweis im Kontext reicht nicht (die naechste Session vergisst ihn wieder), deshalb schreibt der Hook
den Satz selbst in Kontext/Stand.md (Block KORREKTUREN), der per Import in jeder Session geladen wird.
Claude sortiert die Zeile danach in den richtigen Abschnitt ein und loescht sie dort.

Bewusst eng: nur Saetze, in denen Max sagt, dass etwas schon gesagt wurde, weg/tot ist oder Claude etwas
nicht kann. Eingefuegter Text (<pasted_content>) und Zitate in Anfuehrungszeichen zaehlen nicht, sonst
loest jeder Auftrag, der solche Saetze als Beispiel nennt, den Reflex aus.
Wird von on_prompt.py aufgerufen, wirft nie (Fehler landen in hook_errors.log beim Aufrufer)."""
import datetime
import re
from pathlib import Path

STAND = Path(__file__).resolve().parents[2] / "Kontext" / "Stand.md"
START = "<!-- KORREKTUREN START -->"
ENDE = "<!-- KORREKTUREN ENDE -->"
MAX_ZEILEN = 12

MUSTER = [
    r"\b(hab|habe|hatte)\s+ich\s+(dir|euch)?\s*(doch|schon|bereits|eben|gerade|vorhin|mehrfach|\s)*\s*(gesagt|erkl[aä]rt|geschrieben|erw[aä]hnt)",
    r"\bwie\s+(ich\s+)?(schon|bereits)\s+(gesagt|geschrieben|erkl[aä]rt)",
    r"\b(zum\s+(zweiten|dritten|x-?ten|hundertsten)\s+mal)\b",
    r"\b(sind|ist)\s+(doch\s+|schon\s+|l[aä]ngst\s+|seit\s+\S+\s+|eh\s+|alle\s+)*(weg|tot|geschlossen|gek[uü]ndigt|gel[oö]scht|verloren|raus)\b",
    r"\bexistier(t|en)\s+(doch\s+)?nicht\s+mehr\b",
    r"\bgibt\s+es\s+(doch\s+)?nicht\s+mehr\b",
    r"\bdu\s+kannst\s+(das|die|den|es|dort|da)?\s*(doch\s+|eh\s+|gar\s+|ja\s+)*nicht\b",
    r"\bdas\s+(geht|kannst\s+du)\s+(nur|bloß)\s+(per|über|mit)\b",
    r"\b(vergisst|vergesst)\s+(du\s+)?(immer|st[aä]ndig|schon\s+wieder|jedes\s+mal)",
]
_RX = [re.compile(m, re.I) for m in MUSTER]
_PASTE = re.compile(r"<pasted_content[^>]*>.*?</pasted_content[^>]*>", re.S | re.I)
_ZITAT = re.compile(r"[„\"“»][^„\"“”»«]{0,200}[“”\"«]")


def bereinigen(text):
    text = _PASTE.sub(" ", text or "")
    return _ZITAT.sub(" ", text)


def erkenne(prompt):
    """Saetze aus Max' eigenem Text, die eine Korrektur sind. Reihenfolge wie im Text, ohne Dubletten."""
    out = []
    for satz in re.split(r"(?<=[.!?])\s+|\n+", bereinigen(prompt)):
        s = " ".join(satz.split()).strip(" -–•>▎")
        if len(s) < 8:
            continue
        if any(r.search(s) for r in _RX) and s not in out:
            out.append(s[:220])
    return out


def sichere(saetze, pfad=STAND, heute=None):
    """Haengt neue Saetze an den KORREKTUREN-Block. -> Liste der wirklich neu geschriebenen Saetze."""
    if not saetze or not pfad.exists():
        return []
    alt = pfad.read_text(encoding="utf-8")
    if START not in alt or ENDE not in alt:
        return []
    a, e = alt.index(START) + len(START), alt.index(ENDE)
    zeilen = [z for z in alt[a:e].strip("\n").splitlines() if z.strip()]
    tag = (heute or datetime.date.today()).strftime("%d.%m.%Y")
    neu = [s for s in saetze if not any(s in z for z in zeilen)]
    if not neu:
        return []
    zeilen += [f"- {tag}: „{s}“ (noch einsortieren)" for s in neu]
    zeilen = zeilen[-MAX_ZEILEN:]
    text = alt[:a] + "\n" + "\n".join(zeilen) + "\n" + alt[e:]
    tmp = pfad.with_suffix(".korr.tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(pfad)
    return neu


def hinweis(prompt, pfad=STAND):
    """Fuer on_prompt.py: erkennen, sichern, Kontext-Hinweis zurueck ('' wenn nichts)."""
    saetze = erkenne(prompt)
    if not saetze:
        return ""
    neu = sichere(saetze, pfad)
    gesichert = "schon in Kontext/Stand.md (Abschnitt Korrekturen) gesichert" if neu else "stand schon im Korrektur-Block"
    return ("KORREKTUR-REFLEX: Max korrigiert einen Fakt: " + " | ".join(f"„{s}“" for s in saetze) +
            f". Der Satz ist {gesichert}. Jetzt: (1) die Aussage ernst nehmen und nicht nochmal nachfragen, "
            "(2) sie in den passenden Abschnitt der Stand-Datei (Konten, Tot, Kann/Kann nicht, Offen) oder als "
            "Memory-Eintrag einsortieren, (3) die Zeile im Korrektur-Block löschen und Max in einem Satz sagen, wo es steht. "
            "War es keine Korrektur (Fehlalarm), nur die Zeile löschen.")
