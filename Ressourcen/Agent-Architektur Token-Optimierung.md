---
tags: [architektur, token, entscheidung]
created: 2026-07-29
status: implementiert
---

# Agent-Architektur: Token-Optimierung (Entscheidung 29.07.2026)

Auftrag kam von einer externen KI (18 Vorschläge A-R). Kritisch geprüft gegen das **reale** System. Ergebnis: 4 Maßnahmen implementiert, der Rest ist bereits vorhanden, Plattform-Sache oder für unsere Größenordnung überdimensioniert.

## 1. Executive Summary

- **System:** Claude-Code-Harness (Claudian in Obsidian) + deterministische Python-Engine (`trading-data\engine`) + NT8/VPS. KEIN eigenes LLM-Framework, keine eigenen API-Clients, kein MCP, kein Vektorindex.
- **Hauptursachen Tokenverbrauch (beobachtet, nicht gemessen):** ① Marathon-Sessions (Kontext wächst, Compaction nötig), ② volle Discovery-Logs (100+ Zeilen) im Kontext statt Verdichtung, ③ Frontier-Modell für Routinearbeit, ④ Wieder-Recherche externer Fakten, ⑤ breite Grep-Muster mit riesigen Treffermengen.
- **Implementiert:** `summarize_results.py` (deterministische Discovery-Verdichtung), [[Research-Cache]] (Evidence Store, real befüllt), Token-Disziplin-Block in CLAUDE.md (inkl. Modell-Leitfaden), diese Doku.
- **Erwartung:** qualitativ deutliche Reduktion der Input-Tokens pro Discovery-Zyklus und pro Recherche; messbar erst nach Baseline (siehe §8).

## 2. Systemanalyse (Ist-Stand 29.07.2026)

| Bereich | Befund |
|---|---|
| Plattform | Claude Code: Prompt-Caching, Auto-Compaction, Subagenten (`Agent`-Tool mit model-Override sonnet/opus/haiku/fable), Skills, deferred Tools — alles nativ vorhanden und aktiv |
| Modellwahl | manuell durch Max via `/model` (heute z.B. sonnet→fable gewechselt) |
| Vault | 63 Notizen, 242 KB gesamt. Größte Datei: Strategie-Logbuch 52 KB. Kein Retrieval-Problem |
| Engine | vollständig deterministisch: qbt, Auto-Fit, Auto-Check (30-min-Cron), Edge-Monitor, MC — 0 LLM-Tokens |
| Ergebnisschema | existiert: `reports/*.meta.json` (~0,9 KB/Report), `book_state.json`, `portfolio.json`, `tasks.json`, `alerts.json` = versionierte Zustandsartefakte |
| Rohdaten | HTML-Reports (9,8 MB) + results.json (bis 84 KB) bleiben auf Platte, gehen nicht durchs Modell |
| Telemetrie | Plattform-intern (`~/.claude/telemetry`), keine eigene API-Kostensicht verfügbar → Token pro Aufgabe nicht selbst messbar |

## 3. Entscheidungsmatrix (alle 18 Vorschläge)

