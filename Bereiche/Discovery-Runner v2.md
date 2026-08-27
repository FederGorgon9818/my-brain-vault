---
tags:
  - bereich/trading
  - trading/alpha
  - trading/tooling
erstellt: 2026-08-18
---
# 🤖 Discovery-Runner v2 — die Maschine sucht, Claude entscheidet

⬅️ [[Alpha-Suche]] · [[Discovery-Prozess (wie wir Alpha finden)]] · [[Strategie-Logbuch]] #118 · [[Backtest-Engine]]

> [!important] Kernidee (Max, 18.08.2026)
> **Rechnen macht die Maschine, denken macht Claude.** Der Runner läuft auf der Box als Dauerprozess (niedrige Prio, Pause im US-Handel), arbeitet eine Queue von Such-Jobs ab, filtert ehrlich und legt Kandidaten in eine Inbox. **Kandidaten mit belegtem Vorteil gehen automatisch ins Next-Week-Buch (`promote_next.py`, alle 30 Min auf der Box) — nie ins Live-Buch.** Die Übernahme ins Live-Buch bleibt die Wochenend-Entscheidung über das Ticket (Quant-Team + Auditor). PC darf aus sein.

## Warum die alten Batches nichts fanden (Diagnose 18.08.)
1. **Abgegraster Raum:** Param-Grids auf bekannten Mechanismen, gleiche 4 Indizes, gleiche Minutenbars. Engpass ist Mechanismen-Vielfalt, nicht Kombinatorik.
2. **Filter zu grob und zu spät:** „edge ≥ 3 %" ließ Tail-Lotterien durch (NR7-EOD) und warf unkorrelierte Dünn-Edges raus; das Buch-Kriterium kam erst ganz am Ende (Auto-Fit).
3. **Kein Gedächtnis:** ~20 Einzelskripte, ~1400 Trials, niemand zählte global mit → Zufallsdecke pro Skript statt pro Gesamtsuche.

