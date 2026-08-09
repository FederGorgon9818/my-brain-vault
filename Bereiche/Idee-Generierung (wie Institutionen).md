---
tags:
  - bereich/trading
  - trading/framework
erstellt: 2026-07-15
---
# 💡 Idee-Generierung — wie Institutionen es wirklich machen

⬅️ [[Alpha-Suche]] · [[Strategie-Familien]] · [[Simplex beats Komplex]]

> [!important] Kern
> Institutionen (Renaissance, Two Sigma, Citadel, WorldQuant, D.E. Shaw) suchen NICHT „irgendwas in Papers". Sie haben einen **Prozess**: **Hypothese zuerst (mit Why), dann Test.** Reines Data-Mining ohne Why scheitert live, weil es Zufalls-Artefakte findet. Ideen kommen aus einer **Landkarte von Edge-Quellen**, nicht aus dem Nichts.

## 1. Die zwei Paradigmen
- **Theorie-first:** Theorie WARUM eine Ineffizienz existiert → testen ob sie hält.
- **Daten-first:** Daten nach Mustern durchsuchen — aber nur behalten, was ein **ökonomisches Why** hat.
- **Gewinner:** Hypothese-first. Eine gute Trading-Hypothese ist **spezifisch, falsifizierbar (Ablehnungskriterium VOR dem Test), und ökonomisch motiviert.**

## 2. Die 4 Edge-Quellen (die Ideen-Landkarte) ⭐
Jede echte Edge kommt aus einer dieser vier. Das ist der Fragen-Katalog, mit dem man Ideen ABLEITET:

| Quelle | Frage | Beispiele (Intraday Index) |
|---|---|---|
| **Behavioral** | Wo sind Menschen vorhersagbar irrational? | Überreaktion auf News/Gaps, Herding, Angst/Gier, Anchoring an Vortages-Levels |
| **Structural** ⭐ | **Wer MUSS handeln, egal zum welchem Preis?** | Index-Rebalancing (Month/Quarter-End), MOC-Imbalance, OpEx/Gamma, ETF-Creation, Roll-Tage, FOMC/CPI-Positionierung, Margin-Zwänge |
| **Risk-Premium** | Wofür wird man fürs Risiko-Tragen bezahlt? | Volatilitäts-Risikoprämie (Overnight-Gap-Prämie), Carry |
| **Informational** | Was weiß ich, bevor es eingepreist ist? | Cross-Asset Lead-Lag (VIX/Bonds/DXY → Index), langsame Info-Diffusion, Alt-Data |

## 3. Der Ideen-Funnel (López de Prado „Meta-Strategy")
Industrielle Pipeline statt Einzelkämpfer:
**Daten → Hypothese → Feature-Engineering → Labeling → Modell → Backtest → Feature-Importance (WHY) → Deploy.**
- **Kern-Regel:** **Feature-Importance ÜBER Backtesting.** Nicht „es hat gut gebacktestet", sondern „WELCHES Feature treibt es und WARUM". Ohne Why = Overfitting.
- Viele Ideen rein, wenige überleben. Es ist ein **Trichter**, kein Geistesblitz.

## 4. Signal-Decay = warum es eine Pipeline ist
Alphas verfallen (neues Alt-Data-Signal hält 12-24 Monate, bis der Vendor es an genug Fonds verkauft hat → commoditized). Two Sigma/Citadel/WorldQuant beschäftigen **hunderte** Researcher, nur um schneller neue Signale zu bauen als alte verfallen. → **Ideen-Generierung ist ein Dauer-Prozess, kein einmaliges Finden.**

## 5. Woher das Rohmaterial kommt (Sources)
- **Alternative Data** (Satellit, Kreditkarten, Geolocation, Sentiment) — für uns meist zu teuer.
- **Expert Networks** (Insider fragen) — nicht für Intraday-Index.
- **Struktur-/Regulatorik-Wissen** → die „Plumbing" verstehen → erzwungene Flows finden. ⭐ FÜR UNS am besten.
- **Reverse-Engineering von Flows:** „Wer ist gezwungen zu handeln, wann, warum?"
- **Kombinatorische Generierung (WorldQuant):** simple Operatoren auf Preis/Volumen kombinieren → Millionen Kandidaten-Alphas, dann filtern. (Unser `refine.py`-Explorer ist genau das im Kleinen.)
- **Academic/Broker-Research** nur als **Saat**, nie als fertiges Rezept.

## 6. 🔧 Der Idee-Engine-Prozess für UNS (wiederholbar)
1. **Edge-Quelle wählen** (rotiere durch die 4 aus Abschnitt 2). Leitfrage v.a.: *„Wer MUSS hier handeln, egal zu welchem Preis?"*
2. **Hypothese mit Why schreiben, VOR dem Test.** Vorlage: *„Weil [ökonomischer Grund], neigt [Instrument] dazu, unter [Bedingung] zu [Verhalten]. Prüfbar: [Vorhersage]. Verwerfen wenn: [Kriterium]."*
3. **In eine der 5 [[Strategie-Familien]] + Anatomie einordnen** (Entry/Stop/Ziel/Notausgang/Sizing/Why).
4. **Ehrlich testen** (OOS, Kosten). Behalten nur wenn Why hält UND OOS überlebt.
5. **Kombinatorisch erweitern** (bestehende robuste „Atome" × Regime × Uhrzeit × Instrument) via Explorer.

## 7. 🎯 Unsere untapped Adern (priorisiert, für Intraday-Index + Prop)
Wir waren fast nur im **Informational/Technical**-Raum (OHLCV-Muster). Der reichste ungenutzte Bereich für uns ist **Structural/Calendar** — erzwungene Flows, nur mit Kalender + Preis baubar:
1. **Kalender-/Event-Struktur:** FOMC/CPI-Tage (Drift & Vol), **Month-/Quarter-End** (Rebalancing-Flows), **OpEx/Gamma** (Verfallstage), **MOC-Imbalance** (letzte 30 Min), Wochentag, Session-Opens (Asia/EU/US), Roll-Tage, Half-Days.
2. **Cross-Asset / Relative Value:** VIX (lief schon, +16 Pkt), dazu Bonds (ZN), Dollar (DXY), Sektor-Breadth als Lead-Lag/Filter.
3. **Behavioral Overreaction:** Reaktion auf Overnight-News/Gaps (teils getestet).

**Warum Structural zuerst:** klares Why (jemand MUSS handeln), mit vorhandenen Daten baubar, und auf Retail-Ebene weniger wegarbitragiert als reine Technicals.

## Quellen
[How quant funds build signals](https://youngandcalculated.substack.com/p/how-quant-hedge-funds-actually-build) · [López de Prado – 10 Reasons ML Funds Fail](https://www.smallake.kr/wp-content/uploads/2018/07/SSRN-id3104816.pdf) · [Quantitative Meta-Strategies (SSRN)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2547325) · [Alt-Data for Hedge Funds](https://vertdata.com/blog/alternative-data-hedge-funds-guide)
