"""Selbsttest fuer den Typ-Router: work_types, receipt, guard_chain, on_prompt, on_stop."""
import json
import subprocess
import sys
from pathlib import Path

VAULT = Path(r"C:\Users\maxlk\Documents\Obsidaian\My Brain\My Brain")
# Die Hooks neben diesem Skript, nicht fest die des Vaults: so prueft eine Kopie des
# .claude-Ordners (Staging) ihre EIGENEN Hooks. VAULT bleibt fest, weil die Testpfade
# echte Vault-Pfade sein muessen -- unter Temp/ griffe sonst die Freiliste.
HOOKS = Path(__file__).resolve().parents[1] / "hooks"
SID = "testsess-0000-0000-0000-000000000001"

ok = fail = 0


def check(name, cond, extra=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  OK   {name}")
    else:
        fail += 1
        print(f"  FAIL {name} {extra}")


def hook(script, payload):
    p = subprocess.run([sys.executable, str(HOOKS / script)],
                       input=json.dumps(payload), capture_output=True, text=True,
                       encoding="utf-8", cwd=str(VAULT))
    try:
        return json.loads(p.stdout) if p.stdout.strip() else {}, p.stderr
    except Exception:
        return {"_raw": p.stdout}, p.stderr


def decision(res):
    return (res.get("hookSpecificOutput") or {}).get("permissionDecision")


def clear_stop_memory(sid):
    """on_stop blockt je Befund und Session nur EINMAL (SEEN_DIR). Fuer einen
    wiederholbaren Test muss dieses Gedaechtnis vorher weg."""
    import hashlib
    import tempfile
    f = Path(tempfile.gettempdir()) / "claude_stop_blocks" / (hashlib.md5(sid.encode()).hexdigest() + ".json")
    f.unlink(missing_ok=True)


def cli(*args):
    p = subprocess.run([sys.executable, str(HOOKS / "receipt.py"), *args],
                       capture_output=True, text=True, encoding="utf-8", cwd=str(VAULT))
    return p.stdout + p.stderr


print("\n== 1. work_types ==")
sys.path.insert(0, str(HOOKS))
import work_types as WT
check("14 Typen geladen", len(WT.TYPES) == 14, f"({len(WT.TYPES)})")
check("jeder Typ hat what", all(t["what"] for t in WT.TYPES))
s = [t for t, _ in WT.suggest("Baue im Hub einen Button und rechne die Passquote aus")]
check("suggest findet ui+rechnen", "ui" in s and "rechnen" in s, s)
check("suggest leer bei Geplauder", not WT.suggest("moin wie gehts"))
check("Kette buch = 3 Schritte", len(WT.chain_of("buch")) == 3)
check("wf-Schritt erkannt", WT.step_is_workflow("wf:ein-weg") and WT.step_name("wf:ein-weg") == "ein-weg")

print("\n== 2. receipt CLI ==")
import receipt as R
p = R.path_for(SID)
if p.is_file():
    p.unlink()
out = cli("--types")
check("--types listet Typen", "rechnen" in out and "logbuch" in out)
R.ensure(SID, prompt_hint="testprompt")
out = cli("--sid", R.sid8(SID), "--type", "rechnen")
check("Typ setzen", "rechnen" in out and "quant-mathematician" in out, out[:120])
out = cli("--sid", R.sid8(SID), "--type", "quatsch")
check("unbekannter Typ abgelehnt", "Unbekannter Typ" in out)
out = cli("--sid", R.sid8(SID), "--skip", "quant-statistician", "--why", "x")
check("Ausnahme ohne echten Grund abgelehnt", "braucht einen Grund" in out, out[:100])
out = cli("--sid", R.sid8(SID), "--skip", "quant-statistician", "--why", "reine Plausibilitaetsrechnung ohne Edge-Anspruch")
check("Ausnahme mit Grund akzeptiert", "Ausnahme vermerkt" in out, out[:100])
rec = R.load(SID)
check("Ausnahme steht in der Quittung", "quant-statistician" in (rec.get("skipped") or {}))
check("missing_steps respektiert Ausnahme",
      R.missing_steps(rec, None) == ["quant-mathematician"], R.missing_steps(rec, None))

print("\n== 3. guard_chain: Aktions-Gates ==")
base = {"session_id": SID, "transcript_path": None}
# ohne Transkript darf nie geblockt werden
res, err = hook("guard_chain.py", dict(base, tool_name="WebSearch", tool_input={"query": "x"}))
check("ohne Transkript kein Block", decision(res) is None, res)

# Transkript ohne Agent-Aufrufe bauen
tdir = Path(__file__).parent
tr = tdir / "fake_transcript.jsonl"
tr.write_text(json.dumps({"type": "user", "timestamp": "2026-09-21T20:00:00Z",
                          "message": {"content": "test"}}) + "\n", encoding="utf-8")
b2 = {"session_id": SID, "transcript_path": str(tr)}

res, err = hook("guard_chain.py", dict(b2, tool_name="WebSearch", tool_input={"query": "x"}))
check("WebSearch ohne research-scout blockt", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Write",
                tool_input={"file_path": r"C:\Users\maxlk\Projects\hub\static\app.js", "content": "x"}))
