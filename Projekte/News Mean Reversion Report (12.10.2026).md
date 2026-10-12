---
tags:
  - projekt/trading
  - trading/alpha
  - trading/report
erstellt: 2026-10-12
status: fertig (Prämisse trägt nicht, NFP als Hinweis mit Wiedervorlage)
---
# 📰 Report: Mean Reversion nach News-Release (Juli-Modus Idee 5)

⬅️ [[Testphase Juli-Modus]] · [[Strategie-Logbuch]] #181 (Vorläufer #105, #109) · [[Alpha-Suche]]

> [!summary] Ergebnis in drei Sätzen
> Nach einem News-Release gegen die Erstreaktion zu handeln verdient auf NQ kein Geld: über alle 505 Releases sind alle sechs Strategie-Varianten null bis negativ, engere Stops machen es schlechter. Nur an NFP-Tagen ist der Fade in allen sechs Varianten positiv (bis rund 200 $ im Jahr je Micro), das ist aber die beste Gruppe aus vielen Versuchen, hängt an wenigen Tagen in 2021 bis 2023 und reicht statistisch nicht. Nebenbei gesehen: unser eigenes Buch verdient an News-Tagen deutlich mehr als an normalen Tagen, News-Bewegungen laufen also eher weiter als zurück.

## 1. Was getestet wurde

- **Markt und Daten:** NQ, 24h-Minutenbars, 03.01.2016 bis 10.08.2026.
- **Events:** 508 Releases um 08:30 ET (Kerze mit mindestens 3-fachem Volumen: NFP, CPI, Claims, PPI, Retail Sales, PCE) plus 84 FOMC. Davon 118 NFP, 111 CPI, 279 sonstige.
- **Idee als Regel:** Erstreaktion = Bewegung der ersten 5 Minuten nach dem Release. Einstieg um 08:35 dagegen (Short nach Sprung hoch, Long nach Sprung runter).
- **Zwei Stufen:** erst die reine Messung ohne Strategie (Prämissen-Tafel, 23 Zellen), dann auf Ansage als echte Strategie mit Stop, Ziel und Kosten (12 Varianten). Zusammen 35 Versuche.
- **Kosten:** 1,01 NQ-Punkte je Trade (2 Ticks je Seite plus Kommission), Stress-Rechnung mit 3 Punkten.

## 2. Stufe 2: reine Messung (Fade-Ertrag je Event in bp, positiv = kommt zurück)

| Gruppe | Events | bis 08:45 | bis 09:00 | bis 09:30 | bis 16:00 |
|---|---|---|---|---|---|
| **Alle 08:30-Releases** | 505 | | | **−0,02** (95 % −2,9 bis +2,9) | |
| NFP | 117 | +3,0 | +1,5 | **+7,4** (t 2,27) | +2,2 |
| CPI | 109 | −0,3 | −2,8 | +0,1 | +15,7 (t 1,35) |
| Sonstige 08:30 | 279 | +0,6 | −2,2 | −3,2 (t −1,66) | −4,2 |
| FOMC (ab 14:05) | 83 | +3,1 | +1,3 | +0,8 | +9,2 |

| Bedingung (alle Releases, bis 09:30) | Events | Fade-Ertrag |
|---|---|---|
| Großer Sprung (oberstes Drittel) | 176 | −1,4 |
| Kleiner Sprung (unterstes Drittel) | 150 | +0,7 |
| Sprung gegen den Nachttrend | 249 | +1,8 |
| Sprung mit dem Nachttrend | 256 | −1,8 |

- Trefferquote der Hauptzelle 50 %. Normale Tage zur selben Uhrzeit: −0,01 bp. Es gibt keinen Unterschied.
- Nötig wären rund 4 bp je Event vor Kosten gewesen (3 bp netto). Das ist ausgeschlossen.
- Die Sprünge selbst sind groß: im Median 16 bp an News-Tagen gegen 3,5 bp an normalen Tagen. Die Reaktions-Range der ersten 5 Minuten lag 2016 bis 2019 bei rund 13 Punkten, 2024 bis 2026 bei rund 97 Punkten.

## 3. Als Strategie mit Trades (1 Micro MNQ, nach Kosten)

