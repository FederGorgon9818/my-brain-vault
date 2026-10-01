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
| **E8 Eval** | keine Consistency-Rule | — |
| **E8 Funded** | **35-%-Best-Day-Regel**: bester Tag ≤ 35 % des Zyklusgewinns, Reset nach jedem Payout | kein Bust, nur Auszahlungssperre, bis die Regel erfüllt ist. Kein RiskGuard-Deckel nötig ([[Funded-Phase]]) |
| **FundedNext — Challenge** | Tagesgewinn ≤ **40%** des Profit Targets | kein Bust: das **Target steigt auf höchster Tagesgewinn / 0,40** (50k: Tag 1.500 $ → Target 3.750 $) |
| **FundedNext — Funded** | keine Consistency-Rule | — |

Quelle: `fn_lib.py` Kopf-Kommentar (`_scratch_box_urlaub/1e3478e2/qm/fn_lib.py`, `day_cap_frac=0.40`), primärquellenbestätigt lt. Research-Cache-Eintrag vom 21.08.2026 (FN-Käfig-Recherche). **Konsequenz primärquellenbestätigt 29.09.2026** (FN Help Center 14298275 / 14878851 über die FN-Wissensbasis): „New Profit Target = Highest Daily Profit / 40 %", gleiche Formel wie `tempo_plan.run_eval_fn`. Schriftlich bestätigt hatte das der FN-Support schon am 22.09.2026 (Mail an maxlkho4, Thread „Futures accounts: commission breakdown, consistency rule details, inactivity rule"): 40 % strikt gegen das Target, nur in der Challenge, bei Überschreitung weder Breach noch Sperre noch Verzögerung, nur das Target steigt. E8-Best-Day: E8-Support-Mail 18.08.2026 ([[Research-Cache]]). Korrigiert 29.09.: vorher stand hier „E8 (Eval + Funded): keine Consistency-Rule" und als FN-Konsequenz „Überschuss zählt nicht zur Passquote / gefährdet den Pass".

