---
tags: [projekt, trading, alpha-suche, rvol, volumen]
erstellt: 2026-09-21
aktualisiert: 2026-09-21
status: aktiv
ziel: Zeit bis 50.000 $ Eigenkapital verkürzen, oder das RVOL-Kapitel sauber schließen
---

# RVOL Wege-Karte

**Ziel (einziges Kriterium):** **E[Zeit bis 50.000 $ Eigenkapital aus Payouts]** verkürzen, bei begrenzter Auslage. Passquote je Eval und Kosten pro funded Konto bleiben Zwischengrößen, nicht das Ziel. Nicht Sharpe, nicht Einzel-Edge, nicht Vollständigkeit der Taxonomie. Jede Zeile beantwortet am Ende: **Ersatz für welches Bein, oder neues Bein, und wie viel Zeit spart es?**

> [!warning] Kriteriumswechsel am 21.09.2026 — diese Karte wurde unter dem alten Ziel gebaut
> Die komplette Agent-Kette (`familien-scout`, Quant-Team, `verdict-auditor`, `variant-scout`, `strategy-auditor`) lief am 21.09. noch mit „Passquote je Eval" im Briefing. Am selben Abend hat Max das Kriterium auf **E[Zeit bis 50.000 $]** umgestellt und dabei **Min-Size 1 Kontrakt je Bein als Betriebspunkt gestrichen** („Größe wird gerechnet", siehe CLAUDE.md und [[Daily Notes/2026-09-21]]).
>
> **Was das ändert:** Die Sizing-Rolle (W18) war unter Min-Size 1 praktisch wertlos — kleiner als ein Kontrakt gibt es nicht, also blieb nur ein Gate an/aus. Mit gerechneter Größe ist die theta-optimale Gewichtung `f_i ∝ mu_i / sigma_i²` tatsächlich anfahrbar, und die vom `quant-mathematician` gemessene Varianz-Ordnung (sd 38,8 → 61,8 Punkte über RVOL-Dezile, monoton, Faktor 2,54 in der Varianz) wird damit direkt nutzbar statt nur eine Obergrenze zu sein. **W18 steigt deshalb von Rang 8 auf Rang 2, W23 fällt von Rang 4 auf Rang 6** (das Abschalt-Gate ist die grobe Krücke für dasselbe Problem — und es kann die E8-Inaktivitätsregel reißen, ein Runterskalieren nicht).
>
> Die Urteile über die Signal-Rolle (tot) sind vom Kriteriumswechsel **nicht** betroffen: sie hängen an der Kostenhürde von ~2 Punkten, nicht am Zielmaß.

Angelegt am 21.09.2026 vom `familien-scout` (Auftrag Max: Zerlegung **familienweise** über alle fünf [[Strategie-Familien]], unterversorgte Familien eigenständig auffüllen). Inventar gegen Register (65.035 Trials), Queue (1.004 Jobs, leer seit 20.09.), [[Strategie-Logbuch]] #031/#044/#067/#068/#098/#099/#125/#138, [[Hypothesen-Bank (Volumen & Flows)]] (180 Zeilen) und [[Research-Cache]] (Abschnitt vom 21.09.2026). Aufbau nach dem Vorbild [[VWAP-Offensive]]; Schwester-Karten desselben Agenten: [[Rundzahlen Wege-Karte]], [[Fibonacci Wege-Karte]], [[Session Momentum Wege-Karte]], [[ES-NQ-Divergenz Wege-Karte]].

Volle Belege und Zahlen im Report: `discovery/scout_reports/familien_rvol_260921.md`. Skelette als JSON: `discovery/jobs_proposed/familien_rvol_260921.json`.

> [!warning] Der Kern des Konzepts ist zweimal ehrlich tot — und das ist der Wert dieser Karte
> „Hohes RVOL sagt Fortsetzung voraus" ist bei uns **gemessen und erledigt**: [[Strategie-Logbuch]] **#068** (OR-RVOL ehrlich auf NQ, „Index in Play" überträgt sich NICHT von Aktien auf Index-Futures) und **#125** (volshock, 52k/26k Buckets 2016-2026, kein Trefferquoten-Shift — High-RVOL-Terzil liegt sogar 1-3 pp UNTER dem Low-Terzil). Der einzige scheinbare Positivbefund (**#031/#044**, RVOL ≥ 1,2 als ORB-Qualitätsfilter) war ein **Look-ahead-Artefakt**, entlarvt in **#067** — er darf nirgends mehr als Stütze zitiert werden.
>
> Von 40 Wegen tragen deshalb **13** ein Skelett, und die drei bestplatzierten davon behaupten bewusst **keine Richtungsprognose aus Volumen**, sondern nutzen RVOL als Kontroll-, Abschalt- oder Skalen-Variable. Wer hier zwanzig Hypothesen produziert, hebt nur die Zufallsdecke für alle anderen.

