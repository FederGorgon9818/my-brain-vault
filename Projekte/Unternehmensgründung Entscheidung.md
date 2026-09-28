---
tags:
  - projekt
  - bereich/business
  - steuer
erstellt: 2026-09-23
status: Entscheidung vorbereitet, Termin mit Freundin offen
---
# 🏢 Unternehmensgründung: jetzt oder später?

⬅️ [[Steuer & Gewerbe (Prop-Payouts)]] · [[Belegordner 2026]] · [[Eval-Passing]] · [[Firm-Regeln je Konto]]

> [!summary] Ergebnis in drei Sätzen
> **Empfehlung: sofort gründen, also im Oktober 2026 als Nebengewerbe (Einzelunternehmen), direkt nach dem Termin mit deiner Freundin.** Der Grund ist nicht „Gründer machen das so", sondern dein Kalender: Nur solange du Gehalt hast (bis 03.07.2027), bringen Gewerbe-Verluste echtes Geld zurück (Grenzsteuersatz ≈ 26 bis 28 % inkl. Kirchensteuer). Im BOS-Jahr ohne Gehalt ist der Satz praktisch 0 %. Jeder Euro Eval, Claude, Box und Hardware, den du vorher als Betriebsausgabe ansetzt, ist jetzt am meisten wert (Rechnung: [[Gründung Zeitplan]]). Außerdem startet mit dem ersten Steuerbescheid die 2 bis 3 Jahre lange Uhr, die eine Bank später für „Einkommen aus Trading" sehen will.
>
> **Die eine Entscheidung, die du vor der Anmeldung treffen musst:** Kleinunternehmer oder Regelbesteuerung. Das Ergebnis dieses Dokuments ist: für dein Setup ist die Regelbesteuerung sehr wahrscheinlich günstiger (Details in Abschnitt 4.5). Deine Freundin soll das gegenprüfen.

> [!danger] ⚠️ WORAUF DU UNBEDINGT ACHTEN MUSST
> 1. **Im Fragebogen NICHT einfach „Kleinunternehmer" ankreuzen.** Erst Termin mit Freundin (AP235). Die Wahl bindet bis zu 5 Jahre und macht bis Juli 2027 ≈ 1.000 bis 1.300 € Unterschied (Rechnung in [[Gründung Zeitplan]]).
> 2. **Bis 03.04.2027 arbeitsuchend melden** (AP236). Sonst Sperrzeit, und die ALG-I-Option für Juli/August ist weg.
> 3. **Krankenversicherung ab 04.07.2027 klären** (AP237). Nach Jobende bist du nicht automatisch versichert.
> 4. **Kein Hardwarekauf und keine Zusatz-Evals, bevor der BOS-Finanzplan steht** (AP238). Ab Juli 2027 kommt kein Gehalt mehr.
> 5. **Hardware nicht zu 100 % geschäftlich ansetzen**, wenn du sie privat nutzt (AP239).
> 6. **Belege ab jetzt lückenlos sammeln**, auch die seit August (rückwirkend erledigt 24.09., laufend AP251). Ohne Beleg keine Betriebsausgabe.

> [!warning] Grenzen dieses Dokuments
> Kein Steuerberater-Ersatz. Zahlen zu Grenzen und Sätzen sind Stand meines Wissens (Mitte 2026) und im Text als „prüfen" markiert, wo ich nicht sicher bin. Hardware-Preise, Databento-Kosten und die Einordnung der Payouts sind **Annahmen**. Alles, was mit Geld auf deiner Seite zu tun hat, bitte mit deiner Freundin gegenrechnen.

---

## 1. Aktuelle Ausgangssituation

### Berufliche Situation
| Punkt | Stand |
|---|---|
| Job | Junior Fachinformatiker AE, IT bei GEWO Feinmechanik, Vollzeit 40 h |
| Gehalt | 3.600 € brutto/Monat (≈ 43.200 €/Jahr, ohne evtl. Sonderzahlungen) |
| Vertrag | **befristet bis 03.07.2027** |
| Nebentätigkeit | **heute (23.09.2026) genehmigt**, Pflicht aus §8 Arbeitsvertrag damit erfüllt. Achtung §8.4: Zustimmung ist jederzeit widerruflich |
| Danach | 04.07. bis Anfang Sept. 2027: Vollzeit selbstständig (≈ 2 Monate) |
| BOS | ab Anfang Sept. 2027, Gewerbe läuft als **Nebengewerbe** weiter |
| Gewerbe | **noch nicht angemeldet** (AP34 offen), Belegordner steht, ist aber leer |
| Vorhanden | ELSTER-Zugang (eID), Revolut Personal, Tätigkeitstext für GewA 1 fertig formuliert, Gewerbeamt VG Oberneuching recherchiert |

### Geld
| Punkt | Stand |
|---|---|
| Sparrate | 600 €/Monat aufs Konto + 450 €/Monat ETF-Sparplan |
| Bis 03.07.2027 (9 Monate) | ≈ 5.400 € Cash-Zuwachs + ≈ 4.050 € in ETFs |
| Risikorahmen Trading | Deckel **2.500 $ Netto-Auslage** (AP204), Start 1x E8 150k am 02.10. (AP214), „Kasse knapp" |
| Payouts bisher | **keine** |

### Technisches Know-how und Stand der Algorithmen
- Eigene Backtest-Engine (Python), Discovery-Runner als Dauerdienst auf der Box, Hub als Desktop-Cockpit, Hooks/Agents als Qualitätssicherung, Strategie-Logbuch mit 170+ Einträgen und Friedhof.
- **Buch: 3 Beine** (NQ_Momentum, Asia-Dir, NQ_LastHour). Backtest IS 22,36 $/Tag, geschrumpft 12,8 $/Tag. Sharpe 1,55, geschrumpft 0,88.
- Live seit 18.08.2026 unbeaufsichtigt auf der Box (NT8, MaxRiskGuard, Telegram). Live-Abgleich: trade-identisch bis auf 1 Tick.
- Discovery: seit 21.08. ~65.000 Trials, **0 neue Mechanismen** im Live-Buch. Das ist der ehrlichste Satz über den Stand: das System ist technisch weit, die Edge ist schmal.

