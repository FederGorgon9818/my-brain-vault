---
tags: [trading, prozess, research]
created: 2026-08-28
quelle: https://www.youtube.com/watch?v=TyHTEtArsS4
status: aktiv
---

# Noel T. (SQX-Algotrader): Was wir übernehmen

Aus dem Chart-Fanatics-Interview (85 Min, gesehen 28.08.2026, Claims im [[Research-Cache]]). Noel T. („Ultra Instinct"): ~1 Mio $ Selbstclaim, >150 Algos parallel, StrategyQuant X + MultiCharts, Breakout-Fokus mit ~40 % WR / RR 2.

**Einordnung vorab:** Sein Prozess ist strukturell unsere Pipeline (Massengenerierung + Gates + OOS + MC + Inkubation). Wir sind bei Statistik-Disziplin strenger (Register/Zufallsdecke, Why-Pflicht, Look-ahead-Controls, Buch-Marginal). Interessant ist bei ihm der **Live-Betrieb**: was passiert NACH dem Deploy. Genau da haben wir Lücken.

---

## Übernahme-Kandidaten (priorisiert)

### 1. Bein-Kill-Kriterium (seine Idee, aber bessere Mathematik) ⭐ höchster Nutzen
- **Seine Regel:** Überschreitet der Live-Drawdown eines Algos das 1,5-fache des Backtest-MaxDD, wird er abgeschaltet und läuft auf Sim weiter (nicht gelöscht, kann zurückkommen).
- **Unsere Lücke:** Wir haben KEIN codiertes Abschalt-Kriterium je Bein. Der [[Day Trading|Buch]]-Betrieb läuft unbeaufsichtigt auf der Box, `live-reconciler` vergleicht nur Konto vs. Erwartungsband, aber niemand zieht automatisch die Reißleine je Bein.
- **Quant-Befund (28.08., quant-mathematician):** Die 1,5×-DD-Regel ist die richtige Idee mit schwacher Statistik. DD wächst als Max-Statistik ~sqrt(t), egal ob die Edge lebt; eine feste DD-Schranke erkennt eine TOTE Strategie nach 2 Jahren nur zu ~15 % (False-Positive dabei ~4-6 %). Besser: **sequentieller Drift-Test (Wald/SPRT) auf die kumulierte PnL** (kill wenn cumPnL unter einer Geraden aus mu/sigma des Backtests liegt). Gleiche False-Positive-Rate, etwa **doppelte Erkennungsrate**.
- **Umsetzung:** `mu/sigma` je Bein aus dem Leg-Report in `book_state.json` ablegen, `live-reconciler` prüft täglich die SPRT-Linie je Bein. Bei Bruch: Telegram-Alarm + Ticket, Entscheidung bleibt bei Max. Kein Auto-Abschalten im ersten Schritt.

### 2. Inkubations-Bank (Sim-Track für Fast-Kandidaten)
- **Sein Setup:** Hunderte Strategien laufen dauerhaft auf Sim-Geld mit. Fällt ein Live-Algo aus, ersetzt er ihn durch einen, der sich auf UNGESEHENEN Live-Daten bewährt hat („it worked on unseen data").
- **Unsere Lücke:** Discovery-Kandidaten, die alle Gates bestehen, aber beim Buch-Marginal „neutral" sind, landen im Register/Friedhof und sammeln keine Live-OOS-Evidenz. Bei einem Bein-Ausfall müssten wir frisch suchen statt aus einer bewährten Bank zu greifen.
- **Umsetzung:** `discovery/incubation.json` auf der Box: die Top-N „neutral"-Kandidaten je Familie laufen als Paper-Track mit (nur Signal-Simulation auf neuen Tagesdaten, kein NT8). Wöchentlicher Blick im Rahmen des Next-Week-Tickets. Das ist echtes Out-of-Sample, das keiner mehr wegoptimieren kann.

### 3. MC-Worst-DD (95 %) je Bein als Erwartungsband
- **Sein Punkt:** Der Backtest-DD ist Schönwetter. Im Video wurde aus 13k Backtest-DD nach Reshuffle 34k MC-Worst-DD (Faktor ~2,6). Er sized und beurteilt nur nach der MC-Zahl.
- **Bei uns:** Block-Bootstrap existiert in den Gates und auf Konto-Ebene (`eval_plan`), aber je Bein weisen die Reports kein 95 %-Worst-DD-Band aus. Genau diese Zahl braucht Punkt 1 als saubere Referenz (1,5× Backtest-DD ist gröber als 95 %-MC-DD, beides ausweisen, das strengere gewinnt).
- **Umsetzung:** im Leg-Report (`report.py`/`copilot`) eine Zeile „MC-DD 95 %" je Bein, gespeist aus dem vorhandenen Bootstrap.

### 4. Konfluenz-Sizing (Ensemble-Voting) → GEKLÄRT: für uns gegenstandslos
- **Sein Setup:** Geben 3 unkorrelierte Algos gleichzeitig dasselbe Signal, fährt er automatisch 3× Size, weil die Signalqualität höher sei.
- **Quant-Befund (28.08., quant-mathematician):** Für unser Buch nicht relevant, drei Gründe, jeder allein reicht: (a) Sizing ist bei uns auf 1 Kontrakt quantisiert, die nächste Stufe wäre +100 %; (b) unter der v2-Zielfunktion ([[Strategie-Logbuch]] #106) fällt die Passquote streng monoton in der Größe, Aufstockung schiebt in die falsche Richtung; (c) Funded-Payouts sind gedeckelt, Größe ist dort kein Hebel. Mathematisch ist Konfluenz nur Kelly auf dem Joint-Signal, und die Unkorreliertheit misst unser Korrelations-Gate (#079) schon. Frühestens relevant im Live-Buch mit eigenem Kapital und mehr als 1 Kontrakt Basisgröße. Nicht weiter verfolgen.

## Bewusst NICHT übernehmen
- **SQX-Massengenerierung ohne Register:** „10.000 generieren, 25 überleben" ohne Trial-Register ist exakt die Multiple-Testing-Falle, gegen die unsere Zufallsdecke existiert (#494). Unsere Hypothesen-Bank (Why-Pflicht, ≥10 Implementierungen, Register) bleibt der Weg.
- **Genetische Evolution auf Indikator-Settings:** er nennt es selbst Curve-Fitting und filtert hinterher. Wir filtern vorher (Prämisse + Why).
- **Seine 60 %-Live-Quote als Benchmark:** ohne Register nicht interpretierbar.

## Die zwei gezeigten Setups (Test 28.08.2026)
1. **ES Mean Reversion (Connors-Klassiker):** Long wenn Close > SMA200 und RSI(2) < 20, Exit RSI(2) > 70. Seine Zahlen: 34 % p.a. auf 25k, DD 22 %, WR 77 %, Exposure 25 % (2009-2026).
2. **„Gold Rush":** Gold long jeden Donnerstag wenn RSI < 40, 1× ATR-Stop, Zeit-Exit 3 Tage. Seine Zahlen: 22,6 % p.a., DD 25 %, Exposure 12 %. Gold-Daten haben wir nicht, Test nur als Mechanismus-Proxy auf den Indizes.

**Testergebnis (28.08.2026, ES/NQ/YM/RTY Tagesbars aus 1m-Daten 2016-2026, netto, geprüft von quant-statistician + quant-mathematician + pipeline-auditor):**

1. **ES RSI(2)-MR: Zahlen replizieren, Edge-Aussage hält nicht.** Nominell WR 80 %, PF 2,47, Exposure 23 % (seine Claims: 77 %, 25 %, „34 % p.a."). Aber: (a) auf unserer unadjustierten Serie stammen +56,5k$ von 144k$ aus positiven Roll-Gaps (Carry seit 2023), roll-adjustiert bleibt PF 2,03; (b) gegen die Long-Bias-Nullverteilung (#108, Zufalls-Longs im Uptrend mit gleichen Haltedauern) liegt das Ergebnis nur im 92. Perzentil, p ≈ 0,08, ~40 % des PnL ist reiner Markt-Drift; (c) 2016-2019 ist die Strategie von „einfach long" nicht unterscheidbar, die Edge lebt nur im Hochvola-Regime ab 2020, 2021 allein = 35 % des Gesamt-PnL; (d) der echte Mark-to-Market-DD ist -26,6k$ je Kontrakt (nicht -18,5k auf Closed-Trade-Basis). Geschrumpfter Forward-Erwartungswert laut Statistiker: 500-650 $/Trade, 7-9k$/Jahr je ES-Kontrakt.
2. **Prop-Käfig: endgültig tot.** 61 von 138 Trades reißen intraday den E8-50k-Trailing-DD (2,5k$); sigma je Trade ist das 1,6-fache des ganzen Käfigs. Keine Variante prüfen (#077).
3. **Live-Buch: nur theoretisch interessant.** Nötige Kontogröße ~45-50k$ je Kontrakt (MC-Ruin < 5 % + Overnight-Margin), darauf 19-31 % p.a. in-sample. Bei p ≈ 0,08 gegen die Long-Null ist das aber keine belegte Edge, sondern „Timing schlägt Buy-and-Hold pro Exposure-Einheit". Kein LIVE_EXTRA-Kandidat ohne saubere roll-adjustierte Neuberechnung + echtes OOS.
4. **„Gold Rush"-Proxy auf Indizes: null.** Gepoolt und nach Datum geclustert t = 0,55; der Wochentag ist ein impliziter Trial-Raum (Montag sähe „besser" aus als Donnerstag); der scheinbar starke RTY-Befund war ein Datenartefakt (Fremdkontrakt-Sessions 2017). Gold selbst bleibt ungetestet (keine Daten). Nicht weiterverfolgen.

**Nebenfund Datenqualität (wichtig über dieses Thema hinaus):** Die 1m-Parquets aller Märkte enthalten um jeden Quartals-Roll ganze Tage Fremdkontrakt-Daten (ES z.B. Spread-Preise um -3, RTY negative Preise Sept. 2017); das hat auch den Ratio-Adjust der 1d-Parquets zerstört (in `copilot.py:407` als Symptom bekannt, Root Cause war unbekannt). Reparatur-Task ist angelegt. Dazu drei Pipeline-Gate-Vorschläge des Auditors im Ticket `pipeline-haertung-cvd-funde` ergänzt (Roll-Gap-Gate, Käfig-MAE-Gate, absolute Fremdkontrakt-Erkennung).

**Buch-Lücke beider Setups:** ES-MR scheitert endgültig an der Käfig-Stufe (MAE vs. Trailing-DD, nicht heilbar), Donnerstag-Setup scheitert an Stufe 0 (keine belegte Prämisse). Keines geht in `hypothesis_bank.py`.

Verwandt: [[Discovery-Runner v2]], [[Strategie-Logbuch]], [[Alpha-Suche]], [[Strategie-Familien]]
