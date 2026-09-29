---
tags:
  - projekt
  - tickets
erstellt: 2026-09-29
status: Schnappschuss (Backup trading-data vom 29.09.2026 morgens)
---
# 🗂️ Ticket-Übersicht ohne Dringend (Stand 29.09.2026)

⬅️ [[Ticket-Board (Jira-Stil)]] · [[Daily Notes/2026-09-29]]

**Was drin ist:** alle offenen Tickets mit Prio **Wichtig (orange)**, **Mittel (gelb)** und **Normal (grün)**. Dringend (rot) fehlt absichtlich, die hat Max schon durchgesehen.

**Quelle:** `engine/tasks.json` aus dem GitHub-Backup `trading-data` (main `06191a4`, 29.09.2026 09:36). Die Box ist die Quelle der Wahrheit. Nicht drin sind alles, was nach dem Backup geändert wurde (auch beim Durchsehen der roten Tickets), und die danach angelegten AP267 bis AP272 (Abschnitt 4). Die Liste veraltet schnell, live gilt `/ticket` oder der Tab Tickets im Lab.

**106 Tickets:** Wichtig 20 · Mittel 72 · Normal 14.

| | Trading | Infra | Lab | Privat | Summe |
|---|---|---|---|---|---|
| Wichtig | 13 | 5 | 0 | 2 | **20** |
| Mittel | 44 | 18 | 9 | 1 | **72** |
| Normal | 6 | 2 | 4 | 2 | **14** |
| **Summe** | 63 | 25 | 13 | 5 | **106** |

Board nach der Stichwort-Regel aus `ticket_migrate.py`, sieben Tickets von Hand umsortiert (Abschnitt 5, Punkt 6). Innerhalb der Prio nach Thema gruppiert.

**Spalte „Stand":** *Max* = Max muss handeln oder entscheiden · *Claude* = Claude-Aufgabe · *läuft* = in Arbeit · *offen* = noch niemand zugeordnet.

---

## 1. 🟠 Wichtig (20)

### Discovery wieder anwerfen (Queue leer seit 23.09.)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP261 | Box-Sync Engine-Stand 25./26.09. (Gap-Null-Schalter, ctl_null, book_gate_v3) + Runner-Neustart | Claude | sofort, vor dem nächsten Discovery-Batch |
| AP257 | Latte-Audit 25.09.: Messfehler fixen, dann Kette kalibrieren (P0 bis P6) | Claude | vor dem nächsten Batch, erst P0 |
| AP250 | Gate v2 Restpunkte: Fenster OOS vs. voll, Long-only-Zwilling, Laufzeit | Claude | vor dem nächsten Batch |
| AP246 | Betriebspunkt zentral: evaluate_v2 und primary_tier-Fallback auf den gekauften Betriebspunkt | Claude | bevor die Queue wieder gefüllt wird |
| AP211 | Entscheidung Nachschub: drei Low-Prior-Jobs? Bitcoin-Daten (MBT/MET)? prescan_gross als Pflicht? | Max | vor dem nächsten Nachtlauf |
| AP194 | Job-Generator prüfen, Queue läuft leer | offen | hängt an AP211 |
| AP195 | CL-Nachtest: Filter-/Event-Hypothesen auf MCL nie gerechnet + Lint auf Assert | Max (Gate-Lockerung) | ca. 1 Box-Stunde |

### Tempo, Kauf und Konten

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP204 | Kaufpolitik zum 50k-Ziel: E8 150k + FN 150k, Deckel 2.500 $, Start E8 150k mit k2 | Max | Kauf Fr 02.10., FN 150k erst nach AP205 |
| AP245 | tempo_plan: Kalender-Modus fest einbauen, ökonomischer Tod + Zombie-Anteil | läuft (Claude) | vor dem zweiten Kauf, spätestens 06.11. |
| AP260 | tempo_plan: Ausgabe-Marken verändern die Simulation, Engine-Fix + Regressionstest | Claude | vor der nächsten Tempo-Entscheidung, spätestens 06.11. |
| AP248 | FN Flex 150k: echten Kaufpreis klären (Liste 483,99 $, Reset 278,99 $), dann FN-Größe | Max | hängt an AP205 (rot) |
| AP240 | Kinfo-Zahlen gegen eigene Zahlen abgleichen (verifizierter Track Record) | Claude | sobald neue Trades in Kinfo stehen |