### Prop-Firm-Accounts
| Konto | Kauf | Stand |
|---|---|---|
| E8 Signature 50k (E61803453048) | 113 $ (Liste 150 $, Rabatt) | 49.870 $ (22.09.), also −130 $ |
| FundedNext Flex 50k FN1 | 69,99 $ (Coupon AUGFLEX, Liste 133,99 $) | +929,80 $ (21.09.) |
| FundedNext Flex 50k FN2 | 69,99 $ (Coupon AUGFLEX, Liste 133,99 $) | +959,30 $ (21.09.) |
| Geplant | E8 150k 390 $ (02.10.), danach Kaufrunde jeden 1. Freitag | Deckel 2.500 $ netto |

### Infrastruktur
Contabo-VPS (Box, 31,06 €/Monat brutto laut Rechnung), PC, Laptop als Zweitgerät, Tailscale, Git-Vault, NT8 über Tradovate. Kein TradingView. Daten: 16 Jahre 1m-Daten vorhanden, Databento geplant.

### Stärken
- **Kosten sind klein und planbar.** Kein Kredit, kein Lager, kein Personal. Das maximale Risiko ist hart gedeckelt.
- **Automatisiert.** Das System handelt ohne dich, das passt zu Job, BOS und Nebengewerbe.
- **Dokumentation ist schon da.** Belegordner, EÜR-CSV, Logbuch. Buchhaltung ist für dich kein Neuland.
- **Nebentätigkeit genehmigt**, die größte rechtliche Hürde aus dem Arbeitsvertrag ist weg.
- **Steuerberatung in Reichweite** durch deine Freundin.

### Risiken
- **Edge ist nicht belegt.** Live bisher −130 $ auf E8, FN leicht im Plus, null Payouts. Der realistische erste Payout lag in der Planung vom 24.08. bei 11 bis 18 Monaten.
- **Einkommen bricht am 03.07.2027 weg**, danach BOS ohne Gehalt. Jeder Euro, der bis dahin in Prop-Käufe und Hardware geht, fehlt in der BOS-Zeit.
- **Counterparty-Risiko:** Prop Firms können Regeln ändern, Konten schließen oder Payouts verweigern.
- **Liebhaberei-Risiko:** mehrere Jahre Verluste ohne Payout können dazu führen, dass das Finanzamt die Verluste rückwirkend nicht anerkennt.

---

## 2. Geplante Ausgabenanalyse

Wechselkurs für die Rechnung: 1 $ ≈ 0,87 €. Zeitraum „bis Juli" = Okt. 2026 bis Juni 2027 (9 Monate).

| Position | Kosten | Geschäftl. Notwendigkeit | Steuerliche Relevanz | Prio | Nutzen fürs Unternehmen |
|---|---|---|---|---|---|
| **Prop-Challenges** (E8/FN) | bis 2.500 $ netto (≈ 2.150 €), Deckel AP204 | **Kern.** Ohne Eval kein Payout | Voll Betriebsausgabe. Leistung aus Drittland → §13b (siehe 4.5) | 🔴 hoch | Einzige Umsatzquelle |
| **Prop-Accounts / Resets / Aktivierung** | Reset FN 150k 278,99 $, Aktivierungsgebühren je Firma | Kern, im Deckel enthalten | Betriebsausgabe | 🔴 hoch | Hält Konten am Leben |
| **VPS Contabo** | 31,06 €/Monat brutto (26,10 € netto) → ≈ 280 € | **Kern.** Hier läuft alles | Betriebsausgabe, deutsche Rechnung mit 19 % USt → Vorsteuer möglich (nur bei Regelbesteuerung) | 🔴 hoch | Handel, Runner, Watchdog |
| **Claude Max 5x** | 90 € netto, heute 107,10 € brutto mit 19 % deutscher USt (Belege Juni bis Sept.) → ≈ 810 € netto | Hoch, Engine/Discovery/Doku laufen darüber | Betriebsausgabe, geschäftlichen Anteil realistisch ansetzen (du nutzt ihn auch privat). Anthropic sitzt in der EU (Irland) → mit USt-IdNr. §13b | 🔴 hoch | Entwicklungs-Produktivität |
| **Anthropic API** (Strategy Developer) | nutzungsabhängig, unbekannt | Mittel | Betriebsausgabe | 🟡 mittel | Developer-Tab |
| **Databento** | Annahme: 100 bis 300 € einmalig für historische Daten (nutzungsbasiert, ~0,10 $/Symbol für 10 J. 1m laut Recherche) | Mittel. Neue Märkte = neue Mechanismen = Sharpe | Betriebsausgabe, US-Anbieter → §13b | 🟡 mittel | Direkt auf das eine Ziel „Sharpe hoch" |
| **Neuer Monitor** | Annahme 300 bis 500 € | Mittel, kommt ohnehin | Anschaffung, Computer-Hardware seit 2021 mit **1 Jahr Nutzungsdauer** → komplett im Kaufjahr absetzbar. **Nur der geschäftliche Anteil** | 🟡 mittel | Arbeitsplatz |
| **Neuer PC** | Annahme 1.200 bis 2.000 € | Mittel, kommt ohnehin | wie Monitor. Kaufzeitpunkt 2026 vs. 2027 ist steuerlich relevant (siehe 4.5) | 🟡 mittel | Lokales Rechnen, Entwicklung |
| **Domain** | ≈ 15 €/Jahr | Niedrig jetzt, wichtig ab öffentlicher Doku (Ziel Schritt 2) | Betriebsausgabe | 🟢 niedrig | Marke für späteres Publikum/Mentorship |
| **Hosting** | 0 € jetzt (Artifacts/GitHub Pages reichen) | Niedrig | Betriebsausgabe, falls später | 🟢 niedrig | erst mit Mentorship |
| **Software** (NT8, Tradovate) | bisher keine Kosten bekannt, Lizenz kommt über die Prop Firms (prüfen) | Kern, aber kostenlos | Betriebsausgabe falls Kosten | ⚪ prüfen | Handelsplattform |
| **Weitere KI-Abos** | keine | Nicht nötig, Claude deckt es ab | nur geschäftlicher Anteil | ⚪ nein | kein Mehrwert erkennbar |
| **Cloud** (Tailscale, GitHub) | 0 € | Kern, kostenlos | keine | ⚪ | Fernzugriff, Versionierung |
| **Gründungskosten** | Gewerbeanmeldung ≈ 20 bis 60 €, Geschäftskonto 0 bis 10 €/Monat | Pflicht bzw. empfohlen | Betriebsausgabe | 🔴 hoch | sauberer Start |
| **Sonstige Hardware** | keine geplant | nein | | ⚪ | |

