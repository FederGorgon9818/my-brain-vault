---
tags: [projekt, trading, alpha-suche, adx, vwap]
erstellt: 2026-09-21
aktualisiert: 2026-09-21 (Research-Rückschreibung)
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Kapitel "ADX im VWAP-Zweig" in einem Lauf sauber schließen
---

# ADX x VWAP Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 21.09.2026 vom `familien-scout` (Auftrag Max: „ADX in Kombination mit unserer VWAP-Strategie einbauen, alle Möglichkeiten", Markt-Fokus ES/NQ Intraday).
**Nachtrag 21.09.2026 (nach `verdict-auditor`):** sieben Wege ergänzt (W31-W37), sechs Stände korrigiert, vier übersehene Friedhofseinträge nachgetragen. Details unten im Abschnitt „Nachtrag". Die Wege W1-W30 behalten ihre Nummern, die Rangliste ist um W35 und W33 erweitert und daher neu durchnummeriert.
**Nachtrag 2, 21.09.2026 (nach `research-scout`):** je Skelett ist der Research-Stand eingetragen (2× belegt, 10× offen, 1× widerlegt), dazu eine Korrektur an Randbedingung 2. Abschnitt „Research-Stand je Skelett“ unten. Keine Umnummerierung, nichts gelöscht.

Diese Karte **doppelt nichts**: [[VWAP-Offensive]] (Hand-Karte vom 10.09.2026) zerlegt den VWAP in zwölf Mechanismus-Klassen, die [[ADX Wege-Karte]] (21.09.2026, derselbe Agent) zerlegt ADX in 39 Wege. Hier steht ausschließlich die **Kombination**: eine Preis-Bewegung relativ zum VWAP, konditioniert auf einen ADX-Zustand. Die beiden Elternkarten werden nicht angefasst.

Inventar gegen Register (65.035 Trials, Stand 21.09. 19:27), Queue (1.004 Jobs, 0 pending), Engine-Quellcode, [[Strategie-Logbuch]] #046/#097/#101/#108/#133/#136/#139/#142/#147/#150/#153/#157/#161/#162, [[Hypothesen-Bank (Momentum & Averages)]] (AW-01…AW-15b, AR-15/16/17, AC-06/06b/06c, AS-08, AK-01), [[Research-Cache]] (Z. 290-296, 405-416, 460-470, 814-905, 1130, 1278-1292), [[Friedhof-Analyse (17.09.2026)]] (#196) und — neu im Nachtrag — `ideas.json` (vier VWAP-Einträge) plus die drei Hausmessungen vom Abend des 21.09.

---

