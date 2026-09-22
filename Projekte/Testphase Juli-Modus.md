---
tags:
  - projekt/trading
  - trading/alpha
  - trading/prozess
erstellt: 2026-09-22
status: geplant (Start offen, Max liefert 3 Ideen)
dauer: eine Woche ab Start
---
# 🧪 Testphase Juli-Modus

⬅️ [[Alpha-Suche]] · [[Discovery-Prozess (wie wir Alpha finden)]] · [[Friedhof-Analyse (17.09.2026)]] · [[Strategie-Logbuch]]

> [!important] Trigger-Wort (Regel Max, 22.09.2026)
> Sagt Max **„Juli-Modus"**, **„Testphase Juli-Modus"** oder bezieht sich auf **„unseren Vorschlag / das Gespräch vom 22.09., warum wir früher mehr gefunden haben"**, ist genau diese Notiz gemeint. Sofort hier weitermachen, keine Rückfrage, was gemeint ist. Teil A = Suche im Juli-Modus, Teil B = Gate-Kalibrierung (Prompt unten).

---

## 1. Befund: warum wir im Juli mehr gefunden haben als heute

Ausgangsfrage von Max (22.09.2026): „Woran liegt es, dass wir am Anfang so viel mehr gefunden haben als jetzt? Ehrliche Einschätzung, nicht ‚der Markt ist schwieriger geworden'."

**Kurzantwort:** Der Markt ist nicht die Ursache. Es sind drei hausgemachte Dinge.

### Erst die Erinnerung geradeziehen

