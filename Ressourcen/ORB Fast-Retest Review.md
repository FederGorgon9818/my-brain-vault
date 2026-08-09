---
tags:
  - ressource/trading
  - trading/orb
  - review
erstellt: 2026-07-05
---
# 🔍 Code-Review: ORB Fast-Retest Pipeline

Review der Arbeit in `Quantpad Data/` (mit QuantPad-Agent erstellt). Kombiniert Zarattini/Aziz (ORB-Richtung) + Pineda (Fast-Retest-Entry) auf NQ-Futures. Siehe [[Backtesting & MultiCharts]], [[Trading-Profil]], [[ORB Paper (Zarattini, Aziz, Pineda)]].

## Was gebaut wurde (verstanden)
- `orb_retest.pine` – Live-Strategie (TradingView, Webhook-fähig)
- `orb_retest_backtest.py` – Kern-Backtest + Paper-2-Validierung
- `sweep.py` – Parameter-Grid (bestätigt: OR5/Retest20/Stop0.25/3R ist globales Optimum)
- `walkforward.py` – rollierende WF-Optimierung (SQN-Objective), OOS gestitcht, Heatmaps
- `stats_montecarlo.py` – Kosten + MC-Bootstrap (DD/Streak/Terminal)
- `prop_analysis.py` / `prop_lifecycle.py` / `prop_portfolio.py` – Prop-Sizing (3 Objectives)

## Stärken (echt)
- **Richtige WF-Methodik**: Re-Optimierung pro Fenster, OOS gestitcht, Kosten NUR auf OOS-Trades. Kein In-Sample-Selbstbetrug bei der Headline-WF-Zahl.
- **Paper 2 auf eigenen NQ-Daten bestätigt**: Fortsetzungsrate fällt monoton mit Retest-Zeit. Unabhängige Verifikation, stark.
- **Geringe Renditekonzentration** (größter Tag 1,2% des Netto): kein Lucky-Trade-Artefakt, gut für Prop-Consistency.
- **Ehrliche Deklaration** brutto vs netto, mehrfach "Prop-Terms selbst verifizieren".

## Schwachstellen (nach Impact sortiert)
1. **Fill-Optimismus beim Retest-Entry (wichtigster Punkt).** Retest triggert, wenn Low bis `level*(1+tol)` (~0,05% = ~9 Pkt bei NQ ÜBER dem Level) kommt, aber Entry wird bei exakt `level` angenommen. Kurs muss das Level real nie berührt haben → Phantom-Trades + zu günstige Fills. Bei Median-R ~14 Pkt sind 9 Pkt viel. **Fix:** Fill nur wenn Low ≤ level (echter Touch), sonst kein Trade. Danach neu rechnen. (Pine ist realistischer: Market-Order auf nächster Bar.)
2. **Trailing-DD nur auf geschlossenen Trades.** Alle Prop-Sims ignorieren die intratrade-MAE. Echte Prop-Trailing-DD läuft oft intraday mit → ein Trade, der erst gegen dich läuft, kann die DD reißen, obwohl er als Gewinner schließt. Breach-Wahrscheinlichkeiten & "sichere" Kontraktzahlen sind dadurch zu optimistisch.
3. **"Unabhängige Instrumente" unrealistisch.** `prop_portfolio.py`: rosiger Fall (0,3% Verlust, ~12k/Jahr) nimmt NQ/ES/YM/RTY als unkorreliert an. Real intraday ~0,8+ korreliert. Wahrheit liegt nah am "korrelierten" Fall.
4. **8-MNQ-"Optimum" = Eval-Churning, 39% Blow-up-Rate.** `prop_lifecycle.py` maximiert EV durch akzeptierte Konten-Verluste. Aggressiv, hochvariant, und systematisches Konten-Verheizen verstößt oft gegen Prop-AGB. Realistisch: 2-3 MNQ (safe-Ansätze).
5. **i.i.d.-Bootstrap** unterschätzt Regime-Cluster; setzt voraus, dass die Edge weiter besteht (kein Alpha-Decay modelliert).
6. **Kern-Backtest & Pine ohne Kosten** (Headline 677% ist brutto). Slippage 1 Tick/Seite ist für Retest/Stop-Fills eher knapp.
7. **roll_adjust="none" intraday**: an Roll-Tagen ggf. verzerrte OR-Levels. Klein.

