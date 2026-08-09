---
tags:
  - bereich/trading
  - trading/logbuch
  - system/archiv
erstellt: 2026-07-29
---
# 📓 Strategie-Logbuch — Archiv #001–#025

⬅️ [[Strategie-Logbuch]]

> [!info] Ausgelagert am 29.07.2026 (Token-Disziplin). Einträge #001–#025 (04.07.–15.07.2026). Alle Kern-Erkenntnisse daraus stehen weiterhin in der Insight-Bank im [[Strategie-Logbuch]].

## #001 — ORB Fast-Retest
- **Datum:** 04.07.2026 · **Instrument:** NQ / ES (1m RTH)
- **Quelle:** Zarattini/Aziz (ORB) + Pineda (Retest), SSRN 4416622 / 6745958
- **Verdict:** ❌ NO-GO
- **Kernzahlen:** Original (Fill-Bug) CAGR 36% / Sharpe 2,0. Nach Fill-Fix OOS: CAGR **-4,8%**, Sharpe -0,36, PF 0,84.
- **Warum:** Fill-Bug erzeugte die ganze Edge (Phantom-Fills). Parameter instabil = Overfitting. Paper-2-Signal real, Umsetzung nicht.
- **Dateien:** [[ORB Fast-Retest Review]], `Quantpad Data/fixed/`

## #002 — Regime-Filtered VWAP Mean Reversion (QuantPad)
- **Datum:** 05.07.2026 · **Instrument:** MNQ / MES (~10,5 J.)
- **Quelle:** [[Mean-Reversion Paper (High-Winrate Fokus)]], via [[QuantPad Brief - VWAP Mean Reversion]]
- **Verdict:** ❌ NO-GO
- **Kernzahlen:** OOS netto Win 42%, Exp -0,224R, PF 0,66, Sharpe -2,6. **P(Prop-Pass) 0%.** 0/624 Sweep-Configs positiv.
- **Warum:** VWAP-Z-Stretch zeigt CONTINUATION statt Reversion. Win 42% < Random-Walk-Baseline 59%.

## #003 — VWAP Z-Stretch beide Richtungen (lokale Engine)
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH, [[Backtest-Engine]]
- **Verdict:** ❌ NO-GO (beide Richtungen)
- **Kernzahlen:** Reversion 56% (Baseline 60% → -4%). Continuation brutto nur +0,1% über Baseline = Rauschen.
- **Wert:** Engine unabhängig validiert (reproduziert QuantPad + ehrlicher).

## #004 — VWAP Continuation / Intraday Momentum (Grid-Studie)
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH, [[Backtest-Engine]] + [[Intraday Momentum Paper]]
- **Verdict:** ❌ NO-GO netto (aber echte Edge sichtbar)
- **Kernzahlen:** 0/30 Configs netto positiv. Beste: Trend-gefiltert RR2 (Stop1/Target2): Win 34,9% vs Baseline 33,3% = **+1,6% echte Edge**, netto -0,168R (Kosten fressen sie). P(pass) bis 14%. Lab: `NQ_momentum_trend_RR2`.
- **Warum wertvoll:** Momentum real & messbar, deckt sich mit Gao/Han/Zhou (stärker an Trend-/Vola-/News-Tagen). Trend-Filter hebt P(pass) 2%→16%.
- **Fix-Richtung:** weniger, GRÖSSERE Trades (Frequenz runter → Kostendrag runter).

## #005 — VWAP Holy Grail (Zarattini, vwap_trend)
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH, [[Backtest-Engine]] + [[Prop-Eval-Passing (Fokus)]]
- **Quelle:** Zarattini/Aziz "VWAP Holy Grail" (SSRN 4631351)
- **Verdict:** ❌ NO-GO auf NQ
- **Kernzahlen:** Win 13,5% vs Breakeven 15,8%, expR -0,026, PF 0,83, Sharpe **-1,5**, netto negativ. (Paper behauptete 9,4% DD / Sharpe 2,1 — aber auf QQQ/TQQQ, gehebelter ETF, andere Ära.)
- **Warum:** Long über VWAP / short darunter (Flip am Cross) reproduziert auf NQ-Futures mit ehrlichen Fills nicht. Meine Umsetzung ist eine faire Rekonstruktion; exaktes Paper könnte abweichen (bräuchte PDF).
- **Nebenbei:** Fill-realistisch getestet, Eval-Optimizer + PFPL-Kostenmodell dabei. Lab: `NQ_vwap_holygrail_stop6.0_none`.

