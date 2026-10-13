---
tags:
  - projekt/trading
  - sizing
  - agent
  - konzept
erstellt: 2026-10-13
status: Konzept, Entscheidung Max offen (nichts gebaut, nichts gerechnet)
---
# Vola-Prognose Agent: wohin läuft die Schwankung, und was heißt das für die Größe?

⬅️ [[Hochstuf-Regel je Konto (Entwurf)]] · [[Konto-Karten (Rechnung je Konto automatisch)]] · [[Firm-Regeln je Konto]] · [[Großes Ziel]]

> [!summary] In drei Sätzen
> Heute entscheidet eine Zahl über die Größe: die Schwankung des eigenen Kontobuchs über 60 Buch-Tage. Die ist sicher, aber träge, sie hängt rund 16 Wochen nach. Der Vola-Agent sagt dazu, wie wild die **kommenden** Wochen voraussichtlich werden und wann die träge Zahl die Schwelle erreichen kann, und er darf uns nur vorsichtiger machen, nie mutiger.

Anlass: Max, 13.10.2026 („Time Series Vola-Prognose können wir machen, um die Sizing-Entscheidung zu erleichtern“). Das Konzept beantwortet die offene Frage 5 aus der [[Hochstuf-Regel je Konto (Entwurf)]]: träge Messung oder schnelle Schätzung?

**Stand:** Entwurf Claude, am 13.10. vom Quant-Team gegengelesen (nur Methode, nichts gerechnet). Deren Korrekturen sind eingearbeitet und in Abschnitt 11 aufgelistet.

## 1. Welche Frage der Agent beantwortet

Genau drei, immer dieselben:

1. **Wo steht die Schwankung heute?** Markt (NQ, RTY) und eigenes Buch je Konto.
2. **Wie wild werden die nächsten 4 und 8 Wochen?** Erwartete Tagesschwankung des Kontobuchs an den kommenden Handelstagen, mit Spannweite.
3. **Was heißt das für die Größe?** Wann kann ein Konto frühestens unter seine Schwelle fallen (FFN 235 $, E8 150k etwa 200 $), und droht irgendwo das Zurückstufen?

Er beantwortet **nicht**: ob eine Strategie gut ist, ob ein Bein ins Buch kommt, wie ein Konto insgesamt dasteht (das bleibt `konto-analyst`).

## 2. Die wichtigste Regel: die Prognose darf nur bremsen

| Richtung | Was entscheidet | Rolle der Prognose |
|---|---|---|
| **Hochstufen** (k1 auf k2) | die gemessene 60-Tage-Zahl, wie am 12.10. beschlossen | Veto: hochgestuft wird nur, wenn auch die **Obergrenze** der Prognose (der Wert, der nur in einem von zehn Fällen überschritten wird) unter der Rückstuf-Schwelle liegt |
| **Zurückstufen** (k2 auf k1) | Messung **oder** Prognose, was zuerst anschlägt | Frühwarnung: darf das Zurückstufen auslösen, bevor die träge Zahl es merkt |
| **Planung** (wann kommt k2, wann lohnt ein Kauf) | Prognose | hier ist sie die Hauptzahl, weil nichts kaputtgehen kann |

Grund: eine falsche Prognose nach unten würde uns zu früh groß machen, das kostet den Track Record. Eine falsche Prognose nach oben kostet nur ein paar Wochen Tempo. Die beiden Fehler sind nicht gleich teuer, deshalb zählt beim Hochstufen nicht der erwartete Wert, sondern die Obergrenze.

**Fällt die Prognose aus (alte Daten, Modell durchgefallen), ist Hochstufen gesperrt.** Ein stummes Modell darf das Veto nicht heimlich entfernen.

## 3. Wie gerechnet wird (drei Schichten, einfach zuerst)

Gleiches Prinzip wie bei den Konto-Karten: **ein festes Skript rechnet, der Agent liest nur.**

