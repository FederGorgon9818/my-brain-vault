"""Selbsttest Rechen-Bremse-Hinweis (AP411, Regel Max 18.10.2026).

Prueft vier Dinge, jeweils mit Treffern UND mit den Fehlalarm-Quellen:
  1. _common.pool_ohne_bremse: eigener Prozess-Pool ohne `rechen_bremse` wird erkannt, ThreadPool, Fremdworte mit "pool"
     und Dateien, die rechen_bremse erwaehnen, nicht.
  2. _common.py_ziele: welche .py-Datei ein Kommando-Segment startet (python -B x.py, in Anfuehrungszeichen, nicht -c/-m).
  3. guard_bash.py / after_change.py laufen als echte Hook-Prozesse (JSON auf stdin, eigener Engine-Ordner per
     MAXLAB_ENGINE) und geben den Hinweis genau einmal aus; Pool MIT Bremse und fremde Pfade schweigen; kaputte Eingabe
     blockt nie.
  4. ENGINE_CORE enthaelt rechen_bremse.py, und die Aenderung loest den Regressionstest-Zwang aus (newest_engine_core).

    python .claude/scripts/test_bremse_hint.py
"""
import json
import os
import subprocess
import sys
import tempfile
import shutil
import time
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
sys.path.insert(0, str(HOOKS))
import _common as C  # noqa: E402

RES = []


def check(name, ok, info=""):
    RES.append((name, bool(ok)))
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}" + (f"   {info}" if info else ""))


POOL_JA = [
    "import multiprocessing as mp\nwith mp.Pool(4) as p:\n    p.map(f, x)\n",
    'import multiprocessing as mp\nwith mp.get_context("spawn").Pool(n_proc) as pool:\n    pass\n',
    "import multiprocessing\npool = multiprocessing.Pool(processes=3)\n",
    "from multiprocessing import Pool\nPool(5)\n",
    "from concurrent.futures import ProcessPoolExecutor\nwith ProcessPoolExecutor(max_workers=w) as ex:\n    pass\n",
    "from concurrent.futures import ProcessPoolExecutor as PPE\nex = ProcessPoolExecutor ( max_workers=2)\n",
]
POOL_NEIN = [
    "import rechen_bremse as RB\nres = RB.pool_map(f, x, 4)\n",
    "import multiprocessing as mp\n# rechen_bremse: nicht noetig, laeuft nur auf der Box\nwith mp.Pool(4) as p:\n    pass\n",
    "from multiprocessing.pool import ThreadPool\nThreadPool(4)\n",
    "pool = tp.make_pool(dc, dw, firm, tier, k, n=POOL_N)\nx = make_pool(1)\n",
    "from concurrent.futures import ThreadPoolExecutor\nwith ThreadPoolExecutor(4) as ex:\n    pass\n",
    "print('kein Pool hier')\n",
    "",
]
PY_ZIELE = [
    ("python -B test_x.py --jobs 4", ["test_x.py"]),
    ("python test_x.py", ["test_x.py"]),
    ('python "C:/a b/x.py" --nsim 4', ["C:/a b/x.py"]),
    ("python3.11 -u _scratch_a/run.py", ["_scratch_a/run.py"]),
    ("py -3 ./foo.py", ["./foo.py"]),
    ("python -c \"print(1)\"", []),
    ("python -m konten.account_card --fleet", []),
    ("ls *.py", []),
    ("echo python is nice", []),
]


def hook(script, payload, engine, raw=None):
    env = dict(os.environ, MAXLAB_ENGINE=str(engine))
    r = subprocess.run([sys.executable, "-B", str(HOOKS / script)], input=raw if raw is not None else json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=60)
    ctx = ""
    if r.stdout.strip():
        try:
            ctx = json.loads(r.stdout)["hookSpecificOutput"].get("additionalContext", "")
        except Exception:
            ctx = "<<keine JSON-Ausgabe>>"
    return r.returncode, ctx, r.stdout


