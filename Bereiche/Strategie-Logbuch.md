---
tags:
  - bereich/trading
  - trading/logbuch
erstellt: 2026-07-05
---
# 📓 Strategie-Logbuch

⬅️ [[Day Trading]]

> [!info] Zweck
> Vollständiges Logbuch **jeder** getesteten Strategie. Erwartung: hunderte Tests, ~90% landen im Müll. Damit nichts verloren geht und Max jederzeit sieht, was schon geprüft wurde und warum. Jede neue Strategie kommt hier als Eintrag rein.

## Format je Eintrag
Datum · Strategie · Instrument · Quelle · Verdict · Kernzahlen · Warum · Dateien

---

> [!tip] 📦 Einträge **#001–#025** (04.07.–15.07.) ausgelagert → [[Strategie-Logbuch Archiv (001-025)]]. Insight-Bank + Eval-Portfolio unten bleiben vollständig.


## #026 — Per-Asset Discovery-Batch + Funded-Portfolio (15.07.2026)
- **Aufgabe (Max):** vollständiger Overnight-Batch — pro Asset (NQ/ES/RTY/YM) je 3 research-basierte Mechaniken tunen, ehrlicher OOS-Forward-Test, Nicht-Robuste killen, Überlebende zu einem Funded-Portfolio bauen. Scripts: `asset_discovery.py` (+ `instrument_tune.py`, `alpapolio.py`).
- **Discovery (12 Versuche → 5 Überlebende):** NQ = Momentum + ORB-Breakout + **LastHour** (neu, 188/yr) · ES = nur Momentum (schwach, OOS +1,0%) · RTY = **Gap-fade** (Reversion, OOS +5,8%) · **YM = nichts robust** (Edge kippt IS↔OOS → ehrlich gekillt).
- **Funded-Portfolio `PORTFOLIO_optimized`:** `NQ_Momentum + NQ_LastHour + NQ_ORB-Breakout + RTY_Gap-fade`. Note C · **362 Trades/Jahr** · |Korr| 0,09 · PF 1,17 · **RoDD 7,69** · Sharpe 1,03. Frontier: frac 0,22 → **50% / ~44 Tage**, frac 0,30 → 46% / ~22 Tage.
- **Besser als altes NQ-only-Buch** (205/yr, RoDD 6,2): mehr Frequenz (LastHour) + echte Instrument-Diversität (RTY-Sleeve).
- **Bestätigtes Prinzip:** Cross-Instrument-Diversifikation nur mit **anderer Mechanik/Familie** (gleiche Familie über Instrumente korreliert, weil Index-Futures ~0,9 co-bewegen). RTY-Gap-fade half, weil es Reversion ist; ES-Momentum half nicht (korreliert mit NQ-Momentum).
- 5 neue Einzelreports im Lab. **Lab neu starten** für aktuelle Ansicht.

## #027 — Strategy Lab als Desktop-App mit Auto-Update (21.07.2026)
- **`lab_app.py`** (pywebview/Edge WebView2): natives Fenster, startet den Server automatisch als Subprozess, Fenster zu = Server aus.
- **Hot-Reload-Kette:** Code-Änderung an `app_server.py` → Supervisor startet Server neu → `/api/version` ändert sich → Hub lädt sich selbst neu. **Nie wieder manuell neustarten oder Ctrl+F5.** Reports/Portfolio/Ideas waren schon live (4s-Polling).
- **Desktop-Verknüpfung "Strategy Lab"** (pythonw, kein Konsolenfenster). Doppelklick = alles läuft.
- Wichtig: alte manuell gestartete `python app_server.py`-Terminals schließen (App erkennt Doppelstart und verweigert). Es liefen sogar 2 alte Server parallel auf 8756 (Windows SO_REUSEADDR) — beendet.

## #028 — Asian-Range-Discovery: 10 Strategien, 2 Überlebende, 1 Juwel (21.07.2026)
- **Neues Modul `asian.py`:** Session-Range-Framework auf vollen 24h-Globex-Daten (2016-2026, alle 4 Instrumente). Research-Basis: 10 Quellen (Boyarchenko RFS 2023, NY-Fed-Update 2026, Lou/Polk/Skouras JFE 2019, Gao et al. 2018, Zarattini ORB, u.a.).
- **⚠️ Fill-Bug gefunden & gefixt (wichtige Lektion):** Stop-Entry am Range-Level füllte beim Overnight-Gap zum LEVEL statt zum (schlechteren) OPEN → Traumzahlen (PF 2,49) waren Fantasie. Nach ehrlichem Fix: PF 1,08. **Regel: Stop-Orders füllen bei Gap am Open, nie am Level.** Kompletter Rerun.
- **8/10 ehrlich getötet:** London-Breakout (alle Varianten inkl. NR-Filter + London-IB, 46 Configs!), Overnight-Drift 2-3h (bestätigt tot, wie NY-Fed 2026 sagt), Asia-Fade (NQ+RTY), ES-Break. **Die klassische Asian-Range-London-Lore hält auf Index-Futures nicht.**
- **💎 Überlebender #1: `NQ_Asia-Dir-USopen` — VERDICT A (Score 100).** Klare Asien-Richtung (≥0,8× Range) → am US-Open mit ihr, EOD-Exit. Nur 25 Trades/Jahr, aber OOS-Edge +10,1%, PF 1,35, expR +0,22. Solo auf Static-EOD: **72% P(pass)**. → **Als 6. Bein ins Buch:** |Korr| sinkt auf 0,07, Frontier verbessert auf **65%/~42d (frac 0.18) bzw. 61%/~30d (0.22)**.
- Überlebender #2: `NQ_Asia-Break-USsession` (robust aber dünn, PF 1,07) → Bank, nicht Buch.

## #029 — Lucid-Umbau + Konogrößen-Analyse (04.08.2026)
- **Firmen-Entscheid: Lucid Flex** (statt MFFU): gleiche Eval-Mathe, aber Einmalgebühr, Voll-Automation offiziell erlaubt, Funded EOD ohne Consistency. Lucid als Firma in `copilot.PROP_FIRMS`, Portfolio-Tab + alle Reports auf Lucid regeneriert.
- **Buch-Recheck unter Lucid-Regeln** (`lucid_opt.py`): alle 4 Bank-Kandidaten (ES-Mom, Asia-Break-US, Gap-cont, Overnight) verschlechtern das 6-Bein-Buch → **Buch bleibt unverändert.** Wieder: Qualität > Quantität.
- **Ehrliche Physik:** DD $2.000 statt $2.500 = ~8 Punkte weniger. **Decke 58%** (frac ≤0.12), >60% pro Einzelversuch unerreichbar.
- **Konogrößen-Fund:** 25k = Speed-Konto (50%/~27d, Min-Size-Effekt macht Sizing-Knopf wirkungslos) · 50k = Pass-König (58%) · 100k = schlechter (Ratio). **Empfehlung: 2× 25k parallel → ≥1 Pass ≈ 75% in ~4-6 Wochen (~$190).** Kumulativ schlägt einzeln.

## #030 — Auto-Fit-Pipeline (04.08.2026)
- **Neue Automatik:** Jede neu validierte Strategie, die das Prop-Valide-Gate besteht (Edge>0, Net>0, P(pass)≥40%), wird **automatisch gegen das Buch getestet** (Lucid-Regeln, `auto_fit.py`). Verbessert sie den Betriebspunkt (+2 Punkte Pass oder ≥15% schneller bei gleichem Pass) → **automatische Aufnahme** ins Buch (`book_state.json` = Single Source of Truth) + Portfolio-Report-Neubau. Sonst: Ablehnung mit Begründung ins `fit_log.json` (kein Doppeltest).
- Massen-Regens lösen den Auto-Fit nicht aus (MAXLAB_AUTOFIT=0 in allen regen_*-Skripten).
- **End-to-End-Test bestanden:** NQ_Asia-Break-USsession bestand das Gate, wurde vom Fit-Test korrekt ABGELEHNT (Buch 57%/103d → mit ihr 48%/54d = Verwässerung erkannt).

## #031 — ORB-Qualitätsfilter: RVOL bestätigt, ATR-Expansion getötet (04.08.2026)
- **Max' Hypothesen getestet** (`orb_atr_rvol_study.py`, neue opt-in Filter `rvol_min`/`atr_exp_min` in qbt):
- **RVOL ≥ 1,2 = echter Filter ✅:** macht den rohen, negativen ORB (−0,7%) robust profitabel (+1,9%, **OOS +2,2%**, PF 1,08, 49/yr). RVOL = kumuliertes Volumen bis zur Breakout-Minute vs. 20-Tage-Schnitt derselben Minute (kein Look-Ahead). Aufs Buch-ORB redundant (hat schon Breakout-Vol-Filter).
- **ATR-Expansion (ATR5/ATR20) = Overfit-Falle ❌:** In-Sample teils +2,5%, **OOS ALLE negativ** (bis −9,6%). Lehrbuchbeispiel, warum OOS-Pflicht gilt. RVOL ≥ 1,5 ebenfalls zu streng (kollabiert).
- **Param-Opt Stufe 2:** bester robuster Fund = Buch-ORB-Variante `stop 0.3 / kein Target / EOD` → **VERDICT B (70)**, expR +0,34, Report `NQ_ORB_ATR-RVOL`.
- **Auto-Fit-Pipeline lief automatisch:** Buch 57%/103d vs. mit neuem Bein 58%/96d → knapp unter Aufnahme-Schwelle (+2 Punkte) → korrekt abgelehnt, liegt auf der Bank (Prop-Valide).

## #032 — Käfig-Scan + Sizing-Policy-Suche (04.08.2026)
- **Käfig-Scan (Hebel #1): BULENOX 50k EOD ist der Gewinner.** $2.500 EOD-Trailing (statt $2.000 bei Lucid/MFFU) bei gleichem $3.000-Target = **+7 Punkte auf jeder Geschwindigkeit**: 63%/96d (frac 0.14) · 66%/117d (0.10) · 59%/61d (0.18). Algo/Copier erlaubt, NT/Tradovate, ~$19-40/Mon. mit Dauercodes, Reset $78, Funded 100% der ersten $10k + wöchentliche Payouts. ETF-Static (T$4000/DD$2000 static, 62%/93d) knapp dahinter, aber Algo nur mit schriftlicher Genehmigung → raus. **Vor Kauf prüfen: Eval-Consistency, Renewal, Algo-AGB.**
- **Sizing-Policy-Suche (Hebel #2): ehrliches Null-Ergebnis.** 60+ Policies getestet (Progress-Taper, Konvexität, Signal-Tag-Boost, Verlust-Throttle) mit Train/Test-Split auf den Handelstagen: **KEINE schlägt das simple Cushion-Sizing robust.** Simplex gewinnt wieder — die naive Kelly-Approximation ist schon nahe am Optimum. Erspart uns fragile Steuerungs-Komplexität im Risk-Guard.
- **Netto-Ergebnis beider Fronten: 56% → 63-66%** — komplett durch die Firmenwahl. Max' 60%+-Wunsch erfüllt.

## #033 — RELATIVE VALUE: Die 5. Familie ist besetzt! (04.08.2026)
- **Research-Basis:** Gatev/Goetzmann/Rouwenhorst (RFS 2006), Krauss-Survey (2017), Avellaneda/Lee (2010), Göncü/OU-Modelle, Lead-Lag-Literatur (Kawaller/Chan), NQ/ES-Praxis (~93% Korrelation). Neues Modul `rv.py` (mode="rv", 5 Edge-Familien, doppelte Kosten korrekt).
- **~90 Configs getestet** (`rv_discovery.py`): div_fade (4 Pairs) · div_mom · leadlag · gap_div · eod_conv.
- **💎 FUND: `RV_leadlag_NQES` — VERDICT A (87).** NQ bewegt sich in den ersten 30 Min ≥0,2%, ES hinkt (<0,3× des Moves) → ES folgt dem Leader. **Edge +6,6%, OOS +9,4%, PF 1,37, expR +0,24** — robustes Plateau übers ganze Grid (8/8 leadlag-NQES-Configs überleben!). Informations-Diffusion, kein Zufalls-Fit.
- **Auto-Fit hat es SELBSTSTÄNDIG ins Buch aufgenommen** (erster automatischer Neuzugang!). **7-Bein-Buch auf Bulenox: 66%/~93d (frac 0.10-0.12) · 65%/93d (0.14) · 60%/~55d (0.18) · 56%/43d (0.22).**
- **Ehrliche Kills:** div_fade in ALLEN 48 Varianten tot (doppelte Kosten fressen die engen Spreads — klassisches Retail-Problem bei Pairs) · eod_conv tot · div_mom nur marginal (Bank) · leadlag NQ→RTY zu schwach (Bank) · **gap_div = Bug** (Division durch Mini-Risiko wenn Gap bis Entry konvergiert; Report gelöscht, Modul-Fix ausstehend).
- Multi-Day-Kointegrations-Pairs: für [[Live-Account]] notiert (Prop = intraday only).

## #034 — Kalender-Effekte: 51 Configs, viel Friedhof, 1 Bank-Fund (04.08.2026)
- **Setup:** Neues Modul `calendar_fx.py` (mode="cal"): ToM, Pre-Holiday, OpEx-Fade, Quartalsende, Pre-/Post-FOMC (echte Fed-Termine 2021-2026 von federalreserve.gov). Klein-N-Modi mit Skepsis-Aufschlag (Edge-Hürde 3% statt 1%).
- **✅ Bank-Fund: `CAL_fomcpost_ES` (FOMC-Announcement-Momentum):** 14:15 mit der ersten Statement-Reaktion bis Close → Edge +13,3%, OOS +39%, PF 1,71. ABER nur 43 Trades/8 pro Jahr → Klein-N-Vorbehalt, Auto-Fit korrekt abgelehnt (Buch-Beitrag zu klein). Liegt auf der Bank/Prop-Valide.
- **👀 Watchlist-Muster: Turn-of-Month.** IS (2016-22) flach, **OOS (ab 2023) klar positiv (+8-9% auf NQ/ES)** — der McConnell/Xu-Effekt scheint wiederbelebt, besteht aber das IS+OOS-Protokoll (noch) nicht. In 6-12 Monaten neu testen (Backlog).
- **Ehrliche Kills:** OpEx-Fade (−22%! Vormittag setzt sich fort statt zu faden) · Quartalsende beide Richtungen · **Pre-FOMC-Drift (Lucca/Moench) im modernen Sample tot** (2021+ negativ — konsistent mit Post-Publikations-Verfall) · Pre-Holiday (zu wenig Trades/kein Effekt).
- Nebenbei bestätigt: Auto-Fit läuft jetzt auf Bulenox-Käfig, **7-Bein-Buch dort 66%/~95d**.

## #035 — Live-Monitor im Lab (24.07.2026… äh 04.08., dritter Top-Tab) 
- **📡 Live-Tab** neben Strategy Lab + Idea Engine: Performance-Karten pro Algo (P&L heute/gesamt, Trades, Win%), Gesamt-Karte, klickbare Trade-Liste, **Trade-Detail mit Mini-Chart** (Entry/Exit-Marker auf 1m-Bars).
- Datenquelle: `engine\live\*executions*.csv` + `bars_<INSTR>.csv` — genau das Format, das der NinjaScript-Logger schreibt (kommt mit dem Port). Aktualisiert alle 4s übers bestehende Polling.
- **Demo-Daten liegen drin** (Konto "DEMO"), damit das UI sofort sichtbar ist → löschen, sobald echte Logs fließen (`engine\live\demo_executions.csv` + `bars_*.csv`).
- Zweck: primäres Werkzeug der **Sim-Phase** (Sim-vs-Backtest-Tracking) und danach Live-Aufsicht.

## #036 — ORB Long/Short-Split geprüft (Max' Sell-Side-Frage) (04.08.2026)
- **Behauptung ("ORB-Short macht Minus"):** echter Effekt (Index-Long-Drift), aber bei uns nur teilweise. `orb_side_check.py`:
  - **NQ_ORB-Breakout:** Long +0,136 vs Short +0,019 expR — Short deutlich schwächer, aber noch profitabel (+989$/µ). Long-Bias bestätigt, dank Trend-Filter bleibt Short im Plus.
  - **NQ_ORB-Fade+NR7:** Short (+0,113) > Long (+0,006). Reversion, umgekehrte Logik.
  - **NQ_ORB_RVOL:** Short (+0,535) >> Long. ES-ORB: Long −0,543 (Müll), Short +0,098.
- **Entscheidung: nichts abschalten.** Short ist überall netto positiv und feuert an roten Tagen (Diversifikation, trägt Portfolio-Sharpe 1,0). Kappen würde Equity-Glättung kosten. Regel "no shorts" verdient sich OOS nicht → raus. NinjaScript-ORBs bleiben beidseitig (= Backtest).

## #037 — 📓 Trade-Journal im Lab (26.07.2026, vierter Top-Tab)
- **Research-Basis:** TradeZella/Edgewonk/Tradervue-Patterns (Kalender-P&L, Review-Kadenz, Prop-Dashboard, Strategie-Attribution) + **Locke & Mann (JFE 2005)** "Professional trader discipline and trade disposition" (Disposition-Effekt via Haltezeiten messbar) + Barber/Odean (Trader-Lernen).
- **Gebaut (Lucid-Look):** Trading Growth Curve (Balance vs. Target-/MLL-Linien) · 3 Objective-Karten mit Fortschrittsbalken (Profit-Ziel, Max-Loss-Puffer, Consistency ≤50%) · Statistik-Zeile (P&L, Win%, PF, Expectancy, RRR, Ø Win/Loss, Best/Worst, Kontrakte) · **TradeZella-Kalender** (Monatsraster mit Tages-P&L-Zellen + Wochen-Summen, Monats-Navigation) · Konto-Filter (Sim101 / später BX-Eval).
- **Alleinstellungs-Feature: 🧠 Disziplin-Check nach Locke/Mann** — Ø Haltezeit Gewinner vs. Verlierer; Alarm, wenn Verlierer >1,3× länger gehalten werden (Disposition-Muster → bei Algos = Stop sitzt falsch). Plus Strategie-Attributions-Tabelle (N, Win%, P&L, Hold W/L je Bein).
- Datenquelle: dieselben Live-Fills (Auto-Sync vom VPS alle 2 Min). Ab Montag füllt sich alles von selbst.

## #038 — RTY_Gap-fade: Ablation + Retune statt Rauswurf (27.07.2026)
- **Max' Verdacht** ("hässlichstes Bein, verschlechtert das Buch") ehrlich getestet:
- **Ablation:** OHNE RTY 59%/56d vs. MIT 60%/55d am Betriebspunkt → verschlechtert NICHT, trägt aber nur ~+1 Punkt. Verdacht widerlegt, Kritik am Solo-Profil berechtigt.
- **Mini-Retune (6 Varianten, IS/OOS):** **`gap_confirm_min 15 → 10`** ist auf allen Achsen klar besser: OOS-Edge +5,8→**+15,4%**, OOS-expR +0,062→**+0,164**, Sharpe 0,74→**1,19**, Note D→C. Kausale Logik: schnellere Bestätigung erwischt die Reversion, bevor das Gap halb gefüllt ist. (Caveat notiert: Auswahl der besten aus 6 Varianten = milde Selektion; Größe des Sprungs + monotone Param-Sensitivität 10>15>20 rechtfertigen den Swap.)
- **Buch nach Swap:** RoDD 10,0→**10,67**, |Korr| 0,06, f0.14 jetzt 66%/92d, f0.22 57%/43d. Betriebspunkt bleibt Speed (0.18 ≈ 60%/55-57d).
- ⚠️ **VPS-Nachzug nötig:** MaxGapFadeRTY-Instanz auf dem Server läuft noch mit ConfirmMinutes=15 → Parameter auf **10** stellen (kein Recompile, nur Strategie-Einstellung).

## #039 — 🧬 Edge-Decay-Monitor + Live-Phase-Prozess (27.07.2026)
- **Research:** McLean/Pontiff (JoF 2016): publizierte Edges −26% OOS / −58% post-Publikation → Edges sind ein kündbares Abo. Lopez de Prado (AFML): CUSUM-Overlay entkoppelt von Entry-Logik, Deflated Sharpe.
- **Gebaut:** `edge_ref.json` (Backtest-$-Verteilung je Bein via `gen_edge_ref.py`) + `/api/edgehealth` + **Edge-Health-Ampeln im Journal**: z-Score der Live-Summe gegen den Backtest-Erwartungs-Kegel (±σ·√n). 🟢 z≥−1,28 · 🟡 bis −2,33 (Size halbieren) · 🔴 darunter (Bein pausieren + Re-Validierung). Schützt in beide Richtungen: erkennt echten Decay UND verhindert Panik-Kills in normalen Drawdowns.
- **Live-Phase-Prozess dokumentiert** in [[Edge-Decay-Monitor (Konzept + Regeln)]]: Wochen-Takt (Ampeln + 1 Discovery-Batch/Woche + Auto-Fit), Quartals-Walk-Forward, Ersatzbank-Prinzip (Prop-Valide-Tab als Nachrücker-Pool).
- ⚠️ Nebenbei gefunden: **MaxLeadLagES auf dem VPS läuft mit StopMoveMult 0.75, Buch-Bein ist s0.5** → Parameter auf **0.5** stellen (Konsistenz fürs Tracking).

## #040 — Vollautomatik: Auto-Check + 🔔 Notifications + 📋 Aufgaben-Spalte (27.07.2026)
- **`auto_check.py`** läuft alle 30 Min unsichtbar (geplante Aufgabe "MaxLab Auto-Check"): prüft Edge-Decay-Ampeln, Sync-/VPS-Frische während der Session, RiskGuard-Kill-Events, Discovery-Kadenz (1 Batch/Woche), erzeugt Montags-Review-Aufgaben und ToM-Retest-Erinnerung (ab 01/2027).
- **🔔 Glocke im Lab-Topnav** mit Badge (rot bei kritischen Meldungen): Panel zeigt alle Alerts + offene Aufgaben mit ✓-erledigt-Knopf.
- **📋 Aufgaben-Spalte in der Idea Engine** (vor Backlog): von Claude + Auto-Checker gepflegt, Prio-Farben rot/orange/grün. Startbestand: LeadLag-Param (rot), GapFade-Param, Bulenox-VPS-Ticket, Telegram-Token, Frequenz-Bein-Discovery, OpEx-Momentum, Eval-Go-Live-Checkliste.
- Damit fragt das System VON SELBST: Max muss nichts mehr abfragen — alles Wichtige landet als Notification/Aufgabe im Lab.

## #041 — ⚠️ VPS-Verbot bei Bulenox → Pivot zur Home-Trading-Box (27.07.2026)
- **Support-Antwort (#RAX-292098):** VPN/VPS/Proxy strikt verboten, Verstoß = Kündigung + Reward-Verfall. Der Ticket-Check VOR dem Go-Live hat sich voll bezahlt gemacht (ohne ihn: Eval-Kauf + Payout-Verlust-Risiko).
- **Recherche:** Kein Bulenox-Sonderfall — Apex/MFFU verlangen für VPS ebenfalls Einzelfreigabe; Datacenter-IP = branchenweites Flag. Cloud-Tools (TradersPost) gehen nur, weil deren Infra gewhitelistet ist.
- **Entscheidung: HOME-TRADING-BOX** (alter Laptop oder Mini-PC ~€120-250, Wohnsitz-IP): Bulenox-Käfig (+7 Punkte) bleibt, zukunftssicher bei jedem Firmenwechsel, gesamte Infrastruktur (Tailscale/Bridge/Sync/RiskGuard) zieht 1:1 um. Fernaufsicht bleibt via RDP/Tailscale.
- **Sofortmaßnahmen (rote Aufgaben):** Bulenox-Verbindung auf dem VPS trennen (jeder Datacenter-Login = Flag-Risiko), Sim pausiert bis Box steht, VPS nach Migration kündigen.

## #042 — FIRMEN-ENTSCHEID: E8 Futures + VPS (28.07.2026)
- **4 VPS-Anfragen, 4 Antworten:** E8 ✅ A-Note (Mensch: "permitted on evaluation AND funded", keine Restriktionen) · MFFU ✅ (Mensch + Link) · Lucid ⚠️ B-Note (Mensch "yes", aber vage + "own risk") · Tradeify ⚠️ ("at your own risk" vom AI-Agent) · Bulenox ❌ (strikt verboten).
- **E8-Vetting:** seit 11/2021, Dallas+Prag, $38-68M ausgezahlt (12.700+ Payouts), Trustpilot 4,3-4,4 (3.000+ Reviews), Negativ-Reviews = Regelkomplexität, NICHT verweigerte Payouts → legitim.
- **Max' Entscheidung: E8 + VPS** (kein Platz/Lärm für Hardware daheim, will zügig live; akzeptiert ~53%/72d statt 60%/55d — Kompensation über Portfolio-Weiterentwicklung; 2 Versuche kumulativ ~78%). Bulenox-Abo wird gekündigt (Sunk Cost akzeptiert). **Der VPS bleibt die Trading-Maschine!**
- **E8-Konditionen (korrigiert 28.07., echter Checkout-Screenshot):** **E8 Signature**, Futures-Markt, Tradovate, 50k, $150 einmalig (Code DGT wirkte hier nicht, kein Monats-Abo) · EOD-DD 4% ($2.000) · Target 6% ($3.000) · **80% Profit-Split (fix, kein Add-on, gilt firmenweit für alle Tiers)** — meine erste Recherche hatte fälschlich $90/Mon. + 100% Split notiert, das war falsch und ist überall im Lab korrigiert. Daily-Loss 2% nur Soft-Pause · Funded: Tier-1-News-Flat (→ News-Modul für RiskGuard nötig), Best-Day ≤35%, Payout ab 5×0,3%-Tagen · NT8 via **Tradovate-Connector** (nicht Rithmic).
- Lab umgestellt: E8 in PROP_FIRMS, Portfolio/Firm-Block auf E8-Käfig, Aufgabenliste neu (Mini-PC/Laptop/VPS-Kündigung obsolet → archiviert).

## #043 — Frequenz-Bein-Discovery: 0 von 98 Survivors (28.07.2026)
- **Hypothese:** VWAP-z-Burst (Continuation nach >z Sigma Abweichung von Session-VWAP), NQ+ES, Multi-Trade/Tag, Ziel ≥350 Trades/Jahr für ein glatteres Eval-Buch.
- **Ergebnis: klar durchgefallen, ehrlich.** Rohes Signal ohne Filter feuert 15-20k Trades/Jahr und verliert brutal (PF 0,5-0,8) — Kosten ($3,50/RT) fressen den dünnen Edge bei dieser Frequenz komplett auf. Mit Trend-Regime-Filter wird es besser (bis PF 0,94 OOS in der besten Zelle), aber IS bleibt unprofitabel (PF <0,8) → Gate korrekt verworfen. ES ist auf allen Parametern desaströs (PF 0,09-0,22) — Continuation-Edge ist NQ-spezifisch (unser Buch bestätigt das schon länger), nicht auf ES übertragbar.
- **Insight:** Frequenz und Edge sind ein Trade-off. Je öfter man tradet, desto mehr verwässert sich ein Zufalls-Signal zu Kosten-getriebenem Verlust. Ein "immer mehrfach am Tag"-Bein braucht einen deutlich schärferen Filter als Tages-Level-Strategien (ORB, Gap, Asia-Dir) — die Latte liegt bei hoher Frequenz strukturell höher, nicht niedriger.
- **Konsequenz:** Kein neues Bein aus dieser Runde, Auto-Fit lief nicht mal an (0 Survivors = kein Report). Buch bleibt bei 7 Beinen, 457 Trades/Jahr. Frequenz-Hebel vorerst nicht über "mehr Trades desselben Mechanismus", sondern eher über **weitere unkorrelierte Tages-Level-Beine** (nächster Kandidat: OpEx-Momentum-Discovery, Task offen) ziehen.

## #044 — ORB-Offensive: Vol-Scalp wird Bein 8 ✅ (28.07.2026)
- **Anstoß:** Max sah Multi-ORB-Ansatz bei einem Ex-Hedge-Fund-YouTuber (sehr sicher Carlo Zarattini/Concretum). Research-Runde: Zarattini/Aziz 2023 (5m-ORB, 33% Alpha), Zarattini/Barbon/Aziz 2024 (Edge sitzt im **relativen Volumen**), Syu et al. 2019 (TORB), Holmberg et al. 2013, Crabel 1990, arXiv-2026-MNQ-Warnstudie.
- **Engine-Ausbau:** `orb_entry="first_candle"` in orb_std (Zarattini-Entry: Richtung der 1. OR-Kerze, Entry Open Folgekerze, Stop Gegenextrem, Target optional/EOD).
- **Grid: 81 Configs, 3 Teile.** A) Zarattini first-candle · B) ungefilterte Scalps · C) Breakout-Scalps mit Vol-Filter. Protokoll wie immer (Real-Fills, Kosten, OOS ab 2024).
- **Ergebnis:**
  - **AUFGENOMMEN: `ORB2_BRK_or15_c90_t1.0_vol`** = oder15-Breakout, Cutoff Minute 90, Stop 0,5×OR, Target 1R, EINZIGER Filter: Breakout-Bar-Volumen ≥1,5× OR-Schnitt. **A (Score 100), Win 62,4% vs Baseline 53,8%, IS PF 1,36 / OOS PF 1,67, ~33 Tr/Jahr, Ø 12 Min Hold.** Auto-Fit: Buch 57%/82d → **59%/81d**, |corr| 0,07. → Buch = **8 Beine**. Port: `MaxORBScalpNQ.cs` (Deploy aufs VPS ausstehend, VPS war offline). Edge-Monitor erweitert (mean +11,28$/Trade, win 62%).
  - **Abgelehnt trotz A-Note:** t1.5- und or10-Variante = gleicher Mechanismus, Auto-Fit-Marginaltest zeigt +1/±0 Punkte → wäre nur Size-Verdopplung auf demselben Trade, keine Diversifikation. Wichtige Lehre für Max' "alle parallel laufen lassen"-Frage: **niedrige |corr| bei seltenen Tradern täuscht, der Marginaltest entscheidet.**
  - **Zarattini pur (5m, EOD)** einziger Grid-Survivor (OOS PF 1,15), aber Auto-Fit lehnt ab: macht Buch schneller (48d statt 82d) aber −10 Punkte Pass. Watchlist. **or15-Zarattini:** OOS brillant (PF 1,34), IS tot (0,99) → ehrlich verworfen.
  - **Scalp-Exits ohne Filter töten den ORB-Edge** (je früher der Zeit-Exit, desto schlechter): der Edge kommt vom Laufenlassen auf Trendtagen. Ein Scalp funktioniert NUR mit dem Volumen-Gate (verwirft 87% der Breakouts).
