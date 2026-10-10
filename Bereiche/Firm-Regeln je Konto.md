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
> Wird ein weiteres Konto gekauft (oder wechselt eines die Phase), werden **vor dem ersten Trade** dessen Regeln geprüft, in die Tabellen unten eingetragen und alles Nötige angepasst (RiskGuard-cfg, Größe, Käfig in `book_state.json`/`cage_policy_lib`, Watchdog). Ablauf steht unten im Abschnitt „Ablauf bei neuem Konto oder neuer Firma" (Skill `/neues-konto`). Checkliste je Konto: Consistency/Tagesgewinn · DD-Typ und Einrasten · News-Regel · Inaktivität · Flat-Zeit · Kontraktlimit · Payout-Regeln · Algo-/VPS-Erlaubnis · Haushaltsgrenze.

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
| Overnight-Halten | ❌ **nicht über den Tagesschluss** (Antwort E8 01.10.2026). Innerhalb des Handelstags 18:00 bis 16:10 ET erlaubt, daraus folgt Nacht ab 18:00 bis Open (nicht wörtlich bestätigt) | ❌ **verboten** |
| Wochenend-Halten | ❌ **verboten**, vor dem Freitags-Cutoff schließen (Antwort E8 01.10.2026) | ❌ **verboten** |
| Zwangs-Flat | **15:10 CT** (= 16:10 ET), automatische Schließung aller offenen Positionen (Antwort E8 01.10.2026). Reset-Zeit für DD/Tageslimits nicht beantwortet | **15:10 CT** (= 16:10 ET), System-Auto-Close aller offenen Positionen |
| Handel wieder ab | 17:00 CT (= 18:00 ET), je nach Instrument (Antwort E8 01.10.2026) | 17:00 CT, nach dem Wochenende So 17:00 CT |

Quelle E8: Mail von support@e8markets.com vom 01.10.2026 (Thread „Signature Futures: holding positions overnight, daily close and weekend“). Gilt für SimFi Challenge und SimFi Performance, für 50k und 150k gleich, nur das Kontraktlimit hängt an der Kontogröße. Damit sind E8 und FN-Futures bei Flat-Zeit und Overnight gleich.

Quelle FN: FundedNext-Wissensbasis, Artikel „Does FundedNext Futures allow overnight and weekend trade holding?" (helpfutures.fundednext.com/en/articles/14268506). **Achtung Verwechslungsgefahr:** für die CFD-/Forex-Konten von FundedNext ist Overnight- und Wochenend-Halten ausdrücklich ERLAUBT (Artikel 11982358). Die Futures-Sparte hat die gegenteilige Regel. Nur die Futures-Regel ist für uns relevant.

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

## 🟦 Funded Futures Network (FFN) STEADY 150K (eingetragen 05.10.2026)

**Live seit 09.10.2026 01:50 (Boxzeit), zwei Konten:** `2D-150K394206247048` (FFN1) und `2D-150K010602681476` (FFN2, BOGO). Je ein MaxBookHost mit LastHour, OpenDrive und Asia. **PB3 seit 10.10.2026 nur auf FFN1** (10 s Stop-Verzögerung, Kat-Stop 2R, AP328, Datei f760d269, Host aktiv seit 10.10. 18:48 Boxzeit, im Log bestätigt), FFN2 zieht nach dem ersten sauberen PB3-Handelstag nach (Max 10.10., kein Sim-Test vorab). Exit-Versatz 15 s (AP332), RiskGuard je Konto: DD 4.700, Tagesstopp 2.500, Ziel 9.000, fixedqty 1 (k1), maxcontracts 2, Consistency 0,468, Telegram an. Host-JSONs `maxlab_book_host.live_ffn150k.json` / `..._2.json` (finden ihr Konto über `account`). **Falle Kontoname:** NT8 zeigt Rithmic-Konten als `<id>!FundedFuturesNetwork!FundedFuturesNetwork`, intern (`Account.Name`, cfg-Präfix, JSON-`account`) heißt das Konto nur `<id>`. **Copy-Zählung:** mit FFN2 laufen 5 Konten mit gleichen Signalen (FFN-Limit 5), E8 150k erst nach der Antwort zu AP333.

