---
date: 2026-09-19
tags: [projekt, alpha, daten, ninjatrader, neue-maerkte, discovery]
status: aktiv
---

# 🌍 Neue Märkte (NT8-Daten): Plan, Test-Register, Review

Auftrag Max 19.09.2026 (Nacht, Max schläft): NT8-Historie für neue Futures nutzen, Instrumente in Familien einteilen, je Familie die passenden Hypothesen aus der Bank **breit** testen (über die Queue, nicht in der Session), Suchziel **Buch-Nutzen bei möglichst wenig Korrelation** zu den 3 NQ-Beinen, danach den **gesamten Weg reviewen**. Diese Notiz ist die eine Datei, die morgens reicht. Verwandt: [[Daily Notes/2026-09-19]], [[Daily Notes/2026-09-18]] (MGC-Käfigrechnung, „Tageszeit dekorreliert, nicht das Asset"), [[E8-Support-Anfrage (Instrumente GC-CL + Micros)]], [[Discovery-Runner v2]], [[Alpha-Suche]].

> **Freigaben von Max (Rückfrage 06:45):** nach dem Plan voll starten · Engine-Anpassung mit Regressionstest + Runner-Neustart erlaubt · Daten in eigenen Ordner `exported_data_nt8` · Agents sparsam.
> **Harte Grenzen:** nichts ins Live-Buch (`book_state.json` unberührt) · Regression rot = Stopp · NT8 ab Sonntagabend nicht mehr anfassen.

> ## ✅ STAND 19.09. ~17:30 Boxzeit: durchgerechnet und reviewt. **0 Kandidaten fürs Buch.**
> 90 Jobs (GC→MGC 49, CL→MCL 41) liefen 14:42-16:23. Ergebnis, Review-Befunde und das gestempelte Urteil: **Abschnitt 6.2 und 6.3**. Drei Dinge warten auf Max: (1) CL-Filter-Hypothesen mit übersteuerter Prämisse nachrechnen ja/nein, (2) Job-Generator prüfen (Queue ist wieder leer), (3) fehlende Kontrakte nachladen. Details Abschnitt 6.4.

---

## 1. Daten: was da ist

**Quelle:** NT8 auf der Box (Tradovate-Historie), Export per AddOn `MaxBulkExport` (684 Kontrakte, 0 Fehler, 19.09. 06:24-06:54). Rohdaten `Desktop\NT8_Export\<ROOT>\<Kontrakt>.Last.txt` (UTC, Bar-Ende). Continuous gebaut mit `exported_data_nt8\_nt8_to_parquet.py` → `C:\Users\maxlk\Projects\trading-data\exported_data_nt8\<ROOT>_FUT_1m.parquet` im Engine-Format (UTC, **Bar-Anfang**, o/h/l/c/v, **unadjustiert**), Roll je Session nach Volumen-Führung, nur vorwärts. Roll-Protokoll je Markt in `<ROOT>_rolls.json`.

| Markt | Zeitraum | Bars | Rolls | Anmerkung |
|---|---|---|---|---|
| ES / NQ / YM | 12/2015 bis 18.09.2026 | 3,69-3,76 Mio | 42 | 5 Wochen länger als Databento (endet 10.08.) |
| RTY | 07/2017 bis 18.09.2026 | 3,02 Mio | 36 | |
| GC | 12/2015 bis **25.07.2026** | 3,73 Mio | 54 | ⚠️ endet früh, GC 12-26 nicht geladen (nur 1 Tag im Cache) |
| CL | 12/2015 bis **25.07.2026** | 3,72 Mio | 127 | ⚠️ endet früh, CL 09-26 ff. nicht geladen |
| 6E / 6B | 12/2015 bis **14.09.2026** | 3,71 / 3,49 Mio | 42 | Dezember-Kontrakt fehlt |
| ZN / ZB | 12/2015 bis 18.09.2026 | 3,51 / 3,28 Mio | 42 | |
| ZS / ZW | 12/2015 bis 09/2026 | 2,47 / 2,16 Mio | 53 | Tages-Session endet 14:20 ET |
| FDAX | 12/2015 bis 18.09.2026 | 2,76 Mio | 42 | **bei E8 nicht handelbar** (Eurex), nur als Signalgeber denkbar |

**Datenvergleich NT8 gegen Databento** (`exported_data_nt8\_vergleich_databento.json`, Fenster 2016-01 bis 2026-08):

| | ES | NQ | RTY | YM |
|---|---|---|---|---|
| OHLC identisch | 97,0 % | 95,5 % | 97,9 % | 97,5 % |
| Close ≤ 1 Tick | 98,5 % | 97,7 % | 99,0 % | 98,7 % |
| Volumen NT8/Databento (Median, p10, p90) | 1,0 / 1,0 / 1,0 | gleich | gleich | gleich |
| Tagesrendite-Korrelation | 0,9997 | 0,9994 | 0,9998 | 0,9997 |
| Zeit-Versatz | 0 Minuten (Bar-Anfang passt) | | | |

Abweichungen sitzen an den **Roll-Tagen** (anderes Roll-Timing, 31-55 Sessions je Markt) plus ein **2018-Effekt**: ~10 % der Bars (RTH 24 %) weichen um typisch 1 Tick ab (Median 1, p95 3 Ticks), vermutlich anderer Bar-Builder bei NT8 für 2018. Klein, aber dokumentiert. NT8 hat ~450 Mini-Sessions mehr (einzelne Settlement-Bars am Wochenende, 1 Bar), harmlos für RTH-Strategien.

**Buch-Check (3 NQ-Beine, `evaluate_v2`, isolierte Engine-Kopie im Scratchpad):** siehe Abschnitt 6, wird nachgetragen.

---

## 2. Instrument-Steckbriefe (gemessen, `exported_data_nt8\_steckbrief.json`)

US-Fenster 09:30-16:00 ET, letzte 3 Jahre, Median. Käfig-Maßstab: die Buch-Beine laufen auf MNQ (Range 509 $/Tag). Faustregel vom 18.09.: σ_Bein ≈ 0,15 × Tagesrange in $, Buch-Beine liegen bei 73-101 $.

| Markt | Range/Tag | $ Voll | $ Micro | Kosten (2 Ticks / Range) | Anteil Volumen 09:30-16:00 | ρ zu NQ (3 J) | Käfig-Kontrakt |
|---|---|---|---|---|---|---|---|
| NQ (Referenz) | 254 Pkt | 5.090 | **509** | 0,2 % | 79 % | 1,00 | MNQ |
| **GC** | 25,2 $ | 2.515 | **251** | 0,8 % | 50 % | 0,24 | **MGC** |
| **CL** | 1,36 $ | 1.360 | **136** | 1,5 % | 65 % | 0,07 | **MCL** (evtl. 2-3 Stück) |
| **6E** | 0,00375 | **469** | 47 | 2,7 % | 47 % | 0,13 | **6E voll** (Micro zu klein) |
| 6B | 0,00480 | **300** | 30 | 4,2 % | 46 % | 0,29 | 6B voll |
| ZS | 12,75 ct | **638** | – | 3,9 % | 78 % | 0,08 | ZS voll |
| ZW | 10,5 ct | **525** | – | 4,8 % | 81 % | 0,03 | ZW voll |
| ZN | 0,3125 | 312 | – | **10,0 %** | 60 % | 0,05 | nicht handelbar (Kosten) |
| ZB | 0,656 | 656 | – | **9,5 %** | 63 % | 0,14 | nicht handelbar (Kosten) |
| FDAX | 138,5 Pkt | 3.462 | 692 | 0,7 % | 43 % | 0,75 | bei E8 nicht im Angebot |

**Befunde:**
- ⭐ **Nachtest 1 des `verdict-auditor` vom 18.09. ist damit erledigt:** MGC-Tagesrange ist jetzt **gemessen** (251 $ im US-Fenster, σ Open-Close 277 $), nicht mehr geschätzt (50-84 σ_c war die Annahme). MGC liegt bei halber MNQ-Größe, käfigtauglich.
- **Neu gegenüber 18.09.:** bei den ruhigen Märkten passt der **Vollkontrakt** in den Käfig (6E 469 $, ZS 638 $, ZW 525 $, 6B 300 $ Range), „klein schlägt groß" heißt dort nicht automatisch Micro.
- Kostenquote sortiert hart: GC 0,8 % und CL 1,5 % sind tragbar (NQ 0,2 %, ES 1,0 %), 6E/ZS/ZW 2,7-4,8 % nur für seltene, große Moves, ZN/ZB 10 % tot für alles Intraday (deckt sich mit AP140).
- Alle neuen Märkte sind zu NQ praktisch unkorreliert (ρ 0,03-0,29). ⚠️ Lehre vom 18.09. gilt weiter: Vorzeichen-ρ sagt wenig, der **Vola-Kanal** ρ(|PnL|) entscheidet und ist für keinen dieser Märkte gemessen → Pflichtpunkt im Review.
- GC, 6E, 6B handeln die Hälfte ihres Volumens **außerhalb** des US-Fensters (London). Die Engine rechnet RTH 09:30-15:59 ET, das London-Fenster ist damit nur über den `asian`-Modus (volle Session) erreichbar.

---

## 3. Familien-Einteilung (wofür der Markt bekannt ist → welche Hypothesen)

| Markt | Charakter (bekannt für) | Primäre Familie | Sekundär | Prio |
|---|---|---|---|---|
| **GC** | Makro-/Realzins-Trends, Safe-Haven-Schübe, Asia/London-Drift, reagiert auf 08:30-Daten | **Trend Following** | Intraday Bias (Session), Mean Reversion um VWAP | 1 |
| **CL** | stärkster Intraday-Momentum-Markt, Event-getrieben (EIA Mi 10:30 ET), hohe Vola | **Trend Following** (Momentum, ORB, Opening Drive) | Intraday Bias | 2 |
| **6E** | ruhig, Range-lastig, London macht die Richtung, US-Nachmittag läuft aus | **Mean Reversion** | Intraday Bias (Asia/London → US) | 3 |
| **ZS** | Wetter-/USDA-Trends, Re-Open 09:30 ET mit Opening Drive, kurze Tages-Session | **Trend Following** (Opening Drive/ORB) | Swing | 4 |
| **ZW** | wie ZS, volatiler, dünner | Trend Following | Swing | 5 |
| **6B** | wie 6E, etwas volatiler, teurer | Mean Reversion | Intraday Bias | 6 |
| ZN / ZB | Makro-Events, Mean Reversion | – | nur Signalgeber | nicht getestet |
| FDAX | Europa-Vorlauf für US-Open | – | nur Signalgeber | nicht getestet |

**Zuordnung Hypothesen-Bank (143 Hypothesen, 7.402 Configs je Symbol):**

| Block der Bank | Anzahl | GC | CL | 6E | ZS | ZW | 6B |
|---|---|---|---|---|---|---|---|
| Trend Following `tsmom` (TS/TA/TV/TN/TE/TK …) | 48 | ✅ | ✅ | – | ✅ | ✅ | – |
| Trend Following `maband` (AV/AC/AS/AB/AW/AR/AK) | 53 | ✅ | ✅ | – | Auswahl | Auswahl | – |
| Trend Following `ts_reversal` / `orb` | 7 | ✅ | ✅ | – | ✅ | ✅ | – |
| Mean Reversion `tsmom` / `maband` | 8 | ✅ | – | ✅ | – | – | ✅ |
| Intraday Bias (`tsmom`, `maband`, `asian`, `last_hour`) | 10 | ⚠️ falsch markiert, siehe Korrektur unten | ✅ | ✅ | – | – | ✅ |
| Swing `tsmom` | 4 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **bewusst NICHT** | | | | | | | |
| Relative Value `rv` (Index-Paare) | 7 | nein: Paar-Logik ES/NQ/RTY/YM, kein ökonomisches Paar mit Gold/Öl definiert |
| `vix_bias` | 2 | nein: VIX ist Aktien-Vola, kein Why für Gold/Öl/FX |
| Delta/CVD-Hypothesen | 9 | nein: **keine Orderflow-Daten** für die neuen Märkte |
| `cal` (Monatsende/OpEx), `vwap_pullback`-Bein, `xref` | 5 | nein: Aktien-spezifisches Why (Rebalancing, OpEx-Pinning) bzw. Ersatz-Job für ein Bein, das seit 18.09. nicht mehr im Buch ist |

Endgültige Liste je Hypothese × Markt entscheidet der Agent-Durchgang (Abschnitt 5, Story-Check: trägt das **Why** auf diesem Markt?). Das vollständige Register steht in Abschnitt 7.

---

## 4. Was technisch nötig ist (Engine)

| # | Änderung | Datei | Warum |
|---|---|---|---|
| E1 | `POINT_VALUE` / `TICK` / `MICRO_OF` für GC→MGC, CL→MCL, 6E→6E, 6B→6B, ZS→ZS, ZW→ZW | `qbt.py` | sonst `KeyError` (Lehre 136, bewusst kein stiller Default) |
| E2 | Kommission je Kontrakt statt pauschal 1,02 $ (Micro-Wert): Vollkontrakte 6E/6B/ZS/ZW ~4-5 $ RT | `qbt.py` (`COMMISSION_RT`-Tabelle, Default bleibt für Bestand) | sonst Kosten um Faktor 4 zu niedrig |
| E3 | Daten-Fallback: fehlt `<SYM>_FUT_1m.parquet` in `exported_data`, aus `exported_data_nt8` lesen | `qbt.load_rth`, `asian.load_full` | Max' Entscheidung: getrennter Ordner, Databento-Dateien unberührt |
| E4 | Stub-Kontrakte im Loader ignorieren (GC 12-26 / CL 09-26 mit 1 Tag) und Continuous für GC/CL neu bauen | `_nt8_to_parquet.py` | letzter „Roll" springt sonst auf einen 1-Tages-Kontrakt |
| E5 | Multi-Markt-Block in `hypothesis_bank.py`: Klon je Hypothese × Markt (`TS-01@GC`), **%-Schwellen mit dem Vola-Verhältnis skaliert** (GC 0,75 · CL 1,6 · 6E 0,29 · 6B 0,31 · ZS 0,96 · ZW 1,6 gegenüber NQ), `replaces=None`, eigener `tag` `neue_maerkte_0919` zum Rausnehmen | `discovery/hypothesis_bank.py` | Regel „neue Idee = Zeile in der Bank, kein Einzelskript"; NQ-Schwellen (0,3 %) wären auf 6E (0,34 % Tagesrange) sinnlos |
| E6 | ⚠️ **Vorgefundener Fehler:** `hypothesis_bank.py` lässt sich seit 18.09. **nicht mehr importieren** (`AW-11b: replaces='NQ_VWAP-Pullback'` → Bein ist aus dem Buch, Assert wirft). Damit ist `--enqueue` für ALLE Hypothesen blockiert. Fix: AW-11b auf `hold="Bein NQ_VWAP-Pullback seit 18.09.2026 nicht mehr im Buch"` | `discovery/hypothesis_bank.py` | ohne das geht kein einziger Job in die Queue |

Danach: `engine-regression-tester` (Golden Master, Bestands-Zahlen müssen bit-identisch bleiben) → Runner-Neustart über NSSM (`MaxLabDiscovery`) → Dry-Run → `pipeline-auditor` → `--enqueue`.

**Bekannte Risiken, die der Review prüfen muss:**
- **R1 Roll-Sprünge:** Serien sind unadjustiert (wie die Databento-Indizes). GC springt am Roll 30-85 $ (mehr als eine Tagesrange), CL monatlich. Alles, was `prev_close`/Overnight/Gap als Basis nimmt, sieht an Roll-Tagen Schein-Gaps. Prüfung: Ergebnis je Kandidat mit und ohne Roll-Sessions (`<ROOT>_rolls.json`).
- **R2 Session-Fenster:** RTH 09:30-15:59 ET gilt für alle Märkte. ZS/ZW handeln nur bis 14:20 ET (`last_hour` läuft leer), GC/6E haben ihr Hauptgeschehen in London.
- **R3 CL April 2020:** negative Preise, `_drop_corrupt_sessions` verwirft diese Tage (gewollt).
- **R4 Zufallsdecke:** ~30.000 neue Trials auf 17.600 im Register, Decke steigt um grob +5-8 %. Im Review in Zahlen.
- **R5 Vola-Kanal** ρ(|PnL|) zum Buch je Kandidat, nicht nur Vorzeichen-ρ (Lehre 18.09.).
- **R6 2018-Tick-Effekt** in den NT8-Daten.
- **R7 Datenende** GC/CL 25.07.2026, „letzte 3 Jahre"-Gate rechnet dort auf leicht kürzerem Fenster.

---

## 5. Ablauf heute Nacht

1. ✅ Export, Continuous, Datenvergleich, Steckbriefe
2. ⏳ Buch-Check NQ auf NT8-Daten
3. Agents (sparsam): `variant-scout` + `strategy-auditor` als Batch über die Zuordnung Hypothese × Markt (trägt das Why, stimmen die Achsen, welche %-Parameter müssen skaliert werden) → Entscheidungstabelle
4. Engine E1-E6 → `engine-regression-tester` → Runner-Neustart
5. Dry-Run der neuen Jobs → `pipeline-auditor` → `--enqueue` (Prio nach Abschnitt 3: GC, CL zuerst)
6. Überwachen: Heartbeat, Queue-Race-Check nach dem Einreihen, erste Prämissen-Ergebnisse je Markt gegenlesen (stirbt alles aus demselben technischen Grund → Stopp und Ursache suchen statt weiterrechnen lassen)
7. **Gesamt-Review** sobald Ergebnisse da sind: `pipeline-auditor` (Prozess) + `verdict-auditor` (Urteile) + eigene Prüfung R1-R7

---

## 5a. Entscheidung nach dem Agent-Durchgang (19.09. ~07:45)

Zwei Batch-Läufe, beide nur lesend: `variant-scout` (Achsen, Skalierung, Doppelzählung) und `strategy-auditor` (Story). **Beide haben den Umfang gegenüber Abschnitt 3 deutlich gekürzt, und ich bin dem gefolgt.**

**Der Befund, der alles andere schlägt (strategy-auditor):** meine Kostenspalte in Abschnitt 2 war zu günstig (2 Ticks gesamt, ohne Kommission). Ehrlich gerechnet wie `GATES_HARD` (2 Ticks **je Seite** + Kommission, Käfig-Kontrakt):

| | RT-Kosten | % der Tagesrange | × MNQ | nötige Netto-Edge je Trade (100 Tr./J) |
|---|---|---|---|---|
| MNQ | 3,20 $ | 0,63 % | 1,0 | 2,8 % der Range |
| **MGC** | 5,20 $ | 2,07 % | 3,3 | 3,5 % |
| **MCL** | 5,20 $ | 3,82 % | 6,1 | 4,8 % |
| 6E voll | 29,50 $ | 6,29 % | 10,0 | 8,4 % |
| 6B voll | 29,50 $ | 9,83 % | 15,6 | 11,4 % |
| ZS voll | 54,50 $ | 8,54 % | 13,6 | 11,1 % |
| ZW voll | 54,50 $ | 10,38 % | 16,5 | 12,6 % |
| ZN (tot, AP140) | 67,00 $ | 21,47 % | 34,2 | 23,1 % |

6B/ZW liegen damit in derselben Liga wie ZN/ZB, die ich selbst als tot ausgeschlossen hatte → **interner Widerspruch im Plan, korrigiert.** Zahlen sind ein Größenordnungsvergleich des Auditors (eigener Fit), kein Pass/Fail.

**Was daraus folgt:**

| Entscheidung | Grund |
|---|---|
| **Stufe 1 = nur GC (→MGC) und CL (→MCL)** | einzige Märkte mit tragbarem Kosten/Hürde-Profil |
| **6E / 6B zurückgestellt** | 10-16× MNQ-Kosten UND falscher Anker (London 03:00-11:00 ET, Engine kann nur US-Fenster) |
| **ZS / ZW zurückgestellt (Stufe 2)** | einzige Märkte mit echter 09:30-ET-Auktion (Re-Open nach der 08:45-Pause), aber: 13× Kosten, der dazu passende TN-Block hängt an Vortagesschluss (Roll-Falle), und `sigcore.py:483/496/543` rechnet die Pflichtkontrollen hart mit 390 Session-Minuten (ZS/ZW haben ~290) |
| **AV / AC / AW nicht geklont** | reine Filter-Reparametrisierung ohne Akteur, größter Trial-Verbrauch bei kleinstem Erkenntnisgewinn; AW: Session-VWAP ab 09:30 ist für Gold (LBMA-Fix 10:00 ET) der falsche Benchmark |
| **Einzel-Ausschlüsse:** TS-21 (MOC-Auktion), TA-09 (Dealer-Gamma), TV-09 (VIX), TK-03 (2018-Tick-Effekt), AB-13 (Schluss-Anker 15:00), AR-06 (Schwestermarkt nicht geladen) | Akteur bzw. Daten existieren auf dem Markt nicht |
| **alles mit `prev_close` / `prev_rth` / `overnight` ausgeschlossen** | unadjustierte Serien: GC springt am Roll 30-85 $, CL rollt monatlich (~5 % aller Sessions) → Schein-Gaps wären falsch-POSITIV |
| **Korrektur an Abschnitt 3:** Delta ist nicht pauschal tot | nur `tm_delta_src="real"` braucht Orderflow-Daten, der OHLCV-Proxy (Default) läuft überall |

⚠️ **Abweichung von Max' Ansage „ausführlich ALLE passenden Trials":** umgesetzt ist „alle, deren Why auf dem Markt trägt". Den Rest breit zu klonen hätte laut Auditor einen Preis, den Max bei der Ansage nicht kannte: **jeder zusätzliche Trial hebt die Zufallsdecke auch für die laufenden NQ-Kandidaten** (30.000 Trials ≈ +5-8 %). Stufe 1 sind 3.750 Configs (≈ +1 %). Die zurückgestellten Blöcke stehen unten unter NOCH NICHT GEMACHT, einreihbar mit einer Zeile in `NM_MARKETS`, **Entscheidung bei Max.**

**Neuer Mechanismus statt Klon (Idee des Auditors, nicht umgesetzt):** ZS↔ZW und 6E↔6B sind echte ökonomische Paare (gleicher Wetter-/USDA- bzw. USD-Treiber) für den `rv`-Modus, und der GSCI/BCOM-Index-Roll (5.-9. Geschäftstag) ist ein Kalender-Flow mit benennbarem Akteur auf CL/GC. Beides Kandidaten für `alpha-scout` / `familien-scout`.

## 5b. Engine-Stand (19.09. ~08:00)

| # | Status | Was genau |
|---|---|---|
| E1 | ✅ | `qbt.py`: `POINT_VALUE` GC 100 / MGC 10 / CL 1000 / MCL 100 / ZS 50 / ZW 50, `TICK` GC 0,1 / CL 0,01 / ZS, ZW 0,25, `MICRO_OF` GC→MGC, CL→MCL, ZS→ZS, ZW→ZW |
| E2 | ✅ anders gelöst | keine Engine-Änderung nötig: `commission_rt` ist ein Job-Parameter, die Klone setzen 1,6 $ (MGC/MCL, konservativ über MNQ 1,02 $) |
| E3 | ✅ | `qbt.bars_file()`: `exported_data` hat immer Vorrang, Fallback `exported_data_nt8` nur bei fehlender Datei; `load_rth` + `asian.load_full` nutzen ihn |
| E4 | ✅ | Loader ignoriert Kontrakte mit < 5 Sessions; GC zusätzlich am 24.07.2026 gekappt (danach nur noch der auslaufende August-Kontrakt, Dezember fehlt) |
| E5 | ✅ | `hypothesis_bank.py` „BLOCK NM": `_nm_clone_all()`, Hyp-ID `NM-<orig>`, Job-ID `hyp_NM<orig>_<Markt>`, `tag="neue_maerkte_0919"`, Skalierung k = GC 0,746 / CL 1,588 auf `tm_thr` (nur bei `tm_norm=pct`, inkl. Modul-Default 0,003), `rev_thr`, `lh_thr`, `entry_thr`, `mb_thr` (nur bei `mb_norm=none`) |
| E6 | ✅ | fünf Hypothesen mit `replaces="NQ_VWAP-Pullback"` (AW-11b, AW-15b, AW-01, LD-02, EC-03) auf `hold` gesetzt, Bank importiert wieder |
| — | Backups | `qbt.py`, `asian.py`, `discovery/hypothesis_bank.py` jeweils `.bak-20260919-neue-maerkte` (Engine-Ordner ist kein Git-Repo) |

**$-Selbsttest je Markt (Pflichtkontrolle des Auditors), bestanden:** MGC 1 Tick = 1,00 $, Kosten/Trade 0,36 Pkt = 3,60 $ · MCL 1 Tick = 1,00 $, 0,036 Pkt = 3,60 $ · ZS/ZW 1 Tick = 12,50 $, 0,592 Pkt = 29,60 $ · jeweils exakt gleich dem Soll aus Tick × Slippage + Kommission. ZS/ZW haben nach 14:20 ET **0 Bars** (keine Phantom-Füllungen).
**Erster Eindruck aus dem Selbsttest (kein Urteil, 1 unskalierte Config):** Kosten je R liegen bei MGC 11 %, MCL 21 % gegen MNQ 3 %. Das ist die eigentliche Hürde der neuen Märkte.

**Ergebnis Klon-Lauf:** 90 Jobs, 3.750 Configs (GC 49 Jobs / 2.004, CL 41 / 1.746), geschätzt ~10 Box-Stunden. 21 Kombinationen übersprungen (8 Story, 6 Kontroll-Jobs des NQ-Originals, 4 Vortagesschluss-Basis, 3 gemischte Normierung im Grid). Vollständige Liste geklont/übersprungen mit Grund: `exported_data_nt8\_nm_testregister.json`.

## 5c. Pipeline-Audit vor dem Einreihen (19.09. ~08:10-08:30)

`engine-regression-tester`: **grün**, 6 Referenzfälle bit-identisch (NQ_Momentum, NQ_LastHour_v3, RTY_Gap-fade, NQ_Asia-Dir, NQ_VWAP-Pullback, VIX_spike_rev), Kanarien Look-ahead + Zufallssignal wie erwartet gestorben, Marker `regression_ok` 07:27 gesetzt. Einschränkung: 4 weitere Kanarien nicht neu gerechnet (ihre Dateien sind unverändert).

`pipeline-auditor` Runde 1: **STOPP**, vier Blocker. Runde 2 nach Fix: **sauber mit einer Auflage.**

| # | Blocker | Erledigt durch |
|---|---|---|
| 1 | Runner (PID 10212, Start 18.09. 05:25) hat den neuen Code nicht im Speicher → `KeyError` auf GC/CL (Vorfall-Klasse 28.08.) | **offen, Auflage:** Neustart unmittelbar VOR `--enqueue`. `-SyncOnly` unnötig, wir arbeiten direkt im Box-Ordner |
| 2 | `regression_ok` älter als die Änderung | Regressionslauf lief parallel, Marker jetzt jünger als `qbt.py` / `asian.py` / `hypothesis_bank.py` |
| 3 | `controls.ctl_symbols` rechnet einen GC/CL-Kandidaten stumpf gegen den Aktienindex-Korb NQ/ES/RTY/YM (zirkulär oder grundlos rot) | `controls.py`: `if sym_now not in SYMS: return {"ok": None, ...}`; die Kontrolle gilt für GC/CL als **nicht erbracht**, blockt `deploy_ready` nicht hart |
| 4 | `job_generator.mk_job` gibt automatisch gespawnten Folge-Jobs (refine/exits) einen eigenen Tag, die Notbremse `neue_maerkte_0919` hätte sie verloren | `parent_tag` wird durchgereicht; Skalierung und `commission_rt` erbten die Folge-Jobs ohnehin korrekt |

Backups: `controls.py` / `job_generator.py` `.bak-20260919-neue-maerkte`. Für diese zwei Dateien verlangt der Auditor keinen neuen Regressionslauf (früher Return nur außerhalb `SYMS`, Tag ist ein Queue-Metadatum).

**Review-Punkte, die bleiben:** (a) Der Roll-Sprung wirkt auch in rollierenden ATR-/Sigma-Fenstern, nicht nur bei Vortagesschluss-Basis → je Kandidat mit und ohne Roll-Sessions gegenrechnen. (b) `promote_next.py` prüft nicht, ob es für das Symbol überhaupt eine NT8-Strategie gibt; ein MGC/MCL-Kandidat könnte automatisch ins **Next-Week**-Buch (nie ins Live-Buch). Das entspricht Max' Regel „neue Edge sofort ins Next-Week-Buch", ist beim Wochenend-Review aber bewusst anzuschauen: Familie ist vom NQ-Original geerbt, Multi-Markt-Kontrolle fehlt, NinjaScript für MGC/MCL existiert nicht.

**Nebenbefunde:** Das Register steht bei **64.184 Trials** (nicht 17.600 wie in R4 angenommen), 3.750 neue Configs heben die Zufallsdecke damit nur um ~0,5 %. Die Queue ist seit 18.09. leer (3× `queue_empty` in der Inbox, bewusst ungelesen gelassen); ob der Import-Fehler E6 auch den `job_generator` lahmgelegt hat, ist **nicht geprüft**.

---

## 6. Ergebnisse

### 6.1 Buch-Check: die 3 NQ-Beine auf NT8-Daten (19.09. 07:20)

Isolierte Engine-Kopie im Scratchpad (`book_check.py`), `evaluate_v2` mit den Standard-Seeds 11/23/37, `book_state.json` nur gelesen. A = Databento (Referenz), B = NT8 im selben Zeitfenster, C = NT8 bis 18.09.2026.

| | A Databento | B NT8 gleiches Fenster | C NT8 bis 18.09. |
|---|---|---|---|
| Handelstage | 1.580 | 1.577 | 1.592 |
| Momentum: Trades / expR netto | 813 / 0,224 | 810 / 0,229 | 819 / 0,228 |
| LastHour v3: Trades / expR | 976 / 0,099 | 976 / 0,101 | 983 / 0,097 |
| Asia-Dir: Trades / expR | 266 / 0,171 | 267 / 0,167 | 269 / 0,158 |
| **Passquote 25k** (Seeds) | **72,8 %** (73,5 / 72,3 / 72,7) | **74,7 %** (74,9 / 74,4 / 74,6) | **72,6 %** (72,8 / 71,2 / 73,8) |
| Passquote 50k | 87,4 % | 87,9 % | 86,7 % |
| Passquote 100k | 84,8 % | 88,9 % | 87,2 % |

Trade-für-Trade A gegen B: gleiche Richtung in **100 %** der gemeinsamen Trades, Korrelation der Netto-R **1,000**, nur 2 von 2.042 Trades weichen um mehr als 0,25 R ab, 3-7 Handelstage je Bein existieren nur in einer der Quellen (Roll-Tage).

**Lesart:** das Buch ist gegen den Datenquellen-Wechsel robust, die Edge hängt nicht an Databento-Eigenheiten. B liegt 1,8 pp über A, das ist mehr als das Seed-Rauschen (~0,5 pp) und kommt aus den wenigen abweichenden Tagen; C (5 Wochen mehr) liegt wieder auf A-Niveau, die jüngsten Wochen waren also leicht unterdurchschnittlich (Asia-Dir 0,171 → 0,158). **Kein Handlungsbedarf, kein Urteil über das Buch**, reine Datenvalidierung. Die NT8-Daten sind damit für die Engine freigegeben. *(Einschränkung nach Review F4: belegt ist nur die NQ-Quellenrobustheit, GC/CL haben keine zweite Quelle.)*

### 6.2 Discovery-Ergebnisse GC / CL (19.09. 14:42-16:23 Boxzeit)

| | Jobs | an der Prämisse gescheitert | Grid gerechnet | Configs | Survivors | Kandidaten |
|---|---|---|---|---|---|---|
| GC → MGC | 49 | 30 | 19 | 861 | 0 | 0 |
| CL → MCL | 41 | **41** | 0 | 41 (nur Prämissen, 28 verschiedene) | 0 | 0 |

Register 64.184 → 65.035 (**+851**, nicht die geplanten 3.750, weil die Prämissen-Stufe 71 Grids gar nicht erst gestartet hat; Wirkung auf die Zufallsdecke vernachlässigbar). 0 Folge-Jobs vom Generator. Kein Fehler-Job, kein `KeyError`, Queue-Race-Kontrolle ok.

**GC:** expR netto Median −0,063, 16 % der Configs > 0 (151 von 784 mit n ≥ 100 netto positiv). Fail-Gründe (Mehrfachnennung): top5 822 · cost2t 810 · OOS 768 · edge 762 · last3y 726 · IS 493. Typisches Bild: IS positiv, OOS negativ. **4 Near-Misses**, die NUR an `freq` und/oder `top5` scheitern:

| Config | n | $/Jahr (1 MGC) | scheitert an | Roll-Gegenprobe (eigene Messung, 0 neue Trials) |
|---|---|---|---|---|
| NM-TS-13 (`tm_wins_k=2`, thr 0,0037, Fenster 30, Stop 0,8), 2 Varianten | 215 | **434** (Bestwert, besteht edge/IS/OOS/last3y/cost_stress/plateau) | freq 21 < 25 Tr./J, top5 1,21 | Roll-Tage ±2: 10 Trades, +26 $ bzw. −138 $ von 3.822 / 4.537 $ → **kein Roll-Artefakt** |
| NM-TV-02 (Sigma-Quantil-Gate 0,2-0,6), 2 Varianten | 169 / 279 | 164 / 74 | freq, top5 1,7 / 3,2 | Roll-Tage: +327 / +147 $ von 1.707 / 771 $ → kein Roll-Artefakt |

⚠️ **Aber Regime-Artefakt:** bei NM-TS-13 liegen alle fünf besten Tage zwischen 21.10.2025 und 31.03.2026 (30.01.2026 +1.997 $, 29.01. +1.047 $, 20.03. +991 $, 31.03. +766 $, 21.10.2025 +692 $), zusammen ~5.500 $ bei 3.800 $ Gesamtgewinn. Ohne den Gold-Boom 2025/26 ist die Config negativ. Das `top5`-Gate hat hier genau getan, wofür es gebaut wurde (#038).

**CL:** alle 41 Prämissen netto negativ (bester −0,023 R, Median −0,219 R). Brutto je Trade maximal +1,74 $ gegen 3,60 $ Kosten, Median −1,30 $: **CL ist an der Baseline nicht kosten-getötet, da ist brutto nichts.** Fade-/Gegenseite vom `verdict-auditor` nachgerechnet: einziger positiver Fall NM-TE-02 mit +1,27 $/Trade (~66 $/Jahr), unter jedem Gate, Rest ≤ −1,67 $.

### 6.3 Gesamt-Review des Wegs (Pflicht-Abschluss, `verdict-auditor` + `pipeline-auditor` + eigene Prüfung)

**Gestempeltes Urteil (Formulierung des `verdict-auditor`, übernommen):**
> Auf **MGC** tragen die NQ-Intraday-Trend-/MA-Mechaniken im RTH-Fenster 09:30-15:59 ET **keine buchfähige Edge mit ≥ 25 Trades/Jahr**; 812 Grid-Configs, 0 Survivors, die 4 besten scheitern an Frequenz und Tail-Konzentration, **nicht an den Kosten**. Auf **MCL** ist nur belegt, dass das **nackte 15-Min-Momentum ab 09:30 ET brutto ≈ 0 und netto klar negativ** ist; die Filter-, Regime- und Event-Hypothesen sind dort **ungetestet**, weil das Prämissen-Gate sie vor dem Grid abgeräumt hat.

**Was schief lief bzw. korrigiert werden musste:**

| # | Befund | Schwere | Status |
|---|---|---|---|
| F1 | **Mein Urteils-Entwurf war an zwei Stellen falsch:** „beste Dollar-Zahl 164 $/Jahr" (ich hatte nach expR sortiert und NM-TS-13 mit 434 $/Jahr übersehen) und „tragen die Kosten nicht" als Diagnose für GC (GC scheitert an Frequenz/Tail, nur CL hat brutto nichts). Auch „19 verschiedene CL-Prämissen" war falsch, es sind 28. | Urteil | korrigiert, oben steht die geprüfte Fassung |
| F2 | **AP151 P1 hat das CL-Ergebnis entwertet:** 8 Jobs (TA-02, TE-01, TE-14, TV-02, TV-03, TV-07, TV-08, TV-13) starben an EINER identischen Basis-Config (n=546, IS expR −0,158). Bei Filter-Hypothesen steht die These komplett im `grid`, die Prämisse rechnet nur `base`: auf einem Markt ohne Baseline-Edge **kann** so eine Hypothese Stufe 0 nie passieren. Auf GC kamen genau diese Jobs durch, auf CL keiner. EIA-Mittwoch, Panik-Veto, Sigma-Filter, Long-only sind auf CL **ungetestet**. Dazu erbt `NM-TE-06_CL` die bekannte Lint-Lücke des Originals (`tm_dir`). | verfälscht CL (falsch-negativ) | offen, Entscheidung Max (6.4 Punkt 1) |
| F3 | **Der 09:30-Anker begrenzt das GC-Urteil:** 50 % des GC-Volumens liegen außerhalb des RTH-Fensters (COMEX 08:20, Makro 08:30, LBMA-Fix 10:00). Die Engine kann nur RTH + `asian`. Über Gold außerhalb des US-Kassa-Fensters ist **nichts** belegt. | Reichweite | offen, Engine-Ticket |
| F4 | **„NT8-Daten für die Engine freigegeben" (6.1) war zu weit gestempelt.** Belegt ist: das NQ-Buch ist quellenrobust. GC/CL haben keine zweite Quelle, ihre Datenqualität ist ungeprüft (nur Plausibilität: Median 390 RTH-Bars/Tag, keine verdeckten Lücken in der GC-Stichprobe). | Stempel | in 6.1 so zu lesen, Satz bleibt mit dieser Einschränkung |
| F5 | **Methodische Warnung aus 6.1:** der reine Datenquellen-Wechsel bewegt die 25k-Passquote um **1,8 pp** (72,8 → 74,7), das ist mehr als unsere eigene Annahme-Schwelle von 1,5 pp für ein neues Bein. | Pipeline | ins Logbuch #165 |
| F6 | Meine Kostenquote je R war für MGC ~25 % zu pessimistisch: gemessen MGC **0,085 R** (p10-p90 0,045-0,144), MCL **0,180 R**, MNQ 0,034 R. Verhältnis real 2,5× / 5,3× statt 3,7× / 7×. Die Kostenannahme selbst (1,60 $ + 1 Tick/Seite) ist konservativ, aber fair; Slippage ist 55 % der Kosten. | Zahl | korrigiert |
| F7 | Plan schätzte 3.750 Configs / ~10 h, real 902 Configs / 1 h 41 min. | Doku | korrigiert |
| F8 | **Job-Generator:** Inbox zeigt 10× `queue_empty` seit 14.09. 21:18, also schon VOR dem Import-Fehler E6 (18.09.). Nach dem NM-Batch ist die Queue wieder leer (1.004 Jobs, 0 pending), ohne neuen Nachschub. Ob E6 den Generator zusätzlich lahmgelegt hatte, ist weiter unbewiesen. **Nicht von dieser Aktion verursacht, aber aufgedeckt.** | Bestand | offen, nächster Generator-Takt ~01:40 Boxzeit |

**Geprüft und sauber:** Skalierung k = 0,746 / 1,588 in den gerechneten Configs drin, keine unskalierte %-Schwelle in verschachtelten `exit_profile` / `confirm`-Dicts · `top5_share` > 1 ist korrekte Arithmetik bei winzigem Gesamtgewinn, kein Punktwert-Fehler · kein eigenes Dollar-Gate aktiv (`usd_per_year_min=0`) · Kosten laufen über den Micro-Punktwert (`meta.json`: `commission_rt=1.6`, Symbol korrekt) · `book_state.json`, `book_state_next.json`, `portfolio.json` unverändert · keine verwaisten Queue-Jobs durch die 5 `hold`-Hypothesen · 2018-Tick-Effekt im Buch-Check implizit mitgetestet, unauffällig · Roll-Gegenprobe R1 für die Near-Misses negativ (kein Artefakt).

**Von den Prüfern ausdrücklich NICHT geprüft:** Vola-Kanal ρ(|PnL|) zum Buch (R5, mangels Kandidat gegenstandslos), Roll-Termine je Roll gegen Volumen-Führung, CL-Datenvollständigkeit (nur GC gestichprobt), direkter `qbt.run_strategy`-Gegencheck eines Discovery-Werts (von mir vor dem Einreihen an 4 Jobs gemacht), Zähllogik des Registers auf Config-Ebene.

**Darf NICHT als „tot" ins Logbuch oder `ideas.json`:** „Gold/Öl tot" · TV-02/03/05/07/08/13, TE-01/02/14, TA-02 auf CL (Status: nicht getestet, Prämissen-Sperre) · alles außerhalb des RTH-Fensters · AV/AC/AW · 6E/6B/ZS/ZW (nie gerechnet). **Geprüft tot:** die 19 GC-Grids im RTH-Fenster und die CL-Fade-Seite.

### 6.4 Was jetzt bei Max liegt

**Als Tickets angelegt (19.09., `tasks.json` auf der Box, Backup `.bak-20260919-neue-maerkte`):** AP194 🟠 Job-Generator / leere Queue · AP195 🟠 CL-Nachtest + Lint-Assert · AP196 🟡 NT8-Daten nachladen/erweitern/Tick · AP197 🟡 Session-Fenster je Markt + `sigcore` 390 · AP198 🟡 **Überthema**: alles nie Gerechnete (6E/6B, ZS/ZW, AV/AC/AW), neue Mechanismen, Multi-Markt-Korb, `promote_next`-Check, Vola-Kanal · AP199 🟡 Datenquelle NT8 vs Databento + 1,8-pp-Quellenrauschen · AP200 🟢 Aufräumen. AP140 (Gold/CL ins Universum) auf „teilweise erledigt" mit Verweis.

1. **CL-Nachtest ja/nein** (Vorschlag `verdict-auditor`, billig: ~600 Configs, ~1 Box-Stunde, +0,9 % Zufallsdecke): TV-02, TV-03, TV-13, TE-14, TE-15, TS-15 auf CL mit übersteuerter Prämisse neu einreihen, damit das Grid läuft. Geht nicht ohne Eingriff: `prem_min_edge_pp` erlaubt `H()` heute nur für Kontroll-Jobs (`book=False`). Bewusst nicht selbst gemacht, das ist eine Gate-Lockerung.
2. **Job-Generator prüfen** (F8): produziert er wieder Jobs? Wenn nein, `alpha-scout` einschalten (Regel „Queue darf nie leerlaufen").
3. **Nachladen in NT8:** GC 12-26, CL 09-26 ff., 6E/6B 12-26 (Daten enden sonst 24.07. / 21.07. / 14.09.).
4. **Engine-Ticket:** eigenes Session-Fenster je Markt (GC 08:20/08:30 ET, 6E London), sonst bleibt jede Aussage über diese Märkte auf das US-Kassa-Fenster beschränkt. Dazu `sigcore` 390-Minuten-Annahme (ZS/ZW).
5. **Pipeline-Vorschläge des Auditors:** `_lint_thesis_premise` für NEUE Hypothesen/Klone als Assert statt Warnung · eigenes Inbox-Ereignis `job_generator_dead` · Register-Zähl-Selbsttest.
6. **Zurückgestellt, unverändert:** 6E/6B, ZS/ZW, AV/AC/AW auf GC/CL, neue Mechanismen (`rv` ZS↔ZW / 6E↔6B, GSCI/BCOM-Roll).
7. Offen aus dem Vormittag: `_staging`-Ordner aufräumen.


---

## 7. Test-Register: GEMACHT / NOCH NICHT GEMACHT

### ✅ GEMACHT

| Wann (Boxzeit) | Was | Wo / womit | Ergebnis |
|---|---|---|---|
| 19.09. 06:18 | AddOn `MaxBulkExport` deployt | `bin\Custom\AddOns\MaxBulkExport.cs`, Backup `_bak_archiv\deploy-20260919-0618` | Build 0 Fehler, `ninja-coder`-Review eingearbeitet |
| 06:23 | TEST-Export GC 02-16/02-17 gegen manuellen Export | `Desktop\NT8_Export_TEST` | 0 Abweichungen in 90.640 Bars |
| 06:24-06:54 | Vollexport 684 Kontrakte, 20 Roots | `Desktop\NT8_Export` | ok=684 fail=0 |
| 06:56 | Continuous 13 Märkte | `exported_data_nt8\*_FUT_1m.parquet`, `*_rolls.json`, `_summary.json` | siehe Abschnitt 1 |
| 07:00 | Datenvergleich ES/NQ/RTY/YM | `_vergleich_databento.json` | 95,5-97,9 % identisch, Versatz 0 |
| 07:02 | 2018-Abweichung NQ untersucht | ad hoc | 1-Tick-Effekt, Roll-Tage, kein Strukturfehler |
| 07:05 | Steckbriefe 13 Märkte | `_steckbrief.py` / `_steckbrief.json` | Abschnitt 2 |
| 07:10 | Hypothesen-Bank inventarisiert (in-memory, Datei unverändert) | ad hoc | 143 Hypothesen, Import-Fehler AW-11b gefunden (E6) |
| 07:20 | Buch-Check NQ: Databento vs NT8 | Scratchpad `book_check.py`, isolierte Engine-Kopie | Abschnitt 6.1, trade-identisch |
| 07:25 | Loader-Fix Stub-Kontrakte, GC/CL/6E/6B neu gebaut, GC am 24.07. gekappt | `_nt8_to_parquet.py` | E4 |
| 07:30-07:45 | `variant-scout` + `strategy-auditor` Batch | nur lesend | Abschnitt 5a |
| 07:50 | Engine E1/E3/E5/E6 | `qbt.py`, `asian.py`, `hypothesis_bank.py` (+ Backups) | Abschnitt 5b |
| 07:55 | $-Selbsttest GC/CL/ZS/ZW + Prämissen-Probelauf 4 NM-Jobs | ad hoc | Kosten exakt, Pipeline läuft Ende-zu-Ende |
| 08:00-08:30 | `engine-regression-tester` + `pipeline-auditor` (2 Runden), Fix Blocker 3+4 | `controls.py`, `job_generator.py` (+ Backups) | Abschnitt 5c |
| 14:38-14:45 | Freigabe Max, `pipeline_ok`, Runner-Neustart (PID 444), `--enqueue` 90 Jobs, Laufzeit-Kontrolle | `discovery/queue.json` | 90 pending → läuft sauber |
| 14:42-16:23 | 90 Jobs gerechnet | `discovery\results\hyp_NM*_GC.json` / `_CL.json` | 0 Survivors, 0 Kandidaten (6.2) |
| 16:40 | eigene Auswertung Fail-Gründe + beste Configs | ad hoc aus `results` | Entwurf, vom Auditor in 3 Punkten korrigiert (F1) |
| 16:45-17:20 | Gesamt-Review `verdict-auditor` + `pipeline-auditor` | nur lesend | 6.3 |
| 17:10 | Roll-Gegenprobe der 4 GC-Near-Misses | `qbt.run_strategy` + `GC_rolls.json`, 0 neue Trials | kein Roll-Artefakt, aber Regime-Klumpen 10/2025-03/2026 |
| 08:30 | Prüfung: `--enqueue` würde exakt 90 NM-Jobs hinzufügen, 0 andere | Queue nur gelesen | ID-Liste `exported_data_nt8\_nm_only.txt` |

### ⚠️ Korrektur 22.09.2026 (backtest-runner-Check)

Die Zeile „Intraday Bias (tsmom, maband, asian, last_hour) | 10 | GC ✅" in Abschnitt 3 ist **falsch dokumentiert**. Geprüft anhand `exported_data_nt8\_nm_testregister.json` + `discovery\queue.json` + `discovery\results\hyp_NM*_GC.meta.json`: alle 49 GC-Jobs sind Trend-Following (`maband`/`tsmom`/`ts_reversal`), auch die NM-AS-/NM-AB-/NM-AK-/NM-AR-Präfixe (MA-Band-/Donchian-Varianten der Trend-Familie, kein `engine/asian.py`). **Kein einziger GC-Job mit Modus `drift`/`fade_us`/`break_us`/`us_dir` (die eigentlichen `asian.py`-Muster) existiert.** Die 4 Asian/London-Session-Muster auf GC stehen also weiterhin komplett aus — echte Buch-Lücke, nicht nur zurückgestellt.

### ⬜ NOCH NICHT GEMACHT

| Was | Warum offen |
|---|---|
| CL-Filter-/Event-Hypothesen mit übersteuerter Prämisse (TV-02/03/13, TE-14/15, TS-15) | Prämissen-Sperre AP151 P1, wäre eine Gate-Lockerung → Entscheidung Max (6.4) |
| Job-Generator lebt wieder? | Queue nach dem Batch erneut leer, nächster Takt ~01:40 Boxzeit |
| Vola-Kanal ρ(|PnL|) neuer Märkte zum Buch (R5) | kein Kandidat, an dem man ihn messen könnte |
| 6E / 6B klonen | zurückgestellt: Kosten 10-16× MNQ, London-Anker fehlt in der Engine, Entscheidung Max |
| ZS / ZW klonen (Stufe 2: nur TN + ORB) | zurückgestellt: Kosten 13×, Roll-Falle im TN-Block, `sigcore` rechnet Pflichtkontrollen hart mit 390 Minuten |
| AV / AC / AW auf GC/CL | bewusst ausgelassen (Reparametrisierung ohne Akteur), einreihbar über `NM_MARKETS[...]['blocks']` |
| Multi-Markt-Kontrolle für Rohstoffe (Vergleichskorb z.B. GC↔SI, CL↔NG) | Schwestermärkte nicht geladen |
| neue Mechanismen: `rv` ZS↔ZW / 6E↔6B, GSCI/BCOM-Index-Roll | Idee des Auditors, braucht `alpha-scout` / `familien-scout` |
| Gesamt-Review R1-R7 | wenn Ergebnisse da sind |
| **Tick-Daten** | Test GC 02-16/02-17 kam leer zurück, alte Tick-Historie über Tradovate vermutlich nicht verfügbar |
| **GC 12-26, CL 09-26 ff., 6E/6B 12-26 nachladen** | braucht Max im NT8 (Historical Data → Load), Daten enden sonst 25.07. bzw. 14.09. |
| ZN / ZB als handelbares Instrument | Kosten 10 % der Range, bewusst ausgelassen; als Signalgeber (Zins-Kontext) später denkbar |
| FDAX | bei E8 nicht handelbar; als Vorlauf-Signal für den US-Open später denkbar |
| London-Fenster für GC/6E/6B (eigenes Session-Fenster in der Engine) | Engine kennt nur RTH 09:30-15:59 + `asian`; größerer Umbau, nicht heute Nacht |
| Micros MGC/MCL/M2K/MES/MNQ/MYM/MBT aus dem Export | nur 1-4 Kontrakte Historie, preisgleich zum großen Kontrakt, kein Mehrwert |
| SI, HG, NG, 6J, ZC (bei E8 handelbar, nicht geladen) | Max hat sie nicht heruntergeladen; Kandidaten für die nächste Lade-Runde |
| RV/VIX/Delta/Kalender-Hypothesen auf neuen Märkten | siehe Abschnitt 3, kein Why bzw. keine Daten |
| Databento-Dateien durch NT8 ersetzen / verlängern (5 Wochen mehr Historie) | Entscheidung bei Max nach dem Buch-Check |
| `_staging`-Ordner mit 5 alten Strategie-Dateien aufräumen | Entscheidung bei Max |
