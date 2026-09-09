#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statusline fuer Claude Code: zeigt live, wie viel Kontingent noch da ist.

Quelle der Wahrheit ist diese Datei im Vault (versioniert). Die aktive Kopie
liegt unter ~/.claude/statusline.py, darauf zeigt der statusLine-Eintrag in
~/.claude/settings.json (user-weit, gilt also in jedem Projekt).

Datenquelle ist ausschliesslich das stdin-JSON von Claude Code, keine Logs und
keine Schaetzung: context_window kommt aus der letzten API-Antwort, rate_limits
liefert die echten Prozentwerte von Anthropic (nur Pro/Max, erst ab der ersten
API-Antwort der Session, jedes Fenster kann einzeln fehlen).

Sync auf ein anderes Geraet:
    cp .claude/statusline.py ~/.claude/statusline.py
"""

import io
import json
import sys
import time

# UTF-8 hart erzwingen. Ohne das zerlegt die Windows-Konsolen-Codepage die
# Balken- und Trennzeichen und der Reader stolpert ueber Umlaute im Payload
# (dieselbe Falle wie bei den Hooks, 09.09.2026).
try:
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", errors="replace")
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"

SEP = DIM + " | " + RESET
FULL = "\u2588"   # Vollblock
EMPTY = "\u2591"  # Schattenblock


def ampel(frei_pct):
    """Farbe nach verbleibendem Anteil, nicht nach verbrauchtem."""
    if frei_pct is None:
        return DIM
    if frei_pct >= 40:
        return GREEN
    if frei_pct >= 15:
        return YELLOW
    return RED


def balken(frei_pct, breite=8):
    if frei_pct is None:
        return DIM + EMPTY * breite + RESET
    voll = max(0, min(breite, int(round(frei_pct / 100.0 * breite))))
    return ampel(frei_pct) + FULL * voll + DIM + EMPTY * (breite - voll) + RESET


def restzeit(resets_at):
    """Epoch-Sekunden -> '2h14m' / '38m' / '3d 4h'. None wenn unbekannt."""
    if not resets_at:
        return None
    sek = int(resets_at) - int(time.time())
    if sek <= 0:
        return "gleich"
    tage, rest = divmod(sek, 86400)
    std, rest = divmod(rest, 3600)
    minuten = rest // 60
    if tage:
        return "%dd %dh" % (tage, std)
    if std:
        return "%dh%02dm" % (std, minuten)
    return "%dm" % minuten


def kurz_tok(n):
    """Tokenzahl kurz: 124k, 1.0M."""
    n = int(n or 0)
    if n >= 1000000:
        return "%.1fM" % (n / 1000000.0)
    return "%dk" % round(n / 1000.0)


def fenster(daten, name, kurz):
    """Ein Rate-Limit-Fenster als '5h ####.... 77% frei 2h14m'."""
    block = (daten or {}).get(name) or {}
    used = block.get("used_percentage")
    if used is None:
        return DIM + kurz + " k.A." + RESET
    frei = max(0.0, 100.0 - float(used))
    teile = ["%s%s%s %s %s%d%% frei%s" % (DIM, kurz, RESET, balken(frei), ampel(frei), round(frei), RESET)]
    rest = restzeit(block.get("resets_at"))
    if rest:
        teile.append(DIM + rest + RESET)
    return " ".join(teile)


def main():
    roh = sys.stdin.read()
    d = json.loads(roh) if roh.strip() else {}

    stuecke = []

    modell = ((d.get("model") or {}).get("display_name") or "").strip()
    if modell:
        stuecke.append(BOLD + CYAN + modell + RESET)

    # Kontextfenster der laufenden Session
    ctx = d.get("context_window") or {}
    ctx_frei = ctx.get("remaining_percentage")
    if ctx_frei is None and ctx.get("used_percentage") is not None:
        ctx_frei = 100.0 - float(ctx["used_percentage"])
    if ctx_frei is None:
        stuecke.append(DIM + "ctx k.A." + RESET)
    else:
        groesse = ctx.get("context_window_size") or 0
        drin = ctx.get("total_input_tokens") or 0
        label = "ctx %s%d%% frei%s" % (ampel(ctx_frei), round(ctx_frei), RESET)
        if groesse:
            label += DIM + " (%s/%s)" % (kurz_tok(drin), kurz_tok(groesse)) + RESET
        stuecke.append(label)

    # Kontingent: die eigentliche Frage "wie viel hab ich noch"
    limits = d.get("rate_limits") or {}
    stuecke.append(fenster(limits, "five_hour", "5h"))
    stuecke.append(fenster(limits, "seven_day", "7d"))

    kosten = (d.get("cost") or {}).get("total_cost_usd")
    if kosten:
        stuecke.append(DIM + "$%.2f" % kosten + RESET)

    sys.stdout.write(SEP.join(stuecke))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Eine kaputte Statusline darf nie die Arbeit stoeren: lieber eine
        # stille Kurzmeldung als ein roter Fehlerblock unter dem Prompt.
        try:
            sys.stdout.write(DIM + "statusline: " + str(e)[:60] + RESET)
        except Exception:
            pass