## #006 — Overnight-Intraday Reversal ⭐ erster Lichtblick
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH, [[Backtest-Engine]]
- **Quelle:** SSRN 5807282 / 2730304 (Overnight-Return sagt Reversal voraus)
- **Verdict:** ⚠️ SCHWACH, aber **erste positive Netto-Edge**
- **Kernzahlen:** Beste Config (Gap ≥0,5% faden, 60 Min halten): Win 48,6% vs Baseline 48,1% = **+0,4% Edge**, expR **+0,005**, PF 1,02, Sharpe +0,10, **+$6.316/micro netto.** P(pass) Apex 31% @ 3 Micro, EV +$259. **MaxDD nur $3-7k** (niedrig = gut fürs Eval).
- **Warum wertvoll:** Erstes Signal mit echter Edge + niedrigem DD. Ganz anderer Ansatz (Overnight-Gap statt VWAP). Ausbaufähig.
- **Fix-Richtung:** Signal schärfen (Gap-Threshold, Exit, Vola-Filter, evtl. mehrere Index-Instrumente), um Edge & P(pass) zu heben. Lab: `NQ_overnight_reversal_thr0.005_h60`.

## #007 — Gefilterte ORB (Trend + VWAP + Volumen) 🏆 bisher bester
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH · [[Backtest-Engine]] + [[ORB Master-Synthese (Eval-Fokus)]]
- **Quelle:** ORB-Literatur-Synthese (Zarattini 4416622, Chuk 6355218 Filter-Stack, u.a.)
- **Verdict:** ✅ **A-Note (100), überlebt Out-of-Sample.** ⚠️ nur NQ.
- **Kernzahlen (S4 = Trend+VWAP+Vol, 269 Trades):**
  - EOD-Target: expR +0,281, PF 1,37, Sharpe **+1,68**, MaxDD nur **-$2.178**. **OOS 2021-26: Sharpe +1,19, edge +4,1%** (hält!).
  - 1R-Target (High-Win): Win **60,6%**, Sharpe **+2,35**, MaxDD **-$716**. **OOS: Win 57,4%, Sharpe +1,85.**
  - **P(pass): Apex 61,1%, Topstep 54%** @ 3-5 Micro. EV/Account bis **+$3.816**. Nah an der 70%-Schwelle!
- **Der Schlüssel:** **Volumen-Filter** (Breakout-Bar > 1,3× OR-Volumen) → nur A-Setups, 2685→269 Trades, Win springt. Deckt sich mit Chuk (Filter 46,8%→65,4%).
- **⚠️ Caveat:** funktioniert NUR auf NQ (ES/YM/RTY negativ). Plausibel (Nasdaq trendigster Index) ODER Warnsignal. Braucht Walk-Forward + Parameter-Sensitivität zum Härten.
- **Lab:** `NQ_ORB_S4_tgtNone`, `NQ_ORB_S4_1R_highwin`.

### #007 Härtung (06.07.2026)
- **Walk-Forward** (3y IS → 1y OOS, Config je Fenster neu gewählt): gestitchte OOS **expR +0,138, PF 1,24, edge +5,3%**. Überlebt → echte Edge. Das ist die *ehrliche* Erwartung.
- **Parameter-Sensitivität:** sauberes **Plateau**, höherer Vol-Filter → monoton höhere Win-Rate. Keine Messerschneide.
- **70%-Marke geknackt:** OR15/Vol1.7 (67% Win) → **Topstep P(pass) 82%, Apex 88%**, EV bis +$13.892.
- **⚠️ ABER (gesunde Zwischenbilanz):** diese Top-Config macht nur **~7 Trades/Jahr** → passt LANGSAM (Wochen-Monate, gegen Fast-Pass-Ziel) + nur **76 Trades = dünnes Sample** (teils Glück möglich). Praktischer Sweet-Spot: Vol ~1,3-1,5, ~20-40 Trades/Jahr, P(pass) 55-65%, robuster + schneller. Optimizer rechnet jetzt Passzeit in **Kalendertagen**.
- **Lab-Vergleich:** `NQ_ORB_maxwin_or15_vol1.7` (88% aber langsam), `NQ_ORB_balanced_or30_vol1.7` (51%, A), `NQ_ORB_fast_or30_vol1.3` (38%, schnell), `NQ_ORB_S4_1R_highwin` (61%).
- **Nächste:** Balance-Config härten (evtl. NR7-Filter für Win↑ ohne Frequenz-Verlust), gewählte Config OOS-verifizieren, dann Forward-Test.

### #007 Passzeit-Wahrheit + NR7 (06.07.2026)
Neue **Passzeit-Statistik** (Median-Kalendertage bis Pass) eingebaut. Sie entlarvt das reine P(pass)-Denken:

| Config | Note | Win | Trades/Jahr | P(pass) | **Median Tage** |
|---|---|---|---|---|---|
| maxwin or15/vol1.7 | A | 67% | 7,4 | **88%** | **916 (2,5 J!)** |
| **sweet or15/vol1.3** | **A** | **61%** | **26** | **61%** | **275 (~9 Mon)** |
| balanced or30/vol1.7 | A | 61% | 23 | 51% | 306 |
| nr7 or30/vol1.3 | A | 64% | 7,7 | 48% | 1042 |
| fast or30/vol1.3 | C | 57% | 50 | 38% | 140 (~4,6 Mon) |

