---
tags: [projekt, trading, alpha-suche, gap, overnight]
erstellt: 2026-09-22
aktualisiert: 2026-09-22
status: aktiv
ziel: v2-Passquote je Eval verbessern, oder das Gap-Kapitel sauber schließen
---

# Gap Wege-Karte

**Ziel (einziges Kriterium):** die **v2-Passquote je Eval** des aktuellen Buchs verbessern. Nicht Einzel-Edge, nicht Sharpe, nicht Vollständigkeit der Taxonomie. Jede Zeile muss am Ende beantworten: **Ersatz für welches Bein, oder neues Bein, und wie viel pp bringt es?**

Angelegt am 22.09.2026 vom `familien-scout`. Quelle des Konzepts: Max, 22.09.2026 — Vendor-Seite `oxfordstrat.com/trading-strategies/gap-pattern`, "Gap bei uns testen und optimieren". Die Spezifikation der Seite holt `research-scout` parallel; diese Karte steht **komplett auf unserem Bestand** (Register, Logbuch, Banken, Engine). Aufbau nach dem Vorbild [[VWAP-Offensive]] (Hand-Karte, anderes Konzept, hier nicht angefasst).

> [!note] Abgrenzung zu den beiden Schwesterkarten — vor jedem Skelett dort gegenlesen
> [[Overnight-Bias ORB Wege-Karte]] deckt **W21 (Gap-Fill), W22 (Gap-Continuation), W23 (Gapgröße als Tor) und W44 (Globex-Reopen-Lücke)** bereits ab — dort ist der Gap ein *Zustand der Nacht*, der auf einen Opening-Range-Ausbruch wirkt. [[Session Momentum Wege-Karte]] deckt mit **W6 / SES-W6a** den Tug-of-War ab, und dort steht die Auflage, die auch hier gilt: `tm_base="overnight"` ist **bitgleich** mit der Gap-Formel, das Skelett muss als **Reparatur der Bank-Zeile TN-03** laufen, nicht als neue ID.
>
> Was diese Karte NEU hat: den Gap als **eigenes Objekt mit eigener Geometrie** — die Fill-Linie als Ziel *und* als Einstiegs-Ereignis, die Vortages-Range statt des Vortages-Close als Bezug, die Gap-Historie über mehrere Tage, und die beiden Wartungsfälle, bei denen ein Gap-Urteil auf überholtem Grund steht.

---

## Die Lage in einem Satz

Der Gap ist bei uns **das am dichtesten gemessene und am schlechtesten aufgelöste Konzept**: 397 Trials im `gap`-Modus plus 145 im `tsmom`-Overnight-Pfad, 143 Survivors, **0 Kandidaten** — und trotzdem sind Long und Short nie getrennt, der Vortages-Bereich nie einbezogen, der Fill nie als Einstieg genutzt und der Einstiegszeitpunkt nie variiert worden. Zwei der drei Gap-Urteile im Haus stehen zusätzlich auf einem Stand, den es so nicht mehr gibt.

---

## Die acht harten Randbedingungen

**1. `mode="gap"` kann heute nicht `deploy_ready` werden.** `controls.ctl_null` (Z. 688-690) kennt nur `tsmom`, `maband`, `ts_reversal`, `last_hour`, `asian`, `vwap_pullback`; `ctl_delay` hat ebenfalls keinen `gap`-Zweig. Das ist das Modus-Loch aus [[Strategie-Logbuch]] #139 (B1), und es betrifft den ganzen klassischen Gap-Pfad. Wer im `gap`-Modus bleibt, braucht zuerst Modul-Spec S-GAP-1 (15-20 Zeilen).

**2. Es gibt einen zweiten, vollwertigen Gap-Pfad — und der ist deploy-fähig.** `tsmom` mit `tm_base="overnight"` liest `on_ret`, und `on_ret` ist **bitgleich** mit `gap` (`sigcore.py` Z. 702 gegen Z. 716). `tm_side="fade"` ist der Gap-Fade, `tm_side="momentum"` die Continuation — mit Nullkontrolle, Delay-Selbsttest, Bestätigungsachse (`AX_CONFIRM`), Exit-Profilen, Richtungstrennung (`tm_dir`), Wochentag (`tm_dow`) und Größenband (`tm_on_ret_min/max`). Preis dafür: kein ATR-normiertes Band (nur Prozent), keine inhaltliche Bestätigung "erste Kerze dreht Richtung Fill", kein `prev_close` als Ziel. **Ein Gap-Bein fürs Buch wird auf diesem Pfad gebaut, nicht im `gap`-Modus.**

**3. Die Engine kennt vom Vortag nur den Schluss, nicht die Spanne.** `sigcore.daily_context` liefert `prev_close`, `gap`, `on_ret`, `prev_rth`, `on_pos`, `on_range` — aber **kein `prev_high`/`prev_low`**. "Echter Gap über das Vortages-Hoch" gegen "Gap innerhalb der Vortages-Range" ist damit in **0 von 397** Trials unterschieden. Das ist die größte inhaltliche Lücke des Konzepts.

**4. Die Engine kennt kein Gestern-Gap.** Kein `prev_gap`, keine Serie, kein "ungefülltes Gap vom Vortag". Der ganze Mehrtages-Ast — also ausgerechnet das Wort **"Pattern"** von der Vendor-Seite — hat 0 Trials und keinen Pfad.

**5. Der Fill ist im Code ausschließlich ein Exit.** `qbt._gap_trades` setzt bei `fade` `target = prev_close` und beendet dort. Es gibt keinen Zweig, der die **Berührung** von `prev_close` als Einstiegs-Ereignis nutzt. Fill-and-Go, Overfill und Fade-des-Fades sind damit strukturell unmessbar — nicht "getestet und schlecht".

**6. Es gibt keine Richtungsachse im Gap-Modus.** `_gap_trades` leitet `tdir` aus dem Gap-Vorzeichen ab, ein `gap_dir`-Parameter existiert nicht. Long und Short sind auf diesem Pfad in allen 397 Trials **vermischt** — der Long-Bias aus #108 ist hier schlicht ungeprüft.

**7. Die externe Beweislage steht gegen den Fade und ist beim Continuation nur unterpowert.** [[Research-Cache]] Z. 1314, Mesfin (arXiv 2605.04004) Tabelle 5 auf MNQ: Gap-Fill-Fade N 238-245/Jahr, netto −1,92 / −1,31 / −2,24 Punkte, T −0,44 / −0,32 / −0,59, alle FAIL, Wortlaut *"MNQ gaps do not consistently fill within RTH"*. Gap-Continuation-Short N=22, **+14,52 Punkte, T=+3,23, Win 68,2 %**, FAIL **nur wegen N<30**. Deckt sich exakt mit unserem Register: alle guten `tm_base="overnight"`-Trials sind `momentum` (expR +0,046 bis +0,060), alle schlechtesten sind `fade` (bis −0,131).