### Kapitalbedarf bis Juli 2027 (Okt. 2026 bis Juni 2027)

| Block | Betrag |
|---|---|
| Laufend (Claude, Contabo, Domain, Konto) | ≈ 1.120 € |
| Prop (Deckel netto) | ≈ 2.150 € |
| Databento | ≈ 200 € |
| **Summe ohne Hardware** | **≈ 3.500 €** |
| Monitor + PC | ≈ 1.500 bis 2.500 € |
| **Summe mit Hardware** | **≈ 5.000 bis 6.000 €** |

**Gegenrechnung:** Bis Juli kommen ≈ 5.400 € aufs Konto. Ohne Hardware frisst das Geschäft rund zwei Drittel davon, mit Hardware praktisch alles. Payouts würden den Prop-Block zurückfüllen, einplanen darf man sie aber nicht.

### Kapitalbedarf bis Start Vollzeit-Selbstständigkeit (04.07.2027) und danach
Der Start fällt praktisch auf „bis Juli", also gleiche Zahl. Wichtiger ist, **was danach fehlt**:

| Posten ab 04.07.2027 | pro Monat |
|---|---|
| Laufende Geschäftskosten (Claude, Box) | ≈ 125 € |
| Prop-Budget (Politik ≈ 300 $/Monat) | ≈ 260 € |
| Krankenversicherung, falls du nicht mehr familienversichert bist (freiwillig, Mindestbeitrag, **prüfen**) | ≈ 230 bis 260 € |
| Lebenshaltung | **unbekannt**, fehlt in diesem Dokument |

Zwei Jahre BOS mit nur den Geschäftskosten und dem Prop-Budget sind ≈ 9.000 €, ohne Payouts. **Das ist der eigentliche Engpass, nicht die Gründung.** Die Gründung selbst kostet fast nichts.

---

## 3. Geschäftsmodell

### Produkt
Ein eigenes, automatisiertes Handelssystem für Index-Futures (NQ/ES, NinjaTrader 8), bestehend aus:
- einem Portfolio unkorrelierter, regelbasierter Strategien (aktuell 3 Beine),
- einer Backtest- und Discovery-Engine, die neue Strategien nach festen statistischen Gates prüft (Walk-Forward, PBO/DSR, Nulldrift-Kontrolle, Buch-Marginal),
- einer Betriebsinfrastruktur (VPS, RiskGuard mit firmenspezifischen Regeln, Watchdog, Telegram).

### Dienstleistung (so wie es steuerlich und rechtlich tatsächlich läuft)
Du erbringst eine **Handelsleistung auf simulierten Konten für ausländische Prop Firms** (E8: USA/Saint Lucia, FundedNext: außerhalb EU) und wirst bei Erfolg am simulierten Gewinn beteiligt (E8 80 %, FN funded 95 %). Du handelst **kein eigenes Kapital und kein fremdes Kapital**. Das ist wichtig: keine Anlageberatung, keine Vermögensverwaltung, keine BaFin-Erlaubnis nötig.

### Wertschöpfung
Eval-Gebühr rein (Kosten) → System besteht die Eval → Funded-Konto → Payouts. Die Wertschöpfung steckt komplett in der Software: Edge finden, sauber prüfen, regelkonform ausführen. Deine Arbeitszeit skaliert nicht mit der Kontenzahl.

### Wettbewerbsvorteile
- **Methodik statt Bauchgefühl:** Gates, Register gegen Zufallsdecke, Friedhof mit Reichweite. Die meisten Prop-Trader haben nichts davon.
- **Firmenregeln als Code** (Consistency-Deckel, Flat-Zeiten, Bust-Schutz), nicht als Erinnerung.
- **Automatisierung:** kein Diskretionsfehler, läuft neben Job und Schule.
- **Dokumentierter Weg** (Vault, Logbuch): später das Rohmaterial für das Wissensprodukt.

### Skalierungsmöglichkeiten
- Mehr Konten parallel, begrenzt durch Firmenregeln (E8 max. 5 aktive Performance-Konten je Haushalt, FN bis 750k inkl. Challenges).
- Mehr Firmen (Diversifikation gegen Counterparty-Risiko).
- Neue Märkte und Mechanismen (GC, CL, weitere) → höherer Sharpe → kürzere Zeit bis Ziel.
- Später: eigenes Live-Konto, dann Mentorship/Wissensprodukt (Prozess, nie Signale).

### Technologische Besonderheiten
Eigene Engine mit ehrlichen Fills (Intraday-Bust-Check, Kosten, OOS), Discovery-Queue als Dauerdienst, deterministische Qualitätssicherung über Hooks, Box-Deploy ohne Handarbeit.

### Risiken
| Risiko | Einschätzung |
|---|---|
| Edge zu klein oder verschwindet | hoch |
| Prop Firm ändert Regeln, schließt oder zahlt nicht | mittel |
| Technischer Ausfall (Box, NT8, RiskGuard) | mittel, gut abgesichert |
| Zu viele Konten auf einmal gekauft (Größe kauft Bust) | niedrig, weil Deckel |

