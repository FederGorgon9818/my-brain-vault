---
tags: [projekt, trading, alpha-suche, politiker-kaeufe, juli-modus]
erstellt: 2026-10-12
aktualisiert: 2026-10-12
status: aktiv
ziel: Zeit bis 50.000 $ Eigenkapital aus Payouts verkürzen (Gate v4), oder das Kapitel Politiker-Käufe mit Reichweite schließen
---

# Politiker-Käufe Wege-Karte

**Ziel (einziges Kriterium, seit 18.09.2026):** verkürzt der Weg die **Zeit bis 50.000 $ Eigenkapital aus Payouts** bei begrenzter Auslage? Übersetzt in Gate v4 Stufe 1: allein profitabel nach Kosten, Walk-Forward mit Neuauswahl bestanden, **Buch-Sharpe steigt**, Passquote höchstens −3 pp. Die Passquote je Eval ist nur noch Zwischengröße. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, neues Bein oder nur Live-Buch-Merker?**

Angelegt am 12.10.2026 vom `familien-scout`. Quelle des Konzepts: Max, [[Testphase Juli-Modus]] Idee 5 („kaufen, wenn Politiker kaufen“, US-Kongress, STOCK-Act-Offenlegungen). Eine Hand-Karte zum selben Konzept gibt es nicht. Aufbau nach dem Vorbild [[VWAP-Offensive]].

**Nachtrag 12.10.2026 (nach `verdict-auditor`):** sieben neue Wege W21 bis W27, Stände und Marken bei W4, W8, W10, W11, W13, W14, W17, W20 korrigiert, übersehene Verwandte nachgetragen, Kopf und Randbedingung 3 auf den Stand nach dem 18.09. gebracht. W1 bis W20 behalten ihre Nummern. Die alte Zielzeile („v2-Passquote je Eval“) war aus der VWAP-Vorlage mitkopiert und ist ersetzt.

**Rückschreibung Research 12.10.2026 (Workflow `konzept-weg`, nach `research-scout`):** Research-Stand je Skelett eingetragen, siehe Abschnitt „Research-Stand“. POL-W13a und POL-W11a: **Research widerlegt**, das ist kein Tot-Stempel (tot nur nach vollem Test). POL-W21a, POL-W1a, POL-W10a: offen. **Kein Skelett geht in dieser Runde an `ein-weg`.** Kein Weg gelöscht, keine Nummer geändert.

> [!warning] Die Lage in einem Satz
> Das Konzept ist bei uns **komplett unberührt und heute nicht rechenbar**: 0 Trials, 0 Bank-Zeilen, 0 Logbuch-Einträge, 0 Zeilen im Research-Cache, keine Kongress-Daten, keine Aktien-Daten. Max' eigentliche Idee (die Aktie nachkaufen) ist ein Swing-Weg und im Prop-Rahmen nicht handelbar. Prop-fähig ist nur der Umweg über ein Tages-Tor auf Index-Futures, und dessen Story ist die schwächste der Karte. Der Horizont, der zum Signal passt (Index-Future über Wochen, W21), ist mit unseren Futures-Daten rechenbar, aber Prop verbietet ihn.
>
> **Nach Research (12.10.2026):** der [[Research-Cache]] hat jetzt Einträge. Die Literatur stützt keinen der beiden prop-fähigen Wege (W13, W11: Research widerlegt, Aggregat-Effekt nur vor 2012 belegt und auf Monats-Horizont). Gerechnet ist weiterhin nichts: 0 Trials, keine Daten.

---

## Harte Randbedingungen

