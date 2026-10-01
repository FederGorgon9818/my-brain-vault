---
tags: [projekt, gate, konzept]
date: 2026-09-29
status: Konzept, Entscheidung Max
---

# Überoptimierungs-Prüfung Stufe 2 (Konzept 29.09.2026)

Auftrag Max: klar erkennen, ob ein Next-Week-Bein nur durch Nachoptimieren gut ist, ohne es wie frühere Gates zu überkomplizieren. Entstanden per Workflow (3 Entwürfe: Statistik, Struktur/Nachbarn, Praktiker; bewertet von verdict-auditor und pipeline-auditor gegen die Fehlerliste; Synthese mit Nachrechnung). Verwandt: [[Latte-Audit (25.09.2026)]], CLAUDE.md Abschnitt Gate v4, Ticket AP275. Skripte: `engine/_scratch_latte/ueberopt/`.

## Überoptimierungs-Check in Stufe 2: „Was konnte die erste Fassung?"

**Die Idee.** Jede Idee hatte eine erste Fassung, bevor wir auf denselben Daten Runde um Runde daran geschraubt haben. Das Glück aus dem Nachschrauben steckt genau im Abstand zwischen dieser ersten Fassung und dem Bein von heute. Wir schauen deshalb nur zwei Dinge an:
1. War die erste Fassung schon belegt gut?
2. Ist das Next-Buch auch dann noch schneller bei 50k, wenn jedes Bein nur die Edge seiner ersten Fassung behalten darf?

**Warum nicht zählen und nicht Nachbarn anschauen.** Beides trennt am Prüfset nachweislich nicht.
- Unsere eigenen Familien sind größer als die der Nieten: 882, 367 und 345 Trials gegen 241 bei GAPFADE.
- Die schärfsten Parameter-Spitzen sitzen in unseren eigenen Beinen, zum Beispiel das 15-Minuten-Signal bei Momentum und die 240-Minuten-Referenz bei LastHour.

Beides fliegt komplett raus.

### Was die „erste Fassung" ist
- Die Config, mit der die Idee dastand, bevor wir sie auf den Daten nachgeschärft haben. Sie stand fest, bevor getunt wurde, also kann das Tuning sie nicht schönrechnen.
- **Neues Bein aus der Discovery:** die Basis des ersten Jobs seiner Linie.
- **Ersatz-Bein:** Die Linie geht zurück bis zur ersten Fassung des Originals. PB3 ersetzt Momentum, also ist seine erste Fassung die Juli-Version von Momentum.
- **Erster Job war nur ein Gerüst ohne feste Config:** Dann zählt das Walk-Forward-Ergebnis aus Stufe 1, dort ist die Auswahl schon ehrlich eingerechnet.
- **Unsere drei Juli-Beine:** einmal auf den Buchstand vom 09.08. festnageln. Den Stand habe ich mit dem Backup abgeglichen, er stimmt.
- **Ab dem Einbau** schreibt die Box die erste Fassung beim Übernehmen ins Next-Buch gleich mit, und zwar in eine Begleitdatei neben dem Buch, nicht ins Buch selbst.

### Prüfung 1: War die erste Fassung schon gut?
- **Was gerechnet wird:** der Sharpe-Beleg der ersten Fassung, also t = Sharpe × Wurzel(Jahre), über die volle Historie mit der aktuellen Engine. Das ist dieselbe Zahl wie beim Sharpe-Beleg in den Vor-Gates.
- **Regel:** Liegt t unter 2, bekommt das Bein die Markierung „erste Fassung nicht belegt". Die 2 ist die bestehende Latte aus den Vor-Gates, keine neue Zahl.
- **Rauschband:** das 90-%-Band des Sharpe der ersten Fassung. Dazu kommt als Info der Tuning-Zuwachs, also heutiges Bein minus erste Fassung, gepaart und mit Fehlerbalken.
- **Ehrlich dazu:** Bei 10,6 Jahren Daten bekommt auch eine echte, aber mittelmäßige Idee (Sharpe 0,65) diese Markierung in rund 45 % der Fälle. Momentum (2,10) und Asia (2,07) liegen genau auf der Linie.
- Deshalb erklärt Prüfung 1 nur, sie urteilt nicht. Die Empfehlung im Bericht kommt allein aus Prüfung 2.