- **Encoding-Bug gefixt:** ✅-Emoji im Auto-Fit-Print crashte unter cp1252 beim Log-Pipen und brach die Buchaufnahme ab — Fit-Log bereinigt, Re-Run, jetzt ASCII.

## #045 — Betriebspunkt frac 0.22 + Ticket-Feature im Lab (29.07.2026)
- **Betriebspunkt-Entscheid (Max): frac 0.18 → 0.22** auf dem 8-Bein-Buch (E8 50k): **52% Pass in ~45 Tagen** statt 56%/77d. EV-Logik: erwartete Zeit-bis-Funded **~87d statt ~138d** (T/p inkl. Fehlversuche), Mehrkosten nur ~$20 erwartete Fees. 0.22 = bewusst der letzte Frontier-Punkt über 50% (0.26/0.30 wären rechnerisch schneller, aber zu viel Vertrauen in die Sim-Genauigkeit). Umgestellt: `funded_finalize.py` (FRAC), `portfolio.json`, Portfolio-Tab zeigt Betriebspunkt jetzt dynamisch. **RiskGuard CushionFrac 0.22 beim Eval-Start = offenes rotes Ticket im Lab.**
- **🎫 Ticket-Feature gebaut:** Max kann jetzt selbst Aufgaben ins Lab schreiben (nichts mehr vergessen). Eingabefeld + Prio-Ampel (🟢🟠🔴) in der 📋 Aufgaben-Spalte (Idea Engine) **und** im 🔔 Meldungen-Panel, Enter = anlegen. Neuer Endpunkt `/api/tasks/add` → `tasks.json` (source "max"), erledigen wie gehabt per ✓. Hot-Reload übernimmt den Server-Neustart.