## Verdict
Solide, ehrliche, methodisch saubere Arbeit. ABER Kernzahlen am oberen Ende. **Vor echtem Einsatz: Punkt 1 fixen + neu backtesten, Punkt 2 mit MAE-Tracking nachrüsten.** Überlebt die Edge das, ist es ein ernstzunehmendes System.

## ⚠️ UPDATE 05.07.2026: Fix durchgeführt — Edge verschwindet

Alle Fixes lokal umgesetzt in `Quantpad Data/fixed/` (kein QuantPad nötig, alles auf gecachten Parquet-Daten). Kompletter Re-Test:

### A) Fill-Fix allein (2019-2025, gleiche Original-Parameter OR5/Retest20/Stop0.25/3R)
| Kennzahl | ALT (Bug) | NEU (echter Touch) |
|---|---|---|
| Trades | 393 | 319 (74 Phantom-Trades entfernt) |
| Gesamtrendite | +662% | **-7,4%** |
| Sharpe | 2,12 | **-0,04** |
| Profit-Faktor | 1,87 | **0,99** |

### B) Voller Parameter-Sweep mit fixer Engine
Nur 35/72 Kombinationen noch positiver Sharpe. Alte "beste" Kombi (OR5/20/0.25/3R) jetzt im unteren Drittel. Neue beste Kombi (OR=30, Retest≤10, Stop 0.25, EoD): Sharpe nur noch 0,59, PF 1,63, N=116 — deutlich schwächer, und **nicht** mehr das gleiche Setup.

### C) Walk-Forward OOS mit fixer Engine (die ehrliche Zahl)
| Kennzahl | ALT (Bug) | NEU (fix) |
|---|---|---|
| Gesamtrendite OOS | +1.094% | **-32,4%** |
| CAGR | 36,4% | **-4,8%** |
| Sharpe | 2,02 | **-0,36** |
| Win-Rate | 37,75% | 19,6% |
| PF | 1,82 | **0,84** |
| Netto (Kosten) CAGR | 29,8% | **-6,8%** |
| Netto Sharpe | 1,73 | **-1,42** |

**Zusätzlich:** Parameterwahl springt jetzt wild zwischen Fenstern (OR 5→15→30→5...) statt stabil zu bleiben — genau das Gegenteil vom ursprünglichen "kein Overfitting"-Argument.

### D) MAE-Check
Trades liefen im Schnitt 1,19R gegen die Position (Max 4,21R durch Gap-Through über Stop), selbst Gewinner im Schnitt 0,48R im Minus davor. Zeigt: reales Risiko war schon vorher unsichtbar, nicht nur die Fill-Frage.

### E) Paper-2-Kernaussage bestätigt sich weiterhin ✅
Fortsetzungsrate fällt weiter sauber monoton mit Retest-Zeit (56% bei 0-10min → 12,8% bei >60min), auch mit korrigierter Retest-Erkennung. **Die Marktbeobachtung aus dem Paper ist real.** Nur die konkrete Strategie (dieser Entry/Stop/Target-Aufbau) hat die Edge nicht überlebt.

### Entscheidung
MC/Prop-Sizing-Skripte NICHT mit MAE/Block-Bootstrap nachgerüstet — macht keinen Sinn, für eine Strategie zu sizen, die OOS Geld verliert. Punkte 3 (Korrelation) und 4 (Blow-up-Rate) sind damit vorerst irrelevant.

## Nächste Schritte
- [x] Fill-Logik fixen und neu rechnen — erledigt, Edge verschwindet
- [ ] Entweder: neue Filter/Variante auf Paper-2-Signal aufbauen (Kernsignal ist real) und sauber neu testen
- [ ] Oder: dieses Setup als falsifiziert archivieren, anderes Paper/Ansatz probieren
- [ ] Code liegt in `Quantpad Data/fixed/` (orb_core_v2.py = wiederverwendbare korrigierte Engine)