### Realistische Umsatzquellen
| Quelle | wann | realistisch |
|---|---|---|
| Prop-Payouts | erster Payout frühestens Anfang/Mitte 2027 | Schätzung 18.09.: ≈ 730 $/Monat bei 5 Konten, sobald die laufen. tempo_plan: Median 36 bis 102 Monate bis 50.000 $ brutto, je nach Edge-Annahme |
| Mentorship/Wissensprodukt | erst nach 12 Monaten Live-Beleg | 0 in den nächsten 2 Jahren |
| Softwareentwicklung/IT-Dienstleistung | im Tätigkeitstext mit drin | von dir aktuell nicht geplant, bleibt als Option offen |

### Langfristige Entwicklung
Track Record → eigenes Konto (100k) → Wissensprodukt → Vermögensaufbau. Das Gewerbe ist dabei die Hülle, in der der Track Record **steuerlich belegt** entsteht. Genau das braucht die Bank später.

---

## 4. Gründung jetzt oder später?

### 4.1 Vorteile einer sofortigen Gründung (Okt. 2026)
1. **Verluste zählen nur, solange Gehalt da ist.** 2026 (Ausbildung bis Juli, dann Job) liegt dein Grenzsteuersatz bei ≈ 27,5 %, 2027 (13. Gehalt, Job bis 03.07.) bei ≈ 26 %, jeweils inkl. Kirchensteuer. Verluste aus dem Gewerbe werden direkt mit dem Gehalt verrechnet. Im BOS-Jahr ohne Gehalt liegst du unter dem Grundfreibetrag, dort ist ein Verlust nur noch Vortrag. **Kosten vor Juli 2027 sind deutlich mehr wert als danach.** (Korrigiert 23.09.: die erste Fassung ging fälschlich von 12 vollen Gehältern in 2026 aus.)
2. **Hardware im Dezember 2026 kaufen** und komplett im Jahr 2026 absetzen (1 Jahr Nutzungsdauer). Beispiel: 2.000 € Hardware, 60 % geschäftlich → 1.200 € Betriebsausgabe → ≈ 360 € weniger Einkommensteuer.
3. **Bank-Uhr läuft früher.** Prop-Einkommen zählt für die Bank erst nach 2 bis 3 Steuerbescheiden. Gewerbe ab 2026 heißt: erster Bescheid für 2026, nicht für 2027.
4. **Anmeldepflicht ist wahrscheinlich schon da.** Nach §14 GewO meldest du mit Beginn der Tätigkeit an. Du handelst seit 18.08. live mit echtem Geldeinsatz (Eval-Gebühren) und klarer Gewinnabsicht. „Später" ist also nicht neutral, sondern eigentlich schon spät. (Verspätete Anmeldung ist eine Ordnungswidrigkeit, in der Praxis bei Nebengewerbe selten ein Problem, aber unnötig.)
5. **Alles ist vorbereitet:** Nebentätigkeit genehmigt, Formular vorformuliert, Gewerbeamt bekannt, Belegordner steht. Der Aufwand ist ein Nachmittag.
6. **Kein Stress beim ersten Payout.** Der kommt irgendwann ohne Vorwarnung. Dann ist die Hülle schon da.

### 4.2 Nachteile einer sofortigen Gründung
1. **Buchhaltung ab sofort:** EÜR, Belege sammeln, ggf. Umsatzsteuer-Voranmeldungen (bei Regelbesteuerung oder §13b).
2. **Liebhaberei-Frage:** Verluste 2026/2027 ohne Payout. Das Finanzamt akzeptiert Anlaufverluste meist, kann Bescheide aber vorläufig machen und später kippen, wenn nie Gewinn kommt.
3. **§13b-Falle als Kleinunternehmer:** Sobald du Unternehmer bist, schuldest du auf Leistungen ausländischer Anbieter (Evals, Claude mit USt-IdNr., Databento) selbst 19 % Umsatzsteuer. Als Kleinunternehmer ohne Vorsteuerabzug ist das echte Mehrkosten (siehe 4.5).
4. **Krankenversicherung in der BOS** kann teurer werden, wenn Gewerbegewinne die Familienversicherungs-Grenze reißen (siehe 4.7). Betrifft aber nur Gewinne, und die Frage stellt sich bei späterer Gründung genauso.

### 4.3 Vorteile einer späteren Gründung (z. B. erst beim ersten Payout)
1. Kein Buchhaltungsaufwand, solange nichts reinkommt.
2. Keine Liebhaberei-Diskussion, wenn das Projekt vorher scheitert.
3. Keine §13b-Pflichten auf die Eval-Käufe bis dahin.

### 4.4 Nachteile einer späteren Gründung
1. **Du verschenkst die Absetzbarkeit im teuersten Jahr** (2026) oder musst die Kosten später mühsam als vorweggenommene Betriebsausgaben nachweisen, bei niedrigerem Steuersatz.
2. **Erster Payout fällt vermutlich in 2027 oder in die BOS-Zeit.** Dann gründest du genau in der Phase mit Jobende, Schulstart und KV-Umstellung. Schlechtestes Timing für Papierkram.
3. Bank-Uhr startet ein Jahr später.
4. Die Anmeldepflicht besteht wahrscheinlich schon (siehe 4.1 Punkt 4).

### 4.5 Steuerliche Auswirkungen

**Einkommensteuer**
- Einkunftsart: Der Vault geht von **gewerblichen Einkünften** (§15 EStG) aus. Das ist die übliche Einordnung, weil du nachhaltig eine Leistung gegen Vergütung erbringst und kein eigenes Kapital anlegst. Die Alternative „sonstige Einkünfte" (§22 Nr. 3) wäre für dich schlechter (Verluste nur begrenzt verrechenbar). **→ mit Freundin klären.**
- Verluste 2026 werden mit dem Gehalt verrechnet → Erstattung über die Steuererklärung 2026.
- Gewerbesteuer: erst ab 24.500 € Gewinn/Jahr relevant, und wird dann größtenteils auf die Einkommensteuer angerechnet. Für die nächsten Jahre egal.
- Steuerrücklage: die 42 % aus der alten Notiz sind bei deinem Einkommen zu vorsichtig. Realistisch ≈ 30 % auf Payouts bis Juli 2027, in der BOS-Zeit fast keine Einkommensteuer, dafür Krankenversicherung (siehe [[Gründung Zeitplan]]). **→ gegenrechnen lassen.**

