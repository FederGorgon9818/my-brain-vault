"""Selbsttest Konto-Gate und Einschalt-Regel konto-analyst (Regel Max, 13.10.2026).

Prueft drei Dinge, jeweils mit Treffern UND mit den Fehlalarm-Quellen:
  1. agent_triggers.py: der Prompt-Hook erkennt Konto-Fragen (und laesst Unbeteiligtes durch).
  2. guard_chain.py KONTO_FILE: Edit/Write auf Host-JSON oder RiskGuard-cfg eines Kontos.
  3. guard_chain.py KONTO_CMD: Bash, das solche Dateien schreibt oder auf die Box kopiert --
     reines Lesen (Get-ChildItem, cat, account_sync) darf NICHT treffen.

    python .claude/scripts/test_konto_gate.py
"""
import re
import sys
from pathlib import Path

VAULT = Path(r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain")
sys.path.insert(0, str(VAULT / ".claude" / "hooks"))

# guard_chain ruft am Modulende `run(main)` auf -- Quelltext laden, letzte Zeile kappen
# (gleiches Verfahren wie test_urteil_gate.py).
_src = (VAULT / ".claude" / "hooks" / "guard_chain.py").read_text(encoding="utf-8")
_src = re.sub(r"^run\(main\)\s*$", "", _src, flags=re.M)
G = {"__file__": str(VAULT / ".claude" / "hooks" / "guard_chain.py"), "__name__": "guard_chain_test"}
exec(compile(_src, "guard_chain.py", "exec"), G)

import agent_triggers as A  # noqa: E402

_rows = [t for t in A.TRIGGERS if t[0] == "konto"]
assert len(_rows) == 1, "genau eine Trigger-Zeile `konto` erwartet"
TRIGGER = _rows[0][3]

PROMPTS = [
    (True, "wie steht ffn2 gerade"),
    (True, "wie stehen die konten"),
    (True, "zeig mir die konto-karten"),
    (True, "darf ffn1 schon auf k2"),
    (True, "was bringt pb3 auf ffn2"),
    (True, "sollen wir fn1 hochstufen"),
    (True, "ffn2 bekommt jetzt auch das bein nachgezogen"),
    (True, "lohnt sich das e8 50k noch"),
    (True, "wie viel puffer hat das konto noch bis zum drawdown"),
    (True, "k2 auf dem 150k-konto, ja oder nein"),
    (True, "ist die inaktivität bei ffn1 ein problem"),
    (True, "rechne mir mal pro konto durch was passiert"),
    (False, "mein kontostand bei der sparkasse"),
    (False, "baue im hub ein fenster"),
    (False, "mach den datentag-test auf gold"),
    (False, "was hat die discovery gefunden"),
    (False, "leg ein ticket fuer den export an"),
    (False, "schreib die daily note"),
]

FILES = [
    (True, "c:/users/maxlk/projects/trading-data/nt8_staging_20261003_host/maxlab_book_host.live_ffn150k_2.json"),
    (True, "c:/users/maxlk/projects/trading-data/x/maxlab_riskguard.cfg"),
    (True, "c:/users/maxlk/projects/trading-data/nt8_staging/cfg_vorlage_ffn_150k.txt"),
    (False, "c:/users/maxlk/projects/trading-data/nt8_staging_20261003_host/maxlab_book_host.sim.json"),
    (False, "c:/users/maxlk/projects/trading-data/nt8_staging_20261003_host/maxlab_book_host.example.json"),
    (False, "c:/users/maxlk/projects/trading-data/engine/konten/accounts.json"),
    (False, "c:/users/maxlk/projects/trading-data/engine/book_state.json"),
]

CMDS = [
    (True, "scp nt8_staging/maxlab_book_host.live_ffn150k_2.json administrator@100.127.89.9:'c:/users/administrator/documents/ninjatrader 8/'"),
    (True, "ssh box \"powershell copy-item c:/tmp/maxlab_riskguard.cfg 'c:/users/administrator/documents/ninjatrader 8/maxlab_riskguard.cfg'\""),
    (True, "echo 'x.fixedqty=2' >> maxlab_riskguard.cfg"),
    (True, "cp /tmp/neu.json nt8_staging/maxlab_book_host.live_fn1.json"),
    (False, "ssh box \"powershell get-childitem maxlab_book_host*.json\""),
    (False, "cat nt8_staging/maxlab_book_host.live_ffn150k.json | head -20"),
    (False, "python -m konten.account_sync --check"),
    (False, "md5sum nt8_staging/maxlab_book_host.live_ffn150k.json"),
    (False, "ssh box \"powershell select-string -path maxlab_riskguard.cfg -pattern 394206\""),
    (False, "diff a/maxlab_book_host.live_ffn150k.json b/maxlab_book_host.live_ffn150k_2.json"),
    # Kanarien aus dem verdict-auditor (13.10.2026): die echten Wege, an denen die erste Fassung vorbeisah
    (True, "L=c:/x/nt8_staging_20261003_host; for t in e8_50k fn1 fn2; do f=maxlab_book_host.live_$t.json; scp -q \"$L/$f\" \"administrator@100.127.89.9:c:/users/administrator/documents/ninjatrader 8/\"; done"),
    (True, "ssh administrator@100.127.89.9 \"powershell -noprofile -file c:/users/administrator/ffn_cfg_einspielen.ps1 -konto 2d-150k394206247048\""),
    (True, "scp -r c:/x/nt8_staging_20261011_rtygap_live \"administrator@100.127.89.9:c:/users/administrator/documents/ninjatrader 8/\""),
    (True, "sed -i 's/qty.: 1/qty.: 2/' nt8_staging_20261003_host/maxlab_book_host.live_ffn150k.json"),
    (True, "ssh box \"powershell -command add-content 'c:/x/maxlab_riskguard.cfg' 'k.fixedqty=2'\""),
    (False, "scp -q \"administrator@100.127.89.9:c:/users/administrator/documents/ninjatrader 8/maxlab_book_host.live_ffn150k.json\" \"$temp/scratch/box_ffn150k.json\""),
    (False, "ssh box \"type c:/x/maxlab_riskguard.cfg\" > \"$temp/scratch/box_maxlab_riskguard.cfg\""),
    (False, "cp nt8_staging/maxlab_riskguard.cfg \"$temp/scratch/rg.bak\""),
    (False, "python ticket_tool.py note ap338 \"per scp maxlab_book_host.live_ffn150k_rtygap.json auf die box gelegt\""),
]

# Die Sperre muss auch fuer das PowerShell-Tool gelten (11.10.2026 lief der FFN1-Deploy darueber).
assert "PowerShell" in G["SHELL_TOOLS"], "SHELL_TOOLS ohne PowerShell"
PROMPTS += [
    (True, "mach deine empfehlung zu rty-gap mit auf die 150k konten"),
    (True, "ok mach den deploy, erst nur ffn1"),
    (True, "auf die 150k ffn-accounts auch drauf spielen"),
    (True, "einspielen auf einem der beiden ffn accounts und dann nachziehen"),
    (True, "was machen wir mit dem 150k konto?"),
    (True, "was fuer einen k wir jetzt nehmen, also k1 oder k2"),
    (False, "hat e8 auf die mail geantwortet"),
    (False, "ffn support hat geschrieben, lies die mail"),
]

fail = 0


def check(name, soll, ist, text):
    global fail
    ok = bool(ist) == soll
    if not ok:
        fail += 1
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: {'trifft' if ist else 'trifft nicht'} | {text[:90]}")


print("1. Einschalt-Regel (Prompt-Hook)")
for soll, p in PROMPTS:
    check("Prompt", soll, re.search(TRIGGER, p, re.I), p)
print("2. Konto-Datei (Edit/Write)")
for soll, f in FILES:
    check("Datei", soll, re.search(G["KONTO_FILE"], f), f)
print("3. Konto-Kommando (Bash)")
for soll, c in CMDS:
    check("Bash", soll, G["_konto_write"](c), c)

print(f"\nERGEBNIS: {'alles gruen' if not fail else str(fail) + ' FAIL'} "
      f"({len(PROMPTS) + len(FILES) + len(CMDS)} Faelle)")
sys.exit(1 if fail else 0)
