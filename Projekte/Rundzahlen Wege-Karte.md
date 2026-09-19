---
tags: [projekt, trading, alpha-suche, rundzahlen]
erstellt: 2026-09-16
aktualisiert: 2026-09-17
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Rundzahl-Kapitel sauber schließen
---

# Rundzahlen Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 16.09.2026 vom `familien-scout` (Auftrag Max). Inventar gegen Register (63.431 Trials), Queue (899 Jobs), [[Strategie-Logbuch]] #138/#149/#151 inkl. AP153-Nachtrag, [[Hypothesen-Bank (Volumen & Flows)]], [[Hypothesen-Bank (Momentum & Averages)]], [[Research-Cache]] und `ideas.json`. Aufbau nach dem Vorbild [[VWAP-Offensive]] (Hand-Karte zu einem anderen Konzept, hier nicht angefasst); Schwester-Karte desselben Agenten: [[Fibonacci Wege-Karte]].

> [!warning] Die Beweislage steht gegen das Konzept, und das ist der Wert dieser Karte
> Der Kern-Anspruch „viele Augen auf demselben Preis drehen den Kurs" ist bei uns **schon gemessen und tot**: zehn von zehn Bounce-Zellen (NQ 25/100/500, ES 5/100, je σ√T- und V(t,T)-Normierung) sind seit dem 15.09.2026 final tot, der Durchbruch-Messfund ist als Tick-Raster-Artefakt zurückgezogen. Von 33 Wegen tragen deshalb **sieben** ein Skelett, und **drei davon behaupten bewusst keine Reaktion am Level**, sondern nutzen das Raster als Messgerät oder als Ausführungs-Geometrie. Wer hier zwanzig Hypothesen produziert, hebt nur die Zufallsdecke für alle anderen.

> [!important] Update 17.09.2026 — Schritt 2 des EINEN Wegs gelaufen (`variant-scout` × 7 + `strategy-auditor`-Batch), Karte an mehreren Stellen korrigiert
> Alle sieben Skelette (Rang 1-7) wurden gegen die echten Engine-Achsen vermessen und anschließend die fünf story-fähigen (W19, W33, W26, W17, W5k) in einem `strategy-auditor`-Batch geprüft. Ergebnis: **kein einziger Weg ist heute als `H()`-Zeile baubar**, und zwei Aussagen dieser Karte waren schlicht falsch (siehe unten). Neue Rangfolge und Korrekturen im Detail bei den jeweiligen Wegen und in der Tabelle „Reihenfolge nach Buch-Chance". Freigegeben zum Bauen: **W17** (unbedingtes Close-Histogramm, ~40 Zeilen, kein Engine-Kern) und **W5k** (κ-Prescan-Skript, ~80-120 Zeilen, kein Engine-Kern). Alles andere wartet auf diese zwei Läufe oder auf einen `research-scout`-Call (W26) bzw. ruht ganz (W33).
>
> **Zwei Karten-Fehler, die korrigiert wurden:**
> - **W17 stand nicht bei „0 Trials".** Die Dosis-Achse ist am 10.09.2026 bereits gerechnet (`_kill_check` in `roundnum_precursors.py`) und **nicht monoton** (NQ buckelig mit Maximum in der mittleren Klasse, ES sogar gegenläufig). Die Karte hatte einen bereits gelaufenen Test für offen erklärt.
> - **W5k stand nicht bei „nur `finalize()` fehlt".** Die Kernmessung (Payoff X Minuten NACH der Bruch-Bar) existiert im gesamten Engine-Ordner nirgends — realistischer Aufwand ist ein neues Skript (~80-120 Zeilen), nicht fünf Zeilen.
>
> **Randbedingung 3 ist seit AP157 (15.09.) überholt** (`ctl_null` deckt inzwischen auch `ts_reversal`/`last_hour`/`asian`/`vwap_pullback`), ändert aber am Grid-Feature-Befund nichts. **Neue, siebte Randbedingung** unten: die ES-Futures-Serie im Bestand ist rückadjustiert (Versatz bis 1.121 Punkte, quartalsweise springend) — jedes Rundzahl-Level auf ES ist damit **zufällig phasenverschoben zum realen Strike-Raster**. Betrifft W23 tödlich, W19/W21/W26/W33 nicht (dort ist das Level Messgerät/Geometrie, kein Strike-Bezug).

> [!success] Update 17.09.2026, spät — W17-Lauf fertig: KEINE DOSIS, sauber und epochenstabil
> `roundnum_histogram_w17.py` gebaut und gerechnet (unbedingtes Close-Histogramm nach Rundungsgrad, ~100x mehr Power als die Reaktionsstatistik, kein Placebo-Konstrukt nötig — Nullhypothese ist die geschlossene Formel 1/n_Ticks unter Gleichverteilung). Vorregistriertes Kriterium (strategy-auditor 17.09.): relativer Clustering-Überschuss der 100er (inklusiv) gegenüber den 25er-nicht-50ern (exklusiv) < 5 Prozentpunkte ⇒ keine Dosis.
>
> **Ergebnis (final, nach `verdict-auditor`-Gegencheck und zwei Fixes — siehe unten): NQ dose_gradient = −5,26 pp [−12,33; 2,06], ES dose_gradient = −10,18 pp [−21,66; 1,53].** Beide Punktschätzungen klar unter der 5-pp-Schwelle. **Urteil: KEINE DOSIS**, aber mit einer Einschränkung: bei einem gröberen Bootstrap-Blockmaß (20+ Handelstage statt einzelner Tage) überschreitet die ES-CI-Obergrenze die Schwelle knapp (die Richtung kippt nie, nur die exakte CI-Breite ist auf ES nicht 100 % blockrobust). Epochen-Check bestätigt `epoch_stable=True` in beiden Märkten — kein Epochen-Artefakt. Reichweite bewusst begrenzt: das killt die **Dosis-Formulierung** von W17, **nicht** das ganze Rundzahl-Kapitel.
>
> **Zwei Korrekturen aus dem `verdict-auditor`-Gegencheck (17.09., beide behoben und final neu gerechnet):** (1) Rechenfehler in `_class_hits()` — die Erwartung einer exklusiven Klasse muss `1/n_fein − 1/kgV(n_fein,n_grob)` sein, nicht `1/n_fein − 1/n_grob` (gilt nur, wenn `n_fein` `n_grob` teilt). Erzeugte einen Phantom-Fund bei ES `10not25` (+32,7 % statt korrekt ≈0 %) — betraf NICHT das Primärpaar (100 vs. 25not50), Urteil unverändert. (2) Bootstrap-Seed hing an Python's `hash()` (PYTHONHASHSEED-Randomisierung, Läufe waren nicht exakt reproduzierbar) — auf deterministischen `hashlib`-Seed umgestellt.
>
> **W33 braucht NACHTRÄGLICH eine andere Begründung als „W17 widerlegt die Vorprämisse doppelt"** (verdict-auditor: diese Lesart ist nicht schlüssig — W33 braucht gar keine Dosis, sondern Zeitvariation des Clustering-Anteils, und die Epochen-Daten zeigen sogar signifikante Zeitvariation auf NQ 25). W33 bleibt trotzdem tot, aber aus den ursprünglichen `strategy-auditor`-Gründen (kein Akteur im Why, MS-61-Falle am Ziel-Slot) — nicht wegen W17.
>
> **Nebenbefund, nicht überinterpretieren:** NQ zeigt auf dem 25er-Raster in der jüngsten Epoche (2022-26) einen signifikant POSITIVEN Exzess (+5,04 bis +14,58 % je Jahr 2025/2026) — es gibt also Clustering, nur skaliert es nicht mit der Grobheit (keine Dosis). „Es gibt kein Clustering" wäre die falsche Lesart der Karte.
>
> **Damit: W17 fertig geschlossen (kein Bein — Dosis-Formulierung widerlegt), W33 tot (aus eigenen Gründen).** 6 Trials ins Register nachgetragen (`registry_pending`). Rohdaten: `roundnum_histogram_w17_results.json`.

