---
tags: [trading, prop, eval, funded, portfolio-tab, tempo_plan]
datum: 2026-10-18
status: Einschätzung fertig, Entscheidungen bei Max
tickets: [AP111, AP204, AP334, AP335, AP379, AP392, AP396]
---

# Eval vs. Funded Neubewertung (18.10.2026)

⬅️ [[Funded-Phase]] · [[Eval-Passing]] · [[Firm-Regeln je Konto]] · [[Kaufvorlage Kaufrunde 06.11.2026]] · [[Hochstuf-Regel je Konto (Entwurf)]]

**Frage Max:** Seit dem 18.09. ist das Ziel „Zeit bis 50.000 $ aus Payouts“. Passt der Portfolio-Tab (Eval / Funded / Live) mit seiner Kosten-Kennzahl noch dazu? Und sollten wir Eval und Funded je Firma unterschiedlich fahren, weil die Regeln je Phase verschieden sind? Umfang: alle 5 Konten plus Kaufplan (E8 150k und FFN 150k im Wechsel ab 06.11.).

> [!important] Kurzantwort
> 1. **Die Kosten-Kennzahl im Tab ist das alte Ziel und gehört raus.** „Passquote je Eval und $ pro funded“ sortiert die Firmen fast umgekehrt zum Ziel. Oben gehört die Zeit bis 50k hin.
> 2. **Eval und Funded getrennt fahren lohnt sich an genau einer Stelle sicher: die Größe.** Die Eval bleibt immer k1. k2 gibt es höchstens im Funded der 150k-Konten, erst nach dem Floor-Lock und nur über die Hochstuf-Regel. Heute heißt das k1 überall, weil die Vola zu hoch ist.
> 3. **FFN im Funded nur volle Caps auszahlen** wäre in schwachen Jahren 6 bis 10 Monate schneller. Das Ergebnis hängt aber an einer FFN-Regel, die keiner kennt: Was passiert nach dem 5. Payout? **Noch nicht entscheiden**, erst die FFN-Antwort holen. Druck gibt es keinen, der erste FFN-Payout liegt frühestens rund 10 Monate entfernt.
> 4. **Der Rest bleibt gleich:** gleiche Beine, Tagesstopp 2.500 $, Consistency-Deckel nur in der Eval. Die FFN-News-Sperre im Funded ist Pflicht (AP335) und billiger, als ein Bein zu streichen.
> 5. **Nebenbei gefunden:** E8 150k zahlt bei Neukauf weniger aus, als alle unsere Modelle annehmen. Dazu rechnet tempo_plan wegen eines Cache-Fehlers mit 3,2 % zu viel Drift. Beides muss vor der Kaufrunden-Neurechnung am 05.11. gefixt sein.

---

## 1. Was wir damals gemacht haben

