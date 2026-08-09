---
tags:
  - ressource/claude-code
  - ressource/tools
erstellt: 2026-07-05
---
# 🤖 Claude Code Tools & Skills

Sammelstelle für nützliche Tools, Skills und Erweiterungen rund um Claude Code.

## Installiert / im Einsatz
- **kepano/obsidian-skills** (5 Skills): obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle.
- **Claudian Plugin** (realclaudian): Claude Code direkt in Obsidian.

## Eigene Tools
- **Smart Router** (`C:\Users\maxlk\Projects\smart-router`): wählt automatisch Haiku/Sonnet/Opus + Effort je nach Aufgabe. Regelbasiert, kein manuelles `/model`. ⚠️ Läuft über die **kostenpflichtige API** (API-Key nötig), nicht übers Max-Abo. Start: `python router.py "..."` oder `start.bat`. Modell-Logik: siehe [[Modellwahl (Opus vs Sonnet vs Haiku)]].
- **Token Tracker** (`C:\Users\maxlk\Projects\token-tracker`): siehe [[Token Tracker App]].

## Geprüft & bewertet

### ECC (affaan-m/ECC) → NICHT nutzen (05.07.2026)
Riesiges Optimierungs-Framework für Coding-Agents (277+ Skills, 67+ Agents, Session-Hooks, Security-Scanning, Cross-Platform).

**Verdict: Overkill für Max' Setup, nicht installieren.**
- Widerspricht dem bewusst schlanken, organisch wachsenden System.
- Vieles schon vorhanden: Daily Notes (statt Session-Persistence), eigener Token Tracker, eingebaute Skills `/code-review`, `/security-review`, `/verify`.
- Frisst Kontext & Tokens (viele Skills/Agents müssen geladen werden).
- Generisch, nicht auf Max zugeschnitten. **Nicht trading-/backtesting-bezogen.**
- Falls mal konkreter Bedarf: gezielt **eine** Sache rauspicken, nicht das ganze Framework.

## Eingebaute Skills, die ich schon habe
- `/code-review` – Diff auf Bugs & Cleanups prüfen
- `/security-review` – Security-Check der Änderungen
- `/verify` – Änderung end-to-end testen
- `/run` – App starten und Ergebnis sehen