### Buch

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP265 | Next-Week-Bein NQ_OpenDrive_maband2050: vor Live Delay-Kontrolle + NT8-Bein | Claude | vor dem Wochenend-Review |
| AP183 | Friedhof-Analyse 17.09.: fünf Entscheidungen + zwölf Pipeline-Fixes | Max | offen seit 18.09. |

### Box und NT8 autonom

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP86 | NT8 startet erst mit angemeldeter RDP-Session, Auto-Recovery fehlt | offen | „sofort" seit 11.08., blockiert AP177 und AP126 |
| AP134 | UI-Automation NT8: Login-Fenster ausfüllen + Strategien aktivieren | offen | nächste Session |
| AP145 | Herzschlag Soll-Ist gegen Kontoliste + darf Feed-Stillstand NT8 neu starten? | offen (Teil-Entscheidung Max) | erste Session nach dem Urlaub |
| AP177 | Windows-Updates auf der Box kontrolliert einspielen | offen | nach 20:30 ET oder Wochenende, hängt an AP86 |

### Gründung und Privat

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP37 | Revolut Business + Steuer-Rücklagenkonto mit fester Regel | läuft (Max) | nach der Gewerbeanmeldung (Okt.) |
| AP239 | Hardware (Monitor/PC) im Dezember, nur wenn der BOS-Finanzplan grün ist | Max | Dez. 2026, hängt an AP238 (rot) |

---

## 2. 🟡 Mittel (72)

### Trading: Pipeline und Gates (16)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP117 | Day-Gate-Mechanik + Tages-Gate-Kontrollbatterie in die Engine (Lehre #136) | offen | ohne Datum |
| AP122 | Pipeline-Härtung Audit 03.09.: Register append-only, Profil-Achsen-Assert | offen | nächster Engine-Block |
| AP146 | Dollar-Gates je Min-Size, n_trials aus dem Register, Kosten-Kanarie | offen | nächste Engine-Session |
| AP156 | Pipeline-Härtung CVD-Audit: exec_bug-, Daten-Integritäts-, DSR-Gate | offen | **überfällig (30.08.)** |
| AP163 | Pipeline-Fixes Audit #139: Modus-Zulassungs-Gate, replaces_leg-Assert, ehrliche Decke | offen | nächster Engine-Block |
| AP168 | FA-01-Nachlauf: gepaarte Overlay-Auswertung + Placebo in die Pipeline | offen | **überfällig (30.08.)** |
| AP173 | Familien-Sperre in promote_next + cal-Kontrollen + add_job-Validierung | offen | **überfällig (30.08.)** |
| AP182 | Vorab-Messung ES-NQ-Divergenz per backfill_registry.py ins Register | offen | vor der Auswertung von hyp_XD12_NQ |
| AP184 | book_cells.json-Cache: Engine-Fingerprint + eine Key-Funktion | offen | vor dem nächsten Buch-Bein-Patch |
| AP188 | Teilmengen-/LOO-Scan nie ohne Out-of-Bag-Spalte | offen | vor dem nächsten Subset-Scan |
| AP189 | Pipeline-Fixes AC-06d-Audit: write_json-Retry, control_labels, ctl_null | offen | nächster Engine-Block |
| AP209 | promote_next nachschärfen: block_marginal als Aufrufer, NEW-Zweig sperren | offen | vor der nächsten Wochenend-Bewertung |
| AP213 | Golden-Master: Look-ahead-Kanarie zu schwach, Erwartungen veraltet | offen | vor dem nächsten GM-Update |
| AP229 | GATES_HARD top5_share_max n-normieren (verkappter Frequenz-Wall) | offen | ohne Datum |
| AP231 | Hartes Gate „Mindest-Risiko in Ticks" in controls.py | offen | ohne Datum |
| AP264 | job_generator: Slot-Familie + Parameter-Nachbarn der Live-Beine erkennen | Claude | hängt an AP250 |

