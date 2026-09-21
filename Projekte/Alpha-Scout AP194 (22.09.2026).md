---
tags:
  - projekt/discovery
  - alpha-suche
erstellt: 2026-09-22
status: Entscheidung Max (AP211)
---
> [!info] Bericht des alpha-scout zu Ticket AP194 (Queue leer, Generator ausgereizt). Entscheidungen: AP211. Rechnen/Vorzählungs-Skripte (cnt1-cnt8) lagen im Session-Scratchpad und sind nicht abgelegt; Zählwerte stehen im Bericht. Bezug: [[Alpha-Suche]], [[Strategie-Logbuch]] #165, #169, #170.

# Alpha-Scout AP194 (22.09.2026): Queue leer, Vorlagen-Welt ausgereizt, was kommt danach?

Auftrag: gerankte Liste queue-fertiger Jobs mit Why vorab (mind. 8), nur NEUE Mechanismen. Nicht angefasst: RVOL, ADX, ADX x VWAP, Overnight-Bias ORB (Globex-Form, London-ORB, Nacht als Tor). Nichts geschrieben in `hypothesis_bank.py`, Queue, Bank-Notizen, `jobs_proposed/`. Kein Research-Cache-Eintrag (siehe Abschnitt 7).

## 0. Das Ergebnis in vier Sätzen

1. Ich habe 12 neue Kandidaten **vorgemessen, bevor ich einen Job schreibe** (Zählung: Trades/Jahr und mittlere gerichtete Bewegung in Punkten bzw. $ je Micro, ohne Stops und Kosten, **0 Register-Trials**, Skripte `cnt1.py` bis `cnt8.py` im Scratchpad). Methode gegen das bekannte Buch-Bein geeicht: Asia-Dir NQ thr 0,8 liefert 25 Trades/Jahr und +12,5 Pkt brutto (Register: 266 Trades in 10 Jahren), Momentum NQ 76 Trades/Jahr, +14,2 Pkt, t = 2,24.
2. **Kein Kandidat mit vorhandenem `mode` und vorhandenen Daten überlebt die Zählung** (brutto unter 3x Kosten, t unter 2, oder Trades/Jahr unter der 25er-Hürde). Ich lege deshalb keinen Job zum Einreihen vor, sondern drei optionale Low-Prior-Jobs (Abschnitt 3) und eine Empfehlung, sie nur als Abdeckungs-Abschluss laufen zu lassen.
3. Der einzige Raum mit echtem Informationsgewinn ist ein **neuer Markt mit eigener Uhr und dokumentiertem Intraday-Momentum: Bitcoin (CME BTC/MBT/MET)**. Er ist blockiert (Daten + Session-Modul), Plan und Zählung-zuerst-Ablauf stehen in Abschnitt 4.
4. Die Karten-Wege (Fibonacci, Rundzahlen, Session Momentum, ES-NQ) haben **keinen** ein-weg-fertigen Weg ohne Job mehr, der auch nur eine offene Prämisse trägt (Abschnitt 5).

## 1. Inventar in 5 Zeilen

