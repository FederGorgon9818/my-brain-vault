---
tags: [projekt, trading, alpha-suche, es-nq-divergenz]
erstellt: 2026-09-16
aktualisiert: 2026-09-17
status: aktiv
ziel: v2-Passquote je Eval verbessern über Cross-Index-Gates auf Buch-Beinen oder SMT-Level-Wege, oder das Kapitel sauber schließen
---

# ES-NQ-Divergenz Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 16.09.2026 vom `familien-scout` (Auftrag Max: Lesart a SMT-Level-Divergenz + Lesart b Cross-Index-Bestätigung, Handel in ES und NQ). Am selben Tag nach dem Vollständigkeits-Check des `verdict-auditor` ergänzt: W26-W30 sind neu, W10/W13/W19/W21/W22/W25 haben einen korrigierten Stand. Ebenfalls am 16.09. der Research-Stand je Skelett zurückgeschrieben (Abschnitt „Research-Stand“): 8 offen, 3 widerlegt, 0 belegt. Es gibt keine Hand-Karte zum selben Konzept. Überschneidung besteht nur mit Zelle **V9 (Cross-Market-VWAP-Spread)** in [[VWAP-Offensive]], die hier nicht angefasst wird. Format-Vorbild: [[Fibonacci Wege-Karte]].

