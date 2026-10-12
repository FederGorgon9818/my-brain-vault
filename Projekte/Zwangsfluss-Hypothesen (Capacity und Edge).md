---
tags: [projekt, alpha-suche, research, hypothesen, zwangsfluss]
erstellt: 2026-10-12
status: Recherche fertig, nichts gerechnet, Entscheidung Max offen
---

# Zwangsfluss-Hypothesen (Capacity und Edge)

> Auftrag Max, 12.10.2026: zu jedem Mechanismus aus der Recherche „Lower Capacity, Higher Edge“ fünf Research Papers finden, die Hypothese daran prüfen und alles als Detail in die jeweilige Hypothese schreiben (wie es funktioniert, was getestet wurde).
> Gehört zu [[Alpha-Suche]]. Quellen zusätzlich im [[Research-Cache]] (Abschnitte „Capacity und Edge“ und „Zwangsfluss-Hypothesen, Paper-Lauf“, beide 12.10.2026). Eigene Vorarbeit im [[Strategie-Logbuch]]: #111, #163, #180, #028, #141.

## Worum es geht

**Ausgangsthese:** je weniger Geld in eine Strategie passt, desto höher die Edge. Das ist so allgemein nicht belegt. Belegt ist nur, dass große Fonds zu festen Terminen handeln müssen und wir nicht.

**Die Hypothese, die wir daraus prüfen:**
Edge liegt für uns dort, wo ein vorhersagbarer institutioneller Zwangsfluss in einem kurzen Fenster läuft und der Gewinn je Trade groß genug ist, um die Micro-Kosten zu tragen (MNQ rund 3,8 Ticks Round-Turn, das sind etwa 0,5 bp).

## Wichtig vorab (ehrlich)

- **Kein Mechanismus ist voll bestätigt.** Fünf sind „teilweise bestätigt“, einer (Roll) ist für unseren Fall nicht bestätigt.
- **Kein einziger Volltext wurde gelesen.** Alle Zahlen stammen aus Abstracts, Suchsnippets oder Sekundärquellen. Vor einem Test, der an einer Zahl hängt, das Paper selbst lesen (`/paper-edge`).
- **Fünf echte Papers je Mechanismus gab es nicht überall.** Beim Rebalancing (A) sind es nur zwei direkte. Es wurde nichts aufgefüllt.
- **Fast alles ist Tagesdaten und Aktien.** Intraday-Auflösung auf Futures fehlt in der Literatur fast durchgehend. Die Übertragung auf uns ist jeweils die eigentliche Hypothese.
- **Kosten sind fast nie das Problem, die Fallzahl ist es.** Die meisten Effekte liegen bei 10 bis 20 bp, die Kosten bei 0,5 bp, aber es gibt nur 40 bis 120 Ereignisse in zehn Jahren.
- Gerechnet wurde nichts, kein Trial verbraucht. Alle Power-Angaben unten sind Überschläge der Recherche, keine Messung.

## Übersicht

| # | Mechanismus | Beleglage | Für uns handelbar (intraday flat)? | Ereignisse in 10 Jahren | Größte Hürde |
|---|---|---|---|---|---|
| A | Quartals-/Monatsende-Rebalancing | teilweise (1 direktes Paper dafür, 1 dagegen) | unklar, Effekt ist Close zu Close gemessen | 120 Monate, 40 Quartale | Power (t rund 1,3) |
| B | Monatsende-Liquiditätsbedarf und Turn-of-the-Month | teilweise, neueste Quellen sagen „weg“ | unklar, Kernfrage Nacht gegen Tag | rund 500 Tage, effektiv 120 Monatswechsel | Verfall nach 2001 |
| C | Gehebelte ETFs und Dealer-Gamma am Close | teilweise, LETF-Anteil schrumpft | ja | 100 bis 250 große Tage | Zusatz zum LastHour-Bein kaum nachweisbar |
| D | Roll-Zwang | nicht bestätigt für uns | nein (Effekt liegt im Spread) | 40 Rollwochen ES/NQ | kein Paper, kein Outright-Effekt |
| E | Event-Fenster (FOMC, NFP, EIA, Gold-Fix, Auktionen) | teilweise, Pre-FOMC seit 2016 nicht mehr signifikant | teils, Regelrisiko News-Handel | 80 FOMC, rund 360 mit NFP/ISM/GDP | Rauschen, Konsensdaten fehlen |
| F | Nacht-Drift Europa-Fenster | teilweise, seit 2021 laut Autoren nahe null | ja (Globex-Nacht erlaubt) | 2.500 Nächte, davon 1.245 seit 2021 | Effekt aktuell weg, Proxy für Imbalance nötig |

