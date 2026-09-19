# Friedhof-Analyse — gemeinsames Briefing für alle Extraktions-Agents (17.09.2026)

## Auftrag von Max
"Mach eine Analyse über unsere Friedhöfe, ob es in unseren Friedhöfen nicht doch noch brauchbare Edge geben könnte (mit Erweiterungen), und analysiere, wo wir Fehler begangen haben könnten/haben, um Dinge nicht gefunden/getestet zu haben." Max will das SEHR genau und intensiv.

Du bist EIN Extraktions-Agent von mehreren. Du lieferst Rohmaterial, keine Endurteile. Die Hauptsession und danach Quant-Team/verdict-auditor bewerten. Sei vollständig, nicht knapp: lieber 60 Zeilen Tabelle als 10.

## Kontext: was bereits bekannt ist (nicht neu entdecken, aber als Prüfraster benutzen)
Der Vault hat schon einen Bestands-Durchlauf (Logbuch #137, AP116, 30./31.08.2026): 46 Urteile geprüft, 13 voreilig. Und #139 (01.09.): Pipeline suchte pro forma (nur tsmom/maband/orb konnten deploy_ready werden; "neues Bein" hat NIE funktioniert, Spearman(Buch-Score, Trades/Jahr) = -0,81; Referenzbuch schlechter als sein 4-Bein-Subset). Diese Befunde sind Grundwissen. Deine Aufgabe ist, DARÜBER HINAUS systematisch alles zu erfassen.

## Bekannte Engine-/Pipeline-Fix-Zeitleiste (Urteile VOR einem Fix stehen auf einem alten Stand — das ist der wichtigste Prüfpunkt je Todesurteil)
- 09.08.2026 #066/#067: ORB-Breakout hatte Look-ahead (orb_exec="book"); ehrlich = "close"/"stop_honest". Urteile "gut" für ORB-Breakout VOR 09.08. sind wertlos; Kills danach ehrlich.
- 10.08.2026 #072/#074/#075: zwei Rechenfehler, die ALLE Vault-Zahlen betrafen; Engine-Audit 5 Bugs (u.a. rv.py, MAE-Doppelzählung AP73, Limit-Entry-Slippage). Alles vor 10.08. = alte Engine.
- 16.08.2026 #106: Zielfunktion v2 "Passquote je Eval / $ pro funded" ersetzt "P(funded) pro Zeit"; Min-Size 1 Kontrakt/Bein. JEDE Buch-Ablehnung durch Auto-Fit VOR 16.08. lief auf dem alten Kriterium.
- 18.08.2026: Discovery-Runner v2 + Register (Backfill 1390 Alt-Trials). Buch wechselte mehrfach (Beine _d260818 etc.).
- 23.08.2026: Kostenbasis bis dahin falsch (#137 Punkt 4). 24.08. 18:40: corr_book-Ersatz-Bug gefixt (jeder Ersatz-Kandidat scheiterte vorher an sich selbst, #129) + Buch-Drift-Wächter. "schlechter"-Verdicts 23./24.08. gegen falsches Buch.
- 30.08.2026 #135: Roll-Garbage in den 1m-Parquets — 83 Fremdkontrakt-Sessions entfernt, alle vier 1d-Ratio-Serien repariert. ALLE Trials vor 30.08. liefen auf kontaminierten Daten.
- 31.08.2026 #137: rv.py gap_div-Bug gefixt (r=-349 Einzeltrade); job_generator-Jobs liefen bis dahin mit WEICHEREN Gates (top5 0,60/boot_p 0,85 statt 0,50/0,90) — 324 Generator-Jobs nie nachgerechnet.
- 01.09.2026 #139: Modus-Loch (nur tsmom/maband/orb deploy-fähig), replaces_leg-Namens-No-Op ("NQ_Momentum" statt "NQ_Momentum_d260818", 39 Läufe rechneten Buch+Duplikat, 84 von 138 Ersatz-Jobs mit toten Namen), Rauschmaß hypot statt gepaart, null_ceiling mit sr_std des Jobs statt Theorie. Lost-Update-Fenster in queue.json (Jobs verschwanden still).
- 06.09./16.09.2026 #145/#157: Null-Schalter für ts_reversal/last_hour/asian/vwap_pullback + Kalender-/DIX-Gates gebaut (Laptop), erst 16.09. auf die Box deployt. Bis dahin konnten die vier BUCH-Modi nie deploy_ready werden.
- 09.09.2026 #146: Prämissen-Gate (Stufe 0) war weicher als Grid-Gates → Fix. Buch-Marginal-Rauschmaß: echte Streuung 2,6-3,7pp statt 0,24pp; neues Bestätigungs-Gate verlangt real >5pp. max_book_evals 6→30 (→ später 3).
- 14.09.2026 #153: sharpe_ann_daily annualisiert nur Handelstage mit √252 → Inflation bis 2,5×, Zufallsdecke "measured" damit teils absurd streng; Placebo mb_rand_level würfelt Seite mit (Kontroll-Arm kaputt); trail_profile tr1.5d1.0 Phantom-Achse.
- 15.09.2026 AP161: Backtest-Exit auf 15:55 wie live umgestellt (sigcore). 16.09. #156: Šidák-Korrektur, Schwelle heute k_eff=2 → ~5,4pp; 0 von 600 Result-Dateien hätten es je geschafft. 16.09. #157: mb_vwap_dnorm="atr" war Tages-ATR20 statt Bar-ATR14 (#097-Maß) → Prämissen kollabierten auf 3 Trades; neues atr_bar. Bank-Enqueue dedupt über Job-ID → Reruns unter alter ID werden still übersprungen (≥7 Bank-Jobs betroffen).

## Register-Stand (17.09.2026)
63.727 Trials: tsmom 38.998, maband 16.406, firstbar_ematrail 2.880, ts_reversal 1.031, rv 739, i2 547, regime_gate 530, last_hour 463, gap 397, asian 298, cal 200, orb 184, vwap_pullback 155, continuation 96, vix_bias 73, pivot 52, orb_std 45, flip 24, event_study 24. Märkte: NQ 35.511, RTY 11.547, ES 8.455, YM 7.856. Survivors 4.098. Queue: 902 Jobs, 474 done, 427 premise_failed (davon tsmom 174, maband 166, rv 50), 0 Kandidaten seit 24.08., Queue seit 17.09. 01:33 leer.

## Dein Output-Format (Markdown-Datei, Pfad steht in deinem Auftrag) — je Grabstein EINE Zeile in dieser Tabelle:
| # | Name/ID | Familie | Mechanismus (1 Satz) | Markt | Datum Urteil | Urteil (tot/abgelehnt/neutral/Bank/zurückgezogen) | Beweisbasis (n Configs/Varianten, IS/OOS, welche Gates, Trades) | Engine-Stand beim Urteil + welche SPÄTEREN Fixes das Urteil berühren könnten | Was NICHT getestet wurde (Achsen: Gegenseite, andere Märkte, Exit/Stop, Bestätigung, Zeitfenster, Regime) | Wiederbelebungs-Potenzial (hoch/mittel/niedrig) + 1-Satz-Grund | Fehlerklasse (siehe unten) | Quelle (Logbuch-Nr./Datei/Zeile) |

Fehlerklassen (mehrere möglich):
F1 = Urteil auf alter Engine/alten Daten (vor einem der Fixes oben), nie nachgerechnet
F2 = Urteil unter altem Kriterium (Zeit-Score/Auto-Fit vor #106) statt v2-Passquote
F3 = zu wenig Varianten (< 10 Implementierungen, nur 1-2 Configs, nur eine Seite, nur ein Markt)
F4 = Gate-Artefakt (top5/freq/n_min-Gates bei Filtern, Prämisse zu hart/weich, Zufallsdecke aus Job-sr_std, Sharpe-Inflation)
F5 = Prior/Story-Kill statt Test (strategy-auditor oder Session hat verworfen, ohne zu rechnen)
F6 = Tod durch Pipeline-Bug (corr_book, replaces_leg-No-Op, KeyError in Prämisse, n=0, Lost-Update, Modus ohne Null-Schalter → skipped_required)
F7 = Falscher Kontroll-Arm / falsches Maß (Placebo würfelt Seite mit, PF statt $/Trade, Sharpe-Inflation, dnorm falsches Maß)
F8 = Karten-Status verdeckt Mechanismus (ein "Getötet" für mehrere Mechanismen, Doku sagt tot, Code/Buch sagt lebt)
F9 = Nie eingereiht / liegengeblieben (jobs_proposed, hold-Flag, CVD_ENABLED=False, Ticket offen)
F10 = Mechanismus tot, aber Nebenbefund/Messfund nie weiterverfolgt (z.B. "Richtungsinformation ist ein NQ-Befund", "Konstant-Arm raus", Spiegel-Trick nicht geprüft)
F0 = Urteil hält sauber, nichts offen

Nach der Tabelle: ein Abschnitt "Muster" (welche Fehlerklassen häufen sich, in welcher Phase), ein Abschnitt "Top-10 Wiederbelebungs-Kandidaten aus meinem Teil" mit konkretem Erweiterungs-Vorschlag (welche Achse/welcher Test fehlt), und ein Abschnitt "Offene Nebenbefunde/Messfunde, die nie weiterverfolgt wurden".

Regeln: Nur lesen, nichts ändern. Keine runner.log/results-Volltexte. Zitiere Logbuch-Nummern. Wenn ein Urteil sauber hält, trotzdem eine Zeile mit F0 (damit die Vollständigkeit prüfbar ist). Schreibe auf Deutsch. Keine Gedankenstriche.
