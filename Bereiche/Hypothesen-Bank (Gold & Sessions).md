---
tags:
  - bereich/trading
  - trading/alpha
  - trading/hypothesen
  - trading/gold
erstellt: 2026-10-12
status: offen (nichts getestet, nichts auf der Box)
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
| GC-ON-01 | Nacht-Halten: long ab 18:00 ET, Ausstieg 03:00 oder 05:30 ET, tagsüber flat | Intraday Bias | **hält mit Vorbehalt, stärkste Story** (24 Varianten, grenzwertig) | Buchungsdatum = Ausstiegstag in der Engine. Nulldrift-Zwilling und Schnitt vor 2024 als Pflichtteil im Job. Vola-Filter nur als markierte Zusatzachse (Falle aus #178). Literatur-Beleg in den [[Research-Cache]]. E8-Bestätigung „Nacht ab 18:00“ steht nur abgeleitet in [[Firm-Regeln je Konto]]. |
| GC-MR-03a | Band-Fade London 03:00 bis 08:19 | Mean Reversion | **hält mit Vorbehalt** (zusammen mit 03b 144 Varianten) | Ausstieg „zurück zum Schnitt“ existiert in `maband` noch nicht. Akteur ins Why. Messung oben stützt London (0,79, stabil). |
| GC-MR-03b | Band-Fade Asien 18:00 bis 02:59 | Mean Reversion | hält mit Vorbehalt, schwächer | Wie 03a, dazu Nacht-Auflage (Buchungsdatum). Messung oben spricht eher für Spread-Rauschen. |
| GC-MR-02 | VWAP-Rückkehr in der COMEX-Session, Ziel VWAP | Mean Reversion | **hält mit Vorbehalt** (144 Varianten) | Ausstieg „Ziel VWAP“ bauen. VWAP und Sigma nur aus Bars bis zum Einstieg. Erst Prämisse auf Schwelle 2,0 und 2,5 Sigma plus Placebo mit Zufallszeit, dann das Grid. Vorbelastung: VWAP-Abstand war auf NQ und in #174 Regime, kein stabiler Filter. |
| GC-NEWS-01 | 08:30-Sprung an Datentagen faden, Ausstieg 10:00 ET | Mean Reversion | hält mit Vorbehalt, **blockiert** (48 Varianten) | Echter Datentag-Kalender für GC (Wiedervorlage aus #180b). Schalter „nur Event-Tage“ im Umkehr-Modus. Prämissen-Messung 08:35 bis 10:00 brutto nach Sprunggröße. Rund 250 Events, dünne Power. |
| GC-MR-01 | Umkehr nach großer COMEX-Eröffnungsbewegung | Mean Reversion | **nicht bauen (Story)** | 49 % Fortsetzung ist ein Münzwurf, keine Umkehr. Spiegelbild von #180b, dort war Mitgehen brutto leicht positiv, ein Fade startet also im Minus. |
| GC-TOD-01 | Mittags-Schwäche 11:30 bis 13:30 ET short | Intraday Bias | **nicht bauen (Story)** | Ein Block aus sieben, nachträglich ausgesucht, kein Akteur. Kehrseite von GC-ON-01, kein zweiter Mechanismus. |
| GC-RV-01 | Gold gegen Zins- und Dollar-Residuum faden | Relative Value | **nicht bauen (Story)** | Story kennt ihr Vorzeichen nicht. Kein Vorlauf auf 5 Minuten, Zins-Kopplung fällt von 0,46 auf 0,24. Neuer Engine-Modus dafür zu teuer. |

## Reihenfolge (Vorschlag)

1. **GC-MR-03a London-Band-Fade**: einzige Umkehr-Zeile mit stabiler Messung dahinter, kein Nacht-Problem, braucht nur den Schnitt-Ausstieg.
2. **GC-ON-01 Nacht-Halten**: stärkste Story, braucht den Datums-Umbau.
3. **GC-MR-02 VWAP-Rückkehr**: nach der Prämissen-Messung.
4. GC-NEWS-01 erst mit Kalender.

**Buch-Lücke für alle Zeilen:** noch vor Stufe 1. Es gibt keinen Job, keine Prämisse, keinen Trial.
