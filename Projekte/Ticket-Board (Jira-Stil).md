---
tags:
  - projekt
  - bereich/softwareentwicklung
  - strategy-lab
  - tickets
erstellt: 2026-09-28
status: geplant (Bau aus PC-/Laptop-Session, Engine nötig)
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
python ticket_tool.py new --board trading --type story --prio orange --title "..." --why "..." [--epic AP250] [--hours 3]
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

## Start-Prompt für die Bau-Session (PC oder Laptop)

> Baue das Ticket-Board im Strategy Lab nach `Projekte/Ticket-Board (Jira-Stil).md`, Phase 0 und 1. Auftrags-Typ `ui` (Kette design-guard). Vorher `session-guard`, `inbox_tool.py --pull`. Erst Phase 0 (Statuswerte, alle Leser/Schreiber von `tasks.json`), Ergebnis kurz zeigen und Spalten-Zuordnung mit mir abstimmen, dann bauen. Nichts umbenennen, nur additive Felder. Danach `lab_selftest.py`, `--push-tasks`, Daily Note.
