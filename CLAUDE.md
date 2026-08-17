# CLAUDE.md – Max' zweites Gehirn

Dies ist der persönliche Wissensspeicher (Obsidian Vault) von **Max**. Diese Datei wird bei jedem Session-Start geladen und ist deine zentrale Anleitung.

---

## 👤 Wer ist der User

- **Name:** Max (Ansprache gerne „Boss").
- **Beruf:** Fachinformatiker für Anwendungsentwicklung (Ausbildung abgeschlossen), Entwickler.
- **Fokus:** Eigene IT-Projekte & Tools bauen + Day Trading (~2 Jahre Erfahrung).
- **Details:** siehe [[Über mich]], [[Tech-Stack]].

---

## 🗣️ Kommunikationsstil (WICHTIG)

Volle Regeln in [[Schreibstil]]. Kurzfassung:

- **Deutsch**, englische Fachbegriffe sind ok.
- **Locker und direkt.** So menschlich wie möglich.
- **Übersichtlich** antworten, gut strukturiert, keine Textwände, aber die wichtigsten Infos vollständig.
- **Mitdenken:** prüfen ob etwas Sinn ergibt, bei Entscheidungen den besten Weg hinterfragen. Nicht nervig alles hinterfragen.
- **No-Gos:** keine Gedankenstriche, keine E-Mail-Logik, keine typische KI-Sprache.
- Max ist Entwickler: Code direkt liefern, keine Grundlagen-Erklärungen nötig.

---

## 🤝 Trust my Work (Regel Max, 15.08.2026)

Wenn etwas gebaut, getestet und für gut befunden wurde, gilt es als **fertig und vertrauenswürdig** — nicht bei jeder Folge-Session oder Folge-Frage erneut in Frage stellen oder nochmal durchtesten.

- **Kein wiederholtes Hinterfragen** von bereits abgeschlossener Arbeit (Code, Backtest-Ergebnis, Entscheidung) ohne konkreten Anlass.
- **Neu testen/prüfen nur wenn Max es explizit sagt** („teste nochmal", „prüf das neu", „bist du sicher?" o.ä.) oder wenn sich die zugrunde liegenden Fakten nachweislich geändert haben (z.B. Engine-Fix, neue Daten, Code-Änderung an der betroffenen Stelle).
- Gilt für alles: Code-Änderungen, Backtest-/Portfolio-Ergebnisse, getroffene Entscheidungen, abgeschlossene Recherchen.
- Das steht nicht im Widerspruch zum „Mitdenken" aus dem Kommunikationsstil: Mitdenken heißt, **bei neuen** Entscheidungen den besten Weg zu hinterfragen — nicht, bereits erledigte Arbeit ohne Grund erneut aufzurollen.

---

## 🗂️ Vault-Struktur

Damit du weißt, wo du suchen und ablegen musst (spart Tokens):

| Ordner         | Inhalt                                                                       |
| -------------- | ---------------------------------------------------------------------------- |
| `Kontext/`     | Alles über Max: [[Über mich]], [[Schreibstil]], [[Tech-Stack]]               |
| `Inbox/`       | Rohe Gedanken & Notizen, unsortiert ([[Brain Dump]])                         |
| `Projekte/`    | Aktive Vorhaben **mit** Ziel/Deadline                                        |
| `Bereiche/`    | Laufende Themen **ohne** Deadline ([[Day Trading]], [[Softwareentwicklung]]) |
| `Ressourcen/`  | Allgemeines Wissen, Doku, Recherche                                          |
| `Daily Notes/` | Logbuch, eine Notiz pro Tag (`YYYY-MM-DD.md`)                                |
| `Archiv/`      | Fertige Projekte & erledigte Aufgaben                                        |
| `Anhänge/`     | Bilder & Dateianhänge                                                        |

---

## 📏 Regeln für den Vault

- **Markdown** nutzen, mit **Wikilinks** `[[...]]` zwischen zusammenhängenden Notizen.
- Neue Infos **am richtigen Ort** ablegen (siehe Tabelle). Im Zweifel kurz fragen.
- **Frontmatter** (Tags, Datum) bei neuen Notizen setzen, bestehendes respektieren.
- Bilder in `Anhänge/` ablegen und per `![[...]]` einbetten.
- Fertige Projekte nach `Archiv/` verschieben.
- Wenn Max sagt „merk dir das", die Info in die passende Datei schreiben (z.B. neue Regel in [[Schreibstil]]).

---

## 💰 Token-Disziplin (Entscheidung 29.07.2026, siehe [[Agent-Architektur Token-Optimierung]])

- **Recherche:** VOR jeder Websuche erst [[Research-Cache]] + Insight-Bank ([[Strategie-Logbuch]]) greppen. Neue externe Claims danach in den Research-Cache eintragen.
- **Discovery-Läufe:** immer Background + danach `python summarize_results.py <results.json>` lesen — NIE das volle Log einlesen. Logs nur per `-Tail` / gezieltem Select-String.
- **Suchen:** spezifische Grep-Muster + `head_limit`/`glob` statt breiter Treffermengen; große Outputs auf Platte lassen und referenzieren.
- **Modell-Leitfaden für Max:** Standard-Modell ist seit 29.07. **sonnet** (Claudian-Settings, vorher Opus = ~5x Limit-Verbrauch!). Routine → sonnet/haiku, Frontier (fable/opus) nur gezielt per `/model` für Architektur-/Strategie-Entscheidungen und finale Reviews, danach zurückwechseln. Pro Themenblock lieber frische Session (Cache warm, Kontext klein) statt Marathon.
- **Claude erinnert Max aktiv**, wenn ein Themenblock abgeschlossen ist und ein Sessionwechsel/Downgrade sinnvoll wäre.
- **Bei JEDER Aufgabe von Max** am Ende der Antwort kurz dazuschreiben: (1) welches Modell dafür am besten passt (sonnet/haiku/opus/fable) und (2) ob vorher ein `/clear` (frische Session) sinnvoll ist oder der aktuelle Kontext weiterverwendet werden kann.

---

## ▶️ Bei Session-Start

1. **Inbox prüfen:** Schau in `Inbox/` (v.a. [[Brain Dump]]) nach neuen Notizen.
2. Wenn etwas drin liegt: kurz zusammenfassen und **anbieten, es einzusortieren** (ins passende Projekt / Bereich / Ressource).
3. **PC-Loops übernehmen (Regel Max, 17.08.2026):** Prüfe `C:\Users\maxlk\Projects\trading-data\engine\.claude_loop_heartbeat.json`. Ist die Datei jünger als 50 Minuten, läuft der Buch-Sync-Watchdog + Discovery-Batch-Loop schon in einer anderen Session — nichts starten, höchstens kurz erwähnen. Fehlt sie oder ist sie älter: diese Session startet den Loop selbst per `/loop` (kombinierter Tick alle ~35 Min: `book_state.json` vs. `portfolio.json` vergleichen und bei Bedarf `funded_finalize.py` nachziehen, plus Discovery-Batch-Kadenz-Check gegen [[Strategie-Logbuch]] und FIREFIGHT-Status) und schreibt bei jedem Tick den aktuellen Zeitstempel in die Heartbeat-Datei. Grund: Max hat oft mehrere Sessions parallel offen, ohne die Sperre würde jede eigene Kopie des Loops starten und sich beim Schreiben von `book_state.json`/`portfolio.json`/`tasks.json` in die Quere kommen (der nicht-versionierte `trading-data`-Ordner verzeiht das nicht, siehe `session-guard`).
4. Erst danach mit der eigentlichen Aufgabe weitermachen.

---

## 🧭 Kontext bei Bedarf

Wenn Max fragt „was steht an?", „wo war ich stehengeblieben?", „gib mir ein Briefing" o.ä.:

1. Lies die **letzten 2-3 Daily Notes** aus `Daily Notes/`.
2. Lies die **aktiven Projekte** aus `Projekte/`.
3. Gib ein kurzes, übersichtliches Briefing: Stand, nächste Schritte, was dringend ist.

---

## ⏹️ Bei Session-Ende

Wenn eine Session endet oder Max darum bittet:

1. **Daily Note** für heute erstellen/ergänzen (`Daily Notes/YYYY-MM-DD.md`) mit kurzer Zusammenfassung: was gemacht, was geschafft.
2. **Neue Erkenntnisse** in die passenden Projekt- oder Bereichs-Dateien schreiben.
3. **Inbox aufräumen**, falls noch nicht geschehen.

---

## 🖥️ Portfolio-Tab immer mitziehen (Regel Max, 10.08.2026)

Sobald sich am Portfolio etwas ändert (neues Bein, Bein raus, andere Parameter, neue Firma/Frac), **im selben Zug den Portfolio-Tab im Strategy Lab aktualisieren** — nicht erst „später".

1. `book_state.json` ist die einzige Quelle der Wahrheit für das Buch **und seit 11.08.2026 auch für Käfig und Betriebspunkt** (Block `plan`: Firma, Target/DD, Cap, Preis pro Eval, Käufe pro Monat, `dd_mode`, und die Konten mit ihrem Cushion-Frac). Vorher standen Käfig und frac hartkodiert in `funded_finalize.py` und liefen still auseinander, sobald sich am Plan etwas änderte.
2. `cd C:\Users\maxlk\Projects\trading-data\engine && python funded_finalize.py` → schreibt `portfolio.json` + Report `PORTFOLIO_optimized` und legt fehlende Bein-Reports automatisch an.
3. Danach prüfen: jedes Bein hat ein `report`-Feld, das auf eine existierende Datei in `reports/` zeigt (sonst 404 beim Klick).
4. `portfolio_tab.py` **nicht** benutzen (veraltet, eingefrorene Juli-Beine, läuft nur noch mit `--force` und fasst `portfolio.json` nicht mehr an).

### Was „Änderung am Portfolio" heißt (Auslöser für Schritt 2)
Nicht nur Beine rein/raus. **Jede** dieser Änderungen zieht denselben Zug nach sich:

| Änderung | Wo eintragen |
|---|---|
| Bein rein/raus, andere Bein-Parameter | `book_state.json` → `legs` |
| Anderer Cushion-Frac / Betriebspunkt | `book_state.json` → `plan.accounts` |
| Andere Kontogröße, andere Firma, anderes Target/DD | `book_state.json` → `plan` (+ `firm`/`target`/`dd`) |
| Andere Kaufpolitik (Evals pro Monat, Preis) | `book_state.json` → `plan.buys_per_month` / `price_per_eval_usd` |
| Umstellung des Bust-Checks (eod ↔ intraday) | `book_state.json` → `plan.dd_mode` |

Danach **immer** `funded_finalize.py` laufen lassen, im selben Zug, nicht „später". Der Portfolio-Tab zeigt dann automatisch: Kaufplan (beide Konten mit Frac, Solo-Quote, Median-Dauer), P(funded) rollend über 1/2/3/6/12 Monate, erwartete Eval-Anzahl und Kosten, sowie die Frontier in **beiden** Bust-Modi (EOD-Kopfzahl + ehrliche Intraday-Zahl nach #077).

**Betriebspunkt seit 16.08.2026 = Min-Size** ([[Strategie-Logbuch]] #106): unter der v2-Zielfunktion (Passquote je Eval / $ pro funded) ist die Passquote streng monoton fallend in der Größe, also 1 Kontrakt je Bein, frac ist ausgereizt und **die Kontogröße ist der Sizing-Hebel** (25k schlechtester Käfig, 50k billigster $/funded, 100k/150k höchste Passquote). Der frühere Paar-Betriebspunkt (#089, „P(funded) pro Zeit") gilt nur noch, wenn Max ausdrücklich wieder auf Tempo optimieren will — dann zuerst klären: einzelnes Konto oder Kauf-Rate?

Die Rechenlogik dafür liegt in `eval_plan.py` (gemeinsame Quelle für `funded_finalize.py` und den Analyse-Lauf `frac_pair_budget.py`) — Änderungen an der Passquoten-Mathematik gehören dorthin, nicht in eine Kopie.

### 📗 Next-Week-Buch = Staging (Regel Max, 17.08.2026)
**Neue Strategien, neue Versionen oder Parameter-Änderungen gehen NIE direkt in `book_state.json`**, sondern immer erst ins Staging-Buch **`book_state_next.json`** („Next Week"). Max testet das Buch eine Woche lang (Sim auf der Box + Backtest-Vergleich), optimiert am Wochenende und lässt es dann weiterlaufen. Ablauf bei jeder Buch-Änderung:

1. Änderung in `book_state_next.json` eintragen (Bein rein/raus, andere Params — gleicher Aufbau wie `book_state.json`, plus Block `next_week` mit `created`, `base_fingerprint`, `changes[]` (date/what/why/ticket) und `note`). Neue Version eines bestehenden Beins bekommt einen **neuen Namen** (z.B. `NQ_LastHour_v3`), damit der Leg-Report frisch erzeugt wird und der Vergleich beide Stände zeigt.
2. `python funded_finalize.py --next` und `python live_finalize.py --next` → schreiben `portfolio_next.json` / `live_portfolio_next.json` + Reports `PORTFOLIO_optimized_next` / `PORTFOLIO_live_next` (gleiche Rechnung wie das aktuelle Buch, nur anderes Buch). Vorher session-guard: zwei parallele Läufe schreiben dieselben JSONs.
3. **Ticket anlegen** in `tasks.json` (Prio gelb, `when` = kommendes Wochenende, `guide` mit Übernehmen/Verwerfen-Schritten) — die Übernahme ins Buch passiert nur über dieses Ticket, nie nebenbei.
4. Portfolio-Tab im Lab: oben Umschalter **📘 Aktuelles Buch / 📗 Next Week / ⚖️ Vergleich**; Eval/Funded/Live gibt es in beiden Büchern. Der Vergleich stellt v2-Passquote je Tier, $/funded, Median, Frontier am Betriebspunkt, Trades/Jahr, Korrelation, RoDD, Sharpe, Beine (in beiden / nur Next / raus) und das Live-Buch nebeneinander, mit Delta und Rausch-Einordnung (≥ 1,5 pp und 2× Seed-Streuung, sonst „neutral").
5. **Übernehmen** (Wochenende, Ticket): `book_state_next.json` → `book_state.json` (Backup vorher), dann `funded_finalize.py` + `live_finalize.py` ohne `--next`, NT8-Deploy, dann `next_week`-Block auf das neue Buch zurücksetzen. **Verwerfen:** `book_state_next.json` wieder auf den Stand von `book_state.json` bringen. Ticket danach löschen.

Der Developer-Tab bleibt der Ort, wo eine Strategie in Versionen entsteht; „ins Buch" heißt seit 17.08. „ins Next-Week-Buch + Ticket".

**Seit 11.08.2026 gibt es zusätzlich ein Live-Buch** (Regel Max: nichts von dem, was je eine Edge zeigte, soll verloren gehen, nur weil es nicht ins Prop-Buch passt). Portfolio-Tab hat jetzt 3 Unter-Reiter: 🎓 Eval / 💰 Funded (beide identisch, `portfolio.json`) / 🚀 Live (`live_portfolio.json`).
- `python live_finalize.py` (Engine-Ordner) = Buch-Beine aus `book_state.json` **plus** die per Hand kuratierten Grade-A-„Bank"-Funde in `LIVE_EXTRA` (Strategien mit robuster OOS-Bestätigung, die der Auto-Fit nur mangels Portfolio-Beitrag/Frequenz fürs Prop-Buch abgelehnt hat — kein Prop-Firma-Limit mehr, also kein Ausschlussgrund).
- Neuer Grade-A-Bank-Fund? → in `LIVE_EXTRA` in `live_finalize.py` eintragen (Params, Familie, Why mit Logbuch-Bezug), dann `python live_finalize.py` laufen lassen. Grade-C/D-Funde bewusst NICHT aufnehmen (ehrliches Backtesting: schwache Qualität bleibt schwach, auch live).
- **Falle, auf die schon einmal reingefallen:** ein alter Report kann durch spätere Engine-Fixes überholt sein, ohne dass ideas.json es merkt (bei RV_leadlag_NQES so passiert — Report vom 31.07. zeigte Grade A, mit dem seit 10.08. gefixten `rv.py` neu gerechnet PF 0.91/tot). `live_finalize.py` rechnet jedes Bein bei jedem Lauf frisch mit dem aktuellen Engine-Code — bei Abweichung vom alten Report-Stand zählt die frische Rechnung, nicht das `.meta.json`.
- Kein Prop-Pass-Frontier und keine Kapital-/Sizing-Kurve im Live-Tab (Kapitalgröße & Risiko/Trade noch nicht festgelegt) — nur die ehrliche kombinierte Backtest-Sicht.

---

## 🛠️ Strategy Developer (neuer Tab im Strategy Lab, seit 14.08.2026)

Max entwickelt hier **interaktiv genau eine Strategie in Versionen** — er sagt im Chat, was gebaut/geändert werden soll, Claude setzt es um. Kein Auto-Discovery, Max' eigene Ideen.

**Trigger-Regel (Max, 14.08.):** Sagt Max **„Developer"** im Zusammenhang mit einer Strategie-Idee („bau im Developer…", „Developer: teste mal…"), heißt das automatisch: dieser Workflow, ohne Rückfrage wohin. Claude legt die Version an, rechnet durch und hält den Tab aktuell — nach JEDER Änderung sofort `developer_run.py` laufen lassen, nie nur die Datei ablegen.

**Dateien (alle in `C:\Users\maxlk\Projects\trading-data\engine\developer\`):**
- `state.json` = aktive Strategie + Versions-Historie + Archiv (Single Source of Truth für den Tab)
- `versions/<slug>__v<N>.py` = eine Datei pro Version. Vertrag: `META` (name, market, family, rules, why) + entweder `PARAMS` (→ `qbt.run_strategy`) oder `def trades()` (qbt-kompatibler DataFrame mit `r_net`; optional `px_in/px_out/tmin_entry/tmin_exit` für exakte Chart-Marker)
- `developer_run.py --version N` = Rechenkern, schreibt `results/<slug>__v<N>.json`

**Workflow wenn Max eine Änderung ansagt:**
1. Neue Versionsdatei anlegen (nie alte überschreiben), in `state.json` an `versions` anhängen (`changelog` = was geändert + warum, `base` = Ausgangsversion), `active_version` hochsetzen.
2. `python developer_run.py` laufen lassen (oder Max drückt „Neu durchrechnen" im Tab — gleicher Effekt, Server startet Subprozess).
3. Neue Strategie statt neuer Version? → aktive nach `archive` in `state.json` schieben (`archived`-Datum setzen), neue `active` anlegen mit v1.

**Was jeder Lauf automatisch rechnet** (ehrliche Basis, Käfig aus `book_state.json`): die **komplette Standard-Validierung wie jeder Lab-Report** — `copilot.full_report_data` + `report.build` erzeugen einen 1:1-Lab-Report nach `developer/reports/<slug>__v<N>.html` (Route `/devreports/`), der im Tab eingebettet wird (Regel Max 14.08.: Ansicht identisch zu den normalen Reports, inkl. Equity, MC-Charts, KPI-Kästen, Prop-Tabellen, Heatmap). Dazu Developer-spezifisch: OOS-Kontrolle (letzte 30 %), Solo-Frontier (EOD + Intraday #077), Kaufplan-Sicht (#089), **Prop-Firm-Check** (E8-Regeln aus AP90), **⭐ Buch-Beitrag** (P(funded) Buch heute vs. Buch + Strategie — das Entscheidungskriterium) und Preis-Chart mit Trade-Markern. Buch-Beine sind gecacht in `developer/book_cells.json`, Key = Hash der legs aus `book_state.json` (invalidiert sich selbst). Sagt Max nach der Entwicklung „ins Buch": normaler Weg über `book_state.json` → `funded_finalize.py` (Portfolio-Tab-Regel gilt).

**Rollback:** Max klickt im Tab auf eine ältere Version (aktiviert + rechnet sie), oder sagt es im Chat. Versionen sind append-only.

### 💬 Chat im Developer (Max, 15.08.2026)
Rechte Spalte im Developer-Tab: Max redet dort direkt mit Claude über die Anthropic-API, Claude legt Versionen an, rechnet durch und beantwortet die Buch-Frage. **Das ist ein zweiter Claude, nicht die laufende Claude-Code-Session** — gleiche Tools und gleicher Kontext, aber eigener Verlauf.

- Tool-Schicht + Chat-Runner: `dev_agent.py` (14 Tools: `dev_status`, `list_strategies`, `read_version`, `write_version`, `new_strategy`, `select_strategy`, `run_version`, `get_result`, `compare_versions`, `set_goal`, `save_report`, `read_book_state`, `search_engine`, `read_engine_file`).
- **Bewusst EINE Tool-Schicht:** ein späterer MCP-Server importiert dieselben Funktionen, statt sie zu kopieren. Neue Developer-Fähigkeit → als Tool in `dev_agent.py`, nicht als Sonderweg im Server.
- **Schlüssel:** `ANTHROPIC_API_KEY` oder Datei `engine/.anthropic_key`. Abrechnung läuft über die API, **getrennt vom Claude-Code-Abo** (AP95). Modell/Effort in `developer/agent_config.json`, Standard `claude-opus-5` / `high`.
- **Report speichern nur auf Ansage:** Developer-Läufe bleiben unter `developer/reports/`. Erst wenn Max „Report speichern" sagt, kopiert `save_report` HTML + `meta.json` nach `reports/` und der Report taucht in der Lab-Seitenleiste auf.
- **Strategie wechseln:** „ich will die und die Strategie bearbeiten" → `select_strategy(slug)` holt sie aus dem Archiv zurück, die bisher aktive wandert hinein.
- Chat läuft job-basiert (senden → ID → pollen), damit ein 15-Minuten-Backtest sichtbar läuft und nie in einen Browser-Timeout rennt. Verlauf in `developer/chat.json`.

### 📊 Charts im Developer = Charts im Lab-Report (Max, 15.08.2026)
Equity-Kurve und Monte Carlo im Developer-Tab sind **1:1 dieselbe Darstellung wie in den Lab-Reports**: gleiche Chart.js-Defaults (Mono-Schrift, Achse `#78776f`, Grid `rgba(255,255,255,.05)`), gleiche Kartenhöhen (Equity und Fächer 580 px, Histogramme 300 px), gleiche Farben und Linienstärken. Die Werte sind aus `report.py` kopiert — **ändert sich dort etwas, muss es in der `HUB`-Sektion von `app_server.py` mitgezogen werden**, sonst driften Report und Developer optisch auseinander.

Dazu Developer-spezifisch: OOS-Fenster in der Equity blau hinterlegt, Perzentil-Kegel und Preis-Chart mit Trade-Markern. Die Chart-Rohdaten sind groß und laufen deshalb über `/api/dev/charts` statt über den 4-Sekunden-Poll.

**Ganz oben im Tab** steht immer die eine Frage in Klartext: verbessert sie das Buch, ja oder nein — plus eine Warum-Zeile, die das Delta gegen das MC-Rauschen einordnet.

**Ziel-Banner (Max, 14.08., oberster Punkt im Tab):** `state.json` hat ein Feld `goal` (`book` | `solo`), im Tab oben umschaltbar. `book` = Entscheidung „✓/✗ ins Buch" (verbessert es P(funded) des aktuellen Buchs — Deltas 3m/6m, Median, Kosten), `solo` = „käfigtauglich ja/nein" (≥60 % in ≤50 Tagen, Intraday). Der volle Lab-Report wird NICHT mehr eingebettet (Max' Wunsch), sondern ist als Link „voller Lab-Report ↗" am Regelwerk erreichbar (Route `/devreports/`, liefert auch `chart.min.js` aus `reports/` mit — sonst bleiben die Report-Charts leer).

**Buch-Beitrag ist rauschbewusst (seit 14.08., Vorfall NQ-ORB-Breakout-Demo):** ein einzelner MC-Lauf (4000 Sims) schwankt beim Delta locker ±1-2pp allein durchs Sampling — ein Bein mit eindeutig negativer Edge zeigte auf einen Blick "+1,4pp verbessert das Buch". `book_contribution()` in `developer_run.py` rechnet deshalb über **5 unabhängige Seeds**, nimmt die Streuung als Rauschmaß und verlangt vom Delta mindestens das Doppelte davon (min. ±1,5pp), sonst "neutral" statt "besser/schlechter". Gilt bei jeder künftigen Änderung an der Buch-Beitrags-Logik: nie ein einzelner Seed als Entscheidungsgrundlage.

**Falle bei `mode="orb"` (Strategie-Logbuch #066/#067):** der Default `orb_exec="book"` hat Look-ahead (Volumen-/VWAP-Filter werten die komplette Ausbruchs-Bar aus, der Fill ist aber schon vorher). Jede Developer-Version mit ORB-Modus braucht **explizit** `orb_exec="close"` (echte Live-Logik) oder `"stop_honest"` (Level-Fill via ruhende Order) — sonst zeigt die Strategie eine Schein-Edge, die live nicht existiert.

---

## 🧮 Quant-Team: Mathematiker + Statistiker (Regel Max, 16.08.2026)

Zwei Subagents in `.claude/agents/`, die sich **automatisch und ohne Rückfrage** einschalten, sobald es um neues Alpha oder darum geht, es für die Eval zu optimieren:

| Agent | Zuständig für |
|---|---|
| `quant-mathematician` | Struktur & Formeln: First-Passage/Gambler's Ruin unter Trailing-DD (EOD + Intraday), Sizing-Frontier als Optimierungsproblem (Frac-Paar #089), Kelly unter Ruin-Constraint, Optimal Stopping, OU/Halbwertszeit, Kointegration, Kosten-Schwelle. Liefert geschlossene/semi-analytische Lösung + numerischen Check + Patch-Vorschlag für `eval_plan.py`/Engine. |
| `quant-statistician` | Beweislage & Unsicherheit: CIs (Block-Bootstrap), DSR/PSR/PBO/Purged-CV aus `overfit.py`, `n_trials`, Shrinkage der In-Sample-Edge, Power/Stichprobengröße, Regime-Splits, Tail-Konzentration, MC-Seed-Rauschen, Korrelation der Buch-Beine → geschrumpfte Edge → P(funded) mit Fehlerbalken. |

**Auslöser (jeder davon reicht):** [[Alpha-Suche]]-Arbeit, Discovery-Lauf auswerten, neue Developer-Version bewerten, Buch-Beitrag/„ins Buch?", Frac-/Sizing-/Betriebspunkt-Frage, Parameter-Wahl, Käfig- oder Firmen-Vergleich, Paper-/Idee-Prüfung (`paper-edge`).

**So laufen sie:** beide **parallel im Background** starten (ein Agent-Aufruf mit beiden), Ergebnisse zusammenführen, dann erst antworten. Aufgabenteilung: Mathematiker = „wie sieht das Problem aus, was ist optimal", Statistiker = „wie viel Beweis ist da, wie groß ist die Edge wirklich". `strategy-auditor` bleibt der qualitative Gegenleser (Look-ahead, Why, Anatomie) und kommt dazu, bevor etwas auf eine Eval geht. `backtest-runner` startet die großen Läufe; die Quant-Agents rechnen nur nach und ändern keine Engine-Dateien.

Beide laufen auf `opus` (Formeln/Statistik lohnen das Modell; Max kann die `model:`-Zeile in der Agent-Datei jederzeit auf `sonnet` setzen). Der Developer-Chat (`dev_agent.py`) ist ein zweiter Claude und kann diese Agents **nicht** aufrufen — dort gilt weiter die eingebaute Standard-Validierung; die Quant-Sicht holt Max über die Claude-Code-Session.

---

## 🖥️ Box-Fernzugriff (Regel Max, 11.08.2026 — WICHTIG, nie wieder vergessen)

**Claude hat vollen SSH-Zugriff auf die Trading-Box und soll ihn immer selbst nutzen, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.**

- Zugang: `ssh Administrator@100.127.89.9` (Tailscale, Key liegt lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, Zeitzone deutsche Zeit.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1` auf der Box (NT8 beenden → Backup außerhalb des NT8-Baums → Staging rein → Pre-Flight-Compile → `dotnet build` → DLL setzen → `obj`/`bin` wieder entfernen). Details und bekannte Fallen: [[VPS-Einrichtung Schritt für Schritt]], [[Strategie-Logbuch]] #084.
- Vor jedem Deploy: NT8-Log des Tages checken ob wirklich nichts Live läuft, danach den kompletten Zielzustand in einem Wegwerf-Ordner vorab kompilieren (`_check_compile.ps1 -SrcDir`), bevor NT8 überhaupt gestoppt wird. Das Leichen-Problem im `_staging` ist seit 11.08. (AP84) im Skript selbst entschärft: `box_deploy.ps1` sagt vor allem anderen die Deploy-Kandidaten an, warnt bei Dateien die es in `Strategies` noch nicht gibt (neues Bein oder Leiche?) und leert das Staging nach erfolgreichem Lauf. Die Ansage trotzdem immer lesen, bevor NT8 gestoppt wird.
- **Wiederanlauf braucht aktuell eine angemeldete RDP-Session** (Autologon fehlt noch, AP86) — NT8 hängt sonst beim UI-Aufbau. Bis das gefixt ist, nach jedem Deploy kurz Bescheid geben, dass eine RDP-Anmeldung nötig ist.
- **Lab-Server ist seit 15.08.2026 multi-threaded** (`ThreadingTCPServer` in `app_server.py`). Vorher blockierte ein laufender Backtest oder Chat jede andere Anfrage und die Oberfläche wirkte tot. Port ist per `MAXLAB_PORT` überschreibbar — wichtig zum Testen, weil Windows sonst eine zweite Instanz still auf denselben Port lässt und man gegen den alten Prozess testet.
- Ticket-Tracker liegt in `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (Feld `ap_id` = die AP-Nummern, die Max nennt — bei unklaren AP-Nummern immer erst dort nachschauen statt zu raten).
- **Geplant (Max, 11.08.26):** ein zentraler „Deployer" — eine Oberfläche/Skript, in dem Max nur noch die gewünschten Strategien + Parameter einträgt und der Rest (Staging, Pre-Flight, Build, Deploy, Restart) automatisch läuft. Noch nicht gebaut, aber das Zielbild für den Deploy-Workflow — künftige Deploy-Arbeit sollte darauf einzahlen statt Einzelskripte zu vermehren.

---

## 🖥️ Hub — Max' Desktop-Cockpit (Regel Max, 19.08.2026 — WICHTIG)

Eigene Desktop-App (`C:\Users\maxlk\Projects\hub\`, gebaut als `dist\Hub\Hub.exe`), Discord-artiges Layout mit frei verschieb-/größenbaren Fenstern (Channels+Agents, Vault-Graph „My Brain", Strategy Lab, Gmail, …). **Das wird Max' Hauptarbeitsweg** — der Ort, über den er künftig alles bündelt, nicht nur ein Nebenprojekt.

**Trigger-Regel:** Sagt Max sinngemäß **„Baue im Hub …"** / **„im Hub …"** im Zusammenhang mit einer UI-Änderung oder einem neuen Feature, heißt das automatisch: Projekt ist `C:\Users\maxlk\Projects\hub\`, ohne Rückfrage wohin. Gilt **session-übergreifend** — unabhängig davon, welche Session den Hub zuletzt bearbeitet hat, sofort dort direkt weitermachen (Dateien lesen reicht, kein Nachfragen nötig).

**Nur gezielt ändern:** exakt das umsetzen, was Max ansagt — nicht nebenbei andere Teile der UI mitanfassen, aufräumen oder „verbessern", die er nicht angesprochen hat.

**Hub bleibt offen, nie für Kleinkram neu starten (Regel Max, 19.08.):** Für Änderungen an einzelnen Sub-Apps — Strategy-Lab-Server neu starten, Gmail-Snapshot aktualisieren — **niemals** `Hub.exe` selbst neu starten, sondern nur den betroffenen Prozess bzw. die betroffene Datei anfassen. `static/`, `hub_config.json` und Laufzeitdaten wie `gmail_cache.json` liegen bewusst NEBEN der exe (nicht im PyInstaller-Bundle) und werden vom Server live gelesen (`/api/apps` ohne Cache).

**UI-/Config-Änderung (JS/CSS/HTML/`hub_config.json`):** Datei in `static/` bzw. `hub_config.json` bearbeiten, dann `.\hot_reload.ps1` laufen lassen (synct nach `dist\Hub` per robocopy, triggert `/api/reload` → offenes Fenster macht `location.reload()`, Python-Prozess läuft durch). **Kein Rebuild, kein Neustart, kein Flackern der ganzen App.**

**Rebuild + Neustart NUR bei echter Code-Änderung** an `hub_app.py`/`hub_server.py` selbst (Server-Logik, neue Endpunkte, Fenster-Verhalten): `.\build_exe.ps1`, dann `Hub.exe` neu starten.

---

## 🎯 Aktueller Fokus

- **Trading-Pipeline: Eval → Funded → Live.** Einstieg immer über [[Day Trading]].
- **Aktuelle Phase: [[Eval-Passing]]** (Prop-Eval bestehen, **E8**, nicht Apex — Sim-Eval am 03.08.26 bestanden, echte Eval noch nicht gekauft). Optimiert wird NUR auf hohe Passchance in kurzer Zeit, nicht auf Funded/Payouts.
- **Plattform: NinjaTrader 8 / NinjaScript (C#)** auf Tradovate, nicht MultiCharts/PowerLanguage (siehe [[Tech-Stack]]).
- Nächster Schwerpunkt: **[[Alpha-Suche]]** (First-Passage-Sizing + Cross-Asset-Signale).
- Werkzeuge: [[Backtest-Engine]], [[Portfolio-Simulator]], [[Strategie-Logbuch]].

### 🧭 Stehende Trading-Prinzipien (für JEDE künftige Strategie)
- **⭐ DAS einzige Entscheidungskriterium (Max, 10.08.26, präzisiert 16.08.26 / Logbuch #106):** Bei JEDER Empfehlung/Entscheidung (Bein rein/raus, Parameter, Firma, Kontogröße, Sizing) zuerst fragen: **verbessert oder verschlechtert es die Passquote je Eval bzw. die Kosten pro funded Konto (Preis ÷ Passquote)?** Nicht Einzel-Edge, nicht Sharpe, nicht Eleganz, und **nicht mehr „P(funded) pro Zeit"** — der Zeit-Score belohnt Größe und Nachkauf-Lotterie (Nulldrift-Test: 88 % davon entstehen bei Edge 0). Zeit läuft nur als Kontext mit. Die Rechnung muss auf der ehrlichen Basis stehen: aktuelles Buch, gefixte Engine, **Intraday-Bust-Check** (#077), **Min-Size 1 Kontrakt je Bein**, **Block-Bootstrap** (Vola-Clustering), Nulldrift-Kontrolle und Letzte-3-Jahre-Spalte daneben; bei Bein-Selektion **nested OOS / Marginal-Test „Buch + 1, nur OOS"**. Positive Edge ist notwendig, nicht hinreichend (Präzedenz: OR_DELTA_BIAS #079; bei Min-Size ist „Bein dazu" = „mehr Position", Lehre 82). Kernrechnung: `eval_plan.evaluate_v2` / `cage_policy_lib.evaluate_v2`, Tiers in `cage_v2_tiers.json`.
- **Simplex beats Komplex:** immer so einfach wie möglich starten. Komplexität nur mit OOS-Beweis + Why, sonst raus (mehr Regeln = fragiler). Siehe [[Simplex beats Komplex]].
- **Jede Strategie = vollständiges Skript:** Entry + Stop + Take-Profit + Notausgang(Zeit) + Sizing + **WHY**. Siehe [[Strategie-Anatomie (Framework)]].
- **Jede Strategie gehört in genau eine der 5 [[Strategie-Familien]]:** Trend Following · Mean Reversion · Intraday Bias · Swing · Relative Value.
- **Ehrliches Backtesting Pflicht:** Real-Fills, OOS-Split, Kosten. Kein Fit ohne kausales Why.

---

## 🚦 Parallele Sessions: session-guard (Regel Max, 16.08.2026)

Max fährt regelmäßig mehrere Claude-Sessions gleichzeitig, die alle auf denselben Engine-Ordner schreiben. Der Subagent `session-guard` prüft, ob sich dabei zwei Sessions gegenseitig überschreiben — Rechenkern ist `.claude/scripts/session_conflicts.py` (liest die Session-Transkripte aus `~/.claude/projects`, nie selbst einlesen, die sind mehrere MB groß).

**Einschalten:** wenn Max fragt „überschreibe ich gerade was?" / „läuft noch eine andere Session?", wenn eine Änderung unerklärlich weg ist, und **von selbst**, bevor eine größere Änderung an einer der Sammel-Dateien ansteht (`app_server.py`, `developer_run.py`, `report.py`, `book_state.json`, `portfolio.json`, `developer/state.json`).

**Zwei harte Fakten dazu:**
- `C:\Users\maxlk\Projects\trading-data` ist **kein Git-Repo**. Genau dort passieren die Kollisionen, und dort gibt es keinen `git checkout` als Rettung — ein Überschreiber ist endgültig. Der Vault selbst ist versioniert.
- Claude Codes `file-history` wird seit ~15.08. nicht mehr befüllt, taugt also nicht als Netz. `session_conflicts.py --recover <datei>` durchsucht sie trotzdem, falls für den Einzelfall doch etwas da ist.

**Die eigentliche Gefahr sind nicht die Edits**, sondern parallele Bash-Schreiber: zwei gleichzeitige `funded_finalize.py`- oder `developer_run.py`-Läufe schreiben dieselben JSONs ohne Sperre. Vor jedem solchen Lauf gilt: erst schauen, ob eine andere Session gerade dasselbe tut.

---

*Dieses System ist bewusst einfach gehalten und darf mit der Zeit wachsen. Max kann Claude jederzeit sagen: „merk dir das in deiner CLAUDE.md", um Verhalten anzupassen.*