check("Hub-Datei ohne design-guard blockt", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Bash",
                tool_input={"command": ".\\hot_reload.ps1"}))
check("hot_reload OHNE eigene UI-Aenderung blockt nicht", decision(res) is None, res)

# Transkript, in dem diese Session selbst eine Hub-Datei geschrieben hat:
# dann ist hot_reload sehr wohl UI-Arbeit und design-guard Pflicht. Faengt auch
# den Umgehungsweg "UI-Datei per sed aendern" ab.
tr_ui = tdir / "fake_transcript_ui.jsonl"
tr_ui.write_text(json.dumps({
    "type": "assistant", "timestamp": "2026-09-21T20:00:00Z",
    "message": {"content": [{"type": "tool_use", "name": "Edit",
                             "input": {"file_path": r"C:\Users\maxlk\Projects\hub\static\app.js"}}]}}) + "\n",
    encoding="utf-8")
res, err = hook("guard_chain.py", {"session_id": SID, "transcript_path": str(tr_ui),
                                   "tool_name": "Bash", "tool_input": {"command": ".\\hot_reload.ps1"}})
check("hot_reload NACH eigener UI-Aenderung blockt", decision(res) == "deny", res)
tr_ui.unlink(missing_ok=True)
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": str(VAULT / "Bereiche" / "Strategie-Logbuch.md"),
    "old_string": "alt", "new_string": "### #168 Neue Lehre"}))
check("neuer Logbuch-Eintrag ohne distiller blockt", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": str(VAULT / "Bereiche" / "Strategie-Logbuch.md"),
    "old_string": "Tippfehlr", "new_string": "Tippfehler"}))
check("Logbuch-Tippfehler blockt NICHT", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\trading-data\engine\book_state.json", "content": "{}"}))
check("book_state ohne Quant/Auditor blockt", decision(res) == "deny", res)

# hub_config.json: Roster-Pflege ist keine UI-Arbeit, Layout-Aenderung schon
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\hub\hub_config.json",
    "old_string": '"mock_loops": [', "new_string": '"mock_loops": [ {"name": "x"},'}))
check("hub_config Roster-Eintrag blockt NICHT", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\hub\hub_config.json",
    "old_string": '"apps": [', "new_string": '"apps": [ {"name": "neu"},'}))
check("hub_config Layout-Aenderung blockt", decision(res) == "deny", res)

print("\n== 3b. guard_chain: Subagents und Workflows (Befund 25.09.2026) ==")
# Gemessen 26.09.2026 (Claude Code 2.1.281, Agent-Tool) und 28.09.2026 (Workflow-Agents):
# im Subagent traegt die Hook-Eingabe agent_id + agent_type, transcript_path ist das
# HAUPT-Transkript. Hier: tr, ohne
# jeden Agent-Aufruf -- genau die Lage des research-scouts im Workflow eval-vs-funded.
WEB = [("WebSearch", {"query": "x"}), ("WebFetch", {"url": "https://example.org", "prompt": "x"})]
for typ in ("research-scout", "alpha-scout", "claude-code-guide"):
    decs = [decision(hook("guard_chain.py", dict(b2, tool_name=t, tool_input=ti,
                                                 agent_id="a0000000000000001", agent_type=typ))[0])
            for t, ti in WEB]
    check(f"{typ} im Workflow darf ins Web", decs == [None, None], decs)
res, err = hook("guard_chain.py", dict(b2, tool_name="WebSearch", tool_input={"query": "x"},
                                       agent_id="a0000000000000001", agent_type="quant-mathematician"))
check("anderer Subagent ohne research-scout blockt weiter", decision(res) == "deny", res)
check("Sperre sagt dem Subagent, dass er zurueckmelden soll",
      "Subagent `quant-mathematician`" in str(res), str(res)[:200])
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", agent_id="a0000000000000001",
                agent_type="research-scout",
                tool_input={"file_path": r"C:\Users\maxlk\Projects\hub\static\app.js", "content": "x"}))