### Prüfung 2: Ist das Next-Buch auch ohne Tuning-Gewinn schneller?
- **Neue dritte Spalte** im Wochenend-Check, neben „Shrink 0,58" und „letzte 3 Jahre": die Spalte **„erste Fassung"**.
- **Jedes Bein beider Bücher** bekommt dort nur die Edge seiner ersten Fassung. Die Drift geht runter, Schwankung und Handelstage bleiben gleich. Wer besser ist als seine erste Fassung, wird also gestutzt, egal ob Bestand oder Neuling.
- **Danach ganz normal:** Zeit bis 50k im Kalender-Modus mit RiskGuard-Stopp, über **5 Seeds**, gepaart gegen das echte Buch in derselben Spalte.
- **Regel:** Der Vorsprung trägt, wenn er größer ist als 2 Standardfehler. Sonst erscheint der Hinweis „mit der Edge der ersten Fassung nicht belegt (Differenz ± SE)". Da steht nie „nein" oder „tot".
- **Sonderfall Ersatz in derselben Linie** (PB3 statt Momentum):
  - Beide haben dieselbe erste Fassung und in der Spalte deshalb dieselbe Edge. Die Spalte sagt dann nur: „Der Vorteil ist reiner Tuning-Gewinn."
  - Daneben steht der Tuning-Schritt mit Fehlerbalken. PB3 gegen Momentum liegt bei +0,39 ± 0,22 Sharpe, und da ist die Auswahl noch nicht abgezogen.
  - Ob dieser Gewinn hält, zeigen nur frische Tage.
- **Das ersetzt die heutige Glücksbereinigung komplett:** Familien-Zählung, 100er-Regel, 3-fach-Regel und den Abzug der Zufallsdecke nur beim Neuling. Die alte Bereinigung hat einseitig nur Neulinge bestraft und hätte unsere eigenen Beine selbst auffällig gemacht.

### Was im Wochenend-Bericht steht
1. **Eine Tabelle je Bein (beide Bücher):** erste Fassung mit Quelle und Datum, t der ersten Fassung mit 90-%-Band, Tuning-Zuwachs ± SE, Markierung ja oder nein.
2. **Eine Zeile mehr in der Spalten-Tabelle:** „erste Fassung" mit Median, Differenz zum echten Buch ± SE und der Lesart „trägt" oder „nicht belegt".
3. **Eine Info-Zeile je Bein:** frische Handelstage seit dem ersten Blick auf die Idee. Heute ist das praktisch 0, weil die Daten am 06.08. enden.
4. **Ein fester Satz:** „Ob die ganze Idee samt erster Fassung Glück war, lässt sich auf denselben Daten nicht prüfen. Das klären nur frische Tage."

**So sähe es diese Woche aus** (gerechnet, 5 Seeds):
- **OpenDrive:** erste Fassung t 2,64. Das Bein trägt auch ohne Tuning-Gewinn, das Buch ist damit 12,1 ± 1,1 Monate schneller.
- **PB3 statt Momentum:** Die erste Fassung ist das Juli-Momentum mit t 2,10. In der neuen Spalte ist der Vorsprung nicht belegt (1,9 ± 1,3 Monate). Roh bringt der Tausch zusätzlich zu OpenDrive 7,4 Monate, und die kommen komplett aus dem Tuning-Gewinn.
- **Next-Buch gesamt:** trägt (11,2 ± 1,5 Monate schneller), und zwar wegen OpenDrive.

### Was NICHT passiert
- Kein Bein wird ausgeschlossen, gesperrt oder automatisch aus dem Next-Buch genommen. Beide Prüfungen liefern nur Text für deine Entscheidung am Wochenende.
- Es gibt keine Trial-Zählung, keine Familiengröße und keine Zufallsdecke als Latte.
- Es gibt keine Nachbar-, Plateau- oder „bestes Jahr raus"-Lampe.
- Stufe 1 und die automatische Übernahme ins Next-Buch bleiben, wie sie sind.
- Zerfall wie bei VWAP-Pullback ist nicht Aufgabe dieses Checks. Den deckt die Spalte „letzte 3 Jahre" ab.

