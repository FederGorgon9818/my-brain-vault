---
tags: [projekt, trading, alpha-suche, adx]
erstellt: 2026-09-21
aktualisiert: 2026-09-21
research_stand: 2026-09-21
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das ADX-Kapitel in einem Lauf sauber schließen
---

# ADX Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 21.09.2026 vom `familien-scout` (Auftrag Max, Markt-Fokus ES/NQ Intraday). **Nachtrag am 21.09.2026 nach `verdict-auditor`-Gegenlesen:** 8 fehlende Wege ergänzt (W32-W39), 6 Stände korrigiert, 5 übersehene Tote nachgetragen, Register-Tabelle auf nachgezählte Zahlen gesetzt, Rangfolge neu. Bestehende Weg-Nummern wurden **nicht** umnummeriert. **Research-Rückschrieb am 21.09.2026** (Workflow `konzept-weg`, nach `research-scout`): je Skelett steht der Stand jetzt im eigenen Abschnitt und gesammelt im Block „Research-Stand (21.09.2026)". Ergebnis: **ein** Beleg-Treffer (W38), **zwei** Herabstufungen von „belegt" auf „offen" (W15, W29), **kein** Weg widerlegt. Nichts gelöscht, nichts umnummeriert, keine Stempel angefasst.

Inventar gegen Register (65.035 Trials), Queue (1.004 Jobs, 0 pending), `ideas.json` (64), Engine-Quellcode, [[Strategie-Logbuch]] #046/#080/#111/#116/#133/#136/#139/#141/#142/#147/#150/#162, [[Hypothesen-Bank (Momentum & Averages)]] (AR-15/AR-16/AR-17/AR-04/AR-14/AR-06/TS-03/TS-11/AV-02/AV-13/AC-02/AC-06/AC-06b/AC-09/AS-08/AK-01), [[Research-Cache]] (Z. 828, Z. 872-884, Z. 1130) und [[Friedhof-Analyse (17.09.2026)]] (`karten_scouts_labs.md` Z. 288). Aufbau nach dem Vorbild [[VWAP-Offensive]] (Hand-Karte zu einem anderen Konzept, hier nicht angefasst). Schwester-Karten desselben Agenten: [[Fibonacci Wege-Karte]], [[Rundzahlen Wege-Karte]], [[Session Momentum Wege-Karte]], [[ES-NQ-Divergenz Wege-Karte]].

> [!warning] Zwei Sätze, die über die ganze Karte entscheiden (Satz 1 am 21.09. korrigiert)
> **1. ADX existiert in der ENGINE nicht — im VAULT schon, mit Tötungs-Stempel.** Engine-Seite geprüft und bestätigt: **0 Treffer** in allen `*.py` (die Rohtreffer sind `dmi` in `admin` bzw. in `Bandmittellinie`), **0 von 65.035** Register-Trials, **0 von 1.004** Queue-Jobs, **0 von 64** `ideas.json`-Einträgen. Kein einziger Weg ist heute als `H()`-Zeile baubar. **Aber:** die [[Friedhof-Analyse (17.09.2026)]] führt unter `karten_scouts_labs.md` Z. 288 den Eintrag **#196 — „VWAP Z-Score Mean-Reversion, regime-gefiltert"** auf MNQ/MES mit dem Filter **„ADX < 20-25"**, Status laut Strategie-Katalog #002/#003 **NO-GO**. Der Originaltext steht in [[QuantPad Brief - VWAP Mean Reversion]] Z. 82. ADX ist bei uns also **einmal gelaufen und einmal getötet** — und zwar auf genau dem Mechanismus von **W6**. Die Zufallsdecke ist gegen ADX noch nicht gelaufen, die Jungfräulichkeit ist es nicht.
> **2. ADX ist kein Preis-Level, sondern eine ATR-normierte Statistik.** Niemand handelt an `ADX = 25`. Damit fallen alle Wege weg, die auf Reflexivität am Wert bauen (abprallen an der Schwelle, Kreuzung scheitert, ADX × ADXR). Übrig bleiben genau drei Story-Typen: **Zustands-Konditionierung**, **Richtung aus dem DI-Spread** (= MA-Crossover in anderer Gewichtung, Levine/Pedersen) und **Turnover-/Kostenersparnis** — nur letzteres ist belegt.

