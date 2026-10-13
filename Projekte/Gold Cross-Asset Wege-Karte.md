---
tags: [projekt, trading, alpha-suche, gold, cross-asset]
erstellt: 2026-10-13
aktualisiert: 2026-10-13
status: aktiv
ziel: Zeit bis 50.000 $ Eigenkapital aus Payouts verkürzen (Gate v4), oder das Kapitel Fremdmarkt-Signale für Gold mit Reichweite schließen
---

# Gold Cross-Asset Wege-Karte

**Ziel (einziges Kriterium, seit 18.09.2026):** verkürzt der Weg die **Zeit bis 50.000 $ Eigenkapital aus Payouts** bei begrenzter Auslage? Übersetzt in Gate v4 Stufe 1: allein profitabel nach Kosten, Walk-Forward mit Neuauswahl bestanden, **Buch-Sharpe steigt**, Passquote höchstens −3 pp. Jede Zeile muss am Ende beantworten: Ersatz für welches Bein, neues Bein, oder Live-Buch-Merker.

Angelegt am 13.10.2026 vom `familien-scout`. Quelle des Konzepts: Auftrag Max 13.10.2026 (diktiert): Cross-Asset-Analyse für Gold, welche Signalgeber wir haben, welche fehlen, was schon getestet ist und wie groß die Chance ist, etwas zu finden. Eine Hand-Karte zum selben Konzept gibt es nicht. Nachbarn: [[Hypothesen-Bank (Gold & Sessions)]] (Gold mit eigenen Session-Ankern, 12.10.2026) und [[Neue Märkte (NT8-Daten) Plan]]. Aufbau nach dem Vorbild [[VWAP-Offensive]].

**Nachtrag 13.10.2026 (nach `verdict-auditor`):** zehn neue Wege (W36 bis W45), acht korrigierte Stände, sieben Gruppen übersehener Verwandter. Die Wege W1 bis W35 behalten ihre Nummern. Was sich geändert hat, steht gesammelt im Abschnitt „Nachtrag“ am Ende.

**Research-Rückschreibung 13.10.2026 (nach `research-scout`):** alle neun Skelette stehen beim Why auf **offen**: kein Beleg, keine Widerlegung. Kein Weg wurde gestrichen oder umnummeriert, Ränge und Chancen bleiben. Stand je Skelett im Abschnitt „Research-Stand 13.10.2026“ hinter der Reihenfolge.

**Abgrenzung:** Diese Karte behandelt nur die Richtung Fremdmarkt → Gold. Die Gegenrichtung (Gold als Signalgeber für ES oder Silber) gehört nicht zum Konzept. Sie liegt in der [[Hypothesen-Bank (Volumen & Flows)]], Zeile XA-32 (Gold-Anstieg bei fallendem ES, Folgetag ES, ungetestet).

> [!warning] Die Lage in einem Satz
> Gold ist das Handelsziel, der Fremdmarkt liefert die Information. Bei uns ist das **fast unberührt**: im Register stehen 2.777 GC-Trials, aber **0 davon mit einer Fremdmarkt-Achse**, in der Bank steht eine einzige Zeile (GC-RV-01, „nicht bauen“), im Logbuch kein Eintrag. Gemessen ist nur eines: über eine 5-Minuten-Bar Versatz führt weder Zins noch Dollar noch Nasdaq den Goldpreis (rund 0), die Märkte bewegen sich gleichzeitig. Kürzere Vorläufe (1 bis 4 Minuten) sind nie gemessen. Die besten vorhandenen Signalgeber sind ZN und 6E, beide sind geladen. Die Chance auf ein Bein ist klein, weil es auf Gold kein Basis-Signal mit handelbarer Edge gibt und die Zins-Kopplung seit 2024 halbiert ist.

---

## Signalgeber im Überblick (Max' Frage)

Chance = grobe Schätzung des Scouts, dass der Signalgeber bis ins Next-Week-Buch trägt. **Nicht gerechnet.** Maßstab: seit dem 21.08.2026 rund 65.000 Trials ohne neuen Mechanismus im Live-Buch; auf Gold 2.777 Trials und vier Prämissen-Tafeln, nichts trägt; der Alpha-Scout schätzte am 10.10.2026 für Grid-Nachbarn höchstens 10 % je Job; unter Gate v4 kommt reines Rauschen in bis zu 4,2 % der Such-Läufe durch. Eine Chance unter 5 % heißt also: ein Treffer wäre vom Rauschen kaum zu unterscheiden. Der Nachtrag ändert die Schätzungen nicht (Begründung im Abschnitt „Nachtrag“).

Gold selbst (GC, 1 Minute) reicht von 12/2015 bis **24.07.2026**.

| Signalgeber | Kanal | Daten | Schon gemessen oder getestet | Wege | Chance (Schätzung) |
|---|---|---|---|---|---|
| **ZN** (10Y-Future) | Zins | 1 Minute, 12/2015 bis 18.09.2026. Bei E8 handelbar, bei FN nicht in der Liste | Gleichzeitig 0,35 (0,46 → 0,38 → 0,24 ab 2024). Versatz eine 5-Minuten-Bar +0,007. Lags 1 bis 4 Minuten nie gemessen. 0 Trials. Bedingt, an Datentagen, als Bestätigung, am eigenen Level: nie gemessen | W1, W5, W6, W12, W15, W21, W27, W36, W38 bis W42 | 5 bis 10 %, bester vorhandener |
| **ZB** (30Y-Future) | Zins | 1 Minute, bis 18.09.2026 | nichts | Zwilling von ZN, nur Achse | kein Zusatz zu ZN |
| **DGS10, DGS2** (FRED) | Zins, Tagesstand | Tag, enden 14.08.2026 | Tor existiert (`tm_dgs10_*`, `tm_dgs2_*`), ein Kurven-Tor (10Y minus 2Y) nicht. Auf GC 0 Trials, eine nachträgliche Zählung (GCZINS-01: t −2,2, 15 Trades im Jahr). Auf NQ 9 Trials (`mak01_macrogate_pb3_NQ`, 6 Survivors, kein Kandidat, offener Fall) | W7, W19, W43 | 3 bis 5 % |
| **6E** (Euro-Future) | Dollar | 1 Minute, bis 14.09.2026 | Gleichzeitig 0,40 (0,46 → 0,40 → 0,36), stabilste Kopplung. Versatz eine 5-Minuten-Bar +0,002. 0 Trials | W2, W5, W12, W15, W27, W36, W38 bis W41 | 5 bis 10 %, zusammen mit ZN |
| **6B** (Pfund-Future) | Dollar | 1 Minute, bis 14.09.2026 | nichts | Zwilling von 6E | kein Zusatz |
| **DTWEXBGS** (breiter Dollar, FRED) | Dollar, Tagesstand | Tag, endet 14.08.2026 | Tor existiert (`tm_dxy_*`). Auf GC 0 Trials | W7, W19, W45 | 3 bis 5 % |
| **6J** (Yen) | Dollar, sicherer Hafen | **fehlt** (NT8 nachladbar) | nichts | Achse von W2, W15 | unter 3 %, dritter Dollar-Blick |
| **DXY intraday** | Dollar | **fehlt** (ICE-Kontrakt, im CME-Feed vermutlich nicht enthalten, ungeprüft) | nichts | durch 6E abgedeckt | kein Zusatz |
| **Realzins, TIPS** (DFII10), **Inflationserwartung** (T10YIE) | Zins, Tagesstand | **fehlt** (FRED, gratis) | Research-Cache: Kopplung Gold zu Realzins seit 2022 nur noch 3 bis 7 % | W7, W21, W31, W44 | unter 3 % als Signal, nützlich als Zustands-Beschreibung |
| **SI** (Silber) | Metall | **fehlt** (NT8 nachladbar, bei E8 und FN handelbar; AP221 wartet darauf, AP143 ist die Databento-Kostenabfrage) | nichts gerechnet. Im Cache: Wei 2026 (Gold und Silber über Sessions, nur Abstract) | W8, W18, W24, W25, W32 | 3 bis 6 %, einziger enger Ersatz-Markt |
| **HG** (Kupfer), **PL** (Platin) | Metall, Konjunktur | **fehlt** | nichts | W26, W35 | unter 3 %, keine Gold-Story |
| **CL** (Öl) | Inflation | 1 Minute, bis 21.07.2026 | Gegen GC nie gemessen | W9, W26, W29, W44 | unter 3 % |
| **NQ, ES** | Risiko | 1 Minute | Gleichzeitig 0,11, Vorzeichen kippte (−0,18 → +0,20 ab 2020), Versatz eine 5-Minuten-Bar −0,006, Tageskorrelation 0,09. 0 Trials | W3, W17, W21, W22, W23, W41, W42 | 3 bis 6 %, nur im Stress |
| **YM, RTY, FDAX** | Risiko | 1 Minute | nichts | Achse von W3 | kein Zusatz |
| **VIX** (FRED) | Risiko, Tagesstand | Tag, endet 26.08.2026 | Tor existiert (`tm_vix_*`). Auf GC 0 Trials (Klone schließen VIX aus). Auf anderen Märkten 316 Trials, 35 Survivors (alle NQ, ES und YM 0). Zwei getötete Verwandte in `ideas.json` (ORB-VIX-Band, AXV-W26) | W20, W22 | 3 bis 5 % |
| **GEX, DIX** | Aktien-Dealer | Tag | nichts für Gold | keiner | keine Story |
| **GLD-Bestände, GDX** | Gold-Nachfrage | **fehlt** | nichts | W10, W33 | unter 3 % intraday |
| **Shanghai-Prämie, USDCNH** | Nachfrage Asien | **fehlt**, Quelle unklar | nichts. Nachbarn: GC-ON-01 (Nacht-Halten, Prämisse trägt nicht), #174 Urteil C (US → Asien auf GC selbst, unentscheidbar) | W30, W41 | 3 bis 6 %, aber Daten und Engine fehlen |
| **Bitcoin** | Erzählung „digitales Gold“ | **fehlt** (AP311 liegt bei Max) | nichts | W11 | unter 3 % |
| **ZS, ZW** | Agrar | 1 Minute | nichts | keiner | keine Story |
| **Treasury-Auktionskalender** | Termin | **fehlt** (auch Blocker für KF-44 und SZ-14) | nichts | W29 | keine Story für Gold |

**Über die ganze Karte geschätzt:** rund 10 bis 15 %, dass irgendein Weg hier ein echtes Bein fürs Next-Week-Buch liefert. Der größte Teil davon hängt an ZN und 6E, also an Daten, die schon da sind. Neue Daten kaufen oder laden hebt die Zahl kaum, Silber ist die einzige Ladung mit eigenem Wert (enger Ersatz-Markt und selbst handelbar).

---

## Harte Randbedingungen

