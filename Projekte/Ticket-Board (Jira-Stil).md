---
tags:
  - projekt
  - bereich/softwareentwicklung
  - strategy-lab
  - tickets
erstellt: 2026-09-28
status: am PC eingespielt, Jira-Umbau fertig (29.09.2026), Box-Migration offen (AP267)
---
# 🗂️ Ticket-Board im Strategy Lab (Jira-Stil)

⬅️ [[Strategy Lab Workbench]] · [[Design-System (Hub & Apps)]] · [[Daily Notes/2026-09-28]]

## Anlass (Max, 28.09.2026)

Max will das Ticketsystem so bedienen wie Jira: Backlog, Sprints mit Sprint Planning, Boards zu verschiedenen Themen, Tickets frei hin und her schieben. Voraussetzung: Claude kann Tickets selbst anlegen, verschieben und verwalten.

## Entscheidungen von Max (28.09.2026)

1. **Eigenes Board im Strategy Lab**, kein echtes Jira, kein Hybrid. `tasks.json` bleibt die Quelle der Wahrheit (Box führt, Regel 06.09.), Box-Automatik (`auto_notes`, `inbox_tool --pull/--push-tasks`), `/ticket` und Hooks laufen unverändert weiter.
2. **Alle AP-Tickets übernehmen**, offene und erledigte. AP-Nummer bleibt der Schlüssel.
3. **Sprint = 1 Woche**, Mo bis So, Planning sonntags (passt zum Wochenend-Review fürs Next-Week-Buch), erster Sprint ab 05.10.
5. **Schätzung in Stunden**, nicht Story Points.
6. **Box-Automatiken legen selbst Tickets an** (Abschnitt 3b).
4. **Vier Boards:** Trading/Alpha · Infra/Box/NT8 · Hub/Lab/Tools · Gründung/Privat.

Verworfen, mit Grund: echtes Jira Cloud (Atlassian-Connector) hätte `tasks.json`, Box-Automatik und `/ticket` auf die Jira-API gezwungen, die Box bräuchte einen API-Token, und der Connector kostet in jeder Session Kontext (gut 20 Tools). Hybrid wäre zwei Quellen plus Sync-Skript, also das meiste Bauen für den gleichen Nutzen.

---

## 1. Was Jira kann und was davon ins Board kommt

| Jira-Funktion | Was es ist | Im Board | Phase |
|---|---|---|---|
| **Ticket-Arten** | Epic, Story, Task, Bug, Subtask | ja, Feld `type` | 1 |
| **Epics** | Klammer über viele Tickets (bei uns: die Projekte, z.B. Workbench, Gründung, Juli-Modus) | ja, Feld `epic` + Fortschrittsbalken | 1 |
| **Subtasks** | Unteraufgaben eines Tickets | ja, Feld `parent` | 1 |
| **Issue Links** | blockiert / wird blockiert von / hängt zusammen mit / Duplikat | ja, `blocked_by` bleibt, dazu `links` | 1 |
| **Priorität** | Highest bis Lowest | vorhanden (`prio` rot/orange/gelb/grün), nur anders angezeigt | 1 |
| **Labels, Komponenten** | freie Schlagworte, feste Bereiche | `labels` (Komponente = Board) | 1 |
| **Fälligkeit** | Due Date | vorhanden (`when`) | 1 |
| **Schätzung** | Story Points oder Stunden | **Stunden** (Max, 28.09.), Feld `estimate_h` | 2 |
| **Kommentare / Verlauf** | Diskussion und Änderungshistorie am Ticket | `progress_notes` + neues Ereignis-Log | 1 |
| **Akzeptanzkriterien** | wann ist es fertig | vorhanden (`done_when`) | 1 |
| **Checkliste** | Schritte im Ticket | vorhanden (`guide`), abhakbar | 2 |
| **Backlog** | priorisierte Liste aller nicht geplanten Tickets, per Drag&Drop sortierbar | ja, Feld `rank` | 2 |
| **Sprints** | Zeitbox mit Ziel, Start, Ende | ja, eigene Datei (siehe Datenmodell) | 2 |
| **Sprint Planning** | Tickets aus dem Backlog in den Sprint ziehen, Kapazität gegen Stunden | ja, eigene Ansicht + `/sprint`-Skill | 2 |
| **Sprint abschließen** | Unfertiges wandert in Backlog oder nächsten Sprint, Sprint-Report entsteht | ja | 2 |
| **Scrum-Board** | Spalten für den laufenden Sprint | ja | 1 |
| **Kanban-Board** | Dauerfluss ohne Sprint, WIP-Limits | ja, pro Board umschaltbar | 1 |
| **Workflow** | Status und erlaubte Übergänge, Spalten = Mengen von Status | ja, Spalten-Status-Zuordnung wie in Jira | 1 |
| **Swimlanes** | Zeilen nach Epic, Priorität oder Board | ja | 3 |
| **Quick Filters** | Ein-Klick-Filter (nur rot, nur blockiert, nur Epic X) | ja | 1 |
| **Suche (JQL)** | Abfragesprache | vereinfachte Suchzeile `board:trading prio:rot status:offen sprint:aktuell text` | 1 |
| **Burndown** | offene Stunden je Tag im Sprint | ja, aus Ereignis-Log | 3 |
| **Velocity** | geschaffte Stunden je Sprint | ja | 3 |
| **Sprint-Report** | geschafft / verschoben / neu reingekommen | ja, auch als Daily-Note-Baustein | 3 |
| **Cumulative Flow** | Tickets je Status über Zeit | ja | 3 |
| **Timeline / Roadmap** | Epics als Balken auf der Zeitachse | ja, einfach | 3 |
| **Automation** | Regeln wie „alle Subtasks fertig → Parent fertig" | wenige feste Regeln, keine Regel-Engine; Box legt selbst Tickets an (Abschnitt 3b) | 3 |
| Rechte, Teams, Mehrbenutzer, Zeiterfassung, Anhänge, Watcher, Releases/Versionen | Team- und Enterprise-Kram | **bewusst weggelassen** (ein Nutzer, Simplex beats Komplex) | nein |

