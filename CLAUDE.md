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
3. Erst danach mit der eigentlichen Aufgabe weitermachen.

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

**Betriebspunkt ist ein PAAR, kein einzelner frac** ([[Strategie-Logbuch]] #089): Wer rollend nachkauft, optimiert nicht die Einzel-Passquote, sondern P(funded) pro Zeit. Fragt Max nach „dem besten frac", immer zuerst klären: ein einzelnes Konto oder eine Kauf-Rate? Die Antwort ist in beiden Fällen eine andere.

Die Rechenlogik dafür liegt in `eval_plan.py` (gemeinsame Quelle für `funded_finalize.py` und den Analyse-Lauf `frac_pair_budget.py`) — Änderungen an der Passquoten-Mathematik gehören dorthin, nicht in eine Kopie.

**Seit 11.08.2026 gibt es zusätzlich ein Live-Buch** (Regel Max: nichts von dem, was je eine Edge zeigte, soll verloren gehen, nur weil es nicht ins Prop-Buch passt). Portfolio-Tab hat jetzt 3 Unter-Reiter: 🎓 Eval / 💰 Funded (beide identisch, `portfolio.json`) / 🚀 Live (`live_portfolio.json`).
- `python live_finalize.py` (Engine-Ordner) = Buch-Beine aus `book_state.json` **plus** die per Hand kuratierten Grade-A-„Bank"-Funde in `LIVE_EXTRA` (Strategien mit robuster OOS-Bestätigung, die der Auto-Fit nur mangels Portfolio-Beitrag/Frequenz fürs Prop-Buch abgelehnt hat — kein Prop-Firma-Limit mehr, also kein Ausschlussgrund).
- Neuer Grade-A-Bank-Fund? → in `LIVE_EXTRA` in `live_finalize.py` eintragen (Params, Familie, Why mit Logbuch-Bezug), dann `python live_finalize.py` laufen lassen. Grade-C/D-Funde bewusst NICHT aufnehmen (ehrliches Backtesting: schwache Qualität bleibt schwach, auch live).
- **Falle, auf die schon einmal reingefallen:** ein alter Report kann durch spätere Engine-Fixes überholt sein, ohne dass ideas.json es merkt (bei RV_leadlag_NQES so passiert — Report vom 31.07. zeigte Grade A, mit dem seit 10.08. gefixten `rv.py` neu gerechnet PF 0.91/tot). `live_finalize.py` rechnet jedes Bein bei jedem Lauf frisch mit dem aktuellen Engine-Code — bei Abweichung vom alten Report-Stand zählt die frische Rechnung, nicht das `.meta.json`.
- Kein Prop-Pass-Frontier und keine Kapital-/Sizing-Kurve im Live-Tab (Kapitalgröße & Risiko/Trade noch nicht festgelegt) — nur die ehrliche kombinierte Backtest-Sicht.

---

## 🖥️ Box-Fernzugriff (Regel Max, 11.08.2026 — WICHTIG, nie wieder vergessen)

**Claude hat vollen SSH-Zugriff auf die Trading-Box und soll ihn immer selbst nutzen, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.**

- Zugang: `ssh Administrator@100.127.89.9` (Tailscale, Key liegt lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, Zeitzone deutsche Zeit.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1` auf der Box (NT8 beenden → Backup außerhalb des NT8-Baums → Staging rein → Pre-Flight-Compile → `dotnet build` → DLL setzen → `obj`/`bin` wieder entfernen). Details und bekannte Fallen: [[VPS-Einrichtung Schritt für Schritt]], [[Strategie-Logbuch]] #084.
- Vor jedem Deploy: NT8-Log des Tages checken ob wirklich nichts Live läuft, danach den kompletten Zielzustand in einem Wegwerf-Ordner vorab kompilieren (`_check_compile.ps1 -SrcDir`), bevor NT8 überhaupt gestoppt wird. Das Leichen-Problem im `_staging` ist seit 11.08. (AP84) im Skript selbst entschärft: `box_deploy.ps1` sagt vor allem anderen die Deploy-Kandidaten an, warnt bei Dateien die es in `Strategies` noch nicht gibt (neues Bein oder Leiche?) und leert das Staging nach erfolgreichem Lauf. Die Ansage trotzdem immer lesen, bevor NT8 gestoppt wird.
- **Wiederanlauf braucht aktuell eine angemeldete RDP-Session** (Autologon fehlt noch, AP86) — NT8 hängt sonst beim UI-Aufbau. Bis das gefixt ist, nach jedem Deploy kurz Bescheid geben, dass eine RDP-Anmeldung nötig ist.
- Ticket-Tracker liegt in `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (Feld `ap_id` = die AP-Nummern, die Max nennt — bei unklaren AP-Nummern immer erst dort nachschauen statt zu raten).
- **Geplant (Max, 11.08.26):** ein zentraler „Deployer" — eine Oberfläche/Skript, in dem Max nur noch die gewünschten Strategien + Parameter einträgt und der Rest (Staging, Pre-Flight, Build, Deploy, Restart) automatisch läuft. Noch nicht gebaut, aber das Zielbild für den Deploy-Workflow — künftige Deploy-Arbeit sollte darauf einzahlen statt Einzelskripte zu vermehren.

---

## 🎯 Aktueller Fokus

- **Trading-Pipeline: Eval → Funded → Live.** Einstieg immer über [[Day Trading]].
- **Aktuelle Phase: [[Eval-Passing]]** (Prop-Eval bestehen, **E8**, nicht Apex — Sim-Eval am 03.08.26 bestanden, echte Eval noch nicht gekauft). Optimiert wird NUR auf hohe Passchance in kurzer Zeit, nicht auf Funded/Payouts.
- **Plattform: NinjaTrader 8 / NinjaScript (C#)** auf Tradovate, nicht MultiCharts/PowerLanguage (siehe [[Tech-Stack]]).
- Nächster Schwerpunkt: **[[Alpha-Suche]]** (First-Passage-Sizing + Cross-Asset-Signale).
- Werkzeuge: [[Backtest-Engine]], [[Portfolio-Simulator]], [[Strategie-Logbuch]].

### 🧭 Stehende Trading-Prinzipien (für JEDE künftige Strategie)
- **⭐ DAS einzige Entscheidungskriterium (Max, 10.08.26):** Bei JEDER Empfehlung/Entscheidung (Bein rein/raus, Parameter, Firma, Sizing) zuerst fragen: **verbessert oder verschlechtert es die Wahrscheinlichkeit auf einen funded Account (Passquoten-Frontier)?** Nicht Einzel-Edge, nicht Sharpe, nicht Eleganz. Die Rechnung muss auf der ehrlichen aktuellen Basis stehen: aktuelles Buch, gefixte Engine, **Intraday-Bust-Check** (#077 — E8 prüft kontinuierlich). Positive Edge ist notwendig, nicht hinreichend (Präzedenz: OR_DELTA_BIAS #079).
- **Simplex beats Komplex:** immer so einfach wie möglich starten. Komplexität nur mit OOS-Beweis + Why, sonst raus (mehr Regeln = fragiler). Siehe [[Simplex beats Komplex]].
- **Jede Strategie = vollständiges Skript:** Entry + Stop + Take-Profit + Notausgang(Zeit) + Sizing + **WHY**. Siehe [[Strategie-Anatomie (Framework)]].
- **Jede Strategie gehört in genau eine der 5 [[Strategie-Familien]]:** Trend Following · Mean Reversion · Intraday Bias · Swing · Relative Value.
- **Ehrliches Backtesting Pflicht:** Real-Fills, OOS-Split, Kosten. Kein Fit ohne kausales Why.

---

*Dieses System ist bewusst einfach gehalten und darf mit der Zeit wachsen. Max kann Claude jederzeit sagen: „merk dir das in deiner CLAUDE.md", um Verhalten anzupassen.*
