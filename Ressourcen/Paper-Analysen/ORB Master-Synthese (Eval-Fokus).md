---
tags:
  - ressource/paper
  - trading/orb
  - synthese
erstellt: 2026-07-06
---
# 🧬 ORB Master-Synthese (Eval-Fokus)

⬅️ [[Strategie-Katalog]] · [[Backtest-Engine]] · [[Prop-Eval-Passing (Fokus)]]

> [!abstract] Zweck
> Mein eigenes synthetisiertes Research-Dokument: alle nützlichen ORB-Erkenntnisse aus der Literatur + unsere eigenen Engine-Funde, kombiniert zu **einem konkreten, prop-eval-optimierten ORB-Bauplan**. Basis für die iterative Entwicklung im [[Strategie-Logbuch]].

> [!warning] **NACHTRAG #070 (09.08.2026, zweite ORB-Runde):** Auch die drei „Überlebenden" unten sind schwächer als gedacht.
> **VIX-Band ist auf dem Noise-ORB falsifiziert** (hebt nur IS, Gegenprobe außerhalb ist OOS besser — der VIX ist dort nur ein Vola-Proxy, corr(σ,VIX)=0,44). **Noise-Band generalisiert nicht** (RTY/YM tot, ES fraglich) — er ist NQ-spezifisch, aber auf NQ der sauberste ehrliche ORB-Verwandte (IS≈OOS, 10/11 Jahre, top5 0,29). **Und der ORB-Fade im Buch ist eine Regime-Wette**: 8 Jahre netto +95$, dann +5.672$; Top-10 von 422 Trades = 127% des Gewinns. Details: [[Strategie-Logbuch]] #070, [[ORB-Runde 070 (Hypothesen vorab)]].

> [!danger] **KORREKTUR 09.08.2026 (#066-#068): Der Kernbefund unten ist für Index-Futures FALSIFIZIERT.**
> Die "Filter heben Win-Rate auf 55-65%"-Belege beruhten bei uns auf Look-ahead (Filter der Ausbruchs-Bar bei Level-Fill). Ehrlich gemessen (NQ 1m, 10J, netto): **kein Follow-Through nach dem Linien-Break** (+1,1 Pkt in der Bar, −0,6 danach bis EOD), alle klassischen Filter-Stacks tot, NR7-Varianten = Tail-Lotterie (2025/26 negativ), Pineda-Retest 2× falsifiziert, "in Play"-Volumen überträgt sich nicht von Aktien auf Index. **Was ehrlich überlebt:** ORB-Fade (Bein 4, +0,063), Chuk-VIX-Band 15-25 als Kontext (+0,10, Bank), **Zarattini Noise-Band** (`NOISE_ORB_NQ`, +0,094, IS=OOS). Details: [[Strategie-Logbuch]] #067/#068, `Research-Cache` #068-Block.

## ~~Kernbefund (das Wichtigste)~~ (falsifiziert, s.o.)
**ORB roh scheitert. ORB gefiltert kann die Win-Rate von ~40-50% auf 55-65% heben.** Und da fürs Eval **niedriger Drawdown + hohe Win-Rate + wenige Trades** zählen, ist ein streng gefiltertes ORB (1 Trade/Tag, nur A-Setups) der aussichtsreichste Kandidat.

## Belege (kombiniert)
| Quelle | Erkenntnis für uns |
|---|---|
| Zarattini/Aziz 4416622 | 5-Min ORB, Richtung des Breaks, Stop Gegenseite, Target R-Multiple/EoD. Fundament. |
| Pineda 6745958 | Range-Größe ~ Move-Größe. Schneller Retest → höhere Fortsetzung. |
| **Chuk 6355218 (SPY 0DTE ORB)** | **3-Faktor-Filter (Wochentag + VIX-Regime 15-25 + Makro-Event-Ausschluss) hebt Win 46,8% → 65,4%.** Filter = Schlüssel. |
| Liquidity Breakout 5962358 | Breakouts in Low-Volume-Zonen laufen länger. Volumen-Kontext zählt. |
| NSE Block-ORB 5198458 | ORB-Varianten, Block-Performance, Robustheit. |
| TORB (ResearchGate) | Timely ORB: 8-20% p.a., Win 40-55%, mit Trend-Filter Richtung 55%. |
| arXiv 2605.04004 | Roh-ORB auf MNQ (09:30-09:55) scheitert statistisch, Win ~50%, negativ. → Filter Pflicht. |

## Die Filter, die Win-Rate heben (Priorität)
1. **Higher-Timeframe-Trend-Filter (größter Hebel):** Longs nur wenn Tages-Close > 20-Tage-SMA, Shorts nur wenn <. Hebt Win ~40% → ~55%. Reduziert Counter-Trend-Fehlausbrüche.
2. **VWAP-Alignment:** Break nur handeln/halten, wenn Preis auf der Breakout-Seite der VWAP.
3. **Volumen-Bestätigung:** Breakout-Bar RVOL > ~1,5 × OR-Durchschnitt. Schwache Breaks raus.
4. **Time-Cutoff:** keine Breakouts nach ~11:30 ET (dünne Fake-Outs).
5. **Volatilitäts-/NR7-Filter:** ORB stärker nach engem Vortag (NR7) und in mittlerem Vola-Regime.
6. **Makro-Event-Ausschluss:** FOMC/CPI/NFP meiden (oder gezielt, da Momentum an News-Tagen stärker — testen).
7. **1 Trade/Tag:** nur der erste, beste Breakout → wenige Trades = niedriger DD = eval-ideal.

## Konkreter Bauplan v1 (in Engine gießen)
- Instrument: NQ (+ ES gegenprüfen). RTH.
- OR = erste 15 Min → orH/orL.
- Erster Breakout nach OR (Outside-Bar-Tage skippen).
- **Filter-Stack schrittweise zuschalten** (Baseline → +Trend → +VWAP → +Volumen → +Cutoff), Win-Rate & P(pass) je Stufe messen.
- Entry am Level (Stop-Order-Konvention), Stop = 0,5 × OR jenseits, Target = 1-2R oder EoD.
- 1 Trade/Tag.

## Eval-Design-Prinzipien (übergeordnet)
- **Niedriger Drawdown schlägt Rendite.** Wenige, selektive Trades.
- **Baseline-Regel:** Win-Rate gegen realisierte Breakeven-Win-Rate messen.
- **Ehrliche Fills** (echter Touch/Level, Stop-before-Target, Kosten, MAE).
- Ziel: P(pass) ≥ 70% bei akzeptabler EV, kleiner DD.

## Iterationsplan
Stufenweise Filter zuschalten, jede Stufe als eigener Lab-Report, bis Win-Rate + P(pass) die Schwelle erreichen oder klar ist, dass ORB auf NQ nicht reicht.
