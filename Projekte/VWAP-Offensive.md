---
tags: [projekt, trading, alpha-suche, vwap]
erstellt: 2026-09-10
status: aktiv
ziel: Buch-Passquote verbessern über den VWAP-Zweig
---

# VWAP-Offensive

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile hier muss am Ende die Frage beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 10.09.2026 auf Ansage von Max ("alle Punkte abdecken, mit Research und Why, Hauptprio Buch verbessern"). Vorlauf: Inventar über Register (47.370 Trials), Queue, [[Strategie-Logbuch]] und die Bank-Notiz [[Hypothesen-Bank (Momentum & Averages)]].

---

## Die drei harten Randbedingungen

**1. Alles Neue muss in `maband`.** `_null_direction` existiert auf der Box nicht. Damit gilt `job_generator.py:298`: nur `tsmom` und `maband` haben einen Null-Schalter (`controls.py` `ctl_null`), **alle anderen 20 Modi können nie `deploy_ready` werden** und werden von `promote_next.py:134` weggeworfen. Das Buch-Bein `NQ_VWAP-Pullback` läuft auf `mode="vwap_pullback"` und hätte über die Pipeline nie entstehen können. Wer eine VWAP-Idee als eigenes Modul baut, verbrennt Box-Zeit ohne mögliche Konsequenz.

**2. Ersatz schlägt Neuzugang.** Nach #139 B3 hat der Weg "neues Bein" noch nie einen Kandidaten geliefert. Standard für jeden VWAP-Job: `replaces_leg: "NQ_VWAP-Pullback"`, `book_marginal: true`. Neue Beine nur, wenn die Idee mechanistisch etwas anderes tut als jedes Bestandsbein.

**3. Reversion an der VWAP ist tot, Continuation lebt.** Insight #211 und #097, gestützt auf Gao/Han/Li/Zhou (JFE 2018) und auf eigene Zahlen. Jede Zeile, die auf Mean Reversion am VWAP hinausläuft, braucht einen neuen Grund, warum sie diesmal anders ausgeht.

---

## Was schon gemessen ist (Register-Stand 10.09.2026)

146 Trials mit `mb_kind="vwap"`, plus 128 auf `mode="vwap_pullback"` und 163 auf `i2/vwap_pull`. Verteilung der Signalarten:

| Signalart | Trials | Survivors | Urteil |
|---|---|---|---|
| `side` (Preisseite) | 61 | 0 | ohne Kandidat |
| `pullback` (nah am VWAP) | 52 | 0 | ohne Kandidat |
| `reclaim` | 27 | 0 | ohne Kandidat |
| `dist` (Überdehnung, **Fade**) | 5 | 0 | **negativ, nicht neutral** |

Die Fade-Zahlen im Detail, weil sie eine ganze Familie schließen:

| Config | Trades | PF | Gates |
|---|---|---|---|
| k=2,0 NQ (AW-09b) | 2.494 | 0,87 | alle 6 gerissen |
| k=2,5 NQ (AW-09b) | 1.273 | 0,81 | alle 6 gerissen |
| k=1,0 Anker Tagestief NQ | 5.354 | 0,91 | alle 6 gerissen |
| k=1,0 Anker Tagestief ES | 5.336 | 0,77 | alle 6 gerissen |

**Leere Achsen über alle 146 VWAP-Trials** (Stand nach Register-Nachprüfung am 10.09.2026): `tm_rvol_min` 0-mal gesetzt, `tm_delta_min` 0-mal, `tm_vwap_side` 0-mal, `mb_side="against"` 0-mal, `mb_invert` 0-mal, `mb_rand_level=True` 0-mal, Stop-Schätzer `range` und `points` 0-mal, Sigma-Stop 1-mal.

**Korrektur:** die erste Fassung zählte auch den Session-Split als frei. Das stimmt nicht, `mb_start_min` ist über die VWAP-Trials rund 64-mal gesetzt (Werte 15/60/90/120/180/240) und `tm_cutoff_min=330` 4-mal; frei ist die Achse nur auf dem `dist`-Arm. Ebenso ist `tm_ema_confirm` 12-mal gesetzt (immer Wert 100), frei sind dort nur EMA 12 und 20.

**⚠️ Phantom-Achsen, wichtig für jeden künftigen Job:** im VWAP-Zweig haben `mb_norm`, `mb_ma`, `mb_fast`, `mb_slow`, `mb_third`, `mb_src`, `mb_thr` und `mb_confirm` **null Wirkung**. `_norm()` wird nur aus den Zweigen `cross`, `dist` (MA), `price_ma` und `slope` aufgerufen (`maband.py:173/182/191`), der VWAP-Zweig rechnet sein `z` selbst und liest `mb_thr`/`mb_confirm` gar nicht. Jede dieser Achsen in einem Grid erzeugt **bitgleiche Trades unter verschiedenen Register-Hashes**, hebt also die Zufallsdecke und liefert null Information. Einzige Ausnahme: `mb_band_n` wirkt indirekt, sobald `tm_stop_mode="range"`.

**Prämissen-Friedhof:** AW-02, AW-05, AW-09, AW-11, AW-14 stehen bei 1 bis 2 Trials. Das heißt nicht "getestet und tot", das heißt **Prämisse gescheitert, Grid nie gerechnet**. Bei AW-05 und AW-14 ist das besonders teuer, siehe unten.

---

