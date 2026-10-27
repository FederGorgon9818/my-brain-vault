---
tags:
  - projekt/trading
  - idee
  - orderflow
  - geparkt
erstellt: 2026-10-22
status: geparkt, Wiedervorlage sobald die MNQ-Tickdaten aus AP427 da sind
---
# Sekunden-Scalping 5 bis 10 s: Edge genau oberhalb der FFN-HFT-Grenze?

⬅️ [[Alpha-Suche]] · [[Firm-Regeln je Konto]] · [[Order-Flow Predictive Research]] · [[Testphase Juli-Modus]] · [[1555-Zeit-Exit Entscheidung (AP426)]]

> [!summary] In drei Sätzen
> Idee Max (22.10.2026): FFN verbietet zu viele Trades unter 5 s, also gezielt etwas suchen, das genau 5 bis 10 s hält, „HFT auf Retail-Art“. Der Überschlag sagt: auf MNQ fressen die Kosten rund ein Drittel der typischen 10-s-Bewegung, die Richtung müsste in rund zwei von drei Fällen stimmen, und mit 1-Minuten-Bars ist das gar nicht testbar. Geparkt, bis die Tickdaten aus AP427 da sind, dann eine Prämissen-Tafel im Juli-Stil.

## 1. Regel-Lage (Stand 22.10.2026)

| Firma | HFT-Regel | Folge für ein 5-bis-10-s-Bein |
|---|---|---|
| FFN | max. 30 % der Trades mit Round-Trip ≤ 5 s je Session, keine Mindestanzahl, Zählbasis (je Strategie oder Konto-FIFO) vom Support unbeantwortet | formal erlaubt, aber Stops unter 5 s zählen in die 30 %, und das Bein mischt sich womöglich mit den anderen Beinen. Verstoß = Konto und Profit weg |
| E8 | mehr als 300 Trades/Tag verboten (Primärquelle), laut Nebenquelle max. 50 % der Trades unter 1 Minute | nach der Nebenquelle **nicht erlaubt** |
| FN | nur „kein HFT-Missbrauch“ | unklar |

Dazu der Geist der Regel: ein Bein, das systematisch knapp über 5 s aussteigt, sieht für ein Risk-Team genau nach dem aus, was die Regel verhindern soll. Quelle: [[Firm-Regeln je Konto]] (HFT-Zeile, Support 05.10. und 09.10.).

## 2. Überschlag Kosten gegen Bewegung (22.10.2026)

Stempel: `qbt.load_rth` NQ/ES, 1-Minuten-Bars bis 16.10.2026, erste Minute je Tag raus, σ der Minuten-Änderung mit Wurzel-Zeit auf 5 und 10 s skaliert (Näherung, unter einer Minute nicht gemessen). Kosten je Round-Trip: Kommission 1,78 $ je Micro ([[Firm-Regeln je Konto]]) plus 1 Tick Spread mit Market-Orders. Nötige Trefferquote unter der Annahme gleich großer Gewinne und Verluste.

| | Kosten RT | typische Bewegung 5 s | typische Bewegung 10 s | Kosten / Bewegung 5 s · 10 s | nötige Trefferquote 5 s · 10 s |
|---|---|---|---|---|---|
| MNQ, 60 Tage | 2,28 $ = 1,14 Pkt (4,6 Ticks) | 2,64 Pkt (5,27 $) | 3,73 Pkt (7,46 $) | 43 % · 31 % | 71,6 % · 65,3 % |
| MNQ, 3 Jahre | 2,28 $ | 2,50 Pkt (5,01 $) | 3,54 Pkt (7,08 $) | 46 % · 32 % | 72,8 % · 66,1 % |
| MES, 60 Tage | 3,03 $ = 0,61 Pkt | | | 141 % · 100 % | nicht erreichbar |
| MES, 3 Jahre | 3,03 $ | | | 119 % · 84 % | nicht erreichbar |

