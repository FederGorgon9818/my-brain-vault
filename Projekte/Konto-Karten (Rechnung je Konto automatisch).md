---
tags:
  - projekt/trading
  - projekt/infra
  - sizing
erstellt: 2026-10-12
status: Konzept, Entscheidung Max offen
---
# Konto-Karten: jedes Konto wird nach demselben Prinzip automatisch gerechnet

⬅️ [[Firm-Regeln je Konto]] · [[Hochstuf-Regel je Konto (Entwurf)]] · [[Buch-Workflow]] · [[Großes Ziel]]

> [!summary] In drei Sätzen
> Heute rechnen wir jede Frage zu einem Konto von Hand neu, weil jedes Konto andere Firmenregeln, eine andere Größe und ein anderes Buch hat. Die Lösung ist kein Agent, der jedes Mal neu rechnet, sondern ein Konto-Register plus ein festes Rechenskript, das je Konto immer dieselbe Karte ausgibt und nur neu rechnet, wenn sich etwas geändert hat. Ein kleiner Agent liest danach nur noch die Karten und fasst zusammen.

## 1. Was heute schiefläuft (Anlass 12.10.2026)

| Problem | Beispiel von heute |
|---|---|
| Jede Frage wird neu aufgebaut | zwei Quant-Läufe, zusammen rund 840.000 Tokens und 80 Minuten |
| Die Belegung je Konto steht nirgends maschinenlesbar | ich habe FFN falsch angenommen (FFN2 „ohne Asia“), richtig war „ohne PB3“ |
| `book_state.json` kennt nur ein Buch | E8 50k und FN passen, FFN1 (5 Beine) und FFN2 (3 Beine) nicht |
| Die Rechenwerkzeuge kennen FFN nicht | Sonderweg über `ffnlib.py` im Wegwerf-Ordner (AP334) |
| Regeln gelten pauschal | Hochstuf-Schwelle für alle Konten gleich, obwohl Puffer und Buch verschieden sind |
| Zahlen von gestern und heute sind nicht vergleichbar | jede Rechnung mit eigenem Flottenmodell, eigenem Nachkauf, eigenem Deckel |

## 2. Das Prinzip: fünf Bausteine

**Baustein 1: Konto-Register (eine Datei, eine Wahrheit je Konto).**
Je Konto ein Eintrag: Firma, Kontotyp, Phase (Eval oder Funded), Kontostand und Hoch, Größe k, RiskGuard-Werte, Kaufpreis, und vor allem die **Belegung** (welche Beine). Die Belegung wird nicht getippt, sondern von der Box gelesen: aus den laufenden Host-Dateien und der RiskGuard-Konfiguration, mit Prüfsumme. Weicht die Box vom Register ab, gibt es einen Alarm statt einer stillen Abweichung.

**Baustein 2: Regeln je Firma als ein gemeinsamer Baukasten.**
E8, FundedNext und FFN bekommen dieselbe Schnittstelle: Gewinnziel, Drawdown-Art, Einrasten, Payout-Regeln, Deckel, Split, Gebühren. Eine neue Firma heißt dann: einen Regelsatz ergänzen, nicht ein neues Rechenskript schreiben.

**Baustein 3: Tagesergebnisse je Bein, einmal gerechnet.**
Für jedes Bein liegt die Tagesreihe je Micro im Zwischenspeicher, mit Stempel (Datenstand, Engine-Stand, Parameter). Das Buch eines Kontos ist dann nur noch „diese Beine mal k“. Kein neuer Backtest je Frage.

**Baustein 4: Die Konto-Karte (immer dieselben Zahlen).**
Ein Skript rechnet je Konto dieselbe feste Liste:

| Block | Zahlen |
|---|---|
| Schwankung | Tagesschwankung der eigenen Belegung über 20, 60, 120 Tage und alle Jahre |
| Abstand | Puffer geteilt durch Tagesschwankung, heute und bei k2 |
| Überleben | Chance auf 12 Monate ohne Bust, ab jetzt und ab Funded |
| Auszahlung | Zeit bis zum ersten Payout, Payout-Monate in 12 und 36 Monaten |
| Geld | Netto nach Split und Käufen über 12 und 36 Monate, mit Spannweite |
| Hebel | Was bringt k2, was bringt ein zusätzliches Bein, jeweils gegen heute |
| Kontrolle | Nulldrift-Zwilling, geschrumpfte Spalte, letzte drei Jahre |
| Regel-Ampel | Hochstufen erlaubt ja oder nein (235-$-Regel), Inaktivität, offene Firmen-Auflagen |

Dazu eine **Flotten-Karte**: alle Konten auf gemeinsamem Kalender, mit Auslage-Deckel.

