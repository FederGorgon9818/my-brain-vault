---
name: box
description: Ampel-Check der Trading-Box (vmd202078, 100.127.89.9) über den box-ops-Agent - Discovery-Runner, Queue, Buch-Sync, RiskGuard/Telegram, NT8. Nutzen, wenn Max /box aufruft oder fragt "läuft alles?", "check die Box", "steht der Runner?".
---

# Skill: Box-Check

Startet den Subagent `box-ops` und gibt das Ergebnis als Ampel zurück. Nichts wird neu gestartet oder geändert, außer Max sagt es danach.

## Schritte

1. Prüfen, wo die Session läuft: Hostname `vmd202078` = direkt auf der Box (kein SSH nötig), sonst SSH `Administrator@100.127.89.9`.
2. `box-ops` als Agent starten (Rundgang: Runner-Heartbeat und PID, `queue.json` pending/running, Inbox ungelesen, `book_state*.json` Push-Stand, NT8-Prozess und Log des Tages, RiskGuard-Telegram-Felder, freier Plattenplatz). Im Urlaubs-Zeitraum (CLAUDE.md oben) ist der PC aus: Hub, Lab-Server und Heartbeat-Datei sind dann erwartet nicht erreichbar, keine Störung.
3. Ergebnis verdichten.

## Ausgabe

Eine Zeile je Punkt mit Ampel:

| Punkt | Ampel | Detail |
|---|---|---|
| Discovery-Runner | 🟢/🟡/🔴 | PID, Heartbeat-Alter, aktueller Job |
| Queue | | pending / running / Vorrat in Tagen |
| Inbox | | ungelesene Kandidaten, davon „besser" |
| Buch-Sync | | `book_state*.json` jünger als letzter Push? |
| NT8 + RiskGuard | | Prozess läuft, letzter Log-Eintrag, Telegram-Felder gefüllt |
| Platte/Last | | frei in GB, CPU grob |

Danach maximal drei Sätze: was rot/gelb ist und welcher Handgriff das beheben würde (Runner-Neustart per WMI-Zeile in `box_provision_discovery.ps1`, `--push-next`, Telegram-Werte aus `maxlab_watchdog.json`). Den Handgriff NICHT ausführen, nur benennen, es sei denn Max sagt „mach".
