---
tags:
  - projekt
  - bereich/business
  - social-media
erstellt: 2026-09-25
status: Idee, Entscheidungen bei Max offen
---
# 📣 Social Media & Wissensprodukt

⬅️ [[Unternehmensgründung Entscheidung]] · [[Gründung Zeitplan]] · [[Eval-Passing]] · [[Strategie-Logbuch]]

> [!info] Anlass (Max, 25.09.2026)
> 50.000 $ in 5 bis 10 Jahren aus Prop-Payouts sind stabil, aber nichts, wovon man leben kann. Deshalb **parallel** zum Buch einen Social-Media-Kanal aufbauen: anderen beibringen, was ich über systematisches Trading, Quant-Methodik und das Arbeiten mit KI-Agents gelernt habe. Später vielleicht ein Produkt (Mentorship, Kurs, eventuell Algorithmen, noch nicht entschieden). Dafür brauche ich **Beweise**.

Passt zu Schritt 2 der Reihenfolge in der CLAUDE.md (Abschnitt „Das große Ziel"): **den Weg früh öffentlich dokumentieren und Publikum aufbauen, bevor es ein Produkt gibt.**

---

## 1. Beweis-Zeitplan (gerechnet 25.09.2026)

Plan AP204 (1× E8 150k k2 ab 02.10., laufende E8 50k + FN1/FN2, Deckel 2.500 $), alle Konten auf gemeinsamem Kalender, 600 Welten je Szenario. Monat 0 ≈ Ende Sept. 2026. Skript `engine/_scratch_ap204_kal/ap204_firstpay.py`, reproduziert Logbuch #175 exakt. Geprüft von `quant-mathematician` (Protokoll korrekt, plausibel gegen Einzelkonten) und `quant-statistician` (Fehlerbalken, Beweiskraft).

**Ehrliche Hauptspalte ist ×0,58** (Hausstandard, Backtest-Edge geschrumpft). Die anderen zeigen die Spanne.

| | ×0,58 (ehrlich) | Letzte 3 J ×0,58 | Backtest | Letzte 3 J | **ohne Edge** |
|---|---|---|---|---|---|
| **Erste bestandene Eval** (Zertifikat), Median | 14,7 M (~Dez. 2027) | 10,4 M | 9,2 M | 6,6 M | 42 % jemals |
| **Erster Payout**, Median | **27,6 M (~Jan. 2029)** | 19,3 M (~Mai 2028) | 15,7 M (~Jan. 2028) | 11,2 M (~Sept. 2027) | 25 % jemals |
| P(erster Payout bis 12 M) | 17 % | 25 % | 30 % | 53 % | 5 % |
| P(erster Payout bis 18 M) | 33 % | 45 % | 58 % | 78 % | 9 % |
| P(erster Payout bis 24 M) | 46 % | 62 % | 78 % | 89 % | 13 % |
| **Erstmals netto im Plus**, Median | 35,5 M | 25,2 M | 18,7 M | 13,9 M | 16 % jemals |
| Erster Payout, Betrag (Median) | 566 $ | 689 $ | 728 $ | 655 $ | 589 $ |
| Brutto-Payouts nach 24 M (Median) | 0 $ | 1.867 $ | 4.742 $ | 12.863 $ | 0 $ |
| Brutto-Payouts nach 36 M (Median) | 2.506 $ | 6.557 $ | 17.463 $ | 34.180 $ | 0 $ (p90 2.797) |

Fehlerbalken aus den 600 Welten: ±3 bis 4 pp bei den Quoten, ±1 bis 2,3 Monate beim Median. Die Unsicherheit steckt im Szenario (11 bis 28 Monate), nicht im Rauschen.

Kleine Verzerrungen, die sich grob aufheben: FN1/FN2 starten im Modell bei 0, obwohl sie schon Gewinn haben (pessimistisch). Bearbeitungszeit der Firmen und KYC fehlen (+0,3 bis 0,7 Monate, optimistisch). Beim E8 50k ist der bisherige Höchststand unbekannt.

> [!warning] Was ein Payout beweist (quant-statistician)
> **Ein einzelner Payout ist ein Ereignis, kein Beleg.** Jeder vierte Pfad ohne jede Edge zahlt irgendwann aus, weil Nachkäufe Lotterielose sind. Das Verhältnis „mit Edge vs. ohne" liegt nach 24 Monaten nur bei etwa 3,5 zu 1. Selbst nach 3 Jahren liegen die Brutto-Payouts im ehrlichen Szenario nur in etwa der Hälfte der Fälle über der Glücksgrenze.
> **Was wirklich trägt:** der **vollständige Live-Tradelog aller Konten** (nicht nur die Gewinner) plus die **Netto-Rechnung** (Payouts minus alle Käufe, auch der Busts). Nur Payouts zeigen wäre Survivorship. Statistisch braucht es etwa (2 / Sharpe)² Jahre Live, also rund 1,8 Jahre bei Sharpe 1,5 und 4 Jahre bei Sharpe 1,0.
> **Genau das ist der Content-Vorteil:** alles zeigen, auch die Busts, ist ehrlicher als jeder Payout-Screenshot und beweist mehr.

---

## 2. Leitplanken (stehen schon, hier nur gebündelt)

1. **Nie vor dem Beleg verkaufen.** Content ja, ab sofort. Bezahlprodukt erst nach 12 Monaten Live-Track-Record.
2. **Verkaufbar ist der Prozess, nie die Edge.** Eine verkaufte Strategie verwässert (Nachahmer, Kapazität), und Signale, Copy-Trading oder fremdes Geld verwalten können in DE schnell lizenzpflichtig werden (genaue Grenze: offene Frage, siehe unten).
3. **Kein Backtest-Screenshot als Beweis.** Beweis heißt Live: Firmen-Zertifikate, Payout-Belege, Live gegen Backtest (`live-reconciler`), später Steuerbescheid.
4. **Ein einzelner Payout beweist keine Edge.** Siehe Nulldrift-Zeile in Abschnitt 1: auch ohne Edge zahlen Konten manchmal aus. Tragen tut erst die Summe: mehrere Konten, Live passt zum Backtest, über 12 Monate.
5. **Keine Kontonummern, Logins oder Firmen-Interna öffentlich.**
6. **Ehrlichkeit ist das Produkt.** Todesurteile, Fehler und Minus-Monate gehören genauso in den Kanal wie Payouts. Genau das zeigt sonst kaum jemand.

---

## 3. Content-Säulen (Material liegt schon im Vault)

| Säule | Worum es geht | Material |
|---|---|---|
| **Der Friedhof** | Strategien, die wir beerdigt haben, mit Grund, Reichweite und Stempel. Das Alleinstellungsmerkmal. | [[Strategie-Logbuch]] (#133, #067/#068, #165 als Vorbilder), [[Friedhof-Analyse (17.09.2026)]] |
| **Wie man sich selbst betrügt** | Look-ahead, geschenkter Tick, Limit-Fill-Illusion, Overfitting, zu viele Trials | Logbuch #066/#067, #171, 22.09. Limit-Entry, Gate v2 |
| **Prop-Firm-Mathematik** | Größe kauft Bust, nicht Tempo. Passquote vs. Zeit bis Ziel. Nulldrift-Kontrolle. Warum 93 % „Funding-Chance" in YouTube-Videos Marketing sind. | Logbuch #106, #175, Research-Cache (IQCapital-Video) |
| **Bauen mit KI-Agents** | Wie ein 19-Jähriger mit Claude ein Quant-System baut: Agents, Hooks, Gates, „Rechnen macht die Maschine, entscheiden macht Claude" | [[Hooks-Referenz]], [[Discovery-Runner v2]], [[Strategy Lab Workbench]] |
| **Live-Tagebuch** | Evals, Busts, Payouts, Live gegen Backtest, monatlich | Daily Notes, `live-reconciler` |
| **Der Weg** | Ausbildung, Job, BOS, Plan Finance und Quant, Gewerbe gründen mit 19 | [[Über mich]], [[Unternehmensgründung Entscheidung]] |

---

## 4. Entscheidungen bei Max

- [ ] **Plattform(en):** YouTube (lang, Tiefe) / Instagram, TikTok (kurz, Reichweite) / X oder LinkedIn (Quant- und Finance-Netzwerk, passt zum Werdegang) / Newsletter
- [ ] **Sprache:** Deutsch (kleiner Markt, wenig Konkurrenz mit ehrlicher Quant-Methodik) oder Englisch (großer Markt, mehr Konkurrenz)
- [ ] **Gesicht zeigen** oder anonym mit Marke
- [ ] **Name, Marke, Domain** (Domain ≈ 15 €/Jahr, steht schon in der Kostenliste der Gründung)
- [ ] **Rhythmus**, der neben Vollzeitjob und Buch realistisch ist (lieber klein und konstant)
- [ ] **Algorithmen verkaufen: ja oder nein?** Empfehlung Claude: nein, Methodik statt Edge (Leitplanke 2).

## 5. Offene Fragen (klären, bevor es öffentlich wird)

- [ ] **Rechtliches (research-scout, später Fachanwalt oder IHK):** Wo ist in DE die Grenze zwischen Bildung und erlaubnispflichtiger Anlageberatung oder Finanzdienstleistung? Algorithmen oder Indikatoren verkaufen, Signale, Copy-Trading? Pflicht-Disclaimer und Impressum für Social-Media-Kanäle?
- [ ] **Arbeitgeber:** deckt die Nebentätigkeits-Genehmigung vom 23.09. (Trading/Gewerbe) auch Content und Mentorship ab?
- [ ] **Steuer (Gespräch mit Freundin):** Einnahmen aus Werbung, Affiliate und Mentorship im selben Gewerbe? Wirkung der Kleinunternehmer- bzw. Regelbesteuerungs-Bindung (steht schon in [[Gespräch mit Freundin (Steuer & Gründung)]] Frage 30).
- [ ] **Prop-Firmen:** erlauben E8 und FundedNext öffentliche Posts über Konten, Zertifikate und Payouts? Affiliate-Programme als zusätzliche Einnahme?

## 6. Nächste Schritte

1. Max entscheidet Plattform, Sprache, Gesicht (Abschnitt 4).
2. `research-scout`: rechtliche Grenze Bildung vs. Finanzdienstleistung, Prop-Firm-Regeln zu öffentlichen Posts.
3. Erste 10 Themen aus den Content-Säulen als Liste, das erste Stück aus dem Friedhof.
4. Beweis-Sammlung ab jetzt systematisch ablegen (Zertifikate, Payout-Belege, monatlicher Live-Abgleich), am besten im [[Belegordner 2026]] mit.