Konto `2D-150K394206247048`, gekauft 05.10.2026 für 292,50 $ (50 % + BOGO, Bonus-Konto binnen 45 Tagen einlösen). Ticket **AP325** (Einrichtung vor dem ersten Trade). Quellen: FFN-Help-Center Art. 2.5 STEADY, 3.3, 3.4, 3.5, 3.7, 3.8, 6.5, 8.3, 9.1, 12.1 (Links und Wortlaut im [[Research-Cache]], Abschnitt FFN STEADY 150k) plus Support-Mails 01.10. und 05.10.2026.

**Freigabe ist geklärt, nicht erneut fragen:** schriftlich vom FFN-Support am 01.10.2026: unbeaufsichtigter Algo auf Windows-VPS, Eval und Funded, dieselbe Strategie mehrfach und bei anderen Firmen, Deutschland erlaubt. Regelwerk 3.7 deckt eigene Algos und eigene VPS. Die Zeile auf der Steady-Landingpage „automated bots/EAs not supported" heißt „nicht von FFN-Tooling unterstützt", die Mail schlägt den Marketing-Text. Mail aufheben (Gmail-Thread mit support@fundedfuturesnetwork.com).

| Regel | FFN STEADY 150K | Abgleich mit uns |
|---|---|---|
| Target | 9.000 $ (6 %), 2 Gewinntage mit je ≥ 250 $, kein Zeitlimit | `target=9000` |
| Max-DD | **4.700 $ EOD-Trailing**, rastet bei Startsaldo + 100 ein (150.100) | `maxdd=4700`, `lockoffset=100`; RiskGuard rechnet intraday, also strenger als die Firma |
| Tageslimit der Firma | keins | eigener Tagesstopp, Wert vom Quant-Team (AP325) |
| Consistency | Eval 52 %, Funded keine | `dailyprofitcap` 0,52 bzw. mit Abstand; bei k1 praktisch nie berührt |
| Flat-Zeit | flat bis **16:50 ET**, Wiedereröffnung 18:00 ET, Fr 16:50 bis So 18:00. Verpasst = Konto weg | unsere Beine flat 15:55 ET, Orphan-Flat 15:58 ET. Kein Konflikt |
| News | Art. 3.3: T1 (FOMC, FOMC Minutes, NFP, CPI) 1 Min vor/nach flat. **Support 05.10.: gilt nur Funded**, dort Liquidation plus Profit weg | Eval frei. Vor dem Funded-Wechsel Entry-Sperre bauen (AP335) |
| Kontraktlimit | **Support 05.10.: Eval = Maximum, das Rithmic setzt.** Funded skaliert, Erhöhung nur auf Antrag | k1 = 3 Micros (3 Beine). Rithmic-Kontolimit vor dem ersten Trade prüfen (muss ≥ 3 sein, sonst Reject → Sofort-Flatten → HFT-Gefahr) |
| HFT | max. 30 % der Trades mit Round-Trip ≤ 5 s je Session. Verstoß = Konto und Profit weg. **Support 05.10.: keine Mindestanzahl, 1 schneller Trade bei 1 bis 3 Trades reicht**. **Support 09.10.: Zählbasis (je Strategie oder Konto-FIFO) nicht beantwortet**, nur Regel wiederholt plus „Adding to a trade still counts as 1 trade“ (deutet auf Zählung der Konto-Position) | PB3 raus (AP328). Asia vorerst raus (AP331, 4 Stop-Berührungen in der 1. Minute). Netting gegenläufiger Beine (AP332) |
| Inaktivität | ≥ 3 Handelstage (|realisiert| ≥ 5 $) in jedem 29-Tage-Fenster, sonst Kündigung ohne Warnung | **Tages-Alarm reicht NICHT** (3-Bein-Buch historisch genau auf 3, Alarm kennt Fenster und 5-$-Schwelle nicht). Rollfenster-Alarm „< 3 in 22 Tagen" = AP330 |
| Copy-Trading | eigene FFN-Konten max. 5 gleichzeitig, sonst alle disqualifiziert. **Support 09.10.: „You can copy trade up to 5 FFN Accounts at a time“**, gezählt werden also FFN-Konten (andere Firmen nicht ausdrücklich ausgeschlossen, aber nicht genannt) | FFN1 + FFN2 = 2 |
| Kontolimit | 10 Konten, max. 5 funded | |
| Plattform | NT8 **nur via Rithmic**, eigene NT8-Lizenz, Rithmic-Daten zahlt FFN, nur ein Gerät gleichzeitig eingeloggt | Rithmic-Verbindung auf der Box, kein R Trader parallel. Lizenz + Login macht Max |
| IP | ein konsistentes IP-Umfeld je Konto, keine IP-Teilung mit anderen Tradern, kein Shared-VPS | Box ist nur unsere. E8/FN/FFN auf derselben Box: **Support 09.10. verweist nur auf Art. 3.7** (verbietet IP-Teilung mit anderen FFN-Tradern), keine direkte Antwort. Mit Mail 01.10. („andere Prop-Firmen erlaubt“) gilt: ok nach Auslegung |
| Payout | alle 5 Profittage (je ≥ 250 $), Buffer 4.700 $, min. 500 $, Cap 2.500 $ (1 bis 3), danach 3.000 $; Net-Rule; Split 90/10 | |
| Live-Review | nach 5 Sim-Payouts, Sim-Profit verfällt beim Wechsel. Betrifft andere Konten nicht (Mail) | |
| Reset | 480 $ (mit 50 % 240 $) | |