## Die VWAP-Familien

Zwölf Mechanismus-Klassen. Das ist die Landkarte: was kann man am VWAP überhaupt handeln. Jede Familie mit ihrem Why-Kern, den zugeordneten Hypothesen und der ehrlichen Lücke. Die Angabe "Strategie-Familie" ordnet in Max' bestehende fünf [[Strategie-Familien]] ein, damit die Taxonomien nicht auseinanderlaufen.

### V1 — Lage und Seite
**Mechanismus:** wo steht der Preis relativ zum VWAP, und wie lange stand er dort.
**Why-Kern:** der Session-VWAP ist die Benchmark der Ausführungsalgos. Wer darüber kauft, liegt schlechter als der Tagesdurchschnitt, und das erzeugt Handlungsdruck.
**Strategie-Familie:** Intraday Bias / Trend Following.

| Hypothese | Stand |
|---|---|
| AW-06 Zeitanteil über VWAP als Tagesbias | 49 Trials, kein Kandidat |
| AW-13 VWAP-Seite als Richtungsfilter für Momentum-Beine | 24 Trials, kein Kandidat |
| AW-10 RTH-Open relativ zum Globex-VWAP | ungebaut, braucht Globex-Anker |

**Lücke:** die Familie ist auf NQ breit gemessen und liefert nichts. AW-10 ist der einzige unverbrauchte Rest, weil er einen **anderen Referenzpunkt** benutzt statt denselben nochmal.

### V2 — Distanz und Überdehnung
**Mechanismus:** Abstand Preis zu VWAP, in Sigma gemessen, als Signal.
**Why-Kern:** je weiter der Preis vom durchschnittlichen Einstand entfernt ist, desto größer der Druck auf die schlechter liegende Seite. Offene Frage ist nur das Vorzeichen.
**Strategie-Familie:** Mean Reversion (Fade) bzw. Trend Following (Continuation).

| Hypothese | Stand |
|---|---|
| AW-09 / AW-09b Überdehnung als Reversionssignal | 5 Trials, **negativ**, Familie geschlossen |
| **Continuation ab Überdehnung** | **heute baubar, nie gemessen** |

**Korrektur 10.09.2026 (zwei `variant-scout`-Läufe unabhängig):** die ursprüngliche Fassung dieser Notiz behauptete, die Gegenrichtung sei nicht parametrisierbar. Das ist falsch. `maband.py:307` ist zwar fest auf Reversion verdrahtet (`return -1 if z > 0 else 1`), die Richtungsumkehr sitzt aber eine Ebene höher: `maband.py:401` dreht über `mb_side="against"` bzw. `mb_invert=True` das Ergebnis **jedes** `mb_kind`. Continuation ab Überdehnung braucht also keine Modul-Änderung. Über alle 146 VWAP-Trials ist `mb_side="against"` **null-mal** gesetzt, `mb_invert` ebenfalls nie: die Achse ist frei und unbelastet.

**Was wirklich fehlt, ist die ATR-Normierung.** `maband.py:302` normiert ausschließlich mit einem session-kumulativen, ungewichteten Sigma. Das Maß, das #097 als einzigen belegten VWAP-Effekt nachgewiesen hat, ist aber `vwap_dist_min_atr`. Mit der Sigma-Normierung testet man genau die Größe, an der die Fade-Familie schon gerissen ist. Aufwand rund 15 Zeilen (`mb_vwap_dnorm`), Haken: `_event` bekommt den Tageskontext heute nicht durchgereicht. Gleichzeitig macht unser Buch-Bein genau diese Gegenrichtung: `vwap_pullback.py:73` handelt erst ab `vwap_dist_min_atr = 2,5` in Trendrichtung, und #097 hat den Distanz-Filter als einzigen Eingriff nachgewiesen, der die Familie von "schadet dem Buch" auf "neutral" hebt (monoton steigend bis 2,5 ATR, in allen 11 Jahren positiv, Gegenprobe nahe am VWAP durchgehend negativ). **Der einzige belegte VWAP-Effekt ist also in der Discovery-Pipeline nicht baubar.**

### V3 — Annäherung und Pullback
**Mechanismus:** Rücklauf an den VWAP im intakten Trend als Einstiegs-Timing.
**Why-Kern:** Ausführungsalgos müssen am VWAP nachkaufen, das erzeugt eine wiederkehrende Nachfrage genau dort.
**Strategie-Familie:** Trend Following.

| Hypothese | Stand |
|---|---|
| AW-01 Bestandsbein mit heutigem Engine-Stand | 17 Trials, Bein läuft live |
| AW-11b Reclaim gegen Pullback | 49 Trials, kein Kandidat |

**Lücke:** `mb_vwap_evt="pullback"` verlangt `near = abs(c - vw) <= k*sd`, also **nah** am VWAP. Das ist genau die Seite, die #097 als die schlechtere nachgewiesen hat. Die maband-Reparametrisierung des Buch-Beins testet damit den Mechanismus systematisch falsch herum. Erklärt auch, warum alle `gen_maband_combo_vwap*`-Jobs in der Prämisse sterben (16 Jobs, alle `premise_failed`).

### V4 — Kreuzung und Kontrollwechsel
**Mechanismus:** das Durchqueren des VWAP als Ereignis.
**Why-Kern:** eine Rückeroberung zeigt, dass die Gegenseite das Level nicht halten konnte.
**Strategie-Familie:** Trend Following.

