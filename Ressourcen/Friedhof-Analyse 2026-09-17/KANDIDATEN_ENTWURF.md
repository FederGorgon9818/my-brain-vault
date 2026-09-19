# Entwurf: Wiederbelebungs-Kandidaten aus den Friedhoefen (Hauptsession, 17.09.2026, VOR verdict-auditor)

Stempel-Vorschlag je Zeile: WIEDERBELEBEN (konkreter Nachtest lohnt), NACHRECHNEN (altes Urteil auf heutigen Stand heben, Erwartung offen), BLEIBT TOT (Urteil haelt trotz Fehlerklasse). Beweislage mit Quelle. Von der Hauptsession selbst am Register/Code verifizierte Punkte sind mit [V] markiert.

## A. Urteile, die auf einem Pipeline-Bug stehen (F6), Nachtest billig
A1 [V] 39 Ersatz-Jobs / 212 Buch-Bewertungen vom 18.-24.08. liefen als "Buch + Duplikat": das zu ersetzende Bein stand noch in book_legs_in_base (replaces "NQ_Momentum"/"NQ_LastHour" ohne Suffix, #139 B5). Darunter TV-02 (OOS expR 0,75), TE-06 (0,68), tsmom_erret (0,57), AB-06, AR-11 (PBO 0), TV-13 Panik-Veto (PBO 0,0001, 26/36 Survivors), AR-02 MA-Steigungs-Gate (54/54 Survivors, PBO 0), TN-04 LastHour-News-Filter (sel ok). Nur TE-02/04/15 wurden als _v2 neu gerechnet (TE-02: Ersatz +0,4 pp = neutral, F0). Stempel: NACHRECHNEN als echter Ersatz (nur Stufe 2 auf vorhandenen Survivors, ~25 s/Config, kein neuer Register-Trial). Erwartung: Duplikat kostet laut #129 ca. -2,2 pp; Zellen mit -0,5 bis -2,0 als Duplikat koennten als Ersatz neutral bis leicht positiv sein; unter Šidák 5,4 pp trotzdem kaum "Kandidat".
A2 [V] hyp_AW14c_NQ (Anker-Placebo rand_time, die Kontrolle, die ueber V1-V9 der VWAP-Familie entscheidet): Status "failed", PermissionError(13) am 16.09. 20:01, nie gerechnet, keine Result-Datei; Queue lief danach leer, niemand hat es gemerkt. Stempel: WIEDERBELEBEN (einfach neu einreihen, Ursache pruefen: NSSM-Dienst-Rechte auf results/).
A3 Modi ohne Null-Schalter bis heute (rv, gap, cal, i2, vix_bias, pivot, flip, continuation): ~2.500 Register-Trials konnten nie deploy_ready werden [V: controls.py ctl_null-Zweige]. Betroffene Bank-Funde: VIX_spike_rev (Live-Bank), EVENT_ES/OPEXMOM (cal), Gap-fade NQ 45 Survivors, RV-08/09/10. Stempel: kein Alpha-Urteil moeglich, NACHRECHNEN erst nach Null-Schalter je Modus (oder Umsetzung als tsmom-Kalender-/VIX-Gate, das seit #145 existiert).
A4 [V] Praemissen-Stufe: 369 Jobs starben mit n>=100 an negativer Basis-Edge, ohne dass das >=10-Varianten-Grid je lief; ~70 davon nur -1..0 pp. Stempel: NACHRECHNEN nur fuer die knappen Faelle mit kausalem Why (Liste in c_premise_friedhof.md), sonst BLEIBT TOT (Basis-Config ehrlich negativ).
A5 TS-21 (MOC-Imbalanz mit echtem Delta) und alle Zeilen mit tm_delta_src="real" vor AP151 P4 massen still das Proxy-Gate (#140). Stempel: NACHRECHNEN (echtes Delta erst seit 15./16.09. in maband ladbar).

## B. Urteile auf alten Daten (F1), besonders ES/RTY vor dem 30.08.
B1 [V] RTY_Gap-fade: am 24.08. aus dem Buch genommen (Top5 0,638, 2/3 Epochen negativ); #135 misst das Bein am 30.08. nach Bereinigung um +8 % expR / +8,7 % Sharpe besser ("unterschaetzt"). Buch hat heute kein RTY-Bein, Entscheidung nie revidiert. Gap-Modus rechnet aus 1m-Open vs Vortages-Close [V], also frontal betroffen. Stempel: NACHRECHNEN (Retune + Epochen + Buch-Marginal auf bereinigten Daten, gegen 4-Bein-Buch; gap braucht Null-Schalter).
B2 Gap-Fade ES/YM, Reversal-Fade RTY (21.08.), ES-Alpha-Woche komplett (25.-28.08.: CE-01/04 Kalender, CR-01/02 Fade, EC-01..05 1080 Configs, wexp_charm, eusession, vixrev/CR-03) [V: alle vor 30.08.]. Stempel: NACHRECHNEN fuer CE-04 (Quartalsende = Roll-Fenster), CR-02 (Overnight-Dislokation = Signal aus Fremdkontrakt-Gaps), CR-03 (VIX-Spike ES, NQ-Pendant Grade A); EC-01..05 BLEIBT TOT bis auf Stichprobe (Momentum auf ES an Kosten gescheitert, Kostenurteil datenunabhaengig).
B3 Juli-Urteile vor 10.08. auf ES/RTY (Bars mit Preis <= 0, #075): Noise-ORB ES/RTY (T62), div_fade 48 Varianten (T15), YM/ES Per-Asset-Batch (T01/T03), IB-Extension, ONREV ES. Stempel: NACHRECHNEN nur Noise-ORB ES/RTY und div_fade (beide hatten NQ-Pendants mit Substanz); Rest BLEIBT TOT.
B4 TR-01/04/06/12 Residual-Momentum (mode=rv, vor rv.py-Fix 31.08.; TR-04 Praemisse -33,5 pp sieht nach Rechenfehler aus). Stempel: NACHRECHNEN.

## C. Urteile unter altem Kriterium (F2) und Bank-Funde ohne v2-Nachrechnung
C1 [V] 15 "Validiert"-Karten in ideas.json, nur 3 in LIVE_EXTRA; 14 von 19 nie unter v2 (#106) bewertet. Noise-ORB NQ (IS=OOS, 9/11 Jahre, top5 0,29) weder aufgenommen noch dokumentiert ausgeschlossen; Mom-lowVIX (OOS +10,4 %, Sharpe 2,78); Gap-Continuation grosse Gaps (OOS +7-9 %); FOMC-solo ES; OPEXMOM ES/RTY/YM. Stempel: NACHRECHNEN als Batch (live_finalize rechnet jedes Bein frisch): Bank-Funde standalone auf heutiger Engine, dann LIVE_EXTRA-Entscheidung (Regel "nichts mit Edge geht verloren"). Kein Prop-Buch-Anspruch.
C2 Klein-N-Event-Edges (FOMC-Post, OpEx-Mom, VIX-Spike-Rev, Turn-of-Month ab 2023 OOS +8-9 %): alle nur als eigenes Bein geprueft, am Frequenz-Gate/Tempo-Kriterium gestorben; nie als Size-/Gate-Overlay auf Bestandsbeine. Stempel: WIEDERBELEBEN als Overlay-Test (gepaart, Event-Tag vs Nicht-Event-Tag auf denselben Beinen), abhaengig von Quant-Antwort Frage 2.
C3 Renko-Flip NQ (T41): 3 der 4 Train-only-robusten Setups in #088, 400-500 Trades/Jahr, abgelehnt unter Verwaesserungs-Logik vor #106. Stempel: NACHRECHNEN unter v2/Min-Size als maband-Kanal-Variante (HF-Fokus Max).
C4 Overnight-RV-Filter (T75): einziger externer Vol-Praediktor mit Sharpe +17 %, verworfen wegen 30-Tage-Frist. Stempel: NACHRECHNEN unter v2 als Tages-Gate (AR-17-Methodik: Shift-Placebo, Episoden-Jackknife).
C5 ONREV_NQ (T49, OOS expR +0,147, 70/Jahr, MM-Inventar-Why) mit Vola-Konditional statt Epochen-Split-Kill. Stempel: NACHRECHNEN.

## D. Falsches Mass / falscher Kontrollarm (F7)
D1 [V] AW-15b (atr_bar, 16.09.): 29/144 Survivors, aber PBO "kaputt", bester Sharpe 0,76 vs Huerde 0,71, Buch-Marginal als Ersatz fuer VWAP-PB -8 bis -24 pp. Stempel: BLEIBT TOT (Extraktion hatte "hoch" gesagt, die Zahlen sagen nein).
D2 AW-09b/AW-11b/AW-02/LD-02/EC-03 nach AP160-Umstellung auf "atr" (Tages-ATR20): beim naechsten Enqueue stiller Praemissen-Tod (3 Trades). Stempel: vor Enqueue auf atr_bar umstellen + len(trades)-Sanity; kein Urteil.
D3 GEX als Vola-/Stop-Weiten-Gate statt Richtungs-Gate (validiert t -6,9 auf ES, nur in der falschen Anwendung getestet); Filter-Hypothesen generell an top5/freq-Gates gestorben, die mit der Trade-Zahl skalieren (#137 P9, AP117 offen). Stempel: NACHRECHNEN gepaart (Bein mit/ohne Gate, gleiche Tage).
D4 VWAP-Pullback Multi-Symbol-Kill (T2-10): lief auf v4 (beide Seiten, ohne Delta/Distanz/RR 1,5) auf ES/RTY vor #135. Stempel: NACHRECHNEN mit v8-Spezifikation, ATR-Stops, bereinigte Daten (aber erst nach AP158, weil das NQ-Bein selbst -4,7 pp misst).

## E. Messfunde ohne Weiterverfolgung (F10), 0 neue Register-Trials noetig
E1 pts_per_kdelta als Continuation-Filter auf NQ_Momentum (#107: stationaer, monoton, IS=OOS, explizit als offene Frage notiert, nie gerechnet).
E2 Absorptions-Inverse als VWAP-Pullback-Filter (#100: OOS +0,0269 ohne vs -0,0053 mit, IS gleichgerichtet).
E3 Erstkerzen-Richtung als Bestaetigung auf NQ_Momentum (#147: traegt Info, 82,8 % Momentum-gleich; als Filter = weniger Trades, Lehre 82 greift nicht).
E4 AR-19 Korrelationsregime (Stufe 1 bestanden, nicht COVID-getragen, seit 01.09. unberuehrt).
E5 NQ_LastHour_v3 Unter-MA-Ueberschuss (+27,7 $/Tag, CI ohne Null, vola-konfundiert; RV20-Terzile nie geprueft).
E6 Spiegel-Trick nie angewandt bei: ES-VWAP-Reversion (PF 0,09-0,22 Continuation), ES/YM-Breakout-Fade, IB-Fade, First-Bar-Fade auf ES/YM/RTY (Brown 2025), OR_DELTA SHORT (OOS +60R, "IS=0" war Bullen-IS).
E7 NOISE_ORB mit halber Varianz (engerer Stop/Teil-Size) + FA-01-Pullback-Entry auf ORB (Vorabmessung +0,85 Pkt/Trade gepaart, nur in tsmom verdrahtet [V]).
Stempel E1-E7: WIEDERBELEBEN als billige Konditional-Checks auf vorhandenen Trades, je 1-2 Stunden, kein Grid.

## F. Liegengebliebene Vorraete (F9)
F1 [V] Volumen-&-Flows-Bank: 479 Hypothesen, 0 gebaut, 192 ohne neuen Code testbar, Status seit 21.08. "noch nichts getestet"; Queue lief seither 4x leer. TWAP-Bank 99/100 und PCA-Bank 21/21 ungebaut (je ein fehlender Basis-Baustein). Pairs-Bank 71/100 ungebaut.
F2 Scout-Modul-Specs, mehrfach als "billigster Hebel" benannt und nie gebaut: Orderflow-v2-Nebenspalten als Gate (0 von 63k Trials nutzen sie), DIX-01 (Daten in daily_context), macro_gate/daygate, volshock (mit 2023+-Nebenbefund t 3,2), tm_stop_mode="leg" (Fib-W14a, AC-06c dritter Arm), Coast-to-Target (cage_policy_lib:316).
F3 [V] 2.634 von 4.605 Survivors nie gegen das Buch gerechnet (max_book_evals-Deckel); die staerksten (tsmom EMA-Leiter HF, OOS-expR ~0,74) als "neues Bein" neutral, als Ersatz fuer NQ_Momentum nie (Slot-Tabelle #146 unabgenommen).
F4 379 ungelesene Inbox-Eintraege; Ergebnisse von RV-08/09/10, LD-01/02, LQ-01, GEX01/02, lunch_fade nie in einem Urteil angekommen.

## G. Bestandsbeine (Referenzbuch-Problem)
G1 NQ_VWAP-Pullback -4,7 pp (AP158), NQ_LastHour_v3 -4,3 pp LOO (AP162), Momentum-BE auf expR negativ (AP121). Alle Ersatz-Marginale der VWAP-Familie messen gegen ein negatives Referenzbein ("Wash" = so schlecht wie ein Bein, das das Buch belastet). Stempel: Entscheidung Max zuerst (Wochenend-Paket), danach alle VWAP-Ersatz-Urteile neu lesen.
