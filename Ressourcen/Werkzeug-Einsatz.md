---
tags:
  - ressourcen/werkzeuge
  - claude/prozess
erstellt: 2026-10-05
status: aktiv (Regel Max, 16.09.2026)
---
# 🧩 Werkzeug-Einsatz: Plugins und neue Werkzeuge immer mitnutzen

Herkunft: aus der CLAUDE.md ausgelagert am 05.10.2026 ([[CLAUDE.md Verschlankung]])

⬅️ [[Hooks-Referenz]] · [[Claude Code Tools & Skills]]

Installiert ist nicht genug: sobald eines davon passt, **von selbst** einsetzen, ohne dass Max danach fragt. Passt es bewusst nicht, in einem Halbsatz sagen warum.

| Werkzeug | Einsetzen, wenn … |
|---|---|
| **pyright-lsp** (Plugin, `LSP`-Tool) | Python-Code in Engine/Hub/Hooks gelesen oder geändert wird: Definition/Referenzen/Aufrufer per LSP statt breitem Grep, nach jeder Änderung Diagnosen prüfen (fehlende Imports wegen `sys.path` sind bekannt und kein Befund). |
| **claude-md-management** → `claude-md-improver` | CLAUDE.md wird größer umgebaut oder auditiert, oder ein Abschnitt ist offensichtlich veraltet. |
| **claude-md-management** → `revise-claude-md` | am Session-Ende (`/abschluss`), wenn die Session eine neue dauerhafte Regel oder Lehre ergeben hat, bevor sie von Hand in die CLAUDE.md geschrieben wird. |
| **claude-code-setup** → `claude-automation-recommender` | ein neuer Hook, Skill, Agent, Workflow oder MCP-Server geplant wird, und bei Retro-Vorschlägen des `retro-agent`. |
| **`engine/overfit_crosscheck.py`** (pypbo-Gegenprobe) | nach jeder Änderung an `overfit.py` (zusätzlich zum `engine-regression-tester`), und wenn ein PBO/DSR-Urteil angezweifelt wird. Bekannte Abweichung: PBO-Median-Konvention bei ungeradem N (AP179). |
| **`engine/.venv-analysis`** (pyfolio-reloaded, pypbo; pandas 2.3.3) | Risiko-Tearsheets für ein Bein oder das Buch als Zusatzsicht zu den Lab-Reports. **Nie** ins System-Python installieren (würde pandas 3 des Runners downgraden); Daten im System-Python erzeugen, als Datei übergeben, in der venv auswerten. |
| **NSSM-Dienst `MaxLabDiscovery`** (Box) | jeder Runner-Stopp/-Start: STOP-Datei bzw. `engine\discovery\start_runner.ps1`, nie WMI daneben. Neue Dauerläufer (Hub/Lab am PC) ebenfalls als NSSM-Dienst statt WMI-Job-Escape planen (AP179). |

Mehr zum Runner: [[Discovery-Runner v2]].