---

## 2. Datenmodell (nur additiv, nichts umbenennen)

**Grundsatz:** `tasks.json` bleibt eine JSON-Liste, alle bisherigen Felder bleiben wie sie sind. Neue Felder sind optional, damit `inbox_tool`, `auto_check.py`, `/ticket` und alle Hooks ohne Änderung weiterlaufen.

### Neue Felder je Ticket in `tasks.json`

| Feld | Werte | Default bei Migration |
|---|---|---|
| `type` | `epic` / `story` / `task` / `bug` / `subtask` | `task` |
| `board` | `trading` / `infra` / `lab` / `privat` | per Stichwort-Zuordnung, Claude prüft, Max stichprobt |
| `epic` | `ap_id` eines Epics | leer, aktive Projekte werden Epics |
| `parent` | `ap_id` (nur bei `subtask`) | leer |
| `sprint` | Sprint-ID, z.B. `S2026-41` | leer (= Backlog) |
| `estimate_h` | geschätzte Stunden (0,5er-Schritte) | leer |
| `spent_h` | tatsächlich gebrauchte Stunden, beim Schließen eintragen | leer |
| `source_key` | Herkunft bei Auto-Tickets, z.B. `auto_check:wv:164` (verhindert Doppel-Tickets) | leer |
| `labels` | Liste | leer |
| `rank` | Zahl, Backlog-Reihenfolge | aus `prio` + `when` |
| `links` | `[{"rel": "relates", "ap_id": "AP12"}]` | leer (`blocked_by` bleibt eigenes Feld) |
| `updated` | ISO-Zeit | Datei-Stand |

### Status und Spalten (Jira-Modell)

`status` bleibt das einzige Statusfeld. Spalten sind **Mengen von Status-Werten**, genau wie in Jira. Dadurch kann nichts auseinanderlaufen, und wer heute `status == "done"` prüft, merkt nichts.

| Spalte | Status-Werte (Vorschlag, beim Bau gegen den echten Bestand prüfen) |
|---|---|
| Backlog / To Do | `offen`, `open`, `todo`, leer |
| In Arbeit | `in_arbeit`, `in progress`, `laufend` |
| Blockiert | `blockiert`, `blocked`, oder `blocked_by` mit offenem Ticket |
| Review | `review`, `wartet_max` |
| Fertig | `done`, `erledigt`, `closed` |

Vor dem Festzurren: `grep` über Engine, Box-Skripte und `.claude/hooks/` nach allen Stellen, die `status` lesen oder schreiben, und die Liste der tatsächlich vorkommenden Werte ziehen.

### Neue Dateien neben `tasks.json`

- **`ticket_board.json`**: Boards (Name, Farbe, Modus Scrum/Kanban, Spalten-Status-Zuordnung, WIP-Limits, Quick-Filter), Sprints (`id`, `name`, `goal`, `start`, `end`, `state` geplant/aktiv/fertig, `capacity_h`), Velocity-Historie.
- **`ticket_events.jsonl`**: append-only Log jeder Änderung (`ts`, `ap_id`, `feld`, `alt`, `neu`, `wer` = max/claude/box). Basis für Burndown, Velocity, CFD und gleichzeitig Verlauf am Ticket. Box-Auto-Notes schreiben ein Ereignis mit `wer: box`.
- **Sync:** `inbox_tool.py --pull/--push-tasks` zieht beide Dateien mit (gleiche Regeln wie `tasks.json`: `.bak`, nie blind überschreiben). Beim Log: Zeilen zusammenführen statt überschreiben.

### Schreibschutz (wichtigster Punkt)

Box, Lab-UI und Claude-Sessions schreiben künftig alle in `tasks.json`. Deshalb läuft **jeder Schreibzugriff über eine Bibliothek** `engine/ticket_lib.py`:
- Datei-Sperre (Lock-Datei) plus Versionsprüfung (Hash beim Lesen, beim Schreiben erneut prüfen; hat sich was geändert, neu laden und nur das eigene Feld anwenden).
- `.bak` vor jedem Schreiben, atomar über Temp-Datei + Rename, UTF-8.
- Server-Endpunkte, CLI und Box-Skripte benutzen dieselbe Bibliothek, keine zweite Schreiblogik.

---

## 3. Steuerung durch Claude

**CLI `engine/ticket_tool.py`** (dünn über `ticket_lib`), damit jede Session Tickets anlegen und verwalten kann, ohne JSON von Hand anzufassen:

