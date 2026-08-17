---
tags:
  - ressource/trading
  - ressource/backtesting
erstellt: 2026-07-04
---
# 📈 Backtesting & MultiCharts

Sammelstelle für alles rund um eigene Backtesting-Tools, MultiCharts und Trading-Strategien.

## Plattform
- **MultiCharts** als Basis.
- **PowerLanguage** vs **MultiCharts.NET (C#)** siehe Entscheidung unten.
- Idee: eigene **API** an MultiCharts, um Backtests durchzuprobieren.

## Referenzen / Inspiration
- **Delta Trend** (YouTuber): hat eine eigene **Backtesting-Software / Website** gebaut. Als Vorbild/Inspiration für ein eigenes Projekt interessant. *(Name evtl. „Delta Trend" / „Data Trend" – noch verifizieren.)*
- **QuantPad** (https://quantpad.ai) ✅ **GEKAUFT (05.07.2026)**: **AI-IDE fürs Quant Trading** mit eingebauten institutionellen Daten. Hauptwerkzeug für Backtesting.
  - **Daten inklusive:** CME, Nasdaq, NYSE, CBOE. Futures (40+), 8000+ US-Aktien, volle Options Chains + Futures Options, Tick/L1/L2, 8-16 J. Historie.
  - **Features:** Monte Carlo, Drawdown, Risk of Ruin, Regime-Analyse, Prop-Firm-Simulatoren (Topstep/Apex), FRED + SEC EDGAR, Multi-DSL (PineScript, NinjaScript).
  - **Python-Zugang:** `import quantpad_data` (ob nur in ihrer Cloud oder lokal = offen).
  - **Eigener AI-Agent** eingebaut (Überschneidung mit Claude).

## Entscheidung: Build vs Buy (04.07.2026)
Kernfrage ist die **Datenverfügbarkeit** (Max hat keine CME/Nasdaq-Anbindung):

- **Options / IV-Strategien → KAUFEN.** Historische Options-Daten (Chains, Greeks, IV) sind teuer & aufwendig. Eigene Pipeline lohnt sich für Einzelperson kaum. Tools: QuantPath, OptionOmega, ORATS, Option Alpha. Datenanbieter: ORATS, CBOE DataShop, Polygon, Databento.
- **Preisbasierte Strategien (ORB, Momentum, Paper-Checks auf Aktien/Futures) → SELBST in Python.** Daten billig/gratis (Polygon, Databento, stooq). Volle Kontrolle, günstig.

**Wichtig:**
- **Monte Carlo** muss man NICHT kaufen → paar Zeilen Python (Trade-Reihenfolge resampeln / Equity bootstrappen).
- **„Über Claude nutzbar"** nur, wenn Tool eine **API** hat. SaaS-UI ohne API = nur manuell. Datenanbieter mit API = ideal, dann eigene Backtests/MC drumherum bauen.

## Verdict QuantPad (04.07.2026): KAUFEN, nicht nachbauen
Der Wert sind **Daten + Infrastruktur**, nicht die Charts/MC (die könnte man selbst in Python). Daten (v.a. Options/IV von CBOE) kann Max als Einzelperson nicht sinnvoll selbst besorgen. QuantPad löst genau das.

**Empfohlene Aufteilung:**
- Options / IV / Monte Carlo / datenintensiv → **QuantPad**
- Preisbasiert (ORB, Momentum, Paper-Checks) → weiter **selbst in Python** (billige Daten)
- **Obsidian + Claude** = zweites Gehirn & Orchestrator drumherum

## Noch zu klären (jetzt genutzt)
- [ ] Läuft `quantpad_data` **lokal** (eigenes VS Code / Claude Code) oder **nur in ihrer Cloud**? → entscheidet, ob ich Daten direkt ziehen kann
- [ ] Dürfen Rohdaten **exportiert** werden oder nur in-platform rechnen?
- [ ] Welche **Strategie-Sprache/Format** erwartet QuantPad (PineScript / NinjaScript / Python)? → damit ich direkt einbaubaren Code liefern kann

## Research-Workflow (Paper → Edge)
Siehe Skill [[paper-edge]] und [[Trading-Profil]]. Max gibt SSRN-Paper, ich prüfe ehrlich auf Edge + baue QuantPad-Spezifikation.

## Entscheidung: Sprache (04.07.2026)
Use Case ist v.a. **Research**: ORB testen, Research Papers auf Edge prüfen, bestehende Strategien nachbauen & statistisch validieren.

**Fahrplan:**
1. **Research in Python** (`pandas` + `vectorbt`/`backtrader`) → schnelle Iteration, Statistik, Plots. Bestes Tool für Edge-Checks.
2. **Gewinner nach MultiCharts.NET (C#) portieren**, wenn Plattform/Live gewünscht. C# passt (Java-Background, eigene App/API-Ziel).
3. **PowerLanguage überspringen**, außer für schnelle simple Chart-Signale.

## Offene Punkte
- [ ] Datenquellen festlegen (MultiCharts-eigene Daten vs. externe API)
- [x] Entscheidung Sprache: Python für Research, C#/.NET für Portierung
- [ ] Delta Trend Projekt genauer anschauen
- [ ] Erste Strategie zum Testen: **Opening Range Breakout (ORB)**

> [!note] Status
> Aktuell **nur gesammelt**. Umsetzung kommt später, erst wird das ganze System / die Ordnerstruktur eingerichtet.

## Verdict (16.08.2026): MultiCharts als Engine erledigt, kein Wechsel
Frage kam wieder auf: eigene Engine gegen MultiCharts tauschen? **Nein.** Die Note oben ist Stand 04.07. und überholt — inzwischen läuft die eigene Engine produktiv mit dem gesamten Entscheidungsapparat (P(funded)-Frontier, Intraday-Bust-Check #077, Betriebspunkt-Paar #089, Buch-Beitrag über 5 Seeds), das ist Custom-Mathe auf Trade-Listen, die MultiCharts nicht liefert. Dazu keine brauchbare API für headless/Sweep-Betrieb (Discovery-Läufe, Subagents), und die Live-Plattform ist ohnehin NT8/Tradovate, nicht MultiCharts (siehe [[Tech-Stack]]). Die Engine ist außerdem schon durch die schmerzhaften Fixes durch (ORB-Look-ahead #066/#067, rv.py-Fix, Real-Fills, OOS-Split) — Vertrauen ist bezahlt, ein Wechsel würfe das weg.

**Einzig sinnvolle Rolle für eine Fremd-Engine:** NT8 Strategy Analyzer als Gegenprobe fürs Fill-Modell des fertigen Live-Codes, nicht als Research-Engine. `mc-coder`-Agent und Skill `multicharts-powerlanguage` sind damit faktisch archiviert.

**Stattdessen (16.08.2026 beschlossen und umgesetzt):** die eigene Engine hat jetzt ein MultiCharts/TradingView-ähnliches **UI** im Developer-Tab des Strategy Lab. Nicht die Engine selbst getauscht, nur die Oberfläche angenähert — Max wollte explizit TradingView-Bedienbarkeit (Zoom/Pan/Crosshair) und MultiCharts/TradingView-Optik, kein eigenes MCP-Tool.

**Umsetzung:**
- **TradingView Lightweight Charts** (Open-Source, Apache-2.0, dieselbe Firma) lokal vendort unter `reports/lightweight-charts.js`, analog zu `reports/chart.min.js`. Kein CDN, kein Freigabe-Antrag nötig — das ist die kostenlose Open-Source-Bibliothek, nicht TradingViews lizenzierte Advanced/Charting Library (die für "wirklich alle" Indikatoren/Zeichentools nötig wäre, siehe Entscheidung oben).
- `developer_run.py::price_chart()` liefert jetzt eine durchgehende Kerzen-Serie (nicht mehr Session-Häppchen mit </>-Navigation) + flache Trade-Liste + VWAP-Indikator (Session-Reset), Zeitstempel als ET-Wandzeit-als-Fake-UTC (Chart-Lib zeigt UTC standardmäßig — Trick spart Timezone-Umrechnung im Frontend).
- Developer-Tab (`app_server.py`): echter Kerzen-Chart mit Entry/Exit-Marken (Pfeilrichtung = Long/Short, Farbe = Gewinn/Verlust, nach MultiCharts-Konvention), VWAP-Linie mit Toggle, native Zoom/Pan/Crosshair. Trade-Liste darunter: Klick springt im Chart zum Trade, Crosshair im Chart highlightet die nächstgelegene Zeile (das stärkste UX-Muster aus der MultiCharts-Recherche).
- Bewusst NICHT gebaut: MFE (nur MAE wird engine-weit getrackt), Zeichentools/weitere Indikatoren über VWAP hinaus.

**Nachgezogen (16.08.2026, gleicher Tag):**
- **Timeframe-Umschalter** (1m/5m/15m/30m/1h): Server liefert jetzt native 1m-Bars + 1m-VWAP, Frontend aggregiert per Klick selbst hoch (`devAggBars()`). Zoom/Pan-Erhalt läuft über die Zeit-Range (nicht Index-Range), damit er einen TF-Wechsel übersteht.
- **SL/TP-Zonen-Box pro Trade** (wie TradingViews Long/Short-Position-Tool: grüne Zone Entry→Target, rote Zone Entry→Stop, mit Preis-/RR-Label). Doch nachgerüstet, anders als am selben Tag noch vermutet: `qbt.py` und die Developer-Versionsdateien berechnen `stop`/`target` ohnehin schon lokal beim Simulieren, nur bisher nicht rausgeschrieben — reines Anreichern des Trade-Dicts um `px_stop`/`px_target` (optionales Feld im Versions-Vertrag, wie `px_in`/`px_out`), keine Änderung an der Kernsimulation. Aktuell nur für Developer-Versionen mit eigener `trades()`-Funktion verdrahtet (Max' normaler Workflow), nicht für die 8 eingebauten `qbt`-Bibliotheksmodi (PARAMS-Pfad, höheres Risiko, geringerer Nutzen — eigene Aufgabe falls gewünscht). Lightweight Charts v4 hat kein eingebautes Rechteck-Werkzeug, darum ein HTML-Overlay über dem Chart-Canvas, positioniert über `priceToCoordinate`/`timeToCoordinate`. Zeigt nur die Zone des angeklickten Trades, nicht alle gleichzeitig.
- Visuelle/interaktive Prüfung (Pan/Zoom, Zonen-Position beim Draggen) über den Sandbox-Browser nicht zu Ende verifizierbar — die Test-Pane war nicht sichtbar/composited, wodurch Chrome `requestAnimationFrame` pausiert (worauf Lightweight Charts fürs Anwenden von Range-Änderungen intern wartet). Datenfluss und DOM-Erzeugung sind bestätigt korrekt (richtige RR-Berechnung, richtige Preise), die optische Positionierung braucht einen echten Blick von Max.
