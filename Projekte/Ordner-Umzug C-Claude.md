---
date: 2026-10-31
tags: [projekt, setup, ordner, claude-code, terminal]
status: Phase 1 vorbereitet (31.10.2026), Ausführung durch Max, danach Phase 2 im Terminal
---

# 📁 Ordner-Umzug nach C:\Claude (31.10.2026)

**Auftrag Max 31.10.2026:** Weg von der Desktop-App, Claude künftig im Terminal. Dafür alles, was mit Claude zu tun hat (Vault, Projekte, Gewerbe/Steuer, Be Obsessed), übersichtlich unter `C:\Claude`. Große Daten sollten weder lange dauern noch Tokens kosten.

## Entscheidungen Max (31.10.)

| Frage | Entscheidung |
|---|---|
| Methode | Echt umziehen, am alten Ort bleibt eine Brücke (Junction) |
| Marktdaten | trading-data komplett mit (gleiches Laufwerk = nur Umbenennen, eine Sekunde) |
| Extras | Be Obsessed Videos, Gewerbe + Steuer, heimweg ins Archiv. Desktop-Kram bleibt. |
| Vault-Name | bleibt „My Brain" |

## Zielbild

Karte mit allen Ordnern: `C:\Claude\README.md`. Kurz: `My Brain\` (Vault), `projekte\` (trading-data, hub, webde-mail, whoop-mcp, token-tracker, smart-router), `content\` (Be Obsessed), `buero\` (Gewerbe, Steuer), `archiv\` (heimweg, ohne Brücke), `_umzug\` (Skripte).

Bleibt am alten Ort: `~\.claude` und `.claude.json` (Claude Code), `Documents\NinjaTrader 8` (NT8), Spiele, OneDrive, Desktop.

## Warum Brücken statt alles umschreiben

Bestandsaufnahme 31.10.: feste Pfade auf die alten Orte stecken in 1.192 Stellen in 898 Engine-Dateien, 57 Stellen in 31 Dateien unter `.claude` (Hooks, Agents, Skills, Workflows), 9 im Hub, in den zwei Windows-Tasks (`MaxLab Auto-Check`, `MaxLab Live Sync`), im Mail-MCP, in Obsidian, in den Vault-Worktrees und im Claude-Gedächtnis (Schlüssel = Ordnerpfad). Mit Brücke laufen alle weiter, umgestellt wird danach Schritt für Schritt.

Die Hooks erkennen Engine- und Hub-Dateien über `/engine/` bzw. `/hub/` im Pfad, die Sperren greifen also auch am neuen Ort. `_common.py` sucht Engine und Hub seit 31.10. zuerst unter `C:\Claude\projekte\...`, dann am alten Ort. `_LIVE_BASE` in `guard_bash.py` ist der Pfad **auf der Box** und bleibt.

## Phase 1: Umzug (Skript, Max startet es)

Skripte in `C:\Claude\_umzug\`: `umzug.ps1`, `rueckweg.ps1`, `umzug_lib.ps1`, `umzug_config.py`, Plan `umzug_plan.json` (12 Ordner, 11 mit Brücke, Vault zuletzt).

Ablauf im Skript: Vorcheck (Quelle da, Ziel frei, gleiches Laufwerk, keine blockierenden Programme) → Tasks pausieren → Ordner per Umbenennen verschieben → Brücke am alten Ort → `git worktree repair` im Vault → Claude-Gedächtnis: neuer Schlüssel `C--Claude-My-Brain` bekommt eine Brücke auf den alten `memory`-Ordner (alte Sessions bleiben unter dem alten Schlüssel, so zählt der Token-Tracker nichts doppelt) → Configs (`.claude.json` Projekt-Einträge kopiert, Mail-MCP, githubRepoPaths, `settings.json` additionalDirectories, Obsidian-Vault-Pfad, Sicherung in `_umzug\backup`) → Tasks auf neuen Pfad, wieder an.

Sicherheit: es wird nie ein echter Ordner gelöscht, nur Brücken nach Prüfung. Verschieben nur per Umbenennen auf demselben Laufwerk (sonst Abbruch, nie Kopie). Klemmt ein Ordner, dreht das Skript alles bereits Verschobene zurück.

**Getestet 31.10.** an Wegwerf-Ordnern (Scratchpad, mit Git-Repo und Worktree, Ordnername mit Leerzeichen): Trockenlauf ändert nichts, gesperrte Datei führt zu Abbruch mit vollständigem Zurückdrehen, echter Lauf mit identischen Inhalten am neuen Ort, Lesen und Schreiben über die Brücke, Worktree auf neuen Pfad repariert, zweiter Lauf wird abgelehnt, Rückweg stellt alles identisch wieder her. 0 Fehler. Config-Umsteller an Kopien der echten Dateien: nur die gemeinten Felder geändert, Rückweg byte-gleich. Trockenlauf mit echtem Plan: alle 12 Ordner planbar, Blocker erkannt (Claude, offener Editor mit Gewerbe-Datei, Mail-MCP).

Der Umzug kann nicht aus einer Desktop-Session laufen: Windows sperrt den Ordner, in dem die Session läuft.

### Anleitung für Max

1. Claude Desktop ganz beenden (auch im Tray), Obsidian, VS Code, Hub und offene Editoren schließen.
2. Normale PowerShell öffnen (kein Admin).
3. Trockenlauf: `powershell -ExecutionPolicy Bypass -File C:\Claude\_umzug\umzug.ps1 -DryRun`. Erwartet: 12 Zeilen „plane:" und „Trockenlauf fertig". Steht „LAEUFT NOCH:" da, das Programm schließen (notfalls Task-Manager) und wiederholen.
4. Echt: dieselbe Zeile ohne `-DryRun`. Erwartet am Ende „FERTIG". Bei „Abgebrochen, Stand wie vorher" ist nichts passiert, die Zeile davor sagt, welcher Ordner klemmt.
5. `cd "C:\Claude\My Brain"`, dann `claude`, und als Erstes „Umzug Phase 2" sagen.

Rückweg jederzeit: `powershell -ExecutionPolicy Bypass -File C:\Claude\_umzug\rueckweg.ps1`.

## Phase 2: erste Terminal-Session (Claude)

- [ ] Gedächtnis geladen (MEMORY.md im Kontext), Hooks melden sich, `_common.ENGINE` zeigt auf `C:\Claude\projekte\trading-data\engine`.
- [ ] `git status` und `git worktree list` in Vault, trading-data, hub.
- [ ] Selbsttests: `test_chain.py`, `test_konto_gate.py`, `test_urteil_gate.py`, `test_sync_gate.py`.
- [ ] Tasks: `Get-ScheduledTask "MaxLab*"` zeigt neuen Pfad und Ready, Auto-Check einmal von Hand anstoßen.
- [ ] MCP: webde-mail verbindet. `.mcp.json` (whoop) auf neuen Pfad.
- [ ] Obsidian öffnet „My Brain" aus `C:\Claude`.
- [ ] Hub und Lab-Server starten vom neuen Ort.
- [ ] Pfade umstellen: CLAUDE.md, `.claude/launch.json`, `knowledge_router.py`, Agents, Skills und Workflows (die 57 Stellen), `hub_config.json`, Obsidian-Plugin `token-status`, Memory-Einträge mit Pfaden.
- [ ] Engine-Pfade (1.192 Stellen) bleiben über die Brücke, Umstellung nach und nach (eigenes Ticket).
- [ ] Hinweis: alte Desktop-Sessions liegen unter dem alten Schlüssel, `claude --resume` im neuen Ordner zeigt sie nicht.

Verwandt: [[Tech-Stack]], [[Hooks-Referenz]], [[Daily Notes/2026-10-31]].
