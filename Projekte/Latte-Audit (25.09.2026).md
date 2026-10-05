---
tags: [projekt, discovery, gate, analyse]
date: 2026-09-26
status: Entscheidungen bei Max
---

# Latte-Audit (25./26.09.2026)

Frage von Max: *„Wir finden Alpha, aber nutzen es nicht, weil es nicht gut genug fürs Buch ist. Ist unsere Messlatte zu hart?"*

Gemessen per Workflow (20 Agents): Trichter über alle 1.041 Discovery-Jobs, Gate-Inventar mit Herkunft, die eigenen Beine durch die **komplette** Kette, Mathematik (Zufallsdecke, Buch-Hürde, UND-Kette), Statistik (Power je Gate per Bootstrap-Parallel-Historien, Fehlalarm per Nulldrift-Zwillingen), 12 spät gestorbene Funde adversarial nachgerechnet, `pipeline-auditor` + `verdict-auditor` gegen die #106-Falle. Skripte und Zahlen: `engine/_scratch_latte/`. Nichts an Engine oder Buch geändert. Verwandt: [[Testphase Juli-Modus]] (Teil B), [[Discovery-Runner v2]], CLAUDE.md Abschnitt „Gate v2", [[Friedhof-Analyse (17.09.2026)]].

## Kurzurteil

Die Latte ist nicht einfach zu hart, sie ist schief gebaut: hinten blockt sie so stark, dass nicht mal unsere eigenen drei Beine durchkämen (Chance für eine echte Edge in Buch-Bein-Größe rund 0,1 % je Job), und gleichzeitig lässt sie Rechenfehler, Kopien unserer eigenen Beine und reine Long-Drift erstaunlich weit kommen. Verlorenes Alpha ist bei den 12 gegengeprüften späten Toden nicht nachweisbar: alle waren im Ergebnis richtig, vier davon aber aus dem falschen Grund. Das Problem hat zwei Seiten. Die Kette ist blind, also beweisen 0 Funde gar nichts, und die Suche lief im September zu 93 bis 97 % auf zwei alten Mechanismen statt auf neuen Ideen. Selbst mit perfektem Gate bringt ein viertes Bein eher 3 bis 9 Monate als Jahre.

## Urteil je Stufe

Stempel: Buch 91c972fe (3 Beine), Register 68.112 Trials, Engine-Stand 25.09.2026. Einordnung: **(a)** zu hart, **(b)** misst die falsche Größe, **(c)** passend, das Problem liegt im Suchraum. Dazu kommt **(z)**: zu weich oder kaputtes Messwerkzeug.