**8. Prop-Regel-Grauzone, vor dem Live-Einsatz klären.** FundedNext listet *"Gapped or Illiquid Market Trading"* ausdrücklich unter den verbotenen Strategien, E8 formuliert mit *"Gapped, Illiquid Market Trading"* plus *"micro-scalping during illiquid market hours"* noch enger ([[Research-Cache]] Z. 1358/1362). Der Wortlaut zielt auf das Ausnutzen dünner Bücher, nicht auf eine normale RTH-Order um 09:30 — aber eine Strategie, die "Gap" im Namen trägt, gehört vor dem Deploy schriftlich beim Support abgesichert. Betrifft FN1/FN2 direkt. Siehe [[Firm-Regeln je Konto]].

---

## Register-Stand (22.09.2026)

| Griff | Zahl |
|---|---|
| `n_total` im Register | **65.613 Trials** |
| `mode="gap"` | **397** (RTY 225, NQ 116, ES 29, YM 27) |
| davon Survivors | **143** (RTY 98, NQ 45, ES 0, YM 0) |
| Gap-Seite | `fade` 344 Trials / **143 Survivors** · `continuation` 53 Trials / **0 Survivors** |
| Gap-Trials nach dem Roll-Garbage-Fix (30.08.) | **2** (beide ES-Montag, beide `premise_failed`) |
| `tsmom` `tm_base="overnight"` (Gap als Signal) | **145** (NQ 95, ES 50), **0 Survivors** |
| `tm_on_ret_min/max` (Größe als Tor) | 90, alle NQ, alle aus zwei ONORB-Jobs — **nie zusammen mit dem Gap-Signal** |
| `tm_on_dir` (Nachtrichtung als Tor) | **0** |
| `gap_cutoff_min` abweichend vom Default | **0 von 397** |
| `gap_dow` gesetzt | **2** |
| `rv_mode="gap_div"` (RV-08/09/10) | je 1, alle drei `premise_failed` (03.09.) |
| Gap-Jobs in der Queue mit Status `pending` | **0** (35 Gap-Jobs, alle `done` oder `premise_failed`) |
| Buch heute | **3 Beine**: NQ_Momentum_d260818, NQ_LastHour_v3, NQ_Asia-Dir-USopen_d260820 |

**Achsen-Abdeckung im Gap-Modus:** `gap_atr` dicht zwischen 0,2 und 1,75 (Block 1,0/3,0 mit 32 Trials), nie unter 0,2 als `lo`, nie über 3,0 als `hi` · `gap_confirm_min` nur 5 / 10 / 15 (147 / 186 / 62), nie 0 und nie 20-30 · `target_mult` und `be_trigger` gut abgedeckt (Exit-Sweeps).

---

## Wege-Tabelle