> [!danger] Befund A (neu, 21.09.2026) — `maband` misst als „RVOL" faktisch eine Uhrzeit
> `maband.py:528` setzt das Referenzfenster hart auf `window_vol_median(df, 0, 30)` (die ersten 30 Minuten), der Zähler ist aber **Session-Beginn bis Signalende** (`maband.py:623`, `sig_i0=0, sig_i1=j1`). Der Zähler wächst also mit der Tageszeit, der Nenner ist konstant. Auf NQ über die volle Historie gemessen:
>
> | Minuten nach Open | Median-„RVOL" | Anteil ≥ 1,2 | Anteil ≥ 1,6 |
> |---|---|---|---|
> | 15 | 0,63 | 0,6 % | 0,1 % |
> | 45 | 1,42 | 77,5 % | 31,3 % |
> | 60 | 1,74 | 92,5 % | 63,8 % |
> | 120 | 2,79 | 97,2 % | 96,0 % |
> | 240+ | 4,22+ | 100 % | 100 % |
>
> `tm_rvol_min=1.2` heißt auf diesem Pfad praktisch **„handle nicht vor ca. 10:15"** und hat ab Mittag null Volumen-Selektivität. Konsequenz: die **175 maband-Jobs mit RVOL-Achse (47 gerechnet) haben RVOL nie getestet**, und die **195 maband-Survivors mit aktivem RVOL-Gate** sind sehr wahrscheinlich von einem Uhrzeit-Filter getragen. `tsmom.py:251` macht es richtig (Zähler- und Nennerfenster identisch) — und dort trägt **0 von 1.673 Survivors** ein RVOL-Gate. Über alle Läufe: **0 von 38 Kandidaten** trägt je ein aktives RVOL-Gate.
>
> **Das ist eine Ticket-Empfehlung (MS-A), kein Urteil und kein Fix.** Der `verdict-auditor` entscheidet, ob daraus ein Stempel wird.

> [!info] Befund B — RVOL-Gates existieren überall, nur nicht im Buch
> `tm_rvol_min`/`tm_rvol_max` werden ausschließlich in `sigcore.gates_pass` ausgewertet, und die wird nur von `tsmom` und `maband` gerufen. Die drei Buch-Beine (`ts_reversal`, `last_hour`, `asian`) und `vwap_pullback` kennen **kein** RVOL-Gate — obwohl sie seit AP157 alle den Null-Schalter `tm_null` auswerten (`discovery/controls.py:667`). Genau die Falle, an der **MS-61** gescheitert ist (falscher Engine-Pfad) und die [[Strategie-Logbuch]]-Zeile 2596 beschreibt. Jeder Weg, der ein Buch-Bein gaten will, braucht deshalb **MS-B**, nicht einen Job.

---

## Die sieben harten Randbedingungen

**1. Vorzeichenlos gemessenes RVOL ist tot.** #068 und #125 haben beide RVOL *ohne* Flow-Vorzeichen getestet. Chan/Fong (2000, [[Research-Cache]]) zeigen, dass das Order-Imbalance-**Vorzeichen** der Treiber ist und rohes Volumen seine Erklärungskraft verliert, sobald man kontrolliert. Jeder Weg, der weiterhin unsigniertes RVOL als Richtungssignal behauptet, bekommt kein Skelett.

**2. #031/#044 ist kein Positivbefund.** Look-ahead, entlarvt in #067. Nicht zitieren, nicht aufwärmen.

**3. RVOL-Gates erreichen die Buch-Beine heute nicht** (Befund B). Kein Job ohne MS-B.

**4. Der maband-Pfad ist als Evidenzquelle gesperrt**, bis MS-A gelaufen ist (Befund A).

**5. E8 erlaubt kein Overnight, flat vor Close** (Randbedingung 1 der [[Hypothesen-Bank (Pairs Trading & Relative Value)]]). Alle Swing-Wege inklusive des Cartea-Overnight-Kanals sind damit **Live-Buch-Merker**, kein Prop-Buch-Job. Sie stehen trotzdem hier — Regel Max: nichts, was je eine Edge zeigte, geht verloren.

