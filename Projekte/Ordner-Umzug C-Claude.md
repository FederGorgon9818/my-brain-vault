---
date: 2026-10-31
tags: [projekt, setup, ordner, claude-code, terminal]
status: Umzug und Aufräumen erledigt (31.10.2026), Aufräum-Check läuft sonntags, offen nur Brücken-Abbau (Schritt 7) und Engine-Pfade nach und nach
---

# 📁 Ordner-Umzug nach C:\Claude (31.10.2026)

**Auftrag Max 31.10.2026:** Weg von der Desktop-App, Claude künftig im Terminal. Dafür alles, was mit Claude zu tun hat (Vault, Projekte, Gewerbe/Steuer, Be Obsessed), übersichtlich unter `C:\Claude`. Große Daten sollten weder lange dauern noch Tokens kosten.

## Entscheidungen Max (31.10.)

| Frage | Entscheidung |
|---|---|
| Methode | Echt umziehen, am alten Ort bleibt eine Brücke (Junction) |
| Marktdaten | trading-data komplett mit (gleiches Laufwerk = nur Umbenennen, eine Sekunde) |
| Extras | Be Obsessed Videos, Gewerbe + Steuer, heimweg ins Archiv. Desktop-Kram bleibt. |
| Vault-Name | bleibt „My Brain" |

## Zielbild

