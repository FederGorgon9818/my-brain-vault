---
tags:
  - projekt/discovery
  - alpha-suche
erstellt: 2026-10-10
status: entschieden (Gruppe 1 lief 12.10., Gruppe 2 6E/ZS/ZW eingereiht 16.10., Gruppe 3 als AP311/AP196/AP399/AP400/AP401, TE-14 und ORB-NR7 verworfen)
---
> [!info] Bericht des alpha-scout zum Auto-Ticket "Discovery-Queue leer". Vorgänger: [[Alpha-Scout AP194 (22.09.2026)]]. Nichts eingereiht, keine Queue/Bank/Registry/Ticket angefasst. Die 9 Job-Dateien liegen als Vorschlag unter `engine\discovery\jobs_proposed\261010_*.json` (alle durch `inbox_tool.validate_job` ohne Beanstandung, alle ≤ 24 Configs). Zählskripte (0 Register-Trials) lagen im Session-Scratchpad: `cnt_a.py` bis `cnt_d.py`.

# Alpha-Scout Queue-Nachschub (10.10.2026)

> [!success] Stand 16.10.2026 (Session 1ea17a41, Entscheidungen Max 15.10.)
> - **Gruppe 1** (8 Jobs) lief am 12.10., kein Kandidat. Die OPEXMOM-Ergebnisse liefen noch mit dem alten `calendar_fx` (Look-ahead) und sind laut Engine-Fixes-Session ungültig, Neubewertung in AP286.
> - **Gruppe 2:** 6E-, ZS- und ZW-Probe am 16.10. eingereiht (pipeline-auditor go, Vorzählung im Register nachgetragen). ORB-Fade NR7 no-go (pipeline-auditor 13.10.), ONORB-W45a war am 06.10. schon korrekt gemessen (AP304, kein NaN-Durchlass).
> - **Gruppe 3:** BTC (AP311), NT8-Nachladen (AP196), neu AP399 (alle Märkte, die bei unseren und anderen Prop-Firms handelbar sind), AP400 (Mega-Cap-Earnings), AP401 (USDA, Wiedervorlage nach der ZS/ZW-Probe).
> - **CL TE-14** verworfen. **Bank-Befund** (`replaces='NQ_Momentum_d260818'`) war am 13.10. schon repariert.

## 0. Das Ergebnis in sechs Sätzen

