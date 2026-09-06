# CLAUDE.md – Max' zweites Gehirn

Dies ist der persönliche Wissensspeicher (Obsidian Vault) von **Max**. Diese Datei wird bei jedem Session-Start geladen und ist deine zentrale Anleitung.

---

## 🏖️ Urlaub 04.09.–ca. 18.09.2026 — PC ist aus (diesen Abschnitt nach der Rückkehr wieder rausnehmen)

Max ist ab 04.09.2026 zwei Wochen im Urlaub und arbeitet in dieser Zeit nur über seinen **Laptop**. Der Haupt-PC ist die ganze Zeit **aus**.

- **Nicht erreichbar:** Hub, lokaler Lab-Server (`app_server.py`), NT8-lokale Instanz, PC-Discovery-Fallback, die PC-Loop-Heartbeat-Datei (`C:\Users\maxlk\Projects\trading-data\engine\.claude_loop_heartbeat.json`). Das ist erwartet — keine Störung, keine Eskalation nötig.
- **Läuft normal weiter:** Live-Handel auf der Box (100.127.89.9, NT8 + RiskGuard) läuft unbeaufsichtigt weiter, Discovery-Runner läuft 24/7 auf der Box weiter (Auto-Promotion ins Next-Week-Buch inklusive). Beides braucht den PC nicht.
- **Session-Start-Regel „PC-Loops übernehmen" pausiert** in diesem Zeitraum (Heartbeat-Datei liegt auf dem ausgeschalteten PC, nicht prüfbar). Stattdessen für den Status den `box-ops`-Agent nutzen.
- **Zugriff läuft so:** Vault per Git (`git@github.com:mkmeboss/my-brain-vault.git`), Engine-/Buch-Arbeit per SSH auf die Box (100.127.89.9). Kein Zugriff auf Dateien, die nur lokal auf dem PC liegen (u.a. `book_state.json`/`portfolio.json` im nicht-versionierten `trading-data`-Ordner, falls die Box-Kopie mal abweicht — im Zweifel die Box-Kopie als Quelle der Wahrheit behandeln, solange der PC aus ist).
- Größere Buch-/Portfolio-Entscheidungen (Next-Week-Buch übernehmen, neue Firma, Kontowechsel) über SSH auf der Box vorbereiten, aber wenn möglich bis zur Rückkehr als Ticket liegen lassen statt allein zu entscheiden — Max hat gesagt, er will vom Laptop aus weiterarbeiten können, nicht dass in seiner Abwesenheit unumkehrbare Entscheidungen ohne ihn fallen.

---

## 📦 Queue-Stand Urlaub (06.09.2026, Laptop-Session spät abends) — für JEDE Session, die die Discovery-Queue anfasst

Max hat vor dem Urlaub entschieden: die Box rechnet zwei Wochen ohne Nachfüllen, **und alles, was jetzt in der Queue liegt, ist bewusst „unseres" und darf im Notfall wieder raus.** Stand und Regeln:

- **Was läuft:** Varianten-Vorlagen des Generators (`VARIANT_SPECS` in `job_generator.py`, Job-IDs `gen_<vorlage>_<suffix>_<markt>`, Suffixe `_mt`, `_hf`, `_kal`, `_dix`, `_tfm`, `_tf`, `_gegen`, `_spaet`), dazu die neue Ersatz-Vorlage `vwap_pullback_leg` (ersetzt `NQ_VWAP-Pullback`). Jeder dieser Jobs trägt das Feld **`tag: "vacation_variants_0906"`** (Coverage-Jobs der alten Vorlagen: `generator_coverage`). Vorrat ≈ 174k Configs ≈ 22 Box-Tage, Prio HF zuerst (Max' Ansage 06.09.).
- **Erwartung, damit niemand einen Filter-Bug vermutet:** die Varianten laufen als „neues Bein" gegen das Buch (kein `replaces_leg`, weil das Buch kein tsmom/maband-Bein hat), und dieser Weg hat noch nie einen Kandidaten geliefert (#139 B3). **„0 Kandidaten" ist bei den `_mt/_hf/_tf/_tfm/_gegen/_spaet`-Jobs das erwartete Ergebnis.** Kandidaten-Chance haben nur: `vwap_pullback_leg` (Ersatz-Slot), `_kal`/`_dix` (neue ökonomische Bedingungen) und Ersatz-Jobs in den vier Buch-Modi, seit diese einen Null-Schalter haben (siehe unten). Details und Rechnung in [[Discovery-Runner v2]].
- **Rausnehmen (wenn eine Session Rechenzeit für etwas Besseres braucht):** nie `queue.json` von Hand kürzen, sondern auf der Box `python -c "import json;q=json.load(open('discovery/queue.json',encoding='utf-8'));n=0
for j in q['jobs']:
  if j.get('status')=='pending' and j.get('tag')=='vacation_variants_0906': j['status']='skipped'; n+=1
json.dump(q,open('discovery/queue.json','w',encoding='utf-8'),ensure_ascii=False,indent=1);print(n)"` (nur `pending`, nie `running`), danach Runner NICHT neu starten (er liest die Queue je Job frisch). Der Generator füllt dann weiter Varianten nach — wer das dauerhaft stoppen will, entfernt die Suffixe aus `VARIANT_SPECS` und startet den Runner neu (Stop → Sync → Start). Handgebaute Jobs mit höherer `priority` (≥ 60) laufen ohnehin vor den Varianten.
- **Nicht anfassen:** `registry.json` (append-only, AP122), laufende Jobs (`running`), `generator_state.json`.
- **Runner-Code auf der Box:** seit 06.09. 23:07 mit Varianten-Generator und `registry_write_every_configs: 200` (Register nur alle 200 Configs, Audit B2). Null-Schalter für ts_reversal/last_hour/asian/vwap_pullback und die Kalender-/DIX-Gates: Stand siehe Ticket **AP137** (Übergabe-Ticket dieser Session) und Daily Note 06.09.

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

**Vorfall:** Max hat mehrfach angemerkt, zu oft nicht gefragt worden zu sein, bevor etwas geändert wurde — diese Regel existierte bereits, wurde aber nicht konsequent genug angewendet. Ab jetzt: **im Zweifelsfall immer fragen**, auch wenn es nach der zweiten Nachfrage in Folge aussieht.

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
4. **Discovery-Inbox lesen (Regel Max, 18.08.2026):** `cd C:\Users\maxlk\Projects\trading-data\engine && python discovery/inbox_tool.py --pull` (holt den Stand von der **Box** — dort läuft der Runner seit 18.08. 23:06 dauerhaft, der lokale Ordner ist nur Spiegel — und zeigt Status + ungelesene Kandidaten kompakt). Gibt es Kandidaten mit „besser" (bzw. bei Exit-Sweeps „vs Original besser"): Quant-Team + `strategy-auditor` drüberschauen lassen, dann Next-Week-Buch + Ticket, danach `inbox_tool.py --seen-all` (schreibt die seen-Flags auf die Box zurück). Steht der Runner auf der Box (Heartbeat > 30 min alt; seit 20.08. gibt es keine Pause mehr, 24/7) und die Queue hat `pending`-Jobs: per SSH neu starten (WMI-Zeile in `box_provision_discovery.ps1`). Details [[Discovery-Runner v2]].
5. Erst danach mit der eigentlichen Aufgabe weitermachen.

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

