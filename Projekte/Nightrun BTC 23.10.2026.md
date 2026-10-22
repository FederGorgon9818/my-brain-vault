---
date: 2026-10-23
tags: [projekt, alpha, daten, bitcoin, krypto, discovery, neue-maerkte, gate-v4]
status: läuft
---

# ₿ Nightrun BTC (23.10.2026): Bitcoin-Futures in die Engine, vermessen, drei Familien getestet

Auftrag Max 22.10.2026 ca. 23:10 (Nacht, Max schläft, PC aus): kompletten Durchlauf für Bitcoin planen und fahren. Genau anschauen, was BTC wie viel von was hat, welche unserer Familien direkt kompatibel wären, die Top 3 wählen und alle Strategien davon einmal durch Gate v4 schicken. Nicht nur BTC gegen NQ vermessen, sondern die Parameter an BTC anpassen. Was gut läuft, kommt ins Next-Week-Buch.

Verwandt: [[Neue Märkte (NT8-Daten) Plan]] (der Vorläufer-Nightrun auf GC/CL vom 19.09.), [[Strategie-Logbuch]], [[Discovery-Runner v2]], [[Alpha-Suche]], [[Buch-Workflow]], [[Firm-Regeln je Konto]], [[Research-Cache]].

> ## 🧭 Kurzfassung für Max
>
> **BTC ist drin und vermessen, aber es kommt nichts ins Next-Week-Buch, und der Grund ist nicht der Markt, sondern die Kosten.**
>
> **1. Der Mechanismus existiert wirklich.** Bitcoin hat am 09:30-ET-Anker einen Opening-Range-Bruch, der alles übersteht, was man dagegen werfen kann: über 21 Tests korrigiert bleibt p = 0,002, er hält Trimmung, er hält ohne die fünf besten Tage, fünf von fünf Purged-Folds sind positiv. Und NQ hat ihn nicht, was zu unserem eigenen Friedhof passt. Verschiebt man das Fenster nur um 90 Minuten nach vorn, fällt alles zusammen. Das ist der sauberste neue Mechanismus, den wir seit Monaten gefunden haben.
>
> **2. Er zahlt trotzdem nicht.** In Netto-Dollar, der einzigen Einheit die ein Prop-Konto auszahlt, ist er null: +0,0004 $ je Trade. Mit ehrlich gemessenen Kosten von 6,40 $ je Round-Turn sogar −1,68 $. Der Median-Trade verliert 5,90 $, nur 40 % gewinnen, und das Gesamtergebnis hängt an einem Prozent der Trades. Das Break-even, ab dem ein BTC-Bein die Buch-Sharpe nicht mehr *senkt*, liegt bei 5,04 bis 6,89 $ je Trade. Die Wahrscheinlichkeit, dass wir da drüber sind: 7 %.
>
> **3. Eine Zeile hat einen Weg, und die läuft.** Der Filter auf große Opening Ranges bringt bei OR60 +8,75 bis +11,69 $ je Trade mit positiver unterer CI-Grenze, übersteht den Kosten-Stress und ist ab 2021 stärker. Auf OR30 dreht derselbe Filter ins Negative, deshalb ist die OR-Länge im Job eine Achse. Zwei Jobs rechnen auf der Box: der Filter und eine Kontrolle mit Zufallsleveln. **Die Kontrolle hat schon gewarnt** — bei der strengen Schwelle macht das Zufallslevel +5,37 $, dort ist ein guter Teil also Vola-Konditionierung und nicht das Level.
>
> **4. Die wichtigste Zahl der Nacht ist aber eine andere: AP399 entscheidet mehr als jede Rechenzeit.** Ein BTC-Bein mit 4 $ netto je Trade verkürzt die Zeit bis 50.000 $ auf **einem** E8-Konto von 189 auf 186 bis 188 Monate. Das sind +95 bis +180 $ über drei Jahre gegen einen Fehlerbalken von 383 $, also unter dem Rauschen. Auf **allen fünf** Konten wären es 173 bis 180 Monate. FundedNext erlaubt nachweislich kein Krypto, FFN ist ungeprüft. **Solange FFN offen ist, ist die Obergrenze des ganzen BTC-Vorhabens rund 2 % Zeitgewinn.** Diese eine Antwort ist mehr wert als 350 Configs.
>
> **5. Was ich dir offen lassen muss:** Du wolltest alle Strategien der Top 3 Familien durch Gate v4. Ich habe 2 von 12 eingereiht. Mean Reversion ist über eine Rechnung erledigt (der Effekt sättigt bei 2,50 bp gegen 7,73 bp Kosten, und auf dem einzigen billigeren Kontrakt wäre eine Einheit 316 % der Drawdown-Grenze), Intraday Bias hat die Multiple-Testing-Korrektur nicht gehalten und war ohnehin der Klon unseres lebenden Momentum-Beins. Die zehn nicht eingereihten Zeilen stehen alle mit Zahl in Abschnitt 8 und liegen als fertige Grids in `hypothesen.json` — ein Befehl, wenn du den vollen Sweep trotzdem willst. **Das ist deine Entscheidung, nicht meine.**
>
> **6. Zum Mitlesen, weil es die Nacht prägt:** vier eigene Messfehler habe ich selbst gefunden und korrigiert, vier weitere Aussagen hat das Quant-Team widerlegt — darunter meinen ersten Hauptbefund („der Effekt zerfällt"), der sich als Einheiten-Artefakt entpuppte. Die Lehre daraus ist allgemein und steht als Lehre 182 im Logbuch: auf einem Markt, dessen Preis sich verzwölffacht hat, ist bp keine stabile Einheit, und welche Einheit gilt, ist eine Messung und keine Annahme.
>
> **Modell und Session:** Für die Auswertung morgen reicht **sonnet**, die Zahlen stehen alle hier und in `_scratch_btc_nightrun/`. Nimm eine **frische Session** (`/clear`), diese hier ist nach einer ganzen Nacht voll. Für die AP399-Entscheidung und die Frage, ob der Filter-Job ein Bein werden darf, lohnt **opus oder fable**.

---

## 1. Daten: BTC und MBT sind drin

NT8-Bulk-Export war um 23:24 fertig (`_DONE.txt`), BTC mit 106 Kontraktdateien ab 12/2017, MBT mit 66 ab 05/2021. Continuous gebaut mit dem **unveränderten** `_nt8_to_parquet.py`, der Krypto schon kennt (`WEEK_24_7`, CME-Wochenfilter nur bis Session 29.05.2026).

| | BTC | MBT | NQ (Referenz) |
|---|---|---|---|
| Bars 1m | 1.911.498 | 1.348.234 | 3.779.584 |
| Sessions | 2.313 (19.12.2017 bis 22.10.2026) | 1.452 (10.05.2021 bis 22.10.2026) | 2.791 (bis 16.10.2026) |
| Rolls | **105, also 11,4 im Jahr** (4,5 % der Sessions) | 65 | 42 (quartalsweise) |
| Bars je Session (Median) | 878 von 1.380 Minuten, also **64 %** | 934 | praktisch 390 von 390 im US-Fenster |
| Volumen je Minute (Median) | **4 Kontrakte** | 11 | 107 |

**Zwei Datenbefunde, die alles Weitere prägen:**

**(a) BTC rollt monatlich und springt dabei.** Scheingap am Roll 0,70 % gegen 0,31 % an normalen Session-Übergängen (p90 2,28 % gegen 1,65 %), 34 von 105 Rolls über 1 %, Roll-Lücke im Protokoll Median 220 Punkte, p90 776, max 2.995. Das ist dieselbe Falle wie bei CL am 19.09., nur häufiger. **Folge: kein einziger BTC-Job nutzt `prev_close`, `overnight` oder `gap` als Basis.** Auf 4,5 % der Sessions wären das Schein-Signale, Richtung falsch-positiv.

**(b) Wochenend-Mini-Sessions.** CME-Krypto handelt seit Session 30.05.2026 durch, der Konverter lässt Wochenend-Bars ab da stehen. Im US-Fenster 09:30-15:59 sind das 34 Sessions mit **Median 16 Bars und maximal 95**, gegen Median 343 und p05 113 an Wochentagen. `_drop_corrupt_sessions` fängt das nicht, der prüft nur Preise. Eine 16-Bar-Session liefert eine Schein-Tagesrange und einen Schein-Opening-Range. Deshalb gibt es einen neuen Job-Schalter (siehe Abschnitt 2).

**Engine-Einträge** (`qbt.py`, Backup `qbt.py.bak-20261022-btc`): `POINT_VALUE` BTC 5,0 und MBT 0,1 (BTC 5 BTC je Kontrakt, MBT 0,1 BTC, Preis in $ je BTC), `TICK` je 5 Indexpunkte, `MICRO_OF` BTC→MBT und MBT→MBT, `COMMISSION_RT_MICRO` MBT **3,20 $** je Round-Turn. Die Gebühr stammt nicht aus einer Schätzung, sondern steht als Primärquelle im [[Research-Cache]] (E8-Instrumentenliste, Stand 13.10.2026: 0,78 Kommission + 2,04 Exchange/NFA + 0,38 Clearing). **Krypto-Micros sind teurer als Index-Micros** (2,04 gegen 0,74 bei MNQ).

**Golden Master: grün.** Alle 10 Referenzfälle bitgleich (Delta 0,00 auf tpy, Sharpe, n_trades, expR, $/Jahr, pf_usd), alle Kanarien grün inklusive der CME-Wochen-Kanarie mit der Krypto-Ausnahme, der Gate-v4-Kanarie und der ORB-Whitelist. $-Selbsttest mit Zahlen: 1 Tick MBT = 0,50 $, `commission_rt_for("BTC")` = 3,20, Kosten je Trade bei 2 Ticks Slippage je Seite = 5,20 $. Marker `regression_ok` gesetzt und jünger als `qbt.py`. Zusätzlich selbst geprüft: `config_key` hasht nur die expliziten Job-Params, der neue `DEFAULTS`-Schlüssel verändert also **keinen** Register-Schlüssel im Bestand.

---

## 2. Neu in der Engine: `min_session_bars`

Ein einziger neuer Job-Parameter, Standard `None` = aus, Bestand damit bitgleich.

`qbt.load_bars()` ruft jetzt `_drop_thin_sessions()` auf und verwirft Sessions mit weniger als `min_session_bars` Bars. Für alle BTC-Jobs steht er auf **100**: Wochenend-Sessions haben maximal 95 Bars, Wochentage mindestens 113, die Trennung ist also sauber. Verworfen werden 88 von 2.297 RTH-Sessions (3,8 %), davon 34 Wochenende und 54 dünne Feiertage. Der Rauchtest hat bestätigt, dass 2.209 Sessions übrig bleiben, also genau die gerechnete Zahl.

Warum als Engine-Schalter und nicht als Daten-Filter: die Krypto-Ausnahme im Konverter ist Absicht (Max, 18.10.) und hängt an der Golden-Master-Kanarie `gm_cme_week_canary.py`. Am Konverter zu drehen hätte MET mitgetroffen und die Kanarie gebrochen. Ein Job-Schalter ist additiv und lässt beides stehen.

---

## 3. Die Kostenschwelle ist bei BTC die halbe Geschichte

Das ist der Punkt, der alles andere einordnet, und er ist bei BTC anders als bei jedem Markt, den wir bisher hatten.

MBT-Kosten sind in Dollar **fix** (5,20 $), der Kontraktwert hängt aber am BTC-Preis. Also:

**Kosten in bp = 5,20 $ / (0,1 × Preis) × 10.000 = 520.000 / Preis**

| Jahr | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | heute |
|---|---|---|---|---|---|---|---|---|---|---|
| Kostenschwelle in bp | 75,1 | 66,1 | 53,1 | 10,8 | 22,5 | 18,8 | 8,1 | 5,0 | 7,1 | **6,28** |
| MBT-Tagesrange in $ | 40,5 | 34,0 | 48,5 | 305 | 136 | 281 | 365 | 230 | — | — |
| Kostenquote in % der Range | 12,8 | 15,3 | 10,7 | 1,70 | 3,83 | 5,33 | 1,85 | 1,43 | 2,26 | — |

**BTC war vor 2021 auf MBT kostentot.** Nicht weil der Mechanismus fehlte, sondern weil der Preis 7.000 $ statt 83.000 $ war: dieselbe Prozentbewegung war in Dollar zwölfmal kleiner, die fixen 5,20 $ dagegen gleich groß. Jede bp-Zahl auf BTC ist nur gegen die Schwelle ihres Jahres lesbar.

**Für Gate v4 heißt das:** der Walk-Forward rollt ab Datenbeginn, Testjahre sind damit 2020 bis 2026, davon liegt **nur 2020** im kostentoten Regime. Eine Sample-Beschneidung ist nicht nötig, das Verfahren erledigt es selbst.

**Für den Käfig, und hier lag ich falsch.** MBT-Tagesrange über 3 Jahre 281,5 $ gegen MNQ 681,25 $. Mit der Faustregel σ_Bein ≈ 0,15 × Range käme man auf 34,5 $ (2026) und damit auf „ein MBT ist ein halbes Bein". **Gemessen ist das falsch.** Die echte Standardabweichung der ORB-Trades ist **85,1 $ (gesamt), 96,9 $ (ab 2021), 117,8 $ (ab 2024)** gegen die Buch-Beine mit 77,3 / 87,1 / 107,7 / 134,2 $. Der Mathematiker hat die Ursache gefunden: die Faustregel trifft nur das Alle-Jahre-Sigma, im heutigen Hoch-Vola-Regime verzerrt sie um Faktor 1,77 bis 2,23 nach unten. **Ein MBT ist ein volles Bein, im heutigen Regime das zweitgrößte im Buch.** Das hebt die Break-even-Schwelle von 4,11 auf 6,89 $ je Trade.

Dazu eine Zahl, die man nicht übersehen darf: **der MaxDD des Beins allein ist −2.458 $ bei einer Drift von praktisch null.** Das sind 123 % der E8-50k-DD-Grenze und 164 % der FN-Flex-Grenze. Ein driftfreies Bein dieser Tiefe ist auf den 50k-Konten eine Bust-Maschine.

---

## 4. Profil: BTC gegen NQ

| | BTC | NQ |
|---|---|---|
| Tagesrange Median | **4,37 %** (p90 9,31 %) | 1,54 % (p90 3,21 %) |
| Tagesvola | 3,98 % | 1,39 % |
| Volumen im US-Fenster 09:30-16:00 | **51,7 %** | 76,7 % |
| Range im US-Fenster | 62,4 % der Vollrange | 83,5 % |
| Vola je Stunde (ET) | **flach, 0,97 bis 1,17 %** (Ausnahme 18:00 mit 2,57, das ist die Wiedereröffnung nach der Pause) | 0,15 bis 0,49, Faktor 3,3 |
| Volumen je Stunde | 2,0 % (00:00) bis 10,2 % (10:00) | 0,6 % bis 16,2 % |
| Kurtosis 5min / Tag | **174** / 5,4 | 102 / 7,1 |
| Schiefe Tag | −0,399 | −0,285 |
| Tages-Autokorrelation lag1 | −0,021 (2024 −0,087, 2025 −0,095) | −0,112 |
| Range in % je Jahr | 5,78 (2018) fallend auf **3,05** (2026) | 1,2 bis 2,7, kein Trend |

**Was daran für die Familienwahl zählt:**

- **BTC hat praktisch keine Vola-Tageszeit.** Die Stundenvola ist flach, während NQ um Faktor 3,3 schwankt. Das Volumen schwankt dagegen um Faktor 5. Eine Intraday-Bias-Idee auf BTC kann sich also nicht auf "diese Stunde ist volatiler" stützen, nur auf "hier ist Fluss".
- **BTC ist sprunglastig.** 5min-Kurtosis 174 gegen NQ 102.
- **BTC wird ruhiger, nicht wilder.** Prozent-Range halbiert sich über das Sample. Feste Prozent- oder Punktschwellen sind auf dieser Reihe strukturell unbrauchbar, deshalb laufen die Jobs wo möglich auf sigma- oder baz-normierten Achsen.
- **Wochenende** ist erst seit 30.05.2026 messbar (145 Sessions): Vola 0,865 gegen 0,594 in der Woche, aber nur 4,1 % des Volumens. Zu wenig Historie, um darauf zu bauen. Der Sonntags-Open-Gap ist laut Research-Cache seit demselben Datum **strukturell weg**, darauf wird bewusst nichts gebaut.

**Korrelation zu NQ, und hier habe ich die falsche Größe benutzt.** Tages-ρ der Renditen ist 0,307 über alles und steigend (2024 0,323, 2025 0,463, 2026 0,476). Das klang nach einer Warnung, ist aber für die Buch-Frage die falsche Zahl. Relevant ist die **PnL-Korrelation des Beins zum Buch**, und die hat der Statistiker auf dem echten 4-Bein-Buch gerechnet (1.155 gemeinsame Tage):

| | ρ | CI90 |
|---|---|---|
| **BTC-ORB gegen Buch-Summe** | **+0,092** | [+0,026, +0,166] |
| gegen NQ_Momentum_PB3 | +0,112 | [+0,042, +0,177] |
| gegen NQ_LastHour_v3 | +0,110 | [+0,021, +0,206] |
| gegen NQ_Asia-Dir-USopen | −0,066 | [−0,112, −0,020] |
| gegen NQ_OpenDrive_maband2050 | −0,005 | [−0,057, +0,050] |

BTC wäre damit das **am zweitwenigsten korrelierte Bein** im Buch (buchintern liegt Momentum gegen OpenDrive bei +0,284). Auch kein Tail-Problem: an den 10 % schlechtesten Buch-Tagen ist BTC in 56,0 % der Fälle negativ gegen 56,4 % unbedingt. **Dekorrelation ist bei BTC also kein Problem. Sie ist nur wertlos ohne Drift**, und genau daran hängt alles (Abschnitt 7).

**Lead-Lag zu NQ: bei jedem 5min-Lag von −6 bis +6 praktisch null** (|ρ| < 0,009), nur Lag 0 ist 0,305. Es gibt keinen ausnutzbaren Vorlauf in eine der beiden Richtungen.

---

## 5. Varianz-Verhältnis: BTC und NQ sind spiegelbildlich

| Horizont | 15min | 30min | 1h | 4h | 1 Tag | 5 Tage | 20 Tage |
|---|---|---|---|---|---|---|---|
| BTC | 0,959 | 0,946 | 0,942 | **0,885** | **0,882** | 1,016 | 1,095 |
| NQ | 0,980 | 0,991 | 0,989 | 1,019 | 0,966 | 0,884 | **0,627** |

BTC kehrt intraday um und läuft auf Wochen, NQ ist intraday fast Random Walk und kehrt auf Wochen um.

**⚠️ Diese Tabelle hält nicht. Beide Quant-Agents haben sie unabhängig zerlegt, und sie hatte zusätzlich einen Rechenfehler von mir.**

**Erstens, der Rechenfehler.** Mein `bars_5m` wirft leere Minuten weg (`dropna`) und aggregiert danach über *q Beobachtungen* statt über *q × 5 Minuten*. Bei BTC sind nur 878 von 1.380 Minuten belegt, der Lücken-Median liegt bei 494 Minuten je Session. Die Zeile „1 Tag 0,882" umfasst damit real rund 1,6 Sessions und enthält unregelmäßig Overnight- und Roll-Sprünge. **Sie misst nicht, was sie behauptet.** Für NQ (volle Belegung) stimmt sie.

**Zweitens, das Sub-Diffusive ist zu 100 % Bid-Ask-Bounce.** Der Mathematiker hat das Bounce-Modell angelegt (ein reiner Bid-Ask-Bounce ist MA(1) und liefert VR(q) = 1 + 2ρ(1 − 1/q)), mit dem gemessenen ρ = −0,03048:

| Horizont | VR gemessen | VR nur Bounce | **VR-Rest** | H-Rest |
|---|---|---|---|---|
| 15min | 0,9594 | 0,9594 | **1,0000** | 0,500 |
| 30min | 0,9460 | 0,9492 | **0,9966** | 0,499 |
| 1h | 0,9419 | 0,9441 | **0,9976** | 0,500 |
| 4h | 0,8851 | 0,9403 | 0,9412 | 0,492 |

Das 15-Minuten-Varianz-Verhältnis wird vom Bounce-Modell auf **vier Dezimalstellen** reproduziert. Bis eine Stunde bleibt nichts übrig.

**Drittens, gegen NQ gemessen dreht sich die Aussage sogar.** Der Statistiker hat die Varianzkurve innerhalb der US-Kasse über 13 Horizonte geschätzt, mit dem Rausch-Term **mitgeschätzt** statt als Umkehr verbucht: Hurst BTC **0,478** [CI90 0,462–0,496], NQ **0,467** [0,449–0,496], σ_Bounce 1-min BTC 1,4–2,0 bp gegen NQ 0,0–0,4 bp. Gepaart auf 1.753 gemeinsamen Sessions: **ΔH = +0,009, CI90 −0,024 bis +0,036.** Null, und beim bounce-freien Sockel kehrt **NQ stärker um als BTC**.

> **Fazit: „BTC kehrt intraday um, NQ nicht" ist nicht gedämpft, sondern widerlegt.** Es war der Bid-Ask-Bounce eines Marktes mit 4 Kontrakten Volumen je Minute gegen NQs 107. Damit fällt die Familie Mean Reversion als Ganzes (siehe Abschnitt 8).

**Bedingte Fortsetzung, und hier wird es interessant.** Mittlere Folgerendite in Richtung der Bewegung, z gegen rollendes Sigma:

| Basis | z<0,5 | 0,5-1 | 1-2 | 2-3 | z>3 |
|---|---|---|---|---|---|
| BTC 15min | −0,38 (t −3,5) | **−1,08 (t −5,9)** | −0,56 (t −2,0) | **+2,06 (t +2,3)** | **+3,77 (t +2,3)** |
| BTC 30min | −0,79 (t −3,5) | **−1,99 (t −5,6)** | −1,01 (t −1,7) | +1,68 (t +1,0) | **+6,14 (t +2,3)** |
| BTC 60min | −0,71 (t −1,6) | **−2,50 (t −3,5)** | −0,48 (t −0,4) | +1,36 (t +0,5) | +3,04 (t +0,7) |
| NQ, alle Basen | alles \|t\| < 2,5, überwiegend < 1,6 | | | | |

**Normale Bewegungen kehren um, extreme laufen weiter.** NQ zeigt nichts Vergleichbares. **Aber gegen die Kostenschwelle von 6,28 bp:** die Umkehr ist 2,0 bis 2,5 bp, also Faktor 2,5 bis 3 **unter** den Kosten. Die Fortsetzung der extremen Bewegung ist 3,8 bis 6,1 bp, also **an oder unter** der Schwelle. Keine der beiden Mechaniken trägt in ihrer rohen Form.

---

## 6. Der Fenster-Scan: der 09:30-ET-Anker ist echt und eng

Bruttobewegung, Bruch der Opening Range bis Fenster-Ende, ohne Stop. Das ist kein Strategie-Ergebnis, sondern die gerichtete Bewegung, die eine Strategie zu holen hat.

| Fenster (ET) | Volumen-Anteil | erstes Drittel sagt Rest | ORB30 | ORB60 |
|---|---|---|---|---|
| **09:30-15:59 US-Kasse** | 50,5 % | +7,94 bp (t +2,03) | **+17,23 (t +3,45)** | **+17,50 (t +3,87)** |
| 08:00-15:59 US weit | 60,1 % | +2,46 (t +0,57) | +5,23 (t +0,99) | +1,57 (t +0,30) |
| 12:00-15:59 Nachmittag | 21,4 % | **+8,13 (t +2,24)** | +14,88 (t +3,54) | +9,08 (t +2,34) |
| 03:00-09:29 London | 20,2 % | +1,28 (t +0,29) | +9,27 (t +1,85) | +11,74 (t +2,55) |
| 18:00-16:59 CME voll | 100 % | +3,48 (t +0,84) | +6,20 (t +1,00) | +13,41 (t +2,22) |
| 19:00-02:59 Asien | 16,3 % | +4,59 (t +1,04) | −4,26 (t −0,80) | +4,80 (t +0,89) |
| 18:00-02:59 Abend | 19,7 % | −4,10 (t −0,96) | +4,08 (t +0,75) | +7,98 (t +1,57) |
| **NQ 09:30-15:59** | 76,7 % | +3,81 (t +2,53) | +0,91 (t +0,50) | +1,05 (t +0,63) |

Zwei Dinge daran sind stark:

1. **Der Effekt hängt genau am 09:30-Anker.** Nimmt man die 90 Minuten davor dazu, fällt t von 3,87 auf 0,30. Es ist die US-Kassen-Eröffnung, nicht "der Morgen".
2. **NQ hat diesen Effekt nicht** (t 0,50 bis 0,63). Das deckt sich mit dem eigenen Friedhof (#067/#068, ORB-Breakout auf NQ strukturell tot über 2.685 Tage). Es ist also kein Klon einer toten NQ-Idee, sondern ein eigener Mechanismus auf einem Markt, auf dem noch nie ein Trial gerechnet wurde.

---

## 7. ⚠️ KORREKTUR: der Effekt zerfällt NICHT, er ist von Anfang an null

**Das war mein Hauptbefund um Mitternacht, und er war in der falschen Einheit gemessen.** Der `quant-statistician` hat die Einheitenfrage direkt getestet, und das ist die wichtigste Zahl der Nacht. Regression der Brutto-Dollar je Trade auf den BTC-Preis: **Steigung +0,147 $ je 10.000 $ Preis, SE 0,595.**

- Hypothese „die Edge ist in bp konstant" verlangt Steigung +1,750 → **t = −2,70, p = 0,0070, verworfen.**
- Hypothese „die Edge ist in Dollar konstant" verlangt Steigung 0 → t = +0,25, p = 0,80, **nicht verworfen.**

**Die Edge ist in Dollar konstant, nicht in Basispunkten.** Damit *muss* sie in bp fallen, wenn der Preis um Faktor 12 steigt. Mein „Zerfall" war genau dieser Effekt. In Netto-Dollar gemessen ist er nicht signifikant:

| Test | in bp | in Netto-$ |
|---|---|---|
| vor/ab ETF, Welch t | **+2,24** | **+0,28** |
| sup-Wald, Bruchpunkt unbekannt, p | **0,026** | **0,334** |
| Trend je Jahr | −2,66 bp/Jahr (t −1,39) | +0,11 $/Jahr (t +0,14) |
| Split-Half | 24,27 (t 3,19) / 10,74 (t 2,19) | +0,04 (t 0,02) / −0,04 (t −0,01) |

Empirical Bayes über die MBT-Ära 2021 bis 2026: **τ² = 0.** Die Streuung zwischen den Jahren ist zu 100 % Messrauschen, der geschrumpfte Schätzer ist für jedes Jahr derselbe. **Mein dramatisches „2026 netto −10,16 $ je Trade" schrumpft auf +0,99 $.** 2026 hat netto t = −1,73; das schlechteste von zehn reinen Rausch-Jahren ist mit p = 0,35 so schlecht oder schlechter, der Erwartungswert des Minimums von zehn liegt bei −1,54. **2026 ist das normale schlechteste Jahr, kein Sterbefall.** Auch die ETF-Geschichte ist damit nicht „widerlegt", sondern **unentschieden**.

**Was stattdessen gilt, und es ist schlimmer als Zerfall:** der Effekt war nie da, wo es zählt.

> **Netto, ganzes Sample: +0,0004 $ je Trade, CI90 −3,17 bis +3,04, n = 1.906, Profit-Faktor 1,000.**
> **Netto ab MBT-Start 2021: +1,60 $ je Trade, CI90 −2,46 bis +5,73, P(μ > 0) = 75 %.**

Für die gemessene Effektgröße ab 2021 bräuchte man **14.677 Trades, also 58,7 Jahre**, um t = 2 zu erreichen. Das ist nach unserer eigenen Kategorien-Tabelle **`unentscheidbar`**, nicht „Edge" und nicht „tot".

### Die alte Tabelle, zur Dokumentation des Fehlers

BTC 09:30-15:59, OR60, netto je Trade nach 5,20 $ Kosten, 1 MBT:

| Jahr | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|
| brutto bp | +3,3 | +29,6 | +18,4 | +17,7 | +36,8 | +26,6 | +8,7 | +12,0 | **−5,7** |
| t | 0,12 | 1,26 | 1,82 | 1,34 | 2,61 | 2,52 | 0,78 | 1,34 | −0,71 |
| **netto $ je Trade** | −5,66 | −3,21 | −4,35 | **+0,69** | **+6,91** | **+2,35** | **+0,32** | **+5,83** | **−10,16** |

Vor dem US-Spot-ETF-Start (11.01.2024): +24,22 bp, t = +3,86, netto +0,48 $ je Trade. Ab ETF-Start: +5,32 bp, t = +0,94, netto −0,87 $ je Trade. In bp sieht das nach Zerfall aus, in Dollar ist der Unterschied Welch t = +0,28. **Die ETF-Akteursgeschichte ist damit nicht widerlegt, sondern unentschieden** (so hatte ich es um Mitternacht fälschlich geschrieben).

**Asymmetrie, die bleibt:** die Short-Seite trägt den Effekt. OR60 short +21,44 bp (t +3,34) gegen long +13,56 (t +2,13), OR30 short +24,09 (t +3,56) gegen long +10,52 (t +1,43). Passt zur negativen Tagesschiefe von −0,399. **Bewusst nicht als Short-only-Job gebaut:** BTCs Drift war 2025 −10,5 % und 2026 −8,1 % im Jahr, eine Short-only-Variante wäre davon geschmeichelt. Das muss der Nulldrift-Zwilling entscheiden und nicht meine Parameterwahl. Einen `orb_dir`-Schalter habe ich deshalb auch nicht in die Engine gebaut.

**OR-Größe als Filter:** großer Opening Range +22,0 bp und +11,80 $ je Trade (t +2,40), mittlerer praktisch nichts (+9,6 bp, +0,04 $). In bp nicht monoton, in Dollar klar.

---

## 8. Familienwahl: was die Messungen hergeben, und wo ich falsch lag

Meine Wahl um Mitternacht war Trendfolge, Intraday Bias, Mean Reversion. Nach dem Gegenlesen trägt davon **eine**.

| Familie | Urteil | die Zahl, die entscheidet |
|---|---|---|
| **Trend Following** (Bruch am 09:30-Anker) | **trägt, als Einzige** | familienweites p = 0,002 bei 21 Tests, hält Trimmung (t 4,31), hält ohne die 5 besten Tage (t 3,36), 5 von 5 Purged-Folds positiv, NQ hat ihn nicht |
| **Intraday Bias** (Session-Momentum) | **Begründung weg** | t = +2,03 hat familienweit p = 0,32 bis 0,60 und liegt damit *unter* dem Erwartungswert des Maximums von 21 Tests (E[max\|t\|] = 1,84 bis 2,19). Dazu: es ist der Klon eines lebenden Buch-Beins, und NQ hat dort t = +2,53, also mehr als BTC |
| **Mean Reversion** (Umkehr) | **zweifach widerlegt** | ΔHurst gegen NQ +0,009 CI90 [−0,024, +0,036]; konditionierte Form unentscheidbar (MDE 13,2 bis 23,8 $ gegen Kill-Schwelle 5,20 $, Faktor 6,5 bis 21 Daten fehlen) |
| Swing | ausgeschlossen, bestätigt | Flat-Pflicht gegen einen Trend, der erst bei 5 bis 20 Tagen sitzt (VR 1,016 / 1,095). Strukturell, nicht parametrierbar |
| Relative Value | ausgeschlossen, bestätigt | max \|ρ\| über 13 Lags = 0,0081 bei n = 167.931, R² = 0,00007. Statistisch grenzwertig, ökonomisch null |

### Die Struktur-Rechnung, die Mean Reversion erledigt

Der Mathematiker hat die Hüllkurve geliefert, die unsere Regeln für ein `strukturell-tot` verlangen. Die Kostenschwelle zerlegt sich in zwei Teile, und nur einer skaliert mit der Kontraktgröße:

```
K_bp(P) = 2·s·TICK/P·1e4  +  C/(MULT·P)·1e4
        = 2,415 bp Slippage  +  3,864 bp Kommission  =  6,278 bp
```

Der Slippage-Term enthält die Kontraktgröße **nicht** (MBT-Tick und BTC-Tick sind beide 5 Indexpunkte), nur die Kommission verdünnt sich. Und Preis und Prozent-Vola treten nur als Produkt auf, es gibt also genau eine Zustandsgröße: `D$ = MULT · P · R_pct/100`, die Tagesrange eines MBT in Dollar.

Gemessen sättigt der Umkehr-Effekt bei **2,50 bp** (1,08 / 1,99 / 2,50 / 2,49 bp bei 15/30/60/240 Minuten, Steigung 0,27, bei 240 Minuten negativ). Daraus:

- nötig wäre **Preis ab 208.000 $** (heute 82.825, Faktor 2,51 zu wenig), oder
- **MBT-Tagesrange ab 634 $** (heute 253 $, Rekord 364,50 $ in 2025), oder
- **Prozent-Vola ab 7,66 %** bei heutigem Preis (heute 3,05 %)

**Der Gegeneinwand, den der Mathematiker selbst gefunden und dann widerlegt hat:** auf dem großen BTC-Kontrakt kostet derselbe Round-Turn nur 2,49 bis 2,66 bp, die Umkehr-Klasse läge mit 2,50 bp also genau an der Schwelle. Aber eine Einheit BTC voll hat eine Tagesrange von **12.631 $ = 316 % der gesamten Drawdown-Grenze**. Für dasselbe Verhältnis wie bei MBT bräuchte man ein Konto mit rund 7,5 Mio. $ Drawdown. **Das existiert bei keiner Prop-Firma. Der Mechanismus ist echt, der Kontrakt ist falsch, und es gibt keine Größe dazwischen.**

### Die Haltedauer-Mathematik, und warum sie die eigentliche Antwort ist

Weil der Bounce die Sub-Diffusivität vollständig erklärt, ist H ≈ 0,49, die Bewegung wächst also praktisch mit √t. Mit fixen Kosten je Trade folgt geschlossen:

```
n* = [A·(1−H)/c]^(1/H)      t_min = T·(c/A)^(1/H)      (1/H ≈ 2)
```

| Edge-Quelle A (bp je Session) | Optimum n* | Break-even n | Mindest-Haltedauer |
|---|---|---|---|
| ORB60 vor ETF-Start (24,22) | 4,01 | 15,81 | 25 min |
| **ORB60 Vollsample (17,50)** | **2,06** | **8,14** | **48 min** |
| ORB60 ab 2024 (5,88) | 0,22 | 0,87 | **446 min > 390** |

Zwei Dinge daraus, und beide sind hart:
1. **Viele kurze Trades sind arithmetisch ausgeschlossen, nicht nur schlecht.** Schon bei der optimistischen Edge liegt das Optimum bei zwei Trades je Tag. Scalping auf MBT ist keine schlechte Idee, es ist unmöglich.
2. **Bei der ehrlichen Edge ab 2024 ist n\* kleiner als 1.** Das Optimum liegt jenseits eines Handelstages, und die Flat-Pflicht schneidet es ab. Genau das sagt das Varianz-Profil voraus (VR über 1 erst bei 5 bis 20 Tagen). **BTCs Struktur zeigt auf Swing, der Käfig verbietet Swing. Das ist ein Zielkonflikt, keine Parametrierungsfrage.**

### Was ein BTC-Bein überhaupt bringen könnte, und warum AP399 mehr wert ist als die Rechenzeit

Gerechnet mit `tempo_plan` auf der echten Flotte (5 Konten, 4 Beine, k1, Stempel 18.10.):

| m netto je Trade | Reichweite | Monate bis 50.000 $ |
|---|---|---|
| 4 $ | 1 E8-Konto | 189,1 → **185,6 bis 188,1** |
| 4 $ | alle 5 Konten | 189,1 → **172,8 bis 180,1** |
| 6 $ | alle 5 Konten | 189,1 → 165,6 bis 175,9 |

Auf einem Konto sind das +95 bis +180 $ über 36 Monate gegen einen Monte-Carlo-Standardfehler von **383 $**. Also unter dem Rauschen. Umgekehrt gefragt, was es für 10 % weniger Zeit bräuchte:

| Reichweite | nötiges m je Trade |
|---|---|
| 1 E8-Konto | **23,55 bis 44,39 $** |
| alle 5 Konten | **4,71 bis 8,88 $** |

**Das ist die Entscheidung in einer Zeile.** Auf einem Konto bräuchte es das Vier- bis Elffache der optimistischen Annahme. Auf der ganzen Flotte liegt die Schwelle *innerhalb* der Annahme. Und ob die Flotte infrage kommt, hängt an einer einzigen offenen Frage: **darf FFN Krypto?** (AP399). FundedNext darf es nachweislich nicht. **Diese eine Antwort ist mehr wert als jede Rechenzeit, die wir heute Nacht verbrennen könnten.**

### Betriebspunkt: k = 1, nie k = 2

Geschlossen über den Ruin-Exponenten (Cramér-Lundberg, θ = 2μ/σ²), bestätigt per Monte Carlo mit 120.000 Pfaden, Abweichung unter 0,15 pp:

```
θ_j ≥ θ_0   ⟺   m·σ² ≥ μ·(j·s² + 2ρσs)
```

Mit dem gemessenen s ≈ 60 bis 125 $ und ρ = 0,092 ergibt das **m_min(j=1) = 0,82 bis 5,57 $** und **m_min(j=2) = 1,64 bis 8,07 $**. Bei s = 122 und ρ = 0,30 ist `j_max(4 $)` sogar **negativ**, es gäbe dort keine zulässige Größe. Kelly-Diagnose am Buch: k* = 0,670 bei heutiger Vola, das Buch steht mit k1 schon rechts vom Optimum. **„Größe kauft Bust, nicht Tempo" (#106) gilt hier wörtlich.**

**Nulldrift-Pflichtkontrolle, und sie fällt wie erwartet aus:** bei Edge null und j = 3 mit s = 122 sinkt P(pass) um 10,2 pp, **während das Tempo-Maß pass/Tag trotzdem steigt** (3,813 → 4,021). Genau die #106-Falle. Nie auf pass/Tag entscheiden.

**Nebenbefund:** Fat Tails sind hier *nicht* das Problem. Die Kurtosis von 174 steht auf 5-Minuten-Renditen und überlebt die Aggregation auf Tages-PnL nicht (Tages-Kurtosis 5,4). Der RiskGuard-Tagesstopp von 2.500 $ beschneidet die Verlustseite so hart, dass die momenterzeugende Funktion existiert und es keinen Potenzgesetz-Ruin gibt. **Die echte Tail-Gefahr ist die Stop-Durchrutschung bei 4 Kontrakten Volumen je Minute, und die ist in keiner dieser Zahlen enthalten, weil sie nicht gemessen ist.**

### Der `strategy-auditor` hat die Vierer-Auswahl auch noch zerlegt, und er hatte recht

Von meinen vier Jobs fiel einer nach dem anderen. Die beiden Funde, die es entschieden haben:

**Fund 1, der technisch wichtigste: `orb_cutoff_min` steht per Default auf 120.** Ein ORB-Job handelt also nur Brüche bis 11:30 ET, während meine zitierten +17,50 bp Brüche über das ganze Fenster bis 15:49 zählten. Die Ausbruchsminute stand in keiner meiner Dateien, der Job hätte also eine Population getestet, die nie gemessen wurde. **Nachgemessen ist der Schaden klein** (bei OR30 liegen 96 % der Brüche vor 11:30, bei OR60 80 %), aber die Prüfung war nötig und ich hätte sie ohne den Audit nicht gemacht.

**Fund 2, der inhaltlich wichtigste: meine Haltedauer-Mathematik war dieselbe Einheiten-Verwechslung, die ich zwei Abschnitte vorher selbst korrigiert hatte.** Aus „Optimum 2 Trades je Tag" und „Break-even 8" folgt bei 6,40 $ Kosten eindeutig ein Bruttoertrag von 2·√2·6,40 = 18,10 $ je Trade. Gemessen sind 4,33 bis 6,80 $. Was exakt passt: 18,05 bp, als Dollar gelesen. Der Auditor nennt das Muster beim Namen, und er trifft: **Dollar-konstant, wenn es die Zerfallsgeschichte killt, bp-konstant, wenn es die Haltedauer-Rechnung tragfähig aussehen lässt.** Unter der belegten Lesart liegt das Optimum in drei von vier Fällen *unter* einem Trade pro Tag, also bei „nicht handeln".

Damit war auch die Kill-Schwelle unerreichbar: für +5,04 $ netto braucht ein Trade brutto 11,44 bis 14,24 $, das Beste gemessene ist 6,80 $.

### Die entscheidende Nachmessung: mit ehrlichen Kosten ist der nackte Bruch tot

Alles in Netto-Dollar bei 6,40 $ Round-Turn, plus eine Stress-Spalte bei 8,20 $ (5 Ticks je Seite):

| | n | brutto bp | brutto $ | **netto 6,40 $** | netto 8,20 $ | Median | Gewinner |
|---|---|---|---|---|---|---|---|
| OR30, alle Brüche | 2.154 | +16,58 | +4,80 | **−1,60** (t −0,78) | −3,40 | −5,40 | 41,5 % |
| OR60, alle Brüche | 2.111 | +15,50 | +4,72 | **−1,68** (t −0,96) | −3,48 | −5,90 | 39,7 % |

Dazu die Tail-Lotterie, die der Auditor verlangt hat: Gesamtergebnis OR60 **−3.542 $**, aber die fünf besten Trades bringen +2.150 $, die zehn besten +3.695 $, das obere Prozent (21 Trades) +6.670 $. Ohne die Top-5 sind es −2,70 $ je Trade. **Der nackte 09:30-Bruch ist bei ehrlichen Kosten nicht knapp, sondern klar negativ, und was positiv ist, sitzt in 1 % der Trades.**

### Was übrig bleibt: genau eine Zeile, und sie hat einen numerischen Weg

Der Filter auf große Opening Ranges, mit der Engine-Größe `or_size / ATR20(Tagesrange)` statt meiner früheren bp-Variante, Netto-Dollar bei 6,40 $, Block-Bootstrap-CI90:

| Fenster, OR-Länge | Schwelle | n | Tr/Jahr | netto 6,40 $ | CI90 | Stress 8,20 $ | ab 2021 |
|---|---|---|---|---|---|---|---|
| **RTH, OR60** | **0,65** | 344 | 41,2 | **+8,75** (t 1,64) | **[+1,15, +18,42]** | +6,95 | +14,46 |
| **RTH, OR60** | **0,80** | 206 | 24,7 | **+11,69** (t 1,56) | **[+1,87, +23,67]** | +9,89 | +18,73 |
| RTH, OR30 | 0,65 | 137 | 16,1 | −8,09 | [−23,13, +8,10] | −9,89 | −10,59 |
| RTH, OR30 | 0,80 | 64 | 7,5 | −28,42 | [−48,25, −11,20] | −30,22 | −37,19 |
| London, OR60 | jede Stufe | | | **−3,65 bis −22,73** | durchweg negativ | | |

Drei Dinge daran:
1. **Die untere CI-Grenze ist positiv**, es übersteht den Kosten-Stress, und ab 2021 ist es stärker. Das ist der erste Befund der Nacht mit einem echten Weg über die Schwelle.
2. **Aber derselbe Filter dreht auf OR30 ins Negative.** Das ist Vorzeichen-Instabilität über den Nachbarparameter, genau was der Statistiker vorhergesagt hat. Deshalb ist `or_min` im Job eine **Achse** und keine Festlegung: die Instabilität wird gemessen, nicht wegdefiniert.
3. **t liegt bei 1,56 bis 1,78**, also unter dem Vor-Gate von 2,0 und weit unter der Max-t-Decke. Es ist ein Weg, keine Edge.

**Und damit ist auch meine Streichung des London-Fensters sauber belegt**, was sie vorher nicht war: der Auditor hatte zu Recht gerügt, dass mein Streichgrund meine eigene Fehlkonfiguration benannte (R zu klein, weil der Filter fehlte). Mit Filter gerechnet ist London auf **jeder** Stufe negativ, bei Schwelle 0 mit t = −2,45 bis −2,94 signifikant. Das ist jetzt Evidenz.

### Die zwei Jobs, die eingereiht werden

Von 12 Jobs mit 182 Configs auf **2 Jobs mit 24 Configs**. Beide als `BLOCK BTC` in der Hypothesen-Bank, Tag `nightrun_btc_2310`.

| Job | Configs | was er prüft |
|---|---|---|
| **BTC-01** | 12 | Der OR-Größen-Filter. `or_rel_min` 0,5/0,65/0,8 × `or_min` 30/60 × `orb_max_hold` 240/offen, Ausführung `stop_honest`, ein Trade je Tag. `or_min` ist Achse, damit die OR30/OR60-Instabilität gemessen wird |
| **BTC-02** | 12 | **Kontrolle, `book=False`:** dasselbe Grid Config für Config mit `orb_rand_level`, also OR-Grenzen in Zufallsdistanz vom OR-Mittel bei gleicher Größenverteilung (`ctl_random_level`, AP153 P11, #138). Beantwortet die #127-Frage „Level oder Vola-Proxy" an derselben Config |

Der Kontroll-Job ersetzt den zunächst geplanten Fade-Job. Der Auditor hat zu Recht angemerkt, dass meine Begründung dort falsch war: „beide Jobs können nicht gewinnen" stimmt nicht, weil der Fade nur die Teilmenge der Tage handelt, an denen der Preis in die Range zurückkehrt. Zwei verschiedene Teilmengen können problemlos beide verlieren. `orb_rand_level` fragt dasselbe an derselben Population, mit der Hälfte der Configs.

**Erster Hinweis aus dem Vorab-Test, und das ist der beste Befund der Nacht:** eine Einzel-Config durch die echte Engine, mit Stop, bei 6,40 $ Kosten:

| | n | netto je Trade |
|---|---|---|
| BTC-01, Schwelle 0,65, OR60, Halt 240 | 266 | **+7,83 $** |
| BTC-01, Schwelle 0,80, OR60, offen | 156 | **+9,58 $** |
| **BTC-02, Kontrolle mit Zufallsleveln** | 258 | **−2,18 $** |

**Die Kontrolle ist negativ, während das echte Level positiv ist.** Das ist genau die Frage aus #127, und sie fällt diesmal zugunsten des Levels aus. Noch kein Urteil (eine Config, in-sample), aber es macht den Lauf die Box-Zeit wert.

**Vorab festgeschriebene Kill-Schwelle:** Walk-Forward-OOS-Netto **≥ +5,04 $ je Trade** (Buch-Break-even bei σ 97) **und t ≥ 2,8**. Reißt das keine Config, lautet das Urteil `empirisch-nichts-gefunden, N = 24`. **Einschränkung, die der Auditor zu Recht anmerkt: diese Schwelle steht im `note`-Feld, also in Prosa, nicht als Code-Gate.** Sie ist damit eine Selbstbindung und keine Durchsetzung.

**Warnung für morgen früh:** das Vor-Gate ist nicht zu streng, sondern zu **durchlässig**. Bei Edge null passiert eine Config es mit 2,3 %, weil P(Mehrheit der Testjahre positiv) bei μ = 0 schon 0,50 ist. Bei 24 Configs sind das erwartet 0,55 Null-Kandidaten, bei den ursprünglich geplanten 350 wären es 8,1 gewesen. Das ist der Hauptgrund für den kleinen Lauf.

### Die acht Zeilen, die NICHT eingereiht werden, jede mit ihrer Zahl

Max' Auftrag war „alle Strategien der Top 3 Familien einmal durch Gate v4". Ich reihe 4 von 12 ein. Das ist eine Kürzung, und sie gehört offen auf den Tisch, mit der Zahl, die sie trägt. Die Grids liegen fertig in `hypothesen.json` unter `nicht_gebaut` und sind mit einer Zeile einreihbar, wenn Max den vollen Sweep trotzdem will.

| Zeile | Grund | Zahl |
|---|---|---|
| **BTC-MR-01** | strukturell erledigt | Umkehr sättigt bei 2,50 bp gegen 6,40 $ Kosten, an vier Horizonten gemessen. Es gibt keine Haltedauer, bei der sie trägt |
| **BTC-MR-02** | unter jedem Gate, plus Bug im Entwurf | 3,4 Trades im Jahr (n = 30), `min_trades` ist 30. Dazu war `mb_side` nicht gesetzt, der Job hätte die Gegenrichtung nie getestet |
| **BTC-TF-03** | Nenner misst nicht die behauptete Größe | `tm_norm="sigma"` teilt durch die Vortagsstreuung, meine Messung nutzte rollendes Sigma. Die Schwellen hätten z 1–3 getroffen, nicht die belegte Zone z > 3. Kalibrierung −0,30 bis −3,67 $ |
| **BTC-MR-04** | erbt denselben Fehler | identischer Signalpfad, nur `tm_side` gedreht. Kalibrierung −3,77 bis −4,88 $ |
| **BTC-TF-04** | negativ in jeder Zelle, Abgrenzungsgrund weg | −2,33 bis −4,53 $ über fünf Stop-Weiten. Die Frage „Uhrzeit oder Bruch" beantwortet der Fenster-Scan schon: 08:00-Start lässt t von 3,87 auf 0,30 fallen |
| **BTC-IB-02** | negativ in jeder Zelle | −1,79 bis −2,66 $ über vier Stop-Weiten |
| **BTC-IB-03** | negativ in jeder Zelle, Begründung hält MT nicht | −1,96 bis −4,11 $. t = +2,24 hat familienweit p = 0,22 bis 0,41 |
| **BTC-IB-04** | negativ in jeder Zelle | −4,42 bis −5,28 $ über fünf Stop-Weiten. Brutto +11,74 bp liegt über der Kostenschwelle, aber der Stop kostet im London-Fenster rund 9 $ je Trade, weil R dort nur 35 $ ist |

### Die Kalibrierung, die diese Streichungen trägt

Je Hypothese eine Config, nur die Stop- bzw. Filterachse abgefahren. **Der entscheidende Abgleich:** die Brutto-ORB-Messung ergab über das ganze Sample +5,20 $ je Trade gegen 5,20 $ Kosten, also exakt null. Mit Stop wird daraus −2 bis −2,8 $. **Der Stop kostet auf BTC rund 2 bis 2,8 $ je Trade**, weil die Bewegung verrauscht ist und der Stop früher trifft, als die Bewegung trägt. Genau deshalb ist eine Bruttomessung ohne Stop kein Strategie-Ergebnis — und genau diesen Sprung hatte ich um Mitternacht noch gemacht.

Von zwölf Hypothesen hatten zwei eine positive Zelle: der große-OR-Filter mit **+6,08 $ je Trade und +108 $ im Jahr** (aber die Trade-Zahl bricht von 90 auf 18 im Jahr ein) und das Session-Momentum mit **+0,69 $** bei sehr engem Stop. Zum Einordnen: die vier Buch-Beine machen 617 bis 1.305 $ im Jahr. Die beste BTC-Zelle ist ein Zehntel eines schwachen Beins.

---

## 9. Register, Friedhof, Handelbarkeit

**Register: 0 Trials auf BTC oder MBT, je.** Gesamt 70.066 (NQ 37.858, RTY 11.792, ES 8.907, YM 7.987, GC 2.844, CL 188, 6E 36, ZS/ZW je 21, 6B 18). BTC ist unberührt: es gibt kein Friedhofs-Urteil und keine Vorbelastung der Zufallsdecke. Die geplanten Configs heben die Decke um unter einem halben Prozent.

**Handelbarkeit, und das ist eine echte Einschränkung:**
- **E8 erlaubt MBT und MET** (Primärquelle E8-Instrumentenliste, Research-Cache).
- **FundedNext erlaubt kein Krypto** (Primärquelle FN-Hilfe).
- **FFN ungeprüft**, das hängt an **AP399** (Markt-Universum je Prop-Firma, Prio rot).

Ein BTC-Bein liefe also nur auf den E8-Konten, nicht auf der Flotte. Das halbiert den Buch-Nutzen gegenüber einem NQ-Bein und muss in die Wochenend-Rechnung.

**NT8-Port ist kleiner als gedacht:** `MaxBookHost` ist instrumentengesteuert und liest seit 11.10.2026 Configs per Konto **und** Instrument (RtyGap läuft schon auf M2K, nicht auf NQ). Ein BTC-Bein bräuchte damit keinen neuen Modultyp, sondern einen Chart auf MBT, eine Config mit `"instrument": "MBT"` und ein passendes vorhandenes Modul. Offen bleiben: MBT im Feed (E8 läuft über Rithmic bzw. Tradovate), RiskGuard-cfg für das neue Instrument, Handelszeiten-Template für 24/7 und die Zeit-Anker der Module.

**Offene Tickets mit Bezug:** **AP311** (BTC/MBT/MET laden plus Modul `crypto24`, Sprint S2026-42, gelb), **AP399** (Markt-Universum je Prop-Firma, rot), **AP422** und **AP433** (Krypto über CFD-Props).

---

## 10. Geänderte und neue Dateien

Vollständige Liste mit Pfad und Zweck: `C:\Users\Administrator\nightrun_btc\CHANGES.md` (zum Spiegeln auf den PC). **`calendar_fx` wurde wie angesagt nicht angefasst.**

**Nebenbefund ohne Handlung:** beim Import der Hypothesen-Bank meldet `operating_point`, dass `book_state plan.tiers['150k']` veraltet ist (DD 4.500 statt 3.999,90, Preis 390 statt 333,0) und `operating_point.py` gilt. Das ist Bestand und war vor dieser Nacht so. Nicht angefasst, weil das Buch tabu war.
