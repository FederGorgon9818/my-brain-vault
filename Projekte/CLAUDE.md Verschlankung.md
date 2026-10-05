---
tags:
  - projekt/meta
  - claude/prozess
erstellt: 2026-10-05
status: Phase 1 gebaut (05.10.2026), Schattenbetrieb läuft
---
# ✂️ CLAUDE.md Verschlankung

⬅️ [[Hooks-Referenz]] · [[Arbeits-Workflow (Auftrags-Typen)]] · [[Agent-Architektur Token-Optimierung]]

## Ziel

CLAUDE.md von 57 KB (~15.000 bis 17.000 Tokens, geht in **jede Session und jeden Subagent**) auf 15 bis 18 KB bringen. Ersparnis ~11.000 bis 12.000 Tokens je Session und je Subagent. **Bedingung von Max: nichts darf verloren gehen, und alles muss trotzdem erkannt werden, so wie Max redet.**

## Die zwei Absicherungen von Max (05.10.2026, nicht verhandelbar)

1. **Alles, was jede Antwort heute am Ende macht, bleibt in der CLAUDE.md, wörtlich und vollständig:**
   - Kurzfassung am Ende, ohne Code-Bezeichnungen (Regel 22.09.)
   - Modell-Empfehlung (sonnet/haiku/opus/fable)
   - `/clear` ja oder nein
   - Daily-Note-Bestätigung (was wurde eingetragen, Regel 09.09.)
   - aktives Erinnern an Sessionwechsel, wenn ein Themenblock fertig ist
   - **Schlusszeilen-Check (beschlossen Max 05.10.):** `on_stop.py` prüft die letzte Antwort. Hat die Session in diesem Zug Dateien geändert, müssen Modell-Zeile, `/clear`-Zeile und Daily-Note-Zeile drinstehen, sonst einmal zurück mit Hinweis. Bei reinen Frage-Antworten nur Modell + `/clear`. Erkennung locker (Wörter „Modell“, „/clear“ oder „frische Session“, „Daily Note“), nie zweimal hintereinander blocken, Fehler im Hook blockieren nie. Eigener Selbsttest mit echten Schlussblöcken aus alten Antworten.
2. **Der Stichwort-Router wird an Max' echter Sprache getestet, nicht an sauberen Stichworten.** Grundlage: Auswertung von 945 eigenen Prompts der letzten 30 Tage (Abschnitt „Sprachbefund“). Jeder Trigger braucht Testfälle mit Diktier-Varianten, analog `test_chain.py`. Ohne grünen Test wird nichts aus der CLAUDE.md gestrichen.

## Sprachbefund (945 Prompts, 30 Tage)

- **Diktiert, lang, voller Füllwörter:** Median 207 Zeichen; „quasi“ 561×, „ähm“ 461×, „sozusagen“ 349×, „äh“ 214×. Router muss Füllwörter ignorieren.
- **„Cloud“ heißt fast immer Claude:** „Cloud-Desktop“, „Cloud Code“, „Cloud MD“, „Cloud im D-Fall“, „Claude MD Fall“, „Claude in D-File“. **„cloud“ darf nie den GitHub-Router auslösen**, sondern zählt als Claude/CLAUDE.md.
- **„hab“ ist fast nie Hub**, sondern „habe“. Hub-Trigger nur auf „Hub“ selbst und Wendungen wie „im Hub“, „Baue im Hub“.
- **„Juni-Modus“** kam als Verhörer für Juli-Modus vor. Juli-Trigger: `jul[iy]|juni` + `modus`, mit und ohne Bindestrich oder Leerzeichen.
- **Tickets als Einstieg:** „AP 72“, „AP73“, „Kümmer dich um AP73“. Ticketnummer mit oder ohne Leerzeichen → Router lädt den Tickettitel und routet dessen Stichworte mit.
- **Kurze Folge-Prompts ohne Stichwort** („ja“, „mach weiter“, „okay passt“, „FERTIG“): 518 von 945 Prompts treffen kein Thema. Das ist ok, weil das Thema im Kontext der Session schon geladen ist. Der Router muss nur beim **ersten** Auftauchen in einer Session feuern.
- Echte Formen je Thema (Häufigkeit): Developer/Workbench 39, Gate/Next-Week/Wochenende 217, Discovery/Queue/Runner/Inbox 112, Telegram/RiskGuard/„Risk Guard“/Tagesstopp 67, 50k/150k/E8 150k/„neuen Account“ 66, Laptop/git/push 110 (ohne „cloud“!), Mail/Rechnung/Belege/Postfach/„web.de“ 131, Sprint/Backlog 18, tot/Friedhof/Urteil 22, Box/VPS/NT8/Ninja/SSH 277, Buch/Portfolio/Bein 315.

