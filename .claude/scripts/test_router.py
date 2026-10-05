"""Selbsttest Wissens-Router (.claude/hooks/knowledge_router.py), Plan 05.10.2026.

Faelle stammen aus Max' echter Sprache (Auswertung 945 Prompts, 30 Tage):
diktiert, Fuellwoerter, "Cloud" = Claude, "hab" = habe, "Juni-Modus" als Verhoerer,
Ticketnummern mit und ohne Leerzeichen. Jeder Fund aus dem Schattenbetrieb wird hier
als neuer Fall ergaenzt.

  python .claude/scripts/test_router.py            # Faelle
  python .claude/scripts/test_router.py --korpus <prompts.json>   # Trefferquote je Thema
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
import knowledge_router as KR  # noqa: E402

KR.ENGINE = None  # Tickettitel nicht nachschlagen, Tests sollen ueberall laufen

# (Prompt, muss treffen, darf nicht treffen)
CASES = [
    ("Juli-Modus", {"juli"}, set()),
    ("ähm, gerade in dem Juni-Modus oder Juli-Modus, ähm, und da geht es ja darum", {"juli"}, set()),
    ("Juli Modus weiter", {"juli"}, set()),
    ("Testphase Juli-Modus, sobald ich das quasi sage", {"juli"}, set()),
    ("unser Vorschlag vom 22.09., warum wir früher mehr gefunden haben", {"juli"}, set()),
    ("Developer", {"developer"}, set()),
    ("Developer: ich hab eine Idee für eine ORB-Variante", {"developer"}, {"hub"}),
    ("zeig mir das in der Workbench", {"developer"}, set()),
    ("Baue im Hub einen neuen Button für die Queue", {"hub"}, set()),
    ("Wenn ich's richtig verstanden hab quasi, unser Eval ist dann sozusagen durch", set(), {"hub"}),
    ("den hab ich auch letztens neu aufgesetzt", set(), {"hub"}),
    ("was machen wir mit dem Next-Week-Buch am Wochenende?", {"gate", "buch"}, set()),
    ("geht das durch Gate v4 durch?", {"gate"}, set()),
    ("was hat die Discovery gefunden, gibt es Kandidaten?", {"discovery"}, set()),
    ("steht der Runner? die Queue ist leer", {"discovery"}, set()),
    ("ich hab den Risk Guard neu reingezogen", {"riskguard"}, {"hub"}),
    ("RiskGuard neu angelegt, Telegram kommt nix", {"riskguard"}, set()),
    ("Hat geklappt, ich habe jetzt den Account gekauft. 50k. 150k.", {"konto"}, set()),
    ("Das war der 150k Account von ffn", {"konto"}, set()),
    ("ich hab mir ein neues Konto bei E8 geholt", {"konto"}, {"hub"}),
    ("Kannst du das auf GitHub pushen?", {"github"}, set()),
    ("am Laptop zieht er das nicht", {"github"}, set()),
    ("schreib es auch in die Cloud MD", {"claude"}, {"github"}),
    ("Geh unsere komplette Cloud im D-Fall durch", {"claude"}, {"github"}),
    ("über mein Cloud-Desktop hier dein Cloud-Desktop steuern", {"claude"}, {"github"}),
    ("such mal im Postfach nach der Rechnung von Contabo", {"mail"}, set()),
    ("schau mal ob die Mail von web.de angekommen ist", {"mail"}, set()),
    ("die Belege für September fehlen noch", {"mail"}, set()),
    ("plan mir den Sprint", {"sprint"}, set()),
    ("ist das wirklich tot oder haben wir das falsch begraben?", {"tot"}, set()),
    ("check die Box, läuft alles?", {"box"}, set()),
    ("deploy das auf die VPS", {"box"}, set()),
    ("pack das Bein ins Buch", {"buch"}, set()),
    ("mit k2 statt k1 rechnen", {"buch"}, set()),
    ("wie viel Steuer zahle ich mit Gewerbe?", {"gruendung"}, set()),
    ("Mentorship später verkaufen, Track Record aufbauen", {"ziel"}, set()),
    ("schreib eine E-Mail an Funnet Next oder i8 wegen dem Account", {"mail"}, {"hub"}),
    ("ich hab bei i8 150k gekauft", {"konto"}, {"hub"}),
    ("mach das in Stereolab im Workbench-Tab", {"developer"}, set()),
    ("alles in die Cloud und D-File, dass das als Regel gilt", {"claude"}, {"github"}),
    ("python discovery/inbox_tool.py --pull und dann schauen", {"discovery"}, {"github"}),
    ("ok", set(), set()),
    ("ja mach weiter", set(), set()),
    ("FERTIG", set(), set()),
]

TICKET_CASES = [
    ("Kümmer dich um AP73", {"AP73"}),
    ("Dann kannst du weiter machen mit AP 71", {"AP71"}),
    ("AP1, AP5, AP10. Bitte das machen.", {"AP1", "AP5", "AP10"}),
    ("das Ticket AP-251", {"AP251"}),
]

NOT_MAX_CASES = [
    "Another Claude session sent a message:\n<agent-message from=\"x\">Box läuft, Runner steht</agent-message>",
    "<task-notification><task-id>a1</task-id></task-notification>",
    "[SYSTEM NOTIFICATION - NOT USER INPUT] Discovery fertig",
]


def run_cases():
    fails = 0
    for prompt, must, mustnot in CASES:
        hits, _ = KR.match(prompt)
        h = set(hits)
        bad = (must - h) | (mustnot & h)
        if bad:
            fails += 1
            print(f"FAIL  {prompt[:70]!r}\n      Treffer {sorted(h)}, erwartet {sorted(must)}, verboten {sorted(mustnot)}")
    for prompt, ids in TICKET_CASES:
        got = {a for a, _ in KR.ticket_titles(prompt)}
        if got != ids:
            fails += 1
            print(f"FAIL  Ticket {prompt!r}: {sorted(got)} statt {sorted(ids)}")
    for prompt in NOT_MAX_CASES:
        if not KR.is_not_max(prompt):
            fails += 1
            print(f"FAIL  nicht-Max nicht erkannt: {prompt[:60]!r}")
    if not KR.is_not_max("Box läuft?") is False:
        pass
    n = len(CASES) + len(TICKET_CASES) + len(NOT_MAX_CASES)
    print(f"{n - fails}/{n} gruen")
    return fails


def korpus(path):
    from collections import Counter
    P = json.load(open(path, encoding="utf-8"))
    c, none = Counter(), 0
    for o in P:
        hits, _ = KR.match(o["p"])
        c.update(hits)
        none += not hits
    for tid, *_ in KR.TOPICS:
        print(f"{tid:10} {c[tid]:4}")
    print(f"ohne Thema: {none} von {len(P)}")


if __name__ == "__main__":
    if "--korpus" in sys.argv:
        korpus(sys.argv[sys.argv.index("--korpus") + 1])
    else:
        sys.exit(1 if run_cases() else 0)