**Umsatzsteuer: die wichtigste Entscheidung**

| | Kleinunternehmer (§19) | Regelbesteuerung |
|---|---|---|
| USt auf Payouts | keine (nicht steuerbar, Empfänger im Drittland) | **auch keine**, gleiche Logik |
| §13b auf Evals, Claude, Databento | **du zahlst 19 % obendrauf, ohne Erstattung** | 19 % angemeldet und sofort als Vorsteuer zurück = **null** |
| Vorsteuer auf Contabo, PC, Monitor (deutsche Rechnungen) | nein | **ja**, trotz nicht steuerbarer Umsätze, weil die Leistung an Empfänger im Drittland geht (§15 Abs. 2 Nr. 2 bzw. Abs. 3 Nr. 2 UStG, **prüfen**) |
| Aufwand | gering, aber bei §13b trotzdem Voranmeldungen | Voranmeldungen monatlich oder quartalsweise, Jahreserklärung |
| Bindung | keine | **5 Jahre**, wenn du auf §19 verzichtest |

Grobe Rechnung für Okt. 2026 bis Juni 2027:
- §13b-Belastung als Kleinunternehmer: 19 % auf ≈ 2.150 € Prop + ≈ 810 € Claude + ≈ 200 € Databento ≈ **600 € Mehrkosten**.
- Vorsteuer bei Regelbesteuerung: Contabo ≈ 45 € + Hardware (geschäftlicher Anteil) ≈ 150 bis 250 € ≈ **200 bis 300 € zurück**.
- **Unterschied zugunsten Regelbesteuerung: ≈ 800 bis 900 € im ersten Jahr.**

Der Haken an der Regelbesteuerung ist die **5-Jahres-Bindung**. Wenn du in 2 bis 3 Jahren Mentorship an Privatkunden in Deutschland verkaufst, musst du 19 % USt ausweisen und abführen. Das macht das Produkt teurer. Ab dann rechnet man neu, nach 5 Jahren kannst du zurück.

Außerdem offen: Ist der Payout umsatzsteuerlich überhaupt ein Leistungsaustausch? Wenn das Finanzamt sagt „nein, das ist keine Leistung", gibt es auch keinen Vorsteuerabzug. **Das ist genau die Frage für deine Freundin.**

**Eine ehrliche Anmerkung zur Hardware:** Du hast gesagt, dass man die private Nutzung nirgendwo angeben muss. Einen Nachweis wie ein Fahrtenbuch verlangt beim PC zwar niemand. Wenn du den PC aber auch privat nutzt, ist 100 % geschäftlich schlicht falsch, und genau Hardware ist bei Neugründern mit Verlust ein beliebter Prüfpunkt. Üblich und sicher: ein plausibler Anteil (bei überwiegend Trading/Entwicklung z. B. 60 bis 80 %), oder 100 %, wenn private Nutzung wirklich unter 10 % liegt. Das kostet dich bei 2.000 € Hardware je nach Anteil ≈ 100 bis 250 € Steuerersparnis, dafür ist der Bescheid wasserdicht. Deine Freundin weiß, was das Finanzamt bei euch vor Ort durchwinkt.

### 4.6 Organisatorische Auswirkungen
- Gewerbeanmeldung (GewA 1, VG Oberneuching), danach automatisch Fragebogen zur steuerlichen Erfassung (ELSTER) → Steuernummer.
- IHK-Mitgliedschaft entsteht automatisch, als Kleingewerbe mit wenig Gewinn **beitragsfrei** (Neugründer-Befreiung).
- Keine Berufsgenossenschafts-Pflicht, solange du keine Angestellten hast.
- **Arbeitsuchend melden** bei der Agentur für Arbeit spätestens 3 Monate vor Vertragsende, also **bis ca. 03.04.2027**. Pflicht bei befristeten Verträgen, sonst Sperrzeit, falls du ALG I beantragst.
- **Juli/August 2027:** Hier gibt es eine Alternative zu „Vollzeit selbstständig": arbeitslos melden, ALG I beziehen (grob ≈ 60 % vom Netto, KV läuft mit) und das Gewerbe **unter 15 h/Woche** weiterführen. Weil das System automatisch handelt, ist das realistisch. Das geht aber nur, wenn du in der Zeit wirklich für Arbeit zur Verfügung stehst. Mit festem BOS-Start ab September muss die Agentur das akzeptieren. **→ bei der Agentur fragen, nicht annehmen.** Wenn du hauptberuflich selbstständig bist, fällt ALG I weg und du zahlst die KV selbst.

### 4.7 Auswirkungen auf zukünftige Förderungen
- **Gründungszuschuss:** Setzt ALG-I-Anspruch mit ≥ 150 Resttagen und eine **hauptberufliche** Gründung voraus. Mit BOS ab September ist das für dich nicht erreichbar, egal wann du gründest. Eine Anmeldung jetzt verschlechtert nichts.
- **KfW/Gründerkredite:** kein Kapitalbedarf, irrelevant.
- **Schüler-BAföG für die BOS:** Gewinne aus dem Gewerbe zählen als Einkommen und können den BAföG-Anspruch kürzen. Verluste schaden nicht. Das Problem entsteht erst mit Gewinn, unabhängig vom Gründungszeitpunkt. **→ prüfen, ob du überhaupt BAföG-berechtigt bist.**
- **Familienversicherung (KV) in der BOS:** bis 25 als Schüler möglich, wenn ein Elternteil gesetzlich versichert ist, du **nicht hauptberuflich selbstständig** bist und dein Gesamteinkommen unter ≈ 565 €/Monat liegt (Grenze 2026, **prüfen**). Gewerbegewinn zählt nach Steuerbescheid mit. Heißt: sobald Payouts laufen, bist du vermutlich raus und zahlst selbst ≈ 230 bis 260 €/Monat. **Das gehört in die Rechnung, ob sich die Payouts in der BOS-Zeit lohnen.**

