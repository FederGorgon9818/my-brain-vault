---
tags: [projekt, trading, alpha-suche, overnight-bias, orb]
erstellt: 2026-09-21
aktualisiert: 2026-09-22
research: 2026-09-22 (research-scout-Rueckschrieb: 1 belegt, 12 offen, 0 widerlegt, 0 raus)
nachtrag: 2026-09-21 (verdict-auditor-Lueckenschluss: W39-W50, elf korrigierte Staende)
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Kapitel "Overnight-Bias als Bedingung fuer den Opening-Range-Breakout" sauber schliessen
---

# Overnight-Bias ORB Wege-Karte

**Ziel (einziges Kriterium):** die **v2-Passquote je Eval** des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollstaendigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz fuer welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 21.09.2026 vom `familien-scout`. Quelle des Konzepts: Max, 21.09.2026 (Chat) -- "wie die Overnight-Sessions uns sagen koennten, was wir am heutigen Tag erleben werden". Aufbau nach dem Vorbild [[VWAP-Offensive]] (Hand-Karte, anderes Konzept, hier nicht angefasst) und [[Session Momentum Wege-Karte]].

> [!note] Abgrenzung zur [[Session Momentum Wege-Karte]]
> Die Session-Momentum-Karte fragt: **welches Zeit-Segment sagt welches andere voraus?** Diese Karte fragt enger und konkreter: **was macht der Preis an einem Opening-Range-Level (London 03:00, New York 09:30), abhaengig davon, was die Nacht davor getan hat?**
>
> **Korrektur 21.09.2026 (verdict-auditor):** die urspruengliche Behauptung "Ueberschneidung gibt es bei W7, W28 und W36" war falsch. Tatsaechlich ueberschneiden sich **mindestens 16 Wege**: W5/SES-W26 - W10-W11/SES-W22+W45+W46 - W15-W16/SES-W23 - W17/SES-W2 - W20/SES-W47 - W21/SES-W27 - W22/SES-W28 - W28/SES-W1 - W29-W30/SES-W38 - W31/SES-W32 - W32/SES-W30 - W36/SES-W3 - W37/SES-W11 - W38/SES-W10, dazu neu W39/SES-W26, W40/SES-W6, W43/SES-W31, W44/SES-W43+W44, W49/SES-W35, W50/SES-W36+W37. In mehreren Faellen wich der Stand ab (W20, W37, W15) -- die Schwesterkarte war dort genauer. **Regel ab jetzt:** vor jedem Skelett aus dieser Karte den Stand in der Schwesterkarte gegenlesen, sonst entsteht Doppel-Messung im Register.
>
> Was diese Karte trotzdem NEU hat: alle Wege, bei denen die Nacht ein **Tor** ist statt ein Signal, und der ganze London-ORB-Ast.

**Was "Overnight-Bias -> ORB" hier heisst:** Die Nacht bringt Elemente mit -- Richtung, Spanne, Volumen, Volatilitaet, Pfadform, zwei Segmente (Asien, Europa), den Sprung zum Vortagesschluss und die Position des Cash-Opens in der Nacht-Spanne. Der Morgen bringt eine Linie mit: die Opening-Range-Grenze (London oder New York). Jeder Weg ist eine Bewegung des Preises an dieser Grenze, bedingt auf einen Zustand der Nacht.

---

## Die Lage in einem Satz

> [!important] Der Befund
> Die Engine kennt von der Nacht **einen einzigen Wert**: den Sprung vom Vortagesschluss zum Cash-Open (`on_ret`) -- und der ist zeilengleich mit `gap`. Spanne, Volumen, Volatilitaet, Pfadform und die Trennung Asien/Europa existieren als Kennzahl **nirgends**, obwohl `asian.load_full` die vollen 24-Stunden-Bars schon laedt. Deshalb stehen die meisten Nacht-Zustands-Wege bei 0 Trials, **nicht aus Desinteresse, sondern weil der Schalter fehlt.** Und der eine Job, der den Nacht-Kontext je als Tor gemessen hat (`on01_cashopen_decision_NQ`), fiel in die richtige Richtung -- sein Folge-Job hat dann ausgerechnet die **ungegatete** Zelle weiteroptimiert.

---

## Nachtrag 21.09.2026 (Lueckenschluss nach `verdict-auditor`)

Der `verdict-auditor` hat die erste Fassung dieser Karte geprueft und zehn fehlende Wege, elf falsche Staende und sechzehn uebersehene tote Verwandte gefunden. Alles nachgetragen, **ohne Umnummerierung**: bestehende Wege behalten W1-W38, neu sind **W39-W50**.

**Die drei wichtigsten Korrekturen, weil sie die Beweislast der Rangliste betreffen:**

1. **W3 ist nicht ergebnislos, sondern BESTANDEN.** Die Kontrollzelle "ruhige Naechte" (`tm_on_ret_max=0,0025`) hat **0 von 18 Survivors**, der gegatete Arm (`tm_on_ret_min=0,0025`) **13 von 18**. Die alte Formulierung "Streuung ist das Ergebnis" hat den eigentlichen Befund unterschlagen. Das ist die Beweislast von Rang 1.
2. **Die ON01-Zahlen waren falsch.** `on01_cashopen_decision_NQ` = **71 Trials / 28 Survivors**, nicht 72/18. Die "18" war die GROESSE einer Zelle. Vier Zellen: `on_ret_min 0,0025` 13/18 - ungegatet 10/17 - `on_ret_min 0,0045` 5/18 - `on_ret_max 0,0025` 0/18.
3. **W7 hat sehr wohl eine Leiche.** `mode='firstbar_ematrail'` (Opening-Drive ohne Level, erste 5m-Kerze gegen EMA) hat **2.880 NQ-Register-Trials** und steht in `ideas.json` auf allen vier Maerkten als "Getoetet". Splits: `ny`/`ema_basis=24h` 960 Trials / **109 Survivors**, `ny`/`rth` 960 / **0**, `eu`/`24h` 960 / **0**. Der Europa-Nullbefund aendert zusaetzlich die Erwartung fuer den ganzen London-Ast.

**Zwei Stellen, an denen ich dem Auditor widerspreche** (Begruendung ausfuehrlich im Report, Abschnitt 8.4):

- **`orb`+`orb_std` sind 226 Trials, nicht 229** (181 `orb` + 45 `orb_std`, eigener Counter-Lauf 21.09.). Der Rest der Zahlen des Auditors ist bestaetigt. Ebenso `break_us` mit `rs 03:00` = **35 Trials / 15 Surv** (Karte hatte 33/15), nicht nur die Gesamtzahl 43.
- **Die vier `fb01`/`fb01b`-Job-Dateien sind NICHT dasselbe wie W5.** Sie implementieren `maband mb_kind='channel'` + `mb_side='against'`, also den Fehlausbruch am **RTH-Bar-Extrem-Kanal**, nicht am **Opening-Range-Level** und nicht am **Nacht-Extrem**. Der Auditor hat trotzdem recht, dass Rang 6 nicht 25 Zeilen bauen darf, bevor der billigere Arm ueberhaupt eine Zahl gesehen hat: alle vier Dateien tragen im File `"status": "pending"`, aber in `queue.json` stehen `fb01_failbreak_session_NQ/RTY` und `fb01b_failbreak_fixed_NQ/RTY` auf **`premise_failed`** -- nie gerechnet. Das ist nach "Hypothese vor Urteil" kein Tot-Stempel, sondern ein Vorlauf, der zuerst repariert gehoert.

**Was der Auditor ueber sein eigenes Ergebnis hinaus ausgeloest hat:** beim Nachlesen fuer den neuen Weg W41 (Overnight-VWAP/POC als Level) ist eine Leiche aufgetaucht, die weder Karte noch Auditor hatten -- **#108** hat acht VWAP-Arten gegen ein Placebo gemessen, darunter `on_frozen` (Overnight-VWAP als festes Level, meanR **-0,042**) und `globex` (VWAP ab 18:00 ET, **-0,036**). Keine schlaegt das Placebo. Der Cross-Arm von W41 ist damit tot, bevor er gebaut wird.

---

## Die acht harten Randbedingungen

**1. `mode="orb"` kann NIE `deploy_ready` werden.** `controls.ctl_null` (Z. 689-691) listet nur `tsmom`, `maband`, `ts_reversal`, `last_hour`, `asian`, `vwap_pullback`. `qbt._orb_trades` wertet `tm_null` nicht aus (`tm_null` steht in `qbt.py` nur Z. 267 und 915). Jeder ORB-Kandidat bekommt `{"ok": None, "note": "Modus ohne Null-Schalter"}` und ist per Konstruktion Bank-Material. **Folge fuer diese Karte: der NY-ORB wird ueber `asian.trades` mit `asia_mode="break"`, `rs 09:30-10:00`, `tr 10:00-15:55` gerechnet** -- dasselbe Level, aber mit Null-Schalter (`asian.py` Z. 149-156). Kein neuer `mode`.

**2. `mode="gap"` ebenfalls ohne Null-Schalter.** Betrifft W21/W22. Wer den Gap-Ast als Bein will, braucht zuerst `tm_null` in `qbt._gap_trades`.

**3. `gap` und `on_ret` sind in `sigcore.daily_context` BITGLEICH.** Z. 697: `d["gap"] = d["o"]/d["prev_close"] - 1.0`, Z. 709: `d["on_ret"] = d["o"]/d["prev_close"] - 1.0`. Die Gates `tm_gap_max` und `tm_on_ret_max` sind damit derselbe Filter unter zwei Namen. Kein Job darf beide als getrennte Achsen fuehren (Schein-Vielfalt im Register). Ein echter Gap gegen den Globex-Close existiert bei uns nicht.

**4. Beide Overnight-Gates sind UNSIGNIERT.** `sigcore.py` Z. 1163-1171 nehmen durchgehend `abs()`. Die Engine kann die Nacht heute nur als GROESSE filtern, nie als RICHTUNG. Das ist der Grund, warum W24-W27 bei 0 Trials stehen -- nicht Desinteresse, sondern ein fehlender Schalter.

**5. Die Engine kennt von der Nacht nur den SPRUNG, nicht die SPANNE.** `daily_context` rechnet auf RTH-Bars; `on_ret` ist der Close-zu-Open-Sprung. Range, Vola, Volumen, Pfadform und Segmentierung der Nacht existieren als Kennzahl nirgends. Genau diese Luecke traegt 7 der 38 Wege (W29-W34). Die Daten liegen da: `asian.load_full` laedt die vollen 24h-Bars.

**6. `tsmom`/`maband` handeln nur im RTH** (`sigcore.tmin_of` zaehlt ab 09:30, Daten `between_time("09:30","15:59")`). Jeder London-Weg MUSS ueber `asian.py` laufen. Dort sind `rs_start/rs_end` (Range-Fenster) und `tr_start/tr_end` (Handelsfenster) frei waehlbar -- `asian.py` ist faktisch ein generischer Session-ORB, nicht nur ein Asien-Modul.

**7. Kosten.** MNQ-Round-Trip rund 2 Punkte. Im London-Fenster (03:00-09:30 ET) ist das Buch duenner; jeder Job dort setzt `slippage_ticks=2.0` VORAB (Muster TN-10), sonst ist das Ergebnis wertlos. E8 verbietet Overnight-HALTEN, nicht Nacht-HANDEL -- ein 03:30-09:25-Trade ist regelkonform, solange er vor der EOD-Zwangsschliessung flach ist.

**8. Zufallsdecke.** 65.035 Trials im Register. Zehn Skelette sind bewusst wenige: jedes zusaetzliche Grid hebt die Decke fuer alle bestehenden Kandidaten mit.

---

## Register-Stand (21.09.2026)

