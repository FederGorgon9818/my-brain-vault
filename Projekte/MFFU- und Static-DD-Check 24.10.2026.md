---
date: 2026-10-24
tags: [projekt, prop-firm, mffu, static-drawdown, tempo_plan, recherche]
status: Bericht fertig, Entscheidungen bei Max
---

# 🏦 MFFU- und Static-DD-Check (24.10.2026): bringt MyFundedFutures oder ein Static-Drawdown-Konto die Zeit bis 50k nach vorn?

Auftrag Max 24.10.2026: intensive Recherche zu MyFundedFutures (MFFU), „My-Studios / My-Funded Studios“ und Static-Drawdown-Plänen, Regeln genau prüfen, und ob wir das mit der Box nutzen können, um schneller ans Ziel zu kommen. Session 40bff0bb. Recherche über zwei `research-scout`-Läufe (Cache-Abschnitte siehe unten), Rechnung auf der Box, gegengelesen vom Quant-Team.

Verwandt: [[CFD-Check 23.10.2026]] (gleiche Methode, Vergleichszeilen E8/FFN/FN stammen von dort), [[Kaufvorlage Kaufrunde 06.11.2026]], [[Firm-Regeln je Konto]], [[MFFU 50k Pläne (Regeln + Wahl)]] (Stand 04.08., überholt), [[Research-Cache]].

> ## 🔁 Zweite Runde (24.10. nachmittags, Auftrag Max: Rapid EOD 50K komplett nachrechnen, Kriterien prüfen, offen Gebliebenes per Mail klären)
>
> **Korrektur zur ersten Runde:** die „−16,7 Monate“ unten galten für ein MFFU-Konto **zusätzlich** zur heutigen Flotte, mit eigenem Budget und eigenem Deckel obendrauf. Entscheidend ist aber, was MFFU **im echten Kaufplan** bringt (Kaufvorlage: ein Kauf je Monat, Deckel 2.500 $ für alles, BOS-Regel). Dort sind es **2 bis 5 Monate**, nicht 16.
>
> | Regime | E8 + FFN (Kaufvorlage) | + MFFU Rapid EOD in der Rotation | Vorsprung |
> |---|---|---|---|
> | alle Jahre | 55,9 Monate Median, 50k in 5 J: 61,5 % | 49,6 Monate, 72,5 % | **−5,3 ± 0,4 Monate** (9 %), in 84 % der Welten schneller |
> | letzte 3 Jahre | 35,1 | 32,6 | −2,0 ± 0,2 |
> | Edge x 0,58 | Mittel bis Kappe 100,1, 50k in 10 J: 51,2 % | 97,0, 55,5 % | −3,1 ± 0,6 |
> | nur 2016 bis 2020 | kein Ziel in 10 J | kein Ziel | 0 (das Buch hatte damals kaum Edge) |
> | Nulldrift | 0 % | 0 % | |
>
> Auslage p90 sogar etwas niedriger (2.146 statt 2.210 $). Laut Statistiker belastbar in jedem Regime mit Edge (z ≥ 5, Bonferroni bestanden), die Größe aber unsicher. Details Abschnitt 10.
>
> **Der Vorteil hängt komplett am Keep-alive bei MFFU (quant-mathematician):** MFFU schließt ein Konto nach 7 Kalendertagen ohne Trade, unser Buch hat rund 2 solche Lücken im Jahr. Bei E8 ist ein Keep-alive-Trade erlaubt (jeder geschlossene Trade zählt, heute Alarm plus Hand-Trade). Bei MFFU ist er **nicht eindeutig erlaubt** (Support 29.09.: „your strategy must remain consistent“). Rechnet man die Inaktivität deshalb nur bei MFFU, ist der Kaufplan **mit** MFFU **4,75 ± 0,40 Monate langsamer** als ohne, weil ein MFFU-Konto dann fast nie bis zur Auszahlung kommt (Eval-Pass 23 % statt 76 %, Netto je Konto 779 statt 13.606 $). **Also: Rapid EOD 50K nur kaufen, wenn MFFU den Keep-alive-Trade schriftlich erlaubt.** Das ist Frage 1 der Mail. Fehlt er überall (auch bei E8), fällt jeder Kaufplan von 58 auf rund 105 Monate, das wiegt zehnmal mehr als die Frage MFFU ja oder nein.
>
> **Kriterien:** schriftlich geklärt aus den Mails vom 28./29.09. (lagen im Postfach maxlkho4): Automation in allen Stufen, VPS ohne IP-Beschränkung, unbeaufsichtigt erlaubt („provided it can be intervened“), NT8 über Tradovate, Copy auf eigenen Konten, Deutschland, CLUB-Rabatt mehrfach. **Offen:** dieselbe Strategie bei anderen Firmen (zweimal gefragt, nie beantwortet), Keep-alive-Trade, Hedging gegenläufiger Beine, T1-Regel bei Rapid EOD Funded, Live-Wechsel. Nachfrage-Mail liegt als Entwurf in maxlkho4 und geht erst mit Max' OK raus. Kriterien-Tabelle Abschnitt 11.

