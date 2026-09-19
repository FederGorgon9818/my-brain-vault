---
tags: [projekt, trading, alpha-suche, session-momentum]
erstellt: 2026-09-16
aktualisiert: 2026-09-17 (Nachtrag 2, ein-weg: variant-scout + strategy-auditor)
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Session-Momentum-Kapitel sauber schließen
---

# Session Momentum Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 16.09.2026 vom `familien-scout`. Quelle des Konzepts: [[Momentum-Theorie (Futures)]] (Abschnitt 3, Lou/Polk/Skouras-Zeile), TN-Block in [[Hypothesen-Bank (Momentum & Averages)]] (12 Zeilen), SZ-Block in [[Hypothesen-Bank (Volumen & Flows)]] (60 Zeilen), [[Strategie-Logbuch]] #057/#113. Aufbau nach dem Vorbild [[VWAP-Offensive]] (Hand-Karte zu einem anderen Konzept, hier nicht angefasst) und [[Fibonacci Wege-Karte]].

> [!warning] Nachtrag 1 (16.09.2026, nach `verdict-auditor`)
> Zwölf Wege fehlten (**W36-W47**), vier Stände waren falsch (**W15, W16, W27/W28, W34**), sechs tote/validierte Verwandte fehlten, ein Skelett (**SES-W18a**) wäre am `H()`-Assert gescheitert, drei Zähler waren schief. Alles unten eingearbeitet, **keine Nummer umbenannt**. Wichtigste Folge: **SES-W15a ist zurückgezogen** (Weg ist teilgemessen, nicht offen), neu dazu **SES-W42a**. Die Nachtrag-Zeilen sind mit 🆕 bzw. ✏️ markiert.

> [!success] Nachtrag 2 (17.09.2026, Workflow `ein-weg` — Schritt 2 des EINEN Wegs)
> Die 6 gerankten Skelette liefen durch `variant-scout` (je Hypothese, parallel) und danach durch EINEN `strategy-auditor`-Batch-Call. Ergebnis: **1x direkt gebaut** (SES-W16a, `hypothesis_bank.py`), **1x gebaut mit Auflagen** (SES-W42a, Familie korrigiert, Kontrast-Zelle, SZ-57 verlinkt), **1x offen mit klarer Auflage** (SES-W6a, Reparatur von TN-03 statt neuer Zeile, braucht `prior='low'` + Prescan — noch nicht gerechnet), **3x durchgefallen** (SES-W8a: gegatete Seite am echten Bein in der falschen Richtung gemessen — 976 Trades, alle vier Schwellen negativ; SES-W6b: kein eigenes Why, ist ein Achsenwert von W6a; SES-W18a: Story sagt Gegenbewegung, ~10k gemessene Trades im selben Fenster sagen Fortsetzung, plus zwei der drei Pflichtbeilagen existieren nicht in der Engine — Abnahmekriterium unerreichbar). Details je Weg unten und in den H()-Kommentaren. Volltext des Batch-Reports: `discovery/scout_reports/` folgt beim nächsten `pipeline-auditor`-Lauf, bis dahin siehe Journal des Workflow-Laufs `wf_b636c89e-99b`.

**Was „Session Momentum" hier heißt:** die Beziehung zwischen zwei Zeit-Segmenten. Richtung, Größe, Form und Volumen eines Segments (Asien-Globex, Europa, Pre-Market, RTH-Open, Lunch, Nachmittag, Schlussstunde, Overnight als Ganzes) sagen die Bewegung des nächsten Segments voraus. Nicht ein einzelnes Signal, sondern ein Gitter aus Segment-Paaren.

> [!important] Die Lage in einem Satz
> Session Momentum ist **das am besten vermessene Konzept im ganzen Register** (1.693 Trials in den Kern-Wegen, 396 Survivors, 0 Kandidaten) — und trotzdem steht ein gutes Dutzend Wege bei **0 Trials**, weil ihre Jobs an ein bis zwei Prämissen-Configs gestorben sind oder weil die Beziehung nie als Weg formuliert wurde.

---

## Die fünf harten Randbedingungen

**1. `tsmom` und `maband` rechnen nur im RTH.** `sigcore.tmin_of` zählt Minuten seit 09:30, die Daten sind `between_time("09:30","15:59")`. Die Nacht kommt nur als **Tageskontext** rein (`tm_base="overnight"`/`"prev_rth"`, Gates `tm_on_ret_min/max`, `tm_gap_max`). Wer außerhalb 09:30-15:59 **handeln** will, braucht `mode="asian"` oder eine Modul-Spec. Kein neuer `mode`.

**2. Null-Schalter — Korrektur zur CLAUDE.md.** `controls.ctl_null` deckt seit AP137/AP157 auch `ts_reversal`, `last_hour`, `asian` und `vwap_pullback` ab (`controls.py` Z. 643/644), nicht nur `maband`/`tsmom`. `asian`-Wege können also `deploy_ready` werden. Ein **neuer** `mode` bleibt ausgeschlossen.

**2b. ✏️ Nachtrag: `mode="gap"` fehlt in genau dieser Liste.** Ein Gap-Kandidat (W27/W28/W43/W44) bekommt `{"ok": None, "note": "Modus ohne Null-Schalter"}` und kann damit **nie `deploy_ready`** werden. Wer den Gap-Ast ernsthaft öffnen will, braucht zuerst `tm_null` in `gap.py` — sonst ist jeder Gap-Job per Konstruktion Bank-Material.