- **Die 88%-Config ist eine Illusion:** sie passt nur, weil die Sim ihr 2,5 Jahre Zeit gibt. Real wartet keiner so lange. Hohe P(pass) ohne Passzeit = wertlos.
- **NR7 getestet:** hebt Win 57→64% & Sharpe auf 3,7, ABER Frequenz stürzt auf ~8/Jahr → P(pass) SINKT auf 48% (zu wenig Trades im Challenge-Fenster) und Median 1042 Tage. **NR7 ist fürs Eval-Ziel raus.** (Wäre gut für ein diskretionäres High-Quality-Setup, nicht für schnelles Passen.)
- **Kern-Erkenntnis:** gefilterte ORB auf Micros ist fundamental **langsam** (Frequenz × Micro-Size). Schneller passen = mehr Frequenz ODER mehr Size (mehr Risiko). Die drei Hebel P(pass) / Kalender-Speed / Frequenz stehen im Dreieck.
- **Bester ehrlicher Kompromiss aktuell: `NQ_ORB_sweet_or15_vol1.3`** (A, 61% Pass, ~9 Mon, robustes 269-Trade-Sample). `fast` wenn Speed > Sicherheit (4,6 Mon, aber nur 38%).
- **Lab-Upgrade:** Vergleichstabelle (alle Strategien nebeneinander, sortierbar), ⤢ = Report in eigenem Fenster rausziehen (in Windows frei andocken), Passzeit-Kurve pro Report.
- **Nächster echter Hebel für Speed:** Size-Optimierung (schneller $3k bei kontrolliertem Trailing-DD) oder eine höher-frequente Strategie kombinieren. ORB-Edge bleibt NQ-spezifisch.

## #008 — Intraday TS Reversal → als Momentum entlarvt 🔄 zweitbester Edge
- **Datum:** 06.07.2026 · **Instrument:** NQ 1m RTH · [[Backtest-Engine]] (`mode="ts_reversal"`)
- **Quelle:** Intraday Time-Series Reversal (SSRN 5807282), Gegentest zu Gao/Han/Zhou Intraday Momentum (2552752)
- **Verdict:** Reversal ❌ NO-GO · **Momentum-Spiegel ✅ A-Note, OOS-robust.** ⚠️ nur NQ, schwacher Standalone-Passer.
- **Der Weg:** frühen Tages-Move (15-Min-Fenster ab Open) faden = **edge -6%, PF <1, Sharpe negativ, MaxDD -20 bis -27k.** Bestätigt Insight-Regel #1 (NQ = continuation). **Also Richtung gedreht → den Move weiterlaufen lassen (Momentum).**
- **Kernzahlen Champion (sig15 / thr0.003 / stop1.5×Range / EOD, 798 Trades = ~76/J):**
  - Win 52% vs Baseline 44% = **edge +7,9%**, expR **+0,124**, PF 1,37, **Sharpe +2,03**, **MaxDD nur -$5.903**.
  - **Temporal-Split (Killer-Test):** IS 2016-20 edge +6,6% → **OOS 2021-26 edge +8,8%, Sharpe 2,28** (OOS STÄRKER = kein Overfitting).
  - **Walk-Forward stitched OOS:** edge +6,3%, PF 1,29. Hält.
  - **Cross-Instrument:** NQ +7,9% · ES +1,7% (schwach) · YM -0,6% · RTY -3,7%. NQ-zentriert wie ORB.
- **⚠️ Standalone-Prop-Schwäche:** P(pass) nur **33-42%** @ 1-2 Micro, trotz Sharpe 2,0. Grund: RR>1-Momentum mit choppiger Equity lässt sich am engen Trailing-DD **nicht hochskalieren** (Optimizer bleibt bei 1-2 Micro). Stop-Tuning (0,75-1,5) & Targets ändern das kaum.
- **Wert:** echter zweiter validierter Edge, **3-5× höhere Frequenz als ORB** (~76-122/J), niedriger DD → idealer **Frequenz-/Speed-Lieferant fürs Portfolio-Bein**, nicht als Solo-Passer.
- **Lab:** `NQ_MOM_champion_sig15_thr3_stop1.5` (Sharpe-König), `NQ_MOM_maxfreq_sig15_thr2_stop1.5` (122/J), `NQ_MOM_propbest_stop0.75` (Apex 42%).
- **Nächste:** ORB-vs-Momentum-**Korrelation** messen → wenn dekorreliert, **kombinierte Equity + P(pass)** simulieren (Portfolio-Bein).

---

