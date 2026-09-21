---
tags:
  - bereich/trading
  - trading/risk
erstellt: 2026-09-21
---
# ⚖️ Firm-Regeln je Konto

⬅️ [[Eval-Passing]] · [[Funded-Phase]] · [[Live-Setup (Algo auf Prop)]]

> [!important] Warum diese Notiz
> Auslöser 21.09.2026: ein laufender Trade auf den FundedNext-Challenge-Konten stand bei +600-700$ Tagesgewinn. Wäre er bis Handelsende einfach weitergelaufen, hätte das möglicherweise die **Consistency-Rule der FN-Challenge** gerissen — eine Regel, die für E8 gar nicht existiert. `MaxRiskGuard.cs` läuft zwar schon pro Konto als eigene Instanz mit eigenen Werten, aber es gab noch KEIN Property für diese eine Regel. Diese Notiz ist die zentrale Stelle, die sammelt, welche Regel für welche Firma/Phase gilt, damit sowas nicht mehr aus dem Kopf behalten werden muss.

## 🧮 Consistency-Rule (Tagesgewinn-Deckel)

| Firma/Phase | Regel | Konsequenz wenn gerissen |
|---|---|---|
| **E8 (Eval + Funded)** | keine Consistency-Rule | — |
| **FundedNext — Challenge** | Tagesgewinn ≤ **40%** des `EvalProfitTarget` | Überschuss zählt nicht zur Passquote / gefährdet den Pass |
| **FundedNext — Funded** | keine Consistency-Rule | — |

Quelle: `fn_lib.py` Kopf-Kommentar (`_scratch_box_urlaub/1e3478e2/qm/fn_lib.py`, `day_cap_frac=0.40`), primärquellenbestätigt lt. Research-Cache-Eintrag vom 21.08.2026 (FN-Käfig-Recherche).

**Umsetzung (AP205 = AP202, gebaut 21./22.09.2026, Deploy-Skript `engine/_deploy_consistency/deploy.ps1`):** `MaxRiskGuard.cs` hat `DailyProfitCapFrac` (0 = aus, Default) und `DailyProfitCapMarginUsd` (Default 100). Auslöser = `DailyProfitCapFrac × EvalProfitTarget − Abstand` (FN Flex 50k: 0,40 × 2.500 − 100 = **900 $** Tagesgewinn, alle Beine, realisiert + offen). Dann flatten und für den Rest der Session kein Entry mehr (Nachbrenner alle 30 s), Reset bei der nächsten Session, Stand pro Konto in `maxlab_consistency_<Konto>.txt` (überlebt NT8-Neustart). Werte kommen aus der cfg-Datei `maxlab_riskguard.cfg` (`<konto>.dailyprofitcap`, `<konto>.dailyprofitcapmargin`), die cfg gewinnt vor der UI: FN-Challenge-Konten 71491/89622 → 0.40 / 100, E8 + FN-Funded → keine Zeile (aus). Wichtig: gebaut auf der **Box-Fassung** (50.259 B, 09.09.); die Repo-Kopie war veraltet (43.547 B) und darf nie direkt deployt werden.

> [!warning] Regel Max 22.09.2026: neues Konto oder neue Firma = Regeln prüfen
> Wird ein weiteres Konto gekauft (oder wechselt eines die Phase), werden **vor dem ersten Trade** dessen Regeln geprüft, in die Tabellen unten eingetragen und alles Nötige angepasst (RiskGuard-cfg, Größe, Käfig in `book_state.json`/`cage_policy_lib`, Watchdog). Ablauf steht in der CLAUDE.md unter „Neues Konto oder neue Firma". Checkliste je Konto: Consistency/Tagesgewinn · DD-Typ und Einrasten · News-Regel · Inaktivität · Flat-Zeit · Kontraktlimit · Payout-Regeln · Algo-/VPS-Erlaubnis · Haushaltsgrenze.

**Offener Widerspruch zum Tempo-Plan (21.09.2026, Nacht):** dort steht „Tagesgewinn-Stopp: nicht bauen" (harte Kappung im Trailing-Käfig kostet Zeit bis zum Ziel). Das galt für die Tempo-Optimierung; die FN-Consistency-Rule ist ein anderer Mechanismus (Target-Neuberechnung bei > 40 %). Max hat am 22.09.2026 „FN-Deckel bauen" entschieden. Beim nächsten Tempo-Plan-Lauf (`tempo_plan.py`) den Deckel für FN-Challenge-Konten einrechnen.

## 📋 Weitere bekannte Unterschiede je Firma/Phase (Stand 21.09.2026, unvollständig)

| Regel | E8 | FundedNext |
|---|---|---|
| Algo/Automation erlaubt | ✅ | ✅ (primärquellenbestätigt, Research-Cache 21.08.) |
| DD-Typ | Intraday-Trailing | Intraday (Floating-Equity-Breach) |
| MLL-Einrasten | bei Startbilanz | bei Startbilanz + 100 |
| Reward Share (Funded) | 80% | 95% |
| Auszahlung (Funded) | — | min(50% des aktuellen Kontogewinns, Cap) |
| Gratis-Reset nach 5 Payouts | — (Annahme, nicht belegt) | ❌ **KEIN** Gratis-Reset — Live-Programm, alle Challenge-Konten schließen, Sim-Profit verfällt (Research-Cache 21.09.) |
| Haushaltsgrenze | max. 5 aktive Performance-Konten | 750k inkl. laufender Challenges zählt mit |
| Aktuelle RiskGuard-Werte live | `MaxTrailingDD 2000 · DailyLossLimit 900 · EvalProfitTarget 3000` (Konto E61803453048) | `MaxTrailingDD 1500 · DailyLossLimit 600 · EvalProfitTarget 2500` (Konten FNFTCHMAXIMILIANKHO71491/89622) |

> [!note] Noch nicht eingebaut
> Diese Tabelle ist reine Vault-Doku, nicht maschinenlesbar. Ob sich daraus eine zentrale `firm_rules`-Registry lohnt, die `MaxRiskGuard.cs` UND `cage_policy_lib`/`evaluate_v2` gemeinsam lesen (statt die Werte doppelt in NT8-Properties und Python-Konstanten zu pflegen), ist eine offene Folge-Entscheidung — siehe AP204.

## 🔗 Verwandt
- [[Strategie-Logbuch]] — Vorfall 21.09.2026 (falls dort nachgetragen)
- `engine/ninjascript/MaxRiskGuard.cs` — Enforcement
- `engine/_scratch_box_urlaub/1e3478e2/qm/fn_lib.py` — Backtest-seitige Consistency-Rechnung
