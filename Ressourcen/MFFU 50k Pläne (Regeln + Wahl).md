---
tags:
  - ressource/propfirm
  - trading/eval
erstellt: 2026-08-04
aktualisiert: 2026-09-28
---
# 🏦 MFFU 50k: Pläne im Vergleich (Screenshots 04.08.2026)

⬅️ [[Live-Setup (Algo auf Prop)]] · [[Eval-Passing]]

> [!warning] ⚠️ Alter Stand (04.08.2026), aktualisiert am 28.09.2026
> Alles ab „Alle 4 Pläne“ ist der Screenshot-Stand vom 04.08. Was davon heute falsch ist, ist durchgestrichen oder mit ⚠️ markiert. **Der aktuelle Stand steht im nächsten Abschnitt.** Quelle: [[Research-Cache]] Abschnitt „MyFundedFutures Re-Check (28.09.2026)“. Achtung: dort nur Such-Snippets (Firmenseiten waren aus der Cloud-Session gesperrt), vor einem Kauf im Checkout und im Help Center gegenlesen.

## ✅ Stand 28.09.2026 (Re-Check)

- **Pläne:** verkauft werden nur noch **Rapid, Rapid EOD (nur 25K/50K), Builder, Pro**. **Flex ist seit 05.08.2026 eingestellt**, Core gibt es auch nicht mehr.
- **Preis:** seit 25.08.2026 für alle neuen Evals **Einmalzahlung**, keine Verlängerung, keine Aktivierungsgebühr. Das Monats-Abo gibt es für Neukäufe nicht mehr. Code **CLUB** 40 bis 50 % nur auf den Erstkauf (Rate schwankt).
- **Kein Static-Plan mehr:** alle vier Pläne trailen (EOD oder intraday).

| Regel | ⚡ Rapid 50K | ⚡ Rapid 150K | 💼 Pro 150K |
|---|---|---|---|
| Listenpreis einmalig | $209 | $463 (mit CLUB ca. $232 bis $278) | $557 |
| Target / Max Loss | $3.000 / $2.000 | $9.000 / $4.500 | $9.000 / $4.500 |
| Eval: DD-Modus | EOD-Trailing | EOD-Trailing | EOD-Trailing |
| **Funded: DD-Modus** | ⚠️ **intraday-trailing** | ⚠️ **intraday-trailing** | ✅ **EOD-Trailing** |
| Daily Loss | keiner | keiner | keiner |
| Consistency | Eval 50 %, Funded keine | Eval 50 %, Funded keine | Eval 50 %, Funded keine |
| Min. Handelstage Eval | 2 | 2 | 2 |
| Payout | täglich, min $500, **90/10**, Buffer $2.100 | täglich, min $500, **90/10**, Buffer $4.600, kein Cap | alle 14 Tage, min $1.000, max 60 % je Payout, 80/20, Buffer $4.600 |
| Live-Wechsel | automatisch bei $10.000 Netto an einem Tag | automatisch bei $10.000 Netto an einem Tag | Review nach 3 Payouts oder $20.000 |

