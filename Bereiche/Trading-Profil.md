---
tags:
  - bereich/trading
  - trading/profil
erstellt: 2026-07-05
---
# 🎯 Trading-Profil & Constraints

> [!important] Diese Constraints gelten für JEDE Strategie-Analyse
> Wird vom Skill `paper-edge` gelesen, bevor ein Research Paper bewertet wird.

## Instrumente
- **Fokus: Index.** Nasdaq (NQ Futures / QQQ / NAS100), dazu SPY / SPX / ES.
- Grundsätzlich handelbar: alles. Präferenz liegt klar auf Index-Intraday.

## Aktuelle Phase: Prop Firm
Noch nicht genügend Eigenkapital → Trading läuft über **Prop Firms**.
Daraus ergeben sich harte Anforderungen an jede Strategie:

### Muss-Kriterien (jetzt)
- ✅ **Intraday only** – Positionen werden am selben Tag geschlossen.
- ❌ **Keine Overnight-Holds.**
- ❌ **Keine Multi-Day-Strategien** (z.B. **PEAD**, ~60 Tage Haltedauer → geht aktuell NICHT).
- ✅ Muss zu **Prop-Firm-Regeln** passen: Daily Loss Limit, Max / Trailing Drawdown, ggf. Consistency Rules.
- ✅ Definierte, harte **Stops** (Risk pro Trade begrenzt).

## Spätere Phase: Eigenkapital aufgebaut
Sobald genug eigenes Kapital da ist:
- Dann auch **Swing / Overnight / längere Horizonte** möglich.
- Dann werden auch Multi-Day-Paper (PEAD & Co.) relevant.

## Tools
- **QuantPad** (gekauft, 05.07.2026): Backtesting, Monte Carlo, Drawdown, institutionelle Daten. Siehe [[Backtesting & MultiCharts]].
- Research-Quelle: **SSRN** Papers (und ähnliche).

## Workflow
1. Max gibt ein Research Paper (PDF oder SSRN-Link).
2. Skill [[paper-edge]] analysiert es gegen dieses Profil.
3. Output: gibt es eine plausible, prop-firm-taugliche Edge? Plus Bauanleitung für QuantPad.