### Trading: Buch-Beine und Live-Buch (9)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP266 | Next-Week: NQ_Momentum_PB3_fa01b ersetzt NQ_Momentum_d260818 (knapp) + NT8-Umbau | Max | Wochenend-Review |
| AP118 | NQ_Momentum_d260818: DSR-Nachweis nachrechnen | offen | kein Zeitdruck |
| AP119 | NQ_LastHour_v3: neue Delay-Kontrolle fällt durch (z = -3,39) | offen | nächster Engine-Block |
| AP121 | Momentum: BE-Komponente nicht von Null unterscheidbar, Why korrigieren | offen | Wochenend-Review, keine Alleinentscheidung |
| AP120 | TS-01-v2 EWMAC: Timing-Verdacht nach Cutoff-Bugfix | offen | vor der nächsten TS-01-Entscheidung |
| AP129 | Entscheiden: Risikofaktoren je Bein statt Uniform-Sizing? | offen | nächster Engine-Block |
| AP161 | Backtest-Exit 15:55 wie live: sigcore, Developer-Cache, Edge-Ref, Register | offen | **überfällig (20.09.)** |
| AP172 | Live-Betrieb härten (Noel-T): DD-Kill-Switch, Inkubations-Bank, MC-DD je Bein | offen | **überfällig (30.08.)** |
| AP186 | Bestandsdurchlauf: vier Buch-Aufnahmen unter korrigiertem Rauschmaß nachrechnen | offen | Blocker AP185 ist weg |

### Trading: Alpha-Suche und neue Märkte (16)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP147 | VWAP-Offensive: zwölf Familien abarbeiten | offen | laufend |
| AP150 | maband VWAP-Erweiterungen: ATR-Distanz, Level-Export, tm_exit=level | offen | nach hyp_AW14b_NQ |
| AP259 | FLIP (Renko-Flip NQ): Null-Schalter bauen, damit zwei Kandidaten durch Gate v2 können? | Max | war fürs Wochenende 26./27.09. geplant |
| AP198 | Überthema Neue Märkte: 6E/6B, ZS/ZW, neue Mechanismen statt Klone | offen | laufend |
| AP140 | Gold (GC) als erster Nicht-Index-Markt ins Discovery-Universum, danach CL | offen | hängt formal an AP142 und AP143 |
| AP142 | Datenexport neue Futures-Symbole über Databento | offen | hängt an AP143 |
| AP197 | Session-Fenster je Markt (GC, CL, FX London) + sigcore-390-Minuten-Annahme | offen | vor jeder weiteren Runde auf GC/6E/6B/ZS/ZW |
| AP167 | Modul cal_mode='macro_post' (CPI/NFP auf ES) + BLS-Datumslisten | offen | **überfällig (30.08.)** |
| AP218 | Fit außerhalb RTH: Intraday Bias (LBMA-Fix GC), stärkster Kandidat | Claude | ohne Datum |
| AP219 | Fit außerhalb RTH: Trend Following (London-Anker fehlt) | Claude | ohne Datum |
| AP220 | Fit außerhalb RTH: Mean Reversion (Fix-Anker statt Session-VWAP) | Claude | hängt an AP218 |
| AP221 | Fit außerhalb RTH: Relative Value (GC/SI, 6E/6B), datenblockiert | Claude | ohne Datum |
| AP224 | Wiederaufnahme #164 (TD-12): Blocker „keine unkorrelierten Märkte" seit #165 weg | Claude | wenn Rechenzeit frei ist |
| AP225 | Wiederaufnahme #119 (NOISE_ORB): Größen-, kein Qualitätsproblem, bei 150k neu | Claude | zusammen mit AP204 |
| AP226 | Wiederaufnahme #106: 22 Kandidaten mit einer Min-Size-Folgerung erschlagen | Claude | nach dem neuen Betriebspunkt in book_state |
| AP227 | RVOL-Wege W18/W21/W23 aus dem „Kapitel zu" lösen | Claude | nach dem Feasibility-Vorfilter |

### Trading: Evals und Firmen (3)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP111 | E8-Support: Payout-Caps für 100k/150k schriftlich bestätigen lassen | offen | „nächste Woche" seit 20.08. |
| AP234 | E8-Regeln zu Overnight-Halten und „Gapped Market Trading" ungeprüft | offen | ohne Datum |
| AP127 | eval_journal.json für die Überwachung der AP107-Widerlegungsregeln | offen | vor dem nächsten Bust |

