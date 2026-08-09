---
tags:
  - ressource/paper
  - trading/orb
erstellt: 2026-07-05
status: gefunden-zu-analysieren
---
# 📄 ORB Paper-Familie (SSRN)

Gefundene Paper zum **Opening Range Breakout** für [[Trading-Profil|Prop-Firm-Intraday-Index-Trading]]. Analyse via Skill [[paper-edge]].

## Kern-Paper

### 1. Fundament: ORB auf QQQ ⭐
- **Titel:** Can Day Trading Really Be Profitable? Evidence of Sustainable Long-term Profits from Opening Range Breakout (ORB) Day Trading Strategy vs. Benchmark in the US Stock Market
- **Autoren:** Carlo Zarattini, Andrew Aziz (2023)
- **SSRN:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622
- 5-Min ORB, QQQ/TQQQ, 2016-2023, **intraday, kein Overnight**. TQQQ 1484% vs QQQ 169%.

### 2. Verfeinerung: der Retest
- **Titel:** Anatomy of the Retest in the QQQ Opening Range Breakout
- **Autor:** Mario Pineda (2024)
- **SSRN:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6745958
- 1-Min-Daten 2017-2024, zerlegt Opening Range → Breakout → Retest → Outcome. Hilft bei Entry / weniger Fehlausbrüchen.

## Erweiterungen
- **A Profitable Day Trading Strategy For The U.S. Equity Market** (Zarattini, Barbon, Aziz 2024) – ORB auf 7000+ Aktien, „Stocks in Play". SSRN 4729284.
- **Beat the Market: Intraday Momentum Strategy for SPY** (Zarattini, Aziz, Barbon 2024) – SPY intraday, Sharpe 1,33. SSRN 4824172.

## Prop-Firm-Hinweis
Renditen im Fundament-Paper stammen aus **TQQQ (3x) + Compounding** → nicht 1:1 auf Prop-Firm-Trading (NQ/MNQ/QQQ) übertragbar. Signal/Edge aber schon.

## Nächste Schritte
- [ ] PDF(s) besorgen (SSRN-Login, kostenlos) → in `Inbox/` oder `Anhänge/`
- [ ] `/paper-edge` auf Paper 1 laufen lassen (Volltext-Analyse + QuantPad-Spez)
- [ ] Retest-Paper als Entry-Filter einarbeiten
