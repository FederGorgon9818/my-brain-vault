---
tags:
  - ressource/propfirm
  - trading/eval
erstellt: 2026-08-04
---
# 🏦 MFFU 50k: Pläne im Vergleich (Screenshots 04.08.2026)

⬅️ [[Live-Setup (Algo auf Prop)]] · [[Eval-Passing]]

## Alle 4 Pläne (50k, Target immer $3K, Max DD immer $2K!)

| Regel | ⚡ Rapid | 💼 Pro | 🧱 Builder | 🎛️ Flex |
|---|---|---|---|---|
| **Preis (mit Code)** | **$78.50** (300K) | $113.50 (300K) | $76.50 (BUILDER) | $153 (kein Code) |
| **Eval: DD-Modus** | EOD-Trailing | EOD-Trailing | EOD-Trailing | EOD-Trailing |
| **Eval: Daily DD** | ❌ keiner | ❌ keiner | ⚠️ **$1.000!** | ❌ keiner |
| Eval: Max Position | 5 Kontrakte | 3 | 4 | 3 |
| Eval: Micro-Scaling | 10:1 ✓ (=50 Micros) | 10:1 ✓ | 10:1 ✓ | 10:1 ✓ |
| **Eval: Consistency** | 50% | 50% | ❌ keine | 50% + min 2 Handelstage |
| **Funded: DD-Modus** | ⚠️ **RealTime (intraday!)** | ✅ **EOD** | EOD | EOD |
| Funded: Daily DD | ❌ | ❌ | $1.000 | ❌ |
| Funded: Consistency | ❌ | ❌ | 50% | ❌ (aber Scaling-Regel ✓) |
| Payout-Takt | **1 Tag** | 14 Tage | 2 Tage | 5 Tage + min $150/Tag-Regel |
| Min. Payout | $500 | $1.000 | $500 (max $2.000) | $500 (max $2.000, 50% requestable) |
| **Profit-Split** | **90%** | 80% | 80% | 80% |
| Buffer vor Payout | $2.1K | $2.1K | $2.1K | keiner (MLL $100 locked nach 1. Payout) |
| Plattform | Tradovate ✓ | Tradovate ✓ | Tradovate ✓ | Tradovate ✓ |

## Unsere ehrlichen Passchancen (6-Bein-Buch, Target $3K / DD $2K EOD-Trailing)

| Cushion-Frac | P(pass) | ~Tage |
|--:|--:|--:|
| 0.10 | 58% | ~104 |
| **0.14** | **56%** | **~101** |
| **0.18** | **52%** | **~72** |
| 0.22 | 49% | ~53 |
| 0.26 | 47% | ~40 |

(Die $2.000 DD statt $2.500 kosten ~6-8 Punkte vs. frühere Rechnung. Realität: ~52-56% pro Versuch, über 2-3 Versuche >85% kumulativ.)

## 🆚 UPDATE: Lucid Trading 50k im Vergleich (04.08.2026)

