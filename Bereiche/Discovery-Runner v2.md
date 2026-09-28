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

## Varianten-Vorlagen: Vorrat für Wochen ohne Session (Max, 06.09.2026)
Befund 06.09.: Queue seit 03.09. 22:00 leer, `queue_empty` zweimal täglich, Box 4 Tage still. Alle 130 Vorlage×Markt-Schlüssel vergeben, Folge-Jobs bis Tiefe 3 abgehakt, `hypothesis_bank.py` restlos eingereiht, `jobs_proposed/` leer. Die Bilanz seit 18.08.: 556 Jobs, nur **43 h Rechenzeit in 20 Tagen (~9 % Auslastung)**, ein Job im Median 2,3 min (p90 9 min), 9,4 s je Config. Eine handgebaute 10-Job-Runde war deshalb in 4-6 h durch und die Queue wieder leer (Scout-Report 03.09., Abschnitt 7).

**Lösung = vierte Quelle im Generator (`VARIANT_SPECS` / `build_variants()` in `job_generator.py`):** jede tsmom/maband-Vorlage (22 Stück) wird programmatisch geklont, je Klon EINE im Register nachweislich leere Achse. Nur tsmom/maband, weil nur diese zwei Modi einen Null-Schalter haben (`controls.py ctl_null`) und deploy_ready werden können. Reihenfolge = Priorität, HF zuerst:

| Suffix | Modus | neue Achse | Register-Beleg (n=17.639) | Prio | Configs | ~Stunden |
|---|---|---|---|---|---|---|
| `_mt` | maband | `mb_max_trades` 2/4/6 | ≠1 nur in 238 von 2.990 | 52 | 16.848 | 44 |
| `_hf` | tsmom | Profil `tm_sig_len`/`tm_thr` 10/0,0015 · 5/0,0015 · 5/0,001 | len 15 + thr 0,003 in 7.470 von 9.255 | 52 | 45.360 | 118 |
| `_tfm` | maband | `mb_bar_min` 1/2/3 | 184 von 2.990 | 48 | 16.848 | 44 |
| `_tf` | tsmom | Profil `tm_bar_min` 3/5 × `tm_signal` signratio/wins, Fenster 30 min | 0 von 9.255 | 44 | 45.360 | 118 |
| `_gegen` | maband | `mb_side=against` / anderes Band-/VWAP-Ereignis | against 29 von 2.990 | 42 | 8.208 | 21 |
| `_spaet` | beide | `tm_sig_start` / `mb_start_min` 120/210 | < 2 %, 0 Survivors (Reserve) | 36 | 41.472 | 108 |
| `_kal` (neu 06.09. spät) | beide | Profil Kalender-Gates: aus / Monatsende ±3 Tage / außerhalb / OpEx-Woche ja / nein / Roll-Woche | Gates neu, 0 Trials | 50 | ~124.000 | ~325 |
| `_dix` (neu 06.09. spät) | beide | Profil Dark-Pool-Index (Vortag): aus / DIX ≥ 0,45 / DIX ≤ 0,40 | `dix_prev` lag ungenutzt in `daily_context` | 49 | ~62.000 | ~162 |
| `vwap_pullback_leg` (Vorlage, kein Klon) | vwap_pullback | Stop/Ziel in Punkten, ATR-Abstand, 1h-Trendfilter um die Live-Defaults | Modus hatte nie eine Vorlage (128 Trials) | 58 | 81 | 0,2 |

Summe ohne `_kal`/`_dix` **174.096 Configs ≈ 455 h ≈ 22 Tage bei 20 h/Tag**, mit den beiden Gate-Varianten ~360.000 Configs ≈ 940 h (Reihenfolge: `_mt`/`_hf` → `_kal` → `_dix` → Rest) (Single-Process), plus die automatische Refine-/Exit-Kette. Ein Varianten-Job hat 324-1.080 Configs, also 50 min bis ~3 h, damit fällt die Queue nicht mehr nach Stunden leer. Die Prämisse jedes Klons setzt die neue Achse auf den mittleren Wert, damit die Prämissen-Stufe die Variante prüft und nicht die schon gerechnete Basis. Preis: die Zufallsdecke steigt mit √(2 ln n) um rund +15 %, bewusst in Kauf genommen.

