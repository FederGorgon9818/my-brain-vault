---
tags:
  - ressource/anleitung
  - trading/prop
  - e8
erstellt: 2026-08-16
status: beantwortet
ticket: AP99
---
⬅️ [[Eval-Passing]] · [[Ticket-Epics]] · [[Research-Cache]] · [[Strategie-Logbuch]]

# 📧 E8-Support-Anfrage: DD-Höhe 100k/150k + Signature-Status + Reset

> [!warning] Warum das vor dem Kauf geklärt sein muss
> AP99 entscheidet, ob die gestrichenen 2x25k durch weitere 50k oder durch 100k/150k ersetzt werden. Beim 100k/150k-Tier widersprechen sich die Sekundärquellen beim Drawdown (3 % vs. 4 %, Research-Cache Z. 81). Das sind unter Zielfunktion v2 rund **11 Prozentpunkte Passquote** (100k: 80 % bei DD 4 % gegen 69 % bei DD 3 %) und damit 326 $ gegen 378 $ pro funded Konto — der Unterschied entscheidet die Kaufempfehlung. Dazu: mehrere Review-Seiten führen „Signature" seit August 2026 als Auslaufprodukt (Cache Z. 85), und ob ein geplatztes Konto per Reset billiger nachgekauft werden kann, geht direkt in die Kostenrechnung ein.

## Kanal
Offizieller Support-Chat (wie AP77/AP90), Antwort als Screenshot archivieren.

## Text zum Rauskopieren

```
Hello E8 Team,

I am planning to purchase an E8 Signature Futures evaluation account and
would like a few details confirmed in writing before I buy.

1) Drawdown on the larger accounts
What is the exact maximum drawdown for the 100k and the 150k Signature
Futures evaluation accounts, in dollars? Public review sites list
contradictory numbers (3% vs 4%, i.e. $3,000 vs $4,000 on the 100k and
$4,500 vs $6,000 on the 150k). Could you also confirm the drawdown type
for these two account sizes: is it the same EOD trailing/dynamic drawdown
as on the 25k and 50k accounts, where the floor only trails the end-of-day
high of the closed balance?

2) Profit target
Please also confirm the profit target for 100k and 150k (I have $6,000 and
$9,000 from secondary sources).

3) Product status
Is E8 Signature Futures still available for purchase as of today, and will
the current rule set continue to apply to accounts purchased now? Some
review sites describe it as a legacy product that is being phased out.

4) Fee structure
Is the evaluation fee a one-time payment, or is there any recurring or
monthly charge while the evaluation is running? Since there is no time
limit on the evaluation (confirmed to me earlier by your team), I want to
be sure that a long-running evaluation does not incur additional costs.

5) Reset
If an evaluation account breaches its drawdown, is there a reset option,
and what does a reset cost for the 50k, 100k and 150k accounts? Is a reset
cheaper than purchasing a new evaluation account?

Thank you very much for the written confirmation.

Best regards,
Max
```

## Antwort erhalten (E8 Support, Support@e8markets.com, 16.08.2026, 17:49 Uhr)

> Dear Maxl, Thank you for reaching out. Regarding account structure you can fully review this information here: https://helpfutures.e8markets.com/en/articles/11864618-e8-signature-futures. There are no subscriptions or activation fees within E8 Markets, only one-time payment accounts at the moment of checkout. And in case you want to retry the same account you can do it but you would have to pay. Resets always provide you with a 10% discount but normally you can get the same discount using code "E8" for a complete new order!

Pauschale Antwort — verweist statt eigener Zahlen auf den Help-Center-Artikel. Der Artikel selbst ist aber die gesuchte Primärquelle und beantwortet den eigentlichen Streitpunkt vollständig.

## Ergebnis aus dem verlinkten Help-Center-Artikel (Primärquelle, "updated this week")

1. **DD-Streit aufgelöst: 3%, nicht 4%.** EOD Dynamic Drawdown: 25k $1.000 · 50k $2.000 · **100k $3.000 · 150k $4.500**. Das entspricht den bisherigen "dd3"-Werten in `cage_v2_tiers.json` — die "dd4"-Annahme (100k $4.000 / 150k $6.000) ist widerlegt.
2. **Targets bestätigt:** 25k $1.500 · 50k $3.000 · 100k $6.000 · 150k $9.000 (deckt sich mit dem, was schon angenommen war).
3. **Kein Zeitlimit, Inaktivität nach 7 Tagen** — deckt sich mit der AP90-Antwort (1x/Woche).
4. **Kontraktlimits bestätigt:** 25k 2 · 50k 4 · 100k 8 · 150k 12 Kontrakte.
5. **Kein Auslaufprodukt** — Artikel ist frisch gepflegt, Support berät anstandslos zum Kauf.
6. **Keine laufenden Kosten**, nur Einmalzahlung — das lange Median (450 Tage auf 150k) kostet nichts extra.
7. **Reset = 10% Rabatt**, praktisch gleichwertig zu Neukauf mit Rabattcode "E8" — kein eigener Kostenvorteil, aber auch kein Nachteil.

## Was danach passiert

1. ~~`cage_v2_tiers.json` auf die bestätigten Werte korrigieren~~ — Datei hatte die richtigen dd3-Werte bereits, die dd4-Einträge sind jetzt als falsch markiert/entfernt.
2. 150k-DD3-Passquote fehlt noch im Tier-Vergleich (bisher nur DD4 gerechnet) — `python cage_v2_tiers.py` mit den korrigierten Tiers neu laufen lassen.
3. Danach `python funded_finalize.py` (Portfolio-Tab-Regel), AP99 entscheiden und schließen, AP91 (Kauf) auf den bestätigten Käfig umschreiben.
