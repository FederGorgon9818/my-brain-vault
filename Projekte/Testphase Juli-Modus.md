---
tags:
  - projekt/trading
  - trading/alpha
  - trading/prozess
erstellt: 2026-09-22
status: läuft (Idee 1 bis 6 bis Stufe 2, keine Prämisse trägt)
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
| 2 Prämissen-Tafel | EINE Tabelle ohne Strategie: Gruppen der These × mittlere gerichtete Bewegung in Punkten mit 90 %-CI, Trefferquote, N Tage, getrennt 2016-19 / 2020-23 / 2024-26, Kosten in denselben Punkten, Gegengruppe daneben | **trägt** = obere 90 %-Grenze der gerichteten Bewegung liegt in keiner Epoche unter 0 (CI-Gate), N je Epoche mindestens 60 Tage, Bewegung im Mittel über den Kosten, Gegengruppe zeigt es nicht. Vorzeichen-Konsistenz ist Zusatzinfo, kein Killer (Dreifach-Konjunktion auf Punktschätzern tötet echte 3-pp-Effekte, P4 andersherum). Sonst Ende nach ~20 Min. **Rechenweg seit 01.10.2026:** `engine/tafel_lib.py`, `pruefe(y, gruppe, sesoi, kosten=)` mit SESOI vorab (ehrliches Band, Jahres-Fixeffekte, Etikett-Rotation bei Filtern, Vola-Pflichtzeile bei Vola-Thesen, Kategorie mit Pflichtsatz der Wiedervorlage, Lehren aus #178). Ob `kategorie()` das „trägt"-Kriterium davor ersetzt (dann wären Epochen und N ≥ 60 nur noch Info), entscheidet Max. Bis dahin stehen beide nebeneinander in der Tafel. |
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

### Ergebnis Teil B (24.09.2026, Session eadffd5a, Quant-Team)

Stempel: Engine-Fingerprint `91c972fe`, Buch 3 Beine (book_state.json), 50k-Tier, Rechenweg exakt wie `book_marginal_confirm` (B=200, Block 10, Seed 17). Rechnungen und JSONs: `engine/_scratch_gate_kalibrierung/`. Nichts an Engine/Buch geändert.

**1. Unsere Beine als Fremde gegen das 2-Bein-Restbuch: alle drei fallen durch.**

| Bein | Δ Passquote | Streuung | 90 %-CI | Schwelle k2 / k8 | Gate heute | gepaart gegen Nulldrift-Zwilling |
|---|---|---|---|---|---|---|
| Momentum | +2,1 pp | 4,8 | −3,9 bis +10,6 | 7,8 / 10,6 | nein | +4,6 (z 1,25, knapp unter Schwelle, mit 10 Zwillingen neu rechnen) |
| LastHour_v3 | +5,2 pp | 8,2 | −4,1 bis +21,2 | 13,4 / 18,3 | nein | +16,4 (z 2,55, besteht) |
| Asia-Dir | −2,7 pp | 5,2 | −11,5 bis +4,1 | 8,5 / 11,6 | nein | +2,4 (z 0,39, nein) |

- Echte Streuung bei ganzen Beinen 4,8 bis 8,2 pp, nicht ~3 pp wie angenommen. Power des heutigen Gates für einen echten 3-pp-Effekt: **0,10 bis 0,16** (nicht 0,24). Für 50 % Power bräuchte das Maß „Δ Passquote gegen null" 45 bis 130 Jahre Historie.
- Die richtige Null ist negativ: ein Zufalls-Bein ohne Edge kostet das Buch über seine Varianz allein 2,5 bis 11 pp. Das Gate testet gegen 0 und ist damit um genau so viel zu streng.
- LastHour trägt seine +5,2 pp komplett über **Tempo** (ohne 36-Monats-Grenze −0,15 pp). Das passt zum Ziel Zeit bis 50k.
- Asia-Dir kostet im Punkt auch ohne Zeitgrenze ~4 pp (Intraday-Tiefs summieren sich, Verlust-Cluster), statistisch aber nicht von 0 unterscheidbar. Gehört zu AP183, nicht zur Gate-Frage.

**2. Seltene Grade-A-Strategien aus dem Vergleich-Tab (Zusatz Max, 6 bis 15 Trades/Jahr) als 4. Bein, heutige Engine, ORB nur ehrlich:**

| Strategie | Trades | $/Jahr (1 Kontrakt) | Δ pp | 90 %-CI |
|---|---|---|---|---|
| REFINE_ORB_2 (close) | 152 | 531 | +1,45 | −1,6 bis +3,8 |
| OPEXMOM_ES | 74 | 193 | +1,06 | −1,6 bis +5,6 |
| EVENT_ES_primary | 110 | 265 | +1,03 | −2,0 bis +4,7 |
| OPEXMOM_RTY / _YM | 85 / 102 | 82 / 95 | +0,7 / +0,5 | beide um 0 |
| OPEXMOM_NQ | 66 | 257 | −0,1 | −4,7 bis +6,5 |
| FOMC-post ES, ORB maxwin/nr7 (close) | 44 bis 81 | 33 bis 124 | ~0 | um 0 |
| Korb OPEXMOM_NQ + EVENT_ES | 176 | 515 | −0,1 | −6,3 bis +6,0 |
| Korb 4 Kalender-Beine | 363 | 679 | −0,8 | −8,3 bis +7,1 |

- Keine ist von 0 unterscheidbar, die Körbe sind schlechter als die Einzelbeine (Varianz und Intraday-Tiefs summieren sich, OpEx NQ/ES/YM korrelieren 0,83 bis 0,96, das ist **ein** Bet, nicht vier; vor 2020 Edge ≈ 0).
- ORB-Reports aus dem Juli liefen im Look-ahead-Modus (`orb_exec` book). Ehrlich mit Stop-Order bleiben 5 bis 15 Trades in 10 Jahren, mit close ist ORB_maxwin tot (expR −0,02), nr7 im OOS negativ. REFINE_ORB_2: close 152 Trades, stop_honest 15, Look-ahead-Verdacht bei der Juli-Auswahl.
- Mathematiker: Frequenz ist nicht das Problem, **Sharpe** ist es. Ein Bein wird über dem Gate sichtbar ab Jahres-Sharpe ≈ 1,9 (1,25 × Buch), egal wie oft es handelt. Die seltenen liegen bei 0,1 bis 0,7, bei 7 bis 10 Trades/Jahr bräuchte es ≳ 2.000 $/Jahr je Kontrakt. Für einen Korb aus Sharpe-0,6-Beinen bräuchte es ≥ 10 wirklich unabhängige Mechanismen.
- Offen: Beitrag bei θ-optimaler Größe statt 1 Kontrakt nie gerechnet (Juli-Buch hatte OPEXMOM 6 bis 8× Gewicht).

**3. Frequenz-Gates:** `min_tpy=25` und `min_trades=100` sind Proxys, keine Statistik (min_trades zitiert Lehre 113 falsch, θ hängt nicht an der Frequenz). Ein Bootstrap-/t-Gate hält seine Fehlalarmrate schon ab n=30. Weitere versteckte Frequenz-Gates: `min_oos_trades=25`, `top5_share_max` (hängt mechanisch an n).

**4. Vorschlag neues Lineal (Entscheidung Max, noch nicht umgesetzt):**

| Design | Fehlalarme je Job (Edge 0) | Power 3 pp | Fehlalarme je 500 Jobs |
|---|---|---|---|
| heute (k2) | 0,001 bis 0,016 | 0,10 bis 0,16 | ~1 bis 15 |
| gepaart gg. 10 Zwillinge, α 0,10, + Δ real ≥ 0 | 0,04 bis 0,09 | 0,53 bis 0,62 | 20 bis 46 |
| gepaart, α 0,05, + Δ real ≥ 0 | 0,025 bis 0,05 | 0,39 bis 0,60 | 12 bis 25 |
| gepaart, α 0,02, + Δ real ≥ 0 | 0,013 bis 0,02 | 0,25 bis 0,53 | 7 bis 10 |

Bei 2 % echten Mechanismen: heute ~1,3 echte Funde auf ~4 falsche, mit α 0,02 ~4 echte auf ~8 falsche (gleiche Reinheit, 3× mehr Funde).

- Stufe 1 Edge-Nachweis: gepaart gegen ≥ 10 Nulldrift-Zwillinge, ein gepoolter Test je Mechanismus (k=1, kein Šidák mehr), α 0,02 bis 0,05.
- Stufe 2 Buch-Nutzen: Δ real ≥ 0 im Punkt statt Signifikanz. SD-Boden 3 pp weg (kostet seltene Kandidaten Power 0,45 → 0,17).
- Vor-Gates: `min_trades` 100 → 30, `min_oos_trades` 25 → 10, `min_tpy` streichen, dafür Beleg t = SR·√Jahre ≥ 2 und Sharpe-Kriterium SR_c/SR_b ≥ 1,25. `top5_share_max` → „Erwartungswert ohne Top 5 % Trades > 0".
- #106 bleibt: 5 % Placebo-Jobs (Zwilling als Kandidat) durch die ganze Kette, Alarm, wenn deren Durchlassquote über α + 2·SE liegt. „0 %" gibt es bei keinem Test, erreichbar ist „genau α".
- Das Next-Week-Buch ist **keine** statistische zweite Stufe (3 Monate Forward = 6,5-fache SD). Echte Zusatzevidenz nur aus unabhängigen Kontrollen (Delay, Spiegel, zweiter Markt).
- 36-Monats- und Passquote ohne Zeitgrenze getrennt ausweisen (Tempo-Bein vs. Sicherheits-Bein).

**5. Gate v2 beschlossen (Max, 24.09.2026, α 0,02) und an den drei Beinen durchgerechnet** (10 Zwillinge, `gate_v2_legs.py` → `v2res_*.json`):

- Stufe 1 Edge: gepaart gegen 10 Nulldrift-Zwillinge, ein Test je Mechanismus (k=1), einseitig α 0,02 (z 2,05).
- Stufe 2 Buch: Δ Passquote real ≥ 0 im Punkt.
- Beleg: Sharpe-t = SR_ann·√Jahre ≥ 2 statt Frequenz-Filter.
- Kontrolle: Placebo-Jobs (#106).

| Bein | Stufe 1: Edge über Zwillinge (pp) | Schwelle | P(besser als Zwillinge) | Stufe 2: Δ Buch | Sharpe-t | Ergebnis |
|---|---|---|---|---|---|---|
| LastHour_v3 | +19,0 (sd 6,5) | 13,4 | 1,00 | +5,4 | 3,67 | **besteht** |
| Momentum | +4,4 (sd 3,65) | 7,5 | 0,89 | +2,1 | 2,86 | Stufe 1 nein (auch bei α 0,10 knapp nein: 4,4 gegen 4,7) |
| Asia-Dir | +2,7 (sd 5,8) | 11,9 | 0,67 | −2,7 | 2,62 | nein, beide Stufen |

Lesart: Das neue Gate hätte LastHour gefunden, das alte keines der drei. Momentum hat im Buch-Maß eine plausible, aber nicht belegte Edge (89 % Wahrscheinlichkeit besser als Münzwurf). Das liegt an der Beweislage des Beins, nicht am Lineal. Asia-Dir ist weder als Edge noch als Buch-Beitrag belegt, das gehört zu AP183. Kein Stempel „tot" für eines der Beine: Kategorie `unentscheidbar` im Buch-Maß, Einzel-Sharpe-t liegt bei allen dreien über 2.

**Vorbedingungen / offene Punkte:** ~~Momentum mit 10 Zwillingen nachrechnen~~ (erledigt, siehe 5) (entscheidet α 0,10). LastHour-Zwilling hat 11 bis 14 % weniger Trades als das Original (kein reines Richtungswürfeln, Frage an pipeline-auditor). `cal`/`orb` haben keinen Null-Schalter (sonst läuft Design B dort leer). θ-Surrogat ersetzt die MC nicht (Rangkorrelation 0,18), höchstens Kill-Filter ab < −3 pp. **Nebenfund Falle:** Min-Size in `cage_policy_lib.evaluate_v2` hängt an frac 0,01 und Median-Intraday-Tief > 30 $ (heute 35 bis 48 $). Ein Kandidat mit vielen kleinen Verlusttagen rechnet still auf 2 Kontrakte hoch.

---

## 4. Stand und Ideen-Sammlung

| # | Idee (Markt, Beobachtung, Warum, Wann) | Stufe erreicht | Ergebnis | Datum |
|---|---|---|---|---|
| 1 | ES/NQ/GC. Fr-High < Do-High ⇒ Montag holt in der RTH das Fr-Tief. Why fehlt (Claude-Entwurf vom strategy-auditor verworfen). Montag RTH | 2 (Prämissen-Tafel) | **trägt nicht** für den Short ab Montag-RTH-Open: Treffer 27 bis 34 % (mit Gap-Fällen unter 50 %), Überschuss über Montags-Placebo ES +1,5 %, NQ +5,2 %, GC −4,1 % (alle CI über 0), netto negativ in allen 6 Zellen. Effekt ≥ ~10 pp ausgeschlossen, kleinere nicht auflösbar. Offen: Einstieg Sonntag 18:00 ET (Gap-Fälle). `engine/_scratch_juli_frlh/`, Lab-Tests `20260926_frlh_*`. Stempel im Logbuch noch offen. **Why-Recherche 28.09.:** kein erzwungener Wochentags-Akteur (Chen/Singal widerlegt, externer Backtest ~Zufall), einziger tragfähiger Kandidat Monatsende-Zahlungsdruck (Etula 2020 + Wang/Li/Erickson 1997), ungeprüft | 26.09.2026 |
| 2 | *(von Max, 29.09.)* NQ und ES. Wenn beide wenig Vola haben, ist ein Bullmarkt wahrscheinlicher. Why aus der Recherche: Vol-Control-Fonds bauen in ruhigen Phasen Hebel auf (asymmetrisch, im Spike ist der Abbau stärker). Tageszeit offen, geprüft wurden RTH und Nacht | 2 (RTH) und 2b (Nacht) | **RTH trägt nicht** (`empirisch-nichts-gefunden`): ruhige Tage −3,4 gegen +6,1 Pkt an volatilen (rollierend +1,6 gegen +8,6). Die These gilt nur gleichzeitig (Bull 90 % gegen 28 %), nicht als Vorhersage (60 Sessions später 58 % gegen 57 %, Folgerendite eher kleiner). **Nacht bei absolut ruhigem Markt unentscheidbar:** Überschuss +4,9 bp je Nacht, aber nur 2020 bis 2026, gemessen ohne das handelbare Fenster. Relative Ruhe zeigt nichts. Nacht-Folge siehe Idee 3 (#178): auch mit 24h-Daten nicht entscheidbar. Logbuch **#177**, `engine/_scratch_juli_lowvol/` | 29.09.2026 |
| 3 | *(von Max, 29.09. abends)* NQ steigt in der Globex-Nacht (18:00 bis 09:30 ET, bei FN nach Auslegung erlaubt) bei niedriger Vola. Why aus der Recherche: Keine Studie testet das, die Literatur sieht die Nachtdrift eher nach Abverkäufen. Einzige Vola-Stütze ist Moreira/Muir (Vola sagt das Risiko voraus, nicht die Rendite), also gerade die Null | 2 (Kern-Fenster 00:00 UTC bis 09:30 ET, rekonstruiert) | **unentscheidbar** (Power, auch mit absehbaren Daten), beide Definitionen. Absolut ruhig +5,5 gegen +2,9 bp je Nacht. Der Überschuss von +2,6 bp liegt je nach Fehlerschätzung knapp über oder unter 0, innerhalb der Jahre bleiben +0,8 bp, die MDE liegt bei rund 6 bp. Relativ ruhig −0,8 bp (Richtung gegen die These), YM nichts. Explorativ fällt nur das Risiko, die Drift bleibt flach (Muster der Null). Kein Grid, kein Werkzeugbau. **01.10. auf Ansage Max durch Gate v4:** keine Variante besteht, einzeln wie als Job (knappster Fall: ruhig absolut mit Sharpe-t 1,92 statt 2,0), auch Max' Drawdown-Regel fällt, nichts ins Next-Week-Buch. Logbuch **#178** (mit Nachtrag), `engine/_scratch_juli_nacht/` | 29.09.2026 |
| 4 | *(von Max, 12.10.)* NQ, VWAP-Pullback v8 (long, SL 80 / TP 120, seit 18.09. nicht im Buch). Das Bein von der jüngsten Vergangenheit abhängig machen: Vola der letzten 1/2/5/20 Tage gegen Schnitt (Beispiel Max: mindestens 30 % drüber), Trend der letzten 1/2/5/20 Tage, klare Trigger- bzw. Eröffnungskerze, erste 5/15/30-Minuten-Kerze grün → nur Long, rot → nur Short. Why nur als Entwurf (strategy-auditor: A/B/D mit Vorbehalt, Trigger-Kerze fällt als Story durch) | 2 (Prämissen-Tafel, 22 Zellen, SESOI vorab 8 Punkte je Handelstag) | **trägt nicht**, kein Grid. Frische Basis auf der gefixten Engine: 1.272 Trades, +5,1 Punkte je Trade netto (2016-19 +1,4 / 2020-23 +10,5 / 2024-26 +1,9). **18 Zellen `empirisch-nichts-gefunden`** (kein Filter hebt das Bein um 8 oder mehr Punkte je Tag, kleinere Effekte nicht ausgeschlossen), **4 `unentscheidbar`** (Vola 5 Tage ≥ 1,3× und die drei Short-nach-rot-Zellen). Max' Beispiel läuft eher andersherum: nach Tagen mit 30 % mehr Range ist das Bein schlechter (−7 bis −10 Punkte je Tag bei 1, 2 und 20 Tagen), die Gegenrichtung bringt aber nur rund +2 Punkte je Tag und 2016-19 ist das Vorzeichen umgekehrt: Hinweis, kein Fund. Einzige echte Auffälligkeit: gespiegelter Short nur nach roter erster 15-Minuten-Kerze (n 606, +4,4 Punkte je Trade, alle Epochen positiv, Rotation p 0,016), aber 1 von 22, Nachbarn 5 und 30 Minuten tragen nicht, t 1,5 unter dem Vor-Gate. Das wäre ein neues Short-Bein, kein Filter. Nicht tot. Trigger-Körper nur als nachträgliche Auswahl geprüft, nicht als Gate in der Engine. **Wiedervorlage:** Short nach roter 15-Minuten-Kerze unverändert auf Daten ab 11.08.2026, sobald rund 150 neue Short-Trades da sind (rund 1,5 Jahre). Stempel: Engine `00009138…bf26`, Daten bis 10.08.2026, Long bitgleich zu qbt, Kosten 1,01 Punkte je Trade. `engine/_scratch_juli_vwapfilter/`, Lab-Test `20261012-2021_juli4_…`. Logbuch-Eintrag offen | 12.10.2026 |
| 5 | *(von Max, 12.10. nachts)* NQ. Mean Reversion nach einem News-Release: die Erstreaktion läuft zurück. Läuft als **Messung ohne Why** (strategy-auditor: das Liquiditäts-Why ist ein Sekunden-Effekt und in #105 widerlegt). Vorläufer #105/#109 vom 16.08., beide ohne Stempel | 2 (Prämissen-Tafel, 23 Zellen vorab, SESOI 3 bp je Event netto, 508 Releases um 08:30 ET plus 84 FOMC) | **trägt nicht**, kein Grid. **Gepoolter Fade** (alle 08:30-Releases, Einstieg 5 Min nach dem Release gegen die Erstreaktion, raus nach 60 Min): −0,02 bp je Event, 95 % [−2,9; +2,9], Treffer 50 %, normale Tage zur selben Uhrzeit −0,01 → `empirisch-nichts-gefunden` (nötig wären 4 bp brutto). Große Jumps −1,4 bp (eher Fortsetzung, `unentscheidbar`). **Einzige Auffälligkeit: NFP bis T+60** +7,4 bp (t 2,27, n 117, alle Epochen positiv), aber 1 von 23 (Max-t p 0,19), 6 Events tragen 70 %, sitzt in 2021 bis 2023, roh rund 350 $/Jahr je Micro → `unentscheidbar`, Hinweis, kein Fund. Die Rückkehr kommt fast ganz aus 09:00 bis 09:30, das sähe eher nach Drift in die Kassa-Eröffnung aus (nachträglich gefunden, wäre eine eigene Idee). CPI, sonstige, FOMC, Bedingungen: `unentscheidbar` (zu wenig Power). **Wiedervorlage NFP:** nur mit NQ-Minutendaten vor 2016 (Databento), unverändert. Stempel: `news_calendar.py` 23.08.2026, `tafel_lib.py` 02.10.2026, Engine `e6f39975…347f`, NQ bis 10.08.2026 (dieselben Daten wie #105, keine unabhängige Bestätigung). `engine/_scratch_juli_newsmr/`. Logbuch **#181** | 12.10.2026 |
| 5 | *(von Max, 12.10.)* Kaufen, wenn Politiker kaufen (US-Kongress, STOCK-Act-Offenlegungen). Markt offen: die Meldungen betreffen Einzelaktien, prop-fähig wäre nur ein Index-Signal. Why nur als Entwurf (Wissen aus Ausschüssen, bis 45 Tage Meldeverzug) | 1 (Register-Check und Recherche, `konzept-weg` plus Nachrecherche) | **Keine Prämissen-Tafel, nichts gerechnet, kein Urteil.** 0 Trials, keine Kongress- und keine Aktien-Daten. 27 Wege in [[Politiker-Käufe Wege-Karte]]. Die zwei prop-fähigen Wege (Kongress-Nettokauf als Tages-Tor auf Momentum bzw. als eigenes NQ-Long-Bein) haben einen Gegenbeleg aus der Literatur: Aggregat-Effekt nur 2004 bis 2014 belegt, Horizont 2 bis 3 Monate, nach 2012 nichts gefunden. Die Aktien-Variante ist nach 2012 überwiegend negativ (Chen/Sacerdote 2012 bis 2023, Belmont 2022, Göteborg ab Offenlegung mit Kosten −40 bp pro Monat), einzige positive Untergruppe Fraktionsführung (Wei/Zhou, 20 Personen, nicht ab Offenlegung). Alles Abstract-Ebene. **Buch-Lücke:** hängt vor der Prämisse, es fehlen Daten und ein Why-Beleg. Billigste eigene Messung: NANC/KRUZ gegen QQQ/SPY. Entscheidung Max offen | 12.10.2026 |
| 6 | *(von Max, 12.10. nachts)* NQ. Die NFP-Bewegung 09:00 bis 09:30 ET: vor der Kassa-Eröffnung läuft der Preis gegen die Reaktion auf den 08:30-Release. Nachher-Fund aus Idee 5, NFP selbst ist deshalb kein Test. Why-Entwurf (Liquidität kommt vor der Eröffnung zurück) ohne gezwungenen Akteur | 2 (Prämissen-Tafel, 4 Test-Zellen vorab auf Gruppen ohne NFP, Schwelle z 2,5) | **trägt nicht**, kein Grid. CPI plus sonstige Releases +0,1 bp (95 % −1,7 bis +2,0), normale Tage 0,0 bp, alle Tage gegen die Nachtbewegung +0,9 bp (t 2,29, unter Schwelle und unter den Kosten, nur 2020 bis 2023) → alle vier `empirisch-nichts-gefunden`, das Why ist in der allgemeinen Form widerlegt. **NFP allein** bleibt auffällig (+5,9 bp, t 3,2, wächst über die Epochen +0,3 / +7,6 / +12,4, ES gleich) → `unentscheidbar`, Hinweis ohne Test. Wiedervorlage: neue NFP-Termine mitzählen (72 nötig) oder Daten vor 2016. Stempel: Engine `e6f39975…347f`, NQ bis 10.08.2026. `engine/_scratch_juli_newsmr/` (`prereg6.md`, `tafel6.py`). Logbuch **#182** | 12.10.2026 |
| 7 | *(von Max, 13.10.)* Gold (GC, gehandelt MGC). Ein Fremdmarkt liefert das Signal: Zinsen (ZN), Dollar (6E), Aktien (NQ). Kein Why belegt (Research 9 von 9 offen), läuft als Messung. COMEX-Fenster 08:20 bis 13:25 ET | 1 (Register-Check, `konzept-weg`) und 2 vorbereitet | **Tafel steht, Lauf noch nicht gestartet.** 0 von 2.777 GC-Trials haben eine Fremdmarkt-Achse. 45 Wege in [[Gold Cross-Asset Wege-Karte]]. Vorab-Festlegung `engine/_scratch_juli_gcx/prereg.md` (acht Test-Zellen, Test auf y / σ60, SESOI Sharpe-neutral, Holm plus Familien-Test), Quant-Team blind gegengelesen, Trockenlauf fehlerfrei. Einzelzelle erkennt erst Bein-Sharpe ab rund 1,1. Drei Entscheidungen bei Max (SESOI, Datenstand, Kosten), Ticket AP371 | 13.10.2026 |

**Offene Entscheidungen bei Max, die in diese Woche gehören:** AP183 (Slot-Tabelle umsetzen, Coast-Leg-Schalter, Live-Grade-Karte, Stufe-2-Design), AP211 (Bitcoin-Daten, prescan_gross).

**Log:**
- 22.09.2026: Analyse und beide Teile festgeschrieben, Trigger-Regel in CLAUDE.md, Teil-B-Prompt fertig. verdict-auditor (Pflichtkette `meta`) hat 12 Punkte geliefert, alle eingearbeitet: Kernaussage „0 neue Beine seit Runner" korrigiert auf „0 neue Mechanismen, Exit-Versionen aus den ersten Runner-Tagen", Slot-Tabelle-Stand, Schwellen-Spannen, Register-Stichtag; Teil A um Null-Schalter-Check, Zufallsdecke, OOS-only, CI-Gate statt Vorzeichen-Konjunktion, GC/CL-Vorschritt und Auftragstypen je Stufe ergänzt; Teil-B-Prompt um k_eff, Trade-Erzeugung, Zwilling-Weg, kanonischen Rechenweg, session-guard und #156-Quervergleich ergänzt. Nicht nachgerechnet vom Auditor: Quant-Zahlen (1.811 $/Jahr, Power 0,24), Coast-Leg-Spanne, ob es noch 670 Bank-Zeilen sind. Start wartet auf Max' drei Ideen und die Teil-B-Session.
- 29.09.2026: Idee 2 von Max („ruhig → Bull") in einer Cloud-Session bis Stufe 2b gerechnet. Dabei liefen research-scout (21 neue Claims im Research-Cache), verdict-auditor (hält mit Auflagen) und logbook-distiller. Das Urteil steht als #177 im Logbuch. `ein-weg` wurde bewusst ausgelassen, weil die Prämisse in Stufe 2 durchfiel und es damit kein Grid gab. **Vorschlag an Max (Lehre 2 aus #177):** In Stufe 2 bei Richtungs-Thesen die Fenster RTH, Nacht und Schluss zu Schluss als Pflichtspalten vorab festlegen und als Auswahl zählen. Hier lag das einzige Signal in der Nacht, gefunden wurde es erst im Nachgang. Die Stufe-2-Zeile oben ist unverändert, bis Max entscheidet.
- 29.09.2026 abends: Idee 3 von Max („NQ steigt nachts bei niedriger Vola") in der Cloud-Session bis Stufe 2 gerechnet (Nacht aus Tagesbars rekonstruiert, Kern-Fenster). Dabei liefen research-scout, quant-statistician, quant-mathematician, verdict-auditor (hält mit Auflagen) und logbook-distiller. Das Urteil steht als #178 im Logbuch: unentscheidbar, auch mit absehbaren Daten. `ein-weg` wurde bewusst ausgelassen. Die #177-Wiedervorlage „Nacht-Tafel am PC mit 24h-Daten" ist damit überholt, sie hätte 1 bis 3 bp nicht entscheiden können (Lehre 2 in #178). **Vorschlag an Max (Lehren 1 bis 5 aus #178):** ein Tafel-Helfer `engine/tafel_lib.py` (rund 110 Zeilen). Er soll enthalten: robustes Episoden-Band, Jahres-Fixeffekte, Etikett-Rotation als Filter-Zwilling, die Null „Drift flach" und `kategorie()` mit Feasibility. Verdrahtet würde er in Stufe 2. Die Entscheidung liegt bei Max.
- 12.10.2026: Idee 4 von Max (Filter auf dem VWAP-Pullback v8 nach jüngster Vergangenheit, Kerzen-Klarheit, erste Kerze als Richtung) bis Stufe 2 gerechnet. `ein-weg` lief vorab (variant-scout × 4, strategy-auditor Batch), verdict-auditor hat das Urteil mit Auflagen gehalten (Kategorien 18 / 4 / 0 statt Sammelstempel, Short nach roter 15-Minuten-Kerze namentlich als unentscheidbar). **Lehre für `tafel_lib` (Ticket-Vorschlag, nicht umgesetzt):** das Episoden-Band klebt täglich wechselnde Etiketten (grün/rot, Vortag hoch/runter) zu 2 bis 4 Episoden zusammen und liefert dann Bänder von ±20 Punkten; für solche Etiketten ist das Jahres-Fixeffekt-Band das passende Lineal. Nebenbei: der PC hat kein scipy, `tafel_lib` lief nur mit einem Mini-Ersatz im Scratch-Ordner.
- 12.10.2026 abends: Folgeauftrag Max zu Idee 4 („dieselbe Logik auf andere Sessions und Gold, Parameter passend skalieren“). Als unveränderte Replikation gefahren, Regel vorab festgelegt (`xs_prereg.md`): Stop = 5,16 × mittlere 5-Minuten-Schwankung der Zelle, fest in Punkten, Ziel 1,5×, Stunden-Schwelle mitskaliert, alle Zeiten als Minuten ab Session-Start, ein Lauf je Zelle. Zellen: NQ Asia (20:00 bis 02:30 ET, Stop 26), NQ London (03:00 bis 09:30, Stop 41,25), Gold Asia (4,20), Gold London (5,90), Gold US (08:20 bis 14:50, 8,10). quant-mathematician hat die Skala bestätigt (Range und sigma·√T geben denselben Stop auf ±7 %), quant-statistician das Ergebnis geprüft. **Urteilsvorschlag Quant-Team, noch kein Logbuch-Stempel:**
  - **Short nach roter 15-Minuten-Eröffnung: `empirisch-nichts-gefunden`** (5 Zellen plus Ursprungszelle). Gepoolt +0,011 R vor Kosten [−0,017; +0,040], 2 von 5 positiv, nach Kosten alle fünf negativ. Die Größe aus der NQ-Tageszelle (+0,064 R brutto) ist mit rund 98 % Power ausgeschlossen. Kein nächster Test.
  - **Long nur nach ruhigen Tagen (Range der letzten 2 Sessions unter 1,3 × 20er-Schnitt): `echt-aber-zu-klein` auf NQ, auf Gold `empirisch-nichts-gefunden`** (3 Zellen). NQ gefiltert minus aussortiert +0,125 R [+0,053; +0,199], in allen drei NQ-Sessions gleiches Vorzeichen. Kein reiner Drift-Effekt (Long ohne Signal an denselben Tagen zeigt +0,00 bis +0,04, mit Signal +0,10 bis +0,14). Aber: kommt fast ganz aus 2020 bis 2023, effektiv rund 1,5 unabhängige Bestätigungen, und der Effekt sitzt in den schlechten aussortierten Trades. Als Filter auf dem Tages-Bein bringt er rund 0,5 R im Jahr (etwa 80 $ je Micro, Fehlerbalken −1,7 bis +2,7 R). NQ Asia als eigenes Bein: +0,054 R netto [+0,009; +0,098], geschrumpft rund 150 $ je Micro und Jahr, 2016-19 negativ.
  - **Buch-Lücke:** hängt an der Stufe Buch-Marginal (Ersatz), nicht mehr an der Prämisse. Einziger sinnvoller nächster Test: v8 gegen v8 plus Filter am aktuellen Buch, 5 Seeds, vorab festgelegt; Erwartung des Statistikers: im Rauschen.
  - Stempel: Engine `00009138…bf26`, NQ bis 10.08.2026, Gold bis 24.07.2026, Kosten 2 Ticks plus Kommission (Gold nachts eher optimistisch). Schwächen: feste ET-Uhrzeiten treffen Tokio und London wegen der Sommerzeit nur das halbe Jahr, Delta-Näherung nachts verrauscht, Kontrollzelle NQ tagsüber über die neue Pipeline 1.253 statt 1.272 Trades (Sessions unter 300 Bars fallen raus). Rechnung: `engine/_scratch_juli_vwapfilter/` (`xsession.py`, `xs_result.json`, `xs_pool.json`, `stat/chk.py`).
- 12.10.2026 nachts: zwei Folgetests auf Ansage Max, beide vorab festgelegt (`ruhe_prereg.md`), je ein Lauf, Engine `00009138…bf26`, NQ bis 10.08.2026.
  - **Ruhe-Filter auf die aktiven Beine (Momentum, LastHour, Asia-Dir, OpenDrive, RTY-Gap): hilft nicht, schadet dem Buch.** Die aussortierten „wilden“ Tage verdienen Geld: gepoolt +0,170 R je Trade (Band +0,049 bis +0,295, 548 von 2.541 Trades), ruhig +0,269, Unterschied +0,099 [−0,048; +0,240]. Buch mit 1 Micro je Bein: ohne Filter 6.495 $/Jahr bei Tages-Sharpe 2,17, mit Filter 4.957 $/Jahr bei 1,97. Je Bein sind die wilden Tage bei LastHour (+0,148), Asia-Dir (+0,449) und OpenDrive (+0,250) sogar besser als die ruhigen. Einzige Ausnahme Momentum: Long an wilden Tagen −0,205 R (n 101, Band ±0,35, in Geld −16 $/Jahr), Short an wilden Tagen +0,676. Das ist ein Hinweis aus einem Nachher-Schnitt, kein Fund, und in Geld ohne Gewicht. Kategorie `empirisch-nichts-gefunden` (5 Beine, 1 Schwelle), Reichweite: Tages-Etikett Range 2 gegen 20 Sessions unter 1,3 als Gate auf die Beine des Buchs vom 12.10., 1 Micro je Bein, Tages-PnL statt Käfig-Rechnung. Der Befund vom Abend („echt-aber-zu-klein“ am VWAP-Pullback) überträgt sich damit nicht auf andere Long-Beine.
  - **Skalierungs-Methode auf die aktiven Beine (Momentum, LastHour, OpenDrive auf NQ Asia, NQ London, Gold Asia, Gold London, Gold US): die Methode läuft, die Beine übertragen sich nicht.** Kontrolle NQ tagsüber reproduziert das Buch (Momentum +0,545 R, LastHour +0,099, OpenDrive +0,169). In den 15 neuen Zellen liegt kein Bein vor Kosten in 4 von 5 Zellen im Plus (Momentum 3/5 um null, LastHour 3/5 bei rund +0,02, OpenDrive 3/5 bei rund +0,02), nach Kosten sind 11 von 15 negativ, die besten (Gold London Momentum +0,116 ±0,366, OpenDrive Gold London +0,023 ±0,027) liegen im Rauschen. Kosten fressen nachts 0,08 bis 0,21 R je Trade bei Momentum und LastHour. Die Beine haben keine Punkt-Parameter (Stops hängen schon an Range/ATR/Sigma), skaliert wurde nur die Prozent-Schwelle. Asia-Dir und RTY-Gap nicht übertragen (über Sessions hinweg definiert). OpenDrive feuert nachts sieben Mal so oft (1.770 statt 255 Trades), ist dort also nicht dieselbe Strategie. Kategorie `empirisch-nichts-gefunden` (15 Zellen), nicht tot: die Beine sind an ihre Session gebunden (Eröffnung, Schlussstunde), was zu ihrem Why passt.
  - Quant-Team hier mit Grund ausgelassen (kein Grenzfall), Rechnung: `engine/_scratch_juli_vwapfilter/` (`ruhe.py`, `ruhe_trades.pkl`, `xs_legs.py`).
- 12.10.2026 spät: Idee 5 von Max („Mean Reversion nach einem News-Release“) bis Stufe 2 gerechnet, Urteil als **#181** im Logbuch. Stufe 1 fand die Vorläufer #105/#109 ohne Stempel; gemessen wurden deren offene Punkte auf doppelter Eventmenge. Kette: `ein-weg` vorab (variant-scout, strategy-auditor: nur als Messung ohne Why), quant-statistician und quant-mathematician auf dem Ergebnis, verdict-auditor (hält, acht Auflagen eingearbeitet), logbook-distiller. Wiedervorlage NFP in `wiedervorlagen.json` (`lb181_nfp_vor2016`). **Zwei Lehren für `tafel_lib` (Ticket-Vorschlag, nicht umgesetzt):** das Episoden-Band verklebt häufige Etiketten (505 Events → 6 Episoden, zweiter Fall nach Idee 4), und „trägt“ je Zelle berücksichtigt die Zahl der gezählten Zellen nicht (NFP bekam „trägt“ bei Max-t p 0,19). Offen bei Max: ob die nachträglich gesehene NFP-Drift 09:00 bis 09:30 eine eigene Idee wird (bräuchte frische Daten).
- 12.10.2026 spät, Folgeauftrag Max zu Idee 5: als Strategie mit Trades gerechnet (12 Varianten vorab, Stop 1,0 / 0,5 / keiner, Ausstieg 09:30 oder Pre-News-Preis). Alle Releases −252 bis +35 $ im Jahr je Micro, NFP +23 bis +202 $ (Max-t p 0,09, ohne die besten 5 % der Trades rund 0). Urteil unverändert. Vier Karten im Tests-Tab, Report: [[News Mean Reversion Report (12.10.2026)]].
- 13.10.2026: Idee 7 von Max (Gold Cross-Asset). `konzept-weg` (familien-scout, verdict-auditor, research-scout) lieferte die Wege-Karte, danach Stufe 2 nur vorbereitet: Vorab-Festlegung und Skript, Kette `rechnen` (quant-mathematician, quant-statistician) auf dem Entwurf statt auf dem Ergebnis. `ein-weg` bewusst ausgelassen (Messung ohne Strategie, kommt vor einem Grid). **Drei Lehren für jede künftige Tafel (stehen als AP374 im Backlog, nicht umgesetzt):** (1) auf vola-normierter Größe testen, sobald sich die Vola im Datensatz vervielfacht hat (Gold 5,6 → 33 Punkte), sonst misst die Tafel nur die letzten Jahre; (2) die SESOI als Jahres-Sharpe gegen das Buch herleiten, nicht als runde Punktzahl (hier lagen 0,5 und 2,0 Punkte in beide Richtungen falsch); (3) vor dem einen Lauf einen Trockenlauf mit Zufallsvorzeichen fahren (der Lauf wäre am fehlenden scipy abgebrochen). Dazu: `tafel_lib.pruefe` klebt Ereignistage mit der festen Lücke von 20 Sessions zu 2 bis 6 Episoden zusammen.
