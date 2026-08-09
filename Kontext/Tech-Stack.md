---
tags:
  - kontext/tech-stack
erstellt: 2026-07-04
---
# 🛠️ Tech-Stack & Präferenzen

## Sprachen, die ich kann
- **Python**
- **Java**
- **SQL**
- **YAML** (ein bisschen)
- Plus alles aus der Ausbildung zum Fachinformatiker Anwendungsentwicklung.

## Will ich noch lernen
- **C++** (für die Zukunft)

## Umgebung
- **OS:** Windows
- **Editor/IDE:** VS Code

## Trading / Backtesting
- **NinjaTrader 8** als Live-Plattform, verbunden über Tradovate (Prop-Konto E8). MultiCharts/PowerLanguage war der ursprüngliche Plan, wurde verworfen zugunsten von NT8 (offiziell prop-firm-unterstützt, robustere Order-Engine).
- Skriptsprache: **NinjaScript (C#)**.
- Backtesting: eigene lokale Python-Engine (`qbt.py`, siehe [[Backtest-Engine]]) statt QuantPad für die Masse der Tests, QuantPad nur noch für Datenexport/Cross-Check.
- Datenquellen: 1-Minuten-Bars NQ/ES/YM/RTY 2016-2026, einmalig aus QuantPad exportiert, lokal gecacht.

> [!note] Für Claude
> Max ist Entwickler. Code direkt liefern, saubere Struktur, keine Grundlagen-Erklärungen nötig. C#-Vorschläge sind ok, da Java-Background den Umstieg leicht macht.
