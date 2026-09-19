# Engine-Audit A/D/E/F (17.09.2026) — quantitativer Teil der Friedhof-Analyse

Regeln beachtet: nur gelesen, nichts geaendert. Keine runner.log/results-Volltexte eingelesen (nur Aggregate via Python). Quelle je Fund als Datei:Zeile bzw. Feldname angegeben.

---

## A) Fix-Zeitleiste verifiziert (Code-Stand 17.09.2026, per grep/Docstring, NICHT per Mtime — Dateien werden staendig weiterbearbeitet, Mtime sagt nichts ueber das urspruengliche Fix-Datum)

### A1) sharpe_ann_daily-Inflation (#153) — GEFIXT, bestaetigt im Code
`discovery/discovery_lib.py:312-324`: `sharpe_ann_daily(tr)` annualisiert seit dem Fix ueber den VOLLEN Boersentage-Kalender (`pd.bdate_range(s.index.min(), s.index.max())`, 0-PnL-Tage aufgefuellt), nicht mehr ueber die Tage MIT Trades. Docstring zitiert explizit "Strategie-Logbuch #153 / AP151 Punkt 7". Aufruf `row["sharpe_ann"] = round(sharpe_ann_daily(tr), 2)` (Zeile 418) in `evaluate_config()`, also global fuer jede Config aktiv.