> [!warning] Der Spread-Zweig ist bis 14:30 erledigt, offen sind Level, Gate, Vortags-Führung und das Fenster nach 15:00
> Alles, was ES/NQ über einen **Rendite-Spread** mit Entries bis 14:30 handelt, ist ausgereizt: 739 RV-Trials im Register, Lead-Lag tot ([[Strategie-Logbuch#090]]), Spread-Fade tot ([[Strategie-Logbuch#033]]), RS-01/SM-04/SM-10/RV-08 premise_failed oder 0 Kandidaten. `rv` hat keinen Null-Schalter und kann nie `deploy_ready` werden. **Offen sind:** die Level-Divergenz (SMT, im Haus nie gemessen), das Cross-Index-Gate auf Buch-Beinen, der gestrige Führer als Tages-Gate (RS-08) und die späte Divergenz nach 15:00 (ZF-05, wegen `rv_cutoff=300` nie gesehen). Alles davon braucht eine Modul-Spec.

---

## Harte Randbedingungen

**1. Alles Neue in `maband`/`tsmom` oder als Gate in Modi mit Null-Schalter.** Das Gate (Spec B) hängt in den vier Buch-Modi, die seit AP157 `tm_null` haben, und in `sigcore.gates_pass`. Die SMT-Wege (Spec A) werden ein neuer `mb_kind`. Ein neuer `mode` kommt nicht in Frage, `rv` nur als Prämissen-Messung.

**2. Ersatz schlägt Neuzugang** (#139 B3). Die Gate-Wege W12/W13/W15/W25 sind Ersatz-Slots und stehen deshalb vorn. SMT (W5) und die späte Divergenz (W27) sind neue Beine und stehen hinten.

**3. Positions-Instrument trägt Risiko und Kosten** (Lehre 46, [[Strategie-Logbuch#090]]). Eine Position in ES heißt MES mit relativ zur Range höheren Kosten als MNQ (~2 Pkt Round-Trip). `_drop_corrupt_sessions` muss für ES aktiv sein ([[Strategie-Logbuch#075]]).

**4. Level-Bedeutung ist im Haus widerlegt** ([[Strategie-Logbuch#138]], [[Strategie-Logbuch#149]], [[Strategie-Logbuch#051]]). Jeder SMT-Weg läuft mit `ctl_random_level` auf **beiden** Leveln.

**5. Look-ahead-Falle Vortageslevel:** `sigcore.daily_context` trägt `h`/`l` des laufenden Tags. Vortageshoch/-tief und Vortags-Führung deshalb nur mit `shift(1)`.

**6. Tages-Gates brauchen einen Placebo, kein Seed-Rauschen** (Nachtrag). Seed-Streuung ist bei Tages-Gates das falsche Rauschmaß ([[Strategie-Logbuch#136]] Lehre 2). Pflicht: Circular-Shift-Placebo pro Variante ([[Strategie-Logbuch#139]] Lehre 1), Off-Tage-Malus als Hürde (#139 Lehre 2), invertiertes Gate, und bei Filtern t ≥ 3,1 oder eine vorab fixierte Hauptvariante ([[Strategie-Logbuch#111]] Lehre 101).

**7. Bei ES-Positionen keine Richtungsinformation voraussetzen** ([[Strategie-Logbuch#150]]): die ES-Basen der Buch-Modi haben keinen Survivor.

---

## Register-Stand (16.09.2026, Box)

| Griff | Zahl |
|---|---|
| `n_total` | **63.431 Trials** |
| davon `mode=rv` (einzige Zwei-Symbol-Trials) | **739** |
| rv NQ/ES je Art | leadlag 99 · div_mom 70 · div_fade 19 · gap_div 5 · eod_conv 3 |
| mit Level-Divergenz oder Cross-Index-Gate | **0** |
| div_mom NQ/ES mit Entries nach 14:30 | **0** (`rv_cutoff` Default 300) |
| LL-01 NQ→ES | v1 premise_failed mit n=0 (Bug), v2 36 Configs / 14 Survivors / **0 Kandidaten** |
| LL-04 / LL-07 / LL-14 NQ→ES v2 | 24/7/0 · 16/2/0 · 24/0/0 |
| RS-01 NQ/ES | v1 premise_failed (IS expR −0,052), v2 63/0/0 |
| SM-04 v1+v2, SM-10, hf_NQES_RV_divfade | premise_failed, IS expR −0,15 bis −0,17 |
| RV-08 gap_div NQ/ES | premise_failed (−0,145) |
| ES in Buch-Modi | ts_reversal 87 · last_hour 56 · asian 28 Trials, **0 Survivors** außer 1 von 8 im Alt-Backfill |
| `maband channel` NQ (Ausbruchs-Basis) | 4.085 Trials, 149 Survivors, **0 Kandidaten** |
| Buch (live = next) | NQ_Momentum_d260818 · NQ_LastHour_v3 · NQ_Asia-Dir-USopen_d260820 · NQ_VWAP-Pullback |

---

## Die 30 Wege

Die Wege sind mechanisch aus Elementen, Beziehungen und Richtung aufgebaut.
- **Elemente:** Preis NQ, Preis ES · Level je Index (Session-Extrem, Vortag, OR, n-Bar-Swing, Overnight, VWAP) · Signal im Positions-Index · Rendite-Spread · Zustände (Konsens, Korrelation, relative Vola, Führung, Zeitversatz, Tageszeit).
- **Achsen, keine eigenen Wege:** Level-Art, bei Lesart (a) auch das Positions-Instrument und der Y-Zustand (flach/gegenläufig).
- **Richtung:** X = der Index, der sich bewegt, Y = der andere.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| W1 | X bricht Level, Y nicht, Fade X **früh** | Mean Reversion | Signal | offen, Einstiegs-Achse von W5 | Spec A | neues Bein |
| W2 | X bricht, Y nicht, Trade im **nicht bestätigenden Y** | Relative Value | Signal | kontaminiert (RS-01 tot), kein Skelett | Spec A | neues Bein |
| W3 | X bricht, Y nicht, Y läuft **hin zu** seinem Level | Trend Following | Signal | kontaminiert (LL-01, #090), Reparametrisierung, kein Skelett | Spec A | neues Bein |
| W4 | X bricht und **hält**, Y nicht, Continuation X | Trend Following | Signal | keine Story (Nichtbestätigung spricht dagegen) | Spec A | – |
| W5 | X **kreuzt und scheitert**, Y nicht bestätigt, Fade X | Mean Reversion | Signal | 🟢 **offen → XD-W5a / XD-W5b** (Research offen) | Spec A | neues Bein |
| W6 | X und Y **brechen beide**, Continuation | Trend Following | Signal | 🟡 Basis gemessen ohne Kandidat (channel 4.085), Gate erst nach W12 | Spec A / channel + Spec B | neues Bein |
| W7 | X und Y **prallen beide ab** | Mean Reversion | Signal | kein Skelett, Level-Bedeutung widerlegt | Spec A | – |
| W8 | beide **laufen entlang** Session-Extrem | Trend Following | Filter | keine eigene Story (→ W18) | Spec A | – |
| W9 | X scheitert, Y **bestätigt** | Mean Reversion | Signal | keine Story (keine Divergenz), = #116/#112 | Spec A | – |
| W10 | Divergenz **weitet sich**, Entries bis 14:30 | Relative Value | Signal | 🟡 **gemessen ohne Kandidat** (div_mom NQ/ES 70 Trials: RS-01, TR-01; #033 „marginal“, nicht tot) | rv | – |
| W11 | Y **kreuzt später und hält** | Trend Following | Signal | keine eigene Story (= W3/W6 spät) | Spec A | – |
| W12 | NQ-Momentum, ES **zieht mit** | Trend Following | Filter | 🟢 **offen → XD-W12a / XD-W12b** (Research offen) | Spec B (ts_reversal) | **Ersatz NQ_Momentum_d260818** |
| W13 | NQ-LastHour, ES **zieht mit** | Trend Following | Filter | 🟠 **Research widerlegt (#087, Research-Cache Z.515)** → XD-W13a nicht in dieser ein-weg-Runde, kein Tot-Stempel; toter Verwandter #111 | Spec B (last_hour) | **Ersatz NQ_LastHour_v3** |
| W14 | NQ-Asia-Richtung, ES gleichgerichtet | Trend Following | Filter | offen, kein Skelett (Gate bindet vermutlich kaum) | Spec B (asian) | Ersatz NQ_Asia-Dir-USopen_d260820 |
| W15 | NQ-VWAP-Pullback, ES **gleiche VWAP-Seite** | Trend Following | Filter | 🟢 **offen → XD-W15a / XD-W15b** (Research offen, Lücke Cache Z.1087) | Spec B (vwap_pullback) | **Ersatz NQ_VWAP-Pullback** |
| W16 | anderer zieht **nicht** mit → Veto | – | Kontrolle | kein eigener Weg: invertiertes Gate = Pflichtkontrolle | Spec B | – |
| W17 | unbestätigter Move → **Fade, 1 Bein** | Mean Reversion | Signal | 🟡 als 2-Bein gemessen ohne Kandidat (SM-04/10, #033), kein Skelett | rv / Spec B | – |
| W18 | **Konsens** aller 4 Indizes | Trend Following | Filter | Achse von W12 (TS-18, LL-11) | Spec B | wie W12 |
| W19 | Intraday-**Korrelation** hoch/niedrig | Relative Value | Filter | 🟡 als Buch-Regime Stufe 1 gemessen ([[Strategie-Logbuch#141]] AR-19, ~7 Episoden), Paar-Gate ungetestet (SM-09, RG-01), Achse | Spec B | – |
| W20 | Y **folgt X verzögert** (Lead-Lag) | Trend Following | Signal | ❌ **tot ([[Strategie-Logbuch#090]])** | rv leadlag | – |
| W21 | **Gap-Divergenz** am Open | Relative Value | Signal | 🟡 **gemessen ohne Kandidat** (RV-08, 5 Trials; Bug aus #033 in #137 gefixt) | rv gap_div | – |
| W22 | Spread **konvergiert bis EOD** | Relative Value | Signal | ❌ **tot ([[Strategie-Logbuch#033]], gestützt durch #087)**, aber nur 3 Trials | rv eod_conv | – |
| W23 | X **kreuzt VWAP und hält**, Y nicht | Relative Value | Signal | offen, Research zuerst (= V9 in [[VWAP-Offensive]]) | Spec A (Level=VWAP) | – |
| W24 | **(Swing)** Tages-/Wochen-SMT → Mehrtages-Reversal | Swing | Signal | offen, **Live-Buch-Merker, nicht Prop-Buch** | Spec C | Live-Buch-Merker |
| W25 | Gestriger **Führer** als Tages-Gate (RS-08) | Trend Following | Filter | 🟡 **offen, Prämisse schwach** (Vorab-Messung 17.09., verdict-auditor-korrigiert: keine Definition >~10pp MDE signifikant, Gate-Effekt +11,6 bps p=0,21 bei halber Trade-Zahl; nicht in dieser ein-weg-Runde, kein Tot-Stempel) | Spec B + `prev_day_rel` | **Ersatz NQ_Momentum_d260818** |
| W26 | **Spiegel (b):** Signal im ES, NQ **zieht mit** | Trend Following | Filter | neu, kein Skelett: ES-Basen ohne Survivor, #150 | Spec B (`tm_xref_sym=NQ`) | neues Bein |
| W27 | **Späte Divergenz** ab 15:00 läuft bis Close (ZF-05) | Relative Value | Signal | 🟠 neu, **Research widerlegt (ZF-05 kontaminiert, #087, Research-Cache Z.515)** → XD-W27a/b nicht in dieser ein-weg-Runde, kein Tot-Stempel | rv (Prämisse) / tsmom + Spec B `rel` | neues Bein |
| W28 | **Führungswechsel** intraday | Relative Value | Signal | neu, keine Story (= Konvergenz-Arm von div_fade) | rv / Spec B | – |
| W29 | X bricht Hoch, Y bricht **gleichzeitig Tief** | Mean Reversion | Signal | neu, Achse `mb_smt_ystate` von W5 | Spec A | wie W5 |
| W30 | **Relative Vola** ES/NQ eng/weit | Relative Value | Filter | neu, keine Story (kein handelnder Akteur), Achse neben W19 | Spec B (`range_ratio`) | – |

---

## Wege mit Skelett

### W12: NQ-Momentum nur, wenn ES mitzieht
- **Story (Entwurf):** ein Impuls, den beide Indizes tragen, ist marktweiter Flow, der gestückelt weiterläuft; ein NQ-only-Impuls ist öfter Einzeltitel-News.
- **Skelette:** XD-W12a (long), XD-W12b (short), beide `why_status: entwurf`.
- **Engine:** Spec B, Hook neben `vix_gate` in `qbt._reversal_trades`.
- **Kontamination:**
  - LL-01 hat das **Komplement** gehandelt (ES hinkt → ES kaufen) und ist tot. Das sagt nichts über die NQ-Fortsetzung an bestätigten Tagen, die Tagespartition ist aber dieselbe.
  - [[Strategie-Logbuch#136]] (AR-15) und [[Strategie-Logbuch#139]] (AR-17): Tages-Gates auf Buch-Beinen ohne Kandidat. Placebo-Pflicht (Randbedingung 6), dazu prüfen, ob die Maske nur die Hochvola-Menge nachbildet.
- **Research (16.09.):** beide **offen**. Keine Studie zu Cross-Index-Bestätigung als Verstärker. Intraday-Momentum ist belegt, aber pro Instrument (Gao/Han/Li/Zhou JFE 2018, Baltussen et al. JFE 2021, Cache Z.30/476/699). Dow-Konfirmation (Brown/Goetzmann/Kumar JoF 1998) nur Monats-/Jahreshorizont. W12b zusätzlich nur Krypto-Kontext (Shen 2022, Cache Z.509). Why bleibt Entwurf, geht an ein-weg.
- **Stempel:** –

### W13: NQ-LastHour nur, wenn ES mitzieht
- **Story (Entwurf):** Schlussstunden-Flows sind indexweit. Ohne ES-Gleichlauf fehlt der Treiber, die Flow-These selbst ist aber umstritten und in der MOC-Form falsifiziert ([[Strategie-Logbuch#087]]).
- **Skelett:** XD-W13a (long, das Bein ist `long_only`).
- **Toter Verwandter:** [[Strategie-Logbuch#111]]. Dort wurden rund 150 Filter auf genau diesem Bein gerechnet, und keiner ist bewiesen (nested WF +0,9 $/Trade [−2,1; +5,9]). Der Cross-Index-Filter zählt zur selben Filter-Familie. Deshalb gibt es nur **eine** vorab fixierte Hauptvariante (Lehre 100/101).
- **Research (16.09.):** **Research widerlegt** (Logbuch #087: 0/72; Cache Z.515: kein Konsens, Ivanov/Lenkey 2018 contra Cheng/Madhavan). XD-W13a geht **nicht** in diese ein-weg-Runde. Kein Tot-Stempel, der Weg bleibt offen für einen neuen Grund.
- **Stempel:** –

### W15: NQ-VWAP-Pullback nur, wenn ES auf derselben VWAP-Seite steht
- **Story (Entwurf):** ein Rücksetzer wird nur gehandelt, wenn der Tagestrend marktweit getragen ist.
- **Skelette:** XD-W15a (long), XD-W15b (short).
- **Kontamination:**
  - [[Strategie-Logbuch#108]] (VWAP-Cross am NY-Open = Wegmessung). Dort war der eigene Cross das Signal, hier ist die Seite des Schwester-Index der Filter.
  - #136/#139: Tages-Gate-Klasse.
- **Abgleich mit V9** der [[VWAP-Offensive]] macht die Hauptsession.
- **Research (16.09.):** beide **offen**. Dokumentierte Forschungslücke (Cache Z.1087, 10.09.): kein Paper zum Cross-Market-VWAP-Spread. Why bleibt Entwurf, geht an ein-weg.
- **Stempel:** –

### Vorab-Messung (17.09.2026, Hauptsession + verdict-auditor-Korrektur)

Alle drei registerfreien Vorab-Checks aus dem Abschnitt „Reihenfolge nach Buch-Chance" gerechnet (`qbt.load_rth("NQ")`/`("ES")`, ~2717-2718 gemeinsame Handelstage, Skripte im Scratchpad der Session, kein Trial, keine Registry).

- **W12/W15-Gate (ES zieht bei NQ-Momentum-Signal nicht mit):** 64,6 % der 808 NQ-Signaltage (thr 0,3 %, 15-Min-Fenster) — weit über der 15 %-Schwelle, **Gate bindet, W12/W15 bleiben in dieser Runde**. Davon aber nur 5,7 % echter Vorzeichen-Widerspruch; die restlichen 64,6 % sind ES unter der 0,3 %-Schwelle (ES-Vola strukturell kleiner als NQ). Die Modul-Spec (Spec B) sollte deshalb ein relatives/z-Score-Maß für ES statt eines festen Prozentsatzes prüfen, sonst filtert das Gate primär „ES war ruhig", nicht „ES widerspricht".
- **W5/W29-Level-Basisrate:** je Richtung 5,3–9,2 % „einer nimmt sein Erste-Stunde-Extrem erneut, anderer nicht" (Proxy, 2715 Tage) — genug Basis, **kein Killer für W5**. Die W29-Gegenrichtungs-Zahl (36,3 %) ist mit der groben Proxy-Definition nicht belastbar (Mehrfachereignisse pro Tag), bleibt offen mit besserer Definition.
- **W25/RS-08-Übergangsmatrix — korrigiert nach verdict-auditor-Check (17.09.2026):** die erste Messung (Führer = größerer `|RTH-Return|`) war fehlkonstruiert — das ist ein Vola-Verhältnis-Proxy (NQ/ES ≈ 1,3×), keine Führungs-Rangfolge, und der direkte Gate-Test hatte eine Fensterüberlappung (Signalfenster im Ergebnisfenster), die jeden Effekt verdünnt. Nachgerechnet mit 3 Führer-Definitionen (2718 Tage, 04.01.2016–10.08.2026): **|Return|** +1,7 pp (p=0,37), **signiert** (= Bank-Definition RS-08) −3,1 pp (p=0,11, Tendenz Umkehr statt Persistenz), **vol-normiert** +4,6 pp (p=0,018, aber 1 von 3 Definitionen, vermutlich Vola-Clustering). MDE bei 80 % Power ≈ 9,7 pp — das Design kann nur Effekte >~10 pp ausschließen, „kein Effekt gefunden" ≠ „widerlegt". Gate-Wirkung auf NQ_Momentum-Signaltagen ohne Fensterüberlappung (Definition B, signiert): +11,6 bps Restrendite mit Gate vs. +4,6 bps ohne (p=0,21), halbiert aber die Trade-Zahl. **Urteil: Prämisse nicht bestätigt, nicht widerlegt — kein Job in dieser Runde, kein Tot-Stempel** (gleiche Behandlung wie W13/W27). Zusätzlich formal: eine 2-Wege-NQ/ES-Messung kann die Bank-Zeile RS-08 (4er-Rangfolge NQ/ES/YM/RTY, ~25 %) ohnehin nicht killen, nur das W25-Gate selbst. Präzedenz: [[Strategie-Logbuch#136]] (AR-15), [[Strategie-Logbuch#139]] (AR-17) — dieselbe Gate-Klasse „Tages-Gate auf Buch-Bein" ist teuer und bisher ohne Kandidaten. Sollte der Ersatz-Slot nach W12 frei werden: Nachtest auf Netto-R des echten Beins mit Definition B, vorab fixiert, voller #136/#139-Placebo-Batterie.

### W25: Gestriger Führer als Tages-Gate auf NQ_Momentum (Nachtrag)
- **Story (Entwurf, Bank RS-08):** Sektorführung ist mehrtägig. Ein NQ-Impuls an einem Tag nach NQ-Führung hat Rückenwind aus demselben Allokations-Flow. Es gibt keine Overnight-Position, der Weg gehört also ins Prop-Buch und ist **kein Swing**.
- **Skelette:** XD-W25a (long), XD-W25b (short). Nur die NQ-Hälfte, weil ES-Beine keine Roh-Edge haben (W26, [[Strategie-Logbuch#150]]).
- **Vorab und registerfrei:** RS-08-Übergangsmatrix NQ vs. ES. Fällt sie, fallen beide Skelette ohne Trial.
- **Doppelzählung:** Die ideas.json-Karte „Cross-Sectional Momentum“ (Backlog) nennt dasselbe Instrument-Auswahl-Overlay. Beides zählt als **eine** Trial-Familie.
- **Slot-Konkurrenz:** W25 teilt sich den Ersatz-Slot mit W12. W12 kommt zuerst.
- **Research (16.09.):** beide **offen**. RS-08 intern ungetestet (Bank Z.127). Extern nur Jegadeesh 1990 / Lehmann 1990 (Einzelaktien-Reversal der Eigenrendite), mechanisch etwas anderes.
- **Vorab-Messung (17.09., Details oben):** Prämisse nicht bestätigt, nicht widerlegt. **XD-W25a/b gehen in dieser Runde nicht an ein-weg**, bleiben aber offen (kein Tot-Stempel) — Nachtest auf Netto-R des echten Beins lohnt erst, wenn der Ersatz-Slot nach W12 frei wird.
- **Stempel:** –

### W5: SMT-Fehlausbruch
- **Story (Entwurf):** ein Extrem nur in einem Index ist ein Stop-Run ohne marktbreiten Nachschub. Das Scheitern trennt den Fehlausbruch von laufender Rotation.
- **Skelette:** XD-W5a (short an Hochs), XD-W5b (long an Tiefs).
- **Achse Y-Zustand (Nachtrag, W29):** `mb_smt_ystate`, entweder `flat` (Y bleibt vor seinem Level) oder `against` (Y bricht gleichzeitig sein Gegen-Extrem).
- **Kontaminationswarnung:**
  - [[Strategie-Logbuch#116]] und [[Strategie-Logbuch#112]] (Einzelindex-Fehlausbruch schwach bzw. Friedhof)
  - [[Strategie-Logbuch#138]] und [[Strategie-Logbuch#149]] (Level am Zufallslevel nicht unterscheidbar)
  - [[Strategie-Logbuch#133]] (Divergenz korrelierter Serien ist ein kleines Residuum)
  - [[Strategie-Logbuch#068]] (nach dem Ausbruch Münzwurf)
- **Neu ist nur die Nichtbestätigung im Schwester-Index.** Zuerst die Basisrate messen.
- **Research (16.09.):** beide **offen**. SMT ist ein reines ICT-/Retail-Konzept ohne akademische Stütze oder Zahl (LuxAlgo/FXOpen/TradingFinder, neu im Cache). #116/#112 sind Einzelindex-Mechanismen. Für W5b gilt #108: Long-Bias-Kontrolle ist Pflicht. Why bleibt Entwurf, geht an ein-weg.
- **Stempel:** –

### W27: Späte Divergenz läuft bis Close (Nachtrag)
- **Story (Entwurf, Bank ZF-05):** in der letzten Stunde wirken Rebalancing und MOC-Flows je Index verschieden. Eine erst dort entstehende Divergenz ist echte Umschichtung und läuft weiter.
- **Skelette:** XD-W27a (long NQ bei relativer NQ-Stärke), XD-W27b (short NQ bei relativer NQ-Schwäche).
- **Warum der Weg offen ist:** RS-01 und TR-01 liefen mit `rv_cutoff=300`, also ohne Entries nach 14:30.
- **Engine:**
  - Prämisse vorab als Spread in `rv` messbar (`rv_entry_after=330`). Das zählt als Trial, hat aber keinen Null-Schalter.
  - Buch-Weg: `tsmom` mit `tm_sig_start=330` plus Spec B mit Basis `rel`.
- **Kontamination:**
  - [[Strategie-Logbuch#087]]: absolutes Late-Entry-Momentum ab 15:00 ist auf 4 Indizes tot (0/72). Neu ist hier nur die relative Bedingung.
  - eod_conv: die Gegenrichtung ist tot, aber nur mit 3 Trials belegt.
  - #111: gleiches Zeitfenster.
- **Buch:** neues Bein. Die Tages-Korrelation zu NQ_LastHour_v3 muss ≤ 0,70 sein (#079).
- **Research (16.09.):** **Research widerlegt** (ZF-05 in der Bank Z.166 als kontaminiert markiert; #087 0/72; Cache Z.515 ohne Konsens). XD-W27a/b gehen **nicht** in diese ein-weg-Runde. Kein Tot-Stempel, der Weg bleibt stehen.
- **Stempel:** –

## Wege ohne Skelett, kurz begründet
- **W1:** Einstiegs-Achse von W5.
- **W2:** RS-01 zweimal tot, Verwandter ist Cross-Sectional Momentum (ideas.json).
- **W3:** Diffusion wie LL-01, der Level-Trigger ist nur eine Reparametrisierung.
- **W6:** Filter auf eine Basis ohne Roh-Edge wäre Overfitting, erst nach W12 sinnvoll.
- **W7:** Level-Bedeutung widerlegt.
- **W14:** ES/NQ-Asia-Richtung fast identisch, das Gate bindet vermutlich kaum. Dazu kommt #141 AR-20 (Asia-Dir-Konfig ❌).
- **W17:** Prämisse edge −12 bis −14 pp, halbe Kosten drehen das nicht.
- **W19:** Korrelationsregime nur ~7 Episoden (#141), als Achse von W5/W12 führen.
- **W23:** V9 steht schon als „Research zuerst“.
- **W26:** ES-Basen ohne Survivor (87/56/28 Trials), #150.
- **W28:** Ein Führungswechsel ist ein Spread-Nulldurchgang, also der Konvergenz-Arm von div_fade (tot).
- **W29:** Achse von W5. Die Basisrate ist bei hoher ES/NQ-Korrelation vermutlich zu klein.
- **W30:** kein handelnder Akteur, Vola-Gates ohne Kandidat (#136/#139). Getrennt von W19 führen (#141 Lehre 3).

## Swing-Zeilen (Live-Buch-Merker)
**W24** Tages-/Wochen-SMT läuft nur auf Tageshorizont. Der Weg wird mitgeführt, damit nichts verloren geht, bekommt aber keinen Prop-Job. W25 stand hier bis zum Nachtrag und ist jetzt Prop-Weg.

---

## ein-weg-Entscheidung (17.09.2026, variant-scout + strategy-auditor-Batch)

Zusatzmessung vor dem Batch (registerfreie Auflage aus dem Batch selbst, s.u.): VWAP-Seiten-Übereinstimmung NQ/ES stündlich 10:00-14:30 ET, 2718 Tage — **83,6-88,5 % Übereinstimmung**, also nur **11,5-16,4 % Nicht-Übereinstimmung**. Das liegt genau um die 15 %-Schwelle, unter der laut Karte ein Gate "praktisch wegfällt" — die Prämisse für W15 ist damit **schwach**, nicht klar tot.

| Skelett | Varianten (variant-scout) | Story-Urteil (strategy-auditor) | Entscheidung |
|---|---|---|---|
| XD-W12a | 36, Grenzwertig | Story hält mit Vorbehalt: Gate misst zu ~94 % "ES war ruhig" statt "ES widerspricht" | **Nachbessern, dann H()-Zeile.** Fix: ES-Schwelle relativ (z-Score/ATR) statt fest 0,3 %; TS-18/LL-11 als abgedeckt markieren, falls Konsens-Achse mitgebaut wird |
| XD-W12b | 4, nicht sinnvoll testbar | – (schon bei Varianten raus) | **Nicht bauen.** Gate bindet auf der Short-Seite nur 5,2 % und streicht dabei die besten Trades (+0,98R entfernt, −0,008R behalten); jede bindende Variante fällt unter `min_tpy=25` |
| XD-W15a | 24, Grenzwertig | Story hält mit Vorbehalt: Why ist reine Korrelationsbehauptung ohne Akteur | **Prämisse schwach** (VWAP-Basisrate s.o., ~12-16 % Nicht-Übereinstimmung, nahe der 15 %-Wegfall-Schwelle). Gleiche Behandlung wie W25: offen, kein Tot-Stempel, nicht in dieser Runde |
| XD-W15b | 54, Grenzwertig | **Story fällt durch, nicht bauen**: Träger hat auf der Short-Seite keine Roh-Edge (#098/#099 zweimal Münzwurf, IS+OOS, `vwap_pullback.py` deshalb hart long-only codiert) | **Nicht bauen.** Nur wieder aufmachen mit eigenständigem Beleg für Short-Roh-Edge in der ES-bestätigten Teilmenge |
| XD-W5a | 216, Grenzwertig | Story hält mit Vorbehalt: Bestätigungs-Uhr fehlt im Text (#066/#067-Formulierung, Look-ahead-Risiko) | **Nachbessern, dann H()-Zeile.** Fix: Bestätigungsfenster explizit geschlossen vor Entry, Look-ahead-Delay-Kontrolle aus `controls.py` Pflicht, Level-Art wählen die `min_tpy=25` erreicht (5,3 % Basisrate ≈ 13 Ereignisse/Jahr reicht allein nicht) |
| XD-W5b | 216, Grenzwertig | Story hält mit Vorbehalt, gleiche Auflagen wie W5a + Long-Bias-Kontrolle (#108) Pflicht | **Nachbessern, dann H()-Zeile — zusammen mit W5a als EINE Trial-Familie**, nicht zwei |

**Ergebnis dieser Runde: 2 von 8 ursprünglichen Skeletten gehen weiter** (XD-W12a einzeln, XD-W5a+b als eine Familie), beide erst nach den genannten Nachbesserungen. 6 sind draußen — 3 davon mit Tür offen ohne Tot-Stempel (W13, W25, W15a — Research widerlegt / Prämisse schwach), 3 klarer ausgeschlossen (W12b, W15b, W27a/b — Varianten-/Story-Check gescheitert bzw. Research widerlegt).

**Update 17.09.2026 (Hauptsession, nach ein-weg):** Spec B ist gebaut, geprüft und **enqueued**. `sigcore.xref_signal()`/`xref_confirm()` (z-Score-basiert gegen 60-Tage-Streuung, kein fester Prozentsatz, Default aus, entry_min-Assert gegen Look-ahead) plus `tm_xref_*`-Parameter und Hook in `qbt._reversal_trades` (vor `tm_null`).

**pipeline-auditor-Runde 1 fand einen echten Blocker:** das erste Grid (`tm_xref_len=[15,30,60]` bei `rev_signal_min=15`) hätte in 20 von 30 Configs ES-Kurse bis zu 45 Minuten NACH dem Fill gelesen (#066/#067) — die Edge wuchs dabei nur mit der Menge an Zukunftsinformation (Faktor 4,8 im Extremfall bei ehrlich 0,20-0,22 expR). Gefixt: harter `AssertionError` in `xref_confirm()` wenn `tm_xref_start+tm_xref_len > entry_min`, Grid auf `tm_xref_len=[5,10,15]` bei fixem `tm_xref_start=0` beschränkt (strukturell sicher), `controls.ctl_delay` verschiebt `tm_xref_start` jetzt mit (sonst hätte der Look-ahead-Selbsttest das Gate selbst nie erwischt), `controls.ctl_symbols` überspringt Märkte, die mit `tm_xref_sym` kollidieren (sonst ES-Selbstbestätigung). Runde 2: **sauber mit Auflagen**, `pipeline_ok` gesetzt.

**Erwartungsmanagement (pipeline-auditor, frisch gerechnet):** auf der `open`-Basis liegt expR (0,15-0,20) UNTER dem ungegateten Original (0,224) — dort kommt kein Kandidat. Die `prev_close`-Configs sehen mit 0,26-0,41 besser aus, haben aber nur 164-527 Trades über ~10,5 Jahre (16-50/Jahr) und laufen vermutlich in die Trades/Jahr-Gates; zusätzlich ist `prev_close` inhaltlich eine ANDERE Behauptung als das Why (Overnight-ES-Gap statt Intraday-Bestätigung) — Punkt für strategy-auditor/verdict-auditor bei der Auswertung. **Wahrscheinlichstes Ergebnis: 0 Kandidaten**, aber ein sauberer, look-ahead-freier Job.

**engine-regression-tester:** alle 6 Buch-Beine + beide Kanarien bitgleich zur Baseline, `regression_ok` gesetzt.

**Enqueued:** `hyp_XD12_NQ` steht `pending` in der (Box-)Queue, Runner neu gestartet (Stop→Start, 17.09. ~09:10 Boxzeit) — läuft jetzt mit dem neuen Code. Ticket **AP182** (Vorab-Messung als Register-Nachtrag, fällig vor der Auswertung von hyp_XD12_NQ, kein Enqueue-Blocker).

**Nebenfund:** während des Regressionslaufs schrieb eine andere parallele Session gleichzeitig an `hypothesis_bank.py` (SES-W16a/W42a, Session-Momentum-Karte) — inhaltlich harmlos, XD-12 unangetastet, aber ein session-guard-Fall zum Vormerken.

**Spec A (`mb_kind="smt"` in `maband.py`, für W5a/b) ist NICHT gebaut.** Der bestehende Signal-Dispatcher in `maband.py` (`dist`/`cross`/`slope`/`fan`/`speeds`) arbeitet mit vorberechneten Linien eines EINEN Symbols pro Bar; SMT braucht eigenen Zustand (laufende Extreme, Ausbruchs-Event, Bestätigungsfenster, Cross-Symbol-Y-Zustand) und passt architektonisch nicht in diesen Dispatcher. Das ist ein eigener, sorgfältiger Bau-Schritt, kein Anhängsel — offen für eine dedizierte Session/Runde.

## Modul-Specs (Kurzfassung, Details im Report)
- **Spec B, Cross-Index-Gate** (~95-110 Z.):
  - Helper `sigcore.xref_confirm()` mit `tm_xref_sym/_base/_min/_ratio/_invert`
  - Basen: `open`, `prev_close`, `vwap_side`, `prev_day_rel` (W25), `rel` (W27)
  - Hooks in `qbt._reversal_trades`, `qbt._last_hour_trades`, `vwap_pullback.trades`, `asian.trades`, `sigcore.gates_pass`
  - Default aus = bitgleich, `engine-regression-tester` vor Sync
  - Circular-Shift-Placebo ist laut #136 noch nicht in `controls.py` codiert, der Job muss ihn selbst mitrechnen
- **Spec A, `mb_kind="smt"`** in `maband.py` (~105-125 Z.):
  - Parameter: `mb_smt_ref/_level/_or_min/_evt/_fail_n/_ystate`
  - Ref-Frame auf gemeinsame Zeitstempel ausgerichtet, Level nur aus Vergangenheit (Vortag mit `shift(1)`)
  - `mb_rand_level` tick-treu auf beiden Symbolen, `NULL_REF_BY_MODE`-Zeile, Overnight-Level erst mit 24h-Loader
- **Spec C, Tagesbars:** nur für den Swing-Merker W24, nicht bauen.

## Reihenfolge nach Buch-Chance
1. XD-W12a: Ersatz Momentum, long
2. XD-W12b: Ersatz Momentum, short
3. ~~XD-W13a: Ersatz LastHour, long~~ (Research widerlegt, nicht in dieser Runde)
4. XD-W15a: Ersatz VWAP-Pullback, long
5. XD-W15b: Ersatz VWAP-Pullback, short
6. ~~XD-W25a: Ersatz Momentum über Vortags-Führung, long~~ (Vorab-Messung 17.09.: Prämisse nicht bestätigt, nicht widerlegt, kein Job in dieser Runde)
7. ~~XD-W25b: Ersatz Momentum über Vortags-Führung, short~~ (dito)
8. XD-W5a: SMT-Fade short, neues Bein
9. XD-W5b: SMT-Fade long, neues Bein
10. ~~XD-W27a: späte Divergenz long, neues Bein~~ (Research widerlegt, nicht in dieser Runde)
11. ~~XD-W27b: späte Divergenz short, neues Bein~~ (Research widerlegt, nicht in dieser Runde)

**An ein-weg in dieser Runde (6):** XD-W12a, XD-W12b, XD-W15a, XD-W15b, XD-W5a, XD-W5b. XD-W25a/b seit 17.09. draußen (Vorab-Messung, s.o.), gleiche Behandlung wie W13/W27: kein Tot-Stempel, nur nicht in dieser Rechenrunde.

**Vorab-Messung, bevor Rechenzeit fließt (11 Skelette sind die Obergrenze):**
- Basisrate „ES zieht nicht mit“ an NQ-Momentum-Tagen. Unter ~15 % bindet das Gate kaum, dann fallen W12, W13 und W15 praktisch weg.
- RS-08-Übergangsmatrix. Fällt sie, fällt W25 ohne Trial.
- ZF-05-Prämisse per `rv`. Fällt sie, fällt W27.
- Basisrate „X nimmt Level, Y nicht“ je Level-Art und Y-Zustand (für W5/W29).

## Research-Stand (16.09.2026, research-scout)

| Skelett | why_status | Quelle | ein-weg diese Runde |
|---|---|---|---|
| XD-W12a | offen | Cache Z.30/476/699, Brown/Goetzmann/Kumar 1998 | ja |
| XD-W12b | offen | wie W12a, Shen 2022 (Cache Z.509) | ja |
| XD-W13a | **widerlegt** | Logbuch #087, Cache Z.515 | **nein** (kein Tot-Stempel) |
| XD-W15a | offen | Cache Z.1087 (Lücke) | ja |
| XD-W15b | offen | Cache Z.1087 (Lücke) | ja |
| XD-W25a | offen | Bank Z.127 (RS-08), Jegadeesh 1990, Lehmann 1990 | ja |
| XD-W25b | offen | wie W25a | ja |
| XD-W5a | offen | LuxAlgo/FXOpen/TradingFinder (Retail, ohne Zahl) | ja |
| XD-W5b | offen | wie W5a, #108 Long-Bias | ja |
| XD-W27a | **widerlegt** | Bank Z.166 (ZF-05 kontaminiert), #087, Cache Z.515 | **nein** (kein Tot-Stempel) |
| XD-W27b | **widerlegt** | wie W27a | **nein** (kein Tot-Stempel) |

Kein Skelett ist belegt, deshalb wurde kein Why umgeschrieben. „Research widerlegt“ heißt nur: nicht in dieser Rechenrunde. Tot ist ein Weg erst nach vollem Test.

## Offene Research-Fragen
1. Ist marktbreites Intraday-Momentum in Index-Futures belegt stärker als Einzelindex-Momentum? (W12)
2. Setzen sich marktbreite Abverkäufe stärker fort als marktbreite Anstiege? (W12b)
3. Ist das Schlussstunden-Momentum an indexweite Flows gebunden? (W13)
4. V9: Steckt Information im relativen VWAP-Abstand zweier Index-Futures, nutzbar als Richtungsfilter? (W15, W23)
5. Dow-Theorie, Intermarket-Nichtbestätigung, SMT: Gibt es Belege, dass nicht bestätigte Extreme öfter scheitern? Gibt es eine Asymmetrie zwischen Hoch und Tief? (W5)
6. Hält relative Stärke zwischen Index-Futures kurzfristig (1-5 Tage) an, oder dreht sie meist? (W25)
7. Laufen Index-Divergenzen in der letzten Handelsstunde weiter, und sind MOC-Imbalances je Index unterschiedlich gerichtet? (W27)

## Verwandte Notizen
[[Strategie-Logbuch]] · [[Hypothesen-Bank (Pairs Trading & Relative Value)]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[VWAP-Offensive]] · [[Fibonacci Wege-Karte]] · [[Familien-Scout Agent]] · [[Research-Cache]] · [[Discovery-Runner v2]] · [[Strategie-Familien]]

Dateien: Report `engine/discovery/scout_reports/familien_es_nq_divergenz_260916.md` · Skelette `engine/discovery/jobs_proposed/familien_es_nq_divergenz_260916.json`