```
python ticket_tool.py new "Titel" --board trading --type story --prio orange --why "..." [--epic AP250] [--hours 3]
python ticket_tool.py move AP260 --status in_arbeit
python ticket_tool.py edit AP260 --hours 5 --labels gate,v3
python ticket_tool.py note AP260 "Zwischenstand ..."
python ticket_tool.py link AP260 blocks AP261
python ticket_tool.py find "board:trading prio:rot sprint:aktuell"
python ticket_tool.py sprint new --goal "..." --start 2026-10-05
python ticket_tool.py sprint plan S2026-41 AP260 AP261
python ticket_tool.py sprint start S2026-41 | close S2026-41
python ticket_tool.py report S2026-41        # Sprint-Report als Markdown für die Daily Note
```

- `new` macht vorher selbst `--pull` (Nummernkollision 03.-06.09.) und danach `--push-tasks`. Andere Schreibbefehle pushen am Ende ebenfalls.
- Ausgabe kompakt (eine Zeile je Ticket), nie die ganze Datei in den Kontext.
- **Skill `/ticket`** wird erweitert (anlegen, verschieben, Notiz) und ruft das CLI auf.
- **Neuer Skill `/sprint`**: Sprint Planning mit Claude. Liest Backlog, Velocity der letzten Sprints und offene Blocker, schlägt einen Sprint vor (Ziel, Tickets, Stunden gegen Kapazität, Kapazität aus den gebrauchten Stunden der letzten Sprints), Max nickt ab oder schiebt um, dann `sprint plan` + `start`. Zum Sprint-Ende: Report, Unfertiges zurück, Retro-Zeile in die Daily Note.

### 3b. Box legt selbst Tickets an (Max, 28.09.2026)

Automatiken schreiben über dasselbe `ticket_lib` (nie direkt ins JSON), immer als `wer: box`, Label `auto`, **immer in den Backlog, nie direkt in den laufenden Sprint**. Max oder `/sprint` entscheiden beim Planning, was davon reinkommt.

