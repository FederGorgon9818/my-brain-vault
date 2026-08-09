---
tags: [research, cache, evidence]
created: 2026-07-29
zweck: Persistenter Evidence Store. VOR jeder Websuche hier greppen. Nach jeder Recherche neue Claims eintragen.
---

# Research-Cache (Quellen & Claims)

**Regeln:**
- Ein Claim pro Zeile: Aussage · Quelle · Abrufdatum · Status (`bestätigt` = Paper/Primärquelle, `praktiker` = Blog/Backtest Dritter, `eigene-daten` = von uns repliziert, `veraltet`).
- Zeitkritisches (Preise, Firmenregeln) bekommt ein "gültig Stand"-Datum → nach 60 Tagen neu prüfen.
- Modell-Zusammenfassungen sind KEINE Quelle. Immer Original-Link.
- Markterkenntnisse aus eigenen Backtests → gehören in die [[Strategie-Logbuch|Insight-Bank]], nicht hierher. Hier nur EXTERNE Evidenz.

## ORB / Opening Range Breakout (recherchiert 28.07.2026)

| Claim | Quelle | Status |
|---|---|---|
| 5m-ORB auf QQQ 2016-23: 33% Alpha p.a. nach Kosten; Entry Kerze 2 in Richtung Kerze 1, Stop Kerzen-Extrem, EOD-Exit, Leverage nötig | [Zarattini/Aziz SSRN 4416622](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622) | bestätigt · **eigene-daten:** NQ-Port PF 1,08 (einziger Grid-Survivor #044) |
| ORB-Edge konzentriert sich auf "Stocks in Play" = hohes relatives Volumen | [Zarattini/Barbon/Aziz SSRN 4729284](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284) | bestätigt fürs AKTIEN-Universum · ⚠️ **eigene "Bestätigung" via Bein 8 war Look-ahead (#067)!** Ehrlicher OR-RVOL-Test auf NQ (#068): überträgt sich NICHT auf Index-Futures (alle Varianten $-negativ o. konzentriert) |
| TORB: ORB-Entries nahe Markt-Open am profitabelsten, 5 Index-Futures signifikant (2003-13) | [Syu et al. IEEE 2019](https://ieeexplore.ieee.org/document/8641124/) | bestätigt |
| ORB auf Futures (Crude) auch mit Tages-OHLC profitabel | [Holmberg et al. 2013](https://www.sciencedirect.com/science/article/abs/pii/S1544612312000438) | bestätigt |
| ORB nach NR7/Kompression am effektivsten; "Stretch"-Konzept | Crabel 1990 (Buch, out of print) via [QuantifiedStrategies](https://www.quantifiedstrategies.com/nr7-trading-strategy-toby-crabel/) | praktiker · **eigene-daten:** NR7 im ORB-fade-Bein |
| Viele ORB-Varianten auf MNQ statistisch NICHT signifikant (Falsifikations-Studie) | [arXiv 2605.04004](https://arxiv.org/pdf/2605.04004) | bestätigt — Mahnung: nur gefilterte Varianten tragen |
| Praktiker-Konsens: 5m früh+noisy / 15m Allrounder / 30m Trendtage; EOD-Exit hilft; Target 1-3R | [BuildAlpha](https://www.buildalpha.com/opening-range-breakout/), [QuantifiedStrategies](https://www.quantifiedstrategies.com/opening-range-breakout-strategy/) | praktiker |
| Scalp-Zeit-Exits ohne Filter töten den ORB-Edge (Gewinner werden abgeschnitten) | — | eigene-daten (#044, 27 Configs Teil B alle IS-fail) |
| **MNQ ORB direkt am Breakout (bar+1) = 51,9% Win, FAIL; längerer Horizont (bar+15) 55,5% Win, T=1,50 aber immer noch FAIL.** Kurzes Fenster ist die SCHLECHTESTE Variante, nicht die beste | [arXiv 2605.04004 Tabelle 3](https://arxiv.org/pdf/2605.04004) (lokal: `mnq_falsification.txt`) | bestätigt — Kern-Gegenbeweis zur Short-Hold-Scalp-Intuition |
| **Roher Short-Horizon-Edge auf MNQ strukturell nur 0,07-1,50 Pkt über ALLE Signalfamilien → unter den 2-Pkt-Round-Trip-Kosten.** Naked-Scalping clears die Kosten nicht | dito (Conclusion) | bestätigt |
| **Einziges Signal mit hoher Signifikanz: Volumen-Filter >2,5× → T=3,23, +14,52 Pkt, Win 68,2% — aber nur 22 Trades/3J (<30-Schwelle)** | dito | bestätigt → Filter (Volumen) ist der Hebel, nicht das kurze Fenster; deckt sich mit Bein 8 |
| Market Intraday Momentum: erste 30 Min (Vortagesschluss→10:00 ET) sagen letzte 30 Min (15:30-16:00) signifikant voraus; Mechanik = Gamma-Hedging von MMs/Leveraged-ETFs; **Horizont = Open→Close (Stunden), NICHT Minuten-Scalp**; revertiert über Folgetage | [Gao/Han/Li/Zhou, JFE 2018 (nd.edu)](https://academicweb.nd.edu/~zda/intramom.pdf) | bestätigt — Momentum lebt vom LANGEN Halten bis Close, nicht vom schnellen Rausgehen |
| TORB (Timely ORB, 1-min, 5 Index-Futures 2003-13): >8% p.a., bestes TAIEX 20,3%; Entries NAHE Open am stärksten | [Syu et al. IEEE 2019](https://ieeexplore.ieee.org/document/8641124/) | bestätigt (Entry-Timing ja, aber Hold über den Tag) |

### #068 Deep-Dive 09.08.2026 (alles mit ehrlicher Exec: Close-Confirm oder ruhende Orders, netto)
| Claim | Quelle | Status |
|---|---|---|
| **NQ-ORB hat KEIN Follow-Through nach dem Break:** Zerlegung 2.685 Ausbruchstage: Ausbruchs-Bar +1,1 Pkt, danach→EOD −0,6 Pkt (51% pos = Coinflip); auch mit Trend/Vol-Spike-Kondition ≈ 0. Die alte "Edge" waren die +6,4 Pkt IN der Spike-Bar (nur mit Look-ahead erntbar) | eigene-daten `orb_followthrough_066.py` | eigene-daten — Kern-Erklärung für #066/#067 |
| Momentum-Displacement (≥0,3% in 15 Min) hat dagegen ECHTEN Drift: +13,6 Pkt bis EOD, 56% pos (n=796) — "früher Impuls→Tages-Run" lebt im Momentum-Bein, nicht im Linien-Break | eigene-daten | eigene-daten |
| NR7-Breakout-EOD (Crabel) sieht IS/OOS gut aus (+0,28-0,33 expR), ist aber **Tail-Lotterie**: Top-5 Trades 46-63% des R, 2025-26 NEGATIV (−1.900$) → für Trailing-DD-Evals ungeeignet | eigene-daten `orb_honest_discovery_066.py` | eigene-daten — Vorsicht Multiple-Testing-Falle |
| Pineda-Retest auf NQ **zweite ehrliche Falsifikation**: Signal existiert, aber alle 36 Varianten (Limit am Level, echter Touch) OOS/2025+ negativ | eigene-daten `orb_retest_068.py` | falsifiziert für NQ-Futures |
| **Chuk VIX-Band 15-25 (Vortag) repliziert auf NQ:** close-EOD-ORB expR +0,10 im Band vs +0,00 außerhalb (n=1.317), 8/11 Jahre positiv, Nachbar-Parameter alle positiv, 2024-26 stärkste Phase; Wochentags-Faktor überträgt sich NICHT | [Chuk SSRN 6355218] + eigene-daten | eigene-daten — Kandidat `ORB_VIXBAND_NQ` |
| **Zarattini Noise-Band (SSRN 4824172) auf NQ portiert:** 30-Min-Checks, Band=max(Open,PrevClose)±σ(t) (14d, Punkte), VWAP-Trail, EOD; m1.0 (Paper-Default): expR +0,094, IS +0,094 = OOS +0,097, 9/11 Jahre $-positiv, Top5 nur 29%, MaxDD −5k$/Micro | [SSRN 4824172](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172) + eigene-daten `noise_orb.py` | eigene-daten — Kandidat `NOISE_ORB_NQ` |
| Maróy (SSRN 5095349) verbessert Zarattini-Exits, aber 1 Instrument/kurzer Zeitraum, Overfitting-Kritik in Reviews | [SSRN 5095349](https://papers.ssrn.com/sol3/abstract_id=5095349) | praktiker — nicht übernommen |

## Prop-Firmen (gültig Stand 28.07.2026 — nach 60 Tagen neu prüfen!)

| Claim | Quelle | Status |
|---|---|---|
| E8 Signature Futures 50k: $150 einmalig, EOD-DD 4% ($2.000), Target 6% ($3.000), 80% Split (fix, kein Add-on, alle Tiers) | Checkout-Screenshot Max 28.07. + Support-Mail | bestätigt (menschl. Bestätigung Split: Max' Checkout) |
| E8: VPS/Datacenter-IP schriftlich erlaubt, Eval UND Funded (Support Mohamed, 27.07.) | Screenshot archiviert (Payout-Versicherung) | bestätigt |
| Bulenox: VPS strikt verboten (Ticket #RAX-292098) | Support-Antwort 27.07. | bestätigt |
| E8 seit 11/2021, $38-68M Payouts, Trustpilot 4,3-4,4; Negativ-Reviews = Regelkomplexität, nicht Payout-Verweigerung | WebSearch 28.07. (mehrere Quellen) | praktiker |

## Exit-Overlays: Break-Even & Trailing Stops (recherchiert 29.07.2026)

| Claim | Quelle | Status |
|---|---|---|
| Break-Even-Stops senken langfristige Profitabilität (Gewinner werden gekappt, "Markt braucht Raum"); fühlen sich nur emotional besser an | [Quantfish Research](https://quant.fish/wiki/the-truth-break-even-and-trailing-stops-in-trading-systems/) | praktiker · **eigene-daten:** #046 — 0/8 Buch-Beine überleben OOS |
| Trailing-Stops haben nur in trendenden Märkten positive Expectancy, in Chop "loss machine" | [IQ Option Blog](https://blog.iqoption.com/en/how-to-use-trailing-stops-without-killing-your-winners/), [ATAS](https://atas.net/blog/break-even-in-trading/) | praktiker · eigene-daten: RV-leadlag TR1.5 OOS 0,398→0,247 |
| Trailing-SL-Studie (Europa-ETFs): mixed vs. Buy&Hold, Hauptnutzen = weniger Verluste in Hochvola-Szenarien (Varianz, nicht Edge) | [EJBMR](https://www.ejbmr.org/index.php/ejbmr/article/download/1426/787) | bestätigt · eigene-daten: MAE sinkt real (0,82→0,65R), Expectancy trotzdem schlechter |

## TSI Mean Reversion — Requejo SSRN 4708400 (recherchiert 29.07.2026)

| Claim | Quelle | Status |
|---|---|---|
| Daily-TSI-MR auf SPY/QQQ 1996-2022, Ø 5d Holds, Close-Signal→Open-Fill, Walk-Forward 3J-Fenster; exakte Parameter hinter Paywall | [SSRN 4708400](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4708400) (403 für Volltext/PDF), [CARL-Summary](https://investwithcarl.com/investment-strategies/efficacy-of-a-mean-reversion-trading-strategy-using-true-strength-index-tsi) | praktiker · **eigene-daten:** #047 Proxy-Test NO-GO (n=21, kippt über Instrument/Params, Overnight-Anteil negativ) |

## Edge-Decay (recherchiert 27.07.2026)

| Claim | Quelle | Status |
|---|---|---|
| Publizierte Edges verlieren ~26% OOS, ~58% post-publication | McLean/Pontiff 2016 (J. Finance) | bestätigt → Basis des Ampel-Monitors |
| CUSUM-Verfahren für Strukturbruch-Erkennung in Strategie-Returns | Lopez de Prado, Advances in Financial ML | bestätigt |

## OpEx / Charm-Vanna-Flows (recherchiert 30.07.2026)

| Claim | Quelle | Status |
|---|---|---|
| Am Expiry-Tag konzentriert sich Gamma extrem an ATM-Strikes; kleine Moves triggern große Dealer-Hedge-Flows | [GexMetrix OpEx-Effects](https://www.gexmetrix.com/blog/opex-effects), [SpotGamma GEX](https://spotgamma.com/gex/) | praktiker |
| Charm-Flows (Delta-Zerfall über Zeit) wirken am stärksten in same-day/weekly Expiries; Charm-Fenster später Vormittag → Nachmittag relevant für Continuation vs. Fade | [MenthorQ Vanna/Charm](https://menthorq.com/guide/why-markets-can-go-wild-after-options-expiration-vanna-and-charm-and-the-volatility-effect/), [VCAlgo](https://vcalgo.com/blog/vanna-charm-gamma-exposure-gex/) | praktiker |
| Negatives 0DTE-Gamma → scharfe Nachmittags-Trends; positives Gamma → Pinning an Max-OI-Strike. Beide Regime existieren am OpEx | [GexMetrix Vanna/Charm](https://www.gexmetrix.com/blog/vanna-charm) | praktiker |
| OpEx-Nachmittag fadet den Vormittag NICHT (Fade −22% netto NQ/ES 2016-26) → Continuation-Seite plausibel | — | eigene-daten (#034) |

## Pivot Points / Technische Level (recherchiert 30.07.2026)

> [!warning] Blog-vs-Paper-Trennung: Fast die gesamte Pivot-"Evidenz" im Netz ist Marketing (edgeful, tradealgo, tradingsim). Präzise Zahlen ("64% Reaktion", "89% Touch", "PF 2,93") ohne nachprüfbare Primärquelle → mit Selektionsbias-Prior behandeln (wie Instagram-Paper #047).

| Claim | Quelle | Status |
|---|---|---|
| **TA-Regeln verlieren ihre Profitabilität in reifen Index-Märkten (S&P500/DJIA), sobald Data-Snooping-Bias kontrolliert wird (stepwise SPA-Test); Edge überlebt eher in jungen/ineffizienten Märkten und zerfällt über die Zeit** | Hsu/Hsu/Kuan, J. Empirical Finance 2010 ([SSRN 1087044](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1087044), 403) | bestätigt — stärkster Skepsis-Anker gegen Pivot-Edge auf ES/NQ |
| Technische Muster tragen *modeste* inkrementelle Information (bedingte Renditeverteilung ≠ unbedingte), v.a. NASDAQ; aber KEIN Profitabilitäts-Claim nach Kosten | Lo/Mamaysky/Wang, J. Finance 2000 ([SSRN 228099](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=228099), 403) | bestätigt — Info ≠ handelbare Edge |
| "Preis berührt den Pivot in 67-89% der Sessions" | edgeful/tradealgo-Blogs | praktiker — **near-tautologisch**: ein aus HLC/3 des Vortags gebildetes Level liegt fast immer INNERHALB der heutigen Range → Touch ist fast garantiert, sagt NICHTS über handelbare Edge |
| Pivot-Varianten (Standard/Floor, Woodie H+L+2C/4, Camarilla, Fibonacci): kein Typ objektiv genauer; Standard-Floor default weil am meisten beobachtet (Selbsterfüllungs-Argument) | [Babypips](https://www.babypips.com/learn/forex/other-pivot-point-calculation-methods), [TradingSim](https://www.tradingsim.com/blog/pivot-points) | praktiker |
| **Mechanismus (ehrlich):** Pivots = Vortages-HLC-Referenzlevel, die viele Teilnehmer beobachten → *potenziell* selbsterfüllende Reaktionspunkte. Keine kausale Order-Flow-Fundierung wie Charm/Gamma (#049) oder RVOL (#044) | Synthese | eigene-einschätzung — **muss durch ehrlichen Backtest, nicht durch Touch-Statistik** |

## Video-Analyse: proptradingindicators.com "Pivot Point Strat" (30.07.2026)

> [!warning] Verkäufer-Demo, keine Studie. Genre wie #047 (Instagram-Paper) — Marketing-Bias-Prior.

| Claim | Quelle | Status |
|---|---|---|
| Produkt heißt "Pivot Point Strat", ist aber KEIN Floor-Pivot-System (kein P/R1/S1 aus Vortages-HLC) — proprietärer Indikator "PPG1" auf symmetrischen Renko-Bricks, binäres Regime, Formel nicht offengelegt | [YouTube 92hI5TrBcPk](https://www.youtube.com/watch?v=92hI5TrBcPk) (Transkript von Max) | praktiker — Name ≠ Mechanik, wichtig für spätere Verwechslung |
| Mechanik: Entry auf Schlusskerze in Regime-Richtung, haltet bis Gegensignal (Flatten+Flip), fixer Stop (Bsp. MNQ 160 Ticks = 40 Pkt), Break-Even-Lock ab +170 Ticks, kein festes Target, EOD/Session-Ende, immer erste 2 Min nach Open ausgeschlossen | dito | praktiker |
| **Zwei Modi:** Signals (Entries ganztägig) vs Time-Window (Entries nur 8:32-12:30 US Central = 9:32-13:30 ET, offene Trades laufen normal weiter) — Verkäufer-Claim: Time-Window leicht besser, gestützt nur auf 1 Kunden-Anekdote "50-60 Tage", keine Zahlen | dito | praktiker — **schwache Evidenz**, bewusst ausgewählte Beispieltage im Video ("two days I picked by design") |
| **Eigener Test (flip.py, Schwellen-Umkehr-Regime als Renko-Proxy auf echten 1-Min-Daten):** EMA-Crossover-Regime (Iteration 1) whipsawt komplett (42.727 Trades/10J auf NQ, win 28,6%) — bestätigt indirekt, WARUM Renko nötig ist (filtert genau dieses Rauschen). Schwellen-Umkehr-Regime (Iteration 2, Brick=0,75×ATR20) zeigt moderaten echten Edge (PF 1,10, edge +2,5%, ~516 Trades/Jahr) | eigene-daten (30.07.) | eigene-daten — siehe Logbuch #052 |
| **Time-Window vs Signals-Mode A/B (24 Configs, NQ/ES/YM/RTY):** nur NQ hat überhaupt Edge (ES/YM/RTY negativ, bestätigt Buch-Charakter). Auf NQ: Time-Window minimal besser als Signals (expR +0,041 vs +0,036 bei Brick 0,75), aber Unterschied klein/uneindeutig über andere Brick-Größen (7 von 12 Paarvergleichen Window besser, 5 Signals — im Rauschen). Video-These NICHT klar bestätigt. **Alle 4 Survivors vom Auto-Fit abgelehnt:** Buch-Passquote fällt von 61%/81d auf 47-51%/37-40d — zu viele Trades (400-500/Jahr) mit zu schwachem Edge (~46% Win, nahe Coinflip) verwässern das bestehende Buch trotz niedriger Korrelation (0,08-0,09) | eigene-daten (30.07.) | eigene-daten — siehe Logbuch #052 |

## Makro-Kalender Rest-2026 (gültig Stand 30.07.2026 — vor 2027 neu ziehen!)

| Claim | Quelle | Status |
|---|---|---|
| FOMC-Statements Rest-2026: 16.09., 28.10., 09.12. (je 14:00 ET; Jul-Meeting war 28.-29.07.) | [federalreserve.gov FOMC-Kalender](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | bestätigt |
| NFP (Employment Situation) Rest-2026: 07.08., 04.09., 02.10., 06.11., 04.12. (je 08:30 ET) | [BLS-Schedule 2026](https://www.bls.gov/schedule/2026/01_sched.htm) via [OMB-PFEI-PDF](https://statspolicy.gov/assets/fcsm/files/docs/OMB_pfei_schedule_release_dates_cy2026.pdf) | bestätigt |
| CPI Rest-2026: 12.08., 11.09., 14.10., 10.11., 10.12. (je 08:30 ET) | dito | bestätigt |


## Alpha-Batch #056: VWAP-Pullback / IB-Extension / Overnight-Reversal (02.08.2026)

| Claim | Quelle | Status |
|---|---|---|
| **Overnight-Intraday Reversal (Cross-Section):** Long niedrige / Short hohe Overnight-Returns liefert intraday 2-5x hoehere Sharpe als Close-to-Close-Reversal, ueber Equity-Index-/Zins-/Rohstoff-/FX-Futures. Mechanismus: Market-Maker-Liquiditaets-Provision (Inventar-Rebalancing), NICHT Sentiment/Makro-News | [SSRN 2730304](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2730304) (Liu/Liu/Wang/Zhou/Zhu), verwandt [Della Corte/Kosowski](https://assets.super.so/e46b77e7-ee08-445e-b43f-4ffd88ae0a0e/files/c953a0e6-e93e-4bf7-b839-45a90cedced4.pdf) | bestaetigt (akademisch) — fuer uns als ZEITREIHEN-Variante auf Einzelinstrument zu testen, nicht 1:1 |
| **Intraday TS Reversal (US-Indizes):** Overnight-Return sagt die ERSTEN 30 Min invers voraus; staerker bei hoher Vola (GFC, frueh-COVID), **schwaecher nach den 2010ern und spaet-COVID** (Decay-Warnung!). Mechanismus: Retail kauft overnight, Arbitrageure verkaufen intraday. Nur US-Indizes, nicht international | [SSRN 5807282](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5807282) (Iwanaga/Sakemoto, 11/2025) | bestaetigt (akademisch) — Decay im modernen Sample ist DIE Kernfrage fuer unseren OOS-Split |
| VWAP-Pullback-Continuation: Institutionen benchmarken Executions gegen VWAP -> intraday "Fair-Value-Magnet"; Setup = fruehe Momentum-Bewegung, Pullback an VWAP, Entry in Trendrichtung. Praktiker-Backtests: SPY 1h 2017-2025 PF 1,69 bei Win <50%; Setup-Alignment hebt Win auf ~64% | [TradingSim](https://www.tradingsim.com/blog/vwap-indicator-guide), [Substack-Backtest](https://tradinginvestingstrategies.substack.com/p/the-simple-vwap-strategy-pine-script-tradingview), [BullsOnWallStreet](https://www.bullsonwallstreet.com/post/what-is-the-vwap-trading-indicator-and-how-to-use-it-as-a-day-trader) | praktiker — kein Akademik-Paper; konsistent mit Insight-Bank #1 (VWAP-Stretches = Continuation, nicht Reversion) |
| Initial-Balance-Extension (Market Profile): IB = Range der ersten 60 Min; spaete Range-Extension (nach Mittag) gilt als Trend-Tag-Bestaetigung mit Fortsetzung bis Close | Steidlmayer/Dalton-Standardwissen (Market-Profile-Literatur) | praktiker — anderes Zeitfenster als unser ORB (15-Min-OR, Cutoff 90-120), muss auf Korrelation zu ORB-Beinen geprueft werden |

## Alpha-Batch #057: Intraday-Momentum (first30→last30) / Vol-Breakout / Momentum-Selektiv (02.08.2026)

| Claim | Quelle | Status |
|---|---|---|
| **Market Intraday Momentum:** Return der ERSTEN 30 Min (inkl. Overnight, d.h. PrevClose→10:00) sagt den Return der LETZTEN 30 Min voraus (SPY 1993-2013, JFE 2018); staerker an High-Vol-/High-Volume-/Rezessions-/Makro-News-Tagen; gilt auch fuer 10 weitere aktiv gehandelte ETFs. Mechanismen: infrequent portfolio rebalancing (Bogousslavsky 2016) + late-informed trading nahe Close | [SSRN 2440866](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2440866) (Gao/Han/Li/Zhou, JFE 2018), [Alpha Architect](https://alphaarchitect.com/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/) | bestaetigt (akademisch, top-publiziert) — Abgrenzung zu PowerHour-Bein: anderes Signal (first-30 statt 240-Min-Move) + engeres Fenster (nur letzte 30 Min) |
| **Crabel Vol-Breakout ("Stretch"):** Entry bei Open +/- vordefiniertem Betrag; am wirksamsten NACH NR4/NR7-Kompression (Vol-Kontraktion -> Expansion); pre-1990-Backtests mit Win 60-76% in getesteten Setups; moderne Praktiker-Adaptionen sehen den Effekt weiter vor Trend-Tagen | [QuantifiedStrategies](https://www.quantifiedstrategies.com/nr7-trading-strategy-toby-crabel/), [OxfordStrat NR7](https://oxfordstrat.com/trading-strategies/nr7/), Crabel-Buch | praktiker (Daten pre-1990!) — hohe Verwandtschaft zu unserem ORB-Breakout -> Korrelations-Check durch Auto-Fit ist Pflicht |
| Momentum-Selektiv (eigener Backlog-Kandidat): weniger/groessere Trades an "sauberen" Trendtagen via Kaufman-Efficiency-Ratio des Signal-Fensters (rev_er_min existiert ungenutzt in der Engine) | eigene Hypothese aus #045/#053-Beobachtungen | eigene-einschaetzung — reine Filter-Verschaerfung des bestehenden Beins, kein neuer Mechanismus |

## Video-Analyse: Matteo Coni „Drift VWAP Pullback / Prop Firm Golden Ticket" (09.08.2026)
Quelle: Interview youtube.com/watch?v=wm4A6qo0g3I (Ex-Market-Maker Nordea, CIO SQR Capital). Voller Nachtest in [[Strategie-Logbuch]] #069.

| Claim | Prüfung | Status |
|---|---|---|
| Strategie: NQ Session-VWAP-Drift (Preis vs. VWAP + VWAP-Slope 15m + ±0,1%/1h) → Entry auf ersten Gegenfarb-5m-Pullback, Long 40/80, Short 50/80, max 4 Tr/Tag, 10:30–15:30, flat 15:55 | 1:1 repliziert, seine Stats exakt getroffen (Win 63,6% vs. 64, Ø-Win $861 vs. 866, ~3.950 Tr seit 2021 vs. „4.000+") | bestätigt — Regeln vollständig & ehrlich beschrieben |
| „64% Win-Rate = extrem gut" | stimmt, ABER Breakeven-Baseline bei RR<1 liegt bei ~62% → echter Edge nur +1,5–2pp, expR +0,02–0,03, PF 1,05–1,09 | bestätigt-mit-Sternchen — dünner echter Edge |
| 90–95% institutioneller Orders laufen über VWAP-Execution-Algos → Pullback zur VWAP enthüllt Imbalance | Mechanismus plausibel (Continuation an VWAP = unser Insight #1), aber im Video unbelegt; Effektstärke im Test klein | praktiker-plausibel, nicht separat verifiziert |
| ~50% P(pass) pro Eval, 93,6% in 4 Versuchen, Ø 3 Tage („Golden Ticket") | reproduziert sich NUR mit Close-only-Equity (43%/89,5%). Ehrlich mit Intraday-MAE-Trailing (Apex 50k): 1 NQ 23–27%, 4 MNQ ~33% | **widerlegt (~2x zu optimistisch)** — Trailing-DD zieht intraday, 1 NQ auf 50k ist übersized |
| In-Sample 2020–2024, seither OOS, „kein Overfitting" | OOS 24–26 hält tatsächlich (PF 1,09, +30k/Jahr/NQ). ABER Pre-Sample 2016–2019 (nie gezeigt): 3 von 4 Jahren negativ → Edge erst ab 2020er-Regime | teilweise bestätigt — regime-abhängig |