## Was der Runner anders macht
| Stufe | Was | Warum |
|---|---|---|
| **0 Prämisse** | Kern-Config(s) zuerst: n ≥ 60, IS expR > 0, IS-Edge > 0. Sonst **kein Grid** | Lehre 113 (Prämisse vor Sweep messen, AP61 sparte den ganzen Cross-Asset-Sweep) |
| **1 Grid + Gates** | IS/OOS (fixes Datum 01.01.2024), n ≥ 100 / OOS ≥ 25, tpy ≥ 25, Edge ≥ 1 pp (3 pp bei n < 200), **Top-5-Anteil ≤ 60 %**, **letzte 3 Jahre ≥ 0**, **Block-Bootstrap P(mean>0) ≥ 0,85**, **Plateau** (≥ 50 % der Grid-Nachbarn expR > 0), dazu PBO/DSR/Reality-Check über `overfit.discovery_report` und **Zufallsdecke** E[max SR \| Null] gegen die Trialzahl des Jobs UND des gesamten Registers | Tail-Lotterie, Spitze-statt-Plateau, Multiple Testing |
| **2 Buch-Marginal** | Für die Top-Survivors (nach OOS-Sharpe): `developer_run.book_contribution` — v2-Passquote Buch vs. Buch + Kandidat, 5 Seeds, Rausch-Schwelle. Bei Exit-Sweeps Ersatz-Semantik (`replaces_leg`): Vergleich gegen das **Original-Bein** | ⭐ das einzige Kriterium (#106) — keine zweite Kopie der Mathematik |

**Register** (`registry.json`): jeder je gerechnete (mode, symbol, params) mit Ergebnis. Backfill 18.08.: **1390 Alt-Trials** aus 22 Ergebnisdateien. Zufallsdecke damit ~1,0 Sharpe (statt 0,1 wenn man nur den einzelnen Lauf zählt). Wichtig: die SR-Streuung für die Decke ist die **theoretische** 1/√Jahre, nicht die gemessene über die Configs (Exit-Varianten desselben Entries sind hoch korreliert → Scheindecke).

## Dateien (`C:\Users\maxlk\Projects\trading-data\engine\discovery\`)
| Datei | Zweck |
|---|---|
| `discovery_runner.py` | Daemon: Queue → Stufen → results/registry/inbox. `--once`, `--job ID [--force]`, `--dry`, `--status` |
| `discovery_lib.py` | Gates, Grid-Expansion (Profil-Achsen mit `_label`), Bootstrap, Register, Buch-Marginal, Inbox-Rendering |
| `queue.json` | Jobs (Felder siehe `_doc`). Runner setzt `status/started/finished/result` |
| `registry.json` | Trial-Register (`n_total`, `trials{key}`) |
| `inbox.json` / `inbox.md` | Kandidaten + Job-Abschlüsse; `seen`-Flag |
| `inbox_tool.py` | **Morgen-Check**: Status + ungelesene Einträge kompakt; `--seen-all`; `--add-job job.json` |
| `results/<job>.json` (+ `.meta.json`) | summarize_results-Schema (`python summarize_results.py discovery/results/<job>.json`) + Job-Meta (Prämisse, Decke, Selektion, Original-Buch-Score) |
| `runner_config.json` | `poll_sec`, `pause_hours` (Box seit 20.08.: `[]` = 24/7, Max' Ansage; vorher `[[15,22]]`), Prio |
| `start_discovery.ps1` | job-frei starten (WMI), `-Stop`, `-Status` |
| `backfill_registry.py` | Alt-Ergebnisse ins Register (idempotent) |
| `promote_next.py` | **Auto-Übernahme ins Next-Week-Buch**: bester Kandidat je Bein (Ersatz: vs Original besser; neu: besser + über Zufallsdecke) → `book_state_next.json` (Backup, `next_week.changes` mit `auto`), `funded_finalize --next` + `live_finalize --next`, Ticket vormerken. `--box-mode` (Box: Tickets → `pending_tickets.json`), `--dry`. Konflikte (Bein im Next-Buch schon geändert) → nur Inbox-Hinweis |
| `box_provision_discovery.ps1` | Box: `-SyncOnly` (Engine-Update), `-Stop`. Provisionierung selbst ist am 18.08. erledigt |
| `STOP` (Datei) | sauberer Stopp nach dem laufenden Config; `runner.lock` = eine Instanz je Maschine; `runner_heartbeat.json` |

## Betrieb (seit 18.08.2026 23:06 auf der Box)
- **Wo:** Box `VMD202078`, `C:\Users\maxlk\Projects\trading-data\engine\discovery\` (gleicher Pfad wie am PC — `qbt.py`, `asian.py` & Co. haben absolute Pfade), Python 3.11.9 all-users (`C:\Program Files\Python311`), numpy 2.4.6 / pandas 3.0.3 / pyarrow 24 / scipy 1.17. Payload (Engine ohne `.app_profile`/Reports/Caches + `exported_data` inkl. RTH-Cache, 448 MB) als tar-Zip rüber, mit `tar -xf` entpackt (Expand-Archive nimmt tar-Zips nicht). Start job-frei via WMI (`Invoke-CimMethod Win32_Process Create`), **seit 20.08.2026 `pause_hours []` = 24/7-Betrieb** (Max' Ansage; BELOW_NORMAL schützt NT8 — bei Auffälligkeiten im Live-Handel wieder `[[15,22]]` setzen, Config wird je Schleifendurchlauf neu gelesen, kein Neustart nötig), BELOW_NORMAL. Erster Backtest je Symbol dauert länger (Cache-Aufbau, Asian 73 s), danach ~3–7 s je Config.
- **Scheduler-Tasks auf der Box** (Benutzer Administrator, laufen solange die RDP-Session angemeldet ist — dieselbe Bedingung wie NT8, AP86): „MaxLab Discovery Runner" (alle 30 Min `discovery_runner.py`; der Lock lässt nur eine Instanz zu, also reiner Keepalive/Neustart) und „MaxLab Discovery Promote" (alle 30 Min `promote_next.py --box-mode`).
- **Lokaler Ordner = Spiegel.** `python discovery/inbox_tool.py --pull` holt Heartbeat/Queue/Register/Inbox/results **plus** `book_state_next.json`, `portfolio_next.json`, `live_portfolio_next.json`, die zugehörigen Reports und vorgemerkte Tickets (→ `tasks.json`) von der Box; `--seen-all` (Merge, keine Box-Einträge gehen verloren), `--add-job` und `--push-next` schreiben zurück. Läuft automatisch über `auto_check.py` alle 30 Min, solange der PC an ist. **Manuelle Next-Buch-Änderung am PC → `--push-next`**, sonst promotet die Box in einen alten Stand. `start_discovery.ps1` lokal nur als Notnagel, nie parallel zur Box.
- **Queue-Race-Falle (20.08.2026 passiert):** Läuft auf der Box gerade ein Job, hält der Runner die Queue im Speicher und schreibt sie beim Job-Abschluss zurück — Jobs, die währenddessen per `--add-job` gepusht wurden, werden dabei still überschrieben und verschwinden. Deshalb nach jedem `--add-job`, während der Runner rechnet, ein paar Minuten später gegenprüfen, ob der neue Job noch in der Box-Queue steht (zwei HF-Jobs mussten am 20.08. neu eingereiht werden).
- **Engine-Sync:** Änderung an Engine-Code am PC → `box_provision_discovery.ps1 -SyncOnly` vor dem nächsten Nachtlauf (RV-Leadlag-Falle: alter Code = falsche Zahlen).
- **Morgen-Check (Claude, Session-Start):** `python discovery/inbox_tool.py --pull` → Kandidaten mit „besser" (bzw. „vs Original besser") → Quant-Team + `strategy-auditor` → Next-Week-Buch + Ticket → `--seen-all`. Runner-Log oder volle results NIE einlesen (Token-Disziplin).
- **Neue Jobs:** Job-JSON schreiben (Mechanismus, Familie, **Why vorab**, `base`, `grid`, ggf. `premise.configs`, `replaces_leg`) → `inbox_tool.py --add-job`. Faustregel: kleine, flache Grids (≤ 100 Configs), Prämisse-Configs mit dokumentiertem Why.
- **Kosten:** ~2 s je Config (warmer Cache), Buch-Marginal ~6 s je Kandidat, PBO ~10 s je Job. 336 Configs ≈ 15–20 min.
- **Box:** 6 Kerne, 12 GB, 183 GB frei — seit 18.08. 23:06 provisioniert und Hauptort des Runners (siehe Betrieb). Die ersten drei Jobs (Momentum/LastHour/Gap-fade) liefen noch am PC und wurden rübergesynct; die Box hat Asia-Dir + VWAP-Pullback übernommen.

## Erster Lauf (Nacht 18.→19.08.)
Exit-Sweep über 5 Buch-Beine (ORB-fade bewusst nicht: fliegt per Next-Week raus, `orb_exec`-Falle): NQ_Momentum (72), NQ_LastHour (60), RTY_Gap-fade (72), NQ_Asia-Dir (72), NQ_VWAP-Pullback (60). Frage je Bein: hebt eine Exit-Variante die v2-Passquote des Buchs gegenüber dem Original (Pfad-Varianz), nicht „mehr expR".

**Nebenbefund Smoke-Test:** NQ_Momentum als Bein macht das aktuelle 6er-Buch um **−1,8 pp schlechter** (Basis ohne Bein 77,0 % → mit 75,2 %, Rauschen 0,7); NQ_LastHour analog −1,9 pp. Passt zu AP104 Leave-one-out (Lehre 82: bei Min-Size ist „Bein dazu" = „mehr Position").

**Erste Auto-Promotion (18.08. 23:16):** `NQ_Momentum → NQ_Momentum_d260818` (eod, `rev_stop_mult 0.3`, `be_trigger 0.5`; vs Original **+5,4 pp** v2-Passquote, Buch-Marginal „besser" +3,6 pp, Rauschen 0,5). Job: 72 Configs, 19 Survivors, PBO „ok", 6 Kandidaten. ⚠️ Fürs Wochenende: `be_trigger` ist ein Break-Even-Overlay — genau das stand in **#046 auf dem Friedhof** (BE/Trailing-Overlay). Entweder wirkt es hier nur in Kombination mit dem engeren Stop (0,3 statt 0,4) oder es ist Multiple Testing über 8 Buch-Marginal-Picks. Quant-Team + Auditor müssen das vor der Übernahme klären; bis dahin läuft es nur im Next-Buch.

## Fulltime-Betrieb (Regel Max, 21.08.2026)
Die Queue darf **nie leerlaufen** — Fokus aktuell HF (mehr Trades/Jahr). Erster Versuch (9 `hf_*`-Jobs von Hand) war in 2 h durch: 5 an der Prämisse gestorben, 4 ohne Kandidat. Deshalb seit 21.08. 16:50 **`job_generator.py` im Runner-Loop** (`min_pending` 3):

1. **Folge-Jobs** zu jedem fertigen Job mit Survivors (auch handgebaute): *refine* = feineres Grid um den besten Survivor (Rangfolge OOS-Sharpe > 0, dann Trades/Jahr — HF-Fokus; Schrittweite halbiert, ≤ 3 Achsen), *exits* = Exit-Profil-Sweep (Target/BE/Zeit-Stop je Modus) auf dem besten Survivor.
2. **Abdeckung**: 11 Vorlagen × 4 Märkte (ts_momentum, ts_fade, last_hour, gap fade/continuation, orb_break mit close-Exec, i2 volbrk/vwap_pull/ib_ext/on_rev, asian us_dir, asian fade/break) im Round-Robin, jede mit Why + 2 Prämissen-Configs.
3. **Tiefe** bis 3, dann ausgereizt → `queue_empty` → Claude muss neue *Mechanismen* liefern (Engine-Modul + Eintrag in `TEMPLATES`), nicht mehr Grid.

**Kosten-Stress-Gate (seit 21.08.2026, [[Strategie-Logbuch]] #125):** `DEFAULT_GATES.cost_stress_ticks = 2.0` — jeder Config wird `r_net` analytisch auf 2 Ticks Slippage je Seite umgerechnet (`discovery_lib.stress_costs`, Limit-Entry/Target-Exit zahlen wie in AP74 keinen Spread); expR gesamt und OOS müssen positiv bleiben, sonst `fails=["cost2t"]`. Kandidaten in der Inbox zeigen die Stress-Zahl. Grund: bei 200 tpy entscheidet ein halber Tick, `NQ_Momentum_d260821` fiel im Test von 0,10 auf 0,05 expR @2t und unter null @3t. `None` im Job-`gates`-Block schaltet es ab.

Register-Pruning (Job fällt weg, wenn < 4 Configs neu), max. 120 Jobs/Tag, `replaces_leg` automatisch, wenn Modus+Markt einem Buch-Bein entsprechen. Zustand in `generator_state.json` (wird mit `--pull` gespiegelt). Ehrlichkeit: die Zufallsdecke steigt mit jedem Job — Brute Force kann sich keine Edge erschleichen, die Prämisse-Stufe killt tote Vorlagen nach 1–2 Backtests.

## Offen / nächste Ausbaustufen
- Register-Merge Box → PC; Job-Typen „Regime-Conditioning" (Ein/Aus-Schalter für bestehende Beine) und „Event-Bein" (braucht Engine-Modul); Kandidaten-Karten im Strategy Lab (Tab) statt nur `inbox.md`.
- Ehrlich: mehr Alpha kommt nur mit **neuen Inputs** (Tick/L2, Optionen-Positionierung, Breadth). Der Runner macht die Suche sauber und billig, aber er zaubert keine neuen Mechanismen aus alten Minutenbars.