### Was der Check grundsätzlich nicht kann
- **Glück der ganzen Idee samt erster Fassung:** auf denselben Daten nicht prüfbar, das zeigen nur frische Tage.
- **Tuning vor der ersten dokumentierten Fassung:** sieht er nicht. Die Juli-Beine wurden auch schon aus Juli-Sweeps gewählt, der Test ist für sie also milder.
- **Ob ein Tuning-Schritt die Auswahl überlebt:** misst er nicht. Er sagt nur, ob die Entscheidung am Tuning hängt.

### Aufwand für den Einbau (rund 1 Arbeitstag, vor dem 03.10. machbar)
1. **Erste Fassungen festhalten:** eine Begleitdatei für die 3 eigenen Beine und die 2 Next-Beine, etwa 30 Minuten.
2. **Wochenend-Check umbauen,** etwa 2 bis 3 Stunden:
   - Familien-Zählung und Glücksbereinigung raus, das sind rund 100 Zeilen weniger.
   - Prüfung 1 rein: 5 bis 8 Backtests, unter 1 Minute Laufzeit.
   - Prüfung 2 als dritte Spalte mit 5 Seeds.
3. **Selbsttest mit dem Prüfset,** etwa 1 Stunde. Er prüft: eigene Beine ohne Hinweis, GAPFADE mit Hinweis, und bei Edge 0 mindestens 95 % Markierung.
4. **Box schreibt die erste Fassung beim Übernehmen mit,** etwa 1 bis 2 Stunden inklusive Regressionstest, Box-Sync und Runner-Neustart. Das kann eine Woche später kommen. Bis dahin trägt Claude die erste Fassung am Wochenende von Hand nach, das sind nur wenige Beine pro Woche.

**Laufzeit:** Der Wochenend-Lauf wird um rund 30 bis 40 Minuten länger, weil die neue Spalte 5 Seeds braucht.

## Zahlen am Prüfset

## Prüfset für das gewählte Konzept (Statistik-Entwurf mit den Auflagen beider Auditoren)

**Urteil in einem Satz:** Das Konzept trägt am Prüfset.
- Die eigenen Beine sind 3/3 unauffällig, in Prüfung 2 mit großem Abstand.
- GAPFADE fällt in beiden Prüfungen auf.
- VWAP-Pullback fällt nicht auf. Das ist Zerfall, keine Nachoptimierung.
- OpenDrive trägt, PB3 trägt nur über den Tuning-Gewinn.

**Stempel:**
- Engine 9cc1bcffa899a2a4.
- Daten: NQ 2016 bis 06.08.2026 (10,6 Jahre), RTY ab 25.07.2017 (9,0 Jahre).
- Bücher: book_state.json (Stand 18.09.) und book_state_next.json (Stand 29.09.).
- Juli-Erstfassungen geprüft gegen book_state.json.bak-20260809-pre066, sie stimmen.

### Prüfung 1: t der ersten Fassung (Regel: Markierung, wenn t unter 2)

| Bein | Rolle | erste Fassung | t | 90-%-Band Sharpe | Tuning-Zuwachs ± SE | Chance auf Markierung bei Wiederholung* | Markierung |
|---|---|---|---|---|---|---|---|
| NQ_Momentum_d260818 | Buch | Juli, Stand 09.08. | 2,10 | 0,17 bis 1,08 | +0,21 ± 0,25 | 45 % | nein, liegt auf der Linie |
| NQ_LastHour_v3 | Buch | v1, Stand 09.08. | 3,25 | 0,54 bis 1,45 | +0,11 ± 0,27 | 7 % | nein |
| NQ_Asia-Dir-USopen_d260820 | Buch | Stand 09.08. | 2,07 | 0,17 bis 1,07 | +0,15 ± 0,14 | 46 % | nein, liegt auf der Linie |
| GAPFADE-RT | Niete | RTY_Gap-fade, Stand 09.08. | **1,09** | -0,12 bis 0,86 | +0,55 ± 0,30 (60 % des Sharpe) | 84 % | **ja** |
| NQ_VWAP-Pullback | Niete (Zerfall) | gleich dem Bein | 3,07 | 0,49 bis 1,38 | 0 | n/a | nein |
| NQ_Momentum_PB3_fa01b | Next, Ersatz | Kette zum Juli-Momentum | 2,10 | 0,17 bis 1,08 | +0,60 ± 0,22 gegen Juli, +0,39 ± 0,22 gegen d260818 | 45 % | nein |
| NQ_OpenDrive_maband2050 | Next, neu | Basis des wide-Jobs vom 28.08. | 2,64 | 0,35 bis 1,31 | +0,65 ± 0,31 | 24 % | nein |
| AS-07 | optional | Gerüst, daher Walk-Forward aus Stufe 1 | 2,56 | 0,43 bis 1,30 | n/a | n/a | nein |
| NQ_Momentum_d260821 | Retune, in #126 verworfen | Kette zum Juli-Momentum | 2,10 | wie Momentum | -0,27 ± 0,32 gegen d260818 (das Bein selbst hat t 1,91) | 45 % | nein. Prüfung 1 sieht Retunes derselben Linie nicht. |