check("Web-Freiheit gilt nur fuer Web: research-scout auf Hub-Datei blockt", decision(res) == "deny", res)

# Workflow-Journal: <sid>/subagents/workflows/<wf>/journal.jsonl + agent-<id>.meta.json
import shutil
tr_wf = tdir / "fake_transcript_wf.jsonl"
tr_wf.write_text(tr.read_text(encoding="utf-8"), encoding="utf-8")
wf_root = tdir / "fake_transcript_wf" / "subagents" / "workflows"


def fake_wf(wf, aid, typ, events):
    d = wf_root / wf
    d.mkdir(parents=True, exist_ok=True)
    (d / f"agent-{aid}.meta.json").write_text(json.dumps({"agentType": typ, "spawnDepth": 1}), encoding="utf-8")
    with (d / "journal.jsonl").open("a", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps({"type": ev, "agentId": aid, "key": "v2:x", "label": f"{typ}: Test"}) + "\n")


bw = {"session_id": SID, "transcript_path": str(tr_wf)}
fake_wf("wf_fail", "afa11ed0000000001", "research-scout", ["started", "failed"])
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"}))
check("gescheiterter Workflow-Agent zaehlt nicht als gelaufen", decision(res) == "deny", res)
fake_wf("wf_run", "a4c0000000000001", "research-scout", ["started"])
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"}))
check("laufender/abgebrochener Workflow-Agent zaehlt noch nicht", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"},
                                       agent_id="afa11ed0000000001"))
check("ohne agent_type: Typ kommt aus der meta.json", decision(res) is None, res)
# Abgebrochener Auditor darf das Buch nicht freigeben (Fund verdict-auditor, 26.09.2026)
fake_wf("wf_buch", "a5a0000000000001", "strategy-auditor", ["started"])
fake_wf("wf_buch", "a5a0000000000002", "quant-statistician", ["started"])
res, err = hook("guard_chain.py", dict(bw, tool_name="Write", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\trading-data\engine\book_state.json", "content": "{}"}))
check("abgebrochener Workflow-Auditor gibt book_state nicht frei", decision(res) == "deny", res)
# Gemessene Eingabe eines LAUFENDEN Workflow-Agents (Mini-Workflow hook-probe, 28.09.2026):
# agent_id + agent_type, transcript_path = Haupt-Transkript, im Journal nur `started`.
# Genau die Lage des research-scouts in bulenox-check (26.09.).
fake_wf("wf_live", "aeb2d06d9fc2dd7df", "research-scout", ["started"])
fake_wf("wf_live", "ad1c171bce5db0d77", "Explore", ["started", "result"])
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"},
                                       agent_id="aeb2d06d9fc2dd7df", agent_type="research-scout"))
check("laufender research-scout im Workflow (gemessene Eingabe) darf ins Web", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"},
                                       agent_id="ad1c171bce5db0d77", agent_type="Explore"))
check("Explore im selben Workflow bleibt gesperrt", decision(res) == "deny", res)
fake_wf("wf_adhoc", "a5c0070000000001", "research-scout", ["started", "result"])
res, err = hook("guard_chain.py", dict(bw, tool_name="WebSearch", tool_input={"query": "x"}))
check("research-scout aus Ad-hoc-Workflow zaehlt als gelaufen", decision(res) is None, res)
SIDW = "wfwf0000-0000-0000-0000-000000000005"
R.path_for(SIDW).unlink(missing_ok=True)
R.ensure(SIDW, prompt_hint="t")
R.set_type(SIDW, "research")
check("Ad-hoc-Workflow schliesst Kette `research`", R.missing_steps(R.load(SIDW), str(tr_wf)) == [],
      R.missing_steps(R.load(SIDW), str(tr_wf)))
R.path_for(SIDW).unlink(missing_ok=True)
shutil.rmtree(tdir / "fake_transcript_wf", ignore_errors=True)
tr_wf.unlink(missing_ok=True)

# Quittungs-Gate: der Scout muss in den Research-Cache zurueckschreiben koennen, auch wenn
# die Kette eines anderen Typs offen ist (Session d954c57e, 23.09.2026, Typ `buch`).
SIDB = "cacb0000-0000-0000-0000-000000000006"
R.path_for(SIDB).unlink(missing_ok=True)
R.ensure(SIDB, prompt_hint="t")
R.set_type(SIDB, "buch")
bb = {"session_id": SIDB, "transcript_path": str(tr), "tool_name": "Edit", "tool_input": {
    "file_path": str(VAULT / "Ressourcen" / "Research-Cache.md"), "old_string": "a", "new_string": "b"}}
