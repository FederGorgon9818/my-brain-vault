---
tags:
  - bereich/trading
  - trading/alpha
  - trading/hypothesen
  - trading/relative-value
erstellt: 2026-08-23
status: offen (noch nichts getestet)
---
# 🧪 Hypothesen-Bank: Pairs Trading & Relative Value

⬅️ [[Alpha-Suche]] · [[Strategie-Familien]] · [[Discovery-Runner v2]] · [[Strategie-Logbuch]] · [[Research-Cache]]
Schwester-Banken: [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]]

> [!important] Was das ist
> Max' Auftrag 23.08.2026: aus der Pairs-Trading-/Stat-Arb-Literatur (Journals, SSRN, arXiv, Scholar) **100 falsifizierbare Hypothesen** ableiten, **alle käfigtauglich** — also im Prop-Käfig (E8, intraday only, Min-Size) mit unseren Daten testbar. Nur gesammelt, **noch nichts davon getestet**. Relative Value ist die einzige der 5 [[Strategie-Familien]] ohne aktuell bestätigten Kandidaten (#090) — das hier ist der Vorrat, um das zu ändern.

---

## 🔒 Der Käfig-Filter (warum 90 % der Pairs-Literatur bei uns rausfällt)

Bevor irgendeine Hypothese hier landet, muss sie durch fünf harte Tore. Ich habe die Literatur bewusst dagegen gefiltert, statt schöne Paper zu zitieren, die wir nie handeln können:

| Tor | Regel | Was dadurch stirbt |
|---|---|---|
| **1. Intraday only** | E8 erlaubt kein Overnight. Flat vor Close. | Die **komplette klassische Kointegrations-Literatur** (Gatev et al. 2006, Krauss/Stübinger, Avellaneda/Lee): Haltedauern von Tagen bis Wochen, Halbwertszeiten > 1 Tag. Nicht handelbar, nur als Mechanismus-Vorlage nutzbar. |
| **2. Nur 4 Instrumente** | ES, NQ, RTY, YM (1m, 2016-01 bis 2026-07). Keine Aktien, keine ETFs, kein CL/GC/ZN, kein Orderbuch, keine Options-Chains. | Die **gesamte Pair-Selection-Literatur**. Bei 100+ Aktien ist „welches Paar" die Hauptarbeit; bei uns gibt es genau **6 Paare** (ES-NQ, ES-RTY, ES-YM, NQ-RTY, NQ-YM, RTY-YM). Vielfalt muss aus Signalbau, Timing, Konditionierung und Exit kommen, nicht aus dem Universum. |
| **3. Doppelte Kosten** | Zwei Beine = 2 × Spread + 2 × Commission je Richtung. | `div_fade` ist bei uns in **allen 48 Varianten** gestorben (#033), genau daran. Jede 2-Bein-Hypothese muss zeigen, dass die Spread-Bewegung groß genug ist — Standard bei Index-Futures, die zu ~93 % korrelieren, ist sie es meistens nicht. **Deshalb ist jede Zeile hier mit `Beine 1/2` markiert.** |
| **4. Min-Size (#106)** | 1 Kontrakt je Bein. „Bein dazu" = „mehr Position" (Lehre 82). | Portfolio-Stat-Arb über viele gleichzeitige Spreads. Wir handeln einen Spread, nicht 40. |
| **5. Passquote je Eval** | Einziges Kriterium (#106). Nicht Sharpe, nicht Edge. Trailing-DD, Intraday-Bust-Check (#077). | Alles, was Edge über sehr viele sehr kleine Trades erzeugt (klassisches HF-Stat-Arb). Unter Min-Size + Kosten bleibt davon nichts. |

**Konsequenz, die durch die ganze Bank zieht:** Die kostengünstigste Form von Relative Value ist bei uns **das Paar als Signal, ein einziges Bein als Position** (Beine = 1). Genau das war `RV_leadlag` — und genau das ist die Familie, in der noch am ehesten etwas liegt. 2-Bein-Hypothesen stehen trotzdem drin, aber mit offener Beweislast.

## ⚠️ Zwei Warnungen aus unserer eigenen Geschichte

1. **Der R_pts-Fehler (#090, Lehre 46).** Bei Lead-Lag sind Signal-Symbol und PnL-Träger verschiedene Instrumente. Jede Risiko-, PnL- und Kosten-Normierung muss am **Bein hängen, das die Position trägt**. Der Fehler ließ `RV_leadlag_NQES` mit PF 1,37 statt echt PF 0,91 dastehen — Faktor 3,1 auf den Kosten-Drag. **Jede Hypothese hier, die zwei Symbole mischt, ist demselben Fehler ausgesetzt.**
2. **Korrupte Serien (#075).** ES 780 Bars und RTY 8.591 Bars mit Preis ≤ 0 aus Kalender-Spread-Quotes der Quartals-Rolls. Zwei Leadlag-Trades auf solchen Tagen trugen 22,3 % des Leg-P&L. Der Guard `_drop_corrupt_sessions` existiert — **bei jedem Paar-Test muss er aktiv sein**, sonst ist das Ergebnis Müll. NQ und YM sind clean.

## 📉 Und die unbequemste Zahl der ganzen Literatur

Krauss' Meta-Review über 76 Pairs-Trading-Studien: im Schnitt **10,8 % p.a. bei Sharpe 0,96** — aber der Verlauf ist **15,6 % vor 2000 → 6,4 % nach 2010**. Do/Faff führen das auf Crowding und Effizienz zurück; Avellaneda/Lee liefern denselben Knick (Sharpe 1,44 über 1997-2007, aber nur 0,9 in 2003-2007). **Die Erwartungshaltung an diese ganze Bank muss entsprechend niedrig sein.** Ich halte das für den ehrlichsten Kontext, den man vor 100 Hypothesen setzen kann: die Familie ist akademisch belegt und gleichzeitig akademisch als schrumpfend belegt. Was bei uns noch übrig sein kann, ist der Teil, der *nicht* gecrowdet ist — Intraday, Index-Futures untereinander, unter Käfig-Nebenbedingungen. Nicht der klassische Spread-Fade.

---

## Legende
- **Daten:** 🟢 sofort testbar (1m OHLCV ES/NQ/RTY/YM 2016-2026) · 🟡 vorhandene Tages-Zusatzdaten nötig (VIXCLS, DGS2/DGS10, DTWEXBGS, DIX_GEX_daily, Kalender) · 🔴 Daten fehlen
- **Engine:** ✅ bestehender Modus reicht (`rv.py` kann `div_fade`, `div_mom`, `leadlag`, `gap_div`, `eod_conv`) · 🔧 neues Feature/Modul nötig
- **Beine:** **1** = Paar liefert nur das Signal, Position in einem Instrument (kostengünstig) · **2** = echter Spread, doppelte Kosten (Beweislast höher)
- **ID-Präfixe:** LL Lead-Lag · SM Spread-Mean-Reversion · RS Relative Strength · SK Spread-Konstruktion · ZF Zeitfenster · RG Regime-Filter · EV Event/Kalender · MS Mikrostruktur · KX Käfig/Exit · KO Kosten/Kontrolle

## Friedhof (nicht wieder testen, nur zur Abgrenzung)
- `RV_leadlag_NQES` in der gebuchten Form: tot nach Engine-Fix, PF 0,91, expR −0,074 (#090). Der Mechanismus ist damit **nicht** widerlegt, die konkrete Config schon.
- `RV_leadlag_NQRTY`: Totalschaden über alle 8 Configs, PF 0,36-0,57 (#090).
- `div_fade` in allen 48 Varianten: tot an doppelten Kosten (#033).
- `eod_conv`: tot (#033).
- `div_mom`: nur marginal, Bank-Status (#033).
- `gap_div`: Bug (Division durch Mini-Risiko bei Konvergenz bis Entry), Modul-Fix ausstehend (#033) — **Zeilen mit gap_div erst nach dem Fix testbar.**
- Multi-Day-Kointegrations-Paare: durch Overnight-Verbot gesperrt, nur [[Live-Account]].
- RV_mom im Pool-Neuaufbau: −4 bis −15 pp Buchbeitrag OOS (#123).

## Status-Workflow
Hypothese → Quant-Team prüft Why + Power → Discovery-Job (`inbox_tool.py --add-job`) → Ergebnis in Inbox → Zeile hier mit ✅/❌/➖ und Logbuch-Nummer markieren. Getestete Hypothesen bleiben stehen, der Friedhof ist Wissen.

---

## Block LL — Lead-Lag & Informationsdiffusion (14)

**Forschungsbasis:** Hasbrouck (Information Share, NYU FIN-00-046) — Preisfindung in US-Index-Märkten liegt dominant bei den Futures, ETFs tragen signifikant aber klein bei; in Hochvola-Phasen dominiert der E-mini, sonst führt zeitweise SPY. Cont/Cucuringu/Zhang (Quantitative Finance 2023, „Cross-impact of order flow imbalance") — verzögerte Cross-Asset-Signale verbessern Return-Prognosen nur über wenige Minuten und zerfallen danach schnell. Ältere Futures-Spot-Literatur misst Vorläufe von 5-15 Minuten. Der Mechanismus ist graduelle Informationsdiffusion, nicht Arbitrage.
**Unser Stand:** Der Mechanismus hat bei uns einmal Grade A gezeigt und ist an einem Rechenfehler gestorben, nicht am Mechanismus (#090). Höchste Priorität — und Beine = 1, also kostenverträglich.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| LL-01 | Weil der Mechanismus (Diffusion) nie widerlegt wurde, sondern nur eine Config an einem Normierungsfehler starb, überlebt mindestens eine der 12 gerichteten Paarungen (6 Paare × 2 Richtungen) den sauberen Nachtest mit korrektem `R_pts` und 2-Tick-Kostenstress. | Voller `leadlag`-Sweep über alle 12 Richtungen, gefixter Code, `_drop_corrupt_sessions` aktiv, IS/OOS-Split, `cost_stress_ticks=2.0` | Keine einzige Richtung mit OOS-expR > 0 nach Kostenstress → der ganze Block LL fällt | 🟢 | ✅ `rv_mode="leadlag"` | 1 |
| LL-02 | Weil neue Information zuerst dort eingepreist wird, wo Beta und Reaktion am größten sind, ist der Leader systematisch das volatilere Instrument (NQ, RTY) und der Laggard das breitere (ES, YM) — nicht umgekehrt. | Gerichtete Vorlaufstärke (Kreuzkorrelation r(leader_t, lagg_t+k), k=1..10 min) je Paar gegen das Vola-Verhältnis der Beine | Vorlaufrichtung korreliert nicht mit dem Vola-Verhältnis oder dreht im OOS | 🟢 | 🔧 Kreuzkorrelations-Diagnostik (kein Trade) | 1 |
| LL-03 | Weil zu verschiedenen Tageszeiten verschiedene Akteure dominieren, rotiert die Führung im Tagesverlauf (Open tech-getrieben NQ, Mittag ES, Nachmittag Sektorrotation RTY), statt konstant zu sein. | Rollender Information-Share je 30-Min-Fenster über alle 6 Paare, 10 Jahre, Bootstrap-CI je Fenster | Führungsanteil je Fenster nicht von 50 % trennbar oder Muster instabil zwischen 2016-2021 und 2022-2026 | 🟢 | 🔧 Information-Share je Uhrzeitfenster | 1 |
| LL-04 | Weil Cross-Impact-Information laut Cont et al. binnen Minuten zerfällt, liegt die gesamte Edge in den ersten 1-3 Minuten nach dem Leader-Move; ein Entry nach Minute 10 ist wertlos. | Edge je Entry-Verzögerung (1,2,3,5,10,15,30 min nach Trigger), gleiche Exit-Regel | Edge fällt nicht monoton mit der Verzögerung, oder Minute 1-3 ist nicht besser als Minute 10+ | 🟢 | ✅ `leadlag` + Entry-Delay | 1 |
| LL-05 | Weil der E-mini laut Hasbrouck gerade in Hochvola-Phasen die Preisfindung dominiert, existiert der Effekt nur oberhalb eines Vola-Schwellenwerts und verschwindet in ruhigen Sessions. | Edge getrennt nach VIX-Terzil bzw. realisierter Vormittags-Vola des Leaders | Kein monotoner Zusammenhang Vola → Edge, oberes Terzil nicht signifikant über dem unteren | 🟡 | ✅ `leadlag` + VIX-/RV-Gate | 1 |
| LL-06 | Weil der Laggard eine eigene Beta-Beziehung zum Leader hat, holt er nur den Bruchteil β des Leader-Moves nach — ein Ziel auf volle Konvergenz ist systematisch zu weit und wird nie erreicht. | Verteilung des nachgeholten Anteils je Trade; Edge bei Ziel 1,0 × Rest-Gap vs. 0,5 × vs. β̂ × | β-skaliertes Ziel schlägt das volle Ziel nicht, oder der nachgeholte Anteil hat keine stabile Zentrale | 🟢 | 🔧 β-skalierter Take-Profit in `rv.py` | 1 |
| LL-07 | Weil ein sehr großer Leader-Move ein gemeinsamer Schock ist (beide reagieren sofort) und kein Diffusionsvorgang, kippt die Edge oberhalb einer Schwelle ins Negative — der Zusammenhang ist ein umgekehrtes U, nicht monoton. | Edge über Leader-Move-Dezile (0,05 % bis 1,0 %), Vorzeichen und Höhe je Dezil, separat IS/OOS | Edge steigt monoton mit der Move-Größe (dann Momentum statt Diffusion) oder ist über alle Dezile flach | 🟢 | ✅ `leadlag` + Move-Obergrenze | 1 |
| LL-08 | Weil negative Information schneller eingepreist wird als positive, ist der Vorlauf asymmetrisch: Abwärts-Leader-Moves liefern eine zuverlässigere Laggard-Reaktion als Aufwärts-Moves. | Edge getrennt nach Vorzeichen des Leader-Moves, Block-Bootstrap-CI auf die Differenz | Differenz Long/Short nicht von 0 trennbar oder dreht im OOS | 🟢 | ✅ `leadlag` + Richtungs-Split | 1 |
| LL-09 | Weil ein Leader-Move ohne Volumen nur eine dünne Quote ist und keine Information trägt, filtert RVOL des Leaders die Fehlsignale: Vorlauf existiert nur bei RVOL > 1,5 im Trigger-Fenster. | Edge mit/ohne RVOL-Gate am Leader (Trigger-Volumen / Median derselben Minuten der letzten 20 Tage) | Gate hebt die Edge um < 3 pp oder halbiert die Trade-Zahl ohne Edge-Gewinn | 🟢 | 🔧 RVOL-Gate am Signal-Symbol (nicht am Positions-Symbol) | 1 |
| LL-10 | Weil Korrelationen laut Epps-Literatur unter Handelszeit schneller entstehen als unter Kalenderzeit, ist ein in Volumen-Zeit gemessener Vorlauf schärfer als der in Minuten gemessene. | Identische Regel auf Zeit-Bars vs. Volumen-Bars (fixes Kontraktvolumen je Bar), Trade-Zahl angeglichen | Volumen-Bar-Variante schlägt die Zeit-Bar-Variante nicht oder nur im Seed-Rauschen | 🟢 | 🔧 Volumen-Bar-Aggregator in `qbt.py` | 1 |
| LL-11 | Weil ein Move nur dann Marktinformation ist, wenn er breit getragen wird, liefert Bestätigung durch ein drittes Instrument die Trennung: Trade nur, wenn 2 der 3 anderen Indizes dieselbe Richtung zeigen. | Edge mit Konsens-Gate (2/3) vs. ohne, plus Basisrate bei Uneinigkeit | Konsens-Variante nicht besser oder Uneinigkeitsfälle nicht messbar schlechter | 🟢 | 🔧 Multi-Symbol-Konsens-Filter (4 Serien) | 1 |
| LL-12 | Weil ein Laggard gegen seinen eigenen Trend nur widerwillig nachzieht, funktioniert der Trade nur, wenn die Trigger-Richtung dem Vormittagstrend des Laggards nicht widerspricht. | Edge getrennt nach Übereinstimmung Signalrichtung ↔ Vorzeichen des Laggard-Returns seit Open | Nicht-übereinstimmende Fälle nicht signifikant schlechter | 🟢 | ✅ `leadlag` + Trend-Gate am Positions-Symbol | 1 |
| LL-13 | Weil der Dow nur 30 preisgewichtete Mega-Caps enthält, verarbeitet YM Information am langsamsten und ist der beste Laggard aller vier — besser als ES, das durch SPY-Arbitrage extrem eng geführt wird. | Vorlaufstärke für Laggard ∈ {ES, YM, RTY} bei gleichem Leader (NQ), gleiche Parameter | YM nicht besser als ES, oder Unterschied innerhalb der Bootstrap-Streuung | 🟢 | ✅ `leadlag` mit YM als Symbol 2 | 1 |
| LL-14 | Weil Übernacht-Information beim Open asynchron in die vier Kontrakte einfließt, ist der Vorlauf in den ersten 15 Minuten nach 09:30 am stärksten und verschwindet danach. | Edge je Trigger-Uhrzeit-Bucket (09:30-09:45 / 09:45-10:15 / 10:15-11:00 / Rest), Trade-Zahl je Bucket | Erstes Fenster nicht besser, oder Effekt verschwindet nach Kontrolle auf die höhere Open-Vola | 🟢 | ✅ `leadlag` + Uhrzeit-Bucket | 1 |

---

## Block SM — Spread-Mean-Reversion & Divergenz-Fade (13)

**Forschungsbasis:** Leung/Li (arXiv 1411.5062, „Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit") — optimales doppeltes Stoppproblem unter OU: die Eintrittsregion ist ein **begrenztes Intervall strikt über dem Stop-Loss**, und ein höherer Stop-Loss impliziert immer ein niedrigeres optimales Take-Profit. Das ist für uns die wichtigste Formel der ganzen Literatur, weil sie Entry, TP und Stop **gekoppelt** löst statt getrennt. Dazu: Hurst-/GHE-Selektion schlägt auf Intraday-Daten Distance, Correlation und Cointegration; Mean Reversion ist in anti-persistenten Phasen wahrscheinlicher und schneller. Han et al. (J. Supercomputing 2021): Strukturbrüche in der Kointegration sind im Intraday-Pairs-Trading der Haupt-Verlusttreiber.
**Unser Stand:** `div_fade` ist in 48 von 48 Varianten an den doppelten Kosten gestorben (#033). Der Block startet deshalb mit einer Kontroll-Hypothese, die über den ganzen Block entscheidet.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| SM-01 | **Kontrolle zuerst, entscheidet den ganzen Block:** Es existiert mindestens eine Kombination aus Paar und Schwelle, bei der die mittlere Spread-Rückbewegung nach Entry ≥ 4 × Round-Trip-Kosten beider Beine beträgt. Ohne diese Zahl ist jede weitere SM-Zeile Zeitverschwendung. | Reine Messung ohne Trading: je Paar und z-Schwelle mittlere Spread-Konvergenz bis Session-Ende gegen 2 × (Spread + Commission) beider Beine, in Dollar | Kein Paar und keine Schwelle erreicht Faktor 4 → SM-02 bis SM-12 werden nicht getestet, nur SM-13 bleibt | 🟢 | 🔧 Messskript (kein Backtest) | 2 |
| SM-02 | Weil Mean Reversion laut Hurst-Literatur nur in anti-persistenten Phasen schnell eintritt, filtert ein rollender Hurst-Exponent des Spreads (H < 0,45) die Signale, die sonst in Trendphasen ausgestoppt werden. | Edge mit/ohne H-Gate (rollendes Fenster 120 min, GHE-Schätzer), Trefferquote und expR je H-Terzil | H-Terzile unterscheiden sich nicht messbar oder das Gate kostet mehr Trades als es Edge bringt | 🟢 | 🔧 Hurst-/GHE-Schätzer auf den Spread | 2 |
| SM-03 | Weil vor Close glattgestellt werden muss, ist ein Fade nur sinnvoll, wenn die geschätzte OU-Halbwertszeit kleiner ist als die verbleibende Sessionzeit — Signale spät am Tag mit langer Halbwertszeit sind strukturell verloren. | OU-Fit (κ) auf rollendem Fenster; Edge getrennt nach Verhältnis Halbwertszeit / Restzeit (<0,25 / 0,25-0,5 / 0,5-1 / >1) | Kein Zusammenhang zwischen Verhältnis und Edge, oder auch Fälle mit Verhältnis > 1 sind profitabel | 🟢 | 🔧 rollender OU-Fit (κ, μ, σ) in `rv.py` | 2 |
| SM-04 | Weil die optimale Eintrittsregion laut Leung/Li ein begrenztes Intervall ist, ist die Edge über der z-Schwelle nicht monoton: sehr extreme Divergenzen (z > 3) sind kein besseres Signal, sondern Strukturbruch, und liefern negative Edge. | Edge über z-Buckets (1,0-1,5 / 1,5-2 / 2-2,5 / 2,5-3 / >3), Vorzeichen und Trade-Zahl je Bucket | Edge steigt monoton mit z (dann ist die begrenzte Eintrittsregion bei uns nicht relevant) | 🟢 | ✅ `div_fade` + z-Bucket-Auswertung | 2 |
| SM-05 | Weil laut Leung/Li ein höherer Stop-Loss zwingend ein niedrigeres optimales Take-Profit impliziert, ist unser übliches unabhängiges Sweepen von Stop und TP falsch: das Optimum liegt auf einer fallenden Kurve, nicht im Kreuzprodukt. | 2D-Gitter Stop × TP; prüfen, ob das Optimum je Stop-Niveau mit steigendem Stop monoton fällt | Optimum-Kurve flach oder steigend → die analytische Kopplung überträgt sich nicht auf unsere Kostenstruktur | 🟢 | ✅ `div_fade` 2D-Sweep + Auswertung | 2 |
| SM-06 | Weil RTY als Small-Cap-Index die größte idiosynkratische Bewegung gegen die drei Large-Cap-Indizes hat, haben RTY-Paare die höchste Spread-Vola und als einzige ein tragfähiges Verhältnis von Bewegung zu Kosten. | Spread-Vola (Dollar je Kontraktpaar) je der 6 Paare, gegen die jeweiligen Round-Trip-Kosten normiert | RTY-Paare haben kein besseres Verhältnis, oder ihre höhere Vola geht vollständig in höhere Stop-Verluste | 🟢 | 🔧 Diagnostik-Skript (Vorstufe zu SM-01) | 2 |
| SM-07 | Weil der faire Anker eines Intraday-Spreads nicht null ist, sondern der bisher gehandelte Durchschnitt, revertiert der Spread zum VWAP des Spreads seit Open, nicht zu einem rollenden Mittel und nicht zum Open-Wert. | Drei Anker-Varianten (Open-Wert / rollendes 60-min-Mittel / Spread-VWAP) bei sonst identischen Parametern | Spread-VWAP nicht besser als das rollende Mittel oder Unterschied im Seed-Rauschen | 🟢 | 🔧 Spread-VWAP als Ankeroption in `rv.py` | 2 |
| SM-08 | Weil eine innerhalb der Session entstandene Divergenz Verarbeitungsungleichgewicht ist, eine über Nacht entstandene dagegen echte Neubewertung, revertiert nur die erste; Gap-Divergenzen laufen weiter statt zu konvergieren. | Edge getrennt nach Herkunft der Divergenz (Spread bei Open ≈ Vortagesschluss vs. Gap-Spread), gleiche Fade-Regel | Beide Herkünfte verhalten sich gleich, oder Gap-Divergenzen konvergieren ebenfalls | 🟢 | ⚠️ `gap_div` erst nach dem Modul-Fix (#033) | 2 |
| SM-09 | Weil laut Han et al. Strukturbrüche der Haupt-Verlusttreiber sind, hebt ein Strukturbruch-Veto (rollende 60-min-Korrelation der Beine fällt unter 0,7) die Edge stärker als jede Parameteroptimierung. | Edge mit/ohne Korrelations-Veto; separat: Anteil der größten 5 Verluste, die im Veto-Bereich lagen | Veto entfernt weniger als die Hälfte der Tail-Verluste oder senkt die Edge | 🟢 | 🔧 rollende Paar-Korrelation als Gate | 2 |
| SM-10 | Weil im Mittagsfenster am wenigsten neue Information eintrifft, ist 11:30-13:30 das einzige Fenster, in dem Spread-Mean-Reversion die Kosten schlägt; Divergenzen am Open und in der letzten Stunde sind informationsgetrieben und laufen weiter. | Edge je Uhrzeitfenster (Open / Vormittag / Mittag / Nachmittag / letzte Stunde), Trade-Zahl je Fenster | Mittagsfenster nicht signifikant besser, oder Trade-Zahl dort zu klein (n < 150) | 🟢 | ✅ `div_fade` + Zeitfenster | 2 |
| SM-11 | Weil eine Divergenz mit hoher Dispersion über alle vier Indizes Sektorrotation ist (echte Umschichtung, konvergiert nicht) und mit niedriger Dispersion nur Rauschen (konvergiert), trennt die Querschnitts-Streuung gute von schlechten Fades. | Dispersion = Standardabweichung der vier Tagesreturns bis Signalzeit; Edge je Dispersions-Terzil | Kein Zusammenhang oder Vorzeichen dreht zwischen IS und OOS | 🟢 | 🔧 4-Symbol-Dispersionsmaß | 2 |
| SM-12 | Weil die Abhängigkeit zweier Indizes nicht linear ist (Tail-Abhängigkeit in Stress), schlägt ein Copula-Mispricing-Index (kumulierte bedingte Wahrscheinlichkeit minus 0,5, nach Krauss/Stübinger) den einfachen z-Score als Signal. | Beide Signale bei identischer Exit-Regel; t-Copula auf 60-Tage-Formationsfenster, Mispricing-Index kumuliert | Copula-Signal schlägt z-Score nicht oder nur um weniger als die Seed-Streuung | 🟢 | 🔧 Copula-Modul (t-Copula-Fit + Mispricing-Index) | 2 |
| SM-13 | **Die Ein-Bein-Rettung des Blocks:** Weil doppelte Kosten das eigentliche Problem sind, ist ein Fade nur des überschießenden Beins (Position ausschließlich im Instrument, das gegenüber den anderen drei am weitesten abweicht) profitabel, obwohl der 2-Bein-Spread es nicht ist. | Identisches Signal, Position nur im Ausreißer-Instrument; Edge und expR gegen die 2-Bein-Variante | Ein-Bein-Variante ebenfalls negativ → Divergenz-Fade ist bei uns endgültig tot, nicht nur zu teuer | 🟢 | 🔧 Ein-Bein-Ausführung im Fade-Modus | 1 |

---

## Block RS — Relative Strength & Divergenz-Momentum (11)

**Forschungsbasis:** Krauss/Stübinger (S&P 100, Copula-Framework) finden, dass **beide Richtungen funktionieren**: die Top-5-Mean-Reversion-Paare liefern 7,98 % p.a., die Top-5-**Momentum**-Paare 7,22 % p.a. Divergenz ist also nicht automatisch ein Fade-Signal, sie kann genauso ein Fortsetzungssignal sein, und welche der beiden gilt, ist eine empirische Frage je Paar und Regime. Praktiker-Variante: 5-Tage-Relative-Stärke über ES/NQ/YM/RTY, long der stärkste, short der schwächste.
**Unser Stand:** `div_mom` war in #033 „nur marginal, Bank-Status", also nicht getötet, nur nicht gut genug. Wichtig: die Ein-Bein-Variante (nur den stärksten kaufen) wurde nie sauber gegen die Zwei-Bein-Variante gestellt.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| RS-01 | Weil laut Krauss/Stübinger Momentum-Paare fast so gut abschneiden wie Mean-Reversion-Paare, ist Divergenz bei Index-Futures ein Fortsetzungs- und kein Umkehrsignal: `div_mom` schlägt `div_fade` bei identischen Parametern. | Direkter Kopf-an-Kopf-Vergleich beider Modi auf demselben Gitter, gleiche Paare, Schwellen, Exits | `div_mom` ist nicht besser als `div_fade` oder beide sind negativ | 🟢 | ✅ `div_mom` vs `div_fade` | 2 |
| RS-02 | Weil Rangfolge robuster ist als Abstand, liefert das Ranking der vier Indizes nach Return seit Open ein besseres Signal als der paarweise z-Score: Long im Rang-1-Instrument allein trägt die Edge. | Querschnitts-Ranking der 4 Returns seit Open zur Signalzeit; Position nur im Rang 1 bzw. nur Short im Rang 4; Edge gegen Basisrate | Rang-1-Instrument schlägt eine zufällige Auswahl der vier nicht | 🟢 | 🔧 Querschnitts-Ranking-Modul über 4 Serien | 1 |
| RS-03 | Weil Informationsdiffusion eine endliche Reichweite hat, ist Intraday-Relative-Stärke über 30-60 Minuten persistent und kippt danach in Umkehr: es gibt einen messbaren Vorzeichenwechsel-Horizont. | Autokorrelation des RS-Rangs über Horizonte 5/15/30/60/120 min; Edge einer Fortsetzungsregel je Horizont | Kein Vorzeichenwechsel auffindbar oder Autokorrelation über alle Horizonte null | 🟢 | 🔧 Rang-Autokorrelations-Diagnostik | 1 |
| RS-04 | Weil Kauf- und Verkaufsdruck unterschiedlich schnell wirken, ist die Edge asymmetrisch: Short im schwächsten Index liefert mehr als Long im stärksten (oder umgekehrt), und die 2-Bein-Version verwässert genau diesen Unterschied. | Edge getrennt: nur Long Rang 1 / nur Short Rang 4 / beides (2 Beine), gleiche Signalzeit | Beide Seiten liefern dasselbe (dann ist die Zwei-Bein-Version nur teurer, aber nicht falsch) | 🟢 | 🔧 Rangbasierte Ein-Bein-Ausführung | 1 |
| RS-05 | Weil ein Relative-Stärke-Trade ohne Marktrichtung ein reiner Beta-Trade ist, funktioniert Long-Rang-1 nur, wenn der Gesamtmarkt (ES) selbst positiv ist: Relative Stärke in einem fallenden Markt ist nur geringerer Verlust, kein Gewinn. | Edge getrennt nach Vorzeichen des ES-Returns seit Open, mit Trade-Zahl je Zelle | Kein Unterschied zwischen steigendem und fallendem Markt | 🟢 | 🔧 Marktrichtungs-Gate über Referenzsymbol | 1 |
| RS-06 | Weil bei geringer Streuung zwischen den vier Indizes das Ranking nur Rauschen sortiert, existiert die Edge erst oberhalb einer Mindest-Dispersion (Standardabweichung der vier Returns über dem Median). | Edge je Dispersions-Terzil zur Signalzeit; Trade-Zahl je Terzil | Oberes Terzil nicht besser als das untere, oder Effekt verschwindet nach Kontrolle auf die allgemeine Vola | 🟢 | 🔧 4-Symbol-Dispersionsmaß (gemeinsam mit SM-11) | 1 |
| RS-07 | Weil der eigene VWAP der Anker jedes Instruments ist, ist der bessere Relative-Stärke-Messwert nicht der Roh-Return, sondern der Abstand zum eigenen VWAP in eigenen ATR-Einheiten, im Querschnitt verglichen. | Ranking nach Roh-Return vs. nach VWAP-Abstand in ATR, sonst identisch | VWAP-Abstands-Ranking schlägt das Return-Ranking nicht | 🟢 | 🔧 VWAP-Abstand normiert, über 4 Serien | 1 |
| RS-08 | Weil Sektorführung mehrtägig ist (Tech-Regime, Small-Cap-Regime), ist der Index, der gestern die Rangfolge angeführt hat, heute überproportional oft wieder vorn: nutzbar als reines Auswahlkriterium, ohne Overnight-Position. | Übergangsmatrix der Tagesrangfolge (Rang gestern nach Rang heute) über 10 Jahre, gegen die 25-Prozent-Zufallserwartung | Übergangsmatrix nicht von der Gleichverteilung trennbar | 🟢 | 🔧 Tagesrang-Statistik als Vorfilter | 1 |
| RS-09 | Weil Positionierung im Tagesverlauf gedreht wird, ist der Index mit der stärksten ersten Stunde überproportional der schwächste der letzten Stunde: eine Intraday-Rang-Umkehr, kein Fortsetzungseffekt. | Zusammenhang Rang(09:30-10:30) zu Rang(15:00-16:00) über 10 Jahre; Edge einer Umkehrregel | Ränge sind unabhängig oder positiv statt negativ verbunden | 🟢 | 🔧 Zwei-Fenster-Rangvergleich | 1 |
| RS-10 | Weil Relative Stärke ohne Streuung nicht existieren kann, ist Dispersion selbst das Regime-Signal: an Tagen mit hoher Querschnitts-Streuung funktioniert RS-Momentum, an Tagen mit niedriger funktioniert Spread-Fade. Dieselbe Größe schaltet zwischen zwei Strategien um. | Edge beider Modi (`div_mom`, `div_fade`) je Dispersions-Terzil; prüfen, ob sich die Vorzeichen kreuzen | Kein Kreuzungspunkt, ein Modus dominiert in allen Terzilen | 🟢 | ✅ beide Modi + Dispersions-Split | 1/2 |
| RS-11 | Weil das NQ/ES-Verhältnis Technologie-Führerschaft misst und laut Praktiker-Literatur an historischen Extremen (über dem 95. Perzentil der 12-Monats-Werte) zur Umkehr neigt, liefert ein Intraday-Einstieg an solchen Tagen eine erhöhte Fade-Trefferquote. | Tages-Ratio NQ/ES, rollendes 12-Monats-Perzentil; Edge eines Intraday-Fades an Tagen im obersten/untersten Perzentil-Bereich | Trefferquote an Extremtagen nicht über der Basisrate, oder n zu klein für eine Aussage | 🟢 | 🔧 Tages-Ratio-Perzentil als Tagesfilter | 1 |

---

## Block SK — Spread-Konstruktion & Hedge-Ratio (11)

**Forschungsbasis:** Kalman-Literatur (QuantStart, Palomar „Portfolio Optimization" Kap. 15.6) — rollende OLS-Betas schwanken wild (Beispielspanne 0,6 bis 1,2), Kalman-Betas bleiben in einem engen Band (0,55 bis 0,65), und die daraus gebauten Spreads sind messbar stationärer und mean-revertierender. Avellaneda/Lee (Quantitative Finance 2010, SSRN 1153505) extrahieren systematische Faktoren per PCA und handeln das mean-revertierende **Residuum** über einen s-Score (Abstand zum Gleichgewicht in Standardabweichungen), Sharpe 1,44 über 1997-2007, aber nur 0,9 in 2003-2007.
**Unser Stand:** `rv.py` rechnet im Return-Raum seit Entry und normiert auf einen Referenzpreis; ein echter Hedge-Ratio-Schätzer existiert nicht. Das ist der Block mit dem größten Hebel pro Aufwand, weil er alle anderen Blöcke gleichzeitig verbessert.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| SK-01 | Weil ein Kalman-geschätztes Beta laut Literatur deutlich stabiler ist als ein rollendes OLS-Beta, ist der damit gebaute Spread stationärer und liefert bei identischer Handelsregel mehr Edge. | Spread aus Kalman-Beta vs. rollendem OLS-Beta vs. festem Beta gleich 1; ADF-Statistik des Spreads und Edge der identischen Regel | Kalman-Spread ist nicht stationärer oder die Edge-Differenz liegt im Seed-Rauschen | 🟢 | 🔧 Kalman-Filter für Beta in `rv.py` | 2 |
| SK-02 | Weil die vier Indizes um Faktor 5 unterschiedliche Preisniveaus haben, ist ein Spread als Log-Ratio skaleninvariant und über 10 Jahre vergleichbar, während eine Preisdifferenz mit dem Niveau mitwächst und alte Signale unvergleichbar macht. | Identische Regel auf Log-Ratio-Spread vs. Preisdifferenz-Spread; Stabilität der optimalen Schwelle über 2016-2019 vs. 2022-2026 | Log-Ratio bringt keine stabilere Schwelle über die Zeit | 🟢 | 🔧 Spread-Definition als Option in `rv.py` | 2 |
| SK-03 | Weil ein Kontrakt ES 50 Dollar je Punkt und ein Kontrakt NQ 20 Dollar je Punkt trägt, ist ein 1:1-Kontraktspread nicht marktneutral, sondern eine versteckte Richtungswette; dollarneutrale Gewichtung liefert ein niedrigeres Spread-Beta und damit sauberere Mean Reversion. | Residual-Beta des Spreads gegen ES bei 1:1 vs. dollarneutral; Edge beider Varianten | Dollarneutral senkt das Residual-Beta nicht oder verschlechtert die Edge | 🟢 | 🔧 Kontraktmultiplikator-Gewichtung | 2 |
| SK-04 | Weil die Beziehung der Indizes außerhalb der RTH von anderen Akteuren getragen wird, ist ein nur aus RTH-Daten geschätztes Beta für Intraday-Handel treffsicherer als eines aus der 24h-Serie. | Beta-Schätzung aus RTH-only vs. 24h; Vorhersagefehler des Spreads am Folgetag, dann Edge | Kein Unterschied im Vorhersagefehler | 🟢 | 🔧 RTH-Maske in der Beta-Schätzung | 2 |
| SK-05 | Weil laut Avellaneda/Lee der handelbare Teil das Residuum nach Abzug des gemeinsamen Faktors ist, liefert eine PCA über alle vier Indizes (PC1 gleich Markt) ein besseres Signal als jeder paarweise Spread: das Residuum eines Index gegen PC1 ist der eigentliche Kandidat. | PCA auf rollendem Fenster über die 4 Return-Serien; s-Score des Residuums je Index; Edge gegen die beste paarweise Variante | Residual-Signal schlägt den besten paarweisen Spread nicht | 🟢 | 🔧 PCA-Modul über 4 Serien plus s-Score | 1 |
| SK-06 | Weil Avellaneda/Lee ihre Schwellen (Öffnen bei s-Score-Betrag über 1,25, Schließen nahe 0,5) aus einem Tagesmodell gewinnen, sind genau diese Werte für Intraday zu eng und müssen mit der schlechteren Signal-Rausch-Rate nach oben skalieren. | Schwellen-Sweep um die Literaturwerte (s-Score-Betrag von 0,75 bis 3,0), Optimum je Zeitskala, Vergleich mit dem Literaturwert | Optimum liegt bei den Literaturwerten (dann ist die Skalierungs-Hypothese falsch, aber die Schwelle ist geschenkt) | 🟢 | 🔧 s-Score-Schwellen (mit SK-05) | 1 |
| SK-07 | Weil sich Indexzusammensetzung und Sektorgewichte langsam ändern, ist die Frequenz der Beta-Neuschätzung eine eigene Stellschraube: tägliche Neuschätzung schlägt wöchentliche, und beide schlagen ein statisches Beta. | Edge bei Beta-Update täglich / wöchentlich / monatlich / statisch, sonst identisch | Kein monotoner Zusammenhang oder statisch ist genauso gut (dann ist der Aufwand nicht gerechtfertigt) | 🟢 | 🔧 Beta-Update-Frequenz als Parameter | 2 |
| SK-08 | Weil die Spread-Volatilität selbst eine U-Form über den Tag hat, ist ein z-Score gegen die unbedingte Vola zur Eröffnung systematisch zu klein und mittags systematisch zu groß; die Normierung muss gegen die Vola derselben Tageszeit laufen. | z-Score gegen unbedingte Vola vs. gegen uhrzeitbedingte Vola (Median derselben Minute, 20 Vortage); Verteilung der Signalzeiten und Edge | Signalverteilung ändert sich nicht oder Edge bleibt gleich | 🟢 | 🔧 uhrzeitbedingte Vola-Normierung | 2 |
| SK-09 | Weil ein Korb weniger idiosynkratisches Rauschen enthält als ein einzelner Gegenpart, hat ein 3-Bein-Spread (NQ gegen eine Mischung aus ES und RTY) eine niedrigere Residual-Varianz als jeder 2-Bein-Spread; die Frage ist nur, ob das die dritte Kostenschicht schlägt. | Residual-Varianz 2-Bein vs. 3-Bein; danach Netto-Edge nach dreifacher Kostenlast | Varianzreduktion kleiner als der Kostenaufschlag (dann sind 3 Beine bei uns strukturell tot) | 🟢 | 🔧 Multi-Leg-Ausführung in `rv.py` | 3 |
| SK-10 | Weil `rv.py` den Spread heute im Return-Raum seit Entry rechnet, wird der Anker mit jedem Trade neu gesetzt; ein Spread mit festem Session-Anker (Return seit Open statt seit Entry) ist über den Tag konsistent und liefert vergleichbare Signale. | Beide Anker-Definitionen bei identischer Regel; Stabilität der optimalen Schwelle über Tageszeiten | Session-Anker liefert keine stabilere Schwelle | 🟢 | 🔧 Anker-Option in `rv.py` | 2 |
| SK-11 | Weil in den Quartals-Roll-Wochen Kalender-Spread-Quotes in die Continuous-Serien lecken (bei uns nachgewiesen, #075), sind alle Beta- und Korrelations-Schätzungen aus Roll-Wochen verzerrt; deren Ausschluss aus der Schätzung, nicht nur aus dem Handel, hebt die Edge messbar. | Beta und Korrelation mit und ohne Roll-Wochen im Schätzfenster; Edge beider Varianten; Anteil der Trades in Roll-Wochen | Ausschluss ändert Beta um weniger als 2 Prozent und die Edge nicht | 🟢 | 🔧 Roll-Kalender-Maske in der Schätzung | 2 |

---

## Block ZF — Zeitfenster & Intraday-Saisonalität der Paar-Beziehung (12)

**Forschungsbasis:** Epps-Literatur (arXiv 0704.3798, physics/0701110, arXiv 2011.11281) — gemessene Korrelationen **sinken mit steigender Abtastfrequenz**; Ursachen sind Asynchronität der Preisbeobachtungen und die Lead-Lag-Beziehung selbst. Heston/Korajczyk/Sadka (Journal of Finance 2010, SSRN 1107590) — Return-Kontinuation an exakten Halbstunden-Vielfachen, am stärksten in erster und letzter Halbstunde, und **explizit nicht auf einen Wochentag konzentriert** (im [[Research-Cache]] als Negativbefund für Wochentagsfilter hinterlegt).
**Warum das für Paare besonders zählt:** Ein Paar-Signal ist eine Differenz zweier Serien. Alles, was die beiden Serien unterschiedlich schnell macht (Eröffnungsauktion, Europa-Schluss, dünner Mittag, Settlement), erzeugt eine **scheinbare** Divergenz ohne Information. Diese Zeilen trennen scheinbare von echter Divergenz.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| ZF-01 | Weil Volumen und Vola eine U-Form über den Tag haben, hat auch die Spread-Vola eine U-Form: derselbe z-Score bedeutet mittags einen viel kleineren Dollar-Betrag als zur Eröffnung, weshalb eine über den Tag konstante Schwelle systematisch falsche Trades erzeugt. | Spread-Vola je 30-Min-Fenster über 10 Jahre; Dollar-Wert eines 2-Sigma-Moves je Fenster gegen die Round-Trip-Kosten | Spread-Vola ist über den Tag flach (dann ist die konstante Schwelle korrekt) | 🟢 | 🔧 Diagnostik-Skript | 2 |
| ZF-02 | Weil laut Epps-Literatur Korrelation Zeit zum Entstehen braucht und Asynchronität sie zerstört, ist die gemessene Paar-Korrelation direkt nach dem Open am niedrigsten und steigt über den Tag; eine Divergenz um 09:35 ist deshalb überwiegend Messartefakt, keine handelbare Abweichung. | Rollende 30-min-Korrelation je Tageszeit, gemittelt über 10 Jahre; Anteil der Divergenzsignale je Fenster, das ohne Konvergenz endet | Korrelation ist über den Tag flach oder frühe Signale sind nicht schlechter | 🟢 | 🔧 Korrelations-Tagesprofil | 2 |
| ZF-03 | Weil Heston et al. Return-Kontinuation an exakten Halbstunden-Vielfachen finden, überträgt sich dieses Muster auf die **relative** Performance: der Index, der in einer Halbstunde vorn lag, liegt in derselben Halbstunde des Folgetags überproportional wieder vorn. | Rang je Halbstundenslot heute gegen denselben Slot morgen, über 10 Jahre, mit Zufallserwartung als Basis | Kein Zusammenhang oder nur an einzelnen Slots ohne Muster über die Slots hinweg | 🟢 | 🔧 Slot-Rang-Persistenz-Statistik | 1 |
| ZF-04 | Weil um 11:30 ET die europäischen Kassamärkte schließen und dort gebundene Hedges aufgelöst werden, ist das der Zeitpunkt, an dem vormittags aufgebaute Divergenzen entweder auflösen oder sich verfestigen: Divergenzen vor 11:30 konvergieren, danach entstandene nicht. | Konvergenzrate von Divergenzen nach Entstehungszeit (vor/nach 11:30), Restweg bis Close | Kein Bruch um 11:30 oder Bruch liegt an einer anderen Uhrzeit (dann Uhrzeit korrigieren, Hypothese neu) | 🟢 | ✅ `div_fade` + Zeitfenster-Split | 2 |
| ZF-05 | Weil in der letzten Stunde Index-Rebalancing und MOC-Flows instrumentspezifisch wirken, ist eine dort entstehende Relative-Stärke-Divergenz **echt** (Umschichtung) und läuft bis Close weiter, statt zu konvergieren. | Konvergenz vs. Fortsetzung von Divergenzen, die nach 15:00 entstehen, gemessen bis 16:00 | Späte Divergenzen konvergieren genauso wie frühe | 🟢 | ✅ `div_mom` + Zeitfenster | 1 |
| ZF-06 | Weil die Übernacht-Session von anderen Akteuren getragen wird, aber dieselbe Information verarbeitet, sagt die **Rangfolge der vier Indizes in der Asien- bzw. Europa-Session die Rangfolge der RTH voraus** — nutzbar als Vorfilter, ohne selbst über Nacht zu halten. | Rang der 4 Indizes im Fenster 02:00-08:00 ET gegen Rang 09:30-16:00, Übergangsmatrix über 10 Jahre | Kein Zusammenhang über der Zufallserwartung | 🟢 | 🔧 Overnight-Fenster-Ranking (Daten liegen vor, RTH-Maske umkehren) | 1 |
| ZF-07 | Weil die vier Kontrakte nicht exakt synchron eröffnen und die erste Minute Auktionsartefakte enthält, ist das Fenster 09:30-09:35 für Paar-Signale reines Rauschen: der Ausschluss dieser Minuten hebt die Edge **aller** Paar-Strategien gleichzeitig. | Identische Regeln mit und ohne Ausschluss der ersten 5 Minuten, über mehrere Modi hinweg | Ausschluss verbessert nichts oder verschlechtert (dann steckt echte Information in diesen Minuten) | 🟢 | ✅ Startzeit-Parameter | 1/2 |
| ZF-08 | **Kontrollhypothese:** Wenn ein gefundener Uhrzeit-Effekt an der Börsenuhr hängt (echter Akteur), muss er die Sommerzeit-Umstellung unbeschadet überstehen; wandert er dagegen mit der Kalenderuhr, ist er ein Datenartefakt. | Jeden gefundenen ZF-Effekt getrennt für Sommer- und Winterzeit prüfen, in ET und in UTC | Effekt hängt an UTC statt an ET (dann ist die zugehörige Zeile tot) | 🟢 | 🔧 DST-Split in der Auswertung | 1/2 |
| ZF-09 | Weil im Mittagsfenster die Bücher dünn sind, ist eine dort auftretende Spread-Ausweitung mechanisch (Liquiditätsmangel) und nicht informationsgetrieben, weshalb sie mit höherer Rate zurückläuft als eine gleich große Ausweitung am Vormittag. | Konvergenzrate gleich großer Spread-Ausweitungen, getrennt nach Fenster, kontrolliert auf die Größe | Konvergenzrate im Mittag nicht höher | 🟢 | ✅ `div_fade` + Fenster + Größenkontrolle | 2 |
| ZF-10 | Weil die Kontrakte unterschiedliche Settlement-Mechaniken und Schlusszeiten haben, entstehen in den letzten Minuten systematische Scheindivergenzen; ein Exit-Cutoff einige Minuten vor Close verbessert jede Paar-Strategie, ohne Edge zu kosten. | Edge bei Exit-Cutoff 16:00 / 15:55 / 15:50 / 15:45, Anteil der Trades, die davon betroffen sind | Früherer Cutoff kostet mehr Edge als er an Artefakten spart | 🟢 | ✅ Exit-Zeit-Parameter | 1/2 |
| ZF-11 | **Kontrollhypothese gegen Overfitting:** Weil Heston et al. den Wochentag als Erklärung für das verwandte Halbstundenmuster explizit getestet und verworfen haben, darf auch bei uns kein Paar-Effekt auf einen einzelnen Wochentag konzentriert sein; passiert das doch, ist es Multiple Testing und kein Mechanismus. | Jeden Fund zusätzlich nach Wochentag aufschlüsseln; prüfen, ob die Edge auf ein bis zwei Tagen konzentriert ist | Edge konzentriert sich auf einzelne Wochentage (dann ist der Fund verdächtig, nicht bestätigt) | 🟢 | 🔧 Wochentags-Aufschlüsselung in der Auswertung | 1/2 |
| ZF-12 | Weil ein Zeit-Exit vor Close jede Position hart abschneidet, sind spät eröffnete Trades systematisch benachteiligt: Es existiert eine **letzte sinnvolle Entry-Zeit**, ab der die verbleibende Sessionzeit kleiner ist als die typische Haltedauer bis Ziel. | Verteilung der Haltedauer bis Ziel bei erfolgreichen Trades; Edge je Entry-Uhrzeit; Schnittpunkt bestimmen | Edge ist über die Entry-Uhrzeit flach (dann ist die Haltedauer kurz genug, dass es egal ist) | 🟢 | ✅ Entry-Cutoff-Parameter | 1/2 |

---

## Block RG — Regime-Filter (13)

**Forschungsbasis:** Hasbrouck — die Preisfindungs-Dominanz des E-mini ist regimeabhängig (Hochvola vs. Normal). Barbon/Buraschi („Gamma Fragility", SSRN 3725454, im [[Research-Cache]]) — Dealer-Gamma-Imbalance sagt Intraday-Vola, Spreads und **Autokorrelation** auf 5- bis 60-Minuten-Frequenzen voraus; negative Imbalance bedeutet höhere Spreads und mehr Fortsetzung, positive bedeutet Kompression. Pitkäjärvi/Suominen/Vaittinen (JFE 2019, im Cache) — Bond-Renditen sagen Equity-Renditen voraus. Krauss sowie Do/Faff — die Rendite der Familie ist über die Zeit gefallen, Zeit ist also selbst ein Regime.
**Warum das nach LL der wichtigste Block ist:** Relative Value lebt davon, dass zwei Instrumente sich unterschiedlich verhalten. Genau das ist regimeabhängig: bei Korrelation nahe 1 gibt es nichts zu handeln, bei gebrochener Beziehung nichts zurückzuholen. Das Fenster dazwischen ist die eigentliche Edge-Quelle.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| RG-01 | Weil bei Korrelation nahe 1 keine handelbare Divergenz entsteht und bei gebrochener Beziehung keine Konvergenz mehr folgt, existiert die Edge nur in einem mittleren Korrelationsband (etwa 0,75 bis 0,93) und verschwindet an beiden Rändern: umgekehrtes U, kein monotoner Zusammenhang. | Edge je Quintil der rollenden 20-Tage-Paar-Korrelation, Vorzeichen und Trade-Zahl je Quintil, IS und OOS getrennt | Edge steigt oder fällt monoton mit der Korrelation (dann kein Bandeffekt) | 🟢 | 🔧 rollende Korrelation als Regime-Label | 1/2 |
| RG-02 | Weil laut Hasbrouck die Futures gerade in Hochvola-Phasen die Preisfindung dominieren, ist Lead-Lag ein Hochvola-Phänomen und Spread-Fade ein Niedrigvola-Phänomen: das VIX-Terzil schaltet zwischen den beiden Familien um. | Edge von `leadlag` und `div_fade` je VIX-Terzil (Vortagesschluss, kein Look-ahead), Kreuzungspunkt suchen | Beide Familien reagieren gleich auf VIX oder gar nicht | 🟡 | ✅ beide Modi plus VIX-Gate | 1/2 |
| RG-03 | Weil ein VIX-Sprung (Tagesänderung über 15 Prozent) Korrelationen gegen 1 treibt, stirbt an solchen Tagen jede Relative-Value-Edge, während Richtungsstrategien weiterlaufen: der Filter ist ein reines Veto, kein Signal. | Edge an Tagen mit VIX-Sprung gegen Basisrate, zusätzlich realisierte Paar-Korrelation an diesen Tagen | Sprungtage sind nicht schlechter als normale Tage | 🟡 | ✅ VIX-Änderungs-Gate | 1/2 |
| RG-04 | Weil negative Dealer-Gamma-Imbalance laut Barbon/Buraschi mit höherer Intraday-Autokorrelation einhergeht, ist der Lead-Lag-Effekt (Fortsetzung im Laggard) in negativen Gamma-Regimen deutlich stärker als in positiven. | Edge von `leadlag` je Terzil des Gamma-Proxys aus `DIX_GEX_daily.csv` (Vortageswert), mit Trade-Zahl je Terzil | Kein monotoner Zusammenhang oder Vorzeichen dreht im OOS | 🟡 | ✅ `leadlag` plus GEX-Gate | 1 |
| RG-05 | Weil positive Gamma-Imbalance laut derselben Quelle Range-Kompression und niedrigere Vola bedeutet, ist genau dieses Regime das einzige, in dem Spread-Mean-Reversion zuverlässig zum Ziel kommt, statt ausgestoppt zu werden. | Edge von `div_fade` je GEX-Terzil, zusätzlich Anteil der Trades, die das Ziel erreichen, je Terzil | Zielerreichungsquote ist über die Terzile flach | 🟡 | ✅ `div_fade` plus GEX-Gate | 2 |
| RG-06 | Weil Small Caps zinssensitiv verschuldet und Tech-Werte lange Duration sind, verschiebt die Steilheit der Zinskurve (DGS10 minus DGS2) die relative Führung zwischen RTY und NQ systematisch. | Relative Tagesperformance RTY gegen NQ je Terzil der Kurvensteilheit (Vortageswert), 10 Jahre | Kein Zusammenhang oder Vorzeichen instabil zwischen erster und zweiter Sample-Hälfte | 🟡 | 🔧 Zinskurven-Feature aus DGS2/DGS10 | 1 |
| RG-07 | Weil Tech-Bewertungen über den Diskontsatz an langen Zinsen hängen, sagt die Tagesänderung der 10-Jahres-Rendite die relative Performance NQ gegen RTY voraus: steigende Renditen begünstigen RTY relativ, fallende NQ. | Regression der relativen Tagesperformance auf die Vortagesänderung von DGS10, danach Edge einer darauf gebauten Intraday-Regel | Vorzeichen nicht stabil oder Effekt verschwindet nach Kontrolle auf die Marktrichtung | 🟡 | 🔧 Zins-Feature als Tagesfilter | 1 |
| RG-08 | Weil RTY-Unternehmen überwiegend im Inland verdienen und ES/NQ-Unternehmen international, begünstigt ein stärkerer Dollar (DTWEXBGS) RTY relativ zu ES und NQ. | Relative Tagesperformance je Terzil der Dollar-Tagesänderung (Vortageswert), 10 Jahre, IS/OOS getrennt | Kein Zusammenhang oder Effekt kleiner als die Kosten einer darauf gebauten Regel | 🟡 | 🔧 DXY-Feature als Tagesfilter | 1 |
| RG-09 | **Kontrollhypothese gegen die Literatur:** Weil die Pairs-Trading-Rendite laut Krauss von 15,6 Prozent vor 2000 auf 6,4 Prozent nach 2010 gefallen ist und Do/Faff das auf Crowding zurückführen, muss auch bei uns jede gefundene Edge über die Zeit abnehmen; tut sie das nicht, ist der Fund verdächtig statt beruhigend. | Jeden Fund in Jahresscheiben zerlegen, Trend der jährlichen Edge, zusätzlich 2016-2019 gegen 2022-2026 | Edge über die Jahre konstant oder steigend (dann besonders kritisch gegenlesen, nicht feiern) | 🟢 | 🔧 Jahresscheiben in der Auswertung | 1/2 |
| RG-10 | Weil in Stressphasen alles gemeinsam fällt, kollabiert die Querschnitts-Dispersion der vier Indizes an genau den Tagen, an denen die Vola am höchsten ist: hohe Vola und hohe Dispersion sind nicht dasselbe Regime, und Relative Value braucht das zweite, nicht das erste. | Korrelation zwischen Tagesvola und Querschnitts-Dispersion; Edge in der Zelle hohe Vola/niedrige Dispersion gegen hohe Dispersion/niedrige Vola | Beide Größen austauschbar (Korrelation über 0,8), dann ist die Trennung wertlos | 🟢 | 🔧 Zwei-Faktor-Regime-Label | 1/2 |
| RG-11 | Weil in einem trendenden Markt jede Divergenz vom Trend mitgezogen wird, funktioniert Spread-Fade nur in seitwärts laufenden Sessions: das Regime-Label ist die Trendstärke des Referenzindex (ES), nicht die Vola. | Edge je Terzil der ES-Trendstärke am Signaltag (Betrag des Returns seit Open geteilt durch die Tagesrange bis dahin) | Kein Zusammenhang oder Trendstärke ist nur ein Vola-Proxy (Korrelation über 0,8) | 🟢 | 🔧 Trendstärke-Feature | 2 |
| RG-12 | Weil ein Regime nur nützt, wenn es morgen noch gilt, muss jedes Regime-Label eine messbare Persistenz über mindestens einen Tag haben; Labels, die täglich neu würfeln, sind im Live-Betrieb wertlos, auch wenn sie im Backtest trennen. | Übergangswahrscheinlichkeit jedes Regime-Labels (Tag t nach Tag t plus 1) gegen die Zufallserwartung | Persistenz nicht über der Zufallserwartung (dann fliegt das Label aus allen abhängigen Zeilen) | 🟢 | 🔧 Persistenzprüfung je Label | 1/2 |
| RG-13 | Weil alle unsere Regime-Quellen nur als Tagesdaten vorliegen, muss jedes Regime-Gate den Vortageswert verwenden; ein Test, der den Tageswert desselben Tages benutzt, hat Look-ahead und ist automatisch ungültig. | Jede RG-Zeile zusätzlich mit Same-Day-Wert rechnen und die Differenz ausweisen; die Differenz misst den Look-ahead-Vorteil | Same-Day-Variante deutlich besser (dann ist das Regime nur ein verstecktes Zukunftssignal) | 🟡 | 🔧 Lag-Kontrolle in allen Regime-Gates | 1/2 |

---

## Block EV — Event- und Kalender-Konditionierung (9)

**Forschungsbasis:** Die FOMC-Mikrostrukturliteratur (u.a. arXiv 1707.02419 zur Spot-Kovariation) zeigt: rund eine Stunde vor planmäßigen FOMC-Ankündigungen steigen die Spot-Kovarianzen deutlich, während die Volatilitäten nur mäßig zunehmen — die **Korrelationen springen also hoch**. Für Relative Value ist das die denkbar schlechteste Umgebung: alles bewegt sich gemeinsam, es gibt keine Divergenz zu handeln. Dazu Pre-FOMC-Drift (NY Fed Staff Reports) und BIS WP 1079 zur Volumendynamik um FOMC.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| EV-01 | Weil die Korrelationen laut Mikrostrukturliteratur bereits rund eine Stunde vor der FOMC-Entscheidung hochspringen, ist das Fenster 13:00-14:00 an FOMC-Tagen für jede Relative-Value-Strategie strukturell tot; ein Veto dort hebt die Edge, ohne nennenswert Trades zu kosten. | Realisierte Paar-Korrelation im Fenster an FOMC-Tagen gegen normale Tage; Edge mit und ohne Veto | Korrelation springt bei uns nicht oder das Veto ändert die Edge nicht | 🟡 | 🔧 FOMC-Kalender als Flag | 1/2 |
| EV-02 | Weil nach der Entscheidung die Zinssensitivitäten der Indizes auseinanderlaufen (RTY verschuldet, NQ lange Duration), ist das Fenster 14:00-15:00 an FOMC-Tagen umgekehrt das beste Dispersions-Fenster des Quartals und trägt Relative-Stärke-Momentum. | Querschnitts-Dispersion und Edge einer RS-Momentum-Regel im Fenster an FOMC-Tagen gegen normale Tage | Dispersion dort nicht erhöht oder Edge nicht über der Basisrate | 🟡 | 🔧 FOMC-Flag plus RS-Modul | 1 |
| EV-03 | Weil CPI- und NFP-Zahlen um 08:30 ET erscheinen und die Indizes je nach Zinsbezug unterschiedlich stark reagieren, ist eine bei Open bestehende Divergenz an diesen Tagen echte Neubewertung und darf nicht gefadet werden. | Konvergenzrate der Open-Divergenz an Datentagen gegen normale Tage | Kein Unterschied zwischen Datentagen und normalen Tagen | 🟡 | 🔧 Makro-Kalender als Flag | 2 |
| EV-04 | Weil Optionsverfall die Indizes unterschiedlich stark pinnt (SPX-Optionsvolumen ist um Größenordnungen höher als RUT-Optionsvolumen), ist an OpEx-Tagen ES relativ zu RTY künstlich ruhig, was eine mechanische und handelbare Divergenz erzeugt. | Verhältnis der realisierten Vola ES zu RTY an OpEx-Tagen gegen normale Tage; Edge einer darauf gebauten Regel | Vola-Verhältnis unterscheidet sich nicht oder die Divergenz ist zu klein für die Kosten | 🟡 | 🔧 OpEx-Kalender-Flag | 1/2 |
| EV-05 | Weil in der Quartals-Roll-Woche die Continuous-Serien nachweislich verunreinigt sind (#075) und zusätzlich echte Roll-Flows laufen, sind Paar-Signale dort systematisch unzuverlässig; der Ausschluss der Roll-Woche hebt die Edge und senkt die Tail-Verluste. | Edge und Verlust-Tails mit und ohne Roll-Woche; Anteil der größten 5 Verluste, die in Roll-Wochen liegen | Roll-Wochen sind nicht auffällig (dann reicht der Guard aus #075) | 🟢 | ✅ Kalender-Maske | 1/2 |
| EV-06 | Weil Monatsende-Rebalancing zwischen Anlageklassen und Indizes umschichtet, entsteht an den letzten zwei Handelstagen des Monats eine gerichtete Relative-Stärke-Verschiebung, die groß genug ist, um die Kosten zu tragen. | Relative Performance der 4 Indizes an T-2 und T-1 des Monats gegen den Monatsdurchschnitt, 10 Jahre, mit Trade-Zahl | Effekt kleiner als die Kosten oder nur in einzelnen Jahren vorhanden | 🟢 | 🔧 Monatsende-Offset-Flag | 1 |
| EV-07 | Weil Quartalsende zusätzlich Fonds-Reporting und größere Umschichtungen bringt, ist der Monatsende-Effekt am Quartalsende deutlich stärker als an gewöhnlichen Monatsenden. | Monatsende-Effekt getrennt für Quartals- und Nicht-Quartalsmonate | Kein Unterschied (dann reicht EV-06 und diese Zeile entfällt) | 🟢 | 🔧 Quartalsende-Flag | 1 |
| EV-08 | Weil an Halbtagen vor Feiertagen die Bücher dünn und die Schlusszeiten verschoben sind, produzieren Paar-Signale dort überwiegend Scheindivergenzen; ein pauschales Veto an Halbtagen kostet fast keine Trades und entfernt Ausreißerverluste. | Anteil der Halbtage an den größten Verlusten; Edge mit und ohne Halbtags-Veto | Halbtage sind bei den Verlusten nicht überrepräsentiert | 🟢 | 🔧 Halbtags-Kalender (aus Session-Länge ableitbar) | 1/2 |
| EV-09 | Weil Mega-Cap-Quartalszahlen NQ viel stärker bewegen als RTY, ist die relative Vola NQ zu RTY in den Kernwochen der Berichtssaison systematisch erhöht, was die optimale Spread-Schwelle saisonal verschiebt. | Verhältnis realisierter Vola NQ zu RTY nach Kalenderwoche relativ zum Berichtszyklus, 10 Jahre | Kein saisonales Muster erkennbar | 🟡 | 🔧 Näherung über Kalenderwochen, echter Earnings-Kalender fehlt | 1/2 |

---

## Block MS — Mikrostruktur-Proxies ohne Orderbuch (7)

**Forschungsbasis:** Epps-Literatur — die gemessene Korrelation sinkt mit der Abtastfrequenz, Hauptursache ist **Asynchronität der Preisbeobachtungen**, zweite Ursache die Lead-Lag-Beziehung selbst; Korrekturansätze sind Hayashi/Yoshida und der Fourier-Schätzer von Malliavin/Mancino. Cont/Cucuringu/Zhang (QF 2023) — die **gleichzeitige** Cross-Impact-Komponente enthält den Großteil der Information, die verzögerte trägt nur über sehr kurze Horizonte zusätzlich bei.
**Unsere Einschränkung, ehrlich benannt:** Wir haben kein Orderbuch, keine Ticks, kein Trade-Delta. Alles hier sind Proxies aus 1m-OHLCV. Das reicht für Datenqualitäts- und Asynchronitäts-Fragen, nicht für echte Mikrostruktur.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| MS-01 | Weil ein Teil jeder auf 1-Minuten-Daten gemessenen Divergenz laut Epps-Literatur reines Asynchronitäts-Artefakt ist, verschwindet ein Teil der Signale bei 5-Minuten-Abtastung; wer nur auf 1m misst, handelt teilweise Messrauschen. | Signalzahl und Edge bei Abtastung 1 / 2 / 5 / 15 min bei sonst identischer Regel; Anteil der Signale, die bei 5m verschwinden | Signalzahl und Edge sind über die Frequenzen stabil (dann ist Asynchronität bei uns kein Problem) | 🟢 | 🔧 Resampling-Parameter | 2 |
| MS-02 | Weil ein Instrument nur dann sauber führen kann, wenn dort auch gehandelt wird, ist das Volumenverhältnis der beiden Beine im Trigger-Fenster ein Gültigkeits-Filter: Signale, bei denen der Leader relativ dünn gehandelt wurde, tragen keine Information. | Edge je Terzil des Volumenverhältnisses Leader zu Laggard im Trigger-Fenster | Kein Zusammenhang zwischen Volumenverhältnis und Edge | 🟢 | 🔧 Volumenverhältnis-Feature | 1 |
| MS-03 | Weil eine Divergenz im illiquideren Instrument eher Preis-Impact als Information ist, ist ein Amihud-Proxy (Betrag des Returns geteilt durch Volumen) je Bein der bessere Gültigkeits-Filter als das Volumen allein. | Edge je Terzil des Amihud-Proxys des divergierenden Beins; Vergleich gegen den reinen Volumenfilter aus MS-02 | Amihud-Proxy trennt nicht besser als das Volumen | 🟢 | 🔧 Amihud-Proxy je Bar und Symbol | 1/2 |
| MS-04 | Weil eine Bewegung mit viel Volumen und wenig Range Absorption ist und eine mit wenig Volumen und viel Range ein Liquiditätsloch, trennt das Range-zu-Volumen-Verhältnis des Leaders echte Information von einem Ausrutscher im dünnen Buch. | Edge je Terzil des Range-zu-Volumen-Verhältnisses der Trigger-Bars des Leaders | Kein Zusammenhang oder der Proxy ist nur ein Vola-Proxy (Korrelation über 0,8 mit ATR) | 🟢 | 🔧 Range/Volumen je Bar | 1 |
| MS-05 | Weil eine Serie mit vielen Null-Return-Minuten schlicht nicht gehandelt wurde, ist eine gegen eine solche Serie gemessene Divergenz eine Scheindivergenz (Stale Price); ein Staleness-Gate entfernt genau diese Fehlsignale. | Anteil Null-Return-Minuten je Bein im Messfenster; Edge mit und ohne Gate; zusätzlich Verteilung über die Tageszeit | Staleness kommt in RTH praktisch nicht vor (dann Gate unnötig, aber Frage geklärt) | 🟢 | 🔧 Staleness-Zähler je Fenster | 1/2 |
| MS-06 | Weil fehlende Bars in einer der beiden Serien eine Divergenz erzeugen, die es nie gab, muss jedes Paar-Signal an eine **Vollständigkeitsprüfung beider Serien** im Messfenster gebunden sein; ohne diese Prüfung sind Datenlücken als Edge fehlinterpretierbar. | Zahl der Signale, bei denen eine der beiden Serien im Messfenster unvollständig ist; Edge dieser Teilmenge gegen den Rest | Unvollständige Fenster sind nicht überrepräsentiert und nicht auffällig | 🟢 | 🔧 Bar-Vollständigkeitsprüfung (ergänzt `_drop_corrupt_sessions`) | 1/2 |
| MS-07 | Weil laut Cont et al. die gleichzeitige Cross-Impact-Komponente den Großteil der Information trägt, ist ein rein **gleichzeitiges** Divergenzmaß (beide Beine in derselben Minute) dem verzögerten überlegen, und der verzögerte Anteil trägt nur in den ersten Minuten zusätzlich bei. | Edge eines gleichzeitigen Divergenzmaßes gegen ein verzögertes (1-5 min Versatz), beide bei identischem Exit | Verzögertes Maß ist deutlich besser (dann ist es Diffusion und Block LL ist der richtige Rahmen, nicht MS) | 🟢 | 🔧 Versatz-Parameter im Divergenzmaß | 1/2 |

---

## Block KX — Käfig-, Exit- und Buchbeitrags-Mechanik (6)

**Forschungsbasis:** Leung/Li (arXiv 1411.5062) lösen Entry, Take-Profit und Stop-Loss **gemeinsam** unter Transaktionskosten; die Eintrittsregion liegt strikt über dem Stop-Loss, und Stop und Ziel sind gekoppelt. Das ist die einzige Stelle der Pairs-Literatur, die direkt auf unsere Käfig-Frage einzahlt, weil bei uns der Trailing-DD ein zweiter, äußerer Stop ist.
**Unsere Messlatte:** Nicht Edge, sondern **Passquote je Eval und Kosten pro funded Konto** (#106), auf ehrlicher Basis (Intraday-Bust, Min-Size, Block-Bootstrap, Marginal-Test Buch plus 1 nur OOS).

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| KX-01 | Weil ein marktneutraler Spread eine deutlich kleinere Tagesvarianz hat als ein Richtungsbein, verbraucht er unter Trailing-DD weniger Cushion pro Tag; ein RV-Bein kann deshalb die Passquote heben, obwohl sein Solo-expR unter dem der Buch-Beine liegt. | Marginal-Test Buch plus 1, nur OOS, `dd_mode="intraday"`, Min-Size, 5 Seeds; Delta P(funded) gegen die Tagesvarianz des Beins | Delta liegt unter 1,5 pp oder unter dem doppelten Seed-Rauschen (dann neutral, kein Buchbeitrag) | 🟢 | ✅ `funded_finalize.py --next` plus Marginal-Test | 1/2 |
| KX-02 | **Gegenhypothese zu KX-01, muss mitgetestet werden:** Weil bei Min-Size „Bein dazu" gleichbedeutend mit „mehr Position" ist (Lehre 82, #123), hilft ein RV-Bein nur, wenn sein Verhältnis von Drift zu Risiko über dem des Buchs liegt; niedrige Varianz allein reicht nicht. | Drift-zu-Risiko-Verhältnis des Kandidaten gegen das des Buchs, vor dem Marginal-Test berechnet als billiger Vorfilter | Verhältnis liegt unter dem des Buchs (dann Marginal-Test gar nicht erst starten) | 🟢 | 🔧 Vorfilter-Kennzahl vor dem Marginal-Test | 1/2 |
| KX-03 | Weil der Zeit-Exit vor Close ein harter äußerer Stop ist, wird ein Teil der Konvergenz systematisch abgeschnitten; die Größe dieses Abschnitts ist messbar und entscheidet, ob Intraday-Pairs bei uns überhaupt sinnvoll sein kann. | Für jeden Trade zusätzlich den hypothetischen Ausgang bei Halten bis zum Folgetag rechnen (nur als Messgröße, nicht handelbar); Differenz ist die Käfig-Steuer | Käfig-Steuer frisst über die Hälfte der Brutto-Edge (dann ist die Familie im Prop-Käfig strukturell benachteiligt und gehört ins [[Live-Account]]) | 🟢 | 🔧 Schatten-Auswertung ohne Zeit-Exit | 1/2 |
| KX-04 | Weil der Stop bei einer Paar-Strategie sinnvollerweise in Spread-Einheiten liegt, der Käfig aber in Dollar auf dem Konto rechnet, ist ein in Spread-Sigma definierter Stop dem in Instrument-ATR definierten überlegen, obwohl nur der zweite direkt zum Käfig passt. | Beide Stop-Definitionen bei identischem Entry und Ziel; Edge, Zielerreichungsquote und maximaler Tagesverlust je Variante | Spread-Sigma-Stop erzeugt größere Tagesverluste (dann gewinnt die Käfig-Kompatibilität) | 🟢 | 🔧 Stop-Definition als Option | 2 |
| KX-05 | Weil ein marktneutrales Bein per Konstruktion wenig mit den bestehenden Richtungs-Beinen gemein hat, ist seine Korrelation zum Buch nahe null — aber das ist eine Behauptung, keine Messung, und muss vor jedem Buchbeitrags-Argument belegt werden. | Korrelation der Tages-P&L des Kandidaten mit der Tages-P&L jedes Buch-Beins und des Gesamtbuchs, mit Bootstrap-CI | Korrelation liegt betragsmäßig über 0,3 (dann ist das Diversifikations-Argument hinfällig) | 🟢 | ✅ vorhandene Korrelationsauswertung | 1/2 |
| KX-06 | Weil unter Trailing-DD nicht die Höhe des Erwartungswerts zählt, sondern die Wahrscheinlichkeit, die Barriere zu berühren, schlägt ein Profil mit hoher Trefferquote und kleinen Gewinnen bei gleichem expR ein Profil mit wenigen großen Gewinnern — RV-Profile sind ersteres und passen dadurch besser in den Käfig als die ORB-Beine. | First-Passage-Rechnung mit gleichem expR aber unterschiedlichem Trefferquoten-/R-Profil, gegen die tatsächlichen Profile von Kandidat und Buch-Beinen | Passquote hängt bei gleichem expR nicht vom Profil ab (dann ist die Trefferquote irrelevant und nur expR zählt) | 🟢 | ✅ `eval_plan.evaluate_v2` plus Profil-Variation | 1/2 |

---

## Block KO — Kosten, Ausführung und Nullkontrollen (4)

**Warum dieser Block ganz zum Schluss steht und trotzdem zuerst gerechnet werden sollte:** Bei Index-Futures, die zu über 90 Prozent korrelieren, ist die Kostenfrage nicht ein Detail der Umsetzung, sondern **der Mechanismus, an dem die Familie bei uns bereits einmal komplett gestorben ist** (48 von 48 `div_fade`-Varianten, #033). Jede Zeile aus SM, SK und MS ist wertlos, solange KO-01 und KO-02 nicht beantwortet sind.

| ID | Hypothese | Prüfbar | Verwerfen wenn | Daten | Engine | Beine |
|---|---|---|---|---|---|---|
| KO-01 | Weil ein Spread beide Beine bezahlt, trägt eine 2-Bein-Strategie den vierfachen Kosten-Drag einer 1-Bein-Strategie (zwei Beine mal Ein- und Ausstieg); jeder Kandidat muss deshalb den 2-Tick-Stresstest **je Bein** bestehen, nicht nur insgesamt. | `discovery_lib.stress_costs` je Bein angewandt, Gate `cost_stress_ticks=2.0` auf expR gesamt und OOS; Ausweis des Drags in Prozent von R | Kandidat fällt bei 2 Ticks je Bein durch (dann ist er kein Kandidat, egal wie gut die Rohzahl aussieht) | 🟢 | ✅ `stress_costs`, Gate existiert | 1/2 |
| KO-02 | Weil eine ruhende Limit-Order keinen Spread zahlt (AP74), lässt sich bei Lead-Lag der Entry im Laggard als ruhende Order auf dem berechneten Niveau platzieren; das halbiert die Entry-Kosten und kann allein über Leben und Tod der ganzen Familie entscheiden. | Edge mit Market-Entry gegen Limit-Entry auf dem Ziel-Niveau, gleiche Signale, korrekte Ordertyp-Logik in der Kostenrechnung | Limit-Entry hebt die Edge nicht messbar (dann bleibt Market-Entry und der Kostenvorteil ist keiner) | 🟢 | ✅ Ordertyp-Logik wie bei `orb_exec="stop_honest"` | 1 |
| KO-03 | **Ehrlichkeits-Gegenprobe zu KO-02:** Weil eine ruhende Order Queue-Risiko hat und ein nur berührtes Niveau real oft nicht gefüllt wird, ist ein Teil der Limit-Entry-Edge fiktiv; der Anteil der Trades, die von einem Touch-only-Fill abhängen, ist die Größe dieses Risikos. | Anteil der Trades, deren Entry-Niveau in derselben Bar nur berührt und nicht durchhandelt wurde; Edge ohne diese Trades | Über ein Drittel der Edge hängt an Touch-only-Fills (dann ist KO-02 nicht belastbar) | 🟢 | 🔧 Touch-vs-Trade-Through-Zähler | 1 |
| KO-04 | **Nullhypothese für die gesamte Bank:** Weil die Zufallsdecke mit jedem gerechneten Trial mitwächst (`n_global` im Register), muss jeder Fund aus dieser Bank die Decke schlagen, die sich aus der Gesamtzahl aller RV-Trials ergibt — und zusätzlich eine Kontrolle mit zufälligen Entry-Zeitpunkten bei identischer Trade-Zahl und identischen Exits. | Alle RV-Trials im Register mitzählen; Zufallsdecke gegen `n_global`; Placebo-Lauf mit permutierten Signalzeiten | Fund liegt unter der Zufallsdecke oder schlägt den Placebo-Lauf nicht (dann ist er kein Fund) | 🟢 | ✅ Register plus Placebo-Variante | 1/2 |

---

## 📊 Übersicht (Stand 23.08.2026, 100 Hypothesen, 0 getestet)

| Block | n | 🟢 sofort | 🟡 Tages-Zusatzdaten | ✅ Engine reicht | 🔧 neues Feature | Beine 1 | Beine 2+ |
|---|---|---|---|---|---|---|---|
| LL Lead-Lag & Diffusion | 14 | 13 | 1 | 9 | 5 | 14 | 0 |
| SM Spread-Mean-Reversion | 13 | 13 | 0 | 4 | 8 | 1 | 12 |
| RG Regime-Filter | 13 | 6 | 7 | 4 | 9 | 4 | 9 |
| ZF Zeitfenster & Saisonalität | 12 | 12 | 0 | 5 | 7 | 3 | 9 |
| SK Spread-Konstruktion | 11 | 11 | 0 | 0 | 11 | 2 | 9 |
| RS Relative Strength | 11 | 11 | 0 | 2 | 9 | 9 | 2 |
| EV Event & Kalender | 9 | 4 | 5 | 1 | 8 | 3 | 6 |
| MS Mikrostruktur-Proxies | 7 | 7 | 0 | 0 | 7 | 2 | 5 |
| KX Käfig & Buchbeitrag | 6 | 6 | 0 | 3 | 3 | 0 | 6 |
| KO Kosten & Nullkontrollen | 4 | 4 | 0 | 3 | 1 | 2 | 2 |
| **Summe** | **100** | **86** | **14** | **30** | **69** | **40** | **60** |

Familie: alle 100 gehören zu **Relative Value** (der bislang leeren 5. Familie). Keine Zeile braucht Daten, die wir nicht haben — die 14 🟡-Zeilen greifen auf die vorhandenen Tages-CSVs zu (VIXCLS, DGS2/DGS10, DTWEXBGS, DIX_GEX_daily) bzw. auf Kalender-Flags, die aus den Daten ableitbar sind.

**Zwei Zahlen, die die Reihenfolge der Arbeit bestimmen:**
- **40 Hypothesen sind Ein-Bein** (Paar als Signal, Position in einem Instrument). Das ist die kostenverträgliche Hälfte, und dort liegt nach unserer eigenen Historie (#033: leadlag überlebte, div_fade starb an den Kosten) die realistische Chance.
- **69 Hypothesen brauchen ein neues Feature.** Das klingt nach viel, ist es aber nicht: sechs Bausteine schalten den Großteil davon frei (siehe unten).

### Bausteine, die viele Hypothesen gleichzeitig freischalten (nach Hebel sortiert)
1. **Querschnitts-Modul über alle 4 Serien** (Ranking, Dispersion, PCA/s-Score): schaltet RS-02 bis RS-10, SM-11, SK-05/06, RG-10, EV-02 frei — rund 15 Zeilen mit einem Modul.
2. **Hedge-Ratio-Schicht in `rv.py`** (Kalman-Beta, Log-Ratio, dollarneutral, Update-Frequenz, Session-Anker): SK-01 bis SK-04, SK-07, SK-10 — und **verbessert gleichzeitig jede SM- und ZF-Zeile**, weil alle auf demselben Spread rechnen.
3. **Regime-Label-Schicht** (rollende Korrelation, Dispersion, Trendstärke, VIX/GEX/Zins/DXY, jeweils mit Vortages-Lag und Persistenzprüfung): der gesamte RG-Block plus die Splits in SM und RS.
4. **Kalender-Flags** (FOMC, CPI/NFP, OpEx, Roll-Woche, Monats-/Quartalsende, Halbtage): der gesamte EV-Block; teilweise mit den Flags aus [[Hypothesen-Bank (Volumen & Flows)]] gemeinsam nutzbar.
5. **Zeitfenster-/Diagnostik-Schicht** (Uhrzeit-bedingte Vola, Korrelations-Tagesprofil, Slot-Ranking, DST-Split, Entry/Exit-Cutoffs): ZF fast komplett plus SK-08.
6. **Ein-Bein-Ausführung im Paar-Kontext** (Signal aus zwei Serien, Position in einer, korrekte `R_pts`-Zuordnung nach Lehre 46): SM-13, RS-02/04, MS-02/04, KO-02 — und es ist derselbe Codepfad, an dem #090 gescheitert ist, also ohnehin überfällig, sauber gebaut zu werden.

### Kontroll- und Nullhypothesen zuerst (billig, entscheiden über ganze Blöcke)
Diese sieben Zeilen sind **keine Strategien, sondern Messungen**, und sie kosten fast nichts. Sie sollten vor allem anderen laufen, weil jede von ihnen im negativen Fall einen ganzen Block erledigt:

| Zuerst rechnen | Was es entscheidet |
|---|---|
| **SM-01** (Spread-Bewegung vs. 4× Kosten) | Ob 2-Bein-Divergenz-Fade bei uns überhaupt möglich ist. Fällt sie, fallen SM-02 bis SM-12, also 11 Zeilen. |
| **KO-01** (2-Tick-Stress je Bein) | Gate für jeden Kandidaten der ganzen Bank. |
| **KO-02 / KO-03** (Limit-Entry und seine Ehrlichkeits-Gegenprobe) | Ob der Kostenvorteil real ist oder ein Fill-Artefakt. |
| **LL-01** (12 gerichtete Paarungen, sauberer Nachtest) | Ob der einzige Mechanismus, der bei uns je Grade A zeigte, nach dem Fix noch lebt. Fällt er, fällt Block LL. |
| **RG-12 / RG-13** (Regime-Persistenz und Vortages-Lag) | Ob Regime-Labels live überhaupt nutzbar sind. Fallen sie, fällt der halbe RG-Block. |
| **ZF-08 / ZF-11** (DST-Kontrolle, Wochentags-Kontrolle) | Ob gefundene Zeit-Effekte Mechanismus oder Multiple Testing sind. |
| **KO-04** (Zufallsdecke gegen `n_global` plus Placebo) | Ob überhaupt irgendein Fund dieser Bank über der Decke liegt. |

---

## 🥇 Rangfolge: die 12, mit denen ich anfangen würde

Sortiert nach Erkenntnisgewinn pro Rechenzeit, nicht nach Schönheit der Idee.

| Rang | ID | Warum zuerst |
|---|---|---|
| 1 | **SM-01** | Reine Messung, kein Backtest, Minuten Rechenzeit, und sie entscheidet über 11 andere Zeilen. Schlägt die Spread-Bewegung die Kosten nicht um Faktor 4, ist der ganze Fade-Zweig erledigt und wir sparen einen kompletten Sweep. |
| 2 | **LL-01** | Der einzige Mechanismus mit eigener Grade-A-Historie bei uns. Gestorben an einem Rechenfehler, nicht am Markt — und nach dem Fix nur für die alte Config nachgerechnet, nie über alle 12 Richtungen. Offene Frage, keine erledigte. |
| 3 | **KO-02 + KO-03** | Zusammen, nie einzeln. Limit-Entry kann die Kostenrechnung der ganzen Familie drehen, die Gegenprobe verhindert, dass wir uns ein Fill-Artefakt als Edge verkaufen. |
| 4 | **SK-01** | Ein besserer Spread verbessert jede andere Zeile gleichzeitig. Höchster Hebel pro Zeile Code im ganzen Dokument. |
| 5 | **RS-02** | Ein Bein, Querschnitts-Ranking, konzeptionell simpel, und die Literatur (Krauss/Stübinger: Momentum-Paare fast so stark wie MR-Paare) stützt genau die Richtung, die wir bisher nur als „marginal" abgelegt haben. |
| 6 | **RG-01** | Existiert das Korrelationsband, ist es der Filter, der alle anderen Zeilen scharf stellt. Existiert es nicht, sparen wir neun Regime-Zeilen. |
| 7 | **LL-04** | Billig (nur ein Entry-Delay-Parameter) und beantwortet direkt, ob wir überhaupt schnell genug sind, um Diffusion zu handeln. |
| 8 | **KX-03** | Misst die Käfig-Steuer. Ehrlichste Zahl der ganzen Bank: sagt uns, ob Intraday-Pairs im Prop-Käfig überhaupt Sinn ergibt oder ins [[Live-Account]] gehört. |
| 9 | **SK-05** | PCA-Residuum über alle vier statt paarweise. Ein Bein, Avellaneda/Lee im Rücken, und es nutzt unsere vier Serien vollständig aus statt nur zwei. |
| 10 | **ZF-07** | Trivial umzusetzen (Startzeit-Parameter), verbessert potenziell alle Paar-Signale gleichzeitig. |
| 11 | **SM-05** | Die Stop-TP-Kopplung aus Leung/Li. Gilt sie, sweepen wir seit Monaten falsch — und zwar auch bei Nicht-RV-Beinen. |
| 12 | **RG-04** | GEX-Daten liegen ungenutzt herum, Barbon/Buraschi liefern die direkte Vorhersage (negatives Gamma bedeutet mehr Autokorrelation), und es ist ein reines Gate auf eine Strategie, die wir ohnehin rechnen. |

---

## 🚪 Buch-Lücke: was fehlt, damit hiervon etwas ins Buch kommt

Pflichtangabe nach der stehenden Regel. Je Zweig die Stufe, an der es hängt, und was sie braucht:

| Zweig | Aktuelle Stufe | Was konkret fehlt |
|---|---|---|
| **Lead-Lag (LL, 14)** | Prämisse steht, Mechanismus war einmal Grade A, Config tot (#090) | Sauberer Sweep über 12 Richtungen mit gefixtem `R_pts`, Corrupt-Guard, 2-Tick-Stress. Danach über die Zufallsdecke gegen `n_global`, dann Buch-Marginal „besser" (mindestens 1,5 pp und 2× Rauschen). |
| **Spread-Fade (SM, 13)** | Steht **vor** der Prämisse | SM-01 als Messung. Ohne Faktor 4 zwischen Spread-Bewegung und Kosten gibt es keine Prämisse, und der Zweig endet dort. |
| **Relative Strength (RS, 11)** | Prämisse steht (Krauss/Stübinger, beide Richtungen belegt), `div_mom` war marginal | Querschnitts-Ranking-Modul (Baustein 1), dann Gates und OOS, danach dieselbe Kette wie LL. |
| **Spread-Konstruktion (SK, 11)** | Kein Buch-Kandidat, sondern Infrastruktur | Hedge-Ratio-Schicht in `rv.py` (Baustein 2). Zahlt auf LL, SM und RS gleichzeitig ein, ist aber selbst nie ein Bein. |
| **Regime/Zeit/Event (RG, ZF, EV, 34)** | Filter, keine eigenständigen Strategien | Erst braucht es einen Kandidaten mit positiver Roh-Edge. Ein Filter auf einer negativen Strategie ist Overfitting, kein Fund. Diese 34 Zeilen sind Stufe 2, nicht Stufe 1. |
| **Mikrostruktur (MS, 7)** | Datenqualität und Gültigkeit | Kein Buch-Weg. Sie verhindern falsche Funde, sie erzeugen keine. |
| **Käfig/Kosten (KX, KO, 10)** | Bewertungsschicht | Läuft am Ende jeder Kette, entscheidet über Next-Week-Buch plus Ticket. |

**Ehrliche Gesamteinschätzung:** Kein einziger dieser 100 Punkte ist heute ein Buch-Kandidat. Der kürzeste realistische Weg zu einem ist **LL-01** — dort stehen bereits Prämisse, Modul, ein früherer Grade-A-Report und ein verstandener Grund fürs Scheitern. Alles andere ist mindestens zwei Stufen weiter hinten. Und über allem steht die Zahl aus der Meta-Literatur: die Familie hat von 15,6 auf 6,4 Prozent p.a. abgebaut, seit sie bekannt ist.

---

## 📚 Quellen

**Überblick und Taxonomie**
- Krauss (2017), „Statistical Arbitrage Pairs Trading Strategies: Review and Outlook", Journal of Economic Surveys 31(2), 513-545 — [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/joes.12153)
- „A Survey of Statistical Arbitrage", WNE Working Paper 22/2025 (485), Univ. Warschau — [PDF](https://www.wne.uw.edu.pl/application/files/5617/5819/7786/WNE_WP485.pdf)
- „Performance of Pairs Trading", WNE Working Paper 21/2025 (484) — [PDF](https://www.wne.uw.edu.pl/application/files/8917/5759/3293/WNE_WP484.pdf)

**Modelle und Optimierung**
- Leung/Li, „Optimal Mean Reversion Trading with Transaction Costs and Stop-Loss Exit" — [arXiv 1411.5062](https://arxiv.org/pdf/1411.5062)
- Leung/Li, „Optimal Multiple Trading Times Under the Exponential OU Model with Transaction Costs" — [arXiv 1504.04682](https://arxiv.org/pdf/1504.04682)
- Avellaneda/Lee (2010), „Statistical Arbitrage in the U.S. Equities Market", Quantitative Finance 10(7) — [SSRN 1153505](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1153505)
- Wu/Zang/Zhao, „Analytic Value Function for Pairs Trading with a Lévy-Driven OU Process" — [SSRN 3553064](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3553064)
- „Optimal switching for pairs trading rule: a viscosity solutions approach" — [arXiv 1412.7649](https://arxiv.org/pdf/1412.7649)
- „Finding Moving-Band Statistical Arbitrages via Convex-Concave Optimization" — [arXiv 2402.08108](https://arxiv.org/pdf/2402.08108)

**Copula und nichtlineare Abhängigkeit**
- Krauss/Stübinger, „Nonlinear dependence modeling with bivariate copulas: statistical arbitrage pairs trading on the S&P 100" — [EconStor PDF](https://www.econstor.eu/bitstream/10419/125514/1/844416606.pdf)

**Intraday und Hochfrequenz**
- „Intraday pairs trading strategies on high frequency data: the case of oil companies", Quantitative Finance 17(1) — [Tandfonline](https://www.tandfonline.com/doi/abs/10.1080/14697688.2016.1184304)
- „Intraday high-frequency pairs trading strategies for energy futures: evidence from China", Applied Economics 55(56) — [Tandfonline](https://www.tandfonline.com/doi/abs/10.1080/00036846.2022.2161993)
- „Estimation of Ornstein-Uhlenbeck Process Using Ultra-High-Frequency Data with Application to Intraday Pairs Trading" — [arXiv 1811.09312](https://arxiv.org/pdf/1811.09312)
- „Price spread prediction in high-frequency pairs trading using deep learning architectures" — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1057521924007257)

**Paar-Auswahl, Hurst, Strukturbrüche**
- „Applying Hurst Exponent in pair trading strategies on Nasdaq 100 index" — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S037843712100964X)
- „Introducing Hurst exponent in pair trading" — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378437117306738)
- Han et al., „Structural break-aware pairs trading strategy using deep reinforcement learning" — [Springer](https://link.springer.com/article/10.1007/s11227-021-04013-x)
- „Pairs trading with time-series deep learning models" — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2405918826000024)

**Preisfindung, Lead-Lag, Mikrostruktur**
- Hasbrouck, „Intraday Price Formation in US Equity Index Markets", NYU FIN-00-046 — [PDF](https://archive.nyu.edu/bitstream/2451/27374/2/FIN-00-046.pdf)
- Cont/Cucuringu/Zhang, „Cross-impact of order flow imbalance in equity markets", Quantitative Finance 2023 — [Tandfonline](https://www.tandfonline.com/doi/full/10.1080/14697688.2023.2236159)
- „Price discovery in the S&P 500 index derivatives markets" — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1059056016300624)
- „Wavelet-based methods for high-frequency lead-lag analysis" — [arXiv 1612.01232](https://arxiv.org/pdf/1612.01232)
- Epps-Effekt — [arXiv 0704.3798](https://arxiv.org/pdf/0704.3798) · [physics/0701110](https://arxiv.org/pdf/physics/0701110) · [arXiv 2011.11281](https://arxiv.org/pdf/2011.11281)

**Events und Regime**
- „Estimating the Spot Covariation of Asset Prices" (Korrelationsanstieg vor FOMC) — [arXiv 1707.02419](https://arxiv.org/pdf/1707.02419)
- „The Pre-FOMC Announcement Drift", NY Fed Staff Reports — [PDF](https://web-docs.stern.nyu.edu/old_web/finance/docs/pdfs/Seminars/113w-moench.pdf)
- „Volume dynamics around FOMC announcements", BIS Working Paper 1079 — [PDF](https://www.bis.org/publ/work1079.pdf)
- Barbon/Buraschi, „Gamma Fragility" — [SSRN 3725454](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3725454) (bereits im [[Research-Cache]])
- Heston/Korajczyk/Sadka (2010), „Intraday Patterns in the Cross-Section of Stock Returns" — [SSRN 1107590](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1107590) (bereits im Cache)
- Pitkäjärvi/Suominen/Vaittinen, „Cross-Asset Signals and Time Series Momentum", JFE 2019 — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302156) (bereits im Cache)

**Hedge-Ratio**
- Kalman-Filter für dynamische Hedge-Ratios — [QuantStart](https://www.quantstart.com/articles/Dynamic-Hedge-Ratio-Between-ETF-Pairs-Using-the-Kalman-Filter/) · [Palomar, Portfolio Optimization Kap. 15.6](https://bookdown.org/palomar/portfoliooptimizationbook/15.6-kalman-pairs-trading.html)

---

## 🚀 Stand der Umsetzung (23.08.2026, 17:2x)

**14 Jobs in der Queue** (Quelle `hypothesis_bank_pairs`, Prio 88, auf die Box gepusht, Runner läuft):

| Job-IDs | Hypothese | Modus | Configs |
|---|---|---|---|
| `hyp_SM04_{NQ_ES, NQ_RTY, ES_RTY, NQ_YM, ES_YM, RTY_YM}` | SM-04 | `div_fade` | 6 × 63 |
| `hyp_SM05_NQ_ES` | SM-05 (Stop-TP-Kopplung) | `div_fade` | 60 |
| `hyp_SM10_NQ_ES` | SM-10 (Zeitfenster, deckt ZF-04/ZF-09 mit ab) | `div_fade` | 32 |
| `hyp_RS01_{NQ_ES, NQ_RTY, ES_RTY, NQ_YM, ES_YM, RTY_YM}` | RS-01 (Kopf-an-Kopf gegen SM-04) | `div_mom` | 6 × 63 |

Gates wie im Momentum-Schub, inklusive `cost_stress_ticks=2.0`. Die Job-Dateien liegen in `discovery/jobs_proposed/`.

### ⛔ Block LL ist eingefroren — Engine-Bug in der Kostenbasis

Beim Bau der Jobs gefunden und nachgerechnet: **bei `rv_mode="leadlag"` läuft die Position in Symbol 2, die Kosten werden in `run_strategy` aber mit Tick und Punktwert von Symbol 1 berechnet.** `cost_pts_per_trade` (qbt.py:1312) hängt an `symbol`, und `symbol` muss laut `qbt.py:53` gleich `rv_sym1` sein — dem Leader, der die Position gar nicht trägt.

Das ist **Lehre 46 aus #090 ein zweites Mal**, diesmal im Kostenterm statt im Risikoterm. #090 hat `R_pts` auf `c2` umgestellt und die Kostenbasis nicht angefasst; folgenlos blieb das nur, weil die beiden damals getesteten Richtungen (NQ→ES, NQ→RTY) zufällig zu hohe statt zu niedrige Kosten bekommen.

Gemessen (je eine Config, `rv_thr=0.002`, `lag_ratio=0.5`, `rv_stop=0.5`):

| Richtung | n | expR wie berechnet | expR mit korrekter Kostenbasis |
|---|---|---|---|
| **NQ→ES** | 655 | **−0,0259** | **+0,0774** |
| NQ→RTY | 408 | −2,5425 | −0,8948 |
| ES→RTY | 143 | −2,7980 | −1,3913 |
| YM→RTY | 197 | −6,1136 | (Kosten-Drag 648 % von R) |

Bein-Kosten in eigenen Punkten: NQ 1,010 · ES 0,704 · RTY 0,404 · **YM 4,040**. Verhältnis C(sym1)/C(sym2) über alle 12 Richtungen: 6 davon rechnen mit **zu niedrigen** Kosten (RTY→YM Faktor 10, ES→YM Faktor 6, RTY→NQ 2,5) — dort entstünden Scheinedges. Die anderen 6 rechnen mit zu hohen, bis Faktor 10 — dort entstehen falsche Negative.

**Konsequenz:** Der Sweep würde für NQ→ES ein falsches „tot" liefern, obwohl die einzige gerechnete Config mit korrekter Kostenbasis positiv ist. Deshalb ist **kein einziger LL-Job eingereiht**. Die 9 fertigen Job-Dateien (`hyp_LL01_*` × 6, `hyp_LL04`, `hyp_LL07`, `hyp_LL14`) liegen einreihbereit in `discovery/jobs_proposed/`.

**Was der Fix braucht:** in `rv.py` für `leadlag` die von `run_strategy` abgezogene Kostenbasis korrigieren — analog zu `cost2_pts`, das für die Spread-Modi bereits richtig zwischen den Symbolen umrechnet. Danach `box_provision_discovery.ps1 -SyncOnly`, sonst rechnet die Box weiter mit dem alten Code. Vorher `session-guard`, weil `rv.py` eine geteilte Datei ist.

**Wichtig zur Einordnung:** +0,0774 in einer Config ist **keine Edge**. Kein OOS, keine Gates, kein Kostenstress, und es ist genau die Config-Familie, die in #090 beerdigt wurde. Was die Zahl belegt, ist ausschließlich, dass der Test kaputt ist — nicht, dass die Strategie lebt.

### Nicht eingereiht und warum
- **`gap_div` (SM-08):** Modul-Bug aus #033 (Division durch Mini-Risiko) ist im Code weiterhin sichtbar, nicht gefixt.
- **`eod_conv`:** in #033 getötet, steht im Friedhof.
- **Die übrigen 62 Hypothesen:** brauchen einen der sechs Bausteine (Querschnitts-Modul, Hedge-Ratio-Schicht, Regime-Labels, Kalender-Flags, Zeitfenster-Diagnostik, Ein-Bein-Ausführung). Ohne die sind sie keine Queue-Jobs, sondern Entwicklungsarbeit.

### ✅ Nachtrag 23.08.2026, 18:0x — Kostenfix gemacht, LL entsperrt

Max' Ansage: Fix machen und LL nachreihen. Erledigt.

**Der Fix** (`rv.py`, Backup `rv.py.bak-20260823-175453`): für `leadlag` wird die Differenz zwischen der Kostenbasis des Leaders und der des Positions-Beins auf `r` aufgeschlagen, sodass `run_strategy` netto den Betrag des Beins abzieht, das die Position trägt.

```python
cost_lead_pts = 2 * p["slippage_ticks"] * qbt.TICK[s1] + p["commission_rt"] / qbt.POINT_VALUE[micro1]
cost_lag_pts  = 2 * p["slippage_ticks"] * qbt.TICK[s2] + p["commission_rt"] / qbt.POINT_VALUE[micro2]
...
else:  # leadlag
    r += (cost_lead_pts - cost_lag_pts) / R_pts
```

Sauber ist das, weil es bei `leadlag` keinen `target`-Exit gibt und `entry_is_limit` nur für `mode="orb"` greift — `run_strategy` zahlt hier also konstant die volle Slippage auf beiden Seiten, der Korrekturterm ist damit exakt und nicht approximativ.

**Verifikation** (Lead-Lag trifft die handgerechneten Sollwerte, Spread-Modi unverändert):

| Test | erwartet | gemessen |
|---|---|---|
| NQ→ES `leadlag` | +0,0774 | +0,0774 ✓ |
| NQ→RTY `leadlag` | −0,8948 | −0,8948 ✓ |
| ES→RTY `leadlag` | −1,3913 | −1,3913 ✓ |
| NQ/ES `div_fade` (Regression) | −0,0874 | −0,0874 ✓ |
| RTY/YM `div_mom` (Regression) | −0,7213 | −0,7213 ✓ |

Vorher `session-guard`: keine Kollision, keine andere Session hat `rv.py` angefasst. Danach `box_provision_discovery.ps1 -SyncOnly`, damit die Box nicht mit altem Code rechnet.

**Nebenwirkung fürs Register:** alle vor dem 23.08. gerechneten `leadlag`-Trials stammen aus dem alten Kostenmodell und sind mit den neuen nicht direkt vergleichbar. Sie zählen weiter für `n_global` (die Zufallsdecke wächst korrekt mit), taugen aber nicht als Vergleichswert für einzelne Configs.

**LL-Jobs eingereiht: 15 statt 9.** Mit dem Fix sind alle 12 gerichteten Paarungen valide, nicht nur die 6 kostenkonservativen — und damit ist **LL-13 überhaupt erst testbar** (YM als Laggard, also `*→YM`; vorher waren dort die Kosten bis Faktor 10 zu hoch, ein garantiertes falsches Negativ).

| Jobs | Hypothese | Configs |
|---|---|---|
| `hyp_LL01_*` (12 Richtungen) | LL-01, davon 3 zugleich LL-13 | 12 × 36 |
| `hyp_LL04_NQ_ES` | LL-04 Zerfallszeit | 24 |
| `hyp_LL07_NQ_ES` | LL-07 umgekehrtes U | 16 |
| `hyp_LL14_NQ_ES` | LL-14 Uhrzeit (deckt ZF-07/ZF-12 mit ab) | 24 |

Damit sind **29 Jobs aus dieser Bank in der Queue** (14 SM/RS + 15 LL), 1624 Configs. Der Abschnitt „Block LL ist eingefroren" oben ist damit erledigt und nur noch als Fundprotokoll interessant.
