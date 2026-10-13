---
tags:
  - projekt/trading
  - sizing
  - track-record
erstellt: 2026-10-12
status: Entwurf, Entscheidung Max offen (Wochenend-Thema)
---
# Hochstuf-Regel je Konto: wann darf ein Konto von k1 auf k2?

⬅️ [[Großes Ziel]] · [[Firm-Regeln je Konto]] · [[Buch-Workflow]] · Tickets AP355 (PB3-Nachzug FFN2), AP356 (NT8-Export Oktober)

> [!summary] In drei Sätzen
> Heute gilt eine Regel für alle Konten: k1, und hoch auf k2, sobald die Schwankung des Buchs unter etwa 400 $ am Tag fällt. Die Messung vom 12.10.2026 zeigt, dass das je Konto sehr verschieden wirkt: auf den 50k-Konten bringt k2 praktisch nie etwas, auf den 150k-Konten bringt k2 Geld, kostet aber die durchgehende Kurve. Vorschlag: eine Regel je Kontogröße und je Belegung, mit einer Schwelle, die zum Ziel „Track Record schützen“ passt.

> [!success] Kernentscheidung Max, 12.10.2026 abends
> **Schwelle fürs Hochstufen auf k2 ist die Track-Record-Variante: 235 $ Tagesschwankung** (FFN 150k, gemessen am eigenen Buch des Kontos, entspricht Puffer = 10-fache Schwankung bei k2). Die alte Schwelle von 400 $ gilt damit nicht mehr. Für das noch nicht gekaufte E8 150k ergibt dieselbe Rechnung etwa 200 $, das wird beim Kauf bestätigt. Die Fragen 2 bis 6 in Abschnitt 7 sind noch offen. **Gemessen wird in Buch-Handelstagen:** 60 Buch-Tage sind beim heutigen Buch rund 16 Wochen, nicht 60 Kalendertage. Die Regel läuft seit 12.10. als Code in den [[Konto-Karten (Rechnung je Konto automatisch)]] (Hochstuf-Ampel je Konto, bei Daten älter als 14 Tage ist Hochstufen gesperrt). Heute ändert das nichts: alle Konten bleiben auf k1.

> [!success] Ergänzung Max, 13.10.2026
> **Der Maßstab hinter den 235 $ ist jetzt ausdrücklich festgelegt: Bust-Chance in 12 Monaten höchstens 30 %.** Die 235 $ bleiben, ohne Abschlag für die Mess-Unschärfe (gemessen 235 $ heißt grob 25 %, im Pechfall etwa 35 %). Neben der gemessenen 60-Tage-Zahl darf künftig auch eine Vola-Schätzung grünes Licht geben, sobald sie die Rückrechnung bestanden hat und ihr vorsichtiger Wert unter der Schwelle liegt. Das System meldet nur, die Größe ändert Max. Damit ist Frage 5 in Abschnitt 7 entschieden. Details: [[Vola-Prognose Agent (Konzept)]], Ticket AP358.

Alles andere hier ist ein **Vorschlag**. Geändert ist nichts, weder am Buch noch am RiskGuard. Zahlen aus `engine/_scratch_trackrecord_1210/` (Quant-Team, 12.10.2026), Daten bis 11.09.2026.

## 1. Worum es geht

**k** heißt: wie viele Micros je Bein ein Konto handelt. k1 ist ein Micro je Bein, k2 sind zwei. Mit k2 verdoppelt sich jeder Tagesgewinn und jeder Tagesverlust. Die Drawdown-Grenze des Kontos wächst dabei **nicht** mit. Mit k2 ist der Weg zur Grenze also halb so lang.

Die Frage ist immer dieselbe Abwägung:

| | mehr Größe bringt | mehr Größe kostet |
|---|---|---|
| Geld | Gewinnziel und Payouts werden schneller erreicht | mehr Busts, jede neue Eval kostet Gebühr und Wartezeit |
| Track Record | mehr Payout-Belege | die Kurve reißt öfter ab, die Beleg-Uhr startet neu |

## 2. Was heute gilt

- k1 auf allen Konten.
- Hochstufen auf k2, wenn die Schwankung des Buchs über 60 Tage unter etwa 400 $ je Micro-Satz und Tag fällt.
- Eine Schwelle für alle Konten und alle Belegungen.

## 3. Warum eine Regel für alle nicht passt

**Grund 1: Die Konten haben sehr verschieden viel Puffer.**

| Konto | Puffer bis zur Grenze | Gewinnziel in der Eval |
|---|---|---|
| FundedNext 50k | 1.500 $ | 2.500 $ |
| E8 50k | 2.000 $ | 3.000 $ |
| E8 150k (geplant) | 4.000 $ | 9.000 $ |
| FFN 150k | 4.700 $ | 9.000 $ |