Das 9-Bein-Buch vom 30.07. war zur Hälfte ein Messfehler. Es leben heute 3 der 9 Beine: `NQ_Momentum`, `NQ_LastHour_v3` (PowerHour), `NQ_Asia-Dir`. **Mechanismus und Bein-Version trennen:** die drei Mechanismen stammen aus den ersten drei Wochen (Archiv #008 SSRN-Gegentest gespiegelt, #009 refine-Explorer, #028 `asian.py`-Lauf am 21.07. im Hauptlogbuch), je mit Paper oder Marktstruktur-Story dahinter und nach der damaligen Regel „9 bis 24 Configs je Mechanismus, bewusst flach" ([[Discovery-Prozess (wie wir Alpha finden)]]; #028 selbst hatte 46). Die heutigen **Versionen** kamen im August: Momentum-Exit und Asia-Dir-Exit aus den ersten drei Runner-Tagen (18./20.08., Quant-Verdikt #126), LastHour_v3 aus dem Developer (17.08., #111).

| Bein von damals | Warum weg |
|---|---|
| ORB-Breakout, ORB-Scalp 8 und 9 | Look-ahead im Vol-/VWAP-Filter (#066/#067), ehrlich gerechnet expR nahe null |
| Lead-Lag ES | tot (#090) |
| ORB-Fade + NR7 | Filter mit falsifizierter Wirkrichtung, Regime-Wette 2024-26 (#116) |
| RTY Gap-fade | raus 24.08. (#130), sechs Tage später vom Datenfix (#135) als „unterschätzt" gemessen, nie neu entschieden |

Echte Trefferquote Juli: 3 tragende Mechanismen aus ~25 Logbuch-Einträgen. Discovery-Runner v2 seit 18.08.: die einzigen Funde, die es ins Live-Buch schafften, waren **Exit-Varianten bestehender Beine in den ersten drei Tagen** (also genau der Ersatz-Pfad). Seit dem 21.08.: rund 65.000 Trials (Stand 22.09.), **0 neue Mechanismen** im Live-Buch. VWAP-Pullback (Developer, 16.08.) kam rein und am 18.09. wieder raus (#161).

### Die drei Ursachen

**1. Die großen, einfachen Effekte waren zuerst dran, und jedes Bein im Buch hebt die Latte für das nächste.** Intraday-Momentum, Power-Hour, Asia-Richtung sind die bestdokumentierten NQ-Anomalien. Alles danach ist dünner. Mathematik (Friedhof-Analyse, Abschnitt 3): ein zusätzliches NQ-Intraday-Bein muss bei ρ ≈ 0,2 allein ~1.811 $/Jahr je Kontrakt verdienen, mehr als das beste Bestandsbein. Der einzige rechnerisch offene Pfad ist **Ersatz**, und 87 % aller Trials liefen als „neues Bein" (Pfad-Blindheit, P1). Die Slot-Tabelle #146, die den Pfad öffnet, gilt laut #158-Nachtrag als AP183-Entscheidung 2 freigegeben, ist aber **nicht umgesetzt** (Ticket AP183 offen, Generator setzt weiter kein `replaces_leg` für tsmom/maband).

**2. Das Messgerät wurde nach jedem Vorfall härter gestellt, aber nie kalibriert.** Juli: kein Intraday-Bust, kein Bootstrap, keine Zufallsdecke, Look-ahead-Modus Standard → zu weich, viele Funde, viele spätere Leichen. Heute: Šidák-Schwelle 4,9 bis 7,1 pp (Friedhof-Analyse) bzw. 5,4 bis 7,4 pp (#156, k_eff 2 bis 8) bei echter Streuung ~3 pp, Power für einen realen 3-pp-Effekt 0,24 (P4). Zwei der damals vier Bestandsbeine kämen als Neuzugang nur auf +1,9/+2,0 pp, gemessen am 4-Bein-Buch mit VWAP-Pullback (Friedhof Abschnitt 1; Bein-Zuordnung dort nicht genannt, Basis heute 3 Beine). **Die heutige Pipeline hätte das heutige Buch vermutlich nicht gefunden. Ob das stimmt, ist genau die Frage von Teil B.**

**3. Die Suche kippte von Breite auf Tiefe, gegen die eigene Regel vom 30.07.** ([[Discovery-Prozess (wie wir Alpha finden)]]: „Tiefe kam aus Breite, mehr Param-Grids auf bestehenden Mechanismen helfen nicht.")

| Stand 22.09.2026 | Juli (Backfill) | August | September |
|---|---|---|---|
| Register-Trials | 596 | 15.572 | 48.985 |
| Anteil tsmom/maband | 0 | ~72 % | ~93 % |
| Neue Mechanismen im Live-Buch | 3 | 0 (nur Exit-Versionen 18./20.08.) | 0 |

Dazu 670 ungebaute Bank-Zeilen (Volumen-Bank 479/0 gebaut), Generator klont Varianten statt Bank-Zeilen zu ziehen (P6). Bei GC/CL wurde Schritt 1 des Juli-Prozesses (Research-Prior je Instrument) übersprungen: 90 NQ-Ideen um 09:30 ET geklont, obwohl COMEX 08:20 / LBMA 10:00 der Takt ist und MGC die 3,3-fache Kostenquote hat (#165).

**Nicht die Ursache:** die Prämissen-Stufe (427 Tode, erwarteter Kandidaten-Verlust ≈ 0).

### Was Claude falsch gemacht hat
- Suchmaschine entlang vorhandener Module (tsmom/maband) gebaut, nicht entlang der Mechanismen mit dem stärksten Why.
- Gates verschärft ohne Power-Rechnung.
- „Getötet" als Dauersperre ohne Stempel stehen lassen (alle ES-/RTY-Urteile vor 30.08. auf kaputten Daten).
- Auf „mach 200 Hypothesen" Bänke geliefert statt zu widersprechen.
- Schleife Idee → Urteil von einer Stunde auf Tage wachsen lassen (388 ungelesene Ergebnisse, P7).

### Was Max anders prompten kann
1. **Eine Idee, ein Why, ein Markt** statt „baue 100 Hypothesen". Die drei Mechanismen kamen aus je einem Paper oder einer Struktur-Story mit kleinem Grid, die Bänke mit 670 Zeilen lieferten 0 Beine.
2. **Prämissen-Tafel vor jedem Grid verlangen.** Kein Job in die Queue, dessen Prämisse Max nicht als Tabelle gesehen hat.
3. **Neue Märkte: zuerst Struktur** (Sessions, wer handelt wann, Events, Kostenquote), dann erst Ideen.
4. **Offene Entscheidungen abarbeiten**: AP183 (Slot-Tabelle umsetzen, Coast-Leg-Schalter +2,2 bis 3,6 pp MC, Live-Grade-Karte, Stufe-2-Design), AP211. Der Flaschenhals mit dem größten Hebel.
5. **Wochen-Urteil statt Ergebnisse**: „an welcher Stufe hing es diese Woche".
6. **Bei „tot" nach dem Stempel fragen** (Engine, Daten, Kriterium).

---

## 2. Teil A: eine Woche Suche im Juli-Modus

**Grundidee:** Schleife Idee → Zahl → Urteil zurück in eine Session. Keine Bank, keine Queue, keine Box. Max sieht jede Zwischenzahl, bevor die nächste Stufe läuft.

### Was Max liefert (Tag 1): drei Ideen, je vier Zeilen
- **Markt** (NQ, oder GC/CL mit eigenem Zeitfenster)
- **Beobachtung** („nach X passiert meistens Y")
- **Warum Geld** (wer ist gezwungen, in dieser Situation zu handeln)
- **Wann am Tag**, grob

Beispiel: „NQ. Wenn die erste Stunde eng ist und das Volumen unter Schnitt liegt, läuft der Nachmittag stärker in eine Richtung. Weil Institutionen ihre Tagesorders dann in die zweite Hälfte schieben. 13:00 bis 15:55 ET." Max muss nicht wissen, ob es stimmt.

**Bei GC/CL (oder jedem Nicht-Index-Markt) kommt ein Vorschritt davor, ohne Ausnahme** (#165 Lehre 1 und 6): eigenes Session-Fenster je Markt (GC: COMEX 08:20 / LBMA 10:00 ET; CL: 09:00, EIA Mi 10:30) statt 09:30 ET, und die Kostenquote je Käfig-Kontrakt (2 Ticks je Seite + Kommission gegen die Tagesrange; MGC 3,3×, MCL 6,1× MNQ). Erst dann Stufe 1.

### Was Claude je Idee macht, mit Stopp nach jeder Stufe

| Stufe | Inhalt | Stopp-Regel |
|---|---|---|
| 1 Register- und Modus-Check | Trials dazu? Engine-Stand? Urteil? „tot" ohne Stempel gilt als offen. **Ziel-Modus benennen** und prüfen, ob er einen Null-Schalter in `controls.py::ctl_null` hat (heute: tsmom, maband, ts_reversal, last_hour, asian, vwap_pullback) | Modus ohne Null-Schalter → entweder als tsmom/maband-Gate nachbauen oder Idee zurückgeben, **kein Grid** (sonst läuft die Kontroll-Batterie leer durch, Friedhof A3) |
| 2 Prämissen-Tafel | EINE Tabelle ohne Strategie: Gruppen der These × mittlere gerichtete Bewegung in Punkten mit 90 %-CI, Trefferquote, N Tage, getrennt 2016-19 / 2020-23 / 2024-26, Kosten in denselben Punkten, Gegengruppe daneben | **trägt** = obere 90 %-Grenze der gerichteten Bewegung liegt in keiner Epoche unter 0 (CI-Gate), N je Epoche mindestens 60 Tage, Bewegung im Mittel über den Kosten, Gegengruppe zeigt es nicht. Vorzeichen-Konsistenz ist Zusatzinfo, kein Killer (Dreifach-Konjunktion auf Punktschätzern tötet echte 3-pp-Effekte, P4 andersherum). Sonst Ende nach ~20 Min |
| 3 Kleines Grid | max. 24 Configs (z.B. 2 Schwellen × 2 Stops × 2 Exits × 3 Fenster), Grid vorher zeigen. **Alle Configs ins Register über `registry_pending_add` (discovery_lib.py), nie `registry.json` direkt.** Kontroll-Batterie (`controls.py`: Nulldrift, Delay, Spiegel, zweiter Markt) auf ALLE Survivors | kein Survivor → Ende mit Stempel |
| 3b Zufallsdecke | vor jeder Marginal-Zahl: `e_max_sr` gegen `max(n_eff_mech, 10)·F` UND gegen n_global ausweisen (der Ersatz-Pfad prüft `above_ceiling` sonst nicht, `discovery_runner.py:575`) | bester Survivor unter beiden Decken → Ende mit Stempel „unter Zufallsdecke" |
| 4 Ersatz-Marginal (Auftragstyp `rechnen`, Quant-Team) | je Survivor vier Zahlen: als Ersatz für Momentum / LastHour / Asia-Dir (`book_marginal_confirm(tr, replaces_leg=...)`, baut die Basis „Buch ohne X" selbst) und als viertes Bein. Jede Zahl **full-sample UND OOS-only** getrennt (CLAUDE.md: „Buch + 1, nur OOS"), 5 Seeds, Fehlerbalken, gepaart gegen den Nulldrift-Zwilling (`params["tm_null"]=seed` → `qbt.run_strategy` → dieselbe Marginal-Rechnung). Rechenweg wie das Gate: `eval_plan.evaluate_v2` über `_one_tier_plan` | „besser" nur, wenn full-sample und OOS-only beide über dem in Teil B kalibrierten Gate liegen |
| 5 Urteil mit Stempel (Auftragstyp `urteil`, verdict-auditor) | Logbuch-Zeile (über logbook-distiller): Idee, Stufe an der es hing, Engine-Fingerprint, Datenstand, Kriterium, Kategorie nach CLAUDE.md „Tot ist ein Urteil mit Reichweite", Buch-Lücke. Fund → Next-Week-Buch + Ticket, nie direkt live | |

### Was bewusst wegbleibt
Kein Eintrag in `hypothesis_bank.py`, kein Runner-Job, keine Varianten-Vorlage. Auftragstypen je Stufe: `hypothese` für Stufe 1 bis 3 (löst einmal `ein-weg` aus: variant-scout zählt Testarten, strategy-auditor liest die drei Whys in EINEM Call), `rechnen` für Stufe 4, `urteil` für Stufe 5. Das sind Aufrufe, kein Prozess.

### Zeit und Modell
Je Idee 1 bis 2 h bis Stufe 2 (sonnet), weitere Session bis Stufe 4 wenn sie trägt (opus, Quant-Team). Drei Ideen = 3 bis 6 Sessions. Je Idee eine frische Session.

### Erfolgskriterium nach einer Woche
Nicht „ein neues Bein". Sondern: **mindestens eine Idee mit tragender Prämisse und einer sauberen Ersatz-Zahl mit Fehlerbalken.** Fallen alle drei Prämissen durch, liegt der Engpass bei der Ideenqualität, nicht bei der Pipeline, und wir wissen es nach einer Woche.

### Danach
Mit Zahlen entscheiden, ob und womit der Runner wieder anläuft. Naheliegender Job: die 670 ungebauten Bank-Zeilen als Prämissen-Tafeln abarbeiten, nicht weitere tsmom-Varianten.

---

## 3. Teil B: das Lineal kalibrieren (Gate-Kalibrierung)

**Warum zuerst:** Eine Session reicht, und Teil A rechnet sonst gegen ein möglicherweise blindes Gate. Friedhof-Analyse P4: Momentum und LastHour brächten als Neuzugang +1,9/+2,0 pp, die Schwelle liegt bei 4,9 bis 7,1 pp.

**Drei Schritte:** (1) die drei Bestandsbeine als Fremde durch Stufe 2 schicken, Basis jeweils das 2-Bein-Restbuch; (2) Ergebnis lesen: bestehen alle, ist das Gate ok; fällt eines durch, wird das Gate geändert, nicht das Buch; (3) Schwelle nach Power setzen: ein echter 3-pp-Effekt soll mit ≥ 50 % zählen (heute 24 %), Bauteile vom Statistiker (#156/#158): gepaart gegen Nulldrift-Zwilling, Pooling vor Selektion, zweistufig (Screening ~2,7 pp, Power 0,54 → Next-Week-Buch als zweite Stufe). Nulldrift-Kontrolle (#106) bleibt Pflicht.

### Prompt für eine neue Session (kopieren, `/clear` vorher, Modell opus)

```text
Auftrag: Gate-Kalibrierung, Teil B der Testphase Juli-Modus (Vault-Notiz "Projekte/Testphase Juli-Modus.md", Abschnitt 3, dort zuerst lesen). Auftragstyp: rechnen, danach urteil.

Frage: Würden unsere drei eigenen Buch-Beine das heutige Buch-Marginal-Gate bestehen, wenn sie heute als neue Discovery-Kandidaten kämen? Und wenn nicht: welche Schwelle und welches Design brauchen wir, damit ein echter 3-pp-Effekt mit mindestens 50 % Wahrscheinlichkeit als Kandidat zählt?

Kontext (nicht neu herleiten, steht alles im Vault):
- Buch heute: engine/book_state.json, drei Beine NQ_Momentum_d260818, NQ_LastHour_v3, NQ_Asia-Dir-USopen_d260820.
- Heutiges Gate: discovery/discovery_lib.py::book_marginal_confirm(tr, replaces_leg=..., k_eff=2, B=200, block=10) (Šidák-korrigiert seit Logbuch #156; effektive Schwelle 5,4 pp bei k_eff 2 bis 7,4 pp bei k_eff 8). Das Gate rechnet intern eval_plan.evaluate_v2 über _one_tier_plan (nur primary_tier, Seeds 11/23/37, B=200, Block 10). GENAU diesen Weg nehmen, nicht cage_policy_lib.evaluate_v2_seeds, sonst kommt eine andere Zahl als das Gate heraus.
- Friedhof-Analyse (Projekte/Friedhof-Analyse (17.09.2026).md), Abschnitt 1, 3 (quant-statistician) und 5 (P4): Power bei 3 pp = 0,24; zwei der damals vier Beine kämen am 4-Bein-Buch nur auf +1,9/+2,0 pp. Diese Zahlen sind nachzurechnen, nicht zu übernehmen. Quervergleich: #156 hat bereits „4 Beine als Stand-in-Kandidat gegen den Rest, B=200" gemessen; die Abweichung 4-Bein- vs. heutiges 3-Bein-Buch ist erwartbar, kein Fehler.
- Nulldrift-Zwilling: alle drei Buch-Modi (ts_reversal, last_hour, asian) haben seit AP157 einen Null-Schalter. Zwilling erzeugen über params["tm_null"]=<seed> → qbt.run_strategy → dieselbe book_marginal_confirm-Rechnung. controls.py::ctl_null ist nur die Referenz für die Logik, es gibt {ok, note} zurück, keinen Trade-Satz. Die #106-Kontrolle bleibt Pflicht: unter Edge 0 muss jede Politik 0 % zeigen.
- Vorher session-guard: developer_run.book_baseline_cells schreibt developer/book_cells.json (geteilte Datei, parallele developer_run-Sessions möglich).

Schritte:
1. Für jedes der drei Beine: Trades per qbt.run_strategy(leg["params"]) erzeugen, dann book_marginal_confirm(tr, replaces_leg="<Bein-Name>") aufrufen. Die Funktion baut die Basis „Buch ohne dieses Bein" (2 Beine) selbst aus book_baseline_cells minus X. k_eff festlegen und begründen: Hauptlauf k_eff=2 (ein Bestandsbein hat kein Grid, es gab nichts zu selektieren), Sensitivität k_eff=8 dazu, weil k_eff über bestanden/nicht bestanden entscheidet. Ausgabe je Bein: Delta in pp, Fehlerbalken (Seeds + Bootstrap), Schwelle je k_eff, bestanden ja/nein.
2. Zusätzlich je Bein das Delta gepaart gegen seinen Nulldrift-Zwilling (tm_null, gleiche Trades, gewürfelte Richtung, mindestens 3 Seeds) rechnen und die Streuung des gepaarten Maßes mit der ungepaarten vergleichen.
3. quant-statistician und quant-mathematician parallel: (a) Power-Kurve des heutigen Gates für wahre Effekte 1/2/3/5 pp, (b) Power-Kurve für das Design "gepaart gegen Zwilling + Pooling über die Varianten eines Mechanismus vor der Selektion + zweistufig (Screening, dann Next-Week-Buch als zweite Stufe)", (c) Falsch-Positiv-Rate beider Designs unter Edge 0 über eine Kampagne von ~500 Jobs. Der Mathematiker liefert dazu, ob das theta-Surrogat (2 mu / sigma^2, Friedhof Abschnitt 3) als glatter Vorfilter die MC-Läufe ersetzen kann.
4. verdict-auditor über das Ergebnis, bevor ein Stempel gesetzt wird.

Regeln:
- book_state.json und Engine-Dateien nicht ändern. Änderungsvorschlag am Gate als Ticket (tasks.json erst --pull) mit exakter Datei/Funktion/Zeile und den Zahlen, die ihn tragen. Entscheidung liegt bei Max.
- Alle Rechnungen im Scratchpad oder engine/_scratch_gate_kalibrierung/, Ergebnis-JSON dort ablegen, nie volle Logs einlesen.
- Ergebnis-Tabelle (3 Zeilen Beine + Power-Tabelle beider Designs) in Abschnitt 3 der Notiz "Testphase Juli-Modus" nachtragen, Logbuch-Eintrag über logbook-distiller, Daily Note.

Ausgabe an Max am Ende (Kurzfassung, keine Code-Bezeichnungen): (1) bestehen unsere Beine das eigene Gate, ja/nein je Bein mit Zahl, (2) welche Schwelle und welches Design vorgeschlagen wird und was es an Power und Falsch-Positiven kostet, (3) was sich damit an der Bewertung der offenen Kandidaten (Friedhof Abschnitt 4) ändern würde, (4) Modell-/Clear-Hinweis.
```

### Ergebnis Teil B
*(noch nicht gerechnet, wird von der Teil-B-Session nachgetragen)*

---

## 4. Stand und Ideen-Sammlung

| # | Idee (Markt, Beobachtung, Warum, Wann) | Stufe erreicht | Ergebnis | Datum |
|---|---|---|---|---|
| 1 | *(von Max)* | | | |
| 2 | *(von Max)* | | | |
| 3 | *(von Max)* | | | |

**Offene Entscheidungen bei Max, die in diese Woche gehören:** AP183 (Slot-Tabelle umsetzen, Coast-Leg-Schalter, Live-Grade-Karte, Stufe-2-Design), AP211 (Bitcoin-Daten, prescan_gross).

**Log:**
- 22.09.2026: Analyse und beide Teile festgeschrieben, Trigger-Regel in CLAUDE.md, Teil-B-Prompt fertig. verdict-auditor (Pflichtkette `meta`) hat 12 Punkte geliefert, alle eingearbeitet: Kernaussage „0 neue Beine seit Runner" korrigiert auf „0 neue Mechanismen, Exit-Versionen aus den ersten Runner-Tagen", Slot-Tabelle-Stand, Schwellen-Spannen, Register-Stichtag; Teil A um Null-Schalter-Check, Zufallsdecke, OOS-only, CI-Gate statt Vorzeichen-Konjunktion, GC/CL-Vorschritt und Auftragstypen je Stufe ergänzt; Teil-B-Prompt um k_eff, Trade-Erzeugung, Zwilling-Weg, kanonischen Rechenweg, session-guard und #156-Quervergleich ergänzt. Nicht nachgerechnet vom Auditor: Quant-Zahlen (1.811 $/Jahr, Power 0,24), Coast-Leg-Spanne, ob es noch 670 Bank-Zeilen sind. Start wartet auf Max' drei Ideen und die Teil-B-Session.
