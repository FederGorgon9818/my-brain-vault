---
tags:
  - bereich/trading
  - trading/tooling
erstellt: 2026-09-17
---
# 🛠️ Strategy Developer — Tab im Strategy Lab (seit 14.08.2026)

> [!info] Seit 25.09.2026 heißt der Tab **Workbench** ([[Strategy Lab Workbench]]). Versionen, `developer_run.py`, Chat und Trigger-Regel bleiben gleich, dazu kommen: alle Trades im Chart, Patterns, Filter mit Overfit-Schutz, Urteil nach dem neuen Lineal, „Als Version speichern“, NT8-Overlay.

⬅️ [[Day Trading]] · [[Buch-Workflow]] · [[Backtest-Engine]]

Max entwickelt hier **interaktiv genau eine Strategie in Versionen** — er sagt im Chat, was gebaut/geändert werden soll, Claude setzt es um. Kein Auto-Discovery, Max' eigene Ideen.

**Trigger-Regel (Max, 14.08.):** Sagt Max **„Developer"** im Zusammenhang mit einer Strategie-Idee („bau im Developer…", „Developer: teste mal…"), heißt das automatisch: dieser Workflow, ohne Rückfrage wohin. Claude legt die Version an, rechnet durch und hält den Tab aktuell — nach JEDER Änderung sofort `developer_run.py` laufen lassen, nie nur die Datei ablegen.

## Dateien (alle in `C:\Users\maxlk\Projects\trading-data\engine\developer\`)

- `state.json` = aktive Strategie + Versions-Historie + Archiv (Single Source of Truth für den Tab)
- `versions/<slug>__v<N>.py` = eine Datei pro Version. Vertrag: `META` (name, market, family, rules, why) + entweder `PARAMS` (→ `qbt.run_strategy`) oder `def trades()` (qbt-kompatibler DataFrame mit `r_net`; optional `px_in/px_out/tmin_entry/tmin_exit` für exakte Chart-Marker)
- `developer_run.py --version N` = Rechenkern, schreibt `results/<slug>__v<N>.json`

## Workflow wenn Max eine Änderung ansagt