**Betriebspunkt (Entscheidung Max 05.10.2026, Quant-Team):** k1 (1 Micro je Bein), RiskGuard-Tagesstopp **2.500 $** (Katastrophenbremse, in den Daten nie erreicht), `maxcontracts=2`, Consistency-Deckel ~~4.380 $~~ **4.212 $** (Nachrechnung unten) nur in der Eval. **FFN handelt ohne PB3** (nur LastHour, Asia, OpenDrive; Asia seit Nachrechnung vorerst auch raus, AP331): PB3 hat 10,8 % Stop-outs in derselben Minute, ein einziger Round-Trip unter 5 s kann bei 1 bis 3 Trades je Session die HFT-Regel reißen. PB3 kommt erst mit AP328 dazu (Sekunden-Messung live oder Mindestabstand zum Stop). cfg-Vorlage: `nt8_staging_20261003_riskguard_eod/cfg_vorlage_ffn_150k.txt`, eingespielt wird sie erst, wenn Rithmic in NT8 steht und der Kontoname geprüft ist. BOGO-Konto legt Max selbst an („Start New Evaluation", Support 05.10.).

**Nachrechnung 05.10.2026 spät (Session 016cea93, Quant-Team + strategy-auditor):** Die Rechnung oben lief am 4-Bein-Buch inkl. PB3, FFN handelt aber mit 3 Beinen. Ergebnis am 3-Bein-Buch, vola-normiert:
- **k1 bleibt, Tagesstopp 2.500 $ bleibt** (Plateau, wirkt wie kein Stopp). P(Pass) ca. 93 % [82; 99], geschrumpft 73 %, Median 12 bis 17 Monate. FFN spart in jedem Regime 3 bis 8 Monate bis 50k, Nulldrift 0 %. k2 wäre nach der Vola-Regel knapp erlaubt (σ60 391 < 400, Daten nur bis 06.08.), kostet geschrumpft aber 10 bis 14 pp mehr Plan-Tod. Hochstufen erst mit frischen Daten (AP313).
- **Consistency-Deckel 4.212 $** (0,468 / Abstand 0, Max 05.10.), ersetzt die 4.380 $ der Vorlage. Bei k1 nie berührt (größter Tag 3.077 $).
- **Asia auf FFN: no-go bis AP331.** LastHour und OpenDrive: go mit Auflagen (Netting AP332, Rithmic-Limit, T1-Sperre vor Funded AP335).
- **Neue Haken:** Inaktivität (AP330), Copy-Trading-Zählung über Firmen hinweg unklar: mit E8 150k wären es 6 Konten mit gleichen Signalen (AP333).
- **Nicht in book_state:** die Rechenwerkzeuge kennen FFN noch nicht (AP334).

**Support-Antworten 05.10.2026 (20:26 UTC):** DD-Bruch zählt sofort („go to or below drawdown, blown immediately"). HFT „Yes", also ohne Mindestanzahl. T1-News nur Funded. VPS ok, Kontraktlimit Eval = Rithmic-Maximum. ~~**Noch offen:** gleiche IP wie andere Firmen, Copy-Zählung und HFT-Zählbasis FIFO (AP333).~~ **Antwort 09.10.2026 (03:07 UTC, AP333):** Copy „up to 5 FFN Accounts at a time“ (Zählung über FFN-Konten). HFT nur Regeltext wiederholt plus „Adding to a trade still counts as 1 trade“, Zählbasis FIFO bleibt unbeantwortet. IP: nur Verweis auf Art. 3.7, keine direkte Antwort.

### Aus der CLAUDE.md übernommen (05.10.2026): FFN-Ergänzungen

- FFN ist eine **eigene Firma**, nicht FundedNext und nicht My Funded Futures. Das Gratis-Zweitkonto (BOGO) ist beim Support angefragt.
- Die Freigabe-Mail liegt in Gmail (maxlkho4), Thread „Questions before purchase: STEADY 150K…", Absender support@fundedfuturesnetwork.com. Inhalt: vollautomatische, selbst entwickelte NT8-Strategie, **unbeaufsichtigt, auf Windows-VPS mit Rechenzentrums-IP, in Eval und Funded erlaubt**; dieselbe Strategie auf mehreren FFN-Konten und bei anderen Prop-Firmen erlaubt; Deutschland erlaubt; Live-Review nach 5 Payouts betrifft andere Konten nicht.
- Technik: NT8 **nur via Rithmic** (nicht Tradovate), **eigene NT8-Lizenz nötig**, Rithmic-Datengebühren trägt FFN, nur **ein Gerät gleichzeitig** eingeloggt.
- Regelwerte (DD, Ziel, Consistency, Payout): Tabelle oben und [[Research-Cache]]; Quelle FFN-Help-Center Artikel 2.5 STEADY + 3.7 Independent Trading Rules.
- Die Zeile „Freigabe geklärt, nicht erneut fragen" bleibt in der CLAUDE.md, solange FFN läuft.

## Ablauf bei neuem Konto oder neuer Firma (Regel Max, 22.09.2026)

Aus der CLAUDE.md übernommen (Abschnitt „Neues Konto oder neue Firma → Regeln prüfen und alles anpassen"). Skill: `/neues-konto`.

**Auslöser:** Firma-Regel, die E8 nicht kennt (FundedNext-Challenge hat eine Consistency-Rule, Tagesgewinn ≤ 40 % vom Target), fehlte im RiskGuard, bis sie am 21.09. per Zufall auffiel. Deshalb: **sobald Max ein weiteres Konto kauft oder eine neue Firma/Phase dazukommt** (auch Funded-Wechsel, Kontogröße, Reset, Add-on), läuft der Ablauf **von selbst und vor dem ersten Trade**:

1. **Regeln holen:** Regeln der Firma/Phase aus der Primärquelle holen (`research-scout`, [[Research-Cache]] zuerst) und hier eintragen: Consistency/Tagesgewinn, DD-Typ und Einrasten, News-Regel, Inaktivität, Zeitfenster/Flat-Zeit, Kontraktlimit, Payout-Regeln, Algo-/VPS-Erlaubnis, Haushaltsgrenze.
2. **Gegen die Umsetzung abgleichen und alles Nötige anpassen:** `MaxRiskGuard.cs` (cfg-Datei `maxlab_riskguard.cfg` pro Konto, nie nur die UI), Strategie-Instanzen/Größe (k), `book_state.json`/Käfig (`cage_policy_lib`, `evaluate_v2`), Watchdog/Telegram. Was noch nicht als Property existiert, wird als Ticket angelegt und vor dem Trade gebaut, oder das Konto handelt bis dahin nur mit Handaufsicht.
3. **Festhalten und ansagen:** Konten-Liste, Regel-Tabelle und die aktiven Deckel (Werte je Konto) hier festhalten und Max ansagen, was angepasst wurde.

**Ein Konto gilt erst als startklar, wenn diese Prüfung durch ist.** Der Dauer-Check bei Statuswechsel (Challenge zu Funded) hängt an **AP203**.

## 🔗 Verwandt
- [[Strategie-Logbuch]] — Vorfall 21.09.2026 (falls dort nachgetragen)
- `engine/ninjascript/MaxRiskGuard.cs` — Enforcement
- `engine/_scratch_box_urlaub/1e3478e2/qm/fn_lib.py` — Backtest-seitige Consistency-Rechnung
- [[Gap Wege-Karte]] — betroffen von Flat-Zeit (W34) und Gap-Verbot
