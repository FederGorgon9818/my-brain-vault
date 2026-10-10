---
tags:
  - bereich/trading
  - trading/phase-eval
erstellt: 2026-07-07
---
# 🎯 Phase 1 – Eval-Passing (AKTUELLER FOKUS)

⬅️ [[Day Trading]] · ➡️ [[Funded-Phase]] · 🎫 **Arbeitsreihenfolge: [[Ticket-Epics]]**

> [!success] Stand 06.09.2026: FIREFIGHT beendet, Buch handelt live
> Die echte E8 50k Eval laeuft seit dem Kontowechsel am 18.08.2026 unbeaufsichtigt auf der Box, vier Beine + `MaxRiskGuard` sind aktiv. Damit ist der FIREFIGHT-Zustand faktisch seit Wochen vorbei; die Notiz hier hinkte nur hinterher.
> Das Flag `maxlab_watchdog_firefight.flag` auf der Box wurde am 06.09.2026 entfernt (als `.bak` archiviert). Solange es lag, waren **zwei** Alarme stumm: die Datenfrische-Pruefung und der neue Alarm "NT8 laeuft und ist verbunden, aber keine Strategie aktiv". Genau dieser Zustand blieb beim Ausfall vom 05.09. einunddreissig Stunden unbemerkt.
>
> **Wer das Flag wieder setzt, schaltet damit die Ausfallmeldung ab** — also nur bewusst und nur solange die Beine absichtlich aus sind.
>
> *Historisch (10.08.2026): zwei Beine liefen mit falschen Zahlen ([[Strategie-Logbuch]] #075), alles aus bis FIREFIGHT in [[Ticket-Epics]] gruen ist. Die Zahlen weiter unten in dieser Notiz sind aelter als die Bugfixes vom 10.08. und **nicht mehr gueltig**, siehe [[2026-08-10]].*

> [!important] Einziges Ziel dieser Phase
> **Die Prop-Eval bestehen.** Nichts anderes zählt hier. Optimiert wird ausschließlich auf: **hohe Passchance in kürzester Zeit.** Payouts, Profit-Split, Funded-Management = spätere Phase ([[Funded-Phase]]), spielen für die Strategie-Wahl HIER keine Rolle.
>
> **Ziel-Firma: algo-freundlich + EOD-Drawdown** (Tradeify oder MyFundedFutures). **NICHT Apex** (kein Voll-Algo + intraday trailing = härtestes Modell).
>
> *(Überholt seit 18.09.2026, siehe „Aus der CLAUDE.md (05.10.2026)" unten: Das Ziel ist jetzt Zeit bis 50.000 $ Eigenkapital aus Payouts, die Funded-Phase zählt mit, gehandelt wird bei E8, FN und FFN.)*

## Aus der CLAUDE.md (05.10.2026): aktueller Stand und Entscheidungskriterium

Aus den Abschnitten „Aktueller Fokus" und „Stehende Trading-Prinzipien" der CLAUDE.md übernommen, damit sie dort gekürzt werden können.

### Stand

- **Aktuelle Phase: Eval-Passing** (Prop-Eval bestehen, **E8**, nicht Apex). **Die erste ECHTE E8 50k Eval läuft live** (Konto `E61803453048`, handelt unbeaufsichtigt von der Box), dazu FN1/FN2 (FundedNext Flex 50k). Neu seit 05.10.2026: Funded Futures Network STEADY 150K, siehe [[Firm-Regeln je Konto]].
- **Plattform: NinjaTrader 8 / NinjaScript (C#)** auf Tradovate, nicht MultiCharts/PowerLanguage (siehe [[Tech-Stack]]). FFN läuft stattdessen über Rithmic.
- **ZIEL seit 18.09.2026 (Max, präzisiert 21.09.): 50.000 $ Eigenkapital aus gebündelten Prop-Payouts, um ein eigenes Live-Konto (am liebsten 100k) zu eröffnen.** Zielfunktion ist **E[Zeit bis Zielkapital]** (Netto-Payouts minus alle Eval-Käufe), nicht mehr die Passquote je Eval. Die Funded-Phase zählt mit. Laufende Konten laufen weiter, die Frage ist nur, was dazukommt. Rechnung: `engine/tempo_plan.py` (Bestandskonten, Kaufpolitiken, Haushaltsgrenzen, Regime-Spalten).
- **Entschieden (AP204/AP214, Update 05.10.2026):** 1× **E8 Signature 150k** (DD 3.999,90, Preis 333 $) mit **k1** (1 Micro je Bein) und **RiskGuard-Tagesstopp 2.500 $** (05.10. abends von 1.500 angehoben, Nachrechnung am 4er-Buch), Kauf nach der ausstehenden E8-Antwort. **Deckel 2.500 $ Netto-Auslage.** FN 150k erst nach AP205, FN-Größe offen (AP248).
- **Warum k2 vom 24.09. nicht mehr gilt:** k2 galt für das 3-Bein-Buch mit DD 4.500 und alter Vola. Mit 7 Beinen ist k1 schon 7 Micros, und bei heutiger NQ-Vola ist k2 nicht schneller, stirbt aber zehnmal so oft (Quant-Team 04./05.10.). **Hochstufen auf k2 nur per Vola-Regel: 60-Tage-σ des Buchs unter ~400 $ je Micro-Satz.**
- Details: [[Strategie-Logbuch]] #175, [[Daily Notes/2026-09-18]], [[Daily Notes/2026-09-21]], [[Daily Notes/2026-09-24]].
- Nächster Schwerpunkt: [[Alpha-Suche]] (First-Passage-Sizing + Cross-Asset-Signale). Werkzeuge: [[Backtest-Engine]], [[Portfolio-Simulator]], [[Strategie-Logbuch]].

### Das einzige Entscheidungskriterium (Max, 10.08.2026, präzisiert 16.08.2026 / Logbuch #106, Zieländerung 18.09.2026)

Bei JEDER Empfehlung/Entscheidung (Bein rein/raus, Parameter, Firma, Kontogröße, Sizing) zuerst fragen: **Verkürzt oder verlängert es die Zeit bis 50.000 $ Eigenkapital aus Payouts, bei begrenzter Auslage?** Nicht Einzel-Edge, nicht Sharpe, nicht Eleganz. Passquote je Eval und Kosten pro funded Konto bleiben Zwischengrößen, nicht das Ziel.

- Die #106-Warnung gilt weiter als Pflichtkontrolle: ein Zeit-Score belohnt Größe und Nachkauf-Lotterie (**Nulldrift-Test: 88 % davon entstanden bei Edge 0**). Deshalb IMMER mit **Nulldrift-Zwilling** rechnen (unter Edge 0 muss jede Politik 0 % Erreichung zeigen) und die **Auslage p90** mitnennen.
- **Min-Size (1 Kontrakt je Bein) ist als Betriebspunkt nicht mehr gesetzt, Größe wird gerechnet.**
- **Rechnung auf ehrlicher Basis:** aktuelles Buch, gefixte Engine, Intraday-Bust-Check (#077), Block-Bootstrap, Nulldrift-Kontrolle, Letzte-3-Jahre-Spalte plus geschrumpfte Spalte (Shrinkage 0,58). Bei Bein-Selektion nested OOS/Marginal-Test „Buch + 1, nur OOS".
- Positive Edge ist notwendig, nicht hinreichend (Lehre 82).
- **Kernrechnung:** `tempo_plan.py` (Zeit bis Ziel). Es rechnet die Konten unabhängig und ist damit in schwachen Regimen bis Faktor 2 zu optimistisch, bis AP245 den Kalender-Modus einbaut (Vorlage `engine/_scratch_ap204_kal/`). Dazu `eval_plan.evaluate_v2` / `cage_policy_lib.evaluate_v2` (Käfig je Konto), Tiers in `cage_v2_tiers.json`.
- Kriterium und Betriebspunkt im Zusammenhang mit dem Buch: [[Buch-Workflow]], [[Strategie-Logbuch]] #106 und #175.

## 📌 Ehrlicher Stand (07.07.2026)
Von allen Seiten geprüft (3 Objektiv-Läufe + Portfolio + Sizing): **70% in 3 Wochen ist mit den aktuellen Edges nicht erreichbar.** ABER der Firmen-Pivot half stark. Multi-Markt-Buch (5 robuste Zellen, 3 Instrumente):

| Tempo | Apex (intraday) | **EOD-Firma (Tradeify/MFFU)** |
|---|---|---|
| ~3-4 Wochen | 33% | **~49%** |
| ~2 Monate | 40% | **~54%** |
| Decke (langsam) | 68% | **72%** |

→ **Realistischer Plan:** EOD-Firma + schnelles Buch (~49% in ~4 Wochen) + Cheap-Resets = in ~2 Monaten funded, günstig. Parallel weiter **stärkeres Alpha** ([[Alpha-Suche]]).

## 🧰 Werkzeuge
- [[Backtest-Engine]] – lokale ehrliche Engine (real fills, OOS, Prop-MC)
- [[Portfolio-Simulator]] – mehrere Beine auf 1 Apex (Korrelation + kombinierte P(pass))
- [[Strategie-Logbuch]] – jede getestete Strategie + Verdict

## 📊 Detailergebnisse (Historie)
- [[Wochenreport 2026-W32 (03.08-11.08)]] – aktuellster Stand: Sim-Eval bestanden, ehrliche Passquoten (43%/34% intraday), FIREFIGHT, Sim-Abgleich auf Null
- [[Wochenreport 2026-W31 (27.07-31.07)]] – 9 Beine, NetLiq +2,8%, Live-Monitor-Bugfixes
- [[Portfolio-Simulator]] – Kombinationen, Empfehlung `PORTFOLIO_balance`
- [[Refine-Lab-Ergebnisse (apex)]] – 20 Strategien auf Apex-Speed optimiert
- [[Refine-Lab-Ergebnisse (prop)]] · [[Refine-Lab-Ergebnisse]] – Explorer-Läufe
- [[Overnight-Lab-Ergebnisse]] – erster breiter Sweep

## ✅ Aktueller Kandidat für den echten Versuch (Update 21.07.2026)
`PORTFOLIO_optimized` (5 Beine: NQ Momentum + NQ Power-Hour + NQ ORB-Breakout + NQ ORB-Fade + RTY Gap-Fade):
- **EOD-Trailing-Firma: 54-58% in ~43-70 Tagen** (frac 0.22-0.18)
- **Static-DD-Firma (falls verfügbar): 63% in ~45 Tagen** — Firmenwahl = größter Hebel, siehe [[Portfolio-Simulator]]
- |Korr| 0,08 · RoDD 9,2 · 402 Trades/Jahr · Report im Strategy Lab (Portfolio-Tab)

## 🚀 Umsetzung live
→ **[[Live-Setup (Algo auf Prop)]]** — komplette Anleitung: Firmenwahl (MFFU/Tradeify, Algo-Regeln geprüft), Setup-Vergleich (Empfehlung: NinjaTrader 8 + NinjaScript auf Tradovate-Konto), 4-Phasen-Plan (Konto → C#-Port → Sim-Validierung → Eval).
