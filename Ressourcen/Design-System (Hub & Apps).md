---
tags: [design, ui, hub, strategy-lab]
erstellt: 2026-08-30
status: lebend
---

# Design-System (Hub & Apps)

Die **verbindliche Quelle** für Aussehen und Bedienung aller Apps, die Max baut. Der Subagent `design-guard` prüft jede UI-Änderung gegen diese Datei. Was hier nicht steht, ist nicht entschieden — dann fragt der Agent nach, statt zu raten.

**Wichtig:** Jede App hat ihre **eigene Charta**. Nicht alle Apps sehen gleich aus, aber jede App sieht **in sich** überall gleich aus. Ein neuer Button im Strategy Lab sieht aus wie die Buttons, die dort schon stehen — nicht wie ein Hub-Button und nicht wie ein neu erfundener.

Diese Datei liegt im Vault (versioniert), weil `C:\Users\maxlk\Projects\hub` **kein Git-Repo** ist — eine Charta im Hub-Ordner wäre bei jedem Fehlgriff endgültig weg.

---

## 0. App-übergreifende Grundregeln (gelten IMMER, in jeder App)

Max' Bedien-Prinzipien, unabhängig von Farben und Optik.

### Bedienung / Usability
1. **Klick-Tiefe minimal.** Was Max oft braucht, ist mit **einem** Klick erreichbar. Zweiter Klick nur für Seltenes. Nie eine Aktion hinter drei Menüs verstecken.
2. **Klickfläche ≥ 32×32 px** (Ausnahme: Icon-Buttons in dichten Zeilen ≥ 28 px). Der sichtbare Rahmen darf kleiner sein als die Klickfläche, nie umgekehrt.
3. **Klick-Ziele wandern nicht.** Beim Laden/Aktualisieren darf sich kein Button verschieben (Platzhalter reservieren statt einblenden), sonst klickt Max daneben.
4. **Jeder Klick antwortet sofort** (< 100 ms sichtbar): Hover-Zustand, Aktiv-Zustand, oder Spinner/Disabled bei längeren Aktionen. Nie ein Button, der still nichts tut.
5. **Kein Doppel-Auslösen.** Buttons, die einen Lauf starten, gehen sofort in `busy` (disabled + Spinner) bis das Ergebnis da ist.
6. **Destruktives ist anders.** Löschen/Überschreiben/Deploy nie in derselben Optik wie Normalaktionen und nie direkt neben dem meistgeklickten Button.
7. **Zustand ist ablesbar ohne Klick.** Ampel/Badge/Zahl direkt sichtbar, nicht erst im Tooltip.
8. **Tastatur:** Esc schließt jedes Overlay/Fenster, Enter bestätigt das Hauptfeld eines Formulars.
9. **Nichts flackert.** Kein Voll-Reload für eine Teil-Aktualisierung; Listen an Ort und Stelle aktualisieren.
10. **Leere Zustände erklären sich.** "Keine Kandidaten" plus eine Zeile warum und was jetzt zu tun ist, nie eine leere Fläche.

### Optik
11. **Nur Tokens, keine losen Werte.** Farben, Abstände, Radien, Schriftgrößen kommen aus den `:root`-Variablen der jeweiligen App. Ein hartkodiertes `#5b8fd6` mitten im Markup ist ein Befund.
12. **Eine Radius-Familie je App**, keine Mischung aus 5/9/12 px im selben Fenster.
13. **Abstände aus einer 4-px-Skala** (4/8/12/16/20/24). Keine krummen 7/13/19 px, außer die App-Charta nennt sie ausdrücklich.
14. **Zahlen immer `tabular-nums` + Mono**, damit Spalten nicht springen.
15. **Farbe trägt nie allein Bedeutung** (rot/grün immer zusätzlich mit Vorzeichen, Wort oder Icon).
16. **Text kürzt sauber** (`ellipsis`), das Layout bricht nie wegen eines langen Strategie-Namens.

---

## 1. Hub — Desktop-Cockpit

`C:\Users\maxlk\Projects\hub\static\hub.css` · Stil: **Discord-artig**, dunkelgrau gestuft, kompakt, viele Fenster nebeneinander.

**Tokens (Ist-Stand, `:root` in `hub.css`):**