Die 50k-Konten haben wenig Puffer und ein kleines Ziel: k1 reicht, k2 killt. Die 150k-Konten haben viel Puffer und ein großes Ziel: k1 überlebt fast immer, braucht aber Jahre bis zum ersten Payout.

**Grund 2: Die Konten handeln nicht dasselbe Buch.**

| Konto | Beine | Schwankung je Tag, alle Jahre | letzte 120 Tage |
|---|---|---|---|
| E8 50k, FN1, FN2 | 4 | 235 $ | 459 $ |
| FFN1 | 5 (mit PB3 und RTY-Gap) | 230 $ | 449 $ |
| FFN2 | 3 (ohne PB3) | 192 $ | 330 $ |

Ein Buch mit weniger Beinen schwankt von sich aus weniger. Eine pauschale Schwelle von 400 $ würde FFN2 früher hochstufen als die anderen, obwohl es dort nicht ruhiger ist, sondern nur weniger gehandelt wird.

**Grund 3: Das Ziel hat sich verschoben.** Die 400 $ stammen aus der Rechnung „Zeit bis 50.000 $“. Seit dem 12.10. steht darüber die Leitplanke „Track Record darf nicht kaputtgehen, Überleben vor Tempo“. Dafür ist 400 $ zu locker (siehe Abschnitt 5).

## 4. Die eine Kennzahl, die alles zusammenfasst

**Puffer geteilt durch die Tagesschwankung bei der gewählten Größe.** Anders gesagt: wie viele ganz normale Schwankungstage passen zwischen Kontostand und Grenze.

Aus den Tabellen vom 12.10. abgelesen (geschrumpfte Edge):

| Puffer ist das …-fache der Tagesschwankung | Chance auf 12 Monate ohne Bust | Beispiel |
|---|---|---|
| etwa 4- bis 5-fach | 20 bis 40 % | E8 50k k1 heute, FFN1 k2 heute |
| etwa 7-fach | rund 50 % | FFN2 k2 heute |
| etwa 9- bis 10-fach | 70 bis 80 % | FFN1 k1 heute, E8 150k k1 heute, FFN k2 bei normaler Vola |
| etwa 14-fach | rund 95 % | FFN2 k1 heute |
| 20-fach und mehr | 99 % | 150k-Konten k1 bei normaler Vola |

> [!warning] Einordnung
> Das ist meine Faustregel aus den Simulations-Tabellen, noch keine vom Quant-Team bestätigte Formel. Sie hängt auch am Sharpe: mit ungeschrumpfter Edge liegen alle Überlebensquoten höher. FundedNext fällt etwas aus der Reihe, weil dort zusätzliche Regeln greifen. Der Mathematiker hat dieselbe Idee als Formel (theta) aufgeschrieben, die Kipplinie je Kontotyp ist als offene Aufgabe notiert.

**Die andere Seite der Medaille:** bei 20-fach und mehr überlebt das Konto, zahlt aber nicht aus. Ein 150k-Konto mit k1 bei normaler Vola braucht im Median über 36 Monate bis zum ersten Payout. Zu viel Sicherheit ist auch kein Track Record.

## 5. Vorschlag: die Regel in sechs Bausteinen

**Baustein 1: 50k-Konten bleiben immer bei k1.**
Der Puffer ist dort schon mit k1 nur das 6- bis 9-fache einer normalen Tagesschwankung. In keiner Rechnung hat k2 dort verlässlich mehr Geld gebracht, in jeder mehr Busts.

**Baustein 2: Erst mehr Beine, dann mehr Größe.**
Ein zusätzliches unabhängiges Bein bringt fast so viel wie k2, bei deutlich besserem Überleben. Gemessen an FFN2: PB3 und RTY-Gap nachziehen bringt rund +3.100 $ in 36 Monaten bei 77 % ohne Bust, k2 auf drei Beinen +3.200 $ bei 52 %. Kein Konto wird hochgestuft, solange es weniger Beine handelt als das volle Buch (AP355).

**Baustein 3: 150k-Konten dürfen auf k2, wenn der Puffer auch mit k2 noch mindestens das 10-fache der Tagesschwankung ist.**
Gemessen wird die Schwankung **der eigenen Belegung** des Kontos, nicht pauschal.

| Konto | Puffer | k2 erlaubt, wenn die Tagesschwankung des eigenen Buchs höchstens … | heute (120 Tage) |
|---|---|---|---|
| FFN 150k | 4.700 $ | etwa 235 $ | FFN1 449 $, FFN2 330 $ |
| E8 150k | 4.000 $ | etwa 200 $ | 459 $ |

