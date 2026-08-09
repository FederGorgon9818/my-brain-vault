---
tags:
  - ressource/paper
  - trading/mean-reversion
  - quantpad-brief
erstellt: 2026-07-05
---
# 🏗️ QuantPad Build Brief — Regime-Filtered Intraday VWAP Mean Reversion

> [!info] Wofür
> Diese Datei 1:1 an den QuantPad-Agenten geben. Sie enthält Profil, Ziel, Constraints, die konkrete Strategie und die exakten Test- + Output-Anweisungen (inkl. Prop-Firm-Pass-Wahrscheinlichkeit). Bewusst auf Englisch für den Agenten.

---

## COPY EVERYTHING BELOW THIS LINE INTO QUANTPAD

---

# BUILD BRIEF: Regime-Filtered Intraday VWAP Mean-Reversion Strategy

## 1. Who I am and what I want

I am a systematic retail futures trader and software developer. I am building my
first serious trading capital (target: +10,000 EUR) **through proprietary trading
firms** (Topstep, Apex), because I do not yet have large personal capital. I need
a strategy that fits prop-firm rules and produces **consistent** results.

**My priorities, in order:**
1. High win rate (target 55-75%).
2. High trade frequency (ideally multiple trade opportunities per week, intraday).
3. Reward-to-risk <= 1:1 (target is closer than the stop) — but with a HARD,
   well-defined stop on every trade.
4. Absolute prop-firm compatibility (see constraints).

I am not looking for a moon-shot trend system. I want a high-hit-rate,
mean-reverting, prop-survivable edge.

## 2. Hard constraints (non-negotiable)

- **Intraday only.** Every position is opened and closed the same session. NO
  overnight holds, NO multi-day holds.
- **Single instrument** (one contract at a time), automatable.
- **Prop-firm rules must hold:** respect a daily loss limit and an intraday
  **trailing max drawdown** (the drawdown follows peak equity in real time,
  including open/unrealized P&L — not just closed-trade equity).
- **Hard stop on every trade.** No averaging down, no "hold until it reverts".
- **Consistency rule friendly:** no single day should be a large share of total
  profit (prop firms often require the best day to be < 30-50% of net profit).

## 3. The strategy to build

**Concept:** Intraday mean reversion to the session VWAP, filtered by a
trend/range regime classifier so that reversion trades are only taken when the
market is NOT trending (trend days are the #1 killer of high-win-rate reversion).

**Academic basis:** intraday time-series / VWAP reversion + regime conditioning.
Reference concepts (SSRN): 4708400 (Requejo, TSI mean reversion, walk-forward
method), 5807282 (intraday time-series reversal on indices), 6087107 (Bhatti,
regime-conditioned mean reversion), 6438039 (Lee, VWAP regime classification),
4878676 (Vu & Bhattacharyya, stop-loss impact on mean reversion).

**Instrument:** Primary **MNQ** (Micro Nasdaq-100 future), RTH session only.
Also validate the same rules out-of-sample on **MES** (Micro S&P 500).

**Entry signal (VWAP Z-score):**
- Anchor VWAP at the RTH open.
- Deviation = price − VWAP, normalized to a z-score using intraday volatility
  (rolling std of (price − VWAP) or an ATR-based sigma).
- Go **long** when z <= −Z_ENTRY (price stretched below VWAP); go **short** when
  z >= +Z_ENTRY. Optimize Z_ENTRY in a sensible range (e.g. 1.5 – 3.0).

**Exit / target (this is what makes RR < 1 with high win rate):**
- Target = reversion back toward VWAP (e.g. z returns to ~0, or a configurable
  fraction of the deviation). Target distance is CLOSER than the stop.
- **Hard stop** = fixed distance beyond entry (e.g. k × sigma), sized so that
  target/stop (RR) is in the 0.5 – 1.0 range.
- **Time stop** and forced **flat at end of RTH**.

**Regime filter (THE CORE — do not skip):**
- Only take reversion trades when the market is in a range / mean-reverting
  regime. Test at least two filters and keep the best:
  (a) trend strength below a threshold (e.g. ADX < 20-25),
  (b) higher-timeframe VWAP/EMA slope near flat,
  (c) a realized-volatility or efficiency-ratio regime measure.
- Skip the first ~5-15 min after the open (opening volatility) and avoid major
  scheduled macro releases (FOMC, CPI, NFP) if feasible.

**Parameters to optimize (via walk-forward, not full-sample):**
Z_ENTRY, target (z_exit / deviation fraction), stop distance, regime threshold,
session window, max trades per day.

## 4. What to test and output (run ALL of this)

**Data:** intraday 1-minute (or finer) RTH bars, as many years as available
(ideally 2016-2025).

**A) Walk-forward out-of-sample (primary honesty check):**
- Rolling in-sample optimization window (e.g. 24 months) → out-of-sample window
  (e.g. 6 months), stepped forward and stitched into one OOS equity curve.