> [!warning] Drei Befunde, die vor allen Wegen stehen
> **1. Die Kombination ist seit heute ohne eine Zeile Code baubar — die ADX-Karte von heute Morgen ist an dieser Stelle schon überholt.** Die dort als „existiert nicht" geführten Specs MS-1/MS-2 sind inzwischen im Code: `sigcore.daily_context()` liefert `plus_di`, `minus_di`, `adx14`, `di_spread`, `adx_slope5`, `adx_rank` (alle `.shift(1)`, `sigcore.py:712-722`), `sigcore.gates_pass()` kennt `tm_adx_min/max`, `tm_adx_rank_min/max`, `tm_adx_slope_min/max` (`sigcore.py:1142-1146`), `controls.GATE_OFF` und `GATE_INVERT_PAIR` tragen sie (`controls.py:133-142`, `:172-178`). `maband.trades()` ruft `gates_pass` mit genau diesem `ctx_row` auf (`maband.py:633`). **„VWAP-Ereignis × Tages-ADX-Zustand" ist damit heute als `H()`-Zeile in `maband` baubar — mit Null-Schalter, mit automatischem Invert-Arm, und mit 0 Register-Trials Vorbelastung.**
>
> **2. ~~Drei ADX-Gate-Familien sind gebaut, aber von niemandem gefüttert~~ — KORRIGIERT am 21.09.2026 (Nachtrag).** Dieser Befund war **falsch**, nicht nur unvollständig. `tsmom.py:331` schreibt `x_adx14`/`x_adx_rank` aus dem Fremdmarkt-Kontext, `tsmom.py:359-361` schreibt `badx`/`badx_hi`/`badx_slope` inklusive Parametrisierung (`tm_badx_look`, `tm_badx_slope_k`) mit Look-ahead-Wache („letzte vollständige Signalbar"). Dateizeit `tsmom.py` **23:12:10**, also vor Report (23:13) und Karte (23:17): eine Parallel-Session hat MS-V2 und MS-V7 auf dem `tsmom`-Pfad **während** des Scout-Laufs gebaut. **Real offen ist nur noch der `maband`-Zweig** (`maband.py`, Dateizeit 19:31). Folgen für W5/W21/W25: nicht „Fütterung fehlt", sondern „auf `tsmom` da, in `maband` nachziehen" — rund 10 kopierte Zeilen statt 20-30 in zwei Modulen.
>
> **3. Der VWAP-Slot im Buch existiert nicht mehr.** `book_state.json` = `NQ_Momentum_d260818`, `NQ_LastHour_v3`, `NQ_Asia-Dir-USopen_d260820` (`book_state_next.json` identisch). `NQ_VWAP-Pullback` ist seit **#161** (18.09.) raus, gemessen mit **−4,7 ± 0,4 pp**. `replaces="NQ_VWAP-Pullback"` wirft beim Bank-Import einen Assert und hat einen Tag lang **alle** Enqueues blockiert (#161 Lehre 4, fünf Bank-Zeilen stehen deshalb auf `hold`). Jeder Weg dieser Karte ist damit **neues Bein** (`replaces_leg=None`: 577 Buch-Evals, Median −12,3 pp, **0 Treffer jemals**, #139 B3) oder **familien-fremder Ersatz für `NQ_Momentum_d260818`** (Präzedenz AC-06b; laut AP137 Max' Entscheidung). Das ist die harte Obergrenze der Buch-Chance dieser ganzen Karte.

> [!danger] Vierter Befund, nachgetragen: drei Hausmessungen vom selben Abend belasten diese Karte vor
> Parallel zum Scout-Lauf liefen drei **vorregistrierte** Messungen zum ADX-Kern, die in der ersten Fassung dieser Karte in keiner Zeile standen:
> - **`adx_w19_result.json` (23:08)** — ADX gegen Vola, 2.670 NQ- und 2.654 ES-Tage. R²(ADX ~ Vola) 0,19 / 0,11, mit Trend-Proxies 0,30 / 0,27 → unter der vorab gesetzten 0,60-Schwelle, **ADX ist nicht bloß Vola**. Aber die zweite Hälfte derselben Regel reißt: partielles Spearman ρ 0,006-0,027, **alle 90 %-CIs enthalten 0**, Vorzeichen kippt zwischen 2016-20 und 2021-26. „Trägt Information" ist auf beiden Märkten **nicht** erfüllt.
> - **`adx_w38_result.json` (23:14)** + **`adx_w38_level_result.json` (23:27)** — Ereignisstudie zum Rollover-Mechanismus, siehe W30.
> - **`adx_w27_result.json` (23:18)** — ADX-Rollover als Exit auf `NQ_Momentum`, 813 Trades, siehe W23.
>
> Konsequenz für die Filter-Wege W1/W2/W4/W14 und den Torwächter W26: der Stand ist **nicht** „unbelastet offen", sondern **„offen, aber die Feature-Ebene ist bereits negativ gemessen; offen bleibt nur die entry-bedingte Fassung"** (ADX misst auf Tagesebene nichts, was nach Vola-Bereinigung noch nachweisbar wäre — dass es auf der Teilmenge der VWAP-Überdehnungs-Entries anders ist, ist die verbleibende, deutlich engere These).

> [!info] Nebenbefund, der eine Randbedingung der [[VWAP-Offensive]] aufhebt
> `mode="vwap_pullback"` hat seit AP157 Blocker B einen **Null-Schalter** (`controls.py:515-519`, `:688-689`) und kann jetzt `deploy_ready` werden — die dortige Randbedingung 1 („nur `tsmom`/`maband`") gilt nicht mehr. Das Modul ruft allerdings `gates_pass` nie auf und lädt keinen Tageskontext (`vwap_pullback.py`, 193 Zeilen). ADX dort = **MS-V1**, 12-15 Zeilen.

---

## Die sieben harten Randbedingungen

**1. Kein VWAP-Slot mehr** (siehe oben). Ersatz schlägt neu (#139 B3), aber der einzige verfügbare Ersatz ist familien-fremd.

**2. ~~ADX ist ATR-normiert und damit Vola-verwandt~~ — KORRIGIERT 21.09.2026 (Research): der Vola-Confound ist empirisch, nicht konstruktiv.** DX = |+DI − −DI| / (+DI + −DI) — TR/ATR steht in **beiden** DI im Nenner und **kürzt sich im Quotienten heraus** (StockCharts-Formel). ADX ist ein skalenfreies Verhältnis der einseitigen Hoch/Tief-Expansion, **kein** ATR-Proxy per Konstruktion; `adx_w19` (R² 0,19/0,11) passt genau dazu. Der Confound bleibt trotzdem bestehen, nur als **empirische** Tatsache (Trend-Tage sind Hochvola-Tage) statt als Rechenidentität. #136 hat diese Falle einmal aufgedeckt: das gematchte RV20-Gate war **3× stärker** als die eigentliche These. Auf VWAP-Entries kommt erschwerend dazu, dass auch das VWAP-Band ATR-/Streuungs-normiert ist — beide Seiten der Kombination teilen sich den Nenner. **Deshalb steht W26 auf Rang 1 und nicht irgendein Signal-Weg.** *(Nachtrag: `adx_w19_result.json` entlastet ADX teilweise — R² 0,19/0,11 statt der befürchteten Redundanz — belastet ihn aber auf der Informationsseite, siehe Befund 4.)*

**3. Die Tages-Gate-Form ist zweimal durchgemessen und zweimal ohne Kandidat — zusammen 533 Trials.** #136 (AR-15, 353 Trials) und #139 (AR-17, 180 Trials). Dazu die Off-Tage-Malus-Kurve (#139 Lehre 2): **−0,8 pp schon bei 5 % Off-Tagen**, und der θ-Vorfilter r_σ² > r_µ als **Vorab**-Check. Jeder ADX-Tages-Filter zahlt das, bevor er überhaupt Information beweisen darf.

**4. Der Power-Deckel (#162).** Die drei Buch-Beine haben 798 / 967 / 264 Trades gesamt. Für 10 Gate-Varianten × 3 Beine mit Bonferroni bräuchte es 22-217× mehr Trades; Power dort **0,03-0,10**. Jede Gate-Achse bekommt **einen vorregistrierten Test**, kein Grid.

**5. Reversion am VWAP ist tot, Continuation lebt** (#211, #097, #002-#005, Gao/Han/Li/Zhou JFE 2018) — und **#196** trägt den NO-GO-Stempel auf exakt dem Mechanismus, der die ADX-Fassung davon wäre („VWAP Z-Score Mean-Reversion, regime-gefiltert, ADX < 20-25", [[Friedhof-Analyse (17.09.2026)]], `karten_scouts_labs.md` Z. 288). W3/W7/W10/W18/W32 sind damit vorbelastet, nicht jungfräulich.

**6. Der VWAP-Cross ist als Ereignis erledigt (#108).** Der anchored VWAP startet auf dem Open und löst sich nur langsam davon (|VWAP − Open| Median 0,20 σ bei t=5, 0,48 bei t=60); „Cross" heißt im Opening-Fenster per Konstruktion „mehr als die Hälfte retraced" (gemessenes Median-Retracement 0,62). **Acht VWAP-Arten × zwei Exits, keine schlägt das Placebo.** W11/W12 tragen das. `ideas.json` trägt dazu den direkten Haus-Beleg: **„VWAP Holy Grail (vwap_trend)" — Getötet, „NO-GO auf NQ-Futures (Sharpe −1,5, netto negativ)"**, also genau die Seiten-/Flip-am-Cross-Logik.

**7. (Nachtrag) Die Abbruchbedingung für JEDEN Filter-Weg steht schon vereinbart in AR-16.** [[Hypothesen-Bank (Momentum & Averages)]] Z. 421, Mutterhypothese aller Tages-Trendstärke-Filter, Status 🟢, nennt ADX wörtlich als die Variante ohne akademische Primärzahl. Ihr vorab fixiertes Gate: **Kontrast unter expR-Faktor ~1,8 bei ≤ 50 % Trade-Verlust reicht nicht** (Placebo-Rechnung #111: Halbierung der Trades kostet allein ~1,7 pp Passquote). Zusammen mit [[Research-Cache]] Z. 829 (Praktiker-Beispiel: ADX-Gate −81 % Trades) ist das die harte Latte, an der W1/W2/W4/W5/W14/W26/W34 gemessen werden — nicht „expR besser als ohne Gate".

---

## Register-Stand (21.09.2026, nachgezählt)

| Achse | Trials | Survivors | Buch-Kandidat |
|---|---|---|---|
| `mb_kind="vwap"` gesamt | **674** | 77 | 0 |
| ↳ `mb_vwap_evt="dist"` | 517 | — | 0 |
| ↳ `side` / `pullback` / `reclaim` | 61 / 60 / 35 | — | 0 |
| `mb_vwap_dnorm="atr_bar"` (#097-treu, seit #157) | 275 | — | 0 |
| Anker `session` / `hi` / `lo` / `rand_time` | 93 / 38 / 38 / 60 | — | 0 |
| `mb_side="against"` auf VWAP (Continuation) | **426** (10.09. noch 0) | — | 0 |
| `mb_rand_level` auf VWAP | 36 | — | 0 |
| `mode="vwap_pullback"` | 155 | 91 | 0 |
| `i2_mode="vwap_pull"` | 163 | — | 0 |
| `tm_vwap_side` (Schlüssel **aktiv**) | 24.523 | — | 0 |
| `tm_rvol_min` / `tm_delta_min` / `tm_atr_exp_min` (aktiv) | 32.717 / 30.193 / 19.279 | — | 0 |
| ER-Achsen `tm_er_min` (aktiv) / `er_thr` (**vorhanden**) / `rev_er_min` (aktiv) | 168 / 147 / 58 | — | 0 |
| **alle ADX-Schlüssel (`tm_adx*`/`tm_badx*`/`tm_xadx*`)** | **0** | **0** | **0** |
| **ADX zusammen mit `mb_kind="vwap"`** | **0** | **0** | **0** |

> [!note] Zählweise (Nachtrag, Konvention statt Korrektur)
> Die Tabelle mischt zwei Zählweisen und braucht deshalb diese Fußnote: **„Schlüssel aktiv"** heißt, der Parameter steht im Trial **und ist nicht None/aus** (`tm_vwap_side` 24.523, `tm_rvol_min` 32.717, `tm_delta_min` 30.193, `tm_atr_exp_min` 19.279, `tm_er_min` 168, `rev_er_min` 58, `tm_xref_min` 24). **„Schlüssel vorhanden"** heißt bloße Präsenz im Parameter-Dict (`er_thr` 147) — nach dieser Zählweise wären es **49.343 / 49.576 / 45.451 / 38.904 / 297 / 115 / 30**, also grob Faktor 2. Wer gegenrechnet und die Konvention nicht kennt, hält die Karte für falsch. Alle übrigen Zahlen sind unabhängig bestätigt.

**Job-Stand der VWAP-Seite:** `hyp_AW14b_NQ` 72 Configs / 0 Surv / 0 Kand · `hyp_AW15_NQ` 144 / 4 / 0 · `hyp_AW15b_NQ` 144 / **29** / 0 (Decke 1,32) · `hyp_AW14c_NQ` 96 / 17 / 0 (Decke 2,61) · `exit2` 27 / 11 / 0. **Queue:** 1.004 Jobs, 0 pending (504 `done`, 500 `premise_failed`), viermal `queue_empty` seit 20.09. → Rechenzeit ist frei.

---

## Die 37 Wege

Mechanisch aus **Elementen × Beziehungen × Richtung**.
*Elemente VWAP-Seite:* Preis · VWAP-Linie · k-Band (sigma / ATR-Bar) · Bandbreite · VWAP-Steigung · Anker (session / hi / lo / Globex / rand_time) · Kreuzungszahl.
*Elemente ADX-Seite:* Tages-ADX (Niveau, Rang, Steigung) · Bar-ADX (Niveau, Peak, Steigung) · +DI / −DI / DI-Spread · Fremd-ADX (ES) · ATR (gemeinsamer Nenner beider Seiten) · **Wechselzahl des DI-Vorzeichens** (Nachtrag).
*Bewegungen:* hin zu · weg von · durch hindurch · abprallen an · **entlanglaufen an** · kreuzen und halten · kreuzen und scheitern. *Zustände:* eng / weit / wechselt · steigt / fällt / flach.

| Weg | Bewegung × ADX-Zustand | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W1** | weg vom VWAP über k·ATR hinaus, Tages-ADX hoch → Continuation **long** | Trend | Filter | offen, **aber Feature-Ebene negativ vorgemessen** (`adx_w19`, 23:08); VWAP-Arm 517 dist-Trials, ADX-Arm 0 | `maband` `mb_kind=vwap` `mb_vwap_evt=dist` `mb_side=against` `mb_vwap_dnorm=atr_bar` + `tm_adx_rank_min` | Ersatz `NQ_Momentum` |
| **W2** | dieselbe Bewegung **short** | Trend | Filter | offen, dieselbe Vorbelastung wie W1 | wie W1, `tm_dir="short_only"` | Ersatz `NQ_Momentum` |
| **W3** | weg vom VWAP, Tages-ADX **niedrig** → Fade zurück | Mean Reversion | Signal | **Verwandter mit Tötungs-Stempel (#196)** + Fade-Familie geschlossen | wie W1 ohne `mb_side` | — |
| **W4** | weg vom VWAP, ADX **steigt** | Trend | Filter | offen, dieselbe Vorbelastung wie W1 | wie W1 + `tm_adx_slope_min` | Ersatz `NQ_Momentum` |
| **W5** | weg vom VWAP, **Bar-ADX** zum Signalende | Trend | Filter | **korrigiert:** offen; Fütterung auf `tsmom` **vorhanden** (`tsmom.py:359-361`), im `maband`-Zweig fehlt sie | `tm_badx_min` + **MS-V2** (nur noch `maband`, ~10 Zeilen) | Ersatz `NQ_Momentum` |
| **W6** | hin zum VWAP (Pullback) im ADX-hoch-Regime | Trend | Filter | offen, aber Bein raus (#161, −4,7 pp), `pullback` 60 Trials, #097: nah = schlechtere Seite, **+ `ideas.json` „Matteo Coni Drift VWAP Pullback" NO-GO** | `mb_vwap_evt=pullback` + `tm_adx_rank_min`; Buch-Fassung **MS-V1** | neues Bein |
| **W7** | hin zum VWAP bei ADX niedrig → MR am VWAP | Mean Reversion | Signal | **tot** (#002-005, #211, #097, #196) | — | — |
| **W8** | hin zum VWAP, **DI-Spread** wählt die Seite statt der VWAP-Seite | Filter | Messweg | offen; Spalte da, Gate fehlt; **Seiten-Logik im Haus schon tot** (`ideas.json` „VWAP Holy Grail") | **MS-V3** (~10 Zeilen) | kein Bein (**Torwächter 2**) |
| **W9** | **durch** das Band hindurch, ADX hoch | Trend | Signal | offen, deckt sich mit W1; `mb_kind="band"` 179 / 1 | `mb_kind=band` oder W1-Pfad | Ersatz `NQ_Momentum` |
| **W10** | **abprallen** am Band, ADX niedrig | Mean Reversion | Signal | **keine eigene Story** | — | — |
| **W11** | **kreuzen und halten** (Reclaim) mit ADX-Bestätigung | Trend | Signal | offen, aber `reclaim` 35 / 0, **#108** und **`ideas.json` „VWAP Holy Grail" (Sharpe −1,5)** | `mb_vwap_evt=reclaim` + `tm_adx_min` | Ersatz `NQ_Momentum` |
| **W12** | **kreuzen und scheitern** bei ADX niedrig | Mean Reversion | Signal | **keine Story** (#108) | — | — |
| **W13** | **Zahl der VWAP-Kreuzungen je Tag** gegen ADX | Filter | Messweg | offen; AW-07 ungebaut, echte Literatur-Lücke | **MS-V5** | kein Bein |
| **W14** | Bandbreite **eng** × ADX **hoch** | Trend | Filter | offen, Vorbelastung wie W1 **+ `ideas.json` „ORB gefiltert (Trend+VWAP+Vol)" getötet** (derselbe Filterstapel, war Bein 8/9) | `tm_atr_exp_rank_max` + `tm_adx_rank_min` (Proxy sofort), exakt **MS-V6** | Ersatz `NQ_Momentum` |
| **W15** | Bandbreite **weitet sich** × ADX steigt | Trend | Filter | **keine eigene Story** | — | — |
| **W16** | ADX **gegen** die VWAP-Bandbreite (Redundanz) | Filter | Messweg | offen | **MS-V6** | kein Bein |
| **W17** | VWAP-**Steigung** × DI-Spread | Trend | Filter | offen, aber V7 „geprüft, redundant" (91 % Vorzeichendeckung) + „VWAP Holy Grail" tot | **MS-V3** | Ersatz `NQ_Momentum` |
| **W18** | VWAP-Steigung **flach** × ADX niedrig | Mean Reversion | Zeitfenster | **Story deckungsgleich mit W7** | — | — |
| **W19** | Anker-VWAP ab Tagesextrem × ADX | Trend | Filter | offen; hi/lo je 38 Trials, **AW-14c 0 Kandidaten** | `mb_vwap_anchor=hi\|lo` + `tm_adx_*` | neues Bein |
| **W20** | **Globex**-VWAP × Globex-ADX → RTH-Bias | Intraday Bias | Filter | offen, Loader fehlt (AP150 P4), #108 `globex`/`on_frozen` negativ, `tm_base="overnight"` 145 / 0 | Globex-Loader + MS-V2 | neues Bein |
| **W21** | **ES**-ADX als Gate für den NQ-VWAP-Entry | Trend | Filter | **korrigiert:** offen; `tm_xadx_*` auf `tsmom` **verdrahtet** (`tsmom.py:331`), im `maband`-Zweig fehlt es | **MS-V7** (nur noch `maband`, ~8 Zeilen) | Ersatz `NQ_Momentum` |
| **W22** | VWAP-Abstand NQ − ES, gefiltert auf ADX | Relative Value | Signal | offen, **gehört in die [[ES-NQ-Divergenz Wege-Karte]]** | `rv`/`xref`-Pfad | — |
| **W23** | ADX-Rollover als **Exit** eines VWAP-Trades | Trend | Exit | **korrigiert: Verwandter frisch und voll gemessen, gerissen** (`adx_w27_result.json`, 813 Trades) | `tm_exit`-Schicht (ADX-Karte MS-4) | — |
| **W24** | ADX setzt die **Bandweite k** (atmendes Ziel) | Trend | **Level** | offen; neuer Winkel aus AC-06c | **MS-V4** | Ersatz `NQ_Momentum` |
| **W25** | Bar-ADX als **Intraday-Zeitfenster** | Trend | Zeitfenster | **korrigiert:** offen; Fütterung auf `tsmom` da, wartet auf W5 (`maband`) | **MS-V2** (`maband`-Zweig) | Ersatz `NQ_Momentum` |
| **W26** | ⭐ ADX-Gate **gegen gematchtes Vola-Rang-Gate** | Filter | Messweg | offen, beide Gates existieren; **Feature-Ebene am 21.09. schon gemessen** (`adx_w19`: nicht redundant, aber ohne nachweisbare Eigeninformation) | `tm_adx_rank_*` gegen `tm_atr_exp_rank_*` | kein Bein (**Torwächter 1**) |
| **W27** | ADX-Gate gegen RVOL/Delta/ER-Gate | Filter | Messweg | offen; **Arm von W26**, kein eigener Job | wie W26 | kein Bein |
| **W28** | invertiertes ADX-Gate + Off-Anteil-gematchtes Zufalls-Gate | Filter | Messweg | **läuft gratis mit** (`ctl_gate_invert`) | `controls.py:172-178` | kein Bein |
| **W29** *(Swing)* | Mehrtages-/Wochen-VWAP × Tages-ADX | Swing | Signal | offen | MS-V4 + Overnight-Logik (fehlt) | **Live-Buch-Merker** |
| **W30** *(Swing)* | ADX-Rollover über Nacht, Preis jenseits des Tages-VWAP | Swing | Signal | **Research widerlegt (#168 / `adx_w38_result.json` / Schmidhuber arXiv 2006.07847)** — kein Tot-Stempel, der Weg bleibt stehen. Rollover-Form auf eigenem Horizont **gerissen** (`adx_w38_result`, 23:14), **Niveau-Form trägt auf NQ/ES** (L35/L40, `adx_w38_level_result`, 23:27), **Replikation YM/RTY gerissen** | MS-V2 + Overnight-Logik (fehlt) | **Live-Buch-Merker** |
| **W31** *(neu)* | **entlanglaufen an** k-Band: Preis läuft n Bars **außerhalb** des Bands (Band-Walk), ADX hoch → halten/nachlegen statt einsteigen | Trend | **Exit** | offen; **Exit-Block viermal tot** (#046/#142/#147/#150) **+ W23 heute voll gemessen negativ** | **MS-V8** (Persistenz-Zähler, ~20-30 Zeilen) | Ersatz `NQ_Momentum` |
| **W32** *(neu)* | **entlanglaufen an** der VWAP-Linie: Preis klebt n Bars innerhalb ±0,25 σ, ADX **flach** (Balance-Tag) | Mean Reversion | Zeitfenster | **keine Story** (Reparametrisierung von W18, das seinerseits deckungsgleich mit W7 = tot) | — | — |
| **W33** *(neu)* | ADX **fällt** von hohem Niveau als **Intraday-Einstiegs**-Zustand × hin zum VWAP | Mean Reversion | Signal | offen; **Bank-Zeile `ADX-W14` heute 23:19 angelegt** (`hypothesis_bank.py:2183`, ohne VWAP-Kopplung), Tages-Fassung ADX-W38 gerissen | **MS-V2** (`maband`-Zweig, ~10 Zeilen) — auf `tsmom` sofort baubar, aber dort ohne VWAP-Ereignis | Ersatz `NQ_Momentum` |
| **W34** *(neu)* | ADX **flach/Plateau über 40** (Niveau hoch, Steigung ≈ 0 über n Tage) × VWAP-Überdehnung | Trend | Filter | offen; **sofort baubar**, aber Konjunktion aus W1 und zweiseitigem W4 | `tm_adx_rank_min` + `tm_adx_slope_min`/`_max` beidseitig (`sigcore.py:1145`) | Ersatz `NQ_Momentum` |
| **W35** *(neu)* | ⭐ **Torwächter 3 (Level-Placebo):** dasselbe ADX-Gate auf einem **Zufalls-Level** statt auf dem echten VWAP, identische Ereignismenge | Filter | Messweg | offen; `rand_time` 60 Trials, `mb_rand_level` 36; läuft heute **nur für Kandidaten** automatisch mit (`ctl_random_level`, `controls.py:863-866`) | `mb_vwap_anchor="rand_time"` als zweite Achse desselben W26-Jobs | kein Bein (**Torwächter 3**) |
| **W36** *(neu)* | ADX/DI-Spread als **stetiges Größengewicht** auf einem VWAP-Bein (Größe ∝ Trendstärke) statt An/Aus-Gate | Trend | **Sizing** | offen; **ADX-W32-Absage („Min-Size") ist seit 18.09. veraltet** (Größe wird gerechnet, `tempo_plan.py`) | **MS-V9** — weder `maband` noch `tsmom` kennen eine Trade-Größe → **kein Null-Schalter-Pfad, kein Job** | Ersatz `NQ_Momentum` (Sizing-Schicht) |
| **W37** *(neu)* | **DI-Vorzeichen wechselt k-mal in N Bars** (Whipsaw-Zähler auf der ADX-Seite) als Chop-Gate für VWAP-Entries | Mean Reversion | Filter | offen; Spiegelbild von W13, Elternfassung `ADX-W33` | **MS-V10** (= MS-V3 + Zähler, ~15 Zeilen obendrauf) | Ersatz `NQ_Momentum` |

---

## Wege ohne Story (stehen bewusst da, damit sichtbar ist, dass nichts übersprungen wurde)

- **W10 — keine eigene Story, weil das Band kein Order-Level ist.** k·σ bzw. k·ATR um einen gleitenden Durchschnitt ist keine Ebene, auf die jemand eine Order legt. Der „Abprall" ist die Fade-Story aus W3 unter anderem Trigger-Namen, also Reparametrisierung.
- **W12 — keine Story, weil #108 den Cross als Wegmessung entlarvt hat.** „Cross" heißt im Opening-Fenster per Konstruktion „mehr als die Hälfte retraced"; ein **gescheiterter** Cross ist dieselbe Geometrie rückwärts, kein enttäuschter Akteur.
- **W15 — keine eigene Story, weil beide Seiten denselben Nenner haben.** VWAP-Bandbreite und ADX sind beide streuungsnormiert aus derselben Bar-Reihe; „beide expandieren" misst zweimal Vola-Expansion. Das ist der #136-Confound in Reinform.
- **W18 — Story deckungsgleich mit W7** (flacher VWAP + niedriger ADX = Chop-Fenster), kein eigenes Ereignis.
- **W32 *(neu)* — keine Story, weil Reparametrisierung von W18.** „Preis klebt am VWAP" ist dieselbe Zelle wie „VWAP-Steigung flach × ADX niedrig", nur über die Preis-Nähe statt über die Linien-Steigung definiert; W18 ist seinerseits deckungsgleich mit dem toten W7. Die Zelle steht hier trotzdem, weil die Beziehung „entlanglaufen an" im Raster oben steht und sonst niemand sähe, dass sie auch auf der VWAP-Linie geprüft wurde.

## Wege mit Story, aber bewusst ohne Skelett

- **W3 / W7 (Fade und MR am VWAP)** — #196 trägt den NO-GO-Stempel auf **genau diesem** Mechanismus, dazu #002-#005, #211 und die eigene Fade-Messung (AW-09b: PF 0,81-0,91, alle sechs Gates gerissen). Kein neuer Grund vorhanden.
- **W6 (Pullback + ADX-Gate)** — das Bein ist nach vollem Test raus (#161). Ein Gate nachträglich auf ein falsifiziertes Bein zu legen ist Rosinenpickerei, solange W26/W35 nicht gelaufen sind; dazu #162 (Power 0,03-0,10) und der `ideas.json`-Eintrag „Matteo Coni Drift VWAP Pullback" (NO-GO, expR +0,018-0,027, PF 1,05-1,09, P(pass) 23-33 %).
- **W9 (Band-Break)** — deckt sich mechanisch mit W1; ein zweites Skelett auf derselben Bewegung hebt nur die Decke für beide.
- **W11 (Reclaim + ADX)** — #108 (acht VWAP-Arten, keine schlägt das Placebo) + `reclaim` 35 Trials ohne Kandidat + `ideas.json` „VWAP Holy Grail (vwap_trend)": Flip am Cross, Sharpe −1,5, netto negativ. Braucht einen neuen Grund, ich habe keinen.
- **W16** — Zwilling von W26 auf der Session-Bandbreite statt auf dem Tages-Vola-Rang. Erst W26 (kostenlos), dann entscheiden.
- **W17 (VWAP-Steigung × DI-Spread)** — wartet auf **W8**. Die ganze Story ruht auf der Annahme, dass das Hoch/Tief-basierte DI-Vorzeichen mehr trägt als das Close-basierte VWAP-Vorzeichen; genau das misst W8.
- **W19 (Anker × ADX)** — die Anker-Kontrolle selbst hat gerade 0 Kandidaten geliefert (AW-14c). Solange der Anker nicht als informativ belegt ist, ist jeder Anker-Zweig Multiple Testing (VWAP-Offensive V5/V12).
- **W20 (Globex)** — Loader fehlt (AP150 P4 bewusst zurückgestellt), #108 hat `globex` und `on_frozen` bereits negativ gemessen.
- **W21 (ES-ADX)** — die [[ADX Wege-Karte]] führt diese Frage schon als `ADX-W24` mit Skelett. Dazu der Dämpfer aus [[Research-Cache]] Z. 1292: der einzige Cross-Asset-Beleg trägt über **gering** korrelierte Assets, ES/NQ sind ~90 % korreliert.
- **W22 (NQ−ES-VWAP-Spread)** — eigene Karte ([[ES-NQ-Divergenz Wege-Karte]]), nicht doppeln.
- **W23 (ADX-Exit)** — **nicht mehr „offen mit Friedhof daneben", sondern gemessen und gerissen.** `adx_w27_result.json` (21.09., 813 Trades auf dem Buch-Bein-Äquivalent `NQ_Momentum`, zeit-gematchte Pflichtkontrolle im selben Lauf): alle acht Arme haben `d_vs_time ≤ 0` (z.B. `adx_tf1_g3` −0,0368, CI [−0,068; −0,005]; `adx_tf1_g8` −0,0406, CI [−0,070; −0,011]), `d_vs_eod` −0,08 bis −0,21 mit CIs komplett unter 0. Die vorab festgelegte Regel („trägt nur, wenn Differenz gegen Zeit-Exit > 0 UND CI ohne 0 UND nicht schlechter als EOD") ist klar gerissen. Offen bliebe höchstens die Fassung auf `maband`-VWAP-Entries — die braucht einen **neuen** Grund, und ich habe keinen.
- **W25 (Intraday-Fenster)** — derselbe Modulbau wie W5; erst W5 rechnen.
- **W27 / W28** — Arme desselben Kontroll-Jobs wie W26 bzw. automatisch (`ctl_gate_invert`).
- **W31 *(neu)* (Band-Walk als Halte-/Nachlege-Zustand)** — die Story trägt: ein Band-Walk ist ein **Dauer**-Ereignis (n Bars außerhalb), nicht das Schwellen-Ereignis von W1 (einmal k·ATR), und beschreibt genau den Tag, an dem VWAP-benchmarkte Ausführungsalgos gegen einen davonlaufenden Benchmark nachkaufen müssen. Kein Skelett trotzdem, aus zwei Gründen: er landet in der Rolle **Exit/Halten**, dem dichtesten Friedhof des Hauses (#046: 0 von 8 Beinen überlebt OOS; #142: keine Config schlägt OFF, Cross-Leg 0/12; #147/#150: vier `ideas.json`-Einträge getötet), und **W23 ist heute auf genau diesem Bein voll gemessen worden und gerissen**. Dazu braucht er MS-V8. Reaktivierung, konkret: wenn W1 oder W5 einen Kandidaten liefern, ist der Band-Walk die erste Exit-Frage auf diesem Kandidaten — dann mit vorregistrierter Zeit-Exit-Kontrolle wie in `adx_w27_probe.py`.
- **W34 *(neu)* (ADX-Plateau über 40)** — Story trägt (ein Plateau heißt: die gerichtete Range-Erweiterung läuft seit Tagen, ohne sich zu beschleunigen — das ist ein anderer Zustand als „hoch" und als „steigt"), aber mechanisch ist es die **Konjunktion aus W1 und einem zweiseitigen W4** auf derselben Entry-Menge. #162 gibt jeder Gate-Achse **einen** vorregistrierten Test; W1 und W4 sind bereits in der Rangliste. W34 wird entschieden, sobald beide gerechnet sind — ein drittes Skelett hier hebt nur die Zufallsdecke für alle drei.
- **W36 *(neu)* (Sizing-Gewicht)** — die Story ist die stärkste neue der Karte: ein Gate, das die Trade-Zahl um bis zu 81 % senkt ([[Research-Cache]] Z. 829), zahlt zwingend die #139-Off-Tage-Malus-Kurve und die AR-16-Latte (expR-Faktor 1,8 bei ≤ 50 % Trade-Verlust); ein **Gewicht** behält alle Trades und skaliert nur — genau der Ausweg aus dieser Kurve, und seit der Zieländerung vom 18.09. („Min-Size ist als Betriebspunkt nicht mehr gesetzt, Größe wird gerechnet") nicht mehr durch die ADX-W32-Absage blockiert. Trotzdem kein Skelett: **es gibt keinen Pfad.** Weder `maband` noch `tsmom` tragen eine Trade-Größe (Grep `tm_size`/`qty`/`size_mode`: 0 Treffer); ein Gewicht müsste als Spalte je Trade bis in `eval_plan.evaluate_v2` / `cage_policy_lib.evaluate_v2` durchgereicht werden — also **außerhalb** der Null-Schalter-Welt. Hausregel: Wege ohne Null-Schalter-Pfad bekommen eine Modul-Spec (MS-V9), nie einen Job-Vorschlag.
- **W37 *(neu)* (DI-Whipsaw-Zähler)** — Story trägt und ist das exakte Spiegelbild von W13 („misst ein Ereigniszahl-Maß etwas anderes als ein Amplituden-Maß?"), nur auf der ADX- statt auf der VWAP-Seite. Genau deshalb kein zweites Skelett: beide beantworten dieselbe Frage und würden die Decke gemeinsam heben. W37 wird der **zweite Arm von W13**, sobald MS-V3 (DI-Gate) ohnehin für W8 gebaut ist — dann kostet er nur noch MS-V10 (~15 Zeilen) und keine eigenen Trials.

---

## Reihenfolge nach Buch-Chance (13 Skelette)

Ersatz vor neu, engine-fähig vor Modul-Spec, ohne tote Verwandte vor kontaminiert. Kosten-Schwelle MNQ Round-Trip ~2 Punkte je Weg mitgedacht; [[Research-Cache]] Z. 829 warnt, dass ein ADX-Gate die Trade-Zahl massiv senkt (Praktiker-Beispiel −81 %) — jeder Filter-Weg zahlt das gegen θ = 2µ/σ², gegen die #139-Malus-Kurve **und gegen die AR-16-Latte (expR-Faktor ~1,8 bei ≤ 50 % Trade-Verlust)**.

| Rang | ID | Weg | Rolle | Engine | Buch-Bezug | why_status | Stempel |
|---|---|---|---|---|---|---|---|
| 1 | `AXV-W26` | ADX-Gate gegen gematchtes Vola-Rang-Gate (**Torwächter 1**) | Messweg | sofort | kein Bein | **belegt** (#136, Gao/Han/Li/Zhou, Li/Sakkas/Urquhart; Why überarbeitet) | offen |
| 2 | `AXV-W35` *(neu)* | dasselbe ADX-Gate auf `rand_time`-Level (**Torwächter 3**) | Messweg | sofort | kein Bein | **belegt** (#108, #127, Cache Z. 1114; Why überarbeitet) | offen |
| 3 | `AXV-W1` | Continuation ab Überdehnung × ADX hoch, **long** | Filter | sofort | Ersatz `NQ_Momentum` | **offen** (Gao/Han/Li/Zhou ohne Trend-vs-Range-Split) | offen |
| 4 | `AXV-W2` | dieselbe Bewegung **short** (Asymmetrie ist die These) | Filter | sofort | Ersatz `NQ_Momentum` | **offen** (Bollerslev et al. belegt Leverage, nicht ADX) | offen |
| 5 | `AXV-W5` | Überdehnung × **Bar-ADX** statt Tages-ADX | Filter | **MS-V2** (nur `maband`) | Ersatz `NQ_Momentum` | **offen** (+ Warm-up-Problem: 78 Bars/Session gegen ~150) | offen |
| 6 | `AXV-W4` | Überdehnung × ADX-**Steigung** | Filter | sofort | Ersatz `NQ_Momentum` | **offen** (Cache Z. 1288, nur Praktiker-Konsens) | offen |
| 7 | `AXV-W14` | Bandbreite eng × ADX hoch | Filter | sofort (Proxy) | Ersatz `NQ_Momentum` | **offen** (Cache Z. 1285, Gegenwind Daniel/Moskowitz) | offen |
| 8 | `AXV-W8` | DI-Seite gegen VWAP-Seite (**Torwächter 2**) | Messweg | **MS-V3** | kein Bein | **offen** (Cache Z. 1289, größte Literatur-Lücke) | offen |
| 9 | `AXV-W33` *(neu)* | ADX-Rollover intraday als Einstieg zurück zum VWAP | Signal | **MS-V2** (nur `maband`) | Ersatz `NQ_Momentum` | **offen** (Tages-Fassung #168 gerissen, Intraday + Ziel-Level ungemessen) | offen |
| 10 | `AXV-W24` | ADX setzt die Bandweite k (atmendes Ziel) | Level | **MS-V4** | Ersatz `NQ_Momentum` | **offen** (Magnet-These bleibt Analogieschluss) | offen |
| 11 | `AXV-W13` | VWAP-Kreuzungszahl gegen ADX als Chop-Maß | Messweg | **MS-V5** | kein Bein | **offen** (Cache Z. 1290 / 1129-1130) | offen |
| 12 | `AXV-W29` **(Swing)** | Mehrtages-VWAP × Tages-ADX | Signal | MS-V4 + Overnight | **Live-Buch-Merker** | **offen** (Cache Z. 413/1022/1023, Mehrtages-Horizont nirgends belegt) | offen |
| 13 | `AXV-W30` **(Swing)** | ADX-Rollover über Nacht am Tages-VWAP | Signal | MS-V2 + Overnight | **Live-Buch-Merker** | **widerlegt** (#168 invertiert den Trigger; Schmidhuber trägt ihn nicht) | offen |

*(Die Spalte „Stempel" füllt später der `verdict-auditor`, nicht dieser Agent. Die Ränge sind gegenüber der Erstfassung um W35 und W33 erweitert und deshalb neu durchnummeriert; die **Weg**-Nummern W1-W30 sind unverändert.)*

**Begründung der Rang-Abweichungen:**
- `AXV-W35` auf Rang 2, vor allen Signal-Wegen: ein positives W1/W14 ist ohne Level-Placebo nicht von „irgendein Level + ADX-Gate" trennbar. #108 hat acht VWAP-Arten gemessen, **keine schlägt das Placebo** — der Level-Arm ist bei uns der historisch tödlichste. Kostet keine eigene Rechenrunde: zweite Achse desselben W26-Jobs.
- `AXV-W5` (Modul-Spec) vor zwei engine-fähigen Wegen, weil es der einzige Weg dieser Karte ist, der die **zweimal tote Tages-Gate-Achse** nicht wiederholt: Bar-ADX ist ein Intraday-Zustand zum Signalende, kein An/Aus-Schalter über ganze Tage, und fällt damit nicht unter die Off-Tage-Malus-Kurve. **Preis korrigiert:** nicht „~25 Zeilen in zwei Modulen", sondern **~10 kopierte Zeilen in einem** — die `tsmom`-Fassung steht seit 21.09. 23:12 (`tsmom.py:359-361`). Damit ist die Abweichung billiger begründet als in der Erstfassung.
- `AXV-W33` hinter den Torwächtern und hinter W8, obwohl Ersatz-Bein: der Mechanismus ist auf seinem eigenen Horizont am selben Abend **gerissen** (ADX-W38-Messung), die Intraday-Fassung ist also eine Zweitchance mit anderem Horizont und braucht die Vorbelastung sichtbar im Why.

> [!warning] Nicht an `ein-weg` in dieser Runde
> **`AXV-W29`** und **`AXV-W30`** — Swing-Wege, **Live-Buch-Merker**, kein Prop-Buch-Job: mehrtägiges Halten ist unter Trailing-DD-Käfig und Intraday-Bust-Check (#077) nicht führbar, und die Engine hält keine Position über Nacht (`qbt.load_rth()` schneidet auf 09:30-15:59). Beide **bleiben in der Karte** (Regel Max 11.09.2026: nichts, was je eine Edge zeigte, geht verloren). Die übrigen **elf** Skelette gehen an `ein-weg` Schritt 2.
> **Bestätigt nach dem Research (21.09.):** es bleibt bei genau diesen beiden, kein weiteres Skelett wurde aus der Runde genommen. `AXV-W30` ist zusätzlich **Research widerlegt** — das ändert nichts an seinem Verbleib in der Karte, denn „widerlegt“ ist **kein Tot-Stempel** (tot nur nach vollem Test, Regel „Hypothese vor Urteil“). Die zehn „offen“-Skelette gehen mit `why_status: offen` plus Research-Frage an `ein-weg`, nicht als belegt.

---

## Modul-Specs

| Spec | Was fehlt | Wo | Grob |
|---|---|---|---|
| **MS-V1** | `vwap_pullback.py` kennt keinen Tageskontext und ruft `gates_pass` nie auf — das Modul hat seit AP157 einen Null-Schalter, aber kein Gate greift dort | `vwap_pullback.py:69` (`trades()`): `S.daily_context(df, symbol)` + `S.gates_pass(...)` vor dem Entry | **12-15 Zeilen** |
| **MS-V2** *(korrigiert)* | **Auf `tsmom` erledigt** (`tsmom.py:359-361`, inkl. `tm_badx_look`/`tm_badx_slope_k` und Look-ahead-Wache „letzte vollständige Signalbar"). Offen ist nur der `maband`-Zweig: dort läuft `gates_pass` ohne `badx`-Spalten, jedes `tm_badx_*` sperrt weiter jeden Trade (`badx_na`) | denselben Block vor `maband.py:633` kopieren | **~10 Zeilen** (vorher fälschlich 20-30 in zwei Modulen) |
| **MS-V3** | `tm_di_side`: Richtungs-Gate auf `di_spread`. Die **Spalte existiert** (`sigcore.py:718`), das Gate fehlt | `gates_pass` (analog `tm_vwap_side`), `GATE_OFF`, `GATE_INVERT_PAIR` bzw. `GATE_NOT_INVERTIBLE` | **8-12 Zeilen** |
| **MS-V4** | `mb_vwap_k` ist eine Konstante (`maband.py:494`); kein Pfad koppelt die Bandweite an einen Zustand | `maband._signal()` VWAP-Zweig (`maband.py:493-500`) + Ziel/Stop (`maband.py:655-670`) | **15-20 Zeilen** |
| **MS-V5** | VWAP-Kreuzungszähler je Tag als Gate, mit Look-ahead-Wache | `maband._signal()`, Zähler über `sign(c − vw)`-Wechsel bis Signalende | **25-40 Zeilen** |
| **MS-V6** | VWAP-Bandbreite als Gate (`mb_vwap_sd_max/min`); `sd` wird in `maband.py:489` bereits gerechnet und nur nach `level_out` geschrieben, nicht als Gate exportiert | `maband._signal()` | **10-15 Zeilen** |
| **MS-V7** *(korrigiert)* | **Auf `tsmom` erledigt** (`tsmom.py:331`: `x_adx14`/`x_adx_rank` aus `ctx_x`, mit „fehlt der Fremdmarkt-Tag → Gate gibt NIE frei"-Wache). Offen nur der `maband`-Zweig | denselben `ctx_x`-Block vor `maband.py:633` | **~8 Zeilen** (vorher fälschlich 15-20) |
| **MS-V8** *(neu, W31)* | Band-Walk-Persistenz: wie viele aufeinanderfolgende Bars lag der Close **außerhalb** von k·(σ bzw. ATR-Bar)? Existiert nirgends — `maband._signal` kennt nur das Schwellen-Ereignis `abs(z) >= k` (`maband.py:497-500`) | `maband._signal()` VWAP-Zweig, Lauflängen-Zähler bis Signalende, als Gate `mb_vwap_walk_min`, Eintrag in `controls.GATE_OFF`, Look-ahead-Wache | **20-30 Zeilen** |
| **MS-V9** *(neu, W36)* | **Pro-Trade-Größengewicht existiert nicht.** Grep über `maband.py`/`tsmom.py`/`controls.py` nach `tm_size`/`qty`/`size_mode`: 0 Treffer. Ein Gewicht `w = f(adx_rank)` müsste als Spalte je Trade bis in `eval_plan.evaluate_v2:429` / `cage_policy_lib.evaluate_v2:185` durchgereicht werden | `maband`/`tsmom` (Spalte) + Eval-Schicht (Gewichtung) | **40-60 Zeilen über drei Dateien**, davon die Hälfte **außerhalb** der Null-Schalter-Welt → **niemals `deploy_ready` ohne eigenen Kontroll-Arm**; deshalb Spec, kein Job |
| **MS-V10** *(neu, W37)* | DI-Vorzeichenwechsel-Zähler über die letzten N Bars als Gate (`tm_di_flips_max`) — setzt MS-V3 voraus | `sigcore.gates_pass` + Zähler auf `di_spread` bzw. Bar-DI | **~15 Zeilen** zusätzlich zu MS-V3 |

**Keine dieser Specs schlägt einen neuen `mode` vor.** Alles bleibt in `maband`/`tsmom`/`sigcore` bzw. in den sechs Modi mit Null-Schalter (`controls.py:688-689`: `tsmom`, `maband`, `ts_reversal`, `last_hour`, `asian`, `vwap_pullback`). **Ausnahme MS-V9**, die die Null-Schalter-Welt verlässt — deshalb ausdrücklich ohne Job-Vorschlag.

---

## Nachtrag 21.09.2026 (verdict-auditor)

**Sieben Wege ergänzt:** W31 (Band-Walk außerhalb des Bands, die siebte Bewegung „entlanglaufen an", die im eigenen Raster stand und von keinem der 30 Wege benutzt wurde) · W32 (dieselbe Bewegung auf der VWAP-Linie, ohne Story) · W33 (ADX „fällt" als Einstiegs-Zustand — vorher nur als Exit W23 und als Swing W30 vertreten) · W34 (ADX flach/Plateau, der dritte Steigungs-Zustand) · W35 (Level-Placebo, Torwächter 3) · W36 (Rolle Sizing, die einzige fehlende Rolle) · W37 (Wechselzähler auf der ADX-Seite).

**Sechs Stände korrigiert:** Befund 2 / W5 / W21 / W25 / MS-V2 / MS-V7 (Fütterung ist auf `tsmom` da) · W1/W2/W4/W14/W26 (Feature-Ebene bereits negativ gemessen) · W23 (gerissen statt offen) · W30 (`why_status` zurück auf `entwurf`, in Karte, Report **und** JSON — vorher drei Quellen, drei Stände) · Register-Tabelle (Zählweisen-Fußnote).

**Vier übersehene Friedhofseinträge nachgetragen** (alle aus `ideas.json`, Status „Getötet"): „VWAP-z-Burst / Frequenz-Bein" → W1/W2 · „VWAP Holy Grail (vwap_trend)" → W8/W11/W17 · „Matteo Coni Drift VWAP Pullback" → W6 · „ORB gefiltert (Trend+VWAP+Vol)" → W14/W26. Dazu **AR-16** als Mutterhypothese aller Filter-Wege inklusive ihrer vorab fixierten Abbruchbedingung (jetzt Randbedingung 7).

> [!bug] Nebenbefund für ein Ticket, nicht für diese Karte
> Der `ideas.json`-Eintrag „Matteo Coni 'Drift VWAP Pullback'" behauptet in seiner AP116-Klarstellung noch, der Mechanismus „läuft heute LIVE als Buch-Bein `NQ_VWAP-Pullback` in `book_state.json` UND `book_state_next.json`". Das ist seit **#161 (18.09.)** falsch — der Friedhof lügt an dieser Stelle und erzeugt beim nächsten Scout denselben Fehlschluss.

**Wo ich dem Auditor widerspreche** (Begründung, nicht Ignorieren):
1. **Fundstelle Level-Placebo.** Der Auditor nennt `controls.py:749`. Dort steht die `tm_xref_sym`-Kollisionswache in `ctl_symbols`. Der Level-Placebo ist `ctl_random_level`, **`controls.py:831-901`**, der `rand_time`-Zweig für VWAP `dist`/`pullback` in **`:860-866`** samt Selbstbezugs-Wache („Kandidat IST schon der `rand_time`-Placebo-Arm"). Der Befund selbst stimmt komplett, inklusive der Diagnose zu `mb_rand_level` („würfelt Richtung UND Distanz").
2. **„Die Level-Seite kontrolliert nichts."** Zu hart: `ctl_random_level` läuft für **jeden** `maband`-VWAP-**Kandidaten** automatisch mit den Basisparametern, also inklusive des ADX-Gates. Die Lücke ist enger, aber real: die Kontrolle feuert erst **nach** der Gate-Batterie und nur auf Kandidaten, nicht als expliziter Arm auf der vollen Ereignismenge — und genau daran ist AW-14b am 14.09. gescheitert. W35 schließt das als zweite Achse desselben W26-Jobs.
3. **W30.** Der Auditor stützt sich auf `adx_w38_result.json` (23:14). Um 23:27 hat eine Parallel-Session denselben Mechanismus als **Niveau**-Ereignisstudie neu vorregistriert (`adx_w38_level.py`, ausdrücklich auf Auditor-Anstoß) — Ergebnis: **NQ_L35 +77,9 bp (CI [19,8; 133,3], Holm 0,035), NQ_L40 +144,2 bp, ES_L35 +146,7 bp, ES_L40 +113,9 bp, alle vier Kriterien erfüllt → „TRÄGT"**; die Replikation auf **YM/RTY reißt vollständig** (alle vier Zellen, CIs über 0, Hälften uneinheitlich, Holm 1,0) und widerspricht damit direkt Schmidhubers Universalitäts-Anspruch über vier Asset-Klassen. Entscheidend für W30: die Form, die trägt, ist **„ADX hoch UND steigend → Fade"** — also der **Kontroll**-Arm, nicht der Rollover. W30s Trigger ist damit nicht nur unbelegt, sondern von der Messung **invertiert**. Ergebnis gleich (`why_status: entwurf`), Begründung schärfer: nicht „Mechanismus nicht gezeigt", sondern „gezeigt hat sich der Gegenzustand, und nur auf NQ/ES".

---

## Research-Stand je Skelett (21.09.2026, `research-scout`)

Zurückgeschrieben aus dem Research-Schritt des Workflows `konzept-weg`. **Zwei belegt, zehn offen, eins widerlegt.** „Widerlegt“ heißt **nicht tot** — tot wird ein Weg nur nach vollem Test (Regel „Hypothese vor Urteil“). Nichts gelöscht, keine Weg-Nummer geändert.

| ID | `why_status` | Quelle / Befund |
|---|---|---|
| `AXV-W26` | **belegt** | Notwendigkeit der Pflichtkontrolle belegt durch **#136** (gematchtes RV20-Gate 3× stärker als der MA-Filter, +6,98 gegen +2,37 pp) und durch Gao/Han/Li/Zhou + Li/Sakkas/Urquhart (einziger extern belegter Regime-Hebel ist **Vola/News**, Cache Z. 1040/839). Extern **keine** Studie, die ADX gegen ein Vola-Gate auf demselben Entry-Set misst (neuer Negativ-Eintrag im Cache). **Why überarbeitet**, weil das Konstruktions-Argument des Entwurfs mathematisch falsch war (TR kürzt sich in DX heraus). |
| `AXV-W35` | **belegt** | **#108** (acht VWAP-Arten × zwei Exits, keine schlägt das gematchte Placebo, bester Abstand +0,011 R bei 2/5 positiven Blöcken) und **#127** (Bollinger-Break trägt in expR identisch zu einem Zufallslevel gleicher Distanz, Cache Z. 827). Cache Z. 1114: extern testet niemand einen VWAP gegen zufällig verankerte VWAPs — die Kontrolle ist nur hausintern lösbar. **Why überarbeitet** um den Scope-Vorbehalt: #108 misst das **Cross**-Signal, nicht die #097-Distanz-Continuation, und #097 ist NQ-only. |
| `AXV-W1` | offen | Gao/Han/Li/Zhou (SSRN 2440866) belegt Regime-Abhängigkeit für Vola/Volumen/Rezession/News, **keinen** Trend-vs-Range-Split. Eigen: **#097 Punkt 4** (Vortags-Trendstärke-Maße kippen OOS, Trend-Tag-Effekt „real, nicht prognostizierbar“) + `adx_w19` (partielles ρ 0,006-0,027, CIs mit 0). Trade-Reduktion weiter unbelegt: Cache Z. 829 (−81 %, Praktiker), Z. 1291 (18,7 %-Claim unverifizierbar), eigen **#168 W36** (11,7 tpy, Konjunktion 14 % statt 20 %). |
| `AXV-W2` | offen | Bollerslev/Litvinova/Tauchen (JFEC 2006, SSRN 782768) belegt das Leverage-Muster hochfrequent (abwärts = mehr Vola), testet aber **kein** Trendstärke-Maß. Vortags-ADX ist richtungsblind (\|+DI − −DI\|), eine Long/Short-Asymmetrie kann nur über die **Entry-Seite** entstehen. Eigen: #097 Punkt 3 (Kante NQ-only, ES/RTY/YM negativ → ES-Warnung), `adx_w19` negativ. |
| `AXV-W5` | offen | Keine Studie Intraday-ADX gegen Tages-ADX auf demselben Signal gefunden (Sammelsuche, nicht gezielt tief). **Neuer harter Dämpfer:** StockCharts nennt ~150 Perioden, bis ADX stabil ist; 5-Minuten-RTH hat nur **78 Bars je Session** — ein je Session neu gestartetes Bar-ADX wird **nie** stabil. Zusammen mit **#138** (Averages über die durchgehende Serie) heißt das: MS-V2 muss auf der durchgehenden Bar-Serie rechnen, nicht sessionweise neu. |
| `AXV-W4` | offen | Cache Z. 1288: keine Studie ADX-Steigung gegen Niveau, nur Praktiker-Konsens. Überschneidung mit ADX-W13 / `AXV-W1` / W34 hoch (gleiche Entry-Menge, gleiche Gate-Achse); im Haus gewann in der W38-Niveau-Studie gerade **„hoch UND steigend“** (NQ/ES ja, YM/RTY gerissen, **#168**). Feature-Ebene `adx_w19` negativ. |
| `AXV-W14` | offen | Cache Z. 1285: keine Quelle trennt „hohe Trendstärke + niedrige Vola“ von „hoch + hohe Vola“; Daniel/Moskowitz und Li/Sakkas/Urquhart koppeln Trendstärke eher an **hohe** Vola. Der mathematische Teil des Why hält (Browne 1995, Cache Z. 1112; #139-Modell r_µ < r_σ²). Mechanisch ist das Skelett die **ADX-W36-Konjunktion**, die in #168 an 11,7 tpy gestorben ist (`hold`), plus ORB-Bein-8/9-Friedhof. |
| `AXV-W8` | offen | Cache Z. 1289: **keine** Quelle zum Informationsgehalt von Wilders +DM/−DM (Hoch/Tief) gegenüber dem Close-Vorzeichen — größte Literatur-Lücke beider Karten. StockCharts bestätigt nur die Konstruktion (DM aus Hoch/Tief-Differenzen, 14er-Wilder-Glättung, also **langsam**). Haus: die Seiten-Logik „VWAP Holy Grail“ ist getötet (`ideas.json`, #108). |
| `AXV-W33` | offen | Tages-Rollover-Trigger im Haus **gerissen** (#168: 16/18 Zellen CI mit 0, Kontrolle „hoch und steigend“ stärker; W27 `adx_peak`-Exit 8/8 nicht besser als Zeit-Exit). Schmidhuber (arXiv 2006.07847) ist Tages-Horizont + Signifikanz-Maß, **kein ADX** (neuer Cache-Eintrag). Keine Quelle verbindet Trendstärke-Abbau mit einem konkreten **Ziel-Level** — genau der neue Winkel bleibt ungemessen und unbelegt. |
| `AXV-W24` | offen | Execution-Literatur belegt VWAP-**Benchmarks** und vorhersagbaren Preisdruck (Choi/Larsen/Seppi 2021, Cache Z. 1032; Busseti/Boyd; Białkowski et al. Z. 1031), **nicht** VWAP/Band als **Kursziel** — die Magnet-These bleibt Analogieschluss. Eigen: AC-06c (atmend > fest, gemessen aber nur mit **Vola** als Atemgröße); Tages-ADX trägt laut `adx_w19` keine Folgetag-Information, was eine Weitensteuerung schwer begründbar macht. |
| `AXV-W13` | offen | Cache Z. 1290 (kein Vergleich Ereigniszahl gegen Amplitude für Chop) und Z. 1129-1130 (keine Studie mit VWAP-Kreuzungen als Tagescharakter; nur Zero-Crossing-Rate-Literatur ECB WP 450 / Donaldson 2021 im Makro-Kontext). Eigen: #108 misst **0,46 Cross-Events je Tag** — Power-Problem für jeden Zähler auf dieser Basis. |
| `AXV-W29` *(Swing)* | offen | Cache Z. 413 und Z. 1022: keine Vergleichs- oder Placebo-Studie zu Anchored VWAP, der Mehrtages-Horizont ist nirgends belegt. Boyarchenko/Larsen/Whelan (NY Fed SR 917, Z. 1023) benennt nur Dealer-Overnight-Positionen, **nicht** deren VWAP-Einstand. Die Engine hält nichts über Nacht → bleibt Live-Buch-Merker. |
| `AXV-W30` *(Swing)* | **widerlegt** | Die eigene vorregistrierte Messung **invertiert den Trigger**: #168 — Rollover-Fade CI mit 0 in 16/18 Zellen, die Kontrolle „hoch **UND steigend**“ schlägt ihn; die Niveau-Form trägt nur NQ/ES, YM/RTY reißt vollständig. Schmidhuber (arXiv 2006.07847) ist Tages-Futures + Signifikanz-Maß ohne ADX, die beanspruchte Universalität wird von YM/RTY nicht gestützt. **Stand: Research widerlegt — kein Tot-Stempel, der Weg bleibt stehen.** |

**Was sich daraus für die Karte ändert, nicht nur für die Skelette:**
- **Randbedingung 2 ist korrigiert** (siehe oben): ADX ist kein ATR-Proxy per Konstruktion. `AXV-W26` bleibt Rang 1, aber mit **empirischer** statt konstruktiver Begründung — Trend-Tage sind Hochvola-Tage, und `adx_w19` hat die Frage nur auf Tagesebene **ohne Entry-Bedingung** gemessen.
- **Neuer Dämpfer für W5 / W25 / W33** (alle drei auf Bar-ADX): 78 RTH-Bars je Session gegen ~150 Perioden Warm-up. MS-V2 muss auf der **durchgehenden** Bar-Serie rechnen, sonst misst das Gate den Warm-up (#138).
- **W1 und W14 haben je einen frischen Haus-Vorläufer, der an der Trade-Zahl gestorben ist** (#168 W36: 11,7 tpy). Die AR-16-Latte aus Randbedingung 7 ist damit nicht theoretisch, sondern praktisch gerissen.
- **`AXV-W30` bleibt in der Karte**, mit Stand „Research widerlegt“ statt „entwurf“. Reaktivierung nur mit **neu formuliertem Trigger** (die Form, die in #168 trägt, ist „hoch UND steigend → Fade“, also der Gegenzustand).

---

## Offene Research-Fragen (für `research-scout`)

1. Ist der Gao/Han/Li/Zhou-Intraday-Continuation-Effekt regime-abhängig (Trendtag gegen Range-Tag)? — trägt W1/W2/W4.
2. Trennt irgendeine Quelle „hohe Trendstärke + niedrige Vola" empirisch von „hohe Trendstärke + hohe Vola"? ([[Research-Cache]] Z. 1285: Negativbefund vom 21.09.) — trägt W14/W16/W34.
3. Informationsgehalt des Wilder-±DM-Vorzeichens (Hoch/Tief) gegenüber dem Close-Return-Vorzeichen derselben Periode? (Z. 1289: Negativbefund, größte Lücke beider Karten) — trägt W8/W17/W37.
4. Gibt es einen empirischen Vergleich Ereigniszahl-Maß gegen Amplituden-Maß für Chop? (Z. 1290) — trägt W13/W37.
5. Wird der VWAP bzw. sein Band in der Execution-Literatur als **Kursziel** institutioneller Desks belegt? (VWAP-Offensive V8: Choi/Larsen/Seppi belegt Preisdruck-Muster, nicht die Magnet-These) — trägt W24/W31.
6. Gibt es eine Zahl zur Trade-Zahl-Reduktion durch ADX-Gates jenseits des Praktiker-Beispiels (−81 %, Z. 829)? — trägt jeden Filter-Weg und insbesondere die AR-16-Latte.
7. Richtungs-Asymmetrie von Trendstärke-Maßen in Index-Futures (Leverage-Effekt auf ADX)? — trägt W2.
8. *(neu)* Existiert Literatur zu **stetiger** Regime-Gewichtung der Positionsgröße gegen An/Aus-Regime-Gates bei gleicher Signalmenge? (Daniel/Moskowitz-Vol-Scaling ist das nächstliegende, misst aber Vola, nicht Trendstärke.) — trägt W36, die einzige Rolle ohne jeden Beleg.
9. *(neu)* Gibt es eine Quelle zur **Persistenz** von Bandüberschreitungen (Lauflänge außerhalb eines Bands) gegenüber dem einmaligen Schwellen-Ereignis? — trägt W31.

---

## Dateien dieses Laufs

- Report: `C:\Users\maxlk\Projects\trading-data\engine\discovery\scout_reports\familien_adx_x_vwap_260921.md`
- Hypothesen-JSON: `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\familien_adx_x_vwap_260921.json` — **21.09. zurückgeschrieben**: `why_status` je Skelett, `research_status`, `research_date`, `ein_weg`-Flag; bei `AXV-W26`/`AXV-W35` das überarbeitete `why` (Entwurfsfassung steht unter `why_prior_to_research`). Der Report bleibt **unverändert** (Stand des Scout-Laufs).
- Hausmessungen, die diese Karte belasten: `engine\adx_w19_result.json`, `engine\adx_w38_result.json`, `engine\adx_w38_level_result.json`, `engine\adx_w38_level_result_rep_YM_RTY.json`, `engine\adx_w27_result.json`

## Verwandte Notizen
[[VWAP-Offensive]] · [[ADX Wege-Karte]] · [[ES-NQ-Divergenz Wege-Karte]] · [[Alpha-Suche]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Discovery-Runner v2]] · [[Strategie-Familien]] · [[Research-Cache]] · [[Friedhof-Analyse (17.09.2026)]] · [[Day Trading]]
