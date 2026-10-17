---
tags:
  - projekt
  - trading/backtest
status: einsatzbereit
erstellt: 2026-07-06
ort: C:\Users\maxlk\Projects\trading-data
---
# ⚙️ Lokale Backtest-Engine + Daten

⬅️ [[_Projekte]] · verwandt: [[Day Trading]], [[Strategie-Logbuch]]

> [!success] Status: einsatzbereit & validiert (06.07.2026)
> Lokale, ehrliche Intraday-Backtest-Engine. Testet Strategien **gratis** (kein QuantPad-Token), reproduziert QuantPads Ergebnis unabhängig und ist sogar ehrlicher (echte Fills in beide Richtungen).

## Wozu
QuantPad kostet Tokens pro Test. Ziel: hunderte Strategien testen, ~90% wegwerfen. Deshalb: Daten **einmal** aus QuantPad exportiert, danach alles lokal.

## 📦 Exportierte Daten (`exported_data/`)
1-Minuten-Bars, volle Session (RTH + Overnight), UTC, OHLCV. Geprüft: lückenlos, 0 OHLC-Fehler, 0 NaN, Volumen komplett.

| Instrument | Zeilen (1m) | Zeitraum |
|---|---|---|
| NQ | 3.669.335 | 2016-01 → 2026-07 |
| ES | 3.681.813 | 2016-01 → 2026-07 |
| YM | 3.649.650 | 2016-01 → 2026-07 |
| RTY | 2.936.649 | 2017-07 → 2026-07 |

Dazu Tages-Bars (nur Benchmark; ES/RTY haben Ratio-Adjust-Artefakte, unkritisch).
**Noch nicht exportiert (bei Bedarf):** 1-Sekunden-Bars, Tick, L2 (siehe `probe_quantpad_data.py`).

## 🧠 Engine (`engine/qbt.py`)
Instrument-agnostisch, wiederverwendbar. Kann:
- **Ehrliche Fills:** kein Look-ahead (Entry auf nächster Bar-Open), Stop-before-Target, echte Touch-Logik.
- **Kosten** (Slippage + Kommission), brutto UND netto.
- **MAE** pro Trade (auch Gewinner) → echtes Intraday-Risiko.
- **Volle Metriken:** Win-Rate, Expectancy, PF, Sharpe, MaxDD, Streaks, Trades/Woche.
- **Baseline-Check:** Random-Walk-Win-Rate = Stop/(Stop+Target) = Breakeven. Strategie muss die schlagen.
- **Monte Carlo** (Block-Bootstrap): Terminal, MaxDD, P(Verlust).
- **Prop-Pass-Wahrscheinlichkeit** (Topstep/Apex) mit Trailing-DD über die MAE (intraday, nicht nur Trade-Schluss).
- Modi: `reversion` und `continuation`, VWAP-Z-Score-Signal, optionaler Regime-Filter (Efficiency Ratio).

## ▶️ Nutzung
```bash
cd C:\Users\maxlk\Projects\trading-data\engine
python run_vwap.py            # Self-Validation + Demo
```
Neue Strategie: `qbt.run_strategy({...params...})` → `qbt.metrics(tr)` → `qbt.monte_carlo(tr)` → `qbt.prop_pass_probability(tr)`.
Erster Lauf baut RTH-Cache (`exported_data/cache/`), danach schnell.