for typ in ("research-scout", "alpha-scout"):
    res, err = hook("guard_chain.py", dict(bb, agent_id="a0000000000000003", agent_type=typ))
    check(f"{typ} darf bei offener Kette `buch` in den Research-Cache", decision(res) is None, res)
res, err = hook("guard_chain.py", bb)
check("Hauptthread bleibt beim Research-Cache gesperrt", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(bb, agent_id="a0000000000000003", agent_type="quant-mathematician"))
check("anderer Subagent bleibt gesperrt, mit Rueckmelde-Hinweis",
      decision(res) == "deny" and "Subagent `quant-mathematician`" in str(res), str(res)[:200])
R.path_for(SIDB).unlink(missing_ok=True)

print("\n== 4. guard_chain: Quittungs-Gate ==")
R.set_type(SID, "urteil")
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", tool_input={
    "file_path": str(VAULT / "Projekte" / "ADX Wege-Karte.md"), "content": "Urteil: tot"}))
check("Typ urteil + offene Kette blockt Vault-Write", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", tool_input={
    "file_path": str(VAULT / "Daily Notes" / "2026-09-21.md"), "content": "x"}))
check("Daily Note bleibt frei", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", tool_input={
    "file_path": str(HOOKS / "foo.py"), "content": "x"}))
check(".claude bleibt frei", decision(res) is None, res)
# Wechsel auf einen ketten-losen Typ ist selbst eine begruendete Ausnahme (siehe 7b)
R.set_type(SID, "frage", why="Testfall: doch nur eine Rueckfrage ohne Stempel")
res, err = hook("guard_chain.py", dict(b2, tool_name="Write", tool_input={
    "file_path": str(VAULT / "Projekte" / "ADX Wege-Karte.md"), "content": "x"}))
check("Typ frage blockt nicht", decision(res) is None, res)

print("\n== 5. on_prompt ==")
if R.path_for(SID).is_file():
    R.path_for(SID).unlink()
res, err = hook("on_prompt.py", {"session_id": SID, "prompt": "Rechne mir mal die Passquote fuer drei Wochen aus"})
ctx = (res.get("hookSpecificOutput") or {}).get("additionalContext", "")
check("on_prompt fordert Typ an", "receipt.py" in ctx and "--type" in ctx, ctx[:160])
check("on_prompt schlaegt rechnen vor", "`rechnen`" in ctx, ctx[:200])
check("on_prompt legt Quittung an", R.load(SID) is not None)
res, err = hook("on_prompt.py", {"session_id": SID, "prompt": "/briefing"})
check("Slash-Kommando ignoriert", not res, res)

print("\n== 6. on_stop ==")
res, err = hook("on_stop.py", {"session_id": SID, "transcript_path": str(tr), "stop_hook_active": False})
check("on_stop laeuft ohne Crash", isinstance(res, dict), err[:200])

# Der eigentliche Beweis: blockt on_stop wirklich, wenn die Quittung offen ist?
# Dafuer ein Transkript, das echte Aenderungen zeigt (made_changes), plus eine
# Quittung mit Typ und nicht gelaufener Kette. Frische session_id, weil on_stop
# je Befund nur EINMAL blockt (SEEN_DIR).
SID2 = "aa22bb22-0000-0000-0000-000000000002"
tr2 = tdir / "fake_transcript_changed.jsonl"
tr2.write_text(json.dumps({
    "type": "assistant", "timestamp": "2026-09-21T20:00:00Z",
    "message": {"content": [{"type": "tool_use", "name": "Edit",
                             "input": {"file_path": str(VAULT / "Projekte" / "Irgendwas.md")}}]}}) + "\n",
    encoding="utf-8")

if R.path_for(SID2).is_file():
    R.path_for(SID2).unlink()
R.ensure(SID2, prompt_hint="test")
clear_stop_memory(SID2)
res, err = hook("on_stop.py", {"session_id": SID2, "transcript_path": str(tr2), "stop_hook_active": False})
check("on_stop blockt bei fehlendem Typ", res.get("decision") == "block", res)
check("Block nennt den receipt-Befehl", "receipt.py" in str(res.get("reason", "")), str(res)[:200])