**Pipeline-Audit vor dem Neustart (06.09., zwei Runden):** (B1) `tm_bar_min` ist bei `tm_signal=ret` mathematisch wirkungslos (Fenster-Return ist aggregationsinvariant), deshalb läuft `_tf` nur mit Signaltypen, die die Bar-Struktur lesen (signratio/wins), und mit 30-Minuten-Fenster, damit genug Bars im Fenster sind. (B2) Das Register wurde alle 10 Configs komplett neu geschrieben (1,4 s bei 17k, 15 s bei 190k Einträgen, hochgerechnet ~4 TB Schreiblast über den Urlaub): `discovery_runner.py` schreibt es jetzt nur noch alle 200 Configs und am Jobende (`registry_write_every_configs`), die Ergebnisdatei weiter alle 10.

**Übergabe für den Urlaub (Kartierungslauf, bewusst so entschieden 06.09.):** erwartete deploy-fähige Kandidaten ≈ 0, weil alle Varianten als „neues Bein" gegen das Buch laufen (siehe Grenzen unten) und HF-Score mit dem Buch-Score negativ korreliert (Spearman −0,81, #139). Der Ertrag ist Registerwissen über sechs bisher leere Achsen; der Preis ist eine dauerhaft um ~11-15 % höhere Zufallsdecke für jede künftige Hypothese. **„0 Kandidaten" nach dem Urlaub ist deshalb das erwartete Ergebnis und kein Filter-Bug.** Interessant sind Survivors/PBO je Variante und die Monotonie-Fragen (Ertrag je Trade vs. `mb_max_trades`, Gegenseite vs. Basis). Die Ersatz-Slot-Frage (welches Buch-Bein einen Varianten-Fund ersetzen dürfte) bleibt Max' Entscheidung im Ticket Buch-Komposition.

Zwei Fixes im selben Zug: `fill()` speichert den Generator-State auch bei 0 akzeptierten Jobs (vorher gingen die `n/a`-Marken verloren und der Runner versuchte alle 2 Minuten dieselben zwei Duplikate), und `_finer_values` hält Integer-Achsen ganzzahlig (`tm_bar_min` 7,5 wäre Unsinn).

