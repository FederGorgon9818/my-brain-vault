---
date: 2026-10-23
tags: [projekt, cfd, prop-firm, krypto, bitcoin, tempo_plan, recherche]
status: Bericht fertig, Entscheidungen bei Max
tickets: [AP399, AP422]
---

# 💱 CFD-Check (23.10.2026): können wir NAS100 und BTC auf CFD-Props handeln, und bringt es Zeit bis 50k?

Auftrag Max 23.10.2026 vormittags, gefahren auf der Box ohne Mensch am Bildschirm (Session c97e7af8, 09:36 bis ca. 11:30 Boxzeit). Eigenes CFD-Buch, nicht mit dem Futures-Buch verrechnet: ein zusätzliches Konto neben der laufenden Flotte. Futures-Daten (NQ, BTC) als Kurs-Ersatz, Kosten durch die CFD-Kosten der Firma ersetzt. **Kein Gate v4, keine neue Suche, keine neuen Varianten.** Einzige Frage: verkürzt ein CFD-Konto die Zeit bis 50k?

Verwandt: [[Nightrun BTC 23.10.2026]], [[Firm-Regeln je Konto]], [[Research-Cache]] (neuer Abschnitt „CFD-Prop-Firmen für NAS100/BTC"), [[Eval vs. Funded Neubewertung (18.10.2026)]], [[Strategie-Logbuch]] #188.

> ## 🆕 Nachtrag 23.10. abends: weiteres Futures-Konto gegen CFD-Konto (Abschnitt 9 und 10)
>
> **Empfehlung: erst ein weiteres Futures-Konto, nicht das CFD-Konto.** Ein E8 Signature Futures 100K (260 $) bringt fast genauso viel wie das beste CFD-Konto: **−10,1 ± 0,3 Monate** gegen −10,6 (E8 One) und −11,8 (FTMO) bei 1,5 Pkt Spread. Mit einem Tagesstopp von 900 $ wie beim E8 50k liegt es gegen E8 One schon gleichauf (+0,03 ± 0,17), bei 4 Pkt Spread ist es vor jedem CFD-Konto. Pro Euro ist es mit 3,4 Monaten je 100 $ Auslage eins der besten Konten, und es braucht **keinen Port**: es kann am Tag nach dem Kauf handeln, das CFD-Konto erst nach Spread-Messung, Freigabe und MQL5-EA. **Die Reihenfolge ist aber nicht robust:** mit geschrumpfter Edge (x 0,58) liegt CFD gleichauf oder vorn, der Unterschied beträgt 0 bis 2 Monate und ist kleiner als die Unsicherheit der Edge. FFN 150K und E8 150K bringen je rund −8 Monate. **`book_state` kennt jetzt alle 5 Konten**, und `weekend_check` rechnet damit (zwei kleine Code-Änderungen nötig, Abschnitt 10).
>
> ## 🧭 Kurzfassung für Max (Vormittag)
>
> **1. Die vier NQ-Beine auf einem CFD-Konto: ja, das verkürzt die Zeit bis 50k. Die Richtung ist sicher, die Größe nur auf etwa Faktor 2 genau.** Mit k1 (1 MNQ-Äquivalent je Bein) und angenommenen 1,5 Punkten NAS100-Spread, Backtest-Edge: FTMO 2-Step 100K **rund 12 Monate schneller**, E8 One 100K **rund 11**, FundedNext Stellar 2-Step 25K **rund 6** (Flotte ohne CFD: Median 78,7 Monate; in 97 bis 98 % der Welten ist die Flotte mit FTMO oder E8 schneller). Mit geschrumpfter Edge (Drift x 0,58 auf beiden Büchern) bleibt es ein Ja, aber kleiner: FTMO **−6,4**, E8 **−5,4**, FN **−2,0** Monate (Mittel bis zur 120-Monats-Kappe), und die Chance, 50k in 10 Jahren zu erreichen, steigt von 18,7 % auf 38,3 % (FTMO) bzw. 37,3 % (E8). Nulldrift-Zwilling überall 0,0 %. Die Monte-Carlo-Fehlerbalken (± 0,3 bis 0,6) sind dabei klein gegen die Unsicherheit der Edge selbst, deshalb nenne ich Spannen statt einer Zahl.
>
> **2. BTC auf CFD: nein.** Die BTC-Variante aus dem Nachtlauf bringt allein auf jedem CFD-Konto nichts (+0,1 bis +0,7 Monate, also leicht langsamer, weil das Konto die Prüfung praktisch nie besteht). Zusammen mit den NQ-Beinen spart sie zusätzlich 0,6 bis 1,2 Monate (FN 0,61, FTMO 0,70, E8 1,15), das ist kleiner als das, was die unbekannten Spreads verschieben können.
>
> **3. Das Ja hängt an einer Zahl, die keine Firma veröffentlicht: dem NAS100-Spread.** Break-even liegt bei rund **9,6 Punkten (E8), 9,8 (FTMO), 11,2 (FN)**. Üblich sind bei CFD-Brokern 1 bis 2 Punkte zur US-Session, das ist aber nicht gemessen. Bevor irgendwas gekauft wird, muss der Spread auf einem Demo-Konto gemessen werden.
>
> **4. Was das Ja eigentlich ist:** ein weiteres Konto, das dasselbe Buch handelt. Der Gewinn kommt aus mehr arbeitendem Kapital, nicht aus etwas CFD-Eigenem. Ein höherer Kaufdeckel für die Futures-Flotte allein bringt dagegen **0,0 Monate** (Kontrolllauf), das Budget ist also nicht der Engpass. Ob ein weiteres Futures-Konto dasselbe günstiger leistet, habe ich nicht gerechnet (nicht beauftragt). **Am Abend gerechnet, siehe Abschnitt 9.**
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
- **`book_state.json` plan.accounts nachziehen** (FFN1, FFN2 fehlen), sonst rechnet `weekend_check` mit 3 statt 5 Konten. Ich habe die Datei nicht angefasst (Verbot im Auftrag). **Erledigt am Abend, siehe Abschnitt 10.**
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

## 9. Vergleich mit weiterem Futures-Konto (Box, 23.10. abends, Session 246ecc87)

**Frage von Max:** ein weiteres Futures-Konto gleicher Größe gegen das CFD-Konto, gleiche Methode, nur Zeit bis 50k.

**Methode, wie im CFD-Check:** Flotte = die 5 echten Konten (Stand 16.10.), `tempo_plan.simulate_fleet_calendar` mit den Einstellungen von `weekend_check` (Kalender-Modus, RiskGuard-Tagesstopp, Lane E8 150k k1, Budget 600 $/Monat, Deckel 2.500 $, Seed 101), 600 Welten, Nulldrift-Zwilling 300 Welten. Das Zusatzkonto läuft auf **denselben Masterpfaden** und sein Netto wird je Welt zum Flotten-Netto addiert, also gepaart.
- **CFD-Konto:** unverändert aus dem CFD-Check (`cfdsim.run_cfd`), NQ-Beine k1, NAS100 1,5 und 4 Pkt Spread. Die 1,5-Pkt-Zeilen reproduzieren den Vormittag exakt (E8 One −10,62, FTMO −11,76), damit ist die Paarung nachgeprüft.
- **Futures-Konto:** echte Engine-Käfige aus `tempo_plan` (E8 Signature, FundedNext Flex, FFN STEADY über `konten/ffnlib`), echtes Buch mit MNQ, Engine-Kosten (MNQ 2,90 $ je RT), k1, Tagesstopp wie in `weekend_check` (`riskguard_loss`). Genau **ein aktives Konto** (nach Bust Nachkauf), Kauf am Tag 0, eigener Deckel 1.000 $ wie das CFD-Konto.
- Eine erste Fassung des Laufs kaufte mit dem Engine-Standard der Lane 2 Evals gleichzeitig. Die habe ich verworfen (Datei `out_B_m2.npz`), sie war nicht mit einem CFD-Konto vergleichbar.

**Gewählte Futures-Konten (Werte aus der Engine, Quelle Research-Cache / [[Firm-Regeln je Konto]]):**

| Konto | warum | Preis | Ziel / DD | Tagesstopp (Engine) |
|---|---|---|---|---|
| E8 Signature Futures 100K | gleiche Firma und Größe wie E8 One 100K CFD | 260 $ | 6.000 / 3.000 EOD-Trailing | 600 $ (**nur Default 600 x k**, kein Firmenwert) |
| E8 Signature Futures 150K | DD näher an E8 One (6.000) | 333 $ | 9.000 / 3.999,90 | 2.500 $ |
| FFN STEADY 150K | unsere günstigste Linie, drittes FFN-Konto (Copy-Limit 5) | 292,50 $ | 9.000 / 4.700 | 2.500 $ |
| FundedNext Flex 100K | FN Futures erlaubt unseren Bot (läuft auf FN1/FN2) | 144,99 $ | 5.000 / 2.500 | 600 $ (Default) |
| FundedNext Flex 150K | größere FN-Variante | 278,99 $ | 8.000 / 4.000 | 2.500 $ |

Kein Futures-Konto erreicht den DD-Spielraum der CFD-Konten (E8 One 6.000, FTMO 10.000), deshalb stehen 100K und 150K beide drin.

**Ergebnis je Zusatzkonto** (Flotte ohne: Median 78,8 Monate, Erreichung 93,3 %, Auslage p90 1.332 $; Δ = mit minus ohne, negativ = schneller):

| Zusatzkonto | Preis $ | Drift $/Tag | Median ohne → mit | Δ Mittel ± SE | Δ Median ± SE | schneller in % der Welten | Nulldrift | Auslage p90 ohne / mit (obere Schranke) | Monate je 100 $ Ø-Auslage | Käufe Ø |
|---|---|---|---|---|---|---|---|---|---|---|
| CFD E8 One 100K, 1,5 Pkt | 342 | 31,41 | 78,8 → 68,0 | −10,62 ± 0,31 | −10,8 ± 0,7 | 97,2 | 0,0 % | 1.332 / 1.674 | 3,08 | 1,01 |
| CFD E8 One 100K, 4 Pkt | 342 | 24,88 | 78,8 → 72,5 | −6,30 ± 0,26 | −6,3 ± 0,7 | 82,2 | 0,0 % | 1.332 / 1.674 | 1,80 | 1,02 |
| CFD FTMO 2-Step 100K, 1,5 Pkt | 590 | 31,41 | 78,8 → 66,8 | −11,76 ± 0,32 | −12,0 ± 0,7 | 98,3 | 0,0 % | 1.332 / 1.922 | 1,99 | 1,00 |
| CFD FTMO 2-Step 100K, 4 Pkt | 590 | 24,88 | 78,8 → 71,2 | −7,31 ± 0,26 | −7,6 ± 0,7 | 89,2 | 0,0 % | 1.332 / 1.922 | 1,24 | 1,00 |
| **E8 Futures 100K** | 260 | 32,85 | 78,8 → 68,3 | **−10,12 ± 0,30** | −10,5 ± 0,8 | 96,0 | 0,0 % | 1.332 / 1.592 | **3,42** | 1,38 |
| E8 Futures 150K | 333 | 32,85 | 78,8 → 70,4 | −8,00 ± 0,27 | −8,4 ± 0,7 | 90,8 | 0,0 % | 1.332 / 1.665 | 2,31 | 1,08 |
| FFN STEADY 150K | 292,50 | 32,85 | 78,8 → 71,0 | −7,84 ± 0,27 | −7,8 ± 0,7 | 89,7 | 0,0 % | 1.332 / 1.624 | 2,64 | 2,95 |
| FN Flex 100K | 144,99 | 32,85 | 78,8 → 73,2 | −6,23 ± 0,24 | −5,6 ± 0,8 | 83,8 | 0,0 % | 1.332 / 1.622 | 3,67 | 5,91 |
| FN Flex 150K | 278,99 | 32,85 | 78,8 → 72,7 | −6,15 ± 0,25 | −6,1 ± 0,7 | 84,2 | 0,0 % | 1.332 / 1.611 | 2,14 | 4,01 |

Busts: CFD-Konten Eval/Funded im Schnitt höchstens 0,01 / 0,02. Futures (Mittel je Welt): Eval-Busts E8 100K 0,19, E8 150K 0,04, FFN 0,01, FN 100K 0,53, FN 150K 0,05; Funded-Konten E8 100K 2,34 (mit Gratis-Challenges), E8 150K 2,06, FFN 2,52, FN 100K 4,88, FN 150K 3,42. „Käufe" bei Futures = bezahlte Käufe, E8-Gratis-Challenges nicht mitgezählt.

### Kernfrage: Futures-Konto X gegen CFD-Konto Y (gepaart, Zeit mit X minus Zeit mit Y, negativ = Futures schneller)

| X Futures | Y CFD | Δ Mittel (M) ± SE | X schneller % | Y schneller % | gleich % |
|---|---|---|---|---|---|
| E8 100K | E8 One 1,5 Pkt | +0,50 ± 0,17 | 20,8 | 30,3 | 48,8 |
| E8 100K | E8 One 4 Pkt | −3,82 ± 0,24 | 65,8 | 3,0 | 31,2 |
| E8 100K | FTMO 1,5 Pkt | +1,64 ± 0,18 | 13,0 | 41,0 | 46,0 |
| E8 100K | FTMO 4 Pkt | −2,80 ± 0,22 | 54,8 | 5,5 | 39,7 |
| E8 150K | E8 One 1,5 / 4 Pkt | +2,62 ± 0,22 / −1,71 ± 0,18 | 6,5 / 43,5 | 50,8 / 7,3 | 42,7 / 49,2 |
| E8 150K | FTMO 1,5 / 4 Pkt | +3,76 ± 0,24 / −0,69 ± 0,17 | 1,7 / 30,8 | 60,8 / 14,8 | 37,5 / 54,3 |
| FFN 150K | E8 One 1,5 / 4 Pkt | +2,78 ± 0,23 / −1,54 ± 0,18 | 7,5 / 36,3 | 52,3 / 10,3 | 40,2 / 53,3 |
| FFN 150K | FTMO 1,5 / 4 Pkt | +3,92 ± 0,25 / −0,52 ± 0,18 | 5,0 / 26,0 | 62,3 / 19,5 | 32,7 / 54,5 |
| FN 100K | E8 One 1,5 / 4 Pkt | +4,39 ± 0,24 / +0,07 ± 0,14 | 0,7 / 19,7 | 72,8 / 18,3 | 26,5 / 62,0 |
| FN 100K | FTMO 1,5 / 4 Pkt | +5,53 ± 0,25 / +1,08 ± 0,14 | 0,0 / 8,7 | 82,3 / 33,0 | 17,7 / 58,3 |
| FN 150K | E8 One 1,5 / 4 Pkt | +4,47 ± 0,24 / +0,15 ± 0,13 | 0,3 / 17,7 | 75,3 / 20,7 | 24,3 / 61,7 |
| FN 150K | FTMO 1,5 / 4 Pkt | +5,61 ± 0,25 / +1,17 ± 0,13 | 0,2 / 8,0 | 84,7 / 36,0 | 15,2 / 56,0 |

Viele Welten liegen gleichauf (Raster der Zeitmarken), deshalb ist das Mittel ± SE die bessere Zahl als der Median-Abstand.

### Gegenlesen

**`quant-mathematician`: trägt mit Einschränkung.** Paarung sauber (Lauf E8 100K bitgleich nachgerechnet). Firmenweite Grenzen (E8 max. 5 Funded, FN-Allokation 750k, FFN-Copy-Limit 5) greifen bei dieser Flotte praktisch nicht. Der Nachkauf aus 600 $/Monat bremst eher die Futures-Seite. **Wichtigster Punkt: der 600-$-Tagesstopp für E8 100K ist nur der Engine-Default** und bestraft das Futures-Konto. Gepaart nachgerechnet, E8 Futures 100K gegen CFD:

| Tagesstopp E8 100K | gg. E8 One 1,5 | gg. E8 One 4 | gg. FTMO 1,5 | gg. FTMO 4 |
|---|---|---|---|---|
| 600 $ (Default) | +0,50 ± 0,17 | −3,82 ± 0,24 | +1,64 ± 0,18 | −2,80 ± 0,22 |
| 900 $ (wie E8 50k live) | +0,03 ± 0,17 | −4,29 ± 0,24 | +1,17 ± 0,18 | −3,27 ± 0,22 |
| 2.500 $ | −0,46 ± 0,16 | −4,79 ± 0,25 | +0,68 ± 0,16 | −3,77 ± 0,22 |

Break-even-Spread (ab hier ist E8 Futures 100K schneller, linear zwischen 1,5 und 4 Pkt): gegen E8 One **1,79 Pkt** (Stopp 600), 1,52 (900), 1,23 (2.500); gegen FTMO 2,42 / 2,16 / 1,88. E8 150K gegen E8 One / FTMO 3,01 / 3,61 Pkt, FFN 150K 3,11 / 3,71, FN 100K / 150K gegen E8 One 4,04 / 4,09. Für FN 100K gilt dasselbe Stopp-Problem, nicht nachgerechnet. Offen: ob E8 One einen Gratis-Reset hat (im CFD-Käfig nicht modelliert, wäre ein kleiner Nachteil für CFD).

**`quant-statistician`: trägt mit Einschränkung.** Die SE messen nur das Pfad-Rauschen bei fester Edge. Mit geschrumpfter Edge (x 0,58 auf beiden, 200 Welten) dreht die Reihenfolge, weil bei kleiner Edge der breitere CFD-Drawdown mehr zählt als der Kostenvorsprung (plus = Futures langsamer, Stopp 600):

| E8 Futures 100K gegen | roh (600 Welten) | shrink058 (200 Welten) |
|---|---|---|
| E8 One 1,5 Pkt | +0,50 ± 0,17 | +1,65 ± 0,32 |
| E8 One 4 Pkt | −3,82 ± 0,24 | +0,13 ± 0,32 (gleich) |
| FTMO 1,5 Pkt | +1,64 ± 0,18 | +2,32 ± 0,42 |
| FTMO 4 Pkt | −2,80 ± 0,22 | +0,82 ± 0,29 |

Einschränkung dazu: unter shrink058 liegt der Median bei der 120-Monats-Kappe, die Mittel sind gestutzt, und roh gegen shrink vergleicht 600 gegen 200 Welten. Nulldrift überall 0,0 % (300 Welten, also echt höchstens rund 1 %). Seine Formulierung, die ich übernehme: **„Ein weiteres E8-Futures-Konto 100K bringt ungefähr so viel wie das beste CFD-Konto bei 1,5 Pkt Spread und ohne Port. Bei 4 Pkt ist es nur dann klar besser, wenn die Edge in voller Höhe hält. Die Reihenfolge Futures gegen CFD ist nicht robust, der Unterschied liegt bei 0 bis 2 Monaten und ist kleiner als die Unsicherheit der Edge selbst."**

### Aufwand und frühester Handelsstart

- **Futures-Konto (alle fünf):** kein Port, der NT8-Host mit den 4 Beinen läuft schon. Nach dem Kauf: Ablauf `/neues-konto` (Regeln, RiskGuard-cfg mit eigenem Tagesstopp, Telegram, Host-Datei). Realistisch **am Tag nach dem Kauf** handelbar, so wie FFN1/FFN2 (aktiviert 05. bzw. 08.10.). Bei E8 100K vorher den eigenen Tagesstopp festlegen (900 $ wie E8 50k wäre die naheliegende Wahl, nicht gerechnet als Empfehlung).
- **CFD-Konto:** Spread eine Woche auf Demo messen, schriftliche Freigabe vom Support, Port der 4 Beine als MQL5-EA mit Paritätsprüfung und eigenem Tagesstopp (mehrere Tage). Meine Einschätzung, nicht gerechnet: **nicht vor Ende November 2026**.

### Was das heißt (Einschätzung)

- **Pro Aufwand gewinnt Futures klar**, pro Euro liegen E8 Futures 100K (3,42 Monate je 100 $) und FN Flex 100K (3,67, aber nur −6,2 Monate absolut) vorn, CFD E8 One bei 1,5 Pkt bei 3,08, FTMO wegen 590 $ bei 1,99.
- **Bei der absoluten Zeit ist es ein Unentschieden**, das am CFD-Spread und an der Edge-Höhe hängt. Das CFD-Konto lohnt sich nur, wenn der gemessene Spread unter rund 1,5 Pkt liegt **und** der EA-Port ohnehin gewollt ist (z. B. als zweite Plattform).
- Beides schließt sich nicht aus: das Futures-Konto ist jetzt machbar, das CFD-Konto ist eine spätere Option.
- **Kauf nur mit Blick auf die BOS-Reserve** (Lebenslage), Entscheidung Max. Nichts gekauft, nichts angelegt.
- **Achtung, nebenbei aufgefallen (`konto-analyst`):** die E8-50k-Karte steht seit dem Neuschreiben heute 17:03 auf **ROT wegen Inaktivität** (bis 22.10. fehlte ein Handelstag), Stand der Daten aber 16.10. Bitte prüfen, ob E8 seit dem 16.10. gehandelt hat.

**Nicht gerechnet (nicht beauftragt oder nicht in der Zeit):** FN 100K mit realistischem Tagesstopp, shrink058 für alle Paare, Worst-Case 2016 bis 2020, andere k als k1, zwei Zusatzkonten.

Dateien: `C:\Users\Administrator\cfd_vergleich\calc\` (`v_run.py`, `v_table.py`, `t_table.txt`, `out_A.npz`, `out_B.npz`), Prüfungen in `cfd_vergleich\qm\` und `cfd_vergleich\qs\`.

## 10. book_state nachgezogen (Box, 23.10. abends)

- **`book_state.json` → `plan.accounts`** hat jetzt die 5 echten Konten: A = E8 50k `E61803453048`, FN1, FN2, FFN1 `2D-150K394206247048`, FFN2 `2D-150K010602681476`. Je Konto: Größe, k1, Stufe eval, Ziel, DD, Tagesstopp (E8 900, FN 600, FFN 2.500 $), Beine (PB3, LH, Asia, OD), Kontostand und Hoch vom 16.10. als Startpunkt (`bal0`/`peak0`), Konto-ID. Quelle `engine/konten/accounts.json` (Register der Konto-Karten, gleich mit der RiskGuard-cfg laut `konto-analyst`). Bisher rechnete `weekend_check` mit 3 Konten und einem E8-Startsaldo vom 21.09.
- **Beine, Parameter, Betriebspunkt, `plan.tiers` unverändert** (im Skript per Vergleich geprüft). Backup `book_state.json.bak-20261023-konten`.
- **md5 `book_state.json`: vorher `FF4710EFBC31F8B4A3780F0B6C642203`, nachher `90E5EAF7D0A8994E4DC3ED42DB0F3BC0`.** Muss auf den PC gespiegelt werden (kein `--push-next`, direkt im Box-Ordner gearbeitet).
- **`weekend_check.py` brauchte zwei kleine Änderungen**, sonst hätte er nicht mit 5 Konten gerechnet: (1) die Größe `FFN-150k` war unbekannt, FFN-Konten wären still übersprungen worden; (2) im Lauf mit dynamischem Stopp bricht der FFN-Käfig ab, FFN bekommt dort jetzt den festen RiskGuard-Stopp (wie live). Datei muss ebenfalls auf den PC.
- `funded_finalize.py` gelaufen (Fingerprint 90e5eaf7, Kaufplan listet 5 Konten). **`weekend_check --quick` gelaufen:** Bestand „A E8 50k k1, FN1, FN2, FFN1 FFN 150k k1, FFN2 FFN 150k k1", echtes Buch Median 76,9 ± 5,0 Monate (nur 60 Welten, Orientierung). Bericht `engine/weekend_check/2026-10-23_konten_quick.md`. Kleiner Anzeigefehler dort: die Spaltenüberschrift nennt für FFN DD 4000, gerechnet wird mit dem FFN-Käfig (4.700).
- `book_state_next.json`, NT8, RiskGuard-cfg, Host-Dateien, Runner: nicht angefasst.
