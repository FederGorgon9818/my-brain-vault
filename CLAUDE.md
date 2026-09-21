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

## ❓ Offene Fragen zuerst (Regel Max, 27.08.2026 — verschärft 30.08.2026)

**Immer zuerst fragen, wenn etwas unklar ist — bevor irgendetwas umgesetzt, geändert oder losgerechnet wird.** Das ist keine Kann-Regel, sondern die Standard-Reihenfolge: erst klären, dann handeln. Nicht raten, nicht die wahrscheinlichste Interpretation annehmen und einfach loslegen.

**Wann das gilt:** Ziel unklar, mehrere sinnvolle Wege möglich, Scope nicht eindeutig, Formulierung mehrdeutig, oder eine Änderung greift in etwas Bestehendes ein (Buch, Code, Datei, Regel) ohne dass klar ist, was genau gewünscht ist. Im Zweifel gilt: lieber einmal zu oft nachfragen als eine Annahme treffen, die falsch sein könnte.

**Ausnahme:** nur triviale, eindeutige Aufträge ohne Interpretationsspielraum brauchen keine Rückfrage (z.B. „lies Datei X", „was steht in Y").

Max hat mehrfach angemerkt, zu oft nicht gefragt worden zu sein, bevor etwas geändert wurde. Ab jetzt: **im Zweifelsfall immer fragen**, auch wenn es nach der zweiten Nachfrage in Folge aussieht.

---

## 🤝 Trust my Work (Regel Max, 15.08.2026)

Wenn etwas gebaut, getestet und für gut befunden wurde, gilt es als **fertig und vertrauenswürdig** — nicht bei jeder Folge-Session oder Folge-Frage erneut in Frage stellen oder nochmal durchtesten.