- **Builder** (100K/150K): Eval in 1 Tag möglich, weiches Daily Loss ($1.750 / $2.500, pausiert nur), Payout-Cap $3.000 / $4.500, max. 5 Payouts, nur ein Builder-Funded-Konto je Person.
- **Für alle Pläne:** max. 10 Evals gleichzeitig. Sobald ein 100K- oder 150K-Funded dabei ist, max. **3 Sim-Funded** insgesamt. **7 Kalendertage ohne Trade** und das Konto kann geschlossen werden. Auto-Close 16:10 ET. T1-News im Sim-Funded flat (±2 Min). **Live-Wechsel ist nicht ablehnbar**, sobald man ausgewählt wird (bis $5.000 gehen in eine Reserve).
- **Algo und VPS:** Support-Mail vom 27.07.2026 (Stephanie, Mensch): keine IP-Beschränkung, VPS erlaubt, Algo auf allen Plänen und Stufen (Eval, Sim-Funded, Live) erlaubt, kein HFT, keine Sim-Fill-Exploits. **Aber:** unsere Anfrage beschrieb damals „actively supervising remotely via phone“. **Ob unbeaufsichtigter Betrieb erlaubt ist, ist offen**, mehrere Drittquellen sagen „kein Set-and-forget“. Sammel-Anfrage am 28.09.2026 verschickt, Antwort nach 8 Min (Psalm): **VPS ohne Einschränkung, solange man kein Gerät mit anderen Tradern teilt, Deutschland ok. Die Frage „unbeaufsichtigt ja/nein“ hat er nur mit dem Fair-Play-Textbaustein beantwortet, also weiter offen.** Nachfrage mit Bitte um klares Ja/Nein am 28.09. verschickt: wieder nur Textbaustein (Nihar), Ticket geschlossen. Dritte Mail mit reiner Ja/Nein-Frage am 29.09.: ✅ **„Yes it is allowed provided it can be intervened by the user and managed.“** (Oliver, 29.09.2026). **Unbeaufsichtigter Box-Betrieb ist damit schriftlich erlaubt**, Bedingung: eingreifen können (RiskGuard + Telegram + Fernzugriff). Mail als Beleg aufheben.
- **Neu aus der Support-Antwort 28.09.:** Rapid-Funded-Intraday-Trailing zählt **offene Gewinne mit** (jeder Zwischenhoch zieht den Floor hoch). EOD-Floor rastet bei Start + 100 $ ein, sobald die Tagesschluss-Balance Start + DD + 100 $ erreicht (150K: 154.600 $ → 150.100 $). Max. **10 Konten insgesamt** (Eval + Funded zusammen). News im Rapid/Pro-Funded: **keine Positionen und keine Orders** ±2 Min um FOMC, FOMC-Minutes, NFP, CPI (Energie zusätzlich EIA). Eval-Consistency: bester Tag × 2 wird das neue Ziel, kein Fail. NT8 nur über Tradovate (Rithmic für NT8 gesperrt).
- **Kontakt:** support@myfundedfutures.com funktioniert (läuft über Intercom, Antwort am 27.07. nach 7 Minuten).

## 🧮 Rechnung: MFFU Pro 150K als dritte Firma (29.09.2026)

Kalender-Modus, Gerüst vom Bulenox-Check (`engine/_scratch_mffu_2909/`, golden() bitgleich zu `tempo_plan`), Buch-Fingerprint a4dd9e28, 5 Regime × 3 Seeds × 250 Welten, gepaart gegen AP204 (E8 150k k2 + FN 150k k2, Deckel 2.500 $). Kernel geprüft von `quant-mathematician`, Auswertung `quant-statistician` (90 %-CI, Seed-stratifizierter Bootstrap). dRMST in Monaten bis 50k, negativ = schneller.

| Variante | IS | letzte 3 J ×0,58 | ganze Historie ×0,58 | Plan-Tod IS |
|---|---|---|---|---|
| **Hauptfall** (Keep-alive-Trade gebaut, Buffer bleibt stehen, Live-Wechsel beendet die MFFU-Konten) | **+1,3 [+0,6; +2,1]** | +1,4 | 0,0 [−0,5; +0,6] | 3,2 → 10,9 % |
| Payout „loose“ (Buffer darf mit raus) | −2,0 | −1,3 | −2,2 | 10,8 % |
| Live beendet die Konten NICHT | −4,6 | −4,3 | −4,6 | 10,8 % |
| CLUB 50 % auf die ersten 4 Käufe | −1,8 | −1,5 | −1,2 | 4,7 % |
| ohne Keep-alive (7-Tage-Inaktivität greift) | +12,6 | +9,6 | +5,9 | 13,6 % |
| MFFU statt FN | +14,3 | +9,8 | +6,7 | 5,1 % |
| Referenz: alte Annahme „FN-ähnliche Drittfirma“ | −7,6 | −6,4 | −5,2 | 4,5 % |

- **Urteil (29.09.):** Im Hauptfall bringt MFFU Pro **keine Zeit** und hebt den Plan-Tod um 8 bis 20 pp. Ein Plus gibt es nur unter Zusatzannahmen (Live beendet nichts, Rabatt auf 4 Käufe, lockere Payout-Lesart), und selbst dann bleibt es hinter einer FN-ähnlichen Drittfirma. Nulldrift-Kontrolle bestanden (0 % Erreichung ohne Edge).
- **Warum so schwach:** Eval braucht bei k2 im Median rund 14,6 Monate, erster Payout 7 bis 9 Monate danach, und nach dem 3. Payout droht der Live-Wechsel, der alle Sim-Konten stilllegt. Ohne Keep-alive-Trade töten die 2 bis 3 Buch-Lücken pro Jahr (≥ 7 Tage ohne Trade) fast jede Eval.
- **Was es kippen könnte:** Live-Regeln aus der Primärquelle (größter Hebel, rund 6 Monate), Payout-Lesart (rund 3 Monate), CLUB-Rabatt-Details, Erlaubnis für einen Keep-alive-Trade. Nicht gerechnet: News-Flat ±2 Min im Funded, Kombination CLUB4 + loose.

