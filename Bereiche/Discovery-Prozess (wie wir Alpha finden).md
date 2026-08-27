---
tags:
  - bereich/trading
  - trading/alpha
erstellt: 2026-07-30
---
# 🔬 Discovery-Prozess: wie wir unsere besten Trades gefunden haben

⬅️ [[Alpha-Suche]] · [[Backtest-Engine]] · [[Strategie-Logbuch]] · **Seit 18.08.2026 läuft die Suche als Dauerprozess: [[Discovery-Runner v2]]** (Register, Prämisse-Stufe, Plateau/Bootstrap-Gates, Buch-Marginal zuerst)

> [!important] Kernbotschaft
> Unser Moat ist **nicht** eine große Edge. Es ist **(1) ehrliches Backtesting** (killt die Schein-Edges, die andere für echt halten) **+ (2) Diversifikation vieler dünner, unkorrelierter Edges**. Kein einzelnes Bein ist beeindruckend — das Buch als Ganzes schon.

## 1️⃣ Der Prozess (6 Schritte, so entstanden alle 8 Beine)

1. **Research-Prior pro Instrument** — kein blindes Grid. Wir wissen vorher, was wo funktionieren *sollte*: NQ = Momentum/Breakout (High-Beta-Tech), ES = milder Drift, RTY/YM = mean-reverting (Small-Cap/Blue-Chip). **Jeder Mechanismus braucht ein dokumentiertes „Why" VOR dem Test** (Data-Mining-Schutz).
2. **Kleine Parameter-Grids** (9-24 Configs pro Mechanismus) — *bewusst flach*. Tiefe Grid-Suche = Overfitting. Simplex beats Komplex.
3. **Ehrliche Engine** — Real-Fills (Entry auf nächster Bar-Open, Stop-before-Target, echte Touch-Logik), **Kosten in JEDER Zahl** (Slippage + Kommission), **MAE pro Trade** (echtes Intraday-Risiko, auch bei Gewinnern).
4. **IS/OOS-Split** (OOS ab 2024-01-01) + Skepsis-Gates: Edge muss IS **UND** OOS positiv sein, OOS netto > 0. Klein-N bekommt Skepsis-Aufschlag.
5. **Auto-Fit** — ein Bein kommt nur ins Buch, wenn es die **Portfolio-Passquote** hebt, nicht wenn es einzeln gut ist. Korrelations-Check gegen das bestehende Buch.
6. **Alles gegen das Eval-Objektiv** (P(pass) schnell = First-Passage-Problem), **nicht gegen Sharpe**.

## 2️⃣ Was tatsächlich funktioniert hat (das 8-Bein-Buch)

| Bein | Edge vs Baseline | PF | Warum es lebt |
|---|---|---|---|
| **ORB-Vol-Scalp (NQ)** | +8,7% | 1,43 | Zarattini RVOL: Edge sitzt im relativen Volumen |
| **Asia-Dir (NQ)** | +6,7% | 1,35 | Session-übergreifendes Momentum (Gao et al.) |
| **NQ-ES Lead-Lag (ES)** | +6,6% | 1,37 | Info-Diffusion: großer Bruder zieht, kleiner folgt |
| Momentum (NQ) | +4,3% | 1,21 | Früh-Move zeigt Positionierung, Trägheit trägt |
| Gap-Fade (RTY) | +4,2% | 1,18 | Small-Cap-Gaps überschießen, reverten |
| ORB-Breakout (NQ) | +3,6% | 1,16 | Order-Flow-Entladung nach Open (mit Trend/VWAP/Vol) |
| Power-Hour (NQ) | +2,4% | 1,10 | U-Form des Tages, MOC-Flows |
| ORB-Fade+NR7 (NQ) | +1,1% | 1,07 | Fehlausbrüche an ruhigen Range-Tagen |

**Das Ergebnis:** 490 Trades/Jahr, **avg_corr 0.07** (fast unkorreliert!) → als Portfolio ~52-59% P(pass) auf E8 50k. Die dünnen Edges einzeln wären nutzlos; die **Unkorreliertheit** macht sie wertvoll.

## 3️⃣ Wie tief haben wir gesucht — und wo geht es *ehrlich* tiefer?

**Tiefe kam aus BREITE (Mechanismen × Instrumente), nicht aus feinem Param-Tuning.** Das ist Absicht: tiefer graben in denselben Parametern = Overfitting.

