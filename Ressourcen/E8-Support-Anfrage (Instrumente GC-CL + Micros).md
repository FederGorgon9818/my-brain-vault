---
tags:
  - ressource/anleitung
  - trading/prop
  - e8
erstellt: 2026-09-09
status: gesendet-wartet-auf-antwort
ticket: AP141
---
⬅️ [[Eval-Passing]] · [[Ticket-Epics]] · [[Research-Cache]] · [[Strategie-Logbuch]]

# 📧 E8-Support-Anfrage: welche Nicht-Index-Futures sind handelbar (GC, CL, SI, NG, ZN, 6E + Micros)?

> [!info] Ausgangslage
> Max will Gold-Futures ins Universum nehmen (09.09.2026). Die Futures-Recherche vom 25.08. (Logbuch #132, Research-Cache) hatte festgestellt: kein einziger Nicht-Index-Markt ist bei E8 primärquellen-belegt handelbar, Terms und ESPA enthalten keine Instrumentenliste, Sekundärquellen nennen nur ES/NQ/YM/RTY/CL/GC/SI (+ vereinzelt NG). Bevor Daten gekauft und Engine-Arbeit investiert wird, muss das schriftlich stehen. Ticket **AP141** (vorher `e8-instrumente-anfrage` ohne Nummer), Dach-Ticket **AP140** (Gold/Crude als neue Märkte), Daten-Ticket **AP142**.

## Status

- **09.09.2026:** Mail an `support@e8markets.com` abgeschickt (gleicher Kanal wie AP77/AP90/AP93, Gmail messageId `1a086b5bda9e607c`).
- Antwort bitte hier unten unter „Antwort" eintragen, dann Research-Cache-Zeile „E8 Signature Futures Instrumente (unvollständig, nur Sekundärquellen)" auf „bestätigt" setzen und AP141 schließen.

## Gesendeter Text (Entwurf)

**Betreff:** Signature Futures: which instruments are tradable in Evaluation and Funded (GC, CL, SI, NG, ZN, 6E, Micros)?

> Hi E8 team,
>
> quick question about the instrument universe for E8 Signature Futures (Tradovate). My futures account is E61803453048.
>
> Before I put development time into new markets, I would like to confirm in writing which CME products are tradable, and whether the rules differ between the Evaluation and the Funded stage.
>
> 1. Which of the following full-size contracts are tradable in (a) the Evaluation and (b) the Funded account? GC (Gold), SI (Silver), CL (WTI Crude), NG (Henry Hub Natural Gas), ZN / ZB (10-Year / 30-Year Treasury Notes/Bonds), 6E (Euro FX)
> 2. Are the CME Micro versions available as well, and if so which ones: MGC, MCL, MNG, M6E, the Micro Treasury Yield futures (2YY/5YY/10Y/30Y), MBT?
> 3. Do the same risk parameters apply to these markets as to the index futures (ES/NQ/YM/RTY): maximum contracts per market / scaling plan; the intraday-only rule (flat before the daily close) and the exact daily close time that applies to metals/energy, since their CME sessions end at different times than the equity indices; any product-specific news restrictions (e.g. EIA inventory report for CL/NG, London fix for GC)?
> 4. Is there an official, complete list of permitted symbols somewhere in the dashboard or help center that I can refer to? I could not find one in the Terms or the ESPA.
>
> Thanks a lot, and thanks for the fast replies in the past.
> Best regards, Max

## Warum genau diese Fragen

- **Eval vs. Funded getrennt:** bei AP77 stellte sich heraus, dass Regeln zwischen den Stufen abweichen können. Ein Markt, der nur in der Eval geht, nützt nichts.
- **Close-Zeit je Produkt:** COMEX-Gold und NYMEX-Crude haben andere Pit-/Settlement-Zeiten (GC 13:30 ET, CL 14:30 ET) als die Indizes (16:00/17:00 ET). Wenn E8 „flat before close" an der Index-Uhr misst, ändert das den Exit jeder Gold-Strategie.
- **News-Sperren:** E8 hat ein News-Fenster (AP77-Antwort). EIA-Report (Mi 10:30 ET) und London PM Fix (10:00 ET) sind genau die Zwangsflows, die wir handeln wollen; sind sie gesperrt, fällt das Why weg.
- **Micros:** nur relevant, falls E8 sie zulässt und der Spread relativ nicht deutlich schlechter ist; 1 GC passt ohnehin in den 50k/2k-Käfig.

## Antwort

*(noch offen)*