1. **Keine Daten.** `exported_data/` enthält an Tagesreihen nur `DIX_GEX_daily.csv`, `VIXCLS.csv`, `DGS2.csv`, `DGS10.csv`, `DTWEXBGS.csv`. Kein Kongress-Datensatz, keine Aktien, keine ETFs. Vor jedem Weg steht Daten-Spec **D-POL-1**.
2. **Nur das Offenlegungsdatum ist handelbar.** Das Transaktionsdatum liegt bis zu 45 Tage davor. Jede Reihe muss auf Offenlegungsdatum gebaut und um einen Tag verschoben werden, sonst Look-ahead. Quellen, die nur das Transaktionsdatum führen, sind unbrauchbar.
3. **Prop-Konten: kein Halten über den Tagesschluss, die Nacht-Session ist aber nicht überall zu.** Stand [[Firm-Regeln je Konto]]: **E8** verbietet das Halten über den Tagesschluss (Zwangs-Flat 16:10 ET), erlaubt es aber innerhalb des Handelstags 18:00 bis 16:10 ET, also auch die Nacht ab 18:00 bis zum Open (Mail 01.10.2026, die Nacht-Folgerung ist nicht wörtlich bestätigt). **FN-Futures:** Overnight verboten, Auto-Close 16:10 ET. **FFN** (Konto seit 05.10.2026): flat bis 16:50 ET, wieder auf ab 18:00 ET. Folge: alle Aktien- und Mehrtages-Wege sind Live-Buch-Merker, ein Nacht-Weg (W23) ist bei E8 nicht verboten.
4. **Kein neuer Modus.** Außerhalb der Modi mit Null-Schalter wird nichts `deploy_ready` ([[Strategie-Logbuch]] #139, Eintrag vom 01.09.2026, B1). Der einzige saubere Engine-Weg ist ein Tages-Tor in `sigcore.gates_pass`. Das lesen heute **nur `tsmom` und `maband`** (Grep 12.10.: `asian.py` 0 Fundstellen, `qbt.py` mit dem Gap-Modus 0 Fundstellen). Vorlage: Modul-Spec B aus #163 (Zins und Dollar als Tageszustand, mit Registrierung in `controls.py`).
5. **Feasibility vor dem ersten Trial.** Ein 30-Tage-Aggregat ist stark autokorreliert. Bei rund 2.600 Handelstagen seit 2016 bleiben grob 85 unabhängige Blöcke. #163 Lehre 168: erst `overfit.feasibility_gate()`. Härter noch #139 (31.08.2026): bei einem Tages-Tor bindet die Zahl unabhängiger **Episoden**, nicht die Tageszahl, „mehr Grid hilft nicht, nur mehr Jahre“.
6. **Long-Drift.** Ein Tor, das nur Long-Tage freigibt, sieht auf NQ immer gut aus. Vergleich gegen den ungefilterten Arm und gegen die Inversion, Nulldrift-Zwilling mit dem Long-Anteil des Kandidaten. Dazu der Off-Tage-Malus aus #139 (31.08.): zufälliges Abschalten kostet unter dem Trailing-DD-Käfig monoton, ein Tor muss das erst aufholen.
7. **Meldungen tragen nur Betrags-Bänder** (keine exakten Dollar). Jede Dollar-Gewichtung ist eine Schätzung, die Zählung der Meldungen ist die robustere Reihe.

---

## Register-Stand (12.10.2026)

| Griff | Zahl |
|---|---|
| Register gesamt (`inbox_tool.py`, Decke global) | **69.585 Trials** |
| Trials zum Konzept (Zähler `cong`, `politi`, `insider` im Register) | **0** |
| Bank-Zeilen (6 Banken, `hypothesis_bank.py`) | **0** |
| Logbuch-Einträge | **0** |
| Research-Cache (Nachtrag erneut gegriffen) | **0 Zeilen** bei Anlage; nach `research-scout` am 12.10. gefüllt (7 Fundstellen für `Karadas`, `NANC`, `STOCK Act`) |
| `ideas.json` (75 Karten) | **0** zum Konzept, vier verwandte Karten (siehe Verwandte) |
| Verwandte Tages-Tore im Register (Textfundstellen, keine Trial-Zählung) | `tm_vix_` 600, `tm_gex` 59, `tm_dgs10` 4, `tm_dxy` 4, `tm_dix_` 0, `tm_dgs2` 0 |
| Buch live (`book_state.json`) | NQ_Momentum_PB3_fa01b (tsmom), NQ_LastHour_v3 (last_hour), NQ_Asia-Dir-USopen_d260820 (asian), NQ_OpenDrive_maband2050 (maband) |
| Next-Week-Buch (`book_state_next.json`) | die vier Live-Beine **plus** `gen_gap_RTY_r1_08242126_v4re_d261002` (Gap-Modus, RTY) |

Das Tor `tm_dix_min/max` ist in `controls.GATE_OFF` registriert, hat im Register aber 0 Fundstellen: der nächste Verwandte („informierte Käufer als Tageszustand“) wurde nie als Job gerechnet, nur als Regression (#110).

---

## Elemente und Beziehungen

**Elemente:** Einzelmeldung (Ticker, Kauf oder Verkauf, Betrags-Band, Person), Transaktionsdatum, Offenlegungsdatum, Verzug dazwischen, Aggregat (Netto-Kauf über alle Meldungen), **Aktivität (Käufe plus Verkäufe, unabhängig vom Netto)**, Sektor-Mix, Untergruppe (Ausschuss, Führung, Top-Performer, **Partei, Kammer**), Cluster (mehrere Personen, ein Ticker), Copycat-Vehikel (NANC, KRUZ), dazu der Preis von Aktie, Sektor und Index-Future (**NQ, ES, RTY, YM; RTH, Nacht-Session, Mehrtages-Horizont**).

**Bewegungen:** Preis läuft nach dem Ereignis weiter, springt und läuft zurück, reagiert gar nicht, läuft dagegen (Fade); Aggregat ist hoch, niedrig, dreht; **Aktivität ist eng, weit, flach**; Sektor-Mix kippt. Jede Bewegung mal Richtung ist ein Weg. Rollen: Signal, Filter, Zeitfenster, Exit, **Sizing**.

---

## Wege-Tabelle

Marken: **(Swing)** = nur auf Mehrtages-Horizont sinnvoll, Prop verboten. **(Aktie)** bzw. **(ETF)** = nicht Prop, weil das Instrument fehlt, unabhängig von der Haltedauer.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W1** (Swing, Aktie) | Aktie läuft nach Kauf-Offenlegung weiter, long | Swing | Signal | offen (Research 12.10.: nach 2012 gemischt) | keiner, keine Aktien-Daten | Live-Buch-Merker |
| **W2** (Swing, Aktie) | Aktie fällt nach Verkaufs-Offenlegung weiter, short | Swing | Signal | offen, keine Story | keiner | Live-Buch-Merker |
| **W3** (Swing, Aktie) | Käufe long gegen Verkäufe short, marktneutral | Relative Value | Signal | offen, Messform von W1 | keiner | Live-Buch-Merker |
| **W4** (Aktie) | Aktie springt am Offenlegungstag und läuft zurück, Sprung faden (intraday bis Folgetag) | Mean Reversion | Signal | offen | keiner, keine Aktien-Intraday-Daten | Live-Buch-Merker wegen Instrument, nicht wegen Haltedauer |
| **W5** (Swing, Aktie) | Cluster: mehrere Personen kaufen denselben Titel | Swing | Filter auf W1 | offen | keiner | Live-Buch-Merker |
| **W6** (Swing, Aktie) | Nur Untergruppe: Ausschuss, Führung, Top-Performer, Partei, Kammer | Swing | Filter auf W1 | offen | keiner | Live-Buch-Merker |
| **W7** (Swing, Aktie) | Verzug kurz gegen lang | Swing | Zeitfenster auf W1 | offen | keiner | Live-Buch-Merker |
| **W8** (Swing, Aktie) | Einstieg am Transaktionsdatum | Swing | Signal | keine Story, nicht handelbar | keiner | keiner |
| **W9** (Swing, Aktie) | Großer Betrag oder Optionen als Überzeugungs-Maß | Swing | Filter auf W1 | offen | keiner | Live-Buch-Merker |
| **W10** (Swing, ETF) | Copycat-ETF NANC/KRUZ gegen SPY/QQQ messen | Swing | Messung, kein Signal | offen, Vorab-Messung für W1 (Research 12.10.: keine faktorbereinigte Rechnung gefunden) | keiner, keine ETF-Daten | Live-Buch-Merker |
| **W11** | Aggregat hoch, Index läuft intraday nach oben, long | Intraday Bias | Signal | Research widerlegt als Intraday-Lesart (Karadas 2021/2022, Horizont-Mismatch), kein Tot-Stempel | `tsmom` long plus Tor, Modul-Spec S-POL-1 | neues Bein (Warnung #139 B3) |
| **W12** | Aggregat tief (Netto-Verkauf), Index läuft intraday nach unten, short | Intraday Bias | Signal | offen, keine Story | wie W11 | keiner |
| **W13** | Aggregat als Tages-Tor auf ein bestehendes Bein, long | Filter | Filter | Research widerlegt (Karadas/Schlosky/Hall JRFM 2021), kein Tot-Stempel | `sigcore.gates_pass`, Modul-Spec S-POL-1 | Ersatz für NQ_Momentum_PB3_fa01b |
| **W14** | Aggregat dreht von Verkauf auf Kauf | Filter | Filter | offen, Achse von W13 | `_chg`-Reihe in S-POL-1 | wie W13 |
| **W15** | Sektor-Mix kippt Richtung Tech, NQ gegen ES/RTY | Relative Value | Filter | offen, Story schwach | Tor auf NQ-Beine, `rv` ist gesperrt | keiner bis Research |
| **W16** (Swing, ETF) | Sektor-Mix als Sektor-ETF-Tilt | Swing | Signal | offen | keiner | Live-Buch-Merker |
| **W17** | Kongress kauft in den Einbruch, Index long, konträr | Mean Reversion | Signal | offen, Feasibility fraglich | wie W11 | neues Bein (Warnung #139 B3) |
| **W18** | Tag mit vielen Offenlegungen, Index reagiert intraday | Intraday Bias | Zeitfenster | keine Story | keiner | keiner |
| **W19** | Energie- oder Gold-Käufe, CL/GC long | Relative Value | Signal | keine Story | keiner | keiner |
| **W20** (Swing) | Haltedauer Tage bis Monate | Swing | Exit | Achse, kein eigener Weg | keiner | keiner |
| **W21** (Swing) | Aggregat hoch, Index-Future (NQ/ES/RTY) long über Tage bis Wochen | Swing | Signal | offen (Research 12.10.: negativer Prior) | keiner in `tsmom`/`maband` (kein Mehrtages-Pfad), Prämisse-Messung außerhalb der Pipeline | Live-Buch-Merker, Prop verboten |
| **W22** (Swing) | Aggregat tief, Index-Future short über Tage bis Wochen | Swing | Signal | offen, keine Story | keiner | keiner |
| **W23** | Aggregat als Tor oder Richtung auf die Nacht-Session (18:00 ET bis Open) bzw. auf NQ_Asia-Dir-USopen | Filter | Filter | offen, keine eigene Story, heute kein Engine-Weg | `asian.py` liest `gates_pass` nicht, Modul-Spec S-POL-2 | Ersatz für NQ_Asia-Dir-USopen_d260820, nur E8 |
| **W24** | Aktivität hoch bei flachem Netto (viele Käufe und viele Verkäufe) als Vola- oder Regime-Tor | Filter | Filter | keine Story | Reihe fiele aus D-POL-1 ab, Tor wäre eine Zeile mehr in S-POL-1 | keiner |
| **W25** | Fade: Aggregat hoch, Index short (Politiker als Kontra-Indikator) | Mean Reversion | Signal | keine Story | `tsmom` short plus Tor, **nicht** der Inversions-Arm | keiner |
| **W26** | Fade: Aggregat tief, Index long | Mean Reversion | Signal | keine eigene Story, läuft als Inversions-Arm von W11/W13 mit | `GATE_INVERT_PAIR`-Arm von S-POL-1 | keiner |
| **W27** | Größe nach Aggregat-Rang skalieren statt an/aus | Filter | Sizing | Achse geschlossen (#139, 31.08.2026), keine Story | keiner | keiner |

---

## Die Wege im Einzelnen

### Block A: Einzelaktie und ETF (alles Live-Buch-Merker)

**W1 Aktie läuft nach Kauf-Offenlegung weiter, long (Skelett POL-W1a, Rang 4).** Max' Ursprungsidee. Story-Entwurf: Abgeordnete haben über Ausschüsse Wissen, das im Kurs noch nicht steckt, und dürfen bis zu 45 Tage später melden. Die Edge nach der Offenlegung gibt es nur, wenn die Information langsamer eingepreist wird als der Verzug dauert. Unbelegt. Messung wäre eine Ereignisstudie außerhalb der Pipeline, als Überrendite gegen den Index, sonst misst man Beta. Verwandte Tote: keine. **Verwandte in der Warteschlange (keine Toten):** `ideas.json` „Multi-Day-Kointegrations-Pairs“ (Backlog, Abbruchgrund „Prop-Regeln verbieten Overnight, erst im Live-Account testbar“) und „Cross-Sectional Momentum“ (Backlog). Diese Schlange „erst im eigenen Live-Konto“ gibt es also schon, W1 stellt sich hinten an.

- **Research-Stand W1 (12.10.2026): offen.** Nach 2012 gemischt. Dafür: Lazzaretto 2024, +90 bp im Folgemonat ab Offenlegung, nur Käufe (Beleg nur aus dem QuantConnect-Forum). Dagegen: House 2020 bis 2024 mit negativer CAR bei 20 und 40 Tagen (Göteborg-Thesis); Eggers/Hainmueller und Belmont et al. ohne Überrendite (NBER w26975). Der Untergruppen-Effekt (mächtige Republikaner, kleine Firmen) ist nur vor 2012 belegt (Karadas 2013). Aktien-Daten mit Delisting-Bereinigung: nicht recherchiert, offen. Why bleibt Entwurf. **Nicht an `ein-weg`:** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job.

**W2 Verkaufs-Offenlegung, short.** Keine Story, weil Verkäufe viele Gründe ohne Information haben (Steuern, Liquidität, Umschichtung) und ein Aktien-Short gegen die Marktdrift läuft. Research-Frage: unterscheidet die Literatur Käufe und Verkäufe?

**W3 Käufe gegen Verkäufe, marktneutral.** Kein eigener Weg, sondern die saubere Messform von W1 (Beta raus). Kein eigenes Skelett.

**W4 Sprung am Offenlegungstag und Rücklauf (Aktie, kein Swing).** Intraday- bis Folgetags-Fade. Nicht Prop, **weil es eine Aktie ist**, nicht wegen der Haltedauer: gäbe es das Instrument, wäre der Weg ohne Overnight handelbar. Story-Entwurf: Nachkauf-Apps und Kleinanleger kaufen am Meldetag ohne Blick auf den Preis, der Überschuss läuft zurück. Braucht Aktien-Intraday-Daten rund um den Meldezeitpunkt, die wir nicht haben. Kein Skelett, Research-Frage: gibt es einen messbaren Kurssprung am Offenlegungstag?

**W5 Cluster, W6 Untergruppe, W7 Verzug, W9 Betrag/Instrument.** Vier Filter auf W1, keine eigenen Wege im Sinn einer eigenen Preisbewegung. Sie stehen als Achsen im Skelett POL-W1a. **W6 hat fünf Untergruppen-Achsen:** Ausschuss mit Sektorbezug, Fraktionsführung, Top-Performer, **Partei (Mehrheits- gegen Minderheitspartei)**, **Kammer (House gegen Senate)**. Partei steckte bisher nur versteckt in POL-W10a (NANC minus KRUZ). Warnung: „Top-Performer“ ist eine Auswahl nach vergangener Rendite und nur rollierend, mit Daten bis zum Vortag, sauber. Partei und Kammer haben keine eigene Story außer „die Mehrheit setzt die Agenda“, das ist eine Research-Frage, keine Begründung.

**W8 Einstieg am Transaktionsdatum (Swing, Aktie).** Keine Story als handelbarer Weg, weil das Datum erst mit der Offenlegung bekannt wird. Taugt nur als Obergrenzen-Messung: wie viel der Edge frisst der Verzug.

**W10 Copycat-ETFs NANC und KRUZ (Skelett POL-W10a, Rang 5).** Rolle: **Messung, kein Signal.** Stand: offen, Vorab-Messung für W1. Die Fonds setzen Max' Idee regelbasiert um. Ist ihre Beta-bereinigte Überrendite null, ist W1 auf Offenlegungsdatum für uns erledigt, bevor ein Datensatz gebaut wird. Halten als Bein wäre Index-Beta mit Aufschlag.

- **Research-Stand W10 (12.10.2026): offen.** NANC und KRUZ laufen seit 07.02.2023, Gebühr rund 0,75 bis 0,83 %. NANC im ersten Halbjahr +7,72 % gegen S&P +5,47 %; ein Jahr bis Mitte 2024 NANC +33 %, KRUZ +22,5 %, SPY +27 % (etf.com, N-CSR). **Keine faktorbereinigte Rechnung gefunden**, NANC hält 39 % Tech, Seeking Alpha nennt die Outperformance zufällig. Die rohen Zahlen entscheiden die Vorab-Frage für W1 also nicht. Selbst rechnen (Tagesdaten NANC/KRUZ gegen QQQ/SPY) ist günstig. **Nicht an `ein-weg`:** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job.

**W16 Sektor-ETF-Tilt (Swing, ETF), W20 Haltedauer (Swing).** W16 ist die Swing-Fassung von W15, Live-Buch-Merker ohne Skelett. W20 ist eine Exit-Achse von W1 und W21, kein eigener Weg.

### Block B: Index-Futures intraday (prop-fähig)

**W13 Aggregat als Tages-Tor auf ein bestehendes Bein (Skelett POL-W13a, Rang 1).** Netto-Kauf der letzten 30 Tage nach Offenlegungsdatum, Vortagsstand, Rang über 250 Tage. Long-Trades von NQ_Momentum_PB3_fa01b nur bei hohem Rang. Story-Entwurf: breites Netto-Kaufen des Kongresses als langsamer Zustand „Rückenwind für Aktien“. Schwachstellen offen benannt: bis 45 Tage Verzug, ein Intraday-Bein sieht von einem Wochen-Zustand nur einen Bruchteil, und es gibt bei uns keine Quelle dafür. Rang 1 nur, weil es der einzige prop-fähige Ersatz-Weg ist, nicht weil die Story stark wäre.

- **Research-Stand W13 (12.10.2026): Research widerlegt, kein Tot-Stempel.** Karadas/Schlosky/Hall, JRFM 2021 (https://www.mdpi.com/1911-8074/14/6/256): das Aggregat hat Vorhersagekraft **vor 2012** (Daten 2004 bis 2014), der STOCK Act hat sie abgeschwächt. Der Horizont ist Monate (Karadas 2022), kein Tages-Tor. Belegtiefe: Abstract-Ebene. Cache und Logbuch hatten vorher nichts. Reichweite des Befunds: Literatur, keine eigene Messung, 0 Trials. **Nicht an `ein-weg` in dieser Runde.** Das Why bleibt als Entwurf stehen, der Weg bleibt in der Karte.

- **Stand „offen“ trägt:** 0 Fundstellen für `cong`, `politi`, `insider` im Register.
- **Tote bzw. geschlossene Verwandte:**
  - **#139 (31.08.2026, AR-17 Vola-Konditional als Tages-Gate)**, engster Präzedenzfall für ein Tages-Tor aufs Buch: 24 Varianten, 180 Trials, Hauptvariante +7,46 pp mit Placebo p 0,025 bestanden und **trotzdem geschlossen**, weil ohne COVID p 0,30 blieb und die Zahl unabhängiger Episoden (16 bis 20 in 10 Jahren) bindet. Gleich: Tageszustand schaltet das Buch an und aus. Anders: dort Vola mit sauberem Varianz-Mechanismus, hier ein Richtungs-Argument ohne Beleg, also schwächer.
  - **#132 (25.08.2026, GEX-Buch-Gate tot):** +2,67 pp am 16.08. wurden gegen das neue Buch +1,21 pp, neutral, „buchabhängiges Rauschen“. Direkte Warnung für jedes Ersatz-Urteil hier: ein Tor-Gewinn muss einen Buchwechsel überleben.
- **Verwandte, nicht tot:**
  - **#163 ist eine Feasibility-Warnung, kein Toter:** der Befund ist „unentscheidbar“ (MDE 0,26 bis 0,88 ATR20 gegen Kill-Schwelle 0,15 ATR20), zählt nach Regel 22.09. nicht als Friedhof.
  - **#087 VIX-Teil ist Verwandter (Bank, Klein-N), nicht tot:** 8 von 24 Survivors, „abgelehnt, Bank“, `ideas.json` Status Validiert. Tot ist in #087 nur die MOC-These (0 von 72).
  - **#110 DIX:** der nächste Verwandte von „informierte Käufer als Tagesrichtung“. NQ beta +0,003 (t +0,14), ES mit falschem Vorzeichen, keine Literatur als Return-Prädiktor. Nur Regression, nie als Job gerechnet (`tm_dix_` 0 im Register).
  - **`ideas.json` „Mom-lowVIX“** (Status Validiert, nicht im Buch, „VIX-Filter selbst nie gegen das Buch auto-gefittet“) und **#111** (LastHour-Filter): VIX „als Kontext richtig, als Filter nein“, nested Walk-Forward der ganzen Filter-Suche +0,9 $ je Trade mit P(Δ≤0) 0,39, Lehre 101 (der Beste aus rund 100 Filter-Varianten liegt unter reiner Null bei t ≈ 2,4). Ehrlicher Zusatz: der vorab formulierbare Makro-Tage-Filter aus #111 ist als NQ_LastHour_v3 im Buch. Ein Tages-Tor ist also nicht per se chancenlos, aber es war das billigste und einzige mit Kalender-Logik.
- **Achsen für `variant-scout`:** Ziel-Bein (NQ_OpenDrive_maband2050 als zweites, `maband` liest `gates_pass`), **Markt (ES, RTY, YM statt nur NQ)**. Zur Markt-Achse: #132 nennt MES-Kosten je Einheit Bewegung beim 3,6-fachen von MNQ, und das RTY-Bein im Next-Week-Buch läuft im Gap-Modus, der `gates_pass` nicht liest. Markt-Achse heißt also heute: neues `tsmom`- oder `maband`-Bein auf ES/RTY/YM, kein Tor auf ein vorhandenes.

**W11 Aggregat hoch, Index long (Skelett POL-W11a, Rang 2).** Dasselbe Tor auf einem dünnen `tsmom`-Long-Signal als eigenes Bein. Muss gegen den ungefilterten Long-Arm bestehen, nicht gegen null. Neues Bein ist der schwächere Weg (#139 vom 01.09., B3: 577 Buch-Evals ohne `replaces_leg`, Median −12,3 pp, 0 Treffer). Verwandte, nicht tot: #087 VIX-Teil (Bank, Klein-N, gleiches Bauprinzip „Tagessignal, Long Open bis EOD“, 170 Trades), #110 DIX (siehe W13). Markt-Achse ES, RTY, YM wie bei W13.

- **Research-Stand W11 (12.10.2026): Research widerlegt als Intraday-Lesart, kein Tot-Stempel.** Gleiche Quellen wie W13: der Aggregat-Effekt wirkt auf 2 bis 3 Monate (Karadas, Dissertation und JFEP 2022), es gibt keinen Beleg für eine Tagesdrift Open bis Close, dazu die Abschwächung nach dem STOCK Act. Widerlegt ist die Intraday-Lesart über den Horizont-Mismatch, als Schlussfolgerung aus der Literatur, **nicht durch eigene Messung**. **Nicht an `ein-weg` in dieser Runde.**

**W12 Aggregat tief, Index short.** Keine Story, weil Verkäufe wenig Information tragen und ein Index-Short gegen die Drift läuft. Kein eigenes Skelett.

**W14 Aggregat dreht.** Reparametrisierung von W13 (Änderung statt Niveau), als `_chg`-Reihe in der Modul-Spec vorgesehen, kein eigener Weg. Trifft die Episoden-Falle aus #139 (31.08.) härter als W13: Drehpunkte eines 30-Tage-Aggregats sind noch seltener als Hoch-Phasen. #163 gilt als Feasibility-Warnung.

**W15 Sektor-Mix Richtung Tech, NQ gegen ES/RTY.** Story schwach: der Sektor-Mix der Käufe folgt vermutlich einfach den Index-Gewichten und schwankt kaum. Kein Skelett vor Research. Der `rv`-Modus hat keinen Null-Schalter, es bliebe nur ein Tor auf NQ-Beine.

**W17 Kongress kauft in den Einbruch.** Story-Entwurf vorhanden (Käufe gegen die Angst als informiertes Signal), aber die Zahl solcher Episoden seit 2016 ist vermutlich einstellig. Kein Skelett, bevor `overfit.bucket_mde()` zeigt, dass es entscheidbar ist. Buch-Bezug neues Bein, **gleiche Warnung wie W11: #139 B3**. Verwandte, nicht tot: #087 VIX-Teil (Bank, Klein-N), #163 als Feasibility-Warnung.

**W18 Offenlegungs-Flut-Tag.** Keine Story, weil Einzeltitel-Meldungen im Millionen-Bereich keinen Index-Future bewegen.

**W19 Energie- oder Gold-Käufe auf CL/GC.** Keine Story, weil ein Aktienkauf in einer Öl- oder Minenfirma keine Sicht auf den Rohstoffpreis ist, und die Fallzahl winzig wäre.

### Block C: Nachtrag 12.10.2026 (W21 bis W27)

**W21 Aggregat hoch, Index-Future long über Tage bis Wochen (Swing, Skelett POL-W21a, Rang 3).** Der Horizont, der zum Signal passt: ein 30-Tage-Aggregat mit bis zu 45 Tagen Verzug lebt in Wochen, nicht in Stunden. Mit unserem Futures-Bestand rechenbar, sobald D-POL-1 steht, als Prämisse-Messung außerhalb der Pipeline (Muster `gex_validate.py` aus #110: Regression, Vortagsstand, Newey-West, 0 Register-Trials). Story-Entwurf identisch mit W13, nur ohne den Horizont-Bruch. Kein Engine-Weg: `tsmom` und `maband` kennen nur Minuten-Haltedauer (`tm_hold_min`) bis zum Tagesende, ein Mehrtages-Modus hätte keinen Null-Schalter. Buch-Bezug: **Live-Buch-Merker, Prop verboten** (Randbedingung 3). Fallen: Dauer-Long auf NQ verdient schon an der Drift, gemessen wird also die Mehrrendite gegen Dauer-Long und gegen W26; bei 30 Tagen Haltedauer bleiben rund 85 nicht überlappende Blöcke, #139 (31.08.) und #163 gelten voll. Verwandte: `ideas.json` Pairs und Cross-Sectional Momentum (Backlog, gleiche Sperre), #110 DIX.

- **Research-Stand W21 (12.10.2026): offen, negativer Prior.** Der Horizont passt zur Literatur (Karadas 2022, 2 bis 3 Monate), aber die Daten sind nur von vor 2012. Karadas 2021 zeigt die Abschwächung nach dem STOCK Act, eine Aggregat-Studie nach 2012 ab Offenlegungsdatum wurde nicht gefunden. Zur Autokorrelation und zur Zahl unabhängiger Phasen wurde nichts gefunden, das geht nur per eigener Rechnung. Kein Todesurteil. **Nicht an `ein-weg`:** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job.

**W22 Aggregat tief, Index-Future short über Wochen (Swing).** Keine Story, aus demselben Grund wie W2 und W12: Verkäufe tragen wenig Information, ein Wochen-Short auf den Index läuft gegen die Drift. Fällt in der W21-Messung als unteres Terzil gratis ab, kein Skelett.

**W23 Aggregat auf die Nacht-Session bzw. auf NQ_Asia-Dir-USopen.** E8 erlaubt das Halten innerhalb des Handelstags 18:00 bis 16:10 ET ([[Firm-Regeln je Konto]]), wir haben ein Nachtbein im Buch, der Weg ist also bei E8 nicht verboten (FN: Overnight verboten). **Kein Engine-Weg heute:** `asian.py` hat 0 Fundstellen für `gates_pass`. Der Modus steht in `discovery_lib.NULL_MODES` (Z. 1016), eine Erweiterung wäre also deploy-fähig: Modul-Spec S-POL-2. **Keine eigene Story:** die Nacht-Session wird von Asien- und Europa-Flow getrieben, ein US-Kongress-Aggregat mit Wochen-Verzug hat dorthin keinen eigenen Kanal, es wäre W13 auf einem anderen Bein. Deshalb kein Skelett, sondern Ziel-Bein-Achse von POL-W13a, sobald S-POL-2 steht. Look-ahead-Hinweis: die Nacht ab 18:00 ET gehört schon zum nächsten Handelstag, die Reihe muss gegen den Stand **vor** 18:00 ET verschoben sein. **Toter Verwandter:** `ideas.json` „Overnight-Drift 2-3h ET (Boyarchenko)“, Status Getötet, alle drei Fenster-Varianten negativ. Gleich: Long-Drift in der Nacht als Träger. Anders: dort unbedingt, hier bedingt auf das Aggregat, aber ohne Grund, warum die Bedingung eine tote Drift wiederbelebt.

**W24 Aktivität hoch bei flachem Netto als Vola- oder Regime-Tor.** Zustände eng, weit, flach des Aggregats. Die Reihe `n_buy + n_sell` fällt aus D-POL-1 gratis ab. **Keine Story,** weil (1) die Meldezahl vermutlich am Meldekalender und an wenigen Vielhändlern hängt und nicht an einer Marktsicht (Research-Frage 8, unbelegt), (2) für Vola mit VIX und GEX direkte, tagesaktuelle Maße im Bestand sind (#110: GEX sagt Vola auch nach VIX-Kontrolle voraus) und ein bis 45 Tage altes Zählmaß dagegen keinen Grund hat zu gewinnen, (3) #139 (31.08.) gezeigt hat, dass selbst ein sauber begründetes Vola-Tor mit unserem Sample nicht auflösbar ist. Kein Skelett.

**W25 Fade: Aggregat hoch, Index short.** Keine Story: für „Politiker als Kontra-Indikator“ gibt es keinen Mechanismus, und der Short läuft gegen die Drift. **Korrektur zum Auditor:** dieser Weg ist **nicht** der `GATE_INVERT_PAIR`-Arm. `controls.ctl_gate_invert` dreht das Tor (Min-Schwelle wird Max-Schwelle, Trades unterhalb statt oberhalb), nicht die Seite. Der Inversions-Arm von S-POL-1 misst also W26, nicht W25. W25 bräuchte einen eigenen Short-Arm (`tm_dir=short` plus Tor) und bekommt ohne Story keinen.

**W26 Fade: Aggregat tief, Index long.** Keine eigene Story (denkbar wäre „Kongress verkauft am Tief“, unbelegt). **Läuft als Inversions-Arm von W11 und W13 mit:** dasselbe Bein, Tor gedreht. Gewinnt dieser Arm, ist das die Widerlegung von W13, kein neuer Fund. Abgrenzung zu W17: W17 ist auf den Preis bedingt (Kauf in den Einbruch), W26 nur auf das Aggregat.

**W27 Rolle Sizing: Größe nach Aggregat-Rang.** Achse geschlossen laut **#139 (31.08.2026)**: vola-skaliertes Sizing war die saubere Antwort auf den dortigen Befund, „unter Min-Size 1 Kontrakt nicht ausführbar, Achse GESCHLOSSEN, wieder auf erst bei mehreren Kontrakten je Bein oder feinerer Kontraktgröße“. Stand der Bedingung: laut CLAUDE.md seit 21.09. formal eingetreten (Größe wird gerechnet), der Betriebspunkt vom 05.10. ist aber k1 auf allen Konten, also 1 Micro je Bein, darunter gibt es nur an oder aus. Dazu fehlt die Story: #139 begründete Sizing über die Varianz (Drift behalten, Varianz kappen), das Aggregat hat kein Varianz-Argument. Kein Skelett. Wiedervorlage: sobald ein Konto nach der Vola-Regel auf k2 geht **und** W13 eine Prämisse hat.

---

## Reihenfolge nach Buch-Chance

| Rang | Skelett | Weg | Why-Status | Was vorher passieren muss |
|---|---|---|---|---|
| 1 | POL-W13a | Tor auf NQ_Momentum_PB3_fa01b | widerlegt (Research 12.10.) | nicht an `ein-weg` in dieser Runde; sonst D-POL-1, S-POL-1, Feasibility |
| 2 | POL-W11a | eigenes Long-Bein mit Tor | widerlegt als Intraday-Lesart (Research 12.10.) | nicht an `ein-weg` in dieser Runde; sonst wie Rang 1 |
| 3 | POL-W21a (Swing) | Index-Future long über Wochen | offen (negativer Prior) | D-POL-1, Feasibility, kein Prop-Job |
| 4 | POL-W1a (Swing, Aktie) | Aktie nachkaufen | offen (Research gemischt) | Aktien- und Kongress-Daten, kein Prop-Job |
| 5 | POL-W10a (Swing, ETF) | NANC/KRUZ als Live-Beleg | offen | Research reichte nicht (nichts Faktorbereinigtes), eigene Messung mit ETF-Tagesdaten |

POL-W21a steht vor POL-W1a, weil es mit dem vorhandenen Futures-Bestand rechenbar ist und nur D-POL-1 braucht. POL-W1a und POL-W10a haben ihre Ränge 3 und 4 dadurch auf 4 und 5 getauscht, die IDs bleiben.

**Billigster erster Schritt (unverändert):** Research zu W1 und W10. Zeigt die Literatur nach 2012 und zeigen die ETFs nichts, fällt die Begründung für D-POL-1 und S-POL-1 weg, bevor Code entsteht.

**Stand nach Research (12.10.2026):** die Bedingung ist nicht sauber eingetreten. Die Literatur nach 2012 ist für W1 gemischt, die ETFs zeigen roh eine Mehrrendite bei NANC, aber ohne Faktorbereinigung. Für S-POL-1 (Tor im Code) gibt es nach dem Research keine Begründung mehr, solange W13 und W11 auf „Research widerlegt“ stehen. Billigster nächster Schritt laut Research: NANC und KRUZ gegen QQQ und SPY selbst rechnen (W10, Tagesdaten, 0 Register-Trials). Das ist eine Messung außerhalb der Pipeline und nicht Teil dieser Runde.

**Buch-Lücke je Skelett:** alle fünf hängen **vor** der ersten Stufe (Prämisse). Es fehlen Why-Beleg, Daten und bei Rang 1 und 2 das Tor im Code. Rang 3 bis 5 erreichen das Prop-Buch strukturell nie. Nach dem Research (12.10.) gilt zusätzlich: Rang 1 und 2 haben keinen Why-Beleg bekommen, sondern einen Gegenbeleg aus der Literatur. Damit hat das Konzept in dieser Runde **keinen Weg, der ins Prop-Buch führen kann**.

---

## Research-Stand (12.10.2026, Rückschreibung nach `research-scout`)

„Research widerlegt“ heißt: die Literatur spricht dagegen. Es ist **kein Tot-Stempel**, gerechnet wurde nichts (0 Trials, keine Daten). Tot wird ein Weg nur nach vollem Test.

| Skelett | Weg | why_status | Befund und Quelle | An `ein-weg`? |
|---|---|---|---|---|
| POL-W13a | W13 | **widerlegt** | Karadas/Schlosky/Hall, JRFM 2021 (https://www.mdpi.com/1911-8074/14/6/256): Aggregat-Vorhersagekraft vor 2012 (Daten 2004 bis 2014), vom STOCK Act abgeschwächt; Horizont Monate (Karadas 2022), kein Intraday-Tor. Abstract-Ebene. Cache und Logbuch hatten vorher nichts. | **Nein.** Research widerlegt, nicht in diese Runde. |
| POL-W11a | W11 | **widerlegt** (als Intraday-Lesart) | Gleiche Quellen: Effekt auf 2 bis 3 Monate (Karadas, Dissertation und JFEP 2022), kein Beleg für Tagesdrift Open bis Close, Abschwächung nach STOCK Act. Horizont-Mismatch, Schlussfolgerung aus der Literatur, keine eigene Messung. | **Nein.** Research widerlegt, nicht in diese Runde. |
| POL-W21a | W21 (Swing) | **offen** | Horizont passt zur Literatur (Karadas 2022), aber nur Daten vor 2012; Karadas 2021 zeigt Abschwächung nach STOCK Act; keine Aggregat-Studie nach 2012 ab Offenlegungsdatum gefunden. Negativer Prior, kein Todesurteil. Autokorrelation und Zahl unabhängiger Phasen: nichts gefunden, nur eigene Rechnung möglich. | **Nein.** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job. |
| POL-W1a | W1 (Swing, Aktie) | **offen** | Nach 2012 gemischt: Lazzaretto 2024 (+90 bp Folgemonat ab Offenlegung, Käufe; nur QuantConnect-Forum), House 2020 bis 2024 CAR negativ bei 20 und 40 Tagen (Göteborg-Thesis), Eggers/Hainmueller und Belmont et al. ohne Überrendite (NBER w26975). Untergruppen-Effekt (mächtige Republikaner, kleine Firmen) nur vor 2012 (Karadas 2013). Aktien-Daten mit Delisting-Bereinigung: nicht recherchiert. | **Nein.** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job. |
| POL-W10a | W10 (Swing, ETF) | **offen** | NANC/KRUZ seit 07.02.2023, Gebühr rund 0,75 bis 0,83 %; NANC Halbjahr +7,72 % gegen S&P +5,47 %; ein Jahr bis Mitte 2024 NANC +33 %, KRUZ +22,5 %, SPY +27 % (etf.com, N-CSR). Keine faktorbereinigte Rechnung gefunden, NANC 39 % Tech, Seeking Alpha: Outperformance zufällig. Selbst rechnen ist günstig. | **Nein.** Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job. |

**Ergebnis der Runde:** 0 von 5 Skeletten gehen an `ein-weg`. Kein Why wurde belegt, deshalb ist kein Why-Text überarbeitet, alle fünf bleiben als Entwurf stehen. Wiedervorlage für W13 und W11: eine Arbeit, die das Aggregat **nach 2012 ab Offenlegungsdatum** misst, oder eine eigene W21-Messung, die auf dem Wochen-Horizont trägt.

---

## Modul-Specs

- **D-POL-1 (Daten, außerhalb der Engine):** Loader schreibt `exported_data/CONGRESS_NET_daily.csv` mit `date` (Offenlegungsdatum), `n_buy`, `n_sell`, `usd_buy_mid`, `usd_sell_mid`. Quelle offen (Research-Frage). Für die Achsen aus W6 zusätzlich je Zeile Partei und Kammer mitführen, sonst sind sie später nicht rechenbar.
- **S-POL-1 (Engine, rund 25 Zeilen):** `sigcore._spx_daily_context()` lädt die Reihe, bildet 30-Tage-Summe, `shift(1)`, Rang 250 Tage und 5-Tage-Änderung. Zwei Zeilen in der lo/hi-Schleife von `sigcore.gates_pass()` (`tm_cong_net_min/max`, `tm_cong_rank_min/max`), Default `None`. Registrierung in `discovery/controls.py` (`GATE_OFF` Z. 136, `GATE_INVERT_PAIR` Z. 178). Danach `engine-regression-tester`, alle Buch-Beine bitgleich.
- **S-POL-2 (Engine, nur für W23, grob 10 bis 15 Zeilen, ungelesen geschätzt):** `asian.py` ruft `sigcore.gates_pass()` je Handelstag vor dem Entry. Nicht nur für dieses Konzept nützlich: heute kann kein Tages-Tor (VIX, GEX, Zins) auf das Nachtbein. Erst bauen, wenn W13 eine Prämisse hat.

---

## Offene Research-Fragen (für `research-scout`)

1. Gibt es nach dem STOCK Act 2012 noch Überrendite, gemessen ab **Offenlegungsdatum**? Kandidaten zum Prüfen, nicht belegt: Ziobrowski et al. (vor 2012), Eggers/Hainmueller, Belmont et al., neuere Arbeiten zur Fraktionsführung.
2. Trägt der Effekt nur in Untergruppen und nur bei Käufen? Gibt es Befunde nach **Partei** und **Kammer**?
3. Misst irgendeine Arbeit den **aggregierten** Netto-Kauf als Prädiktor für Index-Renditen, und auf welchem Horizont (Tag, Woche, Monat)?
4. Welche freie Quelle liefert Transaktions- und Offenlegungsdatum je Meldung mit Historie ab 2016 (House Clerk, Senate eFD, House/Senate Stock Watcher, Capitol Trades, Quiver)? Lizenz, Pflegezustand?
5. Verzug im Median und im Schwanz, Anteil verspäteter Meldungen?
6. NANC und KRUZ: Auflage, Regelwerk, Kosten, Rendite gegen SPY/QQQ, Anteil reiner Tech-Gewichtung?
7. Gibt es einen messbaren Kurssprung am Offenlegungstag (W4)?
8. Woran hängt die **Zahl** der Meldungen je Monat (Meldefristen, wenige Vielhändler, Jahresende)? Entscheidet, ob W24 je eine Story bekommt.

**Stand der Fragen nach Research (12.10.2026):** Frage 1 beantwortet mit „gemischt“ (siehe W1). Frage 2 teilweise: Untergruppen-Effekt nur vor 2012 belegt (Karadas 2013), zu Kammer nur der negative House-Befund 2020 bis 2024. Frage 3 beantwortet: ja, Karadas/Schlosky/Hall 2021 und Karadas 2022, Horizont 2 bis 3 Monate, Daten 2004 bis 2014, nichts nach 2012. Frage 6 beantwortet bis auf die Faktorbereinigung. Fragen 4, 5, 7 und 8 sowie die Aktien-Datenquelle stehen in den zurückgemeldeten Research-Zeilen nicht und bleiben hier offen.

**Nachrecherche 12.10.2026 (zweiter `research-scout`-Lauf, gezielt auf die Lücken).** Alles Abstract-Ebene oder Presse, kein Volltext. Die NBER-Seiten nennen nicht, ob ab Transaktions- oder ab Offenlegungsdatum gemessen wird.

- **Frage 4 (Datenquellen):** keine Quelle ist als sauber bestätigt belegt. House Clerk liefert jährliche XML-Indexe und die Meldungen als PDF, fertige Parser decken die Historie vor 2020 nicht ab (`congressional-trading` auf PyPI, nur House, Alpha). Quiver (Kopie bei QuantConnect ab 01/2016, API laut Dritten ab rund 30 $ im Monat) und Benzinga (ab 2003) sind kommerziell, das Offenlegungsfeld ist bei beiden nicht belegt. Senate eFD ungeprüft (Abruf 403). House/Senate Stock Watcher offline, kein Kaggle- oder GitHub-Dump gefunden.
- **Frage 5 (Verzug):** keine akademische Zahl. Mittel 32 Tage (Tracking-Seite, 3.400 Meldungen), Median 27 Tage (lambdafin), 20 bis 41 % verspätet je nach Quelle.
- **Frage 7 (Sprung am Meldetag):** Abdurakhmonov et al., SMJ 2023 (Senat 2012 bis 2020): am Offenlegungstag nur rund 0,09 bis 0,11 % abnormale Rendite, mit Ausschuss-Zuständigkeit etwa 0,5 % (Pressetext). Danach 6 bis 12 Monate negativ, gezählt ab Transaktionsdatum. Ob der Sprung zurückläuft, ist nicht belegt. W4 bleibt offen, Story schwächer.
- **Frage 8 (Zahl der Meldungen):** nichts gefunden, nur eigene Rechnung auf D-POL-1 möglich.
- **Neue Arbeiten:** Chen/Sacerdote (NBER w35041, 2012 bis 2023): Portfolios nach dem STOCK Act gleich oder unter Markt, die Trades folgen Analysten und Retail-Stimmung statt dem Kurs voraus. Belmont et al. (J. Public Economics 2022): Senatskäufe 11 bis 28 bp unter der Vergleichsgruppe. Göteborg-Thesis (House 2020 bis 2024, **ab Offenlegungsdatum, mit Kosten**): rund −40 bp pro Monat, nicht begutachtet. Wei/Zhou „Captain Gains“ (NBER w34524): Fraktionsführer +47 Prozentpunkte pro Jahr gegen Kollegen, aber nur 20 Personen, Stichprobe 1995 bis 2021 und nicht ab Offenlegung. Das ist die einzige Quelle für eine Untergruppe (W6), als handelbar nicht belegt.
- **NANC/KRUZ:** 2025 NANC +20,8 %, GOP +18,8 %, S&P +16,6 % (Anbieterzahlen). Beta zu SPY 1,12, Korrelation 96,6 %. Weiter kein QQQ-Vergleich und nichts Faktorbereinigtes.
- **Aggregat nach 2012 gegen Index:** Negativbefund, keine Arbeit und kein Praktiker-Test gefunden (nur Websuche).
- **Folge:** kein Stand in der Wege-Tabelle geändert. W1 kippt klarer ins Negative (Chen/Sacerdote, Belmont, Göteborg gegen Lazzaretto und SMJ). W13 und W11 bleiben „Research widerlegt“. Einziger Weg mit einem positiven Beleg ist die Achse Fraktionsführung in W6, und die ist ein Aktien-Swing.

---

## Verwandte Notizen

- [[Testphase Juli-Modus]] (Idee 5)
- [[VWAP-Offensive]] (Vorbild für den Aufbau)
- [[Strategie-Logbuch]] #034, #087, #110, #111, #132, #139 (31.08. und 01.09.), #163
- [[Firm-Regeln je Konto]] (Halten über den Tagesschluss, Nacht-Session E8, FFN flat 16:50 ET)
- [[Research-Cache]]
- [[Familien-Scout Agent]]
- [[Gap Wege-Karte]] (Schwesterkarte, gleiche Swing-Regel bei W34)