1. **Kein Basis-Signal mit handelbarer Edge auf Gold.** Die reinen Preis-Signale sind brutto null: 90 Klon-Jobs im RTH-Fenster ([[Strategie-Logbuch]] #165), Eröffnungsimpuls an vier Ankern (#174, 1.800 Configs), COMEX-Richtungsfortsetzung (#180b), dazu vier Prämissen-Tafeln vom 12.10.2026 (Nacht-Halten, London-Band-Fade, VWAP-Rückkehr, Datentag). **Eine Ausnahme mit belegter Information (Korrektur Nachtrag):** TD-12 auf GC (#180c), Steigung +0,0146 ATR je z (CI90 +0,0049 bis +0,0243), IC +0,068 (CI90 +0,021 bis +0,112), Kategorie echt-aber-zu-klein, weil der Vorzeichen-Handel unter den MGC-Kosten bleibt. Dort ausdrücklich „Nicht tot: TD als Filter für andere GC-Mechaniken, Betragsregel“. Für die Filter- und Bestätigungs-Wege (W15, W20) ist TD-12 damit der einzige Träger mit belegter Information. Alle anderen Träger haben nichts zu filtern, diese Rollen sind dort nur als **Mischungs-These** sinnvoll (die Null besteht aus zwei Gruppen mit entgegengesetztem Vorzeichen) und brauchen vorab eine Prämissen-Tafel mit festgelegten Zellen. Sonst Nachher-Filter-Falle (#174 Lehre 4). Exit und Sizing (W36, W37) haben ohne Basis-Signal gar keinen Gegenstand.
2. **Vorlauf: nur eine 5-Minuten-Bar Versatz ist gemessen, und die ist null.** ZN +0,007, 6E +0,002, NQ −0,006 bei n 167.503 (`engine/_scratch_sip_orb/gc_diff.json`, 12.10.2026). `gc_diff.py` (Z. 121 bis 133) korreliert 5-Minuten-Renditen mit einer 5-Minuten-Bar Versatz, 08:20 bis 13:30 ET, linear, unbedingt. Das deckt Vorläufe von 5 bis 10 Minuten. **Ein Vorlauf von 1 bis 4 Minuten landet überwiegend in der gleichzeitigen Korrelation (0,35 und 0,40) und nur verdünnt im Lag-Wert, er ist also nie gemessen** (Daten sind da, 1-Minuten-Bars). Ebenfalls nicht gedeckt: große Sprünge, Datentage, Horizonte über 10 Minuten, andere Sessions, der Fremdmarkt am eigenen Level.
3. **Die Kopplung zerfällt.** GC zu ZN 0,46 (2016 bis 2019) → 0,24 (ab 2024). GC zu 6E 0,46 → 0,36. GC zu NQ wechselte 2020 das Vorzeichen. Research-Cache: Gold gegen Realzins 2022/23 nur noch 3 %, seit 2024 7 %, erklärt mit Zentralbank-Käufen. Jede Story über den Zins-Kanal beschreibt eher die Vergangenheit.
4. **Kosten.** MGC 3,6 $ je Trade. Bis 2023 war alles unter rund 2 Stunden Haltedauer kaum zu bezahlen, seit 2024 liegt Gold bei NQ-Kosten ([[Hypothesen-Bank (Gold & Sessions)]], Kostentabelle). Folge: COMEX-Fenster, ein Trade am Tag, lange Haltedauer.
5. **Session-Fenster und Fremdmarkt vertragen sich noch nicht.** Seit AP197 kann ein Job `session_start` setzen. Auflage des `pipeline-auditor`: mit eigenem Fenster keine Fremdmarkt-Filter (`tm_xref_sym`, `tm_xadx_*`), weil die fest gegen 09:29 rechnen. Geprüft im Code: `sigcore.xref_signal` lädt das Fremdsymbol über `qbt.load_rth` ohne Verschiebung (sigcore.py:873), bei 08:20-Anker würde es 70 Minuten in die Zukunft lesen. Abhilfe ist Modul-Spec S-GCX-1.
6. **Kein neuer Modus.** Einen Null-Schalter haben laut `discovery_lib.NULL_MODES` (Z. 1016): `ts_reversal`, `last_hour`, `asian`, `tsmom`, `maband`, `vwap_pullback`, `orb`, `cal`, `gap`. **`rv` und `vix_bias` nicht**, ein Paar-Trade über `rv` kann nie `deploy_ready` werden. Die Tages-Tore in `sigcore.gates_pass` lesen nur `tsmom` und `maband`.
7. **Daten enden früh, und Gold endet zuerst (Korrektur Nachtrag).** **GC: 24.07.2026** (`exported_data_nt8/GC_FUT_1m.parquet` und `engine/cache/GC_full.parquet`, letzter Zeitstempel 24.07.2026 20:59 UTC; AP196 nennt die GC-Kappung am 24.07. selbst; Stempel #180c ebenso). CL: 21.07.2026. DGS10, DGS2, DTWEXBGS: 14.08.2026. VIX: 26.08.2026. 6E/6B: 14.09.2026. ZN/ZB: 18.09.2026. Folge: jede Gold-Messung endet rund zwei Monate vor ZN und 6E, das Letzte-3-Jahre-Fenster ist entsprechend kürzer. Vor jedem Job auffrischen (AP196).
8. **Langsame Zustände zählen in Episoden, nicht in Tagen.** Eine 5-Tage-Änderung oder ein Korrelations-Zustand wechselt selten. Vor dem ersten Trial `overfit.feasibility_gate()` (#163 Lehre 168). Vergleichswert aus dem eigenen Haus: das Korrelationsregime der Buch-Beine (#141 AR-19) hat eine Halbwertszeit von rund 40 Tagen und damit nur rund 7 unabhängige Hochkorrelations-Episoden. Ereignis-Wege haben rund 44 Datentage im Jahr, je Seite also rund 22 und damit unter der Latte von 25 Trades im Jahr.
9. **Long-Drift.** Gold ist 2024 bis 2026 stark gestiegen. Long und Short stehen getrennt, jeder Long-Weg braucht den Nulldrift-Zwilling mit dem Long-Anteil des Kandidaten.
10. **Kein GC-Bein im Buch.** Live: NQ_Momentum_PB3_fa01b, NQ_LastHour_v3, NQ_Asia-Dir-USopen_d260820, NQ_OpenDrive_maband2050. Next-Week zusätzlich das RTY-Gap-Bein. Jeder Weg hier ist ein **neues Bein**, kein Ersatz. Warnung #139 (01.09.2026) B3: unter der alten Zielfunktion 0 Treffer in 577 Buch-Evals ohne Ersatz. Unter Gate v4 kam aber ein neues Bein durch (RTY-Gap).
11. **Live-Betrieb (Korrektur Nachtrag).** Es gibt keine NT8-Strategie für MGC. Ein Fremdmarkt als zweite Datenreihe braucht Echtzeit-Kurse für ZN (CBOT) und 6E (CME) auf dem Prop-Feed. **ZN, ZB, 6E, 6J, SI, HG und PL sind bei E8 handelbar** (Research-Cache Z. 793, E8-Instrumentenliste, Primärquelle, 09.09.2026). Das „nicht handelbar (Kosten)“ im [[Neue Märkte (NT8-Daten) Plan]] (Z. 63) ist unser Kostenurteil für ZN als Handelsmarkt, keine E8-Regel. Die Feed-Hürde ist für E8 damit klein (am Konto trotzdem nicht nachgesehen). Bei FN stehen Zins-Futures nicht in der Instrumentenliste (Cache Z. 1442), bei FFN ist nichts dazu im Cache: dort bleibt die Frage offen. FRED-Tagesreihen kommen mit Verzug, live trägt eher die ZN-Tagesrendite (Modul-Spec S-GCX-4).
12. **Prop-Regeln.** E8: Fenster 18:15 ET bis 16:10 ET, kein Halten über den Tagesschluss. FN: Overnight verboten. Alles über mehrere Tage ist Live-Buch-Merker ([[Firm-Regeln je Konto]]).

---

## Register-Stand (13.10.2026)

| Griff | Zahl |
|---|---|
| Register gesamt (Zähler über `registry.json`) | **69.587 Trials** |
| GC-Trials | **2.777**, davon 1.805 aus `juli_gc_od_24092026` (#174), Rest Klone und Regime-Filter |
| GC-Survivors | 12, alle aus #174, dort als Nullniveau eingeordnet |
| **GC-Trials mit Fremdmarkt-Achse** (`tm_xref_sym`, `tm_xadx_*`, `tm_dgs*`, `tm_dxy*`, `tm_vix*`, `tm_gex*`) | **0** |
| `tm_xref_sym` auf anderen Märkten | 43, alle NQ: `hyp_XD12_NQ` 31 (0 Survivors), `friedhof_v4_01102026` 12 (**11 Survivors**, Urteil im Friedhof-Nachlauf: empirisch-nichts-gefunden, Rolle Zusatzbein) |
| `tm_xadx_*` auf anderen Märkten | 22, alle NQ: `hyp_ADXW24_NQ` 12, `friedhof_v4_01102026` 10, **0 Survivors** |
| Makro-Tore auf anderen Märkten | `mak01_macrogate_pb3_NQ`: **9 Trials, 6 Survivors** (Tor aus 1, 10Y fällt 2, Dollar steigt 2, Dollar fällt 1), Lauf 12.10.2026, 0 Kandidaten, in der Daily Note 13.10. als „Verdacht zum Nachsehen (kein Urteil)“ geführt (dort 7 von 10, Box-Stand, nicht abgeglichen) |
| VIX-Tore auf anderen Märkten | 316 (NQ 184, ES 92, YM 40), **35 Survivors, alle NQ** (`friedhof_v4_01102026` 28, `lp_prevday_NQ` 4, `hyp_VOLBNULLVIX_NQ` 2, `vt01_delever_short_NQ` 1). Ausgang je Job nicht nachgelesen |
| GEX-Tore | 59 |
| Modus `rv` (Paar-Trades) | 810, nur Index-Paare, kein Gold |
| Modus `vix_bias` | 77 (NQ 25, ES 52) |
| 6E, 6B, ZN, ZB, ZS, ZW, FDAX als Handelsmarkt | 0 Trials |
| Bank-Zeilen zum Konzept | **1** im engen Sinn (Fremdmarkt → Gold): GC-RV-01 „nicht bauen (Story)“. Nachbarn in [[Hypothesen-Bank (Volumen & Flows)]]: XA-32 (Gegenrichtung Gold → ES), XA-28 (Korrelations-Vorzeichen ES zu ZN als Regime), KF-44 und SZ-14 (Treasury-Auktion 13:00 ET, Ziel ES), KF-61 (Monatsende-Rebalancing, geparkt). In `hypothesis_bank.py` 0 Zeilen, die Klon-Regeln schließen `xref`, `rv_sym`, `vix` für neue Märkte aus (Z. 2426 bis 2428). Als „blocked“ geführt: TR-08 (ZN) und TR-09 (DXY), beide für Index-Momentum (Z. 2640) |
| Logbuch-Einträge zum Konzept | **0**. Verwandt und nachgelesen: #033, #090, #141 (AR-19), #163, #165, #171 (ADX auf GC/CL/YM/RTY), #174 (Urteile A und C), #180 (a, b, c), #181, #139. Nur Überschrift: #087 |
| `ideas.json` | keine Gold-Cross-Asset-Karte. Verwandt: „Index-Spread Divergenz-Fade“ (getötet), „Multi-Day-Kointegrations-Pairs“ (Backlog), „ORB-VIX-Band“ (getötet), „AXV-W26“ (getötet), „NQ-ES Lead-Lag“ (getötet) |
| Tickets | AP196 (Daten nachladen, offen), AP221 (Relative Value GC/SI und 6E/6B, datenblockiert, offen), AP143 (Databento-Kostenabfrage GC, CL, SI, NG, ZN, 6E), AP311 (Bitcoin-Daten) |
| Messungen ohne Trials | `gc_diff.json` (12.10.2026, Kopplung und 5-Minuten-Versatz), Zählung GCZINS-01 (Alpha-Scout AP194, 22.09.2026), TD-12 auf GC (#180c), Wei-Nachmessung US → Asien (#174 Urteil C) |
| Research-Cache | Abschnitt „Gold (GC/MGC) Makro-Treiber“ vom 22.09.2026 (Realzins, DXY, Baur/Lucey, Makro-News), Abschnitt vom 24.09.2026 (Donati, Sobti, Smales, **Wei 2026 „Cross-Session Momentum Gold/Silver“, Z. 1445, nur Abstract**). Negativbefund Z. 1478: kein Paper zu Gold intraday bedingt auf Realzins oder Dollar. Kein Eintrag zu Minuten-Vorlauf Zins/Dollar auf Gold, zur Shanghai-Prämie, zum WMR-Fix. Ungelesen vermerkt: Ma/Bouri/Xu/Zhou 2025 („night effect“, China-Gold und Silber). **Neu 13.10.2026:** Abschnitt „Gold Cross-Asset“ (Z. 2083 ff.) mit Lahaye/Laurent/Neely, Awartani/Hussain/Virk 2024, Gürkaynak/Sack/Swanson 2005, Akhtaruzzaman et al. 2021, Cusatis et al. 2009, J.P. Morgan 2026 und zwei Negativbefunden (Lead-Lag Gold gegen Treasury/Dollar auf Minutenbasis; Ausbruch-Fortsetzung in Treasury- und Währungs-Futures) |
| Queue | leer seit 13.10.2026 03:49 (`queue_empty`) |

---

## Elemente und Beziehungen

**Elemente:** Goldpreis (Asien 18:00 bis 02:59, London 03:00 bis 08:19, COMEX 08:20 bis 13:29 ET, US-Nachmittag 13:30 bis 17:00), Fremdmarkt-Bewegung im Fenster, **Fremdmarkt-Level (Vortageshoch und -tief, Nacht-Range)**, Fremdmarkt-Zustand (Trend über Tage, **Trendstärke**, Vola, **Zinskurve**), Kopplung zwischen Gold und Fremdmarkt (Korrelation, Vorzeichen), **Verhältnis der Fremdmärkte untereinander (einig oder im Widerspruch)**, Residuum (Gold minus dem, was Zins und Dollar erklären, mit Null-Linie und Band), Ratio zu einem zweiten Markt (Silber, Kupfer, Platin, Öl), Sprung im Fremdmarkt an einem Termin, Zwangsfluss-Termine im Fremdmarkt, Session-Übergabe.

**Rollen:** Signal, Filter, Level, Zeitfenster, **Exit, Sizing** (die letzten beiden im Nachtrag ergänzt).

**Bewegungen und wo sie stehen:**

| Beziehung | Bewegung | Wege |
|---|---|---|
| Gold zu Fremdmarkt-Bewegung | hin zu (Gold zieht nach) | W1 bis W11 |
| | weg von (Gold löst sich) | W13 |
| | durch hindurch (Gold überschießt) | W28 |
| | entlanglaufen (Gleichlauf) | W15, W17, W18 |
| | nicht mitlaufen | W16 |
| Fremdmarkt zu eigenem Level | kreuzen und halten | W38 |
| | kreuzen und scheitern | W39 |
| Fremdmarkt zu Fremdmarkt | einig | W15 |
| | im Widerspruch | W40 |
| Residuum zu Null-Linie und Band | abprallen und zurück | W12 |
| | kreuzen und halten, kreuzen und scheitern | W14 |
| Fremdmarkt-Zustand | Trend steigt, fällt, flach | W7, W19 |
| | Trendstärke hoch, niedrig | W42 |
| | Kurve steiler, flacher | W43 |
| | Vola eng, weit, wechselt | W20 |
| | Stress | W22, W23 |
| Kopplung | hoch, niedrig, kippt, Vorzeichen | W21 |
| Ratio zum zweiten Markt | hin zum Mittel, weg vom Mittel | W24, W25, W26 |
| Sprung am Termin | folgen, überschießen, andere Termine, Zwangsfluss | W27, W28, W29, W45 |
| Session-Übergabe | London → COMEX, US-Nachmittag → Asien, Asien-Nachfrage | W6, W41, W30 |
| Laufender Trade | schließen bei Dreher des Fremdmarkts, Größe nach Gleichlauf | W36, W37 |
| Mehrtages-Horizont | alle Kanäle | W31 bis W35, W44 |

Jede Bewegung hat eine Long- und eine Short-Seite (a und b). Einstieg früh (im Fenster), bei Bestätigung (Fensterende) oder spät (nach Rücksetzer, `tm_pb_entry`) ist Sache des `variant-scout`. ZB gegen ZN, 6B und 6J gegen 6E, YM/RTY/FDAX gegen NQ/ES sind Achsen, keine eigenen Wege.

---

## Wege-Tabelle

Marke **(Swing)** = nur über mehrere Tage sinnvoll, im Prop-Rahmen verboten.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W1** | Zins führt um Minuten: ZN/ZB bewegt sich, GC zieht 1 bis 5 Min später nach | Trend | Signal | offen für Lags 1 bis 4 Min (nie gemessen, Daten da); Versatz eine 5-Minuten-Bar gemessen, null (+0,007, 0 Trials) | Modul-Spec S-GCX-2 | keiner, keine Story |
| **W2** | Dollar führt um Minuten: 6E/6B → GC | Trend | Signal | wie W1 (5-Minuten-Versatz +0,002) | S-GCX-2 | keiner, keine Story |
| **W3** | Aktien führen um Minuten: NQ/ES → GC | Trend | Signal | wie W1 (5-Minuten-Versatz −0,006) | S-GCX-2 | keiner, keine Story |
| **W4** | Vorlauf unter 1 Minute, alle Kanäle | Trend | Signal | offen, Daten fehlen | keiner (Sekunden-Daten, Latenz) | keiner, keine Story für unsere Technik |
| **W5** | Bedingter Vorlauf: nur nach großem ZN/6E-Sprung ohne Termin zieht GC in 15 bis 60 Min nach | Trend | Signal | offen (nie gemessen) | S-GCX-2 | keiner, Kontrollzelle von W27 |
| **W6** | Session-Vorlauf: Zins/Dollar-Richtung aus London setzt die GC-Richtung in der COMEX-Session | Intraday Bias | Signal | offen (0 Trials, verwandt #180b) | S-GCX-2 mit Fenster vor der Session | keiner, keine Story |
| **W7** | Tages-Vorlauf: Zins/Dollar-Änderung über 5 Tage gibt GC die Richtung für heute | Intraday Bias | Signal | offen (0 Trials auf GC; Frequenz nicht gezählt) | `tsmom` + `tm_dgs10_chg5_*`, `tm_dxy_chg5_*`; rechenbar, aber nur ohne Impuls-Schwelle über der Frequenz-Latte | neues Bein, unter Vorbehalt der Zählung |
| **W8** | Silber führt: SI bewegt sich zuerst, GC zieht nach | Trend | Signal | offen, Daten fehlen | S-GCX-2 nach D-GCX-2 | keiner bis Research |
| **W9** | Öl führt: CL-Sprung → GC über Inflationserwartung | Trend | Signal | offen, keine Story intraday (Swing-Fassung ist W44) | S-GCX-2 | keiner |
| **W10** | Minen und ETF führen: GDX/GLD → GC | Trend | Signal | offen, Daten fehlen, keine Story | keiner | keiner |
| **W11** | Bitcoin führt → GC | Trend | Signal | offen, Daten fehlen, keine Story | keiner | keiner |
| **W12** | Residuum kehrt zurück: GC weicht vom Zins- und Dollar-Wert ab und läuft zurück | Relative Value | Signal | offen (Bank GC-RV-01: nicht bauen, 0 Trials) | Modul-Spec nötig, nicht ausgearbeitet | keiner, kein neuer Grund |
| **W13** | Residuum läuft weiter: GC löst sich vom Zins- und Dollar-Wert und läuft weg | Trend | Signal | offen (0 Trials) | wie W12 | keiner, Gegenzelle von W15 |
| **W14** | Residuum kreuzt Null und hält bzw. scheitert | Relative Value | Signal | offen, keine Story | keiner | keiner |
| **W15** | Bestätigung: GC-Signal nur handeln, wenn ZN und 6E gleichgerichtet mitlaufen | Trend | Filter | offen (0 Trials auf GC) | Weg wie beschrieben (ZN und 6E, COMEX-Anker, je Seite): **Modul-Spec S-GCX-1**. Sofort nur abgespeckt: `ts_reversal` + `tm_xref_sym` mit einem Fremdsymbol, 09:30-Anker, beide Seiten gemischt | neues Bein |
| **W16** | Gold-only-Impuls faden: GC bewegt sich, ZN/6E nicht | Mean Reversion | Signal | offen (0 Trials) | `tm_xref_invert`, Inversions-Arm von W15 | keiner, Vorzeichen offen |
| **W17** | Bestätigung durch Aktien (NQ/ES gleichgerichtet) | Trend | Filter | offen, keine Story | `tm_xref_sym=NQ` sofort | keiner |
| **W18** | Bestätigung durch Silber (Metalle laufen gemeinsam) | Trend | Filter | offen, Daten fehlen | `tm_xref_sym=SI` nach D-GCX-2 | Achse von W15 |
| **W19** | Zins/Dollar-Trend als Schalter: Gold-Momentum trägt oder kippt je nach Zins-Wochenrichtung | Filter | Filter | gemessen ohne Kandidat (0 Trials, Zählung t −2,2, 15 Trades im Jahr) | `tsmom` + `tm_dgs10_chg5_*` sofort | keiner, Frequenz unter 25 |
| **W20** | Makro-Vola als Schalter: ZN/6E-Vola oder VIX-Niveau schaltet Gold-Signale | Filter | Filter | offen (0 Trials auf GC) | `tm_vix_rank_*` sofort | keiner; einziger Träger mit Information wäre TD-12 |
| **W21** | Kopplungs-Zustand als Schalter: Korrelation hoch → Abweichung kehrt zurück, niedrig → läuft weiter; Vorzeichen GC zu NQ als Hafen-Schalter für W22 | Filter | Filter | offen (0 Trials, Messwerte 0,46 → 0,24 und −0,18 → +0,20) | Modul-Spec S-GCX-6 | keiner bis Feasibility |
| **W22** | Aktien-Stress: NQ bricht ein oder VIX hoch → GC long (a). Aktien-Rally → GC short (b) | Intraday Bias | Signal | offen (0 Trials auf GC); b keine Story | Tages-Variante `tm_vix_*` sofort; Intraday S-GCX-2 | neues Bein (nur a) |
| **W23** | Liquidations-Stress: Gold wird im Abverkauf mitverkauft → GC short | Intraday Bias | Signal | offen, keine Story fürs Prop-Buch | S-GCX-2 | keiner |
| **W24** | Gold-Silber-Ratio kehrt intraday zum Mittel zurück | Relative Value | Signal, Level | offen, Daten fehlen (Platz dafür: AP221) | `rv` ohne Null-Schalter; Einbein-Tor als Modul-Spec nach D-GCX-2 | keiner bis Research |
| **W25** | Gold-Silber-Ratio läuft weg (Gold schlägt Silber bei Risk-off) | Trend | Signal | offen, Daten fehlen, keine eigene Story | wie W24 | keiner |
| **W26** | Gold gegen Kupfer, Platin, Öl als Ratio intraday | Relative Value | Signal | offen, keine Story | keiner | keiner |
| **W27** | Datentag 08:30: ZN/6E-Sprung als Überraschungsmaß, GC folgt der ZN-Richtung | Trend | Signal | offen (0 Trials; verwandt GC-NEWS-01, Prämisse trägt nicht) | Modul-Spec S-GCX-2 + S-GCX-3 | neues Bein |
| **W28** | Datentag: GC überschießt gegen den ZN-Sprung und kommt zurück | Mean Reversion | Signal | offen (verwandt GC-NEWS-01: Fade verliert) | wie W27 | keiner, Gegenzelle von W27 |
| **W29** | Sprung an FOMC 14:00, Treasury-Auktion 13:00, EIA Mittwoch 10:30 → GC | Trend | Zeitfenster | offen, keine Story fürs Prop-Buch; Auktionskalender fehlt | wie W27 + D-GCX-4 | keiner |
| **W30** | Asien-Nachfrage: Shanghai-Prämie oder USDCNH-Zustand → GC long in der Asien-Session | Intraday Bias | Filter | offen, Daten fehlen (verwandt GC-ON-01, #174 Urteil C) | Tages-Tor und Nacht-Buchung fehlen | keiner bis Daten |
| **W31** (Swing) | Realzins- und Dollar-Trend über Wochen → Gold über Tage halten | Swing | Signal | offen | kein Mehrtages-Pfad in `tsmom`/`maband` | Live-Buch-Merker, nicht Prop-Buch |
| **W32** (Swing) | Gold-Silber-Ratio im Extrem → Rückkehr über Wochen | Swing | Signal | offen, Daten fehlen (Backlog-Karte „Multi-Day-Kointegrations-Pairs“) | keiner | Live-Buch-Merker |
| **W33** (Swing) | GLD-Bestände und ETF-Zuflüsse → Gold über Tage | Swing | Signal | offen, Daten fehlen | keiner | Live-Buch-Merker |
| **W34** (Swing) | Sicherer Hafen nach Aktien-Crash: Gold long über Tage bis wenige Wochen | Swing | Signal | offen | keiner | Live-Buch-Merker |
| **W35** (Swing) | Kupfer-Gold-Ratio als Konjunktur- und Zins-Zustand über Wochen | Swing | Filter | offen, Daten fehlen, keine Gold-Story | keiner | Live-Buch-Merker |
| **W36** | Exit: offenen GC-Trade schließen, wenn ZN/6E gegen die Position dreht | Filter | Exit | offen, keine Story (kein Basis-Signal) | keiner: `AX_EXITS` kennt nur `eod`, `time`, `rr` | keiner bis ein GC-Bein existiert |
| **W37** | Sizing: Größe des GC-Trades nach Gleichlauf oder Kopplungs-Zustand | Filter | Sizing | offen, keine Story (kein Basis-Signal, bei k1 keine Stufe unter 1 Micro) | keiner | keiner bis GC-Bein und k ≥ 2 |
| **W38** | Fremdmarkt kreuzt sein eigenes Level (Vortageshoch/-tief oder Nacht-Range von ZN, 6E) und hält: GC folgt | Trend | Level | offen (nie gemessen, 0 Trials, Daten da) | Modul-Spec S-GCX-2 + S-GCX-8 | neues Bein |
| **W39** | Fremdmarkt kreuzt sein Level und scheitert: GC dreht | Mean Reversion | Level | offen (nie gemessen) | wie W38 | keiner, Gegenzelle von W38 |
| **W40** | Signalgeber widersprechen sich: ZN sagt long, 6E sagt short (oder umgekehrt). Wem folgt Gold? | Filter | Filter | offen (nie gemessen), keine Story mit Vorzeichen | S-GCX-1 mit zweitem Symbol | keiner, vorab festgelegte Zelle der W15-Tafel |
| **W41** | Session-Übergabe US-Nachmittag → Asien: Bewegung in ZN/6E/NQ 13:30 bis 17:00 ET setzt die GC-Richtung in der Asien-Session bzw. bis zum COMEX-Start | Intraday Bias | Signal | offen, Engine fehlt (verwandt #174 Urteil C, unentscheidbar) | S-GCX-2 plus Nacht-Buchung | keiner bis Feasibility und Engine |
| **W42** | Fremdmarkt-Trendstärke als Schalter: ADX von ZN/6E/NQ schaltet Gold-Signale | Filter | Filter | offen (0 Trials auf GC), keine Story | `tm_xadx_sym` (tsmom.py:320, Default ES) vorhanden, mit eigenem Session-Fenster gesperrt (AP197) | keiner |
| **W43** | Zinskurve als Zustand: 10Y minus 2Y steiler oder flacher als Schalter oder Tages-Richtung für GC | Intraday Bias | Filter | offen (0 Trials), keine Story mit Vorzeichen; Achse von W7/W19 | `tm_dgs2_*` sofort; Kurven-Tor Modul-Spec S-GCX-7 | keiner |
| **W44** (Swing) | Öl und Inflationserwartung (CL, T10YIE) über Wochen → Gold über Tage halten | Swing | Signal | offen, T10YIE fehlt | kein Mehrtages-Pfad | Live-Buch-Merker, nicht Prop-Buch |
| **W45** | Zeitfenster Dollar-Zwangsfluss: WMR-Fix 11:00 ET und Monatsende-Rebalancing im Dollar wirken auf GC | Intraday Bias | Zeitfenster | offen, keine Story fürs Prop-Buch | `cal` kennt den Termin nicht | keiner |

---

## Die Wege im Einzelnen

### Block A: Vorlauf (der Fremdmarkt bewegt sich zuerst)

**W1 Zins führt um Minuten, W2 Dollar führt um Minuten, W3 Aktien führen um Minuten.** **Stand korrigiert (Nachtrag):** gemessen ist nur der Versatz um eine 5-Minuten-Bar, und der ist null (ZN +0,007, 6E +0,002, NQ −0,006, n 167.503). Das deckt Vorläufe von 5 bis 10 Minuten. **Lags von 1 bis 4 Minuten sind auf 1-Minuten-Bars nie gemessen**, sie stecken überwiegend in der gleichzeitigen Korrelation (0,35 und 0,40). Der alte Stand „gemessen ohne Kandidat“ trug für „1 bis 5 Minuten“ also nicht. Trotzdem keine Story: der Research-Cache nennt für Makro-Daten eine Reaktion binnen 30 bis 90 Sekunden, Gold ist selbst einer der liquidesten Makro-Märkte, und ein Trade über wenige Minuten trägt die MGC-Kosten nicht (Randbedingung 4). Die Lücke gehört als Messzelle in die gemeinsame Prämissen-Tafel (Kreuzkorrelation auf 1-Minuten-Bars, Lags 1 bis 4, 0 Register-Trials), nicht in einen Job. **Nicht gedeckt:** bedingt auf große Bewegungen (W5), Datentage (W27), der Fremdmarkt am eigenen Level (W38), andere Sessions als COMEX (W41).

**W4 Vorlauf unter 1 Minute.** Die Gold-Bank nennt das als letzten offenen Punkt. Keine Story für uns: unter einer Minute spielt man gegen Kolokations-Händler, unsere Box handelt per Markt-Order über einen VPS, und die Kosten liegen auf 5 Minuten seit 2024 bei 9 % der typischen Bewegung, darunter höher. Daten fehlen (nur Minuten-Bars). Research-Frage: Halbwertszeit der Anpassung von GC an ZN in Sekunden.

**W5 Bedingter Vorlauf nach großem Sprung ohne Termin.** Story dünn: hat Gold nach 5 Minuten nicht reagiert, war die Bewegung eher zins- oder dollar-intern als dass Gold träge wäre. Nie gemessen. Kein Skelett, läuft als Kontrollzelle (Nicht-Event-Tage) in der Prämissen-Tafel von W27 mit.

**W6 Session-Vorlauf London → COMEX.** Keine Story, weil Gold in London selbst handelt (21 % des Volumens) und Zins und Dollar gleichzeitig einpreist. Verwandt: #180b (Golds eigene London-Richtung setzt sich in der COMEX-Session nicht fort, expR −0,09, N = 4).

**W7 Tages-Vorlauf aus Zins und Dollar (Skelette GCX-W7a long, GCX-W7b short, Rang 3 und 4 unter Vorbehalt).** Der einzige Weg, der ohne Engine-Arbeit läuft: `tsmom` auf GC mit COMEX-Fenster, Richtung fest (`tm_dir`), Tor auf die 5-Tage-Änderung von DGS10 oder DTWEXBGS (sigcore.py:1259 bis 1264). Story-Entwurf: langsame Makro-Bücher schichten über Tage um, der Fluss trifft an den Folgetagen auf die COMEX-Session. Unbelegt. Dagegen: Tages-Autokorrelation von GC 0,01, Realzins-Kopplung seit 2022 fast weg, Long-Tor profitiert von der Gold-Drift.
**Korrektur Nachtrag, Frequenz:** das Tor halbiert die Tage, `tm_dir` halbiert noch einmal. Überschlag, nicht gerechnet: ohne Impuls-Schwelle bleiben grob 60 Trades im Jahr je Seite. Mit der Schwelle aus #174 (rund 30 Trades im Jahr am 08:20-Anker) bleiben nur 7 bis 8 (Überschlag des `verdict-auditor`), das liegt wie W19 unter der Latte von 25. Der Weg ist also **nur ohne Impuls-Schwelle** rechenbar und dann ein reiner Tages-Bias. Die Zählung ist Pflicht vor jedem Job; fällt sie unter 25, entfällt das Skelett.
**Korrektur Nachtrag, Stütze:** die Zählung GCZINS-01 (AP194 Z. 39) misst Gold-Momentum beider Seiten im obersten Zins-Terzil (−3,7 Punkte, t −2,2), ohne Trennung nach Long und Short. Sie stützt „Momentum kippt“ (W19), nicht „GC short“. Die Short-Seite hat damit keinen eigenen Hinweis.
Verwandte, keiner davon tot: Zählung GCZINS-01 (nachträglich, 6 Tests), `mak01_macrogate_pb3_NQ` (dieselben Tor-Zeilen auf NQ, 9 Trials, 6 Survivors, 0 Kandidaten, offener Fall, kein Urteil). Pflicht vorab: Daten auffrischen, Frequenz zählen, `feasibility_gate`, Freigabe der Tages-Tore unter `session_start` durch den `pipeline-auditor` (stehen nicht in der AP197-Verbotsliste, sind aber nicht ausdrücklich freigegeben). Live braucht S-GCX-4.
**Research-Stand 13.10.2026: offen (W7a und W7b).** Kein Paper zu einem Tages-Vorlauf von Zins oder Dollar auf die Gold-Rendite des Folgetags. Im Cache nur Granger Dollar → Gold nach Rezessionen (Z. 1367, Abstract) und die Realzins-Korrelation von 3 bis 7 % seit 2022 (Z. 1365). Das Donati-Hut-Muster (Z. 1447) ist auf GC 2016 bis 2026 nicht reproduziert, die Session-Frage bleibt also auch offen. Short-Seite: der Kopplungsbruch Ende 2022 ist auf Praktiker-Niveau belegt (T. Rowe Price, Janus Henderson, LongtermTrends/LBMA), dazu der asymmetrische Gegner (J.P. Morgan 2026: Gold fällt bei steigenden Renditen weniger). Weiter kein eigener Hinweis für GC short.

**W8 Silber führt.** Story nur Folklore („Silber hat das höhere Beta und läuft vor“). In der Regel führt der liquidere Markt, das wäre Gold. Daten fehlen. Im Cache steht dazu nur Wei 2026 (Gold und Silber über Sessions, nur Abstract, keine Aussage zum Minuten-Vorlauf). Kein Skelett, Research-Frage, Daten-Spec D-GCX-2.

**W9 Öl führt, W10 Minen und ETF führen, W11 Bitcoin führt.** Keine Story intraday. Öl wirkt über Inflationserwartungen und damit über Wochen: das ist ein Swing-Weg und steht seit dem Nachtrag als **W44**. GLD ist ein Derivat des Goldpreises, kein Vorläufer, Minen-Aktien handeln nur 09:30 bis 16:00. Für Bitcoin gibt es keinen Akteur, der Gold wegen Bitcoin handeln muss. CL ist geladen und kann in jeder Messung als Kontrolle mitlaufen.

### Block B: Divergenz und Residuum

**W12 Residuum kehrt zurück.** Das ist GC-RV-01 aus der Gold-Bank: „nicht bauen (Story)“, weil die Story ihr Vorzeichen nicht kennt (läuft Gold zurück oder zieht der Fremdmarkt nach?). Nie gemessen, 0 Trials. **Kein neuer Grund, also kein Skelett.** Ein neuer Grund könnte nur aus W21 kommen (Vorzeichen je Kopplungs-Zustand). Verwandter Toter (Nachtrag): #033, Divergenz-Fade auf Index-Paaren, alle 48 Varianten tot. Der Grund dort waren die doppelten Kosten von zwei Beinen, er überträgt sich nicht auf eine Einbein-Fassung.

**W13 Residuum läuft weiter.** Story-Entwurf: preisunempfindliche Käufer (Zentralbanken, physische Nachfrage) drücken Gold vom Zins-Wert weg und kaufen weiter. Das ist in der Praxis die Gold-Aufwärtsdrift 2024 bis 2026 und kaum von ihr zu trennen. Kein Skelett, fällt als Gegenzelle aus der Tafel von W15 ab.

**W14 Residuum kreuzt Null.** Keine Story, weil der Nulldurchgang eines Regressions-Residuums vom Schätzfenster abhängt und kein Ereignis im Markt ist. Die Bewegung „kreuzen und halten“ an einem echten Markt-Level steht seit dem Nachtrag in W38 und W39.

### Block C: Bestätigung

**W15 Bestätigung durch Zins und Dollar (Skelette GCX-W15a long, GCX-W15b short, Rang 1 und 2).** Story-Entwurf: ein Gold-Impuls, den Zins und Dollar mittragen, ist Makro-Fluss und wird gestückelt abgearbeitet. Ein Impuls ohne beide ist Einzel-Fluss. Die gepoolte Null aus #174 und #180b wäre dann eine Mischung.
**Korrektur Nachtrag, Engine:** „sofort rechenbar“ gilt nur für eine abgespeckte Fassung. `tm_xref_sym` nimmt genau ein Fremdsymbol (das zweite steht erst in S-GCX-1), gerechnet wird auf dem 09:30-Anker, der für Gold nicht der eigene ist (#174: Literal-Klon 09:30 expR +0,155, aber OOS −0,03 und letzte 3 Jahre −0,10), und `ts_reversal` mischt Long und Short in einem Job. **Der Weg wie beschrieben (ZN und 6E zusammen, COMEX-Anker, je Seite) ist Modul-Spec S-GCX-1.**
**Korrektur Nachtrag, XD-12:** die Mechanik lief auf NQ mit ES-Bestätigung zweimal. `hyp_XD12_NQ`: 31 Trials, 0 Survivors. Friedhof-Nachlauf Gate v4 (01.10.2026): 12 Trials, 11 Survivors, Urteil „empirisch-nichts-gefunden, Rolle Zusatzbein“ (dSR −0,092, Walk-Forward 7 von 9). XD-12 scheiterte also am Buch, das NQ-Momentum schon enthält, nicht an der Mechanik. Dieser Grund überträgt sich nicht auf Gold. XD-12 hat keine Logbuch-Nummer.
**Ergänzung Nachtrag, Träger:** der Eröffnungsimpuls (Träger A) hat keine eigene Edge. TD-12 (Träger B, #180c) trägt belegte Information (IC +0,068) und scheitert nur an den Kosten. Eine Bestätigung, die die Treffer verdichtet, könnte ihn über die Kostenhürde heben. Das ist eine vorab festgelegte Zelle der Tafel, kein eigener Job, und der Engine-Weg für TD-12 als Träger ist nicht geprüft (die Messung lief als Skript).
Die Short-Seite hat einen Vorgänger, der am Varianten-Check fiel (XD-W12b, nie gerechnet). **Erst die Prämissen-Tafel, dann ein Job.** Zellen vorab: beide bestätigen, nur einer bestätigt, die Fremdmärkte widersprechen sich (W40), beide laufen gegen Gold (W13), beide flach (W16), je Seite und je Träger.
**Research-Stand 13.10.2026: offen (W15a und W15b).** Keine Studie trennt makro-bestätigte von gold-eigenen Impulsen und misst Fortsetzung gegen Umkehr über 30 bis 300 Minuten. Neu: Lahaye/Laurent/Neely (Fed St. Louis WP 9826, Abstract) ordnen Co-Jumps von Aktien, Anleihen, Wechselkursen und Gold nur Ankündigungen zu, nichts zu Fortsetzung. Negativbefund: keine Studie zu Lead-Lag oder Preisfindung Gold gegen Treasury- bzw. Dollar-Futures auf Minutenbasis (3 Suchläufe, keine Datenbanksuche). Cache Z. 526 betrifft Index-Futures, nicht Gold, Z. 1478 bleibt die Lücke. Short-Seite: Asymmetrie doppelt dokumentiert, aber schwach (J.P. Morgan 13.03.2026, Praktiker; Awartani/Hussain/Virk 2024, IRFA, Abstract, nur FOMC: 5-Minuten-Reaktion stärker bei Lockerung als bei Straffung). Das ist Gegenwind, keine Widerlegung der Fortsetzungs-These. W40 (Zins und Dollar im Widerspruch): Kanal-Dominanz regimeabhängig (Z. 1365 bis 1367), keine Studie zum Gegensatz-Fall.

**W16 Gold-only-Impuls faden.** Vorzeichen nicht begründbar (Einzel-Fluss kann auslaufen oder weiterkaufen). Wird als Inversions-Arm von W15 mitgemessen, kein eigenes Skelett.

**W17 Bestätigung durch Aktien.** Keine Story: Kopplung 0,11 und Vorzeichenwechsel 2020.

**W18 Bestätigung durch Silber.** Achse von W15, sobald SI geladen ist. Kein eigenes Skelett.

**W40 Signalgeber widersprechen sich (Nachtrag).** ZN steigt (Renditen fallen, spricht für Gold), 6E fällt (Dollar steigt, spricht gegen Gold), oder umgekehrt. W15 kannte nur „beide laufen mit“, W16 nur „keiner läuft mit“. Keine Story mit Vorzeichen: man kann für den Dollar argumentieren (stabilere Kopplung, 0,36 gegen 0,24 seit 2024) oder für den Zins (Realzins-Kanal), beides ist geraten. Nie gemessen. Kein Skelett, aber **vorab festgelegte Zelle der W15-Tafel** mit der Erwartung „kein Fortsetzungs-Effekt“. Trägt die Zelle doch, ist das ein Befund für eine eigene Hypothese, kein Nachher-Filter. Engine: braucht das zweite Symbol aus S-GCX-1.

### Block D: Zustand als Schalter

**W19 Zins/Dollar-Trend schaltet Gold-Momentum.** Gemessen ohne Kandidat: die Zählung GCZINS-01 fand im obersten Terzil der 10Y-Wochenänderung ein negatives Gold-Momentum (−3,7 Punkte, t −2,2), bei 15 Trades im Jahr, 6 Tests, im Nachhinein. Der Alpha-Scout stufte das als „kein Job“ ein (Frequenz). Kein Skelett. Offener Verwandter mit denselben Tor-Zeilen: `mak01_macrogate_pb3_NQ` (9 Trials, 6 Survivors, kein Urteil).

**W20 Makro-Vola als Schalter.** Keine eigene Story. Golds eigene Vola- und Volumen-Filter trennten in #174 nichts. Ein VIX-Tor auf ein Signal ohne Edge wäre der nächste Nachher-Filter. **Nachtrag:** auf anderen Märkten 316 VIX-Tor-Trials, 35 Survivors, alle NQ. Zwei getötete Verwandte in `ideas.json`: „ORB-VIX-Band“ (das VIX-Band war OOS nur ein Vola-Proxy, außerhalb des Bands lief es besser) und AXV-W26 (ADX-Tor gegen VIX-Tor, Unterschied +0,0015 R, CI90 enthält 0). Der einzige Träger, auf dem ein Schalter hier etwas zu schalten hätte, ist TD-12 (#180c).

**W21 Kopplungs-Zustand als Schalter.** Story-Entwurf: ist Gold eng an Zinsen gekoppelt, sind Abweichungen Rauschen und laufen zurück (W12 bekäme ein Vorzeichen). Ist Gold entkoppelt, sind Abweichungen Information und laufen weiter (W13). Das würde auch erklären, warum auf Gold alles nur 2023 bis 2026 trägt. **Zweite Achse (Nachtrag): das Vorzeichen der Kopplung GC zu NQ** (−0,18 bis 2019, +0,20 ab 2020) als Schalter „Gold als Hafen“ gegen „Gold als Risiko-Anlage“. Nur im Hafen-Zustand hätte W22a seine Story. Problem bei beiden Achsen: der Zustand wechselte im Datensatz im Kern einmal. Lebende Verwandte derselben Bewegung: Bank XA-28 (Vorzeichen der 60-Tage-Korrelation ES zu ZN als Regime, ungetestet) und #141 AR-19 (Korrelationsregime der Buch-Beine, Halbwertszeit rund 40 Tage, rund 7 unabhängige Episoden, „vermutlich zu wenig für einen Familien-Null-Test“). Diese Zahl ist der beste Anhaltspunkt für die Feasibility hier. **Feasibility vor Skelett.** Modul-Spec S-GCX-6 nur skizziert.

**W22 Aktien-Stress (Skelett GCX-W22a long, Rang 7).** Teils gestützt: Baur und Lucey 2010 (Research-Cache) zeigen Gold als sicheren Hafen im extremen Aktien-Stress, kurzlebig. Unbelegt ist, ob die Flucht nach der ersten Stunde weiterläuft. Dagegen: seit 2020 läuft Gold intraday mit dem Nasdaq (siehe W21, zweite Achse), und starke Abverkäufe sind selten. Tages-Variante über `tm_vix_rank_min` sofort, Intraday-Variante über S-GCX-2. Lebender Verwandter: VIX-Spike-Reversion auf NQ (#087). **W22b** (Aktien-Rally → Gold short): keine Story, die Safe-Haven-Eigenschaft ist einseitig.
**Research-Stand 13.10.2026: offen (W22a).** Der Mechanismus ist nur schmal gestützt: Baur/Lucey 2010 (Cache Z. 1368, kurzlebiger sicherer Hafen nur im extremen Stress) und neu Akhtaruzzaman/Boubaker/Lucey/Şensoy 2021 (Economic Modelling, hochfrequente Daten: sicherer Hafen nur in Phase I der COVID-Krise, in Phase II verloren). Eine Fortsetzung nach der ersten RTH-Stunde ist nirgends belegt, und ein NQ-Einbruch in der ersten Stunde ist kein extremer Stress im Sinne der Papers. Das alte „teils gestützt“ gilt nur für den Mechanismus, nicht für den handelbaren Teil.

**W23 Liquidations-Stress.** Keine Story fürs Prop-Buch: eine Handvoll Episoden in zehn Jahren, nicht entscheidbar.

**W42 Fremdmarkt-Trendstärke als Schalter (Nachtrag).** Die Achse existiert: `tm_xadx_sym` (tsmom.py:320, Default ES) mit `tm_xadx_min/max` und `tm_xadx_rank_*`. Im Register 22 Trials auf NQ, 0 Survivors. Keine Story: es gibt keinen Akteur, der Gold anders handelt, weil ZN „stark trendet“, und ohne Basis-Signal ist es der nächste Nachher-Filter. Toter Verwandter: #171 (22.09.2026), ADX des Vortags trägt auf keinem von sechs Märkten Information über den Folgetag, Gold eingeschlossen. Dort war es Golds eigener ADX, hier wäre es der des Fremdmarkts, das ist der einzige Unterschied. Mit eigenem Session-Fenster ist die Achse laut AP197-Auflage gesperrt.

**W43 Zinskurve als Zustand (Nachtrag).** DGS2 steht in der Signalgeber-Tabelle, das Tor `tm_dgs2_*` existiert, aber kein Weg nutzte die Kurve. Keine Story mit Vorzeichen: eine steilere Kurve kann von fallenden kurzen Zinsen kommen (Zinssenkungs-Erwartung, eher gut für Gold) oder von steigenden langen Zinsen (Laufzeitprämie, eher schlecht), das Vorzeichen hängt also daran, welches Ende sich bewegt. Die Zählung GCZINS-01 hat die 2Y-Fassung mitgemessen (−3,8 Punkte, t −2,3, gleiche 15 Trades im Jahr). Engine: 2Y allein sofort (`tm_dgs2_chg5_*`), ein Kurven-Tor fehlt (S-GCX-7, rund 8 Zeilen). Geführt als **benannte Achse von W7 und W19**, kein eigenes Skelett, gleiche Frequenz- und Episoden-Schranke.

### Block E: Paar und Ratio

**W24 Gold-Silber-Ratio kehrt intraday zurück.** Daten fehlen. Als Paar-Trade liefe es über `rv`, das keinen Null-Schalter hat und doppelte Kosten trägt. Als Einbein-Tor (nur GC handeln, wenn Gold gegen Silber billig ist) bräuchte es eine Modul-Spec. Story-Entwurf schwach, weil unklar ist, welches der beiden Metalle sich anpasst. Research-Frage, kein Skelett. **Nachtrag:** toter Verwandter ist #033 (04.08.2026) und die `ideas.json`-Karte „Index-Spread Divergenz-Fade“: `div_fade` in allen 48 Varianten tot, Grund doppelte Kosten bei zwei Beinen. Vorbehalt: #033 stammt von vor dem `rv.py`-Fix (#090) und trägt keine Pflichtfelder, also „empirisch, altes Lineal“, kein Strukturbeweis. Der Platz für diesen Weg existiert schon: **Ticket AP221** (Relative Value GC/SI und 6E/6B, datenblockiert, offen). Zweite Datenquelle neben NT8: AP143 (Databento-Kostenabfrage).

**W25 Ratio läuft weg, W26 Gold gegen Kupfer, Platin, Öl.** Keine eigene Story intraday. Verwandter aus #033: `div_mom` auf Index-Paaren „nur marginal (Bank)“, gleiches Lineal-Problem wie oben.

### Block F: Sprung am Termin

**W27 Datentag, ZN-Sprung als Überraschungsmaß (Skelette GCX-W27a long, GCX-W27b short, Rang 5 und 6).** Der neue Winkel zu GC-NEWS-01: dort war Golds eigenes Vorzeichen wertlos, und es fehlten Konsensdaten. Der ZN-Sprung ist die Markt-Lesart der Überraschung. Story-Entwurf: Gold verarbeitet die Zahl über zwei Kanäle in einem dünneren Buch und hängt der ZN-Lesart nach oder läuft kurz gegen sie, Makro-Händler schließen die Lücke. Unbelegt. Dagegen: Reaktion laut Cache in 30 bis 90 Sekunden durch, die Zelle mit Widerspruch ist selten, gleicher Eventsatz wie GC-NEWS-01 (nicht unabhängig). Frequenz: rund 44 Datentage im Jahr, je Seite rund 22. Ein Job geht nur mit beiden Seiten zusammen, die Seiten weist `ctl_sides` getrennt aus. Engine: Modul-Spec S-GCX-2 und S-GCX-3. Verwandte: Bank GC-NEWS-01 (Prämisse trägt nicht, kein Urteil gestempelt), #181 (NQ), #174.
**Research-Stand 13.10.2026: offen (W27a und W27b).** Eine verzögerte Gold-Anpassung über 90 Sekunden hinaus ist nur für FOMC belegt (Awartani/Hussain/Virk 2024: Anpassung läuft über 5 Minuten weiter, Abstract). Für die 08:30-Daten bleibt es bei 30 bis 90 Sekunden (Cache Z. 1373). Sobti (Z. 1448) sagt nichts zu Fortsetzung, der Volltext war am 13.10. nicht lesbar. Der Zins-Sprung als Überraschungsmaß ist nur für FOMC etabliert (Gürkaynak/Sack/Swanson 2005), für CPI/NFP mit ZN wurde keine Validierung gefunden. Short-Seite: Awartani 2024 und J.P. Morgan 2026 zeigen die stärkere Gold-Reaktion bei Lockerung bzw. fallenden Renditen (Gegenwind), Smales 2014 (Z. 1449) negative Nachrichten stärker, in der Rezession umgekehrt. Der Widerspruch zu Z. 1373 ist nicht aufgelöst.

**W28 Gold überschießt und kommt zurück.** Verwandte Messung: der gepoolte Fade in GC-NEWS-01 verliert (t −1,7 bis −2,3). Kein neuer Grund für ein eigenes Skelett, fällt als Gegenzelle aus W27 ab.

**W29 FOMC, Auktion, EIA.** Keine Story fürs Prop-Buch: FOMC hat 8 Termine im Jahr (#181c: n 84, nicht entscheidbar), EIA trägt nicht einmal auf CL selbst (#180a), für die Treasury-Auktion gibt es im Cache nur einen Beleg für ZN, keinen für Gold. **Nachtrag:** die Auktion 13:00 ET steht schon zweimal in der Bank, mit Ziel ES (KF-44, SZ-14), beide blockiert, weil der **Auktionskalender fehlt**. Der Blocker ist also auch ein fehlender Datensatz (D-GCX-4), nicht nur die Story. Research-Frage.

**W45 Dollar-Zwangsfluss (Nachtrag).** WMR-Fix (16:00 London, 11:00 ET) und Monatsende-Rebalancing im Dollar. Keine Story fürs Prop-Buch. Tägliche Fassung: die Richtung des Fix-Flusses ist ohne Kenntnis des Überhangs nicht vorab bekannt, und Gold preist eine Dollar-Bewegung gleichzeitig ein (Kopplung 0,40). Monatsende-Fassung: 12 Termine im Jahr, weit unter der Latte. Verwandte, keiner davon ein sauberer Toter: #163 (Monatsende-Rebalancing auf Aktien, Titel „endgültig tot“, nach der eigenen Lehre 168 unentscheidbar, weil die Kill-Schwelle 27 bis 29 Jahre Historie bräuchte) und Bank KF-61 (stetige Fassung, geparkt, vorab unentscheidbar). Im Cache steht zum WMR-Fix nichts. Nachbar ohne Fremdmarkt: der LBMA-Nachmittags-Fix (15:00 London) als Golds eigener Zwangsfluss, in #180b unter „Nicht tot“.

### Block G: Asien und Session-Übergabe

**W30 Shanghai-Prämie oder USDCNH.** Der einzige Signalgeber mit einem anderen Akteur (physische Nachfrage in Asien). Story-Entwurf: hohe Prämie = Käufer in Shanghai zahlen über London, Arbitrage zieht Metall nach Osten, Gold steigt in der Asien-Session. Donati 2019 (im Cache) beschreibt den Tagesgang dazu, auf unseren Daten 2016 bis 2026 ist das Muster nicht vorhanden (Cache Z. 1447). **Nachtrag:** Wei 2026 (Cache Z. 1445, nur Abstract) meldet für 07/2024 bis 08/2026, dass die Asien-Session 77 % der Gold-Rendite trägt und US → Asien mit +0,13 fortsetzt. Unsere Nachmessung (#174 Urteil C): ρ +0,01 [−0,07; +0,11], Kategorie unentscheidbar, Sessiongrenzen geraten. Dagegen: GC-ON-01 (Nacht-Halten ohne Bedingung) trug nur 2025/26. Blocker: keine Datenquelle, Nacht-Fenster brauchen den Buchungsdatum-Umbau, FN verbietet Overnight. Kein Skelett, Research-Frage.

**W41 Session-Übergabe US-Nachmittag → Asien (Nachtrag).** Nach dem COMEX-Schluss (13:30 ET) handelt Gold dünn, ZN, 6E und NQ laufen bis 16:00 bzw. 17:00 ET mit vollem Buch weiter. These: die Nachmittags-Bewegung der Fremdmärkte setzt die Gold-Richtung in der Asien-Session bzw. bis zum nächsten COMEX-Start. Story dünn: Gold handelt in dem Fenster durchgehend und preist mit (gleiches Argument wie W6), ein Rückstand bräuchte einen Akteur, der erst in Asien handeln kann. Das wäre die physische Nachfrage aus W30. Verwandt: #174 Urteil C (US → Asien auf Gold selbst, ρ +0,01, **unentscheidbar**, zählt nicht als Friedhof; Wiedervorlage dort: Volltext Wei mit den Sessiongrenzen). Die Fremdmarkt-Fassung hat dieselbe Stichprobe und damit dieselbe Auflösungsgrenze (MDE 0,07). Stand: offen, Engine fehlt (Signal aus dem Fremdmarkt S-GCX-2, dazu die Nacht-Buchung). E8 erlaubt das Fenster ab 18:15 ET, FN nicht. Kein Skelett: erst Feasibility und der Wei-Volltext, dann eine Zelle der Tafel (Daten für GC, ZN, 6E sind da).

### Block H: Swing (Live-Buch-Merker, kein Job fürs Prop-Buch)

**W31 Realzins- und Dollar-Trend über Wochen.** Cross-Asset-Momentum. Im Cache: Pitkäjärvi et al. belegen es für Bonds und Aktien auf Monatsebene, für Gold nichts, und die Realzins-Kopplung ist seit 2022 fast weg.
**W32 Gold-Silber-Ratio im Extrem.** Klassischer Wochen-Trade, Daten fehlen. Platz dafür: `ideas.json` „Multi-Day-Kointegrations-Pairs“ (Backlog, #033: „für den Live-Account notiert“).
**W33 GLD-Bestände.** Tagesdaten wären gratis, Quelle und Vorlauf ungeprüft.
**W34 Sicherer Hafen nach Aktien-Crash.** Baur und Lucey (im Cache): der Effekt ist kurzlebig, eine genaue Dauer steht nicht im Cache.
**W35 Kupfer-Gold-Ratio.** Zeigt eher auf Zinsen als auf Gold, keine Gold-Story.
**W44 Öl und Inflationserwartung über Wochen (Nachtrag).** W9 begründete „keine Story“ damit, dass der Inflationskanal über Wochen wirkt. Dann ist es ein Swing-Weg und wird nach der Regel vom 11.09.2026 mitgeführt: steigen Ölpreis und Inflationserwartung (T10YIE) über Wochen, wird Gold als Inflationsschutz gekauft, Halten über Tage. Unbelegt, im Cache nichts dazu. CL ist geladen, T10YIE fehlt (FRED, gratis, D-GCX-2). Live-Buch-Merker, kein Job fürs Prop-Buch.

### Block I: Fremdmarkt am eigenen Level (Nachtrag)

**W38 Fremdmarkt kreuzt sein Level und hält (Skelette GCX-W38a long, GCX-W38b short, Rang 8 und 9).** „Kreuzen und halten“ stand bisher nur für die Null-Linie des Residuums (W14), W5 kennt nur die Sprunggröße, kein Level. Hier: ZN oder 6E schließt über dem eigenen Vortageshoch oder über dem Hoch der Nacht-Range und liegt nach einer festen Haltezeit noch darüber → GC long. Spiegel am Tief → GC short. Story-Entwurf: an diesen Marken liegen Stops und Ausbruchs-Orders der Zins- und Devisen-Händler, hält der Ausbruch, arbeiten trendfolgende Bücher ihn über Stunden ab, und Gold läuft über die gleichzeitige Kopplung mit. Gehandelt würde Gold, weil ZN nach unserem Kostenurteil nicht bezahlbar ist (Kostenquote 10 % im Neue-Märkte-Plan) und MGC seit 2024 schon. Liegen bleiben könnte das Geld, weil Gold-Händler auf Gold-Marken schauen. Unbelegt. Dagegen: ob Ausbrüche in ZN oder 6E überhaupt weiterlaufen, ist bei uns nie gemessen (beide 0 Trials als Handelsmarkt), der Effekt käme bei Gold nur verdünnt an (Kopplung 0,24 bzw. 0,36 seit 2024), und der unbedingte 5-Minuten-Versatz ist null. Engine: Modul-Spec S-GCX-2 plus S-GCX-8 (Level-Zustand am Fensterende). Tote Verwandte auf Gold: keiner gefunden (Logbuch-Überschriften zu Vortageshoch und Nacht-Range: 0 Treffer, nur Überschriften gesucht). **Zuerst eine Zelle der Prämissen-Tafel**, Daten sind da.
**Research-Stand 13.10.2026: offen (W38a und W38b).** Osler 2005 und 2003 (Cache Z. 944 bis 945, peer-reviewed, FX) stützen Stop-Cluster jenseits von Vortageshochs, aber Take-Profit- und Stop-Loss-Orders wirken gegensätzlich. Cusatis/Kulkarni/Thomas 2009 (neu, Abstract) finden für Treasury-Note-Futures intraday **negative** Serienkorrelation, das spricht gegen Fortsetzung in ZN (17 Jahre alt, nicht auf Level-Ausbrüche bezogen). Kein Paper zur Fortsetzung von Ausbrüchen in ZN oder 6E, keines zur Übertragung auf Gold. Die erste Stufe der Kette hat damit einen Gegenhinweis und keinen Beleg. Short-Seite zusätzlich gegen den Zentralbank-Käufer (J.P. Morgan 2026) und die schwächere Gold-Reaktion auf Straffung (Awartani 2024).

**W39 Fremdmarkt kreuzt sein Level und scheitert.** ZN oder 6E kreuzt die Marke und fällt binnen der Haltezeit zurück → GC gegen die Ausbruchsrichtung. Keine eigene Story über den Spiegel von W38 hinaus, „scheitern“ braucht ein zusätzliches Zeitfenster als freien Parameter. Gegenzelle von W38 in derselben Tafel, kein Skelett.

### Block J: Exit und Sizing (Nachtrag)

**W36 Exit über den Fremdmarkt.** Einen offenen GC-Trade schließen, wenn ZN oder 6E gegen die Position dreht. Keine Story, weil es kein Basis-Signal gibt (Randbedingung 1): ein Exit kann nur einen Trade mit positivem Erwartungswert verbessern. Dazu kommt die gleichzeitige Kopplung: der Dreher im Fremdmarkt und der Verlust in Gold fallen in dieselbe Minute, der Exit wäre ein zweiter Stop. Engine: `AX_EXITS` kennt `eod`, `time`, `rr` (hypothesis_bank.py:108 bis 112), ein Fremdmarkt-Exit fehlt in `tsmom` und `maband`. Keine Modul-Spec, solange kein Träger existiert. Wiedervorlage: sobald ein GC-Bein im Next-Week-Buch steht.

**W37 Sizing über Gleichlauf oder Kopplungs-Zustand.** Größer handeln, wenn Zins und Dollar mitlaufen oder die Kopplung hoch ist. Keine Story, weil es kein Basis-Signal gibt. Zusätzlich hat der Betriebspunkt k1 (1 Micro je Bein) keine Stufe unter 1: Sizing fällt dort auf An/Aus zusammen und ist dann der Filter aus W15 bzw. W21. Wiedervorlage: GC-Bein vorhanden und k mindestens 2.

---

## Verwandte: tot, gemessen ohne Urteil, lebend

Die erste Fassung hat diese drei Gruppen in einem Feld gemischt. Getrennt:

| Gruppe | Eintrag | Betrifft | Was gleich ist, was anders |
|---|---|---|---|
| **tot** | #174 Urteil A (GC-Eröffnungsimpuls, N = 1.800, empirisch-nichts-gefunden) | W15, W7, W20, W22, W27 | gleiches Basis-Signal, neu ist die Fremdmarkt-Bedingung |
| tot | #180b (GC-COMEX-Fortsetzung, N = 4, empirisch-nichts-gefunden) | W6, W15 | Golds eigene Richtung; dort „Nicht tot: Gold-Zins-Lead, Datentage, LBMA-Fix-Zeiten“ |
| tot | #165 (GC-Klone im RTH-Fenster, 0 Survivors) | alle Filter-Wege | RTH-Fenster, NQ-Mechaniken |
| tot | #180c TD-12 auf GC (echt-aber-zu-klein) | W15, W20 | Information belegt, scheitert an den Kosten; „Nicht tot: TD als Filter“ |
| tot | #033 und `ideas.json` „Index-Spread Divergenz-Fade“ (48 Varianten, doppelte Kosten) | W12, W24, W25, W26 | Index-Paare, zwei Beine; altes Lineal (vor dem `rv.py`-Fix), keine Pflichtfelder |
| tot | #090 (NQ-ES-Vorlauf, Tod bestätigt) | W1 bis W3 | andere Märkte, gleiche Mechanik |
| tot | XD-12 (NQ mit ES-Bestätigung; Friedhof-Nachlauf: empirisch-nichts-gefunden, Rolle Zusatzbein) | W15 | gleiche Mechanik; gescheitert am Buch, nicht an der Mechanik; keine Logbuch-Nummer |
| tot | #171 (ADX des Vortags ohne Folgetag-Information, 6 von 6 Märkten) | W42 | Golds eigener ADX statt Fremdmarkt-ADX |
| tot | `ideas.json` „ORB-VIX-Band“ und AXV-W26 (VIX-Tor nur Vola-Proxy; ADX gegen VIX, CI enthält 0) | W20 | NQ, andere Träger |
| tot | #180a (EIA auf CL, N = 36, empirisch-nichts-gefunden), #181a (NQ, gepoolter Fade nach 08:30-Releases, empirisch-nichts-gefunden) | W29, W27 | andere Märkte, gleiches Fenster |
| **gemessen ohne Urteil** | Zählung GCZINS-01 (AP194) | W19, W43 | nachträglich, 6 Tests, 15 Trades im Jahr; stützt „Momentum kippt“, nicht „GC short“ |
| gemessen ohne Urteil | `mak01_macrogate_pb3_NQ` (9 Trials, 6 Survivors, 0 Kandidaten) | W7, W19 | dieselben Tor-Zeilen auf NQ; offener Fall |
| gemessen ohne Urteil | Bank GC-NEWS-01, GC-ON-01 (Prämisse trägt nicht, kein Stempel) | W27, W28, W30 | Golds eigenes Vorzeichen, gleicher Eventsatz |
| gemessen ohne Urteil | `gc_diff.json` (5-Minuten-Versatz null) | W1 bis W3, W38 | unbedingt, linear, eine Bar |
| **unentscheidbar** (kein Friedhof) | #174 Urteil C (Wei, US → Asien auf GC) | W41, W30 | Gold selbst statt Fremdmarkt |
| unentscheidbar | #181b (NFP auf NQ) und #181c (CPI, FOMC n 84, übrige Zellen) | W27, W29 | NQ |
| unentscheidbar | #163 (Monatsende-Rebalancing, Titel „endgültig tot“) | W45 | Aktien statt Gold |
| **lebend oder offen** | #087 VIX-Spike-Reversion auf NQ | W22 | gleicher Auslöser, anderes Ziel |
| lebend oder offen | #141 AR-19 (Korrelationsregime, Stufe 1), Bank XA-28 | W21 | gleiche Bewegung, andere Märkte |
| lebend oder offen | Bank XA-32 (Gegenrichtung), KF-44, SZ-14 (Auktion, ES), KF-61 (geparkt) | W22, W34, W29, W45 | anderes Ziel |
| lebend oder offen | AP221, AP143, AP196, Backlog „Multi-Day-Kointegrations-Pairs“ | W24, W32, D-GCX | Platz und Daten |
| nie gerechnet | XD-W12b (Short-Seite, am Varianten-Check raus) | W15b | NQ/ES |
| Lehre, kein Urteil | #163 Lehre 168, #174 Lehre 4 | W7, W19, W21, alle Filter | Feasibility vor dem Trial, Nachher-Filter-Falle |

---

## Reihenfolge nach Buch-Chance

Regel: Ersatz vor neu (hier alles neu), rechenbar vor Modul-Spec, ohne tote Verwandte vor kontaminiert, Intraday-Information vor langsamem Zustand.

| Rang | Skelett | Weg | Engine | Why-Stand | Warum dieser Rang |
|---|---|---|---|---|---|
| 1 | GCX-W15a | Bestätigung Zins und Dollar, long | abgespeckt sofort (ein Fremdsymbol, 09:30, beide Seiten gemischt); der Weg wie beschrieben S-GCX-1 | offen (Research 13.10.) | Daten da, schärfste prüfbare These (Mischung), Mechanik lieferte auf NQ Survivors |
| 2 | GCX-W15b | dasselbe, short | wie Rang 1 | offen (Research 13.10.) | Short-Seite gegen die Gold-Drift, Vorgänger XD-W12b am Varianten-Check raus |
| 3 | GCX-W7a | Renditen fallen über 5 Tage, GC long | `tsmom` + `tm_dgs10_chg5_max`, rechenbar | offen (Research 13.10.) | rechenbar, aber langsamer Zustand, Long-Drift und **Vorbehalt Frequenz-Zählung** |
| 4 | GCX-W7b | Renditen steigen, GC short | wie Rang 3 | offen (Research 13.10.) | wie Rang 3, ohne jeden Hinweis aus einer Messung |
| 5 | GCX-W27a | Datentag, ZN-Sprung, GC long | Modul-Spec S-GCX-2 + S-GCX-3 | offen (Research 13.10.) | originellster Weg, braucht Engine-Arbeit, je Seite nur rund 22 Trades im Jahr |
| 6 | GCX-W27b | dasselbe, short | wie Rang 5 | offen (Research 13.10.) | Asymmetrie der Gold-Reaktion unklar |
| 7 | GCX-W22a | Aktien-Stress, GC long | Tages-Variante sofort, Intraday S-GCX-2 | offen (Research 13.10.), Mechanismus schmal gestützt | seltene Ereignisse, Kopplung seit 2020 positiv |
| 8 | GCX-W38a | ZN/6E hält über dem eigenen Level, GC long | Modul-Spec S-GCX-2 + S-GCX-8 | offen (Research 13.10.) | Daten da, kein toter Verwandter, aber zweistufige Kette und verdünnter Effekt |
| 9 | GCX-W38b | dasselbe am Tief, short | wie Rang 8 | offen (Research 13.10.) | wie Rang 8, gegen die Gold-Drift |

**Empfehlung des Scouts (Entscheidung liegt bei der Hauptsession und Max):** vor jedem Job eine gemeinsame Prämissen-Tafel auf den vorhandenen Minuten-Daten (GC, ZN, 6E, NQ), Zellen vorab festgelegt, 0 Register-Trials. Sie beantwortet W15, W16, W13, W40, W27, W28, W5, W22, W38, W39 und die Lücke aus W1 bis W3 (Lags 1 bis 4 Minuten) in einem Lauf und entscheidet, ob S-GCX-1, S-GCX-2 und S-GCX-8 überhaupt gebaut werden. Neun Skelette als neun Jobs würden nur die Zufallsdecke heben. Die Tafel hat viele Zellen, die Korrektur für Mehrfachtests gehört vorab festgelegt.

**Buch-Lücke für alle Skelette:** Stufe 0, vor der Prämisse. Danach: Survivors und Vor-Gates → Walk-Forward → Buch-Sharpe steigt → Next-Week-Buch → Wochenend-Prüfung → NT8-Strategie für MGC mit zweiter Datenreihe (existiert nicht) → Paritäts-Prüfung.

---

## Research-Stand 13.10.2026 (Rückschreibung)

Quelle: `research-scout` am 13.10.2026, neuer Abschnitt im [[Research-Cache]] (Z. 2083 ff., „Gold Cross-Asset“). Lesetiefe dort: Abstract bzw. Zusammenfassung, kein Volltext. **Ergebnis: 9 von 9 offen, 0 belegt, 0 widerlegt.** Kein Why wurde überarbeitet, weil keines belegt ist. „Offen“ heißt: die Literatur entscheidet die Frage nicht, das kann nur die eigene Prämissen-Tafel.

| Skelett | Research-Stand | Was gefunden wurde | Quelle | An `ein-weg` in dieser Runde |
|---|---|---|---|---|
| GCX-W15a | offen | Keine Studie trennt makro-bestätigte von gold-eigenen Impulsen über 30 bis 300 Minuten. Co-Jump-Literatur ordnet nur Ankündigungen zu. Kein Lead-Lag-Beleg auf Minutenbasis. W40-Frage offen | Cache Z. 1478, Z. 526 (Index-Futures), Z. 1365 bis 1367; neu Lahaye/Laurent/Neely (Fed St. Louis WP 9826, Abstract) | ja |
| GCX-W15b | offen, Gegenwind | Asymmetrie gegen die Short-Seite doppelt dokumentiert, aber schwach. Keine Widerlegung der Fortsetzungs-These, kein Intraday-Test seit 2022 | J.P. Morgan Private Bank 13.03.2026 (Praktiker); Awartani/Hussain/Virk 2024, IRFA (Abstract, nur FOMC) | ja |
| GCX-W7a | offen | Kein Paper zum Tages-Vorlauf Zins/Dollar auf den Gold-Folgetag. Session-Frage offen (Donati bei uns nicht reproduziert). Eigene Zählung nachträglich, 15 Trades im Jahr | Cache Z. 1367 (Granger, Abstract), Z. 1365, Z. 1447; Zählung GCZINS-01 | ja |
| GCX-W7b | offen, Gegenwind | Wie W7a. Kopplungsbruch 2022 auf Praktiker-Niveau belegt, asymmetrischer Gegner. Zählung trennt Long und Short nicht, stützt W19 | T. Rowe Price, Janus Henderson, LongtermTrends/LBMA (Z. 1365); J.P. Morgan 2026 | ja |
| GCX-W27a | offen | Verzögerte Anpassung über 90 Sekunden nur für FOMC belegt. Für 08:30-Daten 30 bis 90 Sekunden. ZN-Sprung als Überraschungsmaß für CPI/NFP nicht validiert gefunden. Sobti-Volltext nicht lesbar | Awartani 2024 (Abstract); Cache Z. 1373, Z. 1448; Gürkaynak/Sack/Swanson 2005 | ja |
| GCX-W27b | offen, Gegenwind | Asymmetrie seit 2020 zeigt eher stärkere Gold-Reaktion bei Lockerung. Widerspruch zu Z. 1373 nicht aufgelöst | Awartani 2024; J.P. Morgan 2026; Smales 2014 (Cache Z. 1449) | ja |
| GCX-W22a | offen | Mechanismus schmal gestützt (nur extremer Stress, nur phasenweise). Fortsetzung nach der ersten RTH-Stunde nirgends belegt | Baur/Lucey 2010 (Cache Z. 1368); neu Akhtaruzzaman et al. 2021 | ja |
| GCX-W38a | offen, Gegenhinweis | Stop-Cluster an Vortageshochs in FX belegt, Wirkung zweischneidig. ZN intraday negativ serienkorreliert. Kein Paper zur Ausbruch-Fortsetzung in ZN/6E, keines zum Gold-Transfer | Osler 2005/2003 (Cache Z. 944 bis 945); neu Cusatis/Kulkarni/Thomas 2009 (Abstract) | ja |
| GCX-W38b | offen, Gegenwind | Wie W38a, dazu Zentralbank-Käufer und schwächere Gold-Reaktion auf Straffung | wie W38a; J.P. Morgan 2026; Awartani 2024 | ja |

**Nicht an `ein-weg` in dieser Runde:** keines gestrichen (kein Skelett widerlegt, kein Swing-Skelett, kein Why zu kurz). **Aber: `ein-weg` ist am 13.10.2026 nicht gelaufen** (Hauptsession hat den Schritt ausgelassen, Max wollte die Übersicht, keine Bank-Einträge). Die Spalte „ja“ heißt also nur „dürfte an `ein-weg`“. Vor jeder Bank-Zeile oder jedem Job steht `ein-weg` noch aus (Varianten-Check und Gegenleser).

**Anmerkung des Scouts (keine Entscheidung):** die Empfehlung oben steht unverändert. Research hat keine der Fragen entschieden, also bleibt die gemeinsame Prämissen-Tafel der erste Rechenschritt, nicht neun Jobs. Wo Research etwas verschoben hat, dann nach unten: alle vier Short-Skelette (W15b, W7b, W27b, W38b) haben jetzt einen dokumentierten Gegner (asymmetrische Gold-Reaktion, Zentralbank-Käufe), W38 hat einen Gegenhinweis auf der ersten Stufe (ZN negativ serienkorreliert), W27 verliert die Stütze „ZN-Sprung ist ein etabliertes Überraschungsmaß“ außerhalb von FOMC. Das liegt innerhalb der Unschärfe der Chancen-Schätzung, die Zahlen in der Signalgeber-Tabelle bleiben.

**Im JSON:** je Skelett `research_status`, `research_date`, `research_evidence`, `research_sources`, `research_open`. `why_status` bleibt `entwurf` (das Feld kennt nur `entwurf` und `belegt`, „offen“ steht in `research_status`).

---

## Modul-Specs

| Spec | Was fehlt | Wo | Umfang |
|---|---|---|---|
| **S-GCX-1** | Fremdmarkt-Bestätigung mit eigenem Session-Fenster: `xref_signal` lädt das Fremdsymbol mit derselben Verschiebung, `xref_confirm` auch in `tsmom.trades` (dort trennt `tm_dir` Long und Short), **zweites Symbol** (für W15 wie beschrieben und W40 Pflicht) | `sigcore.py` 862 bis 950, `tsmom.py`, `controls.py` | rund 35 Zeilen |
| **S-GCX-2** | Signal aus dem Fremdmarkt: `tm_signal="xret"` (Fensterrendite von `tm_xsig_sym` mal Vorzeichen, normiert, Fremd-Bars nur bis zur letzten vollständigen Bar vor dem Einstieg). `tm_null` bleibt wirksam, kein neuer Modus | `tsmom.py` (`_signal`, `trades`), `controls.py` (`ctl_symbols`) | rund 50 Zeilen |
| **S-GCX-3** | Datentag-Tor: `tm_news_only` oder Volumen-Ereignis, dazu `news_calendar` für GC lauffähig machen (#180 Lehre 6) | `sigcore.gates_pass`, `news_calendar.py` | rund 15 Zeilen |
| **S-GCX-4** | Fremdmarkt-Tagesrendite als Tor (`x_ret1`, `x_ret5`), ersetzt FRED im Live-Betrieb | `tsmom.py` 317 bis 340, `sigcore.gates_pass`, `controls.py` | rund 10 Zeilen |
| **S-GCX-6** | Kopplungs-Zustand als Tagesreihe (Korrelation GC zu ZN/6E und Vorzeichen GC zu NQ), nur skizziert, erst nach Feasibility | `sigcore._spx_daily_context` | rund 30 Zeilen |
| **S-GCX-7** | Kurven-Tor: `curve_prev` und `curve_chg5` (DGS10 minus DGS2) im Makro-Tageskontext, Tor-Paare `tm_curve_*` | `sigcore.py` 961 bis 985 und 1259 bis 1264, `controls.py` | rund 8 Zeilen |
| **S-GCX-8** | Fremdmarkt-Level: `tm_signal="xlevel"`, Signalwert +1 oder −1, wenn der Fremdmarkt am Fensterende seit mindestens `tm_xlvl_hold` Minuten jenseits seines Vortageshochs bzw. -tiefs oder der Nacht-Range schließt. Baut auf dem Fremd-Bar-Laden aus S-GCX-2 auf | `tsmom.py` | rund 25 Zeilen zusätzlich |
| **D-GCX-1** | Daten auffrischen: FRED-Reihen, VIX, NT8-Nachladen GC (endet 24.07.2026), CL, 6E, 6B, ZN, ZB | AP196 | Handarbeit Max in NT8 |
| **D-GCX-2** | SI nachladen (Anhängsel HG, 6J, PL), DFII10 und T10YIE von FRED. Zweite Quelle: Databento (AP143) | NT8, FRED | Handarbeit plus 2 CSV |
| **D-GCX-3** | Shanghai-Prämie und GLD-Bestände: Quelle erst über Research | offen | offen |
| **D-GCX-4** | Treasury-Auktionskalender (auch Blocker für KF-44 und SZ-14) | offen | offen |

Die Nummer S-GCX-5 ist nicht vergeben. Nach jeder Engine-Änderung: `engine-regression-tester`, alle Buch-Beine bitgleich, dann Runner neu starten.

---

## Offene Research-Fragen (für `research-scout`)

**Stand 13.10.2026:** die Fragen 1 bis 6, 11 und 12 hat der `research-scout` bearbeitet (Cache Z. 2083 ff.). Keine ist beantwortet, alle bleiben offen. Die übrigen sind unbearbeitet.

1. **W15:** Trennt die Literatur Gold-Impulse in makro-bestätigte (gleichzeitige Sprünge in Treasuries und Dollar) und gold-eigene, mit Fortsetzung gegen Umkehr über 30 bis 300 Minuten? **13.10.: gesucht, nichts gefunden.** Co-Jump-Literatur (Lahaye/Laurent/Neely) ordnet nur Ankündigungen zu.
2. **W15, W1, W4:** Wie lange braucht GC, um eine ZN- oder 6E-Bewegung einzupreisen (Preisfindung, Informationsanteile, Halbwertszeit)? **13.10.: Negativbefund**, keine Studie zu Lead-Lag oder Preisfindung Gold gegen Treasury- bzw. Dollar-Futures auf Minutenbasis (3 Suchläufe, keine Datenbanksuche, Information-Share-Stichworte nicht gezielt geprüft).
3. **W27:** Gibt es eine verzögerte Anpassung von Gold an die Treasury-Reaktion nach US-Makrodaten über 90 Sekunden hinaus? Taugt die Größe des ZN-Sprungs als Ersatz für die Überraschung gegen Konsens? Sobti (EFMA 2024) im Volltext zu Co-Jumps. **13.10.: offen.** Verzögerung nur für FOMC belegt (Awartani 2024), ZN-Sprung als Maß nur für FOMC etabliert (Gürkaynak/Sack/Swanson 2005), Sobti-Volltext nicht lesbar.
4. **W27b, W15b:** Richtung der Asymmetrie der Gold-Reaktion seit 2020 (die Studien im Cache widersprechen sich). **13.10.: offen, Tendenz gegen Short** (Awartani 2024, J.P. Morgan 2026: stärkere Reaktion bei Lockerung bzw. fallenden Renditen), Widerspruch zu Cache Z. 1373 nicht aufgelöst.
5. **W7, W31:** Sagen Bond- oder Dollar-Renditen der letzten 1 bis 5 Tage die Gold-Rendite des Folgetags voraus, und in welcher Session fällt die Drift an? **13.10.: gesucht, nichts gefunden** (nur Granger Dollar → Gold nach Rezessionen, Abstract).
6. **W22:** Intraday-Belege für Flucht-in-Sicherheit-Episoden mit Gold, und hält der Effekt nach 2020? **13.10.: offen.** Intraday-Beleg nur für COVID Phase I (Akhtaruzzaman et al. 2021), Fortsetzung nach der ersten Stunde nirgends.
7. **W8, W24, W32:** Wer führt zwischen Gold und Silber intraday, ist das Ratio kointegriert, welche Halbwertszeit?
8. **W30, W41:** Datenquelle für die Shanghai-Prämie ab 2016 (täglich). Wei 2026 im Volltext (Sessiongrenzen). Ma, Bouri, Xu, Zhou 2025 („night effect“) steht im Cache als ungelesen.
9. **W33:** Sagen GLD-Zuflüsse die Folgetags-Rendite voraus?
10. **W29:** Reaktion von Gold auf Treasury-Auktionen (im Cache nur ZN, Smales 2021), und eine Quelle für den Auktionskalender.
11. **W38:** Laufen Ausbrüche von Treasury- und Devisen-Futures über Vortageshoch und -tief intraday weiter (Intraday-Momentum in Zins- und FX-Futures)? Reagiert Gold darauf gleichzeitig oder verzögert? **13.10.: offen mit Gegenhinweis.** Kein Paper zur Ausbruch-Fortsetzung, Cusatis et al. 2009 finden ZN intraday negativ serienkorreliert.
12. **W40:** Welcher Kanal dominiert den Goldpreis, wenn Zins und Dollar in entgegengesetzte Richtungen zeigen (Zerlegung der Gold-Rendite in Realzins- und Dollar-Anteil auf Intraday-Ebene)? **13.10.: offen**, Kanal-Dominanz regimeabhängig, keine Studie zum Gegensatz-Fall.
13. **W43:** Hängt die Gold-Rendite davon ab, welches Kurven-Ende sich bewegt (2Y gegen 10Y)? Hinweis im Cache vom 13.10. (nicht gezielt gesucht): StoneX, Gold reagiere früher auf das kurze Ende (Praktiker, nur Titel und Suchzusammenfassung gelesen).
14. **W45:** Gibt es einen belegten Effekt des WMR-Fix oder des Monatsende-Dollar-Rebalancings auf Gold?
15. **W44:** Sagen Öl oder Inflationserwartung (Breakevens) die Gold-Rendite über Tage bis Wochen voraus?

**Betriebsfrage, kein Research:** Liefern FN und FFN Echtzeit-Kurse für ZN und 6E auf dem Konto-Feed? Bei E8 ist ZN handelbar, dort nur einmal am Konto nachsehen.

---

## Nachtrag 13.10.2026: was der `verdict-auditor` gefunden hat

**Neue Wege (10):** W36 Exit, W37 Sizing, W38 und W39 Fremdmarkt am eigenen Level, W40 Widerspruch der Signalgeber, W41 US-Nachmittag → Asien, W42 Fremdmarkt-Trendstärke, W43 Zinskurve, W44 Öl und Inflationserwartung (Swing), W45 Dollar-Zwangsfluss. Neue Skelette nur für W38 (long und short). Dazu als Achse ohne eigene Nummer: Kopplungs-Vorzeichen GC zu NQ (W21).

**Korrigierte Stände:**
1. W1 bis W3: nicht „gemessen ohne Kandidat“ für 1 bis 5 Minuten, sondern 5-Minuten-Versatz null und Lags 1 bis 4 Minuten nie gemessen.
2. Randbedingung 7: GC endet am 24.07.2026, nicht am 26.08. (das ist VIX).
3. Randbedingung 11: ZN ist bei E8 handelbar.
4. W7: Frequenz-Vorbehalt ergänzt, die Behauptung „Zählung stützt die Short-Seite“ gestrichen.
5. W15: „sofort“ gilt nur abgespeckt, der Weg wie beschrieben ist Modul-Spec. XD-12 scheiterte am Buch.
6. `mak01_macrogate_pb3_NQ`: 9 Trials, 6 Survivors, offener Fall, kein Toter.
7. Verwandte getrennt in tot, gemessen ohne Urteil, unentscheidbar, lebend.
8. Randbedingung 1: TD-12 auf GC (#180c) als einziger Träger mit belegter Information ergänzt.

**Wo der Scout dem Auditor nicht ganz folgt:** beim Frequenz-Überschlag zu W7. Die 7 bis 8 Trades im Jahr gelten mit der Impuls-Schwelle aus #174, die das Skelett nicht vorschreibt. Ohne Schwelle sind es grob 60. Beides ist ein Überschlag, deshalb steht die Zählung jetzt als Pflicht vor dem Job und das Skelett unter Vorbehalt. Details im Report, Abschnitt 8.

**Warum die Chancen gleich bleiben:** was die Korrekturen heben (ungemessene Lags, XD-12 scheiterte nicht an der Mechanik, TD-12 als Träger) und was sie senken (W15 nur abgespeckt rechenbar, W7 an der Frequenz-Latte, Gold-Daten zwei Monate kürzer), liegt beides innerhalb der Unschärfe einer Schätzung.

---

## Verwandte Notizen

- [[Hypothesen-Bank (Gold & Sessions)]] (GC-RV-01, GC-NEWS-01, GC-ON-01, Kostentabelle)
- [[Hypothesen-Bank (Volumen & Flows)]] (XA-28, XA-32, KF-44, KF-61, SZ-14)
- [[Neue Märkte (NT8-Daten) Plan]] (Daten, Kostenquoten, #165)
- [[Strategie-Logbuch]] #033, #087, #090, #139, #141, #163, #165, #171, #174, #180, #181
- [[Friedhof-Nachlauf Gate v4 (01.10.2026)]] (XD-12 als Zusatzbein)
- [[Alpha-Scout AP194 (22.09.2026)]] (Zählung GCZINS-01, MAKRO-01)
- [[Alpha-Scout Queue-Nachschub (10.10.2026)]]
- [[ES-NQ-Divergenz Wege-Karte]] (Herkunft von `tm_xref_sym`, XD-12)
- [[ADX Wege-Karte]] (Herkunft von `tm_xadx_sym`)
- [[Research-Cache]] (Abschnitte Gold vom 22.09. und 24.09.2026, Abschnitt Gold Cross-Asset vom 13.10.2026 ab Z. 2083, E8-Instrumentenliste Z. 793)
- [[Firm-Regeln je Konto]], [[Discovery-Runner v2]], [[Familien-Scout Agent]], [[VWAP-Offensive]]
- Report: `engine/discovery/scout_reports/familien_gold-cross-asset_261013.md`
- Skelette: `engine/discovery/jobs_proposed/familien_gold-cross-asset_261013.json`