Es gibt zwei verschiedene Zielgrößen, die man nicht vermischen darf:
- **Die kommenden Tage** (wie wild wird es wirklich): daran hängt das Bust-Risiko, also Veto und Frühwarnung.
- **Der künftige Stand der 60-Tage-Zahl:** reine Planungsgröße („wann kann die Schwelle fallen“).

**Schicht A: Was schon feststeht (reine Arithmetik).**
Die 60-Tage-Zahl ist ein rollendes Fenster. Wir wissen heute schon, welche wilden Tage hinten rausfallen, wenn neue dazukommen. Gerechnet wird in Buch-Tagen, nicht in Kalendertagen: das Buch handelt nicht jeden Tag (heute rund 60 von 80 Markttagen), der Kalendertermin hat also eine eigene Unsicherheit. Nach 4 Wochen sind noch rund drei Viertel des Fensters bekannte Tage.

**Schicht B: Wie wild wird der Markt?**
Ein schlichtes Modell für die Tagesschwankung von NQ und RTY aus drei Zutaten: gestern, Schnitt der letzten Woche, Schnitt des letzten Monats (in der Literatur „HAR“, drei Stellschrauben, normale Regression). Vola hat ein Gedächtnis: wilde Tage kommen in Haufen und beruhigen sich langsam Richtung Normalniveau. Kein GARCH, kein Machine Learning, solange das schlichte Modell nicht nachweislich verliert ([[Simplex beats Komplex]]).

**Schicht C: Vom Markt zum eigenen Buch.**
Die Beine handeln NQ und RTY intraday, ihr Tagesergebnis schwankt mit dem Markt mit, aber nicht eins zu eins: feste Stops kappen den Zusammenhang, und wie oft gehandelt wird, kann selbst an der Vola hängen. Deshalb je Belegung eine Gerade (Grundschwankung plus Anteil vom Markt) und die Handelshäufigkeit als eigene Zahl. Schritt 0 prüft, ob das trägt und ob RTY neben NQ überhaupt etwas beiträgt.

Technischer Hinweis für den Bau: B und C rechnen in Varianz (quadrierte Schwankung), nicht in Standardabweichung. Das Fenster mittelt Quadrate, sonst kommt systematisch eine zu kleine Zahl heraus.

**Ergebnis je Konto:** erwartete Tagesschwankung der nächsten 4 und 8 Wochen mit Spannweite, dazu aus Schicht A der früheste Zeitpunkt, an dem die 60-Tage-Zahl die Schwelle erreichen kann. Eine 12-Wochen-Prognose gibt es nicht, dort bleibt nur Schicht A.

## 4. Woran wir merken, ob die Prognose etwas taugt

> [!warning] Ehrlich vorweg (Statistiker, 13.10.)
> Die Beweislage ist dünn und wird es bleiben. In knapp 11 Jahren Daten stecken nur etwa 35 unabhängige 16-Wochen-Fenster und 6 bis 8 echte Vola-Phasen. Dass die 235 $ unterschritten wurden, kam vermutlich nur eine Handvoll Mal vor. Ob das Veto „richtig“ bremst, lässt sich damit wahrscheinlich nicht beweisen. Das ist ein weiterer Grund, warum die Prognose nur bremsen darf.

**Der richtige Gegner** ist nicht „bleibt wie es ist“ (den schlägt schon das Herausrollen alter Tage rein mechanisch), sondern:

| Gegner | Aussage |
|---|---|
| Schicht A plus kurze Messung | für die neuen Tage gilt einfach die Schwankung der letzten 20 Buch-Tage |
| Schicht A plus Normalniveau | für die neuen Tage gilt der langjährige Schnitt |

Schlägt das Modell (B und C) diese beiden nicht, entfallen B und C ersatzlos. Dann ist die Frühwarnung schlicht das kurze 20-Tage-Fenster, und der „Agent“ ist ein Block in der Konto-Karte.