**Register (`discovery/registry.json`, Counter-Einzeiler, nie voll gelesen) -- Stand nach dem Nachtrag 21.09., alle Zahlen neu gezaehlt:** 65.035 Trials gesamt. Relevante Schnitte:
`tsmom` 39.846 / `maband` 16.755 / `gap` 397 (143 Surv; `fade` 344, `continuation` 53) / `asian` 298 (65 Surv, 0 Kandidaten) / **`orb`+`orb_std` 226** (181 + 45, 21 Surv, 0 Kandidaten -- korrigiert von 229) / `i2 on_rev` 94 (9 Surv) / **`firstbar_ematrail` 2.880 (109 Surv)**.
Innerhalb `asian`: **`us_dir` 245 (49 Surv**, korrigiert von 52; das Buch-Bein), **`break_us` 43 (16 Surv**, korrigiert von 44; davon `rs 03:00-09:25` **35 Trials / 15 Surv**, korrigiert von 33/15), `fade_us` 8 (0 Surv), **`break` = 2 Trials im ganzen Register**. Der London-eigene ORB (`rs 03:00-03:30`) hat **0 Trials**.
Die 21 `orb`-Survivors sind **20x `SCALP_NQ`** (`backfill:scalp_discovery_results.json`, 60 Trials, #050) **+ 1x `ORB2_ZAR_or5_f380_tEOD`** (Zarattini-Noise-ORB). **`orb_side='fade'` hat im ganzen Register 0 Trials** (`orb_side` kennt nur `breakout` 76, `break` 9, `None` 141). Exit-Achsen am ORB: `orb_max_hold` 5/10/15/20 je 12 Trials, `target_mult` auf allen 226, `or_min` in 5/10/15/30.
`firstbar_ematrail`-Splits: `ny`/`ema_basis=24h` **960 / 109 Surv**, `ny`/`rth` 960 / 0, `eu`/`24h` **960 / 0**.
Overnight-Kontext als Gate: `tm_on_ret_min` 36 Trials / `tm_on_ret_max` 18 / `tm_gap_max` 36 / **`gap_pct_max` (ORB) 0** / **`vix_band` 0**. Alle on_ret-Trials stammen aus EINEM Job: **`on01_cashopen_decision_NQ` = 71 Trials / 28 Survivors** (korrigiert von 72/18), 0 Kandidaten, Status `done`. Zellen: `on_ret_min 0,0025` 13/18 Surv - ungegatet 10/17 - `on_ret_min 0,0045` 5/18 - `on_ret_max 0,0025` **0/18**.
Overnight als Signal: `tm_base="overnight"` 145 Trials, **0 Survivors** -- zusammengesetzt aus **TN-01 97** (ES 49 + NQ 48), **TN-12 25**, **TN-09 21**, **TN-03 1**, **CR-02 1** (nicht "TN-01/03/12" wie in W24 zugeordnet; TN-03 hat exakt EINEN Trial).
`mb_band_evt`: `break` 100 / `fade` 68 / **`walk` 6** -- das Entlanglaufen existiert also als Schalter und ist gemessen. `mb_kind='channel'` 4.086 Trials, `mb_side='against'` 867 (77 Surv). `tm_dow` 72 Trials (davon `hyp_TN09_NQ` 16).
**Queue-Nachtrag:** `premise_failed` und damit NIE GERECHNET sind u.a. `hyp_TN03_NQ`, `hyp_TN05_NQ`, `hyp_TN10_NQ`, `hyp_CR02_ES`, `hyp_AB11_NQ`, `gen_i2_on_rev_ES/RTY/YM`, `gen_asian_fade_break_ES/RTY`, `eusession_break_ES`, `fb01_failbreak_session_NQ/RTY`, `fb01b_failbreak_fixed_NQ/RTY`.
**Buch:** `book_state.json` = 3 Beine (`NQ_Momentum_d260818`, `NQ_LastHour_v3`, `NQ_Asia-Dir-USopen_d260820`), `book_state_next.json` identisch. **Queue:** 1.004 Jobs, 504 `done` / 500 `premise_failed`, **0 pending** (queue_empty).
**Vault:** `Strategie-Logbuch.md` gegrept (#028, #030, #031, #036, #038, #043, #046, #050, #056, #066-#068, #112/#113, #126/#127, #130, #137/#138, #141, #157, #161, #164, #187), `ideas.json` (64 Karten, 8 Treffer im Konzept), vier `Hypothesen-Bank (*).md` (TN-Block 12 Zeilen ungebaut, VV-19/20/48/49, HV-07/08/11, TA-06, ZF-06), `Research-Cache.md` (ORB-Block #068/#070, Alpha-Batch #056, Overnight-RV-Block, Zarattini/Chuk/Syu/Crabel, Boyarchenko + Disappearing-Drift, Rosa 2022, Bogousslavsky 2021, Mesfin arXiv 2605.11423).

---

## Wege-Tabelle (38 Wege)

| Weg | Bewegung | Etikett | Rolle | Stand | Buch-Bezug |
|---|---|---|---|---|---|
| [[#W1]] | Preis bricht nach oben durch das NY-OR-High, nachdem die Nacht eine grosse gerichtete Bewegung gemacht hat. | Trend | Signal | offen (0 Trials in dieser Kombination; 229 orb/orb_std-Trials im Register, davon 0 mit irgendeinem Overnight-Gate) | neues Bein |
| [[#W2]] | Preis bricht nach unten durch das NY-OR-Low, nachdem die Nacht eine grosse gerichtete Bewegung gemacht hat. | Trend | Signal | offen (0 Trials; Short-Seite bei ORB nie getrennt gegen Nacht-Kontext gemessen) | neues Bein |
| [[#W3]] | Preis bricht durch das NY-OR-Level, obwohl die Nacht ruhig war -- der Kontrollweg, der versagen muss. | Trend | Filter | **gemessen, Kontrollweg BESTANDEN** (korrigiert 21.09.): ON01-Zelle `on_ret_max=0,0025` "ruhige Naechte" = **0 von 18 Survivors**, gegen **13 von 18** im gegateten Arm `on_ret_min=0,0025`. Nicht ergebnislos, sondern der Beleg fuer Rang 1 | keiner, Kontrollzelle |
| [[#W4]] | Preis prallt am NY-OR-High/-Low ab und dreht zurueck in die Range, nachdem die Nacht eng war. | Mean Reversion | Signal | **offen, Beleg war falsch zugeordnet** (korrigiert 21.09.): `orb_side='fade'` hat im ganzen Register **0 Trials**; die "32 orb-Trials mit 20 Survivors" gibt es so nicht -- die 20 Survivors sind `SCALP_NQ` (#050, 0,3R-Target + Vol-Filter), ein Breakout-Scalp, kein Fade. ORB-Fade war Buch-Bein `NQ_ORB-fade` bis #126/#127, ist im Register aber nie abgebildet | Ersatz fuer NQ_ORB-fade (Bein war im Buch, ist raus) |
| [[#W5]] | Preis kreuzt das NY-OR-Level, scheitert dort und dreht -- Fehlausbruch gegen eine gegenlaeufige Nacht. | Mean Reversion | Signal | offen am OR-Level (0 Trials), **aber der Mechanismus ist anderswo vorhanden** (korrigiert 21.09.): `maband mb_kind='channel'` + `mb_side='against'` = 867 Register-Trials / 77 Surv am RTH-Kanal, dazu vier fertige Job-Dateien `fb01`/`fb01b`, alle vier in `queue.json` auf `premise_failed` (nie gerechnet) | neues Bein |
| [[#W6]] | Preis bricht das NY-OR-Level, kommt zurueck und laeuft am Level entlang (Retest-Einstieg). | Trend | Signal | tot (#068: Pineda-Retest auf NQ, alle 36 Varianten OOS/2025+ negativ). **Nummer korrigiert 21.09.:** die IVB-Retest-Falsifikation steht in **#083** ("IVB-Nachtest mit exakter Paper-Spec: auch die Original-Regeln haben keine Edge") bzw. #079, **nicht in #164** (= TWAP-Modul-Entscheidung) | keiner |
| [[#W7]] | Preis laeuft vom Cash-Open einfach weg (Opening-Drive ohne Level), aber nur an Tagen mit echter Nacht-Preisfindung. | Trend | Signal | gemessen ohne Kandidat, **Zahlen korrigiert 21.09.**: `on01_cashopen_decision_NQ` = **71 Trials / 28 Survivors** (nicht 72/18; die "18" war die Zellgroesse). Zusaetzlich **massiv vorbelegt**: `firstbar_ematrail` (Opening-Drive ohne Level) hat 2.880 Trials, in `ideas.json` auf allen vier Maerkten "Getoetet" | Ersatz fuer NQ_Momentum_d260818 |
| [[#W8]] | Preis durchquert die NY-OR von einer Seite zur anderen und bleibt drin (Range-Tag), nach enger Nacht. | Mean Reversion | Signal | offen (0 Trials) | neues Bein |
| [[#W9]] | Die NY-OR ist eng im Verhaeltnis zur Overnight-Range -- Kompressionsverhaeltnis statt absolute Breite. | Trend | Filter | offen (0 Trials; Verhaeltnis-Kennzahl existiert nirgends) | neues Bein |
| [[#W10]] | Preis bricht nach oben durch das London-OR-High, in Richtung der Asien-Session. | Trend | Signal | **offen, aber staerker kontaminiert als behauptet** (korrigiert 21.09.): #028 woertlich "London-Breakout (alle Varianten inkl. NR-Filter + **London-IB**, 46 Configs)" -- London-IB IST die London-eigene Range, sie ist mitgetoetet. Neu ist **allein die Asien-Richtungsbedingung**. Dazu: `firstbar_ematrail` mit `session='eu'` = **960 Trials / 0 Survivors** gegen `ny`/24h 109/960 | neues Bein (Live-Buch-Merker bei duennen Fills) |
| [[#W11]] | Preis bricht nach unten durch das London-OR-Low, in Richtung der Asien-Session. | Trend | Signal | offen mit toter Verwandtschaft (wie W10, inkl. der #028-Korrektur und des Europa-Nullbefunds 960/0; Short-Seite im London-Fenster nie getrennt gemessen) | neues Bein (Live-Buch-Merker) |
| [[#W12]] | Preis prallt an der London-OR ab und dreht, wenn Asien richtungslos war. | Mean Reversion | Signal | offen (0 Trials) | neues Bein (Live-Buch-Merker) |
| [[#W13]] | Preis kreuzt die London-OR, scheitert und dreht -- Fehlausbruch bis zum NY-Open. | Mean Reversion | Signal | offen (0 Trials) | neues Bein (Live-Buch-Merker) |
| [[#W14]] | Preis bricht die London-OR ohne jede Nacht-Bedingung -- der reine Lore-Weg. | Trend | Signal | tot (#028: London-Break, Hold-Variante, NR-Filter, London-IB, ES-Variante, 46 Configs alle durchgefallen) | keiner |
| [[#W15]] | Preis bricht im RTH nach oben durch das Overnight-High. | Trend | Level | gemessen ohne Kandidat (asia_mode='break_us': 44 Trials, 16 Survivors, 0 Kandidaten; ideas.json 'NQ Asian-Levels RTH-Breakout' = validiert, aber duenn: OOS +1,2 %, PF 1,07) | neues Bein |
| [[#W16]] | Preis bricht im RTH nach unten durch das Overnight-Low. | Trend | Level | gemessen ohne Kandidat (Teil der 44 break_us-Trials, Seiten nie getrennt ausgewertet) | neues Bein |
| [[#W17]] | RTH eroeffnet ausserhalb der Overnight-Range und laeuft zurueck hinein. | Mean Reversion | Signal | **duenn gemessen, nicht tot** (korrigiert 21.09.): `asia_mode='fade_us'` hat **8** Register-Trials -- das sind keine zehn Implementierungen. Die Transfer-Jobs `gen_i2_on_rev_ES/RTY/YM` und `gen_asian_fade_break_ES/RTY` stehen auf `premise_failed` (nie gerechnet), die lebende Verwandte `i2 on_rev` hat 9/94 Surv. `ideas.json`-KILL bleibt als Urteil fuer NQ/RTY stehen | keiner bis nachgemessen |
| [[#W18]] | Preis laeuft im RTH hin zum Overnight-High/-Low als Ziel -- das Nacht-Extrem als Exit, nicht als Einstieg. | Mean Reversion | Exit | offen (0 Trials; alle bisherigen Exit-Sweeps nutzen nur Zeit, R-Vielfache und ATR) | Ersatz-Exit fuer jedes der drei Buch-Beine |
| [[#W19]] | Preis kreuzt die Mitte der Overnight-Range und haelt sie. | Intraday Bias | Level | offen (0 Trials) | keiner |
| [[#W20]] | Preis laeuft am Overnight-High/-Low entlang, ohne es zu brechen (Absorption am Nacht-Extrem). | Mean Reversion | Filter | **offen, Entwertung ZURUECKGEZOGEN** (korrigiert 21.09.): der Placebo-Vergleich steht in **#138** (AB-14), nicht in #137, und **#151 hat ihn zurueckgezogen** ("Der Satz 'Verhalten am Zufallslevel identisch' ist nicht mehr gedeckt", ungerundetes Placebo, Lehre 151). Engine-Weg existiert: `mb_band_evt='walk'` (maband.py Z. 71/376, 6 Trials) | keiner, aber testbar |
| [[#W21]] | Preis laeuft hin zum Vortages-Schluss und fuellt den Gap. | Mean Reversion | Signal | gemessen, gemischt (mode='gap' gap_side='fade': 344 Trials, Grossteil der 143 gap-Survivors; RTY_Gap-fade war Buch-Bein bis #130, NQ-Gap-fade in ideas.json als tot gefuehrt, Zahl aber von AP116 korrigiert) | Ersatz fuer RTY_Gap-fade (Bein bereits raus) oder neues Bein |
| [[#W22]] | Preis laeuft weg vom Vortages-Schluss und erweitert den Gap. | Trend | Signal | gemessen ohne Kandidat (mode='gap' gap_side='continuation': 53 Trials; ideas.json 'Gap-Continuation (grosse Gaps)' = validiert, D-Note, 17 Trades/Jahr) | neues Bein, realistischer: Gate fuer W1/W2 |
| [[#W23]] | Die Gap-Groesse wirkt nur als Tor auf die Opening-Range-Wege, nicht als eigenes Signal. | Trend | Filter | offen (gap_pct_max existiert in qbt._orb_trades Z. 513-518 und hat NULL Register-Trials; das tsmom-Pendant tm_gap_max hat 36 Trials, ist aber mit tm_on_ret_max identisch, siehe Randbedingung 3) | Gate fuer W1/W2/W7, kein eigenes Bein |
| [[#W24]] | Die Nacht steigt, also werden am NY-Open nur Long-Ausbrueche zugelassen. | Trend | Filter | offen (0 Trials; das vorhandene Gate ist unsigniert -- sigcore.py Z. 1163-1171 nehmen ueberall abs()) | Ersatz fuer NQ_Momentum_d260818 |
| [[#W25]] | Die Nacht faellt, also werden am NY-Open nur Short-Ausbrueche zugelassen. | Trend | Filter | offen (0 Trials, gleiche Luecke wie W24) | Ersatz fuer NQ_Momentum_d260818 |
| [[#W26]] | Nacht-Richtung und Ausbruchsrichtung widersprechen sich, also wird gar nicht gehandelt. | Filter | Filter | offen (0 Trials) | Ersatz-Overlay auf alle drei Buch-Beine |
| [[#W27]] | Die Nacht dreht in sich: Asien laeuft hoch, London laeuft runter -- der Tag wird ein Reversal-Tag. | Mean Reversion | Filter | offen (0 Trials; Segment-Trennung Asien/Europa existiert in sigcore gar nicht, asian.py kann die Fenster nur EINZELN rechnen) | Ersatz-Filter fuer NQ_Asia-Dir-USopen_d260820 |
| [[#W28]] | Die Nacht-Richtung setzt sich im RTH einfach fort, ohne dass ein Level gebrochen werden muss. | Intraday Bias | Signal | im Buch (NQ_Asia-Dir-USopen_d260820, asian asia_mode='us_dir', 245 us_dir-Trials, 52 Survivors) | besetzt -- Ersatz-Slot fuer W24/W25/W27/W32/W34 |
| [[#W29]] | Die Nacht war weit (grosse Range), also traegt der Ausbruch am Morgen. | Trend | Filter | offen (0 Trials; on_range existiert als Kennzahl nicht, sigcore.daily_context kennt nur gap/on_ret) | Gate fuer W1/W2/W7, Ersatz-Overlay auf NQ_Momentum |
| [[#W30]] | Die Nacht war eng, also scheitert der Ausbruch und der Tag wird eine Range. | Mean Reversion | Filter | offen (0 Trials), aber gegen einen eigenen Befund | Gate fuer W4/W8 |
| [[#W31]] | Die europaeische Nacht-Session hatte hohes Volumen, also wird der US-Tag trendig. | Trend | Filter | offen (0 Trials; VV-19 steht als Bank-Zeile ungebaut da, on_rvol existiert nicht) | Gate fuer W1/W2, Ersatz-Overlay NQ_Momentum |
| [[#W32]] | Die Nacht lief trendig statt hin und her (hohe Effizienz des Nacht-Pfades), also wird der RTH ein Trendtag. | Trend | Filter | offen (0 Trials; TN-07 ungebaut, Efficiency Ratio existiert in sigcore nur fuer RTH-Fenster als tm_er_min, 297 Trials) | Ersatz-Filter fuer NQ_Asia-Dir-USopen (dessen asia_dir_thr ist der grobe Vorlaeufer) |
| [[#W33]] | Die Nacht war volatil, also werden Stop und Ziel des Tages groesser gewaehlt -- Skalierung statt Richtung. | Trend | Exit | offen (0 Trials; TV-11 ungebaut, alle Stop-Skalen laufen ueber Vortages-ATR/Sigma) | Ersatz-Overlay auf alle drei Buch-Beine (v2-Passquote direkt ueber die Pfad-Varianz) |
| [[#W34]] | Wo der Cash-Open innerhalb der Nacht-Range liegt (oben, unten, Mitte), bestimmt den Bias des Tages. | Intraday Bias | Filter | offen (0 Trials; on_pos existiert nicht) | Ersatz-Filter fuer NQ_Asia-Dir-USopen_d260820 |
| [[#W35]] | Der Ausgang des London-ORB (durchgelaufen oder gescheitert) ist der Bias fuer den NY-ORB. | Intraday Bias | Filter | offen (0 Trials; zweistufig, kein Modul kann heute zwei Sessions verketten) | Gate fuer W1/W2, kein eigenes Bein |
| [[#W36]] | Die London-Range (nicht die Asien-Range) dient als Level im NY-RTH. | Intraday Bias | Level | gemessen ohne Kandidat (break_us mit rs 03:00-09:25: 33 Trials, 15 Survivors, 0 Kandidaten) | neues Bein |
| [[#W37]] **(Swing)** | Position wird ueber Nacht gehalten, um den Overnight-Drift selbst zu ernten. | Swing | Signal | **teil-tot** (korrigiert 21.09.): #137 fuehrt "Boyarchenko-Overnight-Drift (nur 3 Varianten, Mechanismus nie im richtigen Fenster im Register)" ausdruecklich unter den Urteilen, deren **Formulierung korrigiert werden musste**. Die Schwesterkarte fuehrt SES-W11 ebenfalls als teil-tot. Bei E8 unabhaengig davon regelwidrig | Live-Buch-Merker, nicht Prop-Buch |
| [[#W38]] **(Swing)** | Mehrere gleichgerichtete Naechte hintereinander bilden eine Kette und verstaerken den Bias. | Swing | Filter | offen (0 Trials; TN-11 ungebaut) | Live-Buch-Merker, nicht Prop-Buch |
| [[#W39]] 🆕 | Preis nimmt im RTH das Overnight-High/-Low, haelt es nicht und dreht (Sweep des Nacht-Extrems). | Mean Reversion | Signal | offen, Mechanismus vorbereitet aber nie gerechnet (vier Job-Dateien `fb01`/`fb01b` = `maband channel/against`, alle vier `premise_failed`; lebende Verwandte `i2 on_rev` 94/9) | neues Bein |
| [[#W40]] 🆕 | Die Nacht-Richtung kehrt sich im RTH um, ohne dass ein Level gebrochen wird (Tug-of-War auf Tagesebene, Spiegel zu W28). | Mean Reversion | Signal | duenn gemessen (TN-03 hat **1** Register-Trial, `hyp_TN03_NQ` = `premise_failed`; Schwesterkarte SES-W6a offen mit Auflage, SES-W6b durchgefallen) | Ersatz-Arm zu NQ_Asia-Dir-USopen_d260820 |
| [[#W41]] 🆕 | Preis laeuft zum volumengewichteten Schwerpunkt der Nacht (Overnight-VWAP / -POC / -TWAP), hindurch oder prallt ab. | Mean Reversion | Level | **teilgemessen, Cross-Arm verloren** (#108: `on_frozen` Overnight-VWAP als festes Level meanR **-0,042**, `globex`-VWAP **-0,036**, keine von 8 VWAP-Arten schlaegt das Placebo). POC-/TWAP-Arm und "hin zu als Ziel" weiterhin 0 Trials | kein eigenes Bein; Ziel-Arm faellt unter W18/W47 |
| [[#W42]] 🆕 | Die Wochenend-/Feiertags-Nacht (Freitag-Schluss bis Montag-Open) ist ein anderer Nacht-Typ als die Werktags-Nacht. | Filter | Filter | gemessen ohne Kandidat (TN-09, 21 Register-Trials, davon 16 mit `tm_dow`, 0 Survivors) -- als **Pflicht-Split** aber auf keinem einzigen Nacht-Weg dieser Karte angewendet | keine eigene Zeile: **Auflage** auf W1-W41 |
| [[#W43]] 🆕 | Langer Globex-Pfad bei kleinem Sprung zum Open: die Nacht hat gearbeitet und nichts bewegt (Absorption). | Mean Reversion | Filter | offen (0 Trials; TN-06 ungebaut, Pfadlaenge existiert als Kennzahl nicht; Schwesterkarte SES-W31) | Gate fuer W4/W8/W30 |
| [[#W44]] 🆕 | Die zweite Naht der Nacht: die Globex-Reopen-Luecke (RTH-Close 17:00 gegen Reopen 18:00), hin zu (Fill) und weg von (Erweiterung). | Mean Reversion | Level | offen (0 Trials; `mode='gap'` kennt nur den Cash-Open und hat keinen Null-Schalter; Schwesterkarte SES-W43/W44) | kein Bein ohne S6-Aequivalent im gap-Modus |
| [[#W45]] 🆕 | Die letzte Nacht-Stunde vor dem Open (08:30-09:30 ET) ist ein eigenes Segment neben Asien und Europa. | Trend | Filter | offen (0 Trials; MO-51 und KF-40 ungebaut; `asian.py` kann das Fenster einzeln rechnen, `sigcore` kennt es nicht) | Gate fuer W1/W2/W7, Ersatz-Overlay NQ_Momentum |
| [[#W46]] 🆕 | Der Nacht-Zustand bestimmt die DEFINITION der Opening Range (Laenge/Breite adaptiv), nicht nur den Entry daraus. | Trend | Level | offen als Bedingung (0 Trials); die **feste** OR-Laenge ist gesweept (`or_min` 5/10/15/30 ueber 226 orb-Trials), die Kopplung an die Nacht nie. Bank-Verwandte VV-14 | Achse fuer W1/W2/W4, kein eigenes Bein |
| [[#W47]] 🆕 | Ziel und Haltedauer am NY-OR-Level werden an der Nacht-Vola bemessen (ORB-Scalp: enges Ziel, kurzes Fenster). | Trend | Exit | teilgemessen ohne Nacht-Bedingung: **#050 `SCALP_NQ` = 60 Trials / 20 Survivors**, war Buch-Bein 9, die EINZIGE ORB-Familie mit Survivors. `orb_max_hold` 5/10/15/20 je 12 Trials, `target_mult` auf allen 226. Mit Nacht-Bedingung 0 Trials | Ersatz-Exit fuer alle drei Buch-Beine |
| [[#W48]] 🆕 | Preis bricht die London-OR, kommt zurueck und laeuft am Level entlang (Retest im London-Fenster). | Trend | Signal | offen (0 Trials); die Relation "entlanglaufen" war im London-Ast leer, NY hat sie als W6 (dort zweimal tot) | neues Bein (Live-Buch-Merker) |
| [[#W49]] 🆕 | Kontrollweg: verschiebt sich jeder 03:00-ET-Effekt mit der Sommerzeit-Umstellung (US und EU schalten an verschiedenen Terminen)? | -- | Kontrolle | offen, **Pflichtbeilage** zu W10-W14, W36, W45, W48; Schwesterkarte fuehrt ihn als SES-W35 | keiner, Kontrollweg |
| [[#W50]] 🆕 **(Swing)** | Der heutige RTH-Return setzt sich in der kommenden Nacht fort bzw. dreht (Rueckrichtung Tag -> Nacht). | Swing | Signal | offen (0 Trials; jeder der 298 `asian`-Trials handelt im RTH, keiner mit dem RTH als Quelle; Schwesterkarte SES-W36/SES-W37) | Live-Buch-Merker, nicht Prop-Buch |


**Vollstaendigkeits-Nachweis (mechanisch, nicht aus dem Kopf; Stand nach dem Nachtrag 21.09.):** Elemente = Preis, NY-OR-Grenze, London-OR-Grenze, Overnight-High/-Low/-Mitte, **Overnight-VWAP/POC**, Vortages-Schluss, **Globex-Reopen-Grenze**, Overnight-Richtung, Overnight-Spanne, Overnight-Volumen, Overnight-Vola, Overnight-Pfadform, Asien-Segment, Europa-Segment, **Vor-Open-Segment 08:30-09:30**, **Nacht-Typ (Werktag/Wochenende/Feiertag)**, Position des Opens in der Nacht-Spanne. Bewegungen je Paar = hin zu, weg von, durch hindurch, abprallen an, entlanglaufen an, kreuzen und halten, kreuzen und scheitern. Zustaende = steigt/faellt, eng/weit, hoch/niedrig, dreht.

Daraus: **A** NY-OR (W1-W9, **W46 Definition**, **W47 Exit-Raum**) - **B** London-OR (W10-W14, **W48 entlanglaufen**) - **C** Overnight-Extrema (W15-W20, **W39 kreuzen und scheitern**) - **D** Vortages-Schluss (W21-W23) + **zweite Naht Globex-Reopen (W44)** - **E** Nacht-Richtung (W24-W28, **W40 Umkehr-Arm**) - **F** Nacht-Zustaende (W29-W34, **W43 Absorption**) - **G** Kaskade London->NY (W35-W36) - **H** Segmente (**W45 drittes Segment**, **W42 Nacht-Typ**) - **I** Nacht-Schwerpunkt (**W41**) - **J** Kontrollen (**W49 DST**) - **K** Swing (W37-W38, **W50 Tag->Nacht**).

**Drei Wege stehen bewusst ohne Handels-Story da** (W19 geometrische Nacht-Mitte, W42 Nacht-Typ = Auflage statt Strategie, W49 DST-Kontrolle) -- mit Begruendung, nicht durch Weglassen. **W20 steht nicht mehr darunter**: seine Entwertung ist zurueckgezogen.

---

## Je Weg


### W1

**Bewegung:** Preis bricht nach oben durch das NY-OR-High, nachdem die Nacht eine grosse gerichtete Bewegung gemacht hat.

- **Etikett / Rolle:** Trend / Signal
- **Stand:** offen (0 Trials in dieser Kombination; 229 orb/orb_std-Trials im Register, davon 0 mit irgendeinem Overnight-Gate)
- **Story:** Wer die Nacht ueber in Asien/Europa eine Position aufgebaut hat, kann sie ohne US-Cash-Liquiditaet nicht groesser machen. Am 09:30-Open kommt die eigentliche Entscheider-Kohorte (Index-Fonds, Creation/Redemption, US-Desks) und muss die Nachtbewegung bestaetigen oder korrigieren. Bricht der Preis danach durch die OR-Grenze, ist das die Bestaetigung mit dem groessten verfuegbaren Kaeufer im Ruecken. Das Geld bleibt liegen, weil der reine Level-Bruch ohne Nacht-Bedingung nachweislich 51/49 ist (#068) und deshalb kaum jemand ihn noch bedingt handelt.
- **Engine-Weg:** Modul-Spec: Overnight-Gate in asian.py (as_on_ret_min/max) -- der ORB selbst ist als asian.trades mit asia_mode='break', rs_start='09:30', rs_end='10:00', tr_start='10:00', tr_end='15:55' schon rechenbar (asian.py Z. 132-156) und hat ctl_null. mode='orb' waere naeher am Vorbild, hat aber KEINEN Null-Schalter (controls.py Z. 689-691).
- **Buch-Bezug:** neues Bein
- **Verwandte Tote (21.09. erheblich erweitert, der ORB-Friedhof aus `ideas.json` fehlte fast komplett):** #068 (kein Follow-Through nach ORB-Break, 2.685 Tage), #067 (Breakout-ORBs ehrlich tot, aus dem Buch geworfen). Dazu aus `ideas.json`:
  - **"Noise-ORB NQ (Zarattini SSRN 4824172)" = Validiert** -- #068 `NOISE_ORB_NQ_m1.0`, IS +0,094 = OOS +0,097, 9/11 Jahre, Auto-Fit abgelehnt. **Der staerkste ehrliche ORB-Verwandte auf NQ**, im Register als `ORB2_ZAR_or5_f380_tEOD` der 21. Survivor. Wichtig fuer Rang 2/4: das Noise-Band ist ein 14-Tage-Sigma-Band -- `on_sigma`/`on_range` wuerden genau dieses Band parametrisieren. Jeder Nacht-Gate-Test am ORB muss das Noise-Band als Vergleichsarm mitfuehren, sonst misst er gegen den falschen Stand der Technik.
  - **"ORB-VIX-Band (Chuk-Dealer-Hedging-Faktor)" = Getoetet** -- #068 `ORB_VIXBAND_NQ`, expR +0,10 im VIX-Band 15-25, **vom Auto-Fit abgelehnt, nicht vom Mechanismus**. Der Test lief ausserhalb des Registers; der Zaehler "`vix_band` 0 Trials" ist deshalb irrefuehrend.
  - **"OR_DELTA_BIAS_NQ (Tick-Rule-Delta OR-Fenster 09:30-10:00)" = Validiert** (#079/#083): LONG ueberlebt, SHORT nicht. Lebender Verwandter im selben Fenster, mit genau der Long/Short-Asymmetrie, die W2/W16 behaupten.
  - **"Standard-ORB (Institutional, roh) + ORB+RVOL-Filter"**, **"ORB gefiltert (Trend+VWAP+Vol) inkl. Vol-Scalp Bein 8/9"**, **"ORB + ATR-Expansions-Filter"** = alle **Getoetet**.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W2

**Bewegung:** Preis bricht nach unten durch das NY-OR-Low, nachdem die Nacht eine grosse gerichtete Bewegung gemacht hat.

- **Etikett / Rolle:** Trend / Signal
- **Stand:** offen (0 Trials; Short-Seite bei ORB nie getrennt gegen Nacht-Kontext gemessen)
- **Story:** Spiegel zu W1, aber die Kohorte ist eine andere: nach unten wird nicht neu aufgebaut, sondern glattgestellt. Die Nacht-Bewegung ist dann kein Aufbau, sondern ein Risiko-Abbau, den der US-Open beschleunigt. #036 hat auf NQ gemessen, dass ORB-Short je nach Variante mal deutlich schwaecher (Breakout) und mal deutlich staerker (RVOL-Filter) ist als Long -- die Seite gehoert also getrennt gemessen, nicht mitgeschleift.
- **Engine-Weg:** Modul-Spec: wie W1, zusaetzlich tm_dir/Seiten-Trennung; Pflichtkontrolle controls.ctl_sides.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** #036 (ORB Long/Short-Split), #067
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W3

**Bewegung:** Preis bricht durch das NY-OR-Level, obwohl die Nacht ruhig war -- der Kontrollweg, der versagen muss.

- **Etikett / Rolle:** Trend / Filter
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **gemessen, Kontrollweg BESTANDEN.** Die alte Formulierung "Streuung ist das Ergebnis" hat den eigentlichen Befund unterschlagen. Register, Job `on01_cashopen_decision_NQ`, Zellen: `on_ret_max=0,0025` (ruhige Naechte) **0 von 18 Survivors** gegen `on_ret_min=0,0025` **13 von 18** -- ungegatet 10 von 17, `on_ret_min=0,0045` 5 von 18. Die Kontrollzelle versagt also genau so, wie sie versagen muss. **Das ist die Beweislast von Rang 1**, nicht ein ergebnisloser Lauf.
- **Story:** Keine eigene Handels-Story, und das ist Absicht: dieser Weg ist die Kontrollzelle fuer W1/W2/W7. Wenn das Overnight-Gate echt ist, muss die ruhige Nacht die Edge kaputtmachen. Ohne diese Zelle ist jedes Gate-Ergebnis nur eine Stichprobenverkleinerung. **Offene Gegenfrage, die der bestandene Kontrollweg NICHT beantwortet:** 0 von 18 kann auch heissen, dass die Teilstichprobe zu klein fuer einen Survivor war. Vor jeder Berufung auf diese Zelle gehoert die Trade-Zahl je Arm daneben (`quant-statistician`, Power).
- **Engine-Weg:** engine-faehig: tsmom tm_on_ret_max (sigcore.py Z. 1166-1168)
- **Buch-Bezug:** keiner, Kontrollzelle
- **Verwandte Tote:** gehoert als Pflichtzelle in ON-W7a und ON-W24a
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W4

**Bewegung:** Preis prallt am NY-OR-High/-Low ab und dreht zurueck in die Range, nachdem die Nacht eng war.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **Beleg war falsch zugeordnet.** `orb_side='fade'` hat im **gesamten** Register **0 Trials** (`orb_side` kennt nur `breakout` 76, `break` 9, `None` 141). Die "32 orb-Trials mit 20 Survivors" gibt es so nicht: die 20 Survivors sind `SCALP_NQ` aus `backfill:scalp_discovery_results.json` (60 Trials, #050 ORB-Scalp mit 0,3R-Target + Vol-Filter) -- ein **Breakout**-Scalp, das Gegenteil eines Fades. ORB-Fade war zwar Buch-Bein `NQ_ORB-fade` bis #126/#127, ist im Register aber nie abgebildet. Damit ist W4 **offen und ungemessen**, nicht teilgemessen.
- **Story:** Eine enge Nacht heisst, dass die Nacht-Kohorte keine neue Bewertung gefunden hat. Dann ist die OR-Grenze am Morgen kein Informations-Level, sondern die Grenze einer Auktion im Gleichgewicht -- der erste Ausbruch ist Liquiditaetssuche, kein Trend. Das Geld bleibt liegen, weil Fade-Setups am Level gegen die Intuition laufen und im Trailing-DD-Kaefig unangenehm aussehen.
- **Engine-Weg:** Modul-Spec: Overnight-Range-Kennzahl (on_range) fehlt; ORB-Fade selbst ist als orb orb_side='fade' vorhanden, aber ohne Null-Schalter.
- **Buch-Bezug:** Ersatz fuer NQ_ORB-fade (Bein war im Buch, ist raus)
- **Verwandte Tote:** #126/#127 (ORB-fade aus dem Buch), #030 (ORB-fade + NR7 im Buch)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W5

**Bewegung:** Preis kreuzt das NY-OR-Level, scheitert dort und dreht -- Fehlausbruch gegen eine gegenlaeufige Nacht.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** am OR-Level weiterhin 0 Trials, **aber die Engine-Aussage "weder orb noch asian kennen eine gescheiterter-Bruch-Seite" war zu eng.** `maband` `mb_kind='channel'` + `mb_side='against'` IST dieser Arm (867 Register-Trials / 77 Survivors), nur am RTH-Bar-Extrem-Kanal statt am OR-Level. Dazu liegen **vier fertige Job-Dateien** in `jobs_proposed`: `260831_fb01_failbreak_NQ/RTY` und `260903_fb01b_failbreak_fixed_NQ/RTY`. Alle vier tragen im File `"status": "pending"`, stehen in `queue.json` aber auf **`premise_failed`** -- also **nie gerechnet**, nicht widerlegt.
- **Story:** Der teuerste Trade des Tages ist der, der genau am Level gegen die Nacht-Positionierung gekauft wird. Wenn die Nacht nach unten lief und der Morgen nach oben ausbricht, stehen die Nacht-Shorts im Verlust und die Ausbruchs-Longs gegen die Nacht-Information -- geht der Bruch nicht durch, liquidieren beide in dieselbe Richtung. Das Geld bleibt liegen, weil der Weg eine explizite Fehlschlag-Definition braucht, die kein Standard-ORB-Modul hat.
- **Engine-Weg:** Modul-Spec: as_side='against' plus Fehlschlag-Fenster in asian.py (~25 Zeilen, Muster mb_side='against' aus maband.py Z. 608-611).
- **Buch-Bezug:** neues Bein
- **Verwandte Tote / Vorlauf:** #068 (Retest-Variante falsifiziert -- anderer Mechanismus, gleiche Gegend); **`fb01_failbreak_session_NQ/RTY` und `fb01b_failbreak_fixed_NQ/RTY` (alle vier `premise_failed`)**; `i2 on_rev` als lebende Verwandte (94 Trials / 9 Surv, kein Null-Schalter). Schwesterkarte: SES-W26 fuehrt denselben Mechanismus als "offen, kontaminiert".
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W6

**Bewegung:** Preis bricht das NY-OR-Level, kommt zurueck und laeuft am Level entlang (Retest-Einstieg).

- **Etikett / Rolle:** Trend / Signal
- **Stand:** tot (#068: Pineda-Retest auf NQ, alle 36 Varianten OOS/2025+ negativ; `orb_exec='retest'` existiert seit #068). **Nummer korrigiert 21.09.2026:** die IVB-Retest-Falsifikation steht in **#083** ("IVB-Nachtest mit exakter Paper-Spec: auch die Original-Regeln haben keine Edge" -- IVB bleibt Friedhof, jetzt endgueltig) bzw. **#079**, **nicht in #164** (#164 = TWAP-Modul-Entscheidung, ein voellig anderes Thema). Das Urteil "tot" haelt, die Beweiskette stimmte nicht.
- **Story:** Story existiert (wer den Ausbruch verpasst hat, kauft den Rueckfall), ist aber zweimal ehrlich falsifiziert -- einmal als Pineda-Retest (#068), einmal als Valentini/IVB-Retest (#083/#079). Ohne einen neuen Grund, der ueber 'diesmal mit Nacht-Filter' hinausgeht, kein Skelett.
- **Engine-Weg:** engine-faehig: orb orb_exec='retest' (qbt.py Z. 618)
- **Buch-Bezug:** keiner
- **Verwandte Tote:** #068, **#083** (IVB mit exakter Paper-Spec ohne Edge), **#079** (nur der Delta-Beifang `OR_DELTA_BIAS_NQ` ueberlebt, LONG)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W7

**Bewegung:** Preis laeuft vom Cash-Open einfach weg (Opening-Drive ohne Level), aber nur an Tagen mit echter Nacht-Preisfindung.

- **Etikett / Rolle:** Trend / Signal
- **Stand (Zahlen korrigiert 21.09.2026, `verdict-auditor`):** gemessen ohne Kandidat. `on01_cashopen_decision_NQ` = **71 Trials / 28 Survivors** / 0 Kandidaten (Karte hatte 72/18 -- die "18" war die GROESSE einer Zelle, nicht die Survivor-Zahl; die Schwesterkarte SES-W12 fuehrt korrekt 71). Zellen: `on_ret_min 0,0025` **13/18**, ungegatet **10/17**, `on_ret_min 0,0045` **5/18**, `on_ret_max 0,0025` **0/18**. Gate-Zellen mit OOS-Edge 7-13 %, ungegatete Zelle 6-9 %.
- **Story:** Die Nacht-Preisfindung in Index-Futures laeuft ohne US-Cash-Liquiditaet. Hat sie eine echte Bewegung produziert, MUSS der US-Open dazu Stellung nehmen, und diese Stellungnahme ist gerichtet und schnell. War die Nacht ruhig, ist der Open nur Rauschen. Das Geld bleibt liegen, weil die meisten Opening-Drive-Systeme jeden Tag handeln statt nur die Entscheidungstage. Belegter Teil: das Gate-Ergebnis existiert bereits im Register und faellt in die richtige Richtung.
- **Engine-Weg:** engine-faehig: tsmom tm_on_ret_min (sigcore.py Z. 1169-1171), Ersatz-Semantik wie ON01
- **Buch-Bezug:** Ersatz fuer NQ_Momentum_d260818
- **Verwandte Tote (korrigiert 21.09.2026 -- "keine Leiche" war falsch):** `mode='firstbar_ematrail'` ist **derselbe Mechanismus ohne Level** (erste 5-Minuten-Kerze der NY-Session gegen die EMA12, Stop an der Erstkerze, EMA-Trail) und hat **2.880 NQ-Register-Trials**; in `ideas.json` auf **allen vier Maerkten** als "Getoetet" gefuehrt. Splits: `ny`/`ema_basis=24h` **960 Trials / 109 Survivors**, `ny`/`rth` 960 / **0**, `eu`/`24h` 960 / **0**. Der Opening-Drive ohne Level ist damit massiv vorbelegt, und der einzige Split mit Survivors ist der 24h-EMA-Arm -- also genau der, der die Nacht ueberhaupt in die Basis nimmt. Das ist ein Hinweis fuer Rang 1, kein Gegenbeweis. ACHTUNG bleibt: der Folge-Job `gen_tsmom_combo_mom_NQ_exits_09032135` hat ausgerechnet die UNGEGATETE Zelle weiteroptimiert.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W8

**Bewegung:** Preis durchquert die NY-OR von einer Seite zur anderen und bleibt drin (Range-Tag), nach enger Nacht.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** offen (0 Trials)
- **Story:** Wenn die Nacht nichts entschieden hat, ist der Vormittag eine Zwei-Seiten-Auktion zwischen den OR-Grenzen. Dann verdient nicht der Bruch, sondern das Hin und Her. Das Geld bleibt liegen, weil Range-Handel in einem Trailing-DD-Kaefig nur mit sehr engem Risiko zu rechtfertigen ist und deshalb selten systematisch gebaut wird. Schwachstelle der Story: die Kosten-Schwelle (MNQ-Round-Trip rund 2 Punkte) frisst kleine OR-Durchquerungen.
- **Engine-Weg:** Modul-Spec: on_range-Kennzahl plus ein Range-Handels-Modus; nichts davon existiert.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** #043 (Frequenz-Bein: hohe Frequenz braucht strukturell schaerferen Filter)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W9

**Bewegung:** Die NY-OR ist eng im Verhaeltnis zur Overnight-Range -- Kompressionsverhaeltnis statt absolute Breite.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials; Verhaeltnis-Kennzahl existiert nirgends)
- **Story:** Eine OR, die nach einer weiten Nacht eng ist, heisst: der Markt hat die neue Bewertung schon nachts gefunden und wartet am Morgen nur. Das ist ein anderer Zustand als 'beides eng'. Das Geld bleibt liegen, weil alle gaengigen Kompressions-Masse (NR7, ATR-Expansion) innerhalb des RTH-Tages rechnen und die Nacht ignorieren. Warnung: TB-03/#138 hat gemessen, dass Kompression bei uns KLEINERE Folgebewegung bedeutet -- dieser Weg muss sich davon abgrenzen, nicht darauf aufbauen.
- **Engine-Weg:** Modul-Spec: on_range + Verhaeltnis zu or_range in sigcore.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** #138 (TB-03 Kompression: Bewegung danach in ATR-Einheiten kleiner, CI klar getrennt)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W10

**Bewegung:** Preis bricht nach oben durch das London-OR-High, in Richtung der Asien-Session.

- **Etikett / Rolle:** Trend / Signal
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **Die Abgrenzung zu #028 trug nicht.** #028 woertlich: "London-Breakout (alle Varianten inkl. NR-Filter + **London-IB**, 46 Configs!)" -- London-IB IST die London-eigene Range, sie ist mitgetoetet. Die Behauptung, #028 habe nur den ASIEN-Range-Break bei London-Open getroffen, war falsch. **Neu ist allein die Asien-Richtungsbedingung**, und nur so darf der Why formuliert werden, sonst ist der Weg ein Aufwaermen (#211-Muster). Zweiter neuer Befund: `firstbar_ematrail` mit `session='eu'` hat **960 Register-Trials mit 0 Survivors** (gegen `ny`/24h 109/960) -- derselbe Opening-Drive-Mechanismus ist im Europa-Fenster 960-fach ohne einen einzigen Survivor gelaufen. Das senkt die Erwartung fuer W10-W14 und die Einstufung des London-Skeletts deutlich. `asia_mode='break'` hat weiterhin 2 Register-Trials, `rs 03:00-03:30` weiterhin 0.
- **Story:** Um 03:00 ET oeffnet London und uebernimmt ein Buch, das acht Stunden lang in Asien gelaufen ist. Die ersten 30 Minuten sind die Preisfindung dieser Uebergabe. Laeuft sie in Asiens Richtung weiter, ist das eine Bestaetigung durch die groessere Kohorte. Das Geld bleibt liegen, weil das Fenster fuer US-Trader unbequem ist und weil die Standard-Lore ('Asia-Range brechen bei London') nachweislich nicht traegt -- das ist aber eine ANDERE Behauptung als die hier.
- **Engine-Weg:** engine-faehig: asian.trades asia_mode='break', rs_start='03:00', rs_end='03:30', tr_start='03:30', tr_end='09:25' (asian.py Z. 73-76, 132-156); Overnight-Bedingung braucht die Spec aus W1.
- **Buch-Bezug:** neues Bein (Live-Buch-Merker bei duennen Fills)
- **Verwandte Tote / Vorlauf (21.09. erweitert):** #028 (London-Breakout in allen Varianten getoetet, **inklusive London-IB**, 46 Configs), `ideas.json` "Asian Range Breakout @ London (alle Varianten)" = Getoetet, `firstbar_ematrail` `session='eu'` (960 Trials, 0 Surv). **Fertige Job-Dateien liegen seit dem 21./25.08. bereit und waren in der Karte nicht genannt:** `260821_asian_EUbreak_NQ.json` (gelaufen, 17 Trials), `260821_asian_EUdir_NQ.json` (gelaufen, 18 Trials), `260825_eusession_break_ES.json` (**`premise_failed`**). Der Europa-Ast ist also nicht ungetestet, und eine Uebertragung auf ES ist bereits an der Praemisse gestorben.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W11

**Bewegung:** Preis bricht nach unten durch das London-OR-Low, in Richtung der Asien-Session.

- **Etikett / Rolle:** Trend / Signal
- **Stand (korrigiert 21.09.2026):** wie W10 inklusive der #028-Korrektur (London-IB mitgetoetet) und des Europa-Nullbefunds (`firstbar_ematrail` `eu` 960/0). Short-Seite im London-Fenster weiterhin nie getrennt gemessen.
- **Story:** Spiegel zu W10. Eigene Berechtigung, weil die europaeische Eroeffnung ueberwiegend Absicherungs- und Risikoabbau-Flow ist und damit nach unten dringlicher als nach oben. Long-Bias-Kontrolle ist hier besonders wichtig, weil das RTH-Long-Drift-Argument im London-Fenster gar nicht greift.
- **Engine-Weg:** engine-faehig: wie W10 plus Seiten-Trennung; ctl_sides Pflicht.
- **Buch-Bezug:** neues Bein (Live-Buch-Merker)
- **Verwandte Tote:** #028, #036
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W12

**Bewegung:** Preis prallt an der London-OR ab und dreht, wenn Asien richtungslos war.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** offen (0 Trials)
- **Story:** Spiegelbild von W10 auf der anderen Nacht-Bedingung: ohne Asien-Richtung ist die London-Eroeffnung keine Uebergabe, sondern ein Liquiditaetswechsel ohne Information. Dann sind die ersten 30 Minuten ein Ueberschiessen, das zurueckkommt. Das Geld bleibt liegen, weil der Weg nur an einem Teil der Tage existiert und ohne Nacht-Klassifikation im Rauschen verschwindet.
- **Engine-Weg:** Modul-Spec: asian.py braucht as_on_dir/as_on_ret_max (Nacht-Bedingung) plus einen Fade-Arm fuer beliebige Fenster (fade_us ist auf den US-Open verdrahtet, asian.py Z. 159).
- **Buch-Bezug:** neues Bein (Live-Buch-Merker)
- **Verwandte Tote:** #028, ideas.json 'RTY/NQ Asia-Fade am US-Open' (KILL)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W13

**Bewegung:** Preis kreuzt die London-OR, scheitert und dreht -- Fehlausbruch bis zum NY-Open.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** offen (0 Trials)
- **Story:** Gleicher Mechanismus wie W5, aber im duenneren Buch: ein gescheiterter Bruch in duenner Liquiditaet raeumt mehr Stops ab, weil weniger Gegenseite da ist. Das Geld bleibt liegen, weil genau diese duenne Liquiditaet auch die Fills verschlechtert -- die Story und ihr Killer sind dieselbe Tatsache. Vor jedem Test muss slippage_ticks=2.0 gesetzt sein (Muster TN-10).
- **Engine-Weg:** Modul-Spec: as_side='against' plus Fehlschlag-Fenster (wie W5), im London-Fenster.
- **Buch-Bezug:** neues Bein (Live-Buch-Merker)
- **Verwandte Tote:** #028, #033 (doppelte Kosten toeten enge Spreads)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W14

**Bewegung:** Preis bricht die London-OR ohne jede Nacht-Bedingung -- der reine Lore-Weg.

- **Etikett / Rolle:** Trend / Signal
- **Stand:** tot (#028: London-Break, Hold-Variante, NR-Filter, London-IB, ES-Variante, 46 Configs alle durchgefallen)
- **Story:** Keine neue Story. Steht hier nur, damit sichtbar ist, dass W10-W13 sich von diesem Weg durch die Nacht-Bedingung unterscheiden muessen und nicht durch Reparametrisierung.
- **Engine-Weg:** engine-faehig, aber ohne neuen Grund kein Test.
- **Buch-Bezug:** keiner
- **Verwandte Tote:** #028
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W15

**Bewegung:** Preis bricht im RTH nach oben durch das Overnight-High.

- **Etikett / Rolle:** Trend / Level
- **Stand:** gemessen ohne Kandidat (asia_mode='break_us': 44 Trials, 16 Survivors, 0 Kandidaten; ideas.json 'NQ Asian-Levels RTH-Breakout' = validiert, aber duenn: OOS +1,2 %, PF 1,07)
- **Story:** Das Nacht-Hoch ist der Preis, an dem die Nacht-Kohorte zuletzt Verkaeufer gefunden hat. Wird er im RTH mit US-Liquiditaet genommen, ist die Nacht-Obergrenze widerlegt und die dort sitzenden Shorts muessen decken. Das Geld bleibt liegen, weil das Level so offensichtlich ist, dass die Bewegung meist schon in der Bruchbar passiert -- exakt die #068-Falle.
- **Engine-Weg:** engine-faehig: asian asia_mode='break_us', rs 19:00-03:00 oder 03:00-09:25, tr 09:30-15:55 (asian.py); ctl_null vorhanden.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** #028 (Fill-Bug-Lehre: Stop-Order fuellt bei Gap am Open, nicht am Level), #068
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W16

**Bewegung:** Preis bricht im RTH nach unten durch das Overnight-Low.

- **Etikett / Rolle:** Trend / Level
- **Stand:** gemessen ohne Kandidat (Teil der 44 break_us-Trials, Seiten nie getrennt ausgewertet)
- **Story:** Spiegel zu W15 mit anderer Kohorte (Risikoabbau statt Aufbau). Die getrennte Messung fehlt komplett; bei ORB hat sich genau diese Trennung als ergebnisrelevant erwiesen (#036).
- **Engine-Weg:** engine-faehig wie W15 plus Seiten-Trennung.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** #036
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W17

**Bewegung:** RTH eroeffnet ausserhalb der Overnight-Range und laeuft zurueck hinein.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **"tot" war zu hart -- richtig ist "duenn gemessen".** `asia_mode='fade_us'` hat **8** Register-Trials; das sind keine zehn Implementierungen und damit kein Tot-Stempel nach "Hypothese vor Urteil". Die Transfer-Jobs `gen_i2_on_rev_ES/RTY/YM` und `gen_asian_fade_break_ES/RTY` stehen auf **`premise_failed`** -- der Fade-Ast ist ausserhalb NQ **nie gerechnet** worden. Die lebende Verwandte `i2 on_rev` hat **9 von 94** Survivors. Das `ideas.json`-KILL ("RTY/NQ Asia-Fade am US-Open") bleibt als Urteil fuer NQ und RTY stehen, deckt aber weder ES/YM noch die 8-Trial-Duenne ab.
- **Story:** Story existiert (Ueberschiessen der duennen Nacht wird vom liquiden Open korrigiert) und ist die naechste Verwandte des validierten Overnight-Reversal-Bankfunds. Als Asia-Fade auf NQ/RTY ehrlich getoetet, auf ES/YM nie gemessen. Ein neuer Grund muesste erklaeren, warum die i2-Variante (`on_rev`, 9/94 Survivors) lebt und diese nicht. **Kein Skelett in dieser Runde**, aber der Stand darf nicht "tot" heissen.
- **Engine-Weg:** engine-faehig: asian asia_mode='fade_us'; i2 i2_mode='on_rev' ist die lebende Verwandte (94 Trials, 9 Survivors), hat aber keinen Null-Schalter.
- **Buch-Bezug:** keiner
- **Verwandte Tote / nie gerechnet:** `ideas.json` "RTY/NQ Asia-Fade am US-Open" (KILL, NQ+RTY), #056 (Overnight-Reversal, Bank). **Nie gerechnet (`premise_failed`):** `gen_i2_on_rev_ES`, `gen_i2_on_rev_RTY`, `gen_i2_on_rev_YM`, `gen_asian_fade_break_ES`, `gen_asian_fade_break_RTY`.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W18

**Bewegung:** Preis laeuft im RTH hin zum Overnight-High/-Low als Ziel -- das Nacht-Extrem als Exit, nicht als Einstieg.

- **Etikett / Rolle:** Mean Reversion / Exit
- **Stand:** offen (0 Trials; alle bisherigen Exit-Sweeps nutzen nur Zeit, R-Vielfache und ATR)
- **Story:** Ein Trade, der am Morgen in Richtung Nacht-Extrem laeuft, hat dort sein natuerliches erstes Widerstands-Cluster. Ein Ziel AM Level ist etwas anderes als ein Ziel bei 1R, weil es die Marktstruktur statt die eigene Risikogroesse benutzt. Das Geld bleibt liegen, weil der Exit-Raum bei uns nachweislich der am wenigsten ausgereizte Hebel ist (**#050**, Zitat: "Der **Exit-Raum** war der eigentliche Hebel, nicht ein neuer Mechanismus") und Level-Ziele dort nie vorkamen. **Korrektur 21.09.2026:** die urspruenglich zitierte Nummer **#187 existiert nicht** -- das Strategie-Logbuch endet bei #168. Belegt ist der Satz in #050.
- **Engine-Weg:** Modul-Spec: Level-basiertes Ziel als Exit-Profil (on_high/on_low als Zielpreis) -- betrifft qbt.run_strategy und die Exit-Achse, nicht ein Signal-Modul.
- **Buch-Bezug:** Ersatz-Exit fuer jedes der drei Buch-Beine
- **Verwandte Tote:** #046 (BE/Trail-Overlays: 0 von 8 Beinen ueberlebt OOS) -- Abgrenzung: hier ein Level-Ziel, kein Trail
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W19

**Bewegung:** Preis kreuzt die Mitte der Overnight-Range und haelt sie.

- **Etikett / Rolle:** Intraday Bias / Level
- **Stand:** offen (0 Trials)
- **Story:** Keine eigene Story, weil die **geometrische** Nacht-Mitte kein Ort ist, an dem jemand handeln musste -- anders als High, Low oder Cash-Open. Ohne Zwangshandel kein Mechanismus. Steht hier zur Vollstaendigkeit; wenn ueberhaupt, ist sie ein Zustandsmass (oberhalb/unterhalb) und damit ein Spezialfall von W34.
- **Abgrenzung, nachgetragen 21.09.2026:** dieses Argument trifft auf den **volumengewichteten** Schwerpunkt der Nacht (Overnight-VWAP/POC/TWAP) ausdruecklich NICHT zu -- dort hat jemand tatsaechlich Volumen abgewickelt. Das ist jetzt ein eigener Weg: **[[#W41]]**.
- **Engine-Weg:** kein Weg noetig; faellt unter W34 (on_pos).
- **Buch-Bezug:** keiner
- **Verwandte Tote:** keine
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W20

**Bewegung:** Preis laeuft am Overnight-High/-Low entlang, ohne es zu brechen (Absorption am Nacht-Extrem).

- **Etikett / Rolle:** Mean Reversion / Filter
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **offen. Die Entwertung ist zurueckgezogen und stand ausserdem auf der falschen Nummer.** Der Placebo-Vergleich steht in **#138** (AB-14), nicht in #137 (#137 = AP116-Bestandsdurchlauf). Und **#151 Befund 3** hat ihn zurueckgezogen: "Das Uplift-Urteil stand auf einer heute gesperrten Null, der Zufallslevel-Arm (`random_level_shift`, ungerundet) ist nach Lehre 151 kontaminiert. Der Satz **'Verhalten am Zufallslevel identisch' ist nicht mehr gedeckt**." Roh/grob: echt k3/k4 35,8/31,7 % gegen Zufall 38,6/36,2 %; k-Steigung echt -4,8 gegen Zufall +0,1 pp.
- **Story (nachgetragen):** Ein Preis, der am Nacht-Extrem entlanglaeuft statt es zu brechen, zeigt, dass dort jemand mit Groesse absorbiert -- das ist der Gegenzustand zum Sweep (W39) und damit dessen Kontrollarm. Die Story war nie schwach, sie war nur durch einen inzwischen zurueckgezogenen Befund blockiert. **Was bleibt:** ohne tick-treues Placebo (Lehre 151, `random_level_shift` verlangt jetzt `tick`) ist hier kein Urteil moeglich, in keine Richtung.
- **Engine-Weg (korrigiert):** **`mb_band_evt='walk'` existiert** (`maband.py` Z. 71 und Z. 376, 6 Register-Trials) -- die Schwesterkarte fuehrt ihn unter SES-W47 korrekt als vorhanden. Die alte Aussage "kein Weg noetig" war falsch. Fuer das Nacht-Extrem als Schiene fehlt nur die Level-Quelle (S4/S5-Umfeld).
- **Buch-Bezug:** keiner bis zum tick-treuen Placebo-Lauf
- **Verwandte Tote:** **#138** (AB-14, Placebo-Vergleich -- **von #151 zurueckgezogen**), #151 Lehre 151 (Placebo braucht dieselbe Diskretisierung wie das echte Level), #113/#112 (Value-Area-Reversal als Barrieren-Artefakt, gleiche Fehlerklasse)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W21

**Bewegung:** Preis laeuft hin zum Vortages-Schluss und fuellt den Gap.

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** gemessen, gemischt (mode='gap' gap_side='fade': 344 Trials, Grossteil der 143 gap-Survivors; RTY_Gap-fade war Buch-Bein bis #130, NQ-Gap-fade in ideas.json als tot gefuehrt, Zahl aber von AP116 korrigiert)
- **Story:** Ein Gap ist eine Neubewertung ohne Handelspfad. Wer sie nicht mitgemacht hat, bekommt sie beim Open angeboten und nimmt sie -- das zieht zurueck. Bei Index-Futures ist der Effekt dokumentiert schwach (Falsifikation auf MNQ), auf RTY war er lange ein Bein. Das Geld liegt hier nicht mehr frei herum, der Weg ist gut besetzt.
- **Engine-Weg:** engine-faehig: mode='gap' -- ABER gap steht nicht in controls.ctl_null (Z. 689-691), kann also nie deploy_ready werden.
- **Buch-Bezug:** Ersatz fuer RTY_Gap-fade (Bein bereits raus) oder neues Bein
- **Verwandte Tote:** #130 (RTY_Gap-fade zum Abschuss freigegeben), #038 (Retune), ideas.json 'Overnight-Gap-Fade' + 'Gap-Fade klein' (getoetet, AP116-Korrektur)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W22

**Bewegung:** Preis laeuft weg vom Vortages-Schluss und erweitert den Gap.

- **Etikett / Rolle:** Trend / Signal
- **Stand:** gemessen ohne Kandidat (mode='gap' gap_side='continuation': 53 Trials; ideas.json 'Gap-Continuation (grosse Gaps)' = validiert, D-Note, 17 Trades/Jahr)
- **Story:** Ein grosser Gap ist keine Verirrung, sondern eine Nachricht. Dann ist nicht die Rueckkehr das Geschaeft, sondern die Anpassung der Portfolios an die neue Bewertung, die den ganzen Tag dauert. Das Geld bleibt liegen, weil die Trefferzahl mit 17/Jahr zu klein ist, um allein zu tragen -- als Gate auf einen bestehenden Ausbruchsweg (W23) ist es wertvoller als als eigenes Bein.
- **Engine-Weg:** engine-faehig: mode='gap' gap_side='continuation'; kein Null-Schalter (siehe W21).
- **Buch-Bezug:** neues Bein, realistischer: Gate fuer W1/W2
- **Verwandte Tote:** ideas.json 'Gap-Continuation' (validiert, informell verworfen)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W23

**Bewegung:** Die Gap-Groesse wirkt nur als Tor auf die Opening-Range-Wege, nicht als eigenes Signal.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (gap_pct_max existiert in qbt._orb_trades Z. 513-518 und hat NULL Register-Trials; das tsmom-Pendant tm_gap_max hat 36 Trials, ist aber mit tm_on_ret_max identisch, siehe Randbedingung 3)
- **Story:** Ein sehr grosser Gap macht die Opening Range mechanisch breit und das Risiko je Trade gross, ohne die Trefferwahrscheinlichkeit zu heben -- ein Deckel ist dann eine Risiko-Entscheidung, keine Prognose. Umgekehrt ist ein Mindest-Gap die Bedingung dafuer, dass ueberhaupt etwas zu entscheiden war. Das Geld bleibt liegen, weil der Parameter seit Monaten in der Engine steht und nie eingeschaltet wurde.
- **Engine-Weg:** engine-faehig im orb-Modus (aber ohne Null-Schalter); sauber erst nach der Trennung gap != on_ret in sigcore.daily_context.
- **Buch-Bezug:** Gate fuer W1/W2/W7, kein eigenes Bein
- **Verwandte Tote:** keine
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W24

**Bewegung:** Die Nacht steigt, also werden am NY-Open nur Long-Ausbrueche zugelassen.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials; das vorhandene Gate ist unsigniert -- sigcore.py Z. 1163-1171 nehmen ueberall abs())
- **Story:** Die Richtung der Nacht ist die Positionierung, mit der die US-Sitzung startet. Ein Ausbruch mit dieser Positionierung hat die schon vorhandenen Halter im Ruecken, ein Ausbruch dagegen muss sie erst umdrehen. Das Geld bleibt liegen, weil unsere gesamte Engine die Nacht bisher nur als GROESSE kennt und nie als RICHTUNG hat filtern koennen -- die 145 tm_base='overnight'-Trials benutzen sie als Signal, nicht als Tor.
- **Engine-Weg:** Modul-Spec: signiertes Gate tm_on_dir in {'agree','against'} -- muss nach der Richtungsbestimmung greifen, also in tsmom._trades statt in sigcore.gates_pass (~20 Zeilen).
- **Buch-Bezug:** Ersatz fuer NQ_Momentum_d260818
- **Verwandte Tote (Zuordnung korrigiert 21.09.2026):** die 145 `tm_base='overnight'`-Trials (0 Survivors) setzen sich aus **TN-01 97** (`hyp_TN01_ES` 49 + `hyp_TN01_NQ` 48), **TN-12 25**, **TN-09 21**, **TN-03 1** und **CR-02 1** zusammen -- nicht aus "TN-01/TN-03/TN-12". **TN-03 hat exakt EINEN Register-Trial**, und `hyp_TN03_NQ` steht auf `premise_failed`. Die Nacht-Richtung ist als Signal also sehr ungleich gemessen: TN-01 und TN-12 tragen 122 der 145 Trials, TN-03 (der Tug-of-War, jetzt [[#W40]]) praktisch nichts. Ebenfalls `premise_failed` und nie gerechnet: `hyp_TN05_NQ`, `hyp_TN10_NQ`, `hyp_CR02_ES`, `hyp_AB11_NQ`. Unterschied zu diesem Weg bleibt: dort SIGNAL, hier TOR.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W25

**Bewegung:** Die Nacht faellt, also werden am NY-Open nur Short-Ausbrueche zugelassen.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials, gleiche Luecke wie W24)
- **Story:** Spiegel zu W24, eigenstaendig, weil die Index-Long-Drift die Short-Seite strukturell benachteiligt (#036) und ein Nacht-Filter genau dort den groessten Unterschied machen muesste, wenn er echt ist. Faellt der Filter auf der Short-Seite durch, waehrend er long traegt, ist er wahrscheinlich nur Drift.
- **Engine-Weg:** Modul-Spec wie W24; ctl_sides als Pflichtkontrolle.
- **Buch-Bezug:** Ersatz fuer NQ_Momentum_d260818
- **Verwandte Tote:** #036
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W26

**Bewegung:** Nacht-Richtung und Ausbruchsrichtung widersprechen sich, also wird gar nicht gehandelt.

- **Etikett / Rolle:** Filter / Filter
- **Stand:** offen (0 Trials)
- **Story:** Der billigste Weg, Geld zu verdienen, ist, die teuersten Trades nicht zu machen. Ein Ausbruch gegen die Nacht-Positionierung ist derselbe Trade wie W5, nur aus Sicht des Ausbruch-Haendlers. Das Geld bleibt liegen, weil ein Veto keine neue Strategie ist und deshalb nie als eigener Job formuliert wird -- gemessen wird es trotzdem sauber, als Gegenprobe zu W24/W25.
- **Engine-Weg:** Modul-Spec wie W24 (derselbe Schalter, anderer Wert).
- **Buch-Bezug:** Ersatz-Overlay auf alle drei Buch-Beine
- **Verwandte Tote:** keine
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W27

**Bewegung:** Die Nacht dreht in sich: Asien laeuft hoch, London laeuft runter -- der Tag wird ein Reversal-Tag.

- **Etikett / Rolle:** Mean Reversion / Filter
- **Stand:** offen (0 Trials; Segment-Trennung Asien/Europa existiert in sigcore gar nicht, asian.py kann die Fenster nur EINZELN rechnen)
- **Story:** Wenn zwei Kohorten in derselben Nacht gegeneinander handeln, ist keine Bewertung gefunden worden, und die US-Sitzung beginnt ohne Konsens. Genau dann ist der erste Ausbruch am wahrscheinlichsten ein Fehlausbruch. Das Geld bleibt liegen, weil unsere Engine die Nacht als EINE Zahl (on_ret) fuehrt und den internen Widerspruch damit per Konstruktion nicht sehen kann.
- **Engine-Weg:** Modul-Spec: asia_ret/eu_ret als getrennte Tageskontext-Spalten in sigcore (aus asian.load_full, ~40 Zeilen) plus Gate.
- **Buch-Bezug:** Ersatz-Filter fuer NQ_Asia-Dir-USopen_d260820
- **Verwandte Tote / Bank-Zeilen (21.09. nachgetragen):** TN-08 (Europa-Richtung als besserer Bias, 37 Trials im `asian`-Modus, 0 Kandidaten). **Fehlten in der ersten Fassung:** **XA-39** ("Europa-Session-Rendite ist ein besserer RTH-Praediktor als die Asien-Rendite, weil europaeische Haeuser ES aktiv hedgen" -- die Bank-Zeile zur Segment-Frage, Pruefplan ist eine Regression mit beiden Segmenten als getrennte Praediktoren) und **MO-51** ("Drift-Richtung der letzten Globex-Stunde 08:30-09:30 gegen die erste RTH-Stunde", jetzt eigener Weg [[#W45]]). **Pflicht-Split, der hier fehlte:** TN-09 / [[#W42]] -- der Montags-Overnight ist ein anderer Prozess.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W28

**Bewegung:** Die Nacht-Richtung setzt sich im RTH einfach fort, ohne dass ein Level gebrochen werden muss.

- **Etikett / Rolle:** Intraday Bias / Signal
- **Stand:** im Buch (NQ_Asia-Dir-USopen_d260820, asian asia_mode='us_dir', 245 us_dir-Trials, 52 Survivors)
- **Story:** Das ist das Bestandsbein: klare Asien-Richtung (Bewegung >= 0,8x Range) -> am US-Open mit ihr, EOD-Exit. Die Story ist belegt und im Buch bezahlt. Fuer diese Karte ist der Weg wichtig als Ersatz-Slot: alles, was die Nacht-Richtung besser nutzt als 'einfach mitlaufen', konkurriert hier und nicht um einen neuen Platz.
- **Engine-Weg:** engine-faehig, laeuft live.
- **Buch-Bezug:** besetzt -- Ersatz-Slot fuer W24/W25/W27/W32/W34
- **Verwandte Tote:** #028 (VERDICT A), #128 (Asia_d260820 promotet), #141/AR-20 (Einzelkonfiguration unter der Familien-Decke, 87,7 % aus einer COVID-Episode)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W29

**Bewegung:** Die Nacht war weit (grosse Range), also traegt der Ausbruch am Morgen.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials; on_range existiert als Kennzahl nicht, sigcore.daily_context kennt nur gap/on_ret)
- **Story:** Overnight-Volatilitaet sagt die Intraday-Volatilitaet desselben Tages stark voraus -- peer-reviewed und unabhaengig repliziert, mehr als 40 % der Tagesvola entsteht nachts (Research-Cache, DN-SV-RV-Block). Hohe erwartete Intraday-Vola heisst groessere Ausbruchsdistanzen bei gleicher Kostenschwelle, also besseres Verhaeltnis fuer jeden Level-Bruch-Weg. Das Geld bleibt liegen, weil die Kennzahl bei uns schlicht nicht gerechnet wird.
- **Engine-Weg:** Modul-Spec: on_range/on_sigma in sigcore aus asian.load_full (~70 Zeilen inkl. Cache) plus Gates.
- **Buch-Bezug:** Gate fuer W1/W2/W7, Ersatz-Overlay auf NQ_Momentum
- **Verwandte Tote / Bank-Zeilen (21.09. nachgetragen):** #138 (TB-03: INTRADAY-Kompression -> kleinere Folgebewegung; hier Nacht statt Intraday, Abgrenzung Pflicht). **Fehlten:** **HV-44** ("breites Overnight-Value-Gebiet -> ORB-Ausbrueche zuverlaessiger als nach engem Overnight-Value" -- das ist woertlich dieser Weg, mit `orb_exec="close"` als Pruefplan), **HV-43** (Abstand Overnight-POC zum RTH-Open als besserer Gap-Fill-Praediktor als die Gapgroesse), **GM-15** ("Verhaeltnis Overnight-Range zu RTH-Range ist ab 2022 niedriger als davor, 0DTE-Verlagerung") -- **GM-15 ist zugleich die Kennzahl von [[#W9]] und eine Epochen-Warnung fuer die ganze Karte: jeder Nacht-Range-Test braucht einen Epochen-Split vor/ab 2022.** Dazu die gemessenen Tages-Verwandten zur Kompressionsfrage: **TV-03** ("kontrahierende Vola") und **AB-03** ("Squeeze", Crabel) -- zusammen im 229er-Block, 59 Survivors, 0 Kandidaten (Stand laut Schwesterkarte SES-W38).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W30

**Bewegung:** Die Nacht war eng, also scheitert der Ausbruch und der Tag wird eine Range.

- **Etikett / Rolle:** Mean Reversion / Filter
- **Stand:** offen (0 Trials), aber gegen einen eigenen Befund
- **Story:** Spiegel zu W29 und zugleich der Weg, bei dem wir am ehesten falsch liegen: TB-03/#138 hat auf unseren Daten gemessen, dass nach Kompression die Folgebewegung KLEINER ist, nicht dass sie dreht. 'Klein' ist aber genau die Bedingung fuer einen Fade, nicht fuer einen Breakout -- die Story ist damit nicht widerlegt, sondern gedreht. Das Geld bleibt liegen, weil wir aus #138 die falsche Lehre gezogen haben koennten (Kompression als tot statt als Fade-Bedingung).
- **Engine-Weg:** Modul-Spec wie W29, Fade-Arm.
- **Buch-Bezug:** Gate fuer W4/W8
- **Verwandte Tote:** #138 (TB-03, eng gestempelt), **TV-03** und **AB-03** (Tages-Kompression, gemessen, 0 Kandidaten -- Schwesterkarte SES-W38), **GM-15** (Epochen-Warnung: das Nacht/Tag-Range-Verhaeltnis hat sich ab 2022 verschoben)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W31

**Bewegung:** Die europaeische Nacht-Session hatte hohes Volumen, also wird der US-Tag trendig.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials; VV-19 steht als Bank-Zeile ungebaut da, on_rvol existiert nicht)
- **Story:** Nacht-Volumen misst, wie viele echte Institutionelle in Europa gearbeitet haben. Hohe Beteiligung heisst laufende Metaorders, die am US-Open nicht fertig sind und weiterarbeiten -- das ist der einzige Mechanismus im Konzept, der eine ANHALTENDE Kraft beschreibt statt einer einmaligen Reaktion. Das Geld bleibt liegen, weil Volumen-RVOL bei uns nur gegen den Uhrzeit-Median innerhalb des RTH gerechnet wird (sigcore), nie fuer Nacht-Fenster.
- **Engine-Weg:** Modul-Spec: on_rvol je Nacht-Segment gegen den 20-Tage-Median desselben Fensters (~30 Zeilen auf der W29-Basis).
- **Buch-Bezug:** Gate fuer W1/W2, Ersatz-Overlay NQ_Momentum
- **Verwandte Tote / Bank-Zeilen (21.09. nachgetragen):** VV-19 (ungebaut), #031 (RVOL als ORB-Filter bestaetigt -- aber intraday gerechnet). **Fehlten, und eine davon behauptet das Gegenteil:** **XA-42** ("Overnight-Bewegung mit hohem Globex-Volumen = Fortsetzung, mit niedrigem = Reversion -- das erklaert den bisher gescheiterten Overnight-Fade") ist woertlich dieser Weg; **MO-19** behauptet das **GEGENTEIL** ("nach Overnight-Sessions mit hohem Overnight-Volumen relativ zum Normal laeuft NQ in der ersten RTH-Stunde zurueck", Begruendung: Metaorder-Impact im duennen Buch) und ist damit der fehlende **Fade-Arm**; **MO-50** (gerichtete Drift in der europaeischen Kernzeit 03:00-08:00 bei erhoehtem Volumen -> Fortsetzung im US-Open). **Folge fuer das Skelett:** der Weg muss beide Vorzeichen als eine Messung fuehren (Fortsetzung XA-42/MO-50 gegen Reversion MO-19), sonst ist das Ergebnis egal welcher Richtung nur die Auswahl des passenden Priors.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W32

**Bewegung:** Die Nacht lief trendig statt hin und her (hohe Effizienz des Nacht-Pfades), also wird der RTH ein Trendtag.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen (0 Trials; TN-07 ungebaut, Efficiency Ratio existiert in sigcore nur fuer RTH-Fenster als tm_er_min, 297 Trials)
- **Story:** Ein trendiger Globex-Verlauf zeigt, dass jemand ueber Nacht durchgearbeitet hat, statt dass zwei Seiten sich abgewechselt haben. Das ist eine Aussage ueber die Art des Flows, nicht ueber seine Groesse -- und damit unabhaengig von on_ret (gross und choppy ist etwas anderes als gross und gerade). Das Geld bleibt liegen, weil on_ret beide Faelle zusammenwirft.
- **Engine-Weg:** Modul-Spec: on_er in sigcore (Wiederverwendung der vorhandenen ER-Formel auf das Nacht-Fenster, ~15 Zeilen auf der W29-Basis).
- **Buch-Bezug:** Ersatz-Filter fuer NQ_Asia-Dir-USopen (dessen asia_dir_thr ist der grobe Vorlaeufer)
- **Verwandte Tote:** TN-07 (ungebaut). **TN-06 (Gap gegen Globex-Pfadlaenge, Absorption) ist seit 21.09. ein eigener Weg: [[#W43]]** -- er gehoert nicht als Fussnote unter W32, weil "gross und choppy" dort ausdruecklich von "gross und gerade" getrennt wird und die Absorptions-Quadranten eine andere Kennzahl brauchen (Pfadlaenge gegen Sprung, nicht Effizienz).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W33

**Bewegung:** Die Nacht war volatil, also werden Stop und Ziel des Tages groesser gewaehlt -- Skalierung statt Richtung.

- **Etikett / Rolle:** Trend / Exit
- **Stand:** offen (0 Trials; TV-11 ungebaut, alle Stop-Skalen laufen ueber Vortages-ATR/Sigma)
- **Story:** Belegt, nicht vermutet: Overnight-Realized-Volatility sagt die Intraday-RV von S&P- und Nasdaq-Futures stark voraus, der Zusammenhang ist zeitlich asymmetrisch (Nacht -> folgender Tag, nicht umgekehrt) und unabhaengig repliziert (Research-Cache). Unsere Stops skalieren an der VORTAGES-Vola, also an der aelteren Information. Das Geld bleibt liegen, weil das kein Signal ist, sondern eine Risikogroesse -- und Risikogroessen werden selten als Alpha-Idee formuliert, obwohl der Exit-Raum bei uns der staerkste Hebel war (**#050**; die urspruenglich mitzitierte **#187 existiert nicht**, das Logbuch endet bei #168 -- korrigiert 21.09.2026).
- **Engine-Weg:** Modul-Spec: tm_stop_mode='on_sigma' auf der W29-Basis (~12 Zeilen, sobald on_sigma existiert).
- **Buch-Bezug:** Ersatz-Overlay auf alle drei Buch-Beine (v2-Passquote direkt ueber die Pfad-Varianz)
- **Verwandte Tote:** #046 (BE/Trail: 0 von 8 ueberlebt) -- Abgrenzung: hier Stop-SKALA vorab, kein nachlaufender Eingriff; #157 (be_trail auf v2 +2,95 pp mit weitem CI)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W34

**Bewegung:** Wo der Cash-Open innerhalb der Nacht-Range liegt (oben, unten, Mitte), bestimmt den Bias des Tages.

- **Etikett / Rolle:** Intraday Bias / Filter
- **Stand:** offen (0 Trials; on_pos existiert nicht)
- **Story:** Ein Open am oberen Rand der Nacht-Range heisst: jeder, der nachts gekauft hat, sitzt im Gewinn und kann verkaufen; jeder Short sitzt im Verlust und muss decken. Das ist eine Aussage ueber die Schmerzverteilung der Nacht-Kohorte und damit ueber die naechste erzwungene Order. Sie ist unabhaengig von on_ret: derselbe Nacht-Return kann oben oder mitten in der Range enden. Das Geld bleibt liegen, weil die Kennzahl bei uns fehlt.
- **Engine-Weg:** Modul-Spec: on_pos auf der W29-Basis (~10 Zeilen).
- **Buch-Bezug:** Ersatz-Filter fuer NQ_Asia-Dir-USopen_d260820
- **Verwandte Tote / Bank-Zeilen (21.09. nachgetragen):** #112/#113 (Value-Area-Reversal war ein Barrieren-Artefakt) -- Abgrenzung: `on_pos` ist ein Zustand am Open, kein Beruehrungs-Ereignis, das Placebo-Problem tritt hier nicht auf. **Fehlte:** **XA-38** ([[Hypothesen-Bank (Volumen & Flows)]]) ist **woertlich dieser Weg**: "Weil die Asien-Session Positionen aufbaut, die im US-RTH abgearbeitet werden, traegt die Asien-Range-Position des Preises beim US-Open (oberes oder unteres Drittel der Overnight-Range) Richtungsinformation fuer den RTH-Vormittag." Die erste Fassung schrieb "`on_pos` existiert nicht" und nannte keine Bank-Zeile -- die Zeile existiert seit Wochen samt Pruefplan (Terzile).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W35

**Bewegung:** Der Ausgang des London-ORB (durchgelaufen oder gescheitert) ist der Bias fuer den NY-ORB.

- **Etikett / Rolle:** Intraday Bias / Filter
- **Stand:** offen (0 Trials; zweistufig, kein Modul kann heute zwei Sessions verketten)
- **Story:** Der Kern von Max' Frage: die Nacht sagt nicht nur 'gross/klein', sondern hat am Morgen bereits EINEN Ausbruch durchgespielt. Ist er in London gelaufen, hat sich die Ausbruchs-Mechanik an diesem Tag als funktionsfaehig erwiesen, und die US-Wiederholung hat eine hoehere Vorwahrscheinlichkeit. Ist er gescheitert, ist der Tag ein Range-Tag, bevor der NY-Open ueberhaupt beginnt. Das Geld bleibt liegen, weil der Weg zwei Rechnungen hintereinander braucht und kein einzelner Job das heute abbilden kann.
- **Engine-Weg:** Modul-Spec: London-Ausgang als Tageskontext-Spalte (lon_break_ok) vorab berechnen und wie gex_rank joinen (~45 Zeilen), dann ein normales Gate.
- **Buch-Bezug:** Gate fuer W1/W2, kein eigenes Bein
- **Verwandte Tote:** #028 (London-Break selbst tot -- hier wird nicht der London-Trade gehandelt, sondern sein AUSGANG gelesen)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W36

**Bewegung:** Die London-Range (nicht die Asien-Range) dient als Level im NY-RTH.

- **Etikett / Rolle:** Intraday Bias / Level
- **Stand:** gemessen ohne Kandidat (break_us mit rs 03:00-09:25: 33 Trials, 15 Survivors, 0 Kandidaten)
- **Story:** Die Europa-Session ist zeitlich naeher am US-Open und hat die groesseren Teilnehmer als Asien, also sollte ihr Extrem das relevantere Level sein. Die Messung existiert bereits und hat mit 15 von 33 Survivors eine der hoechsten Survivor-Quoten im ganzen asian-Block -- aber nie einen Kandidaten. Das Geld liegt hier nicht frei, der Weg ist angetestet und an der Buch-Huerde gescheitert.
- **Engine-Weg:** engine-faehig: asian break_us rs_start='03:00', rs_end='09:25'.
- **Buch-Bezug:** neues Bein
- **Verwandte Tote:** TN-08 (Europa-Richtung, 37 Trials, 0 Kandidaten)
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W37

**Bewegung:** Position wird ueber Nacht gehalten, um den Overnight-Drift selbst zu ernten.  
**Swing-Zeile:** ja, Buch-Bezug ist Live-Buch-Merker, kein Prop-Buch-Job.

- **Etikett / Rolle:** Swing / Signal
- **Stand (korrigiert 21.09.2026, `verdict-auditor`):** **teil-tot**, nicht tot. #137 fuehrt "Boyarchenko-Overnight-Drift (**nur 3 Varianten, Mechanismus nie im richtigen Fenster im Register**)" ausdruecklich unter den Urteilen, deren Formulierung korrigiert werden musste -- "tot" widerspricht der eigenen Doku-Auflage. Die Schwesterkarte fuehrt denselben Weg als SES-W11 korrekt als teil-tot. `ideas.json` "Overnight-Drift 2-3h ET (Boyarchenko)" = Getoetet bleibt als Stempel fuer die drei gerechneten Fenster stehen. Bei E8 unabhaengig davon regelwidrig (kein Overnight-Halten, EOD-Zwangsschliessung).
- **Story:** Story ist gut dokumentiert (Dealer managen Inventar ueber Nacht, NY Fed Staff Report 917), aber das Folge-Papier desselben Teams heisst 'The Disappearing Overnight Drift'. Bei uns zweimal negativ gemessen. Bleibt als Swing-Zeile stehen, damit der Mechanismus nicht verloren geht, falls das Live-Konto kommt.
- **Engine-Weg:** engine-faehig: asian asia_mode='drift'.
- **Buch-Bezug:** Live-Buch-Merker, nicht Prop-Buch
- **Verwandte Tote:** #028, `ideas.json` "Overnight-Drift 2-3h ET (Boyarchenko)" (Getoetet), #137 (Formulierungs-Korrektur: nur 3 Varianten), Research-Cache (Liberty Street 2026, "The Disappearing Overnight Drift"). Schwesterkarte: SES-W11.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W38

**Bewegung:** Mehrere gleichgerichtete Naechte hintereinander bilden eine Kette und verstaerken den Bias.  
**Swing-Zeile:** ja, Buch-Bezug ist Live-Buch-Merker, kein Prop-Buch-Job.

- **Etikett / Rolle:** Swing / Filter
- **Stand:** offen (0 Trials; TN-11 ungebaut)
- **Story:** Eine mehrtaegige Metaorder arbeitet ueber mehrere Naechte. Drei gleichgerichtete Overnight-Returns sind dann kein dreifaches Rauschen, sondern eine Signatur. Der Weg ist per Konstruktion mehrtaegig im SIGNAL (nicht in der Haltedauer), also im Prop-Buch grundsaetzlich baubar -- er wird hier trotzdem als Swing gefuehrt, weil die Trefferzahl auf Tagesebene zu klein wird, um im Eval-Fenster zu tragen.
- **Engine-Weg:** engine-faehig im Prinzip (tm_base='overnight' mit Mehrtages-Fenster), Kennzahl on_ret_chain fehlt.
- **Buch-Bezug:** Live-Buch-Merker, nicht Prop-Buch
- **Verwandte Tote:** TN-11 (ungebaut), TN-01 (97 der 145 `tm_base='overnight'`-Trials, 0 Survivors). Schwesterkarte: SES-W10.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

---

## Nachgetragene Wege W39-W50 (21.09.2026)

### W39

**Bewegung:** Preis nimmt im RTH das Overnight-High/-Low, haelt es nicht und dreht -- der Sweep des Nacht-Extrems. (Element ON-High/Low x Relation "kreuzen und scheitern", beide Richtungen getrennt.)

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** **offen; der Mechanismus ist vorbereitet, aber nie gerechnet.** Vier Job-Dateien in `jobs_proposed` implementieren ihn als `maband mb_kind='channel'` + `mb_side='against'` (`260831_fb01_failbreak_NQ/RTY`, `260903_fb01b_failbreak_fixed_NQ/RTY`); alle vier tragen im File `"status": "pending"`, stehen in `queue.json` aber auf **`premise_failed`**. Lebende Verwandte: `i2 on_rev` 94 Trials / **9 Survivors**. Am **Nacht-Extrem** selbst: 0 Trials.
- **Warum die Zelle vorher leer war:** W5 deckt nur die NY-OR, W13 nur die London-OR, W17 ist "Open **ausserhalb** der Range" (ein Zustand **am Open**, kein Intraday-Ereignis). Der Sweep des Nacht-Hochs mitten im RTH hatte keine Zeile.
- **Story:** Das Overnight-High ist der einzige Preis, den alle Teilnehmer ohne Absprache gleich berechnen -- dort haengen die Stop-Orders der Nacht-Shorts und die Ausbruchs-Kaeufe der Tages-Kohorte im selben Cluster. Ein Ausfuehrungsalgo mit Groesse steuert diese ruhende Liquiditaet gezielt an, weil er sie sonst nirgends findet. Der Bruch entsteht dann **nicht aus Information, sondern aus dem Abraeumen der Stops**: danach ist das Buch jenseits des Levels leer, es gibt keinen Anschluss-Flow, und der Preis faellt zurueck. Das Geld bleibt liegen, weil es wie ein Ausbruch aussieht und von der ganzen Breakout-Kohorte gekauft wird.
- **Engine-Weg:** `asian.trades` `asia_mode='break_us'` liefert das Level (Nacht-Extrem) und hat `ctl_null` (43 Register-Trials). Der Fehlschlag-Arm fehlt: **Modul-Spec S5** (`as_side='against'` + `as_fail_win`) im `break_us`-Zweig, ~25 Zeilen, Muster `mb_side='against'` aus `maband.py` Z. 608-611. **Vorlauf-Pflicht:** zuerst die vier `fb01`/`fb01b`-Jobs reparieren und rechnen -- sie messen denselben Mechanismus am billigeren RTH-Kanal und sind an der Praemisse gestorben, nicht widerlegt.
- **Buch-Bezug:** neues Bein (`NQ_ONSweep`)
- **Verwandte Tote / nie gerechnet:** `fb01_failbreak_session_NQ/RTY`, `fb01b_failbreak_fixed_NQ/RTY` (alle `premise_failed`); #068 (nach erfolgreichem Bruch ist der Rest des Tages ein Coinflip -- das ist hier die **Praemisse**); Schwesterkarte SES-W26.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W40

**Bewegung:** Die Nacht-Richtung kehrt sich im RTH um, ohne dass ein Level gebrochen wird (Tug-of-War auf Tagesebene, Spiegel zu [[#W28]]).

- **Etikett / Rolle:** Mean Reversion / Signal
- **Stand:** **duenn gemessen.** Bank-Zeile **TN-03** ("Der eigentliche Tug-of-War: weil beide Segmente gegenlaeufig reverten, ist ein grosser positiver Overnight-Return ein negatives Vorzeichen fuer den folgenden RTH-Return") hat im Register **1 Trial**; `hyp_TN03_NQ` steht auf **`premise_failed`**, also nie gerechnet. Die Schwesterkarte fuehrt den Weg getrennt: **SES-W6a offen mit Auflage** (Reparatur TN-03, `prior='low'` + Prescan noetig), **SES-W6b durchgefallen**.
- **Warum die Zelle vorher leer war:** W28 fuehrt nur den **Fortsetzungs**-Arm. Die Relation "Richtung steigt/faellt x Richtung" verlangt beide Arme; die Karte hatte nur einen.
- **Story:** Wenn die Nacht-Kohorte in duenner Liquiditaet eine Bewertung durchgesetzt hat, ist der US-Open der erste Moment, in dem die groessere Kohorte widersprechen kann -- und sie widerspricht genau dann, wenn die Nacht-Bewegung ohne Volumen entstanden ist. Das ist derselbe Mechanismus wie beim validierten Overnight-Reversal, nur auf der Tages- statt der Ereignisebene.
- **Engine-Weg:** `tsmom` `tm_base='overnight'` mit invertiertem Vorzeichen (vorhanden, 145 Register-Trials) plus die Volumen-Bedingung aus [[#W31]] (Modul-Spec S1).
- **Buch-Bezug:** Ersatz-Arm zu `NQ_Asia-Dir-USopen_d260820`
- **Kein eigenes Skelett in dieser Runde:** der Weg laeuft bereits als **SES-W6a** in der Schwesterkarte, mit Auflage. Ein zweites Skelett waere Doppel-Messung und hebt die Zufallsdecke fuer beide Karten. Stattdessen: Verweis, und bei der Auswertung von SES-W6a wird der Stempel hier nachgetragen.
- **Verwandte Tote / nie gerechnet:** `hyp_TN03_NQ` (`premise_failed`, 1 Trial), TN-01/TN-12 (122 der 145 Trials, 0 Surv), SES-W6b (durchgefallen).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W41

**Bewegung:** Preis laeuft zum volumengewichteten Schwerpunkt der Nacht (Overnight-VWAP / Overnight-POC / Overnight-TWAP), hindurch oder prallt daran ab.

- **Etikett / Rolle:** Mean Reversion / Level
- **Stand:** **teilgemessen -- der Cross-Arm ist tot, der Rest ist offen.** #108 hat acht VWAP-Arten gegen ein Placebo gemessen; darunter **`on_frozen`** (Overnight-VWAP als festes Level) mit meanR **-0,042** und **`globex`** (VWAP ab 18:00 ET Vortag) mit **-0,036**. Keine schlaegt das Placebo, bester Abstand +0,011 (`globex`) bei 2/5 positiven Bloecken. **Diesen Befund hatten weder die erste Fassung der Karte noch der `verdict-auditor`.** Der POC-/TWAP-Arm und der Arm "hin zu, als **Ziel**" haben weiterhin 0 Trials.
- **Warum die Zelle vorher leer war:** [[#W19]] verwirft nur die **geometrische** Nacht-Mitte mit "kein Ort, an dem jemand handeln musste". Genau dieses Argument trifft den volumengewichteten Schwerpunkt nicht: dort wurde tatsaechlich Volumen abgewickelt. Die Bank hat dafuer **vier** Zeilen -- **AW-10** (Globex-VWAP als Tagesbias: Position des RTH-Open darueber/darunter), **TA-06** (Overnight-TWAP als Referenzpreis der Uebernacht-Positionen), **HV-08** (Overnight-POC als ueberdurchschnittlich oft getesteter Wendepunkt), **HV-43** (POC-Abstand als Gap-Fill-Praediktor). Die erste Fassung listete TA-06/HV-07/HV-08 im Inventar und gab ihnen dann keinen Weg.
- **Story:** Der Overnight-POC ist der Preis, an dem die Nacht-Positionen sitzen -- also der Einstand der Kohorte, die am Morgen entweder verteidigt oder aussteigt. Ein Open weit darueber heisst, die Nacht-Kaeufer sitzen im Gewinn. Das ist eine Aussage ueber erzwungene Orders. **Schwachstelle, die #108 offenlegt:** AW-10 sagt selbst als Verwerfungsgrund "das Signal ist zu ueber 80 % ein Gap-Proxy" -- und `gap` ist bei uns bitgleich mit `on_ret` (Randbedingung 3). Der Weg muss also gegen `on_ret` kontrolliert werden, sonst misst er W7 noch einmal.
- **Engine-Weg:** **Modul-Spec S11** -- `mb_vwap_anchor` kennt heute nur `session|hi|lo|rand_time` (`maband.py` Z. 75, 425-429); ein `globex`-Anker plus Overnight-POC waere ~30 Zeilen. **Erst nach Klaerung der Gap-Proxy-Frage bauen.**
- **Buch-Bezug:** kein eigenes Bein. Der Ziel-Arm ("Overnight-VWAP/POC als Zielpreis") gehoert in den Exit-Raum und wird dort unter [[#W18]] / [[#W47]] gefuehrt.
- **Kein Skelett in dieser Runde:** der Cross-Arm ist gegen Placebo verloren (#108), der Bias-Arm ist laut eigener Bank-Zeile zu ueber 80 % ein Gap-Proxy, und der Ziel-Arm laeuft unter W18/W47. Ein Skelett waere hier ein Aufwaermen.
- **Verwandte Tote:** **#108** (8 VWAP-Arten gegen Placebo, `on_frozen` -0,042, `globex` -0,036), AW-10/TA-06/HV-08/HV-43 (Bank, ungebaut), #109/#113 (Level-Placebo-Fehlerklasse), #151 Lehre 151 (Placebo-Diskretisierung -- fuer den POC unkritisch, weil stetig).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W42

**Bewegung:** Die Wochenend-/Feiertags-Nacht (Freitag-Schluss bis Montag-Open) ist ein anderer Nacht-Typ als die Werktags-Nacht.

- **Etikett / Rolle:** Filter / Filter (Pflicht-Split, keine eigene Strategie)
- **Stand:** **gemessen ohne Kandidat** -- `hyp_TN09_NQ`: 21 Register-Trials (davon 16 mit `tm_dow`), 0 Survivors. Schwesterkarte: SES-W33. **In der ersten Fassung dieser Karte kommen "Montag", "Wochenende" und "Feiertag" kein einziges Mal vor.**
- **Story:** Bank-Zeile **TN-09** sagt es ausdruecklich: "Weil Wochenend-Risiko und Wochenanfangs-Positionierung asymmetrisch sind, ist der Montags-Overnight-Return (Freitag-Schluss bis Montag-Open) ein **anderer Prozess** als der werktaegliche und **darf nicht in dieselbe Statistik**." Ueber ein Wochenende laeuft 65 Stunden Nachrichtenfluss in eine Preisluecke, ueber Nacht 17,5 Stunden. Ein `on_ret`-Schwellenwert, der beide Typen mischt, ist ein Mittelwert ueber zwei Verteilungen.
- **Engine-Weg:** **engine-faehig**, `tm_dow` existiert (72 Register-Trials). Fuer `asian.py` waere derselbe Split ~6 Zeilen.
- **Buch-Bezug:** keine eigene Zeile. **Auflage auf W1-W41 und auf jedes Skelett dieser Karte:** jeder Nacht-Gate-Test bekommt Montag als eigene Zelle oder schliesst Montag aus; welche Variante, entscheidet der Trade-Zahl-Verlust, nicht der Geschmack.
- **Kein eigenes Skelett:** ein Split ist keine Strategie. Er wird ab sofort als Pflichtzelle in ONORB-W7a, -W24a, -W29a, -W33a, -W34a, -W45a mitgefuehrt.
- **Verwandte Tote:** TN-09 (21 Trials, 0 Surv), SES-W33.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W43

**Bewegung:** Langer Globex-Pfad bei kleinem Sprung zum Open -- die Nacht hat gearbeitet und nichts bewegt (Absorption).

- **Etikett / Rolle:** Mean Reversion / Filter
- **Stand:** offen, 0 Trials. Bank-Zeile **TN-06** ungebaut, Schwesterkarte SES-W31 (ebenfalls 0 Trials, Modul-Spec C).
- **Warum die Zelle vorher leer war:** die erste Fassung nannte TN-06 nur als tote Verwandte unter [[#W32]] (Efficiency Ratio) und gab ihr keine Zeile -- obwohl W32 selbst "gross und choppy" ausdruecklich von "gross und gerade" trennt. Pfadlaenge gegen Sprung ist eine andere Kennzahl als Effizienz: ER normiert auf die Nettobewegung, die Absorptions-Quadranten stellen Brutto-Pfad und Netto-Sprung gegeneinander.
- **Story:** TN-06 woertlich: "Weil der Gap nur den Preisunterschied misst, das Overnight-Segment aber den ganzen Globex-Pfad, tragen die beiden verschiedene Information: ein kleiner Gap nach grossem Globex-Pfad bedeutet **Absorption**." Absorption heisst: jemand hat die ganze Nacht Gegenliquiditaet gestellt und sitzt am Morgen auf einer Position, die er noch nicht los ist. Das Geld bleibt liegen, weil `on_ret` die beiden Faelle per Konstruktion zusammenwirft.
- **Engine-Weg:** **Modul-Spec S10** -- `on_path` (Summe der absoluten Globex-Bar-Returns) in `overnight_context`, ~10 Zeilen auf der S1-Basis, plus Quadranten-Gate.
- **Buch-Bezug:** Gate fuer W4/W8/W30
- **Kein eigenes Skelett in dieser Runde:** faellt vollstaendig unter die S1-Spec und konkurriert mit W32/W29 um dieselbe Zelle; sobald S1 gebaut ist, ist es eine **Achse** fuer `variant-scout`, kein eigener Job.
- **Verwandte Tote:** TN-06 (ungebaut), SES-W31, #138 (Kompressions-Fehlerklasse).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W44

**Bewegung:** Die zweite Naht der Nacht -- die Globex-Reopen-Luecke (RTH-Close 17:00 gegen Reopen 18:00 ET), hin zu (Fill) und weg von (Erweiterung).

- **Etikett / Rolle:** Mean Reversion (Fill) / Trend (Erweiterung), Rolle Level
- **Stand:** offen, 0 Trials. Schwesterkarte: SES-W43 (Fill) und SES-W44 (Erweiterung), beide 0 Trials, Modul-Spec G.
- **Warum die Zelle vorher leer war:** die Karte kannte als Sprung-Element nur den **Cash-Open-Gap** (W21-W23). Der Reopen-Gap ist die zweite Naht **derselben** Nacht und ein eigenes Element.
- **Story (Fill-Arm):** Um 17:00 ET schliesst der CME-Handel fuer eine Stunde; wer eine unfertige Order hat, findet um 18:00 ein anderes Buch vor. Der Sprung ueber diese Pause ist eine Neubewertung ohne Handelspfad -- dieselbe Logik wie beim Cash-Gap, nur mit duennerer Gegenseite. **Story (Erweiterungs-Arm) ist schwach:** um 18:00 fehlt der Informationsschock, der grosse Gaps traegt; die Schwesterkarte stempelt sie deshalb selbst als schwach.
- **Engine-Weg:** **Modul-Spec G** (Schwesterkarte): `mode='gap'` kennt nur den RTH-Open **und hat keinen Null-Schalter** (`controls.ctl_null`, Randbedingung 2). Ohne ein S6-Aequivalent fuer `gap` ist jeder Kandidat hier per Konstruktion Bank-Material.
- **Buch-Bezug:** kein Bein, solange der `gap`-Modus keinen Null-Schalter hat.
- **Kein Skelett:** Null-Schalter fehlt (harte Regel: Wege ohne Null-Schalter-Pfad bekommen eine Modul-Spec, nie einen Job-Vorschlag).
- **Verwandte Tote:** SES-W43/W44, #130 (RTY_Gap-fade raus), `ideas.json` "Overnight-Gap-Fade" (Getoetet).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W45

**Bewegung:** Die letzte Nacht-Stunde vor dem Open (08:30-09:30 ET) ist ein eigenes Segment neben Asien und Europa.

- **Etikett / Rolle:** Trend / Filter
- **Stand:** offen, 0 Trials. Bank-Zeilen **MO-51** und **KF-40** ungebaut.
- **Warum die Zelle vorher leer war:** [[#W27]] trennt die Nacht nur in Asien und Europa. Recency ist hier **kein Parameter, sondern ein anderer Akteur**: um 08:30 ET liegen die US-Makrodaten (CPI, PPI, Claims, NFP), und sie werden **vor** dem Cash-Open verarbeitet.
- **Story:** **MO-51** -- "Weil eine grosse Order ueber die Sessiongrenze hinweg fortgesetzt wird, neigt NQ dazu, dass Drift-Richtung der letzten Globex-Stunde vor RTH (08:30-09:30) und die erste RTH-Stunde gleichgerichtet sind, wenn das Volumen in beiden Fenstern erhoeht ist." **KF-40** liefert den zweiten, unabhaengigen Grund: "Weil CPI-Releases um 08:30 ET vor dem RTH-Open liegen, ist die Reaktion beim Cash-Open bereits verarbeitet, weshalb ein CPI-Tag-Bias nur in der Globex-Phase 08:30-09:30 existiert und im RTH tot ist." Beide zusammen sagen: dieses Fenster traegt Information, die sich in `on_ret` (Close-zu-Open ueber 17,5 Stunden) vollstaendig verduennt. Das Geld bleibt liegen, weil unsere Nacht-Kennzahl per Konstruktion die letzte Stunde nicht von der ersten unterscheidet.
- **Engine-Weg:** **Modul-Spec S9** -- `pre_ret`/`pre_rvol` (08:30-09:29 ET) als dritte Segmentspalte in `overnight_context`, ~12 Zeilen auf der S1-Basis. `asian.py` kann das Fenster schon heute **einzeln** rechnen (`rs_start='08:30'`, `rs_end='09:25'`), aber nicht als Kontext neben Asien/Europa.
- **Buch-Bezug:** Gate fuer W1/W2/W7, Ersatz-Overlay auf `NQ_Momentum_d260818`
- **Pflichtzellen:** Makro-Tage getrennt von Nicht-Makro-Tagen (sonst misst der Weg nur KF-40), plus der Montags-Split aus [[#W42]], plus die DST-Kontrolle aus [[#W49]] entfaellt hier (09:30 ET ist ein US-Anker, kein 03:00-Problem).
- **Verwandte Tote:** MO-51/KF-40 (ungebaut), TN-08 (Europa allein, 37 Trials, 0 Kandidaten), #163 (Spec-B-Modul Makro-Tageszustand -- gebaut, hier wiederverwendbar).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W46

**Bewegung:** Der Nacht-Zustand bestimmt die **Definition** der Opening Range (Laenge und Breite adaptiv), nicht nur den Entry daraus.

- **Etikett / Rolle:** Trend / Level (Rolle: **Level-Definition**, in der ersten Fassung fehlte diese Rolle komplett)
- **Stand:** offen als Bedingung (0 Trials). Die **feste** OR-Laenge ist durchaus gesweept: `or_min` in 5/10/15/30 ueber 226 `orb`-Trials. Die **Kopplung an den Nacht-Zustand** hat 0 Trials.
- **Warum die Zelle vorher leer war:** die Karte behandelt die 30-Minuten-OR durchgehend als gesetzt. Element "NY-OR-Grenze" x Zustand "eng/weit" in der Rolle "Level-Definition" war nicht besetzt.
- **Story:** Nach einer weiten Nacht ist die Preisfindung schon gelaufen; eine 30-Minuten-Range misst dann nur noch Nachlauf und ist mechanisch zu breit, was das Risiko je Trade aufblaeht, ohne die Trefferquote zu heben. Nach einer engen Nacht ist das Gegenteil der Fall. Verwandte Bank-Zeile **VV-14** nimmt denselben Gedanken von der Volumenseite: "NQ neigt zu klarerer Ausbruchs-Definition, wenn die Opening Range ueber eine feste Kontraktzahl statt ueber 30 Minuten definiert wird."
- **Engine-Weg:** **Modul-Spec S12** -- `or_min` adaptiv aus `on_range`/`on_sigma` in `qbt._orb_trades`, ~15 Zeilen, **setzt S1 voraus**. Achtung: `mode='orb'` hat keinen Null-Schalter (Randbedingung 1), der Test muss ueber den `asian`-Nachbau laufen oder S6 abwarten.
- **Buch-Bezug:** Achse fuer W1/W2/W4, kein eigenes Bein.
- **Kein eigenes Skelett:** sobald `on_range` existiert, ist das eine **Achse** von ONORB-W29a und gehoert zu `variant-scout`, nicht als zwoelftes Grid ins Register.
- **Verwandte Tote:** VV-14 (ungebaut), #050 (`or_min=5` beim Noise-ORB und beim Scalp -- die kurze OR ist der Survivor-Bereich), #068.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W47

**Bewegung:** Ziel und Haltedauer **am NY-OR-Level** werden an der Nacht-Vola bemessen (ORB-Scalp: enges Ziel, kurzes Fenster).

- **Etikett / Rolle:** Trend / Exit
- **Stand:** **teilgemessen, aber nie bedingt auf die Nacht.** `SCALP_NQ` ist die **einzige ORB-Familie mit Survivors** im Register: `backfill:scalp_discovery_results.json` = 60 Trials / **20 Survivors** (#050, 0,3R- bis 1,0R-Target x Haltezeit-Cap 5/10/15/20/EOD, war Buch-Bein 9). Achsen vorhanden: `orb_max_hold` 5/10/15/20 je 12 Trials, `target_mult` auf allen 226 `orb`-Trials. Mit Nacht-Bedingung: 0 Trials.
- **Warum die Zelle vorher leer war:** [[#W33]] skaliert nur **Stops** auf den drei aktuellen Buch-Beinen und laesst den **Zielraum am OR-Level** aus -- obwohl #050 woertlich sagt: "Der **Exit-Raum** war der eigentliche Hebel, nicht ein neuer Mechanismus."
- **Story:** Ein festes 0,3R-Target ist eine Wette darauf, wie weit der Preis in den naechsten Minuten typischerweise laeuft. Genau diese Groesse ist an der Nacht-Vola ablesbar, und zwar aktueller als an der Vortages-ATR. Nach einer volatilen Nacht ist ein 0,3R-Ziel zu frueh (Gewinn wird verschenkt), nach einer ruhigen zu spaet (der Trade laeuft in den Stop, bevor das Ziel erreichbar ist). Das Geld bleibt liegen, weil Ziel und Haltedauer als **Parameter** behandelt werden statt als bedingte Groessen -- und weil #050 zwar den Hebel benannt, aber nie eine Bedingung dafuer gesucht hat.
- **Engine-Weg:** Achsen existieren (`target_mult`, `orb_max_hold`), die Bedingung braucht `on_sigma` aus **S1** (faellt mit ONORB-W33a ab). **Null-Schalter-Falle:** im `orb`-Modus gibt es keinen (Randbedingung 1) -- die saubere Messung laeuft als **Exit-Ueberlagerung auf den drei Buch-Beinen** (Exit-Sweep-Weg, `ctl_null` vorhanden) und erst danach am OR-Level selbst.
- **Buch-Bezug:** Ersatz-Exit fuer alle drei Buch-Beine
- **Verwandte Tote:** #050 (`SCALP_NQ` Bein 9 -- der **Beleg**, nicht der Widerspruch), #046 (BE/Trail-Overlays: 0 von 8 Beinen ueberlebte OOS -- Abgrenzung: hier vorab festgelegte Zielgroesse, kein nachlaufender Eingriff), #157 (`be_trail` v2 +2,95 pp mit CI von -2 bis +8), #126/#127 (ORB-fade aus dem Buch).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W48

**Bewegung:** Preis bricht die London-OR, kommt zurueck und laeuft am Level entlang (Retest im London-Fenster).

- **Etikett / Rolle:** Trend / Signal
- **Stand:** offen, 0 Trials. Die Relation "entlanglaufen" war im London-Ast **leer** -- NY hat sie als [[#W6]], London hatte sie nicht.
- **Story:** Wie W6 (wer den Ausbruch verpasst hat, kauft den Rueckfall), aber im duenneren Buch: dort ist der Rueckfall groesser und der Wiedereinstieg billiger zu bekommen. **Genau dieselbe duenne Liquiditaet verschlechtert aber den Fill** -- Story und Killer sind dieselbe Tatsache, wie schon bei W13.
- **Engine-Weg:** `orb_exec='retest'` existiert (`qbt.py` Z. 618), laeuft aber nur im RTH-Fenster; im London-Fenster braucht es den `asian`-Nachbau plus eine Retest-Seite (S5-Umfeld). `slippage_ticks=2.0` **vorab** Pflicht (Muster TN-10).
- **Buch-Bezug:** neues Bein (Live-Buch-Merker)
- **Kein Skelett:** W6 ist auf NQ **zweimal** ehrlich falsifiziert (#068 Pineda-Retest 36 Varianten, #083 IVB mit exakter Paper-Spec). "Dasselbe im anderen Zeitfenster" ist kein neuer Grund (harte Regel: kein Aufwaermen). Der Weg steht hier, damit die Zelle nicht mehr leer aussieht, und nicht, weil er gerechnet werden soll.
- **Verwandte Tote:** #068, #083, #079, #028 (London-Breakout inkl. London-IB, 46 Configs), #033 (doppelte Kosten toeten enge Spreads).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W49

**Bewegung:** Kontrollweg -- verschiebt sich jeder 03:00-ET-Effekt mit der Sommerzeit-Umstellung?

- **Etikett / Rolle:** -- / Kontrolle (keine Handels-Story, und das ist der Punkt)
- **Stand:** offen. Die erste Fassung gibt unter "Was NICHT geprueft wurde" selbst zu: "DST-Verhalten von `asian.load_full` (`sess = index + 6h`) gelesen, aber **nicht geprueft**" -- und fuehrt dann keinen Kontrollweg dafuer. Die Schwesterkarte hat ihn als **SES-W35** als **Pflichtbeilage**.
- **Warum das zaehlt:** US und EU schalten die Uhr an **verschiedenen** Terminen um. Zwei bis drei Wochen im Jahr liegt der London-Open nicht bei 03:00 ET, sondern bei 04:00 ET. Ein fester Uhrzeit-Anker misst in diesen Wochen ein anderes Ereignis. Ein Effekt, der die Umstellung **mitmacht**, ist ein Session-Effekt; einer, der an der Uhrzeit klebt, ist ein Artefakt des Zeitachsen-Codes.
- **Engine-Weg:** **Modul-Spec S13** = kein Code, eine Auswertungs-Pflichtspalte: jeder 03:00-ET-Job wird zusaetzlich nach DST-Regime gesplittet (US-Sommerzeit / EU-Sommerzeit / beide / keine), und der Effekt muss in beiden Regimen dasselbe Vorzeichen haben.
- **Buch-Bezug:** keiner. **Pflichtbeilage** zu W10-W14, W36, W45 (nein: W45 haengt am US-Anker) und W48 -- konkret: zu allen Wegen mit einem 03:00-ET-Fenster.
- **Verwandte:** SES-W35, #152 (Chart-Template-Vorfall: eine nicht versionierte Zeitfenster-Einstellung hat das ganze Buch still auf eine andere Session verschoben -- dieselbe Fehlerklasse).
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

### W50

**Bewegung:** Der heutige RTH-Return setzt sich in der kommenden Nacht fort bzw. dreht (Rueckrichtung Tag -> Nacht).
**Swing-Zeile:** ja, Buch-Bezug ist Live-Buch-Merker, kein Prop-Buch-Job.

- **Etikett / Rolle:** Swing / Signal
- **Stand:** offen, 0 Trials -- **jeder** der 298 `asian`-Register-Trials handelt im RTH (`tr_start='09:30'`), keiner nimmt den RTH als **Quelle**. Schwesterkarte: SES-W36 (Fortsetzung) und SES-W37 (Umkehr), beide 0 Trials, beide als (Swing) markiert.
- **Warum die Zelle vorher leer war:** die Swing-Pflicht war formal erfuellt (W37/W38 sind markiert und als Live-Buch-Merker gefuehrt), aber die Rueckrichtung **Tag -> Nacht** fehlte -- in einer Karte ueber Nacht-Tag-Kopplung ist das die zweite Haelfte der Frage.
- **Story:** Lou/Polk/Skouras trennen Overnight- und Intraday-Segment in zwei Klientelen mit je eigener Fortsetzung. Wenn das stimmt, muss es in **beide** Richtungen pruefbar sein, nicht nur Nacht -> Tag. Der Fortsetzungs-Arm (SES-W36) und der Umkehr-Arm (SES-W37) sind dieselbe Messung mit zwei Vorzeichen.
- **Engine-Weg:** `asian` mit `rs 09:30-15:55` / `tr 18:00-09:25` (Fenster frei waehlbar, `asian.py` Z. 73-76).
- **Buch-Bezug:** **Live-Buch-Merker, nicht Prop-Buch.** E8 verbietet Overnight-Halten (EOD-Zwangsschliessung), der Weg kann im Prop-Buch per Konstruktion nicht gehandelt werden.
- **Kein Prop-Buch-Skelett** (Swing-Regel Max, 11.09.2026). Steht hier, damit nichts verloren geht, falls das Live-Konto kommt.
- **Verwandte:** SES-W36/SES-W37, TN-05 ("Vortages-Intraday-Return als besserer Bias", `hyp_TN05_NQ` = `premise_failed`), #037-Umfeld Overnight-Halten bei E8.
- **Stempel (`verdict-auditor` traegt hier nach):** _offen_

---

## Reihenfolge nach Buch-Chance (13 Skelette, Stand nach dem Nachtrag)

| Rang | ID | Weg | Engine | Buch-Bezug | why_status |
|---|---|---|---|---|---|
| 1 | ONORB-W7a | W7 Weg vom Cash-Open | engine-faehig | NQ_Momentum_d260818 | **offen** (22.09.: keine Quelle vergleicht `rangepos` gegen `ret`; Gegenindiz Grant/Wolf/Yu 2005) |
| 2 | ONORB-W33a | W33 Nacht-Vola als Stop-Skala | Modul-Spec S1 | NQ_Momentum_d260818 | **belegt** (Zhang/Zhao SSRN 3574323 + Zadourian/Grassberger; Why 22.09. ueberarbeitet) |
| 3 🆕 | ONORB-W47a | **W47 Ziel- und Haltedauer am OR an der Nacht-Vola** | Achsen da, Bedingung aus S1 | alle drei Buch-Beine (Exit) | **offen** (keine Arbeit zu TP/Haltedauer bedingt auf Nacht-Vola; Gegenindiz Mesfin Tab. 3) |
| 4 | ONORB-W24a | W24/W25 Nacht-Richtung als Tor | Modul-Spec S2 | NQ_Momentum_d260818 | **offen** (Literatur spricht gegen 'Halter im Ruecken': Yu/Rentzler/Wolf 2005 -- als TOR nie getestet) |
| 5 | ONORB-W29a | W29/W30 Nacht-Range als Tor | Modul-Spec S1/S3 | NQ_Momentum_d260818 | **offen** (Overnight-RANGE als ORB-Bedingung nirgends getestet; Teilstuetze nur ueber Vola) |
| 6 🆕 | ONORB-W39a | **W39 Sweep des Nacht-Extrems (kreuzen und scheitern)** | `asian break_us` da + S5; Vorlauf: 4 `premise_failed`-Jobs | neues Bein NQ_ONSweep | **offen** (kein Futures-Nachweis fuer Stop-Cluster; Mesfin 4.3 nach Friktion negativ) |
| 7 | ONORB-W34a | W34 Position des Opens in der Nacht-Range | Modul-Spec S1/S3 | NQ_Asia-Dir-USopen_d260820 | **offen** (nur Market-Profile-Praktikerwissen, nichts peer-reviewt) |
| 8 | ONORB-W5a | W5 Kreuzen und scheitern am NY-OR | Modul-Spec S5 (revidiert) | NQ_ORFail | **offen** (keine Fehlausbruch-Arbeit mit sauberer Definition + OOS auf Index-Futures) |
| 9 | ONORB-W27a | W27 Nacht dreht in sich | Modul-Spec S1 | NQ_Asia-Dir-USopen_d260820 | **offen** (Ito/Hashimoto ist FX-Spot; Asien->Europa-Uebergabe in Futures unbeschrieben) |
| 10 🆕 | ONORB-W45a | **W45 Letzte Nacht-Stunde 08:30-09:30 als drittes Segment** | Modul-Spec S9 | NQ_Momentum_d260818 | **offen, staerkste Teilstuetze** (Kurov et al. JFQA 2019: ES-Drift ab ca. 30 Min vor 08:30, ~40 % der Anpassung vorher) |
| 11 | ONORB-W31a | W31 Nacht-Volumen als Tor (jetzt mit Fade-Gegenarm MO-19) | Modul-Spec S1 | NQ_Momentum_d260818 | **offen** (kein Globex-Volumen-Praediktor; Cartea et al. laufen in Gegenrichtung) |
| 12 | ONORB-W35a | W35 Kaskade London-Ausgang -> NY-Ausbruch | Modul-Spec S8 | NQ_Momentum_d260818 | **offen** (keine Literatur zu Breakout-Kaskaden; #028 hat den London-Break mitgetoetet) |
| 13 ⬇ | ONORB-W10a | W10/W11 Durch die London-OR hindurch (**abgewertet**) | S4, aber Auflage | NQ_LondonOR | **offen** (keine Arbeit zur London-eigenen OR; kein verifizierbarer MNQ-Spread 03:00-09:30) |


**Warum diese Reihenfolge (Stand nach dem Nachtrag):** Ersatz schlaegt neu (#139 B3) -- elf der dreizehn Skelette zielen auf einen bestehenden Bein-Slot. Engine-faehig schlaegt Modul-Spec: Rang 1 braucht **keine Code-Aenderung**, Rang 3 nur eine Bedingung auf Achsen, die schon da sind. Belegt schlaegt Entwurf: Rang 2 ist weiterhin das einzige Skelett mit `why_status: belegt`. Ohne tote Verwandte schlaegt kontaminiert.

**Was der Nachtrag an der Reihenfolge geaendert hat:**
- **Rang 3 (neu, `ONORB-W47a`):** #050 sagt woertlich, der Exit-Raum sei der eigentliche Hebel, und `SCALP_NQ` ist die **einzige** ORB-Familie mit Survivors im Register (20 von 60 Trials). W33 skaliert nur Stops -- der Zielraum am OR-Level war ausgelassen. Das ist der billigste dokumentierte Hebel der ganzen Karte.
- **Rang 6 (neu, `ONORB-W39a`):** der Fehlausbruch-Mechanismus liegt als vier fertige Job-Dateien vor, alle vier `premise_failed`. Vor jeder neuen Zeile Code wird dieser Vorlauf repariert und gerechnet.
- **Rang 13 (`ONORB-W10a`, von 8 auf 13 abgewertet):** #028 hat London-IB, also die London-eigene Range, ausdruecklich mitgetoetet; zusaetzlich hat `firstbar_ematrail` im Europa-Fenster 960 Trials ohne einen Survivor. Der einzige verbleibende neue Grund ist die Asien-Richtungsbedingung. Der Weg bleibt im Vorrat, aber **erst rechnen, wenn oben nichts traegt**.
- **Kein Skelett bekommen** trotz Story: W40 (laeuft als SES-W6a in der Schwesterkarte, Doppel-Messung vermeiden), W41 (Cross-Arm gegen Placebo verloren, #108), W42 (Split, keine Strategie -- wird Pflichtzelle), W43/W46 (Achsen auf der S1-Basis, gehoeren zu `variant-scout`), W44 (kein Null-Schalter), W48 (W6 zweimal falsifiziert, "anderes Fenster" ist kein neuer Grund), W49 (Kontrollweg), W50 (Swing, Live-Buch).

**Dreizehn und nicht dreissig:** 65.035 Register-Trials. Jedes zusaetzliche Grid hebt die Zufallsdecke fuer alle bestehenden Kandidaten mit. Drei Skelette mehr als in der ersten Fassung, dafuer sind zwei der urspruenglichen zehn (Rang 12 und 13) auf "erst nach Auflage" gestellt -- die erste Rechenrunde bleibt bei acht.

**Pflichtzellen fuer JEDES Skelett dieser Karte (neu, 21.09.):** (1) Montags-/Feiertags-Split aus [[#W42]], (2) Epochen-Split vor/ab 2022 aus GM-15, (3) bei jedem 03:00-ET-Fenster der DST-Kontrollweg [[#W49]], (4) beim ORB-Ast das Zarattini-Noise-Band als Vergleichsarm (`ORB2_ZAR`, der 21. Survivor).



## Research-Rueckschrieb 22.09.2026 (`research-scout` -> `familien-scout`)

**Ergebnis in einer Zeile:** 13 Skelette geprueft, **1 belegt** (`ONORB-W33a`), **12 offen**, **0 durch Research widerlegt**, **0 fallen aus der Rechenrunde**.

- **"Offen" heisst hier fast immer Negativbefund der LITERATUR, nicht Gegenbeweis:** zu elf der zwoelf offenen Wege gibt es schlicht keine Arbeit. Die Negativbefund-Zeilen sind am 22.09. in [[Research-Cache]] eingetragen, damit dieselbe Suche nicht zweimal laeuft.
- **Vier Skelette haben ein externes GEGENINDIZ bekommen** und muessen ihre Kontrollzellen zwingend mitfuehren: `ONORB-W24a` (Yu/Rentzler/Wolf JOIM 2005 -- Nacht-Return eher Reversal als Fortsetzung, also beide Vorzeichen messen), `ONORB-W39a` (Mesfin arXiv 2605.04004 Abschn. 4.3: 6.442 Asia-Grabs, Fade brutto 0,2-0,8 Punkte, nach Friktion -2,20 Punkte, T -14,1), `ONORB-W34a` (Mesfin Tab. 5: MNQ-Gaps fuellen sich nicht konsistent im RTH), `ONORB-W47a` (Mesfin Tab. 3: kurzer Horizont ist die schlechteste Variante).
- **`ONORB-W33a` ist und bleibt das einzige belegte Skelett.** Der Mechanismus ist jetzt mit Quelle hinterlegt (Zhang/Zhao SSRN 3574323, Cache Z. 386; Zadourian/Grassberger EPL 2017, Z. 387), der Why wurde ueberarbeitet. Zwei Teile bleiben ausdruecklich unbelegt und sind damit der eigentliche Testgegenstand: Nacht-Vola als **Stop-Skala gegen ATR** (keine Arbeit) und die **Persistenz 2023-2026** (das Paper endet 04/2020).
- **`ONORB-W45a` hat die staerkste neue Teilstuetze der offenen Gruppe** (Kurov/Sancetta/Strasser/Wolfe JFQA 2019: ES-Futures driften ab rund 30 Minuten vor dem 08:30-Release, etwa 40 Prozent der Anpassung laufen vor der Zahl; Barclay/Hendershott fuer den informationsmotivierten Pre-Open). Der Praediktions-Teil (erste RTH-Stunde) bleibt trotzdem ungetestet, die KF-40-Frage offen.
- **Kein Weg wurde geloescht, keine Nummer geaendert, kein Tot-Stempel gesetzt.** "Research widerlegt" waere ohnehin keiner -- tot nur nach vollem Test (Regel "Hypothese vor Urteil").

**Nicht an `ein-weg` in dieser Runde:** keines. Alle 13 Skelette gehen weiter.

---

### Rang 1 -- `ONORB-W7a`: Opening-Range-FORM statt Opening-Drive, mit dem Nacht-Gate, das im Register schon in die richtige Richtung faellt

- **Weg:** W7 Weg vom Cash-Open, beide Richtungen getrennt
- **Mechanismus:** tsmom auf NQ mit tm_signal='rangepos' und tm_sig_start=15 (Position des Kurses in der 09:30-09:45-Range, Entry ab Minute 15) statt tm_signal='ret'/tm_sig_start=0, gegatet auf tm_on_ret_min in {0,0025; 0,0045}. Pflichtzellen: ungegatet und tm_on_ret_max=0,0025 (Weg W3) als Kontrollen, plus ctl_sides und ctl_null.
- **Why (`entwurf`, Zahlen am 21.09.2026 korrigiert):** Weil die Nacht-Preisfindung in Index-Futures ohne US-Cash-Liquiditaet stattfindet, muss die US-Entscheider-Kohorte am 09:30-Open zu einer ueber Nacht gelaufenen Bewegung Stellung nehmen -- und diese Stellungnahme zeigt sich als Position des Preises in der ersten Viertelstunde, nicht als blosser Return vom Open. `on01_cashopen_decision_NQ` hat den Return-Weg bereits gemessen (**71 Trials / 28 Survivors**, nicht 72/18): Zelle `on_ret_min=0,0025` **13 von 18 Survivors**, ungegatet **10 von 17**, `on_ret_min=0,0045` 5 von 18, Kontrollzelle `on_ret_max=0,0025` (ruhige Naechte) **0 von 18**. Die Kontrollzelle faellt also genau so aus, wie sie ausfallen muss, wenn das Gate echt ist. Die **Formseite** desselben Gates hat null Trials.
- **Engine-Weg:** tsmom: tm_signal='rangepos' (tsmom.py Z. 26), tm_sig_start (Z. 63), tm_on_ret_min (sigcore.py Z. 1169-1171)
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote (21.09. erweitert):** `on01_cashopen_decision_NQ` (**71 Trials / 28 Survivors**, 0 Kandidaten); `gen_tsmom_combo_mom_NQ_exits_09032135` (Folge-Job optimierte die UNGEGATETE Zelle weiter); **`firstbar_ematrail`** (derselbe Opening-Drive ohne Level, **2.880 Trials**, in `ideas.json` auf allen vier Maerkten "Getoetet"; Split `ny`/24h 109/960, `ny`/rth 0/960, `eu`/24h 0/960); `ideas.json` **"OR_DELTA_BIAS_NQ" = Validiert** (LONG ueberlebt, SHORT nicht -- gehoert als Vergleichsarm daneben).
- **Research-Fragen:** Gibt es eine Quelle, die die POSITION in der Opening Range gegen den REINEN RETURN ueber dasselbe Fenster als Praediktor vergleicht (`rangepos` vs. `ret`)? Zarattini/Aziz nutzen die Richtung der ersten Kerze, nicht die Position. / Ab welcher Overnight-Bewegung gilt eine Nacht in der Literatur als 'Preisfindung' statt Rauschen -- gibt es eine belegte Schwelle in Sigma oder Prozent?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Quelle vergleicht die POSITION in der Opening Range (rangepos) gegen den reinen Return ueber dasselbe Fenster; Zarattini/Aziz nutzen die RICHTUNG der ersten Kerze (Research-Cache Z. 19). Keine belegte Sigma- oder Prozent-Schwelle, ab der eine Nacht als 'Preisfindung' statt Rauschen gilt. Gegenindiz: Grant/Wolf/Yu JBF 2005 (der Open-Sprung revertiert intraday). Eigen: #147/#150 -- die First-Bar-Richtung ist ein NQ-Befund. Cache am 22.09. um die Negativbefund-Zeilen ergaenzt. Folge: Why bleibt Eigenkonstruktion aus dem Register-Befund (ON01), nicht aus Literatur.
- **Pflichtzellen (neu 21.09.):** Montags-Split [[#W42]], Epochen-Split vor/ab 2022 (GM-15), Vergleichsarm `ORB2_ZAR` (Zarattini-Noise-Band).
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 2 -- `ONORB-W33a`: Stop- und Zielgroesse an der Nacht-Vola statt an der Vortages-ATR

- **Weg:** W33 Nacht-Vola als Skala, richtungsneutral
- **Mechanismus:** Neue Tageskontext-Spalte on_sigma (realisierte 1m-Vola der Globex-Session 18:00-09:29 ET) und neuer tm_stop_mode='on_sigma'. Getestet als Ersatz-Overlay auf alle drei Buch-Beine gegen die bestehende range-/atr-Skalierung, Entscheidungskriterium v2-Passquote, nicht expR.
- **Why (`belegt`, am 22.09.2026 nach dem Research ueberarbeitet):** Weil mehr als 40 Prozent der Tagesvarianz von Index-Futures in der Nacht anfaellt und die Overnight-RV die Intraday-RV vorhersagt (Zhang/Zhao SSRN 3574323, MSE -27 Prozent gegenueber der Benchmark; Zadourian/Grassberger EPL 2017 fuer die Asymmetrie; Samples enden ca. 2020 bzw. sind Aktien), traegt die Nacht Information ueber die Pfad-Varianz des heutigen Tages, die die Vortages-ATR nicht kennt. Dass das Vola-Regime bei uns die Varianz treibt, ist gemessen (Logbuch #139 / AR-17: sd_off/sd_on = 1,50, CI [1,24; 1,88], Drift dabei nicht kleiner -- also Skalieren statt Gaten). Bewusst nur SKALA, nie Gate: Overnight-Vola als Tagesfilter hob den Sharpe, senkte aber die Passquote (#074, Lehre 21). Unbelegt bleiben (a) dass ein Nacht-Vola-Stop besser ist als ein ATR-Stop (keine Arbeit gefunden, Test noetig) und (b) die Persistenz auf NQ im Fenster 2023-2026 (das Paper ist von 04/2020). Dass der Exit-Raum bei uns der am wenigsten ausgereizte Hebel ist, steht in **#050** ("Der Exit-Raum war der eigentliche Hebel, nicht ein neuer Mechanismus") -- die frueher zitierte **#187 existiert nicht**, das Logbuch endet bei #168.
- **Engine-Weg:** Modul-Spec noetig -- sonst nichts: tm_stop_mode ist bereits eine Achse (tsmom.py Z. 76)
- **Modul-Spec:** sigcore.py: overnight_context(symbol) aus asian.load_full, Spalten on_sigma/on_range/on_er/on_rvol/on_pos je Globex-Tag, Cache wie _CTX_CACHE (~70 Zeilen); daily_context um diese Spalten erweitern (~8 Zeilen); tsmom.py tm_stop_mode='on_sigma' (~12 Zeilen). Pflicht: ctl_delay muss gruen bleiben (die Nacht endet vor 09:30, aber der Join ueber den Globex-Tag ist die Fehlerquelle).
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote:** #046 (BE/Trail-Overlay: 0 von 8 Beinen ueberlebte OOS); #157 (be_trail v2 +2,95 pp, CI von -2 bis +8)
- **Research-Fragen:** Gibt es eine Arbeit, die Overnight-RV EXPLIZIT als Stop-Skala (nicht als Prognosevariable) testet, mit Ergebnis gegen ATR? / Ist der Overnight-RV->Intraday-RV-Zusammenhang auf NQ-Futures im Fenster 2023-2026 noch vorhanden, oder ist er wie der Overnight-Drift verfallen?
- **Research-Stand (22.09.2026, `research-scout`):** `belegt` -- Mechanismus belegt: Overnight-RV sagt Intraday-RV voraus, ueber 40 Prozent Overnight-Anteil an der Tagesvarianz -- Zhang/Zhao SSRN 3574323 (Cache Z. 386) plus Zadourian/Grassberger EPL 2017 (Z. 387). Eigene Stuetze: Logbuch #139/AR-17, sd_off/sd_on = 1,50, CI [1,24; 1,88]. NICHT belegt und damit Testgegenstand: (a) Overnight-RV als STOP-SKALA gegen ATR (keine Arbeit gefunden), (b) Persistenz 2023-2026 (das Paper ist von 04/2020). Why ueberarbeitet und mit Quellen versehen.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 3 🆕 -- `ONORB-W47a`: Ziel und Haltedauer am OR-Level an der Nacht-Vola statt als fester Parameter

- **Weg:** W47 Ziel-/Haltedauer-Achse am NY-OR, bedingt auf die Nacht-Vola
- **Mechanismus:** `target_mult` und `orb_max_hold` werden nicht mehr fest gesetzt, sondern aus `on_sigma` (realisierte Globex-Vola, faellt mit `ONORB-W33a` ab) abgeleitet: Ziel = k x `on_sigma`, Haltedauer-Cap = f(`on_sigma`). Gerechnet zuerst als **Exit-Ueberlagerung auf den drei Buch-Beinen** (dort gibt es `ctl_null`), danach am OR-Level selbst. Zellen: feste Skala (Status quo, #050-Werte 0,3R/0,5R/0,75R/1,0R x Cap 5/10/15/20/EOD), Nacht-Vola-Skala, ungegatet. Entscheidungskriterium **v2-Passquote**, nicht `expR`.
- **Why (`entwurf`):** Weil ein festes 0,3R-Ziel eine implizite Wette darauf ist, wie weit der Preis in den naechsten Minuten typischerweise laeuft, und weil genau diese Groesse an der gerade zu Ende gegangenen Nacht ablesbar ist statt an der Vortages-ATR, ist die Ziel- und Haltedauer-Wahl ein **bedingter** Parameter und kein fester. Nach einer volatilen Nacht ist 0,3R zu frueh und verschenkt die Bewegung, nach einer ruhigen zu spaet und der Trade laeuft vorher in den Stop. Belegt ist der Hebel, nicht die Bedingung: **#050** sagt woertlich "Der Exit-Raum war der eigentliche Hebel, nicht ein neuer Mechanismus", und `SCALP_NQ` ist mit **20 Survivors aus 60 Trials** die einzige ORB-Familie im Register, die je Survivors hatte (Buch-Bein 9). Bedingt auf die Nacht wurde dieser Raum nie gemessen: 0 Trials.
- **Engine-Weg:** Achsen sind vorhanden (`target_mult` auf allen 226 `orb`-Trials, `orb_max_hold` 5/10/15/20 je 12 Trials). Die Bedingung braucht `on_sigma` aus **Modul-Spec S1**. **Null-Schalter-Falle:** `mode='orb'` hat keinen (Randbedingung 1) -- deshalb erst als Exit-Ueberlagerung auf den Buch-Beinen rechnen.
- **Modul-Spec:** keine eigene. S1 (`on_sigma`) faellt mit Rang 2 ab, danach ~10 Zeilen fuer die Ableitung der beiden Exit-Groessen.
- **Buch-Bezug:** Ersatz-Exit fuer `NQ_Momentum_d260818`, `NQ_LastHour_v3`, `NQ_Asia-Dir-USopen_d260820`
- **Verwandte Tote:** #050 (`SCALP_NQ` Bein 9 -- der Beleg); #046 (BE/Trail-Overlays: 0 von 8 Beinen ueberlebte OOS -- Abgrenzung: hier **vorab** festgelegte Zielgroesse, kein nachlaufender Eingriff); #157 (`be_trail` auf v2 +2,95 pp, CI von -2 bis +8); #126/#127 (ORB-fade aus dem Buch).
- **Research-Fragen:** Gibt es eine Arbeit, die Take-Profit-Distanz oder Haltedauer EXPLIZIT an der Overnight-Vola bedingt (nicht am Vortages-ATR)? / Existiert Literatur zur optimalen Haltedauer nach einem Opening-Range-Bruch als Funktion der erwarteten Tages-Vola (Optimal-Stopping-Rahmen)?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Arbeit zu Take-Profit-Distanz oder Haltedauer bedingt auf die Overnight-Vola, und keine Optimal-Stopping-Arbeit zur Haltedauer nach einem OR-Bruch (Cache 22.09., Negativbefund). Gegenindizien: eigen #068 (kein Follow-Through nach dem Bruch, auch mit Vola-Kondition) und Mesfin arXiv 2605.04004 Tab. 3 (kurzer Horizont ist die schlechteste Variante). Der Hebel bleibt belegt (#050), die BEDINGUNG nicht -- Why steht unveraendert auf Entwurf.
- **Pflichtzellen:** Montags-Split [[#W42]], Epochen-Split vor/ab 2022, `ctl_sides`, Seed-Streuung ueber 5 Seeds (Exit-Effekte sind klein, #157-Muster).
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 4 -- `ONORB-W24a`: Die Nacht als TOR statt als Signal: Ausbruchsrichtung muss mit der Nacht-Richtung uebereinstimmen

- **Weg:** W24/W25 Nacht-Richtung als Tor, long und short getrennt
- **Mechanismus:** Signiertes Gate tm_on_dir in {'agree','against'} auf dem Opening-Drive/ORB-Weg. Vier Zellen: agree, against, ungegatet, plus ctl_null. Long und Short getrennt ausgewertet (Wege W24/W25), Veto-Arm (W26) faellt als 'against'-Komplement mit an.
- **Why (`entwurf`):** Weil die Richtung der Nacht die Positionierung ist, mit der die US-Sitzung startet, hat ein Ausbruch MIT ihr die bereits vorhandenen Halter im Ruecken, waehrend ein Ausbruch GEGEN sie diese Halter erst umdrehen muss -- das ist ein Unterschied in der Gegenseiten-Dichte, nicht in der Prognose. Unsere 145 Register-Trials mit tm_base='overnight' haben die Nacht-Richtung ausschliesslich als SIGNAL benutzt (0 Survivors); als TOR auf ein bestehendes Signal ist sie nie gemessen worden, weil beide vorhandenen Gates in sigcore mit abs() rechnen und die Richtung wegwerfen.
- **Engine-Weg:** Modul-Spec noetig (Gate muss nach der Richtungsbestimmung greifen)
- **Modul-Spec:** tsmom.py: tm_on_dir in DEFAULTS plus Pruefung in _trades() direkt nach der Richtungsbestimmung, NICHT in sigcore.gates_pass (dort ist die Richtung noch nicht bekannt), ~20 Zeilen. Gleiche Pruefung optional in asian.py fuer die London-Wege (~10 Zeilen).
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote:** TN-01/TN-03/TN-12 (145 Trials tm_base='overnight', 0 Survivors -- dort Signal, hier Tor); #036 (Long/Short-Asymmetrie bei ORB)
- **Research-Fragen:** Gibt es Evidenz, dass Overnight-Returns als BEDINGTES Tor auf ein Intraday-Signal besser funktionieren denn als eigenstaendiges Signal (Conditioning statt Prediction)? / Lou/Polk/Skouras trennen Overnight und Intraday in eigenstaendige Fortsetzungseffekte -- sagt jemand etwas ueber die INTERAKTION beider Vorzeichen am selben Tag?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Einzige Interaktions-Arbeit auf NQ: Yu/Rentzler/Wolf JOIM 2005 (Nacht-Return ueberwiegend mit REVERSAL verbunden), dazu Grant/Wolf/Yu JBF 2005 und SSRN 2730304 / 5807282 (Cache Z. 294/295). Die Literatur spricht damit gegen das Bild 'Halter im Ruecken'. Als TOR auf ein Ausbruchssignal ist die Nacht-Richtung aber nie getestet worden, und unser eigenes Buchbein Asia-Dir setzt die Asien-Richtung fort. Auflage: der Test muss BEIDE Vorzeichen (agree und against) messen, nicht nur agree.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 5 -- `ONORB-W29a`: Nacht-Range als Tor fuer den NY-Ausbruch: nur nach weiter Nacht wird ein Level-Bruch gehandelt

- **Weg:** W29/W30 Nacht-Range als Tor, Breakout- und Fade-Arm in einer Messung
- **Mechanismus:** Neue Kennzahl on_range (Globex-High minus Globex-Low, normiert auf ATR20) als Gate auf den NY-ORB-Weg. Beide Aeste als eine Messung: on_range_min (Breakout-Arm, W29) und on_range_max (Fade-Arm, W30) plus ungegatete Kontrolle.
- **Why (`entwurf`):** Weil die Nacht-Range misst, wie weit die Bewertung ohne US-Liquiditaet verschoben wurde, und weil Overnight-Volatilitaet die Intraday-Volatilitaet desselben Tages vorhersagt, ist eine weite Nacht die Bedingung dafuer, dass ein Ausbruch am Morgen ueberhaupt genug Distanz macht, um die Kostenschwelle (MNQ-Round-Trip rund 2 Punkte) zu ueberspringen. Der Grund, warum das Geld liegen bleibt, ist mechanisch: unsere daily_context kennt nur gap und on_ret, also nur den SPRUNG, nie die SPANNE der Nacht.
- **Engine-Weg:** Modul-Spec noetig (baut auf derselben overnight_context-Funktion wie ONORB-W33a auf)
- **Modul-Spec:** sigcore.py: on_range in overnight_context (faellt bei ONORB-W33a mit ab, +0 Zeilen), Gates tm_on_range_min/max in gates_pass (~14 Zeilen).
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote / Bank-Zeilen (21.09. erweitert):** #138 / TB-03 (Intraday-Kompression -> KLEINERE Folgebewegung, eng gestempelt); #068 (ORB-Break ohne Follow-Through); **HV-44** ("breites Overnight-Value-Gebiet -> ORB-Ausbrueche zuverlaessiger" -- woertlich dieser Weg, mit `orb_exec="close"` als Pruefplan); **HV-43** (POC-Abstand als Gap-Fill-Praediktor); **TV-03** und **AB-03** (Tages-Kompression, im 229er-Block gemessen, 59 Surv / 0 Kandidaten laut SES-W38); **GM-15** (Nacht/Tag-Range-Verhaeltnis ab 2022 niedriger -- **Epochen-Split vor/ab 2022 ist hier Pflicht**); `ideas.json` **"Noise-ORB NQ (Zarattini)" = Validiert** (das 14-Tage-Sigma-Noise-Band ist der Stand der Technik, gegen den `on_range` antreten muss).
- **Research-Fragen:** Gibt es eine Arbeit, die die Overnight-RANGE (nicht den Return, nicht die RV) als Bedingung fuer Opening-Range-Breakouts testet? / Zarattini nutzt ein Noise-Band aus 14-Tage-Sigma; ist die Overnight-Range als Band-Breite je getestet worden?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Arbeit testet die Overnight-RANGE als ORB-Bedingung oder als Band-Breite. Teilstuetze nur indirekt ueber Overnight-Vola -> Intraday-Vola (Cache Z. 386). Eigene Gegenindizien: #074 / Lehre 21 (Overnight-Vola-Filter senkte die Passquote) und #068 (Vola-Spike-Kondition aendert das Follow-Through nicht).
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 6 🆕 -- `ONORB-W39a`: Der Sweep des Nacht-Extrems -- Preis nimmt das Overnight-High/-Low und dreht

- **Weg:** W39 Kreuzen und scheitern am Overnight-High/-Low, beide Richtungen getrennt
- **Mechanismus:** `asian` mit `asia_mode='break_us'` liefert das Level (Nacht-Extrem) und den Null-Schalter; neu ist der Fehlschlag-Arm (**S5**: `as_side='against'` + `as_fail_win`). Entry in die Gegenrichtung, wenn der Preis das Nacht-Extrem nimmt und innerhalb von N Minuten wieder dahinter zurueckkehrt. Zellen: `against` mit Fehlschlag-Fenster in {5, 10, 15, 30} Min, `breakout` (Status quo, 43 Trials) als Vergleichsarm, ungegatet, plus **tick-treues Zufallslevel** (`ctl_random_level`, Lehre 151 -- Pflicht, weil das Nacht-Extrem auf dem Tick-Raster liegt).
- **Why (`entwurf`):** Weil das Overnight-High und das Overnight-Low die einzigen Preise sind, die jeder Teilnehmer ohne Absprache gleich berechnet, haengen dort die Stop-Orders der Nacht-Kohorte in Clustern -- ruhende Liquiditaet, die ein Ausfuehrungsalgo mit Groesse gezielt ansteuert, weil er sie sonst nirgends findet. Der Bruch entsteht in diesem Fall **nicht aus Information, sondern aus dem Abraeumen dieser Stops**: danach ist das Buch jenseits des Levels leer, es gibt keinen Anschluss-Flow, und der Preis faellt in die Range zurueck. Das ist ein Zwangshandel-Argument, kein Prognose-Argument. Es passt zur **Praemisse** #068 (nach einem erfolgreichen Bruch ist der Rest des Tages ein Coinflip -- also traegt nicht der Bruch, sondern sein Scheitern) und zur lebenden Verwandten `i2 on_rev` (94 Trials, 9 Survivors).
- **Engine-Weg:** `asian.trades` `asia_mode='break_us'` (43 Register-Trials, `ctl_null` vorhanden) + **Modul-Spec S5** (~25 Zeilen, gemeinsam mit W5/W13).
- **Vorlauf-Auflage (bindend):** zuerst `260831_fb01_failbreak_NQ/RTY` und `260903_fb01b_failbreak_fixed_NQ/RTY` reparieren und rechnen. Diese vier Dateien implementieren denselben Mechanismus als `maband mb_kind='channel'` + `mb_side='against'` am RTH-Kanal (867 Register-Trials in dieser Achse, 77 Survivors), tragen im File `"status": "pending"` und stehen in `queue.json` auf **`premise_failed`** -- **nie gerechnet, nicht widerlegt**. Traegt der Mechanismus am billigen Level nicht, wird S5 nicht gebaut.
- **Modul-Spec:** S5 (`asian.py`: `as_side='against'` + `as_fail_win`, Muster `mb_side='against'` aus `maband.py` Z. 608-611, ~25 Zeilen; deckt W5, W13 und W39 gemeinsam ab).
- **Buch-Bezug:** neues Bein `NQ_ONSweep`
- **Verwandte Tote / nie gerechnet:** `fb01_failbreak_session_NQ/RTY`, `fb01b_failbreak_fixed_NQ/RTY` (alle `premise_failed`); #068 (Praemisse); #138/AB-14 und #151 Lehre 151 (Level-Placebo-Fehlerklasse -- das tick-treue Zufallslevel ist hier nicht optional); Schwesterkarte SES-W26.
- **Research-Fragen:** Existiert Literatur zum "failed breakout" / "liquidity sweep" auf Index-Futures mit sauberer Fehlschlag-Definition und OOS-Test? / Gibt es eine Quelle, die Stop-Cluster an Session-Extrema direkt misst (Osler 2000/2003 zeigt das fuer FX mit Kundenorderdaten -- gibt es ein Futures-Pendant?)
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Kein Futures-Nachweis fuer Stop-Cluster an Session-Extrema (Osler-Futures-Negativbefund Cache Z. 1217; Turtle-Soup ist nur Folklore, Z. 49). Der naechste Test faellt negativ aus: Mesfin arXiv 2605.04004 Abschn. 4.3, 6.442 Asia-Grabs, Fade -2,20 Punkte (T -14,1), brutto nur 0,2-0,8 Punkte und damit unter der Friktionsdecke -- allerdings auf Bar-Ebene in Asien, nicht am Overnight-High/-Low zum NY-Open. Eigen: #028 (Asia-Fade tot), lebende Verwandte i2 on_rev 9/94.
- **Pflichtzellen:** tick-treues Zufallslevel, `ctl_sides`, Montags-Split [[#W42]], Epochen-Split vor/ab 2022.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 7 -- `ONORB-W34a`: Wo der Open in der Nacht-Range liegt, ist die Schmerzverteilung der Nacht-Kohorte

- **Weg:** W34 Position des Opens in der Nacht-Range, beide Richtungen
- **Mechanismus:** Neue Kennzahl on_pos (Position des 09:30-Opens in der Globex-Range, 0..1) als Richtungs-Bias: oberes Drittel -> Long-Bias, unteres Drittel -> Short-Bias, Mitte -> Kontrollzelle ohne Bias. Getestet als Ersatz-Filter fuer die Richtungsbedingung des Asia-Dir-Beins.
- **Why (`entwurf`):** Weil ein Open am oberen Rand der Nacht-Range bedeutet, dass jeder Nacht-Kaeufer im Gewinn sitzt und jeder Nacht-Verkaeufer im Verlust, ist on_pos eine Aussage ueber die naechste ERZWUNGENE Order (Gewinnmitnahme oder Deckung) und nicht ueber eine Prognose. Sie ist von on_ret unabhaengig: derselbe Nacht-Return kann am Rand oder in der Mitte der Spanne enden. Das Bestandsbein NQ_Asia-Dir benutzt mit asia_dir_thr die grobe Version davon (Bewegung relativ zur Range), aber gemessen am SESSION-Close, nicht am Cash-Open.
- **Engine-Weg:** Modul-Spec noetig (auf der overnight_context-Basis)
- **Modul-Spec:** sigcore.py: on_pos in overnight_context (+~6 Zeilen), Gate tm_on_pos_min/max (~10 Zeilen); fuer den asian-Ast dieselbe Groesse als as_on_pos (~10 Zeilen in asian.py).
- **Buch-Bezug:** NQ_Asia-Dir-USopen_d260820
- **Verwandte Tote / Bank-Zeilen (21.09. erweitert):** #112/#113 (Value-Area-Reversal war Barrieren-Artefakt -- hier kein Beruehrungs-Ereignis, sondern ein Zustand am Open); AR-20 (Asia-Dir-Einzelkonfiguration unter der Familien-Decke); **XA-38** ist **woertlich dieser Weg** und stand die ganze Zeit in der Bank: "die Asien-Range-Position des Preises beim US-Open (oberes oder unteres Drittel der Overnight-Range) traegt Richtungsinformation fuer den RTH-Vormittag", Pruefplan Terzile.
- **Research-Fragen:** Gibt es Literatur zur Position des Cash-Opens innerhalb der Overnight-Range als Praediktor (Market-Profile-Praktikerwissen vs. peer-reviewed)? / Wird die Schmerzverteilung der Nacht-Halter irgendwo quantifiziert (unrealisierter Gewinn/Verlust der Overnight-Kohorte)?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Nur Market-Profile-Praktikerwissen (Cache Z. 554, Konvention) und Blog-Statistiken. Keine peer-reviewte Arbeit zur Position des Cash-Opens in der Overnight-Range, keine Quantifizierung der Schmerzverteilung der Nacht-Halter (Cache 22.09., Negativbefund). Gegenindiz: Mesfin Tab. 5 -- MNQ-Gaps fuellen sich nicht konsistent im RTH.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 8 -- `ONORB-W5a`: Der Fehlausbruch am NY-OR-Level gegen eine gegenlaeufige Nacht

- **Weg:** W5 Kreuzen und scheitern am NY-OR, Gegenrichtung
- **Mechanismus:** Neue Seite as_side='against' plus Fehlschlag-Fenster in asian.py: Level wird beruehrt, Preis kehrt innerhalb von N Minuten hinter das Level zurueck, Entry in die Gegenrichtung. Bedingung: Nacht lief entgegen der Bruchrichtung (tm_on_dir='against').
- **Why (`entwurf`, Engine-Aussage am 21.09.2026 korrigiert):** Weil an einem Fehlausbruch zwei Gruppen gleichzeitig falsch liegen -- die Nacht-Positionierung, die gegen die Bruchrichtung steht, und die Ausbruchs-Kaeufer, die gegen die Nacht kaufen -- liquidieren beide in dieselbe Richtung, sobald der Bruch nicht traegt. Das ist ein Zwangshandel-Argument, kein Prognose-Argument, und es erklaert, warum die Bewegung nach einem gescheiterten Bruch groesser sein sollte als nach einem erfolgreichen (#068: nach erfolgreichem Bruch ist der Rest des Tages ein Coinflip).
- **Engine-Weg (korrigiert):** Der Fehlausbruch-ARM existiert bereits als `maband mb_kind='channel'` + `mb_side='against'` (**867 Register-Trials / 77 Survivors**) -- aber am RTH-Bar-Extrem-Kanal, **nicht am OR-Level**. Fuer das OR-Level bleibt die Spec noetig; sie darf aber erst gebaut werden, nachdem der billigere Vorlauf gerechnet ist.
- **Modul-Spec (unveraendert, aber mit Vorlauf-Auflage):** `asian.py`: `as_side='against'` plus `as_fail_win` (Minuten bis zur Rueckkehr hinter das Level) im `break`-Arm, Muster `mb_side='against'` aus `maband.py` Z. 608-611, ~25 Zeilen. Null-Schalter ist im `break`-Arm bereits vorhanden (`asian.py` Z. 149-156).
- **Vorlauf-Auflage (neu 21.09.):** zuerst die vier vorbereiteten Job-Dateien `260831_fb01_failbreak_NQ/RTY` und `260903_fb01b_failbreak_fixed_NQ/RTY` reparieren und rechnen. Sie tragen im File `"status": "pending"`, stehen in `queue.json` aber auf **`premise_failed`** -- der Mechanismus hat auf dem billigsten Level noch nie eine Zahl gesehen. 25 Zeilen Code davor zu bauen waere Verschwendung.
- **Buch-Bezug:** NQ_ORFail
- **Verwandte Tote / nie gerechnet:** #068 (ORB-Break kein Follow-Through -- das ist hier die PRAEMISSE, nicht der Widerspruch); #068 Pineda-Retest (36 Varianten negativ -- Retest ist der Einstieg NACH dem Bruch, nicht nach dessen Scheitern); **`fb01_failbreak_session_NQ/RTY` und `fb01b_failbreak_fixed_NQ/RTY` (alle vier `premise_failed`)**; Schwesterkarte SES-W26.
- **Research-Fragen:** Existiert Literatur zum 'failed breakout' / 'false break' auf Index-Futures mit sauberer Fehlschlag-Definition und OOS-Test? / Gibt es eine Quelle, die Fehlausbruch-Haeufigkeit als Funktion der Overnight-Positionierung misst?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Arbeit zum Fehlausbruch mit sauberer Definition und OOS-Test auf Index-Futures, und keine zur Haeufigkeit als Funktion der Overnight-Positionierung (Cache Z. 49 / Z. 1217, am 22.09. bestaetigt). Naechste Verwandte Mesfin Abschn. 4.3 ist nach Friktion negativ. Eigene Vorlaeufer fb01/fb01b stehen weiterhin auf premise_failed (nie gerechnet). Die Vorlauf-Auflage bleibt damit bindend.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 9 -- `ONORB-W27a`: Die Nacht, die in sich dreht: Asien hoch, London runter, also Fade-Tag

- **Weg:** W27 Nacht dreht in sich, Fade- und Breakout-Arm
- **Mechanismus:** Getrennte Tageskontext-Spalten asia_ret (19:00-03:00 ET) und eu_ret (03:00-09:29 ET). Gate auf das Vorzeichen-Paar: gleichgerichtet -> Breakout-Arm, gegenlaeufig -> Fade-Arm, plus ungegatete Kontrolle. Erste Messung als Filter auf das Bestandsbein NQ_Asia-Dir.
- **Why (`entwurf`):** Weil zwei Kohorten, die in derselben Nacht gegeneinander handeln, keine gemeinsame Bewertung gefunden haben, startet die US-Sitzung an solchen Tagen ohne Konsens -- und genau dann ist der erste Ausbruch am wahrscheinlichsten ein Fehlausbruch. Unsere Engine kann diesen Zustand heute per Konstruktion nicht sehen: sie fuehrt die Nacht als EINE Zahl (on_ret), in der sich Asien und Europa gegenseitig wegkuerzen. Eine grosse Nacht ohne inneren Konsens sieht damit aus wie eine ruhige Nacht.
- **Engine-Weg:** Modul-Spec noetig
- **Modul-Spec:** sigcore.py: asia_ret/eu_ret/asia_range/eu_range in overnight_context (+~20 Zeilen auf der W33a-Basis), Gates tm_seg_agree in {'agree','against'} (~12 Zeilen).
- **Buch-Bezug:** NQ_Asia-Dir-USopen_d260820
- **Verwandte Tote / Bank-Zeilen (21.09. erweitert):** TN-08 (Europa-Richtung als besserer Bias: 37 Trials im `asian`-Modus, 0 Kandidaten -- dort Europa ALLEIN, hier das Vorzeichen-PAAR); **XA-39** (Europa-Rendite als besserer RTH-Praediktor als Asien, Pruefplan = beide Segmente als getrennte Regressoren); **MO-51** (letzte Globex-Stunde gegen erste RTH-Stunde -- jetzt eigener Weg [[#W45]] / Skelett `ONORB-W45a`); #113 (Session-VAH/VAL-Unterschiede waren reine Vola-Geometrie)
- **Research-Fragen:** Gibt es Arbeiten zur Informations-Uebergabe zwischen Asien- und Europa-Session in Index-Futures (Ito/Hashimoto behandelt FX)? / Wird der intranight-Richtungswechsel irgendwo als Regime-Merkmal fuer den Folgetag genutzt?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Arbeit zur Asien->Europa-Uebergabe und keine zum intranight-Richtungswechsel als Regime-Merkmal in Index-Futures. Ito/Hashimoto (Cache Z. 553) behandelt nur FX-Spot (Cache 22.09., Negativbefund).
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 10 🆕 -- `ONORB-W45a`: Die letzte Nacht-Stunde (08:30-09:30 ET) als eigenes Segment

- **Weg:** W45 Drittes Nacht-Segment, Vor-Open-Fenster
- **Mechanismus:** Neue Tageskontext-Spalten `pre_ret` und `pre_rvol` (08:30-09:29 ET) neben `asia_ret`/`eu_ret` aus `ONORB-W27a`. Gate auf den Opening-Drive-/ORB-Weg: `pre_ret`-Vorzeichen als Richtungsbedingung, `pre_rvol` als Qualitaetsbedingung. Zellen: nur `pre_ret`, nur `on_ret` (Status quo), beide, ungegatet. **Pflicht-Split Makro-Tage gegen Nicht-Makro-Tage** (das Spec-B-Makro-Tageszustands-Modul aus #163 ist gebaut und wird hier wiederverwendet), sonst misst der Weg nur KF-40.
- **Why (`entwurf`):** Weil die US-Makrodaten um 08:30 ET erscheinen, also **vor** dem Cash-Open, ist die letzte Nacht-Stunde nicht das juengste Stueck derselben Nacht, sondern ein Fenster mit einem **anderen Akteur**: dort handeln die Desks, die auf die Zahl reagieren muessen, in einem Buch, das noch duenn ist. Zwei Bank-Zeilen sagen dasselbe aus verschiedenen Richtungen -- **MO-51** (Drift der letzten Globex-Stunde und der ersten RTH-Stunde sind gleichgerichtet, wenn beide Fenster erhoehtes Volumen haben, weil eine grosse Order ueber die Sessiongrenze hinweg fortgesetzt wird) und **KF-40** (ein CPI-Tag-Bias existiert nur in der Phase 08:30-09:30 und ist im RTH tot). Das Geld bleibt liegen, weil `on_ret` als Close-zu-Open-Sprung ueber 17,5 Stunden diese eine Stunde vollstaendig verduennt: eine scharfe Reaktion um 08:31 und eine gleichgrosse Drift um 21:00 sehen in unserer Kennzahl identisch aus.
- **Engine-Weg:** **Modul-Spec S9** (~12 Zeilen auf der S1-Basis). `asian.py` kann das Fenster schon heute einzeln rechnen (`rs_start='08:30'`, `rs_end='09:25'`), aber nicht als Kontextspalte neben Asien und Europa.
- **Modul-Spec:** `sigcore.py`: `pre_ret`/`pre_rvol` (08:30-09:29 ET) in `overnight_context` (~12 Zeilen), Gates `tm_pre_ret_min` / `tm_pre_rvol_min` (~10 Zeilen).
- **Buch-Bezug:** Gate fuer W1/W2/W7, Ersatz-Overlay auf `NQ_Momentum_d260818`
- **Verwandte Tote:** MO-51 und KF-40 (Bank, beide ungebaut); TN-08 (Europa **allein** als Bias, 37 Trials, 0 Kandidaten); XA-39 (Europa gegen Asien als Regressoren); #163 (Spec-B Makro-Tageszustand -- gebaut, hier Pflichtbeilage).
- **Research-Fragen:** Gibt es Arbeiten zur Informationsverarbeitung im Pre-Market-Fenster von Index-Futures (08:30-09:30 ET) als Praediktor fuer die erste RTH-Stunde? / Ist der 08:30-Release-Effekt in Futures bis zum Cash-Open nachweislich vollstaendig eingepreist, oder laeuft er im RTH weiter (KF-40 behauptet Ersteres)?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Teilstuetze fuer ein eigenes Informationsfenster vor dem Cash-Open: Kurov/Sancetta/Strasser/Wolfe JFQA 2019 (ES-Futures, Drift ab ca. 30 Minuten vor dem 08:30-Release, rund 40 Prozent der Anpassung laufen vorher) und Barclay/Hendershott (Aktien, Pre-Open-Handel ist informationsmotiviert). NICHT getestet: die Praediktion der ersten RTH-Stunde und ob der 08:30-Effekt bis 09:30 vollstaendig eingepreist ist -- die KF-40-Frage bleibt offen. Damit staerkste Teilstuetze der offenen Skelette, aber kein Beleg fuer den Praediktor selbst.
- **Pflichtzellen:** Makro-Tage gegen Nicht-Makro-Tage, Montags-Split [[#W42]], Epochen-Split vor/ab 2022. **DST-Kontrolle [[#W49]] entfaellt** -- 08:30/09:30 ET sind US-Anker und wandern mit.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 11 -- `ONORB-W31a`: Nacht-Volumen statt Nacht-Bewegung: hohe europaeische Beteiligung als Trendtag-Bedingung

- **Weg:** W31 Nacht-Volumen als Tor auf den Morgen-Ausbruch
- **Mechanismus (21.09. um den Gegenarm erweitert):** Neue Kennzahl `on_rvol` je Nacht-Segment (Volumen 03:00-09:29 ET gegen den 20-Tage-Median desselben Fensters) als Gate auf den NY-Ausbruchs- und Opening-Drive-Weg. **Beide Vorzeichen in EINER Messung**, weil die Bank sich selbst widerspricht: XA-42/MO-50 sagen Fortsetzung bei hohem Nacht-Volumen, **MO-19 sagt das Gegenteil** (Metaorder-Impact im duennen Buch -> Ruecklauf in der ersten RTH-Stunde). Zellen: `on_rvol` hoch/Fortsetzung, `on_rvol` hoch/Fade, `on_rvol` niedrig, ungegatet. Kontrollzelle: `on_ret` gross bei `on_rvol` niedrig (Bewegung ohne Beteiligung).
- **Why (`entwurf`):** Weil Volumen misst, wie viele echte Institutionelle gearbeitet haben, und weil eine Metaorder, die nachts in Europa laeuft, am US-Open nicht fertig ist, ist hohes Nacht-Volumen der einzige Mechanismus in diesem Konzept, der eine ANHALTENDE Kraft im RTH beschreibt statt einer einmaligen Reaktion auf eine Nachricht. Bewegung ohne Volumen ist dagegen Liquiditaetsluecke und sagt fuer den liquiden Tag nichts. Das Geld bleibt liegen, weil unser RVOL ausschliesslich gegen den Uhrzeit-Median INNERHALB des RTH rechnet und Nacht-Fenster gar nicht kennt.
- **Engine-Weg:** Modul-Spec noetig
- **Modul-Spec:** sigcore.py: on_rvol je Segment in overnight_context (~30 Zeilen auf der W33a-Basis), Gate tm_on_rvol_min/max (~10 Zeilen).
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote / Bank-Zeilen (21.09. erweitert):** VV-19 (ungebaut); **XA-42** (hohes Globex-Volumen = Fortsetzung, niedriges = Reversion -- woertlich dieser Weg); **MO-19** (Gegenthese: hohes ON-Volumen -> Ruecklauf in der ersten RTH-Stunde); **MO-50** (Europa-Kernzeit-Drift bei erhoehtem Volumen -> Fortsetzung); #031 (RVOL als ORB-Filter bestaetigt, aber intraday gerechnet); #021 (Orderflow-Delta tot -- hier reines OHLCV-Volumen, kein Delta)
- **Research-Fragen:** Ist Globex-Nachtvolumen als Praediktor fuer die Trendstaerke des folgenden US-Tages irgendwo peer-reviewed getestet? / Zarattini/Barbon/Aziz finden die ORB-Edge im relativen Volumen bei Aktien -- gibt es ein Futures-Pendant mit Nacht-Volumen?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Kein Globex-Nachtvolumen-Praediktor und kein Futures-Pendant zu Zarattini/Barbon/Aziz gefunden. Cartea et al. (Cache Z. 1275) laufen in die GEGENRICHTUNG (Tagesvolumen -> Overnight-Return, Aktien). Eigen: #068 / #125 -- RVOL uebertraegt sich auf NQ nicht.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 12 -- `ONORB-W35a`: Der Ausgang des London-Ausbruchs als Vorzeichen fuer den NY-Ausbruch

- **Weg:** W35 Kaskade London-Ausgang -> NY-Ausbruch
- **Mechanismus:** Vorberechnete Tageskontext-Spalte lon_break_ok in {+1 gelaufen, -1 gescheitert, 0 kein Bruch} aus der London-OR, als Gate auf den NY-ORB-Weg (W1/W2) gejoint wie gex_rank. Drei Zellen plus ungegatete Kontrolle.
- **Why (`entwurf`):** Weil der Tag bis 09:30 bereits EINEN Ausbruchsversuch durchgespielt hat, ist die Frage am US-Open nicht mehr nur 'war die Nacht gross', sondern 'hat die Ausbruchs-Mechanik heute funktioniert'. Ein gelaufener London-Bruch zeigt, dass Liquiditaet heute nachgibt statt zu absorbieren; ein gescheiterter zeigt das Gegenteil, bevor die US-Sitzung beginnt. Das Geld bleibt liegen, weil der Weg zwei Rechnungen hintereinander braucht und kein einzelner Job das heute abbilden kann -- genau das ist der Grund, warum es kaum jemand systematisch macht.
- **Engine-Weg:** Modul-Spec noetig
- **Modul-Spec:** Neues Vorberechnungs-Skript (Muster _spx_daily_context): lon_break_ok je Handelstag aus asian.load_full als CSV/Parquet, dann in sigcore.daily_context joinen wie gex_rank/vix_rank (~45 Zeilen gesamt). Erst NACH ONORB-W10a sinnvoll, sonst wird ein Ausgang gelesen, dessen Definition nie geprueft wurde.
- **Buch-Bezug:** NQ_Momentum_d260818
- **Verwandte Tote:** #028 (London-Break selbst tot -- hier wird der Trade nicht gehandelt, nur sein Ausgang gelesen)
- **Research-Fragen:** Gibt es Literatur zu session-uebergreifenden Breakout-Kaskaden (Europa-Ausbruch als Praediktor fuer US-Ausbruch)? / Wird 'Liquiditaet gibt heute nach vs. absorbiert' irgendwo als Tageszustand quantifiziert und mit Breakout-Erfolg verknuepft?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Literatur zu Europa->US-Breakout-Kaskaden und keine zu 'Liquiditaet gibt nach vs. absorbiert' als Tageszustand (Cache 22.09., Negativbefund). Eigen: der London-Breakout wurde in #028 (46 Configs) mitgetoetet -- der 'London-Ausgang' als ZUSTANDSVARIABLE ist damit kaum gemessen, nicht widerlegt.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

### Rang 13 (abgewertet von 8) -- `ONORB-W10a`: Die London-EIGENE Opening Range (03:00-03:30 ET), bedingt auf die Asien-Richtung

- **Weg:** W10/W11 Durch die London-OR hindurch, beide Richtungen getrennt
- **Mechanismus:** asian.trades mit asia_mode='break', rs_start='03:00', rs_end='03:30', tr_start='03:30', tr_end='09:25', slippage_ticks=2.0 vorab gesetzt. Bedingung: Bruchrichtung stimmt mit der Asien-Richtung ueberein (as_on_dir='agree'). Kontrollzellen: ungegatet und 'against'.
- **Why (`entwurf`, am 21.09.2026 neu formuliert -- die alte Abgrenzung trug nicht):** Weil London um 03:00 ET ein acht Stunden in Asien gelaufenes Buch uebernimmt, sind die ersten 30 Minuten die Preisfindung dieser Uebergabe. **Abgrenzung zum Kill #028, ehrlich:** #028 hat den London-Breakout in allen Varianten getoetet, **inklusive London-IB** -- die London-eigene Range ist mitgetoetet, die alte Behauptung (#028 habe nur den Asien-Range-Break bei London-Open getroffen) war falsch. **Der einzige neue Bestandteil ist die Asien-Richtungsbedingung**: nicht "London bricht aus", sondern "London bricht **in Asiens Richtung** aus", und nur diese Bedingung darf den Why tragen. Trifft sie nicht, ist der Weg ein Aufwaermen und wird nicht gerechnet. Gegenbefund, der vor dem Rechnen auf dem Tisch liegt: derselbe Opening-Drive-Mechanismus hat im Europa-Fenster (`firstbar_ematrail`, `session='eu'`) **960 Register-Trials und 0 Survivors**, waehrend er im NY-Fenster mit 24h-Basis 109 von 960 liefert.
- **Engine-Weg:** engine-faehig fuer den Bruch selbst (asian.py Z. 132-156, ctl_null vorhanden), Modul-Spec nur fuer die Nacht-Bedingung
- **Modul-Spec:** asian.py: as_on_dir/as_on_ret_min aus den bereits geladenen 24h-Daten im selben Loop (die Daten liegen in load_full schon vor, rmask-Technik), ~35 Zeilen -- die billigste Spec der Karte.
- **Buch-Bezug:** NQ_LondonOR
- **Verwandte Tote:** #028 (London-Breakout **inkl. NR-Filter und London-IB**, 46 Configs, ALLE Varianten getoetet); `firstbar_ematrail` `session='eu'` (960 Trials, 0 Survivors); `260825_eusession_break_ES.json` (**`premise_failed`** -- die ES-Uebertragung ist an der Praemisse gestorben); `260821_asian_EUbreak_NQ.json` und `260821_asian_EUdir_NQ.json` (gelaufen, 17 bzw. 18 Trials); #033 (doppelte Kosten toeten enge Spreads -- hier einfache Kosten, aber duennes Buch)
- **Research-Fragen:** Gibt es eine Arbeit, die die LONDON-eigene Opening Range auf Index-Futures testet (nicht den Asia-Range-Break bei London-Open)? / Wie gross ist der reale Spread/Slippage auf MNQ im Fenster 03:00-09:30 ET gegenueber dem RTH -- gibt es eine belastbare Zahl?
- **Research-Stand (22.09.2026, `research-scout`):** `offen` -- Keine Arbeit zur London-EIGENEN Opening Range auf Index-Futures. Das eigene Logbuch spricht stark dagegen (#028: London-Break inklusive London-IB, 46 Configs tot; firstbar_ematrail eu 0/960). Einziger neuer Baustein bleibt die Asien-Richtung, und die ist ungemessen. Zusaetzlich kein verifizierbarer MNQ-Spread fuer 03:00-09:30 ET -- es gibt nur die 2-Punkte-Pauschale aus Mesfin arXiv 2605.04004. Die Auflage 'erst rechnen, wenn Rang 1-11 nichts getragen haben' bleibt.
- **Auflage vor dem Rechnen (neu 21.09.):** (1) der Why muss allein auf der Asien-Richtungsbedingung stehen, (2) `slippage_ticks=2.0` vorab, (3) DST-Kontrollweg [[#W49]] als Pflichtspalte, (4) erst rechnen, wenn Rang 1-11 nichts getragen haben.
- **Stempel:** _offen, noch nicht durch `variant-scout` + `strategy-auditor`_

---

## Modul-Specs (was in der Engine fehlt)

| # | Wo | Was | grob Zeilen | traegt Wege |
|---|---|---|---|---|
| S1 | `sigcore.py` | `overnight_context(symbol)` aus `asian.load_full`: `on_range`, `on_sigma`, `on_er`, `on_rvol`, `on_pos`, `asia_ret`/`eu_ret` je Globex-Tag, Cache wie `_CTX_CACHE`, Join in `daily_context` | ~70 + 8 | W27, W29-W34 |
| S2 | `tsmom.py` | `tm_on_dir` in {`agree`,`against`}, greift NACH der Richtungsbestimmung in `_trades()` | ~20 | W24-W26 |
| S3 | `tsmom.py` / `sigcore.gates_pass` | `tm_on_range_min/max`, `tm_on_rvol_min/max`, `tm_on_pos_min/max`, `tm_seg_agree`, `tm_stop_mode="on_sigma"` | ~60 | W29-W34 |
| S4 | `asian.py` | `as_on_ret_min/max`, `as_on_dir`, `as_on_pos` aus dem schon geladenen 24h-Frame im selben Loop | ~35 | W1, W2, W4, W10-W13 |
| S5 | `asian.py` | `as_side="against"` + `as_fail_win` (Fehlausbruch-Arm im `break`-Zweig) | ~25 | W5, W13 |
| S6 | `qbt._orb_trades` + `controls.py` | `tm_null` im ORB-Modus + `orb` in die `ctl_null`-Liste | ~10 + 2 | macht den ganzen ORB-Ast `deploy_ready`-faehig |
| S7 | `sigcore.daily_context` | `gap` vom `on_ret` trennen (echter Gap gegen Globex-Close) | ~6 | W23, Register-Hygiene |
| S8 | neues Vorberechnungs-Skript | `lon_break_ok` je Handelstag, Join wie `gex_rank` | ~45 | W35 |
| **S9** 🆕 | `sigcore.py` | `pre_ret`/`pre_rvol` (08:30-09:29 ET) als **drittes** Nacht-Segment auf der S1-Basis, plus Gates | ~12 + 10 | W45 |
| **S10** 🆕 | `sigcore.py` | `on_path` (Summe der absoluten Globex-Bar-Returns) fuer die Absorptions-Quadranten Pfad-gegen-Sprung | ~10 | W43 |
| **S11** 🆕 | `maband.py` | `mb_vwap_anchor='globex'` plus Overnight-POC als Level (`mb_vwap_anchor` kennt heute nur `session\|hi\|lo\|rand_time`, Z. 75/425-429) | ~30 | W41, **nur der Ziel-Arm** -- der Cross-Arm ist nach #108 tot |
| **S12** 🆕 | `qbt._orb_trades` | `or_min` adaptiv aus `on_range`/`on_sigma` statt fest (setzt S1 voraus) | ~15 | W46 |
| **S13** 🆕 | Auswertung, **kein Code** | DST-Split (US-Sommerzeit / EU-Sommerzeit / beide / keine) als Pflichtspalte fuer jedes 03:00-ET-Fenster | 0 | W49, Pflichtbeilage zu W10-W14, W36, W48 |
| **S5 erweitert** | `asian.py` | `as_side='against'` + `as_fail_win` gilt jetzt auch im `break_us`-Zweig | +0 | W5, W13, **W39** |

**S1 ist der Hebel:** eine Funktion traegt nach dem Nachtrag **zehn** Wege (W27, W29-W34, W43, W45, W46). S6 ist die Hygiene-Pflicht: ohne sie ist jeder ORB-Kandidat per Konstruktion Bank-Material, egal wie gut er rechnet. **S13 kostet nichts und wurde trotzdem vergessen** -- die erste Fassung hat das ungepruefte DST-Verhalten von `asian.load_full` selbst unter "Was NICHT geprueft" gelistet und daraus keinen Kontrollweg gemacht.

---

## Offene Research-Fragen (fuer `research-scout`, nicht selbst beantwortet)

1. Position in der Opening Range (`rangepos`) gegen reinen Return ueber dasselbe Fenster -- gibt es einen direkten Vergleich als Praediktor?
2. Ab welcher Overnight-Bewegung gilt eine Nacht als "Preisfindung" statt Rauschen? Belegte Schwelle in Sigma oder Prozent?
3. Overnight-RV explizit als **Stop-Skala** (nicht als Prognosevariable) gegen ATR getestet?
4. Ist der Overnight-RV -> Intraday-RV-Zusammenhang auf NQ-Futures im Fenster 2023-2026 noch da, oder verfallen wie der Overnight-Drift?
5. Overnight-Return als **bedingtes Tor** statt als eigenstaendiges Signal -- gibt es Evidenz fuer Conditioning statt Prediction?
6. Interaktion der Vorzeichen von Overnight- und Intraday-Segment am selben Tag (Lou/Polk/Skouras trennen sie, verknuepfen sie aber nicht).
7. Overnight-RANGE (nicht Return, nicht RV) als Bedingung fuer Opening-Range-Breakouts?
8. Position des Cash-Opens in der Overnight-Range als Praediktor -- Praktikerwissen oder peer-reviewed?
9. Informations-Uebergabe Asien -> Europa in Index-Futures (Ito/Hashimoto behandelt FX).
10. LONDON-eigene Opening Range auf Index-Futures getestet (nicht der Asia-Range-Break bei London-Open)?
11. Realer Spread/Slippage auf MNQ im Fenster 03:00-09:30 ET gegenueber RTH -- belastbare Zahl?
12. Session-uebergreifende Breakout-Kaskaden (Europa-Ausbruch als Praediktor fuer US-Ausbruch)?
13. Globex-Nachtvolumen als Praediktor fuer die Trendstaerke des folgenden US-Tages, peer-reviewed?
14. Failed-Breakout auf Index-Futures mit sauberer Fehlschlag-Definition und OOS-Test?

**Nachgetragen 21.09.2026 (aus den Wegen W39-W50):**

15. Take-Profit-Distanz oder Haltedauer explizit an der **Overnight-Vola** bedingt (nicht am Vortages-ATR) -- gibt es das?
16. Optimale Haltedauer nach einem Opening-Range-Bruch als Funktion der **erwarteten** Tages-Vola (Optimal-Stopping-Rahmen)?
17. Stop-Cluster an Session-Extrema direkt gemessen -- Osler 2000/2003 zeigt es fuer FX mit Kundenorderdaten; gibt es ein Futures-Pendant?
18. Informationsverarbeitung im Pre-Market-Fenster 08:30-09:30 ET als Praediktor fuer die erste RTH-Stunde?
19. Ist der 08:30-Release-Effekt in Futures bis zum Cash-Open vollstaendig eingepreist, oder laeuft er im RTH weiter (KF-40 behauptet Ersteres)?
20. Montags-Overnight (Freitag-Schluss bis Montag-Open) als eigener Prozess -- gibt es eine Quelle, die ihn getrennt modelliert statt nur als Wochentags-Dummy?
21. Overnight-**POC/TWAP** (volumengewichtet) gegen den reinen Overnight-VWAP als Level -- misst das jemand getrennt? Unsere eigene Messung (#108) hat nur VWAP-Varianten getestet, keinen POC.
22. Globex-**Pfadlaenge** gegen Gap (Absorption, TN-06) -- existiert eine Arbeit, die Brutto-Pfad und Netto-Sprung derselben Nacht gegeneinander stellt?
23. OR-Definition ueber Volumen oder Vola statt ueber eine feste Minutenzahl (VV-14) -- gibt es einen belegten Vergleich?
24. Sommerzeit-Umstellung als Robustheitstest fuer Session-Effekte -- macht das jemand systematisch?

---

## Was NICHT geprueft wurde

- Keine Websuche (das ist `research-scout`); alle zitierten Papers stammen aus [[Research-Cache]].
- Kein Backtest, kein Job eingereiht, nichts in `queue.json`, `hypothesis_bank.py`, eine Hypothesen-Bank, `book_state*.json` oder eine bestehende Projekt-Karte geschrieben.
- ~~**Groesste bekannte Luecke:** die 500 `premise_failed`-Jobs wurden nicht einzeln geprueft~~ -- **am 21.09. teilweise geschlossen.** Gezielt nachgesehen und in die Karte eingetragen: `hyp_TN03_NQ`, `hyp_TN05_NQ`, `hyp_TN10_NQ`, `hyp_CR02_ES`, `hyp_AB11_NQ`, `gen_i2_on_rev_ES/RTY/YM`, `gen_asian_fade_break_ES/RTY`, `eusession_break_ES`, `fb01_failbreak_session_NQ/RTY`, `fb01b_failbreak_fixed_NQ/RTY`. **Die uebrigen rund 480 `premise_failed`-Jobs sind weiterhin nicht einzeln durchgesehen.**
- ~~DST-Verhalten von `asian.load_full` gelesen, aber nicht geprueft~~ -- immer noch ungeprueft, **aber jetzt als Kontrollweg [[#W49]] und Modul-Spec S13 gefuehrt** statt nur als Fussnote.
- Die 14 alten `orb*_*.py`-Einzelskripte nicht gelesen; die ORB-Staende stammen aus [[Strategie-Logbuch]], `ideas.json` und eigenen Register-Countern.
- **Neu offen nach dem Nachtrag:** (1) Die Bank-Zeilen `HV-07`, `HV-11`, `VV-20`, `VV-48`, `VV-49`, `ZF-06` sind im Inventar genannt, haben aber weiterhin keinen eigenen Weg -- sie gehoeren beim naechsten Lauf gegen die Wege-Liste geprueft. (2) Der Epochen-Split vor/ab 2022 (GM-15) ist als Pflichtzelle eingetragen, aber nirgends gemessen. (3) Die Trade-Zahl je ON01-Zelle wurde nicht nachgeschlagen -- "0 von 18 Survivors" in der Kontrollzelle koennte auch ein Power-Problem sein (Frage an `quant-statistician`). (4) Der `#108`-Befund (`on_frozen` / `globex`-VWAP gegen Placebo) wurde aus dem Logbuch zitiert, die zugrundeliegenden Zahlen nicht nachgerechnet.

---

## Dateien dieses Laufs

- Report: `C:\Users\maxlk\Projects\trading-data\engine\discovery\scout_reports\familien_overnight-bias-orb_260921.md`
- Skelette (direkt als `args.hypotheses` fuer `ein-weg`): `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\familien_overnight-bias-orb_260921.json`
- Diese Karte ist das lebende Register je Weg: `verdict-auditor` traegt die Stempel hier nach, Nummern werden nie umbenannt.
- **Nachtrag 21.09.2026:** W39-W50 ergaenzt, elf Staende korrigiert, sechzehn uebersehene tote Verwandte eingetragen. Report und JSON tragen dasselbe Datum und wurden im selben Zug fortgeschrieben.
- **Research-Rueckschrieb 22.09.2026:** `why_status` je Skelett in Karte UND JSON nachgetragen (1 belegt, 12 offen, 0 widerlegt, 0 raus), Why von `ONORB-W33a` ueberarbeitet. Der Report vom 21.09. bleibt unveraendert (Lauf-Dokument).

## Verwandte Notizen

[[Session Momentum Wege-Karte]] · [[VWAP-Offensive]] · [[RVOL Wege-Karte]] · [[ADX Wege-Karte]] · [[Rundzahlen Wege-Karte]] · [[Fibonacci Wege-Karte]] · [[Strategie-Logbuch]] · [[Research-Cache]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Discovery-Runner v2]] · [[Alpha-Suche]] · [[Strategie-Familien]] · [[Familien-Scout Agent]] · [[Buch-Workflow]]