Das ist deutlich strenger als die heutigen 400 $. Mit 400 $ wäre der Puffer bei k2 nur noch das 5- bis 6-fache, also eine Chance von grob 25 bis 50 % auf 12 Monate ohne Bust. Das passt zum Ziel „schnell zu 50k“, nicht zum Ziel „durchgehende Kurve“. **Welche der beiden Schwellen gilt, ist die Kernentscheidung.**

**Baustein 4: Zurückstufen ist Pflicht und geht sofort.**
Steigt die Schwankung wieder über die Schwelle (mit etwas Abstand, damit es nicht hin und her springt, zum Beispiel ab dem 1,25-fachen), geht das Konto zurück auf k1. Hochstufen nur am Wochenende, Zurückstufen jederzeit.

**Baustein 5: Der Tagesstopp im RiskGuard wird mitentschieden.**
Heute 2.500 $ auf den 150k-Konten bei k1. Bei k2 gibt es zwei Möglichkeiten: der Stopp wächst mit (5.000 $, dann greift er praktisch nie) oder er bleibt bei 2.500 $ (dann kostet er bei hoher Vola rund 500 bis 900 $ in 36 Monaten, schützt aber besser). Für den Track Record spricht mehr für den festen Stopp.

**Baustein 6: Jede Stufe wird festgehalten.**
Datum, Konto, alte und neue Größe, gemessene Schwankung, Grund. Damit bleibt der Record erklärbar.

## 6. Was das heute heißt

- **Nichts ändert sich.** Die Schwankung ist hoch, überall bleibt k1.
- Die Schwankung fällt am Markt bereits. Die 60-Tage-Messung des Buchs zeigt das voraussichtlich ab Ende November.
- Mit der strengen Schwelle (Baustein 3) käme k2 auf FFN erst in Frage, wenn die Schwankung wieder auf Normalniveau ist. Mit der heutigen Schwelle von 400 $ käme es früher, bei schlechterem Überleben.

## 7. Was du entscheiden musst

| Nr. | Frage | Meine Empfehlung |
|---|---|---|
| 1 | Schwelle fürs Hochstufen der 150k-Konten: Tempo (400 $) oder Track Record (etwa 235 $ FFN, 200 $ E8 150k)? | Track Record, passt zur Leitplanke vom 12.10. |
| 2 | 50k-Konten fest auf k1? | Ja |
| 3 | „Erst Beine, dann Größe“ als feste Reihenfolge? | Ja |
| 4 | Tagesstopp bei k2: fest oder mitwachsend? | Fest bei 2.500 $ |
| 5 | Womit wird die Schwankung gemessen: 60 Tage des Buchs (träge, hängt Monate nach) oder aus der aktuellen Tagesspanne des Markts abgeleitet (schneller, aber eine Schätzung)? | Beides anzeigen, entscheiden muss die trägere Zahl |
| 6 | Soll ein Konto vor dem Hochstufen schon einen Payout geliefert haben? | Auf den 150k-Konten nein: mit k1 kommt dort der erste Payout zu spät, die Bedingung würde das Hochstufen praktisch verbieten |

## 8. Was noch fehlt, bevor die Regel gilt

1. Daten bis Oktober (AP356), dann die Schwankung je Belegung neu messen.
2. Der Mathematiker liefert die Schwelle als Formel je Kontotyp statt meiner Faustregel aus Abschnitt 4.
3. Die Regel einmal mit beiden Schwellen durch die Flotten-Rechnung schicken (gemeinsamer Kalender, Auslage-Deckel 2.500 $, Nulldrift-Kontrolle).
4. Wenn entschieden: in [[Firm-Regeln je Konto]] und in die Wochenend-Prüfung eintragen, RiskGuard-Werte je Konto ableiten.

## 9. Was dagegen spricht (ehrlich)

- Die Überlebenszahlen sind Simulation. HFT-Regel, News-Sperre und Inaktivitätsregel von FFN sind nicht mitgerechnet, die echten Quoten liegen eher darunter.
- Welcher Sharpe wirklich gilt (geschrumpft 1,2 oder Backtest 2,1), entscheidet erst die Live-Zeit. Mit dem höheren Sharpe wäre die strenge Schwelle zu vorsichtig.
- Mit k1 liefern die 150k-Konten im ersten Jahr im Median keinen Payout. Wer Payout-Belege will, kommt um die Frage „mehr Beine oder mehr Größe“ nicht herum. Die Regel verschiebt das nur auf die sichere Reihenfolge.
