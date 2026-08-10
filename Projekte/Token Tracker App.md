---
tags:
  - projekt
status: prototyp-läuft
prioritaet: hoch
deadline: 
erstellt: 2026-07-04
ort: C:\Users\maxlk\Projects\token-tracker
---
# 🎫 Token Tracker App

> [!success] Fertig als .exe gebaut & getestet (04.07.2026)
> Läuft lokal unter `C:\Users\maxlk\Projects\token-tracker`.
> **Starten (kein Python nötig):** Doppelklick auf `dist\TokenTracker.exe` → Browser öffnet `http://localhost:8712`.
> **Alternativ:** `start.bat` oder `python server.py`.
> Pure Python (Standard-Library) + Chart.js-Dashboard, als eigenständige 7-MB-.exe verpackt (PyInstaller).
> Getestet gegen echte Logs: korrekte Aggregation nach Tag/Stunde/Modell/5h-Block, HTTP 200.
> `config.json` (Budgets) liegt neben der .exe im `dist`-Ordner und ist editierbar.

> [!abstract] Ziel
> Eine kleine **Test-App**, mit der Max seinen **Claude Token-Verbrauch** im Blick hat: wie viel heute verbraucht, zu welcher Uhrzeit, Verlauf über die Zeit, und wie viel noch offen ist.

## Was die App können soll
- Anzeigen, **wie viele Tokens verbraucht** wurden (heute / gesamt).
- Verbrauch **nach Uhrzeit** aufschlüsseln.
- **Verlauf über die Zeit** speichern und darstellen.
- Idealerweise: **verbleibendes Kontingent** managen können.

## Zweck
- Erstes kleines **Testprojekt**, um das Setup und den Workflow mit Claude auszuprobieren.
- Praktischer Nutzen: Token-Budget im Pro/Max-Plan besser steuern.

## Datenquelle GEFUNDEN (04.07.2026)
Claude Code loggt pro Session lokal nach:
```
C:\Users\maxlk\.claude\projects\<projektordner>\*.jsonl
```
Jede Nachricht enthält ein `usage`-Objekt mit:
- `input_tokens`, `output_tokens`
- `cache_creation_input_tokens`, `cache_read_input_tokens`
- `timestamp` (sekundengenau), `model`

**Damit machbar:** Verbrauch heute/gesamt, Aufschlüsselung nach Uhrzeit, Verlauf über Tage, nach Modell.

**Einschränkung:** „Verbleibende Tokens" gibt Anthropic für Pro/Max nicht per API raus. Nur schätzbar, indem man Verbrauch gegen bekannte Rolling-Limits (5h-Fenster, Woche) rechnet. Die exakten `rate_limits`-Werte (5h/7d, used_percentage + resets_at) existieren zwar seit CC v2.1.x, sind aber NUR über den `statusLine`-stdin-Kanal erreichbar - und damit an einen Host gebunden, der diesen Hook auch aufruft (siehe Log 09.08./10.08.: bei Max' Setup **nicht** der Fall). Für alles andere (Dashboard, Skill, Obsidian-Plugin) bleibt es bei der Schätzung über `block_token_budget`/`weekly_token_budget`.

## Offene Punkte / zu klären
- [x] **Datenquelle:** lokale JSONL-Logs von Claude Code
- [x] **Tech:** Python (Standard-Library, kein Framework)
- [x] **Darstellung:** lokales Web-Dashboard (Chart.js) + Chat-Report (Skill `token-usage`, seit 03.08.)
- [x] **Speicherung:** keine eigene DB - liest JSONL-Logs live bei jedem Request

