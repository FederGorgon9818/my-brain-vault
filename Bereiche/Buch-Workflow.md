---
tags:
  - bereich/trading
  - trading/buch
erstellt: 2026-09-17
---
# 🖥️ Buch-Workflow — Portfolio-Tab, Next-Week-Buch, Live-Buch, Edge-Health

⬅️ [[Day Trading]] · [[Portfolio-Simulator]] · [[Discovery-Runner v2]] · [[Strategie-Logbuch]]

> [!important] Kernregel (Max, 10.08.2026)
> Sobald sich am Portfolio etwas ändert (neues Bein, Bein raus, andere Parameter, neue Firma/Frac), **im selben Zug den Portfolio-Tab im Strategy Lab aktualisieren** — nicht erst „später". Kurzfassung + Trigger stehen in der CLAUDE.md, dieser Weg hier ist die Ausführung.

## Grundmechanik

1. `book_state.json` ist die einzige Quelle der Wahrheit für das Buch **und seit 11.08.2026 auch für Käfig und Betriebspunkt** (Block `plan`: Firma, Target/DD, Cap, Preis pro Eval, Käufe pro Monat, `dd_mode`, Konten mit Cushion-Frac). Vorher standen Käfig und frac hartkodiert in `funded_finalize.py` und liefen still auseinander, sobald sich am Plan etwas änderte.
2. `cd C:\Users\maxlk\Projects\trading-data\engine && python funded_finalize.py` → schreibt `portfolio.json` + Report `PORTFOLIO_optimized`, legt fehlende Bein-Reports automatisch an.
3. Danach prüfen: jedes Bein hat ein `report`-Feld, das auf eine existierende Datei in `reports/` zeigt (sonst 404 beim Klick).
4. `portfolio_tab.py` **nicht** benutzen (veraltet, eingefrorene Juli-Beine, läuft nur noch mit `--force` und fasst `portfolio.json` nicht mehr an).

### Was „Änderung am Portfolio" heißt (Auslöser für Schritt 2)

| Änderung | Wo eintragen |
|---|---|
| Bein rein/raus, andere Bein-Parameter | `book_state.json` → `legs` |
| Anderer Cushion-Frac / Betriebspunkt | `book_state.json` → `plan.accounts` |
| Andere Kontogröße, andere Firma, anderes Target/DD | `book_state.json` → `plan` (+ `firm`/`target`/`dd`) |
| Andere Kaufpolitik (Evals pro Monat, Preis) | `book_state.json` → `plan.buys_per_month` / `price_per_eval_usd` |
| Umstellung des Bust-Checks (eod ↔ intraday) | `book_state.json` → `plan.dd_mode` |

Danach **immer** `funded_finalize.py`, im selben Zug, nicht „später". **Und im selben Zug `python discovery/inbox_tool.py --push-next`** (pusht `book_state.json` + `book_state_next.json` auf die Box) — gilt für JEDE Änderung an `book_state.json`, nicht nur am Next-Buch.