*Chance auf Markierung bei Wiederholung: Die Tages-PnL der ersten Fassung wird mit Block-Bootstrap neu gezogen (Block 10, 2000 Ziehungen), wobei die wahre Edge gleich der gemessenen ist. Gezählt wird der Anteil der Ziehungen mit t unter 2.

**Wie oft die Markierung kommt**, gerechnet auf den echten Tages-PnL der 5 ersten Fassungen. Die Tages-PnL wird auf den Ziel-Sharpe verschoben und per Block-Bootstrap neu gezogen:

| wahrer Sharpe | Anteil mit Markierung (Spanne über die 5 Fassungen) |
|---|---|
| 0 (keine Edge, egal wie viel getunt wurde) | 98,1 bis 98,7 % |
| 0,3 | 85 bis 89 % |
| 0,5 | 64 bis 70 % |
| 0,65 | 44 bis 51 % |
| 0,8 | 24 bis 34 % |
| 1,0 | 7 bis 13 % |

- **Null-Idee, bei der schon die erste Fassung aus k Varianten ausgesucht wurde:** Die Markierung kommt in 98,6 % (k=1), 95,9 % (k=3), 93,2 % (k=5) und 86,8 % (k=10) der Fälle.
- **Nulldrift-Zwillinge aus dem Entwurf:** 4 von 140 liegen über 2, also 2,9 % bei einem Soll von 2,3 %.
- „Kalibriert" im strengen Sinn ist das nicht: Die Latte wurde übernommen, und die Tabelle zeigt ihre Trefferquoten.

### Prüfung 2: Spalte „erste Fassung", Zeit bis 50k
**Setup:** 5 Seeds (101, 202, 303, 404, 505) mit je 240 Sims, also 1200 gepaarte Sims. Kalender-Modus mit RiskGuard-Stopp. Das SE kommt aus dem Bootstrap über die Sims, zusätzlich ist die Spanne der Seeds angegeben. Ein * heißt: um mindestens 2 SE schneller.

| Variante | roh: Differenz zum echten Buch | Spalte „erste Fassung": Differenz | Seed-Spanne in der Spalte | Lesart |
|---|---|---|---|---|
| echtes Buch (Median) | 64,2 ± 1,2 Monate | 81,7 ± 1,4 Monate | | |
| Next-Buch | -24,1 ± 1,1 * | -11,2 ± 1,5 * | -9,7 bis -13,1 | trägt |
| echt + OpenDrive | -16,7 ± 1,0 * | -12,1 ± 1,1 * | -9,0 bis -15,0 | trägt |
| PB3 ersetzt Momentum | -14,6 ± 1,0 * | -1,9 ± 1,3 | +1,3 bis -4,7 | nicht belegt, reiner Tuning-Gewinn |
| echt + PB3 | -18,5 ± 1,0 * | -1,0 ± 1,5 | +3,3 bis -5,3 | nicht belegt |
| Next gegen echt + OpenDrive (was der PB3-Tausch zusätzlich bringt) | -7,4 ± 0,5 * | +0,9 ± 1,2 | +2,3 bis -1,0 | nicht belegt |
| **echt + GAPFADE (Niete)** | **-4,9 ± 0,8 *** | **-0,3 ± 0,9** | +4,6 bis -1,8 | **Hinweis:** roh belegt schneller, ohne Tuning-Gewinn nichts |
| d260821 ersetzt Momentum (Retune) | +10,0 ± 1,2 (langsamer) | +3,7 ± 1,3 (langsamer) | | fällt schon roh durch |
| echt ohne Momentum | +28,7 ± 1,4 | +33,1 ± 1,8 | | eigenes Bein trägt |
| echt ohne LastHour | +55,8 ± 1,3 | mindestens +38,3 ± 1,4 (Median bei 120 Monaten gekappt) | | eigenes Bein trägt |
| echt ohne Asia | +21,0 ± 1,1 | +33,6 ± 1,6 | | eigenes Bein trägt |