1. Neue Versionsdatei anlegen (nie alte überschreiben), in `state.json` an `versions` anhängen (`changelog` = was geändert + warum, `base` = Ausgangsversion), `active_version` hochsetzen.
2. `python developer_run.py` laufen lassen (oder Max drückt „Neu durchrechnen" im Tab — gleicher Effekt, Server startet Subprozess).
3. Neue Strategie statt neuer Version? → aktive nach `archive` in `state.json` schieben (`archived`-Datum setzen), neue `active` anlegen mit v1.

## Was jeder Lauf automatisch rechnet

Ehrliche Basis, Käfig aus `book_state.json`: die **komplette Standard-Validierung wie jeder Lab-Report** — `copilot.full_report_data` + `report.build` erzeugen einen 1:1-Lab-Report nach `developer/reports/<slug>__v<N>.html` (Route `/devreports/`), der im Tab eingebettet wird (Ansicht identisch zu den normalen Reports, inkl. Equity, MC-Charts, KPI-Kästen, Prop-Tabellen, Heatmap).

Dazu Developer-spezifisch: OOS-Kontrolle (letzte 30 %), Solo-Frontier (EOD + Intraday #077), Kaufplan-Sicht (#089), **Prop-Firm-Check** (E8-Regeln aus AP90), **⭐ Buch-Beitrag** (P(funded) Buch heute vs. Buch + Strategie — das Entscheidungskriterium) und Preis-Chart mit Trade-Markern. Buch-Beine sind gecacht in `developer/book_cells.json`, Key = Hash der legs aus `book_state.json` (invalidiert sich selbst). Sagt Max nach der Entwicklung „ins Buch": normaler Weg über `book_state.json` → `funded_finalize.py` ([[Buch-Workflow]]).

**Rollback:** Max klickt im Tab auf eine ältere Version (aktiviert + rechnet sie), oder sagt es im Chat. Versionen sind append-only.

## 💬 Chat im Developer (Max, 15.08.2026)

Rechte Spalte im Developer-Tab: Max redet dort direkt mit Claude über die Anthropic-API, Claude legt Versionen an, rechnet durch und beantwortet die Buch-Frage. **Das ist ein zweiter Claude, nicht die laufende Claude-Code-Session** — gleiche Tools und gleicher Kontext, aber eigener Verlauf.

- Tool-Schicht + Chat-Runner: `dev_agent.py` (14 Tools: `dev_status`, `list_strategies`, `read_version`, `write_version`, `new_strategy`, `select_strategy`, `run_version`, `get_result`, `compare_versions`, `set_goal`, `save_report`, `read_book_state`, `search_engine`, `read_engine_file`).
- **Bewusst EINE Tool-Schicht:** ein späterer MCP-Server importiert dieselben Funktionen, statt sie zu kopieren. Neue Developer-Fähigkeit → als Tool in `dev_agent.py`, nicht als Sonderweg im Server.
- **Schlüssel:** `ANTHROPIC_API_KEY` oder Datei `engine/.anthropic_key`. Abrechnung läuft über die API, **getrennt vom Claude-Code-Abo** (AP95). Modell/Effort in `developer/agent_config.json`, Standard `claude-opus-5` / `high`.
- **Report speichern nur auf Ansage:** Developer-Läufe bleiben unter `developer/reports/`. Erst wenn Max „Report speichern" sagt, kopiert `save_report` HTML + `meta.json` nach `reports/` und der Report taucht in der Lab-Seitenleiste auf.
- **Strategie wechseln:** „ich will die und die Strategie bearbeiten" → `select_strategy(slug)` holt sie aus dem Archiv zurück, die bisher aktive wandert hinein.
- Chat läuft job-basiert (senden → ID → pollen), damit ein 15-Minuten-Backtest sichtbar läuft und nie in einen Browser-Timeout rennt. Verlauf in `developer/chat.json`.

## 📊 Charts im Developer = Charts im Lab-Report (Max, 15.08.2026)

Equity-Kurve und Monte Carlo im Developer-Tab sind **1:1 dieselbe Darstellung wie in den Lab-Reports**: gleiche Chart.js-Defaults (Mono-Schrift, Achse `#78776f`, Grid `rgba(255,255,255,.05)`), gleiche Kartenhöhen (Equity und Fächer 580 px, Histogramme 300 px), gleiche Farben und Linienstärken. Die Werte sind aus `report.py` kopiert — **ändert sich dort etwas, muss es in der `HUB`-Sektion von `app_server.py` mitgezogen werden**, sonst driften Report und Developer optisch auseinander.

Dazu Developer-spezifisch: OOS-Fenster in der Equity blau hinterlegt, Perzentil-Kegel und Preis-Chart mit Trade-Markern. Die Chart-Rohdaten sind groß und laufen deshalb über `/api/dev/charts` statt über den 4-Sekunden-Poll.

**Ganz oben im Tab** steht immer die eine Frage in Klartext: verbessert sie das Buch, ja oder nein — plus eine Warum-Zeile, die das Delta gegen das MC-Rauschen einordnet.

**Ziel-Banner (Max, 14.08.):** `state.json` hat ein Feld `goal` (`book` | `solo`), im Tab oben umschaltbar. `book` = Entscheidung „✓/✗ ins Buch" (verbessert es P(funded) des aktuellen Buchs — Deltas 3m/6m, Median, Kosten), `solo` = „käfigtauglich ja/nein" (≥60 % in ≤50 Tagen, Intraday). Der volle Lab-Report wird NICHT mehr eingebettet (Max' Wunsch), sondern ist als Link „voller Lab-Report ↗" am Regelwerk erreichbar (Route `/devreports/`, liefert auch `chart.min.js` aus `reports/` mit — sonst bleiben die Report-Charts leer).

## Zwei Fallen

**Buch-Beitrag ist rauschbewusst** (seit 14.08., Vorfall NQ-ORB-Breakout-Demo): ein einzelner MC-Lauf (4000 Sims) schwankt beim Delta locker ±1-2pp allein durchs Sampling — ein Bein mit eindeutig negativer Edge zeigte auf einen Blick "+1,4pp verbessert das Buch". `book_contribution()` in `developer_run.py` rechnet deshalb über **5 unabhängige Seeds**, nimmt die Streuung als Rauschmaß und verlangt vom Delta mindestens das Doppelte davon (min. ±1,5pp), sonst "neutral" statt "besser/schlechter". Gilt bei jeder künftigen Änderung an der Buch-Beitrags-Logik: nie ein einzelner Seed als Entscheidungsgrundlage.

**`mode="orb"`** ([[Strategie-Logbuch]] #066/#067): der Default `orb_exec="book"` hat Look-ahead (Volumen-/VWAP-Filter werten die komplette Ausbruchs-Bar aus, der Fill ist aber schon vorher). Jede Developer-Version mit ORB-Modus braucht **explizit** `orb_exec="close"` (echte Live-Logik) oder `"stop_honest"` (Level-Fill via ruhende Order) — sonst zeigt die Strategie eine Schein-Edge, die live nicht existiert.