| Quelle | Wann | Board | Prio |
|---|---|---|---|
| `auto_check.py` | Wiedervorlage aus dem Logbuch ist fällig oder ihre Bedingung ist eingetreten (Fälle #164/#139) | Trading/Alpha | orange |
| Discovery-Inbox | Kandidat „besser"/„vs Original besser" | Trading/Alpha | orange |
| `promote_next.py` | Kandidat ins Next-Week-Buch promotet (Wochenend-Review nötig) | Trading/Alpha | gelb |
| Runner/Box-Watchdog | Runner steht, `queue_empty`, Buch-Sync veraltet, Telegram stumm | Infra/Box/NT8 | rot |

- **Keine Doppel-Tickets:** jedes Auto-Ticket trägt `source_key`. Gibt es schon ein offenes Ticket mit demselben Schlüssel, kommt nur eine Notiz dazu, kein neues Ticket.
- **Deckel:** höchstens 10 Auto-Tickets pro Tag und Quelle, darüber ein Sammelticket. Sonst flutet ein kaputter Runner den Backlog.
- Nummernvergabe läuft auf der Box (Quelle der Wahrheit), deshalb keine Kollision mit den Tickets vom PC.
- Welche Quellen genau angebunden werden, wird in Phase 0 gegen die echten Skripte geprüft. Die Tabelle ist der Startumfang.

---

## 4. Oberfläche im Lab

Neuer Top-Tab **„Tickets"** in `engine/lab_ui/` (eigene Dateien `tickets.css`/`tickets.js`, wie die Workbench), Sub-Tabs:

| Sub-Tab | Inhalt |
|---|---|
| **Board** | Board-Umschalter (4 Boards + „Alle"), Spalten nach Workflow, Karten per Drag&Drop verschieben, WIP-Limit-Warnung, Quick-Filter, Suchzeile, Swimlanes (Phase 3) |
| **Backlog** | Sprint-Blöcke oben (aktiv, geplant), Backlog darunter, Drag&Drop zum Sortieren und zum Einplanen, Stunden-Summe je Sprint gegen Kapazität |
| **Planning** | Sprint anlegen (Ziel, Zeitraum, Kapazität), Vorschlag von `/sprint` anzeigen, übernehmen |
| **Reports** | Burndown, Velocity, Sprint-Report, CFD, Timeline der Epics |

- **Ticket-Detail** als Seitenpanel (Esc schließt): alle Felder editierbar, Checkliste aus `guide` abhakbar, Verlauf aus dem Ereignis-Log, Links klickbar.
- **Schnell anlegen:** Taste `c` oder Button, Titel + Board + Prio reichen, Rest später.
- **Karte:** AP-Nummer, Titel (gekürzt), Prio-Balken + Wort (Farbe nie allein, Charta Regel 15), Typ-Icon, Stunden, Epic-Chip, `auto`-Chip bei Box-Tickets, Blocker-Symbol.
- **Charta-Pflichten:** nur bestehende Tokens, Radius `var(--radius)`, `--sp-*`-Abstände, Zahlen Mono + `tabular-nums`, leere Spalten mit Satz, Karten verschieben ohne Voll-Reload, Server-Schreibvorgang mit `busy`-Zustand, Fehler (Versionskonflikt) sichtbar statt still. `design-guard` in jeder Phase.
- **Server:** Endpunkte `/api/tickets` (lesen, gefiltert), `/api/tickets/<ap>` (ändern), `/api/sprints`, `/api/boards`, alle über `ticket_lib`.

---

## 5. Sprint-Rhythmus (von Max bestätigt 28.09.2026)

- Sprint läuft **Mo bis So**. Planning + Review am **Sonntag**, gleich nach dem Wochenend-Review fürs Buch.
- **Schätzung und Kapazität in Stunden** (Max, 28.09.). Vollzeitjob bis 03.07.2027, deshalb die ersten 2 bis 3 Sprints ohne festen Kapazitätswert, danach der Schnitt der tatsächlich gebrauchten Stunden (`spent_h`) als Richtwert. Ab 04.07.2027 (Vollzeit selbstständig) Kapazität neu setzen.
- **Erster Sprint: S2026-41, Mo 05.10. bis So 11.10.**, Planning So 04.10. Danach jede Woche gleich.

---

## 6. Phasen

- [ ] **Phase 0, Bestand:** `--pull`, Statuswerte und Leser/Schreiber von `tasks.json` erfassen, Spalten-Zuordnung festziehen. `session-guard` vorher (geteilte Datei).
- [ ] **Phase 1, Kern:** `ticket_lib.py` (Sperre, Versionsprüfung, Events), Migration aller Tickets (neue Felder, Board-Zuordnung, Epics aus aktiven Projekten), `ticket_tool.py`, Board-Ansicht mit Drag&Drop, Detail-Panel, Quick-Filter, Suche. `inbox_tool` synct die neuen Dateien. `/ticket` erweitert.
- [ ] **Phase 2, Scrum:** Backlog mit Rang, Sprints anlegen/planen/starten/abschließen, Stunden (Schätzung + gebraucht), Checkliste, `/sprint`-Skill.
- [ ] **Phase 3, Reports:** Burndown, Velocity, Sprint-Report (auch als Daily-Note-Baustein), CFD, Timeline, Swimlanes, feste Automations-Regeln, Box legt selbst Tickets an (3b).
- [ ] Nach jeder Phase: `lab_selftest.py` um Ticket-Routen erweitern und laufen lassen, `design-guard`, `verdict-auditor` vor „fertig", Box-Sync (Lab + `inbox_tool`) erst nach Test.

Tickets je Phase werden in der Bau-Session angelegt (neue Nummern nur nach `--pull`).

## 7. Entschieden am 28.09.2026 (vorher offen)

- Sprint Mo bis So, Planning sonntags, Start 05.10.: **ja**.
- Schätzung: **Stunden**.
- Box-Automatiken legen selbst Tickets an: **ja**, siehe 3b.

---

## Stand 28.09.2026 abends: gebaut (Cloud-Session, noch nicht auf PC/Box)

Gebaut in der Cloud gegen das GitHub-Backup `trading-data`, Branch `claude/awesome-hawking-tqcayx` (Commits 24c3487, df1c21d). **Weder PC noch Box haben den Stand.** Auf der Box ist noch nichts migriert.

| Teil | Datei | Was |
|---|---|---|
| Schreibschicht | `engine/ticket_lib.py` | einzige Stelle, die tasks.json schreibt: Sperre, atomar mit Windows-Retry, Tagesbackup `tasks.json.bak-board-*`, Verlauf `ticket_events.jsonl`, Sprints `ticket_board.json`, Burndown, Velocity, Auto-Tickets |
| CLI für Claude | `engine/ticket_tool.py` | show, find, new, move, edit, note, link, board, backlog, sprint (new/plan/start/close/edit/list), report |
| Migration | `engine/ticket_migrate.py` | Probelauf Standard, `--apply` schreibt. Additiv: Board, Typ, Rang, Zuständig. Holt entfernte Tickets aus `tasks.json.bak*` als erledigt mit Label `archiv` zurück (auf dem PC-Schnappschuss: 118 ergänzt, 140 zurück). Legt Sprint S2026-41 an |
| Lab | `engine/lab_ui/tickets_board.js/.css`, `lab.js`, `index.html` | im Tab Tickets drei neue Ansichten: **Board**, **Backlog**, **Sprints**. Tab-Leiste jetzt oben für alle sechs Ansichten |
| Server | `engine/app_server.py` | `/api/tickets/*`. Die alten `/api/tasks`-Schreibwege laufen jetzt über die Sperre. 15 s nach der letzten Änderung wird mit der Box abgeglichen, vor dem Anlegen wird gezogen |
| Abgleich | `engine/discovery/inbox_tool.py` | Dreiwege-Merge über `tasks.json.sync-base`: pro Feld gewinnt die Seite, die geändert hat. Notizen werden vereinigt. Kollision nur bei gleicher AP mit anderer id. Sprints und Verlauf laufen mit |
| Automatik (3b) | `engine/auto_check.py` | `auto_tickets()`: Discovery-Kandidat „besser" (letzte 7 Tage, ungelesen), `queue_empty` (24 h), Runner-Herzschlag > 30 Min. `promote_next` und Workbench „Trade ist falsch" tragen Board-Felder |
| Tests | `test_ticket_lib.py`, `test_ticket_sync.py`, `lab_selftest.py` | alle grün in der Cloud, Workbench-Teil vom Selbsttest braucht Windows-Daten |
| Skills (Vault) | `.claude/skills/ticket`, `.claude/skills/sprint` | `/ticket` über das CLI, `/sprint` für Planning und Abschluss |

**Farben:** Prio „gelb" heißt im Board „Mittel" und nutzt `--accent`. Die alte Ansicht kennt „gelb" gar nicht (zeigt es als grün „Normal"), das war vorher schon so.

**Gegenleser:** `design-guard` vorab und nach dem Bau (9 Pflichtpunkte, alle umgesetzt), `verdict-auditor` (Urteil zuerst „voreilig": Umbenennen hätte den Sync blockiert, Erledigt am PC wäre von einer späteren Box-Notiz überschrieben worden; beides behoben und als Test drin).

### Einspielen (in dieser Reihenfolge, aus einer PC-Session)

1. `session-guard`, dann `git status` in trading-data. Lokale Änderungen seit dem Backup (28.09. 15:37) an denselben Dateien vorher sichern.
2. Branch holen und zusammenführen (`git fetch origin claude/awesome-hawking-tqcayx`, dann `git merge`). Die Dateien `tasks.json` und `tasks.json.bak*` fasst der Branch nicht an.
3. Am PC: `python test_ticket_lib.py`, `python test_ticket_sync.py` (jetzt mit echter discovery_lib), `python lab_selftest.py` komplett, `engine-regression-tester`. Ein kurzer Test, ob das Schreiben klappt, während das Lab die Datei liest.
4. Box: `tasks.json` sichern, Engine-Dateien syncen (Hook verlangt `regression_ok`), Runner laut Hook neu starten (Discovery-Code geändert).
5. Auf der Box `python ticket_migrate.py` (Probelauf) und Max die Zahlen zeigen, erst dann `--apply`. Die Box hat andere Backups als der PC, die Zahl 140 gilt dort nicht.
6. Am PC `python discovery/inbox_tool.py --pull`, Lab-Server neu starten (Python-Code geändert).
7. **Erst danach** den Vault-Branch mit den neuen Skills übernehmen, sonst zeigt `/ticket` auf ein Tool, das es am PC noch nicht gibt.

### Grenzen und Tickets für später (nach `--pull` anlegen)

- Auto-Tickets entstehen im `auto_check.py` am PC. **Ist der PC aus, legt die Box selbst keine an.** Ein Box-eigener Check wäre ein eigenes Ticket.
- Wiedervorlagen aus dem Logbuch sind nicht angebunden, es gibt dafür keine maschinenlesbare Liste.
- Beim Zurückschreiben auf die Box nutzt scp keine Sperre und schreibt nicht atomar. Das Fenster ist ein paar Sekunden lang.
- `updated` steht ohne Zeitzone. Rund um die Zeitumstellung (25.10.) kann eine Stunde lang die falsche Seite als neuer gelten, das betrifft nur den Fall, dass beide dasselbe Feld geändert haben.
- Löschen wird nicht synchronisiert, Tickets werden nur erledigt.
- Noch nicht gebaut: Swimlanes, Cumulative Flow, Epic-Timeline, WIP-Limit im Lab einstellbar (geht nur in `ticket_board.json`, Standard: keins).

**Entschieden (Max, 28.09.2026 abends):** kein WIP-Limit (Commit 08f1eb3 in trading-data). Prio „gelb" heißt jetzt auch in der alten Ansicht „Mittel". Einspielen über eine PC-Session (Aufgaben-Karte in der Claude-App), die Box-Migration darf nach plausiblem Probelauf direkt `--apply` machen.

## Stand 29.09.2026: am PC eingespielt, Box offen (Session baa48c56)

**Eingespielt am PC, Box noch nicht.** Grund: Die Gate-v4-Session (eadffd5a, AP257) baute nachts an denselben Discovery-Dateien und wollte selbst auf die Box syncen. Max hat entschieden, den PC jetzt zu machen und die Box erst danach. Die Box-Migration hängt an **AP267**. Max sagt Claude Bescheid, wenn es losgehen soll.

| Schritt | Ergebnis |
|---|---|
| Sicherung | Arbeitsstand vorher als Commit `4c77802` („Backup-Stand vor Ticket-Board“) |
| Merge | Branch ohne Konflikt in trading-data `main` (`724e752`). Gate v4 (lokal) und Ticket-Sync (Branch) berühren in `inbox_tool.py`/`promote_next.py` verschiedene Stellen |
| Tests | `test_ticket_lib` und `test_ticket_sync` grün, mit echter discovery_lib, ohne „nutzt Ersatz“. `lab_selftest --static` und komplett gegen den laufenden Server grün |
| Windows-Check | Beim Schreiben unter Dauerlesen: 5 von 5 Läufen 20/20 Notizen. Ein früher Lauf im Extremfeuer hatte 7 Schreibfehler. Gefunden: Leser bekamen genau während `os.replace` PermissionError (etwa 5 von 2.000). **Fix:** Lese-Retry in `ticket_lib._read_json`, alte `/api/tasks` läuft darüber (vorher kurz leere Liste). Danach 5 von 5 Läufen fehlerfrei (`9a77094`) |
| Golden Master | grün, Marker `regression_ok` 29.09. 09:21. Fingerprint neu wegen der Gate-v4-Nachbesserungen, Rechenkern unverändert |
| Lab | neu gestartet (job-frei per WMI, Port 8756). Board, Backlog, Sprints laufen, Konsole ohne Fehler. Ohne Migration stehen alle Boards auf 0 und es gibt noch keinen Sprint, das ist so erwartet |
| Test-Ticket im Lab | **nicht gemacht**, weil es nach 15 s mit der Box abgleicht. Kommt mit der Box-Migration (AP267) |
| Hub | Automatik „MaxLab Auto-Check (auto_check.py)“ mit „legt Auto-Tickets an (Kandidat besser, Queue leer, Runner steht)“ eingetragen, hot_reload ok. Skills sind in `hub_config.json` nicht gelistet, `/sprint` hat dort keinen Platz |
| Backup | trading-data `main` gepusht (`e050b23`, inkl. Merge der Cloud-Marktzustands-Karte) |
| Vault | Branch in `master` gemergt und gepusht (Konflikte in Daily Note 28.09. und `.gitignore`, beide Seiten behalten). **Der Vault-Ordner am PC ist noch nicht nachgezogen**, weil dort andere Sessions offene Änderungen haben (CLAUDE.md, Daily Notes 28./29., Latte-Audit). `/ticket` und `/sprint` gibt es am PC erst nach `git pull` im Vault |

**Fund beim Einspielen:** `box_provision_discovery.ps1 -SyncOnly` kopiert den ganzen Engine-Ordner, **`tasks.json` steht nicht in der Ausnahmeliste**. Jeder Engine-Sync überschreibt damit die Box-`tasks.json` mit dem PC-Stand. Deshalb vor jedem Sync zuerst die Box-`tasks.json` sichern, Ticket **AP268**.

**Schon passiert:** `ticket_tool new` gleicht mit der Box ab. Beim ersten Anlegen gingen 25 Tickets hoch, die am PC neuer waren (lokale Änderungen, die vorher nicht gepusht waren). Die Box-`tasks.json` ist also schon im neuen Abgleich, aber noch nicht migriert. Auch `auto_check.py` am PC läuft ab jetzt mit dem neuen Code (Auto-Tickets, Abgleich beim Pull).

**Folge-Tickets (29.09.):** AP267 Box einspielen (Max) · AP268 tasks.json vom Engine-Sync ausnehmen · AP269 Auto-Tickets auf der Box · AP270 Box-seitig atomar/unter Sperre · AP271 `updated` mit Zeitzone (vor 25.10.) · AP272 Wiedervorlagen als maschinenlesbare Liste.

## Jira-Umbau 29.09.2026: der ganze Tab als „Jira 2.0“ (Session baa48c56)

**Auftrag Max:** Tickets öffnen mit einem Board, links die Boards, oben Backlog/aktiver Sprint, Sprints planen und Tickets Wochen zuweisen, so nah an Jira wie möglich. Die alten Ansichten (Reihenfolge, Abläufe, Nach Zeitfenster) fliegen raus, die Tickets bleiben.

**Vorlage:** `research-scout` (Atlassian-Doku, 15 Claims im Research-Cache) plus die echten Atlassian-Produktbilder (Scrum-Board, Backlog mit Sprint-Container und Insights, Sprint-Board mit Insights, Burndown-Report), angesehen am 29.09.

**Entscheidungen Max (29.09.):** vier Boards + „Alle“ links, **ein** Sprint für alles (Mo–So), Dark-Theme des Labs (Struktur von Jira, Farben vom Lab), alle Extras rein (Insights, Übersicht, Timeline, Swimlanes + Epic-Filter), Prio-Farben wie bisher, neuer Token `--violet` für Epics, Design zuerst mit einer migrierten Kopie testen.

| Teil | Was |
|---|---|
| Sidebar | Projektkopf, Boards (Alle, Trading/Alpha, Infra/Box/NT8, Hub/Lab/Tools, Gründung/Privat) mit Zähler, Ansichten Übersicht, Timeline, Backlog, Board, Reports, Box-Abgleich unten, einklappbar |
| Kopf | Pfad „Tickets / Board / Ansicht“, Titel (auf dem Board der Sprintname + Ziel), rechts „noch X Tage“, Insights, **Sprint abschließen**, **+ Erstellen** |
| Filter | Suche (auch `prio:rot sprint:aktuell col:doing`), Zuständig-Avatare M/C/–, Epic ▾, Typ ▾, Dringend/Wartet/Auto, „Filter löschen“, auf dem Board **Gruppieren** (Keine/Epic/Zuständig) |
| Board | Spalten mit Zähler und Stunden, Karten wie Jira (Titel, Epic-Etikett, Typ-Icon, Key, Stunden, Prio-Pfeil, Avatar, Haken bei erledigt), Swimlanes, Ziehen zwischen Spalten und Lanes (Lane-Wechsel ändert Epic/Zuständig), ohne Sprint: Kanban über alles Offene mit Hinweis |
| Insights | rechts einblendbar: Sprint-Fortschritt (Stunden, sonst Anzahl), Mini-Burndown, Arten, Boards. Schließt sich mit dem Ticket-Panel aus |
| Backlog | einklappbare Sprint-Container (Datum, Zähler offen/in Arbeit/erledigt, Stunden gegen Kapazität mit „über“, **Sprint starten**/**abschließen**, ••• bearbeiten), Backlog darunter, „+ Ticket erstellen“ direkt in jedem Container (Enter legt an, Fokus bleibt), Häkchen + „In Sprint verschieben“, Ziehen zum Einplanen und Sortieren |
| Dialoge | Sprint starten (Name, Ziel, Kapazität, Zeitraum Mo–So fest), Sprint abschließen (offene Tickets in den nächsten Sprint, einen **neuen** Sprint oder den Backlog, danach Sprint-Report) |
| Übersicht | Kacheln erledigt/aktualisiert/angelegt (7 Tage) und fällig, Status-Donut, letzte Aktivität, Priorität, Arten, Epic-Fortschritt, Zuständig, Fällig-Liste |
| Timeline | 12 Wochen, Sprint-Zeile, Epics mit Kind-Tickets, Balken aus Start/Fällig, sonst Sprint-Zeitraum, nur Fällig = Raute, Heute-Linie, ◀ Heute ▶ |
| Reports | Sprint-Report, Burndown (rote Ist-Linie, graue Ideallinie), Velocity mit Schnitt-Linie |
| Ticket-Panel | Jira-Aufbau: Titel, Status + Erledigt oben, links Beschreibung, Fertig wenn, Schritte, Epic-Kinder, Wartet auf/Blockiert/Verknüpft, Aktivität mit Tabs Alle/Notizen/Verlauf; rechts Details (Zuständig, Sprint, Prio, Schätzung, Gebraucht, **Start**, **Fällig**, Epic, Labels, Board, Typ, Wann) |
| Backend | `ticket_lib`: Felder `start`/`due` (Datum, Start nicht nach Fällig), `sprint_close(carry_to="new")` legt den Folgesprint an; `app_server`: `/api/tickets/activity`, Sprint umbenennen, Test-Schalter `MAXLAB_TICKET_NOSYNC=1` (kein Box-Abgleich) |

**Geprüft:** Test-Instanz (Port 8766) auf einer migrierten Kopie im Scratchpad, echte `tasks.json` unberührt (Hash-Vergleich). Alle Ansichten bei 800 und 1440 px ohne Konsolenfehler, Status-Wechsel, Esc je Ebene, Epic-Filter, Inline-Create, Swimlanes, Insights/Panel-Ausschluss, Mehrfach-Verschieben, Sprint starten per Enter, Sprint abschließen in einen neuen Sprint, Ziehen Board/Lane/Backlog/Sortieren (per DragEvent, weil die Test-Maus im Browserfenster kein natives Ziehen auslöst). `test_ticket_lib` (neue Fälle: Datum, Abschluss „neu“, Umbenennen), `test_ticket_sync`, `lab_selftest` komplett gegen Test- und echtes Lab grün. `design-guard` vorab (17 Pflichtpunkte) und Abnahme (13 Befunde, alle eingearbeitet: Poll verschluckte Änderungen, Reports flackerten, aktive Filter nur per Farbe, Kartenfuß zu breit, Sprint abschließen sah aus wie Erstellen, Enter im Abschluss-Dialog, schmales Fenster, Timeline-Status, Klickflächen, Hover, Ellipsis).

**Bis zur Box-Migration (AP267)** zeigt das echte Lab die vier Boards mit 0 Tickets und keinen Sprint, alles steht unter „Alle Tickets“. Nach der Migration sind Boards, Epics und Sprint S2026-41 da.

## Stand 02.10.2026: neue Prio-Skala, Dringlichkeits-Sortierung, Backlog-Filter

**Auftrag Max:** Tickets neu bewerten, neue Prios „Sehr hoch“ (Live-Betrieb in den nächsten 3 Tagen gefährdet) und „Wichtig mit Datum“ (nicht sofort, aber mit Datum), Backlog auch gefiltert nach Dringlichkeit sortieren, Filter anpassen.

**Entscheidungen Max (02.10.):** 5 Stufen · Datum-Tickets bleiben fest auf ihrer Stufe (keine automatische Hochstufung, der Chip „Dringend“ fängt fällige ab) · Sortierung als Dringlichkeit immer aktiv, Drag-Rang nur Gleichstand-Brecher · Neubewertung direkt angewendet · Filter: Prio, „Dringend“ neu, Board im Backlog, Fälligkeit.

| Stufe | intern | Symbol | Farbe | heißt |
|---|---|---|---|---|
| Sehr hoch | `kritisch` | ⇈ als rote Pille | #e66767 | gefährdet den Live-Betrieb innerhalb von 3 Tagen |
| Hoch | `rot` (`orange` = Alt-Alias) | ↑ | #e66767 | wichtig, bald angehen |
| Wichtig (Datum) | `datum` | ◷ | `--blue` | wichtig, aber nicht sofort, braucht `due` (sonst „Datum fehlt“) |
| Mittel | `gelb` | = | `--accent` | normale Arbeit |
| Niedrig | `gruen` | ↓ | #4bbf8f | wenn Zeit ist |

Interne Schlüssel bewusst kompatibel gelassen (Box, `auto_check`, `promote_next`, alte Tickets schreiben weiter `rot`/`orange`/`gelb`/`gruen`).

**Dringlichkeit** (`ticket_lib.urgency_key`, gleich im Lab `byUrgency`): Stufe → nicht blockiert vor blockiert → Fällig-Datum aufsteigend (ohne Datum hinten) → manueller Rang. Gilt für Backlog, Sprint-Container, Board-Spalten, `ticket_tool.py backlog/find`. Ziehen in derselben Liste zeigt die Einfügelinie nur bei gleicher Stufe und gleichem Datum, sonst Hinweis.

**Filterzeile:** Suche (jetzt auch `prio:hoch|sehrhoch|datum|mittel|niedrig`), Avatare, **Prio ▾**, Epic ▾, Typ ▾, **Board ▾** (synchron mit der Sidebar), **Fällig ▾** (Überfällig / Diese Woche / Ohne Datum), **Dringend** = Sehr hoch + Hoch + Datum fällig in ≤ 7 Tagen (auch der Zähler am Tab), Wartet, Auto. Backlog-Zeile hat einen festen Fällig-Slot.

**Neubewertung (145 offene Tickets):** 2 Sehr hoch (AP284 RiskGuard-Tagesbasis, AP214 E8-150k-Setup), 21 Hoch, 21 Datum, 78 Mittel, 23 Niedrig. 56 Tickets geändert, auf die Box geschrieben (`--push-tasks`).

**Geändert:** `ticket_lib.py` (PRIOS, `norm_prio`, `urgency_key`, `PRIO_LABEL`), `ticket_tool.py` (`--due/--start`, Labels), `ticket_migrate.py`, `app_server.py`, `auto_check.py` (Glocke: Sehr hoch = rot, Hoch = gelb), `lab_ui/tickets_board.js/.css`, `lab.js` (PRIODEF), Skills `/ticket`, `/sprint`, `/briefing`. Backups `*.bak_prio5`. Lab-Server neu gestartet (job-frei). `lab_selftest` grün, `test_ticket_lib` mit denselben 4 Fehlern wie vorher (datumsabhängig, nicht durch diese Änderung), `test_ticket_sync` grün. `design-guard` vorab (25 Punkte) und Abnahme (4 Befunde, alle eingearbeitet: Alt-`orange` zeigte im Detail-Select „Sehr hoch“, Fällig-Slot zu schmal für „überfällig“, 7-Tage-Fenster über die Zeitumstellung einen Tag zu kurz, Pillen-Padding). Offen für Max: Fälligkeit auch auf den Board-Karten zeigen?

**Offen:** Box-seitiger Code (`ticket_lib` auf der Box) kennt die neuen Stufen erst nach dem nächsten Engine-Sync, bis dahin zeigt nur das PC-Lab sie richtig an. Die Charta (Abschnitt Tickets) nennt die Prio-Skala noch nicht, Regel trägt Max selbst ein.

## Aus der CLAUDE.md (05.10.2026): Sprint-Regeln und Ticket-Tracker

Aus der CLAUDE.md übernommen (Regel Max, 29.09.2026 und 06.09.2026), damit der Abschnitt dort auf einen Einzeiler schrumpfen kann.

### Wir arbeiten in Sprints, Max plant sie selbst (Regel Max, 29.09.2026)

Tickets laufen seit 29.09. im Strategy Lab im Jira-Aufbau (Boards, Backlog, Board, Reports), Sprint = eine Woche **Mo bis So**.

- **Max plant jeden Sprint selbst.** Er holt sich die Tickets aus dem Backlog und entscheidet, was in welche Woche kommt. Die Prio ist die Bewertung, mehr braucht es dafür nicht.
- **Neue Tickets landen immer im Backlog**, egal ob von Claude, `ticket_tool.py`, Auto-Check oder Box. Claude plant nie von sich aus Tickets in einen Sprint, startet oder schließt keinen Sprint und schlägt kein Planning vor.
- **`/sprint` nur auf Zuruf.** Ruft Max ihn auf, darf Claude einen Vorschlag machen, geschrieben wird erst nach seinem OK.
- Ein leerer Sprint-Container (z.B. S2026-41 aus der Migration) ist kein Planning und bleibt leer, bis Max ihn füllt.

(Überholt seit 29.09.2026, siehe oben: die Formulierung in Abschnitt 5, Planning gehöre sonntags zum Ablauf und `/sprint` schlage von sich aus einen Sprint vor. Heute gilt: Max plant selbst, `/sprint` nur auf Zuruf.)

### Ticket-Tracker: zweiseitig, Box ist die Quelle der Wahrheit (seit 06.09.2026)

- Ablage: `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (Feld `ap_id`).
- **Seit 06.09.2026 zweiseitig:** Max legt Tickets auch direkt auf der Box an. `tasks.json` wird bei jedem `inbox_tool.py --pull` mitgezogen und mit `--push-tasks` zurückgeschrieben, **die Box ist die Quelle der Wahrheit**.
- Der Abgleich überschreibt nie blind: `.bak` vorher, eine Nummernkollision wird gemeldet statt aufgelöst.
- **Vor dem Anlegen eines neuen Tickets immer erst `--pull`.** Vorfall 03. bis 06.09.2026: Nummernkollision AP121 bis AP127 (siehe [[Strategie-Logbuch]]).

## Start-Prompt für die Bau-Session (PC oder Laptop)

> Baue das Ticket-Board im Strategy Lab nach `Projekte/Ticket-Board (Jira-Stil).md`, Phase 0 und 1. Auftrags-Typ `ui` (Kette design-guard). Vorher `session-guard`, `inbox_tool.py --pull`. Erst Phase 0 (Statuswerte, alle Leser/Schreiber von `tasks.json`), Ergebnis kurz zeigen und Spalten-Zuordnung mit mir abstimmen, dann bauen. Nichts umbenennen, nur additive Felder. Danach `lab_selftest.py`, `--push-tasks`, Daily Note.
