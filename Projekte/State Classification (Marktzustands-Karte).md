---
tags: [projekt, trading/regime, analyse]
erstellt: 2026-09-28
status: Bericht fertig (Karte v1 für NQ, ES, YM, RTY), Nachlauf GC/CL/NT8-Märkte am PC offen
---

# 🗺️ State Classification (Marktzustands-Karte)

**Auftrag Max (28.09.2026):** Screenshot zu Market Regimes, *„für die gesamte Zeit, die wir backtesten können, eine State Classification durchführen"*. Entscheidungen von Max: **Karte zuerst** (Diagnose, kein Filter), **9 Zustände**, **alle Märkte**, **erst Bericht**. Einordnung und Vorgeschichte: [[Daily Notes/2026-09-28]], Regime-Filter-Bilanz im [[Strategie-Logbuch]] (#136, Regime-Tafel vom 24.09.), Regime-Wette #117 und #143.

## Kurzfassung

- **Die Karte steht.** Jeder Handelstag seit Januar 2017 hat für NQ, ES und YM (RTY ab August 2018) einen von 9 Zuständen, jeweils Richtung × Vola. Das Etikett ist vor der Eröffnung bekannt. GC, CL und die NT8-Märkte fehlen im GitHub-Backup und laufen am PC mit demselben Skript nach.
- **Die Regime-Wette steckt nicht in dieser Karte.** Das Buch verdient ab 2021 in *jedem* häufigen Zustand mehr als vorher. Je nach Rechenweg entstehen 80 bis 90 % des Sprungs innerhalb gleicher Zustände. Als Frühwarnung für die Wette taugt die Karte nicht.
- **Ein Teil davon ist Preisniveau.** NQ stand ab 2021 im Schnitt 2,3-mal so hoch, und ein Micro bewegt entsprechend mehr Dollar. Auf heutiges Preisniveau umgerechnet verdient das Buch ab 2021 immer noch 8-mal so viel je Session wie vorher, auf die Dollar-Vola normiert 3-mal so viel. Woher dieser Rest kommt, kann die Karte nicht trennen. Möglich sind eine echte Änderung der Edge, die Auswahl der Beine auf Daten ab 2021 (#117) oder ein Zustand, den die Karte nicht misst.
- **Die Richtung trennt, bei der Vola ist nichts belegt.** In Bull-Phasen verdient das Buch weniger als seitwärts, 6 $ gegen 20 $ je Session, und das in beiden Epochen. Gegen Bär gilt das nur ab 2021. Der Treiber ist LastHour. Für Momentum und Asia-Dir reicht die Datenmenge nicht, um ein Muster zu belegen oder auszuschließen.
- **Kein belegter Filter-Kandidat.** Kein einzelner Zustand übersteht die Mehrfachtest-Korrektur. Bär/hoch sieht mit +38 $ je Session stark aus, aber zwei Phasen tragen die ganze Summe (Januar bis Juli 2022 und März bis Mai 2025). Das passt zur Bilanz von 0 aus 17 Regime-Filtern. Ungeprüft ist ein Filter über den Sharpe: LastHour verbringt 56 % der Tage im Bull, holt dort aber nur 16 % seines Gewinns. Das wäre ein eigener Gate-v2-Trial.
- **Risiko folgt der Dollar-Vola, nicht dem Etikett.** Bei „Vola hoch" schwankt das Buch rund doppelt so stark wie bei „ruhig", und der Drawdown-Puffer einer Eval ist etwa 4-mal so schnell weg. Ob die Chance, das Ziel vor dem Drawdown zu erreichen, dabei gleich bleibt, ist offen. Sicher ist nur das schnellere Ergebnis. Stärker als die Vola-Stufe wirkt das Preisniveau: Die Tagesschwankung des Buchs stieg von 20 $ (2017) auf 267 $ (2026).
- **Suchrichtung für neue Beine: steigende Märkte.** Im Bull-Drittel verdient das Buch weniger als seitwärts, und Bull ist mit 56 % der Tage der häufigste Zustand. Ein Bein, das in Aufwärtsphasen verdient, würde das Buch am stärksten ergänzen.

## 1. Was die Karte ist

| Achse | Regel | Warum so |
|---|---|---|
| **Vola** (ruhig, normal, hoch) | Mittel der Intraday-Schwankung (5-Min-Renditen, reguläre Handelszeit) der letzten 20 Sessions, als Rang gegen die gesamte bisherige eigene Historie, gedrittelt | Gleiche Bauweise wie der Vola-Filter F1 vom 24.09., nur ohne Nachtdaten, die im Backup fehlen. Die Intraday-Schwankung ist frei von Roll-Sprüngen |
| **Richtung** (Bull, Seitwärts, Bär) | t-Wert der Drift der letzten 60 Sessions: Summe der Tagesrenditen geteilt durch Standardabweichung × √60. Über +0,43 Bull, unter −0,43 Bär | 0,43 teilt einen Markt ohne Drift genau in Drittel (mit echten Renditen nachgeprüft: 33,3 / 33,1 / 33,6 %). Dass NQ zu 56 % Bull ist, liegt an der normalen Aufwärtsdrift eines Index und nicht an einem Sondertrend |
| **Zeitbezug** | Das Etikett für Tag t nutzt nur Daten bis zum Schluss von t−1 | Vor der Eröffnung bekannt, kein Look-ahead, live nutzbar |
| **Rolls** | Die Kalenderspanne je Quartalsroll wird abgezogen. Quelle ist der NT8-Export, bei Widerspruch zum Zins-Carry die 2-Jahres-Rendite | Fund des Quant-Teams: Der NT8-Wert vom 13.03.2020 (−544 Punkte) war eine Preisbewegung und keine Spanne. Er hätte eine Phantom-Rendite von +16,8 % erzeugt. Per Carry ersetzt: NQ 3, ES 3, YM 6 und RTY 1 der Rolls |

Als Gegenprobe gibt es zusätzlich die 4 Zustände nach Goulding/Harvey/Mazzoleni 2023 (Bull, Correction, Bear, Rebound aus 12- und 1-Monats-Momentum, siehe [[Research-Cache]]).

![[regime_zeitachse.png]]

## 2. Die Karte je Markt

| Markt | Etiketten ab | Bull | Seitwärts | Bär | ruhig | normal | hoch | Bär-Phasen ab 10 Tagen |
|---|---|---:|---:|---:|---:|---:|---:|---|
| NQ | 19.01.2017 | 56 % | 30 % | 13 % | 17 % | 38 % | 45 % | 9: 10/18 (10), 11/18 (39), 01/22 (48), 04/22 (24), 06/22 (28), 10/22 (32), 10/23 (12), 03/25 (49), 03/26 (14) |
| ES | 19.01.2017 | 58 % | 28 % | 14 % | 22 % | 36 % | 41 % | 13: 04/18 (16), 10/18 (11), 11/18 (15), 12/18 (29), 03/20 (35), 05/20 (11), 02/22 (12), 03/22 (19), 06/22 (29), 10/22 (26), 09/23 (33), 03/25 (48), 03/26 (15) |
| YM | 19.01.2017 | 55 % | 31 % | 15 % | 18 % | 41 % | 41 % | 9: 04/18 (17), 12/18 (28), 03/20 (53), 03/22 (12), 06/22 (28), 10/23 (29), 02/25 (16), 04/25 (30), 03/26 (20) |
| RTY | 20.08.2018 | 40 % | 37 % | 22 % | 18 % | 41 % | 41 % | 8: 10/18 (71), 02/20 (61), 01/22 (32), 05/22 (16), 06/22 (28), 04/23 (33), 09/23 (38), 02/25 (63) |

- **Leer oder fast leer:** Bär/ruhig gibt es praktisch nicht, weil Bärenmärkte immer volatil sind. Seitwärts/ruhig (NQ 38 Tage) und Bär/normal (35 Tage) sind zu selten für Aussagen. **Effektiv bleiben 6 Zustände.**
- **Die Vola ist schief verteilt** (NQ: ruhig 17 %, hoch 45 %). Das kommt vom Rang gegen die wachsende Historie, denn 2017 war extrem ruhig. Mit einem rollierenden Jahres-Rang ist die Verteilung gleichmäßig, die Ergebnisse unten ändern sich dadurch nicht (Abschnitt 6).
- **Zustände halten an.** Mit 71 bis 94 % Wahrscheinlichkeit ist der nächste Tag im selben Zustand, Episoden dauern im Mittel 4 bis 17 Sessions.
- **Die Märkte ticken verschieden.** ES und NQ haben an 68 % der Tage denselben Zustand, NQ und RTY nur an 47 %. RTY hat mit 22 % die meisten Bär-Tage.

## 3. Das Buch auf der Karte

Buch sind die 3 Live-Beine (Buch 91c972fe), je 1 Micro, netto, in $ je NQ-Session. Tage ohne Trade zählen als 0. Grundlage sind 2.462 Sessions von 19.01.2017 bis 06.08.2026. Das 90-%-Band stammt aus einem Bootstrap über Episoden, also zusammenhängende Phasen eines Zustands. Das ist strenger als über Kalendermonate. Grenzen der Datenbasis: Die Asia-Dir-Zellen sind ungeprüft übernommen, weil die 24h-Daten fehlen. Die Kursdaten reichen bis 10.08.2026, die Buch-Zellen bis 06.08.2026.

![[regime_buch_je_zustand.png]]

| Zustand | Tage | Episoden | Buch $/Session | 90-%-Band (Episoden) | Momentum | LastHour | Asia-Dir | Schwankung (SD) |
|---|---:|---:|---:|---|---:|---:|---:|---:|
| Bull/ruhig | 391 | 14 | **+5,4** | −0,3 bis 16,0 | +3,1 | +1,8 | +0,5 | 87 |
| Bull/normal | 645 | 18 | **+11,5** | 6,6 bis 16,1 | +4,2 | +3,3 | +4,0 | 100 |
| Bull/hoch | 354 | 23 | **−2,2** | −9,5 bis 8,3 | −2,3 | −0,8 | +0,9 | 148 |
| Seitwärts/ruhig ⚠️ zu selten | 38 | 4 | **−8,1** |  | −5,5 | +0,5 | −3,2 | 48 |
| Seitwärts/normal | 258 | 20 | **+21,7** | 9,7 bis 34,5 | +13,1 | +3,6 | +5,0 | 133 |
| Seitwärts/hoch | 447 | 23 | **+21,6** | 13,3 bis 31,5 | +3,8 | +9,3 | +8,6 | 133 |
| Bär/normal ⚠️ zu selten | 35 | 5 | **+20,2** |  | −4,0 | +20,3 | +3,9 | 109 |
| Bär/hoch | 294 | 11 | **+38,0** | −2,7 bis 62,3 | +10,9 | +25,9 | +1,1 | 253 |
| Bär/ruhig | 0 | 0 | keine Tage | | | | | |

**Nach Richtung zusammengefasst:**

| Richtung | Tage | Buch $/Session | 90-%-Band (Episoden) | Momentum | LastHour | Asia-Dir |
|---|---:|---:|---|---:|---:|---:|
| Bull | 1390 | **+6,3** | 3,6 bis 9,5 | +2,2 | +1,8 | +2,2 |
| Seitwärts | 743 | **+20,1** | 13,5 bis 27,6 | +6,5 | +6,9 | +6,7 |
| Bär | 329 | **+36,1** | −0,6 bis 58,2 | +9,4 | +25,3 | +1,4 |

**Trennt die Karte das Buch überhaupt?** Geprüft wurde gegen zeitlich verschobene Etiketten, mit Welch-Statistik. Die einfache Variante war bei Zuständen mit großer Streuung zu großzügig: Im Größen-Check verwarf sie in 24 % statt 5 % der Nullfälle. Es gibt drei Nullen, von locker bis streng:

| Test (studentisiert) | ohne Epochen-Kontrolle | Epoche festgehalten | jedes Kalenderjahr zentriert (streng) |
|---|---:|---:|---:|
| Buch nach Richtung | 0,018 | 0,001 | 0,138 |
| Buch nach 9 Zuständen | 0,059 | 0,028 | 0,105 |
| Buch nach Vola | 0,109 | 0,121 | 0,344 |
| LastHour nach Richtung | 0,035 | 0,016 | 0,189 |
| LastHour nach Vola | 0,136 | 0,128 | 0,607 |
| Momentum nach Richtung | 0,335 | 0,340 | 0,834 |
| Asia-Dir nach Richtung | 0,210 | 0,199 | 0,280 |

- **Die Richtung trennt.** Global liegt p bei 0,02, bei festgehaltener Epoche bei 0,001. Nur diese zweite Variante übersteht auch die Holm-Korrektur über 12 Globaltests (p 0,017). Die strengste Null, bei der jedes Kalenderjahr einzeln zentriert wird, lässt es nicht mehr durch (p 0,14). Sie nimmt aber auch jeden Effekt mit raus, der ganze Jahre betrifft.
- **Eine Vola-Trennung ist nicht belegt** (p 0,11 bis 0,34), bei keinem Bein. Das heißt nicht „gleich“: Die Mittel liegen bei 4,2 $ (ruhig), 14,6 $ (normal) und 18,3 $ (hoch) je Session.
- **Die 9 Zustände zusammen** trennen nur knapp (p 0,03 bis 0,10). Kein einzelner Zustand übersteht die Mehrfachtest-Korrektur. Die Richtungsachse trägt alles.
- **Gegenprobe Goulding:** gleiche Reihenfolge (Bull 9 $ < Correction 21 $ ≈ Rebound 22 $ < Bear 30 $ je Session), mit 4 Zuständen aber nicht signifikant (p 0,22).

**Stabil in beiden Epochen ist nur eins: Bull liegt unter Seitwärts.** Gegen Bär gilt das erst ab 2021, vor 2021 lag Bär sogar darunter, allerdings auf nur 79 Tagen.

| Epoche | Bull | Seitwärts | Bär | Seitwärts minus Bull | Bär minus Bull |
|---|---:|---:|---:|---|---|
| 2017 bis 2020 | −0,4 $ (655 Tage) | +9,3 $ (285) | −13,0 $ (79) | **+9,7 [1,1; 20,8]** | −12,6 [−84,0; 44,8] |
| 2021 bis 2026 | +12,3 $ (735) | +26,9 $ (458) | +51,6 $ (250) | **+14,6 [1,4; 28,0]** | +39,3 [8,8; 68,8] |

Ob sich das restliche Profil zwischen den Epochen verschiebt, kann die Stichprobe nicht entscheiden. Der Interaktionstest Epoche × Zustand liegt bei p 0,4, die kleinste erkennbare Interaktion wäre 27 bis 106 $ je Session groß. Die Rangkorrelation der Zustände vor und ab 2021 (0,09) hängt an 11 Bär/hoch-Tagen im März 2020 (−2.419 $), ohne sie liegt sie bei 0,94.

**Je Bein:**
- **LastHour** trägt die Richtungs-Trennung: +1,8 $ je Session im Bull, +6,9 $ seitwärts, +25,3 $ im Bär. Das passt zu Gao/Han/Li/Zhou 2018 (Intraday-Momentum ist an volatilen Tagen und in Rezessionen stärker, [[Research-Cache]]). Die Bär-Stärke ist aber ein Befund ab 2021. Eine Abhängigkeit von der Vola ist nicht belegt. LastHour verbringt 56 % der Tage im Bull und holt dort 16 % seines Gewinns (Tages-Sharpe 0,03 gegen 0,09 seitwärts und 0,15 im Bär).
- **Momentum** und **Asia-Dir**: kein belastbares Trennsignal. Bei dieser Datenmenge ist das unentscheidbar und heißt nicht „gleich": Die kleinste erkennbare Differenz liegt bei 14 bis 20 $ je Session, die Bein-Mittel bei 3,5 bis 6,5 $.

**Buch je Jahr** (zum Vergleich mit der Zeitachse):

| Jahr | Buch | Momentum | LastHour | Asia-Dir | Schwankung (SD) | häufigster NQ-Zustand |
|---|---:|---:|---:|---:|---:|---|
| 2017 (ab 19.01.) | +129 | +7 | −54 | +176 | 20 | Bull/ruhig (61 %) |
| 2018 | +1.052 | −62 | +1.369 | −256 | 55 | Seitwärts/hoch (23 %) |
| 2019 | +820 | +668 | −202 | +354 | 48 | Seitwärts/hoch (31 %) |
| 2020 | −665 | −672 | +1.078 | −1.071 | 147 | Bull/hoch (44 %) |
| 2021 | +5.816 | +1.510 | +1.798 | +2.508 | 104 | Bull/normal (44 %) |
| 2022 | +11.689 | +4.355 | +5.797 | +1.537 | 213 | Bär/hoch (55 %) |
| 2023 | +2.265 | +42 | +1.923 | +301 | 98 | Bull/normal (45 %) |
| 2024 | +3.398 | +2.331 | −660 | +1.727 | 128 | Bull/normal (46 %) |
| 2025 | +6.087 | +728 | +4.835 | +524 | 194 | Bull/ruhig (28 %) |
| 2026 (bis 06.08.) | +4.987 | +2.141 | +100 | +2.746 | 267 | Seitwärts/normal (25 %) |

## 4. Die Regime-Wette (#117, #143)

Seit #117 wissen wir, dass das Buch fast nur ab 2021 verdient, hier 1,3 $ je Session vorher und 23,7 $ ab 2021. Die Frage an die Karte war: Ist „ab 2021" ein messbarer Marktzustand, den man live erkennen und als Frühwarnung nutzen kann?

![[regime_wette_epochen.png]]

- **Nicht in dieser Karte.** Der Sprung von +22,4 $ je Session [14,2; 30,7] zerlegt sich symmetrisch so:
  - **+2,0 $ durch einen anderen Zustands-Mix** [−2,9; 6,8]
  - **+19,9 $ innerhalb gleicher Zustände** [10,6; 30,4]
  - Das sind rund 90 % innerhalb (Band 64 bis 111 % mit Monats-Clustern, 72 bis 136 % mit Quartals-Clustern). Nimmt man die Zustände ab 2021 als Referenz, sind es 80 %. Im Punktschätzer erklärt der Mix nirgends mehr als ein Fünftel, am Bandende gut ein Drittel.
- **Das Preisniveau als Teil der Erklärung.** NQ stand vor 2021 im Mittel bei 7.700 und ab 2021 bei 17.800. Auf heutiges Preisniveau umgerechnet verdiente das Buch vorher 5,4 $ und ab 2021 44,0 $ je Session. Das Preisniveau erklärt also den Faktor 2,3 aus dem Faktor 18. Übrig bleibt ein Faktor von etwa 8, auf die Dollar-Vola normiert etwa 3. Auch dieser Rest liegt zu rund 90 % innerhalb gleicher Zustände. Was er ist, trennt die Karte nicht. Möglich sind eine echte Änderung der Edge, die Auswahl der Beine auf Daten, in denen die Jahre ab 2021 dominieren (#117: „genau dieses Regime hat die Beine hervorgebracht“), oder ein ungemessener Zustand.
- **Die Gegenproben des Verdict-Auditors kippen das Urteil nicht.** Anteil innerhalb gleicher Zustände: mit Goulding-Zuständen 93 % [65; 103], mit absoluter statt Rang-Vola 88 % [61; 109], auf Dollar-Vola normiert 88 % [48; 137], mit einem Trenndatum irgendwo zwischen 2019 und 2022 überall 77 bis 96 %.
- **Was das für die Wette heißt:** Die Karte kann nicht anzeigen, wann die Wette endet. Es bleibt bei #143, warnen kann nur das Live-Ergebnis selbst (`live-reconciler`).
- **Reichweite:** Geprüft sind genau diese Achsen, also Richtung aus 20 bis 120 Tagen Drift und Vola als Intraday-Schwankung. Ein anderer Zustand (Makro, Zinsen, Optionsmarkt und 0DTE, Marktstruktur) könnte die Wette trotzdem erklären. Das ist ungemessen und nicht widerlegt. Bei LastHour allein erklärt der Richtungs-Mix einen kleinen, belegten Teil: +1,9 von 7,4 $ (Band 0,1 bis 4,4).

## 5. Risiko: wo das Buch gemeinsam verliert

| Vola-Stufe | Schwankung je Session | 5-%-schlechtester Tag | Tages-Sharpe |
|---|---:|---:|---:|
| ruhig | 84 $ | −84 $ | 0,05 |
| normal | 110 $ | −106 $ | 0,13 |
| hoch | 178 $ | −158 $ | 0,10 |

- **Das ist Mechanik.** Die Stops der Beine wachsen mit der Vola, die Kontraktzahl bleibt fest. Die Dollar-Schwankung folgt deshalb der Dollar-Vola eines Micros, also Vola × Preisniveau. Hoch zu ruhig ergibt Faktor 2,1 (Band 1,5 bis 3,4). Vor 2021 war es Faktor 3,6, ab 2021 Faktor 1,8.
- **Was das für eine Eval heißt** (First-Passage, Quant-Mathematiker): Die Zeit bis zum Trailing-Drawdown fällt mit dem Quadrat der Schwankung. Bei „hoch" ist der Puffer etwa **4-mal so schnell** weg wie bei „ruhig", ab 2021 etwa 3-mal. Ob die Chance, +3.000 $ vor −2.000 $ zu erreichen, gleich bleibt, ist offen: Steigt die Drift mit der Vola mit, sind es 0,69 zu 0,68, bei gleicher Drift 1,00 zu 0,59. Sicher ist nur das **schnellere Ergebnis**.
- **Wichtiger als die Vola-Stufe ist das Preisniveau.** Die Tagesschwankung des Buchs stieg von 20 $ (2017) auf 267 $ (2026). Ein ruhiger Tag ab 2021 hat mehr Dollar-Vola (247 $) als ein hoch-volatiler Tag vor 2021 (200 $).
- **Die schlechtesten 5 % der Tage** (≤ −124 $) liegen häufiger in Bär/hoch und Bull/hoch. Das ist durch die Mechanik erklärbar: Rechnet man die Dollar-Vola vor der Eröffnung heraus, ist kein Klumpen mehr nachweisbar (p 0,57 bis 0,81). Für den Trailing-Drawdown zählt die Dollar-Vola, nicht das Etikett.
- **Die drei tiefsten Drawdowns** (je Micro-Satz):
  1. 04.03. bis 25.03.2020: −3.338 $, zu 56 % Bär/hoch, 38 % Seitwärts/hoch und 6 % Bull/hoch (Corona).
  2. 11.06. bis 28.07.2026: −2.718 $, zu 85 % Bull/hoch. Das ist ein Einzelfall, Bull/hoch ist als Zustand nicht von null unterscheidbar (−2,2 $, Band −9,5 bis 8,3).
  3. 04.12.2024 bis 30.01.2025: −1.394 $, gemischte Bull-Zustände.

## 6. Was trägt und was nicht

| Aussage | Urteil | Reichweite |
|---|---|---|
| Die Regime-Wette ist kein Zustand dieser Karte | **trägt mit Einschränkung**: 80 bis 90 % des Sprungs innerhalb gleicher Zustände, der Mix erklärt im Punktschätzer höchstens ein Fünftel, am Bandende gut ein Drittel | nur Richtung und RTH-Vola, NQ, 2017 bis 2026. Externe Achsen (VIX, Leitzins, Optionsmarkt) und die Selektion der Beine sind ungemessen |
| Die Richtung trennt das Buch, Bull liegt unter Seitwärts | **trägt mit Einschränkung**: in beiden Epochen, p 0,02 global und 0,001 bei festgehaltener Epoche (nur diese übersteht Holm). Bei zentriertem Kalenderjahr nicht mehr (0,14). Gegen Bär gilt es erst ab 2021 | Buch 91c972fe, Treiber LastHour |
| Die Vola-Stufe trennt den Ertrag | **unentscheidbar**: nicht belegt (p 0,11 bis 0,34), aber auch nicht gleich (4,2 / 14,6 / 18,3 $) | |
| Ein einzelner Zustand ist besonders gut oder schlecht | **trägt nicht**: Kein Zustand übersteht die Mehrfachtest-Korrektur. Bär/hoch (+38 $) hängt an zwei Episoden, Band über Episoden −2,7 bis 62,3 | |
| Das Zustandsprofil ist über die Epochen stabil | **unentscheidbar** (Interaktion p 0,4, kleinste erkennbare Interaktion 27 bis 106 $) | |
| Filter nach Zustand | **kein belegter Kandidat**. Ungeprüft ist ein Sharpe-Filter „LastHour im Bull aus“ (56 % der Tage, 16 % des Gewinns) | Jede Filteridee daraus liefe als Trial durch Gate v2, mit Auswahl über alle angeschauten Zustände. Referenzklasse 0 aus 17 |
| Schwankung und schlechteste Tage hängen an der Vola | **trägt**: durch die Dollar-Vola erklärbar, kein Rest nachweisbar | feste Kontrakte, vola-skalierte Stops |
| Momentum und Asia-Dir je Zustand | **unentscheidbar**, nicht „gleich" | kleinste erkennbare Differenz 14 bis 20 $ je Bein |
| Seitwärts/ruhig, Bär/normal, Bär/ruhig | **unentscheidbar** bzw. keine Daten (38, 35, 0 Tage) | zählt nicht als Befund |

**Kleinste erkennbare Differenz je Zustand gegen den Rest** (80 % Power, Episoden-Cluster, Quant-Statistiker): Bull/normal 15 $, Bull/ruhig, Bull/hoch und Seitwärts/hoch 18 bis 19 $, Seitwärts/normal 23 $, Bär/hoch 62 $, Bär/normal 74 bis 98 $. Gemessen an einer sinnvollen Filtergröße von etwa 15 $ je Session ist nur die Bull-Seite gut vermessen.

**Robustheit der Karte** (NQ, Sensitivität, keine Trials):

| Variante (NQ) | gleiche Etiketten | davon Richtung / Vola | Sprung ab 2021 innerhalb gleicher Zustände |
|---|---:|---|---:|
| Richtung 20 Tage | 57 % | 57 % / 100 % | +21,5 $ von +22,4 $ |
| Richtung 120 Tage | 66 % | 66 % / 100 % | +20,6 $ von +22,4 $ |
| Vola-Rang rollierend 250 | 61 % | 100 % / 61 % | +22,4 $ von +22,4 $ |
| ohne Roll-Korrektur | 97 % | 97 % / 100 % | +22,5 $ von +22,4 $ |

Die Richtung hängt stark am Fenster (57 bis 66 % gleiche Etiketten bei 20 oder 120 statt 60 Tagen). Das Hauptergebnis bleibt in jeder Variante gleich: Der Sprung ab 2021 liegt innerhalb gleicher Zustände.

## 7. Nächste Schritte (Entscheidung bei Max)

1. **Nachlauf am PC für alle Märkte:** zuerst `python regime_map.py --markets NQ,ES,YM,RTY,GC,CL,ZN,6E,...`, danach `regime_book.py` und `regime_charts.py`. GC, CL und die NT8-Märkte fehlen im Backup. FDAX braucht ein eigenes Sessionfenster.
2. **Suchrichtung für neue Beine:** Mechanismen, die in steigenden Märkten verdienen. Das wäre ein Auftrag für den nächsten `alpha-scout`-Lauf. Gemeint ist ausdrücklich kein „Bein X nur im Bull handeln" (Filter, 0 aus 17), sondern ein Bein, das im Bull von selbst verdient.
3. **Workbench-Farbband:** den Zustand als Band unter jeder Equity-Kurve zeigen, damit bei jedem Test sichtbar ist, in welchen Phasen er verdient. Das ist UI-Arbeit und braucht vorher `design-guard`.
4. **Offene Frage an das Quant-Team (ungerechnet):** Die Voll-Historie-Spalten in `tempo_plan` (IS, shrink058) ziehen Tage aus 2017 mit 20 $ Schwankung neben Tagen aus 2026 mit 267 $, ohne sie auf das heutige Preisniveau anzupassen. Ob und in welche Richtung das die Zeit bis 50k verzerrt, ist nicht gerechnet.
5. **Engine-Vorschlag des Statistikers:** den studentisierten Verschiebungstest mit Epochen-Schichtung als Ergänzung in `overfit.py` aufnehmen. Vorlage sind `stud_test` und `stud_test_epoch` in `regime_book.py`, gegen die Rechnung des Statistikers abgeglichen. Das ist eine Engine-Änderung und braucht vor jedem Box-Sync den `engine-regression-tester`.
6. **Kipp-Test Selektion** (etwa 30 Minuten, kein Trial): das Auswahlfenster der drei Beine gegen den Bruch 2021 legen. Das klärt, ob der Rest nach Preisniveau Edge oder Auswahl ist.
7. **Karte v2 mit externer Achse** (VIX-Niveau oder Leitzins, vor Eröffnung bekannt), gleiche Zerlegung, etwa ein halber Tag. Das ist die einzige Klasse von Tests, die das Kernurteil noch kippen kann.
8. **Nur falls du Filter willst:** „LastHour im Bull aus“ als ein Gate-v2-Trial mit Placebo.
9. **Logbuch-Eintrag:** Soll der Befund als #177 ins [[Strategie-Logbuch]]? Dann mit Kategorie `empirisch-nichts-gefunden` (Regime-Wette über diese Karte nicht erklärbar), Reichweite wie in Abschnitt 6 und Wiedervorlage bei Karte v2 oder dem PC-Nachlauf. Vorher läuft `logbook-distiller`.

Tickets für 1 bis 8 sind nicht angelegt, weil die Box von der Cloud-Session aus nicht erreichbar ist (`tasks.json` hat die Box als Quelle der Wahrheit).

## 8. Stempel und Dateien

**Stempel:** Buch 91c972fe (3 Live-Beine), Engine-Tageszellen aus `developer/book_cells.json` (Engine-Fingerprint bb9ac564). Momentum und LastHour wurden am 28.09. gegen einen frischen Engine-Lauf geprüft, jeder Tag war identisch. Asia-Dir ist ungeprüft übernommen, weil die 24h-Daten fehlen. Kursdaten: RTH-Cache des GitHub-Backups von trading-data, Stand bis 10.08.2026. Gerechnet in einer Cloud-Session, geprüft von quant-mathematician, quant-statistician und verdict-auditor (28.09.). Deren Korrekturen sind eingearbeitet: Roll-Fund 13.03.2020, studentisierte Tests, Episoden-Bänder, Preisniveau und Dollar-Vola, vorsichtigere Urteile bei Vola, Richtung und Filter. Kein Trial, keine Registrierung, reine Beschreibung.

**Dateien in trading-data** (Branch `claude/relaxed-dirac-kp7xvn`):
- `engine/regime_map.py`: die Karte mit den Etiketten je Markt und Tag. Aufruf siehe Docstring.
- `engine/regime_book.py`: die Buch-Diagnose mit Zuständen, Trenntests, Epochen-Zerlegung und Risiko.
- `engine/regime_charts.py`: die drei Grafiken.
- `engine/regime_map/states_daily.csv`: die Karte selbst (Spalten date, market, state, dir, vol, dir_z, vol_rank, goulding). Für Workbench und tempo_plan über `regime_map.load_states()`.
- `engine/regime_map/book_regime.json`: alle Kennzahlen dieses Berichts.

**Grafiken** in `Anhänge/`: `regime_zeitachse.png`, `regime_buch_je_zustand.png`, `regime_wette_epochen.png`.
