---
tags:
  - projekt/trading
  - trading/alpha
  - trading/friedhof
erstellt: 2026-09-17
status: aktiv (Entscheidungen bei Max, siehe Abschnitt 6)
---
# 🪦 Friedhof-Analyse (17.09.2026)

⬅️ [[Alpha-Suche]] · [[Strategie-Logbuch]] · [[Discovery-Runner v2]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Entscheidungen nach dem Urlaub]] · Rohmaterial: `Ressourcen/Friedhof-Analyse 2026-09-17/`

> [!important] Auftrag Max (17.09.2026)
> „Analyse über unsere Friedhöfe: gibt es dort nicht doch noch brauchbare Edge (mit Erweiterungen), und wo haben wir Fehler begangen, Dinge nicht gefunden oder getestet zu haben?" Sehr genau, mit Zeit.

**Umfang:** Logbuch #026 bis #157 (287 Grabsteine), fünf Hypothesen-Banken (914 Zeilen), ideas.json (64 Karten), Register (63.727 Trials), Queue (902 Jobs), alle 901 Ergebnisdateien (1.971 Buch-Bewertungen je Zelle), vier Wege-Karten, 12 Scout-Reports, Juli-Labs, Paper-Analysen. Sieben Extraktions-Agents, danach quant-statistician, quant-mathematician, pipeline-auditor, verdict-auditor (zwei Durchgänge). Zentrale Zahlen hat die Hauptsession selbst am Register und am Code nachgezählt. **Nichts wurde geändert:** keine Engine-Datei, kein Buch, keine Queue. Diese Notiz ist Befund plus Vorschlag.

> [!warning] Korrektur 17.09.2026, später am Tag — die „+9,6 pp"-Ersatz-Rechnung war nie gerechnet und hält nicht
> Max hat die tsmom-EMA-Leiter-Ersatz-Rechnung (Abschnitt 1 Punkt 1, Abschnitt 3, Abschnitt 4a Punkt 4) nachrechnen lassen — Quant-Team (Mathematiker + Statistiker), unabhängig voneinander, beide mit derselben Kernkorrektur: **R war mit 60 $ falsch angenommen, real ist R ≈ 30 $ (Median, MNQ-Punktwert 2 $)** — die HF-Variante hat ein kürzeres Signalfenster (5 statt 15 Min), also eine kürzere Range, also ein kleineres R. Damit fällt µ_c von den angenommenen 2.442 $/Jahr auf real **1.132 $/Jahr** (Bestandsbein NQ_Momentum: 1.026 $/Jahr) — beide meilenweit unter der eigenen Hürde des Mathematikers (1.551 $/Jahr für +3 pp).
>
> **Ersatz-MC, echt gerechnet (5 Seeds, OOS-Basis):** Mathematiker +0,1 pp (Spanne −0,03 bis +0,31, Pipeline-Gate `confirmed: FALSE`). Statistiker (θ-Surrogat + Block-Bootstrap) +1,76 bis +1,92 pp roh, aber 90 %-CI [−0,8; +5,1] pp, P(Δ ≥ 1,5 pp) = 0,605 — ein Münzwurf. Nach Selektionskorrektur (die „EMA-Leiter"-Achse ist über 3.044 Configs gemessen **wirkungslos**, n_eff der 40 „stärksten" Survivors ist 1,3–2,6, nicht 40; Empirical-Bayes-Shrinkage-Faktor τ²=0) liegt die ehrliche Schätzung bei **0 bis +1 pp**, Schwerpunkt auf reiner Varianzreduktion (weniger Handelstage, kein neues Alpha). In der jüngsten Epoche (2024-2026) ist der Vorteil +35 $/Jahr — praktisch null.
>
> Ein zweiter, wichtigerer Zweitbefund des Mathematikers: die R-Sensitivität in der ursprünglichen Rechnung hatte **das falsche Vorzeichen**. Größeres R macht den Ersatz nicht besser, sondern schlechter (gemessen bei R≈60 $: −0,3 pp full / −2,15 pp OOS; bei R≈120 $: −11,4 pp) — Ziel/Trailing-DD stehen in Dollar fest, σ² wächst quadratisch mit, µ nur linear. Das Buch ist beim heutigen R schon leicht jenseits des θ-Optimums.
>
> **Was bestätigt/liefert wurde:** `theta_gate()` ist gegen 22 echte MC-Läufe kalibriert (Vorzeichen immer richtig, Fehler stets konservativ, ≤3,3 pp) — `logbook-distiller` stellte fest, dass die Formel zunächst nur in dieser Notiz stand, nicht im Code (dieselbe Lücke wie schon bei `ap69_theta_scan.py`, seit August unbenutzt im Repo). Inzwischen nachgeholt: `scale_leg()`/`theta_of()`/`theta_gate()` liegen jetzt in `eval_plan.py`, Vorzeichen-Test `test_theta_gate.py` grün, `engine-regression-tester` ohne Beanstandung. Kalibrierungskonstante bisher nur für 50k-Tier gemessen. Der #153-Sharpe-Bug ist für diese Job-Familie mit Faktor 2,19 bestätigt (weiterhin ungefixt, macht jedes `above_ceiling`-Urteil unzuverlässig, bis er gefixt ist). Long/Short der Kandidaten symmetrisch (kein Bias-Artefakt) — sauberster Teil des Funds.
>
> **Konsequenz:** „der einzige Pfad, der rechnerisch trägt, ist Ersatz" (unten, Punkt 1) gilt **nicht mehr** für diese Survivor-Menge. Die Slot-Tabelle #146 wurde zwischenzeitlich unabhängig freigegeben (AP183-Entscheidung 2, „neuer Fund darf Bein derselben Familie ersetzen, wenn es das Buch verbessert") — dieser Fund verbessert es nicht, verbraucht also keine Slot-Freigabe. Rohdaten, Skripte und die zwei vollen Subagent-Berichte liegen im Session-Transkript vom 17.09., nicht als Datei im Rohmaterial-Ordner. Volltext-Befunde und Empfehlungen: [[Strategie-Logbuch]] #158-Nachtrag.