Danach **immer** `funded_finalize.py` laufen lassen, im selben Zug, nicht „später". **Und im selben Zug `python discovery/inbox_tool.py --push-next`** (pusht `book_state.json` + `book_state_next.json` auf die Box) — gilt für JEDE Änderung an `book_state.json`, nicht nur am Next-Buch. Vorfall 21.08.2026 ([[Strategie-Logbuch]] #126): der Momentum-Duplikat-Fix vom 20.08. wurde nie gepusht, die Box rechnete drei Tage lang alle Buch-Marginals (inkl. drei Auto-Promotionen) gegen das alte 7-Bein-Buch. Der Portfolio-Tab zeigt dann automatisch: Kaufplan (beide Konten mit Frac, Solo-Quote, Median-Dauer), P(funded) rollend über 1/2/3/6/12 Monate, erwartete Eval-Anzahl und Kosten, sowie die Frontier in **beiden** Bust-Modi (EOD-Kopfzahl + ehrliche Intraday-Zahl nach #077).

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

### 🧬 Edge-Health-Monitor zieht Bein-Änderungen automatisch mit (Regel Max, 01.09.2026)

Der Decay-Monitor unten im Lab-Tab (🧬 Edge-Health, Live-Trades je Bein gegen den Backtest-Erwartungs-Kegel, McLean/Pontiff + Lopez de Prado) baut seine Referenz (`edge_ref.json`) seit 01.09.2026 **automatisch neu**, sobald `book_state.json` neuer ist als `edge_ref.json` (Mtime-Check in `_edge_health()`, `app_server.py`) — kein manueller Lauf von `gen_edge_ref.py` mehr nötig. Die Zuordnung NinjaScript-Name → Bein läuft über Familien-Präfix (Endung `_d<Datum>`/`_v<N>` wird abgeschnitten), damit ein Discovery-Auto-Promote oder eine neue Developer-Version desselben Mechanismus (neuer Bein-Name, gleiche Familie) automatisch mitgezogen wird. Außerdem seit 01.09.2026 nur noch **das aktuell aktive Konto** (per letztem Fill ermittelt), nicht mehr alle historischen Konten vermischt.

**Ein Fall bleibt manuell:** eine WIRKLICH neue Strategie-Familie (neue NinjaScript-Klasse, die noch nie im Buch war) braucht einmalig einen neuen Eintrag in `NS_MAP` (`gen_edge_ref.py`, NinjaScript-Klassenname → Bein-Familie-Präfix) — die Klasse kennt sonst niemand vorab. Bei jedem neuen NT8-Deploy einer neuen Strategie also kurz `NS_MAP` in `gen_edge_ref.py` ergänzen, danach läuft der Rest wieder automatisch. Vorfall, der zum Fix führte: `NQ_VWAP-Pullback` fehlte komplett in der alten, hartkodierten Zuordnung und wurde vom Decay-Monitor gar nicht erfasst — genau der Fall, den diese Regel künftig verhindert.

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

## 🤖 Discovery-Runner v2 (Regel Max, 18.08.2026)

**Rechnen macht die Maschine, entscheiden macht Claude.** Alpha-Suche läuft als lokaler Dauerprozess `engine/discovery/discovery_runner.py` (Queue → Prämisse → Grid+Gates → Buch-Marginal → Inbox), Doku in [[Discovery-Runner v2]].

