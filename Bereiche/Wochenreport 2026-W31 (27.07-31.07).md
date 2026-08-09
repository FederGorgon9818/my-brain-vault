---
tags:
  - bereich/trading
  - wochenreport
zeitraum: 2026-07-27 bis 2026-07-31
erstellt: 2026-07-31
---
# 📈 Wochenreport 27.07.–31.07.2026

⬅️ [[Eval-Passing]] · [[Strategie-Logbuch]] · [[Backtest-Engine]]

## 🎯 Big Picture

**Konto (E8 50k Sim101):** NetLiq **100.000 $ → 102.821 $** (Stand 31.07., läuft noch). **+2,8% in 5 Handelstagen**, trotz eines Kill-Switch-Tages. Eval-Ziel Gesamt-PnL 3.000 $ (Auto-Flatten) — davon **~94% erreicht**.

**Buch: 8 → 9 Beine.** Neu: `SCALP_NQ_t0.5_hEOD` (Bein 9, 30.07.) — Scale-Out von Bein 8 mit engerem 0,5R-Target statt 1,0R (Win 81%, PF 1,70). Buch-Passquote 59%→**61% in ~81 Tagen**.

## 💰 Trading-Woche (Live)

| Strategie | PnL (Woche) | Trades |
|---|---:|---:|
| MaxORBBreakoutNQ | +649,00 $ | 2 |
| MaxMomentumNQ | +499,50 $ | 5 |
| MaxORBScalpNQ | +490,50 $ | 2 |
| MaxORBScalpNQ2 | +243,50 $ | 2 |
| MaxPowerHourNQ | +181,00 $ | 8 |
| MaxLeadLagES | −138,75 $ | 1 |
| **Summe** | **+1.924,75 $** | **20** |

> [!warning] Diese Tabelle ist die per-Strategie-Rekonstruktion aus den Order-Logs — vor den Fixes am Donnerstag/Freitag durch Doppel-Instanzen teils verzerrt (s. unten). Die **NetLiq-Zahl oben ist die ehrliche Wahrheit**, nicht diese Summe.

**29.07. Kill-Switch-Tag:** Tages-PnL −954 $, RiskGuard hat korrekt gegriffen und alles geflattet. Danach normal weitergelaufen.

## 🐛 Infrastruktur: die große Baustelle der Woche

Das war der eigentliche Schwerpunkt — nicht neue Strategien, sondern dafür sorgen, dass das Live-System das tut, was der Backtest verspricht.

1. **RiskGuard v2 gebaut + deployed** (#048): Eval-Pass-Auto-Flatten ($3.000-Ziel → alles zu, dauerhaft flat) + News-Flat-Modul (FOMC/CPI/NFP).
2. **Live-Monitor-Bug-Saga (3 Tage, mehrere Schichten):**
   - RiskGuards `Account.Flatten()` loggt nicht über die Order-Objekte der Strategie → Phantom-Positionen im Lab. Fix: eigenes Fill-Log (`maxlab_acct_fills.csv`) + **Ground-Truth-Snapshot** (RiskGuard schreibt jede Bar die echte Broker-Position, App vertraut dem als Wahrheit).
   - Pairing-Bug: neue Entry-Fills wurden fälschlich gegen alte Phantom-Positionen verrechnet → Stale-Regel eingebaut (Beine sind EOD-flat by design, älteres "Offen" = Log-Artefakt).
   - Nebenbei: Live-Cache war durch Variablen-Shadowing komplett kaputt (hat nie gecacht).
3. **NT8-Chart-Hygiene:** Doppel-Instanzen auf mehreren Charts (MaxMomentum, ORBFade, ORBBreakout, AsiaDir liefen zeitweise 2-3× parallel), PowerHour lief auf falschem 24h-Session-Template statt RTH (Trades um 4 Uhr nachts statt nachmittags!). Aufgeräumt auf 1 Instanz/Bein, 3 Charts (MNQ/M2K/MES), alle RTH.
4. **NT8-GUI-Bug entdeckt:** `GetTradingHours()`-NullReferenceException beim Enablen alter Strategien nach Data-Series-Wechsel — reines NT8-internes Problem, nicht unser Code. Fix: Remove + frisch hinzufügen statt Re-Enable.
5. **Erkenntnis:** NT8s „Sync"-Spalte ist **kein verlässlicher Gesundheits-Check** (leer = nicht automatisch gut, hat einen echten Fake-Position-Fall bei Momentum versteckt). Die **Position**-Spalte gegen die Realität ist der einzige verlässliche Check.

## 🎨 Design

Kompletter institutioneller Redesign-Umbau (Bloomberg-Terminal-Stil statt „KI-Look"): Emojis raus, Haarlinien-Panels statt runde Kästen, Monospace-Ziffern, ruhige Palette, vertikale Gridlines in allen Diagrammen (Reports + Live-Charts + Journal). Alle aktiven Reports regeneriert.

## 🔬 Discovery / Research

| Batch | Ergebnis | Verdict |
|---|---|---|
| ORB-Scalp (Max' "kurzes Fenster") | 20 Survivors, alle NQ, bis 87% Win | ✅ **Bein 9 aufgenommen** |
| Pivot Points (echtes Paper nachgebaut) | 47/52 sterben IS, 2 Rausch-Survivors | ❌ NO-GO |
| Flip/Trend (Renko-Proxy, Video-These) | Alle 4 Kandidaten würden Buch-Passquote senken | ❌ NO-GO |
| **Event-Bein (FOMC-Post + OpEx-Mom kombiniert)** | Grade A, 108 Tr., OOS-Edge +25%, 7/7 Robustheits-Grid stabil | 🏦 Bank (Auto-Fit: 61%/81d→82d, zu marginal) |

**Lehre der Woche (Event-Bein):** Zwei Klein-N-Edges kombinieren verbessert die Einzelqualität stark, aber die Auto-Fit-Hürde ist nicht nur Frequenz — der tatsächliche Portfolio-Beitrag (Tage-bis-Pass) muss sich verbessern. Frequenz-Wette allein reicht nicht.

## 📋 Offen für nächste Woche

- **Parameter-Audit:** Live-Defaults (`.cs`-Dateien) gegen Buch-Parameter (`book_state.json`) systematisch abgleichen — Verdacht auf Drift bei PowerHour/Momentum entdeckt, noch nicht verifiziert.
- **M2K/MES-Chart-Hygiene:** gleicher Doppel-Instanz-Check wie bei MNQ, noch nicht gemacht.
- Kandidaten-Backlog: Momentum selektiver (weniger/größere Trades), Intraday Time Series Reversal (SSRN 5807282), Overnight-Intraday Reversal (SSRN 2730304).
- Shell-Feinschliff (Idea-Board, Compare-Tab) im neuen Design-Stil.

## 🏆 Fazit

Trotz einer ganzen Woche „Feuerwehr statt Forschung" ist das Konto **+2,8%** im Plus, das Buch ist jetzt **strukturell sauberer** als je zuvor (Ground-Truth-Snapshot, saubere Chart-Konfiguration, funktionierender Auto-Fit-Prozess), und ein neuntes Bein kam trotzdem dazu. Die gefundenen Bugs waren alle **latent seit Live-Start am 23.07.** — gut, dass sie jetzt raus sind, bevor mehr Kapital dranhängt.
