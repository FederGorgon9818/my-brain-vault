---
tags:
  - bereich/trading
  - trading/alpha
  - trading/hypothesen
  - trading/pca
erstellt: 2026-08-30
status: offen (noch nichts getestet, Quant-Review + variant-scout/strategy-auditor-Audit 21.09.2026 eingearbeitet)
---
# 🧪 Hypothesen-Bank: PCA & Faktorstruktur

⬅️ [[Alpha-Suche]] · [[Strategie-Familien]] · [[Discovery-Runner v2]] · [[Strategie-Logbuch]] · [[Research-Cache]]
Schwester-Banken: [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Hypothesen-Bank (Pairs Trading & Relative Value)]]

> [!important] Was das ist
> Max' Auftrag 30.08.2026: aus 10 Research-Papers (PCA auf Futures-/Index-Märkten, Vorrecherche im [[Research-Cache]]) **falsifizierbare Hypothesen** ableiten, was PCA uns bringen könnte. **Jede Hypothese wird auf allen 4 Märkten identisch getestet** (Positions-Bein = ES, NQ, RTY oder YM, Signal aus dem Querschnitt aller 4). Nur aufgestellt, **noch nichts getestet** (Regel: Hypothese vor Urteil). SK-05/SK-06 aus der Pairs-Bank sind hiermit zur eigenen Bank ausgearbeitet.
> **30.08.2026: Quant-Team-Review (Mathematiker + Statistiker) eingearbeitet** — beide haben deskriptiv auf unseren echten Daten gerechnet (keine Edge-Tests, keine Trials verbraucht). Ihre Messwerte stehen bei den betroffenen Zeilen.

---

## ⚠️ Die zentrale Warnung: N=4 ist nicht N=500

Fast die gesamte PCA-Literatur arbeitet mit 100-1000 Assets. Wir haben 4 Serien mit **ρ̄ = 0,856** mittlerer Paar-Korrelation (nicht 0,93 — das ist nur ES-NQ/ES-YM; NQ-RTY liegt bei 0,77). Gemessene Eigenwert-Struktur (Tagesreturns 2017-2026):

| | λ1 | λ2 | λ3 | λ4 |
|---|---|---|---|---|
| Varianzanteil | 89,3 % | 6,4 % | 4,0 % | 0,4 % |

Die Kernaussage in einem Satz (Quant-Mathematiker):

> **PC1 ist stabil, aber trivial** (1,7° vom gleichgewichteten Durchschnitt entfernt — fast nur "der Markt als Mittelwert"), **und PC2 ist nicht-trivial, aber kaum identifiziert** (Eigenwert-Lücke λ2−λ3 = 0,096, Bootstrap-Kegel um die PC2-Richtung 17-74°). Einen komfortablen Zwischenbereich gibt es nicht.

Und die ehrliche Edge-Erwartung (Quant-Statistiker, Fundamental Law): Avellaneda/Lee hatten ~125.000 unabhängige Wetten pro Jahr auf ~500 Aktien; wir haben **effektiv 2,32 unabhängige Residuen** (die Residuen summieren unter einem Gleichgewichts-Faktor auf ≈ 0; gemessene Residuen-Korrelationen ES/RTY **−0,72**, NQ/YM −0,67). Bei gleichem Informationsgehalt je Wette bleibt von A/Ls Sharpe 0,9 bei uns **≈ 0,1-0,3 annualisiert** übrig — plus deren eigener dokumentierter Zerfall. **Mit dieser Zahl wird geplant, nicht mit 0,9.** Kein Paper testet unser Setup; die Literatur liefert den Mechanismus, nicht den Beweis.

## 🔒 Käfig-Filter

