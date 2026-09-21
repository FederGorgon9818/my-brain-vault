"""Ausweg-Buchhaltung ueber die Prozess-Quittungen (Max' Vault, 21.09.2026).

Der Typ-Router erlaubt bewusst Ausnahmen: einen Kettenschritt per `--skip` auslassen
oder von einem Gate-Typ auf einen ketten-losen Typ wechseln -- beides nur mit Grund.
Der verdict-auditor hat am Bautag zu Recht angemerkt: "der Grund landet im Retro" war
eine unbelegte Zusage, weil NICHTS die Quittungen je wieder gelesen hat. Ohne Zaehler
merkt niemand, wenn 90 % der Ketten uebersprungen werden -- dann ist der ganze Bau
Theater.

Dieses Skript ist der fehlende Verbraucher. `retro-agent` liest es sonntags, Max kann
es jederzeit aufrufen.

Nutzung (Vault-Root):
    python .claude/scripts/receipt_stats.py [--days 7] [--md]

Alarmschwellen (bewusst konservativ, beim ersten Retro nachjustieren):
    > 30 % der Ketten uebersprungen   -> das Gate passt nicht zur Arbeit, nicht umgekehrt
    > 3 Downgrades in der Woche       -> der Typ-Router trifft die Aufgaben nicht
    ein Agent immer uebersprungen     -> entweder Fehlalarm oder die Kette ist falsch
"""
import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "hooks"))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from _common import STATE  # noqa: E402
import work_types as WT  # noqa: E402

RECEIPTS = STATE / "receipts"


def load_all(days):
    cutoff = time.time() - days * 86400
    out = []
    if not RECEIPTS.is_dir():
        return out
    for p in sorted(RECEIPTS.glob("*.json")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if float(rec.get("created") or 0) >= cutoff:
            out.append(rec)
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="Ausweg-Buchhaltung der Prozess-Quittungen")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--md", action="store_true", help="Markdown-Ausgabe fuer den Retro")
    a = ap.parse_args(argv)

    recs = load_all(a.days)
    P = print
    P(f"# Prozess-Quittungen, letzte {a.days} Tage ({len(recs)} Sessions mit Quittung)\n")
    if not recs:
        P("Keine Quittungen im Zeitraum. Entweder lief nichts, oder der Router greift nicht "
          "(dann: `python .claude/scripts/test_chain.py`).")
        return 0

    typed = [r for r in recs if r.get("type")]
    untyped = len(recs) - len(typed)
    types = Counter(r["type"] for r in typed)
    skips = Counter()
    skip_reasons = []
    downgrades = []
    with_chain = 0
    fully_skipped = 0

    for r in typed:
        chain = [WT.step_name(s) for s in (r.get("chain") or [])]
        sk = r.get("skipped") or {}
        if chain:
            with_chain += 1
            if all(s in sk for s in chain):
                fully_skipped += 1
        for step, info in sk.items():
            skips[step] += 1
            skip_reasons.append((r.get("sid"), step, (info or {}).get("why", "")))
        for d in r.get("downgrades") or []:
            downgrades.append((r.get("sid"), d.get("from"), d.get("to"), d.get("why", "")))

    P("## Auftrags-Typen\n")
    for tid, n in types.most_common():
        P(f"- {tid}: {n}")
    if untyped:
        P(f"- **ohne Typ: {untyped}** (Session hat gearbeitet, Typ nie festgeschrieben)")

    quote = (100.0 * fully_skipped / with_chain) if with_chain else 0.0
    P(f"\n## Ketten\n")
    P(f"- Sessions mit Pflichtkette: {with_chain}")
    P(f"- davon komplett uebersprungen: {fully_skipped} ({quote:.0f} %)")
    if quote > 30:
        P(f"- ⚠️ **ueber der Schwelle (30 %)** — das Gate passt nicht zur Arbeit. "
          f"Entweder Kette kuerzen oder Gate-Bedingung verengen, nicht weiter ausnehmen.")

    if skips:
        P("\n## Uebersprungene Schritte\n")
        for step, n in skips.most_common():
            total = sum(1 for r in typed if step in [WT.step_name(s) for s in (r.get("chain") or [])])
            P(f"- {step}: {n}x uebersprungen (von {total} Ketten, die ihn fordern)")
            if total and n == total:
                P(f"  ⚠️ **immer uebersprungen** — entweder Fehlalarm oder der Schritt "
                  f"gehoert nicht in diese Kette.")
        P("\nBegruendungen:\n")
        for sid, step, why in skip_reasons[-15:]:
            P(f"- `{sid}` {step}: {why}")

    if downgrades:
        P(f"\n## Typwechsel auf ketten-lose Typen ({len(downgrades)})\n")
        for sid, f, t, why in downgrades[-10:]:
            P(f"- `{sid}` {f} -> {t}: {why}")
        if len(downgrades) > 3:
            P("\n⚠️ **mehr als 3** — der Typ-Router trifft die tatsaechlichen Aufgaben nicht. "
              "Typen/Regex in `work_types.py` nachschaerfen.")

    P("\n---\nQuelle: " + str(RECEIPTS))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