Einstieg 08:35 gegen die Erstreaktion. Stop als Vielfaches der Reaktions-Range. Ausstieg um 09:30 oder am Pre-News-Preis.

| Variante | Trades | $ je Jahr | t | Treffer | Jahre im Plus | Max. Rückgang | Zufalls-Zwilling p |
|---|---|---|---|---|---|---|---|
| **Alle**, Stop 1,0, raus 09:30 | 505 | −22 | −0,12 | 46 % | 4 von 11 | −1.799 $ | 0,17 |
| Alle, Stop 1,0, Ziel Pre-News | 505 | −104 | −0,70 | 59 % | 5 von 11 | −2.269 $ | 0,30 |
| Alle, Stop 0,5, raus 09:30 | 505 | −180 | −1,04 | 36 % | 3 von 11 | −2.983 $ | 0,42 |
| Alle, Stop 0,5, Ziel Pre-News | 505 | −252 | −1,80 | 50 % | 3 von 11 | −3.307 $ | 0,64 |
| Alle, kein Stop, raus 09:30 | 505 | +35 | +0,19 | 48 % | 5 von 11 | −1.951 $ | 0,24 |
| Alle, kein Stop, Ziel Pre-News | 505 | −54 | −0,36 | 60 % | 4 von 11 | −2.159 $ | 0,35 |
| **NFP**, Stop 1,0, raus 09:30 | 117 | +159 | +1,52 | 53 % | 8 von 11 | −492 $ | 0,015 |
| NFP, Stop 1,0, Ziel Pre-News | 117 | +101 | +1,18 | 62 % | 8 von 11 | −477 $ | 0,045 |
| NFP, Stop 0,5, raus 09:30 | 117 | +66 | +0,66 | 42 % | 5 von 11 | −628 $ | 0,055 |
| NFP, Stop 0,5, Ziel Pre-News | 117 | +23 | +0,29 | 50 % | 6 von 11 | −759 $ | 0,23 |
| NFP, kein Stop, raus 09:30 | 117 | +202 | +2,05 | 54 % | 9 von 11 | −459 $ | 0,020 |
| NFP, kein Stop, Ziel Pre-News | 117 | +139 | +1,77 | 63 % | 9 von 11 | −468 $ | 0,040 |

- **Alle Releases:** keine Variante trägt. Das Ziel „zurück zum Pre-News-Preis" hebt die Trefferquote auf rund 60 %, verdient aber weniger: die Gewinner werden klein abgeschnitten, die Verlierer laufen. Das ist genau der Effekt aus #105 („kommt meistens zurück" stimmt, ist aber keine Edge).
- **Engere Stops sind durchweg schlechter.** Direkt nach dem Release schwankt der Preis so stark, dass ein enger Stop fast immer fällt.
- **NFP:** alle sechs Varianten im Plus, beste +202 $ im Jahr. Ohne die besten 5 % der Trades bleibt rund 0 bis +42 $ im Jahr. Jahre: 2016 bis 2019 um null, 2020 −210, 2021 +668, 2022 +169, 2023 +462, 2024 +133, 2025 +410, 2026 +21.
- **Mehrfachtest:** bestes t über die 12 Varianten 2,05, Zufallsniveau dafür p 0,09 (Schwelle wäre t 2,35). Dabei ist noch nicht eingerechnet, dass NFP selbst die beste von vier Gruppen aus der Messung war.
- **Stress-Kosten (3 Punkte):** alle Releases −155 bis −442 $ im Jahr, NFP +158 bis −20 $.

## 4. Was das Quant-Team dazu gerechnet hat

- **Statistiker:** Hauptzelle sauber leer (alle Bänder unter der Schwelle). NFP: sechs Events tragen 70 % des Effekts, ohne sie t 0,95. Plausible echte Größe nach Schrumpfen 1 bis 4 bp. Für einen sauberen Nachweis bräuchte es 141 neue NFP-Termine (knapp 12 Jahre).
- **Mathematiker:** keine Rechnung verbietet den Fade grundsätzlich, es ist rein empirisch. Als Bein würde NFP den Buch-Sharpe roh von 2,17 auf rund 2,25 heben, geschrumpft auf 2,20. Der Engpass ist der Nachweis (t unter 2 nach Kosten), nicht der Buch-Nutzen.
- **Auffällig:** die Rückkehr an NFP-Tagen passiert fast ganz zwischen 09:00 und 09:30, nicht in der ersten halben Stunde. Das sieht eher nach einer Bewegung in die Kassa-Eröffnung aus als nach Mean Reversion. Nachträglich gesehen, also nur eine Hypothese.
- **verdict-auditor:** alle drei Urteile halten.