| Rolle | Token | Wert |
|---|---|---|
| Rail | `--bg-0` | `#1e1f22` |
| Channels | `--bg-1` | `#2b2d31` |
| Inhalt | `--bg-2` | `#313338` |
| Hover | `--bg-3` | `#383a40` |
| Aktiv | `--bg-4` | `#404249` |
| Text | `--fg` / `--fg-muted` / `--fg-dim` | `#dbdee1` / `#949ba4` / `#80848e` |
| Akzent | `--accent` | `#5865f2` |
| Ampel | `--green` / `--yellow` / `--red` | `#23a559` / `#f0b232` / `#f23f43` |
| Rahmen | `--border` | `rgba(255,255,255,.06)` |
| Schrift | `--font` / `--mono` | gg sans / JetBrains Mono |

**Regeln:**
- Fenster (`.win`): Radius **10 px**, Schatten `0 8px 24px rgba(0,0,0,.35)` plus 1 px Border-Ring. Drag/Resize-Zustand färbt den Ring auf `--accent`.
- Fenster-Kopf `.app-frame-head`: 40 px hoch, `--bg-1`, 13 px, `600`.
- Hover = `--bg-3`, aktiv/ausgewählt = `--bg-4`. Nie eine dritte Hover-Farbe erfinden.
- Icons 17 px (`.ico`), immer `flex: none`.
- **Neue Sub-App im Hub** = eigenes `.win` mit `.app-frame-head`, nicht ein eigenes Layout-Konzept.

**Änderungs-Weg:** `static/` bzw. `hub_config.json` bearbeiten, dann `.\hot_reload.ps1`. Kein Rebuild, kein Neustart (CLAUDE.md).

---

## 2. Strategy Lab (+ Developer-Tab)

`C:\Users\maxlk\Projects\trading-data\engine\lab_ui\` (seit 25.09.2026: `index.html`, `lab.css` mit `:root`, `lab.js`, dazu `workbench.css/.js`; vorher HUB-String in `app_server.py`, AP244) · Selbsttest nach jeder Änderung: `python lab_selftest.py` · Stil: **fast schwarz, Terminal-Ernst, Gold-Akzent**, viel Tabelle und Zahl.

**Tokens (Ist-Stand):**

| Rolle | Token | Wert |
|---|---|---|
| Seite | `--page` | `#0a0a0b` |
| Karte | `--surface` / `--surface2` | `#141416` / `#1c1c1f` |
| Text | `--text` / `--text2` / `--muted` | `#f3f3f0` / `#a8a7a1` / `#6d6c67` |
| Aktion | `--blue` | `#5b8fd6` |
| Akzent | `--accent` | `#c79a3f` |
| Gewinn/Verlust | `--up` / `--down` | `#33a37c` / `#d76666` |
| Rahmen / Grid | `--border` / `--grid` | `rgba(255,255,255,.08)` / `rgba(255,255,255,.05)` |
| Mono | `--mono` | Cascadia/Segoe UI Mono/Consolas |

**Bausteine (so und nicht anders wiederverwenden):**
- **Tab oben:** `.tv` — `7px 15px`, Radius 9, 13 px, `700`, inaktiv `--surface2`/`--text2`, aktiv `.tv.on` = `--blue` auf Weiß.
- **Karte:** `.devcard` (Radius 5, `--surface`, 1 px `--border`, Padding `14px 16px`) bzw. `.lcard` (Radius 12, Padding `13px 16px`) für KPI-Kacheln.
- **Button:** `.devbtn` primär (`--blue`, weiß, `700`), `.devbtn.sec` sekundär (`--surface2`, `--text2`, Border), `.devbtn.busy` = 55 % Deckkraft plus kein Pointer.
- **Spinner:** `.devspin`, 12 px, Border-Top in `--blue`, `.8s linear`.
- **KPI-Zahl:** `.lcard .big` 22 px `800`, darunter `.mt` in `--muted` 11.5 px.
- **Charts:** Achse `#78776f`, Grid `rgba(255,255,255,.05)`, Equity/Fächer 580 px, Histogramme 300 px — **identisch in Report und Developer-Tab** (CLAUDE.md-Regel, driftet sonst auseinander).

**Bekannte Ist-Abweichung (Aufräum-Kandidat, nicht Vorbild):** Radien laufen aktuell 5 / 9 / 12 px durcheinander (`.devcard` 5, `.jday` 9, `.lcard` 12). Bis Max eine Ziel-Radius-Familie festlegt gilt: **neue Elemente übernehmen den Radius des Bausteins, den sie kopieren** — keine vierte Zahl dazu erfinden.

