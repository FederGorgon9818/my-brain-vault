---
tags:
  - ressource/trading
  - quantpad-brief
  - trading/backtest
erstellt: 2026-08-10
---
# 🔍 QuantPad Brief — Engine Verification (Blind-Audit)

> [!info] Wofür
> Diesen Brief 1:1 an den QuantPad-Agenten geben. Er beschreibt unsere komplette Validierungs-Methodik (die "Engine-Strategie") und gibt QuantPad **drei Benchmark-Aufgaben, deren ehrliche Ergebnisse wir lokal schon kennen** — QuantPad kennt sie nicht (Blind-Test). Vergleich der Zahlen unten in der [[#Auswertung (nur für uns, NICHT mitschicken)]].
> Verwandt: [[QuantPad Brief - VWAP Mean Reversion]], [[Backtest-Engine]], [[ORB Fast-Retest Review]], [[Strategie-Logbuch]].

---

## COPY EVERYTHING BELOW THIS LINE INTO QUANTPAD

---

# VERIFICATION BRIEF: Reproduce three strategy studies under strict honesty rules

## 1. Context and goal

I am a systematic futures trader and software developer. I run my own local
backtesting engine and I am cross-validating results between my engine and
QuantPad. Your task is NOT to find a new edge. Your task is to **reproduce
three precisely specified studies** under the honesty rules below and report
the numbers exactly as they come out — positive or negative.

This is an audit-style task: I already have reference results for all three
studies. I am checking whether your simulation methodology (fills, costs,
walk-forward hygiene) matches a strict, conservative standard. **A "this
strategy loses money" result is a perfectly good outcome.** Do not tune,
rescue, or reframe a losing strategy. Run exactly what is specified.

## 2. Mandatory methodology (applies to ALL three studies)

**Fills (most important — this is where backtests lie):**
- F1. Signals are computed on CLOSED bars only. Market entries fill at the
  NEXT bar's open. No same-bar entry on the signal bar.
- F2. Limit orders fill ONLY on a real touch: a buy limit at level L fills
  only if a later bar's low <= L. Never assume a fill because price came
  "close" to the level. Fill price = L (or worse), never better.
- F3. Stop orders assume 1 tick of slippage beyond the stop price. Gaps
  through the stop fill at the actual traded price, not the stop price.
- F4. If a bar's range contains BOTH the stop and the target, count it as a
  STOP (conservative same-bar rule). No intrabar sequencing guesses.
- F5. No look-ahead of any kind: every input to a decision at time t must be
  known strictly before t. Volume filters may only use volume up to and
  including the last CLOSED bar before entry.

**Costs:**
- C1. Report every result GROSS and NET. Net = 1 tick per side slippage on
  market/stop fills + realistic round-turn commission for CME micro futures.
- C2. Never present a gross number as the headline if the net number differs
  materially.

**Statistics:**
- S1. Baseline check: for a fixed stop/target bracket, the random-walk
  win rate is stop/(stop+target) (in R terms). A strategy only has an edge
  if its win rate beats this breakeven baseline — report both numbers.
- S2. Report per-trade MAE (maximum adverse excursion, in R), including for
  winning trades.
- S3. Walk-forward where requested: rolling in-sample optimization window,
  out-of-sample window stepped forward, OOS segments stitched into ONE
  equity curve. Costs applied to OOS trades. Also report whether the chosen
  parameters are STABLE across windows — parameter jumping = overfit flag.
- S4. Monte Carlo where requested: block/stationary bootstrap (not i.i.d.)
  of the OOS trade sequence, 5000+ resamples.

**Reporting:**
- R1. Full metric set: n trades, win rate (vs. baseline), avg R, expectancy
  (R), profit factor, Sharpe, max drawdown, longest losing streak, largest
  single day as % of total net profit.
- R2. State every assumption you had to make that is not specified here.
- R3. If a result is negative or below baseline, say so in the first line of
  your summary. Honesty over optimism — I will verify every number.

## 3. Study A — ORB Fast-Retest on NQ (fixed parameters, no optimization)

Instrument: NQ futures, 1-minute bars, RTH (09:30–16:00 ET), 2019-01-01 to
2025-12-31. Roll adjust: none.

Rules (run EXACTLY this, no tuning):
1. Opening range = first 5 minutes of RTH (09:30–09:35). OR-high / OR-low.
2. A breakout occurs when a 1m bar CLOSES outside the OR.
3. After the breakout, wait for a RETEST of the broken OR level within 20
   minutes: for a long, price must come back DOWN and actually TOUCH the
   OR-high (bar low <= OR-high). Entry = limit at the OR level, fill rule F2
   strictly (no tolerance band, no fill if the level was never touched).
4. Stop = 0.25 x opening-range height beyond the level. Target = 3R.
5. One trade per direction per day maximum; everything flat at 15:55 ET.

Deliverables A: full metric set (R1) gross and net for 2019–2025, plus a
**walk-forward** (24-month IS, 6-month OOS, SQN objective) over the same
period where OR length {5,15,30}, retest window {10,20,30}, stop {0.25,0.5}
and target {1R,2R,3R,EoD} are optimized per window. Report the stitched OOS
equity (gross and net) and the parameter stability across windows.

## 4. Study B — Naked VWAP z-score reversion on NQ (no filters)

Instrument: NQ futures, 1-minute bars, RTH only, 2016–2025. Session VWAP
anchored at 09:30 ET. z = (price − VWAP) / rolling std of (price − VWAP).

Rules:
1. Long when z <= −2.0, short when z >= +2.0 (next-bar-open market entry,
   rule F1).
2. Target = 1.0 sigma back toward VWAP, stop = 1.5 sigma against the
   position (so baseline breakeven win rate = 1.5/(1.5+1.0) = 60%, rule S1).
3. Time exit: flat at end of RTH. Max 3 trades per day.

Deliverables B: full metric set gross and net, win rate vs. the 60% baseline,
separately for the LONG side, SHORT side, and combined. Then run the exact
mirror (continuation instead of reversion: buy the +2z stretch, sell the
−2z stretch, same bracket) and report the same table. State clearly whether
EITHER direction beats baseline net of costs.

## 5. Study C — ORB breakout follow-through decomposition on NQ

Instrument: NQ futures, 1-minute bars, RTH, 2016–2025. Opening range = first
15 minutes.

Question: after a 1m close outside the OR, is there ANY follow-through?
1. Identify every first breakout per day (close outside OR).
2. Measure two legs separately: (a) the breakout bar itself (open to close
   of the bar that closes outside the OR), and (b) from the NEXT bar's open
   to the 16:00 ET close, signed in the breakout direction.
3. Report for each leg: mean points, median points, % positive days, n.
   No trading rules, no stops — this is a pure drift measurement.

Deliverable C: the two-leg table plus one sentence: does the post-breakout
leg (b) show economically meaningful positive drift, or not?

## 6. Prop-firm simulation (apply to any study whose NET result is positive)

If — and only if — one of the studies shows a net positive OOS edge, run a
prop lifecycle simulation on its OOS trades: E8 50k evaluation, profit
target $3,000, trailing max drawdown $3,000 (END-OF-DAY trailing), daily
loss limit $2,000 (verify current E8 terms and state your assumptions).
Model the trailing drawdown against intraday equity including open-trade
MAE as a sensitivity case. Output per contract size: P(pass), median days
to pass, P(breach). If nothing is net positive, skip this section and say so.

## 7. Output format

For each study: (1) one-line honest verdict first, (2) metric tables gross
and net, (3) assumptions made, (4) anything in my specification you had to
deviate from and why. Do not add motivational commentary. Numbers over
narrative.

---

## Auswertung (nur für uns, NICHT mitschicken)

Unsere lokalen Referenz-Ergebnisse (ehrliche Engine, siehe [[ORB Fast-Retest Review]], [[Backtest-Engine]], [[Strategie-Logbuch]] #068):

### Studie A — ORB Fast-Retest (der Phantom-Fill-Test)
Das ist QuantPads eigene alte Strategie von Juli. Der Original-Agent hatte Entry-Fills bei `level` angenommen, obwohl der Kurs das Level nie berührt hatte (Toleranzband ~9 Punkte).

| Kennzahl (2019–2025, fixe Params) | Mit Phantom-Fill-Bug | Ehrlich (echter Touch) |
|---|---|---|
| Trades | 393 | 319 |
| Gesamtrendite | +662% | **−7,4%** |
| Sharpe | 2,12 | **−0,04** |
| Profit-Faktor | 1,87 | **0,99** |
| WF-OOS gestitcht | +1.094% | **−32,4%** (netto Sharpe −1,42) |
| Parameter über WF-Fenster | "stabil" | springen wild (OR 5→15→30→5) |

**Lesart:** Meldet QuantPad wieder dreistellige Plus-Renditen → Fill-Logik immer noch optimistisch, Daten-Exports ok, aber Backtests dort nicht trauen. Meldet es ~Null/negativ + instabile WF-Parameter → sauber gearbeitet.

### Studie B — VWAP z-Stretch (der Baseline-Test)
Lokal: Reversion netto ~56% Win-Rate **unter** der 60%-Baseline = keine Edge. Continuation brutto nur +0,1% über Baseline = Rauschen. **Keine Richtung hat Edge.** Meldet QuantPad hier eine tradebare Edge (in irgendeiner Richtung), stimmt etwas an Fills/Kosten/Baseline nicht.

### Studie C — ORB Follow-Through (der Look-Ahead-Test)
Lokal (2.685 NQ-Ausbruchstage): Ausbruchs-Bar selbst **+1,1 Pkt** (nur per Look-ahead erntbar), danach bis EOD **−0,6 Pkt**, 51% = Coinflip. **Kein Follow-Through.** Meldet QuantPad deutlichen positiven Drift nach dem Break → die beiden Legs wurden vermischt (klassischer Look-ahead).

### Gesamt-Urteil
- **3/3 Treffer** → QuantPad arbeitet ehrlich; Backtests dort als Zweitmeinung brauchbar.
- **Studie A daneben** → Fill-Optimismus (bekanntes Muster von Juli), nur noch als Daten-Quelle nutzen.
- **B oder C daneben** → Methodik-Problem tiefer (Baseline/Look-ahead), Ergebnisse dort grundsätzlich nicht übernehmen.
