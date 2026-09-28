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

**Umsetzung (AP205 = AP202, gebaut 21./22.09.2026, Deploy-Skript `engine/_deploy_consistency/deploy.ps1`):** `MaxRiskGuard.cs` hat `DailyProfitCapFrac` (0 = aus, Default) und `DailyProfitCapMarginUsd` (Default 100). Auslöser = `DailyProfitCapFrac × EvalProfitTarget − Abstand` (FN Flex 50k: 0,40 × 2.500 − 100 = **900 $** Tagesgewinn, alle Beine, realisiert + offen). Dann flatten und für den Rest der Session kein Entry mehr (Nachbrenner alle 30 s), Reset bei der nächsten Session, Stand pro Konto in `maxlab_consistency_<Konto>.txt` (überlebt NT8-Neustart). Werte kommen aus der cfg-Datei `maxlab_riskguard.cfg` (`<konto>.dailyprofitcap`, `<konto>.dailyprofitcapmargin`), die cfg gewinnt vor der UI: FN-Challenge-Konten 71491/89622 → ~~0.40 / 100~~ **seit 24.09.2026: 0.36 / 0** (Entscheidung Max 22.09., 90 % der Kante; 50k löst weiter bei 900 $ aus, FN 150k mit Target 8.000 bei 2.880 $), E8 + FN-Funded → keine Zeile (aus). cfg-Backup `maxlab_riskguard.cfg.bak-20260924`. Live seit 24.09.2026 23:17 (beide Guards neu gestartet, Log bestätigt). Neue Konten: cfg-Block anlegen, dann Instanz neu starten (cfg wird nur beim Start gelesen). Wichtig: gebaut auf der **Box-Fassung** (50.259 B, 09.09.); die Repo-Kopie war veraltet (43.547 B) und darf nie direkt deployt werden.

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

## ⏰ Flat-Zeit & Overnight-Halten (nachgetragen 22.09.2026, Primärquelle FN-Wissensbasis)

| Regel | E8 | FundedNext **Futures** |
|---|---|---|
| Overnight-Halten | offen, nicht geprüft | ❌ **verboten** |
| Wochenend-Halten | offen, nicht geprüft | ❌ **verboten** |
| Zwangs-Flat | offen, nicht geprüft | **15:10 CT** (= 16:10 ET), System-Auto-Close aller offenen Positionen |
| Handel wieder ab | — | 17:00 CT, nach dem Wochenende So 17:00 CT |

Quelle: FundedNext-Wissensbasis, Artikel „Does FundedNext Futures allow overnight and weekend trade holding?" (helpfutures.fundednext.com/en/articles/14268506). **Achtung Verwechslungsgefahr:** für die CFD-/Forex-Konten von FundedNext ist Overnight- und Wochenend-Halten ausdrücklich ERLAUBT (Artikel 11982358). Die Futures-Sparte hat die gegenteilige Regel. Nur die Futures-Regel ist für uns relevant.

**Abgleich mit unserer Umsetzung:** unsere Beine sind alle intraday mit Zwangs-Flat `eod_flat_min=385` (15:55 ET = 14:55 CT), also **75 Minuten vor** dem FN-Auto-Close. Kein Konflikt. Konsequenz für die Strategie-Auswahl: **jedes Mehrtages-/Swing-Bein ist auf FN-Futures strukturell unmöglich**, unabhängig von seiner Edge. Betrifft u. a. den Weg W34 (Mehrtages-Gap-Fill) aus der [[Gap Wege-Karte]] und jede aus Tagesbar-Literatur portierte Strategie.

## 🚫 Verbotene Strategien (nachgetragen 22.09.2026)

| Verbot | E8 | FundedNext Futures |
|---|---|---|
| **Gapped or Illiquid Market Trading** | offen, nicht geprüft | ❌ ausdrücklich verboten |
| Arbitrage (jede Form) | offen | ❌ verboten |
| Strategie-/Risiko-Wechsel nach dem Pass | offen | ❌ verboten |

Wortlaut FN zur Gap-Regel: Orders in „gapped or illiquid market conditions" zu platzieren, um von Preis-Ineffizienzen zu profitieren, sei unzulässig, wegen unvorhersehbarer Ausführung, hoher Slippage und Manipulationsgefahr; ausdrücklich genannt wird Handel in Phasen niedriger Liquidität oder **vor großen Marktereignissen**. Quelle: helpfutures.fundednext.com/en/articles/14298337.

> [!warning] Offene Frage vor jedem Gap-Bein auf FN (22.09.2026)
> Der Wortlaut zielt auf das Ausnutzen dünner Bücher, nicht auf eine reguläre RTH-Order um 09:30 im liquidesten Moment des Tages. Unser historisches Gap-Bein (`RTY_Gap-fade`, Entry nach 10 Min Bestätigung innerhalb RTH) fällt nach dem Sinn der Regel nicht darunter. **Aber:** bevor ein Bein mit „Gap" im Mechanismus auf FN1/FN2 läuft, gehört das schriftlich vom FN-Support bestätigt. Der Name allein kann bei einer Payout-Prüfung Fragen auslösen. Bei E8 ist die Regellage dazu **noch gar nicht geprüft** — nachholen, bevor dort ein Gap-Bein läuft.

## 🔗 Verwandt
- [[Strategie-Logbuch]] — Vorfall 21.09.2026 (falls dort nachgetragen)
- `engine/ninjascript/MaxRiskGuard.cs` — Enforcement
- `engine/_scratch_box_urlaub/1e3478e2/qm/fn_lib.py` — Backtest-seitige Consistency-Rechnung
- [[Gap Wege-Karte]] — betroffen von Flat-Zeit (W34) und Gap-Verbot