- Faktoren in der Spalte (Edge der ersten Fassung geteilt durch Edge des Beins):
  - Momentum 0,75, LastHour 0,90, Asia 0,81
  - PB3 0,52, OpenDrive 0,56, GAPFADE 0,40
  - d260821 1,0 (das Bein ist schlechter als seine erste Fassung)
- Heutige einseitige Logik zum Vergleich (Entwurf, 1 Seed): Das Next-Buch kommt nur auf -4,3 statt -16,9 Monate, also rund 12,6 Monate Verzerrung gegen die Neuen.

### Abnahme
- **Eigene Beine:**
  - Prüfung 1: 3/3 unauffällig. Momentum und Asia liegen ohne Puffer auf der Linie, jeweils mit rund 45 % Chance, beim nächsten Datenstand oder nach einem Engine-Fix zu kippen.
  - Prüfung 2: 3/3. Jedes eigene Bein bringt auch mit der Edge seiner ersten Fassung 33 bis 38 Monate, roh 21 bis 56 Monate, jeweils mit mindestens 18 SE Abstand.
- **Nieten:**
  - GAPFADE fällt in beiden Prüfungen auf.
  - VWAP-Pullback fällt in keiner auf. Laut #161 ist das Zerfall (2.814 auf 956 $ pro Jahr) plus ein kaputtes Why, keine Nachoptimierung. Alle drei Entwürfe und beide Auditoren sagen: Soll umetikettieren. Nach altem Soll ist das 1 von 2, nach korrigiertem 1 von 1.
  - Ehrlich: Getrennt wird mit nur einer echten Tuning-Niete.
- **Next-Beine:** OpenDrive trägt. Bei PB3 ist der Vorsprung nicht belegt, er hängt am Tuning-Gewinn.
- **Buch-Lücke:** Beide Next-Beine stehen schon im Next-Buch. Es fehlen nur noch das Wochenend-Review und der NT8-Deploy.
- **Retune derselben Linie (d260821):** Prüfung 1 ist blind dafür (das Bein erbt das Juli-t), in Prüfung 2 bekommen beide dieselbe Edge. Die normale roh-Spalte fängt ihn trotzdem, dort ist er 10 Monate langsamer.

### Nebenbefunde
- **Median-Gleichheit auf 14 Stellen aus dem Entwurf:** Im Neulauf mit 5 Seeds kommt sie nirgends vor, pro Seed sind nur 17 bis 23 von 240 Werten gleich. Die Monate sind Tage geteilt durch Tage pro Monat, also diskret. Die Gleichheit war ein Zufall zweier Mediane, die auf dieselbe Tageszahl fielen.
- **Leicht andere Zahlen als im Entwurf** (echtes Buch roh 64,2 statt 63,3 Monate): Die gemeinsame Tagesachse ist durch die zwei Zusatzbeine größer (19,1 Tage pro Monat), und es sind 5 Seeds statt einem. Die Aussagen bleiben gleich.
- **Nulldrift-Zwilling von tsmom nicht zentriert** (t-Mittel +1,32): Das gehört an den pipeline-auditor und betrifft Stufe 1, nicht dieses Konzept.

