---
tags:
  - projekt
  - bereich/softwareentwicklung
  - strategy-lab
erstellt: 2026-09-24
status: gebaut (lokal), Box-Sync + NT8-Deploy offen
---
# 🧰 Strategy Lab Workbench (ersetzt den Developer-Tab)

⬅️ [[Strategy Developer]] · [[Design-System (Hub & Apps)]] · [[Backtest-Engine]]

## Anlass (Max, 24.09.2026)

Max bekommt von Claude nur Zahlen, sieht aber nie selbst, wie eine Strategie tradet. Muster wie die Regimefilter wären ihm so nie aufgefallen. Das Strategy Lab soll wie eine App behandelt werden, die aktiv gepflegt wird: jeder neue Test ist dort sichtbar, und der Developer wird durch eine Workbench ersetzt, in der Max Equity, alle Trades, Patterns und Filter selbst sieht und prüft.

## Bestand (24.09.2026)

- Lab-Reports sind statische HTML-Seiten (`report.py`) ohne Trade-Liste und ohne Chart. Trades werden nicht gespeichert.
- Developer-Tab hat einen Kerzenchart mit Trades, aber nur die letzten 40 Sessions, nur RTH.
- Parameter/Filter im UI nicht änderbar, nur über Chat oder Claude Code.
- Tests aus Claude-Sessions (ein-weg, Juli-Modus, Regime-Vergleiche) erscheinen nicht im Lab.
- Frontend steckt als String in `app_server.py` (~4.600 Zeilen).

## Entscheidungen von Max (24.09.2026)

1. Chart-Prüfung: eigener Chart im Lab **plus NT8-Overlay** (Trades auf dem NT8-Chart). Kein TradingView.
2. Die Workbench **ersetzt den Developer-Tab**.
3. Filter: **alle Merkmale vorhanden und frei kombinierbar.**
4. Konzept als Projektnotiz mit Tickets pro Phase.
5. Zusätzlich: **Overfit-Risiko in %** und **P(Pass) in % je Prop-Firma** immer sichtbar.
6. Übersichtlich halten, gleiches Schema wie der Rest des Labs, nicht zu viele Daten auf einmal.

## Konzept

### Ein Datensatz pro Test
Jeder Test schreibt dasselbe Format (Developer, ein-weg, Juli-Modus, Discovery-Kandidat, Regime-Vergleich): alle Trades (Entry, Exit, SL, TP, R, MAE, Exit-Grund) **plus alle Merkmale zum Entry-Zeitpunkt** (Uhrzeit, Wochentag, Trend-/Vol-Regime, Gap, Vortagesrange, VIX, strategieeigene Werte), Equity, Kennzahlen, Parameter, Stempel. Das Lab liest nur noch dieses Format.

### Aufbau der Workbench (nach design-guard-Review)

| Bereich | Sichtbarkeit | Baustein |
|---|---|---|
| Kopfzeile: Name, Version, Stempel, **Overfit-Risiko %**, **P(Pass) % (E8, FN)**, Trial-Zähler als Meta-Zeile | immer | `bbPanel` + `.bbstrip`, max. 4-5 Zellen |
| Equity + Drawdown, OOS abgesetzt, Prop-DD-Linie, Klick springt zum Trade | immer | `.rcard`, volle Breite |
| Trades (Tabelle) links, Kerzenchart rechts, SL/TP-Box, Indikatoren, J/K, „Trade ist falsch", „In NT8 zeigen" | immer | `bbgrid` zweispaltig, Vorbild Live-Tab, Lightweight-Charts-Setup aus `report.py` |
| Patterns: R nach Merkmal-Buckets mit n + Fehlerbalken, zwei Merkmale kreuzbar | eingeklappt | `<details>` |
| Filter: freie Regeln aus allen Merkmalen, Wirkung sofort, Parameter-Edit startet Serverlauf, „Als Version speichern" | eingeklappt | `<details>` |
| Chat (zweiter Claude) mit Trade/Filter als Kontext | Randpanel oder unten eingeklappt | bestehender Developer-Chat |