**Abnahme, vorab festgelegt:**
- Rückrechnung ab 2016, immer nur mit Daten, die es zu dem Zeitpunkt schon gab.
- Festes Fehlermaß und fester Test (QLIKE auf die Varianz, Vergleichstest mit Block-Bootstrap, Blöcke mindestens 16 Wochen), Mindestvorteil 10 % gegenüber dem besseren Gegner. Sonst zählt man überlappende Wochenprognosen als 550 Beobachtungen, obwohl es 35 sind.
- Die Obergrenze hält: in höchstens rund einem von zehn Fällen lag die echte Schwankung darüber. Nur diese Grenze bremst, also wird nur sie geprüft. Toleranz vorab nennen, bei 35 Beobachtungen sind rund 7 Prozentpunkte Unschärfe normal.
- Veto-Test: erst zählen, wie viele Hochstuf-Momente es seit 2016 gegeben hätte. Sind es einstellig viele, heißt das Ergebnis „unentscheidbar“ und nicht „bestanden“.

**Dauerkontrolle danach:** laufende Fehlerbilanz über 52 Wochen gegen eine Schwelle aus der Rückrechnung. (8 Wochen wären nur zwei unabhängige Prognosen, also Münzwurf.) Fällt das Modell durch: Prognose weg, Hochstufen gesperrt, bis Max entscheidet.

## 5. Der Agent: Ablauf

Name: `vola-analyst`, Modell sonnet, nur Lesen plus das eine feste Skript.

1. **Karte holen.** Skript aufrufen, es rechnet nur bei neuem Fingerabdruck (neue Daten, andere Belegung, neuer Modellstand). Sonst kommt die gespeicherte Vola-Karte sofort.
2. **Frische prüfen.** Sind die Marktdaten älter als 5 Handelstage, ist das die erste Zeile der Antwort, es gibt keine Prognose und Hochstufen ist gesperrt.
3. **Fehlerbilanz lesen.** Modell durchgefallen? Dann nur Messung und Schicht A, Hochstufen gesperrt.
4. **Feste Aussage liefern** (Abschnitt 6).
5. **Abgeben**, wenn es knapp wird: Grenzfall geht ans Quant-Team. Soll eine Größe wirklich geändert werden, kommt `konto-analyst` (Pflicht per Hook seit 13.10.) und vor dem Hochstufen der `strategy-auditor`.

**Was er nie tut:** selbst rechnen, eine Größe ändern, den RiskGuard anfassen, eine Prognose ohne Spannweite nennen, eine Zahl als Prognose ausgeben, die die Abnahme nicht bestanden hat.

## 6. Die feste Aussage (immer dieses Format)

Je 150k-Konto genau ein Satz aus sechs festen Zuständen, dazu drei Zahlen:

| Zustand | Wortlaut | Folge |
|---|---|---|
| 🔴 hoch, bleibt | „Schwankung hoch, die Schwelle ist in den nächsten 8 Wochen rechnerisch nicht erreichbar.“ | k1, nichts zu tun |
| 🟡 fällt | „Schwankung fällt, Schwelle frühestens in N Buch-Tagen (etwa Kalenderwoche X bis Y).“ | k1, Termin vormerken |
| 🟠 Grenzfall | „Messung liegt innerhalb ihrer eigenen Unschärfe um die Schwelle.“ | Quant-Team, nicht selbst entscheiden |
| 🟢 bestätigt | „Messung samt Unschärfe unter der Schwelle, Obergrenze der Prognose unter der Rückstuf-Schwelle.“ | Hochstufen ist Wochenend-Thema für Max |
| ⚠️ steigt | „Konto ist auf k2 und die Prognose kreuzt die Rückstuf-Schwelle.“ | Zurückstufen prüfen, sofort melden |
| ⚫ blind | „Daten zu alt oder Modell durchgefallen.“ | Hochstufen gesperrt |

Dazu immer: gemessene 60-Tage-Zahl mit Unschärfe, erwartete Schwankung der nächsten 4 und 8 Wochen mit Obergrenze, Fehlerbilanz in einem Halbsatz.