---

## A: Quartals- und Monatsende-Rebalancing

### Wie es funktioniert
Pensions-, Misch- und Target-Date-Fonds haben feste Zielgewichte, grob 60 Prozent Aktien und 40 Prozent Anleihen. Laufen Aktien in einem Monat oder Quartal besser als Anleihen, sind sie übergewichtet und müssen Aktien verkaufen und Anleihen kaufen. Nach schwachen Aktienmonaten läuft es umgekehrt. Ausgelöst wird das über den Kalender (Monats- und Quartalsende) oder über Schwellen, gehandelt wird über Kasse oder Futures. Erwartete Richtung: nach starkem Aktienmonat Druck nach unten, nach schwachem nach oben. Eine Uhrzeit nennt die Literatur nicht.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Harvey/Mazzoleni/Melone 2025, „The Unintended Consequences of Rebalancing“, [NBER w33554](https://www.nber.org/papers/w33554) | Marktdaten 1997 bis 2023, täglich, zwei Signale (Schwelle, Kalender), Rendite am Folgetag | +1 Standardabweichung Signal: rund −16 bis −17 bp Aktien am nächsten Handelstag, +2 bis +4 bp Anleihen. Bildet sich in etwa 2 Wochen zurück. Brutto, Working Paper | stützt |
| Bikker/Broeders/de Dreu 2010, [IJCB 6(2)](https://www.ijcb.org/journal/ijcb10q2a3.htm) | niederländische Pensionsfonds, quartalsweise | nur rund 39 % der Aktien-Überrendite werden je Quartal zurückgebaut, nach Verlusten stärker als nach Gewinnen, größte Fonds laufen sogar mit dem Trend | schwächt (der Fluss ist kleiner und unzuverlässiger als die Story annimmt) |
| Hartzmark/Solomon 2022, „Predictable Price Pressure“, [NBER w30688](https://ideas.repec.org/p/nbr/nberwo/30688.html) | USA und international, täglich, Dividenden-Reinvestition | vorhersagbare Flüsse ohne Information bewegen Preise, oberstes Quintil etwa 4-mal das unterste | stützt nur das Prinzip, kein Rebalancing-Test |
| Rattray/Granger/Harvey/Van Hemert 2020, „Strategic Rebalancing“, [JPM 46(6)](https://doi.org/10.3905/jpm.2020.1.150) | 60/40-Portfolios | mechanisches Rebalancing existiert und kostet in Krisen | neutral, kein Preisdruck-Test, nicht als Beleg zählen |

**Nur zwei direkte Papers, ein fünftes echtes wurde nicht gefunden.** Broker-Schätzungen (Goldman, BofA) sind Modellzahlen und zählen nicht.

### Was bei uns schon getestet ist
#163 hat nur die Variante mit Monatsrendite in Terzilen gerechnet. Urteil inhaltlich **unentscheidbar** (kleinster auflösbarer Effekt 0,26 bis 0,88 ATR20 gegen Kill-Schwelle 0,15, 127 Monats-Episoden), der Titel „endgültig tot“ passt nicht dazu. Nicht getestet: Intraday-Auflösung, Quartalsende mit stetigem Signal nach Harvey, Anleihen-Seite.

### Was die Literatur nicht testet
Uhrzeit am Stichtag, Futures statt Kasse, Zeitraum nach 2023, Kosten. Seit der Veröffentlichung 2025 könnten Vorläufer den Effekt schon abgegriffen haben.

### Skelett für einen Test
- Markt: MNQ, MES, optional M2K.
- Signal: Aktien-Überrendite des laufenden Monats oder Quartals gegen Anleihen (ZN, falls Daten da sind), stetig statt Terzil.
- Richtung: gegen die Überrendite.
- Einstieg am letzten Handelstag ab 15:30 ET oder am Folgetag zur Eröffnung, Ausstieg am selben Tag.
- Fallzahl: 120 Monatsenden, 40 Quartalsenden.
- Power: bei 130 bp Tagesvola und 120 Fällen liegt ein Effekt von 16 bp bei t rund 1,3.

### Was die Hypothese beerdigt
Kein Effekt von mindestens rund 8 bp im Tagesanteil am Stichtag und Folgetag. Oder der Effekt liegt komplett in der Nacht, dann ist er auf Prop-Konten nicht handelbar. Reicht die Power wieder nicht, ist es erneut unentscheidbar und kein Todesurteil.

**Stand der Hypothese: teilweise bestätigt, für uns voraussichtlich nicht entscheidbar.**

---

## B: Monatsende-Liquiditätsbedarf („Dash for Cash“) und Turn-of-the-Month

### Wie es funktioniert
Fonds und Pensionskassen müssen zum Monatsende Renten, Gehälter und Rücknahmen auszahlen. Weil ein Aktienverkauf erst nach der Abwicklungsfrist Geld bringt, verkaufen sie einige Tage vorher, früher etwa drei Tage vor Ultimo. Das drückt die Kurse, danach kommt die Erholung. Verwandt ist der Turn-of-the-Month-Effekt: die Marktrendite fiel historisch fast ganz auf den letzten und die ersten drei Handelstage des Monats.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Etula/Rinne/Suominen/Vaittinen 2020, „Dash for Cash“, [RFS 33(1)](https://academic.oup.com/rfs/article/33/1/75/5494694) | US-Aktien und Index, international, täglich | Reversal um T−3, Long-Short 5,6 % p.a. Überrendite, auch auf Indexebene sichtbar (Arbeitsversion). Brutto | stützt |
| McConnell/Xu 2008, [SSRN 1135217](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1135217) | CRSP 1926 bis 2005, 31 von 35 Ländern | 0,15 % je Tag im 4-Tage-Fenster gegen etwa null an den übrigen Tagen. Brutto | stützt (bis 2005) |
| Ogden 1990, [J. Finance 45(4)](https://ideas.repec.org/a/bla/jfinan/v45y1990i4p1259-72.html) | Indexrenditen 1969 bis 1986 | Zahlungsrhythmus am Monatswechsel erzeugt den Liquiditätsschub | stützt die Mechanik, alt |
| Maberly/Waggoner 2000, [Atlanta Fed WP 2000-11](https://www.atlantafed.org/research/publications/wp/2000/11.aspx) | S&P-500-Futures und Kasse | Effekt verschwindet in den Futures nach 1990 | schwächt, einziges Futures-Paper |
| Han/Han/Tian 2025, „The disappearing turn-of-month effect“, [FRL 71](https://ideas.repec.org/a/eee/finlet/v71y2025ics1544612324014909.html) | Indexebene | Effekt nach 2001 vollständig weg, vermutete Ursache niedrigere Handelskosten | schwächt, jüngste Quelle |

Zusätzlich, nicht mitgezählt: Graziani 2024 (Working Paper, Monatsende-Rendite sagt Folgemonat negativ voraus, laut Abstract robust nach Kosten, Zahlen nicht gelesen) und Choi/Hong/Lou/Mukherjee (Entwurf zu 401(k)-Zuflüssen, Ergebnisse nicht gelesen).

**Offener Widerspruch:** Etula sagt, die Reversals seien über die Zeit stärker geworden, Han sagt, der Effekt sei seit 2001 weg. Unterschiedliche Messung (Querschnitt gegen Index), nicht aufgelöst.

### Abwicklungsfrist T+1
Es gibt **keine Studie**, die das Timing nach der Umstellung prüft. „T−3 wandert auf T−1“ ist reine Ableitung aus der Mechanik. Unsere Daten 2016 bis 2026 enthalten drei Regime: T+3 bis 04.09.2017 (rund 20 Monatsenden), T+2 bis 27.05.2024 (rund 80), T+1 seitdem (rund 28). Das wäre ein natürliches Experiment, aber mit sehr kleinen Teilmengen.

### Was bei uns schon getestet ist
#163 (siehe A) und laut Cache #034. Auffällig aus #163: der unbedingte Effekt lag bei +0,29 ATR20 über 5 Tage mit gleichem Vorzeichen in NQ, ES, RTY und YM.

### Was die Literatur nicht testet
Die Kernfrage für uns: liegt der Gewinn im Tagesanteil oder in der Nacht? Dazu gibt es keine Quelle. Ebenso fehlen Futures nach 2000 und Ergebnisse nach Kosten.

### Skelett für einen Test
- Markt: NQ, ES, RTY, YM.
- Variante 1: Long von Eröffnung bis Schluss an T−1 bis T+3.
- Variante 2: Reversal-Timing, Druckphase T−6 bis T−3 meiden oder short, danach long.
- Immer abends flat.
- Fallzahl: rund 500 Handelstage in zehn Jahren, wegen der hohen Korrelation der Indizes effektiv etwa 120 Monatswechsel.
- Power: 15 bp je Tag bei 480 Tagen ergäbe t rund 2,4, aber nur wenn der volle Effekt am Tag liegt und nicht verfallen ist.

### Was die Hypothese beerdigt
Der Tagesanteil im Fenster liegt nicht über den übrigen Tagen (unter rund 3 bp je Tag), der Effekt liegt ganz in der Nacht, oder das Vorzeichen kippt zwischen den Indizes.

**Stand der Hypothese: teilweise bestätigt, mit ernstem Gegenbefund. Von allen sechs hat dieser Test die beste Fallzahl.**

---

## C: Gehebelte ETFs und Dealer-Gamma am Handelsschluss

### Wie es funktioniert
Gehebelte und inverse ETFs müssen ihr Engagement jeden Tag auf das feste Vielfache zurückstellen. Nach einem Anstieg kaufen die Bull-Fonds dazu und die inversen decken Shorts ein, also kaufen beide. Nach einem Fall verkaufen beide. Der Bedarf wächst linear mit der Tagesrendite **seit dem Vortagesschluss** und fällt ins letzte Handelsfenster. Händler, die Optionen verkauft haben und short Gamma sind, sichern in dieselbe Richtung ab. Unterschied: Options-Hedger können den Zeitpunkt wählen, der ETF-Fluss ist streng vorhersagbar.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Cheng/Madhavan 2009, [JOIM 7(4)](https://joim.com/dynamics-leveraged-inverse-exchange-traded-funds) | US-ETFs 2008 | Bedarf bis 16,8 % des Schlussvolumens an einem 1-%-Tag, 50,2 % bei 5 % | stützt die Mechanik |
| Tuzun 2013, [Fed FEDS 2013-48](https://www.federalreserve.gov/pubs/feds/2013/201348/index.html) | US-ETFs, 2008/09 und 2011 | 1 % Indexplus löst rund 1,04 Mrd. $ Rebalancing aus | stützt, vorsichtig |
| Shum/Hejazi/Haryanto/Rodier 2012 | 346 Large Caps, 2006 bis 2011, Einstieg 14:45 in Flussrichtung | rund ein Drittel der Spät-Vola, 0,60 % je Trade brutto | stützt, alt |
| Ivanov/Lenkey 2018, [JFM 41](https://ideas.repec.org/a/eee/finmar/v41y2018icp36-56.html) | US-Aktien-ETFs 2006 bis 2014, mit Kapitalflüssen als Kontrolle | Zuflüsse heben den Bedarf weitgehend auf, Effekt ökonomisch unbedeutend | schwächt |
| Lenkey 2024, Literatur-Überblick, [QFE](https://www.aimspress.com/article/doi/10.3934/QFE.2024031) | Überblick | Zusammenhang durchgängig signifikant, aber klein, viele Papers methodisch angreifbar | schwächt |
| Barbon/Beckmeyer/Buraschi/Moerke 2022, [SSRN 3925725](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3925725) | US-Einzelaktien | ETF-Effekt nimmt über die Zeit signifikant ab, Gamma-Effekt bleibt | stützt Gamma, schwächt ETF-Anteil |
| Baltussen/Da/Lammers/Martens 2021, [JFE](https://www3.nd.edu/~zda/intramom.pdf) | über 60 Futures, 1974 bis 2020 | Rest des Tages sagt die letzten 30 Minuten voraus | stützt |

Praktiker-Zahl, nicht als Paper gezählt: Credit Suisse 2015, ETF-Rebalancing über 2 % des Volumens der letzten 30 Minuten (2011 noch rund 3 %).

### Was bei uns schon getestet ist
Das Bein NQ_LastHour läuft live. #111 hat darauf Schwelle auf den Morgenmove, Perzentil, VIX, Volumen, Makro-Tage und das Zarattini-Band getestet, kein Filter trug (nested +0,9 $ je Trade).

**Nicht in #111 getestet:**
1. Die ETF-Referenz selbst: Rendite **seit Vortagesschluss** (inklusive Gap) statt Eröffnung bis 13:30.
2. Die Höhe dieser Rendite als Stärke (Terzile) statt Schwelle ja oder nein.
3. Später Einstieg 15:30 bis 15:45 ET statt 13:30.
4. Zeitverlauf: schrumpfender ETF-Anteil gegen stabilen Gamma-Anteil.
5. Long-Short-Asymmetrie aus der ETF-Struktur.

### Was die Literatur nicht testet
Den Effekt auf NQ/ES-Futures im Minutenraster, eine Strategie nach Kosten nach 2015, die Größe des ETF-Bedarfs gegen das Futures-Volumen am Schluss.

### Skelett für einen Test
- Markt: MNQ, zum Vergleich MES.
- Richtung: Vorzeichen der Rendite seit Vortagesschluss.
- Bedingung: Betrag dieser Rendite in Terzilen oder ab 1,5 bis 2 %.
- Einstieg 15:30 ET (Varianten 15:00, 15:45), Ausstieg bis 15:55 ET.
- Fallzahl bei großen Tagen: geschätzt 100 bis 250 in zehn Jahren.
- Power: bei 100 Fällen muss der Effekt grob 7 bp erreichen, um t = 2 zu schaffen.

### Was die Hypothese beerdigt
Kein gleichmäßiger Anstieg über die Terzile, netto null im obersten Terzil, kein Zuwachs gegenüber dem bestehenden LastHour-Bein, oder der Effekt ist nach 2018 weg.

**Stand der Hypothese: Mechanik belegt, Preiswirkung umstritten und schrumpfend. Für uns ist es eine neue Variante des bestehenden Beins, kein neuer Mechanismus.**

---

## D: Roll-Zwang

### Wie es funktioniert
Passive Rohstoff-Indizes müssen den vorderen Kontrakt zu bekannten Terminen in den nächsten tauschen (beim S&P GSCI über fünf Tage). Rohstoff-ETFs wie USO rollen ebenfalls angekündigt. Bei ES und NQ wandert das Volumen in der Woche vor dem dritten Freitag im März, Juni, September und Dezember in den nächsten Kontrakt. Der Fluss ist immer „vorne verkaufen, hinten kaufen“, wirkt also zuerst auf den Abstand zwischen den Kontrakten, nicht auf die Richtung.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Mou 2010, „Front-Running the Goldman Roll“, [SSRN 1716841](https://papers.ssrn.com/abstract=1716841) | GSCI-Rohstoffe 2000 bis 03/2010 | Sharpe bis 4,39, Index-Anleger verloren rund 3,6 % p.a. | stützt, alt, unklar ob Spread oder Einzelkontrakt |
| Dubois/Maréchal 2020, [EFMA-Paper](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2020-Dublin/papers/EFMA%202020_stage-1301_question-Full%20Paper_id-418.pdf) | GSCI-Roll | vor 2004 +115 bp im Frontkontrakt, 2004 bis 2010 −60 bp, nach Kosten kein Gewinn | schwächt (Vorzeichenwechsel) |
| Bessembinder/Carrion/Tuttle/Venkataraman 2016, [JFE 121(1)](https://digitalcommons.memphis.edu/facpubs/11609) | USO-Roll in Rohöl | an Rolltagen engere Spreads und mehr Tiefe, kein systematisches Vorlaufen | schwächt |
| Hamilton/Wu 2015, [NBER w19892](https://www.nber.org/papers/w19892) | Agrar und Rohöl | Index-Positionen sagen Frontkontrakt-Renditen nicht voraus, bei Rohöl nur 2007 bis 2009 | schwächt |
| Yan/Irwin/Sanders 2022, [J. Commodity Markets 26](https://ideas.repec.org/a/eee/jocoma/v26y2022ics2405851321000295.html) | 24 Rohstoffe 2004 bis 2019, jährliches Rebalancing | höchstens 72 bp, nach einer Woche weg | klein und vorübergehend |
| Brunetti/Reiffen 2014, [Fed FEDS 2011-57](https://www.federalreserve.gov/pubs/feds/2011/201157/index.html) | CFTC-Daten | der Abstand zwischen den Kontrakten steigt mit dem Index-Anteil | stützt, aber Spread-Effekt |

**Zum ES/NQ-Quartalsroll gibt es kein einziges Paper zum Preiseffekt.** Gefunden wurden nur Arbeiten zur Wahl des Rolldatums (Carchano/Pardo 2009) und zur Spread-Ausführung (Slivka/Qin/Ye).

### Was bei uns schon getestet ist
Nichts. #135 betrifft nur Roll-Müll in den Daten.

### Skelett für einen Test
- Rohstoff-Roll in CL: der belegte Effekt ist ein Spread über mehrere Tage, auf Prop-Konten kaum handelbar. Als Einzelkontrakt nur mit einem Vorzeichen begründbar, das nach 2004 gekippt ist.
- ES/NQ-Rollwochen: 40 Ereignisse in zehn Jahren, kein Literaturbeleg, reine Erkundung mit praktisch null Power.

### Was die Hypothese beerdigt
Kein Unterschied der Tagesrenditen in Rollwochen gegen normale Wochen.

**Stand der Hypothese: für uns nicht bestätigt. Kandidat zum Weglassen, nicht zum Testen.**

---

## E: Event-Fenster mit festem Termin

### Wie es funktioniert
Hier stecken mehrere Mechanismen in einer Zeile:
- **Drift vor Makro-Terminen** (FOMC 14:00 ET, NFP, ISM, GDP): Indizes steigen im Schnitt in den Stunden davor, als Prämie für die erhöhte Unsicherheit. Richtung long.
- **EIA-Rohölbestände, Mittwoch 10:30 ET:** Reaktion auf die Überraschung gegen die Erwartung, Information in Sekunden, Nachlauf bis rund 30 Minuten.
- **Gold-Fix in London:** wer den Auktionsfluss sieht, handelt in den ersten Minuten.
- **Treasury-Auktionen 13:00 ET:** Händler sichern die Zuteilung vorher ab und kaufen danach zurück. Die Wirkung auf Aktienindex-Futures ist nur unsere Annahme.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Lucca/Moench 2015, [J. Finance 70(1)](https://doi.org/10.1111/jofi.12196) | S&P 500, 1994 bis 2011, 24 Stunden vor FOMC | rund 49 bp je FOMC, brutto | stützt (bis 2011) |
| Kurov/Wolfe/Gilbert 2021, [FRL 40](https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/) | S&P-500-Futures 1994 bis 2019 | 49 bp (t rund 4,6), 2011 bis 2015 mit Pressekonferenz 44 bp, **2016 bis 2019 nur 9 bp (t rund 1,3)**, ohne Pressekonferenz nie Drift | schwächt |
| Hu/Pan/Wang/Zhu 2022, [NBER w25817](https://www.nber.org/papers/w25817) | US-Index, vor FOMC, NFP, ISM, GDP | große Renditen in der Nacht davor ohne Zusatzrisiko, auch vor NFP, ISM und GDP | stützt, hängt an der Unsicherheit |
| Kurov/Sancetta/Strasser/Wolfe 2019, [SSRN 2637528](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2637528) | E-mini und 10Y, 30 Minuten vor 08:30-Zahlen | 40 bis 50 % der Bewegung laufen vor der Veröffentlichung | stützt, aber das ist Information, kein Zwangsfluss |
| Caminschi/Heaney 2014, [J. Futures Markets](https://onlinelibrary.wiley.com/doi/10.1002/fut.21636) | GC und GLD um den Londoner Fix | Vorteil in den ersten 4 Minuten für Informierte | stützt, für uns kaum nachbaubar |
| Halova/Kurov/Kucher 2014, [J. Futures Markets 34(10)](https://ideas.repec.org/a/wly/jfutmk/v34y2014i10p911-933.html) | Öl und Gas um EIA | Reaktion sofort und ohne Umkehr | stützt die Reaktion, schwächt Gegenhandel |
| Miao/Ramchander/Wang/Yang 2018, [J. Futures Markets 38(1)](https://ideas.repec.org:443/a/wly/jfutmk/v38y2018i1p38-65.html) | CL um EIA | keine Asymmetrie, Preise bewegen sich schon vorher | stützt Vorlauf, widerspricht Rousse/Sévi |
| Lou/Yan/Zhang 2013, [RFS 26(8)](https://doi.org/10.1093/rfs/hht034) | Treasury-Markt um Auktionen | Kurse fallen vorher und erholen sich, 9 bis 18 bp | neutral, Anleihen, kein Index-Test |

### Was bei uns schon getestet ist
#180: CL-EIA (Fortsetzung und Umkehr ab 10:40, Tagesdrift, 36 Zellen) und GC-COMEX, kein Bein trägt. Pre-FOMC laut Cache schon in #034 für 2021+ ohne Ergebnis.
**Nicht gerechnet:** Drift vor NFP, ISM und GDP, EIA mit Einstieg vor 10:30, der Gold-Fix selbst, Treasury-Auktion auf ES/NQ.

### Was die Literatur nicht testet
Treasury-Auktion auf Aktienindex-Futures (kein Paper), EIA nach Kosten im Minutenraster, Drift vor Makro-Terminen nach 2019.

### Skelett für einen Test
- Long MNQ/MES vor NFP, ISM, GDP und FOMC, Ausstieg vor der Veröffentlichung (kein News-Handel).
- Fallzahl: FOMC 80, alle vier Termine zusammen rund 360 in zehn Jahren.
- Power: bei 80 Fällen sind erst 20 bis 37 bp auflösbar, die Literatur nennt seit 2016 nur 9 bp.
- EIA mit Überraschungsmaß braucht Konsensdaten, die wir nicht haben.
- **Regelrisiko:** alles, was zum Termin selbst ein- oder aussteigt, kann bei E8 und FundedNext unter verbotenen News-Handel fallen. Wortlaut vor einem Test prüfen.

### Was die Hypothese beerdigt
Auf 2016 bis 2026 keine Rendite über dem Vergleich mit Tagen ohne Termin, auch nicht bei hohem VIX.

**Stand der Hypothese: teilweise bestätigt, der bekannteste Teil (Pre-FOMC) ist seit 2016 statistisch weg.**

---

## F: Nacht-Drift im Europa-Fenster

### Wie es funktioniert
Händler, die am US-Schluss einen Verkaufsüberhang aufnehmen mussten, sitzen auf Bestand. Sie geben ihn erst ab, wenn mit der Europa-Eröffnung neue Liquidität kommt. Dadurch steigt der Future zwischen 02:00 und 03:00 ET, am stärksten nach Tagen mit Abverkauf am Schluss und bei hoher Vola. Formel der Autoren: erwartete Nachtrendite = Schluss-Überhang × Renditevarianz ÷ Risikotragfähigkeit der Händler. Fällt einer der drei Faktoren, verschwindet der Effekt.

### Papers

| Paper | Daten und Test | Kernzahl | Urteil |
|---|---|---|---|
| Boyarchenko/Larsen/Whelan 2023, [RFS 36(9)](https://doi.org/10.1093/rfs/hhad020) | E-mini S&P 500, 1998 bis 2018 | 02:00 bis 03:00 ET rund 3,6 % p.a. brutto, Sharpe 1,0; nach stärkstem Verkaufsüberhang 7,5 % p.a. | stützt (brutto) |
| Boyarchenko/Larsen/Whelan 2026, [Liberty Street 01.07.2026](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/) | E-mini 1998 bis 2020 gegen 2021 bis 2025, gleiches Bild in NQ und YM | früher rund 3,7 % p.a., **seit 2021 nahe null**; Streuung des Schluss-Überhangs von 6,5 % auf 2,9 % gefallen | schwächt, einzige Prüfung nach 2021 |
| Bondarenko/Muravyev 2023, [SSRN 3596245](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3596245) | E-mini, 24 Stunden | vier Stunden um die Europa-Eröffnung tragen die ganze Durchschnittsrendite, Sharpe 1,6 | stützt, andere Erklärung (Unsicherheit baut sich ab) |
| Liu/Tse 2017, [SSRN 2921758](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2921758) | Index-ETFs und Futures 1999 bis 2014 | Nacht positiv, Tag negativ | stützt, endet 2014 |
| Cooper/Cliff/Gulen, [SSRN 1004081](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1004081) | Aktien, Index, Futures bis 2006 | Nacht +2,8 bis +4,8 bp, Tag etwa null | stützt, alt |

Die Autoren sagen voraus: weitet sich die Streuung des Schluss-Überhangs wieder, kommt der Drift im selben Fenster zurück. Das ist prüfbar, aber noch nicht geprüft.

### Was bei uns schon getestet ist
Das Asia-Bein (#028, #141) ist ein anderes Fenster. #177 (Nachtsession bei niedriger Vola) wurde in dieser Recherche nicht gelesen. Die Frage „Europa-Fenster mit Überhang-Maß“ ist damit offen.

### Was die Literatur nicht testet
Ob sich der Schluss-Überhang ohne Orderbuch aus Minutenbars schätzen lässt. Mögliche Ersatzmaße: Rendite 15:15 bis 16:00 ET oder Lage im Tagesbereich. Ob die mit dem echten Überhang zusammenhängen, ist nirgends belegt. Eine unabhängige Wiederholung für die Zeit nach 2021 fehlt.

### Skelett für einen Test
- Markt: MNQ, MES.
- Long 02:00 bis 03:00 ET, nur nach Tagen im untersten Drittel des Ersatzmaßes. Vergleich: alle Tage.
- Fallzahl: rund 2.500 Nächte, unterstes Drittel rund 830, seit 2021 rund 415.
- Größe früher rund 1,4 bp je Nacht unbedingt, rund 3 bp im untersten Drittel, gegen 0,5 bp Kosten.
- Erster Schritt wäre nur: bildet das Ersatzmaß das Muster 2016 bis 2020 überhaupt nach?

### Was die Hypothese beerdigt
Das unterste Drittel bringt 2016 bis 2020 nicht mehr als der Rest (dann taugt das Ersatzmaß nicht), oder die Differenz liegt 2021 bis 2026 bei null mit einem Band, das die alte Größe ausschließt.

**Stand der Hypothese: bis 2020 gut belegt und mit Mechanik unterlegt, seit 2021 laut den Autoren selbst weg. Wert als Beobachtungsposten: der Drift soll zurückkommen, wenn die Schluss-Überhänge wieder streuen.**

---

## Einordnung (Claude, kein Urteil)

Nach Beleglage, Fallzahl und Handelbarkeit sortiert:

1. **B, Turn-of-the-Month am Tag.** Beste Fallzahl, eigener Vorbefund mit gleichem Vorzeichen in vier Indizes. Die eine Frage, die niemand beantwortet hat: Tag oder Nacht.
2. **C, Rendite seit Vortagesschluss mit spätem Einstieg.** Sauber aus der Mechanik abgeleitet und in #111 nicht gerechnet. Zählt als Variante des LastHour-Beins, also Ersatz-Vergleich statt Zusatzbein.
3. **F, Europa-Fenster mit Ersatzmaß.** Viele Fälle, aber der Effekt ist aktuell weg. Lohnt nur als billiger Nachbau 2016 bis 2020 und danach als Wiedervorlage.
4. **E, Drift vor NFP, ISM, GDP.** Nicht gerechnet, aber die Power reicht voraussichtlich nicht.
5. **A, Rebalancing.** Voraussichtlich wieder unentscheidbar.
6. **D, Roll.** Weglassen.

**Buch-Lücke für alle sechs:** Stufe null. Es gibt noch keine Prämissen-Tafel, keinen Eintrag in einer Hypothesen-Bank, keinen Job. Nächster Schritt je Hypothese ist `ein-weg` (variant-scout und strategy-auditor), erst danach Rechnen.

## Aufräumarbeiten, die die Recherche nebenbei gefunden hat
- Research-Cache Zeile rund 472: „The disappearing pre-FOMC announcement drift“ ist von Kurov/Wolfe/Gilbert, nicht von Cocoma.
- Research-Cache Zeilen rund 474 und 1349 nennen für Kurov/Sancetta/Strasser/Wolfe unterschiedliche Zahlen (7 von 21 gegen 9 von 20).
- Research-Cache Zeilen rund 801 und 1452 (EIA asymmetrisch, Rousse/Sévi) stehen im Widerspruch zu Miao u.a. 2018.
- Die SSRN-Nummer 7035838 für den verschwundenen Nacht-Drift (Zeilen rund 1770 und 1827) ließ sich nicht bestätigen.
- Logbuch #163 trägt „endgültig tot“ im Titel, ist inhaltlich aber unentscheidbar.
