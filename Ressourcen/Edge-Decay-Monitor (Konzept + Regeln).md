---
tags:
  - ressource/konzept
  - trading/live
erstellt: 2026-07-27
---
# 🧬 Edge-Decay-Monitor: Wann ist eine Edge tot?

⬅️ [[Funded-Phase]] · [[Live-Setup (Algo auf Prop)]] · [[Strategie-Logbuch]]

> [!important] Die Forschungs-Basis
> - **McLean & Pontiff (Journal of Finance 2016):** 97 publizierte Edges untersucht → im Schnitt **−26% out-of-sample, −58% nach Publikation**. Edges sterben durch (a) Statistik-Bias im Backtest und (b) andere Trader, die dieselbe Edge handeln. Stärkste Decays bei den lautesten Edges.
> - **Lopez de Prado (AFML 2018):** Struktur-Brüche sind DER Grund, warum Systeme live sterben. Werkzeug: **CUSUM als Risiko-Overlay** — entkoppelt von der Entry-Logik, steuert nur die Size. Plus Deflated Sharpe gegen Mehrfachtest-Illusionen.
> - Konsequenz: **Eine Edge ist kein Besitz, sondern ein Abo, das gekündigt werden kann.** Man braucht einen objektiven Kündigungs-Detektor, KEIN Bauchgefühl.

## Wie unser Monitor funktioniert (📓 Journal → Edge-Health)

Pro Bein wird die **Live-Performance gegen den Backtest-Erwartungs-Kegel** gehalten:
- Referenz: $-Verteilung der Backtest-Trades (Ø und Streuung je Trade, `edge_ref.json`)
- Nach n Live-Trades: erwartete Summe = Ø·n, Unsicherheit = σ·√n
- **z-Score** = (Ist − Erwartet) / (σ·√n)

**Ampel-Regeln (hart, nicht verhandelbar):**

| Ampel | Bedingung | Aktion |
|---|---|---|
| ⚪ grau | < 10 Live-Trades | warten, kein Urteil |
| 🟢 grün | z ≥ −1,28 (im 80%-Kegel) | Edge intakt, normal weiter |
| 🟡 gelb | −2,33 ≤ z < −1,28 | **Size halbieren**, wöchentlich prüfen |
| 🔴 rot | z < −2,33 (unter 99%-Kegel) | **Bein pausieren.** Re-Validierung durchs volle Discovery-Protokoll (IS/OOS auf frischen Daten). Nur mit neuem OOS-Beweis zurück ins Buch |

Wichtig: Die Ampel misst **Abweichung von der Erwartung**, nicht "Verlust". Ein Bein darf verlieren (37%-Win-Rate-Beine verlieren oft!) — rot wird es erst, wenn es *statistisch schlechter läuft, als sein eigener Backtest je erwarten ließe*.

**Warum kein vorschnelles Killen:** Bei z.B. 30 Trades ist σ·√n groß — normale Pechsträhnen bleiben grün/gelb. Das schützt vor dem teuersten Fehler im Live-Betrieb: gute Beine in normalen Drawdowns zu killen (Barber/Odean: Trader "lernen" meist das Falsche aus kurzen Fenstern).

## Der Weiterentwicklungs-Prozess ab Funded (die "Trading-Fabrik")

**Wöchentlicher Takt:**
1. **Montag:** Edge-Health-Ampeln checken (Journal) + Sim-vs-Backtest-Tracking der Live-Beine
2. **Unter der Woche:** 1 neuer Discovery-Batch pro Woche (Backlog aus [[Alpha-Suche]]/Idea Engine: ToM-Watchlist, OpEx-Momentum-Hypothese, Frequenz-Bein, Cross-Asset) — läuft durchs Standardprotokoll, **Auto-Fit entscheidet über Buchaufnahme** automatisch
3. **Freitag:** Journal-Review (Kalender, Disziplin-Check), Logbuch-Eintrag

**Quartals-Takt:**
- Jedes Buch-Bein durch Walk-Forward-Re-Validierung (letzte 12 Monate als frisches OOS)
- Parameter NICHT nachoptimieren, solange grün (Re-Tuning nur bei gelb/rot mit kausaler Hypothese — sonst ist es Curve-Fitting am lebenden Objekt)
- Kontogrößen/Firmen-Regeln neu scannen (Käfig-Hebel!)

**Ersatzbank-Prinzip:** Validierte Bank-Strategien (Prop-Valide-Tab) sind die Nachrücker. Stirbt ein Bein (rot + Re-Validierung gescheitert), rückt der beste Bank-Kandidat nach (Auto-Fit-Test entscheidet). So bleibt das Buch immer voll besetzt, ohne Panik-Entwicklung.