**Der Grenzfall ist breit, und das ist richtig so.** Eine Schwankung aus 60 Tagen ist selbst nur auf grob 15 bis 20 % genau gemessen (wilde Tage kommen gehäuft, Faustformel des Statistikers). Bei 235 $ sind das 35 bis 45 $: alles zwischen etwa 190 $ und 290 $ ist Grenzfall. 🟢 gibt es erst, wenn die Messung samt Unschärfe unter der Schwelle liegt, also grob ab 190 $. Das gilt unabhängig von jeder Prognose und betrifft schon die heutige Regel (siehe Entscheidung 6).

50k-Konten bekommen keine Ampel (bleiben laut Entwurf fest auf k1), nur die Zahl zur Info.

Beispiel, wie es klingen würde (Zahlen erfunden):
> FFN1: 🟡 Schwankung fällt. Gemessen 449 $ (plus/minus 75 $). Nächste 4 Wochen erwartet 340 $, Obergrenze 430 $. Schwelle frühestens in 45 Buch-Tagen, etwa Mitte bis Ende Januar. Bleibt k1.

## 7. Wann er läuft

| Auslöser | Was passiert |
|---|---|
| Neue Marktdaten (täglich, siehe Entscheidung 2) | Skript rechnet die Vola-Karte neu, kein Agent nötig |
| Wochenend-Prüfung (`/wochenende`) | Agent liefert die feste Aussage je Konto |
| Jede Größen-Frage („darf X auf k2?“) | läuft zusammen mit `konto-analyst` |
| Zustand wechselt (zum Beispiel 🟡 auf 🟢, oder ⚠️) | Meldung über den Auto-Check, bei ⚠️ per Telegram |
| Neues Konto (`/neues-konto`) | Schwelle und Zusammenhang für die neue Belegung anlegen |
| Frage von Max („wie ist die Vola?“) | Karte lesen |

Durchsetzung später als Hook, nicht als Text: Größe hoch auf einem Konto nur mit frischer Vola-Karte im Zustand 🟢 (passt an die bestehende Konto-Sperre).

## 8. Bauplan

| Schritt | Was | Wer |
|---|---|---|
| 0 | **Machbarkeit zuerst (ein Nachmittag):** (a) erklärt die Marktschwankung die Buch-Schwankung gut genug (Schicht C)? (b) wie viele Hochstuf-Momente und Vola-Phasen gibt es seit 2016 wirklich, ist die Abnahme überhaupt entscheidbar? Wenn nein: nur Schicht A plus 20-Tage-Fenster bauen, Rest entfällt. | Quant-Team |
| 1 | Schicht A und das 20-Tage-Fenster als Block in die Konto-Karten (trägt in jedem Fall) | Claude |
| 2 | Nur wenn Schritt 0 grün: Schicht B und C, Rückrechnung ab 2016 | Claude |
| 3 | Abnahme nach Abschnitt 4, Urteil mit Stempel | Quant-Team, `verdict-auditor` |
| 4 | Agent anlegen, Trigger, Hub-Eintrag, `/wochenende` erweitern | Claude |
| 5 | 8 Wochen Technik-Probelauf: kommen die Daten täglich, stimmt live mit der Rückrechnung überein? Das belegt nur die Technik, nicht die Güte. Die Güte kommt aus Schritt 3. | läuft von selbst |
| 6 | Erst danach: Veto und Frühwarnung scharf, Hook | Max entscheidet |

Vorbedingung: Daten bis Oktober (AP356).

## 9. Was Max entscheiden muss