## Ebenen (wer lädt was wann)

| Ebene | geladen | Inhalt |
|---|---|---|
| E1 CLAUDE.md | immer | Verhaltensregeln, Schlusszeilen, harte Nie-Regeln als Einzeiler, **Wegweiser-Tabelle Thema → Notiz** (Rückfall, wenn Hooks nicht laufen, z.B. Cloud) |
| E2 Stichwort-Router (`on_prompt.py`) | erstes Stichwort je Session | 1 bis 3 Kernzeilen + „lies Notiz X“ |
| E3 Skills | bei Aufruf | Abläufe: neues Konto/Firma, RiskGuard/Telegram |
| E4 Vault-Notizen | bei Bedarf | Warum, Geschichte, Stand |
| E5 Hooks auf Pfade/Befehle | bei Datei/Befehl | Engine liegt außerhalb des Vaults, Pfad-Regeln greifen dort nicht sicher |
| E6 `.claude/rules` mit `paths` | beim Lesen der Datei | nur Vault-Dateien, ergänzend |

## Abschnitt → Ziel

| Abschnitt | Ziel | vorher übertragen (steht sonst nur in CLAUDE.md) |
|---|---|---|
| Wer ist der User | E1 kurz, Zahlen → [[Unternehmensgründung Entscheidung]] | BOS-Reserve-Kaufregel (bleibt E1), „Umsatz nur Prop-Payouts“, Finance → Quant nach [[Über mich]] |
| Kommunikationsstil | E1 Kurzfassung | „Code direkt“ steht in [[Tech-Stack]], nicht [[Schreibstil]] |
| Offene Fragen zuerst | E1 komplett | ganze Regel, keine Heimat |
| Trust my Work | E1 komplett | ganze Regel, keine Heimat |
| Auftrags-Typ | E1 3 Zeilen | nichts |
| Vault-Struktur / Vault-Regeln | E1 2 bis 3 Zeilen | Archiv, „merk dir das“, Anhänge/ |
| Token-Disziplin | E1 Schlusszeilen + Grep/Log-Regel, Rest → [[Agent-Architektur Token-Optimierung]] | MCP-Kontext-Warnung 17.09., statusline.py (nirgends verdrahtet, prüfen) |
| Session-Start | **bleibt E1, bis** `session_start.py` Heartbeat + Discovery-Pull selbst kann (Neubau) | PC-Loops-Absatz komplett, NSSM/AP179 → [[Discovery-Runner v2]] |
| Kontext bei Bedarf / Session-Ende / Skill-Shortcuts | raus (Skills briefing/abschluss) | `revise-claude-md` in den abschluss-Skill |
| Sprints | E1 Einzeiler + E2 | „Claude plant nie selbst“, S2026-41 leer → [[Ticket-Board (Jira-Stil)]] |
| Belege | E1 Einzeiler + E2 | Lösch-Logik, „Rechnung direkt anfordern“ → [[Belegordner 2026]] |
| Portfolio-Tab | E1 Einzeiler | [[Buch-Workflow]] Betriebspunkt „Min-Size“ veraltet, fixen |
| Strategy Developer / Workbench | E2 + E5 (`mode=orb`, `engine/lab_ui/`) | `orb_exec`-Falle, `lab_selftest.py`, `workbench.publish` → [[Strategy Developer]] |
| Juli-Modus | E2 → [[Testphase Juli-Modus]] | nichts |
| Discovery-Runner v2 | E1 2 Zeilen + E2 + E5 | „Funde selbst einreihen“, Runner-Neustart nach Engine-Änderung (28.08.), NSSM |
| Gate v4 | E1 5 Zeilen + E2 → [[Latte-Audit (25.09.2026)]] + wochenende-Skill | Stopp je Konto 900/600/1.500, AP292-Ampel, „kein Tag darf killen“, Placebo 5 %, `--stand-setzen` nach Box-Sync (E5); Skill „600 $ × k“ und Latte Z.169-190 veraltet |
| Quant-Team / Meta-Agents / Hooks | E1 je 1 bis 2 Zeilen | Kernfrage in jede Agent-`description`, `urteil_ok` + `test_urteil_gate.py` → [[Hooks-Referenz]], Meta-Regel „neue Reflex-Regel erst als Hook prüfen“ bleibt E1 |
| Tot = Urteil | **Kategorien-Tabelle + Sperre strukturell-tot bleiben E1**, Rest → neue Notiz Todesurteil-Regel | Anlass 82/24/46, Vorbilder, #164/#139 |
| Plugins/Werkzeuge | neue Notiz Werkzeug-Einsatz + E5 (`*.py` → pyright, `overfit.py` → Gegenprobe) | alles |
| Box-Fernzugriff | E1 Einzeiler SSH + „vor Ticket `--pull`“, Rest → [[VPS-Einrichtung Schritt für Schritt]] | Laptop-Regel, Deploy-Ablauf, AP86, MAXLAB_PORT, Deployer |
| RiskGuard/Telegram | Skill + E2 | Erinnerungspflicht, `maxlab_watchdog.json`, maxbot |
| Neues Konto/Firma | Skill + Ablauf → [[Firm-Regeln je Konto]] (Zirkelverweis weg) + E2 | 3 Schritte, „startklar erst nach Prüfung“, AP203, **FFN-Block** (Rithmic, eigene NT8-Lizenz, ein Gerät, „geklärt, nicht erneut fragen“ bleibt E1 solange FFN läuft) |
| GitHub | neue Notiz GitHub & Repos + E2 | alles |
| web.de | neue Notiz + E1 „nie ohne OK senden, auch per CLI“ + E5 Sperre `webde_mail.py send` | alles; [[Belegordner 2026]] „nicht durchsuchbar“ veraltet |
| Hub | E2 + Hub-README | Trigger „Baue im Hub“, nur gezielt, kein Neustart für Kleinkram, Roster-Regel |
| Dauerläufer / Parallele Sessions | E1 Einzeiler | nichts (Hooks decken ab) |
| Großes Ziel | E1 4 Zeilen, Rest → **neue Vault-Notiz** (Memory ist nur lokal am PC) | Formel 0,0147, Beleg-Definition, Leitplanken, Horizont |
| Aktueller Fokus + Prinzipien | E1 Kriterium 50k + Nulldrift + p90 + Buch-Lücke + Simplex/Anatomie/5 Familien; Stand → [[Eval-Passing]] | E8-150k-Beschluss, k2-Vola-Regel, Rechnungsbasis (Shrinkage 0,58, Lehre 82, nested OOS, cage_v2_tiers) |

