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

**Fábio (E8 Support), 09.09.2026, 17:22 Uhr, ~15 Minuten nach dem Absenden:**

> Same rules apply in both stages. The only difference of the Performance Stage (Funded) is that you'll also have the payout requirements. You can trade GC, SI, CL, NG, and 6E. Yes, micro versions are available. No news restrictions for the Signature program, but slippage may occur around high-impact news — factor it into position sizing.

Fábios Aufzählung ("GC, SI, CL, NG, and 6E") ist **unvollständig** — er hat auf die offizielle Instrumentenliste verlinkt, und die zeigt deutlich mehr. Die verlinkte Liste ist die primäre, verbindliche Quelle, nicht seine Kurzfassung.

### Offizielle Instrumentenliste + Handelszeiten
Quelle: [helpfutures.e8markets.com/.../instrument-list-and-trading-hours](https://helpfutures.e8markets.com/en/articles/13001922-instrument-list-and-trading-hours) (per curl mit Browser-User-Agent geladen, 09.09.2026, WebFetch bekam 403).

**⭐ Wichtigste Korrektur gegenüber unserer Annahme:** Es gibt **keine produktspezifische Close-Zeit**. E8 fährt für ALLE Futures (Indizes, Metalle, Energie, FX, Ags, Rates, Krypto) dasselbe Fenster: **17:00–16:00 CT Handelszeit, Zwangsglättung aller offenen Positionen täglich um 15:10 CT (= 16:10 ET)**, unabhängig vom offiziellen Börsen-Settlement (COMEX-Gold settelt eigentlich 13:30 ET, NYMEX-Crude 14:30 ET — bei E8 irrelevant, es zählt nur die E8-eigene 15:10-CT-Regel). Unsere Annahme in AP140 ("COMEX RTH 08:20-13:30 ET, anderer Open als Index") war falsch und ist dort korrigiert.

**Handelbare Instrumente (bestätigt, offizielle Liste):**

| Gruppe | Symbole |
|---|---|
| Metalle (COMEX) | GC, MGC (Micro Gold), SI, Micro Silver (Symbol im Dump abgeschnitten), HG (Copper), PL (Platinum), PA (Palladium) |
| Energie (NYMEX) | CL, MCL (Micro Crude), QM (E-mini Crude), NG, MNG (Micro NG), QG (E-mini NG), RB (RBOB Gasoline), HO (Heating Oil) |
| FX (CME) | 6A, 6B, 6C, **6E**, 7E (E-mini Euro), M6A, M6B, **M6E**, MCD, 6J, 6S, 6M, 6N |
| Zinsen (CBOT) | **ZT (2Y), ZF (5Y), ZN (10Y), ZB (30Y), UB (Ultra-Bond), TN (Ultra-Note), ZQ (30-Day Fed)** — alle als klassische Preis-Futures, KEINE Micro-Yield-Futures (2YY/5YY/10Y/30Y) im Angebot |
| Agrar (CBOT) | ZC, ZW, ZS, ZM, ZL, LE, HE, GF |
| Krypto (CME) | MBT (Micro Bitcoin), MET (Micro Ether) |
| Index (zum Vergleich) | ES, NQ, RTY, YM, EMD, NKD + alle Micros |

**Margin je Kontrakt (aus der Kontraktgrößen-Seite, [Link](https://helpfutures.e8markets.com/en/articles/10155917-max-available-contract-sizes)):** GC 10.000 $, MGC 1.000 $, **SI nur 2.000 $** (deutlich günstiger als die anderen Vollkontrakte — für spätere Sizing-Überlegungen merken), CL 10.000 $, MCL 1.000 $, NG 10.000 $, MNG 1.000 $, 6E 10.000 $, M6E 1.000 $, ZN 10.000 $. E8 Signature Käfig-Struktur unverändert (50k-Konto → 4 Kontrakte / 40.000 $ Margin erlaubt, wie bei den Indizes) — 1 Kontrakt passt bei jedem der genannten Märkte locker rein.

**News-Trading:** keine Sperre für das Signature-Programm (anders befürchtet). EIA-Report und London-PM-Fix sind also nicht regelseitig blockiert, nur normales Slippage-Risiko wie am echten Markt.

**Damit für AP140 relevant:** ZN/ZB sind entgegen Fábios Kurzantwort tatsächlich handelbar — die Einschätzung "ZN nur als Event-Trade" bleibt trotzdem stehen (5 % Kosten/Range killt jede Dauer-Mechanik, das ändert die neue Info nicht). Die produktspezifische Close-Zeit-Sorge (Punkt 3 unserer Frage) ist erledigt: ein einziges Regelwerk für alle Märkte, einfacher als angenommen.