## #009 — Auto-Explorer + 3 Objektiv-Läufe (07.07.2026)
- **Was:** `refine.py` gebaut = Explorer (breit denken) + OOS-gated Verschärfung (kein Curve-Fitting). Neue Engine-Modi: ORB-Fade (`orb_side`), Gap-Momentum (`on_side`), Power-Hour (`last_hour`). Drei automatische Läufe hintereinander (expR → prop → apex-speed über 20 Strategien).
- **Kern-Erkenntnis (harte Grenze):** Das Ideal **70% Pass + 3 Wochen + 10 Trades ist mit EINER Strategie unmöglich.** Frequenz-vs-Passquote-Frontier auf NQ-Micros:
  - expR-Ziel → ORB nr7+cutoff60: **77% Pass, aber 14 Trades/J (Monate).**
  - prop-Ziel → ORB vol1.3+cutoff90+stop0.4: **56% Pass, 59/J (~3-4 Wochen).** ← bester Einzel-Kompromiss.
  - apex-Ziel (21-Tage) → Momentum roh: **39% Pass, 122/J**; ORB cutoff60: 36%, **214/J**.
- **„10 Trades bis Pass bei 70%" mathematisch unrealistisch** (bräuchte Mega-Size oder Mega-Edge). Realistisch: ~20-40 Trades in 3 Wochen via Portfolio.
- **Neu entdeckt:** ORB-Fade + NR7 wird robust (40/J); ES/YM ORB bekommt mit NR7 Puls; Power-Hour-Momentum roh leicht positiv, hochfrequent.
- **Fazit:** Der Weg zu „70% schnell" ist das **Portfolio** (mehrere hochfreq. dekorrelierte Beine auf 1 Apex), nicht die perfekte Einzelstrategie.
- **Ergebnisse:** [[Bereiche/Refine-Lab-Ergebnisse.md|expR]], `Refine-Lab-Ergebnisse (prop)`, `Refine-Lab-Ergebnisse (apex)` + Reports `REFINE*_` im Lab.
- **Nächste:** kombinierte Equity + Korrelation + kombinierte P(pass) der Top-Fast-Beine simulieren (Portfolio-Prop-Assistant).