| Hypothese | Stand |
|---|---|
| AW-11b Reclaim-Arm | 27 Trials, kein Kandidat |
| AW-07 Kreuzungszähler als Regime-Gate | ungebaut |

**Kontamination beachten:** der verwandte Berührungszähler ("erste Berührung ist das A+-Setup") ist in #097 gekippt (IS +0,036, OOS −0,039) und hat keine Primärquelle. AW-07 misst etwas anderes (Anzahl Kreuzungen als Tagescharakter, nicht als Entry-Qualität), muss diesen Unterschied aber im Why ausdrücklich tragen, sonst ist es dieselbe Folklore.

### V5 — Ankerwahl
**Mechanismus:** ab welchem Zeitpunkt der VWAP gerechnet wird.
**Why-Kern:** der Anker bestimmt, wessen Einstandspreis abgebildet wird.
**Strategie-Familie:** Trend Following / Intraday Bias / Swing.

| Hypothese | Stand |
|---|---|
| AW-02 Anker am Tagesextrem | 1 Trial, Prämisse gescheitert |
| AW-03 Event-Anker (FOMC, CPI, OpEx) | ungebaut |
| AW-04 Mehrtages-VWAP als Swing-Level | ungebaut |
| AW-10 Globex-VWAP | ungebaut |

**Lücke und Warnung:** die Ankerwahl ist der eigentliche Freiheitsgrad dieses Zweigs, **jeder Anker ist ein Trial**. Ohne die Kontrolle V12 ist jede Zahl aus dieser Familie Multiple Testing. Reihenfolge deshalb zwingend: erst V12, dann V5.

### V6 — Bandbreite und Struktur
**Mechanismus:** nicht die Lage zum VWAP, sondern die **Breite** der Verteilung um ihn herum als eigenes Maß.
**Why-Kern (Entwurf):** eine enge Bandbreite heißt, dass sich die Marktteilnehmer über den fairen Preis einig sind und noch kein Positionsaufbau stattgefunden hat. Eine Ausdehnung heißt, dass neue Information verarbeitet wird.
**Strategie-Familie:** Intraday Bias (als Regime-Gate).

| Hypothese | Stand |
|---|---|
| **keine** | **Familie komplett leer** |

**Hier muss Research neue Edge suchen.** Zwei Ansätze für die Suche:
- Bandbreite bis 11:00 als Prognose für den Nachmittags-Trendtag. Zulässig, weil bis 11:00 bekannt (Lehre 63: Zeitstempel zuerst prüfen).
- Band-Expansionsrate als Trigger statt als Filter.

Vorsicht: #139 (AR-17) hat gezeigt, dass Vola-Konditionale im Modell tragen, mit diesem Sample aber nicht auflösbar sind. Diese Familie muss erklären, warum sie nicht dasselbe Schicksal hat.

### V7 — Steigung und Dynamik
**Mechanismus:** die Änderungsrate des VWAP selbst.
**Why-Kern:** die Steigung misst die Richtung des kumulierten Flow, träger als der Preis, dafür weniger verrauscht.
**Strategie-Familie:** Trend Following.

| Hypothese | Stand |
|---|---|
| AW-08 VWAP-Steigung als Signal | ungebaut |

**Lücke:** das Falsifikationskriterium steht schon in der Bank und ist scharf: trägt die Steigung nicht mehr als der Preis, ist sie nur ein geglätteter Preis. Muss gegen `tsmom` gleicher Fensterlänge gemessen werden, sonst ist es eine Doppelzählung gegen die Zufallsdecke. Als Signal wahrscheinlich schwach, als **Gate** noch offen.

### V8 — Exit-Geometrie
**Mechanismus:** VWAP und seine Bänder als Ziel und Stop, statt fester R-Vielfacher.
**Why-Kern:** die Bänder messen die typische Abweichung der Ausführung. Wenn irgendwo ein natürliches Kursziel liegt, dann dort.
**Strategie-Familie:** Trend Following.

| Hypothese | Stand |
|---|---|
| AW-05 Bänder als Ziel und Stop | 1 Trial, Prämisse gescheitert, Grid nie gerechnet |

