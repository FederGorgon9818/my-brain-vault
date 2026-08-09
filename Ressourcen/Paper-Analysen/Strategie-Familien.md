---
tags:
  - ressource/paper
  - trading/framework
erstellt: 2026-07-14
---
# 👪 Strategie-Familien (die 5)

⬅️ [[Strategie-Katalog]] · [[Strategie-Anatomie (Framework)]] · [[Simplex beats Komplex]]

> [!info] Ordnungsprinzip
> Jede Strategie gehört in **genau eine** von 5 Familien. Das gibt Struktur und zeigt sofort, WIE eine Strategie Geld verdient und welches Profil (Win-Rate / RR) sie hat. Jeder Lab-Report zeigt die Familie oben als Badge.

## Die 5 Familien

### 1. 🟢 Trend Following — „Was sich bewegt, bewegt sich weiter"
- **Merkmale:** What moves keeps moving · **Low Win Rate** · **Big Winners** (RR > 1).
- **Why:** Order-Flow + Trägheit tragen Bewegungen weiter.
- **Unsere:** ORB-Breakout, Intraday-Momentum, Gap-Continuation, VWAP-Trend.

### 2. 🟣 Mean Reversion — „Was sich überdehnt, schnappt zurück"
- **Merkmale:** What stretches / snaps back · Mean reverting · **High Win Rate** · **Small Winners** (RR < 1).
- **Why:** Überdehnung/Illiquidität kehrt zum fairen Wert zurück.
- **Unsere:** ORB-Fade, Gap-Fade / Overnight-Reversal, VWAP-Reversion.

### 3. 🟠 Intraday Bias — „Der Tag hat eine Struktur"
- **Merkmale:** Intraday Buyers · Patterns tied to the Clock · Day of week (oft Trend-Filter + Pullback).
- **Why:** strukturelle Flows zu festen Zeiten (Open-Auktion, MOC, Session-Übergänge).
- **Unsere:** Power-Hour (Nachmittags-Momentum). Ausbaufähig (Wochentag, Time-of-Day).

### 4. 🔵 Swing — „Über mehrere Tage halten"
- **Merkmale:** Multi-Day-Holds, längerer Horizont.
- **Why:** mehrtägige Reaktionen (z.B. PEAD, Post-Event-Drift).
- **Unsere:** KEINE — Prop = intraday only. Kommt in [[Live-Account]].

### 5. 🔴 Relative Value — „Den Spread zwischen zwei korrelierten Assets handeln"
- **Merkmale:** Trade the gap between two correlated assets · **Direction agnostic** / markt-neutral.
- **Why:** temporäre Fehlbewertungen zwischen korrelierten Instrumenten.
- **Unsere:** KEINE — **nächstes Ziel** via Cross-Asset ([[Alpha-Suche]]: VIX/Bonds/DXY, NQ-ES-Spread).

## Wo wir stehen
Aktuell besetzt: **Trend Following, Mean Reversion, Intraday Bias.** Leer: **Swing** (später, Live) und **Relative Value** (nächster Alpha-Schritt). Die zwei leeren Familien sind die Roadmap.
