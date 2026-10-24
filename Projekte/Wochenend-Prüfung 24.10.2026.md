---
tags: [projekt, trading, gate-v4, stufe-2, buch, wochenende]
date: 2026-10-24
status: entschieden 24.10. (LD01 A und OpEx ins echte Buch), live erst nach Deploy und Auflagen
---

# Wochenend-Prüfung 24.10.2026

Gate v4 Stufe 2 für das Wochenende 24./25.10. Vorgänger: [[Wochenend-Prüfung 17.10.2026]]. Ablauf: [[Buch-Workflow]], Skill `/wochenende`. Gerechnet am PC (nur dort gibt es Abschnitt 5b NT8-Port und die FFN-Fixes vom 23.10.).

## Ausgangslage

- **Echtes Buch** (`book_state.json`, md5 90e5eaf7, PC gleich Box): PB3, LastHour_v3, Asia-Dir, OpenDrive. 5 Konten, alle k1: E8 50k, FN1, FN2, FFN1, FFN2.
- **Next-Week-Buch** (md5 e2ccf7ad): echtes Buch plus OpEx (`NQ_OPEXMOM_fv4`) und LD01 (`NQ_LD01_vix16_fv4`, Variante A).
- **Gerechnet auf einer Scratch-Kopie** (`engine/_scratch_wochenende_1024/next_1024.json`): Next-Buch plus 15:55-Exit bei OpEx (`cal_eod_flat` true, `eod_flat_min` 385, `eod_flat_px` close), Auflage des strategy-auditor vom 22.10. Die erste Fassung von OpEx bekam denselben Exit, damit beide Seiten dasselbe Ausführungsmodell haben. Das echte Next-Buch ist bis zu Max' Entscheidung unverändert.
- Erste Fassungen für OpEx und LD01 standen schon seit 15.10. in `book_erstfassung.json`.
- Seit der letzten Prüfung: RiskGuard Trade-PnL-Fix (AP319) und OpEx-Modul als Code (AP394) am 22.10. deployt, Nightrun BTC 0 Kandidaten (#188), CFD-Vergleich 23.10. (siehe [[CFD-Check 23.10.2026]]), Discovery-Queue seit 20.10. leer.
- Der erste volle Lauf brach bei 15 von 36 Varianten ab (App-Neustart gegen 23:02), der zweite lief job-frei per WMI durch (4.508 s).

## Ergebnis

Bericht `engine/weekend_check/2026-10-24_wochenende.md`, Engine 20fbf8e4, 600 Sims, RiskGuard-Stopp je Konto (E8 50k 900 $, FN 600 $, FFN 150k 2.500 $).

| Variante | Median Monate bis 50k | Diff. zu echt | erste Fassung | recent3y |
|---|---|---|---|---|
| echtes Buch | 79,2 ± 1,1 | | | 49,9 |
| Next (echt + OpEx + LD01) | 67,0 ± 0,9 | −12,2 ± 0,9 | z 3,21, −6,3 M | 41,0 (−8,9) |
| echt + LD01 | 69,3 ± 1,1 | −10,0 ± 0,9 | z 2,27, −3,1 M | 43,4 (−6,5) |
| echt + OpEx | 74,5 ± 1,1 | −4,7 ± 0,8 | z 2,36, −2,8 M | |

- Nulldrift-Zwilling überall 0 %, ökonomischer Tod 0 %, kein Tages-Kill mit Guard, dynamischer Stopp ohne belegten Unterschied.
- Schlimmster Buchtag intraday: echt −1.148 $, Next −1.449 $ (17.07.2026, PB3 + LastHour + Asia + OpEx).
- Regel-Sieger und Empfehlung des Skripts: Next-Week-Buch, Vorsprung trägt.
- Ersatz-Varianten (OpEx oder LD01 statt eines Buch-Beins) sind alle langsamer, außer LD01 statt Asia (−3,9 ± 1,0), das schlägt aber „echt + LD01“ nicht.

## Quant-Team (heute, 5-Konten-Plan)

**Statistiker:**
- **LD01 empfohlen,** Planzahl −3 bis −4,5 Monate (roh −10,0; Drift der ersten Fassung −4,4 ± 0,65; ohne eigene Edge +3,1 langsamer). Eigene Beweislage trägt: t 3,40, ohne Top-5 t 2,49. DSR 0,79 bei 188 Versuchen, belegt bis etwa 50. Regime: 104,6 $ je Trade in den letzten 3 Jahren gegen 24,9 $ davor, 2022 null Trades.
- **OpEx nur vertretbar,** Lesart vom 15.10. bleibt („unentscheidbar, nach Selektion null-kompatibel“). Der 15:55-Exit ändert am Bein nichts (+0,5 $ je Trade). z 2,36 ist das In-Sample-t der Grid-Mitte, die Selektion (Richtung gespiegelt, 4 Symbole, Friedhof-Reaktivierung) zieht die Spalte nicht ab. Top-5 79 % der Summe, ohne Top-5 t 0,61. Planzahl allein −2,7 M (Band −1,3 bis −4,6), neben LD01 0 bis −2 M, **Null ist im Band.**
- **Next als Paket:** Planzahl −3 bis −8 M, Mitte etwa −4, nicht −12,2. Der tragende Teil ist LD01.

**Mathematiker:**
- Der tiefere Tail kommt hinter den Tagesstopp nicht durch. Ruin über die volle Historie sinkt leicht (FN frisch 23,8 → 22,4 %, E8 50k 14,7 → 13,7 %).
- In den letzten 3 Jahren steigt der FN-Ruin um +0,8 pp (FN1/FN2). Das kommt ganz von OpEx: 3 zusätzliche FN-Stopptage, alle OpEx-Freitage. OpEx allein +1,6 bis +1,8 pp FN-Ruin, LD01 allein senkt ihn.
- Keine verdeckte Hochstufung: σ +10 %, Drift +19 %, θ praktisch gleich. Gegen „echtes Buch nur größer“ ist Next auf FN 4 bis 6 pp sicherer.
- Strukturell am saubersten: nur LD01. Beide sind vertretbar. Wenn etwas weg soll, dann OpEx auf den FN-Konten.
- Bericht-Bug nebenbei: die Tages-Kill-Tabelle in `weekend_check` nimmt für FFN die DD 4.000 statt 4.700 (nur die Info-Tabelle, Sims korrekt).

**LD01 A gegen B** (Port-Session, Notiz `LD01_quant_team.md`): A allein oder keins, nie B, nie beide. A gegen B −0,1 ± 0,35 Monate, beide zusammen sind ein Größenaufschlag (R² 0,992 gegen 2×A), also eine Hochstufung an der Vola-Regel vorbei.

## Konto-Karten (konto-analyst)

- Register gleich Box. Einzelkarten vom 22.10., Flotte vom 24.10. 00:37, Daten bis 16.10.
- Alle Ampeln grün, alle k1. Keine Hochstufung: σ60 des Buchs 630 $, FFN-Grenze 235 $.
- Überleben 12 M ohne Bust: E8 50k 12,0 %, FN1 1,6 %, FN2 2,4 %, FFN1/FFN2 67,9 %.
- **E8 50k: Inaktivitäts-Frist 28.10., bis dahin fehlt 1 Handelstag.**
- Flotte: Netto 36 M 9.810 $ (SE 387), P(50k in 36 M) 0,0 %, Auslage p90 2.465 $ knapp am Deckel.
- Die Karten führen keinen Hebel „plus Bein“, dafür ist dieser weekend_check-Lauf da.

## Modus-Check und NT8 (Abschnitt 5 und 5b)

- **OpEx, Modus `cal` „geändert“:** der Code-Check für die Änderung (`cal_eod_flat`) ist erledigt, strategy-auditor 22.10. (go mit Auflagen, AP394). Nach Übernahme `weekend_check --stand-setzen`.
- **OpEx „nicht live-fähig“ ist ein Fehlalarm:** 5b vergleicht die Buch-Params wörtlich mit den Paritäts-Params. Die Parität vom 22.10. lief mit `cal_eod_flat` true und den Engine-Standards (`eod_flat_min` 385, `eod_flat_px` close, `qbt.run_strategy` mischt DEFAULTS ein). Die drei expliziten Werte sind also genau das, was geprüft wurde. Bei Übernahme in `nt8_port_status.json` unter `engine_extra` nachtragen, dann ist 5b grün.
- OpEx-Code (md5 3565f4e9) ist auf der Box, steht aber in keiner Host-JSON.
- **LD01 A live-fähig** (Parität 163/163), Code nur im Staging. Vor live laut Auditor: VIX-Feed eine Woche messen, externer Feed-Wächter, NT8-Bars an Feiertagen prüfen, Sim-Host-Lauf, FFN-HFT-Restrisiko (Max).

## Buch-Lücke je Bein

| Bein | was vor Live fehlt |
|---|---|
| OpEx | Entscheidung Max; JSON-Eintrag je Konto mit `skip_dates` 2027-06-18 und Exit-Reihenfolge; `MaxOpexMomNQ` in `gen_edge_ref` und LIVE_EXTRA bereinigen; Roll vor 18.12.; eigene Ausstiegsregel für ein Tail-Bein (expR-Regel greift erst nach ~7 Jahren) |
| LD01 A | Entscheidung Max; Deploy `deploy_ld01_20261024.ps1` (Max), VIX-Feed starten und eine Woche messen, Feed-Wächter, Feiertags-Bars, Sim-Host-Lauf, eigene Ausstiegsregel (expR-Regel greift erst nach ~3,3 Jahren) |

## Entscheidung Max 24.10. (Popup)

| # | Frage | Empfehlung | Max |
|---|---|---|---|
| 1 | LD01 A ins echte Buch? | ja (Quant-Team: empfohlen) | **ins Buch** |
| 2 | OpEx ins echte Buch? | im Next lassen, nicht live (nur vertretbar, Null im Band) | **ins Buch, alle Konten** |

strategy-auditor vor der Übernahme (24.10.): beide **go mit Auflagen**. OpEx-Params mit den drei Exit-Werten nachgerechnet, 78/78 Trades identisch zur Parität (9,667 R). Look-ahead im aktuellen `cal`-Code (Dateistand 22.10. 17:18) neu geprüft, sauber.

## Umsetzung 24.10.

- `book_state.json`: 6 Beine (PB3, LastHour, Asia, OpenDrive, OpEx mit 15:55-Exit, LD01 A), md5 90e5eaf7 → 0f3d3772. Beide neuen Beine tragen `since` „im echten Buch, noch NICHT live“ und eine `live_note` mit den Auflagen.
- `book_state_next.json`: gleich dem echten Buch (6 Beine), OpEx-Exit explizit, Protokoll-Eintrag 24.10., md5 e2ccf7ad → bdcf26df.
- `book_erstfassung.json`: OpEx-Erstfassung mit demselben 15:55-Exit, Stand 24.10.
- `nt8_port_status.json`: OpEx-Params um die drei Exit-Werte ergänzt, 5b wird damit grün.
- `live_finalize.py`: LIVE_EXTRA `OPEXMOM_NQ` raus (Regel vom 18.10.: raus, sobald OpEx im echten Buch ist).
- `funded_finalize.py` echt und `--next`, `live_finalize.py` echt und `--next`, `inbox_tool.py --push-next`, `weekend_check.py --stand-setzen`.
- Backups aller geänderten Dateien: `*.bak-20261024-wochenende` im Engine-Ordner.

## Was Max noch tun muss (vor dem ersten Live-Trade)

**LD01 A:**
1. Deploy `deploy_ld01_20261024.ps1` starten (außerhalb 09:00 bis 16:05 ET). Danach prüfen, dass die bestehenden Momentum-Instanzen unverändert laufen.
2. VIX-Feed starten (`install_vix_feed.ps1`) und eine Woche messen: der Vortagesschluss muss vor 09:40 ET da sein.
3. Externer Wächter auf das jüngste Datum in `maxlab_vix.csv`.
4. NT8-Bars an Feiertagen prüfen (2026-09-07, 2025-11-27), Sim-Host-Lauf.
5. FFN-HFT-Restrisiko bei Variante A bewusst entscheiden.
6. Erst dann LD01 in die Host-JSONs.

**OpEx** (erster möglicher Trade Fr 20.11.2026):
1. Eintrag in jede Host-JSON mit `skip_dates` 2027-06-18 und festgelegter Exit-Reihenfolge (Muster `maxlab_book_host.opexmom.example.json`).
2. Nachlaufend: Roll MNQ 12-26 vor Fr 18.12., 2027-Feiertage im RTH-Template (alle Beine), eigene Ausstiegsregel für ein Tail-Bein vor dem 2. Trade.

**Sonst aus dieser Prüfung:**
- E8 50k: Inaktivitäts-Frist 28.10., es fehlt 1 Handelstag.
- Sonntag vor dem Open prüfen, ob NT8 Hosts und RiskGuards wegen des Wochenend-Abbruchs abgeschaltet hat (AP413).
- Discovery-Queue seit 20.10. leer, `alpha-scout` wäre dran.
