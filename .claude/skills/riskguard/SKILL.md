---
name: riskguard
description: RiskGuard und Telegram nicht vergessen. Nutzen, wenn Max ansagt, dass MaxRiskGuard entfernt oder neu hinzugefügt wird, eine neue Strategie-Instanz angelegt wird, die Box rebootet, das Konto gewechselt wird, oder Telegram-Meldungen still sind. Prüft TelegramToken/TelegramChatId und die Tageslimits je Konto.
---

# Skill: RiskGuard neu anlegen, Telegram nicht vergessen

Regel Max, 20.08.2026.

`MaxRiskGuard` startet mit leeren `TelegramToken`/`TelegramChatId`-Feldern und schweigt dann bei JEDER Meldung, ohne Fehler oder Log-Eintrag. Ist schon mal wochenlang unbemerkt so gelaufen (Kontowechsel 18.08.2026).

## Wann

Immer wenn Max ansagt, dass RiskGuard entfernt oder neu hinzugefügt wird oder eine neue Strategie-Instanz angelegt wird, außerdem nach Box-Reboot und nach Kontowechsel.

## Schritte

1. **Aktiv daran erinnern**, `TelegramToken` + `TelegramChatId` neu einzutragen.
2. **Werte holen und direkt mit ausgeben.** Echte Werte liegen NICHT im Vault, sondern auf der Box in `C:\Users\Administrator\maxlab_watchdog.json` (Bot **maxbot** @maxbotalgobot). Per `ssh Administrator@100.127.89.9` holen und Max in der Antwort direkt nennen. Nie in eine Notiz oder Datei im Vault schreiben.
3. **Konten-Konfiguration prüfen.** Einstellungen laufen pro Konto über die cfg-Datei `maxlab_riskguard.cfg`, nie nur über die UI (Ablauf bei neuem Konto: Skill `neues-konto`).

## Tageslimits je Konto (Stand CLAUDE.md, Gate v4 Stufe 2)

Der echte RiskGuard-Tages-Stopp wird je Konto aus der cfg gelesen und fließt in die Wochenend-Rechnung ein:

| Konto | Tages-Stopp (bei k1) |
|---|---|
| E8 50k | 900 $ |
| FN (FundedNext) | 600 $ |
| E8 150k | 1.500 $ |

Hinweis: 600 $ × k ist beim 7er-Buch zu eng (Quant-Team 04./05.10.), deshalb feste Werte je Konto statt Multiplikator.

## cfg-Zeilen aus dem Deploy 2 (Daily Note 04.10.2026, nicht aus der CLAUDE.md)

- `inactivityalarmdays=4` je Konto (Inaktivitäts-Alarm ab Tag 4).
- `lockoffset=100` nur für FN1/FN2 (FN-Lock 50.100).
- Backup der cfg vor dem Deploy: `maxlab_riskguard.cfg.bak-20261004-deploy2`.
- Feste Größe je Konto per `fixedqty` (gebaut für E8 150k).

Details: [[Firm-Regeln je Konto]], [[Daily Notes/2026-10-04]].