### Infra: NT8-Deploy-Paket (5)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP159 | NT8-Beine härten: Phantom-Fills, AsiaDir IgnoreAllErrors, Zeit statt Bar-Zähler | läuft | Deploy nach Handelsschluss oder am Wochenende |
| AP144 | OnExecutionUpdate ohne Realtime-Filter: Sim-Fills landen im Live-Log | läuft (Max) | nächstes Deploy-Fenster |
| AP171 | RiskGuard End-of-Day-Telegram-Report: fertig, Deploy fehlt | offen | **überfällig (30.08.)** |
| AP216 | MaxMomentumNQ: Break-Even-Stop nutzt Signal-Bar-Close statt Fill-Preis | läuft (Claude) | kein Zeitdruck |
| AP193 | maxlab_acct_fills/orders-CSV schreiben seit 14.09. nicht mehr | offen | kein akutes Handelsrisiko |

### Infra: Konten und Überwachung (4)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP203 | Regel-Check: RiskGuard automatisch umstellen beim Wechsel Challenge zu Funded | offen | vor dem ersten Statuswechsel |
| AP212 | Live-Sicht nach Konto-Suffix: Watchdog, vps_health, auto_check auf neue Dateinamen | offen | zeitnah |
| AP126 | CushionFrac Konto A (E8) prüfen: noch 0,14 oder Min-Size v2? | offen | hängt an AP86 |
| AP132 | Mehrkonten-Zuordnung zentral (RiskGuard, Telegram, Sizing je Konto) | offen | irgendwann |

### Infra: Box, Runner und Geräte (6)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP137 | Null-Schalter Buch-Modi + Kalender/DIX-Gates deployen, Ersatz-Slot-Semantik | offen | erste Session nach dem Urlaub |
| AP131 | Discovery-Runner parallelisieren (4 Worker, ca. 4x Durchsatz) | offen | wenn die Queue Vorrat hat |
| AP136 | Bash-Berechtigung für Claude auf der Box | Max | nächste Session |
| AP148 | Git-Härtung: Engine unter Git, Schreib-Sperre, Union-Merge, Branch-Bereinigung | offen | nach dem Urlaub, am PC |
| AP179 | PBO-Median-Konvention entscheiden + NSSM/Box-Skripte auf den PC | Max | erste Session nach der Rückkehr |
| AP201 | Geräte-Abgleich: settings.json am PC, Laptop-Patches, Laptop-Token | offen | settings.json „sofort" |

### Infra: Daten und Live-Automatisierung (3)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP155 | Entscheiden: Live-Strategien künftig über NT8-Host, MultiCharts oder Tradovate-API? | Max | nach dem Urlaub |
| AP199 | Datenquelle: NT8 neben oder statt Databento (1,8 pp Quellenrauschen) | offen | vor der nächsten Buch-Entscheidung unter 2 pp |
| AP196 | NT8-Historie: fehlende Front-Kontrakte nachladen (GC, CL, 6E/6B) | offen | nur außerhalb der Handelszeit |

