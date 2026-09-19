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
| `after_change.py` (PostToolUse Edit/Write/Bash) | Sagt die Folgepflicht an: `book_state*.json` neuer als letzter Push → finalize + push-next; Engine-Kern → Regressionstest vor Sync; Discovery-Code → Runner-Neustart; Hypothesen-Bank → variant-scout/strategy-auditor/pipeline-auditor; Hub/Lab/Report-Oberfläche → design-guard; neuer Agent/Automatik → Hub-Roster; Logbuch → logbook-distiller; neue `.cs`-Strategie → `NS_MAP`. |
| `on_stop.py` (Stop) | **Lässt die Session nicht enden**, solange `book_state*.json` neuer ist als der letzte `--push-next` (einmal blocken, dann nur noch erinnern). Unlock: `python .claude/hooks/mark.py push_next_at`. Seit 09.09.2026 zusätzlich: **lässt die Session nicht enden**, wenn sie selbst Dateien geändert hat, aber die heutige Daily Note seit Session-Start nicht angefasst wurde — gilt geräteübergreifend, auch ohne Engine-Ordner. Erkennung über das eigene Transkript, reine Lese-Sessions triggern nichts. |
| `on_prompt.py` (UserPromptSubmit, seit 11.09.2026) | **Agent-Reflex beim Tippen:** prüft den Prompt gegen die Einschalt-Regeln in `agent_triggers.py` und legt die passenden Agents als Kontext hin. Keine Sperre, nur Erinnerung. |
| `on_stop.py`, Teil 3 (Stop, seit 11.09.2026) | **Agent vergessen?** Scannt das eigene Transkript mit denselben Regeln (Prompt, geänderte Dateien, Bash-Kommandos, direkte WebSearch/WebFetch) und lässt die Session einmal nicht enden, wenn ein Trigger gefeuert hat, der Agent aber nie lief. Ausweg: einschalten, oder in einem Satz sagen, warum er hier nicht passt, dann erneut beenden. Achtung Fehlalarme: die Regex matcht auf reinen Text (auch zitierte Tool-Ausgaben wie `/context`-Listen oder Skill-Namen in einer Tabelle), nicht auf Bedeutung — ein Treffer heißt nicht automatisch, dass der Agent wirklich passt. |
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

## Sonstiges

- **Marker von Hand:** `python .claude/hooks/mark.py <regression_ok|pipeline_ok|push_next_at>` aus dem Vault-Root. Der Marker ist der bewusste Unlock — nie setzen, um einen Block „wegzumachen", ohne dass der Agent gelaufen ist.
- **Engine-Pfad:** die Hooks schauen auf `C:\Users\maxlk\Projects\trading-data\engine` (per `MAXLAB_ENGINE` überschreibbar). Der Laptop hat dort eine Kopie vom 03.09.2026, also greifen die Buch-/Sync-Wächter auch dort; die Box bleibt die Quelle der Wahrheit für das Buch. Ohne Engine-Ordner sind nur die Kommando-Wächter aktiv.
- **Ein Hook darf nie die Arbeit blockieren, weil er selbst kaputt ist:** jedes Skript fängt eigene Fehler ab und lässt still durch (`<engine>/.claude_hooks/hook_errors.log`). Hook-Änderungen greifen erst nach `/hooks` bzw. Neustart der Session. Neue Reflex-Regel in der CLAUDE.md → zuerst fragen, ob sie als Hook abbildbar ist (Dateipfad, Kommando-Muster, Dateizeit); Text bleibt für das, was der Harness nicht sehen kann.
- **Noch offen (PC ist aus):** die Hooks als Automatik in `hub_config.json` (`mock_loops`) eintragen, sobald der PC wieder an ist.

## Workflow `ein-weg` = Schritt 2 des EINEN Wegs als Skript (Max, 04.09.2026)

`.claude/workflows/ein-weg.js` (Aufruf: Workflow-Tool mit `name: "ein-weg"`, `args: {hypotheses: [{id, title, mechanism, why, market?, family?, source?}]}`). Ablauf deterministisch statt Prompt-Kette: ohne Why harter Stopp → `variant-scout` je Hypothese parallel (mit Strukturausgabe **plus** vollem Report-Text) → nur die als Testbar/Grenzwertig eingestuften gehen in **einen** `strategy-auditor`-Batch-Call → Entscheidungstabelle je Hypothese (in Bank + H()-Zeile / nachbessern / nicht bauen, mit Grund). Schritt 3/4 bleiben bei der Hauptsession: H()-Zeilen eintragen, `pipeline-auditor` (setzt `pipeline_ok`), `--enqueue --push`. Der Workflow schreibt nie Dateien.

## Workflow `konzept-weg` (Max, 11.09.2026)

`.claude/workflows/konzept-weg.js`, `args: {concept, date, source?, market?, skip_research?, skip_ein_weg?}`. Kette: `familien-scout` → `verdict-auditor` als Vollständigkeits-Check direkt dahinter (fehlt ein Weg, stimmt ein Stand, toter Verwandter übersehen?) → bei Lücken eine Nachtrag-Runde des Scouts → `research-scout` EIN Call mit allen Research-Fragen → Rückschreiben des Research-Stands in Karte + JSON durch den Scout → Kind-Workflow `ein-weg`. Details und Abnahmetests: [[Familien-Scout Agent]].
