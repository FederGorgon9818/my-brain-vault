---
tags: [projekt, agent, alpha-suche]
erstellt: 2026-09-10
aktualisiert: 2026-09-11
status: gebaut, Abnahmetest offen
ziel: Ein Konzept/eine vermutete Edge automatisch in alle handelbaren Wege zerlegen und je Weg eine testfertige Hypothese liefern
---

# Familien-Scout Agent

**Auftrag Max, 10.09.2026:** ein Agent, der eine voraussichtliche Edge in alle testbaren Familien unterteilt, und zwar Familie im Sinne von konkreten Preis-Wegen innerhalb des Konzepts (VWAP raus zum Band, vom Band zurück, durch das Band), nicht im Sinne der fünf groben Strategie-Familien, daraus Hypothesen baut, die dann `research-scout`, `variant-scout` und die übrigen Prüf-Agents durchgehen, damit jede einzelne Familie des Konzepts ausführlich getestet wird.

**Entscheidungen Max, 11.09.2026** (die vier offenen Punkte vom 10.09.):
1. Name: **`familien-scout`** (statt „edge-mapper").
2. Der Scout **schreibt die Vault-Projekt-Karte selbst** (`Projekte/<Konzept> Wege-Karte.md`), nicht nur den Report.
3. Swing-Wege werden **mitgeführt und markiert** (Live-Buch-Merker, kein Prop-Buch-Job).
4. Workflow **`konzept-weg` gleich mitgebaut**, nicht erst nach zwei Handläufen.
5. Dazu Max' Hinweis: der `verdict-auditor` („der am Ende drüberschaut, ob was vergessen wurde") gehört direkt hinter den Scout, nicht nur ganz ans Ende. Eingebaut als Vollständigkeits-Check mit Nachtrag-Schleife.

**Gebaut am 11.09.2026 (Box-Session):**
- `.claude/agents/familien-scout.md` (opus; Read, Grep, Glob, Bash, Write)
- `.claude/workflows/konzept-weg.js` (Aufruf: Workflow-Tool mit `name: "konzept-weg"`)
- Einschalt-Satz in der CLAUDE.md, Roster-Zeile; Hub-Roster (`hub_config.json`, PC aus) als Ticket AP149

**Noch offen:** Abnahmetest 1 (VWAP gegen die Hand-Karte [[VWAP-Offensive]]) und Abnahmetest 2 (Fibonacci) laufen erst, wenn Max es sagt. Hub-Roster nachtragen, sobald der PC an ist (AP149).

**Vorbild aus dem Handbetrieb:** [[VWAP-Offensive]] (10.09.2026). Dort wurde „VWAP" von Hand in zwölf Zellen V1 bis V12 zerlegt (Lage, Distanz, Annäherung, Kreuzung, Anker, Band, Steigung, Exit, Differenzen, Overlay, Volumenprofil, Kontrolle), je Zelle mit Story, Register-Stand, Buch-Bezug und Reihenfolge nach Buch-Chance. Der Familien-Scout macht genau das für jedes Konzept, reproduzierbar und gegen Register/Logbuch/Engine geprüft statt aus dem Kopf.

---

## 1. Platz in der Kette (= Workflow `konzept-weg`)

```
Konzept  (Max, research-scout-Fund, alpha-scout-Idee)
   |
   v
familien-scout     Breite: Konzept -> Elemente -> Wege (x Richtung) -> Skelette mit Why-Entwurf
   |                schreibt Karte + Report + Hypothesen-JSON
   v
verdict-auditor    Vollstaendigkeit: fehlt ein Weg? stimmt ein Stand? toter Verwandter uebersehen?
   |                bei Luecken: familien-scout traegt nach (eine Runde)
   v
research-scout     EIN Call je Konzept: alle Research-Fragen, Cache zuerst -> Whys belegt/widerlegt/offen
   |                widerlegte Skelette und Swing-Wege gehen nicht weiter
   v
ein-weg (Workflow) Tiefe: variant-scout je Hypothese, dann strategy-auditor Batch
   |
   v
Hauptsession       Karte gegen Hand-Karte abgleichen, H()-Zeilen, pipeline-auditor (pipeline_ok), Enqueue + Push
   |
   v
Box rechnet -> verdict-auditor stempelt je Weg -> Stand wandert in die Karte zurueck
```

**Abgrenzung zu den Nachbarn (damit nichts doppelt läuft):**

| Agent | Frage | Einheit |
|---|---|---|
| `alpha-scout` | Was testen wir überhaupt als Nächstes? | viele Mechanismen, gerankt |
| **`familien-scout`** | **Welche Wege gibt es in DIESEM Konzept, und welche sind offen?** | **ein Konzept, alle Wege** |
| `verdict-auditor` | Ist die Karte vollständig, trägt jeder Stand? Später: Stempel je Weg | eine Karte |
| `variant-scout` | In wie vielen echten Implementierungen lässt sich DIESE Hypothese bauen? | eine Hypothese, alle Achsen |
| `research-scout` | Was sagt die Literatur/der Markt dazu? | Belege, Cache-Pflicht |

Kurz: der Scout ist Breite, `variant-scout` ist Tiefe. Der Scout endet dort, wo eine Hypothese mit Why steht. Ab da gilt „Der EINE Weg" (CLAUDE.md, 23.08.2026) unverändert.

---

## 2. Die Wege-Matrix (der Kern)

**Präzisierung Max, 10.09.2026:** „Familie" heißt hier NICHT Mean Reversion / Momentum / Intraday Bias. Gemeint sind die konkreten **Wege**, die der Preis innerhalb des Konzepts nehmen kann. Bei VWAP plus Bollinger-Band: vom VWAP raus zum Band, vom Band zurück zum VWAP, durch das Band hindurch, am Band abprallen, VWAP kreuzen und halten. Jeder Weg ist eine eigene Familie und wird für sich komplett durchgetestet. Die fünf [[Strategie-Familien]] sind nur noch ein Etikett, das jeder Weg hinten dranbekommt.

**So entstehen die Wege, in drei Schritten:**

1. **Elemente des Konzepts auflisten.** Alles, was das Konzept an Linien, Zonen und Zuständen mitbringt. VWAP: die VWAP-Linie selbst, ihre Bänder (1σ/2σ oder Bollinger auf der VWAP), ihre Steigung, die Bandbreite, ein zweiter Anker (Wochen-/Session-VWAP), das Volumen dahinter. Dazu immer der Preis.
2. **Beziehungen zwischen den Elementen aufzählen.** Für jedes Paar (Preis ↔ Linie, Preis ↔ Band, Linie ↔ Anker, Band ↔ Band) die möglichen Bewegungen: **hin zu**, **weg von**, **durch hindurch**, **abprallen an**, **entlanglaufen an**, **kreuzen und halten**, **kreuzen und scheitern**. Für Zustände (Steigung, Breite): **steigt / fällt / flach**, **eng / weit / wechselt**.
3. **Jede Bewegung × Richtung = ein Weg.** Long und Short getrennt, weil sie oft nicht symmetrisch sind (Long-Bias #108). Dazu die Frage, an welchem Punkt des Wegs eingestiegen wird (früh, bei Bestätigung, spät).

**Was je Weg eingetragen wird:**

- **Beschreibung des Wegs** in einem Satz („Preis liegt am VWAP und läuft zum oberen Band")
- **Story:** wer muss handeln, warum, warum bleibt das Geld liegen (Why-Entwurf)
- **Stand:** `im Buch` / `tot (Logbuch #)` / `gemessen ohne Kandidat (n Trials)` / `offen`
- **Rolle** des Konzepts in diesem Weg: Signal, Filter, Level, Exit oder Zeitfenster
- **Etikett:** eine der fünf Strategie-Familien, nur zur Einordnung im Report
- **Engine-Weg:** `maband`/`tsmom`-Achse vorhanden (sofort testbar) oder Modul-Spec nötig (welcher `mb_kind`/`tm_signal`). Alles außerhalb von `maband`/`tsmom` hat keinen Null-Schalter und kann nie `deploy_ready` werden (VWAP-Offensive, Randbedingung 1). Der Scout schlägt deshalb nie einen neuen `mode` vor, sondern eine Erweiterung der bestehenden Module.
- **Buch-Bezug:** Ersatz für welches Bein oder neues Bein. Ersatz schlägt neu (#139 B3).
- **Verwandte Tote:** IDs aus Logbuch/Bank/Register, Kontaminationswarnung wie bei `variant-scout`
- **Research-Frage:** was `research-scout` belegen soll, falls das Why noch schwach ist
- **Swing-Markierung:** Wege mit Tages-/Mehrtages-Horizont bleiben in der Karte (`swing: true`, Live-Buch-Merker), bekommen aber keinen Prop-Buch-Job.

**Beispiel VWAP + Bänder, wie die Wege-Liste aussieht:**

| Weg | Bewegung | Etikett | Stand (10.09.) |
|---|---|---|---|
| W1 | Preis am VWAP, läuft raus zum Band (Expansion) | Trend | offen |
| W2 | Preis am Band, kehrt zurück zum VWAP (Rückkehr zur Mitte) | Mean Reversion | Fade tot (#211/#097), braucht neuen Grund |
| W3 | Preis bricht durch das Band und läuft weiter (Band-Walk) | Trend | offen |
| W4 | Preis prallt am Band ab (Bounce) | Mean Reversion | mit W2 verwandt, tot-kontaminiert |
| W5 | Preis kreuzt VWAP von unten nach oben und hält (Kontrollwechsel) | Trend | `reclaim` gemessen, 27 Trials ohne Kandidat |
| W6 | Preis kommt zum VWAP zurück, hält ihn, läuft weiter (Pullback) | Trend | im Buch (`NQ_VWAP-Pullback`), Ersatz-Slot |
| W7 | Preis fällt durch den VWAP und scheitert beim Retest von unten | Trend | offen |
| W8 | Bänder eng, dann Ausbruch (Squeeze) | Trend | offen, Modul-Frage Bandbreite |
| W9 | Bänder weit, Kontraktion beginnt | Mean Reversion | offen, schwaches Why |
| W10 | VWAP steigt/fällt (nur als Filter für andere Wege) | Filter | offen (V7 in VWAP-Offensive) |
| W11 | Tages-VWAP nähert sich dem Wochen-VWAP / entfernt sich | Relative Value | offen (V5/V9) |
| W12 | Preis läuft am Band entlang ohne Rückkehr (Trend-Tag) | Intraday Bias | offen, eher Filter als Signal |

Jeder Weg bekommt zwei Richtungen und drei Einstiegspunkte, das ist die Vorlage, die `variant-scout` danach in Achsen (Fenster, Bestätigung, Stop, Exit, Markt) aufdröselt. Das Beispiel ist die Übersetzung von V1 bis V12 aus [[VWAP-Offensive]] in Wege; die Zuordnung dort bleibt die Quelle für die Stände.

**Vollständigkeits-Regel:** der Scout geht die Beziehungs-Liste aus Schritt 2 mechanisch durch. Ein Weg, der keine Story hat, steht trotzdem in der Tabelle mit „keine Story, weil ...". Nur so ist sichtbar, dass nichts übersprungen wurde. Der `verdict-auditor` prüft im Workflow genau das.

---

## 3. Ablauf im Agent

1. **Input.** Konzept in einem Satz plus Quelle (Max, Paper, Discovery-Fund). Mehr braucht er nicht. Ein Why je Hypothese ist sein Output, nicht sein Input.
2. **Inventar, Pflicht vor allem anderen.** Gezielte Greps (nie volle Dateien): `Bereiche/Strategie-Logbuch.md`, `Bereiche/Hypothesen-Bank (*).md`, `discovery/hypothesis_bank.py`, `ideas.json`, Register-Zusammenfassung (`inbox_tool.py`/`summarize_results.py`, nie `registry.json` komplett), Engine-Achsen (`mb_kind` in `maband.py`, `tm_signal` in `tsmom.py`, `AX_CONFIRM`/`AX_RISK`/`AX_EXITS`), bestehende Projekt-Karten in `Projekte/`. Ergebnis: jeder Weg bekommt seinen Stand, bevor eine Story geschrieben wird.
3. **Wege-Liste füllen.** Elemente, Beziehungen, Richtungen mechanisch durchgehen (Abschnitt 2). Wege ohne Story bleiben mit Grund in der Liste.
4. **Hypothesen-Skelette bauen.** Ein Skelett je Weg und Richtung, nur für Wege mit Story und Stand `offen` oder `gemessen ohne Kandidat` mit neuem Winkel. Format ist das `ein-weg`-Format, damit die Kette ohne Umformatierung weiterläuft:

```json
{"id": "VWAP-W5a", "title": "...", "mechanism": "...", "why": "...",
 "market": "NQ", "family": "trend", "source": "familien-scout 2026-09-11",
 "path": "W5 Kreuzen und halten, long", "role": "signal", "engine_path": "maband mb_kind=vwap mb_vwap_evt=reclaim", "module_spec": null,
 "book_target": {"replaces_leg": "NQ_VWAP-Pullback"}, "related_dead": ["#211"],
 "why_status": "entwurf", "research_questions": ["..."], "rank": 3, "swing": false}
```

5. **Ranking nach Buch-Chance**, nicht nach Eleganz: Ersatz vor neu, engine-fähig vor Modul-Spec, ohne tote Verwandte vor kontaminiert, HF vor LF (Fokus seit 21.08.2026). Kosten-Schwelle je Weg mitdenken (MNQ-Round-Trip ~2 Punkte).
6. **Ausgabe, drei Dateien.** Report `discovery/scout_reports/familien_<konzept>_<datum>.md` (Wege-Tabelle mit Stand und Reihenfolge), `discovery/jobs_proposed/familien_<konzept>_<datum>.json` (Hypothesen-Liste, direkt als `args.hypotheses` für `ein-weg` nutzbar) und die Vault-Karte `Projekte/<Konzept> Wege-Karte.md` im Aufbau von [[VWAP-Offensive]]. Existiert schon eine Karte zum Konzept, wird sie nie überschrieben, die neue liegt daneben; der Abgleich ist der Abnahmetest der Hauptsession.

**Was er nie tut:** in `queue.json`, `hypothesis_bank.py`, Bank-Notizen, `book_state*.json` oder eine bestehende Karte schreiben. Kein Web (das bleibt bei `research-scout`, sonst bricht die Cache-Pflicht). Keine Backtests. Kein Urteil über Beweislage (das ist `verdict-auditor`).

**Harte Regeln:**
- Jeder Weg aus der Beziehungs-Liste bekommt einen Eintrag, auch „keine Story, weil ...". Vollständigkeit ist der Sinn des Agents.
- Ein Weg, dessen Verwandter im Logbuch tot ist, braucht einen neuen Grund oder bleibt leer. Kein Aufwärmen.
- Why-Entwurf ohne Beleg wird als `why_status: "entwurf"` markiert und bekommt eine Research-Frage. Der Scout erfindet keine Kausalität, die er nicht belegen kann.
- Wege ohne Null-Schalter-Pfad (kein `maband`/`tsmom`) bekommen eine Modul-Spec, nie einen Job-Vorschlag.

---

## 4. Workflow `konzept-weg` (gebaut 11.09.2026)

`.claude/workflows/konzept-weg.js`, Aufruf mit `name: "konzept-weg"` und `args: {concept, date: "YYYY-MM-DD", source?, market?, skip_research?, skip_ein_weg?}` (Datum ist Pflicht, Workflows haben keine Uhr).

1. **Wege:** `familien-scout` schreibt Karte, Report, JSON; liefert Wege + Skelette strukturiert zurück.
2. **Vollständigkeit:** `verdict-auditor` geht Elemente × Beziehungen × Richtung selbst durch, prüft jeden Stand gegen Register/Logbuch (Counter-Greps), sucht übersehene tote Verwandte, prüft die Swing-Markierung.
3. **Nachtrag:** nur bei Lücken. `familien-scout` trägt in dieselben drei Dateien nach, ohne umzunummerieren; Widerspruch zum Auditor wird begründet, nicht ignoriert.
4. **Research:** `research-scout`, EIN Call mit allen Research-Fragen. Cache zuerst. Je Skelett `belegt` (Why wird mit Beleg neu formuliert), `widerlegt` (geht nicht in diese Rechenrunde, bleibt aber in der Karte, kein Tot-Stempel), `offen` (geht als Entwurf weiter). Ein Why unter 20 Zeichen wird aussortiert statt den ganzen `ein-weg`-Batch zu stoppen.
4b. **Rückschreiben:** `familien-scout` trägt den Research-Stand und das Aussortierte in Karte + JSON ein, damit die Karte nicht am Tag ihrer Entstehung veraltet.
5. **Ein Weg:** Kind-Workflow `ein-weg` mit der bereinigten Liste (ohne Swing, ohne widerlegte). Ergebnis: Entscheidungstabelle je Hypothese.

Rückgabe: Dateipfade, Wege mit Stand-Zählung, Vollständigkeits-Urteil (inkl. ob nachgetragen wurde), Research-Zeilen, was rausflog und warum, das `ein-weg`-Ergebnis, die vollen Agent-Reports. Der Workflow selbst schreibt nichts; `familien-scout` schreibt die drei Dateien, `research-scout` den Cache.

**Noch nicht mit einem echten Konzept gelaufen.** Beim ersten Echtlauf (VWAP) das Ergebnis gegen die Hand-Karte gegenlesen, das ist der Abnahmetest.

**Abnahme des Baus durch `verdict-auditor` (11.09.2026): „hält mit Auflagen".** Umgesetzt: Why-Mindestlänge im Schema und Aussortieren statt Batch-Stopp, unbekannte/unbeantwortete Research-IDs werden geloggt, absolute Pfade an den Auditor, Nachtrag behält Pfade und Hand-Karte, Nachtrag als „ungeprüft" gekennzeichnet, Rückschreib-Phase, „Research widerlegt" ausdrücklich kein Tot-Stempel, Re-Lauf-Regel (Karte aktualisieren, Report/JSON mit Datum), Vollständigkeits-Modus in `verdict-auditor.md` dokumentiert, Abgrenzung in `alpha-scout.md`/`variant-scout.md`. **Offen:** Kanarien-Lauf mit `{skip_research: true, skip_ein_weg: true}` (prüft Schema-Erfüllung, Dateischreiben, Auditor findet die Karte) und ein minimaler `ein-weg`-Lauf über `workflow()`, beides erst auf Ansage von Max. Bekannte Grenze: auf dem Laptop landen Report und JSON in der Engine-Kopie vom 03.09., nur die Vault-Karte ist git-sicher.

---

## 5. Danach: Handbetrieb der Hauptsession

1. Karte lesen, mit einer bestehenden Hand-Karte abgleichen, streichen, was Max nicht will.
2. H()-Zeilen eintragen, `pipeline-auditor` setzt `pipeline_ok`, dann Enqueue + Push auf die Box.
3. Box rechnet, `verdict-auditor` stempelt je Weg, Ergebnis wandert als Stand zurück in die Karte. Damit wird die Karte zum lebenden Register je Konzept: welcher Weg offen, welcher tot, welcher im Buch.

---

## 6. Abnahmetests (auf Ansage von Max)

**Test 1, VWAP:** der Scout muss aus „VWAP" die Wege W1 bis W12 (Abschnitt 2) reproduzieren, die Rückkehr-Wege (W2/W4) als tot mit #211/#097 markieren, W5/W6 als „gemessen ohne Kandidat" bzw. „im Buch", die Anker-/Steigungs-Wege (W10, W11) als offen mit `maband`-Pfad, und Ersatz für `NQ_VWAP-Pullback` als Buch-Bezug setzen. Weil [[VWAP-Offensive]] schon existiert, legt er `Projekte/VWAP Wege-Karte.md` daneben. Weicht sein Ergebnis von der Hand-Karte ab, ist das der Abnahmetest: entweder hat die Hand-Karte einen Weg übersehen oder der Agent. Dazu die Erfahrung vom 10.09. (Daily Note): die Agents haben bewusst keine 20 Arten je Familie erfunden, sondern ehrliche Zahlen geliefert. Das muss der Scout genauso halten.

**Test 2, Fibonacci** (Research-Cache 10.09.2026, Placebo-Test der Literatur negativ, Logbuch #149). Erwartung: fast alle Wege sind Rolle „Level" und laufen auf denselben toten Verwandten, der Scout sollte das Konzept mit wenigen offenen Wegen zurückgeben statt zwanzig Hypothesen zu produzieren.

## Verwandte Notizen
[[VWAP-Offensive]] · [[Strategie-Familien]] · [[Hypothesen-Bank (Momentum & Averages)]] · [[Hypothesen-Bank (Volumen & Flows)]] · [[Discovery-Runner v2]] · [[Strategie-Logbuch]] · [[Alpha-Suche]]
