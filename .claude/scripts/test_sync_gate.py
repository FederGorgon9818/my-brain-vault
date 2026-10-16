"""Selbsttest AP398 (15.10.2026): Box-Sync-Sperre in guard_bash.py fuer Bash UND PowerShell.

Prueft:
  1. Sync-Start ohne frischen regression_ok wird geblockt, egal ob Bash-Tool (powershell -File ...)
     oder PowerShell-Tool (& / .\\ / Backtick-Fortsetzung).
  2. Kein Fehlalarm mehr auf Text, der das Skript nur ERWAEHNT (Ticket-Text mit "Teil-Sync" vom
     15.10., grep, Get-Content), und Trockenlauf / Testziel (-RemoteBase woanders) sind frei.
  3. Mit frischem regression_ok laeuft der Sync durch, -Stop sowieso.
  4. Die Bash-Regeln 2-4 greifen im PowerShell-Tool (noch) nicht (Rest von AP362).
  5. settings.json meldet guard_bash.py fuer Bash UND PowerShell an.
  6. Kaputte Eingabe blockiert nie.

Laeuft gegen einen Wegwerf-Engine-Ordner (MAXLAB_ENGINE), fasst nichts Echtes an.

    python .claude/scripts/test_sync_gate.py
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
HOOK = VAULT / ".claude" / "hooks" / "guard_bash.py"
ENG = Path(tempfile.mkdtemp(prefix="hook_sync_"))
(ENG / "discovery").mkdir()
STATE = ENG / ".claude_hooks"
STATE.mkdir()
fails = []

SCRIPT_W = r"C:\Users\maxlk\Projects\trading-data\engine\discovery\box_provision_discovery.ps1"
SCRIPT_U = "/c/Users/maxlk/Projects/trading-data/engine/discovery/box_provision_discovery.ps1"


def check(name, cond, info=""):
    print(("OK   " if cond else "FAIL ") + name + (f"  [{info}]" if info and not cond else ""))
    if not cond:
        fails.append(name)


def hook(tool, command):
    env = dict(os.environ, MAXLAB_ENGINE=str(ENG), PYTHONIOENCODING="utf-8")
    payload = {"tool_name": tool, "tool_input": {"command": command}} if tool else command
    raw = payload if isinstance(payload, str) else json.dumps(payload)
    p = subprocess.run([sys.executable, str(HOOK)], input=raw, capture_output=True, text=True,
                       encoding="utf-8", env=env, timeout=30)
    try:
        out = json.loads(p.stdout) if p.stdout.strip() else {}
    except Exception:
        out = {"_raw": p.stdout}
    hs = out.get("hookSpecificOutput") or {}
    return hs.get("permissionDecision") == "deny", hs, p


def arm(fresh_ok):
    """Kern-Datei jetzt geaendert; regression_ok davor (Sperre scharf) oder danach (frei)."""
    core = ENG / "qbt.py"
    core.write_text("# kern\n", encoding="utf-8")
    t = time.time() - 60
    os.utime(core, (t, t))
    mk = STATE / "regression_ok"
    mk.touch()
    tm = t + 30 if fresh_ok else t - 3600
    os.utime(mk, (tm, tm))


print("== 1. Sperre scharf: echter Sync-Start wird geblockt ==")
arm(fresh_ok=False)
blocked = [
    ("Bash", f"powershell -NoProfile -ExecutionPolicy Bypass -File {SCRIPT_W} -SyncOnly"),
    ("Bash", f"cd /c/x && powershell.exe -File {SCRIPT_U} -SyncOnly 2>&1 | tail -20"),
    ("Bash", f"pwsh -File '{SCRIPT_W}' -SyncOnly"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly"),
    ("PowerShell", f"& \"{SCRIPT_W}\" -SyncOnly *>&1 | Out-File C:\\tmp\\sync.txt"),
    ("PowerShell", "Set-Location C:\\Users\\maxlk\\Projects\\trading-data\\engine\\discovery; .\\box_provision_discovery.ps1 -SyncOnly"),
    ("PowerShell", f"& {SCRIPT_W} `\n    -SyncOnly"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -RemoteBase C:\\Users\\maxlk\\Projects\\trading-data"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -Force"),
    ("Bash", f"powershell -File {SCRIPT_W} -Sync"),
    # verdict-auditor 16.10.: diese zehn kamen bei der ersten Fassung frei durch
    ("Bash", f"powershell -File {SCRIPT_W}"),                         # Vollmodus: synct UND startet den Runner
    ("PowerShell", f"& {SCRIPT_W}"),
    ("Bash", f"time powershell -File {SCRIPT_W} -SyncOnly"),
    ("Bash", f"timeout 900 powershell -File {SCRIPT_W} -SyncOnly"),
    ("Bash", f"MSYS_NO_PATHCONV=1 powershell -File {SCRIPT_W} -SyncOnly"),
    ("Bash", f"(powershell -File {SCRIPT_W} -SyncOnly)"),
    ("PowerShell", f"Measure-Command {{ & {SCRIPT_W} -SyncOnly }}"),
    ("PowerShell", f"$p = '{SCRIPT_W}'; & $p -SyncOnly"),
    ("PowerShell", f"Start-Job {{ & {SCRIPT_W} -SyncOnly }}"),
    ("PowerShell", f"& {SCRIPT_W} -Sy"),
    # weitere Startwege
    ("PowerShell", f"Start-Process powershell -ArgumentList \"-File {SCRIPT_W} -SyncOnly\" -Wait"),
    ("PowerShell", f"powershell -NoProfile -Command \"& '{SCRIPT_W}' -SyncOnly\""),
    ("PowerShell", f"if ($?) {{ & {SCRIPT_W} -SyncOnly }}"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -WithScratch"),
]
for tool, cmd in blocked:
    d, hs, p = hook(tool, cmd)
    check(f"{tool}: geblockt  {cmd[:70]!r}", d, (hs or p.stderr)[:200] if not d else "")
    if d:
        check("  Grund nennt engine-regression-tester", "engine-regression-tester" in hs.get("permissionDecisionReason", ""))

print("\n== 2. Kein Fehlalarm, Trockenlauf und Testziel frei ==")
free = [
    # Fehlalarm vom 15.10.: Skriptname + "Teil-Sync" im Ticket-Text
    ("Bash", "python ticket_tool.py new --why \"aus Git Bash nimmt box_provision_discovery.ps1 /usr/bin/scp\" "
             "\"Box-Sync haerten: Git-Bash-scp, Teil-Sync ohne Stempel\""),
    ("Bash", f"grep -n SyncOnly {SCRIPT_U}"),
    ("Bash", f"sed -n 1,40p {SCRIPT_U} | grep -i sync"),
    ("PowerShell", f"Get-Content {SCRIPT_W} | Select-String -Pattern '-SyncOnly'"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -DryRun"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -RemoteBase C:\\Users\\Administrator\\sync_test\\trading-data"),
    ("Bash", f"powershell -File {SCRIPT_W} -SyncOnly -DryRun"),
    ("PowerShell", f"& {SCRIPT_W} -Stop"),
    ("PowerShell", "Write-Host 'vor dem box_provision_discovery.ps1 -SyncOnly erst den Regressionstest'"),
    # Praefix-Kuerzungen der freien Schalter
    ("PowerShell", f"& {SCRIPT_W} -St"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -Dr"),
    ("PowerShell", f"& {SCRIPT_W} -SyncOnly -R C:\\Users\\Administrator\\sync_test\\trading-data"),
    # Lesen/Pruefen des Skripts in allen Formen, die am 15./16.10. wirklich vorkamen
    ("PowerShell", f"powershell -NoProfile -Command \"Get-Content {SCRIPT_W} | Select-String Sync\""),
    ("PowerShell", f"foreach ($f in \"{SCRIPT_W}\",\"C:\\x\\start_runner.ps1\") {{ $t=$null; $e=$null; "
                   f"[void][System.Management.Automation.Language.Parser]::ParseFile($f, [ref]$t, [ref]$e) }}"),
    ("PowerShell", f"[void][System.Management.Automation.Language.Parser]::ParseFile('{SCRIPT_W}', [ref]$t, [ref]$e)"),
    ("PowerShell", f"$s = '{SCRIPT_W}'; Get-Content $s -Raw"),
    ("PowerShell", f"$src = Get-Content \"{SCRIPT_W}\" -Raw"),
    ("Bash", f"cp -p {SCRIPT_U} {SCRIPT_U}.bak-20261016"),
    ("Bash", f"python - <<'EOF'\np=r'{SCRIPT_W}'\ns=open(p).read()\nEOF"),
]
for tool, cmd in free:
    d, hs, p = hook(tool, cmd)
    check(f"{tool}: frei  {cmd[:70]!r}", not d, hs.get("permissionDecisionReason", "")[:160])

print("\n== 3. Frische Freigabe: Sync laeuft durch ==")
arm(fresh_ok=True)
for tool, cmd in [("Bash", f"powershell -File {SCRIPT_W} -SyncOnly"), ("PowerShell", f"& {SCRIPT_W} -SyncOnly")]:
    d, hs, p = hook(tool, cmd)
    check(f"{tool}: frei mit regression_ok", not d, hs.get("permissionDecisionReason", "")[:160])
    check(f"{tool}: Hinweis Stop/Sync/Start kommt", "Runner neu starten" in hs.get("additionalContext", ""), str(hs)[:160])

print("\n== 4. Bash-Regeln 2-4 im PowerShell-Tool (noch) aus, im Bash-Tool an ==")
d, _, _ = hook("PowerShell", "Get-Content C:\\x\\discovery\\runner.log")
check("PowerShell: Get-Content runner.log wird (noch) nicht geblockt", not d)
d, _, _ = hook("Bash", "cat /c/x/discovery/runner.log")
check("Bash: cat runner.log bleibt geblockt", d)

print("\n== 5. Matcher in settings.json ==")
try:
    st = json.loads((VAULT / ".claude" / "settings.json").read_text(encoding="utf-8"))
    ms = [h.get("matcher", "") for h in st["hooks"]["PreToolUse"]
          if any("guard_bash.py" in x.get("command", "") for x in h.get("hooks", []))]
    check("guard_bash.py fuer Bash UND PowerShell angemeldet",
          any({"Bash", "PowerShell"} <= set(m.split("|")) for m in ms), str(ms))
except Exception as e:
    check("settings.json lesbar", False, repr(e))

print("\n== 6. Kaputte Eingabe blockiert nie ==")
for raw in ["", "{kaputt", json.dumps({"tool_name": "PowerShell"}), json.dumps({"tool_input": None})]:
    d, hs, p = hook(None, raw)
    check(f"Eingabe {raw[:20]!r}: kein Block, kein Traceback", not d and "Traceback" not in p.stderr, p.stderr[:160])

print()
print("ALLES OK" if not fails else f"{len(fails)} FEHLER: {fails}")
sys.exit(1 if fails else 0)
