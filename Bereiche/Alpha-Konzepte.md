---
tags:
  - bereich/trading
  - trading/alpha
erstellt: 2026-07-07
---
# 🧠 Alpha-Konzepte (Web-Recherche Praktiker)

⬅️ [[Alpha-Suche]]

> [!info] Zweck
> Konzepte von Quant-/Prop-Algo-Tradern (nicht Paper), destilliert auf: **welche Teile können WIR mit unseren Daten bauen** (1-Min OHLCV NQ/ES/YM/RTY, kein L2/Tick, ehrliches Backtest, Ziel = Eval passen). Bewertung: 🟢 sofort baubar · 🟡 braucht Gratis-Zusatzdaten (VIX) · 🔵 braucht mehr Daten · 🔴 braucht L2/Tick (raus).

## 1. 🟡 VIX-Regime-Filter / Regime-Switching (TOP-Kandidat)
- **Konzept:** Der VIX definiert das Regime. **Low VIX → grinden/trenden, flache Pullbacks → Mean-Reversion/Fade funktioniert.** **High VIX → Gaps, Whips, Range-Expansion → Breakout/Trend funktioniert.** Ein simpler VIX-Filter (nur handeln wenn VIX > 16) hob laut Praktiker Win-Rate 48%→55% und Return/DD +34%.
- **Nutzbare Teile:** VIX als **Regime-Gate** auf unsere bestehenden Beine legen: ORB-Breakout nur bei hohem/steigendem VIX, Fade-Beine nur bei niedrigem VIX. Das könnte die **Win-Rate real heben** → das Einzige, das die Passquoten-Decke anheben könnte.
- **Daten:** VIX täglich gratis (FRED `VIXCLS`); intraday VIX gegen Aufpreis, aber Tages-VIX als Regime reicht oft.

## 2. 🟢 Gap-Fill mit Größen-Filter (sofort baubar, stark)
- **Konzept:** Overnight-Gaps füllen sich früh und größenabhängig. **Kleine Gaps ~78% Fill, große Gaps nur ~8%.** Median NQ-Fill 18 Min, erste 30 Min = die Hälfte aller Fills. Der RTH-Open **reversed** oft den Gap (institutionelle Flows in der ersten Stunde). Nachmittags kaum noch Fills.
- **Nutzbare Teile:** Genau das, was unser schwaches Overnight-Fade falsch machte: es fadete ALLE Gaps. Richtig: **nur kleine bis mittlere Gaps faden**, Ziel = Vortages-Close (der Fill), Exit bei Fill, **nur erste 30-60 Min**, große Gaps skippen. Größen-Bucketing als Kern-Filter.
- **Daten:** haben wir alles (Gap = heutiger Open vs gestriger RTH-Close). 🟢

## 3. 🟢 Market Intraday Momentum (erste 30 Min → letzte 30 Min)
- **Konzept (Gao/Han/Zhou):** Die **erste Halbstunde** sagt die **letzte Halbstunde** voraus (gleiche Richtung). U-Shape bei Volumen/Vola, News in erster halber Stunde verdaut, MOC-Flows treiben die letzte. Zusatz-Prädiktoren (Overnight-Return) verbessern es.
- **Nutzbare Teile:** Unser `PowerHour` ist eine grobe Version. Präzise bauen: Signal = **exakt erste 30-Min-Return**, Trade nur die **letzte halbe Stunde**, optional + Overnight-Return als zweiter Prädiktor. Schärfer als jetzt.
- **Daten:** haben wir. 🟢

## 4. 🟢 RVOL-Filter (Relative Volume, richtig gemacht)
- **Konzept:** Ausbrüche/Setups nur handeln, wenn das Volumen **relativ zum typischen Volumen zur selben Tageszeit** erhöht ist (echte Beteiligung).
- **Nutzbare Teile:** Unser `vol_filter` vergleicht nur mit der Opening-Range. Besser: RVOL = kumuliertes Volumen heute vs Durchschnitt zur gleichen Uhrzeit über viele Tage. Sauberer Aktivitäts-Filter für ORB.
- **Daten:** haben wir. 🟢

## 5. 🔵 Cross-Asset / Intermarket (Bonds, Dollar, Sektoren)
- **Konzept:** Stocks-Bonds invers, Dollar/DXY, Sektor-Breadth ko-bewegen sich mit dem Index; Risk-on/Risk-off-Zustand als Kontext.
- **Ehrliche Einschränkung (aus der Recherche selbst):** Korrelationen **brechen oft zusammen**, taugen selten zur direkten Vorhersage. Bestenfalls als **Risk-on/off-Regime-Filter** (VIX + Bond-Richtung), nicht als Signal.
- **Daten:** braucht TLT/ZN/DXY. 🔵 mittel, eher Filter als Alpha.

## 6. 🔴 Order Flow / CVD / Volume Profile / Liquidity Sweeps — ✅ GETESTET, ❌ tot (15.07.2026)
- **Konzept:** Order-Flow-Imbalance, Cumulative Delta, Absorption. Angeblich die echte institutionelle Edge.
- **Getestet:** NQ Minuten-Delta/CVD 2021-2025 aus QuantPad gezogen. **Keine handelbare Info** — Predictive corr ~0, Extremwerte/Divergenz ~0. Scheinbarer ORB-Filter war reiner **Look-Ahead** (Delta = gleichzeitige Preisbewegung). Logbuch #021.
- **Verdict:** Minuten-OF ist tot. Echte OF-Edge sitzt auf Sub-Sekunden-/L2-Ebene (weder verfügbar noch bei Retail-Latenz nutzbar). 🔴 endgültig raus.

---
## 🎯 Meine Priorisierung
1. **VIX-Regime (1)** + **Gap-Fill-Größenfilter (2)** = die zwei aussichtsreichsten für ECHTE neue/bessere Edge.
2. **Intraday-Momentum präzise (3)** + **RVOL (4)** = solide Verbesserungen bestehender Beine, sofort baubar.
3. Cross-Asset (5) nur als Regime-Filter, Order-Flow (6) nur mit neuen Daten.

## Quellen
- VIX-Regime: [algotr.substack](https://algotr.substack.com/p/stop-leaving-money-on-the-table-a) · [Volatility Box](https://volatilitybox.com/research/volatility-regimes-explained/) · [NQ815](https://www.nq815.com/learn/vix-nq-correlation.html)
- Gap-Fill: [tradingstats.net Gap-Fill-Strategy](https://tradingstats.net/gap-fill-strategy/) · [When Do Gaps Fill](https://tradingstats.net/when-do-gaps-fill/)
- Intraday Momentum: [Market Intraday Momentum (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351)
- Intermarket: [QuantifiedStrategies](https://www.quantifiedstrategies.com/intermarket-strategies/)
- VWAP/Order Flow: [LuxAlgo Order-Flow VWAP](https://www.luxalgo.com/library/indicator/order-flow-vwap-deviation/) · [Bulls on Wall Street](https://www.bullsonwallstreet.com/post/what-is-the-vwap-trading-indicator-and-how-to-use-it-as-a-day-trader)
- Alpha-Konstruktion: [QuantJourney](https://quantjourney.substack.com/p/decoding-successful-alphas-the-combinatory)
