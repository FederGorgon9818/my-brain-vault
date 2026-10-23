---
date: 2026-10-23
tags: [projekt, cfd, prop-firm, krypto, bitcoin, tempo_plan, recherche]
status: Bericht fertig, Entscheidungen bei Max
tickets: [AP399, AP422]
---

# 💱 CFD-Check (23.10.2026): können wir NAS100 und BTC auf CFD-Props handeln, und bringt es Zeit bis 50k?

Auftrag Max 23.10.2026 vormittags, gefahren auf der Box ohne Mensch am Bildschirm (Session c97e7af8, 09:36 bis ca. 11:30 Boxzeit). Eigenes CFD-Buch, nicht mit dem Futures-Buch verrechnet: ein zusätzliches Konto neben der laufenden Flotte. Futures-Daten (NQ, BTC) als Kurs-Ersatz, Kosten durch die CFD-Kosten der Firma ersetzt. **Kein Gate v4, keine neue Suche, keine neuen Varianten.** Einzige Frage: verkürzt ein CFD-Konto die Zeit bis 50k?

Verwandt: [[Nightrun BTC 23.10.2026]], [[Firm-Regeln je Konto]], [[Research-Cache]] (neuer Abschnitt „CFD-Prop-Firmen für NAS100/BTC"), [[Eval vs. Funded Neubewertung (18.10.2026)]], [[Strategie-Logbuch]] #188.

> ## 🧭 Kurzfassung für Max
>
> **1. Die vier NQ-Beine auf einem CFD-Konto: ja, das verkürzt die Zeit bis 50k. Die Richtung ist sicher, die Größe nur auf etwa Faktor 2 genau.** Mit k1 (1 MNQ-Äquivalent je Bein) und angenommenen 1,5 Punkten NAS100-Spread, Backtest-Edge: FTMO 2-Step 100K **rund 12 Monate schneller**, E8 One 100K **rund 11**, FundedNext Stellar 2-Step 25K **rund 6** (Flotte ohne CFD: Median 78,7 Monate; in 97 bis 98 % der Welten ist die Flotte mit FTMO oder E8 schneller). Mit geschrumpfter Edge (Drift x 0,58 auf beiden Büchern) bleibt es ein Ja, aber kleiner: FTMO **−6,4**, E8 **−5,4**, FN **−2,0** Monate (Mittel bis zur 120-Monats-Kappe), und die Chance, 50k in 10 Jahren zu erreichen, steigt von 18,7 % auf 38,3 % (FTMO) bzw. 37,3 % (E8). Nulldrift-Zwilling überall 0,0 %. Die Monte-Carlo-Fehlerbalken (± 0,3 bis 0,6) sind dabei klein gegen die Unsicherheit der Edge selbst, deshalb nenne ich Spannen statt einer Zahl.
>
> **2. BTC auf CFD: nein.** Die BTC-Variante aus dem Nachtlauf bringt allein auf jedem CFD-Konto nichts (+0,1 bis +0,7 Monate, also leicht langsamer, weil das Konto die Prüfung praktisch nie besteht). Zusammen mit den NQ-Beinen spart sie zusätzlich 0,6 bis 1,2 Monate (FN 0,61, FTMO 0,70, E8 1,15), das ist kleiner als das, was die unbekannten Spreads verschieben können.
>
> **3. Das Ja hängt an einer Zahl, die keine Firma veröffentlicht: dem NAS100-Spread.** Break-even liegt bei rund **9,6 Punkten (E8), 9,8 (FTMO), 11,2 (FN)**. Üblich sind bei CFD-Brokern 1 bis 2 Punkte zur US-Session, das ist aber nicht gemessen. Bevor irgendwas gekauft wird, muss der Spread auf einem Demo-Konto gemessen werden.
>
> **4. Was das Ja eigentlich ist:** ein weiteres Konto, das dasselbe Buch handelt. Der Gewinn kommt aus mehr arbeitendem Kapital, nicht aus etwas CFD-Eigenem. Ein höherer Kaufdeckel für die Futures-Flotte allein bringt dagegen **0,0 Monate** (Kontrolllauf), das Budget ist also nicht der Engpass. Ob ein weiteres Futures-Konto dasselbe günstiger leistet, habe ich nicht gerechnet (nicht beauftragt).
>
> **5. Technik: geht, aber nur mit Eigenbau.** NT8 kann nicht direkt an MT5/cTrader. Kopierer von NT8 zu MT5 sind Beta oder falsche Richtung. Der saubere Weg ist ein **eigener MQL5-EA (oder cBot in C#)** in einer eigenen MT5-Portable-Installation, ohne Berührung zu NT8. Das ist ein Port der vier Beine mit Paritätsprüfung, mehrere Tage Arbeit.
>
> **6. Firmen:** FTMO und E8 (CFD-Linie) sind im Rennen. FundedNext nur bis 25K (EA und VPS ab 50k verboten), mit 3-%-Risikoregel im Funded und widersprüchlichem Hebel. The5ers nur mit schriftlicher Freigabe. Alpha Capital raus (Primärzitat: keine unbeaufsichtigten EAs), FundingPips wahrscheinlich raus (kein VPS). FFN hat kein CFD, erlaubt aber MBT/MET laut FAQ (AP399).
>
> **7. Nebenbefund, wichtig:** `book_state.json` kennt nur 3 Konten (A, FN1, FN2), die Flotte hat aber 5 (FFN1, FFN2 fehlen). `weekend_check` rechnet damit gegen die falsche Flotte. Ich habe hier mit den 5 echten Konten aus den Konto-Karten gerechnet.

---

## 1. Ergebnis-Tabelle Firma × Kontotyp × Instrument

Kosten je Round-Turn: NAS100 je 1 MNQ-Äquivalent (2 $/Pkt), BTC je 0,1 BTC. Zum Vergleich unsere Futures in der Engine: **MNQ 2,90 $, MBT 6,40 $**. Zeit: Mittelwert der gepaarten Differenz (mit minus ohne CFD-Konto), Fehlerbalken = Monte-Carlo-SE über 600 Welten, Basis Flotte ohne CFD Median 78,7 Monate.

| Firma / Kontotyp | Instrument | zugelassen | Plattform | technischer Weg | Kosten je RT (Annahme) | Zeiten ok | Zeit bis 50k |
|---|---|---|---|---|---|---|---|
| **FTMO 2-Step 100K** | NAS100 (US100.cash) | **ja** (EA erlaubt, VPS „generally allowed", DE ok; Rechenzentrums-IP nicht erwähnt) | MT4, MT5, cTrader | MQL5-EA oder cBot | 4,00 $ bei 1,5 Pkt Spread (Komm. 0, sekundär; Spread nicht gefunden) | ja | **ja, −11,8 ± 0,3 M** (k1) |
| FTMO 2-Step 100K | BTCUSD | ja | dto. | dto. | 15,44 $ bei 5 bp (0,065 % je Seite, sekundär) | ja (Wochenende Krypto offen) | **nein, +0,7 ± 0,1 M** |
| FTMO 2-Step 100K | beides | ja | dto. | dto. | dto. | ja | **ja, −12,5 ± 0,3 M** |
| **E8 One 100K** (Classic Markets) | NAS100 | **wahrscheinlich** (EA ja, Kopierer eigene Konten ja, DE ok; **VPS-Regel nicht gefunden**) | MT5, cTrader, MatchTrader, TradeLocker | MQL5-EA oder cBot | 4,00 $ bei 1,5 Pkt (Spread und Komm. nicht gefunden) | ja (Serverzeit UTC+3/+2) | **ja, −10,6 ± 0,3 M** (k1) |
| E8 One 100K | BTCUSD | wahrscheinlich | dto. | dto. | 10,56 $ bei 5 bp (0,035 % Raw, sekundär) | ja | **nein, +0,5 ± 0,1 M** |
| E8 One 100K | beides | wahrscheinlich | dto. | dto. | dto. | ja | **ja, −11,8 ± 0,3 M** |
| **FN Stellar 2-Step 25K** | NDX100 | **bedingt** (EA und VPS nur unter 50k, EA-Add-on Gebühr unbekannt; 3-%-Risikoregel; Funded-Hebel 1:5 laut FN-Tabelle gegen 1:15 laut Help Center) | nur MT4/MT5 (cTrader/Match-Trader: keine EAs) | MQL5-EA | 4,00 $ bei 1,5 Pkt (Komm. 0 laut FN-Tabelle, Kontrakt 10) | ja, Asia-Range-Start in den DST-Lückenwochen 15 Min vor Indexöffnung | **ja, −6,0 ± 0,3 M** (k1, nur bei 1:15), **−7,4 ± 0,3 M** (halbe Größe, passt auch bei 1:5) |
| FN Stellar 2-Step 25K | BTCUSD | ja, **nur Mo bis Fr** | MT4/MT5 | dto. | 8,12 $ bei 5 bp (0,04 % nur bei Eröffnung laut FN-Tabelle; 11,38 $ falls je Seite) | ja | **nein, +0,1 ± 0,1 M** |
| FN Stellar 2-Step 25K | beides | bedingt | MT4/MT5 | dto. | dto. | ja | **ja, −6,6 ± 0,3 M** (k1), **−8,1 ± 0,3 M** (halbe Größe) |
| FN Stellar ab 50K, cTrader, Match-Trader | alle | **nein** | | | | | EA/VPS verboten |
| The5ers (High Stakes) | NAS100, BTC | nur mit schriftlicher Freigabe (FAQ „any EA", AGB „prior written approval") | MT5 | MQL5-EA | nicht gefunden | nicht geprüft | nicht gerechnet (Preise, Specs fehlen) |
| FundingPips | | wahrscheinlich nein („No VPN or VPS", nur sekundär) | | | | | nicht gerechnet |
| Alpha Capital | | **nein** (Primärzitat: unbeaufsichtigte EAs verboten) | | | | | |
| FFN | | kein CFD-Angebot gefunden | | | | | |

### Größere Größe (nur zur Einordnung, „Größe kauft Bust, nicht Tempo")

| Konto | Größe | Zeit bis 50k | Nulldrift | Funded-Busts Ø |
|---|---|---|---|---|
| E8 One 100K | k3 (gleiche DD-Ausnutzung wie E8 50k) | −26,9 ± 0,6 M | 0,0 % | 1,1 |
| FTMO 2-Step 100K | k5 | −42,0 ± 0,7 M | **1,0 % → Nulldrift-Alarm, Zeile nicht verwertbar** | 2,2 |

### Volle Ausgabe (aus `cfd_check/calc/t7_table.md`)

| Firma | Fall | CFD-Drift $/Tag | Median ohne -> mit (M) | Δ Mittel (M) ± SE | Δ Median ± SE | schneller in % der Welten | Nulldrift mit CFD | Auslage p90 ohne / mit (obere Schranke) | CFD-Käufe Ø | CFD funded Ø | Busts Eval/Funded Ø |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FN_Stellar2_25K | a_NQ_k0.5 | 15,7 | 78,8 -> 71,7 | -7,4 ± 0,3 | -7,1 ± 0,6 | 89,0 | 0,0 % | 1.332 / 1.532 | 2,3 | 2,1 | 0,0 / 1,3 |
| FN_Stellar2_25K | c_NQ+BTC_k0.5 | 16,5 | 78,8 -> 70,4 | -8,1 ± 0,3 | -8,4 ± 0,6 | 90,7 | 0,0 % | 1.332 / 1.532 | 2,4 | 2,1 | 0,0 / 1,4 |
| FN_Stellar2_25K | a_NQ_k1 | 31,4 | 78,8 -> 73,0 | -6,0 ± 0,3 | -5,8 ± 0,6 | 75,5 | 0,0 % | 1.332 / 1.732 | 9,4 | 8,1 | 0,7 / 7,8 |
| FN_Stellar2_25K | b_BTC_k1 | 1,5 | 78,8 -> 78,9 | 0,1 ± 0,1 | 0,1 ± 0,2 | 0,7 | 0,0 % | 1.332 / 1.532 | 1,0 | 0,4 | 0,0 / 0,0 |
| FN_Stellar2_25K | c_NQ+BTC_k1 | 33,0 | 78,8 -> 72,5 | -6,6 ± 0,3 | -6,3 ± 0,6 | 79,5 | 0,0 % | 1.332 / 1.732 | 9,6 | 8,4 | 0,7 / 8,0 |
| E8_One_100K | a_NQ_k1 | 31,4 | 78,8 -> 68,0 | -10,6 ± 0,3 | -10,8 ± 0,7 | 97,2 | 0,0 % | 1.332 / 1.674 | 1,0 | 1,0 | 0,0 / 0,0 |
| E8_One_100K | b_BTC_k1 | 1,5 | 78,8 -> 79,3 | 0,5 ± 0,1 | 0,5 ± 0,3 | 0,0 | 0,0 % | 1.332 / 1.674 | 1,0 | 0,0 | 0,0 / 0,0 |
| E8_One_100K | c_NQ+BTC_k1 | 33,0 | 78,8 -> 66,5 | -11,8 ± 0,3 | -12,3 ± 0,7 | 97,7 | 0,0 % | 1.332 / 1.674 | 1,0 | 1,0 | 0,0 / 0,0 |
| E8_One_100K | a_NQ_k3 | 94,2 | 78,8 -> 48,0 | -26,9 ± 0,6 | -30,8 ± 0,9 | 88,3 | 0,0 % | 1.332 / 2.016 | 2,4 | 1,9 | 0,4 / 1,1 |
| E8_One_100K | c_NQ+BTC_k3 | 98,9 | 78,8 -> 46,9 | -27,6 ± 0,7 | -31,9 ± 0,9 | 87,7 | 0,0 % | 1.332 / 2.016 | 2,4 | 1,9 | 0,4 / 1,1 |
| FTMO_2Step_100K | a_NQ_k1 | 31,4 | 78,8 -> 66,8 | -11,8 ± 0,3 | -12,0 ± 0,7 | 98,3 | 0,0 % | 1.332 / 1.922 | 1,0 | 1,0 | 0,0 / 0,0 |
| FTMO_2Step_100K | b_BTC_k1 | 1,4 | 78,8 -> 79,6 | 0,7 ± 0,1 | 0,8 ± 0,4 | 0,0 | 0,0 % | 1.332 / 1.922 | 1,0 | 0,0 | 0,0 / 0,0 |
| FTMO_2Step_100K | c_NQ+BTC_k1 | 32,8 | 78,8 -> 66,3 | -12,5 ± 0,3 | -12,5 ± 0,7 | 98,5 | 0,0 % | 1.332 / 1.922 | 1,0 | 1,0 | 0,0 / 0,0 |
| FTMO_2Step_100K | a_NQ_k5 | 157,1 | 78,8 -> 34,8 | -42,0 ± 0,7 | -44,0 ± 1,0 | 98,2 | 1,0 % | 1.332 / 2.512 | 3,5 | 3,0 | 0,3 / 2,2 |
| FTMO_2Step_100K | c_NQ+BTC_k5 | 163,8 | 78,8 -> 34,4 | -43,0 ± 0,7 | -44,4 ± 1,0 | 98,0 | 0,7 % | 1.332 / 2.183 | 3,7 | 3,2 | 0,4 / 2,4 |

Flotte ohne CFD: Erreichung 93,3 %, Median 78,7 Monate, Auslage p90 1.332 $, Nulldrift 0,0 %. Kontrolle „Flotte mit Deckel +1.000 $ bzw. +1.500 $, ohne CFD": 0,0 Monate Unterschied.

### Break-even-Spread NAS100 (Gitter, 200 Welten, k1)

Nullstelle der gepaarten Differenz über den Spread, linear interpoliert, Band aus Differenz ± 2 SE. Dazu der Spread, ab dem nur noch jede zweite Welt schneller ist.

| Firma | Break-even-Spread | Band | „schneller in 50 % der Welten" ab |
|---|---|---|---|
| E8 One 100K | 9,6 Pkt | 8,8 bis 11,5 | 5,9 Pkt |
| FTMO 2-Step 100K | 9,8 Pkt | 9,1 bis 11,5 | 6,5 Pkt |
| FN Stellar 2-Step 25K | 11,2 Pkt | 10,0 bis 13,6 | 4,5 Pkt |

Die CFD-Drift fällt um rund 2,6 $ je Tag je Punkt Spread (Gitter: 34,03 $/Tag bei 0,5 Pkt, 9,21 bei 10 Pkt). Ab dem Spread, bei dem NAS100 so teuer ist wie MNQ in der Engine, sind es **0,95 Punkte**; darüber ist der CFD je Trade teurer als der Future.

**BTC:** Break-even gibt es nicht, das BTC-Bein allein ist auf keinem Konto und bei keinem Spread (0 bis 40 bp) schneller. Die Kostenhöhe ist egal, weil das Konto mit rund 1,5 $ Drift je Tag die Prüfung praktisch nie besteht.

---

## 2. Annahmen (alles, was nicht gemessen ist, steht hier)

- **Spreads sind nicht gemessen.** Keine Firma veröffentlicht NAS100- oder BTCUSD-Spreads als Text. Hauptrechnung 1,5 Pkt NAS100 und 5 bp BTC, dazu Slippage 0,25 Pkt je Seite (wie Futures) bzw. 1 bp. Deshalb das Break-even-Gitter.
- **Kurs-Ersatz:** NQ-Futures für NAS100-Cash, BTC-Futures für BTCUSD. Basis und Carry ignoriert (Beine sind intraday, um 15:55 ET flat, kein Swap).
- **Kosten voll auch in die Auslenkung gebucht** (konservativ). BTC-Kosten in bp vom Tagespreis, also historisch kleiner in Dollar.
- **Käfige:** FN 2-Step 25K Ziele 2.000/1.250, DD 2.500 statisch, Tagesverlust 1.250, 5 Mindesttage je Phase, Split 80 %, Payout 21/14 Kalendertage, **3-%-Regel (750 $ offenes Risiko) im Funded als Bust gerechnet** (an 1,9 % der Tage bei k1 gerissen). E8 One 100K Ziel 9.000, Dynamic DD 6.000 auf Schluss-Saldo, rastet bei Initial ein, Tagesverlust 4.000, Funded-Konsistenz 40 %, Mindestauszahlung 2.000 $, Auszahlung nur über dem DD-Puffer, Split 80 % (wählbar 80/90/100). FTMO 2-Step 100K Ziele 10.000/5.000, DD 10.000 statisch, Tagesverlust 5.000, 4 Mindesttage, Split 80 %, Gebühr mit erstem Payout zurück, **Preis 590 $ ungeprüft** (nicht gefunden). Eigener Tagesstopp = Tagesverlust minus 300 $ × k. Neukauf nach Bust bis 1.000 $ (FTMO 1.500 $) Netto-Auslage.
- **Flotte:** `tempo_plan.simulate_fleet_calendar` mit den Einstellungen von `weekend_check` (Kalender-Modus, RiskGuard-Tagesstopp, Lane E8 150k k1, Budget 600 $/Monat, Deckel 2.500 $, Seed 101). **Bestand = 5 echte Konten** aus `engine/konten/accounts.json` (Stand 16.10., konto-analyst), nicht der veraltete Plan in `book_state.json`. CFD-Konto auf denselben Masterpfaden, also gepaart: dieselben historischen Tage treffen beide gleichzeitig.
- **Margin geprüft:** max. 3 NQ-Beine gleichzeitig offen (1,7 % der Tage). FN k1 bei 1:5 Funded-Hebel bräuchte 35.270 $ Margin auf 25.000 $, geht nicht; bei 1:15 sind es 11.756 $. Halbe Größe (0,1 Lot) passt auch bei 1:5 (17.635 $). E8 und FTMO unkritisch.
- **Nicht modelliert:** Consistency der FTMO-1-Step (nicht gerechnet), News-Regeln (FN Funded ±5 Min nur 40 % Gewinn, E8 One 5 Min Sperre), Inaktivität (handeln fast täglich), Ausführungsunterschiede MT5 gegen NT8.

## 3. Zeiten (Phase 3)

- Alle Bein-Zeiten liegen im CFD-Handelsfenster: RTH 09:30 bis 15:55 ET = 16:30 bis 22:55 Serverzeit (GMT+3 im Sommer), LastHour ab 13:30 ET, BTC-OR60 09:30 bis 10:30 ET.
- **Asia-Range 19:00 bis 03:00 ET** wird auf dem CFD-Feed gelesen. In den Wochen, in denen USA und EU die Uhr unterschiedlich umstellen (März, Ende Okt./Anfang Nov.), liegt 19:00 ET auf 01:00 Serverzeit, FN-Indexöffnung ist 01:15: die ersten 15 Minuten fehlen. Klein, aber im EA abfangen.
- FN-Settlement-Fenster 00:00 bis 02:00 Serverzeit = 17:00 bis 19:00 ET: keine Trades von uns darin.
- Krypto: FN nur Mo bis Fr (Sa/So geschlossen), E8 Classic und FTMO auch am Wochenende. Für die 09:30-ET-Variante egal.
- Flat-Pflicht: CFD-Firmen erlauben Overnight und Wochenende (FTMO Funded: nicht über Pausen über 2 Stunden). Unsere Beine sind ohnehin um 15:55 ET flat.

## 4. Technik (Phase 4, nur geprüft, nichts installiert)

| Weg | geht? | Kosten | Aufwand (Einschätzung) | Hauptrisiko | neben NT8 ok? |
|---|---|---|---|---|---|
| NT8 direkt an MT5/cTrader | nein, kein Adapter | | | | nein |
| Cloud-Kopierer (Duplikium) | vielleicht, NT8 nur „Beta" | ab 9 €/Konto/Monat | 1 bis 3 Tage Test | Ausfall = Position ohne Stop, FN verbietet Cloud-Kopierer | ja (Cloud) |
| Kopierer über TradingView | nein (kein TradingView, falsche Ziele) | | | | |
| Eigene Bridge NT8-Add-on zu MT5 | technisch ja | 0 | 5 bis 10 Tage | Code im NT8-Prozess der Live-Konten | **nein** |
| **Eigener MQL5-EA oder cBot (C#)** | **ja** | 0 (FN: EA-Add-on) | Port der 4 Beine plus Parität, mehrere Tage | Paritäts-Abweichung, eigener Tagesstopp nötig | **ja**, eigener Prozess, eigene MT5-Portable-Installation |
| Python über MT5-API | ja, ein Prozess je Terminal | 0 | 4 bis 8 Tage | Prozess-Stabilität | ja |

Empfehlung der Recherche: eigener MQL5-EA mit serverseitigem Stop und TP, in eigener MT5-Portable-Installation. Noch sicherer für die 5 Live-Konten: ein eigener kleiner VPS (8 bis 15 $/Monat, ungeprüft). Bekannte Konflikte MT5 neben NT8 auf Windows Server 2022: keine Quelle dafür oder dagegen.

## 5. Was bis zum ersten Trade fehlen würde

1. **Spread und Kontrakt-Specs messen** (NAS100, BTCUSD) auf einem Demo-Konto der Firma, 09:30 bis 16:00 ET, eine Woche. Ist der Spread unter rund 6 Pkt, trägt das Ja mit großer Mehrheit der Welten.
2. **Schriftliche Freigabe vom Support** (wie bei FFN): vollautomatischer eigener EA, unbeaufsichtigt, Windows-VPS mit Rechenzentrums-IP, Deutschland, dieselbe Strategie auch auf unseren Futures-Konten (bei E8 und FN dieselbe Firma!), mehrere Konten. Bei FN zusätzlich: welcher Funded-Hebel gilt (1:5 oder 1:15), Gebühr EA-Add-on, Folge eines Verstoßes gegen die 3-%-Regel.
3. **Port der 4 Beine als MQL5-EA** mit Paritätsprüfung gegen die Engine auf CFD-Daten, eigener Tagesstopp im EA (RiskGuard-Ersatz), bei FN Begrenzung des offenen Risikos.
4. Eintrag in [[Firm-Regeln je Konto]] und Ablauf `/neues-konto`, bevor der erste Trade läuft.
5. Kauf erst mit Blick auf die BOS-Reserve (CLAUDE.md, Lebenslage).

## 6. Offene Entscheidungen für Max

- **Lohnt sich der EA-Port** für ein (oder mehrere) CFD-Konten? Das ist der eigentliche Preis, nicht die 342 bis 590 $.
- **Welche Firma:** FTMO 2-Step 100K oder E8 One 100K (FN nur 25K und mit Auflagen).
- **Größe:** k1 ist gerechnet und sauber. E8 k3 wäre deutlich schneller, aber mit Funded-Busts; FTMO k5 fällt am Nulldrift-Zwilling durch.
- **BTC auf CFD:** aus meiner Sicht nein, die Rechnung gibt nichts her.
- **Vergleich mit einem weiteren Futures-Konto** gleicher Größe rechnen lassen? Ohne den ist offen, ob das CFD-Konto die beste Art ist, ein Konto mehr zu fahren.
- **`book_state.json` plan.accounts nachziehen** (FFN1, FFN2 fehlen), sonst rechnet `weekend_check` mit 3 statt 5 Konten. Ich habe die Datei nicht angefasst (Verbot im Auftrag).
- Support-Anfragen aus Abschnitt 5 schicken (ich darf keine Mails senden).

## 7. Quellen und Dateien

- Recherche: `C:\Users\Administrator\cfd_check\research_A_e8_fn_ffn.md`, `research_B_andere.md`, `research_C_technik.md`, `research_FN_mcp.md`, alle Zeilen im [[Research-Cache]] unter „CFD-Prop-Firmen für NAS100/BTC" (Abruf 23.10.2026). FundedNext zusätzlich direkt aus der FN-Wissensbasis über den FundedNext-Connector (nur lesend).
- Rechnung: `C:\Users\Administrator\cfd_check\calc\` (`t1_trades.py` Trades brutto/netto, `cfdsim.py` CFD-Käfig und Kosten, `t3_run.py` gepaarte Flotte, `t4_check.py` Margin/Risiko/Zeiten, `t5_costs.py` Kosten je RT, `t6_breakeven.py`, `t7_table.py`; Ergebnisse `out_main.json`, `out_grid.json`). In `trading-data` wurde nichts geändert.
- Gegengelesen: `quant-mathematician` (Paarung korrekt, Kernaussage trägt; seine Befunde zu Payout-Zyklen, E8-Konsistenz, FN-Risikoregel, Tagesstopp und Auslage sind eingebaut) und `quant-statistician` (siehe Abschnitt 8).

## 8. Gegenlesen Statistik und Robustheits-Spalte

`quant-statistician` (eigene Gegenrechnung mit 300 Welten, zwei Seeds, Dateien in `cfd_check\qs\`):

- **Paarung korrekt**, Nulldrift-Zwilling sauber (beide Bücher je Pfad zentriert, 0 % in allen Fällen).
- **Die MC-Fehlerbalken sind nicht die ehrliche Unsicherheit.** Futures-Buch 32,85 $/Tag, Block-SE 5,79, CI90 23,42 bis 42,38. Die Edge liegt fast ganz ab 2021 (2016 bis 2020 jeweils höchstens 13,4 $/Tag). Das NQ-CFD-Buch korreliert mit 1,00 mit der Flotte: es ist eine **verdoppelte Wette auf dieselbe Edge**, Schrumpfung trifft Basis und Zusatz gleichzeitig.
- **BTC:** auf dem CFD 1,54 $/Tag, Block-t 1,66, CI90 0,06 bis 3,12, Korrelation zum Futures-Buch 0,01. Passt zu „OR60 unentscheidbar" in #188. Zeile (b) heißt „kein messbarer Beitrag", nicht „Beitrag 0". Fall (c) **nicht als eigene Option führen**, der Gewinn kommt komplett aus NQ.
- Seine FN-Zahlen (ohne 3-%-Regel) liegen bei −19 Monaten; mit der Regel als Funded-Bust sind es bei mir −6. **Die 3-%-Regel ist bei FN der größte Einzelposten**, deshalb ist die Support-Frage nach ihrer Folge wichtig.

**Robustheits-Spalte shrink058** (meine finalen Konfigurationen, 300 Welten, Drift x 0,58 auf Futures- UND CFD-Buch, Median dort gekappt, deshalb Mittel bis 120 Monate und Erreichung):

| Konto, k1, NQ-Beine | Δ Zeit (Mittel bis Kappe) | Erreichung 50k in 10 Jahren ohne -> mit | Auslage p90 ohne / mit | Nulldrift |
|---|---|---|---|---|
| FTMO 2-Step 100K | −6,35 ± 0,64 M | 18,7 -> 38,3 % | 1.998 / 2.588 $ | 0,0 % |
| E8 One 100K | −5,43 ± 0,58 M | 18,7 -> 37,3 % | 1.998 / 2.340 $ | 0,0 % |
| FN Stellar 2-Step 25K | −1,97 ± 0,39 M | 18,7 -> 24,3 % | 1.998 / 2.531 $ | 0,0 % |

**Auslage:** das CFD-Konto hat einen eigenen Deckel (1.000 $, FTMO 1.500 $) neben den 2.500 $ der Flotte. Die Summe liegt also über dem heutigen Rahmen, die angegebene p90 „mit" ist eine Obergrenze.

**Was zum Beweis noch fehlt (nicht gerechnet, nicht beauftragt):** CFD-Konto gegen ein weiteres Futures-Konto bei gleicher Auslage (bei Korrelation 1,00 die eigentliche Alternative); Worst-Case-Spalte 2016 bis 2020.