**Korrektur 10.09.2026 (`variant-scout`), der ursprüngliche Why trägt nicht:** die erste Fassung begründete V8 mit "RR unter 1, also ist der Exit der Haupthebel". Das Buch-Bein steht auf `sl_pts=80` und `tp_pts=120` (`vwap_pullback.py:71-72`), also **RR 1,5**. Die 40 waren v7 und sind seit 16.08.2026 überholt (#101/#102). Zweitens ist die Ziel-**Distanz** bereits ausgemessen: #101 fuhr SL fest 80 gegen TP 20 bis 240, der Buch-Beitrag ist von RR 0,5 bis 3,0 durchgehend "besser" mit +1,6 bis +2,0 pp, die Unterschiede liegen im Rauschen. Ein Level-Ziel kann also nicht über die Distanz gewinnen.

**Der einzig verbliebene Freiheitsgrad ist die Konditionierung:** dass die Zieldistanz mit der Tages-Dispersion atmet, statt fest zu sein. Nur darauf darf der Why lauten, sonst ist V8 ein Re-Run von #101.

**Geometrie-Ausschluss, der die Familie halbiert:** `sigcore.py:541-547` verwirft jeden Trade, dessen Ziel hinter dem Entry liegt. "Ziel gleich VWAP" und "Ziel gleich Gegenband" setzen damit zwingend einen **Fade**-Entry voraus und erben dessen Friedhof. Bei einem Continuation-Entry ist nur "Band in Trade-Richtung" geometrisch gültig.

**Baubarkeit: 30 echte Arten, davon heute null.** maband hat keinen Pfad, der ein Preis-Level als Ziel oder Stop akzeptiert, und `_event()` wirft `vw` und `sd` nach der Signalprüfung weg. Nach einem kleinen Patch (Level-Export plus `tm_exit="level"`) sind es 5, mit dem Sigma-Fix 15. Ein **mitlaufendes** Level existiert in der ganzen Engine nicht: `sigcore.simulate_trade` hält `target` als Skalar, und `qbt._trail_stop` kann nur enger werden, während ein VWAP sich auch entfernen kann. Das wäre ein Eingriff in die Ausführungsschicht.

Zusatzbefund: **AW-05 misst nicht, was ihr Titel behauptet.** `hypothesis_bank.py:1116-1122` fährt `tm_stop_mode="sigma"` (das ist `sigma_prev` aus dem Tageskontext, nicht das VWAP-Band) und `tm_exit="rr"` mit `tm_target_r`, also genau das feste R-Vielfache, gegen das die Hypothese antreten soll. Die Zeile gehört ersetzt, nicht wiederbelebt.

### V9 — Differenzen und Relative Value
**Mechanismus:** VWAP gegen eine zweite Referenz stellen statt gegen den Preis.
**Why-Kern:** die Differenz VWAP minus TWAP zeigt, ob das Volumen mit oder gegen die Bewegung lief. Der VWAP-Abstand zweier Indizes zeigt, welcher relativ zurückhängt.
**Strategie-Familie:** Relative Value.

| Hypothese | Stand |
|---|---|
| AW-12 VWAP minus TWAP als Flow-Vorzeichen | ungebaut |
| **Cross-Market-VWAP-Spread (NQ gegen ES)** | **existiert nicht als Zeile** |

**Hier muss Research neue Edge suchen.** Die TWAP-Seite hat eine eigene Bank-Notiz ([[Hypothesen-Bank (TWAP)]]), die Cross-Market-Variante fehlt komplett. Sie ist die einzige VWAP-Idee, die als **neues Bein statt Ersatz** Sinn ergäbe, weil sie mechanistisch etwas anderes tut als jedes Bestandsbein. Damit auch die einzige mit einem Argument gegen Randbedingung 2. Vorprüfen gegen `rv.py` und die Lehre aus RV_leadlag_NQES (alter Grade-A-Report war nach Engine-Fix PF 0,91).

**Korrektur 10.09.2026 (`research-scout`):** die erste Fassung ordnete den Cross-Market-VWAP-Spread als mögliche Umformulierung des Index-**Dispersions**effekts ein. Das trifft den Mechanismus nicht. Dispersion handelt implizite gegen realisierte Korrelation zwischen Index und Konstituenten, also eine Options- und Volatilitätsstrategie. Die tatsächlich verwandte Literatur ist Index-Futures-**Lead-Lag und Kointegration** (Bangsgaard/Kokholm zu VIX- gegen SPX-Futures). Kein Paper testet einen VWAP-Abstand als Signal, die Abgrenzung, die V9 wirklich braucht, ist die gegen unser eigenes `rv.py`.

**Beleglage nach Recherche: keine, für beide Teilfragen.** Ob VWAP minus TWAP mehr ist als der Preis-Return selbst, klärt keine externe Quelle. Das ist eine Regression, die wir selbst rechnen müssen, und sie ist billig.

### V10 — Overlay und Ausführung
**Mechanismus:** nicht ein neues Signal, sondern eine Änderung an der Ausführung eines bestehenden VWAP-Beins.
**Why-Kern:** unter Gambler's Ruin bei Min-Size ist P(pass) monoton in kappa = mu/sigma². Ein Overlay, das die Tages-Varianz stärker senkt als die Expectancy, hebt die Passquote, obwohl das Bein schlechter aussieht.
**Strategie-Familie:** greift auf Trend Following.

| Hypothese | Stand |
|---|---|
| BE 0,5R + Offset 0,2R auf `NQ_VWAP-Pullback` | **Kandidat mit +2,45 pp, CI [+0,16; +5,14], P(>0) 0,96** |

**Der Job dazu ist kaputt.** `exit2_NQ_VWAP-Pullback_be_offset` (Prio 80, 27 Configs) steht seit 03.09.2026 auf `failed`, abgebrochen nach einer Sekunde: `AttributeError("'list' object has no attribute 'get'")`, Ursache ist `premise: [{}]`. Das ist der einzige VWAP-Punkt mit gemessener Materialität, und er liegt unberührt.

### V11 — Bezug zum Volumenprofil
**Mechanismus:** VWAP gegen POC und Value Area stellen.
**Strategie-Familie:** Intraday Bias.

| Hypothese | Stand |
|---|---|
| Value-Area-Migration (Valentini Baustein 1) | in #134 auf Tages- **und** Candle-Ebene falsifiziert |

**Urteil: geschlossen**, solange kein neuer Mechanismus auftaucht. Hier nicht weitersuchen.

### V12 — Kontrolle
**Mechanismus:** der Pflichttest, ob der VWAP-Anker überhaupt Information trägt.
**Why-Kern:** wenn ein zufällig gesetzter Anker gleicher Historienlänge dasselbe leistet, handeln wir irgendein Level und nennen es nur VWAP.
**Strategie-Familie:** keine, Kontrolle.

| Hypothese | Stand |
|---|---|
| AW-14 echter Anker gegen 200 Zufallsanker | 1 Trial, nie gelaufen |

**Das ist die teuerste offene Stelle des Projekts.** `mb_rand_level` existiert im Modul bereits (`maband.py:279`, `S.random_level_shift`), die Kontrolle ist also billig. Fällt sie durch, sind V1 bis V9 ohne weiteren Sweep erledigt und wir sparen Wochen. Besteht sie, steht jede spätere Zahl auf festerem Grund.

---

## Familien ohne Hypothese: hier wird neue Edge gesucht

| Familie | Was fehlt | Suchauftrag an die Research-Phase |
|---|---|---|
| **V6 Bandbreite** | alles | Gibt es Literatur zur VWAP-Dispersion als Regime-Maß? Abgrenzung gegen gewöhnliche Realized Vola nötig, sonst ist es AR-17 nochmal |
| **V9 Cross-Market-VWAP-Spread** | die Zeile selbst | Gibt es einen belegten Lead-Lag im relativen VWAP-Abstand zwischen Index-Futures? Abgrenzung gegen `rv.py` und gegen den bekannten Dispersions-Effekt |
| V7 Steigung | Modul | Ist die VWAP-Steigung in der Literatur je etwas anderes als ein geglätteter Preis? |
| V5 Anker | drei von vier Ankern | Welcher Anker hat einen **Mechanismus** statt nur Charttechnik? Globex hat den besten Kandidaten (Einstand der Übernacht-Akteure) |
| V8 Exit | Grid | Wird der VWAP in der Execution-Literatur als Kursziel institutioneller Desks belegt? Das wäre ein echter Mechanismus statt Charttechnik |

---

## Phasenplan

### Phase 0 — Blocker räumen
| # | Aufgabe | Ergebnis |
|---|---|---|
| 0.1 | Messen, ob ein `exit_sweep` mit `replaces_leg` den `deploy_ready`-Filter passiert | entscheidet 0.2 |
| 0.2 | Falls nötig: `_null_direction` für `vwap_pullback` auf die Box (Laptop-Patch aus AP137) oder Umzug des Tests auf `maband` | V10 wird promotebar |
| 0.3 | `premise: [{}]` im `exit2`-Job reparieren, neu einreihen mit Prio 80 | 27 Configs laufen endlich |
| 0.4 | Sigma-Warmup in `maband.py:302` messen (`np.std(c - vw)` kumulativ ab Session-Start, am Tagesanfang winzig, außerdem ungewichtet statt volumengewichtet) | sagt, ob die V2-Zahlen überhaupt gültig sind |
| 0.5 | V12 (AW-14) als eigenständigen Job einreihen, Prio hoch | Gültigkeit des ganzen Zweigs |

`engine-regression-tester` vor jedem Box-Sync, sonst blockt der Hook.

### Phase 1 — Research, gebündelt
Ein `research-scout`-Auftrag über alle Familien, Cache-Pflicht zuerst ([[Research-Cache]] und Insight-Bank greppen, dann Web). Schwerpunkt auf den leeren Familien V6 und V9, dazu die Schwellenwert-Frage aus V2 (ab welcher Abweichung greift Continuation) und die Execution-Frage aus V8. Familien ohne belegbaren Mechanismus fallen hier raus und werden nicht gebaut.

### Phase 2 — Hypothesen formen und vorprüfen
`/ein-weg` über die ganze Gruppe: `variant-scout` je Hypothese (mindestens zehn echte Implementierungen, sonst wird nicht gebaut), dann **ein** `strategy-auditor`-Batch-Call über alle Whys zusammen. `variant-scout` bekommt die Kontaminationsliste mit: Fade, Berührungszähler, Multi-Symbol als Frequenzhebel, Trailing und Breakeven-auf-Entry sind verbraucht.

### Phase 3 — Modulbau in `maband`
| Erweiterung | Deckt ab |
|---|---|
| `mb_vwap_dir = "fade" \| "go"` | V2, die größte Lücke |
| `mb_vwap_target = "vwap" \| "band"` | V8 |
| Sigma sauber (Mindest-Bar-Zahl, optional volumengewichtet) | V2, V6 |
| zusätzliche Anker | V5, nur was Phase 1 belegt |

### Phase 4 — Jobs bauen und einreihen
`H()`-Zeilen in `hypothesis_bank.py`, `replaces_leg` gesetzt, Prämisse sauber formatiert, `pipeline-auditor` setzt `pipeline_ok`, dann einreihen und pushen, danach Runner **Stop → Sync → Start**. Prio 80 und höher, damit die Jobs vor den Generator-Varianten laufen.

### Phase 5 — Auswerten
`inbox_tool.py --pull`, nie das volle Log. Kandidat mit belegtem Vorteil: Quant-Team parallel, `strategy-auditor` im Vollmodus, `verdict-auditor` über den Stempel, dann Next-Week-Buch plus Ticket. **Die Übernahme ins Live-Buch bleibt liegen, bis Max aus dem Urlaub zurück ist (ca. 18.09.2026).**

---

## Reihenfolge nach Buch-Chance

| Rang | Punkt | Familie | Aufwand | Chance aufs Buch |
|---|---|---|---|---|
| 1 | BE-Offset-Exit reparieren und rechnen | V10 | sehr klein | **hoch**, +2,45 pp gemessen |
| 2 | Zufallsanker-Kontrolle | V12 | klein | keine direkt, entscheidet über alles andere |
| 3 | Continuation ab Überdehnung | V2 | mittel | mittel bis hoch |
| 4 | Bänder als Ziel und Stop | V8 | mittel | mittel |
| 5 | Leere Bestätigungs-Achsen (RVOL, Delta, Sigma-Stop) | quer | klein | mittel, kein Modul nötig |
| 6 | Bandbreite als Regime | V6 | groß | offen, Research zuerst |
| 7 | Cross-Market-VWAP-Spread | V9 | groß | offen, Research zuerst |
| 8 | Alternative Anker | V5 | groß | niedrig, erst nach V12 |

---

## Ergebnis der Vermessung, 10.09.2026

Sieben Agents parallel: drei `research-scout` über alle zwölf Familien, vier `variant-scout` auf V2, V5, V7 und V8.

### Beleglage je Familie

| Beleglage | Familien | Quelle |
|---|---|---|
| **stark** | V10 | Browne (1995), *Mathematics of Operations Research* 20(4): ψ(w) = exp(−2µw/σ²), optimale Kontrolle läuft über µ/σ². Stützt das kappa-Argument aus #122/#136/#142 extern |
| **mittel** | V8 | Choi/Larsen/Seppi (2021), *Math. and Financial Economics* 15: VWAP-Benchmark-Handel erzeugt formal nachweisbare Preisdruck-Muster. Belegt **nicht** die Magnet-These |
| schwach | V1, V3, V5 | V5 immerhin mit Akteur: Boyarchenko/Larsen/Whelan, NY Fed Staff Report 917, Dealer lagern Inventar-Schocks zum Asien-Open aus |
| **keine** | V2, V4, V6, V7, V9, V12 | für V2 existiert **kein** publizierter Schwellenwert, unsere #097-Zahlen sind die einzige quantifizierte Aussage dazu weltweit |
| geschlossen | V11 | #134, Gegenprüfung ohne Wiedereröffnungsgrund |

Warnung zu V5: ein Fed-Folgepost von Juli 2026 heißt "The Disappearing Overnight Drift". Wir haben mit `NQ_Asia-Dir-USopen_d260820` ein Bein im Buch, das auf genau diesem Effekt sitzt.

### Echte Arten, ehrlich gezählt

Max' Vorgabe waren mindestens 20 Arten je Familie. Das gibt die Sache nicht her, ohne Reparametrisierung als Art zu verkaufen. Die gemessenen Zahlen:

| Familie | Echte Arten | Heute baubar | Anmerkung |
|---|---|---|---|
| V2 | 12, mit ATR-Normierung 24 | **12** (144 Configs) | Schwellenwert k, Stop-Schätzer, Timeframe und Markt zählen nicht als Art |
| V5 | 4 Anker mit Akteur | 3 | kombiniert mit V12 in **einem** Job: 72 Zellen, kein Modulcode |
| V7 | 4 als Signal, 1 als Gate | **0** | alle modulpflichtig, siehe Urteil unten |
| V8 | 30 | **0** | nach kleinem Patch 5, mit Sigma-Fix 15 |

### V7 ist erledigt, und der Nebenbefund ist wertvoller als die Familie

Frisch gemessen auf NQ und ES, 2.731 bzw. 2.716 Sessions. Es gilt exakt `VWAP_i − VWAP_{i−1} = (v_i / W_i) · (tp_i − VWAP_{i−1})`, numerisch verifiziert über 209.721 Bars (corr 1,000). Die VWAP-Steigung ist damit **kein geglätteter Preis**, sondern ein volumenanteils-gewichteter Mittelwert von (Preis minus VWAP), also ein Level-Maß. Das Falsifikationskriterium der Bank-Zeile AW-08 lief gegen die falsche Referenz.

- Vorzeichen-Deckung mit `z = (c − VWAP)/sd`: **91 % bei 30 Minuten**. Die Steigung ist ein verrauschtes `mb_vwap_evt="side"`.
- Volumengewichtung ändert das Vorzeichen in **3 bis 4 %** der Bars und kauft nichts (+0,479 gegen +0,421 Punkte, SE 0,088). Grund: die Intraday-Volumensaisonalität ist eine deterministische U-Form, `w_j` ist praktisch eine Funktion der Tageszeit.
- `W_i` wächst monoton, die Steigung zerfällt mechanisch mit 1/t. Eine feste `mb_thr` darauf ist zu großen Teilen ein **Tageszeit-Filter**.
- Bester Rohwert +0,48 Punkte gegen eine Kostenschwelle von rund 0,87 Punkten auf NQ.

**Urteil: AW-08 nicht bauen.** Korrektur `verdict-auditor` 11.09.2026: Stempel lautet **„geprüft, redundant“**, nicht „nicht baubar“. Der Gate-Arm ist nicht ungetestet, sondern 23.041-mal unter anderem Namen gemessen: `tm_vwap_side` (Close gegen Session-VWAP, exakt die Größe der Identität) steht in 46.349 Trials des Registers, Survivor-Quote an 3,75 % gegen aus 3,88 %. Damit ist auch „`tm_vwap_side` 0-mal gesetzt“ nur für die 146 `mb_kind="vwap"`-Trials richtig, global ist es die meistgetestete Achse überhaupt und keine unbelastete Reserve. Der Nebenbefund unten ist mit t 1,93 (60 min) und t 0,83 (120 min) **schwach**, NQ und ES zählen als ein korrelierter Beleg (#051); AW-15 steht deshalb auf #097 (elf Jahre, monoton), nicht auf dieser Zahl.

**Der Nebenbefund, unabhängige Stütze für V2:** `E[sign(z) · fwd]` auf NQ ist **+0,876 Punkte (t 1,93) bei 60 Minuten** und **+1,008 (t 0,83) bei 120 Minuten**, Vorzeichen positiv, also **Continuation**. In beiden Märkten, über 2.700 Sessions, driftbereinigt stabil. `maband.py:307` verdrahtet exakt das Gegenteil. Das erklärt die fünf negativen `dist`-Trials und stützt den Continuation-Arm mit frischen Zahlen statt nur mit Literatur.

**Zweiter Nebenbefund:** wer "Steigung" als Mechanismus will, hat den Ast schon offen. `mb_kind="slope"` (AC-06) hat bei nur 71 Trials **3 Survivors**, bester Fund `hyp_AC06_NQ` (ema50, `mb_thr=0.1`, `mb_confirm=2`): OOS PF 1,50, 104 OOS-Trades, 42 Trades pro Jahr, `fails: []`. Dort fehlt das Grid, nicht das Modul.

### Pipeline-Befunde, die über den VWAP hinausgehen

Sechs strukturelle Funde, alle register- oder codeverifiziert. Gehören an `pipeline-auditor` und `logbook-distiller`:

1. **Der Prämissen-Friedhof ist ein Bug, kein Ergebnis.** Stufe 0 rechnet ausschließlich die Base-Config. Bei AW-02 und AW-14 steht im Base `mb_vwap_evt="pullback"` ohne Anker-Override, der Anker liegt nur im Grid. Beide Jobs haben also den Session-Pullback gemessen, also die per #097 belegte schlechtere Seite, und sind daran gestorben. **Die Ankerachse wurde nie erreicht.** In der Queue stehen insgesamt 303 `premise_failed`.
2. **Für eine Kontrolle ist das Edge-Gate in Stufe 0 konzeptionell falsch.** AW-14 soll prüfen, ob der echte Anker den Zufallsanker schlägt. Eine Kontrolle darf keine Edge haben müssen, um gerechnet zu werden. So gebaut kann der Job nie laufen.
3. **`mb_vwap_anchor` wird nicht validiert.** Jeder unbekannte String fällt still auf `a0=0` zurück, also auf den Session-Anker. Ein Grid mit `["session","globex","fomc"]` würde vor der Modul-Änderung dreimal denselben VWAP rechnen und drei Registry-Einträge schreiben. Braucht eine Whitelist.
4. **Phantom-Achsen im VWAP-Zweig** (siehe oben): acht `mb_*`-Parameter ohne Wirkung erzeugen bitgleiche Trades unter verschiedenen Hashes.
5. **AW-05 ist falsch etikettiert** und misst das feste R-Vielfache, gegen das sie antreten soll.
6. **`tm_delta_src="real"` ist in `maband` unbenutzbar**, weil `delta_1m` nie geladen und an `gates_pass` durchgereicht wird (Gegenbeispiel `tsmom.py:240/344`). Immerhin wirft es einen ValueError statt still falsch zu rechnen.

### Korrigierte Reihenfolge nach Buch-Chance

| Rang | Punkt | Warum | Modulcode |
|---|---|---|---|
| 1 | `exit2`-Job reparieren (V10) | +2,45 pp gemessen, CI schließt Null aus, jetzt zusätzlich extern belegt (Browne 1995), liegt seit 03.09. kaputt | nein |
| 2 | V5 plus V12 in einem Job, 72 Zellen | beantwortet die Anker-Gültigkeit für den ganzen Zweig. Fällt die Kontrolle, sind V1 bis V9 ohne weiteren Sweep erledigt | nein |
| 3 | V2 Continuation, 144 Configs | `mb_side="against"`, frische Messung stützt die Richtung, Achse unbelastet | nein, besser mit ATR-Normierung |
| 4 | AC-06 Slope-Ast ausbauen | 3 Survivors bei 71 Trials, OOS PF 1,50, `fails: []`. Grid fehlt, Modul steht | nein |
| 5 | V8 nach maband-Patch | Level-Export plus `tm_exit="level"`, deckt zugleich AB-08 und die Sigma-Hygiene ab | ja |
| — | V7 | nicht bauen, siehe oben | — |
| — | V1, V3, V4, V6, V9 | keine Beleglage und breit gemessen. Kein Bau ohne neuen Mechanismus | — |

---

## Stand 11.09.2026 — gebaut und eingereiht

Max: „schau was wir da gemacht haben, und fang an alles zu testen, oder was wir nicht gleich testen als Ticket aufzumachen." Session lief auf der Box. Die Box stand seit 16:20 leer (Generator am Tageslimit 120, 0 pending), die vier Jobs aus der korrigierten Reihenfolge sind gebaut, dazu ein fünfter (AC-06c). Alle vier Hypothesen-Jobs wurden 17:57 eingereiht, der Runner (neu gestartet mit Kontroll-Prämissen-Patch, PID 7780) rechnet seit 17:57:55 AW-14b.

**Smoke-Test vorab** (15 Configs, Scratchpad, je 13-26 s): jede geplante Grid-Achse ändert die Trades (RVOL, Delta, EMA20, Range-Stop, Time-/RR-Exit, Anker hi, Zufallslevel). `tm_vwap_side` und `mb_thr` sind im VWAP-Zweig **bitgleich** zur Basis (Phantom bestätigt) und fliegen aus jedem Grid. Erste Zahlen: Continuation k=1,5 expR +0,007 (n 2.690), k=2,0 −0,001, Fade k=2,0 −0,014; Zufallslevel −0,008 gegen echten VWAP −0,001; AC-06-Randzelle (thr 0,05, confirm 1, ema80) expR +0,038; BE-Offset reproduziert die 1.408 Trades aus #142.

| Rang | Job | Stand | Configs | Prio |
|---|---|---|---|---|
| 1 | `exit2_NQ_VWAP-Pullback_be_offset` (V10) | **repariert und fertig (17:55): 0 Kandidaten.** 11/27 Survivors, alle Buch-Marginals absolut „schlechter“ (−2,8 bis −4,8 pp gegen Buch ohne Bein), Original-Bein −4,7 pp, bestes „vs Original“ +1,9 pp (be0,5/o0,2 + Trail). Der #142-Kandidat verbessert das Bein, nicht das Buch. Review-Frage: bleibt `NQ_VWAP-Pullback` im Buch? Prämisse war Liste statt Dict, dazu `gates`/`controls` ergänzt. Bleibt auf `mode="vwap_pullback"`: kein Null-Schalter auf der Box, Kandidaten landen als „blocked: uebersprungen:null", **nie deploy_ready**, keine Auto-Promotion. Bewertung von Hand in der Wochenend-Review, Null-Schalter = AP137/AP150 (5) | 27 | 80 |
| 2 | `hyp_AW14b_NQ` (V12+V5) | eingereiht. Kontrolle echter Anker gegen `mb_rand_level`, session/hi/lo × with/against × k × Stop. Neuer H()-Parameter `prem_min_edge_pp` (nur `book=False`) plus Runner-Patch (`discovery_runner.py`: `ins.expR > 0` und der Dollar-Check gelten nicht für Kontroll-Jobs mit `premise.min_edge_pp`), sonst wäre der Job mit IS expR −0,030 exakt wie AW-14 gestorben (`pipeline-auditor`). **Grenze der Aussage:** `random_level_shift` würfelt beim dist-Ereignis Richtung und Distanz mit, der Zufallsarm ist damit eine Tages-Zufallsrichtung auf anderer Trigger-Menge, kein „anderer Anker gleicher Distanz“. Das Ergebnis darf **nicht** als „V1 bis V9 erledigt“ gelesen werden; der saubere Anker-Placebo (VWAP ab zufälligem Start-Bar, `mb_vwap_anchor="rand_time"`) ist AP150 Punkt 6 | 72 | 96 |
| 3 | `hyp_AW15_NQ` (V2) | eingereiht. Continuation via `mb_side="against"`, Sigma-normiert, Ersatz für `NQ_VWAP-Pullback`, Prämisse auf drei Grid-Zellen statt der Basis (Befund 1) | 144 | 90 |
| 5 | `hyp_AC06c_NQ` | eingereiht, aus dem `verdict-auditor`-Gegenlesen von AW-05: „Zieldistanz fest gegen atmend“ auf dem AC-06-Survivor, Stops `points`/`atr`/`sigma` am NQ-Median kalibriert (ATR20 204 Pkt, Sigma 6,2 Pkt). Auswertung nur je Epoche (Vola-Drift 52 → 436 Pkt), AC-06b und AC-06c sind eine Auswahl für denselben Slot | 36 | 82 |
| 4 | `hyp_AC06b_NQ` | eingereiht. Grid um die drei AC-06-Survivors (Rand nach unten und außen). **Annahme:** Ersatz-Test gegen `NQ_Momentum_d260818` (Familien-Ersatz ist laut AP137 Max' Entscheidung; Stufe 1 und Register sind davon unabhängig) | 108 | 85 |

**Zurückgestellt und als Ticket:** AW-05 steht in der Bank auf `hold` (misst nicht, was der Titel sagt). **AP150** = maband-Erweiterungen (ATR-Normierung, Level-Export + `tm_exit="level"` für V8, Sigma-Hygiene, Globex-Anker, Null-Schalter-Deploy), erst nach dem AW-14b-Ergebnis. **AP151** = die sechs Pipeline-Befunde plus Hook-Fehlalarme. V6/V9 bleiben ohne Bau, solange kein Mechanismus da ist.

**Auswertung:** `inbox_tool.py --pull` (bzw. auf der Box direkt `inbox_tool.py`), AW-14b von Hand aus `results/hyp_AW14b_NQ.json` (expR echt minus Zufall je Zelle, nie die Datei komplett lesen, gezielt per Python filtern). Übernahme ins Live-Buch erst nach Max' Rückkehr.

## Verwandte Notizen
[[Alpha-Suche]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (TWAP)]] · [[Discovery-Runner v2]] · [[Strategie-Familien]] · [[Day Trading]] · [[Research-Cache]]
