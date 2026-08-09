---
tags:
  - ressource/paper
  - trading/framework
erstellt: 2026-07-14
---
# 🧩 Strategie-Anatomie (Framework)

⬅️ [[Strategie-Katalog]] · [[Strategie-Logbuch]] · [[Alpha-Suche]]

> [!info] Idee (nach Matty Koni "Institutional Approach" + Lopez de Prado)
> Eine Strategie ist kein Signal, sondern ein **vollständiges, erklärbares Skript**. Jede Strategie im [[Backtest-Engine|Strategy Lab]] zeigt jetzt oben eine „Anatomie", kindgerecht erklärt.

## Die Bausteine jeder Strategie
1. **Einstieg (Entry):** so präzise, dass man es einem Dreijährigen erklären kann.
2. **Stop-Loss:** Verlust pro Trade hart begrenzen.
3. **Take-Profit:** wann Gewinn genommen wird.
4. **Notausgang / Zeit-Exit (Emergency):** wenn weder Stop noch Ziel auslöst → zwangsweise glatt (bei uns: US-Handelsschluss, nie über Nacht). = **Triple-Barrier** (Lopez de Prado).
5. **Positionsgröße (Sizing):** der oft unterschätzte Hebel.
6. **⭐ Das WHY:** warum die Edge existieren SOLLTE. Ohne das halten die anderen vier nicht.

## Recherche: das WHY (warum Strategien funktionieren)
Edges kommen aus zwei Quellen:
- **Strukturell:** Order-Flow-Ungleichgewichte, Liquiditäts-Zwänge, Marktmikrostruktur → wiederholbare Preis-Muster (z.B. ORB-Ausbruch mit Volumen).
- **Verhalten:** Angst, Gier, Panik, Herdenverhalten → systematische, wiederkehrende Anomalien.
- **Lopez de Prado (Kern-Warnung):** Modelle auf NICHT-kausalen Zusammenhängen brechen zusammen, wenn sich die Bedingungen ändern. Ein Backtest allein ist Selbstbetrug ("Pseudo-Mathematics and Financial Charlatanism") — man braucht eine **kausale These VOR dem Test.** Genau darum testen wir jede Idee OOS + fragen nach dem Why.

## Recherche: Position Sizing (der stärkste Hebel nach dem Stop)
- **Van Tharp:** nach dem strikten Stop ist Sizing „die einzige stärkste Kraft, um ein Konto am Leben zu halten". Es bestimmt, ob man sein Ziel erreicht.
- **Kelly / fractional Kelly:** maximiert das geometrische Wachstum, volles Kelly ist zu aggressiv → **Bruchteil davon** nehmen.
- **Ralph Vince, Optimal f:** erweitert Kelly um variable Gewinn-/Verlustgrößen.
- **Wichtig:** Sizing ändert NICHT die Trefferquote, sondern die **Effizienz/Geschwindigkeit** — genau unser Fund: `cushion_frac` (Bruchteil des Puffers zum Drawdown-Limit riskieren) = **dynamischer fractional-Kelly**, akademisch als optimal unter Drawdown-Constraint belegt (Grossman-Zhou 1993, Cvitanić-Karatzas 1994).

## Status
✅ In jeden Lab-Report eingebaut (oben, Sektion „🧩 Strategie-Anatomie"): Typ, Einstieg, Stop, Ziel, Notausgang, Sizing, WHY + Quelle. Modul: `engine/anatomy.py`.

## Quellen
[Lopez de Prado – Causality & Factor Investing](https://rpc.cfainstitute.org/sites/default/files/docs/research-reports/rf_lopezdeprado_causalityprimer_online.pdf) · [4 Forces of Edge](https://ryanswright.substack.com/p/why-trading-edge-exists-and-the-4) · [Ralph Vince – Optimal f](https://bettersystemtrader.com/011-ralph-vince/) · [Kelly vs Optimal f](https://www.quantifiedstrategies.com/kelly-criterion-vs-optimal-f/) · [Triple-Barrier / Time-Exit](https://medium.com/@jpolec_72972/stop-loss-take-profit-triple-barrier-time-exit-advanced-strategies-for-backtesting-8b51836ec5a2)