### Schutz gegen Overfitting (fest eingebaut)
- Jeder angewendete Filter und jede Parameteränderung zählt als Trial, Zähler sichtbar.
- **Overfit-Risiko %** = PBO über die Trial-Menge der Session (CSCV, `overfit.py`), DSR mit echtem `n_trials` daneben.
- **OOS bleibt verdeckt**, solange gefiltert wird, aufgedeckt erst bei „Version einfrieren".
- **P(Pass) %** je Firma aus dem vorhandenen Prop-Check (Intraday-Bust-Check, Block-Bootstrap).

### Charta-Pflichten beim Bau (design-guard)
Nur bestehende Tokens (`--up`/`--down`/`--accent`/`--muted`), Radius `var(--radius)` = 6px, Abstände `--sp-*`. Serverlauf-Buttons mit `.devbtn.busy`. Folgenreiche Buttons (Trade ist falsch, Einfrieren) farblich abgesetzt. Zahlen Mono + `tabular-nums`. Leerer Zustand mit Satz + Grund. Beim Filterwechsel Platz reservieren statt leeren. Chart-Defaults identisch zu `report.py`.

### Lab als App pflegen
- Neue Workbench als eigene Frontend-Dateien, nicht mehr als String im Server. Alte Tabs ziehen später um.
- Jeder Test aus Claude-Sessions landet automatisch im Lab (Hook, analog zu den anderen Pflicht-Hooks).
- Selbsttest nach jeder Änderung: alle Tabs laden, Charts haben Daten. design-guard bei jeder Phase.

## Phasen

1. **Datensatz + Kern-Workbench:** Format je Test, Merkmals-Katalog, Kopfzeile mit Overfit-Risiko % und P(Pass) %, Equity, alle Trades + Chart ohne 40-Session-Limit, Patterns. Developer-Tab wird ersetzt.
2. **Filter-Panel:** freie Filterregeln, Trial-Zähler, verdecktes OOS, Einfrieren, Parameter-Edit, als Version speichern.
3. **Feed + NT8:** alle Tests aus Sessions automatisch im Lab (Hook), NT8-Overlay-Indikator (liest Trade-CSV, zeichnet Marker + SL/TP), „Trade ist falsch" als Ticket.
4. **Umzug:** restliche Lab-Oberfläche aus `app_server.py` in eigene Dateien, Selbsttest.

## Stand 25.09.2026: gebaut (alle vier Phasen, nur lokal)

**Bedienung:** Lab → Tab **Workbench** (ersetzt Developer, `topSwitch('dev')` leitet um). Sub-Tabs **Workbench** und **Tests**.

| Teil | Wo | Was |
|---|---|---|
| Backend | `engine/workbench.py` | Datensatz je Test (`runs/<id>/`: run.json, trades.json, trials.json, frozen.json), Merkmals-Katalog (Uhrzeit, Wochentag, Monat, Jahr, Richtung, Trend SMA50, Gap/ATR, Vortagesrange/ATR, 20-T-Rendite, Vola 20 T, Vola-Rang 250 T, Volumen Vortag, VIX Vortag, RVOL bis Entry, Bewegung bis Entry, dazu alle `*_entry`-Spalten der Strategie), alles nur Wissen vor dem Entry |
| Urteil | `workbench.verdict` | Vor-Gates = `discovery_lib.evaluate_config` (DEFAULT_GATES), Stufe 1/2 = Gate v2 aus dem Developer-Lauf, PBO über alle Filter-Trials (IS), DSR mit echtem n_trials. Keine zweite Gate-Definition. Trim-Regel = Engine-Wert (1 %, nicht 5 % wie oben im Konzept) |
| P(Pass) | `workbench.pass_rates` | `eval_plan.evaluate_v2`, **solo, Min-Size**, E8 50k (cage_v2_tiers) + FN 50k (tempo_plan, Kontrakt-Deckel 40 angenommen). 50k = primary tier wie Gate v2; 150k (Kaufplan) ergibt bei 1 Micro nur 1-2 % und wäre irreführend. **Kein Buch-Urteil**, FN ohne 40-%-Consistency-Regel, also zu hoch |
| Oberfläche | `engine/lab_ui/` | `index.html`, `lab.css`, `lab.js` (der frühere HUB-String, 1:1 ausgelagert, bytegleich geprüft), `workbench.css/.js`. UI-Änderung = Datei ändern + Browser-Reload, kein Server-Neustart |
| Filter-Version | `workbench.save_version` | neue Developer-Version filtert die Basis-Trades per `RULES`; `developer_run.py` gibt den Gate-v2-Zwillingen denselben Filter (`slicer`) |
| NT8 | `nt8_staging_20260924/Indicators/MaxLabTradeOverlay.cs` | liest `Documents\NinjaTrader 8\maxlab_trades\current.csv` (Button „In NT8 zeigen“ schreibt lokal + per scp auf die Box), zeichnet Entry/Exit/SL/TP/R. **Noch nicht kompiliert/deployt** (Wochenend-Deploy) |
| Tests-Pflicht | `.claude/hooks/on_stop.py` Teil 5 | Scratch-Test ohne `workbench.publish` → Session endet einmal nicht (Ausweg `mark.py tests_ok`) |
| Selbsttest | `engine/lab_selftest.py` | Dateien, JS-Syntax, alle Routen, Workbench-Auswertung, Bars, Patterns |