### Probeläufe, Dateien
- **Gerechnet:** 5 neue Backtests, 7 Backtests für die Zellen und 100 Flotten-Läufe (7692 s, 3 Prozesse). Alles nur gezählt, nichts im Register. Keine Engine- oder Buch-Datei geändert.
- **Skripte und Ergebnisse** in `C:\Users\maxlk\Projects\trading-data\engine\_scratch_latte\ueberopt\`:
  - `final_01_p1.py` schreibt `final_01_p1.json` (Trefferquoten, Kette d260821).
  - `final_02_spalte5.py` schreibt `final_02_raw.json` und `final_02_log.txt`.
  - `final_03_eval.py` schreibt `final_03_eval.json`.
  - `final_04_next_vs_od.py`.
  - Dazu die Entwurfsdateien `erstbefund.json`, `kette.json`, `kalibrierung.json`.

### Technische Notiz für die Session, die das einbaut
**In `weekend_check.py`:**
- `FAM_ABS`, `FAM_REL`, `luck_adjust` und die N-Logik in `herkunft_eval` raus.
- Neue Spalte „erstfassung": je Bein vor `variant_cells` skalieren, Vorlage ist `scale_drift` in `final_02_spalte5.py`.
- Seed pro Job setzen statt über das Modul-`SEED`.
- Regel: belegt, wenn Differenz ≤ -2 × max(SE aus Bootstrap, Seed-Streuung / Wurzel 5).
- `regime_eval` urteilt heute für shrink058 und recent3y nur nach dem Punktwert (Differenz < 0). Das beim Einbau auf 2 SE mitziehen.

**Außerhalb:**
- Pins in eine Begleitdatei, nicht in `book_state.json`.
- `promote_next` schreibt den Pin.
- Prüfset-Fälle in `test_gate_v4.py` aufnehmen.
- Danach engine-regression-tester, Box-Sync und Runner Stop, Sync, Start.

## Fehlerliste

## Fehlerliste 1 bis 8, geprüft am gewählten Konzept

**(1) Globale Trial-Zählung als Hartlatte: vermieden.**
- Keine der beiden Prüfungen nutzt ein N. Das Register dient nur dazu, die Linie eines Beins zu finden (Ersatz geht zurück bis zum Original).
- Beleg, warum Zählen hier falsch wäre:
  - Bei gemeinsamem N=50 liegt der DSR von GAPFADE bei 0,68 und der von Momentum bei 0,70, beide sind also nicht zu unterscheiden.
  - Mit dem Familien-N liegen Momentum (0,34) und Asia (0,36) sogar unter GAPFADE (0,47).
  - Die eigenen Familien sind größer als die der Nieten: 882, 367 und 345 gegen 241.

**(2) Rangstabilität statt Edge: vermieden.**
- Prüfung 1 misst das Edge-Niveau einer festen Config, Prüfung 2 misst Monate bis 50k. Es gibt keine Ränge, keinen Rangvergleich zwischen IS und OOS und keine Plateau-Logik.
- Nachbar- und Plateau-Tests wurden verworfen, und zwar gerechnet: Sie mahnen die Zeit-Achsen unserer Beine an (15 und 240 Minuten) und lassen beide Nieten durch (Mathe 0 von 2, Praktiker 0 von 2).

**(3) Proxy statt Statistik: vermieden.**
- Prüfung 1 nutzt denselben Sharpe-Beleg wie die Vor-Gates.
- Prüfung 2 ist das Entscheidungskriterium selbst: Zeit bis 50k mit RiskGuard-Stopp.
- Es geht weder um Frequenz noch um die Anzahl der Parameter.

**(4) Schwellen nach Vorfall statt nach Kalibrierung: vermieden, mit einem Rest.**
- Die 2 in Prüfung 1 ist die bestehende Vor-Gate-Latte, die 2 SE in Prüfung 2 sind die bestehende Wochenend-Regel. Am Prüfset wurde nichts nachjustiert.
- Das Wort „kalibriert" fliegt raus. Stattdessen stehen die gemessenen Trefferquoten da:
  - bei Edge 0: 98 bis 99 %
  - bei Sharpe 0,65: rund 45 %
  - bei Sharpe 0,8: 24 bis 34 %
- **Rest:** Die erste Fassung der Juli-Beine ist einmal Ermessen, dafür gibt es Entscheidung 1 an Max. Die Empfindlichkeit ist geprüft, Prüfung 1 kippt bei keiner Alternative: Momentum 18.08. t 2,60, LastHour TN04 t 3,18, GAPFADE mit breiterer Basis t 1,43.

**(5) Einseitig nur den Kandidaten bestrafen: vermieden.**
- Beide Prüfungen laufen für jedes Bein beider Bücher mit derselben Regel.
- Gemessen: Die heutige einseitige Bereinigung verzerrt um rund 12,6 Monate gegen das Next-Buch.
- Symmetrisch gerechnet tragen die eigenen Beine trotzdem deutlich: Ohne jedes einzelne eigene Bein ist das Buch 33 bis 38 Monate langsamer, mit mindestens 18 SE Abstand.

**(6) Entscheidung auf Punktschätzung ohne Rauschband: vermieden, mit einem Rest.**
- Prüfung 1: t ≥ 2 ist selbst eine 2-SE-Regel, dazu kommt das 90-%-Band.
- Prüfung 2: 2 SE über 5 Seeds mit 1200 gepaarten Sims, die Spanne der Seeds wird ausgewiesen.
- **Rest:** Die Unsicherheit der ersten Fassung (bei Momentum Band 0,17 bis 1,08) steckt nicht im Band von Prüfung 2. Prüfung 2 ist ein Szenario („Tuning-Gewinn gleich null"), kein Test. Deshalb gibt sie nur einen Hinweis.
- **Zweiter Rest:** Die bestehenden Spalten shrink058 und recent3y urteilen heute nur nach dem Punktwert. Das sollte beim Einbau gleich auf 2 SE umgestellt werden.

**(7) So kompliziert, dass es keiner nachvollzieht: vermieden.**
- Es gibt eine Zahl je Bein, eine Spalte mehr und eine Frage an Max: „War die erste Fassung schon gut, und ist das neue Buch auch ohne Tuning-Gewinn schneller?"
- Der Code wird kürzer, weil die Familien-Zählung rausfliegt.
- **Rest:** Die Regel für die erste Fassung braucht die Kette (Ersatz führt zum Original) und einen Ausweg für Gerüst-Jobs (Walk-Forward aus Stufe 1).

**(8) Gate, durch das das eigene Buch nicht kommt: vermieden, aber in Prüfung 1 ohne Puffer.**
- Prüfung 1 liefert 3/3, aber Momentum (2,10) und Asia (2,07) liegen genau auf der Linie. Ein Engine-Fix oder mehr Daten können die Markierung mit je rund 45 % Chance umwerfen.
- Genau deshalb löst Prüfung 1 allein keine Empfehlung aus.
- Prüfung 2 liefert 3/3 mit großem Abstand.

**Was offen bleibt:**
- Die Trennschärfe beruht auf einer einzigen echten Tuning-Niete (GAPFADE).
- VWAP-Pullback muss als Zerfalls-Niete umetikettiert werden.
- Retunes derselben Linie sieht die Überoptimierungs-Prüfung nicht. Sie fallen aber in der normalen roh-Spalte auf (d260821 ist dort 10 Monate langsamer).

## Offene Entscheidungen

1. **Die drei Juli-Beine bekommen als erste Fassung den Buchstand vom 09.08.?** Das ist eine einmalige Festlegung, danach gilt die Regel.
   - Ich habe die Alternativen gerechnet (Momentum Stand 18.08., LastHour TN04, GAPFADE mit breiterer Basis). Prüfung 1 kippt dabei nirgends.
   - Bei PB3 in Prüfung 2 hängt das Ergebnis an der Kettenregel, also daran, dass PB3 als Ersatz auf das Juli-Momentum zurückgeht. Würde man PB3 stattdessen an seiner eigenen Job-Basis festnageln, bekäme es den Tuning-Schritt von Momentum zwischen Juli und August geschenkt.
   - Empfehlung: ja, Stand 09.08., und die Kettenregel so lassen.

2. **Darf die Markierung aus Prüfung 1 allein einen Hinweis in der Empfehlung auslösen?**
   - Empfehlung: nein, sie steht nur als Erklärung daneben.
   - Grund: Momentum (2,10) und Asia (2,07) liegen genau auf der Latte. Jedes der beiden würde die Markierung mit rund 45 % Chance bekommen, obwohl es echt ist.
   - Prüfung 2 hat am Prüfset allein sauber getrennt: GAPFADE bekommt einen Hinweis, OpenDrive trägt, die eigenen Beine tragen mit großem Abstand.

## Verworfen (gerechnet)
- **Zählen (Familiengröße, Zufallsdecke je Familie):** trennt nicht, unsere eigenen Familien sind größer als die der Nieten (882/367/345 gegen 241), DSR bei jedem N gleich für GAPFADE und Momentum.
- **Nachbarschafts-/Spitzen-Test:** 0/2 Nieten erkannt; Glück aus vielen Runden steckt in den Trades, die alle Nachbarn teilen, deshalb strukturell blind.
- **Praktiker (Viertel-Drehung, bestes Jahr raus):** mahnt eher unsere eigenen Beine an (15-min-Signal, 240-min-Referenz) als die Nieten.
