---
tags:
  - bereich/trading
  - trading/phase-funded
erstellt: 2026-07-07
aktualisiert: 2026-09-26
---
# 🏦 Phase 2: Funded-Phase, Playbook nach dem Pass

⬅️ [[Eval-Passing]] · ➡️ [[Live-Account]] · ⚖️ [[Firm-Regeln je Konto]] · 🎫 Ticket **AP258** (Checkliste als Ticket in `tasks.json`)

> [!important] Kurzfassung
> **Am Handeln ändert sich im Funded nichts:** gleiche Größe, gleiche Beine, keine Extra-Stopps. Anders werden nur drei Dinge: der **RiskGuard beim Pass**, **wie wir auszahlen** und die **Buchhaltung ab dem ersten Payout**.
> Grundlage: Analyse 25./26.09.2026 (Quant-Team, strategy-auditor, verdict-auditor, research-scout), Zusammenfassung in [[Daily Notes/2026-09-26]] Abschnitt „Eval vs. Funded“.
> Gilt für jeden Pass: E8 50k (läuft), FN1/FN2 (FundedNext Flex 50k), ab 02.10. E8 150k.

---

## 1. Checkliste am Pass-Tag (vor dem ersten Funded-Trade)

### A) Sofort
- [ ] Pass-Mail und Dashboard prüfen: gibt es ein **neues Funded-Konto** (neue Kontonummer)? Funded-Vertrag bzw. KYC abschließen, falls verlangt. Konto-ID, Firma und Größe an Claude geben.
- [ ] **Pass-Zertifikat sichern** (PDF oder Screenshot). Das ist Track Record, also Beweis fürs große Ziel.
- [ ] In NT8 (RDP): Beine und RiskGuard am **alten Challenge-Konto ausschalten**, damit nichts auf ein totes Konto handelt.

### B) RiskGuard am Funded-Konto (RDP, NT8)
- [ ] **EvalProfitTarget im UI auf 0.** Wichtigster Punkt: steht dort ein Wert über 0, macht `MaxRiskGuard.cs` das Konto bei +Target **dauerhaft flat** (Z. 477-493). Die cfg-Datei kann das nicht, sie lehnt target=0 ab (Z. 826). Also im UI umstellen.
- [ ] **MaxTrailingDD** je Tier: E8 50k = 2.000, E8 150k = 4.500, FN Flex 50k = 1.500, FN Flex 150k = 4.000.
- [ ] **DailyLossLimit nie unter 600 $ × k** (k = Micros je Bein). k1-Konten wie bisher (E8 900, FN 600), E8 150k k2 = 1.200 $. 900 $ bei k2 kostete über die volle Historie rund 13 % Drift.
- [ ] **FundedNext Funded: keine Consistency-Zeile** (dailyprofitcap aus). Die 40-%-Regel gilt nur in der Challenge. Den cfg-Block des alten Challenge-Kontos nicht aufs neue Konto kopieren. FN hat am 01.10.2026 schriftlich bestätigt, dass das Abschalten erlaubt ist und kein Strategiewechsel ([[Firm-Regeln je Konto]]).
- [ ] **Telegram:** `TelegramToken` + `TelegramChatId` eintragen (Claude holt die Werte per SSH aus `maxlab_watchdog.json`), sonst schweigt der Guard ohne Fehlermeldung (Vorfall 18.08.).
- [ ] **Beine mit derselben Größe wie in der Eval** aufs neue Konto legen. Keine anderen Beine, nicht „im Funded aggressiver werden“ (Begründung in Abschnitt 2).
- [ ] Claude prüft danach per SSH: CONFIG-Zeile im RiskGuard-Log (target 0, maxdd, dailyloss, Telegram an), Zahl der aktiven Strategien, News-Flat-Einstellung.

### C) Claude zieht nach (kein Klick für Max)
- [ ] `book_state.json`: Konto auf funded setzen (Bestand für `tempo_plan`), `funded_finalize.py` + `inbox_tool.py --push-next`.
- [ ] [[Firm-Regeln je Konto]]: Konto in die Liste, aktive Deckel eintragen.
- [ ] **Kaufrunde prüfen:** ein Pass löst sofort eine Kaufrunde aus (Kaufregel AP214, Deckel 2.500 $ Netto-Auslage).
- [ ] `live-reconciler` auf das neue Konto ansetzen.

---

