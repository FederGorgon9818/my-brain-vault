---
tags:
  - projekt
  - trading
  - urlaub
datum: 2026-09-16
status: aktiv
zweck: Kuratierte Liste der Punkte, die Max nach dem Urlaub (Rückkehr ca. 18.09.2026) selbst entscheiden muss. Ticket-Details bleiben in tasks.json (Box = Quelle der Wahrheit); diese Notiz ist die kompakte Übersicht dafür.
---
⬅️ [[Projekte/_Projekte|Projekte]] · [[Eval-Passing]] · [[Strategie-Logbuch]]

# 🏖️➡️ Entscheidungen nach dem Urlaub

> [!info] Zweck
> Max ist ab 04.09.2026 zwei Wochen im Urlaub (siehe CLAUDE.md-Abschnitt oben). Diese Notiz sammelt die Punkte, die bewusst bis zur Rückkehr liegen gelassen wurden, statt allein entschieden zu werden — damit beim Wiedereinstieg nichts übersehen wird. Details/Guide immer im jeweiligen Ticket in `tasks.json` (`/ticket AP…`), hier nur die Kurzfassung + Stand.

## Offene Entscheidungspunkte

- **AP155 — Live-Strategien künftig automatisieren: NT8-Host-Strategie / MultiCharts / direkte Tradovate-API?**
  Claude-Empfehlung: Option 1 (NT8-Host-Strategie `MaxBookHost`) jetzt bauen, Option 2 (MultiCharts) verwerfen (research-scout 14.09.: löst das Klick-Problem nicht, Tradovate-Anbindung fehlt/abgelehnt), Option 3 (Python direkt an Tradovate-API) als späteres Ziel.
  **Update 16.09.2026:** E8 hat schriftlich bestätigt (Fábio, 14.09.), dass Option 3 erlaubt ist — auf Eval UND Funded, keine separate Freischaltung nötig, nur die üblichen Automatisierungsregeln (kein HFT >300 Trades/Tag). Option 3 ist damit nicht mehr tot, die Vorbedingung aus dem Ticket ist erfüllt.
  → Entscheidung: Option 1, 2 oder 3 (bzw. 1 jetzt + 3 als späteres Ziel)? Danach Folge-Tickets anlegen.

## Erledigt / kein Entscheidungsbedarf mehr

- **AP141 — welche Nicht-Index-Futures sind bei E8 handelbar:** beantwortet, keine Entscheidung nötig (reine Fakten, in [[E8-Support-Anfrage (Instrumente GC-CL + Micros)]] dokumentiert).