1. **Gruppe 1 (sofort einreihbar) enthält keinen neuen Mechanismus.** Sie besteht aus Bestätigungs-Nachtests von Next-Buch-Kandidaten (OPEXMOM), einem Beinahe-Treffer-Nachtest (RTY-Gap), einem Gate-Abschluss (MAKRO-01) und drei CL-Nachtests aus AP195. Das sind Grid-Nachbarn bzw. Abdeckungs-Abschlüsse, nützlich für saubere Stempel, mit niedriger Fundwahrscheinlichkeit.
2. **Das einzige Material mit echtem Informationsgewinn sind neue Märkte**, weil nur dort ein mäßiges Bein auf ρ ≈ 0 zum NQ-Buch trifft (Maßstab aus #179: echte Beine bringen dSR +0,2 bis +0,3, die 6 Friedhofs-DURCH nur +0,002 bis +0,065). Daten für 6E, 6B, ZS, ZW sind seit 19.09. da und wurden **nie gerechnet**. Meine Vormessung (Abschnitt 3) findet genau eine Zelle über 3x Kosten: **6E, Signal 30 Min ab 09:30, Schwelle 0,15 %** (Gruppe 2, braucht 3 Engine-Zeilen).
3. **Der Rest des Index-RTH-Raums ist ausgereizt.** Die Hypothesen-Bank im Code (258 Zeilen) ist bis auf 3 begründete Holds komplett in der Queue gewesen. Die Vault-Banken (Volumen und Flows 479, TWAP 100, PCA) sind nur zu etwa 5 % in Code übersetzt, aber ich habe die 186 Zeilen mit "Daten da und Modus reicht" durchgesehen: Praktisch jede ist Grid-Nachbar eines gerechneten Mechanismus oder durch eine Wege-Karte/Logbuch abgedeckt (Abschnitt 6).
4. **Zwei Vorzählungen haben Kandidaten sofort beerdigt:** Long-only-Dip-Buy nach schwacher Eröffnung (NQ −22 $/Trade) und die Ausdehnung der OpEx-Fortsetzung auf wöchentliche/tägliche Verfälle (KF-26/KF-27: andere Freitage +10 $, t 0,8; ES −1 $).
5. **Zwei Befunde für die Hauptsession, die wichtiger sind als jeder Job:** (a) `replaces='NQ_Momentum_d260818'` in mindestens 16 H()-Zeilen löst nicht mehr auf, `--enqueue` bricht deshalb ab (AP210); (b) der NaN-Durchlass in `sigcore.gates_pass` für `tm_on_ret_min`/`tm_pre_ret_min`/`tm_pre_rvol_min` kann AP304 erklären und würde dann **alle ONORB-Gate-Jobs** (W24a, W27a, W31a, W34a, W45a) entwerten (Abschnitt 7).
6. **Ehrliches Urteil zu Gruppe 1:** nur Grid-Nachbarn. Wer echten Suchraum will, muss Gruppe 2 (6E/ZS-Probe, W45a nach Fix) und Gruppe 3 (BTC, Kalender) freigeben.

## 1. Was sich seit dem 22.09. geändert hat (Delta)

| Seit | Folge für die Suche |
|---|---|
| Gate v4 live (29.09.) | Walk-Forward mit Neuauswahl und Buch-Stufe auf der OOS-Kurve. Formal reicht dSR > 0 bei Passquote ≥ −3 pp, aber echte Beine liefern +0,2 bis +0,3, die Friedhofs-DURCH nur +0,002 bis +0,065 (#179 Lehre 2). Unkorreliertheit ist damit praktisch die Bedingung, nicht nur ein Bonus. |
| Friedhof-Nachlauf (#179, 01.10.) | 240 Karten gemessen, 6 DURCH im Rausch-Band, 94 Buch-Durchfälle ohne eigenes Alpha. Beinahe-Treffer: ORB-fade_nr7_honest (dSR +0,141, t_alpha 2,46), RTY-Gap-Retune (+0,083), OPEXMOM als Familie. |
| Abdeckungs-Jobs aus AP194 gelaufen (#180, 05.10.) | CL-EIA, GC-COMEX: `empirisch-nichts-gefunden`. TD-12 GC/CL: echt-aber-zu-klein. Die drei optionalen Jobs des Vorgängers sind damit erledigt, MAKRO-01 NQ nie eingereiht. |
| NT8-Daten GC/CL/6E/6B/ZS/ZW/ZN/ZB/FDAX | GC/CL komplett gerechnet (143 Hypothesen geklont), **6E/6B/ZS/ZW nie gerechnet**, BTC/MBT/MET weiter nicht geladen (AP311 liegt bei Max, Sprint KW41). |
| Marktzustands-Karte (28.09.) | Suchrichtung "Bein, das im Bull von selbst verdient". Ich habe das als Long-Dip-Buy gezählt: tot (Abschnitt 3). |
| Engine heute lokal gefixt, Box noch alt | AP223 (Target-Exits mit voller Slippage), AP286 (opex_mom ohne Same-Bar-Look-ahead), AP296 (vwap_pullback Stop). OPEXMOM-Jobs sind **erst nach dem Sync ehrlich**. |

## 2. Inventar in 5 Zeilen

1. Register 69.481 Trials: `tsmom` 41.000, `maband` 17.094, `ts_reversal` 3.158, `firstbar_ematrail` 2.880, `rv` 810, `i2` 563, `regime_gate` 530, `gap` 506, `last_hour` 472, `asian` 453, `orb` 253, `cal` 231, `gap_daily` 228, `vwap_pullback` 166. Symbole NQ 37.724, RTY 11.691, ES 8.797, YM 7.961, GC 2.777, CL 161, **6E/6B/ZS/ZW 0**.
2. Queue 1.554 Jobs: 989 done, 564 premise_failed, 1 failed, 0 pending. Quellen: Generator 631, Nachlauf v4 505, Bank 341. `long_only` kommt in nur 311 von 40.000 `tsmom`-Trials vor.
3. Code-Bank (`hypothesis_bank.py`, 258 H()-Zeilen): alles gelaufen außer ADX-W36 und ADX-W14 (beide mit konkreter Hold-Begründung) und ONORB-W27b (Code-Prüfung `as_side`).
4. Offene Fäden: AP304 (W45a ungemessen), AP305 (Beinahe-Treffer), AP195 (CL-Thesen), AP218/AP219 (Gold außerhalb RTH), AP225/AP226/AP227 (Wiederaufnahmen, sind Auswertungen, keine Discovery-Jobs), AP311 (BTC) und AP196 (NT8-Nachladen, GC/CL enden 07/2026).
5. Daten: NQ/ES/RTY/YM 1m+1d, VIX, DGS2/DGS10, DTWEXBGS, DIX/GEX; NT8-Continuous GC, CL, 6E, 6B, ZN, ZB, ZS, ZW, FDAX. E8-Universum laut Cache 793: Metalle, Energie, FX, Zinsen, Agrar (ZC/ZW/ZS/ZM/ZL/LE/HE/GF), MBT/MET, Zwangsglättung 16:10 ET.

## 3. Vormessungen (Zählung, 0 Register-Trials, ohne Stops, brutto vor Kosten)

Methode wie im Vorgänger (Entry Open der Bar nach dem Signalfenster, Exit Close Sessionende, `qbt.load_rth`, 2016 bis 09/2026). **Das ist eine Zählung, kein Tot-Stempel.** Kosten je Round-Trip für 1 Micro bzw. 1 Vollkontrakt: Index-Micros 4 $, ZS/ZW 30 $, 6E 20 $, 6B 25 $.

| Zählung | Ergebnis | Lesart |
|---|---|---|
| Long-only Dip-Buy: 30 Min ab 09:30 unter −0,3 % bzw. −0,5 %, Long ab 10:01, Exit EOD | NQ **−21,6 $/Trade** (t −1,6, OOS −33), 50 Tr/J. ES +9,6 (t 0,8), YM +6,6, RTY −0,5. Unbedingt (alle Tage nach schwachem Open) NQ −7,8 | **verworfen.** Nach schwacher Eröffnung läuft NQ weiter, das ist das Momentum-Bein. "Bein, das im Bull von selbst verdient" ist nicht der Dip-Buy. |
| OpEx-Fortsetzung nach Wochentag (Morgen-Move bis 12:00, Entry 12:00, Exit EOD, Schwelle 0,2 %) | **3. Freitag NQ +53 $/Micro, t 2,93, n 94, 9 Tr/J**; ES +38,5, t 2,67, n 70. **Andere Freitage NQ +9,8 (t 0,78), ES −1,2 (t −0,14).** Mo bis Do NQ +9,7 (t 1,67, 146 Tr/J), ES +1,1 | **KF-26/KF-27 verworfen** (kein generischer Freitags-/0DTE-Effekt). Mo bis Do 9,7 $ gegen 4 $ Kosten ist die allgemeine Nachmittags-Fortsetzung = LastHour/Momentum. Der OpEx-Effekt ist **monatsverfallspezifisch**, das stützt das Why (Open-Interest-Bündelung), nicht die Ausweitung. |
| ZS Eröffnungs-Drift (Signal ab 09:30, Exit 14:20): Momentum | 15 Min/0,4 %: **+40,9 $** (t 1,87, 66 Tr/J, OOS ab 2024 +52,9). 30 Min/0,2 %: +20 $ (t 1,6, 152 Tr/J). Fade jeweils spiegelbildlich negativ | positives Rohsignal, aber **1,4x Kosten** (30 $), dazu Stops. Grenzfall. |
| ZW dito | 30 Min/0,2 %: +20,1 $ (t 2,37, 193 Tr/J, OOS +16). 15 Min/0,4 %: +23 $ (t 1,84). 60 Min ≈ 0 | unter Kosten (30 $). |
| **6E Eröffnungs-Drift (09:30 ab, Exit 15:50): Momentum** | **30 Min/0,15 %: +64,6 $ (t 2,48, 26 Tr/J, OOS ab 2024 +75,7, n 45).** Nachbarn: 15 Min/0,15 % +5 $ (t 0,1), 60 Min/0,15 % +12,7 (t 0,9), 30 Min/0,08 % +9,5 | **einzige Zelle über 3x Kosten (20 $)**, aber 1 von 12 geprüften Zellen (Bonferroni p ≈ 0,17), Nachbarn tragen nicht, also Spitze statt Plateau. Wert liegt im Informationsgewinn, nicht in der Erwartung. |
| 6B dito | alle 12 Zellen −40 bis +2 $ | nichts. |

## 4. Ranking (0 bis 2 je Kriterium, Summe max. 14)

Kriterien: Why · Kosten ≥ 3x · Frequenz · Neuheit im Register · Buch-Unkorreliertheit · Baubarkeit · Stetigkeit.

| Rang | Idee | Gruppe | W | K | F | N | U | B | S | Σ | Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BTC/MBT/MET Intraday-Momentum (`crypto24`) | 3 | 2 | 2 | 2 | 2 | 2 | 0 | 2 | **12** | blockiert: Daten + Modul (AP311), unverändert Rang 1 seit 22.09. |
| 2 | **6E-Probe** (tsmom, Drift ab 09:30, 18 Configs) | 2 | 1 | 2 | 1 | 2 | 2 | 1 | 1 | **10** | drei Engine-Zeilen; Why dünn (Hedge-Flow-Staffelung ist Plausibilität) |
| 3 | **ZS/ZW-Probe** (Re-Open 09:30 ET, USDA-Welt) | 2 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | **9** | Roll-Falle, Vollkontrakt-Kosten, `sigcore` 390-Min |
| 4 | ONORB-W45a Wiederaufnahme (letzte Nachtstunde 08:30 bis 09:30, Kurov et al. JFQA 2019) | 2 | 2 | 1 | 1 | 2 | 0 | 1 | 2 | **9** | erst AP304 klären; Gate auf Momentum, nicht Bein |
| 5 | CL-Nachtest TE-14 (ohne Makro-Tage) | 1 | 1 | 0 | 1 | 1 | 2 | 2 | 1 | 8 | Basis brutto ≈ 0 |
| 6 | CL-Nachtest TV-02 (Sigma-Quantil) | 1 | 1 | 0 | 1 | 1 | 2 | 2 | 1 | 8 | dito |
| 7 | CL-Nachtest TE-15 (long-only) | 1 | 1 | 0 | 1 | 1 | 2 | 2 | 1 | 8 | dito |
| 8 | Mega-Cap-Earnings-Tag, Gap-Fortsetzung NQ | 3 | 2 | 1 | 1 | 2 | 1 | 0 | 0 | 7 | Kalender (28 Termine/Jahr) fehlt, kein Datenanbieter im Bestand |
| 9 | OPEXMOM Original-Grid NQ | 1 | 2 | 2 | 0 | 0 | 1 | 2 | 0 | 7 | Bestätigung eines Next-Buch-Beins, 9 Tr/J |
| 10 | OPEXMOM ES | 1 | 2 | 2 | 0 | 0 | 1 | 2 | 0 | 7 | |
| 11 | RTY-Gap-Retune Nachtest | 1 | 1 | 1 | 1 | 0 | 1 | 2 | 1 | 7 | Beinahe-Treffer, Selektions-Leck |
| 12 | USDA WASDE/Grain Stocks/Acreage (12:00 ET) auf ZS/ZW | 3 | 2 | 1 | 0 | 2 | 2 | 0 | 0 | 7 | ~16 Termine/Jahr, Kalender fehlt |
| 13 | ORB-fade NR7 honest, Original-Grid | 2 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 6 | größtes dSR im Friedhof, aber IS widerspricht WF |
| 14 | MAKRO-01 (Zins/Dollar als Stärke-Gate) NQ | 1 | 1 | 0 | 1 | 1 | 0 | 2 | 1 | 6 | MDE ~43 Pkt, nicht auflösbar |
| 15 | OPEXMOM YM/RTY | 1 | 2 | 1 | 0 | 0 | 1 | 2 | 0 | 6 | r 0,83 bis 0,96 zu NQ/ES = derselbe Bet |
| 16 | TWAP-Slice-Spur-Modul (Modul-Spec I, TW-05/07/11, TB-06/12) | 2 | 1 | 0 | 1 | 2 | 0 | 0 | 1 | 5 | TD-12 gescheitert, Abstandszeilen = AW-Reparametrisierung (#163) |
| 17 | SMT-Fehlausbruch (Spec A, ~110 Zeilen) | 2 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 4 | Level-Bedeutung vierfach widerlegt |
| verworfen | Long-only Dip-Buy | | | | | | | | | | NQ −22 $/Trade (Abschnitt 3) |
| verworfen | OpEx-Fortsetzung wöchentlich/täglich (KF-26/27, GM-27/28) | | | | | | | | | | andere Freitage +10 $ t 0,8; ES −1 $ |
| verworfen | Kalender-Welt (TOM, Pre-Holiday, Quartalsende, Monatsende-MTD, Pre-FOMC, MOC) | | | | | | | | | | #034, #087, #163: abgearbeitet |
| verworfen | Breite/Konsens aller 4 Indizes, Lead-Lag, Korrelations-Gate | | | | | | | | | | XD-W12a gerechnet (0 Kandidaten), LL-01 u.a. (`rv` 810 Trials), `tm_xref_*` existiert |
| verworfen | 6B-Drift | | | | | | | | | | alle Zellen ≤ +2 $ |
| verworfen | Bond-Equity-Gate ZN/ZB als Intraday-Signal | | | | | | | | | | Information steckt schon im NQ-Globex-Preis (08:30 bis 09:30), ZN-Kosten 10 % der Range |
| kein Job | AP225 (NOISE_ORB bei 150k/k3), AP226 (22 #106-Kandidaten bei k3), AP227 (RVOL-Wege Feasibility) | | | | | | | | | | sind `tempo_plan`/Feasibility-Auswertungen, keine Discovery-Läufe |
| kein Job | AP218/AP219 (LBMA-Fix, London-Anker) | | | | | | | | | | zuerst `konzept-weg`; Caminschi/Heaney: Effekt nur in den ersten 4 Minuten, 1m-Daten lösen das nicht auf |

## 5. Gruppe 1: sofort einreihbar (heutige Engine, heutige Daten)

Gemeinsam: `book_marginal: true`, `controls: true`, Prämisse trägt die These (nicht die Basis, Lehre AP151 P1), Gate v4 rechnet Walk-Forward mit Neuauswahl im Job-Grid. **Vor dem Einreihen** (CLAUDE.md): `ein-weg` (variant-scout + strategy-auditor), `pipeline-auditor`, dann `--add-job`. OPEXMOM erst nach Sync der Box (AP286). Mögliches Problem: das Register wirft bereits gerechnete Configs mit identischem Schlüssel als Zwillinge weg. Die 27er OPEXMOM-Zellen laufen im Register schon (k_job 87/27), neu ist die Engine nach AP286, ob der Runner sie dann neu rechnet, prüft die Hauptsession mit einem Dry-Run.

### 5.1 `opexmom_orig_NQ` / `_ES` / `_YM` / `_RTY` (Prio 70 / 66 / 58 / 58)

- **Why:** Dealer müssen am monatlichen Verfall (Open Interest an wenigen Strikes gebündelt) ihre Delta-Hedges nachmittags in Vormittagsrichtung abbauen (Charm/Gamma, Cache 238 bis 245, #049). Prüfbar: gerichtete Bewegung 12:00 bis EOD am 3. Freitag > 3x Kosten **und** nicht an anderen Freitagen/Mo bis Do. Die zweite Hälfte ist heute gemessen und trägt (Abschnitt 3). Verwerfen wenn n < 40, nur 1 bis 2 Jahre, Null-Zwilling gleichauf, Top-5 > 100 %.
- **Modus/Achsen:** `cal`, `cal_mode=opex_mom`; `cal_entry_min` [120, 150, 180] × `cal_thresh` [0,1; 0,2; 0,3] × `cal_stop` [0,75; 1,5] = **18 Configs** (Original hatte 27, Stop-Mitte 1,0 gestrichen wegen 24er-Grenze, Basis steht auf 1,0).
- **Daten:** da. **Trades/Jahr:** 6 bis 9 je Index (NQ/ES), ein Bet (r 0,83 bis 0,96). **Erwartete Edge:** NQ ~26 Pkt, ES ~7,7 Pkt je Trade (Vorzählung), YM/RTY nicht gezählt.
- **Friedhof/Verwandte:** #049 (OPEXMOM), #034 (OpEx-Fade −22 % tot, Fortsetzung gewinnt), LIVE_EXTRA-Bein, #179 (NQ DURCH dSR +0,048, ES +0,043, YM +0,020, RTY +0,008, alle scheitern außer NQ an Power-Vor-Gates), Teil B ("−0,1 pp, CI −4,7 bis +6,5").
- **Engine-Arbeit:** keine. Sync-Abhängigkeit AP286. `event_combo` (FOMC-Post + OpEx, ES, #179 +0,035) ist derselbe OpEx-Zweig plus FOMC-Zweig (FOMC-Daten nur ab 2021), deshalb nicht als eigener Job.
- **Ehrlich:** Stetigkeit 0 (Tail-Bein), Frequenz 0. Der Job bestätigt oder entkräftet ein Next-Buch-Bein (AP295 Schritt 2), er findet nichts Neues. Wer nur 2 Slots geben will: NQ und ES.

### 5.2 `gaprty_retune_orig_RTY` (Prio 62)

- **Why:** Overnight-Gaps in RTY (dünne Small-Cap-Bücher, Nacht kaum gehandelt) sind oft Positionierung statt Information, Market Maker ziehen nach der Eröffnungsauktion zur Vortagsmitte zurück. Prüfbar: Rückbewegung Entry bis EOD > 3x Kosten, Plateau, Null-Zwilling. Verwerfen bei Spitze statt Plateau, sharpe_t < 2 im WF, OOS ab 2024 negativ.
- **Modus/Achsen:** `gap`, `gap_side=fade`; `gap_atr_lo` [0,3; 0,5; 0,7] × `gap_atr_hi` [1,25; 1,75; 2,5] × `gap_stop_mult` [0,5; 1,0] = **18 Configs**, Basis `gap_confirm_min=5`, kein Target (AP223-unabhängig).
- **Trades/Jahr:** ~40 bis 60. **Edge:** nicht vorgemessen (#179: dSR +0,083, t_alpha 2,32, scheitert nur an sharpe_t 1,85).
- **Verwandte:** Generator hat 12 RTY-Gap-Jobs (done), `exit_RTY_Gap-fade` (Exit-Sweep). Gap-Wege-Karte offen. **Grid-Nachbar**, kein neuer Mechanismus.
- **Engine-Arbeit:** keine.

### 5.3 `mak01_macrogate_pb3_NQ` (Prio 55)

- **Why:** Zins-/Dollar-Schock (5-Tages-Änderung 10Y ≥ +10 bp bzw. Dollar-Index) als Stärke-Gate für den Opening-Drive (Diskontsatz-Kanal, anderer Informationskanal als VIX/GEX und AP61). Prüfbar: gegatetes Bein schlägt zeit-gematchte Zufallsausdünnung um ≥ 20 $/Tag (AR-04, Lehre 161).
- **Modus/Achsen:** `tsmom` mit der PB3-Parametrierung (`tm_pb_entry=3`) als Basis; Achse `gate` [aus, 10Y-Schock, 10Y-Fall, USD-Anstieg, USD-Fall] × `tm_stop_mult` [0,3; 0,5] = **10 Configs**, `replaces_leg=NQ_Momentum_PB3_fa01b` (Ersatz-Bewertung).
- **Daten:** `DGS10.csv`, `DTWEXBGS.csv` da (`tm_dgs10_chg5_*`, `tm_dxy_chg5_*` in `sigcore.gates_pass`). **Trades/Jahr** 25 bis 45 je Arm. **Edge:** nicht auflösbar (Terzil-Spreizung 14 Pkt bei se 15,6, MDE ~43 Pkt). Abdeckungs-Abschluss "macro_gate", Erwartung ~0.
- **Verwandte:** AP61 (Rendite als Richtungssignal, negativ), AR-15/AR-17 (Regime-Gates auf Buch-Beine, 0 Kandidaten), #110 (GEX). **Gleicher Mechanismus, anderes Gate.**
- **Engine-Arbeit:** keine. Die Wirksamkeitsprobe (Gate-Config muss weniger Trades liefern als Basis, weil `tsmom.DEFAULTS` die `tm_dgs*`-Schlüssel nicht kennt) macht der `pipeline-auditor`, siehe auch Befund NaN-Durchlass in Abschnitt 7.

### 5.4 `ap195_cl_tv02_sigq` (24 Configs), `ap195_cl_te15_longonly` (18), `ap195_cl_te14_news` (24), je Prio 52

- **Why/Zweck:** AP195 Schritt 2 und 3: die Thesen-Prämisse laufen lassen, die bei den NM-Klonen an der Basis-Config (n 546, IS expR −0,158) gestorben ist. Je Job steht die These in der Prämisse (`tm_sigma_q_max=0,8`; `tm_dir=long_only`; `tm_exclude_news=core`).
  - TV-02: Opening-Drive-Momentum in Rohöl überschießt an Panik-/Spike-Tagen (oberstes Sigma-Quantil).
  - TE-15: nur die Long-Seite trägt (Hedger/Raffinerien ziehen nach, Verkäufer-Impulse kommen von Fonds).
  - TE-14: an Makro-Tagen (CPI/NFP/FOMC) ist Rohöl ein anderer Prozess. **Achtung:** TE-14 heißt "Makro-Tage ausschließen", **nicht** EIA-Mittwoch (Korrektur #180).
- **Modus:** `tsmom` auf CL, `commission_rt=1,6` (MCL), `tm_exit=eod`. **Daten:** CL 1m NT8, endet 21.07.2026 (AP196). **Trades/Jahr** 25 bis 60. **Edge:** Basis brutto ≈ 0 (Plan 6.3), also Erwartung ~0.
- **Nicht eingereicht** (rr-Exit-Profile, deshalb erst nach AP223-Sync sinnvoll): TV-03 (ATR-Expansion), TV-13 (Panik-Veto), TS-15 (Fensterlage).
- **Verwandte:** #180a (EIA, `empirisch-nichts-gefunden`), NM-Batch 19.09. (90 Jobs GC/CL, 0 Survivors). **Grid-Nachbarn auf neuem Markt.** Entscheidung Max (AP195 Schritt 1: Gate-Lockerung ja/nein).
- **Engine-Arbeit:** keine; AP195 Schritt 4 (`_lint_thesis_premise` als Assert) bleibt offen.

## 6. Volumen-/Flows-Bank: warum daraus kein Job wird

186 von 479 Zeilen sind "Daten da und Modus reicht". Ich habe sie (ohne Null-/Konträr-/Kosten-Zeilen) gegen Register, Wege-Karten und Logbuch gelegt:

- **VV/MO (Volumen, Metaorder):** RVOL-Richtungsachse ist geschlossen (24 Zellen, keine schlägt den Placebo); Filter-/Sizing-Rollen sind AP227 (Feasibility, kein Lauf). MO-11/12/13/22, VV-08, GM-16/17 sind Mehrtages-Ereignisstudien (Swing), im Käfig nicht handelbar außer als Folgetag-Intraday; VIX-Spike-Reversion (`vix_bias`, 77 Trials) deckt MO-22/GM-21/22.
- **HV (Volumenprofil):** 22 Zeilen mit `amt_profile` als **Analyse**, nicht als Handelsmodus (`mode="profile"` fehlt in `qbt`). HV-02/10/15/53 sind Kontrollen. Das ist die Max-Frage "Volumen horizontal als Signal": ein eigenes Vorhaben mit Modul, nicht ein Job.
- **KF (Kalender):** KF-26/27 gezählt und verworfen, KF-08/11/15/16/24 sind Monatsende/TOM (#163, Cache). KF-17/18/22/30/32 brauchen ein Roll-Wochen-Flag, Baum-Ertrag klein (4 Termine/Jahr).
- **MS (Mikrostruktur):** 19 Zeilen mit vorhandenem Modus, die übrigen brauchen Features (λ, VR, OU, Entropie); jede ist ein Gate auf ein Bein, Erwartung nach 0 aus 17 Regime-Filtern.
- **XA/SZ:** Lead-Lag (XA-14 bis 20): `rv` hat 810 Trials, tot; SZ-Fenster liefen großteils als 8 VOLB-Jobs (überwiegend `premise_failed`). SZ-26/29 sind LON-01/W45.
- **GM (Gamma):** 0DTE-Wochentagsmuster (GM-27/28) gezählt, nichts. Optionsdaten fehlen für den Rest (blockiert).

Ergebnis: Die Bank enthält keine unübersetzte Zeile, bei der ich Neuheit, Why und Messbarkeit zugleich sehe.

## 7. Gruppe 2: braucht kleine Engine-Arbeit oder Prüfung

### 7.1 `fx6e_open_probe_6E` (Rang 2 insgesamt, Σ 10)

- **Why (dünn, ehrlich):** Weil globale Aktien-Portfolios ihre EUR-Absicherungsquote nach dem US-Cash-Open und den 10:00-Uhr-Veröffentlichungen anpassen und diese Hedge-Flows über Stunden gestaffelt laufen, neigt 6E dazu, die 30-Min-Richtung ab 09:30 bis 15:50 fortzusetzen. Das ist Plausibilität, kein Beleg. Prüfbar: gerichtete Bewegung > 3x Kosten (20 $), Plateau über Fenster 15/30/60 und Schwellen 0,10/0,15/0,20 %. Verwerfen wenn Zelle nur ein Punkt ist (so sieht die Vorzählung aus), OOS negativ, Roll-Gegenprobe (`6E_rolls.json`) kippt sie.
- **Draft:** `tsmom`, `symbol=6E`, `tm_base=open`, `tm_signal=ret`, `tm_side=momentum`, `tm_stop_mode=range`, `tm_exit=eod`, Achsen `tm_sig_len` [15, 30, 60] × `tm_thr` [0,001; 0,0015; 0,002] × `tm_stop_mult` [0,5; 0,8] = 18, Prämisse `{tm_sig_len: 30, tm_thr: 0,0015}`, `min_n` 100, `commission_rt` aus der E8-Gebührentabelle (Platzhalter 5 $).
- **Engine-Arbeit:** `qbt.POINT_VALUE["6E"]=125000`, `TICK["6E"]=0.00005`, `MICRO_OF["6E"]="6E"` (Plan E1 hat 6E bewusst offen gelassen). Vollkontrakt, weil M6E relativ 1,7x teurer ist (Tick 0,0001 bei 1/10 Notional). 26 Tr/J liegen an der 25er-Grenze.
- **Verwandte:** FX-01 (London-Richtung bis 12:00, 22.09. gezählt, t −0,95 bis +0,17), Plan "6E/6B zurückgestellt: Kosten 10 bis 16x MNQ" (die Zählung zeigt in der besten Zelle 20 $ Kosten gegen ~65 $ brutto).
- **Erwartung:** Fundwahrscheinlichkeit niedrig (eine Zelle von 12). Wert: erster Test eines Marktes mit ρ ≈ 0,13 zu NQ.

### 7.2 `grain_open_probe_ZS` / `_ZW` (Σ 9)

- **Why:** Das CBOT-Tagesgeschäft startet 09:30 ET (08:30 CT) nach 45 Minuten Pause, Overnight-Information (Wetter, Exporte, China-Käufe) trifft das Buch gebündelt; Hedger und Fonds staffeln. Prüfbar: Drift > 3x Kosten (30 $/Vollkontrakt). Vorzählung: ZS 1,4x, ZW 0,7x Kosten. **Erwartung: stirbt an der Dollar-Hürde (Lehre 161, 812 bis 2.078 $/Jahr: ZS 15 Min/0,4 % ergibt 66 × 11 $ netto ≈ 700 $/Jahr).**
- **Draft:** `tsmom` auf ZS bzw. ZW, `tm_sig_len` [15, 30] × `tm_thr` [0,002; 0,004] × `tm_stop_mult` [0,5; 0,8] = 8 je Job, Prämisse `{tm_sig_len: 15, tm_thr: 0,004}`.
- **Engine-Arbeit:** `commission_rt` auf Vollkontrakt-Niveau im Job (MICRO_OF-Kommentar in `qbt`), `sigcore`-Pflichtkontrollen rechnen hart mit 390 Minuten (Session endet 14:20 = 290 Min), Roll-Falle (53 Rolls). Plan 6.4: "Stufe 2 nur TN + ORB".
- **Rang:** nach 6E, weil schwächere Zahl; läuft aber billig im selben Schritt.

### 7.3 `onorb_w45a_rerun_NQ` (Σ 9)

- **Why:** US-Makrodaten kommen 08:30 ET, die letzte Nachtstunde bis 09:30 ist deshalb ein Fenster mit anderem Akteur (Desks, die auf die Zahl reagieren müssen, in einem dünnen Buch). Kurov/Sancetta/Strasser/Wolfe JFQA 2019: Drift auf ES ab ca. 30 Minuten vor dem Release, ~40 % der Anpassung laufen vorher. MO-51/KF-40/SZ-29 stützen dasselbe Bild. Der Weg ist der einzige, bei dem `ein-weg` am 22.09. "hält ohne Vorbehalt" sagte.
- **Problem:** AP304: in allen 12 Gate-Kombinationen identische Kennzahlen wie ohne Gate (808/711/590 Trades). **Der Lauf hat nichts gemessen.** Befund: `sigcore.py` 1303 bis 1308 prüft `abs(ctx_row.get("pre_ret", 0) or 0) < pm`. Bei NaN (`NaN or 0` bleibt NaN) ist der Vergleich False, das Gate lässt durch. NaN entsteht, wenn `overnight_context` im `except`-Zweig (Zeile 751) landet. **Lokal ist `pre_ret` für NQ zu 100 % gefüllt** (2.734 Tage), die Ursache liegt also eher auf der Box (24h-Datei fehlt?) oder in der Weitergabe des Schlüssels. Eine Prüfung dauert Minuten: auf der Box `sigcore.overnight_context('NQ')` aufrufen und `tsmom.trades` einmal mit/ohne `tm_pre_ret_min=0.003` zählen.
- **Draft (nach Fix):** Basis wie im Queue-Job `hyp_ONORBW45a_NQ` (`tsmom`, `tm_sig_len=15`, `tm_stop_mode=atr`, `tm_exit=eod`), Achsen `tm_pre_ret_min` [None, 0,0015, 0,003] × `tm_pre_rvol_min` [None, 1,2] × `tm_stop_mult` [0,5; 0,8] × `tm_exclude_news` [None, core] = **24** (Original 72). `replaces_leg=NQ_Momentum_PB3_fa01b`. Pflichtzellen wie in der Wege-Karte (Makro/Nicht-Makro-Split, Montags-Split, Epochen-Split).
- **Gilt dasselbe Muster für `tm_on_ret_min`** (Zeile 1301): wenn die Ursache NaN-Durchlass ist, sind **W24a, W27a, W31a, W34a** ebenfalls verdächtig (alle als `done`/0 Kandidaten gestempelt). Dann gehört der Fix (`if not np.isfinite(x) or abs(x) < pm: return False`) plus Golden Master plus Liste der betroffenen Urteile in AP304.

### 7.4 `orb_fade_nr7_honest_orig_NQ` (Σ 6, aber größtes dSR des Friedhofs)

- **Why:** Nach einem NR7-Tag (Kompression) stößt der Opening-Range-Bruch auf wenig Gegenliquidität, Fehlausbrüche werden vom Book zurückgenommen; der Fade am OR-Extrem wirkt, wenn der Fill ehrlich ist. #179: dSR +0,141, t_alpha 2,46, r 0,00 zum Buch, WF 7/9, OOS +8.076 $. **Aber:** IS-Prämisse negativ (expR −0,17), Herkunft "Kostenvorteil war geschenkter Tick" (#171), Basis aus 224 Varianten mit 0 robust (#116).
- **Draft:** `orb`, `orb_side=fade`, `nr7_filter=True`, `orb_exec=stop_honest`, `or_min` [10, 15, 30] × `stop_frac` [0,3; 0,4; 0,6] × `nr_window` [5, 7] = 18; `orb_honest_job` verdoppelt automatisch, wenn `orb_exec` offen bleibt.
- **Voraussetzung:** `pipeline-auditor` bestätigt, dass Fade + `stop_honest` einen ehrlichen Limit-Fill modelliert (Berührung ist kein Fill) und den "geschenkten Tick" nicht wiederholt (AP305). Max-Entscheidung AP305.

### 7.5 Weitere Modul-Specs (nicht empfohlen)

- **TWAP-Basismodul** (Modul-Spec I, Scope TW-05/07/11, TB-06/12): Σ 5, Logbuch #163 sagt: Abstandszeilen kollidieren zu 0,984 mit dem VWAP-Block AW. Nur wenn Max den Volumen-Faden bewusst öffnen will.
- **SMT-Fehlausbruch** (`mb_kind="smt"`, ~110 Zeilen): Level-Bedeutung ist vierfach widerlegt (#138/#149), neu nur die Nichtbestätigung im Schwesterindex. Σ 4.
- **`mode="profile"`** (HV-Block, Volumen pro Preis): Max-Faden "horizontales Volumen", Eingaben 1m-Bars, kein Tick. Ohne Tick-Volumen ist POC aus Bar-Volumen eine Näherung (HV-53). Eigenes Vorhaben, nicht für diese Runde.

## 8. Gruppe 3: braucht Daten oder Entscheidung von Max

| Idee | Was fehlt | Aufwand | Σ |
|---|---|---|---|
| **BTC/MBT/MET** (`crypto24`) | AP311: Export per `MaxBulkExport` (nur bei geschlossenem Markt), research-scout zu Replikation nach 2021 und E8-Limits MBT/MET, dann Zählung, dann Modul (UTC-Tag, Flat 16:10 ET) | Max-Klicks + 1 Modul | 12 |
| **Mega-Cap-Earnings** (NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA; Nachbörsen-Reaktion → NQ-Gap) | Kalender 2016 bis 2026 (~28 Termine/Jahr), keine Quelle im Bestand. Mechanismus: informationsgetriebener Gap mit Drift (Post-Earnings-Announcement), nur über Index-Gewichte | Datenquelle entscheiden (EDGAR 8-K-Daten gratis, Aufwand mittel) | 7 |
| **USDA-Termine auf ZS/ZW** (WASDE, Grain Stocks, Acreage 12:00 ET, Export Sales Do 08:30) | Kalender (usda.gov, öffentlich) plus erst Gruppe-2-Befund ZS/ZW; ~16 Termine/Jahr, Tail-Lotterie-Verdacht | klein, aber erst nach 7.2 sinnvoll | 7 |
| **GC/CL/6E/6B bis heute** (AP196) | NT8-Historie 12-26/09-26 nachladen. Ohne das enden alle GC/CL-Urteile am 21./24.07., "letzte 3 Jahre"-Gate rechnet kürzer, 6E/6B enden 14.09. | Max in NT8, Wochenende | Voraussetzung |
| **SI, HG, NG, 6J, ZC, RB, HO** | Nachladen (E8 handelbar). Prior niedrig, weil GC/CL leer sind; sinnvoll nur als Anhängsel derselben Ladung. NG-Storage (Do 10:30) wäre das CL-EIA-Pendant | gleiche Ladung | 6 |
| **CL sub-minute / EIA-Konsens** | Wiedervorlage #180a: Databento-Tick oder Konsensquelle. Die einzige offene Klammer um die EIA-These | Kostenentscheidung (Databento geplant) | 5 |

## 9. Befunde für die Hauptsession

1. **`replaces` löst nicht mehr auf.** Beim Laden von `hypothesis_bank.py` warnt `build_jobs`: `replaces='NQ_Momentum_d260818' nicht eindeutig gegen book_state.json aufloesbar (0 Praefix-Treffer)`, "`--enqueue` bricht deshalb ab" (AP210). Betroffen mindestens 16 Zeilen (AC-06b/c, LD-01, ONORB-W7a/W24a/W29a/W31a/W33a/W45a, VOLB-MO59x/MO15x u.a.). Das Buch heißt jetzt `NQ_Momentum_PB3_fa01b`. Jede künftige Wiedereinreihung aus der Bank scheitert daran. Meine Jobs benutzen den neuen Namen.
2. **NaN-Durchlass in `sigcore.gates_pass`** (Abschnitt 7.3), mögliche Erklärung für AP304 und Alarm für alle ONORB-Gate-Jobs.
3. **Zufallsdecke:** Gruppe 1 bringt 9 Jobs, 166 Configs; Gruppe 2 weitere ~76.
4. **Queue-Status:** `queue_empty` seit 06.10. ist keine Panne. Der Generator ist ausgereizt, die Bank ebenfalls. Weitere Auto-Tickets "Queue leer" sagen nichts Neues, bis Gruppe 2/3 Material liefert.

## 10. Ehrliches Urteil

- **Gruppe 1:** keine echten neuen Mechanismen. OPEXMOM ist ein bekannter Mechanismus mit besserer Beweisführung (monatsverfallsspezifisch, bestätigt gegen andere Freitage), RTY-Gap und CL-Nachtests sind Grid-Nachbarn, MAKRO-01 ist ein Gate auf bekanntem Bein. Fundwahrscheinlichkeit je Job ≤ 10 %, Nutzen sind Stempel und ein bestätigtes oder entkräftetes Next-Buch-Bein.
- **Wo der Raum noch offen ist:** neue Märkte (6E/ZS/ZW nie gerechnet, BTC nicht geladen), ein Gate-Fix (W45a) und Kalender-Daten (Earnings, USDA). Alles andere im Index-RTH-Raum ist laut Register, Friedhof und Vorzählungen abgegrast.
- **Was die Pipeline selbst bremst:** Formal reicht bei Gate v4 dSR > 0, tatsächlich Material liefern +0,2 bis +0,3 nur Beine mit eigener Quelle (#179). Das schafft kein weiteres Bein im selben NQ-Fenster, eher eines auf anderem Markt oder anderer Uhr. Das spricht dafür, die Box-Zeit auf Gruppe 2 zu legen und BTC (AP311) vorzuziehen.

## 11. Woher

- **Vault/Inventar:** Alpha-Scout AP194, Logbuch #163, #164, #179, #180, Latte-Audit, Neue Märkte Plan (Abschnitte 1 bis 7), State Classification, Wege-Karten (Zählung der "offen"-Zeilen, Overnight-Bias-ORB Abschnitt W45), Hypothesen-Banken Volumen/TWAP (Header, 186 Zeilen), Alpha-Suche "Offene Fäden", Momentum-Theorie Abschnitt 7, Institutionelle Order-Execution Abschnitt 2, Research-Cache Zeilen 793 (E8-Universum) und 1704 bis 1722 (Kalender), Tickets AP195/196/218/219/225/226/227/304/305/311 per `ticket_tool.py show`.
- **Engine:** `registry.json` (nur Zählung per Python, nie gelesen), `queue.json`, `book_state.json` (Legs), `ideas.json`, `hypothesis_bank.py` (HYPOS gegen Queue-IDs), `calendar_fx.py`, `tsmom.py` (DEFAULTS), `sigcore.py` (Zeilen 739 bis 765, 1296 bis 1312), `qbt.py` (POINT_VALUE/TICK/MICRO_OF), `inbox_tool.validate_job` (Trockenlauf, schreibt nichts).
- **Neu gerechnet (eigene Daten, gehört nicht in den Cache):** Zählungen aus Abschnitt 3, Skripte `cnt_a.py` bis `cnt_d.py` im Session-Scratchpad. Sie lesen nur den RTH-Cache und schreiben nichts in die Engine, 0 Register-Trials. Das ist Zählung, kein Backtest-Lauf; falls die Hauptsession es als Grenzfall sieht, sind es je ~40 Zeilen.
- **Web:** nicht gelaufen. Kein Research-Cache-Eintrag. Offene Fragen für einen `research-scout`-Call: Replikation Intraday-Momentum auf CME-Bitcoin; Gebühren und Kontraktlimits E8 für 6E/ZS/ZW; ob es für den USDA-Kalender und Mega-Cap-Earnings eine freie Quelle gibt.

## 12. Empfehlung nächste Runde

1. **Entscheidungen Max:** (a) Gruppe 1 einreihen oder nur OPEXMOM NQ/ES + RTY-Gap (Box-Zeit klein, ~1 Stunde); (b) Freigabe Gruppe 2 (3 Engine-Zeilen für 6E, Vollkontrakt-Gebühren, `sigcore` 390-Fix); (c) AP195 Gate-Lockerung ja/nein; (d) AP311/AP196 am Wochenende erledigen.
2. **Vor allem anderen:** AP304 und der NaN-Durchlass (Minuten, deckt eine mögliche Fehl-Stempelung von fünf Jobs auf), dann das `replaces`-Namensproblem.
3. **Nächste Edge-Quelle:** Risk-Premium/Behavioral im neuen Markt (BTC, danach ZS/ZW-Kalender), nicht mehr Index-RTH. Für Informational: Mega-Cap-Earnings-Kalender als Datenprojekt.

## Dateien

- Job-Vorschläge: `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\261010_opexmom_orig_NQ.json`, `..._ES.json`, `..._YM.json`, `..._RTY.json`, `261010_gaprty_retune_orig_RTY.json`, `261010_mak01_macrogate_pb3_NQ.json`, `261010_ap195_cl_tv02_sigq.json`, `261010_ap195_cl_te15_longonly.json`, `261010_ap195_cl_te14_news.json`.
- Dieser Bericht: `Projekte/Alpha-Scout Queue-Nachschub (10.10.2026).md`.