### 🎯 Soll-Ansicht Strategy Lab (Entwurf, 30.08.2026 — Basis: UX-Recherche, wartet auf Max' Freigabe)

**Leitidee:** Terminal-Ernst bleibt, aber die App soll sich wie ein geschlossenes Desktop-Werkzeug anfühlen, nicht wie eine Website mit vielen Tabs. Kein neues Farbschema, kein Rebrand — es geht um Konsistenz, Feedback und Bedientempo.

**A. Tokens final (löst die alte "5/9/12 durcheinander"-Abweichung auf)**

| Token | Wert | Ersetzt |
|---|---|---|
| `--radius` | **6px**, einzige Radius-Familie im ganzen Lab | `.devcard`(5) `.tv`(9→5) `.lcard`(12→5) `.jday`(9→4) `.badge`(7→4) `.pop`(7→4) `.col`(12→5) `.icard`(10→4) `.rcard`(4) — alle auf 6 |
| `--space-*` | 4-px-Skala: 4/8/12/16/20/24/32 | krumme Werte wie `14px 16px`-Padding, `9px`-Gaps beim Umsetzen glätten |
| `--motion-fast` | 0 ms (Hover/Active per CSS `:hover`/`:active`, sofort) | — |
| `--motion-state` | 150–200 ms ease-out (Spinner rein, Karte einblenden, Tab-Wechsel) | nichts über 300 ms — fühlt sich sonst träge an für ein Tool, das Max den ganzen Tag bedient |

**B. Neue/erweiterte Bausteine**

1. **Command Palette** (`Strg+K`, global über alle Top-Tabs erreichbar): Fuzzy-Sprung zu Reports/Tickets/Strategien, Tab wechseln, "Neu durchrechnen" für die aktive Developer-Version, Ticket anlegen, Inbox pull. Ein Eingabefeld, Ergebnisliste mit Tastatur (Pfeiltasten + Enter), `Esc` schließt (Grundregel 8).
2. **Shortcut-Overlay** (`?`-Taste zeigt Cheat-Sheet): macht die Tastenkürzel entdeckbar, sonst bleiben sie ungenutzt.
3. **Busy/Empty/Error einheitlich für JEDEN Button**, nicht nur `.devbtn`: aktuell haben `.pop`, `.jnav`, `.nmlink`, Idea-Engine-Aktionen keinen sichtbaren Busy-Zustand — genau die Lücke, die eine App "tot" wirken lässt (siehe Recherche: Feedback < 100 ms Grundregel 4). Ein einziges CSS-Muster (`.busy` = 55 % Deckkraft + Spinner-Icon-Vorlage aus `.devspin`) für alle klickbaren Elemente im Lab, nicht pro Tab neu erfunden.
4. **Platzhalter reservieren statt einblenden** bei allen Listen/KPI-Kacheln (Grundregel 3) — v.a. beim Report-Refresh in der Sidebar und beim Portfolio-Reload, wo aktuell die Liste kurz leer aufblitzt.

**C. Hierarchie je Bereich**

| Tab | Regel |
|---|---|
| Lab · Reports | Sustained-Reading-Dichte (Liste bleibt eng), wichtigste Kennzahl je Report-Item größer/fett, Rest gedimmt (`--muted`) |
| Lab · Portfolio | Ein-Blick-Kriterium zuerst (P(funded)-Delta), Kaufplan/Frontier darunter — genau wie jetzt, nur mit reservierten Platzhaltern beim Neurechnen |
| Idea Engine | Board bleibt (6 Spalten), aber `.icard` bekommt denselben Busy-Zustand wie Developer-Karten |
| Live / Journal | Entscheidungsmoment-Dichte (mehr Weißraum als Reports-Liste), Tagesergebnis größtes Element pro Kachel |
| Developer | unverändert Referenz-Baustein für Karten/Charts (Regel: Report und Developer-Tab bleiben 1:1) |
| Tickets | Badge-Zahl bleibt einzige Ampel, Rest wie Journal |

**D. Bewusst unverändert**
- Chart-Optik (Achsen, Grid, Höhen) bleibt exakt wie in `report.py` — bestehende CLAUDE.md-Regel, hier nicht neu verhandelt.
- Farbpalette (`--page`/`--surface`/`--accent` etc.) bleibt, keine Recherche-Trend-Farben übernehmen.