| # | Vorschlag | Entscheid | Begründung |
|---|---|---|---|
| A | Aufgaben-Router | **verworfen** | Es gibt keinen programmatischen Einstiegspunkt — Max spricht direkt mit Claude. Ein Router wäre ein neues Parallelsystem. Ersatz: Modell-Leitfaden in CLAUDE.md (Mensch als Router, Kosten: 0) |
| B | Scout/Analyst/Reviewer-Modelle | **angepasst** | Kein eigenes Multi-Modell-Framework baubar/nötig. Vorhandene Mechanik dokumentiert: `Explore`-Subagent (read-only) + `Agent`-model-Override `haiku` für Massenextraktion, Frontier nur auf Max' Wunsch. Harness-Regel beachtet: Subagenten nur wenn angefordert |
| C | Eskalationslogik | **verworfen** | Eskalation = Max sagt `/model opus`. Automatische Eskalation ist im Harness nicht steuerbar; Selbsteinschätzungs-Trigger explizit unerwünscht |
| D | Deterministik statt LLM | **bereits umgesetzt** | Kernprinzip der Engine seit Tag 1 (Backtests, MC, Auto-Fit, Auto-Check, Ampeln). Neu ergänzt: `summarize_results.py` |
| E | Einheitliches Ergebnisschema | **bereits umgesetzt** | meta.json/results.json/book_state.json. Alle Engines (qbt-Modi) teilen ein Schema. Kein Versions-Overhead nötig bei 1 Entwickler |
| F | Progressive Disclosure/Retrieval | **verworfen (Vektorsuche), Praxis beibehalten** | 242-KB-Vault: Grep+Wikilinks schlagen jeden Vektorindex (Aufbau+Pflege+Embedding-Kosten > Nutzen). Abschnittslesen via Read-offset wird bereits praktiziert |
| G | Kuratierte Strategiekontexte | **bereits umgesetzt** | Genau das ist `book_state.json` (maschinell) + Strategie-Logbuch-Einträge #001-#044 (menschlich): Ziel, Stand, Why, verworfene Ansätze, Entscheidungen |
| H | Handoff-Artefakte | **bereits umgesetzt** | tasks.json (mit Guides), book_state.json, Logbuch = persistente Handoffs. Session-Übergabe macht die Plattform-Compaction; Originalartefakte bleiben auf Platte referenzierbar |
| I | Prompt Caching | **Plattform-Sache** | Anthropic-Harness cached automatisch (5-min-TTL). Einziger Hebel für uns: stabile CLAUDE.md (nicht ständig umbauen) + Sessions nicht unnötig lang laufen lassen. In CLAUDE.md-Leitfaden aufgenommen |
| J | Compaction/Context Editing | **Plattform-Sache** | Auto-Compaction existiert und lief in dieser Session real. Eigenbau wäre schlechter. Schutzliste (nie verlieren): steht implizit in CLAUDE.md/Logbuch (Prinzipien, offene Fehler → tasks.json) |
| K | Tool-Output-Limits | **übernommen** | summarize_results.py + CLAUDE.md-Regeln (Tail-Reads, gezielte Greps, head_limit). Fehlerzeilen bleiben erhalten: Logs liegen vollständig auf Platte |
| L | Token-Budgets | **verworfen** | Keine API-Kostensicht im Abo-Harness; harte Selbst-Limits würden Prüfungen mitten im Lauf abbrechen (explizit unerwünscht). Ersatz: Max steuert Modell + Sessionlänge, Claude erinnert aktiv |
| M | Schleifenbegrenzung | **Plattform-Sache / Praxis** | Harness benachrichtigt bei Background-Tasks (kein Polling nötig); Wiederhol-Lesen desselben Files vermeidet der File-State-Tracker. Kein Eigenbau |
| N | Output-Disziplin | **bereits umgesetzt** | [[Schreibstil]]-Regeln (kompakt, keine Textwände) + strukturierte JSON-Artefakte. Finale Reports behalten Detailtiefe (diese Doku) |
| O | Research-Cache | **übernommen** | [[Research-Cache]] neu angelegt, sofort mit ORB-/Prop-Firm-/Edge-Decay-Evidenz befüllt. Regel in CLAUDE.md: erst Cache greppen, dann suchen; Zeitkritisches mit Gültigkeitsdatum |
| P | Obsidian-Bereinigung | **nicht nötig** | 63 Notizen, keine Duplikate/Rohdaten im Vault (Stichprobe + Größenprofil). Archiv-Ordner existiert. Kein Handlungsbedarf |
| Q | Zentrale Modellkonfiguration | **verworfen** | Es gibt genau 0 hartcodierte Modellnamen im Projekt (Engine ist LLM-frei). Nichts zu zentralisieren |
| R | Telemetrie | **verschoben (Messplan statt Eigenbau)** | Input/Output/Cache-Tokens sind im Abo-Harness nicht pro Aufgabe auslesbar. Eigenbau = Schätzwerte = verboten laut Auftrag ("keine erfundenen Messwerte"). Messplan: §8 |

**Zusätzlich identifiziert (Phase 3):** ① Discovery-Skripte printen künftig nur Summary+Fails-Zähler (Vorlage: orb_discovery2 + summarize_results); ② der 30-KB-Grep von heute (`100%` als Muster) → Regel "spezifische Muster"; ③ Strategie-Logbuch wächst (52 KB) → bei >80 KB Einträge #001-#025 in Archiv-Notiz auslagern (Insight-Bank bleibt).

## 4. Geänderte Dateien