**✅ Bestätigte echte Edges:** ORB+RVOL, Asia-Dir, Lead-Lag, Intraday-Momentum, FOMC-Post (#034), OpEx-Momentum (#049, Bank).

**❌ Ehrliche Friedhof (wichtig — das ist der Moat):** nacktes VWAP-z (keine Edge), Frequenz-Bein (0/98, #043), Break-Even/Trailing-Overlay (#046), TSI-MR (n=21, #047), OpEx-Fade (−22%, #034), **nackte Pivots (negativ, #050)**, **Scalp auf ES/YM (edge −29%! #050)**.

**Wo tiefer graben WIRKLICH lohnt** (aus [[Alpha-Suche]], priorisiert):
1. ~~Cross-Asset / Intermarket (VIX, Bonds/ZN, DXY, Sektor-Breadth) — Daten da, nie getestet. Bester nächster Schritt.~~ **AP61, 18.08.2026: getestet, negativ.** Prämisse direkt gemessen (nicht gesweept) für alle vier Familien: VIX-Level als Filter kein |t|>2, Bonds/ZN-Renditeanstieg kollabiert in OOS (r 0,031→0,007), DXY zeigt durchgehend das FALSCHE Vorzeichen (Dollarstärke ↔ leicht stärkere statt schwächere NQ/RTY-Folgetage), Sektor-Breadth weiterhin keine Datenquelle im Repo. Kein Sweep gefahren, weil keine Prämisse trug (siehe Faustregel unten). Bank: VIX-Spike-Reversion (aus früherer Arbeit, #087/AP49) bleibt der einzige validierte Fund der Familie, Klein-N, offene Buch-Entscheidung AP89.
2. **Event-/Zeitstruktur** — OpEx-Mom + FOMC-Post bestätigt → **kombiniertes Event-Bein** (Backlog).
3. **Regime-Conditioning** bestehender Edges (nur an den richtigen Tagen).
4. **Order-Flow / L2** — da sitzt die echte Ex-Institutional-Edge, braucht aber Tick/L2-Daten (bewusst weggelassen).

**Wo tiefer graben NICHT hilft:** mehr Param-Grids auf bestehenden Mechanismen · mehr Frequenz desselben Mechanismus (#043).

## 4️⃣ Faustregel: wann lohnt Alpha-Arbeit überhaupt? (AP65, Lehre 15, Strategie-Logbuch #073)

> **Kurze Frist = Barrieren-Mathematik, lange Frist = Edge.**

Bei einer Frist, die zu kurz ist, um viele Trades zu sammeln, konvergiert P(pass) gegen `DD/(Target+DD)` — das Buch trägt dann nur noch wenige Prozentpunkte bei, egal wie gut die Beine sind. **Tempo-Ziele sind deshalb primär eine Firmen-/Käfig-Frage, keine Strategie-Frage** (Käfigwahl war in #073 +7 Punkte wert, mehr als jedes Bein). Alpha-Arbeit lohnt sich nur, wenn die Frist lang genug ist, dass eine Edge überhaupt Zeit hat zu wirken.

**Praktisch, vor jedem größeren Discovery-/Sweep-Lauf kurz prüfen:**
1. **In welchem Regime bin ich?** Kurze Frist (Eval-Zeitdruck, wenige Trades bis zur Entscheidung) → am Käfig/Betriebspunkt drehen, nicht am Buch. Lange Frist (Funded-Phase, viele Monate) → hier trägt Edge tatsächlich.
2. **Prämisse vor Parameter-Sweep messen** (Lehre 113, bestätigt AP61): eine einzige Trefferquoten-Tafel oder Korrelationsmessung des unterstellten Mechanismus zeigt in Sekunden, ob die Grundannahme überhaupt das richtige Vorzeichen hat — spart den kompletten Sweep, wenn nicht.
3. **Zufallsdecke vor die Suche stellen, nicht danach** (Lehre 116): `E[max Sharpe | Null]` bei der geplanten Suchbreite vorher ausrechnen. Liegt der beste Fund am Ende darunter, war die Suche zu Ende, nicht der Suchraum zu klein.

> [!tip] Neue Prozess-Erkenntnis (30.07., aus dem Scalp-Lauf #050)
> Der **Exit-Raum** ist unser am wenigsten ausgereizter Hebel. Dasselbe NQ-ORB-Entry mit engem 0,3R-Target statt 1R hebt die Win-Rate von 62% auf **87%** und **dekorreliert** (corr 0.08!) — es hebt die Passquote zwar nicht genug für eine Buchaufnahme, zeigt aber: eine gezielte **Exit-Optimierung gegen das Eval-Objektiv** (niedrige Pfad-Varianz statt max. expR) ist ein unerforschtes Feld. Kandidat für einen eigenen Block.