## 5. Urteil ([[Strategie-Logbuch]] #181)

| Teil | Kategorie | Bedeutet |
|---|---|---|
| Fade nach allen 08:30-Releases zusammen | `empirisch-nichts-gefunden` | gemessen, leer, auch als Strategie in 6 Varianten |
| Fade nur an NFP | `unentscheidbar`, Hinweis | positiv, aber nicht von Zufall trennbar |
| CPI, sonstige, FOMC, große Sprünge, Nachttrend | `unentscheidbar` | zu wenige Events für eine Aussage |

- **Buch-Lücke:** hängt an der Prämisse. Kein Kandidat, nichts fürs Next-Week-Buch.
- **Wiedervorlage NFP:** nur mit NQ-Minutendaten vor 2016 (über Databento), unverändert derselbe Test. Termin-Erinnerung halbjährlich ab 04.01.2027.
- **Stempel:** PC-Lauf 12.10.2026, Engine `e6f39975…347f`, Eventliste Stand 23.08.2026, NQ bis 10.08.2026. Dieselben Daten wie #105, keine unabhängige Bestätigung.

## 6. Was wir daraus brauchen können

1. **News-Tage sind gute Tage für unser Buch.** Die vier NQ-Beine verdienen an Release-Tagen im Schnitt rund 62 $ je Tag gegen 36 $ an normalen Tagen, an NFP-Tagen rund 124 $. Das ist ein Nachher-Schnitt und kein Test, passt aber zu allem anderen: News-Bewegungen halten. Praktische Folge: das Buch an News-Tagen nicht abschalten, und keinen Fade-Baustein danebenstellen, der dagegen arbeitet.
2. **Enge Stops direkt nach einem Release kosten Geld.** Gilt für jede künftige Idee in diesem Zeitfenster.
3. **„Kommt meistens zurück" bleibt eine Falle.** 60 % Trefferquote beim Ziel Pre-News-Preis und trotzdem Verlust. Trefferquote ohne Gegenrechnung der Verlierer sagt nichts.
4. **Was offen bleibt und eine eigene Idee wäre:** Sprung nach echter Überraschung sortiert (Ist gegen Konsens, bräuchte eine Datenquelle), Einstieg in den ersten Sekunden (bräuchte Daten unter einer Minute), die NFP-Bewegung 09:00 bis 09:30, und die Gegenrichtung (Fortsetzung bei „sonstigen" Releases, dort −3,2 bp für den Fade).
5. **Was an den Zahlen schwach ist:** NFP- und CPI-Tage sind über das Volumen erkannt, nicht über den echten Kalender. Slippage direkt nach dem Release ist nur pauschal angesetzt. Die Gegengruppe ist nicht auf Volumen abgeglichen.

## 7. Wo alles liegt

- **Workbench, Sub-Tab Tests:** vier Karten vom 12.10. um 22:30 mit allen Trades im Chart: `juli5_news_fade_alle_stop1_60min`, `juli5_news_fade_alle_stop1_ziel_prenews`, `juli5_news_fade_nfp_stop1_60min`, `juli5_news_fade_nfp_ohne_stop_60min`.
- **Rechnung:** `engine/_scratch_juli_newsmr/` (`prereg.md` Vorab-Festlegung, `tafel.py` Messung, `strat.py` Strategie, Ergebnisse `tafel_out.txt`, `strat_out.txt`, Quant-Skripte in `stat/` und `math/`).
- **Nicht gemacht:** kein Lauf durch das Discovery-Gate (es gibt keinen Engine-Modus für 08:30, die Beine laufen nur in der regulären Handelszeit), keine Zeit-bis-50k-Rechnung, weil die Prämisse nicht trägt.