| Stufe | Urteil | wichtigster Beleg | Vorschlag | Preis in Fehlalarmen |
|---|---|---|---|---|
| Prämisse | passend (c) | 519 von 1.041 Jobs sterben hier, 462 davon mit IS expR ≤ 0. Gate v2 rettet keinen. Power 0,88 bei wahrer SR 0,6 | so lassen. min_n 60 an min_trades 30 koppeln, die 18 Fehler-Jobs von Hand sichten | keiner |
| Stufe 1 Kern (n ≥ 30, Sharpe-t ≥ 2, Trim 1 %) | passend (c) | 4 von 5 eigenen Beinen bestehen, Gap-fade stirbt ehrlich (t 1,09). Rauschen je Config ≤ 0,4 %. Gate v2 hat hier +5 bis +10 pp Power gebracht | so lassen, nicht zurückdrehen | keiner |
| Stufe 1 Rest (IS, OOS, last3y, Kosten-Stress, Bootstrap, Dollar) | passend, Kosten-Stress unklar | Bootstrap und Dollar töten 0 % zusätzlich (redundant). Kosten-Stress kostet 6 bis 13 % Power, gegen Zwillinge wirkt er gar nicht | Bootstrap nur noch als Info. Kosten-Stress erst gegen echte MNQ-Fills kalibrieren, dann ggf. den OOS-Teil streichen | gering |
| Plateau | passend, aber blind für Spitzen (z) | tötet nie. GAPFADE-RT (lo 0,5), VWAP-Touch 0,2 und Momentum rev_signal_min 15 sind lokale Spitzen und gingen durch | zusätzlich den Median der Nachbarn bewerten statt nur die Basis | Verschärfung spart Fehlalarme |
| Top-8-Deckel (Picks nach OOS-Sharpe) | unklar, Sichtbarkeits-Bug | 57 % der Survivors in Jobs ohne Kandidat wurden nie gegen das Buch gerechnet und sehen trotzdem aus wie "kein Fund". Der VWAP-Exit war Platz 1 nach OOS-Sharpe, aber Platz 25 nach Gesamt-SR (OOS verbrannt) | Feld "nie gemessen" in Meta und Inbox. Die ~20 Jobs mit bestem Pick ≥ -2 pp komplett nachbewerten (0 neue Trials). Nicht mehr nach OOS ranken | keiner, kostet nur Rechenzeit |
| Zufallsdecke global | (a) + (b) | Decke 1,32 bis 1,67, alle drei Beine (0,79 bis 1,11) liegen darunter. Power 1 bis 24 %. Seit 15.09. liegen 0 von 366 Survivors darüber. Streuung = max(Theorie, gemessen) bläht die Decke in 36 % der Jobs auf über 2,0 | sofort: Streuung nur aus der Theorie (reiner Bug). Den globalen Hartblock erst nach der Placebo-Kampagne durch eine Familien-Decke (Modus × Markt × Why) ersetzen, die nur noch als Info läuft | gegen Rauschen fast nichts (< 0,1 falsche Kandidaten auf 1.041 Jobs). Gegen die Zwillings-Null aber 0,16 auf 0: ohne Decke trägt Gate v2 allein, und dessen echter Fehlalarm liegt bei 5 bis 12 % |
| Selektions-Veto (PBO "kaputt") | (a) + (b), misst Rangstabilität statt Edge | Synthetik: ein echtes flaches Plateau wird 22 von 30 Mal "kaputt" gestempelt, Rauschen 27 von 30. Asia hat PBO 71 %, VWAP gilt als "kaputt", obwohl alle Configs im OOS profitabel sind | Veto an den Reality-Check-p koppeln, PBO nur als Info | klein, der Reality-Check fängt Rauschen. Synthetik aber nur N = 30 (±16 pp) |
| Stufe 2 Buch-Marginal (Δ Passquote, OOS-Fenster, 50k Min-Size) | (b), dadurch (a) | 92,6 % der Picks liegen unter 0, der Median von -6,2 pp liegt im Null-Band. Das Passquoten-Kriterium ist ≈ doppelt so streng wie das Zeit-Kriterium. Ohne 36-Monats-Zensur sind alle 3 echten Beine negativ. LastHour fällt im OOS durch (-0,8). Gemessen wird bei x ≈ 0,5 statt am gekauften Punkt 150k k2 | auf Zeit bis 50k umstellen: ΔSR bzw. Δ E[Zeit] gepaart gegen Nulldrift-Zwillinge, mit Shrinkage 0,58 und Letzte-3-Jahre-Spalte, am Betriebspunkt 150k k2 (AP246). Volle Historie erst nach dem Placebo | hoch ohne Zwilling: der alte Zeit-Score sagte bei 2.114 von 2.114 "schneller" (#106). Eine Tempo-Stufe ließe VWAP-PB (#161) auf voller Historie wieder rein |
| Ersatz vs Original | passend (c) | die alte weiche Regel ließ 28 von 38 Kandidaten durch, die das Buch absolut verschlechterten | so lassen | eine Lockerung brächte genau das zurück |
| Gate v2 Bestätigung (10 Zwillinge, α 0,02) | unklar, in beide Richtungen falsch | Zu wenig Power: Momentum 18 %, Asia 6 %, LastHour 22 % im OOS bzw. 75 % voll. Gleichzeitig zu weich (z): der echte Fehlalarm liegt bei 5,4 % (OOS) bzw. 12 % (voll), weil die Picks nach OOS-Sharpe ausgewählt werden. Der Zwilling fängt weder Selektion an Filtergrenzen (GAPFADE-RT) noch Long-Drift (AS-07, ToM). Der Code rechnet Šidák über 8 Picks, beschlossen war k = 1 je Mechanismus. Ein placebo_log existiert nicht | Placebo-Kampagne mit ganzen Null-Grids und derselben Top-k-Auswahl, die Schwelle daraus ableiten. Zwilling v2: gleicher Long-Anteil wie der Kandidat, Filtergrenzen mitwürfeln | heute schon 2,5 bis 6 mal über nominal. Jede Lockerung ohne Placebo macht das schlimmer |
| Kontrolle periods | unklar, echter Widerspruch | tötet LastHour und Asia wegen Rauschen in 2016 bis 2019 (t -0,09 / -0,14), fängt aber 52 % der Momentum-Zwillinge | asymmetrisch machen: nur tot, wenn die junge Epoche ≤ 0 ist oder beide Epochen mit t über 2 gegenläufig sind. Vorher per Zwillings-Simulation prüfen | ungetestet, das muss die Simulation zeigen |
| Kontrolle symbols (2 von 4 Märkten) | (a) als Pflicht | tötet Momentum und VWAP (beide NQ-spezifisch). Das ist eine Replikationspflicht, keine Mehrfachtest-Korrektur | nur als Info führen, Pflicht nur dann, wenn der Job selbst über mehrere Märkte gesucht hat | der Schutz vor VWAP-PB fällt weg, den müssen dann Stufe 2 und der Zwilling tragen |
| Kontrolle sides | passend, bis der Zwilling driftbereinigt ist | kostet 27 bis 46 % Power (Bootstrap). AS-07, ToM und i2-VWAP zeigen aber genau das Drift-Loch, das sides abfängt (#098) | erst den Zwilling fixen, dann auf "Short-Seite nicht signifikant negativ" (t > -1) umstellen | schützt heute gegen Long-Beta |
| Kontrolle delay | passend, mit Umsetzungsfehler | an 15 Negativkontrollen kalibriert. Der Momentum-Fail ist ein Artefakt (der Test verschiebt das Signalfenster mit, z_sign +6,3). LastHour mit z_sign -6,6 ist ein echter Befund | für ts_reversal und last_hour nur die Fill-Bar verschieben. LastHour-Slippage live prüfen | keiner |
| Kontrollen null, corr_book | passend (c) | alle Beine bestehen, corr_book hat Momentum-Klone abgefangen (0,71 bis 0,97) | so lassen | entfällt |
| übersprungene Pflichtkontrolle = nie promotbar | Bug | ctl_null kennt gap, orb und cal nicht, obwohl diese Modi einen Null-Schalter haben. 135 von 1.041 Jobs sind dadurch strukturell gesperrt | Modusliste angleichen. rv und i2 gesperrt lassen, bis rv.py gefixt ist | keiner für gap/orb/cal. rv jetzt zu öffnen wäre gefährlich |
| Messwerkzeuge (neu aus der Gegenprüfung) | (z) zu weich | rv.py prüft den Stop auf dem Close und füllt am Stop-Preis: ~0,25 R je Trade geschenkt, das ist die ganze LL-Edge. vwap: flatten 300 ohne Entry-Sperre ergibt 47 % Phantom-Trades. SR vor #153 ist um √(252/tpy) zu hoch (Faktor ~3 bei 28 Trades im Jahr). leadlag-USD rechnet mit 2 $ statt 5 $ je Punkt | vor jeder Lockerung fixen, danach Engine-Regression | diese Fehler SIND Fehlalarme |
| Kette gesamt bis promote_next | (a) als UND-Kette | Power ≈ 0,1 % je Job (SR 0,6) bzw. ≈ 1 % (SR 1,0). 0 von 3 Buch-Beinen kommen durch. Physikalische Grenze bei 10,6 Jahren und 2 % Fehlalarm: 22 % bzw. 74 % | nach den Fixes einen Kalibrierlauf mit Positiv- und Negativsatz fahren | Abnahme: höchstens 1 von 5 Negativen kommt durch |

## Ging Alpha verloren?

## Kurz: nachweislich verloren ist nichts. Ob woanders was verloren ging, kann man weder ausschließen noch sehen.

### Die 12 spätesten Tode, adversarial nachgerechnet (aktuelle Engine, aktuelles 3-Bein-Buch)

| Fall | was es wirklich war | Tod berechtigt? | Zeit bis 50k, falls echt |
|---|---|---|---|
| GAPFADE-RT (RTY Gap-Fade Retune) | Filterspitze bei 0,5 bis 0,6 ATR, 52 % der R-Summe aus diesem Band. OOS war vorab angeschaut. Der SR von 3,22 war das alte Maß, ehrlich sind es 0,92 | ja, aber falscher Grund | roh 2 bis 4 Monate schneller, mit Plateau-Median nur 1 bis 1,5 (Rauschen) |
| TE-06 (Momentum mit festem 3R-Ziel) | die Long-Hälfte unseres Momentum-Beins. Das Ziel kostet 0,2 R je Trade | ja | ~47 Tage langsamer |
| Asia-Exits (Stop 0,4625) | Kopie des Live-Beins, Korrelation 0,95, 551 $ weniger Gewinn | ja | keine Änderung |
| AS-07 (MA-Abstand sigma) | Long-Drift. Der Richtungsmehrwert beträgt +0,017 ± 0,048 R. Den Zwilling besteht es nur über Beta | ja | -2 bis +5 Monate |
| LL-04 (NQ führt ES) | Stop-Artefakt in rv.py, ehrlich gerechnet expR -0,058 | ja, sogar zu spät | ehrlich langsamer |
| Turn-of-Month NQ | Effekt nur als Regime ab 2024, im IS nichts da. Das OOS war vorab angeschaut | ja, aber falscher Grund | roh 6 Monate schneller, mit Shrinkage 4 bis 9 Monate langsamer |
| ts_momentum Exits | echte Edge, aber es ist das Momentum-Bein mit größerem Stop (1,84-fache Vola) | ja | ~17 Monate langsamer |
| TN-04 (LastHour-Variante) | unser eigenes Bein (Korrelation 0,89). Die damaligen -10,4 pp waren ein Messfehler (Namensbug, Zusatz statt Ersatz). Korrekt nachgerechnet trotzdem schlechter | ja, aber falsche Zahl | ~3 Monate langsamer |
| i2 VWAP-Pull | Short-only-Subgruppe an einer Spitze, repliziert nicht auf ES/YM | ja | 0 nach Shrinkage |
| VWAP-PB Exit | 47 % Phantom-Trades, über das OOS ausgewählt | ja | roh 0 bis 3 Monate, nach Shrinkage 0 |
| gen_gap_RTY (Gap-Fade 0,5 bis 1,5 ATR) | vierte Retune-Generation, selektionskorrigiert nur p ≈ 0,05 | Ergebnis ja, aber falsche Stufe | 2 bis 3 Monate von ~54, **unentscheidbar** (bräuchte 24 bis 33 Jahre Daten) |
| LL-01 (NQ führt ES) | rv.py-Artefakt, was übrig bleibt, ist verdünntes Momentum | ja | ehrlich ~4 Monate langsamer |

**Bilanz:** 12 von 12 Toden waren im Ergebnis richtig, 4 davon aus dem falschen Grund. Hinter den Fällen steckt:
- 4-mal ein Wiederfund unserer eigenen Beine,
- 3-mal ein Messartefakt (rv-Stop 2-mal, Phantom-Trades 1-mal),
- 3-mal Long-Drift oder Regime,
- 2-mal ein dünner RTY-Gap-Fade.

Beide "echt wahrscheinlich"-Fälle sind Edges, die das Buch schon erntet. **Der Obergrenze-Verlust, der sich sichtbar machen lässt, ist der RTY Gap-Fade mit 2 bis 3 Monaten auf ~54, und das liegt im Rauschen.** Bei der Frage nach Alpha, das nicht ins Buch passt, war die Latte an diesen Fällen eher zu weich als zu hart: Nur wegen aufgeblähter Sharpes, rv-Fills und Phantom-Trades kamen die Fälle überhaupt bis Stufe 2.

### Was die Gegenprüfung nicht sehen kann
Die Kette hat für eine echte Edge in Buch-Bein-Größe eine Power von ≈ 0,1 % je Job. Bei 1.041 Jobs passt die beobachtete 0 zu 0 echten Mechanismen genauso gut wie zu etwa 20. Falls etwas verloren ging, dann früher, also an Decke, PBO oder Stufe 2, und dort nie einzeln gemessen. Das klärt nur der Kalibrierlauf mit Positiv- und Negativsatz (Vorschlag P5), nicht noch mehr Einzelfälle.

### "Wir finden Alpha" hält so nicht
- Die 14.336 "Alpha-Configs" aus dem Trichter-Strang sind überzeichnet. Für Jobs vor dem 16.09. stehen die gespeicherten SR im alten Maß (√(252/tpy) zu hoch), damit sind Sharpe-t, Decken-Vergleich und die 6.037 nachgerechneten v2-Survivors nur Obergrenzen.
- 679 von 1.216 neuen Picks gehören zur Momentum-Familie.
- 11 der 12 neuen Picks mit Buch ≥ 0 sind Lead-Lag, und genau das ist das rv.py-Artefakt.

### Widersprüche zwischen den Strängen, aufgelöst
- **LL-01 als "bester neuer Fund" (Trichter) gegen Fill-Artefakt (Gegenprüfung):** Die Gegenprüfung hat recht. Sie trifft die Engine exakt (n 1.344, expR 0,207) und zeigt, dass ehrlich gefüllt -0,041 R übrig bleiben.
- **Gate v2 "am besten kalibriert, Power 0,53 bis 0,62" (Inventar) gegen Auditor 2:** Auditor 2 hat recht. In der Vault-Notiz (Testphase Juli-Modus, Tabelle Z. 188 bis 190) ist das die Zeile für α 0,10. Bei α 0,02 sind es 0,25 bis 0,53, gemessen an den eigenen Beinen nur 6 bis 22 % (OOS). Dazu weicht der Code vom Beschluss ab (Šidák über 8 Picks statt k = 1).
- **Top-8-Deckel "zu hart" (Inventar, Auditor 1) gegen "unklar" (Auditor 2):** Auditor 2 hat recht, eine Zählung ist kein Beleg. Die Sichtbarkeitslücke ist aber real.
- **periods zu hart (eigene_beine) gegen passend (statistik):** Beide messen etwas anderes, beide stimmen. Entscheiden muss die Zwillings-Simulation mit asymmetrischer Regel.
- **sides zu hart (statistik) gegen passend (Auditor 2):** Die späten Tode (AS-07, ToM, i2) stützen Auditor 2, denn sides deckt das Drift-Loch des Zwillings ab. Also erst den Zwilling fixen, dann weicher machen.
- **Decke "kauft fast nichts" (statistik) gegen "0,16 auf 0 gegen Zwillinge" (Auditor 2):** Beides stimmt. Die Decke ist heute das Einzige, was die Fehlkalibrierung des Zwillings überdeckt, darf also erst nach der Placebo-Kampagne weg.
- **Namensbug beim Ersatz:** Ist nur historisch. Im Code ist er seit 24./27.08. gefixt (discovery_runner.py Z. 254 bis 287, selbst nachgesehen), betroffen sind nur alte Urteile.

### Buch-Lücke der drei Kandidaten, die überhaupt noch offen sind
- **RTY Gap-Fade (gen_gap_RTY):** hängt an Stufe 1 (Selektion, unentscheidbar). Zwei ehrliche Wege: ein einzelner Gate-v2-Lauf gegen das aktuelle Buch mit 0 neuen Parametern, oder Forward-Paper mit der eingefrorenen Config. Keine weitere Retune-Runde.
- **Turn-of-Month:** hängt an der Beweislage (Regime seit 2024). Forward-Test ab 01.10.2026, für z 2 braucht es ~75 neue Trades (~1,6 Jahre).
- **Lead-Lag (LL):** erst der rv.py-Stop-Fix, dann einen Null-Schalter für rv bauen, dann die ganze rv-Familie neu rechnen. Ins Next-Week-Buch geht davon heute nichts.

## Vorschläge (priorisiert, nichts umgesetzt)

## Einordnung zuerst
- **(a) zu hart:** globale Zufallsdecke als Hartblock, PBO-Veto, symbols als Pflicht, die UND-Kette insgesamt, Stufe 2 im OOS-Fenster.
- **(b) misst die falsche Größe:** Stufe 2 misst Passquote bei 50k Min-Size statt Zeit bis 50k am Betriebspunkt. PBO misst Rangstabilität statt Edge. Die Decke zählt korrelierte Trials als unabhängig. delay verschiebt bei ts_reversal das Signalfenster.
- **(c) kein Alpha da:** Die späten Tode sind Wiederfunde, Artefakte und Regime, und der Suchraum sitzt zu 93 bis 97 % auf tsmom/maband. **Das ist der größere Hebel.**
- **(z) zu weich:** rv.py-Stop, vwap-Phantom-Trades, SR-Maß vor #153, leadlag-USD, Šidák über OOS-selektierte Picks, der Zwilling ohne Drift- und Filterbereinigung, Plateau ohne Spitzenerkennung.

**Reihenfolge ist Pflicht:** Erst (z) zumachen, dann (a) und (b) lockern. Sonst wäre LL-01 heute der "beste Fund".

## Priorisierte Änderungen (nichts davon angewandt)

**P0: Messfehler fixen (zu weich), vor jeder Lockerung**
1. `engine/rv.py`, Stop-Schleife: Stop intrabar gegen High/Low prüfen wie in `qbt.py` (ab Z. 305), mit Gap-Fill. Wirkung: nimmt ~0,25 R je Trade Scheinedge aus allen ~739 rv-Trials. #106: reiner Messfix, danach `engine-regression-tester`.
2. `engine/vwap_pullback.py` Z. 78/79 und `job_generator.py` (Exit-Sweeps): `no_new_entry_min` automatisch mit `flatten_min` mitziehen. Wirkung: keine Phantom-Frequenz mehr (bisher 47 % der Trades).
3. `usd_series` für leadlag: 5 $ je ES-Punkt statt 2 $.
4. Alle Results vor dem 16.09. (#153) als "SR altes Maß" markieren. Wer sie auswertet, rechnet `sharpe_ann_daily` neu. Alte Stufe-2-Urteile gegen 5- bis 7-Bein-Bücher zählen nicht als Friedhof.

**P1: reine Bugs ohne Fehlalarm-Preis**
5. `discovery_runner.py` ~Z. 487: `sr_std` nur aus der Theorie (1/√Jahre). Wirkung: Die Decke sinkt in 36 % der Jobs von über 2 auf ~1,3, das allein bringt aber noch kein Bein durch.
6. `controls.py` Z. 688 bis 690: Die Modusliste von `ctl_null` an `NULL_MODES` angleichen (`discovery_lib.py` Z. 937), also gap, orb und cal. rv und i2 bleiben gesperrt bis nach P0.1 und einem eigenen Null-Schalter.
7. `discovery_runner.py` Z. 536 bis 538: das Feld `n_never_evaluated` in Meta und Inbox schreiben. Danach die ~20 Jobs mit bestem Pick ≥ -2 pp komplett durch Stufe 2 schicken (0 neue Trials). Klärt, ob hinter dem Deckel etwas liegt.
8. `controls.py` Z. 445 bis 520 (delay): für ts_reversal und last_hour nur die Fill-Bar verschieben, das Signal bleibt fix. Den LastHour-Befund (z_sign -6,6) als Live-Prüfauftrag an den `live-reconciler` geben (Entry-Slippage).

**P2: Placebo-Kampagne, Voraussetzung für alles Weitere**
9. Mindestens 50 ganze Null-Grids (tm_null auf allen Configs echter tsmom-, ts_reversal- und last_hour-Jobs), mit derselben Top-k-Auswahl nach OOS-Sharpe und derselben Korrektur, im OOS-Fenster und auf voller Historie, durch `book_gate_v2`. Daraus die Schwelle ableiten, statt Šidák über die Picks zu nehmen. Den Doppel-Dip (Auswahl über OOS, Bewertung auf voller Historie) explizit mittesten (Auditor 1).
10. Zwilling v2: denselben Long-Anteil wie der Kandidat behalten (Drift-Loch, siehe AS-07 und ToM) und die Filtergrenzen mitwürfeln (Selektions-Loch, siehe GAPFADE-RT). **Das ist die #106-Kontrolle für die ganze Kette.**

**P3: Stufe 2 auf das echte Ziel umstellen**
11. `eval_plan` bzw. `tempo_plan` statt Δ Passquote: ΔSR_Buch bzw. Δ E[Zeit bis 50k], gepaart gegen Nulldrift-Zwillinge, mit Shrinkage 0,58 und Letzte-3-Jahre-Spalte, am gekauften Punkt 150k k2 (AP246). Nutzen: Die Hürde halbiert sich ungefähr (Zeit-Kriterium S_c > S_b·(ρ + x/2) statt S_b·(x + 2ρ)). #106: ohne Zwilling kam 2.114 von 2.114 Mal "schneller" raus, also ist der Zwilling Pflicht. tempo_plan ist bis AP245 in schwachen Regimen bis Faktor 2 zu optimistisch.

**P4: Lockerungen, erst nach P2**
12. Globale Decke (`discovery_runner.py` Z. 490, 518, 657 bis 660 und `promote_next.py` Z. 307) nur noch als Familien-Decke (Modus × Markt × Why, alle Jobs der Familie zählen mit) und nur als Info.
13. PBO-Veto (Runner ~Z. 661): Hartblock nur, wenn der Reality-Check fällt, PBO bleibt als Info.
14. symbols als Info, Pflicht nur bei Jobs, die über mehrere Märkte gesucht haben.
15. periods asymmetrisch, aber erst wenn die Zwillings-Simulation zeigt, dass die Momentum-Zwillinge weiter gefangen werden. sides erst nach P2.10 weicher machen.

**P5: Abnahme**
16. `_scratch_latte/own_chain.py` mit dem kompletten Paket laufen lassen.
   - Positivsatz: Momentum, LastHour, Asia.
   - Negativsatz: VWAP-PB (#161), Momentum_d260821 (#126), Gap-fade, RV_leadlag_NQES gefixt (#090), REFINE_ORB_2 close, dazu neu LL-01/LL-04 mit Intrabar-Stop, AS-07 und GAPFADE-RT.
   - Freigabe nur, wenn mindestens 2 von 3 Positiven durchkommen und höchstens 1 von 5 Negativen.

**P6: der eigentliche Hebel, der Suchraum**
17. Juli-Modus weiterfahren: Ideen mit Why (Prior ~0,12 statt ~0,006 beim Generator), Ersatz statt Zusatz (Asia-Slot, AP183), neue Märkte und Mechanismen statt weiterer tsmom/maband-Grids. Ein Ersatz fügt keine Größe hinzu, deshalb sagen Passquote und Zeit dort dasselbe, und es gibt keine Decke im Weg.

## Was NICHT gelockert wird, und warum
- **Prämisse, Sharpe-t ≥ 2, Trim 1 %:** kalibriert, kosten kaum Power, tragen den Rauschschutz.
- **Ersatz muss besser als das Original sein:** Die weiche Regel hat 28 von 38 Verschlechterungen durchgelassen (#126).
- **Nulldrift-Pflicht für jede Tempo-Metrik (#106):** Ohne sie ist "schneller" nur mehr Größe.
- **delay als Look-ahead-Schutz (#066/#067) und corr_book:** funktionieren nachweislich.
- **sides:** bleibt, bis der Zwilling driftbereinigt ist, sonst kommt Long-Beta rein.
- **Decke und PBO:** nicht ersatzlos streichen, bevor die Placebo-Kampagne gelaufen ist. Ohne sie steigt der echte Fehlalarm von Gate v2 auf 5 bis 12 %.
- **rv und i2:** nicht öffnen vor dem rv.py-Fix.
- **RTY-Gap-Daten:** keine weitere Retune-Runde darauf.
- **Größe ist kein Tempo-Hebel:** Mehr Kontrakte kaufen Bust, keine Zeit.

## Offene Lücken

- **Keine MC- oder Bootstrap-Zahl** der Stränge wurde unabhängig nachgerechnet (Auditor 2). Selbst geprüft habe ich nur zwei Stellen: die Power-Tabelle in Teil B (Vault, Z. 185 bis 195) und den Namensbug-Fix im Runner (Z. 254 bis 287).
- **Echte Fehlalarmrate von Gate v2 ist unbekannt:** `placebo_log.json` gibt es nicht. Die 5,4 % bzw. 12 % sind eine MC-Schätzung.
- **n_eff ist undefiniert:** Die Schätzungen liegen um Faktor 30 bis 80 auseinander (218 gegen 7k bis 18k gegen 1,9 bis 2,6 je Grid). "Decke auf n_eff" ist deshalb noch kein fertiger Fix.
- **Trichter-Zahlen aus alten Results** (14.336 Alpha-Configs, 6.037 v2-Survivors, Decken-Vergleiche vor dem 16.09.) stehen teilweise im aufgeblähten SR-Maß und sind nur Obergrenzen. Außerdem enthält results/ nur den letzten Lauf je Job.
- **Top-8-Deckel:** Ob unter den 2.692 nie bewerteten Survivors etwas mit Buch ≥ 0 liegt, ist ungeklärt (P1.7).
- **periods asymmetrisch und sides t > -1** wurden nie gegen Zwillinge getestet. Das entscheidet den Widerspruch zwischen den Strängen.
- **Zwillings-Edge beim Momentum-Bein** (+0,106 R bei Zufallsrichtung): Ist das echte Trendpersistenz oder ein Fill-Artefakt am BE-Trigger? Das klärt der `strategy-auditor`. Ist sie echt, fragt Gate v2 Stufe 1 fürs Buch das Falsche.
- **LastHour delay z_sign -6,6:** echte Fortsetzung in der ersten Minute oder Fill-Empfindlichkeit? Braucht einen Live-Abgleich.
- **Späte Tode nur mit Faustformel bewertet:** Sie wurden nie per tempo_plan im Kalender-Modus gegen das aktuelle Buch bei 150k k2 gerechnet. Gegen dieses Buch liegt für den Gap-Fade nur die Faustformel vor.
- **sr_std-Exzess im Register:** Möglicherweise stammt er teils aus einer Mischung verschiedener Engine-Stände (SD 2,54 über 60k Trials). Nicht geprüft.
- **Stale State:** Die Box lief am 25.09. mit einem älteren `discovery_lib.py` als der PC, und `pipeline_ok` ist älter als `hypothesis_bank.py`. Vor dem nächsten Enqueue müssen Sync, Runner-Neustart und ein frischer Marker her.
- **Nicht registrierte Diagnose-Läufe:** Die Gegenprüfung hat rund 30+ Prüf-Configs gerechnet (Nachbarn, andere Märkte, Varianten). Werden sie weiterverwendet, müssen sie per registry_pending_add nachgetragen werden.
- **Nebenwirkung:** Ein Strang hat eine Zeile "Buch geladen" an die lokale `discovery/runner.log` angehängt. Sonst wurde keine Engine- oder Buch-Datei geändert.
- **Nebenbefund für das Quant-Team:** Die Short-Hälfte des Momentum-Beins trägt kaum (t 0,46), macht das Bein aber schneller (281 statt 309 Tage). Das ist eine #106-Frage, kein Urteil.

---

## Beschluss Gate v4 (Max, 28.09.2026)

**Anlass:** Gate v3 (Zwillinge, z 2,5, Schrumpfen 0,58) ist gebaut und lokal getestet (AP257), die Abnahme fiel aber durch: 0 von 3 eigenen Beinen kamen durch, 0 von 9 Nieten. Max: „Es bringt nichts, wenn nichts mehr durchkommt. Was Geld bringt, nicht overfitted ist und mich schneller zum Ziel bringt, kommt ins Buch." Gate v3 bleibt im Code als Info-Wert, entscheidet aber nicht mehr.

**Das Gate:**
1. **Bringt Geld:** alleine profitabel, nach Kosten, auch ab 2024. Vor-Gates wie heute: Sharpe-t ≥ 2, n ≥ 30 (10 OOS), Trim 1 %, Kosten-Stress.
2. **Overfit-Bremse = Walk-Forward mit Neuauswahl:** 2 Jahre Training, 1 Jahr Test, rollierend 2016 bis 2026 (~8 Fenster). In jedem Trainingsfenster wird aus dem Job-Grid die beste Config nach festem Kriterium neu gewählt, im Folgejahr getestet, die Test-Stücke werden aneinandergehängt. Bestanden: die zusammengesetzte OOS-Kurve ist nach Kosten profitabel UND die Mehrheit der Test-Jahre ist positiv (nicht jedes Jahr).
3. **Verbessert das Buch (auf der OOS-Kurve):** Buch-Sharpe steigt (roh, ohne Schrumpfen, ohne Zwillinge). Leitplanken fest vorab: Max-Drawdown intraday wächst nicht um mehr als 20 %, Passquote fällt nicht um mehr als 3 pp. **(überholt seit 29.09.: Max-DD-Leitplanke gestrichen, nur Passquote −3 pp bleibt, siehe Abschnitt „Umsetzung und Stand 29.09.2026" und „Aus der CLAUDE.md (05.10.2026)" unten.)** Ersatz: besser als das Original auf derselben Walk-Forward-Basis. Kein freies Abwägen je Kandidat.
4. **Korrelation, gesunde Mitte:**
   - keine harte Korrelations-Sperre, Korrelation kostet schon über Schritt 3,
   - Tages-Korrelation > 0,7 zu einem Buch-Bein → wird als Ersatz-Kandidat für dieses Bein behandelt, nicht als Zusatz,
   - **einzige harte Regel:** schlimmster historischer Buch-Tag (intraday, Betriebspunkt 150k k2) mit dem Kandidaten ≤ fester Anteil vom Trailing-DD (Startwert 50 %, an den 3 Beinen kalibrieren), **(überholt: wanderte am 28.09. abends aus Stufe 1 raus; in Stufe 2 gilt heute „kein simulierter Tag darf das Konto killen", siehe unten)**,
   - Info im Wochenend-Review: gemeinsame Verlusttage, Tail-Korrelation, Markt/Uhrzeit/Mechanismus; bei gleicher Zeit bis 50k gewinnt der weniger korrelierte Kandidat.
5. **Bestätigung vor dem Next-Week-Buch:** tempo_plan Zeit bis 50k kürzer (Kalender-Modus, Nulldrift-Zwilling 0 %, Auslage p90).
6. **Nur noch Info:** Zwillinge/Gate v3, Schwelle, Schrumpfen, Zufallsdecke, PBO, Delay, symbols. Look-ahead-Schutz über Engine-Regeln (orb_exec usw.) und Test-Kanarie. Long-Drift ist erlaubt (Max: „Hauptsache Profit"), Korrelation an schlechten Tagen wird angezeigt.
7. **Danach:** Next-Week-Buch, Wochenend-Entscheidung Max, Live-Tracking (raus bei expR < 0 nach 50 Live-Trades).

**Einmalige Gegenprobe (kein Dauer-Gate):** 50 reine Null-Grid-Jobs durch Gate v4. Mehr als ~5 % Durchlass = Bremse zu weich.
**Abnahme:** mindestens 2 von 3 eigenen Beinen kommen als neues Bein zum Rest-Buch durch, von den 9 Nieten höchstens 2 (AS-07 als reiner Long-Drift ist nach Max' Regel erlaubt und zählt nicht als Fehler).

### Start-Prompt für die neue Session (opus, vorher `/clear`)

```text
Auftrag: Gate v4 bauen (Max-Beschluss 28.09.2026). Zuerst lesen: Vault "Projekte/Latte-Audit (25.09.2026).md" Abschnitt "Beschluss Gate v4" (die Regel), Ticket AP257 (tasks.json, erst --pull), Daily Notes 2026-09-26 bis 28. Stand: AP257/Gate v3 ist LOKAL gebaut und getestet, NICHT auf der Box (Box läuft noch Gate v2). Backups: engine/_scratch_latte/bak_ap257/ und bak_ap257_rest/. Werkzeuge: engine/_scratch_latte/own_chain_v3.py (Abnahme-Skript), placebo_out/ (Null-Grids), math_v3_* (Power), discovery_lib.book_gate_v3 (bleibt als Info).
Auftragstyp: deploy (Engine + Box). Ablauf als Workflow:
1. Walk-Forward mit Neuauswahl als Bibliotheksfunktion (discovery_lib), Job-Grid je Fenster neu auswählen, OOS-Stücke zusammensetzen.
2. Stufe "verbessert das Buch" auf der OOS-Kurve: Buch-Sharpe roh + Leitplanken (Max-DD intraday +20 %, Passquote -3 pp), Ersatz vs Original.
3. Korrelations-Mitte: Klon > 0,7 -> Ersatz-Pfad; harte Tages-Tail-Regel (schlimmster Buch-Tag intraday bei 150k k2 <= 50 % Trailing-DD, an den 3 Beinen kalibrieren); Info-Felder fürs Wochenend-Review.
4. Runner, promote_next (nur Next-Week-Buch), developer_run, inbox_tool, summarize umstellen; Gate v3, Zwillinge, Decke, PBO, Delay, symbols nur Info.
5. tempo_plan-Bestätigung für Next-Week-Kandidaten (Claude, nicht im Runner).
6. Einmalige Gegenprobe 50 Null-Grid-Jobs (Durchlass <= ~5 %), Abnahme 3 Beine (>= 2/3) + 9 Nieten (<= 2/9, AS-07 erlaubt).
7. Fester Test discovery/test_gate_v4.py, pipeline-auditor, engine-regression-tester, verdict-auditor, CLAUDE.md-Abschnitt "Gate" neu schreiben, Box-Sync + Runner-Neustart, Folge-Ticket Workbench-Anzeige.
Nichts an book_state*.json. Engine ist nur Backup-Repo: vor Änderungen Backups. Am Ende Kurzfassung für Max.
```

### Präzisierung 28.09.2026 abends (Max): zwei Stufen
- **Stufe 1 = Gate v4 (Discovery, automatisch, je Kandidat) → Next-Week-Buch:** Punkte 1 bis 3 oben plus Klon-Regel (> 0,7 → Ersatz-Pfad). Die harte Tages-Regel („schlimmster Tag ≤ 50 % Trailing-DD") und die tempo_plan-Bestätigung wandern aus Stufe 1 raus.
- **Stufe 2 = Wochenend-Prüfung (Claude + Max) → echtes Buch:** fürs ganze Buch prüfen, ob Ersetzen, Hinzufügen oder andere Zusammensetzung mehr bringt. tempo_plan Zeit bis 50k mit dem echten RiskGuard-Tages-Stopp (600 $ × k, **überholt: Soll ist der Stopp je Konto aus der cfg, siehe unten**) und im Vergleich ein dynamischer Stopp (Anteil vom Rest-Puffer). Korrelation so niedrig wie möglich, aber nichts deswegen hart ausschließen; hart nur: kein simulierter Tag killt das Konto.
- Umsetzungsdetails Stufe 1 (für den Bau): Auswahl im Trainingsfenster über ALLE Grid-Configs nur mit Trainingsdaten (die Vor-Gates rechnen auf der vollen Historie und dürfen deshalb nicht in die WF-Auswahl), Kriterium Sharpe im Trainingsfenster; eingesetzt wird die Config, die im jüngsten Trainingsfenster gewählt wurde; Einzel-Config (Developer-Tab, feste Beine) = rollierendes OOS ohne Neuauswahl.

### Umsetzung und Stand 29.09.2026 (Gate v4 live)
- **Änderungen gegenüber dem Beschluss vom 28.09. (Max 29.09.):** Max-DD-Leitplanke gestrichen (sie verbot Zusatzbeine schon rechnerisch, +22 % allein durch ein drittes Bein gleicher Vola); Passquote −3 pp bleibt. Delay-Test ohne jede Wirkung, nur Info-Zahl (Entscheidung A: Look-ahead ist eine Eigenschaft des Modus-Codes; Schutz über ehrliche Modi und Code-Check bei neuen Modi). ORB wird nie ausgeschlossen, sondern ohne ehrlichen Modus automatisch in close + stop_honest gerechnet. Überoptimierungs-Prüfung (Herkunft) in Stufe 2 (Entscheidung B), noch unkalibriert.
- **Abnahme:** eigene Beine 2/3 (Momentum, LastHour; Asia nur an der Passquote −5,2 pp), Nieten 1/9 (GAPFADE-RT), Selbst-Ersatz 3/3 korrekt nicht durch.
- **Null-Kampagne:** 0 von 69 reinen Zufalls-Such-Läufen (10.169 Configs, 24 Grids > 200 Configs, 22 dünne Grids) durch Gate v4, obere 90-%-Grenze 4,2 %. Walk-Forward allein lässt 23 % Nullen durch, die Hauptlast tragen Vor-Gates und „Buch-Sharpe steigt". Nebenbefund: Null-Schalter in tsmom/maband war undicht (Würfel vor den Richtungsfiltern), repariert.
- **GAPFADE-RT (strategy-auditor):** Filterspitze (52 % der R-Summe aus 0,50 bis 0,60 ATR), ≥ 252 Configs über 11 Jobs, Sharpe 0,92 ≈ Zufallsdecke der Familie; Kategorie `unentscheidbar`. Genau dafür die Herkunfts-Prüfung in Stufe 2.
- **Offen (Tickets):** ORB-Whitelist nach (Seite, Modus) statt Blacklist, Herkunft kalibrieren (eigene Beine müssen unauffällig sein, N_eff statt N_family, symmetrisch, 2×SE) vor dem 03.10., `job_generator` „break"-Tippfehler (5 Jobs rechneten Fade), ENGINE_CORE-Hook um discovery_lib/runner/promote_next/job_generator/developer_run erweitern, Look-ahead-Code-Kanarie im Golden Master, Workbench-Anzeige Gate v4.

### Nachtrag 01.10.2026 (Session fcf296d9, AP283-Abgleich)
- **Gebaut (Review):** ORB-Whitelist + Netz je Config + harter Abbruch bei unbekannter Seite/Ausführung (AP276), „break"-Vorlage repariert (Generator reiht die 4 Breakout-Jobs selbst neu ein, Hand-Job `hf_orb_scalp_breakout_NQ` mit ehrlichem Why), Kanarie `gm_gate_v4_canary.py` + AST-Hash im Modus-Check (AP277), ENGINE_CORE inkl. Altfehler `controls.py` (AP278), Workbench auf Gate v4 (AP279), B6-Annahme + Placebo-Dauerkontrolle (AP280), last_hour-Zwilling = echte Null (AP281, Option B), Hub-Roster (AP282). Golden Master grün, `pipeline-auditor` sauber mit Auflagen (alle umgesetzt).
- **Neu gefunden, Tickets im Backlog:** AP290 NT8-Port + Paritäts-Prüfung als fester Schritt vor der Übernahme, AP291 Kaufpolitik in `weekend_check` fest verdrahtet (E8 + FN 150k statt beschlossenem E8 150k), AP292 Live-Ausstieg „expR < 0 nach 50 Trades" steht gegen die Edge-Health-Ampel (Entscheidung Max), AP293 dynamischer Tages-Stopp nur simuliert. AP260 (Marken-Bug tempo_plan) trifft auch Stufe 2, hochgestuft.
- **Offen:** AP275 (Herkunft nach Konzept „Was konnte die erste Fassung?"), wartet auf die zwei Entscheidungen in [[Überoptimierungs-Prüfung Stufe 2 (Konzept)]].

## Aus der CLAUDE.md (05.10.2026)

Aus der CLAUDE.md übernommen (05.10.2026): aktueller Stand von Gate v4, soweit er nur dort stand. Wo oben ältere Leitplanken stehen (Max-DD 20 %, „einzige harte Regel" 50 % vom Trailing-DD, 600 $ × k), gilt dieser Abschnitt.

**Stufe 2: Rechnung und Regeln (Stand 05.10.2026)**
- Frage fürs **ganze** Buch: holen wir mehr raus, wenn wir ein Bein **ersetzen**, eins **hinzufügen** oder die Zusammensetzung ändern?
- Rechnung: `tempo_plan` Zeit bis 50k im Kalender-Modus, Nulldrift-Zwilling 0 %, Auslage p90, simuliert **mit dem echten RiskGuard-Tages-Stopp**. Stopp je Konto aus der cfg: **E8 50k 900 $, FN 600 $, E8 150k 2.500 $ bei k1 (seit 05.10. abends, vorher 1.500)**. 600 $ × k ist beim 7er-Buch zu eng (Quant-Team 04./05.10.). Dazu einmal ein **dynamischer Stopp** (Anteil vom Rest-Puffer zur DD-Grenze) im Vergleich. Stand: `tempo_plan`/`weekend_check` rechnen noch fest 600 × k, bis AP323 gefixt ist (Stufe 2 rechnet bis dahin einen falschen Betriebspunkt).
- Korrelation und gemeinsame Verlusttage aller Beine werden gezeigt. **Keine starre Grenze:** so niedrig wie möglich, aber nichts deswegen hart ausschließen. Bei gleicher Zeit bis 50k gewinnt die weniger korrelierte Variante. **Hart nur: kein simulierter Tag darf das Konto killen.**
- Übernahme ins echte Buch = Max' Wochenend-Entscheidung.

**Live-Tracking nach der Übernahme (Max 03.10.2026, AP292)**
- Zwei Regeln zusammen: Edge-Health-Ampel als Frühwarnung (**gelb: Size halbieren, rot: pausieren**) plus **harter Ausstieg bei expR < 0 nach 50 Live-Trades**.
- Umsetzung: `app_server._edge_health`, Feld `exit_rule`, Alarm in `auto_check`.

**Überoptimierungs-Prüfung (Herkunft)**
- Für neue Beine zählt `weekend_check`, in wie vielen Varianten/Runden die Idee schon optimiert wurde. Bei auffälliger Zahl zusätzlich eine glücksbereinigte Variante.
- **Stand 29.09.: noch unkalibriert** (würde auch die eigenen Beine anmahnen). Die Empfehlung daraus ist nur Hinweis, nicht entscheidungsrelevant, bis die Kalibrierung steht (Ticket AP275).
- Dazu Regime-Spalten `shrink058` und `recent3y` für die Top-Varianten.

**Werkzeug**
- `engine/weekend_check.py`, Kurzbefehl `/wochenende`.
- Nach jedem Box-Sync mit grünem Golden Master einmal `python weekend_check.py --stand-setzen` (Referenz für den Modus-Check).

**Stand 29.09.2026 (live auf der Box)**
- Abnahme bestanden: eigene Beine 2/3 (Momentum + LastHour, Asia nur an der Passquote), Nieten 1/9.
- Null-Kampagne: 0 von 69 Zufalls-Such-Läufen durch, obere 90-%-Grenze 4,2 %. **Erwartet realistisch ein Rauschkandidat alle 3 bis 5 Wochen.** Golden Master grün.
- Code: `discovery_lib.walk_forward`/`gate_v4`, Test `discovery/test_gate_v4.py`, Golden-Master-Kanarie `discovery/gm_gate_v4_canary.py`.

**Stand 01.10.2026**
- **ORB-Whitelist (AP276):** ehrlich nur `close`, `stop_honest`, breakout+`retest`, fade+`return`. ORB wird nie ausgeschlossen, aber alles außerhalb der Whitelist wird automatisch in `close` UND `stop_honest` gerechnet, Prämisse auf beiden. **Unbekannte `orb_side`/`orb_exec` brechen hart ab.** Vorfall: `orb_side "break"` rechnete sechs Wochen lang einen Fade.
- Look-ahead ist eine Eigenschaft des Modus-Codes, nicht der Strategie: Schutz über ehrliche Modi und Code-Prüfung. Neuer Modus oder Engine-Änderung → einmaliger Code-Check (`pipeline-auditor`, Golden Master, Modus-Check in `weekend_check`).
- ENGINE_CORE-Hook-Abdeckung, Kanarie, Workbench-Anzeige Gate v4.
- **Placebo-Dauerkontrolle: ~5 % der Generator-Jobs.**
- **Nulldrift-Zwilling ist jetzt überall eine echte Null** (auch last_hour long_only, AP281).

**Offen (Stand 05.10.2026)**
- AP275: Herkunft (zwei Entscheidungen Max).
- AP290: NT8-Port + Paritäts-Prüfung vor der Übernahme.
- AP291: Kaufpolitik in `weekend_check` fest verdrahtet.
- AP292: Live-Ausstiegsregel klären (Ampel gegen harten Ausstieg).
- AP260: Marken-Bug `tempo_plan` trifft auch Stufe 2.
- AP323: `tempo_plan`/`weekend_check` mit Tagesstopp je Konto statt fest 600 × k.