## 🛑 Rechen-Bremse: Multiprocessing nur noch darüber (16.10.2026)
Anlass: der PC hat nur 6 Threads. Zwei Sessions mit je eigenem Pool (5 plus 4 Worker, alle auf normaler Priorität) legten ihn lahm. `engine/rechen_bremse.py` löst das PC-weit:
- **BELOW_NORMAL** für Hauptprozess und Worker, damit Maus, Browser und Claude bedienbar bleiben.
- **Obergrenze 4 gleichzeitig rechnende Prozesse über alle Sessions zusammen** (`MAXLAB_MAX_WORKER` ändert sie, in allen Sessions gleich setzen). Geteilt wird über 4 Sperrdateien in `%LOCALAPPDATA%\MaxLab\rechen_bremse\`, je Aufgabe ein Slot, wartende Läufe bekommen nach jeder Freigabe Vortritt. Stirbt ein Lauf, gibt Windows den Slot selbst frei, und seine Worker beenden sich mit (Eltern-Wächter). Findet ein Lauf 5 Minuten keinen Slot, rechnet er eine Aufgabe ohne weiter, hängen bleibt nie etwas.
- **Aus** auf der Box, auf Nicht-Windows und mit `MAXLAB_BREMSE=0`. `python rechen_bremse.py --status` zeigt, wer gerade rechnet. Test: `python test_rechen_bremse.py` (32 Prüfungen, rund 1 Minute).

Eingebaut in `weekend_check.py` (`--jobs`, `run_jobs`), `konten/account_card.py` und `test_erstfassung.py`. **Für jedes neue Scratch-Skript mit mehreren Prozessen:**
```python
import sys; sys.path.insert(0, r"C:\Users\maxlk\Projects\trading-data\engine")
import rechen_bremse as RB
ergebnisse = RB.pool_map(meine_funktion, aufgaben, wunsch=4)              # Liste, Eingabe-Reihenfolge
for r in RB.pool_imap_unordered(meine_funktion, aufgaben, wunsch=4): ...  # Fertig-Reihenfolge
with RB.slot(): grosse_einzelrechnung()                                   # ein einzelner Prozess
```
`meine_funktion` muss auf Modulebene stehen (Spawn). Kein eigenes `mp.Pool(cpu_count()-1)` mehr. Wer unbedingt einen eigenen Pool braucht: `mp.Pool(RB.worker_zahl(5), initializer=RB.senke_prioritaet)`, das deckelt Zahl und Priorität, teilt aber keine Slots. Die Zahlen hängen nicht von Worker-Anzahl oder Priorität ab (jede Aufgabe hat ihren eigenen Seed).

**Fallen:**
- Ein gebremster Lauf kriecht, solange daneben noch ein ungebremstes Skript die CPU voll auslastet (Kinder erben die niedrige Priorität, auch ihr Start dauert dann). Gewollt, aber wer einen kurzen Test mit Zeitmessung braucht, setzt `MAXLAB_BREMSE_PRIO=0` (Slots und Obergrenze bleiben). Ein Skript mit eigenem `mp.Pool(cpu_count()-1)` ohne Bremse bringt die ganze Rechnung ins Leere.
- Die Bremse zieht nur, wo das Skript sie benutzt. Seit 18.10.2026 (AP411, Max): Regel in der CLAUDE.md, ein Hook weist bei `Pool(` ohne `rechen_bremse` darauf hin (Bash-Start und Schreiben eines Engine-Skripts, nur Hinweis, einmal je Datei; abschalten pro Datei mit dem Kommentar `# rechen_bremse: nicht noetig`), und `rechen_bremse.py` steht in `ENGINE_CORE` (Regressionstest vor dem Box-Sync).
- Wird ein Lauf abgebrochen (Fehler, Strg+C), kann eine harmlose Meldung `OSError: handle is closed` aus dem Aufgaben-Puffer erscheinen. Das ist kein Fehler im Ergebnis.
- `konten/account_card.py` gehört zum Karten-Fingerabdruck: die Konto-Karten gelten seit dem 16.10. als veraltet und werden beim nächsten Lauf neu ausgegeben (Simulation kommt aus dem Cache, Zahlen unverändert, nur Datum und Fingerabdruck neu).

## ✅ Validierungs-Ergebnis
- Baseline (60%) = exakt Breakeven für Stop 1,5 / Target 1,0 → Engine-Mathe konsistent.
- Reversion 56% netto (unter Baseline) → keine Edge = reproduziert QuantPad.
- Continuation brutto nur +0,1% über Baseline → **Rauschen, keine echte Edge** (ehrlicher als QuantPads +170k-Mirror mit optimistischen Fills).
- **Fazit: nacktes VWAP-Z-Stretch-Signal hat in keiner Richtung Edge.**

## 🧪 Quant Co-Pilot (lokaler QuantPad-Nachbau)
Nach dem QuantPad-Video (Thomas Skinner) die zweite Säule lokal nachgebaut: die **Strategie-Validierungs-Pipeline** als dunkles Dashboard im Browser. `engine/copilot.py` + `engine/report.py`.

**Start:** `python run_copilot.py` → generiert HTML in `engine/reports/` und öffnet den Browser.

**Zeigt (wie QuantPad):**
- **Verdict** als Buchstaben-Note A-F mit Score + Begründung
- KPI-Kacheln: Win-Rate vs Breakeven-Baseline, Expectancy, PF, Sharpe, Trades, MaxDD, Gesamt-P&L, MC P(Verlust)
- Equity-Kurve (netto, pro Micro)
- **Regime-Analyse**: Performance nach Trend (Efficiency Ratio), Volatilität, Tageszeit
- **🏦 Prop Firm Assistant** (Herzstück): strukturiertes Monte Carlo über Challenge + Funded-Phase (Trailing DD via intraday MAE, Withdrawals, Profit Split). Pro Kontraktgröße: **P(pass), Ø Tage bis Pass, P(payout), Ø Tage bis 1. Payout, EV pro Account.**

Nimmt Trade-Logs aus der Engine. *(v2: beliebige CSV / Live-Trade-Logs ingesten, wie QuantPads Co-Pilot.)*

## 🖥️ Strategy Lab (Desktop-App)
Persistentes App-Fenster für den zweiten Monitor. Start: **`Strategy Lab.bat`** (oder `python app.py`). Öffnet ein natives App-Fenster (Edge/Chrome App-Modus, kein Browser-Tab), frei verschiebbar.
- **Seitenleiste** listet alle validierten Strategien mit Note-Badge, Win-Rate, P(pass), Datum.
- **Live-Update:** pollt alle 4s → sobald Claude einen neuen Report generiert (`run_copilot`/`validate`), erscheint er automatisch, ohne Neustart.
- Auswahl zeigt den vollen Report rechts.
- Server `app_server.py` (Port 8756), reine Standard-Library.
- **Workflow:** App offen lassen. Ich teste Strategien lokal → neue Reports poppen in deiner App auf.

**Was NICHT nachgebaut (bewusst):** QuantPads AI-Agent (= das bin ich + die lokale Engine), die Cloud-All-you-can-eat-Daten (= einmal exportiert), die Community. Die wertvolle Säule für Prop haben wir.

### 🎨 Design-Sprache: Institutional Terminal (30.07.2026)
Umbau weg vom „KI-Look" (Emojis, bunte runde Kästchen) hin zu einem Bloomberg-/Refinitiv-artigen Terminal. Recherche-Prinzip: *jeder Pixel muss sich rechtfertigen, Hierarchie durch Wichtigkeit statt Deko*.
- **Emojis komplett raus** aus Reports (`report.py`) + Shell (`app_server.py`) → Uppercase-„Eyebrow"-Labels mit Haarlinie.
- **De-Box:** flache Panels + Haarlinien statt schwebender runder Kästen (Radius 14px → 4px), KPI-Zellen durch 1px-Linien getrennt statt gapped Cards.
- **Monospace-Tabellenziffern** (`tabular-nums`) überall bei Zahlen — der eigentliche Pro-Look.
- **Zurückhaltende Palette:** ein Amber-Akzent (`#c79a3f`) + Grün/Rot nur für Vorzeichen, statt Regenbogen. Tokens in `:root` von report + shell synchron.
- **Charts prominenter:** Equity 580px, volle Breite über die ganze Historie, Flächenverlauf, feine Gridlines, Mono-Achsen. Aktive Tabs: dezenter Akzent-Unterstrich statt grellblauer Block.
- Design-Tokens sind zentral in `:root` — Farbe/Radius global änderbar.

### 🎫 Tickets: Reihenfolge & Abläufe (09.08.2026)
Tickets hängen jetzt zusammen. Datenmodell: `blocked_by` als Liste von Ticket-IDs in `tasks.json`, sonst nichts. Schritt-Nummern werden **nicht** gepflegt, sondern berechnet (längster Pfad = Tiefe, Ketten = zusammenhängende Gruppen).
- **Fang hiermit an:** genau EIN Ticket oben, aus nicht-blockiert + Zeitfenster offen + Prio + Unblock-Hebel, mit Begründung.
- **Reihenfolge (1..n):** topologisch korrekt (nie vor dem eigenen Blocker), blockierte eingerückt.
- **Abläufe:** Kette als Zeitstrahl mit Schritt 1..n, erledigt durchgestrichen, aktueller Schritt „JETZT DRAN". Erledigte Ketten fliegen raus.
- **Verknüpfen:** Ticket aufklappen → REIHENFOLGE → „+ wartet auf …". API `/api/tasks/setdeps`, Zyklen werden serverseitig abgelehnt.
- Gebaut + im Headless-Chrome gegen echte Daten verifiziert (42 Tickets, 2 Ketten). Backup: `app_server.py.bak-20260809-deps`.

![[tickets-reihenfolge.png]]

### 🧩 Portfolio-Tab: Quelle der Wahrheit + 404-Fix (10.08.2026)
Klick auf ein Bein landete im rohen `Error code: 404 / Message: Not Found` statt im Report. Zwei Ursachen, beide behoben:
- **Daten:** `portfolio_tab.py` (Stand Juli, eigene eingefrorene Bein-Liste, schreibt kein `report`-Feld pro Bein) hatte die gute `portfolio.json` überschrieben → die Beine hießen „Momentum NQ" statt `NQ_Momentum`, dazu passte keine Datei in `reports/`. Jetzt gebaut aus **`book_state.json` via `funded_finalize.py`** (legt fehlende Bein-Reports selbst an). `portfolio_tab.py` ist deprecated: läuft nur mit `--force` und fasst `portfolio.json` nicht mehr an.
- **Server/UI:** `/reports/...` dekodiert jetzt `%20` (Namen mit Leerzeichen liefen immer ins Leere). Fehlt ein Report wirklich, kommt statt des http.server-404 eine Seite im Lab-Look mit den nächstliegenden Reports zum Anklicken. Zusätzlich löst die UI Anzeige-Namen per Token-Match auf echte Report-Namen auf („Momentum NQ" → `NQ_Momentum`), auch beim ⤢-Popout.
- **Nebenbefund:** ein verwaister `app_server.py` aus einem alten Lauf hing noch auf Port 8756 und beantwortete die Requests mit altem Code, obwohl der Supervisor längst neu gestartet hatte. Bei „Änderung wirkt nicht": `netstat -ano | findstr 8756` prüfen, Zombie killen.

**Regel ab jetzt:** jede Buch-Änderung → sofort `python funded_finalize.py`, damit der Tab nie ein altes Buch zeigt.

## 📐 MFE/MAE in jedem Trade-Record (seit 03.09.2026)
Jeder Trade-Record trägt neben `mae_r` jetzt auch **`mfe_r`** (Maximum Favorable Excursion in R), erzeugt in `qbt._mfe_r` (alle 8 qbt-Loops), `sigcore.simulate_trade`, `vwap_pullback.py`, `asian.py`, `rv.py`. Rein deskriptiv, fließt nirgends in Exit, Gates oder Sizing zurück. Zwei Vorbehalte beim Auswerten ([[Strategie-Logbuch]] #142): bei `stop`- und `time`-Exits zählt die Exit-Bar nicht (Untergrenze), bei `target`-Exits ist der Wert per Konstruktion ≈ Ziel (zensiert), `rv.py` misst auf Close-PnL statt intrabar. Sweeney-/E-Ratio-Tabellen deshalb nur über `eod`/`time`-Exits bilden und nie Trail-Trigger aus einer MFE-Verteilung über ein Grid ableiten. `vwap_pullback.py` kennt seit demselben Tag das opt-in BE/Trailing-Overlay (`be_trigger`/`trail_trigger`, Default aus, bitgleich).

## Nächste Schritte
- [ ] Regime-Filter + Selektivität testen (weniger, bessere Trades statt 261/Woche)
- [ ] Andere Signale aus [[Mean-Reversion Paper (High-Winrate Fokus)]] durchjagen
- [ ] Co-Pilot v2: externe/Live-Trade-Logs (CSV) ingesten
- [ ] Bei Bedarf 1s-Daten für ehrlichere Fills + Volume Profile
