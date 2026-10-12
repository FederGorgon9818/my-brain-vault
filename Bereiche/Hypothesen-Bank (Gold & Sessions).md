---
tags:
  - bereich/trading
  - trading/alpha
  - trading/hypothesen
  - trading/gold
erstellt: 2026-10-12
status: offen (drei Prämissen gerechnet, keine trägt, nichts auf der Box)
---
# 🧪 Hypothesen-Bank: Gold & Sessions

⬅️ [[Alpha-Suche]] · [[Neue Märkte (NT8-Daten) Plan]] · [[Discovery-Runner v2]] · Schwester-Banken: [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]]

> [!important] Was das ist
> Auftrag Max 12.10.2026: Gold nicht mehr mit NQ-Logik im NQ-Fenster testen, sondern mit eigenem Session-Anker und anderen Familien als „Bewegung setzt sich fort“. Herkunft: Strukturvergleich GC gegen NQ ([[Daily Notes/2026-10-12]], Zahlen `engine/_scratch_sip_orb/gc_diff.json`). Jede Zeile ist durch `ein-weg` gelaufen (variant-scout je Zeile, ein strategy-auditor-Batch, 12.10.2026). **Keine Zeile ist getestet, keine ging direkt auf die Box.**

> [!info] Was dafür seit 12.10.2026 in der Engine steht (AP197)
> Ein Job kann `session_start` / `session_end` setzen (ET, auch über Mitternacht). Die Bars werden auf den 09:30-Anker verschoben, alle Minuten-Angaben zählen ab Session-Beginn. Ohne die Angabe läuft der alte Weg. Auflagen vom `pipeline-auditor`:
> - `commission_rt=1.6`, `eod_flat_min` und `rv_eod_min` auf Session-Länge minus 5 (COMEX 08:20 bis 13:29: 304).
> - Keine Vorbörsen-, Nacht-, Europa-, Asien-, Fremdmarkt-Filter (`tm_pre*`, `tm_on_*`, `tm_eu*`, `tm_asia*`, `tm_xref_sym`, `tm_xadx_*`), kein `lh_exclude_news`, kein Hazard-Modell: die rechnen fest gegen 09:29 bzw. 390 Minuten.
> - **Nacht-Fenster dürfen erst rechnen, wenn das Buchungsdatum auf dem Ausstiegstag liegt** (sonst läuft der Buch-Abgleich einen Tag versetzt).

## Messwerte, auf die sich die Zeilen stützen

| Fenster (ET) | Varianz-Verhältnis 60 Min | 2016-19 | 2020-23 | 2024-26 | Anteil Varianz | Anteil Volumen |
|---|---|---|---|---|---|---|
| Asien 18:00 bis 02:59 | 0,89 | 0,89 | 0,88 | 0,90 | 28 % | 20 % |
| London 03:00 bis 08:19 | **0,79** | 0,75 | 0,81 | 0,79 | 20 % | 21 % |
| COMEX 08:20 bis 13:29 | 0,82 | 0,80 | 0,90 | 0,76 | 41 % | 49 % |
| NQ 09:30 bis 15:59 (Vergleich) | 0,90 | 0,89 | 0,90 | 0,91 | 61 % | 77 % |

Unter 1 heißt: Bewegungen laufen eher zurück als weiter. London ist am deutlichsten und über alle drei Abschnitte stabil. Asien liegt schon auf 5 Minuten bei 0,90, das riecht nach Spread-Rauschen statt handelbarer Umkehr.

## Die Zeilen

