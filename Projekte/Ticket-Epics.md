---
tags:
  - projekt
  - trading
  - epics
datum: 2026-08-10
status: aktiv
zweck: Steuerungsdokument. Jedes Ticket gehört in genau ein Epic. Reihenfolge ist bindend.
---
⬅️ [[Projekte/_Projekte|Projekte]] · [[Eval-Passing]] · [[Strategie-Logbuch]] · [[Day Trading]]

# 🎫 Ticket-Epics: von kaputt zu funded

Angelegt am 10.08.2026, nachdem der Tag sieben Bugs und drei falsche Live-Referenzen freigelegt hat (siehe [[2026-08-10]]). Ziel des Systems: **jederzeit auf einen Blick sehen, was gerade dran ist und was warten muss.**

> [!danger] Aktueller Zustand (10.08.2026, abends)
> **Alle Strategien sind deaktiviert.** Grund: zwei Beine laufen mit falschen Zahlen (`MaxLeadLagES` Edge-Referenz 3,7× zu hoch, `MaxAsiaDirNQ` steigt eine Minute zu spät ein) und der RiskGuard nutzt möglicherweise das kaputte MAE-Maß.
> **Reaktivierung erst, wenn 🔥 FIREFIGHT komplett grün ist.** Nicht vorher, auch nicht "nur ein Bein zum Testen".

---

## Die sechs Epics auf einen Blick

| # | Epic | Tag | Frage, die es beantwortet | Gate |
|---|---|---|---|---|
| 1 | 🔥 **FIREFIGHT** | `#epic/firefight` | Blutet gerade Geld? | jetzt offen |
| 2 | 🧹 **CLEANROOM** | `#epic/cleanroom` | Ist die Engine sauber? | nach FIREFIGHT |
| 3 | 🔬 **GROUNDTRUTH** | `#epic/groundtruth` | Stimmen die Zahlen? | nach CLEANROOM |
| 4 | 🎯 **DIALIN** | `#epic/dialin` | Welches Buch, welcher frac? | nach GROUNDTRUTH |
| 5 | 🏛️ **GATEKEEPER** | `#epic/gatekeeper` | Was erlaubt die Firma? | parallel ab jetzt |
| 6 | 🚀 **LAUNCH** | `#epic/launch` | Rauf aufs echte Konto | nach 1 bis 5 |
| ❄️ | 📈 **ALPHAHUNT** | `#epic/alphahunt` | Neue Beine finden | **eingefroren** |

**Die Kette:** 🔥 → 🧹 → 🔬 → 🎯 → 🚀, mit 🏛️ als Nebenstrang, der jederzeit laufen darf (Support-Antworten dauern).

**Die eine Regel:** 📈 ALPHAHUNT bleibt zu, bis 🔬 GROUNDTRUTH grün ist. Sonst optimieren wir wieder auf Zahlen, die nicht stimmen. Genau das ist heute passiert und hat einen ganzen Tag gekostet.

---

## 🔥 FIREFIGHT
`#epic/firefight` · **Live-Blutungen stoppen**

Alles, was **jetzt gerade** auf echtem oder Sim-Konto mit falschen Zahlen läuft. Keine Verbesserung, keine Forschung, nur Blutstillung.

**Fertig wenn:** kein laufendes Script mehr eine Referenz benutzt, von der wir wissen, dass sie falsch ist.