> ## 🧭 Kurzfassung für Max (erste Runde)
>
> 1. **„My-Funded Studios“ gibt es wirklich: MyFundedStudio ist MFFUs Static-Drawdown-Linie.** Winzige Konten (5k, 10k, 20k, MLL 250 bis 1.000 $ static, 75 bis 280 $), **nur auf MFFUs eigener Plattform Hyperprop, kein NinjaTrader**. Für die Box heute nicht nutzbar. Selbst wenn NT8 käme, wäre Studio 20k nur ungefähr so gut wie ein E8 150K, bei viel mehr Käufen (rund 14 bis 19 in 10 Jahren).
> 2. **Die normalen MFFU-Pläne (Builder, Rapid EOD, Pro) sind für uns rechnerisch das beste Zusatzkonto, das wir bisher gefunden haben.** Ein zusätzliches **Rapid EOD 50K (135 $) spart rund 16,7 Monate** bis 50k, Pro 50K 14,2, Builder 50K 12,2 (vorsichtig gerechnet: Konto endet beim Live-Wechsel, Auszahlung in großen Beträgen). Zum Vergleich: E8 Futures 100K **10,1**, E8 150K 8,0, FFN 150K 7,8. Pro Euro am besten ist **Builder 50K (92 $)**, absolut am schnellsten **Rapid EOD 50K** oder Pro 50K (die Reihenfolge innerhalb von MFFU ist nicht robust). **Mit geschrumpfter Edge (x 0,58)** bleibt es ein klares Ja: MFFU −5,6 bis −7,2 Monate gegen E8 100K −3,9 und FFN −3,2, gepaart in jedem Fall schneller (quant-statistician, Holm-p unter 0,001).
> 2a. **Bedingung für jede dieser Zahlen: ein Keep-alive-Trade.** MFFU schließt ein Konto nach 7 Kalendertagen ohne Trade (wie E8). Unser Buch hat rund 2 solche Lücken im Jahr. Ohne Keep-alive fällt Rapid EOD von −16,4 auf **−1,3 Monate** (quant-mathematician). Das ist dieselbe Lage wie beim E8 50k heute (Inaktivitätsregel im RiskGuard mit Alarm, dazu Hand-Trade von Max; der automatische Mini-Trade ist im RiskGuard als Option gebaut, steht aber standardmäßig auf aus), nur muss es vor einem MFFU-Kauf verlässlich laufen, am besten automatisch.
> 3. **Aber: die Rechnung sagt nur, dass es sich lohnen würde. Ob wir dürfen, ist offen.** MFFU erwähnt VPS und unbeaufsichtigten Betrieb in keinem Text, die Copy-Regeln widersprechen sich („coordinated trading“-Sperren in Beschwerden), Hedging ist „of any kind“ verboten. Vor einem Kauf brauchen wir eine **schriftliche Freigabe** wie bei FFN (Fragenliste Abschnitt 7).
> 4. **Static-DD bei anderen Firmen:** fast alles fällt an Algo- oder VPS-Verbot (Topstep, Tradeify, Elite, Phidias, FXIFY, Traders Launch). Übrig bleiben **DayTraders Static** (Bots, VPS und Copier schriftlich erlaubt, NT8 nicht offiziell) und **BluSky Static** (NT8 ja, Bots/VPS ungeklärt). **BluSky bringt nichts** (Monatsabo plus zwei Phasen bei 1.000 $ Static). **DayTraders Static 150K bringt rund 13,5 Monate, aber nur mit Einmalpreis**, mit Monatsabo ist es wertlos. Preismodell und NT8 müssen schriftlich geklärt werden.
> 5. **Lehre 17 (#073) hält bei der Ratio, greift aber zu kurz:** alle Static-Pläne haben ein schlechteres Verhältnis DD/(Target+DD) als 40 % (20,6 bis 33,3 %). Trotzdem kann ein Static-Konto schnell sein, wenn die Funded-Phase großzügig ist (DayTraders: 100 % Split, Floor bleibt fest, nach dem ersten Payout 3.750 $ Puffer). Für Zeit bis 50k zählt die Funded-Phase mehr als die Eval-Ratio.
> 6. **Empfehlung:** MFFU-Support schriftlich anfragen (Fragenliste Abschnitt 7). Kommt eine saubere Freigabe, ist ein MFFU-Konto die stärkste nächste Kaufoption, noch vor E8 100K: **Rapid EOD 50K**, wenn die T1-News-Sperre (AP335) bis dahin steht, sonst **Builder 50K** (News im Funded erlaubt, billigster Plan). Vorher muss der Keep-alive gegen die 7-Tage-Inaktivität verlässlich laufen. Kauf nur mit Blick auf die BOS-Reserve und nach den Bedingungen der Kaufvorlage (AP238, AP381).

---

## 1. Was „My-Funded Studios“ ist

- **MyFundedStudio** = Static-Drawdown-Linie von MFFU (Seitentitel „Static Drawdown Prop Firm Plans | MyFundedStudio“, myfundedfutures.com/studio). Limitierte Pläne mit Tageskontingent („Sold out for today“ am 24.10.).
- Pläne: **#001** 10k, 140 $, Target 1.000, MLL 500 static, 10 Micros. **#002** 20k, 280 $, Target 2.000, MLL 1.000 static, 20 Micros. **#003** 5k, 75 $, Target 500, MLL 250 static (seit 14.10.2026). Kein DLL, keine Consistency, keine Mindesttage, Payout jederzeit ab 250 $ (100 $ bei #003), kein Puffer, 80/20, Live nach 5 Payouts oder 5.000/10.000 $ angefordert. Nur **ein** aktives Studio-Konto.
- **Plattform nur Hyperprop** („More platforms coming soon“), keine Aussage zu NT8, API, Automation. Damit für unseren NinjaScript-Bot heute ausgeschlossen.
- Nicht verwechseln: **MyFunded Perpetuals** (Perps, „Elite“, ebenfalls Static) ist eine eigene Firma, nicht MFFU.

## 2. MFFU-Pläne heute (Stand 24.10.2026, Preise mit Code CLUB, einmalig, 0 $ Aktivierung)

| Plan | Preis | Eval | Funded | Payout | Split |
|---|---|---|---|---|---|
| **Builder 50K** | 92 $ (Liste 153) | 3.000 / 2.000 EOD, weicher DLL 1.000, keine Consistency, 1 Tag, 4/40 | EOD 2.000, Lock +100, Consistency 50 % nur beim Payout | ab 500 über Puffer 2.100, alle 48 h, max. 2.000 je Request, 2 Handelstage je Zyklus, 5 Payouts bis Live, **News erlaubt** | 80/20 |
| **Rapid EOD 50K** | 135 $ (225) | 3.000 / 2.000 EOD, Consistency 30 %, 4 Tage, 3/30 | EOD 2.000, Lock +100, keine Consistency, max. 3 Funded | erste ab 2.100 Gewinn, dann je 500 Netto, täglich, kein Cap, **T1-News im Funded verboten** | 90/10 |
| **Pro 50K** | 159 $ (265) | 3.000 / 2.000 EOD, Consistency 50 %, 2 Tage, 3/30 | EOD, nach 1. Payout static bei +100, **Kontrakte „3/3“ (evtl. nur 3 Micros)** | alle 14 Tage, Min 1.000, Puffer 2.100, Live nach 3 Payouts, T1 im Funded verboten | 80/20 |
| Pro 150K | Preis unbelegt (Aug. Liste 477 $) | 9.000 / 4.500 EOD | wie Pro 50K, Puffer 4.600 | wie Pro 50K | 80/20 |
| Rapid 50K–150K | 125 $ (209) für 50K | wie Rapid EOD, aber 50 % Consistency, 2 Tage | **Intraday-Trailing** im Funded | täglich | 90/10 |
| Studio #001–#003 | 75–280 $ | siehe Abschnitt 1 | Static | jederzeit | 80/20 |

Nicht mehr kaufbar: Core, Scale, (Flex unklar). Rapid (Intraday-Trailing im Funded) habe ich nicht gerechnet: die Engine-Zellen kennen den Tageshöchststand nicht, und Intraday-Trailing ist für uns nach Lehre 18 ohnehin das schlechteste Modell.

## 3. MFFU-Regeln gegen unsere Box

> [!note] Stand erste Runde
> Überholt bei VPS und unbeaufsichtigtem Betrieb: beides ist seit den Support-Mails vom 28./29.09. schriftlich erlaubt (lagen im Postfach maxlkho4, beim ersten Durchgang übersehen). Aktueller Stand: Abschnitt 11.

| Regel | Ampel | Kern |
|---|---|---|
| Eigene Automation | grün | „automated trading strategies tailored to their own specific settings“, solange keine Sim-Fills ausgenutzt werden. HFT verboten, ohne Zahl. |
| **Unbeaufsichtigt** | gelb | im Primärtext nicht geregelt, Drittquellen widersprechen sich |
| **VPS, Rechenzentrums-IP** | gelb | in keinem Help-Artikel und nicht in den Terms. Das „Simulated Trader Agreement“ (Terms §29) ist nicht öffentlich. Chat-Antwort aus dem August („VPS ok“) ist nicht schriftlich belegt. |
| NT8 | gelb | Login über „My NinjaTrader“ (Simulation), Tradovate als Broker. Rithmic nicht genannt, Lizenz/Datengebühren nicht geregelt. |
| **Copy / dieselben Signale** | gelb | „allows copy trading across all account types“ gegen „not permitted to copy trade one another“ und Terms §23.1.3.3 („hedge, mirror, copy, or coordinate“ bei unfairem Vorteil). Andere Firmen nicht geregelt. Beschwerden über Sperren wegen „coordinated trading“. |
| **Hedging** | gelb/rot | „prohibits hedging of any kind“: long und short im selben Underlying gleichzeitig. Wir handeln nur MNQ (plus M2K), die Positionen eines Kontos netten am Broker, gegenläufige Beine heben sich also auf. Ob MFFU das als Hedge wertet, ist offen. |
| Kontolimits | grün | max. 10 Evals, bis 5 Sim Funded (Rapid EOD max. 3, **Builder 50K max. 1**, Studio 1) |
| Flat-Zeit | grün | Auto-Close 16:10 ET, wir sind 15:55 flat |
| News | grün (Builder, alle Evals), gelb (Rapid EOD/Pro Funded) | T1 (FOMC, Minutes, NFP, CPI): 2 Min vor/nach keine Position und keine Order. Bräuchte die T1-Sperre wie bei FFN (AP335). |
| HFT, Haltedauer | gelb | keine Zahl, keine Mindesthaltedauer. PB3 (11 % Stop-outs in derselben Minute) ist Auslegungsfrage. |
| Inaktivität | grün | 1 Trade je 7 Kalendertage (wie E8), gleicher Alarm |
| Positionsgröße | gelb | Terms §12.4: „substantially larger position sizes than typical“ = Verstoß. Relevant für ein späteres k2. |
| Deutschland | grün | nicht auf der Sperrliste |

## 4. Static-Drawdown am Markt (ohne MFFU)

| Firma / Plan | Target / Static-DD | DD/(T+DD) | Algo/VPS/NT8 | Ergebnis |
|---|---|---|---|---|
| **DayTraders Static 50K / 150K** | 3.750 / 1.000 bzw. 6.750 / 1.750 | 21,1 % / 20,6 % | Bots, VPS, Copier (auch andere Firmen) **schriftlich erlaubt**; NT8 „not officially supported“, geht über Rithmic | **Kandidat**, Preismodell (Monat oder einmalig) und NT8 klären |
| **BluSky Propel 150K Static** | 3.000 + Buffer-Phase 2.000 / 1.000 | 25,0 % | NT8 über Rithmic dokumentiert; Bots nur im alten Blog, VPS nicht geregelt | gerechnet: bringt nichts |
| Topstep 50K Static | 4.000 / 2.000, DLL 1.000 | 33,3 % | **VPS verboten**, nur TopstepX | raus |
| Tradeify Level Up | 1.000 static je Level | | Mehr-Firmen-Verbot, ausverkauft | raus |
| Elite Trader Funding Static | 4.000 / 2.000 | 33,3 % | nur genehmigte Kopierer | raus |
| Phidias Express to Live | 2.500 / 650 | 20,6 % | Automation verboten | raus |
| Traders Launch, FXIFY, Uprofit, Phoenix | | | kein NT8 oder EA-Verbot | raus |
| TradeDay Static, Apex Static | | | nicht mehr kaufbar | |

## 5. Zeit bis 50k mit einem Zusatzkonto

**Methode (wie [[CFD-Check 23.10.2026]] Abschnitt 9):** Flotte = die 5 echten Konten (Stand 16.10.), `tempo_plan.simulate_fleet_calendar` mit den Einstellungen von `weekend_check` (Kalender-Modus, RiskGuard-Tagesstopp, Lane E8 150k k1, Budget 600 $/Monat, Deckel 2.500 $, Seed 101), 600 Welten, Nulldrift 300. Das Zusatzkonto läuft als Ein-Lane-Flotte (genau 1 Konto, Kauf am Tag 0, Nachkauf nach Bust, eigener Deckel 1.000 $) **auf denselben Master-Pfaden**, Netto je Welt zur Flotte addiert, also gepaart. Buch: die 4 NQ-Beine (PB3, LastHour, Asia, OpenDrive), k1, 32,85 $/Tag, Tages-Std 231,7 $. MFFU als eigener Käfig in der Engine-Logik (Selbsttest: Eval bei E8-Regeln bitgleich zum E8-Käfig), DayTraders/BluSky über einen zweiten, unabhängigen Einzelkonto-Simulator (kann Monatsabos). **Gegenprobe:** MFFU Rapid EOD 50K in beiden Wegen gerechnet, Ergebnis identisch (−16,37 ± 0,39).

**Varianten für MFFU**, weil der Live-Wechsel nach Ermessen läuft:
- **cont:** Konto zahlt nach dem Live-Wechsel mit denselben Regeln weiter (freundlich).
- **end:** Konto endet beim Live-Wechsel (Builder nach 5, Pro nach 3, Rapid EOD angenommen nach 5 Payouts), Rest-Saldo verfällt, Auszahlung schon ab 500 $. Laut Mathematiker ein Politik-Artefakt (die wenigen Payouts bis Live gehen für Kleinbeträge drauf), nur zur Einordnung.
- **endg2 (maßgeblich):** wie end, aber Auszahlung erst ab 4.000 $ über dem Puffer (Rapid EOD), 5.000 $ (Pro 50K/150K), Builder 2.000 $ (Cap je Request). Das ist die vorsichtige Variante mit vernünftiger Auszahlungspolitik. Bei Rapid EOD liegt sie gleichauf mit cont, der Live-Wechsel ist dann fast egal.
- endg: Zwischenstufe mit 2.000 $ (Builder ist dort schon endgültig).

Flotte ohne Zusatzkonto: **Median 78,8 Monate**, Erreichung 93,3 %, Auslage p90 1.332 $, Nulldrift 0,0 %. Δ = mit minus ohne, negativ = schneller.

| Zusatzkonto | Preis $ | Median mit (M) | Δ Mittel ± SE | schneller in % der Welten | Nulldrift | Auslage p90 mit | Monate je 100 $ Auslage |
|---|---|---|---|---|---|---|---|
| **MFFU Rapid EOD 50K** cont / **endg2** / endg / end | 135 | 61,0 / 61,0 / 65,0 / 70,2 | −16,4 / **−16,7** / −13,2 / −8,5 | 98,7 / 99,0 / 97,8 / 93,3 | 0,0 % | 1.602 | 7,9 / 7,8 / 6,2 / 4,1 |
| **MFFU Pro 50K** cont / **endg2** / endg / end | 159 | 61,8 / 64,4 / 66,8 / 70,8 | −16,3 / **−14,2** / −11,6 / −8,5 | 98,7 / 98,8 / 97,2 / 93,2 | 0,0 % | 1.650 | 6,9 / 5,9 / 4,8 / 3,6 |
| **MFFU Builder 50K** cont / **endg** / end | 92 | 62,3 / 66,5 / 66,7 | −15,9 / **−12,2** / −11,5 | 99,0 / 98,2 / 97,5 | 0,0 % | 1.516 | 11,7 / **8,9** / 8,5 |
| MFFU Pro 150K cont / **endg2** / endg / end | 286 (unbelegt) | 65,2 / 66,5 / 71,2 / 75,3 | −13,3 / **−11,6** / −7,7 / −4,1 | 98,2 / 98,0 / 90,3 / 66,8 | 0,0 % | 1.618 | 4,6 / 4,0 / 2,6 / 1,4 |
| *MFFU Rapid EOD 50K cont **ohne Keep-alive** (Inaktivität als Bruch, quant-mathematician)* | 135 | | *−1,3* (+15,1 ± 0,4 gegen cont) | | | | |
| MFFU Studio 20k cont / end (kein NT8) | 280 | 65,4 / 70,6 | −12,3 / −7,7 | 92,7 / 87,7 | 0,0 % | 1.978 / 2.053 | 2,9 / 1,8 |
| MFFU Studio 10k cont / end (kein NT8) | 140 | 72,8 / 73,8 | −5,4 / −4,7 | 66,8 / 64,0 | 0,0 % | 2.212 | 1,1 / 0,9 |
| DayTraders Static 150K einmalig / monatlich | 405 | 64,4 / 79,8 | **−13,5** / +0,9 | 97,2 / 0,0 | 0,0 % | 2.142 | 2,8 / − |
| DayTraders Static 50K einmalig / monatlich | 205 | 69,3 / 78,8 | −8,8 / +0,2 | 88,7 / 6,2 | 0,0 % | 1.947 / 2.142 | 2,5 / − |
| BluSky Propel 150K Static (Abo) | 170 je Monat | 79,6 | +0,9 | 0,7 | 0,0 % | 2.182 | − |
| *Vergleich 23.10.:* E8 Futures 100K | 260 | 68,3 | −10,1 | 96,0 | 0,0 % | 1.592 | 3,4 |
| E8 Futures 150K | 333 | 70,4 | −8,0 | 90,8 | 0,0 % | 1.665 | 2,3 |
| FFN STEADY 150K | 292,50 | 71,0 | −7,8 | 89,7 | 0,0 % | 1.624 | 2,6 |
| FN Flex 100K | 144,99 | 73,2 | −6,2 | 83,8 | 0,0 % | 1.622 | 3,7 |

Nulldrift bei MFFU nur für `cont` gerechnet (wer dort 0 % hat, hat es in `end` erst recht), bei DayTraders/BluSky für alle Zeilen. Die Fehlerbalken messen nur das Pfadrauschen bei fester Edge, nicht, ob die Edge hält (Abschnitt 6).

**Warum MFFU so weit vorn liegt:** tägliche bzw. 48-h-Auszahlungen ohne Caps (Rapid EOD) oder mit 2.000-$-Cap, kein 5-Gewinntage- oder 35-%-Best-Day-Zwang im Funded wie bei E8, 90 % Split bei Rapid EOD, und ein niedriger Kaufpreis, der nach einem Bust schnell nachgekauft ist (3 bis 8 Käufe in 10 Jahren bei 1.000 $ Deckel). **Warum Studio und BluSky abfallen:** 1.000 $ Static sind nur 4,3 Tagesschwankungen des Buchs, das Konto stirbt oft (Studio 20k rund 14 bis 19 Käufe), und bei BluSky frisst das Monatsabo in der zweiphasigen Eval den Deckel, bevor das Konto funded wird.

## 6. Robustheit und Gegenlesen

### `quant-mathematician`: Käfig und Paarung tragen

- **Kernel geprüft** auf Kunstpfaden (Payout-Takt, Lock bei +100, Intraday-Bruch gegen den Floor vom Vortag, Tagesstopp, Builder-Consistency und Cap, Static-Floor nach Auszahlungen, Rapid-Eval mit 30 % und 4 Tagen): alles wie gewollt. Einhängung in `tempo_plan` wirkt, Achsentage-Umrechnung stimmt (14 Kalendertage = 6 Achsentage).
- **Paarung belegt:** gleiche Ziehung, Achse, TM, Weltenzahl, Engine-Stand seit `out_A` unverändert. Sein eigener Runner liefert meine Basis bitgleich nach. Korrelation Flotte gegen Zusatzkonto je Welt 0,74 bis 0,91 (E8 100K aus `out_B`: 0,80).
- **Puffer:** `keep = 2.100` ist die exakte Lesart der Regel. Abschöpfen bis nahe an den Floor kostet 3,6 bis 7 Monate (Ruin je Zyklus fällt erst ab etwa 3 x 660 $ Puffer). Freiwillig 3.100 $ stehen lassen bringt noch −0,9 Monate.
- **Auszahlungsschwelle in der end-Variante:** mit 500 $ ein Politik-Artefakt, deshalb `endg2` (Rapid EOD 4.000, Pro 5.000) als maßgebliche vorsichtige Zeile.
- **Static gegen Trailing:** Static ist für uns kein eigener Hebel. Was zählt, sind Split und Puffer nach der Auszahlung. Bei Split 0,8 schlägt kein Static-Konto ein Rapid EOD 50K mit freiwilligem Puffer (Obergrenze der Rate ist Split x Drift). Bei Split 0,9 bräuchte ein Static-Konto D 1.500 bis 2.000 bei Target 3.000. Studio #002 (D 1.000) schafft es in keiner Kombination. Für Faustformeln: wegen der rechtsschiefen Tage den Lundberg-Exponenten (1/R rund 660 $) statt 2μ/σ² nehmen, sonst wird der Funded-Wert um Faktor 2 unterschätzt.
- **Was am meisten bewegt (Rapid EOD 50K):** (1) Inaktivität 7 Tage ohne Keep-alive: +15,1 ± 0,4 Monate, Konto praktisch wertlos. (2) Live-Wechsel mal Auszahlungsschwelle, mit großer Schwelle fast weg. (3) Puffer-Politik. (4) Intraday- statt Tagesschluss-Bruch: nur −0,6 Monate, die vorsichtige Wahl ist richtig. Ohne Wirkung: Eval-Lock, Builder-Qualifying-Schwelle, Preis, Pro-Kontraktlimit (laut Mathematiker höchstens 2 Beine gleichzeitig offen; der CFD-Check fand mit `t4_check` an 1,7 % der Tage 3 gleichzeitig offene NQ-Beine, bei „3 Micros gesamt" wäre das also knapp, aber erlaubt, solange M2K nicht dazukommt).
- Prüfdateien: `C:\Users\Administrator\mffu_check\calc\qm\`.

### `quant-statistician`: trägt mit Einschränkung

**Robustheits-Spalte shrink058** (Drift x 0,58 auf Flotte und Zusatzkonto, 200 Welten, Seed 101, gepaart). Flotte ohne: Mittel bis Kappe 115,6 Monate, Erreichung in 10 Jahren 20,5 %, Nulldrift 0,0 %.

| Zusatzkonto | Δ Mittel bis Kappe ± SE (shrink) | Erreichung 10 J (ohne 20,5 %) | Auslage p90 mit | Netto des Kontos nach 60 M (shrink) |
|---|---|---|---|---|
| Rapid EOD 50K cont / endg2 | −6,3 ± 0,8 / **−7,2 ± 0,8** | 35,0 / 37,5 % | 2.277 | 4.588 ± 360 $ (cont) |
| Pro 50K cont / endg2 | −7,2 ± 0,8 / −6,7 ± 0,8 | 38,0 / 37,0 % | 2.286 | 5.503 ± 354 $ (cont) |
| Builder 50K cont / endg2 | −6,9 ± 0,8 / −5,6 ± 0,7 | 37,5 / 34,5 % | 1.918 / 2.068 | 5.298 ± 316 $ (cont) |
| Pro 150K cont / endg2 | −7,0 ± 0,8 / −5,8 ± 0,7 | 39,0 / 35,0 % | 1.994 | |
| E8 Futures 100K | −3,9 ± 0,6 | 31,0 % | 2.116 | 1.729 ± 198 $ |
| FFN STEADY 150K | −3,2 ± 0,5 | 28,5 % | 1.957 | 2.271 ± 194 $ |

- **Belastbar:** alle MFFU-50K-Pläne und Pro 150K schlagen E8 100K und FFN 150K, in `cont` und `endg2`, roh und geschrumpft, gepaart, Holm über 63 Paare (alle p unter 0,001). Unter shrink gegen E8 100K: Rapid EOD endg2 −3,2 ± 0,5, Pro 50K −2,7 ± 0,5, Builder −1,7 ± 0,4 Monate. Gegenprobe mit dem zweiten Simulator: Zielzeit in 600 von 600 Welten identisch.
- **Nicht belastbar:** die Reihenfolge innerhalb von MFFU. Robust ist nur „Rapid EOD oder Pro 50K“, Builder liegt in `endg2` 1,0 bis 1,5 Monate dahinter. Die `endg2`-Schwellen sind auf denselben Welten gewählt (eher optimistisch), Gegenprobe auf Seed 202 fehlt. E8 150K gegen FFN 150K ist nicht unterscheidbar.
- **Größenordnung der Unsicherheiten:** Pfadrauschen 0,2 bis 0,4 Monate, Edge-Unsicherheit rund 20-mal größer (unter shrink bleiben 38 bis 52 % des Gewinns, die Rangfolge hält, Spearman 0,96), am größten die Konto-Mechanik (Live-Wechsel, Auszahlungspolitik, Inaktivität). Eine einzelne echte Zukunft streut 5 bis 9 Monate.
- **Inaktivität ist echt, keine Datenlöcher:** 23 Lücken ab 8 Kalendertagen, 133 von 142 betroffenen Werktagen mit vollen RTH-Daten, die übrigen sind Feiertage oder Halbtage. 2017 war ein ruhiges Jahr (104 Handelstage). Rate 2,13 je Jahr (90-%-CI 1,46 bis 3,02), ab 2019 1,41, stark geballt. 10 der 23 Lücken sind genau 8 Tage lang: greift die Regel erst ab 9 Tagen, halbiert sich die Rate. Auch dann übersteht ein Konto ohne Keep-alive 12 Monate nur mit 46 %. **Folge:** Keep-alive bauen, und die Inaktivität symmetrisch auch für E8 rechnen (dieselbe Regel, die Vergleichszeilen E8 100K/150K hätten dasselbe Problem).
- **Static sauber getrennt** (derselbe Plan, nur DD-Typ umgeschaltet, gepaart): Pro 50K Static gegen EOD −1,6 roh / −3,0 shrink, Builder −0,3 / −0,2 (nicht signifikant). Static hilft also nur spürbar, wenn sonst wenig Puffer bleibt. **„Studio lohnt nicht“ ist robust:** Builder cont schlägt Studio 20k um 3,6 (roh) bzw. 2,9 Monate (shrink), Studio 20k gegen E8 100K unter shrink gleichauf. Bei DayTraders entscheidet das Gebührenmodell, nicht Static.
- **Was zum Beweis fehlt:** `endg2` auf Seed 202, Inaktivität symmetrisch für alle Firmen (oder überall Keep-alive), Pro-Funded-Kontraktlimit, T1-Sperre und Rapid-Live nach Ermessen (Verzerrung zugunsten MFFU), Worst-Case-Spalte 2016 bis 2020.
- Dateien: `C:\Users\Administrator\mffu_check\qs\`.

## 7. Was vor einem MFFU-Kauf fehlt

**Schriftlich vom MFFU-Support** (Ticket **AP440**; Live-Chat oder Discord, eine offizielle Support-Mail ist nicht belegt; Antwort als Screenshot/Transkript sichern):
1. Vollautomatischer, unbeaufsichtigter, selbst geschriebener NinjaScript-Bot auf einem Windows-VPS in Deutschland (Rechenzentrums-IP), in Eval, Sim Funded und Live erlaubt?
2. Dieselben Signale auf mehreren eigenen MFFU-Konten und gleichzeitig auf eigenen Konten bei E8, FundedNext und FFN: erlaubt, fällt das unter Terms §23.1.3.3?
3. Hedging: zwei Beine im selben Konto, eins long und eins short MNQ zur gleichen Zeit (die Position nettet am Broker): Verstoß?
4. HFT/Microscalping: Grenze (Trades je Tag, Haltedauer)? Problem, wenn ein Bein in 11 % der Fälle in derselben Minute ausgestoppt wird?
5. EOD-MLL: wird ein Bruch intraday ausgelöst, wenn die Equity den Floor berührt, oder nur zum Tagesschluss?
6. Builder 50K und Rapid EOD 50K: was passiert beim Live-Wechsel mit dem Sim-Saldo, und läuft das Konto danach wie im Sim Funded weiter? (Das entscheidet zwischen −12 und −16 Monaten.)
7. Pro Funded „3/3“: 3 Kontrakte gesamt, 3 Minis oder 3 Micros?
8. NT8: Tradovate oder Rithmic, eigene NT8-Lizenz nötig, Datengebühren, nur ein Gerät gleichzeitig?
9. Positionsgröße (Terms §12.4): ist ein späteres Hochstufen von 1 auf 2 Micros je Bein ok?
10. Bitte die Appendices des „Simulated Trader Agreement“ zu Automation, VPS und IP.

**Danach, vor dem ersten Trade:** Ablauf `/neues-konto` (Regeln in [[Firm-Regeln je Konto]], RiskGuard-cfg mit Tagesstopp 900 $ wie E8 50k, Telegram, Host-Datei), bei Rapid EOD/Pro die T1-Sperre (AP335) auch für das MFFU-Konto, **Keep-alive gegen die 7-Tage-Inaktivität verlässlich, am besten automatisch** (Mini-Trade-Option im RiskGuard, heute aus), sonst ist das Konto fast wertlos. Kauf nach den Bedingungen der [[Kaufvorlage Kaufrunde 06.11.2026]] (BOS-Plan AP238, Doppel-Exit-Fix AP381, harter Deckel).

**Für DayTraders Static 150K** (nur wenn gewünscht): Einmalpreis oder Abo, NT8 über Rithmic auf Static-Konten, Deutschland ausdrücklich, Copy-Zählung über Firmen, Qualifying-Day-Schwelle bei 150K, Live-Kriterien.

## 8. Annahmen und was nicht im Modell ist

- EOD-Floor wird intraday geprüft (wie E8, vorsichtig), Eval ohne Lock, Puffer bleibt nach jeder Auszahlung stehen (nach Wortlaut ist er bei Rapid EOD/Builder nur die Schwelle für die erste Auszahlung, die Folge-Payouts hängen an 500 $ Netto seit dem letzten, das rechnet sich praktisch gleich).
- Builder Qualifying Day mit 100 $ Mindestgewinn gerechnet, laut Wortlaut reicht ein Handelstag (Modell also etwas strenger).
- Rapid EOD Live-Wechsel nach 5 Payouts nur in `end`/`endg` angenommen, die Regel ist Ermessen.
- Jeder Kauf zum CLUB-Preis (40 %), Reset = Neukauf zum selben Preis. Pro 150K Preis 286 $ angenommen (Aug.-Liste x 0,6).
- Eigener Tagesstopp 900 $ bei DD 2.000, 2.500 $ bei DD 4.500, Static-Konten 45 % der DD.
- Nicht modelliert: T1-News-Sperre (Rapid EOD/Pro Funded), Inaktivität, Hedging, Kontraktlimit Pro Funded, MFFU-Live-Reserve (bis 5.000 $ Sim-Gewinn erst nach 20 Live-Tagen), Regelverstöße, die die ganze Firma treffen. DayTraders: Qualifying Day 200 $ auch bei 150K angenommen, Live-Kriterien unbekannt (läuft weiter).
- Nur **ein** Zusatzkonto gerechnet. MFFU erlaubt bis 5 Sim-Funded (Rapid EOD 3, Builder 1), mehrere MFFU-Konten sind nicht gerechnet.
- Buchdaten wie im CFD-Check (bis 07.08.2026). 50k sind brutto vor Steuern.

## 9. Dateien und Quellen

- Recherche: [[Research-Cache]] Abschnitte „MyFundedFutures (MFFU): alle Pläne inkl. Static-DD, Regeln, Algo/VPS, Copy (24.10.2026)“ mit Nachtrag „Detailregeln für die Simulation“ und „Static-Drawdown-Futures-Pläne am Markt (ohne MFFU), Regeln und Algo/VPS (24.10.2026)“.
- Rechnung auf der Box: `C:\Users\Administrator\mffu_check\calc\` (`mffu_kern.py` Käfig, `mffu_plans.py` Parameter und Annahmen, `mffu_run.py` Lauf je Plan, `acct_sim.py` Einzelkonto-Simulator für DayTraders/BluSky und Gegenprobe, `mffu_table.py` Tabelle, `test_kern.py` Selbsttest, Ergebnis `table_final.md`). Flotte und Vergleichszeilen aus `C:\Users\Administrator\cfd_vergleich\calc\out_A.npz` / `out_B.npz`. In `trading-data` wurde nichts geändert.


## 10. Zweite Runde: MFFU im echten Kaufplan (24.10. nachmittags)

**Methode:** wie die [[Kaufvorlage Kaufrunde 06.11.2026]] (`kauf_0611_v2.py`): Kaufrunde monatlich, höchstens ein bezahlter Kauf je Runde über alle Firmen (Reihenfolge rotiert), Budget 600 $/Monat bis Gehaltsende (7,9 Monate ab 06.11.), Deckel Netto-Auslage 2.500 $, danach BOS-Regel (nur noch aus Gewinn kaufen), FFN höchstens 5 Konten, E8 höchstens 5 Funded, RiskGuard-Tagesstopp, alle Politiken gepaart auf denselben Pfaden. Neu gegenüber der Kaufvorlage: **Kontostände vom 23.10.** (konto-analyst, kein Konto geplatzt, alle Salden gestiegen), **Trade-Daten bis 15.10.2026** (Kaufvorlage: bis 07.08.), Gebühr 1,90 $ je Round-Turn, MFFU Rapid EOD 50K als dritte Firma (135 $, max. 3 Funded laut Support, vorsichtige Auszahlung: Ende nach 5 Payouts, Auszahlung erst ab 4.000 $ über dem Puffer). 400 Welten je Regime (Nulldrift 200), andere Seeds als in der ersten Runde. Skript `C:\Users\Administrator\mffu_check\kauf\kauf_mffu.py`, Ergebnisse `kauf_mffu.md`, `kauf_mffu_fix.md`, `kauf_mffu_wc.md`.

**Ergebnis (Δ = gegen E8 + FFN, gepaart, negativ = schneller, Monate bis 50k als Mittel bis zur 120-Monats-Kappe):**

| Politik | alle Jahre | letzte 3 Jahre | Edge x 0,58 | 2016 bis 2020 | Auslage p90 |
|---|---|---|---|---|---|
| P5B E8 + FFN (Kaufvorlage) | 58,3 (Median 55,9) | 37,8 | 100,1 | 120 (Kappe) | 2.210 $ |
| **M1 E8 + FFN + MFFU** | **−5,32 ± 0,38** | **−2,03 ± 0,24** | **−3,08 ± 0,61** | −0,03 | 2.146 $ |
| M1c dasselbe, MFFU zahlt nach Live weiter | −6,14 ± 0,40 | −2,29 ± 0,22 | −3,07 ± 0,55 | −0,11 | 2.146 $ |
| M2 MFFU zuerst, dann E8 + FFN | −5,04 ± 0,45 | −1,42 ± 0,29 | −1,91 ± 0,66 | −0,06 | 1.989 $ |
| M3 FFN + MFFU (kein E8) | −4,72 ± 0,60 | −1,07 ± 0,44 | −0,71 ± 0,86 | −0,13 | 1.418 $ |
| M4 E8 + MFFU (kein FFN) | −3,61 ± 0,50 | −0,29 ± 0,35 | −0,74 ± 0,72 | −0,03 | 2.070 $ |
| M5 nur MFFU | +1,07 ± 0,77 | +5,07 ± 0,70 | +5,92 ± 0,88 | −0,09 | 540 $ |
| M1n E8 + FFN + nur 1 MFFU-Konto | −3,25 ± 0,25 | −1,48 ± 0,16 | −2,43 ± 0,43 | −0,03 | 2.344 $ |
| M1L E8 + FFN + MFFU, Live nach 3 Payouts (Reserve verfällt, nur 1 MFFU-Konto) | −3,22 ± 0,25 | −1,45 ± 0,16 | −2,35 ± 0,41 | −0,03 | 2.344 $ |
| M1b E8 + FFN + Builder 50K statt Rapid EOD | −2,51 ± 0,21 | −1,45 ± 0,16 | −2,21 ± 0,31 | −0,03 | 2.302 $ |

Nulldrift: in allen 10 Politiken 0,0 % Zielerreichung. Chance auf 50k in 5 Jahren (alle Jahre): P5B 61,5 %, M1 72,5 %.

**Sensitivitäten (alle Jahre):**
- **News-Sperre** für MFFU- und FFN-Funded (Trades, die an FOMC- und Minutes-Tagen 13:58 bis 14:02 offen sind, fallen weg; 55 Trades in 10 Jahren, davon LastHour 33, OpenDrive 14, PB3 8): P5B +1,0 Monate, M1 +1,4, M1 bleibt −4,95 ± 0,38 vorn. Die Sperre ist für uns billig, muss aber gebaut sein (AP335), weil LastHour um 14:00 immer offen ist.
- **Inaktivität ohne Keep-alive** (E8 und MFFU, erster Handelstag nach 7 vollen Kalendertagen ohne Trade = Bruch, 23 Fälle in 10 Jahren, echte Handelspausen, keine Datenlöcher): P5B fällt auf 105,5 Monate (Mittel, **+47,2**), M1 bleibt −3,14 ± 0,55 vorn. Diese Zeile ist die realistische, wenn der Keep-alive nicht verlässlich läuft.

**Kontrollen:** ein erster Lauf hatte in den Sensitivitäten einen Fehler (wiederverwendete Rechenprozesse stapelten die Umleitungen, die News-Zeile lief mit Inaktivitäts-Sperre). Behoben, Nachlauf: das Hauptregime kommt **bitgleich** heraus, nur die News-Zeile ändert sich. Ein zweiter kleiner Fehler (Zeit-Versatz des Asia-Beins griff nie, 3 Trades, 0,2 % der Drift) ist im Skript korrigiert, die Läufe sind deswegen nicht wiederholt. Käfig-Erweiterung um den Live-Wechsel bitgleich zur alten Fassung für alle alten Pläne (`test_kern2.py`).

**Gegenlesen:**
- `quant-statistician`: **M1 trägt mit Einschränkung.** Gepaart in jedem Regime mit Edge schneller (z −14 / −8,5 / −5,1), Bonferroni über alle Vergleiche bestanden (kleinstes |z| 5,05). Die Größe ist klein gegen die Unsicherheit der Edge: der Vorsprung entspricht 0,29 Standardfehlern der Drift (1 SE Drift = rund 18 Monate). M2 und M3 tragen nicht belastbar, M4 und M5 nicht. In 2016 bis 2020 ist die Buch-Drift nicht von null unterscheidbar (4,65 $/Tag gegen 56,1 ab 2021), die ganze Zeit bis 50k hängt am Regime seit 2021. Minutes-Termine: +21 Tage trifft 79 von 87, mit echten Terminen 60 statt 55 Trades, ändert nichts. Inaktivität: 7 volle Tage (Abstand ≥ 8) ist die wörtliche Lesart bei E8 und MFFU.
- `quant-mathematician`: **trägt nach dem Worker-Fix**, mit einem kleinen Fehler und zwei Modellfragen.
  - Buch, Gebühr, Achse, Kaufrunde, Paarung (P5B in seinen Nachläufen bitgleich), Kernel-Erweiterung (auf den Buch-Zellen bitgleich zu v1), Regime: tragen. Die Worker-Stapelung hat er selbst nachgestellt, der Fix ist korrekt.
  - **Asia-Versatz bei T1** (derselbe Fund wie beim Statistiker): richtig gerechnet 58 Trades und +3.354 $, M1 in der News-Variante −4,62 ± 0,38 statt −4,95. Im Skript korrigiert.
  - **Inaktivität als Szenario schief:** „symmetrisch“ heißt „nirgends Keep-alive“ und bestraft vor allem E8, wo Keep-alive erlaubt ist und praktiziert wird. Sein Nachlauf nur für MFFU (IS_inactM, 400 Welten, gleiche Seeds): M1 **+4,75 ± 0,40**, M1c +3,65, M1n +2,42, M2 +8,00, M5 +57,3 Monate gegen P5B. Je MFFU-Konto: Eval-Pass 22,6 statt 75,9 %, mindestens ein Payout 15,1 statt 83,6 %, Netto 779 statt 13.606 $. Grund: 1,39 % Lücken-Rate je Handelstag, 270 Handelstage ohne Lücke schafft ein Konto nur mit 2,3 % (seit 2021 0,86 % Rate, tödlich bleibt sie trotzdem).
  - **Live:** „nach 3 Payouts“ ist eine Annahme, laut Regel automatisch erst bei 10.000 $ an einem Tag (für unser Buch nie), sonst Ermessen. Der 3. Payout kommt im Median erst rund 40 Monate nach dem Kauf, deshalb M1L ≈ M1n. Das echte Risiko ist eine frühe Beförderung nach Ermessen (andere MFFU-Konten frieren ein, 21 Tage Cooldown nach Live-Bruch). Ehrliche Spanne: M1n (−3,25) bis M1 (−5,32).
  - **Eval-Einrasten bei +100** (Support 28.09. für Rapid/Pro, Rapid EOD nicht genannt): Pass-Quote 84,9 statt 76,7 %, M1 −5,73 statt −5,32. Gerechnet ist ohne Einrasten, also vorsichtig.
  - News-Fenster: Treffer mit 1 und 2 Minuten identisch, ganze Trades streichen ist pessimistischer als „Tag auslassen“ oder „um 13:58 glattstellen“. Für die Umsetzung: OpenDrive steigt teils um 14:04 ein, auch ruhende Orders dürfen im Fenster nicht offen sein.
  - `y16_20` hat eine Drift von 4,65 $/Tag (t = 1,0), ist praktisch ein zweiter Nulldrift-Lauf und unterscheidet MFFU nicht von P5B.
  - Prüfdateien: Box `C:\Users\Administrator\mffu_check\kauf\qm\`, PC-Scratchpad der Session `kauf\qm`, `kauf\pcrun2`.

## 11. Kriterien-Check Rapid EOD 50K gegen Box und Regeln

| Kriterium | Stand | Quelle |
|---|---|---|
| Automation, eigener NinjaScript-Bot | ✅ erlaubt in Eval, Sim Funded, Live, kein HFT | Support-Mails 28.09. |
| VPS mit Rechenzentrums-IP | ✅ „no VPS/IP restrictions as long as you are not sharing devices“ | Support 28.09. |
| Unbeaufsichtigt | ✅ „allowed provided it can be intervened by the user and managed“ (Telegram plus Fernzugriff) | Support 29.09. |
| Plattform | ✅ NT8 über Tradovate (Rithmic bei MFFU gesperrt). ⚠️ ob die MFFU-Verbindung in derselben NT8-Installation neben Tradovate (E8, FN) und Rithmic (FFN) läuft: offen, auf der Box testen | Support 28.09., Help Center |
| Deutschland, KYC | ✅ | Support 28.09. |
| Copy auf eigenen MFFU-Konten | ✅ | Support 28.09. |
| **Dieselbe Strategie bei E8/FN/FFN** | ❌ offen, zweimal gefragt, nie beantwortet; bewusst nicht nochmal gefragt (Max 24.10.) | Thread 28./29.09. |
| Drawdown | ✅ EOD-Trailing 2.000, rastet bei +100 ein (auch in der Eval). ⚠️ Bruch intraday oder nur Tagesschluss: offen, gerechnet intraday (vorsichtig) | Support 28.09., Help Center |
| Consistency | ✅ Eval 30 % (nur das Ziel steigt, kein Bruch), Funded keine | Help Center |
| Kontraktlimit | ✅ 3 Minis / 30 Micros, wir handeln höchstens 5 Micros | Help Center |
| Flat-Zeit | ✅ Auto-Close 16:10 ET, wir sind 15:55 flat | Help Center, Support |
| **News (T1) im Funded** | ⚠️ für Rapid EOD widersprüchlich (Plan-Artikel ja, Policy und Support nennen nur Rapid und Pro). Falls ja: Sperre 13:58 bis 14:02 an FOMC/Minutes, LastHour ist dann immer offen, also AP335 bauen. Kostet rechnerisch rund 1 Monat | Help Center, Support 28.09. |
| **Inaktivität 7 Tage** | ❌ **entscheidend:** ohne erlaubten Keep-alive ist MFFU im Kaufplan 4,75 Monate langsamer statt 5,3 schneller. Ein reiner Mini-Trade ist nicht eindeutig erlaubt („strategy must remain consistent“), Frage 1 der Mail | Support 29.09., quant-mathematician |
| **Hedging** | ❓ „hedging of any kind“ verboten, gegenläufige Beine im selben Konto nicht geklärt, bewusst nicht gefragt (Max 24.10.) | Help Center |
| HFT, schnelle Stop-outs | ⚠️ keine Zahl, PB3 hat rund 11 % Stop-outs in der ersten Minute | Help Center |
| Kontolimits | ✅ 10 Konten, bis 3 Rapid EOD Funded | Support 28.09. |
| Live | ⚠️ nur 1 Live-Konto, dann ruhen alle MFFU-Sim- und Eval-Konten; Zeitpunkt nach Ermessen, bis 5.000 $ Sim-Gewinn als Reserve. Gerechnet als M1L: −3,2 statt −5,3 Monate | Support 29.09., Help Center |
| Preis | ✅ 135 $ mit CLUB, laut Support für beliebig viele Käufe | Support 29.09. |

**Vor dem ersten Trade (wenn die Antworten passen):** `/neues-konto` (Firm-Regeln, RiskGuard-cfg mit Tagesstopp 900 $, Telegram), Keep-alive verlässlich (für MFFU nur, wenn erlaubt), AP335 News-Sperre, falls T1 für Rapid EOD gilt, MFFU-Verbindung in NT8 auf der Box testen. Kauf nach den Bedingungen der Kaufvorlage (BOS-Plan AP238, AP381).

## 12. Nachfrage-Mail an MFFU

Neue, kurze Mail an support@myfundedfutures.com (Gmail maxlkho4, Entwurf, **gesendet erst nach Max' OK**), bewusst **nicht** als Antwort im alten Verlauf, weil dort andere Firmen erwähnt sind. Regel Max 24.10.: nur das Nötige fragen, nichts schon Beantwortetes wiederholen (VPS, Automation), keine anderen Firmen erwähnen, nichts Unnötiges über das System preisgeben.

Gefragt wird nur noch: (1) Keep-alive-Trade gegen die Inaktivität, entscheidet (A/B, mit Ausweichfrage), (2) gilt T1 für Rapid EOD Funded, zählen Stop/Target-Orders, Folge eines Verstoßes, (3) Live-Wechsel und Rest-Saldo, (4) NT8-Lizenz für Automation, (5) Provision MNQ und Reset-Preis. Ticket AP440.

**Bewusst nicht gefragt (Max 24.10.):** dieselbe Strategie bei anderen Firmen, Hedging gegenläufiger Beine, schnelle Stop-outs, Prüfzeitpunkt des EOD-Floors, Einrasten in der Eval, späteres Hochstufen. Diese Punkte bleiben offen und werden im Betrieb selbst abgesichert (vorsichtig rechnen, NT8-Verbindung auf der Box testen).