## ~~Alle 4 Pläne (50k, Target immer $3K, Max DD immer $2K!)~~ Stand 04.08., veraltet

> ⚠️ Preise hier waren **Monats-Abo** (heute Einmalzahlung, siehe oben), **Flex gibt es nicht mehr**, Builder-Regeln haben sich geändert.

| Regel | ⚡ Rapid | 💼 Pro | 🧱 Builder | 🎛️ ~~Flex~~ (eingestellt) |
|---|---|---|---|---|
| **Preis (mit Code)** | ~~**$78.50** (300K)~~ | ~~$113.50 (300K)~~ | ~~$76.50 (BUILDER)~~ | ~~$153 (kein Code)~~ |
| **Eval: DD-Modus** | EOD-Trailing | EOD-Trailing | EOD-Trailing | EOD-Trailing |
| **Eval: Daily DD** | ❌ keiner | ❌ keiner | ⚠️ **$1.000!** | ❌ keiner |
| Eval: Max Position | 5 Kontrakte | 3 | 4 | 3 |
| Eval: Micro-Scaling | 10:1 ✓ (=50 Micros) | 10:1 ✓ | 10:1 ✓ | 10:1 ✓ |
| **Eval: Consistency** | 50% | 50% | ❌ keine | 50% + min 2 Handelstage |
| **Funded: DD-Modus** | ⚠️ **RealTime (intraday!)** | ✅ **EOD** | EOD | EOD |
| Funded: Daily DD | ❌ | ❌ | $1.000 | ❌ |
| Funded: Consistency | ❌ | ❌ | 50% | ❌ (aber Scaling-Regel ✓) |
| Payout-Takt | **1 Tag** | 14 Tage | 2 Tage | 5 Tage + min $150/Tag-Regel |
| Min. Payout | $500 | $1.000 | $500 (max $2.000) | $500 (max $2.000, 50% requestable) |
| **Profit-Split** | **90%** | 80% | 80% | 80% |
| Buffer vor Payout | $2.1K | $2.1K | $2.1K | keiner (MLL $100 locked nach 1. Payout) |
| Plattform | Tradovate ✓ | Tradovate ✓ | Tradovate ✓ | Tradovate ✓ |

## Unsere ehrlichen Passchancen (6-Bein-Buch, Target $3K / DD $2K EOD-Trailing)

> ⚠️ Rechnung vom 04.08. mit dem damaligen 6-Bein-Buch und alter Engine. Gilt nicht für das heutige Buch (E8 150k k2 wird mit `tempo_plan.py` gerechnet).

| Cushion-Frac | P(pass) | ~Tage |
|--:|--:|--:|
| 0.10 | 58% | ~104 |
| **0.14** | **56%** | **~101** |
| **0.18** | **52%** | **~72** |
| 0.22 | 49% | ~53 |
| 0.26 | 47% | ~40 |

(Die $2.000 DD statt $2.500 kosten ~6-8 Punkte vs. frühere Rechnung. Realität: ~52-56% pro Versuch, über 2-3 Versuche >85% kumulativ.)

## 🆚 UPDATE: Lucid Trading 50k im Vergleich (04.08.2026)