- **Neue Suchidee = Job in der Queue**, kein neues Einzelskript mehr: Job-JSON (Mechanismus, Familie, **Why vorab**, `base`, `grid` ≤ ~100 Configs, `premise.configs`, ggf. `replaces_leg`) → `python discovery/inbox_tool.py --add-job job.json`. Braucht die Idee ein neues Engine-Modul (neuer `mode`), erst das Modul, dann der Job.
- **⭐ Neue Edge / Vorteil gegenüber dem alten Portfolio → NIE ins Live-Buch, IMMER sofort ins Next-Week-Buch (Regel Max, 18.08.2026).** `discovery/promote_next.py` macht das automatisch: läuft auf der Box alle 30 Min (`--box-mode`, Scheduler-Task „MaxLab Discovery Promote"; deckt „sofort" und den 15-Uhr-Punkt ab), nimmt je Bein den besten Kandidaten mit belegtem Vorteil (Ersatz: „vs Original besser"; neues Bein: „besser" + über der Zufallsdecke), schreibt ihn in `book_state_next.json` (neuer Bein-Name `<Bein>_d<YYMMDD>`, Backup vorher, `next_week.changes` mit `auto`-Block), rechnet `funded_finalize --next` + `live_finalize --next` und merkt das Next-Week-Ticket vor. **`book_state.json` (Live) wird davon nie angefasst** — die Übernahme ins Live-Buch bleibt die Wochenend-Entscheidung über das Ticket (Quant-Team + Auditor). Konflikte (Bein im Next-Buch schon manuell geändert, z.B. `NQ_LastHour_v3`) werden NICHT automatisch aufgelöst, sondern in der Inbox gemeldet. Der Runner selbst schreibt nie in `book_state*.json`, `tasks.json`, `developer/state.json`.
- **PC darf aus sein:** Runner + Auto-Promotion laufen komplett auf der Box. Ist der PC an, spiegelt `auto_check.py` (alle 30 Min) bzw. `inbox_tool.py --pull` den Box-Stand (Inbox, Register, `book_state_next.json`, `portfolio_next.json`, Reports, vorgemerkte Tickets → `tasks.json`). **Manuelle Änderung am Next-Buch am PC → sofort `python discovery/inbox_tool.py --push-next`**, sonst promotet die Box in einen alten Stand.
- **Register ist Pflicht:** jeder Trial zählt (auch Backfill 1390 Alt-Trials); Zufallsdecke immer gegen `n_global`. Wer außerhalb des Runners sweept, trägt die Ergebnisse per `backfill_registry.py`-Muster nach.
- **Läuft auf der Box** (seit 18.08.2026 23:06, Max' Okay): `C:\Users\maxlk\Projects\trading-data\engine\discovery\` auf `VMD202078` (gleicher Pfad wie am PC, weil die Engine absolute Pfade hat), Python 3.11 unter `C:\Program Files\Python311`, **seit 20.08.2026 24/7 (`pause_hours []`, Max' Ansage — BELOW_NORMAL schützt NT8; bei Auffälligkeiten im Live-Handel wieder `[[15,22]]`)**. Eine Instanz je Maschine (`runner.lock`), Stopp über `STOP`-Datei (`box_provision_discovery.ps1 -Stop`). **Engine-Änderung am PC → vor dem nächsten Nachtlauf `box_provision_discovery.ps1 -SyncOnly`**, sonst rechnet die Box mit altem Code. Neue Jobs immer über `inbox_tool.py --add-job` (macht pull → append → push auf die Box). Lokal starten (`start_discovery.ps1`) nur, wenn die Box nicht erreichbar ist — nie beide gleichzeitig auf derselben Queue.
- **⭐ Die Queue darf nie leerlaufen (Regel Max, 21.08.2026 — Fulltime-Suche, Fokus aktuell HF/mehr Trades pro Jahr).** Seit 21.08. 16:50 füllt der Runner die Queue **selbst** nach: `discovery/job_generator.py` (im Daemon-Loop, `min_pending` 3) erzeugt erst Folge-Jobs zu fertigen Jobs mit Survivors (Verfeinerung um den besten Survivor, HF-Rangfolge; Exit-Profil-Sweep), dann Abdeckungs-Jobs aus 11 Vorlagen × 4 Märkten (nur Modi mit dokumentierten Params, `orb` immer `orb_exec=close`), bis Tiefe 3; Register-Pruning gegen Doppelarbeit, max. 120 Jobs/Tag. **Seit 06.09.2026 vierte Quelle: Varianten-Vorlagen** (`VARIANT_SPECS` in `job_generator.py`): jede tsmom/maband-Vorlage wird mit je einer im Register leeren Achse geklont (HF zuerst: `mb_max_trades`, kürzeres Signalfenster; dann Zeitrahmen, Gegenseite, später Start), ~174k Configs ≈ 22 Box-Tage Vorrat, damit die Queue auch ohne Session wochenlang rechnet. Details [[Discovery-Runner v2]]. Handgebaute Jobs (`--add-job`) laufen mit Vorrang (höhere `priority`). Schreibt der Runner trotzdem `queue_empty` in die Inbox, ist die Vorlagen-Welt ausgereizt → Claude muss **neue Mechanismen** (Engine-Modul + Vorlage in `TEMPLATES`) liefern, nicht mehr Grid. Mehr Grid auf altem Mechanismus bringt nichts (#494), die Zufallsdecke wächst mit jedem Job mit. **Dafür gibt es seit 21.08.2026 den Subagent `alpha-scout`** (`.claude/agents/alpha-scout.md`, Background starten): bei `queue_empty`, bei „was testen wir als nächstes?" und wenn Max eine Idee in einen Job übersetzt haben will. Er macht erst Inventar (Register, Queue-Ausgänge, Friedhof in `ideas.json`/Logbuch, Engine-Modi, Datenbestand), rotiert durch die 4 Edge-Quellen, rankt und schreibt queue-fertige Jobs nach `discovery/jobs_proposed/` + Report nach `discovery/scout_reports/` (Modul-Specs für Ideen ohne `mode`). Er baut keine Vorlagen-Grids nach und schreibt nie in `queue.json`: die Hauptsession prüft kurz und reiht mit `inbox_tool.py --add-job` ein.
- **Nie** `runner.log` oder volle `results/*.json` einlesen — `inbox_tool.py` bzw. `summarize_results.py` reichen.
- **⭐ Claude reiht neue Funde selbst ein, ohne dass Max „tu es in die Queue" sagen muss (Regel Max, 28.08.2026).** Sobald eine neue Hypothese/Vorlage fertig gebaut und geprüft ist (Dry-Run + `pipeline-auditor`), gehört sie standardmäßig ans Ende der Queue — Einreihen ist der Normalfall, keine Ausnahme, die erst extra angesagt werden muss. Gilt genauso für `alpha-scout`-Vorschläge aus `jobs_proposed/`: kurz prüfen, dann einreihen, nicht liegen lassen. Nach jeder Engine-/`job_generator.py`-Änderung dazu **nicht vergessen: Runner muss neu gestartet werden** (Stop → Sync → Start), sonst läuft er mit dem alten Code weiter (Python cacht importierte Module, ein laufender Prozess lädt `job_generator.py`/`vix_bias.py` & Co. nie automatisch neu — Vorfall 28.08.2026, 5,5 Std. Leerlauf trotz bereits gebauter neuer Vorlagen). Ziel: wenn ein Job-Batch fertig ist, steht bereits der nächste bereit, damit die Box nie leerläuft, ohne dass Max jedes Mal explizit nachfragen muss.

---

## 🔬 Der EINE Weg für jede Strategie-Idee (Regel Max, 23.08.2026 — verbindlich)

**Es gibt ab jetzt genau einen Weg, wie eine Idee getestet wird. Nicht mehrere Arten, sondern eine Art, die dafür sehr intensiv läuft.** Gilt für jede neue Strategie, jede Hypothese, jeden Discovery-Job, jede Developer-Version. Wer davon abweicht, braucht einen ausdrücklichen Grund von Max.

**Die vier Schritte, immer in dieser Reihenfolge:**

1. **WHY zuerst.** Kein Test ohne Mechanismus im Klartext: wer muss handeln, warum, und warum bleibt das Geld liegen. Ohne Why kein Job — das Feld ist Pflicht und wird beim Job-Bau geprüft (`assert` in `hypothesis_bank.py`).
2. **Dann die ARTEN.** Eine Hypothese wird **nie als eine Strategie** getestet, sondern als **mindestens zehn Implementierungen desselben Mechanismus**: andere Fensterlänge, anderer Signaltyp, andere Bestätigung (**Volumen / Delta / EMA12 / EMA20 / VWAP-Seite**), anderer Stop (Range/Sigma/ATR), anderer Exit (EOD/Zeit/RR). Der Baustein dafür ist `AX_CONFIRM` / `AX_RISK` / `AX_EXITS` in `hypothesis_bank.py`. Weniger als zehn Varianten lässt der Job-Bau nicht zu. **Diesen Schritt übernimmt seit 01.09.2026 der Subagent `variant-scout`** (automatisch, sobald eine neue Hypothese vorliegt, bevor sie in eine Bank-Notiz oder einen Job geschrieben wird): er misst gegen die echten Engine-Achsen und die bestehende Bank, wie viele ECHTE Varianten es gibt, und warnt vor Doppelzählung mit bereits toten Verwandten. **Direkt danach, seit 01.09.2026: `strategy-auditor` im Batch-Vorprüfungs-Modus** — EIN Aufruf über die ganze Gruppe der von `variant-scout` als testbar eingestuften Hypothesen (nicht einzeln!), der nur die ökonomische Story gegenprüft (Why kausal? Look-ahead schon im Text erkennbar? Familie eindeutig? zu gut um wahr zu sein?), bevor überhaupt Box-Rechenzeit für die Configs verbrannt wird. Der bisherige Vollmodus-Trigger (adversarialer Gegenleser mit Backtest-Ergebnis, kurz vor Eval-Deploy) bleibt zusätzlich bestehen — die Batch-Vorprüfung ersetzt ihn nicht, sie fängt nur die billigen Fälle früher ab.
3. **Dann die bekannten FALLEN — als Vorbedingung, nicht als Nachgedanke.** Alles, was uns bisher umgebracht hat, läuft automatisch mit. Zwei Ebenen:
   - **`GATES_HARD`** (in `discovery/hypothesis_bank.py`) für jede Grid-Zelle: min. Trades/OOS-Trades/Trades pro Jahr, Top-5-Konzentration ≤ 50 % (#038), Block-Bootstrap P ≥ 0,90, Plateau statt Spitze, letzte 3 Jahre nicht negativ (#057), Kosten-Stress 2 Ticks je Seite.
   - **`discovery/controls.py`** für jeden Kandidaten, der das Buch-Marginal besteht: Look-ahead-Delay (#066/#067), Long-Bias (Goyal/Jegadeesh, #108), Nulldrift mit gewürfelter Richtung, Multi-Markt (#051), Epochen-Split 2016-2019 vs. 2022-2026 (#057), Zufallslevel bei Level-Strategien, Tages-Korrelation zum Bestandsbuch ≤ 0,70 (#079, Lehre 82).
   Erst wenn alles davon steht, ist ein Fund **`deploy_ready`**. `promote_next.py` promotet seit 23.08. **nur noch deploy_ready-Kandidaten** automatisch ins Next-Week-Buch.
4. **Dann rechnen, lange und breit.** Auf der **Box**, nicht im Chat, damit Max' PC aus sein kann. Jobs kommen aus `python discovery/hypothesis_bank.py --enqueue --push`.

**Die Werkzeuge dafür stehen und werden benutzt, statt neue Einzelskripte zu bauen:**

| Datei | Rolle |
|---|---|
| `engine/sigcore.py` | gemeinsame Signal-/Ausführungsschicht: Bars, Averages, RVOL, Delta-Proxy, Tageskontext (immer um einen Tag verschoben), ehrliche Trade-Simulation, alle Gates an EINEM Ort |
| `engine/tsmom.py` (`mode="tsmom"`) | verallgemeinertes Time-Series-Momentum: Fenster, Signaltyp (ret/zscore/rank/rangepos/signratio/accel/jerk/wins), Basis (open/prev_close/prev_rth/overnight), Schwelle in % oder σ |
| `engine/maband.py` (`mode="maband"`) | Averages, Crossover, Geschwindigkeiten, Bänder, Kanäle, Anker-VWAP — teilt sich Ausführung und Gates mit `tsmom` |
| `discovery/hypothesis_bank.py` | Hypothese → Job mit ≥ 10 Implementierungen, Why, harten Gates |
| `discovery/controls.py` | die Lehren aus den Fehlschlägen als automatische Batterie |

**Neue Idee heißt: neue Zeile in `hypothesis_bank.py`** (und bei einem wirklich neuen Mechanismus ein neuer `mb_kind`/`tm_signal` in den bestehenden Modulen) — **nicht** ein neues Skript daneben. Der Grund: nur so zählt das Register jeden Trial mit, nur so gilt dieselbe Zufallsdecke, und nur so ist der Look-ahead-Check an einer Stelle statt an dreißig. Hypothesen-Vorrat: [[Hypothesen-Bank (Momentum & Averages)]] und [[Hypothesen-Bank (Volumen & Flows)]].

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

## 🔍 Pipeline-Auditor (Regel Max, 25.08.2026)

Subagent `pipeline-auditor` (`.claude/agents/pipeline-auditor.md`): der Meta-Prüfer über den **Prozess** — nicht die einzelne Strategie (das bleibt `strategy-auditor`), sondern ob wir methodisch sauber rechnen, messen und entscheiden, ob wir Fehler aus dem Logbuch wiederholen und wo die Pipeline selbst besser werden kann (neue Gates, neue Selbsttests, Automatiken).

**Einschalten (automatisch, ohne Rückfrage):** bevor ein neuer Hypothesen-Job auf die Box geht, nach jeder Discovery-Batch-Auswertung, bei jeder Engine-Änderung an der Ausführungs-/Gate-Schicht (`sigcore.py`, `controls.py`, `hypothesis_bank.py`, `overfit.py`), wenn ein Ergebnis "zu gut" aussieht, und auf Zuruf. Er ändert nie selbst Dateien — Befunde und Verbesserungsvorschläge setzt die Hauptsession um. Prüfraster: Look-ahead, Multiple Testing/Register, Gate-Batterie aktiv, Rausch-Disziplin (Seeds), Stale-State (Box-Sync, push-next), v2-Kriterium, Null-Ergebnis-Verdacht.

---

## 🆕 Neue Agents vom 27.08.2026 — automatisch einschalten, nicht nur dokumentiert liegen lassen

Jeder Subagent hat seinen Trigger schon in der eigenen `description` (`.claude/agents/*.md`) — das reicht der Hauptsession technisch, um ihn zu sehen, aber die Erfahrung mit `pipeline-auditor`/Quant-Team zeigt: **ohne einen expliziten Satz hier in der CLAUDE.md wird ein Agent leicht vergessen**, weil er nicht im Reflex sitzt. Deshalb für jeden neuen Agent die Einschalt-Regel ausgeschrieben, keine Ausnahme:

- **`engine-regression-tester`**: automatisch VOR jedem `box_provision_discovery.ps1 -SyncOnly` und nach jeder Änderung an `sigcore.py`, `controls.py`, `hypothesis_bank.py`, `overfit.py`, `qbt.py`, `tsmom.py`, `maband.py` — ohne Rückfrage einschalten, nicht erst wenn Max danach fragt. Meldet er "Sync STOPPEN", wird nicht gesynct, bis geklärt ist warum.
- **`logbook-distiller`**: automatisch nach jedem neuen Vorfall/jeder neuen Lehre, die frisch ins Strategie-Logbuch geschrieben wird ("ist das jetzt auch als Gate codiert oder bleibt es nur Text?"). Wöchentlich zusätzlich per Automatik (siehe unten), aber das ersetzt nicht das sofortige Einschalten nach einem frischen Vorfall.
- **`box-ops`**: läuft seit 27.08. bereits automatisiert stündlich als deterministisches Skript auf der Box (kein Subagent-Aufruf nötig für den Routine-Check) — der Subagent selbst kommt zusätzlich bei "läuft alles?"/"check die Box" zum Einsatz, wenn Max eine tiefere Einschätzung will als die reine Ampel-Zeile.
- **`live-reconciler`**: soll täglich nach Handelsschluss automatisiert laufen, hängt aber am API-Guthaben-Blocker vom 27.08. (siehe Box-Fernzugriff-Abschnitt) — bis das geklärt ist, auf Zuruf einschalten ("passt das Konto noch?") oder wenn ein Live-Kontostand deutlich vom Erwartungsband abweicht.
- **`retro-agent`**: soll wöchentlich Sonntag 12:00 automatisiert laufen, hängt am selben Blocker. Bis dahin: die Hauptsession fragt sich am Ende eines längeren Arbeitsblocks selbst "würde eine Retro hier etwas bringen?" und schlägt es Max proaktiv vor, statt nur zu warten bis die Automatik steht.

- **`verdict-auditor`** (neu 30.08.2026, `model: opus`): der Gegenleser für das **Urteil selbst**. Automatisch einschalten, **bevor** ein Stempel draufkommt: (a) jedes Testergebnis, das mit "tot"/"gut"/"neutral"/"ins Buch" bewertet wird (Backtest, Discovery-Batch, Developer-Version, Hypothesen-Test), und (b) alles neu Gebaute (Engine-Modul, Gate, Vorlage, Skript, Automatik), das für "fertig" erklärt werden soll. Er prüft, ob die Beweislage das Urteil trägt, was ausgelassen wurde und welche max. 3 Nachtests sich rational lohnen — Regel "Hypothese vor Urteil" (tot nur nach vollem Test) ist sein Kern. Abgrenzung: `pipeline-auditor` = Prozess, `strategy-auditor` = Strategie vor Deploy, `verdict-auditor` = der Stempel danach. Er ändert nie Dateien; Trust-my-Work gilt (nur frische Urteile, alte nur auf Auftrag oder bei geänderten Fakten). Einmaliger Bestands-Durchlauf über alte Urteile: Ticket AP116.
- **`design-guard`** (neu 30.08.2026, `model: sonnet`): automatisch bei **JEDER** Änderung an einer Oberfläche — Hub, Strategy Lab, Developer-Tab, Lab-Reports, jede künftige App. Neuer Button, neuer Tab, neues Panel, neues Fenster, neue Tabelle/Karte, geänderte Farbe/Abstand: `design-guard` läuft mit, ohne dass Max danach fragt. Er misst gegen [[Design-System (Hub & Apps)]] (Vault, `Ressourcen/`) — App-übergreifende Usability-Grundregeln plus die eigene Charta jeder App. **Jede App darf anders aussehen, aber jede App muss in sich gleich aussehen**: ein neuer Punkt im Lab sieht aus wie die Punkte, die dort schon stehen. Er ändert nie selbst Dateien, sondern liefert den fertigen Schnipsel; die Hauptsession setzt um und macht danach `.\hot_reload.ps1` (Hub) bzw. Lab-Server-Neustart. Steht eine Regel nicht in der Charta, entscheidet er nicht, sondern fragt — neue verbindliche Design-Regeln schreibt nur Max in die Design-System-Notiz.

**Der Blocker (API-Guthaben) hebt die Regel nicht auf** — er verschiebt nur den Weg (automatisiert vs. auf Zuruf), nicht die Pflicht, den Agent zu nutzen, sobald sein Trigger eintritt.

## 🆕 Neuer Agent vom 01.09.2026 — `variant-scout`

**`variant-scout`** (`model: opus`): automatisch einschalten, **sobald eine neue Hypothese/ein neuer Mechanismus vorliegt** — egal ob aus Research (Paper, `research-scout`-Fund), aus einer Discovery-Auswertung oder aus Max' eigener Idee — und **bevor** sie als Zeile in eine Hypothesen-Bank-Notiz (`Bereiche/Hypothesen-Bank (*).md`) oder als `H()`-Job in `hypothesis_bank.py` geschrieben wird. Er beantwortet die Vorfrage zu Schritt 2 aus "Der EINE Weg" (⬆️): in wie vielen ECHTEN, sinnvollen Arten lässt sich der Mechanismus bauen (Fensterlänge, Signaltyp, Basis, Bestätigung, Stop, Exit, Markt), geprüft gegen die tatsächlichen Engine-Achsen (`AX_CONFIRM`/`AX_RISK`/`AX_EXITS` in `hypothesis_bank.py`, `mb_kind`/`tm_signal` in `maband.py`/`tsmom.py`) statt gegen eine optimistische Schätzung. Er flaggt außerdem Verwandtschaft mit bestehenden Bank-Zeilen (Doppelzählung gegen die Zufallsdecke vermeiden) und mit bereits toten Funden (Kontaminationswarnung, z.B. ein neuer λ-Proxy-Ableger nahe einem bereits per #138 widerlegten Verwandten). Er ändert nie selbst Dateien — die Achsen-Tabelle trägt die Hauptsession ein. Trigger sitzt bewusst VOR dem Bank-Eintrag, nicht danach, weil sich sonst dieselbe Falle wiederholt wie bei den anderen 27.08-Agents: ohne den Reflex hier in der CLAUDE.md wird der Schritt beim Tippen einer neuen Zeile leicht übersprungen.

---

## 🪝 Hooks: Reflex-Regeln laufen im Harness, nicht im Kopf (Max, 04.09.2026)

Seit 04.09.2026 setzt Claude Code selbst einige der „Claude muss dran denken"-Regeln durch — deterministisch, per Hook in `.claude/settings.json` (versioniert, gilt auf PC und Laptop), Skripte in `.claude/hooks/`, Marker-Dateien in `<engine>/.claude_hooks/` (nicht versioniert). Anlass: die Agentic-OS-Recherche vom 04.09. (Guardrails gehören in den Harness) plus die Vorfälle 21.08. (Buch drei Tage ungepusht) und 28.08. (Runner 5,5 h mit altem Code).

| Hook | Was er tut |
|---|---|
| `guard_bash.py` (PreToolUse Bash) | **Blockt** `box_provision_discovery.ps1 -Sync*`, solange kein `regression_ok`-Marker jünger als die Engine-Kern-Dateien ist (engine-regression-tester setzt ihn bei „Sync frei"). **Blockt** `hypothesis_bank.py --enqueue`, solange kein `pipeline_ok`-Marker jünger als `hypothesis_bank.py` ist (pipeline-auditor setzt ihn bei „sauber"). **Blockt** Dauerläufer als Session-Kind (Hub.exe, app_server/lab_app/hub_app/discovery_runner, Start-Process, start_discovery.ps1) ohne `Invoke-CimMethod`/`job_escape`. **Blockt** volles Einlesen von `runner.log`, `results/*.json`, Session-Transkripten. Merkt sich `--push-next` und `funded_finalize`-Läufe als Marker. |
| `guard_read.py` (PreToolUse Read) | Dieselbe Lese-Sperre für das Read-Tool. |
| `after_change.py` (PostToolUse Edit/Write/Bash) | Sagt die Folgepflicht an: `book_state*.json` neuer als letzter Push → finalize + push-next; Engine-Kern → Regressionstest vor Sync; Discovery-Code → Runner-Neustart; Hypothesen-Bank → variant-scout/strategy-auditor/pipeline-auditor; Hub/Lab/Report-Oberfläche → design-guard; neuer Agent/Automatik → Hub-Roster; Logbuch → logbook-distiller; neue `.cs`-Strategie → `NS_MAP`. |
| `on_stop.py` (Stop) | **Lässt die Session nicht enden**, solange `book_state*.json` neuer ist als der letzte `--push-next` (einmal blocken, dann nur noch erinnern). Bewusst kein Push nötig: `python .claude/hooks/mark.py push_next_at`. |
| `session_start.py` (SessionStart) | Inbox-Inhalt + Stale-State (ungepushtes Buch, Kern ohne Regressions-OK) direkt in den Kontext. |

- **Marker von Hand:** `python .claude/hooks/mark.py <regression_ok|pipeline_ok|push_next_at>` aus dem Vault-Root. Der Marker ist der bewusste Unlock — nie setzen, um einen Block „wegzumachen", ohne dass der Agent gelaufen ist.
- **Engine-Pfad:** die Hooks schauen auf `C:\Users\maxlk\Projects\trading-data\engine` (per `MAXLAB_ENGINE` überschreibbar). Der Laptop hat dort eine Kopie vom 03.09.2026, also greifen die Buch-/Sync-Wächter auch dort; die Box bleibt die Quelle der Wahrheit für das Buch. Ohne Engine-Ordner sind nur die Kommando-Wächter aktiv.
- **Ein Hook darf nie die Arbeit blockieren, weil er selbst kaputt ist:** jedes Skript fängt eigene Fehler ab und lässt still durch (`<engine>/.claude_hooks/hook_errors.log`). Hook-Änderungen greifen erst nach `/hooks` bzw. Neustart der Session. Neue Reflex-Regel in der CLAUDE.md → zuerst fragen, ob sie als Hook abbildbar ist (Dateipfad, Kommando-Muster, Dateizeit); Text bleibt für das, was der Harness nicht sehen kann.
- **Noch offen (PC ist aus):** die Hooks als Automatik in `hub_config.json` (`mock_loops`) eintragen, sobald der PC wieder an ist.

### 🔁 Workflow `ein-weg` = Schritt 2 des EINEN Wegs als Skript (Max, 04.09.2026)

`.claude/workflows/ein-weg.js` (Aufruf: Workflow-Tool mit `name: "ein-weg"`, `args: {hypotheses: [{id, title, mechanism, why, market?, family?, source?}]}`). Ablauf deterministisch statt Prompt-Kette: ohne Why harter Stopp → `variant-scout` je Hypothese parallel (mit Strukturausgabe **plus** vollem Report-Text, damit nichts gegenüber dem Handbetrieb verloren geht) → nur die als Testbar/Grenzwertig eingestuften gehen in **einen** `strategy-auditor`-Batch-Call → Entscheidungstabelle je Hypothese (in Bank + H()-Zeile / nachbessern / nicht bauen, mit Grund). Schritt 3/4 bleiben bei der Hauptsession: H()-Zeilen eintragen, `pipeline-auditor` (setzt `pipeline_ok`), `--enqueue --push`. Der Workflow schreibt nie Dateien. Noch nicht mit echten Hypothesen gelaufen (04.09., PC aus) — beim ersten Echtlauf Ergebnis gegen den Handbetrieb gegenlesen.

---

## 🖥️ Box-Fernzugriff (Regel Max, 11.08.2026 — WICHTIG, nie wieder vergessen)

**Claude hat vollen SSH-Zugriff auf die Trading-Box und soll ihn immer selbst nutzen, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.**

- Zugang: `ssh Administrator@100.127.89.9` (Tailscale, Key liegt lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, Zeitzone deutsche Zeit.
- **Laptop ist seit 03.09.2026 als zweites, dauerhaftes Arbeitsgerät eingerichtet** (nicht nur für den Urlaub oben) — gleicher Weg wie vom PC: Vault per Git-Remote (`git@github.com:mkmeboss/my-brain-vault.git`), Engine-/Box-Arbeit per SSH mit demselben Tailscale-Key. Auf dem Laptop läuft kein eigener Discovery-Fallback und kein Hub/Lab-Server — die Box bleibt für beide Geräte die gemeinsame, dauerhaft laufende Instanz.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1` auf der Box (NT8 beenden → Backup außerhalb des NT8-Baums → Staging rein → Pre-Flight-Compile → `dotnet build` → DLL setzen → `obj`/`bin` wieder entfernen). Details und bekannte Fallen: [[VPS-Einrichtung Schritt für Schritt]], [[Strategie-Logbuch]] #084.
- Vor jedem Deploy: NT8-Log des Tages checken ob wirklich nichts Live läuft, danach den kompletten Zielzustand in einem Wegwerf-Ordner vorab kompilieren (`_check_compile.ps1 -SrcDir`), bevor NT8 überhaupt gestoppt wird. Das Leichen-Problem im `_staging` ist seit 11.08. (AP84) im Skript selbst entschärft: `box_deploy.ps1` sagt vor allem anderen die Deploy-Kandidaten an, warnt bei Dateien die es in `Strategies` noch nicht gibt (neues Bein oder Leiche?) und leert das Staging nach erfolgreichem Lauf. Die Ansage trotzdem immer lesen, bevor NT8 gestoppt wird.
- **Wiederanlauf braucht aktuell eine angemeldete RDP-Session** (Autologon fehlt noch, AP86) — NT8 hängt sonst beim UI-Aufbau. Bis das gefixt ist, nach jedem Deploy kurz Bescheid geben, dass eine RDP-Anmeldung nötig ist.
- **Lab-Server ist seit 15.08.2026 multi-threaded** (`ThreadingTCPServer` in `app_server.py`). Vorher blockierte ein laufender Backtest oder Chat jede andere Anfrage und die Oberfläche wirkte tot. Port ist per `MAXLAB_PORT` überschreibbar — wichtig zum Testen, weil Windows sonst eine zweite Instanz still auf denselben Port lässt und man gegen den alten Prozess testet.
- Ticket-Tracker liegt in `C:\Users\maxlk\Projects\trading-data\engine\tasks.json` (Feld `ap_id` = die AP-Nummern, die Max nennt — bei unklaren AP-Nummern immer erst dort nachschauen statt zu raten).
- **⭐ Der Ticket-Tracker ist seit 06.09.2026 zweiseitig (Regel Max).** Max legt Tickets auch direkt auf der Box an (per SSH vom Laptop oder Handy), nicht nur am PC. `tasks.json` wird deshalb bei jedem `inbox_tool.py --pull` von der Box mitgezogen und mit `python discovery/inbox_tool.py --push-tasks` zurückgeschrieben; **die Box ist die Quelle der Wahrheit**. Der Abgleich überschreibt nie blind: Tickets, die nur eine Seite kennt, bleiben erhalten, vor dem Schreiben entsteht ein `.bak`, und eine **Nummernkollision wird gemeldet statt still aufgelöst** (dann schreibt das Tool gar nichts). Vorfall, der zur Regel führte: am 03.09. wurden am PC AP121/122/123 angelegt und nie zur Box gebracht; die Box-Session vom 06.09. hielt die Nummern für frei und vergab sie ein zweites Mal — sechs Tickets unter drei Nummern, und das Lab am PC zeigte AP107 noch als offen, obwohl es längst erledigt war (aufgelöst: die älteren PC-Tickets behalten 121-123, die Box-Tickets wurden AP125/126/127). **Vor dem Anlegen eines neuen Tickets also immer erst `--pull`**, sonst wiederholt sich genau das.
- `inbox_tool.py` erkennt seit 06.09.2026 selbst, ob es **auf** der Box läuft (`_on_box()`, Hostname `vmd202078`) und überspringt den Sync dann, statt per scp eine Selbstverbindung zu versuchen. Das ist die Wurzel des AP124-Vorfalls; `push_next()` hat denselben Bug noch, der bleibt Ticket AP124.
- **Geplant (Max, 11.08.26):** ein zentraler „Deployer" — eine Oberfläche/Skript, in dem Max nur noch die gewünschten Strategien + Parameter einträgt und der Rest (Staging, Pre-Flight, Build, Deploy, Restart) automatisch läuft. Noch nicht gebaut, aber das Zielbild für den Deploy-Workflow — künftige Deploy-Arbeit sollte darauf einzahlen statt Einzelskripte zu vermehren.

### 🔔 RiskGuard neu anlegen → Telegram nicht vergessen (Regel Max, 20.08.2026)
Wenn `MaxRiskGuard` neu an ein Konto gehängt wird (Kontowechsel, Reboot, Neuanlage der Strategie-Instanzen) startet es mit leeren `TelegramToken`/`TelegramChatId`-Feldern — der Code schweigt dann bei JEDER Meldung (Fills, Session-Start, Kill-Switch, Drawdown-Breach) komplett, ohne Fehler oder Log-Eintrag (`if (string.IsNullOrEmpty(...)) return;`). Ist schon mal wochenlang unbemerkt so gelaufen (20.08.: seit dem Kontowechsel auf `E61803453048` am 18.08. keine einzige Telegram-Nachricht mehr).

- **Immer wenn Max ansagt, dass RiskGuard entfernt/neu hinzugefügt/eine neue Strategie-Instanz angelegt wird** (oder nach jedem Box-Reboot/Kontowechsel): aktiv daran erinnern, `TelegramToken` + `TelegramChatId` in den RiskGuard-Parametern neu einzutragen.
- Die echten Werte liegen NICHT hier im Vault (bewusst kein Secret im Git-Repo), sondern auf der Box in `C:\Users\Administrator\maxlab_watchdog.json` (`{"TelegramToken":"...","TelegramChatId":"..."}`, Bot **maxbot** @maxbotalgobot). Beim Erinnern die Werte per SSH von dort holen und direkt mit ausgeben, damit Max sie nur noch in NT8 einfügen muss.

---

## 🖥️ Hub — Max' Desktop-Cockpit (Regel Max, 19.08.2026 — WICHTIG)

Eigene Desktop-App (`C:\Users\maxlk\Projects\hub\`, gebaut als `dist\Hub\Hub.exe`), Discord-artiges Layout mit frei verschieb-/größenbaren Fenstern (Channels+Agents, Vault-Graph „My Brain", Strategy Lab, Gmail, …). **Das wird Max' Hauptarbeitsweg** — der Ort, über den er künftig alles bündelt, nicht nur ein Nebenprojekt.

**Trigger-Regel:** Sagt Max sinngemäß **„Baue im Hub …"** / **„im Hub …"** im Zusammenhang mit einer UI-Änderung oder einem neuen Feature, heißt das automatisch: Projekt ist `C:\Users\maxlk\Projects\hub\`, ohne Rückfrage wohin. Gilt **session-übergreifend** — unabhängig davon, welche Session den Hub zuletzt bearbeitet hat, sofort dort direkt weitermachen (Dateien lesen reicht, kein Nachfragen nötig).

**Nur gezielt ändern:** exakt das umsetzen, was Max ansagt — nicht nebenbei andere Teile der UI mitanfassen, aufräumen oder „verbessern", die er nicht angesprochen hat.

**Hub bleibt offen, nie für Kleinkram neu starten (Regel Max, 19.08.):** Für Änderungen an einzelnen Sub-Apps — Strategy-Lab-Server neu starten, Gmail-Snapshot aktualisieren — **niemals** `Hub.exe` selbst neu starten, sondern nur den betroffenen Prozess bzw. die betroffene Datei anfassen. `static/`, `hub_config.json` und Laufzeitdaten wie `gmail_cache.json` liegen bewusst NEBEN der exe (nicht im PyInstaller-Bundle) und werden vom Server live gelesen (`/api/apps` ohne Cache).

**UI-/Config-Änderung (JS/CSS/HTML/`hub_config.json`):** Datei in `static/` bzw. `hub_config.json` bearbeiten, dann `.\hot_reload.ps1` laufen lassen (synct nach `dist\Hub` per robocopy, triggert `/api/reload` → offenes Fenster macht `location.reload()`, Python-Prozess läuft durch). **Kein Rebuild, kein Neustart, kein Flackern der ganzen App.**

**Rebuild + Neustart NUR bei echter Code-Änderung** an `hub_app.py`/`hub_server.py` selbst (Server-Logik, neue Endpunkte, Fenster-Verhalten): `.\build_exe.ps1`, dann `Hub.exe` neu starten.

### 🗺️ Alles, was wir bauen, zieht automatisch in den Hub nach (Regel Max, 27.08.2026)

Der Hub ist Max' zentrales Cockpit — **jeder neue Agent, jede neue Automatik/jeder neue Loop gehört dort sofort mit rein**, nicht erst wenn Max danach fragt. Sobald ein neuer Subagent unter `.claude/agents/` angelegt wird oder eine neue Automatisierung/ein neuer Scheduled Task entsteht: sofort **ohne Rückfrage** in `C:\Users\maxlk\Projects\hub\hub_config.json` eintragen (Roster `mock_agents` für Agents, `mock_loops` für Automatiken/Cron-Jobs — Name, Rolle/Task in einem Halbsatz, Modell-Tier, Zustand), danach `.\hot_reload.ps1` laufen lassen (Regel oben: kein Rebuild, kein Neustart nötig für eine reine JSON-Änderung).

**Agent-Roster (Stand 27.08.2026, `mock_agents` in `hub_config.json`):**

| Agent | Rolle | Modell |
|---|---|---|
| alpha-scout | Neue Alpha-Mechanismen suchen | opus |
| pipeline-auditor | Meta-Check: rechnen/messen/entscheiden wir richtig | opus |
| strategy-auditor | Adversarialer Gegenleser vor Eval-Deploy | opus |
| quant-mathematician | Formeln/Optimierung für Alpha & Sizing | opus |
| quant-statistician | Beweislage/Unsicherheit für Alpha | opus |
| logbook-distiller | Lehren aus dem Logbuch → Code-Gates abgleichen | opus |
| retro-agent | Wöchentliche Prozess-Retro (So 12:00) | opus |
| backtest-runner | Backtest-/Discovery-Läufe ausführen | sonnet |
| research-scout | Externe Recherche mit Cache-Pflicht | sonnet |
| vault-librarian | Vault/Inbox aufräumen | sonnet |
| ninja-coder | NinjaScript (NT8) | sonnet |
| mc-coder | PowerLanguage (MultiCharts) | sonnet |
| engine-regression-tester | Golden-Master-Check vor Box-Sync | sonnet |
| live-reconciler | Backtest vs. echte NT8-Fills | sonnet |
| box-ops | Infrastruktur-Watchdog Box | haiku |
| session-guard | Parallel-Session-Konfliktcheck | haiku |
| design-guard | UI/UX-Wächter für Hub & alle Apps | sonnet |
| verdict-auditor | Gegenleser für Urteile (tot/gut/fertig) | opus |
| variant-scout | Testarten-Vermesser pro Hypothese, vor dem Bank-Eintrag | opus |

**Automatik-Roster (Stand 27.08.2026, `mock_loops` in `hub_config.json`):** Buch-Sync + Discovery-Loop (~35 Min, Claude-Session), Token-Tracker-Statusline (live), Beleg-Sortierer AP36 (täglich), NT8-Live-Strategien-Watchdog (Handelszeit), **box-ops-Watchdog (stündlich)**, **live-reconciler (täglich nach Handelsschluss)**, **logbook-distiller + retro-agent (wöchentlich, So 12:00)**.

Diese beiden Tabellen sind der Stand zum Zeitpunkt des Schreibens — die Liste in `hub_config.json` ist die lebende Quelle, hier steht sie nur zur Orientierung, welche Kategorien es gibt und dass jede Ergänzung in BEIDEN Dateien passiert (Vault-Regel + Hub-JSON), nicht nur in einer.

---

## 🚫 Dauerläufer NIE als Kind einer Claude-Session starten (Regel Max, 18.08.2026 — hart)

Claude Desktop ist ein MSIX-Paket und läuft in einem Job Object („Desktop AppX Container"). **Jeder Prozess, der aus einer Claude-Session heraus gestartet wird, landet in diesem Job** und vererbt ihn an seine eigenen Kinder weiter. Solange ein einziger Prozess darin lebt, hält er das Claude-Paket für Windows „in Benutzung": Claude lässt sich dann nicht mehr öffnen, wird beim Start sofort wieder geschlossen oder bringt den Dialog „Ein anderes Programm greift gerade auf diese Datei zu" (Fehler `0x80070020`, Ereignisanzeige `Microsoft-Windows-AppModel-Runtime` 208/215, dazu `AppXDeploymentServer` 658 „zurückgestellte Registrierung"). Max hat genau das seit dem Hub erlebt.

**Betrifft alles, was Claude überlebt:** Hub, Lab-Server (`lab_app.py`/`app_server.py`), NT8-Deploy-Helfer, dauerhafte `ssh`-Verbindungen, Discovery-/Backtest-Läufe im Hintergrund.

**Richtig starten** (gemessen 18.08.: `CREATE_BREAKAWAY_FROM_JOB` und `schtasks` bleiben im Job, WMI und `explorer.exe` kommen frei):

```powershell
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = '"<exe>" <args>'; CurrentDirectory = '<ordner>' }
```

Aus Python: `job_escape.spawn([...])` aus `C:\Users\maxlk\Projects\hub\job_escape.py`. Kurzläufer (Backtest im Vordergrund, Grep, Build) sind egal, die sterben mit der Session.

**Der Hub schützt sich seit 18.08. selbst:** `hub_app.py` erkennt am Env-Marker `CLAUDECODE`, dass er in einer Claude-Session hängt, und startet sich per WMI job-frei neu (Protokoll `dist\Hub\hub_launch.log`). `build_exe.ps1 -Run` und `hub_server.ensure_app()` starten ebenfalls job-frei.

**Wenn es doch klemmt:** `C:\Users\maxlk\Projects\hub\tools\Claude entsperren.cmd` doppelklicken (außerhalb von Claude) — listet die blockierenden Prozesse und räumt sie weg. Aus einer laufenden Session: `python tools/claude_unlock.py`.

---

## 🎯 Aktueller Fokus

- **Trading-Pipeline: Eval → Funded → Live.** Einstieg immer über [[Day Trading]].
- **Aktuelle Phase: [[Eval-Passing]]** (Prop-Eval bestehen, **E8**, nicht Apex — Sim-Eval am 03.08.26 bestanden). **⭐ Die erste ECHTE E8 50k Eval läuft bereits live** (Konto aktiv seit dem Kontowechsel auf `E61803453048` am 18.08.26, das Buch handelt sie unbeaufsichtigt von der Box; Stand 25.08.26: ~49.290 $, also leicht unter Start — normal, kein Grund für Kurswechsel). Nicht mehr behaupten, es sei noch keine echte Eval gekauft. Optimiert wird NUR auf hohe Passchance in kurzer Zeit, nicht auf Funded/Payouts.
- **Plattform: NinjaTrader 8 / NinjaScript (C#)** auf Tradovate, nicht MultiCharts/PowerLanguage (siehe [[Tech-Stack]]).
- Nächster Schwerpunkt: **[[Alpha-Suche]]** (First-Passage-Sizing + Cross-Asset-Signale).
- Werkzeuge: [[Backtest-Engine]], [[Portfolio-Simulator]], [[Strategie-Logbuch]].

### 🧭 Stehende Trading-Prinzipien (für JEDE künftige Strategie)
- **⭐ DAS einzige Entscheidungskriterium (Max, 10.08.26, präzisiert 16.08.26 / Logbuch #106):** Bei JEDER Empfehlung/Entscheidung (Bein rein/raus, Parameter, Firma, Kontogröße, Sizing) zuerst fragen: **verbessert oder verschlechtert es die Passquote je Eval bzw. die Kosten pro funded Konto (Preis ÷ Passquote)?** Nicht Einzel-Edge, nicht Sharpe, nicht Eleganz, und **nicht mehr „P(funded) pro Zeit"** — der Zeit-Score belohnt Größe und Nachkauf-Lotterie (Nulldrift-Test: 88 % davon entstehen bei Edge 0). Zeit läuft nur als Kontext mit. Die Rechnung muss auf der ehrlichen Basis stehen: aktuelles Buch, gefixte Engine, **Intraday-Bust-Check** (#077), **Min-Size 1 Kontrakt je Bein**, **Block-Bootstrap** (Vola-Clustering), Nulldrift-Kontrolle und Letzte-3-Jahre-Spalte daneben; bei Bein-Selektion **nested OOS / Marginal-Test „Buch + 1, nur OOS"**. Positive Edge ist notwendig, nicht hinreichend (Präzedenz: OR_DELTA_BIAS #079; bei Min-Size ist „Bein dazu" = „mehr Position", Lehre 82). Kernrechnung: `eval_plan.evaluate_v2` / `cage_policy_lib.evaluate_v2`, Tiers in `cage_v2_tiers.json`.
- **⭐ Buch-Lücke immer mitnennen (Regel Max, 21.08.2026):** Sobald über eine Strategie/Variante/einen Discovery-Kandidaten gesprochen wird, IMMER dazusagen, **was konkret noch fehlt, damit sie ins Buch kommt** — je Strategie eine Zeile, entlang der Stufen: Prämisse → Survivors/Gates → PBO sauber → über Zufallsdecke → Buch-Marginal „besser" (≥ 1,5 pp und 2× Rauschen; Ersatz: „vs Original besser") → Next-Week-Buch + Ticket → Wochenend-Review (Quant-Team + Auditor) → NT8-Deploy. Nicht nur „0 Kandidaten" melden, sondern die Stufe benennen, an der es hängt, und was sie braucht (Zahl, Test oder Modul).
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
