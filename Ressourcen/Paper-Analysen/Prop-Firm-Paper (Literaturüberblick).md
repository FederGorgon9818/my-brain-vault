---
tags:
  - ressource/paper
  - trading/prop
  - research
erstellt: 2026-09-28
quelle: research-scout Seed + Workflow-Sweep (8 Suchwinkel), Session 81756f43
beleg: Abstract-/Suchtreffer-Ebene, kein Volltext gelesen (siehe Warnkasten)
---
# 📚 Prop-Firm-Paper (Literaturüberblick)

⬅️ [[_Paper-Registry]] · [[Prop-Eval-Passing (Fokus)]] · [[Research-Cache]]

Auftrag Max (28.09.2026): alle Research Paper finden, die sich speziell auf Prop Firms beziehen, jeweils mit **Why** (warum wurde das untersucht) und **was sie sagen**.

Gesucht wurde in drei Bedeutungen: **A** moderne Funded-/Eval-Firmen (E8, FTMO, Topstep ...), **B** klassische Prop-Trading-Firmen und Prop-Trader, **C** angrenzend institutionelle Principal Trading Firms (HFT) und Bank-Eigenhandel. Dazu Branchenberichte (D) und Glücksspiel-/Gamification-Arbeiten (E), jeweils getrennt markiert.

> [!warning] Beleg-Stufe: Abstract-Ebene, nicht Volltext
> Alles hier stammt aus Suchtreffern und Abstract-Seiten. **Kein Paper wurde im Volltext gelesen. Die Gegenprüfung lief nur gegen die Suchtreffer-Rohdaten (Korrekturleser, 25 Punkte eingearbeitet), nicht gegen die Originalquellen.** Grund: die Netzwerk-Policy dieser Cloud-Session sperrt SSRN, arXiv, OpenAlex, Semantic Scholar, Crossref, RePEc, federalreserve.gov, Springer und Google Scholar, und das WebSearch-Kontingent der Session (200 Suchen) war nach dem Sweep aufgebraucht. Zwei der acht Suchwinkel (graue Literatur/nicht-englisch, Datenbank-APIs) lieferten deshalb gar nichts.
> **Zahlen vor jeder Nutzung im Volltext prüfen** (Skill `/paper-edge`). Nächster Schritt steht unten.

---

## 🧭 Kurzfazit

