---
tags:
  - trading
  - plan
datum: 2026-08-24
status: Entwurf aus Loop-Session, Wochenend-Review offen
---
⬅️ [[Day Trading]] · [[Eval-Passing]] · [[Funded-Phase]]

# 🎯 Payout-Plan: Erster Payout + 10.000 €

**Max' Ziele (24.08.2026):** (1) erster Netto-Payout so schnell wie möglich, (2) 10.000 € kumuliert entnommen (gerechnet als 11.000 $), Politik: 50 % jedes Payouts reinvestieren, 50 % behalten. Alle Zahlen aus der Quant-Nacht 24.08. (Kaskaden-MC + Purged-WF + Pool-Suche, Details [[Strategie-Logbuch]] #129 ff.).

## Die Lage in vier Sätzen

1. **Die Passquote ist nicht der Engpass, die Uhr ist es:** ~26 $/Tag Backtest-Drift auf 3.000 $ Eval-Ziel + 2.625 $ Funded-Schwelle = ~14,6 Monate reine Driftstrecke bei E8 (Median erster Payout: Monat ~13-15).
2. **Die ehrliche Drift ist kleiner:** Purged-Walk-Forward → **10-14 $/Tag** (halb echtes Post-2022-Regime, halb Fit-Prämie). Vier unabhängige Methoden konvergieren dort. Alle Planzahlen zweigleisig lesen (IS-Drift / ehrlich).
3. **Mehr Size hilft nicht:** k_eval=3 ist statistisch ein Verzicht (P(µ>19 $/Tag) nur 12-16 %) UND operativ tot (E8 4-Mini-Kombicap an 47 % der Tage gerissen, RiskGuard kennt kein Per-Leg-Sizing). Mehrere korrelierte Beine parallel = dasselbe in Grün (P fällt monoton in k).
4. **Kein anderes Portfolio ist besser:** 2.643 Kombinationen aus dem 21er-Pool getestet, **keine schlägt das aktuelle Buch out-of-sample** (IS→OOS-Rangkorrelation −0,18; das Buch selbst: OOS-Rang 10/121).

## ✅ Der Plan (Hebel nach Robustheit)

### Hebel 1 — Firmen-Käfig für den ersten Slot: FundedNext Flex 50k (~80 $)
Der größte robuste Zeitgewinn kommt nicht aus Size oder Beinen, sondern aus den **Payout-Schwellen**: FN zahlt ab 500 $ Zyklusprofit + 5 Benchmark-Tagen (à ≥200 $), E8 erst ab 2.625 $ über Start.

| Median (Kalendertage) | E8 50k | FN Flex 50k |
|---|---|---|
| Ziel 1 (erster Payout), k=1, IS-Drift | 461 | **318** |
| Ziel 1, ehrliche Drift µ=13 | 918 | **546** |
| Ziel 2 (11k $), IS-Drift | 1.674 | **1.361** |
| Langfrist (120 M Entnahme-Median) | **112.859 $** | 81.026 $ |

→ **E8-Konto behalten** (langfristig besser: Gratis-Challenge-Recycling nach 5 Payouts), **FN Flex als schnellen ersten Payout-Slot dazu**. Passquote des Buchs im engeren FN-Käfig (1.500 $ effektiv intraday!): 76,1 % — eingerechnet.
⚠️ Vor FN-Kauf klären (Mail, wenn Max zurück ist): Lock-Zeitpunkt des Floors (Mails widersprüchlich) + Bestätigung, dass Parallelbetrieb zu E8 ok ist. Regeln: [[Research-Cache]] „FundedNext Flex — Support-Mail-Bestätigungen".

### Hebel 2 — Auszahlungs-Politik: sofort abrufen
„Payout anfordern, sobald Minimum verfügbar" (E8: 125 $ brutto; FN: 250 $) statt auf volle Caps warten: **~1-2 Monate früheres erstes Geld, kostet ~10 % auf 24 Monate, Ziel 2 unberührt.** Nach dem ersten Payout auf halben Cap umstellen. Freier Parameter, keine Firmenregel — sofort umsetzbar.