| Regel | MFFU Rapid | **Lucid Flex** | Lucid Pro |
|---|---|---|---|
| Preis | $78.50/**Monat** (läuft weiter!) | **einmalig** (~$90-370 je Größe, exakt beim Kauf prüfen) | einmalig |
| Eval: Target / DD | $3K / $2K EOD-Trailing | **$3K / $2K EOD-Trailing (identisch)** | $3K / $2K EOD-Trailing |
| Eval: Daily Loss | ❌ | **❌ keiner** | ⚠️ $1.200 |
| Eval: Consistency | 50% | 50% | ❌ |
| Max Position | 5 Mini / 50 Micro | 4 Mini / 40 Micro | 4 Mini / 40 Micro |
| **Funded: DD-Modus** | ⚠️ **RealTime** | ✅ **EOD-Trailing** | ✅ EOD-Trailing |
| Funded: Consistency | ❌ | **❌ keine** | 40% |
| Split | 90% | 90% | 90% |
| **Algo-Policy** | semi-auto, **beaufsichtigt** | ✅ **VOLL-Automation explizit erlaubt** (Bots/Copier) | ✅ voll |
| Payout | 1 Tag | 5 separate Tage mit Min-Tagesprofit | ab 3 Handelstagen |

**→ NEUE ENTSCHEIDUNG: Lucid Flex 50k.** Gründe:
1. **Gleiche Eval-Mathematik** wie MFFU Rapid (identische Passchancen: ~52-56% / 72-101d)
2. **Einmalzahlung statt Monats-Abo:** unser Grind dauert 2,5-3,5 Monate → MFFU würde ~$160-275 kosten, Lucid einmal ~$150-190
3. **Voll-Automation offiziell erlaubt** → Max' Job-Situation (nicht am PC um 15:30) ist bei Lucid regelkonform, bei MFFU (Aufsichtspflicht) ein Graubereich
4. **Funded deutlich besser:** EOD-Trailing + KEINE Consistency (MFFU Rapid: RealTime-DD)
5. Kein Daily-Loss-Limit im Eval (Pro und MFFU Builder haben eins → Sim-Mismatch)

**Ehrliche Caveats:** Lucid ist jünger als MFFU (weniger Track-Record = Auszahlungs-Vertrauensrisiko; Reviews zeigen aber laufende Payouts). Vor Kauf auf lucidtrading.com prüfen: exakter 50k-Preis, Aktivierungsgebühr Funded, Min-Handelstage im Eval. Microscalping-Regel (<5s-Trades >50% Profit) betrifft uns nicht (Haltezeit Minuten+).

## ~~ENTSCHEIDUNG: Rapid 50k mit Code "300K" = $78.50~~ (ersetzt durch Lucid Flex, s.o.)

**Warum Rapid:**
1. **Günstigster Preis** (gleichauf mit Builder)
2. **Eval-Regeln = exakt unser simuliertes Regime:** EOD-Trailing, KEIN Daily-DD, 5 Kontrakte (weit über unserem Cap von 14 Micros)
3. Builder ist zwar $2 billiger, hat aber **Daily DD $1.000 = zusätzliche Ruin-Barriere**, die NICHT in unserer Simulation ist → senkt real die Passchance und zwingt den Risk-Guard zu einem harten Tagesstopp. Nicht wert für $2 Ersparnis.
4. Flex: teurer + min $150/Tag-Payout-Regel + nur 3 Kontrakte → nein.
5. Pro: $35 teurer für besseres Funded (EOD statt RealTime). Fürs ERSTE Konto nicht nötig — Ziel ist jetzt Eval-Passen.

**Der Rapid-Haken (bewusst akzeptiert):** Funded = RealTime-Trailing-DD (das harte Apex-Modell). Gegenstrategie: **90% Split + 1-Tages-Payouts** = Gewinne sofort rausziehen, Risiko de-risken. Wenn wir funded sind und das Buch läuft, kaufen wir fürs zweite Konto ggf. Pro (EOD-Funded) — Entscheidung dann.

**Addons: KEINE.** (Builder-MaxLoss-Addon irrelevant, Pro's "One Day to Pass" = $4K-Target gegen Consistency-Befreiung ist ein schlechter Tausch für uns — unsere vielen kleinen Tage haben mit 50%-Consistency kein Problem.)

## ⚠️ Für den Risk-Guard zu überwachen (Eval)
1. **Consistency 50%:** kein Einzeltag > 50% des Gesamtprofits beim Pass-Antrag. Guard-Regel: wenn bester Tag > 45% vom Total → Size auf Minimum bis verdünnt.
2. **Max 5 Kontrakte / 50 Micros:** unser Cap 14 Micros → nie relevant, trotzdem hart im Guard verdrahten.
3. DD-Floor $2.000 EOD-Trailing → Cushion-Berechnung im Sizing auf 2.000 stellen (nicht 2.500!).
