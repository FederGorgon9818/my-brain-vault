---
tags:
  - ressource/research
  - trading/orb
erstellt: 2026-08-09
status: abgeschlossen
---
# 🧪 ORB-Runde #070 — Hypothesen VORAB fixiert

⬅️ [[Strategie-Logbuch]] · [[ORB Master-Synthese (Eval-Fokus)]] · [[Discovery-Prozess (wie wir Alpha finden)]]

> [!important] Zweck dieser Datei
> Nach [[Discovery-Prozess (wie wir Alpha finden)|Prozess-Schritt 1]] braucht **jeder Mechanismus ein dokumentiertes „Why" VOR dem Test**. Diese Datei entsteht deshalb, bevor ein einziger Backtest läuft. Alles, was hier nicht steht und später „gefunden" wird, ist Data-Mining und bekommt einen Skepsis-Aufschlag.

## Ausgangslage (Stand nach #068)
Der klassische Breakout-ORB auf Index-Futures ist ehrlich tot: **kein Follow-Through nach dem Linien-Break** (Break-Bar +1,1 Pkt, danach bis EOD −0,6 Pkt = Coinflip). Übrig sind drei ehrliche Dinge:

| Ding | expR | Status |
|---|---|---|
| ORB-Fade + NR7 (NQ) | +0,063 | im Buch (Bein 4) |
| `ORB_VIXBAND_NQ` (Chuk-Faktor) | +0,10 im VIX-Band 15-25 | Bank, Auto-Fit abgelehnt |
| `NOISE_ORB_NQ_m1.0` (Zarattini 4824172) | +0,094, IS ≈ OOS | Bank, Auto-Fit abgelehnt |

## 🔑 Die Leit-Einsicht dieser Runde
Es gibt einen scheinbaren Widerspruch in unseren eigenen Daten:

- **Linien-Break hat KEIN Follow-Through** (#068).
- **Momentum-Displacement ≥0,3%/15min hat +13,6 Pkt echten Drift** (#068, n=796, 56%).

Beides ist gemessen, beides stimmt. Der Unterschied ist der **Trigger-Typ**:
> Ein Break durch ein *Level* sagt nichts über die *Größe* der Bewegung. Ein Displacement schon.

Genau das ist auch der Grund, warum Zarattinis Noise-Band funktioniert und der ORB nicht: das Noise-Band ist **volatilitäts-normiert** (σ(t) der letzten 14 Tage), es triggert nur, wenn die Bewegung relativ zur eigenen erwarteten Tagesbewegung groß ist. Der ORB triggert, wenn ein beliebig dünner Tick über eine beliebig enge Linie geht.

**Arbeitsthese #070:** *Nicht das Level trägt die Edge, sondern die vola-normierte Größe der Bewegung. Alles, was wir am ORB noch holen können, holen wir über die Normierung — nicht über bessere Linien.*

---

## Hypothesen (priorisiert, mit Kill-Kriterium)

### H1 — Noise-Band × VIX-Band (Regime-Conditioning des besten Fundes)
- **Why:** Beide Funde aus #068 sind unabhängig voneinander entstanden und nie kombiniert worden. Der VIX-Band-Effekt (Chuk) hebt einen ansonsten toten close-EOD-ORB von 0,00 auf +0,10 — er ist also ein **Kontext-Faktor, kein Signal**. Kontext-Faktoren sollten auf das *beste* Signal wirken, nicht auf das schlechteste. Der Noise-ORB ist das beste ehrliche Signal, das wir haben.
- **Erwartung:** weniger Trades (~50-60%), höherer expR. Für ein Trailing-DD-Eval ist das der richtige Trade-off (Insight #6: Pfad-Varianz zählt, nicht Langfrist-Erwartung).
- **Kill-Kriterium:** Muss IS **und** OOS heben. Hebt es nur eins, ist es Selektion. Und der Trade-Verlust darf die Passquote nicht unter den Noise-Solo-Wert drücken.

### H2 — Noise-Band auf ES / RTY / YM (Robustheitsprüfung, keine neue Freiheit)
- **Why:** Der Noise-Band-Port läuft mit dem **Paper-Default ohne Tuning** (m1.0). Ihn unverändert auf drei weitere Instrumente zu werfen, fügt **null Freiheitsgrade** hinzu und ist damit der ehrlichste Robustheitstest, den es gibt: hält der Mechanismus, ist er echt; kippt er, war NQ Glück.
- **Dämpfer (bewusst vorab notiert):** Nach #026 korreliert **gleiche Mechanik über Instrumente** stark (Index-Futures co-bewegen ~0,9). Ein ES-Noise-ORB wird das Buch daher vermutlich **nicht** über den Auto-Fit tragen — sein Wert liegt primär in der Falsifikation/Bestätigung, sekundär im Buch.
- **Kill-Kriterium:** Wenn ≥2 von 3 Instrumenten OOS-negativ sind, ist auch der NQ-Fund verdächtig und wandert von „Bank" auf „nur NQ-Zufall".

### H3 — Der Fade konsequent zu Ende gedacht (Spiegel-Trick auf den #068-Kernbefund) ⭐ **aufgewertet**
- **Why:** Wenn nach dem Break kein Follow-Through kommt, die Break-Bar selbst aber schon +6,4 Pkt gelaufen ist, dann ist „gerade impulsiv ausgebrochen" ein Zustand **erhöhter Rückkehrneigung**. Das ist Insight #7 (Spiegel-Trick) angewandt auf unseren eigenen frischesten Befund. Unser Fade-Bein nutzt aktuell nur NR7 als Filter — die **Spike-Größe selbst** wurde nie als Fade-Filter getestet.
- **🆕 Externe Rückendeckung (Recherche 09.08., siehe [[Research-Cache]] #070-Block):** **Grant/Wolf/Yu (2005), Journal of Banking & Finance** ([SSRN 689282](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=689282)) finden Intraday-**Reversal nach großen Opening-Moves** in US-Aktienindex-Futures, hoch signifikant über 15 Jahre (1987-2002) — und **stärker nach positiven Open-Moves**. Das ist exakt H3, peer-reviewed, und deckt sich fast wortwörtlich mit unserem #068-Befund. Warnung aus dem Paper selbst: die Signifikanz bricht stark ein, sobald ein Bid-Ask-Kostenproxy dazukommt → **unsere Netto-Rechnung ist hier die entscheidende Hürde, nicht die Signifikanz.**
- **Konkret zu testen:** (a) Größe der Ausbruchs-Bar relativ zu σ als Fade-Filter, (b) VIX-Regime (Fade sollte laut [[Alpha-Konzepte]] bei *niedrigem* VIX besser sein — spiegelbildlich zum Breakout), (c) Distanz des Ausbruchs über das Level, (d) **🆕 Richtungs-Asymmetrie**: Short-Fade nach Up-Break vs. Long-Fade nach Down-Break getrennt auswerten (Grant/Wolf/Yu sagen: Up-Moves reverten stärker).
- **Kill-Kriterium:** Der bestehende Fade (+0,063) ist die Latte. Eine Variante muss ihn IS und OOS **netto** schlagen, sonst bleibt Bein 4 wie es ist (Simplex beats Komplex). Bei der Asymmetrie zusätzlich: n pro Seite muss reichen, sonst ist es Halbierung der Stichprobe statt Erkenntnis.

### H4 — Exit-Raum gegen das Eval-Objektiv statt gegen expR
- **Why:** Laut [[Discovery-Prozess (wie wir Alpha finden)]] unser **am wenigsten ausgereizter Hebel** — dasselbe ORB-Entry mit 0,3R-Target statt 1R hob die Win-Rate 62% → 87% und **dekorrelierte** (corr 0,08). Bisher wurde immer auf expR optimiert; das Eval bestraft aber Pfad-Varianz (Insight #6). Für Noise-ORB und Fade nie systematisch durchgespielt.
- **Kill-Kriterium:** Muss P(pass) des Buchs heben, nicht expR. Wenn die Exit-Variante nur die Win-Rate hübsch macht und die Passquote steht, ist es Kosmetik.

### H5 — Auto-Fit-Ablehnung der beiden #068-Funde über die volle Frontier prüfen
- **Why:** Beide Funde wurden am **Betriebspunkt** abgelehnt (Quote runter, Speed rauf). Der Vergleich lief nie über **alle fracs**. Bei einem Eval mit Reset-Option ist „52% in 53 Tagen" möglicherweise *besser* als „57% in 86 Tagen" — die relevante Größe ist Zeit-bis-Funded-EV inkl. Resets, nicht die nackte Einzel-Passquote.
- **Kill-Kriterium:** Kein neuer Backtest nötig, reine Auswertung. Wenn die Frontier-Kurven sich nicht schneiden, ist die Ablehnung korrekt und das Thema erledigt.

---

---

## 📚 Was die Literatur-Recherche (09.08.) ergeben hat
Vier Suchrichtungen abgeklopft, **ein** verwertbarer Fund, drei ehrliche Sackgassen. Details im [[Research-Cache]] #070-Block.

| Richtung | Ergebnis |
|---|---|
| Failed-Breakout / Opening-Reversal | ✅ **Grant/Wolf/Yu 2005 (JBF)** — stützt H3, siehe oben |
| Neue Zarattini-Arbeiten 2025/26 | ❌ **keine.** Concretum ist auf GTAA/Vol-Targeting/Krypto weitergezogen → der ORB-Zweig ist auch bei der Quelle selbst zu Ende erforscht. Spart uns künftige Wiederholungssuchen. |
| „Turtle Soup" / Liquidity-Sweep am OR-Level | ❌ **reine Retail-Folklore**, keine einzige Quelle mit Zahlen oder Backtest. Keine Literatur-Lücke, die man schließen kann — dort ist schlicht nichts publiziert. |
| VIX-Term-Structure (VIX9D/VIX, VVIX) als Gate | ❌ nichts Belastbares. Der Chuk-VIX-Band-15-25-Befund bleibt unsere einzige Vol-Regime-Quelle. |

> [!note] Konsequenz für die Priorisierung
> Es gibt **nichts Neues zu bauen, das von außen kommt.** Der Wert dieser Runde muss aus unseren eigenen Daten kommen (H1-H5). Das ist kein schlechtes Zeichen — es heißt, wir sind an der Front und nicht mehr am Nachbauen.

## Was diese Runde NICHT nochmal anfasst
Erledigt und dokumentiert in #067/#068 — wird nicht neu gegrided:
- Breakout-ORB in allen Exec-Varianten (book/close/stop_honest) · Pineda-Retest (2× falsifiziert) · „Index in Play" / OR-RVOL · NR7-Breakout-EOD (Tail-Lotterie) · Zarattini-STD roh · Wochentags-Faktor.

---

## ✅ Ergebnis (Abschluss 09.08.2026)
Volle Auswertung in [[Strategie-Logbuch]] **#070**. Kurzfassung gegen die oben fixierten Kill-Kriterien:

| # | Vorab-Erwartung | Ergebnis | Kill-Kriterium |
|---|---|---|---|
| H1 | VIX-Band hebt Noise-ORB | ❌ **falsifiziert** — hebt nur IS (0,094→0,189), OOS bricht ein (0,034); Gegenprobe *außerhalb* ist OOS besser (0,235) | griff exakt wie formuliert |
| H2 | Paper-Default hält auf ES/RTY/YM | ⚠️ **NQ hält sauber, generalisiert nicht** (RTY tot, YM tot, ES fraglich) | formal knapp verfehlt, qualitativ erfüllt |
| H3a | Fade lebt bei niedrigem VIX | ❌ **umgekehrt** — vix10-18 ist die schwächste Zelle | These widerlegt |
| H3b | SHORT-Fade > LONG-Fade (Grant/Wolf/Yu) | ⚠️ **nur scheinbar** — kippt vor 2022 ins Gegenteil | Regime-Artefakt |
| H3c | R/σ als Qualitätsachse | 💀 **toter Test** — Quotient per Konstruktion konstant 0,4 (eigener Bug) | kein Ergebnis |
| H4 | Enge Exits heben P(pass) | ❌ T1.0 unter Baseline, T0.5 hebt Win% aber nicht expR | kein Gewinn |
| H5 | Frontier über alle fracs statt Betriebspunkt | ✅ **bestätigt und relevant** — Noise-ORB macht das Buch fensterstabil (53/53 statt 51/63) | — |

> [!danger] Der eigentliche Fund war keiner der fünf
> Beim Messen der Fade-„Latte" fiel auf, dass **Bein 4 selbst** das Discovery-Gate verletzt: 8 Jahre netto +95$, dann +5.672$ in 2,5 Jahren; Top-10 von 422 Trades = 127% des Gewinns. Daraus wurde der erste **fenstergetrennte Passquoten-Stresstest** des Buchs — und der zeigt, dass die 57%/86d eine Eigenschaft des Endfensters sind (IS: 51%/117d). Siehe #070.

**Methodisch gelernt:** die drei Schutzmechanismen, die diese Runde ehrlich gehalten haben, waren (1) Primärtest vorab deklariert, (2) **Gegenprobe der Komplementärmenge**, (3) adversariales Gegenlesen *vor* der Interpretation. Punkt (2) hat H1 gekillt, Punkt (3) hat meinen H3c-Bug gefunden.