**Weg ins Buch (25.09.2026, Max):** `workbench.gate_status` rechnet je Stand die erste offene Buch-Stufe (Vor-Gates → Gate v2 Stufe 1 → Stufe 2 → Next-Week-Buch → Deploy) und was fehlt, aus `evaluate_config`/`DEFAULT_GATES` und Gate v2. Anzeige als Panel unter der Kopfzeile und auf jeder Test-Karte; Tests-Tab filtert/sortiert danach („am nächsten am Buch“). Fehlt in einem Gate-v2-Ergebnis die Schwelle, wird sie aus `paired_sd_pp` × z(α, k=1) nachgerechnet und als geschätzt markiert.

**Ausbau 25.09.2026 (Plattform-Recherche, Punkte 1-6):** Robustheit (Zwillings-Verteilung `start_twins`, Parameter-Plateau `start_plateau`, beide als Hintergrund-Job mit Cache `runs/<id>/twins.json`/`plateau_*.json`, nur bei 1:1 nachrechenbaren Tests), Pivot bis 3 Merkmale (`pivot_view`), Monte Carlo (`mc_view`), Kalender (`calendar_view`), Vergleich A/B im Tests-Tab. Walk-Forward bewusst nicht gebaut (quant-statistician: bei festen Parametern Theater), billige Stabilitätsansicht je Jahr als Option. Notizblock: AP256.

**Session-Tests veröffentlichen:**
```python
import workbench
workbench.publish("GC Drive 09:30 F2", trades_df, why="...", n_trials=1900,
                  source="Session 25.09.", symbol="GC", micro="MGC")
```
`trades_df` = qbt-Trades; Entry-Uhrzeit nicht ab 09:30? Spalten `entry_time`/`exit_time` mitgeben (Beispiel `_scratch_gc_od/publish_workbench.py`).

**Bekannte Grenzen:** Kursdaten im Chart nur RTH (GC 08:20/08:30-Trades ohne Kerzen). Fehlende Preise werden aus dem Close der Minute geschätzt und markiert. Gate v2 für Session-Tests wird nicht automatisch gerechnet (Ampel dann höchstens gelb mit Hinweis), nur für Developer-Versionen.

### verdict-auditor 25.09.2026 (nach dem Bau) und was daraus wurde

