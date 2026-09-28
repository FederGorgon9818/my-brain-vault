---
tags:
  - ressource/paper
  - trading/prop
erstellt: 2026-07-06
---
# 🎯 Prop-Eval-Passing (Fokus)

Neuer Fokus (06.07.2026): **zuerst konstant Funded-Evals bestehen**, dann Funded-Phase. Ziel: **P(pass) ≥ 70-80% in kürzester Zeit.** Siehe [[Trading-Profil]], [[Backtest-Engine]] (Prop Firm Assistant misst P(pass) schon).

## Kern-Mathematik
Eval = **+Target erreichen, bevor Trailing-DD greift**, in begrenzter Zeit (Boundary-Problem). Optimieren auf **P(pass)**, nicht auf Langfrist-Sharpe.
- **Niedriger Drawdown > hohe Rendite.** Kleiner DD = Trailing-DD seltener gerissen.
- **70-80% Pass nachhaltig braucht echte Edge.** Ohne Edge geht P(pass) nur über Bold Play (große Size) hoch, aber Funded-Phase explodiert dann (EV negativ). Bisherige Strategien: 14-16% Pass = zu wenig.
- Optimale **Kontraktgröße** existiert (Size↑ = schneller zum Target UND zur DD).

## Paper (nach Eval-Nutzen)
1. **Pass-First-Pay-Later — Leo Ng (SSRN 6672818):** Deferred-Fee-Modell, Restgebühr erst NACH Bestehen. Senkt Kosten fehlgeschlagener Versuche massiv → verändert EV komplett. 2026 quasi Standard. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6672818
2. **Zarattini "VWAP Holy Grail" (SSRN 4631351):** Sharpe 2,1 bei **nur 9,4% Max DD**. Niedriger DD = starker Eval-Kandidat. Behauptung mit ehrlicher Engine prüfen. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4631351
3. **MaxAI — Huber (SSRN 5761402):** RL/GA Index-Futures, PF 1,07, DD $41k → zu wackelig fürs Eval. Referenz.
4. **Wong (SSRN 6722841):** MC-Stresstest-Methodik.
5. **Neu (28.09.2026):** fünf Preprints von Juli bis Sept. 2026, die Challenges als First-Passage-Problem rechnen (Villahermosa, Lim ×2, Fernández, Hall), dazu die klassische Prop-Trader-Literatur. Übersicht: [[Prop-Firm-Paper (Literaturüberblick)]].

## Plan
- [ ] **Eval-Optimizer** in Prop Firm Assistant bauen: findet pro Strategie die Size/Risiko-Kombi mit max P(pass) + min Tage bis Pass, pro Firm, inkl. PFPL-Kostenmodell.
- [ ] Kandidaten mit **niedrigem DD + hoher Win-Rate** testen (Max nennt Strategien).
- [ ] VWAP Holy Grail ehrlich nachbauen (9,4% DD verifizieren).