### 4.8 Auswirkungen auf Buchhaltung und Verwaltung
| Aufgabe | Aufwand |
|---|---|
| Belege sammeln (Ordner steht schon) | laufend, 10 Min./Woche |
| EÜR-CSV fortschreiben | monatlich, 30 Min. |
| USD-Umrechnung (Payouts, Käufe) | Tageskurs oder EZB-Monatskurs |
| USt-Voranmeldung (Regelbesteuerung oder §13b) | monatlich oder quartalsweise, je 15 Min. über ELSTER |
| Anlage EÜR + Gewerbesteuer- + USt-Jahreserklärung | 1x im Jahr |
| Aufbewahrung | 8 Jahre Buchungsbelege |
| E-Rechnungen empfangen können | seit 2025 Pflicht, praktisch: PDF/XML-Postfach reicht |

Das meiste davon kann ein Skript übernehmen (Logging-Skript pro Konto, schon als Idee in [[Steuer & Gewerbe (Prop-Payouts)]]).

### 4.9 Fazit Abschnitt 4
Die Gründung kostet fast nichts, der Aufwand ist überschaubar und größtenteils schon vorbereitet. Der Nutzen ist **jetzt am größten**, weil du nur bis Juli 2027 Gehalt hast, gegen das Verluste verrechnet werden, und er schrumpft mit jedem Monat, den du wartest. Die echten Risiken (Liebhaberei, KV in der BOS, BAföG) hängen am Gewinn oder am Verlauf, **nicht am Gründungszeitpunkt**.

---

## 5. Agenda: Termin mit deiner Freundin

> [!note] Ausführlicher Fragenkatalog zum Mitnehmen (inkl. ihrer Meinung): [[Gespräch mit Freundin (Steuer & Gründung)]]

> [!tip] Vorbereitung für den Termin
> Mitbringen: Arbeitsvertrag (§8) + Genehmigung Nebentätigkeit, Kontoauszüge/Belege der Eval-Käufe seit August (E8 113 $, FN 2x 69,99 $, Bulenox 43,75 $, alle abgelegt), Contabo-Rechnungen, Claude-Rechnungen, dieses Dokument.

### Steuerliche Themen (Grundsatz)
| | |
|---|---|
| **Warum wichtig** | Alles andere hängt an der Einordnung der Payouts |
| **Entscheidung** | Gewerbliche Einkünfte (§15) oder sonstige Einkünfte (§22 Nr. 3)? Umsatzsteuerlich Leistungsaustausch ja/nein? |
| **Fehlt aktuell** | Kennt sie Mandanten mit Prop-Trading? Gibt es eine Verfügung oder Praxis beim Finanzamt Erding? |

### Gewerbeanmeldung
| | |
|---|---|
| **Warum wichtig** | Pflicht mit Beginn der Tätigkeit, Startpunkt für alles |
| **Entscheidung** | Beginndatum: 18.08.2026 (Live-Start) oder 01.10.2026? Passt der Tätigkeitstext? |
| **Fehlt aktuell** | Nichts, Formular ist vorbereitet. Nur die Datumsfrage |

### Einzelunternehmen
| | |
|---|---|
| **Warum wichtig** | Rechtsform bestimmt Aufwand und Kosten |
| **Entscheidung** | Einzelunternehmen (Empfehlung) vs. UG. UG lohnt erst bei deutlich fünfstelligem Gewinn und die Prop Firms zahlen ohnehin an natürliche Personen (KYC) |
| **Fehlt aktuell** | Bestätigung, dass Einzelunternehmen für die nächsten Jahre reicht |

### Umsatzsteuer
| | |
|---|---|
| **Warum wichtig** | ≈ 800 bis 900 €/Jahr Unterschied, 5-Jahres-Bindung |
| **Entscheidung** | Kleinunternehmer oder Regelbesteuerung? Muss im Fragebogen angekreuzt werden |
| **Fehlt aktuell** | Einschätzung, ob Vorsteuerabzug bei nicht steuerbaren Payouts ans Drittland hält. Gilt für Neugründer 2027 monatliche Voranmeldung? Wie wirkt die Bindung auf ein späteres Mentorship-Produkt? |

### Vorsteuerabzug
| | |
|---|---|
| **Warum wichtig** | Hauptgrund für die Regelbesteuerung |
| **Entscheidung** | Welche Kosten ziehen Vorsteuer (Contabo, Hardware), wie wird die private Nutzung bei der Vorsteuer behandelt (Zuordnung, unentgeltliche Wertabgabe)? |
| **Fehlt aktuell** | Rechnungen auf deinen Namen mit Adresse? Bisherige Rechnungen korrigierbar? |

### Betriebsausgaben
| | |
|---|---|
| **Warum wichtig** | Verluste 2026 senken deine Steuer auf das Gehalt |
| **Entscheidung** | Was ist Betriebsausgabe, was vorweggenommene Betriebsausgabe (Käufe seit August)? Arbeitszimmer/Arbeitsecke (Homeoffice-Pauschale neben dem Job?) |
| **Fehlt aktuell** | Vollständige Belegliste seit August |

### Hardwarekäufe
| | |
|---|---|
| **Warum wichtig** | Größter Einzelposten, Timing 2026 vs. 2027 |
| **Entscheidung** | Im Dezember 2026 kaufen? Welcher Geschäftsanteil ist bei Monitor und PC vertretbar? |
| **Fehlt aktuell** | Konkrete Kaufpreise, dein ehrlicher Privatanteil |

### Software-Abonnements
| | |
|---|---|
| **Warum wichtig** | Claude ist der größte laufende Posten |
| **Entscheidung** | Geschäftsanteil Claude? USt-IdNr. bei Anthropic hinterlegen (dann §13b) oder als Privatkunde lassen? |
| **Fehlt aktuell** | Wie Anthropic aktuell abrechnet (mit/ohne deutsche USt) |

