---
tags: [trading, alpha-suche, es, plan]
created: 2026-08-27
deadline: 2026-09-06
status: aktiv
---

# ES-Alpha-Woche (KW36)

**Ziel:** Innerhalb einer Woche systematisch ES-Alpha fürs Portfolio erschließen — Erfolgskriterium ist ausschließlich der [[Strategie-Logbuch|v2-Buch-Beitrag]] (Passquote je Eval / $ pro funded), nicht Solo-Schönheit. Ausführung durch eine **sonnet**-Session + Box, nicht durch Fable. Analysebasis: Register (7.379 Trials), 106 Report-Metas, ideas.json, Logbuch #001–#132 (ausgewertet 27.08.2026).

---

## 1. Warum NQ funktioniert und ES nicht (die Analyse)

Die Zahlen (Register, Stand 27.08.): NQ **1.504 Survivors aus 5.406 Trials (28 %)**, ES **34 aus 889 (3,8 %)**, 0 ES-Kandidaten in der Inbox, 0 Promotionen. Das ist kein Pech, sondern hat vier klare Gründe:

1. **Die Kostenmechanik ist invertiert (#132, #112).** MES zahlt pro Bewegungseinheit das **3,6-fache** von MNQ (Round-Trip 0,90 % der Median-Tagesrange vs. 0,25 %; im 2-Tick-Stress 1,54 %). In R gerechnet: ES-Kosten ≈ 0,013–0,018R pro Trade vs. NQ 0,003–0,005R. **Auf ES sind die Kosten größer als die meisten Rohsignale.** Deshalb stirbt ES primär am edge-Gate (61 % der Trials) und an Top-5-Konzentration (70 %) — nicht erst am Kosten-Stress-Gate: die kleine Edge ist nach Kosten schlicht weg.
2. **NQ ist ein Continuation-Markt, ES dreht.** Breakouts laufen auf NQ durch, auf ES kippen sie (#050: ORB-Scalp ES PF 0,18–0,57; #007, #052, #183/184). Konsequenz im Register: **alle** Preis-Momentum-Modi sind auf ES komplett leer trotz NQ-Erfolg — tsmom 0/354 (NQ: 506 Survivors), last_hour 0/56, maband 0/42, gap 0/27, asian 0/28, orb 0/22, vix_bias 0/40.
3. **Direkte NQ/ES-Paare zeigen: ES braucht überall breitere Stops und strengere Filter und liefert trotzdem nur ⅓–½ der Edge.** VIX-Spike-Rev: NQ A/PF 1,51 vs. ES C/PF 1,22 (Stop 0,75→1,0σ). MOMSEL: NQ A/PF 1,30 bei 83 Trades/Jahr vs. ES C/PF 1,09 bei 27 (ER-Schwelle 0,3→0,5). VOLBRK: NQ C/1,23 vs. ES D/1,06 bei 3,5× mehr Trades. Die Edge ist auf ES „verdünnt".
4. **Was auf ES trotzdem funktioniert, sind strukturelle Zwangs-Flows.** `cal` hat auf ES 24/42 Survivors (57 % — identisch stark wie NQ), `rv` 8/15. OPEXMOM_ES (PF 1,61) ≈ OPEXMOM_NQ (1,64). Und das **beste Event-Bein im ganzen System ist ein ES-Bein**: `EVENT_ES_primary` (FOMC-Post + OpEx, Grade A, PF 1,89, Sharpe 3,25, OOS-Edge +25,3 %) — liegt ungenutzt in der Live-Bank, weil der Auto-Fit es damals gegen das ALTE Buch als zu frequenzschwach ablehnte.

**Die Leitidee in einem Satz:** ES ist kein schlechterer NQ, sondern der am engsten arbitrierte und (relativ zur Bewegung) teuerste der vier Index-Futures — Preis-Momentum wird dort wegarbitriert und von Kosten gefressen; übrig bleiben **Termin-Flows mit großem $/Trade** (jemand MUSS zu einem Datum handeln: OpEx, FOMC, CPI/NFP, Rebalancing), **Überdehnungs-Reversion an Tagen mit großer Range** (wo die Kostenquote klein wird) und **ES als Informationsquelle statt Ausführungsinstrument**.

Dazu passt der Portfolio-Blick: Das Next-Buch ist nach dem RTY-Gap-fade-Exit **4/4 NQ**. Ein ES-Klon einer NQ-Mechanik brächte eh keine Diversifikation (Index-Korrelation ~0,9, Friedhof-Eintrag „Cross-Instrument"). Wertvoll ist nur, was einen **anderen Mechanismus** trägt.

---

## 2. Die vier Angriffs-Lanes

| Lane | Mechanismus-Klasse | Warum auf ES | Status |
|---|---|---|---|
| **A — Event/Kalender** | Zwangs-Flows mit Termin (OpEx, FOMC, CPI/NFP, Month-/Quarter-End, Quad-Witching, Charm/Wexp) | Einzige Klasse mit bewiesenen ES-Survivors; großer $/Trade schlägt die Kostenhürde; Gegenpartei muss handeln (Gamma-Hedging, Rebalancing) | `cal`-Modus existiert; CPI/NFP-Modul fehlt (Ticket `cal-macro-post-modul`, laut #132 aussichtsreichster ES-Buch-Weg) |
| **B — Konditionierte Reversion** | Fade von Überdehnung, aber NUR wenn Range/Kosten-Verhältnis stimmt (Vol-Regime als Prämisse) | Passt zum Dreh-Charakter von ES; die 0,90 %-Kostenquote gilt für die MEDIAN-Range — an Hochvola-Tagen bricht sie ein | ts_reversal hat 1 ES-Survivor; vixrev_ES_wide gerechnet (VIXCLS-Daten aber veraltet!) |
| **C — RV/Residuum NQ~ES** | Spread-/Residuum-Reihe statt totem Lead-Lag; LL-13: ist YM der bessere Laggard? | NQ führt Information, ES wird per SPY-Arbitrage eng geführt; korrigiertes Kostenmodell seit 23.08. | Engine-Baustein „Residuum-Reihe NQ~ES" fehlt — schaltet TR-01..07 + Pairs-Bank frei |
| **D — ES als Signal, NQ als Instrument** | SPX-nahe Features (GEX wirkt auf ES stärker: β −0,235 vs. −0,129 #110; VV-42 NQ/ES-Volumen-Ratio; VV-44) als Filter auf NQ-Beine | Buch-Beitrag ohne ES-Kosten zu zahlen — das v2-Kriterium fragt nicht, welches Instrument ausführt | Hypothesen liegen ungetestet in den Bänken |

Dazu ein **Quick-Win vorab**: Die Bank-Beine `EVENT_ES_primary`, `OPEXMOM_ES`, `CAL_fomcpost_ES` wurden gegen ein **anderes Buch** abgelehnt. Gegen das heutige 4/4-NQ-Buch (Diversifikation fehlt jetzt erst recht) ist der Buch-Marginal neu zu rechnen — das ist die billigste Chance der ganzen Woche auf ein ES-Bein.

---

## 3. Wochenplan

Rahmen: Queue ist seit 25.08. **leer**, Runner idelt — die Box gehört diese Woche den ES-Jobs (hohe `priority`, Auto-Nachschub des job_generator läuft in Lücken weiter). Durchsatz laut Register: 100–120 Jobs bzw. 1.200–2.900 Grid-Zellen pro Batch-Tag sind machbar. n_global aktuell 7.379 — die Zufallsdecke wächst mit, also **Mechanismus-Vielfalt statt Grid-Masse** (#494/#127-Lehre).

### Tag 0 — sofort (½ Tag): Aufräumen + Quick Wins
1. ~~Die drei ES-Jobs vom 25.08. auswerten~~ **Erledigt beim Pull am 27.08.:** alle drei durchgefallen — `wexp_charm_ES` 0 Survivors (PBO kaputt), `eusession_break_ES` Prämisse tot (Edge −2,4 pp), `vixrev_ES_wide` 0 Survivors, aber Selektion „dünn" (PBO 22 %, p=0,12) und auf **veralteten VIXCLS-Daten** gerechnet → Re-Run nach Daten-Refresh ist gerechtfertigt. Inbox danach mit `--seen-all` aufräumen (141 ungelesene Einträge, die „besser"-Kandidaten darin sind alle geblockt: corr_book ~0,9 / nur 1 von 4 Märkten).
2. ~~Daten-Hygiene~~ **Erledigt (27.08.):** VIXCLS.csv (FRED, jetzt bis 2026-08-26) und DIX_GEX_daily.csv (SqueezeMetrics, jetzt bis 2026-08-26) neu gezogen, nach `exported_data` geschrieben, per `box_provision_discovery.ps1 -SyncOnly` auf die Box verifiziert. Ticket `spx-csv-refresh` gelöscht. `vixrev_ES_v2`-Re-Run steht noch aus (Tag 1–2, Lane B).
3. ~~Quick-Win-Marginals~~ **Erledigt (27.08., 5 Seeds, v2 gegen das 4-Bein-Next-Buch):** beide **neutral**, kein Zug. `EVENT_ES_primary` (110 Trades, 10,8/Jahr): Δ 0,0pp, Rauschen 0,7pp, Schwelle 1,5pp. `OPEXMOM_ES` (74 Trades, 7,1/Jahr): Δ 0,8pp, Rauschen 0,5pp, Schwelle 1,5pp — beide unter der Schwelle, also kein Next-Buch-Zug. `CAL_fomcpost_ES` existiert nicht mehr eigenständig (in `EVENT_ES_primary` aufgegangen, live_finalize.py-Kommentar: "keine Doppelzaehlung"). Ehrliches Ergebnis: die beiden validierten ES-Bank-Beine sind zu selten, um die Buch-Passquote spürbar zu bewegen — bestätigt exakt das Muster aus Abschnitt 1 (Punkt 4), sie bleiben in der Live-Bank.
4. ~~Lane-A Welle 1 einreihen~~ **Erledigt, Ergebnis da:** `pipeline-auditor` (27.08.) fand vor dem Push einen strukturellen Fehler — `min_tpy=25` in `GATES_HARD` gilt unconditional pro Grid-Zelle; Kalender-Hypothesen deren Trade-Zahl an Terminen hängt (nicht an den Grid-Parametern) können diese Schwelle durch KEINE Grid-Variation erreichen. `CE-02` (FOMC pre/post, ~9 Tr/Jahr) und `CE-03` (event_combo-Nachbarschaft, ~10-11 Tr/Jahr) wären ein garantierter Nulldurchlauf gewesen → aus der Queue genommen. Ticket für später: `H()` braucht einen `gates=`-Override für niedrig-frequente Bank-taugliche Hypothesen. **`CE-01` (Turn-of-Month) und `CE-04` (Quartalsende) sind auf der Box durchgelaufen — beide `premise_failed`, ehrliches Negativ:** CE-01 n=509, cost-stressed Edge −1,5pp (lokaler Naiv-Test zeigte +0,62pp — Differenz kommt vom 2-Tick-Kosten-Stress in der echten Pipeline-Bewertung, kein Bug). CE-04 beide Richtungen negativ (−4,1pp / −1,0pp). Turn-of-Month und Quartalsende tragen auf ES nicht.

### Tag 1–2: CPI/NFP-Modul bauen (Box rechnet parallel Welle 1)
⚠️ **Gate-Warnung vorab (27.08., aus dem CE-02/CE-03-Befund):** CPI ist ~12 Termine/Jahr, NFP ~12/Jahr — einzeln beide unter `min_tpy=25`, addiert ~24, immer noch grenzwertig. Bevor das Modul gebaut wird: entweder beide zu EINER Hypothese stacken (wie `event_combo` es mit FOMC+OpEx tut) um über 25/Jahr zu kommen, oder von vornherein einplanen, dass der Fund über den Quick-Win-Marginal-Pfad laeuft statt über den Discovery-Survivor-Funnel. Sonst gleiche Falle wie CE-02/03: Engineering-Aufwand fuer einen Job, der strukturell nie Survivor werden kann.
5. **`cal-macro-post-modul`**: harte Datumslisten (BLS: CPI + NFP; FOMC-Kalender) 2016–2026 als CSV nach `exported_data`, neuer cal-Untertyp (kein neues Einzelskript — Erweiterung des `cal`-Modus). Post-Event-Drift UND -Reversion, beide Richtungen, Zeitfenster-Achse, CPI+NFP gestackt (siehe Warnung oben). Danach: `engine-regression-tester`, dann `box_provision_discovery.ps1 -SyncOnly`, dann Jobs einreihen (Specs unten).
6. ~~Lane-B-Hypothesen~~ **Erledigt (27.08., vorgezogen aus Tag 1-2), Ergebnis da:** `CR-01` (Fade bei erhöhter Aktivität), `CR-02` (Fade Overnight-Dislokation), `CR-03` (VIX-Spike-Reversion neu vermessen) gebaut, smoke-getestet, `pipeline-auditor` freigegeben, `engine-regression-tester` GO (legt erste `golden_masters.json`-Baseline an, 6 Referenz-Beine + 2 Fallen-Kanarien, alle wie erwartet), auf der Box gerechnet. **Alle drei negativ:** CR-01 premise_failed (n=61, −16,4pp). CR-02 premise_failed (n=1313, −1,8pp). CR-03 lief den vollen Grid (24 Configs) durch, 0 Survivors, Selektion „dünn" (PBO 14%, p=0,12 — besser als Zufall, aber nicht sauber getrennt). **Dabei echten Engine-Bug gefunden und gefixt:** `qbt.py` DEFAULTS definiert `vix_thr=18.0` für ein anderes Feature (absolute VIX-Schwelle), kollidiert namentlich mit `vix_bias.py`s eigenem `vix_thr` (relative Spike-Schwelle, Default 0.10) — jeder Aufruf ohne explizites `vix_thr` erbt still den falschen Wert, 0 Trades, kein Crash. Betraf keine validierten Beine (die setzen `vix_thr` immer explizit), hätte aber CR-03 stumm leerlaufen lassen. Fix: Warn-Kommentar + `assert thr < 2.0` in `vix_bias.py`, regressionsgetestet, synct. **Fazit Tag 0: alle 5 gerechneten ES-Kalender-/Reversion-Hypothesen (CE-01, CE-04, CR-01, CR-02, CR-03) sind negativ oder zu schwach.** Konsistent mit der Analyse aus Abschnitt 1 — Preis-basierte Reversion/Kalender-Drift trägt auf ES nicht ohne weiteres; Lane C (Residuum) und Lane D (ES-als-Signal) sind jetzt die tragenden Hoffnungen der Woche.

### Tag 3–4: RV-Baustein
⚠️ **Vorab-Befund (27.08.):** Sämtliche LL01/LL04/LL07/LL14-Pairs-Jobs vom 24.08. starben mit **n=0 in der Prämisse** (`expR=None`) — das ist ein Verdrahtungs-/Datenproblem, kein ehrliches Negativ (Null-Ergebnis-Verdachtsregel). Erst klären, warum die Pairs-Prämisse 0 Trades baut (fehlender Spread-Feed?), dann bauen. Die RS01/SM04/SM05/SM10-Fails dagegen waren echt (klar negative Edges).
7. **Residuum-/Spread-Reihe NQ~ES** als Engine-Baustein in `sigcore.py`/`rv.py` (rollierende Beta-Bereinigung, Tageskontext um 1 Tag verschoben wie alles in sigcore). Regression-Test, Sync. Dann: Pairs-Bank `SM-01` (erst messen!), `LL-01` (Lead-Lag sauber mit korrigiertem Kostenmodell), `LL-13` (YM statt ES als Laggard), `TR-01..07`. Abgrenzungs-Pflicht zur Leiche `RV_leadlag_NQES`: Überlappungs-Test < 30 % (TR-11).

### Tag 5: Lane D + Vertiefung
8. ~~ES-als-Signal-Jobs~~ **Teilweise vorgezogen (27./28.08.):** `LD-01` (VIX-Regime-Filter auf NQ_Momentum-Mechanik, replaces_leg=NQ_Momentum_d260818) und `LD-02` (VIX-Regime-Filter auf NQ_VWAP-Pullback-Mechanik) gebaut und eingereiht — nutzen die bereits vorhandenen sigcore-Gates (tm_vix_min/max/rank), kein neuer Code nötig. GEX-Achse lief schon vorher als separater Job (`hyp_GEX01_NQ`). VV-42/VV-44 (NQ/ES- bzw. YM-Volumen-Ratio als Cross-Symbol-Feature) fehlt noch — braucht echten Engine-Baustein, siehe Punkt 7.
9. Follow-ups: der job_generator verfeinert Survivors automatisch; handgebaute Vertiefung nur, wo Welle 1/2 Survivors zeigt.

### ⭐ Zusatz-Auftrag Max, 27./28.08.2026 (nach Tag-0-Review, WICHTIG fürs Verständnis der Woche)
Nach dem ersten negativen Tag-0-Ergebnis hat Max explizit klargestellt: der Sinn der Woche ist, dass die **Box autonom tagelang/wochenlang** durch viele Implementierungen rechnet — nicht dass ich im Chat einzelne Jobs nachreiche. Zwei konkrete Aufträge daraus, beide umgesetzt:

- **Block EC** (`discovery/hypothesis_bank.py`, neu 28.08.): jede Kern-Mechanik unserer NQ-Strategien (Momentum, Fade, VWAP-Pullback, Kanal/Breakout) als vollständiger **Kombinations-Sweep** aus EMA (20/50/100/150/200 + SMA50), RVOL, Delta und VWAP-Seite auf ES — nicht nacheinander wie Block CE/CR, sondern gestapelt (`AX_FILTERS_COMBO`, 4 unabhängige Achsen, kartesisches Produkt). Dazu `EC-05`: EMA-Crossover 20–200 als **eigener Mechanismus**, nicht nur Filter. 5 Hypothesen, 1080 Configs, `pipeline-auditor`-geprüft (fand echten Design-Fehler in EC-05 — `mb_thr`-Default 0.0 ließ den Trigger praktisch immer feuern, nachgeschärft) und die Register-Pflicht für meine manuellen Vorab-Scans nachgetragen (27 Configs, `n_total` 7490→7518, dann +1080 durch den Job-Push). **Vorab-Scan-Befund, der die Grid-Suche motiviert:** rohes ES-Momentum ist negativ (−8,9pp), mit EMA100/EMA200-Bestätigung dreht die Edge auf +6,9/+9,4pp, mit EMA200+Delta kombiniert auf +11,9pp — bei allerdings noch zu niedriger Frequenz (tpy 18–22, unter der Käfig-Schwelle 25). Die Grid-Suche prüft, ob eine Zelle Edge UND Frequenz gleichzeitig schafft.
  **Endergebnis (28.08., über Nacht durchgelaufen): alle 5 negativ.** `EC-01` lief den vollen Grid (216 Configs, 23 min), 0 Survivors, Selektion „kaputt" (PBO 49% — reines Rauschen, keine der 108 Filter-Kombinationen trennt sich vom Zufall). `EC-05` ebenso voller Grid (216 Configs, 70 min), 0 Survivors, „kaputt" (PBO 29%). `EC-02`/`EC-03`/`EC-04` premise_failed wie erwartet. Der im Vorab-Scan gesehene positive Einzelpunkt (EMA200+Delta +11,9pp) hat sich im vollen Grid **nicht** als robuste Zelle bestätigt — Einzelfund, kein Plateau. **Fazit Block EC: negativ, aber sauber und vollständig geprüft, kein Bug.**
- **`alpha-scout`** läuft im Hintergrund mit einem gezielten Auftrag: neue HF-taugliche (>25 Trades/Jahr) ES-Mechanismen jenseits von Preis-Momentum/Fade/Kalender finden (Mikrostruktur, Options-Flows jenseits GEX, Intermarket-Spreads, häufigere strukturelle Flows). Ergebnis kommt als Report nach `discovery/scout_reports/` + Job-Vorschläge nach `discovery/jobs_proposed/` — muss noch geprüft und eingereiht werden.

**Ehrlicher Hinweis zur Queue-Tiefe:** der automatische `job_generator` (min_pending=3, 24/7) füllt die Queue zwar immer auf, aber sein Standard-Coverage-Mechanismus ist ein Round-Robin über 9 generische Vorlagen × 4 Märkte — für ES sind davon bereits 10 von 11 Kombinationen als „gerechnet" markiert (`generator_state.json`), meist mit 0 Survivors. Ohne gezielte neue Hypothesen (wie Block EC oder alpha-scouts Funde) würde der Generator also grösstenteils NQ/RTY/YM-Lücken füllen, nicht ES. Block EC (1080 Configs) und was `alpha-scout` liefert, sind der eigentliche Puffer für mehrere Tage autonome Box-Zeit — nicht der Generator allein.

### Tag 6 / Wochenende 05.–06.09.: Review + Entscheidung
10. Gesamtauswertung: Inbox + Register-Delta, alle „besser"/deploy_ready-Kandidaten durch **Quant-Team + strategy-auditor**, `pipeline-auditor` über den Wochenprozess. Next-Week-Ticket abarbeiten (Übernehmen/Verwerfen). Logbuch-Eintrag mit ehrlichem Fazit je Lane. Entscheidung für Woche 2: die stärkste Lane bekommt den Fokus — und **wenn ES als Ausführungsmarkt ehrlich scheitert, ist das ein valides Ergebnis** (dann trägt Lane D + die Bank-Beine den ES-Beitrag, kein Zwang zum ES-Bein).

### Tagesroutine (jeden Tag, ~15 min, sonnet)
`inbox_tool.py --pull` → neue Survivors/Kandidaten checken (Stufe benennen) → Queue ≥ 3 pending halten (ES-Jobs mit Vorrang) → bei Next-Buch-Änderung sofort `--push-next`.

---

## 4. Queue-fertige Job-Specs

Alle über `hypothesis_bank.py` (neue Zeilen, **kein** Einzelskript): Why-Pflicht, ≥ 10 Implementierungen via `AX_CONFIRM`/`AX_RISK`/`AX_EXITS`, `GATES_HARD` + `controls.py` automatisch. Märkte: primär ES, RTY/YM als Multi-Markt-Kontrolle läuft über die Controls mit. Grids ≤ ~100 Configs.

**Lane A (Tag 0, cal-Modus existiert) — Stand 27.08., real umgesetzt statt der urspruenglichen Konzept-Namen:**
1. ✅ `CE-01` (=`cal_monthend_ES`, `cal_mode=tom`) — Why wie geplant. 36 Configs, auf der Box eingereiht (`hyp_CE01_ES`, prio 97). Premise: n=509, Edge +0,62pp (schwach positiv, geht in die volle Grid-Vermessung).
2. ✅ `CE-04` (=`cal_quadwitch_ES`, als `qend_long`/`qend_short` — Quartalsende statt exaktem Quad-Witching-Verfallstag, engine hat kein eigenes Quad-Witch-Datum) — 10 Configs, eingereiht (`hyp_CE04_ES`, prio 96). Premise: beide Richtungen negativ (-4,35pp / -2,96pp) — vermutlich premise_failed, ehrliches Negativ.
3. ❌ `cal_opex_stack_ES` (=`CE-03`, event_combo-Nachbarschaft von `EVENT_ES_primary`) — **NICHT eingereiht.** `pipeline-auditor`: `min_tpy=25` ist unconditional, event_combo liegt bei ~10-11 Tr/Jahr, garantierter Nulldurchlauf unabhängig von der Edge. Stattdessen ueber Quick-Win-Marginal geprueft (Ergebnis: neutral, Abschnitt „Tag 0" oben).
4. ❌ `cal_fomc_variants_ES` (=`CE-02`, fomc_pre/fomc_post) — **NICHT eingereiht**, gleicher Grund (~9 Tr/Jahr). FOMC-Pre-Drift bleibt damit fuers Erste ungetestet; waere nur ueber den Bank-Pfad (nicht Discovery-Funnel) sinnvoll pruefbar.

**Lane A (Tag 1–2, nach Modul-Bau):**
5. `macro_cpi_post_ES` — Why: CPI-Prints setzen den Repricing-Pfad für Zins-Erwartungen; institutionelles Nachziehen dauert Stunden bis Tage, Privatanleger können 8:30-ET-Prints nicht systematisch handeln. Harte BLS-Datumsliste statt Volumen-Spike-Heuristik. Achsen: Drift vs. Fade, Einstiegs-Verzögerung (0/30/60 min), Haltedauer (Intraday/Overnight/2d), Stop, Bestätigung.
6. `macro_nfp_post_ES` — analog NFP (Freitags-Prints, Wochenend-Gap als eigene Achse).

**Lane B (Tag 1–2):**
7. `rev_bigrange_ES` — Why: ES ist der Dreh-Markt; an Tagen mit Range ≥ x·ATR bricht die Kostenquote von 0,90 % auf handelbar ein und Überdehnung zieht Arbitrage-/MM-Gegenflow an. **Prämisse = Range-Regime** (RVOL/ATR-Schwelle), nicht Nachgedanke. Achsen: Dehnungs-Messung (VWAP-Distanz/σ-Stretch/rangepos), Schwelle, weite Stops (1,0–1,5σ), Exit (Zeit/EOD/Mean-Touch).
8. `rev_overnight_ES` — Why: Übernacht-Dislokationen (Gap gegen Vortagstrend) werden im RTH von Index-Arb geschlossen; Haltedauer länger = weniger Round-Turns = Kostenquote sinkt. Achsen: Gap-Größe in σ, Basis (prev_rth/overnight aus tsmom-Modul), Halten bis Mittag/EOD/T+1.
9. `vixrev_ES_v2` — Why: VIX-Spike-Reversion ist die validierteste Reversion auf ES (Grade C, PF 1,22); nach VIXCLS-Daten-Refresh Verfeinerung um den bestehenden Survivor (Schwellen-/Stop-Nachbarschaft statt neues Grid). **Erst nach Ticket `spx-csv-refresh`.**

**Lane C (Tag 3–4, nach Residuum-Baustein):**
10. `rvres_meanrev_NQES` — Why: NQ führt Information, ES wird per SPY-Arbitrage eng geführt; das beta-bereinigte Residuum sollte mean-revertieren, und der Fehler des toten Lead-Lag (Risiko im falschen Instrument, #075/#090) ist im neuen Baustein strukturell ausgeschlossen. Achsen: Beta-Fenster, Einstiegs-Schwelle in Residuum-σ, welches Bein ausführt (ES vs. NQ!), Halbwertszeit-Exit. Pflicht: Überlappungs-Test < 30 % zur Leiche.
11. `rvres_laggard_YM` — Why: LL-13 — wenn ES der am engsten arbitrierte Index ist, ist der träge YM der bessere Laggard; gleiche Mechanik, Instrument-Achse YM. (Kein ES-Bein, aber beantwortet, OB die RV-Lane überhaupt ein Index-Bein trägt.)

**Lane D (Tag 5):**
12. `nqfilter_es_signals` — Why: SPX-nahe Zwangs-Flows (Gamma, Volumen-Migration) sind auf ES messbar stärker (β −0,235 vs. −0,129, #110), wirken aber auf den Gesamtindex-Komplex; als Regime-Filter auf NQ-Beine verbessert das den Buch-Beitrag ohne ES-Kosten. Format: Filter-/Exit-Sweep „vs Original besser" auf `NQ_Momentum` und `NQ_VWAP-Pullback`. Achsen: Signalquelle (VV-42 Volumen-Ratio / VV-44 YM-RVOL / GEX-Vorzeichen / VIX-Level), Schwellen, Filter-Logik (nur Long-Seite / beide).

---

## 5. Guardrails (nicht verhandelbar)

- **Der EINE Weg gilt** (CLAUDE.md 23.08.): alles über `hypothesis_bank.py`, ≥ 10 Implementierungen, Why-Pflicht, `GATES_HARD`, `controls.py`. Neue Mechanik = neuer `mb_kind`/`tm_signal`/cal-Untertyp, kein Skript daneben.
- **ES-Kosten-Vorabrechnung (neu, aus #132):** jede ES-Hypothese rechnet VOR dem Einreihen den erwarteten $/Trade gegen Round-Turn + 2-Tick-Stress; unter ~3× Kosten → Haltedauer/Selektivität erhöhen oder Idee verwerfen. Empfehlung an die ausführende Session: das als Prämissen-Check in den Job-Bau übernehmen, dann prüft es die Maschine statt der Disziplin.
- `pipeline-auditor` vor jeder Job-Welle; `engine-regression-tester` vor jedem `-SyncOnly`; Quant-Team + `strategy-auditor` vor jeder Buch-Entscheidung.
- Rausch-Disziplin: Marginals immer 5 Seeds, „besser" heißt ≥ 1,5 pp UND 2× Seed-Streuung. Korrelation zum Bestandsbuch ≤ 0,70. ORB-artiges immer `orb_exec=close`.
- Box-Disziplin: Engine-Änderung → `-SyncOnly` vor dem Nachtlauf; jede Änderung an `book_state*.json` → sofort `--push-next` (Vorfall #126). Register lückenlos.

## 6. Erfolgskriterien am Sonntag (06.09.)

- Pflicht: alle 4 Lanes gerechnet (~60–100 ES-Jobs durchs Register), CPI/NFP-Modul und Residuum-Baustein in der Engine, Quick-Win-Marginals entschieden, Logbuch-Eintrag mit Lane-Fazit.
- Zielbild: **≥ 1 ES-Bein oder ES-Signal-Filter deploy_ready im Next-Week-Buch.**
- Ehrliche Alternative: belegtes „ES trägt als Ausführungsmarkt nur Events" → Woche 2 fokussiert Lane A-Stacking + Lane D.

## 7. Buch-Lücken-Status der bekannten ES-Kandidaten (27.08.)

| Kandidat | Stufe, an der es hängt | Was fehlt konkret |
|---|---|---|
| `EVENT_ES_primary` (Bank) | Buch-Marginal — **erledigt, neutral** | Δ 0,0pp vs. 1,5pp-Schwelle gegen das 4-Bein-Next-Buch (27.08.). Bleibt in der Live-Bank, kein Next-Buch-Zug. |
| `OPEXMOM_ES` (Bank) | Buch-Marginal — **erledigt, neutral** | Δ 0,8pp vs. 1,5pp-Schwelle (27.08.). Bleibt Bank-Kandidat. |
| `CAL_fomcpost_ES` | — | existiert nicht mehr eigenständig, in `EVENT_ES_primary` aufgegangen (live_finalize.py) |
| `CE-01` (tom, ES) | rechnet auf der Box | 36 Configs eingereiht 27.08., Premise schwach positiv (+0,62pp) |
| `CE-04` (qend, ES) | rechnet auf der Box | 10 Configs eingereiht 27.08., Premise beide Richtungen negativ — voraussichtlich premise_failed |
| `CE-02`/`CE-03` (FOMC pre/post, event_combo-Nachbarschaft) | strukturell blockiert | `min_tpy=25` unerreichbar bei ~9-11 Tr/Jahr — braucht `gates=`-Override in `H()` (Ticket fuer spaeter) oder bleibt beim Bank-Pfad |
| `wexp_charm_ES` | tot (0 Survivors, PBO kaputt) | nichts — beerdigt, ins Register eingezahlt |
| `eusession_break_ES` | tot (Prämisse, Edge −2,4 pp) | nichts — beerdigt |
| `vixrev_ES_wide` | Datenbasis erledigt (VIXCLS/DIX-GEX 27.08. aktualisiert) | Re-Run als `vixrev_ES_v2` steht noch aus (einziger der drei 25.08.-Jobs mit Restchance) |
| Pairs-Bank LL-01/13 | Verdrahtung (n=0-Prämisse) | Bug-Klärung + Residuum-Baustein (Tag 3–4) |
| alles Momentum-artige auf ES | Prämisse/edge-Gate | nichts — beerdigt lassen, neue Mechanismen statt mehr Grid |

Verwandt: [[Alpha-Suche]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Discovery-Runner v2]] · [[Day Trading]]