SID3 = "cc33dd33-0000-0000-0000-000000000003"
if R.path_for(SID3).is_file():
    R.path_for(SID3).unlink()
R.ensure(SID3, prompt_hint="test")
R.set_type(SID3, "urteil")  # Kette verdict-auditor, im Transkript nie gelaufen
clear_stop_memory(SID3)
res, err = hook("on_stop.py", {"session_id": SID3, "transcript_path": str(tr2), "stop_hook_active": False})
check("on_stop blockt bei offener Kette", res.get("decision") == "block", res)
check("Block nennt den fehlenden Schritt", "verdict-auditor" in str(res.get("reason", "")), str(res)[:200])

# Kette bewusst ausgelassen -> darf nicht mehr blocken
R.skip(SID3, "verdict-auditor", "Testfall, bewusst ausgelassen zur Pruefung des Overrides")
res, err = hook("on_stop.py", {"session_id": SID3, "transcript_path": str(tr2), "stop_hook_active": True})
check("begruendete Ausnahme loest den Block", "verdict-auditor" not in str(res.get("reason", "")), str(res)[:200])

for s in (SID2, SID3):
    if R.path_for(s).is_file():
        R.path_for(s).unlink()
tr2.unlink(missing_ok=True)

print("\n== 7. Alt-Hooks unbeschaedigt ==")
for h, payload in [("guard_bash.py", {"tool_input": {"command": "ls"}}),
                   ("guard_write.py", {"tool_name": "Edit", "tool_input": {"file_path": "x.md"}}),
                   ("after_change.py", {"tool_name": "Edit", "tool_input": {"file_path": "x.md"}}),
                   ("guard_read.py", {"tool_input": {"file_path": "x.md"}})]:
    res, err = hook(h, payload)
    check(f"{h} laeuft", "Traceback" not in err, err[:150])

print("\n== 7b. Befunde des verdict-auditors (21.09.2026) ==")

# (1) DER Kern-Bug: ein vollstaendiger `kette`-Lauf muss die Kette schliessen.
# Workflow-interne Agent-Aufrufe stehen NICHT im Haupt-Transkript -- ohne Gutschrift
# blieb die Kette nach dem Lauf offen und --skip waere der einzige Ausweg gewesen.
for tid in [t["id"] for t in WT.TYPES if t["chain"] and t["id"] not in ("konzept", "hypothese")]:
    trk = tdir / f"fake_kette_{tid}.jsonl"
    trk.write_text(json.dumps({
        "type": "assistant", "timestamp": "2026-09-21T20:00:00Z",
        "message": {"content": [{"type": "tool_use", "name": "Workflow",
                                 "input": {"name": "kette", "args": {"type": tid}}}]}}) + "\n",
        encoding="utf-8")
    SIDK = f"ke{tid[:2]}0000-0000-0000-0000-00000000000{len(tid)}"
    if R.path_for(SIDK).is_file():
        R.path_for(SIDK).unlink()
    R.ensure(SIDK, prompt_hint="t")
    R.set_type(SIDK, tid)
    rk = R.load(SIDK)
    check(f"kette-Lauf schliesst Kette `{tid}`", R.missing_steps(rk, str(trk)) == [],
          R.missing_steps(rk, str(trk)))
    R.path_for(SIDK).unlink(missing_ok=True)
    trk.unlink(missing_ok=True)

# ein-weg/konzept-weg muessen weiterhin ihre Ketten schliessen
for tid, wf in (("hypothese", "ein-weg"), ("konzept", "konzept-weg")):
    trk = tdir / f"fake_{wf}.jsonl"
    trk.write_text(json.dumps({
        "type": "assistant", "timestamp": "2026-09-21T20:00:00Z",
        "message": {"content": [{"type": "tool_use", "name": "Workflow",
                                 "input": {"name": wf}}]}}) + "\n", encoding="utf-8")
    SIDK = f"wf{tid[:2]}1111-0000-0000-0000-000000000009"
    if R.path_for(SIDK).is_file():
        R.path_for(SIDK).unlink()
    R.ensure(SIDK, prompt_hint="t")
    R.set_type(SIDK, tid)
    check(f"{wf} schliesst Kette `{tid}`", R.missing_steps(R.load(SIDK), str(trk)) == [],
          R.missing_steps(R.load(SIDK), str(trk)))
    R.path_for(SIDK).unlink(missing_ok=True)
    trk.unlink(missing_ok=True)

# (2) Typwechsel auf einen ketten-losen Typ ist eine Ausnahme, kein Generalschluessel
SIDD = "dd44ee44-0000-0000-0000-000000000004"
if R.path_for(SIDD).is_file():
    R.path_for(SIDD).unlink()