## Max-Plan Limits (Stand 07/2026, zum Kalibrieren)
Anthropic gibt **keine feste Token-pro-Tag-Zahl** raus (misst intern in Tokens, zeigt nur „Nachrichten"). Zwei Limits nebeneinander:
- **5h-Fenster (rolling):** Pro ~45 Prompts, Max 5x ~225, Max 20x ~900. (Für Claude Code am 06.05.2026 verdoppelt.)
- **Wochenlimits:** zwei Caps (alle Modelle + Sonnet separat), Reset wöchentlich zu fixer Zeit. Grob in Claude-Code-Stunden:
  - Pro: ~40-80h Sonnet
  - Max 5x: ~140-240h Sonnet, ~15-35h Opus
  - Max 20x: ~240-480h Sonnet, ~24-40h Opus
- **Opus frisst massiv mehr** als Sonnet/Haiku → einfache Tasks auf Sonnet/Haiku legen.

**Kalibrierung:** Beobachten, bei welchem verbrauchten Token-Wert das Limit greift, dann genau den als `block_token_budget` / `weekly_token_budget` setzen.

## Nächste Schritte
- [x] Datenquelle festlegen (wichtigste Frage)
- [x] Tech-Stack für den Prototyp wählen
- [x] Minimalen Prototyp bauen (nur Zahl „heute verbraucht")
- [ ] Budgets in config.json anhand echter Limits kalibrieren (einziger offener Punkt)

## Log
- **2026-07-04:** Projekt angelegt beim Onboarding.
- **2026-08-03:** `chat_report.py` ergänzt (importiert server.py direkt, gleiche Dedup-/Budget-Logik) + Skill `token-usage` in `.claude/skills/` angelegt. Report ab sofort direkt im Claudian-Chat abrufbar (`/token-usage`), kein Dashboard-Öffnen nötig - inkl. "Tokens seit letzter Anfrage" (Turn-Erkennung: echte User-Texteingabe vs. tool_result). Live getestet, echte Zahlen.
- **2026-08-03 (2):** Zusätzlich eigenes Obsidian-Plugin `.obsidian/plugins/token-status/` gebaut: Statusleisten-Anzeige (Text, kein Bild/Heatmap - echtes Claude-Code-Statusline-Prinzip), reagiert per `fs.watch` auf die Log-Datei statt Polling. Erst ungetestet übergeben, dann gemeinsam mit Max via Dev-Konsole verifiziert: Plugin lädt, `fs.watch` reagiert, Zahlen stimmen (`todayBillable`/`used5h`/`pct5h` live geprüft). Läuft. Gleiche config.json wie server.py, aber eigene vereinfachte 5h-Rolling-Window-Logik (nicht 1:1 die Block-Logik vom Dashboard) und zählt Subagent-Sidechains nicht mit.
- **2026-08-09:** `statusline.py` gebaut (native Claude-Code-Statusline statt nachgebaut wie im Obsidian-Plugin), eingetragen in `~/.claude/settings.json` (`statusLine`-Key). Zeigt „heute" aus den Logs (import server.py) plus die exakten `rate_limits.five_hour`/`seven_day` (used_percentage + resets_at), die CC seit v2.1.x per stdin mitliefert. Lokal mit simuliertem stdin funktional getestet, aber im echten Chat blieb die Zeile unsichtbar.
- **2026-08-10:** Ursache gefunden und Feature **verworfen**. Max chattet nicht über ein Terminal, sondern über die offizielle **Claude Desktop App** (`CLAUDE_CODE_ENTRYPOINT=claude-desktop`) - deren Chat-UI hat keine Plugin-/Erweiterungsstelle und ruft den `statusLine`-Hook nachweislich nie auf (Debug-Log in `statusline.py` blieb nach mehreren Nachrichten/Neustarts leer). Statusline ist ein reines Terminal-Feature; die exakten `rate_limits`-Werte sind ausschließlich über diesen Hook erreichbar, es gibt keinen anderen lokalen Zugriffsweg darauf. `statusline.py` wieder gelöscht, `statusLine`-Eintrag aus `~/.claude/settings.json` entfernt. **Entscheidung:** Max bleibt bei der bereits fertigen Obsidian-Statusleiste (`token-status`-Plugin, siehe 03.08.) als "immer sichtbare" Lösung - die läuft bereits echt live per `fs.watch`, unabhängig davon welcher Chat-Client gerade offen ist.