### Prop-Firm-Accounts
| | |
|---|---|
| **Warum wichtig** | Kern des Geschäfts, beide Richtungen in USD über Drittland |
| **Entscheidung** | Eval-Gebühr = Betriebsausgabe, §13b ja/nein? Payout-Zeitpunkt = Zufluss bei Gutschrift? Welcher Kurs? |
| **Fehlt aktuell** | Welche Entity rechnet genau ab (E8 LLC USA oder Ltd Saint Lucia, FundedNext wo)? |

### Datenanbieter
| | |
|---|---|
| **Warum wichtig** | Databento ist geplant, US-Anbieter |
| **Entscheidung** | §13b, Betriebsausgabe sofort |
| **Fehlt aktuell** | Konkreter Betrag |

### Geschäftskonto
| | |
|---|---|
| **Warum wichtig** | Trennung privat/geschäftlich, weniger Chaos in der EÜR, AP37 offen |
| **Entscheidung** | Revolut Business (Payouts in USD) oder einfaches zweites Girokonto? Steuer-Rücklagenkonto mit welcher Quote? |
| **Fehlt aktuell** | Nichts, nur Wahl |

### Buchhaltung
| | |
|---|---|
| **Warum wichtig** | EÜR-Pflicht, Grundlage für die Bank später |
| **Entscheidung** | Selbst mit CSV + Skript, oder Software (z. B. lexoffice/sevdesk)? Soll sie die Erklärung machen? |
| **Fehlt aktuell** | Was sie bei ihrem Arbeitgeber nebenbei darf (siehe unten) |

### Digitale Belegverwaltung
| | |
|---|---|
| **Warum wichtig** | GoBD, 8 Jahre Aufbewahrung, E-Rechnung |
| **Entscheidung** | Reicht der Ordner `Documents\Gewerbe\Belege` + Backup? Namensschema? |
| **Fehlt aktuell** | Backup-Ort (Ordner liegt nur lokal am PC?) |

### Eventuelle Beschäftigung deiner Freundin
| | |
|---|---|
| **Warum wichtig** | Klingt nach Steuertrick, rechnet sich aber nur mit echten Umsätzen |
| **Entscheidung** | Jetzt nicht, später Minijob (Grenze 2026: 603 €/Monat) für Belegverwaltung/Buchhaltung? |
| **Fehlt aktuell** | Darf sie das neben ihrem Hauptjob (Nebentätigkeit beim Steuerbüro, Steuerberatungsgesetz)? Ihr wohnt nicht zusammen, das Finanzamt prüft trotzdem Fremdvergleich (Vertrag, echte Arbeit, echte Zahlung) |

**Meine Einschätzung dazu:** Solange keine Payouts kommen, erhöht ein Gehalt an sie nur deinen Verlust. Rechnung pro 100 € Lohn: +≈ 31 € Minijob-Abgaben, −≈ 39 € Steuerersparnis bei dir. Für euch beide zusammen ist das fast eine Nullnummer, dafür kommen Minijobzentrale, Lohnabrechnung und Berufsgenossenschaft dazu, und das Liebhaberei-Risiko steigt. **Frühestens, wenn regelmäßige Payouts da sind.**

---

## 6. Kritische Gegenprüfung (konservativer Steuerberater und Unternehmer)

> Rolle: jemand, der dir die Gründung ausreden will und nach Gründen sucht.

| # | Einwand | Bewertung |
|---|---|---|
| 1 | **„Du hast null Umsatz und keine belegte Edge.** Live −130 $ auf E8, 0 Payouts, 0 neue Mechanismen aus 65.000 Trials. Du gründest ein Unternehmen, das es wirtschaftlich noch nicht gibt." | 🔴 **hoch.** Stimmt. Das Gegenargument ist nur, dass die Gründung fast nichts kostet und die Kosten ohnehin anfallen |
| 2 | **Liebhaberei.** Wenn 2026 bis 2028 nur Verluste kommen, kann das Finanzamt die Verluste rückwirkend streichen. Die Eval-Käufe wirken für einen Prüfer wie ein Glücksspiel-Hobby | 🟡 **mittel.** Deine Doku (Logbuch, Engine, Gates) ist das beste Gegenmittel, das es gibt. Bescheide werden ggf. vorläufig |
| 3 | **Umsatzsteuerliche Einordnung ist ungeklärt.** Wenn der Payout kein Leistungsaustausch ist, fällt der Vorsteuerabzug weg und du hast dich 5 Jahre an die Regelbesteuerung gebunden, ohne Vorteil, mit Voranmeldungen | 🟡 **mittel.** Genau deshalb erst Freundin, dann Fragebogen |
| 4 | **Kasse bis Juli ist knapp.** Mit Hardware und vollem Prop-Deckel ist dein ganzer Cash-Zuwachs bis Juli weg, und danach kommt kein Gehalt mehr | 🔴 **hoch.** Nicht wegen der Gründung, sondern wegen der Ausgaben. Hardware nur kaufen, wenn die BOS-Zeit trotzdem gedeckt ist |
| 5 | **Lebenshaltung in der BOS ist nicht geplant.** Das Dokument kennt deine Fixkosten nicht | 🔴 **hoch.** Übersehener Punkt, gehört vor jede Kaufentscheidung |
| 6 | **Krankenversicherung.** Gewinn in der BOS → raus aus der Familienversicherung → ≈ 230 bis 260 €/Monat. Juli/August „Vollzeit selbstständig" → KV komplett selbst | 🟡 **mittel.** Planbar, aber muss in die Rechnung |
| 7 | **„Vollzeit selbstständig" im Juli/August** ist bei einem automatischen System vor allem ein Etikett. Es kostet dich ALG I und die KV-Deckung für zwei Monate | 🟡 **mittel.** Bei der Agentur klären (Abschnitt 4.6) |
| 8 | **Nebentätigkeits-Genehmigung ist widerruflich** (§8.4). Wenn GEWO widerruft, musst du bis 03.07.2027 aufhören oder abmelden | 🟢 **niedrig.** Automatisiert, kein Wettbewerb, Vertrag endet ohnehin bald |
| 9 | **Prop Firms sind unreguliert.** Ein Payout-Stopp oder eine Pleite (bei anderen Firmen schon passiert) trifft dich ohne Rechtsweg | 🟡 **mittel.** Zwei Firmen statt einer ist schon die richtige Antwort |
| 10 | **Beratung durch die Freundin ersetzt keinen Steuerberater.** Unentgeltliche Hilfe in Steuersachen ist rechtlich nur für Angehörige frei, eine Freundin ist das formal nicht. Und bei Streit mit dem Finanzamt fehlt dir die Haftung eines Beraters | 🟢 **niedrig** jetzt, 🟡 **mittel** ab echtem Gewinn (Notiz sagt: STB ab ≈ 30.000 € Gewinn) |
| 11 | **CME-Datenstatus.** Wenn du irgendwo „Nutzung für ein Unternehmen" angibst, kann ein Datenanbieter dich als Professional einstufen, das ist deutlich teurer | 🟢 **niedrig.** Einzelunternehmer bleiben meist Non-Pro, Formulare genau lesen |
| 12 | **BAföG.** Gewinne können den Anspruch kürzen, und du weißt noch nicht, ob du überhaupt Anspruch hast | 🟢 **niedrig**, solange keine Gewinne |
| 13 | **Hardware zu 100 % absetzen, obwohl privat genutzt.** Beliebter Prüfpunkt bei Verlust-Neugründern, im Zweifel wird alles gestrichen | 🟡 **mittel.** Mit ehrlichem Anteil: 🟢 niedrig |
| 14 | **Die alte Leitplanke „Job behalten" in deinen Notizen passt nicht mehr** zu Vertragsende und BOS. Das Gehalt als Kredit-Asset fällt ab Juli 2027 weg, die Bank-Strategie braucht damit einen neuen Plan | 🟡 **mittel.** Kein Gründungsthema, aber ein Planungsthema |

