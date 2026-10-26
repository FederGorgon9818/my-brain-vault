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

## Nachtrag 22.10.2026: neuer Live-Tag, Close-Modell bestätigt, Tick-Skript bereit

- **Stand:** Option A läuft seit 18.10. (Engine füllt den 15:55-Flat am Close der 15:55-Bar). Nichts davon neu gerechnet. Offen sind nur der Tick-Befund (AP427, Max) und danach B' (AP428).
- **20.10., 5 Echtgeld-Konten, LastHour long:** die Fills kamen diesmal schon **0,5 bis 1,0 s** nach 15:55:00 (vorher 1,0 bis 4,2 s). Trotzdem **+35 Ticks schlechter als der Open** der 15:55-Bar und 42 Ticks besser als ihr Close. 38 % der Abwärtsbewegung der ganzen Minute war schon in der ersten halben Sekunde passiert, Volumen der 15:55-Minute 1,6x der 15:54-Minute. Bars aus Yahoo NQ=F 1m, weil die NT8-Daten am 16.10. enden.
- **Heißt:** der Sprung sitzt in der ersten halben Sekunde nach 15:55:00. Schneller ausführen bringt nichts. Helfen kann nur ein Exit vor 15:55:00, also B'.
- **Das Close-Modell passt:** über 11 Echtgeld-Tage liegt Live im Mittel **+0,8 Ticks** neben dem Close der 15:55-Bar (Median −2, t 0,08), gegen den Open +33,8 Ticks (t 3,2). Die Engine-Annahme seit 18.10. trifft also im Mittel.
- **Tick-Skript fertig:** `engine/_scratch_ap426/tick_burst.py "<NT8-Tick-Export>"` misst je Live-Tag den Preis von 15:54:00 bis 15:56:00 gegen die Position (15:54:30, :45, :50, :55, 15:55:00, +0,25 s bis +30 s), Volumen je Sekunde und ab wann der Preis 10 Ticks weg ist, mit Zeitzonen-Gegenprobe gegen die 1m-Bars. Mit künstlichen Daten getestet. Sobald die Ticks auf der Box liegen, ist der Befund ein Aufruf.
- **Why, wahrscheinlich die Nasdaq-Schlussauktion:** um 15:55:00 ET endet bei Nasdaq der MOC-Cutoff des Closing Cross, und der Imbalance-Feed (NOII) läuft ab da jede Sekunde statt alle 10 s, erstmals mit dem Preis, zu dem die Auktion gerade laufen würde (Primärquellen Federal Register 2019, Nasdaq-FAQ). NQ hängt am Nasdaq-100, das passt zum Zeitpunkt. NYSE hat ihren Schnitt um 15:50, nicht um 15:55. **Die Größe von rund 35 Ticks erklärt keine Quelle**, eine Studie zur Reaktion von NQ in Sekunden gibt es nicht. Details im [[Research-Cache]], Abschnitt „Closing Cross, MOC-Cutoffs und Imbalance-Feeds“.
- **Für B' heißt das:** ist der Auslöser die Nasdaq-Veröffentlichung um 15:55:00, liegt er fest auf der Uhr, und ein Exit vor 15:55:00 umgeht ihn. Die Ticks (AP427) müssen das noch bestätigen.
- Rechnungen: `engine/_scratch_ap426/` (Fill-Abgleich `fills_vs_bars.csv` plus 20.10. aus dem NT8-Log der Box).

## Nachtrag 26.10.2026: zwei weitere Live-Tage, Sprung geht in beide Richtungen

- **23.10.:** Fill 0,6 bis 1,4 s nach 15:55:00, nur +1,8 Ticks gegen den Open der 15:55-Bar. **26.10.:** Fill 0,9 bis 1,8 s, **40 Ticks besser** als der Open. Beide Male LastHour long auf allen 5 Konten, Bars aus Yahoo NQ=F 1m.
- **Über 13 Echtgeld-Tage:** gegen den Open +25,6 Ticks im Mittel (Median +34,6, t 2,4), gegen den Close der 15:55-Bar −6,0 (t −0,65). Das Close-Modell der Engine liegt damit weiter im Rauschen, eher leicht zu vorsichtig.
- **Korrektur zum 22.10.:** in der ersten Sekunde nach 15:55:00 springt der Preis stark, aber nicht immer gegen uns. Im Mittel kostet es, die Streuung ist groß (sd 38 Ticks). Ob ein Exit vor 15:55:00 die Kosten spart oder nur die Streuung, zeigen erst die Ticks (AP427).
- **Ticks:** die Ticks vom 10.09. bis 22.10. liegen schon in NT8 auf der Box (am 22.10. geladen), es fehlen 23.10. und 26.10. Neue Anleitung in AP427 (Download der zwei Tage, Export 21.09. bis 26.10.). `tick_burst.py` deckt jetzt alle 13 Live-Tage ab und erkennt die Zeitzone des Exports selbst, `box_tick_filter.py` kürzt den Export auf der Box auf 15:40 bis 15:59.

## Offen, nicht Teil der Entscheidung

- Am 13.10. zwei Exit-Fills auf FN1 im Abstand von 1,35 s: das ist der Doppel-Exit aus AP382 (Fix am 16.10. deployt), hier nur als Gegenprobe vermerkt.
- Why der 15:55-Umkehr: Zeitpunkt seit 22.10. mit Primärquelle erklärt (Nasdaq 15:55, siehe Nachtrag), Größe weiter offen.
- Halbtage: Exit am letzten Close, nicht kalibriert.