**Nachtrag 06.09. spät (Max: „Kandidaten, nicht Beschäftigung"):** (a) Generischer Null-Schalter `qbt._null_direction` für ts_reversal, last_hour, asian (us_dir) und vwap_pullback, dazu `ctl_delay` für asian → alle vier Buch-Modi können jetzt `deploy_ready` werden, also Ersatz-Kandidaten gegen `replaces_leg` liefern. (b) Neue Gate-Achsen in `sigcore`: Kalender-Flags (`mend_off`, `opex_week`, `roll_week`, `dto_opex`; Gates `tm_mend_within/outside`, `tm_opex_week`, `tm_roll_week`, `tm_dto_opex_max`) und `tm_dix_min/max`. Das sind neue ökonomische Bedingungen (Monatsende-Rebalancing, OpEx-Pinning, Roll-Woche, Off-Exchange-Akkumulation), keine neuen Parameter. Stichprobe NQ-Momentum ungegated: `tm_mend_within=3` n 284 statt 813, expR +0,60 statt +0,22 (IS, Vorsicht). (c) Jeder Generator-Job trägt `tag` (`vacation_variants_0906` / `generator_coverage`), Rausnehmen siehe CLAUDE.md „Queue-Stand Urlaub". Rest der Liste (Ersatz-Slot-Semantik, Trade-Size-Gate, Ideen-Schleife, neue Futures): Ticket AP137.

**Bekannte Grenzen (nicht gelöst, nur benannt):** (1) Buch-Marginal läuft für alle Varianten als „neues Bein", weil `book_leg_for` für tsmom/maband kein Buch-Bein findet, und „neues Bein" hat laut #139/B3 noch nie funktioniert (577 Evals, 0 Treffer). Ein Fund zeigt sich also eher an Survivors/PBO als am Buch-Score. (2) Der Runner rechnet weiter auf einem von sechs Kernen; Parallelisierung über die Config-Schleife wäre der nächste 4x-Hebel. (3) `ctl_null` für die anderen 20 Modi fehlt weiterhin (Ticket „Pipeline-Fixes aus Audit #139").

## Register-Pending-Weg (seit 14.09.2026, AP153 P10 / AP122 P1 Minimalbau)

Externe Schreiber (Prescans, Backfill, Hand-Sweeps) fassen `registry.json` **nie** direkt an (kein Lock, Lehre 144 zweimal verletzt). Stattdessen: `discovery_lib.registry_pending_add({key: entry}, source=...)` legt `discovery/registry_pending/<uuid>.json` ab. `load_registry()` mischt beim nächsten Laden alle Pending-Dateien **append-only** ein (ein vorhandener Key wird nie überschrieben, `n_total` zählt nur neue Keys), `write_registry()` schreibt das Register und löscht erst danach die eingemischten Dateien. Der Runner benutzt `write_registry` an allen drei Schreibstellen. Prescans (`mode="prescan"`) zählen damit als Trials (Zufallsdecke gegen `n_global`), Key = sha1 der Pseudo-Params (`prescan`, `symbol`, `step`, `arm`/`norm`). Noch offen aus AP122: `registry_add` ohne `runner.lock`-Besitz verweigern, `register_cf.py`/`backfill_registry.py` auf den Pending-Weg umstellen.

Ebenfalls seit 14.09.: jeder Job aus der Hypothesen-Bank trägt `null_ref` (welche `controls.py`-Kontrolle die mechanische Null liefert; `none:…` bei Modi ohne Null-Schalter), Inbox-Kandidaten tragen `prior`/`prescan`/`null_ref`, und `promote_next` promotet `prior=low` ohne vertraglichen Prescan (`prescan_contract.ok` in der `*_results.json`) sowie `null_ref none:*` nie automatisch.

## 🔬 Der EINE Weg für jede Strategie-Idee (Regel Max, 23.08.2026 — verbindlich)

**Es gibt genau einen Weg, wie eine Idee getestet wird. Nicht mehrere Arten, sondern eine Art, die dafür sehr intensiv läuft.** Gilt für jede neue Strategie, jede Hypothese, jeden Discovery-Job, jede Developer-Version. Wer davon abweicht, braucht einen ausdrücklichen Grund von Max.

**Die vier Schritte, immer in dieser Reihenfolge:**

1. **WHY zuerst.** Kein Test ohne Mechanismus im Klartext: wer muss handeln, warum, und warum bleibt das Geld liegen. Ohne Why kein Job — das Feld ist Pflicht und wird beim Job-Bau geprüft (`assert` in `hypothesis_bank.py`).
2. **Dann die ARTEN.** Eine Hypothese wird **nie als eine Strategie** getestet, sondern als **mindestens zehn Implementierungen desselben Mechanismus**: andere Fensterlänge, anderer Signaltyp, andere Bestätigung (Volumen / Delta / EMA12 / EMA20 / VWAP-Seite), anderer Stop (Range/Sigma/ATR), anderer Exit (EOD/Zeit/RR). Baustein: `AX_CONFIRM` / `AX_RISK` / `AX_EXITS` in `hypothesis_bank.py`. Weniger als zehn Varianten lässt der Job-Bau nicht zu. Übernimmt seit 01.09.2026 `variant-scout` (Vorfrage: wie viele ECHTE Varianten gegen die Engine-Achsen, Doppelzählungs-/Kontaminationswarnung gegen die Bank). Direkt danach `strategy-auditor` im Batch-Vorprüfungs-Modus — EIN Aufruf über die ganze Gruppe testbarer Hypothesen, reine Story-Prüfung, bevor Box-Rechenzeit verbrannt wird. Der Vollmodus-Trigger (adversarialer Gegenleser mit Backtest-Ergebnis, kurz vor Eval-Deploy) bleibt zusätzlich bestehen.
3. **Dann die bekannten FALLEN — als Vorbedingung, nicht als Nachgedanke.**
   - **`GATES_HARD`** (`discovery/hypothesis_bank.py`) für jede Grid-Zelle: min. Trades/OOS-Trades/Trades pro Jahr, Top-5-Konzentration ≤ 50 % (#038), Block-Bootstrap P ≥ 0,90, Plateau statt Spitze, letzte 3 Jahre nicht negativ (#057), Kosten-Stress 2 Ticks je Seite.
   - **`discovery/controls.py`** für jeden Kandidaten, der das Buch-Marginal besteht: Look-ahead-Delay (#066/#067), Long-Bias (Goyal/Jegadeesh, #108), Nulldrift mit gewürfelter Richtung, Multi-Markt (#051), Epochen-Split 2016-2019 vs. 2022-2026 (#057), Zufallslevel bei Level-Strategien, Tages-Korrelation zum Bestandsbuch ≤ 0,70 (#079, Lehre 82).
   Erst wenn alles davon steht, ist ein Fund **`deploy_ready`**. `promote_next.py` promotet nur noch deploy_ready-Kandidaten automatisch ins Next-Week-Buch.
4. **Dann rechnen, lange und breit.** Auf der Box, nicht im Chat. Jobs kommen aus `python discovery/hypothesis_bank.py --enqueue --push`.

**Werkzeuge (statt neue Einzelskripte):**

| Datei | Rolle |
|---|---|
| `engine/sigcore.py` | gemeinsame Signal-/Ausführungsschicht: Bars, Averages, RVOL, Delta-Proxy, Tageskontext (immer um einen Tag verschoben), ehrliche Trade-Simulation, alle Gates an EINEM Ort |
| `engine/tsmom.py` (`mode="tsmom"`) | verallgemeinertes Time-Series-Momentum: Fenster, Signaltyp (ret/zscore/rank/rangepos/signratio/accel/jerk/wins), Basis (open/prev_close/prev_rth/overnight), Schwelle in % oder σ |
| `engine/maband.py` (`mode="maband"`) | Averages, Crossover, Geschwindigkeiten, Bänder, Kanäle, Anker-VWAP — teilt sich Ausführung und Gates mit `tsmom` |
| `discovery/hypothesis_bank.py` | Hypothese → Job mit ≥ 10 Implementierungen, Why, harten Gates |
| `discovery/controls.py` | die Lehren aus den Fehlschlägen als automatische Batterie |

**Neue Idee heißt: neue Zeile in `hypothesis_bank.py`** (bei wirklich neuem Mechanismus ein neuer `mb_kind`/`tm_signal` in den bestehenden Modulen) — nicht ein neues Skript daneben. Nur so zählt das Register jeden Trial mit, nur so gilt dieselbe Zufallsdecke, nur so ist der Look-ahead-Check an einer Stelle statt an dreißig. Hypothesen-Vorrat: [[Hypothesen-Bank (Momentum & Averages)]] und [[Hypothesen-Bank (Volumen & Flows)]].

## ⚖️ Gate v2: das kalibrierte Lineal (Max, 24./25.09.2026, AP250)

Anlass: [[Testphase Juli-Modus]] Teil B. Das alte Buch-Gate hätte keines der drei eigenen Buch-Beine aufgenommen (Power für einen echten 3-pp-Effekt 0,10 bis 0,16). Seitdem gilt:

| Stufe | Frage | Regel |
|---|---|---|
| Vor-Gates (Stufe 1, je Config) | Trägt die Config überhaupt? | `min_trades` 30, `min_oos_trades` 10, **kein Frequenz-Filter mehr**, stattdessen Sharpe-Beleg t = SR_ann·√Jahre ≥ 2; Tail-Test: Gewinn ohne die besten 1 % der Trades > 0 (an den Buch-Beinen kalibriert, 5 % hätte Momentum und LastHour rausgeworfen) |
| Edge (Stufe 2, `book_gate_v2`) | Schlägt der Kandidat seine eigenen Zufalls-Zwillinge? | gepaart gegen 10 Nulldrift-Zwillinge (gleiche Trades, Richtung gewürfelt), α 0,02 je Job, Šidák über die bewerteten Picks |
| Buch (Stufe 2) | Wird das Buch nicht schlechter? | Δ Passquote im Punkt ≥ 0, bei Ersatz: besser als das Original |
| Kontrolle (#106) | Ist das Gate ehrlich? | Placebo je Job (Zwilling des besten Picks als Kandidat), `discovery/placebo_log.json`, Inbox-Alarm wenn mehr als α + 2 SE durchkommen |

- Bewertet wird Stufe 2 auf der **vollen Historie** (im OOS-Fenster allein fiel selbst LastHour durch). Pro Job umschaltbar mit `gate_window: "oos"`.
- Null-Schalter (`tm_null`) haben: ts_reversal, last_hour, asian, tsmom, maband, vwap_pullback, orb, cal. Andere Modi werden sichtbar geblockt („kein Null-Schalter").
- Developer-Tab zeigt dasselbe Urteil (`MAXLAB_GATE_V2=0` schaltet es für schnelle Iterationen ab, ~8 Min je Lauf).
- Referenz: LastHour besteht, Momentum (Edge +4,4 pp, 80 bis 89 % über Zufall) und Asia-Dir nicht. Rechnungen `engine/_scratch_gate_kalibrierung/`.

## Offen / nächste Ausbaustufen
- Register-Merge Box → PC; Job-Typen „Regime-Conditioning" (Ein/Aus-Schalter für bestehende Beine) und „Event-Bein" (braucht Engine-Modul); Kandidaten-Karten im Strategy Lab (Tab) statt nur `inbox.md`.
- Ehrlich: mehr Alpha kommt nur mit **neuen Inputs** (Tick/L2, Optionen-Positionierung, Breadth). Der Runner macht die Suche sauber und billig, aber er zaubert keine neuen Mechanismen aus alten Minutenbars.