**Was der konservative Berater am Ende trotzdem zugeben muss:** Keiner der Einwände wird durch späteres Gründen kleiner. Einwand 1, 4, 5 und 6 sind Argumente gegen **Ausgaben**, nicht gegen die **Anmeldung**.

---

## 7. Empfehlung

> [!success] **Sofort gründen** (Oktober 2026, Nebengewerbe, Einzelunternehmen), direkt nach dem Termin mit deiner Freundin.

**Begründung, nur aus deiner Situation:**
1. **Dein Gehalt endet am 03.07.2027.** Bis dahin bringt jeder Euro Betriebsausgabe ≈ 26 bis 28 Cent zurück, danach im BOS-Jahr praktisch nichts. Wer wartet, verschenkt genau das.
2. **Die Kosten laufen ohnehin.** Evals (Kaufplan steht, Start 02.10.), Claude, Box, Hardware und Databento hast du so oder so. Ohne Gewerbe sind sie steuerlich wertlos oder mühsam nachzuweisen.
3. **Die Anmeldepflicht besteht wahrscheinlich schon** seit dem Live-Start am 18.08. Mit der Genehmigung von heute ist die letzte Hürde weg.
4. **Dein großes Ziel braucht Steuerbescheide.** Track Record plus bankfähiges Einkommen ist das Asset. Jede EÜR ab 2026 ist ein Jahr früher Beleg.
5. **Der erste Payout wird wahrscheinlich in die schlechteste Phase fallen** (Jobende, BOS-Start, KV-Wechsel). Die Hülle muss vorher stehen.
6. **Die Risiken hängen nicht am Zeitpunkt.** Liebhaberei, KV und BAföG werden erst mit Gewinn oder über Jahre relevant, egal ob du im Oktober oder im Juli anmeldest.

**Warum nicht „erst bei den ersten Umsätzen":** Dein Geschäft hat eine lange Kostenphase vor dem ersten Umsatz (Planung: 11 bis 18 Monate bis zum ersten Payout). Genau diese Phase fällt in die Zeit, in der du noch Gehalt hast. Warten wäre nur sinnvoll, wenn die Kosten klein und der Steuersatz später höher wäre. Bei dir ist es umgekehrt.

**Was die Empfehlung NICHT heißt:** mehr ausgeben. Die Gründung ist fast kostenlos, die Ausgaben sind das Risiko. Den Deckel von 2.500 $ nicht anheben, und die Hardware erst kaufen, wenn die BOS-Zeit durchgerechnet ist.

### Fahrplan
| Wann | Was |
|---|---|
| Diese/nächste Woche | Termin mit Freundin (Agenda Abschnitt 5). Entscheidung Kleinunternehmer vs. Regelbesteuerung |
| Direkt danach (Anfang Okt.) | GewA 1 an VG Oberneuching (AP34), Beginn laut Absprache |
| 1 bis 2 Wochen danach | Fragebogen steuerliche Erfassung über ELSTER (AP35), USt-IdNr. mit beantragen |
| Oktober | Geschäftskonto + Rücklagenkonto (AP37), Belege monatlich einsortieren (AP251, rückwirkende Belege mit AP36 erledigt) |
| Bis Ende Nov. | Lebenshaltung BOS + KV-Status klären (Eltern gesetzlich versichert?), BAföG-Anspruch prüfen |
| Dezember 2026 | Hardware kaufen, **wenn** die BOS-Rechnung es hergibt |
| Bis 03.04.2027 | Arbeitsuchend melden, dabei ALG-I-Option Juli/August klären |
| Anfang 2027 | Steuererklärung 2026 mit Anlage EÜR (Verlust mit Gehalt verrechnen) |

### Offene Punkte, die in diesem Dokument fehlen
- Monatliche Lebenshaltungskosten (Wohnen bei den Eltern? Miete?)
- Wie die Eltern krankenversichert sind (gesetzlich/privat)
- Kirchensteuerpflicht ja/nein
- Sonderzahlungen beim Gehalt (13. Gehalt, Urlaubsgeld)
- Konkrete Preise für Monitor/PC