Die Karte trägt einen Fingerabdruck aus Belegung, Größe, Datenstand, Engine-Stand und Regelversion. **Gerechnet wird nur, wenn sich der Fingerabdruck ändert.** Sonst kommt die gespeicherte Karte in Sekunden.

**Baustein 5: Ein kleiner Agent, der nur liest.**
Der Agent rechnet nicht. Er liest die Karten, fasst je Konto in drei Sätzen zusammen, benennt, was sich seit der letzten Karte geändert hat, und sagt, welche Entscheidung ansteht. Das Quant-Team kommt nur noch dazu, wenn eine Karte einen Grenzfall zeigt oder die Methode selbst geändert wird.

## 3. Wann die Karten neu gerechnet werden

| Auslöser | Was passiert |
|---|---|
| Belegung oder Größe eines Kontos ändert sich auf der Box | Karte dieses Kontos und Flotten-Karte neu |
| Neues Konto oder Phasenwechsel (Eval zu Funded) | neuer Register-Eintrag, Karte neu, Ablauf `/neues-konto` hängt daran |
| Neue Daten (Export) oder neuer Engine-Stand | alle Karten neu |
| Wochenend-Prüfung | Karten werden angezeigt, nicht neu erfunden |
| Frage von Max im Chat | Karte lesen statt rechnen |

## 4. Was das bringt

- **Kosten:** eine Frage wie heute kostet Sekunden und ein paar tausend Tokens statt 400.000 je Lauf.
- **Vergleichbarkeit:** jede Zahl kommt aus demselben Modell, gestern und heute passen zusammen.
- **Weniger Fehler:** die Belegung kommt von der Box, niemand muss sie im Kopf haben.
- **Track Record:** jede Karte ist ein datierter Beleg, was wir zu welchem Zeitpunkt über das Konto wussten.

## 5. Bauplan in sechs Schritten

| Schritt | Inhalt | Gegenleser | Aufwand |
|---|---|---|---|
| 0 | Entscheidungen Max (Abschnitt 6) | | kurz |
| 1 | Konto-Register anlegen, von der Box befüllen, Abweichungs-Alarm in den Auto-Check | pipeline-auditor | klein |
| 2 | Firmen-Baukasten: E8 und FN aus dem bestehenden Werkzeug, FFN aus `ffnlib.py` übernehmen (löst AP334) | pipeline-auditor | mittel |
| 3 | Bein-Zwischenspeicher und Konto-Karte als Skript, Vorlage ist der Wegwerf-Ordner von heute | Quant-Team einmal | mittel |
| 4 | **Abnahme:** das Skript muss die Zahlen von heute nachstellen (Flotte, FFN1, FFN2), Nulldrift muss Null zeigen | verdict-auditor | klein |
| 5 | Anzeige: Reiter „Konten“ im Lab, Karten in die Wochenend-Prüfung, Agent anlegen und im Hub eintragen | design-guard | mittel |
| 6 | Regeln als Code: Hochstuf-Regel (235 $), „erst Beine, dann Größe“, Ampel je Konto | Quant-Team einmal | klein |

Schritte 1 bis 4 ändern nichts am Live-Betrieb, sie lesen nur. Geschätzt zwei bis drei Sessions.

## 6. Was Max entscheiden muss

| Nr. | Frage | Empfehlung |
|---|---|---|
| 1 | Bauen wir das? | Ja, es zahlt sich nach zwei bis drei Konto-Fragen aus |
| 2 | Woher kommt die Belegung: von der Box gelesen oder im Register gepflegt? | Von der Box gelesen, Register ist nur der Spiegel |
| 3 | Wird `book_state.json` zum Buch je Konto umgebaut oder bleibt es das „Hauptbuch“ und das Register steht daneben? | Daneben. `book_state.json` hängt an zu vielen Stellen, der Umbau wäre ein eigenes Projekt |
| 4 | Soll der Agent von selbst melden (zum Beispiel Telegram bei Ampelwechsel) oder nur auf Zuruf und am Wochenende? | Erst nur auf Zuruf und am Wochenende |
| 5 | Reihenfolge: erst das (dann rechnet sich AP355 und die Hochstuf-Regel von selbst) oder erst neue Beine suchen? | Schritte 1 bis 4 zuerst, sie sind klein und sparen sofort |

## 7. Was dagegen spricht

- Ein Rechenmodell für alles heißt auch: ein Fehler darin steckt in jeder Karte. Deshalb die Abnahme in Schritt 4 und der Nulldrift-Zwilling als Pflicht.
- Die Karte zeigt Simulationen, keine Wahrheit. Der Abgleich mit den echten Fills (live-reconciler) bleibt nötig und sollte später als eigene Zeile in die Karte.
- Mehr Werkzeug ist nicht mehr Sharpe. Der Bau darf die Suche nach neuen Beinen nicht verdrängen, deshalb der kleine Zuschnitt.