| Weg | Bewegung | Etikett | Rolle | Stand | Engine-Weg | Buch-Bezug |
|---|---|---|---|---|---|---|
| [[#W1]] | Gap-up, Preis läuft hin zum Vortages-Close (Short bis Fill) | Mean Reversion | Signal | gemessen, Seite nie getrennt (344 Trials, 143 Surv, 0 Kandidaten) | `gap` fade ✅ / `tsmom` overnight+fade ✅ | Ersatz NQ_Asia-Dir |
| [[#W2]] | Gap-down, Preis läuft hin zum Vortages-Close (Long bis Fill) | Mean Reversion | Signal | wie W1, in denselben Trials vermischt | dito | Ersatz NQ_Asia-Dir |
| [[#W3]] | Preis läuft weg vom Vortages-Close (Continuation) | Trend Following | Signal | gemessen ohne Kandidat (53 gap-Trials, **0 Surv**; 145 tsmom-Trials, alle Bestwerte auf dieser Seite) | `tsmom` overnight+momentum ✅ | Ersatz NQ_Asia-Dir |
| [[#W4]] | Fill erreicht, dann weiter in Gap-Richtung (Fill-and-Go) | Trend Following | Signal | **offen, 0 Trials** | Modul-Spec S-GAP-5 | neues Bein |
| [[#W5]] | Durch den Fill hindurch, weiter gegen die Gap-Richtung | Mean Reversion | Exit | **offen, 0 Trials** | Modul-Spec (Ziel-Verlängerung) | Exit-Achse von W1/W2 |
| [[#W6]] | Fill wird angetestet und scheitert, Preis dreht zurück | Trend Following | Signal | **offen, 0 Trials** | Modul-Spec S-GAP-5 | neues Bein |
| [[#W7]] | Preis kreuzt den Vortages-Close und hält bis Close | Trend Following | Signal | **offen, 0 Trials** | Modul-Spec S-GAP-5 | Achse von W4 |
| [[#W8]] | Preis läuft am Vortages-Close entlang (Pendeltag) | — | Filter | **keine Story, weil** kein Akteur dahinter steht — beschreibt einen Tag ohne Ereignis | — | — |
| [[#W9]] | Open jenseits Vortages-Hoch/-Tief (echter Gap, Neuland) | Trend Following | Filter | **offen, 0 Trials** | Modul-Spec S-GAP-2 | Ersatz NQ_Asia-Dir |
| [[#W10]] | Open innerhalb der Vortages-Range | Mean Reversion | Filter | **offen, 0 Trials** | S-GAP-2 | Gegenzelle zu W9 |
| [[#W11]] | Echter Gap läuft weiter (Preisfindung ohne Anker) | Trend Following | Signal | **offen, 0 Trials** | S-GAP-2 + W3 | Achse von W9 |
| [[#W12]] | Lage des Vortages-Close in der Vortages-Range als Tor | Intraday Bias | Filter | **offen, 0 Trials** | S-GAP-2 | Tor auf W1/W3 |
| [[#W13]] | Gap in Richtung des Vortagstrends | Trend Following | Filter | **offen, 0 Trials** (`prev_rth` da, Tor fehlt) | Modul-Spec S-GAP-3 | Tor auf NQ_Momentum |
| [[#W14]] | Gap gegen den Vortagstrend | Mean Reversion | Filter | **offen, 0 Trials** | S-GAP-3 | Tor auf NQ_Momentum |
| [[#W15]] | Winzige Gaps (< 0,2 ATR) | Mean Reversion | Filter | offen, aber **Achse** von W1/W2, kein eigener Weg | ✅ | — |
| [[#W16]] | Kleine/mittlere Gaps (0,2-1,0 ATR) | Mean Reversion | Filter | dicht gemessen, **Achse** | ✅ | — |
| [[#W17]] | Große Gaps (1,0-3,0 ATR) | Trend Following | Filter | dünn gemessen (32 Trials), **Achse** von W3 | ✅ | — |
| [[#W18]] | Extremgaps (> 3 ATR) | Trend Following | Filter | **offen, 0 Trials**, aber Frequenz-Gate erschlägt es voraussichtlich | ✅ | kein Skelett |
| [[#W19]] | Zweiter Gap in dieselbe Richtung (Serie) | Trend Following | Filter | **offen, 0 Trials** | Modul-Spec S-GAP-4 | Tor auf NQ_Momentum |
| [[#W20]] | Gap gegen das gestrige Gap | Mean Reversion | Filter | **offen, 0 Trials** | S-GAP-4 | Gegenzelle zu W19 |
| [[#W21]] | Ungefülltes Gap vom Vortag als Magnet für heute | Mean Reversion | Level | **offen, 0 Trials** | S-GAP-4 | Achse von W19 |
| [[#W22]] | Gap nach dem Wochenende (Montag) | Intraday Bias | Filter | gemessen ohne Kandidat auf ES (2 Trials, `premise_failed`), **0 auf NQ** | `tsmom` + `tm_dow` ✅ | neues Bein |
| [[#W23]] | Gap nach Feiertag/verlängerter Pause | Intraday Bias | Filter | **offen, 0 Trials** (kein Feiertagskalender) | Modul-Spec (Feiertagsliste) | Achse von W22 |
| [[#W24]] | Gap an/nach Makro-Tagen (CPI/NFP/FOMC) | Intraday Bias | Filter | **offen, 0 Trials** im Gap-Kontext | Modul-Spec (News-Flag generalisieren) | Tor auf W1/W3 |
| [[#W25]] | Länge des Bestätigungsfensters | — | Filter | gemessen 5/10/15, nie 0 und nie 20-30 — **Achse** | ✅ | — |
| [[#W26]] | Später Einstieg (Nachmittags-Fill statt erste Stunde) | Mean Reversion | Signal | **offen** (Cutoff in 395/397 Trials auf Default) | `tsmom` ✅ | Ersatz NQ_LastHour_v3 |
| [[#W27]] | Gapgröße als Tor auf ein bestehendes Bein | — | Filter | gemessen, fremd (90 Trials, zwei ONORB-Jobs) | ✅ | gehört [[Overnight-Bias ORB Wege-Karte]] W23 |
| [[#W28]] | Gaptag als Sizing-/Risiko-Modulator | — | Sizing | **offen, 0 Trials** — bei uns Buch-Ebene, nicht Bein-Ebene | kein Pfad | kein Bein |
| [[#W29]] | Gap-Differenz zwischen zwei Index-Futures konvergiert | Relative Value | Signal | **`premise_failed`** (RV-08/09/10, je 1 Trial) — nie widerlegt, nur nie gerechnet | `rv gap_div` ✅, aber `rv` ohne Null-Schalter | Bank-Zeilen stehen |
| [[#W30]] | Derselbe Gap-Weg auf GC/CL | Trend Following | Signal | **offen, 0 Trials** | `tsmom` overnight ✅ | neues Bein |
| [[#W31]] | **Wartung:** RTY_Gap-fade nach dem Roll-Fix neu bewerten | Mean Reversion | Signal | **Wiedervorlage offen** (#135 nie nachgeholt) | `gap` + S-GAP-1 | Wiederaufnahme oder sauberes Urteil |
| [[#W32]] | **Wartung:** NQ_Gap-fade_hf am heutigen Buch/Betriebspunkt | Mean Reversion | Signal | **stale** (Urteil gegen ein Buch, das es nicht mehr gibt) | `gap` + S-GAP-1 | neues Bein |
| [[#W33]] | Long und Short getrennt führen | — | Filter | **strukturell unmöglich** im `gap`-Modus, im `tsmom`-Pfad frei — **Achse** | `tsmom` ✅ | — |
| [[#W34]] | Gap füllt nicht heute, sondern in den Folgetagen **(Swing)** | Swing | Signal | **offen, 0 Trials** · `swing: true` | kein Halten über Nacht möglich | **Live-Buch-Merker, nicht Prop-Buch** (E8 verbietet Halten) |

**Vollständigkeit:** W8 ist der einzige Weg ohne Story. W15/W16/W17/W25/W33 sind ehrlich als **Achsen** markiert und zählen nicht als eigene Wege — sie stehen trotzdem in der Tabelle, damit sichtbar ist, dass sie geprüft wurden. W5/W7 hängen an derselben Modul-Spec wie W4 und bekommen kein eigenes Skelett; W18 und W28 keins aus Frequenz- bzw. Ebenen-Gründen; W27 und W29 gehören anderen Karten bzw. bestehenden Bank-Zeilen und werden nicht dupliziert.

---

## Block A — Preis gegen den Vortages-Close (die Fill-Linie)

### W1 / W2 → **GAP-W1a** (Rang 2) · Hin zum Vortages-Close, Seiten getrennt

**Bewegung:** Gap-up, Preis läuft zurück nach unten zum Vortages-Close (W1, Short) bzw. Gap-down, Preis läuft zurück nach oben (W2, Long).
- **Story:** Wer die Neubewertung der Nacht nicht mitgemacht hat, bekommt sie am Open zum Vorzugspreis angeboten und nimmt sie — das zieht den Preis zurück zum letzten fairen Preis, an dem alle noch dabei waren. Das Geld liegt hier **nicht mehr frei herum** (344 Trials, 143 Survivors, 0 Kandidaten), es bleibt nur offen, weil drei Dinge nie in derselben Zelle standen: echte Bestätigung, Größenband und **getrennte Seiten**.
- **Stand:** gemessen ohne Kandidat, Seiten nie getrennt. `gen_gap_NQ` 0 Kandidaten (PBO 71-96 %, Zufallsband), `hf_NQ_Gap_daily` 33 Trials / 0 Kandidaten, `gapfade_retune_RTY_260824` 53 Trials / 0 Kandidaten bei sauberer Selektion (PBO 3 %).
- **Engine-Weg:** ✅ heute rechenbar als `tsmom tm_base="overnight" tm_side="fade"` + `AX_CONFIRM` + `tm_on_ret_min/max` + `tm_dir`.
- **Buch-Bezug:** Ersatz für `NQ_Asia-Dir-USopen_d260820` (beide sind Overnight-Bias-Beine, gleicher Slot).
- **Verwandte Tote (Kontaminationswarnung):** `ideas.json` "Overnight-Gap-Fade" (getötet) und "Gap-Fade klein" (getötet; AP116-Korrektur: **tot an der Selektions-/Buch-Stufe, nicht an der Prämisse**) · [[Strategie-Logbuch]] #130 (RTY-Abschuss) · **[[Session Momentum Wege-Karte]] SES-W6a — dieselbe Zeile, Auflage "Reparatur TN-03 statt neuer ID", `prior='low'` + Prescan, noch nicht gerechnet.** Was anders ist als bei den Toten: getrennte Seiten und Bestätigungsachse, beides nie gemessen. Was gleich ist: der Mechanismus. **Ohne die Seitentrennung ist das ein Aufwärmen.**
- **Research-Frage:** Gap-Fill auf Index-Futures nach Größe **und** mit Bestätigungsfenster — gibt es das als Quelle? Und gegen welche Definition läuft die Praktiker-Zahl "70-75 % füllen"?

### W3 → **GAP-W3a** (Rang 1) · Weg vom Vortages-Close (Continuation)

**Bewegung:** Gap-up läuft weiter nach oben, Gap-down weiter nach unten.
- **Story:** Ein großes Gap ist keine Verirrung, sondern eine Neubewertung, die im dünnen Globex-Buch stattfand. Die liquiden RTH-Desks müssen ihre Bücher an den neuen Preis anpassen, und dieses Umschichten dauert Stunden, nicht Minuten. Das Geld bleibt liegen, weil die Klasse bei uns **nur unbestätigt und ohne Größenband** gemessen wurde.
- **Stand:** gemessen ohne Kandidat. 53 `gap`-Trials `continuation`, **0 Survivors**. 145 `tsmom`-Overnight-Trials, 0 Survivors — aber **alle fünf besten davon sind `momentum`** (expR +0,046 bis +0,060, Fails `top5`/`cost2t`/`OOS`), alle schlechtesten sind `fade` (bis −0,131). Keine einzige dieser 145 Zellen hatte eine Bestätigungs- oder Größenachse an.
- **Engine-Weg:** ✅ `tsmom tm_base="overnight" tm_side="momentum"` + `AX_CONFIRM` + `tm_on_ret_min/max` + `tm_dir` + `AX_EXITS`.
- **Buch-Bezug:** Ersatz für `NQ_Asia-Dir-USopen_d260820`.
- **Verwandte Tote:** `ideas.json` "Gap-Continuation (große Gaps)" = **Validiert**, D-Note, 17 Trades/Jahr, nie ins Buch · [[Strategie-Logbuch]] #045 (Lucid-Recheck: Gap-cont verschlechtert das damalige 6-Bein-Buch) · #139 (Pool-Neuaufbau: Gap-cont −4 bis −15 pp OOS). **Neuer Grund gegenüber diesen Toten:** die externe Continuation-Messung mit T=+3,23 (Mesfin Tab. 5) und die Tatsache, dass beide alten Ablehnungen gegen ein 5-6-Bein-Buch liefen, das es nicht mehr gibt.
- **Research-Frage:** Gibt es eine Primärquelle, die Gap-Continuation nach **Größe** trennt (Schwelle in ATR/Sigma), statt nur "große Gaps laufen"?

### W4 → **GAP-W4a** (Rang 8) · Fill-and-Go

**Bewegung:** Preis läuft zum Vortages-Close, füllt den Gap — und läuft danach weiter in die ursprüngliche Gap-Richtung.
- **Story:** Der Fill ist ein Magnet, aber kein Ziel. Die Limit-Orders derer, die auf den Fill warten, liegen genau am Vortages-Close. Sind sie abgearbeitet, ist der Widerstand weg, und die Neubewertung der Nacht setzt sich durch — jetzt ohne Gegenpartei. Das erklärt, warum Fade und Continuation bei uns **beide halb** funktionieren: der Tag hat oft beide Phasen, und wir messen immer nur die erste.
- **Stand:** **offen, 0 Trials.** Im Code ist der Fill ausschließlich ein Exit (`target = prev_close`).
- **Engine-Weg:** Modul-Spec S-GAP-5 (`gap_side="fill_and_go"`, ~25 Zeilen) **plus** S-GAP-1 (Null-Schalter), sonst nicht deploy-fähig.
- **Buch-Bezug:** neues Bein.
- **Verwandte Tote:** [[Strategie-Logbuch]] #028 — die Fill-Bug-Lehre gilt für die Ausführung dieses Wegs unmittelbar: eine Stop-Order füllt beim Gap **am Open, nie am Level**.
- **Research-Frage:** Misst jemand den Preispfad **nach** einem Fill?

### W5 · Overfill (durch die Fill-Linie hindurch)
**Offen, 0 Trials.** Bei `fade` ist das Ziel fix `prev_close`; `target_mult` wirkt nur bei `continuation`. Ein Fade, der über den Fill hinaus laufen darf, ist in der Engine nicht darstellbar (Ziel-Verlängerung, ~5 Zeilen). **Kein eigenes Skelett:** das ist eine Exit-Achse von W1/W2 und gehört in deren Grid, nicht in eine eigene Hypothese.

### W6 · Fade des Fades
**Offen, 0 Trials.** Preis läuft Richtung Fill, erreicht ihn nicht, dreht zurück in Gap-Richtung. Story hält (die Fill-Erwartung selbst erzeugt die Gegenbewegung, und wenn sie scheitert, sind die Fill-Käufer gefangen) — braucht aber dieselbe Ereignis-Mechanik wie W4. **Kein eigenes Skelett vor W4**, sonst wird dieselbe Spec zweimal bezahlt.

### W7 · Kreuzen und halten
**Offen, 0 Trials.** Schluss jenseits des Vortages-Close nach einem Gap in die Gegenrichtung. **Achse von W4** (Exit-Variante "bis EOD halten"), kein eigenes Skelett.

### W8 · Entlanglaufen am Vortages-Close
**Keine Story, weil** dahinter kein Akteur steht: das beschreibt einen Tag, an dem nichts passiert. Als No-Trade-Tor für andere Beine denkbar, aber ein Tor ohne Why ist eine Kurvenanpassung. Bleibt bewusst ohne Skelett.

---

## Block B — Gap gegen die Vortages-RANGE statt gegen den Vortages-Close

### W9 / W10 / W11 → **GAP-W9a** (Rang 5) · Echter Gap gegen Gap in der Range

**Bewegung:** Open jenseits des Vortages-Hochs bzw. -Tiefs (echtes Neuland) gegen Open innerhalb der gestrigen Spanne.
- **Story:** Ein Gap, das innerhalb der Vortages-Spanne bleibt, springt über Preise, an denen gestern real gehandelt wurde — dort liegen Orders, Erinnerungen und ein bekannter fairer Wert, also füllt es leicht. Ein Gap über das Vortages-Hoch hinaus eröffnet in Preisen, die **noch nie gehandelt wurden**: es gibt keinen Anker, zu dem der Preis zurückkehren könnte, und die Preisfindung läuft weiter. **Das ist die wahrscheinlichste Erklärung dafür, dass Fade und Continuation bei uns beide je zur Hälfte funktionieren — wir mischen zwei verschiedene Ereignisse in einer Zelle.**
- **Stand:** **offen, 0 von 397 Trials.** `daily_context` kennt Vortages-Hoch und -Tief nicht.
- **Engine-Weg:** Modul-Spec S-GAP-2 (~12-15 Zeilen, kein Engine-Kern, alle Werte Vortageswerte → kein Look-ahead).
- **Buch-Bezug:** Ersatz für `NQ_Asia-Dir-USopen_d260820`.
- **Verwandte Tote:** [[Overnight-Bias ORB Wege-Karte]] W23 (Gapgröße als Tor, `gap_pct_max` mit 0 Trials) — anderes Maß, kein Duplikat.
- **Research-Frage:** Trennt jemand diese beiden Klassen und bewertet sie getrennt? Gibt es Füllwahrscheinlichkeiten je Klasse?

### W12 · Lage des Vortages-Close in der Vortages-Range
**Offen, 0 Trials.** Ein Schluss am Tageshoch mit Gap-up ist etwas anderes als ein Schluss in der Mitte mit Gap-up (im ersten Fall ist der Trend intakt, im zweiten ist der Gap eine Meinungsänderung). Hängt an derselben Spec S-GAP-2, ist aber eine **Achse** von W9/W13 — kein eigenes Skelett, damit nicht dieselbe Fläche doppelt gegen die Zufallsdecke zählt.

---

## Block C — Gap gegen den Vortagstrend

### W13 / W14 → **GAP-W14a** (Rang 6)

**Bewegung:** Gap in Richtung des gestrigen RTH-Tages (W13) gegen Gap gegen ihn (W14).
- **Story:** Ein Gap gegen die Richtung des gestrigen Handelstages ist ein Meinungswechsel, der über Nacht in dünnem Buch stattfand — die Akteure, die gestern in die Gegenrichtung gekauft haben, sind noch da und verteidigen ihre Position, deshalb fällt der Gap zurück. Ein Gap in Richtung des gestrigen Tages ist dagegen die Fortsetzung einer laufenden Umschichtung und bekommt am Open zusätzliche Nachfrage.
- **Stand:** **offen, 0 Trials.** `prev_rth` liegt seit Monaten in `daily_context`, wird aber von **keinem einzigen** Gap-Trial benutzt: die Familie kennt nur den Sprung, nie den Tag davor.
- **Engine-Weg:** Modul-Spec S-GAP-3 (~10 Zeilen, `tm_prev_rth_dir` analog zum vorhandenen `tm_on_dir`; bewusst **nicht** in `gates_pass`, weil dort die Handelsrichtung noch nicht feststeht).
- **Buch-Bezug:** Tor auf `NQ_Momentum_d260818` (Ersatz-Semantik).
- **Verwandte Tote:** Bank **TN-05** (Vortages-RTH-Return als Bias) und **TS-05** (Basis open gegen prev_close) — beide messen `prev_rth` als *Signal*, hier ist es ein *Tor*. Abgrenzung muss im Why stehen.
- **Research-Frage:** Sagt Lou/Polk/Skouras oder die Nachfolgeliteratur etwas zur **Interaktion** beider Vorzeichen, statt nur zu jedem Segment für sich?

---

## Block D — Größenklassen (W15-W18)

**Alle vier sind Achsen, keine eigenen Wege** — das ist die ehrliche Buchführung, eine Reparametrisierung ist kein Weg.
- **W15 winzig (< 0,2 ATR):** nie getestet, `gap_atr_lo` ging nie unter 0,2. Gehört als zusätzliche Bandgrenze in das Grid von GAP-W1a. Kostenschwelle mitdenken (MNQ-Round-Trip ~2 Punkte) — bei NQ ist 0,2 ATR immer noch deutlich über der Schwelle, das ist also kein Ausschlussgrund.
- **W16 klein/mittel (0,2-1,0):** der dicht gemessene Kern der 344 Fade-Trials.
- **W17 groß (1,0-3,0):** nur 32 Trials, das ist die **dünnste Stelle der ganzen gemessenen Fläche** und genau die Region, in der die externe Continuation-Evidenz liegt. Gehört ins Grid von GAP-W3a.
- **W18 extrem (> 3 ATR):** 0 Trials. Frequenz-Gate (`min_tpy=25`) erschlägt das voraussichtlich — solche Tage gibt es einstellig pro Jahr. Kein Skelett.

---

## Block E — Gap nach Gap (das Wort "Pattern")

### W19 / W20 / W21 → **GAP-W19a** (Rang 9)

**Bewegung:** zweiter Gap in dieselbe Richtung (W19), Gap gegen das gestrige Gap (W20), ungefülltes Gap vom Vortag als Magnet (W21).
- **Story:** Ein einzelner Gap ist ein Ereignis, zwei Gaps in dieselbe Richtung sind ein **Prozess**: eine Adresse, die über mehrere Nächte umschichtet und dafür jeweils die dünne Globex-Session nutzt, weil sie im RTH zu viel Marktwirkung hätte. Das ist der Unterschied zwischen Nachricht und Fluss, und nur der Fluss ist prognostizierbar, weil er per Definition noch nicht fertig ist.
- **Stand:** **offen, 0 Trials.** Alle 397 Gap-Trials sehen genau einen Tag.
- **Engine-Weg:** Modul-Spec S-GAP-4 (~18 Zeilen, setzt S-GAP-2 voraus → gemeinsam bauen).
- **Buch-Bezug:** Tor auf `NQ_Momentum_d260818`.
- **Verwandte Tote:** Bank **TN-01** ("setzt sich der Overnight-Return von Tag zu Tag fort", 97 Trials, 0 Survivors) — das ist der **lineare** Vorläufer dieser Frage. Neuer Winkel: Serie/Schwelle statt Gewicht, plus "ungefüllt" als Zustand.
- **Research-Frage:** Was meint die Oxford-Seite mit "Gap Pattern" — Intraday-Ablauf oder Mehrtages-Muster? Falls Letzteres, ist W19 der eigentliche Kern des Auftrags.

---

## Block F — Kalender

### W22 → **GAP-W22a** (Rang 11) · Montags-Gap
- **Story:** Zwischen Freitag-Close und Montag-Open liegen rund 65 Stunden, in denen Nachrichten anfallen, aber niemand handeln kann. Der Montags-Gap ist deshalb gebündelte Information, kein Rauschen der dünnen Nacht — er muss sich anders verhalten als ein normaler Übernacht-Gap.
- **Stand:** gemessen ohne Kandidat **auf ES** (`cal_mongap_ES`, 2 Trials, `premise_failed`: fade expR −0,375 / continuation −0,265 auf 256 Trades) — **0 Trials auf NQ**. Zwei Gründe, warum das ES-Ergebnis NQ nicht erschlägt: das Band war `gap_atr 0,0-5,0` (also ungefiltert, alle Montage), und ES ist über **alle** Preis-Momentum-Modi leer (Survivor-Quote 3,6 % gegen NQ 28 %).
- **Engine-Weg:** ✅ `tsmom tm_base="overnight"` + `tm_dow=[0]`, Kontrastzelle Di-Fr im selben Grid.
- **Verwandte Tote:** Bank TN-09 (Wochentags-Struktur, 21 Trials) · [[Research-Cache]]: French 1980 (Montagseffekt S&P 1953-77), in modernen Märkten instabil.
- **Research-Frage:** Montags-Gap auf Index-**Futures** nach 2010? Und reicht die Frequenz bei 52 Montagen im Jahr überhaupt für `min_tpy=25`, wenn zusätzlich ein Größenband greift?

### W23 · Feiertags-Gap
**Offen, 0 Trials.** Dieselbe Story wie W22, nur stärker (verlängertes Wochenende). Braucht eine Feiertagsliste in der Engine — die existiert nirgends. **Achse von W22**, kein eigenes Skelett, aber die Liste wäre billig und würde auch anderen Karten dienen.

### W24 · Makro-Tag-Gap
**Offen, 0 Trials im Gap-Kontext.** Ein Gap nach CPI/NFP/FOMC hat einen benennbaren Erzeuger, ein Gap ohne Nachricht nicht — das ist die sauberste Trennung "Nachricht gegen Rauschen", die es gibt. `lh_exclude_news` existiert, aber nur für `mode="last_hour"`. **Modul-Spec (News-Flag generalisieren) nötig**, danach Tor auf W1/W3. Kein eigenes Skelett, weil es als Achse von GAP-W1a/GAP-W3a mehr wert ist als als eigenes Bein.

---

## Block G — Zeit und Ausführung

### W26 → **GAP-W26a** (Rang 7) · Der späte Fill
- **Story:** Die Eröffnungsauktion und die erste Stunde sind der lauteste Teil des Tages: höchste Spreads, höchste Slippage — und genau dort steigen alle Gap-Strategien ein. Wenn der Fill ein Flow-Effekt ist (Nachzügler, die die Nacht verpasst haben), muss er nicht in 60 Minuten passieren, sondern kann den ganzen Tag dauern. Dann verdient der späte Einstieg mehr, weil er die Eröffnungs-Reibung nicht bezahlt.
- **Stand:** **offen.** `gap_cutoff_min` steht in 395 von 397 Trials auf dem Default 60 — die Achse wurde faktisch nie variiert.
- **Engine-Weg:** ✅ `tsmom tm_base="overnight"` mit `tm_sig_len` 120/180/240 und gestaffeltem `tm_cutoff_min`.
- **Buch-Bezug:** Ersatz für `NQ_LastHour_v3` (gleicher Tagesabschnitt, direkter Marginal-Vergleich möglich).
- **Verwandte Tote:** Mesfin Tab. 5 misst genau die **frühen** Zeitpunkte (09:30 / 09:45 / 10:00) und findet sie alle negativ — das ist eher Rückenwind für diesen Weg als Gegenwind.
- **Research-Frage:** Gap-Fill-Wahrscheinlichkeit als Funktion der Tageszeit (Hazard-Rate)?

### W25 · Bestätigungsfenster
**Achse.** Gemessen 5 / 10 / 15 Minuten (147 / 186 / 62 Trials), **nie 0** (also ohne Bestätigung, sofort am Open) und **nie 20-30**. Gehört als Achse in GAP-W1a/GAP-W3a. #038 hat auf RTY bereits eine monotone Sensitivität gezeigt (10 > 15 > 20) — das ist ein Hinweis, kein Beweis.

### W27 · Gapgröße als Tor auf ein bestehendes Bein
**Gemessen, aber woanders:** 90 Trials mit `tm_on_ret_min/max`, alle NQ, alle aus `on01_cashopen_decision_NQ` (54) und `hyp_ONORBW45a_NQ` (36). Gehört in die [[Overnight-Bias ORB Wege-Karte]] (W23) — hier bewusst **kein Duplikat**.

### W28 · Gaptag als Sizing-Modulator
**Offen, 0 Trials, kein Pfad.** Sizing ist bei uns Buch-Ebene (`funded_frontier`, `evaluate_v2`), nicht Bein-Ebene. Eine Hypothese "an Gaptagen kleiner traden" wäre eine Buch-Politik-Frage und gehört zum Quant-Team, nicht in diese Karte. Bleibt ohne Skelett.

---

## Block H — Andere Märkte und Cross-Instrument

### W29 · Gap-Divergenz zwischen zwei Index-Futures
**Stand: `premise_failed`, nicht tot.** RV-08 (NQ/ES), RV-09 (RTY/ES), RV-10 (NQ/YM) liefen am 03.09.2026 mit je **einer** Config und scheiterten an der Prämisse. Der `gap_div`-Bug in `rv.py` ist seit dem 31.08. gefixt ([[Strategie-Logbuch]] #139). Zusatzhürde: **`mode="rv"` hat ebenfalls keinen Null-Schalter.** Die Bank-Zeilen stehen bereits — **kein neues Skelett von mir**, das wäre Doppelzählung. Wiedervorlage gehört an die bestehenden Zeilen.

### W30 → **GAP-W30a** (Rang 10) · Gap auf GC/CL
- **Story:** Bei Index-Futures entsteht das Gap aus globaler Risikoneubewertung — dieselbe Information, die auch RTH handelt, nur in dünnem Buch. Bei Gold und Öl entsteht es aus etwas strukturell anderem: London-Fix und asiatische physische Nachfrage bei GC, Nachrichten aus Förderländern und Positionierung vor den wöchentlichen Lagerdaten bei CL. **Die Erzeuger sind nicht dieselben Akteure, die tagsüber in New York handeln** — deshalb ist offen, ob die US-Eröffnungsauktion diese Bewegung bestätigt oder zurückholt.
- **Stand:** **offen, 0 Trials** (0 von 397 und 0 von 145), obwohl beide Reihen vorliegen: GC 2015-12-28 bis 2026-07-24, CL 2015-12-30 bis 2026-07-21.
- **Engine-Weg:** ✅ `tsmom tm_base="overnight"`, sofort rechenbar.
- **Bekannte Lücke, kein Freifahrtschein:** `controls.ctl_symbols` kennt keinen Vergleichskorb für GC/CL → die Multi-Markt-Kontrolle wird **nicht gerechnet** (`ok=None`). Und `asian.py` auf GC brachte am 22.09. 0 Kandidaten.
- **Research-Frage:** Ist die E8-/FundedNext-Handelbarkeit von GC/CL primärquellen-belegt (offenes Ticket `e8-instrumente-anfrage`)? Gibt es Arbeiten zum Rohstoff-Overnight-Gap getrennt nach Erzeuger?

---

## Block I — Wartung: zwei Urteile auf überholtem Grund

### W31 → **GAP-W31a** (Rang 4) · RTY_Gap-fade wurde auf kaputtem Lineal hingerichtet

> [!warning] Wiedervorlage, die nie stattfand
> **24.08.2026** ([[Strategie-Logbuch]] #130): Bein raus, weil es sein eigenes Top5-Gate mit 0,638 verfehlt, in 2 von 3 Epochen negativ ist und schlechter als seine Grid-Nachbarn liegt. Retune-Job `gapfade_retune_RTY_260824` sauber (PBO 3 %), aber 0 Kandidaten.
> **30.08.2026** (#135): der Roll-Garbage-Fix zeigt, dass **genau dieses Bein unterschätzt** war — 222 → 211 Trades, expR 0,0551 → **0,0595**, Sharpe 1,114 → **1,211**.
> **Seither:** im Register stehen nach dem 30.08. exakt **2** Gap-Trials, beide ES-Montag. Die Gates, an denen das Bein starb, wurden nie auf den bereinigten Daten nachgerechnet.

- **Stand:** Wiedervorlage offen. Nach der Regel „tot ist ein Urteil mit Reichweite" (CLAUDE.md, 22.09.) ist das ein `empirisch-nichts-gefunden`-Urteil auf einem Messwerkzeug, das sechs Tage später als fehlerhaft bekannt wurde.
- **Engine-Weg:** `gap` + Modul-Spec S-GAP-1. **Zusatzprüfung:** RTY-Historie endet im Bestand am 10.08.2026 — Datenstand vor dem Urteil prüfen, sonst ist die Revision selbst stale.
- **Buch-Bezug:** Wiederaufnahme oder ein sauberes, diesmal haltbares Urteil.

### W32 → **GAP-W32a** (Rang 3) · NQ_Gap-fade_hf am heutigen Buch

> [!warning] Das Urteil steht gegen ein Buch, das es nicht mehr gibt
> Der AP116-Marginal-Lauf vom **31.08.2026** (also **nach** dem Roll-Fix, datenseitig sauber) rechnete gegen ein **4-Bein-Buch inklusive `NQ_VWAP-Pullback`**. Dieses Bein ist inzwischen raus, das Buch hat **3 Beine**.
> Zahlen aus dem Lauf (Config: `gap` fade, `gap_atr 0,5-1,5`, `stop 0,75`, `confirm 10`): 25k 54,74 gegen 59,2 · 50k 78,81 gegen 82,59 · 100k 86,94 gegen 88,19 · **150k 90,68 gegen 83,85** · FN-Flex50k 68,64 gegen 74,45. Korrelation zum Bestand: Asia-Dir **−0,13**, LastHour +0,02, Momentum +0,09.
> **Der Tier, an dem der Kandidat gewinnt, ist genau der, den Max seit AP204 kauft (E8 150k, Start 02.10.).**

- **Stand:** stale. Das „schlechter/neutral" gilt für die damaligen Tiers und das damalige Buch, nicht für den heutigen Betriebspunkt.
- **Engine-Weg:** `gap` + Modul-Spec S-GAP-1 (ohne Null-Schalter kein `deploy_ready`).
- **Buch-Bezug:** neues Bein — der einzige Grund, warum ein Mean-Reversion-Bein hier etwas beitragen kann, ist die negative Korrelation zum Asia-Dir-Bein.
- **Kosten:** 0 neue Register-Trials (bestehende Config), damit die billigste Erkenntnis der ganzen Karte.

### W33 · Long und Short getrennt
**Achse, aber eine mit Befund:** im `gap`-Modus **strukturell unmöglich** (`_gap_trades` hat keinen `gap_dir`-Parameter, `tdir` folgt immer dem Gap-Vorzeichen). Alle 397 Trials mischen beide Seiten. Im `tsmom`-Pfad ist `tm_dir` frei — ein weiterer Grund, warum Rang 1 und 2 dort gebaut werden.

---

## Block J — Swing

### W34 · Mehrtages-Gap-Fill **(Swing)**
`swing: true` · Etikett **Swing** · Buch-Bezug **Live-Buch-Merker, nicht Prop-Buch**.
**Bewegung:** der Gap füllt sich nicht heute, sondern in den folgenden Tagen. **Story:** Gerade die großen Gaps, die intraday nicht zurückkommen, sind die, bei denen die Rückkehr über Tage läuft — der Fill ist dann ein Swing-Ziel, kein Intraday-Ziel. **Stand: offen, 0 Trials.** Die Engine kann über Nacht nicht halten, und E8 verbietet es ohnehin. **Kein Job-Vorschlag fürs Prop-Buch** — steht hier, damit die Regel „nichts, was je eine Edge zeigte, geht verloren" greift. Falls ein Live-Konto kommt, ist das der erste Gap-Weg, der dort hingehört.

---

## Modul-Specs

| Spec | Datei | Umfang | Schaltet frei |
|---|---|---|---|
| **S-GAP-1** Null-/Delay-Schalter für `mode="gap"` | `qbt._gap_trades` + `discovery/controls.py` (Z. 688, `ctl_delay`) | 15-20 Z. | W31, W32, W4-W7 — **ohne das kann kein Gap-Kandidat je `deploy_ready` werden** |
| **S-GAP-2** Vortages-Range im Kontext (`prev_high`, `prev_low`, `gap_beyond`, `prev_close_pos`) | `sigcore.daily_context` + `gates_pass` + `tsmom.DEFAULTS` | 12-15 Z. | W9, W10, W11, W12 |
| **S-GAP-3** Vortagstrend als Richtungs-Tor (`tm_prev_rth_dir`) | `tsmom.trades`, analog `tm_on_dir` (Z. 428-440) | 10 Z. | W13, W14 |
| **S-GAP-4** Gap-Historie (`prev_gap`, `gap_streak`, `prev_gap_filled`) | `sigcore.daily_context` + `tsmom.trades` | 18 Z. | W19, W20, W21 (setzt S-GAP-2 voraus) |
| **S-GAP-5** Fill als Einstiegs-Ereignis (`gap_side="fill_and_go"`) | `qbt._gap_trades` | 25 Z. | W4, W6, W7 (braucht S-GAP-1) |

**S-GAP-2, -3 und -4 gehören in einen Engine-Zug** (gemeinsamer Vortages-Kontext), nicht in drei.

---

## Reihenfolge nach Buch-Chance

Kriterien: Ersatz vor neu · engine-fähig vor Modul-Spec · ohne tote Verwandte vor kontaminiert · Wartung eines stale gewordenen Urteils vor neuer Fläche (kostet 0 neue Trials) · HF vor LF.

| Rang | ID | Weg | Engine | Buch-Bezug | Warum hier |
|---|---|---|---|---|---|
| 1 | **GAP-W3a** | W3 Continuation mit Bestätigung + Größenband | `tsmom` ✅ | Ersatz NQ_Asia-Dir | heute rechenbar, deploy-fähig, eigene Bestzahlen **und** externe Evidenz zeigen in dieselbe Richtung |
| 2 | **GAP-W1a** | W1/W2 Fade, Seiten getrennt (Reparatur TN-03) | `tsmom` ✅ | Ersatz NQ_Asia-Dir | gleiche Rechenkosten, aber externe Evidenz steht dagegen — deshalb hinter Rang 1 |
| 3 | **GAP-W32a** | W32 Bestandsrevision am 150k-Punkt | S-GAP-1 | neues Bein | 0 neue Trials, Urteil nachweislich stale, 150k war schon „besser" |
| 4 | **GAP-W31a** | W31 Wiedervorlage RTY nach Roll-Fix | S-GAP-1 | Wiederaufnahme | 0 neue Ideen, offene Pflicht aus #135 |
| 5 | **GAP-W9a** | W9/W10/W11 echter Gap vs. Gap in der Range | S-GAP-2 | Ersatz NQ_Asia-Dir | größte inhaltliche Lücke, erklärt möglicherweise alle bisherigen Nullergebnisse |
| 6 | **GAP-W14a** | W13/W14 Gap gegen/mit Vortagstrend | S-GAP-3 | Tor auf NQ_Momentum | billigste Spec, Kennzahl liegt schon da |
| 7 | **GAP-W26a** | W26 später Fill | `tsmom` ✅ | Ersatz NQ_LastHour_v3 | engine-fähig, aber schwächere Story als 1/2 |
| 8 | **GAP-W4a** | W4 Fill-and-Go | S-GAP-5 + S-GAP-1 | neues Bein | teuerste Spec, dafür der einzige echt neue Mechanismus |
| 9 | **GAP-W19a** | W19/W20/W21 Gap nach Gap | S-GAP-4 | Tor auf NQ_Momentum | hängt an der Oxford-Klärung (ist das „Pattern" gemeint?) |
| 10 | **GAP-W30a** | W30 GC/CL | `tsmom` ✅ | neues Bein | engine-fähig, aber Handelbarkeit unbelegt und Multi-Markt-Kontrolle nicht rechenbar |
| 11 | **GAP-W22a** | W22 Montags-Gap NQ | `tsmom` ✅ | neues Bein | Frequenz-Risiko (52 Montage/Jahr gegen `min_tpy=25`) |

**Zufallsdecke:** 11 Skelette bei 65.613 Trials. Wer alle elf gleichzeitig rechnen lässt, hebt die Decke für alle anderen Karten mit. Empfehlung: Rang 1-4 zuerst, danach neu bewerten.

---

## Offene Research-Fragen

1. Was meint die Oxford-Seite mit **„Gap Pattern"** — Intraday-Ablauf oder Mehrtages-Muster? (entscheidet über den Rang von W19)
2. Gap-Fill auf **Index-Futures** nach Gapgröße **und** mit Bestätigungsfenster — gibt es das? (W1)
3. Trennt jemand „Gap über das Vortages-Extrem" von „Gap innerhalb der Vortages-Range"? (W9)
4. Gap-Fill-Wahrscheinlichkeit als Funktion der **Tageszeit** (Hazard-Rate) statt Ja/Nein bis Close? (W26)
5. Preispfad **nach** einem Fill — Fortsetzung oder Umkehr? (W4)
6. Montags-Gap auf Index-Futures nach 2010 (nicht French 1980 auf Kassa)? (W22)
7. Overnight-Gap bei Rohstoff-Futures, getrennt nach Erzeuger (London-Fix GC, EIA-Woche CL)? (W30)
8. **E8/FundedNext:** fällt eine Gap-Strategie mit RTH-Entry unter die „Gapped Market Trading"-Klausel? Schriftliche Support-Antwort **bevor** ein Gap-Bein live geht. (Randbedingung 8)

---

## Dateien dieses Laufs

- Report: `C:\Users\maxlk\Projects\trading-data\engine\discovery\scout_reports\familien_gap_260922.md`
- Skelette: `C:\Users\maxlk\Projects\trading-data\engine\discovery\jobs_proposed\familien_gap_260922.json` (11 Stück, direkt als `args.hypotheses` für `ein-weg`)
- Diese Karte ist das lebende Register je Weg — `verdict-auditor` schreibt hier den Stempel zurück, Wege behalten ihre Nummern.

## Verwandte Notizen

[[Overnight-Bias ORB Wege-Karte]] · [[Session Momentum Wege-Karte]] · [[VWAP-Offensive]] · [[Rundzahlen Wege-Karte]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Research-Cache]] · [[Discovery-Runner v2]] · [[Alpha-Suche]] · [[Strategie-Familien]] · [[Familien-Scout Agent]] · [[Firm-Regeln je Konto]] · [[Buch-Workflow]]