Gleiche fünf Tore wie in der [[Hypothesen-Bank (Pairs Trading & Relative Value)]] (intraday only, 4 Instrumente, Kostenlast, Min-Size, Passquote je Eval als einziges Kriterium). Dazu die bekannten Fallen: R_pts-Normierung am Positions-Bein (#090, Lehre 46), `_drop_corrupt_sessions` immer aktiv (#075).

**Korrektur 30.08. (Quant-Mathematiker):** Der Pairs-Bank-Reflex „bevorzugt Beine = 1" ist hier **rechnerisch falsch pauschalisiert**. Mit einem Bein handelt man Residuum **plus** ungehedgten Faktor — und der Residualanteil an der Positionsvarianz ist winzig (5m, gegen PC1): **ES 2,7 %**, YM 9,5 %, NQ 11,5 %, RTY 18,6 %. Bei ES sind 97 % der Position edge-freies Faktorrauschen, das nur den Drawdown aufbläst. Beine = 1 oder 2 wird deshalb **je Markt** über die Regel in PR-06 entschieden, nicht per Voreinstellung.

## 📚 Forschungsbasis (Details im [[Research-Cache]])

| # | Paper | Kernbefund für uns |
|---|---|---|
| 1 | Avellaneda/Lee 2010 (SSRN 1153505) | PCA-Residuum als OU-Prozess, s-Score-Handel; Sharpe 1,44 (1997-2007), 0,9 (2003-2007) — Mechanismus-Vorlage, Aktien-Querschnitt |
| 2 | Yeo/Papanicolaou 2017 | nur **schnell** mean-revertierende Residuen handeln |
| 3 | d'Aspremont 2011 (arXiv 0708.3048) | Sparse/simple Faktoren für kleine, instabile Asset-Basen |
| 4 | Kritzman/Li/Page/Rigobon 2010/11 (SSRN 1633027) | Absorption Ratio als Fragilitäts-Frühindikator |
| 5 | Aït-Sahalia/Xiu 2019 (JASA) | Intraday-PCA: Faktorstruktur ist zeitvariabel, PC1-Anteil steigt in Krisen |
| 6 | Epps 1979 (JASA) | Korrelationen sinken mit der Messfrequenz — **bei uns gemessen klein**: ρ̄ 0,845 (1m) vs. 0,875 (60m) |
| 7 | Litterman/Scheinkman 1991 | Level/Slope/Curvature der Zinskurve — Kontext, nachrangig |
| 8 | Laloux et al. 1999 (PRL 83) | Random-Matrix: Rausch-Bulk vs. Signal-Eigenwerte — **MP-Schwelle bei N=4 nicht anwendbar**, siehe F2-03 |
| 9 | Plerou et al. 2002 (PRE 65) | nur wenige Eigenwerte tragen Information |
| 10 | Fenn/Porter et al. 2011 (PRE 84) | PCA-Komponenten zeitlich instabil, Kopplung steigt in Stress |

## 🛡️ Look-ahead-Grundregeln (gelten für JEDE Zeile, sitzen im Modul, nicht in den Jobs)

1. **Jede Terzil-, Perzentil-, Schwellen- und Uhrzeit-Norm wird expandierend oder rollend aus Tagen bis einschließlich gestern gebildet, nie aus dem vollen Sample.** Das Modul liefert Quantile ausschließlich in dieser Form. (Der klassische Look-ahead, den `controls.py` nicht abfängt, weil er in der Signaldefinition sitzt.)
2. **PC-Ladungen nur aus Fenstern bis gestern**, innerhalb des Tages eingefroren. Gleiches für den OU-Fit hinter dem s-Score (m, σ_eq): kein Re-Fit mit Bars des laufenden Tages — bei Avellaneda/Lee steckt genau hier die Falle.
3. **Vorzeichenkonvention deterministisch:** PC2 wird so orientiert, dass die NQ-Ladung positiv ist. Bei Ladungs-Rotation > 90° zum Vortag wird eine kumulierte PC2-Reihe neu verankert, nicht fortgeschrieben.
4. **PCA auf der Korrelationsmatrix**, nicht Kovarianz (Kovarianz-PC1 ist zu 1,3° einfach die Vol-Gewichtung und mischt Vol-Dispersion ins Regime-Signal).

## 📋 Prä-Registrierung (Statistiker-Auflage — ohne die entscheidet das Register hier nichts)

Die globale Zufallsdecke (aktuell SR 2,39 bei n=15.457) hat gegen eine wahre Edge von 0,1-0,3 eine **Power von 0-2 %** — ein echter Fund dieser Größe passiert sie fast nie, und was sie passiert, ist fast sicher Rauschen. Deshalb für diese Bank verbindlich, **vor dem ersten Lauf**:

| Stufe | Zeilen | Regel |
|---|---|---|
| **Primär** | ST-01, PR-04, PR-01 | Bonferroni α = 0,05/3, Primärstatistik je Zeile vorab schriftlich (Testgröße, Horizont, Seite). Entscheiden, ob der Mechanismus existiert und ob PCA das Werkzeug ist. |
| **Sekundär** (Konditionierung) | AR-01, AR-03, PR-05, ST-03, F2-03 | Laufen nur, wenn Primär hält. Auswertung als **Interaktionstest auf dem vollen Sample**, nie als „bestes Terzil" (3 Größen × 3 Terzile auf denselben Trades = Subgruppen-Inflation, die der Trial-Zähler nicht sieht). |
| **Explorativ** | Rest (PR-02, PR-06, AR-02, AR-04, F2-01/02/04, ST-02/04/05) | Ergebnisse werden protokolliert; **kein Kandidat aus dieser Gruppe geht ohne eigene Re-Registrierung ins Next-Week-Buch.** |

> [!warning] Audit 21.09.2026 (variant-scout + strategy-auditor, nachgeholt — Regel 01.09.2026 galt bei Bau dieser Bank noch nicht)
> **Reihenfolge-Fund:** die 11 Zeilen, die variant-scout als Testbar/Grenzwertig einstuft (genug echte Achsen-Varianten für einen `H()`-Job), enthalten **weder PR-04 noch ST-01** — genau die zwei ungeprüften Primär-Wurzeln, von denen laut dieser Tabelle alles andere abhängt. PR-01/PR-05/ST-02/ST-05 vor PR-04+ST-01 zu bauen widerspricht der eigenen Prä-Registrierung. Reihenfolge: **1)** PR-04 (VR-Test) + ST-01 (TOST) zuerst, keine Grid-Jobs. **2)** danach PR-01 allein (2-Bein, NQ/YM, ES raus). **3)** AR-02 läuft sofort parallel (braucht kein PCA, konditioniert nur das Buch, Auflage: nur auf OOS-Tagen der Beine messen). **4)** AR-04 erst nach einer 20-Minuten-Vormessung ohne Trials (corr(intraday-ρ̄, intraday-RV) — ist die hoch, ist die Zeile nur ein RV-Proxy). **5)** F2-04 (fester NQ−RTY-Kontrast, 0 Schätzparameter) vor F2-01/F2-03, spart im Erfolgsfall 270 Varianten.
>
> **PR-02 und AR-03 fallen als Story durch, nicht bauen:** PR-02 überschreibt die protokollierte Todesursache von div_fade (#033, „doppelte Kosten fressen die engen Spreads") durch „falsches Timing" ohne jede Messung dafür — und behauptet auf 15-60 Min das **umgekehrte Vorzeichen** von PR-01 auf demselben Residuum (zwei Zeilen mit Gegenvorzeichen auf derselben Größe finden garantiert eine Gewinnerin, der Trial-Zähler sieht das nicht). Die Frage ist ohnehin durch PR-04 für 0 statt 48 Varianten mitbeantwortet (VR(q)<1 → Reversion, VR(q)>1 → Fortsetzung). AR-03 ist ein Umschalter zwischen zwei Armen, von denen einer (div_fade) tot und der andere (div_mom) „nur marginal" ist — ein Interaktionstest auf einer Null-Basis zeigt nur, in welchem Regime das Rauschen lag, keine Edge.
>
> **Direkt bauen ohne weitere Vorstufe:** ST-03 (n=6, sauberste Zeile der Gruppe, aber als Interaktionstest, nicht eigenes Bein) und AR-02 (n=27, mit OOS-Auflage).
>
> **Rechnungs-Realitätscheck:** die 11 geprüften Zeilen summieren auf 726 Achsen-Varianten, bei effektiv ~2,32 unabhängigen Markt-Replikationen also ~313 Varianten je echter Replikation — die globale Zufallsdecke bewegt sich davon kaum (+0,2 %), das Problem ist reine Box-Zeit auf einer Bank mit 0-2 % Power bei der eigenen ehrlichen Edge-Erwartung (Sharpe 0,1-0,3).
>
> **Vor dem Bauen offen:** PR-01s Gegenkraft-Frage (warum bleibt Geld im meistgehandelten Index-Arb-Komplex der Welt liegen — steht schon als offene Auditor-Frage im Block-Kopf), F2-03s Formulierung „laufendes Fenster" → muss „bis gestern" heißen (sonst Look-ahead im Gate selbst), und die Familien-Einordnung von PR-01/F2-01 in der 1-Bein-Fassung (dort Mean Reversion bzw. Intraday Bias mit ungehedgtem Faktor-Ballast, nicht Relative Value — siehe Residualanteile im Block-Kopf).

## Legende
- **Daten:** 🟢 sofort testbar (1m OHLCV ES/NQ/RTY/YM 2016-2026) · 🟡 Tages-Zusatzdaten nötig
- **Engine:** alle Zeilen hängen an **einem** neuen Querschnitts-Modul. Bausteine laut Review: `rho_bar` (mittlere Paar-Korrelation), expandierende/rollende Quantile, Kendall-korrigierte AR(1)-Halbwertszeit, `bootstrap_cone(PC2)`, `l2_null_p95(T, rho)` (parametrischer 1-Faktor-Bootstrap). **Nicht** gebraucht: Marchenko-Pastur, Kovarianz-AR. Der AR-Block braucht überhaupt kein PCA (drei Zeilen Code, siehe Block-Kopf).
- **Beine:** **1** = Querschnitt ist Signal, Position in einem Index · **2** = echter Spread · Entscheidung je Markt nach PR-06
- **Märkte:** jede Zeile läuft ×4, aber **effektiv sind das nur ~2,3 unabhängige Replikationen** (Residuen spiegeln sich) — Multi-Markt-Bestätigung zählt hier etwa halb, nicht vierfach (#051 mit Abschlag)

---

## Block PR — PCA-Residuum handeln (Kern-Block, Avellaneda/Lee)

**Mechanismus-Why:** Der gemeinsame Faktor (PC1 = "der Markt") wird von Index-Arbitrage effizient gehalten. Was nicht sofort arbitriert wird, ist die idiosynkratische Abweichung eines einzelnen Index vom Faktor — einseitiger Flow (Sektor-Rotation, Rebalancing, Optionshedging), den Market-Maker zurückpreisen müssen. Das Geld läge, weil niemand Intraday-Mean-Reversion auf 4 Futures-Residuen mit 1 Kontrakt handelt (zu klein für Institutionen, zu instrumentenarm für Stat-Arb-Desks). *Offene Auditor-Frage dazu: hält das Why, wenn dieselben 4 Serien der meistgehandelte Index-Arb-Komplex der Welt sind?*

**Schon beantwortet ohne Rechenlauf (Review 30.08.):** Die Kostenfrage ist positiv entschieden. Nötige s-Score-Strecke, damit der Bruttofang 2× Roundtrip-Kosten deckt: **NQ 0,17 σ, RTY 0,37, YM 0,40, ES 1,14** — bei A/L-Schwellen (Strecke 0,75) tragen NQ/RTY/YM die Kosten mit Faktor 2-4 Luft. Der Block stirbt nicht an Kosten. **ES ist als Positions-Bein praktisch tot** (Residualanteil 2,7 %, Kostenstrecke > 1 σ).

| ID | Hypothese | Warum sie gut sein könnte | Prüfbar | Verwerfen wenn | Daten | Beine |
|---|---|---|---|---|---|---|
| PR-01 ⭐primär | Das Residuum eines Index gegen PC1 (rollende PCA auf Tagesreturns, Ladungen + OU-Fit bis gestern eingefroren) revertiert: s-Score über Schwelle → Position gegen die Abweichung, flat vor Close. | A/L-Kernmechanismus in der kostentauglichsten Form, die RV bei uns haben kann. Die Kostenhürde ist für NQ/RTY/YM vorab als machbar belegt (s.o.) — es hängt allein daran, ob die Reversion existiert. | s-Score je Index, Edge je Schwellen-Stufe, ×4 Märkte | Kein Markt zeigt Edge außerhalb des CIs (Block-Bootstrap), oder nur ES (dort Artefakt-Verdacht, siehe Kontrolle a) | 🟢 | je PR-06 |
| PR-02 | ❌ **Story fällt durch (strategy-auditor 21.09.2026), nicht bauen:** überschreibt die protokollierte Todesursache von div_fade (#033, „doppelte Kosten fressen die engen Spreads") durch „falsches Timing" ohne jede Messung dafür, und behauptet auf 15-60min das **umgekehrte Vorzeichen** von PR-01 auf demselben Residuum (Gegenvorzeichen-Paar findet garantiert eine Gewinnerin, Trial-Zähler sieht das nicht). Frage ist durch PR-04 für 0 statt 48 Varianten mitbeantwortet (VR(q)&lt;1 → Reversion, VR(q)&gt;1 → Fortsetzung). | ~~Fortsetzungs- vs. Umkehr-Regel je Haltefenster (Fenster-Grid vorab fest)~~ | — | 🟢 | entfällt (siehe PR-04) |
| PR-03 (Kalibrierungsmessung, zählt nicht als Hypothese) | Wo liegt das Schwellen-Optimum intraday relativ zu den A/L-Tagesmodell-Werten (öffnen ~1,25, schließen ~0,5)? | SK-06-Übertrag: beide Ausgänge informativ — deshalb per Definition keine falsifizierbare Hypothese, sondern eine Messung, die PR-01 kalibriert. | Sweep 0,75-3,0 σ, Plateau-Check | — (Plateau-Pflicht: nur Spitze = Overfit-Verdacht) | 🟢 | — |
| PR-04 ⭐primär | **Varianz-Ratio-Test:** Das kumulierte PC1-Residuum ist auf 15-120-min-Horizonten sub-diffusiv — VR(q) < 1 (Lo/MacKinlay, heteroskedastie-robust) — und die implizierte Reversion bei \|s\| > 1,5 deckt 2× Kosten. | **Der eine Test, der den ganzen Block entscheidet, ohne Grid und fast ohne Trial-Verbrauch.** Die alte Spannweiten-Fassung war unfalsifizierbar (eine Range entsteht auch beim Random Walk, E[Range] ≈ 1,6σ√n — das Verwerfen-Kriterium hätte an 0 von 2.173 Tagen gefeuert). VR misst Rückkehr, nicht Diffusion. | VR(q) für q = 15/30/60/120 min je Markt, Block-Bootstrap (Block = 1 Handelstag) | VR(q) für kein q signifikant < 1, **oder** implizierte Reversion unter 2× Kosten | 🟢 | — |
| PR-05 | Trade nur, wenn die OU-Halbwertszeit des Residuums kürzer als die Restzeit bis Close ist. HL geschätzt mit **Kendall-korrigiertem** AR(1)-Koeffizienten (b̃ = b̂ + (1+3b̂)/T), **gepoolt über die letzten K Tage** (T ≥ 35× der zu erkennenden HL), nie within-day. | Yeo/Papanicolaou-Logik, bei uns strukturell zwingend (EOD-Flat schneidet langsame Reversion ab). Ohne Korrektur unterschätzt OLS die HL bei T=60 um **Faktor 2,4** — der unkorrigierte Filter würde genau die langsamen Residuen durchlassen, die er aussortieren soll, und die 390 RTH-Bars eines Tages lösen HL > 11 min gar nicht auf. | Edge mit/ohne HL-Filter (ΔSharpe-CI, Block-Bootstrap) | CI enthält 0 nach Korrektur + Mindest-T; oder HL durchweg > 1 Tag (→ [[Live-Account]], nicht Eval) | 🟢 | je PR-06 |
| PR-06 | Für Märkte mit kleinem Residualanteil ist das **zweite Bein trotz doppelter Kosten der bessere Handel**. Entscheidungsregel: 2 Beine, wenn C/G < (1−k)/(2−k) (C = Roundtrip-Kosten, G = Bruttofang, k = Rest-Rauschanteil nach 1:1-Micro-Hedge). Vorab gemessen: **NQ (Hedge MES, x 0,11 vs. Schwelle 0,33) und YM klar für 2 Beine, RTY knapp für 1, ES für keins.** | Ein Bein trägt Residuum + ungehedgten Faktor; bei 2,7-18,6 % Residualanteil ist der Faktor-Ballast der Drawdown-Treiber ohne Edge. Die Regel ist eine geschlossene Sharpe-Aussage — der Käfig-Check (Passquote) muss sie bestätigen, das ist der Test. | Identische Regel 1- vs. 2-beinig, Kriterium Passquote je Eval (`eval_plan.evaluate_v2`) | Die Passquoten-Rechnung dreht die Sharpe-Ordnung um (dann ist die DD-Struktur der Engpass — selbst ein Befund) | 🟢 | 1 vs 2 |

## Block AR — Gleichlauf-Regime (Absorption Ratio ≡ mittlere Paar-Korrelation)

**Mechanismus-Why:** Wie sehr handeln die 4 Indizes als **ein** Markt? Hoch = ein Makro-Faktor treibt alles, idiosynkratische Signale sind leer; niedrig = Rotation, Querschnitts-Signale tragen. Kritzman: Anstiege kündigen Fragilität an. Für uns kein eigenes Bein, sondern ein **Schalter über anderen Strategien** — die billigste Sorte Alpha, weil kostenfrei.

**Werkzeug-Korrektur (Review, exakt bewiesen):** Bei N=4 gilt AR ≥ 1/N + (1−1/N)·ρ̄, gemessene Lücke 0,07 pp, **corr(AR, ρ̄) = 0,9998**. Das Regime-Signal wird deshalb operativ als **ρ̄** definiert (Mittelwert von 6 Korrelationen, keine Eigenzerlegung, kleinere Schätzvarianz). Wo „AR" steht, ist ρ̄ gemeint. Der Kovarianz-AR (Kritzman-Original) wird **nicht** verwendet (partiell +0,33-0,42 mit Vol-Dispersion konfundiert); Vol-Dispersion läuft als **getrennte zweite** Regime-Variable mit. **Stärkster positiver Vorab-Befund der Bank:** corr(AR, VIX) nur 0,386, corr(ΔAR, ΔlogVIX) 0,115 — das Signal ist **nicht** der x-te VIX-Proxy, es gibt echten inkrementellen Raum.

| ID | Hypothese | Warum sie gut sein könnte | Prüfbar | Verwerfen wenn | Daten | Beine |
|---|---|---|---|---|---|---|
| AR-01 (sekundär) | Residual-Strategien (PR) haben ihre Edge nur bei **niedrigem** ρ̄; bei hohem gibt es nichts Idiosynkratisches zu handeln. | Aït-Sahalia/Xiu: der Faktor absorbiert in Stressphasen fast alles. Der Filter würde die PR-Zeilen von ihrem totesten Drittel befreien. Power-Warnung: ρ̄ ist extrem persistent (AC(1) 0,994, ~32 unabhängige Blöcke je Terzil) — nur ein Terzil-Unterschied von ~0,5 Sharpe wäre überhaupt nachweisbar. | **Interaktionsterm** PR-Edge × ρ̄ auf dem vollen Sample (nicht Terzil-Bestwahl) | Interaktions-CI enthält 0 | 🟢 | Filter |
| AR-02 | ρ̄-Anstieg (orthogonalisiert) sagt schlechte Tage der Buch-Beine voraus → Tagesfilter hebt die Passquote ohne neue Kosten. **Als stetige Konditionierung, nicht als Crash-Ereignis** (nur 7 Stress-Episoden in 9 Jahren — als Ereignis-Hypothese untestbar). | Kritzman-Mechanismus + der gemessene Befund, dass ρ̄ fast orthogonal zu VIX ist. Ein Filter, der nur Trades wegnimmt, hat keine Kostenlast. | Bein-Tagesergebnis ~ logVIX + RV20 + **ρ̄_orth** (Residuum von ρ̄ gegen beide); Urteil über den ρ̄_orth-Koeffizienten, Block-Bootstrap (30-Tage-Blöcke); dann ΔP(funded) über 5 Seeds | CI enthält 0, oder ΔP(funded) < 2× Seed-Streuung | 🟢🟡 | Filter |
| AR-03 (sekundär) | ❌ **Story fällt durch (strategy-auditor 21.09.2026), nicht bauen:** Umschalter zwischen zwei Armen, von denen einer (div_fade) in allen 48 Varianten tot und der andere (div_mom) „nur marginal" ist — ein Interaktionstest auf einer Null-Basis zeigt nur, in welchem Regime das Rauschen lag, keine Edge. Wiederbelebbar erst als reine Konditionierung auf einem Arm mit eigenständiger Edge, die es derzeit nicht gibt. | ~~Dispersion kann hoch sein, weil alles volatil ist (ρ̄ hoch) oder weil die Indizes auseinanderlaufen (ρ̄ niedrig) — nur der zweite Fall ist der RS-Fall.~~ | — | — | 🟢 | entfällt |
| AR-04 | Intraday-ρ̄ (rollend über 15m-Bars, gegen die Uhrzeit-Norm bis gestern) steigt an Tagen mit Nachmittags-Trend schon mittags → Vorfilter für Trend-/LastHour-Beine. | Fenn: Kopplung steigt in Bewegungsphasen — messbar Stunden vor dem LastHour-Fenster. | Nachmittags-Trendmaß ~ Mittags-ρ̄ (Interaktionstest); dann ΔP(funded) der LastHour-Beine über 5 Seeds | CI enthält 0, oder ΔP(funded) < 2× Seed-Streuung | 🟢 | Filter |

## Block F2 — Der zweite Faktor (Tech vs. Breite)

**Mechanismus-Why:** Bei 4 US-Indizes ist PC2 fast zwangsläufig die Achse NQ gegen RTY/YM. Diese Rotation wird von langsamen Allokations-Flows getrieben (RS-08-Ökonomie) — der Faktor bündelt die RS-Information in einer stetigen Größe. **Vorab-Messungen:** PC2 ist bei uns identifizierbar (Vorzeichen-Flips nach Ankerung nur 0,4 % der Tage, mediane Eigenlücke 0,48; an 9,5 % der Tage < 0,2 → die werden ausgeschlossen), teilt aber 54 % Varianz mit dem simplen vol-normierten NQ−RTY-Spread — der Zusatznutzen gegenüber dem Billig-Kontrast ist die eigentliche Frage (F2-04).

| ID | Hypothese | Warum sie gut sein könnte | Prüfbar | Verwerfen wenn | Daten | Beine |
|---|---|---|---|---|---|---|
| F2-01 | Die PC2-Bewegung der ersten Stunde (Ladungen von gestern!) setzt sich bis Close fort: Position im Index mit der betragsstärksten PC2-Ladung, Richtung PC2. | Rotation ist mehrtägig und träge; springt der Faktor morgens an, arbeitet der Flow weiter. Gegen PC1 immunisiert, nutzt alle 4 Serien. | `r_Rest ~ a·spread_NQRTY + b·PC2_orth` — Urteil über **b** (inkrementell, corr zu NQ−RTY ist 0,74) | CI von b enthält 0 (dann ist PC2 die teurere Verpackung von RS-11) | 🟢 | 1 |
| F2-02 (Streichkandidat) | An PC2-Extremen (oberstes/unterstes **Dezil** eines 252-Tage-Rollfensters, vorab fest, keine Bandsuche) kippt Fortsetzung in Umkehr. | RS-11-Verallgemeinerung. **Aber:** nur ~62 unabhängige Extrem-Episoden in 9 Jahren → nachweisbar erst ab +13 pp Trefferquote, was es realistisch nicht gibt. Steht nur noch drin, damit sie niemand „neu entdeckt". Zusatzproblem (Auditor-Riecher): kumulierter PC2 bei rollend neu geschätzten Ladungen ist kein konsistenter Zustand — muss vor jedem Test gelöst sein (Neu-Verankerung, Regel 3). | Interaktionsterm `r_Rest ~ a·PC2_1h + b·PC2_1h×Extrem`, volles Sample; Mindest-n ≥ 60 Episoden vorab | CI von b enthält 0. Unterschreitet n die 60: **gestrichen**, nicht „verworfen" — die „n zu klein"-Hintertür ist zu | 🟢 | 1 |
| F2-03 (sekundär, Gate) | PC2-Zeilen nur handeln, wenn λ2 über der p95-Rauschdecke eines **parametrischen 1-Faktor-Bootstraps** liegt (Äquikorrelations-Null mit ρ̄ aus dem laufenden Fenster, T=60) **und** Eigenlücke ≥ 0,2. | Codiert die N=4-Warnung als Filter. **Die ursprüngliche Marchenko-Pastur-Fassung war ein Konstruktionsfehler:** MP unterstellt unkorrelierte Serien (Decke 1,58), unser λ2 lebt im Residualraum (max. 1,12) — das Gate hätte an 0,0 % der Tage gefeuert und den Block grundlos getötet. Die Bootstrap-Fassung feuert an ~68-70 % der Tage (T=60) und trennt tatsächlich. | F2-Edge mit vs. ohne Gate (ΔSharpe-CI) | Gate trennt die Edge nicht (nicht: Gate feuert nie) | 🟢 | — |
| F2-04 | Der **feste Kontrast NQ−RTY** (a priori aus der Indexzusammensetzung, null Schätzparameter, kein Flip, keine Rotation) leistet für F2-01/02 dasselbe wie der geschätzte PC2. | [[Simplex beats Komplex]] als Messung: Median-Winkel NQ−RTY zu PC2 26,6° bei Bootstrap-Kegel um PC2 von 16,9° (p90 58,8°) — statistisch nicht klar unterscheidbar. Gewinnt der feste Kontrast, entfällt die halbe Modul-Komplexität. | F2-01/02 identisch mit festem Kontrast vs. geschätztem PC2 | Geschätzter PC2 schlägt den Kontrast über das Seed-Rauschen (dann verdient die Schätzung ihr Geld — auch gut) | 🟢 | 1 |

## Block ST — Schätzung & Stabilität (verdient PCA sein Geld überhaupt?)

**Mechanismus-Why:** Dieser Block prüft unser Werkzeug, nicht den Markt. Geht ST-01 gegen PCA aus, wird der Rest der Bank mit dem billigeren Werkzeug gerechnet — [[Simplex beats Komplex]] in Aktion. **Vorab-Messung:** Korrelations-PC1 liegt 1,68° am Gleichgewicht, corr(PCA-Residuum, faires EW-Residuum) = 0,93-0,999 — PCA muss aus fast identischen Signalen einen Edge-Unterschied erzeugen. Die Erwartung ist klar gegen PCA.

| ID | Hypothese | Warum sie gut sein könnte | Prüfbar | Verwerfen wenn | Daten | Beine |
|---|---|---|---|---|---|---|
| ST-01 ⭐primär | **Äquivalenztest (TOST), drei Arme bei identischer Regel:** (a) Residuum gegen rollende Korrelations-PCA, (b) gegen den gleichgewichteten Durchschnitt der **rollend vol-normierten** Returns (die faire Null!), (c) gegen den rohen Durchschnitt. Marge vorab: \|ΔSharpe\| < 0,15. | Entscheidet das Werkzeug für die ganze Bank. Zwei Fallen aus dem Review eingebaut: der **rohe** Durchschnitt wäre ein Strohmann (PCA gewänne nur die Vol-Normierung, die `x/rolling_std` gratis liefert — a-vs-b misst Faktorstruktur, b-vs-c nur Vol-Normierung); und ein normaler Signifikanztest kann Gleichheit nicht belegen (geringe Power „findet" automatisch nichts), deshalb TOST. | TOST a-vs-b; Ausgang vorab definiert: Äquivalenz → Mittelwert-Residuum, Modul schrumpft; PCA besser → behalten; **weder noch → unentschieden, Bank pausiert** (wahrscheinlichster Ausgang, braucht die Vorab-Regel) | — (Äquivalenztest hat keinen „Verwerfen"-Arm, die drei Ausgänge sind vorab definiert) | 🟢 | — |
| ST-02 | Die Schätzfrequenz der Ladungen ist ein **Bias-Varianz-Problem**, keine Bias-Frage: Epps ist bei unseren 4 Kontrakten klein (3 pp über den ganzen Frequenzbereich), der Varianzgewinn intraday riesig (715k vs. 2.250 Beobachtungen). Signature-Plot statt Zweier-Alternative. | Die ursprüngliche „Tagesschätzung ist sauberer"-Fassung stand auf schwacher Analogie (Epps 1979 = Aktien, Ticks); dazu enthalten Tagesreturns Overnight-Gaps, die eine intraday-flache Strategie nie handelt. | Identische PR-Regel mit Ladungen aus 1m/5m/15m/30m/1d | Keine Frequenz schlägt die anderen außerhalb des Seed-Rauschens (dann frei, 5m Default) | 🟢 | — |
| ST-03 (sekundär) | Fades nur bei stabiler Faktorstruktur. Maß ist die **Breite des Bootstrap-Kegels** um die PC2-Richtung (200 Row-Resamples, p95-Winkel) — **nicht** der Winkel aufeinanderfolgender Fenster: der liegt wegen 99 % Überlappung bei median 0,3-1,2° und trennt per Konstruktion nichts (Fehler der Erstfassung). Kegel gemessen: Median 17-27°, p90 bis 74° — echte Streuung, brauchbarer Filter. | Fenn: ein Fade gegen ein wanderndes Gleichgewicht ist eine verdeckte Richtungswette. Beste Power der ganzen Bank (Maß fast weiß, ~377 unabhängige Blöcke je Terzil). | Interaktionstest PR-/F2-Edge × Kegelbreite | CI enthält 0 | 🟢 | — |
| ST-04 | Roll-Wochen im **Schätzfenster** (nicht nur im Handel) verzerren Ladungen/ρ̄; Ausschluss ändert die Schätzung und hebt die Edge. | SK-11-Übertrag; Kovarianzschätzung ist gegen die nachgewiesenen Roll-Artefakte (#075) empfindlicher als ein Beta. Kostet nur eine Kalendermaske, die SK-11 ohnehin braucht. | Ladungen/ρ̄ mit vs. ohne Roll-Wochen; Edge-Differenz | Ladungen ändern sich < 2 % und Edge gleich | 🟢 | — |
| ST-05 | Ein **geschrumpfter** Ein-Faktor-Schätzer (Ledoit-Wolf gegen das Äquikorrelations-Target, Intensität δ analytisch) liefert stabilere Residuen als rohe PCA und als der Mittelwert — als dritter Arm in ST-01. | Lehrbuchfall: bei T=60 werden 10 Kovarianzparameter geschätzt, die reale Struktur ist mit 2 Zahlen (ρ̄, Vol-Dispersion) fast vollständig beschrieben; der Gewinn greift genau dort, wo die kleine Eigenlücke (0,096) die PCA instabil macht. Operationalisiert das d'Aspremont-Zitat, statt es nur zu nennen. | Verlauf von δ über die Zeit + Edge-Vergleich im ST-01-Rahmen | δ liegt durchweg nahe 0 oder 1 (Arm kollabiert auf einen der beiden anderen, überflüssig) | 🟢 | — |

---

## 🧷 Zusatz-Kontrollen (nur für diese Bank, ergänzend zu `controls.py`)

1. **Stale-Bar-Kontrolle — der wahrscheinlichste Falsch-Positiv-Erzeuger.** Anteil 1m-RTH-Bars ohne Preisänderung: **ES 12,8 %**, YM 6,7 %, RTY 6,0 %, NQ 3,9 %. Ein stehender Preis erzeugt mechanisch eine „Abweichung vom Faktor", die beim nächsten Tick verschwindet — perfekte, nicht handelbare Mean Reversion. Pflicht: Lauf mit 1 Bar Delay daneben, Edge-je-Positions-Bein-Sicht (lebt die Edge im Bein mit den meisten Null-Bars → Artefakt), Entry nur wenn der letzte Bar des Positions-Beins bewegt hat.
2. **Zufallsladungs-Kontrolle.** Identische Regel mit 200 gewürfelten orthonormalen Ladungen statt PC-Ladungen. Überlebt die Edge das, misst sie generische Querschnitts-Mean-Reversion, nicht Faktorstruktur — Analogon zum Zufallslevel-Test, den `controls.py` für Level-Strategien hat und für Faktor-Strategien nicht.
3. **Buch-Marginal als Menge.** Die Residuen summieren auf ≈ 0: „ES faden" und „RTY faden" (Residuen-corr −0,72) sind weitgehend derselbe Trade gespiegelt. PCA-Kandidaten werden im Buch-Marginal **gemeinsam** gerechnet, nie einzeln nacheinander promotet, plus Korrelationsgate zwischen den neuen Beinen selbst (Lehre 82: „Bein dazu" = „mehr Position").

## 📋 Buch-Lücke (Stand 30.08.2026, nach Quant-Review)

Alle Zeilen stehen auf **Prämisse**. Reihenfolge:

1. **Prä-Registrierung fixieren** (Tabelle oben) — Primärstatistiken schriftlich, bevor irgendetwas rechnet.
2. **PR-04 (VR-Test) zuerst:** ein Test, kein Grid, entscheidet den ganzen PR-Block. Ist VR nirgends < 1, ist die Bank erledigt, bevor ein Modul gebaut wird.
3. **ST-01 (TOST):** entscheidet, ob das PCA-Modul überhaupt gebaut wird. Der AR-Block braucht es nachweislich nicht (ρ̄ reicht, 3 Zeilen Code).
4. Erst danach Querschnitts-Modul (Bausteine siehe Legende) + Jobs über `hypothesis_bank.py` (≥ 10 Implementierungen, `GATES_HARD`, `controls.py` + die 3 Zusatz-Kontrollen), Rechnung auf der Box.
5. F2-03 nur in der Bootstrap-Fassung. F2-02 ist Streichkandidat.