- [ ] **Alle Strategien deaktiviert lassen**, bis dieses Epic grün ist (Zustand seit 10.08. abends)
- [x] ~~`edge_ref.json`: `MaxLeadLagES` von 34,06 auf 9,12 $/Trade korrigieren~~ ✅ erledigt, aber anders als geplant (11.08., [[Strategie-Logbuch]] #090): keine proportionale Skalierung, Bein komplett aus `edge_ref.json`/`book_state.json` entfernt — Nachrechnung zeigt negativen expR (−0,074), nicht nur einen kleineren positiven Wert
- [ ] `MaxAsiaDirNQ`: Einstieg von 09:31 auf 09:30 fixen (`OnBarClose` im `IsFirstBarOfSession`-Block). Kostet aktuell 36% der Bein-Edge, ca. 271 $/Jahr/Micro
- [ ] Ticket `riskguard-risk-mass`: nutzt der Live-RiskGuard dasselbe MAE-Maß wie `book.cell_daily:43`? Wenn ja, wird live systematisch zu klein gesized
- [ ] Prüfen, ob noch weitere Live-Scripts gegen `edge_ref.json` oder das alte Risikomaß laufen
- [ ] Nach allen Fixes: **ein** Bein reaktivieren, einen Tag beobachten, dann Rest

---

## 🧹 CLEANROOM
`#epic/cleanroom` · **Engine und Daten sauber machen**

Die sieben Bugs von heute sind gefixt, aber nicht abgesichert. Hier geht es darum, dass sie **weg bleiben** und nicht in drei Wochen wieder auftauchen.

**Fertig wenn:** ein Regressionslauf beweist, dass die Engine gegen bekannte Referenzwerte rechnet, und kaputte Daten nicht mehr durchrutschen.

- [x] ~~MAE-Doppelzählung an allen drei Fundstellen verifiziert~~ ✅ 11.08. ([[Strategie-Logbuch]] #082): `book.py:43` war schon korrekt, `qbt.py`/`copilot.py` gefixt und bitidentisch gegengecheckt
- [x] ~~Guard gegen korrupte Kursdaten aktiv und getestet~~ ✅ 11.08. ([[Strategie-Logbuch]] #091): 11 betroffene ES/RTY-Reports vor dem Fix nachgerechnet, nur 2 minimal verändert (leicht besser), keine Strategie kippt
- [x] ~~`rv.py:167`: Risiko-Skalierung mit dem richtigen Instrument (ES statt NQ), Fix verifiziert~~ ✅ verifiziert 11.08. ([[Strategie-Logbuch]] #090): Mechanismus hergeleitet + 16er Robustheits-Sweep, Ergebnis bestätigt tot
- [ ] Slippage nach Ordertyp statt pauschal 2 Ticks (Limit-Entry 0, Target-Exit 0, Market/Stop 1 Tick) — **Achtung (#091): war fälschlich als erledigt markiert.** Nur Einmal-Analyse in `goal_last_push.py`, nie in `qbt.py` integriert. Echt offen, betrifft ORB-fade/ASIA/NOISE/OPEX
- [ ] `passmc`: Horizont in **Kalendertagen** statt Handelstagen, oder zumindest eindeutig benannt
- [ ] **Golden-File-Test bauen:** ein fixer Datensatz, ein fixes Buch, erwartete Kennzahlen eingefroren. Läuft vor jeder Buch-Entscheidung
- [ ] Backups der gefixten Dateien aufräumen, damit klar ist, welche Version gilt

---

## 🔬 GROUNDTRUTH
`#epic/groundtruth` · **Jede Zahl, auf die wir uns verlassen, neu beweisen**

Der teuerste Fund von heute: die Zahlen aus #071 bis #076 standen alle auf dem falschen Bust-Check. Hier wird das ein für alle Mal geradegezogen.

**Fertig wenn:** es genau eine gültige Zahl pro Buch/frac-Kombination gibt, gerechnet mit Intraday-Check auf der gefixten Engine, und der Vault keine widersprüchlichen Altzahlen mehr führt.

- [ ] **`dd_mode="intraday"` als Default** überall, wo bisher EOD gerechnet wurde ([[Strategie-Logbuch]] #077)
- [x] Ticket `splithalf-validierung` ✅ erledigt 11.08. ([[Strategie-Logbuch]] #088): kein Einbruch im Test, aber Train-only-Suche findet das Zielbuch nicht — 3 von 4 Zielbeinen sucheffekt-verdächtig, nur NOISE_ORB_NQ echt bestätigt. AP53 entblockt
- [ ] Sharpe-Gewichtung statt Gleichgewichtung: gilt der Effekt aus #074 auch auf der gefixten Engine?
- [ ] Alle Passquoten im Vault mit Stand-Marker versehen oder entwerten (57% / 65% / 48,6% sind tot)
- [ ] [[QuantPad Brief - Engine Verification]] rausschicken: Blind-Audit mit den drei Benchmark-Studien, deren ehrliche Ergebnisse wir lokal kennen
- [ ] Tail-Risiko OPEX-Bein: 9 bis 10 Trades/Jahr bei Gewicht 8 im aktuellen Buch. Unter Intraday-DD schärfer als gedacht

---

## 🎯 DIALIN
`#epic/dialin` · **Betriebspunkt und Buch festlegen**

Erst hier wird entschieden, **womit** wir antreten. Vorher ist jede Entscheidung auf Sand gebaut.

**Fertig wenn:** Buch, frac, Kontogröße und Kontenanzahl schriftlich festgelegt sind, mit der ehrlichen Passquote daneben.

- [x] ~~`cushion-size-uebertragung` (AP92)~~ ✅ erledigt 11.08. ([[Strategie-Logbuch]] #092): Cushion-Sizing aus dem RiskGuard an alle 9 Beine übertragen, Size-Datei jetzt pro Konto getrennt (`maxlab_size_<Konto>.txt`), deployed + kompiliert. AP91 entblockt
- [ ] **AP53: Betriebspunkt wählen.** frac 0.10 (Quote hoch, langsam) oder höher (Tempo). #078 und #080 zeigen beide auf **niedrig**
- [ ] MOMSEL-Replace entscheiden (#080). Lohnt nur bei frac ≈ 0.10, dort ca. 25% schneller bei gleicher Quote
- [ ] Ticket `claude-071-buchumbau`: 5 von 6 Beinen raus ist radikal, gehört bewusst entschieden
- [ ] Kontogröße festlegen (10k / 25k / 50k). Nach #073 macht der Käfig den Unterschied, nicht das Buch
- [ ] Ein Konto oder zwei mit Sizing-Split? Hängt an `e8-zwei-konten` aus 🏛️ GATEKEEPER
- [ ] Ergebnis als **eine** Zeile ins Logbuch: Buch, frac, Größe, P(funded), Tage, Kosten

---

## 🏛️ GATEKEEPER
`#epic/gatekeeper` · **Firma, Regelwerk, Papierkram**

Alles, was von außen entschieden wird und deshalb Vorlauf braucht. Darf **parallel** zu allen anderen Epics laufen, weil Support-Antworten dauern.

**Fertig wenn:** die Eval gekauft ist und wir jede Regel kennen, die unser Setup betrifft.

- [x] ~~`e8-dd-mechanik`~~ ✅ geklärt 10.08. (#077): Floor trailt EOD, Bruch wird kontinuierlich geprüft
- [x] ~~`e8-zwei-konten`~~ ✅ geklärt 11.08. (#085, AP77): Sizing-Split zwischen zwei gleichzeitigen Evals erlaubt (Support-Bestätigung Fábio), 57% aus #076 buchbar. Nebenbefund: kein News-Trading-Verbot bei E8 Signature Futures
- [x] ~~`e8-eval-zeitlimit` (AP90)~~ ✅ geklärt 11.08. (#093): kein Zeit-/Tageslimit für die Evaluation, nur eine Wochen-Inaktivitätsregel (Futures: 1 Trade auf+zu pro Woche, ab 0,1 Lot genügt)
- [ ] **`e8-heartbeat-bein` (AP93):** dediziertes Mini-Bein (1 Lot/Woche auf+zu) statt Einzelbein-Audit, um die Wochen-Inaktivitätsregel sicher zu erfüllen — Idee Max 11.08., erst E8 kurz bestätigen lassen
- [ ] **`e8-kontraktlimits`:** Sim nimmt Cap 14 Micros an. Stimmt das auf dem gewählten Konto?
- [ ] VPS-Regel bei E8 schriftlich bestätigen (Bulenox ist genau daran gestorben, Ticket #RAX-292098)
- [ ] Eval kaufen, erst nach 🎯 DIALIN
- [ ] [[Steuer & Gewerbe (Prop-Payouts)]] durchgehen, bevor der erste Payout kommt

---

## 🚀 LAUNCH
`#epic/launch` · **Rauf aufs echte Konto**

**Fertig wenn:** das entschiedene Buch auf dem gekauften Konto läuft und täglich gegen den Backtest abgeglichen wird.

- [ ] NT8-Scripts für das finale Buch deployen ([[Live-Setup (Algo auf Prop)]])
- [ ] Kill-Switch und Notaus testen, **bevor** echtes Geld drauf ist
- [ ] Tägliche Abgleich-Routine: Live-Fill gegen Backtest-Fill, Abweichung > X sofort sichtbar
- [ ] `edge_ref.json` als Referenz aktuell halten (siehe 🔥 FIREFIGHT, sonst wiederholt sich der Fehler)
- [ ] Startchecklist schreiben und einmal trocken durchgehen

---

## ❄️ ALPHAHUNT (eingefroren)
`#epic/alphahunt` · **Neue Beine, bessere Beine**

**Auftauen erst, wenn 🔬 GROUNDTRUTH grün ist.** Bis dahin landen neue Ideen hier und werden nicht gerechnet.

- [ ] `OR_DELTA_BIAS_NQ`: liegt als `engine/or_delta.py` bereit. Statistisch sauber, verbessert die Frontier aktuell nicht (#079). Bei anderem Sizing-Modell nochmal prüfen
- [ ] Offene Kandidaten aus [[Strategie-Logbuch]] (Overnight-Intraday-Reversal SSRN 2730304 etc.)
- [ ] Orderflow-Daten aus dem v2-Export auswerten, sobald sie durch sind

---

## 📋 Alle Tickets (Sidebar-Ansicht)

Flache Liste, wie die linke Spalte im Tracker. Jede Zeile: Status, Name, Epic-Tag, wofür es zuständig ist. Rekonstruiert aus allem, was im Vault dokumentiert ist ([[Strategie-Logbuch]], Daily Notes) — **der Tracker auf der Box hat 29 Tickets, hier stehen die namentlich dokumentierten.** Rest siehe „Noch nicht zugeordnet" unten, morgen im Tracker selbst abgleichen und Tag setzen.

### 🔥 firefight
| Status | Ticket | Wofür |
|---|---|---|
| ✅ erledigt 11.08. | ~~`edge-ref-leadlag-korrektur`~~ | Anders als geplant: Bein komplett aus `edge_ref.json` entfernt statt auf 9,12 $/Trade skaliert ([[Strategie-Logbuch]] #090) |
| ✅ gelöscht 11.08. | ~~`asiadir-entry-fix` (AP72)~~ | Einstieg 09:31 → 09:30, deployed und kompiliert ([[Strategie-Logbuch]] #084) |
| 🔴 offen | `riskguard-risk-mass` | Prüfen ob Live-RiskGuard dasselbe kaputte MAE-Maß nutzt wie `book.cell_daily` |
| 🔴 offen | `riskguard-historical-replay-guard-f5` | `State.Historical`-Guard fürs RiskGuard-C#, wartet auf F5 |
| ✅ erledigt 11.08. | ~~`f5-compile-fenster` / AP83~~ | **F5 ist tot.** Deploy läuft extern per SSH + `box_deploy.ps1`, kein Kompilier-Fenster mehr nötig |
| 🟡 halb erledigt | `AP78` | RiskPerMicro 80 → **104 ist live**. Offen nur noch: `MaxLeadLagES` bei der Reaktivierung nicht anhaken |
| 🔴 offen | `AP84` box-deploy-staging-leeren | Staging enthielt 3 gelöschte Beine — der nächste Deploy hätte sie wiederbelebt |
| 🔴 offen | `AP85` box-deploy-csproj-guard | `box_deploy.ps1` löscht obj/bin und lässt die csproj-Referenzen stehen → nächster Build stirbt mit CS2001 |
| 🟠 offen | `AP86` nt8-restart-haengt-nach-kill | NT8 kommt nach hartem Kill nicht bis zum Control Center, braucht einen Klick am RDP |
| 🟡 offen | `AP87` watchdog-alert-datum | Alert ohne Datum, loggt danach „ok" obwohl das Problem weiterläuft |

### 🧹 cleanroom
| Status | Ticket | Wofür |
|---|---|---|
| ✅ verifiziert 11.08. (#082) | `mae-doppelzaehlung-verify` | Fix an drei Stellen gegengecheckt: `book.py:43` war schon korrekt, `qbt.py`/`copilot.py` gefixt, bitidentische Werte |
| ✅ verifiziert 11.08. (#091) | `corrupt-data-guard-verify` | 11 ES/RTY-Reports vor dem Fix nachgerechnet: nur 2 minimal (RTY_Gap-fade, VWAPPULL_RTY leicht besser), keine tot |
| ✅ verifiziert 11.08. (#090) | `rv-instrument-scaling-verify` | `rv.py:167` ES-statt-NQ-Skalierung gegengecheckt: Mechanismus hergeleitet, 16er Sweep bestätigt tot |
| 🟡 **Status falsch, korrigiert 11.08. (#091)** | `slippage-ordertyp` | War NIE in `qbt.py` integriert — nur Einmal-Analyse in `goal_last_push.py`. Jeder normale `run_strategy()`-Call (inkl. alle Reports und `live_finalize.py`) rechnet noch pauschal 2 Ticks. Echtes Ticket bleibt offen |
| 🔴 offen | `passmc-kalender-horizont` | Horizont von Handelstagen auf Kalendertage umstellen (einer der 3 roten aus #076) |
| 🟡 offen, neu | `golden-file-test` | Fixer Datensatz + erwartete Kennzahlen, läuft vor jeder Buch-Entscheidung |
| 🔴 offen, neu (#091) | `slippage-ordertyp-integration` | `entry_slip_ticks`/`exit_slip_ticks` echt in `qbt.py::run_strategy` einbauen (bisher nur Analyse-Skript). Betrifft v.a. Limit-Entry/Target-Exit-Beine (ORB-fade, ASIA, NOISE, OPEX) |

### 🔬 groundtruth
| Status | Ticket | Wofür |
|---|---|---|
| ✅ erledigt 11.08. (#088) | `splithalf-validierung` | Zielbuch-Herkunft widerlegt: Train-only-Suche findet nur NOISE_ORB_NQ, AP53 entblockt |
| 🟡 offen | `dd-mode-intraday-default` | Intraday-Check als Default überall, wo bisher EOD lief |
| 🟡 offen | `sharpe-gewichtung-verify` | Gilt der #074-Gewichtungseffekt auch auf der gefixten Engine? |
| 🟡 offen | `alte-passquoten-entwerten` | 57%/65%/48,6% im Vault als überholt markieren |
| 🟡 offen | `quantpad-blind-audit-senden` | [[QuantPad Brief - Engine Verification]] ist geschrieben, noch nicht raus |
| 🟢 beobachten | `opex-tail-risiko` | Nur 9-10 Trades/Jahr bei Gewicht 8, unter Intraday-DD schärfer |

### 🎯 dialin
| Status | Ticket | Wofür |
|---|---|---|
| 🔴 offen, **zentral** | `AP53` | Betriebspunkt: frac 0.10 (Quote) oder höher (Tempo) |
| 🟡 offen | `momsel-replace-entscheidung` | Nur bei frac ≈0.10 sinnvoll (#080), hängt an AP53 |
| 🟡 offen | `buch-umbau-071` / `claude-071-buchumbau` *(vermutlich dasselbe Ticket, zwei Namen im Vault)* | 5 von 6 Beinen raus, radikal, bewusst entscheiden |
| ⚪ vermutlich überholt | `buch-entscheidung-070` | Vorläufer von `buch-umbau-071`, seit #071 vermutlich erledigt/ersetzt — morgen prüfen |
| 🟡 offen | `kontogroesse-festlegen` | 10k / 25k / 50k, hängt an AP53 |
| 🟡 offen | `ein-oder-zwei-konten` | `e8-zwei-konten`-Blocker seit 11.08. weg (#083), hängt jetzt nur noch an AP53 |

### 🏛️ gatekeeper
| Status | Ticket | Wofür |
|---|---|---|
| ✅ geschlossen 10.08. | `e8-dd-mechanik` (AP51) | E8-DD-Mechanik schriftlich geklärt (#077) |
| ✅ geschlossen 11.08. | `e8-zwei-konten` / AP77 | Sizing-Split zwischen zwei gleichzeitigen Evals erlaubt (Support Fábio), kein News-Trading-Verbot bei Signature Futures. Details: [[E8-Support-Anfrage (Sizing-Split + News-Fenster)]], [[Strategie-Logbuch]] #085 |
| 🔴 offen | `e8-kontraktlimits` | Cap 14 Micros auf dem 50k stimmt das? |
| ✅ geschlossen | `rax-292098` | Bulenox: VPS strikt verboten → Bulenox damit tot |
| ✅ geschlossen | `w8ben-check-e8` | W-8BEN läuft automatisch über WorkMarket/Riseworks beim Payout |
| 🟢 offen, kein Zeitdruck | `w8ben-onboarding-beim-payout` | Reminder für den ersten echten Payout-Request |
| ⚪ offen, blockiert | `eval-kaufen` | Erst nach 🎯 dialin |
| 🟡 offen | `steuer-gewerbe-check` | [[Steuer & Gewerbe (Prop-Payouts)]] vor erstem Payout durchgehen |

### 🚀 launch
Noch keine Tickets angelegt — entstehen erst, wenn 🎯 dialin steht. Siehe Checkliste im Epic oben.

### ❄️ alphahunt (eingefroren)
| Status | Ticket | Wofür |
|---|---|---|
| ✅ gelöscht (No-Go) | `AP82` | OR-Delta-Bias-Bein-Aufnahme, verbessert Frontier nicht (#079) |
| 🟡 eingefroren | `or-delta-bias-sizing-retest` | Bei anderem Sizing-Modell nochmal prüfen |
| 🟡 eingefroren | `overnight-intraday-reversal-ssrn` | SSRN 2730304, noch offen |
| 🟡 eingefroren | `orderflow-v2-auswertung` | Wartet auf den laufenden Datenexport |

### ⚪ Noch nicht zugeordnet
Alte Einträge aus dem Lab-Startbestand (29.07.), Status unbekannt — möglich, dass einige längst erledigt sind. Morgen im Tracker selbst nachsehen und dann einsortieren, hier nur als Erinnerung:

`LeadLag-Param` (🔴) · `GapFade-Param` · `Telegram-Token` · `Frequenz-Bein-Discovery` · `OpEx-Momentum` · `Eval-Go-Live-Checkliste`

---

## 📋 Regeln für dieses System

1. **Jedes Ticket gehört in genau ein Epic.** Wenn es in zwei passt, gehört es ins frühere.
2. **Neues Ticket ohne Epic gibt es nicht.** Beim Anlegen Tag setzen.
3. **Erledigt = gelöscht**, nicht abgehakt und archiviert. Ergebnis kommt ins [[Strategie-Logbuch]], nicht in den Tracker (siehe #077, #079).
4. **Kein Epic überspringen.** Die Reihenfolge ist der ganze Sinn der Sache: erst nicht bluten, dann sauber, dann beweisbar, dann entschieden, dann live.
5. Ein Epic ist grün, wenn seine **Fertig-wenn**-Bedingung erfüllt ist, nicht wenn die Liste leer aussieht.

> [!tip] Noch nachzutragen
> Die 29 Tickets aus dem Tracker auf der Box sind hier noch nicht einzeln zugeordnet. Morgen einmal durchgehen und jedem Ticket sein `#epic/...` verpassen. Die Struktur oben deckt alle bisher im Vault dokumentierten Tickets ab.
