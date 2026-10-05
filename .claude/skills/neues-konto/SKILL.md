---
name: neues-konto
description: Prüfablauf, wenn Max ein Prop-Konto kauft oder hinzufügt, eine neue Firma oder Phase dazukommt (Funded-Wechsel, Kontogröße, Reset, Add-on). Trigger-Wörter wie "Account gekauft", "neues Konto", "150k", "FFN", "E8", "Challenge gekauft". Vor dem ersten Trade Regeln holen, gegen RiskGuard und Buch abgleichen.
---

# Skill: Neues Konto oder neue Firma

Regel Max, 22.09.2026. Auslöser: FundedNext-Challenge hat eine Consistency-Rule (Tagesgewinn ≤ 40 % vom Target), E8 nicht. Der Deckel fehlte im RiskGuard, bis er am 21.09. per Zufall auffiel. Deshalb läuft dieser Ablauf **von selbst und vor dem ersten Trade**, sobald Max ein weiteres Konto kauft oder eine neue Firma/Phase dazukommt (auch Funded-Wechsel, Kontogröße, Reset, Add-on). Ein Konto gilt erst als startklar, wenn die Prüfung durch ist.

## Schritte

1. **Regeln holen.** Regeln der Firma/Phase aus der Primärquelle holen (`research-scout`, Research-Cache zuerst, nicht direkt ins Web) und in [[Firm-Regeln je Konto]] eintragen: Consistency/Tagesgewinn, DD-Typ und Einrasten, News-Regel, Inaktivität, Zeitfenster/Flat-Zeit, Kontraktlimit, Payout-Regeln, Algo-/VPS-Erlaubnis, Haushaltsgrenze.
2. **Jede Regel gegen die Umsetzung abgleichen und alles Nötige anpassen:**
   - `MaxRiskGuard.cs`: cfg-Datei `maxlab_riskguard.cfg` pro Konto, nie nur die UI.
   - Strategie-Instanzen und Größe (k).
   - `book_state.json` und Käfig (`cage_policy_lib`, `evaluate_v2`).
   - Watchdog und Telegram: **RiskGuard Telegram-Felder prüfen, siehe Skill `riskguard`** (leere `TelegramToken`/`TelegramChatId` heißt stumm).
   - Was noch nicht als Property existiert, wird als Ticket angelegt (vorher `inbox_tool.py --pull`) und **vor dem Trade gebaut**. Bis dahin handelt das Konto nur mit Handaufsicht.
3. **Festhalten und ansagen.** Konten-Liste, Regel-Tabelle und die aktiven Deckel (Werte je Konto) in [[Firm-Regeln je Konto]] eintragen und Max ansagen, was angepasst wurde. Der Dauer-Check bei Statuswechsel (Challenge zu Funded) hängt an **AP203**.

## Zugriff

Box per `ssh Administrator@100.127.89.9`, immer selbst nutzen, nicht an Max delegieren (siehe Skill `box`).