- **Kein wiederholtes Hinterfragen** von bereits abgeschlossener Arbeit (Code, Backtest-Ergebnis, Entscheidung) ohne konkreten Anlass.
- **Neu testen/prüfen nur wenn Max es explizit sagt** („teste nochmal", „prüf das neu", „bist du sicher?" o.ä.) oder wenn sich die zugrunde liegenden Fakten nachweislich geändert haben (z.B. Engine-Fix, neue Daten, Code-Änderung an der betroffenen Stelle).
- Gilt für alles: Code-Änderungen, Backtest-/Portfolio-Ergebnisse, getroffene Entscheidungen, abgeschlossene Recherchen.
- Kein Widerspruch zum „Mitdenken" aus dem Kommunikationsstil: Mitdenken heißt, **bei neuen** Entscheidungen den besten Weg zu hinterfragen — nicht, bereits erledigte Arbeit ohne Grund erneut aufzurollen.

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
- **Daily-Note-Bestätigung (Regel Max, 09.09.2026):** wenn in der Antwort etwas angepasst/geändert wurde (Datei, Code, Regel, Entscheidung — nicht bei reinen Frage-Antwort-Antworten ohne Änderung), am Ende genauso kurz dazuschreiben, ob und was in die heutige Daily Note nachgetragen wurde. Ergänzt den Daily-Note-Pflicht-Hook (`on_stop.py`, siehe [[Hooks-Referenz]]): der Hook blockt erst beim Session-Ende, diese Zeile gibt die Bestätigung direkt in der Antwort.
- **MCP-Tools/Connectors kosten Kontext, auch wenn sie nicht gebraucht werden** (Fund 17.09.2026: ein einzelner ungenutzter Connector mit vielen Tools kann zweistellig Prozent vom Startkontext ziehen, sobald er geladen wird). Passt ein verbundener MCP-Server nicht zu Max' aktueller Firma/Setup, aktiv drauf hinweisen statt ihn stillschweigend mitzuschleppen.

---

## ▶️ Bei Session-Start

1. **Inbox prüfen:** Schau in `Inbox/` (v.a. [[Brain Dump]]) nach neuen Notizen. Liegt was drin: kurz zusammenfassen und **anbieten, es einzusortieren**.
2. **PC-Loops übernehmen (Regel Max, 17.08.2026):** Prüfe `C:\Users\maxlk\Projects\trading-data\engine\.claude_loop_heartbeat.json`. Jünger als 50 Minuten → läuft schon in einer anderen Session, nichts starten. Fehlt sie oder ist sie älter → diese Session startet den Buch-Sync-Watchdog + Discovery-Batch-Loop selbst per `/loop` (~35 Min Tick: `book_state.json` vs. `portfolio.json`, `funded_finalize.py` bei Bedarf, Discovery-Kadenz-Check) und schreibt den Zeitstempel bei jedem Tick zurück. Grund: mehrere Parallel-Sessions ohne diese Sperre würden sich beim Schreiben von `book_state.json`/`portfolio.json`/`tasks.json` in die Quere kommen (`trading-data` ist nicht versioniert, siehe `session-guard`).
3. **Discovery-Inbox lesen (Regel Max, 18.08.2026):** `cd C:\Users\maxlk\Projects\trading-data\engine && python discovery/inbox_tool.py --pull` (Stand von der Box, dort läuft der Runner dauerhaft). Kandidaten mit „besser"/„vs Original besser": Quant-Team + `strategy-auditor` drüberschauen lassen, dann Next-Week-Buch + Ticket, danach `inbox_tool.py --seen-all`. Steht der Runner (Heartbeat > 30 min) und die Queue hat `pending`-Jobs: per SSH `engine\discovery\start_runner.ps1` (NSSM-Dienst `MaxLabDiscovery` seit 16.09.2026, nie zusätzlich per WMI starten, AP179). Details [[Discovery-Runner v2]].
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

Sobald sich am Portfolio etwas ändert (neues Bein, Bein raus, andere Parameter, neue Firma/Frac, andere Kontogröße, anderer Betriebspunkt, andere Kaufpolitik, anderer Bust-Check-Modus), **im selben Zug**: `book_state.json` anpassen (einzige Quelle der Wahrheit für Buch + Käfig + Betriebspunkt) → `python funded_finalize.py` (Engine-Ordner) → **im selben Zug `python discovery/inbox_tool.py --push-next`**. `portfolio_tab.py` nicht mehr benutzen (veraltet).

Neue Strategien/Versionen/Parameter-Änderungen gehen NIE direkt in `book_state.json`, sondern erst ins Staging-Buch `book_state_next.json` (Next-Week-Buch) + Ticket; Übernahme ist eine Wochenend-Entscheidung. Seit 11.08.2026 gibt es zusätzlich ein Live-Buch (`live_finalize.py`, `LIVE_EXTRA`), damit keine Edge verloren geht, die es nicht ins Prop-Buch schafft.

**Voller Ablauf, Next-Week-Buch, Live-Buch, Edge-Health-Monitor: [[Buch-Workflow]].** Vorfall, warum `--push-next` nie ausgelassen werden darf: [[Strategie-Logbuch]] #126 (Box rechnete drei Tage gegen ein altes Buch).

---

## 🛠️ Strategy Developer (Tab im Strategy Lab, seit 14.08.2026)

**Trigger-Regel:** Sagt Max **„Developer"** im Zusammenhang mit einer Strategie-Idee, heißt das automatisch: dieser Workflow, ohne Rückfrage. Nach JEDER Änderung sofort `developer_run.py` laufen lassen, nie nur die Datei ablegen. Rechnet automatisch die komplette Standard-Validierung plus Buch-Beitrag (⭐ das Entscheidungskriterium, rauschbewusst über 5 Seeds).

**Falle:** `mode="orb"` braucht explizit `orb_exec="close"` oder `"stop_honest"`, sonst Look-ahead ([[Strategie-Logbuch]] #066/#067).

Voller Ablauf (Dateien, Chat mit zweitem Claude, Charts, Ziel-Banner): [[Strategy Developer]].

---

## 🤖 Discovery-Runner v2 (Regel Max, 18.08.2026)

**Rechnen macht die Maschine, entscheiden macht Claude.** Alpha-Suche läuft als Dauerprozess auf der Box (Queue → Prämisse → Grid+Gates → Buch-Marginal → Inbox). Volle Doku, Betrieb, Varianten-Vorlagen: [[Discovery-Runner v2]].

- **Neue Suchidee = Job in der Queue** (Job-JSON mit Why vorab → `inbox_tool.py --add-job`), kein neues Einzelskript. Der genaue Ablauf je Hypothese steht als „Der EINE Weg" in [[Discovery-Runner v2]] (4 Schritte: Why → mind. 10 Varianten via `variant-scout` → Gate-Batterie `GATES_HARD`/`controls.py` → Rechnen auf der Box).
- **⭐ Neue Edge → NIE ins Live-Buch, IMMER sofort ins Next-Week-Buch.** `promote_next.py` macht das automatisch alle 30 Min auf der Box, nur für `deploy_ready`-Kandidaten. `book_state.json` (Live) wird davon nie angefasst.
- **PC darf aus sein**, Runner + Auto-Promotion laufen komplett auf der Box. Manuelle Änderung am Next-Buch am PC → sofort `--push-next`, sonst promotet die Box in einen alten Stand.
- **Register ist Pflicht**, jeder Trial zählt gegen die Zufallsdecke. Externe Sweeps tragen per `registry_pending_add`-Weg nach ([[Discovery-Runner v2]]), nie `registry.json` direkt anfassen.
- **⭐ Die Queue darf nie leerlaufen.** `job_generator.py` füllt selbst nach (Folge-Jobs, Abdeckungs-Vorlagen, Varianten-Vorlagen). Schreibt der Runner `queue_empty`, ist die Vorlagen-Welt ausgereizt → `alpha-scout` einschalten, neue Mechanismen liefern, nicht mehr Grid.
- **Nie** `runner.log` oder volle `results/*.json` einlesen — `inbox_tool.py`/`summarize_results.py` reichen.
- **⭐ Claude reiht neue Funde selbst ein**, ohne dass Max es ansagen muss, sobald Dry-Run + `pipeline-auditor` durch sind. Nach jeder Engine-/`job_generator.py`-Änderung: Runner neu starten (Stop → Sync → Start), sonst läuft er mit altem Code weiter (Vorfall 28.08.2026: 5,5 h Leerlauf).

---

## 🧮 Quant-Team: Mathematiker + Statistiker (Regel Max, 16.08.2026)

Zwei Subagents, die sich **automatisch und ohne Rückfrage** einschalten, sobald es um neues Alpha oder Eval-Optimierung geht:

| Agent | Zuständig für |
|---|---|
| `quant-mathematician` | Struktur & Formeln: First-Passage/Gambler's Ruin, Sizing-Frontier, Kelly, Optimal Stopping, OU/Halbwertszeit, Kointegration, Kosten-Schwelle. Liefert Lösung + numerischen Check + Patch-Vorschlag. |
| `quant-statistician` | Beweislage & Unsicherheit: CIs (Block-Bootstrap), DSR/PSR/PBO/Purged-CV, `n_trials`, Shrinkage, Power, Regime-Splits, Tail-Konzentration, MC-Seed-Rauschen, Korrelation der Buch-Beine → P(funded) mit Fehlerbalken. |

**Auslöser:** [[Alpha-Suche]]-Arbeit, Discovery-Lauf auswerten, neue Developer-Version bewerten, Buch-Beitrag/„ins Buch?", Frac-/Sizing-/Betriebspunkt-Frage, Käfig-/Firmen-Vergleich, Paper-Prüfung.

**Wie:** beide **parallel im Background**, Ergebnisse zusammenführen, dann erst antworten. `strategy-auditor` bleibt der qualitative Gegenleser (Look-ahead, Why, Anatomie) und kommt vor jeder Eval dazu; `backtest-runner` startet die großen Läufe; die Quant-Agents rechnen nur nach und ändern keine Engine-Dateien. Beide laufen auf `opus` (lohnt sich für Formeln/Statistik). Der Developer-Chat (`dev_agent.py`, zweiter Claude) kann diese Agents nicht aufrufen.

---

## 🕵️ Weitere Meta-Agents

Jeder Subagent trägt seine eigene Einschalt-Regel in `.claude/agents/*.md` (Feld `description`) **und** in `.claude/hooks/agent_triggers.py` — der Prompt-Hook (`on_prompt.py`) erinnert live beim Tippen, der Stop-Hook (`on_stop.py`) lässt eine Session einmal nicht enden, wenn ein Trigger gefeuert hat und der Agent nie lief. Das ist die durchgesetzte Quelle, nicht diese Datei — neuer Agent → Zeile in `agent_triggers.py`, nicht nur Prosa hier. Details, Vorfallgeschichte, Audit-Skript: [[Hooks-Referenz]].

Kurzer Kompass, welcher Agent wofür (volle Trigger stehen in der jeweiligen `description`):

| Agent | Kernfrage | Modell |
|---|---|---|
| `pipeline-auditor` | Rechnen/messen/entscheiden wir methodisch sauber? | sonnet |
| `verdict-auditor` | Trägt die Beweislage den Stempel „tot/gut/fertig"? | opus |
| `strategy-auditor` | Adversarialer Gegenleser vor Eval-Deploy / Batch-Story-Check | opus |
| `variant-scout` | Wie viele ECHTE Testarten hat diese Hypothese? | sonnet |
| `familien-scout` | Konzept in Preis-Wege zerlegen, Stand je Weg, Karte + Skelette | opus |
| `alpha-scout` | Was testen wir als Nächstes, wenn die Queue leerläuft? | sonnet |
| `logbook-distiller` | Ist die Lehre schon ein Code-Gate oder nur Text? | sonnet |
| `retro-agent` | Wo wurde Zeit/Tokens verbrannt, was ändern? (So 12:00) | sonnet |
| `engine-regression-tester` | Golden-Master vor jedem Box-Sync | sonnet |
| `design-guard` | Sieht das neue UI-Element aus wie der Rest der App? | sonnet |
| `box-ops` / `live-reconciler` | Läuft die Box? / Passt Live zu Backtest? | haiku / sonnet |
| `session-guard` | Überschreiben sich zwei Parallel-Sessions? | haiku |

`familien-scout` (Konzept → Preis-Wege, Workflow `konzept-weg`) und der Workflow `ein-weg` (Schritt 2 des EINEN Wegs als Skript): Details in [[Hooks-Referenz]] und [[Familien-Scout Agent]].

---

## 🪝 Hooks: Reflex-Regeln laufen im Harness, nicht im Kopf (Max, 04.09.2026)

Seit 04.09.2026 setzt Claude Code Regeln deterministisch per Hook durch (`.claude/settings.json`, Skripte in `.claude/hooks/`, Marker in `<engine>/.claude_hooks/`, nicht versioniert). Volle Tabelle, Vorfallgeschichten (UTF-8-Fix, Cross-Session-Überblick), Audit-Skript: **[[Hooks-Referenz]]**.

Kurzfassung, was blockt statt nur erinnert:
- `guard_bash.py`/`guard_read.py`: kein Box-Sync ohne frischen `regression_ok`-Marker, kein `--enqueue` ohne `pipeline_ok`-Marker, keine Dauerläufer als Session-Kind, kein volles Log-/Transkript-Einlesen.
- `guard_write.py` (Regel 21.09.2026, Fund: Momentum&Averages- und PCA-Bank blieben sonst wochenlang ohne Gegenleser): keine neue Zeile in einer Hypothesen-Bank, solange `variant-scout` + `strategy-auditor` nicht in derselben Session gelaufen sind (am einfachsten über Skill/Workflow `ein-weg`). Reine Status-/Formatierungs-Edits lösen nichts aus; Fehlalarm-Override `python .claude/hooks/mark.py hypothese_ok`.
- `on_stop.py`: Session endet nicht, solange `book_state*.json` neuer als der letzte `--push-next` ist, oder solange eigene Datei-Änderungen ohne Daily-Note-Eintrag im Raum stehen.
- **Ein Hook blockiert nie die Arbeit, weil er selbst kaputt ist** — Fehler werden verschluckt und geloggt, nie geworfen.
- Neue Reflex-Regel geplant? Zuerst fragen, ob sie als Hook abbildbar ist (Dateipfad, Kommando-Muster, Dateizeit), statt sie nur als Text hier abzulegen.

---

## 🧩 Plugins & neue Werkzeuge immer mitnutzen (Regel Max, 16.09.2026)

Installiert ist nicht genug: sobald eines davon passt, **von selbst** einsetzen, ohne dass Max danach fragt. Passt es bewusst nicht, in einem Halbsatz sagen warum.

| Werkzeug | Einsetzen, wenn … |
|---|---|
| **pyright-lsp** (Plugin, `LSP`-Tool) | Python-Code in Engine/Hub/Hooks gelesen oder geändert wird: Definition/Referenzen/Aufrufer per LSP statt breitem Grep, nach jeder Änderung Diagnosen prüfen (fehlende Imports wegen `sys.path` sind bekannt und kein Befund). |
| **claude-md-management** → `claude-md-improver` | CLAUDE.md wird größer umgebaut oder auditiert, oder ein Abschnitt ist offensichtlich veraltet. |
| **claude-md-management** → `revise-claude-md` | am Session-Ende (`/abschluss`), wenn die Session eine neue dauerhafte Regel oder Lehre ergeben hat, bevor sie von Hand in die CLAUDE.md geschrieben wird. |
| **claude-code-setup** → `claude-automation-recommender` | ein neuer Hook, Skill, Agent, Workflow oder MCP-Server geplant wird, und bei Retro-Vorschlägen des `retro-agent`. |
| **`engine/overfit_crosscheck.py`** (pypbo-Gegenprobe) | nach jeder Änderung an `overfit.py` (zusätzlich zum `engine-regression-tester`), und wenn ein PBO/DSR-Urteil angezweifelt wird. Bekannte Abweichung: PBO-Median-Konvention bei ungeradem N (AP179). |
| **`engine/.venv-analysis`** (pyfolio-reloaded, pypbo; pandas 2.3.3) | Risiko-Tearsheets für ein Bein oder das Buch als Zusatzsicht zu den Lab-Reports. **Nie** ins System-Python installieren (würde pandas 3 des Runners downgraden); Daten im System-Python erzeugen, als Datei übergeben, in der venv auswerten. |
| **NSSM-Dienst `MaxLabDiscovery`** (Box) | jeder Runner-Stopp/-Start: STOP-Datei bzw. `engine\discovery\start_runner.ps1`, nie WMI daneben. Neue Dauerläufer (Hub/Lab am PC) ebenfalls als NSSM-Dienst statt WMI-Job-Escape planen (AP179). |

---

## 🖥️ Box-Fernzugriff (Regel Max, 11.08.2026 — WICHTIG, nie wieder vergessen)

**Claude hat vollen SSH-Zugriff auf die Trading-Box und soll ihn immer selbst nutzen, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.**

- Zugang: `ssh Administrator@100.127.89.9` (Tailscale, Key lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, deutsche Zeitzone.
- **Laptop ist seit 03.09.2026 zweites, dauerhaftes Arbeitsgerät** — gleicher Weg wie vom PC: Vault per Git-Remote, Engine-/Box-Arbeit per SSH mit demselben Key. Kein eigener Discovery-Fallback und kein Hub/Lab-Server am Laptop, die Box bleibt die gemeinsame Instanz.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1` (NT8 beenden → Backup → Staging → Pre-Flight-Compile → `dotnet build` → DLL setzen → aufräumen). Details/Fallen: [[VPS-Einrichtung Schritt für Schritt]], [[Strategie-Logbuch]] #084.
- Vor jedem Deploy: NT8-Log des Tages checken, danach `_check_compile.ps1 -SrcDir` in einem Wegwerf-Ordner, bevor NT8 überhaupt gestoppt wird. `box_deploy.ps1` sagt die Deploy-Kandidaten vorab an und warnt bei unbekannten Dateien (neues Bein oder Leiche?) — die Ansage immer lesen.
- **Wiederanlauf braucht aktuell eine angemeldete RDP-Session** (Autologon fehlt noch, AP86) — nach jedem Deploy kurz Bescheid geben.
- **Lab-Server ist multi-threaded** (`ThreadingTCPServer`). Port per `MAXLAB_PORT` überschreibbar — wichtig zum Testen, sonst läuft eine zweite Instanz still auf demselben Port.
- **Ticket-Tracker** liegt in `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (Feld `ap_id`). **Seit 06.09.2026 zweiseitig:** Max legt Tickets auch direkt auf der Box an, `tasks.json` wird bei jedem `inbox_tool.py --pull` mitgezogen und mit `--push-tasks` zurückgeschrieben, **die Box ist die Quelle der Wahrheit**. Der Abgleich überschreibt nie blind (`.bak`, Nummernkollision wird gemeldet statt aufgelöst). **Vor dem Anlegen eines neuen Tickets also immer erst `--pull`** (Vorfall 03.-06.09.: Nummernkollision AP121-127, siehe [[Strategie-Logbuch]]).
- **Geplant:** ein zentraler „Deployer", der Staging/Pre-Flight/Build/Deploy/Restart automatisch macht. Noch nicht gebaut, aber das Zielbild — künftige Deploy-Arbeit sollte darauf einzahlen.

### 🔔 RiskGuard neu anlegen → Telegram nicht vergessen (Regel Max, 20.08.2026)

`MaxRiskGuard` startet mit leeren `TelegramToken`/`TelegramChatId`-Feldern und schweigt dann bei JEDER Meldung, ohne Fehler oder Log-Eintrag. Ist schon mal wochenlang unbemerkt so gelaufen (Kontowechsel 18.08.2026).

- **Immer wenn Max ansagt, dass RiskGuard entfernt/neu hinzugefügt/eine neue Strategie-Instanz angelegt wird** (oder nach Box-Reboot/Kontowechsel): aktiv daran erinnern, `TelegramToken` + `TelegramChatId` neu einzutragen.
- Echte Werte liegen NICHT im Vault, sondern auf der Box in `C:\Users\Administrator\maxlab_watchdog.json` (Bot **maxbot** @maxbotalgobot). Beim Erinnern die Werte per SSH holen und direkt mit ausgeben.

---

## 🖥️ Hub — Max' Desktop-Cockpit (Regel Max, 19.08.2026 — WICHTIG)

Eigene Desktop-App (`C:\Users\maxlk\Projects\hub\`, `dist\Hub\Hub.exe`), Discord-artiges Layout mit frei verschieb-/größenbaren Fenstern. **Das ist Max' Hauptarbeitsweg.**

**Trigger-Regel:** Sagt Max **„Baue im Hub …"** im Zusammenhang mit einer UI-Änderung, heißt das automatisch: Projekt ist `C:\Users\maxlk\Projects\hub\`, ohne Rückfrage. Session-übergreifend, sofort dort weitermachen.

**Nur gezielt ändern:** exakt das umsetzen, was Max ansagt — nicht nebenbei andere Teile der UI mitanfassen.

**Hub bleibt offen, nie für Kleinkram neu starten:** Änderung an einer Sub-App (Lab-Server, Gmail-Snapshot) → nur den betroffenen Prozess/die Datei anfassen, niemals `Hub.exe` neu starten. UI-/Config-Änderung (`static/`, `hub_config.json`) → Datei bearbeiten, dann `.\hot_reload.ps1` (kein Rebuild). Rebuild + Neustart NUR bei Code-Änderung an `hub_app.py`/`hub_server.py` selbst (`.\build_exe.ps1`).

**Alles, was wir bauen, zieht automatisch in den Hub nach:** neuer Subagent oder neue Automatisierung → sofort **ohne Rückfrage** in `hub_config.json` eintragen (`mock_agents`/`mock_loops`: Name, Rolle, Modell-Tier, Zustand), danach `.\hot_reload.ps1`. `hub_config.json` ist die lebende Quelle für das komplette Agent-/Automatik-Roster — hier keine Doppel-Tabelle, im Zweifel dort nachsehen bzw. dort pflegen. **Modell-Änderungen an fünf Agents (17.09.2026: `alpha-scout`, `pipeline-auditor`, `logbook-distiller`, `retro-agent`, `variant-scout` opus→sonnet) sind in `hub_config.json` noch nachzuziehen, sobald PC/Laptop erreichbar sind.**

---

## 🚫 Dauerläufer NIE als Kind einer Claude-Session starten (Regel Max, 18.08.2026 — hart)

Claude Desktop läuft in einem Job Object. **Jeder Prozess, der aus einer Claude-Session heraus gestartet wird, vererbt diesen Job an seine Kinder.** Solange einer darin lebt, hält er das Claude-Paket für Windows „in Benutzung" — Claude lässt sich dann nicht mehr öffnen oder schließt sich sofort wieder (Fehler `0x80070020`).

**Betrifft alles, was Claude überlebt:** Hub, Lab-Server, NT8-Deploy-Helfer, dauerhafte `ssh`-Verbindungen, Discovery-/Backtest-Läufe im Hintergrund.

**Richtig starten:**
```powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"<exe>" <args>'; CurrentDirectory = '<ordner>' }
```
Aus Python: `job_escape.spawn([...])` aus `C:\Users\maxlk\Projects\hub\job_escape.py`. Kurzläufer (Backtest im Vordergrund, Grep, Build) sind egal, die sterben mit der Session.

Der Hub schützt sich seit 18.08. selbst (Env-Marker `CLAUDECODE` → job-freier Neustart per WMI). Klemmt es trotzdem: `C:\Users\maxlk\Projects\hub\tools\Claude entsperren.cmd` außerhalb von Claude doppelklicken, oder `python tools/claude_unlock.py` aus einer laufenden Session.

---

## 🎯 Aktueller Fokus

- **Trading-Pipeline: Eval → Funded → Live.** Einstieg immer über [[Day Trading]].
- **Aktuelle Phase: [[Eval-Passing]]** (Prop-Eval bestehen, **E8**, nicht Apex). **⭐ Die erste ECHTE E8 50k Eval läuft live** (Konto `E61803453048`, handelt unbeaufsichtigt von der Box), dazu FN1/FN2 (FundedNext Flex 50k).
- **⭐ ZIEL seit 18.09.2026 (Max, präzisiert 21.09.): 50.000 $ Eigenkapital aus gebündelten Prop-Payouts, um ein eigenes Live-Konto (am liebsten 100k) zu eröffnen.** Zielfunktion ist **E[Zeit bis Zielkapital]** (Netto-Payouts minus alle Eval-Käufe), nicht mehr die Passquote je Eval. Die Funded-Phase zählt mit. Laufende Konten laufen weiter, Frage ist nur, was dazukommt. Rechnung: `engine/tempo_plan.py` (Bestandskonten, Kaufpolitiken, Haushaltsgrenzen, Regime-Spalten). Stand 21.09.: Empfehlung E8 150k k3 + FN 150k k3, Deckel 2.500 $ Netto-Auslage, Entscheidung offen in Ticket AP204. Details [[Daily Notes/2026-09-18]], [[Daily Notes/2026-09-21]].
- **Plattform: NinjaTrader 8 / NinjaScript (C#)** auf Tradovate, nicht MultiCharts/PowerLanguage (siehe [[Tech-Stack]]).
- Nächster Schwerpunkt: **[[Alpha-Suche]]** (First-Passage-Sizing + Cross-Asset-Signale).
- Werkzeuge: [[Backtest-Engine]], [[Portfolio-Simulator]], [[Strategie-Logbuch]].

### 🧭 Stehende Trading-Prinzipien (für JEDE künftige Strategie)

- **⭐ DAS einzige Entscheidungskriterium (Max, 10.08.26, präzisiert 16.08.26 / Logbuch #106, Zieländerung 18.09.26):** Bei JEDER Empfehlung/Entscheidung (Bein rein/raus, Parameter, Firma, Kontogröße, Sizing) zuerst fragen: **verkürzt oder verlängert es die Zeit bis 50.000 $ Eigenkapital aus Payouts, bei begrenzter Auslage?** Nicht Einzel-Edge, nicht Sharpe, nicht Eleganz. Passquote je Eval und Kosten pro funded Konto bleiben Zwischengrößen, nicht das Ziel. Die #106-Warnung gilt weiter als Pflichtkontrolle: ein Zeit-Score belohnt Größe und Nachkauf-Lotterie (Nulldrift-Test: 88 % davon entstanden bei Edge 0), deshalb IMMER mit Nulldrift-Zwilling rechnen (unter Edge 0 muss jede Politik 0 % Erreichung zeigen) und die Auslage p90 mitnennen. Min-Size (1 Kontrakt je Bein) ist als Betriebspunkt nicht mehr gesetzt, Größe wird gerechnet. Rechnung auf ehrlicher Basis: aktuelles Buch, gefixte Engine, Intraday-Bust-Check (#077), Block-Bootstrap, Nulldrift-Kontrolle, Letzte-3-Jahre-Spalte plus geschrumpfte Spalte (Shrinkage 0,58); bei Bein-Selektion nested OOS/Marginal-Test „Buch + 1, nur OOS". Positive Edge ist notwendig, nicht hinreichend (Lehre 82). Kernrechnung: `tempo_plan.py` (Zeit bis Ziel), `eval_plan.evaluate_v2` / `cage_policy_lib.evaluate_v2` (Käfig je Konto), Tiers in `cage_v2_tiers.json`.
- **⭐ Buch-Lücke immer mitnennen (Regel Max, 21.08.2026):** Sobald über eine Strategie/Variante/einen Discovery-Kandidaten gesprochen wird, IMMER dazusagen, **was konkret noch fehlt, damit sie ins Buch kommt** — entlang der Stufen: Prämisse → Survivors/Gates → PBO sauber → über Zufallsdecke → Buch-Marginal „besser" → Next-Week-Buch + Ticket → Wochenend-Review → NT8-Deploy. Nicht nur „0 Kandidaten" melden, sondern die Stufe benennen, an der es hängt.
- **Simplex beats Komplex:** immer so einfach wie möglich starten. Komplexität nur mit OOS-Beweis + Why, sonst raus. Siehe [[Simplex beats Komplex]].
- **Jede Strategie = vollständiges Skript:** Entry + Stop + Take-Profit + Notausgang(Zeit) + Sizing + **WHY**. Siehe [[Strategie-Anatomie (Framework)]].
- **Jede Strategie gehört in genau eine der 5 [[Strategie-Familien]]:** Trend Following · Mean Reversion · Intraday Bias · Swing · Relative Value.
- **Ehrliches Backtesting Pflicht:** Real-Fills, OOS-Split, Kosten. Kein Fit ohne kausales Why.

---

## 🚦 Parallele Sessions: session-guard (Regel Max, 16.08.2026)

Max fährt regelmäßig mehrere Claude-Sessions gleichzeitig, die alle auf denselben Engine-Ordner schreiben. Der Subagent `session-guard` prüft, ob sich dabei zwei Sessions gegenseitig überschreiben (`.claude/scripts/session_conflicts.py`, liest Session-Transkripte, nie selbst einlesen — mehrere MB groß).

**Einschalten:** wenn Max fragt „überschreibe ich gerade was?" / „läuft noch eine andere Session?", wenn eine Änderung unerklärlich weg ist, und **von selbst**, bevor eine größere Änderung an einer geteilten Datei ansteht (`app_server.py`, `developer_run.py`, `report.py`, `book_state.json`, `portfolio.json`, `developer/state.json`).

**Zwei harte Fakten:**
- `C:\Users\maxlk\Projects\trading-data` ist **kein Git-Repo**. Ein Überschreiber ist dort endgültig. Der Vault selbst ist versioniert.
- Claude Codes `file-history` wird seit ~15.08. nicht mehr befüllt. `session_conflicts.py --recover <datei>` durchsucht sie trotzdem, falls doch was da ist.

**Die eigentliche Gefahr sind nicht die Edits**, sondern parallele Bash-Schreiber: zwei gleichzeitige `funded_finalize.py`- oder `developer_run.py`-Läufe schreiben dieselben JSONs ohne Sperre. Vor jedem solchen Lauf: erst schauen, ob eine andere Session gerade dasselbe tut.

---

*Dieses System ist bewusst einfach gehalten und darf mit der Zeit wachsen. Max kann Claude jederzeit sagen: „merk dir das in deiner CLAUDE.md", um Verhalten anzupassen.*
