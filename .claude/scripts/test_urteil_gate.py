import re
import sys
from pathlib import Path

VAULT = Path(r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain")
sys.path.insert(0, str(VAULT / ".claude" / "hooks"))

# guard_chain ruft am Modulende `run(main)` auf -- beim Import wuerde der Hook also
# sofort laufen und sich beenden. Deshalb Quelltext laden, die letzte Zeile kappen
# und in einen eigenen Namensraum ausfuehren.
_src = (VAULT / ".claude" / "hooks" / "guard_chain.py").read_text(encoding="utf-8")
_src = re.sub(r"^run\(main\)\s*$", "", _src, flags=re.M)


class _NS:
    pass


G = _NS()
G.__dict__["__file__"] = str(VAULT / ".claude" / "hooks" / "guard_chain.py")
G.__dict__["__name__"] = "guard_chain_test"
exec(compile(_src, "guard_chain.py", "exec"), G.__dict__)

FAELLE = [
    ("1 Todesurteil nackt -> MUSS blocken", True, """
## #172 -- Fibonacci-Retracement auf NQ

Gerechnet ueber 2.400 Tage, 18 Varianten.

**Verdikt:** tot. Keine Variante schlaegt den Placebo.
"""),
    ("2 Todesurteil mit allen Feldern -> durch", False, """
## #172 -- Fibonacci-Retracement auf NQ

**Verdikt:** tot als Entry-Signal.
Reichweite: als Richtungssignal auf NQ/ES bei 15-Min-Frequenz unter MNQ-Kosten. Rollen
Filter und Sizing nicht getestet.
KATEGORIE: empirisch-nichts-gefunden (18 Varianten)
Wiedervorlage: wenn die Kostenstruktur unter 0,5 Pkt Round-Turn faellt.
Stempel: Engine b4c263ff, Daten bis 2026-09-19, Kriterium E[Zeit bis 50k], k=3.
"""),
    ("3 Rueckblick zitiert fremdes Urteil -> KEIN Fehlalarm", False, """
## #173 -- Lehre 28 korrigiert

Die alte Fassung nannte den ORB-Fade tot und berief sich auf +109 %. Das war falsch:
der Eintrag #075 nennt fuer dieselbe Sache +36 %. Im Friedhof liegt damit Zeug, das
mit kaputtem Lineal erschlagen wurde.

**Verdikt:** Lehre 28 ersetzt, Guard in qbt.py gebaut.
"""),
    ("4 Prozess-/Werkzeugeintrag -> KEIN Fehlalarm", False, """
## #174 -- Queue lief 26 h leer

Der Generator war ausgereizt, der Runner hat es nicht gemeldet.

**Verdikt:** Generator-Vorlagen erschoepft, alpha-scout eingeschaltet.
"""),
    ("5 strukturell-tot ohne zitierte Rechnung -> MUSS Beleg fordern", True, """
## #175 -- RVOL als Richtungssignal

**Verdikt:** tot.
Reichweite: alle Frequenzen, alle Order-Arten, NQ und ES.
KATEGORIE: strukturell-tot
Wiedervorlage: nur auf ausdrueckliche Ansage.
Stempel: Engine b4c263ff, Daten bis 2026-09-19, Kriterium E[Zeit bis 50k].
"""),
    ("6 strukturell-tot MIT Rechnung -> durch", False, """
## #176 -- RVOL als Richtungssignal

**Verdikt:** tot.
Reichweite: als Richtungssignal, alle Frequenzen und Order-Arten, NQ und ES.
KATEGORIE: strukturell-tot
Beleg: die Huellkurve ueber alle Frequenzen liegt bei max 0,19 Sharpe gegen einen
Nachweisboden von 0,86; die Kostenhuerde von 1,01 Pkt schlaegt die 0,447 Pkt Bruttoedge.
Wiedervorlage: nur auf ausdrueckliche Ansage.
Stempel: Engine b4c263ff, Daten bis 2026-09-19, Kriterium E[Zeit bis 50k], k=3.
"""),
    ("7 gar kein Urteilsblock -> KEIN Fehlalarm", False, """
## #177 -- Datenimport GC/CL

Zehn Jahre 1m-Historie ueber NT8 geholt. Alte Ideen sind damit nicht mehr tot,
weil die Maerkte jetzt da sind.
"""),
]

fehler = 0
for name, soll_blocken, text in FAELLE:
    fehlt = G._urteil_felder_fehlen(text)
    blockt = bool(fehlt)
    ok = blockt == soll_blocken
    fehler += (not ok)
    print(f"[{'OK ' if ok else 'FAIL'}] {name}")
    if fehlt:
        for f in fehlt:
            print("          fehlt:", f[:88])

print()
print("Alle Faelle bestanden." if not fehler else f"{fehler} FEHLER")
sys.exit(1 if fehler else 0)
