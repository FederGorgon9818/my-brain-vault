---
tags: [projekt, trading, alpha-suche, fibonacci]
erstellt: 2026-09-11
aktualisiert: 2026-09-11
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Fibonacci-Kapitel sauber schließen
---

# Fibonacci Wege-Karte

**Ziel (einziges Kriterium):** die v2-Passquote je Eval des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 11.09.2026 vom `familien-scout` (Abnahmetest 2 des Workflows `konzept-weg`, Auftrag Max). Vorlauf: Inventar über Register (60.019 Trials), Queue, [[Strategie-Logbuch]], [[Hypothesen-Bank (Momentum & Averages)]], [[Research-Cache]] und `ideas.json`. Vorbild für den Aufbau: [[VWAP-Offensive]] (Hand-Karte zu einem anderen Konzept, hier nicht angefasst).

> [!warning] Die Lage ist unbequem, und das ist der Wert dieser Karte
> Der Diskriminanztest, den wir selbst fahren würden, ist **bereits publiziert und negativ**: Bounce-Wahrscheinlichkeit an Fibonacci-Zonen ist von Zufallszonen statistisch nicht unterscheidbar (Tsinaslanidis/Guijarro/Voukelatos, ESWA 187, 115893, 2022). Von 26 Wegen tragen deshalb **drei** ein Skelett. Wer hier zwanzig Hypothesen produziert, hebt nur die Zufallsdecke für alle anderen.

---

## Die vier harten Randbedingungen

**1. Alles Neue muss in `maband`/`tsmom`.** Nur diese beiden Module haben einen Null-Schalter (`controls.py` `ctl_null`), alles andere kann nie `deploy_ready` werden und wird von `promote_next.py` weggeworfen. Kein neuer `mode`, nur Erweiterung der bestehenden Module.