1. **Es gibt seit Juli 2026 eine kleine, brandneue Literatur, die Prop-Challenges mathematisch als First-Passage-Problem rechnet** (A1 bis A5, fünf Preprints, alle ohne Peer-Review). Der Logbuch-Negativbefund „kein Paper zu Prop-Firm-First-Passage-Sizing“ ([[Strategie-Logbuch]] #074, Abschnitt Externe Research, Zeile ~700) ist damit überholt.
2. **Gemeinsamer Tenor:** zum Listenpreis sind die meisten Verträge für den Käufer im Erwartungswert negativ (29 von 31, A3). Mit Rabatt kann das kippen (siehe Break-even-Zahlen bei A1). Die Marge der Firmen sitzt im Kleingedruckten (Trailing-Frequenz, Breach-Check-Frequenz, Zeitlimit, Daily Loss Limit), dieselbe beworbene Kontogröße streut in der Erfolgswahrscheinlichkeit um 62 % (A4).
3. **Ohne Edge ist die Passquote nicht null**, sondern im Idealfall L/(T+L) (A1), bei E8 50k also 2.000/(3.000+2.000) = **40 %**. Bestehen ist deshalb kein Skill-Beweis (A5). Das ist von außen genau unsere Nulldrift-Pflicht (#106) und „Größe kauft Bust, nicht Tempo“.
4. **Die Branchenzahl mit der größten Datenbasis:** 14 % bestehen, rund 7 % aller Konten bekommen je einen Payout (FPFX Tech, 300.000+ Konten, 10 Firmen, D1). Branchenbericht, kein Paper.
5. **Klassische Prop-Trader-Forschung (B):** profitable Prop-Teams gibt es (SOES Bandits, Garvey & Murphy), aber Überleben ist selten (rund 15 % überstehen das erste Jahr, Locke & Mann 2015), bei Day-Tradern allgemein überwiegen die Verlierer, gelernt wird Risikotoleranz statt Skill, Dispositionseffekt und „Verlust am Vormittag, Risiko am Nachmittag“ kosten Geld. Für ein vollautomatisches Buch eher Bestätigung der Methode als neue Edge.
6. **Keine akademische Studie mit Trader-Daten einer modernen Funded-Firma gefunden** (nur der Branchenbericht D1, und Halls Kohorte mit offener Datenquelle). Einschränkung wie unten: Abstract-Ebene, 2 von 8 Suchwinkeln leer.

---

## A. Moderne Funded-/Eval-Prop-Firmen (Kern)

### A1. Villahermosa (2026): Prop-Firm Challenges: A Barrier Model of Pass Rates and Expected Value
- **Wo:** SSRN 7445798, Working Paper, Sept. 2026, kein Peer-Review. [Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7445798)
- **Why:** Warum bestehen so wenige Challenges, und wann lohnt sich der Kauf? Die Challenge wird als Barrier-Crossing-Problem modelliert: der Kontopfad muss das Target treffen, bevor er die Verlustgrenze trifft.
- **Was sie sagen:**
  - Für einen Trader ohne Drift gilt P(Pass) = **L/(T+L)** (Verlustlimit durch Target plus Verlustlimit), **unabhängig von Volatilität** (Optional Stopping).
  - Tägliches Flat, Trailing-Drawdown und Friktionen pro Trade drücken die reale Passquote darunter.
  - Break-even-Passquote für den Anbieter: **20 % bezogen auf die tatsächlich gezahlte Gebühr, 40 % auf den Listenpreis**, gegen 34,7 % für den modellierten mechanischen Teilnehmer. Was das für den Käufer bei Rabatt heißt, im Volltext prüfen.
  - Kalibriert mit 6 Jahren 1-Minuten-Index-Futures-Daten, zerlegt damit die Lücke zwischen Modell und Realität.
- **Für Max:** liefert die Nulllinie für unsere Rechnung. Unser Nulldrift-Zwilling in `tempo_plan.py`/`evaluate_v2` müsste bei statischer Barriere ungefähr L/(T+L) treffen, mit E8-Intraday-Check darunter. Guter unabhängiger Gegencheck (Quant-Team). „Unabhängig von Volatilität“ gilt nur bei statischer Barriere ohne Zeitlimit: dann ändert Größe ohne Edge das Tempo, nicht die Passchance. Mit Trailing, Daily Loss Limit oder Frist ändert Größe auch die Passchance (A2).

### A2. Lim (2026a): The Price of a Funded Account: An Actuarial Analysis of Proprietary Trading Firm Challenges
- **Wo:** SSRN 7178078, Working Paper, Juli 2026, kein Peer-Review. [Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7178078)
- **Why:** Was ist ein Challenge-Vertrag aus Käufersicht wert? Bewertung der Zwei-Stufen-Challenge wie ein Contingent Claim: Konto als arithmetische Brownsche Bewegung, First-Passage per Monte Carlo, inklusive Funded-Stufe, Profit-Split und Gebühren-Rückerstattung.
- **Was sie sagen:**
  - **Das Zeitlimit ist ein versteckter Vorteil für den Anbieter:** ein Trader ohne Edge besteht den reibungsfreien Benchmark mit p = 0,50, den Standardvertrag nur mit p = 0,30.
  - Der Vertragswert hängt an einem **schmalen Risiko-Grat nahe 2 % Tagesvolatilität**, der laut Abstract in der Vermarktung nicht offengelegt wird.
  - Modellierter Erwartungswert eines 500-$-Vertrags rund 221 $ unter einer illustrativen Baseline-Population (Lesart im Volltext prüfen).
- **Für Max:** der Risiko-Grat ist unsere Sizing-Frontier-Frage je Bein. Der Zeitlimit-Effekt passt zu unserem Bulenox-Check (Daily Note 28.09.): dort scheitert die Eval in der Rechnung an der 30-Tage-Frist. E8-Eval hat laut [[Research-Cache]] kein Zeitlimit, FN prüfen.

### A3. Lim (2026b): Phantom Generosity: Contract Design and Value in the Market for Proprietary-trading Evaluations
- **Wo:** SSRN 7184138, Working Paper, Juli 2026, Begleitpaper zu A2. [Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7184138)
- **Why:** Empirie statt Theorie: sind die beworbenen Angebote (Rabatte, große Konten, hohe Splits) wirklich großzügig?
- **Was sie sagen:**
  - Regelwerke und Gebühren von **31 Verträgen bei 21 Firmen** von Hand erhoben (Stand 25./26.07.2026, datierte Screenshots), alle auf derselben Benchmark-Population bewertet (300-Handelstage-Deckel, 1 Jahr Funded-Horizont).
  - **29 von 31 Verträgen haben zum Listenpreis einen negativen Erwartungswert**, noch bevor Consistency-Regeln, Payout-Caps und monatliche Gebühren eingerechnet sind.
- **Für Max:** die 31 Verträge sind ein fertiger Firmen-Vergleich. Im Volltext prüfen, ob E8 und FundedNext dabei sind und ob sie zu den zwei positiven gehören. Direkt relevant für AP248 (FN-Größe) und die Frage „dritte Firma“.

### A4. Tomàs Fernández (2026): Valuing Proprietary Trading Firm Evaluation Contracts: Closed Form, Cross-Firm Dispersion and the Source of the Margin
- **Wo:** SSRN 7260819, Working Paper 2026, Autor Martí Tomàs Fernández. [Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7260819)
- **Why:** Woher kommt die Marge der Firmen, wenn Target und Drawdown überall gleich beworben werden?
- **Was sie sagen:**
  - **Geschlossene Formel** für die Erfolgswahrscheinlichkeit als Kette von First-Passage-Problemen über sechs Vertragsparameter: Target, Drawdown-Puffer, Trailing-Level, Trailing-Frequenz, **Breach-Check-Frequenz**, Daily Loss Limit. Fehler unter 1 % gegen Simulation.
  - **13 Produkte gleicher Kontogröße: Erfolgswahrscheinlichkeit streut um 62 %**, obwohl Target und Puffer identisch beworben werden.
- **Für Max:** unser E8-Befund AP51 (EOD-Floor, aber Intraday-Check) ist vermutlich über den Parameter Breach-Check-Frequenz abbildbar (im Volltext prüfen). Stärkster Kandidat als unabhängiger Gegencheck für `cage_policy_lib`/`evaluate_v2`, und als Werkzeug, um neue Firmen vor dem Kauf zu vergleichen.

### A5. Hall (2026): Gate Design and Stage-Dependent Incentives in Retail Proprietary-Trading Evaluations: Why Passing Is Not Standalone Evidence of Skill, and Why the Product Fails to Pay Under Measured Trading Constraints
- **Wo:** arXiv 2609.14859 (q-fin.GN), Sept. 2026, 40 Seiten, 27 Tabellen, Code auf GitHub. Autor-Identität nicht geklärt (nicht sicher Prof. Nicholas G. Hall, OSU). [Link](https://arxiv.org/abs/2609.14859)
- **Why:** Ist ein bestandener Eval ein Beweis für Können, und zahlt das Produkt unter realen Handelsbeschränkungen überhaupt aus?
- **Was sie sagen:**
  - Formales Modell der zweistufigen Struktur Eval plus Funded: der **EOD-Trailing-Drawdown belohnt in der Eval schnelle, klumpige Trades, die Funded-Stufe bestraft genau das** (Faktor 9 im kombinierten Gate).
  - **Reines Sizing ohne Edge erreicht rund 40 % Passquote**, gemessene Kohorten-Passquote 16,8 % (entspricht der Topstep-Zahl 2025 im [[Research-Cache]]). Bestehen ist daher kein eigenständiger Skill-Beweis.
  - Unter gemessenen Handelsbeschränkungen zahlt das Produkt nicht.
- **Für Max:** stützt die Zieländerung vom 18.09. (Zeit bis Payout-Kapital statt Passquote) und #106. Die Spannung Eval-Stil gegen Funded-Stil ist eine eigene Rechnung wert (der Split „große Eval, kleiner Master“ war beim Bulenox-Check noch ungerechnet).

### A6. Ng: Pass-First-Pay-Later (Deferred-Fee-Modell)
- **Wo:** SSRN 6672818, seit 06.07.2026 im Vault, **in dieser Session nicht neu gelesen**. [Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6672818)
- **Why:** Wie verändert ein Modell, bei dem die Restgebühr erst nach dem Bestehen fällig wird, die Ökonomie fehlgeschlagener Versuche?
- **Was es sagt (Stand Vault):** senkt die Kosten fehlgeschlagener Versuche massiv und verändert den Erwartungswert komplett, 2026 fast Branchenstandard.
- **Für Max:** Kostenmodell im Eval-Optimizer ([[Prop-Eval-Passing (Fokus)]]).

### A7. Weitere Treffer mit Prop-Bezug am Rand
| Paper | Why | Was es sagt | Für Max |
|---|---|---|---|
| Arias (2026): Audit-Grade Pre-Validation of Trading Strategies: Five Contributions to the López de Prado Stack, [SSRN 7308022](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7308022) | Validierungsmethodik, ausdrücklich motiviert mit den Prop-Passquoten (86 % scheitern, 7 % Payout) als Beleg für strukturelles Overfitting | 5 Erweiterungen zum López-de-Prado-Stack, 3 Lehrbuch-Strategien getestet (Golden Cross CL, RSI-14 BTC-Perp, Asian-Range-Breakout EURUSD), keine erreicht die Stufe „Robust“ | Methodik-Vergleich mit unserem Gate v2/v3, kein Prop-Paper im engeren Sinn |
| Maile (2026): Proprietary Trading Firms: A Strategic Economic Lever for Lesotho, [SSRN 6785399](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6785399) (Policy-Paper, graue Literatur) | Kann die Prop-Firm-Branche der Jugend in Lesotho helfen (Arbeitslosigkeit rund 38,9 %, Armutsquote rund 49,7 %)? | argumentiert für die Branche als niedrigschwellige Devisenquelle, keine eigene Empirie | nichts |
| Autor unklar (Okt. 2025): The Evolution of Prop Firms: How Innovation in Trader Evaluation is Redefining the Sector, [ResearchGate 396851394](https://www.researchgate.net/publication/396851394_The_Evolution_of_Prop_Firms_How_Innovation_in_Trader_Evaluation_is_Redefining_the_Sector) | Sektor-Überblick zu neuen Evaluationsformen | nur Titel gesehen, vermutlich Branchenüberblick, Journal und Autor ungeprüft | offen |
| Wong, [SSRN 6722841](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6722841) und Huber „MaxAI“, [SSRN 5761402](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5761402) | seit Juli im Vault (MC-Stresstest-Methodik bzw. RL/GA auf Index-Futures) | Prop-Bezug aus den Kurzbeschreibungen nicht erkennbar | als Prop-Paper eher nicht zählen |

---

## B. Klassische Prop-Trading-Firmen und Prop-Trader

Ältere, meist peer-reviewte Forschung mit Daten echter Prop-Firmen, Trading-Teams oder Floor-Trader auf eigene Rechnung.

| Paper | Why | Was es sagt |
|---|---|---|
| **Harris & Schultz (1998):** The Trading Profits of SOES Bandits, JFE 50(1), [SSRN 137949](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=137949) | Wie verdienen „SOES Bandits“ (Day-Trader in prop-artigen Trading-Arcades über Nasdaqs Small Order Execution System) Geld? Daten zweier spezialisierter Broker, rund 20.000 Trades in 3 Wochen | Meist profitabel, aber nicht durch Ausnutzen einzelner veralteter Quotes, sondern weil sie schneller umpreisen als die Mehrheit der Dealer. Erklärt u.a. mit dem Anreiz eigenes Kapital gegen Firmenkapital der Market Maker |
| Imperfect Market Monitoring and SOES Trading, [ResearchGate 4815261](https://www.researchgate.net/publication/4815261_Imperfect_Market_Monitoring_and_SOES_Trading) | laut Titel verwandt mit Harris & Schultz | nur Titel, Autoren und Inhalt ungeprüft |
| **Garvey & Murphy (2002):** How Profitable Day Traders Trade, [Working Paper](https://content.csbs.utah.edu/~ehrbar/erc2002/pdf/P407.pdf) | Wie handeln profitable Day-Trader einer Prop-Firma? | 62 % der Round-Trips richtig (Ø +0,09 $), 28 % falsch (Ø −0,10 $). Rund 30 % der Round-Trips bringen höchstens 50 $, nur 8 % über 150 $ |
| **Garvey & Murphy (2004):** Are Professional Traders Too Slow to Realize Their Losses?, FAJ 60(4), [Link](https://www.tandfonline.com/doi/abs/10.2469/faj.v60.n4.2635) | Gibt es den Dispositionseffekt auch bei Profis mit Firmenkapital? Daten eines US-Prop-Teams | Ja: Gewinner werden deutlich schneller realisiert als Verlierer, das kostet messbar Performance |
| **Garvey & Murphy (2005):** Entry, exit and trading profits: A look at the trading strategies of a proprietary trading team, J. Empirical Finance 12(5), [Link](https://www.sciencedirect.com/science/article/abs/pii/S0927539805000484) | Was unterscheidet die profitablen Trader eines Prop-Teams? | Profitabel wird morgens, an volatilen und volumenstarken Tagen, in großen Nasdaq-Titeln und anonym über Island ECN gehandelt, Quotes vor den meisten Market Makern angepasst. 55 % der Round-Trips nach Kosten profitabel. (Die Snippets nennen 96.323 Trades und 190.350 Round-Trips, das passt nicht sauber zusammen, im Volltext prüfen) |
| **Garvey & Murphy (2005/06):** The Profitability of Active Stock Traders, [SSRN 908615](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=908615) (J. Applied Finance laut Sekundärquellen) | 15 Prop-Day-Trader (Firmenkapital, keine Kommission, Gewinnbeteiligung), 96.000+ Trades, 3 Monate 2000. Vermutlich gleicher Datensatz wie JEF 2005, eventuell eine Fassung derselben Arbeit | Profitablere Trader handeln dort und dann, wo Liquiditäts-Trader aktiv sind: morgens, volatile Tage, große Nasdaq-Titel, anonym über Island ECN |
| **Garvey, Murphy & Wu:** Do Losses Linger? Evidence from Proprietary Stock Traders, [SSRN 1099549](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1099549) | Wirken Verluste auf die Folgeentscheidungen nach? Gleiche Prop-Kohorte | untersucht Verlust-Nachwirkung bei Prop-Day-Tradern, Ergebnis nicht im Treffer, Journal ungeprüft |
| **Coval & Shumway (2005):** Do Behavioral Biases Affect Prices?, J. of Finance 60(1), [Link](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2005.00723.x) | Verändern Verhaltensfehler von Prop-Tradern die Preise? CBOT-Treasury-Futures-Grube | Wer am Vormittag verliert, geht am Nachmittag rund 16 % wahrscheinlicher überdurchschnittlich Risiko ein. Das drückt kurzfristig die Preise, die binnen 10 Minuten zurückkommen |
| **Locke & Mann (2005):** Professional trader discipline and trade disposition, JFE 76, [Link](https://doi.org/10.1016/j.jfineco.2004.11.002) | Hilft Disziplin beim Realisieren von Verlusten? CME-Floor-Trader auf eigene Rechnung | Die erfolgreichsten Trader schließen Verlierer am schnellsten, Disziplin sagt Erfolg voraus (Basis unseres Lab-Disziplin-Checks). Link ungeprüft, die Treffer nannten vier verschiedene |
| **Locke & Mann (2015):** Learning by Aspiring Professional Traders: Learning to Take Risk, J. Behavioral and Experimental Finance 8, [Link](https://ideas.repec.org/a/eee/beexfi/v8y2015icp54-63.html) | Lernen neue Profi-Trader wirklich? Tausende neue Futures-Floor-Trader über 6 Jahre | **Nur rund 15 % überleben länger als 1 Jahr.** Überlebende werden risikofreudiger, aber die risikoadjustierte Performance steigt nicht: gelernt wird Risikotoleranz, nicht Skill |
| **Boyd & Kurov (2012):** Trader Survival: Evidence from the Energy Futures Markets, J. Futures Markets 32(9), [Link](https://onlinelibrary.wiley.com/doi/abs/10.1002/fut.20543) | Wer überlebt den Wechsel vom Floor zum elektronischen Handel? NYMEX-Energie-Futures | Gewinn, Erfahrung, Sophistication und Dual-Trading erhöhen das Überleben, Multi-Markt- und Hybrid-Trader sind im Vorteil |
| **Coates & Herbert (2008):** Endogenous steroids and financial risk taking on a London trading floor, PNAS 105(16), [Link](https://www.pnas.org/doi/10.1073/pnas.0704025105) | Steuern Hormone Risiko und Ergebnis? Speichelproben von Tradern eines Londoner Trading-Floors im Live-Betrieb | Morgen-Testosteron sagt den Tagesgewinn voraus, Cortisol steigt mit der Varianz der Ergebnisse und der Marktvolatilität |
| **Coates, Gurnell & Rustichini (2009):** Second-to-fourth digit ratio predicts success among high-frequency financial traders, PNAS 106(2), [Link](https://www.pnas.org/doi/10.1073/pnas.0810907106) | Gleiche Kohorte: sagt ein biologischer Marker (Fingerlängen-Verhältnis 2D:4D) Erfolg voraus? | 2D:4D sagt Langfrist-Profitabilität und Verbleib im Beruf über 20 Monate voraus |
| **Lo, Repin & Steenbarger (2005):** Fear and Greed in Financial Markets: A Clinical Study of Day-Traders, AER P&P 95(2), [NBER w11243](https://www.nber.org/system/files/working_papers/w11243/w11243.pdf) | 80 Day-Trader, 5 Wochen tägliche Emotions-Selbstauskunft plus Persönlichkeitstests | Stärkere emotionale Reaktion auf Gewinne und Verluste geht mit schlechterer Performance einher. Grenzfall: Kapitalquelle der Teilnehmer im Treffer nicht genannt |
| **Fenton-O'Creevy, Nicholson, Soane & Willman (2003):** Trading on Illusions, J. Occupational and Organizational Psychology 76(1), [LSE](https://eprints.lse.ac.uk/14954/) | 3-Jahres-Projekt mit gut 100 Tradern und Managern in 4 Investmentbanken (Bank-Trader, streng genommen eher C) | Kontrollillusion (am Computer gemessen) hängt signifikant negativ mit Performance und Vergütung zusammen |
| **Haigh & List (2005, laut Literatur, Autoren hier nicht gegengeprüft):** Do Professional Traders Exhibit Myopic Loss Aversion? An Experimental Analysis, [ResearchGate](https://www.researchgate.net/publication/4769445_Do_Professional_Traders_Exhibit_Myopic_Loss_Aversion_An_Experimental_Analysis) | Experiment mit CBOT-Profis gegen Studenten zur kurzsichtigen Verlustaversion (Feedback-Häufigkeit) | Befund aus Literaturkenntnis, nicht aus der Quelle gelesen: Profis zeigen den Effekt eher stärker als Studenten |
| **Saavedra, Malmgren, Switanek & Uzzi (2012):** Foraging under conditions of short-term exploitative competition: The case of stock traders, [arXiv 1205.3124](https://arxiv.org/abs/1205.3124) | Rund 30 Day-Trader einer kleinen bis mittleren Trading-Firma, 300.000+ Trades 2007/08, sekundengenau | Wendet Foraging-Theorie (ausbeuten gegen weiterziehen) auf Handelsentscheidungen an. Unklar, ob echtes Firmenkapital |
| Mesas proprietárias de traders: um relato de experiência, [UNIJUI](https://bibliodigital.unijui.edu.br/items/1c7d6f66-ebbf-4b9e-8b72-621418c5ac1e) | Einziger Hochschultext zu brasilianischen Prop-Desks | Erfahrungsbericht, vermutlich studentische Arbeit, Inhalt nicht geprüft |

**Was B für Max heißt:** keine direkte Edge, aber drei Bestätigungen. (1) Menschliche Prop-Trader verlieren nachweislich durch Disposition und Risiko nach Verlusten (Garvey & Murphy 2004, Locke & Mann 2005, Coval & Shumway), beides fällt bei einem Algo weg. (2) Überleben ist selten (15 %), Erfahrung erhöht Risiko, nicht Können: unser Prinzip „Größe kauft Bust“. (3) Coval & Shumway zeigen einen echten Preiseffekt (Rückkehr binnen 10 Minuten), aber aus einer Treasury-Futures-Grube (Floor-Handel), nicht für NQ/ES heute belegt.

### B2. Grenzfälle: Day-Trader mit eigenem Kapital (kein Prop-Kapital)
Oft zusammen mit Prop-Themen zitiert, aber **keine Prop-Firmen**:
- **Jordan & Diltz (2003):** The Profitability of Day Traders, FAJ 59(6), [Link](https://rpc.cfainstitute.org/research/financial-analysts-journal/2003/the-profitability-of-day-traders). 324 Day-Trader einer US-Brokerfirma (vermutlich Kunden mit eigenem Kapital), Feb. 1998 bis Okt. 1999: etwa doppelt so viele Verlierer wie Gewinner, nur rund 20 % mehr als marginal profitabel, Gewinn hängt an der Nasdaq-Bewegung.
- **Barber, Lee, Liu & Odean (2011, später RFS):** Do Day Traders Rationally Learn About Their Ability? [PDF](https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trading%20and%20Learning%20110217.pdf). Taiwan. Unprofitable hören eher auf, aber die Gesamtperformance der Day-Trader ist jedes Jahr negativ, viele unprofitable Veteranen bleiben.
- **Chague, De-Losso & Giovannetti (2019/20):** Day Trading for a Living? [SSRN 3423101](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101). Alle 19.646 Personen, die 2013 bis 2015 im Mini-Ibovespa-Future mit Day-Trading anfingen: **97 % derer, die über 300 Tage durchhalten, verlieren Geld.**
- **É possível viver de day-trade em ações?** Revista Brasileira de Finanças (FGV), [Link](https://periodicos.fgv.br/rbfin/article/download/81949/78263/176074), Autoren ungeprüft (vermutlich gleiche Gruppe). CVM-Daten aller B3-Day-Trader 2012 bis 2018, nur 7 % nach einem Jahr noch aktiv.
- **Porcher (2019):** DAY TRADE: do outro lado das estatísticas, [arXiv 1912.04274](https://arxiv.org/abs/1912.04274). Gegendarstellung: die Evidenz belege weder, dass Day-Trading als Beruf nicht tragfähig ist, noch dass sich Performance nicht verbessern kann.

---

## C. Angrenzend: Principal Trading Firms (HFT) und Bank-Eigenhandel

Institutionelle Prop-Firmen als Untersuchungsobjekt. Diese Literatur ist riesig, hier nur, was der Sweep mit ausdrücklichem Prop-Bezug fand. **Für Max' Ziel wenig direkt nutzbar.**

| Paper | Worum es geht / Kernaussage |
|---|---|
| **Clark & Ranjan (2012):** How Do Proprietary Trading Firms Control the Risks of High Speed Trading? Chicago Fed PDP 2012-1, [Link](https://www.chicagofed.org/publications/policy-discussion-papers/2012/pdp-1) | Interviews mit 9 Prop-Trading-Firmen in 3 Städten zu Risikokontrollen vor und nach dem Trade, Grundlage für Regulierungsempfehlungen. Am nächsten an „Prop-Firma als Objekt“ |
| **Menkveld (2013):** High Frequency Trading and the New-Market Makers, J. Financial Markets 16(4), [SSRN 1722924](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1722924) | Eine große HFT-Firma beim Chi-X-Markteintritt: verdient am Spread, nicht an Richtungswetten, Sharpe stark abhängig von Kapitalkosten |
| **Baron, Brogaard, Hagströmer & Kirilenko (2019):** Risk and Return in High-Frequency Trading, JFQA 54(3), [SSRN 2433118](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2433118) | Latenz erklärt die Performance-Unterschiede zwischen HFT-Firmen, neue Firmen underperformen und scheiden aus |
| **Boehmer, Li & Saar (2018):** The Competitive Landscape of High-Frequency Trading Firms, RFS 31(6), [Link](https://academic.oup.com/rfs/article-abstract/31/6/2227/4782505) | Per PCA drei Strategie-„Produkte“ (Market Making, Cross-Market-Arbitrage, Richtung), Wettbewerb je Kategorie wirkt auf die Kurzfrist-Volatilität |
| **Baldauf & Mollner (2020):** High-Frequency Trading and Market Performance, J. of Finance, [Link](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12882) | Mehr Geschwindigkeit senkt die Informationsproduktion und verbessert die Liquidität, Vorschlag: Order-Delays oder Batch-Auktionen |
| **Kirilenko, Kyle, Samadi & Tuzun (2017):** The Flash Crash: High-Frequency Trading in an Electronic Market, J. of Finance 72(3), [Link](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12498) | CFTC-Daten E-mini: HFT-Firmen haben den Flash Crash 2010 nicht ausgelöst, aber verschärft |
| **Bergman, Kadan, Michaely & Moulton (2020):** Do Proprietary Traders Provide Liquidity? [SSRN 3724327](https://doi.org/10.2139/ssrn.3724327) | NYSE-Prop-Trader sind Netto-Liquiditätsgeber und kontrarisch, weniger bei angespannten Bilanzen |
| Risk-averse dealers in a risk-free market: The role of trading desk risk limits (JFE laut PII, 2026), [Link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X26000619) | Bindende VaR-Limits bei Bank-Desks erzeugen Verhalten wie Risikoaversion (Inventar runter, mehr Aufschlag nahe am Limit). Strukturell verwandt mit Daily-Loss-Limits, aber keine Prop-Firm-Daten |
| ECB WP 1602 (2013): High Frequency Trading, [PDF](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1602.pdf) | NASDAQ-Datensatz mit HFT-Kennzeichnung, Autoren ungeprüft |
| Data-Driven Measures of High-Frequency Trading (2024), [arXiv 2405.08101](https://arxiv.org/pdf/2405.08101) | Offener HFT-Datensatz US-Aktien 2010 bis 2023 |
| Joint Staff Report (2015): The U.S. Treasury Market on October 15, 2014, [PDF](https://home.treasury.gov/system/files/276/joint-staff-report-the-us-treasury-market-on-10-15-2014.pdf) | Behördenbericht: Principal Trading Firms als dominante Liquiditätsquelle und -abzieher im Flash Rally |
| Fed FEDS Notes (2020): Principal Trading Firm Activity in Treasury Cash Markets, [Link](https://www.federalreserve.gov/econres/notes/feds-notes/principal-trading-firm-activity-in-treasury-cash-markets-20200804.html) | PTF-Aktivität auf Interdealer-Plattformen aus neuen Meldedaten |
| FEDS WP 2020-096: Price Discovery in the U.S. Treasury Cash Market: On Principal Trading Firms and Dealers, [PDF](https://www.federalreserve.gov/econres/feds/files/2020096pap.pdf) | Beitrag von PTFs gegen Dealer zur Preisfindung, Autoren ungeprüft |
| Harkrader & Weitz: How Do Principal Trading Firms and Dealers Trade Around FOMC Statement Releases? [SSRN 3879329](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3879329) | nur Titel gesehen |
| **Bao, O'Hara & Zhou (2018):** The Volcker Rule and Corporate Bond Market Making in Times of Stress, JFE 130(1), [Link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301491) (Vorfassung FEDS 2016-102) | Nach dem Eigenhandelsverbot steigt die Bond-Illiquidität unter Stress, weil die betroffenen Händler vorher die Stress-Liquidität stellten |
| **Trebbi & Xiao:** Regulation and Market Liquidity, [NBER w21739](https://www.nber.org/system/files/working_papers/w21739/w21739.pdf) | Gegenbefund: kein struktureller Bruch der Fixed-Income-Liquidität nach Dodd-Frank, Basel III und Volcker |
| OFR WP 19-02 (2019): The Effects of the Volcker Rule on Corporate Bond Trading: Evidence from the Underwriting Exemption, [PDF](https://www.financialresearch.gov/working-papers/files/OFRwp-19-02_the-effects-of-the-volcker-rule-on-corporate-bond-trading.pdf) | Liquidität der regulierten Händler wurde teurer, ihr Marktanteil sank |
| Whitehead (2011): The Volcker Rule and Evolving Financial Markets, Harvard Business Law Review, [PDF](https://journals.law.harvard.edu/hblr//wp-content/uploads/sites/87/2014/09/Volcker-Rule.pdf) | Rechtswissenschaftliche Analyse des Eigenhandelsverbots |
| FSOC (2011): Study & Recommendations on Prohibitions on Proprietary Trading, [PDF](https://home.treasury.gov/system/files/261/The%20FSOC%E2%80%99s%20Study%20and%20Recommendations%20Regarding%20Implementation%20of%20the%20Volcker%20Rule%20-%20January%2018,%202011_0.pdf) | Die Grundlagenstudie zur Umsetzung der Volcker Rule (Primärquelle) |
| Adedipe: The Impact of the Volcker Rule on Systematically Important Financial Institutions: An Event Study, [UMBC WP](https://economics.umbc.edu/wp-content/uploads/sites/243/2014/09/TundeAdedipeFinalPaperTheImpactOfTheVolckerRuleonSystematicallyImportantFinancialInstitutionsAnEventStudy.pdf) | Aktienreaktion systemrelevanter Banken auf Volcker-Ereignisse |
| Li (2019): Examining the Influence of the Volcker Rule ..., [NYU Shanghai Honors Thesis](https://shanghai.nyu.edu/sites/default/files/chenghao_li_thesis_nyush_honors_2019.pdf) | Studentische Arbeit zur Wirkung auf betroffene Banken |
| Regulation of bank proprietary trading post 2007-09 crisis: An examination of the Basel framework and Volcker rule, [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0261560621001418) | Vergleich Basel gegen Volcker, Autoren und Journal ungeprüft |
| Bank Proprietary Trading and Investment in Private Funds: Is the Volcker Rule a Panacea or Yet Another Maginot Line? [ResearchGate](https://www.researchgate.net/publication/308750567_Bank_Proprietary_Trading_and_Investment_in_Private_Funds_Is_the_Volcker_Rule_a_Panacea_or_Yet_Another_Maginot_Line) | Bewertet, ob die Volcker Rule das Problem trifft, Autoren ungeprüft |

---

## D. Branchen- und Aufsichtsberichte (keine Paper, aber echte Daten)

| Bericht | Was drinsteht |
|---|---|
| **D1. FPFX Tech, berichtet von Finance Magnates (Sept. 2024):** [Only 7% of 300,000 Prop Trading Accounts Achieved Payouts](https://www.financemagnates.com/forex/analysis/exclusive-only-7-of-300000-prop-trading-accounts-achieved-payouts/) | 300.000+ Konten, 100.000 Trader, 10 Firmen: **14 % bestehen, davon rund 45 % mit Payout = rund 7 % aller Konten** (14 % × 45 % ergibt 6,3 %, Rundung oder Bezugsbasis im Bericht unklar), im Schnitt 800 $ Gebühren über 3 Versuche, Ø Payout 4 % der Kontogröße. Das ist sehr wahrscheinlich die Quelle der bisher unverifizierten Zahl im [[Research-Cache]]. FPFX Tech ist ein Software-Anbieter für Prop-Firmen, kein Forscher. Ein Agent fand den Artikel nicht, drei unabhängig schon |
| SEC OCIE (2000): [Report of Examinations of Day-Trading Broker-Dealers](https://www.sec.gov/news/studies/daytrading.htm) | Prüfung von 47 Day-Trading-Firmen (Okt. 1998 bis Sept. 1999): kein flächendeckender Betrug, aber Mängel bei Eigenkapital, Margin, Werbung, Aufsicht |
| NASAA (1999): [Report of the Day Trading Project Group](https://www.nasaa.org/wp-content/uploads/2011/08/NASAA_Day_Trading_Report.pdf) | Bericht über US-Day-Trading-Firmen um 1999, Vorlauf der späteren Pattern-Day-Trader-Regeln |
| CVM (Brasilien): [Caderno CVM 15: Day Trade](https://www.gov.br/investidor/pt-br/educacional/publicacoes-educacionais/cadernos/caderno-cvm-15-day_trade.pdf/@@display-file/file) | Aufsichtsheft auf Basis aller B3-Day-Trader 2012 bis 2018, unter 1 % mit signifikantem Gewinn |
| Fin+ / UFSM (2025), nur als [Blogzitat](https://www.finmore.com.br/post/artigo-wiw2025-o-framework-regulat%C3%B3rio-global-e-brasileiro-das-mesas-propriet%C3%A1rias-prop-trading) | Behauptung: nur 7 % der Teilnehmer brasilianischer Mesas Proprietárias bekommen je einen Payout. Primärquelle nicht gefunden, nicht mit D1 verwechseln |
| SEC (2014): [Equity Market Structure Literature Review Part II: HFT](https://www.sec.gov/marketstructure/research/hft_lit_review_march_2014.pdf) | Literaturübersicht, nützlich als Quellenverzeichnis zu C |
| Topstep-Transparenzzahlen 2025 (schon im [[Research-Cache]]) | 16,8 % Pass je Versuch, 33,3 % der Funded mit Payout. Gleiche Zahl wie Halls gemessene Kohorte (A5), vermutlich Topstep, im Volltext prüfen |

---

## E. Angrenzend: Glücksspiel und Gamification

| Paper | Was es sagt |
|---|---|
| Rabinovitz & Packin (2025): All Bets Are On: Addiction, Prediction, Regulation, and the Future of Financial Gambling, Fordham IPLJ 36(1), [Link](https://ir.lawnet.fordham.edu/iplj/vol36/iss1/2/) | Law Review zur „Gamblification“ von Prediction Markets, Grenze Finanzprodukt gegen Glücksspiel. Prop Firms nicht ausdrücklich |
| Loscalzo, Rogier & Velotti (2025): Problematic trading: a Systematic Review of theoretical considerations, Frontiers in Psychiatry, [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12070191/) | Review über 23 Arbeiten zu „problematischem Trading“ als Sucht-Analogie, Day-Trading und Krypto allgemein |
| Trading Gamification and Investor Behavior (2026), Management Science 72(1), [IDEAS](https://ideas.repec.org/a/inm/ormnsc/v72y2026i1p32-56.html) | Randomisiertes Online-Experiment zu Gamification-Effekten auf Trader-Verhalten. Vermutlich übertragbar auf die Challenge-/Leaderboard-Mechanik, Prop Firms sind nicht das Objekt. Autoren ungeprüft |

---

## 🚫 Was es (Stand heute) nicht gibt

- **Keine Studie mit Trader- oder Konto-Daten einer modernen Funded-Firma** (FTMO, Topstep, E8, FundedNext, Apex, MFFU, The5ers, Earn2Trade). Nur öffentliche Firmenzahlen und D1.
- **Keine akademische Arbeit zu Consistency-Rule oder Profit-Split als Mechanism Design**, nur Branchenblogs.
- **Keine Law Review zum CFTC-Fall My Forex Funds** (nur Kanzlei-Blogs), keine Aufsichtsstudie (FCA, ESMA, ASIC, BaFin, CySEC, CFTC, NFA) speziell zu Funded-Prop-Firmen, kein Paper zur Frage „ist eine Challenge Glücksspiel?“, keine akademische Arbeit zur Besteuerung von Prop-Payouts.
- **Keine Forschung zur Trader-Psychologie innerhalb moderner Funded-Firmen.**
- **Keine echte Forschung zu brasilianischen Mesas Proprietárias** (nur Erfahrungsbericht und Blogzitat).
- **Keine Fallstudien mit internen Daten von Jane Street, Citadel Securities oder DRW.**
- ⚠️ **Einschränkung:** die Suchwinkel „graue Literatur / nicht-englisch“ (Abschlussarbeiten, Tschechien als FTMO-Heimat, Polen, Spanien, Brasilien ...) und „Datenbank-APIs“ (OpenAlex, Semantic Scholar, Crossref, arXiv) liefen wegen der Sperren leer. Für diese Winkel ist „gibt es nicht“ **nicht** belegt, nur nicht gesucht.

---

## ▶️ Offen / nächster Schritt

1. **Deep-Read im Volltext** der Kern-Paper A1 bis A5 (plus A6), sobald das Netzwerk frei ist. Priorität: **A4 Tomàs Fernández** (Formel als Gegencheck zu `evaluate_v2`) und **A3 Lim** (sind E8/FN unter den 31 Verträgen, mit welchem Wert?). Danach Skeptiker-Gegenprüfung je Paper.
2. **Logbuch-Negativbefund** „kein Paper zu Prop-Firm-First-Passage-Sizing“ nachtragen (nur mit `logbook-distiller`, auf Ansage).
3. **Die zwei leer gelaufenen Suchwinkel nachholen** (graue Literatur/nicht-englisch, Datenbank-APIs) plus Zitations-Schneeball über die Kern-Paper.
4. **Quant-Team (Anschlussauftrag):** L/(T+L)-Nulllinie und Tomàs-Fernández-Formel gegen unseren Nulldrift-Zwilling in `tempo_plan.py` legen.

Voraussetzung für 1 und 3: in den Einstellungen der Cloud-Umgebung Network Access erweitern oder diese Hosts erlauben: `papers.ssrn.com`, `arxiv.org`, `export.arxiv.org`, `api.openalex.org`, `api.semanticscholar.org`, `api.crossref.org`, `ideas.repec.org`, `www.federalreserve.gov`, dann frische Session (neues Such-Kontingent).

---

## 🎯 Auftrag für die Volltext-Session (freigegeben von Max, 28.09.2026)

**Startsatz für die neue Session:** „Lies `Ressourcen/Paper-Analysen/Prop-Firm-Paper (Literaturüberblick).md`, Abschnitt ‚Auftrag für die Volltext-Session‘, und führ ihn aus.“ Vorher Network Access erweitern (Hosts siehe oben), sonst hängt sie am selben Proxy.

**Typ und Kette:** `research` → `research-scout` (bei vielen Papern als Workflow, je Paper ein Leser plus ein Skeptiker, der gegen die Originalquelle prüft). Wer eine eigene Rechnung anstößt, wechselt auf `rechnen` (Quant-Team).

**Linse von Max:** nicht nur zusammenfassen, sondern **gezielt suchen, was unsere Sicht dahinter angreift oder uns einen Vorteil bringt.** Je Paper zwei Fragen:
1. **Angriff:** Welche unserer Annahmen unten widerlegt, schwächt oder relativiert das Paper? Mit Seite/Tabelle und Zahl.
2. **Vorteil:** Was können wir konkret nutzen (Firma/Vertrag wählen, Größe, Reset, Payout-Timing, Rabatt, Regel-Lücke), und um wie viel verkürzt es die Zeit bis 50.000 $?

**Unsere Annahmen, gegen die gelesen wird** (Stand CLAUDE.md, 28.09.2026):

| # | Unsere Sicht | Welches Paper könnte sie angreifen |
|---|---|---|
| S1 | Zielfunktion ist E[Zeit bis 50.000 $ aus Payouts] bei begrenzter Auslage (Deckel 2.500 $ netto), nicht die Passquote | A2, A3, A5 (bewerten sie anders, z.B. EV je Vertrag?) |
| S2 | „Größe kauft Bust, nicht Tempo“ (#106), Start mit k2, k4 bringt im Kalender-Modus nichts (#175) | A1 (L/(T+L) nur statisch), A2 (Sizing-Grat bei 2 % Tagesvola), A5 (Sizing allein 40 % Pass). Dazu klassische Theorie mit Frist: Browne (1995/1999, Ziel bis Deadline erreichen), Grossman & Zhou (1993, Drawdown-Grenze) |
| S3 | Jede Politik wird gegen den Nulldrift-Zwilling gerechnet, unter Edge 0 muss Erreichung 0 % sein | A1 bis A5 (deren Zero-Edge-Zahlen als externer Eichpunkt) |
| S4 | Gleiches Buch, gleiche Größe in Eval und Funded (der Split „große Eval, kleiner Master“ ist ungerechnet) | A5 (Eval belohnt anderen Stil als Funded, Faktor 9) |
| S5 | Kaufpolitik P10, Start 1× E8 150k am 02.10., FN 150k nach AP205, FN-Größe offen (AP248) | A3 (31 Verträge: sind E8/FN dabei, welcher EV?), A4 (Streuung 62 % bei gleicher Größe) |
| S6 | E8-Mechanik: EOD-Floor, aber Intraday-Check (AP51, #077) | A4 (Parameter Breach-Check-Frequenz, stimmt unsere Abbildung?) |
| S7 | Regeln (Deckel, Gewinnstopp, Konsistenz) verschieben Monate, nicht Jahre, Gewinnstopp am 21.09. beerdigt | A2, A4, A5 (Wert von Regeln und Stopp-Politik im Vertrag) |
| S8 | Haupthebel ist der Buch-Sharpe: Monate bis 50k ≈ 1 / (0,0147 · (SR − 0,35)) | A1, A2 (ab welcher Drift kippt der EV, wie steil?) |
| S9 | Konten werden in `tempo_plan.py` unabhängig gerechnet (bis Faktor 2 zu optimistisch, AP245 Kalender-Modus) | A2, A3 (wie modellieren sie mehrere Konten und Resets?) |
| S10 | Firmenwahl E8 + FN, Bulenox raus (VPS-Verbot), dritte Firma mit Box-Erlaubnis offen | A3 (Rangliste der 31 Verträge) |

**Zusätzlich neu suchen** (über die Liste oben hinaus): Paper, die S2 oder S4 direkt widersprechen (optimale Größe mit Frist, Reset als Optimal-Stopping-Problem, Größen-Split zwischen Eval und Funded), Paper zu Payout-Politik (wie viel abheben, wie viel Puffer stehen lassen) und alle Zitierer von A1 bis A5. Außerdem die zwei leer gelaufenen Suchwinkel nachholen (Abschlussarbeiten/nicht-englisch, Datenbank-Abfragen).

**Ausgabe:** diese Notiz ergänzen (je Paper „Angriff“ und „Vorteil“, Beleg-Stufe auf Volltext hochsetzen), neue Claims in den [[Research-Cache]], am Ende eine Tabelle „Annahme S1 bis S10: hält / wackelt / fällt, Beleg“. Was eine eigene Rechnung braucht, wird als Ticket vorgeschlagen (vorher `--pull`), nicht still gerechnet.