**Vorfall 21.08.2026** ([[Strategie-Logbuch]] #126): der Momentum-Duplikat-Fix vom 20.08. wurde nie gepusht, die Box rechnete drei Tage lang alle Buch-Marginals (inkl. drei Auto-Promotionen) gegen das alte 7-Bein-Buch.

Der Portfolio-Tab zeigt dann automatisch: Kaufplan (beide Konten mit Frac, Solo-Quote, Median-Dauer), P(funded) rollend über 1/2/3/6/12 Monate, erwartete Eval-Anzahl und Kosten, sowie die Frontier in **beiden** Bust-Modi (EOD-Kopfzahl + ehrliche Intraday-Zahl nach #077).

**Betriebspunkt seit 16.08.2026 = Min-Size** ([[Strategie-Logbuch]] #106): unter der v2-Zielfunktion (Passquote je Eval / $ pro funded) ist die Passquote streng monoton fallend in der Größe, also 1 Kontrakt je Bein, frac ist ausgereizt und **die Kontogröße ist der Sizing-Hebel** (25k schlechtester Käfig, 50k billigster $/funded, 100k/150k höchste Passquote). Der frühere Paar-Betriebspunkt (#089, „P(funded) pro Zeit") gilt nur noch, wenn Max ausdrücklich wieder auf Tempo optimieren will — dann zuerst klären: einzelnes Konto oder Kauf-Rate?

Die Rechenlogik dafür liegt in `eval_plan.py` (gemeinsame Quelle für `funded_finalize.py` und den Analyse-Lauf `frac_pair_budget.py`) — Änderungen an der Passquoten-Mathematik gehören dorthin, nicht in eine Kopie.

## 📗 Next-Week-Buch = Staging (Regel Max, 17.08.2026)

**Neue Strategien, neue Versionen oder Parameter-Änderungen gehen NIE direkt in `book_state.json`**, sondern immer erst ins Staging-Buch **`book_state_next.json`** („Next Week"). Max testet das Buch eine Woche lang (Sim auf der Box + Backtest-Vergleich), optimiert am Wochenende und lässt es dann weiterlaufen.

Ablauf bei jeder Buch-Änderung:

1. Änderung in `book_state_next.json` eintragen (Bein rein/raus, andere Params — gleicher Aufbau wie `book_state.json`, plus Block `next_week` mit `created`, `base_fingerprint`, `changes[]` (date/what/why/ticket) und `note`). Neue Version eines bestehenden Beins bekommt einen **neuen Namen** (z.B. `NQ_LastHour_v3`), damit der Leg-Report frisch erzeugt wird und der Vergleich beide Stände zeigt.
2. `python funded_finalize.py --next` und `python live_finalize.py --next` → schreiben `portfolio_next.json` / `live_portfolio_next.json` + Reports `PORTFOLIO_optimized_next` / `PORTFOLIO_live_next`. Vorher session-guard: zwei parallele Läufe schreiben dieselben JSONs.
3. **Ticket anlegen** in `tasks.json` (Prio gelb, `when` = kommendes Wochenende, `guide` mit Übernehmen/Verwerfen-Schritten) — die Übernahme ins Buch passiert nur über dieses Ticket, nie nebenbei.
4. Portfolio-Tab im Lab: oben Umschalter **📘 Aktuelles Buch / 📗 Next Week / ⚖️ Vergleich**; Eval/Funded/Live gibt es in beiden Büchern. Der Vergleich stellt v2-Passquote je Tier, $/funded, Median, Frontier am Betriebspunkt, Trades/Jahr, Korrelation, RoDD, Sharpe, Beine (in beiden / nur Next / raus) und das Live-Buch nebeneinander, mit Delta und Rausch-Einordnung (≥ 1,5 pp und 2× Seed-Streuung, sonst „neutral").
5. **Übernehmen** (Wochenende, Ticket): `book_state_next.json` → `book_state.json` (Backup vorher), dann `funded_finalize.py` + `live_finalize.py` ohne `--next`, NT8-Deploy, dann `next_week`-Block auf das neue Buch zurücksetzen. **Verwerfen:** `book_state_next.json` wieder auf den Stand von `book_state.json` bringen. Ticket danach löschen.

Der Developer-Tab ([[Strategy Developer]]) bleibt der Ort, wo eine Strategie in Versionen entsteht; „ins Buch" heißt seit 17.08. „ins Next-Week-Buch + Ticket".

## 🚀 Live-Buch (seit 11.08.2026)

Regel Max: nichts von dem, was je eine Edge zeigte, soll verloren gehen, nur weil es nicht ins Prop-Buch passt. Portfolio-Tab hat 3 Unter-Reiter: 🎓 Eval / 💰 Funded (beide identisch, `portfolio.json`) / 🚀 Live (`live_portfolio.json`).

- `python live_finalize.py` (Engine-Ordner) = Buch-Beine aus `book_state.json` **plus** die per Hand kuratierten Grade-A-„Bank"-Funde in `LIVE_EXTRA` (Strategien mit robuster OOS-Bestätigung, die der Auto-Fit nur mangels Portfolio-Beitrag/Frequenz fürs Prop-Buch abgelehnt hat — kein Prop-Firma-Limit mehr, also kein Ausschlussgrund).
- Neuer Grade-A-Bank-Fund? → in `LIVE_EXTRA` in `live_finalize.py` eintragen (Params, Familie, Why mit Logbuch-Bezug), dann `python live_finalize.py` laufen lassen. Grade-C/D-Funde bewusst NICHT aufnehmen (ehrliches Backtesting: schwache Qualität bleibt schwach, auch live).
- **Falle, auf die schon einmal reingefallen:** ein alter Report kann durch spätere Engine-Fixes überholt sein, ohne dass `ideas.json` es merkt (bei RV_leadlag_NQES so passiert — Report vom 31.07. zeigte Grade A, mit dem seit 10.08. gefixten `rv.py` neu gerechnet PF 0.91/tot). `live_finalize.py` rechnet jedes Bein bei jedem Lauf frisch mit dem aktuellen Engine-Code — bei Abweichung vom alten Report-Stand zählt die frische Rechnung, nicht das `.meta.json`.
- Kein Prop-Pass-Frontier und keine Kapital-/Sizing-Kurve im Live-Tab (Kapitalgröße & Risiko/Trade noch nicht festgelegt) — nur die ehrliche kombinierte Backtest-Sicht.

## 🧬 Edge-Health-Monitor (Regel Max, 01.09.2026)

Der Decay-Monitor unten im Lab-Tab (🧬 Edge-Health, Live-Trades je Bein gegen den Backtest-Erwartungs-Kegel, McLean/Pontiff + Lopez de Prado) baut seine Referenz (`edge_ref.json`) seit 01.09.2026 **automatisch neu**, sobald `book_state.json` neuer ist als `edge_ref.json` (Mtime-Check in `_edge_health()`, `app_server.py`) — kein manueller Lauf von `gen_edge_ref.py` mehr nötig. Die Zuordnung NinjaScript-Name → Bein läuft über Familien-Präfix (Endung `_d<Datum>`/`_v<N>` wird abgeschnitten), damit ein Discovery-Auto-Promote oder eine neue Developer-Version desselben Mechanismus (neuer Bein-Name, gleiche Familie) automatisch mitgezogen wird. Seit 01.09.2026 nur noch **das aktuell aktive Konto** (per letztem Fill ermittelt), nicht mehr alle historischen Konten vermischt.

**Ein Fall bleibt manuell:** eine WIRKLICH neue Strategie-Familie (neue NinjaScript-Klasse, die noch nie im Buch war) braucht einmalig einen neuen Eintrag in `NS_MAP` (`gen_edge_ref.py`, NinjaScript-Klassenname → Bein-Familie-Präfix) — die Klasse kennt sonst niemand vorab. Bei jedem neuen NT8-Deploy einer neuen Strategie also kurz `NS_MAP` in `gen_edge_ref.py` ergänzen, danach läuft der Rest wieder automatisch. Vorfall, der zum Fix führte: `NQ_VWAP-Pullback` fehlte komplett in der alten, hartkodierten Zuordnung und wurde vom Decay-Monitor gar nicht erfasst.