| ID | Idee | Familie | Stand nach ein-weg | Was fehlt bis zum Job |
|---|---|---|---|---|
| GC-ON-01 | Nacht-Halten: long ab 18:00 ET, Ausstieg 03:00, 05:30 oder 08:15 ET, tagsüber flat | Intraday Bias | **Prämisse trägt nicht (12.10.2026)**, kein Box-Job | Prämissen-Tafel `engine/_scratch_gc_nacht/premise.py`, 6 Configs (3 Ausstiege, je ohne Stop und mit Stop 1 ATR), MGC-Kosten 3,6 $. Netto 1 bis 3 $ je Nacht (t 0,3 bis 0,7, 90-%-Band schließt 0 ein), **4 von 11 Jahren positiv, vor 2024 minus 3 bis 4,5 $ je Nacht**, 2025/26 tragen alles. Überschuss gegen die anteilige Tagesdrift vor 2024 genau null. Größter Rückgang rund −9.000 $ je MGC. Der Datums-Umbau in der Engine wurde deshalb nicht gebaut. **Nicht gedeckt:** Vola- oder Wochentags-Bedingung, Einstieg später als 18:00, Short-Seite tagsüber. Kein Urteil gestempelt. |
| GC-MR-03a | Band-Fade London 03:00 bis 08:19 | Mean Reversion | **Prämisse trägt nicht (12.10.2026)**, kein Box-Job | Ausstieg „zurück zum Schnitt“ ist gebaut (`tm_exit="mid"`, `tm_stop_mode="band"`). Prämissen-Tafel `engine/_scratch_gc_london/premise.py`: 8 rechenbare Configs (Band 20/40, Breite 2,0/2,5, 5-Minuten-Bars, Stop 1 oder 2 Bandbreiten) brutto −0,02 bis +0,01 R (t höchstens 0,7), nicht besser als Zufallslevel und Münzwurf, netto −0,08 bis −0,26 R, Kosten 0,08 bis 0,27 R. Vor 2024 brutto leicht negativ, ab 2024 leicht positiv. 8 Configs mit 15-Minuten-Bars ohne Trades (Band braucht 300 Minuten Vorlauf in 320 Minuten Session). **Nicht gedeckt:** Band mit Vorlauf aus der Asien-Session, andere Auslöser als Bollinger (Kanal, VWAP), Haltedauer über die Session hinaus. Kein Urteil gestempelt. |
| GC-MR-03b | Band-Fade Asien 18:00 bis 02:59 | Mean Reversion | hält mit Vorbehalt, schwächer | Wie 03a, dazu Nacht-Auflage (Buchungsdatum). Messung oben spricht eher für Spread-Rauschen. |
| GC-MR-02 | VWAP-Rückkehr in der COMEX-Session, Ziel VWAP | Mean Reversion | **Prämisse trägt nicht (12.10.2026)**, kein Box-Job | Prämissen-Messung `engine/_scratch_gc_vwap/premise.py`: Schwelle 2,0 / 2,5 Sigma, Stop 1 oder 2 Abstände, VWAP und Sigma nur aus Bars bis zum Signal, je mit Zufallszeit-Placebo. Brutto −0,4 bis +1,1 $ je Trade (t höchstens 1,0), nicht besser als das Placebo, netto −2,5 bis −4,0 $, 1 von 11 Jahren positiv. Der Ausstieg wurde im Skript gemessen, nicht in `maband` gebaut. Kein Urteil gestempelt. |
| GC-NEWS-01 | 08:30-Sprung an Datentagen faden, Ausstieg 10:00 ET | Mean Reversion | hält mit Vorbehalt, **blockiert** (48 Varianten) | Echter Datentag-Kalender für GC (Wiedervorlage aus #180b). Schalter „nur Event-Tage“ im Umkehr-Modus. Prämissen-Messung 08:35 bis 10:00 brutto nach Sprunggröße. Rund 250 Events, dünne Power. |
| GC-MR-01 | Umkehr nach großer COMEX-Eröffnungsbewegung | Mean Reversion | **nicht bauen (Story)** | 49 % Fortsetzung ist ein Münzwurf, keine Umkehr. Spiegelbild von #180b, dort war Mitgehen brutto leicht positiv, ein Fade startet also im Minus. |
| GC-TOD-01 | Mittags-Schwäche 11:30 bis 13:30 ET short | Intraday Bias | **nicht bauen (Story)** | Ein Block aus sieben, nachträglich ausgesucht, kein Akteur. Kehrseite von GC-ON-01, kein zweiter Mechanismus. |
| GC-RV-01 | Gold gegen Zins- und Dollar-Residuum faden | Relative Value | **nicht bauen (Story)** | Story kennt ihr Vorzeichen nicht. Kein Vorlauf auf 5 Minuten, Zins-Kopplung fällt von 0,46 auf 0,24. Neuer Engine-Modus dafür zu teuer. |

## Reihenfolge (Vorschlag)

1. ~~GC-MR-03a London-Band-Fade~~: Prämisse gerechnet, trägt nicht (siehe Tabelle). Das Varianz-Verhältnis 0,79 auf 60 Minuten wird vom Band-Fade auf 5-Minuten-Bars nicht eingefangen.
2. ~~GC-ON-01 Nacht-Halten~~: Prämisse gerechnet, trägt nicht (siehe Tabelle). Die +42 % „Asien“ aus dem Strukturvergleich waren fast ganz 2024 bis 2026.
3. ~~GC-MR-02 VWAP-Rückkehr~~: Prämisse gerechnet, trägt nicht (siehe Tabelle).
4. GC-NEWS-01 erst mit Kalender.

**Buch-Lücke für alle Zeilen:** noch vor Stufe 1. Es gibt keinen Job, keine Prämisse, keinen Trial.

## Was auf Gold von den Kosten her geht (12.10.2026, `engine/_scratch_gc_vwap/kosten.py`)

Kosten je Trade geteilt durch die typische Bewegung über die Haltedauer. Das ist die Vorhersagegüte, die ein Signal mindestens braucht, um die Kosten zu decken. Unsere beste gemessene Güte auf Gold liegt bei 6,8 % (TD-12, #180c).

| Haltedauer | MGC 2016 bis 2023 | MGC 2024 bis 2026 | GC voll 2016 bis 2023 | MNQ 2016 bis 2023 |
|---|---|---|---|---|
| 5 Min | 28,5 % | 9,0 % | 19,4 % | 7,8 % |
| 15 Min | 16,4 % | 5,1 % | 11,1 % | 4,6 % |
| 30 Min | 11,4 % | 3,6 % | 7,8 % | 3,2 % |
| 60 Min | 8,0 % | 2,7 % | 5,4 % | 2,3 % |
| 120 Min | 5,3 % | 1,8 % | 3,6 % | 1,6 % |
| 300 Min | 3,6 % | 1,2 % | 2,4 % | 1,0 % |

Annahmen: MGC 1 Tick je Seite plus 1,6 $ = 3,6 $, GC voll 1 Tick je Seite plus 4,5 $ = 24,5 $, MNQ 2,02 $. COMEX-Fenster. London und Asien sind je Bewegung 1,5- bis 2-mal so teuer wie COMEX. Limit-Einstieg spart rund 28 %.

**Lesart:** bis 2023 war auf MGC alles unter etwa 2 Stunden Haltedauer rechnerisch kaum zu bezahlen. Seit 2024 liegt Gold bei den Kosten dort, wo NQ lag, als wir die NQ-Beine gefunden haben. Ein Backtest über 10 Jahre mittelt beides und wird von den teuren acht Jahren dominiert.

**Was daraus für die Suche folgt:** lange Haltedauer (2 Stunden bis ganze Session), höchstens ein Trade am Tag, COMEX-Fenster, Einstieg per Limit wo möglich, und ein Vola-Schalter (nur handeln, wenn die Kostenquote unter etwa 3 % liegt). Reine Preis-Signale in diesem Raster sind inzwischen in beide Richtungen gemessen und brutto null (Fortsetzung #174/#180b, Umkehr heute). Offen bleibt nur Information von außen: Datentage mit Kalender (GC-NEWS-01) und Zins-/Dollar-Vorlauf unter 1 Minute.