Karte mit allen Ordnern: `C:\Claude\README.md`. Kurz: `My Brain\` (Vault), `projekte\` (trading-data, hub, webde-mail, whoop-mcp, token-tracker, smart-router), `content\` (Be Obsessed), `buero\` (Gewerbe, Steuer), `archiv\` (heimweg, ohne Brücke), `_umzug\` (Skripte).

Bleibt am alten Ort: `~\.claude` und `.claude.json` (Claude Code), `Documents\NinjaTrader 8` (NT8), Spiele, OneDrive, Desktop.

## Warum Brücken statt alles umschreiben

Bestandsaufnahme 31.10.: feste Pfade auf die alten Orte stecken in 1.192 Stellen in 898 Engine-Dateien, 57 Stellen in 31 Dateien unter `.claude` (Hooks, Agents, Skills, Workflows), 9 im Hub, in den zwei Windows-Tasks (`MaxLab Auto-Check`, `MaxLab Live Sync`), im Mail-MCP, in Obsidian, in den Vault-Worktrees und im Claude-Gedächtnis (Schlüssel = Ordnerpfad). Mit Brücke laufen alle weiter, umgestellt wird danach Schritt für Schritt.

Die Hooks erkennen Engine- und Hub-Dateien über `/engine/` bzw. `/hub/` im Pfad, die Sperren greifen also auch am neuen Ort. `_common.py` sucht Engine und Hub seit 31.10. zuerst unter `C:\Claude\projekte\...`, dann am alten Ort. `_LIVE_BASE` in `guard_bash.py` ist der Pfad **auf der Box** und bleibt.

## Phase 1: Umzug (Skript, Max startet es)

Skripte in `C:\Claude\_umzug\`: `umzug.ps1`, `rueckweg.ps1`, `umzug_lib.ps1`, `umzug_config.py`, Plan `umzug_plan.json` (12 Ordner, 11 mit Brücke, Vault zuletzt).

Ablauf im Skript: Vorcheck (Quelle da, Ziel frei, gleiches Laufwerk, keine blockierenden Programme) → Tasks pausieren → Ordner per Umbenennen verschieben → Brücke am alten Ort → `git worktree repair` im Vault → Claude-Gedächtnis: neuer Schlüssel `C--Claude-My-Brain` bekommt eine Brücke auf den alten `memory`-Ordner (alte Sessions bleiben unter dem alten Schlüssel, so zählt der Token-Tracker nichts doppelt) → Configs (`.claude.json` Projekt-Einträge kopiert, Mail-MCP, githubRepoPaths, `settings.json` additionalDirectories, Obsidian-Vault-Pfad, Sicherung in `_umzug\backup`) → Tasks auf neuen Pfad, wieder an.

Sicherheit: es wird nie ein echter Ordner gelöscht, nur Brücken nach Prüfung. Verschieben nur per Umbenennen auf demselben Laufwerk (sonst Abbruch, nie Kopie). Klemmt ein Ordner, dreht das Skript alles bereits Verschobene zurück.

**Getestet 31.10.** an Wegwerf-Ordnern (Scratchpad, mit Git-Repo und Worktree, Ordnername mit Leerzeichen): Trockenlauf ändert nichts, gesperrte Datei führt zu Abbruch mit vollständigem Zurückdrehen, echter Lauf mit identischen Inhalten am neuen Ort, Lesen und Schreiben über die Brücke, Worktree auf neuen Pfad repariert, zweiter Lauf wird abgelehnt, Rückweg stellt alles identisch wieder her. 0 Fehler. Config-Umsteller an Kopien der echten Dateien: nur die gemeinten Felder geändert, Rückweg byte-gleich. Trockenlauf mit echtem Plan: alle 12 Ordner planbar, Blocker erkannt (Claude, offener Editor mit Gewerbe-Datei, Mail-MCP).

Der Umzug kann nicht aus einer Desktop-Session laufen: Windows sperrt den Ordner, in dem die Session läuft.

Erster Startversuch 31.10. 16:28: sauber abgebrochen, nichts verändert (Claude-App offen, Notepad mit `Mail an Dr. Hahn.txt`, Live-Sync-Lauf). Seitdem wartet das Skript nach dem Pausieren der Tasks bis 3 Minuten auf laufende Auto-Check-/Live-Sync-Prozesse, statt abzubrechen.

### Anleitung für Max

1. Claude Desktop ganz beenden (auch im Tray), Obsidian, VS Code, Hub und offene Editoren schließen.
2. Normale PowerShell öffnen (kein Admin).
3. Trockenlauf: `powershell -ExecutionPolicy Bypass -File C:\Claude\_umzug\umzug.ps1 -DryRun`. Erwartet: 12 Zeilen „plane:" und „Trockenlauf fertig". Steht „LAEUFT NOCH:" da, das Programm schließen (notfalls Task-Manager) und wiederholen.
4. Echt: dieselbe Zeile ohne `-DryRun`. Erwartet am Ende „FERTIG". Bei „Abgebrochen, Stand wie vorher" ist nichts passiert, die Zeile davor sagt, welcher Ordner klemmt.
5. `cd "C:\Claude\My Brain"`, dann `claude`, und als Erstes „Umzug Phase 2" sagen.

Rückweg jederzeit: `powershell -ExecutionPolicy Bypass -File C:\Claude\_umzug\rueckweg.ps1`.

## Phase 2: erste Terminal-Session (Claude)

- [ ] Gedächtnis geladen (MEMORY.md im Kontext), Hooks melden sich, `_common.ENGINE` zeigt auf `C:\Claude\projekte\trading-data\engine`.
- [ ] `git status` und `git worktree list` in Vault, trading-data, hub.
- [ ] Selbsttests: `test_chain.py`, `test_konto_gate.py`, `test_urteil_gate.py`, `test_sync_gate.py`.
- [ ] Tasks: `Get-ScheduledTask "MaxLab*"` zeigt neuen Pfad und Ready, Auto-Check einmal von Hand anstoßen.
- [ ] MCP: webde-mail verbindet. `.mcp.json` (whoop) auf neuen Pfad.
- [ ] Obsidian öffnet „My Brain" aus `C:\Claude`.
- [ ] Hub und Lab-Server starten vom neuen Ort.
- [ ] Pfade umstellen: CLAUDE.md, `.claude/launch.json`, `knowledge_router.py`, Agents, Skills und Workflows (die 57 Stellen), `hub_config.json`, Obsidian-Plugin `token-status`, Memory-Einträge mit Pfaden.
- [ ] Engine-Pfade (1.192 Stellen) bleiben über die Brücke, Umstellung nach und nach (eigenes Ticket).
- [ ] Hinweis: alte Desktop-Sessions liegen unter dem alten Schlüssel, `claude --resume` im neuen Ordner zeigt sie nicht.

Verwandt: [[Tech-Stack]], [[Hooks-Referenz]], [[Daily Notes/2026-10-31]].

## Ergebnis Umzug (31.10.2026, 16:32)

Lauf sauber durch: 12 Ordner verschoben, 11 Brücken, 29 Worktrees repariert, Gedächtnis verlinkt (`C--Claude-My-Brain`, `C--Claude-projekte-trading-data`), Configs umgestellt, beide Tasks auf `C:\Claude\projekte\trading-data\engine\*.vbs` und wieder an. Hooks finden Engine und Hub am neuen Ort. Phase-2-Prüfung: Git in allen drei Repos ok, Selbsttests liefen vor dem Umzug grün.

## Phase 3: Aufräumen und Ablage-Regeln (Analyse 31.10.2026, Vorschlag)

### Bestand (Messung 31.10., Skript im Scratchpad)

C:\Claude: 18,46 GB, 56.290 Dateien. Größte Posten: Engine 5,71 GB (23.614 Dateien), Vault-Worktrees 2,20 GB, Marktdaten-Exporte 3,19 GB, Be-Obsessed-Rohvideo 2,31 GB, heimweg 3,27 GB.

| Fund | Menge | Bewertung |
|---|---|---|
| Vault-Worktrees gemergt und sauber | 26 von 29, 2,12 GB | weg, 3 offene bleiben |
| Engine-Wurzel `.py` | 221: 91 Kern (importiert oder von Hooks/Skills/Tasks/Hub aufgerufen), 72 nur in Notizen erwähnt, 58 nirgends verwendet (56 davon älter als 21 Tage) | Kern bleibt, 58 ins Engine-Archiv |
| Engine `_scratch_*` | 65 Ordner, 2,57 GB; 31 seit über 21 Tagen unberührt (0,17 GB, 2.647 Dateien) | alte ins Archiv, außer in Notizen verlinkte |
| Engine `.bak`-Dateien in der Wurzel | 241 (38,1 MB) | ins Archiv |
| Engine-Logs älter als 30 Tage | 69 | ins Archiv |
| Engine `.app_profile` | 0,75 GB, Browser-Profil der alten `archiv/app.py` (Juli) | löschen (nur mit OK) |
| `nt8_staging_*` in der trading-data-Wurzel | 18 Ordner, 0,42 GB; 16 davon alte Deploy-Abende | in einen Ordner `nt8_staging\`, alte ins Archiv |
| Lose Dateien trading-data-Wurzel | 12 (Export-/Probe-Skripte, alte JSONs) | nach `tools\` bzw. Archiv |
| Vault-Rohdaten `Quantpad Data`, `DATA` | 31,6 MB, im Git | raus aus dem Vault, zu den Marktdaten |
| Projekt-Notizen | 94, davon 12 fertig/entschieden/alte Anleitung, 11 Wege-Karten | 12 nach `Archiv/` |
| Außerhalb | 13 MultiCharts-`.MCReport` lose in Documents, leerer Ordner `C:\Users\maxlk\Claude`, `Pfad Strategy Lab.txt` auf dem Desktop mit altem Pfad | Reports ins Archiv, Rest bereinigen |

### Zielstruktur

```
C:\Claude\
├── README.md                 Karte + Ablage-Regeln (die eine Seite zum Nachschlagen)
├── My Brain\                 WISSEN: Notizen, Entscheidungen, Logbuch, CLAUDE.md, Hooks, Skills, Agents
│   ├── Inbox\  Projekte\ (nur aktive)  Bereiche\  Ressourcen\  Daily Notes\  Archiv\  Anhänge\  Kontext\
├── projekte\                 CODE: je Repo oder Tool ein Ordner
│   ├── trading-data\
│   │   ├── engine\           Kern bleibt flach (Box-Sync, Golden Master, feste Pfade)
│   │   │   ├── _scratch_*\   nur laufende Rechnungen (nach 21 Tagen ohne Änderung ins Archiv)
│   │   │   └── archiv\       einmal\, scratch\, backups\, logs\ (alles Erledigte der Engine)
│   │   ├── nt8_staging\      Deploy-Pakete je Abend: JJJJMMTT_thema\
│   │   ├── exported_data*\   Marktdaten (Engine liest dort)
│   │   ├── tools\            Export- und Probe-Skripte
│   │   └── archiv\           alte Deploy-Pakete
│   ├── hub\  webde-mail\  whoop-mcp\  token-tracker\  smart-router\
├── content\                  BE OBSESSED: Rohvideo, Schnitt, Tests
├── buero\                    GEWERBE + STEUER: Belege, Nachweise, Steuerberater, Steuerjahre
├── archiv\                   GANZE erledigte Dinge: heimweg, Umzug, alte MultiCharts-Reports
└── _umzug\                   bis Phase 3 fertig, danach nach archiv\
```

Regel fürs Archiv: **ganze Sachen** nach `C:\Claude\archiv\`, **Teile eines Projekts** in dessen eigenes `archiv\` (bleibt im Repo-Zusammenhang).

### Ablage-Workflow: wohin mit etwas Neuem (von oben nach unten, erster Treffer gilt)

1. Wissen, Entscheidung, Bericht, Anleitung, Idee → **My Brain** (roh: Inbox, mit Ziel: Projekte, laufend: Bereiche, Nachschlagen: Ressourcen, Tageslog: Daily Notes).
2. Rechnung oder Test für eine konkrete Frage → **`engine\_scratch_<AP>_<thema>\`**. Das Ergebnis gehört als Notiz in den Vault, der Ordner ist nur Werkbank.
3. Code, der bleibt → **`projekte\<repo>\`**. Engine-Kern in `engine\`, neues Tool = neuer Ordner unter `projekte\` mit README.
4. Deploy-Paket für NT8 → **`trading-data\nt8_staging\<JJJJMMTT>_<thema>\`**.
5. Marktdaten, Exporte, Parquet → **`trading-data\exported_data*\`**, nie in den Vault.
6. Beleg, Rechnung, Steuer, Behörde → **`buero\Gewerbe\…`** bzw. **`buero\Steuer\<Jahr>\`**.
7. Video, Schnitt, Content → **`content\`**. Bilder für Notizen → `My Brain\Anhänge\`.
8. Sicherung vor einer Änderung (`.bak`) → neben die Datei, der Aufräum-Check schiebt sie nach 14 Tagen ins Archiv.
9. Fertig → Projekt-Notiz nach `My Brain\Archiv\`, ganzes Projekt nach `C:\Claude\archiv\<name>\`.

### Bewusst nicht

- **Engine-Kern in Unterordner zerlegen:** 1.192 feste Pfade, Box-Sync mit gleichem Layout, Golden Master. Hoher Bruch, kein Mehrwert beim Finden.
- **Marktdaten vom Code trennen:** gleicher Grund, die Engine liest relativ zu sich selbst.
- **Ordner nummerieren (10_, 20_):** bei sechs Ordnern unnötig, nervt im Terminal.
- **Die 72 nur in Notizen erwähnten Studien-Skripte verschieben:** die Notizen verweisen per Name darauf. Später möglich, wenn die Verweise automatisch mit umgeschrieben werden.

### Umsetzung in Schritten (Vorschlag, Reihenfolge nach Risiko)

1. **Pfade auf neu (Rest Phase 2):** CLAUDE.md, Agents, Skills, Workflows, Hub-Config, `.mcp.json` (whoop), `launch.json`, Memory-Einträge, Desktop-Datei `Pfad Strategy Lab.txt`. Sonst schreiben neue Sessions weiter alte Pfade.
2. **Ohne Risiko:** 26 gemergte Worktrees entfernen, leeren Ordner `C:\Users\maxlk\Claude` löschen, MCReports nach `archiv\`.
3. **Engine entrümpeln (nur verschieben, nichts löschen):** 58 Einmal-Skripte, 241 `.bak`, alte Scratch-Ordner (verlinkte bleiben), 69 alte Logs → `engine\archiv\…`; 16 alte Deploy-Pakete → `trading-data\archiv\`, die zwei neuesten nach `nt8_staging\`; lose Wurzel-Skripte → `tools\`. Davor und danach Golden Master + `lab_selftest.py`.
4. **Vault:** 12 fertige Projekt-Notizen nach `Archiv/` (Wikilinks lösen über den Namen auf), `Quantpad Data` + `DATA` zu den Marktdaten.
5. **Löschen, nur mit OK:** `.app_profile` (0,75 GB), `heimweg` (3,27 GB).
6. **Regeln festschreiben:** Ablage-Workflow in `C:\Claude\README.md`, zwei Zeilen CLAUDE.md, Router-Stichwort, Aufräum-Check (Skript, berichtet wöchentlich: Worktrees, alte Scratch, `.bak`, Logs, fertige Projekte, lose Dateien).
7. **Brücken abbauen**, sobald nichts mehr auf den alten Pfad zeigt. Die trading-data-Brücke bleibt wegen der Engine-Pfade länger.

### Entscheidung Max (31.10.) und Ergebnis

Max: Schritte 1 bis 4 umsetzen, nur `.app_profile` löschen (heimweg bleibt im Archiv), wöchentlicher Aufräum-Bericht.

- **Pfade (Schritt 1):** 84 Stellen in 44 Dateien auf `C:\Claude` (CLAUDE.md, 14 Agents, Skills inkl. Steuer-Skript, Workflows, Hook-Router, Tests, Gedächtnis, `.mcp.json`, `launch.json`, `Belegordner 2026`, `Steuer-Werkzeuge`, Desktop `Pfad Strategy Lab.txt`), dazu `hub_config.json` (3 Pfade, `design-guard` begründet ausgelassen: reine Pfadänderung). **Bewusst alt gelassen:** Box-Pfade (`guard_bash._LIVE_BASE`, `test_sync_gate.py`, `box-ops`), weil die Box intern weiter `C:\Users\maxlk\Projects\trading-data` nutzt; Laptop-Rückfall in `_common.py`; Daily Notes, Logbuch und Projekt-Berichte (Geschichte); Engine- und Hub-Code (Brücke). Selbsttests danach grün: test_chain 112/0 (jetzt mit neuen Pfaden, die Sperren greifen am neuen Ort), test_konto_gate 52, test_urteil_gate, test_sync_gate, test_book_sync_hook.
- **Kleinkram (Schritt 2):** 23 gemergte, saubere Worktrees entfernt (1,87 GB). 6 bleiben: 4 mit Änderungen oder offenen Commits (affectionate-pascal, dazzling-shirley, elated-chaum, objective-wright), 2 geschützt (Steuererklärung angepinnt und heute aktiv, Worktree-Verhalten angepinnt). Leerer Ordner `C:\Users\maxlk\Claude` gelöscht, 13 MultiCharts-Reports nach `archiv\multicharts-reports`.
- **Engine (Schritt 3), vorher Verweis-Prüfung:** verschoben wurden nur Dinge, auf die kein Code, Hook, Skill, Ticket oder keine Notiz zeigt. 47 Einmal-Skripte, 241 `.bak`, 69 Logs, 10 alte Scratch-Ordner nach `engine\archiv\`; 7 Export-/Probe-Skripte nach `trading-data\tools\`, 3 Alt-JSONs nach `trading-data\archiv\`. `.app_profile` gelöscht (0,75 GB). Engine-Wurzel: 772 → 415 Dateien. **Nicht verschoben, weil benutzt:** alle 18 `nt8_staging_*` (Konten-Code, `book_state.json`, NT8-Port-Status lesen daraus; Konvention `nt8_staging_<datum>_<thema>` bleibt), 18 alte Scratch-Ordner (z.B. `_scratch_ap204_kal` von `tempo_plan.py`, `_scratch_juli_nacht` vom Box-Sync-Skript), 11 Einmal-Skripte (z.B. `dev_mcp.py` aus `dev_agent.py`, `goal_after_fixes.py` aus `gen_edge_ref.py`, `make_icon.py` aus dem Hub-Build).
- **Vault (Schritt 4):** 6 wirklich abgeschlossene Projekt-Notizen nach `Archiv/` (Cushion-Frac, News Mean Reversion, Deploy-Abend 22.10., Einrichtung 16.10., Live-Stellung 15.10., Friedhof-Nachlauf). Die anderen 6 aus der ersten Zählung laufen noch (Alpha-Playbook AP457 bis AP480, Kombi-Suche AP310, Queue-Nachschub, beide Wochenend-Prüfungen, Be-Obsessed-Content-Plan als gültige Regel) und bleiben. `Quantpad Data` + `DATA` nach `C:\Claude\archiv\vault-rohdaten\` statt zu den Marktdaten: alte Analysen vom Juli/August, und die Engine liest `exported_data` per Suchmuster. Dabei gefunden: 23 lose Dateien in der Vault-Wurzel seit Juli (17 byte-gleiche Doppel davon plus 6 leere Reste) → `archiv\vault-rohdaten\_wurzel-reste\`.
- **Platz frei:** 2,62 GB (Worktrees + `.app_profile`). Alle 408 Bewegungen stehen in `C:\Claude\_umzug\phase3_moves.json`, Rückweg `python C:\Claude\_umzug\phase3_aufraeumen.py --undo`.
- **Regeln (Schritt 6):** Karte und Ablage-Workflow in `C:\Claude\README.md`, Absatz in CLAUDE.md (Abschnitt Vault-Struktur), Router-Stichworte (Ablage, wo kommt, aufräumen). Aufräum-Check `.claude/scripts/aufraeum_check.py` (Bericht, `--ticket`, `--apply` nur nach OK, Log `engine\archiv\aufraeum_log.jsonl`), Task `MaxLab Aufraeum-Check` sonntags 12:00 (pythonw, holt verpasste Läufe nach), Eintrag im Hub-Roster. Getestet: Bericht nach dem Aufräumen überall 0, `--apply` an einer künstlich gealterten Test-`.bak` (gefunden, verschoben, protokolliert, Testspuren entfernt).
- **Offen:** Brücken abbauen (Schritt 7) erst, wenn kein Verweis mehr auf die alten Pfade zeigt; Engine-Pfade (1.192 Stellen) nach und nach; 6 verbliebene Worktrees prüft Max oder die jeweilige Session.

### Gegenprüfung und Nachkorrektur (31.10.2026 abends)

- **Golden Master (engine-regression-tester):** grün. Fingerprint unverändert, alle 12 Referenz-Backtests bitgleich, Kanarien gestorben wie erwartet, 9/9 Selbsttests, keine verschobene Datei vermisst.
- **verdict-auditor: Stempel „nichts gebrochen" war voreilig.** Fehler von mir: `.bak` und `.log` wurden pauschal verschoben, ohne Verweis-Suche, und die Verweis-Suche schloss `_scratch*` aus (Abhängigkeiten zwischen Scratch-Ordnern unsichtbar). Folgen: `test_erstfassung.py` (liest zwei `book_state.json.bak-*`) brach mit FileNotFoundError, der AP412-Nachweis `_scratch_ap412/diff_vs_bak.py` fand `asian.py.bak-20261027-ap412` nicht, drei Regressionstests (`test_overfit`, `test_rvol_clock`, `test_scratch_register`) lagen als „Einmal“ im Archiv und liefen dort nicht.
- **Behoben:** Nachprüfung jeder einzelnen Bewegung gegen allen lebenden Code inklusive Scratch-Ordner und Daten-JSON. 48 Dinge zurückgeholt (`phase3_zurueckgeholt.json`): 45 genannte Dateien/Ordner (u.a. 24 `.bak`, 5 Logs, 10 Studien-Skripte, `_scratch_money_model`, `_scratch_money_stats`) plus die 3 Tests. 5 Fehlalarme blieben (`DATA` als Variablenname, `sweep.py` in `cage_policy_sweep.py`, zwei Export-Skripte, die zusammen in `tools\` liegen, eine Probe-Ausgabe). Danach: `test_erstfassung --ohne-sims` 69/69 grün, die drei Tests exit 0, AP412-Datei wieder da. Verschoben bleiben 360.
- **Skill-Texte:** `queue` und `wochenende` nennen jetzt PC- und Box-/Laptop-Pfad getrennt.
- **Aufräum-Check gehärtet:** `.bak`/`.log` nur ohne Verweis (Code, Daten-JSON, Scratch-Skripte); Worktrees gemergt gemessen im Worktree selbst (abgekoppelte mit eigenen Commits bleiben), gesperrte und ohne Metadaten bleiben; die zwei angepinnten Worktrees per `git worktree lock` geschützt; `--apply` verschiebt nur die Vorschlagsliste, die Max gesehen hat (`engine\archiv\aufraeum_vorschlag.json`, höchstens 14 Tage alt, jeder Eintrag neu geprüft); vor dem Ticket der Box-Pull wie im Auto-Check (AP-Nummern), ohne Pull kein Ticket; git ohne Fenster. Test 13/13 grün, inkl. echtem Ticket gegen eine Kopie der Ticket-Dateien (AP-Nummer vergeben, Backlog, kein Duplikat beim zweiten Lauf) und `pythonw`-Lauf.
- **Lehre:** „Nicht importiert und nirgends genannt“ ist für Tests und Sicherungen das falsche Kriterium, und eine Verweis-Suche, die Scratch-Ordner ausnimmt, ist blind für die Hälfte der Abhängigkeiten.
- **Vorschlag offen (Max):** die drei Tests wieder in die Selbsttest-Liste des `engine-regression-tester` aufnehmen (waren am 04.10. Teil der Batterie).