Urteil des Auditors: „fertig“ war voreilig. Umgesetzt, per Kanarien-Test in `lab_selftest.py` abgesichert:
- **OOS-Leck geschlossen:** Patterns laufen immer nur auf IS (auch ohne Filter), Trade-Liste/Equity/NT8-Export mit Filter ohne Einfrieren nur IS.
- **Gate v2 für Filter-Versionen nur auf OOS** (Kandidat und Zwillinge, `OOS_FROM` in der Version), Filter-Trials zählen in Sidak-k (`WB_TRIALS`).
- **Look-ahead gesperrt:** Gap/Bewegung/RVOL bis Entry nur bei Entry ab 09:30 (vorher ist der Tages-Open Zukunft).
- **Einfrieren gedeckelt** (3× je Test) und gezählt, ab 2× gelb („OOS nach Auswahl“). OOS-Mindestzahl (10) geprüft.
- P(Pass) klar als „solo, Min-Size, kein Buch-Urteil“ beschriftet. Parameter ohne `PARAMS` werden abgelehnt statt still ignoriert.

**Offen (sollte/kann, Ticket):** SR_c/SR_b ≥ 1,25 steht in der Lineal-Notiz, fehlt aber in Engine und Workbench. FN-Consistency-Regel in P(Pass). Gate v2 für Session-Tests. Quintil-Kanten nur aus IS.

## Urteil nach dem neuen Lineal (Max, 24.09.2026)

Die Workbench urteilt **nach dem neuen Gate aus [[Testphase Juli-Modus]] Abschnitt 3** („Lineal kalibrieren"), nicht nach dem alten Buch-Marginal-Gate:

- **Stufe 1 Edge-Nachweis:** gepaart gegen ≥ 10 Nulldrift-Zwillinge, ein gepoolter Test je Mechanismus, α aus der Gate-Konfiguration.
- **Stufe 2 Buch-Nutzen:** Δ real ≥ 0 im Punkt. Passquote 36 Monate und ohne Zeitgrenze getrennt (Tempo- vs. Sicherheits-Bein).
- **Vor-Gates neu:** min_trades 30, min_oos_trades 10, kein min_tpy, Beleg t = SR·√Jahre ≥ 2, SR_c/SR_b ≥ 1,25, Erwartungswert ohne Top 5 % Trades > 0.
- **Keine zweite Definition im Frontend:** die Workbench liest die Gate-Parameter aus derselben Konfiguration wie die Engine. Ändert sich α, urteilt die Workbench automatisch mit.
- **Abhängigkeit:** das Lineal ist in der Engine noch nicht umgesetzt (Stand 24.09.), α (0,02 bis 0,05) noch offen.

## Overfit-Ampel (Max: rot, sobald Claude es als overfitted bewerten würde, egal welche Prozentzahl)

Angezeigt wird PBO in %, **die Farbe kommt aber aus Regeln, nicht aus der Zahl:**

- 🔴 **rot**, sobald eines zutrifft: schlägt die Nulldrift-Zwillinge nicht (Stufe 1), PBO ≥ 50 %, OOS-Vorzeichen kippt gegen IS, Erwartungswert ohne die besten 1 % Trades ≤ 0 (Engine-Wert `trim_top_frac`, an den eigenen Beinen kalibriert; 5 % war der Vorschlag), Edge lebt nur in einer Epoche (z.B. nur 2023-26).
- 🟡 **gelb**, sobald eines zutrifft: DSR < 0,95 mit echtem n_trials (inkl. Filter-Klicks), PBO 20 bis 50 %, Beleg t < 2, ein Filter ohne vorab geschriebenes Why.
- 🟢 **grün** nur, wenn nichts davon zutrifft.
- Unter der Ampel steht immer, **welche** Regel gegriffen hat, damit rot nicht nur eine Farbe ist.
- P(Pass)-Zelle färbt sich nach Stufe 2 (Δ Buch ≥ 0 grün, sonst rot), daneben die Passquote je Firma in %.

## Sub-Tab „Tests" (Max, 24.09.2026)

Eigener Sub-Tab neben der Workbench. Jeder Test, den Claude in einer Session rechnet (ein-weg, Juli-Modus, Regime-Tafeln, Paper-Checks), erscheint dort als Karte: Name, Datum, Mini-Equity, Urteil mit Ampel, Stempel. Klick öffnet den Test in der Workbench mit allen Trades. Grund: bisher landen solche Tests nur im Chat, in der Daily Note und in Scratch-Ordnern, Max sieht sie nie als Chart (z.B. die Regime-Filter-Tafeln vom 24.09.).
