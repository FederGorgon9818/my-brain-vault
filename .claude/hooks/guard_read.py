"""PreToolUse(Read): grosse Logs/Results/Transkripte nie komplett lesen."""
from _common import *  # noqa


def main():
    inp = read_input()
    p = norm((inp.get("tool_input") or {}).get("file_path"))
    if not p:
        sys.exit(0)
    if p.endswith("runner.log"):
        deny("STOP (Hook): runner.log nie komplett lesen. `python discovery/inbox_tool.py --pull` "
             "oder gezielt `Get-Content runner.log -Tail 40` / Select-String.")
    if re.search(r"/results/[^/]+\.json$", p):
        deny("STOP (Hook): results/*.json sind gross. `python summarize_results.py <datei>` lesen, "
             "nie das volle JSON.")
    if re.search(r"/\.claude/projects/.+\.jsonl$", p):
        deny("STOP (Hook): Session-Transkripte sind mehrere MB. Dafuer gibt es "
             "`.claude/scripts/session_conflicts.py` (session-guard).")
    sys.exit(0)


run(main)