## Router-Fallen (Gegenleser 05.10.)

- `on_prompt.py` bricht bei Prompts unter 12 Zeichen und bei `/…` ab: „Juli-Modus“ allein feuert nie. Router vor den Filter.
- Agent-Reflex liest Subagent-Rückmeldungen als Prompt (05.10.: 6 Fehlalarme). Vor E2 fixen.
- Cloud-Sessions: `settings.json` ruft `python`, dort oft nur `python3`, Hooks schlucken Fehler → Wrapper mit Fallback; E1-Zeile „kein Hook-Kontext sichtbar → Wegweiser-Tabelle selbst lesen“.
- Subagents sehen nur E1, nie E2: harte Nie-Regeln zusätzlich in box-ops/backtest-runner; `omitClaudeMd` (ungeprüft) nicht für Agents mit Bash-/Box-Zugriff.
- Box und Laptop: Pfad-Hooks sehen Edits per SSH nicht → guard_bash auch auf `ssh …`-Kommandos.
- `.claude/worktrees/*` tragen alte CLAUDE.md-Kopien: aufräumen, beim Abgleich ausschließen.
- Ungeklärt: lädt Claudian (Obsidian) die Projekt-Hooks?

## Reihenfolge (Freigabe: Max gibt das Go zum Bauen)

