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

## Nächste Kandidaten (noch offen)
- **Replace-Test: NQ_Momentum → MOMSEL_NQ_er0.3_s0.75** (siehe #057 — wartet auf Max' Go)
- ~~Momentum selektiver~~ → in #057 getestet, NQ 8/8 robust (siehe oben)
- ~~Intraday Time Series Reversal auf Index (SSRN 5807282)~~ → in #056 als on_rev/min30-Variante mitgetestet (eod-Variante war stärker)
- Overnight-Intraday Reversal (SSRN 2730304)