### Lab und Tools (9)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP243 | Workbench Rest: NT8-Overlay deployen + lab_ui auf die Box | Claude | Wochenend-Deploy, Blocker AP241 ist weg |
| AP255 | Workbench/Lineal: offene Punkte vom verdict-auditor (SR-Verhältnis, FN-Consistency, Gate v2) | Claude | nächste Lab-Session |
| AP262 | Lab-Sharpe überzeichnet seltene Strategien, Tages-Sharpe mit Nulltagen | Claude | nächste Lab-Session |
| AP125 | Regime-Wächter im Portfolio-Tab (rollierende 3J-Drift, Kelly-Check) | offen | nächster Engine-Block |
| AP130 | Sizing-Trichter im Portfolio-Tab (Passquote + E[Auszahlung] über der Buchgröße) | offen | hängt an AP125 |
| AP187 | Buch-Korrelationsanzeige zeigt nur den Mittelwert, keine Mechanismus-Cluster | offen | vor der nächsten Buch-Komposition |
| AP207 | Nacharbeit Agent-Nutzungs-Audit (#166/#167): Vorbehalts-Zeilen, TE-Block-Sperre | Claude | vor dem nächsten --enqueue |
| AP208 | Wirkungskontrolle Auftrags-Typ-Router: Lücken zu? Wie viele Fehlalarme? | Claude | fällig seit 28.09. |
| AP253 | claude-code-router behalten oder deinstallieren? | offen | nächste ruhige Minute |

### Privat (1)

| AP | Thema | Stand | Fällig / hängt an |
|---|---|---|---|
| AP249 | Anbieter-Konten auf Privat- oder Firmenkunde (USt-IdNr) umstellen | Max | nach der Gewerbeanmeldung, Blocker AP235 ist erledigt |

---

## 3. 🟢 Normal (14)

| AP | Board | Thema | Stand | Fällig / hängt an |
|---|---|---|---|---|
| AP123 | Trading | Exit-Forschung Stufe 2: ATR-/Chandelier-Trailing | offen | nach AP121 |
| AP192 | Trading | Asia-Dir tmin_entry auf anderer Uhr (heute folgenlos) | offen | nur bei buchweitem Tagesstopp |
| AP247 | Trading | NQ_Gap-fade_hf ohne Kapital weiter beobachten | Claude | monatlich ab 11/2026, Entscheidung 01.10.2027 |
| AP263 | Trading | Batch-Harness für Scratch-Nachläufe | Claude | beim nächsten großen Scratch-Batch |
| review-2026-38 | Trading | Wochen-Review KW38: Ampeln, Journal, Logbuch | offen | ohne Datum |
| review-2026-39 | Trading | Wochen-Review KW39: Ampeln, Journal, Logbuch | offen | ohne Datum |
| AP143 | Infra | Databento-Account + echte Kostenabfrage GC/CL/SI/NG/ZN/6E | offen | nach dem Urlaub |
| AP200 | Infra | Aufräumen nach der NT8-/Neue-Märkte-Aktion | läuft | bei Gelegenheit |
| AP149 | Lab | familien-scout + Workflow konzept-weg in den Hub-Roster | offen | nach der Rückkehr |
| AP254 | Lab | session-guard + box-ops zurück auf haiku | offen | nachdem alle Sessions neu gestartet sind |
| AP44 | Lab | Claude dispatch / Claudian anschauen | offen | „sofort" seit 09.08. |
| AP256 | Lab | Workbench-Notizblock: ja oder nein | Max | irgendwann |
| AP39 | Privat | Beim ersten Payout: Processor-Einladung (WorkMarket/Rise) inkl. W-8BEN | offen | beim ersten Payout |
| AP251 | Privat | Belege nachsammeln ab Oktober (Contabo, Claude, E8 150k) | offen | erstmals 07.10., dann monatlich |

---

## 4. Nach dem Backup angelegt (Prio unbekannt)

Aus [[Ticket-Board (Jira-Stil)]]: AP267 Box einspielen (Max) · AP268 `tasks.json` vom Engine-Sync ausnehmen · AP269 Auto-Tickets auf der Box · AP270 Box-seitig atomar und unter Sperre · AP271 `updated` mit Zeitzone (vor 25.10.) · AP272 Wiedervorlagen als maschinenlesbare Liste.

Noch gar nicht angelegt (Daily Note 29.09., Juli-Modus): Nacht-Tafel 18:00 bis 09:30 ET plus Earnings-Test, fällige Wiedervorlage #139 (Vola-Sizing).

---

## 5. Hinweise

1. **AP261 nicht ohne AP268.** Der Box-Sync überschreibt die Box-`tasks.json` mit dem PC-Stand. Vor AP261 erst die Box-`tasks.json` sichern oder AP268 erledigen.
2. **Drei Blocker sind weg:** AP186 (AP185 steht nicht mehr in `tasks.json`), AP243 (AP241 ebenso), AP249 (AP235 erledigt).
3. **Veraltete Daten-Kette:** AP140 (Gold) hängt formal an AP142 und AP143 (Databento). Die GC/CL-Daten kamen aber über NT8 (#165). AP142 und AP143 mit AP199 zusammenlegen oder schließen, dann ist AP140 frei.
4. **Sieben Mittel-Tickets überfällig nach festem Datum:** AP156, AP167, AP168, AP171, AP172, AP173 (alle 30.08.), AP161 (20.09.). Neues Datum setzen oder schließen.
5. **Vermutlich (teilweise) erledigt, kurz prüfen:** review-2026-38 (KW39 liegt schon daneben), AP148 (trading-data ist inzwischen ein Git-Repo mit GitHub-Backup, Rest offen?).
6. **Für die Migration (AP267):** Die Stichwort-Regel in `ticket_migrate.py` legt AP136 wegen „Prozess-**Steuer**ung" aufs Board Privat. Hier von Hand umsortiert: AP122, AP150, AP184, AP265, AP266 nach Trading, AP136 und AP216 nach Infra.