**2. Ersatz schlägt Neuzugang** (#139 B3: der Weg „neues Bein" hat noch nie einen Kandidaten geliefert). Rang 1 und 2 sind Ersatz-Slots, Rang 3 ist genau deshalb Rang 3.

**3. Kein Fibonacci-Weg ist sofort engine-fähig.** Weder `maband` (`cross · dist · slope · fan · speeds · price_ma · band · channel · vwap`) noch `tsmom` kennen ein Leg mit Fraktionen. Nächster Verwandter ist der Donchian-Kanal — er liefert das 0 %- und das 100 %-Level eines n-Bar-Legs, sonst nichts.

**4. „Das Level trägt Bedeutung" ist vierfach widerlegt.** ESWA 2022 (Placebo gegen Zufallszonen) · Logbuch [[Strategie-Logbuch#149]] (Rundzahl-Bounce hält **schwächer** als das phasenverschobene Placebo, ~530k Events) · [[Strategie-Logbuch#138]] (am OR30-Level Verhalten am Zufallslevel identisch, 0/11 Jahre) · eigene Register-Zahl AB-12 (Bollinger-Break gegen Zufallslevel gleicher Distanz: expR +0,007 vs. +0,007). Dazu der Friedhof: **Pivot Points getötet** (`ideas.json` #39). Jeder Weg, der auf Reflexivität am Level baut, braucht einen **neuen** Grund oder bekommt kein Skelett.

---

## Register-Stand (11.09.2026)

| Griff | Zahl |
|---|---|
| `n_total` im Register | **60.019 Trials** |
| davon mit Fibonacci-/Retracement-Level | **0** |
| `mb_kind="channel"` (nächster Verwandter) | 3.285, **0 Kandidaten**, verteilt auf 10 Generator-Jobs |
| davon mit `mb_rand_level` gesetzt (die Kontrolle) | 28 (12-mal auf `True`) |
| Band-Logik | 12.962 · `maband` gesamt 12.854 · `vwap` 48.172 |
| `tm_stop_mode` | `range` 37.922 · `atr` 13.437 · `sigma` 63 · **`points` 0** (aus der AC-06c-Notiz) |
| AB-12 Kontrolllauf `hyp_AB12_NQ` | 25 Configs, **0 Survivors**, PBO 41 % im Zufallsband |
| Queue | seit 11.09. 16:20 **leer** (`queue_empty`) |

**Ein leg-relativer Stop existiert im ganzen Register nicht.** Das ist die einzige wirklich leere Achse, die dieses Konzept anzubieten hat, und sie trägt Rang 1.

---

## Die 26 Wege

Aufgebaut aus Elementen → Beziehungen → Richtung. Elemente: Impuls-Leg (Anker A = Start, B = Ende) · Retracement-Levels 0,236/0,382/0,5/0,618/0,786 · Golden-Pocket-Zone · Extensions 1,272/1,618 · Konfluenz · Zustände (Leg-Größe, Zonenbreite, Berührungszähler) · dazu immer der Preis.

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg |
|---|---|---|---|---|---|
| W1 | **hin zu** Retracement-Level (Ziel) | Mean Reversion | Level/Exit | offen, **entblockt 14.09.** (AC-06c hat nur den Konstant-Arm entschieden), wartet auf `leg`-Arm | Spec A |
| W2 | **abprallen** am Level, long | Trend Following | Signal | Research widerlegt (ESWA 2022) + #149/#138 | Spec A |
| W3 | **abprallen** am Level, short | Trend Following | Signal | wie W2 | Spec A |
| W4 | **hindurch**, Retracement vertieft sich | Mean Reversion | Signal | offen, kontaminiert (κ-Deckel #138) | Spec A |
| W5 | **entlanglaufen** am Level | Trend Following | Filter | offen, keine Story | Spec A |
| W6 | **kreuzen und halten** (Reclaim) | Trend Following | Signal | offen, Reparametrisierung von `vwap reclaim`/`channel` | Spec A |
| W7 | **kreuzen und scheitern** (Fakeout) | Mean Reversion | Signal | offen, Gegenwind aus #149 | Spec A |
| W8 | **weg von** — Retracement-Tiefe kontinuierlich | Trend Following | Filter | ❌ **tot ([[Strategie-Logbuch#149]])**, Barrieren-Artefakt | `pullback_depth_precursor.py` |
| W9 | in die **Golden-Pocket-Zone** und drehen | Trend Following | Signal | Research widerlegt (Zonenbreite trivial) | Spec A |
| W10 | **durch die Zone hindurch** | Mean Reversion | Signal | offen, keine eigene Story (= W4 breiter) | Spec A |
| W11 | **hin zu B** (altes Extrem als Ziel) | Trend Following | Exit/Level | offen, **entblockt 14.09.**, wartet auf `leg`-Arm (AP157) | Spec A |
| W12 | **durch B hindurch** (Swing-Bruch) | Trend Following | Signal | 🟡 **gemessen ohne Kandidat (3.285 Trials)** | `mb_kind=channel` ✅ |
| W13 | **abprallen an B** (Doppel-Extrem) | Mean Reversion | Signal | offen, = lebende ORB-Fade-Familie (#068) | `channel, mb_side=against` ✅ |
| W14 | **durch A hindurch** (100 % retraced) | Trend Following | Exit/Stop | ⏳ **gebaut + eingereiht als AC-06d (17.09.)** | Spec B ✅ (`tm_stop_mode="leg"`) |
| W15 | **abprallen an A** | Mean Reversion | Signal | offen, Kontamination wie W2 | Spec A |
| W16 | **hin zur Extension** 1,272/1,618 | Trend Following | Exit | offen, **entblockt 14.09.**, wartet auf `leg`-Arm (AP157) | Spec A |
| W17 | **abprallen an der Extension** | Mean Reversion | Signal | offen, Verwandter negativ (AW-09, PF 0,77-0,91) | Spec A |
| W18 | **durch die Extension hindurch** | Trend Following | Signal | offen, keine Story über W12 hinaus | Spec A |
| W19 | **Level ↔ Level:** Konfluenz zweier Legs | Trend Following | Filter | offen, keine Story | Spec A |
| W20 | **Level ↔ Level:** Fib-Level ≈ Rundzahl | Trend Following | Filter/Kontrolle | Bounce-Arm erledigt (#149), Rest = **Mitnahme-Spalte** | `nearest_round_levels` ✅ |
| W21 | **Zustand:** Leg-Größe in σ | Trend Following | Filter | offen, Literatur zeigt Gegenrichtung | `tm_sigma_q_min/max` ✅ |
| W22 | **Zustand:** Zonenbreite | Trend Following | Filter | Research widerlegt (trivial) | Spec A |
| W23 | **Zustand:** Berührungszähler k | Trend Following | Filter | ❌ **tot ([[Strategie-Logbuch#138]], AB-14)** | `prebreak_precursors.py` |
| W24 | **Anker:** Fraktionen des Overnight-Legs | Intraday Bias | Level/Signal | 🟢 **offen → Skelett FIB-W24a** | Spec A |
| W25 | **Anker:** Mehrtages-Leg **(Swing)** | Swing | Signal | offen, **Live-Buch-Merker, nicht Prop-Buch** | Spec A (Tagesbars) |
| W26 | Level als **Stop-Ort** statt ATR-Stop | Trend Following | Exit | offen, in FIB-W14a mitgeführt | Spec B |

**Zur Vollständigkeit:** zusammengelegt wurde nur, wo zwei Zellen bitgleiche Trades erzeugt hätten (z.B. „durch die Zone" = „durch das Level" mit breiterer Toleranz). Long/Short getrennt geführt nur bei W2/W3, weil dort die Story verschieden ist; sonst ist die Richtung eine `mb_side`/`tm_dir`-Achse und wäre als eigener Weg eine unehrliche Verlängerung der Liste.

---

## Je Weg: was zu sagen ist

### W14/W26 — Leg-Invalidierung als Stop-Geometrie 🟢 Rang 1
Die **einzige Story im ganzen Konzept, die den Placebo-Einwand überlebt**, weil sie ohne Reflexivität auskommt: es muss niemand am Level reagieren. Behauptet wird nur, dass die These des Trades faktisch falsch ist, sobald der Preis den Leg-Start wieder erreicht. Ein ATR-Stop sitzt zufällig mal innerhalb, mal außerhalb des Legs, stößt mitten in der eigenen These aus, und derselbe Trader steigt danach in dieselbe Bewegung wieder ein — der MNQ-Round-Trip von rund 2 Punkten wird doppelt gezahlt. Register: `tm_stop_mode=points` 0 Trials, leg-relativ gar nicht vorhanden. Träger ist der AC-06-Survivor-Entry (OOS PF 1,50, `fails []`), weil eine Exit-These auf einem Entry ohne Edge nicht messbar ist. **Ersatz `NQ_Momentum_d260818`. Keine toten Verwandten.**

### W24 — Overnight-Leg-Fraktionen 🟢 Rang 2
Das Globex-Leg ist das einzige Leg des Tages ohne Fensterwahl und ohne Zeitrahmen-Freiheitsgrad — jeder sieht es vor dem RTH-Open identisch. Das Buch handelt bereits seine **Extreme** ([[Strategie-Familien|Intraday Bias]]-Bein `NQ_Asia-Dir-USopen_d260820`), die **Fläche dazwischen** hat nie jemand gemessen: 0 Register-Trials. Getestet wird nicht „0,618 ist besonders", sondern ob **irgendeine** Fraktion Information trägt — mit Zufallslevel-Kontrolle UND Ratio-Placebo im selben Job. Fällt sie, ist die Familie in einem Lauf sauber erledigt statt per Analogie. **Ersatz `NQ_Asia-Dir-USopen_d260820`.** Kontaminationswarnung: `ideas.json` #21 (Asian-Levels-Breakout, nach Fill-Fix OOS +1,2 %, PF 1,07, Auto-Fit lehnte ab) ist derselbe Datensatz, aber der Extrem-Arm — Korrelation zum Bestandsbuch nach #079 ist der erste Filter.

### W12 — Swing-Bruch mit Rundzahl-Konfluenz 🟡 Rang 3
Der Durchbruch-Arm ist die einzige Level-Seite, die in **unseren eigenen** Daten real vom Placebo abweicht (#149: ES +4,4 bis +6,8 pp über alle drei Rundungsgrade, 5 Phasen-Offsets, gematchte Bruchraten). Die Bank führt das seit 10.09. als **Messfund mit Mitnahme-Regel** — bisher nur Text, nirgends Code. Neuer Winkel gegenüber den 3.285 gemessenen Donchian-Trials: Konfluenz Swing-Extrem × Rundzahl als Zusatzbedingung. Ökonomisch steht #138s κ-Deckel weiter, deshalb Prescan vor Grid (κ nach #138-Konvention, Payoff ab X Minuten **nach** der Bruch-Bar, nicht die Bruch-Bar selbst).

### W1/W11/W16 — Level als Ziel: entblockt, aber noch nicht gemessen (Stand 14.09.2026)
`AC-06c` hat die Vorfrage „feste gegen atmende Zieldistanz" beantwortet: der **konstante** Punkte-Arm verliert in allen vier breitenkalibrierten Paarungen (Richtung eindeutig, Signifikanz grenzwertig, Stempel `verdict-auditor` 14.09.). Das entscheidet aber nur über den Konstant-Arm. Ein Fib-Ziel (0,618 / 1,272 des Legs) ist **struktur-skaliert**, atmet also ebenfalls, nur an einer anderen Variable als ATR/Sigma; AC-06c unterscheidet nicht zwischen Dispersions- und Struktur-Skalierung. Die drei Wege sind deshalb **offen, nicht gefallen**, und hängen jetzt am fehlenden dritten Arm `tm_stop_mode="leg"` (Spec B, Register 0 Trials, AP157 Punkt 4). Auflagen aus der Quant-Rechnung für diesen Arm: Kalibrierung auf Median **und** Mittel der realisierten Weite, Kontrollarm `points` auf der realisierten Median-Weite des Leg-Arms, Urteil über $/Trade und θ = 2μ/σ² mit gepaartem Block-Bootstrap (nicht PF), Power: 408 NQ-Trades reichen für ±8 $ nicht, also NQ+ES+YM+RTY (~1600 gepaarte Trades).

### W2/W3/W9/W15/W19/W22 — „Das Level trägt Bedeutung"
Keine Story mehr, vier unabhängige Belege (siehe Randbedingung 4). Kein Skelett. Kein Aufwärmen ohne neuen Grund.

### W8 und W23 — tot, nachgelesen
W8: [[Strategie-Logbuch#149]], 477k Events, 4 Märkte, Band-These tot, Dezil-Monotonie als Barrieren-Diskretisierungs-Bias entlarvt (Lehre 148, Richtungs-Placebo reproduziert sie unverändert).
W23: [[Strategie-Logbuch#138]], k1-k4 = 0,365/0,376/0,358/0,317, Zufallslevel identisch, 0/11 Jahre.
Beide bleiben stehen, damit sie niemand neu entdeckt.

### W25 — Mehrtages-Leg **(Swing)**
`swing: true`. Im Prop-Käfig (2.000 $ Budget, Intraday-Bust #077) nicht handelbar → **kein Job-Vorschlag, Live-Buch-Merker**. Steht hier, damit Max' Regel „nichts, was je eine Edge zeigte, geht verloren" greift.

---

## Reihenfolge nach Buch-Chance

1. **FIB-W14a** — Ersatz `NQ_Momentum_d260818`, kleinste Modul-Spec (~30 Zeilen), keine toten Verwandten, Why ohne Reflexivität.
2. **FIB-W24a** — Ersatz `NQ_Asia-Dir-USopen_d260820`, mittlere Spec (~90 Zeilen), Kontamination mit dem Asia-Bein zu prüfen.
3. **FIB-W12b** — neues Bein auf ES, kleines Gate (~15 Zeilen), stützt sich auf einen Messfund mit ökonomischem Deckel.

**Baureihenfolge:** Spec B zuerst (braucht von Spec A nur die Leg-Erkennung, nicht die Level-Logik). Wer Spec A komplett baut, bevor gemessen wurde, verbrennt Zeit vor der ersten Zahl.

---

## Modul-Specs

| Spec | Wo | Umfang | Inhalt |
|---|---|---|---|
| **A** | `maband.py`, `_event()` | ~70-90 Zeilen + 8 `DEFAULTS` | `mb_kind="retr"`: `mb_retr_win` (Bars, `"session"`, `"overnight"`), `mb_retr_ratio`, `mb_retr_evt` (`touch·bounce·break·reclaim·fail`), `mb_retr_tol`. Anker analog `maband.py:290-295`, Level-Vergleich analog `271-285`, alles aus Bars vor i. **Ratio-Placebo ist Pflicht**, sonst misst der Job Distanz statt Bedeutung (AB-12) |
| **B** | `sigcore.py`, Stop-Schätzer | ~20-30 Zeilen | `tm_stop_mode="leg"`: Stop am Leg-Start, `tm_stop_mult` als Faktor auf die Leg-Höhe. Einheiten-Falle nach AC-06c: Arme auf gleiches mittleres R kalibrieren, sonst misst der Job Größe statt Verankerung |
| **C** | `maband.py`, `channel`-Zweig | ~15 Zeilen | `mb_round_conf` (Ticks): nutzt `S.nearest_round_levels` (`sigcore.py:326`), Placebo `S.random_grid_phase` (`:310`) — beide existieren seit #149 |

---

## Offene Research-Fragen

1. Belege jenseits von Praktikerprosa, dass ein an der **Struktur** verankerter Stop bei gleicher mittlerer Stopweite besser abschneidet als ein volatilitätsskalierter? (Optimal Stopping / Barrieren, nicht TA-Blogs.)
2. Literatur zu **Fraktionen** der Overnight-/Globex-Range (nicht nur Extreme) als Intraday-Referenz in Index-Futures? Und: schon durch die Overnight-Return-Literatur erklärt?
3. Evidenz, dass **Konfluenz zweier Level-Arten** (Swing-Extrem × Rundzahl) die Bruch-Kaskade über die Einzeleffekte hinaus verstärkt — oder ist Konfluenz nur eine Stichproben-Verkleinerung?

---

## Stand je Weg (hier stempelt der `verdict-auditor` zurück)

| Datum | Weg | Stempel | Quelle |
|---|---|---|---|
| 11.09.2026 | W8 | tot | Logbuch #149 |
| 11.09.2026 | W23 | tot | Logbuch #138 |
| 11.09.2026 | W12 | gemessen ohne Kandidat (3.285 Trials) | Register |
| 11.09.2026 | W2/W3/W9/W15/W19/W22 | Research widerlegt (ESWA 2022) — **kein Tot-Stempel** | Research-Cache |
| 14.09.2026 | W1/W11/W16 | entblockt: Konstant-Ziel verliert (AC-06c), Struktur-Ziel ungemessen, wartet auf `leg`-Arm | `verdict-auditor`, Logbuch #153 |
| 14.09.2026 | W14/W26 | Auflagen für FIB-W14a präzisiert (Median+Mittel-Kalibrierung, Kontrollarm auf realisierter Weite, $/Trade + θ statt PF, Multi-Markt für Power) | `quant-mathematician` |
| 17.09.2026 | W14/W26 | Spec B gebaut (`maband._leg_stop`, Anker pivot/session/roll/slope_turn), als AC-06d auf NQ/ES/YM/RTY eingereiht; slope_turn und roll vorab raus (Duplikat session bzw. `range`), mult 0,786 raus. Kein Stempel, Erwartung „nicht entschieden“. W1/W11/W16 hängen weiter an diesem Ergebnis | `variant-scout`, Quant-Team, `strategy-auditor`, `pipeline-auditor` |

---

## Verwandte Notizen

[[VWAP-Offensive]] · [[Familien-Scout Agent]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Research-Cache]] · [[Alpha-Suche]] · [[Discovery-Runner v2]] · [[Strategie-Familien]] · [[Simplex beats Komplex]]
