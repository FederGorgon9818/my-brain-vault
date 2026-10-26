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
| Handel wieder ab | **17:15 CT (= 18:15 ET)** laut Antwort E8 vom 12.10.2026 („trading hours that we permit on Futures are between 17:15 to 15:10 CT“). Die Mail vom 01.10.2026 nannte noch 17:00 CT, die neuere und auf die Frage gezielte Antwort gilt | 17:00 CT, nach dem Wochenende So 17:00 CT |

Quelle E8: Mail von support@e8markets.com vom 01.10.2026 (Thread „Signature Futures: holding positions overnight, daily close and weekend“). Gilt für SimFi Challenge und SimFi Performance, für 50k und 150k gleich, nur das Kontraktlimit hängt an der Kontogröße. Damit sind E8 und FN-Futures bei Flat-Zeit und Overnight gleich.

**Primärquelle E8 (geprüft 10.10.2026, AP234):** [Can I hold positions overnight? (Art. 10149596)](https://intercom.help/E8futures/en/articles/10149596-can-i-hold-positions-overnight): „It is not possible to hold positions overnight on the E8 Zero and E8 Signature Futures models." und „All open positions are being forced closed each day at 15:10 CT". Keine Trennung Eval/Funded, kein Unterschied Zero/Signature. Handelszeiten MNQ/MES laut [Art. 13001922](https://intercom.help/E8futures/en/articles/13001922-instrument-list-and-trading-hours-tradovate): „17:00 - 16:00 CT", Sonntag bis Freitag. **Unstimmigkeit im selben Artikel:** Text nennt „between 17:15 to 15:10 CT" (= 18:15 ET). Unsere Nachtbeine steigen später ein, ein Entry kurz nach 18:00 ET wäre betroffen, falls die 17:15 gelten. Details und Wortlaut: [[Research-Cache]], Abschnitt „E8 Futures: Overnight-Halten, Gapped/Illiquid Market Trading ...".

**Antwort E8-Support vom 12.10.2026** (Mail von support@e8markets.com, 18:37 UTC, Gmail maxlkho4, Thread „Signature Futures (E61803453048): session start time, "illiquid market hours", payout caps for 100K / 150K“, Thread-ID 1a13026f39da17d7, AP348/AP111):

1. **Session-Start:** erlaubtes Handelsfenster auf Futures ist **17:15 bis 15:10 CT**, alle offenen Positionen werden täglich um 15:10 CT zwangsgeschlossen. Damit ist die Unstimmigkeit aus Art. 13001922 zugunsten von 17:15 CT aufgelöst: **kein Entry zwischen 17:00 und 17:15 CT (18:00 bis 18:15 ET)**. E8 fragt zurück, auf welcher Seite die anderen Zeiten standen (Antwort an E8 offen, Sache von Max).
2. **„Micro-scalping during illiquid market hours“:** keine Uhrzeiten genannt. Die Regel zielt auf Micro-Scalping in Phasen niedriger Liquidität, in denen die Ausführung im echten Markt so nicht stattfinden würde (sehr schnelle Trades bei dünnem Buch, Ausnutzen der Simulation). Niedrige Liquidität gebe es „oft um Markteröffnungen oder Rollovers“. **Nicht beantwortet:** ob ein einzelner Entry kurz nach Session-Open mit Stop und mehreren Stunden Haltedauer betroffen ist. Nach dem Wortlaut (Ziel sind sehr schnelle Trades) eher nein, das ist aber unsere Lesart, keine Zusage.
3. **Payout-Caps 100K/150K:** im Mailtext keine Zahlen, nur ein Link auf einen Help-Artikel („Click Here“, Linkziel im Klartext der Mail nicht enthalten). **Die Caps je Auszahlung 1 bis 5 sind damit weiter nicht schriftlich bestätigt.** Bestätigt ist: **35 % Best-Day-Regel und 5 profitable Tage gelten für alle Signature-Futures-Größen gleich, auch 100K und 150K.**

Quelle FN: FundedNext-Wissensbasis, Artikel „Does FundedNext Futures allow overnight and weekend trade holding?" (helpfutures.fundednext.com/en/articles/14268506). **Achtung Verwechslungsgefahr:** für die CFD-/Forex-Konten von FundedNext ist Overnight- und Wochenend-Halten ausdrücklich ERLAUBT (Artikel 11982358). Die Futures-Sparte hat die gegenteilige Regel. Nur die Futures-Regel ist für uns relevant.

**Abgleich mit unserer Umsetzung:** unsere Beine sind alle intraday mit Zwangs-Flat `eod_flat_min=385` (15:55 ET = 14:55 CT), also **75 Minuten vor** dem FN-Auto-Close. Kein Konflikt. Konsequenz für die Strategie-Auswahl: **jedes Mehrtages-/Swing-Bein ist auf FN-Futures strukturell unmöglich**, unabhängig von seiner Edge. Betrifft u. a. den Weg W34 (Mehrtages-Gap-Fill) aus der [[Gap Wege-Karte]] und jede aus Tagesbar-Literatur portierte Strategie.

## ⏳ Inaktivität je Firma (eingetragen 14.10.2026, AP376 und AP330)

| Firma | Regel (Wortlaut-Kern) | Zählweise | Was zählt | Folge | Quelle |
|---|---|---|---|---|---|
| **E8 Futures** (Signature, Eval und Funded) | „After 60 or 7 days of inactivity (Depending on the market), the account will be closed", „7 Day inactivity applies to all Futures accounts", gilt auch für frisch gekaufte Konten ohne Trade | **Support bestätigt 18.10.: rollierend ab dem letzten geschlossenen Trade, Kalendertage, 7 Tage für Futures** (nicht 60) | ein **geschlossener** Trade (nur eröffnen zählt nicht), jede Größe, auch Break-even | Konto wird geschlossen, keine Warnstufe genannt. Reise: vorher an Support melden | Help Center Art. 9453425 (Primärquelle, 14.10.) plus Support-Mail 18.10.2026 (Gmail-Thread 1a14c477dbf350bd), Details im [[Research-Cache]] Abschnitt „E8 Futures: Inaktivitätsregel“ |
| **FundedNext Futures** | 30 Tage ohne Trade = Verstoß | nicht geprüft, wir rechnen 1 Tag in jedem 30-Tage-Fenster | ein Trade | Breach | Research-Cache (FN-Abschnitt) |
| **FFN STEADY** | mindestens 3 qualifizierende Handelstage in jeder 29-Tage-Periode | „every 29-day period“, Start nicht genannt. **Wir rechnen rollierend ab Aktivierung** (FFN1 05.10., FFN2 08.10.), die strengste Lesart | Tag mit realisiertem Gewinn oder Verlust von mindestens 5 $ | automatische Kündigung, gilt auch für geblasene Konten | FFN Art. 6.5 (Primärquelle) |

**Zwei Widersprüche bei E8, beide zu unseren Gunsten aufgelöst (strengere Zahl gilt):** der Produktartikel „E8 Signature“ nennt 60 Tage (gemeinsamer Text für Forex und Futures, ohne Markt-Kennzeichnung), die ESPA §9.3 nennt 30 Kalendertage „Dormant“ mit Suspendierung nach Ankündigung. Der Inaktivitätsartikel sagt ausdrücklich 7 Tage für alle Futures-Konten. Betriebsregel bleibt **7 Kalendertage rollierend**. Die E8-Mail vom 12.10. (Thread 1a13026f39da17d7) sagt zur Inaktivität nichts.

**Antwort E8-Support vom 18.10.2026** (support@e8markets.com an maxlkho4, 23:56 UTC am 17.10., Gmail-Thread 1a14c477dbf350bd, AP385), wörtlich: „1. Rolling from your last closed trade. 2. Calendar days. 3. By just opening position, it's not consider activate yet, you must close the position in order to consider your account active. 4. For Futures, 7 days. 5. Yes, any size counts, even at breakeven." Damit ist unsere Betriebsregel genau die von E8: **spätestens 7 Kalendertage nach dem letzten geschlossenen Trade muss der nächste geschlossen sein.** Der RiskGuard (live seit 18.10., Fenster 7, mind. 1, Schwelle 0, 1 Tag Sicherheitsabstand) und die Konto-Karte rechnen schon so, nichts anzupassen.

**Wie die Konto-Karte zählt (seit 14.10.2026):** ein Tag zählt, wenn sich der Tagesend-Kontostand (NetLiq, `maxlab_equity_<Konto>.csv`) gegenüber dem Vortag um mindestens **+5 $** bewegt hat oder um mindestens **−15 $** (FFN; E8 und FN: jede Bewegung). Schief, weil der NetLiq netto ist: ein Gewinntag ab +5 $ netto ist auch brutto über 5 $, ein Verlusttag kann brutto durch die Kommission (rund 1,78 $ je Micro-Round-Turn) unter 5 $ fallen, und ob FFN brutto oder netto zählt, steht nirgends. Eine pauschale 10-$-Schwelle hätte FFN2 am 13.10. (netto +9,88 $, brutto +17 $) einen echten Tag gekostet. Der laufende Tag zählt erst nach Tagesschluss. **Frist** = Tag, an dem spätestens der nächste qualifizierende Tag liegen muss: der drittletzte (FFN) bzw. letzte (E8) Handelstag plus Fenster, solange es noch zu wenige Tage gibt der Tag vor der Aktivierung plus Fenster (bis 14.10. rechnete die Karte hier einen Tag zu spät und ab der ersten Equity-Zeile statt ab Aktivierung). Warum nicht der realisierte PnL vom Broker: auf Tradovate (E8, FN) kommt beim Fill nur die Kommission an (TRADEPNL-Log zeigt −0,95 $), der Trade-PnL hängt eine Execution hinterher. Auf Rithmic (FFN) stimmt er sofort.

**Umsetzung:**
- **Heute live, alle Konten:** RiskGuard-Alarm AP217 ab Tag 4 ohne Round Turn (`inactivityalarmdays=4`), danach täglich. Max setzt dann einen Hand-Trade (Regel Max 06.10.). Für FFN reicht das allein nicht (3 Tage je 29, Mindestbetrag).
- **Konto-Karte:** zeigt je Konto Handelstage im Fenster, Frist und fehlende Tage, Ampel gelb, wenn die Frist höchstens 7 Tage (E8: 3) je fehlendem Tag entfernt ist, rot, wenn weniger Tage bleiben als fehlen (Lab, Reiter Konten).
- **Gebaut, nicht deployt:** einheitliche Inaktivitätsregel im RiskGuard für alle Firmen per cfg (rollierend oder Kalenderwoche, Schwelle, Start, Vorwarnung, optionaler Mini-Trade standardmäßig aus), Auftrag Max an Session 8cbabece, Paket `trading-data/nt8_staging_20261014_inaktivitaet` mit `DEPLOY.md` und `cfg_inaktivitaet_vorschlag.md`. Geht nach dem AP381-Deploy auf dessen neuen Live-Stand (Ticket AP330).

**Stand 14.10.2026 (Konto-Karten, Tage vor heute):**

| Konto | Regel | Tage im Fenster | Frist | fehlen |
|---|---|---|---|---|
| E8 50k | 1 in 7 | 2 (09.10., 13.10.) | 20.10. | 1 |
| FN1, FN2 | 1 in 30 | 11 | 12.11. | 1 |
| FFN1 | 3 in 29, ab 05.10. | 1 (13.10.) | 02.11. | 2 |
| FFN2 | 3 in 29, ab 08.10. | 1 (13.10.) | 05.11. | 2 |

Der 14.10. (FFN1 −86 $, FFN2 −87 $) zählt nach Tagesschluss mit, dann fehlt beiden FFN-Konten noch 1 Tag. E8 ist das einzige Konto mit echter Gefahr: die Belegung hatte historisch 75 von 3.863 Sieben-Tage-Fenstern ohne Handelstag (26 Strecken), ohne Hand-Trade kostet das in der Simulation 14 Punkte Überleben.

## 🚫 Verbotene Strategien (nachgetragen 22.09.2026)

| Verbot | E8 | FundedNext Futures |
|---|---|---|
| **Gapped or Illiquid Market Trading** | ❌ **steht auf der Verbotsliste** („strategies that exploit imperfections of the simulated market, such as Gapped, Illiquid Market Trading", geprüft 10.10.2026, AP234). Tatbestand = Ausnutzen der Simulation, keine Uhrzeiten, keine Eröffnungs-Regel, Eval/Funded und Zero/Signature gleich | ❌ ausdrücklich verboten |
| Arbitrage (jede Form) | offen | ❌ verboten |
| Strategie-/Risiko-Wechsel nach dem Pass | offen | ❌ verboten |

Wortlaut FN zur Gap-Regel: Orders in „gapped or illiquid market conditions" zu platzieren, um von Preis-Ineffizienzen zu profitieren, sei unzulässig, wegen unvorhersehbarer Ausführung, hoher Slippage und Manipulationsgefahr; ausdrücklich genannt wird Handel in Phasen niedriger Liquidität oder **vor großen Marktereignissen**. Quelle: helpfutures.fundednext.com/en/articles/14298337.

> [!warning] Offene Frage vor jedem Gap-Bein auf FN (22.09.2026)
> Der Wortlaut zielt auf das Ausnutzen dünner Bücher, nicht auf eine reguläre RTH-Order um 09:30 im liquidesten Moment des Tages. Unser historisches Gap-Bein (`RTY_Gap-fade`, Entry nach 10 Min Bestätigung innerhalb RTH) fällt nach dem Sinn der Regel nicht darunter. **Aber:** bevor ein Bein mit „Gap" im Mechanismus auf FN1/FN2 läuft, gehört das schriftlich vom FN-Support bestätigt. Der Name allein kann bei einer Payout-Prüfung Fragen auslösen. Bei E8 ist die Regellage dazu **noch gar nicht geprüft** — nachholen, bevor dort ein Gap-Bein läuft. **Nachgeholt 10.10.2026 (AP234):** E8 hat dieselbe Klausel, aber enger gefasst („exploit imperfections of the simulated market, such as Gapped, Illiquid Market Trading"), zusätzlich „reliance on micro-scalping during illiquid market hours" und die Regel „mindestens 50 % aller Gewinne aus Trades mit Haltedauer ≥ 10 Sekunden" (Art. 10209270). Kein Verbot von Gap-Strategien oder Handel um Eröffnungen als solchem, aber Ermessen des Risk-Teams. News-Trading bei E8 ohne Einschränkung (Art. 10209321, 27.08.2026).

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
| Kontraktlimit | **Support 05.10.: Eval = Maximum, das Rithmic setzt.** Funded skaliert, Erhöhung nur auf Antrag | **Geklärt 12.10.2026: 15 Minis / 150 Micros je Konto** (Aktivierungs-Mails von FFN an web.de vom 05.10. für FFN1 und 08.10. für FFN2, Zeile „Max Contracts“, deckt sich mit Art. 3.5). Wir handeln höchstens 5 Micros (4 MNQ + 1 M2K). Funded startet laut Art. 3.5 bei 40 Micros, auch das reicht |
| HFT | max. 30 % der Trades mit Round-Trip ≤ 5 s je Session. Verstoß = Konto und Profit weg. **Support 05.10.: keine Mindestanzahl, 1 schneller Trade bei 1 bis 3 Trades reicht**. **Support 09.10.: Zählbasis (je Strategie oder Konto-FIFO) nicht beantwortet**, nur Regel wiederholt plus „Adding to a trade still counts as 1 trade“ (deutet auf Zählung der Konto-Position) | PB3 raus (AP328). Asia vorerst raus (AP331, 4 Stop-Berührungen in der 1. Minute). Netting gegenläufiger Beine (AP332) |
| Inaktivität | ≥ 3 Handelstage (|realisiert| ≥ 5 $) in jedem 29-Tage-Fenster, sonst Kündigung ohne Warnung | **Tages-Alarm reicht NICHT** (3-Bein-Buch historisch genau auf 3, Alarm kennt Fenster und 5-$-Schwelle nicht). Rollfenster-Alarm = AP330, gebaut 14.10., noch nicht deployt. Fristen und Zählweise: Abschnitt „Inaktivität je Firma“ oben |
| Copy-Trading | eigene FFN-Konten max. 5 gleichzeitig, sonst alle disqualifiziert. **Support 09.10.: „You can copy trade up to 5 FFN Accounts at a time“**, gezählt werden also FFN-Konten (andere Firmen nicht ausdrücklich ausgeschlossen, aber nicht genannt) | FFN1 + FFN2 = 2 |
| Kontolimit | 10 Konten, max. 5 funded | |
| Plattform | NT8 **nur via Rithmic**, eigene NT8-Lizenz, Rithmic-Daten zahlt FFN, nur ein Gerät gleichzeitig eingeloggt | Rithmic-Verbindung auf der Box, kein R Trader parallel. Lizenz + Login macht Max |
| IP | ein konsistentes IP-Umfeld je Konto, keine IP-Teilung mit anderen Tradern, kein Shared-VPS | Box ist nur unsere. E8/FN/FFN auf derselben Box: **Support 09.10. verweist nur auf Art. 3.7** (verbietet IP-Teilung mit anderen FFN-Tradern), keine direkte Antwort. Mit Mail 01.10. („andere Prop-Firmen erlaubt“) gilt: ok nach Auslegung |
| Payout | alle 5 Profittage (je ≥ 250 $), Buffer 4.700 $, min. 500 $, Cap 2.500 $ (1 bis 3), danach 3.000 $; Net-Rule; Split 90/10 | |
| Live-Review | nach 5 Sim-Payouts, Sim-Profit verfällt beim Wechsel. Betrifft andere Konten nicht (Mail) | |
| Reset | 480 $ (mit 50 % 240 $) | |

**Betriebspunkt (Entscheidung Max 05.10.2026, Quant-Team):** k1 (1 Micro je Bein), RiskGuard-Tagesstopp **2.500 $** (Katastrophenbremse, in den Daten nie erreicht), `maxcontracts=2`, Consistency-Deckel ~~4.380 $~~ **4.212 $** (Nachrechnung unten) nur in der Eval. **FFN handelt ohne PB3** (nur LastHour, Asia, OpenDrive; Asia seit Nachrechnung vorerst auch raus, AP331): PB3 hat 10,8 % Stop-outs in derselben Minute, ein einziger Round-Trip unter 5 s kann bei 1 bis 3 Trades je Session die HFT-Regel reißen. PB3 kommt erst mit AP328 dazu (Sekunden-Messung live oder Mindestabstand zum Stop). cfg-Vorlage: `nt8_staging_20261003_riskguard_eod/cfg_vorlage_ffn_150k.txt`, eingespielt wird sie erst, wenn Rithmic in NT8 steht und der Kontoname geprüft ist. BOGO-Konto legt Max selbst an („Start New Evaluation", Support 05.10.).

**Hochstuf-Schwelle neu (Entscheidung Max 12.10.2026):** k2 auf FFN erst, wenn die Tagesschwankung der **eigenen Belegung** des Kontos über 60 Tage bei höchstens **235 $** liegt (Puffer 4.700 $ = 10-fache Schwankung bei k2, Track-Record-Variante). Die alte Vola-Regel „unter ~400 $“ gilt nicht mehr. Stand 12.10. (Daten bis 11.09.): FFN1 449 $, FFN2 330 $ über 120 Tage, also k1. Herleitung und offene Punkte: [[Hochstuf-Regel je Konto (Entwurf)]].

**Nachrechnung 05.10.2026 spät (Session 016cea93, Quant-Team + strategy-auditor):** Die Rechnung oben lief am 4-Bein-Buch inkl. PB3, FFN handelt aber mit 3 Beinen. Ergebnis am 3-Bein-Buch, vola-normiert:
- **k1 bleibt, Tagesstopp 2.500 $ bleibt** (Plateau, wirkt wie kein Stopp). P(Pass) ca. 93 % [82; 99], geschrumpft 73 %, Median 12 bis 17 Monate. FFN spart in jedem Regime 3 bis 8 Monate bis 50k, Nulldrift 0 %. k2 wäre nach der Vola-Regel knapp erlaubt (σ60 391 < 400, Daten nur bis 06.08.), kostet geschrumpft aber 10 bis 14 pp mehr Plan-Tod. Hochstufen erst mit frischen Daten (AP313).
- **Consistency-Deckel 4.212 $** (0,468 / Abstand 0, Max 05.10.), ersetzt die 4.380 $ der Vorlage. Bei k1 nie berührt (größter Tag 3.077 $).
- **Asia auf FFN: no-go bis AP331.** LastHour und OpenDrive: go mit Auflagen (Netting AP332, Rithmic-Limit, T1-Sperre vor Funded AP335).
- **Neue Haken:** Inaktivität (AP330), Copy-Trading-Zählung über Firmen hinweg unklar: mit E8 150k wären es 6 Konten mit gleichen Signalen (AP333).
- **Nicht in book_state:** die Rechenwerkzeuge kennen FFN noch nicht (AP334).

**RTY-Gap live auf FFN1 seit 11.10.2026 (Wochenend-Entscheidung Max, AP338):** fünftes Bein nur auf `2D-150K394206247048`, als zweite Host-Instanz auf einem M2K-Chart (M2K 12-26, 1 Minute, US Equities RTH), Config `maxlab_book_host.live_ffn150k_rtygap.json` mit `"instrument": "M2K"` (MD5 68f60ca6), 1 Micro fest (`qty_source: config`), `stop_delay_seconds 10` und `cat_stop_r 2.0` wie PB3, Ziel-Limit erst 10 s nach dem Einstieg, `skip_dates` 27.11. und 24.12. Der Host löst seitdem nach Konto plus Instrument auf, Dateien ohne `"instrument"` gelten wie bisher. E8 50k, FN1, FN2 und das echte Buch (`book_state.json`) handeln das Bein nicht.
- **Einordnung (strategy-auditor):** Live-Experiment, kein belegtes Bein. Edge rund 300 $/Jahr je Micro, im Plan mit 0 bis 1 Monat buchen. Schlechtester Tag −185 $, Tagesstopp und Consistency-Deckel nie berührt. RiskGuard zählt und flattet M2K kontoweit mit.
- **FFN2 Nachzug 12.10.2026 (Entscheidung Max, AP355):** Max hebt beide Warte-Bedingungen bewusst auf (PB3 hatte auf FFN1 noch kein Signal, RTY-Gap noch keinen Round-Trip). Auf der Box liegen seit 22:20 Boxzeit `maxlab_book_host.live_ffn150k_2.json` (MD5 6874c4f5, LastHour, OpenDrive, Asia, PB3 mit 10 s Stop-Verzögerung und Kat-Stop 2R) und `maxlab_book_host.live_ffn150k_2_rtygap.json` (MD5 3444be51, `"instrument": "M2K"`, 1 Micro fest). Inhalt bis auf die Kontonummer gleich wie FFN1. Alte Datei gesichert unter `_bak_archiv\maxlab_book_host.live_ffn150k_2.json.bak-20261012-vor-pb3-rtygap` (ed5e4c1b). Alles k1, RiskGuard FFN2 unverändert (gleiche Werte wie FFN1). **Live seit 12.10.2026 22:22 Boxzeit:** Host [20] MNQ und Instanz [24] M2K 12-26 melden HOST BEREIT mit diesen Prüfsummen, kein Config-Fehler. FFN1 und FFN2 handeln damit dieselben 5 Beine.
- **FFN2 (`2D-150K010602681476`)** (überholt durch die Zeile darüber) sollte erst nach dem ersten echten RTY-Round-Trip auf FFN1 mit sauberer `HOLD`-Zeile nach. Die fertige Config liegt in `trading-data/nt8_staging_20261011_rtygap_live/`.
- **Ausstiegsregel (Vorschlag strategy-auditor, von Max am 11.10.2026 bestätigt, Ticket AP338):** Verlustbudget −600 $ je Konto, raus bei mehr als ~5 $ Abweichung je Trade zwischen Live und Backtest über 20 Trades, sofort aus bei einem Round-Trip unter 10 s, kein Retune, Review nach 40 Trades oder 12 Monaten.
- **Rithmic-Limit erledigt (12.10.2026):** 150 Micros je Konto, siehe Zeile Kontraktlimit.
- **Offen:** T1-Sperre (AP335) muss vor Funded auch den M2K-Host abdecken.

**Support-Antworten 05.10.2026 (20:26 UTC):** DD-Bruch zählt sofort („go to or below drawdown, blown immediately"). HFT „Yes", also ohne Mindestanzahl. T1-News nur Funded. VPS ok, Kontraktlimit Eval = Rithmic-Maximum. ~~**Noch offen:** gleiche IP wie andere Firmen, Copy-Zählung und HFT-Zählbasis FIFO (AP333).~~ **Antwort 09.10.2026 (03:07 UTC, AP333):** Copy „up to 5 FFN Accounts at a time“ (Zählung über FFN-Konten). HFT nur Regeltext wiederholt plus „Adding to a trade still counts as 1 trade“, Zählbasis FIFO bleibt unbeantwortet. IP: nur Verweis auf Art. 3.7, keine direkte Antwort.

### Aus der CLAUDE.md übernommen (05.10.2026): FFN-Ergänzungen

- FFN ist eine **eigene Firma**, nicht FundedNext und nicht My Funded Futures. Das Gratis-Zweitkonto (BOGO) ist beim Support angefragt.
- Die Freigabe-Mail liegt in Gmail (maxlkho4), Thread „Questions before purchase: STEADY 150K…", Absender support@fundedfuturesnetwork.com. Inhalt: vollautomatische, selbst entwickelte NT8-Strategie, **unbeaufsichtigt, auf Windows-VPS mit Rechenzentrums-IP, in Eval und Funded erlaubt**; dieselbe Strategie auf mehreren FFN-Konten und bei anderen Prop-Firmen erlaubt; Deutschland erlaubt; Live-Review nach 5 Payouts betrifft andere Konten nicht.
- Technik: NT8 **nur via Rithmic** (nicht Tradovate), **eigene NT8-Lizenz nötig**, Rithmic-Datengebühren trägt FFN, nur **ein Gerät gleichzeitig** eingeloggt.
- Regelwerte (DD, Ziel, Consistency, Payout): Tabelle oben und [[Research-Cache]]; Quelle FFN-Help-Center Artikel 2.5 STEADY + 3.7 Independent Trading Rules.
- Die Zeile „Freigabe geklärt, nicht erneut fragen" bleibt in der CLAUDE.md, solange FFN läuft.

## 💵 Kommission je Konto (cfg `commissionrt`, AP319, 22.10.2026)

Der RiskGuard rechnet den **Trade-PnL je Exit** (Telegram „⚡ Fill … | Trade-PnL: −$277.40 (netto)“) seit AP319 aus den Fill-Preisen und zieht die Kommission aus der cfg ab. NT8 liefert die Kommission je Fill bei keinem Broker mit (`Execution.Commission` ist überall 0, NT8-DB geprüft 22.10.).

| Konto | Broker | `<Konto>.commissionrt` | Beleg |
|---|---|---|---|
| E8 50k, FN1, FN2 | Tradovate | **1.90** $ je Micro-Round-Turn | brutto aus Fills gegen NetLiq-Differenz an jedem flachen Tag 05. bis 21.10. identisch, deckt sich mit AP384 |
| FFN1, FFN2 | Rithmic | **1.78** $ | 14.10. (M2K), 15.10. und 21.10. (MNQ) identisch |

- Wirkt **nur auf die Anzeige**, nicht auf Size, Tagesbasis, Kill-Switch, Floor, Deckel oder Inaktivität. Fehlt der Key, zeigt das Telegram brutto mit Hinweis.
- **Neues Konto oder Funded-Wechsel:** Key `<Konto>.commissionrt` mit anlegen (Schritt 2 unten), Satz am ersten flachen Tag gegen die NetLiq-Differenz prüfen.
- Vorher (bis 22.10.) zeigte das Telegram auf Tradovate-Konten „Trade-PnL −$1“: NT8 bucht dort den realisierten Gewinn erst nach dem Fill-Ereignis, der alte Diff sah nur die Kommission einer Seite.

## Ablauf bei neuem Konto oder neuer Firma (Regel Max, 22.09.2026)

Aus der CLAUDE.md übernommen (Abschnitt „Neues Konto oder neue Firma → Regeln prüfen und alles anpassen"). Skill: `/neues-konto`.

**Auslöser:** Firma-Regel, die E8 nicht kennt (FundedNext-Challenge hat eine Consistency-Rule, Tagesgewinn ≤ 40 % vom Target), fehlte im RiskGuard, bis sie am 21.09. per Zufall auffiel. Deshalb: **sobald Max ein weiteres Konto kauft oder eine neue Firma/Phase dazukommt** (auch Funded-Wechsel, Kontogröße, Reset, Add-on), läuft der Ablauf **von selbst und vor dem ersten Trade**:

1. **Regeln holen:** Regeln der Firma/Phase aus der Primärquelle holen (`research-scout`, [[Research-Cache]] zuerst) und hier eintragen: Consistency/Tagesgewinn, DD-Typ und Einrasten, News-Regel, Inaktivität, Zeitfenster/Flat-Zeit, Kontraktlimit, Payout-Regeln, Algo-/VPS-Erlaubnis, Haushaltsgrenze.
2. **Gegen die Umsetzung abgleichen und alles Nötige anpassen:** `MaxRiskGuard.cs` (cfg-Datei `maxlab_riskguard.cfg` pro Konto, nie nur die UI, inklusive `commissionrt`, siehe Abschnitt Kommission), Strategie-Instanzen/Größe (k), `book_state.json`/Käfig (`cage_policy_lib`, `evaluate_v2`), Watchdog/Telegram. Was noch nicht als Property existiert, wird als Ticket angelegt und vor dem Trade gebaut, oder das Konto handelt bis dahin nur mit Handaufsicht.
3. **Festhalten und ansagen:** Konten-Liste, Regel-Tabelle und die aktiven Deckel (Werte je Konto) hier festhalten und Max ansagen, was angepasst wurde.

**Ein Konto gilt erst als startklar, wenn diese Prüfung durch ist.** Der Dauer-Check bei Statuswechsel (Challenge zu Funded) hängt an **AP203**.

## 🔗 Verwandt
- [[Strategie-Logbuch]] — Vorfall 21.09.2026 (falls dort nachgetragen)
- `engine/ninjascript/MaxRiskGuard.cs` — Enforcement
- `engine/_scratch_box_urlaub/1e3478e2/qm/fn_lib.py` — Backtest-seitige Consistency-Rechnung
- [[Gap Wege-Karte]] — betroffen von Flat-Zeit (W34) und Gap-Verbot
