---
tags: [trading, ausfuehrung, live, entscheidung, ap426]
datum: 2026-10-18
status: entschieden 18.10.2026 (Option A umgesetzt, B' später als AP428)
ticket: AP426
---

# 15:55-Zeit-Exit: Entscheidungsvorlage (AP426)

> [!success] Entschieden 18.10.2026, umgesetzt 23:15
> Max: „A jetzt, B' später prüfen". Engine-Standard `eod_flat_px` = „close", Golden Master neu eingefroren, Box-Sync 23:13, Runner läuft, Konto-Karten neu (Flotte Netto 36 M 10.358 auf 9.519 $, Ampel überall grün k1). Tick-Daten: AP427 (Max, Anleitung im Ticket). B': AP428, erst nach den Ticks. Details [[Strategie-Logbuch]] #187a.

Live füllt der Zeit-Exit um 15:55 im Mittel **33,7 Ticks** schlechter als der Backtest annimmt (Echtgeld, 10 Tage 21.09. bis 15.10.). Betroffen sind die drei Beine mit Exit am Tagesende: am stärksten LastHour. Logbuch: [[Strategie-Logbuch]] #187.

## Was wirklich passiert

- Der Host löst den Zeit-Exit **am Bar-Close** der Minutenbar aus, also um 15:55:00,1 bis 0,6. Dann storniert er erst den Stop (fertig bis 15:55:01,3) und schickt danach Market. **Fill 1,0 bis 4,2 s nach 15:55:00** (NT8-Log, Millisekunden).
- Genau in diesen Sekunden springt der Preis. Beleg: am 07.10. füllt das Sim-Konto um 15:55:01,971 bei 31398,75, das echte E8-Konto 7 ms später bei 31403,75. Der NT8-Feed hängt im Burst hinterher, die Börse ist schon weg. Am 05.10. dasselbe mit 41 Ticks.
- Der Burst beginnt erst ab 15:55:00: letzter Preis vor 15:55 und erster danach liegen im Mittel 0,4 Ticks auseinander.
- Über 10 Jahre (1m-Daten) laufen die Minuten 15:53 und 15:54 **für** unsere Positionen, die 15:55-Minute **gegen** sie: LastHour +4, OpenDrive +8, PB3 +7 Ticks je Trade.

## Wie groß ist es wirklich (Quant-Team)

- **Dass es Zusatzkosten gibt, ist belastbar** (alle Tests p 0,02 bis 0,04, robust gegen Ausreißer).
- **Die 31 bis 34 Ticks sind nicht die Erwartung.** Rund 29 davon sind die zufällig schlechte 15:55-Minute genau dieser 10 Tage (gegen 2026 p 0,11, kein Strukturbruch). Ehrliche Planzahl: **10 bis 13 Ticks je Trade**, Obergrenze rund 28.
- Der echte Regimewechsel ist die Vola: die 15:55-Minute schwankt heute gut doppelt so stark wie 2016 bis 2023 (Range 37 auf 90 bis 94 Ticks).

## Was es kostet (k1, je Konto mit allen drei Beinen)

| Modell | LastHour | OpenDrive | PB3 | Summe $/Jahr | Anteil |
|---|---|---|---|---|---|
| Backtest bisher (Fill am Open 15:55) | 1.453 | 1.538 | 2.054 | 5.045 | |
| Fill am Close der 15:55-Bar (Historie) | −149 | −81 | −70 | −299 | −5,9 % |
| Planzahl inkl. Live-Rest (EB) | −401 | −89 | −111 | −601 | −11,9 % |
| Live-Rohwert 31 Ticks hochgerechnet | −1.148 | −353 | −292 | −1.793 | −35,5 % |
| fest raus 15:54:00 | −244 | −50 | −80 | −374 | −7,4 % |
| fest raus 15:50:00 | −249 | −79 | −112 | −439 | −8,7 % |

Stufe 1 hält mit dem realistischen Modell bei allen drei Beinen (t LastHour 3,23, OpenDrive 4,34, PB3 3,92, positive Jahre unverändert: LastHour 7, OpenDrive 11, PB3 10 von 11).

**Zeit bis 50k, echtes Buch** (Kalender-Modus, RiskGuard-Tagesstopp, 600 Sims, Nulldrift-Zwilling überall 0 %, Auslage p90 1.332 $ gleich):

| Modell | erreicht in 120 M | Median | gegen bisher |
|---|---|---|---|
| bisher (Open 15:55) | 83,0 % | 96,7 M | |
| Close der 15:55-Bar | 75,7 % | 101,0 M | +4,3 ±1,0 M |
| Close + 5 Ticks (Stress) | 65,2 % | 108,9 M | +12,2 ±1,1 M |

## Optionen

**A. Ausführung bleibt, Backtest wird ehrlich** ⭐ Empfehlung
- Engine-Standard `eod_flat_px` von „open" auf „close" (Parameter ist gebaut, Golden Master grün, Standard steht noch auf „open").
- Kein NT8-Eingriff. Bücher, Konto-Karten, Discovery und `weekend_check` rechnen danach mit dem, was live heute passiert.
- Mit Auflagen vom `pipeline-auditor`: Register-Stempel für `eod_flat_px`, Kanarie für den Close-Modus, Runner sauber stoppen, Sync, Golden Master neu einfrieren, Konto-Karten neu, Next-Beine OpEx/LD01 neu rechnen. Etwa ein halber Tag Arbeit, alles Claude.
- `strategy-auditor`: go mit Auflagen.

**B'. Später zusätzlich: Exit vor 15:55 als gepaarter Live-Versuch**
- Host-Änderung: Exit per Wanduhr so, dass der letzte Exit spätestens 15:54:50 gesendet ist, Staffel rückwärts mit 15 s Abstand (FFN-HFT-Regel bleibt eingehalten), LastHour als letztes. Neuer Config-Schlüssel je Konto, Standard = heutiges Verhalten.
- Nur auf einem Teil der Konten (zum Beispiel FN1 und FFN2), die anderen bleiben bei 15:55:00. Gleicher Trade, gleicher Tag, dadurch sehr scharfer Vergleich.
- Erwartung: historisch +4 Ticks je Trade (rund +300 $/Jahr je Konto), wenn der Live-Burst so groß bleibt bis +30. Risiko: ab 2024 ist der Vorteil nicht mehr signifikant (t 0,83), und früheres Senden verschenkt einen Teil der guten 15:54-Minute.
- Abbruch sofort bei Fill nach 15:55:00,5 an mehr als 2 Tagen, falscher ET-Uhrzeit, Position nach 15:58, Doppel-Exit oder Round-Trip unter 5 s. Entscheidung nach 20 gepaarten Tagen (Übernahme ab +3 Ticks mit unterer CI90-Grenze über 0).
- **Nicht zwischen 25.10. und 01.11.** (Zeitumstellung EU vor USA). Vorher Tick-Daten (siehe unten).
- `strategy-auditor`: B direkt auf allen Konten ist **No-Go**, B' als Versuch go mit Auflagen.

**C. Fest früher raus (15:54:00 oder 15:50)** verworfen: kostet bei LastHour mehr als der Status quo.

**D. Limit statt Market** verworfen: Hebel höchstens ±0,5 Tick, dafür adverse Selektion.

## Empfehlung

**A jetzt**, dazu **Tick-Daten für 2 bis 3 Live-Tage** (NT8, Markt zu, Max per RDP), um die Sekunden 15:54:30 bis 15:55:05 direkt zu sehen. Erst wenn die Ticks zeigen, dass die guten Sekunden vor 15:55 liegen und der Sprung danach, **B' als Versuch** bauen. Grund: A macht den Backtest heute ehrlich und kostet nichts am Konto, B' ist ein Eingriff in den Live-Code für einen Vorteil, der ab 2024 statistisch nicht mehr sicher ist.

## Was schon erledigt ist

- Engine: Parameter `eod_flat_px` in `qbt.py`, `sigcore.py`, `vwap_pullback.py`, unbekannte Werte brechen hart ab, MAE-Regel im Close-Modus. Standard „open" bitgleich, **Golden Master grün** (9 Fälle exakt, alle Kanarien, 9 Selbsttests). Kein Box-Sync, der gehört zur Umstellung.
- Prüfer: quant-mathematician, quant-statistician, pipeline-auditor (gelb, Auflagen), strategy-auditor, engine-regression-tester, logbook-distiller.
- Workbench: drei Karten „AP426_…_flat_close" im Lab unter Tests.
- Rechnungen und Skripte: `engine/_scratch_ap426/`.

## Offen, nicht Teil der Entscheidung

- Am 13.10. zwei Exit-Fills auf FN1 im Abstand von 1,35 s: das ist der Doppel-Exit aus AP382 (Fix am 16.10. deployt), hier nur als Gegenprobe vermerkt.
- Why der 15:55-Umkehr ist offen (Börsen-Fristen 15:50/15:55 nicht aus Primärquelle geprüft).
- Halbtage: Exit am letzten Close, nicht kalibriert.