> [!important] Die Beweislage ist dünn, und das gehört vorne hin
> Zu ADX selbst gibt es **keine akademische Primärzahl**. Park/Irwin (J. Economic Surveys 2007) nennt ADX/DMI ohne isolierte Kennzahl; der einzige Praktiker-Fund ist eine Richtungsaussage ohne Effektstärke. Belegt ist genau eines: **Baltas/Kosowski 2013** — ein *kontinuierliches* Trendstärke-Signal statt eines binären senkt den Turnover um mehr als ein Drittel **bei gleicher Performance, nicht bei höherer Sharpe**. Gegen das Konzept stehen **Nilsson 2015** und **CFM/Bouchaud 2016**: die kurzfristige Autokorrelation moderner Futures ist nahe Null. Deshalb stand bei 11 von 15 Skeletten `why_status: entwurf`. **Nach dem Research-Rückschrieb 21.09. sind es 12 von 15 `offen` und 3 `belegt`** — W19/W20 hausintern belegt, W38 neu peer-reviewt belegt (Schmidhuber 2021). Die Research-Runde hat die Lücke also nicht geschlossen, sondern bestätigt.
>
> **Präzisierung 21.09. (Auditor):** Baltas/Kosowski ist im Original eine **Gewichtungs**-Aussage (stetiges Signal statt Vorzeichen), keine Aussage über die Entry-Latte. W15 überträgt sie auf die Schwelle — das ist eine Analogie, keine Replikation. Die wörtliche Gewichtungs-Form steht jetzt als **W32** in der Karte und hat bei uns **keine Story**, weil Min-Size (1 Kontrakt je Bein, #106) jede stetige Response auf binär zusammenfaltet (Bank **AS-08** sagt genau das).
>
> In der Bank liegt das schon halb: **AR-16 existiert als hinterlegte, ungetestete Zeile** und sagt dort selbst „nicht zwingend ADX — dazu existiert keine akademische Primärzahl". Diese Karte doppelt AR-16 nicht, sie ist das Dach darunter. **Dieselbe Sorgfalt jetzt auch gegenüber TS-03, AS-08, AC-06, AC-09** — siehe die Verwandten-Spalten unten.

---

## Die sieben harten Randbedingungen

**1. Die Gate-Form ist zweimal durchgemessen und zweimal ohne Kandidat — zusammen 533 Trials.**
[[Strategie-Logbuch]] #136 (AR-15, 200d-MA-Tagesmaske, **353 Trials**, Familien-Null p=0,16; Pflichtvariante +2,37 pp, aber Episoden-Kippe 348 %, LOLO-Kippe 3/5, Delay 1→2 −61 %, **Vola-Confound: matched RV20-Gate 3× stärker**) und #139 (AR-17, Vola-Tagesmaske, **180 Trials**, COVID-freie Familien-Null p=0,30). Jeder ADX-Weg, der „Tages-Zustand an/aus über die Buch-Beine" sagt, wärmt diese Achse auf und braucht einen **neuen** Grund.

**2. Die Off-Tage-Malus-Kurve (#139 Lehre 2).**
Zufälliges Abschalten kostet unter dem Trailing-DD-Käfig monoton: **−0,8 pp schon bei 5 % Off-Tagen**, −1,47 bei 32 %, bis −44,8 pp bei 85 %. Jedes An/Aus-Gate muss diesen Malus erst überwinden, bevor es überhaupt Information beweisen kann. Dazu der **θ-Vorfilter** (#139 Lehre 3): tragen kann ein Tages-Gate nur, wenn **r_σ² > r_µ**; mechanische Hürde r_σ ≳ 1,16, Beweisbarkeits-Hürde bei unserem Sample r_σ ≥ ~1,6. **Das ist ein Vorab-Check, kein Nachtest.**

**3. Der Power-Deckel (#162).**
Die drei Buch-Beine haben **798 / 967 / 264** Trades gesamt (OOS 244 / 293 / Asia nicht auswertbar). Für 10 Gate-Varianten × 3 Beine mit Bonferroni bräuchte es 22-217× mehr Trades; Power dort **0,03-0,10**. Jede Gate-Achse bekommt **einen vorregistrierten Test**, kein Grid. Mehr Rechenzeit hilft nicht, nur mehr Jahre.

**4. Ersatz schlägt neu (#139 B3).**
577 Buch-Evals mit `replaces_leg=None`: Median −12,3 pp, Max +0,8 pp, **0 Treffer jemals**. Alle 14 Kandidaten-Jobs der Historie waren **Ersatz oder Exit**.

**5. ADX ist ATR-normiert und damit Vola-verwandt.**
DX = |+DI − −DI| / (+DI + −DI), beide DI durch ATR normiert. Strukturell ein Verhältnis zweier Vola-Größen. #136 hat genau diese Falle einmal aufgedeckt. **ADX muss gegen `atr_exp`/`sigma_q` antreten, nicht gegen „kein Gate".** Einzige Ausnahme in dieser Karte: **W36**, wo die Vola-Größe absichtlich als zweites Element in der Konjunktion steht statt als Confounder darunter.

**6. Kein neuer `mode`, nie.**
`controls.ctl_null` kennt sechs Modi (`controls.py` Z. 667-668: `tsmom · maband · ts_reversal · last_hour · asian · vwap_pullback`). Alles außerhalb bekommt `ok=None` → `skipped_required` → kann **nie** `deploy_ready` werden (#139 B1). ADX gehört in `sigcore`/`maband`/`tsmom`. Zusatzfalle: `sigcore.gates_pass` wird heute **nur** von `tsmom.py` (Z. 372) und `maband.py` (Z. 543) aufgerufen — die drei Buch-Modi brauchen je ~10-15 Zeilen Verdrahtung, obwohl sie seit AP157 einen Null-Schalter haben.

**7. ⭐ NEU (21.09., Auditor): Der Exit-Block ist der dichtest gemessene Bereich der ganzen Karte — dichter als die Gate-Form.**
Das war in der Erstfassung untergewichtet und ist die wichtigste Korrektur dieses Nachtrags. Preis-Trailing und Break-even sind bei uns **viermal** unabhängig tot gegangen:
- **#046** (29.07.2026, NO-GO): **0 von 8 Beinen überlebte den OOS-Test**, 5/8 zeigten IS-Verbesserung, **alle 5 kollabierten OOS**. „MAE sinkt real, aber gekappte Gewinner fressen den Effekt auf." `ideas.json`-Eintrag „Break-Even/Trailing-Stop-Overlay (generisch, alle Beine)", Status **Getötet** — der Eintrag trägt kein „ADX" im Namen und wurde in der Erstfassung deshalb übersehen.
- **#142** (03.09.2026): MFE-Spalte `mfe_r` seitdem in allen Trade-Records instrumentiert, bar-genaues Counterfactual auf zwei Buch-Beinen, 10 Configs je Bein. **„Leg-Level: keine Config schlägt OFF"**, weder expR noch OOS noch letzte 3 Jahre. Bester Buch-Wert VWAP BE0,5 **+1,16 pp ± 0,25** → besteht den 2×-Rausch-Test, **scheitert an der 1,5-pp-Hürde**. **Cross-Leg-Replikation 0/12 Zellen positiv.** BE-Komponente auf v2 +2,95 pp mit 90 %-CI **[−0,86; +7,25]** = neutral; auf expR **signifikant negativ** (−0,148 R, p 0,025).
- **#147** (09.09.2026, NQ) und **#150** (10.-11.09.2026, ES/YM/RTY): First-Bar-EMA-Trail, vier `ideas.json`-Einträge, alle **Getötet**. #147 wörtlich: **„Trail beschneidet nur Gewinner (6,6k → 17,4k $ ohne Trail)"** — und das Bein dort ist nach Abzug **„NQ_Momentum_d260818 mit 5 statt 15 Min"**, also genau das Bein, das W27 ersetzen will. #150: je 2.880 + 144 + 72 Configs auf drei Symbolen, **0 positiv**.
- **Register (nachgezählt 21.09.):** `trail_ticks` **2.880** Trials / 109 Survivors · `be_trigger` 1.581 vorhanden (874 aktiv) / 672 Survivors · `trail_trigger` 759 vorhanden (393 aktiv) / 299 Survivors · `trail_dist` **743** / 283.

**Konsequenz:** W27 behält sein Skelett — ein Zustands-Trailing ist ein anderer Mechanismus als ein Preis-Trailing —, fällt aber von **Rang 2 auf Rang 5** und trägt die volle Verwandtenliste. Was in der Erstfassung als „Exit schlägt beides" gelesen werden konnte, war falsch: Exit ist die Kategorie mit belegter Buch-**Chance** (#139 B3) und gleichzeitig die mit dem dichtesten **Friedhof**.

---

## Register-Stand (21.09.2026, nachgezählt): wogegen ADX antreten muss

Zählkonvention ab jetzt explizit, weil die Erstfassung sie stillschweigend gemischt hat: **aktiv** = Parameter vorhanden, nicht `None` und nicht `0`. **vorhanden** = Schlüssel im Params-Dict, egal mit welchem Wert.

| Achse | Trials | Survivors | Buch-Kandidat |
|---|---|---|---|
| `tm_er_min` (Kaufman-ER, `sigcore` Z. 191) | 168 aktiv (297 vorhanden) | 16 (51) | 0 |
| `rev_er_min` | 58 aktiv (115 vorhanden) | 43 (84) | 0 |
| `er_thr` | 147 | 84 | 0 |
| **ER-artige Achsen zusammen** | **373 aktiv** | **143** | **0** |
| `mb_kind="slope"` (MA-Steigung) | 355 | 72 | 0 |
| `tm_signal="signratio"` | 5.124 | 231 | 0 |
| `tm_sigma_q_*`-Gate | 313 | 55 | 0 |
| `tm_atr_exp_*`-Gate | 19.400 | 13 | 0 |
| `regime` ∈ {trend, range} (Legacy) | 122 | 36 | 0 |
| `regime` ∈ {trend, range} **∪** `er_thr` | **197** | **84** | 0 |
| `mode="regime_gate"` (AR-15/AR-17-Backfills) | 530 | 0 | 0 |
| `tm_xref_min` (NQ/ES-Kopplung) | 24 aktiv (30 vorhanden) | 0 | 0 |
| alle `tm_xref*`-Schlüssel | 31 | 0 | 0 |
| `tm_base="overnight"` | 145 | 0 | 0 |
| `trail_ticks` / `be_trigger` / `trail_trigger` / `trail_dist` | 2.880 / 1.581 / 759 / 743 | 109 / 672 / 299 / 283 | 0 |
| `mb_kind="band"` | 179 | 1 | 0 |
| **ADX selbst** | **0** | **0** | **0** |

**Drei Korrekturen gegenüber der Erstfassung** (alle vom `verdict-auditor` gefunden, alle nachgezählt und bestätigt):
1. Die Zeile „`qbt`-Regime-Gate (`regime`/`er_thr`, Legacy) 122 / 36" war **falsch etikettiert**: 122/36 ist ausschließlich `regime` ∈ {trend, range}. `er_thr` allein ist 147/84, die Vereinigung **197/84** (Schnitt 72/36). Die Survivor-Zahl war damit um Faktor 2,3 zu niedrig ausgewiesen. **Nebenbefund:** `mode="qbt"` existiert im Register **gar nicht** (0 Treffer) — die Legacy-Trials laufen unter `ts_reversal` (147), `continuation` (48) und `reversion` (2). Das Etikett „qbt" war frei erfunden und ist raus.
2. Die ER-Nachbarschaft ist **mehr als doppelt so dicht** wie ausgewiesen: nicht 168/16, sondern **373 Trials / 143 Survivors** über `tm_er_min` + `rev_er_min` + `er_thr`. Betrifft W6 und W20.
3. Die xref-Zeile („30 Trials / 0 Survivors") steht dreimal in Karte, Report und JSON. **Teil-Widerspruch zum Auditor:** 30 ist keine Phantasiezahl, sondern `tm_xref_min` **vorhanden** — eine der beiden legitimen Lesarten. Verdikt-ändernd ist nichts (0 Survivors in jeder Lesart), aber die Zeile ist jetzt eindeutig: **24 aktiv / 30 vorhanden / 31 über alle `tm_xref*`-Schlüssel**.

**Buch-Fingerprint dieser Karte:** `book_state.json` = 3 Beine — `NQ_Momentum_d260818`, `NQ_LastHour_v3`, `NQ_Asia-Dir-USopen_d260820`. `book_state_next.json` identisch. `NQ_VWAP-Pullback` ist seit #161 raus.

---

## Die 39 Wege

Mechanisch aus **Elementen × Beziehungen × Richtung**. Elemente: Preis · +DI · −DI · DI-Spread (signiert) · DX/ADX (vorzeichenlos) · Schwellen 20/25/40 · ADX-Steigung · ADXR · ATR/TR (Nenner) · zweiter Anker (Tages-ADX, ES-ADX, **zweiter Zeitrahmen**) · **Positionsgröße**. Bewegungen: hin zu · weg von · durch hindurch · abprallen an · entlanglaufen an · kreuzen und halten · kreuzen und scheitern. Zustände: steigt / fällt / flach · eng / weit / **wechselt**.

*(W32-W39 kamen am 21.09. durch den `verdict-auditor`-Nachtrag dazu. Die Zustandsachse **„wechselt"** war in keiner der ersten 31 Zeilen besetzt — W6 ist „eng", W4 ist „weit", W3 ist EINE gescheiterte Kreuzung. Sie ist jetzt W33.)*

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W1** | +DI kreuzt −DI nach oben und hält (**long**) | Trend | Signal | offen | MS-3 | Ersatz `NQ_Momentum` |
| **W2** | −DI kreuzt +DI nach oben und hält (**short**) | Trend | Signal | offen | MS-3 | Ersatz `NQ_Momentum` |
| **W3** | DI-Kreuzung scheitert | Mean Reversion | Signal | offen | MS-3 | — |
| **W4** | DI-Spread spreizt sich auf (weg von) | Trend | Signal | offen | MS-3 | Ersatz `NQ_Momentum` |
| **W5** | DI-Spread läuft zusammen, Preis läuft weiter | Trend | Exit | offen | MS-3 + MS-4 | Ersatz `NQ_Momentum` |
| **W6** | DI-Linien laufen eng nebeneinander entlang (Chop) | Mean Reversion | Zeitfenster | **korrigiert:** offen, aber **Verwandter mit Tötungs-Stempel (#196)** + ER-Achsen 373 Trials / 143 Surv. + voller Buch-Replace-Test (#080) | MS-3 | neues Bein |
| **W7** | ADX durch 25 **von unten**, hält | Trend | Filter | gemessen ohne Kandidat (**533 Trials**) | MS-1 + MS-2 | Ersatz `NQ_Momentum` |
| **W8** | ADX durch 25 von unten, scheitert sofort | Mean Reversion | Signal | offen | MS-3 | — |
| **W9** | ADX durch 25 **von oben** | Trend | Exit | offen | MS-3 + MS-4 | Ersatz `NQ_Momentum` |
| **W10** | ADX prallt von oben an 25 ab | Trend | Signal | offen | MS-3 | — |
| **W11** | ADX läuft flach **unter 20** entlang | Mean Reversion | Zeitfenster | offen | MS-3 | deckt sich mit W6 |
| **W12** | ADX läuft **über 40** entlang (Plateau) | Trend | Filter | offen | MS-3 | — |
| **W13** | ADX **steigt** (Steigung > 0) | Trend | Filter | offen (Niveau-Form gemessen) | MS-1 + MS-2 | Ersatz `NQ_Momentum` |
| **W14** | ADX **fällt** von hohem Niveau (>40) | Mean Reversion | Signal | offen | MS-3 | neues Bein |
| **W15** | ADX moduliert die **Schwelle** stetig | Trend | Filter | offen | MS-1 + Modulator | Ersatz `NQ_Momentum` |
| **W16** | Preis neues Extrem **mit** steigendem ADX | Trend | Filter | offen | MS-3 | deckt sich mit W13 |
| **W17** | Preis neues Extrem **ohne** ADX (Divergenz) | Mean Reversion | Signal | offen; Verwandter tot (#133) | MS-3 | neues Bein |
| **W18** | ADX kreuzt ADXR | Trend | Signal | offen | MS-3 | — |
| **W19** | ADX gegen den eigenen Nenner: **nur Vola-Proxy?** | Filter | Messweg | offen | MS-1 + MS-5 | kein Bein |
| **W20** | ADX gegen ER / slope / signratio (**Redundanz**) | Filter | Messweg | **korrigiert:** offen, Verwandte **373 Trials / 143 Surv.** + Buch-Replace-Test #080 gelaufen | MS-1 + MS-5 | kein Bein |
| **W21** | Tages-ADX hoch → Momentum an | Trend | Filter | gemessen ohne Kandidat (533 Trials) | MS-1 + MS-2 | Ersatz `NQ_Momentum` |
| **W22** | Tages-ADX niedrig → MR/Fade an | Mean Reversion | Filter | gemessen ohne Kandidat (#139: Gegenrichtung ≈ 0) | MS-1 + MS-2 | — |
| **W23** | Tages-DI-Spread als **Richtungs-Bias** | Trend | Filter | offen | MS-1 + MS-2 | Ersatz `NQ_Momentum` |
| **W24** | **ES**-ADX als Gate für das NQ-Bein | Trend | Filter | offen (AR-06 nie voll getestet; xref **24 aktiv / 30 vorh. / 31 alle Schlüssel**, 0 Surv.) | MS-1 + MS-2 | Ersatz `NQ_Momentum` |
| **W25** | ADX-Spread NQ − ES | Relative Value | Signal | offen (xref-Zahl wie W24 korrigiert) | MS-1 je Symbol | — |
| **W26** | ADX-Aufbau nach Open vs. Mittag | Intraday Bias | Zeitfenster | offen | MS-3 | — |
| **W27** | ADX fällt vom **Trade-Peak** | Trend | Exit | **korrigiert:** offen, aber **Exit-Block viermal tot** (#046, #142, #147, #150) + 5.963 Trailing-Trials | MS-3 + MS-4 | Ersatz `NQ_Momentum` |
| **W28** | Stop-/Zielweite an ADX statt ATR | Trend | Exit | offen; Verwandter breit gemessen | MS-1 + MS-4 | — |
| **W29** **(Swing)** | Tages-/Wochen-ADX, Mehrtages-Trendfolge | Swing | Signal | offen | MS-1 + Overnight-Logik (fehlt) | **Live-Buch-Merker** |
| **W30** | ADX des Globex-Segments → RTH-Vorzeichen | Intraday Bias | Filter | **korrigiert:** offen, **Verwandter dünn gemessen** (`tm_base="overnight"` nur **145 Trials** / 0 Surv.) | MS-3 | — |
| **W31** | ADX auf Bar-**Range** gegen Close-zu-Close | Filter | Messweg | offen | MS-5 | kein Bein |
| **W32** *(neu)* | ADX/DI-Spread als stetiges **Sizing-Gewicht** (Positionsgröße ∝ Trendstärke) | Trend | Sizing | **offen, aber ohne Story** (Min-Size, AS-08) | MS-1 + Sizing-Schicht | kein Bein |
| **W33** *(neu)* | DI-Spread **wechselt** das Vorzeichen k-mal in N Bars (Whipsaw-Zähler) | Mean Reversion | Filter | offen | MS-3 + MS-6 | Ersatz `NQ_Momentum` |
| **W34** *(neu)* | **Erste** DI-Kreuzung des Tages gegen spätere (Ordnungsnummer) | Intraday Bias | Signal | offen; **gehört zu AC-09**, nicht hierher | MS-3 + Kreuzungszähler | — |
| **W35** *(neu)* | **Kreuzungswinkel**: Änderungsrate des DI-Spreads IM Moment der Kreuzung | Trend | Signal | offen; Verwandter **tot** (AC-06/AC-06b, 181 Trials, Buch-Marginal −6,5 pp) | MS-3 | — |
| **W36** *(neu)* | **ADX hoch × ATR niedrig**: gerichtet, aber ruhig (Konjunktion) | Trend | Filter | offen | MS-1 + `tm_adx_min` (ATR-Hälfte existiert) | Ersatz `NQ_Momentum` |
| **W37** *(neu)* | **Multi-Timeframe**: schneller Intraday-ADX gegen langsamen Intraday-ADX | Trend | Filter | offen; wartet auf W31 | MS-3 je Zeitrahmen | Ersatz `NQ_Momentum` |
| **W38** **(Swing)** *(neu)* | **W14 in der Mehrtages-Fassung**: ADX-Rollover über Nacht gehalten | Swing | Signal | offen | MS-1 + Overnight-Logik (fehlt) | **Live-Buch-Merker** |
| **W39** **(Swing)** *(neu)* | **W25 in der Mehrtages-Fassung**: ADX-Spread NQ−ES als Paar-Trade über Tage | Swing | Relative Value | offen | MS-1 je Symbol + Overnight-Logik (fehlt) | **Live-Buch-Merker** |

---

## Wege ohne Story (stehen bewusst da, damit sichtbar ist, dass nichts übersprungen wurde)

- **W3, W8 — keine Story, weil kein Akteur am ADX-Wert handelt.** Ein „gescheiterter" Durchgang einer geglätteten Statistik ist Rauschen um die Schwelle, nicht ein enttäuschter Käufer. Bei einem Preis-Ausbruch gibt es die Leute, die zu früh gekauft haben; bei ADX=25 gibt es niemanden.
- **W10 — keine Story, weil ADX kein Preis ist.** Es gibt nichts, woran abgeprallt werden könnte. Die 25 ist eine Konvention aus Wilders Buch von 1978, keine Order-Ebene.
- **W12 — keine eigene Story**, Reparametrisierung von W7/W13 (anderer Schwellenwert, kein eigener Zustandswechsel). Zählt nicht als eigener Weg und darf nicht als eigener Trial gezählt werden.
- **W16 — Story deckungsgleich mit W13** (steigender ADX), kein eigenes Ereignis.
- **W18 — keine Story, weil ADXR nur ADX mit Lag ist.** Die Kreuzung ist ein Nullpunktdurchgang derselben Größe — genau die Lehre aus AC-02 („Die Kreuzung ist nur ein Nullpunktdurchgang; der normierte Abstand misst die Trendstärke").
- **W28 — keine eigene Story, weil ADX ATR-normiert ist.** Die Stopweite an ADX zu koppeln heißt, dieselbe Größe zweimal zu verwenden; `tm_stop_mode="atr"` ist im Register breit besetzt.
- **W32 (Sizing-Gewicht) — keine Story, weil Min-Size die Response-Funktion plattdrückt.** ⭐ Das ist die wörtliche Baltas/Kosowski-Form (stetiges Signal statt Vorzeichen als **Gewicht**, nicht als Latte). Bank **AS-08** liefert die fertige Begründung, warum sie bei uns nicht trägt: „Weil die Baz-Response-Funktion (tanh-Skalierung des Signals in eine Positionsgröße) unter Min-Size auf ein binäres Ja/Nein zusammenfällt, ist sie für uns wertlos — außer als Schwellenkalibrierung." Unser Betriebspunkt ist seit #106/v2 **Min-Size = 1 Kontrakt je Bein** (`book_state.json` Z. 64), also genau der Fall. **Der Weg bleibt in der Karte**, weil er sofort eine Story bekäme, wenn der Betriebspunkt je über Min-Size steigt — und weil W15 sonst fälschlich als „die" Baltas/Kosowski-Umsetzung gelesen wird. Der einzige heute verwertbare Rest ist AS-08s Schlusssatz: die tanh-Form taugt als **Schwellenkalibrierung** — und genau das ist W15.

## Wege mit Story, aber bewusst ohne Skelett

- **W17 (ADX-Divergenz)** — kontaminiert. #133 hat Divergenz nach Session-Open in **über 250 Arten** gemessen → Friedhof. Braucht einen neuen Grund; ich habe keinen.
- **W22 (ADX niedrig → Fade an)** — #139 hat die off-Anteil-**gematchte Gegenrichtung** explizit gemessen, Mittel −0,36 pp ≈ 0. Umdrehen ist kein neuer Winkel.
- **W25 (ADX-Spread NQ−ES)** — die NQ/ES-Kopplung hat eine eigene Karte ([[ES-NQ-Divergenz Wege-Karte]]); ein zweiter Agent auf derselben Kopplung hebt nur die Decke für beide. *(Die Swing-Fassung W39 ist davon nicht betroffen: sie geht nie in die Prop-Rechenrunde und hebt deshalb keine Decke.)*
- **W26 (ADX-Tageszeit)** — ADX wäre hier nur ein Proxy für die Uhrzeit, und die haben wir direkt (`tm_sig_start`, `tm_cutoff_min`, breit gemessen).
- **W30 (Globex-ADX)** — ⚠️ **Begründung am 21.09. korrigiert.** Sie lautete „`tm_base="overnight"`-Verwandte sind breit gemessen". Nachgezählt sind es **145 Trials / 0 Survivors** — das ist die **dünnste Zahl, die in der ganzen Karte als Tötungsgrund benutzt wurde**, und 145 Trials tragen das Wort „breit" nicht. Der Auditor hat recht. **Neue Begründung, reduziert auf das, was trägt:** ADX auf dünnem Globex-Volumen ist ein Vola-Artefakt-Kandidat, kein Zustand — die ±DM-Konstruktion liest in einem illiquiden Buch jede einzelne Lücke als gerichtete Range-Erweiterung, und genau das ist der Confound aus Randbedingung 5 in seiner schärfsten Form. **Stand deshalb: offen, Verwandter dünn gemessen** (nicht „abgeräumt").
- **W34 (erste DI-Kreuzung des Tages)** — ⭐ NEU, **Story vorhanden, Skelett gehört woanders hin.** Bank **AC-09** formuliert exakt diese Story schon: „Weil die erste Kreuzung des Tages den Übergang von der Übernacht-Bewertung in den RTH-Handel markiert, trägt sie mehr Information als jede spätere Kreuzung desselben Tages" (Messgröße: r_net je Kreuzungs-Ordnungsnummer; Status 🟢 offen, braucht nur einen Kreuzungszähler je Tag). Die DI-Fassung ist **dasselbe Elementpaar in anderer Gewichtung**. Genau wie bei AR-16 doppelt diese Karte das nicht: **der Weg steht hier, das Skelett gehört an AC-09.** Wenn AC-09 läuft, ist die DI-Fassung ein Arm darin, kein eigener Job.
- **W35 (Kreuzungswinkel)** — ⭐ NEU, **Story vorhanden, Verwandter tot.** Bank **AC-06** führt den Winkel ausdrücklich als **Gegenthese zu AC-02**: „Weil eine flache Kreuzung nur Rauschen ist, ist der Kreuzungswinkel (Änderungsrate der MA-Differenz) das entscheidende Kriterium und nicht der Abstand danach." Der Auditor hat recht, dass die Karte inkonsequent war: sie benutzt **AC-02, um W18 zu töten**, übernimmt aber die Gegenthese nicht. Nachgetragen — mit dem Befund, der die Sache entscheidet: **AC-06 ist inzwischen gelaufen und tot.** AC-06 selbst 71 Trials / 3 Survivors; Nachfolger **AC-06b** 110 Configs → 26 Survivors, aber `overfit.verdict` „kaputt" (Reality-Check p 0,13), **Buch-Marginal Ersatz Momentum −6,5 pp**, Verdikt `verdict-auditor` 14.09.2026: **„kein Kandidat"**, ausdrücklich **nicht** als „Edge belegt, nur kein Slot" zu führen. Zusammen 181 Trials auf der Winkel-/Abstands-Achse mit negativem Buch-Marginal. Der einzige denkbare neue Grund ist derselbe wie bei W6 — der DI-Winkel rechnet auf Hoch/Tief, der MA-Winkel auf Closes —, und **dieser Grund ist genau die Frage, die W31 misst**. W35 wartet damit auf W31, nicht auf mich. Kein Skelett.
- **W37 (Multi-Timeframe-ADX)** — ⭐ NEU, **Story vorhanden, wartet auf W31.** Die Story trägt: auf dem langsamen Zeitrahmen ist die gerichtete Range-Erweiterung intakt, auf dem schnellen bricht sie ein; der Akteur ist der Intraday-Trader, der auf dem schnellen Rahmen ausgestoppt wird, während die langsame Positionierung hält. **Das ist NICHT W18.** W18 (ADX vs. ADXR) ist die reine Lag-Fassung derselben Reihe und stirbt zu Recht am Nullpunktdurchgangs-Argument; ein 60-Minuten-ADX ist dagegen **keine Glättung** eines 5-Minuten-ADX, weil Hoch und Tief einer 60-Minuten-Bar nicht aus den ±DM der 5-Minuten-Bars rekonstruierbar sind. Die Bar-Aggregation ändert die gemessene Größe. **Aber:** damit ruht der ganze Weg auf genau einer Behauptung — dass die Hoch/Tief-Aggregation Information trägt, die die Close-basierten Maße nicht haben. Das ist wörtlich die Frage von **W31**, und W31 ist in dieser Karte der dafür zuständige Messweg. W37 bekommt ein Skelett, wenn W31 positiv ausgeht; vorher wäre es ein Job auf einer ungeprüften Prämisse. Kein Skelett.
- **W1/W2/W4/W5/W9/W11** — haben Story, sind aber entweder ein verkleidetes MA-Crossover (W1/W2/W4; AK-01 stellt diese Frage für die MA-Familie schon) oder decken sich mit einem höher gerankten Skelett (W5/W9 mit W27/W14, W11 mit W6). Sie bekommen ein Skelett, **sobald W19/W20 positiv ausgehen** — vorher nicht.

---

## Reihenfolge nach Buch-Chance (15 Skelette, Rangfolge am 21.09. neu)

Ersatz vor neu, engine-nah vor Modul-schwer, ohne tote Verwandte vor kontaminiert. **Drei Verschiebungen gegenüber der Erstfassung**, alle aus dem Auditor-Nachtrag:
- **W20 steigt 4 → 2:** die ER-Nachbarschaft ist mit 373 Trials / 143 Survivors doppelt so dicht wie ausgewiesen **und** hat mit #080 einen vollen Buch-Replace-Test hinter sich. Die Redundanzfrage entscheidet damit noch mehr als gedacht.
- **W36 kommt neu auf 3:** einziger Weg, der die Vola-Verwandtschaft (Randbedingung 5) nicht wegdiskutiert, sondern als zweites Element benutzt — und die ATR-Hälfte des Gates existiert im Code bereits.
- **W27 fällt 2 → 5:** Randbedingung 7 (Exit-Block viermal tot).
- **W6 fällt 8 → 12:** #196 nimmt W6 die Jungfräulichkeit auf genau seinem Mechanismus.

| Rang | ID | Weg | Rolle | Buch-Bezug | why_status | Stempel |
|---|---|---|---|---|---|---|
| 1 | `ADX-W19` | Ist ADX nur ein Vola-Proxy? | Messweg | kein Bein — **Torwächter** | belegt | offen |
| 2 | `ADX-W20` | Schlägt ADX ER / slope / signratio? | Messweg | kein Bein — **Torwächter** | belegt | offen |
| 3 | `ADX-W36` **(neu)** | ADX hoch × ATR niedrig | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 4 | `ADX-W15` | ADX moduliert die Schwelle stetig | Filter | Ersatz `NQ_Momentum` | **offen** (21.09. herabgestuft) | offen |
| 5 | `ADX-W27` | ADX-Peak-Trailing als Exit | Exit | Ersatz `NQ_Momentum` | offen | offen |
| 6 | `ADX-W13` | ADX-**Steigung** als Entry-Filter | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 7 | `ADX-W23` | Tages-DI-Spread als Richtungs-Bias | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 8 | `ADX-W33` **(neu)** | DI-Vorzeichenwechsel-Zahl als Chop-Maß | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 9 | `ADX-W14` | ADX-Roll-over als Reversions-Fenster | Signal | neues Bein | offen | offen |
| 10 | `ADX-W21` | EIN vorregistrierter Tages-Gate-Test | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 11 | `ADX-W24` | ES-ADX als Fremdmarkt-Gate | Filter | Ersatz `NQ_Momentum` | offen | offen |
| 12 | `ADX-W6` | ADX <20 als Chop-Fenster (Range statt Close) | Zeitfenster | neues Bein | offen | offen |
| 13 | `ADX-W29` **(Swing)** | Tages-ADX-Regime, Mehrtages-Trendfolge | Signal | **Live-Buch-Merker, kein Prop-Job** | **offen** (21.09. herabgestuft) | offen |
| 14 | `ADX-W38` **(Swing, neu)** | ADX-Rollover über Nacht gehalten | Signal | **Live-Buch-Merker, kein Prop-Job** | **belegt** (21.09., Schmidhuber 2021) | offen |
| 15 | `ADX-W39` **(Swing, neu)** | ADX-Spread NQ−ES als Mehrtages-Paar | Signal | **Live-Buch-Merker, kein Prop-Job** | offen | offen |

*(Die Spalte „Stempel" füllt später der `verdict-auditor`, nicht dieser Agent.)*

---

## Research-Stand (21.09.2026)

Rückschrieb aus dem Workflow `konzept-weg`, nach `research-scout`. **„Research widerlegt" wäre kein Tot-Stempel** (tot nur nach vollem Test, Regel „Hypothese vor Urteil") — in dieser Runde ist ohnehin **kein einziger** Weg widerlegt worden. Spalte „why_status vorher" benutzt noch das Wort „entwurf" aus der Erstfassung; es ist dasselbe wie `offen` im JSON.

| ID | vorher | jetzt | Quelle | Befund | an `ein-weg`? |
|---|---|---|---|---|---|
| `ADX-W19` | belegt | **belegt** | hausintern (#136, #080, `ideas.json`, Register) | keine Research-Frage offen, in der Runde nicht angefasst | ja |
| `ADX-W20` | belegt | **belegt** | hausintern (#080, Register 373/143) | keine Research-Frage offen, in der Runde nicht angefasst | ja |
| `ADX-W36` | entwurf | **offen** | [[Research-Cache]] Z. 881 (Daniel/Moskowitz), Z. 839 (Li/Sakkas/Urquhart) + Websuche 21.09. | Die Literatur koppelt Trendstärke eher an **hohe** statt niedrige Vola (Panic States). Keine Quelle zur Entkopplung „hohe Trendstärke + niedrige Vola" als eigener Zustand. Das Why trägt trotzdem weiter, weil es auf Käfig-Mathematik (θ = 2µ/σ², #142) ruht und nicht auf Chartlehre. | ja |
| `ADX-W15` | belegt | **offen** ⚠️ herabgestuft | Baltas/Kosowski 2013, [[Research-Cache]] Z. 880 + Websuche 21.09. | Bleibt im Original eine **Gewichtungs**-Aussage. Keine Replikation auf Intraday-Horizont, keine Quelle zur Übertragung auf die **Entry-Schwelle** statt auf die Positionsgröße. „Stetig schlägt binär" bleibt plausibel, die Latte-Fassung ist unbelegt. | ja |
| `ADX-W27` | entwurf | **offen** | Websuche 21.09. (Peak-and-Hook, ADX-Drop-Exit) | Nur unquantifizierte Praktiker-Heuristiken. **Keine Studie, die einen Indikator-Exit gegen einen Preis-Trailing-Stop gleicher Haltedauer misst** — genau der Vergleich, der W27 vom viermal toten Preis-Trailing-Block (#046/#142/#147/#150) trennen müsste. | ja |
| `ADX-W13` | entwurf | **offen** | Websuche 21.09. | Nur Praktiker-Konsens („Slope matters more than level") und ein proprietäres Skript (ADX Speed Derivative). Keine Studie Änderungsrate gegen Niveau. Der neue Winkel gegenüber #136 bleibt argumentativ. | ja |
| `ADX-W23` | entwurf | **offen** | Websuche 21.09. (Frage geteilt mit W31/W33/W35/W37) | Keine Quelle zum Informationsgehalt des Wilder ±DM-Vorzeichens gegen das Vorzeichen des Close-Returns derselben Periode. **Größte offene Lücke der Karte**, sie trägt fünf Wege gleichzeitig. | ja |
| `ADX-W33` | entwurf | **offen** | LuxAlgo (Praktiker-Doku zu ER und Choppiness) + Websuche 21.09. | Bestätigt nur die **konzeptionelle** Trennung: Whipsaw-Count zählt Ereignisse, ER rechnet auf Closes, CHOP auf True Range. Kein empirischer Vergleich Ereigniszahl gegen Amplitude. | ja |
| `ADX-W14` | entwurf | **offen** | Schmidhuber, Physica A 570 (2021), DOI 10.1016/j.physa.2020.125642 | Der Fund belegt kritische Trendstärke als Reversal-Prädiktor **nur auf Tagesdaten**. Er widerlegt W14 nicht, bestätigt aber exakt die Annahme, die das Why selbst als seine schwächste benennt (Intraday-Sichtbarkeit). Der Beleg landet vollständig beim Swing-Zwilling W38. | ja |
| `ADX-W21` | entwurf | **offen** | [[Research-Cache]] Z. 829/879 (Park/Irwin) + Websuche 21.09. | Park/Irwin weiterhin ohne isolierte ADX-Zahl. ⚠️ Eine wiederholt auftauchende Behauptung („International Journal of Financial Studies 2021, +18,7 %") ließ sich zu **keinem Paper und keiner DOI** zurückverfolgen — Verdacht auf Suchmaschinen-Konfabulation, **nicht verwendet**, nicht in den Cache übernommen. Die Lücke vom 30.08.2026 besteht unverändert. | ja |
| `ADX-W24` | entwurf | **offen** | Pitkäjärvi/Suominen/Vaittinen, JFE 2020, [[Research-Cache]] Z. 710 | **Eher Dämpfer als Stütze.** Der einzige Cross-Asset-Beleg trägt seinen Mechanismus über **gering** korrelierte Assets (Bonds gegen Equities). Für ein Fremdmarkt-Gate auf einem **hoch** korrelierten Markt (ES für NQ) gibt es keinen Beleg — der strukturelle Vorteil aus dem Why schrumpft genau in dem Maß, in dem ES und NQ korrelieren. | ja |
| `ADX-W6` | entwurf | **offen** | Vault-Archivsuche 21.09. (Strategie-Katalog, [[QuantPad Brief - VWAP Mean Reversion]], [[Friedhof-Analyse (17.09.2026)]] F8) | **Archivfrage beantwortet, zugunsten des Weges:** der Detail-Report zum QuantPad-NO-GO (#196) ist im Vault **nicht auffindbar** — nur Build-Brief und Endstatus „NO-GO #002/#003", keine Zahlen. Damit greift die vorab fixierte zweite Alternative (siehe Rang 12). Die Range-gegen-Close-Frage bleibt offen. | ja |
| `ADX-W29` **(Swing)** | belegt | **offen** ⚠️ herabgestuft | [[Research-Cache]] Z. 879 (Park/Irwin) + Websuche 21.09. | Lempérière trägt Trendfolge **allgemein**, nicht ADX/DMI **als Signal**. Park/Irwin bleibt ohne isolierte ADX-Zahl; eine Praktiker-Zahl (QuantifiedStrategies, DMI-Crossover S&P 500) war wegen Bot-Schutz nicht verifizierbar und wurde nicht übernommen. | **nein** |
| `ADX-W38` **(Swing)** | entwurf | **belegt** ⭐ | Schmidhuber, *Trends, Reversion, and Critical Phenomena in Financial Markets*, Physica A 570 (2021), DOI 10.1016/j.physa.2020.125642 (arXiv 2006.07847) | **Einziger echter Beleg-Treffer der Runde.** 30 Jahre Tages-Futures über Aktienindizes, Zinsen, Währungen, Commodities; kubisches Polynom der Folgerendite in der Trendstärke mit universeller kritischer Schwelle. Exakt der W38-Mechanismus auf exakt dem W38-Horizont. Ersetzt die indirekte CoT-/CTA-Analogie. | **nein** |
| `ADX-W39` **(Swing)** | entwurf | **offen** | Websuche 21.09. | Keine Studie, die eine Trendstärke-**Differenz** zweier korrelierter Index-Futures als eigenständiges Paar-Signal testet — nur generische ADX-Konstruktionsbeschreibungen. | **nein** |

**Bilanz:** belegt 3 (W19, W20, W38) · offen 12 · **widerlegt 0**. 13 von 15 Skeletten hatten offene Research-Fragen, W19/W20 hatten keine.

> [!warning] Nicht an `ein-weg` in dieser Runde — drei Wege, alle aus demselben Grund
> - **`ADX-W29`** — Swing-Weg, **Live-Buch-Merker**, kein Prop-Buch-Job. Geht nie in die Rechenrunde und hebt deshalb keine Zufallsdecke.
> - **`ADX-W38`** — Swing-Weg, **Live-Buch-Merker**, kein Prop-Buch-Job **trotz `why_status: belegt`**. Mehrtägiges Halten ist unter Trailing-DD-Käfig und Intraday-Bust-Check (#077) nicht führbar, und die Engine hält keine Position über Nacht.
> - **`ADX-W39`** — Swing-Weg, **Live-Buch-Merker**, kein Prop-Buch-Job.
>
> Alle drei **bleiben in der Karte stehen** (Regel Max 11.09.2026: nichts, was je eine Edge zeigte, geht verloren). Die übrigen **12 Skelette gehen an `ein-weg` Schritt 2** (`variant-scout` je Weg, danach `strategy-auditor`-Batch) — auch die mit `why_status: offen`, weil „offen" kein Urteil ist.


---

## Die fünfzehn Wege im Einzelnen

### Rang 1 — W19: Ist ADX nur ein Vola-Proxy? `ADX-W19`
**Bewegung:** ADX gegen seinen eigenen Nenner, richtungslos (Messweg).
**Mechanismus:** Terzil-Tafel Tages-ADX(14) aus t−1 gegen `atr_exp` (ATR5/ATR20) und `sigma_q`, off-Anteil-gematcht, auf allen drei Buch-Beinen plus NQ/ES roh.
**Story:** #136 hat die Falle einmal aufgedeckt — das 200d-MA-Gate sah mit +2,37 pp wie ein Fund aus, das gematchte RV20-Gate war mit +6,98 pp **dreimal stärker**; der MA trug nichts über die Vola hinaus. ADX ist ATR-normiert und damit strukturell noch näher an der Vola. Geht dieser Vorweg nicht positiv aus, bekommt **kein** anderer ADX-Weg einen Job, und das Kapitel ist in einem Lauf sauber geschlossen statt in dreißig.
**Verwandte Tote:** #136 (353 Trials), #139 (180 Trials), `atr_exp`-Gate 19.400 Trials, `sigma_q`-Gate 313. **Neu 21.09.:** `ideas.json` „VPIN Order-Flow-Toxizität (Filter)", Status **Getötet** — „Kein sauberer Filter-Edge (Quintile Rauschen), **schwach vs VIX**". Das ist ein **zweiter unabhängiger Präzedenzfall für genau die Frage dieses Wegs** (ein Filter verliert gegen den Vola-Proxy), neben #136; mit #162 (Orderflow-Gate auf Bestandsbeine, kein Effekt) sind es **drei**. Die Erstfassung führte #136 als Einzelfall — das war zu freundlich. **Gleich:** Gate-Form, Zielmetrik, Käfig. **Anders:** ADX war nie die Quelle, und dies ist ein Kontrast-Test, kein Buch-Eval.
**Engine-Weg:** MS-1 (~15-20 Zeilen `sigcore`) + MS-5 (~120-150 Zeilen Skript, kein Engine-Kern).
**Buch-Bezug:** kein Bein. Torwächter.
**Research (21.09.):** `belegt`, unverändert — keine Research-Frage offen, der Beleg ist hausintern (#136, #080, `ideas.json`, Register). In der Runde nicht angefasst.

### Rang 2 — W20: Schlägt ADX die Maße, die wir schon haben? `ADX-W20`
**Mechanismus:** Rangkorrelation + Kontrast-Tafel Tages-ADX gegen Kaufman-ER (`tm_er_min`/`rev_er_min`/`er_thr`), MA-Steigung (`mb_kind="slope"`) und Vorzeichen-Anteil (`tm_signal="signratio"`).
**Story:** Korreliert ADX mit einem davon über ~0,8, ist er eine Reparametrisierung und die Decke gilt bereits gegen ihn — die ehrliche Trial-Zählung entscheidet sich hier, nicht im Backtest. Misst er erkennbar etwas anderes (±DM nutzt nur Hoch/Tief, ER und signratio nur Closes), ist das der einzige Grund, warum ADX überhaupt eine eigene Familie ist. Direktes Analogon zu AK-01, das dieselbe Frage für die MA-Familie stellt.
**Verwandte Tote (21.09. verschärft):** nicht „168 Trials", sondern **373 Trials / 143 Survivors** auf ER-artigen Achsen (`tm_er_min` 168/16 aktiv, `rev_er_min` 58/43, `er_thr` 147/84) plus `mb_kind="slope"` 355/72 und `signratio` 5.124/231. **Entscheidend und in der Erstfassung ganz gefehlt:** [[Strategie-Logbuch]] **#080 (MOMSEL-Replace-Test v2, 10.08.2026)** — der ER-Filter hat nicht nur Register-Trials, er hat einen **vollständigen Buch-Replace-Test** hinter sich: NQ_Momentum gegen dasselbe Bein + `rev_er_min=0.3`, `passmc_vec`, 8000 Sims, Fracs 0,10-0,22. Ergebnis: **„das Pass-Delta ist überall MC-Rauschen (−1,2 bis +0,5 pp)"**, Verdikt **„Replace lohnt NUR bei Betriebspunkt frac ≈ 0,10"**, und der alte „klare Gewinn" vom 03.08. **repliziert nicht**. Dazu `ideas.json` „Momentum-Selektiv (Kaufman Efficiency-Ratio-Filter)", Status Validiert, aber **„Als 10. Zusatz-Bein abgelehnt"**. **Das ist genau die Stufe, auf die W6 und W20 zusteuern — für den Close-basierten Zwilling ist sie schon einmal gelaufen und hat nichts ergeben.** Deshalb Rang 2: wenn ADX ≈ ER, ist die Antwort für das ganze Kapitel bereits bekannt.
**Engine-Weg:** MS-1 + Auswertungsteil von MS-5 (~40 Zeilen). **Buch:** kein Bein.
**Research (21.09.):** `belegt`, unverändert — keine Research-Frage offen, Beleg hausintern (#080, Register 373/143). Torwächter bleiben Rang 1 und 2.

### Rang 3 — W36 (neu): ADX hoch × ATR niedrig — gerichtet, aber ruhig `ADX-W36`
**Bewegung:** Konjunktion zweier Zustände, kein Durchgang und kein Preisweg.
**Mechanismus:** Freigabe des Momentum-Beins nur an Tagen, an denen Tages-ADX(14) aus t−1 **über** seinem 60-%-Quantil **und** `atr_exp` (ATR5/ATR20) **unter** seinem 50-%-Quantil liegt. Beide Hälften aus t−1, beide aus dem bestehenden Tageskontext. Long und short getrennt (#108).
**Story:** ⭐ Das ist der einzige ADX-Zustand, der unter **unserer** Zielfunktion strukturell Sinn ergibt, und der Grund ist die Käfig-Mathematik, nicht die Chartlehre. Der Trailing-DD-Käfig bestraft Varianz, nicht Trendlosigkeit: die Passquote ist monoton in θ = 2µ/σ² (#142, Mathematiker). „Hoher ADX" sagt, dass die Range-Erweiterung gerichtet war (Zähler µ), „niedriger ATR" sagt, dass die Tagesbewegung klein ist (Nenner σ² **und** kleinere Stopdistanzen, also weniger Käfig-Verbrauch je Trade und eine niedrigere Kosten-Schwelle relativ zur Bewegung, MNQ-Round-Trip ~2 Punkte). Beide Buch-Hebel zeigen im selben Zustand in dieselbe Richtung. **Und der Weg beantwortet Randbedingung 5 strukturell statt rhetorisch:** jeder andere ADX-Weg muss beweisen, dass er nicht bloß Vola misst; dieser hier **enthält** die Vola-Größe als zweites, gegenläufiges Element und kann deshalb per Konstruktion nicht mit `atr_exp` kollinear sein. Fällt W19 mit dem Befund „ADX ≈ Vola-Proxy", ist W36 der **einzige** Weg der Karte, der davon nicht automatisch mitfällt — er wird dann sogar interessanter, weil die Konjunktion dann eine reine ATR-Terzil-Aussage ist und gegen `atr_exp` allein antreten kann.
**Verwandte Tote:** `tm_atr_exp_*`-Gate **19.400 Trials / 13 Survivors** (die ATR-Hälfte ist massiv gemessen — aber nie in Konjunktion mit einem Richtungsmaß), #136/#139 (533 Trials Gate-Form), #139 Lehre 2 (Off-Tage-Malus gilt auch hier: eine Konjunktion zweier Quantile schaltet **mehr** Tage ab als jede Hälfte einzeln — das ist die härteste Hürde dieses Wegs und gehört in den θ-Vorfilter). **Gleich:** Tagesmaske über ein Buch-Bein. **Anders:** zwei Elemente statt einem, und die Vola steht im Signal statt im Confound.
**Engine-Weg:** MS-1 + `tm_adx_min` aus MS-2 (~6 Zeilen) — **die ATR-Hälfte existiert bereits** (`tm_atr_exp_max` in `sigcore.gates_pass` Z. 1066-1071). Billigster echter Buch-Weg der Karte.
**Buch:** Ersatz `NQ_Momentum_d260818`.
**Pflicht vor dem Job:** θ-Vorfilter auf der **Konjunktion**, nicht auf den Hälften; und die Off-Anteil-Rechnung, weil zwei Quantile multiplikativ ausdünnen (0,4 × 0,5 ≈ 20 % On-Tage → laut #139-Kurve ein Malus in der Größenordnung mehrerer pp, den der Zustand erst schlagen muss).
**Research (21.09.):** `entwurf` → **`offen`**. [[Research-Cache]] Z. 881 (Daniel/Moskowitz) und Z. 839 (Li/Sakkas/Urquhart) koppeln Trendstärke eher an **hohe** statt niedrige Vola; die gezielte Websuche fand **keine** Quelle, die „hohe Trendstärke + niedrige Vola" als eigenen, entkoppelten Zustand führt. Die Kernfrage von Rang 3 bleibt unbeantwortet. Das Why trägt trotzdem, weil es auf Käfig-Mathematik (θ = 2µ/σ², #142) ruht und nicht auf Chartlehre. **Geht an `ein-weg`.**

### Rang 4 — W15: ADX moduliert die Schwelle stetig `ADX-W15`
**Bewegung:** ADX-Niveau als stetiger Zustand, kein Durchgang, kein Schalter.
**Mechanismus:** Die Entry-Schwelle wird mit dem Tages-ADX aus t−1 skaliert (hoher ADX → niedrigere Latte, niedriger ADX → höhere). **Kein einziger Off-Tag.**
**Story:** Baltas/Kosowski 2013 ist die einzige belegte Aussage, die wir haben: kontinuierliches Trendstärke-Signal statt binärem senkt den Turnover um mehr als ein Drittel bei gleicher Performance. Unter unserer Zielfunktion ist genau das der Gewinn — #139 Lehre 2 zeigt, dass jedes An/Aus-Gate erst die Off-Tage-Malus-Kurve überwinden muss, während ein Modulator sie nie berührt. Der Weg umgeht strukturell den Grund, an dem AR-15 und AR-17 gescheitert sind.
**Ehrliche Einordnung der Quelle (21.09. nachgeschärft):** Baltas/Kosowski ist im Original eine **Gewichtungs**-Aussage. Die wörtliche Umsetzung wäre W32 (Positionsgröße ∝ Trendstärke) und die hat bei uns wegen Min-Size **keine Story** (AS-08). W15 ist die **Übertragung auf die Entry-Latte** — dieselbe Idee „stetig statt binär", aber ein anderer Angriffspunkt. Das ist legitim und es ist genau der Rest, den AS-08 selbst übrig lässt („wertlos — außer als **Schwellenkalibrierung**"), aber es ist **keine Replikation des Papers**, und deshalb steht `why_status: belegt` hier für den Mechanismus „stetig schlägt binär", nicht für die Effektstärke auf der Latte.
**Verwandte (21.09. ergänzt):** #139 Nachtrag hat einen Schwellen-Modulator als TS-19-Verwandten geprüft und wegen der Latte µ > 46,6 $ geschlossen — **aber auf Vola als Treiber, nicht auf Trendstärke.** Das ist der neue Winkel. Dazu zwei Bank-Zeilen, die in der Erstfassung fehlten, obwohl die Karte bei AR-16 genau diese Sorgfalt vorexerziert: **TS-03** ist inhaltlich der Zwilling dieses Wegs auf der Momentum-Seite — „trägt die Signalgröße Zusatzinformation … dann gehört die Schwelle als kontinuierliches Gewicht ins Bein, nicht als Cut", Status 🟢 offen, **mit `ts_reversal` sofort testbar, ohne jeden Modulcode**. W15 ist die ADX-Instanz von TS-03. **Praktische Folge: TS-03 sollte vor W15 laufen**, weil es dieselbe Frage ohne MS-1 beantwortet. Und **AS-08** (tanh fällt unter Min-Size auf binär zusammen) markiert die Grenze, wie weit „stetig" bei uns überhaupt tragen kann.
**Engine-Weg:** MS-1 + `tm_thr_adx_beta` (~10 Zeilen, an `tm_thr_scale` in `tsmom.py` Z. 67 / `_signal` Z. 166 angelehnt). **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.): ⚠️ `belegt` → `offen`, herabgestuft.** Baltas/Kosowski ([[Research-Cache]] Z. 880) bleibt im Original eine **Gewichtungs**-Aussage; die Websuche fand weder eine Replikation auf Intraday-Horizont noch eine Quelle, die die Stetigkeit auf die **Entry-Schwelle** statt auf die Positionsgröße überträgt. „Stetig schlägt binär" bleibt plausibel, die Latte-Fassung ist unbelegt. **Geht trotzdem an `ein-weg`** — „offen" ist kein Urteil. TS-03 bleibt der billigere Vorlauf.

### Rang 5 — W27: ADX-Peak-Trailing als Exit `ADX-W27`
**Bewegung:** ADX fällt vom eigenen Peak seit Entry (Zustandswechsel), richtungsunabhängig.
**Mechanismus:** Bar-ADX mitführen, Höchststand seit Entry merken, Exit sobald ADX um `tm_adx_give` Punkte darunter fällt — unabhängig vom Preis. Gegenprobe gegen den Preis-Trailing-Stop gleicher mittlerer Haltedauer.
**Story (unverändert gültig, aber entlastet vom Rang):** Der Mechanismus unterscheidet „der Trend hört auf" von „der Preis kommt kurz zurück" — genau die Trennung, die ein Preis-Trailing nicht leisten kann. Exit bleibt außerdem eine der beiden Kategorien mit belegter Buch-Chance (#139 B3: alle 14 Kandidaten-Jobs der Historie waren Ersatz oder Exit).
**⚠️ Verwandte Tote — in der Erstfassung massiv untergewichtet, 21.09. vollständig nachgetragen:**
- **#046** (29.07.2026, NO-GO): **0 von 8 Beinen überlebte OOS**, 5/8 IS-Verbesserung, **alle 5 kollabiert**. In der Erstfassung nur indirekt über #141 und ohne Zahl.
- **#142** (03.09.2026), **der direkteste tote Verwandte des ganzen Exit-Blocks und in Karte, Report und JSON komplett gefehlt:** MFE-Instrumentierung (`mfe_r` seitdem in allen Trade-Records), bar-genaues Counterfactual auf zwei Buch-Beinen, 10 Configs je Bein → **„Leg-Level: keine Config schlägt OFF"**. Bester Buch-Wert VWAP BE0,5 +1,16 pp ± 0,25, **scheitert an der 1,5-pp-Hürde**. **Cross-Leg-Replikation 0/12 Zellen positiv**, BE-Komponente auf v2 +2,95 pp mit 90 %-CI [−0,86; +7,25] = **neutral**, auf expR signifikant negativ. Urteil dort: „SL-Trailing und Break-even bringen auf diesem Buch **kein Alpha**."
- **#147 + #150** (09.-11.09.2026), vier `ideas.json`-Einträge, alle **Getötet**: First-Bar-EMA-Trail auf NQ/ES/YM/RTY. #147 wörtlich **„Trail beschneidet nur Gewinner (6,6k → 17,4k $ ohne Trail)"** — auf einem Bein, das nach Abzug **„NQ_Momentum_d260818 mit 5 statt 15 Min"** ist, also **exakt das Bein, das W27 ersetzen will**. #150: 2.880 + 144 + 72 Configs je Symbol, **0 positiv**.
- **Register:** `trail_ticks` 2.880 / 109 · `be_trigger` 1.581 / 672 · `trail_trigger` 759 / 299 · `trail_dist` 743 / 283.
- **#116** (NQ_ORB-fade, 224 Varianten, kein Hebel trägt).
- **Zitat-Korrektur:** die Erstfassung schrieb „#141 (Trailing-Stop-Vorprüfung: **ein echter Fund**, zwei negativ)". Das ist falsch zugeordnet — der eine echte Fund in #141 ist **AR-19 (Korrelationsregime)**. Die Trailing-Vorprüfung selbst endete dort wörtlich mit **„direkte Kontamination, 3 von 5 Buch-Beinen sind Rebuilds derselben Mechanismen"** und der Empfehlung **„kein neuer Grid-Sweep"**. Aus #141 Lehre 2: „Ein wiederbelebter Mechanismus (Lehre 104) verdient eine explizite Verwandtschafts-Prüfung, bevor überhaupt gerechnet wird."
**Was trotzdem NEU bleibt (und warum der Weg offen bleibt):** alle vier Präzedenzfälle trailen den **Preis** (fixierte R-Distanz bei Entry, `_trail_stop` fixiert R einmalig — #141 hält ausdrücklich fest, dass echtes atmendes Trailing im Code gar nicht existiert). W27 trailt einen **Zustand**, der den Preis nicht kennt. Das ist ein anderer Mechanismus, kein anderer Parameter — „Zustand statt Preis" ist der neue Grund im Sinne von Lehre 104. **Aber:** nach #142 ist die Beweis-Hürde 1,5 pp Buch-Marginal, und der nächste Verwandte hat sie mit +1,16 pp knapp gerissen. W27 startet also nicht bei null, sondern bei „muss besser sein als eine Konfiguration, die schon gemessen und für neutral befunden wurde".
**Engine-Weg:** MS-3 Teilmenge (~40 Zeilen) + MS-4 (~20-25 Zeilen). **Buch:** Ersatz `NQ_Momentum_d260818`.
**Pflicht vor dem Job:** MFE-Auswertung nutzen, die seit #142 existiert (`mfe_r`) — und deren dort dokumentierte Grenze beachten: `mfe_r` ist eine **Untergrenze**, bei `target`-Exits zensiert, Auswertung nur auf `eod`/`time`-Exits, **nie** zur Ableitung von Trail-Triggern über ein Grid.
**Research (21.09.):** `entwurf` → **`offen`**. Die Websuche fand nur unquantifizierte Praktiker-Heuristiken (Peak-and-Hook, ADX-Drop-Exit als Parameter) — **keine** Studie, die einen indikator-basierten Exit gegen einen preis-basierten Trailing-Stop **gleicher Haltedauer** misst. Genau dieser Vergleich müsste W27 vom viermal toten Preis-Trailing-Block trennen; er bleibt damit Messaufgabe statt Literaturbeleg. **Geht an `ein-weg`.**

### Rang 6 — W13: Die ADX-Steigung, nicht das ADX-Niveau `ADX-W13`
**Mechanismus:** Nicht „ADX > 25", sondern „ADX(t−1) > ADX(t−6)" — als Entry-Bedingung **im Bein**, nicht als Tagesmaske über dem Buch.
**Story:** #136 nennt die Reichweite seines eigenen Urteils wörtlich: getestet ist die *Tagesmaske*; Entry-Filter in der Bein-Logik und andere Regime-Quellen sind ausdrücklich **ungetestet** (deshalb steht dort ➖ und kein ❌). Die Steigung ist zusätzlich ein anderer Zustand als das Niveau: sie ist definitionsgemäß früh (ADX hinkt beim Niveau-Durchgang bereits mehrere Perioden hinterher) und erzeugt keine zusammenhängenden Off-Blöcke — AR-15 scheiterte unter anderem an einer 78-Handelstage-Aus-Strecke.
**Verwandte Tote:** #136 (353), #139 (180), `mb_kind="slope"` 355 Trials (MA-Steigung, nicht ADX-Steigung).
**Engine-Weg:** MS-1 + `tm_adx_slope_min` (~6 Zeilen) + Verdrahtung `ts_reversal` (~10-15 Zeilen). **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.):** `entwurf` → **`offen`**. Gefunden wurden nur Praktiker-Konsens („Slope matters more than level") und ein proprietäres Skript (ADX Speed Derivative) — keine Studie, die die Änderungsrate eines Trendstärke-Maßes gegen sein Niveau testet. Der neue Winkel gegenüber #136 bleibt argumentativ. **Geht an `ein-weg`.**

### Rang 7 — W23: Tages-DI-Spread als Richtungs-Bias `ADX-W23`
**Mechanismus:** Vorzeichen von (+DI − −DI) aus t−1 entscheidet, welche Seite das Bein heute nehmen darf (`tm_dir="long_only"` / `"short_only"`). Kein Trade-Verlust auf der erlaubten Seite.
**Story:** Der DI-Spread ist der **einzige** ADX-Bestandteil mit Vorzeichen (ADX selbst ist vorzeichenlos) und stammt aus Hoch/Tief, nicht aus dem Close. Die `tm_dir`-Achse ist breit besetzt, aber nie mit einer Hoch/Tief-basierten Vorzeichenquelle. **Ehrlicher Dämpfer vorab:** Nilsson und CFM sagen beide, die kurzfristige Autokorrelation moderner Futures liege nahe Null — stimmt das, hat auch dieser Bias keinen Träger. Long und short getrennt ausweisen (#108).
**Engine-Weg:** MS-1 + `tm_di_side` (~8 Zeilen) + Verdrahtung `ts_reversal`. **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.):** `entwurf` → **`offen`**. Keine Quelle zum Informationsgehalt des Wilder ±DM-Vorzeichens gegen das Vorzeichen des Close-Returns derselben Periode. Diese eine Lücke trägt W23, W31, W33, W35 und W37 **gleichzeitig** und ist damit der größte unbelegte Hebel des Kapitels — sie wird endgültig zur Messaufgabe von W20/W31, nicht zur Literaturfrage. **Geht an `ein-weg`.**

### Rang 8 — W33 (neu): Wie oft dreht der DI-Spread in N Bars? `ADX-W33`
**Bewegung:** Zustand **„wechselt"** — die einzige Achse aus der eigenen Bewegungs-Matrix, die in den ersten 31 Wegen unbesetzt war.
**Mechanismus:** Zähler `k` = Anzahl der Vorzeichenwechsel von (+DI − −DI) in den letzten N Bars. Hoch → Chop-Zustand, Momentum-Bein aus bzw. MR-Fenster frei; niedrig → gerichteter Zustand. Als Filter auf `NQ_Momentum`, gegen ein ausdünnungsgleiches Zufalls-Gate.
**Story:** Jeder Vorzeichenwechsel ist ein **abgeschlossener, gescheiterter Richtungsversuch** — eine Kohorte Trendfolger, die eingestiegen und ausgestoppt wurde. Die Zahl dieser Versuche im Fenster misst direkt, wie teuer das Fenster für ein Ausbruchs-Bein war, und sie misst es **als Ereigniszahl, nicht als Amplitude**. Genau deshalb ist es eine andere Größe als W6 (Spread eng = Amplitude klein), W4 (Spread weit = Amplitude groß) und W3 (EINE gescheiterte Kreuzung): ein Fenster kann breite Spreads haben und trotzdem sechsmal drehen, und dann ist es für ein Momentum-Bein das teuerste Fenster überhaupt — bei einem MNQ-Round-Trip von ~2 Punkten ist die Zahl der Fehlstarts die Kostengröße, nicht ihre Tiefe.
**Verwandte:** Bank **AV-02** und **AV-13** messen beide ausdrücklich die **„Whipsaw-Zahl"** als Kennzahl (AV-02: Hull-MA gegen EMA gleicher Glättung; AV-13: Einfach- gegen Doppelglättung bei angeglichenem Lag) — beide 🟢 offen. Dort ist die Whipsaw-Zahl eine **Bewertungsgröße für eine MA-Konstruktion**; hier ist sie das **Signal selbst**. Das ist der Unterschied, der W33 zu einem eigenen Weg macht und nicht zu einer Doppelung. **Verwandte Tote:** ER-Achsen 373/143 und #080 als nächster „Chop-Maß"-Präzedenzfall — ER misst Chop über das Verhältnis Netto- zu Bruttobewegung auf **Closes**, W33 über die Ereigniszahl auf **Hoch/Tief**. Dieselbe Rechtfertigungslinie wie W6, und deshalb hängt W33 an derselben Vorfrage: **W31/W20 entscheiden, ob die Hoch/Tief-Aggregation überhaupt etwas Eigenes misst.**
**Engine-Weg:** MS-3 (Bar-ADX/DI) + **MS-6** (Vorzeichenwechsel-Zähler `mb_adx_evt="flipcount"`, `mb_adx_flip_n`, ~15 Zeilen obendrauf). **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.):** `entwurf` → **`offen`**. LuxAlgo (Praktiker) bestätigt die **konzeptionelle** Trennung — Whipsaw-Count zählt Ereignisse, ER rechnet auf Closes, CHOP auf True Range — aber es gibt **keinen empirischen Vergleich** Ereigniszahl gegen Amplitude. Die Abgrenzung zu W6/W4 bleibt konstruktiv richtig, aber unbelegt. **Geht an `ein-weg`.**

### Rang 9 — W14: ADX-Roll-over von hohem Niveau `ADX-W14`
**Mechanismus:** Bar-ADX über 40 (oberes Dezil), dann zwei fallende ADX-Bars, während der Preis noch in Trendrichtung steht. Einstieg gegen den Trend, Stop über dem letzten Extrem, Zeit-Exit.
**Story:** Der Akteur ist hier nicht „jemand schaut auf ADX", sondern **systematische Trendfolge, die bei ADX-Maximum voll positioniert ist** und beim Stillstand der Range-Erweiterung abbauen muss. Der einzige Umkehr-Weg im ganzen Konzept, der ohne Reflexivität am Indikator auskommt.
**Verwandte Tote:** #133 (CVD-Divergenz >250 Arten, Friedhof) als nächster Divergenz-Verwandter; `mb_kind="band"` 179 Trials / 1 Survivor.
**Engine-Weg:** MS-3 voll (~70-100 Zeilen) inkl. `mb_rand_level`-Pflichtkontrolle. **Buch:** neues Bein — und #139 B3 steht dagegen. Nur bauen, wenn W19/W20 durch sind.
**Swing-Zwilling:** W38 (Mehrtages-Haltefassung, Live-Buch-Merker).
**Research (21.09.):** `entwurf` → **`offen`**. Schmidhuber (Physica A 570, 2021) belegt kritische Trendstärke als Reversal-Prädiktor **nur auf Tagesdaten** (30 Jahre, vier Assetklassen). Das widerlegt W14 nicht, bestätigt aber exakt die Annahme, die das Why selbst als seine schwächste benennt: dass ein Mehrtages-Abbau innerhalb weniger Stunden sichtbar wird, bleibt unbelegt. **Der Beleg landet vollständig beim Swing-Zwilling W38.** W14 geht trotzdem an `ein-weg`.

### Rang 10 — W21: EIN vorregistrierter Tages-Gate-Test `ADX-W21`
**Mechanismus:** Tages-ADX(14) aus t−1 über dem 70-%-Quantil der eigenen 250-Tage-Historie → Momentum-Bein an, sonst aus. **Genau eine** vorab fixierte Variante, gepoolt, einseitig, mit off-gematchtem Circular-Shift-Placebo, Episoden-Jackknife und LOLO.
**Story:** Die klassische ADX-Aussage muss in der Karte stehen, damit sie später niemand für ungetestet hält. Sie bekommt aber nur einen Test: #162 hat vorgerechnet, dass die Beine für ein Gate-Grid eine Power von 0,03-0,10 haben, und #136/#139 haben dieselbe Gate-Form mit 533 Trials ohne Kandidat durchgemessen. **Vorbedingung, die VOR dem Lauf entscheidet:** θ-Vorfilter r_σ² > r_µ (Hürde r_σ ≳ 1,16) auf der ADX-Teilung — sonst fällt der Weg ohne Rechenzeit.
**Verwandte (21.09. ergänzt):** `ideas.json` **„Mom-lowVIX (Momentum nur bei niedrigem VIX)"**, Status **Validiert**: „OOS-Edge +10,4 %, Sharpe 2,78, EOD-Pass 62 % … **VIX-Filter selbst nie gegen das Buch auto-gefittet**." Das ist ein Regime-Gate auf genau der Momentum-Seite, das **nie die Buch-Marginal-Stufe gesehen hat** — relevant, weil es zeigt, dass der Flaschenhals auf dieser Achse historisch **nicht die Signalqualität** war, sondern die Buch-Stufe. Ein ADX-Gate, das nur Signalqualität beweist, ist damit noch nichts wert; es muss an derselben Stelle liefern, an der lowVIX nie geprüft wurde.
**Engine-Weg:** MS-1 + MS-2 + 3× Verdrahtung Buch-Modi (~30-45 Zeilen). **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.):** `entwurf` → **`offen`**. Park/Irwin ([[Research-Cache]] Z. 829/879) nennt ADX/DMI weiterhin **ohne isolierte Kennzahl**; die Lücke vom 30.08.2026 besteht unverändert. ⚠️ **Konfabulations-Warnung:** eine in der Websuche wiederholt auftauchende Zahl („International Journal of Financial Studies 2021, +18,7 %") ließ sich trotz mehrfacher gezielter Suche **zu keinem Paper und keiner DOI** zurückverfolgen. Sie wurde **nicht verwendet** und **nicht** in den [[Research-Cache]] übernommen — wer sie später wiederfindet, bitte nicht zitieren. **Geht an `ein-weg`.**

### Rang 11 — W24: ES-ADX als Fremdmarkt-Gate `ADX-W24`
**Mechanismus:** Tages-ADX(14) des ES aus t−1 als Freigabe für das NQ-Momentum-Bein.
**Story:** AR-06 formuliert den Gedanken (breiter Markt bildet den Makro-Zustand besser ab als das tech-lastige NQ, kein Selbstbezug), ist aber nie über ein Trend-SMA hinaus getestet worden. Der strukturelle Vorteil ist echt: ein Gate auf sich selbst korreliert mit dem Signal und dünnt genau die Tage aus, an denen das Signal ohnehin klein ist — ein Fremdmarkt-Gate nicht.
**Verwandte Tote:** xref-Achse **24 aktiv / 30 vorhanden / 31 über alle `tm_xref*`-Schlüssel, 0 Survivors in jeder Lesart**; **XD-12** hat auf derselben NQ/ES-Kopplung bereits eine Look-ahead-Falle produziert (Cross-Fenster darf nie länger sein als das Signalfenster, Assert in `sigcore.xref_confirm`). Siehe [[ES-NQ-Divergenz Wege-Karte]].
**Engine-Weg:** MS-1 je Symbol + `tm_adx_xref_min` (~10 Zeilen). **Buch:** Ersatz `NQ_Momentum`.
**Research (21.09.):** `entwurf` → **`offen`, und eher Dämpfer als Stütze.** Pitkäjärvi/Suominen/Vaittinen (JFE 2020, [[Research-Cache]] Z. 710) ist der einzige Cross-Asset-Beleg, trägt seinen Mechanismus aber über **gering** korrelierte Assets (Bonds gegen Equities). Für ein Fremdmarkt-Gate auf einem **hoch** korrelierten Markt (ES für NQ) gibt es keinen Beleg der Überlegenheit — der strukturelle Vorteil aus der Story schrumpft genau in dem Maß, in dem ES und NQ korrelieren. **Geht an `ein-weg`**, aber mit diesem Vermerk.

### Rang 12 — W6: ADX <20 als Chop-Fenster — Range statt Close `ADX-W6`
**Mechanismus:** Bar-ADX unter 20 über mindestens N Bars schaltet ein Mean-Reversion-Fenster frei. Direkt gegen dieselbe Konstruktion mit `tm_er_min` gerechnet: gleiche Zeitpunkte, gleiche Trade-Zahl, gematchte Ausdünnung.
**Story (unverändert):** Die ER rechnet ausschließlich auf Closes (`sigcore` Z. 191-196), **Wilders ±DM ausschließlich auf Hoch und Tief.** In Chop-Phasen ist der Unterschied nicht kosmetisch — Closes können ruhig aussehen, während die Bars breit durchschlagen. Genau diese Fälle sind für ein MR-Bein die teuersten (MNQ-Round-Trip ~2 Punkte) und für ER unsichtbar.
**⚠️ Verwandte Tote — 21.09. zweimal verschärft, deshalb Rang 8 → 12:**
1. **#196 / [[Friedhof-Analyse (17.09.2026)]] `karten_scouts_labs.md` Z. 288 + [[QuantPad Brief - VWAP Mean Reversion]] Z. 82.** Der QuantPad-Brief schreibt als Regime-Filter **wörtlich** „(a) trend strength below a threshold (**e.g. ADX < 20-25**)" für eine VWAP-Z-Score-Mean-Reversion auf **MNQ/MES**; Status laut Strategie-Katalog #002/#003: **NO-GO**. **Das ist W6 in Reinform, mit Stempel.** Es entwertet außerdem teilweise den neuen Grund dieses Wegs: #196 hat bereits das **Range-basierte** Maß benutzt, nicht ER — die „Range statt Close"-Rechtfertigung ist dort also schon einmal durchgelaufen und hat nicht getragen. Einschränkungen, die den Stempel abschwächen und den Weg offen halten: fremdes Tool (separates QuantPad-Setup, unklar ob dieselbe Engine), **kein einsehbarer Detail-Report**, die Friedhof-Analyse flaggt genau diese Beleg-Lücke und bewertet das Vertrauen mit **„niedrig-mittel"**, und die Konstruktion war eine VWAP-Z-MR, nicht unser Chop-Fenster. Nach der Regel „tot nur nach vollem Test" bleibt W6 deshalb **offen** — aber **nicht jungfräulich**.
2. **ER-Vorgeschichte:** nicht 168 Trials, sondern **373 Trials / 143 Survivors** plus der volle Buch-Replace-Test **#080** („Pass-Delta überall MC-Rauschen, −1,2 bis +0,5 pp", „Replace lohnt NUR bei frac ≈ 0,10") und `ideas.json` „Momentum-Selektiv", „als 10. Zusatz-Bein abgelehnt".
**Vorbedingung vor jedem Rechnen (neu, analog zum θ-Vorfilter bei W21):** erst klären, ob der Detail-Report zu #196 auffindbar ist. Bestätigt er das NO-GO mit Zahlen auf MNQ/MES, fällt W6 **ohne Rechenzeit**. Ist er nicht auffindbar, läuft W6 mit dem expliziten Vermerk, dass ein fremder Stempel auf demselben Mechanismus existiert. **✅ Am 21.09. beantwortet: nicht auffindbar.** Im Vault existieren nur Build-Brief und Endstatus „NO-GO #002/#003", keine Zahlen — das bestätigt die Beleg-Lücke, die die [[Friedhof-Analyse (17.09.2026)]] unter F8 selbst flaggt. **W6 fällt also NICHT ohne Rechenzeit**, sondern läuft mit dem Vermerk, dass ein fremder Stempel (Vertrauen „niedrig-mittel") auf demselben Mechanismus existiert.
**Engine-Weg:** MS-3 Teilmenge (~50 Zeilen). **Buch:** neues Bein; später als Fenster-Filter auf ein bestehendes MR-Bein umbauen.
**Research (21.09.):** `entwurf` → **`offen`**. Die **Archivfrage ist beantwortet** (siehe Vorbedingung oben): kein Detail-Report zu #196 auffindbar, also fällt W6 nicht ohne Rechenzeit. Die zweite Frage — Range-basierte gegen Close-basierte Chop-Maße auf Intraday-Futures — bleibt offen, kein direkter Test gefunden. **Geht an `ein-weg`.**

### Rang 13 — W29 (Swing): Tages-ADX-Regime als Mehrtages-Trendfolge `ADX-W29`
> [!note] Swing-Zeile — Live-Buch-Merker, **nicht** Prop-Buch, kein Job-Vorschlag
> Regel Max 11.09.2026: nichts, was je eine Edge zeigte, geht verloren. Mehrtägiges Halten ist unter dem Trailing-DD-Käfig und dem Intraday-Bust-Check (#077) nicht führbar, und die Engine hält heute keine Position über Nacht.

**Mechanismus:** Einstieg, wenn Tages-ADX(14) über 25 steigt, Richtung aus dem DI-Spread; Haltedauer Tage bis Wochen; Ausstieg bei ADX < 20 oder Vorzeichenwechsel des DI-Spreads.
**Story:** Das ist die Form, in der Wilder ADX gemeint hat, und die einzige mit breiter Trendfolge-Evidenz (Lempérière et al., arXiv 1404.3274: t ≈ 5 seit 1960 über vier Assetklassen) — allerdings auf Monate kalibriert und ausdrücklich nicht intraday übertragbar.
**Engine-Weg:** MS-1 + Overnight-Haltelogik (existiert nicht; Aufwand ohne eigene Vorklärung nicht seriös schätzbar).
**Research (21.09.): ⚠️ `belegt` → `offen`, herabgestuft.** Lempérière trägt Trendfolge **allgemein**, nicht ADX/DMI **als Signal** — das war in der Erstfassung zu großzügig gelesen. Park/Irwin ([[Research-Cache]] Z. 879) bleibt ohne isolierte ADX-Zahl; eine Praktiker-Zahl (QuantifiedStrategies, DMI-Crossover S&P 500) war wegen Bot-Schutz nicht verifizierbar und wurde **nicht** übernommen.
**`ein-weg`-Runde 21.09.: nein** — Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job. Bleibt als Merker in der Karte.

### Rang 14 — W38 (Swing, neu): ADX-Rollover über Nacht gehalten `ADX-W38`
> [!note] Swing-Zeile — Live-Buch-Merker, **nicht** Prop-Buch, kein Job-Vorschlag
> Nachgetragen 21.09. auf Auditor-Befund: Regel Max 11.09.2026 verlangt, Swing-Wege **mitzuführen UND zu markieren**. Die Erstfassung führte genau **eine** Swing-Zeile (W29, Trendfolge). Die **Umkehr**-Fassung fehlte, obwohl W14 in seiner natürlichen Haltedauer ein Swing-Weg ist.

**Bewegung:** wie W14 (ADX fällt von hohem Niveau, Preis noch im Trend), aber auf **Tagesbars** und mit Haltedauer über Nacht bis mehrere Tage.
**Mechanismus:** Tages-ADX(14) über 40, danach zwei fallende Tages-ADX-Werte bei weiter bestehendem DI-Vorzeichen → Gegenposition, Stop über dem letzten Swing-Extrem, Exit bei DI-Vorzeichenwechsel oder nach fixer Tageszahl.
**Story (Why überarbeitet 21.09., jetzt belegt):** Die erwartete Folgerendite eines Futures folgt einem **kubischen Polynom seiner aktuellen Trendstärke** — positiver linearer Persistenz-Term, negativer kubischer Reversions-Term — mit einer über Aktienindizes, Zinsen, Währungen und Commodities hinweg **stabilen universellen kritischen Trendstärke**, oberhalb derer Trends systematisch umkehren (Schmidhuber, *Trends, Reversion, and Critical Phenomena in Financial Markets*, Physica A 570 (2021), DOI 10.1016/j.physa.2020.125642 / arXiv 2006.07847 — **30 Jahre Tagesdaten**, vier Assetklassen). Das ist exakt der W38-Mechanismus auf exakt dem Horizont, auf dem W38 laufen soll, und ersetzt die bisherige indirekte CoT-/CTA-Analogie. Derselbe Akteur wie W14, aber auf dem Horizont, auf dem er tatsächlich handelt. CTA-/Trendfolge-Positionierung baut sich nicht innerhalb einer Intraday-Session ab, sondern über Tage — die Intraday-Fassung W14 unterstellt, dass ein Mehrtages-Abbau innerhalb weniger Stunden sichtbar wird, und das ist die schwächste Annahme in W14. W38 ist die Fassung ohne diese Annahme. **Warum trotzdem nur Merker:** mehrtägiges Halten ist unter Trailing-DD-Käfig und Intraday-Bust-Check (#077) nicht führbar, und die Engine hält keine Position über Nacht.
**Engine-Weg:** MS-1 (Tagesebene reicht) + Overnight-Haltelogik (existiert nicht).
**Verwandte:** W14 (Intraday-Zwilling), #133, `tm_base="overnight"` 145 Trials / 0 Survivors (andere Konstruktion: Overnight als *Signalbasis*, nicht als Haltedauer).
**Research (21.09.): ⭐ `entwurf` → `belegt`.** Schmidhuber, *Trends, Reversion, and Critical Phenomena in Financial Markets*, Physica A 570 (2021), DOI 10.1016/j.physa.2020.125642 (arXiv 2006.07847) — 30 Jahre Tages-Futures über Aktienindizes, Zinsen, Währungen und Commodities. **Einziger echter Beleg-Treffer der ganzen Research-Runde**, und er trifft exakt den W38-Mechanismus auf exakt dem W38-Horizont.
**`ein-weg`-Runde 21.09.: nein, trotz `belegt`** — Swing-Weg, Live-Buch-Merker. Mehrtägiges Halten ist unter Trailing-DD-Käfig und Intraday-Bust-Check (#077) nicht führbar, Overnight-Haltelogik existiert nicht. Der beste Beleg des Kapitels liegt damit auf dem Weg, den das Prop-Buch nicht handeln kann — das gehört so festgehalten.

### Rang 15 — W39 (Swing, neu): ADX-Spread NQ−ES als Mehrtages-Paar-Trade `ADX-W39`
> [!note] Swing-Zeile — Live-Buch-Merker, **nicht** Prop-Buch, kein Job-Vorschlag
> Ebenfalls 21.09. nachgetragen. W25 (Intraday-Fassung) hat bewusst kein Skelett, weil die NQ/ES-Kopplung eine eigene Karte hat und ein zweiter Agent dort nur die Zufallsdecke hebt. **Für die Swing-Fassung gilt dieses Argument nicht**, weil sie nie in die Prop-Rechenrunde geht und deshalb keine Decke hebt.

**Bewegung:** zwei Anker (NQ-ADX, ES-ADX), Zustand „nur einer trendet", gehalten über Tage.
**Mechanismus:** Wenn Tages-ADX(NQ) − Tages-ADX(ES) ein oberes/unteres Quantil erreicht, Paar-Position long/short im Verhältnis der Kontraktwerte; Ausstieg bei Rückkehr des Spreads in die Mitte oder nach fixer Tageszahl.
**Story:** Der Spread misst, welcher der beiden Indizes gerade einen eigenen, gerichteten Treiber hat (Tech-Konzentration gegen breiten Markt). Ein solcher Treiber ist ein Mehrtages-Phänomen — Earnings-Zyklen, Sektorrotation —, kein Intraday-Ereignis. Das ist der Grund, warum die Relative-Value-Familie außerhalb von HF überhaupt Sinn ergibt.
**Engine-Weg:** MS-1 je Symbol + Overnight-Haltelogik (existiert nicht).
**Verwandte:** W25 (Intraday-Zwilling), [[ES-NQ-Divergenz Wege-Karte]], XD-12 (Look-ahead-Falle auf derselben Kopplung), xref-Achse 24-31 Trials / 0 Survivors.
**Research (21.09.):** `entwurf` → **`offen`**. Keine Studie gefunden, die eine Trendstärke-**Differenz** zwischen zwei korrelierten Index-Futures als eigenständiges Paar-Signal testet — nur generische ADX-Konstruktionsbeschreibungen.
**`ein-weg`-Runde 21.09.: nein** — Swing-Weg, Live-Buch-Merker, kein Prop-Buch-Job.

---

## ein-weg-Runde (21.09.2026): variant-scout + strategy-auditor-Batch über 12 Wege

Ergebnis: **0 von 12 gehen unverändert in `hypothesis_bank.py`.** 6 nachbessern, dann Bank · 4 nicht bauen (Story fällt durch) · 2 nicht bauen (zu wenige echte Varianten). Querbefund des Auditors: 8 von 10 Storys nennen eine Indikator-Eigenschaft statt eines handelnden Gegenübers, und fünf Wege hängen am selben Bein `NQ_Momentum` (~800 Trades, Power 0,03-0,10), teilen sich also **eine** Beweisdecke.

| Weg | Urteil | Echte Varianten | Auflage / Grund |
|---|---|---|---|
| W19 Vola-Proxy? | nachbessern | 12 (grenzwertig) | P&L-Tafel streichen oder als nicht entscheidend markieren (#139: mu_off > mu_on), Urteil auf Feature-Ebene, Etikett „trend" raus, als Messweg führen |
| W20 ADX vs ER/slope/signratio | nicht bauen als Bank-Zeile | 6 | nur als MS-5-Messskript zusammen mit W19 auf gemeinsamem MS-1, H() bricht bei n<10 ab |
| W36 ADX hoch × ATR niedrig | nachbessern | 16 | erst Zwei-Zeilen-Zählung: wie viele Tage/Trades bleiben in der Konjunktion (`min_tpy=25`)? Satz „per Konstruktion nicht kollinear" streichen, Akteur nachtragen |
| W27 ADX-Peak-Trailing | nachbessern | 36 | zeit-gematchter Exit als Pflichtkontrolle im selben Job, Urteil auf Trade-Ebene (Buch-Marginal nicht auflösbar, Sd 2,3 pp gegen 1,5-pp-Hürde) |
| W14 ADX-Rollover | nachbessern | 108 | erst Swing-Zwilling W38 rechnen, Prescan auf Fade-Trägerdrift (#133, `tm_side=fade` 7.785/7) |
| W24 ES-ADX als Gate | nachbessern | 12 | Roll-/Session-Alignment als Kontrolle, AR-06 stilllegen (sonst doppelte Zufallsdecke), Erwartung auf 15-24 % Teilraum senken |
| W6 ADX<20 Chop-Fenster | nachbessern | 108 | nur mit gebautem ER-Chop-Arm (`tm_er_max`) im selben Job, Prescan auf Fade-Trägerdrift |
| W15 Schwelle stetig | **nicht bauen (Story)** | 9 | „keine Off-Tage" ist falsch (angehobene Latte streicht Grenzsignale), Baltas/Kosowski trifft weder Stellschraube noch Signal, gleicher Pfad wie TS-19 (Tautologie) |
| W13 ADX-Steigung | **nicht bauen (Story)** | 12 | Neuheit „Bein-Logik statt Tagesmaske" existiert bei 1 Trade/Tag mechanisch nicht, #136 hat Steigung explizit mitgemessen |
| W23 Tages-DI-Spread als Bias | **nicht bauen (Story)** | 12 | Hoch/Tief vs Close: 83-85,5 % Vorzeichen-Übereinstimmung, lebt nur auf ~15 % der Tage, Nachbarachse `lp_prevday` 0 Kandidaten / PBO 75 % |
| W33 Whipsaw-Zähler | **nicht bauen (Story)** | 10 | bester Akteur-Satz der Gruppe, aber Persistenz zweimal ~0 gemessen, kein Kanal vom Zähler zum Entry |
| W21 EIN Tages-Gate-Test | **nicht bauen (Varianten)** | 1 | `assert n >= 10` in H(); legitim nur als #162-artiger Einzeltest per Skript, nach W19 und θ-Vorfilter |

**Empfohlene Reihenfolge (Auditor):** W19 nachbessern und rechnen (entscheidet über W20/W21/W13-Reste mit) → Zählung W36 → W38 vor W14 → W24 → W6 → W27. W19 + W20 als **ein** Messskript (MS-5) auf gemeinsamem MS-1.

## Bau- und Testrunde (21.09.2026, Abend)

MS-1 bis MS-3 (Teilmenge) sind gebaut ([[Strategie-Logbuch]] #168): Tages-ADX in `sigcore.daily_context`, Gates `tm_adx_*`/`tm_xadx_*`/`tm_badx_*`/`tm_er_max`, Bar-ADX und `tm_exit="adx_peak"` in `tsmom`, Kontrollen in `controls.py`. Golden-Master „Sync frei", Configs ohne ADX bitgleich, `pipeline-auditor` ohne Blocker (drei Fixes umgesetzt), `verdict-auditor` hat die Urteile gegengelesen.

| Weg | Stand jetzt | Beleg |
|---|---|---|
| **W19/W20** | **gemessen:** ADX weder Vola-Proxy (R² 0,19/0,11) noch ER (ρ 0,31), aber **keine Folgetag-Information** (partielles ρ ≈ 0, CI ±0,03). Gilt für ADX→eigener Markt, Tages-Ziele | `adx_vs_vola_w19.py` |
| **W27** | **tot für den tsmom-Momentum-Träger:** 8/8 Configs nicht besser als zeit-gematchter Exit, gegen EOD −0,08…−0,21 R/Trade. W5/W9 unberührt | `adx_w27_probe.py` |
| **W36** | **zurückgehalten** (`hold=`): 11,7 tpy in der vorregistrierten Form, unter `min_tpy=25`. Reaktivierung: Basis-Bein ≥ 150 tpy | Zählung |
| **W14** | **zurückgehalten** (`hold=`): Tages-Zwilling W38 trägt in der Rollover-Form nicht (CI deckt 0 in 16/18) | `adx_w38_events.py` |
| **W38-Niveau** (neu, Lead) | NQ/ES L35/L40 halten die vorregistrierten Regeln, **Replikation YM/RTY scheitert**, post-hoc-Form, Swing = Live-Buch-Merker | `adx_w38_level.py` |
| **W24** | **Job in der Bank** (`hyp_ADXW24_NQ`, 12 Configs, replaces `NQ_Momentum`), erste Messung ES-ADX→NQ | Box-Lauf offen |
| **W6** | **Job in der Bank** (`hyp_ADXW6_NQ`, 45 Configs, ER-Gegenarm im selben Job); beide Prämisse-Configs negativ (−0,13 / −0,07 R) → Stufe 0 wird sehr wahrscheinlich scheitern (= „Prämisse gescheitert", nicht „tot") | Box-Lauf offen |

**Buch-Lücke:** kein einziger ADX-Weg steht über Stufe 0 (Prämisse). W24, W6 und AXV-W26 sind die drei, die die Box gerade rechnet. Alles andere ist gemessen und ohne Kandidaten oder zurückgehalten mit konkreter Reaktivierungsbedingung.

## W19 ausgerollt auf GC, CL, YM, RTY (22.09.2026)

Max: „auf Gold und alle Märkte testen, die wir noch nicht angefangen haben." `adx_vs_vola_w19.py GC,CL,YM,RTY`, dieselben vorab festgelegten Urteilsregeln wie beim NQ/ES-Erstlauf, eigene Ergebnisdatei (`adx_w19_result_GC_CL_YM_RTY.json`), NQ/ES-Original unangetastet.

| Markt | Tage | R² ADX~Vola | R² ADX~Vola+Trend | Information über Folgetag? |
|---|---|---|---|---|
| GC (Gold) | 2.418 | 0,066 | 0,32 | nein — einziges CI ohne 0 (abs_sig\|Vola [0,007; 0,073]) unter der \|rho\|≥0,05-Schwelle |
| CL (Öl) | 2.418 | 0,119 | 0,312 | nein — alle CIs enthalten 0 |
| YM (Dow) | 2.669 | 0,144 | 0,263 | nein — CIs ohne 0 bei dir_ret (−0,033 / −0,039), beide unter der Schwelle |
| RTY (Russell) | 2.221 | 0,094 | 0,312 | nein — alle CIs enthalten 0 |

**Ergebnis: dasselbe Muster wie NQ/ES, auf allen sechs getesteten Futures-Märkten (Tech-Index, breiter Index, Dow, Small-Cap, Gold, Öl).** ADX ist nirgends ein reiner Vola- oder Trend-Proxy (kein R² erreicht 0,60), trägt aber auch nirgends zusätzliche Information über den Folgetag — kein Markt erfüllt gleichzeitig CI-ohne-0 und \|rho\|≥0,05. Das ist kein Einzelfall von NQ/ES, sondern ein marktübergreifender Befund: die Grundannahme „hoher ADX sagt etwas über den nächsten Tag" trägt auf keinem der sechs Märkte, unabhängig von Assetklasse.

---

## Modul-Specs (nichts davon existiert heute)

| Spec | Was | Wo | Grob |
|---|---|---|---|
| **MS-1** | Tages-ADX: `plus_dm`/`minus_dm`, Wilder-Glättung α=1/n, Spalten `plus_di`, `minus_di`, `adx14`, `di_spread`, `adx_slope5`, alle `.shift(1)` | `sigcore.daily_context()` Z. 640-700 (**TR steht dort schon, Z. 678**) + 6 Namen in `out` Z. 696 | **15-20 Zeilen** |
| **MS-2** | `tm_adx_min`, `tm_adx_max`, `tm_adx_slope_min`, `tm_di_side` | `sigcore.gates_pass()` Z. 1044ff. (analog `tm_atr_exp_min` Z. 1066-1071) + DEFAULTS `tsmom.py` Z. 86-99 | **12-15 Zeilen** + je 10-15 Zeilen Verdrahtung pro Buch-Modus |
| **MS-3** | `mb_kind="adx"` mit `mb_adx_evt ∈ {di_cross, level, slope, rollover}`, `mb_adx_n`, `mb_adx_thr`, plus `mb_rand_level`-Pfad (Zufalls-Trendstärke gleicher Verteilung) | `maband._signal()`, kind-Zweig ab Z. 284 | **70-100 Zeilen** |
| **MS-4** | `tm_exit="adx_peak"` + `tm_adx_give` | sigcore-Exit-Schicht | **20-25 Zeilen** |
| **MS-5** | `adx_vs_vola_w19.py`: Terzil-Tafel, off-gematcht, Circular-Shift-Placebo je Variante, Episoden-Jackknife, LOLO | Scratchpad, **kein Engine-Kern** | **120-150 Zeilen** |
| **MS-6** *(neu, für W33)* | `mb_adx_evt="flipcount"` + `mb_adx_flip_n`: rollender Zähler der Vorzeichenwechsel von `di_spread` über N Bars | Aufsatz auf MS-3, derselbe kind-Zweig | **~15 Zeilen** |

**Billigster echter Buch-Weg:** W36 — MS-1 (15-20 Zeilen) + `tm_adx_min` (~6 Zeilen), weil `tm_atr_exp_max` bereits in `gates_pass` steht. Alles andere braucht mindestens MS-3.
**Nie** ein neuer `mode`: `controls.ctl_null` kennt sechs Modi (`controls.py` Z. 667-668), alles außerhalb bekommt `ok=None` → `skipped_required` → kann nie `deploy_ready` werden (#139 B1).

---

## Pflichtkontrollen für jeden ADX-Job

1. **AR-04-Analog:** ausdünnungsgleiches Zufalls-Gate. Wer die Wochentags-Ausdünnung nicht schlägt, ist kein Gate.
2. **AR-14-Analog:** invertiertes Gate. Funktioniert die Gegenrichtung genauso, misst es Trade-Reduktion.
3. **`mb_rand_level`-Analog:** Zufalls-Trendstärke gleicher Verteilung statt echtem ADX.
4. **θ-Vorfilter vor dem Job** (#139): r_σ² > r_µ, Hürde r_σ ≳ 1,16. **Bei W36 auf der Konjunktion, nicht auf den Hälften.**
5. **Off-Tage-Malus gegenrechnen** und **Circular-Shift-Placebo je Variante**, nicht Max-über-alle (#139 Lehre 1).
6. **Episoden-Jackknife statt Epochen-Split** (#136 Lehre 3).
7. **Delay 1→2** (TK-11) und **long/short getrennt** (#108).
8. **Näherungen dürfen erst ranken, wenn ihre Rangkorrelation zur Entscheidungsmetrik gemessen und > 0 ist** (#136 Lehre 1).
9. **NEU (aus #142, für W27 und jeden Exit-Weg):** `mfe_r` ist eine **Untergrenze** und bei `target`-Exits zensiert — MFE-Auswertungen nur auf `eod`/`time`-Exits, **nie** Trail-Trigger über ein Grid daraus ableiten. Beweis-Hürde ist 1,5 pp Buch-Marginal über 2× Seed-Rauschen, und der nächste Verwandte hat sie mit +1,16 pp gerissen.
10. **NEU (aus #141 Lehre 2):** jeder wiederbelebte Mechanismus bekommt die explizite Verwandtschafts-Prüfung **vor** dem Rechnen, nicht danach.

---

## Research-Fragen (Stand nach der Runde 21.09.2026)

**Bilanz der Runde:** von 10 Fragen ist genau **eine** mit einem Zahlen-Beleg beantwortet (Nr. 6, und zwar **nur für den Tages-Horizont** → der Beleg landet bei W38, nicht bei W14) und **eine** als Archivfrage beantwortet (Nr. 10: kein Detail-Report zu #196 auffindbar). Die übrigen acht bleiben **offen** — zu ADX selbst gibt es weiterhin keine akademische Primärzahl. Frage 3 (Hoch/Tief gegen Close) ist die teuerste: sie trägt fünf Wege und wird damit endgültig zur **Messaufgabe** von W20/W31 statt zur Literaturfrage.

1. Gibt es inzwischen **irgendeine** Quelle mit Effektstärke zu ADX als Gate? Der [[Research-Cache]] hält seit 30.08.2026 die Lücke „nur Richtungsaussage, keine Zahlen".
2. Repliziert der Turnover-Gewinn von Baltas/Kosowski auf **Intraday**-Horizont — und gilt er auch, wenn die Stetigkeit auf die **Entry-Schwelle** statt auf die **Positionsgröße** angewendet wird? (W15 vs. W32)
3. Trägt ein Vorzeichen aus **Hoch/Tief** (Wilder ±DM) mehr Information als das Vorzeichen des Close-Returns derselben Periode? (W23/W31/W33/W35/W37 hängen alle daran)
4. Wird die **Änderungsrate** eines Trendstärke-Maßes irgendwo gegen sein Niveau getestet? (W13)
5. Gibt es eine Quelle, die einen **indikator-basierten Exit** gegen einen preis-basierten Trailing-Stop gleicher Haltedauer misst? (W27)
6. Positionierung systematischer Trendfolger als Reversions-Prädiktor auf **Intraday**-Horizont? (W14/W38)
7. Ist ein Regime-Filter auf einem korrelierten **Fremdmarkt** einem Selbstbezugs-Filter überlegen? (W24)
8. **NEU:** Gibt es Evidenz für die **Konjunktion** „gerichtet, aber ruhig" (hohe Trendstärke bei niedriger Vola) als eigenen Zustand — oder wird Trendstärke in der Literatur immer zusammen mit hoher Vola gefunden? (W36 — das ist die Kernfrage von Rang 3)
9. **NEU:** Wird die **Zahl** der Richtungswechsel in einem Fenster (Whipsaw-Count) irgendwo als eigenständiges Chop-Maß gegen amplitudenbasierte Maße (ER, Bandbreite) getestet? (W33)
10. **NEU:** Ist der Detail-Report zum QuantPad-NO-GO (#196, VWAP-Z-MR mit ADX < 20-25 auf MNQ/MES) beschaffbar? Das ist keine Literaturfrage, sondern eine Archivfrage — sie entscheidet, ob W6 überhaupt gerechnet werden muss. (W6)

---

## Buch-Lücke, ehrlich

Alle 15 Skelette hängen auf **Stufe 0: Prämisse.** Kein Code, kein Trial, kein Job. Reihenfolge bis ins Buch:
**MS-1 + MS-5 bauen → W19 und W20 rechnen (Torwächter) → falls positiv: `variant-scout` je Weg + `strategy-auditor`-Batch → Gate-Batterie `GATES_HARD`/`controls.py` → Jobs auf der Box → Survivors/PBO → über die Zufallsdecke (65.035 Trials) → Buch-Marginal „besser" gegen das 3-Bein-Buch → Next-Week-Buch + Ticket → Wochenend-Review → NT8-Deploy.**

Fällt W19 (ADX ≈ Vola-Proxy) oder W20 (ADX ≈ ER-Reparametrisierung), ist das Kapitel in **einem** Lauf sauber geschlossen statt in dreißig — und ehrlich gesagt ist das das wahrscheinlichere Ergebnis. **Einzige Ausnahme nach dem Nachtrag:** W36 fällt bei „ADX ≈ Vola-Proxy" **nicht** automatisch mit, weil dort die Vola als zweites Element im Signal steht. Wenn das Kapitel einen Überlebenden hat, ist es wahrscheinlich dieser.

**Billigster Erkenntnisgewinn ohne jeden Modulcode:** Bank **TS-03** (🟢, „✅ ts_reversal + Dezil-Auswertung") beantwortet die W15-Kernfrage — trägt die Signalgröße Zusatzinformation, gehört die Schwelle als stetiges Gewicht ins Bein — **mit vorhandener Engine**. Das sollte vor MS-1 laufen.

**Was nach dem Research-Rückschrieb 21.09. weitergeht:** **12 der 15 Skelette** gehen an `ein-weg` Schritt 2 (`variant-scout` je Weg, danach `strategy-auditor`-Batch) — W19, W20, W36, W15, W27, W13, W23, W33, W14, W21, W24, W6. **Nicht** weiter gehen **W29, W38 und W39**: alle drei sind Swing-Wege und **Live-Buch-Merker**, auch W38 mit `why_status: belegt`. Sie bleiben in der Karte stehen und heben keine Zufallsdecke, weil sie nie einen Job im Prop-Register bekommen. Die Reihenfolge bis ins Buch ändert sich durch die Research-Runde **nicht**: MS-1 + MS-5 bauen und die beiden Torwächter rechnen bleibt Schritt eins.

---

## Verwandte Notizen

[[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Research-Cache]] · [[Friedhof-Analyse (17.09.2026)]] · [[QuantPad Brief - VWAP Mean Reversion]] · [[Alpha-Suche]] · [[Discovery-Runner v2]] · [[Strategie-Familien]] · [[Strategie-Anatomie (Framework)]] · [[Simplex beats Komplex]] · [[Eval-Passing]] · [[Buch-Workflow]] · [[Familien-Scout Agent]] · [[VWAP-Offensive]] · [[Fibonacci Wege-Karte]] · [[Rundzahlen Wege-Karte]] · [[Session Momentum Wege-Karte]] · [[ES-NQ-Divergenz Wege-Karte]]