1. Register 65.035 Trials: `tsmom` 39.846, `maband` 16.755, Rest klein (`ts_reversal` 1.118, `rv` 739, `i2` 547, `last_hour` 463, `gap` 397, `asian` 298, `cal` 200, `orb` 184, `vwap_pullback` 155, `vix_bias` 73). Symbole NQ 35.848, RTY 11.583, ES 8.503, YM 7.892, GC 823, CL 28.
2. Queue 1.004 Jobs: 504 done, 500 premise_failed, 0 pending. Letzter Kandidat 21.08.2026. Generator: 426 Abdeckungs-Schlüssel, 504 followed, Dry-Run 0. Letzte Handjobs (XD-12, AC-06d x4, SES-W16a/W42a, NM-Klone GC/CL): alle 0 Kandidaten bzw. premise_failed.
3. Nie im Register: `tm_dgs*`/`tm_dxy*`/`tm_dix*` (Modul B seit 18.09. gebaut, 0 Trials), `asian` auf Nicht-Index-Märkten, EIA-Tag auf CL, Bitcoin, Same-Time-of-Day (Modul D fehlt).
4. Friedhof-Regeln, die jeden Vorschlag begrenzen: Bein-dazu braucht bei rho 0,2 rund 1.811 $/Jahr je Kontrakt (#158), Hürden 812/1.299/2.078 $ (Lehre 161), Gates auf Buch-Beine ohne Kandidat (AR-15/17, XD-12), Zählung vor Job (Lehre ADX-W36), Klein-N-Event-Edges unter der $-Hürde (C2).
5. Daten: NQ/ES/RTY/YM 1m+1d, VIX, DGS2/DGS10, DTWEXBGS, DIX/GEX; NT8-Continuous GC, CL, 6E, 6B, ZN, ZB, ZS, ZW, FDAX bis 07-09/2026 (`exported_data_nt8`). E8 bestätigt handelbar: GC, CL, SI, NG, HG, 6x, ZN/ZB, Getreide, MBT/MET (Cache 09.09.), keine News-Sperre, Zwangsglättung 16:10 ET.

## 2. Ranking nach Informationsgewinn (inkl. Vormessung)

Informationsgewinn = wie viel eine Rechenrunde an Wissen liefert, das wir nicht schon per Zählung haben. Rechte Spalte: was ich empfehle.

| Rang | ID | Mechanismus (Edge-Quelle) | Markt | Baubarkeit | Vormessung (0 Trials) | Empfehlung |
|---|---|---|---|---|---|---|
| 1 | BTC-01 | Intraday-Momentum in 24/7-Markt, erste Hoch-Volumen-Session (Risk-Premium/Behavioral) | MBT/BTC CME | Daten fehlen + Session-Modul | nicht messbar | **Daten-Runde vorbereiten** (Abschnitt 4) |
| 2 | GCUHR-01 | Buch-Mechanismus Asia-Dir/Opening-Drive auf der COMEX-Uhr (08:20) statt 09:30 (F3-Lücke, AP197) | GC | `asian` us_dir, sofort | London-Richtung thr 0,8: 22 Tr/J, +9,1 $/Micro brutto (Kosten 3,6 bis 5,2 $), t 1,15. COMEX-1. Stunde thr 0,8: 26 Tr/J, +1,3 $. thr 0,5: 104-110 Tr/J, +2,8 $ | optional, Prior sehr niedrig (Abschnitt 3) |
| 3 | MAKRO-01 | Zins-/Dollar-Regime als Gate auf Opening-Drive (Informational, Diskontsatz-Kanal) | NQ | `tsmom` + `tm_dgs10_chg5`, `tm_dxy_chg5` | Terzile der 5-Tages-Änderung: alle positiv (t 0,5 bis 2,2), Spreizung 14 Pkt bei se 15,6; MDE rund 43 Pkt, nicht auflösbar | optional als Abschluss des Vorrats "macro_gate" (AP61 direkt negativ, Gate-Rolle nie gerechnet) |
| 4 | CLEIA-01 | EIA-Mittwoch 10:30, Reaktion 10:30-10:40 trägt (Structural) | CL | `tsmom` + `tm_dow=[2]`, sofort | 28-43 Tr/J, brutto 3,4-5,5 $/MCL (Kosten 3,6-5,2 $), t 1,3-1,8, **Kontrolle Nicht-Mittwoch identisch 4,7 $** | optional (schließt AP195 sauber), Prior sehr niedrig |
| 5 | GCZINS-01 | Gold-Momentum invertiert in Zins-Schock-Wochen (Lead aus Zählung) | GC | `tsmom` + `tm_dgs10_chg5_min` | oberstes Terzil 10Y: -3,7 Pkt (t -2,2), 2Y: -3,8 (t -2,3), aber n 156-165 = **15 Tr/J**, 6 Tests, post hoc | **kein Job** (min_tpy 25 unerreichbar), höchstens ein vorregistrierter Einzeltest |
| 6 | ANN-01 | Ankündigungsprämie: Long nur an Makro-Tagen (Risk-Premium, Savor/Wilson) | NQ/ES | `tm_news_only` fehlt (10 Zeilen) | News-Tage NQ +3,4 bp, sonst +2,9 bp (Diff +0,5, t 0,09); ES -2,3 vs +3,3 bp (t -1,24) | **verworfen**, nicht bauen |
| 7 | TOD-01 | Same-Time-of-Day-Kontinuation (Heston/Korajczyk/Sadka 2010, Cache Z.525) | NQ | Modul D fehlt | 13 Halbstunden-Fenster x K 5/10/20: Mittel -0,6 bis +0,04 Pkt, bestes Fenster +1,4 Pkt (Kosten 2 Pkt) | **verworfen**, Modul D nicht bauen |
| 8 | CLV-01 | Vortags-Schlusslage in der Tagesrange als Bias/Gate | NQ | neue ctx-Spalte | 5 Quintile: kein monotoner Verlauf (+15,3 / -2,3 / 0,0 / -5,0 / +0,6 Pkt), Momentum gleich/gegen 7,4 vs 21,0 (t der Diff ca. 1,1) | **verworfen** |
| 9 | LON-01 | Asia-Richtung setzt sich im London-Fenster 03:00-08:25 fort (andere Uhr als alle Beine) | NQ | `asian` us_dir | thr 0,8: 24 Tr/J, **-2,8 Pkt** (Fade-Richtung +0,4 bis 2,8 Pkt < Kosten) | **verworfen** |
| 10 | FX-01 | London-Richtung 03:00-08:00 setzt sich bis 12:00 fort | 6E | `asian` us_dir, 6E fehlt in `qbt.POINT_VALUE` | t -0,95 bis +0,17 in allen Schwellen | **verworfen** (dazu Kosten 10x MNQ) |
| 11 | EFADE-01 | Eröffnungsbewegung wird gefadet (RTY mean-revertiert intraday) | RTY/YM/ES | `ts_reversal`/`tsmom` | RTY \|Fade\| <= 0,7 Pkt; YM Fade +4,7 bis 11,3 Pkt = 2,4 bis 5,7 $/MYM, t 0,5-0,7, 42 Tr/J => rund 155 $/Jahr; ES <= 1,4 Pkt | **verworfen** |
| 12 | POIL-01 | NYMEX-Pit-Eröffnung 09:00, Richtung der ersten Stunde | CL | `asian` us_dir | thr 0,8: 25 Tr/J, +5,0 $/MCL brutto (Kosten 3,6-5,2 $) | **verworfen** |

Lesart: 3 Zeilen (2, 3, 4) sind Abdeckungs-Abschlüsse mit sehr niedrigem Prior. Zeile 1 ist die einzige mit strategischem Informationsgewinn. Zeilen 6-12 sind mit Zahl beantwortet, Box-Zeit dafür wäre verschenkt, und jede würde die Zufallsdecke minimal heben. Wichtig für die Stempel: das ist eine **Zählung ohne Stops/Kosten/OOS, kein Tot-Stempel**. Den Stempel vergibt der `verdict-auditor`; die Zahlen stehen aber so, dass er in einem Schritt entscheiden kann. Grenzfall ehrlich benannt: Zählung nutzt Exit am Fensterende (bei GC/CL/6E die `asian`-Semantik `tr_end`), der Engine-Lauf könnte durch Stops das Tail-Profil verändern, die Größenordnung nicht.

## 3. Drei optionale Jobs (nur als Abdeckungs-Abschluss, Prior sehr niedrig)

Gemeinsam: keine `gates`-Felder eingefroren (Runde-10-Auflage), `book_marginal: true`, `commission_rt: 1.6` wie die NM-Klone, Prämisse trägt die echte These (nicht die Basis, Lehre AP151 P1). Vor dem Einreihen: `variant-scout` + `strategy-auditor` (ein-weg), `pipeline-auditor` (Wirksamkeitsprobe: Gate-Config muss weniger Trades liefern als die Basis, weil `tsmom.DEFAULTS` `tm_dgs*`/`tm_dxy*` nicht kennt, nur `controls.GATE_OFF`).

### 3.1 GCUHR-01 `gcclk01_comex_dir_GC` (Rang 2)

- **Mechanismus:** das Buch-Bein NQ_Asia-Dir-USopen (Richtung der Vorsession setzt sich ab dem Cash-Open fort) auf der Uhr des Marktes, an dem es gehandelt wird. Gold hat sein Hauptgeschäft in London (03:00-08:15 ET) und am COMEX-Open 08:20 mit den 08:30-Daten; der 09:30-Anker aus #165 ist dort der falsche (Lehre 6 in #165, F3, AP197).
- **Why:** Weil physische Käufer und Zentralbanken in London ihre Aufträge über Stunden staffeln und das COMEX-Buch am Open auf dieselbe Richtung trifft, neigt GC dazu, eine klare London-Richtung (Bewegung >= 0,8x Range) ab 08:20 bis zum COMEX-Settlement fortzusetzen. Prüfbar: mittlere gerichtete Bewegung 08:20 bis 13:25 > 3x Kosten und schlägt `tm_null`. Verwerfen wenn: n < 100 in 10 Jahren, Edge nur im Gold-Boom 10/2025-03/2026 (top5), oder Nulldrift gleichauf. Erwartete Edge laut Zählung 9 $/Micro (0,9 Pkt) bei 22 Tr/J, also **unter der 25er-Frequenzhürde und unter 3x Kosten**: der Job stirbt sehr wahrscheinlich an der Prämisse. Familie Intraday Bias.
- **Quelle:** Cache Z.769 (London PM Fix als Zwangshandel, Caminschi/Heaney 2014 JFM: Effekt nur in den ersten 4 Minuten, deshalb kein 1m-Signal), Buch-Bein als Vorbild.
- **Spec:**
```json
{"id":"gcclk01_comex_dir_GC","type":"grid","priority":55,"symbol":"GC","family":"Intraday Bias",
 "base":{"mode":"asian","symbol":"GC","asia_mode":"us_dir","rs_start":"03:00","rs_end":"08:15","tr_start":"08:20","tr_end":"13:25","asia_dir_thr":0.8,"asia_stop_mult":0.5,"asia_target_mult":null,"commission_rt":1.6},
 "grid":{"segment":[{"_label":"london_to_comex","rs_start":"03:00","rs_end":"08:15","tr_start":"08:20"},
                    {"_label":"comex_1h_drive","rs_start":"08:20","rs_end":"09:20","tr_start":"09:20"}],
         "asia_dir_thr":[0.5,0.8],"asia_stop_mult":[0.5,0.75],"asia_target_mult":[null,2.0]},
 "premise":{"configs":[{"asia_dir_thr":0.8},{"asia_dir_thr":0.5}],"min_n":60},
 "book_marginal":true,"max_book_evals":6,"controls":true,"name_prefix":"GCCLK01_GC"}
```
16 Configs. Achtung Engine: `asian.trades` verwirft Sessions mit weniger als 60 Range-Bars (Zeile 94), ein Range-Fenster unter 60 Minuten (z. B. 08:20-08:35) wird komplett übersprungen, deshalb 08:20-09:20. Testarten: Prämisse, Grid+Plateau, Nulldrift (`tm_null` existiert in `asian`), Kosten-Stress 2 Ticks, OOS, Epochen-Split (Gold-Boom), Roll-Gegenprobe (`GC_rolls.json`), Buch-Marginal (MGC-Bein ohne NT8-Strategie).
- **Buch-Lücke:** Stufe Prämisse (Zählung sagt: scheitert dort). Danach: Survivors/Gates (freq, top5), PBO, Zufallsdecke, Buch-Marginal, dann NT8-Strategie für MGC (existiert nicht), Daten GC nur bis 25.07.2026, `promote_next` prüft nicht, ob es eine NT8-Strategie für das Symbol gibt.

### 3.2 CLEIA-01 `cleia01_wed1030_CL` (Rang 4)

- **Mechanismus:** EIA-Lagerbericht Mittwoch 10:30 ET als terminierter Zwangsflow: die Überraschung wird über Minuten eingepreist, Absicherer und Momentum-Trader stapeln nach.
- **Why:** Weil der Lagerbericht eine Überraschung gegenüber dem Konsens liefert, auf die Raffinerien, Händler und Fonds mit Größe reagieren müssen (Cache Z.769: Vola-/Volumen-Reaktion klingt in 20-30 Minuten ab), neigt CL dazu, eine 10-Minuten-Reaktion (10:30-10:40) in den folgenden 30 bis 60 Minuten entweder fortzusetzen oder zu überschießen. Prüfbar: mittlere gerichtete Bewegung 10:41 bis +60 Min am Mittwoch > 3x Kosten und **größer als dieselbe Regel an Nicht-Mittwochen** (Kontrollzelle). Verwerfen wenn: Kontrolle gleichauf (dann ist es Vola-Reaktion 10:30 generell), n < 100, t < 2. Erwartete Edge laut Zählung 3-5 $/MCL bei 28-43 Tr/J, Kosten 3,6-5,2 $: **unter Kosten, Kontrolle identisch (4,7 $)**. Feiertagswochen (EIA am Donnerstag) sind mit `tm_dow=[2]` nicht abgefangen, kleine Verunreinigung.
- **Quelle:** Cache Z.769 (Elder/Miao/Ramchander Energy Economics, Abstract).
```json
{"id":"cleia01_wed1030_CL","type":"grid","priority":55,"symbol":"CL","family":"Trend Following",
 "base":{"mode":"tsmom","symbol":"CL","tm_signal":"ret","tm_base":"window","tm_sig_start":60,"tm_sig_len":10,"tm_thr":0.002,"tm_side":"momentum","tm_dow":[2],"tm_stop_mode":"range","tm_stop_mult":0.5,"tm_exit":"time","tm_hold_min":60,"commission_rt":1.6},
 "grid":{"tm_side":["momentum","fade"],"tm_thr":[0.001,0.002,0.003],
         "exit_profile":[{"_label":"t30","tm_exit":"time","tm_hold_min":30},{"_label":"t60","tm_exit":"time","tm_hold_min":60},{"_label":"eod","tm_exit":"eod"}],
         "tm_stop_mult":[0.5,0.8]},
 "premise":{"configs":[{"tm_side":"momentum"},{"tm_side":"fade"}],"min_n":100},
 "book_marginal":true,"max_book_evals":6,"controls":true,"name_prefix":"CLEIA01_CL"}
```
36 Configs. Kontroll-Job (Nicht-Mittwoch, `tm_dow=[0,1,3,4]`) gehört als `book_marginal:false`-Zwilling daneben, sonst ist ein Ergebnis nicht deutbar. Testarten wie 3.1 plus Roll-Sessions (CL rollt monatlich, ~5 % der Sessions). **Buch-Lücke:** Prämisse; danach wie 3.1, plus E8-Freigabe MCL bestätigt (Cache), NT8-Strategie fehlt, Daten nur bis 25.07.2026.

### 3.3 MAKRO-01 `mak01_macrogate_dgs_dxy_NQ` (Rang 3)

- **Mechanismus:** Zins- und Dollar-Regime (5-Tages-Änderung DGS10, DGS2, DTWEXBGS, alles vom Vortag) als Zustandsvariable für die Stärke des Opening-Drive (Diskontsatz-Kanal für Growth-Duration, globale Risikobereitschaft). Anders als VIX/GEX (getestet) ein zweiter Informationskanal, anders als AP61 (Rendite als Richtungssignal, negativ) hier als Stärke-Gate.
- **Why:** Weil NQ als Long-Duration-Aktiva auf Zinsschocks mit Bewertungsdruck reagiert, neigt der Opening-Drive an Tagen nach einem Renditeschock (10Y +10 bp in 5 Tagen) dazu, stärker zu laufen, weil der Verkaufsdruck dann über Stunden gestaffelt wird. Prüfbar: gegatetes Bein schlägt die zeit-gematchte Zufallsausdünnung (AR-04) um mindestens 20 $/Tag (Lehre 161). Verwerfen wenn: Gate-Wirkung nicht besser als Zufalls-Ausdünnung, oder nur in einem Zinsregime (2022). Erwartete Edge: **aus der Zählung nicht auflösbar** (Spreizung Terzile bis 14 Pkt, se 15,6, MDE rund 43 Pkt bei 800 Trades), also ein Vorrats-Abschluss ohne Erwartung.
```json
{"id":"mak01_macrogate_dgs_dxy_NQ","type":"grid","priority":55,"symbol":"NQ","family":"Trend Following",
 "base":{"mode":"tsmom","symbol":"NQ","tm_signal":"ret","tm_base":"open","tm_sig_start":0,"tm_sig_len":15,"tm_thr":0.003,"tm_side":"momentum","tm_stop_mode":"range","tm_stop_mult":0.3,"tm_exit":"eod"},
 "grid":{"gate":[{"_label":"aus"},
                 {"_label":"z10_schock","tm_dgs10_chg5_min":0.10},
                 {"_label":"z10_fall","tm_dgs10_chg5_max":0.0},
                 {"_label":"usd_rise","tm_dxy_chg5_min":0.5},
                 {"_label":"usd_fall","tm_dxy_chg5_max":0.0}],
         "tm_stop_mult":[0.3,0.5]},
 "premise":{"configs":[{"tm_dgs10_chg5_min":0.10},{"tm_dxy_chg5_max":0.0}],"min_n":100},
 "replaces_leg":"NQ_Momentum_d260818","book_marginal":true,"max_book_evals":6,"controls":true,"name_prefix":"MAK01_MACROGATE_NQ"}
```
10 Configs, 4 echte Gate-Arme (Bonferroni 4). Einheiten: `dgs10_chg5` in Prozentpunkten, `dxy_chg5` in Indexpunkten. **Buch-Lücke:** Stufe Survivors/Gates (Trades/Jahr je Arm, ~76 x Anteil), Pflichtkontrolle AR-04, dann Ersatz-Marginal gegen NQ_Momentum (nested OOS). Ehrlich: Stufe 2 hatte nie die Auflösung für 3 pp (Power 0,24).

## 4. BTC-01: der eine Raum mit strategischem Informationsgewinn (blockiert)

- **Warum hier:** einziger Markt im E8-Universum, für den peer-reviewter Intraday-Momentum-Befund existiert (Shen, Financial Review 2022, Cache Z.524: erste Session mit höchstem Volumen/höchster Vola trägt, stärker in Abwärtsphasen), Kosten je Range klein (MBT Tick 0,50 $, Tagesrange rund 3 % x 0,1 BTC), Uhr und Regime unkorreliert zu den drei NQ-Beinen (Buch-Unkorreliertheit 2). CME-Krypto läuft seit 30.05.2026 24/7 (Cache Z.768), damit fällt der Weekend-Gap-Mechanismus weg, ein Session-Anker muss über Volumen statt Uhr definiert werden.
- **Why:** Weil ein Markt ohne Auktionsschluss Aufträge über Volumen-Sessions staffelt und Liquiditätsgeber Risiko nur zögerlich aufnehmen (Elaut/Frömmel/Lampaert 2018, Cache Z.523), neigt die Richtung der ersten Hoch-Volumen-Stunde eines Tages dazu, sich in der folgenden Stunde fortzusetzen. Prüfbar: mittlere gerichtete Bewegung der Folgestunde > 3x Kosten, stärker nach Abwärtstagen. Verwerfen wenn: nur 2021 (Bullenlauf), OOS negativ, oder Long-Bias-Kontrolle (Dauer-Long) gleichauf. Erwartete Edge: unbekannt, Größenordnung Range 210 $/MBT/Tag, also bei 0,15 R rund 30 $/Trade, 100-200 Trades/Jahr.
- **Blockiert durch:** (a) Daten: BTC (CME, 5 BTC, ab 12/2017), MBT und MET (ab 05/2021) müssen per `MaxBulkExport` aus NT8 exportiert und zu Continuous gebaut werden (aktuell nur 1-4 MBT-Kontrakte, Plan 19.09.). (b) Modul: `asian.trades` und `qbt.load_rth` kennen nur Globex-Tag ab 18:00 ET bzw. RTH; für 24/7 braucht es `session_mode="utc_day"` mit Signalfenster in Minuten seit Tagesbeginn 00:00 UTC und hartem Flat um 16:10 ET (E8-Regel).
- **Modul-Spec `crypto24` (Vorschlag):** Eingabe 1m-Bars UTC; Signalfenster `[s, s+L)` ab UTC-Mitternacht, Entry Open der Folgebar, Exit nach `tm_hold_min` oder 16:10 ET; Parameter: `s` in {0, 13:00, 13:30 UTC}, `L` 30/60, `thr` in Sigma des Vortages, `tm_side`, Stop in Range. Look-ahead-Fallen: Vortages-Sigma darf das aktuelle UTC-Datum nicht enthalten; Continuous-Roll (monatlich) nie zwischen Signal und Entry; MBT-Historie kürzer als BTC (Regime-Vergleich nur über die Schnittmenge). Buch-Marginal braucht MBT-Kosten (commission_rt) und `MICRO_OF`-Eintrag.
- **Ablauf, sobald Daten da sind:** erst Zählung (wie Abschnitt 2, 10 Minuten), dann Prämisse-Job, dann Rest. Offene Frage vorab an E8: Kontrakt-Limits und Handelszeiten für MBT/MET im Signature-Programm (AP141 verweist auf Cache Z.761, Krypto ist dort gelistet, Limits nicht).

## 5. Offene Wege der übrigen Karten (Stand 22.09., Register/Queue gegengezählt)

| Karte / Weg | Stand | ein-weg-fertig? |
|---|---|---|
| Fibonacci W14/W26 (Leg-Invalidierung) | gebaut, AC-06d x4 gerechnet, alle 0 Kandidaten | nein, erledigt |
| Fibonacci W1/W11/W16 (Level als Ziel) | brauchen Ziel-Arm `tm_exit="leg_target"` (~20 Zeilen, nicht gebaut); `_leg_stop` existiert nur in `maband`; hingen an AC-06d, das keinen Stop-Arm-Kandidaten lieferte | nein: erst Modul, Erwartung niedrig |
| Fibonacci W24a (Overnight-Leg-Fraktionen) | Spec A `mb_kind="retr"` nicht gebaut; inhaltlich Nacht-Struktur, überlappt die Overnight-Bias-Karte | nicht vorschlagen (ausgeschlossen) |
| Fibonacci W12b (Swing-Bruch x Rundzahl) | der Messfund #149 wurde in #151 zurückgezogen (Tick-Raster) | nein, Prämisse weg |
| Rundzahlen W19 (Hazard-Prescan) | Prescan offen, kein Grid; Story Zeit-Exit-Kanal; Research ohne Beleg | Prescan, kein Job |
| Rundzahlen W26 (Schluss-Anziehung) | Research-Call lief, Story fällt in jetziger Fassung durch | nein |
| Rundzahlen W17/W5k/W33/W21/W23 | geschlossen, tot bzw. nicht bank-reif | nein |
| Session Momentum W16a/W42a | gerechnet, premise_failed (W42a echt) | nein |
| Session Momentum W6a (TN-03 Reparatur) | Overnight-Segment, deckt die Overnight-Bias-Karte (W40/SES-W6) | ausgeschlossen |
| Session Momentum W40/W41 (Modul D) | Same-Time-of-Day: hier **0,04 bis -0,6 Pkt brutto gemessen**, Modul D lohnt nicht | nein, mit Zahl |
| ES-NQ XD-W12a | gerechnet, 0 Kandidaten | nein, erledigt |
| ES-NQ XD-W15a (VWAP-Seite) | Prämisse schwach (11,5-16,4 % Nicht-Übereinstimmung), Why nur Korrelation; VWAP-Familie ist Kontrast zur laufenden ADX x VWAP-Karte | nein |
| ES-NQ XD-W5a/b (SMT-Fehlausbruch) | Spec A (`mb_kind="smt"`, ~105-125 Zeilen) nicht gebaut; Level-Bedeutung ist vierfach widerlegt (#138/#149), neu nur die Nichtbestätigung im Schwester-Index | Modul-Spec, kein Job; Erwartung niedrig |
| ES-NQ XD-W25a/b, W13, W27 | Prämisse nicht bestätigt bzw. Research widerlegt | nein |

Ergebnis: **kein** Weg ist ein Job ohne vorher gebautes Modul, und für keines der fehlenden Module trägt die Vormessung den Bau.

## 6. Modul-Specs und Blockiert

- **`crypto24`:** siehe Abschnitt 4.
- **`tm_news_only`, `tod_prev` (Modul D), `clv_prev`:** nicht bauen, Zählung negativ (Abschnitt 2).
- **Daten-Runde (Max, NT8 Historical Data laden):** (1) BTC, MBT, MET (Rang 1). (2) SI, HG, NG, 6J, ZC, RB, HO (E8 handelbar, laut Plan 19.09. "nicht geladen"): Prior niedrig, weil CL-EIA und GC-Uhr in der Zählung leer sind, nur als Anhängsel derselben Ladung sinnvoll. (3) GC 12-26, CL 09-26 ff., 6E/6B 12-26 nachladen (AP196), sonst enden die Reihen 25.07.
- **Nicht baubar, Daten/Zugang fehlt:** Mega-Cap-Earnings-Kalender (28 Termine/Jahr, Quelle nötig, NQ-Gap-Fortsetzung), 10:00-Uhr-Releases (Kalender-Erweiterung, `news_calendar` kennt nur 08:30 und FOMC), Optionsketten/0DTE, Orderbuch. ZN/ZB als Handelsmarkt: Kosten 10 % der Range (AP140), tot.

## 7. Woher

- **Inventar/Vault:** `registry.json` (Zählung nach Modus/Symbol/Parameter-Schlüsseln), `queue.json` (Status, Hypothesen-IDs), `ideas.json`, `book_state*.json`, Modulcode (`asian.py`, `tsmom.py`, `sigcore.py`, `calendar_fx.py`, `news_calendar.py`), Plan Neue Märkte, Logbuch #158/#162-#168, Friedhof-Analyse, alle Wege-Karten (Fibonacci, Rundzahlen, Session Momentum, ES-NQ; ADX/RVOL/Overnight-Bias nur zur Abgrenzung), Scout-Runden 8-10, Research-Cache Z.494, 523-525, 761-779, 1052.
- **Neu gerechnet (eigene Daten, gehört nicht in den Cache):** Zählungen aus Abschnitt 2; Skripte `cnt1.py` bis `cnt8.py` im Scratchpad, lesen nur Parquet/CSV und `news_calendar`, schreiben nichts in die Engine. Ich habe sie als Zählung deklariert und keinen Runner-Lauf gestartet; falls die Hauptsession das als Grenzfall zu "keine Backtests" sieht, sind es ~30 Zeilen je Skript, die sich prüfen lassen.
- **Web:** **nicht gelaufen.** Der Harness-Hook (Kette `research`) hat `WebSearch` gesperrt, solange `research-scout` in der Session nicht lief; ich habe den `--skip`-Ausweg bewusst nicht benutzt (Session-Quittung gehört der Hauptsession). Deshalb **keine neuen Research-Cache-Einträge**. Offene Fragen für einen `research-scout`-Call: (1) Replikation Intraday-Momentum auf CME-Bitcoin-Futures nach 2021 und mit 24/7-Handel? (2) Erb/Harvey 2013 "The Golden Dilemma" (Realzins/Dollar als Gold-Treiber, nur aus dem Gedächtnis, unverifiziert) für den GC-Zins-Lead. (3) Post-EIA-Drift in CL-Futures auf 1-Minuten-Ebene, nicht nur Vola-Abklingzeit. (4) Wie hoch ist der Krypto-Kontrakt-Deckel bei E8 (MBT/MET)?
- **Hook-Hinweis:** `book_state_next.json` ist neuer als der letzte `--push-next`; das ist nicht von dieser Runde (ich habe nichts am Buch berührt), aber die Hauptsession sollte `--push-next` nachholen.

## 8. Empfehlung für die nächste Runde und Prozess

1. **Kein weiteres Grid auf Index-Mechanismen.** Der Friedhof-Befund (#158) und diese Zählung zeigen dasselbe: der Stufe-2-Test hat für ein Bein-dazu keine Auflösung, und alle 12 neuen Kandidaten liegen brutto unter Kosten oder unter der Frequenzhürde.
2. **Nächste Edge-Quelle: Risk-Premium/Behavioral im neuen Markt (BTC-01)**, Voraussetzung Datenladung durch Max. Bis dahin: die drei optionalen Jobs (3.1-3.3) nur einreihen, wenn die Box ohnehin leer steht und Max den Abdeckungs-Abschluss will; erwartetes Ergebnis 0 Kandidaten, Nutzen sind saubere Friedhof-Stempel (F3, AP195, "macro_gate"-Vorrat).
3. **Prozess-Vorschlag (Lehre 161 als Code):** die Zählung (Trades/Jahr, gerichtete Bruttobewegung in $/Kontrakt gegen Kosten, t) als Pflichtschritt `prescan_gross.py` vor jedem Handjob in `discovery/`, 0 Register-Trials. Sie hätte hier alle 7 verworfenen Zeilen (6-12) in 10 Minuten beantwortet und hätte MAKRO-01/GCUHR-01/CLEIA-01 als Low-Prior markiert, bevor `ein-weg` gelaufen wäre. Entscheidung Hauptsession/Max.
4. Jobs, die Zeit sparen könnten: wenn Max lieber Ersatz statt Neuzugang testen will, ist der einzige nicht ausgeschöpfte Hebel laut #158 die nested-OOS-Bewertung der Ersatz-Kandidaten am Buch, kein Suchraum, sondern Auswertung der 2.634 unbewerteten Survivors (k_eff-Messung).

## Dateien

- Dieser Report: `C:\Users\maxlk\AppData\Local\Temp\claude\C--Users-maxlk-Documents-Obsidaian-My-Brain-My-Brain\ce94f9b3-4177-4c27-b0de-f3816f3174ea\scratchpad\alpha_scout_ap194.md`
- Zählungs-Skripte: `...\scratchpad\cnt1.py` (Segment-Zählung GC/CL/NQ/6E), `cnt3.py` (Makro-Regime NQ/GC), `cnt4.py` (Ankündigungsprämie, EIA), `cnt5.py` (Same-Time-of-Day, CLV), `cnt6.py` (Momentum nach Tagestyp), `cnt7.py` (Eröffnungs-Fade RTY/YM/ES), `cnt8.py` (Ankündigungsprämie mit Mittelwerten).