**E. Noch offen für Max**
- Ob die Command Palette auch strategie-spezifische Aktionen bekommt (z.B. "Bein XY ins Next-Week-Buch") oder erstmal nur Navigation+Neu-Rechnen macht.

**F. Entschieden, 30.08.2026 (zweite Runde — Sidebar + Portfolio-Reihenfolge)**
- Tokens (6px-Radius, 4px-Abstandsskala) sind freigegeben und umgesetzt, nicht mehr offen.
- **Lab-Sidebar nur noch bei "Reports" sichtbar.** Die 4 Unter-Tabs (Reports/Vergleich/Prop-Valide/Portfolio) sitzen jetzt in einer schmalen Kopfzeile über `.app`, nicht mehr in der 310px-Sidebar. Bei Vergleich/Prop-Valide/Portfolio bekommt der Inhalt die volle Breite (Grund: die Report-Liste war dort irrelevant und hat nur Platz weggenommen).
- **Portfolio-Tab-Reihenfolge:** Titel → Equity-Kurve/vollständiger Report (bewusst weiter eingeklappt, ein Klick — der iframe ist selbst ein kompletter zweiter Report mit eigener Verdict-Karte/KPI/MC-Tabellen, permanent offen würde sich mit der KPI-Zeile direkt darunter doppeln) → KPI-Kacheln (Net Profit/Win Rate/Sharpe/Return-DD/Trades-Jahr/Note, aus den bestehenden Top-Level-Feldern von `portfolio.json`) → Passquote-je-Eval/Zeit-Sicht (Zielfunktion-Box) → Kaufplan/Betriebspunkt/Konten → Rest (Firma-Regeln, Cushion-Frac-Erklärung, Beine, Frontier) unverändert weiter unten. Nichts entfernt, nur umsortiert.
- **Offen:** eine wirklich freistehende Equity-Kurve ganz oben (ohne den restlichen Report mitzuziehen) bräuchte einen eigenen leichten Chart-Endpunkt (`portfolio.json` hat aktuell keine rohe Kursreihe, nur Kennzahlen) — aktuell ungebaut, auf Zuruf nachrüstbar.

