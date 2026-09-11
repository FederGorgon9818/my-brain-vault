"""UserPromptSubmit: Agent-Reflex beim Tippen (Regel Max, 11.09.2026).

Max: "stelle sicher, dass dieser Agent immer genutzt wird, wenn er brauchbar ist".
Die Einschalt-Regeln stehen in der CLAUDE.md, aber die Erfahrung (27.08., 01.09.)
zeigt: ohne Reflex im Harness wird ein Agent leicht vergessen. Dieser Hook liest den
Prompt, prueft ihn gegen agent_triggers.py und legt Claude die passenden Agents als
Kontext hin. Keine Sperre, nur Erinnerung; die Entscheidung bleibt bei Claude/Max.
Slash-Kommandos und sehr kurze Prompts werden ignoriert.
"""
from _common import *  # noqa
from agent_triggers import match


def main():
    inp = read_input()
    prompt = str(inp.get("prompt") or "")
    if len(prompt.strip()) < 12 or prompt.lstrip().startswith("/"):
        sys.exit(0)
    hits = match("user", prompt)
    if not hits:
        sys.exit(0)
    lines = ["Hook (Agent-Reflex): der Prompt trifft Einschalt-Regeln aus der CLAUDE.md."]
    seen = set()
    for tid, agents, why, snippet in hits:
        key = tuple(agents)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- {' + '.join(agents)}: {why} (Fundstelle: \"{snippet[:80]}\")")
    lines.append("Wenn ein Agent hier nicht passt, kurz sagen warum; sonst einschalten, bevor gebaut/gerechnet/geurteilt wird. "
                 "Der Stop-Hook fragt am Ende nach, falls ein getroffener Agent nie lief.")
    context("\n".join(lines), "UserPromptSubmit")


run(main)
