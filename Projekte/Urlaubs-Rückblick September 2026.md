---
datum: 2026-09-21
tags: [projekt, trading, urlaub, rueckblick]
status: aktiv
zeitraum: 2026-09-04 bis 2026-09-19
---

# Urlaubs-Rückblick 04.09. bis 19.09.2026

Gesamtübersicht über alles, was in den zwei Urlaubswochen auf der Box passiert ist. Quellen: Daily Notes 07.09. bis 19.09., [[Strategie-Logbuch]] #146 bis #165, alle neuen Projekt- und Ressourcen-Notizen, CLAUDE.md-Umbau, `.claude/`-Änderungen, `tasks.json` von der Box (Stand 21.09.). Details stehen jeweils in den verlinkten Notizen, hier nur der Überblick. Erstellt am 21.09.2026 am PC, vor dem Heimweg-Sync (siehe ganz unten).

---

## 1. Kurzfassung in zehn Sätzen

1. Das Buch ist von 4 auf **3 Beine** geschrumpft: `NQ_VWAP-Pullback` ist am 18.09. raus (Logbuch #161), 50k-Passquote 82,8 % → **87,4 %**, 172 $ pro funded.
2. Max hat am 18.09. das **Ziel geändert**: nicht mehr Passquote je Eval, sondern **E[Zeit bis 50.000 $ Eigenkapital]** aus gebündelten Payouts. Die CLAUDE.md widerspricht dem an zwei Stellen noch.
3. Empfehlung des Quant-Teams dazu: **E8 150k mit k=2** statt 50k (robust), **FundedNext Flex 150k als zweite Firma** (größter Hebel, spart ~18 Monate), Größe k=3 bis 4 erst mit Live-Evidenz.
4. Live gab es zwei echte Betriebsvorfälle: RiskGuard lief auf drei Konten **ohne Bust-Schutz** (07. bis 09.09., AP138 gefixt) und alle 15 NT8-Instanzen handelten **seit 07.09. mit dem falschen Session-Template** ETH statt RTH (AP152, 14.09. gefixt, Schaden ein Trade, ~160 $ je Konto).
5. Forschung: alles Getestete ist **tot oder ohne Kandidat**. First-Bar-EMA-Trail (NQ/ES/YM/RTY), Fibonacci-Nachfolge, Rundzahlen (10/10 Zellen), VWAP-Offensive (5 Jobs), Way of Dumb, Gold/Crude-Klone (90 Jobs, 0 Survivors).
6. Die **Friedhof-Analyse** (17.09.) zeigt: keine der 1.971 je gerechneten Buch-Bewertungen ist von Null unterscheidbar, 87 % des Registers lief am falschen Pfad („neues Bein" statt Ersatz), und die alte Rausch-Schwelle war 6σ zu lasch.
7. Die Pipeline hat dadurch **fünf Messfehler** verloren: Prämissen-Leck, Seed- statt Trade-Rauschen, Sharpe-Inflation 2,5×, Tick-Raster-Artefakt im Placebo, Tages-ATR statt Bar-ATR. Alle gefixt, teils mit Šidák-Schwelle (~5,4 pp), die kein Bestandsbein je geschafft hätte.
8. Neue Daten: **NT8 liefert 10 Jahre 1m-Historie gratis** (AddOn `MaxBulkExport`, 684 Kontrakte, 13 Märkte), NQ-Buch damit trade-identisch zu Databento. Databento-Anmeldung scheiterte an der Karte.
9. Infrastruktur: **familien-scout** (neuer Agent) + Workflow `konzept-weg`, Agent-Reflex per Hook, 5 Skills (`/abschluss`, `/box`, `/briefing`, `/queue`, `/ticket`), Statusline, NSSM-Dienst für den Runner, CLAUDE.md von 479 auf 309 Zeilen gekürzt.
10. Tickets: AP137 bis AP200 angelegt oder bewegt, davon **AP190 mit einer Anweisung, die dem Ist-Stand widerspricht** (siehe Abschnitt 10).

---

## 2. Zeitstrahl

| Tag | Kern |
|---|---|
| **So 07.09.** | Box-Check aus dem Urlaub. Watchdog zählte Strategien falsch (Enabling minus Disabling, Dauer-Alarm trotz 15 aktiven Instanzen), gefixt. Drei aktive RiskGuards ohne gespeicherte Parameter, eine State-Datei für drei Konten, vier Karteileichen auf E8. E8-Stand 48.872 $, Puffer 880 $. Session lief AUF der Box und versuchte SSH auf sich selbst (AP124-Muster). |
| **Di 08.09.** | AP138 gebaut: konto-eigene Dateien + `maxlab_riskguard.cfg`. verdict-auditor fand vier echte Befunde (Emoji-Mojibake, Lade-Reihenfolge, fehlende Wertgrenzen mit `cushion/0`, Watchdog-Herzschlag). AP135 lag fertig da, hätte aber den Build gebrochen (falscher Property-Name). |
| **Mi 09.09.** | AP138 deployt (zwei Deploys). Echte Ursache: Session-Start hing an `IsFirstBarOfSession`, RiskGuard lief 07. bis 09.09. auf allen drei Konten ohne Bust-Check. AP139 Herzschlag je Konto, Globex-Woche in CT, 26 Gegenproben. „12 h toter Feed" beobachtet (war das Template, siehe 11.09.). Max vertagt AP145 (Auto-Restart-Flag seit 06.09. gesetzt). E8-Support bestätigt breite Instrumentenliste und Zwangsglättung 15:10 CT für alle Futures. Statusline gebaut. First-Bar-EMA-Trail auf NQ tot (#147). AP137: Prämissen-Leck gefixt, k 6 → 30, Seed-Bestätigungs-Gate live (#146). Fibonacci recherchiert, Placebo-Test der Literatur negativ. |
| **Do 10.09.** | Nacht-Stillstand 01:59 bis 14:03 zweimal bestätigt (#148). VWAP-Offensive angelegt (12 Familien, 7 Agents). Fibonacci-Nachfolge: Rundzahl-Bounce tot, Retracement-Tiefe tot (#149). Git-Worktrees abgelehnt, AP148 Git-Härtung angelegt. Edge-Mapper-Konzept (→ familien-scout). |
| **Fr 11.09.** | First-Bar auf ES/YM/RTY tot (#150). **Nacht-Ausfall ist das Chart-Template „US Equities ETH"** seit 07.09.: alle Beine starten 08:00 statt 09:30 ET. AP152 rot, Max deaktiviert VwapPB 515/516/517. familien-scout + `konzept-weg` gebaut (AP149). Fünf VWAP-Jobs eingereiht (360 Configs). Rundzahl-Durchbruch als Tick-Raster-Artefakt zurückgezogen (#151). Prescan-Härtung als Code. Agent-Reflex-Hooks + Nutzungs-Audit. |
| **Sa 12.09.** | Buch-Kennzahlen für externen Kontakt (Sharpe 1,81, PF 1,39). Track-Record- und CTA/NFA-Recherche. 1 NQ statt 1 MNQ: kein statistischer Grund, 50k $ Risikokapital wäre nötig. E8 bei 48.732,90 $ (2 %-Perzentil gegen MC). live-reconciler: Executions-Log zu 53 % Duplikate, Equity-Log ist die Wahrheit. Queue leer, Buch-Sync 6 Tage alt. |
| **Mo 14.09.** | AP152 umgesetzt (MNQ 12-26 + RTH, 15 Instanzen neu aktiviert). Watchdog-Patch: Bars-Check nur RTH, Template- und Kontrakt-Selbstcheck, 45 Gegenproben. AP153 (12 Punkte, Prescan-Vertrag, Register-Pending-Weg). Fünf VWAP-Jobs ausgewertet: 0 Kandidaten, aber **Bestandsbein VWAP-Pullback misst −4,7 pp** → AP158. MultiCharts endgültig keine Live-Option. AP155 (Live-Automatisierung, 3 Optionen) angelegt, E8 wegen API-Trading angefragt. |
| **Di 15.09.** | AP154 geschlossen (Nacht ohne Alarm). Erster Live-Abgleich Trade für Trade: alle Beine decken sich, aber NT8 flattet 15:55, Engine hielt bis 15:59 → `eod_flat_min=385` (#155). Rundzahlen alle 10 Zellen tot. Audit „warum feuern manche Strategien nie": kein Bug, aber `maxlab_executions.csv` verseucht, AsiaDir ohne `IgnoreAllErrors` → AP159. AP150 teils gebaut (#154), AP151 abgearbeitet, AP160 angelegt. Zehn parallele Box-Sessions. |
| **Mi 16.09.** | **E8 erlaubt schriftlich direkte Tradovate-API** (Eval + Funded, kein HFT > 300 Trades/Tag). AP161 deployt, AP176 geschlossen. NSSM-Dienst `MaxLabDiscovery`, pypbo-Gegenprobe (`overfit_crosscheck.py`, PBO-Konvention → AP179). Šidák-Schwelle (#156), `max_book_evals` 8 → 3. `atr` war Tages-ATR20 statt Bar-ATR14 (#157), AW-15 → AW-15b. ES/NQ-Divergenz-, Rundzahlen- und Session-Momentum-Karten. Plugins-Abschnitt in CLAUDE.md. AP177, AP178 (Rückkehr-Checkliste). |
| **Do 17.09.** | **Friedhof-Analyse** (#158, 16 Rohdateien, AP183). „+9,6 pp Ersatz" widerlegt sich selbst (R 30 $ statt 60 $, Lehre 166). **AP158 + AP162 sind eine Entscheidung** (Substitute, #159), `book_cells.json` seit 03.09. stale. Hebel-Rangliste: VWAP-PB raus +5,13 pp. Multi-Markt-Kontrolle #051 ist eine Scheinkontrolle (n_eff 1,14 Märkte). Max entscheidet 3 von 5 AP183-Punkten. AP190 legt „LastHour raus, VWAP bleibt" ab (Bauch-Entscheidung). Fibonacci-Leg-Arm gebaut (AC-06d), Session-Momentum-Jobs, XD12 ohne Look-ahead. |
| **Fr 18.09.** | Gold durchgerechnet: **die Tageszeit dekorreliert, nicht das Asset** (ρ 0,015 vs 0,615). **VWAP-Pullback raus, LastHour bleibt** (#161, θ je Bein 2023-26), 3-Bein-Buch 87,4 %. Tier 50k → 100k: kein Wechsel (#160). Orderflow-v2 als Gate: kein Effekt (#162). **ZIELÄNDERUNG** Max: Zeit bis Eigenkapital. Tempo-Optimierung: 150k + zweite Firma. „Der Käfig ist eine Sharpe-Maschine", Shrinkage 0,58, Tages-Gewinnstopp als Lead. Way of Dumb tot (#163), TWAP-Entscheidung (#164), Spec B Makro-Kontext gebaut. CAPS in `ap106_funded_sizing_lib.py` für 100k/150k korrigiert. |
| **Sa 19.09.** | Databento-Karte abgelehnt → **NT8-Export** (`MaxBulkExport`, 684 Kontrakte, 0 Fehler). NQ-Buch auf NT8-Daten trade-identisch. 90 Klon-Jobs GC/CL: **0 Survivors, 0 Kandidaten** (#165). AP194 bis AP200. Vault gepusht, Engine als Zip-Bundle (888 MB) mit Manifest auf der Box abgelegt. 12 NT8-Instanzen stehen seit 18.09. 18:08 auf Disabled. |

---

## 3. Live-Betrieb und Konten

**Kontostände / Puffer**
- E8 `E61803453048` (50k): 08.09. 48.872 $ (Puffer 880 $), 12.09. 48.732,90 $, 14.09. 48.757,10 $. Seit 25.08. ~ −557 $, 2 %-Perzentil gegen MC-Erwartung, nach AP107 noch kein Alarm.
- FundedNext FN1/FN2 (je 50k Flex, Konten 964331151 / 964331145): 50.000 $, nie gehandelt seit 02.09., Inaktivitätszähler läuft (30 Tage, Verfall Anfang Oktober ohne Trade). Regeln: 1.500 $ EOD-Trailing, kein Daily Loss, Target 2.500 $, 40 % Consistency (RiskGuard kennt sie nicht).

**Vorfälle (alle behoben, außer Markierung)**
- RiskGuard ohne Bust-Schutz 07. bis 09.09. auf drei Konten (Session-Start nie erreicht). AP138 + AP135 deployt 09.09., Telegram bestätigt.
- Chart-Template ETH statt RTH 07. bis 14.09. (AP152). Ein Trade Schaden (VwapPB 09.09., −160 $ je Konto). ~12 Fehlalarme je Nacht aus dem Zeitzonen-Lesefehler.
- Watchdog-Fehlalarm Strategie-Zählung (07.09.), fünfter Messfehler dieser Bauart.
- `maxlab_executions.csv` verseucht (Duplikate, Phantom-Fills, kein State-Guard) → AP144/AP159.
- **Offen:** `maxlab_acct_fills_*.csv` / `maxlab_orders_*.csv` schreiben seit 14.09. 21:55 nicht mehr (AP193). `maxlab_equity.csv` tot seit 05.08. RiskGuard schreibt alle ~4 h „Session-Start NACHGEHOLT". `nt8_autorestart_pause.flag` seit 06.09. (AP145). Karteileichen 487 bis 490 in der NT8-DB.
- **12 NT8-Instanzen stehen seit Fr 18.09. 18:08 Boxzeit auf Disabled.** Nach dem Neustart bewusst nichts aktivieren, außer Max will es.

**Live-Abgleich 14.09. (#155):** alle Beine trade-identisch bis auf 1 Tick Slippage. Systematisch: NT8 flattet 15:55, Engine hielt bis 15:59, jetzt `eod_flat_min=385`. Erster 15:55-Fill lag 17,5 Punkte unter Bar-Open (n=1, beobachten).

**E8-Fakten neu:** Instrumentenliste breit (Metalle, Energie, FX, Zinsen, Agrar, Krypto-Micros), gleiche Regeln Eval/Funded, **Zwangsglättung 15:10 CT für alle Futures**, keine News-Sperre, SI-Margin nur 2.000 $. Direkte Tradovate-API erlaubt. Payout-Caps 100k brutto 15.250 $, 150k 20.250 $ (Sekundärquellen). Details: [[E8-Support-Anfrage (Instrumente GC-CL + Micros)]].

---

## 4. Buch-Entscheidungen

| Was | Ergebnis | Quelle |
|---|---|---|
| **VWAP-Pullback raus** | 18.09. umgesetzt: `book_state.json` 3 Beine, NT8-Instanzen 515/516/517 entfernt, 50k 87,4 % / 172 $ pro funded. θ je Bein 2023-26: Momentum 1,43, LastHour 1,09, Asia-Dir 1,97, **VWAP-PB 0,69** (Buch 0,84). +5,13 ± 3,56 pp Vollhistorie, +11,5 pp 2023-26. | #161, AP158/AP162 erledigt |
| LastHour vs VWAP als Streichkandidat | Unterschied −0,04 pp bei sd 4,51 pp, prinzipiell nicht auflösbar. Wahl lief über Kriterien (Why von VWAP-PB strukturell invalidiert, θ). | #159 |
| Tier 50k → 100k | **Kein Wechsel** unter dem alten Ziel (100k-Ticket teurer als Gesamtkosten bis 50k-Pass). Unter dem neuen Ziel: **150k k=2 empfohlen.** | #160, DN 18.09. |
| Subset {Momentum, LastHour} 90,1 % | Kein Fund, dritter Aufguss desselben gekippten Sweep-Siegers (#106, #117). | #159 |
| Coast-Leg-Schalter | **Nein** (OOS −0,44 pp, Walk-forward −2,7 pp). | AP183 (4) |
| Slot-Tabelle #146 | **Ja**, Ersatz innerhalb derselben Familie erlaubt. | AP183 (2) |
| Live-Grade-Kriterium | **Ja**, ins Live-Buch wenn es das Live-Portfolio verbessert. | AP183 (3) |
| Stufe-2-Statistik-Design | Darf gebaut werden. | AP183 (5) |
| Backtest-Exit 15:55 | Umgesetzt für qbt-Beine und sigcore (Nachtest: Rauschen). | AP161 |
| `max_book_evals` 8 → 3 | Max' Entscheidung, Trade-off bleibt (Picks sortieren nach OOS-Sharpe). | #156 |

**Zieländerung (18.09.):** Zielfunktion = E[Zeit bis 50.000 $ Eigenkapital] aus gebündelten Payouts mehrerer Funded-Konten, Kaufrate „so viele wie rechnerisch optimal", Größe erst rechnen. Min-Size nicht mehr gesetzt. Nulldrift-Kontrolle (#106) bleibt Pflicht.

**Tempo-Rechnung dazu (Median Monate bis 50k):** heute E8 50k k=1 → 100 M. E8 150k k=2 → 79 M (in allen Kennzahlen besser). + FN Flex 150k k=3 → 46 M. Beide k=4 → 35 M, aber 9 % Erreichung / 23k $ Auslage im schwachen Regime. Zweite Firma spart 18,5 Monate. Faustregel `DD / (k·σ_Buch) ≥ 6` (FN Flex 50k fällt durch: 2,1). Mit Selektions-Shrinkage 0,58: SR 1,55 → 0,88, Median 126 Monate, P(Ziel in 5 J) 7 %. Relatives Verhältnis 2,2:1 für 150k hält über den ganzen Unsicherheitsbereich. Live nicht entscheidbar (20 Jahre Power), **Abbruchkriterium ist Pflicht**. Tages-Gewinnstopp: Top 1 % der Tage = 48,5 % des Ergebnisses, Kappung +24 % Slot-Rate (Lead, kein Ergebnis).

---

## 5. Forschung: Ergebnisse #146 bis #165

| # | Thema | Urteil |
|---|---|---|
| 146 | AP137: Prämissen-Leck (19 % Rechenzeit ins Leere), k 6 → 30, Rausch-Schwelle maß Seed- statt Trade-Streuung (0,24 vs 2,6 bis 3,0 pp) | Gate `book_marginal_confirm()` gebaut, Kandidatenzahl geht auf ~0 |
| 147 | First-Bar-EMA-Trail NQ (2880 Configs, v1 bis v4) | **tot**, EMA ist Dekoration, 82,8 % gleiche Richtung wie Momentum |
| 148 | Nächtlicher 12h-Preisstillstand | war das Chart-Template (#152) |
| 149 | Fibonacci-Nachfolge: Rundzahl-Bounce (530k Events), Retracement-Tiefe (477k) | **beide tot**, Durchbruch-Fund später zurückgezogen |
| 150 | First-Bar auf ES/YM/RTY (9.288 Trials) | **tot auf allen drei** |
| 151 | Prescan-Härtung als Code; Rundzahl-Durchbruch war Tick-Raster-Artefakt (+5,79 → +0,32 pp) | zurückgezogen, #138 AB-14 kein Urteil |
| 152 | ETH- statt RTH-Template | Lehre 152 |
| 153 | Fünf VWAP-Jobs: AW-14b nicht auswertbar, AW-15 tot, AC-06b kein Kandidat, AC-06c Konstant-Arm raus, exit2 tot | **VWAP-Pullback −4,7 pp** als Nebenfund |
| 154 | AP150: ATR-Normierung, Level-Export, Sigma-Hygiene (sd bei Bar 6 nur 28 %) | gebaut |
| 155 | Erster Live-Abgleich, 15:55 vs 15:59 | `eod_flat_min=385` |
| 156 | Šidák-Korrektur der Buch-Marginal-Schwelle (11 bis 22 % FPR vorher), B 40 → 200 | effektiv ~5,4 bis 7,4 pp, 0 von 600 Dateien hätten es geschafft |
| 157 | `atr` las Tages-ATR20 statt Bar-ATR14 → AW-14c-Basis 3 Trades in 10 Jahren | `atr_bar` neu, AW-15b, 7 weitere Zeilen ungeprüft |
| 158 | Friedhof-Analyse (287 Grabsteine, 63.727 Trials, 1.971 Bewertungen) | keine Bewertung von Null unterscheidbar, 13 Prozessfehler, Lehren 158 bis 162 + 166 |
| 159 | AP158/AP162 sind eine Entscheidung; `book_cells.json` stale seit 03.09. | Lehren 163 bis 165 |
| 160 | Tier 50k → 100k | kein Wechsel |
| 161 | VWAP-Pullback raus | umgesetzt, Lehre 167 |
| 162 | Orderflow-v2 als Gate auf Bestandsbeine (gepoolt r 0,042, p 0,126) | nicht nachweisbar |
| 163 | Way of Dumb (d) Monatsende; Spec B Makro-Kontext gebaut | **tot**, strukturell unterpowert (MDE-Gate jetzt Code, Lehre 168) |
| 164 | TWAP-Modul | ja, aber nur Ereignis-Zeilen; TD-Block nein („echt, aber zu klein") |
| 165 | Neue Märkte GC/CL, 90 Klon-Jobs | 0 Survivors, MGC-Kosten 3,3× / MCL 6,1× MNQ, CL-Ergebnis falsch-negativ-anfällig (Prämissen-Sperre) |

**Wege-Karten (familien-scout):** [[Fibonacci Wege-Karte]] (26 Wege, 3 Skelette, AC-06d läuft), [[Rundzahlen Wege-Karte]] (33 Wege, 13 final tot, nur W19/W26 offen), [[Session Momentum Wege-Karte]] (47 Wege, SES-W16a gebaut, SES-W42a premise_failed), [[ES-NQ-Divergenz Wege-Karte]] (30 Wege, hyp_XD12_NQ eingereiht, Spec A nicht gebaut).

**Laufende / eingereihte Jobs (Stand 19.09.):** AC-06d NQ/ES/YM/RTY, SES-W16a, hyp_XD12_NQ, AW-14c/AW-15b (Ergebnisse teils ohne Stempel), vt01/vt01b (alpha-scout). Queue nach dem NM-Batch wieder leer, `queue_empty` seit 14.09. (AP194).

**Recherche-Cache neu:** E8-API, Payout-Caps, Fibonacci (ESWA 2022 negativ), Rundzahl-Clustering (peer-reviewed für Index-Futures, aber kein Orderdaten-Beleg), VWAP/TWAP-Literatur, Gao/Han/Li/Zhou aus der Primärquelle (R² 1,6 %), SMT-Divergenz (kein Paper), Databento-Kosten, CME-Kontraktspezifikationen, CTA/NFA-Pflichten, MultiCharts, GitHub-Repos (pypbo, NSSM), Track-Record-Tools. Details: [[Research-Cache]].

---

## 6. Pipeline und Engine (was jetzt anders rechnet)

- **Gates:** Prämissen-Gate mit Edge-Schwelle 1,0 pp auch in Stufe 0; Seed-Bestätigungs-Gate mit gepaartem Block-Bootstrap; Šidák-Schwelle (α 0,10), Zähler `point`, sd-Boden 3,0 pp, B=200; vierter Verdict-Zustand „grenzwertig".
- **Kontrollen:** `random_level_shift`/`random_grid_phase` verlangen `tick`; `mb_vwap_anchor=rand_time`; `ctl_placebo_arm(grid_share)`; `null_ref` Pflichtfeld je Bank-Job; `promote_next` promotet `prior=low` ohne Prescan-Vertrag und `null_ref none:*` nie automatisch.
- **Register:** Register-Pending-Weg (`discovery/registry_pending/`, append-only); Prescans zählen als Trials; 15:59-Konvention markiert (1.494 Alt-Trials); Register n_total 39.071 → **65.035**.
- **Neue Module/Funktionen:** `discovery/prescan_controls.py`, `sigcore.matched_base_selftest()`, `sigcore.hazard_null_fit/expect`, `sigcore.ForwardVariance`, `sigcore.xref_signal()/xref_confirm()` (ES-Bestätigung, mit Look-ahead-Assert), `sigcore._spx_daily_context()` (FRED DGS2/DGS10/DTWEXBGS), `maband._leg_stop` (`tm_stop_mode="leg"`), `mb_vwap_dnorm="sigma"|"atr"|"atr_bar"`, `tm_exit="level"`, `tm_vwap_side_min_atr`, `ctl_dnorm`, `overfit.bucket_mde()/feasibility_gate()`, `eval_plan.scale_leg()/theta_of()/theta_gate()`, `discovery_lib.theta_prefilter()` (Schattenmodus verdrahtet), `discovery/premise_friedhof.py`, `engine/overfit_crosscheck.py` (pypbo, eigene `.venv-analysis`).
- **Fixes:** `sharpe_ann_daily` über Börsentage (war 2,5× aufgebläht); `noise_pp` 5 statt 3 Seeds; Phantom-Trail-Duplikate; unbekannter `tm_stop_mode` wirft `ValueError`; `eod_flat_min` aus `p` gelesen; `book_cells.json` gelöscht (stale); `book_noise.json` repariert; `hypothesis_bank.py` Import-Fehler nach VWAP-Streichung (5 Zeilen auf hold); CAPS 100k/150k in `ap106_funded_sizing_lib.py` (waren +34 % / +52 % zu hoch); `qbt.py` neue Symbole + `bars_file()`-Fallback auf `exported_data_nt8`; Klon-Block NM mit Vola-Skalierung.
- **Hypothesen-Bank:** neue Zeilen AC-06b/c/d, AW-14b/c, AW-15b, TN-03/TN-04-Hinweise, 9 Zeilen auf `atr` umgestellt (7 davon ungeprüft auf die atr_bar-Falle), Block NM (90 Klon-Jobs). Toter Friedhof: Rundzahl-Bounce, Retracement-Tiefe, AW-08 redundant, AW-15 widerlegt.
- **Runner:** läuft seit 16.09. als **NSSM-Dienst `MaxLabDiscovery`** (LocalSystem, BELOW_NORMAL, Neustart über `start_runner.ps1`, nie mehr per WMI). Letzter Stand 19.09.: PID 444.
- **Golden Master:** neue Kanarien `KANARIE_flat1555`; `KANARIE_r_only_artifact` hat usd-Zahlen um Faktor 30 zu hoch (klären).

Details: [[Discovery-Runner v2]], [[Buch-Workflow]], [[Strategy Developer]].

---

## 7. Neue Märkte und Daten

- **NT8-Export** (`MaxBulkExport`, 19.09.): ES/NQ/YM/RTY/GC/CL/6E/6B/ZN/ZB/ZS/ZW/FDAX, je ~3 Mio 1m-Bars ab 12/2015, UTC, Bar-Ende, 0 kaputte Bars. GC/CL enden am 25.07.2026, 6E/6B am 14.09. (Nachladen AP196). Tick-Historie leer. Ordner `exported_data_nt8`, Databento-Dateien unberührt.
- **Vergleich NT8 vs Databento:** 95,5 bis 97,9 % Bars identisch, Tagesrendite-Korrelation 0,9994+, Versatz 0. NQ-Buch trade-identisch (Korr. 1,000). **Aber: Quellenwechsel bewegt die 25k-Passquote um 1,8 pp bei 1,5-pp-Entscheidungsschwelle** (AP199).
- **Kosten je Käfig-Kontrakt** (2 Ticks je Seite + Kommission, % der Tagesrange): MNQ 0,63 % (×1), MGC 2,07 % (×3,3), MCL 3,82 % (×6,1), 6E ×10, 6B ×15,6, ZS ×13,6, ZW ×16,5, ZN ×34. Hürde wächst mit σ_c^1,63, klein schlägt groß im Käfig.
- **Gold:** einziges käfigtaugliches Fremdinstrument (σ_c 76, Tagesrange MGC 251 $), ρ_Bein ≈ 0,014, Hürde ~1.160 $/Jahr, Tail-Kopplung unter drei von vier Bestandsbeinen. ρ_Asset epochen-instabil (2026: +0,305). Liquidestes Fenster 8:20 bis 11:00 ET, nicht 9:30 (AP197 Session-Fenster je Markt).
- **Kernbefund 18.09.:** gleicher Markt/andere Tageszeit ρ 0,015, anderer Markt/gleiche Tageszeit ρ 0,615. **Die Tageszeit dekorreliert, nicht das Asset.**
- **Klon-Lauf GC/CL (#165):** 90 Jobs, 0 Survivors. GC: 4 Near-Misses scheitern an Frequenz und Tail-Konzentration (Gold-Boom 10/2025 bis 03/2026). CL: alle 41 an der Prämisse, aber 8 Jobs starben an derselben Basis-Config, Filter-/Event-Thesen nie gerechnet (AP195). Nicht tot: Gold/Öl insgesamt, alles außerhalb RTH, 6E/6B/ZS/ZW.
- **Databento:** Anmeldung scheiterte (Karte, Curaçao-IP). Kosten wären ~0,10 $ je Symbol für 10 Jahre 1m. AP143 offen, teils obsolet.
- Plan-Notiz: [[Neue Märkte (NT8-Daten) Plan]].

---

## 8. Infrastruktur: Agents, Hooks, Skills, Tools

**Agents**
- Neu: **`familien-scout`** (opus), zerlegt ein Konzept in alle Preis-Wege, schreibt Report + Hypothesen-JSON + Vault-Karte. Workflow **`konzept-weg`** (Scout → verdict-auditor Vollständigkeit → research-scout ein Call → `ein-weg`). Notiz: [[Familien-Scout Agent]]. Hub-Roster fehlt noch (AP149).
- Modell-Wechsel opus → **sonnet** (17.09.): `alpha-scout`, `pipeline-auditor`, `logbook-distiller`, `retro-agent`, `variant-scout`. Auf opus bleiben: `verdict-auditor`, `strategy-auditor`, `familien-scout`, beide Quants.
- `verdict-auditor` prüft Wege-Karten auf Vollständigkeit; Quants rechnen vor jeder Bucketing-Hypothese `bucket_mde()`.
- Agent-Nutzungs-Audit 11.09. (23 Sessions): am häufigsten ausgelassen research-scout (direkte WebSearch), session-guard, design-guard. Notiz: [[Agent-Nutzungs-Audit 2026-09-11]].

**Hooks** (Details [[Hooks-Referenz]])
- **UTF-8-Fix 09.09.:** vorher cp1252, jeder Umlaut ließ `read_input()` still `{}` zurückgeben, **keiner der Wächter griff**. Jetzt UTF-8 hart.
- Neu `on_prompt.py` (UserPromptSubmit) + `agent_triggers.py` (15 Regeln, eine Quelle für Prompt-Hook, Stop-Hook, Audit).
- `on_stop.py` blockt jetzt dreifach: ungepushtes Buch, geänderte Dateien ohne Daily-Note-Eintrag, Trigger ohne Agent-Aufruf. Anti-Endlosschleife per Session-Marker (Vorfall 16.09.).
- `guard_bash.py`: Heredoc-Inhalt und Such-Befehle lösen keine Blocks mehr aus, `--dry` freigegeben.
- `after_change.py`: Prescan-Vertrag-Hinweis. `session_start.py`: Vault-Kurzbriefing + Cross-Session-Überblick (nur dasselbe Gerät).
- `session_conflicts.py`: Titel-Filter-Bug gefixt („(ohne Titel)").

**Skills (5 neu):** `/abschluss` (Session-Ende-Ritual), `/box` (Ampel via box-ops), `/briefing` (Kontext nur lesen), `/queue` (Discovery-Stand mit Buch-Lücke), `/ticket` (tasks.json lesen, Box = Wahrheit).

**Sonstiges:** `.claude/statusline.py` (Modell, Kontext, 5h/7d-Fenster, Kosten; nur im Terminal, nicht in der Desktop-App), `agent_usage_audit.py`, Plugins `pyright-lsp`, `claude-md-management`, `claude-code-setup` in `settings.json`, CLAUDE.md-Abschnitt „Plugins & neue Werkzeuge immer mitnutzen" (16.09.).

**CLAUDE.md-Umbau:** 479 → 309 Zeilen. Urlaubs- und Queue-Abschnitt raus, Buch-Workflow / Strategy Developer / Discovery-Runner / Hooks in eigene Notizen ausgelagert, Meta-Agents als eine Tabelle, neue Regeln Daily-Note-Bestätigung, MCP-Kontextkosten, NSSM statt WMI, `tasks.json` zweiseitig. `Ticket-Epics.md` ins Archiv.

---

## 9. Neue Vault-Notizen (seit 07.09.)

| Notiz | Inhalt |
|---|---|
| [[Entscheidungen nach dem Urlaub]] | Stand 16.09., kennt nur AP155. Überholt, siehe Abschnitt 10 hier. |
| [[VWAP-Offensive]] | 12 Familien, 5 Jobs, 0 Kandidaten, Nebenfund VWAP-PB −4,7 pp |
| [[Friedhof-Analyse (17.09.2026)]] + Ordner `Ressourcen/Friedhof-Analyse 2026-09-17/` (18 Rohdateien) | Vollanalyse, Kandidaten-Stempel A bis G, 13 Prozessfehler |
| [[Neue Märkte (NT8-Daten) Plan]] | Export, Steckbriefe, Kosten, GC/CL-Ergebnis, Review F1 bis F8 |
| [[ES-NQ-Divergenz Wege-Karte]], [[Fibonacci Wege-Karte]], [[Rundzahlen Wege-Karte]], [[Session Momentum Wege-Karte]] | familien-scout-Karten |
| [[Familien-Scout Agent]] | Agent-Konzept und Bau |
| [[Buch-Workflow]], [[Strategy Developer]] | aus der CLAUDE.md ausgelagert |
| [[Hooks-Referenz]] | volle Hook-Tabelle |
| [[Agent-Nutzungs-Audit 2026-09-11]] | Audit-Ergebnis |
| [[E8-Support-Anfrage (Instrumente GC-CL + Micros)]] | E8-Antwort, Instrumentenliste, Margins |
| [[Token Tracker App]] (Update) | Statusline lebt doch |
| [[Archiv/Ticket-Epics]] | archiviert 15.09. |

---

## 10. Tickets AP137 bis AP200 (Box-Stand 21.09.)

**⚠️ Widerspruch, zuerst klären:** **AP190** (rot, offen, 17.09.) sagt „NQ_LastHour_v3 raus, NQ_VWAP-Pullback bleibt" (Bauch-Entscheidung Max vom 17.09.). Am **18.09.** wurde nach den θ-Zahlen das **Gegenteil** umgesetzt (VWAP-PB raus, LastHour bleibt, #161), AP158/AP162 sind erledigt. AP190 muss geschlossen oder umgeschrieben werden, sonst führt eine spätere Session „LastHour raus" auf dem 3-Bein-Buch aus. Dazu passt: `book_state_next.json` hat VWAP-Pullback noch drin (Stand 03.09.), eine Übernahme des Next-Buchs brächte das Bein zurück.

| Ticket | Prio | Status | Kurz |
|---|---|---|---|
| AP137 | gelb | offen | Null-Schalter Buch-Modi + Kalender/DIX-Gates deployen. **Engpass:** ohne das promotet die Box Ersatz-Jobs auf Buch-Beinen nie mehr. Laptop-Patches nicht auf der Box. |
| AP138 | orange | erledigt | RiskGuard konto-eigene Dateien + cfg |
| AP139 | orange | erledigt | Herzschlag Globex-Woche je Konto |
| AP140 | gelb | teilweise | Gold als erster Nicht-Index-Markt |
| AP141 | orange | beantwortet | E8-Instrumente |
| AP142 | gelb | offen | Datenexport neue Symbole (durch NT8 teils obsolet) |
| AP143 | grün | offen | Databento-Account (Karte abgelehnt) |
| AP144 | gelb | offen | `OnExecutionUpdate` ohne Realtime-Filter (Deploy-Paket) |
| AP145 | orange | offen | Herzschlag Soll-Ist + darf Feed-Stillstand NT8 neu starten? (von Max vertagt, Auto-Restart-Flag seit 06.09.) |
| AP146 | gelb | offen | Dollar-Gates je Min-Size, n_trials aus Register, Kosten-Kanarie |
| AP147 | gelb | offen | VWAP-Offensive (Phase 5 ohne Kandidat) |
| AP148 | gelb | offen | Git-Härtung, am PC (master/main, Engine als Repo, Entscheidung Max) |
| AP149 | grün | offen | familien-scout in Hub-Roster |
| AP150 | gelb | teilweise | maband-VWAP-Erweiterungen (P4 Globex-Anker zurückgestellt) |
| AP151 | gelb | erledigt | Pipeline-Hygiene VWAP |
| AP152 | rot | erledigt | Template RTH + Roll MNQ 12-26 |
| AP153 | orange | erledigt | Prescan-Härtung Teil 2 |
| AP154 | gelb | erledigt | AP152-Fix bestätigt |
| AP155 | gelb | offen | **Live-Automatisierung:** 1 `MaxBookHost` (Claude-Favorit) / 2 MultiCharts (nein) / 3 Tradovate-API direkt (E8 erlaubt) |
| AP156 | gelb | offen | Pipeline-Härtung aus CVD-Audit |
| AP157 | gelb | teilweise | Queue-Nachschub (Blocker A/B deployt) |
| AP158 | orange | erledigt | VWAP-Pullback neu vermessen → raus |
| AP159 | gelb | offen | NT8-Beine härten (State-Guard, AsiaDir IgnoreAllErrors, Zeit statt Bar-Zähler), ein Deploy mit AP144 + AP171 |
| AP160 | gelb | erledigt | Lehre 154 Nachlauf (`atr`-Lint, `tm_vwap_side` Phantom-Filter) |
| AP161 | gelb | offen | Punkt 1 deployt; Rest: PC-Caches, Edge-Ref, Register-Markierung, 15:55-Fill beobachten |
| AP162 | gelb | erledigt | LastHour raus? → bleibt |
| AP163 | gelb | (leer) | Pipeline-Fixes aus Audit #139 |
| AP165 | gelb | offen | ORB/Scalp: zwei Scalps feuern dasselbe Signal |
| AP167 bis AP173 | gelb | offen | Altbestand (macro_post, FA-01, ES-Alpha-Woche, FN1 ins Buch, EOD-Telegram-Report, Noel-T-Härtung, Familien-Sperre) |
| AP175 | orange | erledigt | 12h-Preisstillstand |
| AP176 | gelb | erledigt | Sharpe-Drift Golden Master (kein Bug) |
| AP177 | orange | offen | Windows-Updates Box |
| AP178 | orange | offen | **Rückkehr-Checkliste** mit Reihenfolge |
| AP179 | gelb | offen | PBO-Konvention `<= 0` entscheiden, NSSM/Box-Skripte auf PC |
| AP180 | gelb | offen | `add_job()` validiert nicht gegen GATES_HARD |
| AP181 | grün | offen | Premise-Tod nach Grund klassifizieren |
| AP182 | gelb | offen | ES-NQ-Vorabmessung ins Register |
| AP183 | orange | offen | Friedhof: 5 Entscheidungen (1 offen: Referenzbuch, faktisch durch #161 erledigt) + 12 Pipeline-Fixes |
| AP184 | gelb | offen | `book_cells.json` Engine-Fingerprint |
| AP185 | orange | offen | **PRIO:** Buch-Marginals nicht additiv, `block_marginal()` + Ein-Swap-Sperre in `promote_next.py` |
| AP186 | gelb | offen | Bestandsdurchlauf unter korrigiertem Rauschmaß |
| AP187 | gelb | offen | Korrelationsanzeige zeigt nur Mittelwert |
| AP188 | gelb | offen | Out-of-Bag-Pflichtspalte für Subset-Scans |
| AP189 | gelb | offen | Pipeline-Fixes aus AC-06d-Audit |
| **AP190** | **rot** | **offen** | **„LastHour raus, VWAP bleibt" , widerspricht #161, siehe oben** |
| AP191 | grün | offen | Buch-Fingerprint in Konsole |
| AP192 | grün | offen | Asia-Dir tmin_entry andere Uhr (folgenlos) |
| AP193 | gelb | offen | `acct_fills`/`orders`-CSV schreiben seit 14.09. nicht mehr |
| AP194 | orange | offen | Job-Generator: Queue leer seit 14.09. (10× queue_empty) |
| AP195 | orange | offen | CL-Nachtest braucht Gate-Lockerung (Entscheidung Max, ~1 Box-Stunde) |
| AP196 | gelb | offen | NT8-Historie nachladen (GC 12-26, CL 09-26 ff., 6E/6B 12-26), nur außerhalb der Handelszeit |
| AP197 | gelb | offen | Session-Fenster je Markt + sigcore 390-Minuten-Annahme |
| AP198 | gelb | offen | Überthema Neue Märkte |
| AP199 | gelb | offen | Datenquelle NT8 vs Databento (1,8 pp Quellenrauschen) |
| AP200 | grün | offen | Aufräumen (_staging, Backups, Export-Ordner, Heimweg-Zip) |

Weitere offene Altlasten aus AP178: AP86 („Remember me"-Haken, nur Max), AP133 (Telegram je Konto, Optionen A/B/C), AP134 (NT8-UI-Automation), AP136 (Bash-Rechte Box), AP124 (Self-SCP-Bug in `push_next()`), AP127 (Equity-Log tot seit 05.08.), AP113 (PowerHour-Kalender endet 10.12.2026), AP130/AP131/AP132.

---

## 11. Offene Entscheidungen für Max (gebündelt)

**A. Strategisch**
1. Zieländerung offiziell machen: CLAUDE.md an zwei Stellen ändern („Optimiert wird NUR auf hohe Passchance", „nicht mehr P(funded) pro Zeit").
2. Tier E8 50k → 150k bei k=2 (empfohlen, robust).
3. FundedNext Flex 150k als zweite Firma (empfohlen, größter Hebel). Vorher klären: Median erster Payout 20 Tage an den eigenen FN-Konten verifizieren (FundedNext-MCP muss neu autorisiert werden, AUTH_EXPIRED), 750k-Gesamtallokation, „je Haushalt"-Regel, Gratis-Challenge nach 5. Payout.
4. Positionsgröße k=3/4: nicht ohne Live-Evidenz.
5. Abbruchkriterium festlegen (Auslage-Obergrenze 5.500 bis 10.100 $, Slot-Raten-Monitoring).
6. Kommt der größere Teil der 50k aus Payouts oder aus dem Gehalt? (5 Prop-Konten ≈ 730 $/Monat geschrumpft)
7. AP155 Plattform: Option 1 / 3.
8. Beweislast-Richtung für Bein-Streichungen (Haus-Gate ist für „rein" gebaut).
9. Tages-Gewinnstopp als Engine-Variante rechnen lassen?

**B. Sofort operativ**
- AP190 schließen/umschreiben und `book_state_next.json` auf das 3-Bein-Buch bringen.
- 12 NT8-Instanzen wieder aktivieren? (stehen seit 18.09. auf Disabled)
- AP193 (Fills-CSV tot seit 14.09.), AP145 (Auto-Restart-Flag), AP133, AP86, Deploy-Paket AP159+AP144+AP171, AP177 Windows-Updates.

**C. Pipeline**
- AP137 Null-Schalter-Deploy (Engpass). Laptop-Patches auf die Box oder neu bauen?
- `theta_gate()` scharf verdrahten? (Schattenmodus belegt: es hätte Momentum und LastHour aussortiert, also nein, so nicht)
- `max_book_evals` 8 → 3 Trade-off, PBO-Konvention (AP179), KANARIE-usd Faktor 30, Käfig-Kanarie gegen `evaluate_v2` bauen.
- 7 Bank-Zeilen auf atr_bar prüfen, AW-14c neu einreihen, AP185 vor der nächsten Auto-Promotion.
- CL-Nachtest ja/nein (AP195), 6E/6B/ZS/ZW freigeben oder nicht, ES/NQ-Lesart (SMT/Bestätigung), Fibonacci-Tiefen-Achse, W19-Hazard-Prescan.
- Sechs Logbuch-Einträge sind noch nicht geschrieben (Käfig nie nachbauen; Signifikanz validiert nie das Modell; θ keine suffiziente Statistik; Faustregel DD/(k·σ) ≥ 6; Käfig ist Sharpe-Maschine; Shrinkage 0,58 Obergrenze).

---

## 12. Am PC nachziehen (Heimweg)

Der Sync-Prompt von der Box liegt bei Max (Schritte A bis G). Zusätzlich zu dem, was dort steht:

1. Vault: `git pull` (22 Commits, lokale Änderungen an `.obsidian/*` und `Bereiche/Eval-Passing.md` vorher zeigen). Diese Notiz hier ist neu und kollidiert nicht.
2. Engine: Zip (888 MB, SHA256 `66FE…F9170`) + Manifest per scp, in `heimweg\box` entpacken, gegen PC-Stand abgleichen, Box ist Wahrheit für `book_state*.json`, `portfolio*.json`, `tasks.json`, Register/Queue. Discovery-State danach lieber `inbox_tool.py --pull`.
3. `hub_config.json`: 5 Agents auf sonnet, `familien-scout` eintragen, Hooks/Skills/Workflow `konzept-weg` in `mock_loops`, dann `.\hot_reload.ps1`.
4. Statusline: `~/.claude/statusline.py` + `statusLine`-Block in `~/.claude/settings.json` (Forward Slashes, nur Terminal).
5. Hooks greifen erst nach Session-Neustart (`UserPromptSubmit` neu). Plugins `pyright-lsp`, `claude-md-management`, `claude-code-setup` prüfen.
6. Laptop-Patches (AP137 Null-Schalter, seit 07.09. nur auf dem Laptop) nicht vergessen.
7. Danach: Daily Note 21.09. und Entscheidung, ob das Heimweg-Zip auf der Box gelöscht werden kann (AP200).
