---
tags:
  - bereich/trading
  - trading/portfolio
erstellt: 2026-07-07
---
# 🧩 Portfolio-Simulator

⬅️ [[Strategie-Logbuch]] · [[Eval-Passing]] · Update: 2026-08-09 (#067)

> [!warning] **KORREKTUR 09.08. (#067): Buch = 6 Beine, alle älteren ORB-Zahlen unten sind Look-ahead-verseucht.**
> Die Breakout-ORBs (Bein 3/8/9) hatten ehrlich gemessen keinen Edge (Entry-/Filter-Look-ahead, siehe [[Strategie-Logbuch]] #066/#067) und sind raus. **Ehrliches 6-Bein-Buch: 57% / ~86d (frac 0.10, E8 3000/2000 trailing)** statt der geglaubten 61%/81d. ORB-Fade bleibt (echt, +0,063 expR) und wird live auf ruhende Limit-Orders am Level umgestellt. Frontier-Details: `orb_honest_frontier_066.json`.

> [!success] KÄFIG-UPDATE 04.08. (Hebel-Scan): **BULENOX 50k EOD** schlägt Lucid — $2.500 EOD-Trailing statt $2.000 = **+7 Punkte**. Algo erlaubt, NT/Tradovate, ~$19-40/Mon. mit Codes. Sizing-Policy-Suche (60+ Policies, Train/Test): simples Cushion-Sizing bereits optimal. Details [[Strategie-Logbuch]] #032.

> [!success] **7. BEIN 04.08.: RV_leadlag_NQES (VERDICT A)** — die 5. Familie (Relative Value) ist besetzt! NQ führt, ES folgt. Vom Auto-Fit selbstständig aufgenommen. **7-Bein-Buch auf Bulenox: 66%/~93d (frac 0.10-0.12) · 60%/~55d (0.18) · 56%/~43d (0.22).** Alle 5 Familien aktiv: Trend (Momentum, ORB-Break) · Reversion (ORB-Fade, RTY-Gap) · Intraday Bias (Power-Hour, Asia-Dir) · **Relative Value (Lead-Lag)** · Swing (bewusst leer, Prop-intraday). Details [[Strategie-Logbuch]] #033.

> [!important] **Betriebspunkt-Entscheid 29.07. (Max): frac 0.22 → 52% / ~45 Tage** (E8 50k, 8-Bein-Buch).
> Löst den 27.07-Entscheid (0.18 → 56%/77d auf E8) ab, gleiche EV-Logik konsequent weitergedacht: erwartete **Zeit-bis-Funded inkl. Fehlversuchen ~87 Tage statt ~138** (45/0,52 vs. 77/0,56), Mehrkosten nur ~0,13 erwartete Versuche × $150 ≈ $20. Kumulativ 2 Versuche ≈ 77%. 0.22 ist bewusst der letzte Frontier-Punkt **über 50%** — 0.26/0.30 wären nach reiner T/p-Mathe nochmal schneller, lehnen sich aber zu weit auf die Sim-Genauigkeit (Modellrisiko + Varianz). Umgestellt: `funded_finalize.py` (FRAC), `portfolio.json`, Portfolio-Tab. **Offen: RiskGuard CushionFrac 0.22 beim Eval-Start** (Ticket im Lab). Verbessert sich das Buch weiter, Frontier neu anschauen.

> [!important]- ~~Betriebspunkt-Entscheid 27.07. (Max): SPEED-Pfad, frac 0.18 → 60% / ~55 Tage.~~ (abgelöst 29.07.)
> EV-validiert: Auf **Zeit-bis-Funded** schlägt der schnelle Pfad den sicheren klar (~75-85 Tage erwartet inkl. Fehlversuchen vs. ~130 Tage beim 65%-Pfad, weil auch langsame Fehlversuche ~3 Monate fressen). Kumulativ: 2 schnelle Versuche ≈ 84%. Monatsgebühr macht schnelle Versuche zusätzlich billiger. Portfolio-Tab + `portfolio.json` umgestellt. **RiskGuard-Parameter CushionFrac beim Eval-Start auf 0.18 setzen** (Sim läuft eh mit fixer Size 1).

> [!success] Funded-Portfolio (6 Beine) — Report `PORTFOLIO_optimized`
> **Buch: NQ_Momentum + NQ_LastHour + NQ_ORB-Breakout + RTY_Gap-fade + NQ_ORB-fade + NQ_Asia-Dir-USopen** (Lucid-Recheck 04.08.: alle 4 Bank-Kandidaten ES-Mom/Asia-Break/Gap-cont/Overnight verschlechtern → Buch bleibt).
> Note C · PF 1,17 · RoDD 8,53 · 427 Trades/Jahr · |Korr| 0,07.
>
> **Lucid Flex 50k Frontier (Target $3000 / DD $2000 EOD-Trailing):**
>
> | Frac | P(pass) | Tage | |
> |--:|--:|--:|--|
> | 0.10-0.12 | **58%** | ~104 | Decke (langsamer bringt nichts) |
> | **0.14** | **56%** | **~101** | Betriebspunkt |
> | 0.18 | 53% | ~72 | |
> | 0.22 | 49% | ~51 | schnell |
>
> **Ehrlich: >60% pro Versuch ist bei $2.000 DD NICHT erreichbar** (Decke 58%). Der Drop von 65% kommt allein von DD $2.500→$2.000 (~8 Punkte), nicht von den Strategien.
>
> **Der echte 60%+-Weg = Lucids Einmalgebühr ausnutzen (Mehrfach-Versuche):**
> - 50k: 2 Versuche kumulativ **81%**, 3 Versuche **92%** (je ~$150-190 einmalig)
> - **25k-Konten: 50% in ~27 Tagen pro Versuch** (Min-Size-Effekt, Sizing-Knopf wirkungslos) → **2× 25k PARALLEL: ≥1 Pass ≈ 75% in ~4-6 Wochen** für ~$190 gesamt. Copier/Bots sind bei Lucid explizit erlaubt.
> - ⚠️ 25k-Caveat: Eval-Consistency 50% = bester Tag ≤ $625 → Risk-Guard muss nahe am Target die Size drosseln. Exakte 25k-Regeln (Target/DD) vor Kauf verifizieren.

> [!important] Der größte Pass-Hebel ist die FIRMEN-STRUKTUR, nicht das Sizing
> First-Passage-Physik: +$3000 vor −$2500. Driftlos = 45%, wir haben ~+12 Punkte Drift.
> - **Trailing DD:** Boden wandert mit dem Gewinn hoch (wird enger) → max ~59%, 60%/<50d **unmöglich**.
> - **Static DD:** Boden bleibt fix bei −DD → voller Drift-Effekt → **61-64% / <50d machbar**.
> - **Regel für Funded/Eval:** **Static-DD-Anbieter wählen** (Tradeify~~/MFFU~~ Static-Pläne; ⚠️ 28.09.2026: MFFU hat keinen Static-Plan mehr, alle Pläne trailen, siehe [[MFFU 50k Pläne (Regeln + Wahl)]]), nicht Trailing. Das ist +7 Punkte Passchance geschenkt. Mehr DD-Puffer ($3000 statt $2500 static) = nochmal +3-4 Punkte.
> - 5. Bein **NQ_ORB-fade** dazu (Reversion, |Korr| 0,08) hob 61%→63% und RoDD auf 9,2. ES-Momentum brachte NICHTS (korreliert mit NQ-Mom).
>
> **Discovery (ehrlich, 12 Versuche → 5 Überlebende):** NQ = alle 3 (Momentum/ORB-Breakout/LastHour) · ES = nur Momentum (schwach, rausgeworfen) · RTY = nur Gap-fade · **YM = nichts robust**. Einzelreports im Lab.

> [!note] Cross-Instrument-Test (per-Instrument angepasste Strategien) — 2026-07-15
> **Frage:** Statt NQ-Config stumpf auf ES/YM/RTY zu klatschen — jedem Instrument seine EIGENE getunte Mechanik geben (ehrlicher OOS-Split). Ergebnis des Tuners (`instrument_tune.py`):
> - **NQ** → ORB-Breakout (OOS +9,1%) + Momentum (OOS +5,5%) — trendet
> - **RTY** → **Gap-Fade / Reversion** (OOS +5,0%, PF 1,15) ✅ echter Fund, Small Caps reverten
> - **ES** → Momentum, aber schwach (OOS +1,0%)
> - **YM** → nichts robust (Edge kippt IS↔OOS) → gekillt
>
> **Aber das Cross-Instrument-Buch VERLIERT gegen NQ-only:**
>
> | Buch | \|Korr\| | RoDD | Pass/Tempo |
> |---|--:|--:|--|
> | **NQ-only, 4 Mechaniken** | **0,08** | **6,2** | 56% / ~86d |
> | Cross-instr (NQ/ES-Mom + RTY-fade) | 0,15 | 2,4 | 52% / ~147d |
>
> **PRINZIP (merken):** Diversifikation kommt aus der **MECHANIK (Trend vs. Reversion)**, nicht aus dem **Instrument**. US-Index-Futures korrelieren ~0,9, gleiche Familie über Instrumente feuert an denselben Tagen → Korrelation STEIGT statt zu fallen. RTY-Gap-Fade bleibt als Keeper für eine Non-NQ-Risikostreuung (Funded-Phase), aber fürs schnelle Eval-Passen bleibt das NQ-Multi-Mechanik-Buch Champion.

> [!warning] Ehrliche Kill-Findings aus dem Optimizer-Lauf
> - **Multi-Instrument-Momentum ist tot.** Die Momentum-Edge ist **NQ-spezifisch**: ES nur +1,7%, YM −0,4%, **RTY −2,8% (negativ)**. „Gleiche Mechanik über 4 Indizes stapeln" senkt die Passchance (All-4-Momentum: nur 42%). Frequenz ohne Edge hilft nicht.
> - **ORB auf ES ist Müll** (edge −15%, PF 0,53) → raus.
> - **PowerHour verwässert** (edge +0,8%, Sharpe fällt auf 0,73) → nicht ins finale Buch.
> - **Warum Note C?** Die Note misst *pro-Trade-Qualität* (Edge/Sharpe/PF/MC), nicht Pass-Speed. Ein Portfolio verdünnt die Einzel-Edge (Mix aus +5,6% und +1,1%) → PF ~1,19 → C. Das ist für ein Portfolio **normal und ok** — RoDD 7,07 + Sharpe 1,03 + |Korr| 0,09 sind echt gute Portfolio-Werte. Note hochprügeln = Overfitting (verstößt gegen [[Simplex beats Komplex]]).

---

## 📜 Historie: Apex-Analyse (2026-07-07)

> [!tip] Idee
> Mehrere dekorrelierte Beine gleichzeitig auf 1 Apex → mehr Frequenz + glattere Equity → höhere kombinierte Passchance im 3-Wochen-Fenster.

> [!warning] Ehrliches Fazit (WICHTIG)
> Die Beine sind **echt dekorreliert** (|Korr| ≤ 0,23, ORB-fade sogar negativ) → Portfolio-Konzept strukturell bestätigt. **ABER: Diversifikation erzeugt keine Edge.** Max erreichbare Apex-Passquote:
> - **ORB-breakout solo: 61%** (aber ~9 Mon, langsam)
> - **ORB-breakout + ORB-fade-NR7: 53% in ~77 Tagen** ← bester Kompromiss (Report `PORTFOLIO_balance`)
> - Mehr Beine → schneller (bis ~26 Tage) aber **niedrigere** Passquote (38-42%), weil schwache Beine (PowerHour, Overnight) verwässern.
> - **70% in 3 Wochen ist mit den aktuellen Edges NICHT erreichbar** — weder solo noch im Portfolio.
> - **Regel: Qualität > Quantität.** Zwei starke, dekorrelierte Beine schlagen fünf mittelmäßige. Schwache Beine (expR < 0,05) rausnehmen.
> - Weg zu echten 70%: **stärkere Einzel-Edges** (neues Alpha / bessere Daten), nicht mehr Kombination. ODER ~55% akzeptieren + Apex-Cheap-Reset (PFPL) → über mehrere Versuche trotzdem positiv.

## 🏆 Gewinner-Kombination

**Momentum + ORB-fade-NR7**

- **Apex P(pass): 44%** @ 2 Micro/Bein
- Ø Tage bis Pass: **61** (Median 57)
- Note C · Sharpe +1.14 · 116 Trades/Jahr kombiniert
- Report im Lab: `PORTFOLIO_best`

## Korrelation der Beine (Tages-$, 0 = unkorreliert)

```
                ORB-breakout  Momentum  PowerHour  ORB-fade-NR7  Overnight-fade
ORB-breakout            1.00      0.08       0.04         -0.06            0.04
Momentum                0.08      1.00       0.23         -0.07            0.02
PowerHour               0.04      0.23       1.00          0.05           -0.00
ORB-fade-NR7           -0.06     -0.07       0.05          1.00           -0.01
Overnight-fade          0.04      0.02      -0.00         -0.01            1.00
```

## Kombis nach Apex-Speed (Top 8)

| Kombination | Apex P(pass) | Size | ~Tage | Objective |
|---|--:|--:|--:|--:|
| Momentum + ORB-fade-NR7 | 34% | 7u | 9 | 0.441 |
| ORB-breakout + Momentum + PowerHour + ORB-fade-NR7 | 33% | 4u | 12 | 0.433 |
| ORB-breakout + Momentum + ORB-fade-NR7 + Overnight-fade | 33% | 4u | 12 | 0.432 |
| ORB-breakout + Momentum + ORB-fade-NR7 | 33% | 5u | 14 | 0.430 |
| Momentum + PowerHour + ORB-fade-NR7 | 33% | 4u | 13 | 0.427 |
| ORB-breakout + ORB-fade-NR7 + Overnight-fade | 33% | 7u | 9 | 0.425 |
| ORB-breakout + Momentum | 33% | 6u | 12 | 0.425 |
| ORB-breakout + Momentum + PowerHour | 32% | 6u | 7 | 0.421 |

## Einzel-Beine (Baseline)

| Bein | Apex P(pass) | Size | ~Tage | Objective |
|---|--:|--:|--:|--:|
| Momentum | 30% | 5u | 16 | 0.391 |
| Overnight-fade | 30% | 8u | 8 | 0.391 |
| PowerHour | 27% | 6u | 16 | 0.350 |
| ORB-fade-NR7 | 36% | 8u | 40 | 0.191 |
| ORB-breakout | 51% | 8u | 149 | 0.072 |

## Bein-Konfigurationen

- **Momentum** (`ts_reversal`): `{'rev_side': 'momentum', 'rev_base': 'open', 'rev_signal_min': 15, 'rev_exit': 'eod', 'rev_thr': 0.003, 'rev_stop_mult': 0.75}`
- **ORB-fade-NR7** (`orb`): `{'or_min': 15, 'orb_side': 'fade', 'stop_frac': 0.4, 'target_mult': None, 'nr7_filter': True}`