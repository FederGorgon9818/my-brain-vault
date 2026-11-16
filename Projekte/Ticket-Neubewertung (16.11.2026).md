---
tags: [tickets, prio, neubewertung]
datum: 2026-11-16
status: Neubewertung geschrieben, Lösch-Liste wartet auf Max
---

# Ticket-Neubewertung (16.11.2026)

Auftrag Max: alle offenen Tickets neu bewerten, Skala von „sofort, unabdingbar“ bis niedrig. Entscheidungen Max (Popup 16.11.): **6 Stufen, „Wichtig (Datum)“ raus**, veraltete Tickets als **Lösch-Kandidat markieren** (gelöscht wird nur nach Max' OK), **direkt schreiben**. Ergebnis: 233 offene Tickets bewertet, auf PC und Box gleich. Skala im Code und Lab: [[Ticket-Board (Jira-Stil)]] Abschnitt „Stand 16.11.2026“.

## Skala

| Stufe | intern | heißt |
|---|---|---|
| Sofort | `sofort` | unabdingbar, in den nächsten Tagen, sonst Schaden an Live-Konto, Geld oder harter Frist |
| Sehr hoch | `kritisch` | diese Woche angehen |
| Hoch | `rot` | in den nächsten zwei bis drei Wochen |
| Mittel | `gelb` | normale Arbeit, wenn Platz ist |
| Niedrig | `gruen` | irgendwann, wenn Zeit ist |
| Geparkt | `geparkt` | bewusst auf Eis, kommt nur bei Bedingung oder Ansage zurück |

Fällig-Datum bleibt ein eigenes Feld und hebt ein Ticket im Lab automatisch unter „Dringend“, sobald es in 7 Tagen fällig ist (außer geparkt).

## Verteilung

Sofort 2 · Sehr hoch 4 · Hoch 20 · Mittel 59 · Niedrig 111 · Geparkt 10 · Lösch-Kandidaten 27 (stehen bis zur Entscheidung auf Niedrig, Label `loesch-kandidat`).

## Sofort (2)

| Ticket | Titel | warum diese Stufe |
|---|---|---|
| AP258 | Checkliste: SOFORT abarbeiten, wenn ein Eval/Challenge besteht (E8 50k, FN1/FN2, ab 02.10. E8 150k) -- sonst b | Pass war am 10.11.; offen nur noch der RiskGuard-Deploy (EvalProfitTarget 0) am Wochenende, danach schließen |
| AP317 | Host live: skip_dates fuer Kurztage 27.11. und 24.12. pflegen | Kurztag 27.11. (Thanksgiving-Freitag), letztes Deploy-Wochenende davor ist der 21./22.11., sonst bleibt eine Position über den Schluss offen |

## Sehr hoch (4)

| Ticket | Titel | warum diese Stufe |
|---|---|---|
| AP238 | ⚠️ BOS-Finanzplan VOR jedem groesseren Kauf: Lebenshaltung, Reserve, BAfoeG-Anspruch | blockt jeden Kauf (Kaufrunde, Handy, Hardware), Frist 30.11. |
| AP394 | NT8-Port OpEx-Modul (opex_mom) plus Paritaet | erster Live-Tag OpEx Fr 20.11., ab 18:01 Boxzeit NT8-Log je Konto prüfen |
| AP413 | NT8 deaktiviert beim Wochenend-Verbindungsabbruch alle Hosts und RiskGuards, Wiederanlauf jedes Wochenende per | NT8 schaltet jedes Wochenende Hosts und Guards ab, Wiederanlauf per Hand; verpasste Handelstage gefährden die Funded-Konten |
| AP415 | NT8 Auto-Login einspielen und testen (AP134 Login-Teil) | Gegenstück zu AP413 (Auto-Login), nur noch Test 2 offen |

## Hoch (20)

| Ticket | Titel | warum diese Stufe |
|---|---|---|
| AP37 | Revolut Business beantragen (3-10 Tage) + Steuer-Ruecklagenkonto mit fester Regel | Geschäftskonto für die Trennung privat/Gewerbe, Datum 31.10. überzogen |
| AP171 | MaxRiskGuard: End-of-Day-Telegram-Report fertig, Deploy fehlt -- mit dem Wochenend-Deploy buendeln | RiskGuard-Feature fertig, mit dem RiskGuard-Deploy am Wochenende bündeln |
| AP236 | ⚠️ DEADLINE 03.04.2027: bei der Agentur fuer Arbeit arbeitsuchend melden (Vertrag endet 03.07.2027) + ALG-I-Op | harte Frist 03.04.2027, sonst Sperrzeit beim ALG |
| AP237 | ⚠️ Krankenversicherung klaeren: Juli/August 2027 und BOS-Zeit (Familienversicherung? eigene KV?) | Versicherung ab Juli 2027 klären, fällig 30.11. |
| AP251 | Belege-Nachtrag Oktober (einmalig): Claude-Zahlungsbeleg Sept., FFN-Rechnung, Gmail-Funde Juni bis Sept. | Ausgaben zählen nur mit Beleg (EÜR 2026) |
| AP252 | API-Keys Gemini, Groq, OpenRouter neu erzeugen (standen am 22.09. im Klartext im Chat) | Keys standen im Klartext im Chat, 10 Minuten Arbeit |
| AP383 | Look-ahead-Schutz Tageswerte: Lint/Hook fuer Scratch-Joins + Kanarie fuer sigcore.daily_context (Rest AP232) | Look-ahead-Schutz der Tageswerte fehlt in der Pipeline |
| AP390 | BOS-Regel entscheiden: ab Gehaltsende nur noch aus Gewinn nachkaufen? | gehört zum BOS-Plan AP238 |
| AP412 | Discovery-Queue leer: alpha-scout neue Mechanismen liefern lassen | Discovery-Queue seit 18.10. leer, Regel: darf nie leerlaufen |
| AP452 | Box-Sync: Box-seitige Aenderungen erkennen statt still ueberschreiben (Lehre Nightrun BTC) | Box-Sync überschreibt Box-Änderungen still (Vorfall 26.10.) |
| AP454 | Wochenende: einmaliger Look-ahead-Code-Check fuer asian, maband, orb, ts_reversal, tsmom (Modus-Stand am 27.10 | Modus-Stand am 27.10. ohne Look-ahead-Check gesetzt |
| AP456 | Wiedervorlage 28.10.2026: Belege des Monats sammeln (alle Rechnungen + Zahlungsbelege) | Belege Oktober, Ausgaben zählen nur mit Beleg |
| AP457 | Alpha-Suche Playbook: Tickets T01 bis T22 und E6 (Welle 0 zuerst) | Alpha-Suche Playbook, von dir am 28.10. entschieden |
| AP458 | Playbook T01: Ideen-Vorlage mit 7 Angaben, Beobachtungs-Tagebuch und Wissens-Inventur (40 Fragen) | Playbook T01, öffnet deine eigenen Ideen (Juli-Modus-Befund) |
| AP459 | Playbook T02: Werkzeug-Paket Markt-Uhr (Teil A vor Welle 1, Teil B vor Welle 2) | Playbook T02 Teil A, Voraussetzung für Welle 1 |
| AP460 | Playbook T03: Eichung der Stufenregel mit mindestens 200 Placebo-Feldern (Welle 0) | Playbook T03, Welle 0 |
| AP462 | Playbook T05: Buch-Profil und Steckbrief fuer das 6er-Buch neu messen (Welle 0) | Playbook T05, Welle 0 (Zahlen noch vom alten Buch) |
| AP463 | Playbook T06: Erste Fassung automatisch (Hochstufen schreibt Eintrag mit, Satzungs-Vorlage, Sperre 'kein Job o | Playbook T06, sonst ist jedes neue Next-Bein in Stufe 2 nicht prüfbar |
| AP464 | Playbook T07: Walk-Forward-Start 01.01.2016 fest uebergeben (R13) | Playbook T07, Welle 0, klein |
| AP465 | Playbook T08: Unabhaengigkeit messen (Nacht ES/YM/RTY gegen das Buch, BTC ausserhalb RTH, 6B/ZN/ZB/FDAX gegen  | Playbook T08, Welle 0 |

## Mittel (59)

| Ticket | Titel |
|---|---|
| AP39 | Beim ERSTEN Payout-Request: Processor-Einladung (WorkMarket/Rise) vollstaendig durchgehen inkl. W-8BEN |
| AP122 | Pipeline-Haertung aus Audit 03.09.2026: Register append-only (Lehre 144 zum 2. Mal verletzt), Profil-Achsen-As |
| AP134 | UI-Automation fuer NT8: Login-Fenster ausfuellen + Strategien aktivieren (einziger dokumentierter Weg) |
| AP144 | OnExecutionUpdate ohne Realtime-Filter: historische Sim-Fills landen im Live-Log (maxlab_executions.csv doppel |
| AP148 | Git-Haertung statt Worktrees: Engine unter Git, Schreib-Sperre fuer Finalize/Developer, Union-Merge + Branch-B |
| AP155 | Entscheiden: Wie werden die Live-Strategien kuenftig automatisiert (NT8-Host-Strategie / MultiCharts Portfolio |
| AP172 | Live-Betrieb haerten nach Noel-T-Interview: DD-Kill-Switch, Inkubations-Bank, MC-DD je Bein, Konfluenz-Sizing- |
| AP173 | Familien-Sperre in promote_next + cal-Kontrollen + add_job-Validierung (Audit Scout-Batch 30.08.) |
| AP184 | book_cells.json-Cache bekommt Engine-Fingerprint + EINE Key-Funktion (war seit 03.09. stale, hat den Runner ge |
| AP196 | NT8-Historie: fehlende Front-Kontrakte nachladen (GC 12-26, CL 09-26 ff., 6E/6B 12-26), weitere E8-Maerkte lad |
| AP203 | Dauerhaften Regel-Check einbauen: RiskGuard-Regeln automatisch umstellen, wenn ein Konto von Challenge/Eval au |
| AP213 | Golden-Master: KANARIE_lookahead schwaecher als geplant, r_only_artifact-Erwartung veraltet, RVOL-maband ohne  |
| AP229 | GATES_HARD top5_share_max n-normieren: die Schwelle ist ein verkappter Frequenz-Wall und schliesst JEDEN selek |
| AP231 | Hartes Gate 'Mindest-Risiko in Ticks' in controls.py -- zweite Wiederholung derselben Fehlerklasse |
| AP240 | Kinfo-Zahlen gegen unsere eigenen Zahlen abgleichen (verifizierter Track Record) |
| AP249 | Anbieter-Konten: Privat- oder Firmenkunde (USt-IdNr) je nach USt-Entscheidung umstellen |
| AP267 | Ticket-Board auf der Box einspielen (Max sagt Claude Bescheid) |
| AP275 | Stufe 2: Ueberoptimierungs-Pruefung (Herkunft) kalibrieren, VOR dem Wochenende 03./04.10. |
| AP304 | ONORB-W45a ist ungemessen: tm_pre_ret_min/tm_pre_rvol_min wirken nicht (NaN-Verdacht in sigcore) |
| AP311 | Bitcoin-Daten (BTC/MBT/MET) laden + Zaehlung + Modul crypto24 (Rest AP211) |
| AP312 | prescan_gross.py als Pflicht-Vorzaehlung vor Handjobs (Rest AP211) |
| AP315 | MaxBookHost: Exit-Klammer gegen Host-eigene Position statt Konto-Position (Waisen-Falle 15:55) |
| AP316 | Telegram-Alarm bei Host-Zeilen WaitUntilFlat / EXIT uebersprungen |
| AP329 | Bug: Asia-Bein tmin_entry ab Mitternacht statt ab 09:30, buchweiter Stopp auf Trade-Ebene sortiert falsch |
| AP340 | MaxBookHost: 15:55-Flatten (ClampExit) gegen veraltete Konto-Position erzeugt Waisen-Positionen |
| AP347 | Engine-Fingerprint aus dem Modus-Dispatch ableiten (calendar_fx, pivot, flip, vix_bias fehlen in den Listen) |
| AP354 | sync_live.ps1 haengt am SSH-Befehl und hinterlaesst Zombie-Prozesse |
| AP386 | Rest AP212: FN-Snapshot meldet Short 2 obwohl flat, Live-Monitor ohne Preisquelle, zwei Anzeige-Fragen |
| AP387 | Asia-Dir: Stufe 2 mit und ohne Asia, vola-angepasst, getrennt 50k und 150k |
| AP391 | Kaufrunde 06.11.: Neu-Rechnung mit Stand 05.11. und Kauf-Ampel |
| AP393 | Buch-Waechter: gescheiterter --push-next schaltet den Hook stumm |
| AP395 | NT8-Port LD01: VIX-Feed auf der Box plus VIX-Filter im Momentum-Modul plus Paritaet |
| AP396 | Next-Week-Buch und echtes Buch: plan-Block veraltet (Kontodaten nachziehen) |
| AP399 | Markt-Universum je Prop-Firm: welche Maerkte koennen wir handeln (BTC, Waehrungen, Metalle, Agrar) und alle ei |
| AP402 | Live-Gebuehr und Live-Slippage als Dauerkontrolle (live_fee.py woechentlich, live-reconciler) (Folge AP384) |
| AP403 | Knappe Survivors und Kandidaten mit echter Gebuehr nachrechnen, Gebuehren-Stempel im Register (Folge AP384) |
| AP408 | Box-Sync Rest: promote_next gegen halben Sync, Scratch-Liste per Test, CRLF-Warnung, Waisen-Bericht |
| AP409 | Haengende scp/ssh-Aufrufe zur Box ohne Abbruch (Ticket-Abgleich, Live-Datenabholung) |
| AP422 | Krypto-Standbein ueber CFD-Props: BTC/MBT-Daten, Krypto-Edge, CFD-Prop-Recherche |
| AP423 | Live-Ausstiegsregel-Pflicht: jedes live laufende Bein ohne Buch-Eintrag braucht Regel und Alarm |
| AP428 | Paarversuch Zeit-Exit vor 15:55 (B') auf Teil der Konten (AP426) |
| AP433 | AP422 Schritt 1: Binance-Spot BTC/ETH laden, Parquet, Zaehlung gegen CFD-Kosten, NT8-Gegenprobe BTC/MBT |
| AP438 | BTC-Discovery auswerten: OR-Groessen-Filter (BTC-01) gegen Zufallslevel-Kontrolle (BTC-02) |
| AP439 | Drei Pipeline-Luecken aus dem BTC-Nightrun schliessen (Kanarie fuer neue Daten-Filter, Kill-Schwelle als Code- |
| AP446 | RiskGuard Inaktivitaets-Warnung Stufe 1: woechentlicher Fehlalarm bei E8/FN1/FN2 (Fr- und Mo-Abend) |
| AP449 | Firmenhandy: Black-Friday-Angebote gegen Messlatte vergleichen |
| AP451 | Pipeline: neue Engine-Keys gegen alten Runner-Code und still ignorierte Filter absichern |
| AP455 | Fokus-Planer: Google-Zugang einrichten (Kalender Tickets, Dienstkonto, Schlüssel auf die Box) |
| AP461 | Playbook T04: Tafel-Standardeingang ohne scipy (Querzeile, Verzoegerungs-Zelle, Register-Typ Tafel/Grid) |
| AP466 | Playbook T09: Wiedervorlage nach Bedingung statt nur nach Datum |
| AP467 | Playbook T10: Termin-Dateien EIA, WASDE, COT, Crop Progress, Treasury-Auktionen, EZB, LBMA, Index-Roll |
| AP468 | Playbook T11: Roll-Maske / Roll-Adjuster fuer GC, CL, 6E, ZS, ZW |
| AP470 | Playbook T13: Engine-Tabellen 6B, ZN, ZB, FDAX mit Gebuehren aus Primaerquelle |
| AP471 | Playbook T14: Modus 'Ausloeser in A, Handel in B' mit eigener Uhr je Seite |
| AP472 | Playbook T15: Einzelkontrakt-Loader aus dem NT8-Export |
| AP476 | Playbook T19: alpha-scout und familien-scout auf Zeit bis 50k umstellen, Bank um Tafel-Pfad ergaenzen |
| AP478 | Playbook T21: Kosten-Messung je Markt (Databento-Kostenabfrage MBP-1 und Trades, 7 Maerkte) |
| AP480 | Playbook E6: Index-Dateien pruefen (NQ/ES/YM/RTY Ende 10.08. gegen NT8-Versionen bis 18.09.), dann entscheiden |
| AP481 | Steuer: Erklärungen 2023 bis 2025 vorbereiten und ersten Beleg-Abgleich fahren |

## Niedrig (111)

| Ticket | Titel |
|---|---|
| AP44 | Claude dispatch anschauen claudian |
| AP111 | E8-Support: Payout-Caps fuer 100k/150k schriftlich bestaetigen lassen |
| AP117 | Day-Gate-Mechanik + Tages-Gate-Kontrollbatterie in die Engine (Lehre #136) |
| AP119 | NQ_LastHour_v3: neue Delay-Kontrolle faellt sauber durch (z=-3.39, 99% Ueberlappung) |
| AP120 | TS-01-v2 EWMAC (eval_layer.py _ts01v2_mb_cfg): echter Timing-Verdacht nach Cutoff-Bugfix |
| AP123 | Exit-Forschung Stufe 2: ATR-/Chandelier-Trailing (trail_dist_mode=atr) + Zeit-Verschaerfung in _trail_stop, ge |
| AP125 | Regime-Waechter im Portfolio-Tab: rollierende 3J-Drift vs. Break-even + Sizing-Kelly-Check k* |
| AP130 | Sizing-Trichter im Portfolio-Tab: Passquote + E[Auszahlung] ueber der Buchgroesse, laeuft bei jeder Buch-Aende |
| AP131 | Discovery-Runner parallelisieren: Config-Schleife auf 4 Worker (Box hat 6 Kerne, Runner nutzt einen) -- ~4x Du |
| AP132 | Mehrkonten-Zuordnung vereinheitlichen: welches Konto hat welche RiskGuard-/Telegram-/Sizing-Config, zentral st |
| AP137 | Kandidaten-Pipeline (Uebergabe 06.09.): Null-Schalter Buch-Modi + Kalender/DIX-Gates deployen, Ersatz-Slot-Sem |
| AP142 | Datenexport fuer neue Futures-Symbole: Databento GLBX.MDP3 ohlcv-1m -> 1m-Parquet (zuerst GC, dann CL); QuantP |
| AP143 | Databento-Account anlegen + echte metadata.get_cost-Abfrage fuer GC/CL/SI/NG/ZN/6E (Continuous vs. Parent-Symb |
| AP146 | Developer/Discovery-Pipeline: Dollar-Gates je Min-Size neben R, n_trials aus Sweep/Register statt Versionszahl |
| AP147 | VWAP-Offensive: 12 Familien abarbeiten, Hauptziel Buch-Passquote |
| AP150 | maband VWAP-Erweiterungen (VWAP-Offensive Phase 3): ATR-Normierung der Distanz, Level-Export + tm_exit=level f |
| AP156 | Pipeline-Haertung aus dem CVD-Audit: exec_bug-Gate, Daten-Integritaets-Gate, Kontroll-Job-Premise, DSR-Gate |
| AP161 | Backtest-Exit 15:55 wie live: sigcore-Entscheidung, Developer-Cache, Edge-Ref, Register-Markierung |
| AP163 | Pipeline-Fixes aus Audit #139: Modus-Zulassungs-Gate, replaces_leg-Assert, gepaartes Rauschmass, ehrliche Deck |
| AP167 | Modul cal_mode='macro_post' (CPI/NFP-Post-Release auf ES) + harte BLS-Datumslisten 2016-2026 |
| AP168 | FA-01-Nachlauf: gepaarte Overlay-Auswertung + Placebo-Kontrolle in die Pipeline |
| AP182 | Vorab-Messung ES-NQ-Divergenz (Prozent vs. z-Score, 17.09.) per backfill_registry.py nachtragen |
| AP183 | Friedhof-Analyse 17.09.: fuenf Entscheidungen (Referenzbuch, Slot-Tabelle, Live-Grade-Karte, Coast-Leg-Schalte |
| AP186 | Bestandsdurchlauf: alle 4 Buch-Aufnahme-Entscheidungen unter dem seit AP151 P8 korrigierten Rauschmass nachrec |
| AP187 | Buch-Korrelationsanzeige zeigt nur den Mittelwert und die family-Spalte statt Mechanismus-Cluster -- verdeckt  |
| AP188 | Teilmengen-/LOO-Scan darf nie einen Sieger ohne Out-of-Bag-Spalte liefern -- subset_scan() in eval_plan.py + a |
| AP189 | Pipeline-Fixes aus dem AC-06d-Audit: write_json-Retry, control_labels in H(), ctl_null fuer leg in $, save_tra |
| AP195 | CL-Nachtest: Filter-/Event-Hypothesen auf MCL nie gerechnet (Praemissen-Sperre AP151 P1) + Lint fuer neue Hypo |
| AP200 | Aufraeumen nach der NT8-/Neue-Maerkte-Aktion: _staging, Backups, Export-Ordner, Pipeline-Kleinkram |
| AP201 | Geraete-Abgleich Rest nach dem Urlaub: ~/.claude/settings.json am PC (Box-Fassung) + Laptop-Patches AP137 + La |
| AP207 | Nacharbeit aus dem Agent-Nutzungs-Audit (Logbuch #166/#167): 11 Vorbehalts-Zeilen auf hold, TE-Block-Sperre, B |
| AP208 | Wirkungskontrolle Auftrags-Typ-Router: hat er die Agent-Luecken wirklich geschlossen, und wie viele Fehlalarme |
| AP218 | Fit ausserhalb RTH: Intraday Bias (LBMA-Fix-Mechanik GC) -- staerkster Kandidat |
| AP219 | Fit ausserhalb RTH: Trend Following (London-Anker fehlt in der Engine) |
| AP220 | Fit ausserhalb RTH: Mean Reversion (Fix-Anker statt Session-VWAP) |
| AP226 | Wiederaufnahme #106: 22 Kandidaten wurden mit einer reinen Min-Size-Folgerung erschlagen, die seit 21.09. nich |
| AP227 | RVOL-Wege W18/W21/W23 (Sizing, Filter, Zeitfenster) aus dem 'Kapitel zu' loesen -- #068/#125 treffen diese Rol |
| AP230 | ES 24h-Cache hat 31 korrupte Quartals-Roll-Tage (Preise ~50-65 statt ~6.800) |
| AP239 | Hardware (Monitor/PC) im Dezember 2026 kaufen, NUR wenn BOS-Finanzplan gruen - geschaeftlichen Anteil ehrlich  |
| AP243 | Workbench Rest: NT8-Overlay deployen + Workbench/lab_ui auf die Box syncen |
| AP248 | FundedNext Flex 150k: echten Kaufpreis klaeren (Liste 483,99, Reset 278,99, Rabatt) und danach die FN-Groesse  |
| AP253 | claude-code-router: behalten (nur per Desktop-Verknuepfung) oder deinstallieren? Codex-Config ebenfalls vom Ro |
| AP255 | Workbench/Lineal: offene Punkte aus dem verdict-auditor (SR-Verhaeltnis, FN-Consistency, Gate v2 fuer Session- |
| AP262 | Lab-/Workbench-Note: Sharpe ueberzeichnet seltene Strategien (per-Trade-SR x sqrt(252)) -> Tages-Sharpe mit Nu |
| AP263 | Batch-Harness fuer Scratch-Nachlaeufe: Reihenfolge-Guard, fensterloser Start, Smoke-Check gegen Referenzbuch |
| AP264 | job_generator: Slot-Familie + reine Parameter-Nachbarn der Live-Beine erkennen (ein Vertreter je Wette, kein B |
| AP269 | Auto-Tickets auch auf der Box erzeugen, wenn der PC aus ist |
| AP270 | Ticket-Sync: Box-seitig atomar bzw. unter Sperre schreiben |
| AP289 | Entscheidung: zentrale firm_rules-Registry fuer RiskGuard und Kaefig-Rechnung (statt Firmenregeln doppelt in c |
| AP290 | Gate v4 Stufe 2: Schritt NT8-Port + Paritaets-Pruefung vor der Uebernahme |
| AP293 | RiskGuard: dynamischer Tages-Stopp nur in weekend_check simuliert, live nicht vorhanden |
| AP298 | guard_chain: Urteilsblock-Regex tolerant fuer Label-Suffix wie 'Urteil (je Gruppe):' |
| AP299 | Next-Buch/weekend_check: Herkunfts-Flag selection_leak fuer Beine aus Scratch-/Friedhof-Nachlaeufen |
| AP300 | gate_v4 Info-Spalten: Residual-Alpha (t_alpha, IR, dSR bei optimalem Gewicht) + dSR relativ zu eigenen Beinen |
| AP301 | Runner: Praemisse-Tod mit WF-Schattenlauf, wenn IS-BASE und volle Historie sich widersprechen |
| AP302 | strukturell-tot: Beweis-Objekt maschinenlesbar (structural_proofs.json), Erben nur innerhalb des Objekts |
| AP305 | Beinahe-Treffer aus #179 nachtesten: ORB-fade_nr7_honest, OPEXMOM als 4-Index-Familie, RTY-Gap-fade-Retune (EN |
| AP306 | MaxBookHost: Trades im Chart anzeigen (Historie mit Strategie-Namen) + Overlay mit Backtest-Trades je Bein |
| AP314 | test_ticket_lib unabhaengig vom Live-Sprintstand machen |
| AP324 | Vola-Regel fuer k und Stopp-Wiedervorlage maschinell pruefen (auto_check) |
| AP326 | Logbuch #180: Lehren als Code-Gates (Stempel in Discovery-Meta, Skript-Archivpflicht, Why-Behauptung, Kontroll |
| AP327 | Altwerte 150k im Kaefig + shrink058 als Faktor (Nachlauf AP323) |
| AP328 | PB3: Haltedauer der Stop-outs live in Sekunden messen + Mindestabstand zum Stop pruefen (Voraussetzung PB3 auf |
| AP332 | FFN: Netting-Falle gegenlaeufiger Beine (Millisekunden-Round-Trips) zaehlen und abfangen |
| AP339 | EMA-Leiter eingefroren: Forward-Tracking und Wiedervorlage (Korrelation zu PB3 < 0,4) |
| AP341 | Confirm-Job als eigener Job-Typ: Bestaetigungslaeufe duerfen nicht als neues Bein promotet werden |
| AP342 | Gate v4: Rausch-Statusfeld (pass_sd, 'unentscheidbar' nahe der Leitplanke) |
| AP348 | E8-Support fragen: Handelsbeginn 17:00 oder 17:15 CT, was zaehlt als 'illiquid market hours' |
| AP349 | firstbar_core: Target-Exit zahlt keine Slippage (gleicher Freitick wie AP223, eigene Kostenrechnung) |
| AP352 | Live-Grade-Karte: Kriterium fuer LIVE_EXTRA abnehmen, danach die 12 Validiert-Karten frisch rechnen |
| AP353 | Coast-Leg-Schalter: Beine abschalten bei Rest-Puffer unter 800 USD, erst OOS-Split rechnen |
| AP358 | Vola-Prognose fuer die Groessen-Entscheidung: Konzept entscheiden (6 Fragen), dann Schritt 0 Machbarkeit |
| AP359 | Optionsmarkt als Signalquelle pruefen (implizite Vola, VIX-Terminstruktur, Dealer-Gamma, 0DTE) |
| AP360 | Trial-Register von JSON auf eine abfragbare Datenbank umstellen (DuckDB oder SQLite) |
| AP361 | Bein-Gewichtung ueber Kovarianz pruefen statt gleiche Groesse je Bein |
| AP362 | Alte Hook-Sperren auch fuer das PowerShell-Tool (Box-Sync, enqueue, book_state) |
| AP368 | Gold Cross-Asset: Research-Rest (Silber-Vorlauf, Shanghai-Praemie mit Datenquelle, GLD-Zufluesse, Auktionskale |
| AP369 | Gold Cross-Asset: Feasibility fuer die langsamen Wege (Kopplungs-Zustand W21, US-Nachmittag nach Asien W41, Zi |
| AP370 | Gold Cross-Asset: liefern FN und FFN Echtzeit-Kurse fuer ZN und 6E am Konto-Feed (E8 am Konto nachsehen)? |
| AP372 | Gold: TD-12 als Traeger mit COMEX-Anker, dazu Bestaetigung durch ZN und 6E (einziger Gold-Traeger mit belegter |
| AP374 | tafel_lib: Episoden-Luecke (gap) durchreichen, CR2 auf der Differenz Gruppe gegen Rest rechnen, scipy-Abhaengi |
| AP388 | Gate v4: Passquoten-Leitplanke mit 12 Seeds und Schwellen-Hinweis, Power/MDE beim Vor-Gate als Info |
| AP392 | tempo_plan-Folgen: weekend_check auf Kaufrunde, Konto-Karten E8 150k 4 Payouts, FN-Kaefig pruefen |
| AP397 | Host-Module: falsche Template-Warnung beim Host-Start entfernen (naechster Deploy) |
| AP400 | Mega-Cap-Earnings-Kalender NQ (Gap-Fortsetzung nach Earnings NVDA/AAPL/MSFT/GOOGL/AMZN/META/TSLA) |
| AP404 | AP209-Folge: oos_cells mit Engine-Stempel, Auto-Rekonstruktion, Alarm, Nachlauf im Budget |
| AP405 | Gate v4 Stufe 3: Buch-Stufe auch auf der deploy_config pruefen (Minimum aus WF und deploy) |
| AP410 | Erste-Fassung-Spalte: Zusatzbeine aus der Linie eines Bestandsbeins je Trade statt je Jahr uebertragen |
| AP414 | Gold W46 Faktor-Rueckkehr (#184g): Mechanismus-Falsifier, laufen ZN und 6E selbst 09:00 bis 13:25 gegen ihre M |
| AP416 | tafel_lib: Flag 'Daten vorab gesehen', Info 'nichts gefunden je Zelle oder simultan', Kosten aus der Gebuehren |
| AP417 | qbt: explizit gesetzte Micro-Gebuehr unter der Tabelle warnen (Luecke nach AP384, aus #184) |
| AP421 | Wochenend-Entscheidung 18.10. (8): k2 neu pruefen mit frischen NQ-Daten |
| AP424 | MaxBookHost: Rueckfall auf das MNQ-Buch schliessen (instrument MNQ in den MNQ-Configs, unlesbare Config = Fehl |
| AP429 | Lehren 180/181 als Gates: Kanarie eod_flat_px, Sim-Filter, live_fill_check.py (AP426) |
| AP432 | Discovery: Sandbox-Modus im Runner (Lehre 179, nur Info, keine Promotion, kein Register) |
| AP437 | XAUUSD-Replikation zu Logbuch #189 auswerten (Download job-frei) |
| AP444 | leg_cells.py: Docstring ohne RTY-Gap (beim nächsten Code-Fix mitnehmen) |
| AP447 | Konten-Selbsttest: Zellen für die Abnahme (Test 2) als feste Testdaten einfrieren |
| AP448 | E8 150k vor dem Kauf: Flotte bei heutiger Vola, k1 gegen k2 |
| AP453 | Slack evtl. anschauen: Ersatz für Telegram und Handy-Meldungen |
| AP469 | Playbook T12: Uebergabe paper-edge zu Satzung, Eingangsfilter 'Index-Fokus' entkoppeln |
| AP474 | Playbook T17: Daten nachladen (Databento 2010 bis 2015, NT8-Export der 7 fehlenden Marktgruppen und Softs) |
| AP475 | Playbook T18: Reichweite-Felder in Ideen-Liste und Landkarte (Wiedervorlage-Bedingung, /K, Mehrtages-Form P) |
| AP477 | Playbook T20: Pflege (Research-Cache Z. 793, Gold-Karte Randbedingung 11, Altdateien, Fehlalarm, Landkarte neu |
| AP479 | Playbook T22: Anhang-Code (Banner je Anleitung, Block-IDs ^h01 bis ^h110, Korrekturen aus 4.2, volle Landkarte |
| AP482 | Wiedervorlage 01.11.2026: NQ_Gap-fade_hf: Monats-Blick auf die Drift (ohne Kapital) |
| AP483 | ELSTER: IBAN fuer Auszahlungen des Bundes beim BZSt melden |
| AP484 | ELSTER: Elektronische Bekanntgabe ab 2027 einstellen (Postfach oder Brief) |
| AP486 | Aufraeum-Bericht KW46: 4 Punkte in C:\Claude |
| AP487 | Wiedervorlage 16.11.2026: Logbuch #185a: RTY-Gap unentscheidbar, Bedingungen pruefen (NT8-Quelle AP313/AP199,  |
| review-2026-46 | Wochen-Review: Ampeln + Journal + Logbuch |

## Geparkt (10)

| Ticket | Titel |
|---|---|
| AP221 | Fit ausserhalb RTH: Relative Value (GC/SI, 6E/6B) -- datenblockiert |
| AP225 | Wiederaufnahme #119 (NOISE_ORB): Verdikt sagte selbst 'Groessen-, kein Qualitaetsproblem' -- bei 150k zeigt di |
| AP288 | FN 150k Challenge: RiskGuard-cfg mit Consistency-Deckel 0,36 vor dem ersten Trade anlegen (Ausloeser 2.880 $) |
| AP363 | Wiedervorlage Orderflow: nur noch Orderbuch-Tiefe offen, Delta ist erledigt |
| AP364 | Vola-Schaetzung fuer weitere Entscheidungen nutzen: Zeit bis 50k, Kaufzeitpunkt, Tagesstopp |
| AP373 | Gold Cross-Asset, NUR wenn eine Tafel-Zelle traegt: ein-weg, Engine-Umbau Fremdmarkt-Signal (S-GCX-1/-2/-3/-8) |
| AP379 | Hochstuf-Regel: Detailfragen 2 bis 6 entscheiden (Wochenende) |
| AP401 | USDA-Termine auf ZS/ZW (WASDE, Grain Stocks, Acreage 12:00 ET) - Wiedervorlage nach der ZS/ZW-Probe |
| AP445 | Be Obsessed: E-Mail-Liste und Kommentar-DM einrichten (erst nach schriftlicher Freigabe der Führungskraft) |
| AP450 | GEWO: Nebentätigkeit für Be Obsessed beantragen (Erweiterung der Genehmigung) |

## Lösch-Kandidaten (27), Entscheidung Max

| Ticket | Titel | Grund |
|---|---|---|
| AP118 | NQ_Momentum_d260818: DSR-Nachweis nachrechnen (0.11 bei rohem n, echte Spanne unklar) | Bein NQ_Momentum_d260818 ist durch PB3 ersetzt |
| AP121 | NQ_Momentum_d260818: BE-Komponente (be_trigger 0.5) ist auf der v2-Achse nicht von Null unterscheidbar, Why im | Bein NQ_Momentum_d260818 ist durch PB3 ersetzt |
| AP127 | eval_journal.json anlegen: Grundlage fuer die automatische Ueberwachung der AP107-Widerlegungsregeln | Eval-Phase vorbei, die AP107-Widerlegungsregeln galten der Eval-Wette |
| AP140 | Gold (GC) als erster Nicht-Index-Markt ins Discovery-Universum, danach CL; erster Durchlauf = die vier Buch-Mo | GC/CL seit 19.09. gerechnet, Gold-Tafel 13.10. |
| AP192 | Asia-Dir tmin_entry andere Uhr als die anderen drei Beine -- aktuell folgenlos, waere Falle bei buchweitem Tag | Dublette von AP329 (gleicher Asia-tmin_entry-Bug) |
| AP194 | Job-Generator pruefen: Queue laeuft seit 14.09.2026 leer (10x queue_empty), nach dem NM-Batch wieder 0 pending | Dublette von AP412 (Queue leer) |
| AP197 | Engine: eigenes Session-Fenster je Markt (GC 08:20/08:30 ET, CL 09:00 + EIA Mi 10:30, FX London 03:00-11:00) + | vermutlich in AP459 (Playbook T02 Markt-Uhr) aufgegangen, vor dem Loeschen kurz abgleichen |
| AP198 | UEBERTHEMA Neue Maerkte: was nie gerechnet wurde (6E/6B, ZS/ZW, AV/AC/AW auf GC/CL) + neue Mechanismen statt K | Ueberthema, inhaltlich im Alpha-Suche Playbook (AP457) und AP399 aufgegangen |
| AP204 | Schnellster Weg zu 50.000 $ Eigenkapital: E8 150k + FFN 150k abwechselnd, 1 Konto/Monat, Deckel 2.500 $ | FFN seit 26.10. zu, Plan E8 150k + FFN 150k ueberholt; Kauffrage laeuft ueber AP238/AP391 |
| AP261 | Box-Sync Engine-Stand 25./26.09.: Gap-Null-Schalter, ctl_null=NULL_MODES, book_gate_v3 + Runner-Neustart | Box seither mehrfach gesynct (zuletzt 26.10.), Stand 25./26.09. ueberholt |
| AP272 | Wiedervorlagen aus dem Strategie-Logbuch als maschinenlesbare Liste (fuer Auto-Tickets) | Dublette von AP466 (Playbook T09, Wiedervorlage nach Bedingung) |
| AP297 | auto_check: maschinenlesbares Wiedervorlage-Register (Buch-Beine-Set, md5-Stempel, Datum) | Dublette von AP466 (Playbook T09, Wiedervorlage nach Bedingung) |
| AP310 | NT8-Port 7er-Buch: PB3, NQ-OpenDrive, VWAP-Pullback, ORB2, RTY-Gap (je Bein Port + Paritaet, dann einzeln ins  | laut Notiz 15.10. kein Port-Rueckstand mehr, Rest sind Wochenend-Entscheidungen |
| AP331 | FFN: Asia-Stop-outs der ersten Minute in Sekunden messen (Databento, 4 Minuten), Voraussetzung Asia auf FFN | FFN seit 26.10. zu |
| AP334 | FFN als eigenes Firmenmodell in tempo_plan/weekend_check + Buch je Konto, dann in book_state plan.accounts | FFN seit 26.10. zu |
| AP335 | FFN Funded: T1-News-Sperre vor dem Entry statt Flatten danach | FFN seit 26.10. zu |
| AP337 | weekend_check: Gluecksbereinigung mit N_eff statt N_family + Kalibrierungszeile (Stufe 2 Herkunft) | Gluecksbereinigung durch die Erste-Fassung-Pruefung (AP275) ersetzt |
| AP377 | FN1 und FN2: Puffer nur noch 1,4 Tagesschwankungen, weiterlaufen lassen oder entlasten? | betraf die FN-Challenges, die am 10.11. bestanden und ersetzt wurden |
| AP378 | Funded-Wechsel vorbereiten: Konto-Nummer, RiskGuard-Ziel, Register und Karte | Funded-Wechsel am 10.11. erfolgt, Konten-Tabelle laeuft |
| AP420 | Wochenend-Entscheidung 18.10. (3): LD01-Vergleich PB3 doppelt bei VIX unter 16 vor dem NT8-Port | Frage am 22.10. beantwortet, LD01 am 24.10. entschieden |
| AP473 | Playbook T16: FFN-Produktliste per Support (ZN/ZB, FDAX, Micro-Ag, Silber, Kupfer, M6E handelbar?) | FFN seit 26.10. zu |
| AP485 | Aufraeum-Bericht KW45: 2 Punkte in C:\Claude | durch den Aufraeum-Bericht KW46 (AP486) ueberholt |
| next-week-2026-42 | Next-Week-Buch (2026-42) bewerten: Auto-Promotionen aus Discovery uebernehmen oder verwerfen | Woche 42 vorbei, Wochenend-Pruefungen 17./24.10. erledigt |
| review-2026-42 | Wochen-Review: Ampeln + Journal + Logbuch | alte Wochen-Review, Woche vorbei |
| review-2026-43 | Wochen-Review: Ampeln + Journal + Logbuch | alte Wochen-Review, Woche vorbei |
| review-2026-44 | Wochen-Review: Ampeln + Journal + Logbuch | alte Wochen-Review, Woche vorbei |
| review-2026-45 | Wochen-Review: Ampeln + Journal + Logbuch | alte Wochen-Review, Woche vorbei |

Löschen (nach OK, ganz oder teilweise), im Engine-Ordner:

```
python ticket_tool.py delete AP118 AP121 AP127 AP140 AP192 AP194 AP197 AP198 AP204 AP261 AP272 AP297 AP310 AP331 AP334 AP335 AP337 AP377 AP378 AP420 AP473 AP485 next-week-2026-42 review-2026-42 review-2026-43 review-2026-44 review-2026-45
```

Im Lab findest du sie über die Suche `label:loesch-kandidat`.

## Was nebenbei auffiel

- **E8 braucht bis Di 17.11. einen geschlossenen Trade** (7 Tage Inaktivität, steht in der Stand-Datei, ohne eigenes Ticket).
- FN-HFT-Grenze ist weiter unbekannt (Stand-Datei). Davon hängen AP328 und AP332 ab, die bisher nur für FFN galten.
- Die Box kennt die neuen Stufen im Code erst nach dem nächsten Engine-Sync bzw. dem Ticket-Board-Einspielen (AP267). Dort läuft heute nichts, das nach Prio sortiert (Fokus-Planer erst nach AP455 scharf).

Werkzeug: `engine/archiv/einmal/_neubewertung_tickets_20261116.py` (Bewertung je Ticket als Tabelle im Code, eine ticket_lib-Transaktion mit Sperre, Backup und Ereignis-Log, davor und danach Abgleich mit der Box).
