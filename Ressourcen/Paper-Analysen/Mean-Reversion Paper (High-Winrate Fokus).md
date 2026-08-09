---
tags:
  - ressource/paper
  - trading/mean-reversion
erstellt: 2026-07-05
status: gefunden-zu-analysieren
---
# 📄 Mean-Reversion Paper (High-Winrate / 10k-Fokus)

Ziel-Profil (Max, 05.07.2026): **hohe Win-Rate, hohe Frequenz, RR ≤ 1:1, prop-firm-tauglich, ein Index-Instrument, intraday.** Für den Aufbau der ersten 10.000€. Siehe [[Trading-Profil]], analysierbar via [[paper-edge]].

## Shortlist (passt zum Profil)

### 1. Intraday Time Series Reversal ⭐
- Overnight-Return sagt Reversion der ersten halben Stunde bei US-Index voraus. Ein Instrument, intraday, kein Overnight-Hold.
- **SSRN 5807282:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5807282
- Caveat: nur US-Indizes, nach 2010ern schwächer → Decay-Risiko.

### 2. Overnight-Intraday Reversal Everywhere
- Reversal über viele Assets inkl. Indizes (Guofu Zhou, seriös).
- **SSRN 2730304:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2730304

### 3. Momentum Exhaustion & Fair Value (VWAP) Reversion
- Intraday-Reversion zum VWAP mit Momentum-Regime-Filter.
- **SSRN 6454659:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6454659
- Caveat: FX-fokussiert, unabhängiger Autor.

### 4. Mean Reversion via True Strength Index (SPY/QQQ)
- Direkt auf Wunsch-Instrumenten, praxisnah.
- **SSRN 4708400:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4708400
- Caveat: Praktiker-Niveau.

## Passt NICHT (bewusst aussortiert)
- **Zarattini "Beat the Market" (SPY Momentum, 4824172):** Win-Rate niedrige 40er, konvexer Payoff, RR > 1. Gegenteil des Profils.
- **Cross-Sectional Reversal (Da/Schaumburg, Blitz, Brogaard):** handeln hunderte Aktien long/short gleichzeitig. Auf Prop-Konto nicht umsetzbar.

## Ehrliche Warnungen zum Profil
1. **Mean Reversion hat oft keinen natürlichen Stop** → harter Intraday-Stop Pflicht, sonst frisst 1 Ausreißer die Win-Rate auf (Prop-Killer).
2. **Index-Reversal-Edges sind dünn** (30-50 bps/Woche vor Kosten) → nach Slippage/Kommission wenig. Sauber sizen, nicht überhebeln.
3. **Ehrlich testen** mit korrigierter Engine (`Quantpad Data/fixed/orb_core_v2.py`-Ansatz), Fill-Realismus vor jedem Euro. Lektion aus [[ORB Fast-Retest Review]].

## Merge mit Fable-5-Antwort (05.07.2026)
Zweites Modell (Fable 5) unabhängig befragt → **gleiche Strategieklasse** (Regime-gefilterte Intraday Mean Reversion). Starke Bestätigung. Kernidee von Fable übernommen: **Der Regime-Filter ist NICHT optional, sondern das Herzstück** (Trendtage killen High-Winrate-Reversion).

### Als System denken (Bausteine)
- **Signal:** volatilitätsnormalisierter Z-Score / VWAP-Abweichung
- **Regime-Filter (Kern!):** unterscheidet Trend- vs. Reversion-Regime → nur in Reversion traden
- **Risk:** harter Intraday-Stop, vol-adjustiertes Sizing
- **Backtest:** Walk-Forward gegen Curve-Fitting, ehrliche Fills

### Zusätzliche Paper von Fable (verifiziert real)
- **Bhatti – Regime-Conditioned Mean Reversion FX (SSRN 6087107):** Z-Score + Multi-TF-Momentum-Filter + MQL5-Prototyp (MT5 = Prop-Standard). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6087107
- **Vu & Bhattacharyya – Mean Reversion auf QuantConnect (SSRN 4878676):** quantifiziert **Stop-Loss-Einfluss** (direkt relevant für RR<1). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4878676
- **Lee – VWAP Regime Classification (SSRN 6438039):** der Regime-Filter-Baustein. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6438039
- Fables Caveat: Bhatti/Lee sind FX-fokussierte 2026-Preprints, unabhängige Autoren → weniger validiert als die Guofu-Zhou-Paper oben.

### Beide Modelle einig bei
- **Requejo TSI (4708400)** → Pflichtlektüre (Walk-Forward-Methodik).
- Reine Trend/Breakout-Paper passen NICHT (inkl. Zarattini VWAP "Holy Grail" 4631351 = Trend, nicht Reversion).

## Empfohlener Leseplan (kombiniert)
1. **Requejo 4708400** (beide einig, Methodik + SPY/QQQ)
2. **Intraday Time Series Reversal 5807282** (bester akademischer Single-Index-Fit)
3. **Lee 6438039 + Bhatti 6087107** (Regime-Filter = Kern)
4. **Vu 4878676** (Stop-Loss-Impact quantifiziert)

## Nächste Schritte
- [x] Requejo 4708400 → per `/paper-edge` getestet 29.07.: **NO-GO** (nicht robust, n=21, 2 Trades/Jahr) → [[TSI Mean Reversion (Requejo 4708400)]]. PDF bleibt hinter SSRN-Paywall (403).
- [ ] Paper 5807282 besorgen → `/paper-edge` drüberlaufen
- [ ] Regime-Filter zuerst bauen (der Kern), dann Signal + harter Stop
- [ ] Ehrlich backtesten (echte Fills, Kosten, MAE) bevor Prop-Konto