**6. Kostenschwelle rund 2 Punkte MNQ-Round-Trip.** Alles, was die Trade-Zahl erhöht, muss diese Hürde je Trade schlagen. Wege, die Trades *wegnehmen* (W23), müssen das nicht — das ist ihr struktureller Vorteil.

**7. Long und Short werden nur bei gerichteten Entries getrennt.** Filter-, Sizing- und Exit-Wege sind richtungslos und bekommen keine L/S-Spaltung. Das ist keine Sparmaßnahme, sondern verhindert, dass die Liste durch Reparametrisierung länger aussieht als sie ist.

---

## Wege-Tabelle, familienweise (40 Wege)

Stand: `tot` · `scheingemessen` · `gemessen ohne Kandidat` · `offen` · `keine Story`.

### A. Trend Following — Continuation-Kanal

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| W1 | Preis läuft mit hohem RVOL weiter, long | Signal | **tot** (#125, #068) | tsmom ✅ | VV-01 | — |
| W2 | dito, short | Signal | **tot** (#125, #068) | tsmom ✅ | VV-01 | — |
| W3 | Level-Bruch MIT hohem RVOL | Signal | **tot** (#068, `or_rvol_min`) | qbt orb ✅ | VV-01 | — |
| W4 | Level-Bruch bei NIEDRIGEM RVOL | Signal | offen | `or_rvol_max` fehlt | VV-18 | neues Bein |
| W5 | RVOL steigt während der Bewegung | Signal | offen | Modul-Spec | VV-11 | neues Bein |
| W6 | RVOL-Plateau über viele Bars | Filter | offen | Modul-Spec | VV-06, MO-03 | neues Bein |
| W7 | RVOL fällt, während der Preis läuft → aussteigen | Exit | offen | MS-E | VV-12/50/56 | Overlay |
| W8 | RVOL-Gate auf maband-Signalen | Filter | **scheingemessen** (Befund A) | maband, defekt | — | — |
| **W9** | Hohes RVOL **UND** gleichgerichtetes Delta, long | Signal | **offen**, kontaminiert | tsmom ✅ | MO-46 | Ersatz `NQ_Momentum_d260818` |
| **W10** | dito, short | Signal | **offen**, Verwandter tot (#098/#099) | tsmom ✅ | MO-46 | Kontrollarm zu W9 |

### B. Mean Reversion — Exhaustion-Kanal

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| W11 | Umkehr nach RVOL-Spike (Climax) | Signal | **gemessen ohne Kandidat, unterpowert** (`hyp_CR01_ES` n=61, edge −16,4 pp) | tsmom ✅ | VV-03, MO-21 | kein neuer Grund → kein Skelett |
| **W12** | Fade bei RVOL-Trockenheit, long | Signal | **offen** | tsmom ✅ `tm_rvol_max` | VV-04, VV-40 | Ersatz `NQ_Momentum_d260818` |
| **W13** | dito, short | Signal | **offen** | tsmom ✅ | VV-04 | Ersatz `NQ_Momentum_d260818` |
| W14 | Spike, dann sofortige Trockenheit (Stop-Run) | Signal | offen | Modul-Spec | VV-36 | neues Bein |
| W15 | Absorption: RVOL hoch, Fortschritt klein (λ) | Filter | teilgemessen (#068), λ-Feature offen | Modul-Spec | VV-17, MO-23..26 | neues Bein |
| W16 | VWAP-Rückkehr verstärkt bei steigendem RVOL | Filter | offen | MS-B (`vwap_pullback`) | VV-55, MO-40 | neues Bein |
| W17 | Gap-Fill bei niedrigem Open-RVOL | Filter | offen | MS-B (`ts_reversal`) | VV-48/49, MO-20/33 | Ersatz `NQ_Momentum_d260818` |

### C. Intraday Bias — Tagestyp-Kanal

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W18** | Früh-RVOL skaliert Stop/Sizing statt Entry | Exit/Sizing | **offen** | MS-E | VV-51, VV-56 | Overlay, alle 3 Beine |
| W19 | Front-load vs. Back-load des Volumenprofils | Filter | offen | Modul-Spec | VV-39, MO-07/08/49 | neues Bein |
| **W20** | RVOL der Schlussstunde gatet LastHour | Filter | **gemessen ohne Kandidat** (TS-21: 288 Configs, 1 Survivor, 0 Kandidaten) | MS-B | VV-21, VV-46 | Ersatz `NQ_LastHour_v3` |
| **W21** | Asien-/Globex-RVOL gatet das Asia-Bein | Filter | **offen** | MS-B (24h-Daten da) | VV-19/20, XA-42 | Ersatz `NQ_Asia-Dir-USopen_d260820` |
| W22 | Nachhol-Volumen nach FOMC/CPI | Filter | offen | MS-B (`fomc`) | VV-25/26 | neues Bein |
| **W23** | Niedrig-RVOL-Tage: **Beine abschalten** | Filter/Zeitfenster | **offen** | MS-B | VV-34, VV-45 | Overlay, alle 3 Beine |
| W24 | 09:30-Minute aus der Normierung nehmen | — | **keine eigene Story** — Reparametrisierung von W18/W23 | — | VV-46/47 | — |
| W25 | Roll-Woche verzerrt RVOL | Kontrolle | offen, Pflichtkontrolle zu W18/W21/W23 | `calendar` ✅ | VV-22, MO-36 | — |

### D. Swing — Mehrtages-Kanal *(war leer, aufgefüllt)*

Alle mit `swing: true`. **Kein Prop-Buch-Job** (Randbedingung 5), sondern Live-Buch-Merker.

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W26** | RVOL-Persistenz über mehrere Tage | Filter | offen | MS-C | VV-30, MO-11/12/13 | Live-Buch-Merker |
| **W27** | RVOL am Tag eines News-/Levelbruchs bestätigt mehrtägiges Pullback-Setup | Level | **offen, keine Bank-Zeile** (Max 21.09.) | MS-C + Level-Register | — | Live-Buch-Merker |
| **W28** | RTH-RVOL-Extrem → nächste **Overnight**-Bewegung (Cartea) | Signal | **offen, keine Bank-Zeile** (Max 21.09.) | MS-C + `asian drift` | — | Live-Buch-Merker |
| W29 | Mehrtägig erhöhtes Profil nach Vola-Schock | Filter | offen | `vix_bias` + MS-C | VV-59, XA-45 | Live-Buch-Merker |
| W30 | Monatsende-/Rebalancing-RVOL | Filter | offen | `calendar` + MS-C | MO-34/35, XA-52 | Live-Buch-Merker |

### E. Relative Value — Cross-Instrument-Kanal *(war dünn, aufgefüllt)*

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W31** | NQ **und** ES gleichzeitig hohes RVOL (Korb-Flow) | Filter | **offen** | MS-F | VV-41, XA-03 | Ersatz `NQ_Momentum_d260818` |
| W32 | RVOL-Ratio NQ/ES im Extrem → Spread | Signal | offen, **Kosten doppelt** | `rv` + MS-F | VV-42, XA-12/13 | neues Bein |
| W33 | RVOL-Breadth über alle vier Indizes | Filter | offen | MS-F | XA-03, XA-50 | Overlay |
| W34 | Ein Index bewegt sich OHNE Volumen, die anderen mit | Signal | offen | MS-F | XA-09, VV-54 | neues Bein |
| W35 | YM-/RTY-RVOL als Signal, gehandelt wird NQ | Signal | offen | `rv leadlag` + MS-F | VV-43/44, XA-07/08 | neues Bein |

### F. Kontroll-/Mess-Weg

| Weg | Bewegung | Rolle | Stand | Engine-Weg | Bank | Buch-Bezug |
|---|---|---|---|---|---|---|
| **W36** | Ist RVOL nur ein Vola-Proxy? Residual-RVOL gegen realisierte Vola | Filter | **offen** | MS-D (Prescan) | VV-27, VV-60 | kein Bein, entscheidet W9/W10/W12/W13 |

### G. Wege ohne Story (Vollständigkeits-Nachweis)

| Weg | Bewegung | Warum keine Story |
|---|---|---|
| W37 | „Preis prallt am RVOL ab" | keine Story, weil RVOL kein Preis-Level ist — es gibt keine Geometrie zum Abprallen. Kategorienfehler. |
| W38 | „Preis läuft am RVOL entlang" | keine Story, gleicher Kategorienfehler. Die einzige sinnvolle Lesart ist W6. |
| W39 | „RVOL-Fenster kreuzt RVOL-Fenster" | keine eigene Story — deckungsgleich mit W5. Als eigener Weg gezählt wäre es Reparametrisierung. |
| W40 | „RVOL kreuzt die Erwartungskurve und hält" | keine eigene Story — das ist W19 in anderer Formulierung. |

---

## Familien-Versorgung (Max' Kernfrage)

| Familie | Wege | offen | Skelette | Befund |
|---|---|---|---|---|
| Trend Following | 10 | 6 | 2 | **Der Kern ist abgeräumt** (W1-W3 tot). Übrig bleibt nur der vorzeichen-kontrollierte Rest plus Struktur-Features. Nicht unterversorgt, sondern erledigt. |
| Mean Reversion | 7 | 6 | 2 | Gut gefüllt, aber nur W12/W13 sind heute ohne Modulbau testbar. |
| Intraday Bias | 8 | 6 | 3 | **Beste Familie** und die einzige mit drei Wegen, die ein bestehendes Bein ersetzen oder overlayen statt ein neues zu bauen. Hängt komplett an MS-B. |
| Swing | 5 | 5 | 3 | War leer, aufgefüllt — inkl. Max' zwei Vorgaben (W27, W28). Alle nur Live-Buch. |
| Relative Value | 5 | 5 | 1 | War dünn, aufgefüllt. Alles hängt an MS-F, W32 zusätzlich an doppelten Kosten. |

> [!important] Unterversorgt ist keine Familie, sondern eine **Rolle**
> RVOL wurde bei uns fast ausschließlich als **Signal** getestet — und ist dort zweimal ehrlich tot. Die Rollen **Filter auf einem bestehenden Bein**, **Sizing** und **Zeitfenster** sind praktisch unberührt. Genau diese Rollen brauchen keine Richtungsprognose aus Volumen (sind also von #068/#125 gar nicht getroffen) und wirken direkt auf das Zielmaß. Das ist die eigentliche Lücke dieses Kapitels.
>
> Seit dem Kriteriumswechsel vom 21.09. ist **Sizing** die stärkste dieser drei Rollen: RVOL ordnet nachweislich die Streuung (Faktor 2,54 in der Varianz über die Dezile), und Größe darf jetzt gerechnet werden statt bei 1 Kontrakt festzustehen.

---

## Reihenfolge nach Buch-Chance

Kriterien: Ersatz vor neu (#139 B3) · engine-fähig vor Modul-Spec · ohne tote Verwandte vor kontaminiert · HF vor LF · Zufallsdecke bei 65.035 Trials · **seit 21.09. zusätzlich: Wirkung auf E[Zeit bis 50.000 $], nicht auf Passquote allein.**

**Stand nach dem `strategy-auditor`-Batch vom 21.09. und dem Kriteriumswechsel** (alte Reihenfolge in Klammern):

| Rang | ID | Weg | Warum hier |
|---|---|---|---|
| 1 (1) | RVOL-**W36+** | Residual-Prescan **mit Delta-Vorzeichen-Achse** (mit / gegen / ohne) | Umbau auf Vorschlag `strategy-auditor`: der ursprüngliche W36 misst vorzeichenlos und kann damit W09/W10 **gar nicht entscheiden**, obwohl er das beansprucht. Mit der Achse beantwortet ein Job (16 × 3 Zellen) alle drei Fragen inklusive der Climax-Umkehr — statt 160 Configs, die alle gegen die Zufallsdecke zählen. Negativ = Kapitel sauber geschlossen. **Blocker: MS-D erfüllt den AP153-Prescan-Vertrag noch nicht** (Vorlage `_scratch_volshock/falsify.py` ist vom 21.08., kennt `prescan_controls` nicht, schreibt `.txt`). |
| 2 (8) | RVOL-W18 | Früh-RVOL steuert **Sizing** | **Größter Gewinner des Kriteriumswechsels.** RVOL ordnet die Streuung nachweislich (Faktor 2,54 in der Varianz), und mit gerechneter Größe ist `f_i ∝ mu_i / sigma_i²` anfahrbar statt nur als Gate approximierbar. Obergrenze +5,5 % theta (Cauchy-Schwarz). Kostet MS-E. |
| 3 (5) | RVOL-W21 | Asia-RVOL gatet das Asia-Bein | **Einziger Weg mit grünem Licht** vom `strategy-auditor`: echter Bein-Ersatz für `NQ_Asia-Dir-USopen_d260820` statt Neubau, Gate schließt 03:00 ET und Entry liegt am US-Open, strukturell also kein Look-ahead-Fenster. Kürzeste Strecke zum Buch. Auflagen: Why von Entwurf auf belegt, DST-/Tagesgrenzen-Zusicherung für das 19:00-03:00-Fenster. |
| 4 (2) | RVOL-W09 | RVOL × Delta, **long** | **Baustopp für Runde 1.** Nicht wegen der Kontamination, sondern weil niemand die nötige **Effektgröße** aufgeschrieben hat: die Konjunktion müsste um Faktor 4,5 verstärken, während beide Haupteffekte bei ~null liegen. `hypothesis_bank.py:307` lässt ihn ohne bestandenen Prescan-Vertrag ohnehin nicht in die Bank — ein Enqueue jetzt hieße Prior schönen. Wartet auf Rang 1. |
| 5 (3) | RVOL-W10 | RVOL × Delta, **short** | Kontrollarm zu Rang 4, also ebenfalls Baustopp. `strategy-auditor`: „Kontrollarm zu einem Arm, der nicht gerechnet wird, ist kein Kontrollarm, sondern 72 zusätzliche Trials gegen die Zufallsdecke." Der bessere Mechanismus-Kontrast ist ohnehin das Umdrehen der **Delta-Bedingung** bei gleicher Handelsrichtung — das steckt jetzt in W36+. |
| 6 (4) | RVOL-W23 | Abschalt-Gate an dünnen Tagen | **Abgestuft.** Ist die grobe Krücke für das Problem, das W18 sauber löst. Zwei Auflagen des `strategy-auditor`: (a) der Why behauptet eine Risiko-Asymmetrie, die der Mechanismus nicht hergibt — gültig ist nur, dass die ~2 Punkte Kosten in Punkten **fix** sind und nicht mit der Range schrumpfen; (b) **E8-Inaktivitätsregel**: mind. eine Position pro Woche auf und zu, sonst Kontoschließung. Ein Gate auf allen drei Beinen kann Wochen ohne Trade erzeugen = Totalverlust der Eval-Gebühr. Braucht Pflicht-Kennzahl „max. Kalendertage ohne Trade" und einen Notausgang. |
| 7-8 | RVOL-W13 / W12 | Fade bei Trockenheit, short/long | Engine-fähig, Why nur Entwurf. **Korrektur `verdict-auditor`:** das Urteil „Fade erledigt" trägt NICHT (p = 0,50 bei n = 61 ist Nicht-Wissen, nicht Abwesenheit). Bleiben offen. |
| 9 | RVOL-W31 | Gemeinsames NQ/ES-Gate | Braucht MS-F zusätzlich, Why nur Entwurf. |
| 10 | RVOL-W20 | LastHour-Gate | **Kontaminiert** (TS-21: 288 Configs, 0 Kandidaten). Braucht vorher eine Antwort, was TS-21 wirklich ausgeschlossen hat. |
| 11-13 | RVOL-W27 / W28 / W26 | Swing | Kein Prop-Buch-Job (E8-Overnight-Verbot). Live-Buch-Merker, siehe Overnight-Abschnitt. |

**Erste Rechenrunde: Rang 1 allein, danach Rang 2 und 3.** Rang 4-13 warten auf das Ergebnis von Rang 1, sonst hebt die Zufallsdecke für alle. Vor jedem Modulbau gilt die offene Auflösungsfrage: `book_contribution()` hatte laut #125/AP112 ein Rauschmaß, das 3-5x überschätzt war — liegt die gepaarte Seed-Streuung bei ~1 pp, baut man 70-90 Zeilen für etwas unter der Rauschgrenze.

> [!todo] Auflage `verdict-auditor`: fünfte Stand-Kategorie fehlt
> Die Karte kennt `im Buch` / `tot` / `scheingemessen` / `gemessen ohne Kandidat`. Es fehlt **„nicht entscheidbar (Power/Feasibility)"**. Der `quant-statistician` hat gezeigt, dass mehrere „offene" Wege (u.a. W15/Absorption) 12- bis 40-fache Historie bräuchten — ein Job darauf kommt **garantiert leer** zurück und hebt trotzdem die Decke für alle anderen. Alle 25 „offen"-Wege einmal gegen `overfit.feasibility_gate()` laufen lassen, **bevor** Rang 1-3 eingereiht wird. Kostet Minuten, streicht vermutlich einen Großteil.

---

## Kontaminationswarnung zu W9/W10

Der Delta-Kanal ist bei uns **mehrfach gescheitert**:

- **#138 (31.08.2026):** Richtung via Delta = Münzwurf (0,46/0,49), Rest-Uplift war Bin-Artefakt (Zufalls-Bucket-Placebo lieferte MEHR als das Signal). Killt **VV-29** und **VV-57**.
- **POC-Messung:** Delta-Terzile flach (0,48/0,48/0,49); Delta als Breakout-Bestätigung machte es *schlechter*.
- **#098/#099 (16.08.2026):** Delta schlug genau einmal eine Preis-Bedingung (R1-Ersetzung, OOS-Drift +0,081 → +0,171 ATR) — aber **„Short bleibt in JEDER Delta-Variante unter Münzwurf"**, die Richtungsregel war strukturell long-only.

**Gleich ist** die Variable (Delta-Proxy aus OHLCV). **Anders ist** die Konstruktion: dort war Delta ein alleinstehender Richtungsgeber bzw. eine Bestätigung auf einem Preis-Trigger, hier ist die THESE die **Konjunktion** aus hohem RVOL UND gleichgerichtetem Delta — und die war in keinem Job je die Prämisse (TS-21 führte beide nur als *alternative* Prämissen-Arme, nie als UND).

**Konsequenz:** zeigt die Konjunktion keinen Zusatznutzen gegen die Delta-Einzelzelle, ist der Weg tot und wird **nicht** umformuliert.

---

## Modul-Specs

| ID | Was fehlt | Wo | Umfang | Blockiert |
|---|---|---|---|---|
| **MS-A** | **Fix**, kein Feature: Referenzfenster an das Zählerfenster koppeln | `maband.py:528` vs. `:623` | ~10 Zeilen + Golden-Master + Neubewertung der 47 gerechneten Jobs | W8 und jede maband-RVOL-Aussage |
| **MS-B** | `sigcore.rvol_confirm(p, d, entry_min)` nach dem Muster `sigcore.xref_confirm` (`sigcore.py:739`), verdrahtet in `qbt._reversal_trades`, `qbt._last_hour_trades`, `asian.trades`, `vwap_pullback.trades`. Default AUS (bitgleich), `entry_min` Pflicht gegen Look-ahead | sigcore + 4 Aufrufstellen | ~70-90 Zeilen | W16, W17, W20, W21, W22, W23 |
| **MS-C** | `daily_context` um `rvol_day = v / vol_med20` (`vol_med20` existiert, `sigcore.py:684`) + **harte Sperre**: nur für Entries nach dem RTH-Close des Messtags | sigcore | ~15 Zeilen + Guard | W26-W30 |
| **MS-D** | Residual-RVOL-Prescan nach dem Muster `_scratch_volshock/falsify.py` (#125) | eigenständig | ~80-120 Zeilen | W36 |
| **MS-E** | RVOL-abhängige Stop-/Size-Skalierung + Pflicht-Kontrollarm mit konstantem Multiplikator gleicher mittlerer Stop-Weite | sigcore + tsmom/maband | ~30 Zeilen | W7, W18 |
| **MS-F** | Cross-Symbol-RVOL im `xref_confirm`-Muster | sigcore + Aufrufstellen | ~40 Zeilen, setzt MS-B voraus | W31-W35 |

Kein Weg schlägt einen neuen `mode` vor. Alles ist Erweiterung von `sigcore`/`tsmom`/`maband` bzw. Verdrahtung in die vier Modi, die seit AP157 schon `tm_null` auswerten — der Null-Schalter ist damit für jeden Weg vorhanden.

---

## Offene Research-Fragen

1. Überträgt sich Chan/Fong (Vorzeichen schlägt rohes Volumen) von Aktien-Tagesdaten auf Index-Futures-Intraday? (W9/W10)
2. Gibt es Evidenz für den Overnight-Kanal (Cartea et al. 2025) in Index-Futures, wo es keinen Auktionsschluss und fast durchgehenden Handel gibt? (W28)
3. Skaliert die Prognosekraft einer Overnight-Session-Richtung mit der Session-Beteiligung? (W21)
4. Regression Tagesrange ~ Früh-RVOL auf NQ: wie stark, wie regime-stabil? (W18)
5. Identifiziert gleichzeitiges abnormales Volumen über mehrere Index-Futures Korb-Flow, oder nur einen gemeinsamen Vola-Faktor? (W31)
6. Wirken volumen-gewichtete Levels stärker als reine Preis-Levels? Unsere eigene Level-Beweislage (#149/#138) spricht klar dagegen. (W27)
7. Wie viel der Tages-Volumen-Autokorrelation ist Vola-Clustering statt Metaorder-Spur? (W26)
8. Was unterscheidet die eine Delta-Erfolgsmessung (#099) von den drei Delta-Fehlschlägen (#138, POC, TS-21)? (W9)

---

## Nächste Schritte

**Erledigt am 21.09.2026 (abends):**

- ✅ **MS-A / Ticket AP206** angelegt UND umgesetzt. `sigcore.cum_vol_median()` neu, `maband.py` nutzt jetzt einen kumulativen Nenner passend zum Zähler. Gegenprobe NQ: Durchlassquote von `tm_rvol_min=1.2` vorher 0,62 % @15min bis 97,43 % @240min (Spannweite 96,8 pp), jetzt 29,51 % bis 23,68 % (6,3 pp); bei Minute 30 alt = neu = 26,21 %, weil dort beide Nenner zusammenfallen. `engine-regression-tester` unabhängig nachgerechnet: **alle sechs Buch-/Live-Beine 0 Delta**, tsmom bitgleich, maband ohne RVOL-Gate bitgleich, beide Kanarien unverändert. Box-Sync + Runner-Neustart am selben Abend.
- ✅ **Schritt 2 des EINEN Wegs gelaufen:** `variant-scout` über Rang 1-5 (W36=16, W09=72, W10=72, W23=12, W21=12 echte Testarten), danach EIN `strategy-auditor`-Batch-Call über alle Whys. Ergebnis ist in die Reihenfolge oben eingearbeitet.
- ✅ **`research-scout`** auf die E8-Overnight-Regelfrage (Ergebnis: verboten, Zwangsschließung 15:10 CT, Wochenende mit verboten — W27/W28 damit endgültig Live-Buch-only) und auf die externe RVOL-Beleglage (neuer Abschnitt im [[Research-Cache]]).
- ✅ **`verdict-auditor`** über alle Urteile, **`pipeline-auditor`** über die `theta_gate`-Kalibrierung (Ergebnis: Gate läuft im Schattenmodus und filtert nichts, keine Rückwirkung; die geschlossene Formel ist ~25 % zu optimistisch, die verdrahtete Konstante 28,1 vermutlich richtig).

**Offen:**

1. **MS-D auf den AP153-Prescan-Vertrag heben**, dann Rang 1 (W36+ mit Delta-Achse) bauen. Ohne bestandenen Vertrag wirft `hypothesis_bank._check_prescan_ref` hart, und Rang 4/5 bleiben ohnehin gesperrt.
2. **Feasibility-Vorfilter** über alle 25 „offen"-Wege (siehe Auflage oben), bevor irgendetwas eingereiht wird.
3. **Rauschgrenze klären** (gepaarte Seed-Streuung von `book_contribution()`), bevor MS-B oder MS-E gebaut wird — sonst baut man 70-90 Zeilen für einen Effekt unter der Messschwelle.
4. Erst danach `pipeline-auditor` + `--enqueue`. Queue ist seit 20.09. leer, Kapazität ist also da — das ist kein Grund, die Reihenfolge zu überspringen.
5. **Golden-Master-Fall für maband mit `tm_rvol`** anlegen (AP206 Schritt 7). Es gibt bis heute keinen — deshalb blieb der Fensterfehler unbemerkt.

> [!info] Wiedervorlage 08/2027 aus #125 — vom `verdict-auditor` nachgetragen
> #125 enthält eine ausdrückliche Wiedervorlage, die in der ersten Fassung dieser Karte fehlte: *„Einzige positive Zelle: OOS ≥ 2023-09, n = 396/153, mean +17/+24 Punkte, t 3,2/2,7 … falls der 2023+-Effekt in einem Jahr noch steht, Thema neu öffnen."* Ohne diese Zeile gilt #125 einer späteren Session als restlos geschlossen.
>
> Gegenstimme des `quant-statistician`, die gleich mit dazu gehört: genau diese Zelle ist Tail-Lotterie — die Top-5 Tage tragen 75,5 % des Ertrags, und aus ~60 berichteten Zellen ausgewählt liegt der Fund mitten in dem, was Zufall bei dieser Selektionsbreite ohnehin produziert (E[max] 4,9-6,2 Pkt). Geschrumpfte Edge ≈ 0. **Die Wiedervorlage steht also, aber mit dieser Warnung im selben Atemzug.**

---

## Verwandte Notizen

[[Alpha-Suche]] · [[Discovery-Runner v2]] · [[Strategie-Logbuch]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Research-Cache]] · [[Strategie-Familien]] · [[Eval-Passing]] · [[Buch-Workflow]] · [[VWAP-Offensive]] · [[Rundzahlen Wege-Karte]] · [[Fibonacci Wege-Karte]] · [[Session Momentum Wege-Karte]] · [[ES-NQ-Divergenz Wege-Karte]] · [[Familien-Scout Agent]]