**3. Ersatz schlägt Neuzugang** (#139 B3). Rang 1 dieser Karte ist der einzige verbliebene Ersatz-Slot für `NQ_LastHour_v3`, alles darunter ist „neues Bein" und hat strukturell die schlechtere Buch-Chance.

**4. `premise_failed` ist kein Tot-Stempel.** Der Runner wirft ein 72- bis 90-Config-Grid weg, wenn **eine oder zwei** Prämissen-Configs unter 1,0 pp IS-Edge bleiben (`discovery_runner.py` Z. 306-345). Vier Session-Wege (W6, W17-NQ/ES, W18, W20) stehen genau dort: nicht widerlegt, sondern nie gerechnet. Regel „Hypothese vor Urteil" gilt. **✏️ W15 gehört seit dem Nachtrag NICHT mehr in diese Aufzählung** (siehe unten).

**5. ✏️ Nachtrag: `prem_min_edge_pp` gibt es nur für Kontroll-Jobs.** `hypothesis_bank.H()` Z. 316: `assert prem_min_edge_pp is None or not book`. Ein Job mit Prämissen-Override hat `book=False`, also **kein Buch-Marginal und per Konstruktion keinen Kandidaten**. Ein blockierter Buch-Weg wird deshalb über eine **Bracket-Prämisse** repariert (Muster der 15 LL-Jobs, #137), nicht über den Override.

---

## Register-Stand (16.09.2026, Zähler nach Nachtrag korrigiert)

| Griff | Zahl |
|---|---|
| `n_total` im Register | **63.434 Trials** ✏️ (Runner läuft weiter, war 63.431) |
| Session-Wege gesamt (`asian`/`last_hour`/`gap` + `tsmom` overnight/prev_rth + TN-/SZ-/on01-/lp_prevday-Jobs) | **1.693 Trials, 396 Survivors, 0 Kandidaten** |
| `tsmom tm_base="overnight"` | 145, **0 Survivors** |
| `tsmom tm_base="prev_rth"` | 181, 7 Survivors (alle `tm_sig_start=0`) |
| Overnight-Gate `tm_on_ret_max` / `_min` | **18 / 36** (= 54 Trials), alle aus `on01_cashopen_decision_NQ`, alle `tm_sig_start=0`, `tm_sig_len` 15/30 — **kein einziger mit langem Fenster** |
| `mode="asian"` | 298, 65 Survivors — **jeder Trial handelt im RTH** (`tr_start=09:30`) außer **einem** (19:00-23:00 → 23:00-03:00) |
| `mode="last_hour"` | 463, 153 Survivors |
| `mode="gap"` | 397, 143 Survivors |
| `tm_sig_start` ≥ 285 (Schlussstunden-Fenster) | 298 — davon **292 aus `hyp_TS21_NQ/_ES`** ✏️ |
| `tm_signal="er_ret"` | 39, **alle `tm_sig_start=0`** ✏️ |
| `tm_rvol_min/max` gesamt | 32.654 — davon `tm_rvol_**max**` (ruhige Seite) **24**, alle `hyp_AR11_NQ` im Open-Fenster ✏️ |
| Kompressions-Gates `tm_atr_exp_max`/`tm_sigma_q_max` | 229, 59 Survivors, 0 Kandidaten — **alle im Open-Fenster** (TV-02/03, AB-03/06, TV-07/08/13, AR-04) ✏️ |
| TN-Block in `hypothesis_bank.py` | **8** H()-Zeilen ✏️ (TN-01/03/04/05/08/09/10/12), war fälschlich 7 |
| SZ-Block in `hypothesis_bank.py` | **0 von 60 Zeilen** (136 H()-Zeilen gesamt) |
| Queue | 899 Jobs: 468 done, 425 premise_failed, 4 pending, 1 running, **1 failed** ✏️ |

**Die leeren Achsen:** Overnight-Gate im langen Fenster (0), Segment-Ketten (0), Globex-Form ER/Pfadlänge/RVOL (0), Pre-Market-Segment (0), Lunch-Linearität `er_ret` außerhalb des Open-Fensters (0), **RTH als Quelle statt Ziel (0)** 🆕, **Segment-Range als Prädiktor im Segment-Paar (0)** 🆕, **gleiches Uhrzeit-Fenster über Tage (0)** 🆕, **ruhige Volumen-Seite intraday (0)** 🆕, **Segment-Grenze als Schiene (0)** 🆕.

---

## Die 47 Wege

Elemente: Segmente **S1** Asien-Globex 19:00-03:00 · **S2** Europa 03:00-09:30 · **S3** Pre-Market 08:30-09:30 · **S4** RTH-Open 09:30-10:30 · **S5** Lunch 11:30-13:30 · **S6** Nachmittag 13:30-15:00 · **S7** Schlussstunde 15:00-16:00 · **S8** Overnight gesamt · **S9** Vortages-RTH · **S10** RTH als Ganzes (Quelle) 🆕; dazu Zustände je Segment (Richtung, **Größe/Range**, Pfadform, **Volumen**, Kette, Wochentag), die Segment-Grenzen (Open, High/Low, Close, **Globex-Reopen-Lücke** 🆕) und der Preis.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| W1 | S1-Richtung setzt sich im RTH fort | Trend Following | Signal | **im Buch** (`NQ_Asia-Dir-USopen_d260820`) | `asian us_dir` ✅ | Bestand |
| W2 | S1-Richtung dreht am US-Open | Mean Reversion | Signal | ❌ tot ([[Strategie-Logbuch#028]], Asia-Fade NQ+RTY) | `asian fade_us` ✅ | — |
| W3 | S2-Richtung setzt sich im RTH fort | Intraday Bias | Signal | 🟡 gemessen ohne Kandidat (55 Trials) | `asian` rs 03:00-09:30 ✅ | Ersatz Asia-Dir (probiert) |
| W4 | S2-Richtung dreht am US-Open | Mean Reversion | Signal | offen, **keine Story** (kein Akteur benennbar; der Unwind sitzt um 11:00, das ist W18) | `asian fade_us` ✅ | — |
| W5 | S8 setzt sich im RTH fort | Intraday Bias | Signal | 🟡 gemessen ohne Kandidat (TN-01, 97 Trials) | `tsmom tm_base=overnight` ✅ | neues Bein |
| W6 | S8 dreht im RTH (Tug-of-War) | Mean Reversion | Signal | ✏️ Short-Seite (**SES-W6a**) offen mit Auflage (Reparatur TN-03, `prior='low'`+Prescan noetig, noch nicht gerechnet); Long-Seite (**SES-W6b**) ❌ durchgefallen (kein eigenes Why, Achsenwert von W6a) | `tsmom overnight + fade` ✅ | **SES-W6a** (Reparatur TN-03) |
| W7 | S8-Größe als Schwelle statt Gewicht | Intraday Bias | Filter | 🟡 gemessen ohne Kandidat (TN-12, 25 Trials) | `tm_thr`-Leiter ✅ | Achse in SES-W6a/b |
| W8 | S8 als **Filter** auf die Schlussstunde | Intraday Bias | Filter | ✏️ ❌ **durchgefallen** (ein-weg 17.09.) — Mechanismus direkt am echten Bein nachgemessen (976 Trades, Tages-Filter auf \|on_ret\|): die ruhige Seite liegt an **allen vier** Schwellen unter der unruhigen (z = -0,14/-0,24/-0,78/-0,64), reproduziert die alpha-scout-Falsifikation vom 23.08. mit der richtigen Kennzahl (expR) | `tsmom` sig 0-240 + `tm_on_ret_max` ✅ | — |
| W9 | S9 → heute RTH | Intraday Bias | Signal | 🟡 gemessen ohne Kandidat (180 Trials, 7 Survivors) | `tsmom tm_base=prev_rth` ✅ | neues Bein |
| W10 | Kette 3 gleichgerichteter S8 | Trend Following | Filter | offen, **0 Trials** (TN-11 nur Bank) | **Modul-Spec A** | **(Swing)** als Filter prop-tauglich |
| W11 | S8 **selbst handeln**, über Nacht halten | Swing | Signal | teil-tot (#028 Overnight-Drift; laut #137 nur 3 Varianten, nie im richtigen Fenster) | `asian` ✅ | **(Swing)** Live-Buch-Merker, E8 verbietet Overnight |
| W12 | S4 → Resttag, Fortsetzung | Trend Following | Signal | **im Buch** (`NQ_Momentum_d260818`); Ersatz mit ON-Gate gemessen (71 Trials, 0 Kand.) | `ts_reversal`/`tsmom` ✅ | Bestand |
| W13 | S4 → S7 (first30 → last30) | Intraday Bias | Signal | ❌ tot ([[Strategie-Logbuch#057]], 0/48) | `tsmom` ✅ | — |
| W14 | Vormittag → S7 | Intraday Bias | Signal | **im Buch** (`NQ_LastHour_v3`) | `last_hour` ✅ | Bestand |
| W15 | S7-intern 15:00-15:45 → 15:45-15:55 | Intraday Bias | Signal | ✏️ 🟡 **teilgemessen, Verwandte negativ** — `hyp_TS21_NQ/_ES` 292 Trials im selben Fenster (285/300/315/330 × len 15/30), **1 Survivor, 0 Kandidaten**, bereits als Ersatz `NQ_LastHour_v3`; dazu #087 auf 4 Märkten negativ. **Skelett zurückgezogen** | `tsmom tm_sig_start=330` ✅ | Ersatz-Slot bereits einmal bespielt |
| W16 | S5-Steigung → Nachmittag | Trend Following | Signal | ✏️ ✅ **gebaut** (ein-weg 17.09.) — `hypothesis_bank.py H("SES-W16a")`, stärkste Story der Gruppe laut `strategy-auditor`; Auflage: SZ-13 (Vault-Bank, R² statt ER) geht nicht zusätzlich in dieselbe Rechenrunde | `tsmom tm_signal=er_ret` ✅ | SES-W16a (Job gebaut, noch nicht enqueued) |
| W17 | S5-Ausbruch dreht bis 14:00 | Mean Reversion | Signal | 🟡 auf RTY gemessen (90 Trials, 0 Survivors), NQ/ES Prämisse gefallen | `tsmom fade` ✅ | kein Skelett: Richtung einmal sauber negativ |
| W18 | Europa-Close 11:00-11:30 gegen den Vormittag | Mean Reversion | Zeitfenster | ✏️ ❌ **durchgefallen** (ein-weg 17.09.) — 12 im selben Fenster bereits gemessene Fade-Zellen (~10k Trades) sind ALLE negativ (expR -0,026 bis -0,169, PF 0,49-0,93, 0 Survivors), der Spiegel (Fortsetzung) hat 5-8 Survivors; zwei der drei Pflichtbeilagen (DST-Split, Feiertags-Placebo) existieren nicht in `controls.py` — Abnahmekriterium für `deploy_ready` damit unerreichbar | `tsmom` sig 0-90 fade ✅ | — |
| W19 | S3 (08:30-Daten) → RTH | Intraday Bias | Signal | offen, **0 Trials**, Fenster außerhalb des RTH-Frames | **Modul-Spec B** | neues Bein |
| W20 | Momentum **innerhalb** der Globex-Nacht | Trend Following | Signal | 🟢 offen, **1 Prämisse-Trial** (TN-10) | `asian` ✅ | kein Skelett: E8-Handelbarkeit ungeklärt |
| W21 | Globex-Reopen 18:00-18:30 → Nacht | Trend Following | Signal | offen, **0 Trials** (SZ-22) | `asian` ✅ | wie W20 |
| W22 | **hindurch**: Nacht-Range bricht beim London-Open | Trend Following | Signal | ❌ tot (#028, 46 Configs) | `asian break` ✅ | — |
| W23 | **hindurch**: Nacht-Range bricht am RTH-Open | Trend Following | Signal | 🟡 Bank-Fund (`NQ_Asia-Break-USsession`, #028) + 17 Trials/4 Surv. ✏️ Zweitmarkt **ES-Break in #028 ausdrücklich getötet** | `asian break_us` ✅ | Bank, kein Buch |
| W24 | **abprallen** an der Segment-Range-Grenze | Mean Reversion | Level | ❌ tot (#028) **und** Level-Reflexivität separat widerlegt ([[Strategie-Logbuch#113]]/#114, #138, #149) | `asian fade_us` ✅ | — |
| W25 | **kreuzen und halten**: Session-Open-Reclaim | Trend Following | Signal | offen, Verwandter tot (#108 VWAP-Cross am NY-Open = Wegmessung, #107) | `maband price_ma`/`vwap reclaim` ✅ | kein Skelett ohne neuen Grund |
| W26 | **kreuzen und scheitern**: Fakeout an der Grenze | Mean Reversion | Signal | offen, kontaminiert (#065-#068 ORB-Fade, `fb01_failbreak_*` liegen bereit) | `asian break` + `mb_invert` ✅ | eigener Fehlausbruch-Lauf |
| W27 | **hin zu**: Rückkehr zum Vortages-Close (Gap-Fill) | Mean Reversion | Level | ✏️ 🟡 gemessen (397 Trials), Buch-Marginal negativ (#137 Nr. 3), RTY_Gap-fade raus (#130); **`ideas.json` „Gap-Fade klein" getötet — aber laut AP116-Korrektur an der Selektions-/Buch-Marginal-Stufe, nicht an der Prämisse: 45 NQ-Survivors mit `gap_confirm_min=10` existieren, `gen_gap_NQ` PBO 71-96 % im Zufallsband** | `gap` ✅ (kein Null-Schalter!) | — |
| W28 | **weg von**: Gap-Erweiterung, an Nacht-Volumen gekoppelt | Trend Following | Filter | ✏️ **nicht jungfräulich**: `ideas.json` „Gap-Continuation (grosse Gaps)" = **Validiert**, OOS +7-9 %, D-Note, 17 Trades/Jahr, Report `NQ_GAP_cont`, nie im Buch. Die **Volumen-Kopplung** ist der offene Teil, 0 Trials | **Modul-Spec C** | neues Bein, Basis existiert als Bank-Fund |
| W29 | ✏️ **Segment→Segment, später Einstieg** in laufender Richtung (Etikett „entlanglaufen" war falsch, gehört zu W47) | Trend Following | Signal | 🟡 gemessen ohne Kandidat (7.796 Trials, `tm_sig_start` 120/210) | `tsmom` ✅ | — |
| W30 | Globex-ER als Trendtag-Filter | Intraday Bias | Filter | offen, **0 Trials** (TN-07) | **Modul-Spec C** | Filter auf W1 |
| W31 | Globex-Pfadlänge gegen Gap (Absorption) | Intraday Bias | Filter | offen, **0 Trials** (TN-06) | **Modul-Spec C** | Filter auf W27 |
| W32 | Nacht-Volumen/RVOL als Filter | Intraday Bias | Filter | offen, **0 Trials** (VV-19/20) | **Modul-Spec C** | Filter auf W1/W27 |
| W33 | Wochentags-Struktur des Segments | Swing | Filter | 🟡 gemessen ohne Kandidat (TN-09, 21 Trials) | `tm_dow` ✅ | — |
| W34 | Halbtags-/komprimierter Fahrplan | Intraday Bias | Zeitfenster | ✏️ offen, **keine Story stark genug** (6-9 Tage/Jahr) **und Friedhof daneben**: `ideas.json` „Kalender/Structural" = Getötet, „komplett abgearbeitet" (#087, AP49) | `cal` + `tm_dow` ✅ | — |
| W35 | DST-Wanderung des Segment-Effekts | — | Kontrolle | **Kontrollweg, keine Handels-Story** | Auswertungs-Split | Pflichtbeilage zu W18 (✏️ zusammen mit SZ-60 und SZ-45) |
| W36 🆕 | **S10 → S8**: heutiger RTH-Return setzt sich in der kommenden Nacht fort | Swing | Signal | offen, **0 Trials** — jeder der 298 `asian`-Trials handelt im RTH (`tr_start=09:30`), keiner mit RTH als Quelle | `asian` rs 09:30-15:55 / tr 16:00-09:25 ✅ | **(Swing)** Live-Buch-Merker, E8 verbietet Overnight |
| W37 🆕 | **S10 → S8**: heutiger RTH-Return dreht in der kommenden Nacht (Lou/Polk/Skouras rückwärts) | Swing | Signal | offen, **0 Trials** | wie W36 ✅ | **(Swing)** Live-Buch-Merker |
| W38 🆕 | Nacht-**Range** (eng/weit) sagt die RTH-Bewegung voraus | Intraday Bias | Filter | offen, **0 Trials** als Segment-Paar; Tages-Verwandte gemessen (TV-03 „kontrahierende Vola", AB-03 „Squeeze", zusammen im 229er-Block, 59 Surv., **0 Kandidaten**) | **Modul-Spec C + `gx_range`** | Filter auf W1/W27 |
| W39 🆕 | **IB-Breite** (eng/weit, relativ ATR20) sagt den Nachmittags-Ausbruch voraus (SZ-31) | Trend Following | Filter | offen als Segment-Paar, **0 Trials mit Nachmittags-Fenster** (alle 229 Kompressions-Trials sitzen im Open-Fenster) | Proxy `tm_atr_exp_max`/`tm_sigma_q_max` ✅ (Tages-Vola, nicht IB-Breite), echte IB-Breite = **Modul-Spec F**; `i2 ib_max_atr` existiert, hat aber **keinen Null-Schalter** | neues Bein |
| W40 🆕 | Segment(T-1) → **dasselbe Uhrzeit-Fenster**(T), Fortsetzung (Metaorder-Fahrplan, SZ-51) | Trend Following | Signal | offen, **0 Trials** — `tm_base="prev_rth"` nimmt den GANZEN Vortag, das uhrzeitgleiche Fenster gibt es als Achse nicht | **Modul-Spec D** | neues Bein |
| W41 🆕 | Serien-**Ende** im gleichen Uhrzeit-Fenster, Fade (SZ-52) | Mean Reversion | Signal | offen, **0 Trials** | **Modul-Spec D** | neues Bein |
| W42 🆕 | **Volumen-Zustand** eines RTH-Segments sagt das nächste RTH-Segment voraus (ruhiger Vormittag → Nachholen am Nachmittag, SZ-57/34/49) | ✏️ Trend Following (Filter) — Familie korrigiert, siehe unten | Filter | ✏️ ✅ **gebaut** (ein-weg 17.09.) — `hypothesis_bank.py H("SES-W42a")`, Story hält mit Vorbehalt; Auflagen umgesetzt: Familie korrigiert, Kontrast-Zelle `tm_rvol_max=None` im Grid, Bank-Zeile SZ-57 verlinkt | `tsmom` sig 0-150 + `tm_rvol_max` ✅ | SES-W42a (Job gebaut, noch nicht enqueued) |
| W43 🆕 | **Zweite Gap-Grenze, hin zu**: Fill der Globex-Reopen-Lücke (Close 17:00 vs. Open 18:00, SZ-23) | Mean Reversion | Level | offen, **0 Trials** | **Modul-Spec G** (`mode="gap"` kennt nur den RTH-Open und hat keinen Null-Schalter) | kein Skelett: **dieselbe E8-Nachtfrage wie W20/W21** |
| W44 🆕 | **Zweite Gap-Grenze, weg von**: Erweiterung der Reopen-Lücke | Trend Following | Signal | offen, **0 Trials**, Story schwach (um 18:00 fehlt der Info-Schock, der große Gaps trägt) | **Modul-Spec G** | wie W43 |
| W45 🆕 | **S1 → S2**: Asien-Richtung setzt sich im Europa-Segment fort | Trend Following | Signal | offen, **0 Trials** — kein `asian`-Trial mit `tr` 03:00-09:30 | `asian` rs 19:00-03:00 / tr 03:00-09:30 ✅ | kein Skelett: E8-Nachtfrage wie W20/W21 |
| W46 🆕 | **S1 → S2**: Asien-Richtung dreht im Europa-Segment | Mean Reversion | Signal | offen, **0 Trials** | wie W45 ✅ | wie W45 |
| W47 🆕 | **entlanglaufen** (echtes Glied): Preis nutzt Nacht-High/-Low oder Vortages-Close als **Schiene**, statt durchzubrechen oder abzuprallen | Trend Following | Level | offen, **0 Trials** — `mb_band_evt="walk"` existiert, aber nur für Bollinger/Keltner/Donchian, nicht für ein Segment-Level | **Modul-Spec E** (`mb_level_src` = prev_close / on_high / on_low + bestehende `walk`-Logik + `mb_rand_level` als Pflichtkontrolle) | neues Bein |

**Vollständigkeitsnotiz:** Die Preis↔Grenze-Reihe ist nach dem Nachtrag vollständig besetzt: hin zu (W27, W43), weg von (W28, W44), hindurch (W22, W23), abprallen (W24), **entlanglaufen (W47)**, kreuzen+halten (W25), kreuzen+scheitern (W26). W4, W34, W35, W44 stehen bewusst ohne Skelett in der Tabelle („keine Story, weil…").

---

## Die Wege im Einzelnen (nur die mit Skelett)

### ❌ W8 → SES-W8a DURCHGEFALLEN (ein-weg 17.09.2026)
**Bewegung:** Das Overnight-Segment als Filter auf die Schlussstunde, long.
**Ergebnis `ein-weg`:** `variant-scout` fand n=90 mögliche Varianten, aber nur EINE Achse trägt die These überhaupt, und genau die ist am echten `NQ_LastHour_v3`-Bein direkt nachgemessen worden (976 Trades/10 Jahre, Tages-Filter auf `|on_ret|` bei den vier geplanten Schwellen 0,0015/0,003/0,005/0,008): expR fällt von +0,1256 auf +0,1156/+0,1162/+0,1063/+0,1147, die ruhige Seite liegt an **allen vier** Schwellen unter der unruhigen (z = -0,14/-0,24/-0,78/-0,64). Reproduziert die bereits am 23.08. gefundene alpha-scout-Falsifikation (Spec B/TN-04), diesmal mit der richtigen Kennzahl (expR statt R/Jahr). Kein `H()`-Eintrag. Kein Story-Check nötig — Varianten-Stufe hat den Weg schon beendet.
**Story:** Das LastHour-Bein lebt von der Hedging-Nachfrage des Tages (Gao/Han/Li/Zhou JFE 2018, Baltussen et al. JFE 2021, beide im [[Research-Cache]]). Ist die Bewegung schon über Nacht gelaufen, haben Dealer und LETFs ihren Hedge-Bedarf in der dünnen Nacht abgearbeitet — am Nachmittag fehlt dann der Zwangskäufer. Kleiner Overnight-Move heißt: die Nachfrage steht noch aus.
**Stand:** offen. `hyp_TN04_NQ` lief 54 Trials (18 Survivors, 0 Kandidaten) — aber im Modus `last_hour`, und der ruft **keinen** Kontext-Gate auf (`qbt.py` Z. 848-905). Das Gate war nie an. Die 54 Register-Trials mit `tm_on_ret_min/max` sitzen alle in `on01_cashopen_decision_NQ` mit `tm_sig_start=0, tm_sig_len=15/30` — **kein einziger im langen Fenster**.
**Engine:** `tsmom tm_sig_start=0 tm_sig_len=240 tm_base=open tm_dir=long_only tm_stop_mode=range tm_exit=eod` + `tm_on_ret_max`. Bitgleich zum Bein außer dem Gate.
**Buch:** Ersatz `NQ_LastHour_v3`. **Auflage (AR-04):** ein Gate, das nur Trades ausdünnt, muss gegen die Zufalls-Ausdünnung antreten — `hyp_AR04_NQ` ist die vorhandene Pflichtkontrolle.

### ✏️ W15 · SES-W15a ZURÜCKGEZOGEN (kein Skelett mehr)
**Bewegung:** Richtung 15:00-15:45 sagt 15:45-15:55.
**Was der Nachtrag ergab:** Das Fenster ist **nicht offen**. `hyp_TS21_NQ` / `hyp_TS21_ES` („TS-21 MOC-Imbalanz braucht Orderflow im Signal, AP116-Nachtest zu #087") haben **292 Trials** gerechnet: `tm_sig_start` 285/300/315/330 × `tm_sig_len` 15/30, `tm_base="window"`, `tm_exit="eod"`, dazu Stop-Leiter und die vollen Bestätigungsachsen (`tm_delta_min`, `tm_rvol_min`, `tm_ema_confirm`, `tm_vwap_side`) — Ergebnis **1 Survivor** (`TS-21_NQ|tm_sig_start=330,tm_sig_len=30,confirm=delta0.15,tm_stop_mult=0.8`, PF 1,48, 27 Trades/Jahr) und **0 Kandidaten**, und zwar bereits **als `replaces_leg: NQ_LastHour_v3`**, also im exakt selben Buch-Slot. Das sind genau die „298 Trials mit `tm_sig_start` ≥ 285", die die erste Fassung dieser Karte als Leer-Beleg zitiert hat, ohne den Job zu nennen.
**Abgrenzung zu #087 war falsch:** #087 maß `ref` 15:00 / 15:30 / 15:45 auf NQ/ES/RTY/YM (0/72 Survivors, „Late-Day-Momentum-Edge FÄLLT zum Close hin ab"), nicht „15:50-16:00". Die Gegenaussage zur Story steht damit auf vier Märkten.
**Verwandte Tote:** `hyp_TS21_NQ`/`_ES` (je 146 Trials), `ideas.json` „Kalender/Structural" = **Getötet** (#087/AP49, „komplett abgearbeitet"), #137 nennt TS-21 namentlich als Nachfolge-Hypothese zu #087.
**Was den Weg wieder öffnen würde (nicht heute):** Logbuch #137 dokumentiert einen offenen Engine-Bug — `tm_delta_src` kommt in `sigcore.py` kein einziges Mal vor, wer `tm_delta_src="real"` **und** `tm_delta_min` setzt, bekommt still ein **Proxy**-Gate. TS-21 nutzt genau diese Kombination. Die Imbalanz-Variable ist also weiterhin nicht mit echtem Delta getestet — aber ein neuer Job würde denselben stillen Proxy fahren. **Erst Bug fixen (plus `engine-regression-tester`), dann neu bewerten.** Reparametrisierung (len 45 statt 15/30) ist kein neuer Winkel.

### W6 → SES-W6a (offen mit Auflage) / SES-W6b (❌ durchgefallen) · Tug-of-War
**Bewegung:** Großer Overnight-Move dreht den RTH-Tag — Short-Seite und Long-Seite getrennt.
**Ergebnis `ein-weg` (17.09.2026):** `strategy-auditor` — SES-W6a "Story hält mit Vorbehalt": Why ist kausal (Nacht-Klientel trifft am Open auf die bewertenden Desks), aber das Signal ist im Code `prev_close→open`, also bitgleich der Gap-Formel (`sigcore.py:674/686`) — die Neuheits-Behauptung "ganzer Globex-Pfad" ist damit hinfällig, das Feature existiert in der Engine nicht. **Auflage:** als Reparatur der bestehenden Zeile `TN-03` führen (nicht als neue ID, sonst zählt die Idee doppelt gegen die Zufallsdecke), Why auf "Close-to-Open-Return" korrigieren, `prior='low'` + Prescan vor dem Grid (Lehre 139/#133) — noch nicht gerechnet, das ist der nächste Schritt. SES-W6b "Story fällt durch, nicht bauen": keine eigene ökonomische Story, das Why ist wörtlich das von W6a mit einem anderen Achsenwert (`tm_dir`); `ctl_null` als "Pflichtkontrolle" ist keine eigene Hypothese. **Weg nach vorn für W6b:** als `tm_dir=long_only`-Achse im W6a/TN-03-Grid mitfahren lassen, keine eigene ID.
**Story:** Lou/Polk/Skouras (JFE 2019): Overnight- und Intraday-Segment haben verschiedene Klientelen und reverten gegeneinander. Nachts kauft eine Kohorte ohne US-Cash-Liquidität; am Open trifft sie auf die Desks, die den Index wirklich bewerten. Iwanaga/Sakemoto (SSRN 5807282) zeigen die inverse Richtung explizit für US-Indizes, warnen aber vor Decay nach den 2010ern.
**Stand:** offen, `hyp_TN03_NQ` fiel an **einer** Config. Fix nach dem Muster der 15 LL-Jobs aus #137: Prämisse als Bracket über drei Schwellen.
**Warum zwei Skelette:** NQ hat Aufwärtsdrift (#108, Goyal/Jegadeesh) — eine Long-Seite, die „funktioniert", kann reiner Drift sein. `ctl_null` läuft bei W6b als Pflichtkontrolle mit.
**Abgrenzung:** Overnight-Gap-Fade ist tot (`ideas.json`, #028) — dort die **Preislücke**, hier der **Segment-Return** über den ganzen Globex-Pfad. Die Trennung muss der Test selbst zeigen (Trade-Überlappung < 30 %).

### ✅ W16 → SES-W16a GEBAUT (ein-weg 17.09.2026)
**Ergebnis `ein-weg`:** `variant-scout` (n=270, "Testbar") + `strategy-auditor` ("Story hält" — stärkste der Gruppe: klarer Akteur, klare pausierende Gegenpartei, Messgröße passt zum Akteur, kein Look-ahead). Direkt als `H("SES-W16a", ...)` in `hypothesis_bank.py` eingebaut (108 Configs, `--dry` sauber), `pipeline-auditor`-Check vor `--enqueue --push` läuft. **Auflage:** die Vault-Bank-Zeile SZ-13 (dieselbe Idee mit R² statt ER als Glättemaß) geht NICHT zusätzlich in dieselbe Rechenrunde.
**Story (Original):** Im dünnsten Buch des Tages laufen TWAP-/POV-Algos stur weiter, während diskretionäre Gegenparteien pausieren. Ein Mittags-Segment, das fast linear verläuft (hohe Efficiency Ratio), ist der Fußabdruck genau eines arbeitenden Programms — und ein Programm, das um 13:00 nicht fertig ist, arbeitet weiter. Gemessen wird die **Glätte**, nicht die Bewegung.
**Stand:** ✏️ präzisiert. `tm_signal="er_ret"` hat 39 Register-Trials, **alle mit `tm_sig_start=0`** — im Lunch-Fenster also 0. Die **nackte** Fortsetzungsrichtung im Mittagsfenster ist dagegen **nicht** unberührt: `sz10_usflow_bias_ES` lief 40 Trials mit `tm_sig_start` 120/150, `tm_sig_len=30`, `tm_side="momentum"`, `tm_signal="ret"` → **0 Survivors**. Der offene Teil ist damit ausschließlich der **Linearitätsfilter**, nicht die Richtung an sich. `sz11_lunch_fade_*` testete zusätzlich die Gegenrichtung.
**Konsequenz fürs Skelett:** `er_ret` ist Pflicht, nicht Kür — ein Lauf mit `tm_signal="ret"` würde nur ES-Ergebnisse auf NQ wiederholen.

### ❌ W18 → SES-W18a DURCHGEFALLEN (ein-weg 17.09.2026)
**Ergebnis `ein-weg`:** `variant-scout` stufte den Weg noch als "Grenzwertig" ein (n=243), aber `strategy-auditor` widerlegt die Richtung direkt aus den Daten: 12 bereits gemessene Fade-Zellen genau in diesem Fenster (~10k Trades) sind ALLE negativ (expR -0,026 bis -0,169, PF 0,49-0,93, 0 Survivors — `sz08_euclose_fade_NQ/ES`, `er01_impact_split_NQ/ES`), während der Spiegel (Fortsetzung statt Unwind, `tm_side=momentum`) auf NQ Median-expR +0,067/+0,069 mit 5 bzw. 8 Survivors zeigt — die Daten sagen in genau diesem Fenster Fortsetzung, nicht Unwind. Diese Jobs starben NICHT an einem Konstruktionsbug wie die 15 LL-Jobs aus #137 (dort n=0 durch KeyError), sondern haben mit 617-1224 Trades je Zelle echtes Geld verloren — "premise_failed ist kein Tot-Stempel" trägt hier nicht. Zusätzlicher K.o.: zwei der drei selbst gesetzten Pflichtbeilagen (W35/DST-Split, SZ-60/Feiertags-Placebo) existieren nicht in `controls.py` — der Weg kann nach seiner eigenen Abnahmebedingung nie `deploy_ready` werden. **Weg nach vorn (nicht heute):** entweder die Story umdrehen (Hedge-Aufbau statt Unwind, passend zur gemessenen Richtung — anderes Why, eigener Akteur) oder erst die zwei fehlenden Kontrollen in `controls.py` bauen und danach nur den wirklich offenen Rest testen (Exit exakt am Fensterende, `tm_hold_min` 30/45).
**Story (Original):** Europäische Bücher schließen gegen 17:30 MEZ = 11:30 ET und stellen ihre US-Hedges vorher glatt; der Rückfluss läuft gegen die Vormittagsrichtung.
**Stand:** offen, 144 gebaute Configs (NQ+ES) an je zwei Prämissen-Configs gestorben.
**✏️ Was der Nachtrag korrigiert:** Die erste Fassung wollte den `premise.min_edge_pp`-Override **und** `book_target: new_leg` — das geht nicht. `H()` Z. 316 lässt `prem_min_edge_pp` nur mit `book=False` zu, und ein Job ohne Buch rechnet kein Marginal, kann also **per Konstruktion keinen Kandidaten liefern**. Ein Kontroll-Job auf Rang 6 der Buch-Chance-Liste war ein Widerspruch in sich. **Neue Form:** normaler Buch-Job (`book=True`) mit **Bracket-Prämisse** über drei Fade-Schwellen, exakt das Muster der 15 LL-Jobs aus #137. Wer zusätzlich reine Messzahlen will, hängt einen **separaten** `book=False`-Lauf daneben und weiß, dass er nie `deploy_ready` wird.
**Pflichtbeilagen (drei, nicht eine):**
- **W35 / SZ-09+25 (DST):** wandert der Effekt in den Misalignment-Wochen nicht um eine Stunde mit, ist kein europäischer Akteur dahinter.
- ✏️ **SZ-60 (Akteurs-Abwesenheit):** an europäischen Feiertagen muss der Effekt auf ungefähr null einbrechen. Billiger als die DST-Auswertung und schon in der Bank formuliert.
- ✏️ **SZ-45 (Markt-Placebo):** Ordnung NQ/ES > RTY. Zeigt RTY den stärksten Effekt, ist die Akteurs-Zuordnung falsch und SZ-08 verliert sein Why.
Ohne diese drei kein `deploy_ready`.

### ✅ W42 → SES-W42a GEBAUT MIT AUFLAGEN (ein-weg 17.09.2026)
**Bewegung:** Volumen-Zustand des Vormittags-Segments gatet den Nachmittags-Entry in Richtung des Vormittags.
**Ergebnis `ein-weg`:** `variant-scout` (n=162, "Testbar") + `strategy-auditor` ("Story hält mit Vorbehalt" — Akteur plausibel, RVOL-Gate liest ein abgeschlossenes Fenster, kein Look-ahead; aber ungelöster Widerspruch im ursprünglichen Why — ein arbeitendes Programm erzeugt Volumen, hier soll gerade WENIG Volumen sein Fußabdruck sein — und Familie war als Intraday Bias falsch einsortiert, vorhergesagt wird die Fortsetzung des Vormittags-Vorzeichens, das ist Trend Following mit Filter). **Drei Auflagen umgesetzt** beim Bau von `H("SES-W42a", ...)`: Why um den auflösenden Satz ergänzt (unterfülltes Programm erzeugt das fehlende Volumen selbst), Familie auf Trend Following korrigiert, Kontrast-Zelle `tm_rvol_max=[None, 0.7, 0.8, 0.9]` im Grid (die ungefilterte Basislinie hyp_TS02_NQ/hyp_TK03_NQ lebt bereits, Messlatte ist "besser als die Basislinie"), Bank-Zeile SZ-57 verlinkt (dort Range, hier Richtung — dieselbe RVOL-Prämisse zählt beim Bank-Eintrag nur einmal). 72 Configs, `--dry` sauber, `pipeline-auditor`-Check vor `--enqueue --push` läuft.
**Story:** Ausführungsalgos schätzen ihr Volumenprofil aus der Historie (POV/VWAP-Schedules). Bleibt der Vormittag unter dem Erwartungswert, ist die Tagesorder **nicht** abgearbeitet — der Rest muss am Nachmittag laufen, und zwar in derselben Richtung, in die der Vormittag schon gelaufen ist. SZ-57 formuliert die Range-Variante, SZ-34 die Rückgabe-Variante, SZ-49 das Tagestyp-Label.
**Stand:** offen für die ruhige Seite. `tm_rvol_max` hat im **ganzen Register 24 Trials**, alle aus `hyp_AR11_NQ` („Volumen-MA als Aktivitäts-Gate", Open-Fenster, 0 Kandidaten). Die laute Seite ist dagegen breit gemessen: 5.096 Trials mit `tm_rvol_min` 1,2/1,6 bei `tm_sig_start` 120/210, **0 Survivors**. Genau das ist das Argument, die andere Seite zu drehen statt sie zu wiederholen.
**Engine:** `tsmom tm_sig_start=0 tm_sig_len=150 tm_rvol_max=[0.8, 0.9] tm_exit=eod`, beide Richtungen. Der RVOL-Gate misst das Volumen **des Signalfensters** (`sigcore` Z. 987-995) — mit Fenster 09:30-12:00 ist das exakt der Vormittag, Entry folgt danach.
**Auflagen:** AR-04 (Zufalls-Ausdünnung) ist Pflicht — ein Gate, das nur ausdünnt, muss den Zufallsfilter schlagen. Dazu die Trennung gegen den Vola-Zustand: ist „ruhiger Vormittag" nur ein Proxy für niedrige Tagesvola, greift TV-03/AB-03 schon (229 Trials, 59 Survivors, 0 Kandidaten).

---

## Swing-Zeilen (mitgeführt, nicht fürs Prop-Buch)

- **W11 · Das Overnight-Segment selbst handeln.** Entry vor dem Close, Halten über Nacht. Teil-tot: Overnight-Drift 2-3h ET getötet (#028), laut #137 aber nur 3 Varianten und „nie im richtigen Fenster im Register"; Overnight-Reversal ist Bank-validiert (#056). **E8 verbietet Overnight-Halten** ([[Research-Cache]], 10.08.2026) → Live-Buch-Merker, kein Prop-Job.
- **W10 · Kette von 3 gleichgerichteten Nächten.** Als **Filter** auf einen Intraday-Entry prop-tauglich, als eigene Mehrtages-Position Live-Buch-Merker. Braucht Modul-Spec A.
- 🆕 **W36 / W37 · RTH als QUELLE, Nacht als Ziel.** Lou/Polk/Skouras ist bidirektional: wenn Overnight und Intraday verschiedene Klientelen haben und gegeneinander reverten, sagt der heutige RTH-Return das kommende Overnight-Segment genauso voraus wie umgekehrt. Die Karte hatte bisher **nur** Paare mit RTH als Ziel (W1/W3/W5/W6/W9/W19). Im Register faktisch 0 Trials: alle 298 `asian`-Trials handeln im RTH. Engine-fähig wäre es sofort (`asian` mit `rs` 09:30-15:55 und `tr` über Nacht), **E8 verbietet das Halten** → Live-Buch-Merker, kein Prop-Job, kein Skelett.
- **W33 · Wochentags-Struktur** (TN-09, 21 Trials, 0 Survivors) bleibt als Kontrollachse stehen, nicht als eigenes Bein — der Wochentag ist der klassische Scheinfilter (AR-04).

---

## Reihenfolge nach Buch-Chance (✏️✏️ nach `ein-weg`, 17.09.2026)

**Enqueued und laufen auf der Box (17.09.2026, 08:59):**
1. **SES-W16a** — `hypothesis_bank.py`, **216 Configs** (nach pipeline-auditor-Fixes B1-B3: `tm_base="window"` statt Default `"open"`, Schwellenleiter neu kalibriert, `tm_signal=["ret","er_ret"]`-Kontrastarm ergänzt — der ret-Arm ist eine echte Teilmenge des er_ret-Arms bei gleicher Schwelle, sauber genesteter Vergleich). Stärkste Story der Gruppe (strategy-auditor). `hyp_SESW16a_NQ` läuft seit 08:59 auf der Box.
2. **SES-W42a** — `hypothesis_bank.py`, **72 Configs** (nach pipeline-auditor-Fixes B4-B6: `tm_rvol_max=0.7` gestrichen — war strukturell tot, alle Zellen unter min_tpy —, `tm_stop_mult` von [0.5,0.8] auf [0.15,0.25] gesenkt — R lag sonst beim 4-10-fachen des Buch-Beins NQ_Momentum gegen den Trailing-DD-Käfig). Story hält mit Vorbehalt, drei Auflagen umgesetzt (Familie, Kontrast-Zelle, SZ-57-Link). `hyp_SESW42a_NQ` in der Queue, `pending`.

**Wichtig für die Auswertung (pipeline-auditor-Auflage):** beide Jobs enthalten jetzt ihren eigenen Kontrast-Arm als Basislinie (W16a: `tm_signal="ret"` = die bereits tote nackte Fortsetzung; W42a: `tm_rvol_max=None` = die bereits lebende ungefilterte Basis). `promote_next.py` kennt den Unterschied nicht — vor jeder Auto-Promotion prüfen, aus welchem Arm der beste Survivor kommt. Kontrast-Arm = Vergleichsobjekt, kein Kandidat.

**Engine-Regressionstest (17.09., nach der `hypothesis_bank.py`-Änderung):** sauber, alle 6 Referenz-Beine identisch, beide Kanarien (Look-ahead, Zufallssignal) sterben wie erwartet. Runner-Service `MaxLabDiscovery` danach neu gestartet (PID 2064, war seit 16.09. 19:34 mit veraltetem `sigcore.py`/`tsmom.py`/`maband.py`-Stand im Speicher gelaufen — pipeline-auditor-Befund B7).

**Nachtrag 17.09., 09:00-10:11 — beide Jobs erst gescheitert, dann neu:**
- **SES-W42a `premise_failed`** (09:00, echt, kein Konstruktionsfehler): beide Prämissen-Configs zu schwach — `tm_rvol_max=0.85` (Basis) IS expR 0.008 = 0,3pp, `tm_rvol_max=0.8` IS expR 0.003 = 0,1pp, beide unter der 1,0pp-Hürde. Der niedrigfrequente Arm des Mechanismus trägt auch nach den pipeline-auditor-Fixes nicht. **`premise_failed` ist kein Tot-Stempel** (Regel oben) — aber anders als bei W15/W18/W6 keine Konstruktionsfrage, sondern ein echtes Null-Ergebnis auf der gemessenen Achse. Noch nicht `verdict-auditor`-geprüft, ob das reicht für „tot" oder ob eine andere Cap-Region (z.B. 0,9 statt 0,8/0,85) den Mechanismus noch retten könnte.
- **SES-W16a `failed`** (transienter `PermissionError` beim Registry-Schreiben — zweiter Fall dieser Art heute nach `hyp_AW14c_NQ`, vermutlich durch die vielen parallel laufenden Agents dieser Session verursacht, kein Inhaltsproblem). Auf `pending` zurückgesetzt, rechnet erneut.

**Offen mit klarer Auflage, noch nicht gebaut:**
3. **SES-W6a** — Reparatur der bestehenden Zeile TN-03 (nicht neue ID), Why auf "Close-to-Open-Return" korrigieren, `prior='low'` + Prescan vor dem Grid — der Prescan ist der nächste konkrete Schritt, kein Text-Edit.

**Durchgefallen (ein-weg 17.09., kein H()-Eintrag):**
- **SES-W8a** — gegatete Seite am echten Bein (976 Trades) in der falschen Richtung gemessen, alle vier Schwellen negativ.
- **SES-W6b** — kein eigenes Why, ist ein Achsenwert (`tm_dir`) von SES-W6a, keine eigene ID.
- **SES-W18a** — Story sagt Gegenbewegung, ~10k bereits gemessene Trades im selben Fenster sagen Fortsetzung; zwei der drei Pflichtbeilagen existieren nicht in `controls.py`.
- **SES-W15a** (aus Nachtrag 1) — Weg teilgemessen, Ersatz-Slot schon einmal bespielt, kein neuer Winkel ohne den `tm_delta_src`-Fix.

Danach erst Modul-Spec C (Globex-Form, jetzt inkl. `gx_range`), weil sie fünf Wege auf einmal öffnet (W28/W30/W31/W32/W38) — bester Hebel je Codezeile in dieser Karte. Danach D (uhrzeitgleiches Fenster, W40/W41) und E (Segment-Level als Schiene, W47).

---

## Offene Research-Fragen

1. Konditioniert eine Primärquelle die Intraday-Momentum-Edge auf den **Overnight-Return** (nicht nur auf Vola/Volumen)? (W8)
2. ~~Netto-Edge 15:45-16:00~~ ✏️ ersetzt durch: Gibt es eine Quelle, die MOC-/Imbalanz-**Orderflow** (echtes Delta, nicht Preis) als Prädiktor der Schlussminuten belegt? Erst relevant, wenn der `tm_delta_src`-Bug gefixt ist. (W15)
3. Ist der Iwanaga/Sakemoto-Decay auf NQ-**Futures** messbar oder nur auf Kassa-Indizes? (W6)
4. Wie groß ist die unbedingte Aufwärtsquote des NQ-RTH-Segments 2016-2026 (die richtige Null für die Long-Seite)? (W6b)
5. Quantifiziert jemand den TWAP-/POV-Anteil am US-Mittagsvolumen? (W16)
6. Gibt es Zahlen zum europäischen Anteil am ES-/NQ-Volumen 09:30-11:30 ET? (W18)
7. Erlaubt E8 Positionen **innerhalb** der Globex-Nacht (Entry 19:00, Exit 03:00), oder greift die EOD-Zwangsschließung? (W20/W21/W43/W44/W45/W46 hängen daran)
8. 🆕 Belegt die Literatur die **Rückrichtung** von Lou/Polk/Skouras explizit (Intraday-Return sagt das folgende Overnight-Segment), oder nur die Vorwärtsrichtung? (W36/W37)
9. 🆕 Gibt es Zahlen zum **Nachhol-Verhalten** von POV-/VWAP-Algos bei Unterfüllung am Vormittag (Volumen-Profil-Literatur)? (W42)
10. 🆕 Ist die **Kompression→Expansion**-Beziehung auf Segment-Ebene (Nacht-Range, IB-Breite) in der Literatur getrennt von der Tages-Vola belegt? (W38/W39)
11. 🆕 Belegt jemand die **Mehrtages-Wiederholung** von Metaorders im gleichen Uhrzeit-Fenster (Metaorder-Dauer-Literatur)? (W40/W41)

---

## Dateien dieses Laufs

- Report: `C:\Users\maxlk\Projects\trading-data\engine\discovery\scout_reports\familien_session-momentum_260916.md` (Nachtrag 1 angehängt)
- Hypothesen-JSON: `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\familien_session-momentum_260916.json`
- Diese Karte (lebendes Register je Weg, `verdict-auditor` stempelt hier zurück)

## Verwandte Notizen

[[Momentum-Theorie (Futures)]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Strategie-Logbuch]] · [[Research-Cache]] · [[Discovery-Runner v2]] · [[Alpha-Suche]] · [[Strategie-Familien]] · [[VWAP-Offensive]] · [[Fibonacci Wege-Karte]] · [[Familien-Scout Agent]]