1. Heimaten füllen (Spalte „vorher übertragen“), Widersprüche dabei fixen. CLAUDE.md bleibt dabei **unverändert**.
2. Router reparieren und bauen, **Testfälle aus dem Sprachbefund**, grün. Schlusszeilen-Check bauen, Selbsttest grün.
3. **Schattenbetrieb:** Router läuft live mit, während die volle CLAUDE.md noch geladen ist. Er schreibt je Prompt ins Log, welches Thema er erkannt und was er eingeblendet hätte. Max arbeitet ganz normal weiter.
4. **Abnahme nach Schattenbetrieb (Max' Bedingung: erst wenn es live funktioniert und keine Fehler macht):** Log gegen die echten Prompts prüfen. Kein verpasstes Thema, keine Fehlalarme in Serie, kein Hook-Fehler. Jeder Fund → Testfall ergänzen, nachbessern, weiter im Schatten.
5. Erst dann CLAUDE.md kürzen, Abgleich „wer lädt jede alte Zeile wann“, committen. Alte Fassung bleibt als `CLAUDE.md.vor-verschlankung` liegen, Rückweg in einer Minute.

## Stand 05.10.2026 abends: Phase 1 gebaut (Go von Max)

- **Heimaten gefüllt:** neu [[Todesurteil-Regel]], [[GitHub & Repos]], [[web.de-Postfach]], [[Werkzeug-Einsatz]], [[Großes Ziel]], Skills `neues-konto` und `riskguard`. Ergänzt: Latte-Audit, wochenende-Skill (600 × k korrigiert, AP323 offen), Discovery-Runner v2, Hooks-Referenz, Strategy Developer, abschluss-Skill, Quant-Agents, VPS-Einrichtung, Ticket-Board, Firm-Regeln je Konto (Zirkelverweis weg), Eval-Passing, Buch-Workflow, Belegordner 2026, Über mich, Hub-README. Überholtes ist markiert, nicht gelöscht.
- **Router gebaut** (Schattenbetrieb), **Schlusszeilen-Check aktiv**, Doku in [[Hooks-Referenz]]. Tests: Router 51/51, Schlusszeilen 23/23, test_chain 112/112. Gegenleser (verdict-auditor): trägt mit Auflagen, Auflagen erledigt (NOT_MAX am Anfang verankert, Leer-Signal in on_stop nicht mehr überschrieben, Muster an echten Schlussblöcken gelockert, Rückfragen frei, Schluss-Log, `--pull` löst kein GitHub mehr aus, Logs in .gitignore, Probe-Spuren gelöscht).
- **CLAUDE.md unverändert.**
- **Abnahme (nächster Schritt):** ein paar Tage normal arbeiten, dann `python .claude/scripts/router_report.py --days 3` mit Max durchgehen. Erst wenn kein Thema verpasst wird und keine Hook-Fehler auftauchen: Router auf `live`, CLAUDE.md kürzen (Phase 2).
- **Noch offen für Phase 2:** session_start.py Heartbeat-Prüfung (bis dahin bleibt der Session-Start-Absatz in E1), python3-Fallback für Cloud-Sessions, Pfad-Hooks für `mode=orb`, `lab_ui/`, `overfit.py`, Engine-Änderung → Runner-Neustart, Sperre `webde_mail.py send`, alte Worktrees aufräumen.
- **Noch offen, von Max zu klären:** in [[Firm-Regeln je Konto]] (FFN-Tabelle) steht „k1 = 4 Micros", die CLAUDE.md sagt beim 7er-Buch „k1 = 7 Micros". Vor Phase 2 die CLAUDE.md-Referenzfassung committen (enthält Änderungen anderer Sessions von heute).