| Regel | MFFU Rapid | **Lucid Flex** | Lucid Pro |
|---|---|---|---|
| Preis | ~~$78.50/**Monat** (läuft weiter!)~~ seit 25.08.: $209 einmalig (Liste) | **einmalig** (~$90-370 je Größe, exakt beim Kauf prüfen) | einmalig |
| Eval: Target / DD | $3K / $2K EOD-Trailing | **$3K / $2K EOD-Trailing (identisch)** | $3K / $2K EOD-Trailing |
| Eval: Daily Loss | ❌ | **❌ keiner** | ⚠️ $1.200 |
| Eval: Consistency | 50% | 50% | ❌ |
| Max Position | 5 Mini / 50 Micro | 4 Mini / 40 Micro | 4 Mini / 40 Micro |
| **Funded: DD-Modus** | ⚠️ **RealTime** | ✅ **EOD-Trailing** | ✅ EOD-Trailing |
| Funded: Consistency | ❌ | **❌ keine** | 40% |
| Split | 90% | 90% | 90% |
| **Algo-Policy** | ~~semi-auto,~~ Algo erlaubt, **Aufsicht unklar** (Anfrage 28.09.) | ✅ **VOLL-Automation explizit erlaubt** (Bots/Copier) | ✅ voll |
| Payout | 1 Tag | 5 separate Tage mit Min-Tagesprofit | ab 3 Handelstagen |

**→ NEUE ENTSCHEIDUNG: Lucid Flex 50k.** Gründe:
1. **Gleiche Eval-Mathematik** wie MFFU Rapid (identische Passchancen: ~52-56% / 72-101d)
2. ~~**Einmalzahlung statt Monats-Abo:** unser Grind dauert 2,5-3,5 Monate → MFFU würde ~$160-275 kosten, Lucid einmal ~$150-190~~ ⚠️ entfällt seit 25.08.2026, MFFU ist jetzt auch Einmalzahlung
3. **Voll-Automation offiziell erlaubt** → Max' Job-Situation (nicht am PC um 15:30) ist bei Lucid regelkonform, bei MFFU (Aufsichtspflicht) ein Graubereich (⚠️ 28.09.: weiter offen, Sammel-Anfrage läuft)
4. **Funded deutlich besser:** EOD-Trailing + KEINE Consistency (MFFU Rapid: RealTime-DD)
5. Kein Daily-Loss-Limit im Eval (Pro und MFFU Builder haben eins → Sim-Mismatch)

**Ehrliche Caveats:** Lucid ist jünger als MFFU (weniger Track-Record = Auszahlungs-Vertrauensrisiko; Reviews zeigen aber laufende Payouts). Vor Kauf auf lucidtrading.com prüfen: exakter 50k-Preis, Aktivierungsgebühr Funded, Min-Handelstage im Eval. Microscalping-Regel (<5s-Trades >50% Profit) betrifft uns nicht (Haltezeit Minuten+).

## ~~ENTSCHEIDUNG: Rapid 50k mit Code "300K" = $78.50~~ (ersetzt durch Lucid Flex, s.o.)

**Warum Rapid:**
1. **Günstigster Preis** (gleichauf mit Builder)
2. **Eval-Regeln = exakt unser simuliertes Regime:** EOD-Trailing, KEIN Daily-DD, 5 Kontrakte (weit über unserem Cap von 14 Micros)
3. Builder ist zwar $2 billiger, hat aber **Daily DD $1.000 = zusätzliche Ruin-Barriere**, die NICHT in unserer Simulation ist → senkt real die Passchance und zwingt den Risk-Guard zu einem harten Tagesstopp. Nicht wert für $2 Ersparnis.
4. ~~Flex: teurer + min $150/Tag-Payout-Regel + nur 3 Kontrakte → nein.~~ (Flex seit 05.08.2026 eingestellt)
5. Pro: $35 teurer für besseres Funded (EOD statt RealTime). Fürs ERSTE Konto nicht nötig — Ziel ist jetzt Eval-Passen.

**Der Rapid-Haken (bewusst akzeptiert):** Funded = RealTime-Trailing-DD (das harte Apex-Modell). Gegenstrategie: **90% Split + 1-Tages-Payouts** = Gewinne sofort rausziehen, Risiko de-risken. Wenn wir funded sind und das Buch läuft, kaufen wir fürs zweite Konto ggf. Pro (EOD-Funded) — Entscheidung dann.

**Addons: KEINE.** (Builder-MaxLoss-Addon irrelevant, Pro's "One Day to Pass" = $4K-Target gegen Consistency-Befreiung ist ein schlechter Tausch für uns — unsere vielen kleinen Tage haben mit 50%-Consistency kein Problem.)

## ⚠️ Für den Risk-Guard zu überwachen (Eval)
1. **Consistency 50%:** kein Einzeltag > 50% des Gesamtprofits beim Pass-Antrag. Guard-Regel: wenn bester Tag > 45% vom Total → Size auf Minimum bis verdünnt.
2. **Max 5 Kontrakte / 50 Micros:** unser Cap 14 Micros → nie relevant, trotzdem hart im Guard verdrahten.
3. DD-Floor $2.000 EOD-Trailing → Cushion-Berechnung im Sizing auf 2.000 stellen (nicht 2.500!).
4. **Neu (28.09.):** 7 Tage ohne Trade schließen das Konto, T1-News im Funded ±2 Min flat, Auto-Close 16:10 ET.
