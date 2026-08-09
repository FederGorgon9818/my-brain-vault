---
tags:
  - ressource/paper
  - trading/mean-reversion
erstellt: 2026-07-29
ssrn: "4708400"
verdict: NO-GO (Prop-Phase) · vorläufig (Paywall, Proxy-Parameter)
---
# 📄 TSI Mean Reversion — Requejo (SSRN 4708400)

⬅️ [[_Paper-Registry]] · [[Trading-Profil]] · [[Mean-Reversion Paper (High-Winrate Fokus)]] · getestet: `engine/tsi_paper_test.py`

> [!warning] Vorläufige Bewertung
> SSRN blockt Volltext (403, auch PDF-Delivery). Exakte TSI-Schwellen/RSI-Filter des Papers sind **nicht öffentlich**. Test lief mit Standard-TSI(25,13)+Signallinie EMA13 und vorab fixiertem Mini-Grid als Proxy. Quelle-Trigger: Instagram-Reel (alphazone.ai).

## 1. Kernaussage
Daily Mean Reversion auf SPY/QQQ via True Strength Index: TSI-Open/Close-Signale, RSI als Sekundärfilter, Ø 5 Tage Haltedauer, Signale am Close → Ausführung am nächsten Open. 1996-2022, Walk-Forward über 3-Jahres-Fenster (IS 2000-18, OOS 1996-99 + 2019-22).

## 2. Markt & Instrument
SPY/QQQ ETFs → auf NQ/ES Futures grundsätzlich übertragbar (getestet auf unseren RTH-Daten 2016-2026).

## 3. Haltedauer ⚠️ KRITISCHER FILTER
**Ø 5 Tage, Overnight-Holds zwingend** (Close-Signal → Open-Fill). → **Verstößt gegen Muss-Kriterien der Prop-Phase** (Intraday only). Nur eine Intraday-Adaption wäre deploybar — genau die haben wir getestet.

## 4./5. Signal-/Exit-Logik (Proxy, da Paywall)
Long-only: TSI(25,13) < Schwelle {−10, −20} + Cross über Signallinie → Long next Open. Exit: Cross unter Signallinie / TSI > +10 / Zeit-Exit 10d → next Open. RSI(2)<10-Zusatzfilter.

## 6. Eigener Engine-Test (NQ/ES Daily, IS 2016-22 / OOS 2023+, echte Kosten)

| Variante | NQ | ES |
|---|---|---|
| TSI<−10 crossup | IS +1460 / **OOS +1665 pts** (n=21!) | IS +258 / **OOS −518** |
| TSI<−20 crossup | IS −787 / OOS −1909 | IS +365 / OOS n/a (0 Trades) |
| TSI<−20 exit+10 | IS −854 / OOS −3139 | IS +351 / OOS n/a |
| RSI2-Filter | 0 Trades | 0 Trades |

**Zerlegung der einzigen positiven Variante (NQ, TSI<−10):** PnL kommt komplett aus dem **Intraday-Anteil** (+1884/+2006), Overnight-Anteil ist sogar **negativ** (−409/−334). Intraday-only-Adaption: IS PF 1,97 / OOS PF 5,17 — **aber n=21 Trades in 10,5 Jahren = 2/Jahr.**

## 7. Prop-Firm-Check
- Original: ❌ Overnight → disqualifiziert.
- Intraday-Adaption: Stops definierbar, aber **2 Trades/Jahr** tragen nichts zum Eval bei (unser dünnstes Buch-Bein hat 25/Jahr und galt schon als grenzwertig, Logbuch #028).

## 8. Verdict: **NO-GO — nicht deployen**
1. **Nicht robust:** nur 1 von 4 Varianten positiv, nur auf NQ (ES OOS klar negativ). Muster kippt über Instrument & Parameter → klassischer Fragile-Fit.
2. **n=21 Trades** = statistisch nicht unterscheidbar von Glück (OOS-PF 5,17 auf ~9 Trades ist Rauschen).
3. **Frequenz unbrauchbar fürs Eval** (2/Jahr).
4. Paper-Original verletzt Intraday-Constraint; die Übertragung SPY/QQQ-1996-2022 → Futures-2016+ scheitert vermutlich am **toten Overnight-Drift** (NY-Fed-2026-Befund, Logbuch #028) — auf unseren Daten war der Overnight-Anteil des Systems durchweg negativ.

## 9. Was bleibt (Bauanleitung entfällt)
Kein QuantPad-Nachbau. Einziger verwertbarer Gedanke: die Walk-Forward-Methodik (3-Jahres-Fenster) als Validierungs-Muster — haben wir mit IS/OOS-Split aber schon strenger.

## 10. Red Flags
- Paywall → Parameter unreproduzierbar, Praktiker-Autor (kein Peer-Review).
- Instagram-Reel als Vehikel = Marketing-Selektionsbias.
- ETF-Daily-MR 1996-2022 lebt historisch stark von Regimen, die auf modernen Index-Futures (2016+) nachweislich nicht mehr tragen.