**Umsetzung (AP205 = AP202, gebaut 21./22.09.2026, Deploy-Skript `engine/_deploy_consistency/deploy.ps1`):** `MaxRiskGuard.cs` hat `DailyProfitCapFrac` (0 = aus, Default) und `DailyProfitCapMarginUsd` (Default 100). Auslöser = `DailyProfitCapFrac × EvalProfitTarget − Abstand` (FN Flex 50k: 0,40 × 2.500 − 100 = **900 $** Tagesgewinn, alle Beine, realisiert + offen). Dann flatten und für den Rest der Session kein Entry mehr (Nachbrenner alle 30 s), Reset bei der nächsten Session, Stand pro Konto in `maxlab_consistency_<Konto>.txt` (überlebt NT8-Neustart). Werte kommen aus der cfg-Datei `maxlab_riskguard.cfg` (`<konto>.dailyprofitcap`, `<konto>.dailyprofitcapmargin`), die cfg gewinnt vor der UI: FN-Challenge-Konten 71491/89622 → ~~0.40 / 100~~ **seit 24.09.2026: 0.36 / 0** (Entscheidung Max 22.09., 90 % der Kante; 50k löst weiter bei 900 $ aus, FN 150k mit Target 8.000 bei 2.880 $), E8 + FN-Funded → keine Zeile (aus). cfg-Backup `maxlab_riskguard.cfg.bak-20260924`. Live seit 24.09.2026 23:17 (beide Guards neu gestartet, Log bestätigt). **Entscheidung Max 29.09.2026: auf 0.40 / 0 umstellen**, also Auslöser genau an der Kante (50k 1.000 $, 100k 2.000 $, 150k 3.200 $). Grund: laut Rechnung unten etwas besser als 0,36, und ein Überschießen hebt nur das Target an, einen Bust gibt es nicht. **Auf der Box noch nicht umgestellt**, das läuft über das Sammelticket (PC-Session: cfg ändern, beide FN-Guards neu starten, Log „Deckel 40% x Target 2500 = 1000, Abstand 0" prüfen). Neue Konten: cfg-Block anlegen, dann Instanz neu starten (cfg wird nur beim Start gelesen). Wichtig: gebaut auf der **Box-Fassung** (50.259 B, 09.09.); die Repo-Kopie war veraltet (43.547 B) und darf nie direkt deployt werden.

> [!warning] Regel Max 22.09.2026: neues Konto oder neue Firma = Regeln prüfen
> Wird ein weiteres Konto gekauft (oder wechselt eines die Phase), werden **vor dem ersten Trade** dessen Regeln geprüft, in die Tabellen unten eingetragen und alles Nötige angepasst (RiskGuard-cfg, Größe, Käfig in `book_state.json`/`cage_policy_lib`, Watchdog). Ablauf steht in der CLAUDE.md unter „Neues Konto oder neue Firma". Checkliste je Konto: Consistency/Tagesgewinn · DD-Typ und Einrasten · News-Regel · Inaktivität · Flat-Zeit · Kontraktlimit · Payout-Regeln · Algo-/VPS-Erlaubnis · Haushaltsgrenze.

**Offener Widerspruch zum Tempo-Plan (21.09.2026, Nacht):** dort steht „Tagesgewinn-Stopp: nicht bauen" (harte Kappung im Trailing-Käfig kostet Zeit bis zum Ziel). Das galt für die Tempo-Optimierung; die FN-Consistency-Rule ist ein anderer Mechanismus (Target-Neuberechnung bei > 40 %). Max hat am 22.09.2026 „FN-Deckel bauen" entschieden. ~~Beim nächsten Tempo-Plan-Lauf (`tempo_plan.py`) den Deckel für FN-Challenge-Konten einrechnen.~~ Stand 29.09.: Der Tempo-Plan rechnet die reine 40-%-Regel (`run_eval_fn`), nicht den Deckel. Die Rechnung dazu steht unten.

### 📊 Rechnung 29.09.2026: was Regel und Deckel an der FN-Passquote ändern

Gerechnet in der Cloud-Session gegen das `trading-data`-Backup vom 29.09. Grundlage: aktuelles 3-Bein-Buch, offizieller Kern `cage_policy_lib.run_account` (reproduziert die 81,8 % aus `funded_finalize`), 3 Seeds × 6.000 Pfade, 36 Monate, Block-Bootstrap Ø 10.

Drei Varianten:
- **heute** = ohne Regel (Workbench, Buch-Rechnung)
- **reine Regel** = das Target steigt (so rechnet der Tempo-Plan)
- **Deckel** = live 0,36 × Target, auf Tagesebene gerechnet. Gegen die Trade-Ebene geprüft ergibt das +0,1 pp, ist also konservativ.

Das Quant-Team hat gegengelesen. Die Klammern sind 90-%-CIs aus einem äußeren Block-Bootstrap der Historie.

| Konto | Regime | gesamt: heute → mit Deckel | bis 12 Monate: heute → mit Deckel | reine Regel bis 12 M |
|---|---|---|---|---|
| FN 50k k1 (FN1/FN2) | IS | 81,8 → 80,0 (−1,8 [−3,7; −0,2]) | 66,5 → 63,3 (−3,1 [−6,2; −0,9]) | 60,1 |
| | letzte 3 J ×0,58 | 53,5 → 47,8 (−5,7 [−12,1; −1,2]) | 50,3 → 44,0 | 42,5 |
| FN 150k k2 | IS | 85,8 → 85,1 | 40,9 → 39,1 | 38,1 |
| | letzte 3 J ×0,58 | 60,6 → 58,4 | 39,2 → 35,9 | 35,5 |
| FN 150k k3 | IS | 78,7 → 76,6 | 62,4 → 59,2 | 56,7 |
| | letzte 3 J ×0,58 | 48,4 → 43,7 | 45,5 → 40,3 | 39,2 |

FN 150k k1 ändert sich nicht: Mit 1 Micro je Bein kommen 2.880 $ Tagesgewinn nie vor.

- **Die heutigen FN-Zahlen sind zu hoch**, um 2 pp (IS) bis 6 pp (schwaches Regime). Die Größe ist nur auf etwa Faktor 2 genau. Die Richtung ist dagegen sicher, weil die Variante ohne Regel pfadweise nie schlechter abschneidet.
- **Deckel gegen reine Regel:** Über 36 Monate bestehen mit Deckel 1 bis 3 pp weniger, dafür aber schneller. Innerhalb von 6 Monaten liegt der Deckel in 88 bis 98 % der Bootstrap-Replikate vorn. Die Zeit bis funded mit Nachkauf sinkt bei 50k k1 um 0,7 Monate [−1,5; 0,0], bei 150k k2 ist sie gleich. Für Tempo trägt die Entscheidung vom 22./24.09. also. Der Vorsprung kommt aus der Mechanik (ein gehobenes Target verzögert) und nicht aus Edge: Zu zwei Dritteln steht er auch unter Nulldrift.
- **Dünne Basis:** Alles hängt an 8 Tagen über 900 $ in 10 Jahren. Allein der 11.06.2026 (+1.852 $, danach −1.403 $ in 15 Tagen) macht zwei Drittel der 36-Monats-Deltas aus.
- **Nulldrift:** 21,3 → 17,4 % (50k gesamt). Der Deckel nimmt Glückstreffer raus und erzeugt keine, #106 ist sauber.
- **Mathematiker, entschieden 29.09. (Max: 0,40):** Ein Auslöser bei 0,40 × Target statt 0,36 ist in allen Regimen etwas besser (+0,4 bis +1,4 pp), liegt aber im Rauschen der Historie. Der Guard flattet per Bar-Close-Nachbrenner und hat keine echte Entry-Sperre (`MaxRiskGuard.cs` ab Z. 540). Überschießen bis etwa +300 $ kostet laut Schranken-Rechnung nichts. Die Zahlen in der Tabelle oben gelten für 0,36, bei 0,40 liegen sie um diese +0,4 bis +1,4 pp höher.
- **Regelfrage an FN (Statistiker), beantwortet am 01.10.2026** (FN-Support schriftlich, Thread „Futures Flex accounts 964331151 / 964331145: daily profit stop after passing, consistency day boundary"; die Mails vom 29.09. und vom ersten Versuch am 01.10. kamen nie an):
  - **Deckel aus nach dem Pass ist erlaubt.** Der FundedNext Account hat keine 40-%-Regel, das Abschalten dieses Tagesgewinn-Stopps ist erlaubt und gilt „nicht für sich genommen" als Strategie- oder Risikowechsel. Der Pass-Tag-Schritt „FN Funded ohne Consistency-Zeile" ([[Funded-Phase]], AP258) ist damit abgesichert.
  - **Tagesgrenze:** Der Tagesgewinn wird am Ende des Handelstags gerechnet, nach 17:00 CT. Unsere Beine handeln nur intraday, ein Handelstag bei FN entspricht also einer RiskGuard-Session.
  - **Netto:** Gezählt wird der Gewinn nach Kommissionen und Gebühren, nicht brutto. Der Guard misst über NetLiq ebenfalls netto, damit passen beide Maße zusammen. Der Auslöser bei 0,40 sitzt also wirklich an der FN-Kante. Ein Überschießen durch den Bar-Close-Nachbrenner hebt nur das Target leicht an (laut Mathematiker bis etwa +300 $ ohne Kosten).
- Dateien: `Anhänge/2026-09-29 FN-Consistency/`. Die Umsetzung in Workbench, Buch-Rechnung und Tempo-Plan läuft über das Sammelticket ([[PC-Auftrag Sammelticket FN-Consistency]]).

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
