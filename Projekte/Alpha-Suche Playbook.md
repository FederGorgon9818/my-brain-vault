---
tags: [projekt/trading, alpha-suche, methode]
erstellt: 2026-10-13
status: entschieden (Max 28.10.2026, E1 bis E10), Umsetzung über Tickets AP457 bis AP480
---

# Alpha-Suche Playbook: unabhängige Beine finden, ohne etwas auszugrenzen

[[Alpha-Suche]] · [[Testphase Juli-Modus]] · [[Discovery-Runner v2]] · [[Idee-Generierung (wie Institutionen)]] · [[Strategie-Logbuch]] · [[Hochstuf-Regel je Konto (Entwurf)]] · [[Wochenend-Prüfung 24.10.2026]]

Die Schritt-für-Schritt-Anleitungen aller 110 Wege stehen in [[Alpha-Suche Playbook (Anleitungen)]]. Dort hängen auch die Auflagen aus der Methoden-Prüfung an jeder einzelnen Anleitung. In den Tabellen von Abschnitt 4 führt jede ID direkt zu ihrer Anleitung.

> [!important] Achtung beim Lesen der Anleitungen
> Die Regeln R1 bis R16 in Abschnitt 5 gehen dem Text jeder einzelnen Anleitung vor. Die häufigsten Abweichungen:
> 1. **Buch:** In den Anleitungen steht oft „die fünf Beine“ samt RTY-Gap und „Buch 235 $“. Gemeint ist immer das Buch am Tag des Laufs (R1), heute die 6 NQ-Beine PB3, LastHour_v3, Asia-Dir, OpenDrive, OpEx und LD01.
> 2. **Nichts gefunden:** „empirisch-nichts-gefunden“ gibt es nur, wenn der kleinste nachweisbare Sharpe höchstens 0,55 ist (R7). Auf einem Markt allein ist das nie erfüllt, sonst heißt es „unentscheidbar“.
> 3. **Querzeile:** Sie rechnet immer mit der gemessenen Korrelation zwischen den Märkten (R8), nie als einfache Summe.
> 4. **Kosten-Stress** ist eine Info-Zeile, keine K.o.-Stufe (R7). Kostenzahlen gelten nur aus Abschnitt 1 (Gebühr plus 1 Tick je Seite, in Prozent der Tages-Schwankung).
> 5. **Mindestgröße** ohne Angabe von dir: die Käfig-Schwelle aus Rückfrage 4 in Abschnitt 6.2, gerechnet am Buch vom Lauftag.
> 6. **Grid:** startet, wenn die Tafel des Felds trägt (bestes t ab 1,60). Querzeile und Šidák laufen als Etikett mit (R9).
>
> Drei Anleitungen haben zusätzlich Korrekturen im Text, die in Abschnitt 4.2 stehen (H01, H56, H110).