MES ist damit raus, wenn überhaupt, dann nur MNQ.

## 3. Warum die Prämisse schwach aussieht

1. **Kosten:** auf MNQ rund ein Drittel (10 s) bis knapp die Hälfte (5 s) der typischen Bewegung.
2. **Wem die Sekunden-Edge gehört:** laut [[Order-Flow Predictive Research]] lebt Richtungsvorhersage auf Sekunden im Orderbuch (OFI, L2), wirkt meist gleichzeitig statt vorlaufend und wird von Co-Location abgeschöpft. Die Box steht nicht neben der CME und geht über Rithmic/NT8.
3. **Daten:** mit 1-Minuten-Bars liegt ein 10-s-Trade komplett in einer Bar, Reihenfolge von Entry, Exit und Stop unbekannt. Es braucht Ticks mit Bid/Ask.
4. **Denkfehler im Ansatz:** erst die Haltezeit festlegen und dann suchen, was reinpasst, ist Data Mining. Sauber ist ein Mechanismus, der von Natur aus nur Sekunden wirkt (z.B. Stop-Kaskade beim Bruch einer Rundzahl, siehe [[Rundzahlen Wege-Karte]]), und daraus folgt die Haltezeit.

Kein Urteil: nichts gemessen, nur ein Überschlag. Die Idee ist **unentscheidbar**, bis Tickdaten da sind.

## 4. Wiedervorlage

**Bedingung:** AP427 erledigt, also der NT8-Tick-Export `MNQ 12-26` (Last, Bid, Ask, Volumen) für 05.10. bis 20.10.2026 liegt lokal vor. Der Export enthält die vollen Tage, nicht nur 15:54 bis 15:56, es muss also nichts extra geholt werden. **Datei nach der AP426-Auswertung nicht löschen.** Verankert als Notiz am Ticket AP427.

## 5. Prämissen-Tafel, wenn die Ticks da sind (Juli-Stil, eine Tabelle, Stopp wenn sie nicht trägt)

- **Daten:** die AP427-Ticks, RTH 09:30 bis 15:59 ET, Zeitzone wie in `_scratch_ap426/tick_burst.py` gegen die Minuten-Bars prüfen.
- **Zielgröße:** Preisänderung über die nächsten 10 s in Signalrichtung, Einstieg zum Ask/Bid (Market), Ausstieg nach 10 s ebenfalls Market.
- **Signale:** höchstens 3 bis 5, **vor dem Lauf festgelegt**. Vorschlag zum Wiederaufnehmen, Max entscheidet: (a) Aggressor-Ungleichgewicht der letzten 5 s (Volumen am Ask minus am Bid), (b) Bruch des Hochs oder Tiefs der laufenden Minute, (c) Bruch einer runden Zahl (25/50/100 Punkte).
- **Trägt, wenn:** mittlere 10-s-Bewegung in Signalrichtung über 1,14 Pkt (Kosten) und das an der Mehrheit der Tage. Fehlerbalken je Tag (Tages-Cluster), nicht je Trade, sonst täuschen die vielen Signale pro Tag Sicherheit vor.
- **Nicht in der Tafel:** Limit-Orders. Die sparen zwar den Spread, aber die Füllung hängt an der Queue-Position, und die ist aus den Ticks nicht ehrlich abbildbar.
- **Trägt sie:** erst FFN schriftlich fragen (Bein mit systematisch 5 bis 10 s Haltezeit erlaubt? Zählbasis?), E8 klären, dann die üblichen Stufen. **Trägt sie nicht:** Logbuch-Eintrag mit den vier Pflichtfeldern, Kategorie je nach Ergebnis `empirisch-nichts-gefunden` (N Signale) oder `unentscheidbar` (zu wenig Tage).

## 6. Buch-Lücke

Ganz vorne: es fehlt die Prämisse, und davor die Daten, um sie zu prüfen. Danach kämen Regel-Klärung FFN/E8, Gates, Buch-Marginal, NT8-Port.