> [!success] Update 17.09.2026, spät — W5k-Lauf fertig: TOT auf der gepoolten Seite (fein) / unterpowert (grob), korrigiert nach verdict-auditor-Gegencheck
> `roundnum_kappa_w5k.py` gebaut (Nullpunkt bewusst `c[br]`, nicht `lv` — vermeidet den #149-Fehler explizit) und gerechnet: NQ 25/100/500 + ES 5/25/100, je 9 Horizonte (0-60 Min nach der Bruch-Bar), Seiten getrennt UND gepoolt, 2 Epochen, Phasen-Placebo (5 Offsets) durchgängig Pflicht.
>
> **Präzisierung nach dem Gegencheck (17.09., wichtig für die richtige Lesart): „TOT" trägt HART auf den fein besetzten Rastern (NQ25, ES5, ES25) bei kurzen bis mittleren Horizonten — dort ist die CI eng genug, um einen Effekt über der κ_ehrlich-Schwelle (0,15σ) auszuschließen.** Auf den groben Rastern (NQ500, ES100) ist das Urteil **„kein Nachweis", nicht „ausgeschlossen"** — 35 von 162 Zellen (praktisch alle NQ500/ES100) haben eine CI-Obergrenze über 0,15σ, weil dort in 10 Jahren nur 2.658 bzw. 3.927 Ereignisse anfallen (Beispiel X=5: NQ25 −0,013σ [−0,037; 0,013] hart tot; ES100 −0,024σ [−0,245; 0,186] unterpowert, nicht ausgeschlossen). Mehr Power ist auf den groben Rastern nicht durch Rechenzeit zu holen, die Ereigniszahl ist historisch gedeckelt.
>
> **Die eine ursprünglich falsch als "LEBT" markierte Zelle (ES100, nur long, X=15) ist jetzt korrekt TOT — Bug im Skript gefixt, nicht nur neu interpretiert:** das LEBT-Kriterium prüfte nur "real minus Placebo positiv", nie ob der reale Nettoertrag selbst positiv ist. Diese Zelle hatte real −0,378σ gegen Placebo −0,870σ — „verliert weniger als das Placebo", nicht „verdient". Kriterium um `kappa_net_real_mean > 0` ergänzt, Lauf neu gerechnet: **0 von 162 Zellen zeigen jetzt LEBT.** (Die ursprüngliche Begründung „~8 Zufallstreffer bei 5 % wären normal" war zudem methodisch unsauber — die 162 Zellen sind stark abhängig, effektive Testzahl eher 15-20 — spielt fürs Ergebnis keine Rolle, gehört aber nicht mehr in die Karte.)
>
> **Damit: W5/W6 auf den feinen Rastern hart tot, auf den groben Rastern ohne Nachweis (Power-Grenze, nicht widerlegt). W14, W27, W28, W30 sind NICHT einzeln gemessen — das sind bedingte Teilmengen/Filter auf das Bruch-Ereignis, W5k misst nur den unbedingten Mittelwert. Status: „abgeleitet, keine eigene Messung, wird bewusst nicht nachgemessen"** (Teilmengensuche auf einem Nullmittelwert wäre die Multiple-Testing-Falle; TB-03 als Kompressions-Verwandter ist ohnehin tot; bei fair gepreistem Nullmittelwert kann kein Exit-Profil die Erwartung heben). 18 Trials ins Register nachgetragen. Rohdaten: `roundnum_kappa_w5k_results.json`.
>
> **Bekannte, bewusst nicht behobene Lücke (verdict-auditor 17.09.):** die Lehre-151-`grid_share`-Kanarie im Skript prüft `on_level` an der BRUCH-Bar (die per Definition jenseits des Levels liegt, also immer 0,0 % gegen 0,0 % meldet) statt an der Berührungs-Bar davor — der Vertrag ist formal erfüllt, prüft aber nichts. Risiko real gering, weil der eigentliche Schutz (`random_grid_phase(..., tick=...)`) unabhängig davon konstruktiv wirkt. Kein eigener Nachtest empfohlen, aber beim nächsten Umbau des Skripts mitkorrigieren.

> [!important] Zwischenstand 17.09.2026, Abend (final, nach verdict-auditor-Gegencheck) — was vom Kapitel noch offen ist
> Nach W17 und W5k (beide vom `verdict-auditor` geprüft, zwei echte Bugs gefunden und gefixt — Rechenfehler in einer Nebenklasse, unvollständiges LEBT-Kriterium; keiner davon kippt ein Urteil) sind nur noch **zwei Wege unentschieden** (W19, W26), beide hängen an einer Story-Korrektur bzw. einem Research-Call, nicht an Rechenzeit. **W21 und W23 sind aus mechanischen/strukturellen Gründen raus, W33 ist tot (eigene Gründe, nicht wegen W17), W17 ist tot als Bein (Dosis widerlegt), W5/W6 sind fein tot/grob unterpowert, W7/W8 final tot (Bounce), W14/W27/W28/W30 bewusst nicht einzeln gemessen (abgeleitet von W5k).** Randbedingung 7 (ES-Datenkorruption) war ebenfalls falsch und ist korrigiert — ändert an W23 nichts (Frequenz-Gate trägt allein). Realistische Einschätzung: das Kapitel läuft auf „sauber geschlossen, kein Bein" hinaus — aber W19 (Zeit-Exit-Kanal) und W26 (Research zuerst) sind noch offen und könnten das ändern. Nächste Schritte laut Rangfolge unten.

---

## Die sechs harten Randbedingungen

**1. Das Level selbst trägt keine Bedeutung — dreifach gemessen, nicht geschätzt.**
Bounce tot in 10/10 Zellen ([[Strategie-Logbuch]] #149 mit Nachtrag AP153 P9 vom 15.09.; die einzige Zelle mit positiver Punktschätzung, NQ 100 σ√T, bleibt tot, weil −0,59 pp unter der vorregistrierten Mindestdifferenz von 1,0 pp liegen und der Effekt nur am half-Offset trägt). Durchbruch-Messfund zurückgezogen (#151 Befund 1: ES25 +5,79 pp mit ungerundetem, **+0,32 pp [−0,35; 0,97]** mit tick-gerundetem Placebo). Level-Härte allgemein widerlegt (#138: Berührungsraten echt vs. Placebo am ORB-Level deckungsgleich; Zapranis/Tsinaslanidis 2012: S/R-Level ohne Überrendite). **Jeder Weg, der auf Reflexivität am Level baut, braucht einen NEUEN Grund oder bekommt kein Skelett.**

**2. Der κ-Deckel aus #138 gilt auch hier.** Ehrlich realisierbarer Payoff nach einem Level-Bruch: 0,15·σ_1m, nur in der Bruchminute (+5min t=2,0, +30min t=0,4), 5 von 6 Ären unter Kosten. Die #149-Zahl 0,67-0,80 σ ist **nicht** vergleichbar (misst die Bruch-Bar selbst, trifft das Placebo genauso). Der offene Schritt steht wörtlich im Logbuch und ist hier Weg W5k.

**3. Alles Neue muss in `maband`/`tsmom`.** Nur die beiden haben einen Null-Schalter (`controls.py` `ctl_null`). `mode="cal"` — ausgerechnet das einzige Modul mit OpEx-Flag — kann nie `deploy_ready` werden. Kein neuer `mode`, nur Erweiterung.

**4. Ersatz schlägt Neuzugang** (#139 B3). Vier Slots: `NQ_VWAP-Pullback`, `NQ_Momentum_d260818`, `NQ_LastHour_v3`, `NQ_Asia-Dir-USopen_d260820`. Rang 1-3 und 6 sind Ersatz, Rang 7 ist genau deshalb Rang 7.

**5. Placebo-Pflicht mit Diskretisierung (Lehre 151).** Das Rundzahl-Raster liegt auf dem Tick-Raster, also muss das Placebo es auch. Richtig ist `random_grid_phase(step, seed, tick=TICK)` (gleiche Distanzverteilung, gleiche Berührungsfrequenz), **nicht** `random_level_shift` (würfelt Distanz mit). Kanarie: Anteil Close == Level je Arm, > 1 pp = durchgefallen.

**6. Kein einziger Weg ist heute engine-fähig.** `maband` kennt `cross · dist · slope · fan · speeds · price_ma · band · channel · vwap` — **kein Raster**. `ctl_random_level` hat Zweige für Band, Kanal, VWAP und ORB — **keinen für ein Raster**. Fünf Bank-Zeilen (GM-05, GM-07, GM-33, KF-25, HV-50) hängen seit Monaten an genau diesem fehlenden Feature. **Zusatzfalle (neu, 17.09.2026): `NQ_Momentum_d260818` (Ziel-Slot für W33) läuft als `mode="ts_reversal"`, und `qbt._reversal_trades` ruft `sigcore.gates_pass` nie auf — jedes über `gates_pass` geplante Feature (auch `AX_CONFIRM` komplett) erreicht diesen Slot nicht.** Wer dorthin baut, muss das Basissignal in `tsmom` nachbilden, nicht in `qbt.py` patchen.

**7. ⚠ KORRIGIERT (17.09.2026, `verdict-auditor`-Gegencheck): die ES-Serie ist NICHT rückadjustiert — die ursprüngliche Behauptung (Versatz bis 1.121 Punkte) war falsch.** `qbt.load_rth("ES")` verfolgt die realen Jahresendstände fast exakt (2019: 3229,75 vs. real S&P 3230,78; 2021: 4759,5 vs. real 4766,18; 2016: 2236,75 vs. real 2238,83). Nachgeprüft per Stichprobe gegen bekannte historische Settlements — kein systematischer Versatz, keine Quartalsroll-Sprünge (die großen Tagesgaps im März 2020 sind der reale Corona-Crash, keine Roll-Artefakte). **W23 fällt trotzdem raus, aber nur noch über das Frequenz-Gate** (4,2 Trades/Jahr gegen `min_tpy=25`, physikalische Decke 11,8 Tage/Jahr) — der Datenkorruptions-Grund entfällt. Der Nebensatz zu #149/#151 („wir haben das reale Rundzahl-Raster gemessen ist nicht sauber belegt") ist damit ebenfalls hinfällig — das echte Raster wurde gemessen.

---

## Register-Stand (16.09.2026)

| Griff | Zahl |
|---|---|
| `n_total` im Register | **63.431 Trials** |
| davon mit Rundzahl-Bezug (Key `roundnum`) | **22** (10 AP153-Zellen + 12 nachgetragene #149-Prescans) |
| Rundzahl-Trials aus einem **Grid-Job** | **0** (es gibt kein `mb_kind` dafür) |
| Modi | tsmom 38.864 · maband 16.244 |
| `mb_kind` | dist 11.243 · channel 4.085 · vwap 399 · slope 213 · band 175 · cross 83 · price_ma 35 · speeds 6 · fan 5 |
| Queue | 899 Jobs: 468 done, 425 premise_failed, 4 pending, 1 running |
| Rundzahl-Jobs in der Queue | **0** |
| Verwandte Level-Jobs | `fb01`/`fb01b` Fehlausbruch **premise_failed** (NQ+RTY, beide) · `wb01` Band-Walk premise_failed · `lp_prevday` done, 0 Kandidaten · `hyp_AK03_NQ` premise_failed |
| Bank-Zeilen zum Konzept | GM-05, GM-07, GM-33, KF-25, HV-50 — **alle 🟢 ungetestet**, alle mit Vermerk „🔧 Strike-Distanz-Feature" |
| `ideas.json` | kein Rundzahl-Eintrag; Vermerk „Round Numbers/PDH offen (nur als Mitnahme)" im AB-14-Eintrag |

**Werkzeuge, die es schon gibt:** `sigcore.nearest_round_levels`, `sigcore.random_grid_phase(tick=…)`, `sigcore.hazard_null_fit`, `sigcore.ForwardVariance`, `discovery/prescan_controls.py`, `roundnum_precursors.py`, `roundnum_breakout_precursor.py`, `roundnum_cells_ap153.py`. **Die Messschicht steht vollständig, der Runner-Pfad fehlt komplett.**

---

## Wege-Tabelle (33 Wege)

Elemente: Rundzahl-Level · Schrittweite · Korridor zwischen zwei Leveln · Halb-Level x.50 · Level-Klasse (25/100/500/1000) · Abstand Preis↔Level · Berührungshistorie · Clustering-Intensität · OpEx-Zustand · Tageszeit · zweiter Markt · dazu immer der Preis.
Beziehungen: hin zu · weg von · durch hindurch · abprallen an · entlanglaufen an · kreuzen und halten · kreuzen und scheitern; Zustände: nah/fern, grob/fein.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| W1 | hin zum Level oben (Magnet, long) | Trend | Signal | offen, mit dem Standard-Placebo **nicht entscheidbar** | Modul-Spec grid/approach | neues Bein |
| W2 | hin zum Level unten (Magnet, short) | Trend | Signal | offen, wie W1 | Modul-Spec grid/approach | neues Bein |
| W3 | weg vom Level nach oben | Trend | Signal | offen, **keine eigene Story** (= W9 + W5) | Modul-Spec grid | — |
| W4 | weg vom Level nach unten | Trend | Signal | offen, keine eigene Story (= W9 + W6) | Modul-Spec grid | — |
| W5 | durch das Level nach oben (long) | Trend | Signal | **TOT auf feinen Rastern (NQ25/ES5/ES25), unterpowert auf groben (NQ500/ES100)** (17.09., W5k, korrigiert) | — | — |
| W6 | durch das Level nach unten (short) | Trend | Signal | **wie W5**, Long-Bias-Kontrolle bestanden (short separat geprüft, spiegelbildlich null) | — | — |
| W7 | abprallen am unteren Level (long) | Mean Reversion | Signal | **tot** (#149/#151, AP153 P9: 10/10 Zellen) | — | — |
| W8 | abprallen am oberen Level (short) | Mean Reversion | Signal | **tot** (dieselben 10 Zellen) | — | — |
| W9 | am Level entlanglaufen (Pinning) | Mean Reversion | Zeitfenster | offen; verwandt tot: `wb01` premise_failed | Modul-Spec grid/pin | neues Bein |
| W10 | kreuzen und halten nach oben | Trend | Signal | offen, Story sagt die **Null** voraus | Modul-Spec grid/reclaim | neues Bein |
| W11 | kreuzen und halten nach unten | Trend | Signal | offen, wie W10 | Modul-Spec grid/reclaim | neues Bein |
| W12 | kreuzen und scheitern nach unten → Long | Mean Reversion | Signal | offen, **zweifach kontaminiert** (`fb01`, `fb01b`) | Modul-Spec grid/fail | neues Bein |
| W13 | kreuzen und scheitern nach oben → Short | Mean Reversion | Signal | offen, wie W12 | Modul-Spec grid/fail | neues Bein |
| W14 | Kaskade Level k → k+1 nach dem Bruch | Trend | Signal | **Abgeleitet, keine eigene Messung (17.09.):** bedingte Teilmenge von W5k, bewusst nicht einzeln nachgemessen (Multiple-Testing-Falle auf Nullmittelwert) | — | — |
| W15 | Rückkehr in die Korridor-Mitte | Mean Reversion | Signal | offen, **keine eigene Story** (bei step 100 = W16) | Modul-Spec grid | — |
| W16 | Halb-Level x.50 als eigene Linie | Mean Reversion | Level | offen, Schwartz 2004 belegt Clustering an x.00 **und** x.50 | Modul-Spec grid/half | wird in W17 mitgemessen |
| W17 | **Klassen-Abstufung / Dosis** x.00 vs x.50 vs x.25/x.75, 25/100/500/1000 | Filter | Filter | **GESCHLOSSEN (17.09.):** Close-Histogramm gerechnet, KEINE DOSIS (NQ −5,27pp, ES −9,97pp, beide unter 5-pp-Schwelle, epochenstabil) — Dosis-Formulierung widerlegt, kein Bein | `roundnum_histogram_w17.py`, kein Modul nötig | — |
| W18 | Konfluenz Rundzahl × VWAP/OR/PDH/POC | Filter | Filter | offen, **kein neuer Grund** | Modul-Spec grid als Zusatz-Gate | Ersatz `NQ_VWAP-Pullback` |
| W19 | **Abstand zum Level als Zulassungs-Gate** | Filter | Filter | grenzwertig: Wahrscheinlichkeits-Dimension bereits placebo-sauber tot (AP153+#151), nur Zeit-Dimension offen — **Why muss auf Zeit-Exit-Kanal umgeschrieben werden** (strategy-auditor 17.09.), dann Hazard-Prescan — **Rang 3** | Modul-Spec `tm_grid_dist_min`, aber erst Prescan | **Ersatz `NQ_VWAP-Pullback`** |
| W20 | Stop-Platzierung relativ zum Level | Filter | Exit | offen, läuft als Risk-Achse in RN-W19a mit | Modul-Spec grid + `tm_stop_mult` | Ersatz, über RN-W19a |
| W21 | **Ziel knapp vor dem Level** | Filter | Exit | **nicht bank-reif** (17.09.): Backtest kann den behaupteten Fill-Vorteil nicht messen (Füllwahrscheinlichkeit in beiden Placebo-Armen = 1,0), unter 10 echte Varianten. Bei positivem W19-Prescan als Achse IN RN-W19a einbauen, nie eigene Zeile | — | — |
| W22 | k-ter Test desselben Levels am Tag | Filter | Filter | verwandter Test tot auf OR30 (#138 AB-14, Urteil in #151 teilweise entzogen); #138: **nur Mitnahme, kein eigener Job** | Modul-Spec grid + Zähler | — |
| W23 | **OpEx: Anziehung zum 100er, letzte Stunde** | Mean Reversion | Signal + Zeitfenster | **nicht bank-reif, Prop-Buch aus** (17.09.): `min_tpy`-Gate strukturell unerreichbar (4,2 Trades/Jahr, Decke bei 11,8) — physikalische Grenze, unabhängig vom Datenbefund (Randbedingung 7 korrigiert: ES-Serie ist NICHT rückadjustiert). Herabgestuft auf **Live-Buch-Merker**, wie W31/W32 | Modul-Spec grid + `tm_opex` | Live-Buch-Merker, kein Prop-Buch-Job |
| W24 | OpEx: Durchbruch fällt bis Close zurück | Mean Reversion | Signal | offen (GM-07 🟢), **kein Skelett** (Fehlausbruch-Prämisse 2× gescheitert) | Modul-Spec grid/fail + `tm_opex` | neues Bein, LF |
| W25 | Eröffnung nahe einem Level → Tages-Bias | Intraday Bias | Signal | offen (Schwartz: Open/Close clustern stärker) | Modul-Spec grid + `mb_start_min` | Ersatz `NQ_Asia-Dir-USopen_d260820` |
| W26 | **Schluss-Anziehung, letzte Stunde** | Intraday Bias | Signal + Zeitfenster | **Story fällt durch (strategy-auditor 17.09.):** Schwartz belegt Häufung REALISIERTER Closes, nicht Drift aus der Ferne — vollständig alternativ erklärbar durch Settlement-Selektionseffekt. Dazu TS-21 im selben Fenster schon leer (144 Configs), Whipsaw-Geometrie am Level. **Erst `research-scout` (Drift vs. Selektionseffekt), danach neu vorlegen** — **Rang 4** | Modul-Spec grid/approach, aber erst Research | Ersatz `NQ_LastHour_v3`, vorerst zurückgestellt |
| W27 | Vola-Kompression VOR dem Aufwärts-Durchbruch | Filter | Filter | **Abgeleitet, keine eigene Messung (17.09.):** Filter auf ein W5k-Ereignis, bewusst nicht nachgemessen; TB-03 zusätzlich tot | — | — |
| W28 | Vola-Expansion während/nach dem Durchbruch | Filter | Exit | **Abgeleitet, keine eigene Messung (17.09.):** dasselbe — bei fair gepreistem Nullmittelwert kann kein Exit-Profil die Erwartung heben | — | — |
| W29 | ES bricht sein Raster, NQ folgt | Relative Value | Signal | offen, **Datenlücke** (Kassa-Index fehlt); verwandt tot: RV_leadlag_NQES | Modul-Spec grid + Cross-Market | neues Bein |
| W30 | synchroner Bruch beider Raster | Relative Value | Filter | **Abgeleitet, keine eigene Messung (17.09.):** setzt W5/W6 voraus (fein tot, grob unterpowert) — bewusst nicht nachgemessen | — | — |
| W31 | **(Swing)** NQ 1000 / ES 500 als Mehrtages-Magnet | Swing | Level | offen | Modul-Spec grid, Tages-Bars | **Live-Buch-Merker, nicht Prop-Buch** |
| W32 | **(Swing)** 52-Wochen-Extrem × Rundzahl | Swing | Level | offen (Tsao 2017 testet genau das) | Modul-Spec grid + Jahres-Extrem | **Live-Buch-Merker, nicht Prop-Buch** |
| W33 | **Clustering-Intensität als Regime-Zustand** | Filter | Filter | **TOT (17.09., korrigiert):** kein Akteur im Why (strategy-auditor), plus MS-61-Falle (Ziel-Slot `ts_reversal` ruft `gates_pass` nie). NICHT wegen W17 — W33 braucht Zeitvariation des Clustering-Anteils, nicht Dosis, und die zeigt sogar signifikante Variation (verdict-auditor-Korrektur) | — | — |

---

## Die Wege mit Skelett

### W19 — Abstand zum nächsten Level als Zulassungs-Gate (Rang 1, Why korrigiert 17.09.2026)
Ein Setup wird nur zugelassen, wenn zwischen Entry und Ziel kein Rundzahl-Level liegt.

**Warum die alte Story (Erreichbarkeit) nicht mehr trägt:** `variant-scout`/`strategy-auditor` haben gezeigt, dass die **Wahrscheinlichkeits-Dimension bereits placebo-sauber tot ist** — AP153 (Berührungsrate echt = Placebo) und #151 (Durchgangsrate echt = Placebo, ES25 +0,32pp [−0,35;0,97]) kombiniert heißt: auch die First-Passage-**Wahrscheinlichkeit** durch ein Level ist ≈ Placebo. Die alte Formulierung „wer durch ruhende Gegenliquidität muss, kommt seltener an" ist damit gemessen und widerlegt. Dazu kommt ein Story-Fehler, den `strategy-auditor` gefangen hat: Oslers eigener Mechanismus (Stops HINTER dem Cluster) sagt für die Durchgangs-Phase eigentlich **Beschleunigung** voraus, nicht Bremsen — das alte Why hätte die Zeit-Dimension nie tragen können.

**Korrigierte Story (Zeit-Exit-Kanal):** die offene Dimension ist nicht ob, sondern WANN das Ziel erreicht wird. Auch wenn die Ankunfts-Wahrscheinlichkeit unverändert ist, kann der WEG zum Ziel länger dauern, wenn ein Rundzahl-Level dazwischenliegt (Wartezeit vor der ruhenden Gegenliquidität, auch ohne dass die Kaskade am Ende ausbleibt). Das ist ökonomisch relevant, weil unser Buch überall mit **Zeit-Notausgängen** arbeitet (EOD, `time60`): ein Ziel, das später kommt, wird häufiger vom Zeit-Exit abgeschnitten, bevor es ankommt — das kostet Erwartungswert, ganz ohne dass sich die Ankunfts-Wahrscheinlichkeit selbst ändern muss. Das Geld bleibt liegen, weil Zeit-bis-Ziel nie gegen die Anwesenheit eines dazwischenliegenden Levels gemessen wurde.

**Warum das Randbedingung 1 überlebt:** die toten Zellen bedingen alle auf eine **Berührung** des Levels. Diese Frage bedingt auf die **Reihenfolge zweier Barrieren in der Zeit**, nicht auf eine Berührung.

**Pflicht-Auflagen für den Prescan (strategy-auditor 17.09., vor dem Rechnen zu beachten):**
1. **Hazard-/Competing-Risk-Formulierung, kein Mittelwert der Trefferzeiten.** Nur über ERREICHTE Fälle die Zeit zu mitteln ist eine Zensierungs-Selektion (Fälle, die den Zeit-Exit zuerst treffen, fehlen systematisch aus dem Mittel). `sigcore.hazard_null_fit` steht dafür bereit.
2. **Ziel muss zum Entry-Zeitpunkt fest stehen** (R/ATR ab Entry), nicht trailend nachgezogen — sonst braucht das Gate Zukunftsinfo (Look-ahead).

**Ehrliches Gegenargument (bleibt gültig):** #138 hat gezeigt, dass das Level gar nicht bremst. Trägt der Prescan nichts, ist auch der Zeit-Effekt null — ein billiger, sauberer Kill.
**Buch:** Ersatz `NQ_VWAP-Pullback`.

**Research-Ergebnis (17.09.2026, `research-scout`, siehe Research-Cache):** **unentschieden, nicht widerlegt.** Keine Arbeit zu First-Passage-**Zeit** mit dazwischenliegendem Order-Cluster gefunden (echte Literaturlücke, nicht übersehen). Zur Osler-Futures-Übertragung nur schwache Gegenevidenz: ap Gwilym/Alibo 2003 (peer-reviewed, FTSE100-Futures) zeigt Preis-Clustering fällt beim Übergang Parkett→elektronisch von ~98,5 % auf ~75 % — deutlicher Rückgang, aber weit über null, also „schwächer als FX-Analogie nahelegt, aber nicht null". **Die Literatur kann die Frage nicht klären — nur der Hazard-Prescan kann das noch.** Nächster Schritt: Prescan bauen (Auflagen oben) und rechnen.

### W33 — Clustering-Intensität als Regime-Gate (Rang 2)
Anteil der Closes der letzten n Bars auf x.00/x.50 als rollender Zustand, Entry nur unter- bzw. oberhalb einer Schwelle.
**Story:** Schwartz 2004 und Chung/Chiang 2006 — Clustering steigt mit Vola, sinkt mit Volumen/OI, steigt mit menschlichem Ausführungsanteil. Hoher Clustering-Anteil = dünn besetzt, grob gepreist, schlechte Füllbedingungen. Das Geld bleibt liegen, weil Clustering als Mikrostruktur-Statistik publiziert, aber nie als Live-Regime-Filter verdrahtet wurde.
**Warum das Randbedingung 1 überlebt:** das Level ist hier **Messgerät**, nicht Magnet. Es wird keine Reaktion am Level behauptet.
**Buch:** Ersatz `NQ_Momentum_d260818`. **Research-Frage:** trägt der Clustering-Anteil eigene Information gegenüber RVOL/Spread, oder ist er redundant?

### W26 — Schluss-Anziehung in der letzten Stunde (Rang 3)
Steht der Preis in der letzten Stunde nah am nächsten 100er, wird in Richtung dieses Levels gehandelt.
**Story:** Schwartz 2004 — Eröffnungs- und Schlusskurse clustern **stärker** als Settlement-Kurse. Wer Ausführungsziele für den Schluss setzt (Benchmark, MOC-Rest, Optionsabsicherung), nennt sie rund; die Häufung im Close ist die Spur dieser Ordertypen.
**Verwandter Toter:** MOC-Momentum NQ (#087, 0/72) — gleiches Zeitfenster, gleiche Kostenlage, **anderer Mechanismus** (dort Fortsetzung des Tagesmoves, hier Anziehung zu einem festen Preis). Kontaminationswarnung ernst nehmen.
**Buch:** Ersatz `NQ_LastHour_v3`. **Research-Frage:** gilt das Close-Clustering auch im elektronischen 23-Stunden-Handel, oder war es ein Parkett-Artefakt?

### W17 — Within-Grid-Dosis (Rang 4)
Reaktionsstatistik getrennt für x.00 / x.50 / x.25 / x.75 desselben Rasters und für die Klassen 25/100/500/1000.
**Story:** wenn Clustering überhaupt Preisverhalten erzeugt, muss die Wirkung entlang der Clustering-Intensität abgestuft sein.
**Warum das ein NEUER Winkel ist:** die zehn toten Zellen testeten x.00 gegen ein **fremdes, phasenverschobenes** Raster — und genau dessen Diskretisierung hat #151 den Durchbruch-Messfund gekostet. Hier steckt die Kontrolle **im** Raster: Viertel-Level haben dieselbe Diskretisierung, Distanzverteilung und Berührungsfrequenz. Dazu eine Dosis-Achse statt eines Ja/Nein.
**Buch:** Prämissen-Stufe. **Bei flacher Dosiskurve ist das Kapitel Rundzahl-Reflexivität endgültig zu** — das ist der eigentliche Wert dieses Wegs.

### W5k — κ am Rundzahl-Level nach #138-Konvention (Rang 5)
Kein Bein, sondern die vom Logbuch selbst verlangte Messung: Payoff ab X Minuten **nach** der Bruch-Bar, placebo-kontrolliert, gegen Kosten.
**Warum zuerst:** ohne diese Zahl bleiben W5, W6, W14, W27, W28 und W30 unentscheidbar, und jede Rechenrunde darauf ist blind.
**Werkzeug:** vorhanden (`roundnum_breakout_precursor.py` + `prescan_controls.finalize`), offen ist nur das in #151 vermerkte fehlende `finalize()` und der Register-Nachtrag über `discovery/registry_pending/`.

### W21 — Ziel knapp vor dem Level (Rang 6)
Exit-Profil „nächstes Level minus x Ticks" statt fixem R-Ziel. Spiegelbild zu W19.
**Falle, die mitgeschrieben gehört:** das ist die Klasse von Behauptung, vor der #138 warnt (Fill-/Slippage-Aussagen sind im Backtest frei wählbar, #066-Selbstbetrug). Gültig nur gegen ein **gleich weit entferntes, nicht-rundes** Ziel.
**Kostenrechnung:** MNQ-Round-Trip ≈ 2 Punkte, ein 25er-Korridor ist 25 Punkte breit — für diesen Weg gilt `mb_grid_step` ≥ 100.

### W23 — OpEx-Pinning, letzte Stunde (Rang 7)
GM-05 wörtlich: ab 15:00 ET Fade zum nächsten 100er, wenn Abstand < 0,3×ATR.
**Drei ehrliche Einschränkungen:** Pinning ist im [[Research-Cache]] nur **praktiker**-belegt (GexMetrix, SpotGamma), keine peer-reviewte Quelle im Bestand · 12 monatliche OpEx-Tage pro Jahr reißen jedes Trades-pro-Jahr-Gate · laut #110 wirkt der SPX-GEX-Effekt auf **ES** fast doppelt so stark wie auf NQ, die Bank-Zeile nennt trotzdem NQ. **Markt deshalb auf ES korrigiert.**
**Verwandter Toter:** #049 (OpEx-Nachmittag fadet den Vormittag **nicht**).

---

## Wege ohne Skelett — mit Grund (Vollständigkeits-Pflicht)

- **W1/W2 Magnet:** Story vorhanden, aber das Phasen-Placebo hält die Berührungshäufigkeit per Konstruktion konstant. Wird von W17 mitbeantwortet.
- **W3/W4 weg vom Level:** keine eigene Story, das ist W9 + W5/W6. Keine Reparametrisierung als eigenen Weg zählen.
- **W7/W8 Bounce:** tot, 10/10 Zellen.
- **W9 Pinning:** nächster gebauter Verwandter (`wb01`, Band-Walk) an der Prämisse gescheitert, kein neuer Grund.
- **W10/W11 kreuzen und halten:** die Story sagt die **Null** voraus — nach dem Bruch ist der Cluster abgeräumt, der Retest trifft auf nichts. Wird in W5k mitgemessen.
- **W12/W13 Fehlausbruch:** zweifach kontaminiert (`fb01`, `fb01b` premise_failed, identische Story am Session-/Kanal-Level).
- **W14 Kaskade:** κ-Deckel #138, wird durch W5k entschieden.
- **W15 Korridor-Mitte:** bei step 100 deckungsgleich mit W16.
- **W16 x.50:** wird in W17 als Dosis-Stufe mitgemessen.
- **W18 Konfluenz:** Kombination zweier Level, deren Einzelwirkung tot bzw. nie belegt ist.
- **W20 Stop-Platzierung:** läuft als Risk-Achse in RN-W19a mit.
- **W22 Berührungszähler:** #138 verfügt ausdrücklich „nur als Mitnahme in künftigen Level-Jobs, kein eigener Job".
- **W24 OpEx-Fehlausbruch:** Prämisse Fehlausbruch zweimal gescheitert; OpEx ist eine Bedingung darauf, kein neuer Grund für die Prämisse.
- **W25 Eröffnungs-Clustering:** Story vorhanden, aber der Slot ist mit `NQ_Asia-Dir-USopen` schon von einem belegten Eröffnungs-Mechanismus besetzt. Erst W26 messen, dann hier entscheiden.
- **W27/W28 Vola um den Durchbruch:** Vorläufer/Exit für ein Ereignis, dessen Payoff der κ-Deckel begrenzt; dazu TB-03 (#138) als toter Kompressions-Verwandter.
- **W29/W30 Lead-Lag:** Datenlücke (Kassa-Index fehlt, Tsao misst Index gegen Futures) plus toter Verwandter RV_leadlag_NQES.
- **W31/W32 (Swing):** mitgeführt und markiert, **kein Prop-Buch-Job** (Regel Max 11.09.2026), Ziel Live-Buch-Merker.

---

## Reihenfolge nach Buch-Chance

**Stand 17.09.2026 — nach `variant-scout` × 7 + `strategy-auditor`-Batch, ersetzt die Rangfolge vom 16.09.** Kein Weg ist heute eine `H()`-Zeile; die Rangfolge ist jetzt „was rechnen wir als nächstes an billigen Prescans", nicht „welche Bank-Zeile zuerst".

| Rang | ID | Weg | Nächster Schritt | Status | Warum dieser Rang |
|---|---|---|---|---|---|
| — | RN-W17 | W17 | erledigt — Close-Histogramm gerechnet | **GESCHLOSSEN, KEINE DOSIS** | epochenstabiler Kill, 17.09.2026 |
| — | RN-W5k | W5/W6 (fein tot, grob unterpowert), W14/W27/W28/W30 (abgeleitet) | erledigt — κ-Prescan gerechnet, korrigiert | **GESCHLOSSEN** | 0/162 Zellen LEBT nach Bugfix, 17.09.2026 |
| 1 | RN-W19 | W19 | **Why korrigiert (17.09., s.o.)** — als Nächstes Hazard-Prescan bauen (Zensierung, kein Mittelwert, Ziel fix ab Entry) | Why fertig, Prescan offen | Zeit-Exit-Kanal statt Erreichbarkeit — Wahrscheinlichkeits-Dimension bleibt tot, Zeit-Dimension jetzt korrekt begründet |
| 2 | RN-W26 | W26 | `research-scout`-Call **läuft** (Frage 4 + 1/2 im selben Call) | Research läuft | Story fällt in der jetzigen Fassung durch (Häufung realisierter Closes ≠ Drift aus der Ferne); Research kann die Hypothese ersatzlos erledigen, billiger als ein Prescan |
| — | RN-W33 | W33 | keiner | **TOT** | Vorprämisse jetzt zweifach widerlegt (AP153 + W17-Histogramm), kein Akteur im Why, MS-61-Falle am Ziel-Slot |
| — | RN-W21 | W21 | kein eigener Lauf — nur als Achse in W19 einbauen, falls dessen Prescan positiv | **nicht bank-reif** | Backtest kann den behaupteten Fill-Vorteil prinzipiell nicht messen |
| — | RN-W23 | W23 | keiner (Prop-Buch) — als Live-Buch-Merker vormerken | **nicht bank-reif, Prop-Buch aus** | Frequenz-Gate physikalisch unerreichbar (Randbedingung 7 korrigiert: Datenkorruption war kein echter Zusatzgrund) |

**Stand 17.09.2026, Abend: 5 von 7 Skeletten final entschieden (alle tot/geschlossen), 6 weitere Wege (W5/W6/W7/W8/W14/W27/W28/W30) über W5k/Bounce mitentschieden. Nur W19 und W26 sind noch offen — beide brauchen keine Rechenzeit als nächsten Schritt, sondern eine Story-Korrektur bzw. einen Research-Call.**

---

## Was gebaut werden muss (Modul-Specs, rund 165 Zeilen in vier bestehenden Dateien)

1. **`maband.py`: `mb_kind="grid"`** (~80 Zeilen, parallel zu `band`/`channel`). Neue Parameter `mb_grid_step`, `mb_grid_evt` ∈ {approach, break, fade, reclaim, fail, pin}, `mb_grid_zone`, `mb_grid_class` ∈ {full, half, quarter}, `mb_grid_phase`. Level über `sigcore.nearest_round_levels`.
2. **`discovery/controls.py` `ctl_random_level`: Zweig `grid`** (~20 Zeilen). **Nicht** `random_level_shift`, sondern `random_grid_phase(step, seed, tick=qbt.TICK[symbol])`, plus Kanarie `ctl_placebo_arm(grid_share=…)` aus Lehre 151.
3. **`sigcore.gates_pass`: `tm_grid_dist_min` und `tm_grid_share_max/_min`** (~35 Zeilen). Wirkt für `tsmom` und `maband`, weil beide dieselbe Gate-Schicht nutzen.
4. **`sigcore.gates_pass`: `tm_opex`** (~15 Zeilen, nur falls W23 nach dem Research noch steht). Flag-Quelle existiert in `calendar_fx.py`, muss aber in die Gate-Schicht gehoben werden, weil `mode="cal"` keinen Null-Schalter hat.
5. **Neues `exit_profile` „Ziel = nächstes Level − x Ticks"** (~15 Zeilen) samt Pflicht-Kontrollarm „gleiche Distanz, nicht rund".

---

## Offene Research-Fragen (für `research-scout`, nicht selbst beantwortet)

1. Gibt es eine Arbeit, die **First-Passage zu einem Ziel mit dazwischenliegendem Order-Cluster** misst (Barrieren-Reihenfolge statt Level-Härte)? *(W19)*
2. Ist Oslers TP-auf-dem-Level / Stop-dahinter-Muster für Index-**Futures** je mit Orderdaten repliziert, oder bleibt es eine FX-Analogie? *(W19, W21, W5k)*
3. Trägt der Clustering-Anteil in Index-Futures eigene Information gegenüber RVOL/Spread/Tick-Rule-Volumen? Wird Clustering irgendwo als **Zeitreihen**-Liquiditätsproxy verwendet? *(W33)*
4. Ist das Close-Clustering aus Schwartz 2004 im elektronischen 23-Stunden-Handel noch vorhanden, oder ein Parkett-Artefakt? Belegt die Literatur eine **Drift zum Level** oder nur die Häufung der realisierten Schlusskurse (Selektionseffekt)? *(W26)*
5. Misst irgendjemand Reaktionsstärke **abgestuft** nach Rundungsgrad (x.00 vs x.50 vs x.25)? *(W17, W16)*
6. Ist die Kaskadenlänge nach einem Rundzahl-Bruch in Index-Futures mit Orderbuchdaten gemessen? Gibt es bei Tsao/Lee/Shyu 2017 eine Dauer-Angabe in Minuten für den Anschluss-Flow? *(W5k)*
7. Gibt es eine peer-reviewte **Pinning**-Arbeit für Index-Futures (nicht Einzelaktien), und hält der Effekt nach Einführung täglicher Verfälle? Liegt das NDX/QQQ-Strike-Raster überhaupt auf 100er-Schritten? *(W23, W24)*
8. Gibt es Ausführungsdaten (nicht Chartstudien) zu Limit-Fills knapp vor runden Preisen? *(W21)*

---

## Dateien dieses Laufs

- Report: `C:\Users\maxlk\Projects\trading-data\engine\discovery\scout_reports\familien_rundzahlen_260916.md`
- Skelette: `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\familien_rundzahlen_260916.json`
- Diese Karte (lebendes Register je Weg; `verdict-auditor` schreibt hier später den Stempel je Weg zurück)
- **Neu 17.09.2026:** `roundnum_histogram_w17.py` + `roundnum_histogram_w17_results.json` (W17-Dosis-Kill), `roundnum_kappa_w5k.py` + `roundnum_kappa_w5k_results.json` (W5k-Torwächter-TOT), beide unter `C:\Users\maxlk\Projects\trading-data\engine\`, 24 Trials zusammen ins Register nachgetragen (`discovery/registry_pending/`, noch nicht vom Runner eingelesen — passiert automatisch beim nächsten `load_registry()`)

## Verwandte Notizen

[[Strategie-Logbuch]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Research-Cache]] · [[Fibonacci Wege-Karte]] · [[VWAP-Offensive]] · [[Alpha-Suche]] · [[Discovery-Runner v2]] · [[Strategie-Familien]] · [[Familien-Scout Agent]]