| Datei | Zweck |
|---|---|
| `engine\summarize_results.py` | NEU: deterministische Discovery-Verdichtung (getestet auf 2 echten Datensätzen) |
| `Ressourcen\Research-Cache.md` | NEU: Evidence Store, real befüllt (ORB, Prop-Firmen, Edge-Decay) |
| `CLAUDE.md` | Abschnitt "💰 Token-Disziplin" (8 Zeilen) |
| `Ressourcen\Agent-Architektur Token-Optimierung.md` | NEU: diese Entscheidungsdoku |

Rollback: Git existiert nicht im Vault — Rückbau = Abschnitt/Dateien löschen (alle Änderungen additiv, nichts überschrieben, keine Originaldaten angefasst).

## 5. Betriebshandbuch

- **Discovery lesen:** `python summarize_results.py <results.json> [top_n]` — volle Logs nur bei konkretem Debugging-Bedarf per Select-String.
- **Recherche:** `Grep "stichwort" Ressourcen\Research-Cache.md` → nur bei Miss websuchen → Fund eintragen.
- **Modellwechsel:** `/model sonnet` für Routine, `/model fable` für Entscheidungen. Claude schlägt Downgrade aktiv vor, wenn ein Block abgeschlossen ist.
- **Subagenten:** ~~nur auf Zuruf ("nimm einen Haiku-Scout dafür") — Harness-Konvention.~~ Überholt seit den eigenen Agents (`.claude/agents/`, Pflichtketten per Hook/Workflow). Seit 28.09.2026 gilt „Delegieren nach Nutzen, nicht pauschal“ aus dem Token-Disziplin-Block der CLAUDE.md: abgeben bei viel Lesen mit wenig Rückgabe, bei parallelen Aufgaben, bei mechanischer Arbeit (haiku) oder wenn die Hauptsession auf opus/fable läuft (sonnet). Pauschales „nie selbst arbeiten“ wurde verworfen: Übergabe und kalter Start kosten bei kleinen Aufgaben mehr, als ein günstigeres Modell spart (gleiche Begründung wie Orchestrator/Implementierungs-Agent in §9).
- **Sicherheit:** unverändert — nichts davon berührt Trading-Ausführung, Secrets oder produktive Configs.

## 6. Tests

- summarize_results.py: 2 echte Datensätze (81 + 98 Configs) → korrekte Survivor-/Fail-Zählung, knapp Gescheiterte sichtbar (Informationsverlust-Schutz bestanden). Fremdschema-Fallback ungetestet (kein Fremddatensatz vorhanden).
- CLAUDE.md/Research-Cache: wirken ab nächster Session (Kontext-Load).

## 7. Nicht implementiert & warum (Kurzliste)

Router, Eskalationsautomatik, eigenes Caching, eigene Compaction, Vektorindex, Budget-Enforcement, Telemetrie-Eigenbau, zentrale Modellconfig → sämtlich Plattform-Sache, bereits vorhanden oder überdimensioniert für 63 Notizen + 1 Nutzer. Details: Matrix §3.

## 8. Messplan (statt erfundener Zahlen)

Baseline nicht rückwirkend messbar (keine Token-Sicht pro Aufgabe). Proxy-Messung ab jetzt:
1. **Pro Discovery-Zyklus:** Zeilen, die ins Modell geladen werden (Log-Volltext ~100-180 Zeilen vs. Summary ~8-12 Zeilen) — zählbar aus den Artefakten.
2. **Wöchentlich im Review** (bestehender Auto-Check-Task): Anzahl Websuchen, die durch Cache-Hits ersetzt wurden (Research-Cache-Einträge vs. neue Suchen).
3. **Qualitäts-Guard:** Wochen-Review prüft, ob durch Verdichtung etwas übersehen wurde (Abgleich Summary vs. Auto-Fit-Entscheidungen).

## 9. Zweiter Master-Prompt: Agenten-Portfolio (geprüft 29.07.2026, abends)

Zweiter Auftrag einer externen KI: 10 spezialisierte Agentenrollen analysieren + implementieren. Prüfung gegen das reale System (Engine-Bestand unter `C:\Users\maxlk\Projects\trading-data\engine` verifiziert). **Ergebnis: 0 neue Agents.** Jede Rolle war entweder schon deterministisch gelöst, durch Harness-Bordmittel abgedeckt oder unter Kosten/Nutzen. Zuordnung nach den 8 Kategorien des Auftrags:

| Rolle (Vorschlag) | Kategorie | Entscheid + Begründung |
|---|---|---|
| Orchestrator | 4 (Hauptagent) | = Entscheid A (§3). Max spricht direkt mit Claude, Harness delegiert. LLM-Orchestrator = kalter Kontext + Handoff-Overhead pro Auftrag |
| Research-Agent | 3 (Workflow) + Skill | Existiert als Workflow: Research-Cache-First-Regel + `paper-edge`-Skill (strukturierte Paper-Bewertung). Kein eigener Agent nötig |
| Vault/Retrieval-Agent | 2 (Tool) | 242-KB-Vault: Grep + Wikilinks. Der Auftrag selbst fragt „reicht ein Suchtool?" — ja |
| Strategy-Analyst | 4 (Hauptagent) | Spezifikation läuft über [[Strategie-Anatomie (Framework)]] + [[Strategie-Familien]] + Logbuch. Handoff wäre größer als die Aufgabe (voller Trading-Kontext nötig) |
| Implementierungs-Agent | 4 (Hauptagent) | 1 Entwickler, 1 Engine-Repo. Subagent müsste Engine-Konventionen jedes Mal kalt neu lernen |
| Backtest-Controller | 1 (Deterministik) | **Bereits exakt so gebaut:** qbt + Auto-Fit + Auto-Check (30-min-Cron) + einheitliches Ergebnisschema. Der Auftrag empfiehlt selbst „besser deterministisch" — ist es seit Tag 1 |
| Backtest-Analyst | 1 (Deterministik) | summarize_results.py + Auto-Fit-Entscheide + Edge-Ampeln. Regel „keine vollen Trade-Listen in den Kontext" steht schon in §5/CLAUDE.md |
| Debugging-Agent | 4 (Hauptagent) | Selten, stark mit Implementierung verflochten → Modus, keine Rolle |
| Review-Agent | 1 + Harness-Skill | Look-ahead/Leakage prüft die Engine (Lektion #021, orb_core_v2); Code-Review = eingebauter `/code-review`-Skill mit frischem Kontext |
| Doku-Agent | 8 (redundant) | Auftrag zweifelt selbst dran. Session-Ende-Routine in CLAUDE.md erledigt das |

**Rest-Bedarf an Subagenten** (viel Wegwerf-Kontext, z.B. breite Suche): abgedeckt durch eingebauten `Explore`-Agent + `Agent`-model-Override `haiku` — auf Zuruf, wie in §5 dokumentiert. Persistente eigene Agent-Definitionen (`.claude/agents/`) lohnen erst, wenn Max regelmäßig dieselbe Subagenten-Rolle anfordert; aktuell nicht der Fall.

**Nachtrag 29.07. abends (Max läuft täglich ins Tageslimit):** Hauptursache gefunden — Claudian-Standardmodell stand auf **Opus + Effort high** für JEDE Session (`.claudian/claudian-settings.json`). Opus verbraucht das Abo-Limit ~5x schneller als Sonnet. Umgestellt auf **sonnet** als Default; Opus/Fable nur noch gezielt per `/model` für Entscheidungen. Zweitmaßnahme: Logbuch-Archivierung vorgezogen (52→25 KB, halbiert die Kosten jedes Volltext-Reads).

**Einziger neuer Befund:** §3-P („keine Duplikate") war überholt — 14 byte-identische Sync-Duplikate (`* 1.py`/`* 1.parquet`/`* 1.pine`/Canvas) im Vault-Root. Per MD5 verifiziert und entfernt (Originale unberührt). Sonst keine Änderung nötig: Der zweite Auftrag überlappt zu ~80% mit §3 und bestätigt die Architektur.

## 10. Offene Punkte

| Punkt | Auswirkung | Prio | Nächste Aktion |
|---|---|---|---|
| ~~Logbuch-Archivierung~~ | erledigt 29.07. abends | ✅ | #001-#025 → [[Strategie-Logbuch Archiv (001-025)]], Logbuch 52→25 KB |
| Discovery-Skript-Vorlage mit Kompakt-Print | kleiner | niedrig | beim nächsten neuen Discovery-Skript anwenden |
| Proxy-Messung §8 | Erfolgskontrolle | mittel | ab nächstem Wochen-Review mitführen |