| Nr. | Frage | Meine Empfehlung |
|---|---|---|
| 1 | Darf die Prognose nur bremsen (Abschnitt 2)? | Ja. Das ist der Kern, ohne das würde ich es nicht bauen. |
| 2 | Woher kommen tägliche Marktdaten? Heute enden die Daten am 11.09., ohne tägliche Daten ist jede Prognose alt. Wege: täglicher NT8-Export auf der Box, oder kostenlose Tagesdaten. | Täglicher Export auf der Box, weil dann auch die Buch-Zahl frisch ist. |
| 3 | Eigener Agent oder nur ein Block in den Konto-Karten, den `konto-analyst` mitliest? | Erst der Block (Schritt 1). Eigener Agent nur, wenn Schritt 0 und 3 zeigen, dass das Modell mehr kann als das 20-Tage-Fenster. |
| 4 | Darf die Frühwarnung das Zurückstufen **automatisch** auslösen oder nur melden? | Nur melden, bis es überhaupt ein Konto auf k2 gibt. |
| 5 | Später auch für andere Entscheidungen nutzen (Tagesstopp, Kaufzeitpunkt E8 150k, Vola-Pfad in der Zeit-bis-50k-Rechnung)? | Erst nach der Abnahme. |
| 6 | **Neu, betrifft die Regel vom 12.10. direkt:** die 235 $ sind als harte Linie beschlossen, die Messung ist aber nur auf 35 bis 45 $ genau. Soll Hochstufen erst gelten, wenn die Messung **samt Unschärfe** unter 235 $ liegt (praktisch ab etwa 190 $)? Und reicht der Rückstuf-Abstand von 1,25 (das ist nur gut eine Unschärfe, das Konto würde hin und her springen)? | Ja zur Unschärfe. Rückstuf-Abstand vom Quant-Team nachrechnen lassen, bevor das erste Konto auf k2 geht. |

## 10. Was dagegen spricht (ehrlich)

- **Der Gewinn ist begrenzt.** Die Entscheidung hängt an einer 60-Tage-Zahl, die sich von selbst nur langsam bewegt. Der größte Teil des Nutzens steckt wahrscheinlich in Schicht A und dem 20-Tage-Fenster, und die kosten einen Bruchteil.
- **Beweisen lässt sich wenig.** 35 unabhängige Fenster, eine Handvoll Hochstuf-Momente. Gut möglich, dass die Abnahme „unentscheidbar“ ergibt.
- **Vola ist auf Wochen gut vorhersagbar, auf Monate kaum.**
- **Sprünge sieht keiner kommen.** Ein Schock steht in keiner Prognose. Der Agent ersetzt weder den Tagesstopp noch die Regel „Zurückstufen sofort“.
- **Heute ändert es nichts.** Alle Konten bleiben k1. Auszahlen kann sich das erst, wenn die Schwankung in die Nähe der Schwelle kommt.
- **Noch ein Baustein mehr.** Jeder Agent kostet Pflege. Deshalb Empfehlung 3: erst Block, dann vielleicht Agent.

## 11. Was das Quant-Team am ersten Entwurf geändert hat (13.10.2026)

Nur Methode gegengelesen, nichts gerechnet, alle Zahlen sind Faustformeln.

**Mathematiker:** Zielgröße trennen (kommende Tage für Veto und Warnung, Fensterstand nur für Planung). Schicht A in Buch-Tagen. In Varianz rechnen. Markt zu Buch als Gerade mit Grundanteil plus Handelshäufigkeit statt „ein Faktor“. Veto als Obergrenzen-Regel statt „zeigt nach oben“. Dritter Gegner: Schicht A plus 20-Tage-Fenster. 12-Wochen-Spalte gestrichen.

**Statistiker:** Abnahme war so nicht entscheidbar (rund 35 unabhängige Fenster). Gegner, Fehlermaß, Test und Mindestvorteil vorab festschreiben. Veto-Test erst zählen, dann urteilen. Dauerkontrolle über 52 statt 8 Wochen. Stumm heißt gesperrt, nicht frei. Grenzfall beziffert (190 bis 290 $ bei Schwelle 235 $). Rückstuf-Abstand 1,25 ist nur gut eine Unschärfe. Der 8-Wochen-Probelauf belegt nur die Technik.