R.ensure(SIDD, prompt_hint="t")
R.set_type(SIDD, "urteil")
rec_d, err_d = R.set_type(SIDD, "frage")
check("Downgrade urteil->frage ohne Grund abgelehnt", rec_d is None and "Ausnahme" in (err_d or ""), err_d)
rec_d, err_d = R.set_type(SIDD, "frage", why="war doch nur eine Rueckfrage ohne Stempel")
check("Downgrade mit Grund erlaubt", rec_d is not None and rec_d["type"] == "frage", err_d)
check("Downgrade steht in der Quittung", bool(R.load(SIDD).get("downgrades")))
check("Hochstufen bleibt frei", R.set_type(SIDD, "buch")[0] is not None)
R.path_for(SIDD).unlink(missing_ok=True)

# (3) Bash darf die Gates nicht umgehen
R.ensure(SID, prompt_hint="t")
R.set_type(SID, "urteil")
res, err = hook("guard_chain.py", dict(b2, tool_name="Bash", tool_input={
    "command": 'echo "tot" >> "' + str(VAULT / "Projekte" / "ADX Wege-Karte.md") + '"'}))
check("Bash-Write bei offener Kette blockt", decision(res) == "deny", res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Bash", tool_input={
    "command": 'python calc.py > /tmp/scratchpad/out.json'}))
check("Bash ins Scratchpad blockt nicht", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Bash", tool_input={
    "command": 'grep -n "tot" "' + str(VAULT / "Projekte" / "ADX Wege-Karte.md") + '"'}))
check("reines Lesen per Bash blockt nicht", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Bash", tool_input={
    "command": 'sed -i s/a/b/ C:/Users/maxlk/Projects/trading-data/engine/book_state.json'}))
check("book_state per Bash blockt", decision(res) == "deny", res)
R.path_for(SID).unlink(missing_ok=True)

# (4) UI-Gate: gemischte Backend/UI-Dateien nur bei echter Oberflaechen-Aenderung
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\trading-data\engine\app_server.py",
    "old_string": "def load_book(path):", "new_string": "def load_book(path, strict=False):"}))
check("app_server Backend-Edit blockt NICHT", decision(res) is None, res)
res, err = hook("guard_chain.py", dict(b2, tool_name="Edit", tool_input={
    "file_path": r"C:\Users\maxlk\Projects\trading-data\engine\app_server.py",
    "old_string": "<div class='row'>", "new_string": "<div class='row wide'><button>Neu</button>"}))
check("app_server UI-Edit blockt", decision(res) == "deny", res)

print("\n== 8. kette.js deckt sich mit work_types.py ==")
# Die Ketten stehen zwangslaeufig doppelt (Python-Hook + JS-Workflow). Genau so
# etwas driftet still auseinander: der Hook blockt dann auf einen Schritt, den der
# Workflow gar nicht faehrt. Deshalb hier hart gegenpruefen.
import re as _re
kette = (VAULT / ".claude" / "workflows" / "kette.js").read_text(encoding="utf-8")
block = _re.search(r"const CHAINS = \{(.*?)\n\}", kette, _re.S)
check("CHAINS-Block in kette.js gefunden", block is not None)
if block:
    js_chains = {}
    for m in _re.finditer(r"^\s*(\w+):\s*\[([^\]]*)\]", block.group(1), _re.M):
        js_chains[m.group(1)] = [x.strip().strip("'\"") for x in m.group(2).split(",") if x.strip()]
    # Typen mit Kette, die kette.js fahren soll (konzept/hypothese haben eigene Workflows)
    own_wf = {"konzept", "hypothese"}
    for t in WT.TYPES:
        tid, chain = t["id"], t["chain"]
        if not chain or tid in own_wf:
            continue
        check(f"kette.js kennt `{tid}`", tid in js_chains, f"fehlt in kette.js")
        if tid in js_chains:
            check(f"Kette `{tid}` identisch", js_chains[tid] == chain,
                  f"py={chain} js={js_chains[tid]}")
    for tid in js_chains:
        check(f"kette.js hat keinen Geistertyp `{tid}`", tid in WT.BY_ID, "nicht in work_types.py")

# aufraeumen
if R.path_for(SID).is_file():
    R.path_for(SID).unlink()
tr.unlink(missing_ok=True)

print(f"\n==== {ok} OK, {fail} FAIL ====")
sys.exit(1 if fail else 0)