### A2) null_ceiling: Theorie statt Job-sr_std ("measured") — GEFIXT, aber als max(Theorie, gemessen)
`discovery/discovery_lib.py:424-437` definiert `sr_std_theory(years)` (reine Theorie, `1/sqrt(years)`) UND `null_ceiling(n_trials, sr_std)` (nimmt sr_std als Parameter, rechnet selbst nichts). Der eigentliche Fix sitzt im Aufrufer `discovery/discovery_runner.py:448-456`:
```
sr_std_meas = std(sharpe_ann ueber alle Configs des Jobs)
sr_std = max(L.sr_std_theory(yrs), sr_std_meas)
```
Damit ist die Zufallsdecke nicht mehr rein "measured" (das war das #139/#153-Problem: bei stark korrelierten Exit-Varianten faellt die gemessene Streuung absurd klein aus und macht die Decke zu niedrig/zu streng) — sie nimmt jetzt das Maximum aus Theorie und Messung. `meta["null_ceiling"]` speichert beide Werte separat (`sr_std_theory`, `sr_std_measured_across_configs`, `sr_std_used`) — transparent nachvollziehbar je Job in den `.meta.json`-Dateien.

### A3) replaces_leg-Existenz-Assert (#139 B5) — VORHANDEN, an zwei Stellen
- **Baustelle (Build-Time):** `discovery/hypothesis_bank.py:353-369+`, Funktion `_lint_replaces_leg(hyp, replaces)`, wird bei jedem `H()`-Aufruf mit `replaces` aufgerufen (Zeile 321). Prueft gegen `book_state.json`-Beinnamen, exakt ODER eindeutiger Praefix, sonst `assert`-Abbruch beim Bauen der Hypothese ("AP151 Punkt 5"). Docstring nennt explizit den Vorfall: sonst haette der Runner erst spaeter "nicht aufgeloest" geloggt oder bei mehreren Praefix-Treffern den Ersatztest ganz uebersprungen.
- **Laufzeit (Runner):** `discovery/discovery_runner.py:247-274`: loest `replaces_leg` gegen die aktuellen Buchbeine auf (Praefix-Match), bricht den Job bei Nicht-Aufloesung explizit ab (`"ABBRUCH: replaces_leg unaufgeloest"`, schreibt einen Fehlereintrag in die Inbox) statt es als stillen Dazu-Test laufen zu lassen (Kommentarzeile 263 zitiert genau diesen alten Pipeline-Audit-Fund vom 27.08.2026).

Fazit A3: doppelt abgesichert, sowohl beim Bauen als auch beim Rechnen. Sauber.

### A4) Modus-Zulassungs-Gate (#139 Lehre 1) — VORHANDEN als "skipped_required"-Mechanismus
`discovery/controls.py:1096-1144`, Funktion `run_controls()`:
```
skipped = [k for k in ("delay", "null") if res.get(k) dict und res[k]["ok"] is None]
res["deploy_ready"] = not fails and not skipped
```
Ein Modus ohne funktionierenden Delay- oder Null-Schalter liefert bei diesen Kontrollen `{"ok": None, "note": "Modus ohne ... Schalter -- Kontrolle uebersprungen"}` und landet automatisch in `skipped_required` — "uebersprungen" zaehlt NICHT als bestanden, `deploy_ready` bleibt hart `False`. Kommentar datiert das Gate auf "Audit 25.08.2026, B2". Das ist exakt das, was #139 als fehlend beschrieb, und ist jetzt Code, nicht nur Text.

**Aber: NEUER, bisher nicht dokumentierter Nebenbefund (Lücke im Gate selbst, siehe unten A5).**

### A5) NEUER FUND (17.09.2026): Modus-Zulassungs-Gate prüft nur "delay"/"null", ignoriert `null_ref`-Alternativen wie `ctl_random_level` — orb/orb_std strukturell von deploy_ready ausgeschlossen, ohne dass das irgendwo als bewusste Entscheidung steht

`discovery/hypothesis_bank.py:252-278` pflegt eine Tabelle `NULL_REF_BY_MODE`, die je (mode, mb_kind) festlegt, WELCHE Kontrolle die mechanische Null liefert:
- `("orb", None): "ctl_random_level"`, `("orb_std", None): "ctl_random_level"` — orb hat also explizit KEINE `ctl_null`-Zustaendigkeit, sondern `ctl_random_level` als sein Null-Aequivalent (OR-Zufallslevel, tick-treu, AP153 P11).
- Kommentarzeile 277-278 im selben File dokumentiert separat: "Modi OHNE Null-Schalter auf der Box: rv, cal, vix_bias ... Job wird nie deploy_ready" — das ist als bewusste, bekannte Einschraenkung markiert.

ABER: `run_controls()` (controls.py:1134-1136) liest `null_ref` NIE — weder in discovery_runner.py noch in controls.py taucht `null_ref` als Steuergroesse auf (einziger Treffer: `discovery_runner.py:662`, nur zum Durchreichen ins Inbox-Anzeigefeld). Die Skipped-Pruefung ist hart auf die Ergebnis-Keys `"delay"` und `"null"` verdrahtet. `ctl_null()` (controls.py:625-644) akzeptiert nur `mode in ("tsmom","maband","ts_reversal","last_hour","asian","vwap_pullback")` — **orb und orb_std sind da NICHT drin**, obwohl sie laut `NULL_REF_BY_MODE` `ctl_random_level` nutzen sollen. Folge: jeder orb/orb_std-Kandidat, der bis zur Kontroll-Batterie kommt, bekommt `res["null"] = {"ok": None, ...}` (Modus nicht unterstuetzt) → landet automatisch in `skipped_required` → `deploy_ready` bleibt **strukturell immer False**, unabhaengig davon, ob `ctl_random_level` (das eigentlich vorgesehene Aequivalent) besteht oder nicht.

Das widerspricht CLAUDE.md/#139s Aussage, "nur tsmom/maband/orb konnten deploy_ready werden" — nach aktuellem Codestand kann **orb strukturell NIE deploy_ready werden**, weil sein dokumentiertes Null-Aequivalent vom harten Gate ignoriert wird. Praktisch noch nicht aufgefallen: Datenpruefung (siehe unten) zeigt, dass ueberhaupt nur 10 Rows im gesamten Ergebnis-Archiv je das Feld `controls` bekommen haben (alle tsmom/ts_reversal, alle `deploy_ready=False` aus anderen Gruenden) — orb/orb_std haben es also noch nie bis zur Kontroll-Batterie geschafft (0 Kandidaten seit 24.08. deckungsgleich mit dem Register-Stand). Der Bug ist also aktuell **latent, nicht akut** — wird aber sofort zum Blocker, sobald orb/orb_std je einen Buch-Marginal-Kandidaten liefert.

**Fehlerklasse: F6 (Pipeline-Bug, ein Modus ohne funktionierenden Null-Schalter trotz vorhandenem Aequivalent).** Gleiches Muster wahrscheinlich fuer `maband`-Arten `band`/`channel`/`vwap`, die laut `NULL_REF_BY_MODE` ebenfalls `ctl_random_level` statt `ctl_null` brauchen — deren maband-Trials laufen zwar durch `ctl_null` durch (weil `mode == "maband"` pauschal erlaubt ist), aber die Null-KONTROLLE, die dabei tatsaechlich laeuft (`tm_null`-Direction-Placebo), ist fuer `mb_kind in ("band","channel","vwap")` mechanisch die FALSCHE Null (die Geometrie-Null waere ein Zufallslevel, nicht eine gewuerfelte Richtung) — das ist exakt die Sorge, die der Kommentarblock in hypothesis_bank.py Zeile 246-249 ("VV-57") beschreibt. Das heisst: maband band/channel/vwap-Kandidaten koennten `ctl_null` FAELSCHLICH BESTEHEN (falscher Kontrollarm, kein Skip), waehrend orb/orb_std-Kandidaten am selben Gate IMMER hart scheitern (kein Kontrollarm ueberhaupt). Zwei spiegelbildliche Symptome desselben Lochs: `null_ref` wird nirgends durchgesetzt.

### A6) ctl_delay/ctl_null: welche Modi laufen jetzt tatsaechlich (Stand 17.09., aus dem Code)

| Modus | ctl_delay (Look-ahead-Selbsttest) | ctl_null (Nulldrift/Richtung) | deploy_ready ueberhaupt erreichbar? |
|---|---|---|---|
| tsmom | ja (`tm_entry_delay`+1) | ja | ja |
| maband | ja (`mb_start_min`+bump, `tm_cutoff_min` mitgezogen) | ja (aber ggf. falscher Kontrollarm bei mb_kind band/channel/vwap, siehe A5) | ja (formal), Kontrollarm-Qualitaet fraglich fuer band/channel/vwap |
| orb | ja (`orb_exec="close"`) | **nein** (Modus nicht in ctl_null-Liste, obwohl `null_ref=ctl_random_level` vorgesehen) | **nein, strukturell blockiert (A5)** |
| ts_reversal | ja (`rev_signal_min`+1, seit 01.09. AP137/AP157) | ja (seit AP157 Blocker B, 15.09., auf der Box neu gebaut) | ja |
| rv | ja (`rv_entry_after`+1) | **nein** (bekannte, dokumentierte Einschraenkung) | **nein, dokumentiert** |
| last_hour | ja (`lh_ref_min`+1) | ja (seit AP157 Blocker B) | ja |
| vwap_pullback | ja (`vwap_first_entry_min`+5) | ja (seit AP157 Blocker B) | ja |
| asian | ja (`tr_start`+1min) | ja (seit AP157 Blocker B) | ja |
| orb_std | nein (nicht im ctl_delay-mode-zweig gelistet — faellt in `else` "Modus ohne Delay-Schalter") | nein | **nein, doppelt blockiert** |
| cal, vix_bias | nein | nein (dokumentiert) | nein, dokumentiert |
| alle anderen (i2, gap, regime_gate, pivot, flip, continuation, firstbar_ematrail, event_study, regime_gate_subset, cage_daily_stop, reversion) | nein | nein | nein (kein Eintrag in ctl_delay/ctl_null ueberhaupt) |

Damit sind **effektiv nur 5 Modi** (tsmom, maband, ts_reversal, last_hour, vwap_pullback, asian — 6 wenn man asian mitzaehlt) technisch in der Lage, `deploy_ready` zu erreichen. orb/orb_std sind zusaetzlich zu den CLAUDE.md-bekannten Luecken (rv/cal/vix_bias) betroffen — das war noch nicht dokumentiert.

### A7) Register-Flag `exit_konvention_1559` (AP161) — NICHT vorhanden, bewusst offen gelassen
`discovery/registry_flags.json` (Stand 15.09.2026 18:13, 5.742 Bytes) enthaelt aktuell nur Eintraege vom Typ `dead_trail` (VWAP-Pullback Exit2-Redundanzen), **keinen** `exit_konvention_1559`-Schluessel. Bestaetigt durch `tasks.json` (Ticket AP161, `progress_notes` 16.09.2026, zweiter Eintrag, letzter Satz): *"OFFEN, nicht heute erledigt: Registry-Markierung (Punkt 3) ... discovery/registry_flags.json hat noch kein Schema fuer 'exit_konvention_1559'-Flags auf einzelnen Trials, muesste neu angelegt werden. Kein Blocker, reine Audit-Spur."*

Wichtiger Zusatzfund aus demselben Ticket (AP161, direkt relevant fuer den Friedhof): der **eigentliche Code-Patch** (`sigcore.py::simulate_trade`, Zwangs-Flat auf Minute 385 = 15:55 ET statt 15:59-Close, live-treu) wurde am **16.09.2026 19:32:30 MEZ** deployt und ist gruen regressionsgetestet — betrifft aber laut Ticket-Notiz Punkt 6 **nur** die Module, die ueber `sigcore.simulate_trade` laufen (tsmom, maband). **Elf weitere Module halten nach wie vor bis zum 15:59-Close** ohne eigenen Flatten-Parameter: `qbt.py` (orb Zeile 629, gap Zeile 991, on_rev Zeile 803, vwap_trend Zeile 1161, Default-Zweig `_simulate_day` Zeile 1230), `pivot.py:115`, `flip.py:132`, `intraday2.py:102/127/259` (i2 — aktive job_generator-Vorlage!), `noise_orb.py:105`, `vix_bias.py:93/104` (**Live-Bank-Bein `VIX_spike_rev_NQ`**), `calendar_fx.py:110/139/180`. Grenzfall `orb_std`: exitet am Close der Flat-Bar statt am Open.

**Das ist ein aktiver, noch offener Bruch zwischen Backtest und Live-Verhalten** fuer alle diese Module — insbesondere fuer `vix_bias.py`, weil `VIX_spike_rev_NQ` ein **echtes Live-Bank-Bein** ist (`live_finalize.py` LIVE_EXTRA). Fehlerklasse **F1** (Urteil auf alter/inkonsistenter Engine-Konvention) fuer JEDES vor dem 16.09. gefaellte Urteil auf Basis dieser 11 Module UND als **aktuell laufendes Risiko** fuer das Live-Bank-Bein einzustufen, nicht nur historisch.

### A8) Zusammenfassung Fix-Zeitleiste — Stand der Verifikation

| Fix aus dem Briefing | Verifiziert im Code? | Fundstelle |
|---|---|---|
| #153 sharpe_ann_daily-Inflation | ✅ gefixt | discovery_lib.py:312-324 |
| #139/#153 null_ceiling Theorie statt "measured" | ✅ gefixt (max(Theorie,gemessen)) | discovery_lib.py:424-456, discovery_runner.py:448-467 |
| #139 B5 replaces_leg-Existenz-Assert | ✅ vorhanden (Build+Runtime) | hypothesis_bank.py:353ff, discovery_runner.py:247-274 |
| #139 Lehre 1 Modus-Zulassungs-Gate | ✅ vorhanden, ⚠️ mit Loch (A5) | controls.py:1096-1144 |
| ctl_delay/ctl_null Modus-Abdeckung | ⚠️ teilweise (5-6 von 23 Modi) | controls.py:410-483, 625-644 |
| AP161 exit_konvention_1559-Flag | ❌ noch nicht angelegt (bewusst) | tasks.json AP161, registry_flags.json |
| AP161 Exit-Konvention 15:55 | ⚠️ nur sigcore-Module gepatcht, 11 Module offen inkl. Live-Bein VIX_spike_rev_NQ | sigcore.py:834-841, tasks.json AP161 Punkt 6 |

---

## D) Register-Abdeckungs-Luecken (63.727 Trials, Register-Stand 17.09.2026)

**Methodischer Hinweis vorab:** die `params`-Dicts im Register enthalten nur die Feld­werte, die in dem jeweiligen Job explizit gesetzt wurden (Basis + Grid), nicht den vollstaendigen gemergten Default-Parametersatz der Engine-Funktion. "Konstant" bzw. "Feld nie gesehen" heisst deshalb praeziser: *kein Job hat diese Achse je explizit ins Grid gelegt* — nicht zwingend, dass der Code selbst keine Variation zulaesst. Fuer die Frage "was wurde nie GETESTET" ist das trotzdem die richtige Kennzahl.

### D1) Trial-Zahl je (mode, symbol) und Markt-Luecken

| mode | NQ | ES | RTY | YM | gesamt |
|---|---|---|---|---|---|
| tsmom | 19.898 | 4.428 | 9.764 | 4.908 | 38.998 |
| maband | 9.352 | 3.326 | 1.128 | 2.600 | 16.406 |
| firstbar_ematrail | 2.880 | 0 | 0 | 0 | 2.880 |
| ts_reversal | 851 | 87 | 5 | 88 | 1.031 |
| rv | 477 | 101 | 152 | 9 | 739 |
| i2 | 244 | 109 | 85 | 109 | 547 |
| regime_gate | 419 | 0 | 111 | 0 | 530 |
| last_hour | 367 | 56 | 20 | 20 | 463 |
| gap | 116 | 29 | 225 | 27 | 397 |
| asian | 266 | 28 | 4 | 0 | 298 |
| cal | 74 | 45 | 27 | 54 | 200 |
| orb | 136 | 23 | 3 | 22 | 184 |
| vwap_pullback | 155 | 0 | 0 | 0 | 155 |
| continuation | 48 | 48 | 0 | 0 | 96 |
| vix_bias | 21 | 52 | 0 | 0 | 73 |
| pivot | 13 | 13 | 13 | 13 | 52 |
| orb_std | 45 | 0 | 0 | 0 | 45 |
| flip | 6 | 6 | 6 | 6 | 24 |
| event_study | 12 | 12 | 0 | 0 | 24 |

(Zusaetzlich 522 Trials mit mode=None — vermutlich Backfill/Prescan-Sonderfaelle ohne mode-Feld, 358 davon auch ohne Symbol; nicht weiter aufgeschluesselt.)

**Modi, die NIE auf einem Markt liefen:**
- **ES:** firstbar_ematrail, regime_gate, vwap_pullback, orb_std, regime_gate_subset, cage_daily_stop, reversion
- **RTY:** firstbar_ematrail, vwap_pullback, continuation, vix_bias, orb_std, event_study, prescan, cage_daily_stop, reversion
- **YM:** firstbar_ematrail, regime_gate, asian, vwap_pullback, continuation, vix_bias, orb_std, event_study, prescan, regime_gate_subset, cage_daily_stop, reversion

**Auffaelligstes Einzelloch: `vwap_pullback` — das aktuelle Ersatz-Bein fuer NQ_VWAP-Pullback im Buch — lief NOCH NIE auf ES/RTY/YM, nur auf NQ (155 Trials).** Bei einem Modus, der aktiv den Buchweg (`replaces_leg`) geht, ist die fehlende Multi-Markt-Kontrolle (#051, ctl_symbols) eine echte Luecke — ctl_symbols testet zwar automatisch pro Kandidat auf allen 4 Maerkten zur Laufzeit, aber es gab noch nie einen eigenstaendigen Discovery-Job, der prueft, ob die VWAP-Pullback-Mechanik auf ES/RTY/YM ueberhaupt eine andere Struktur zeigt.

**`firstbar_ematrail`** (2.880 Trials, zweitgroesster Nicht-Buch-Modus) lief ausschliesslich auf NQ — trotz beachtlicher Grid-Tiefe komplett unmarkt-getestet.

### D2) Param-Achsen je Modus ohne jede Variation (nur 1 Wert ueber alle Trials, Auszug)

- **tsmom** (n=38.998): konstant `tm_delta_src='real'` (Delta-Quelle NIE gegen einen Proxy getestet — falls `tm_signal='cvddiv'` einen Proxy-Modus kennt, ist der nie geprueft), `tm_entry_delay=1` (Basis-Delay nie variiert — sinnvoll, das ist die Kontrollgroesse fuer ctl_delay selbst), `tm_on_ret_max=0.0025`, `tm_vix_max=16` (VIX-Deckel NIE variiert — jede vix-gefilterte tsmom-Variante nutzt exakt denselben Schwellwert, obwohl das eine der zentralen offenen "Mom-lowVIX"-Ideen aus dem Ideen-Friedhof ist, siehe Task F).
- **maband** (n=16.406): konstant `mb_src='close'` (Signalquelle nie auf z.B. `hl2`/`typical` getestet), `mb_vwap_dnorm='atr_bar'` (seit dem #157-Fix einzige zugelassene Normierung — das alte `atr`/`sigma` sind aus dem Register her nicht mehr vertreten, historische Trials mit `dnorm='atr'` liegen vermutlich VOR dem Fix und sind separat zu pruefen, s. Praemissen-Friedhof/Task C), `be_offset=0.0`, `mb_walk_n=3`.
- **rv** (n=739): `rv_eod_min=385` konstant — deckt sich mit der neuen 15:55-Exit-Konvention (A7), war also vermutlich nie Achse.
- **orb** (n=184): `orb_exec='close'` konstant (korrekt so, seit #066/#067 Pflicht), aber auch `nr7_filter=False` NIE auf True getestet (die NR7-Kompressions-Filter-Idee aus dem Crabel-Stretch-Ideenkarten-Kontext, Task F, wurde nie in orb selbst kombiniert) und `vix_ref='rel'` nie auf einen anderen Referenzmodus.
- **gap** (n=397): `gap_dow='[0]'` konstant — **alle Gap-Trials liefen nur fuer Montag (dow=0)**, kein einziger Trial fuer Dienstag-Freitag. Das ist eine harte, bisher nicht benannte Wochentags-Luecke.
- **continuation** (n=96): `one_trade_per_day=False` nie auf True getestet.
- **prescan** (n=22): `placebo='phase_unrounded'` konstant, kein anderer Placebo-Typ je verglichen.

### D3) tsmom Achsen-Verteilung (n=38.998)
- `tm_signal`: signratio=5.122, wins=2.607, ret=2.472, rangepos=173, accel=107, zscore=61, rank=55, er_ret=39, **jerk=1** (nur EIN einziger Trial jemals mit `tm_signal='jerk'` — praktisch ungetestet)
- `tm_base`: open=32.808 (84%), prev_close=3.704, window=426, prev_rth=181, overnight=145 — extrem open-lastig, prev_rth/overnight (Overnight-Gap-Basis) so gut wie nie verwendet
- `tm_exit`: eod=37.931 (97%), time=635, rr=406, base=22 — `tm_exit='base'` (Exit auf Basis-Ruecklauf) fast nie getestet (22 von 38.998)
- `tm_stop_mode`: range=37.947 (97%), atr=664, sigma=92 — sigma-Stop extrem selten
- `tm_dir`: both=513, long_only=250, short_only=38 — **nur 801 von 38.998 Trials (2,1%) testen ueberhaupt explizit die Richtungsachse**, der Rest laeuft implizit auf Default `both`. short_only mit nur 38 Trials ist die duennste Achse ueberhaupt.
- `tm_side`: momentum=29.204 (75%), fade=7.773 (25%) — die Gegenseiten-Kontrolle (Momentum vs. Fade/Continuation) ist wenigstens in nennenswerter Zahl vertreten.

### D4) maband Achsen-Verteilung (n=16.406)
- `mb_kind`: dist=11.240 (69%), channel=4.085 (25%), vwap=561, slope=213, band=175, cross=83, price_ma=35, **speeds=6, fan=5** — die beiden komplexesten/neuesten Kind-Arten (`speeds`, `fan` — Geschwindigkeits-/Faecher-Signale) sind mit 6 bzw. 5 Trials praktisch nur einmal durchgetestet, nicht ernsthaft exploriert.
- `mb_vwap_anchor`: session=65, hi=26, lo=26 — nur 117 von 561 vwap-Trials (21%) haben den Anchor ueberhaupt explizit gesetzt; der Rest laeuft (vermutlich) auf Default `session`, `rand_time`-Anker (fuer die Kontrolle) taucht in den Params gar nicht auf.
- `mb_vwap_dnorm`: nur `atr_bar=162` im Register sichtbar (Post-Fix-Wert, siehe D2).
- `mb_side`: with=3.806, against=803 — gute Abdeckung.
- `tm_dir`: nur 96 von 16.406 maband-Trials (0,6%) testen die Richtungsachse ueberhaupt explizit.

### D5) Long/Short-Abdeckung ausserhalb tsmom/maband
**Kein einziger anderer Modus (ts_reversal, rv, i2, last_hour, gap, asian, cal, orb, vwap_pullback, continuation, vix_bias, pivot, orb_std, flip, event_study, firstbar_ematrail, regime_gate, cage_daily_stop, reversion) hat das Feld `tm_dir` je im Params-Dict gesetzt** — heisst: bei 17 von 19 benannten Modi wurde Long-only/Short-only NIE als explizite Achse gefahren. Ob diese Module ueberhaupt einen Richtungs-Parameter kennen (oder Richtung anders steuern, z.B. ueber ein Vorzeichen im Signal selbst), ist Code-seitig nicht ueberall belegt und waere ein Punkt fuer `variant-scout`.

### D6) Uhrzeit-Fenster-Abdeckung
- **tsmom `tm_sig_start`** (14 Werte: 0,5,10,15,30,60,120,150,180,210,285,300,315,330 Minuten seit 09:30): ab 12:00 (>=150min) IST abgedeckt (150-330), letzte 90 Minuten (>=300min, RTH bis ~390min) ebenfalls (300/315/330). **Aber die Mitte des Nachmittags (210-285min = 13:00-14:15 ET) hat nur einen einzigen Wert (210), grosse Luecken zwischen 210 und 285 sowie zwischen 330 und Sessionende (390).**
- **maband `mb_start_min`** (9 Werte: 15,30,45,60,90,120,180,210,240): deckt nur bis 240min (13:30 ET) ab — **der gesamte Nachmittag ab 13:30 ET wurde fuer maband-Signalstarts NIE getestet.**
- **last_hour `lh_ref_min`**: 15 Werte, deckt 180-375min breit ab (gute Abdeckung).
- **asian `tr_start`**: nur 2 Werte ('09:30', '23:00') — die Fenstergrenzen der Asien-Session selbst wurden nie systematisch variiert (nur ein fruehes und ein spaetes Startfenster).

---

## E) Survivors ohne Buch-Marginal — DER groesste Einzelfund dieser Analyse

**Struktur:** Buch-Marginal wird nicht fuer jeden Survivor gerechnet, sondern nur fuer die Top-k "picks" je Job (sortiert nach OOS-Sharpe/expR), `k = job.get("max_book_evals", cfg["max_book_evals_default"])`. Laut CLAUDE.md wurde dieser Default mehrfach angepasst: 6 → 30 (09.09., AP137 B4) → wieder auf 3 (spaeter). Feld im Ergebnis: `row["book"]` (gesetzt in `discovery_runner.py:530`, gelesen aus `discovery/results/<job>.json`, NICHT `.meta.json`).

### E1) Gesamtzahlen (901 Job-Ergebnisdateien durchsucht, 0 Ladefehler)
- **Survivors insgesamt: 4.605**
- **Davon mit Buch-Marginal bewertet: 1.971 (42,8%)**
- **Davon OHNE Buch-Marginal: 2.634 (57,2%)**
- Jobs mit >=1 Survivor, aber KEINER bewertet: **7**
- Jobs mit >=1 Survivor, ALLE bewertet: 30
- Jobs mit Survivor-Luecke (mind. 1 unbewertet): **313 von 901 Jobs (35%)**

**Das heisst: fast sechs von zehn Survivors (die bereits ALLE Stufe-1-Gates bestanden haben — n-Trades, Edge, Freq, Dollar, IS/OOS, top5, last3y, Kosten-Stress, Bootstrap, Plateau, ueber der Zufallsdecke) wurden nie gegen das Buch gerechnet, allein weil sie nicht zu den besten 3-30 Configs IHRES EIGENEN Jobs gehoerten.** Das ist strukturell erwartbar (Buch-Marginal ist teuer), aber es bedeutet: die eigentliche Auswahl "was hat Potenzial" findet stillschweigend schon VOR der Buch-Pruefung statt, rein ueber OOS-Sharpe/expR-Ranking innerhalb des Jobs — ein Survivor mit z.B. sehr hohem $/Jahr aber Rang 10 im selben Job wird nie geprueft, selbst wenn er den Buch-Beitrag eines schwaecheren Rang-3-Survivors uebertreffen wuerde.

### E2) Groesste Luecken je Job (Top-Auszug, volle Liste in Skript-Output)
Die groessten Luecken liegen fast ausschliesslich bei den `gen_tsmom_ema_ladder_*_hf_*`- und verwandten Generator-Jobs (EMA-Leiter-Vorlagen mit sehr breiten Grids):

| Job | n_survivors | n_booked | n_unbooked |
|---|---|---|---|
| gen_tsmom_ema_ladder_mom_c3_hf_NQ | 148 | 6 | **142** |
| gen_tsmom_ema_ladder_mom_c2_hf_NQ | 142 | 6 | **136** |
| gen_tsmom_ema_ladder_mom_c4_hf_NQ | 111 | 6 | **105** |
| gen_tsmom_combo_mom_atr_hf_NQ | 104 | 6 | **98** |
| gen_tsmom_ema_ladder_mom_c1_hf_NQ | 103 | 6 | **97** |
| gen_tsmom_combo_mom_hf_NQ | 99 | 6 | 93 |
| gen_maband_crossover_wide_tfm_NQ | 78 | 6 | 72 |

Diese Jobs sind ausnahmslos **tsmom/maband HF-Vorlagen des `job_generator.py`** (die "Varianten"-Generation aus dem 06.09.-Abschnitt der CLAUDE.md) — genau die Kategorie, von der CLAUDE.md sagt "0 Kandidaten ist das erwartete Ergebnis" (kein `replaces_leg`, neues Bein gegen ein Buch ohne tsmom/maband-Bein). Diese Erwartung mag fuer die geprueften 6 Picks je Job stimmen — **sie ist aber nie fuer die anderen 90-140 Survivors je Job verifiziert worden**, weil sie nie bewertet wurden.

### E3) Top 30 beste unbewertete Survivors (n>=100 Trades, Job-`selection.level` != "kaputt", sortiert nach OOS-expR)
Kandidatenpool vor Cutoff: **1.695 Survivors** (von 2.634 unbewerteten). Die Top-Werte kommen fast geschlossen aus den `gen_tsmom_ema_ladder_*_hf_NQ`-Jobs (EMA-Confirm-Leiter 40-200, `tm_delta_min=0.25`, `tm_vwap_side` variiert, `tm_stop_mult=0.3`, `hf_profile=len5_thr15`):

| job | Kern-Params (gekuerzt) | trades | oos_trades | oos_expR | sharpe_ann | sel_level |
|---|---|---|---|---|---|---|
| gen_tsmom_ema_ladder_mom_c3_hf_NQ | tm_ema_confirm=160, vwap_side=True, stop_mult=0.3 | 564 | 148 | **0.729** | 2.28 | ok |
| gen_tsmom_ema_ladder_mom_c3_hf_NQ | tm_ema_confirm=130, vwap_side=True, stop_mult=0.3 | 565 | 147 | 0.728 | 2.31 | ok |
| gen_tsmom_ema_ladder_mom_c3_hf_NQ | tm_ema_confirm=120, vwap_side=False, stop_mult=0.3 | 582 | 151 | 0.726 | 2.20 | ok |
| gen_tsmom_ema_ladder_mom_c4_hf_NQ | tm_ema_confirm=170, vwap_side=True, stop_mult=0.3 | 563 | 149 | 0.717 | 2.23 | ok |
| gen_tsmom_combo_mom_atr_hf_NQ | tm_ema_confirm=100, vwap_side=True, stop_mult=0.3 | 568 | 148 | 0.716 | 2.31 | duenn |
| gen_tsmom_ema_ladder_mom_c2_hf_NQ | tm_ema_confirm=100, vwap_side=True, stop_mult=0.3 | 568 | 148 | 0.716 | 2.31 | duenn |
| ... (24 weitere, gleiches Muster: EMA-Confirm 40-200, alle NQ, alle tsmom, oos_expR 0.63-0.73, sharpe_ann 2.0-2.4) | | | | | | |

Die vollstaendige 30er-Liste liegt in `e_survivors_no_marginal.md`. **Bemerkenswert: sharpe_ann 2.0-2.4 liegt deutlich ueber jeder in Task A ermittelten Zufallsdecke** (die globalen `null_ceiling`-Werte in den Meta-Dateien lagen im Bereich 0.4-1.5 je nach n_global) — diese 30 Survivors sehen nach der reinen Zahlenlage NICHT wie Rauschen aus, wurden aber nie gegen das Buch gerechnet, weil sie in ihren jeweiligen Jobs nicht unter den besten 3-6 waren (die Konkurrenz innerhalb der eigenen EMA-Leiter-Jobs ist einfach sehr dicht).

**Wichtiger Vorbehalt:** diese 30 sind alle `tm_side` vermutlich `momentum` auf sehr kurzen HF-Profilen (`hf_profile=len5_thr15`) — hoch korrelierte Nachbar-Configs derselben Grundidee (EMA-Confirm-Leiter), nicht 30 unabhaengige Mechanismen. Die tatsaechliche Zahl unabhaengiger, pruefenswerter IDEEN darunter ist viel kleiner als 30 — aber selbst 1-2 stellvertretende Vertreter je Job-Familie wurden nie gegen das Buch gerechnet.

### E4) Unbewertete Survivors je Modus
tsmom 1.604, ts_reversal 352, maband 347, last_hour 91, gap 82, vwap_pullback 65, asian 31, i2 29, rv 23, cal 10.

**Fehlerklasse fuer diesen ganzen Befund: F9 (nie eingereiht/liegengeblieben) bzw. F4-nah (Gate-Artefakt durch `max_book_evals`-Deckel) — kein Bug, aber eine bewusste Kostenbremse, die bisher nirgends im Vault als "hier gehen 57% der Survivors systematisch verloren" beziffert war.**

(Volle 30er-Tabelle mit allen Param-Details in e_survivors_no_marginal.md, Abschnitt "Top 30 beste unbewertete Survivors".)

## F) "Validiert, aber nicht im Buch" — Karten aus ideas.json (status Validiert/Backlog) vs. LIVE_EXTRA

ideas.json: 64 Karten total, 40 Getoetet, 5 Im Buch, 15 Validiert, 4 Backlog — 19 Karten im Scope dieser Aufgabe.

live_finalize.py LIVE_EXTRA (Zeilen 49-73) enthaelt genau 3 Karten: VIX_spike_rev_NQ (mechanism NQ Punkt VIX-Spike-Reversion), OPEXMOM_NQ (NQ Punkt OpEx-Momentum), EVENT_ES_primary (ES Punkt FOMC-Post + OpEx kombiniert). Der Modul-Docstring selbst zaehlt explizit die bewusst ausgeschlossenen Grade-C/D-Funde auf: VWAP-Pullback, Overnight-Reversal, Crabel-Stretch, Asia-Break, Mom-lowVIX, MOMSEL.

Der automatische Name/Mechanism-Abgleich per Skript war zu strikt (Substring-Vergleich scheiterte an Formatierungsunterschieden) — Ergebnis unten von Hand nachgezogen anhand der vollen Result-Texte (siehe f_validiert_backlog.md fuer die Rohdaten je Karte).

### F1) Alle 19 Validiert/Backlog-Karten, Stand ggue. LIVE_EXTRA und Nachrechnungs-Check

| Karte | Familie | Status | Im Live-Buch? | Result-Kurzfassung | Nachrechnung nach 16.08 erkennbar? |
|---|---|---|---|---|---|
| Cross-Asset / Relative Value | Relative Value | Validiert | Teilweise, VIX-Teilstueck deckungsgleich mit VIX_spike_rev_NQ, ZN/DXY/Breadth offen | VIX spike_rev ueberlebt OOS (PF 1.91), Short-Gegentest tot. ZN/Bonds/DXY/Sektor-Breadth Daten-Luecke | Nein |
| Mom-lowVIX | Trend Following | Validiert | Nein | OOS-Edge +10,4 Prozent, Sharpe 2,78. Explizit NICHT das gebuchte Momentum-Bein. Status frueher faelschlich als Im Buch gefuehrt, hier korrigiert (F8-Verdacht) | Nein |
| Gap-Continuation (grosse Gaps) | Trend Following | Validiert | Nein | OOS +7-9 Prozent, schwach (D-Note), 17/Jahr, vor #050 informell verworfen | Nein |
| ES-Momentum (adaptiert) | Trend Following | Validiert | Nein | OOS +1,0 Prozent, PF 1,07, korreliert mit NQ-Mom (0,15) | Nein |
| NQ Asian-Levels RTH-Breakout | Trend Following | Validiert | Nein | Nach Fill-Fix nur noch OOS +1,2 Prozent, PF 1,07, Auto-Fit abgelehnt | Nein |
| Multi-Day-Kointegrations-Pairs | Relative Value | Backlog | Nein | Result-Feld leer, nie getestet | n/a |
| FOMC-Announcement-Momentum (ES, solo) | Intraday Bias | Validiert | Nein, nur die kombinierte Version ist drin | Edge +13,3, OOS +39 Prozent, PF 1,71, nur 8 Trades/Jahr | Nein |
| Turn-of-Month Long | Intraday Bias | Backlog | Nein | IS 2016-22 flach/negativ, OOS ab 2023 klar positiv (+8 bis +9 Prozent), Watchlist fuer spaeter | Datumshinweis ja, Inhalt nein |
| Event-Bein FOMC-Post + OpEx kombiniert | Intraday Bias | Validiert | JA, das ist EVENT_ES_primary | ES 108 Trades/Jahr, Grade A, Win 55,6 Prozent, OOS-Edge +25,3 Prozent, Auto-Fit knapp abgelehnt | Nein |
| OpEx-Momentum (solo, alle 4 Instrumente) | Intraday Bias | Validiert | Nur teilweise, nur NQ-Variante ist OPEXMOM_NQ | 59/87 Survivors, beste NQ OOS PF 3,34, aber 6-9 Trades/Jahr | Nein |
| VWAP-Pullback (Continuation) | Trend Following | Validiert | Nein, explizit ausgeschlossen (Grade C/D) | 17/108 Survivors, bester OOS-Edge +6,4 Prozent, Quote gegen Tempo getauscht | Nein |
| Overnight-Reversal | Mean Reversion | Validiert | Nein, explizit ausgeschlossen (Grade C/D) | 9/72 Survivors, invertierte IS/OOS-Signatur, regimeabhaengig | Nein |
| Crabel-Stretch (NR7-Kompression) | Trend Following | Validiert | Nein, explizit ausgeschlossen (Grade C/D) | 18/88 Survivors, NQ-lastig, marginal | Nein |
| Momentum-Selektiv (Kaufman ER-Filter) | Trend Following | Validiert | Nein, explizit ausgeschlossen (MOMSEL, Grade C/D) | REPLACE-TEST v2 (#080): Delta im MC-Rauschen, Tage-bis-Pass sinken konsistent, Entscheidung an AP53 gekoppelt. Einzige Karte mit expliziter v2-Nachrechnung | Ja |
| Noise-ORB NQ (Zarattini SSRN 4824172) | Trend Following | Validiert | Nein, weder aufgenommen noch als bewusst ausgeschlossen genannt | expR +0,094, IS annaehernd OOS (kein Overfit-Abfall), 9/11 Jahre positiv, Top5 nur 29 Prozent, generalisiert nicht auf RTY/YM/ES | Nein |
| OR_DELTA_BIAS_NQ (Tick-Rule-Delta) | Intraday Bias | Validiert | Nein, bewusste Entscheidung | LONG n=1318, IS +54,2R und OOS +89,1R, Top5 nur 3,6 Prozent, Max' explizites No-Go (Edge notwendig, nicht hinreichend) | Nein |
| VIX-Spike-Reversion (Vortags-VIX, NQ) | Intraday Bias | Validiert | JA, das ist VIX_spike_rev_NQ | 8/24 Survivors, alle Long, OOS PF 1.91, Entscheid Max AP88 | Nein |
| Cross-Sectional Momentum (Rank-Futures) | Relative Value | Backlog | Nein | Backlog seit 21.08.2026, Datenlage nur 4 Index-Futures, nie getestet | Datumshinweis ja, Inhalt nein |
| Way of Dumb (Zwangsflows Institutionen) | Intraday Bias | Backlog | Nein | Backlog seit 21.08.2026, vier Teilideen skizziert, keine als Job gebaut | Datumshinweis ja, Inhalt nein |

### F2) Kernbefunde Task F

1. Von 15 Validiert-Karten sind nur 3 tatsaechlich im Live-Buch (VIX-Spike-Reversion, OpEx-Momentum-NQ-Teilmenge, Event-Bein-ES). 12 von 15 validierten, nicht getoeteten Karten liegen brach.
2. 5 Karten sind vom live_finalize.py-Docstring explizit als Grade-C/D ausgeschlossen (VWAP-Pullback, Overnight-Reversal, Crabel-Stretch, Momentum-Selektiv/MOMSEL) — bewusste, dokumentierte Entscheidung, keine Luecke.
3. Noise-ORB NQ ist der auffaelligste echte Gap: Grade-A-aehnliche Kennzahlen (IS annaehernd OOS, 9/11 Jahre positiv, Top5 nur 29 Prozent) und wird im live_finalize.py-Docstring weder als aufgenommen noch als bewusst ausgeschlossen genannt — sieht nach einer schlicht vergessenen Karte aus (Fehlerklasse F9). Passt zu Task A: der orb-Modus ist strukturell nie deploy_ready-faehig (A5) — falls das mit ein Grund ist, warum Noise-ORB nie den Weg von Backtest-Fund zu LIVE_EXTRA fand, wirken ein Pipeline-Bug (A5) und ein Prozess-Loch hier zusammen.
4. OpEx-Momentum ist nur zu einem Viertel im Live-Buch: die Karte selbst testet alle 4 Instrumente mit 59/87 Survivors, LIVE_EXTRA hat aber nur die NQ-Variante. Ob ES/RTY/YM schwaecher sind oder nur nie nachgezogen wurden, ist aus dem Code allein nicht ersichtlich.
5. FOMC-Announcement-Momentum (ES, solo) ist eine eigene Karte neben der kombinierten Event-Bein-Karte, nur die kombinierte Version ist live. Die Solo-Version (Edge +13,3, OOS +39 Prozent) wurde nie separat nachgezogen, obwohl sie eigenstaendig Grade-A-aehnliche Werte zeigt.
6. Nur 1 von 19 Karten (Momentum-Selektiv) traegt einen expliziten Hinweis auf eine v2-/Buch-Marginal-Nachrechnung nach dem 16.08.2026-Kriteriumswechsel (#106) im Result-Text. 14 von 19 Karten wurden nie unter dem aktuellen v2-Kriterium (Passquote je Eval / Dollar pro funded) neu bewertet, sie tragen noch Formulierungen, die auf das alte P(funded)-pro-Zeit-Kriterium (vor #106) hindeuten. Fehlerklasse F2 (Urteil unter altem Kriterium) fuer praktisch den gesamten Validiert-Bestand — der groesste systematische Befund aus Task F.
7. Mom-lowVIX traegt einen Selbstkorrektur-Vermerk (Status frueher faelschlich als Im Buch gefuehrt, hier korrigiert) — ein direkter Beleg fuer Fehlerklasse F8, der Kartenstatus war schon einmal falsch gepflegt.

---

## Zusammenfassung: die 5 groessten Luecken aus A/D/E/F

1. **57,2% aller Survivors (2.634 von 4.605) wurden nie gegen das Buch gerechnet** (Task E) — reiner Kosten-Deckel (`max_book_evals`), kein Bug, aber bisher nirgends beziffert. Darunter mindestens 30 Survivors mit sharpe_ann 2,0-2,4 (deutlich ueber jeder ermittelten Zufallsdecke), rein wegen Rang-Konkurrenz innerhalb des eigenen Jobs nie geprueft.
2. **14 von 19 Validiert/Backlog-Ideenkarten (Task F) tragen keine erkennbare Nachrechnung unter dem seit 16.08.2026 gueltigen v2-Kriterium** (#106) — praktisch der gesamte Ideen-Friedhof ausserhalb der 3 Live-Buch-Aufnahmen steht auf einem veralteten Bewertungsmassstab (Fehlerklasse F2).
3. **orb/orb_std koennen strukturell nie `deploy_ready` werden** (Task A5, neuer Fund) — das harte Skip-Gate prueft nur "delay"/"null"-Ergebnisfelder und ignoriert die in `hypothesis_bank.py` dokumentierte `null_ref`-Zuordnung (`ctl_random_level` fuer orb). Aktuell latent (0 orb-Kandidaten erreichten je die Kontroll-Batterie), wird aber zum harten Blocker, sobald ein orb-Fund so weit kommt — passt zu Noise-ORB NQ (Task F), das nie ins Live-Buch fand.
4. **Der 15:55-Exit-Fix (AP161) ist nur fuer sigcore-Module (tsmom/maband) deployt, 11 weitere Module laufen weiter auf dem alten 15:59-Close** (Task A7) — darunter `vix_bias.py`, das Modul hinter dem echten Live-Bank-Bein `VIX_spike_rev_NQ`. Das ist kein historischer, sondern ein AKTUELL laufender Backtest/Live-Bruch.
5. **Massive Achsen-Luecken im Register** (Task D): `tm_dir` (Long/Short-Achse) wird bei tsmom nur in 2,1% aller Trials, bei maband nur in 0,6% explizit getestet; bei 17 von 19 Nicht-tsmom/maband-Modi ueberhaupt nie. `gap` lief ausschliesslich fuer Montag (`gap_dow='[0]'`). `mb_start_min` deckt maximal bis 13:30 ET ab, der komplette Nachmittag ist fuer maband-Signalstarts ungetestet. `firstbar_ematrail` (2.880 Trials) und `vwap_pullback` (aktuelles Ersatz-Bein!) liefen beide ausschliesslich auf NQ, nie auf ES/RTY/YM.

---