### Hebel 3 — Kaskaden-Disziplin: nie bei null Konten stehen
Größter Einzelhebel im ganzen Modell: **immer mindestens ein Konto am Leben halten** (bei Bust sofort 150 $/80 $ nachschießen). Wörtlich genommen („nur Reinvest") ist die Kaskade eine Sackgasse: 35-53 % der Pfade enden bei 0.

### Hebel 4 — Asia-Dir ×2: **Gegenprüfung durchgefallen, zurückgestellt**
Sah als einziger Portfolio-Hebel OOS-robust aus (−2,0 M erster Payout, −4,0 M bis 11k), aber der Auditor hat die Beweisführung zerlegt: **doppelter Fit auf derselben Historie** (Params am 20.08. retuned #126 + Gewicht aus einer NACH der OOS-Rechnung gewählten 7er-Referenzmenge = #079-Muster, zirkulär). Operativ wäre es machbar (4-Mini-Cap: 0/1816 Tage gerissen; kleiner `SizeMultiplier`-Patch in `MaxAsiaDirNQ.cs`), aber die Statistik steht nicht. **Bedingung für Wiedervorlage:** frischer Hold-out, der weder im #126-Retune noch in der 7er-Auswahl steckt — praktisch heißt das: echte Live-Zeit abwarten. Bis dahin: nicht anfassen.
Der Statistiker doppelt nach: 85 OOS-Tage sind **unterbestimmt** (Nachweisgrenze 64 $/Tag, beobachtet 60; OOS-Mittel = 3,3× IS = Glücksfenster), 31 % des Tempogewinns entstehen auch bei Edge null, und auf der v2-Zielgröße kostet es −3,7 pp (t = −6). Die Pool-Suche insgesamt: PBO 71 % — die IS-Selektion war nicht nur wertlos, sondern kontraproduktiv. Dieselbe Metrik gibt dem nachweislich toten RTY-Bein t = −7,3 — Tempo-Metriken allein sind kein Beweisinstrument.

### Buch-Hygiene (läuft schon)
- **RTY_Gap-fade raus:** besteht eigenes Top5-Gate nicht, 2/3 Epochen negativ, Mechanismus kanonisch tot. Bereits im Next-Week-Buch entfernt (4-Bein-Buch: 86,1 %/174 $/195 d — praktisch identisch), Ticket `next-week-2026-35-gapfade`, Retune-Job `gapfade_retune_RTY_260824` läuft auf der Box.
- **Regime-robusteste Beine:** NQ_Momentum + Asia-Dir (kanonisch schon vor 2020 positiv). LastHour = Post-2020-Phänomen.

## ❌ Geprüft und verworfen (nicht wieder anfassen ohne neuen Grund)
| Idee | Warum tot |
|---|---|
| Mehrere korrelierte Momentum-Beine parallel | Positions-Skalierung, P(pass) fällt monoton (Skalen-Invarianz P_k(T,D)=P_1(T/k,D/k)) |
| k_eval=3 Tempo-Slot | Statistisch Verzicht (12-16 %) + operativ nicht fahrbar (4-Mini-Cap, RiskGuard) |
| „Nach Floor-Lock rausquetschen" | Polster ist nach jedem Payout strukturell ~2.000 $ = bereits 1,16× Voll-Kelly |
| Portfolio-Neubau aus dem Pool | 2.643 Kombis, keine OOS besser; IS-Sieger kollabieren (VWAP-Pullback ×3 → OOS zweitschlechtestes Bein) |
| Buch komplett ×2 | −27 pp Passquote, Ziel 2 unverändert |
| Tradeify als Alternative | „Exclusive to Tradeify"-Klausel + Wohnsitz-Login nach jedem VPS-Neustart |

## 🧭 Ehrliche Erwartung (nicht die Hochglanz-Zahl)
Mit Plan (FN-Slot + Sofort-Abruf + Kaskaden-Disziplin), **ehrliche Drift**: erster Payout Median ~**11-18 Monate**, 10.000 € entnommen: Median jenseits von 3 Jahren, mit breitem Trichter. Mit IS-Drift: erster Payout ~7-10 Monate, 10k in ~4 Jahren. Das Einkommen kommt in Klumpen (>90 % Null-Monate am Anfang). **Der nachhaltigste Beschleuniger bleibt unkorreliertes neues Alpha** — jedes ρ≈0-Bein hebt θ und damit ALLE Zahlen gleichzeitig ([[Alpha-Suche]], Fokus neue Mechanismen/Datenquellen statt mehr Grid).

## 💶 Max' Kaufplan (150 €/Monat, entschieden 24.08. abends) — finale Rechnung

Politik: jeden Monat ~160 $ externes Budget (= 1× E8 ODER 2× FN Flex), dauerhaft; 50 % jedes Payouts kauft weitere Evals, 50 % behält Max. k=1, Sofort-Abruf. **Bindende Größe: der Funded-Cap von 5 Konten je Firma** — deshalb gewinnt die Zwei-Firmen-Politik.

| Median in Monaten | A: nur E8 (1/M) | B: nur FN (2/M) | **C: Mix (2 FN / 1 E8 im Wechsel)** |
|---|---|---|---|
| Erster Payout (IS-Drift / ehrlich) | 14,6 / 27 | **10,0** / 16,7 | 10,3 / 17,3 |
| 10.000 € Payouts **gesamt** | 31,4 / 67 | 25,8 / 56 | **23,5 / 47,6** |
| 10.000 € auf **Max' Hälfte** | 40,6 / 90 | 45,5 / 100 | **31,7 / 67** |
| P(Gesamt-Ziel scheitert in 5 J), ehrlich | 58 % | 46 % | **35 %** |
| Funded-Konten nach 24 M (IS) | 4,5 | 3,4 | **7,6** |
| Externe Kosten bis Gesamt-Ziel (IS, Median) | 1.050 $ | **720 $** | 1.777 $ |

**Empfehlung: C.** E8-Konto behalten, ab sofort im Wechsel ungerade Monate 2× FN Flex, gerade Monate 1× E8. B nur, wenn Kapitaleffizienz wichtiger ist als Zeit (Max' erklärtes Ziel ist Zeit). Warum C gewinnt: FN liefert das schnelle erste Geld (niedrige Payout-Schwelle), E8 die Dauerquelle (Gratis-Neustart nach 5 Payouts, FN-Konten enden endgültig) — und nur zwei Firmen zusammen verdoppeln die Funded-Deckel-Grenze, sodass das Budget überhaupt verbaut werden kann (bei A/B liegt es nach ~1 Jahr brach).

**Drei Vorbehalte:** (1) ⚠️ Der E8-Funded-Cap „5" ist NICHT primärquellen-bestätigt (nur Help-Center-Snippet) und ist der bindende Faktor der ganzen Rechnung — vor größeren Käufen schriftlich klären, wie damals die Payout-Caps. (2) Bei ehrlicher Drift entscheidet die Politik über Monate, die Drift über das Ob (12-34 % Zensur in 5 Jahren). (3) Alle Konten handeln dasselbe Buch — Payouts kommen im Rudel, Durststrecken auch.

## Offene Entscheidungen für Max
1. FN Flex 50k kaufen als ersten Slot? (~80 $; vorher 2 Klärfragen per Mail)
2. Zielfunktion offiziell auf „Zeit bis Payout" umstellen (betrifft Hebel 4 + künftige Discovery-Marginals)?
3. Asia-Dir ×2 je nach Gegenprüfungs-Ergebnis ins Next-Week-Buch?
4. `horizon_months=36`-Zensur in `evaluate_v2` (verzerrt 100k/150k-Tiers) — fixen?
5. Rauschmaß in `book_contribution` um Historien-Bootstrap erweitern (unterschätzt Unsicherheit ~25×)?
