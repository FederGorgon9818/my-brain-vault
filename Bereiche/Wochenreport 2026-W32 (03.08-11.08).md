---
tags:
  - bereich/trading
  - wochenreport
zeitraum: 2026-08-03 bis 2026-08-11
erstellt: 2026-08-11
---
# 📈 Wochenreport 03.08.–11.08.2026

⬅️ [[Eval-Passing]] · [[Strategie-Logbuch]] · [[Backtest-Engine]]

## 🎯 Big Picture

**Sim-Eval am 03.08. bestanden** (Sim101, Gesamt-PnL +3.026 $, RiskGuard-Auto-Flatten hat gegriffen). Danach Konto-Wechsel auf **Simtestsim2** (ab 04.08.) für die weitere Sim-Phase.

**Das war die Wahrheits-Woche, nicht die Gewinn-Woche.** Der ORB-Look-ahead-Fund (#066) hat das Buch von 9 auf 6 Beine gestutzt, die Bug-Serie #071–#082 hat die Passquoten auf ehrliche Füße gestellt: **43,3% (frac 0.22, EOD-Check) bzw. 34,2% unter der bestätigten E8-Intraday-Mechanik** (#077/#081). Die alten 57–65% haben nie existiert. Dafür ist der **2×25k-Parallelplan (57,0% P(funded)) jetzt regelseitig freigegeben** — E8-Support hat Sizing-Split zwischen zwei eigenen Evals schriftlich erlaubt (#085/AP77).

**Seit 10.08. abends sind alle Strategien bewusst deaktiviert** (🔥 FIREFIGHT: zwei Beine liefen mit falschen Zahlen). Kein Live-Gang vor sauberem Buch + neuem Sim-Abgleich.

## 💰 Live-Woche (Simtestsim2, aus den Fills rekonstruiert)

| Tag | PnL | Trades |
|---|---:|---|
| Mo 04.08. | +1.069,00 $ | Momentum +941, PowerHour +128 |
| Di 05.08. | −146,50 $ | Momentum-Stop −244, PowerHour-Short +97,50 |
| Mi 06.08. | −28,25 $ | Momentum +123, LeadLag-Stop −131,25, PowerHour −20 |
| Do 07.08. | −190,50 $ | Momentum-Stop −194, ORB-Entry sofort gecancelt +3,50 |
| **Summe** | **+703,75 $** | 9 Round-Trips |

**Ab Do 07.08. 15:46 (dt.) ist die Datenlage tot:** letzte Bar in `bars_MNQ.csv` um 09:46 ET, NT8-Prozess am 07.08. 22:22 down, seitdem keine Bars und keine Trades — und der Watchdog hat es nicht als Dauerzustand gemeldet (Alert ohne Datum → AP87). Fr 10.08. + Mo/Di gab es daher ohnehin nichts zu messen; ab 10.08. war zusätzlich FIREFIGHT aktiv.

> [!warning] Equity-Log endet schon am 05.08.
> `maxlab_equity.csv` (weiterhin 2-spaltig, Server mappt Konto über das Fill-Log) hat für 06./07.08. keine EOD-Zeilen mehr, obwohl gehandelt wurde. Vermutlich Teil des NT8-/Feed-Ausfalls — beim Sim-Neustart prüfen, ob der RiskGuard wieder täglich schreibt (und dabei gleich den 3-Spalten-Fix aus #058 mitnehmen).

## 🚦 Ampeln + Edge-Health (Stand 11.08.)

**Keine roten oder gelben Edge-Decay-Ampeln.**

| Bein | Live-Trades | kum. PnL | Erwartung (BT) | z | Status |
|---|---:|---:|---:|---:|---|
| NQ_Momentum | 12 | +2.320,50 $ | ~165 $ | +2,55 | 🟢 über Erwartung |
| NQ_LastHour (PowerHour) | 15 | +1.557,00 $ | ~129 $ | +2,29 | 🟢 über Erwartung |
| NQ_ORB-fade (neuer Limit-Port) | 0 | — | — | — | ⚪ keine Live-Trades |
| RTY_Gap-fade | 0 | — | — | — | ⚪ keine Live-Trades |
| NQ_Asia-Dir-USopen | 0 | — | — | — | ⚪ keine Live-Trades |

Einordnung: z > +2 **nach oben** ist bei n=12–15 vor allem Klein-N-Glück, kein Beweis für mehr Edge — aber eben auch kein Decay. Die roten Alerts in der Glocke sind alle Aufgaben-Spiegelungen (Watchdog, Deploy-Fallen AP84/85, Live-gehen-Kette), keine Edge-Probleme.

## 📓 Sim-vs-Backtest-Abgleich: ehrliches Fazit

**Die 2-Wochen-Sim-Validierung ist de facto zurück auf Null.**

1. Nur 2 von 5 Beinen haben überhaupt Live-Daten, beide über Erwartung (gut, aber Klein-N).
2. 3 von 5 Beinen (inkl. des neuen Fade-Limit-Ports, der genau deswegen validiert werden sollte) haben **0 Live-Trades**.
3. Seit 07.08. keine Daten (Feed/NT8), seit 10.08. bewusst alles aus (FIREFIGHT).
4. Das Buch selbst steht zur Disposition (AP53: 3-Bein- vs. 4-Bein-Zielbuch vs. 5-Bein-Status-quo).

→ **Empfehlung: Sim-Neustart erst NACH der Buch-Entscheidung** (AP52 Split-Half → AP53), sonst validiert man zwei Wochen lang ein Buch, das danach umgebaut wird. Der Abgleich-Zähler startet dann bei Tag 0 mit dem finalen Buch.

## 🔬 Forschung/Infrastruktur der Woche (Kurzfassung, Details im Logbuch)

- **#065–#068:** ORB-Sign-Bug gefixt, **Look-ahead im ORB-Port entdeckt** → 3 Breakout-Beine ehrlich tot, Buch auf 6 Beine, Fade auf ruhende Limits. Zwei Bank-Funde (NOISE_ORB, VIXBAND).
- **#071–#074:** „>50% in <30 Tagen" **mathematisch widerlegt** — P(pass) → DD/(Target+DD), der Käfig deckelt bei ~40–45%, das Buch bewegt max. ±3,5pp. Dafür +8,6pp aus reiner Fehlersuche.
- **#075–#076:** Engine-Audit (7 Bugs, 2 mit Live-Geld-Relevanz) → ehrliche 48,4%/Konto; **2×25k mit Sizing-Split 0,10/0,80 → 57,0%**.
- **#077–#081:** E8-DD-Mechanik schriftlich bestätigt (Floor trailt EOD, Bruch intraday geprüft) → Intraday-Zahlen sind die Wahrheit. IVB endgültig beerdigt (#079, #083 mit Original-Spec).
- **#084:** Erster **kompletter Deploy per SSH** (RiskPerMicro 104, AsiaDir-Fix live), dabei zwei stille Deploy-Fallen gefunden (Staging-Zombies AP84, csproj-Leichen AP85). F5-Handbetrieb ist Geschichte.
- **#085:** AP77 final — Sizing-Split erlaubt, **kein News-Trading-Verbot** bei E8 Signature Futures (NewsFlat bleibt vorerst bewusst an).

## 📋 Offen für nächste Woche (Reihenfolge)

1. **AP52 Split-Half-Test** starten (~10 Min) → entblockt **AP53 Buch-Entscheidung** (das ist DIE Entscheidung).
2. **Box wieder handelsfähig:** NT8/Feed hochbringen (braucht RDP-Anmeldung, AP86), Watchdog-Datum-Fix (AP87), Staging leeren (AP84), csproj-Guard (AP85).
3. Nach Buch-Entscheidung: **Sim-Phase sauber neu starten** (Tag 0, alle Beine mit Live-Trades tracken).
4. Wöchentlicher Discovery-Batch ist fällig (gelbe Ampel) — bewusst hinter AP53 einreihen.
5. E8-Kaufentscheidung (1×50k vs. 2×25k) hängt an AP53 + Betriebspunkt.

## 🏆 Fazit

Null neue Beine, Konto nur +0,7% — und trotzdem die wertvollste Woche des Projekts: **die Zahlen stimmen jetzt.** Look-ahead raus, sieben Engine-Bugs raus, die E8-Mechanik vor dem Kauf geklärt statt danach, der Parallelplan regelseitig freigegeben, und die Box ist komplett fernsteuerbar. Was jetzt noch fehlt, ist eine einzige Entscheidung (AP53) und eine saubere Sim-Phase darauf.
