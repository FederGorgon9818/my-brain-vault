---
tags:
  - ressource/theorie
  - trading/momentum
  - trading/trend-following
erstellt: 2026-08-21
quelle: Research-Cache Abschnitt "Momentum im Futures-Markt" (21.08.2026)
---
# 📈 Momentum-Theorie (Futures): TSM, Breakout und die anderen Richtungen

⬅️ [[Alpha-Suche]] · [[Strategie-Familien]] · [[Idee-Generierung (wie Institutionen)]] · Abgeleitete Hypothesen: [[Hypothesen-Bank (Momentum & Averages)]] · Belege: [[Research-Cache]] (Abschnitt „Momentum im Futures-Markt", 21.08.2026)

> [!important] Worum es geht
> Max' Momentum-Runde (21.08.2026), Teil 1 von 3: **reine Theorie** zu Time-Series-Momentum und Breakout-Momentum im Futures-Markt, und zwar nicht nur „Breakout über den Ort" (Preislevel), sondern alle Richtungen, in denen Momentum gemessen wird. Teil 2 (Cross-Sectional Momentum) und Teil 3 („Way of Dumb", Zwangsflows großer Institutionen) liegen als **Backlog-Karten in der Idee-Engine** (`ideas.json`, Lab-Tab Ideen) für später.

---

## 1. Time-Series-Momentum (TSM): was die Literatur wirklich sagt

**Der Kernbefund:** Moskowitz/Ooi/Pedersen (2012, 58 Futures 1965 bis 2009): das Vorzeichen des 12-Monats-Returns sagt den Return des Folgemonats voraus. Der Effekt hält 1 bis 12 Monate, kehrt über 12 bis 36 Monate teilweise um und liefert in Krisen die beste Performance. Hurst/Ooi/Pedersen (2017) ziehen das bis 1880 zurück, positiv in jeder Dekade.

**Die drei Gegenbefunde, die man kennen muss (sie relativieren den Kern stark):**

| Einwand | Quelle | Was es für uns heißt |
|---|---|---|
| Gepoolte t-Statistik ist nicht bootstrap-signifikant; asset für asset ist kaum TSM da | Huang/Li/Wang/Zhou, JFE 2020 | Der Effekt lebt vom Pooling über 50+ Märkte. Auf 4 Index-Futures ist die Beweislage dünn. |
| TSM ist großteils verkapptes Netto-Long-Beta; leverage-adjustiert schlägt Cross-Sectional-Momentum TSM | Goyal/Jegadeesh, RFS 2018 | Ein Long-Bias im Momentum-Bein kann die ganze „Edge" sein. Immer gegen Buy-and-Hold mit gleicher Exposure rechnen. |
| Ohne Vol-Scaling ist TSM ungefähr Buy-and-Hold; der Effekt IST das Sizing | Kim/Tse/Wald 2016 | Vol-Targeting ist kein Bonus obendrauf, sondern oft der ganze Trick. Signal und Sizing getrennt bewerten. |

**Kehrseite:** Momentum-Crashes (Daniel/Moskowitz 2016) entstehen in „Panik-Zuständen" (nach Rückgang plus hoher Vola), sind teilweise vorhersagbar und haben Optionscharakter auf der Verliererseite. Das ist der theoretische Grund für die bereits validierte Idee „Mom-lowVIX" (Momentum nur bei niedrigem VIX).

**Horizonte:** 1-Monats-Reversal (kurz), 1 bis 12 Monate Momentum, 3 bis 5 Jahre Long-Term-Reversal. Alles Monatsebene. **Für Stunden-Horizonte gilt diese Theorie nicht direkt**, siehe Abschnitt 4.

## 2. Signal-Definitionen: Breakout, MA-Crossover, Sign-of-Return sind derselbe Filter

Levine/Pedersen („Which Trend Is Your Friend?", FAJ 2016): Sign-of-Return-TSM und MA-Crossover sind in der allgemeinsten Form **ein und derselbe lineare Filter** über vergangene Returns, nur mit anderer Gewichtungsfunktion. HP-Filter und Kalman-Filter sind Spezialfälle davon. Donchian-/Channel-Breakout ist eine nichtlineare Variante desselben Prinzips (Schwelle statt Gewichtung).

**Konsequenz für die Engine:** Die Wahl „Breakout vs. MA-Crossover vs. Sign-of-Return" ist keine Wahl zwischen Mechanismen, sondern zwischen Gewichtungen. Wer drei Varianten davon testet, testet dreimal fast dasselbe (Multiple Testing ohne neue Information). Was echte Diversifikation bringt, ist die **Geschwindigkeit**: Baz et al. (Man AHL 2015, „Dissecting Investment Strategies") zerlegen in Fast/Medium/Slow-EWMAC und kombinieren die Geschwindigkeiten. Das ist der Industriestandard, und davon gibt es im Vault bisher nur einzelne Lookbacks.

## 3. Die anderen Momentum-Richtungen im Futures-Markt

| Richtung | Kernquelle | Befund | Für Max' Intraday-Welt |
|---|---|---|---|
| **Volatilitäts-Momentum / Range-Expansion** | Crabel (NR7/Stretch) | Kompression vor Expansion, klassisches Profil: viele kleine Stops, wenige große Gewinner | Getestet: `volbrk` Bank-Fund NQ ([[Strategie-Logbuch]] #057), Tail-Lotterie (#038) |
| **Volumen / Hedging-Demand** | Baltussen/Da/Lammers/Martens, JFE 2021; Gao/Han/Li/Zhou 2018 | Intraday-Momentum (erste 30 Min sagen letzte 30 Min voraus) über 60+ Futures 1974 bis 2020, Mechanismus: Gamma-Hedging der Dealer | Basis des `NQ_LastHour`-Beins. Die direkte first30→last30-Variante ist in modernen Daten tot (#057, 0/48) |
| **Carry / Term-Structure / Basis-Momentum** | Koijen et al., JFE 2018; Boons/Prado, JoF 2019 | Roll-Yield und Basis-Änderung sagen Returns voraus, akademisch solide | Für ES/NQ nur Kontext: Roll-Yield klein, quartalsweise. Kein Intraday-Signal |
| **Cross-Asset / Lead-Lag** | Pitkäjärvi/Suominen/Vaittinen 2019/2020 | Bond-Returns sagen Equity-Returns positiv voraus, +45 % Sharpe gegenüber Standard-TSM | Nur Monats-/Länderindex-Ebene getestet. Im Vault: VIX-Spike-Reversion validiert (#087), ZN/DXY sind Datenlücke |
| **Acceleration (Momentum-of-Momentum)** | Ardila/Forró/Sornette | Δ des Returns schlägt reines Momentum in 2/3 der Parametrisierungen | Nicht getestet. Kandidat 2 unten |
| **Residual / idiosynkratisch** | Blitz/Huij/Martens 2011 | Momentum auf Regressions-Residuen rund 2x profitabler als auf Rohrenditen, theoretisch aber schlecht verstanden | Nicht getestet. NQ minus ES als Signal, Kandidat 3 |
| **Overnight vs. Intraday (Tug-of-War)** | Lou/Polk/Skouras, JFE 2019 | Overnight- und Intraday-Segmente setzen sich je Tag-zu-Tag fort, reverten aber gegenläufig zueinander | Anderer Mechanismus als Gao/Han (innerhalb des Tages). Nicht getestet, Kandidat 4 |

## 4. Warum gibt es Momentum (Why), und welches Why gilt für welchen Horizont

- **Behavioral, Monatsebene:** drei konkurrierende Modelle ohne Konsens. Daniel/Hirshleifer/Subrahmanyam 1998 (Overconfidence, Einzel-Agent), Barberis/Shleifer/Vishny 1998 (Konservatismus plus Repräsentativität), Hong/Stein 1999 (heterogene Agenten: Newswatchers vs. Momentum-Trader, explizit **geschwindigkeitsbasiert**, Info diffundiert langsam, dann übertreiben Trendfolger).
- **Risikobasiert:** Momentum als Kompensation für Crash-Risiko (Daniel/Moskowitz), Vol-Scaling als Risikomanagement (Moreira/Muir).
- **Institutionelle Friktionen:** CTA-Flows, Vol-Targeting-Rebalancing, Benchmark-Zwang. Das ist die Brücke zu Teil 3 („Way of Dumb").
- **Intraday (Stunden):** Die Evidenz spricht klar für **Mikrostruktur und institutionelle Hedging-Nachfrage** (Dealer-Gamma, Baltussen; Market-Impact-Loops, Bouchaud), **nicht** für die klassischen Monats-Behavioral-Theorien. Wer intraday „TSM" sagt, meint ökonomisch etwas anderes als Moskowitz/Ooi/Pedersen. Das Why muss intraday also aus der Plumbing kommen (wer muss handeln), nicht aus Anlegerpsychologie.

## 5. Übertragbarkeit und Decay

- **Wichtigster neuer Fund:** Kurth/Eisler/Rej/Bouchaud (arXiv 2607.01550, 2026): schnelle Trendsignale liefern seit etwa 2008/09 keine verlässlichen Renditen mehr, spezifisch auf **Small-Tick-Futures** (ES und NQ sind Small-Tick). Mechanismus ist ein selbstverstärkender Market-Impact-Loop, nicht simples Overcrowding. Deckt sich mit dem eigenen Post-Publikations-Verfall in #057.
- **Fallen:** (1) Look-ahead bei Breakout-Filtern, die die Ausbruchsbar komplett auswerten (Logbuch #066/#067, `orb_exec`). (2) Vol-Scaling als Hebel-Illusion: Scaling erhöht Sharpe, aber unter einem Trailing-DD-Käfig zählt der Pfad, nicht die Sharpe. (3) Transaktionskosten fressen schnelle Signale zuerst. (4) Long-Bias als versteckte Edge (Goyal/Jegadeesh).
- **Lücke:** keine Primärquelle testet die TSM/Vol-Scaling-Zerlegung oder die Fast/Medium/Slow-Zerlegung auf Intraday-Index-Futures. Das kann nur der eigene Backtest schließen.
- Blog-Claim „TSM 10 % → 2 % p.a." ist unverifiziert, nicht als Fakt verwenden.

## 6. Was im Vault schon getestet ist (nicht nochmal)

| Mechanismus | Stand | Logbuch |
|---|---|---|
| Sign-of-Return-Momentum `NQ_Momentum` (sig15) | im Buch, bleibt drin | #106 / #108 / #121 |
| ORB-Breakout am Ort | getötet (kein Follow-Through, Look-ahead) | #065 bis #068 |
| Crabel-Stretch / NR7 (`volbrk`) | Bank-Fund, Tail-Lotterie | #057, #038 |
| Momentum-Selektiv (Kaufman-ER-Filter) | robust, Replace-Frage offen (AP101) | #057, #080, #095, #108 |
| Gao/Han/Li/Zhou first30→last30 als Bein | tot, 0/48 | #057 |
| Pivot-Break (Momentum-Variante) | NO-GO, Multiple-Testing-Rauschen | #051 |
| OpEx-/FOMC-Post-Momentum | bestätigt, Bank (zu wenig Trades) | #049 / #054 |
| Value-Area-/IB-Breakout-Continuation | überwiegend schwach | #112 bis #115 |
| `NQ_LastHour` (Hedging-Demand) | im Buch | 17.08.-Runde |

## 7. Hypothesen-Kandidaten aus der Theorie (noch nicht getestet)

Reihenfolge nach erwartetem Buch-Beitrag. Jede braucht vor dem Job das Why im Idee-Engine-Format und eine Register-Prüfung ([[Discovery-Runner v2]]). Quant-Team vorab bei 1 und 5.

1. **Vol-Targeting-Overlay auf `NQ_Momentum`** (Moreira/Muir, Kim/Tse/Wald): Exposure invers zur kurzfristigen realisierten Vola, als Sizing-Overlay, nicht als neues Bein. Why: #106 nennt die choppige Pfad-Varianz des Momentum-Beins als Buch-Problem, genau das adressiert Vol-Targeting. Achtung: unter Min-Size 1 Kontrakt ist „Exposure runter" gleich „Tag aussetzen", also wird daraus de facto ein Vola-Filter. Sauber gegen das Signal ohne Scaling rechnen.
2. **Acceleration statt Level** (Ardila/Forró/Sornette): Δ des Return-Signals (Fenster 2 minus Fenster 1) als Entry statt Sign-of-Return. Why: Beschleunigung fängt Regimewechsel früher. Achtung: Look-ahead in der Fensterdefinition, Multiple Testing (schon zwei Momentum-Varianten im Buch).
3. **Idiosynkratisches NQ-Momentum** (Blitz/Huij/Martens portiert): NQ-Return minus ES-Return bzw. Residuum NQ~ES als Signal. Why: schließt die im Logbuch notierte Lücke „niemand quantifiziert Korrelation Momentum↔Alternative für Index-Futures". Achtung: Beta-Fenster, Realtime-Berechenbarkeit.
4. **Tug-of-War-Filter** (Lou/Polk/Skouras): `NQ_LastHour` nur, wenn der Overnight-Return klein war (beide Komponenten reverten gegenläufig). Achtung: vorab vom toten OR-Delta-Bias (#079) abgrenzen.
5. **Fast/Medium/Slow-Konsens** (Baz et al.): mehrere EWMAC-Geschwindigkeiten parallel, Konsens als Filter, Divergenz als Veto. Achtung: arXiv 2607.01550 sagt, die schnellen Geschwindigkeiten sind auf Small-Tick-NQ strukturell schwächer, also explizit mit-testen statt blind kombinieren.
6. **Bond→Equity-Gate** (Pitkäjärvi et al.): ZN/ZB-Tagesreturn als Bedingung für Momentum-Entries. Blockiert durch Datenlücke (ZN nicht im QuantPad-Export), bei Datenzugang öffnen.
7. **Basis-Momentum um Quartals-Rolls** (Boons/Prado, stark adaptiert): Momentum-Signale in der Roll-Woche dämpfen/verstärken je nach Steilheit Front/Back. Klein-N (4x/Jahr), nur als Filter sinnvoll.

## 8. Die anderen zwei Richtungen (Tickets, später)

- **Cross-Sectional Momentum** (Rank über das Futures-Universum, Long Winner / Short Loser): Backlog-Karte in der Idee-Engine. Kernproblem: mit 4 Index-Futures ist die Cross-Section schmal, echte Kraft erst mit Bonds/Rohstoffen/FX. Goyal/Jegadeesh sagen, leverage-adjustiert ist das der stärkere Effekt gegenüber TSM.
- **Way of Dumb** (Zwangsflows großer Institutionen: Kalender-Rebalancing, Vol-Targeting-Deleveraging, CTA-Schwellen, LETF-Rebalancing, Dealer-Hedging, MOC, Benchmark-Zwang): Backlog-Karte in der Idee-Engine mit vier konkreten Teil-Hypothesen. Theorie-Unterbau: [[Research-Cache]] Abschnitt „Wie große Marktteilnehmer Positionen in Futures bringen" (21.08.2026) und [[Idee-Generierung (wie Institutionen)]] (Edge-Quelle „Structural").

---
*Belege mit Quelle und Status stehen im [[Research-Cache]]. Diese Notiz ist die verdichtete Lesefassung.*