## #010 — Portfolio-Simulator (07.07.2026)
- **Gebaut:** `portfolio.py` = mehrere Beine auf 1 Apex, echte Kalendertage resampled (Korrelation bleibt erhalten), Trailing-DD kombiniert, Size-Suche, Kombi-Ranking. Report `PORTFOLIO_balance` im Lab, Details [[Bereiche/Portfolio-Simulator.md]].
- **Korrelation:** Beine echt dekorreliert (|Korr| ≤ 0,23; ORB-fade-NR7 negativ zu ORB-breakout & Momentum). Portfolio-Konzept strukturell bestätigt.
- **Aber ehrlich:** Diversifikation glättet, erzeugt aber **keine Edge**. Max Apex-Passquote: ORB solo **61%** (langsam), ORB+ORB-fade **53% in ~77 Tagen** (bester Kompromiss), 5 Beine nur 38% (aber ~26 Tage).
- **Neue Regel (Insight #8):** **Qualität > Quantität** im Portfolio. Schwache Beine (expR < 0,05: PowerHour, Overnight) **verwässern** und senken die Passquote. Zwei starke dekorrelierte Beine schlagen fünf mittelmäßige.
- **Endgültiges Fazit:** **70% in 3 Wochen ist mit den aktuellen Edges nicht erreichbar** (bewiesen über 3 Objektiv-Läufe + Portfolio). Realistisch: ~53-61% Pass. Weg nach oben = stärkeres Alpha, nicht mehr Kombination.

## #011 — First-Passage-Sizing (Hebel 1, 07.07.2026)
- **Gebaut:** `sizing.py` = Trade-Level-Apex-Sim mit dynamischem Sizing (Apex-Floor lockt bei Breakeven, sobald +2.500$ Cushion). Schemata: flat, cushion_frac (Bruchteil des Cushions riskieren), sprint_coast (groß bis Lock, dann klein).
- **Ehrliches Ergebnis:** **Sizing hebt die Passquote NICHT** (Gambler's-Ruin-Theorie: bei positiver Edge maximieren kleine Einsätze P(pass), aber langsam). Flat/klein ist immer der Passquoten-König.
- **ABER:** dynamisches Sizing gibt eine **viel bessere Speed↔Pass-Kurve** als flat. Bester Regler = `cushion_frac`.
  - Portfolio ORB+ORB-fade: flat 66% @ ~222 Tage → **cushion_frac 0,10: 62% @ ~111 Tage** (halbe Zeit, -4% Pass) → cushion_frac 0,20: 45% @ ~33 Tage.
  - Momentum: sprint 10→1 = 39% @ **~10 Tage** (schnellster Pass, aber niedrig).
- **Bestätigt Insight #6:** eng-riskante Strategien (ORB ~28$/Micro) skalieren viel besser als weit-riskante (Momentum ~100$/Micro → nur N=1).
- **Fazit:** Die **Passquoten-Decke (~65-66%) ist durch die EDGE gesetzt, nicht durchs Sizing.** Sizing = besserer Regler, kein Free Lunch. → Um die ganze Frontier zu heben, brauchen wir echtes neues **Alpha** (Hebel 2: Cross-Asset). Praktisch nutzen: `cushion_frac ~0,10` als Sizing-Schema.

## #012 — VIX-Regime-Filter ⭐ erster Ceiling-Heber (07.07.2026)
- **Daten:** VIX täglich von FRED (`VIXCLS`, 1990-2026) in die Engine geholt. Gate nutzt **Vortages-VIX** (kein Look-Ahead), relativ (VIX vs eigener Rolling-Median) oder absolut. Modi: ORB/Reversal/Overnight.
- **Getestet:** ORB nur bei hohem VIX, Fade nur bei niedrigem (Praktiker-Heuristik) → **nur marginal** (ORB abs≥16: Apex 61→64% aber halbe Frequenz; Fade low: 49→51%).
- **⭐ Der echte Fund (widerspricht der Heuristik):** **Momentum + NIEDRIGER VIX** ist stark. NQ-Intraday-Momentum läuft in ruhigen Regimes, nicht im High-VIX-Chop.
  - Apex P(pass) **42% → 58%** (@ 2 Micro, EV +2.861$), Note A.
  - Edge FULL +6,7% → **+9,0%**; **OOS 2021-26 +7,4% → +10,4%, Sharpe +2,04 → +2,78** (OOS stärker = robust).
  - Kosten: Frequenz 76 → 33/Jahr (halbiert, aber Qualität rauf).
- **Erkenntnis (Insight #9):** Regime-Filter mit ECHTEN Daten (VIX) kann die Passquoten-Decke heben, nicht nur die Speed-Kurve. Und: Richtung immer per Daten prüfen, nicht per Heuristik (Momentum mag LOW VIX, nicht High).
- **Lab:** `NQ_MOM_lowVIX`. Nächste: als Bein ins Portfolio + weitere Configs mit VIX-Gate durch den Refiner jagen.

## #013 — Firmen-Pivot: weg von Apex → Algo + EOD-Drawdown ⭐ (07.07.2026)
- **Grund:** Apex erlaubt kein Voll-Algo (und intraday trailing = härtestes Modell). Wir zielen ab jetzt auf **algo-freundliche Firmen mit End-of-Day-Drawdown**.
- **Firmen (recherchiert):** **Tradeify** (voll automatisiert erlaubt, eigener Bot + Disclosure, **EOD-Drawdown**) und **MyFundedFutures** (Algo seit 07/2025, kein HFT, **EOD-Eval**) = Top-Ziele. TopStep/Alpha/FundedNext auch EOD, aber TopStep schränkt Voll-Automation auf Funded ein.
- **EOD- vs Intraday-Drawdown getestet (Multi-Markt-Buch, 5 Zellen):**
  | Tempo | Intraday | **EOD** |
  |---|---|---|
  | ~3 Wo | 31% | **45%** |
  | ~4 Wo | 33% | **49%** |
  | ~2 Mon | 40% | **54%** |
  | Decke | 68% | **72%** |
- **Erkenntnis (Insight #10):** Die Firmen-/Regel-Wahl ist ein ebenso großer Hebel wie die Strategie. **EOD-Drawdown = +12-15 Punkte Passquote gratis**, weil Intraday-Dips nicht mehr zählen. Wir haben die ganze Zeit gegen das schwerste Modell (Apex intraday) optimiert.
- **Realistischer Plan:** Buch @ size 5-6 → **~45-49% in ~3-4 Wochen** auf EOD-Firma + Cheap-Resets = in ~2 Monaten funded, günstig. Der 70%-One-Shot bleibt unrealistisch, aber DAS ist machbar.
- **Nächste:** EOD-Modell + Tradeify/MFFU-Regeln fest in `copilot`/Lab einbauen; Buch als echte Config finalisieren.

## #014 — EOD-Modell fest im Lab (07.07.2026)
- **Gebaut:** `prop_assistant` kann jetzt `dd_mode="intraday"|"eod"`. Jeder Report zeigt **beide nebeneinander** (Eval-Optimizer-Karte, Prop-Tabelle, P(pass)-vs-Size-Chart). Meta hat `best_prop_pass` (EOD) + `best_prop_pass_intraday`.
- **Alle 35 positiven Strategien neu gerechnet.** EOD hebt jede:
  | Config | intraday | EOD |
  |---|---|---|
  | ORB-sweet | 61% | **73%** |
  | ORB-maxwin | 88% | **94%** |
  | Mom-lowVIX | 58% | **62%** |
  | Mom-champion | 37% | **51%** |
- Compare-View im Lab zeigt jetzt die EOD-Zahlen (Ziel-Firmentyp).

## #016 — Gap-Fill (Research + Build) 🕳️ (07.07.2026)
- **Recherche:** 6 Quellen inkl. **MNQ-Falsifikations-Paper** (Mesfin, arXiv 2605.04004). Details: [[Gap-Fill Research (Synthese)]].
- **Modus `gap` gebaut** (H1 Fade kleiner Gaps, H2 Continuation großer Gaps, ATR-Buckets, erste-Bar-Bestätigung, Wochentag).
- **H1 Gap-Fade: ❌ toter Verlierer** in jedem Bucket (edge -14% bis -36%, OOS negativ). Bestätigt Paper + unsere Insight #1 (NQ = continuation, nicht reversion). Endgültig abgehakt.
- **H2 Gap-Continuation: ⚠️ schwach positiv, OOS-robust** (edge +2,8%, **OOS +7-9%**, expR +0,036, Sharpe 0,77, 17/J, EOD-Apex 52%). Genuin anderer Mechanismus (Overnight-Gap), aber **D-Note** standalone. Lab: `NQ_GAP_cont`.
- **Ins Buch getestet:** hebt die Passquote NICHT (Buch bleibt EOD ~52% @ ~2 Mon), fügt nur etwas Frequenz/Speed dazu. Kein Game-Changer.
- **Große Erkenntnis (Insight #11):** Das Falsifikations-Paper testete **14 OHLCV-Signal-Familien** auf MNQ, fast alle scheitern. **Wir haben den OHLCV-Edge-Raum auf dem Index praktisch ausgeschöpft** (~50-55% Pass auf EOD-Firma ist die Decke). Für echt stärkere Edge braucht es **andere Daten** (Order-Flow/L2, Cross-Asset), nicht mehr OHLCV-Strategien.

## #017 — Video-Analyse "Prop Farming / Hedge" (Blue Edge) ⚠️ (14.07.2026)
- **Video:** "Best Prop Firm Trading Strategy | Make Money Even When You Fail" (Blue Edge Financial). Kein technisches Signal, sondern **Challenge-Hedging** ("Titan Hedge"): Challenge mit Gegenposition absichern → beim Fail den Fee über den Hedge zurückholen.
- **Mathe programmiert & validiert (`prop_hedge_sim.py`):** Im Vakuum stimmt es, fair gehedged ist es **+EV (~+700$/Zyklus)**, weil target/DD sich raushebt und nur „P(pass) × Funded-Wert − Fee" übrig bleibt. Video hat mathematisch recht.
- **⛔ Der Haken (K.O.-Kriterium):** Cross-Account-Hedging ist die **am universellsten VERBOTENE** Prop-Praxis. Automatische Erkennung (IP, Device, Zahlungsmethode, Execution-Timing, Positions-Korrelation) → **Accounts gelöscht, Gewinne rückgängig, permanenter Bann.** Break-even bei ~58% Detection; real ist Detection quasi sicher → **echtes EV stark negativ.** Würde unsere Tradeify/MFFU-Accounts sofort killen.
- **Verdict:** Finger weg. Verkauftes „Guaranteed-Pass"-Schema, ToS-Bruch. **Einziger legitimer Take:** die Farming-/Portfolio-Denke (viele Versuche, Wahrscheinlichkeiten, Cheap-Resets) — die haben wir eh schon, nur LEGAL mit echter Edge.
- **Research (seriöse Theorie):** Prop-Challenge = **Double-Barrier-First-Passage-Problem**; optimales Setzen unter Drawdown-Constraint = **dynamischer fractional-Kelly** (Grossman-Zhou 1993, Cvitanić-Karatzas 1994, Cherny-Obłój 2011) = genau unser **cushion_frac-Sizing** → akademisch bestätigt. „Drawdown Control with Restart Mechanism" (arXiv 2303.02613) stützt den Cheap-Reset-Plan.

## #018 — Strategie-Anatomie ins Lab (14.07.2026)
- **Auslöser:** Video Matty Koni ("Institutional Approach"). Jede Strategie = Entry + Stop + Take-Profit + Emergency(Zeit-Exit) + Sizing + **WHY**.
- **Recherche (intensiv):** Why = strukturelle (Order-Flow/Liquidität) + verhaltensbasierte Edges; Lopez de Prado: ohne kausale These bricht alles zusammen. Sizing = nach dem Stop der stärkste Hebel (Van Tharp), fractional-Kelly/Optimal-f = unser cushion_frac. Emergency = Triple-Barrier (Lopez de Prado). Details: [[Strategie-Anatomie (Framework)]].
- **Gebaut:** `engine/anatomy.py` (kindgerechte Beschreibung je Modus) + Report-Sektion „🧩 Strategie-Anatomie" ganz oben in JEDEM Lab-Report: Typ, Was, 1-Einstieg, 2-Stop, 3-Ziel, 4-Notausgang, 5-Sizing, ⭐WHY + Quelle. Alle 37 Reports neu generiert.

## #019 — Simplex beats Komplex + 5 Strategie-Familien (14.07.2026)
- **Simplex beats Komplex** als stehende Regel verankert (CLAUDE.md + [[Simplex beats Komplex]]). Herkunft: Occam → Taleb (Komplexität=Fragilität) → Pardo („genug Parameter fitten jedes Rauschen") → Lopez de Prado. Meine Meinung: voll zugestimmt als Default, aber Komplexität erlaubt WENN sie sich OOS verdient (Einstein: so einfach wie möglich, nicht einfacher). Belegt durch unsere eigenen über-gefilterten Fragil-Configs.
- **Implementiert überall:** jeder Lab-Report hat jetzt in der Anatomie eine **Komplexitäts-Zeile** (zählt Regeln, bewertet einfach/mittel/komplex-fragil). Explorer hat eh schon OOS-Gate + Komplexitäts-Cap.
- **5 Familien** definiert ([[Strategie-Familien]]) + jede Strategie eingeordnet (Badge im Report): **Trend Following** (ORB-Breakout, Momentum, Gap-Cont), **Mean Reversion** (Fades, Overnight, VWAP-Rev), **Intraday Bias** (Power-Hour), **Swing** (leer→Live), **Relative Value** (leer→Cross-Asset, nächstes Alpha-Ziel).
- Die zwei leeren Familien = Roadmap. Alle Reports neu generiert.

## #020 — Standard-ORB + Lab-Ausbau (14.07.2026)
- **Standard-ORB** (`mode="orb_std"`, Matty Koni Lesson 20): 30-Min-Range, Einstieg auf erste 5-Min-CLOSE jenseits der Range, Stop = Gegenseite, Ziel 1×R, flat 14:00. Ehrlich: **pur Breakeven** (Full Win 50,4%, Edge +0,1%, F-Note; OOS +2,2%). Bestätigt: simple Hypothese ist robust, Edge kommt erst durch Struktur+Why. Lab: `NQ_ORB_standard`.
- **Neue KPIs** in jedem Report: **Netto-Profit (gesamt)**, **Ø Gewinn/Trade**, **Ø Verlust/Trade** (in $/Micro), **Return on Drawdown** (RoMaD = Profit ÷ Max-DD, ≥2 gut; Quelle recherchiert).
- **Layout Vollbild-tauglich:** Equity in **2 Hälften** nebeneinander (nicht mehr flach gestreckt); Monte-Carlo als **2 Sims nebeneinander**: 🔀 Reshuffle (gleiche Trades, zufällige Reihenfolge → Reihenfolge-/DD-Risiko) + 🎲 Bootstrap (mit Zurücklegen → Ergebnis-Bandbreite).
- **Order-Flow-Export** komplett vorbereitet (`export_orderflow.py`, alle 4 Instrumente, Trades→Delta/CVD + Spread, resumierbar, NQ zuerst) → speichert nach `D:\trading-data\orderflow`.

## #021 — Order-Flow getestet ❌ (kein Edge auf Minuten-Ebene) (15.07.2026)
- **Daten:** NQ Order-Flow (Trades mit Aggressor-Seite → Minuten Delta/CVD/Buy/Sell), 2021-2025, 472k Minuten, sauber, aus QuantPad auf D: gezogen.
- **Predictive-Test (roh):** Delta/CVD → Zukunfts-Rendite (1-30 Min): corr **0,001-0,008** (praktisch null), Spreads 0-0,7 bps (< Kosten), nicht monoton. Auch Extremwerte (Absorption) ~0, Divergenz ~0. **Standalone keine Edge.**
- **Filter-Test (ORB-Bestätigung):** Erst SPEKTAKULÄR (Delta bestätigt Ausbruch → expR +0,012, dagegen -0,27, sauber monoton). **ABER = Look-Ahead**: Delta der Einstiegs-Minute = dieselbe Info wie die Preisbewegung der Minute (Preis steigt WEIL ins Ask gekauft wird). Mit Delta VOR dem Einstieg: **Edge komplett weg** (Quintile ~Breakeven, nicht monoton).
- **Ehrliches Fazit (Insight #12):** Minuten-aggregierter Order-Flow trägt auf NQ **keine handelbare Info** — Delta und Preis bewegen sich gleichzeitig, kein Vorlauf. Die echte institutionelle OF-Edge sitzt auf **Sub-Sekunden-/L2-Queue-Ebene**, die wir weder haben noch bei Retail-Latenz nutzen könnten. Die „Order-Flow-Gurus" verkaufen großteils Look-Ahead-Illusion.
- **Konsequenz:** ES/YM/RTY Order-Flow NICHT ziehen (spart ~20 Läufe). OHLCV + Minuten-OF auf dem Index sind ausgereizt. Nächste echte Alpha-Richtung = **Cross-Asset / Relative Value** (VIX lief schon, dazu Bonds/DXY/Breadth) ODER den funktionierenden Plan (Buch + EOD-Firma + Cheap-Resets) live gehen.

## #022 — Order-Flow Research + VPIN gebaut (15.07.2026)
- **Recherche** (Papers wo OF predictive ist): OFI (Cont/Kukanov/Stoikov), Multi-Level-OFI (Oxford), Deep-LOB (2024), VPIN (Easley/LdP/O'Hara). Muster: Richtungs-Edge nur auf **Sekunden + L2**, für uns nicht erreichbar. Details: [[Order-Flow Predictive Research]].
- **VPIN gebaut** (aus unseren Buy/Sell-Volumen, Volumen-Clock, kein Look-Ahead) = Order-Flow-Toxizität/Vola-Regime, NICHT Richtung.
- **Korrelation:** VPIN↔VIX -0,32, VPIN↔realVola -0,21 → distinkt von VIX, aber schwach.
- **VPIN als Momentum-Filter:** Quintile nicht monoton, **kein Edge** (kleines Sample). Per Simplex NICHT ins Lab.
- **Konsequenz:** Order-Flow-Track auf unserer Auflösung ausgereizt. Nächster echter Hebel: **Cross-Asset / Relative Value** (VIX lief schon).

## #023 — Score-Transparenz + Book-Sizing OOS-validiert (15.07.2026)
- **Score-Aufschlüsselung** in jeden Report gebaut: zeigt Punkte je Kriterium (Edge/35, Expectancy/20, Sharpe/20, PF/15, MC/10) + „was Punkte gekostet hat".
- **BOOK_diverse = 68/100 (C):** Edge nur 18/35 (dünn, +4,4%), Sharpe 12/20 (1,11), PF 8/15 (1,21), Expectancy 20/20, MC 10/10. → Grund: **Edge ist dünn.** Sizing/RR ändern den Score NICHT (der misst Pro-Trade-Qualität), nur die Passchance.
- **Sizing OOS-validiert (kein Overfitting):** IS 2021-23 vs OOS 2024-25, EOD-Drawdown. Cushion-Sizing schlägt flat; **cushion 0,10-0,15 → IS 51-55% / OOS 62% Pass** (OOS ≥ IS = robust, nicht curve-fit). Empfehlung: `cushion_frac ~0,12`.
- **Ehrlich zu RR:** Sizing (cushion_frac = 1 prinzipieller Parameter, dynamischer Kelly) ist der SICHERE Hebel. Per-Bein-RR-Tuning wäre Overfitting-Gefahr; die Beine sind einzeln schon OOS-validiert.

## #024 — Idea Engine ins Lab gebaut (15.07.2026)
- **Top-Level-Umschalter** oben: 🧪 Strategy Lab ↔ 💡 Idea Engine.
- **Idea Engine = Fließband-Board** (nach López de Prado Meta-Strategy): 5 Spalten Backlog → In Test → Validiert → Im Buch → Getötet. Karten mit Edge-Quelle (Farbe), Familie, **WHY**, Ablehnungskriterium, Ergebnis, → Report-Link.
- **Vorbefüllt** (`ideas.json`, 16 Ideen): 2 Backlog (Cross-Asset, Kalender/Structural), 3 Im Buch (Mom-lowVIX, ORB-sweet, Momentum), 4 Validiert, **7 Getötet = Kill-Log** (VWAP-Rev, Holy Grail, Gap-Fade, Order-Flow, VPIN, Prop-Hedge…).
- Grundlagen: [[Idee-Generierung (wie Institutionen)]]. Server (`app_server.py`) hat neuen `/api/ideas`-Endpunkt.
- **Neu starten nötig:** Lab hält den Hub im Speicher → `Strategy Lab.bat` neu.

## #025 — Prop-Valide-Tab + Portfolio-Tab (15.07.2026)
- **Prop-Valide-Tab:** kuratierte Liste nur profitabler, prop-tauglicher Strategien (Edge>0, Net>0, P(pass)≥40%). Spalten: Familie, Win (grün >50%), Net Profit, P(pass)@Size, Tage bis Pass (grün ≤70), **Pass-Rating (⭐, Passchance × Geschwindigkeit)**. Familie ist jetzt in jeder meta.json.
- **Portfolio-Tab (aktuelles Portfolio):** 5 diverse Mechaniken auf 1 Account (ORB-Breakout · ORB-Fade+NR7 · Momentum · Gap-Continuation · Power-Hour), keine Dopplung.
  - **Ø|Korrelation| 0,09** (nahezu unabhängig), **325 Trades/Jahr**, **EOD-Pass 59% in ~140 Tagen** (cushion 0,12), **Net +34.754$/µ**. Report `PORTFOLIO_current`.
- **Idea-Engine-Klärung:** Validiert = bewiesen gut, auf der Bank; Im Buch = ausgewählt fürs echte Traden (Startaufstellung); Getötet = Kill-Log.
- Server: neue Endpunkte `/api/portfolio`. **Lab neu starten nötig** (Hub im Speicher).