def main():
    print("1) pool_ohne_bremse")
    for i, s in enumerate(POOL_JA):
        check(f"Pool ohne Bremse erkannt #{i + 1}", C.pool_ohne_bremse(s))
    for i, s in enumerate(POOL_NEIN):
        check(f"kein Hinweis #{i + 1}", not C.pool_ohne_bremse(s))
    print("2) py_ziele")
    for cmd, soll in PY_ZIELE:
        check(f"{cmd!r}", C.py_ziele(cmd) == soll, str(C.py_ziele(cmd)))

    print("3) Hook-Prozesse")
    tmp = Path(tempfile.mkdtemp(prefix="bremse_hint_"))
    try:
        eng = tmp / "engine"; (eng / "_scratch_x").mkdir(parents=True)
        mit = eng / "_scratch_x" / "mit_pool.py"; mit.write_text(POOL_JA[0], encoding="utf-8")
        ohne = eng / "_scratch_x" / "mit_bremse.py"; ohne.write_text(POOL_NEIN[0], encoding="utf-8")
        bash = lambda cmd, cwd=None: {"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": str(cwd or eng)}
        rc, ctx, _ = hook("guard_bash.py", bash(f"python -B _scratch_x/mit_pool.py --jobs 4"), eng)
        check("guard_bash: Start eines Skripts mit eigenem Pool -> Hinweis (relativer Pfad, cwd = Engine)",
              rc == 0 and "rechen_bremse" in ctx and "mit_pool.py" in ctx, ctx[:80])
        rc, ctx, _ = hook("guard_bash.py", bash(f"python -B _scratch_x/mit_pool.py"), eng)
        check("guard_bash: derselbe Hinweis kommt nicht noch einmal (einmal je Datei)", rc == 0 and ctx == "", ctx[:60])
        mit2 = eng / "_scratch_x" / "mit_pool2.py"; mit2.write_text(POOL_JA[4], encoding="utf-8")
        rc, ctx, _ = hook("guard_bash.py", bash(f'cd "{eng}" && python "{mit2}"', cwd=tmp), eng)
        check("guard_bash: absoluter Pfad in Anfuehrungszeichen hinter cd && -> Hinweis", rc == 0 and "mit_pool2.py" in ctx, ctx[:80])
        rc, ctx, _ = hook("guard_bash.py", bash("python -B _scratch_x/mit_bremse.py"), eng)
        check("guard_bash: Pool MIT rechen_bremse -> still", rc == 0 and ctx == "")
        rc, ctx, _ = hook("guard_bash.py", bash("grep Pool _scratch_x/mit_pool.py"), eng)
        check("guard_bash: grep auf die Datei startet nichts -> still", rc == 0 and ctx == "")
        rc, ctx, _ = hook("guard_bash.py", bash("python -B gibt_es_nicht.py"), eng)
        check("guard_bash: Datei gibt es nicht -> still, kein Fehler", rc == 0 and ctx == "")
        rc, ctx, out = hook("guard_bash.py", None, eng, raw="das ist kein json")
        check("guard_bash: kaputte Eingabe blockt nie", rc == 0 and "deny" not in out)
        # PostToolUse: Edit/Write einer Datei im Engine-Ordner
        neu = eng / "_scratch_x" / "neu_pool.py"; neu.write_text(POOL_JA[1], encoding="utf-8")
        w = lambda p, tool="Write": {"tool_name": tool, "tool_input": {"file_path": str(p)}}
        rc, ctx, _ = hook("after_change.py", w(neu), eng)
        check("after_change: Write eines Engine-Skripts mit eigenem Pool -> Hinweis", rc == 0 and "rechen_bremse" in ctx and "neu_pool.py" in ctx, ctx[:80])
        rc, ctx, _ = hook("after_change.py", w(neu, "Edit"), eng)
        check("after_change: zweiter Edit derselben Datei -> still", rc == 0 and ctx == "")
        rc, ctx, _ = hook("after_change.py", w(ohne), eng)
        check("after_change: Pool MIT rechen_bremse -> still", rc == 0 and ctx == "")
        fremd = tmp / "anderswo"; fremd.mkdir(); (fremd / "p.py").write_text(POOL_JA[0], encoding="utf-8")
        rc, ctx, _ = hook("after_change.py", w(fremd / "p.py"), eng)
        check("after_change: Datei ausserhalb von engine/ -> still", rc == 0 and ctx == "")
        txt = eng / "_scratch_x" / "notiz.txt"; txt.write_text(POOL_JA[0], encoding="utf-8")
        rc, ctx, _ = hook("after_change.py", w(txt), eng)
        check("after_change: keine .py-Datei -> still", rc == 0 and ctx == "")
        rc, ctx, out = hook("after_change.py", None, eng, raw="{kaputt")
        check("after_change: kaputte Eingabe blockt nie", rc == 0 and "deny" not in out)

        print("4) ENGINE_CORE")
        check("rechen_bremse.py steht in ENGINE_CORE", "rechen_bremse.py" in C.ENGINE_CORE)
        eng2 = tmp / "engine2"; eng2.mkdir()
        old_engine = C.ENGINE
        try:
            C.ENGINE = eng2
            (eng2 / "qbt.py").write_text("x", encoding="utf-8"); os.utime(eng2 / "qbt.py", (time.time() - 600,) * 2)
            (eng2 / "rechen_bremse.py").write_text("y", encoding="utf-8")
            t, f = C.newest_engine_core()
            check("newest_engine_core sieht eine Aenderung an rechen_bremse.py (Regressionstest-Zwang vor dem Box-Sync)", f == "rechen_bremse.py", str(f))
        finally:
            C.ENGINE = old_engine
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    bad = [n for n, ok in RES if not ok]
    print(f"\n{len(RES) - len(bad)} von {len(RES)} Pruefungen gruen")
    if bad:
        print("FEHLER: " + "; ".join(bad))
        sys.exit(1)
    print("ALLE OK")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass
    main()
