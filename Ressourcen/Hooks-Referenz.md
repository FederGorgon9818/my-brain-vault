---
tags:
  - ressource/tooling
erstellt: 2026-09-17
---
# 🪝 Hooks-Referenz — Reflex-Regeln im Harness

⬅️ [[Agent-Architektur Token-Optimierung]] · [[Agent-Nutzungs-Audit 2026-09-11]]

Seit 04.09.2026 setzt Claude Code selbst einige der „Claude muss dran denken"-Regeln durch — deterministisch, per Hook in `.claude/settings.json` (versioniert, gilt auf PC und Laptop), Skripte in `.claude/hooks/`, Marker-Dateien in `<engine>/.claude_hooks/` (nicht versioniert). Anlass: die Agentic-OS-Recherche vom 04.09. (Guardrails gehören in den Harness) plus die Vorfälle 21.08. (Buch drei Tage ungepusht) und 28.08. (Runner 5,5 h mit altem Code). Kurzfassung + wichtigste Hooks stehen in der CLAUDE.md, hier die volle Tabelle + Vorfallgeschichten.

## Die Hooks

| Hook | Was er tut |
|---|---|
| `guard_bash.py` (PreToolUse Bash) | **Blockt** `box_provision_discovery.ps1 -Sync*`, solange kein `regression_ok`-Marker jünger als die Engine-Kern-Dateien ist (engine-regression-tester setzt ihn bei „Sync frei"). **Blockt** `hypothesis_bank.py --enqueue`, solange kein `pipeline_ok`-Marker jünger als `hypothesis_bank.py` ist (pipeline-auditor setzt ihn bei „sauber"). **Blockt** Dauerläufer als Session-Kind (Hub.exe, app_server/lab_app/hub_app/discovery_runner, Start-Process, start_discovery.ps1) ohne `Invoke-CimMethod`/`job_escape`. **Blockt** volles Einlesen von `runner.log`, `results/*.json`, Session-Transkripten. Merkt sich `--push-next` und `funded_finalize`-Läufe als Marker. |
| `guard_read.py` (PreToolUse Read) | Dieselbe Lese-Sperre für das Read-Tool. |
| `guard_write.py` (PreToolUse Edit/Write/MultiEdit, seit 21.09.2026) | **Blockt** eine neue Hypothese, solange `variant-scout` UND `strategy-auditor` nicht in derselben Session gelaufen sind (Scan über `agent_usage_audit.used_agent_names`, zählt auch die Workflows `ein-weg`/`konzept-weg`) — geprüft an ZWEI Stellen: neue ID-Tabellenzeile in `Hypothesen-Bank (*).md` **und** neuer `H("ID-XX", ...)`-Aufruf in `discovery/hypothesis_bank.py` selbst (Nachtrag noch am Bautag: `logbook-distiller` fand, dass die erste Fassung nur die `.md` deckte, die eigentliche Bank aber monatelang direkt im Code wuchs, siehe #166). Reine Status-/Ergebnis-/Formatierungs-Edits an Bestehendem lösen nichts aus. Unlock bei Fehlalarm: `python .claude/hooks/mark.py hypothese_ok` (gilt nur bis zum nächsten echten Edit an der Datei, gleiches Muster wie `regression_ok`). Anlass: Audit 21.09.2026 fand zwei Bänke (Momentum & Averages, PCA & Faktorstruktur), die trotz der `on_stop.py`-Erinnerung wochenlang ohne die beiden Agents blieben — eine reine Text-Erinnerung reicht bei viel Parallelarbeit nicht. **Bekannte Restlücke** (logbook-distiller 21.09.2026, noch nicht gebaut): `mark.py hypothese_ok` ist ein reines Selbstattest ohne Rückprüfung; und `_nm_clone_all()` in `hypothesis_bank.py` klont jede nicht explizit in `NM_EXCLUDE` stehende Zeile automatisch auf bis zu 6 Zusatzmärkte — ein Engine-seitiges `audited`-Pflichtfeld (Default `False`, Klon nur wenn `True`) würde die Default-Richtung umdrehen, ist aber Aufgabe der Hauptsession/`pipeline-auditor`, kein Claude-Hook (der Klon läuft beim Python-Import auf der Box, nicht als Tool-Aufruf einer Session). |
| `after_change.py` (PostToolUse Edit/Write/Bash) | Sagt die Folgepflicht an: `book_state*.json` neuer als letzter Push → finalize + push-next; Engine-Kern → Regressionstest vor Sync; Discovery-Code → Runner-Neustart; Hypothesen-Bank → variant-scout/strategy-auditor/pipeline-auditor; Hub/Lab/Report-Oberfläche → design-guard; neuer Agent/Automatik → Hub-Roster; Logbuch → logbook-distiller; neue `.cs`-Strategie → `NS_MAP`. |
| `on_stop.py` (Stop) | **Lässt die Session nicht enden**, solange `book_state*.json` neuer ist als der letzte `--push-next` (einmal blocken, dann nur noch erinnern). Unlock: `python .claude/hooks/mark.py push_next_at`. Seit 09.09.2026 zusätzlich: **lässt die Session nicht enden**, wenn sie selbst Dateien geändert hat, aber die heutige Daily Note seit Session-Start nicht angefasst wurde — gilt geräteübergreifend, auch ohne Engine-Ordner. Erkennung über das eigene Transkript, reine Lese-Sessions triggern nichts. |
| `on_prompt.py` (UserPromptSubmit, seit 11.09.2026, umgebaut 21.09.2026) | **Typ-Router zuerst:** legt die Quittung für die Session an und fordert den Auftrags-Typ an (`receipt.py --sid <id> --type <typ>`), inklusive Regex-**Vorschlägen** — die Entscheidung fällt bewusst nicht per Regex, weil Max oft diktiert und kein Muster dann sauber trifft. Danach als zweite Spur der alte **Agent-Reflex** gegen `agent_triggers.py`. Keine Sperre, nur Kontext — gesperrt wird in `guard_chain.py`. |
| `on_stop.py`, Teil 5 (Stop, seit 25.09.2026) | **Test nicht in der Workbench?** Hat die Session ein Skript aus einem `_scratch*`-Ordner gerechnet und nie `workbench.publish(...)` aufgerufen, endet sie einmal nicht. Anlass: Max sah von Session-Tests nur Zahlen im Chat, nie die Trades ([[Strategy Lab Workbench]]). Ausweg bei reinen Tafeln ohne Trades: `python .claude/hooks/mark.py tests_ok`. |
| `on_stop.py`, Teil 3 (Stop, seit 11.09.2026) | **Agent vergessen?** Scannt das eigene Transkript mit denselben Regeln (Prompt, geänderte Dateien, Bash-Kommandos, direkte WebSearch/WebFetch) und lässt die Session einmal nicht enden, wenn ein Trigger gefeuert hat, der Agent aber nie lief. Ausweg: einschalten, oder in einem Satz sagen, warum er hier nicht passt, dann erneut beenden. Achtung Fehlalarme: die Regex matcht auf reinen Text (auch zitierte Tool-Ausgaben wie `/context`-Listen oder Skill-Namen in einer Tabelle), nicht auf Bedeutung — ein Treffer heißt nicht automatisch, dass der Agent wirklich passt. |
| `guard_chain.py` (PreToolUse Edit/Write/MultiEdit/Bash/WebSearch/WebFetch, seit 21.09.2026) | **Die harte Hälfte des Auftrags-Typ-Routers** ([[Arbeits-Workflow (Auftrags-Typen)]]). Zwei Wege: **(A) Aktions-Gates**, unabhängig von der Quittung, dort wo die Aktion ihren Typ selbst verrät — `WebSearch`/`WebFetch` ohne `research-scout`, Hub-/Lab-/Report-Datei ohne `design-guard`, **neuer** Logbuch-Eintrag ohne `logbook-distiller` (Tippfehler-Korrektur nicht), `book_state*.json` ohne Quant-Team + `strategy-auditor`. **(B) Quittungs-Gate**: trägt die Quittung einen Typ mit Kette (`urteil`, `buch`, `rechnen`, …) und ist die Kette offen, sind schreibende Aktionen gesperrt. Frei bleiben immer Daily Notes, `.claude/**`, `tasks.json`, Scratchpad — sonst sperrt der Prozess sich selbst aus. Blockt **nie** ohne Transkript (`used is None` → durchlassen). `research-scout`/`alpha-scout`/`claude-code-guide` dürfen als Subagent selbst ins Web, Workflow-Agents zählen als gelaufen (seit 28.09.2026, Abschnitt „Subagents und Workflows" unten). Override mit Begründungspflicht: `receipt.py --sid <id> --skip <schritt> --why "..."`. Zwei Verfeinerungen aus dem Eigentest am Bautag: `hub_config.json` löst nur bei Layout-/App-Schlüsseln aus, nicht bei Roster-Pflege (`mock_agents`/`mock_loops`); `hot_reload.ps1`/`build_exe.ps1` blocken nur, wenn **diese** Session selbst eine UI-Datei angefasst hat (fängt zugleich den Umgehungsweg „UI-Datei per `sed` ändern" ab, den das Datei-Gate nicht sieht). |
| `receipt.py` + `work_types.py` (CLI + Daten, seit 21.09.2026) | Die **Prozess-Quittung** je Session: welcher Auftrags-Typ, welche Pflichtkette, was lief, was wurde mit Grund ausgelassen. Eine Datei je Session (parallel-sicher, Max fährt 5+ gleichzeitig), Kurz-ID steht in jeder Hook-Meldung. Verfällt nach 12 h. `work_types.py` ist die **Quelle der Wahrheit** für die 14 Typen und ihre Ketten — nicht die CLAUDE.md, nicht `kette.js` (das spiegelt sie nur, `test_chain.py` prüft die Deckung). |
| `session_start.py` (SessionStart) | Inbox-Inhalt + Stale-State (ungepushtes Buch, Kern ohne Regressions-OK) direkt in den Kontext. Seit 09.09.2026 zusätzlich ein Vault-Kurzbriefing (letzte 2 Daily Notes, aktive Projekte, neuester Logbuch-Eintrag) und ein Cross-Session-Überblick (letzte 5 auf diesem Gerät aktive Sessions). |

## Cross-Session-Überblick + Daily-Note-Pflicht (Regel Max, 09.09.2026)

Max' Wunsch: jede Session weiß grob, was in parallelen Chats lief, und durch konsequente Daily-Note-Pflege ist „Kontextverlust quasi nicht möglich". Zwei Teile, weil sie unterschiedliche Garantien geben:

1. **Cross-Session-Überblick** (`session_start.py`, `recent_local_sessions()` in `_common.py`): scannt beim Start die Transkripte unter `~/.claude/projects/*/*.jsonl` projektübergreifend, zeigt die 5 zuletzt aktiven anderen Sessions mit Titel/letztem Prompt. **Grenze: nur dasselbe Gerät** — eine Box-Session sieht keine Laptop-Sessions und umgekehrt. Für „was lief auf einem anderen Gerät" bleibt `session-guard` (prüft Datei-Kollisionen, nicht Inhalt) bzw. die Daily Note die Quelle.
2. **Daily-Note-Pflicht** (`on_stop.py`): DIE geräteübergreifende Garantie, weil die Daily Note git-synchronisiert ist. Blockt nach demselben Muster wie der Buch-Push (einmal blocken, dann nur erinnern), nur wenn die Session selbst etwas geändert hat — reine Frage-Antwort-Sessions werden nie unterbrochen.

**Nebenfund beim Bauen:** `.claude/scripts/session_conflicts.py` (nutzt `session-guard`) hatte einen Filter-Bug, der Titel/letzten-Prompt-Zeilen nie erreichte — jeder Report zeigte seitdem „(ohne Titel)". Mitgefixt, plus denselben UTF-8-Fix wie unten (das Skript importiert `_common.py` nicht, hat also einen eigenen Encoding-Block).

## UTF-8-Fix 09.09.2026 — Kontext war teilweise wirklich nicht da

`_common.py` erzwingt seit 09.09. `sys.stdin`/`stdout`/`stderr` fest auf UTF-8. Vorher lief Python auf dem PC/der Box unter der Windows-Konsolen-Codepage (`cp1252`) — jeder Umlaut, Gedankenstrich oder jedes Emoji in einem Hook-Payload (ständig im Vault: Daily Notes, Inbox, Logbuch, auch Bash-Kommandos mit deutschen Kommentaren) hat zwei Sachen ausgelöst:

1. Beim Schreiben wurde die stdout-JSON ungültig, der `additionalContext` ging ganz oder teilweise verloren.
2. Beim Lesen scheiterte `read_input()` am Decodieren, der Fehler wurde still abgefangen und lieferte `{}` zurück — **damit griff keiner der Wächter** (Box-Sync-Block, Dauerläufer-Block, Log-Read-Block, Enqueue-Block), ohne dass irgendwo ein Fehler sichtbar wurde. War nie im `hook_errors.log`, weil kein Absturz, nur ein leises `{}`.

Betraf alle Hooks gleichermaßen (alle importieren `_common`). Reproduziert und mit Vorher/Nachher-Test verifiziert: derselbe `cat runner.log`-Befehl mit Emoji im Kommentar wurde vorher nicht geblockt, nachher schon.

## Eine Quelle für die Agent-Regeln

`.claude/hooks/agent_triggers.py` (Regex je Agent + Scope). Prompt-Hook, Stop-Hook und das Audit-Skript `.claude/scripts/agent_usage_audit.py` (`--days 14`, zeigt je Session, welche Agents liefen und welche Trigger ohne Agent blieben; nur dieses Gerät, Retro-Futter) lesen alle dieselbe Tabelle. Neuer Agent → neue Zeile dort, nicht nur eine Beschreibung in `.claude/agents/*.md`. Erster Audit 11.09.2026 (14 Tage, 23 Sessions): am häufigsten ausgelassen `engine-regression-tester`, `pipeline-auditor`, `strategy-auditor` und das Quant-Team, siehe [[Agent-Nutzungs-Audit 2026-09-11]].

## Auftrags-Typ-Router (Max, 21.09.2026)

Anlass: Max' Befund „ich muss quasi immer selbst sagen, dass alle Agents eingeschaltet werden sollen".
Das Audit (`agent_usage_audit.py --days 14`, 121 Sessions) hat ihn bestaetigt und beziffert:

| Agent | Aufrufe | Sessions mit Trigger, aber ohne Aufruf |
|---|---|---|
| quant-statistician / -mathematician | 39 / 36 | 6 / 6 |
| research-scout | 30 | 25 |
| engine-regression-tester | 19 | 15 |
| session-guard | 18 | 18 |
| verdict-auditor | 14 | 16 |
| design-guard | 8 | 22 |
| alpha-scout | 8 | 14 |
| **logbook-distiller** | **3** | **30** |

Der Unterschied lag nie am Agent, sondern an der Durchsetzung: das Quant-Team ist in den
Workflows `ein-weg`/`konzept-weg` fest verdrahtet, und **jede Session mit Workflow hatte null
Luecken**. Reine Text-Erinnerungen lagen bei 9-56 %.

Daraus der Umbau (Max' Entscheidung: Typ-Router mit Ketten als Workflows, blocken mit Override):

1. `on_prompt.py` legt die Quittung an und schlaegt Typen vor.
2. Claude schreibt den Typ fest -> damit steht die Pflichtkette (`work_types.py`).
3. Workflow `kette` faehrt sie (Rechner parallel, Gegenleser danach **mit** deren Ergebnissen),
   `konzept-weg`/`ein-weg` bleiben die Sonderwege fuer Konzepte und Hypothesen.
4. `guard_chain.py` laesst die schreibenden Aktionen erst danach durch.
5. `on_stop.py` (Punkt 4) laesst die Session bei offener Quittung nicht enden.

Selbsttest: `python .claude/scripts/test_chain.py` (112 Checks seit 28.09.2026, deckt auch ab, dass `kette.js`
und `work_types.py` dieselben Ketten tragen). Volle Doku: [[Arbeits-Workflow (Auftrags-Typen)]].

## Subagents und Workflows in `guard_chain` (gebaut 26.09., eingespielt 28.09.2026)

**Befund:** Gate 1 (Web ohne `research-scout`) hat den research-scout selbst gesperrt, wenn er in einem Ad-hoc-Workflow lief (`eval-vs-funded` 25.09., `bulenox-check` 26.09.: jeder WebSearch/WebFetch geblockt, Ergebnis nur Cache-Wissen, danach per `--skip` umgangen). alpha-scout hing am 21.09. genauso (6 von 6 Web-Aufrufen). Ursache: `used_agent_names` kannte nur Agent-Aufrufe im Haupt-Transkript plus die festen Workflows `ein-weg`/`konzept-weg`/`kette`. Dazu fand der verdict-auditor: das Quittungs-Gate (B) sperrte den research-scout am 23.09. (Typ `buch`) beim Zurückschreiben in den [[Research-Cache]].

**Gemessen** (Dump-Hook): im Subagent sind `session_id` und `transcript_path` die der **Eltern-Session**, dazu kommen `agent_id` und `agent_type`. Der Hauptthread hat beides nicht. Gilt für Agent-Tool-Subagents (26.09., Claude Code 2.1.281) und für **Workflow-Agents** (28.09., Mini-Workflow `hook-probe` mit research-scout + Explore). Deckt sich mit der offiziellen Hooks-Doku.

**Fix:**
- `WEB_AGENTS` = `research-scout`, `alpha-scout`, `claude-code-guide` dürfen selbst ins Web (Entscheidung Max 26.09., bestätigt 28.09.) und bei offener Kette in `Ressourcen/Research-Cache.md` schreiben. Erkannt über `agent_type`, Rückfall über `agent-<id>.meta.json`. Alle anderen Gates gelten für sie weiter.
- Agents aus **jedem** Workflow zählen als gelaufen (Regel 21.09.: Workflows sind die durchgesetzte Form der Kette). Quelle: `<sid>/subagents/workflows/*/journal.jsonl` plus `meta.json`. Gezählt erst ab `result`: abgebrochene Läufe ohne `result` gibt es wirklich, und ein abgebrochener strategy-auditor darf `book_state` nicht freigeben. Das sitzt zentral in `agent_usage_audit.py` und wirkt damit auch auf `guard_write`, `receipt.missing_steps`, `on_stop` und das Audit.
- Sperrt ein Gate einen Subagent, sagt die Meldung jetzt, dass er die Sperre an den Hauptthread zurückmelden soll, statt still weiterzuarbeiten.
- Fehler beim Typ-Lookup landen in `hook_errors.log`, die Aktion läuft durch.

**Live-Test 28.09.** (Probe-Hook, alte Hooks nur protokolliert, neue durchgesetzt): Explore per Agent-Tool und im Workflow → alt und neu gesperrt. research-scout im Workflow → alt gesperrt, neu durch. Hauptthread nach dem Workflow-Scout → alt gesperrt, neu durch.


## Sonstiges

- **Marker von Hand:** `python .claude/hooks/mark.py <regression_ok|pipeline_ok|push_next_at>` aus dem Vault-Root. Der Marker ist der bewusste Unlock — nie setzen, um einen Block „wegzumachen", ohne dass der Agent gelaufen ist.
- **Engine-Pfad:** die Hooks schauen auf `C:\Users\maxlk\Projects\trading-data\engine` (per `MAXLAB_ENGINE` überschreibbar). Der Laptop hat dort eine Kopie vom 03.09.2026, also greifen die Buch-/Sync-Wächter auch dort; die Box bleibt die Quelle der Wahrheit für das Buch. Ohne Engine-Ordner sind nur die Kommando-Wächter aktiv.
- **Ein Hook darf nie die Arbeit blockieren, weil er selbst kaputt ist:** jedes Skript fängt eigene Fehler ab und lässt still durch (`<engine>/.claude_hooks/hook_errors.log`). Hook-Änderungen greifen erst nach `/hooks` bzw. Neustart der Session. Neue Reflex-Regel in der CLAUDE.md → zuerst fragen, ob sie als Hook abbildbar ist (Dateipfad, Kommando-Muster, Dateizeit); Text bleibt für das, was der Harness nicht sehen kann.
- **Noch offen (PC ist aus):** die Hooks als Automatik in `hub_config.json` (`mock_loops`) eintragen, sobald der PC wieder an ist.

## Workflow `ein-weg` = Schritt 2 des EINEN Wegs als Skript (Max, 04.09.2026)

`.claude/workflows/ein-weg.js` (Aufruf: Workflow-Tool mit `name: "ein-weg"`, `args: {hypotheses: [{id, title, mechanism, why, market?, family?, source?}]}`). Ablauf deterministisch statt Prompt-Kette: ohne Why harter Stopp → `variant-scout` je Hypothese parallel (mit Strukturausgabe **plus** vollem Report-Text) → nur die als Testbar/Grenzwertig eingestuften gehen in **einen** `strategy-auditor`-Batch-Call → Entscheidungstabelle je Hypothese (in Bank + H()-Zeile / nachbessern / nicht bauen, mit Grund). Schritt 3/4 bleiben bei der Hauptsession: H()-Zeilen eintragen, `pipeline-auditor` (setzt `pipeline_ok`), `--enqueue --push`. Der Workflow schreibt nie Dateien.

## Workflow `konzept-weg` (Max, 11.09.2026)

`.claude/workflows/konzept-weg.js`, `args: {concept, date, source?, market?, skip_research?, skip_ein_weg?}`. Kette: `familien-scout` → `verdict-auditor` als Vollständigkeits-Check direkt dahinter (fehlt ein Weg, stimmt ein Stand, toter Verwandter übersehen?) → bei Lücken eine Nachtrag-Runde des Scouts → `research-scout` EIN Call mit allen Research-Fragen → Rückschreiben des Research-Stands in Karte + JSON durch den Scout → Kind-Workflow `ein-weg`. Details und Abnahmetests: [[Familien-Scout Agent]].

## Aus der CLAUDE.md (05.10.2026)

Aus der CLAUDE.md übernommen (05.10.2026): Regeln und Overrides, die nur dort standen.

**Todesurteil-Gate in `guard_chain.py` (Regel Max, 22.09.2026)**
- Ein Todesurteil im Strategie-Logbuch wird abgelehnt, solange die vier Pflichtfelder fehlen (Reichweite, Kategorie, Wiedervorlage, Stempel).
- Geprüft wird nur der **Urteilsblock** (`Verdikt:`/`Urteil:`/`Fazit:`), nicht der Fließtext. Rückblicke und Zitate fremder Urteile lösen nichts aus.
- Fehlalarm-Override: `python .claude/hooks/mark.py urteil_ok`.
- Selbsttest: `python .claude/scripts/test_urteil_gate.py` (7 Fälle, inklusive der Fehlalarm-Quellen).

**`on_stop.py`, Teil 5 (Workbench-Tests)**
- Hat die Session Tests mit Trades gerechnet, aber nicht per `workbench.publish(...)` ins Lab gestellt, endet sie einmal nicht (seit 25.09.2026).
- Ausweg bei reinen Tafeln ohne Trades: `python .claude/hooks/mark.py tests_ok`.

**Umgehungen werden gezählt (`receipt_stats.py`)**
- `python .claude/scripts/receipt_stats.py --days 7` zeigt, wie oft eine Kette ausgelassen wurde und warum. Der `retro-agent` liest das sonntags.
- Ein ständig umgangenes Gate ist ein falsches Gate. Dann wird die Kette gekürzt oder das Gate verengt, nicht besser aufgepasst.
- Auslassen ist nur mit Grund erlaubt: `receipt.py --sid <id> --skip <schritt> --why "<ein Satz>"`. Ein Ein-Wort-`--why` wird abgelehnt, der Grund landet in der Quittung und im Retro.

**Meta-Regeln**
- Neue Reflex-Regel geplant? Zuerst fragen, ob sie als Hook abbildbar ist (Dateipfad, Kommando-Muster, Dateizeit), statt sie nur als Text abzulegen.
- Ein Hook blockiert nie die Arbeit, weil er selbst kaputt ist: Fehler werden verschluckt und geloggt, nie geworfen.

## Wissens-Router und Schlusszeilen-Check (Max, 05.10.2026)

Teil des Umbaus [[CLAUDE.md Verschlankung]]. Ziel: die CLAUDE.md schlank machen, ohne dass eine Session etwas nicht mehr weiß.

**Wissens-Router** (`.claude/hooks/knowledge_router.py`, aufgerufen in `on_prompt.py` Abschnitt 0)
- Erkennt im Prompt das Thema (17 Themen: Juli-Modus, Developer, Hub, Gate, Discovery, RiskGuard, Konto, GitHub, Mail, Sprint, Tot, Box, Buch, Claude, Gründung, Ziel, Werkzeug) und legt Kernzeilen plus „lies Notiz X" hin. Je Thema nur beim ersten Auftauchen in einer Session.
- Gebaut für Max' echte Sprache (945 Prompts, 30 Tage): „Cloud" = Claude (nie GitHub), „hab" ist nie Hub, „Juni-Modus" = Juli-Modus, „i8" = E8, „Funnet Next" = FundedNext, „Stereolab" = Strategy Lab. Ticketnummern („AP 72", „AP73") holen den Tickettitel aus `tasks.json` und routen ihn mit.
- Läuft vor dem 12-Zeichen-Filter, damit kurze Prompts wie „Juli-Modus" zünden.
- Subagent-Rückmeldungen und System-Benachrichtigungen (`<agent-message`, `<task-notification`, „Another Claude session sent a message") sind nicht von Max: kein Routing, kein Agent-Reflex, keine Quittung. Fix für die sechs Fehlalarme vom 05.10.
- `MODE = "schatten"`: loggt nur nach `<engine>/.claude_hooks/router_log.jsonl`, blendet nichts ein, solange die volle CLAUDE.md geladen ist. Umschalten auf `"live"` erst nach der Abnahme durch Max.
- Auswertung: `python .claude/scripts/router_report.py --days 3` (Treffer je Thema, Prompts ohne Thema, Hook-Fehler). Tests: `python .claude/scripts/test_router.py` (50 Fälle), Trefferquote auf einem Prompt-Korpus mit `--korpus <datei>`.
- Neue Lücke aus dem Schattenbetrieb → erst als Fall in `test_router.py`, dann Muster anpassen.

**Schlusszeilen-Check** (`.claude/hooks/schlusszeilen.py`, `on_stop.py` Teil 6)
- Hat die Antwort im Zug Dateien geändert (Edit/Write oder Bash mit `>>`, Set-Content, `git commit`, `mv`, `cp`, `rm` …), müssen am Ende Modell-Empfehlung, `/clear`-Zeile und Daily-Note-Zeile stehen. Reine Antworten ab 600 Zeichen brauchen Modell + `/clear`.
- Locker erkannt: „Modell" plus sonnet/haiku/opus/fable, „/clear" oder „frische Session" oder „Kontext weiterverwenden", „Daily Note".
- Frei bleiben: kurze Antworten ohne Änderung, Rückfragen ohne Änderung (Antwort endet mit „?", Regel „Offene Fragen zuerst"), Zwischenmeldungen. **Läuft im Zug noch ein Hintergrund-Agent** (gestartet, keine task-notification zurück), greift der Check nicht (Live-Fund am ersten Abend). Einmal je Prompt geblockt, nie zweimal hintereinander.
- Muster nach Gegenprobe an 1.153 echten Zügen gelockert: Modellname reicht (ohne das Wort „Modell"), „Clear: nein", „Kontext kann bleiben", „Session kann weiterlaufen", „heutige Notiz" zählen.
- Jeder Treffer landet in `<engine>/.claude_hooks/schluss_log.jsonl` (Feld `blocked`), damit die Fehlalarm-Quote abnehmbar ist.
- Tests: `python .claude/scripts/test_schlusszeilen.py` (23 Fälle, davon 6 echte Schlussblöcke aus alten Antworten).
- Router- und Schluss-Log stehen in der `.gitignore` von trading-data (Prompt-Auszüge gehören nicht ins Backup-Repo).
- **Falle beim Bauen (05.10.):** Python-Heredocs über Git Bash haben `\b` als Steuerzeichen geschrieben, der Check blockte dadurch alles. Regex-Zeilen nur mit dem Edit-Tool schreiben, danach auf Steuerzeichen prüfen.
