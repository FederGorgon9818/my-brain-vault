---
tags: [ressource, claude-code, setup, rückblick]
datum: 2026-11-16
---

# Terminal-Phase Rückblick (16.11.2026)

**Anlass (Max, 16.11.2026):** Rückkehr vom Terminal (Claude Code CLI in Windows Terminal) in die Claude-Desktop-App. Frage: was haben wir in der Terminal-Phase benutzt, was lief gut, was gar nicht. Zeitraum: CLI installiert 28.10., Umzug nach `C:\Claude` und Wechsel am 31.10. ([[Ordner-Umzug C-Claude]]), letzte Terminal-Session 12.11.

**Grundlage:** Daily Notes 31.10. bis 12.11., Projektnotizen ([[Jarvis Sprachsteuerung]], [[Jarvis Rückmeldung Vorschlag (09.11.2026)]]), die Cockpit-Mods und ein Skript über alle Session-Protokolle seit 01.10. (Einstiegspunkt, Ordner, Werkzeug-Aufrufe, Fehler). Alle Zahlen unten kommen aus diesem Skript.

## Der Hauptbefund: im Terminal liefen die Hooks fast nie

Die Terminal-Sessions starteten in `C:\Claude`. Dort lädt `C:\Claude\CLAUDE.md` die Vault-Regeln per Import, aber Hooks (`My Brain\.claude\settings.json`) und Gedächtnis hängen am Ordner. **Nur 3 von 33 Terminal-Sessions (9 %) liefen im Vault-Ordner**, mit den Jarvis-Arbeitern 7 von 74. Damit fehlten Pflichtketten, Agent-Trigger, Daily-Note-Sperre und Push-Reflex: die Regeln standen nur als Text da, genau der Effekt aus dem Audit vom 21.09. ([[Arbeits-Workflow (Auftrags-Typen)]]).

| | Desktop 01. bis 30.10. (142 Sessions) | Terminal 31.10. bis 15.11. (33 Sessions) |
|---|---|---|
| Sessions mit Agent | 63 % | 9 % |
| Agent-Aufrufe je Session | 2,74 | 0,21 |
| Sessions mit Workflow | 10 % | 3 % |
| Sessions mit Popup-Frage | 35 % | 48 % |
| Hook-Sperren je Session (grob gezählt) | 0,70 | 0,06 |
| Daily Note im Schnitt | 16,1 KB (25 Tage) | 2,5 KB (9 Tage) |
| Terminal-Tage ohne Daily Note | | 3 von 12 (03.11., 05.11., 09.11.) |

**Abzug:** In der Phase lief weniger Engine- und Alpha-Arbeit (Funded-Umstellung, Steuer, Jarvis). Ein Teil des Rückgangs ist Aufgaben-Mix, der Sprung von 63 % auf 9 % aber nicht.

**Zweite Folge, Gedächtnis gespalten:** Das Terminal hatte ein eigenes Gedächtnis (Projekt `C:\Claude`) mit 4 Einträgen, der Vault-Ordner hat 21. Die Feedback-Regeln (Buch-Lücke, Deploy-Anleitung exakt, Prop-Firm-Mails usw.) waren im Terminal unbekannt. Das passt zu Max' Kritik vom 11.11. („Claude vergisst Kontext“, Gedächtnis „praktisch leer“). Dazu: alte Desktop-Sessions waren per `--resume` im neuen Ordner nicht mehr zu finden.

## Was gut lief

- **Umzug nach `C:\Claude`:** 12 Ordner, 11 Brücken, Golden Master 12/12, Tests grün. Bleibt, hat mit dem Terminal nichts zu tun.
- **Freigabe-Regeln** in `~/.claude/settings.json` (git ohne Force, Lese-Befehle, python, SSH auf die Box): gelten auch in der App.
- **Werkzeuge:** Chrome-Erweiterung, web.de, Gmail, FundedNext-Connector und SSH auf die Box liefen normal (Funded-Umstellung, Template-Fehlalarm-Fix).
- **Popup-Regel** saß auch ohne Hook.
- **Statuszeile** mit Token-Anzeige (nur Terminal).
- **Stand-Datei und Korrektur-Reflex** (Antwort auf die Kritik vom 11.11.) gelten überall.

