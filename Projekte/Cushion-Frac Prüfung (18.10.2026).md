---
tags: [trading, prop, eval, funded, sizing, cushion, portfolio-tab, tempo_plan]
datum: 2026-10-18
status: fertig (nichts ändern, k1 bleibt)
---

# Cushion-Frac Prüfung (18.10.2026)

⬅️ [[Eval vs. Funded Neubewertung (18.10.2026)]] · [[Eval-Passing]] · [[Funded-Phase]] · [[Hochstuf-Regel je Konto (Entwurf)]] · [[Strategie-Logbuch]] (#106, #175)

**Frage Max:** In der Speed/Pass-Frontier im Portfolio-Tab stehen Cushion-Fracs 0,10 bis 0,30. Das alte Ziel war 70 % Passchance in 30 Tagen. Kommen wir mit frac 0,14 schneller ans Ziel als heute mit k1 (1 Micro je Bein)? Gerechnet auf Wunsch von Max: Eval-Sicht **und** Zeit bis 50.000 $, echte Flotte (alle 5 Konten), echtes Buch **und** Next-Buch, alle Phasen-Varianten.

> [!important] Kurzantwort
> 1. **Nein.** Frac 0,14 auf allen Konten bringt uns nicht schneller ans Ziel. Cushion nur in der Eval ist im Normalfall knapp 3 Monate schneller, in den letzten 3 Jahren 2 Monate langsamer. Das trägt nicht. Cushion im Funded kostet Jahre.
> 2. **70 % in 30 Tagen schafft keine Frac.** E8 50k kommt mit Tagesstopp höchstens auf rund 23 % Pass in 30 Tagen, E8 150k auf rund 20 %. Die Tab-Zahl „56 % / 31 Tage“ heißt: 56 % bestehen irgendwann, und wer besteht, braucht im Median 31 Tage.
> 3. **Einziger echter Hebel: mehr Größe nur in neu gekauften E8-150k-Evals.** Das ist aber kein Cushion-Effekt, ein fester k3 ist mindestens genauso schnell. Genau diesen Hebel hat [[Eval vs. Funded Neubewertung (18.10.2026)]] am selben Tag schon geprüft: bei heutiger Vola 23 bis 50 Monate langsamer, deshalb **Eval bleibt k1**. Diese Rechnung bestätigt die anderen drei Spalten dort und ändert das Urteil nicht.

---

## 1. Was frac 0,14 im Tab wirklich heißt

- Größe je Tag wie im RiskGuard: k = Cushion × frac ÷ Risiko, abgeschnitten, mindestens 1.
- Der Tab rechnet mit Risiko = Median des Tagestiefs bei k1. Das sind **58,0 $** (echtes Buch) bzw. **66,0 $** (Next). Live im RiskGuard steht `RiskPerMicro` 104.
- Damit heißt Tab-0,14 am Start rund **4 Micros je Bein auf E8 50k** und **9 bis 11 auf den 150k-Konten** (Mathematiker). Live-0,14 mit 104 $ entspricht Tab-0,0764.
- Der Tab misst „Pass innerhalb 1 Jahr“ und hat keine k1-Zeile. Im selben Maß kommt k1 auf 85,5 % (Mathematiker, Nachbau des Tabs). Deshalb sieht „größer = schneller“ dort gratis aus.

## 2. Eval-Sicht je Konto (echtes Buch, mit RiskGuard-Tagesstopp, 4.000 Pfade)

| Konto | k1 Pass | k1 Pass in 30 T | 0,14 Pass | 0,14 Pass in 30 T |
|---|---|---|---|---|
| E8 50k (Bestand) | 87,1 % | 1,4 % | 60,4 % | 19,1 % |
| FN1 (Bestand) | 85,6 % | 6,1 % | 54,9 % | 11,1 % |
| FFN1 (Bestand) | 99,6 % | 0,0 % | 49,8 % | 8,1 % |
| E8 150k neu | 98,7 % | 0,0 % | 51,0 % | 12,2 % |

- E8 150k neu mit k1: Median **572 Kalendertage** bis zum Pass (bei den Bestandenen). Das ist der Grund, warum Größe in dieser einen Eval überhaupt etwas bringt.
- **Lotterie-Anteil:** 32 bis 43 % vom Gewinn bei „Pass in 30 Tagen“ entsteht auch bei Edge null (Statistiker). Die 30-Tage-Kennzahl ist zu einem Drittel Streuung.
- **Funded mit 0,14 ist klar schlechter** (Netto-Mittel je funded Konto / Ruin):

| Konto funded | k1 | 0,14 |
|---|---|---|
| E8 50k | 6.516 $ / 16,0 % | 1.114 $ / 80,4 % |
| FN 50k | 2.036 $ / 39,9 % | 1.379 $ / 74,6 % |
| FFN 150k | 7.460 $ / 0,8 % | 4.549 $ / 68,3 % |
| E8 150k | 8.530 $ / 1,4 % | 3.451 $ / 68,8 % |

Grund: Payout-Höhe und Payout-Zahl sind in Dollar gedeckelt. Größe kauft im Funded nur Ruin.

## 3. Zeit bis 50.000 $ (Kalender-Modus, gepaart gegen k1 überall)

Hauptmaß: mittlere Zeit bis 50k, gekappt bei 120 Monaten (Vorgabe Statistiker, weil der Median bei unter 50 % Erreichung kippt). Werte = Unterschied in Monaten zu k1, negativ = schneller. Spalten: alle Jahre / letzte 3 J / Drift ×0,58.

| Variante | echtes Buch | Next-Buch |
|---|---|---|
| Cushion 0,14 in allen Evals, funded k1 | −2,8 ±0,9 / **+2,1 ±1,1** / −1,1 ±0,9 | −5,0 ±0,7 / −0,9 ±0,8 / −0,9 ±0,9 |
| Cushion 0,14 nur funded | +35,9 / +60,9 / +5,9 | +37,5 / +52,7 / +11,1 |
| Cushion 0,14 überall | +23,8 / +50,7 / +5,9 | +21,9 / +42,6 / +10,0 |
| Cushion 0,0764 nur in **neuen E8-150k-Evals** (Bestand und Funded k1) | −15,6 / −9,6 / −7,5 | −13,5 / −7,9 / −8,4 |
| fester k3 nur in neuen E8-150k-Evals (Statistiker) | −17,0 / −10,1 / −10,3 | −14,7 / −8,3 / −12,2 |

- Basis k1 überall, echtes Buch: 96,3 % erreichen 50k in 10 Jahren, Median 74,2 Monate.
- **Cushion in allen Evals fällt durch** (Regel vorab vom Statistiker festgelegt: schneller in allen drei Spalten um mindestens 2 SE). Grund: Cushion bustet die Bestandskonten. Eval-Busts je Welt 11,2 statt 0,6.
- **Nur neue 150k-Evals:** besteht die Regel deutlich, kein Lotterie-Effekt (bei Edge null kostet die Größe rund 1.000 $ nach 36 Monaten). Aber:
  - Mit Drift ×0,58 bleibt in den ersten 5 Jahren nur **−0,5 ±0,14 Monate** übrig, der Gewinn liegt fast ganz in Jahr 5 bis 10.
  - Eval-Busts je Welt 2,7 statt 0,6 (Drift ×0,58: 9,5 statt 2,1). Auslage p90 **2.331 $ statt 1.332 $**, also fast am Deckel von 2.500 $. Das geht direkt an die BOS-Reserve.
  - Ein fester k3 ist gleich schnell oder schneller. Cushion bremst im Drawdown die Erholung mehr, als es an Busts spart.
  - **Nicht gerechnet:** die Spalte „Vola heute“. Dort ist laut [[Eval vs. Funded Neubewertung (18.10.2026)]] k2 in der 150k-Eval 23 bis 50 Monate **langsamer**.

### Verlauf als Bild (Netto-Kasse der Flotte je Monat, Normalfall)

Auf Wunsch von Max (18.10. abends): k1 gegen alle Fracs 0,10 bis 0,30 in 0,02er-Schritten, 0,14 hervorgehoben, einmal nur Eval und einmal überall. Linien = Median je Monat über 600 Welten, Band = mittlere Hälfte der Welten. Die Rechnung endet beim Ziel 50.000 $. Gleicher Seed wie oben, die Zahlen decken sich (0,14 überall wieder 38,7 % Erreichung). Achtung: nur der Normalfall. In der Gegenprobe ist 0,14 nur Eval mit den letzten 3 Jahren langsamer als k1, das steht im Bild in der zweiten Zeile.

![[Cushion-Verlauf nur Eval (18.10.2026).png]]

![[Cushion-Verlauf überall (18.10.2026).png]]

- **Nur Eval:** Die Cushion-Linien liegen nach 1 Jahr unter k1 (mehr Eval-Käufe), holen danach auf. Am Ende liegen alle nah beieinander. 0,10 ist im Normalfall am schnellsten (Median 64,6 statt 74,2 Monate), das ist aber nur dieser eine Fall und wurde nicht gegengeprüft.
- **Überall:** k1 läuft allen davon. Schon 0,14 erreicht 50k nur noch in 38,7 % der Welten, ab 0,18 bleibt die Kasse im Median beim Deckel von rund −2.331 $ hängen (alles gebustet, kein Kauf mehr erlaubt).
- Code: `_scratch_cushion_1018/verlauf.py` (Rechnung, Monatsmarken), `plot_verlauf.py` (SVG, PNG per Edge headless, Farben nach dataviz-Skill geprüft).

## 4. Was daraus folgt

- **Nichts ändern.** k1 bleibt in Eval und Funded. Live-RiskGuard bleibt bei `cushionfrac` 0,02 (praktisch immer k1).
- **Tab:** Die Speed/Pass-Frontier verleitet zu „größer = schneller“. Sie zeigt weder k1 noch „Pass in 30 Tagen“. Das deckt sich mit Punkt 1 der [[Eval vs. Funded Neubewertung (18.10.2026)]] (Kosten-Kennzahl im Tab gehört raus, oben die Zeit bis 50k).
- **Wiedervorlage „Größe in der 150k-Eval“:** nur über die Vola, wie in der Neubewertung festgehalten. Fällt die Tagesschwankung deutlich, die feste Größe (nicht Cushion) mit Vola-heute-Spalte und Tagesstopp für k3 (2.500 oder 1.800 $) neu rechnen.
- **Nebenbefund Mathematiker:** im Funded zahlen die Kernel sofort aus, sobald es erlaubt ist (E8 150k 1. Payout im Mittel 696 $ statt Cap 3.000). „Erst ab Cap auszahlen“ steht schon als offener Punkt in der Neubewertung (FFN nur volle Caps, hängt an der FFN-Regel nach dem 5. Payout).

## 5. Stempel

- Zellen gebaut mit Engine `ae2c4063` (eine andere Session hat um 19:46 bis 19:58 qbt.py, sigcore.py und vwap_pullback.py geändert, AP426, neuer Standard unverändert. Der Statistiker hat auf `74ffd28` nachgerechnet, die k1-Basis ist bit-gleich).
- Daten bis 16.10.2026, 1.702 Tage, 157,9 Handelstage je Jahr.
- **Nach der Rechnung umgesetzt:** AP426 Option A (Zwangs-Flat füllt zum Close statt zum Open, `eod_flat_px close`, Commit 36bb59a am Abend des 18.10.). Alle Zahlen hier stammen noch vom alten Fill (open) und wurden **nicht nachgerechnet**. Weil k1 und Cushion dieselben Tageszellen nutzen, ändert das am Vergleich vermutlich wenig. Die absoluten Monate können sich aber verschieben.
- Setup wie `weekend_check`: Ziel 50.000 $, Budget 600 $ je Monat, Deckel 2.500 $, Master-Seed 101, Nachkauf-Lane E8 150k k1, RiskGuard-Tagesstopp fest. Sims: 600 / 300 (Nulldrift) / 300 / 300.
- Bestand aus `konten/accounts.json` (Stand 16.10.): E8 50k, FN1, FN2, FFN1, FFN2 mit aktuellem Kontostand. Vereinfachung: alle Konten handeln dasselbe Buch, FFN ohne RTY-Gap.
- Echtes Buch 4 Beine, Next-Buch 6 Beine (ohne RTY-Gap).
- Gegengelesen: `quant-mathematician` (Modell, Theorie, keine Fehler) und `quant-statistician` (Sim-Zahlen vorab, Mehrfachvergleich, Block-Gegenprobe, Lotterie-Check, fester k).
- Code und Ergebnisse: `trading-data/engine/_scratch_cushion_1018/` (`cushion_lib.py` Kernel mit k je Tag, bit-gleich bei k1 per `test_gleich.py`; `run_cushion.py`; `combine.py`; `result_eval.json`, `result_fleet.json`, `result_fleet_lane.json`, `combined.json`).