**G. Entschieden, 30.08.2026 (dritte Runde — echter Equity-Chart + volle KPI-Zeile, Max' Feedback nach Testen)**
- Die unter F. offene Lücke ist geschlossen: `portfolio.json` hat jetzt `equity_dates`/`equity_usd` (kam aus `copilot.full_report_data()`, war schon berechnet, stand nur nicht in der Datei — `funded_finalize.py` reicht es jetzt durch). Der Equity-Chart oben im Portfolio-Tab ist ein echter Chart.js-Chart (`drawPortEquity()`), kein iframe mehr.
- **KPI-Kachel-Zeile mit 16 Feldern** direkt unter der Equity-Kurve (Net P&L, Win Rate, Profit Factor, Sharpe, Max DD $/%, Expectancy/Trade, Avg Hold, Trades/Woche, Trades gesamt, Avg Win/Loss, Largest Win/Loss, Win/Loss-Streak) — Vorbild war ein Screenshot einer fremden App mit genau dieser Kachel-Reihe. Nutzt `.lcard`/`.mt`/`.big`, keine neue Optik. Drei Felder (`largest_win_usd`, `largest_loss_usd`, `avg_hold_min`) waren komplett neu und stecken jetzt in `qbt.py::metrics()`.
- **Nur noch Equity-Kurve + KPI-Zeile + Beine im Buch + Speed/Pass-Frontier sind permanent sichtbar.** Zielfunktion/Kaufplan/Firma-Regeln sind jetzt auch `portDetails` (einklappbar) statt `portSection` — Max' Linie: alles was nicht "auf einen Blick" gebraucht wird, ist zu.
- Ein Status-Label ("Zeit-Sicht, seit 16.08. nur noch Kontext") von Orange auf `var(--muted)` geändert — Orange bleibt echten Warnungen vorbehalten (Grundregel: Farbe nie alleinige Bedeutung, aber auch nicht inflationär für Nicht-Warnungen).
- Scroll-Bug (Portfolio-Tab sprang beim Scrollen manchmal zurück zu "Reports", vermutlich Windows-Touchpad-Zurück-Geste): `overscroll-behavior-x:none` auf `html,body`, `overscroll-behavior:contain` auf `.main` gesetzt.

**H. Bloomberg-Umbau, 01.09.2026 (Max: "ich mag die Bloomberg-Terminal-Optik — dicht gestapelte, kleine Kacheln nebeneinander"; nach Testen des Portfolio-Piloten: "ja mach es so im ganzen Lab").**
Kein neues Farbschema — `--accent` (Gold `#c79a3f`) übernimmt die Rolle von Bloombergs Orange, `--up`/`--down` blieben unverändert grün/rot. Rollback: `app_server.py.bak-20260901-bloomberg-pilot` (kompletter Stand vor dem gesamten Umbau, Portfolio-Pilot + Lab-Rollout).

- **Neue Bausteine** (CSS `.bbgrid`/`.bbpanel`/`.bbstrip`, JS `bbPanel()`/`bbCell()`): ein 4-spaltiges CSS-Grid mit dichten Panels. Panel-Kopf: kleine Mono-Caption in `--accent`, Panel-Körper dicht gepolstert (`--sp-2`/`--sp-3` statt der bisherigen 13-17px), eigener dünner Scrollbar (`scrollbar-width:thin`) statt des nativen hellen Balkens.
- **`design-guard`-Korrekturrunde 01.09.2026** (Erstversion hatte zwei Befunde): kein eigener `--radius-bbg` mehr — `.bbpanel` nutzt das bestehende `--radius` (6px), Abschnitt 2.A bleibt die einzige Radius-Familie im Lab (Grundregel 12), ein zweiter Radius war ein Befund, kein akzeptabler Pilot-Kompromiss. Alle Abstände in `.bbgrid`/`.bbpanel`/`.bbstrip` laufen jetzt über `--sp-*` statt frei erfundener px-Werte (Grundregel 11/13).
- **KPI-Kachel-Wand → KPI-Streifen:** die 16 `.lcard`-Kacheln (4×4-Grid, Abschnitt G) sind ersetzt durch EINEN `.bbstrip`-Panel — eine Zeile schmaler Zellen mit Haarlinien-Trennern statt Kartenabständen. Gleiche 16 Felder, gleiche Datenquelle (`portfolio.json`), nur als Terminal-Streifen statt Karten-Wand.
- **Beine + Frontier nebeneinander:** vorher zwei volle `portSection()`-Karten untereinander, jetzt zwei `.bbpanel`s in einer `.bbgrid`-Zeile (je 2 von 4 Spalten; ohne Frontier-Daten bekommt Beine die volle Breite). `portSection()` selbst ist unverändert und bedient weiterhin den Funded-Analyse-Block (`fa_*`) — bewusst NICHT ersetzt, bis sich der Pilot bewährt hat.
- **Lange Freitext-Spalten truncaten** (`.bbtrunc`, z.B. "Mechanik") statt die Kachel in die Breite zu ziehen oder einen hässlichen horizontalen Scrollbalken zu erzwingen — Volltext im `title`-Tooltip, vollständige Erklärung bleibt in der aufklappbaren Zeilen-Detailansicht.
- **Scoped statt global:** drei Blau→Gold-Farbwechsel (aktiver Kaufplan-Frac, Konto-Markierung in der Frontier-Tabelle, Kaufplan-Kartenrand) sind NUR innerhalb `renderPortfolio()` inline geändert — der globale `--blue`-Token (Developer-Buttons, Tab-aktiv-Zustand, Links in anderen Tabs) bleibt unangetastet.
- **Rollout aufs ganze Lab, 01.09.2026 (gleicher Tag, zweite Runde):** dieselben Bausteine (`bbPanel`/`bbCell`/`.bbgrid`/`.bbstrip`) jetzt auch außerhalb vom Portfolio-Tab:
  - **Journal** (`renderJournal()`): die 11-teilige Statistik-Zeile ist ein `.bbstrip` in `bbPanel('jstat','Key Metrics',...)`.
  - **Tickets** (`renderTickets()`): die 8-teilige Zusammenfassungs-Zeile ebenso, `bbPanel('tkstat','Key Metrics',...)`.
  - **Live** (`renderLive()`): "Trades" + "Trade-Detail" stehen als zwei `bbPanel(...,2)` nebeneinander (gleiches Muster wie Beine/Frontier). Trade-Detail behält innen `class=lcard` (Box-Chrome per Inline-Style neutralisiert), weil `selTrade()` dessen `.nm`/`.big`/`.mt` über die `.lcard`-gescopten Regeln stylt — ohne die Klasse würde die Detailkarte ihre Typografie verlieren.
  - **Idea Engine** (`renderIdeas()`): NUR die Kanban-Spalten-Kopfzeile (`.col h3`) ist jetzt Mono-Uppercase in `--accent` statt System-Font in `--text2` — an die neue Panel-Kopf-Sprache angeglichen. Board-Struktur selbst (6 Spalten) unverändert, war schon vorher gekachelt.
  - **Vergleich** (`renderCompare()`) und **Prop-Valide** (`renderProp()`): der freie `<h2>`-Titel ist jetzt ein `bbPanel(...,4)`-Rahmen um die unveränderte Sortier-Tabelle. `.bbbd` bekommt hier `overflow:visible` (die Tabelle ist potenziell sehr lang und soll mit der Seite scrollen, nicht in einer eigenen Box).
  - **Developer:** NUR die "Kompakte Kennzahlen"-Zeile (5 `devStat()`-Kacheln) steckt jetzt in `bbPanel('devkpi','Key Metrics',...)` — die Kacheln selbst sind unverändert (sie tragen Label + Wert + Meta-Zeile, mehr als ein `bbCell` kann, deshalb bewusst nicht auf `.bbstrip` reduziert). Der "Kaufplan"-`devStat`-Block, alle `.devcard`-Prosa-/Tabellenblöcke (Regelwerk, OOS-Kontrolle, Solo-Frontier, Buch-Beitrag) und die Chart-Karten (`.rcard`, Abschnitt D "bewusst unverändert") sind bewusst NICHT angefasst — größerer Umbau, eigene Entscheidung wert, siehe "Offen für Max" unten.
- **`design-guard`-Korrekturrunde 01.09.2026 (zweite Runde):** ein Befund — Journals `Profit-Factor`-Zelle hatte Farbe (grün/rot) ohne Vorzeichen/Wort (Regel 15) und war inkonsistent zum bereits freigegebenen Portfolio-KPI-Streifen (dort bewusst neutral). Fix: Farbe entfernt, `bbCell('Profit-Factor',pf.toFixed(2))`.
- **Report/Developer-Sync, 01.09.2026 (dritte Runde — "ja alles", inkl. `report.py`):** die zwei verbliebenen Lücken aus der "Offen für Max"-Zeile oben sind geschlossen, aber bewusst NICHT durch eine Kachel-Restrukturierung von `.devcard`/`report.py`, sondern durch eine gezielte Kopf-Farb-Angleichung — das Risiko einer vollen Neuaufteilung der ~250 Zeilen Report-Erzeugung (Referenzdokument für jede historische Strategie-Bewertung) stand in keinem Verhältnis zum optischen Gewinn:
  - **`report.py`** (das Template für JEDEN `/reports/*.html` UND jeden `/devreports/*.html`): `h2` ist jetzt Mono + `--accent` statt Text-Weiß-Uppercase — cascadiert auf JEDEN Abschnitt (Equity curve, Score-Aufschlüsselung, Regime, Monte-Carlo, Selektions-Ehrlichkeit, Heatmap, Prop Firm Assistant). `.kpi`/`.grid-kpi` dichter gepackt (Zellbreite 148px→122px, Value-Schrift 22px→18px, Padding 13/15px→9/12px), `.card`-Padding 16/18px→14/16px. Mit einer eigenen Sanity-Check-Seite (`report._kpi()`/`report.CSS` isoliert gerendert, danach gelöscht) optisch geprüft, nicht per vollem Report-Rebuild (dauert Minuten, siehe Abschnitt 3-Warnung unten) — **bestehende `reports/*.html`-Dateien zeigen die neue Optik erst nach ihrem nächsten Rebuild**, nicht rückwirkend.
  - **`app_server.py`**: `.rcard h2` (Equity/MC-Chart-Karten in Portfolio- UND Developer-Tab) 1:1 auf denselben Mono-`--accent`-Look gezogen wie `report.py`s `h2` — Pflicht laut der bestehenden Sync-Regel, sonst würden Report und Developer-Tab bei den Chart-Köpfen auseinanderdriften. `.devcard h3` (Regelwerk, OOS-Kontrolle, Solo-Frontier, Buch-Beitrag, Kaufplan) bekommt dieselbe Sprache (Mono + `--accent` statt `--text2`), Padding leicht verschärft (14/16px→12/14px). Live im Portfolio-Tab geprüft (Equity-Kurve/Monte-Carlo-Köpfe jetzt orange) — die `.devcard`-Köpfe selbst waren im Preview-Server nicht zu sehen, weil dort gerade ein Backtest lief; reines CSS auf einem unveränderten Selektor, kein neues Strukturrisiko.
  - **Bewusst unverändert:** Chart-Achsen/Grid/Höhen selbst (Regel D), alle `.devcard`-Inhalte/Tabellen (Regelwerk-Text, OOS-Tabelle, Solo-Frontier-Tabelle, Buch-Beitrag-Logik), `devStat()`-Kacheln — nur die Kopf-Farbe ist neu, keine Kachelung.
- Radius ist geklärt (siehe erste Korrekturrunde oben) — bleibt einheitlich 6px im Lab (4px in `report.py`, eigenständiges Dokument mit eigenem `:root`, siehe Abschnitt 3 — das war schon vor dem Bloomberg-Umbau so und ist kein neuer Befund).

---

## 3. Lab-Reports (`reports/*.html`)

Erben die Lab-Tokens (`report.py`, gleicher `:root`-Block). **Regel aus CLAUDE.md:** ändert sich hier etwas an Chart-Defaults, muss es in `lab_ui/lab.css`/`lab.js` (früher `HUB`-Sektion von `app_server.py`) und in `lab_ui/workbench.js` (Kerzen-/Equity-Chart der Workbench) mitgezogen werden — sonst driften Report und Developer-Tab optisch auseinander.

**Struktur seit 30.08.2026 (Max' Vorgabe, gleiches Prinzip wie Portfolio-Tab — Abschnitt 2.F/G):** Titel → Verdict-Karte → Score-Aufschlüsselung (der "Grund") → Equity-Kurve → KPI-Kachel-Zeile (15 Kacheln inkl. Largest Win/Loss, Win/Loss-Streak) sind **permanent sichtbar**. Alles andere — Eval Pass/Blow-Narrativ, Strategie-Anatomie-Erklärung, Regime-Tabellen, Monte-Carlo, Selektions-Ehrlichkeit/DSR/Purged-K-Fold, Parameter-Heatmap, Prop-Firm-Assistant — steckt in `<details><summary>` (Baustein schon vorher im CSS vorhanden, Zeile ~64-70), **alle standardmäßig zu**. Reine Darstellungs-Änderung, keine Zahl wurde neu gerechnet — Daten kommen unverändert aus `copilot.full_report_data()`/`qbt.metrics()`. `qbt.py::metrics()` liefert seit demselben Tag zusätzlich `largest_win_usd`/`largest_loss_usd`/`avg_hold_min` (additiv, nichts Bestehendes geändert).

**Wichtig:** `report.py` ist nur die Vorlage — bestehende `reports/*.html`-Dateien ändern sich erst, wenn sie neu gebaut werden (`run_copilot.validate(...)` bzw. über `funded_finalize.py`/`live_finalize.py`). Ein voller Rebuild läuft pro Report durch die komplette Pipeline (Backtest + MC + DSR + Heatmap + 6-Firmen-Prop-Optimizer) und dauert spürbar (mehrere Minuten je Report) — bei ~100 bestehenden Reports kein Nebenbei-Task. Rebuild eines alten Reports mit aktuellem Engine-Stand kann außerdem dessen Zahlen gegenüber dem historisch geloggten Stand verschieben (siehe Strategie-Logbuch-Fallen wie RV_leadlag_NQES) — vor einem Massen-Rebuild alter/eingefrorener Reports das kurz gegenchecken, nicht blind alle 100 neu bauen.

---

## 4. Neue App anlegen

Neue App = **neuer Abschnitt in dieser Datei, bevor die erste Zeile CSS entsteht**: Zweck, Stil in einem Satz, `:root`-Token-Tabelle, die 3-5 Bausteine (Button, Karte, Tabelle, Kopfzeile, leerer Zustand). Danach gilt sie als Charta und `design-guard` misst daran.

Verwandt: [[Tech-Stack]], [[Schreibstil]]
