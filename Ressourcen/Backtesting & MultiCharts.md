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