> [!warning] Stand 27.10.2026: was sich seit der Bestandsaufnahme geändert hat
> Abschnitt 1 bis 3 rechnen mit dem **alten Buch vom 13.10.** (4 NQ-Beine plus RTY-Gap, MNQ-Gebühr 1,02 $, kein fester Zeit-Exit). Seit der Wochenend-Prüfung am 24.10. sieht das echte Buch so aus:
> - **6 Beine, alle NQ:** PB3, LastHour_v3, Asia-Dir, OpenDrive, dazu OpEx (erster Live-Trade frühestens 20.11.) und LD01 Variante A (VIX-Filter, live frühestens 31.10. bzw. 03.11.).
> - **RTY-Gap ist seit 18.10. raus.** Es war im alten Buch das einzige Bein über der Käfig-Schwelle (s 0,65 gegen 0,21, es hob die Passquote; die vier NQ-Beine lagen darunter, Probe im Steckbrief Abschnitt 4). Damit steht das Buch jetzt noch stärker auf einem Markt.
> - **LD01** trägt den Großteil des Pakets vom 24.10. Es ist ein NQ-Bein mit anderer Informationsquelle (VIX-Tageswert als Tor). Es korreliert aber an gemeinsamen Tagen 0,89 mit PB3 (Logbuch, Tabelle der Wochenend-Prüfung). Der Gewinn an Monaten kommt also aus der Tagesauswahl, nicht aus neuer Unabhängigkeit. Zuordnung: H06 (vorhandenes Signal in der Rolle Tagesauswahl), OpEx: H90.
> - **Gebühr 1,90 $** je Hin und Zurück für MNQ (1,78 $ M2K), **Zeit-Exit 15:55 ET zum Close**.
> - **Monate bis 50k laut Wochenend-Prüfung** (Median, 600 Simulationen, 5-Konten-Plan mit RiskGuard-Stopps): echtes 4er-Buch 79,2 ± 1,1, Next-6er 67,0 ± 0,9 (Differenz −12,2 ± 0,9; letzte 3 Jahre 49,9 gegen 41,0). Für das Paket plant der Statistiker −3 bis −8 Monate, Mitte etwa −4. Das ist eine **andere Rechnung** als die 69 Monate in Abschnitt 1 (Regime-Wette 13.10., Gebühr 1,02 $, kein 15:55-Exit, eigene Flotte). Die Basen sind nicht direkt vergleichbar, die Differenz ist keine Verschlechterung des Buchs.
> - **Gate v4 Stufe 2** hat die Prüfung „Was konnte die erste Fassung?“ (trägt ab z 1,28). Ohne Eintrag der ersten Fassung kommt keine Idee ins Wochenende.
> - Die Discovery-Queue ist seit 20.10. leer. Im Juli-Modus hat bei Idee 1 bis 9 keine Prämisse getragen, der Nightrun BTC brachte keinen Kandidaten (#188).
>
> **Für das 6er-Buch neu zu messen** (Ticket T05, nicht in diesem Lauf gerechnet): Einzel-Sharpe je Bein, Buch-Sharpe roh und geschrumpft, Tages-Schwankung des Buchs, Paar-Korrelationen mit und ohne Zeit-Überlapp, Belegung je Stunde und flat Tage, Treiber-Anteil (heute 28,5 %), Schwellen-Tabelle und Monats-Tabelle in Abschnitt 1, Größen-Budget je Konto, Kosten-Tabelle mit 1,90 $, dazu die Nacht-Reihen von ES, YM und RTY gegen das Buch. Bis dahin sind die Zahlen unten Richtwerte vom 13.10. In jeder Tabelle steht deshalb **(13.10.)**.

---

## 0. In fünf Sätzen

1. Der Flaschenhals ist der Sharpe des Buchs, und den hebt nur ein neues Bein mit eigenem Vorteil und kleiner Korrelation zum Buch. Faustregel: Bei frei wählbarem Gewicht hilft ein Bein, wenn sein wahrer Sharpe größer ist als Korrelation mal Buch-Sharpe; mit festem Kontrakt muss er über Buch-Sharpe mal (Korrelation plus halbe relative Größe) liegen, und damit die Passquote im Prop-Käfig nicht fällt, über das Doppelte davon, S_B · (2r + v), unkorreliert in Viertel-Buch-Größe also 0,30 (geschrumpft).
2. Gemessen ist: Ein anderer Markt ist dafür **nicht nötig**, denn zwei NQ-Beine ohne Zeit-Überlapp korrelieren mit −0,13 [−0,26; +0,04] und die NQ-Nacht gegen das Buch mit 0,04 [−0,03; 0,11]. Er reicht aber auch **nicht automatisch**, denn ES am Vormittag korreliert mit dem Buch 0,33. Unabhängigkeit kommt aus anderem Zeitfenster, anderem Markt oder anderer Informationsquelle, und sie wird je Bein gemessen. Deine Folgerung „Gold, 6E, Zinsen, Weizen statt NQ/ES“ stimmt deshalb nur teilweise.
3. Von 2.310 Feldern (21 Marktzeilen mal 110 Herangehensweisen) sind 54 gemessen, unentscheidbar oder im Buch, 51 laufen oder sind geplant, 276 sind sofort testbar, 663 hängen am Werkzeug, 1.137 an Daten und 129 an Kontrakt oder Prop-Liste. Auf der Ebene Weg mal Markt ist kein Feld tot; Tote mit Reichweite gibt es auf Zellebene im Logbuch.
4. Die Suche ertrinkt nicht im Rauschen, wenn jedes Feld dasselbe kleine Budget bekommt: 4 vorab notierte Zellen, dann erst ein kleines Grid, gezählt im Register. Die Regel ist allerdings noch nicht geeicht, und die Eichung gehört vor die erste Welle.
5. Dein Wissen ist im Test fast nie angekommen: Seit August waren 29 von 46 Übergaben Stichwörter, über alle 78 Ideen seit Juli kam von 32 Stichwörtern keines ins Buch, und die ICT-Begriffe haben 0 Notizen. Plausibelster Hebel (nicht gemessen) ist eine Wissens-Inventur plus eine 7-Felder-Vorlage zum Diktieren; geprüft wird das an den nächsten 10 Ideen: Wie viele werden als die gemeinte Zelle gerechnet (heute 12 belegte Verlustfälle)?

> [!info] Acht Wörter, die du brauchst
> - **Feld** = ein Weg auf einem Markt, zum Beispiel H13 auf Gold.
> - **Zelle** = eine fest notierte Variante davon (Fenster, Richtung, Ausstieg). Je Feld gibt es 4 **Kern-Zellen**.
> - **Tafel** = alle 4 Zellen eines Felds in einer Tabelle gerechnet, vor jedem Grid. **Grid** = das kleine Raster an Varianten danach (höchstens 24).
> - **Satzung** = der Zettel, der vor dem Rechnen festlegt, was gerechnet wird und ab wann es zählt. Danach darf nichts mehr dazukommen.
> - **Querzeile** = dieselbe Zelle über alle Märkte zusammengezählt. Sie findet kleine Effekte, die überall ein bisschen tragen.
> - **Käfig-Schwelle** = so gut muss ein Bein sein, damit die Prop-Passquote nicht sinkt.
> - **Power** = wie oft ein echter Effekt dieser Größe den Test besteht.
> - **Placebo** = dasselbe Raster auf Zufallszeiten. Es zeigt, wie oft Rauschen besteht (das ist **p0**, der Fehlalarm).
>
> Dazu: **Šidák** ist die strengere Schwelle, wenn man viele Zellen auf einmal ansieht (bei rund 40 Zellen t ab 3,0). **Prämisse** ist die eine Zelle, die die These eines Jobs zuerst zeigen muss.

---

## 1. Was das Buch braucht: der Steckbrief des fehlenden Beins

Ein Zusatzbein hat drei Zahlen: Sharpe **s** nach Kosten, Korrelation **r** zum Buch, Größe **v** (Schwankung des Beins geteilt durch Schwankung des Buchs). „Geschrumpft“ heißt: Backtest-Sharpe mal 0,58, das ist eine Annahme.

**Drei Schwellen (13.10., Buch geschrumpft S_B = 1,20, roh 2,07):**

| Schwelle | Formel | Bedeutung |
|---|---|---|
| Gewicht frei wählbar | s > r · S_B | irgendein Gewicht hebt den Buch-Sharpe |
| fester Kontrakt hebt Sharpe | s > S_B · (r + v/2), genauer S_B·(√(1+v²+2rv) − 1)/v | 1 Micro dazu macht das Buch besser |
| **Käfig** (Passquote fällt nicht) | **s > S_B · (2r + v)** | doppelt so streng wie die Zeile darüber, das ist die harte Latte für Prop-Konten |

**Schwellen geschrumpft, Sharpe-Schwelle / Käfig-Schwelle (13.10.):**

| r \ v | 0,25 (Viertel-Buch) | 0,5 | 1 (so groß wie das Buch) |
|---|---|---|---|
| 0 | 0,15 / 0,30 | 0,28 / 0,60 | 0,50 / 1,20 |
| 0,2 | 0,38 / 0,78 | 0,49 / 1,08 | 0,66 / 1,68 |
| 0,4 | 0,59 / 1,26 | 0,68 / 1,56 | 0,81 / 2,16 |

Roh (Buch 2,07): alle Werte mal 1,7. Gegenprobe per Simulation (150 Felder, zwei Konten): Das Vorzeichen stimmt in 94 % der Felder mit spürbarer Änderung. Bei Beinen über halber Buch-Größe ist die Formel zu freundlich.

**Was ein Bein in Monaten bis 50k spart (13.10., gesparte Monate, Spanne aus zwei Rechenwegen):**

| Bein | wahrer s 0,5 | s 0,8 | s 1,0 |
|---|---|---|---|
| v 0,25, r 0, geschrumpft (Basis über 120 Monate simuliert, rund 160 hochgerechnet) | 15 bis 16 | 25 bis 27 | 31 bis 33 |
| v 0,5, r 0, geschrumpft | 16 bis 22 | 34 bis 40 | 44 bis 49 |
| v 0,25, r 0,2, geschrumpft | 5 bis 9 | 17 bis 20 | 23 bis 27 |
| v 0,25, r 0, roh (Basis 69 Monate) | 2 bis 3 | 5 bis 6 | 7 bis 8 |

Faustzahl: +0,1 Buch-Sharpe sind rund 17 Monate geschrumpft und 4 Monate roh. Die Unsicherheit wird von der Frage dominiert, welche Welt gilt: 43 Monate (Quartile 34 bis 50, letzte 3 Jahre), 69 (58 bis 82, alle Jahre) oder geschrumpft über 120 (simuliert, 30,5 % der Pfade unter 120), rund 160 hochgerechnet. Der zweite Rechenweg liegt auf ±40 %.

**Was die Breite bringt (ab 1,20, Zahl der Beine für Ziel-Sharpe 1,5 / 2,0 / 2,5):**

| Bein-Sharpe | r 0 | r 0,2 unter allen Beinen |
|---|---|---|
| 0,5 | 4 / 11 / 20 | nie / nie / nie (Decke 1,36) |
| 0,8 | 2 / 4 / 8 | 4 / nie / nie (Decke 1,84) |
| 1,0 | 1 / 3 / 5 | 2 / 13 / nie (Decke 2,25) |

„Decke“ heißt: Hängen alle Beine untereinander mit 0,2 zusammen, kommt das Buch nie über diesen Wert, egal wie viele Beine dazukommen. Dann hilft nur höhere Einzel-Qualität oder echte Unabhängigkeit.

**Was wir suchen, in einem Satz:** ein Bein mit wahrem Sharpe ab 0,8, Korrelation höchstens 0,1, flächig über seine Varianten (geschrumpft 1,20 auf rund 1,4). Oder eine Regel, die auf 3 von 5 Märkten je rund 0,57 trägt. Planzahl für jeden Fund: gezeigter Sharpe mal 0,6 bis 0,85.

**Harte Nebenbedingungen:**
- **Nachweis:** Auf 10,6 Jahren ist ein Einzel-Sharpe unter 0,76 nicht von null trennbar (Formel 2,486 / √Jahre, 80 % Power). Mehr Trades ändern daran nichts, nur mehr Jahre.
- **Größen-Budget** je Konto (wahrer s 0,5, r 0, Tages-Schwankung des neuen Beins mit 1 Kontrakt, gemittelt über alle 162 Buchtage im Jahr): FundedNext 50k 88 $, E8 50k 103 $, E8 150k 135 $, FFN 150k 140 $. Bei r 0,2 nur 44 bis 79 $. Ein Vollkontrakt 6E (500 $), ZS (592 $) oder ZW (521 $) schwankt über einen ganzen Tag stärker als das Budget. Das Budget gilt aber im Schnitt über alle Tage, auch die ohne Trade. Erlaubt sind je Trade etwa Budget mal √(162 / Trades im Jahr), bei 25 Trades im Jahr also 225 bis 355 $. Ob ein Bein dort passt, hängt also von Haltedauer und Häufigkeit ab und wird je Feld in Stufe 0 gerechnet. Ein Urteil über den Markt ist das nicht.
- **Kosten** (Gebühr plus 1 Tick Rutschen je Seite) in % der Tages-Schwankung eines ganzen Handelstags je kleinstem Kontrakt: MNQ 0,4, MGC 0,6, MES/MCL 1,5, 6E 3,7, ZS 5,4, ZW 6,2, M6E 8,4, ZN 12,8. Ein Trade über eine halbe Tages-Schwankung kostet relativ doppelt so viel. Das Rutschen ist außerhalb MNQ nicht gemessen, die Werte sind also eher eine Untergrenze (Ticket T21 misst es). **Das ist kein Urteil über einen Markt.**
- **Horizont:** Halten über den Tagesschluss ist bei E8 und FundedNext verboten (Zwangs-Flat 16:10 ET, Primärquelle E8 01.10. und 10.10., FundedNext-Wissensbasis), bei FFN gilt Flat bis 16:50 ET. Mehrtages-Beine sind damit als Handelsobjekt P (nicht handelbar wegen Flat-Zeit), aber nicht tot. Als Signalquelle (Rückblick über Tage oder Wochen als Filter oder Tagesauswahl für ein Intraday-Bein) bleiben sie offen. Nacht innerhalb des Handelstags ist erlaubt: Entry bei E8 ab 18:15 ET (Mail 12.10.), bei FundedNext ab 18:00 ET. Dass E8 das Halten von 18:15 bis in den Morgen erlaubt, folgt aus der Regel, ist aber nicht wörtlich bestätigt (Frage in Schritt 1).

---

## 2. Woher Unabhängigkeit kommt (gemessen)

| Quelle der Unabhängigkeit | Messung (13.10.) | Lesart |
|---|---|---|
| **anderes Zeitfenster, gleicher Markt** | zwei NQ-Beine ohne Zeit-Überlapp: −0,13 [−0,26; +0,04], 353 Paar-Tage, fast nur Vormittags-Beine gegen LastHour. NQ über Nacht (rohe Position) gegen das Buch: 0,04 [−0,03; 0,11] | trägt für Vormittag gegen Nachmittag. Für die Nacht liegt nur die rohe NQ-Nacht-Position vor. Ob ein Nacht-Bein am selben Tagestyp hängt wie das Buch, ist nicht gemessen. Ein anderes NQ-Fenster ist ein guter Kandidat für Unabhängigkeit, gemessen wird sie je Bein. |
| gleicher Markt, gleiche Zeit, gleiche Richtung | +0,63 [0,51; 0,73] | koppelt stark |
| gleicher Markt, gleiche Zeit, Gegenrichtung | −0,28 [−0,54; +0,06], nur 29 Paar-Tage | unentscheidbar |
| **anderer Markt, Rohbewegung im NQ-Fenster 09:30 bis 14:15 ET** | ES 0,91, YM 0,73, RTY 0,69, CL 0,16, 6E 0,14, ZS 0,08, GC 0,07, ZW 0,02 (±0,03) | Aktienindizes koppeln, die anderen kaum |
| anderer Markt, Strategie-Reihe gegen Buch | ES-Vormittag 0,33 [0,25; 0,39]. 12 Gold-Reihen −0,03 bis +0,16 (10 von 12 nicht von 0 trennbar). Öl 0,02 | ein anderer Markt reicht nicht automatisch |
| **CME-BTC** (#188, 23.10.) | Bein gegen Buch-Summe +0,09 [+0,03; +0,17], Rohrendite gegen NQ 0,48 | Bein fast unabhängig, obwohl die Rohbewegung mitläuft. Die Strategie-Reihe ist die richtige Größe. |
| gleiche Nachricht, anderer Markt | zwei Gold-Reihen rund um 08:30-Daten an gemeinsamen Tagen 0,40 ± 0,14 | Hinweis ohne Beleg. Ein Termin kann Märkte koppeln. |
| Zinsen, 6B, FDAX; ES, YM, RTY über Nacht | **nicht gemessen** | offen (Messung in Welle 0, W0-2) |

**Gemeinsamer Tagestyp:** An Tagen ohne Strecke verlieren zwei Beine zu 69 bis 75 % gemeinsam. Ein gemeinsamer Treiber ist also gemessen, auch ohne Zeit-Überlapp. Für ein Nacht-Bein ist er nicht geprüft.

**Wo das Buch leer ist (13.10.):** Außerhalb von 09:30 bis 16:00 ET war es an 0 von 2.758 Tagen im Markt (17,5 von 23 Handelsstunden leer). An 37 % der Tage ist es ganz flat. An den 50 % der Tage ohne Strecke verliert das Buch im Schnitt 24,9 $ je Sitzung. Ein Treiber (die NQ-Strecke) erklärt 28,5 % [22,9; 34,0] der Tagesergebnisse. 97,4 % der Varianz kommen aus NQ. Mit dem 6er-Buch ist das eher stärker geworden, gemessen ist es aber noch nicht.

**Deine Folgerung „nicht mehr NQ/ES, sondern Gold, 6E, Zinsen, Weizen“: teilweise richtig, und zu eng.**
- **Richtig:** ES (0,91), YM und RTY im selben Fenster bringen per Bauart wenig neue Wette. Gold, 6E, Soja und Weizen bewegen sich im NQ-Fenster fast unabhängig (0,02 bis 0,14). Das gilt aber nur für die Rohbewegung. Ob eine *Strategie* dort unabhängig ist, zeigt erst ihre Reihe (Gold bisher −0,03 bis +0,16).
- **Zu eng:** NQ selbst in anderen Fenstern ist bisher gemessen wenig gekoppelt (ein Paar −0,13 [−0,26; +0,04], NQ-Nacht 0,04 [−0,03; 0,11]). ES, YM und RTY außerhalb des NQ-Fensters sind gar nicht gemessen und damit offen.
- **Nicht entscheidbar:** Zinsen haben keine Messung gegen das Buch. Es gibt sie als Daten (ZN/ZB 1-Minuten-Future bis 18.09.), handeln kann man sie aber auf E8 und FundedNext nicht. Bei FFN ist es unbelegt. Als Signalquelle sind sie trotzdem testbar, sobald die Engine sie rechnen kann (T13).
- **Daraus folgt:** Gesucht wird nicht „anderer Markt“, sondern ein **anderer Platz**, also Markt oder Fenster oder Informationsquelle, mit gemessener Korrelation zum Buch. Der jüngste Beleg dafür ist LD01: NQ, aber ein anderes Signal (VIX-Tageswert als Tor), und es trägt den Großteil des Pakets vom 24.10. Wie schon gesagt, korreliert es an gemeinsamen Tagen aber 0,89 mit PB3. Die Reihenfolge-Regel in Abschnitt 5 vergibt Unabhängigkeit deshalb je Feld, also je Markt **und** Fenster, nach dem, was gemessen ist.

---

## 3. Die Landkarte: was getestet ist und was nie

Stand der Landkarte: Logbuch bis #190. Volle Matrix: Datei `p3_landkarte.md` im Scratch-Ordner (Stand vor diesem Nachtrag, 20 Zeilen); die hier gezeigte Zählung mit allen Nachträgen kommt aus `p6_neu.py` (21 Zeilen mal 110 Wege = 2.310 Felder). Kürzel: **B** im Buch, **G** gemessen ohne Kandidat, **U** unentscheidbar, **L** läuft oder geplant, **T** offen testbar, **W** Werkzeug fehlt, **D** Daten fehlen, **P** Kontrakt oder Prop-Liste. Zusatz **/K**: der kleinste handelbare Kontrakt liegt über dem Größen-Budget (Regel 12 unten).

| Markt | B | G | U | L | T | W | D | P |
|---|---|---|---|---|---|---|---|---|
| NQ | 6 | 13 | 4 | 3 | 35 | 35 | 14 | 0 |
| ES | 0 | 7 | 0 | 3 | 39 | 45 | 16 | 0 |
| YM | 0 | 6 | 0 | 3 | 40 | 45 | 16 | 0 |
| RTY | 0 | 4 | 0 | 3 | 51 | 36 | 16 | 0 |
| GC | 0 | 3 | 4 | 3 | 35 | 46 | 19 | 0 |
| CL | 0 | 1 | 2 | 3 | 36 | 49 | 19 | 0 |
| 6E /K | 0 | 1 | 0 | 3 | 1 | 80 | 25 | 0 |
| ZS /K | 0 | 1 | 0 | 3 | 1 | 80 | 25 | 0 |
| ZW /K | 0 | 1 | 0 | 3 | 1 | 80 | 25 | 0 |
| Krypto (CME-BTC; MET D) | 0 | 1 | 0 | 2 | 37 | 49 | 21 | 0 |
| 6B | 0 | 0 | 0 | 3 | 0 | 82 | 25 | 0 |
| ZN/ZB | 0 | 0 | 0 | 3 | 0 | 18 | 25 | 64 |
| FDAX | 0 | 0 | 0 | 2 | 0 | 18 | 25 | 65 |
| 7 Zeilen ohne Daten (Zins kurz, FX Rest, Metalle Rest, Energie Rest, Agrar Rest, Index Rest, VX), je | 0 | 0 | 0 | 2 | 0 | 0 | 108 | 0 |
| Softs/ICE (KC SB CC CT), auch P: auf keiner Prop-Liste | 0 | 0 | 0 | 0 | 0 | 0 | 110 | 0 |

**Summe:** B 6 · G 38 · U 10 · L 51 · T 276 · W 663 · D 1.137 · P 129 · X 0.

**Was sich gegen die Fassung vom 13.10. geändert hat:** Gold Fremdmarkt (H52 × GC) von L auf U (#184: 8 vorab festgelegte Zellen, 4 schließen die Testrichtung aus, 4 unentscheidbar, nur diese Zellen). Beobachtung zuerst auf Gold (H57 × GC) von W auf U (#189, #190: Gold-H1-Breakouts, unentscheidbar). Rollentausch auf NQ (H06 × NQ) von G auf B (LD01). Neue Zeile Softs, deshalb 2.310 statt 2.200 Felder.

**X kann auf der Ebene Weg mal Markt nicht vorkommen,** weil ein solches Feld zu grob ist, um zu sterben. Tote mit Reichweite stehen auf Zellebene im Logbuch (zum Beispiel #068 ORB-Ausbruch NQ, #188 OR30 BTC mit N = 6, #184 Gold-Fremdmarkt) und werden bei Schritt 2 der Übergabe („genau diese Zelle“) abgezogen. Ein G-Feld heißt deshalb nie „nichts mehr zu holen“.

**Wichtig zu G (38 Felder):** „Gemessen ohne Kandidat“ heißt meistens: wenige Configs (oft eine) auf einem Markt in einem Fenster. Beispiel: Die Probe vom 16.10. auf 6E, ZS und ZW war nur Open-Drift/Momentum 09:30 bis 15:55 ET mit 18 bzw. 8 Configs. 6E brachte 0 Survivors (Walk-Forward 3 von 10 Jahren positiv, außerhalb der Stichprobe −2.366 $), ZS und ZW starben an der Prämisse, deren Zelle aus der Vorzählung vom 10.10. gewählt war. Das Urteil gilt nur für diese Zellen. In der vollen Matrix bekommt jedes G-Feld die Spalten **Reichweite** (Markt, Fenster, N) und **Wiedervorlage-Bedingung** dazu (Ticket T18).

**Zuordnungsregeln, die neu oder geändert sind** (die übrigen stehen in `p3_landkarte.md`):
- **Regel 1, ergänzt:** Zu jeder Marktgruppe gehören auch die Micro- und Mini-Varianten, die Kontraktgröße und Kosten ändern: Agrar MZC, MZW, MZS; Zinsen MTN, MWN; FX 7E, M6A, MCD; Metalle SIL, MHG; Energie QM, MNG; Krypto MBT, MET. Daten dazu gibt es heute keine, Prop-Listen führen die meisten nicht.
- **Regel 12, neu:** Liegt die Tages-Schwankung des kleinsten handelbaren Kontrakts über dem Größen-Budget (88 bis 140 $ bei s 0,5, r 0), bekommt das Feld den Zusatz **/K**: zu groß für den Käfig als Tagesbein, nicht tot. In Stufe 0 wird je Feld die Schwankung je Trade gegen Budget mal √(162 / Trades im Jahr) gerechnet. Wiedervorlage: Micro auf der Prop-Liste oder größeres Konto. Betrifft heute 6E, ZS, ZW (255 offene oder gemessene Felder; Micro-Ag ohne Daten und ohne Prop-Liste).
- **Regel 13, neu:** Wege, deren natürliche Form mehrere Tage hält (H35 Terminkurve als Handelsobjekt, H55 Querschnitt über den Korb, H82 Risikoprämien-Inventur), führen den Vermerk **„Mehrtages-Form: P“**. Die Intraday-Form und die Rolle als Signalquelle bleiben mit ihrem Status offen.

**Warum 6E, ZS und ZW fast nur W haben:** Es fehlen der Klon-Weg in Markt-Uhr, das Durchreichen des Fensters und die Kontrollen ohne die feste Annahme von 390 Minuten (ZS/ZW haben 290 Bars). Das ist ein Bau, kein Urteil über den Markt (Welle 0, Abschnitt 5).

Die Zählung des Registers dahinter (69.587 Trials, 95 % auf den vier Aktienindizes) steht in 7.1.

---

## 4. Die Herangehensweisen im Überblick (alle 110)

Jede Zeile hat eine volle Anleitung in [[Alpha-Suche Playbook (Anleitungen)]]. Zusammenlegungen aus der Methoden-Prüfung stehen in der Spalte „Wann nutzen“. Kein Weg ist gestrichen. Zusammengelegte Wege teilen sich aber einen Trial-Zähler, damit dasselbe Feld nicht doppelt gezählt wird.

### 4.1 Wegweiser: „Ich habe … in der Hand, welcher Weg?“

Jeder der 110 Wege hat hier mindestens einen Eingang.

| Ich habe … | Weg (ID) |
|---|---|
| einen Satz „wenn X, dann Y“ aus dem Chart | H57, bei Begriff ohne Formel H60, bei Tagen ohne Satz H61 |
| einen ICT-Begriff oder einen Stop-/Sweep-Gedanken | H60, H100 |
| meinen ganzen Kopf voller Wissen, aber nichts aufgeschrieben | H58, dann H59 (alte Screenshots), H62 (eigene Trades) |
| ein Gefühl, das ich nicht in Worte bekomme | H64 (Blind-Replay), H65 (Vorhersage-Tagebuch) |
| eine fertige Regel (Paper, Praktiker, eigenes Bein) | H01 (Transfer in Markt-Uhr), H69 (gleicher Zähler wie H01), H76 (1:1 nachbauen), H93 (Paper) |
| eine Methode aus Kurs, Buch oder Video | H75, H76, H77 |
| eine Daumenregel „das weiß doch jeder“ | H77, H71 (Erklär-Probe) |
| ein eigenes Bein und will wissen, warum es verdient | H03, H04, H68 |
| ein eigenes Bein, das ich erweitern oder ersetzen will | H02 (gleiche Bau-Eigenschaft woanders), H05 (die liegengelassenen Tage), H07 (Buch als Signal), H10 (Ersatz), H11 (Pfad der Trades) |
| ein vorhandenes Signal in anderer Rolle, Kombination, Bündel | H06, H08, H09 |
| wiederkehrende eigene Verluste oder Handwerksregeln | H63, H67 |
| eine Zahl über das Buch (Lücke, Verlusttag, Treiber) | H12 (Varianten Zeit H13, Treiber H14, Platz H17), H15, H19, Machbarkeit immer über H16 |
| einen Pool fertiger Reihen oder Kandidaten | H18 |
| Kandidaten, die an einer Stufe hängen, oder ungemessenen Bestand | H30, H31, H32 |
| auffällige Tage im Ergebnis, aber keine Ursache | H22, H26 |
| einen Markt, über den ich nichts weiß | H50, H21, H44, H66 |
| einen Markt, den ich auf Sim ausprobieren will | H41 |
| eine Uhrzeit oder einen Termin | H88, H89, H90, H92, dazu H45 (Übergabe zwischen Handelszentren), H51 (Zeitumstellung oder Feiertag als Experiment) |
| einen Satz aus Regelwerk oder Börsen-Mitteilung | H43, H91, H94 |
| mehrere Fälligkeiten oder Roll/Verfall | H34, H35, H36, H37 |
| einen Stress-Tag (Limit, Handelsstopp, Riesen-Spanne) | H49 |
| ein Orderflow-Muster | H48, H46, H47 |
| etwas aus Optionen oder Fonds | H56, H84, H96 |
| eine Tagestyp-Erzählung oder ein Bild der Bewegung | H73, H72, H74 |
| eine Vermutung, wer handeln muss oder wer zahlt | H95, H96, H97, H82, H83 |
| den Verdacht, dass Große etwas nicht handeln können | H85 |
| eine Notenbank-, Staats- oder Kartell-Lage | H104 |
| eine Vermutung über Saison oder physischen Kalender | H99, H101, H106 |
| einen anderen Markt, der etwas vorher zeigt | H52, H53, H54, H105 |
| eine Rangfolge über viele Märkte | H55 |
| Index-Bestandteile (Breite, Gewichte) | H108 |
| eine neue Datenquelle | H23, gezielt H98, H101, H106, H107 |
| einen Kontakt (Händler, Absicherer) oder fremde Trades | H78, H79, H80 |
| eine Geschichte oder Analogie | H81 |
| zwei Aussagen, die sich widersprechen | H70 |
| ein altes Urteil, dem ich nicht glaube | H33. Bei geänderter Lage H27, bei kaputtem Messgerät H28, für ungemessene Nachbarn H29 |
| einen auffälligen Live-Tag oder Fehler | H38, H39, H40 |
| Rechenzeit, aber keine Idee | H24 (Baukasten), H25 (lernendes Modell), H103 (andere Uhr), H87 (Register lesen) |
| gar nichts, Kopf leer | H86 (Landkarte), H109 (feste Verdrahtung), H102 (Maschine), H20 (Scan), Routine in Abschnitt 7 |
| die Frage, ob eine Regel auf alten Jahren hält | H110 (2010 bis 2015 verdeckt), sonst H42 (vorwärts messen) |

### 4.2 Korrekturen, die dem Anhang vorgehen

| ID | Stelle in der Anleitung | Es gilt |
|---|---|---|
| H01 | Eingabe Punkt 1 (Herkunft) | Herkunft: alle 6 Beine des Buchs vom Lauftag (PB3, LastHour_v3, Asia-Dir, OpenDrive, OpEx, LD01) plus RTY-Gap. Die Regel von RTY-Gap bleibt belegt, auch wenn das Bein raus ist. OpEx hat einen Verfallstermin in Markt-Uhr, der sich übersetzen lässt. |
| H01 | Eingabe Punkt 6 (Mindestgröße) | Ohne Angabe gilt die Hürde aus Rückfrage 4 (Abschnitt 6.2), gerechnet am Buch vom Lauftag. |
| H01 | Schritt 7 (Ampel) und Stopp-Regel 2 | Kosten-Stress ist eine Info-Zeile (R7), keine Bedingung für „trägt“. |
| H01, H56 | Stopp-Regeln „empirisch-nichts-gefunden“ | nur nach R7 (kleinster nachweisbarer Sharpe höchstens 0,55, also gepoolt über mindestens rund 2 unabhängige Märkte). |
| H56 | wann_nutzen und Falle 1 | Gemessen ist bisher nur der SPX-GEX auf NQ/ES (#110): Er sagte die Schwankung voraus, eine Richtung zeigte er dort nicht. Für andere Kennzahlen und Märkte gibt es keine Messung. Jede Tafel misst deshalb Richtung und Schwankung getrennt, und ein Treffer nur in der Schwankung geht als Rollen-Idee an H06. |
| H56 | Märkte-Checkliste K5 | Die Zahlen dort (MNQ 0,3 … ZN 9) sind Prozent der **Tagesspanne** aus dem Daten-Inventar. In Prozent der Tages-Schwankung laut Steckbrief gilt: MNQ 0,4, MGC 0,6, MCL 1,5, 6E 3,7, ZS 5,4, ZW 6,2, ZN 12,8. Gerechnet wird mit der Steckbrief-Basis. |
| H56 | Stopp-Regel Bein-Hürde | Bei NQ-Beinen mit r um 0,1 und v 0,25 liegt die Käfig-Schwelle im geschrumpften Buch bei etwa 0,54 (1,20 × 0,45), bei r 0 bei 0,30. |
| H56 | Querzeile Schritt 7 | mit gemessener Korrelation nach R8, nicht als einfache Summe t durch √M. |
| H110 | Schritt 7 | Die Jahre 2016 bis 2026 werden mit derselben eingefrorenen Config, dem Buch-Stand und den Kosten vom Lauftag (R1) einmal neu gerechnet. Das ist kein neuer Blick, weil die Jahre schon gesehen sind, und zählt nicht als Trial. Erst die zusammengesetzte Tagesreihe 2010 bis 2026 geht in Schritt 8 (Nachweisgrenze 0,62). |

**Auflage an den Code, der den Anhang baut:** über jede Anleitung ein festes Banner („Es gelten R1 bis R16 und der Buch-Stand vom Lauftag, 6 Beine NQ, ohne RTY-Gap. Kosten nur aus Abschnitt 1. Tafel-Urteil nur nach R7, Kosten-Stress ist eine Info-Zeile. Mindestgröße nach Rückfrage 4.“), je Anleitung eine Block-ID (`^h01` bis `^h110`), damit die Links unten genau auf die Anleitung springen, und die Korrekturen dieser Tabelle an der jeweiligen Stelle. Fehlt die Block-ID, öffnet der Link die Anhang-Notiz am Anfang.

### Beine: Startpunkt ist ein eigenes Bein, seine Trades oder Signale

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h01\|H01]] | Belegter Effekt, neue Zelle (Regel in Markt-Uhr übertragen) | fertige Regel, Frage „gilt das woanders?“. Mit H69 zusammengelegt. Herkunft: alle 6 Beine vom Lauftag (inkl. OpEx, LD01) plus RTY-Gap. | Name des Beins/Papers, Fenster in Markt-Uhr, Anker je Markt abnicken |
| [[Alpha-Suche Playbook (Anleitungen)#^h02\|H02]] | Struktur-Analogie | was trägt das Bein, wo gibt es dieselbe Bau-Eigenschaft? Felder, die schon unter H01/H69 laufen, rechnet H02 nicht neu, es übernimmt dort nur die Tafel. | je Bein ein Satz „was ist zu dieser Uhrzeit besonders“ |
| [[Alpha-Suche Playbook (Anleitungen)#^h03\|H03]] | Gegenpartei rückwärts | Vermutung, wer die eigenen Beine bezahlt | Teilnehmer, Grund, wann da, Größe grob |
| [[Alpha-Suche Playbook (Anleitungen)#^h04\|H04]] | Anatomie der eigenen Beine | Trade-Listen plus Why. Filter gehen in die H06-Matrix, nicht in eigene Grids. | Warum-Satz, bis 8 Merkmale vorab, Beispieltage |
| [[Alpha-Suche Playbook (Anleitungen)#^h05\|H05]] | Komplement (kein Signal, Filter, Stop) | Was steckt in den Tagen, die das Bein liegen lässt? | optional Beobachtung, Erwartung vorab |
| [[Alpha-Suche Playbook (Anleitungen)#^h06\|H06]] | Rollentausch (Filter, Exit, Größe, Tagesauswahl) | vorhandenes Signal in neuer Rolle. LD01 (VIX-Tor auf dem Momentum-Mechanismus) gehört hierher. Gemeinsames Rollen-Budget für H04, H06 und H15, höchstens 24 Felder je Markt und Runde. | Signal, Rolle, Ziel, Erwartung |
| [[Alpha-Suche Playbook (Anleitungen)#^h07\|H07]] | Buch als Signalgeber | Zustand der frühen Beine bis zu einer Uhrzeit. Die Liste der frühen Beine kommt aus dem Buch vom Lauftag (RTY-Gap gestrichen). | Ankerzeit, 0 bis 3 Tage |
| [[Alpha-Suche Playbook (Anleitungen)#^h08\|H08]] | Kombination zweier Signale | Schnittmenge oder Abfolge zweier gemessener Signale | A, B, Fenster, „allein reicht nicht, weil …“ |
| [[Alpha-Suche Playbook (Anleitungen)#^h09\|H09]] | Bündel schwacher Effekte | Liste „echt, aber zu klein“, nur wenn vorab eine Decke ab 0,5 rechnerisch möglich ist | OK zum Eintrittskriterium, Zielkonto |
| [[Alpha-Suche Playbook (Anleitungen)#^h10\|H10]] | Ersatz im selben Platz | schwächstes oder doppeltes Bein tauschen (LD01 und PB3 laufen an gemeinsamen Tagen mit 0,89). Der alte RTY-Satz entfällt. | Platz, Mindestgewinn in Monaten |
| [[Alpha-Suche Playbook (Anleitungen)#^h11\|H11]] | Pfad der eigenen Trades | „läuft erst gegen mich, dann los“ | Bein, Rücklauf, Beispieltage |

### Buch: Startpunkt ist eine gemessene Eigenschaft des ganzen Buchs

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h12\|H12]] | Lücke des Buchs zuerst | **einziger Buch-Lücken-Weg.** Varianten: Lücke = Zeit (H13), Treiber (H14), Platz (H17). Ein Feld Markt mal Fenster wird nur einmal gereiht. | welche Lücke zuerst, Zeitrahmen |
| [[Alpha-Suche Playbook (Anleitungen)#^h13\|H13]] | Zeit-Lücke (Variante von H12) | leere Stunden, flat Tage. Zelle B (unbedingte Richtung) gilt als **gesehen**. | Nacht ja/nein, Konten |
| [[Alpha-Suche Playbook (Anleitungen)#^h14\|H14]] | Treiber (Variante von H12) | Tage ohne Strecke kosten Geld | optional Beobachtung an Pendeltagen |
| [[Alpha-Suche Playbook (Anleitungen)#^h15\|H15]] | Verlusttag zuerst | schlimmste Buchtage. Vorab muss die Ketten-Power gerechnet werden. Filter gehen nach H06. | 3 bis 10 Tage, je 1 Gegenbeispiel |
| [[Alpha-Suche Playbook (Anleitungen)#^h16\|H16]] | Steckbrief rückwärts | **Stufe 0 (Machbarkeit) aller Wege**, kein eigener Weg | Konten, Rutschen aus Erfahrung |
| [[Alpha-Suche Playbook (Anleitungen)#^h17\|H17]] | Überlapp-Regel (Variante von H12) | Plätze ohne Zeit-Überlapp zum Buch, Unabhängigkeit je Bein gemessen | nichts. Nacht-Halten ist bei E8/FN innerhalb des Handelstags erlaubt, offen ist nur die E8-Reset-Zeit |
| [[Alpha-Suche Playbook (Anleitungen)#^h18\|H18]] | Buch-Marginal zuerst | Pool fertiger Reihen am Buch ranken. Ebene C nur bei passendem Buch-Stand und Engine ab 18.10., sonst Status „unentscheidbar, veraltet“. | Pool, Größe, Latte |
| [[Alpha-Suche Playbook (Anleitungen)#^h19\|H19]] | Epochen-Lücke | Gewinn hängt an wenigen Jahren. Ketten-Power vorab, ein Nullergebnis heißt „unentscheidbar“. | optional „seit Jahr X ist anders …“ |

### Daten: Startpunkt sind Daten ohne Idee

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h20\|H20]] | Landkarten-Scan | festes Raster über Rohdaten. Eine verdeckte Hälfte gibt es nur nach R11. | Märkte, Fenster, Freigabe |
| [[Alpha-Suche Playbook (Anleitungen)#^h21\|H21]] | Markt-Steckbrief statistisch | 15 Kennzahlen gegen Zufall. Ketten-Power vorab. | Liste OK, Mindestgröße |
| [[Alpha-Suche Playbook (Anleitungen)#^h22\|H22]] | Rückwärts vom Ergebnis | Was ging den auffälligsten Tagen voraus? Ketten-Power vorab, das Why bekommt einen Stempel. | Zielgröße, Entscheidungszeit, bis 5 Vermutungen |
| [[Alpha-Suche Playbook (Anleitungen)#^h23\|H23]] | Neue Datenquelle zuerst | Datei ohne Idee | Quelle, Takt, Geld, Zugang |
| [[Alpha-Suche Playbook (Anleitungen)#^h24\|H24]] | Baukasten-Suche | Maschine kombiniert Bausteine. Das Why bekommt einen Stempel. | Neues (Markt, Fenster, Baustein), Budget |
| [[Alpha-Suche Playbook (Anleitungen)#^h25\|H25]] | Lernendes Modell | viele Merkmale, eine Zielgröße. Ketten-Power vorab. | Ziel, Entscheidungszeit, Merkmale |
| [[Alpha-Suche Playbook (Anleitungen)#^h26\|H26]] | Muster zuerst, Erklärung danach | Muster ohne Ursache. Vorbild für die Regel zum Why (R4). | Muster, Herkunft, Zahl der Blicke |
| [[Alpha-Suche Playbook (Anleitungen)#^h103\|H103]] | Andere Uhr (Volumen- oder Strecken-Balken) | Verdacht, dass der Minuten-Schnitt verschmiert. Das Why bekommt einen Stempel. | Uhr-Art, Märkte |
| [[Alpha-Suche Playbook (Anleitungen)#^h110\|H110]] | Rückwärts verlängern (2010 bis 2015) | eingefrorene Regel einmal auf ungesehenen Jahren prüfen (Korrektur Schritt 7 in 4.2) | Kauf-OK nach Kostenabfrage, Regel „ein Blick“ |

### Friedhof: Startpunkt sind alte Urteile oder ungemessener Bestand

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h27\|H27]] | Wiedervorlage nach Bedingung | altes Urteil, neue Lage. Jobs, die an der Prämisse starben, laufen nur über H28 Stufe 4. | Änderungsliste, Obergrenze |
| [[Alpha-Suche Playbook (Anleitungen)#^h28\|H28]] | Lineal-Revision | Messgerät war kaputt oder wurde getauscht | Box-Freigabe |
| [[Alpha-Suche Playbook (Anleitungen)#^h29\|H29]] | Reichweiten-Komplement | ungemessene Nachbarn eines Urteils | welches Urteil, Budget |
| [[Alpha-Suche Playbook (Anleitungen)#^h30\|H30]] | Beinahe-Treffer und Warteraum | an genau einer Stufe hängen geblieben | Quellen der Warteliste, Latte |
| [[Alpha-Suche Playbook (Anleitungen)#^h31\|H31]] | Ungemessener Bestand | aufgeschrieben, nie gerechnet | Streichliste, Sperre aufheben ja/nein |
| [[Alpha-Suche Playbook (Anleitungen)#^h32\|H32]] | Rückholung verlorener Information | Stichwort wurde falsch getestet | 7 Angaben je Punkt |
| [[Alpha-Suche Playbook (Anleitungen)#^h33\|H33]] | Einspruch gegen ein Urteil | dein Bauch sagt „stimmt nicht“ | Urteil, 7 Angaben, „was hätte mich überzeugt“ |

### Laufzeit: Startpunkt sind mehrere Fälligkeiten und der Lebenslauf des Kontrakts

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h34\|H34]] | Terminkurve als Signal | nah gegen fern als Tor für den Front-Kontrakt | Box-Freigabe für Einzelkontrakte |
| [[Alpha-Suche Playbook (Anleitungen)#^h35\|H35]] | Terminkurve als Handelsobjekt | Spread selbst handeln. Zuerst prüfen, ob die Prop-Firma das erlaubt. Mehrtages-Form: P (Flat-Zeit). | Objekt, Haltedauer, Support-Fragen |
| [[Alpha-Suche Playbook (Anleitungen)#^h36\|H36]] | Roll-Fahrplan | Index-Roll, Quartalsroll, Volumenwechsel. Hier landet auch der Rohstoffindex-Roll aus H95 und H99. | Märkte, Roll-Arten |
| [[Alpha-Suche Playbook (Anleitungen)#^h37\|H37]] | Lebensende des Kontrakts | Andienung, Verfall, Lieferung | Termin-Arten, Prop-Erfahrung |

### Live: Startpunkt ist der Betrieb

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h38\|H38]] | Live gegen Backtest | Fills weichen ab | „das war komisch“ mit Datum |
| [[Alpha-Suche Playbook (Anleitungen)#^h39\|H39]] | Post-mortem eines Tags | ein Tag hat überrascht | Datum, was, was erwartet |
| [[Alpha-Suche Playbook (Anleitungen)#^h40\|H40]] | Unfall-Fund | ein Fehler hat etwas gezeigt | Fund, was war gemeint |
| [[Alpha-Suche Playbook (Anleitungen)#^h41\|H41]] | Probe-Handel auf Sim | Fills in fremdem Markt kennenlernen (Teil von T21) | Markt, Fenster, 50 Orders mit Notiz |
| [[Alpha-Suche Playbook (Anleitungen)#^h42\|H42]] | Vorab festschreiben, vorwärts messen | keine brauchbare Historie | Wenn-Dann-Satz, Mindestgröße, Geduld |

### Marktbau: Startpunkt sind Regeln, Uhr und Mikrostruktur eines Markts

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h43\|H43]] | Regelwerk zuerst | Satz aus Spezifikation, Börsen- oder Prop-Regel | Wortlaut, Markt, Uhrzeit |
| [[Alpha-Suche Playbook (Anleitungen)#^h44\|H44]] | Markt-Uhr | Öffnung, Schluss, Pause, Wiedereröffnung | Markt, optional Grenze mit Tagen |
| [[Alpha-Suche Playbook (Anleitungen)#^h45\|H45]] | Staffelstab zwischen Handelszentren | Asien zu London zu NY | optional Killzone-Zeiten |
| [[Alpha-Suche Playbook (Anleitungen)#^h46\|H46]] | Ausführungs-Fußabdruck | „da lief einer rein“ | Ausführungsart, Erkennungsmerkmal, Tage |
| [[Alpha-Suche Playbook (Anleitungen)#^h47\|H47]] | Liquiditäts-Bereitstellung | Druck, dann Rückkehr | optional Merkmal „muss raus“ |
| [[Alpha-Suche Playbook (Anleitungen)#^h48\|H48]] | Orderbuch und Aggressor | Orderflow-Muster (Daten nur NQ, ES, YM; außerhalb davon über T21) | Musterliste mit 7 Angaben |
| [[Alpha-Suche Playbook (Anleitungen)#^h49\|H49]] | Stress-Katalog | Limit-Tage, Handelsstopps, Riesen-Spannen | 3 bis 10 erlebte Tage |
| [[Alpha-Suche Playbook (Anleitungen)#^h50\|H50]] | Markt-Steckbrief strukturell | Markt ohne Meinung | Markt, eigenes Wissen als Zeile |
| [[Alpha-Suche Playbook (Anleitungen)#^h51\|H51]] | Natürliches Experiment | Ursache prüfen über Zeitumstellung, Feiertag | Muster, vermutete Ursache |

### Marktverbund: Startpunkt sind mehrere Märkte zusammen

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h52\|H52]] | Informationsweg A nach B | A zeigt es früher als B (Gold: 8 Zellen in #184 gemessen, nur diese abziehen) | Paar, Verzögerung, Beispiel |
| [[Alpha-Suche Playbook (Anleitungen)#^h53\|H53]] | Preisgleichung | Klammer zwischen Preisen | Beziehung, Datenentscheid |
| [[Alpha-Suche Playbook (Anleitungen)#^h54\|H54]] | Zerlegung in Treiber und Rest | was bewegt alle, was bleibt | Korb, Treiber-Namen |
| [[Alpha-Suche Playbook (Anleitungen)#^h55\|H55]] | Querschnitt über den Korb | Rangordnung über Märkte. Mehrtages-Form: P (Flat-Zeit), Intraday-Form offen. | Korb, Kennzahl |
| [[Alpha-Suche Playbook (Anleitungen)#^h56\|H56]] | Derivate-Rückkopplung | Absicherung aus Optionen und Fonds (Korrekturen in 4.2) | Optionsflow-Liste |
| [[Alpha-Suche Playbook (Anleitungen)#^h105\|H105]] | Gebauter Markt | Kreuz oder Verhältnis zweier Märkte | Objekte, Zwei-Bein-Konto ja/nein |
| [[Alpha-Suche Playbook (Anleitungen)#^h108\|H108]] | Innenleben des Korbs | Breite und Gewicht der Bestandteile | Datenstufe, Geldgrenze |

### Mensch: Startpunkt ist dein Wissen, deine Beobachtung, deine Trades

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h57\|H57]] | Beobachtung zuerst | Satz „wenn X, dann Y“ (Gold-H1-Breakouts in #189/#190 gemessen, nur diese Zellen) | 7 Angaben |
| [[Alpha-Suche Playbook (Anleitungen)#^h58\|H58]] | Wissens-Inventar | „ich weiß viel, steht nirgends“ | 2 bis 3 Sitzungen Diktat |
| [[Alpha-Suche Playbook (Anleitungen)#^h59\|H59]] | Artefakt-Archäologie | alte Screenshots, Journale | Ordner, Erlaubnis |
| [[Alpha-Suche Playbook (Anleitungen)#^h60\|H60]] | Begriff per Markierung scharf machen | ICT-Begriff ohne Formel | 30 bis 50 Markierungen |
| [[Alpha-Suche Playbook (Anleitungen)#^h61\|H61]] | Beispiel-Tage zuerst | Tage ohne Satz | 5 bis 30 Tage |
| [[Alpha-Suche Playbook (Anleitungen)#^h62\|H62]] | Eigene Trades als Datensatz | Exporte aus zwei Jahren | Dateien, Setup-Etiketten |
| [[Alpha-Suche Playbook (Anleitungen)#^h63\|H63]] | Verlust-Muster umdrehen | wiederkehrend ausgestoppt | 3 bis 10 Situationen |
| [[Alpha-Suche Playbook (Anleitungen)#^h64\|H64]] | Intuition im Blind-Replay | Gefühl ohne Worte | 100 Vorhersagen |
| [[Alpha-Suche Playbook (Anleitungen)#^h65\|H65]] | Vorhersage-Tagebuch vorwärts | Erwartungen ohne Regel | Zeilen täglich |
| [[Alpha-Suche Playbook (Anleitungen)#^h66\|H66]] | Bildschirmzeit in unbekanntem Markt | keine eigene Beobachtung | 4 mal 90 Minuten Blind-Blätter |
| [[Alpha-Suche Playbook (Anleitungen)#^h67\|H67]] | Erfahrungsregel in Nebenrolle | Handwerk, Vermeidung | Regel, Rolle, Bein |
| [[Alpha-Suche Playbook (Anleitungen)#^h68\|H68]] | Eigenes Why verallgemeinern | Erklärung eines Beins | Why, Verbot, Dosis |
| [[Alpha-Suche Playbook (Anleitungen)#^h69\|H69]] | Übersetzen statt klonen | **mit H01 zusammengelegt**, ein Trial-Zähler | Original, Anker je Markt |
| [[Alpha-Suche Playbook (Anleitungen)#^h70\|H70]] | Widerspruch zuerst | zwei Aussagen gegeneinander | A, B, Belegregel je Seite |
| [[Alpha-Suche Playbook (Anleitungen)#^h71\|H71]] | Erklär-Probe | „das weiß man halt“ | 1 Stunde Erklären |

### Modell: Startpunkt ist eine Annahme über die Art der Bewegung

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h72\|H72]] | Prozess-Modell zuerst | Bild als Formel (Rückkehr, Schübe, Sprünge) | Bild, optional Zahl |
| [[Alpha-Suche Playbook (Anleitungen)#^h73\|H73]] | Zustand zuerst | Tagestypen, Zustands-Karte | Typen, Uhrzeit des Erkennens |
| [[Alpha-Suche Playbook (Anleitungen)#^h74\|H74]] | Vorhersagbares zuerst | Spanne, Schwankung, Volumen statt Richtung | Zielgröße, Morgen-Gefühl, eine Verwendung |

### Praktiker: Startpunkt ist, was andere Händler sagen oder tun

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h75\|H75]] | Praktiker-Text ausformulieren | Methode mit Ermessen | Quelle, 7 Angaben |
| [[Alpha-Suche Playbook (Anleitungen)#^h76\|H76]] | Fertige Regel 1:1 nachbauen | komplette Regel eines anderen | Originalquelle, Lücken |
| [[Alpha-Suche Playbook (Anleitungen)#^h77\|H77]] | Folklore und Daumenregel | „jeder weiß doch …“ | Spruch, höchstens 2 Lesarten |
| [[Alpha-Suche Playbook (Anleitungen)#^h78\|H78]] | Strukturiertes Praktiker-Gespräch | Kontakt kennt fremden Markt | Kontakt, Einwilligung, Mitschrift |
| [[Alpha-Suche Playbook (Anleitungen)#^h79\|H79]] | Gespräch mit jemand, der handeln muss | Absicherer, Einkäufer | Quelle, Erlaubnis |
| [[Alpha-Suche Playbook (Anleitungen)#^h80\|H80]] | Trades anderer als Datensatz | Calls mit Zeitstempel | Liste, Echtheit, Nutzungsrecht |
| [[Alpha-Suche Playbook (Anleitungen)#^h81\|H81]] | Erzählung, Analogie, Stammtisch | Geschichte ohne Zahlen | Geschichte, Ereignis, Folge |

### Prämie: Startpunkt ist eine bezahlte Risiko-Übertragung

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h82\|H82]] | Risikoprämien-Inventur | wer zahlt wofür. Mehrtages-Form: P (Flat-Zeit), Intraday-Form offen. | Vermutung, Haltedauer |
| [[Alpha-Suche Playbook (Anleitungen)#^h83\|H83]] | Zeit im Risiko | Nacht, Pause, Wochenende (Wochenende: P bei allen drei Firmen) | nur Freigaben |
| [[Alpha-Suche Playbook (Anleitungen)#^h84\|H84]] | Schwankungs-Prämie | eingepreist gegen eingetreten | Daten-Freigabe, Support-Frage zu Optionen |
| [[Alpha-Suche Playbook (Anleitungen)#^h85\|H85]] | Kapazitäts-Nische | was Große nicht handeln können (siehe 7.1) | Kontraktliste, Rutschen-Erfahrung |

### Suchhistorie: Startpunkt ist die eigene Suche

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h86\|H86]] | Landkarte der leeren Zellen | „wo nie geschaut?“ | Achsen absegnen |
| [[Alpha-Suche Playbook (Anleitungen)#^h87\|H87]] | Register als Datensatz | Masse der alten Versuche lesen. Das Why bekommt einen Stempel. | nichts |
| [[Alpha-Suche Playbook (Anleitungen)#^h109\|H109]] | Feste Verdrahtung | Voreinstellungen, die nie bewegt wurden | Liste durchgehen, Herkunft je Zeile |

### Termin: Startpunkt ist ein fester Zeitpunkt

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h88\|H88]] | Termin zuerst | mit gegen ohne Termin. News-Sperre bei FFN Funded beachten (R2). | Termin, Fenster, stark/alle |
| [[Alpha-Suche Playbook (Anleitungen)#^h89\|H89]] | Überraschung zuerst | Ist gegen Erwartung. News-Sperre bei FFN Funded (R2). | Konsensquelle, Schwelle je Art |
| [[Alpha-Suche Playbook (Anleitungen)#^h90\|H90]] | Uhr und Kalender als Raster | die Uhr ist die Hypothese. OpEx im Buch gehört hierher. Weil das Raster selbst viele Zellen hat, gilt hier Šidák über alle Raster-Zellen oder Bestätigung über H110. | OK fürs Raster |
| [[Alpha-Suche Playbook (Anleitungen)#^h91\|H91]] | Regeländerung als Experiment | Datum, ab dem etwas anders ist | Änderung mit Datum |
| [[Alpha-Suche Playbook (Anleitungen)#^h92\|H92]] | Referenzpreis-Fenster | Fixing, Settlement, Auktion. Fixings aus H95 landen hier. News-Sperre bei FFN Funded (R2). | Fenster, optional Beobachtung |

### Text: Startpunkt ist ein Dokument

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h93\|H93]] | Paper zuerst | Studie mit Regel und Zeitraum. **Wird erst gereiht, wenn ein konkretes Paper vorliegt.** | Link oder PDF |
| [[Alpha-Suche Playbook (Anleitungen)#^h94\|H94]] | Teilnehmer-Quellen lesen | Rulebook, Mitteilungen, Händlerberichte | Märkte, bekannte Quellen |
| [[Alpha-Suche Playbook (Anleitungen)#^h107\|H107]] | Wortlaut zuerst | Text als Messgröße | Quellen, 30 bis 50 Blind-Bewertungen |

### Ursache: Startpunkt ist ein Akteur, der handeln muss

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h95\|H95]] | Pflichtfluss-Kalender | Index-Fonds zum Monatsende, Händler nach Auktionen, Absicherer mit Frist. Prop-Flat gehört zu H97, Roll zu H36, Fixing zu H92. | wer, wann, warum |
| [[Alpha-Suche Playbook (Anleitungen)#^h96\|H96]] | Regelgebundene Umschichter | Auftrag aus Formel nachrechnen | Gruppe, Quelle der Regel |
| [[Alpha-Suche Playbook (Anleitungen)#^h97\|H97]] | Zwangsliquidation | Grenze drückt raus (auch Prop-Flat, Freitag) | Grenzen, Prop-Alltag |
| [[Alpha-Suche Playbook (Anleitungen)#^h98\|H98]] | Positionierung | wer sitzt wo | Idee, Datenarten |
| [[Alpha-Suche Playbook (Anleitungen)#^h99\|H99]] | Absicherer und Jahreslauf | physischer Kalender. Index-Roll gehört zu H36. | Märkte, Jahreslauf-Wissen |
| [[Alpha-Suche Playbook (Anleitungen)#^h100\|H100]] | Auftrags-Häufung an Bezugspunkten | Stops, Marken, Sweep | Verhalten, Bezugspunkt, Durchstich |
| [[Alpha-Suche Playbook (Anleitungen)#^h104\|H104]] | Ziel-Akteur | Notenbank, Kartell, Staat | Akteur, Beobachtung |

### Fundamental: Startpunkt ist eine Größe außerhalb des Kurses

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h101\|H101]] | Fundamental-Lage | Mengen-Bilanz, fairer Wert | Daten-Bau-OK, eine Verwendung |
| [[Alpha-Suche Playbook (Anleitungen)#^h106\|H106]] | Außentreiber mit Vorhersage | Wetter und Ähnliches | Beschaffungs-Entscheidung |

### Maschine: Startpunkt ist eine Vorschlags-Schleife

| ID | Name | Wann nutzen | Was Max liefert |
|---|---|---|---|
| [[Alpha-Suche Playbook (Anleitungen)#^h102\|H102]] | Maschine als Ideengeber | Vorschlags-Schleife mit Zählung und Deckel | Budget, Gerüst-Freigabe, keine Startsaat |

---

## 5. Reihenfolge-Regel und Such-Budget

### 5.1 Die Spielregeln für jeden Weg

Diese Regeln gelten für **jede** Anleitung und gehen dem Text der einzelnen Anleitung vor. Darin stecken alle Blocker und alle „wichtig“-Punkte der Methoden-Prüfung und der Gegenleser. Die technischen Details (Dateien, Schlüssel, Code-Stellen) stehen für Claude im Anhang unter „Technik zu R1 bis R16“.

| Nr | Regel |
|---|---|
| **R1 Buch-Stand** | Jede Rechnung zieht den Buch-Stand am Tag des Laufs (Stand 24.10.: 6 Beine NQ, ohne RTY-Gap) mit Gebühr 1,90 $ und Exit 15:55 zum Close. Zahlen vom 13.10. sind nur Beispiele. |
| **R2 Stufe 0 Machbarkeit** | Vor jedem Feld kommt die Steckbrief-Machbarkeit (früher H16), Liste unten. |
| **R3 Satzung vorab** | Bevor eine Zahl gerechnet wird, liegt eine Satzung mit Hash vor: Wortlaut, 4 Kern-Zellen, Fenster in Markt-Uhr, Kosten, Mindestgröße, Reichweite, Variantenbudget, erwartete Zahl gestarteter Grids unter Null (Felder × 0,15). Zellen nachträglich zu wählen ist verboten (Fehlalarm bis 74 %). |
| **R4 Why-Status** | Pflichtfeld in der Satzung, Liste unten. |
| **R5 Look-ahead** | Einstieg zum Open der Bar **nach** der Signal- oder Ereignisminute. Merkmale nutzen nur die letzte abgeschlossene Bar davor. Jede tragende Zelle wird zusätzlich mit Einstieg eine Bar später gerechnet (Kontrolle, keine Kern-Zelle). Bricht der Vorteil um mehr als ein Drittel ein oder dreht das Vorzeichen, fällt die Zelle als Look-ahead- oder Fill-Verdacht. Modi ohne Verzögerungs-Schalter brauchen ein eigenes Skript mit Verzögerung und werden nie zum Live-Kandidaten. |
| **R6 Zählung** | Jede gerechnete Tafel-Zelle und jede Grid-Variante mit Handelsregel wird **vor dem Lauf** ins Register eingetragen. Kontrollen (Placebo, Zwilling, Spiegel, Verzögerung) zählen nicht. Reine Beschreibungen ohne Handelsregel zählen in der Satzung und im Logbuch-N, nicht im Register. Die alte Zufallsdecke bei 69.600 Trials ist gesättigt (1,324 auf 1,327) und taugt nicht als Zähler. Gezählt wird, wie viele Zufallstreffer bei dieser Zahl von Feldern zu erwarten sind: **Zufalls-Kandidaten = Felder × p0**. Unter der Stufenregel ist p0 = 0,09 % (Null mit Kosten) bis 2,2 % (netto genau 0) je Feld, ohne Tafel 3,2 %. Gemessen ist nur die Obergrenze 4,2 % (0 von 69, Index-Märkte, 29.09.). *Zwischen den Prüfern ist strittig, ob Tafel-Zellen ins Register oder nur in die Satzung gehören, deshalb Entscheidung E2.* |
| **R7 Tafel-Urteil** | vorläufig, noch nicht geeicht, Liste unten. |
| **R8 Querzeile** | Z = Σ t_i / √(M + M(M−1)·ρ̄). ρ̄ (mittlere Korrelation der Zellen zwischen den Märkten) wird vorab aus den Tages-Zellreihen gemessen, auf Placebo-Zeiten, nicht aus dem Treffer. Bis dahin gilt ρ̄ 0,3 zwischen Nicht-Index-Märkten und 0,8 unter NQ/ES/YM/RTY. Gepoolt werden darf nur über Zell-Typen, die vorab in der Satzung standen. |
| **R9 Grid-Eingang** | Ein Grid (höchstens 24 Varianten) startet, wenn die Tafel des Felds trägt (bestes t ab 1,60). Querzeile und Šidák über alle Felder der **Welle** (nicht der Satzung, damit man die Hürde nicht durch Aufteilen umgehen kann) laufen als Etikett mit: Unter der Šidák-Schwelle (bei rund 40 Zellen t ab 3,0, gezeigter Sharpe etwa 0,92) heißt der Kandidat in Inbox und Wochenend-Prüfung „Einzeltreffer, Šidák nicht erreicht“. Obergrenze: Grids höchstens 0,25 × Felder je Welle. |
| **R10 Ketten-Power** | Wege mit gestapelten Toren (H15, H19, H21, H22, H25 und alle mit mehr als 2 Toren vor der Tafel) rechnen vorab die Power der ganzen Kette (Tore + Tafel + Gate v4 Stufe 1) bei wahrem Sharpe 0,5 und 0,8. Liegt sie bei 0,8 unter 30 %, gilt der Weg nur noch als Querzeilen-Weg oder als Lieferant für Wiedervorlagen, und ein Nullergebnis heißt „unentscheidbar“. Tore, die dieselbe Frage doppelt stellen, werden zusammengelegt. |
| **R11 Verdeckte Jahre** | Die Jahre ab 2021 gelten auf NQ, ES, YM, RTY und GC als **gesehen** (92 % des Buchgewinns, zigfach angeschaut). CL (163 Trials) bekommt eine verdeckte Hälfte ab 2021, wenn die Gesehen-Liste für CL vorab leer ist. 6E, ZS, ZW gelten im Fenster 09:30 bis 15:55 ET seit 10. bzw. 16.10. als gesehen; ein verdeckter Teil existiert dort nur in anderen Fenstern. Ein verdeckter Teil existiert sonst nur auf Märkten und Fenstern ohne Register-Trials und ohne Vorzählung (6B, ZN, ZB, FDAX). Echte Bestätigung sonst nur über 2010 bis 2015 (H110) oder vorwärts (H42). Deine Bildschirmzeit (etwa 2024 bis heute) wird getrennt ausgewiesen. Trägt eine Zelle nur in den Jahren mit deinem Blick, ist sie ein Hinweis, kein Befund. Die Gesehen-Liste (Markt, Fenster, Datum, Quelle) wird vor der Tafel mit Hash angelegt. |
| **R12 Erste Fassung** | Liste unten. |
| **R13 Walk-Forward-Start** | Für Märkte mit Datenstart 28. bis 30.12.2015 (GC, CL, 6E, ZS, ZW u. a.) wird der Start 01.01.2016 im Job ausdrücklich gesetzt, damit das erste Training 2 volle Jahre hat. Bis zum Fix werden diese Ergebnisse mit „Layout 6 von 10“ gestempelt. |
| **R14 Scratch ist kein Kandidat** | Ein Ergebnis aus einem Einmal-Skript zählt nie als Kandidat. Ins Next-Buch kommt es erst nach einem Runner-Lauf mit durchgereichtem Fenster und dem Eintrag der ersten Fassung. |
| **R15 Null bei vielen Feldern** | Kommen bei mehr als 30 Feldern 0 Kandidaten heraus, ist das zuerst ein Filter-Alarm: Stufen einzeln prüfen (Satzung, Tafel, Gate, Marginal) und melden, wo wie viele hängen blieben. Ein Befund ist es erst danach. |
| **R16 Leere Zeile** | „Kein Akteur / kein Treiber / kein Korb“ gilt nur mit Fundstelle in einer Primärquelle. Ohne Fundstelle bleibt die Zeile „offen“. |

**R2 Stufe 0 Machbarkeit, die Liste:**
- Daten, Engine-Tabelle, Kosten-Bremse mit Vorbehalt (Abschnitt 1), Größen-Budget je Trade (Abschnitt 1, Regel 12 der Landkarte).
- **Prop-Erlaubnis, Symbole:** E8 (44 Symbole, Liste 13.10.): keine ZT/ZF/ZN/ZB/UB/TN/ZQ, kein FDAX, Krypto MBT ja. FundedNext (35 Symbole, Artikel 29.08.): ohne Zinsen, ohne M6E/M6B (FX-Micros nur M6A), ohne Krypto, HO, PL/PA. FFN: Einzelmärkte unbelegt (T16).
- **Prop-Erlaubnis, Zeitregeln:** Entry-Fenster E8 18:15 bis 16:10 ET, FundedNext 18:00 bis 16:10 ET; Flat 16:10 ET bzw. FFN 16:50 ET; Wochenende bei allen verboten; News-Sperre bei FFN Funded (FOMC, Minutes, NFP, CPI je 1 Minute vor und nach, sonst Liquidation und Gewinn weg). Ein Feld, dessen Kern-Zelle in eine Sperre fällt, ist für dieses Konto P, nicht tot. Das gilt besonders für H88, H89 und H92.
- **Handelsobjekt bei großen Kontrakten:** Bei 6E wird in der Satzung festgelegt, ob M6E gehandelt wird (Kosten 8,4 % der Tages-Schwankung, Kosten-Bremse vorab) oder 6E nur Signalquelle für einen anderen Markt ist. Den 6E-Vollkontrakt rechnen wir mit, kennzeichnen ihn aber als „über dem Größen-Budget“ und prüfen die Schwankung je Trade. Dieselbe Regel gilt für ZS und ZW (Micro-Ag ohne Daten und ohne Prop-Liste).
- **Krypto:** nutzbar ab MBT 05/2021 (vorher kostentot, weil der Preis bei 7.000 statt 83.000 $ lag), also rund 5,4 Jahre, Nachweisgrenze etwa 1,07 statt 0,76; Kosten 6,40 $ Hin und Zurück (#188); handelbar nur auf E8. Eigene Informationsquellen, die es nur bei Krypto gibt: Funding der Perpetuals, Spot-ETF-Flüsse, CME-Basis gegen Spot, Spot-Wochenendbewegung gegen die CME-Lücke. Heute D (keine Datei), Wege H23, H52, H53, Beschaffung offen.

**R4 Why-Status, die Liste:**
- In der Satzung steht einer von drei Werten: **kausal vorab** (Akteur, warum er zahlt, warum das Geld liegen bleibt, Datum vor der Tafel), **nur Herkunft** oder **nachträglich**.
- Ein Why, das nach dem ersten Tafel-Ergebnis geschrieben wird, gilt als nachträglich. Dann: Grid höchstens 8 Varianten, Querzeile oder zweiter Markt muss tragen, dazu eine vorab notierte Vorhersage über das Muster hinaus (Dosis, Abwesenheit, Übertragung) als gezählte Zelle und eine Ende-Bedingung.
- Ohne das gilt die Regel aus H26: höchstens Käfig-Untergrenze als Größe, Überwachung auf Verfall, Etikett „Muster ohne Ursache“ in Ticket und Wochenend-Prüfung.

**R7 Tafel-Urteil (noch nicht geeicht), die Liste:**
- Beste der 4 Zellen mit t ab 1,60 (gezeigter Sharpe ab 0,49 auf 10,6 Jahren) → **Kandidat**, weiter nach R9.
- Epochen, Kosten-Stress und Gegengruppe sind Info-Zeilen, keine zusätzliche K.o.-Stufe.
- Alle 4 Zellen bei etwa 0 oder darunter, die obere Bandgrenze unter der Mindestgröße **und** der kleinste nachweisbare Sharpe höchstens 0,55 (gepoolt über die effektive Zahl der Märkte) → **empirisch-nichts-gefunden**, nur für diese Märkte und diese Zellen. Auf einem Markt allein ist das nie erfüllt (0,76 ist größer als 0,55), nötig sind gepoolt mindestens rund 2 unabhängige Märkte. Wo eine Anleitung „nichts gefunden“ auf einem Markt erlaubt, gilt diese Regel vor.
- Alles andere → **unentscheidbar**, kommt nicht auf den Friedhof.
- Bis die Eichung (W0-1) da ist, steht im Urteil: „Fehlalarm dieses Markts ungemessen, Zahlen sind Obergrenzen, real etwa mal 0,85“.
- Bei Beobachtungen sind die 4 Zellen nicht unabhängig (gleiche Ereignistage). Bis der Statistiker es bestätigt, wird der Fehlalarm mit der gemeinsamen Ereignismenge simuliert.

**R12 Erste Fassung, die Liste:**
- **Bevor eine Idee in die Queue geht**, schreibt Claude ihre erste Fassung auf und legt sie dir vor: die Einstellung des ersten Jobs dieser Linie, nicht die Satzung und nicht die beste Grid-Zelle. Bei einem Grid ohne feste Einstellung stattdessen die Kennzahlen aus Stufe 1 (Sharpe, Jahre, Band).
- Ersatz- oder Zusatz-Beine erben die Fassung des Originals.
- Pflichtfeld: Datum des ersten Blicks auf die Idee.
- Eingetragen wird von der Hauptsession. Das Hochstufen ins Next-Buch schreibt den Eintrag heute noch nicht mit (T06).
- **Ohne Eintrag kein Job, ohne Eintrag kein Wochenende.**

### 5.2 Reihenfolge-Regel, korrigiert

Gereiht werden nur Felder mit Status T oder W. **Punkte = 3 × Bedarf + 2 × Unabhängigkeit + 3 × Testbarkeit + 2 × Testkosten.** Die Gewichte sind eine Setzung (Entscheidung E3). Gerechnet mit `p6_neu.py` (Scratch-Ordner).

| Kriterium | Regel |
|---|---|
| **Bedarf A (0 bis 2)** | +1, wenn der Weg ein Fenster außerhalb 09:30 bis 16:00 ET erlaubt (gemessene Lücke des Buchs: nachts in allen Märkten leer). +1, wenn er Pendeltage oder einen zweiten Treiber adressiert (gemessen: −25 $ an Tagen ohne Strecke). **Gestrichen:** „+1, wenn kein Aktienindex“ (Klassen-Etikett, zählte den Markt doppelt) und „Markt hat mindestens 40 % Volumen außerhalb RTH“ (Markt-Eigenschaft, kein Bedarf des Buchs; Liquidität prüft jetzt die Kosten-Bremse in Stufe 0). |
| **Unabhängigkeit U (0 bis 3)** | wird **je Feld (Markt und Fenster)** vergeben, nur nach Gemessenem. Im NQ-Fenster 09:30 bis 16:00 ET zählt die Rohbewegung gegen NQ: unter 0,2 → 2, 0,2 bis 0,5 → 1, ab 0,5 → 0 (CME-BTC 0,48 → 1). Fenster ohne Zeit-Überlapp zum Buch: gemessene Reihe gegen das Buch, also NQ-Nacht 0,04 → 2; GC, CL, 6E, ZS, ZW behalten ihre 2; **ungemessene Nacht-Paare (ES, YM, RTY, BTC, 6B, ZN/ZB, FDAX) → 1** mit dem Vermerk „messen vor Welle“ (W0-2). +1, wenn die Informationsquelle nicht der eigene Preis ist. U aus dem Fenster gilt nur, wenn die Kern-Zellen der Satzung tatsächlich außerhalb 09:30 bis 16:00 ET oder an Buch-flat-Tagen liegen. |
| **Testbarkeit T (0 bis 3)** | offen testbar 3, kleiner Bau 2, großer Bau 1, nicht testbar 0 (dann nicht gereiht) |
| **Testkosten K (0 bis 3)** | 3 = Rechnung ohne Trials, 2 = 4 Tafel-Zellen, 1 = viele Felder oder Beschaffung, 0 = Wochen deiner Zeit |
| **Gleichstand** | entscheidet ein **Los mit vorab notiertem Seed** (20261028), nicht die Reihenfolge der IDs. |
| **Nicht gereiht** | 28 Wege mit Status „braucht Eingabe“: H93 ohne konkretes Paper; 18 Wege, die deine 7 Angaben brauchen (H26, H32, H40, H41, H42, H57, H58, H60, H61, H63, H64, H65, H66, H70, H71, H75, H78, H79); 9 Wege, denen eine Datei oder ein Baustein fehlt (H51, H91, H92, H94, H95, H97, H99, H102, H103). Sie springen in die Reihung, sobald eine Vorlage mit den 7 Angaben bzw. die Datei vorliegt. Bis dahin zählen sie als offen, nicht als nachrangig. |
| **Slots je Welle** | höchstens 3 Felder je Weg und 3 je Markt. **Mindestens 1 Feld auf einem Markt mit (fast) 0 Register-Trials** (6E, ZS, ZW, 6B, ZN/ZB, FDAX), damit der Ausschluss durch Werkzeug sichtbar und befristet bleibt. |
| **Gezählte Sensitivität** | Platz 1 bis 6 sind robust: in 23 bis 24 von 24 Varianten (8 andere Gewichtungen × 3 Lose) dabei. Platz 7 bis 9 nur in 4 bis 8 von 24, Platz 10 ist der Pflicht-Slot, per Los aus 9 gleichauf liegenden Feldern gezogen. Gegen die Gewichte bleiben 6 bis 10 von 10 Feldern gleich, gegen 5 andere Lose 9 bis 10. Zählt man Fenster-Felder als „kleiner Bau“ (T 2, solange W0-4 Teil A fehlt), bleiben nur 2 von 10. |
| **Variante verdict-auditor** | Gibt man jedem Nachtfenster auf jedem Markt U 2 (auch ungemessenen Paaren), füllt sich die Welle mit Index-Nächten (H13 und H83 auf ES, YM, RTY, dazu H88 auf ES/RTY), 10 Felder liegen bei 23 Punkten gleichauf, und je nach Los wechseln 3 bis 5 Felder. Weil die Nacht nur für NQ gemessen ist, nehme ich die strengere Fassung (nur Gemessenes zählt). Entscheidung E9. |

### 5.3 Welle 0: Eichen, Messen und Bauen vor der ersten Welle

Ohne Welle 0 grenzt das Werkzeug faktisch 6E, ZS und ZW aus (80 von 110 Feldern hängen dort am Werkzeug), und 8 der 10 Felder der ersten Welle kämen nicht über die Tafel hinaus. Das ist dieselbe Struktur, die in #165 und im Friedhof-Inventar beanstandet wurde.

| Nr | Was | Wer | Frist (Vorschlag) |
|---|---|---|---|
| W0-1 | **Eichung der Stufenregel:** (a) Fehlalarm der Tafel aus mindestens 200 Placebo-Feldern (Zufallsfenster, Seed vorab, 0 Register-Trials, Fehler etwa ±2,5 Prozentpunkte) auf GC, CL, 6E, ZS, ZW, BTC. (b) Power per Signal-Einbau: auf Placebo-Reihen einen bekannten Sharpe von 0,5 und 0,8 aufsetzen und Tafel plus Gate v4 Stufe 1 durchlaufen lassen. (c) Eigene Beine nur als Plausibilitätsprobe auf den Jahren nach ihrer ersten Fassung (sie sind Sieger aus rund 69.600 Trials, ihr t ist durch die Auswahl aufgebläht). p0 durch Gate v4 bleibt bis zu einer großen Null-Kampagne eine Obergrenze (heute höchstens 4,2 % aus 0 von 69, nur Index-Märkte). Zum Vergleich: 10 bis 20 Placebo-Felder hätten bei 0 Treffern nur „unter 14 %“ gesagt. | Statistiker, Backtest-Runner (Box, über die Rechen-Bremse) | vor Welle 1 |
| W0-2 | **Unabhängigkeit messen, 0 Trials:** Nacht-Reihen von ES, YM und RTY gegen das Buch (wie NQ-Nacht 0,04), Volumen-Anteil außerhalb RTH für BTC aus den Daten (heute Platzhalter 0,5), Rohbewegung 6B, ZN, ZB, FDAX gegen NQ. Danach U neu setzen und neu reihen. BTC gegen das Buch ist schon gemessen (#188). | Claude | vor Welle 1 |
| W0-3 | **Buch-Profil für das 6er-Buch neu messen** (Liste im Kasten oben). | Claude + Mathematiker | vor Welle 1 |
| W0-4 | **Werkzeug-Paket**, zwei Teile. **Teil A vor Welle 1:** eigenes Fenster in Runner, Controls und Nullmodellen durchreichen, Nullmodelle ohne die Annahme von 390 Minuten. **Teil B vor Welle 2:** Generator und Bank, die 9 fest auf RTH stehenden Modi, Klon-Weg in Markt-Uhr, Roll-Maske, Tafel-Eingang ohne scipy, Walk-Forward-Start (R13). | Entwickler + Pipeline-Prüfer, Golden Master | Teil A vor Welle 1, Teil B vor Welle 2, danach neu reihen |

### 5.4 Erste Welle (Ergebnis der korrigierten Regel)

| Nr | Feld | Punkte (A U T K) | Auflage |
|---|---|---|---|
| 1 | H13 Zeit-Lücke × NQ | 23 (2 2 3 2) | Zelle B (unbedingte Richtung) gilt als gesehen (NQ-Nacht long 0,04 gemessen) und zählt nicht als Kern-Zelle. Es laufen Zelle A plus eine neue, vorab notierte Ersatzzelle. Fenster außerhalb 09:30 bis 16:00 ET, braucht W0-4 Teil A. Entry erst ab 18:15 ET (E8) bzw. 18:00 ET (FN). |
| 2 | H13 Zeit-Lücke × CL | 23 (2 2 3 2) | wie 1. Roll-Tage vorab als Liste ausnehmen (CL rollt monatlich), sonst misst die Nacht-Basis den Roll. |
| 3 | H13 Zeit-Lücke × GC | 23 (2 2 3 2) | wie 1. Roll-Tage ausnehmen (GC springt am Roll 30 bis 85 $). |
| 4 | H43 Regelwerk × NQ | 22 (1 3 3 2) | U 3 nur mit Kern-Zellen außerhalb 09:30 bis 16:00 ET oder an Buch-flat-Tagen, sonst U 1 und das Feld rutscht aus der Welle. Braucht W0-4 Teil A. |
| 5 | H43 Regelwerk × CL | 22 (1 3 3 2) | Settlement 14:28 bis 14:30 ET, EIA Mi 10:30. Läuft im US-Fenster, also schon heute bis Gate v4. |
| 6 | H43 Regelwerk × GC | 22 (1 3 3 2) | Settlement 13:29 bis 13:30 ET, LBMA. Läuft schon heute bis Gate v4. |
| 7 | H83 Zeit im Risiko × RTY | 21 (2 1 3 2) | U ungemessen, zuerst W0-2 (Nacht gegen Buch). Platz hängt an den Gewichten (in 4 von 24 Varianten). Braucht W0-4 Teil A. |
| 8 | H83 Zeit im Risiko × ES | 21 (2 1 3 2) | wie 7 (in 7 von 24 Varianten). |
| 9 | H83 Zeit im Risiko × YM | 21 (2 1 3 2) | wie 7 (in 8 von 24 Varianten). |
| 10 | H21 Markt-Steckbrief statistisch × ZW | 20 (1 2 3 2) | **Pflicht-Slot**, per Los aus 9 gleichauf (H13, H21, H83 auf 6E, ZS, ZW). Vollkontrakt über dem Größen-Budget: Schwankung je Trade in Stufe 0 prüfen, sonst nur als Signalquelle. 290 Bars je Tag, braucht W0-4 Teil A. Ketten-Power vorab (R10). Im Fenster 09:30 bis 15:55 ET gesehen (R11), ein verdeckter Teil nur außerhalb. |

Nächste nach Punkten: H13 auf YM, BTC, RTY und ES (21, wegen des Deckels 3 je Weg nicht in der Welle), dann H74, H50 und H46 auf CL sowie H83 auf ZS (20).

**Lesart:** Das ist das Ergebnis der Regel, keine Meinung über Märkte. ES, YM und RTY fehlen im NQ-Fenster wegen der gemessenen Rohbewegung (0,69 bis 0,91). Außerhalb davon sind sie ungemessen und stehen mit U 1 in der Reihung (Platz 7 bis 9). Nach W0-2 und W0-4 wird neu gereiht.

**Was das für dich heißt:** Treffer aus Welle 1 außerhalb von 09:30 bis 16:00 ET sind erst Kandidaten auf dem Papier. Ins Next-Buch können sie erst nach W0-4 Teil A (T02 Teil A), deshalb steht Teil A vor Welle 1. Läuft Welle 1 trotzdem früher, enden die Felder 1 bis 4 und 7 bis 10 bei Tafel und Querzeile als Hinweis: Sie zählen weder als G noch als Kandidat, Wiedervorlage-Bedingung „W0-4 Teil A fertig“. Gold ist mit 2 Feldern dabei, Weizen (ZW) mit dem Pflicht-Slot. Soja (ZS) und 6E lagen im selben Los gleichauf und fehlen nur durch das Los; sonst hängen dort 80 von 110 Feldern am Werkzeug und nur 1 Feld ist sofort testbar. Zinsen (ZN/ZB) fehlen, weil die Engine sie noch nicht rechnen kann (T13) und E8 und FundedNext sie nicht erlauben (FFN offen, T16). Das ist kein Urteil über diese Märkte. Nach T02 und T13 werden sie neu gereiht.

### 5.5 Budget der ersten Welle

- 10 Felder × 4 Zellen = **40 Tafel-Zellen**. Die Placebo-Felder der Eichung laufen in Welle 0 (mindestens 200, Kontrolle, nicht im Register).
- Unter Null gestartete Grids: erwartet 10 × 0,15 = **1,5**. Obergrenze 0,25 × 10 = **2 bis 3 Grids** × 24 = 72 Varianten. Höchstens rund **112 Register-Trials**.
- Zufalls-Kandidaten nach Gate v4 Stufe 1: 10 × 0,09 % bis 2,2 % = **0,01 bis 0,22**. Das ist eine Obergrenze und auf Nicht-Index-Märkten nicht gemessen, bis W0-1 läuft.
- Power je Feld an der Tafel (eine Zelle, 10,6 Jahre, eigene Rechnung): t ab 1,60 bei wahrem Sharpe 0,5 / 0,8 / 1,0 zu 51 / 84 / 95 %. Unter der Šidák-Schwelle t 3,0 wären es nur 9 / 35 / 60 %, deshalb ist Šidák ein Etikett und kein Tor (R9).
- Power der ganzen Kette bis ins Next-Week-Buch (stilisiert, Obergrenze, gerechnet am alten Buch 2,07, Kandidat bei 40 % der Buch-Schwankung): 39 / 75 / 90 % bei wahrem Sharpe 0,5 / 0,8 / 1,0, wenn der Vorteil flächig ist, real etwa mal 0,85.
- Wie das zu „nichts ausgrenzen“ passt: Jedes Feld kostet dasselbe. Breite kostet keine Trefferquote, nur Tiefe je Feld tut es.

---

## 6. Ideen weitergeben: die Vorlage zum Diktieren

### 6.1 Die sieben Felder (höchstens 5 Minuten)

| Nr | Feld | Was du sagst |
|---|---|---|
| 1 | **Woher** | Chart, Live-Tag, Regel der Börse/Firma, Termin, Text/Video/Paper, anderer Markt, wer muss handeln, unsere Beine, altes Urteil, Bauch, Daten |
| 2 | **Was** | der Satz, möglichst „wenn das passiert, kommt danach meistens das“ |
| 3 | **Wo und wann** | Markt (oder „alle“) und Uhrzeit, mit Zeitzone. ET oder die Uhr des Markts? |
| 4 | **Gleichzeitig oder danach** | Zustand oder Vorhersage? Wenn danach: bis wann? |
| 5 | **Beispiel-Tage** | 1 bis 3 Daten, dazu wenn möglich 1 Tag, an dem es nicht kam |
| 6 | **Ab wann lohnt es** | Größe (mit Einheit: Punkte oder Dollar je Micro) und Häufigkeit, grob |
| 7 | **Was ich NICHT meine** | welche Lesart ist deine? |
| (8) | Warum, optional | das Why. Es bekommt den Status „kausal vorab“, wenn es jetzt schon dasteht. |
| (9) | Sicherheit, optional | 1 bis 5 |

Nicht nötig: Stop, Ziel, Einstieg, Parameter, Strategie-Art. Die baut Claude als Plan, und du nickst ihn ab. Jedes Feld darf „weiß nicht“ heißen.

**Warum genau diese Felder:** Von 32 fertigen Regeln kamen 12 ins Buch oder Next-Buch (38 %, Band 23 bis 55 %), von 32 Stichwörtern keine (obere Grenze 11 %). Die Felder 3 bis 7 sind aus den 12 belegten Fällen von Informationsverlust abgeleitet, in denen genau diese Angaben fehlten. Dass die Vorlage hilft, ist damit eine plausible Vermutung, kein Befund: 0 von 32 gegen 12 von 32 ist eine Korrelation, viele Stichwörter wurden nie gerechnet (die Volumen-Liste mit 478 Zeilen zum Beispiel). Geprüft wird es an den nächsten 10 Ideen. Beispiel für den Verlust, ES gegen NQ (16.09.): „Divergenz vergleichen und handeln“. Gerechnet wurde ein Tor auf das Momentum-Bein, der SMT-Fehlausbruch wurde nie gebaut. Mit Feld 7 („ich meine den Fehlausbruch, kein Tor“) wäre es ein anderer Test geworden.

**Beispiel** (erfunden, ungeprüft): „1 Chart, ICT. 2 Wenn Gold in London das Asien-Hoch holt und binnen 15 Minuten wieder drunter schließt, läuft es bis New York Richtung Asien-Tief. 3 GC, Asien-Spanne 18:00 bis 02:00 ET, Abholen 03:00 bis 05:00 ET. 4 danach, bis 08:20 ET. 5 [Datum A, B, C], Gegenbeispiel [D]. 6 4 bis 5 Punkte je Fall (beim Micro rund 40 bis 50 $), zweimal die Woche. 7 nur der Fehlausbruch, beide Seiten. 8 weil über dem Asien-Hoch Stops liegen, die London abholt, danach fehlt der Nachschub. 9 Sicherheit 3.“ Das sind 90 Sekunden und ergibt genau einen Test.

### 6.2 Was Claude damit macht

| Schritt | Was | Zeit |
|---|---|---|
| 0 | Wortlaut wörtlich sichern, mit Datum | 1 min |
| 1 | Einordnen: H-ID (Wegweiser Abschnitt 4), Unabhängigkeit je Feld notieren (wechselt Markt, Fenster oder Quelle; gemessen oder nicht, nur Info), Testbarkeit (messbar / mit Handarbeit / nicht testbar, weil …), Machbarkeit nach R2 | Minuten |
| 2 | Schon gemessen? Register und Logbuch auf **genau diese Zelle** prüfen. Ein Nachbar-Urteil zählt nicht. | Minuten |
| 3 | Höchstens 3 Rückfragen (Tabelle unten) | 30 s für dich |
| 4 | **Plan zum Abnicken**, bevor eine Zahl gerechnet wird: Satzung nach R3 mit Why-Status (R4), 4 Kern-Zellen, Verzögerungs-Kontrolle (R5), Zählung (R6), Nachweisgrenze (0,76 je Markt), erwartete Grids unter Null, **erste Fassung als Pflicht (R12)** | gleiche Session |
| 5 | Workflow starten (Tabelle unten) | |
| 6 | Rückgaben, jede mit dem Satz „Was dieses Ergebnis nicht sagt“ | |
| 7 | Urteil ins Logbuch: Wortlaut, Beispiel-Tage, H-ID, Reichweite, Kategorie nach Todesurteil-Regel, Wiedervorlage **mit Bedingung**. Dazu Zeile im Beobachtungs-Tagebuch auf „gemessen #Nr“ setzen. | |

**Rückfragen, höchstens drei, die ersten offenen gewinnen:**

| Rang | Frage | Standard ohne Antwort |
|---|---|---|
| 1 | Gleichzeitig oder danach, bis wann? | Vorhersage bis Sitzungsende des Markts, Zustand als Info-Zeile |
| 2 | Welche Lesart: A, B oder C? | Claude rechnet **die billigste ehrliche Lesart** und kennzeichnet sie im Plan. Gerechnet wird erst, wenn du den Plan abgenickt hast. |
| 3 | In welcher Uhr gesehen? | Hauptzeit des Markts plus deine Uhr als zweite Kern-Zelle |
| 4 | Ab welcher Größe interessiert es dich? | **Käfig-Schwelle am Buch vom Lauftag:** wahrer s > S_B · (2r + v). Planzahl 0,5, das entspricht dem Käfig bei r 0 und v etwa 0,4, geschrumpft (1,20 × 0,4 = 0,48). Die weichere Sharpe-Hürde (bei r 0 und 40 % der Buch-Schwankung 0,23 geschrumpft bis 0,40 roh) steht als Info daneben. Weil die Mindestgröße über „empirisch-nichts-gefunden“ entscheidet (R7), gilt der Käfig. |
| 5 | Tag, an dem es nicht kam? | ohne Gegenbeispiel |

**Welcher Workflow:**

| Was vorliegt | Workflow |
|---|---|
| Beobachtung, Termin, Marktbau-Fakt, Fremdmarkt, Bauch | **Prämissen-Tafel nach der Stufenregel** (4 Kern-Zellen, Querzeile, R7 bis R9). Den Namen „Juli-Modus-Tafel“ gibt es weiter, das Lineal ist aber dasselbe. Die alte Runner-Prämisse liegt bei 28/57/68 % Power und wird nicht mehr als Standard benutzt. |
| fertige Regel mit 10+ Varianten, passt in einen Modus | ein-weg → Hypothesen-Bank → Runner-Job (Gate v4 Stufe 1) |
| fertige Regel mit weniger Varianten oder ohne Modus | Einzel-Lauf mit fester Einstellung (Gate v4 fixed) |
| Stichwort, Konzept | konzept-weg bis Wege-Karte, dann wählst **du** den einen Weg |
| Paper | paper-edge, danach von Hand in die Vorlage (Übergabe fehlt, T12) |
| Verlusttag, Buch-Lücke | H12/H15-Skript, Ausgabe ist ein Suchauftrag |
| altes Urteil | Reichweite prüfen, nur die ungemessene Zelle neu planen |

---

## 7. Ideen finden, wenn der Kopf leer ist

### 7.1 Die ehrliche Antwort auf „ich habe alles getestet, was ich weiß“

Für einen Ausschnitt stimmt das: Preis und Volumen auf NQ rund um die Eröffnung sind dicht gemessen. Aber so sieht das Register aus (69.587 Trials, Stand 13.10.): 92,4 % liegen auf Preis oder Volumen der vier Aktienindizes (mit Indexpaaren 95,2 %), 83,5 % in nur zwei Bausteinen (tsmom, maband), 74,1 % kamen vom Generator, nicht aus deinem Kopf. 40,5 % steigen zwischen 09:30 und 10:00 ein, 3,4 % vor 09:30, 1,1 % ab 14:30. Über Nacht gehalten wurde in 4 Trials. Ein anderer Markt war in 2,1 % das Signal (davon 4 Trials Zinsen oder Dollar), der Kalender in 0,8 %. Optionen, COT, Wetter, Lager: 0. Bei Markt mal Modus sind 193 von 279 Zellen leer. Der Generator kennt fest nur NQ, ES, RTY und YM.

Getestet wurde vor allem **ein Baukasten sehr oft, nicht dein Wissen.** Angekommen ist von dir wenig: Seit August waren 29 von 46 Übergaben Stichwörter, die sieben ICT-Begriffe haben im Vault 0 Notizen und 0 Tests, und der SMT-Fehlausbruch wurde nie gebaut. Ganze Startpunkte kamen nie vor: Terminkurve, Positionierung, Saisonalität, Verlusttag des Buchs, deine eigenen Trades.

Dazu kommt eine Grenze, die nichts mit dir zu tun hat: Auf 10,6 Jahren ist ein Bein unter 0,76 nicht von null trennbar. „0 von 9 Prämissen tragen“ passiert zu 29 bis 52 % auch dann, wenn eine echte 0,5er-Idee dabei war, und zu rund 80 %, wenn keine echt war. Die 9 Nullen sagen also kaum etwas darüber, ob noch etwas da ist. Sie schließen nur aus, dass mehrere starke Ideen dabei waren (Rechnung wie im Such-Budget, angenommen sind 2,5 % Fehlalarm je Idee).

Und ja, große Fonds suchen dauernd. Dabei ist Ausschuss der Normalfall: Chordia et al. testen 2,1 Millionen Strategien und behalten eine „bemerkenswert kleine Zahl“, bei Hou et al. scheitern 65 % von 452 Anomalien schon am einfachen Test. Ob du am Ende bist, kann gerade niemand beurteilen, weil dein Wissen nirgends als Liste steht. Genau das ist der nächste Schritt.

**Der Unterschied zu einem Fonds liegt nicht im Fleiß, sondern im Spielfeld.** Ein Fonds kann nicht, was du kannst: Effekte handeln, die bei 1 bis 10 Micros noch tragen, aber bei 1.000 Kontrakten den Preis selbst bewegen (H85), in dünnen Stunden und in kleinen Märkten. Du kannst nicht, was er kann: über Nacht oder Wochen halten, Optionen und Spreads handeln, um Termine herum handeln (News-Sperre bei FFN Funded), und deine Historie ist kürzer. Gesucht wird also dort, wo deine Grenze nicht stört und seine Größe stört: Intraday, kleine Effekte, Fenster mit wenig Volumen, mit der Kosten-Bremse als einziger harter Grenze.

**Was Profis machen, wenn Ideen ausgehen (belegt):** denselben Effekt in allen Märkten prüfen (Asness, Moskowitz, Hurst, Jensen/Kelly/Pedersen), eine Literatur-Pipeline im festen Takt mit Rahmen zum Ablehnen, eine Landkarte der Leute, die handeln müssen, kombinatorische Generierung nur als Ideenquelle, wobei jede Formel ein Trial ist. Der eigentliche Hebel gegen Selbstbetrug ist ein **vollständiger Plan vorab** (Brodeur et al.: Registrierung allein wirkt nicht, der volle Analyseplan schon). Eine veröffentlichte Routine großer Häuser für Ideen-Tagebücher gibt es nicht. Die Routine unten ist deshalb abgeleitet und keine Kopie.

**Wo du stehst:** Mit dem 6er-Buch sind es laut Wochenend-Prüfung 67 Monate bis 50k (vorher 79). Ein neues, unkorreliertes Bein mit wahrem Sharpe 0,5 in Viertel-Buch-Größe spart 2 bis 3 Monate, wenn die Backtests stimmen, und 15 bis 16 Monate, wenn sie um 42 % zu gut sind (Zahlen vom 13.10. auf anderer Rechenbasis, T05 rechnet sie neu). Wie viel ein Fund bringt, hängt also vor allem davon ab, ob die alten Beine halten. Deshalb lohnt die Suche gerade dann, wenn du dem Backtest nicht ganz traust.

### 7.2 Die Woche, rund 45 Minuten für dich

| Wann | Min | Was | Wege |
|---|---|---|---|
| jeden Handelstag vor 09:30 ET | 2 | eine Zeile Vorhersage ins Tagebuch, mit Zeitstempel | H65 |
| jeden Handelstag nach Schluss | 2 | wenn dich etwas überrascht hat: eine Zeile | H38, H39, H15 |
| Montag | 10 | schlimmste und beste Buchtage: Was lief in den anderen Märkten, in deren Uhr? | H12 bis H15, H52 |
| Mittwoch | 10 | ein fremder Markt, drei Zufallstage, im Replay nur aufschreiben | H44, H45, H50, H66 |
| Freitag | 10 | ein Text: 3 Abstracts, eine Börsenmitteilung oder ein Praktiker-Video | H93, H94, H75 bis H77 |
| Sonntag nach Wochenend-Prüfung | 10 | Termin-Blatt der Woche über alle Märkte, zu 2 Terminen deine Erwartung | H88 bis H90, H95, H36, H37 |
| monatlich | 15 | 5 Fragen der Wissens-Inventur | H58, H59, H62, H63, H71 |

Ohne deine Zeit liefert Claude je Gruppe das Rohmaterial: Trade-Listen der Beine, das Buch-Profil, Landkarten je Markt, Wiedervorlagen mit eingetretener Bedingung, das Termin-Blatt, Markt-Steckbriefe, Abdeckungs-Karte und die Liste nie bewegter Stellschrauben, dazu 3 Maschinen-Vorschläge pro Woche. Jeder Vorschlag ist ein Trial und läuft durch dieselbe Vorlage. Du wählst aus, Claude rechnet nur das Gewählte.

**Beobachtungs-Tagebuch** (Vorschlag `Inbox/Beobachtungs-Tagebuch.md`, nicht angelegt):

```
Datum Zeit | Art (B/V/T/F/X/L/G) | Markt | Uhr/Fenster | Was | Z oder V bis wann | Beispiel | Sicherheit | Vorab? | Status
```

Art: **B** Beobachtung, **V** Vorhersage, **T** Termin, **F** Fakt aus Regelwerk, **X** Text, **L** Live-Tag, **G** Gefühl. Z heißt Zustand, V Vorhersage.

Die Spalte „Vorab?“ macht aus deinen Vorhersagen nach ein paar Monaten einen Datensatz, der nicht durch Rückblick verfälscht ist (H65, H42).

### 7.3 Wissens-Inventur: 40 Fragen (8 Sitzungen à 5 Fragen, per Diktat)

„Weiß nicht“ ist eine gültige Antwort. Gefragt wird nach Situationen, nicht nach Strategien.

**A. Chart-Zeit (H57, H58, H60, H61, H69)**
1. Welche drei ICT-Begriffe hast du am häufigsten „stimmen“ sehen? Je einen Tag dazu.
2. Vortages-, Asien- oder London-Hoch abgeräumt: Was passierte in den nächsten 30 Minuten typisch, und woran hast du den untypischen Fall erkannt?
3. Gibt es 5 Tage, die sich gleich angefühlt haben?
4. Welche Kerze nennst du „sauber“?
5. In welchem Markt außer NQ hast du länger geschaut, und was ist dir aufgefallen?

**B. Orderflow (H46 bis H48)**
6. Wann zeigte Footprint oder Delta vor dem Preis, dass eine Bewegung nicht hält? Uhrzeit, Markt?
7. In welchen Stunden sagte dir Orderflow nichts?
8. Was sahst du, wenn ein Großer in Scheiben handelte, und zu welchen Uhrzeiten?

**C. Optionsflow und Halten (H56, H83, H84)**
9. Was aus Gamma, Vanna oder täglichen Verfällen hast du am Chart wiedererkannt?
10. Wann hältst du ungern eine Position, und was passierte, wenn du es doch getan hast?

**D. Uhr und Regeln (H43 bis H45, H51)**
11. Welche Eröffnung, Pause oder Abrechnung kennst du, und was passiert in den 10 Minuten danach?
12. Welche Börsen- oder Prop-Regel hat dich in einen Trade gezwungen oder aus einem raus?
13. Ist dir etwas in den Wochen mit ungleicher Zeitumstellung aufgefallen, oder an Feiertagen nur eines Handelsplatzes?

**E. Termine (H88, H89, H92, H36, H37)**
14. Welche Termine hast du gemieden, welche gesucht?
15. Was passiert am Tag vor einem großen Termin und in der ersten Stunde danach?
16. Ist dir an einem Roll-, Verfalls- oder Monatsendtag etwas Unerklärliches aufgefallen?

**F. Andere Märkte (H52 bis H54, H105)**
17. Auf welchen anderen Markt schaust du, um NQ zu handeln? Wann hilft er, wann nicht?
18. Welcher Markt läuft vor, welcher folgt, mit welchem Abstand?

**G. Wer muss handeln (H95, H97, H100)**
19. Wo liegen die Stops von Retail-, ICT- und Prop-Händlern, und hast du gesehen, wie sie ausgelöst wurden?
20. Was machen Prop-Händler vor der Flat-Zeit, am Freitag, nach dem Tagesziel?
21. Wer muss zu festen Zeiten handeln, egal zu welchem Preis?

**H. Live mit den Konten (H38 bis H40, H14, H15)**
22. Welcher Live-Tag seit Juli hat dich am meisten überrascht? Was war am Morgen anders?
23. Wo weichen die Fills am stärksten ab?
24. Woran erkennst du Tage ohne Strecke früh, falls überhaupt?
25. Hat dir ein Fehler einmal ein auffälliges Ergebnis gezeigt?

**I. Eigene Spuren (H59, H62, H63, H67)**
26. Welche Spuren gibt es noch (Screenshots, Layouts, Journale, Exporte)? Wo liegen sie, aus welchem Zeitraum?
27. Wo wirst du immer wieder ausgestoppt, kurz bevor es in deine Richtung läuft?
28. Wann fasst du nichts an, und woher kommt diese Regel?

**J. Selbstverständliches und Einspruch (H109, H70, H71, H33)**
29. Was an unserem Buch hältst du für selbstverständlich (flat 15:55, nur 09:30 bis 16:00, ein Trade am Tag, Minuten-Kerzen)?
30. Welchem Urteil im Logbuch glaubst du nicht, und welcher Tag spricht dagegen?

**K. Andere Händler, Tagestypen, kleine Größe (H72 bis H81, H85)**
31. Aus welchem Kurs, Buch oder Video kennst du eine komplette Regel (Name, Quelle)? (H75, H76)
32. Welche Daumenregel „weiß doch jeder“ hältst du für falsch oder für richtig? (H77)
33. Kennst du jemanden, der einen anderen Markt handelt oder handeln muss (Landwirt, Treasury, Broker-Desk)? (H78, H79)
34. Wessen Live-Calls oder Trade-Listen mit Zeitstempel hast du? (H80) Gibt es eine Geschichte oder einen Vergleich, die dir zu einem Markt immer einfällt? (H81)
35. Welche drei Tagestypen unterscheidest du, und ab welcher Uhrzeit erkennst du sie? Wie sieht die Bewegung für dich aus, wenn du sie als Bild beschreibst? (H72, H73, H74)
36. Was kannst du mit 1 Micro, das ein Fonds wegen Größe oder Auftrag nicht kann? (H85)

**L. Jahreslauf, Akteure, Positionierung, Text (H98, H99, H101, H104, H106, H107)**
37. Welche Saison oder welchen Erntetermin kennst du aus Gold, Öl oder Getreide? Hast du je Wetter oder Lagerdaten verfolgt? (H99, H101, H106)
38. Welche Notenbank- oder OPEC-Phase hast du im Chart gesehen? (H104)
39. Wann hast du COT oder offene Kontrakte angeschaut, und was ist dir aufgefallen? (H98)
40. Welche Schlagzeile oder welches Statement hat einen Markt bewegt, ohne dass ein Termin anstand? (H107)

---

## 8. Was an Werkzeug und Daten fehlt (angelegt am 28.10.2026 als AP458 bis AP479, Epic AP457, alles im Backlog)

Sortiert nach Nutzen. Die Zahl in Klammern ist die Zahl der Landkarten-Felder, die das Ticket öffnet (Zählung vom 13.10.).

| Nr | Ticket | Nutzen | Wer |
|---|---|---|---|
| T01 (AP458) | **Vorlage mit 7 Angaben + Beobachtungs-Tagebuch + Wissens-Inventur (40 Fragen)** (179 Felder) | öffnet alle Mensch-Wege und dein Wissen; Prüfung an den nächsten 10 Ideen | Claude + Max |
| T02 (AP459) | **Werkzeug-Paket Markt-Uhr** (W0-4). **Teil A vor Welle 1:** Fenster in Runner, Controls und Nullmodellen, ohne 390 Minuten. **Teil B vor Welle 2:** Generator, Bank, 9 RTH-feste Modi, Klon-Weg, Generator-Märkte aus Konfiguration (93 Felder) | ohne Teil A enden 8 von 10 Feldern der Welle 1 an der Tafel; mit Teil B werden 6E, ZS und ZW überhaupt testbar | Entwickler, Pipeline-Prüfer, Golden Master |
| T03 (AP460) | **Eichung der Stufenregel** (W0-1): mindestens 200 Placebo-Felder auf GC, CL, 6E, ZS, ZW, BTC, Power per Signal-Einbau, eigene Beine nur als Plausibilitätsprobe | ohne Eichung sind alle Power- und p0-Zahlen Obergrenzen | Statistiker, Backtest-Runner |
| T04 (AP461) | **Tafel-Standardeingang ohne scipy** (die Tafel-Bibliothek bricht am PC ab), mit Querzeile nach R8, Verzögerungs-Zelle nach R5, Register-Typ Tafel/Grid (99 Felder) | ersetzt 6 Handskripte in 18 Tagen | Entwickler |
| T05 (AP462) | **Buch-Profil und Steckbrief für das 6er-Buch neu** (W0-3): Liste im Kasten „Stand 27.10.“ | alle Zahlen in Abschnitt 1 bis 2 sind vom 13.10. | Claude + Mathematiker |
| T06 (AP463) | **Erste Fassung automatisch:** das Hochstufen ins Next-Buch schreibt den Eintrag mit, Satzungs-Vorlage mit Pflichtfeldern (Why-Status, erster Blick, Hash) und Sperre „kein Job ohne Satzung“ | Blocker aus der Methoden-Prüfung | Entwickler |
| T07 (AP464) | **Walk-Forward-Start** fest übergeben (R13) | sonst gilt auf Märkten mit Start 12/2015 „6 von 10“ | Pipeline-Prüfer |
| T08 (AP465) | **Unabhängigkeit messen** (W0-2): Nacht ES, YM, RTY gegen das Buch, BTC-Volumen außerhalb RTH, Rohbewegung 6B, ZN, ZB, FDAX gegen NQ | U in der Reihung bisher ungemessen; Platz 7 bis 9 der Welle hängen daran | Claude |
| T09 (AP466) | **Wiedervorlage nach Bedingung** statt nur nach Datum | jedes „unentscheidbar“ und „nicht testbar, weil“ kommt von selbst zurück | Entwickler |
| T10 (AP467) | **Termin-Dateien** EIA, WASDE, COT, Crop Progress, Treasury-Auktionen, EZB, LBMA, Index-Roll | öffnet Termin- und Ursache-Wege auf allen Märkten | Claude |
| T11 (AP468) | **Roll-Maske / Roll-Adjuster** für GC, CL, 6E, ZS, ZW (18 Felder direkt, viele indirekt; Welle 1 Nr. 2 und 3 brauchen eine Roll-Tage-Liste) | Vortag, Gap und Nacht auf Nicht-Index | Entwickler |
| T12 (AP469) | **Übergabe paper-edge zu Satzung**, Eingangsfilter „Index-Fokus“ entkoppeln | Paper-Weg ohne Vorurteil | Claude |
| T13 (AP470) | **Engine-Tabellen 6B, ZN, ZB, FDAX**, Gebühren gegen Primärquelle (64 Felder 6B) | vier Märkte mit Daten werden testbar | Entwickler |
| T14 (AP471) | **Modus „Auslöser in A, Handel in B“** mit eigener Uhr je Seite (60 Felder) | Fremdmarkt als Auslöser, nicht nur als Tor | Entwickler |
| T15 (AP472) | **Einzelkontrakt-Loader** aus dem NT8-Export (52 Felder) | Terminkurve, Roll, Lebensende | Entwickler |
| T16 (AP473) | **FFN-Produktliste per Support** (129 Felder P), Text in Abschnitt 9 | ZN/ZB, FDAX, Micro-Ag, Silber, Kupfer, M6E handelbar ja/nein | **Max** |
| T17 (AP474) | **Daten:** Databento 2010 bis 2015 (Kostenabfrage vorher) für H110 und verdeckte Jahre. NT8-Export der 7 fehlenden Marktgruppen und Softs (866 Felder D). Entscheidung zu den Index-Dateien (Ende 10.08. gegen NT8 bis 18.09.). | mehr Jahre sind der einzige Hebel auf die Nachweisgrenze (16,2 Jahre → 0,62) | Max entscheidet, Claude fragt Kosten ab |
| T18 (AP475) | **Reichweite-Felder** in Ideen-Liste und Landkarte (G mit N, Wiedervorlage-Bedingung, Zusatz /K, Mehrtages-Form P) | „tot“ wird ein Objekt mit Rand | Claude |
| T19 (AP476) | **alpha-scout und familien-scout** auf Zeit bis 50k umstellen: kein Frequenz-Bonus, kein „unter 3 Punkten tot“, kein „HF vor LF“; Mindestgröße der Bank (10 bis 400 Varianten) um einen Tafel-Pfad ergänzen | Vorab-Sortierung im Werkzeug entfernen | Claude |
| T20 (AP477) | **Pflege:** Research-Cache Zeile 793 und Gold-Karte Randbedingung 11 (Zinsen bei E8 nicht handelbar), Micro-Ag und Micro Ultra Treasuries nachtragen. Sechs Altdateien aus dem ersten Lauf im Engine-Ordner aufräumen. Fehlalarm der Sperre bei Scratch-Skripten prüfen. Overrides aus `p6_neu.py` in `p3_build.py` übernehmen und die volle Landkarte neu bauen. | Konsistenz | Claude |
| T21 (AP478) | **Kosten-Messung je Markt (neu):** Databento-Kostenabfrage für Kursbuch-Spitze (MBP-1) und Trades, 3 Monate je Markt (GC, CL, 6E, ZS, ZW, ZN, MBT), daraus mittlerer Spread und Rutschen je Uhrzeit. Parallel H41 Probe-Handel auf Sim mit 50 Orders je Markt. | ersetzt die Pauschale 1 bzw. 2 Ticks in R2 und in der Kosten-Bremse; öffnet H46 bis H48 außerhalb NQ/ES | Max gibt die Kostenabfrage frei, Claude rechnet |
| T22 (AP479) | **Anhang-Code (neu):** Banner über jeder Anleitung, Block-IDs `^h01` bis `^h110`, Korrekturen aus 4.2 an Ort und Stelle; volle Landkarte als zweite Anhang-Notiz in den Vault | Anleitungen widersprechen dem Hauptteil nicht mehr, Links springen genau | Hauptsession (Vault-Schreibrecht) |

---

## 9. Die ersten Schritte

| Nr | Wer | Was |
|---|---|---|
| 1 | **Max** | (a) Erledigt am 28.10.: E1 bis E10 entschieden (Abschnitt 10). (b) Schick zwei Nachrichten (5 Minuten). An den FFN-Support: „Which individual futures can I trade on my FFN 150k account? Specifically: ZN, ZB, FDAX, micro ag (MZC/MZW/MZS), silver, copper, M6E.“ An den E8-Support: „Can I confirm that holding a futures position from 18:15 ET until the next morning within the same trading day is allowed, and at what time do the daily loss limit and drawdown reset?“ |
| 2 | **Max + Claude** | Erste Sitzung Wissens-Inventur, 5 Fragen aus Block A, per Diktat (15 Minuten). Start: Schreib Claude „Inventur Block A, stell mir Frage 1“. Claude fragt einzeln, du antwortest per Diktat, Claude schreibt mit. Danach das Beobachtungs-Tagebuch anlegen (T01). |
| 3 | **Claude** | Welle 0 Messung: Buch-Profil für das 6er-Buch neu (T05) und Unabhängigkeit messen (T08). Danach Reihung neu rechnen (`p6_neu.py`). |
| 3b | **Max, dann Claude** | Kostenabfrage für Kursbuch- und Trade-Daten freigeben (T21, nur Abfrage, gekauft wird erst nach Preis). Parallel H41 auf Sim, wenn du Lust hast. |
| 4 | **Statistiker + Backtest-Runner** | Eichung der Stufenregel mit mindestens 200 Placebo-Feldern und Signal-Einbau (T03), über die Rechen-Bremse, Box nur in Absprache. |
| 5 | **Entwickler + Pipeline-Prüfer** | Werkzeug-Paket Teil A (Fenster durchreichen, T02 Teil A) und Walk-Forward-Start (T07) **vor Welle 1**. Erst wenn 3, 4 und Teil A fertig sind: Welle 1 mit 10 Feldern, jede mit Satzung und Eintrag der ersten Fassung. Teil B vor Welle 2. |

---

## 10. Grenzen dieser Analyse und offene Entscheidungen bei Max

> [!warning] Auflagen des verdict-auditor (Urteil: trägt mit Auflagen)
> Das hält: der Flaschenhals (Rechnung vom 13.10. gilt), die Formeln im Steckbrief (Tabellenwerte nachgerechnet) und die Summen der Landkarte. Nicht getragen hat der Entwurf die eigene Reihenfolge-Regel. Die Auflagen und wie sie umgesetzt sind:
> 1. **Fenster zählt als Unabhängigkeit** (Blocker): umgesetzt, U je Feld (Markt und Fenster), 40-%-Bedingung gestrichen, neu gereiht (5.2). Abweichung: Ungemessene Nacht-Paare bekommen U 1 statt 2 (Leser-Fassung, begründet in 5.2, Entscheidung E9).
> 2. **Gleichstand per Alphabet:** umgesetzt, Los mit Seed 20261028; Sensitivität neu gezählt (Platz 1 bis 6 robust, 7 bis 10 nicht).
> 3. **R9 halbiert die Power:** umgesetzt, Grid bei t ab 1,60, Šidák nur als Etikett über die Welle.
> 4. **Eichung W0-1 kann nicht liefern:** umgesetzt, mindestens 200 Placebo-Felder, Signal-Einbau, eigene Beine nur als Plausibilitätsprobe.
> 5. **„per Bauart unabhängig“ zu stark:** umgesetzt in Abschnitt 0 und 2 (gemessen ist Vormittag gegen Nachmittag, für die Nacht nur die rohe NQ-Position; gemeinsamer Tagestyp 69 bis 75 %).
> 6. **BTC schon gemessen (#188):** umgesetzt (Abschnitt 2, R2: E8 ja, FN nein, ab 05/2021, Nachweisgrenze 1,07, 6,40 $). W0-2 misst stattdessen den BTC-Nachtanteil.
> 7. **6E-Felder ohne Größen-Auflage:** umgesetzt als Regel in R2 und Regel 12 (/K); 6E steht nach der Neureihung nicht mehr in Welle 1, die Regel greift für ZW auf Platz 10.
> 8. **Nacht-Felder enden an der Tafel:** umgesetzt, W0-4 Teil A vor Welle 1, und 5.4 sagt, was passiert, wenn Welle 1 früher läuft.
> 9. **Landkarte nicht auf Stand:** umgesetzt (#184, #189, #190, LD01; Stand Logbuch bis #190).
> 10. **Mindestgröße zu weich:** umgesetzt, Käfig-Schwelle als Standard (Rückfrage 4, Banner für H01).
> 11. **X auf Zellebene:** umgesetzt (Abschnitt 3).
> 12. **LD01 stützt „anderer Platz“:** umgesetzt (Abschnitt 2, H06).
> 13. **R11 für CL zu vorsichtig:** umgesetzt.
> 14. **Anhang widerspricht Hauptteil:** umgesetzt als Kasten oben, Tabelle 4.2 und Auflage an den Anhang-Code (T22). Die Anleitungen selbst ändert dieser Lauf nicht.
> 15. **7-Felder-Vorlage ist Hypothese:** umgesetzt (Abschnitt 0 Satz 5, 6.1).
> 16. **0 von 9 statt 0 von 6:** umgesetzt (7.1).

**Grenzen:**
- Abschnitt 1 bis 3 stehen auf dem Buch vom 13.10. (mit RTY-Gap, Gebühr 1,02 $). Für das 6er-Buch ist nichts davon neu gemessen (T05).
- Alle Power-, Durchlass- und Budgetzahlen sind stilisiert (127 Monate, normalverteilt, ohne Trim und Kosten-Stress) und deshalb Obergrenzen. Die Stufenregel ist nicht geeicht.
- Die neue Reihung (5.2, 5.4) ist in diesem Lauf gerechnet und von keinem Gegenleser mehr geprüft. Sie hängt an der Setzung, wie ungemessene Nacht-Paare zählen (E9), und an der Testbarkeit der Fenster-Felder (W0-4 Teil A).
- Die Statuszuordnung der Landkarte ist regelbasiert. Kennt jemand ein Urteil zu einem Feld, das hier T oder W heißt, kippt das Feld. Die volle Matrix in `p3_landkarte.md` hat die Nachträge dieses Laufs noch nicht (T20).
- Die Korrelation von Regel-Ergebnissen **zwischen Märkten** ist nicht gemessen. Davon hängt ab, ob 9 Märkte in der Querzeile wie 9, 5 oder 3 zählen.
- Die Monats-Tabellen hängen an der Welt (43, 69 oder über 120 Monate). Der zweite Rechenweg liegt auf ±40 %. Die Wochenend-Prüfung rechnet auf anderer Basis (67 bzw. 79 Monate).
- Rutschen ist außerhalb von MNQ nicht gemessen. Bei großen Ticks entscheidet es fast alles (T21).
- Dein Wissen ist in keiner Zahl dieser Analyse enthalten, weil es nirgends steht.
- Die Anleitungen stammen von mehreren Agenten. Ihre Lücken-Listen enthalten Doppelungen und teils überholte Pfad-Angaben. Es gelten R1 bis R16, Tabelle 4.2 und die Pfade im Anhang.
- Zuordnung im Buch: LD01 = H06 (VIX-Filter als Tagesauswahl auf dem PB3-Mechanismus), OpEx = H90.

**Entscheidungen (Max, 28.10.2026, per Abfrage in der Playbook-Session):**

| Nr | Frage | Vorschlag | Entscheidung Max 28.10. |
|---|---|---|---|
| E1 | Stufenregel (4 Zellen, t ab 1,60, Grid bis 24, Šidák als Etikett nach R9) **vorläufig** freigeben, bis die Eichung (T03) da ist? | ja, mit dem Vermerk „ungeeicht“ in jedem Urteil | übernommen |
| E2 | Zählung der Tafel-Zellen: alle gerechneten Zellen mit Handelsregel **ins Register** (Pipeline-Prüfer) oder **nur in N der Satzung** (Strategie-Prüfer)? | ins Register mit Typ Tafel. Dann misst die Kampagnen-Bilanz alles gleich. | übernommen |
| E3 | Gewichte der Reihung 3/2/3/2 (Bedarf, Unabhängigkeit, Testbarkeit, Kosten) | übernehmen. Die Gewichte sind eine Setzung: Platz 1 bis 6 hängen nicht daran, Platz 7 bis 10 schon. | übernommen |
| E4 | Welle 0 (Eichung, 6er-Profil, Unabhängigkeit messen, Werkzeug Teil A) vor Welle 1, Teil B vor Welle 2 | ja | übernommen |
| E5 | Datenkauf 2010 bis 2015 (Databento, Preis vorher per Kostenabfrage) | Kostenabfrage freigeben, kaufen erst nach Preis | **jetzt nicht** (keine Kostenabfrage 2010 bis 2015) |
| E6 | Index-Dateien (Ende 10.08.) durch NT8-Versionen ersetzen, offen seit 19.09. | entscheiden, weil es den Herkunftsmarkt aller Beine betrifft | **erst prüfen lassen**, nichts tauschen (Ticket AP480) |
| E7 | Nacht-Halten: Innerhalb des Handelstags ist es bei E8 (ab 18:15 ET) und FundedNext (ab 18:00 ET) erlaubt, über den Tagesschluss nicht (Firm-Regeln, 01.10./12.10.). Bei E8 folgt das Halten bis in den Morgen aus der Regel, wörtlich bestätigt ist es nicht. Offen ist die E8-Reset-Zeit für Drawdown und Tageslimit. | nur diese zwei Punkte in einer Nachricht an E8 (Text in Schritt 1) | übernommen |
| E8 | Märkte testen, die heute kein Konto handeln darf (ZN/ZB, FDAX, Softs) | testen ja, als Signalquelle sofort. Ins Buch erst mit Erlaubnis. | übernommen |
| E9 | Unabhängigkeit nachts: nur Gemessenes zählt (ungemessene Nacht-Paare U 1) oder jede Nacht zählt als unabhängig (U 2, Fassung des verdict-auditor)? | nur Gemessenes, bis W0-2 die Nacht-Reihen von ES, YM, RTY gemessen hat. Danach erledigt sich die Frage durch Messung. | übernommen |
| E10 | Kostenabfrage Kursbuch- und Trade-Daten für 7 Märkte (T21) | freigeben, nur Abfrage | übernommen (nur Kostenabfrage, AP478) |

---

## Anhang: Dateien und Quellen

**Berichte der Bestandsaufnahme** (`C:\Users\maxlk\Projects\trading-data\engine\_scratch_alphaplaybook_1310`):
- `p1_buch_profil.md`: Korrelation, Belegung, Faktor, effektive Wetten (Rohdaten `p1/`)
- `p1_such_budget.md`: Nachweisgrenze, Stufenregel, Budget (`such_budget/sb_calc*.out`)
- `p1_steckbrief.md`: Formeln des fehlenden Beins (`stk/`)
- `p1_daten_inventar.md`, `p1_abdeckung_register.md`, `p1_abdeckung_friedhof.md`, `p1_ideen_audit.md`, `p1_werkzeug_inventar.md`
- `p1_extern_methodik.md`, `p1_extern_marktstruktur.md` (je mit fertigem, nicht eingetragenem Research-Cache-Block)
- `p3_landkarte.md`, `p3_landkarte.json`, `p3_build.py`: Matrix 2.200 Felder (Stand vor diesem Nachtrag)
- `p6_neu.py`, `p6_neu.json`: Nachträge der Landkarte (Softs, #184, #189, #190, LD01; 2.310 Felder), Reihung mit U je Feld, Los, Sensitivität (dieser Lauf)
- `p3_uebergabe.md`: Vorlage, Ablauf, Routine, ursprünglich 30 Fragen
- `p5/rerank.py`, `p5/rerank.json`: Reihung des Entwurfs (überholt durch `p6_neu.py`)
- Einzelrechnungen der Anleitungen: `h04/` bis `h29_calc*`, `h*_anleitung.md`
- `ENTWURF.md`: Fassung vor den Gegenlesern (unverändert)

**Lauf auf der Box:** `C:\Users\maxlk\Projects\trading-data\engine\_scratch_alphaplaybook_1310\box_run` (Agent-Ergebnisse unter `ergebnisse/`, Anleitungen H01 bis H110 als JSON, Logs unter `logs/`, Nachrechnungen der Gegenleser `va_power.py`, `va_sens.py`, `va_sens2.py`).

**Vault-Quellen:** Daily Note 2026-10-16 (Ergebnis 6E/ZS/ZW-Probe), [[Wochenend-Prüfung 24.10.2026]], [[Strategie-Logbuch]] (#163, #165, #179, #181, #184, #186 bis #190, Tabelle LD01), [[Firm-Regeln je Konto]], Ressourcen/Todesurteil-Regel, Projekte/Latte-Audit (25.09.2026), Projekte/Friedhof-Analyse (17.09.2026).

### Für Claude: Technik zu R1 bis R16

- **R1:** Buch-Stand aus `book_state.json` (nur lesen). Bein-Namen im Buch: `NQ_OPEXMOM_fv4` (OpEx), `NQ_LD01_vix16_fv4` (LD01).
- **R6:** Buchung über `engine/scratch_register.py`, das `registry_pending_add` in `engine/discovery/discovery_lib.py:676` ruft. Schlüssel `H<id>|markt|zelle|nn`, `source=H<id> <Datum>`, Typ `tafel` oder `grid`. Nie `registry.json` direkt.
- **R12:** Eintrag in `engine/book_erstfassung.json` nach `_doc`: `art config` = Basis-Config des ersten Jobs dieser Linie; bei Grid ohne feste Config `art wf` mit `sr`, `years`, `ci90` aus Stufe 1; Pflichtfeld `erster_blick`. Eintrag über `engine/erstfassung.py` aus der Hauptsession; `discovery/promote_next.py` schreibt noch nicht mit (T06).
- **R13:** `discovery_lib.py:2058` nimmt sonst das erste Datum; im Job-JSON `start=2016-01-01` setzen.
- **R14 und W0-4 Teil A:** Fenster heißt im Code `session_start`/`session_end` (AP197); 0 Treffer in `discovery_lib.py`, `discovery_runner.py`, `controls.py` (Stand 28.10.); `results/grain_open_probe_ZS.meta.json` lief bewusst ohne.
- **Rückfrage 4:** Die alten Werte aus `prescan_gross` (812 $) gelten nicht mehr.
- **Register-Statistik 7.1:** Generator-Märkte fest in `job_generator.py` Z. 50/51.
- **Werkzeug-Pfade:** `tafel_lib.py`, `rechen_bremse.py`, `scratch_register.py`, `erstfassung.py` in `engine/`; `inbox_tool.py`, `promote_next.py` in `engine/discovery/`; `receipt.py`, `work_types.py` im Vault unter `.claude/hooks/`. Alle „fehlt“-Zeilen zu diesen Dateien in den Anleitungen sind überholt. Skripte mit mehreren Prozessen nur über `rechen_bremse.py`.
- **Reihung:** `p6_neu.py` liest die Definitionen aus `p3_build.py`, Overrides für H52 × GC, H57 × GC, H06 × NQ, Zeile `SOFT`, Variante `leser` ist die Hauptfassung, Seed 20261028.