---

## 1. Kurzfassung

### Zur ersten Frage: brauchbare Edge im Friedhof?

**Fürs Prop-Buch: nein, und zwar messbar.** Von 1.971 je gerechneten Buch-Bewertungen ist keine einzige von Null unterscheidbar. Das beste Delta aller Zeiten (+5,2 pp) liegt innerhalb dessen, was reine Selektion über 1.971 Zellen bei 3,2 pp Streuung erzeugt (E[max] ≈ 11 pp). Die 51 „besser"-Zellen sind effektiv zwei Funde: Asia-Dir-Exit (promotet 21.08.) und TE-02 (als Ersatz +0,4 pp, neutral). Das ist kein Friedhofs-Befund, sondern ein Messgeräte-Befund: Stufe 2 hatte nie die Auflösung, einen realistischen Ersatz-Effekt von 2 bis 4 pp zu sehen (Power 0,24 bei 3 pp), und die Bestandsbeine selbst würden das heutige Gate mit +1,9/+2,0 pp reißen.

**Wo Edge tatsächlich liegen kann** (Details Abschnitt 3 und 4):

1. **Am falschen Pfad gesucht.** 87 % aller Trials (tsmom/maband) liefen als „neues Bein". Der Mathematiker hat die Latte ausgerechnet: ein NQ-Intraday-Zusatzbein muss bei ρ ≈ 0,2 allein **1.811 $/Jahr je Kontrakt** verdienen, mehr als das beste Bein im Buch (LastHour, 1.504 $/Jahr). Das war ab dem 24.08. (#129) wissbar, `theta_gate()` wurde nie gebaut. ~~Der einzige Pfad, der rechnerisch trägt, ist **Ersatz**: die stärksten unbewerteten Survivors (tsmom EMA-Leiter, OOS-expR ≈ 0,74 R) ergeben als Ersatz für NQ_Momentum im MC **+9,6 pp** (R = 60 $) und selbst bei einem Viertel der Edge noch +2,6 pp. Nie gerechnet, weil die Slot-Tabelle #146 unabgenommen liegt.~~ **Nachgerechnet 17.09., siehe Korrektur-Callout oben: R war falsch angenommen (real 30 statt 60 $), echtes Ersatz-Delta 0 bis +1 pp, kein Kandidat.**
2. **Die billigste Passquote liegt im Streichen, nicht im Suchen.** LOO am heutigen Buch: ohne LastHour 87,16 %, ohne VWAP-Pullback 87,34 %, bestes Subset {Momentum, LastHour} **90,11 % (+7,3 pp)**. In-Sample über 15 Subsets, braucht nested OOS, aber es ist die größte Zahl der ganzen Analyse (deckt AP158/AP162/#139 B2 und geht darüber hinaus).
3. **Nie gemessen, nicht widerlegt:** Volumen-&-Flows-Bank (479 Hypothesen, 0 gebaut), TWAP-Bank (99/100), PCA-Bank (21/21), Pairs-Bank (71/100), neun Scout-Modul-Specs, rund 50 Nebenbefunde ohne Ort. Das ist Vorrat, kein Friedhof. Die stärkste Zeile: **Orderflow-v2-Nebenspalten** (ntrades, max_size, big_*, tvwap) liegen seit 2016 auf der Box, 0 von 63.727 Trials nutzen sie. Eine unverbrauchte Datenachse ist der einzige Weg, der die Zufallsdecke nicht schon bezahlt hat.
4. **Standalone-Edges ohne Buch-Anspruch (Live-Bank):** 15 „Validiert"-Karten, nur 3 in `LIVE_EXTRA`; 14 von 19 nie unter v2 bewertet. Noise-ORB NQ, Mom-lowVIX, Gap-Continuation, FOMC-solo, OPEXMOM ES/RTY/YM ohne dokumentierte Entscheidung. Braucht zuerst ein geschriebenes Kriterium (Live-Grade-Karte), sonst rutscht Grade C/D durch.
5. **Auf kaputten Daten beerdigt:** alle ES-/RTY-Urteile vor dem 30.08. (3.344 ES-, 1.117 RTY-Trials; RTY hatte an praktisch jedem Roll Fremdkontrakt-Sessions). RTY_Gap-fade wurde am 24.08. aus dem Buch genommen und sechs Tage später vom eigenen Datenfix als „unterschätzt" (+8 % expR) gemessen, ohne dass die Entscheidung je revidiert wurde. Die komplette ES-Alpha-Woche (25. bis 28.08.) liegt davor.
6. **Ein kleiner Sizing-Hebel ohne neues Alpha:** Beine bei dünnem Puffer abschalten (Rest-Cushion < 800 $ nur Momentum laufen lassen) bringt im MC **+2,2 bis +3,6 pp**, live im RiskGuard trivial. Parameter gefittet, OOS-Split fehlt.

### Zur zweiten Frage: wo haben wir Fehler gemacht?

Dreizehn Prozessfehler (Abschnitt 5). Die fünf tragenden:

- **Kein Trial trägt einen Engine-/Daten-Stempel.** Nach neun Fixes zwischen 09.08. und 16.09. steht nur bei 11 von 902 Jobs fest, dass sie auf heutigem Stand sind. Ein Todesurteil ohne Stempel wird nach dem nächsten Fix nicht überprüfbar, sondern zur Sperre (alpha-scout liest „Getötet" als Ausschluss).
- **Die Kontroll-Batterie sitzt hinter dem engsten Gate.** Look-ahead-Delay, Nulldrift, Spiegel-Seite, Multi-Markt sind codiert, liefen aber in 901 Ergebnisdateien auf genau **10 Zellen** (TE-02/04/15, 23./24.08.). Schritt 3 des EINEN Wegs war praktisch nie aktiv.
- **Schwellen ohne Power-Rechnung.** 1,5 pp gegen ein 0,24-pp-Seed-Rauschmaß (echte Streuung 2,6 bis 4,2 pp), dann Šidák 4,9 bis 7,1 pp. Es gab nie ein Fenster, in dem ein echter 3-pp-Effekt als Kandidat gezählt hätte.
- **Pfad-Blindheit.** `book_leg_for()` matcht nur (mode, symbol) exakt, kein tsmom/maband-Job bekommt je ein `replaces_leg`. #139 B3 hat das am 01.09. benannt; 16 Tage später liefen dort weiter 87 % der Rechenzeit.
- **Vorräte ohne Fördermechanik.** Die Bänke sind Markdown ohne Status-Feld, der Generator klont Varianten statt die nächste ungebaute Zeile zu ziehen. Ergebnis: Queue viermal leer (30.08., 03.09., 12.09., 17.09.) bei 670 ungebauten Hypothesen.

**Was NICHT der Fehler war:** die Prämissen-Stufe. 427 Jobs starben dort, aber über 474 Grid-Jobs gemessen gilt: Basis-Edge ≤ 0 pp ergab 0 von 34 Jobs mit Survivor, bis +1 pp 0 von 67 Jobs mit Kandidat, alle 14 Jobs mit je einem Kandidaten hatten Prämissen-Edge ≥ 1,7 pp (AUC 0,83). Erwarteter Kandidaten-Verlust der 369 Prämissen-Tode ≈ 0. Die Extraktion Teil 3 hatte „premise_failed ist ein Bug, kein Ergebnis" behauptet; die Zahlen widerlegen das.

---

## 2. Harte Zahlen (von der Hauptsession selbst am Register/Code verifiziert)

| Was | Zahl |
|---|---|
| Register | 63.727 Trials: tsmom 38.998 + maband 16.406 (87 %), NQ 56 %; Survivors 4.098 bis 4.605 je nach Zählung |
| Buch-Bewertungen je Zelle | 1.971: 51 besser, 25 grenzwertig, 260 neutral, 1.635 schlechter; 55 je über 1,5 pp, im September 8 |
| Queue | 902 Jobs: 474 done, 427 premise_failed; 11 auf heutigem Pipeline-Stand; 485 vor Roll-Garbage-Fix, 305 vor corr_book-Fix, 253 in Modi ohne Null-Schalter |
| Duplikat-Läufe | 39 Ersatz-Jobs / 212 Bewertungen (18. bis 24.08.) mit dem zu ersetzenden Bein noch in `book_legs_in_base` (TV-02 OOS-expR 0,75, TE-06 0,68, TV-13 PBO 0,0001, AR-02 54/54 Survivors, TN-04). Nur TE-02/04/15 als v2 neu gerechnet |
| Kontroll-Batterie | `controls`-Feld in 10 Zellen aus 3 Jobs (23./24.08.); orb/orb_std fehlen in `ctl_null` (Z.645), sind nie deploy_ready; ohne Null-Schalter: rv, gap, cal, i2, vix_bias, pivot, flip, continuation, orb, orb_std, firstbar_ematrail, regime_gate, event_study (6.376 Trials) |
| Unbewertete Survivors | 2.634 von 4.605 (57 %) nie gegen das Buch gerechnet (`max_book_evals`-Deckel); die gebuchten Picks der stärksten Jobs (OOS-expR 0,74, Sharpe 2,2 bis 2,4 vor #153) als neues Bein neutral (−0,6 bis −1,4 pp) |
| Roll-Garbage | ES 16 und RTY 67 Fremdkontrakt-Sessions; Gap-Modus rechnet aus 1m-Open vs Vortages-Close, also frontal betroffen; NQ/YM 1m sauber |
| Hypothesen-Banken | `hypothesis_bank.py` 137 H()-Zeilen, alle Momentum-&-Averages (+EC/CE/CR/LD/RV/FA); Volumen-Bank 0 (Status seit 21.08. „noch nichts getestet", 192 ohne neuen Code testbar) |
| AW-14c | Anker-Placebo (entscheidet über V1-V9 der VWAP-Familie): am 16.09. 20:01 mit PermissionError beim registry.json-Rename abgestürzt, nie gerechnet, unbemerkt |
| AW-15b | 29/144 Survivors nach atr_bar-Fix, aber PBO kaputt, Sharpe 0,76 vs Hürde 0,71, als Ersatz für VWAP-PB −8 bis −24 pp: bleibt tot |
| tm_delta_src | nur 292 tsmom-Trials je „real", 50 davon mit Delta-Gate vor dem Fix; 23.273 Trials mit Delta-Gate liefen bewusst auf dem Proxy (Default), die Survivor-Rangliste ist davon nicht entwertet |
| Korrekturen an Agent-Berichten | „Slippage nach Ordertyp nie eingebaut" (Teil 1): falsch, `qbt.py:1397` Limit = 0 Ticks. „gap nur montags" (Engine-Audit): falsch, 395/397 ohne Wochentagsfilter. „TE-v2 still gelöscht" (Teil 3): falsch, liefen am 01.09. „orb hat Null-Schalter" (Hauptsession): falsch, Auditor hatte recht |

---

## 3. Struktur-Antworten des Quant-Teams

### quant-mathematician (alles am heutigen 4-Bein-Buch gerechnet, 50k-Tier, Min-Size, Intraday-Bust, 5 Seeds)

- **P(pass) hängt praktisch nur von θ = 2μ/σ² ab** (Lehoczky; hier plus Floor-Lock, deshalb MC). Basis 82,80 ± 0,48 %, μ_b 26,3 $/Tag, σ_b 217 $, θ_b 1,118e-3. θ-Kurve: **28,1 pp je 1,0 relativer θ-Änderung**, linear ±20 %.
- **„Bein dazu" ist kein Theorem, sondern eine harte Zahl:** Zusatzbein hilft ⟺ θ_c > θ_b(1 + 2ρσ_b/σ_c). Break-even in $/Jahr je Kontrakt: ρ=0: 155 / 969 / 2.482 (σ_c 40/100/160); **ρ=0,2: 492 / 1.811 / 3.828**. Für +1,5 / +3,0 / +5,4 pp netto: 812 / 1.299 / 2.078 $/Jahr. θ_c = 2e/(R·s²) ist frequenzfrei; mit der empirischen Decay e ∝ n^−0,73 folgt θ_c ∝ n^−0,73, **das ist der formale Grund für Spearman(Buch-Score, Trades/Jahr) = −0,81**, und der HF-Fokus des Generators lief exakt in die falsche Richtung (Optimum n ≈ 17 bis 40, ab n > 126 negativ).
- **Klein-N-Event-Edges:** eigenes Bein mit n=16, e=0,5 R, R=200 $ → +4,8 pp; n=7, e=0,8 R, R=300 $ → +7,0 pp. Hürde ~1.300 $/Jahr netto bei Stop nahe R* = 890/√n. Size-Overlay ohne Zusatz-Edge ist Lehre 82 (7 Event-Tage ×2 → −1,1 pp), mit Edge dieselbe $/Jahr-Hürde. **Event-Edges nur noch in $/Jahr je Kontrakt bewerten; unter 800 $/Jahr tot, egal wie hübsch der Sharpe.**
- **Ersatz statt Zusatz:** Swap gegen NQ_Momentum braucht μ_c ≥ 1,46 μ_o für +3 pp roh (1.551 statt 1.063 $/Jahr). tsmom EMA-Leiter HF (n=55 Trades/Jahr, OOS e=0,74 R): R=40 $ → +7,5 pp, R=60 $ → **+9,6 pp**, R=120 $ → +12,9; Shrinkage-Leiter bei R=60: e 0,45 → +6,1, 0,30 → +4,1, 0,20 → +2,6, 0,15 → +1,6. ~~Rechnerisch aussichtsreich mit großer Reserve.~~ Vor dem Lauf fehlt nur R_c in USD (Stop 0,3 in welcher Einheit). **Nachgerechnet 17.09.: R_c real ≈ 30 $ (nicht 60), µ_c real 1.132 $/Jahr — die R-Sensitivitäts-Leiter hatte zudem das falsche Vorzeichen, größeres R macht den Swap schlechter, nicht besser (σ² wächst quadratisch mit der Skalierung, µ nur linear). Echtes Delta 0 bis +1 pp. Details: Korrektur-Callout oben, Logbuch #158-Nachtrag.**
- **Gates auf Bestandsbeine:** θ_gate = 2μ_on/σ_on², die Kalenderzeit kürzt sich raus, verloren geht nur über die Horizont-Zensur (Malus bei q=0,85/0,70/0,55/0,40: 0 / 2,3 / 4,6 / 8,9 pp). Für +3 pp braucht ein Gate Δμ ≈ 13,5 bis 18 $/Tag. **Killer ist die Nachweisbarkeit:** SE(Δμ) ≈ 10,3 $/Tag bei 60/40-Split, ein Gate mit 15 $/Tag hat t = 1,45. **Vorab-Gate: q ≥ 0,7 und Δμ ≥ 20 $/Tag auf den Tageszellen (3 Zeilen), sonst kein Grid.** Das ist AR-17 (#139) als Zahl statt als Erfahrung.
- **Coast-to-Target:** Größe 0 ist tot (−0,8 bis −83 pp, Risikoaversion −V''/V' = θ ist konstant). **Beine abschalten bei dünnem Puffer** (nur Momentum ab Rest-Cushion < 800 $) **+3,4 pp**, unter konservativerem dw-Modell +2,2 bis +2,3 pp, reiner Overshoot-Effekt am Intraday-Barrier. Patch als Leg-Schalter (`thin_cushion_usd`, `thin_subset`) in `run_account`, nicht als Size-0 in `cage_policy_lib.py:316`. Parameter gefittet, OOS-Split fehlt.
- **Nebenbefund Modellstrafe:** `cage_policy_lib.combine()` summiert die Bein-MAEs (dw = Σ MAE), als hätten alle Beine ihr Intraday-Worst im selben Moment. Gemessen 109 $ Summe gegen 77 $ nur schlimmstes Bein. Effekt: 4-Bein-Buch 82,80 (Summe) vs 84,36 (nur schlimmstes). **Rund 0,35 pp Strafe je zusätzlichem Bein aus einer Modellannahme, nicht aus dem Markt**, ein Fünftel des Abstands zwischen 2- und 4-Bein-Buch. Zeitgewichtetes dw ist ohne neue Daten baubar (`t_in`/`t_out` liegen vor).

### quant-statistician (901 Meta-Dateien + 62.827 Result-Zeilen, selbst gerechnet)

- **Zufallsdecke:** n_eff liegt bei 250 bis 1.600 statt 63.727 (Participation Ratio je Grid Median 5,3, Paar-Korrelation innerhalb eines Grids Median 0,63). Direkt getötet: 0 Zellen (`above_ceiling` nur am Kandidaten-Schritt, ohne `replaces_leg`). Indirekt: 25 der 51 „besser"-Zellen und 978 Survivors liegen zwischen Mechanismus- und Globaldecke. Fix: `e_max_sr(max(n_eff_mech, 10)·F)` mit F ≈ 19 Familien; cal 1,00 statt 1,72.
- **Prämisse:** Spearman 0,58, AUC 0,83; Kandidaten nur ab ≥ 1,7 pp. Gate behalten, aber als CI (obere 90 %-Grenze < 0) statt Punktwert; befreit ~94 Jobs, Ertrag 0 bis 3 Kandidaten.
- **Šidák-Gate:** Schwelle 4,90 (sd 3,0) bis 7,12 pp (k_eff 8). Power bei 3 pp: 0,24 bzw. 0,10. Power 0,80 bräuchte ~70 Jahre Historie. Test gegen 0, die richtige Null ist negativ. α 0,10 je Job ist keine Pipeline-Kontrolle (47 bis 142 Falsch-Positive unter Null bei 474 Jobs). **Design nach Wirkung:** (1) gepaart gegen den Nulldrift-Zwilling (`ctl_null` existiert, SD-Reduktion eine Stunde Messung), (2) Pooling über die ≥ 10 Implementierungen VOR der Selektion (Power ≈ 0,45), (3) glattes Surrogat statt First-Passage-Indikator (der Mathematiker liefert es: θ), (4) FDR kampagnenweit, (5) zweistufig: Screening α 0,20 (2,7 pp, Power 0,54) → Next-Week-Staging als echte zweite Stufe.
- **Rückwirkend:** Mittel −8,06 pp, sd 7,74, Maximum +5,20. Neutral-Zellen: Maximum 1,6 pp, z ≤ 0,5. Besser-Zellen: 14 mit p < 0,10 einzeln, 0 mit z ≥ 1,645; EB-geschrumpft bester Rohwert 2,9 pp. Wer Rohwerte liest, liest ~2,3 pp zu viel.

---

## 4. Kandidaten mit Stempel (verdict-auditor, zwei Durchgänge)

Stempel: **WIEDERBELEBEN** (Nachtest lohnt), **NACHRECHNEN** (Urteil auf heutigen Stand heben, kein Buch-Versprechen), **BLEIBT TOT**, **VORRAT** (nie getestet, kein Friedhof, geht durch `ein-weg`).

**Grundregel des Auditors nach dem Statistik-Befund:** „Buch-Kandidat" ist bei keiner Zeile mehr das Ziel. Jede Nachrechnung muss sich als Daten-Hygiene, als Kontrolle für einen bestehenden Fund oder als Live-Bank-Frage rechtfertigen. Und: **v2 ist strenger, nicht milder.** Was unter dem alten HF-freundlichen Zeit-Kriterium eine fallende oder gleiche Passquote zeigte (Noise-ORB 57→52, VWAP-PB 61→54, Crabel 61→60, Event-Bein 61→61, VIX-Spike 55→55, Renko-Flip), braucht keinen v2-Nachtest fürs Buch. Das räumt den halben F2-Block ohne Rechenstunde ab.

### 4a. Reihenfolge nach Erkenntnis pro Rechenstunde
1. **Referenzbuch entscheiden** (AP158 VWAP-Pullback, AP162 LastHour_v3, AP121 Momentum-BE als EIN Paket, nested OOS, plus alle 15 Subsets). Jede weitere Marginal-Zahl misst sonst gegen eine Basis, die selbst der Fehler ist.
2. **`theta_gate()` bauen** (Code des Mathematikers unten), entscheidet A1 und F3 fast ohne Box.
3. **k_eff der 2.634 unbewerteten Survivors** messen (~20 min).
4. ~~**tsmom EMA-Leiter als Ersatz für NQ_Momentum** rechnen (R_c in USD klären, θ-Gate, dann Stufe 2 auf vorhandenen Survivors), Ergebnis als „breiterer Mechanismus" führen, solange die Slot-Tabelle nicht abgenommen ist.~~ **Erledigt 17.09.: R_c=30$, θ-Gate hätte richtig abgelehnt, MC-Delta 0 bis +1 pp — kein Kandidat, erledigt.**
5. **AW-14c neu einreihen** (neue ID, Dienst-Rechte auf `results/` prüfen).
6. **RTY_Gap-fade:** Top5 und Epochen-Split auf bereinigten Daten (Minuten); erst wenn beide kippen, mehr.
7. Trigger-Zahl-Check der rv/LL-Jobs mit n=0 und der TR-Zeilen (Lehre 157).
8. Sharpe-Neurechnung post-#153 für die Top-200 unbewerteten Survivors.
9. ~~Orderflow-v2-Nebenspalten: Abdeckung je Markt/Jahr klären, dann Modul (Spec A).~~ **Erledigt 18.09.: vorregistrierter Gate-Test statt Modul, kein Effekt nachweisbar** ([[Strategie-Logbuch]] #162). Kein Kandidat, kein Ticket. Offen nur mit abgesenkter Erwartung: Asia-Dir-Integrationsbug (`asian.trades()` tmin_entry-Konvention) oder gröbere Fragestellung auf allen NQ-Bars.
10. Turn-of-Month (OOS ab 2023 +8 bis 9 pp, Wiedervorlage war versprochen).

### 4b. Die Zeilen

| # | Fund | Stempel | Auflage / nächster Schritt |
|---|---|---|---|
| A1 | 39 Duplikat-Läufe (212 Bewertungen) als Ersatz nie gemessen | NACHRECHNEN, nachrangig | erst θ-Gate analytisch über alle 39, nur was die Schwelle zu > 50 % füllt auf die Box; nach dem LOO-Entscheid |
| A2 | AW-14c abgestürzt, nie gerechnet | WIEDERBELEBEN | neue ID (Enqueue dedupt über ID, #157), vorher Schreibrechte des NSSM-Dienstes |
| A3 | 13 Modi ohne Null-Schalter (6.376 Trials), nie deploy_ready | Entscheidung, kein Test | acht Null-Schalter bauen oder Mechanismen als tsmom-Gate nachbilden (billiger, landet in einem Modus mit Kontrolle) |
| A4 | 369 Prämissen-Tode | BLEIBT TOT | Messfehler-Tode (atr-Klasse #157, LQ-01 n=50) gehören nach D2, nicht in die 369 |
| A5 | Zeilen mit `tm_delta_src="real"` vor AP151 P4 maßen den Proxy | NACHRECHNEN | Reichweite: 50 Trials, nicht die Survivor-Rangliste |
| B1 | RTY_Gap-fade 24.08. raus, 30.08. „unterschätzt" | NACHRECHNEN, anderes Ziel | +8 % expR heilt weder Top5 0,638 noch Epochen; nur diese beiden neu, `gap` hat keinen Null-Schalter |
| B2 | ES-Alpha-Woche komplett vor #135 | NACHRECHNEN CE-04, CR-02 (Signal aus Fremdkontrakt-Gaps), CR-03 (Live-Bank); EC-01..05 BLEIBT TOT mit Prüfzeile | Kostenurteil belegen: wie weit liegt die EC-Brutto-Edge unter den Kosten; 16 von ~2.650 ES-Sessions kippen nur knappe Urteile |
| B3 | Noise-ORB ES/RTY und div_fade vor 10.08. (Bars ≤ 0) | NACHRECHNEN als **Multi-Markt-Kontrolle** des NQ-Bank-Funds | nicht als Kandidatensuche etikettieren (zählt sonst doppelt gegen die Decke); orb nie deploy_ready → Bank-Frage |
| B4 | TR-01/04/06/12 (rv, vor rv.py-Fix, TR-04 −33,5 pp) | NACHRECHNEN mit Vorstufe | erst `len(trades)` und max|r| der Basis-Config |
| C1 | 12 Validiert-Karten außerhalb des Live-Buchs, 14/19 nie unter v2 | NACHRECHNEN mit Vorlage-Auflage | **Live-Grade-Karte** zuerst (Max' Abnahme): frischer Code, OOS-expR > 0 mit Block-Bootstrap P ≥ 0,90, Kosten-Stress, Epochen-Split nicht gegenläufig, ctl_delay bestanden, ctl_null oder dokumentiertes „nicht prüfbar", Decke gegen n_global ausgewiesen; die drei bestehenden LIVE_EXTRA-Beine laufen in vix_bias/cal ohne Null-Schalter |
| C2 | Klein-N-Event-Edges als Gate/Size-Overlay | neue Hypothese → `ein-weg` | $/Jahr-Hürde 800/1.300 $ gilt für beide Formen; cal ohne Null-Schalter |
| C3 | Renko-Flip NQ, 400 bis 500 Trades/Jahr | BLEIBT TOT (Buch) | v2 streicht den Zeitterm, der HF belohnte; θ ∝ n^−0,73; Live-Bank nur über C1-Vorlage |
| C4 | Overnight-RV-Filter (Sharpe +17 %, nur an 30-Tage-Frist gescheitert) | NACHRECHNEN | AR-17-Methodik plus Vorab-Gate q ≥ 0,7, Δμ ≥ 20 $/Tag; Prior: AR-15/17/18 fanden mit diesem Sample nichts Auflösbares |
| C5 | ONREV_NQ mit Vola-Konditional | NACHRECHNEN nur mit Vorabfestlegung | Konditional vorab (Größe, Schwelle, Warum), Shift-Placebo, Episoden-Jackknife; sonst BLEIBT TOT |
| D1 | AW-15b | BLEIBT TOT, robust | tot sogar gegen ein Referenzbein, das selbst −4,7 pp trägt |
| D2 | AW-09b/AW-11b/AW-02/LD-02/EC-03 auf `atr` (Tages-ATR20) | Betriebs-Auflage | Dauer-Lint `len(trades)` der Basis-Config bei jedem Enqueue, neue IDs |
| D3 | GEX als Vola-/Stop-Weiten-Gate; Filter an top5/freq-Gates gestorben | neue Hypothese → `ein-weg` | gepaart messen; Zeitstempel der GEX-Größe gegen Entry prüfen; maband band/channel/vwap können `ctl_null` fälschlich bestehen (Richtungs-Placebo statt Zufallslevel) |
| D4 | VWAP-Pullback Multi-Symbol-Kill auf v4 und kontaminierten Daten | NACHRECHNEN als Multi-Markt-Kontrolle, erst nach AP158 | v8-Spezifikation, ATR-Stops |
| E1-E7 | Messfunde ohne Weiterverfolgung: pts_per_kdelta als Continuation-Filter (#107), Absorptions-Inverse (#100), Erstkerzen-Richtung als Momentum-Bestätigung (#147), AR-19 Korrelationsregime (#141), LastHour Unter-MA-Überschuss (#136), Spiegel-Trick bei ES-VWAP-Reversion / ES-YM-Breakout-Fade / IB-Fade / First-Bar-Fade ES-YM-RTY / OR_DELTA SHORT, NOISE_ORB halbe Varianz + FA-01-Pullback-Entry auf ORB | WIEDERBELEBEN mit Beweiszeile je Fund | „0 neue Register-Trials" gilt nur bitidentisch; jede Bedingung ist ein Trial; registerfrei ≠ deckenfrei; der Ersatz-Pfad prüft `above_ceiling` gar nicht (`discovery_runner.py:575`); immer neue Job-ID; Gates zusätzlich Vorab-Gate Δμ ≥ 20 $/Tag |
| F1 | Volumen-Bank 479/0, TWAP 99/100, PCA 21/21, Pairs 71/100 | VORRAT | vor jeder Planung gegenzählen, wie viele Zeilen in einem Modus MIT Null-Schalter landen; zuerst die Block-Kontrollen VV-60, SZ-09/25/60, MS-59, GM-37, PR-04, ST-01 |
| F2 | Scout-Specs nie gebaut: Orderflow-v2-Gate, DIX-01, macro_gate, volshock, `tm_stop_mode="leg"`, Coast-Leg-Schalter | Orderflow-v2-Gate **getestet 18.09., kein Effekt** ([[Strategie-Logbuch]] #162); DIX-01/macro_gate/volshock/Coast-Leg weiter VORRAT | Orderflow-v2 erledigt (kein Kandidat); übrige Specs nach `ein-weg` |
| F3 | 2.634 Survivors ohne Buch-Bewertung | teilerledigt 17.09. (EMA-Leiter-Teilmenge, 721 Survivors): **BLEIBT TOT**, kein Ersatz-Kandidat | Rest (2.634 − 721) weiter offen; k_eff-Methodik jetzt am EMA-Leiter-Fall kalibriert (n_eff 1,3-2,6 statt 40), Sharpe-Inflationsfaktor hier 2,19 gemessen |
| F4 | 379 ungelesene Inbox-Einträge | Betriebsschuld, 0 Rechenzeit | einmal durchstempeln, `--seen-all`, vor allen B/C-Läufen |
| G1 | Bestandsbeine (AP158/AP162/AP121) | Position 1 | LOO war In-Sample, nested OOS ist Rechenzeit; ein Paket, nicht drei Tickets |

---

## 5. Die Prozessfehler (pipeline-auditor, Rang nach Wirkung)

| # | Fehler | Umfang | Status | Dauerhafter Fix |
|---|---|---|---|---|
| P1 | Pfad-Blindheit (`book_leg_for()` nur exakt (mode, symbol); kein tsmom/maband-Job mit `replaces_leg`) | 55.404 Trials; seit 25.08. 289 Buch-Evals, 0 besser | offen; Slot-Tabelle #146 seit 09.09. unabgenommen | Slot-Tabelle in `job_generator.py:493`; Assert in `mk_job()`: kein Job ohne `replaces_leg` oder `neues_bein_begruendung` |
| P2 | Kein Stempel je Trial (`registry_entry()` ohne Engine-/Daten-/Gate-Fingerprint) | 63.727 Trials; 11 von 902 Jobs auf heutigem Stand | offen | `engine_fp`, `data_fp`, `gates_fp`, `criterion`; `rerun_needed.py`; `--rerun` mit neuer ID statt stillem Skip (`hypothesis_bank.enqueue`) |
| P3 | Kontroll-Batterie hinter dem engsten Gate | 10 Zellen in 901 Dateien | offen | `ctl_sides` + `ctl_symbols` als Stufe 1,5 auf die Top-k Survivors, Registerfeld, kein Gate |
| P4 | Schwelle ohne Power-Rechnung | 1.971 Bewertungen, 0 von 600 Dateien über 5,4 pp | offen | Power-Zeile in `book_marginal_confirm()`; reicht die Auflösung nicht, steigt das Mess-Budget (θ-Surrogat, Pooling, gepaarter Zwilling), nicht die Latte |
| P5 | Auswahl vor der Prüfung (Survivors nach OOS-Sharpe sortiert, nur k gebucht) | 2.634 unbewertet | offen, durch 8→3 verschärft | Sortierschlüssel v2-nah ($/Jahr × Dekorrelation), Diversitäts-Pick |
| P6 | Vorräte ohne Fördermechanik | 670 ungebaute Zeilen, 9 Specs, `queue_empty` 42× | offen | `hypotheses.json` mit Status als Quelle 5 des Generators vor dem Varianten-Klon |
| P7 | Ergebnisse kommen nie in einem Urteil an | 388 ungelesene Einträge | offen | Wochen-Aggregat, Pflichtfeld „Stufe, an der es hing" |
| P8 | Referenzbuch nie mit Kandidaten-Härte gemessen | AP158/AP162/AP121; LL04 +0,8 vs +2,7 pp je Basis | offen | Monatslauf in `funded_finalize.py`: LOO + GATES_HARD je Bestandsbein, Ticket automatisch |
| P9 | „Getötet" als Dauersperre ohne Verfallsmechanismus | 14/19 Karten nie unter v2; 6 Doku-Widersprüche | offen | `judged_engine_fp`/`judged_date`/`criterion` in ideas.json und Karten-Frontmatter, `stale_verdicts.py` |
| P10 | Nebenbefunde haben keinen Ort | ~50 Fälle | offen | `findings.json` + Frage in `after_change.py` |
| P11 | Prämisse aus 1-3 Basis-Configs | 427 Jobs, Verlust ≈ 0 | teilgefixt | CI-Gate; Prämisse über ≥ 2 Grid-Achsen |
| P12 | Rerun nach Fix wird still verschluckt (ID-Dedupe) | ≥ 7 Bank-Jobs, strukturell alle 891 | offen | `--rerun`, `superseded_by` |
| P13 | Audit-Behauptungen ohne Ausführungsbeleg (diese Analyse: 4 Fehlaussagen, alle nachgezählt) | 4 von ~40 Kernaussagen | Prozesslücke | Register-Aussagen nur mit Abdeckungszähler; Code-Verhalten per Mini-Probe, nie per grep allein |

**Wer hätte es fangen sollen:** #139 B2/B3 wurden am 01.09. sauber benannt und blieben Text ohne Code-Folge. `pipeline-auditor` prüft Stale-State nur vorwärts (Box-Sync, push-next), nie rückwirkend gegen das Register. `logbook-distiller` prüft „ist die Lehre ein Gate", nicht „ist der Messfund ein offener Posten". `alpha-scout` liest „Getötet" als Sperre, weil ihm der Verfallsmechanismus fehlt. `quant-statistician` lieferte die Šidák-Korrektur, war aber nicht beauftragt zu prüfen, ob danach noch etwas gefunden werden kann.

---

## 6. Was daraus folgt (Vorschlag, Entscheidungen bei Max)

**Entscheidungen (Wochenend-Paket, in dieser Reihenfolge):**
1. Referenzbuch: AP158 + AP162 + AP121 als ein Paket mit nested OOS über alle 15 Subsets (Kandidat: {Momentum, LastHour} 90,1 % In-Sample).
2. Slot-Tabelle #146 abnehmen oder ändern (ohne sie bleibt der einzige tragende Pfad zu).
3. Live-Grade-Karte als Kriterium für `LIVE_EXTRA` abnehmen (Abschnitt 4b, C1).
4. Coast-Leg-Schalter (Beine abschalten bei Puffer < 800 $) bauen ja/nein, nach OOS-Split.
5. Stufe-2-Design: θ-Gate als Vorfilter, gepaarter Null-Zwilling, Pooling, FDR kampagnenweit, zweistufig mit Staging. Das ersetzt die Šidák-Latte nicht, es gibt ihr erst eine Messung, die sie treffen kann.

**Acht Pipeline-Änderungen** (pipeline-auditor, priorisiert): (1) Trial-Stempel + Rerun-Politik, 1 Tag; (2) Slot-Tabelle + Assert, 2 h plus Abnahme; (3) Prämisse repräsentativ + CI-Gate, halber Tag; (4) Stufe 1,5 Spiegel/zweiter Markt, halber Tag; (5) Pick-Auswahl diversifizieren, 2 h; (6) Bank als Datenquelle, 1 bis 2 Tage; (7) Verfallsdatum für Urteile, halber Tag; (8) `findings.json`, 3 h. Dazu (9) Decke je Mechanismus-Familie mit F-Korrektur, (10) `$/Jahr je Kontrakt` als Pflichtfeld neben expR in jeder Zelle, (11) Vorab-Gate für Tages-Gates (q ≥ 0,7, Δμ ≥ 20 $/Tag), (12) zeitgewichtetes dw in `combine()` (0,35 pp Modellstrafe je Bein).

**θ-Gate (Mathematiker, für `eval_plan.py`, rechnet in Mikrosekunden statt 25 s/Config):**
```python
def theta_gate(mu_b, var_b, mu_c, var_c, rho, dpp_ziel=3.0, intraday_abschlag=1.0):
    g = 1.0 + (dpp_ziel + intraday_abschlag) / 28.1      # Steigung der MC-theta-Kurve, 50k-Tier
    sb, sc = var_b ** .5, var_c ** .5
    theta_neu = 2 * (mu_b + mu_c) / (var_b + var_c + 2 * rho * sb * sc)
    return theta_neu >= g * (2 * mu_b / var_b)           # False -> MC sparen
```

**Fünf Lehren fürs Logbuch** (Vorschlag, eingetragen als #158 mit Verweis hierher):
1. Ein Befund ohne Gate kommt wieder.
2. Jedes Urteil braucht einen Stempel (Engine, Daten, Kriterium), sonst wird es nach dem nächsten Fix zur Sperre statt zur Wiedervorlage.
3. Kontrollen hinter dem engsten Gate laufen nie.
4. Eine Schwelle ohne Power-Rechnung misst den Test, nicht den Markt; Beine und Events in $/Jahr je Kontrakt bewerten, nicht in expR oder Trades/Jahr.
5. Eine Register-Aussage über „nie variiert" braucht den Abdeckungszähler, eine Aussage über Code-Verhalten eine Probe.

**Offen / nicht geprüft in dieser Analyse:** die Einzelzahlen aus #088/#100/#107/#147 in den Karten-Extrakten wurden nicht gegengelesen; kein Buch-Marginal-Bootstrap neu gerechnet (sd 3,2 pp aus AP151 übernommen); das +7,3 pp des 2-Bein-Subsets und die Coast-Parameter sind In-Sample; e = 0,74 R der EMA-Leiter stammt aus der Zeit vor dem #153-Sharpe-Fix (expR selbst ist davon nicht betroffen, sharpe_ann schon).