## Was halb lief

- **Cockpit-Leiste** (Sessions links als Textual-App im Windows-Terminal-Split, Punkte für ungelesen/wartet, Ticket-Klick startet Session): am Ende stabil, aber drei Reparatur-Runden (Doppelklick 02.11., doppelte Leiste zweimal am 08.11.). Im Kern ein Nachbau dessen, was die App schon hat.
- **Jarvis:** Stufe 1 und 2 gebaut, 41 Hintergrund-Aufträge gelaufen. Aber: verstand oft falsch, rund 7 s bis zum ersten Ton (4 bis 6 s nach dem Tuning erwartet, nie nachgemessen), hing an alten „kann ich nicht“-Antworten, meldet fertige Sessions nur, wenn er sie selbst geöffnet hat. Seine Arbeiter liefen in `C:\Claude`, also auch ohne Hooks.

## Was gar nicht lief

- Hooks und Pflichtketten (oben). Das war der eigentliche Preis.
- Unter-Sessions, Aufgabenliste und Session-Übersicht gibt es im Terminal nicht, sie wurden per Mod und Jarvis nachgebaut, samt Fehlern.
- Gedächtnis getrennt vom Vault.

## Umgesetzt am 16.11.2026 (Max: „ja einrichten“, Mods für die App umbauen)

Entscheidungen Max per Popup: Tickets als **zweiter Tab** in der rechten Mod (nur Tickets, keine Sessions), Übersicht rechts angedockt, Jarvis parken, Mods **nur noch für die App**.

- **Mod `cockpit-uebersicht` v0.3.0** (`~/.claude/mods/cockpit-uebersicht`): Tab **Übersicht** für die App umgebaut (Fortschrittsbalken statt Blockzeichen, Zeilen per Flexbox, Zustand immer als Wort) und Tab **Tickets** neu: offene Tickets aus `tasks.json` in In Arbeit / Prüfen / Wartet / Offen (nach Dringlichkeit, erst 25, dann „Weitere“), Board-Filter, Klick klappt Details auf, „Unter-Session starten“ schickt einen kurzen Auftrag in den Chat. Sperre gegen Doppelklick (120 s), Fuß mit Stand von `tasks.json`, Warnung ab 2 Tagen. Befehle `/uebersicht`, `/tickets`. design-guard vorab und am fertigen Code, alle Hinweise eingebaut. `claude plugin test`: 3 von 3 grün, Validierung ohne Typfehler.
- **Terminal-Leiste entfernt:** Mod `cockpit-sessions` aus `CLAUDE_CODE_PLUGIN_DIRS` genommen, Ordner nach `~/.claude/backups/mods-20261116/` (dort auch v0.2 beider Mods und die alte `settings.json`).
- **`CLAUDE_CODE_PLUGIN_DIR_WATCH=1`** in `~/.claude/settings.json`: die App lädt Mod-Änderungen künftig ohne neue Session nach.
- **Gedächtnis:** Cockpit-Eintrag aktualisiert in das Vault-Gedächtnis geholt, neue Lehre „Sessions im Vault-Ordner“ in beiden Gedächtnissen.
- **Jarvis geparkt** (Status in beiden Jarvis-Notizen, kein Autostart vorhanden).

**Abnahme 16.11. abends (Screenshots Max nach App-Neustart):** Tabs-Reihenfolge, Ticket-Titel, Fortschrittsbalken passen. Gmail in der Übersicht war kaputt, weil die App den Connector unter einer ID führt statt als „claude.ai Gmail“; behoben in v0.3.1 (Connector wird gesucht, Antwort richtig gelesen, Test dazu).

## Lehre

**Sessions immer im Vault-Ordner starten** (oder einem Worktree davon). Außerhalb laufen keine Hooks und nicht das volle Gedächtnis, und genau das hat die Terminal-Phase gekostet, nicht das Terminal selbst. Gilt auch für Unter-Sessions und Hintergrund-Arbeiter.