- **16.08. (#106):** Zielfunktion „Passquote je Eval und $ pro funded Konto“ bei Min-Size. Das steht bis heute als `objective: cost_per_funded` in `portfolio.json`.
- **18.09.:** Ziel umgestellt auf Zeit bis 50.000 $ aus Payouts minus Käufe (tempo_plan, später Kalender-Modus). Der Portfolio-Tab ist dabei nie mitgezogen worden.
- **25./26.09. (Session 65f70e60):** Eval gegen Funded mit 7 Agents. Ergebnis „im Funded am Handeln nichts ändern“, einziger Funded-Hebel war die FN-Auszahlung nach Floor-Lock. Gerechnet am 3-Bein-Buch mit E8 150k k2, FFN gab es noch nicht.

**Warum neu gerechnet:** Buch (4 Beine live), Betriebspunkt (k1 überall statt k2) und Firmen (FFN STEADY 150k mit sehr verschiedenen Phasen-Regeln) haben sich geändert. Die Trust-my-Work-Regel greift also nicht.

---

## 2. Ergebnis je Hebel

Zwei unabhängige Rechner (quant-mathematician, quant-statistician), Kalender-Modus, Kaufplan P5B, Bestand 16.10., gepaart auf denselben Pfaden, 400 bis 800 Welten je Regime, Nulldrift-Zwilling, 13 Varianten, Bonferroni z ≈ 2,85. Werte = Unterschied in Monaten bis 50k (Median), negativ = schneller. Spalten: alle Jahre / letzte 3 J / Drift ×0,58 / Vola heute (466 $ je Tag, Sharpe ×0,58). Wo die beiden Rechner abweichen, steht die Spanne.

Basis (P5B, k1 überall): Median 46 / 28 bis 29 / 90 / 70 bis 84 Monate, Plan-Tod 0 / 0 / 7 / 26 %, Auslage p90 2.210 $, Nulldrift 0 %.

| Hebel | Phase | Monate bis 50k | Preis | Urteil |
|---|---|---|---|---|
| **k2 in der Eval** (150k) | Eval | −13 bis −19 / −8 bis −12 / −3 bis −16 / **+23 bis +50** | Plan-Tod +17 bis +20 pp, Nulldrift verletzt | **nicht ändern, Eval bleibt k1** |
| **k2 im Funded** (beide 150k) | Funded | −11 / −4 bis −6 / −6 bis −10 / **+13 bis +22** | Funded-Busts +8 bis +17 pp | **nur nach Floor-Lock und nur über die Hochstuf-Regel**, heute nicht |
| k2 im Funded schon vor dem Lock | Funded | etwas schneller in guten Jahren, bei Vola heute +6 bis +14 | Risiko wie in der Eval | nicht ändern |
| **FFN nur volle Caps auszahlen** | Funded | 0 / 0 / **−6 bis −10** / **−8 bis −10** | erster FFN-Payout 3 bis 7 Monate später, Netto nach 24 Monaten in allen Regimen niedriger (−0,1 bis −1,8 k$, BOS-Zeit), bis 7.700 $ über Start im Konto | **offen, hängt an FFN nach dem 5. Payout** (Abschnitt 3) |
| E8 150k nur volle Caps | Funded | −0,4 bis −0,6 / −0,2 bis −0,4 / −1 / −2 bis +0,4 | kaum | echt, aber zu klein. Bleibt bei sofort, neu prüfen mit den echten Caps |
| FN 50k erst nach Lock, E8 50k volle Caps | Funded | alles unter 0,5 Monate | keiner | unentscheidbar, Playbook bleibt |
| **FFN T1-News-Sperre** | Funded | +0,4 bis +0,9 / +0,7 bis +0,8 / +1,6 bis +2,1 / +4,9 bis +8,4 (Obergrenze) | Regelpflicht | **Pflicht (AP335).** Sperre kostet 311 $ je Jahr, LastHour streichen 1.423 $, also Sperre statt Bein-Abwahl |
| Tagesstopp 1.500 statt 2.500 | Funded | 0 / 0 / 0 / +7 | | nicht ändern, 2.500 $ bleibt |
| Consistency-Deckel nur in der Eval | Eval | nicht neu gerechnet | FFN-Deckel 4.212 $ gegen größten Tag 2.961 $ | bestätigt, wie geplant |
| andere Beine je Phase | beide | außer T1 kein Unterschied | | nicht ändern, Asia ist keine Phasenfrage (AP387) |

**Kipppunkt für k2 im Funded** (Mathematiker, Formel): k2 nach dem Lock hilft, solange die Tagesschwankung der Kontobelegung unter rund 236 bis 295 $ (FFN) bzw. 205 bis 256 $ (E8 150k) liegt. Die Hochstuf-Regel steht mit 235 $ bzw. ~200 $ knapp darunter, ist also vorsichtig und nicht zu locker. Heute: σ60 449 / 330 / 459 $, deshalb k1.

### Korrektur zum 26.09.: Mindest-Tage bremsen bei k1

Die 35-%-Best-Day-Regel von E8 ist skaleninvariant, die Mindest-Tage im Funded sind es nicht. Anteil der Tage über der Schwelle (alle Jahre, CI90) und Monate für 5 solcher Tage:

| Firma, Schwelle | k1 | k2 |
|---|---|---|
| E8 50k, 150 $ | 16,7 % [14,6; 18,8], 2,4 M | 26,8 %, 1,5 M |
| FN 50k, 200 $ | 13,0 %, 3,0 M | 22,7 %, 1,7 M |
| FFN 150k, 250 $ | 10,2 % [8,5; 12,1], 3,8 M | 19,7 %, 2,0 M |
| **E8 150k, 450 $ (ab 2. Payout)** | **4,3 % [3,3; 5,4], 9,1 M** | 11,7 %, 3,4 M |

Bei E8 150k mit k1 bremsen ab dem 2. Payout die 450-$-Tage, nicht das Geld. Bei FFN mit k1 bremst vor allem der Mindeststand für den ersten Payout (4.700 $ Buffer plus 500 $): Median 10,5 Monate bis zum ersten FFN-Payout (alle Jahre), 18 Monate bei Drift ×0,58.

---

## 3. Neue Regel-Fakten (research-scout, 18.10.)

Eingetragen im [[Research-Cache]], Abschnitt „Auszahlungspolitik im Funded …“.

**E8 Signature 150k, Kauf nach dem 01.10.2026 (primär, E8 Help Center Art. 11755943 und 11940573):**
- Höchstens **4 Payouts**, danach Konto weg, Rest verfällt, Gratis-Challenge gleicher Größe.
- Caps brutto **3.000 / 3.000 / 3.500 / 3.500** (13.000 $, bei 80 % 10.400 $ netto). Die 3.250 / 3.250 / 4.250 / 4.250 galten nur für Käufe vor dem 01.10.
- DD 4.000 $ (vorher 4.500).
- 5 Tage ≥ 450 $ ab dem 2. Payout gilt so, Zähler nach jedem Antrag auf 0. Profit über dem Cap ist vermutlich für den nächsten Zyklus verloren (Lesart offen).
- **Folge:** tempo_plan, Kaufvorlage und auch die Rechnung von heute rechnen E8 150k mit 2.000 $ brutto zu viel je Konto. Die Kaufvorlage ist für E8 also zu freundlich (gehört zu AP392 und AP111).

**FFN STEADY 150k nach dem 5. Payout (primär für Ablauf, sonst ungeklärt):**
- Nach 5 Payouts kommt ein Live-Review. Live geht es nur mit Freigabe des Risk Managers, der Sim-Gewinn **verfällt** beim Wechsel, danach 90/10 mit täglichen Payouts.
- Live-Kapital, Live-Caps, Live-DD, Freigabekriterien und was bei Ablehnung passiert: **nirgends dokumentiert.**
- Laut FFN-FAQ kosten Live-Konten 126 $ Daten-Gebühr je Monat und Börse (nur eine Seite, Geltung für STEADY offen).
- Ob man beim Antrag den Betrag frei wählen kann: sehr wahrscheinlich, aber nicht ausdrücklich geregelt. Eine Antragsfrist gibt es nicht.
- Das FFN-Help-Center lieferte heute 403, die FFN-Zeilen stützen sich auf Suchindex-Auszüge. **Art. 2.5 und 5.2 einmal selbst im Browser gegenlesen**, bevor darauf Geld gesetzt wird.

**Warum das den FFN-Hebel offen lässt (Gegenleser verdict-auditor):** Der ganze Vorteil von „volle Caps“ kommt daraus, dass das Modell das FFN-Konto nach 5 Payouts enden lässt. Wer sofort auszahlt, verbraucht die 5 Slots mit rund 1.670 $ brutto pro Stück. Läuft das Konto nach Freigabe aber live weiter, kommt „sofort“ schneller ins Live-Konto und kann den Nachteil zurückholen. Ob das passiert, hängt an Freigabe, Live-Kapital und Gebühr. Die heutige Annahme „endet nach 5“ ist die vorsichtige Seite, solange niemand die Live-Bedingungen kennt.

---

## 4. Portfolio-Tab: was falsch ist und was hin gehört

**Heute:**
- Eval- und Funded-Reiter lesen dasselbe `portfolio.json` (Stand 04.10.) mit `objective: cost_per_funded`.
- Der Kopf ist auf die Stufe 50k verdrahtet, 150k steht dort noch mit DD 4.500 und 390 $.
- Der Funded-Reiter zeigt `funded_analysis.json` vom 18.08. (E8 50k, 3 Beine).
- FFN fehlt ganz, der plan-Block kennt nur E8 50k und FN (AP396).

**Warum $/funded falsch sortiert:** FN 50k ist mit 97 $ je funded am billigsten und bringt je Kauf am wenigsten (1.768 $ netto, bei Drift ×0,58 nur 550 $). E8 150k ist mit 336 $ am teuersten und bringt je Kauf am meisten (9.369 $). Die Passquote der 150k-Konten liegt bei k1 je nach Regime bei 72 bis 99 %, sie trennt also nichts. Entscheidend sind dort die rund 18 Monate bis zum Pass.

**Vorschlag (bewertet, nicht gebaut):**
- **Kopf über beiden Reitern:** Monate bis 50k (Median und Chance in 5 Jahren) aus tempo_plan im Kalender-Modus mit echtem Bestand und echter Kaufpolitik. Spalten alle Jahre / letzte 3 J / Drift ×0,58 / Vola heute, dazu Nulldrift-Zwilling, Auslage p90, Netto bei Gehaltsende und nach 24 Monaten.
- **Eval-Reiter, je Konto ab heutigem Stand:** P(Pass), Monate bis Pass, P(Bust vor Pass), Puffer in Tagesschwankungen, am echten k und Stopp.
- **Funded-Reiter, je Firma unter den Funded-Regeln:** Monate bis zum 1. Payout, Abstand der Payouts mit der Regel, die gerade bremst (Mindest-Tage, Geld oder Cap), Netto je Konto, P(Funded-Bust), Kosten der T1-Sperre.
- **$/funded** höchstens klein als Einkaufspreis neben „Netto je Kauf“.
- Vieles davon rechnen die Konto-Karten (`engine/konten/cards`) schon. Der Tab sollte die Karten anzeigen statt eine dritte eigene Rechnung zu bauen.
- Der Live-Reiter war nicht Teil der Frage und bleibt, wie er ist.

---

## 5. Plan

**Ohne Entscheidung machbar (Fehler, keine Politik):**
1. **Gebühren-Cache fixen:** der Schlüssel in `cage_policy_lib.load_pool` enthält weder Gebühr noch Engine-Stand. tempo_plan rechnet deshalb mit 40,16 statt 38,92 $ je Tag (+3,2 % Drift). Muss vor der Kaufrunden-Neurechnung am 05.11. weg.
2. **Modelle auf die echten Regeln:** E8 150k Neukauf (4 Payouts, Caps 3.000 / 3.000 / 3.500 / 3.500, DD 4.000) in tempo_plan, Konto-Karten und weekend_check. Dazu der FN-Formel-Fix (`tempo_plan.py:384`, `konten/funded_kernel.py:151`, 50 % seit dem letzten Payout). Gehört zu AP392 und AP111.
3. **FFN-Support-Mail** (Entwurf durch Claude, Max schickt): Live-Kapital, Live-Caps und Live-DD nach dem 5. Payout, Freigabekriterien, was bei Ablehnung passiert, ob der Algo auf der Box auch live erlaubt ist, ob der Auszahlungsbetrag frei wählbar ist und ein Rest später abrufbar bleibt, ob die 500 $ über Buffer auch für STEADY gelten, ob ein Live-Konto bei den 5 Funded-Konten mitzählt, ob die 126-$-Gebühr für STEADY-Live gilt. Für E8: ob Profit über dem Cap verloren ist.

**Entscheidung Max (Wochenende):**
4. **Hochstuf-Regel nach Phase trennen:** Eval immer k1. k2 nur auf 150k-Konten im Funded nach dem Floor-Lock (FFN Hoch ≥ +4.800 $, E8 Hoch ≥ +4.000 $) und nur bei σ60 ≤ 235 $ (FFN) bzw. ~200 $ (E8). Passt in AP379. Vor der Übernahme den 12-Monats-Bust je Konto für k2 ab Lock nachrechnen (Track-Record-Leitplanke).
5. **FFN-Auszahlungspolitik:** erst nach der FFN-Antwort. Dann eine Gegenprobe rechnen, in der das Konto nach dem 5. Payout mit Wahrscheinlichkeit 0 / 0,5 / 1 live weiterläuft (mit den echten Live-Bedingungen). Kippt „volle Caps“ schon bei 0,5, bleibt es bei sofort. Hält es auch bei 1, kommt es ins Playbook. Nur falls es hält: die Zwischenpolitik „1. Payout sofort als Beleg, danach volle Caps“ beziffern.
6. **Portfolio-Tab umbauen** wie in Abschnitt 4, mit design-guard. Erst nach Punkt 1 und 2, sonst zeigt die neue Kopfzahl falsche Zahlen.
7. **Playbook [[Funded-Phase]] nachziehen:** E8-150k-Fakten (Abschnitt 3), Korrektur Mindest-Tage, Größe je Phase aus Punkt 4.

**Schon geplant, bleibt Pflicht:** T1-Sperre vor dem ersten FFN-Funded-Trade (AP335), auch für den M2K-Host. tempo_plan bekommt die Phasen-Varianten (Patch-Vorschlag des Mathematikers liegt in `psl.py`, bit-gleich mit tempo_plan), passt zu AP334.

---

## 6. Was die Rechnung nicht kann

- Buchdaten nur bis 06./07.08.2026 (AP313, AP356). Die Vola heute ist auf diesem Stand gemessen.
- RTY-Gap auf FFN1/FFN2 nicht gerechnet (rund 300 $ je Jahr).
- HFT-Regel, Inaktivität und Liquidation durch die Firma bei Regelbruch nicht modelliert. Die T1-Sperre ist als „Trade fällt weg“ genähert, ist also eine Obergrenze.
- Das Vola-Regime nimmt einen konstanten Sharpe an, die Drift wächst mit der Vola. Das k2-Urteil hängt direkt daran.
- Die Hochstuf-Regel als dynamische Umschaltung während des Laufs ist nicht simuliert, nur feste Regime.
- E8 150k mit den alten, zu hohen Caps gerechnet. Die Richtung der Urteile ändert sich dadurch nicht, die absoluten Monate für E8 werden etwas schlechter.
- Die Fehlerbalken messen nur das Pfad-Rauschen. Die echte Unsicherheit ist die Spanne zwischen den Regimen.

---

## 7. Belege

- Rechnungen: `C:\Users\maxlk\Projects\trading-data\engine\_scratch_phase_split_v2\` (Mathematiker: `psl.py`, `test_bit.py`, `fleet.py`, `ana.py`, `results\ana.txt`, `results\struct.json`; Statistiker: `stat\README.md`, `stat\results\ana_main.json`, `ana_vol.json`, `s1_qdays.json`, `s3_cadence.json`, `s2_costfunded.json`). Engine, Buch, RiskGuard, Host-Dateien und Box sind nicht angefasst.
- Stempel: Engine d6c9b15a4ada, Zellen `konten/cache/legcells_fa89a976da4b` (Gebühr 1,90 $), tempo_plan md5 30b89227, ffnlib 3ddae4c2, Buch ff4710ef.
- Konto-Karten 18.10. (konto-analyst): alle 5 Konten in der Eval, k1, Ampel gelb, Datenstand 10.08.
- Gegenleser verdict-auditor: 5 von 6 Stempeln tragen, „FFN volle Caps ändern“ trägt noch nicht (Abschnitt 3).
- Vorarbeit: [[Daily Notes/2026-09-26]] Abschnitt „Eval vs. Funded“, [[Strategie-Logbuch]] #106, #117, #130, #175.
