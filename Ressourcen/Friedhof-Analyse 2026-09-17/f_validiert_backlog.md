Karten mit status Validiert/Backlog: 19 (von 64 gesamt)

## Validiert/Backlog Karten (vollstaendig)

### Cross-Asset / Relative Value  [status=Validiert, family=Relative Value]
- Why: Bewegungen in VIX/Bonds(ZN)/Dollar(DXY)/Sektor-Breadth laufen dem Index intraday voraus (Lead-Lag).
- Result (vollstaendig): VIX-Teil getestet (AP49, 11.08.26, Logbuch #087): spike_rev (VIX-Anstieg gestern >= 12% -> Long open->EOD) ueberlebt OOS auf NQ (Verdict A, OOS PF 1.91) und ES; Short-Gegentest (spike_mom) komplett tot -> Richtungsthese bestaetigt. Klein-N: 170 Trades, ~16/Jahr. Auto-Fit lehnt Buchaufnahme ab (55%/90d vs 55%/96d, corr 0.07) -> Bank. ZN/Bonds, DXY, Sektor-Breadth bleiben DATEN-LUECKE (nicht in QuantPad-Export) -- Karte bei Datenzugang wieder oeffnen.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Mom-lowVIX (Momentum nur bei niedrigem VIX)  [status=Validiert, family=Trend Following]
- Why: Intraday-Momentum laeuft in ruhigen Regimes sauber durch; hoher VIX = Chop zerhackt es.
- Result (vollstaendig): OOS-Edge +10,4%, Sharpe 2,78, EOD-Pass 62%. NICHT das live gebuchte Momentum-Bein (das ist die sig15-Variante ohne VIX-Filter, siehe Intraday-Momentum sig15) -- Status faelschlich als 'Im Buch' gefuehrt, hier korrigiert. VIX-Filter selbst nie gegen das Buch auto-gefittet.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Gap-Continuation (grosse Gaps)  [status=Validiert, family=Trend Following]
- Why: Grosse Gaps sind echte Info-Schocks, die weiterlaufen (kleine fuellen, grosse laufen).
- Result (vollstaendig): OOS +7-9% aber schwach (D-Note), 17/Jahr. Kein Auto-Fit-Log gefunden -- vermutlich vor #050 informell verworfen (zu duenn). Nicht im aktuellen Buch.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### ES-Momentum (adaptiert)  [status=Validiert, family=Trend Following]
- Why: Momentum auch auf ES, per-Instrument getunt. Robust aber schwach: OOS-Edge nur +1,0%, PF 1,07.
- Result (vollstaendig): Robust aber marginal. NICHT ins Buch: korreliert mit NQ-Mom (0,15), senkt RoDD.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### NQ Asian-Levels RTH-Breakout  [status=Validiert, family=Trend Following]
- Why: Asian High/Low als Breakout-Level waehrend der US-Session.
- Result (vollstaendig): Nach Fill-Fix nur noch marginal (OOS +1,2%, PF 1,07). Robust aber duenn. Auto-Fit lehnte ab.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Multi-Day-Kointegrations-Pairs  [status=Backlog, family=Relative Value]
- Why: Klassisches Pairs-Trading (Gatev 11 Prozent p.a.) braucht Multi-Day-Haltezeit.
- Result (vollstaendig): 
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### FOMC-Announcement-Momentum (ES)  [status=Validiert, family=Intraday Bias]
- Why: 14:00-14:15-Reaktion nach dem Fed-Statement setzt sich bis zum Close fort (Repricing-Flow).
- Result (vollstaendig): Edge +13,3, OOS +39 Prozent, PF 1,71 -- aber nur 8 Trades/Jahr. Auto-Fit: abgelehnt (Buch 66/95d vs 66/92d, zu wenig Beitrag). Kombiniert mit OpEx-Momentum als 'Event-Bein' getestet, siehe eigene Karte -- auch das noch zu marginal.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Turn-of-Month Long (McConnell/Xu)  [status=Backlog, family=Intraday Bias]
- Why: Aktienpraemie entsteht am Monatswechsel (Gehalts-/Fonds-Flows). 1926-2005 extrem robust.
- Result (vollstaendig): SPANNENDES MUSTER: In-Sample (2016-22) flach/negativ, OOS (ab 2023) klar positiv (+8 bis +9 Prozent auf NQ/ES!). Effekt scheint WIEDERBELEBT. Nach Protokoll kein Survivor (IS fehlt) -> Watchlist: in 6-12 Monaten mit mehr Daten neu testen.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Event-Bein: FOMC-Post + OpEx-Momentum kombiniert  [status=Validiert, family=Intraday Bias]
- Why: Kombination zweier einzeln zu seltener, aber robuster Klein-N-Edges (FOMC-Post + OpEx-Momentum) auf ~15-20 Trades/Jahr bringen, um die Frequenz-Huerde zu knacken.
- Result (vollstaendig): ES, 108 Trades (~10,7/Jahr), Grade A, Win 55,6% vs Baseline 39,9%, expR +0,182, OOS-Edge +25,3%, OOS-expR +0,310, 7/7 Nachbar-Configs robust. Trotzdem Auto-Fit: 61%/81d -> 61%/82d, zu marginal -- die Frequenz-Verdopplung reicht knapp nicht.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### OpEx-Momentum (solo, alle 4 Instrumente)  [status=Validiert, family=Intraday Bias]
- Why: Am Monats-OpEx laufen Dealer-Hedges der auslaufenden Optionen einseitig ab (Charm-/Gamma-Unwind); faellt die Pinning-Kraft weg, setzt sich die Vormittagsrichtung nachmittags fort.
- Result (vollstaendig): 59 von 87 gewerteten Configs ueberleben ueber alle 4 Instrumente. Beste: NQ e150/t0.3/s0.75 mit OOS PF 3,34, Sharpe 6,9. ABER nur ~6-9 Trades/Jahr -- Auto-Fit lehnt alle 4 Besten korrekt ab (Buch 59%/81d -> 60%/78-83d). Klein-N-Bank, kein Bein solo. Kombinierter Versuch siehe Event-Bein-Karte.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### VWAP-Pullback (Continuation)  [status=Validiert, family=Trend Following]
- Why: Preis pullt zur VWAP zurueck und setzt dann den Trend fort statt zu reverten (SSRN 2730304/5807282 + Insight: Continuation an VWAP).
- Result (vollstaendig): 17/108 Survivors, konzentriert auf NQ(10)/RTY(7), ES/YM tot. Bester NQ_t0.4_z0.15_s0.5: 114 Trades/Jahr, Edge +2,7%, OOS-Edge +6,4%, PF 1,12. Auto-Fit: 61%/81d -> 54%/52d -- tauscht Quote gegen Tempo, nicht aufgenommen.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Overnight-Reversal  [status=Validiert, family=Mean Reversion]
- Why: Market-Maker-Inventar-Mechanismus (SSRN 2730304/5807282): Overnight-Positionierung reverted am naechsten Tag.
- Result (vollstaendig): 9/72 Survivors, NQ(7)/YM(2). Bester NQ_l0.5_c0_eod_s0.75: 70 Trades/Jahr, Edge +3,6%, OOS-Edge +9,6%, OOS-expR +0,147, PF 1,16. Auto-Fit: 61%/81d -> 59%/63d, marginal. Invertierte IS/OOS-Signatur = junger/regime-abhaengiger Effekt, Edge-Decay-Monitor-Pflicht falls doch live genutzt.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Crabel-Stretch (Volatility-Breakout, NR7-Kompression)  [status=Validiert, family=Trend Following]
- Why: Crabel-Klassiker: nach Volatilitaets-Kompression (NR7) folgt ein Breakout mit Reichweite.
- Result (vollstaendig): 18/88 Survivors, massiv NQ-lastig (16 von 18). Bester NQ_k0.3_s0.5_nr1_c120: 30 Trades/Jahr, Win 29%, OOS-expR +0,355, PF 1,23. Auto-Fit: 61%/81d -> 60%/73d, marginal.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Momentum-Selektiv (Kaufman Efficiency-Ratio-Filter)  [status=Validiert, family=Trend Following]
- Why: Kaufman Efficiency Ratio filtert choppy Fenster aus dem bestehenden Momentum-Signal raus -- weniger, bessere Trades statt mehr Trades.
- Result (vollstaendig): 9/16 Survivors, NQ 8/8 robust. NQ_er0.3_s0.75: 83 statt 122 Trades/Jahr, Edge +6,0%, expR +0,168, PF 1,30 (vs 0,125/1,21 Original). IS +6,0%/OOS +6,1% -- zeitstabil, keine Regime-Signatur. Als 10. Zusatz-Bein abgelehnt. REPLACE-TEST v2 (#080, ehrliche Basis: 5-Bein-Buch, gefixte Engine, Intraday-DD): Pass-Delta ueberall MC-Rauschen (-1,2 bis +0,5pp), aber Tage-bis-Pass sinken konsistent, am staerksten bei frac 0.10 (Intraday 86->64d bei gleicher Quote). Verdict: Replace lohnt NUR bei Betriebspunkt frac ~0.10, bei 0.18-0.22 Original behalten. Entscheidung an AP53 gekoppelt, liegt bei Max. Alter 03.08.-Lauf ('klarer Gewinn') gilt nicht mehr.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=True

### Noise-ORB NQ (Zarattini SSRN 4824172)  [status=Validiert, family=Trend Following]
- Why: Paper-Default ohne Tuning: Band = max(Open,PrevClose) ± Sigma(t), Ausbruch aus dem Noise-Band statt fixer Opening-Range.
- Result (vollstaendig): NOISE_ORB_NQ_m1.0: expR +0,094, IS +0,094 praktisch = OOS +0,097 (kein Overfit-Abfall), 9/11 Jahre positiv, Top5 nur 29% Konzentration, ~180 Trades/Jahr. Staerkster ehrlicher ORB-Verwandter auf NQ. Auto-Fit: 57%/86d -> 52%/53d, tauscht Quote gegen Tempo, nicht aufgenommen. Generalisiert NICHT auf RTY/YM/ES (nur NQ).
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### OR_DELTA_BIAS_NQ (Tick-Rule-Delta OR-Fenster 09:30-10:00)  [status=Validiert, family=Intraday Bias]
- Why: Reiner Session-Bias aus dem Tick-Rule-Delta des Opening-Range-Fensters (kein Breakout mehr). Beifang aus der IVB-Filter-Runde.
- Result (vollstaendig): LONG besteht sauber: n=1318, avgR +0,109 R/Trade, 8/10 Jahre positiv, IS +54,2R/793Tr UND OOS +89,1R/525Tr (kein reines OOS-Glueck), Top5 nur 3,6% Konzentration. SHORT verworfen (IS praktisch Null = Regime-Glueck). Portfolio-Whatif als 6. Bein: |corr| bleibt niedrig (0,11), ABER Passquoten-Frontier verbessert sich NICHT messbar (frac 0,14: 49%/49d Basis vs. 48%/44d mit Bein). Max' explizite Entscheidung: No-Go fuer Bein-Aufnahme -- positive Edge ist notwendig, aber nicht hinreichend, wenn der Betriebspunkt nicht steigt. Code bleibt liegen (engine/or_delta.py) fuer ein spaeteres Buch/Sizing-Modell.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### VIX-Spike-Reversion (Vortags-VIX -> Long, NQ)  [status=Validiert, family=Intraday Bias]
- Why: VIX-Spike gestern = Angst-Overshoot; Vol-Risk-Premium/Leverage-Effekt-Literatur: nach grossen Angst-Spikes folgt im Schnitt positive Aktien-Drift am Folgetag (Fear-Reversion). Signal nur aus Vortags-Closes (VIXCLS/FRED), kein Lookahead.
- Result (vollstaendig): AP49 (11.08.26): 8/24 Survivors, alle spike_rev/Long (Gegentest 0/12). Beste: NQ thr 0.12 stop 0.75xATR20 -- Verdict A (100), win 54.1% vs Baseline 43.8%, OOS PF 1.91, $5.771 OOS. ABER Klein-N (170 Trades, 16/Jahr). Auto-Fit: abgelehnt, gleiche Passquote wie Buch (55%), nur 6 Tage schneller -> Bank. Entscheid Max: AP88.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=False, v2/Buch-Marginal-Begriff=False

### Cross-Sectional Momentum (Rank über Futures-Universum: Long Winner / Short Loser)  [status=Backlog, family=Relative Value]
- Why: Jegadeesh/Titman 1993 (Aktien) und Asness/Moskowitz/Pedersen 2013 'Value and Momentum Everywhere' (Index-Futures, Bonds, FX, Rohstoffe): relative Gewinner der letzten 1-12 Monate schlagen relative Verlierer, mit Skip-Month gegen den 1-Monats-Reversal. Erklärung: verzögerte Informationsverarbeitung plus Herding (erst Under-, dann Over-Reaction) und Fonds-Flows, die Winner nachkaufen. Für uns: Rang der Index-Futures (NQ/ES/RTY/YM, später ZN/CL/GC sobald Daten da) nach Return über N Tage, dann Long den stärksten / Short den schwächsten (marktneutral, beide Beine intraday flat bis EOD, kein Overnight wegen Prop-Regeln) ODER nur als Instrument-Auswahl-Overlay für bestehende Momentum-Beine (Rang der Vortags-/Overnight-Returns entscheidet, welches Instrument das Bein heute handelt).
- Result (vollstaendig): Backlog 21.08.2026 (Max' Momentum-Runde, Teil 2 von 3, Theorie in [[Momentum-Theorie (Futures)]]). Datenlage: nur 4 Index-Futures im QuantPad-Export, Cross-Section ist also schmal (N=4), echte Kraft erst mit Bonds/Rohstoffen/FX. Offen vor dem ersten Job: Ranking-Lookback (1d/5d/20d/60d), Skip-Periode, Long-only vs. Long-Short, Vol-Normierung der Returns vor dem Ranking. Verwandt aber anders: Cross-Asset Lead-Lag (VIX-Spike validiert), Cross-Instrument gleiche Familie (getötet, das war Klonen, nicht Ranking).
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=True, v2/Buch-Marginal-Begriff=False

### Way of Dumb: Zwangsflows großer Institutionen (Rebalancing, Vol-Targeting, CTA-Trigger, LETF, Benchmark-Zwang)  [status=Backlog, family=Intraday Bias]
- Why: Große Häuser handeln nach Regeln, die öffentlich bekannt und preisunempfindlich sind. Die 'Dummheit' ist nicht fehlendes Wissen, sondern Regeltreue: sie wissen es und müssen trotzdem. (1) Kalender-Rebalancing von Pensions-/Mischfonds: nach starkem Aktienmonat MUSS zum Monats-/Quartalsende Aktien-Future verkauft werden (in CFTC-Daten sichtbar, Research-Cache 21.08.). (2) Vol-Targeting/Risk-Parity: Vola steigt, Exposure geht mechanisch runter, unabhängig vom Preis. (3) CTA-/Trendfolge-Trigger: bekannte Lookback-Schwellen (50/200-Tage, 12-Monats-Sign) bündeln Flows an den Schwellen. (4) LETF-Rebalancing: Hebel-ETFs kaufen in der Schlussphase in Tagesrichtung nach. (5) Options-Dealer-Hedging (Gamma-Regime). (6) MOC-Imbalance und Futures-Arbitrage ab 15:45 ET. (7) Benchmark-Zwang (Closing-Price-Tracking, Index-Rebalancing-Tage). Edge = Richtung und Zeitfenster des erzwungenen Flows vorab berechnen und davor oder dahinter positioniert sein.
- Result (vollstaendig): Backlog 21.08.2026 (Max' Momentum-Runde, Teil 3 von 3, Theorie in [[Momentum-Theorie (Futures)]]). Schon im Vault: Quartalsende-Flow (getötet), Turn-of-Month (Backlog, OOS wiederbelebt), OpEx-Momentum (validiert, Bank), Pre-FOMC-Drift (getötet), MOC-/Rebalancing-Theorie im Research-Cache (21.08.). Noch NICHT getestet, jede Teilidee ein eigener Discovery-Job mit Why vorab: (a) Vol-Targeting-Deleveraging in den Tagen nach einem Vol-Sprung (Verkaufsdruck; Gegenthese zur validierten VIX-Spike-Reversion, beide gegeneinander laufen lassen), (b) CTA-Schwellen-Nähe: Preis kreuzt 200-Tage- oder 12-Monats-Marke, Continuation intraday, (c) LETF-Rebalancing in den letzten 30 Min an Tagen mit großem Move (Continuation in Tagesrichtung, Kopplung ans Power-Hour-Bein prüfen), (d) Monatsende-Rebalancing als Richtungs-Signal konditional auf die Monats-Performance statt blind nach Kalender.
- Erkennbare Nachrechnung nach 16.08 im Result-Text: Datum-Hinweis=True, v2/Buch-Marginal-Begriff=False


## LIVE_EXTRA in live_finalize.py (Zeilen ~49-73)
Keys: ['VIX_spike_rev_NQ', 'OPEXMOM_NQ', 'EVENT_ES_primary']
Mechanism-Strings: ['NQ · VIX-Spike-Reversion', 'NQ · OpEx-Momentum', 'ES · FOMC-Post + OpEx kombiniert']

## Abgleich: welche Validiert/Backlog-Karten sind NICHT in LIVE_EXTRA
- Cross-Asset / Relative Value [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Mom-lowVIX (Momentum nur bei niedrigem VIX) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Gap-Continuation (grosse Gaps) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- ES-Momentum (adaptiert) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- NQ Asian-Levels RTH-Breakout [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Multi-Day-Kointegrations-Pairs [Backlog]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- FOMC-Announcement-Momentum (ES) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Turn-of-Month Long (McConnell/Xu) [Backlog]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Event-Bein: FOMC-Post + OpEx-Momentum kombiniert [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- OpEx-Momentum (solo, alle 4 Instrumente) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- VWAP-Pullback (Continuation) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Overnight-Reversal [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Crabel-Stretch (Volatility-Breakout, NR7-Kompression) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Momentum-Selektiv (Kaufman Efficiency-Ratio-Filter) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Noise-ORB NQ (Zarattini SSRN 4824172) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- OR_DELTA_BIAS_NQ (Tick-Rule-Delta OR-Fenster 09:30-10:00) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- VIX-Spike-Reversion (Vortags-VIX -> Long, NQ) [Validiert]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Cross-Sectional Momentum (Rank über Futures-Universum: Long Winner / Short Loser) [Backlog]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False
- Way of Dumb: Zwangsflows großer Institutionen (Rebalancing, Vol-Targeting, CTA-Trigger, LETF, Benchmark-Zwang) [Backlog]: in LIVE_EXTRA (Name-Match)=False, (Mechanism-Match)=False