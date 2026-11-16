"""Selbsttest Korrektur-Reflex: python .claude/scripts/test_korrektur_reflex.py  (Exit 0 = alles gruen)."""
import datetime, sys, tempfile
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
sys.path.insert(0, str(HOOKS))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # Scratchpad-Lauf
import korrektur_reflex as K  # noqa: E402

POSITIV = [
    "das habe ich dir schon gesagt, die FFN Konten sind weg",
    "Die sind weg seit dem 26.10.",
    "du kannst das nicht, NT8 Properties gehen nur per RDP",
    "Hab ich dir doch schon erklärt.",
    "wie schon gesagt, das Konto existiert nicht mehr",
    "die FFN-Konten gibt es nicht mehr",
    "das geht nur per RDP",
    "zum dritten mal: E8 ist funded",
    "du vergisst immer den Stand",
    "die alten Challenges sind längst raus",
]
NEGATIV = [
    "kannst du nicht mal die Tabelle bauen?",
    "prüf bitte, ob FN1 heute getradet hat",
    "baue im Hub einen neuen Tab für die Konten",
    "was steht an?",
    "<pasted_content id=\"x\">Sätze wie „das habe ich dir schon gesagt“, „die sind weg“</pasted_content>",
    "Schreib Sätze wie „du kannst das nicht“ in die Datei",
    "rechne mir den Puffer für FN2 aus",
]
fehler = 0
for p in POSITIV:
    if not K.erkenne(p):
        print("FEHLT  (positiv):", p); fehler += 1
for p in NEGATIV:
    r = K.erkenne(p)
    if r:
        print("FEHLALARM:", p, "->", r); fehler += 1

with tempfile.TemporaryDirectory() as d:
    f = Path(d) / "Stand.md"
    f.write_text(f"# Stand\n\n{K.START}\n{K.ENDE}\nRest\n", encoding="utf-8")
    h = datetime.date(2026, 11, 11)
    n1 = K.sichere(["die FFN Konten sind weg"], f, h)
    n2 = K.sichere(["die FFN Konten sind weg"], f, h)
    t = f.read_text(encoding="utf-8")
    if n1 != ["die FFN Konten sind weg"] or n2 != [] or t.count("FFN Konten sind weg") != 1 or not t.endswith("Rest\n"):
        print("FEHLER sichere/Dublette:", repr(t)); fehler += 1
    K.sichere([f"Satz Nummer {i} ist weg" for i in range(20)], f, h)
    zeilen = [z for z in f.read_text(encoding="utf-8").split(K.START)[1].split(K.ENDE)[0].splitlines() if z.strip()]
    if len(zeilen) != K.MAX_ZEILEN or "Nummer 19" not in zeilen[-1]:
        print("FEHLER Deckel:", len(zeilen)); fehler += 1
    g = Path(d) / "ohne_marker.md"; g.write_text("kein Block\n", encoding="utf-8")
    if K.sichere(["x ist weg"], g, h) or g.read_text(encoding="utf-8") != "kein Block\n":
        print("FEHLER: Datei ohne Marker wurde angefasst"); fehler += 1
    if K.hinweis("Wetter heute?", f) != "":
        print("FEHLER: Hinweis ohne Korrektur"); fehler += 1
    if "KORREKTUR-REFLEX" not in K.hinweis("das hab ich dir schon gesagt, FN1 ist funded", f):
        print("FEHLER: Hinweis fehlt"); fehler += 1

gesamt = len(POSITIV) + len(NEGATIV) + 6
print(f"{gesamt - fehler}/{gesamt} Fälle grün")
sys.exit(1 if fehler else 0)
