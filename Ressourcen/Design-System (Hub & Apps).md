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

`C:\Users\maxlk\Projects\trading-data\engine\app_server.py` (`:root` ab Zeile ~598) · Stil: **fast schwarz, Terminal-Ernst, Gold-Akzent**, viel Tabelle und Zahl.

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

---

## 3. Lab-Reports (`reports/*.html`)

Erben die Lab-Tokens (`report.py`, gleicher `:root`-Block). **Regel aus CLAUDE.md:** ändert sich hier etwas an Chart-Defaults, muss es in der `HUB`-Sektion von `app_server.py` mitgezogen werden — sonst driften Report und Developer-Tab optisch auseinander.

**Struktur seit 30.08.2026 (Max' Vorgabe, gleiches Prinzip wie Portfolio-Tab — Abschnitt 2.F/G):** Titel → Verdict-Karte → Score-Aufschlüsselung (der "Grund") → Equity-Kurve → KPI-Kachel-Zeile (15 Kacheln inkl. Largest Win/Loss, Win/Loss-Streak) sind **permanent sichtbar**. Alles andere — Eval Pass/Blow-Narrativ, Strategie-Anatomie-Erklärung, Regime-Tabellen, Monte-Carlo, Selektions-Ehrlichkeit/DSR/Purged-K-Fold, Parameter-Heatmap, Prop-Firm-Assistant — steckt in `<details><summary>` (Baustein schon vorher im CSS vorhanden, Zeile ~64-70), **alle standardmäßig zu**. Reine Darstellungs-Änderung, keine Zahl wurde neu gerechnet — Daten kommen unverändert aus `copilot.full_report_data()`/`qbt.metrics()`. `qbt.py::metrics()` liefert seit demselben Tag zusätzlich `largest_win_usd`/`largest_loss_usd`/`avg_hold_min` (additiv, nichts Bestehendes geändert).

**Wichtig:** `report.py` ist nur die Vorlage — bestehende `reports/*.html`-Dateien ändern sich erst, wenn sie neu gebaut werden (`run_copilot.validate(...)` bzw. über `funded_finalize.py`/`live_finalize.py`). Ein voller Rebuild läuft pro Report durch die komplette Pipeline (Backtest + MC + DSR + Heatmap + 6-Firmen-Prop-Optimizer) und dauert spürbar (mehrere Minuten je Report) — bei ~100 bestehenden Reports kein Nebenbei-Task. Rebuild eines alten Reports mit aktuellem Engine-Stand kann außerdem dessen Zahlen gegenüber dem historisch geloggten Stand verschieben (siehe Strategie-Logbuch-Fallen wie RV_leadlag_NQES) — vor einem Massen-Rebuild alter/eingefrorener Reports das kurz gegenchecken, nicht blind alle 100 neu bauen.

---

## 4. Neue App anlegen

Neue App = **neuer Abschnitt in dieser Datei, bevor die erste Zeile CSS entsteht**: Zweck, Stil in einem Satz, `:root`-Token-Tabelle, die 3-5 Bausteine (Button, Karte, Tabelle, Kopfzeile, leerer Zustand). Danach gilt sie als Charta und `design-guard` misst daran.

Verwandt: [[Tech-Stack]], [[Schreibstil]]