## 2. So handeln wir im Funded

| Frage | Entscheidung | Warum |
|---|---|---|
| Größer handeln als in der Eval (k3/k4)? | **Nein**, k bleibt gleich | Bei E8 ist die 35-%-Best-Day-Regel skaleninvariant: die Auszahlungen kommen ab k2 nicht schneller (etwa alle 8 Monate), nur der Ruin steigt (12,9 / 24,0 / 31,5 % bei k2/3/4). Im schwachen Szenario sogar 2,7 ± 1,3 Monate langsamer. |
| Eval mit k3, Funded mit k2? | **Nein** (nur bei neuer Gewichtung von #175) | Ist k3 auf Umweg: im Szenario „letzte 3 J ×0,58“ −1,0 ± 1,5 Monate (nicht trennbar von 0) bei +10 pp Plan-Tod. Wiedergänger von [[Strategie-Logbuch]] #130. Regelseitig wäre es laut Sekundärquellen erlaubt. |
| Andere Beine im Funded („zwei Bücher“)? | **Nein** | Alle drei Buch-Beine helfen in beiden Phasen, τ² = 0, selektionskorrigiert kein Gewinn. Update zu #117. |
| Tagesgewinn-Deckel nur im Funded (gegen die 35-%-Regel)? | **Nein** | Die Drift sitzt im rechten Rand, der Deckel kostet so viel Drift wie er Wartezeit spart. |
| Engerer Tagesverlust-Stopp nur im Funded? | **Nein** | Einstiegssperre wirkungslos, 300-400 $/Satz kostet Drift, 600 $/Satz neutral. |
| DailyLossLimit | **600 $ × k**, in Eval und Funded | Einheiten-Regel, kein Phasen-Hebel. |

> [!note] Wo die Zeit wirklich liegt
> Rund 40 % der Zeit bis 50k stecken in der **Eval-Dauer**, nicht im Funded. Kein Funded-Hebel holt mehr als etwa 4 Monate raus. Schneller wird es nur über Sharpe (neue unabhängige Beine), nicht über Funded-Tricks.

---

## 3. Auszahlungen

**Immer am Wochenende anfordern**, nicht während einer Handelssession: der Tagesverlust-Stopp im RiskGuard rechnet mit NetLiq minus Session-Start und kann bei einer Abbuchung in der Session fälschlich alles glattstellen. Wann E8 und FN die Auszahlung genau abbuchen, ist noch offen.

### E8 (Performance-Konto)
- **Politik: sofort abrufen, sobald möglich** (ab 125 $ brutto = 100 $ netto). Später abrufen bringt in der Flotte nichts, der erste E8-Beleg käme 2,5 bis 4,4 Monate später.
- Buffer in Höhe des DD bleibt stehen (50k: 2.000 $, 150k: 4.500 $). Auszahlbar ist erst, was über Startbilanz + Buffer liegt.
- **35-%-Best-Day-Regel** je Zyklus: der beste Tag darf höchstens 35 % des Zyklusgewinns sein, Reset nach jedem Payout. Kein Bust, nur Auszahlungssperre.
- Ab dem 2. Payout zusätzlich **5 Tage mit ≥ 0,3 %** der Kontogröße (50k: 150 $, 150k: 450 $).
- Caps brutto: 50k 1.250 / 1.250 / 2.250 / 2.250 / 3.250 (bestätigt), 150k 3.250 / 3.250 / 4.250 / 4.250 / 5.250 (Sekundärquellen). Split 80 %.
- **Max. 5 Payouts**, danach endet das Konto und es gibt eine Gratis-Challenge derselben Größe.

### FundedNext (Flex Funded)
- **Politik für FN1/FN2: erste Auszahlung erst nach dem Floor-Lock** (50k: Kontogewinn ≥ 1.650 $), danach normal. Grund: laut Help-Artikel setzt die erste Auszahlung das Max-Loss-Limit zurück. Ist das ungünstig gemeint, wäre sofortiges Auszahlen deutlich riskanter. Mit Lock ist man in beiden Lesarten auf der sicheren Seite, Preis etwa 1 Monat später.
- **Den 5. FN-Payout nie nehmen:** er schließt alle FN-Challenge-Konten (Live-Programm, Sim-Profit verfällt). Konto nach dem 4. Payout aufgeben.
- Regeln: 5 Benchmark-Tage (50k ≥ 200 $, 150k ≥ 250 $), mindestens 500 $ Profit je Zyklus, Auszahlung bis 50 % des Profits **seit dem letzten Payout**, Cap je Zyklus 1.500 $ (50k) bzw. 4.000 $ (150k), Mindestabruf 250 $.
- Split: **ungeklärt**, 95 % (Help-Artikel) oder 80 % plus kaufbares 95-%-Add-on (Support-Mail 20.08.). Im Dashboard von FN1/FN2 nachsehen.
- ~~Für ein späteres FN-150k-Konto („erst nach Lock, dann nur volle Caps“): die Richtung trägt (2,7 bis 5,2 Monate schneller bis 50k), die Monate sind aber mit einer falschen Auszahlungsformel im Modell gerechnet.~~ **Neu gerechnet 01.10.2026** (Cloud gegen `trading-data`-Backup, Auszahlungsformel korrigiert, Kalender-Modus wie die Wochenend-Prüfung, aktuelles 3-Bein-Buch, Quant-Team gegengelesen, Dateien `Anhänge/2026-10-01 FN-Tempo/`). Gilt für alle FN-Konten (FN1/FN2 und 150k-Lane):

| FN-Auszahlung im Funded | schneller bis 50k (RMST, IS / ×0,58 / letzte 3 J / letzte 3 J ×0,58) | Plan-Tod (C → Variante, gleiche Spalten) |
|---|---|---|
| sofort, sobald erlaubt (Referenz C) | — | 2,7 / 15,0 / 4,2 / 25,0 % |
| erst ab halbem Cap (50k ≥ 750 $, 150k ≥ 2.000 $), Floor eingerastet | −5,4 / −4,0 / −4,7 / −3,5 Monate | 3,3 / 18,8 / 4,5 / 29,0 % |
| nur volle Caps | −5,9 / −5,6 / −4,9 / −5,0 Monate | 5,2 / 22,5 / 5,8 / 33,8 % |

  Mechanik: Je FN-Konto gibt es höchstens 4 Auszahlungen (die 5. schließt alle Challenges), jeder Slot soll also möglichst viel tragen. Zu langes Warten verzögert aber die Liquidität unter dem 2.500-$-Deckel. Die zusätzlichen Plan-Tode von „nur volle Caps" liegen zu zwei Dritteln in Monat 7 bis 25, also im BOS-Jahr. „Erst nach Floor-Lock" allein bringt nur 0,4 bis 1,7 Monate und ist bei vollen Caps überflüssig. **Empfehlung Quant-Team: halber Cap** (bester Tausch Tempo gegen Plan-Tod). **Entscheidung Max offen.** Nulldrift: 0 % Erreichung in allen Varianten.
- **FN 150k mit k3 statt k2 (AP248):** 1,3 bis 4,8 Monate schneller, im schwachen Regime aber +7 pp Plan-Tod, und dort früh (Monat 13 bis 15). Das ist dasselbe Muster wie #175, spricht also für **k2**.

---

## 4. Was sich beim Pass an den Regeln ändert

| Regel | E8 Eval | E8 Funded | FN Challenge | FN Funded |
|---|---|---|---|---|
| Profit-Target | 6 % (50k 3.000, 150k 9.000) | **keins** | 50k 2.500, 150k 8.000 | **keins** |
| Consistency | keine | **35-%-Best-Day** (nur für Auszahlung) | **40 % Tagesgewinn/Target** | **keine** |
| Qualifikationstage | n/a | ab 2. Payout 5 × ≥ 0,3 % | n/a | 5 Benchmark-Tage je Zyklus |
| Drawdown | EOD-trailing, Bust intraday | gleich, Floor rastet bei Startbilanz ein | intraday | gleich, Floor rastet bei Start + 100 ein |
| Kontraktlimit | 150k: 12 Mini / 120 Micro | gleich | 50k 3/30, 150k 8/80 | gleich |
| Tagesverlust der Firma | n/a | 2-%-Soft-Pause (150k: 3.000 $, Sekundärquelle) | n/a | n/a |
| Größe/Strategie nach dem Pass ändern | n/a | kein Verbot gefunden (Senken laut Sekundärquellen ok) | n/a | kein Verbot im Artikel 14298337 (nur Manuell↔Algo-Wechsel verboten) |

Quellen und Status je Zeile: [[Research-Cache]], Abschnitt „FundedNext/E8: Größen-/Strategie-Wechsel nach dem Pass …“ (26.09.2026) und die E8-Support-Mails vom 18.08.

---

## 5. Geld, Steuer, Beleg
- **Vor dem ersten Payout muss das Gewerbe angemeldet sein** (Plan Okt. 2026): [[Unternehmensgründung Entscheidung]], [[Steuer & Gewerbe (Prop-Payouts)]].
- Jeder Payout ist Betriebseinnahme: Auszahlungsbestätigung an Claude, landet in `Documents\Gewerbe\Belege\2026` + EÜR-CSV (AP36).
- Zertifikate und Payout-Belege sammeln: das ist der Live-Beweis, auf dem Konto, Bonität und später das Produkt aufbauen.
- Ältere Rechnung zu Payout-Tempo und Kaufplan: [[Payout-Plan (Erster Payout + 10k)]] (Stand 24.08., Zielfunktion inzwischen „Zeit bis 50k“).

---

## 6. Offen, bevor der erste Pass kommt
- [ ] **FN-Support-Mail abschicken.** Die drei Fragen unten sind am 01.10.2026 verschickt, als Antwort im Thread „Futures Flex accounts 964331151 / 964331145 …". Antwort ausstehend. Der Entwurf vom 26.09. im [[Research-Cache]] ist damit nicht mehr nötig.
  - "Is the 50 % payout limit calculated on profit since the last payout or on total account profit?"
  - "What exactly happens to the Max Loss Limit with the first payout (does it reset or lock at a fixed level)?"
  - "Does the 5th Performance Reward really close all active Futures Challenge accounts?"
- [ ] **RiskGuard-cfg E8 150k vor dem 02.10.:** dailyloss 1.200, maxdd 4.500, target 9.000 (AP214).
- [ ] **AP203:** RiskGuard beim Statuswechsel automatisch umstellen, dazu Guard-Patches: target=0 in der cfg zulassen, Auszahlungen im Tagesverlust nicht als Verlust zählen, FN-Floor bei Start + 100, News-Flat prüfen (E8 hat laut Support keine News-Regel).
- [ ] **[[Firm-Regeln je Konto]] korrigieren:** Z. 18 (E8-Funded hat die 35-%-Regel), Z. 38 (FN-Split ungeklärt), Z. 39 (Auszahlungsbasis seit letztem Payout), Z. 66 (FN-Verbot „Wechsel nach dem Pass“ nicht belegt).
- [ ] **`tempo_plan`:** FN-Auszahlungsformel fixen (heute in `run_funded_fn`, rechnet 50 % vom ganzen Kontogewinn) und den Marken-Fehler (Messzeitpunkte sind zugleich Kaufzeitpunkte, Z. 405/616). **Gemessen 01.10.:** Allein die Formel macht die Zeit bis 50k um etwa 4 Monate zu optimistisch (Mathematiker, 50 Sims). Zusammen mit dem Eval-Modell sind es 2,6 bis 4,9 Monate je Regime, und das betrifft auch die Wochenend-Prüfung. Eine korrigierte Fassung zum Übernehmen liegt als `run_funded_fn_x(fix=True)` in `Anhänge/2026-10-01 FN-Tempo/fn_tempo_check.py` (bit-gleich bei ausgeschaltetem Fix). FN-Lock und FN-150k-Lane sind damit schon neu gerechnet (siehe Abschnitt 3).
- [ ] Optional, nur falls „Eval k3, Funded k2“ doch gewollt ist: E8-Support-Mail (Entwurf im Research-Cache).

---

## 7. Belege
- [[Strategie-Logbuch]] #117 (erste Funded-Rechnung, E8-Regeln), #130 (k_eval = 3), #144 (Sizing-Trichter), #175 (AP204 auf gemeinsamem Kalender, Start E8 150k k2).
- Scratch-Rechnungen: `engine/_scratch_phase_split/` (k_eval gegen k_funded), `engine/_scratch_funded_policy/` (Auszahlungsschwellen, Deckel, Verluststopp, Zeit-Zerlegung), `engine/_scratch_funded_stat/` (zwei Bücher, Gate-Bias, Power, Gegencheck in `review/`).
- Der Juli-Stand dieser Notiz (Keeper `NQ_ORB_sweet`, „konservativer sizen als in der Eval“) ist überholt.