- Optimization objective should favor a SMOOTH edge (e.g. SQN or Sortino), not a
  few outlier trades.
- Report whether the chosen parameters are STABLE across windows (instability =
  overfitting warning).

**B) Realistic fills (mandatory — no optimistic simulation):**
- Limit/entry fills only when price ACTUALLY reaches the level (real touch); no
  "phantom" fills at a price that was never traded.
- On a bar where both stop and target could be hit, assume the STOP hit first
  (conservative).
- Include costs: at least 1 tick/side slippage + realistic commission per
  round-turn. Report metrics BOTH gross and net of costs.

**C) Full metric set (gross AND net):**
win rate, avg R, avg win R, avg loss R, expectancy (R), profit factor, Sharpe,
Sortino, CAGR, total return, max drawdown, number of trades, trades per week,
max winning streak, max losing streak, and the **MAE distribution** (per-trade
maximum adverse excursion in R, including winning trades).

**D) Monte-Carlo simulation:**
- 5,000+ resamples of the OOS trade sequence (prefer a block / stationary
  bootstrap to respect autocorrelation and losing-streak clustering).
- Output distributions for: max drawdown (in R and in $ per contract), longest
  losing streak, terminal equity, and the probability of a losing year.

**E) PROP-FIRM PASS PROBABILITY (key deliverable):**
- Simulate the full prop lifecycle (evaluation → funded) for at least:
  **Topstep 50k** and **Apex 50k** (state the exact rule assumptions you use —
  profit target, trailing drawdown, daily loss limit — and note that prop terms
  change, so they must be verified).
- Model the trailing drawdown against **intraday equity including open-trade
  MAE**, not just closed-trade equity (a winning trade can still breach the
  trailing DD if it first drew down enough).
- Output, per contract size: **probability of PASSING the evaluation**,
  probability of blowing the funded account, expected payout per year, and the
  optimal / safe contract size at a chosen breach probability (e.g. < 5%).
- Give one clear headline number: **"Probability of passing a [firm] challenge
  with this strategy: X%."**

**F) Robustness:**
- Parameter sensitivity heatmaps (e.g. Z_ENTRY × stop, regime threshold × target).
- Cross-instrument check on MES with the SAME parameters.

## 5. Honesty requirements (learned the hard way)

- No look-ahead bias, no phantom fills, conservative same-bar stop-before-target.
- If the edge only exists in-sample (disappears in walk-forward OOS or after
  costs), SAY SO CLEARLY — do not present the in-sample number as the result.
- If chosen parameters jump around between walk-forward windows, flag it as an
  overfitting risk.

## 6. Deliverables

1. Best parameter set (from walk-forward).
2. Stitched out-of-sample equity curve (gross and net).
3. All metric tables (gross and net).
4. Monte-Carlo distributions (drawdown, losing streak, terminal, prob of loss).
5. Prop-firm pass-probability table (Topstep 50k, Apex 50k) with the headline
   pass probability.
6. A clear, honest **go / no-go verdict**: is this a real, prop-survivable edge
   after realistic costs and fills, or not?

---