## #046 — Break-Even/Trailing-Stop-Overlay: ehrlich getestet, NO-GO (29.07.2026)
- **Max' Frage:** Break-Even- oder Stop-in-Profit-System fürs Buch? **Gebaut:** generischer opt-in Overlay in der Engine (`qbt._trail_stop`, Params `be_trigger`/`be_offset`/`trail_trigger`/`trail_dist`, Default aus → Buch unberührt), verdrahtet in ALLE 8 Bein-Generatoren (4 qbt-Loops + `asian.py` + `rv.py`, kein Intrabar-Look-Ahead). Studie: `be_trail_study.py`, Ergebnisse `be_trail_results.txt`.
- **Part 1 (per Bein, 7 Configs, IS-Auswahl → OOS-Test): 0 von 8 Beinen überlebt.** 5/8 zeigten IS-Verbesserung (z.B. ORB-Breakout BE0.75: IS +0,026→+0,082) — **alle 5 kollabieren OOS** (ORB OOS 0,242→0,136; RV-leadlag 0,398→0,247). LastHour/ORB2: Overlay wirkungslos (Trades zu kurz). ORB-fade: Trailing OOS sogar negativ.
- **Echter, aber nutzloser Effekt:** MAE sinkt real (z.B. Momentum 0,82→0,65R) — Varianz-Reduktion ja, aber die Expectancy-Kosten (gekappte Gewinner) fressen es auf. Exakt der Literatur-Befund (Quantfish, ATAS, EJBMR-Studie) + unser #044-Befund (Zeit-Exits töten ORB-Gewinner).
- **Part 2 (Buch-Frontier, Ziel-Metrik):** am Betriebspunkt f0.22: Baseline 52%/45d vs. Overlay 53%/47d = **MC-Rauschen**. Scheinbare +3 Punkte bei f0.10 sind IS-kontaminiert (Auswahl auf IS, Frontier über Gesamtzeitraum) + kosten ~15 Tage Tempo.
- **Entscheid: Buch bleibt OHNE Overlay.** Feature bleibt als opt-in in der Engine (kostenlos für künftige Tests). **Simplex beats Komplex bestätigt sich zum 3. Mal** (nach Sizing-Policies #032 und Zeit-Exits #044).

## #047 — Paper-Check: Requejo TSI Mean Reversion (SSRN 4708400) — NO-GO (29.07.2026)
- **Quelle: Instagram-Reel** (alphazone.ai). Paper: Daily-TSI-MR auf SPY/QQQ, Ø 5d Holds, 1996-2022. **Overnight-Holds = verstößt gegen Prop-Constraint.** SSRN-Paywall (403) → exakte Parameter unbekannt, Proxy-Test mit Standard-TSI(25,13), vorab fixiertes Mini-Grid (`tsi_paper_test.py`).
- **Ergebnis auf NQ/ES Daily (2016-26, IS/OOS, echte Kosten):** nur 1 von 4 Varianten positiv, nur auf NQ (ES OOS negativ) — kippt über Parameter UND Instrument. **n=21 Trades in 10,5 Jahren (2/Jahr)** → statistisch Rauschen + fürs Eval nutzlos (dünnstes Buch-Bein hat 25/Jahr).
- **Interessanter Nebenbefund:** Overnight-Anteil des Systems auf NQ durchweg **negativ** (−409 IS/−334 OOS pts) — konsistent mit totem Overnight-Drift (#028/NY-Fed). Die SPY/QQQ-1996-2022-Performance des Papers lebt vermutlich von einem Regime, das es auf modernen Index-Futures nicht mehr gibt.
- **Kein Deploy.** Analyse: [[TSI Mean Reversion (Requejo 4708400)]], Registry aktualisiert. Lehre: **Instagram-Trading-Paper ab jetzt mit Marketing-Selektionsbias-Prior behandeln.**

## #048 — RiskGuard v2: 🏆 Eval-Pass-Auto-Flatten + 📰 News-Flat (30.07.2026)
- **Anstoß: 2 Max-Tickets.** (1) Tool, das beim Erreichen des Gesamt-Profits alle Positionen schließt. (2) "Es ist kein TP da" — Verwirrung am Live-Chart.
- **🏆 EvalProfitTarget (Default $3.000 = E8-Target):** erreicht die **Gesamt-PnL** (NetLiq − Initial-Balance, inkl. offener Positionen) das Ziel → alle Positionen zu, Konto wird **dauerhaft** flat gehalten (Flag überlebt Neustarts via State-Datei, Size-Datei → 0, Telegram-Alarm). Conditions (alle Pflicht): Feature an, Initial-Balance bekannt, NetLiq gültig, noch nicht ausgelöst. 0 = aus (Funded).
- **📰 News-Flat (E8-Funded-Regel, Task von 28.07.):** 2 Min vor / 3 Min nach Tier-1-Events (FOMC/CPI/NFP) wird geflattet + flat gehalten. Termine aus `maxlab_news.csv` (ET, Rest-2026 eingepflegt aus Fed-/BLS-Kalender → [[Research-Cache]]). Läuft ab jetzt in der Sim mit = ehrliche Validierung vor Funded.
- **TP-Ticket = kein Bug:** 5 von 8 Beinen (Momentum, PowerHour, AsiaDir, LeadLag, ORBFade) haben **by design keinen TP** — Zeit-Exit EOD, exakt wie backgetestet. TP nur bei ORB-Breakout/ORB-Scalp/GapFade; beide ORB-TPs sind heute live gefüllt worden. "Viel im Profit ohne TP" ist gewollt: Trend bis EOD laufen lassen; das Gesamt-Ziel sichert jetzt der RiskGuard.
- **Deploy:** v2 + News-CSV liegen auf dem VPS (Backup `MaxRiskGuard.cs.bak-20260730`). **Aktiv erst nach Max' F5-Compile** (rotes Ticket im Lab). Server-Check 17:39: NT8 läuft (seit 26.07.), 3 Kontrakte Size, kurzer E8-Reconnect 16:47 dt. (1,5s, unkritisch), 176 GB frei.

## #049 — OpEx-Momentum: Hypothese BESTÄTIGT, aber Bank statt Buch (30.07.2026)
- **Why (VOR dem Test fixiert, Data-Mining-Schutz):** Am Monats-OpEx laufen Dealer-Hedges der auslaufenden Optionen einseitig ab (Charm-/Gamma-Unwind, Praktiker-Doku → [[Research-Cache]]); fällt die Pinning-Kraft weg, setzt sich die Vormittagsrichtung nachmittags fort. Eigener Vorbefund #034: Fade −22% → Spiegel-Trick (Insight #7).
- **Setup:** Neuer Modus `opex_mom` in `calendar_fx.py` (Entry 11:30/12:00/13:00, |AM-Move| ≥ 0.1/0.2/0.3×ATR20, Stop 0.75/1.0/1.5×ATR20), 108 Configs auf NQ/ES/YM/RTY, IS/OOS 65/35, Klein-N-Hürde 3%.
- **✅ Ergebnis: 59 von 87 gewerteten Configs überleben** (28 starben nur an Frequenz) — der Effekt ist über alle 4 Instrumente und fast alle Parameter robust. Beste: NQ e150/t0.3/s0.75 mit **OOS PF 3.34, Sharpe 6.9**; ES/YM/RTY ähnlich (OOS PF 3.1-3.35). Das ist keine Einzelconfig-Anomalie, das ist ein echter Kalender-Effekt.
- **❌ ABER: nur ~6-9 Trades/Jahr** → Auto-Fit lehnt alle 4 Besten korrekt ab (Buch 59%/81d → 60%/78-83d, |corr| 0.06): Buch-Beitrag zu klein. **Gleiche Kategorie wie CAL_fomcpost (#034): Bank/Prop-Valide, kein Bein.** Reports liegen im Lab (`OPEXMOM_*`).
- **💡 Folge-Idee (Backlog):** Die Bank sammelt jetzt 2 robuste Klein-N-Event-Edges (FOMC-Post ~8/yr, OpEx-Mom ~7/yr). Ein **kombiniertes "Event-Bein"** (ein NT8-Skript, mehrere Event-Trigger) käme auf ~15-20 Trades/Jahr — könnte die Fit-Hürde knacken. Kandidat für den nächsten Discovery-Block.

## #050 — ORB-Scalp: Max' "kurzes Fenster"-Hypothese → 🎉 BEIN 9 aufgenommen! (30.07.2026)
- **Anstoß: Max' Intuition** — "Trade auf, schnell kleinen Profit, oft gewinnen, so den Fund machen". Klassischer Scalp (nicht unser bisheriges "Scalp"-Bein 8, das ist 1 Trade/Tag mit 1R-Target). Engine erweitert: neuer `orb_max_hold`-Param (Zwangs-Exit N Min nach Entry = das "kurze Fenster").
- **Research (Research-Cache 30.07.):** MNQ-Falsifikation (arXiv 2605.04004) — nackter Short-Horizon-Breakout clears die Kosten NICHT (roher Edge 0,07-1,50 Pkt < 2 Pkt), bar+1 (kurz) SCHLECHTER als bar+15. Market Intraday Momentum lebt vom Halten bis Close. ABER: einziges hochsignifikantes Signal = Volumen-Filter (Win 68%). → Test nur MIT Vol-Filter, bewertet gegen Win-Rate + Eval-P(pass), nicht Sharpe (Insight #6).
- **Ergebnis (60 Configs, NQ/ES/YM × Target × Hold-Cap):** **20 Survivors — alle auf NQ.** Enges 0,3R-Target + Vol-Filter → Win-Rate bis 87% (OOS 86%). Höhere Targets = mehr $/Micro (t1.0: $2.400) aber weniger Win. Die ganze NQ-Fläche ist positiv = robust, kein Einzel-Glücksfall.
- **❌ ES/YM: katastrophal.** ES edge −13 bis −29% (PF 0,18-0,57!), YM negativ + zu selten. **Klare Bestätigung des Buch-Charakters:** NQ-Breakouts laufen durch, ES/YM drehen. Scalp ist ein reines NQ-Momentum-Phänomen.
- **🎉 BEIN 9: `SCALP_NQ_t0.5_hEOD` AUFGENOMMEN** (Auto-Fit: Buch 59%/81d → **61%/81d**, |corr| 0,09): 0,5R-Target statt 1,0R, sonst **identischer Entry wie Bein 8** (gleicher Breakout, gleicher Vol-Filter, gleicher Stop). Win 80,9% (OOS 81,2%), PF 1,70, expR +0,142, Haltezeit nur 3,3 Min. **Das ist strukturell ein Scale-Out desselben Signals**, kein neuer Mechanismus — Bein 8 lässt laufen (1,0R), Bein 9 nimmt schneller mit (0,5R). NinjaScript `MaxORBScalpNQ2.cs` gebaut (Kopie von Bein 8, nur TargetMult 0.5 + eigene Order-Tags) und aufs VPS gestaged — **Compile hängt am selben offenen F5-Ticket wie RiskGuard v2.**
- **⚠️ Korrektur:** Erster Bericht sagte fälschlich "alles auf der Bank" — der Report-Lauf für die restlichen 16 Survivor-Configs lief zu dem Zeitpunkt noch im Hintergrund weiter; `SCALP_NQ_t0.5_hEOD` kam erst danach durch den Auto-Fit. **Buch ist jetzt 9 Beine.**
- **💡 Prozess-Erkenntnis bestätigt sich:** Der **Exit-Raum** war der eigentliche Hebel, nicht ein neuer Mechanismus — dieselbe Entry-Logik, zweimal mit unterschiedlichem Exit gefahren, hebt die Passquote. Kandidat: systematisch prüfen, ob andere bestehende Beine (Momentum, Asia-Dir) ebenfalls von einem zweiten, engeren Exit-Profil profitieren. Siehe [[Discovery-Prozess (wie wir Alpha finden)]].

## #051 — Pivot Points: ehrlich getestet → NO-GO (30.07.2026)
- **Anstoß: Max' Frage** — Pivots recherchieren, Mechanismus verstehen, Strategien bauen. Neues `pivot.py` (Floor-Pivots aus Vortages-HLC: P, R1/S1, R2/S2) mit 3 Modi: Revert (Fade an S1/R1 → P), Break (Ausbruch = Momentum), Open-Bias (CPR-Sentiment).
- **Research-Verdict (Research-Cache 30.07.):** Fast alle Pivot-"Evidenz" = Marketing-Blogs. Einziges echtes Paper (Hsu/Hsu/Kuan 2010, data-snooping-robust): **TA-Level überleben in reifen Index-Märkten NICHT.** Lo/Mamaysky/Wang: modeste Info, kein Profit-Claim. Die "89% Touch-Quote" ist near-tautologisch (Level liegt in der Range → Touch fast garantiert, keine Edge).
- **Ergebnis (52 Configs, 4 Instrumente):** **47 sterben IS, bester Full-Edge nur +3,0%.** 2 marginale "Survivors" (NQ pivot_revert, PF 1,06-1,13) — mit hoher Wahrscheinlichkeit **Multiple-Testing-Rauschen** (2/52 am Gate = Zufalls-Bodensatz), noch dazu gegen den NQ-Momentum-Prior. Auto-Fit lehnt beide ab; c180 **senkt** die Passquote sogar (59%→57%).
- **Fazit: Pivots gehen in den ehrlichen Friedhof.** Genau die Disziplin, die unser Moat ist: keine Schein-Edge ins Buch, nur weil das Netz sie feiert. Kein kausales Order-Flow-Why (anders als RVOL #044 oder Charm #049) → kein Deploy.

## #052 — Video-Check: "Pivot Point Strat" (proptradingindicators.com) — NO-GO (30.07.2026)
- **Anstoß: Max' YouTube-Video** ([92hI5TrBcPk](https://www.youtube.com/watch?v=92hI5TrBcPk), Transkript von Max eingefügt, da kein automatischer Zugriff möglich). Wichtiger Fund: Produkt heißt "Pivot Point Strat", ist aber **kein Floor-Pivot-System** (kein P/R1/S1, das haben wir schon in #051 getestet) — proprietärer Indikator "PPG1" auf **symmetrischen Renko-Bricks**, binäres Regime, Formel nicht offengelegt → nicht 1:1 reproduzierbar.
- **Mechanik:** Entry auf Schlusskerze in Regime-Richtung, hält bis Gegensignal (Flatten+Flip), fixer Stop (MNQ-Beispiel 160 Ticks), Break-Even-Lock ab +170 Ticks, kein festes Target. **Kernthese des Videos:** zwei Modi — Signals (ganztägig) vs Time-Window (nur 9:32-13:30 ET) — Verkäufer-Claim: Window leicht besser, gestützt nur auf 1 Kunden-Anekdote, keine Zahlen. Skepsis-Flag: Verkäufer-Demo, bewusst ausgewählte Beispieltage.
- **Eigener Proxy-Test (neues `flip.py`):** PPG1 nicht nachbaubar, also generische Renko-Richtungswechsel-Mechanik nachgebaut (Schwellen-Umkehr-Regime auf echten 1-Min-Daten). **Iteration 1 (EMA-Crossover) scheiterte krachend** (42.727 Trades/10J, win 28,6% — reines Zeit-Bar-Rauschen) — bestätigt indirekt, warum Renko nötig ist. **Iteration 2 (Schwellen-Umkehr, Renko-äquivalent)** funktioniert besser, Sweet Spot bei Brick≈0,75×ATR20.
- **A/B-Test Time-Window vs Signals (24 Configs, NQ/ES/YM/RTY):** Nur NQ hat Edge, ES/YM/RTY negativ (bestätigt wieder unser Buch-Muster: NQ trend-folgt, die anderen nicht). Auf NQ ist Time-Window minimal besser, aber der Unterschied ist klein und über andere Parameter uneindeutig (7:5 im Rauschen) — **die Video-These bestätigt sich nicht klar.**
- **Auto-Fit: alle 4 Survivors klar ABGELEHNT** — Buch-Passquote würde von 61%/81d auf 47-51%/37-40d **fallen**. Grund: 400-500 zusätzliche Trades/Jahr mit schwachem Edge (~46% Win, nahe Coinflip) verwässern das bestehende Buch, trotz niedriger Korrelation (0,08-0,09). **Wichtige Prozess-Lehre: niedrige Korrelation allein reicht nicht — Trade-Qualität (Edge pro Trade) zählt genauso.**
- **Fazit: Video-Strategie NICHT bauen.** Weder die Kernthese (Time-Window > Signals) hält robust, noch würde ein Renko-Flip-System unser Buch verbessern. Kein NinjaScript-Deploy.
> Idee (Max): mehrere unkorrelierte Strategien parallel auf demselben Eval laufen lassen → glattere Equity → höhere kombinierte P(pass) + schnelleres Passen (mehr Trades/Tag).
- **✅ KEEPER #1 (Trend-Bein):** `NQ_ORB_sweet_or15_vol1.3` — gefilterte ORB, A-Note, verdient auf **Trend-/Expansions-Tagen**. Fest eingeplant für die Eval-Passing-Stage.
- **Gesucht (Reversion-Bein):** eine höher-frequente Strategie, die auf **Range-/Fade-Tagen** verdient (die Tage, an denen ORB aussetzt/verliert). Anti-korreliert = maximaler Portfolio-Nutzen.
- **Regel:** Beine müssen auf **verschiedenen Regimes** verdienen, sonst kein Diversifikations-Effekt (zwei Momentum-Strategien = korreliert = bringt wenig).
- **To-Do:** kombinierte Equity/Korrelation + kombinierte P(pass) im Prop-Assistant simulieren, sobald ein zweites Bein steht.

## 🧠 Insight-Bank (kumulierte Markt-Erkenntnisse)
Das Wertvolle aus den Fehlschlägen. Für jede zukünftige Strategie beachten:

1. **NQ/ES 1m an VWAP-Stretches → Continuation, nicht Reversion.** Reversion an der VWAP ist die falsche Richtung. Momentum/Continuation ist der real belegte Effekt (Gao/Han/Zhou), **stärker an Trend-/Vola-/News-Tagen** → Regime-Filter wirkt (P(pass) 2%→16%).
2. **Baseline-Regel (wichtigste):** Breakeven-Win-Rate = Stop/(Stop+Target). Win-Rate IMMER gegen diese Baseline messen, nie absolut. 60% klingt hoch, ist aber bei RR<1 nur Breakeven = keine Edge.
3. **Momentum-Spannungsfeld:** Continuation hat naturgemäß niedrige Win-Rate + RR>1 → Gegenteil des High-Winrate-Wunschprofils. Ehrlich anerkennen.
4. **Fill-Realismus killt Schein-Edges.** Alle bisherigen "Edges" waren Fill-Optimismus (echter Touch, Stop-before-Target, Kosten, MAE = Pflicht).
5. **Frequenz-Falle:** Zu viele marginale Trades → Kosten fressen dünne Edges. Weniger, größere, selektivere Trades.
6. **Prop-Passing ≠ Sharpe.** Der Trailing-DD bestraft **Pfad-Varianz**, nicht die Langfrist-Erwartung. Ein RR≤1-Setup mit hoher Win-Rate (ORB) skaliert auf 4-5 Micro und passt mit 55-61%; ein RR>1-Momentum mit Sharpe 2,0 (TS-Momentum) bleibt bei 1-2 Micro und 33-42%, weil choppige Equity am DD-Limit reißt. **Für Evals: enges, kontrolliertes Risiko + hohe Win-Rate schlägt hohen Sharpe.**
7. **Spiegel-Trick:** Wenn eine Richtung konsistent negativ ist (Fade -6% edge), ist die Gegenrichtung oft der Edge (Momentum +8%). Immer beide Seiten testen, bevor eine Strategie verworfen wird.
8. **R-Multiples driften mit dem Preisniveau** (#070). `r_net = r − cost/R_pts` — bei konstanten Kosten und über 10 Jahre wachsenden absoluten Ranges (NQ: 5,4 → 49,8 Pkt mittleres R) fällt die Kostenquote von 18,7% auf 2,0%. Ein aggregierter expR über die volle Historie gewichtet späte Jahre systematisch hoch. **Immer zusätzlich die USD-Jahrestabelle + mean R_pts pro Jahr ansehen.**
9. **Passquoten sind fensterabhängig** (#070). Die Buch-Zahl 57%/86d wird zu 51%/117d, wenn man nur 2016-2023 rechnet, und zu 63%/46d für 2024-2026. Der Auto-Fit sieht immer nur die volle Historie. **Jede Buch-Änderung braucht die IS/OOS-getrennte Frontier, nicht nur den Betriebspunkt.**
10. **Die Gegenprobe ist wertvoller als der Test** (#070). Ein Regime-Filter, der IS und OOS positiv aussieht, kann trotzdem wertlos sein — entscheidend ist, wie die **Komplementärmenge** läuft. Beim VIX-Band war „außerhalb" OOS *besser* als „innerhalb". **Bei jedem Kontext-/Regime-Filter die Gegenprobe mitmessen, sonst ist der Fund nicht bewertbar.**
11. **Jede Zielfunktion erzeugt ihre eigenen Artefakte** (#071). „Maximiere Passquote" (auto_fit) lehnt systematisch Tempo-Beine ab. „Minimiere Tage bis Pass" zieht systematisch **Tail-Lotterien** an, weil seltene große Gewinne das Target im Monte-Carlo schneller erreichen — auch wenn das Bein die meiste Zeit verliert. **Qualitätsgates gehören VOR die Suche, nicht dahinter.**
12. **Mehr Beine sind nicht besser** (#071). Diversifikation zahlt nur, solange das neue Bein die **Pfad-Varianz** nicht erhöht (Insight #6). `NQ_Momentum` ist einzeln sauber (IS +0,093 / OOS +0,232 / 10 von 11 Jahren) und senkt die Buch-Passquote trotzdem um 10 Punkte, weil Continuation mit RR>1 eine choppige Equity hat. Ein 4-Bein-Buch schlug das 6-Bein-Buch auf **jedem** Punkt der Frontier.

## #054 — Event-Bein: FOMC-Post + OpEx-Momentum kombiniert → Bank statt Buch (31.07.2026)
- **Why (vorab fixiert):** #034 (CAL_fomcpost_ES) und #049 (OPEXMOM_ES) sind beide einzeln robust bestätigt, aber mit ~7-8 Trades/Jahr zu selten fürs Buch. Beide zufällig mit demselben Stop-Multiplikator (0,75×ATR20) validiert → technisch triviale Kombination: neuer Modus `event_combo` in `calendar_fx.py` (FOMC-Statement-Tag → fomc_post-Logik, sonst OpEx-Freitag → opex_mom-Logik, beide Terminarten überschneiden sich strukturell nie).
- **Primärtest (vorab festgelegter Parametersatz, kein Fishing):** ES, entry_min 180, thresh 0.3, stop 0.75× ATR. **108 Trades, ~10,7/Jahr, Grade A (Score 100), Win 55,6% vs. Baseline 39,9%, expR +0,182, OOS-Edge +25,3%, OOS-expR +0,310.** Zusätzliches Robustheits-Grid (7 Nachbar-Configs): **7/7 ebenfalls robust** — sehr stabile Parameter-Nachbarschaft, kein Zufallstreffer.
- **❌ Auto-Fit: ABGELEHNT.** Buch 61%/81d → 61%/82d mit dem Bein (|corr| 0,07) — trotz niedriger Korrelation zu marginal, verschlechtert sogar die Tage-bis-Pass leicht. Landet wie die Einzelversionen auf der Bank/Prop-Valide (`EVENT_ES_primary`), kein 10. Bein.
- **Lehre:** Kombinieren zweier Klein-N-Edges verbessert die Einzelqualität deutlich (Edge/PF beider Bestandteile addiert sich fast), aber die Auto-Fit-Hürde ist nicht nur Frequenz — der Portfolio-Beitrag (Tage-bis-Pass-Verbesserung) zählt am Ende. Frequenz-Wette allein reicht nicht.

## #055 — Parameter-Audit: 2 von 9 Beinen liefen mit falschen Live-Defaults (01.08.2026)
- **Setup:** Alle 9 `SetDefaults()`-Blöcke der NinjaScript-Beine gegen `book_state.json` verglichen, bei Verdachtsfällen zusätzlich die Formel im Backtest-Code (`qbt.py`/`rv.py`) nachverfolgt statt nur Parameternamen zu vergleichen.
- **✅ 7/9 exakt korrekt** (Momentum, PowerHour, ORB-Breakout, ORB-Fade inkl. NR7-Filter im Code bestätigt, AsiaDir, ORB-Scalp Bein 8+9).
- **❌ 2 echte Abweichungen gefunden:**
  - `MaxGapFadeRTY`: `ConfirmMinutes = 15` statt validiertem `gap_confirm_min = 10` — lief mit dem Engine-Default statt dem gebuchten Wert.
  - `MaxLeadLagES`: `StopMoveMult = 0.75` statt validiertem `rv_stop = 0.5` — **50% weiterer Stop** als gebucht (Formel gegengeprüft: `mult × |Leader-Move|`, identisches Konzept in Backtest und Live).
- **Fix + Deploy 01.08.:** Beide Defaults korrigiert, aufs VPS hochgeladen (Konto vorher als flach verifiziert). Braucht noch F5-Compile.
- **Lehre:** Vermutlich beim Bau der NinjaScripts aus dem Engine-Default statt dem tatsächlich gebuchten Wert kopiert — Copy-Paste-Drift zwischen Backtest-Validierung und Live-Deploy. Parameter-Audit sollte fester Bestandteil beim Hinzufügen jedes neuen Beins werden, nicht erst nachträglich.

## #056 — Alpha-Batch VWAP-Pullback / IB-Extension / Overnight-Reversal: 2 Bank-Funde, 1 Kill, kein Bein (02.08.2026)
- **Auftrag Max:** intensiv nach Mechanismen suchen, die im Buch noch nicht vertreten sind (u.a. VWAP). Research vorab in [[Research-Cache]] (Alpha-Batch #056): SSRN 2730304 (Overnight-Intraday-Reversal, Market-Maker-Inventar-Mechanismus), SSRN 5807282 (Overnight → erste 30 Min invers, Decay-Warnung), VWAP-Pullback (Praktiker-Prior, konsistent mit Insight #1), IB-Extension (Market Profile).
- **Setup:** Neues Engine-Modul `intraday2.py` (mode="i2") mit `vwap_pull` / `ib_ext` / `on_rev`, Discovery `alpha_i2_discovery.py`: **252 Configs** über NQ/ES/YM/RTY, IS/OOS 65/35, ≥25 Tr/Jahr, Real-Touch + Kosten. Lauf detached, 17,5 Min.
- **❌ IB-Extension: 0/72 Survivors — kompletter, sauberer Friedhof.** Späte Initial-Balance-Breaks haben auf modernen Index-Futures nach Kosten keinen messbaren Edge. Market-Profile-Klassiker ehrlich beerdigt.
- **🏦 VWAP-Pullback: 17/108 Survivors, konzentriert NQ (10) + RTY (7), ES/YM tot.** Bester: `VWAPPULL_NQ_t0.4_z0.15_s0.5` (114/yr, edge +2,7%, OOS-edge +6,4%, PF 1,12).
- **🏦 Overnight-Reversal: 9/72 Survivors, NQ (7) + YM (2), ES tot.** Bester: `ONREV_NQ_l0.5_c0_eod_s0.75` (70/yr, edge +3,6%, **OOS-edge +9,6%, OOS-expR +0,147**, PF 1,16).
- **⚠️ Ehrliche Beobachtung — invertierte IS/OOS-Signatur:** Bei beiden Gewinnern ist der IS-Edge dünn (+0,5-0,8%) und der OOS-Edge (ab ~2024) deutlich stärker. Das ist das GEGENTEIL des üblichen Overfitting-Musters, heißt aber: der Effekt ist jung/regime-abhängig (hohe-Vola-Ära 2024-26; bei on_rev konsistent mit SSRN 5807282 „stärker bei hoher Vola"). Kein struktureller Langzeit-Edge bewiesen — Decay-Monitor wäre bei Live-Nutzung Pflicht.
- **❌ Auto-Fit: alle 4 Besten ABGELEHNT** — aber mit strategisch interessantem Muster: `ONREV_NQ` → Buch 59%/**63d** (statt 61%/81d), `VWAPPULL_NQ` → 54%/**52d**. Die Kandidaten tauschen Passquote gegen Geschwindigkeit (bis zu 29 Tage schneller bei −2 bis −7pp). Der Auto-Fit optimiert auf Quote → korrekt abgelehnt, aber als **bewusste Option für Max dokumentiert**: wer schneller durch die Eval will und das Quote-Opfer akzeptiert, hat hier Kandidaten (Reports in Prop-Valide).
- **Verdict: kein 10. Bein.** 2 neue Mechanismen-Familien auf der Bank (erste VWAP- und erste Overnight-Signal-Edges im Fundus), 1 ehrlicher Kill. Engine um wiederverwendbares i2-Modul reicher.

## #057 — Alpha-Batch Intraday-Momentum (JFE) / Crabel-Stretch / Momentum-Selektiv (02.08.2026)
- **Setup:** 152 gewertete Configs (`alpha_i2b_discovery.py`), Modi `im_ll` + `volbrk` neu in `intraday2.py`, `mom_sel` über den existierenden ER-Filter (`rev_er_min`) des ts_reversal-Moduls. WHYs vorab in [[Research-Cache]] „Alpha-Batch #057". Lauf detached, 15,9 Min.
- **❌ im_ll (Gao/Han/Li/Zhou JFE 2018, first-30→last-30): 0/48 — BEIDE Seiten tot.** Momentum-Seite: 0 von 24 Configs mit positivem expR (modern klar invertiert), Spiegel-Seite (vorab deklariert, Insight #7): nur 4/24 expR>0, 0 Survivors. **Top-publiziertes Paper, Sample 1993-2013 → Post-Publikations-Verfall in Reinform.** Gleiche Kategorie wie Pre-FOMC-Drift (#034). Wichtiger Friedhof-Eintrag: Berühmtheit eines Papers ≠ lebender Edge.
- **🏦 volbrk (Crabel-Stretch): 18/88 Survivors, massiv NQ-lastig (16 NQ, je 1 ES/YM, RTY 0).** Bester: `VOLBRK_NQ_k0.3_s0.5_nr1_c120` (**mit** NR7-Kompression — Crabels Kernbedingung bestätigt sich): 30/Jahr, Win nur 29% aber classic Crabel-Profil (viele kleine Stops, wenige große Trend-Gewinner), OOS-expR +0,355, PF 1,23. Wieder invertierte IS/OOS-Signatur (+1,7%→+8,7%) wie #056 — junger/Vola-Regime-Effekt.
- **⭐ mom_sel (ER-Filter aufs Buch-Momentum): 9/16 Survivors, auf NQ 8/8 — komplette Parameter-Nachbarschaft robust.** Bester: `MOMSEL_NQ_er0.3_s0.75`: 83/Jahr (statt 96 ungefiltert), edge +6,0%, expR +0,168, PF 1,30 — und **IS +6,0% / OOS +6,1%: perfekt zeitstabil**, als einziger Kandidat der Woche OHNE invertierte Signatur. Das ist ein echter, struktureller Filter-Effekt: der Kaufman-ER wirft die choppy Signal-Fenster raus. ES gemischt (nur er0.5 überlebt) — Effekt ist NQ-spezifisch.
- **❌ Auto-Fit: alle 4 Besten als ZUSATZ-Bein abgelehnt** (gleiche Tempo-vs-Quote-Struktur wie #056: MOMSEL 53%/53d, VOLBRK_NQ 60%/73d).
- **💡 Die eigentliche offene Frage — REPLACE statt ADD:** Der Auto-Fit testet nur „als 10. Bein dazu". Die richtige Frage bei mom_sel ist: **bestehendes NQ_Momentum-Bein durch die ER-0.3-Version ERSETZEN** (gleicher Mechanismus, nur strengerer Filter, +0,168 vs. Basis-expR, zeitstabil). Braucht einen manuellen Replace-Test (book_state-Kopie mit `rev_er_min=0.3`, Buch-MC neu rechnen, P(pass)-Vergleich) — **~15 Min Rechenzeit, Entscheidung liegt bei Max.** Nicht eigenmächtig umgebaut.
- **Verdict: kein neues Bein, 1 Friedhof-Klassiker (JFE-Paper), 1 Bank-Fund (Crabel-NQ), 1 heißer Replace-Kandidat (mom_sel) zur Entscheidung.**

## #058 — Journal-Bug ROOT CAUSE gefunden: Equity-CSV ohne Kontospalte (05.08.2026)
> Tickets liegen im **Lab** (📋 Aufgaben / 🔔 Meldungen), nicht hier — hier nur der Befund. Steuer/Gewerbe-Details: [[Steuer & Gewerbe (Prop-Payouts)]].

- **Max' Symptom:** Journal-Zahlen stimmen wieder nicht — Kontoansichten widersprechen sich (2k vs. 3k), Trade-Log zeigt den ganzen August über alle Accounts statt nur das gewählte Konto. Zweiter Zahlenfehler nach dem Fix vom 03.08.
- **🔎 Root Cause (verifiziert am Live-System):** Der Server erwartet seit dem Multi-Konto-Fix vom 04.08. in `maxlab_equity.csv` **drei** Spalten (`date;konto;netliq`) und **verwirft jede Zeile mit weniger** (`len(p) >= 3`). Die Datei auf dem VPS ist aber weiterhin **zweispaltig** (`date;netliq`) — der RiskGuard schreibt das alte Format, weil der C#-Teil nie nachgezogen/kompiliert wurde. Ergebnis: `_account_equity()` findet **null** gültige Zeilen und fällt auf den RiskGuard-Textlog zurück. Und dieser Fallback kennt kein Konto → er klebt die **komplette** Equity-Historie auf `_current_account()`.
- **Konkret nachgewiesen:** Fill-Log sagt 29.07.–03.08. = **Sim101**, ab 04.08. = **Simtestsim2**. Der Fallback schreibt aber die gesamte Kurve inklusive des **Sim101-Eval-Passes (+3.026 am 03.08.)** auf **Simtestsim2** (zeigt dort 103.046 = „3k plus"), obwohl Simtestsim2 real nur **+2.310** aus 10 eigenen Trades hat. Sim101 (+2.004 aus 20 Trades) verliert seine Historie komplett. Genau der Fehler, den der Code-Kommentar verhindern wollte („sonst würden Sim101-Alt-Zahlen als Simtestsim2-Stand angezeigt") — der Schutz greift nicht, weil der Fallback denselben Fehler nochmal macht.
- **Lehre (dieselbe wie #055):** Der Fix wurde nur auf der Python-Seite gebaut, der schreibende C#-Teil blieb auf dem alten Format. Ein Format-Wechsel braucht **beide** Seiten plus eine Abnahme gegen echte Daten — sonst ist ein „strengeres" Parsing (Zeilen verwerfen) schlimmer als gar kein Fix, weil es still in einen falschen Fallback kippt. **Silent-Fallbacks sind gefährlicher als harte Fehler.**
- **🚨 Der eigentliche Fund kam beim Fixen: der RiskGuard erbt den State des Vorgängerkontos.** `maxlab_riskguard_state.txt` führt keinen Kontonamen und wird beim Kontowechsel nicht zurückgesetzt. Beim Wechsel Sim101 → Simtestsim2 (03.08. 23:19) hat Simtestsim2 deshalb **peakBalance UND initialBalance = 103.046,5** von Sim101 geerbt, obwohl es bei 100.000 startet. Zwei reale Folgen, beide im Log belegt:
  1. **Floor 100.546 statt 97.500** → Cushion ~279 statt 2.500 → **Size dauerhaft 1 statt ~6** (Log 04.08.: „Cushion 523 | Size 1", davor Sim101 „Cushion 2500 | Size 6").
  2. **Eval-Ziel unerreichbar:** die Prüfung ist `NetLiq − initialBalance ≥ 3.000`, mit initial=103.046 bräuchte es NetLiq **106.046 statt 103.000** — rund 3.000 $ zu hoch.
  → **Die Generalprobe auf Simtestsim2 ist seit dem 04.08. nicht aussagekräftig** (falsche Größe, falscher Käfig, falsches Ziel). Das ist der teurere Bug; der Journal-Anzeigefehler war nur das Symptom, das auffiel.
- **⚠️ Zweiter Prozess-Fund:** Auf dem VPS lag bereits eine **neuere** `MaxRiskGuard.cs` als im lokalen Repo — mit dem 3-Spalten-Equity-Fix **und** `CushionFrac = 0.22`. Sie wurde nur **nie kompiliert**. Daher schrieb der laufende Guard weiter 2 Spalten, daher verwarf der Server alles. **Der ganze Journal-Bug hängt an einem offenen F5-Ticket.** Zusatzrisiko dabei entdeckt: das lokale Repo war auf `CushionFrac = 0.14` — ein blinder Upload hätte den Betriebspunkt aus #045 stillschweigend zurückgesetzt. **Vor jedem NinjaScript-Deploy erst den VPS-Stand ziehen und diffen, nie lokal-nach-remote ohne Vergleich.**
- **Umgesetzt am 05.08.:** (1) Server ordnet 2-spaltige Zeilen jetzt über das Fill-Log dem Konto zu, das an dem Tag lief (Sim101 und Simtestsim2 wieder sauber getrennt), State-Peak wird bei mehreren Konten ignoriert, und jeder Fallback erzeugt eine **sichtbare Warnung im Journal** statt still zu passieren. (2) RiskGuard-C# um Konto-Check in der State-Datei erweitert (4. Feld) + Alt-Equity-Zeilen überleben den Format-Wechsel. Liegt deployed auf dem VPS, **Backup `MaxRiskGuard.cs.bak-20260805`, wartet auf F5 nach Session-Ende**.
- **Lehre für die Insight-Bank (Ops):** Ein strengeres Parsing ohne Anpassung des Schreibers ist **schlimmer als gar kein Fix** — es kippt still in einen falschen Fallback. Silent-Fallbacks sind gefährlicher als harte Fehler. Und: Zustand, der zu einem Konto gehört, muss den Kontonamen tragen, sonst wandert er beim Wechsel unbemerkt mit.

## #059 — 🎫 Tickets-Tab im Lab: Aufgaben mit Zeitfenster statt nur Prio (05.08.2026)
- **Max' Anforderung:** eigener Tab neben Journal, der nicht nur zeigt *was* ansteht, sondern **wann es überhaupt geht** (Beispiel: F5-Compile darf nicht während der Session laufen), mit Detailansicht je Ticket und Prio-Ranking.
- **Neues Schema-Feld `when`** in `tasks.json` (5 Zeitfenster): `sofort` (jederzeit) · `nach-close` (nur nach 22:00 dt. / Wochenende, alles was ins Live-System greift) · `vor-open` (vor 15:30) · `werktags` (Behörde/Bank, Mo-Fr 8-18) · `ruhig` (kein Fenster). Dazu `when_note` (warum dieses Fenster) und **`blocked_by`** für Abhängigkeiten zwischen Tickets.
- **Der Tab rechnet live:** aus der aktuellen Uhrzeit + dem Zeitfenster + offenen Blockern ergibt sich pro Ticket „JETZT MÖGLICH" oder „wartet". Zwei Sektionen (✅ Jetzt möglich / ⏳ Wartet), innerhalb nach Prio sortiert, erledigte eingeklappt darunter. Kopfzeile zeigt an, ob gerade Handelssession läuft. Badge im Topnav = Anzahl der **roten** Tickets, die jetzt machbar sind (kein Dauer-Alarm für Dinge, die eh warten müssen).
- **Detailansicht** je Ticket aufklappbar: Zeitfenster + Begründung, Blocker, vollständiges „Warum", nummerierte Schritte aus `guide`, Erledigen-Knopf. Neue Tickets lassen sich direkt im Tab mit Prio **und** Zeitfenster anlegen (`/api/tasks/add` um `when` erweitert).
- **Alle 13 offenen Tickets nachgerüstet.** Effekt sofort sichtbar: die beiden roten Live-System-Tickets (F5-Compile, Journal-Abnahme) rutschen korrekt nach „wartet", weil RTH lief; die 4 Steuer-Tickets stehen als sofort machbar oben.
- **Test:** JS des gesamten Hubs mit esprima gegengeparst (nach Normalisierung von `?.`/`??`, die der Parser nicht kennt) → syntaktisch sauber. Wichtig, weil der Hub **einen** Script-Block hat: ein Syntaxfehler im neuen Tab hätte alle Tabs lahmgelegt. Timing-Logik zusätzlich mit den echten Ticketdaten in Python nachsimuliert.
- Backups: `app_server.py.bak2-20260805`, `tasks.json.bak2-20260805`.

## #060 — E8-Tax-FAQ gefunden: W-8BEN liegt bei WorkMarket/Riseworks, nicht bei E8 (05.08.2026)
- **Max hat E8s eigenes FAQ „Tax, 1099, W-8" gefunden** (Stand 09.03.2026). Bestätigt: Traders sind **Independent Contractors**, KYC nur mit eigenem legalen Namen, **kein Firmenkonto möglich** — deckt sich mit der bisherigen Einschätzung.
- **Korrektur an Ticket `w8ben-check-e8`:** Das W-8-Formular liegt nicht im E8-Dashboard, sondern wird über die Payout-Prozessoren **WorkMarket oder Rise/Riseworks** bereitgestellt und dort ausgefüllt. Ticket im Lab entsprechend korrigiert (richtige Anlaufstelle, Abgleich Name/Adresse über alle drei Plattformen).
- 1099-Prozess betrifft nur US-Residents, für Max zählt nur der W-8-Teil.

## #061 — W-8BEN-Frage final geklärt: läuft automatisch beim ersten Payout (05.08.2026)
- **E8-Support bestätigt:** Kein Prozessor ist vorher im Dashboard sichtbar. Ablauf: Payout anfordern → E8 weist automatisch WorkMarket oder Rise zu + schickt Einladungslink → im dortigen Onboarding werden KYC + Steuerformulare (W-8BEN für internationale Trader automatisch bereitgestellt) ausgefüllt. Aeropay (aus den ToS) ist dafür nicht relevant, das ist nur der ACH-Layer.
- **Konsequenz:** Ticket `w8ben-check-e8` als erledigt geschlossen (nichts vorab zu tun, keine Verspätungsgefahr). Neuer leichter Reminder `w8ben-onboarding-beim-payout` (🟢, kein Zeitdruck) angelegt für den Moment des ersten echten Payout-Requests — einziges Restrisiko ist, den Einladungslink zu übersehen oder das Onboarding nicht vollständig abzuschließen.

## #062 — Tickets-Tab: 5-stufiger Arbeitsstatus statt nur offen/erledigt (05.08.2026)
- **Max' Wunsch:** pro Ticket selbst umschalten können zwischen Zu erledigen → In Arbeit → Prüfen → Warte auf Rückmeldung → Erledigt, nicht nur als Text notiert, sondern als echte Bedienung im Tab.
- **Umsetzung:** neues Feld `workflow` (4 Werte, getrennt vom bestehenden `status` offen/erledigt, der weiterhin die Jetzt/Wartet-Logik + Blocker-Kette steuert). Jede offene Ticket-Karte zeigt jetzt ein Dropdown direkt im Header (auch eingeklappt sichtbar), Auswahl ruft `/api/tasks/setworkflow` auf und schreibt sofort in `tasks.json`. „Erledigt" bleibt bewusst separat über den bestehenden grünen Knopf (mit Verifikation), taucht nicht im Dropdown auf.
- **Übersicht ergänzt:** zwei neue Zähler oben im Tab, „In Arbeit" und „Warte auf Rückmeldung", damit der Stand auf einen Blick sichtbar ist.
- **Alle 12 offenen Tickets migriert** auf Start-Status „Zu erledigen". Getestet: Statuswechsel + Persistenz + Ablehnung eines ungültigen Werts, JS-Gesamtsyntax erneut gegen esprima geprüft.
- Backups: `app_server.py.bak3-20260805`, `tasks.json.bak3-20260805`.

## #063 — Abnahme F5 #1 erfolgreich, dabei zweiten (schlimmeren) Bug gefunden (05.08.2026)
- **Erste Abnahme:** Max hat Strategien komplett entfernt + neu hinzugefügt + F5 kompiliert. Log zeigt jetzt korrekt `STATE VERWORFEN: gespeichertes Konto 'Sim101' != aktuelles 'Simtestsim2'` → Peak/Initial für Simtestsim2 sauber neu auf den echten NetLiq (~100.923) gesetzt, **Cushion zurück auf 2.500, Size zurück auf 6**. Der State-Bug aus #058 ist behoben.
- **🚨 Beim Gegenchecken zweiten, schwereren Bug gefunden:** `OnBarUpdate()` hatte keine Sperre gegen die historische Bar-Wiedergabe, die NinjaTrader beim (Neu-)Anhängen einer Strategie immer erst durchspielt. Der RiskGuard lief dabei mit voller Logik auf JEDER historischen Bar mit, aber `NetLiq()` liefert immer den aktuellen Live-Kontostand, nie den echten historischen Wert. Sichtbar: `maxlab_equity.csv` wurde für **jeden** historischen Tag mit dem heutigen Wert überschrieben (Sim101 überall 103.046,5, Simtestsim2 überall 100.922,5 — echte Tageshistorie weg). **Gefährlicher:** `FlattenAll()` arbeitet auf den echten `acct.Positions` — hätte die Eval-Target- oder Tagesverlust-Bedingung während der Wiedergabe zufällig angeschlagen, wären echte Flatten-Befehle rausgegangen, ausgelöst durch reine Chart-Historie statt Marktgeschehen. Diesmal nichts passiert, aber das war Zufall, keine Absicherung.
- **Sofort behoben:** `maxlab_equity.csv` auf dem VPS bereinigt (die 10 kaputten Zeilen raus, die echte Alt-Historie stand unverändert oben in der Datei und ist wiederhergestellt — nichts verloren). Code-Fix `if (State == State.Historical) return;` ganz am Anfang von `OnBarUpdate()`, VPS-Diff sauber (nur meine Ergänzung), deployed, Backup `MaxRiskGuard.cs.bak-20260805b`. Neues Ticket `riskguard-historical-replay-guard-f5` (🔴) wartet auf den nächsten F5-Zyklus.
- **Lehre:** Ein "harmloser" Remove-and-Readd zum Testen eines Fixes deckte einen zweiten, unabhängigen Bug auf, der seit dem allerersten Deploy im Code lag und nur nie getriggert wurde, weil die Strategie seit dem 04.08. durchgängig lief. Jede künftige Strategie, die auf Live-Kontodaten reagiert (Equity schreiben, Flatten, Limits), braucht diesen `State.Historical`-Guard von Anfang an, nicht erst wenn ein Restart ihn zufällig auslöst.

## #064 — Tickets-Tab: Scroll-Bug + Emojis raus (05.08.2026)
- **Scroll ging nicht:** `#ticketsview` fehlte in der CSS-Regel (`flex:1;min-height:0` + `overflow:auto`), die Journal/Idea/Live erst eine begrenzte, scrollbare Höhe im Flex-Layout gibt. Ohne die schneidet der Body-Container (selbst `overflow:hidden`) den Inhalt einfach ab. Ergänzt, Tab scrollt jetzt normal.
- **Emojis komplett raus** aus dem neuen Tickets-Tab (Tab-Label, Status-Badges, Prio-Auswahl, Zeitfenster, Erledigt-Button) auf Max' Wunsch — nur die funktionalen Auf-/Zuklapp-Pfeile (▸▾) blieben, kein Emoji. Bewusst NICHT angefasst: die bereits bestehenden Emojis im Rest des Lab (Journal, Idea Engine, Edge-Health), das war vorher schon so und nicht Teil des neuen Tabs — Rückfrage an Max, falls das auch bereinigt werden soll.
- Backup: `app_server.py.bak4-20260805`.

## #065 — MaxORBBreakoutNQ „Order rejected": invertiertes Bracket durch `Math.Abs` (09.08.2026)
- **Symptom (07.08., Freitag):** NT8-Fehlerdialog „Strategy MaxORBBreakoutNQ submitted an order that generated the following error 'Order rejected'. Strategy has sent cancel requests, attempted to close the position and terminated itself." Bein 3 war den Rest des Tages tot.
- **Beweiskette aus den Live-Logs** (`maxlab_orders.csv` + `bars_MNQ.csv`, beide auf der Box mitgeschrieben): OR 09:31-09:45 → orHigh 29813, orLow 29683, orSize 130 → Stop = 29813 − 0,4·130 = **29761**. Breakout-Bar 09:46: High **29821,75** (Level gebrochen), Close aber **29756,50** — also 56 Punkte zurück, **unter den Stop**. Order-Log: Stop 29761 `Rejected`, Profit target 29763,25 `Rejected`, Fill des Entries 09:47 long @29756,50. Target-Preis exakt reproduzierbar aus `Close + 1,5·|Close−Stop|` = 29763,25. ✅ eindeutig.
- **Root Cause:** `double risk = Math.Abs(Close[0] - stop);` — das `Math.Abs` verschluckt das Vorzeichen. Schließt die Ausbruchs-Bar wieder **hinter** dem Stop-Level, ist der Stop für einen Long plötzlich **über** dem Entry. Die Strategie hat trotzdem gekauft und ein invertiertes Bracket rausgeschickt (Sell-Stop über Markt = ungültig) → Reject → NT-Default `RealtimeErrorHandling.StopCancelClose` schaltet die Strategie ab.
- **Fix (deployed auf die Box, wartet auf F5):** vorzeichenbehaftetes Risiko `dir * (Close - stop)` + Mindestabstand `MinRiskTicks` (default 8 Ticks) → solche Bars werden übersprungen. Zusätzlich `RoundToTickSize` auf Stop/Target und ein eigener `OnOrderUpdate`-Reject-Handler (selbst flatten + Tag sperren) mit `RealtimeErrorHandling.IgnoreAllErrors`, damit ein Reject nie wieder ein ganzes Bein für den Tag killt. Gleiches Muster in **allen 8 Beinen** nachgezogen (Scalp/Scalp2 identisch betroffen, Fade spiegelverkehrt, GapFade beim Target).
- **Häufigkeit gemessen** (NQ 1m, 2016-2025, 2.555 Ausbruchstage): 35 Tage roh, nach Vol+VWAP-Filter **8 Tage** hätten den neuen Guard ausgelöst. Backtest-Ausgang dieser 8 Tage: **8× Stop**. Der Guard kostet also keinen einzigen Gewinntrade, er überspringt exakt die Tage, die ohnehin −1R waren.
- **Verifikation:** Alle 8 .cs mit `csc.exe` gegen die echten NT8-Assemblies auf der Box gegengeprüft (`_check_compile.ps1`, Wegwerf-DLL, NT nicht angefasst) → „COMPILE OK". Rollback-Backups: lokal `engine/ninjascript/bak-20260809-prerejectfix/`, auf der Box `C:\Users\Administrator\_bak_prefix_20260809`.
- **Lehre:** `Math.Abs` auf einer Distanz, die eine Richtung hat, ist ein Bug-Generator. Bei jedem Bracket gilt ab jetzt: **Stop und Target müssen explizit gegen die Entry-Seite geprüft werden**, bevor die Order rausgeht — nicht nur „Abstand > 0". Und: ein Reject darf nie ein Bein für den Tag abschalten, dafür gehört in jede Strategie ein eigener Reject-Handler.

## #066 — 🚨 Dabei gefunden: NinjaScript-Port der ORB-Beine entspricht nicht dem Backtest (09.08.2026)
- **Der eigentliche Fund.** Beim Nachrechnen des Bugs fiel auf: `qbt._orb_trades()` setzt `entry = max(level, o[i0])` — **Entry am OR-Level** (Stop-Order-Logik, Fill mitten in der Bar). Der NinjaScript-Port handelt dagegen `Calculate.OnBarClose` + Market-Order = **Entry am Close der Ausbruchs-Bar**. Am 07.08. waren das 29813 (Backtest) vs. 29756,50 (Live) — 56 Punkte Unterschied, und R wird aus einer völlig anderen Basis gerechnet.
- **Messung auf NQ 1m 2016-2025** (gleiche Parameter, gleiche Filter, nur Entry-Definition getauscht):

| Bein | Backtest (Level-Entry) | Live-Logik (Close-Entry) |
|---|---|---|
| Bein 3 ORB-Breakout T1.5R | expR **+0,162** · Win 46,7% | expR **+0,013** · Win 40,3% |
| Bein 8 ORB-Scalp T1.0R | expR **+0,251** · Win 62,5% | expR **+0,027** · Win 51,2% |
| Bein 9 ORB-Scalp2 T0.5R | expR **+0,219** · Win 81,3% | expR **+0,038** · Win 69,2% |

- **Das ist mehr als die ±20%-Toleranz aus [[Live-Setup (Algo auf Prop)]] Phase 2 — das ist ~85-90% der Edge.** Betrifft 4 von 9 Beinen (3, 4, 8, 9).
- **Und der Level-Entry im Backtest ist selbst nicht sauber:** der Volumen- und der VWAP-Filter werten die **komplette** Ausbruchs-Bar aus (Volumen der ganzen Minute, VWAP auf deren Close), der Fill passiert aber schon vorher am Level. Das ist Look-ahead. Gegenprobe ohne Bar-Close-Filter, Level-Entry (ehrlich implementierbar als ruhende Stop-Order): Bein 3 expR +0,029 / 1.303 Trades, Bein 8 +0,049 / 2.543 Trades — kleine, aber echte Edge auf großer Stichprobe.
- **Heißt:** die schönen Buch-Zahlen der ORB-Beine leben zu einem großen Teil von der Filter-Zeitpunkt-Unschärfe. Die Passquote-Rechnung (61% / ~81 Tage) ist damit für die ORB-Anteile zu optimistisch, solange das nicht geklärt ist.
- **Entscheidung offen (Max):** (a) Live auf ruhende Stop-Entry-Order am Level umbauen + Filter ehrlich machen (tick-basiertes RVOL bis zum Break, VWAP der Vorbar) und neu bewerten, oder (b) den Backtest auf Close-Entry umstellen und die Beine mit den ehrlichen, deutlich kleineren Zahlen neu durch die Frontier schicken. **Vor dem Live-Gang muss das geklärt sein** — nicht der Reject-Bug ist der Blocker, sondern das hier.

## #067 — #066 GEFIXT: ORB-Breakout-Beine ehrlich tot, Buch auf 6 Beine, Fade auf Limit-Orders (09.08.2026)
- **Werkzeug zuerst:** `qbt._orb_trades()` kann jetzt drei Exec-Modi (`orb_exec`): `book` (Legacy, Look-ahead), `close` (Entry am Close der Ausbruchs-Bar = bisherige Live-Logik, Filter ehrlich, inkl. #065-Guard), `stop_honest` (Level-Fill via ruhende Order, Filter nur mit Vorbar-Infos → live 1:1 baubar). Regression: `book` reproduziert die alten Zahlen exakt.
- **Messung NQ 1m 2016-2026 (netto, inkl. Kosten), alle ehrlichen Varianten der Breakout-Beine:**

| Bein | book (Illusion) | close (Live-Logik) | stop_honest Vorbar-Filter | Level ohne Filter | Vorbar-RVOL 1.1/1.3 |
|---|---|---|---|---|---|
| 3 Breakout T1.5 | +0,091 | **−0,091** | −0,239 (n=35) | −0,051 (n=1365) | −0,065 / −0,120 |
| 8 Scalp T1.0 | +0,173 | **−0,040** | +0,159 (n=34, kein OOS) | −0,013 (n=2673) | +0,003 / +0,013 |
| 9 Scalp2 T0.5 | +0,142 | **−0,030** | +0,026 (n=34) | −0,023 (n=2673) | −0,004 / +0,025 |

- **Verdikt: kein ehrlicher Weg rettet die Breakout-ORBs.** Die #066-Restedge (+0,03/+0,05) war brutto; netto ist alles ≤0 oder n=34-Rauschen. Die Vorbar-Vol-Filter matchen fast nie (der Volumenspike IST die Ausbruchs-Bar).
- **Bein 4 (Fade) ist echt:** `book` == `stop_honest` identisch (+0,063, OOS +0,78) — Entry am Level ist als ruhende Limit-Order ehrlich umsetzbar. Die bisherige Live-Logik (Close-Entry) lieferte davon nur +0,019.
- **Passquoten-Wahrheit (E8-Käfig 3000/2000 trailing, 5000 Sims):** book9 **61%/81d** (reproduziert, aber Illusion) · live9 (Close-ORBs, was das Buch WIRKLICH tat) **56%/78d** · **ohne die 3 Breakout-ORBs: 57%/86d** · ohne alle 4 ORBs 55%/88d.
- **Entscheidung (beste Option für Eval-Passing):** **Buch = 6 Beine** (Momentum, LastHour, RTY-Gap-fade, ORB-fade, Asia-Dir, RV-leadlag). Die 3 Breakout-ORBs fliegen raus: gleiche/bessere ehrliche Passquote als sie drin zu lassen, minus 3 Beine mit netto NEGATIVER Erwartung (kosten real Geld, liefern nur Varianz) und minus Betriebskomplexität. Simplex beats Komplex.
- **Umgesetzt:** `book_state.json` auf 6 Beine (Backup `book_state.json.bak-20260809-pre066`), Portfolio-Report neu gebaut, `MaxORBFadeNQ.cs` auf ruhende Limit-Orders an beiden OR-Leveln umgebaut (erster Fill gewinnt, Gegenorder storniert, Stop 0,4×OR jenseits Level; Backup `ninjascript/bak-20260809-pre066fix/`). Mess-Skripte: `orb_honest_066.py`, `orb_honest_frontier_066.py` (+ JSONs).
- **Offen (Tickets 🔴):** auf der Box B3/B8/B9 aus NT8 entfernen + Fade-Port compile-checken (`_check_compile.ps1`) und per F5 deployen. Danach Phase-2-Sim-Abgleich für den neuen Fade-Entry.
- **Lehre:** Filter, die auf der Ausbruchs-Bar rechnen, während der Fill am Level passiert, sind strukturelles Look-ahead — ab jetzt gilt für jede Intrabar-Entry-Strategie: **Filter dürfen nur Infos verwenden, die zum Order-Platzierungszeitpunkt existieren.** Und: Passquoten immer auf der Exec-Logik rechnen, die live wirklich läuft.

## #068 — Intensive ehrliche ORB-Forschungsrunde: das Kapitel ist jetzt wirklich geklärt (09.08.2026)
Max' Auftrag nach #067: ORB nochmal richtig ernst nehmen — Literatur (Scholar/SSRN/ResearchGate) + alles ehrlich durch die Engine, keine alten Fehler. Live-Gang verschoben, Sim läuft weiter.

**Werkzeug-Ausbau (alles regressionsgetestet):** `orb_exec="retest"` (ruhende Limit am Level nach Close-Confirm), `or_rvol_min` (OR-Volumen ehrlich VOR Orderplatzierung), `vix_band` (absolutes Vortages-VIX-Band), neuer Modus `noise_orb` (Zarattini SSRN 4824172: Band = max(Open,PrevClose)±σ(t) aus 14-Tage-Punktekurve, 30-Min-Checks, VWAP-Trail, EOD).

**Die Kern-Erklärung (Zerlegung, 2.685 NQ-Ausbruchstage):** Nach dem ORB-Break gibt es KEIN Follow-Through — Ausbruchs-Bar +1,1 Pkt, danach bis EOD −0,6 Pkt (51% = Coinflip), auch mit Trend/Spike-Kondition. Die alte "Edge" waren +6,4 Pkt IN der Spike-Bar (nur per Look-ahead erntbar). Gegenprobe: Momentum-Displacement ≥0,3%/15min hat +13,6 Pkt echten Drift (56%) — „früher Impuls → Tages-Run" existiert, lebt aber im Momentum-Bein, nicht im Linien-Break.

**Ehrlich getestet und verworfen:**
- 152-Varianten-Discovery (close-Entry, Tages-Run-Exits): NR7-EOD-Varianten sahen stark aus (+0,33, IS+OOS positiv) → beim genauen Hinsehen **Tail-Lotterie**: Top-5 Trades 46-111% des Gesamt-R, 2025-26 negativ (−1.900$). Multiple-Testing-Falle par excellence, dokumentiert als Warnung.
- **Pineda-Retest: zweite ehrliche Falsifikation** (36 Varianten, echter Touch-Fill): OOS/2025+ durchweg negativ.
- **"Index in Play"** (OR-RVOL, ehrlicher Ersatz für den Look-ahead-Vol-Filter): überträgt sich NICHT von Aktien auf Index-Futures.
- Zarattini-STD roh (5m-Confirm/first-candle): PF ~1,05-1,08, IS ≈ 0 — deckt sich mit #044.

**Zwei echte Funde (beide Bank/Prop-Valide, Auto-Fit lehnt fürs Buch ab):**
- **`ORB_VIXBAND_NQ`** (C/56): Chuk-Faktor repliziert — close-EOD-ORB expR **+0,10 im VIX-Band 15-25** vs 0,00 außerhalb, 8/11 Jahre, Nachbarn robust, 2024-26 stärkste Phase. Wochentags-Faktor überträgt nicht. Auto-Fit: 57%/86d → 50%/58d = abgelehnt.
- **`NOISE_ORB_NQ_m1.0`** (C/68, Paper-Default ohne Tuning): expR +0,094, **IS +0,094 = OOS +0,097**, 9/11 Jahre positiv, Top5 nur 29%, ~180 Tr/Jahr, MaxDD −5k$/Micro. Auto-Fit: 57%/86d → 52%/53d = abgelehnt (Zeit-bis-Funded-EV ~gleich wie Buch @0.22). **Stärkster ehrlicher ORB-Verwandter, den es auf NQ gibt.**

**Verdikt:** Das Buch bleibt bei 6 Beinen. Der klassische Breakout-ORB auf Index-Futures ist als Familie ehrlich zu Ende geforscht: übrig bleiben Fade (im Buch), VIX-Band-Kontext und Noise-Band (Bank, bewusste Speed-Optionen falls Max Quote gegen Tempo tauschen will). Doku: Research-Cache #068-Block, ORB Master-Synthese korrigiert.

**Lehren:** (1) IS+OOS-positiv reicht nicht — immer Konzentration (Top-5-Anteil), Jahres-Stabilität und 2025+-Fenster prüfen. (2) Ein Paper-Prior (VIX-Band, Noise-Band) ist mehr wert als 100 gegridete Filter. (3) Aktien-Mechanismen (Attention/in Play) übertragen sich nicht automatisch auf Index-Futures.

## #069 — Video-Backtest: Matteo Coni „Drift VWAP Pullback" (Prop Firm Golden Ticket) (09.08.2026)
Max' Auftrag: YouTube-Interview (Matteo Coni, Ex-Market-Maker Nordea, SQR Capital) per Transkript analysieren + Strategie ehrlich nachtesten. Video: youtube.com/watch?v=wm4A6qo0g3I. Familie: **Trend Following (intraday)**. Skript: `engine/matteo_vwap_drift.py`, Trades: `matteo_vwap_trades.csv`.

**Regeln (vollständig aus dem Interview extrahierbar):** NQ, Session-VWAP (Anker 9:30 ET). Bias alle 15 min: Long = Preis>VWAP + VWAP steigt (vs. 15 min zuvor) + Preis +0,1%/1h (Short spiegelbildlich). Trigger: erste Gegenfarb-5-min-Kerze → Market am nächsten Open. Long TP 40/SL 80, Short TP 50/SL 80. Kein Trade 9:30–10:30, max 4 Trades/Tag, Stop nach 2 Verlusten, keine Entries nach 15:30, flat 15:55.

**Replikation = Volltreffer.** Seit 2021 ~3.950 Trades (er: „4.000+"), OOS 24–26: Win 63,6% (er 64%), Ø-Win $861 (er $866!), Ø-Loss $1.334 (er $1.300). Die Strategie ist also exakt die, die er zeigt — keine versteckten Regeln.

**Ehrliches Ergebnis (Kosten: 1 Tick/Seite + $1,02 RT):**
- Edge echt, aber **dünn**: expR +0,018–0,027, PF 1,05–1,09, Win nur +1,5–2pp über Breakeven-Baseline. Netto seit 2021 ~$140k/NQ. Exit-Mix: 49% Target, 28% Zeit, 22% Stop (Zeitexits drücken Ø-Loss unter die 80-Pkt-Marke).
- **Pre-Sample 2016–2019 (hat ER nie gesehen): 2016/17/19 negativ**, erst ab 2020 konsistent; 2022 flat (−3k). 2023–2026 stabil ~+30k/Jahr/NQ → Edge ist regime-abhängig (High-Vol-Trend-Ära), aber zuletzt 4 Jahre in Folge positiv.
- **Pass-Rate-Claim entzaubert:** Seine ~50%/Eval (93,6% in 4) reproduziert sich NUR mit Close-only-Equity (unsere Nachbau-Sim: 43%/89,5%). Mit ehrlichem **Intraday-Trailing-DD via MAE: Apex 50k mit 1 NQ nur 23–27%, mit 4 MNQ ~33%**. Sein „Golden Ticket" ignoriert, dass der Trailing-DD intraday zieht — Faktor ~2 zu optimistisch, 1 NQ auf 50k (Risiko $1.600/Trade bei $2.500 DD) ist massiv übersized.

**Verdikt: kein Buch-Kandidat.** P(pass) 33% < 40%-Gate, expR-Qualität auf #060-Niveau (schwache Trades verwässern, Lehre: Korrelation allein reicht nicht). Dein 6-Beine-Buch (61%/81d, Solo-Beine bis 72%) schlägt das klar. Aber: der Typ ist kein Scammer — seine Backtest-Zahlen stimmen, nur seine Prop-Simulation ist naiv.

**Lehren:** (1) Insight #6 bestätigt: hohe Win-Rate + RR<1 ist der richtige Eval-Ansatz — aber ohne Intraday-DD-Modellierung sind Pass-Raten Fantasie. (2) VWAP-Drift-Pullback (Continuation!) passt zu Insight #1 (Continuation statt Reversion an der VWAP) — der Mechanismus ist real, nur zu schwach pro Trade. (3) Video-Strategien ab jetzt immer: Transkript → Regeln → `qbt` → Close-only vs. MAE-Sim vergleichen, um Marketing von Substanz zu trennen.

## #070 — ORB-Runde 2: der gesuchte Fund war nicht da, der ungesuchte schon (09.08.2026)
Max' Auftrag: ORB-Lage komplett anschauen, selbst Strategien suchen, mit Agents recherchieren, eigene Entwicklung. Hypothesen **vorab fixiert** in [[ORB-Runde 070 (Hypothesen vorab)]] (H1-H5, jede mit Kill-Kriterium), erst danach ein Backtest. Skripte: `orb070_noise.py`, `orb070_fade.py`, `orb070_book_stress.py`.

**Leit-These der Runde:** In unseren eigenen Daten steckt ein Widerspruch — Linien-Break hat kein Follow-Through (#068), Momentum-Displacement ≥0,3%/15min hat +13,6 Pkt echten Drift. Der Unterschied ist der Trigger-Typ: ein Level sagt nichts über die *Größe* der Bewegung, ein vola-normiertes Band schon. Daraus: *was am ORB noch zu holen ist, holen wir über die Normierung, nicht über bessere Linien.*

### 🚨 Der Hauptfund (nicht gesucht, aus H3 herausgefallen): Bein 4 ist eine Regime-Wette
Beim Messen der Fade-„Latte" fiel auf, dass der Buch-Fade selbst das Discovery-Gate verletzt:

| Fenster | n | brutto | netto | mean R_pts | Win |
|---|---|---|---|---|---|
| IS 2016-2023 (8 Jahre) | 319 | +739$ | **+95$** | 18,3 | 17,2% |
| OOS 2024-2026 (2,5 J) | 103 | +5.880$ | **+5.672$** | 36,3 | 29,1% |

- **Acht Jahre lang netto Null**, danach der komplette Ertrag. Auch *brutto* war im IS fast nichts — es ist kein reines Kostenproblem.
- **Tail:** Top-5 von 422 Trades = 74% des Netto-Gewinns, **Top-10 = 127%** (ohne sie ist das Bein negativ). Exakt das Muster, das #068 bei den NR7-EOD-Varianten als „Tail-Lotterie" gekillt hat — nur saß es diesmal im Buch.
- **Richtungs-Asymmetrie kippt:** 2016-2021 ist der LONG-Fade besser (−0,190 vs −0,268), ab 2023 der SHORT-Fade (+0,837 vs +0,434). Die Asymmetrie ist keine Struktur, sie ist dasselbe Regime-Artefakt.
- **Warum es #067 durchrutschte:** dort wurde auf `book == stop_honest` und OOS +0,78 geschaut. Der IS-Wert (−0,168) stand nie in der Bewertung.

### 🔬 Der Stresstest, der daraus folgte: Passquoten fenstergetrennt
Erstmals die Buch-Frontier **nicht nur über die volle Historie**, sondern getrennt für IS und OOS gerechnet (`orb070_book_stress.py`):

| Szenario | VOLL | IS 2016-23 | OOS 2024-26 | avg\|corr\| |
|---|---|---|---|---|
| **buch6 (heute)** | **57%/86d** | **51%/117d** | **63%/46d** | 0,069 |
| buch5 ohne Fade | 55%/88d | 52%/118d | 57%/48d | 0,085 |
| buch6 + Noise-ORB | 52%/53d | 53%/68d | 53%/31d | 0,112 |
| buch5 Fade→Noise getauscht | 51%/54d | 52%/73d | 49%/31d | 0,142 |

- **Die 57% sind keine Eigenschaft des Buchs, sondern des Fensters.** Im IS-Fenster wären es 51%/117d gewesen.
- **Bein 4 trägt ausschließlich im OOS.** Im IS macht es das Buch sogar um einen Punkt *schlechter* (51 vs 52).
- **Fade rauswerfen ist trotzdem nicht die Antwort:** buch5 ist in VOLL und OOS schlechter, im IS nur minimal besser. Es gibt keine dominante Variante.
- **Der Noise-ORB stabilisiert:** 53/53 über beide Fenster statt 51/63, und ~40% schneller. Genau das kann der Auto-Fit strukturell nicht sehen, weil er nur die volle Historie bewertet.

### Die vorab fixierten Hypothesen — Ergebnis
- **H1 (Noise × VIX-Band) ❌ falsifiziert.** Das Chuk-Band 15-25 hebt den IS-expR massiv (0,094→0,189), aber OOS bricht ein (0,034) — und die **Gegenprobe „außerhalb des Bands" ist OOS besser** (0,235), in 8 von 10 Band/Instrument-Kombinationen. 2025+ im Band negativ, außerhalb positiv. Die Gegenprobe war der entscheidende Testbaustein; ohne sie hätte die Zelle „IS+OOS positiv, expR 0,14" ausgesehen und wäre durchgegangen. **Mechanismus vom Auditor nachgerechnet:** corr(trailing-σ, Vortages-VIX) = 0,44, Median-σ im Band 79,5 vs. 43,2 Pkt außerhalb → **der VIX ist hier nur ein Vola-Proxy, kein unabhängiger Kontext-Faktor.** Chuks Dealer-Hedging-Story trägt auf dem Noise-ORB nicht.
- **H2 (Noise-Band auf ES/RTY/YM) ⚠️ teilweise.** NQ hält sauber (IS +0,094 ≈ OOS +0,097, 10/11 Jahre, top5 nur 0,29 — der beste Ehrlichkeitswert im ganzen Lauf). Aber **RTY tot** (IS und OOS negativ, 3/10 Jahre), **YM praktisch tot** (IS negativ, OOS +0,008 = Rauschen), **ES fraglich** (formal positiv, aber top5 0,55 und 2025+ negativ). Der Mechanismus generalisiert **nicht** — er ist NQ-spezifisch. Das formale Kill-Kriterium (≥2 von 3 OOS-negativ) ist knapp nicht erfüllt, qualitativ aber schon.
- **H3a (Fade × VIX) ❌ Vorab-These widerlegt.** Erwartet war „Fade lebt bei niedrigem VIX". Gemessen ist es **umgekehrt**: vix10-18 ist die schwächste Zelle (4/11 Jahre), vix15-25 und vix18-32 laufen besser. Ohne NR7-Filter ist über alle Bänder alles negativ — **der NR7-Filter trägt den kompletten Fade-Edge**.
- **H3b (Richtungs-Asymmetrie) ⚠️ nur scheinbar bestätigt.** Über die volle Historie ist der SHORT-Fade 20× stärker (+0,114 vs +0,006), was Grant/Wolf/Yu stützen würde — aber die Zerlegung nach Regime zeigt, dass die Asymmetrie vor 2022 ins Gegenteil kippt. Kein tragfähiger Befund.
- **H3c (R/σ-Terzile) 💀 toter Test, mein Bug.** `sigma_entry` wird im ORB-Zweig auf `or_size` gesetzt, `R_pts` ist `stop_frac × or_size` — der Quotient ist **per Konstruktion konstant 0,4** (nunique=1, std 1,9e-14). Die drei „Terzile" waren eine Zufallspartition nach Float-Rundungsfehler, die gemessenen expR-Unterschiede reines Rauschen. Vom strategy-auditor gefunden, selbst nachgerechnet und bestätigt.
- **H4 (Exits) ❌ kein Gewinn.** T1.0 ist über alle 12 Zellen schlecht (Win-Rate **unter** Baseline, edge_pp −6,7). T0.5 hebt die Win-Rate real über Baseline (+2 bis +8pp, konsistent über alle Bänder), aber der expR bleibt in den starken Zellen unter EOD. Der Exit-Hebel aus dem Discovery-Prozess wirkt hier nicht.
- **H5 (volle Frontier statt Betriebspunkt) ✅ bestätigt und relevant.** Siehe Tabelle oben — die #068-Ablehnung des Noise-ORB ist am Betriebspunkt korrekt, aber sie verdeckt, dass er das Buch **fensterstabil** macht.

### Literatur (research-scout, Cache-Block #070)
Ein Fund: **Grant/Wolf/Yu 2005 (J. Banking & Finance, SSRN 689282)** — Intraday-Reversal nach großen Opening-Moves in US-Index-Futures, signifikant 1987-2002, stärker nach positiven Open-Moves; Signifikanz bricht bei Bid-Ask-Kosten ein. Stützt den Fade-Zweig grundsätzlich, hat sich in H3b aber nicht als handelbare Struktur bestätigt (Sample endet 2002 → gleiche Post-Publication-Kategorie wie das im_ll-Debakel aus #056).
Drei Sackgassen, damit dort nie wieder gesucht wird: **Zarattini/Concretum hat 2025/26 nichts Neues zu ORB** (weitergezogen zu GTAA/Vol-Targeting/Krypto) · **„Turtle Soup"/Liquidity-Sweep am OR-Level = reine Retail-Folklore**, keine Quelle mit Zahlen · **VIX-Term-Structure als Gate = nichts Belastbares**.

### Verdikt
Kein neues Bein. Das Buch bleibt vorerst bei 6 Beinen, **aber die Bewertungsgrundlage hat sich geändert**: die 57%/86d sind eine Fenster-Zahl, und Bein 4 ist eine Wette auf das Regime seit 2023. Die Handlungsoptionen (Bein 4 behalten / Noise-ORB als 7. Bein für Tempo+Stabilität) liegen bei Max — Ticket `buch-entscheidung-070`.

### Lehren
1. **R-Multiples sind über lange Zeiträume mit wachsendem Preisniveau nicht vergleichbar.** `r_net = r − cost/R_pts`: bei konstanten Kosten (1,01 Pkt) und wachsender Range (5,4 Pkt in 2016 → 49,8 Pkt in 2026) fällt die Kostenquote von 18,7% auf 2,0%. Ein über 10 Jahre aggregierter expR gewichtet die späten Jahre systematisch hoch. **Ab jetzt: bei jedem Bein zusätzlich die USD-Jahrestabelle und mean R_pts pro Jahr anschauen.**
2. **Passquoten müssen fenstergetrennt gerechnet werden.** Eine Portfolio-Passquote über die volle Historie kann eine Eigenschaft des Endfensters sein. Der Auto-Fit sieht das strukturell nicht. **Ab jetzt gehört zu jeder Buch-Änderung die IS/OOS-getrennte Frontier.**
3. **Die Gegenprobe ist wertvoller als der Test.** H1 hätte als sauberer Fund durchgehen können (IS+OOS positiv, expR 0,14). Erst „wie läuft es *außerhalb* des Filters?" hat es entlarvt. **Ab jetzt bei jedem Regime-/Kontextfilter Pflicht: die Komplementärmenge mitmessen.**
4. **Ein Filter, der nur IS hebt, ist kein Filter.** Klingt trivial, war aber in #068 nicht geprüft — dort wurde VIX-Band auf Jahres-Positivität und Nachbar-Robustheit geprüft, nicht auf den IS/OOS-Bruch.
5. **Engine-Falle dokumentiert:** `sigma_entry` bedeutet je nach Modus etwas anderes (im ORB-Zweig = `or_size`, nicht Vola). Vor jeder Verhältnisbildung auf Konstanz prüfen.

## #071 — Ziel „>50% Passquote in <30 Tagen": erreicht, und der Nebengewinn ist größer (10.08.2026)
Max' Zielvorgabe: weitere Beine finden, bis die Passquote **über 50% bei unter 30 Tagen** liegt. Skripte: `goal30_inventory.py`, `goal30_qualify.py`, `goal30_legcheck.py`, `goal30_search.py` … `goal30_search4.py`.

**Der Ansatzpunkt:** `auto_fit` nimmt ein Bein nur auf, wenn `pass_neu ≥ pass_alt + 2`. Das ist eine **Quoten-Regel** — sie hat systematisch jeden Kandidaten abgelehnt, der Tempo gegen Quote tauscht (#068: NOISE_ORB 57%/86d → 52%/53d = abgelehnt). Für Max' Ziel ist genau dieser Trade-off der richtige. Die Bank war voll von Beinen, die für das *falsche* Ziel aussortiert wurden.

### 🎯 Ergebnis: 4 Beine statt 6
| Bein | Mechanismus | Tr/Jahr | Status |
|---|---|---|---|
| `NOISE_ORB_NQ` | Zarattini Noise-Band (#068/#070) | 185 | **neu** (lag auf der Bank) |
| `RV_leadlag_NQES_t0.002_lr0.5_s0.75` | NQ→ES Lead-Lag | 63 | **Parameter-Variante** des Buch-Beins |
| `NQ_Asia-Dir-USopen` | Asien-Richtung → US-Open | 25 | bleibt |
| `OPEXMOM_NQ_e150_t0.1_s0.75` | OpEx-Momentum | 10 | **neu** (Bank seit #049) |

**Frontier gegen das aktuelle Buch (E8 50k, EOD-Trailing, identische Methode):**

| frac | 0.10 | 0.22 | 0.30 |
|---|---|---|---|
| Buch heute (6 Beine) | 57%/85d | 50%/48d | 45%/27d |
| **Zielbuch (4 Beine)** | **65%/91d** | **57%/50d** | **51%/28d** |

- **Max' Ziel ist erreicht:** frac 0.30 → **50,6% ± 0,25 / 28,3 Tage** (40.000 Sims, 2σ = 50,1–51,1%).
- **Der eigentliche Gewinn liegt woanders:** das Zielbuch dominiert das aktuelle auf **jedem** Punkt der Frontier. Bei frac 0.10 sind es **65% statt 57%**.
- **Und es ist robuster:** IS 2016-23 **67% vs. 52%**, OOS 2024-26 62% vs. 62%. Das alte Buch war stark fensterabhängig (#070 Insight #9), das neue nicht.

### Weniger ist mehr — jedes zusätzliche Bein verschlechtert es
| Variante | avg\|corr\| | VOLL@0.10 | IS@0.10 |
|---|---|---|---|
| Zielbuch (4) | 0,088 | **65%/91d** | **67%** |
| + NQ_Momentum (5) | 0,147 | 55%/55d | 54% |
| + Momentum + FLIP (6) | 0,148 | 49%/30d | 48% |
| sanft: Buch + Noise + OpEx (8) | 0,095 | 54%/51d | 54% |

Das widerspricht scheinbar der Diversifikations-Doktrin, ist aber **Insight #6 in Reinform**: der Trailing-DD bestraft Pfad-Varianz. `NQ_Momentum` ist einzeln ein sauberes Bein (IS +0,093 / OOS +0,232 / 10 von 11 Jahren), hat aber als Continuation-Strategie mit RR>1 eine choppige Equity — im Buch senkt es die Quote um 10 Punkte. **Diversifikation hilft nur, solange die zusätzlichen Beine die Pfad-Varianz nicht erhöhen.**

### 🚨 Der methodische Fund: die Tage-Minimierung belohnt Tail-Lotterien
Die ersten drei Suchläufe lieferten scheinbar bessere Zahlen (52%/26d) — und waren Schrott:
- **Lauf 2** wählte `OPEXMOM_RTY_..s1.0` **und** `..s0.75`: **corr 0,993, 100% Tagesüberlappung**. Dasselbe Bein zweimal, nur anderer Stop = doppelte Positionsgröße, keine Diversifikation.
- **Lauf 3** (mit Redundanz-Constraints) nahm `PIV_revert_NQ_c180` auf: top5 = **150%** des Gewinns, 5/11 Jahre positiv, 2025+ **negativ** — und Pivots sind in **#051 ausdrücklich als NO-GO beerdigt**. Dazu `VOLBRK_NQ` (top5 91%, 2025+ −1.738$) und `MOMSEL_ES` (4/11 Jahre). Gleichzeitig warf es `NQ_Momentum` raus, eines der saubersten Beine im Bestand.
- **Ursache:** ein Bein mit seltenen, großen Gewinnen erreicht das Target im Monte-Carlo schneller — auch wenn es die meiste Zeit verliert. Wer auf „wenige Tage" optimiert, bekommt Lotterielose.
- **Konsequenz:** Qualität wird **vor** der Suche durchgesetzt, nicht danach geprüft. Von 97 Kandidaten überlebten die #070-Gates (IS>0, OOS>0, top5<60%, ≥55% Jahre positiv, 2025+ positiv) nur **22** — effektiv 7 unabhängige Mechanismen.

### Vorbehalte (müssen vor einem Live-Umbau geklärt sein)
1. **frac 0.30 ist aggressiv.** Das Buch lief bisher auf 0.10-0.22. Wer die Quote statt das Tempo will, nimmt frac 0.10 und bekommt 65%/91d.
2. **Der EOD-vs-Intraday-Vorbehalt.** Unter Intraday-Trailing-DD fällt das Zielbuch auf 35%/30d. Ich stütze mich darauf, dass E8 **EOD**-Trailing hat (Research-Cache 28.07.2026). **Bei frac 0.30 ist diese Annahme existenziell** — vor dem Live-Gang schriftlich bestätigen lassen.
3. **Werkzeug-Befund:** `funded_frontier.passmc` prüft den Drawdown **nur am Tages-Close** — `dw` (Tages-Tiefpunkt) fließt dort nur ins Sizing ein, nicht in den Bust-Check. `book.mc` kann beides (`dd_mode`). Für E8/EOD korrekt, aber man muss es wissen. Meine `passmc_vec` kann beide Modi (Regressions-Check gegen das Original: 57%/85d vs. 57%/86d).
4. **Radikaler Umbau:** 5 der 6 Beine würden getauscht. Entscheidung liegt bei Max → Ticket `buch-umbau-071`.

### Lehren
1. **Ein Optimierungsziel erzeugt seine eigenen Artefakte.** „Maximiere Quote" (auto_fit) lehnt Tempo-Beine ab; „minimiere Tage" zieht Tail-Lotterien an. Beide Male ist nicht der Suchraum das Problem, sondern die Zielfunktion. **Qualitätsgates gehören vor die Suche, nicht dahinter.**
2. **Mehr Beine ≠ besser.** Diversifikation zahlt nur, wenn das neue Bein die Pfad-Varianz nicht erhöht. Ein einzeln sauberes Bein kann das Buch um 10 Punkte verschlechtern.
3. **Der Engpass ist die Mechanismen-Vielfalt, nicht die Kombinatorik.** 169 Survivors → 97 Kandidaten → 22 qualifiziert → 7 unabhängige Mechanismen. Weitere Kombinatorik auf diesem Bestand bringt nichts mehr; für einen echten Sprung braucht es **neue Mechanismen** (→ Cross-Asset, siehe [[Discovery-Prozess (wie wir Alpha finden)]]).

## #072 — Optimierung auf Challenge-Bestehen: zwei Rechenfehler gefunden, die alle Vault-Zahlen betreffen (10.08.2026)
Max' Ziel nach #071: nicht mehr „>50% in <30 Tagen", sondern **so weit wie möglich auf das Bestehen von Funded-Challenges optimieren**. Skripte: `goal_maxpass.py`, `goal_maxpass2.py`, `goal_final.py`, `goal_multiaccount.py`.

### 🚨 Fehler 1: Der Sim-Horizont zählt aktive Handelstage, nicht Kalendertage
Die reine Passquoten-Maximierung lief sofort in eine Entartung: **„100% Passquote in 2.057 Tagen"** mit einem einzelnen OpEx-Bein. Ursache gefunden: `FF.passmc` (und alles, was darauf aufbaut) setzt `horizon=252` — in **aktiven Handelstagen**. Damit bekommt

| Buch | aktive Tage/Jahr | effektive Zeit bei horizon=252 |
|---|---|---|
| Buch heute | 228 | 1,1 Jahre |
| Zielbuch #071 | 181 | **1,4 Jahre** |
| OpEx-Bein solo | ~10 | **25 Jahre** |

**Konsequenz:** Alle Passquoten im Vault (57%, 61%, 65%) bedeuten *„irgendwann innerhalb von ~1,1–1,4 Jahren"*, **nicht** „innerhalb der genannten Median-Tage". Und der Vergleich zweier Bücher unterschiedlicher Frequenz ist systematisch zugunsten des selteneren verzerrt. Fix: Horizont in Kalendertagen vorgeben, je Buch in aktive Tage umrechnen (`h_cal/365.25 × apy`).

**Ehrliche Zahlen mit Kalender-Horizont (E8-EOD-DD):**

| Buch | 60 Tage | 90 Tage | 180 Tage |
|---|---|---|---|
| Buch heute (6 Beine) | 38,2% | 41,2% | 51,3% |
| **Zielbuch #071 (4 Beine)** | **41,4%** | **45,2%** | **57,2%** |

Das Zielbuch bleibt auf jedem Horizont vorn (+3 bis +6 Punkte) — die Rangfolge aus #071 hält, nur das Niveau war zu hoch.

### 🚨 Fehler 2: „2 Konten parallel = 75%" ist falsch (korrigiert #029)
[[Strategie-Logbuch|#029]] empfahl **„2× 25k parallel → ≥1 Pass ≈ 75%"**. Das setzt Unabhängigkeit voraus. Zwei Konten, die dasselbe Buch mit demselben Sizing fahren, handeln aber **dieselben Signale am selben Tag**. Auf gemeinsamen Marktpfaden gemessen (`goal_multiaccount.py`, 40.000 Sims):

| Variante | 25k | 50k |
|---|---|---|
| **A) 2× identisch parallel** | 50,2% → 50,2% (**+0,0pp**) | 33,5% → 33,5% (**+0,0pp**) |
| B) 2× parallel, verschiedene frac (0.04/0.40) | 55,1% (+4,9pp, corr 0,73) | **51,9%** (+18,4pp, corr 0,47) |
| C) sequenziell (Reset nach Fail) | **74,9%** (2×90d, 200$) | 55,6% (2×90d, 300$) |

- **Ein zweites identisches Konto bringt exakt null.** Entweder bestehen beide oder keins.
- Die naive Unabhängigkeitsformel überschätzt Variante B um **11–18 Prozentpunkte**.
- Echte Streuung entsteht nur über **unterschiedliches Sizing** (teilweise) oder **zeitliche Trennung** (voll).
- Beim 25k greift der Min-Size-Effekt: beide fracs landen bei ähnlichem Sizing (corr 0,73), der Split bringt wenig. Beim 50k ist er wirksam (corr 0,47, +18pp).

### Beste Konfiguration für „Challenge bestehen"
Die freie Suche auf 25k (`goal_final.py`) konvergiert **auf dasselbe Buch wie #071** — zwei verschiedene Zielfunktionen, dasselbe Ergebnis. Das ist die bisher stärkste Bestätigung für das 4-Bein-Buch.

| Strategie | P(bestehen) | Zeit | Kosten |
|---|---|---|---|
| Zielbuch auf **25k**, frac 0.04 | **50,1%** | 90 Tage | 100$ |
| Zielbuch auf 25k, **sequenziell mit Reset** | **74,9%** | 180 Tage | 200$ |
| Zielbuch auf 50k, 2 Konten mit frac-Split 0.04/0.40 | 51,9% | 90 Tage | 300$ |
| Buch heute auf 50k (Status quo) | 41,2% | 90 Tage | 150$ |

**Unter Intraday-DD statt EOD fällt alles auf 33–34%** — der Vorbehalt aus Ticket `e8-dd-mechanik` ist damit der wichtigste offene Punkt überhaupt.

### Lehren
13. **Ein Simulations-Horizont in „aktiven Tagen" ist kein Zeitlimit.** Bücher unterschiedlicher Handelsfrequenz bekommen dadurch unterschiedlich viel Kalenderzeit — der Vergleich ist verzerrt, und Klein-N-Strategien werden absurd bevorteilt. **Zeitfenster immer in Kalendertagen vorgeben.**
14. **Parallele Konten mit demselben Buch sind ein einziges Konto.** P(mind. 1 Pass) darf nur mit gemessener Korrelation gerechnet werden, nie mit `1-(1-p)^n`. Diversifikation über Konten braucht unterschiedliches Sizing oder zeitlichen Versatz — sonst ist es nur doppelte Gebühr.

## #073 — „>50% in unter 30 Tagen": mathematisch nicht erreichbar, und zwar unabhängig vom Buch (10.08.2026)
Nach der Horizont-Korrektur aus #072 nochmal hart gegen Max' ursprüngliche Zielvorgabe gerechnet — diesmal mit echter 30-Tage-Frist statt Median-Tagen. Skripte: `goal30_hard.py`, `goal30_ceiling.py`.

### Alles ausgereizt, was es an Hebeln gibt
| Hebel | Ergebnis |
|---|---|
| Kontogröße 10k / 15k / 25k / 50k | Maximum **44,6%** (10k) |
| Kontrakt-Cap 3 → 20 | **kein Einfluss** (43,1% durchgehend — der Cap bindet nie, das Cushion-Sizing begrenzt vorher) |
| Sizing frac bis 1.0 | ausgereizt |
| Zeithorizont 30 → 120 Tage | **kein Einfluss** (43,5% durchgehend) |
| Beam-Search über alle qualifizierten Beine | +1 bis +2 Punkte |

### Warum: bei kurzer Frist zählt nur das Barrieren-Verhältnis
Der Grund, dass Horizont und Cap wirkungslos bleiben, ist strukturell. Bei aggressivem Sizing terminiert jeder Pfad binnen weniger Tage — Target oder Bust. Damit fällt die Passquote auf die Mathematik eines Random Walks mit zwei absorbierenden Barrieren zurück: **P(pass) → DD / (Target + DD)**.

| Käfig (Target/DD) | Theorie | gemessen | Delta |
|---|---|---|---|
| **E8 50k — 3000/2000** | 40,0% | **39,8%** | −0,2pp |
| E8 25k — 1500/1000 | 40,0% | 40,6% | +0,6pp |
| **E8 10k — 600/400** | 40,0% | **43,5%** | **+3,5pp** |
| Bulenox 50k — 3000/2500 | 45,5% | 43,8% | −1,6pp |
| hypothetisch 3000/4000 | 57,1% | 52,0% | −5,2pp |
| hypothetisch 2000/3000 | 60,0% | 54,4% | −5,6pp |

**Das Buch bewegt die Zahl um maximal +3,5 Prozentpunkte.** Alles andere macht der Käfig. E8 hat bei *jeder* Kontogröße dasselbe Verhältnis (Target 6% / DD 4% = 3:2) und damit dieselbe Decke von ~40%.

**Um über 50% in 30 Tagen zu kommen, bräuchte es DD ≥ Target.** Das bietet keine Prop-Firma an — daran verdienen sie.

### Verdikt
**Das Ziel ist bei E8-Konditionen nicht erreichbar, unabhängig davon, welche Beine im Buch stehen.** Es ist keine Alpha-Frage, sondern eine Frage der Frist: in 30 Tagen kann eine Edge von ~0,1R pro Trade schlicht nicht genug Trades sammeln, um die Barrieren-Mathematik zu schlagen. Was geht:

| Ziel | Beste Konfiguration | Wert |
|---|---|---|
| in 30 Tagen | 5-Bein-Buch auf E8 10k | **43,5%** |
| in 90 Tagen | 4-Bein-Zielbuch auf E8 25k | **50,1%** |
| ohne Fristdruck (2 Versuche seriell) | 4-Bein-Zielbuch auf 25k | **74,9%** (180 Tage, 200$) |

### Nachtrag: STATIC vs. TRAILING erstmals gemessen — und die exakte Anforderung an den Käfig
`passmc` konnte bisher **nur trailing** (Floor wandert mit dem Peak nach oben). Der statische Fall (Floor fix bei −DD) war nie implementiert und damit nie gerechnet. Nachgeholt in `goal30_cage.py`:

| Käfig | Theorie | trailing | **static** | Delta |
|---|---|---|---|---|
| E8 50k — 3000/2000 | 40,0% | 39,8% | **42,6%** | +2,8pp |
| E8 25k — 1500/1000 | 40,0% | 40,6% | **44,2%** | +3,6pp |
| **E8 10k — 600/400** | 40,0% | 43,5% | **48,5%** | **+4,9pp** |
| Bulenox — 3000/2500 | 45,5% | 43,8% | **46,2%** | +2,3pp |

**Static ist durchgehend 2,3–4,9 Punkte besser** — der Trailing-Floor kostet real Passquote, weil er nach jedem Hoch nachzieht und den Puffer wegnimmt.

**Damit ist die Anforderung an den Käfig exakt beziffert.** Für >50% in 30 Kalendertagen braucht es:
- bei **static**: DD ≥ **0,83 × Target**
- bei **trailing**: DD ≥ **1,00 × Target**

E8 liegt bei 0,67 × Target (4% DD / 6% Target) — und zwar bei *jeder* Kontogröße. Das ist die ganze Erklärung.

### Der Markt bietet den nötigen Käfig nicht an (Käfig-Scan 10.08., Research-Cache #073-Block)
Nachdem die Anforderung beziffert war (static: DD ≥ 0,83 × Target · trailing: DD ≥ 1,00 × Target), den gesamten Markt abgesucht — 12 Firmen, davon 11 neu recherchiert.

| Firma / Konto | Target | DD | Typ | DD/(T+DD) |
|---|---|---|---|---|
| **Bulenox 50k Opt.2** | 3.000 | 2.500 | EOD-trailing | **45,5%** |
| Tradeify Select 50k | 2.500–3.000 *(unklar)* | 2.000 | EOD-trailing | 40,0–44,4% |
| **E8 / Topstep / TPT / Alpha Zero / MFFU / LucidFlex / TradeDay** | 3.000 | 2.000 | EOD-trailing | **40,0%** |
| Elite Trader Funding 50k | 4.000 | 2.000 | **static** | 33,3% |
| TradeDay Static | 1.500 | 500 | **static** | 25,0% |
| DayTraders Static | 3.750 | 1.000 | **static** | 21,1% |

**Zwei Befunde:**
1. **Der Markt clustert bei exakt 40%.** $3.000 Target / $2.000 DD auf 50k ist Industriestandard — E8, Topstep, Take Profit Trader, Alpha Futures, MFFU, LucidFlex, TradeDay sind identisch. Das ist kein Zufall: bei 40% verdient die Firma an jeder Eval.
2. **„Static" ist kein Garant für eine bessere Ratio.** Alle drei echten Static-Angebote haben ein **schlechteres** Verhältnis als E8 (21–33%), weil die Firmen das Target proportional zur kleineren DD anheben. Der statische Vorteil aus unserer Messung (+2,3 bis +4,9pp) wird durch die Konditionen mehr als aufgefressen.

**Bestes reales Angebot: Bulenox 45,5% — und das ist für uns tot, weil Bulenox VPS strikt verbietet** (Ticket #RAX-292098, Research-Cache). Selbst mit Bulenox wären es gemessen 45,0%, nicht >50%.

### Und wie gut müssten neue Beine sein? — die Anforderung beziffert
Max' wörtlicher Auftrag war „finde weitere Beine". Bisher wurde nur aus dem Bestand kombiniert. Deshalb zum Abschluss quantifiziert, **was ein besseres Buch leisten müsste** (`goal30_required_edge.py`): der Drift der Tages-P&L wird angehoben, die Streuung bleibt gleich (= reine Sharpe-Verbesserung, nicht mehr Size — Size ist über `frac` bereits ausgereizt).

Aktuelles Buch: Tages-P&L **+38,43 $** bei Streuung 450,92 $ → **Sharpe 1,37** annualisiert.

| Drift | Sharpe/Tag | E8 50k | E8 10k | Bulenox |
|---|---|---|---|---|
| ×1,00 (heute) | 0,085 | 40,0% | 43,7% | 43,8% |
| ×1,50 | 0,128 | 45,3% | 49,4% | 49,3% |
| **×2,00** | 0,171 | **51,2%** | **54,6%** | **55,5%** |
| ×3,00 | 0,256 | 63,9% | 64,5% | 68,4% |

**Nötig ist der ~2-fache Drift bei gleicher Streuung — ein Buch mit Sharpe ≈ 2,7.** Bei allen drei Käfigen identisch, was die Robustheit des Befunds zeigt.

**Einordnung:** Renaissance Medallion liegt langfristig bei Sharpe ~2,5, ein sehr gutes systematisches Intraday-Buch bei 1,5–2,5. Das aktuelle Buch (1,37) ist für Retail-Verhältnisse mit 1-Min-OHLCV und ohne L2 bereits solide. **Gefordert wäre also ein Buch über Medallion-Niveau** — das ist mit den verfügbaren Daten nicht erreichbar, und keine Anzahl zusätzlicher Beine aus dem heutigen Mechanismen-Vorrat kommt dort hin (der Pool liefert nur ~7 unabhängige Mechanismen, siehe #071).

### 🔚 Endgültiges Verdikt
**„>50% Passquote in unter 30 Kalendertagen" ist nicht erreichbar — weder mit einem anderen Buch noch mit einer anderen Firma.** Das Buch trägt maximal +3,5 Punkte, der beste am Markt verfügbare Käfig liefert 45,5% Barrieren-Ratio, und die nötigen ≥50% gibt es nirgends. Erreichbar ist:

| Frist | Beste reale Konfiguration | Wert |
|---|---|---|
| 30 Tage | 5-Bein-Buch, Bulenox-Käfig (VPS-K.O.) | 45,0% |
| 30 Tage | 5-Bein-Buch, E8 10k | **44,2%** |
| 90 Tage | 4-Bein-Zielbuch, E8 25k | **50,1%** |
| 180 Tage, 2 Versuche | dito | **74,9%** |

### Lehre
15. **Kurze Frist = Barrieren-Mathematik, lange Frist = Edge.** Bei einer Frist, die zu kurz ist, um viele Trades zu sammeln, konvergiert P(pass) gegen `DD/(Target+DD)` — das Buch trägt dann nur noch wenige Prozentpunkte bei. **Tempo-Ziele sind deshalb primär eine Firmen-/Käfig-Frage, keine Strategie-Frage.** Umgekehrt lohnt Alpha-Arbeit nur, wenn die Frist lang genug ist, dass die Edge wirken kann. Deckt sich mit #032 (Käfig-Scan: Firmenwahl war +7 Punkte, mehr als jedes Bein).
16. **Trailing-DD kostet 2,3–4,9 Prozentpunkte gegenüber static** — bei sonst identischem Käfig. Der Floor zieht nach jedem Hoch nach und nimmt genau den Puffer weg, den man gerade erarbeitet hat. **Bei der Firmenwahl ist der DD-TYP so wichtig wie die DD-HÖHE.** Konkrete Schwellen für >50% in 30 Tagen: static braucht DD ≥ 0,83 × Target, trailing braucht DD ≥ 1,00 × Target.
17. **„Static DD" ist als Werbeversprechen wertlos** (#073-Käfig-Scan). Firmen, die statischen Drawdown anbieten, heben im Gegenzug das Profit-Target an — alle drei gefundenen Static-Angebote haben ein *schlechteres* `DD/(Target+DD)` als der Trailing-Standard (21–33% vs. 40%). **Immer die Ratio rechnen, nie den DD-Typ allein bewerten.**
18. **Eine nominal gute Ratio ist bei Intraday-Trailing wertlos.** Die Näherung `P(pass) ≈ DD/(Target+DD)` gilt nur für EOD- und statischen Drawdown. Bei Intraday-Trailing bricht sie zusammen: Apex 50k hat nominal 45,5%, real gemessen (#069) nur 23–33%. **Bei jeder Firma zuerst klären, ob der DD intraday zieht — das entscheidet mehr als die Ratio.**

## #074 — Alpha durch Fehlersuche: 40,0% → 48,6% ohne ein einziges neues Bein (10.08.2026)
Max' Auftrag: erst in den eigenen Unterlagen nach **Fehlern in Anwendung/Coding** suchen (ein falsch implementierter Algo verliert Geld, sein Fix ist kostenloses Alpha), dann externe Research. Skripte: `goal_variance.py`, `goal_weights.py`, `goal_final_opt.py`, `goal_onrv_filter.py`.

### 🐛 Fund 1: `book.cell_daily` zählt das Tagesrisiko doppelt
```python
cc = np.cumsum(close)
worst = min(cc.min(), (cc - ma).min(), 0.0)      # book.py:43
```
`cc[k]` ist das kumulierte **Ergebnis bis inklusive** Trade k, `ma[k]` das MAE **von** Trade k. Die Formel zieht das MAE also von einem Stand ab, der das Ergebnis desselben Trades schon enthält — bei einem Verlust-Trade wird der Verlust zweimal gezählt. Korrekt ist `cc[k-1] - ma[k]` (Stand **vor** dem Trade minus dessen MAE).

Beispiel: Trade verliert 100 $ und hatte 100 $ MAE → aktuell −200 $, korrekt −100 $.

| Bein | risk alt | risk neu | Faktor |
|---|---|---|---|
| NQ_Momentum | 204,3 $ | 81,0 $ | **2,52** |
| RTY_Gap-fade | 98,5 $ | 36,8 $ | **2,68** |
| NOISE_ORB_NQ | 138,0 $ | 61,0 $ | 2,26 |
| RV_leadlag | 212,5 $ | 97,4 $ | 2,18 |
| NQ_ORB-fade | 77,2 $ | 36,5 $ | 2,12 |

**Alle Beine hatten ein um Faktor 1,7–2,7 überschätztes Tagesrisiko.** Da `risk = median(|dw<0|)` das Cushion-Sizing steuert, wurde systematisch zu klein gesized. Wirkung auf die Passquote: **+1,3pp (EOD), +4,2pp (intraday)** — im EOD-Modus teilweise durch `frac` kompensierbar, im Intraday-Modus voll wirksam.

> [!warning] Live-Relevanz
> Wenn der RiskGuard dasselbe Risikomaß verwendet, sized er live zu klein. Das ist verlorenes Geld, kein Backtest-Artefakt. → Ticket `riskguard-risk-mass`.

### 🐛 Fund 2: Die Beine laufen alle mit derselben Kontraktzahl
`passmc` berechnet **ein** `sz` und wendet es auf die aggregierte Tages-P&L an — implizit Gleichgewichtung. Die Tages-Sharpes der Beine unterscheiden sich aber um Faktor 4 (OPEX 0,30 · ASIA 0,17 · RV 0,14 · NOISE 0,12). Ein Bein mit 0,30 gleich stark zu fahren wie eines mit 0,12 verschenkt Sharpe.

**Das erklärt rückblickend #071:** dort hat *jedes* zusätzliche Bein die Passquote gesenkt. Nicht das Bein war das Problem, sondern die Gleichgewichtung — ein schwaches Bein schleppte seine volle Varianz ins Buch. Mit Sharpe-optimaler Gewichtung (`w ∝ Σ⁻¹μ`, auf ganze Kontrakte gerundet, live pro Bein eine eigene Kontraktzahl) kehrt sich das um.

### Die Verbesserungskette (30 Kalendertage, EOD-DD)
| Schritt | Passquote | Buch-Sharpe |
|---|---|---|
| Ausgangspunkt (gleichgewichtet, dw-Bug) | 40,0% | 0,1057 |
| + dw-Bug gefixt | ~41,3% | — |
| + Exit-Varianten je Bein (auf **Sharpe** optimiert, nicht expR) | 41,9% | 0,1412 |
| + Sharpe-optimale Gewichtung | 44,2% | 0,1529 |
| + fünftes Bein (mit Gewichtung erstmals hilfreich) | 44,5% | 0,1534 |
| **+ Kontogröße 25k** | **48,6%** | — |

**+8,6 Prozentpunkte ohne ein einziges neues Bein**, allein durch zwei Bugfixes und die richtige Zielgröße (Sharpe statt expR). Das gewichtete Endbuch: 3× `NOISE m1.5` · 6× `OPEX` · 2× `RV stop0.3` · 6× `ASIA tgt2.0` · 6× `OPEXMOM s1.5`.

Bemerkenswert: die Exit-Optimierung auf **Sharpe statt expR** hat einzelne Beine massiv verbessert — `RV_leadlag` mit `rv_stop=0.3` erreicht expR **+0,424** (statt +0,219) bei IS +0,353 / OOS +0,651.

### Externe Research (#074-Block im Research-Cache)
Ein verwertbarer Fund, und der hilft nicht: **Overnight-Realized-Vola als Vol-Prädiktor** (Zhang/Zhao SSRN 3574323, MSE −27,8%). Getestet als Tagesfilter: er hebt den Sharpe real (0,1534 → 0,1799 im mittleren Vol-Band), **senkt aber die Passquote** (48,5% → 45,4%). Grund siehe Lehre unten.
Negativbefunde, die künftige Suchen sparen: **ML auf MNQ-OHLCV ist tot** (zwei 2026er Papers: LSTM/GBM schlagen die 51,8%-Basisrate nicht signifikant, Feature-Importance instabil) · **kein Paper zu Prop-Firm-First-Passage-Sizing** existiert (nur Blog-Rechner) · **keine Arbeit quantifiziert Korrelation Momentum↔Alternative für Index-Futures**.
Und im eigenen Pool: **kein einzig negativ korrelierter Kandidat** (Minimum +0,111) — gratis Varianz-Reduktion durch Diversifikation gibt es nicht.

### Stand zum Ziel
**48,6% in 30 Kalendertagen** (25k-Konto). Zum Ziel fehlen **1,4 Prozentpunkte**; der nötige Buch-Sharpe ist 0,1705, erreicht sind 0,1534. Alle drei Kontogrößen konvergieren bei 48,5–48,6% — das ist die Sharpe-Grenze des Buchs, kein Käfig-Effekt mehr.

### Lehren
19. **Ein falsch gerechnetes Risikomaß ist teurer als eine fehlende Strategie** (#074). Der doppelt gezählte Tages-Drawdown hat alle Beine um Faktor 1,7–2,7 zu riskant erscheinen lassen und damit das Sizing gedrosselt. **Vor jeder Alpha-Suche die Messkette prüfen** — hier waren zwei Bugfixes mehr wert als jedes neue Bein.
20. **Gleichgewichtung ist eine stille Annahme, keine neutrale Wahl** (#074). Beine mit Sharpe-Unterschieden von Faktor 4 gleich zu fahren verschenkt Portfolio-Sharpe und lässt gute Zusatzbeine wie Verwässerer aussehen. **Jede Portfolio-Aussage gilt nur zusammen mit ihrer Gewichtung.**
21. **Bei fester Kalenderfrist ist Tage-Wegfiltern kontraproduktiv** (#074). Der Overnight-Vol-Filter hob den Sharpe um 17%, senkte die Passquote aber um 3pp — weil er Handelstage entfernt und man innerhalb von 30 Kalendertagen die Trades *braucht*, um das Target zu erreichen. **Selektivität zahlt sich nur ohne Fristdruck aus.**
22. **Exits gegen Sharpe optimieren, nicht gegen expR** (#074). `RV_leadlag` mit engem Stop (0,3 statt 0,75) verdoppelt den expR auf +0,424 und hebt gleichzeitig den Tages-Sharpe — der expR allein hätte die Variante nicht gefunden, weil er die Streuung ignoriert.

## #075 — Engine-Audit: fünf Bugs, davon zwei die live Geld kosten (10.08.2026)
Fortsetzung von #074. Ein vollständiges Code-Audit auf Bugs mit **Performance-Wirkung** hat drei weitere Funde geliefert, zwei davon kritisch — und zwei von ihnen machen die Zahlen **schlechter**, nicht besser.

### 🔴 Fund 1: `rv.py:167` skaliert das Risiko mit dem falschen Instrument
```python
R_pts = risk_d * c1[i0]     # c1 = Leader (NQ ~20.000)
```
Bei `rv_mode="leadlag"` ist der PnL-Träger aber **Symbol 2** (`base = r2 - r2[i0]`, die Position läuft in ES ~6.000). Median NQ/ES = 3,27. `qbt.py:53` fordert selbst „symbol MUSS = rv_sym1 sein" — das Bein setzt `symbol: ES` und verletzt genau das. Für die Spread-Modes (`div_fade` etc.) ist `c1` korrekt, **nur leadlag ist falsch**.

| | gebucht | ehrlich |
|---|---|---|
| $/R | 113,7 | 36,2 |
| **expR netto** | **+0,239** | **+0,087** |
| $/Trade | **34,06** | **9,12** |
| Total 10,5 J | 11.036 $ | 5.975 $ |

**`edge_ref.json` trägt 34,06 $/Trade als Live-Referenz für `MaxLeadLagES` — das ist 3,7× zu hoch.** Das Bein läuft live. Die Variante `rv_stop=0.3`, die in #074 noch als Star galt (expR +0,424), **fällt nach dem Fix durch die Qualitätsgates**.

### 🔴 Fund 2: Kaputte Kursdaten in ES und RTY
`load_rth` hatte keinen Sanity-Guard. Gemessen: **ES 780 Bars in 2 Sessions, RTY 8.591 Bars in 24 Sessions mit Preis ≤ 0** (Minimum −9,35 $). Ursache: Kalender-Spread-Quotes aus den Quartals-Rolls sind in die Continuous-Serien geleakt. `rv.py:80` normiert auf `c2[0]` — bei `c2[0] ≈ 2` explodiert der Renditevektor. **Zwei leadlag-Trades auf solchen Tagen trugen 22,3% des gesamten Leg-P&L.** NQ und YM sind clean.
Gefixt: `_drop_corrupt_sessions()` verwirft die ganze Session (nicht nur die Bars, sonst bleibt ein halber Tag mit falschem Referenzpreis stehen).

### 🟡 Fund 3: Das Asia-Bein steigt live eine Minute zu spät ein
`MaxAsiaDirNQ.cs` entscheidet im `IsFirstBarOfSession`-Block bei `Calculate.OnBarClose` → Fill am **09:31**-Open. `asian.py:161` nimmt den **09:30**-Open. Gemessen: **$/Trade 29,82 → 18,97, expR +0,217 → +0,176. Die erste US-Open-Minute ist 36% der Leg-Edge** (~271 $/Jahr/Micro). Kein Backtest-Fehler, sondern ein Live-Implementierungsfehler — der Fix im Script (Order vor dem Open platzieren) holt die Edge zurück.

### 🟢 Fund 4: Meine MAE-Doppelzählung steckt an drei Stellen, nicht einer
`book.py:43` (schon in #074), zusätzlich **`qbt.py:1213`** (`prop_pass_probability`) und **`copilot.py:154`** (`_daily_pnl_arrays`). Alle sechs Live-Beine machen genau 1 Trade/Tag — damit ist der Fehler mathematisch eindeutig: buggy liefert `close − mae`, korrekt ist `−mae`.
Auf dem Live-Buch mit **Intraday**-Trailing-DD, flaches Sizing: **1u 41% → 51%, 3u 23% → 31%.** Über `copilot.prop_assistant`: beste Größe 37% → 42%. Bei Cushion-Sizing reskaliert der Fix nur `frac`, die Frontier bleibt fast invariant — **der echte Gewinn steckt im Intraday-Breach-Check.**

### 🟢 Fund 5: Slippage auf Limit-Fills
`cost_pts` belastet unbedingt 2 Ticks, unabhängig vom Ordertyp. Bei einer ruhenden Limit zahlt man keinen Spread. Betroffen: **ORB-fade** (`entry = level`, live bestätigt in `MaxORBFadeNQ.cs`), `orb_exec="retest"`, und jeder Target-Exit. → **ORB-fade expR +0,063 → +0,086 (+36%)**, Buch +290 $ von 60.549 $. Ehrlich dazu: Stop-Market-Exits slippen real oft *mehr* als 1 Tick, und Queue-/No-Fill-Risiko ist gar nicht modelliert. Der saubere Fix ist getrennte `entry_slip_ticks`/`exit_slip_ticks`, nicht pauschal −1 Tick.

### Entkräftet (wo ich Bugs vermutet hatte, sind keine)
- **Stop-vor-Target-Konvention kostet exakt 0.** Über alle drei Loops instrumentiert: **kein einziger Trade** im Live-Buch berührt Stop und Target in derselben Minute. Die konservative Konvention ist gratis.
- **Keine doppelte Kostenverrechnung.** `cost_pts` wird genau einmal abgezogen; Portfolio-Frames setzen `cost_pts=0` nur zur Anzeige.
- **MAE bei `orb_exec="close"` ist korrekt** — der Fill ist der letzte Tick der Bar, innerhalb der Fill-Bar kann keine Adverse Excursion liegen.
- **Latenter Optimismus-Bug für später:** ORB-**Fade mit gesetztem `target_mult`** hat **35/422 (8,3%) Fake-Target-Hits** in der Fill-Bar (`qbt.py:466` seedet MAE mit der kompletten Fill-Bar). Aktuell nicht im Buch (`target_mult: null`), aber die #070-Fade-Arbeit läuft genau dort hinein.

### Stand zum Ziel nach allen Fixes
| Schritt | Passquote (30 Kalendertage) |
|---|---|
| Ausgangspunkt #074 | 40,0% |
| #074-Optimierung (mit rv-Bug) | 48,6% |
| **nach rv-Fix + Datenguard (ehrlich)** | **48,1%** (10k) |

Das gewichtete Endbuch: **3× `NOISE_ORB m1.5` · 8× `OPEXMOM t0.2/s0.75` · 4× `ASIA tgt2.0`**, Buch-Sharpe 0,1509. Es fehlen **1,9 Prozentpunkte**. Die #074-Zahl war um 0,5pp aufgebläht, weil das RV-Bein mit falscher Risiko-Einheit drin war.

### Lehren
23. **Ein Audit auf „Bugs, die Performance kosten" findet auch Bugs, die Performance *vorgetäuscht* haben.** Von fünf Funden machen zwei die Zahlen schlechter (rv-Einheit, Datenqualität) und drei besser (MAE, Slippage, Asia-Minute). Wer nur nach Verbesserungen sucht, findet die gefährlicheren nicht.
24. **Einheiten-Fehler sind in Cross-Instrument-Strategien die Standardfalle** (#075). Wenn Signal und Position in verschiedenen Instrumenten leben, muss jede Risiko-, R- und Dollargröße explizit dem **PnL-Träger** zugeordnet werden. `qbt.py` hatte die Regel sogar dokumentiert — das Bein hat sie verletzt und niemand hat es 6 Wochen gemerkt.
25. **Rohdaten brauchen einen Sanity-Guard, auch nach „geprüft".** Die Daten galten seit #001 als „lückenlos, 0 OHLC-Fehler" — es gab trotzdem 9.371 Bars mit negativem Preis. **Ein `price <= 0`-Check kostet drei Zeilen und hätte 22% eines Leg-P&L als Artefakt entlarvt.**

## #076 — 57% in 30 Tagen: erreicht, aber nur über zwei Konten mit gespaltenem Sizing (10.08.2026)
Letzter Vorstoß nach #075 (Stand dort: 48,1% pro Konto). Zwei Hebel, die noch offen waren. Skript: `goal_last_push.py`.

### Hebel A — Slippage exakt nach Ordertyp (statt pauschal 2 Ticks)
`qbt.py` belastet jeden Trade mit 2 Ticks Slippage. Real gilt: Limit-Entry = 0 Ticks, Target-Exit (Limit) = 0 Ticks, Market/Stop = 1 Tick. Pro Trade aus der `exit`-Spalte rekonstruiert:

| Bein | expR vorher | expR exakt | Target-Exits |
|---|---|---|---|
| `ASIA tgt2.0` | +0,171 | **+0,193** | 84/264 |
| `OPEX t0.2` | — | +0,162 | 0/84 |
| `NOISE m1.5` | +0,100 | +0,112 | 0/1176 |
| `ORBFADE` (Limit-Entry) | +0,063 | +0,132 | 0/422 |

Gegenprobe mit konservativer Annahme (Stop-Exits slippen 1,5 Ticks statt 1): fast identisch, der Effekt ist robust. **Buch-Passquote: 48,1% → 48,4%.** Der ORB-Fade profitiert am meisten (+109%), fällt aber trotzdem durch die Qualitätsgates und kommt nicht ins Buch.

### Hebel B — zwei Konten parallel mit gespaltenem Sizing ✅
In #072 gemessen: zwei Konten mit **identischem** Sizing sind praktisch perfekt korreliert (Zugewinn 0,0pp). Mit **unterschiedlichem** frac entsteht echte Streuung. Für die 30-Tage-Frist nie gerechnet — hier nachgeholt, auf **gemeinsamen Marktpfaden** (also mit echter Korrelation, nicht mit Unabhängigkeitsannahme):

| Konto | frac-Split | Konto 1 | Konto 2 | **mind. 1 Pass** | corr |
|---|---|---|---|---|---|
| 25k | 0,10 / 0,80 | 44,6% | 46,1% | **57,0%** | 0,53 |
| 25k | 0,16 / 0,70 | 44,6% | 46,1% | **56,5%** | 0,55 |
| 25k | 0,08 / 0,60 | 44,6% | 46,6% | **53,8%** | 0,67 |
| 50k | 0,10 / 0,80 | 22,8% | 45,9% | **51,6%** | 0,31 |
| **10k** | beliebig | 49,2% | 49,2% | **49,2%** | **1,00** |

**Warum es funktioniert:** bei 25k (DD 1.000 $, Cap 7) bedeutet frac 0,10 konstant **1 Kontrakt**, frac 0,80 dagegen **3 bis 6 Kontrakte** je nach Kontostand. Die beiden Konten laufen dieselben Signale in völlig unterschiedlicher Größe und scheitern deshalb an verschiedenen Stellen — corr 0,53 statt 1,00.

**Warum es auf 10k NICHT funktioniert:** dort greift die Mindestgröße von 1 Kontrakt für beide fracs, das Sizing ist identisch, corr = 1,00, Zugewinn null. Genau der Min-Size-Effekt aus #029.

### 🎯 Zielerreichung — mit klarer Ansage, welche Lesart gilt
| Größe | Wert | Ziel erreicht? |
|---|---|---|
| Passquote **pro Konto** (beste Einzelkonfiguration) | **48,4%** (10k) | ❌ nein |
| **P(funded) mit zwei 25k-Konten**, frac 0,10 / 0,80 | **57,0%** | ✅ ja |
| Kosten | 2 × 100 $ = **200 $** | statt 100 $ |

Das Buch dazu: **3× `NOISE_ORB m1.5` · 8× `OPEXMOM t0.2/s0.75` · 4× `ASIA tgt2.0`**.

> [!danger] Recherche (10.08.26) — Zwei-Konten-Plan laut E8-Regelwerk vermutlich NICHT zulässig
> Anzahl paralleler Eval-Accounts ist bei E8 nicht limitiert (Frage 1 kein Blocker). Aber: E8s Copy-Trading-Regel verbietet explizit **"copying trades between multiple E8 evaluation accounts"** — "each evaluation must be done independently". Genau das ist unser Setup (zwei Evals, identisches Buch, nur Sizing-Split). Quelle nur via Suchmaschinen-Snippet erreichbar (Primärseite 403), aber über 3 unabhängige Anfragen identisch reproduziert → Konfidenz praktiker, kein bestätigt. Details + Kontraktlimits (25k: 2 Mini/20 Micro, 50k: 4/40, 100k: 8/80) in [[Research-Cache]]. **Vor jedem Kauf: schriftliche Support-Bestätigung einholen, ob der Sizing-Split (unterschiedliche Kontraktgröße, nicht identische Trades) als Ausnahme zählt — sonst Termination-Risiko für beide Konten.** Zusätzlich ungeklärter Widerspruch bei der News-Trading-Regel (2min/3min vs. neu gefunden 5min/5min) offen.

### Lehren
26. **„Passquote" ist zweideutig — pro Konto oder P(funded)?** Pro Konto bleiben wir bei 48,4%; die Wahrscheinlichkeit, überhaupt funded zu werden, liegt mit zwei gespaltenen Konten bei 57%. Beide Zahlen sind korrekt, sie beantworten verschiedene Fragen. **Bei jedem Passquoten-Ziel vorher festlegen, welche der beiden gemeint ist.**
27. **Sizing-Split ist der billigste Diversifikator, den wir haben** (#076). Kein neues Bein, kein neuer Mechanismus, keine Research — nur zweimal dasselbe Buch in unterschiedlicher Größe. Wirkt aber nur, wo die Mindestgröße von 1 Kontrakt nicht beide fracs zusammenzieht: auf 25k bringt es +10pp, auf 10k exakt null.
28. **Slippage ist ordertyp-abhängig, und das ist kein Detail** (#076). Der ORB-Fade gewinnt allein durch die korrekte Behandlung seiner ruhenden Limit-Order +109% expR. Bei jeder Strategie mit Limit-Entry oder Target-Exit gehört die Slippage getrennt gerechnet.

## #077 — E8 DD-Mechanik schriftlich geklärt: schlechtester Fall bestätigt (10.08.2026)
Antwort von E8-Support (Fábio, schriftlich, mit Verweis auf Help-Center-Artikel) auf Ticket `e8-dd-mechanik` (AP51):

> "Yes, the equity is also monitored. [...] if your account equity or balance reaches/falls below the loss level, your account will be permanently closed [...] the EOD Dynamic Drawdown only gets updated by a new EOD highest closed balance, but if the equity and/or balance falls below the EOD DD level for your account, this rule will be violated."

**Damit ist der befürchtete dritte Fall bestätigt, nicht der erhoffte:** der Floor selbst trailt EOD (nur geschlossene Gewinne heben ihn an, das war schon bekannt) — aber der Bruch wird KONTINUIERLICH gegen diesen (tagsüber statischen) Floor geprüft, nicht nur am Tages-Close. Ein kurzer Intraday-Touch unter den Floor beendet das Konto sofort, auch wenn die Bilanz am Abend wieder darüber steht.

**Konsequenz:** Alle Passquoten-Rechnungen im Vault (48,4%/57%/65% etc., #071–#076) sind mit reinem EOD-Bust-Check gerechnet (`funded_frontier.passmc` prüft nur den Tages-Close, siehe #072). Nach eigener Messung (#073) fällt das unter Intraday-Bust-Check auf **33–34%**. Das ist jetzt keine Vorsichtsannahme mehr, sondern der bestätigte Live-Fall.

Quelle: [E8 Help Center — EOD Dynamic Drawdown](https://intercom.help/e8/en/articles/11864596-eod-dynamic-drawdown), Support-Chat 10.08.2026 (Fábio, schriftlich).

Ticket AP51 (`e8-dd-mechanik`) damit geschlossen und im Tracker gelöscht (Ergebnis hier dokumentiert statt im Tracker archiviert). Blocker für AP53 (Buch-Entscheidung) entfällt, aber die Entscheidung selbst braucht jetzt eine Neu-Rechnung mit `dd_mode="intraday"` — bisher existiert dafür kein Lauf mit dem aktuellen Zielbuch.

### Lehre
29. **„EOD-Drawdown" ist Marketing-Sprache für „der Floor trailt EOD", nicht für „der Bruch wird nur EOD geprüft".** Zwei unabhängige Eigenschaften, die Prop-Firmen-Werbetexte routinemäßig vermischen. Präzedenzfall #069 (Matteo Coni) hatte genau diese Verwechslung schon einmal gekostet — diesmal wurde vor dem Kauf-Commitment nachgefragt statt danach.

## #078 — Intraday-DD nachgerechnet: kein pauschaler Einbruch auf 33%, sondern frac-abhängig (10.08.2026)
Nach #077 (E8 prüft den Bust kontinuierlich, nicht nur EOD) nachgerechnet: `goal_intraday_check.py`, `passmc_vec` (E8-50k-Default TARGET 3000/DD 2000 war im Code schon korrekt gesetzt), 8000 Sims, Fracs 0.10/0.18/0.22/0.30.

| Buch | Frac | EOD | Intraday | Δpp |
|---|---|---|---|---|
| Zielbuch (4 Beine, #071) | 0.10 | 59,3%/75d | 52,4%/69d | −6,9 |
| Zielbuch | 0.18 | 46,3%/20d | 36,3%/16d | −10,0 |
| Zielbuch | 0.22 | 42,2%/14d | 33,2%/10d | −9,0 |
| Zielbuch | 0.30 | 40,3%/8d | 30,1%/6d | −10,2 |
| Aktuelles Buch (3 Beine, #076) | 0.10 | 61,9%/43d | 47,9%/37d | −14,0 |
| Aktuelles Buch | 0.18 | 60,0%/40d | 45,7%/34d | −14,3 |
| Aktuelles Buch | 0.22 | 58,6%/40d | 43,5%/34d | −15,1 |
| Aktuelles Buch | 0.30 | 52,9%/18d | 34,5%/15d | −18,4 |

**Die #073-Prognose („Einbruch auf 33-34%") stimmt nur am oberen Frac-Ende (0.22–0.30), nicht pauschal.** Bei niedrigem Sizing (frac 0.10) bleibt deutlich mehr übrig (48–52%). Der Einbruch wächst mit dem Frac — die übliche Pfad-Varianz-Strafe von Trailing-DD wird durch den Intraday-Check verschärft, weil aggressives Sizing weniger Puffer gegen kurze Dochte lässt. **Konsequenz für AP53 (Buch-Entscheidung):** niedriger Frac (Tempo runter, Quote rauf) ist jetzt noch klarer im Vorteil als schon in #071/#073 gefunden.

**Zwei Nebenbefunde beim Nachrechnen:**
1. Das „aktuelle Buch" hat laut #076 tatsächlich nur 3 Beine (NOISE/OPEX/ASIA), nicht 5 — RV und ORBFADE fielen durch die Qualitätsgates und sind nicht im finalen Buch. Damit gerechnet.
2. Die EOD-Baseline hier (Zielbuch 59,3%/75d bei frac 0.10) liegt spürbar unter der in #071 zitierten 65%/91d. Grund: `book.py`/`goal30_search.py` liefen seit #071 durch mehrere Bugfixes (#075: RV-Instrument-Einheit, korrupte ES/RTY-Sessions, MAE-Doppelzählung), die die #071-Zahl künstlich gehoben hatten. Hier wurde mit dem bereits gefixten Code gerechnet — ehrlicher, aber nicht 1:1 mit der #071-Schlagzeile vergleichbar. Die relative EOD→Intraday-Verschlechterung (die eigentliche AP51-Frage) bleibt davon unberührt gültig.

**Bekanntes Restrisiko unverändert:** Das OPEX-Bein hat nur 9–10 Trades/Jahr (84–101 über 10,5 Jahre) und trägt mit Gewicht 8 stark zum aktuellen Buch bei — Tail-Abhängigkeit von wenigen OpEx-Freitagen, schon in #071 als Lehre notiert, unter Intraday-DD schärfer weil weniger Puffer.

Skript: `engine/goal_intraday_check.py` · Ergebnis: `engine/goal_intraday_check_results.json`.

## #079 — OR_DELTA_BIAS_NQ: der Beifang aus der IVB-Runde ueberlebt (LONG), SHORT nicht (10.08.2026)
Vertiefung des in #078-Umfeld dokumentierten Beifangs (Research-Cache "Filter-Lab-Runde 10.08.2026"): reiner Session-Bias aus dem Tick-Rule-Delta des OR-Fensters 09:30-10:00 ET auf NQ, KEIN Breakout mehr. Vier Pruefpunkte vorab festgelegt, alle durchgerechnet (`Quantpad Data/fixed/or_delta_bias_lab.py`, `_deepcheck.py`, `_overlap.py`, NQ RTH 1m 2016-2025, Kosten 0,87 Pkt/RT, IS 2016-2021, OOS 2022-2025):

**(a) Kontroll-Check — bestanden.** Signal schlaegt den naiven unconditional Long-Halt bei identischem Stop/Exit klar: gefiltert (delta>0) avgR +0,109 R/Trade (n=1318) gegen ungefiltert +0,033 R/Trade (n=2578, smul=0,75). Bei engem Stop (smul=0,5) ist der naive Long-Halt sogar netto NEGATIV (IS avgR -0,037, OOS -0,006) — das Delta-Vorzeichen filtert also echt, es ist keine bloße Verpackung des NQ-Aufwaertsdrifts.

**(b) Stop/Target-Grid — smul entscheidet, Target schadet.** 4x4-Grid (smul 0,25/0,5/0,75/1,0 × tmul None/1/1,5/2), LONG:

| smul | tmul | IS avgR | IS Sharpe | OOS avgR | OOS Sharpe |
|---|---|---|---|---|---|
| 0,5 | None | +0,007 | +0,05 | +0,100 | +0,62 |
| 0,75 | None | +0,068 | +0,57 | +0,170 | +1,28 |
| 1,0 | None | +0,046 | +0,47 | +0,146 | +1,35 |
| 0,75 | 1,0 | +0,027 | +0,33 | +0,035 | +0,41 |

Jedes feste Target (egal welcher smul) verschlechtert avgR/Sharpe gegenueber reinem Zeit-Exit — die Kante braucht Platz zum Laufen, kein Gewinnmitnahme-Deckel. Enge Stops (smul 0,25/0,5) sind IS praktisch bei Null. Bester Kandidat: **smul=0,75, tmul=None**.

**(c) Jahres-Stabilitaet — solide, kein Tail-Ritt.** Mit smul=0,75/tmul=None: 8 von 10 Jahren netto positiv (nur 2016 mit -1,4R quasi flach, 2020/2022 leicht negativ mit -7,1R/-7,0R). IS-Periode selbst schon positiv (+54,2R, 793 Trades), OOS staerker (+89,1R, 525 Trades) — kein reines "OOS-Glueck". Top-5-Gewinntrades nur 3,6% der Bruttogewinne, groesster Einzeltrade 5,0% des Gesamt-NetR, staerkstes Jahr (2024) 28,7% des Gesamt-NetR — keine gefaehrliche Konzentration.

**(d) Fensterlaenge-Sweep (cum_delta-Gegenrechnung) — keine saubere Kausalitaet fuers enge Fenster.** Fensterlaengen 15/30/45/60/90/120 Min. ab 09:30 (Entry direkt am Fensterende, smul=0,5 fix) zeigen KEIN monotones "kuerzer=besser": 15min stark (IS Sharpe +0,80), 30min schwach (+0,05), 90/120min wieder stark (+0,87/+0,70). Bei smul=0,5 ist der Stop zu eng fuer 30min-Trades, bei smul=0,75 wird schon das 30min-Fenster robust profitabel (siehe b). **Interpretation:** die Kante haengt primaer an der Stop-Kalibrierung (genug R fuer Marktrauschen), nicht an der Fensterlaenge selbst. Die alte Beobachtung "cum_delta funktioniert nicht" aus der IVB-Runde war vermutlich ein Artefakt der Breakout+d_ratio-Kombination (#068: Level-Break ohne Follow-Through), nicht des Signalfensters.

**(g) SHORT-Seite — faellt durch.** Bei jeder getesteten smul/tmul-Kombination ist die IS-Periode (2016-2021) praktisch bei Null (bestes Ergebnis smul=0,75/tmul=None: avgR 0,000, Sharpe +0,01). Die gesamte positive Gesamtperformance (+60,0R) stammt fast vollstaendig aus der OOS-Periode (+59,7R von +60,0R). Das verletzt das eigene Selektionskriterium (IS UND OOS muessen tragen) — SHORT ist eher Regime-Glueck (2022er Baeren-Start) als robustes Signal und wird NICHT aufgenommen.

**Overlap-Check final (fuer smul=0,75/tmul=None neu gerechnet, nicht die alte Breakout-Config):** 28% Tagesueberlappung mit NQ_Momentum, Tages-PnL-Korrelation (Union) +0,17, auf gemeinsamen Tagen +0,49. Performance ist auf Tagen MIT und OHNE gleichzeitiges Momentum-Signal fast identisch (avgR +0,104 vs. +0,106) — kein verstecktes Duplikat, die Kante traegt unabhaengig vom Momentum-Zustand.

**Engine-Verifikation:** Modul `engine/or_delta.py` (Mode `or_delta` in `qbt.run_strategy`) gebaut und gegen die volle Engine-Datenreihe (2016 bis Juli 2026) gegengerechnet — reproduziert den Vault-Befund (avgR +0,098, PF 1,18, n=1391), 2026 bislang flach (Teiljahr).

**Portfolio-Whatif (6. Bein zum aktuellen Buch, `book_state.json`, Lucid Flex 50k, Target 3000/DD 2000, `engine/or_delta_portfolio_whatif.py`, reiner Lesezugriff, KEIN Schreiben in book_state.json):** |corr| bleibt niedrig (0,08 → 0,11 mit 6. Bein), aber die Passquoten-Frontier verbessert sich in der aktuellen Monte-Carlo-Rechnung NICHT klar (z.B. frac 0,14: 49%/49d Basis vs. 48%/44d mit 6. Bein; frac 0,18: 46%/28d vs. 45%/29d). Das Bein ist eigenstaendig profitabel und niedrig-korreliert, hilft im gepruften Sizing-Modell aber nicht messbar beim Passquote-Tempo — Nutzen liegt eher in Diversifikation als in Geschwindigkeit.

**Verdict: LONG-Seite besteht statistisch als Kandidat "OR_DELTA_BIAS_NQ" (Familie Intraday Bias), SHORT-Seite ist Friedhof.**

**Max' Entscheidung (10.08.2026): No-Go fuer die Bein-Aufnahme.** Ein statistisch sauberes, eigenstaendiges, niedrig-korreliertes Bein ist nutzlos fuers Buch, wenn es die Passquoten-Frontier nicht verbessert (siehe Portfolio-Whatif oben: frac 0,14 sogar leicht schlechter mit 6. Bein). Aufnahme-Kriterium ist nicht "positive Edge", sondern "verbessert den Betriebspunkt" — Ticket AP82 daher wieder geloescht (Ticket-Workflow: erledigt = geloescht, nicht archiviert). Code/Modul bleiben als Referenz liegen (`engine/or_delta.py`), falls ein anderes Sizing-Modell oder ein spaeteres Buch mit anderer Bein-Mischung den Nutzen doch zeigt.

Skripte (Vault, Analyse): `Quantpad Data/fixed/or_delta_bias_lab.py`, `or_delta_bias_deepcheck.py`, `or_delta_bias_overlap.py`. Engine-Modul: `engine/or_delta.py`. Whatif: `engine/or_delta_portfolio_whatif.py`.

### Lehre
30. **Ein Kontroll-Check gegen "einfach long halten" ist Pflicht, bevor ein Delta-Filter als Kante gilt — aber er muss beim GLEICHEN Stop laufen wie das Signal, nicht bei irgendeinem.** Bei engem Stop sah der naive Long-Halt hier sogar negativ aus, bei weiterem Stop weniger dramatisch — das Ergebnis des Kontroll-Checks haengt selbst von der Stop-Kalibrierung ab, ein einzelner Vergleichspunkt waere irrefuehrend gewesen.
31. **Ein IS-Sharpe von praktisch Null ist ein Stop-Schild, keine Randnotiz — auch wenn die OOS-Zahlen gut aussehen.** Die SHORT-Seite haette bei laxerer Pruefung ("Gesamtsumme positiv") durchgewunken werden koennen; erst die getrennte IS/OOS-Betrachtung zeigt, dass die gesamte Kante aus einem einzigen Regimefenster stammt.
32. **Positive Edge ist eine notwendige, keine hinreichende Bedingung fuer Bein-Aufnahme.** OR_DELTA_BIAS_NQ ist statistisch sauber (8/10 Jahre positiv, IS+OOS beide tragend, niedrig-korreliert) und wird trotzdem nicht aufgenommen, weil es die eigentliche Zielgroesse — die Passquoten-Frontier des Buchs — nicht verbessert. Das eigentliche Aufnahmekriterium ist der Betriebspunkt, nicht die Einzel-Edge (Praezedenz: #076 Sizing-Split wirkt nur, wo die Mindestgroesse es nicht auffrisst — gleiches Prinzip, hier eben negativ ausgefallen).

## Nächste Kandidaten (noch offen)
- **Replace-Test: NQ_Momentum → MOMSEL_NQ_er0.3_s0.75** (siehe #057 — wartet auf Max' Go)
- ~~Momentum selektiver~~ → in #057 getestet, NQ 8/8 robust (siehe oben)
- ~~Intraday Time Series Reversal auf Index (SSRN 5807282)~~ → in #056 als on_rev/min30-Variante mitgetestet (eod-Variante war stärker)
- Overnight-Intraday Reversal (SSRN 2730304)
