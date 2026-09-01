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

## #080 — MOMSEL-Replace-Test v2: alter "klarer Gewinn" repliziert nicht (10.08.2026)
- **Anstoß:** Max' neues Dauerkriterium (10.08.): einzige Messlatte für jede Entscheidung ist die **Passquoten-Frontier, ehrlich gerechnet** (aktuelles Buch, gefixte Engine, Intraday-DD nach #077). Der alte Replace-Test vom 03.08. (`_test_momsel_replace.py`: 53,2%→55,0%, "KLARER GEWINN") war auf drei Achsen veraltet: 9-Bein-Buch, Vor-Bugfix-Pipeline (#074/#075), nur EOD-Bust-Check.
- **Neuauflage `momsel_replace_v2.py`** (Methodik = #078: `book.cell_daily` + `passmc_vec`, EOD+Intraday, Fracs 0.10-0.22, 8000 Sims): NQ_Momentum vs. identisches Bein + `rev_er_min=0.3` im aktuellen 5-Bein-Buch.
- **Ergebnis: das Pass-Delta ist überall MC-Rauschen** (−1,2 bis +0,5pp). Konsistent ist nur das **Tempo-Signal**: Tage-bis-Pass sinken in allen 8 Zellen oder bleiben gleich, am stärksten bei frac 0.10 (EOD 94→73d, Intraday 86→64d bei gleicher/leicht besserer Quote 48,2→48,7%). Solo bleibt MOMSEL klar besser (expR 0,168 vs 0,125, PF 1,30 vs 1,21, 83 statt 122 Tr/J).
- **Verdict nach Kriterium: gekoppelt an den Betriebspunkt.** Bei frac ≈0.10 (wohin #078 unter Intraday-DD ohnehin zeigt): Replace lohnt — gleiche Quote, ~25% schneller = besserer Zeit-bis-Funded-EV. Bei frac 0.18-0.22: kein relevanter Unterschied → Original behalten (Simplex beats Komplex). **Entscheidung hängt an AP53 (Betriebspunkt-Wahl) und liegt bei Max.**
- Ergebnis: `momsel_replace_v2_results.json`. Der alte 03.08.-Lauf gilt nicht mehr als Entscheidungsgrundlage.

### Lehre
33. **Ein Verdict ist nur so aktuell wie seine Pipeline.** Derselbe Test, 7 Tage später auf ehrlicher Basis gerechnet, dreht von "klarer Gewinn" auf "Rauschen mit Tempo-Vorteil". Vor jeder Buch-Entscheidung prüfen, ob das zugrundeliegende Ergebnis noch auf dem aktuellen Buch, der gefixten Engine und dem Intraday-Check steht.

## #081 — Intraday-Bust-Vergleich fürs AKTUELLE Buch: Portfolio-Tab-Kopfzahl bei frac 0.22 um 9,1pp zu optimistisch (11.08.2026)
- **Anstoß:** Ticket `max-1786396290151` — `funded_frontier.passmc` (Basis von `funded_finalize.py`/Portfolio-Tab) prüft den Bust NUR am Tages-Close, `dw` fließt dort nur in die Sizing-Formel. #077/#078 hatten den Intraday-Effekt schon fürs damalige #071/#076-Buch beziffert, das aktuelle 5-Bein-Buch (`book_state.json`: NQ_Momentum, NQ_LastHour, RTY_Gap-fade, NQ_ORB-fade, NQ_Asia-Dir-USopen) war seither nicht mehr auf dieser Basis nachgerechnet.
- **Lauf:** neues Skript `goal_intraday_check_current.py`, Beine wie `funded_finalize.py` sie lädt, `goal30_search.passmc_vec` (E8-50k-Default TARGET 3000/DD 2000), Fracs 0.10-0.30, 8000 Sims, `dd_mode` eod vs. intraday. Sanity-Check: eod-Reproduktion trifft `portfolio.json`s Frontier auf <1pp/<1 Tag (z.B. frac 0.22: 43,3%/17,8d gegen dort dokumentierte 43%/18d).

| frac | eod % | eod Tage | intraday % | intraday Tage | Δ pp |
|---|---|---|---|---|---|
| 0.10 | 54,1 | 94,0 | 48,2 | 85,9 | −5,9 |
| 0.12 | 50,8 | 58,4 | 44,7 | 50,3 | −6,1 |
| 0.14 | 48,7 | 47,0 | 42,9 | 40,5 | −5,8 |
| 0.18 | 45,2 | 25,9 | 38,5 | 22,7 | −6,8 |
| **0.22** | **43,3** | **17,8** | **34,2** | **14,6** | **−9,1** |
| 0.26 | 41,7 | 13,0 | 30,5 | 9,7 | −11,2 |
| 0.30 | 40,7 | 11,3 | 28,1 | 8,1 | −12,6 |

- **Betriebspunkt frac 0.22 (aktuell im Tab):** eod-Kopfzahl 43,3%, ehrlich unter #077-Mechanik (Floor trailt EOD, Bruch wird kontinuierlich geprüft) nur 34,2% — 9,1pp weniger, Bust bei Fail auch schneller (Median 14,6 statt 17,8 Tage). Der Effekt wächst mit dem frac (0,30: −12,6pp): je aggressiver gesized wird, desto mehr überschätzt der reine EOD-Check.
- **Entscheidung Max (11.08.2026): Portfolio-Tab/`book_state.json`/`funded_finalize.py`-Default bleiben auf EOD.** Dies ist ein einmaliger Vergleichslauf, keine Umstellung — `portfolio.json` wurde nicht neu geschrieben, `funded_finalize.py` nicht ausgeführt. Grund: die E8-Bust-Mechanik ist zwar schriftlich bestätigt (#077/AP51), aber Max will die Umstellung des Tabs bewusst separat entscheiden statt sie an diesem Ticket mitlaufen zu lassen. Ticket `dd-mode-intraday-default` (Epic GROUNDTRUTH) bleibt dafür offen.
- Ergebnis: `goal_intraday_check_current_results.json`. Ticket `max-1786396290151` geschlossen (gelöscht aus `tasks.json`), Ergebnis hier archiviert statt im Tracker.

### Lehre
34. **Eine bestätigte Firmenregel (#077) ist kein Freifahrtschein, sie automatisch überall einzubauen.** Die ehrliche Zahl existiert jetzt für das aktuelle Buch, aber ob der Tab künftig darauf umstellt, ist eine bewusste zweite Entscheidung — sonst verwischt der Unterschied zwischen "wir wissen es jetzt" und "wir haben uns danach gerichtet".

## #082 — AP73 (MAE-Doppelzählung) verifiziert: Portfolio-Tab unbetroffen, echter Nutzen kleiner als #075 dachte (11.08.2026)
- **Anstoß:** Ticket `mae-bug-3-stellen` (AP73, Fund 4 aus #075) — der Fix (`book.py:43` war schon korrekt, `qbt.py::prop_pass_probability` und `copilot.py::_daily_pnl_arrays` jetzt gefixt: `prev_cc = cc − eigener Close` statt `cc` direkt vor dem MAE-Abzug) sollte laut Ticket-Text einen breiten Blast Radius treffen (`funded_frontier.py`, `portfolio.py`, `run_copilot.py`, `copilot.py` Report-Tab, `matteo_vwap_drift.py`).
- **Sanity-Check bestanden:** alle drei Funktionen liefern jetzt für dasselbe Bein bitidentische „worst equity"-Werte (max. Diff 0,0 $; `book.py`s minimale Restabweichung von 2,02 $ kommt vom dortigen MAE-Clipping, nicht von der Formel).
- **Wichtigste Korrektur am Ticket-Text: `funded_finalize.py`/`portfolio.json` sind vom Bug NICHT betroffen.** Der Pfad läuft über `funded_frontier.passmc` → `book.cell_daily`, und `book.py` hatte die Formel schon immer richtig. Der im Ticket vermutete Blast Radius war für den Portfolio-Tab falsch — **`portfolio.json` wurde deshalb bewusst nicht neu geschrieben, `book_state.json`/Betriebspunkt bleiben unverändert** (frac 0.22 = 43%/18d aus #081, EOD-Basis).
- **Der reale Fix-Effekt zeigt sich nur im `copilot.prop_assistant`/`qbt.prop_pass_probability`-Pfad** (Lab Report-Tab, `run_copilot.py`, `matteo_vwap_drift.py`). Gegengerechnet auf dem AKTUELLEN 5-Bein-Buch (flat Sizing, intraday DD, E8 Futures 50k, gleicher Seed alt/neu):

| Size | vorher | nachher | Δ |
|---|---|---|---|
| 1u | 25,1% | 26,3% | +1,2pp |
| 2u (beste Größe) | 35,0% | 38,6% | +3,6pp |
| 3u | 31,7% | 36,4% | +4,7pp |

- **Das ist deutlich weniger als #075s Erwartung** (1u 41%→51%, 3u 23%→31%, beste Größe 37%→42%) — kein Widerspruch, sondern Buch-Drift: #075 rechnete auf dem damaligen Buch, seither ist IVB raus, OR_DELTA_BIAS verworfen (#079), das Buch mehrfach umgebaut. **Die #075-Prozentsätze sind für das heutige Buch nicht mehr gültig und sollten nicht mehr zitiert werden.**
- Nebenbei mitgeprüft (Cache-Rebuild für Discovery, nicht Teil des Bugs selbst): `goal30_inventory.py` neu gelaufen (97 Kandidaten, ~14,5 Min, keine Fehler) → `goal30_cells_wide.pkl` aktuell. `goal30_cells.pkl` (schmal, ohne „_wide") ist stale (09.08.), wird von keinem vorhandenen Skript mehr geschrieben — bewusst liegen gelassen, keine aktive Nutzung erkennbar.
- Ticket `mae-bug-3-stellen` (AP73) damit geschlossen (aus `tasks.json` gelöscht), Ergebnis hier archiviert.

### Lehre
35. **Ein „Blast Radius" im Ticket-Text ist eine Hypothese, keine geprüfte Tatsache** (AP73). Zwei von drei Bug-Fundorten trafen zu, der dritte (Portfolio-Tab) hing über einen anderen Call-Pfad (`book.cell_daily`) an einer bereits korrekten Formel. **Nach jedem Fix den tatsächlichen Call-Graph prüfen, nicht nur die Symptom-Liste aus der ursprünglichen Diagnose abarbeiten** — sonst hält man einen Tab für „jetzt auch gefixt", der es nie kaputt war, oder umgekehrt einen für „unberührt", der es war.

## #083 — IVB-Nachtest mit exakter Paper-Spec: auch die Original-Regeln haben keine Edge (11.08.2026)
- **Anstoß:** Max lieferte das Original-PDF ("The Institutional Protocol", Matteo Conti / @matfinog, 16 Seiten) mit dem kompletten EasyLanguage-Quellcode des Fabio-Valentini-IVB-Modells. Der #079-Test (`ivb_test.py`) hatte die Range als 09:30-10:00 RTH interpretiert — die Paper-Spec weicht materiell ab: **Range 08:30-09:00 NY (Pre-Market inkl. Makro-Prints), LONG-only, ein Entry/Tag, Entry = erster 5m-Close > ORB-High zwischen 09:00 und 14:00, Filter BarDelta ≥ 200 auf der Signal-Bar, Stop = ORB-Low, TP = 1R, flat 14:00** (Prosa sagt 15:00, Inputs sagen 14:00 → beides getestet).
- **Nachtest `Quantpad Data/fixed/ivb_paper_exact_083.py`** auf `NQ_full.parquet` (1m, voller Globex, NY-Zeit, 2016-2026/07), ehrliche Fills (F1 next-1m-open, F4 Stop gewinnt Same-Bar, F5), Kosten 0,87 Pkt/RT. Delta als Tick-Rule-Proxy (echtes Bid/Ask-Delta haben wir nicht), Schwellen-Sweep 200-12000 inkl. Frequenz-Matching auf deren 823 Trades.
- **Ergebnis: tot, in jeder Variante.** Deren Fenster 2021-2026/04: ohne Filter n=1073, **Win 50,5%, PF netto 0,96, −24,0k$**; mit Delta-Proxy>0 Win 50,9%, PF netto 0,97; flat-15:00-Variante identisch tot. Pre-Sample 2016-2020 ebenso negativ. Schwellen-Sweep nicht-monoton (thr=6000: netto +$10,63/Trade PF 1,01 = Rauschen; thr=8000/12000 wieder negativ). **Die Paper-Zahlen (Win 58,3%, PF 1,31, avg $201/Trade) sind auch mit der exakten Spec nicht ansatzweise reproduzierbar** — wir finden ~50% Win und avg −$5 brutto.
- **Warum das Paper trotzdem "VALIDATED" sagt:** Das eigene Statement of Limitations gibt es zu — die gesamte Validierung (Bootstrap, 1.000 Permutationen, 20.000 MC-Sims, Kosten-Rerun) läuft auf dem **vom Autor gelieferten MultiCharts-Trade-Log**, "no independent re-execution of the strategy on raw market data was performed". Alle vier "unabhängigen" Tests resampeln dieselbe Liste; wenn die Liste optimistisch erzeugt ist, erben sie den Fehler. Wahrscheinlichste Quellen der ~8pp-Win-Differenz: MC-Intrabar-Auflösung von TP/SL auf 5m-Bars ohne Bar Magnifier + synthetisches BarDelta auf Historien-Daten ohne Tickdaten — exakt die #066-Fallenklasse.
- **Verdict: IVB bleibt Friedhof, jetzt endgültig** (beide Interpretationen getestet: RTH-Range #079 UND Paper-Spec Pre-Market-Range #083). Der Beifang OR_DELTA_BIAS (#079) bleibt davon unberührt in der Bank.

### Lehre
36. **"Institutional-grade validation" eines Trade-Logs ist keine Validierung der Strategie.** Bootstrap/Permutation/Monte-Carlo prüfen nur, ob eine Zahlenliste statistisch signifikant ist — nicht, ob die Liste ehrlich zustande kam. Der einzige Test, der zählt, ist die Re-Execution der Regeln auf Rohdaten mit ehrlichen Fills. Steht im Kleingedruckten sogar selbst drin ("no independent re-execution").

## #084 — Erster vollautomatischer Deploy auf die Box: RiskPerMicro 104 live, dabei zwei stille Selbstzerstörungs-Fallen im Deploy-Pfad gefunden (11.08.2026)
- **Anstoß:** AP78 (RiskGuard `RiskPerMicro` 80 → 104) und AP83 (Sammel-Compile inkl. AP72 Asia-Entry-Fix) sollten endlich durch. Bisher hieß der Weg dahin „RDP auf den VPS, F5 drücken". Diesmal komplett per SSH von Max' PC aus gefahren (`ssh Administrator@100.127.89.9`, `box_deploy.ps1`), ohne einen einzigen Klick am Chart.
- **Vorher geprüft statt angenommen:** Session lief (17:25, US-Session bis 22:00) und NT8 war oben — aber der NT8-Log des Tages hatte **2 Zeilen, beide nur Verbindung**. Keine Strategie, keine Order. Damit war der Deploy mitten in der Session gefahrlos. Der Umweg über den Log ist billiger und ehrlicher als die Annahme „ist ja eh alles aus".
- **Falle 1, Staging als Zombie-Lager (→ AP84, rot):** im `_staging` lagen noch 8 `.cs` vom 09.08.-Deploy, darunter `MaxORBBreakoutNQ`, `MaxORBScalpNQ`, `MaxORBScalpNQ2` — **drei Beine, die auf der Box längst nicht mehr deployed sind.** `box_deploy.ps1` kopiert stumpf alles aus dem Staging in den Strategies-Ordner. Ein ahnungsloser Lauf hätte die drei wieder in den Baum geholt. Aufgefallen nur, weil vorher manuell abgeglichen wurde.
- **Falle 2, das Skript stellt sich selbst die Falle (→ AP85, rot):** der erste Build starb mit **18× CS2001**. Die `NinjaTrader.Custom.csproj` listete noch 10 Dateien aus `Strategies\_bak-20260809-2225` und 9 generierte `obj\Release`-Dateien, die alle nicht mehr existieren. Ursache ist die bekannte NT8-Eigenart (F5 schreibt *alles* unterhalb `bin\Custom` in die csproj) — nur andersherum als bisher gedacht: **`box_deploy.ps1` räumt in Schritt 6 selbst obj/bin weg und hinterlässt damit die toten Referenzen für den nächsten Build.** Der bekannte CS0579-Fehler und dieser CS2001-Fehler sind zwei Seiten derselben Münze. Einmalig behoben (`fix_csproj.ps1`, 441 → 422 Zeilen, Backup im `_bak_archiv`), danach Build sauber.
- **Ergebnis live:** `RiskPerMicro = 104` und der AP72-Fix (`Calculate.OnEachTick`) liegen deployed im Strategies-Ordner, DLL neu gesetzt 17:40:47, Pre-Flight und Build fehlerfrei, Baum sauber. Wichtiger Nebenbefund: der **Workspace hatte keinen serialisierten `RiskPerMicro`-Wert** — der Code-Default greift also wirklich, statt von einer gespeicherten 80 überschrieben zu werden. Das war nicht selbstverständlich und ist der Grund, warum der Fix überhaupt wirkt.
- **Grenze der Fernsteuerung (→ AP86):** NT8 ließ sich per interaktivem Task in Session 2 starten (PID 3444), blieb dann aber über zehn Minuten bei 17-31 MB RAM, eingefrorener CPU und einer einzigen Logzeile stehen. **Sobald Max sich per RDP anmeldete, lief er sofort durch** (438 MB, `E8: Primary connection=Connected, Price feed=Connected`, Workspace restored). Ursache ist also nicht ein Wiederherstellungsdialog, sondern die **fehlende angemeldete Desktop-Session** — ohne aktiven Desktop hängt NT8 beim UI-Aufbau. **Deploy und Build sind fernsteuerbar, der Wiederanlauf nicht.** Fix-Richtung: Autologon, oder die RDP-Session konsequent nur trennen statt abmelden.
- **Vorher-Prüfung, die sich gelohnt hat:** der komplette Post-Deploy-Zustand wurde vorab in einem Wegwerf-Ordner kompiliert (`_check_compile.ps1 -SrcDir`), bevor NT8 überhaupt angefasst wurde. Hätte der neue Code nicht gebaut, wäre die Box nie gestoppt worden.

### Lehre
37. **Ein Deploy-Skript, das aufräumt, muss auch die Referenzen aufräumen.** Ordner löschen und Projektdatei stehen lassen heißt: der Lauf, der aufräumt, ist grün — der *nächste* stirbt. Solche Fehler datieren sich selbst in die Zukunft und treffen einen garantiert dann, wenn es eilig ist. Gilt für jedes Skript, das Artefakte entfernt: **was auf die gelöschten Pfade zeigt, muss im selben Schritt mit.**
38. **Ein Staging-Ordner ohne Verfallsdatum ist ein Wiederbelebungsapparat für gelöschte Beine.** Was einmal deployed wurde, gehört sofort raus. Sonst entscheidet nicht `book_state.json` darüber, was live läuft, sondern der Altbestand eines Ordners, in den keiner mehr reinschaut.
39. **„Der Prozess läuft" ist kein Gesundheitszeichen.** NT8 stand mit `Responding=True` in der Prozessliste und war trotzdem nicht handelsbereit — verraten haben es erst RAM (17 MB statt 438), eingefrorene CPU-Zeit und ein Log, das bei einer Zeile stehenblieb. Genau darauf schaut der Watchdog aktuell nicht: er prüft nur, **ob** NT8 existiert. Ein NT8, das nach einem Reboot in dieser Halbtot-Lage hängt, würde er als grün melden.

## #085 — AP77 final geklärt: Sizing-Split zwischen zwei Evals erlaubt, News-Sperre bei Futures existiert nicht (11.08.2026)
- **Anstoß:** Ticket `e8-support-copytrading-klaeren` (AP77) — vor dem Kauf von zwei parallelen 25k-Evals (#076-Plan, frac 0,10/0,80, P(funded) 57,0% statt 48,4% auf einem Konto) musste geklärt sein, ob E8s Copy-Trading-Verbot das trifft. Quelle bis dahin nur ein Suchmaschinen-Snippet (403 auf Primärseite), Konfidenz „praktiker".
- **Erste Support-Antwort (Fábio, 18:04)** war generisch: „Copying between your own Challenge, Performance, or personal accounts" ist erlaubt, verboten nur Signaldienste/Team-Trading. Deckte das konkrete Szenario (zwei GLEICHZEITIG aktive Evals) nicht explizit ab und verlinkte für die News-Frage die allgemeine/Forex-Domain statt Futures — also nachgefasst, explizit für **E8 Signature Futures** und den **Parallel-Eval-Fall**.
- **Nachfass-Antwort (Fábio, 19:08), beide Punkte final geklärt:**
  1. *„Yes, if both challenge accounts will be only trade by you, it does count as copying your own trades."* → **Sizing-Split zwischen zwei gleichzeitigen Evals ist erlaubt.** #076-Parallelplan freigegeben, Kauf der zwei 25k-Konten kann erfolgen.
  2. *„You can trade news with no restrictions in the Signature program [...] we recommend that users avoid trading during high-impact news"* → **kein hartes News-Trading-Verbot bei E8 Signature Futures**, weder Eval noch Funded — nur eine Empfehlung. Löst den Widerspruch 5min/5min vs. 2min/3min auf: **beide Zahlen waren falsch/veraltet, es gibt gar keine Pflicht-Sperrzeit.**
- **Konsequenzen:**
  - `dialin`-Epic: `ein-oder-zwei-konten` kann jetzt zugunsten des Parallelplans entschieden werden (hängt weiterhin an AP53/Betriebspunkt, aber die Blockade durch die Regelfrage ist weg).
  - `gatekeeper`-Epic: `e8-zwei-konten` (rot) kann geschlossen werden, die 57,0%-Zahl aus #076 ist buchbar.
  - RiskGuard hat aktuell `NewsFlatEnabled` aktiv (#048) — das war eine Vorsichtsmaßnahme auf Verdacht, keine Firmenpflicht. Bewusst NICHT automatisch abgeschaltet, das ist eine eigene Entscheidung wert (Empfehlung von E8 selbst ist ja durchaus vernünftig, auch ohne Zwang).
- Beide Screenshots + vollständiger Wortlaut archiviert in [[E8-Support-Anfrage (Sizing-Split + News-Fenster)]], [[Research-Cache]] aktualisiert (beide Einträge jetzt „bestätigt"). Ticket `e8-support-copytrading-klaeren` (AP77) gelöst, aus `tasks.json` gelöscht.

### Lehre
40. **Eine generische erste Support-Antwort ist noch keine Antwort auf die eigentliche Frage** (AP77). Fábios erste Nachricht klang nach „ja, erlaubt", hätte aber weder das exakte Parallel-Szenario noch das richtige Programm (Futures vs. E8 One) sauber abgedeckt. Erst die gezielte Nachfrage mit den exakten Stichworten aus der eigenen Frage brachte die belastbare, direkt zitierbare Bestätigung. **Bei geldrelevanten Regelfragen die erste Antwort auf Präzision prüfen, nicht auf Freundlichkeit — im Zweifel nachfassen, bevor Geld fließt.**

## #086 — Wochen-Review W32 (03.08.–11.08.): keine Decay-Ampeln, aber die Sim-Validierung ist zurück auf Null (11.08.2026)
- **Anstoß:** Tickets AP8 + AP50 (Wochen-Review: Ampeln + Journal + Logbuch). Vollständiger Report: [[Wochenreport 2026-W32 (03.08-11.08)]].
- **Ampeln:** keine roten/gelben Edge-Decay-Ampeln. Momentum (n=12, +2.320,50 $, z=+2,55) und PowerHour (n=15, +1.557 $, z=+2,29) laufen **über** Backtest-Erwartung — bei dem N Klein-Stichproben-Glück, kein Edge-Beweis, aber sicher kein Decay. ORB-Fade (neuer Limit-Port), GapFade, AsiaDir: **0 Live-Trades**, grau.
- **Live-Woche Simtestsim2 (aus Fills rekonstruiert):** 04.08. +1.069 · 05.08. −146,50 · 06.08. −28,25 · 07.08. −190,50 → **+703,75 $**, 9 Round-Trips. Danach nichts mehr.
- **Der eigentliche Befund: die Sim-Phase misst seit dem 07.08. nichts.** Letzte Bar 07.08. 09:46 ET, NT8-Prozess 22:22 down, Watchdog hat den Dauerzustand nicht als solchen gemeldet (AP87). Dazu endet `maxlab_equity.csv` schon am 05.08. (keine EOD-Zeilen für 06./07.08. trotz Trades — beim Sim-Neustart prüfen, zusammen mit dem noch offenen 3-Spalten-Fix aus #058). Ab 10.08. zusätzlich FIREFIGHT (bewusst alles aus).
- **Sim-vs-Backtest-Verdict:** 3 von 5 Beinen ohne einen einzigen Live-Trade, das Buch selbst steht zur Disposition (AP53) → **Sim-Neustart erst nach der Buch-Entscheidung**, sonst validiert man zwei Wochen ein Buch, das danach umgebaut wird.
- Tickets AP8 (`review-2026-30`) + AP50 (`review-2026-32`) geschlossen und aus `tasks.json` gelöscht. Nebenbei Logbuch-Hygiene: der AP77-Eintrag lief doppelt als „#083" — auf **#085** umnummeriert (Referenzen in [[Ticket-Epics]] + [[E8-Support-Anfrage (Sizing-Split + News-Fenster)]] mitgezogen), Lehren-Nummerierung fortlaufend gefixt.

### Lehre
41. **Eine Sim-Phase ohne überwachte Datenpipeline validiert nichts.** Vier Tage toter Feed sind unbemerkt durchgelaufen, weil der Watchdog Frische ohne Datum meldete — der Abgleich war blind, obwohl alles „grün" aussah. Vor jedem Sim-(Neu-)Start gehört die Messstrecke selbst geprüft: frische Bars, Equity-Zeilen pro Handelstag, Fills-Sync. Und: eine Ampel, die **über** Erwartung steht, ist genauso ein Prüfsignal wie eine darunter — erst die Stichprobengröße macht daraus eine Aussage.

## #087 — Discovery-Batch AP49: MOC-These falsifiziert, VIX-Fear-Reversion überlebt (Bank) (11.08.2026)
- **Anstoß:** Ticket AP49 (wöchentlicher Discovery-Batch). Vom Ticket-Text waren Frequenz-Bein (#043 tot) und OpEx-Momentum (#049/#054 fertig) schon abgearbeitet — der echte Backlog der Idea Engine gab zwei Mechanismen her: **MOC-Imbalanz** (letzter offener Punkt der Kalender-Karte) und **Cross-Asset/VIX**. Multi-Day-Pairs bleibt gesperrt (Overnight-Verbot), Turn-of-Month bleibt Watchlist. 96 Configs, ehrliche Engine, IS/OOS-Split 01.01.2024, Klein-N-Skepsis (Edge ≥3% bei n<200). Skript: `moc_vix_discovery.py`, neues Engine-Modul `vix_bias.py` (mode `vix_bias`).
- **MOC-Imbalanz: 0/72 Survivors, These falsifiziert.** WHY vorab: MOC-/Leveraged-ETF-Rebalancing verstärkt die Tagesrichtung in den Schlussminuten → Late-Entry-Momentum (15:00/15:30/15:45 ET) müsste zum Close hin BESSER werden. Ergebnis ist das Gegenteil: ref 15:00 grenzwertig (bestes MOC_NQ PF 1,13, OOS kippt), 15:30/15:45 klar negativ, auf allen 4 Indizes. Der handelbare Teil des Late-Day-Momentums steckt schon im Power-Hour-Bein (Entry 13:30) — danach ist nur noch Rauschen plus Kosten. Kalender-Karte damit **komplett abgearbeitet und geschlossen**.
- **VIX-Fear-Reversion: 8/24 Survivors, sauber einseitig.** WHY vorab (Vol-Risk-Premium/Leverage-Effekt): VIX-Spike gestern = Angst-Overshoot → positive Drift am Folgetag. Signal ausschließlich aus Vortags-Closes (VIXCLS/FRED), kein Lookahead. **Alle 8 Survivors sind die Long-Seite (spike_rev), der Short-Gegentest (spike_mom) ging 0/12 unter** — genau das Muster, das man sieht, wenn die These stimmt, statt eines Data-Mining-Artefakts. Beste Config: `VIX_spike_rev_NQ_t0.12_s0.75` (VIX-Anstieg ≥12% → NQ Long open→EOD, Stop 0,75×ATR20): Verdict **A (Score 100)**, win 54,1% vs. Baseline 43,8%, OOS PF **1,91**, +5.771 $ OOS.
- **Aber: Klein-N und kein Passquoten-Gewinn.** 170 Trades gesamt, ~16/Jahr — VIX-Spike-Tage sind selten. Auto-Fit: Buch 55%/96d vs. mit VIX-Bein 55%/**90d** (corr 0,07) → **abgelehnt, Bank**. Grenzfall: gleiche Passquote, aber 6 Tage schneller — bei Reset-Strategie zählt Tempo mit (#076). Entscheid liegt bei Max: **AP89**.
- **Daten-Lücke dokumentiert:** Vom Cross-Asset-Backlog (VIX/ZN/DXY/Breadth) existiert nur VIX als Daten. Bonds, Dollar, Sektor-Breadth sind nicht im QuantPad-Export — Karte wird bei Datenzugang wieder geöffnet.
- **Housekeeping:** Kalender-Karte → Getötet (Sammelkarte fertig), Cross-Asset-Karte → Validiert (VIX-Teil), neue Karte „VIX-Spike-Reversion" (Validiert, Bank). AP49 aus `tasks.json` gelöscht, AP89 (VIX-Entscheid) angelegt. Ergebnisse: `moc_vix_results.json`, Report `VIX_spike_rev_NQ_t0.12_s0.75.html`.

### Lehre
42. **Der Gegentest ist der billigste Artefakt-Detektor.** Beide Richtungen derselben These mitzutesten kostet ein paar Configs, liefert aber das stärkste Ehrlichkeitssignal des ganzen Batches: 8/12 Survivors auf der These-Seite, 0/12 auf der Gegenseite — so sieht ein echter Mechanismus aus. Hätten BEIDE Seiten „funktioniert", wäre es Rauschen gewesen. Und die MOC-Runde zeigt den Wert des vorab dokumentierten WHY: weil die These eine prüfbare Vorhersage machte (Edge steigt zum Close), war ihr Scheitern eine klare Falsifikation statt eines „fast guten" Ergebnisses, dem man hinterheroptimiert.

## #088 — Split-Half-Validierung (AP52): das Zielbuch bricht im Test nicht ein, aber seine Herkunft ist widerlegt (11.08.2026)
- **Anstoß:** Ticket `splithalf-validierung` (AP52) — der strategy-auditor hatte am 10.08. den #071-Fenstertest als ZIRKULÄR entlarvt (die Qualitätsgates verlangten „OOS-expR > 0", die Beine wurden also danach ausgewählt, im OOS-Fenster zu liefern; dazu ~1000 MC-bewertete Kombinationen über 4 Suchläufe). Sauberer Test: Qualifizierung UND Beam-Search NUR auf Train (Jahre < 2022), dann EINMALIGE Bewertung auf Test (≥ 2022) ohne Nachjustieren. Skript: `engine/goal30_splithalf.py`, 97 Kandidaten, 30.000 MC-Sims, Exit-Code 0. (Der Lauf vom 10.08. 00:32 war nach Schritt 1 abgebrochen, ohne Ergebnis-JSON — heute frisch durchgelaufen.)
- **Qualifizierung auf Train: nur 4 von 97 Beinen bestehen** die reinen Train-Gates (expR>0 in 16-19 UND 20-21, top5<60%, ≥55% profitable Jahre): FLIP_NQ_b0.5_WINDOW, FLIP_NQ_b0.75_SIGNALS, FLIP_NQ_b0.75_WINDOW, **NOISE_ORB_NQ**. **Von den 4 Zielbuch-Beinen (#071) qualifiziert sich nur ein einziges: NOISE_ORB_NQ.** RV_leadlag_NQES, NQ_Asia-Dir-USopen und OPEXMOM_NQ fallen schon an den Train-Gates durch. Der Beam-Search auf Train wählte danach sogar nur **1 Bein** (NOISE_ORB_NQ), Runde 2 brach an den Constraints ab.
- **Kernzahlen** (First-Passage-Passquote/Tage, frac wie im Skript, MC 30k):

| Buch | Train | Test (≥2022) | Δpp |
|---|---|---|---|
| Split-Half-Buch (Train-gewählt, 1 Bein) | 47,0%/29d | 52,0% (±0,29)/70d | **+5,0** |
| Buch heute (6 Beine, Referenz) | 34,2%/23d | 61,2% (±0,28)/58d | +27,0 |
| Zielbuch #071 (4 Beine) | 45,6%/22d | 59,6% (±0,28)/50d | +13,9 |

- **Verdict — zweischneidig, aber klar:**
  1. **Kein Einbruch im Test-Fenster** — alle drei Bücher werden ≥2022 sogar besser (Regime-Rückenwind hilft allen). Das Katastrophen-Szenario „Buch bricht ein → reiner Sucheffekt" ist NICHT eingetreten.
  2. **Aber die Herkunft des Zielbuchs ist widerlegt:** eine Suche, die nur Train sieht, findet das 4-Bein-Zielbuch NICHT — 3 der 4 Beine bestehen die Train-Gates gar nicht. Ihre Qualifizierung in #071 stützte sich also (mindestens teilweise) auf Information aus 2022+, exakt der monierte Zirkularitätsfehler. **Die Test-Performance des Zielbuchs (59,6%) ist damit kein unabhängiger Beweis** — das Buch wurde mit Wissen über das Test-Fenster gebaut. Der einzige Teil mit echter Train→Test-Bestätigung ist **NOISE_ORB_NQ solo** (47%→52%, robust).
- **Konsequenz für AP53 (Buch-Entscheidung):** stärkt die 10.08.-Empfehlung **gegen den Umbau** deutlich. Der marginale Frontier-Vorteil des Zielbuchs (#078: 52,4% vs. 47,9% bei frac 0.10, aber 69 statt 37 Tage) stand schon vorher auf der Kippe; jetzt kommt dazu, dass 3 der 4 Zielbeine sucheffekt-verdächtig sind. AP53 ist entblockt und entscheidungsreif.
- **Methodik-Vorbehalt:** der Lauf rechnet mit `dd_mode="eod"`, nicht intraday (#077) — die absoluten Passquoten sind daher NICHT mit den Intraday-Zahlen aus #078/#081 vergleichbar. Für den eigentlichen Zweck (Train-only-Suche vs. #071-Suche) ist das unerheblich, da alle Vergleiche im selben Modus laufen. Ticket `dd-mode-intraday-default` (GROUNDTRUTH) bleibt offen.
- **Skript-Bug gefunden & gefixt:** `goal30_splithalf.py` schrieb in `goal30_splithalf.json` das Feld `train_pass` mit dem Test-Wert (Copy-Paste, Zeile 138: `p` statt `pt`) — die echten Train-Werte standen nur im String-Feld `train`. Gefixt; das vorliegende JSON hat den Fehler noch drin (String-Felder stimmen).
- Ticket `splithalf-validierung` (AP52) geschlossen und aus `tasks.json` gelöscht, `blocked_by` bei AP53 entfernt. Dateien: `engine/goal30_splithalf.py`, `engine/goal30_splithalf.json`, `engine/goal30_splithalf.log`.

### Lehre
43. **„Kein Einbruch im OOS" und „unabhängig bestätigt" sind zwei verschiedene Aussagen.** Der ehrliche Test einer Buch-Konstruktion ist nicht, ob das fertige Buch im Test-Fenster hält (das kann Regime-Glück sein und ist bei zirkulärer Auswahl sogar zu erwarten) — sondern ob eine Suche, die das Test-Fenster nie gesehen hat, **dasselbe Buch noch einmal findet**. Hier fand sie 1 von 4 Beinen. Künftige Buch-Qualifizierung muss strikt Train-only laufen, BEVOR ein Bein ins Buch kommt, nicht als Nachtest.

## #089 — Betriebspunkt unter Kauf-Budget (max. 2 Evals/Monat): die „niedriger frac"-Empfehlung kippt (11.08.2026)
- **Anstoß (Max, 11.08.):** „Ich kaufe höchstens 2 Evals im Monat — welcher frac bringt mir damit die höchste Chance auf funded?" Alle bisherigen Betriebspunkt-Zahlen (#076/#078/#081, AP53) bewerten **ein einzelnes Konto ohne Nachkauf**. Unter einer Kauf-**Rate** ist das die falsche Zielgröße. Neues Skript: `engine/frac_pair_budget.py` (gemeinsame Marktpfade wie #076-Hebel-B, `dd_mode="intraday"` (#077), 6.000 Sims, 12 Monatskohorten rollend, Beobachtungsfenster 24 Monate, Kauf-Stopp nach dem ersten Pass). Ergebnis: `frac_pair_budget_results.json`.
- **Modellannahme (geprüft, #085/Research-Cache):** parallele Evals sind bei E8 unlimitiert und der Sizing-Split zwischen zwei eigenen Evals ist schriftlich erlaubt. **Ungeprüft und kritisch: ob die E8-Eval ein Zeitlimit oder Mindest-Handelstage hat** → AP90.

### Befund 1: Tempo bleibt wertvoll — die Vermutung „Kaufdeckel entwertet Tempo" ist falsch
Die Intuition war: wenn nur 2 Käufe/Monat möglich sind, ist die knappe Ressource der Versuch (nicht die Zeit), also gewinnt der niedrigste frac mit der höchsten Passquote. Gemessen ist das Gegenteil richtig, weil das Kontingent eine **Rate** ist und nicht ansammelbar — ein Konto, das 85 Tage bis zur Entscheidung braucht, verbrennt keine Käufe, sondern Kalendermonate.

E8 **50k**, 1 Konto/Monat rollend, intraday:

| frac | solo pass% | solo Median | P(funded) 3M | 6M | 12M | Ø Kosten |
|---|---:|---:|---:|---:|---:|---:|
| 0.08 | **50,1%** | 94 d | 28,1% | 58,6% | 87,9% | 929 $ |
| 0.10 | 47,8% | 85 d | 30,1% | 59,7% | 87,6% | 914 $ |
| 0.14 | 42,0% | 37 d | 51,3% | 77,6% | 95,7% | 652 $ |
| 0.18 | 38,2% | 21 d | 60,0% | 83,8% | 97,5% | 558 $ |
| **0.22** | 34,3% | 12 d | **62,9%** | **85,7%** | 97,9% | **530 $** |
| 0.30 | 28,0% | 6,5 d | 61,3% | 83,8% | 97,3% | 553 $ |

**Der frac mit der besten Einzelquote ist der mit der schlechtesten P(funded) — und der teuerste.** frac 0.08 hat +16pp Solo-Vorsprung auf 0.22 und liegt nach 3 Monaten trotzdem 35pp zurück, bei 400 $ mehr Erwartungskosten. Grund: bei 94 Tagen Median ist das erste Konto nach 3 Monaten noch nicht einmal entschieden, während gleichzeitig weitergekauft wird.

### Befund 2: der Sizing-Split ist auch hier der Gratis-Hebel (+10pp, und billiger)
Zwei Konten pro Monat auf **demselben** frac bringen fast nichts (corr ≈ 1, exakt der #076-Befund, hier auch für zeitversetzte Kohorten bestätigt). Erst der Split zwischen langsam und aggressiv erzeugt Streuung. E8 **25k**, 2 Konten/Monat:

| Paar | 1M | 3M | 6M | Median | Ø Kosten |
|---|---:|---:|---:|---:|---:|
| 0.10 / 0.10 | 20,4% | 60,3% | 85,1% | 71 d | 733 $ |
| 0.30 / 0.30 | 27,8% | 63,4% | 85,4% | 62 d | 705 $ |
| 0.10 / 0.22 | 29,4% | 69,8% | 90,9% | 52 d | 606 $ |
| **0.10 / 0.30** | **32,7%** | **73,2%** | **92,3%** | **45 d** | **568 $** |

Der Split kostet nichts und liefert +10pp gegenüber zweimal demselben frac — **und senkt die Erwartungskosten**, weil man früher aufhört zu kaufen. Auf 25k sind alle fracs ≤ 0,14 identisch (Min-Size-Effekt aus #029/#076: 1 Kontrakt egal was man einstellt) — die Wahl ist real also „Min-Size-Konto + aggressives Konto".

### Befund 3: 25k schlägt 50k klar, sobald rollend gekauft wird
| Käfig | bestes Paar | 3M | 6M | Ø Kosten |
|---|---|---:|---:|---:|
| **25k (100 $)** | 0.10 / 0.30 | **73,2%** | **92,3%** | **568 $** |
| 50k (150 $) | 0.18 / 0.30 | 70,9% | 90,8% | 898 $ |

Gleiche Barrieren-Ratio (1500/1000 = 3000/2000 = 40%), aber der kleinere Käfig entscheidet schneller und kostet ein Drittel weniger pro Los. 50k gewinnt nur die **Solo**-Quote (50,1% bei frac 0.08) — also genau die Kennzahl, die unter Nachkauf nicht mehr die relevante ist.

### Empfehlung
**2 × E8 25k pro Monat, frac-Split 0,10 / 0,30, rollend nachkaufen bis das erste Konto besteht.** ≈73% funded in 3 Monaten, ≈92% in 6, Erwartungskosten ≈570 $. Vorbehalte: gerechnet auf dem aktuellen 5-Bein-Buch, dessen Herkunft #088 teilweise widerlegt hat — die absoluten Zahlen wandern mit AP53. Die **Richtung** (Tempo + Split + kleiner Käfig) ist davon unabhängig, weil sie aus der Barrieren-/Zeitstruktur kommt, nicht aus der Edge.

### Konsequenzen für offene Tickets
- **AP53:** die dort notierte Empfehlung „frac 0.10 als Betriebspunkt" gilt nur ohne Nachkauf. Unter Max' Kaufplan ist der Betriebspunkt ein **Paar**, nicht ein Wert. Im Ticket ergänzt.
- **AP89 (VIX-Bein):** das Argument „gleiche Passquote, aber 6 Tage schneller → Tempo zählt bei Reset-Strategie" wird durch diesen Lauf **bestätigt und quantifizierbar** — Tempo ist unter rollendem Nachkauf kein Beiwerk, sondern der Haupthebel.
- **AP90 (neu):** Eval-Zeitlimit/Mindesthandelstage bei E8 Signature Futures schriftlich klären. Ohne das steht das langsame Bein des Splits auf ungeprüftem Grund.

### Lehre
44. **Ein Betriebspunkt ist nur zusammen mit der Kaufpolitik definiert.** Dieselbe Frontier liefert gegensätzliche Empfehlungen, je nachdem ob man ein Konto einmalig kauft (→ niedriger frac, hohe Einzelquote) oder rollend nachkauft (→ hoher frac, kurze Entscheidungszeit). **Vor jeder Betriebspunkt-Frage zuerst festlegen: ein Versuch oder eine Kauf-Rate?** Ergänzt Lehre 26 („Passquote ist zweideutig") um die zeitliche Dimension.
45. **Eine Kauf-Obergrenze pro Monat ist keine Budget-Restriktion, sondern eine Rate.** Nicht ansammelbares Kontingent heißt: langsame Konten sparen keine Käufe ein, sie verzögern nur den Zeitpunkt, an dem sich das Kontingent auszahlt. Deshalb kippt die Optimierung Richtung Tempo, obwohl weniger Versuche zur Verfügung stehen.

## #090 — RV_leadlag_NQES nachgetestet: Tod bestätigt, Mechanismus vollständig erklärt, zwei Tracker-Leichen bereinigt (11.08.2026)
- **Anstoß (Max):** nach dem Bau des Live-Tabs (siehe [[Backtest-Engine]]) nochmal explizit durchtesten, ob `RV_leadlag_NQES` (die einzige Relative-Value-Karte im Vault) wirklich durchfällt oder nicht — der `live_finalize.py`-Lauf hatte sie ausgeschlossen, weil der alte Report vom 31.07. (Grade A) mit dem seit 10.08. gefixten `rv.py` neu gerechnet auf PF 0,91 kippte.
- **Root Cause exakt lokalisiert** (nicht nur bestätigt, sondern hergeleitet): `rv.py`, Modus `leadlag`. Die Position läuft im Laggard (Symbol 2 = ES, `base = r2 - r2[i0]`), aber `R_pts` (das Dollar-Risiko, mit dem sowohl PnL als auch Kosten pro Trade normiert werden) wurde vor dem Fix mit `c1[i0]` (NQ-Preis) statt `c2[i0]` (ES-Preis) berechnet — ein Copy-Paste-Rest aus den Spread-Modi, wo `c1` korrekt ist. Median-`R_pts` fällt durch den Fix von 22,74 auf 7,24 (Faktor ~3,1×). Der raw R-Multiple (`r`) jedes Trades bleibt dabei unverändert (direkt geprüft: alte und neue `trades()`-Ausgabe liefern bitidentische `r`-Werte) — der Fix wirkt ausschließlich über die Kosten-Normierung in `qbt.run_strategy`: `r_net = r - cost_pts / R_pts`. Mit dem kleineren, korrekten `R_pts` verdreifacht sich der Kosten-Drag pro Trade (3,1% → 9,7% von R) und kippt die Strategie von PF 1,37/expR +0,239 auf **PF 0,91/expR −0,074/Sharpe −0,37** (324 Trades, identisch in beiden Versionen).
- **Robustheits-Sweep statt Einzelpunkt:** alle 16 in `rv_results.json` dokumentierten `leadlag`-Configs (8× NQ-ES, 8× NQ-RTY, das komplette ursprüngliche Discovery-Grid) mit dem gefixten Code neu gerechnet. NQ-RTY ist ein Totalschaden (PF 0,36–0,57, Sharpe −1,5 bis −2,2 über alle 8 Configs). NQ-ES: 7 von 8 Nachbarn fallen auf PF ≤1,15 mit gemischtem Vorzeichen bei expR, nur **ein** Ausreißer (`t0.002/lr0.5/s0.75`: Win 42%, expR +0,087, PF 1,15, Sharpe 0,70) zeigt noch einen schwachen positiven Rest — bei 8 getesteten Nachbarn und keiner IS/OOS-Bestätigung hier klar Multiple-Testing-verdächtig, **kein neuer Validierungs-Kandidat ohne frischen, sauberen Test**.
- **Zwei Tracker-Leichen gefunden und bereinigt** ([[Ticket-Epics]]): Ticket `edge-ref-leadlag-korrektur` (FIREFIGHT) stand noch offen mit der Anweisung „`MaxLeadLagES` von 34,06 auf 9,12 $/Trade korrigieren" — das ist eine überholte Zwischenlösung (naive proportionale Skalierung um den R_pts-Faktor), die den nichtlinearen Effekt auf den Kosten-Drag ignoriert. Tatsächlich umgesetzt (siehe `gen_edge_ref.py`, Kommentar zu #075/AP71) wurde die richtige Lösung: Bein komplett aus `edge_ref.json` und `book_state.json` entfernt, nicht auf einen kleineren positiven Wert skaliert. Ticket `rv-instrument-scaling-verify` (CLEANROOM) stand seit dem Fix auf „gefixt, Verifikation offen" — mit diesem Eintrag verifiziert. Beide im Tracker als erledigt markiert.
- **ideas.json aktualisiert:** Karte „NQ-ES Lead-Lag (Relative Value)" von `Validiert` auf `Getötet` gesetzt, Ergebnistext korrigiert (der alte Text zitierte „+0,087" als Korrektur-Zahl für die falsche Config — das war der o.g. Nachbar, nicht die tatsächlich validierte/live gelaufene `t0.002/lr0.3/s0.5`).
- **Für den Live-Tab:** Ausschluss von `RV_leadlag_NQES` in `live_finalize.py` war korrekt. Relative Value bleibt damit die einzige der 5 Strategie-Familien ganz ohne aktuell bestätigten Kandidaten, weder fürs Prop-Buch noch fürs Live-Buch.

### Lehre
46. **Bei Multi-Instrument-Strategien muss jede Größe (Risiko, PnL-Referenz, Kosten-Normierung) am Instrument hängen, das tatsächlich die Position trägt — nicht am Instrument, das nur das Signal auslöst.** Leader und PnL-Träger sind bei Lead-Lag-Strategien per Konstruktion verschiedene Symbole; eine Formel, die stillschweigend das Signal-Symbol für die Risikoskalierung wiederverwendet, sieht in Backtests wie ein 3× überhöhter Edge aus, weil der Kosten-Drag im selben Verhältnis unterschätzt wird.
47. **Eine proportionale „Korrektur" eines gefundenen Skalierungsfehlers ist nicht automatisch die richtige Korrektur**, wenn die fehlerhafte Größe nichtlinear in die Formel eingeht (hier: als Nenner im Kosten-Term). Bei jedem Bug-Fund erst nachrechnen, dann schätzen — nicht umgekehrt.

## #091 — Leichenschau: alle offenen CLEANROOM-Verifikationen durchgetestet, eine Ticket-Leiche gefunden (11.08.2026)
- **Anstoß (Max, per /loop):** nach #090 (RV-Leadlag) alle ähnlichen „Leichen" durchgehen — also jede Strategie/jeden Report, dessen Zahlen ein späterer Engine-Fix (#075) überholt haben könnte, und jedes Ticket, das „gefixt" behauptet, ohne dass das je nachgerechnet wurde.
- **Sweep 1 — Corrupt-Data-Guard (`_drop_corrupt_sessions`, #075 Fund 2):** alle Reports mit `symbol` ES/RTY gesucht, deren `.meta.json` **vor** dem Fix (10.08. 08:52) generiert wurde → 11 Treffer (`ES_Momentum`, `RV_leadlag_NQRTY×1`, `CAL_fomcpost_ES`, `OPEXMOM_ES`, `OPEXMOM_RTY`, `RTY_Gap-fade`, `RV_leadlag_NQES` [schon #090], `EVENT_ES_primary`, `VWAPPULL_RTY`, `MOMSEL_ES`, `VOLBRK_ES`). Alle zehn (außer dem schon behandelten RV_leadlag_NQES) mit dem aktuellen Code frisch nachgerechnet und gegen die gespeicherten Werte verglichen.
  - **8 von 10 exakt unverändert** (win/PF/expR/n bis auf Rundung identisch) — die korrupten Bars lagen nicht in ihren Handelstagen.
  - **2 minimal verändert, beide leicht BESSER, nicht schlechter:** `RTY_Gap-fade` (im aktuellen Buch!) PF 1,185→1,214, expR +0,051→+0,058, 223→220 Trades (3 korrupte Tage raus). `VWAPPULL_RTY` PF 1,119→1,139, expR +0,033→+0,037, 341→331 Trades (10 raus). Beide Male: die entfernten Tage waren netto negativ, ihr Rauswurf hilft leicht.
  - **Verdict: keine neue Leiche, keine neue Edge.** Der Corrupt-Data-Fix war für die einzige stark betroffene Strategie (RV_leadlag) schon in #090 abgehandelt; der Rest des Buchs war nie relevant exponiert. `RTY_Gap-fade`s Report ist technisch stale (Zahlen leicht zu konservativ), aber nicht materiell — Neu-Generierung optional, kein Handlungsdruck.
- **Sweep 2 — Ticket-Status gegen Code geprüft:** `Ticket-Epics.md` (CLEANROOM) führte `slippage-ordertyp` als **„✅ gefixt"**. Direkt im Code nachgesehen: `qbt.py::run_strategy` berechnet `cost_pts` immer noch pauschal mit `2 * slippage_ticks * TICK` — es gibt **kein** `entry_slip_ticks`/`exit_slip_ticks` im ganzen Modul. Der in #075/#076 vorgeschlagene „saubere Fix" wurde nie gebaut. Was tatsächlich existiert: eine **einmalige externe Nachrechnung** in `goal_last_push.py` (aus der `exit`-Spalte manuell rekonstruiert), deren Ergebnis nur in die damalige #076-Buchentscheidung eingeflossen ist. **Jeder normale `run_strategy()`-Aufruf — inkl. jeder Report im Lab und `live_finalize.py` von gestern — rechnet nach wie vor mit der pauschalen, konservativeren Annahme.** Das ist keine falsche Zahl, aber eine falsche Ticket-Behauptung, die bei der nächsten Buch-Entscheidung Verwirrung gestiftet hätte.
- **Konsequenz:** `Ticket-Epics.md` korrigiert — `slippage-ordertyp` von „gefixt" auf „Status war falsch" umgestellt, neues echtes Ticket `slippage-ordertyp-integration` (CLEANROOM) angelegt für den tatsächlichen Einbau. `mae-doppelzaehlung-verify` und `corrupt-data-guard-verify` als verifiziert markiert (waren beide schon erledigt, nur nicht abgehakt).
- **Nicht mehr geprüft, weil nicht durch #075 betroffen:** die Asia-Entry-Minute (#075 Fund 3) war ein reiner Live-NinjaScript-Bug, kein Backtest-Fehler — `asian.py` hatte schon immer 09:30, keine Reports zu re-testen.

### Lehre
48. **„Leiche" ist nicht nur eine Strategie mit toter Edge — auch ein Ticket, das „gefixt" behauptet, ohne dass der Code das tut, ist eine Leiche.** Der Blast-Radius-Fehlschluss aus #082 (Lehre 35: Ticket-Text ist Hypothese, keine geprüfte Tatsache) gilt in beide Richtungen: sowohl „mehr kaputt als gedacht" als auch „mehr gefixt als tatsächlich passiert ist".
49. **Ein systematischer Sweep (alle Reports vor einem Fix-Zeitpunkt) findet mehr als gezieltes Nachfragen** — hier wurden 10 zusätzliche potenziell betroffene Strategien gefunden, die niemand einzeln angefragt hätte, weil sie nie im Verdacht standen.

## #092 — Cushion-Size an alle Beine übertragen, pro Konto getrennt (AP92, 11.08.2026)
- **Anstoß (Max):** Ticket AP92 aus dem Lab-Tracker — RiskGuard rechnet seit Wochen jeden Session-Start die erlaubte Kontraktzahl aus (`cushion * CushionFrac / RiskPerMicro`, geclampt 1..MaxContracts) und schreibt sie nach `maxlab_size.txt`. Aber **kein Bein hat die Datei je gelesen** — alle 9 liefen mit `DefaultQuantity = 1` fix. Folge: der Sizing-Split zwischen den zwei geplanten E8-Konten (#089, AP91: bestehendes 50k-Konto + als nächstes zu kaufendes 25k-Konto, je eigener CushionFrac) wäre live wirkungslos gewesen — zwei identisch große Konten, Korrelation 1.0, der ganze Split-Vorteil (+10pp P(funded), #089 Befund 2) verschenkt.
- **Umsetzung** (`engine/ninjascript/`, alle 9 Bein-Dateien + `MaxRiskGuard.cs`):
  - RiskGuard schreibt die Size jetzt **pro Konto getrennt** (`maxlab_size_<Kontoname>.txt` statt eine gemeinsame Datei) — Voraussetzung dafür, dass zwei parallel laufende RiskGuard-Instanzen (eine je E8-Konto) sich nicht gegenseitig überschreiben. Kontoname wird für den Dateinamen sanitiert (ungültige Windows-Zeichen raus).
  - Jedes Bein liest bei `Bars.IsFirstBarOfSession` seine **eigene** kontospezifische Datei (`Account.Name` ist pro Strategie-Instanz bekannt) und nutzt das Ergebnis (`liveQty`) statt `DefaultQuantity` in allen Entry-Calls.
  - Fallback auf 1 Kontrakt, wenn die Datei fehlt, nicht parsebar ist, oder **veraltet** ist (`LastWriteTime.Date != Today` — RiskGuard hat sie heute noch nicht neu geschrieben). Nie ein Crash, im Zweifel die konservative Größe.
  - Sonderfall `MaxORBFadeNQ` (ruhende Limit-Orders): `liveQty` wird beim Session-Start gecacht und beim späteren Platzieren der Limits verwendet — konsistent mit allen anderen Beinen, da RiskGuard ohnehin nur 1×/Tag schreibt.
- **Deploy:** NT8 war seit 07.08. flach (alle Strategien seit FIREFIGHT-Start am 10.08. abends deaktiviert), Konto-Check vor dem Stop bestätigt (Position-Snapshot leer, letzte Order 07.08.). Über `box_deploy.ps1` auf der Box deployed, Pre-Flight + `dotnet build` beide grün, 0 Errors. NT8 danach gestoppt gelassen — Wiederanlauf braucht laut AP86 eine RDP-Session, macht Max selbst.
- **Bewusst NICHT mitgemacht (Scope-Grenze):** `MaxRiskGuard.cs` schreibt neben der Size noch fünf weitere Dateien (State, Log, Orders, Position-Snapshot, Equity) — alle nach wie vor **ohne** Kontoname im Pfad. Sobald zwei RiskGuard-Instanzen gleichzeitig auf zwei E8-Konten laufen (AP91), würden sie sich diese fünf Dateien gegenseitig überschreiben (State-Kollision ist durch den bestehenden Konto-Check im Dateiinhalt zwar abgefangen — sieht man an den Log-Zeilen vom 05.08., wo `Simtestsim2` den `Sim101`-State korrekt verworfen hat — aber Log/Orders/Snapshot/Equity würden trotzdem Konto A und B vermischen). Eigenes Ticket dafür angelegt, nicht Teil von AP92.

### Lehre
50. **„Der Wächter rechnet die richtige Zahl aus" und „die Beine benutzen sie" sind zwei getrennte Behauptungen.** Cushion-Sizing stand seit Wochen als erledigt im Kopf, weil RiskGuard sie korrekt herleitet und protokolliert — dass die Konsumenten-Seite fehlte, fiel erst auf, als ein zweites Konto die Lücke real gekostet hätte. Bei jeder "Wächter schreibt X"-Architektur explizit gegenprüfen, ob auch etwas X liest.

## #093 — E8 klärt Eval-Zeitlimit: keine Zeit-/Tagesgrenze, nur Wochen-Inaktivitätsregel (AP90, 11.08.2026)
- **Anstoß (Max):** Ticket AP90 — der Betriebspunkt-Plan aus #089 (2x E8 25k, Split 0,10/0,30, rollend nachkaufen) braucht ein langsames Bein (median 45-85 Tage) und ein schnelles Bein (Pass in 6-8 Tagen möglich). War beides nirgends bestätigt: Zeitlimit hätte das langsame Bein wertlos gemacht, Mindest-Handelstage hätten das schnelle formal blockiert.
- **Antwort E8-Support (Laerte, Support-Chat, 11.08.):** keine maximale oder minimale Zeitbegrenzung für die Evaluation. Stattdessen eine Inaktivitätsregel: Futures-Konten brauchen mindestens 1 Trade (auf+zu) pro Woche, ab 0,1 Lot genügt, gilt auch für frisch gekaufte Konten ohne Historie. Forex/Krypto: alle 60 Tage.
- **Ergebnis:** alle drei offenen Fragen geklärt, der Split-Plan aus #089 ist ohne Einschränkung freigegeben. Einziger Nebenpunkt: die Wochen-Regel setzt voraus, dass jedes aktive Bein im Schnitt ≥1x/Woche einen Trade auslöst — vor dem Kauf (AP91) kurz gegen die tatsächliche Trade-Frequenz der Beine prüfen, Kandidat mit dem größten Risiko ist ein selektives Setup wie ORB-Fade+NR7-Filter.
- **Dokumentiert:** [[E8-Support-Anfrage (Eval-Zeitlimit + Mindest-Handelstage)]]. AP90 aus `tasks.json` gelöscht, AP91 (Kauf-Ticket) hängt jetzt nur noch an AP53 (Buch-Entscheidung).
- **Nachtrag (Max, 11.08.):** statt jedes Bein einzeln auf organische Wochen-Frequenz zu prüfen, lieber ein dediziertes Heartbeat-Bein bauen, das einmal pro Woche 1 Lot öffnet und sofort wieder schließt — deterministisch statt Vermutung, Kosten vernachlässigbar gegen das Tail-Risiko einer Kontoschließung. Als AP93 angelegt, vor Live-Einsatz noch kurz bei E8 bestätigen lassen, ob ein bewusst konstruierter Auf-Zu-Trade ohne Handelsabsicht für die Regel zählt.

## #094 — Käfigwechsel auf E8 50k: Betriebspunkt neu bestimmt, zwei Live-Fehlkonfigurationen gefunden (15.08.2026)
- **Anstoß (Max, 15.08.):** Max hat bereits einen **E8 50k gekauft** und tradet ihn. Die 2x25k aus #089 kommen später dazu. Ab sofort ist die Rechenbasis also 1x 50k (aktiv) + 2x 25k (geplant), nicht mehr 2x 25k.
- **Frontier neu gerechnet** (Buch unverändert, 5 Beine, intraday-Bust #077):

| frac | 25k (1500/1000) | **50k (3000/2000)** |
|---|---|---|
| 0,10 | 39 % / 31 d | **49 % / 88 d** |
| 0,12 | 39 % / 31 d | **45 % / 49 d** |
| 0,14 | 39 % / 31 d | **43 % / 41 d** |
| 0,18 | 37 % / 28 d | **39 % / 23 d** |
| 0,22 | 34 % / 15 d | **35 % / 15 d** |
| 0,30 | 30 % / 10 d | **28 % / 8 d** |

- **Kernbefund:** Der 50k ist der **bessere Käfig**, aber nur bei kleinem frac. Auf 25k faltet der Min-Size-Effekt (#029/#076) alles ≤0,14 auf „1 Kontrakt" zusammen — die Frontier ist dort links flach. Auf 50k differenziert sie wieder und öffnet oben 10 pp Passquote, die auf 25k schlicht nicht erreichbar waren.
- **Betriebspunkt gewählt: frac 0,12** (Max' Entscheidung) = 45 % / median 49 Tage. Der Knick der Kurve: gegenüber 0,10 kostet er 4 pp und halbiert die Zeit, gegenüber 0,14 bringt er 2 pp für 8 Tage. Reine Max-Passquote wäre 0,10, aber 88 Tage Median blockieren den einzigen laufenden Slot über ein Quartal, und Max kauft demnächst nach — also zählt Zeit mit (#089).
- **⚠️ Zwei Fehlkonfigurationen im Live-Setup gefunden** (`MaxRiskGuard.cs`, beide korrigiert, Deploy steht noch aus):
  1. `MaxTrailingDD = 2500` — das ist der **Apex**-Wert aus der Sim-Phase. E8 50k hat **2.000**. Der Wächter hätte erst gegriffen, wenn E8 das Konto längst gebustet hat. Der Guard war damit auf dem echten Konto wirkungslos.
  2. `CushionFrac = 0.22` — Sim-Wert aus AP18, kostet auf dem 50k-Käfig ~10 pp Passquote gegenüber 0,12.
  Zusätzlich läuft der Guard laut Box-Log noch auf `Simtestsim2` (Sim-100k), muss aufs E8-Konto.
- **Neu im Rechenkern:** `eval_plan.py` unterstützt jetzt **Käfig pro Konto** (`target`/`dd`/`price_usd` im Konto-Eintrag) plus `owned` (bereits gekauft → läuft ab Tag 0, wird nicht nachgekauft) und `buys_start_month`. Vorher waren target/dd global — jede gemischte Rechnung hätte die 25k-Konten im 50k-Käfig gerechnet und ihre Quoten zu gut ausgewiesen.
- **Neuer Plan-Stand** (`portfolio.json`, 5 Beine, intraday): Konto A (50k, 0,12) solo 43,7 % / 47 d · Konto B (25k, 0,10) 36,8 % / 28 d · Konto C (25k, 0,30) 29,8 % / 8 d. **P(funded) rollend: 1M 14,4 % · 3M 64,3 % · 6M 90,3 % · 12M 99,2 %**, Median 66 Tage, ~4,8 Evals ≈ $476 zusätzlich zu den bereits bezahlten $150.
- **Warum die 3M-Zahl schlechter aussieht als vorher (72,5 %):** ehrlicher, nicht schlechter. Vorher unterstellte der Plan zwei sofort laufende Konten ab Monat 0. Real läuft ein Konto, die anderen kommen ab Monat 1.

### Lehre
51. **Ein Käfigwechsel ist kein Parameter-Update, er verschiebt den ganzen Betriebspunkt.** Der Split 0,10/0,30 war auf den 25k-Min-Size-Effekt gefittet und auf 50k schlicht falsch. Bei jeder Änderung von Kontogröße/Firma/Target/DD gehört die Frontier neu gerechnet, bevor irgendein frac übernommen wird.
52. **Sim-Parameter überleben den Kontowechsel und niemand merkt es.** `MaxTrailingDD 2500` stammte aus einem Apex-Vergleich, `CushionFrac 0.22` aus der Sim-Eval. Beide standen still im Live-Code und wären beim ersten echten Handelstag scharf gewesen. Vor jedem Scharfschalten die Guard-Defaults gegen die **tatsächlichen** Firm-Zahlen gegenlesen, nicht gegen die Erinnerung.

## #095 — AP53 final: kein Buchumbau. Der ganze Vergleich war am falschen Betriebspunkt gerechnet (15.08.2026)

- **Anstoß (Max, 15.08.):** AP53 entscheiden und das Portfolio so umbauen, wie es am besten ist. AP53 lag seit dem 10.08. offen und stützte sich auf die Tabelle aus #078 — gerechnet mit anderen Fracs, vor dem Käfigwechsel (#094) und mit **zwei verschiedenen Cell-Funktionen** für die beiden Bücher (`book.cell_daily` fürs Zielbuch, `goal_last_push.cells_exact_cost` fürs 3-Bein-Buch). Alles neu gerechnet, alle Kandidaten durch dieselbe Funktion. Skripte: `engine/ap53_book_decision.py`, `engine/ap53_operating_point.py`.

### Der Methodenfehler, der die ganze Frage verdreht hat
Erster Lauf, alle Bücher bei **fixem** frac 0,12 (der Betriebspunkt aus #094), 50k-Käfig, intraday, 5 Seeds:

| Buch | Solo frac 0,12 | P(funded) 3M |
|---|---|---|
| Zielbuch #071 **mit** RV_leadlag | 47,8 % / 42d | **69,2 %** |
| 3-Bein #076 (gew. 3/8/4) | 47,1 % / 37d | 68,3 % |
| Live-Buch + NOISE_ORB_NQ | 42,9 % / 52d | 67,0 % |
| Zielbuch **ohne** RV | 47,2 % / 48d | 64,6 % |
| Live-Buch (Status quo) | 44,1 % / 50d | 64,3 % |

Zeile 1 gegen Zeile 4 ist der Knackpunkt: **dasselbe Buch wird um 4,6pp besser, wenn man ihm ein Bein mit bestätigt negativer Erwartung hinzufügt** (`RV_leadlag_NQES`, PF 0,91, in #090 für tot erklärt). Kein Edge-Effekt — das Bein fügt Handelstage hinzu, das Konto entscheidet dadurch schneller, und unter rollendem Nachkauf zahlt Tempo (#089). Genau denselben Effekt bekommt man gratis über den frac.

Damit ist jeder Buchvergleich bei fixem frac wertlos: er belohnt das Buch mit den meisten Handelstagen, nicht das mit der besten Edge. Zweiter Lauf deshalb mit **Optimierung des Konten-Tripels je Buch** (A = 50k owned, B/C = 25k geplant, 75 Kombinationen, Sieger mit 8 Seeds × 8.000 Sims nachgerechnet):

| Buch | bester Punkt A/B/C | 3M | 6M | Median | Ø Kosten |
|---|---|---|---|---|---|
| Live-Buch + NOISE_ORB_NQ | 0,22 / 0,10 / 0,30 | **71,2 % ±0,3** | 92,3 % | 52d | 401 $ |
| Zielbuch ohne RV | 0,22 / 0,18 / 0,30 | 69,4 % ±0,5 | 92,0 % | 52d | 403 $ |
| **Live-Buch (Status quo)** | 0,22 / 0,10 / 0,30 | 69,2 % ±0,4 | 91,6 % | 57d | 413 $ |
| 3-Bein #076 | 0,10 / 0,10 / 0,10 | 67,9 % ±0,3 | 90,3 % | 56d | 443 $ |

**Am eigenen Optimum gemessen ist das Zielbuch vom Live-Buch nicht zu unterscheiden (69,4 vs. 69,2, sd 0,4-0,5).** Der ganze Umbau — 5 neue NinjaScript-Ports, 5 funktionierende raus — kauft exakt nichts. Das 3-Bein-Buch liegt sogar 1,3pp darunter. Zusammen mit #088 (Train-only-Suche findet 3 der 4 Zielbeine gar nicht) und #090 (RV tot) ist AP53 damit beantwortet.

### Entscheidung 1: kein Umbau. Der Gewinn lag die ganze Zeit im Betriebspunkt, nicht im Buch
Auf dem **unveränderten** Live-Buch: frac Konto A von 0,12 auf **0,22** → P(funded) 3M **64,8 % → 69,2 %** (+4,4pp), 6M 90,5 → 91,6 %, Median 66 → 57 Tage, Erwartungskosten 476 → 413 $. Besser, schneller **und** billiger, ohne eine Zeile NinjaScript.

Warum 0,12 falsch war: der Wert wurde am 15.08. (#094) an der **Solo**-Frontier gewählt (45 % Passquote / 49 Tage) — also für ein einzelnes Konto ohne Nachkauf. Der beschlossene Plan kauft aber rollend nach. Das ist Lehre 44 aus #089, angewandt auf den eigenen Käfig und dabei einen Tag zuvor selbst übersehen.

0,22 ist ein **inneres** Optimum, keine Randlösung: 0,18 → 68,5 % · **0,22 → 69,2 %** · 0,26 → 68,9 % · 0,30 → 68,6 % · 0,42 → 66,7 %. In Kontrakten heißt das: Startgröße 4 statt 2 (risk/Kontrakt 104 $, Cushion 2.000 $).

**Bedingung, die mitgeschrieben gehört:** die 0,22 gelten nur, solange nachgekauft wird. Ohne Nachkauf ist der richtige Wert wieder 0,10 (Solo 47,7 % / 89d gegen 33,5 % / 14d). Betriebspunkt und Kaufpolitik sind ein Paar.

### Entscheidung 2: NOISE_ORB_NQ als 6. Bein — ja, aber erst nach dem Port
+2,0pp (69,2 → 71,2 %, sd 0,3/0,4, also ~4 Sigma) und median 5 Tage schneller. Es ist das **einzige** Bein im ganzen Vergleich mit einer echten Train→Test-Bestätigung (#088), und `noise_orb.py` ist sauber gebaut (Signal am Bar-Close, Fill am nächsten Bar-Open, kein Look-ahead — die ORB-Falle aus #066/#067 greift hier nicht). Ticket **AP58** hochgezogen.

Bewusst **nicht** in `book_state.json` eingetragen, solange das Bein nicht live handelbar ist: sonst zeigt der Portfolio-Tab 71,2 %, während real 69,2 % laufen. Genau die Drift, die einen Tag vorher zwei scharfe Fehlkonfigurationen im Guard produziert hat (Lehre 52).

### Nebenbefund: Leave-one-out über das Live-Buch
Jedes Bein einzeln entfernt, P(funded) 3M gegen die 64,3 %-Basis (frac 0,12):

| entfernt | 3M | Δ |
|---|---|---|
| NQ_LastHour | 61,5 % | **−2,8** |
| NQ_Asia-Dir-USopen | 62,5 % | −1,8 |
| NQ_ORB-fade | 63,3 % | −1,0 |
| RTY_Gap-fade | 63,3 % | −1,0 |
| NQ_Momentum | 64,8 % | +0,5 (Rauschen) |

Vier von fünf Beinen tragen. `NQ_Momentum` ist neutral — damit ist auch AP54 („Bein 4 streichen?") und die Restfrage aus #080 (MOMSEL-Replace) erledigt: es gibt nichts zu gewinnen, aber auch keinen Grund zu streichen, also bleibt es drin (Simplex-Regel gilt für neue Komplexität, nicht für das Abreißen funktionierender Teile).

### Umgesetzt
- `book_state.json` → `plan.accounts[A].frac` 0,12 → 0,22, Beine unverändert, Begründung + Bedingung im Feld
- `funded_finalize.py` durchgelaufen → `portfolio.json` + Report neu
- `ninjascript/MaxRiskGuard.cs` → `CushionFrac` 0,12 → 0,22 (**im Source, Deploy offen → AP96**)
- Tickets: AP53/AP48/AP54 gelöscht (entschieden), AP58 auf gelb + Messwert, AP91 + AP80 nachgezogen, **AP96** (Deploy) und **AP97** (Konto C aggressiver?) neu

### Nachtrag 15.08. abends: Port gebaut, verifiziert, deployed
`ninjascript/MaxNoiseORBNQ.cs` als exakter Port von `noise_orb.py`, auf der Box seit 17:58 (Pre-Flight über alle 11 Dateien sauber, Build ok, Staging geleert). Vorher Trade-für-Trade verifiziert mit `engine/verify_noiseorb_port.py`: **1937 von 1937 Trades identisch** (Datum, Richtung, Einstiegsminute), max |ΔR| = 0,0, expR +0,1293 beidseitig.

Die Prüfung hat sich sofort bezahlt gemacht: der erste Lauf zeigte **1938 statt 1937** Trades. Ursache war kein Logikfehler, sondern `if n < 60: continue` in `noise_orb.py` — ein Datenhygiene-Filter gegen kaputte Sessions (im Datensatz genau eine: 2020-06-30 mit 41 Bars). Live ist der nicht nachbaubar: um 10:00 weiß niemand, dass die Session um 10:11 abreißt. Im Header der `.cs` dokumentiert.

Das Bein läuft zunächst **nur auf Simtestsim2** und kommt erst nach der Sim-Validierung in `book_state.json` (AP58) — sonst zeigt der Portfolio-Tab 71,2 %, während real 69,2 % laufen.

### Lehre
53. **Ein Buchvergleich bei fixem Sizing misst nicht das Buch, sondern die Anzahl der Handelstage.** Wer unter rollendem Nachkauf zwei Bücher bei demselben frac vergleicht, bevorzugt systematisch das Buch, das schneller entscheidet — auch wenn es das über eine Verlustbringer-Strategie tut. Jedes Buch muss an seinem **eigenen** optimierten Betriebspunkt gemessen werden, sonst vergleicht man ein getuntes mit einem ungetunten Buch.
54. **Wenn ein Zusatz die Kennzahl verbessert, immer fragen: über Edge oder über Varianz?** Das tote RV-Bein, ein aggressiverer frac und ein zusätzliches Bein können dieselbe Zahl heben. Varianz ist die billigste dieser Zutaten und fast immer die falsche — sie kostet live echtes Geld, während der frac gratis ist. Test: Lässt sich derselbe Effekt durch reines Sizing erzeugen? Dann ist es kein Edge-Befund.
55. **Ein am Solo-Konto gewählter Betriebspunkt gehört bei jeder Planänderung neu geprüft, nicht nur bei Käfigwechseln.** Die 0,12 von gestern waren nicht falsch gerechnet, sondern für die falsche Frage gerechnet — und standen trotzdem einen Tag später als „der Betriebspunkt" im Guard.

## #096 — Strategy Developer: NQ VWAP Trend-Pullback, Parameter-Sweep über VWAP-Fenster/SL-TP (15.08.2026)

Max' erste eigene Idee im neuen Developer-Tab: 5m-Chart, Richtung über 15min-VWAP (Preis-Seite + Slope + 1h-Momentum ≥0,1%), Trigger = erste Gegenfarben-Kerze Richtung VWAP, SL 80/TP 40-50 Punkte, Tages-Limits (max 4 Trades, max 2 Verluste), Fenster 10:30-15:30 ET, flat 15:55 ET.

**v1 (Original-Parameter): F (38), expR +0,009R, PF 1,035.** OOS (letzte 30%) hält (expR +0,0086, kein Overfitting), aber die Kante ist zu schwach: 59% Winrate wird vom ungünstigen R:R (SL 80 vs. TP 40/50) fast komplett aufgefressen. Solo nicht käfigtauglich (31% Pass in 86 Tagen, Ziel ≥60%/≤50d). **Buch-Beitrag: schlechter** (-7,3pp P(funded) 3M, klar über dem Rauschen).

**Sweep (`engine/developer/sweep_vwap_v1.py`, 77 Kombis in 22s):** VWAP-Fenster 1h/2h/3h/4h × Richtungsregel-Varianten (bei 2h zusätzlich: ohne Slope-Filter / ohne Momentum-Filter / nur Preis-vs-VWAP, je mit 3 Momentum-Schwellen) × SL/TP-Grid (7 Varianten von symmetrisch 40/40 bis asymmetrisch 80/40).

- **3h/4h strukturell unbrauchbar, nicht "schlecht getestet":** mit Slope-Lookback = 1x Fenstergröße braucht 3h-VWAP 6h Vorlauf, 4h braucht 8h — bei einer RTH-Session von nur ~6,5h bleibt praktisch kein/kein Handelsfenster übrig (0 Trades über die gesamte Historie bei beiden). Kein Strategie-Problem, sondern eine Grenze dieser Fenster-Definition auf RTH-Daten.
- **Größter Hebel war nicht die Richtungsregel, sondern das R:R.** Symmetrisches SL/TP 40/40 schlug in fast jeder Fenster-Kombination das ungünstige Original 80/40-50 deutlich — die Winrate ändert sich kaum (51-52% statt 59%), aber PF steigt, weil der durchschnittliche Verlust nicht mehr 2x so groß ist wie der Gewinn.
- Lockern der Richtungsregel (ohne Slope-Filter, ohne Momentum-Filter, nur Preis-vs-VWAP) hat in JEDER getesteten Variante die OOS-Performance verschlechtert oder ins Negative gedreht — die volle 3-Bedingungen-Regel aus Max' Originalansage war schon die robusteste Variante, nicht die zu lockernde.

**Zwei Kandidaten mit vollem Report + Buch-Vergleich durchgerechnet** (`developer_run.py`, jetzt v2/v3 im Developer):

| | v2 (2h-VWAP, SL/TP 40/40) | v3 (1h-VWAP, SL/TP 40/40) |
|---|---|---|
| Grade | D (46) | F (38) |
| Trades / Woche | 4,3 | 10,5 |
| expR (IS / OOS) | +0,024 / +0,015 R | +0,014 / +0,012 R |
| PF (IS / OOS) | 1,06 / 1,03 | 1,03 / 1,03 |
| Max DD (1 Micro) | −2.069 $ | −3.051 $ |
| Solo Käfig-tauglich | Nein (33% / 86d) | Nein (32%) |
| **Buch-Beitrag** | **neutral** (score −0,5, Rauschen 0,5) | **schlechter** (score −7,5) |

**v2 gewinnt klar** — deutlich kleinerer Drawdown, besserer Sharpe (0,54 vs. 0,36), und als einzige der drei Versionen kein klar negativer Buch-Beitrag mehr (v1 und v3 beide "schlechter", v2 "neutral"). Trotzdem: **keine der drei Versionen verbessert das Buch**, und solo ist keine käfigtauglich. Der Sweep hat die Idee von "schadet dem Buch" auf "neutral" gehoben, nicht auf "gehört rein".

### Umgesetzt
- `developer/state.json`: v2 (2h/40-40) und v3 (1h/40-40) als Versionen angelegt, aktive Version auf v2 gesetzt
- `developer/sweep_vwap_v1.py` neu: wiederverwendbarer Sweep-Runner (5m-Bars einmal pro Tag vorberechnet, danach ~1s pro Parameter-Kombo)
- `report.py`: Subtitle-Branch für `mode="vwap_pullback"` ergänzt (fehlte, Report-Build crashte sonst mit KeyError auf z_entry/stop_mult — die generischen Report-Felder sind auf Mean-Reversion-Strategien zugeschnitten)

### Nachtrag: Ranking-Kriterium korrigiert (Max' Nachfrage: "geht es nicht eigentlich nur ums Passen?")
Der Sweep oben hat 77 Kombis nach OOS-expR sortiert und v2 daraus als besten Fund gewaehlt — expR ist aber nur ein Proxy. Das tatsaechliche Kriterium ist die Passquote, die vom kompletten Tagesverteilungsprofil abhaengt (Drawdown-Clustering), nicht nur vom Mittelwert. `developer/sweep_vwap_pass2.py` hat deshalb fuer alle 63 Kombis mit ≥300 Trades die echte Solo-Intraday-Frontier nachgerechnet (Tages-Zellen -> `passmc_vec` ueber alle Kaefig-Fracs, 4000 Sims je Frac).

Ergebnis: **0 von 63 Kombis sind käfigtauglich** (bestes Feld 34% vs. Ziel ≥60% in ≤50 Tagen — grosse Luecke, keine knappe Verfehlung). Die beiden Kombis mit der hoechsten simulierten Passquote (34%, `1h orig_asym` und `1h sym80`) haben dabei **keine belastbare OOS-Kante mehr** (expR +0,007 bzw. −0,0004) — die minimal bessere Passquote dort ist vermutlich MC-Sampling-Rauschen, keine echte Verbesserung. v2 liegt bei 33% Passquote (Rang 3/63, mit dem Spitzenfeld statistisch nicht unterscheidbar) UND hat als einzige Top-Kombi eine durchgehend positive, robuste IS+OOS-Kante. Die urspruengliche Wahl (v2) war damit im Ergebnis richtig, aber aus dem falschen Grund begruendet — am Gesamturteil (keine der Varianten ist tradebar) aendert die Korrektur nichts.

### Lehre
56. **Bei einer schwachen ersten Version zuerst das R:R prüfen, bevor an der Signal-Logik gedreht wird.** Eine hohe Winrate mit schlechtem PF ist fast immer ein R:R-Problem, kein Filter-Problem — ein Parameter-Sweep über SL/TP allein hob v1s expR von +0,009R auf bis zu +0,024R, ganz ohne die Richtung/Trigger-Logik anzufassen.
57. **Ein Rolling-Window-Indikator (VWAP, Slope, o.ä.) braucht 2x seine eigene Fenstergröße an Historie, wenn "Änderung über die Fenstergröße" geprüft wird.** Bei kurzen Sessions (RTH ~6,5h) macht das große Fenster (3h+) strukturell unbrauchbar, unabhängig von der Signalqualität — vor einem Sweep über Fenstergrößen die verfügbare Session-Länge gegen 2x-Fenster gegenrechnen, sonst verschwendet man Rechenzeit auf Kombis, die nie eine Chance hatten.
58. **Ein Parameter-Sweep muss direkt nach dem Entscheidungskriterium ranken (Passquote), nicht nach einem Proxy (expR/Sharpe).** Beide korrelieren meistens, aber nicht immer — hier hatte die Kombi mit der besten simulierten Passquote gar keine echte OOS-Kante mehr (wahrscheinlich MC-Rauschen). expR eignet sich zum Vorfiltern (billig zu rechnen), die finale Auswahl/Bewertung muss aber immer über die tatsächliche Solo-Frontier bzw. den Buch-Beitrag laufen.

### Nachtrag: Quelle identifiziert, Transkript wortgenau abgeglichen (Max: "hast du wirklich getestet was er sagt?")
Max' Idee stammt aus YouTube "Market Maker Reveals His 'Golden Ticket' VWAP Strategy" (Matteo Conti, SQR Capital, Kanal IQCapital, `youtube.com/watch?v=wm4A6qo0g3I`). Untertitel-Track per Browser ausgelesen (JSON3-Transkript ueber die YouTube-timedtext-API, nicht nur Beschreibung) und Wort fuer Wort gegen v1 geprueft.

**Zwei echte Abweichungen gefunden, in v4 korrigiert:**
1. VWAP-Definition: v1 hatte einen ROLLIERENDEN 3-Bar-VWAP gebaut (reines 15min-Fenster, kein Anker). Die Quelle sagt explizit "anchored at the market open, so 9:30 Eastern Time" — es ist der Standard-Session-VWAP (kumulativ ab 9:30 ET), nur auf 15-Minuten-Basis berechnet und auf dem 5m-Chart angezeigt.
2. Entry-Fill: v1 fuellt am Close der Trigger-Kerze. Die Quelle: "it's going to be at the opening of the next candle" — Fill am Open der naechsten 5m-Kerze.

Alles andere (SL 80/TP 40-50, Guardrails max 4 Trades/max 2 Verluste/Tag, Fenster 10:30-15:30 ET, flat 15:55 ET, 1h-Move-Filter 0,1%) deckte sich exakt mit dem, was Max beschrieben hatte — keine weiteren Abweichungen.

**v4 (korrigiert) vs. v1:**

| | v1 | v4 (Original-Quelle) |
|---|---|---|
| Win-Rate | 59,1% | **60,1%** (Quelle behauptet 64-65%) |
| expR | +0,009R | **+0,015R** |
| PF | 1,035 | **1,054** |
| Sharpe | 0,32 | **0,55** |
| Solo-Passquote (best) | 31% (86d) | **37%** (108d) |
| Buch-Beitrag | schlechter (-7,3) | schlechter (-5,2, aber weniger schlecht) |

Die Korrektur bringt ein durchgehend besseres, aber immer noch nicht ausreichendes Ergebnis — Passquote 37% bleibt weit unter dem Käfig-Ziel von 60%, und die im Video behauptete 49,8%-Einzel-Eval-Passquote (bzw. 93,6% bei 4 Versuchen) wird nicht annaehernd erreicht. Die Quelle nennt weder Prop-Firma noch Konto-DD/Target noch ob EOD- oder Intraday-Bust-Check verwendet wurde — ohne diese Angaben ist ihre Zahl nicht nachrechenbar, nur die Handelsregeln selbst waren reproduzierbar.

**Zweites Video geprueft** (`youtube.com/watch?v=XWJlBBikUc0`, Robert Rother, Ex-Hedgefonds-Manager) — **keine Variante derselben Strategie**, sondern ein komplett anderer, diskretionärer Ansatz: 3 verschiedene VWAP-Anker (Day/London/US-Session) plus Bookmap-Orderbuch-Lesen (Liquiditäts-Cluster, Spoofing-Erkennung), Entscheidung "welcher VWAP wird gerade respektiert" laut Aussage im Interview explizit ohne festen Regelwert ("I do not have a specific number for that... you simply were watching it"). Nicht backtestbar mit unseren Daten: braucht Orderbuch-/DOM-Tiefe (Bookmap), die in den historischen 1m-OHLCV-Parquets nicht existiert. SL 10 Ticks/TP 10-15 Ticks auf ES sind zwar genannt, aber der Entry-Trigger selbst ist diskretionär, keine kodierbare Regel.

### Lehre
59. **Bei einer YouTube-/Kurs-Quelle immer das Transkript wortgenau ziehen, nicht nur mitschreiben was im Gespräch hängen bleibt.** Zwei stille Annahmen (VWAP-Definition, Entry-Timing) waren beim ersten Bau falsch geraten — beide handfest korrigierbar, sobald das Transkript vorlag. `youtube.com/api/timedtext` liefert das automatische Untertitel-JSON auch ohne sichtbaren Transkript-Button, wenn man den ueber die Player-Response referenzierten Track direkt abruft.
60. **Eine im Marketing-Video behauptete Passquote ohne genannte Käfig-Parameter (Firma/DD/Target/Bust-Modus) ist nicht nachrechenbar und nicht vertrauenswürdig, auch wenn die Handelsregeln exakt stimmen.** v4 mit wortgenau nachgebauten Regeln bleibt bei 37% Solo-Passquote, weit unter den behaupteten 49,8% — die Lücke liegt vermutlich in unbekannten (evtl. günstigeren) Simulationsannahmen der Quelle, nicht in unserer Umsetzung.

## #097 — VWAP-Pullback systematisch ausgereizt: ein echter Fund, vier Falsifikationen (15.08.2026)

Max' Auftrag: über den VWAP-Pullback informieren, daraus eine Bereicherung fürs Prop-Firm-Passing entwickeln, mit Agents in Papern recherchieren, jeweils genau prüfen ob eine Edge da ist, nicht aufhören bis etwas gefunden ist.

**Ausgangslage:** #069 hatte das Coni-Video schon verworfen (P(pass) 33 %), #096 die Regeln wortgenau nachgebaut (v4: 37 % Solo, Buch −5,2pp). Der Satz aus #069 — *„der Mechanismus ist real, nur zu schwach pro Trade"* — war der Ansatzpunkt: nicht die Regeln ändern, sondern die schwachen Trades identifizieren.

### ⭐ Der Fund: Distanz zum VWAP trennt — genau gegen die Aussage der Quelle
Das Video sagt ausdrücklich *„it doesn't matter how close it is to the VWAP"*. Eine Feature-Diagnostik über alle 5.967 v4-Trades (`developer/vwap_diag.py`, protokolliert pro Trade Distanz/Berührungszahl/Tageszeit/Vol-Regime/Slope-Stärke/Wochentag) zeigt das Gegenteil: **der Abstand des Trigger-Closes zum VWAP, in ATR gemessen, ist die einzige Dimension die in IS UND OOS gleichgerichtet trennt.**

| Filter | n | IS expR | OOS expR | Solo-Passquote |
|---|---|---|---|---|
| ohne (v4) | 5967 | +0,0195 | +0,0072 | 37 % |
| Distanz ≥ 2,5 ATR | 3596 | +0,0384 | +0,0085 | **46 %** |

Robustheitskontrollen alle bestanden: monoton steigend bis 2,5 ATR, **Gegenprobe** (nur Trades NAHE am VWAP) durchgehend negativ/flat, Split-Half innerhalb IS beidseitig positiv, und **in allen 11 Jahren positiv** — auch 2026, wo die ungefilterte Version −0,0365 macht und die gefilterte +0,0143.

**Kausales Why (kein Fit ohne Why):** Der research-scout bestätigt aus Cache + Literatur — reine VWAP-Mean-Reversion ist in den eigenen Tests tot (#002-#005), der belegte Effekt ist **Intraday-Continuation** (Gao/Han/Li/Zhou, JFE 2018, peer-reviewed, deckt sich mit Insight #211). Genau den selektiert der Filter: weit weg vom VWAP = Trend intakt = Continuation greift; nah dran = kein Stretch, nichts zu holen. Die Strategie ist damit korrekt als Continuation-Setup mit Pullback-Timing einzuordnen, nicht als Reversion.

**Wirkung auf das eigentliche Kriterium:** der Filter hebt den Buch-Beitrag von **−4,86pp (schädlich) auf +0,02pp (neutral)** — 5 Seeds, Rauschschwelle 1,50pp. Beste Variante überhaupt +0,37pp (dist≥2,5 mit 40/40), ebenfalls klar innerhalb des Rauschens. **Keine einzige Variante erreicht „besser".**

### Vier Falsifikationen (alle sauber nachgewiesen)

**1. Post-hoc-Filtern ist ein Look-ahead — kostete mich hier 7pp Schönfärberei.** Erster Filter-Test wandte die Distanzregel NACHTRÄGLICH auf fertige Trades an → 53 % Passquote. Im Durchlauf angewandt (live-korrekt) → 46 %. Ursache: die Tages-Caps (max 4 Trades / 2 Verluste) wurden von den ungefilterten Signalen verbraucht; gefilterte Signale verbrauchen sie live nicht, es rutschen andere Trades nach. Nachgewiesen mit identischer Sim-Zahl in `developer/vwap_posthoc_check.py`.

**2. ATR-normierte Stops sind schlechter als feste Punkte.** Hypothese war: SL 80 Pkt = 3,1× ATR im Median, aber 9× ATR in ruhigen und 1,5× in volatilen Phasen — das müsse man normieren. Falsch: ATR-normiert halbiert die NQ-Kante (OOS +0,0046 statt +0,0085). Der feste Stop ist ein Feature: in ruhigen Phasen laufen Gewinner ins Target statt ausgestoppt zu werden, und die Zeit-Exits sind kleine Verluste statt voller Stops.

**3. Die Kante ist NQ-spezifisch — 3 von 4 Index-Futures sind negativ.** Gleiche Regeln, ATR-normiert (also fair skaliert): NQ IS +0,0188 / OOS +0,0046, aber ES −0,0247/−0,0265, RTY −0,0545/−0,0335, YM −0,0361/−0,0344. Multi-Symbol als Frequenz-Hebel ist damit tot (kombiniert 29 % statt 46 %). Das ist ein hartes Querschnitts-Falsifikationsergebnis und schwächt das Vertrauen in den NQ-Fund erheblich — es bleibt offen, ob NQ wirklich anders ist (stärkstes Intraday-Momentum) oder ob der NQ-Befund selbst Rauschen ist.

**4. Der Trend-Tag-Effekt ist real, aber nicht prognostizierbar.** Der VWAP-Stretch eines Tages sagt das Buch-Tagesergebnis stark voraus (Korr. **+0,249 IS / +0,241 OOS**, oberstes Quartil +223 $/Tag OOS gegen −66 $ im untersten) — aber er steht erst am Tagesende fest. Aus Vortagsinformation gebildete Varianten tragen nichts: `stretch_prev` Korr. ~0,00; alle Trailing-Mittel (3/5/10/20 Tage) **kippen im OOS das Vorzeichen**; von allen geprüften am Open bekannten Regime-Massen (Stretch-MAs, Vol-MAs, Trendstärke, VIX-Level/-Änderung) übersteht nur `vol_ma20` die Konsistenzprüfung, und das mit Korr. +0,057 bei n=721 ≈ 1,5 Sigma, also nicht signifikant.

### Was sonst noch getestet und verworfen wurde
- **168 Kombis** (Distanz × SL/TP × Tages-Caps × Momentum-Schwelle), nach Passquote gerankt: Maximum 46 %, kein Feld käfigtauglich. SL/TP-Varianten und das Lockern der Tages-Caps bewegen praktisch nichts.
- **Exit-Logik strukturell** (`vwap_exit_test.py`): Zeit-Exits bluten (−0,117 R über 27 % der Trades), aber keine Gegenmassnahme hilft. Breakeven-Stops und ATR-Trailing drehen die OOS-Kante ins **Negative** (−0,018 bis −0,027) — sie verwandeln Gewinner in Nullnummern und behalten die Verlierer. Früherer Zwangsausstieg (15:20 statt 15:55) hebt zwar die OOS-expR auf +0,0207, die Passquote bleibt bei 45 %.
- **Berührungszähler** („erste VWAP-Berührung ist das A+-Setup", Behauptung aus dem zweiten Video): IS +0,036 für die erste Berührung, OOS **−0,039** — kippt, also Folklore. Deckt sich mit dem Rechercheergebnis, dass es dafür keine einzige Primärquelle gibt.

### Fazit
**Gefunden: ja — ein echter, robuster, mechanistisch begründeter Edge-Verstärker.** Der Distanz-Filter ist der erste Eingriff, der die Familie von „schadet dem Buch" auf „neutral" hebt, und er ist über Jahre, Split-Half und Gegenprobe stabil. **Nicht gefunden: eine Bereicherung fürs Passing.** Bei Target 3.000 $ / DD 2.000 $ liefert schon ein driftfreier Zufallspfad ~40 % (2000/5000); 46 % liegen 6pp darüber. Für 60 % bräuchte es einen Sharpe, den diese Familie nicht hat (0,55). Weiteres Parameter-Drehen wäre genau das Overfitting, vor dem Lehre 54 und „Simplex beats Komplex" warnen — deshalb hier Schluss statt noch eine Runde.

### Nachtrag 16.08.: v5 gebaut — und dabei einen Bug in `developer_run.py` gefunden
Der Distanz-Filter liegt jetzt als **v5** im Developer (`versions/nq-vwap-pullback__v5.py`, aktiv). Beim Gegenrechnen fiel ein Widerspruch auf: `developer_run.py` meldete für v5 einen Buch-Beitrag von −4,20pp, mein separater Test für dieselbe Konfiguration +0,02pp. Gleiche Trades (n=3596 beidseitig, identische r_net und mae_r), gleiche Tagesgewinne — aber **unterschiedliche Intraday-Worst-Werte**.

**Ursache:** `get_trades()` machte `tr.sort_values("date")` mit dem Default `kind="quicksort"` — der ist **nicht stabil**. Bei vielen Zeilen mit demselben Datum verwürfelt er die Reihenfolge INNERHALB eines Tages: gemessen **225 von 887 Mehrtrade-Tagen** (25 %). `daily_cells()` rechnet den Intraday-Worst als kumulativen Pfad durch den Tag — bei falscher Reihenfolge ist er schlicht falsch. Beispiel 2016-01-20: echte Reihenfolge (−1,013 dann +0,487) ergibt worst −211 $, verwürfelt (+0,487 dann −1,013) nur −85 $.

**Reichweite geprüft:** betroffen war ausschließlich `developer_run.get_trades()` — also Intraday-Frontier (#077), Buch-Beitrag und Prop-Check **jeder** Developer-Version seit dem Tab-Start. **Nicht betroffen ist der Portfolio-Tab:** `book.cell_daily()` sortiert gar nicht, sondern nutzt die bereits chronologische Ausgabe von `qbt.run_strategy` — die P(funded)-Zahlen des Buchs waren immer korrekt. In `book.py`/`funded_finalize.py`/`live_finalize.py` steht derselbe Aufruf, dort aber nur für den Anzeige-Report und `qbt.metrics` (betrifft den angezeigten `max_dd_usd`, nicht die Passquoten) — vorsorglich mit korrigiert.

**Fix:** `sort_values("date", kind="stable")` an allen vier Stellen. Danach 0 von 887 Tagen verwürfelt, und die Zahlen decken sich mit der unabhängigen Rechnung. Alle fünf Versionen neu gerechnet:

| | Grade | n | expR | PF | Sharpe | Solo-Pass | Buch-Beitrag |
|---|---|---|---|---|---|---|---|
| v1 (Max' Erstfassung) | F (38) | 4814 | +0,0092 | 1,035 | +0,32 | 31 % | −7,10pp schlechter |
| v4 (Quelle wortgetreu) | D (51) | 5967 | +0,0148 | 1,054 | +0,55 | 37 % | −4,90pp schlechter |
| **v5 (+ Distanz-Filter)** | **C (58)** | 3596 | **+0,0275** | **1,116** | **+0,94** | **46 %** | **±0,00pp neutral** |

Der Bug hatte durchgehend zu pessimistisch gerechnet (v5 −4,20pp statt korrekt ±0,00pp). Am Gesamturteil ändert das nichts: v5 ist mit Grade C, Sharpe 0,94 und einem Drittel weniger Drawdown (−3.498 $ statt −5.553 $) die klar beste Version der Familie, bleibt aber solo nicht käfigtauglich (46 % gegen ≥60 %) und als Bein neutral statt verbessernd.

### Lehre
61. **Post-hoc-Filtern auf einem Trade-Set mit Tages-Limits ist Look-ahead.** Wer erst ungefiltert rechnet und danach Trades entfernt, misst eine Strategie, die so nie handelbar war: die Auswahl, welche Signale überhaupt Trades wurden, kannte den Filter noch nicht, und die Caps wurden von Trades verbraucht, die live nie stattgefunden hätten. Hier +7pp Schönfärberei. **Jeder Filter gehört in den Durchlauf, nicht in die Auswertung** — gilt für jede künftige Filter-Idee.
62. **Ein Filter, der auf einem Symbol trägt und auf drei verwandten nicht, ist ein Warnsignal, kein Alleinstellungsmerkmal.** Der Querschnitts-Test über ES/RTY/YM war der billigste und härteste Robustheitstest der ganzen Runde und hätte VOR dem ganzen Parameter-Sweep kommen sollen. Bei jeder künftigen Einzel-Symbol-Entdeckung zuerst: gilt das auch auf den Nachbar-Märkten?
63. **Ein starker Regime-Effekt ist wertlos, solange er nicht aus Information VOR dem Handelstag gebildet werden kann.** Der VWAP-Stretch erklärt das Buch-Tagesergebnis mit Korr. 0,24 in IS und OOS — und ist trotzdem nutzlos, weil er erst abends feststeht. Bei jedem Regime-/Sizing-Signal zuerst den Zeitstempel prüfen: wann genau weiß ich das? Erst danach die Korrelation ansehen.
64. **Breakeven- und Trailing-Stops sind kein neutraler „Risikoschutz".** Auf einer Continuation-Strategie mit niedrigem RR drehten beide die OOS-Kante ins Negative, weil sie systematisch die Gewinner abschneiden, die die Verlierer bezahlen müssen. Wer sie einbaut, ändert die Strategie fundamental und muss sie neu validieren.
65. **Bei jeder kumulativen Intraday-Rechnung muss die Sortierung stabil sein — `sort_values()` ist es per Default NICHT.** Sobald viele Zeilen denselben Schlüssel haben (hier: alle Trades eines Tages), zerwürfelt Quicksort ihre Reihenfolge. Alles, was danach einen Pfad durch den Tag rechnet (Intraday-DD, MAE-Ketten, Equity innerhalb des Tages), wird dadurch falsch — lautlos, ohne Fehlermeldung, und in eine nicht vorhersagbare Richtung. Regel: `kind="stable"` überall dort, wo nach der Sortierung kumuliert wird. Zweite Lehre daraus: **zwei unabhängige Rechenwege für dieselbe Zahl haben den Bug gefunden** — die Abweichung zwischen Eigenbau-Test und `developer_run` war das einzige Warnsignal.

## #098 — Ist die VWAP-Richtung überhaupt bestimmbar? Long ja, Short nein (16.08.2026)

Max' Frage nach v5: trägt die 3-Bedingungen-Richtungsregel (Preis vs. VWAP + Slope + 1h-Move) überhaupt echte Information, isoliert von Trigger/Caps/SL-TP? Bisher wurde immer nur die Gesamtstrategie getestet — ein guter Gesamttest kann an einer wertlosen Richtung liegen, wenn Entry-Timing oder R:R zufällig kompensieren.

**Isolierter Vorwärtstest** (`developer/vwap_direction_test.py`): pro 5m-Bar im 10:30-15:30-ET-Fenster (identisches Fenster wie die Strategie) Richtung nach den 3 Bedingungen bestimmt, dann geprüft ob Preis über 15/30/60/120 Minuten tatsächlich in diese Richtung läuft — ganz ohne Trigger-Kerze oder SL/TP.

**Befund: die Gesamt-Trefferquote lag nahe am Basiswert (49-52%) — aber das verdeckte eine scharfe Asymmetrie:**

| | Trefferquote (60min) | Drift |
|---|---|---|
| IS LONG | 53,6% | +0,119 ATR |
| IS SHORT | **46,7%** | +0,031 ATR |
| OOS LONG | 53,7% | +0,081 ATR |
| OOS SHORT | **47,6%** | +0,020 ATR |

Long trägt die gesamte Richtungs-Information (vermutlich schlicht NQ's Langfrist-Aufwärtstrend im Datensatz — `c_price`/`c_slope` haben beide einen Long-Bias von ~57%), Short liegt in IS **und** OOS unter Münzwurf. Keine der 3 Einzelbedingungen trägt für sich genommen viel (Trefferquoten alle 50-51%); erst die Kombination mit Long-Filterung zeigt eine Kante. Persistenz ist zudem schwach: Median-Länge einer Richtungsphase nur 3 Bars (15 min), 30% flackern sofort wieder weg — kein stabiles Mehrstunden-Regime, wie die "Trend"-Erzählung suggeriert.

**Bestätigt im echten v5-Backtest** (mit Trigger+Caps+SL/TP):

| | Win% | expR | PF |
|---|---|---|---|
| IS LONG | 60,6% | +0,044 | 1,255 |
| IS SHORT | 55,9% | +0,031 | 1,127 |
| OOS LONG | 62,1% | +0,015 | 1,058 |
| **OOS SHORT** | 59,3% | **±0,0000** | **1,000** |

Short liefert OOS eine expR von exakt null — keine graduelle Schwäche, totes Gewicht trotz plausibel aussehender 59% Winrate (PF genau 1,0 zeigt: die Winrate kompensiert nur exakt das R:R, keine echte Kante mehr übrig).

**v6 gebaut: v5 minus Short-Seite.** Ergebnis nuanciert, kein klarer Sieger:

| | n | tpw | Sharpe | OOS expR | MaxDD | Solo-Pass | Buch-Beitrag |
|---|---|---|---|---|---|---|---|
| v5 | 3596 | 6,6 | 0,94 | +0,0085 | −3.498$ | 46% | +0,00pp neutral |
| v6 | 2041 | 3,8 | **1,14** | **+0,0113** | **−1.880$** | 43% | +1,60pp — genau auf der Rauschschwelle (1,60), noch "neutral" |

v6 ist pro Trade klar sauberer (höherer Sharpe, PF, halbierter Drawdown) — bestätigt die Diagnose exakt. Aber die verlorene Frequenz (fast halbiert) kostet auf der Solo-Passquote mehr, als die Qualität dort bringt (43% < 46%), und der Buch-Beitrag liegt bei genau der 2×-Rauschen-Schwelle (score 1,6 = threshold 1,6) — technisch noch nicht "besser", aber ein Wimpernschlag davon entfernt. Klassische Qualität-vs-Frequenz-Spannung: keine der beiden Versionen ist eindeutig überlegen für das Buch-Kriterium.

### Umgesetzt
- `developer/vwap_direction_test.py` neu: 5-Schritte-Diagnostik (Basisraten, Vorwärtstrefferquote vs. Baseline, Einzelbedingungen, Persistenz, Distanz-Kreuzcheck) — wiederverwendbar für jede künftige Richtungs-/Filter-Regel
- v6 als Developer-Version angelegt und aktiv, v5 bleibt im Verlauf erhalten (Rollback jederzeit möglich)

### Bei der Gelegenheit: Bug in `developer_run.py` gefunden und gefixt
Beim Gegenrechnen von v5 fiel ein Widerspruch zwischen zwei unabhängigen Rechenwegen auf (−4,20pp vs. +0,02pp Buch-Beitrag bei identischen Trades). Ursache: `get_trades()` sortierte mit `sort_values("date")` — Default `kind="quicksort"` ist **nicht stabil** und verwürfelt bei vielen Zeilen mit gleichem Datum die Reihenfolge innerhalb eines Tages (225 von 887 Mehrtrade-Tagen betroffen). Da `daily_cells()` den Intraday-Worst als kumulativen Pfad durch den Tag rechnet, war er dadurch lautlos falsch — betraf Intraday-Frontier, Buch-Beitrag und Prop-Check jeder Developer-Version. **Der Portfolio-Tab war nicht betroffen** (`book.cell_daily` sortiert nicht, nutzt die bereits chronologische `qbt.run_strategy`-Ausgabe). Fix: `kind="stable"` in `developer_run.py`, `book.py`, `funded_finalize.py`, `live_finalize.py`. Alle Versionen neu gerechnet, Zahlen oben sind bereits die korrigierten. Siehe Lehre 65.

### Lehre
66. **Eine Gesamtstrategie kann eine schwache Gesamt-Kennzahl zeigen, obwohl eine Hälfte exzellent ist — Durchschnittsbildung versteckt Asymmetrien.** Die Richtungsregel sah in Summe wertlos aus (Trefferquote nahe Münzwurf); erst der Long/Short-Split zeigte, dass eine Hälfte eine echte, robuste Kante hat und die andere strukturell dagegen kämpft. Bei jeder Regel mit einer Long/Short- oder sonstigen Symmetrie-Annahme: immer beide Seiten getrennt prüfen, bevor man die Regel als Ganzes verwirft oder behält.
67. **Qualität schlägt Frequenz nicht automatisch, wenn die Zielgröße zeitabhängig ist.** v6 hatte den saubereren Trade (Sharpe, PF, Drawdown), aber die halbierte Frequenz kostete auf der Solo-Passquote mehr als die Qualität einbrachte — Zeit bis zum Ziel zählt genauso wie die Kante pro Trade. Ein Filter, der die Kante pro Trade verbessert, ist nicht automatisch ein besseres Bein.

## #099 — Richtungsregeln gegen Orderflow-Delta getauscht: erster Buch-Beitrag über der Rauschschwelle (16.08.2026)

Fortsetzung von #098. Max' Folgefrage: die 3 Richtungsbedingungen (Preis vs. VWAP, VWAP-Slope, 1h-Move) einzeln gegen ein Orderflow-Delta-Signal tauschen, plus prüfen wie viel positives Delta nötig ist. Delta-Definition wie `or_delta.py` (#077-079, etablierte Methode): `sign(Close-Open) × Volumen` je 1m-Bar, summiert über ein Fenster — Tick-Rule-Proxy für Orderflow-Imbalance aus reinen OHLCV-Daten.

**Drei Tausch-Varianten** (`developer/vwap_delta_test.py`), je EINE Bedingung ersetzt, Bewertung über denselben isolierten Vorwärts-Trefferquote-Test wie #098:

| Ersetzte Bedingung | Long-Trefferquote (IS/OOS) | Long-Drift OOS |
|---|---|---|
| keine (Original, #098) | 53,6% / 53,7% | +0,081 ATR |
| **R1 Preis>VWAP → Delta seit Session-Open** | **54,7% / 55,4%** | **+0,171 ATR** |
| R2 VWAP-Slope → Delta letzte 15min | 53,5% / 53,7% | +0,110 ATR (kein Effekt) |
| R3 1h-Move → Delta-Ratio 1h (Schwellen-Sweep 0-0,30) | 54,0-55,7 %, steigt scheinbar mit Schwelle | Stichprobe schrumpft von n=66634 auf n=1966 OOS bei Schwelle 0,30 — bei 51,3% Trefferquote und +0,42 ATR Drift ist das Rauschen, kein Fund |

**Nur Variante A (R1 ersetzt) ist echt.** Der OOS-Drift verdoppelt sich fast, bei stabiler Stichprobengröße (nicht durch Schwellen-Tuning erkauft — eine strukturelle 1:1-Ersetzung ist weniger overfitting-anfällig als ein Parameter-Sweep). Short bleibt in JEDER Delta-Variante unter Münzwurf, bestätigt #098: die Richtungsregel ist strukturell long-only.

**v7 gebaut: v6 (Long-only + Distanz-Filter) mit R1 ersetzt, R2/R3 und der Distanz-Filter unverändert.**

| | v5 | v6 | **v7** |
|---|---|---|---|
| Win% / expR / PF | 59,4% / +0,028 / 1,12 | 61,1% / +0,031 / 1,15 | **62,3% / +0,041 / 1,20** |
| Sharpe | 0,94 | 1,14 | **1,48** |
| OOS expR / PF | +0,0085 / 1,029 | +0,0113 / 1,043 | **+0,0183 / 1,071** |
| Solo-Pass (intraday) | 46% | 43% | **49%** |
| ⭐ Buch-Beitrag | neutral (+0,00pp) | neutral (+1,60pp, genau auf der Schwelle 1,60) | **BESSER (+1,80pp, über Schwelle 1,60)** |

**v7 ist die erste Version der ganzen VWAP-Runde, die den Buch-Beitrags-Schwellentest tatsächlich überschreitet** (score 1,80 > Schwelle 1,60, 5-Seed-Rauschen 0,8) — nicht nur "schadet nicht mehr", sondern eine echte, wenn auch kleine, Verbesserung für P(funded). Alle Metriken ziehen konsistent mit: bester Sharpe, beste OOS-Kante, beste Solo-Passquote der ganzen Familie (37% → 46% → 43% → 49%). Solo weiterhin nicht käfigtauglich (49% < 60%). E8-Inaktivitätsregel warnt (längste Lücke 21 Tage bei 3,2 Trades/Woche) — rein operativ, braucht einen Keep-Alive-Trade in handelsarmen Wochen, kein Kanten-Problem.

**Einordnung, warum das plausibel ist statt Zufall:** kumulatives Session-Delta misst tatsächliche Kauf-/Verkaufsaktivität (gewichtet nach Volumen), während Preis-vs-VWAP nur den *Preis-Level* relativ zum volumengewichteten Durchschnitt zeigt — zwei Bars können denselben Preis über/unter VWAP haben, aber sehr unterschiedliches Orderflow-Vorzeichen. Delta ist damit eine direktere Messung von "wer gerade die Kontrolle hat" als ein reiner Preisvergleich, was zur Continuation-Mechanik (Gao/Han/Li/Zhou, #097) besser passt als der Preis-Proxy.

### Lehre
68. **Ein struktureller Tausch (eine Bedingung durch eine andere ersetzen) ist robuster zu bewerten als ein Parameter-Sweep, weil er nicht auf einem kontinuierlichen Schwellenwert optimiert.** Der Delta-Schwellen-Sweep (Variante C) zeigte scheinbar steigende Trefferquote mit steigender Schwelle — aber nur weil die Stichprobe dabei auf ein Zehntel schrumpfte. Der sauberste Fund der Runde (Variante A) war keine Schwellenwahl, sondern ein einfacher Ja/Nein-Tausch derselben Bedingung — weniger Freiheitsgrade, weniger Overfitting-Risiko.
69. **Orderflow-Delta (Tick-Rule-Proxy aus OHLCV) kann eine Preis-Bedingung schlagen, wenn beide dieselbe Information ausdrücken sollen.** Preis-vs-VWAP ist ein Level-Vergleich, Delta ist eine direkte Aktivitätsmessung — bei ansonsten identischer Bedeutung ("wer hat die Kontrolle") war die direktere Messung hier die bessere. Bei künftigen Richtungs-/Filterregeln lohnt sich der Vergleich Preis-Proxy vs. Delta-Proxy als Standard-Test, nicht nur als Sonderfall.

## #100 — Delta auf dem Pullback-Trigger selbst: sauberes Negativergebnis (16.08.2026)

Max' Folgefrage zu #099: traegt das Orderflow-Delta INNERHALB der Trigger-Kerze (1m-Basis, kleiner als die 5m-Kerze) zusaetzliche Information? Bisher wurde Delta nur auf Fenster-/Session-Ebene fuer die Richtungsbedingungen getestet (#099), nicht fuer den Trigger selbst. Der Trigger ist rein preisbasiert ("erste rote Kerze") -- zwei Kerzen mit identischem Open/Close koennen voellig unterschiedliches Orderflow-Muster haben.

Getestet an v7's echten Signalen (`developer/vwap_trigger_delta_test.py`, 1768 Trades): 4 Delta-Merkmale der Trigger-Kerze (Gesamt-Delta normiert, Delta letzte 1m-Bar, Delta letzte 2 Bars, Delta zweite Haelfte) plus die klassische Order-Flow-These "Absorption" (Verkauf am Anfang, Kaeufer uebernehmen zum Schluss, waehrend der Preis noch rot schliesst).

**Kein einziges Merkmal haelt IS und OOS gleichgerichtet:**

| Merkmal | Korr. IS | Korr. OOS |
|---|---|---|
| Gesamt-Delta (normiert) | −0,058 | +0,069 — Vorzeichen kippt |
| Delta letzte 1m-Bar | +0,022 | +0,038 |
| Delta letzte 2 Bars | −0,008 | +0,008 |
| Delta zweite Haelfte | +0,004 | −0,004 |

**Die Absorptions-These war sogar falsch herum:** Trigger-Kerzen MIT Absorptionsmuster performten in IS UND OOS schlechter als ohne (OOS expR mit Absorption **−0,0053**, ohne Absorption +0,0269) -- Kaeufer, die schon waehrend der roten Kerze aktiv werden, sind offenbar eher ein Zeichen von Unentschlossenheit als von einem starken Reversal.

**Keine v8 gebaut.** Bei einem so klaren Vorzeichenwechsel zwischen IS und OOS waere jede darauf aufgesetzte Version reines Rauschen-Fitting. v7 bleibt aktiv und die beste Version der Familie.

### Lehre
70. **Nicht jede Delta-Idee traegt -- die Ebene entscheidet.** Delta auf Session-/Fenster-Ebene (R1, #099) trug echte Information; Delta auf der einzelnen Trigger-Kerze (1m-Basis) nicht. Beide klingen a priori plausibel ("Orderflow ist informativer als Preis"), aber nur eine haelt der IS/OOS-Probe stand. Der Test selbst war billig (eine Diagnostik auf bestehenden Trades, keine neue Version noetig) -- bei jeder neuen "wo koennte noch Delta helfen"-Idee lohnt sich dieselbe schnelle Vorabpruefung, bevor eine Version gebaut wird.

## #101 — R:R-Sweep: erste Grade-A-Version der VWAP-Familie (16.08.2026)

Max' Frage: wie verändert sich alles, wenn man das R:R von sehr gering bis sehr hoch durchvariiert? SL fest bei 80 Punkten (validierter Risiko-Anker, #097), TP von 20 bis 240 Punkten (RR 0,25 bis 3,0), sonst v7's exakte Signal-Logik unverändert (`developer/vwap_rr_sweep.py`).

**Erste Erkenntnis: eine klare Falle am unteren Ende.** Bei RR=0,25 (TP=20) sieht die Winrate mit 75,4% spektakulär aus — die OOS-Erwartung ist trotzdem **negativ** (−0,0033). Das Ziel ist so klein, dass Kosten und die wenigen Verlierer (SL 80) den hohen Trefferanteil komplett auffressen. Eine hohe Winrate allein sagt nichts ohne das R:R.

**Kein scharfes Optimum, sondern ein breites Plateau.** Ab RR≈0,5 bis RR=3,0 ist der Buch-Beitrag durchgehend "besser" (+1,6 bis +2,0pp), die Unterschiede zwischen den Werten liegen im Rauschbereich (Streuung ~0,8pp). RR=1,5 (TP=120) lag im Schnelltest leicht vorn.

**v8 gebaut (v7 mit TP 40→120) und mit der vollen Pipeline bestätigt — kein Sweep-Artefakt:**

| | v6 | v7 | **v8** |
|---|---|---|---|
| Grade | C (58) | C (58) | **A (85)** |
| OOS Win% / expR | 62,0% / +0,0113 | 62,7% / +0,0183 | 51,9% / **+0,0250** |
| Sharpe | 1,14 | 1,48 | 1,48 |
| Solo-Pass | 43% | 49% | **50%** |
| ⭐ Buch-Beitrag | neutral (+1,60pp) | besser (+1,80pp) | **besser (+2,00pp)** |

Schnelltest hatte 2,01pp/50% vorausgesagt, Vollrechnung liefert 2,00pp/50% — nahezu deckungsgleich, das ist der Beleg dass der Fund robust ist, nicht ein zufälliger Sweep-Peak. Klassischer RR-Tradeoff: v8 gewinnt seltener (52% statt 63%), aber wenn, dann deutlich mehr — netto die beste Erwartung der ganzen Familie. Solo weiterhin nicht käfigtauglich (50% < 60%), E8-Inaktivitätsregel warnt weiter (Trades/Woche sinkt mit steigendem TP, längste Lücke 21 Tage — operativ, kein Kanten-Problem).

**v8 ist die erste Grade-A-Version der gesamten VWAP-Runde** (#096-#101), nachdem v1 mit Grade F startete.

### Lehre
71. **Eine hohe Winrate ohne das R:R zu kennen ist bedeutungslos.** RR=0,25 zeigte die höchste Winrate im ganzen Sweep (75,4%) bei gleichzeitig negativer Erwartung — der klassische Fehler, Trefferquote mit Qualität zu verwechseln (vgl. Lehre 56: erst das R:R prüfen, dann die Signal-Logik).
72. **Ein breites Plateau ist ein stärkerer Beleg als ein scharfer Peak.** Dass Buch-Beitrag und Solo-Passquote über einen weiten RR-Bereich (0,5 bis 3,0) stabil "besser" bleiben, statt an einem einzelnen Punkt zu spitzen, spricht gegen Zufallsfund — ein einzelner Ausreisser inmitten überwiegend neutraler Nachbarn waere Grund zur Vorsicht gewesen (vgl. Lehre 68).

## #102 — v8 ins Buch: Port, Verifikation, Frac-Neuprüfung, Distanz-Nachtest (16.08.2026)

Max: „bau ihn in mein Portfolio ein, mit der passenden Cushion-Frac". v8 (RR 1:1,5, Delta-seit-Open, Distanz-Filter 2,5 ATR, Long-only, #096-#101) läuft im Developer nur über eine eigene `trades()`-Funktion — Buch-Beine brauchen einen echten `qbt.run_strategy`-Mode.

**Port:** `engine/vwap_pullback.py` neu (Modul-Vertrag wie `or_delta.py`), Dispatch in `qbt.py` unter `mode="vwap_pullback"` registriert, Parameter per `p.get("vwap_*", default)` mit v8s Werten als Default. **Verifiziert wie beim NoiseORB-NinjaScript-Port (#084): 1257 von 1257 Trades identisch** (r, date, tmin_entry) zwischen Developer-`trades()` und `qbt.run_strategy({"mode":"vwap_pullback"})`.

**Als 6. Bein eingetragen** (`NQ_VWAP-Pullback`, Family Trend Following) in `book_state.json`.

**Cushion-Frac neu geprüft** (Lehre 55: jede Buch-Änderung zieht das nach) statt blind übernommen: Sweep von frac 0,14 bis 0,34 für Konto A unter dem vollen 6-Bein-Buch zeigt ein breites Plateau 0,20-0,30, Maximum bei 0,24 (70,4 % 3M) nur +0,2pp vor dem aktuellen 0,22 (70,2 %) — klar innerhalb des üblichen Seed-Rauschens (~0,6-0,9pp). **0,22 bleibt gültig, keine Anpassung.**

`funded_finalize.py` gelaufen: P(funded) Buch 3M 68,6 % → **70,2 %**, 6M 91,0 % → **92,8 %** — deckt sich mit dem vorher gemessenen Buch-Beitrag (+2,00pp, Ø 3M/6M). Portfolio-Tab ist aktuell.

### Nachtrag: VWAP-Distanz-Varianten nachgetestet (Max' Folgefrage)
„Wie wirken sich verschieden hohe VWAP-Varianten aus?" — Distanz-Schwelle (die 2,5-ATR-Regel aus #097) von 0 bis 6 ATR durchvariiert, auf v8's fertiger Basis (RR 1:1,5).

**Methodische Falle selbst gefangen:** der erste Durchlauf verglich gegen das Buch, das v8 SELBST schon enthielt (seit dem Porting-Schritt oben) — jede Variante wurde also gegen eine Baseline getestet, die einen nahezu identischen Zwilling schon enthielt (Korrelation drückt den Grenznutzen). Korrigiert durch Vergleich gegen das ORIGINALE 5-Bein-Buch (ohne v8):

| Distanz | Buch-Delta (ggü. Original-5-Bein-Buch) |
|---|---|
| 0,0 (kein Filter) | +1,95pp besser |
| 1,0-1,5 | +1,4 bis +1,5pp neutral |
| **2,0** | **+2,25pp besser (Spitze)** |
| **2,5 (= v8)** | **+2,01pp besser** |
| 3,0-5,0 | fallend, +1,1 bis +0,4pp |

**Neuer Befund:** mit dem größeren RR (1:1,5 statt 1:0,5) ist jetzt sogar der UNGEFILTERTE Fall "besser" fürs Buch — unter dem alten RR (#097) war er klar "schlechter". Der größere Take-Profit übernimmt einen Teil der Funktion, die vorher nur der Distanz-Filter leistete. Spitze bei 2,0 ATR, aber 2,0 und 2,5 sind bei üblichem Rauschen nicht unterscheidbar — **v8's Wahl (2,5) bleibt bestätigt, keine Änderung.**

### Lehre
73. **Sobald eine Strategie schon im Buch steckt, misst ein „Variante X hinzufügen"-Test automatisch etwas anderes: den Grenznutzen einer ZWEITEN, korrelierten Kopie — nicht mehr, ob X die richtige Wahl fürs EINE Bein war.** Für die zweite Frage muss die Baseline explizit auf den Zustand VOR der Aufnahme zurückgesetzt werden. Bei jedem Nachtest einer bereits eingebuchten Strategie zuerst fragen: vergleiche ich gegen das Buch mit oder ohne sie selbst?
74. **R:R und Signal-Filter sind nicht unabhängig voneinander zu optimieren.** Der Distanz-Filter war unter RR 1:0,5 unverzichtbar (#097: ungefiltert klar „schlechter"), unter RR 1:1,5 ist selbst der ungefilterte Fall „besser". Ein Filter, der unter einer Parametrisierung entscheidend war, kann unter einer anderen redundant werden — nach jeder größeren Parameteränderung lohnt sich ein Rück-Test der vorher als kritisch geltenden Filter.

## #103 — Betriebspunkt fürs Solo-Zwischenfenster: B/C erst in ~15 Tagen (16.08.2026)

Max kauft die 2x25k-Konten (B/C) erst in ca. 15 Tagen (Zielraum ab ca. 31.08.2026). Bis dahin läuft nur Konto A (50k, gekauft, aktiv) — der 3-Konten-Betriebspunkt aus #095/#101 (frac A = 0,22) ist für den **rollenden Plan mit B/C** optimiert, nicht für die aktuelle Solo-Zwischenzeit. Genau der Fall aus Lehre 44 (#089): „Kauft Max die 2x25k nicht, ist der richtige Wert wieder niedriger."

**Umbau:** `book_state.json` — B/C aus `plan.accounts` in ein neues `plan.accounts_pending` verschoben (Definitionen/Notizen bleiben vollständig erhalten, nur zum Zurückschieben in 15 Tagen). Konto A frac 0,22 → **0,14**.

**Solo-Rolling-Sweep** (1 Konto, 2-Evals/Monat-Deckel auf denselben Kontotyp, aktuelles 6-Bein-Buch inkl. NQ_VWAP-Pullback), bewertet nach der Buch-üblichen Ø(3M,6M)-Methode (wie #095):

| frac | 1M | 3M | 6M | 12M | Ø(3M+6M) |
|---|---|---|---|---|---|
| 0,10 | 6,2% | 30,2% | 46,0% | 48,4% | 38,1 |
| **0,14** | 16,3% | 36,0% | 42,9% | 43,6% | **39,45** ← gewählt |
| 0,16 | 19,2% | 36,8% | 40,5% | 40,8% | 38,65 |
| 0,18 | 20,8% | 36,5% | 38,9% | 39,1% | 37,7 |
| 0,22 (alt, Joint-Plan-Wert) | 25,5% | 34,1% | 34,8% | 34,8% | 34,45 |

0,14 gewinnt auf der 3M/6M-Sicht klar; 0,22 ist nur bei reiner 1-Monats-Betrachtung vorn (25,5% vs 16,3%) — aber genau die Sicht zählt hier nicht, weil ohne Nachkauf die Solo-Passquote über die Zeit entscheidet, nicht die Kaufrate.

`funded_finalize.py` bestätigt: P(funded) solo A **1M 16,3% · 3M 36,0% · 6M 42,9% · 12M 43,6%**, Median 42 Tage.

**Bewusst getrennt gehalten: Planungsebene vs. Live-Ebene.** `book_state.json`/Portfolio-Tab ist umgestellt (reine Backtest-/Planungsarbeit). Der Live-`CushionFrac` in `MaxRiskGuard.cs` auf der Box läuft weiter mit 0,22, bis Max den Box-Deploy explizit freigibt — das laufende Live-Konto wird nicht ohne Ansage angefasst.

**Rückbau vorgemerkt:** sobald B/C gekauft sind, B/C zurück nach `accounts`, frac A neu Richtung Joint-Plan-Wert prüfen (nicht blind auf 0,22 zurücksetzen — das Buch hat sich seit #095 durch NQ_VWAP-Pullback verändert, siehe #101).

### Lehre
75. **Der Betriebspunkt eines bereits laufenden Kontos muss neu geprüft werden, sobald sich seine Kaufpolitik ändert — nicht nur wenn sich das Buch ändert (Lehre 55 erweitert).** „B/C kommen erst in 15 Tagen" ist keine Buch-Änderung, aber ändert trotzdem den relevanten Betriebspunkt fundamental (Solo-Rolling statt Joint-Plan). Jede Änderung an WANN oder OB nachgekauft wird, ist eine Kaufpolitik-Änderung im Sinne von Lehre 44 und verlangt dieselbe Neu-Prüfung wie eine Buch-Änderung.
76. **Planungs-Layer-Updates (book_state.json) und Live-Deploy (Box/NinjaScript) sind getrennte Freigabe-Ebenen.** Ein Betriebspunkt-Wechsel lässt sich sofort und risikofrei in der Planung nachziehen; das Scharfschalten auf dem laufenden Live-Konto ist ein separater, expliziter Schritt. Diese Trennung verhindert, dass eine Backtest-Umrechnung versehentlich echtes Kapital-Risiko verändert.

## #104 — Pass/Blow an der echten Historie statt nur MC-Resampling (16.08.2026)

Max' Frage: nicht „wie hätte das Buch auf einem Live-Account performt", sondern **wie oft hätten wir mit unserem Betriebspunkt tatsächlich gepasst / geblowed**. Bisher gab es das nur als Bootstrap-MC (`passmc`, `passmc_vec`, `eval_plan.evaluate`), das i.i.d. Tage zieht. Neu: `eval_plan.rolling_real()` — jeder echte Handelstag ist ein Eval-Start, der die **tatsächlich gelaufene** Zukunft weiterspielt, gleiches Cushion-Sizing, gleicher Käfig, Intraday-Bust. Zählt Pass / Bust / offen (Horizont erreicht) / Datenende.

**Wo es jetzt steht:** Standard-Lab-Report (neue Sektion „Eval Pass/Blow" direkt nach dem Verdict, `copilot.eval_pass_blow` + `report._eval_pass_blow`), Developer-Tab (Solo-Frontier hat Echt-Spalten, Buch-Beitrag zeigt Echt 3m/6m neben MC), `developer_run.py`. `daily_cells`/`combine_cells` sind dabei aus `developer_run.py` nach `eval_plan.py` gewandert (eine Quelle für Developer UND Report).

**Selbst-Korrektur, die im Log bleiben soll:** erste Version verglich Echt bei **50** Tagen Horizont gegen MC bei **365** Tagen — sah aus wie „echt 10 % vs MC 49 %" und ich hätte fast „Clustering" als Ursache verkauft. Auf gleichem Horizont geprüft (Scratch-Test, VWAP-Pullback v8 und 6-Bein-Buch, frac 0.10/0.14/0.22/0.30, Horizonte 50/120/365):

| | MC pass / bust | Echt pass / bust | Echt Pass unter Entschiedenen |
|---|---|---|---|
| Strategie v8, frac 0.14, 1 J. | 49 % / 42 % | 34,5 % / 34,7 % | 50 % (MC 54 %) |
| Buch, frac 0.14, 1 J. | 45 % / 55 % | **51 % / 37 %** | **58 %** (MC 45 %) |
| Buch, frac 0.14, 120 T. | 41 % / 52 % | 31 % / 25 % | 55 % (MC 44 %) |

**Was wirklich bleibt:** (a) die echte Reihenfolge **entscheidet langsamer** als i.i.d.-Bootstrap — deutlich mehr „offen" bei jedem Horizont, in beiden Fällen (Bootstrap mischt jede Marktphase in jeden Pfad, echt bleiben ruhige/wilde Phasen am Stück). (b) Beim Buch ist echt auf 1 Jahr **besser** als MC (weniger Busts), bei kurzen Horizonten niedriger auf Pass UND Bust. (c) Bei der Einzelstrategie ist echt etwas schlechter als MC. Kein Grund, das MC-Kriterium zu kippen — aber ab jetzt steht die Echt-Zahl daneben, mit Horizont-Beschriftung.

**Vorbehalt:** Echt-Fenster überlappen massiv (2 456 Starts ≈ ~10 unabhängige Jahre); und das Buch wurde auf genau dieser Historie selektiert — die Echt-Zahl ist genauso in-sample wie MC.

### Lehre
77. **Zwei Methoden nur auf identischem Horizont vergleichen.** Pass-Quoten sind Horizont-Funktionen; 50 gegen 365 Tage ist kein Befund, sondern ein Artefakt. Jede neue Kennzahl bekommt den Horizont ins Label.
78. **Bootstrap-MC unterschätzt systematisch die „offen"-Quote** (i.i.d. zerhackt Phasen). Wer P(funded) pro Zeit optimiert (#089), sollte die Echt-Historie als Gegenprobe daneben haben — MC allein macht Evals tendenziell schneller entschieden, als sie es sind.

## #105 — News-Fade-Hypothese (Max): Retrace auf Pre-News-Level ist Random-Walk-Basisrate (16.08.2026)
- **Anstoß: Max' Idee** — nach starker News fällt der Preis „im Normalfall" wieder aufs Pre-News-Niveau (oder retraced deutlich). Geprüft mit research-scout (Literatur), quant-mathematician (Struktur + Null-Rechnung) und quant-statistician (eigene 1m-Daten NQ/ES 2016-2026, **316 Events** FOMC/CPI/NFP, 24h-Bars aus `exported_data/`, weil `qbt.load_rth` 08:30-Releases abschneidet).
- **Verdict: ✗ kein Alpha, weder Fade noch Continuation.** Retrace-Quote aufs Pre-News-Level bis Close **66 % (NQ) / 57 % (ES)** — Random-Walk-Null (Reflexionsprinzip `P = 2·Φ(−a/(σ√T))`) sagt **58 %**. Die Beobachtung „kommt meistens zurück" stimmt, ist aber reine Vola-Mathematik. Gegen Placebo (gleich große Nicht-News-Moves, gleiche Uhrzeit) retracen News-Jumps in den ersten 30-60 Min sogar **10-13 pp seltener** (CI ohne Null) — News-Moves halten besser, nicht schlechter.
- **Handelbarer Fade** (Entry T+5, Stop 0,75×ATR20, Exit Close, Kosten): NQ +0,12R [+0,05; +0,20], ES −0,01R, **gepoolt +0,04R (t=0,91)**; NQ/ES-Trades r=0,80 korreliert → ein Test, nicht zwei. DSR bei n_trials≈40 = 0,50, Nachweisgrenze bei n=138 ist 0,15R → unter Power. Split-Half instabil. Starke Jumps (>0,35 %) drehen den Fade negativ (expR −0,19, Mathematiker) — genau dort, wo die Hypothese ihn behauptet.
- **CAL_fomcpost_ES (#034) relativiert:** roher Richtungs-Drift 14:15→Close über 83 FOMCs = −3,6 bp (Null); PF 1,71 kommt aus dem Stop, der den linken Tail abschneidet, nicht aus einer Richtungsprognose. Und n=43 heißt Nachweisgrenze PF ~1,60 — kein „starker Beweis" für Continuation.
- **Literatur:** kein akademischer Beleg für Makro-News-Fade in Index-Futures auf Minuten/Stunden; Sekunden-Overshoot (ABDV 2003) ist HFT-Domäne; Pre-FOMC-Drift „disappearing"; Straddle/OCO um Release nur Folklore. Details im [[Research-Cache]] (neuer Abschnitt).
- **Buch-Relevanz:** ~13-32 Events/Jahr → selbst optimistisch 0,5R/Jahr, weit unter MC-Seed-Rauschen. Kategorie wie #034/#049: nicht fürs Buch. Skripte im Session-Scratchpad (Wegwerf), keine Engine-Datei angefasst.
- **Offen, falls Max weitermachen will:** (a) konditionierter Fade (nur wenn Jump gegen Vortrend/Positionierung, Why vorab), (b) Vorzeichenkurve `sign(J)·r` über 0-1/1-5/5-15/15-30/30-60/60-Close pro Event-Typ, (c) Post-News-Vola-Burst (3-8× normal) als Regime-Filter für bestehende Momentum-Beine statt als eigenes Bein.

### Lehre
79. **„Kommt meistens zurück" ist bei Vola-Bursts die Basisrate, keine Edge.** Bei jeder Retrace-/Touch-Statistik zuerst die Random-Walk-Null (Reflexionsprinzip) und eine Placebo-Kontrolle gleicher Uhrzeit danebenlegen — sonst misst man σ√T und nennt es Mean Reversion.
80. **Fade und Momentum auf demselben Fenster sind ein Nullsummenspiel minus 2× Kosten.** Sehen beide positiv aus, ist mindestens eins Rauschen (n klein) oder es gibt einen echten Vorzeichenwechsel, der dann sauber über Event-Typen nachweisbar sein muss.

## #106 — Zielfunktion v2: „möglichst viele Evals bestehen" statt „möglichst schnell funded" — Käfig-Policy-Sweep, Pool-Neuaufbau, Tier-Vergleich (16.08.2026)

**Anstoß (Max):** „Wie treffe ich das Profit-Target, ohne den max. Drawdown zu reißen?" Bisher wurde dafür genau EIN Skalar optimiert (Cushion-frac in `eval_plan.py`), Zielfunktion war P(funded) in 3/6 Monaten unter rollendem Nachkauf (#089). Neu gebaut: `cage_policy_lib.py` + `cage_policy_sweep.py` (Sizing-Policy und Buch-Zusammensetzung als Parameter, MC-Kern 1:1 aus `eval_plan.py`), fünf Hebel einzeln gemessen, dann quant-mathematician / quant-statistician / strategy-auditor drauf.

**Phase 1, alte Zielfunktion (Zeit-Score) — was gefunden wurde:**
- **Cushion-Sizing läuft verkehrt herum.** Heute: 2 Kontrakte am Anfang, 3 kurz vor dem Ziel (bei +2800 fehlen 200 $, riskiert werden 1282 $ an einem q90-Tag). HJB (Mathematiker): optimale Größe *fällt* in der Restdistanz. Endspurt-Deckel `sz ≤ (target−bal)·k/risk` dreht das Profil um; bei k≈0,2 ist der Cushion-Term komplett redundant. Einziger Hebel, der in beiden OOS-Folds und beiden Zeitfenstern hält.
- **Bein-Auswahl transferiert negativ.** Sieger „nur LastHour+VWAP-Pullback, frac 0,30" = +14,6pp Score, davon +12,6pp reiner frac-Sprung (gegen falsche Basis verbucht) und +2,0pp Auswahl; nested OOS: **−2,95pp**, letzte 2 Jahre −14pp. Auditor: 2022-Strohfeuer (LastHour 2024 −1,6k, 2026 −2,1k). **Verworfen.**
- **Quantil-Anker ist kein Hebel** (`sz = cushion·frac/anker`, nur das Verhältnis zählt — Umparametrisierung).
- **Block-Bootstrap** (Vola-Clustering, acf|dc| ≈ 0,2 über 5 Lags): P(funded)-Zahlen fallen ~7pp (die Tab-Zahlen waren zu optimistisch), Solo-Passquote *steigt* (P konvex in σ, Jensen auf Eval-Ebene). Rangfolge unverändert. Seit heute Standard.
- **Nulldrift-Test (Statistiker):** 88 % des Zeit-Score-Siegers entstehen bei Edge = 0. Der Zeit-Score ist zur Hälfte eine Lotterie-Kennzahl (Nachkauf gratis, Neustarts unabhängig). Solo-Passquote ist die edge-sensitivere Größe.

**Max' Umkehr (Kern dieses Eintrags):** „Ich will nicht möglichst schnell funded, ich will bei möglichst vielen Evals das Target treffen und möglichst selten blowen." → **Zielfunktion v2 = Passquote je Eval bzw. $ pro funded Konto (= Preis ÷ Passquote), Zeit nur noch Kontext.** Mathematik dazu: reine Passquote ist streng monoton fallend in der Größe (kein inneres Optimum, Kelly wäre 0,51 Kontrakte), also **Min-Size 1 Kontrakt je Bein**; damit ist frac raus und **die Kontogröße wird zum Sizing-Hebel**.

**Phase 2, v2 (alles Min-Size, Block-Bootstrap Ø10, 5 Seeds, `cage_v2_*.py`):**
| Tier | Preis | Passquote | $/funded | Median | letzte 3 J |
|---|---|---|---|---|---|
| 25k | 100 | 37,9 % | 264 | 28 d | 36,5 % |
| **50k** | 150 | 59 % | **255** | 98 d | 53 % |
| 100k DD 4 % | 260 | 80 % | 326 | 272 d | 79 % |
| 100k DD 3 % | 260 | 69 % | 378 | 251 d | 66 % |
| **150k DD 4 %** | 390 | **86 %** | 454 | 450 d | **93 %** |
- Nulldrift-Kontrolle überall ~20 % → der Rest ist Edge, keine Geometrie. Heutiges frac 0,14 auf 50k: 47,5 % / 316 $ — schlechter als schlicht 1 Kontrakt.
- **Korrektur AP99 (16.08.2026, spät):** der 3%-vs-4%-DD-Streit bei 100k/150k ist aufgelöst — E8 Help Center Futures (Primärquelle, vom Support-Chat selbst verlinkt) bestätigt **3%**, nicht 4%. Die DD4-Zeilen oben sind damit falsch, `cage_v2_tiers.json`/`cage_v2_tiers.py` korrigiert und neu gerechnet: **100k 68,8 % / 378 $/funded (med 254 d) · 150k 80,4 % / 485 $/funded (med 438 d)**. Der Käfig-Vorteil der großen Tiers ist damit kleiner als in Phase 2 angenommen; 50k bleibt bei $/funded ungeschlagen, 150k bleibt bei reiner Passquote vorn. Siehe [[E8-Support-Anfrage (100k-150k Drawdown + Signature-Status)]].
- **Pool-Neuaufbau (22 Kandidaten** = Buch + Live-Bank + 13 je getestete Alt-Strategien, Walk-Forward 2016-22 ↔ 2023-26, Marginal-Test Buch+1 nur OOS): **kein einziges Bein verbessert das Buch OOS**, beide Walk-Forward-Auswahlen sind auf der Testperiode klar schlechter als das Buch (41,9/37,1 % vs 56,3/61,8 %). Grund: bei Min-Size ist „Bein dazu" = „mehr Position"; ein Bein hilft nur, wenn seine Drift/Risiko über der des Buchs liegt — hat keins. Alt-Strategien (Gap-cont, Overnight, RV_mom, FLIP, PIV): alle −4 bis −15pp.
- **Gewichte im Buch (Leave-one-out, Split 2016-22 / 2023-26 / 2025-26):** **ohne NQ_Momentum +10,4 / +4,4 / +3,9pp** auf 50k, +3,5 / +5,1 / +5,2 auf 100k, Inaktivität ok (7 d) — einziger Buch-Befund, der in jedem Fenster und Tier gleich zeigt. → **In #108 (AP98) widerlegt: die Zahlen stimmen, „in jedem Fenster und Tier" nicht.** Die drei Fenster sind ineinandergeschachtelt; disjunkte 2-Jahres-Fenster ergeben +1,0 ± 7,8pp mit zwei stark negativen. Die 100k-Spalte rechnete zudem mit dem inzwischen gestrichenen `dd4`-Käfig. **Entscheidung: Momentum bleibt drin.** Ohne LastHour nur im neuen Regime besser (+17), reißt die 7-Tage-Inaktivitätsregel (11 d) und bricht 2016-22 auf 100k ein → nein. Momentum x2 / LastHour x2: −12 bis −15pp.
- Tagesstopp bei Min-Size: 50k +1pp (nichts), 100k +4pp (Stopp 120 $/Kt), 150k +4pp (250 $).
- Parallele Evals auf demselben Buch mit gleichem Start sind *eine* Eval (P(≥1) = P(1)); Staffelung um 2 Monate: 4 Konten → 88,7 %; $/funded bleibt gleich.

**Umgesetzt:** `eval_plan.evaluate_v2` + `funded_finalize.py` (`plan.v2` in `portfolio.json`), Portfolio-Tab Kopfzahl = Passquote je Eval + $/funded je Tier (Zeit-Kaufplan als Kontext-Block), `book_state.json` Plan-Block (`objective`, A frac 0,01 = Min-Size, B/C 25k **gestrichen**), `cage_v2_tiers.json`. **Offen / Max' Entscheidung:** (1) ~~NQ_Momentum aus dem Buch nehmen (Empfehlung: ja, mit Statistiker-Gegenlesen vor dem Deploy)~~ → **erledigt in #108: nein, bleibt drin** (Gegenlesen hat den Befund gekippt), (2) Ersatz für B/C: weitere 50k (billigster $/funded) oder 100k/150k (höchste Passquote, DD-Regel 3/4 % vorher schriftlich klären; „Signature" evtl. Auslaufprodukt), (3) Live-Umstellung CushionFrac auf der Box = separater Deploy.

**Vorbehalt (Statistiker):** Buch-Drift 1. Hälfte 5,8 $/Tag, 2. Hälfte 45 $/Tag — Vollperiodenzahlen mischen zwei Märkte, deshalb steht die Letzte-3-Jahre-Spalte jetzt überall daneben. Und: 25 $ Drift gegen 317 $ Tagesvola bleibt ein Münzwurf mit Übergewicht; Policy holt Prozentpunkte, neues Alpha die Größenordnung.

### Lehre
81. **Zielfunktion vor Hebel.** „P(funded) pro Zeit" belohnt Größe und Nachkauf-Lotterie, „Passquote je Eval" belohnt Min-Size — dieselben Daten, entgegengesetzte Empfehlung. Erst festlegen, was optimiert wird, dann rechnen; Nulldrift-Test als Pflichtkontrolle, ob eine Kennzahl Edge misst oder Geometrie.
82. **Bei Min-Size ist Diversifikation nicht gratis.** Ein Bein mit 1 Kontrakt lässt sich nicht kleiner machen; „mehr Beine" heißt „mehr Exposure" und senkt die Passquote, sofern das Bein nicht mehr Drift pro Risiko bringt als das Buch. Kontogröße ist dann der Sizing-Hebel, nicht frac.
83. **Bein-Selektion braucht nested OOS, nicht Split-Half der Bewertung.** Wer auf der ganzen Historie auswählt und dann halbiert, testet nur die Bewertung; die Selektion selbst transferierte hier negativ. Marginal-Test „Buch + 1, nur OOS" ist die ehrliche Frage.
84. **Zwei Reviews vor der Empfehlung, wenn selektiert wurde** (Statistiker: Multiple Testing/OOS, Auditor: Regime/Praxis/Regeln). Beide haben heute je einen Fund gekippt, den der Sweep als Sieger führte (2-Bein-Buch, 3-Bein-„Sicher"-Buch mit Inaktivitätsbruch).

## #107 — Rückkehr zum NY-Open (Max) + Delta als Filter: Trennung real, Geometrie frisst sie auf (16.08.2026)
- **Anstoß: Max' Idee** — nach 09:30 läuft der Preis im ersten Leg weg vom Open und wird „oft wieder zum Open gehandelt". Danach Nachfrage: **lässt sich per Delta filtern, wann er zurückkommt und wann nicht?** Geprüft mit eigener Messung (NQ 1m RTH, **2612 Tage 2016-01 bis 2026-07**) + quant-statistician; Skripte `open_reversion_probe.py` / `open_reversion_delta.py` (neu, keine bestehende Engine-Datei angefasst).
- **Verdict Fade: ✗ NO-GO, und zwar zum zweiten Mal.** Der Statistiker hat die Alt-Last gefunden: **#008 (06.07.2026) hat genau das schon gemessen** (`mode="ts_reversal"`, `rev_side="fade"`, `rev_base="open"`, inkl. `rev_exit="open"`) → edge −6 %, PF < 1. Zusammen mit `archiv/gen_reversal_study.py` (23 Varianten) und `archiv/overnight_lab.py` (16) trägt die Idee eine **Alt-Last von ~40 Trials**, bevor der erste neue Backtest läuft.
- **Nullmodell (neu, schärfer als #008):** Vorzeichen-Flip der Minuten-Returns — `|r_t|` bleibt Bar für Bar erhalten, also **exakt dieselbe Intraday-Vola-Kurve** (die am Open am höchsten ist), Bar-Spannen gespiegelt, nur Autokorrelation/Drift zerstört. Ergebnis: Touch-Rate real **48,1 %** vs. Null **52,7 %** (z = −2,96) nach 0,5σ-Ausschlag in 5 Min; Varianzratio erste 30 Min = **1,019**. Der Preis kommt also **seltener** zum Open zurück als ein driftloser Pfad gleicher Vola — die ersten 30 Min sind minimal trendig. Fade-PnL −0,16 R (n=1840, t = −4,89), Pullback-Einstieg in Richtung des Legs ebenfalls negativ (−0,064 R, t = −1,99).
- **Delta-Frage (echtes Aggressor-Delta aus dem Trade-Tape, `orderflow2`, 2016-2026):** Trennung ist **real, aber klein**. Sauberstes Feature `pts_per_kdelta` (Punkte Preisbewegung je 1000 Netto-Kontrakte = „wie dünn ist der Move gelaufen"): Touch-Rate **56,1 % → 64,5 %** über die Terzile, monoton (+0,91), stationär (ρ mit Zeit −0,01), IS/OOS gleich (AUC 0,553/0,547), überlebt die Kontrolle auf künftige Vola (z = +2,58). `delta_norm`/`delta_last2` zeigen dieselbe Richtung schwächer: **viel gleichgerichtetes Delta → seltener Rückkehr** (Aggressor hält), wenig/gegenläufig → häufiger.
- **Aber: reicht nicht für Geld.** Fade nur im besten Delta-Terzil: **meanR −0,0013 (t = −0,03)**, Win 45,9 % gegen **Geometrie-Baseline 43,5 %** — also **+2,4 pp über der Nullerwartung**, und das deckt gerade die Kosten. Ohne Filter −0,074 R, in allen anderen Terzilen −0,11 bis −0,17 R. Der Filter hebt die Strategie von „verliert" auf „verliert nichts mehr", nicht auf „verdient". Statistiker-Gate 1 (≥ 3 pp über `p_triv = s/(s+d)`) **nicht bestanden** → Abbruch vor Gate 2-8.
- **Zwei Mess-Artefakte unterwegs entlarvt** (wichtiger als der Fund selbst, gilt für jede künftige Orderflow-Arbeit):
  1. **`avg_trade_size` und `vol_per_pt` sind nicht stationär** (ρ mit Zeit −0,83 bzw. −0,67; Mediane 2,35 → 1,35 bzw. 0,184 → 0,020 über 2016-2026, Marktstruktur). Global gebildete Quantile darauf sind faktisch ein **Jahres-Indikator**: Q1 = späte Jahre, Q5 = frühe. `avg_trade_size` sah mit z = −4,29 wie das stärkste Signal aus und war ein Regime-Effekt. Verräterisches Symptom: **kein einziger Jahresblock enthielt beide Extremquantile.**
  2. **Anlaufbereich rollierender Ränge:** mit `min_periods` < Fenster bekamen 10 % aller Werte einen Rang von exakt 0,0; das unterste Dezil bestand zu **89 % aus 2016/2017** (n=80 statt 242) und zeigte eine scheinbare Delta-Wirkung. Fix: volles Fenster verlangen + Bins **rangbasiert** statt über Quantilgrenzen (`digitize` erzeugte sonst Dezile mit n=80 neben n=390).
- **Was offen bleibt (Max' Entscheidung, nicht eigenmächtig weitergefittet):** die Trennung zeigt in die **Gegenrichtung** nutzbar — niedriger `pts_per_kdelta` / viel stützendes Delta = **keine** Rückkehr = Fortsetzung. Das ist der Zustand, den `NQ_Momentum` (Bein im Buch, aus #008) handelt. Ob das als Filter dort P(funded) hebt, ist eine eigene Frage mit eigenem Marginal-Test (Buch + Filter, nur OOS, 5 Seeds) — und `NQ_Momentum` steht in #106 ohnehin zur Disposition.

### Lehre
85. **Lehre 79 gilt auch ohne News.** „Kommt oft zum Anker zurück" ist am NY-Open genauso Basisrate wie nach News (#105) — hier sogar **unter** der Basisrate. Vorzeichen-Flip der Minuten-Returns ist dafür die schärfste Null: erhält die Vola-Kurve exakt und testet nur die behauptete Pfad-Eigenschaft.
86. **Orderflow-Rohgrößen vor jeder Quantil-Analyse auf Stationarität prüfen** (ρ mit Zeit). Marktstruktur driftet über 10 Jahre stark; ein nicht-stationäres Feature global zu quanteln misst das Jahr, nicht den Flow. Kontrollfrage, die es sofort auffliegen lässt: enthält jeder Zeitblock beide Extremquantile?
87. **Ein Filter, der die Trefferquote hebt, hebt nicht automatisch den Erwartungswert.** Immer `p_triv = s/(s+d)` danebenlegen: +8 pp Touch-Rate wurden hier vollständig von der Payoff-Geometrie aufgefressen (Endstand exakt 0,000 R). Trefferquote ohne Geometrie-Baseline ist eine Verkaufszahl, keine Kennzahl.

## #108 — AP98 entschieden: NQ_Momentum bleibt drin. Der „+4 bis +10pp in jedem Fenster"-Befund war eine Fensterwahl (16.08.2026)

**Frage:** Das einzige Buch-Ergebnis aus #106, das nach einer klaren Empfehlung aussah — NQ_Momentum aus dem Buch nehmen, +10,4 / +4,4 / +3,9pp Passquote auf 50k über 2016-22 / 2023-26 / 2025-26. Mathematiker und Statistiker parallel drauf, dazu ein eigener Schiedsrichter-Lauf, weil sie sich in einem Punkt direkt widersprachen.

### Die Mechanik (Mathematiker): das Kriterium passt in eine Zeile
Alles hängt am Skalenparameter der First-Passage-Lösung, `theta = 2·mu/sigma²`. Ein Bein trägt im **fixen** Käfig genau dann, wenn

```
mu_i / mu_rest  >  (sigma_i² + 2·cov(i,rest)) / sigma_rest²
```

| | mu/Tag | sd/Tag | SR ann | Anteil Drift | Anteil Varianz |
|---|---|---|---|---|---|
| Buch (6 Beine) | 25,45 | 317,2 | 1,23 | | |
| ohne Momentum | 18,24 | 222,8 | **1,25** | | |
| Momentum solo | 7,21 | 176,5 | 0,62 | 28,3 % | 40,8 % |

Break-even-Drift 18,72 $/Tag, geliefert 7,21 ± 3,13. Geschlossene Zweiphasen-Formel (Trailing bis Peak = DD, danach Gambler's Ruin) gegen MC: 45,7 → 55,8 % Formel vs. 58,9 → 66,4 % Engine, Abweichung vollständig durch Tages-Sprünge, Schiefe und Intraday-Check erklärt. Rangfolge in jeder Modellstufe gleich. **Kein Edge-Argument, ein Positionsgrößen-Argument** — Buch-Sharpe ändert sich nicht (1,23 → 1,25).

Wichtiger Nebenbefund gegen die naive Lesart: skaliert man das **Rest-Buch** auf dieselbe Vola hoch (λ = 1,42), kommt es auf 52,7 % — das Buch *mit* Momentum auf 59,3 %. Momentum ist die bessere Art, Exposure zu tragen; es ist nur zu viel Exposure für einen 2000-$-Käfig.

### Warum es trotzdem nicht reicht (Statistiker)
1. **Die drei Fensterzahlen sind reproduzierbar** (62,50→72,76 / 57,03→61,08 / 53,87→57,98) — aber `cage_v2_weights.py` zeigt für „letzte 3 Jahre" nur +0,12pp, und das ist **kein Bug und kein Seed-Rauschen, sondern die Fenstergrenze**: Zeile 30 startet bei 01.07.2023, das Ticket-Fenster bei 01.01.2023. Die 120 Handelstage H1-2023 drehen das Delta von **+4,05 auf +0,22**. Beide Werte sauber reproduziert, Seed-sd nur 0,4-0,8pp.
2. **Nulldrift-Kontrolle im aktuellen Regime:** gemessenes Delta l3 = +0,22pp, reine Geometrie = **+2,17pp**. Der Edge-Anteil des Streichens ist heute **negativ**.
3. **Disjunkte 2-Jahres-Fenster** (der ehrliche nested-OOS-Blick auf eine fixe Hypothese): −7,2 · **−22,0** · +9,5 · +18,5 · +6,3 → Mittel **+1,0 ± 7,8pp**, 2 von 5 stark negativ. „In jedem Fenster" hält nicht; der Vollperiodenwert +6,8 wird komplett von 2020-2023 getragen.
4. **Power:** Bootstrap-sd des Deltas 4,5pp (voll) / 6,7pp (l3). Um 3pp von 0 zu trennen, bräuchte man ~45 Jahre Historie. Die Frage ist mit vorhandenen Daten **nicht entscheidbar**.
5. Das Bein selbst ist sauber: n = 1284, mean R +0,1247, Block-Bootstrap-CI [+0,061; +0,190], PF 1,21, DSR 0,86/0,67/0,51 bei n_trials 12/50/150. Und es ist 2024-26 mit 11,7k $ der größte Einzelbeitrag im Buch.

### Der Widerspruch zwischen den beiden — und wie er ausging
Auf 150k sagte der Mathematiker +8,69pp, der Statistiker **−2,06pp**, beide mit denselben korrigierten AP99-Tiers. Eigener Schiedsrichter-Lauf (`scratchpad/ap98_horizon.py`):

| Käfig | Horizont 36 M | Horizont 120 M |
|---|---|---|
| 50k | +6,69 | +6,69 |
| 100k | +8,47 | +9,56 |
| 150k | **−1,69** | **+8,93** |

**Reine Zensur.** Ohne Momentum ist das Buch langsamer (Median 98 → 152 Tage auf 50k, ~450 Tage auf 150k); ein 36-Monats-Horizont bewertet auf 150k nicht mehr, er schneidet ab. Auf 50k — dem Käfig, der real läuft — ist der Horizont egal. Das Vorzeichen-Argument fällt damit weg, die Punkte 2 und 3 nicht.

### Entscheidung: nein, Momentum bleibt drin
Nach Max' eigener Messlatte (#106, Lehre 83): Nulldrift-Kontrolle im aktuellen Regime **nicht bestanden**, nested OOS **nicht bestanden**. Positive Edge ist notwendig, nicht hinreichend — und hier trägt nicht einmal der Befund selbst. `book_state.json` unverändert, kein `funded_finalize.py`-Lauf, kein Box-Deploy. Deckt sich mit #095, wo dieselbe Frage schon einmal mit „drin lassen" beantwortet wurde.

Was der Befund richtig benennt, bleibt aber offen und geht als **AP101** weiter: Momentums Vola senken, ohne seine Drift wegzuwerfen — `MOMSEL_NQ_er0.3_s0.75` (#057, einziger Kandidat mit echter Train→Test-Bestätigung) als Replace, `rev_stop_mult 0.30` nur als In-Sample-Hinweis. Und der Größenhebel liegt sowieso eine Größenordnung höher im Käfig selbst (50k 59,4 % → 100k 68,8 % → 150k 80,4 %) — das ist AP99.

### Lehre
88. **Ein Fenster ist eine Entscheidung, keine Beobachtung.** Zwei Fensterstarts sechs Monate auseinander (01/2023 vs 07/2023) drehen dasselbe Delta von +4,05 auf +0,22 — mehr als jedes Seed-Rauschen und mehr als jede Modellstufe. Wer Fenster nennt, muss die Grenze mitnennen; wer „in jedem Fenster" schreibt, muss disjunkte Fenster zeigen, nicht ineinandergeschachtelte.
89. **Zensur sieht aus wie ein Vorzeichenwechsel.** Ein fixer MC-Horizont bestraft das langsamere Buch doppelt, und je größer der Käfig, desto stärker. Tier-Vergleiche brauchen einen Horizont, der die Median-Dauer klar überdeckt, sonst misst man die Uhr statt die Strategie (AP102).
90. **Wenn Mathematik und Statistik dasselbe Vorzeichen für unterschiedliche Zeiträume liefern, ist die Frage nicht „wer hat recht", sondern „welcher Zeitraum handelt".** Beide Agents kamen unabhängig auf dieselbe Kennzahl (Break-even-Drift 25,94 vs. geliefert 18,51 im aktuellen Regime = 1,0 se) und leiteten daraus entgegengesetzte Empfehlungen ab. Der Unterschied war reine Gewichtung von Vollhistorie gegen Jetzt-Regime — das gehört explizit entschieden, nicht implizit über die Wahl des Rechenlaufs.

## #108 — VWAP-Cross am NY-Open ist eine Wegmessung, kein Signal (16.08.2026)
- **Anstoß: Max' Folgeidee zu #107** — nach dem Ausschlag vom 09:30-Open liegt der Preis auf einer Seite des Session-VWAP; Signal = **Cross zurück durch den VWAP** Richtung Open, spiegelbildlich je Seite (oben + Cross runter = Short, unten + Cross hoch = Long), mit oder ohne Delta. Nachfrage Max: **verschiedene VWAP-Arten und Zeitbasen**. Geprüft mit eigener Messung (`open_vwap_cross.py`, `open_vwap_variants.py`) + quant-statistician (unabhängig, eigene Skripte, 4 Märkte).
- **Verdict: ✗ tot, und der Trigger war schon da.** `mode="vwap_trend"` in `qbt.py:883-935` ist genau dieser Cross (Zarattini Holy Grail), zweimal **Grade F** (`archiv/gen_holygrail.py`: 19.053 Trades, expR −0,026; `archiv/refine.py` MOVES: expR +0,0008, PF 1,004). **Alt-Last ~120 Trials** inkl. #107 und der v1-v8-VWAP-Familie.
- **Der Grund, analytisch:** Der anchored VWAP **startet auf dem Open** und löst sich nur langsam davon — |VWAP − Open| im Median **0,20σ bei t=5, 0,29σ bei t=15, 0,37σ bei t=30, 0,48σ bei t=60**. Bei Trigger 0,5σ liegt der VWAP damit per Konstruktion bei ~60 % des Wegs zurück zum Open. „Cross" ist im Opening-Fenster ein Synonym für **„mehr als die Hälfte retraced"**. Gemessen: Median-Retracement beim Cross **0,62**.
- **Zahlen (NQ 2612 Tage 2016-2026, Target = Open):** Cross meanR **−0,053**, Win 66,5 % gegen **Geometrie-Baseline 71,1 %**. Statistiker gepoolt NQ/ES/YM/RTY: Lift über `s/(s+d)` = **−0,92 pp, 90 %-CI [−2,53; +0,70], n_eff 2355** → Gate 1 (+3 pp) nicht knapp verfehlt, sondern **oberhalb des CI ausgeschlossen**. Auf `p_triv`-Bins gematchtes Placebo: −0,33 pp. Alle 6 Zweijahresblöcke negativ.
- **8 VWAP-Arten × 2 Exits, keine schlägt das Placebo:** `sess_930` −0,053 · `globex` (ab 18:00 ET Vortag) −0,036 · `on_frozen` (Overnight-VWAP als festes Level) −0,042 · `roll30` −0,069 · `roll60` −0,054 · `sess_5m` −0,048 · `sess_15m` −0,055 · `tvwap` (echter Trade-VWAP aus dem Tape) −0,049. Bester Abstand zum Placebo +0,011 (globex) bei 2/5 positiven Blöcken. **Auch die nicht am Open verankerten Varianten helfen nicht** — sie lösen zwar den Konstruktions-Confounder, liefern aber keine eigene Information.
- **Delta-Bestätigung hilft nicht:** Delta stützt die Umkehr (Vorzeichen) → bestes Ergebnis −0,015 R (t = −0,64, statistisch Null); Schwelle 0,10 → n bricht 1548 → 132 und wird **schlechter** (−0,082). Muster wie Lehre 68.
- **Long/Short:** beide negativ (−0,084 / −0,058). Statistiker: die Asymmetrie **dreht sich gegenüber #098/#099 um** (dort Long tragend, hier Short) und keine Zelle erreicht |z| > 2 → Seiten-Asymmetrie ist hier Stichprobenrauschen, kein Struktureffekt.
- **Power-Befund für künftige Runden:** es sind **0,46 Cross-Ereignisse/Tag**, nicht ~1. NQ allein: MDE 3,87 pp bei 80 % Power — ein 3-pp-Effekt würde nur in 58 % der Fälle gefunden. **Ein NQ-only-Lauf wäre kein Negativergebnis, sondern ein Nicht-Ergebnis.** Tages-Residuen-Korrelation der 4 Märkte ρ = 0,32 → gepoolt n_eff 2355 (nicht 4631), MDE 2,75 pp.
- **Eigener Testfehler, gefunden und korrigiert:** in der ersten Fassung wurden auch Signale gehandelt, bei denen der Preis das Open **schon durchlaufen** hatte — dann liegt das Target hinter dem Einstieg und der Trade ist rechnerisch ein garantierter Verlust. Betraf 12 % (`sess_930`) bis **67 %** (`on_frozen`) der Cross-Fälle und ließ die nicht am Open verankerten Varianten künstlich katastrophal aussehen (Win 24 % gegen Geometrie 81 %). Fix in `open_vwap_cross.py`; die oben genannten Zahlen sind die korrigierten.
- **Placebo-Konstruktionsfehler (Statistiker):** ein fixes Retracement-q trifft die Zielfraktion nicht, weil der Einstieg überschießt (q=0,548 → realisiert 0,607), die Roh-Trefferquote springt dadurch auf 69,5 %. Richtig ist Matching auf **(`p_triv`, Zeit)**-Bins, nicht auf q — Cross-Events kommen im Median bei t=18 min, Fraktions-Events bei t=22 min, und die Touch-Rate hängt an der Restzeit.

- **Fixes RR gegen Open-Level als Ziel (Max' Nachfrage, `open_vwap_rr_sweep.py`, 18 Kombis):** **alle negativ**, bestes Ergebnis RR 0,5 nach Placebo −0,021 (t = −1,42). Ein festes RR ist zwar durchweg besser als das Open-Level (faire Geometrie statt „Target rückt beim Warten näher, Stop klebt am Extrem"), aber es dreht nichts ins Positive. Zusatz-Kontrolle **„sofort einsteigen statt auf ein Signal warten"**: durchweg am schlechtesten (−0,098 bis −0,190) — das Warten hilft also, aber der **VWAP-Cross schlägt dabei nie das Retrace-Placebo** (RR 0,5: Cross −0,046 vs. Placebo −0,021).
- **⚠️ Methodenfalle bei hohem RR mit Zeit-Notausgang:** bei RR 3,0 nach Cross steht Win 37,3 % gegen Geometrie-Baseline 25,0 % — scheinbar **+12 pp Edge**, tatsächlich meanR −0,064. Auflösung über die Exit-Verteilung: Stop 52 %, **Target nur 7 %**, Zeit-Exit 41 %. Die „Gewinner" sind überwiegend Zeit-Exits mit kleinem positivem R, die als Win zählen, aber nie die vollen 3R zahlen. **`p_triv = s/(s+d)` gilt nur ohne Zeitlimit** — mit Zeit-Notausgang ist der Vergleich Win-Rate vs. Geometrie-Baseline irreführend und muss durch die Exit-Verteilung (Stop/Target/Zeit) ergänzt werden.

### Lehre
88. **Vor jedem „neuen" Ereignis-Trigger prüfen, ob er nur eine Umparametrisierung der schon kontrollierten Geometrie ist.** Der VWAP-Cross misst im Opening-Fenster den Retracement-Anteil, und der steckt per Definition bereits in `p_triv = s/(s+d)`. Ein Signal, das mit der Kontrollvariable zusammenfällt, kann nichts dazugewinnen.
89. **Bei einem Level-Target prüfen, ob das Target zum Signalzeitpunkt noch VOR dem Einstieg liegt.** Sonst entstehen mechanische Verlust-Trades, die wie ein Markt-Befund aussehen — hier bis zu 67 % der Fälle bei einem nicht am Open verankerten Anker.
90. **Power vor Gate.** Ein Gate von +3 pp ist wertlos, wenn die MDE des Designs bei 3,9 pp liegt: dann ist „nichts gefunden" kein Ergebnis. Vor der Runde Ereignisrate × effektives n (Cluster-korrigiert) gegen die Gate-Schwelle rechnen, nicht danach.
91. **Ein Level-Target und ein festes RR sind zwei verschiedene Wetten, nicht zwei Exits derselben Strategie.** Beim Level-Target (hier: Open-Preis) verschlechtert jedes Warten auf Bestätigung die Geometrie automatisch, weil das Ziel näher rückt während der Stop am Extrem bleibt. Bei festem RR ist die Geometrie vom Wartezeitpunkt unabhängig. Wer einen Bestätigungs-Trigger testet, muss ihn deshalb mit festem RR testen — sonst misst er den Geometrie-Verfall statt den Trigger.
92. **Trefferquote immer zusammen mit der Exit-Verteilung lesen.** Sobald ein Zeit-Notausgang existiert, sind „Wins" teils Zeit-Exits mit Kleinstgewinn; die Win-Rate steigt dann über die Geometrie-Baseline, während der Erwartungswert fällt. Stop/Target/Zeit-Anteile gehören in jede Ergebniszeile.

## #109 — News-Kerzen-Level (Open/High/Low) tragen nichts, und News-Level halten schlechter als beliebige Level (16.08.2026)
- **Anstoß: Max' Folgeidee zu #107/#108** — dieselbe Anker-Logik auf die 1-Min-Kerze, in der eine News rauskommt: Open (= Pre-News), High und Low als spätere Level, jeweils auch mit VWAP-Gedanken. Geprüft mit eigener Messung (`news_level_probe.py`) + quant-statistician (unabhängiger Pilot, 319 Events NQ / 323 ES).
- **Verdict: ✗ tot.** Nach Lehre 88 wurde nicht „wird das Level getestet" gefragt (das ist entartet), sondern **was am Level passiert**, gegen ein distanzgematchtes Placebo.
- **Gate 0 sofort gerissen — die Barriere ist entartet:** Median-Abstand vom Messpunkt T+5 zum News-Kerzen-Extrem = **−0,2 Punkte**. Der Preis steht fünf Minuten nach dem Release faktisch **auf** dem Level. Touch-Quote bis Close **95,6 %**. Genau der VWAP-Mechanismus aus #108, nur ohne Umweg: ein Level, das per Auswahl dort liegt wo der Preis gerade ist, wird fast sicher berührt. (Präzedenz stand schon in #051: „89 % Touch-Quote ist near-tautologisch".)
- **Eigene Messung (543 News-Kerzen, Range UND Volumen ≥3× Median derselben Minute, 2016-2026, Auflösung C = konservativste):** Touch-Raten Open 79,2 % / High 86,4 % / Low 77,2 % gegen **Placebo (beliebiger Preis in gleicher Entfernung) 81,0 / 83,4 / 83,2 %** — das Level wird nicht öfter berührt als irgendein Preis derselben Distanz. **Break UND Bounce beide negativ** bei allen drei Leveln und bei RR 1,0 wie RR 2,0 (−0,05 bis −0,17 R); bester Wert Low-Bounce −0,045 (t = −0,66, 4/11 Jahre). Beide Richtungen negativ = kein Signal, nur Kosten (Lehre 80).
- **Statistiker-Pilot bestätigt das Vorzeichen und schärft es:** symmetrisches Bracket (±q, Payoff 1:1, Null exakt 50 % — damit ist die Payoff-Geometrie konstruktiv ausgeschaltet). News-Kerzen-Extrem **55,8 % [51,5; 60,2]** gegen distanzgematchtes Placebo-Level **58,7 % [55,7; 61,7]**, gepaarte Differenz **−12,1 pp [−18,5; −5,4]**. Gegen die nackte 50-%-Null sieht das News-Level positiv aus, **gegen ein beliebiges Level am selben Tag ist es schlechter.** Passt exakt zum #105-Placebo (News-Moves retracen 10-13 pp seltener): hinter News-Leveln steht echter Informationsfluss, sie halten deshalb schlechter.
- **⚠️ Der größte Fund der Runde — die Auflösung der Touch-Bar entscheidet mehr als jede Edge:** dieselben Daten, dasselbe Level, nur andere Verbuchung der Fill-Bar → **A 59,5 % · B 54,8 % (qbt-Standard) · C 44,1 %**. Diese Spanne ist größer als jede Edge, die hier je gefunden werden könnte. Das ist die News-Level-Fassung der `orb_exec="book"`-Falle (#066/#067). Unsere Messung lief auf **C** (Entry am Open der Bar NACH dem Touch), also der konservativsten.
- **Alt-Last ~130 Trials, Trigger existiert zweimal im Bestand:** `orb_exec="retest"` (`qbt.py:428-450`, ruhende Limit AM Level nach Close-Confirm) ist genau der benötigte Trigger; `orb_retest_068.py` = **36 von 36 Varianten OOS negativ** (#068, „zweite ehrliche Falsifikation"); `pivot.py`/`pivot_discovery.py` (#051) = 52 Configs, 47 sterben IS. Plus #105 (~40, identischer Eventsatz). Mit dem Anker-Komplex (#107 ~40, #108 ~120) sind es **~290**.
- **Gegenseite der News-Kerze gestrichen statt getestet:** sie liegt im Median **16-18 % weiter weg** als das Pre-News-Niveau (Touch 72,1 % vs. 79,9 %) — also #105 mit härterer Barriere, strikt schlechter als das, was dort schon scheiterte.
- **Ökonomie ist die bindende Schranke, nicht Power:** bei 28 Events/Jahr, Min-Size und q = 0,5×Range bringt selbst eine Trefferquote von 60 % nur **+0,69 pp** Passquote, die `book_contribution()`-Hürde liegt bei ~1,2 pp (2× Seed-Streuung). Nötig wären **65,8 %** (q = 0,5) bzw. 58,8 % (q = 1,0) — der Zielkorridor liegt **komplett oberhalb aller bisherigen Messungen dieser Familie** (55,8 %, gegen Placebo negativ). Statistische Nachweisgrenze bei n≈260: 57,7 %.
- **Praxis-Einwand (unbewertet, aber notiert):** 08:30 ET liegt eine Stunde vor RTH, die News-Kerze hat im Median **41,8 NQ-Punkte** Range gegen 6,2 an normalen Tagen. Slippage auf einer ruhenden Limit-Order an einem Level, das in einer 6,7-fach erweiterten Kerze definiert wurde, ist im Backtest nicht abgebildet.
- **Literatur (research-scout):** keine dedizierte Quelle zu News-Kerzen-Leveln. Aber **Osler 2000 (FRBNY) / Osler 2003 (J. Finance)** liefern den Why-Rahmen: Support/Resistance wirken in FX nur, wenn sie **echte Order-Cluster** (Stop-/Take-Profit-Häufungen) abbilden, nicht bloße Chart-Geometrie — ohne Order-Cluster ist ein Level nur eine Distanzangabe, genau was unser Placebo zeigt. Einschränkung: FX-Dealer-Markt mit Kundenorderdaten, nicht 1:1 auf zentralisierte Futures übertragbar.
- **Umgesetzt:** `news_calendar.py` (neu) sichert die Eventliste dauerhaft — #105 und #109 hatten sie je im Session-Scratchpad rekonstruiert, das aufgeräumt wird. Modi `core` (FOMC+NFP+CPI, 338 Events, 30,7/Jahr) und `wide` (FOMC + alle 08:30-Kerzen mit volratio ≥3, 591 Events, 53,7/Jahr; Zusatztage clustern auf Donnerstag und Monatstag 14-15/26-28 = Claims, PPI, Retail Sales, PCE — dieselbe Hypothesenklasse, keine Verwässerung). **Nicht `calendar_fx.FOMC` für Event-Studien nehmen**, die Liste beginnt erst 2021.

### Lehre
93. **Ein Level, das per Auswahl dort liegt wo der Preis gerade war, ist keine Barriere, sondern eine Definition.** Median-Abstand ≈ 0 und Touch-Quote 95,6 % heißen: „wird es getestet" ist beantwortet, bevor man misst. Die einzige sinnvolle Frage ist, ob AM Level etwas anderes passiert als an einem beliebigen Preis derselben Distanz — und das braucht ein distanzgematchtes Placebo, kein Zeitreihen-Placebo.
94. **Die Verbuchung der Fill-Bar vorab festlegen und mitschreiben.** Touch-Bar zählt / zählt mit Gleichstand als Bruch / Rennen erst ab Folgebar spannen hier 44 bis 60 % auf, ohne dass sich an den Daten etwas ändert. Wer das nachträglich wählt, wählt sein Ergebnis.
95. **Ein symmetrisches Bracket (±q, Payoff 1:1) ist die sauberste Testform für „passiert hier etwas".** Die Null ist exakt 50 %, damit kann keine Payoff-Geometrie eine Trefferquote auffressen (Lehre 87 konstruktiv ausgeschaltet) und kein Zeit-Exit sie aufblähen (Lehre 92).
96. **Vor der Power-Rechnung die Ökonomie rechnen.** Hier war nicht die Statistik die Schranke, sondern der Käfig: bei 28 Events/Jahr und Min-Size ist die nötige Trefferquote für einen messbaren Buch-Beitrag höher als die statistisch nachweisbare. Wenn „beweisbar" und „relevant" sich nicht überlappen, ist die Runde vor dem ersten Backtest entschieden.

## #110 — GEX-Datenquelle validiert: der freie SqueezeMetrics-Wert misst etwas Reales (16.08.2026)
- **Anstoß:** Nach fünf toten Anker-Ideen (#105/#107/#108/#109) die Frage von Max, welche Signale außer Delta und VWAP überhaupt eine belastbare Datengrundlage haben. research-scout: von 6 Kandidaten überlebt **einer** — Dealer-Gamma. Direkte Prädiktor-Literatur: **Barbon/Buraschi „Gamma Fragility"** ([SSRN 3725454](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3725454), Panel-Regression von lagged Dealer-Gamma auf Intraday-Vola/Spreads/Autokorrelation, 5-60-Min-Frequenzen) und **Baltussen/Da/Lammers/Martens** (JFE 142(1) 2021, 60+ Futures 1974-2020).
- **Das Problem, das den Test nötig machte:** beide Papers rechnen Gamma aus **Options-Chains mit Open Interest je Strike**. Max' freie SqueezeMetrics-CSV (SPX-Tagesschluss, naive Annahme Dealer long Calls / short Puts) ist eine **andere, unabhängig unverifizierte Konstruktion**. Die Literatur belegt das Konzept, nicht die Datenquelle. Deshalb erst Datenvalidierung, dann Strategie — genau der Schritt, der in #105-#109 fünfmal gefehlt hat.
- **Verdict: ✓ die freie CSV misst etwas Reales.** `gex_validate.py`, NQ+ES 2016-2026, 2634/2635 Tage. Prädiktoren vom **Vortages-Close** (kein Look-ahead), t-Werte **Newey-West** (Lag 5, sonst wären sie bei autokorrelierter Vola deutlich zu groß).

| Vorhersage der Literatur | ES (SPX-Future) | NQ |
|---|---|---|
| **V1** hohes Gamma → niedrigere Vola(t), roh | β −0,959 (t −18,2) | β −0,921 (t −18,6) |
| V1 kontrolliert für Vola(t−1) | β −0,272 (t −5,5) | β −0,142 (t −6,2) |
| **V1 kontrolliert für Vola(t−1) + VIX(t−1)** | **β −0,235 (t −6,9)** | **β −0,129 (t −5,5)** |
| **V2** hohes Gamma → Varianzratio kleiner (mehr MR), kontrolliert | β −0,039 (t −2,7) | β −0,030 (t −2,1) |

- **⭐ Die Falsifikationsprüfung besteht (K3):** der GEX ist **SPX**-basiert, also muss der Effekt auf **ES stärker sein als auf NQ** — genau so ist es (−0,235 vs. −0,129, also fast doppelt). Wäre NQ stärker gewesen, wäre die Datenquelle verdächtig. Das ist der Test, der den Befund von einer bloßen Korrelation unterscheidet.
- **Der Effekt überlebt die härteste Kontrolle:** GEX ist teilweise ein VIX-Proxy (Terzil-Mediane VIX 21,0 / 16,4 / 13,9), und Vola ist stark autokorreliert. Nach Kontrolle für **beides** bleibt der GEX-Koeffizient signifikant — er trägt Information über VIX und die Vortagesvola **hinaus**. Terzile ES: realisierte Vola 0,0087 → 0,0044, Varianzratio 0,932 → 0,874 (mehr Mean Reversion bei hohem Gamma, wie vorhergesagt).
- **Stationarität geprüft (Lehre 86 angewandt):** GEX-Rohwert ρ(Zeit) = **+0,40**, Median 1,84e9 (2012) → 5,35e9 (2026) — nicht stationär, roh gequantelt wäre er ein Jahres-Indikator. Gerechnet wurde deshalb auf dem **rollierenden 250-Tage-Perzentilrang**.
- **DIX bestätigt den scout-Negativbefund:** NQ β +0,003 (t +0,14), ES t +2,82 mit für die These falschem Vorzeichen. Zhu (RFS 2014) und Comerton-Forde/Putniņš (JFE 2015) sind echte Primärquellen zum Dark-Trading, **keiner testet den Dark-Anteil als Return-Prädiktor**. DIX bleibt ohne externe Validierung.
- **⚠️ Was das NICHT heißt:** Der GEX sagt **Volatilität** voraus, nicht **Richtung**. Vola-Prognose ist ein bekannt leichtes Problem (Vola clustert, Returns nicht) und ist noch keine Edge. Der Schritt von „sagt Vola voraus" zu „hebt die Passquote" ist offen und der eigentliche Test. Offen bleibt auch, ob der VIX-Zusammenhang nichtlinear ist — kontrolliert wurde linear.
- **Daten:** `exported_data/DIX_GEX_daily.csv` von Max frisch gezogen, jetzt 2011-05-02 bis **2026-08-14**, 3845 Zeilen; Überlappung mit dem 11.08.-Stand bitgleich (max. Abweichung 0 auf 3841 Tagen, keine Revisionen). Quelle `https://squeezemetrics.com/monitor/static/DIX.csv`, freier Direktdownload — **Link kann sterben**, für Live-Einsatz täglicher Pull auf der Box plus Fehler-Alarm nötig.
- **Nächster Schritt (offen, Max entscheidet):** GEX-Rang als **Regime-Gate über bestehende Beine** (kein neues Bein — Lehre 82), Marginal-Test „Buch + Gate, nur OOS", 5 Seeds, Intraday-Bust, Min-Size. Erst dort entscheidet sich, ob aus dem validierten Prädiktor Passquote wird. Erst wenn das trägt, lohnt die Frage nach echten Options-Chains (Theta Data ~40-80 $/Monat, CBOE DataShop) für **NDX**-Gamma statt SPX-Proxy.

### Lehre
97. **Datenquelle vor Idee validieren.** Wenn Literatur ein Konzept belegt, die eigene Datenquelle aber eine andere Konstruktion ist als die der Papers, ist die erste Messung nicht die Strategie, sondern: reproduziert meine Quelle den publizierten Zusammenhang? Das kostet keine Trials, hat keine Freiheitsgrade und beantwortet dauerhaft, ob sich alles Weitere lohnt.
98. **Ein instrumentenspezifischer Prädiktor muss dort am stärksten wirken, wo er herkommt.** SPX-GEX muss auf ES stärker sein als auf NQ. Solche eingebauten Falsifikationsprüfungen sind wertvoller als jeder zusätzliche Signifikanztest — sie können nur bestehen, wenn das Signal echt ist.

## #111 — NQ_LastHour: Literatur-Filter durchgetestet (Schwelle, VIX, Volumen, Makro-Tage, Zarattini-Band) — v2-Bein macht das Buch schlechter, Filter machen es harmlos, keiner ist bewiesen (17.08.2026)
- **Anlass (Max):** Research-Scout auf SSRN/Scholar (neu im [[Research-Cache]]: Rosa 2022 JFM, Li/Sakkas/Urquhart 2022 JFM, Jin/Kearney 2020, Zarattini/Aziz/Barbon 2024, Heston/Korajczyk/Sadka, Mesfin 2026 arXiv, Quantitativo-NQ-Test), danach alle Parameter des Developer-Beins `nq-lasthour v2` (long-only, ref 240, thr 0,2 %, Stop 0,4×Range) darauf abklopfen.
- **Werkzeug:** `lh_filter_study_111.py` (Tages-Tabelle mit allen Features + Trade-Ergebnis je Stop-Mult → jede Variante ist nur eine Maske; Bewertung in **Dollar** und R, IS/OOS ab 2023-05-12, nested Walk-Forward jährlich, Letzte-3-Jahre-Spalte). ~150 Varianten in 5 Familien. Ergebnis `lh_filter_study_111.json`, Features `lh_filter_study_111_days.parquet`.
- **Familie A (Schwelle/Stop/Kontinuum):** thr 0,2 %/Stop 0,4 bleibt der beste $/yr-Punkt (1371). Stop 0,25 hat kleineren DD (-1337 statt -2263), kostet aber 27 % $/yr. Schwelle relativ zur Vola (morn/ATR20) ≤ Basis, kein Gewinn. Rollierendes Perzentil ≥0,7 sieht gut aus (OOS avg 21 $), Nachbarn 0,6/0,8 und die ATR-Variante fallen ab → Spike, verworfen. **Rosas „Schwelle schlägt Always-Active" bestätigt (thr 0 → avg 9,2 $ statt 13,1), mehr nicht.**
- **Familie B (VIX/RV-Regime):** Oktil-Profil sieht nach Stufe bei VIX ≈ 19 aus (darunter ~0 $/Trade, darüber +23..34 $). VIX ≥ 18: n 525, avg 24,7 (IS 24,3 / OOS 26,3 / L3y 26,8), PF 1,51 — **aber $/yr 1235 < 1371, Sharpe 0,97 = Basis**: halbiert Trades, verdoppelt Erwartung, kein Geld mehr pro Jahr. Statistiker: kein Bin mit |t| > 2, isotone R² 2,2 %, Sprungstelle im Bootstrap nicht identifiziert (90 %-Band 11,5-19,1), Jahre 2020/2024 negativ, Solo-Lücke bis 454 Tage (E8-Wochenregel). **Als Kontext richtig, als Filter nein.**
- **Familie C (Volumen, 4 Fenster × 11 Schwellen):** kein „mehr Volumen = stärker" (Jin/Kearney) — VolFirst30 ≥ 1,0 kippt OOS negativ. Einziges stabiles Muster: „Tag ist nicht tot" (Opening-Volumen ≥ 0,8× 20d-Median), avg 16,1 / OOS 16,9 / $/yr 1443. Statistiker: t 1,70, p_FWER 0,96, Plateau schmal → **Rauschen mit Schwelle**.
- **Familie D (Makro-Tage, `news_calendar` core):** an FOMC/NFP/CPI-Tagen n 129, avg -10,6 (IS -0,6 / OOS -31,4); ohne sie n 967, avg 16,3, $/yr 1501, DD -1871, Sharpe 1,12 — einziger Filter, der $/yr UND avg$ UND DD hebt und 88 % der Trades behält. **Widerspricht Gao/Han** (News-Tage stärker). Statistiker: Δ +3,2 $ [1,0; 5,4], p einzeln 0,013, p_FWER 0,51; 44 % des Effekts hängen an 5 Tagen; News-Tage selbst nicht nachweisbar negativ (t -1,03) → „entfernt Rauschen, keine belegte Verlustquelle". Geschrumpft +2,4 $/Trade, $/yr 1433.
- **Familie E (Zarattini-Noise-Band auf NQ, long-only):** band 0,75/Check 60 min: n 1336, avg 10,5, $/yr 1342, PF 1,21, DD -3088, OOS avg 17,6 — funktioniert wie LastHour, ist dieselbe Mechanik (Intraday-Momentum ins Close) mit mehr DD; kein zweites Bein.
- **Greedy-Stapelung** (VIXrel + VolMorn + VolFirst30 + News + Close-in-Range) → n 372, avg 32 $, aber $/yr 1141 < Basis. Nested WF über die ganze Suche: **Δ +0,9 $/Trade [−2,1; +5,9], P(Δ≤0) = 0,39** — das ist der ehrliche Erwartungswert der Filter-Suche.
- **Developer-Versionen (Buch = aktuelles Buch ohne LastHour, Passquote v2 = 77,1 %):** v2 → 75,2 % (**−1,9, schlechter**), v3 „ohne Makro-Tage" → 77,9 % (+0,8, neutral), v4 v3+Opening-Vol → 78,0 % (+0,8, neutral), v5 v3+VIX≥18 → 79,2 % (+2,1). Solo 50k: 51 / 58 / 56 / 45 %. Mathematiker (Lundberg-θ, Block-8-MC): C (v4) > D (v3) > B (v5) > A (v2) in jeder Sicht, Buch +2,9 / +1,9 / +2,3 pp — **aber „gefiltertes LastHour drin" vs. „LastHour raus" kippt mit dem Resampling** (Block: drin besser, iid: raus besser). Robust ist nur: **v2 ist überall das Schlusslicht.**
- **Größter Befund am Rande:** die Basis hängt an 2022 (46 % des P&L, ohne 2022 nur 7,9 $/Trade), Top-5-Trades = 36 %, kurt 28,7 — jede Passquoten-Rechnung mit 13 $/Trade wettet auf ein 2022 im Eval-Fenster.
- **Entscheidung (Empfehlung Claude, Max entscheidet):** LastHour auf **v3 (ohne Makro-Tage)** stellen — billig, vorab formulierbar, 88 % Frequenz, kein Verlust in irgendeiner Metrik; keine +10 pp erwarten, sondern +0 bis +3. v4/v5 nicht ins Buch (Statistik trägt sie nicht). Kandidat für den Kick: „LastHour ganz raus" ist im Buch gleichauf mit v3 (76,6 vs 77,9 Block-8) — Marginal-Test „Buch + 1, nur OOS" steht noch aus.
- **Offen:** (1) Statistiker-Vorschlag, billig: News-Filter **vorab spezifiziert** auf NQ_Momentum / VWAP-Pullback / ES anwenden — muss familienweit auftauchen, sonst ist er auch hier tot. (2) `evaluate_v2` mit `horizon_months=36` verzerrt Solo-Vergleiche niedrigfrequenter Beine (E8 hat kein Zeitlimit) → für Solo ≥120 nehmen. (3) `book_contribution()` misst weiter gegen „Buch ohne das Bein" — passt hier, weil `replaces_leg` gesetzt ist.

### Lehre
99. **Vor-Sortierung von Filtern/Beinen unter Min-Size: Lundberg-Exponent θ (E[e^{−θX}] = 1, ≈ 2μ/σ² pro Trade), nicht Sharpe und nicht $/Jahr.** P(pass) hängt nur von θ·D und θ·U ab; die Trade-Zahl steckt nur in der Dauer. Sharpe kürzt das $-Niveau weg und rankt Frequenz, $/Jahr ist nur der Zähler. Placebo-Ausdünnung: Trades zufällig um die Hälfte kürzen kostet 1,7 pp Passquote — Frequenz ist unter v2 fast neutral.
100. **Ein Filter, der OOS-Werte als Auswahlkriterium benutzt hat, hat keinen OOS-Wert mehr.** Der Greedy in #111 verlangte „OOS avg > Basis" — die +13 $ OOS von F1+F2 sind In-Sample. Nur der IS-Δ (+3) und der nested WF (+0,9) sind unkontaminiert, und die liegen genau bei der Shrinkage-Schätzung.
101. **Multiple Testing bei Filter-Sweeps: die Null-Verteilung des BESTEN aus ~100 Varianten liegt bei t ≈ 2,4.** Ein Fund mit t 2,7 ist damit Erwartungswert unter reiner Null. Bevor ein Filter ins Buch geht, muss er entweder t ≥ 3,1 oder eine vorab formulierte, anderswo prüfbare Hypothese haben (Lehre 97/98).

## #112 — Auction Market Theory (Value Area/POC/Initial Balance) systematisch getestet: Friedhof, wie IB-Extension #056 (17.08.2026)

- **Anlass (Max):** nach der Research-Scout-Recherche (AMT akademisch praktisch unbelegt, siehe [[Research-Cache]]) selbst nachprüfen — VAH/VAL-Rejection, POC-Magnet vs. Beschleunigung, Value-Area-Breakout (Retest-zum-POC vs. Momentum-weg, mit Volumen), Balance-vs-Trend-Regime, Initial-Balance-Breakout-Failure (mit Volumen), alles zusätzlich mit Order-Flow kombiniert, auf NQ **und** ES, mit viel Zeit und ausführlich.
- **Werkzeug (neu):** `engine/amt_profile.py` — Vortags-Volume-Profile aus 1m-OHLCV (Bar-Volumen gleichmäßig auf die H-L-Range verteilt, Bin 5 Ticks), POC/VAH/VAL bei 70 % Value-Area, Initial Balance (erste 60 Min), Balance-vs-Trend-Klassifikation (Tagesrange ≥ 2× IB-Breite = Trend Day). Alle Level sind Vortageswerte (look-ahead-frei), IB ist die heutige eigene, ab Minute 60 verwendet. Tagestabellen gecacht: `developer/amt_daily_{NQ,ES}.parquet`, 2709/2707 Tage (2016-2026).
- **Stufe 1 (reine Signalmessung, kein Backtest, wie `vwap_direction_test.py`/`orderflow_power.py`):** `developer/amt_diag_1_levels.py` (Cross-Events durch VAH/VAL/POC, Value-Area-Breakout, IB-Breakout-Failure, Forward-Return in ATR20-Einheiten, Splits nach Volumen-Tertil und Vortags-Regime) + `developer/amt_diag_2_orderflow_regime.py` (Order-Flow-Bestätigung mit echten Aggressor-Daten aus `D:/trading-data/orderflow/v2`, Regime-Persistenz-Autokorrelation).

### Rohbefund
- **VAH/VAL-Rejection und POC-Magnet: kein robustes Vorzeichen.** avgR@30min überall 0,0007–0,02 R, zwischen NQ und ES oft gegenläufig (z. B. POC-Cross-nach-oben: NQ +0,006, ES −0,0069). „Beyond-Rate" (Level hält nach 30 Min noch) liegt bei 52–58 % statt 50 % — sieht nach leichtem Continuation-Bias aus, ist aber laut Mathematiker **reiner Random-Walk-Overshoot**: die beobachtete 1/√h-Abnahme (62 %→56 %→57 % über h=5/15/30/60) reproduziert exakt das Φ(δ/σ√h)-Modell ohne jede Information.
- **Value-Area-Breakout (Retest-POC vs. Momentum-weg):** NQ/ES uneinheitlich auf der Oberseite, auf der Unterseite beide positiv (NQ +0,0116R, ES +0,0159R) — aber kleine Stichprobe (n≈650-700) und laut Statistiker tail-getrieben.
- **Initial-Balance-Breakout-Failure:** Failure-Rate 42–49 % (knapp unter Coinflip, leichter Continuation-Bias). Einziger über beide Symbole konsistenter Fund: High-Volumen-Tertil zeigt mehr Fortsetzung als Low/Mid (NQ +0,014R, ES +0,016R vs. ~0R).
- **Balance-vs-Trend-Regime-Persistenz: tot.** Autokorrelation 0,01–0,02, Split-Half kippt sogar das Vorzeichen (NQ H1 −0,0065/H2 +0,0327, ES H1 +0,0419/H2 −0,0015). Gestriges Regime sagt heutiges nicht voraus.
- **Order-Flow-Bestätigung (echte Aggressor-Daten):** uneinheitlich, Vorzeichen kippt zwischen Symbolen (z. B. IB-Breakout-oben: bei NQ ist „Delta stimmt überein" sogar *schlechter* als „stimmt nicht überein"). Kein #099-Analogon.

### Quant-Team-Befund (Mathematiker + Statistiker, unabhängig, parallel)
- **Kosten schon in der Größenordnung des Effekts:** NQ Round-Turn-Kosten ≈ 0,0031–0,0051 R, ES ≈ 0,0133–0,0177 R — auf ES sind die reinen Kosten **größer** als die meisten gemessenen Rohsignale.
- **Der einzige cross-symbol-konsistente Fund (IB-Hochvolumen-Continuation) zerfällt komplett:** brutto gepoolt t=2,64 — aber die beiden Serien sind am selben Tag korreliert (corr(fwd30)=0,58), das echte kombinierte t liegt bei ≈2,0. Nach Kosten (Tag-Block-Bootstrap, NQ+ES gleicher Tag = ein Cluster): **netto +0,0020 R, 90 %-CI [−0,0086; +0,0133], t=0,36.** ES netto sogar −0,0027 R.
- **Kein Trefferquoten-Shift:** P(fwd30>0) ist über die Volumen-Tertile praktisch identisch (0,530–0,535) — der ganze „Effekt" kommt aus den Tails (Top-5-von-546-Events = 55–66 % der Summe, 20 %-getrimmter Mittelwert NQ isoliert ≈ 0,0001). Ein echter informierter-Orderflow-Mechanismus müsste die Trefferquote verschieben, nicht nur die Tails.
- **Multiple Testing:** 160 getestete Zellen (Haupttabelle + Volumen-Tertile + Regime + Orderflow), Null-Erwartung für das Maximum liegt bei t≈2,8–3,1 — der beste Fund (t=2,64 brutto, 2,0 netto korrigiert) liegt **unter** dem Zufalls-Maximum.
- **Power-Rechnung:** um die gemessene Effektgröße mit t=2 abzusichern, braucht es ~816 Events; vorhanden sind 546 bei ~52/Jahr/Seite → **~16 Jahre bis zu einer echten OOS-Bestätigung.** Ein Effekt, der sich innerhalb des Anlagehorizonts prinzipiell nicht verifizieren lässt, ist kein Eval-Kandidat.
- **Bezug zu #056:** strukturell derselbe Mechanismus wie das damals mit 0/72 Survivors beerdigte IB-Extension — das High-Volumen-Tertil hier *ist* das späte Ausbruch-Cluster (Minute ~145 statt ~92 bei Low). Ein Volumen-Filter obendrauf macht daraus keinen neuen Mechanismus, und ein bereits beerdigter Fund braucht bei Wiederaufnahme stärkere Evidenz, nicht schwächere.

### Gesamtverdikt
**Auction-Market-Theory-Level (Value Area, POC, Initial Balance) tragen auf NQ/ES keine tradeable Kante — Friedhof, wie IB-Extension #056.** Kein Developer-Build, kein neues Bein. Deckt sich mit dem Research-Scout-Befund (AMT ist auch akademisch praktisch unbelegt) und mit den bereits bekannten Mustern dieses Buchs: reine Mean-Reversion an einem "Fair-Value"-Level ist tot (VWAP #002-005, jetzt auch POC/VA), einziger real belegter Nahbereichs-Effekt bleibt Continuation mit Distanz-Filter (#097-101).

### Lehre
102. **Bei binären Schwellenwert-Metriken ("hält der Level", Beyond-Rate) immer zuerst gegen das Random-Walk-Overshoot-Modell prüfen** (P ≈ Φ(Distanz-beim-Cross / (σ·√Horizont))) **bevor sie als Signal gelesen werden.** Hier reproduzierte das Modell den beobachteten 1/√h-Abfall exakt — die scheinbare Kante war reiner Overshoot am Schwellenwert, keine Information.
103. **Cross-Symbol-Bestätigung (NQ und ES zeigen dasselbe Vorzeichen) ist keine unabhängige Evidenz, wenn beide Serien am selben Tag korreliert sind.** Hier lag corr(fwd30, NQ vs. ES) bei 0,58 — das naive Aufaddieren der t-Statistiken beider Symbole täuschte t=2,64 vor, korrekt kombiniert waren es nur ≈2,0. Vor jeder "zwei Märkte bestätigen sich"-Aussage die Tages-Korrelation zwischen den Symbolen prüfen.
104. **Ein bereits beerdigter Mechanismus (hier: IB-Extension, #056) braucht bei Wiederaufnahme STÄRKERE Evidenz als beim Erstversuch, nicht schwächere.** Ein zusätzlicher Volumen-Filter ist kein neuer Mechanismus, wenn er strukturell dieselbe Sub-Population (hier: späte Ausbrüche) selektiert, die beim Erstversuch schon durchgefallen ist.

## #113 — Session-VAH/VAL (Asia/London/NY, developing statt Vortag): Reversal-Rate war ein Barrieren-Artefakt, kein Signal (17.08.2026)

- **Auftrag Max:** Schritt-für-Schritt-Vertiefung von #112, nur VAH/VAL — aber jetzt developing (nicht Vortag) über alle 3 Sessions (Asia 19:00-03:00, London 03:00-09:30, NY 09:30-16:00 ET) und 3 Anker (Globex-Tagesanfang, Session-Anfang, letzte Stunde), Frage: wie viel Volumen/Order-Flow braucht es, einen Trend an der VAH/VAL umzukehren, und welche Session/welches Instrument neigt eher zu Breakout vs. Mean-Reversion.
- **Vorab-Recherche (Research-Scout):** keine akademische Quelle testet, wann eine Range "fertig" ist — die 60-Min-Initial-Balance ist CBOT/Dalton-Konvention, nicht statistisch hergeleitet, und Rekord-Statistik von Random Walks (Majumdar/Ziff, PRL 2008) zeigt: unter reinem Zufall gibt es keinen natürlichen Fertig-Zeitpunkt. Deshalb bewusst **developing** statt fixer Cutoff gebaut (`amt_profile.developing_profile_expanding/_rolling`, look-ahead-frei, Recompute alle 5 Min).
- **Werkzeug:** `developer/amt_session_vaval.py`, Test-Event = Preis läuft in ein Band um VAH/VAL, Decision-Window (Volumen/Delta messen) getrennt vom Outcome-Window (Auflösung: "broke" vs. "reversed").

### Drei Selbst-Korrekturen unterwegs (der eigentliche Wert dieser Runde)
1. **Tautologie:** Erstversion maß Volumen/Delta im selben Fenster, das auch das Outcome definierte — `tick_delta` ist direkt aus der Preisrichtung gebaut, die auch "broke"/"reversed" bestimmt. Delta-AUC kam auf 0,83–0,90. Fix: Decision-Window (10 Bars) strikt getrennt vom Outcome-Window (30 Bars danach, keine Überlappung).
2. **Degenerierte Order-Flow-Daten:** echte Aggressor-Daten (buy_vol/sell_vol) sind 2016 zu 100 % und 2017 zu ~39 % exakt 0 (Platzhalter). Fix: Order-Flow-Messung auf 2018+ beschränkt.
3. **NaN-Propagation im AUC-Code:** `sum()` über Ränge mit eingemischten NaN (Events ohne Order-Flow-Abdeckung) ergab NaN statt eines Werts. Fix: `dropna()` vor der Rangberechnung.

### Der eigentliche Befund kam vom Quant-Team, nicht von mir
Nach allen drei Fixes sah es immer noch nach etwas aus: Reversal-Rate Asia 82–84 %, London 76–78 %, NY 63–65 % (konsistent NQ+ES, alle 3 Anker fast gleich), Volumen-/Delta-AUC 0,57–0,70. Mathematiker und Statistiker haben unabhängig voneinander denselben, vierten Fehler gefunden:

- **Asymmetrische Barrieren.** Das Test-Event triggert bei Preis ≈ `level − margin`. Die Auflösung sucht "broke" bei `level + 2·margin` (Abstand **3·margin** vom Einstieg) und "reversed" bei `level − 2·margin` (Abstand **1·margin**). Reines Gambler's-Ruin ohne jede Information ergibt daraus `P(reversed) = 3/(3+1) = 75 %` — nicht 50 %. Statistikers Null-Simulation (driftloser Random Walk, echte Session-Geometrie) reproduziert Asia 80 %/London 69 %/NY 58 % (beobachtet 83/78/64) — **die echten Werte liegen sogar UNTER dem Zufallsniveau**, nicht darüber.
- **Placebo-Beweis (Mathematiker):** derselbe Code mit dem Level künstlich um ±0,25×Range verschoben (kein VAH/VAL mehr, ein beliebiger Preis) liefert praktisch dieselben Reversal-Raten (Asia 84,1 % real vs. 73,9–72,3 % Placebo, London/NY noch näher beieinander). **Das Level selbst trägt keine Information** — jeder beliebige Preis in der Nähe hätte dieselbe Zahl geliefert.
- **Session-Unterschied ist reine Vola-Geometrie, kein AMT-Effekt:** `margin` war an die Tages-ATR gekoppelt (fix über alle Sessions), aber Asia-Bar-Vola ist nur ~1/2,7 der NY-Bar-Vola → dieselbe Barriere ist in Asia relativ viel weiter weg → fast nur die nahe Barriere ("reversed") wird je erreicht. Die Rangfolge Asia > London > NY ist exakt das, was die Barrieren-Geometrie allein vorhersagt.
- **AUC 0,57–0,70 ebenfalls Artefakt:** `vol`/`delta` gehen nur als `abs()` (Aktivitätsmaß, richtungslos) ein. Bei 3:1-Barrieren ist Volatilität die einzige Größe, die die ferne Barriere überhaupt erreichbar macht — Volumen ist ihr Proxy, die AUC > 0,5 ist mechanisch erzwungen. Beweis: am Placebo-Level war die AUC sogar noch höher (0,65–0,80) als am echten VAH/VAL (0,60).
- **Bonus-Fund (Mathematiker):** `margin` wurde aus `max(h)-min(l)` **des ganzen Tages** berechnet — am Vormittag ist die Tagesrange aber noch gar nicht bekannt. Ein zusätzlicher, unabhängiger Look-ahead-Fehler, der die Handelbarkeit selbst bei positivem Befund kaputt gemacht hätte.

### Gesamtverdikt
**Kein Signal, reines Konstruktionsartefakt — landet im selben Friedhof wie #112.** Ökonomisch zusätzlich tödlich: das implizite R:R der 3:1-Barriere braucht **75 % Trefferquote allein für Break-even**, NY (64 %) ist damit vor Kosten bereits klar negativ (~−175 $/Trade), Asia (84 %) liegt zwar über 75 %, aber unter seinem eigenen Zufalls-Nullwert. Kein Developer-Build, kein Buch-Beitrag.

**Falls die Frage trotzdem sauber zu Ende gemessen werden soll** (Mathematiker-Vorschlag, 3 kleine Code-Änderungen): (1) symmetrische Barrieren ±2×margin ab dem tatsächlichen Einstiegspreis statt ab dem Level, (2) `margin` aus rollierender Vortages-ATR statt Tages-Range desselben Tages (Look-ahead raus) plus Session-Vola-Normierung, (3) eine Placebo-Spalte (Level ± 0,25×ATR) fest als Nullbaseline mitlaufen lassen, (4) signiertes statt betragsmäßiges Delta für die Volumen-/Order-Flow-Frage — bisher nie sauber gemessen, weil `abs()` jede Richtungsinformation wegwirft. Ohne konkreten Anlass nicht von selbst weiterverfolgen, da zwei unabhängige Methoden (Simulation + Placebo) bereits übereinstimmend auf Null zeigen.

### Lehre
105. **Bei First-Passage-/Barrieren-Tests (Preis trifft Level X, löst sich A oder B auf) IMMER die Abstände vom tatsächlichen Einstiegspreis zu beiden Auflösungs-Schwellen ausrechnen, bevor man die Trefferquote interpretiert.** Ein 3:1-Abstandsverhältnis erzeugt unter reinem Zufall bereits 75 % "Erfolg" für die nähere Schwelle — eine beobachtete Rate von 60-85 % kann allein aus der Test-Geometrie kommen, ganz ohne Marktinformation. Symmetrische Abstände ab dem Einstiegspreis (nicht ab einem Referenz-Level) sind die Voraussetzung dafür, dass 50 % die richtige Nullhypothese ist.
106. **Ein Placebo-Level (zufälliger Preis statt des echten Signal-Levels), durch denselben Code gejagt, ist der schnellste Weg, ein First-Passage-Konstruktionsartefakt von einem echten Level-Effekt zu trennen.** Liefert der Placebo dieselbe Zahl wie das echte VAH/VAL, trägt das Level nichts — unabhängig davon, wie plausibel die Geschichte dahinter klingt.
107. **Eine Test-Schwelle (hier: `margin`), die an eine über mehrere Sessions/Regime hinweg unterschiedlich volatile Referenzgröße gekoppelt ist (Tages-ATR angewandt auf Asia UND NY gleichermaßen), erzeugt allein durch die Vola-Differenz einen scheinbaren "Session-Unterschied".** Vor jedem Cross-Session-Vergleich prüfen, ob die Test-Schwelle auf die jeweils EIGENE Vola der Gruppe normiert ist — sonst misst man die Normierung, nicht das Phänomen.

## #114 — Wann ist das NY-Profil "geformt"? VAH/VAL-Bounce sauber negativ, POC-Rückkehr war ein vierter Artefakt (17.08.2026)

- **Auftrag Max:** noch enger fokussiert — nur NQ, nur NY-Session, und die konkrete Frage aus #113 nachgezogen: WANN (nach wie viel Zeit/Volumen/Breite) ist das Profil so weit geformt, dass VAH/VAL als Bounce-Level und POC als Rückkehr-Ziel am besten funktionieren?
- **Werkzeug (neu):** `developer/amt_ny_formation.py`, diesmal mit allen #113-Lehren von Anfang an eingebaut: symmetrische Barrieren ab dem tatsächlichen Einstiegspreis (Lehre 105), feste Placebo-Spalte (Lehre 106), fester Tick-Margin ohne Tages-ATR-Look-ahead. 15 Formations-Kriterien: Zeit seit 09:30 (7 Werte), Anteil am rollierenden 20-Tage-Volumenschnitt (4 Werte), Value-Area-Breite in Ticks (4 Werte). An jedem Formations-Punkt wird das Profil eingefroren (POC/VAH/VAL fix für den Rest der Session).

### Test 1 (VAH/VAL-Bounce): sauber negativ, Methodik hält
Reversal-Rate real vs. Placebo bei **allen 15 Varianten praktisch identisch** (Gap −0,015 bis +0,006, beide nahe 50 %). Diesmal die korrekte Null, kein Barrieren-Artefakt mehr — und trotzdem kein Unterschied zum Placebo. Bestätigt #113 nochmal, jetzt mit sauberer Methodik: **VAH/VAL selbst tragen nichts, unabhängig vom Formations-Zeitpunkt.**

### Test 2 (POC-Rückkehr nach Bounce): sah vielversprechend aus, war aber Fund Nummer vier
14 von 15 Varianten zeigten reale POC-Rückkehr-Rate klar über der Placebo(Mittelpunkt)-Rate, Gap wachsend von +0,03 (früher Formations-Zeitpunkt) bis +0,21 (später) — sah aus wie ein echter, wachsender "Reife-Effekt". Eigener Gegen-Check (POC im Schnitt näher am Bounce-Punkt als der Mittelpunkt?) widerlegte den naheliegendsten Verdacht: POC war im Mittel sogar **weiter** weg (20,2 vs. 19,5 Punkte). Mathematiker und Statistiker haben trotzdem unabhängig den eigentlichen Fehler gefunden:

- **Placebo-Events ≠ reale Events.** `poc_return_real` lief über die Bounces am ECHTEN Level, `poc_return_placebo` über die Bounces am PLACEBO-Level (Level ± 0,25×Value-Area-Breite) — zwei verschiedene Ereignis-Mengen mit unterschiedlichem Startpunkt, nicht derselbe Bounce mit zwei verglichenen Zielen. Der Placebo-Bounce liegt systematisch weiter draußen und hat einen ~1,5× weiteren Weg zu seinem Ziel (Mittelpunkt) als der reale Bounce zu POC.
- **Und dieser Distanz-Unterschied wächst mit der Value-Area-Breite** (die mit späterem Formations-Zeitpunkt zunimmt) — der wachsende Gap kam exakt daher, nicht von einem Reife-Effekt. Statistiker: `corr(Gap, Distanzdifferenz) = 0,96`, `corr(Gap, VA-Breite) = 0,98`.
- **Fairer Test (dieselben Bounce-Events, POC vs. Mittelpunkt als Ziel verglichen), Block-Bootstrap über Handelstage:** Gap schrumpft von +0,209 auf **+0,029** (time_180, CI90 [+0,009; +0,049]) bzw. dreht bei den meisten Varianten ins Negative/Nicht-Signifikante. Der einzige Überlebende (time_180) hält Bonferroni bei ~4 effektiven unabhängigen Tests nur knapp, und dreht laut Mathematiker unter Distanz-Kontrolle (Random-Walk-Reflexionsprinzip als Nullmodell) selbst ins Negative.
- **Zusätzlicher Konstruktionsfehler:** `poc_return_after_bounce` misst "irgendwann berührt", nicht "dreht dort" — eine reine Geometrie-/Exkursions-Größe, kein Magnetismus-Beweis, selbst wenn sie sauber gemessen wäre.

### Gesamtverdikt
**Dritter Grabstein in derselben Reihe (#112/#113/#114).** Test 1 war diesmal methodisch sauber und zeigt konsistent: kein Signal. Test 2 sah vielversprechend aus, war aber ein Placebo-Distanz-Fehler — nach Korrektur bleibt nichts Robustes übrig. Kein Developer-Build, kein Buch-Beitrag. Für alle drei Runden gilt: die AMT-Level selbst (egal ob Vortag, developing, oder frisch eingefroren) tragen auf NQ/ES keine messbare Kante — bestätigt den Research-Scout-Befund vom 17.08. (AMT ist auch akademisch unbelegt) jetzt dreifach mit eigenen Daten.

**Falls Max die Frage trotzdem zu Ende bringen will** (Statistiker-Vorschlag, aufsteigender Aufwand): (a) Placebo immer auf DENSELBEN Events mit distanz-gematchtem Ziel (im Kern schon gerechnet: Ergebnis Null), (b) Outcome von "berührt" auf "dreht dort" umstellen (echte Reversal-Definition, keine Durchlauf-Verzerrung), (c) POC-Nähe als stetigen Regressor statt Ja/Nein-Test. Ohne konkreten Anlass nicht von selbst weitermachen — drei unabhängige Bestätigungen (2 Runden, je 2 Agents) zeigen bereits übereinstimmend Null.

### Lehre
108. **Ein Placebo/Kontroll-Level muss auf DENSELBEN Ereignissen laufen wie der echte Test, nicht auf einer eigenen, durch den Placebo-Level erzeugten Ereignis-Menge.** Sobald der Placebo-Level selbst die Startpunkte verschiebt (hier: weiter draußen, wegen des Offsets vom echten Level), ändert sich die gemessene Distanz zum Ziel mit — und der ganze "Gap" kann allein aus der Distanz-Differenz kommen, nicht aus einem echten Level-Effekt. Sauberer Aufbau: EIN Satz Ereignisse, mehrere Ziele/Level vergleichen, nie mehrere Ereignis-Mengen gegeneinander.
109. **"Preis berührt Ziel X irgendwann binnen Fenster W" ist eine Distanz-/Exkursions-Größe, kein Beweis für Anziehung.** Diese Metrik ist unter einem driftfreien Random Walk vollständig durch die Distanzverteilung zum Ziel bestimmt (Reflexionsprinzip). Ein Level "gewinnt" diesen Test automatisch, wenn es im Schnitt näher liegt oder eine güns­tigere (rechtsschiefe) Distanzverteilung hat — unabhängig davon, ob es irgendeine besondere Marktbedeutung hat. Für einen echten Magnetismus-Test braucht es entweder eine Random-Walk-Null zur Normierung oder eine "dreht dort um"-Definition statt "berührt".

## #115 — Adaptive Value-Area-Segmentierung (Profil je Balance, Reset am Breakout): sauberste Runde der Serie, und trotzdem Friedhof (17.08.2026)

- **Auftrag Max (mit Chart-Vorlagen):** vor jedem Strategie-Test erst die Frage klären, WIE man eine Value Area überhaupt richtig zeichnet. Sein Einwand an #112-#114: ein Profil, das über einen Breakout hinweg weiterläuft, **vermischt zwei verschiedene Balances**. Richtig wäre ein Profil je Balance — Start am NY-Open, Profil wächst mit, ab einem Formations-Kriterium sind VAH/POC/VAL gültig, ein Breakout schneidet ab und startet ein neues Profil am Breakout-Punkt. Nachtrag Max: Delta und Volumen als Breakout-/Reversal-Kriterien mittesten, und "wie viel Volumen HORIZONTAL braucht es für eine valide Value Area".
- **Werkzeug:** `developer/amt_segments.py` (NQ RTH ab 2018, 2191 Tage), 17 Formations- × 10 Breakout-Kriterien, 47 ausgewertete Varianten in zwei Stufen. Formation: Zeit, Volumen-Anteil am 20d-Schnitt, VA-Breite, Stabilität der Grenzen, **horizontale Volumen-Konzentration im POC-Bin** (Max' Nachtrag, zwei Varianten). Breakout: Distanz als Anteil der VA-Breite × Akzeptanz-Bars × **Volumen-Bestätigung** × **echtes Aggressor-Delta**. Dazu `amt_momentum_control.py` (momentum-gematchte Baseline + erweiterter Grid).

### Was diesmal methodisch richtig war
Die Segmentierung selbst funktioniert: 1-4 Balances je Session, Segmente 19-385 Bars, entspricht Max' Charts. Beim Bauen ein eigener Fund: die erste Breakout-Definition (feste Tick-Distanz) zerhackte die Session in ~20 Mini-Segmente, weil eine frisch geformte VA noch schmal ist — Umstellung auf **Akzeptanz** (Distanz relativ zur VA-Breite, mehrere Bars außerhalb) hat das behoben. Die POC-Kernmetrik war diesmal von Anfang an sauber (Spiegelpunkt in gleicher Distanz auf denselben Events, Lehre 108).

### Befunde
- **POC-Magnetismus: null.** −0,019 bis +0,009 über alle 47 Varianten, mit methodisch einwandfreier Null. Endgültig erledigt.
- **Delta trägt nichts** (Max' Frage direkt beantwortet): POC-Erreichungsrate nach Terzil des Anlauf-Deltas ist flach bis auf 1 Prozentpunkt (0,48/0,48/0,49). Delta als Breakout-Bestätigung macht die Ergebnisse leicht **schlechter**. Volumen-Terzile: kein monotones Muster. Horizontale Volumen-Konzentration (`pocfrac`/`pocabs`): ebenfalls nichts.
- **Der Fade (Kauf VAL / Verkauf VAH, die klassische AMT-Rotation) verliert in ALLEN 47 Varianten**, netto −0,59 bis −2,13 Punkte. Das ist der klarste Einzelbefund der ganzen Serie: die Lehrbuch-Rotation ist auf NQ nicht neutral, sondern negativ.
- **Scheinbarer Fund und wie er fiel:** die Gegenrichtung (Continuation an der VA-Kante) war netto positiv in 35/47 Varianten, beste +1,03 Punkte. Meine eigene momentum-gematchte Kontrolle zeigte sogar einen Überschuss von +1,2 bis +1,7 — **sie war aber zu schwach gebaut**: gematcht wurde nur global auf die Momentum-Stärke, nicht innerhalb desselben Tages. Der Statistiker hat die scharfe Version gerechnet (gleicher Tag + gleicher Momentum-Bucket + gleiche Richtung): Kontrolle **+1,33**, VA-Kante **+1,10** → **Differenz −0,23, CI90 [−1,11; +0,67]**. Die Value-Area-Kante ist ein leicht **unterdurchschnittlicher** Momentum-Trigger. 88,6 % der Events haben die 5-Bar-Bewegung ohnehin schon in Handelsrichtung — das Setup ist per Konstruktion ein Momentum-Entry.
- **Multiple Testing:** Tages-Sharpe 0,043 gegen E[max] unter Null von 0,058 bei 47 Trials — der gemessene Wert liegt **unter** der Zufallsdecke. DSR 0,38 (0,29 wenn man die Richtungsumkehr als zweiten Test je Variante zählt).
- **Regime:** 2022 liefert 52 % des Gesamtgewinns. Ohne 2022 t=0,99, OOS 2023-26 t=0,36, 2026 negativ.
- **Die adaptive Segmentierung trägt NEGATIV bei.** Sortiert man nach Segment-Länge: dort wo die Segmentierung wirklich greift (19-38 Bars, 18k-26k Events), ist die Gegenrichtung −0,02 bis −0,51. Die positiven Zahlen kommen ausschließlich aus der `volume=0.3`-Familie, und die selektiert schlicht **spätere Events** (p10 des Event-Zeitpunkts wandert von Minute 27 auf 74/100) — also genau das Nachmittags-Momentum, das über NQ_LastHour längst im Buch ist.
- **Käfig-Sicht (Mathematiker):** als Solo-Bein bei Min-Size P(pass) 0,41 ohne Zeitlimit, praktisch 0 mit; Tages-Schiefe −2,09, Kurtosis 36,7, schlechtester Tag −1179 Punkte, Top-5-Tage 31 % des Gewinns. Selbst bei echter Edge unbrauchbar.

### Gesamtverdikt
**Vierter Grabstein, und der methodisch sauberste — genau deshalb zählt er.** Max' Segmentierungs-Idee war strukturell besser begründet als alles davor und wurde fair getestet; sie verbessert nichts, sie verschlechtert sogar. Damit ist die AMT-Familie auf NQ/ES über vier unabhängige Runden und acht Agent-Gutachten erschöpfend geprüft: **Value Area, POC, Initial Balance und Balance/Trend-Regime tragen keine handelbare Kante, in keiner Anker-Variante, mit keinem Formations-Kriterium, mit und ohne Volumen- und Order-Flow-Bestätigung.** Kein Developer-Build, kein Buch-Beitrag. Ohne grundlegend neue Idee (nicht: neuer Parameter) hier nicht weitermachen.

### Lehre
110. **Ein momentum-gematchter Kontrollarm muss INNERHALB desselben Tages matchen, nicht global über alle Tage.** Meine erste Version matchte nur auf die Momentum-Stärke über den gesamten Datensatz und zeigte einen Überschuss von +1,2 bis +1,7 Punkten; dieselbe Kontrolle mit Tages-Bedingung drehte auf −0,23. Grund: Signal-Events clustern auf bewegten Tagen, und eine global gepoolte Baseline mittelt die ruhigen Tage mit ein — der "Überschuss" ist dann nur die Tages-Komposition. Gilt für jede künftige Kontrollgruppe: erst auf den Tag konditionieren, dann auf die Signalgröße.
111. **Wenn der Trigger eines Level-Setups per Definition mit der jüngsten Preisbewegung korreliert ist, misst der Test Momentum, nicht das Level.** Ein "Touch von innen" an einer Kante heißt zwangsläufig, dass der Preis dorthin gelaufen ist (hier: 88,6 % der Events hatten den 5-Bar-Move schon in Handelsrichtung). Die einzige aussagekräftige Kontrolle ist "gleiche Bewegung, kein Level" — nicht "kein Trade". Vor jedem Level-Test einmal ausrechnen, welcher Anteil der Events das Vorzeichen des Signals schon aus der Trigger-Definition mitbringt.
112. **Wenn ein Parameter-Sweep ausgerechnet dort gewinnt, wo der getestete Mechanismus sich selbst abschaltet, ist das eine Falsifikation, keine Optimierung.** Hier siegten die Varianten mit den längsten Segmenten — Grenzfall 385 Bars = ganze Session = gar keine Segmentierung — während die Varianten mit echter Segmentierung negativ waren. Bei jedem Sweep prüfen, ob der Sieger den Mechanismus überhaupt noch anwendet, bevor man ihn als bestätigten Parameter liest.

## #116 — NQ_ORB-fade komplett durchgesweept (224 ehrliche Varianten): kein Hebel trägt, das Buch-Bein ist eine Regime-Wette (18.08.2026)
Max' Auftrag (Ticket **AP104**): das schwächste Buch-Bein verbessern. Angesagt war ein sehr breiter Sweep — OR-Länge 5/10/15/20/30/45/60, "ruhiger Tag"-Filter über NR-N (2/3/5/10) und Punkt-Schwellen, zwei selbst zu findende Zusatzfilter, Entry am Level vs. Rückkehr in die OR (1m/5m-Bestätigung), Order-Flow-Delta mit und ohne Volumen-Regime, dazu das volle Stop/Target-Gitter. Vier Stufen, Skripte `developer/ap104_sweep_stage{A,B,C,D}.py`, Rohdaten in den gleichnamigen `.json`.

### Ergebnis in einer Zeile
**224 ehrlich gerechnete Varianten, 0 bestehen den Robustheits-Katalog.** Der beste gefundene Tages-Sharpe (2,635) liegt **unter** der Zufallsdecke E[max Sharpe | Null] = 3,26 schon bei nur 30 Trials (bei 224 Trials: 4,41). Wir haben breit gesucht und weniger gefunden, als reiner Zufall bei dieser Suchbreite hergeben würde.

### Die vier Stufen
| Stufe | Was | Varianten | robust |
|---|---|---|---|
| A | OR-Länge × Tagesfilter (NR-N, Range-%, OR-Rel, OR-Rotation) | 50 | 0 |
| B | Entry-Stil (Level / Bar-Close / Rückkehr in die OR, 1m+5m) | 22 | 0 |
| C | Order-Flow-Delta × Volumen-Regime | 92 | **komplett verworfen, siehe unten** |
| D | Stop/Target-Vollgitter (9 × 8) + Zeit-Cap | 152 | 0 |

Scheiter-Statistik über die 224 verwertbaren: **90 % scheitern an IS/OOS**, 93 % an der Jahres-Konsistenz, 70 % am Plateau, 32 % am Jackknife. Die Trade-Zahl war nie das Problem (0 % Ausfall).

### Die Prämisse war falsch — und zwar messbar
Der quant-mathematician hat die Grundannahme direkt getestet, statt sie zu parametrisieren. Zielgröße: P(Kurs kehrt nach dem Ausbruch in die OR zurück), Basisrate 0,485 bei n=2644.

| Filter | P(back) aktiv | inaktiv |
|---|---|---|
| **NR7 (der Filter im Buch!)** | **0,455** | 0,491 |
| ATR-Kontraktion | 0,480 | 0,491 |
| kleiner Overnight-Gap | 0,500 | 0,470 |
| Vortages-Range niedrig | 0,490 | 0,480 |

**NR7 zeigt das umgekehrte Vorzeichen**: nach ruhigen Vortagen setzen sich Ausbrüche eher durch, statt zu scheitern. Der Filter, der laut #070 den kompletten Fade-Edge trägt, arbeitet gegen seine eigene Begründung. Vola-Persistenz existiert zwar (AR(1) auf ln Range = 0,78, Halbwertszeit 2,75 Tage), sagt aber nichts über Ausbruchs-Fehlschlag: corr(Vortages-Kompression, ln(Tagesrange/OR)) = |0,01-0,04|.

Die beiden vom Mathematiker vorgeschlagenen Ersatzfilter messen den **Ausbruchstag selbst** statt den Vortag (Auktionslogik: Balance vs. Initiative) und zeigen wenigstens das richtige Vorzeichen — `or_rel` = OR-Größe / ATR20 der Tagesrange (0,507 vs 0,464) und `or_rotation` = Vorzeichenwechsel von (Close − OR-Mitte) innerhalb der OR (0,506 vs 0,468). Beide je ~1,5σ, im Sweep dann ohne Bestand.

### 🚨 Eigener Look-ahead-Bug gebaut und gefunden (Stage C, alle 92 Zeilen verworfen)
Der neue Delta-Filter `orb_delta_min` mass das Fenster **nach** der Ausbruchs-Bar — der Fill passiert aber **in** dieser Bar. Der Filter kannte beim Entry-Entscheid also 5-30 Minuten Zukunft, was fast das gesamte Trade-Fenster ist. Zwei Diagnosen, beide eindeutig:
- **Monotonie:** expR steigt mit der Fenstergröße von +0,22R (win=5) auf **+1,66R** (win=30). Je mehr Zukunft, desto "besser".
- **Gegenprobe (Lehre #070-3):** Filter in Trade-Richtung PF 2,4-3,2 vs. invertiert PF ~0,10 bei 3 % Trefferquote — eine **fast perfekte Spiegelung**. Eine echte schwache Kante erzeugt so etwas nie.

**75 von 92 Varianten hätten formal "robust" bestanden.** Ohne die Pflicht-Gegenprobe wäre das als Fund durchgegangen. Fix in `qbt.py` eingebaut: das Fenster endet jetzt an der letzten beim Fill nachweislich abgeschlossenen Bar (`i0` bei `close`-Entry, sonst `i0-1`), dazu die dimensionslose Variante `orb_delta_ratio` (Delta / Fenstervolumen), weil das NQ-Volumen über 10 Jahre stark gewachsen ist. Nach dem Fix schwankt der Filter um Null (+0,08 / −0,08 / −0,02 / −0,04 über die Fenstergrößen) — kein Signal, aber ehrlich.

### AP75 bestätigt und schlimmer als gedacht (Stage D)
Der bekannte Fake-Target-Hit-Bug bei Fade+Target: von 126 Target-Zeilen haben **16 eine Fake-Hit-Quote über 50 %**. Die drei besten Target-Kandidaten hingen praktisch vollständig daran:

| Variante | roh | Fake-Hits | bereinigt |
|---|---|---|---|
| stop 0,3 / target 0,5 | +0,068R | 69 % | **−0,30R** |
| stop 0,4 / target 0,25 | +0,060R | 88 % | **−0,34R** (n 422 → 81) |
| stop 0,6 / target 0,25 | +0,055R | 64 % | **−0,12R** |

Ohne das Ticket-Wissen wären das drei "Gewinner" gewesen, die live sofort Geld verbrannt hätten.

### Was der Exit-Hebel strukturell sagt
**Kein Target schlägt "kein Target".** Mittleres expR über das ganze Stop-Gitter: bei `target_mult=None` +0,004R (book) bzw. +0,046R (return), bei **jedem** gesetzten Target von 0,25R bis 3,0R durchgehend negativ (−0,08 bis −0,17R book, −0,02 bis −0,05R return). Sehr enge Stops (0,1 × OR) sind auf beiden Basen die schlechteste Zone. Der aktuelle Buch-Aufbau ist damit bereits das Optimum seiner Familie — in dieser Dimension ist nichts zu holen.

### Der beste Kandidat und warum er trotzdem fällt
`or_min=10, exec=return (win 10 / bar 5), stop_frac=0.6, kein Target`: n=1640, expR +0,075R, PF 1,11, IS +0,080 / OOS +0,062 (OOS besteht!), 8/11 Jahre positiv, max_year_share 0,26, Plateau intakt. Scheitert einzig am **Top-1%-Jackknife: Retain 0,25** — die profitabelsten ~16 von 1640 Trades tragen 75 % der Kante. Genau dasselbe Muster wie in #070 (Top-10 = 127 % des Netto) und beim NQ_Momentum-Delta-Trigger.

### Literatur (research-scout, Cache-Block 18.08.2026)
Gezielte Ergänzungssuche nach 2023-2026-Arbeiten, weil Grant/Wolf/Yu 2005 ein Sample bis 2002 hat. Ergebnis: **kein Ersatz gefunden.** Einzige neuere positive Quelle ist Ladia (SSRN 7124578, 2026) — Opening-Range-Reversal auf **DJIA**, 2023-2026 +0,196R, aber vor 2023 unter Break-even, Single-Author-Preprint, und die 0DTE-Kausalgeschichte passt zu DJI schlecht (0DTE-Volumen sitzt auf SPX/QQQ). Die einzige nennenswerte NQ/MNQ-Forschungslinie 2024-26 (Mesfin-Serie, arXiv 2605.04004 + 2605.11423 + 2605.17724) findet weder bei Breakout-Fortsetzung noch bei Fade/Liquidity-Grab noch per LSTM/Gradient-Boosting etwas, das Kosten übersteht (OOS-Accuracy ~50 %, Permutations-p 0,14/0,52). VWAP-Distanz als Reversion-Anker: weiterhin keine akademische Primärquelle.

### Gesamtverdikt
**Vier unabhängige Wege — altes Logbuch (#070), Prämissen-Messung, 224-Varianten-Sweep, Literatur — landen beim selben Ergebnis.** NQ_ORB-fade hat keine robuste Kante; die positive Buch-Zahl (+0,063R) wird komplett von einem Filter getragen, dessen Wirkrichtung falsifiziert ist, und stammt inhaltlich aus dem Fenster 2024-26. Ohne NR7 ist `or_min=15` bei **−0,074R**. Kein Developer-v2, keine Parameter-Übernahme. Die offene Frage ist nicht mehr "wie verbessern", sondern **"raus aus dem Buch, ersetzen oder als Regime-Wette bewusst behalten"** — das ist die nie final entschiedene Frage aus `buch-entscheidung-070`, jetzt mit deutlich besserer Datenlage. Entscheidung liegt bei Max.

### Lehren
113. **Die Prämisse einer Strategie gehört direkt gemessen, bevor man sie parametrisiert.** Der komplette Stage-A-Sweep (50 Varianten) hätte entfallen können: eine einzige Zeile — P(Rückkehr in die OR | NR7 aktiv) vs. inaktiv — zeigt in Sekunden, dass der Filter das falsche Vorzeichen hat. Ab jetzt vor jedem Filter-Sweep die Trefferquoten-Tafel des unterstellten Mechanismus rechnen, nicht den Parameterraum absuchen.
114. **Ein Filterfenster, das nach dem Fill liegt, ist Look-ahead — auch wenn die Formel aus einem etablierten, korrekten Modul stammt.** `or_delta.py` misst dasselbe Delta völlig sauber, weil dort der Entry NACH dem Fenster liegt. Übernommen in den ORB-Zweig mit Fill IM Fenster wird aus derselben Formel ein Phantom mit +1,66R. Beim Kopieren einer Signalformel immer die Zeitachse mitprüfen: *wann steht der Wert fest, wann wird gefüllt?*
115. **Zwei Selbsttests entlarven Look-ahead schneller als jeder Robustheits-Katalog: Monotonie und Spiegelung.** Wenn die Kennzahl mit der Fenstergröße monoton wächst, misst man Zukunft. Wenn die invertierte Gegenprobe fast exakt spiegelverkehrt herauskommt (PF 3,0 vs. 0,10), war die Auswahl bereits die Antwort. Der Katalog hätte hier 75 von 92 Varianten durchgewunken.
116. **Wenn der beste Fund unter der Zufallsdecke liegt, ist die Suche beendet — nicht der Suchraum zu klein.** Max' Instinkt "such breiter" ist bei einer echten, versteckten Kante richtig; bei E[max Sharpe|Null] = 3,26 gegen einen besten Fund von 2,64 heißt breiteres Suchen nur, dass man irgendwann eine Variante findet, die die Zufallsdecke *scheinbar* überspringt. Ab jetzt gehört die Zufallsdecke VOR den Sweep, als Abbruchkriterium.

## #117 — Die Funded-Phase zum ersten Mal durchgerechnet: die Sizing-Frage ist beantwortet, aber die eigentliche Frage ist eine andere (18.08.2026)
Auslöser: Max' Einwand gegen die v2-Zielfunktion — *"irgendwann haben wir 90 % Passquote, aber erst in 10 Jahren. Bei 150 Tagen bis zum Pass kommt der erste Payout erst in einem Jahr, das ist viel zu lange."* Daraus wurde die erste vollständige Rechnung über die Kette **Eval → funded → Auszahlung**. Skripte: `ap104_leave_one_out.py`, `ap105_vwap_forensik.py`, `ap106_funded_sizing.py` + `_lib.py`, `ap106_funded_leg_metrics.py`.

### 🚨 Die Kopfzahl: das Konto ist unter ehrlicher Drift nicht sicher positiv
| Tages-Drift µ | E[Gesamtauszahlung] | Median | P(Bust vor 1. Payout) | **Wert je $150-Kauf** |
|---|---|---|---|---|
| $27,34 (In-Sample) | $6.384 | $9.006 | 22,4 % | **+$325** |
| $20,5 (×0,75) | $5.069 | $5.248 | 34,3 % | +$97 |
| **$17 (×0,62)** | ~$4.100 | $0 | 43 % | **≈ 0 (Break-even)** |
| $13,7 (×0,50) | $3.250 | $0 | 50,5 % | −$76 |
| $0 (Nulldrift-Kontrolle) | $475 | $0 | 79,5 % | −$280 |

**Break-even liegt bei µ ≈ $17/Tag = 62 % des In-Sample-Werts. Der ehrlich geschrumpfte Punktschätzer liegt bei $7–12/Tag.** Bei n_trials ≥ 1000 (über die `*results*.json` sind ~4000 Konfigurationen dokumentiert, das ist nicht diskutabel) bleibt nach Haircut µ_rest $8,7; bei 4000 Trials $6,6. Die Nulldrift-Kontrolle besteht sauber (E[ges] −93 %, P(alle 5) 63 % → 1,1 %) — das Modell ist nicht kaputt, die Zahl ist echt.

### Die Regime-Zerlegung ist die eigentliche Nachricht
| Fenster | µ/Tag | Wert je Kauf |
|---|---|---|
| 2016–2021 | $6,59 [−2,4; 14,9] | **−$138** |
| 2021–2026 | $48,09 | +$1.107 |
| letzte 3 Jahre | $37,90 [19,0; 57,6] | +$527 |

Die jüngere Periode ist **nicht** schwächer — die ältere ist tot (2016–20: $2,69/Tag, 2020 negativ). Das ist also kein Recency-Problem, sondern eine **Wette auf die Persistenz des Post-2021-Regimes**. Und der entscheidende Satz des Statistikers dazu: *genau dieses Regime hat die Beine hervorgebracht — Shrinkage und Regime sind hier dieselbe Unsicherheit, nicht zwei.*

### Sizing: die Frage ist beantwortet, die Antwort ist "nichts ändern"
Die Auszahlungen sind in **Dollar** gedeckelt (50k: 1250/1250/2250/2250/3250, max $10.250, danach endet der Konto-Zyklus). Eine größere Position holt dieselben Caps **schneller, nicht mehr** — kein Kelly-Wachstumsproblem, sondern ein Wettlauf Zeitgewinn gegen Ruin.

| k je Bein | E[ges] | Median | P(Bust<P1) | E[Payouts] | P(alle 5) |
|---|---|---|---|---|---|
| **1** | **$6.367** | **$9.027** | **22 %** | 3,45 | 63 % |
| 2 | $4.185 | $685 | 49 % | 2,12 | 39 % |
| 3 | $2.952 | **$0** | 64 % | 1,49 | 28 % |
| 40 (Cap) | $272 | $0 | 97 % | 0,14 | 3 % |

Barwert fällt **streng monoton in k**, kein Knick, Rand-Optimum. **Kelly-Gegenprobe:** κ = σ²/µ = 247,49²/27,34 = **$2.241 Polster je Kontrakt und Bein**. Zu Beginn der Funded-Phase ist das Polster genau der DD-Betrag → 50k = 0,89 κ, 25k = 0,45 κ. **Ein Kontrakt je Bein ist auf 50k bereits 1,1× Voll-Kelly, auf 25k 2,2×.** Es gibt keine zulässige Größe darunter. Cushion-proportionales Sizing wurde mitgetestet (κ 1200–6000, kmax 2/4/8) und ist exakt gleich k=1: das Polster wird wegen Buffer + Caps nie groß genug.
**Auszahlungspolitik** (kleiner Hebel, gratis): abrufen sobald verfügbarer Gewinn ≥ 0,5 × Cap (50k: $781), dann vollen Cap nehmen, nichts extra stehen lassen — +3,5 % gegen naiv-sofort. Mehr Polster halten ist messbar schlechter.
**Tier: 50k**, klar — $6.367 gegen $2.297 beim 25k, also 2,8× Ertrag für $50 mehr Gebühr bei halber Bust-Rate.

### E8-Regeln erstmals primärquellenbestätigt (Support-Chat 18.08., zwei Runden)
- **Kein Profit-Target** in der Performance-Phase (die 6 % gelten nur für die Challenge)
- **Maximal 5 Auszahlungen pro Konto**, Caps steigend (25k: 1000/1000/1250/1250/1500 = max $6.000 · 50k: 1250/1250/2250/2250/3250 = max $10.250). Danach endet der Zyklus, es gibt eine Gratis-Challenge derselben Größe. **Ein funded Konto ist ein endliches Gut, kein Einkommensstrom.**
- **Keine 14-Tage-Mindestfrist** (entgegen allen Sekundärquellen), **die 5-Tage-Regel gilt nicht für die erste Auszahlung**, erster Payout praktisch nach ~3 Handelstagen
- **Buffer bestätigt**: $1.000/$2.000 dauerhaft im Konto, nicht auszahlbar
- Split 80 %, steigt nicht; Mindestauszahlung $100 (= $125 anrechenbarer Gewinn)
- **GEKLÄRT am selben Tag (dritte Support-Runde, 18.08. 12:25):** der Floor **rastet ein** — Variante (a), die gute. E8 wörtlich: *"the Loss Level cannot trail above $50,000. Once it reaches the initial balance, it locks there permanently."* E8 korrigiert dabei mein Rechenbeispiel selbst: ab $52.000 EOD-Balance steht der Loss Level fix auf $50.000 und bleibt dort — auch bei $53.000 ist er **nicht** $51.000. Damit gilt die gute Zahl: **E[Gesamtauszahlung] $6.367 statt $1.317**, und eine Auszahlung ist kein Risiko-Ereignis. Die Buffer-Vermutung hat sich bestätigt (der Buffer ergibt nur bei einrastendem Floor Sinn).
- **Zwei Details aus derselben Antwort, die das Modell schärfen:** (1) Der **Buffer liegt oben drauf**, nicht innerhalb — auszahlbar ist erst, was über *Startbilanz + Buffer* liegt; für den vollen ersten 50k-Cap von $1.250 braucht es $53.250 Balance. (2) Die **Caps sind Brutto-Abrufbeträge**, ausgezahlt werden davon 80 % (E8s eigenes Beispiel: $125 anrechenbarer Gewinn → $100 erhalten). Maximal erhalten: **50k ~$8.200, 25k ~$4.800**. Der Mathematiker hatte beide Lesarten gerechnet (netto $946 / brutto $827 diskontiert) — es gilt die Brutto-Lesart.

### Der VWAP-"Widerspruch" war kein Fehler, sondern ein Zielkonflikt
Am 16.08. kam NQ_VWAP-Pullback mit Score +2,00pp ins Buch, der Leave-one-out vom 18.08. zeigte −4,65pp. Forensik (`ap105_vwap_forensik.py`) schließt alle technischen Ursachen aus: Zellen bitgleich (max |Δ| = 0,0 über alle 6 Beine), Developer-v8 identisch zum Buch-Bein (1139/1139 Tage), Cache gültig, beide Seed-Sätze liefern −4,55/−4,65pp. **Die Erklärung liefert die Funded-Messung:** VWAP-Pullback ist das *beste* Funded-Bein (glatteste Kurve, Top-5-Tage nur 20 %, 56,4 % grüne Tage) und deshalb das *schlechteste* Eval-Bein. Beide Messungen waren korrekt, sie messen Verschiedenes.

### 🚨 Zwei eigene Fehlschlüsse, die im selben Lauf gefallen sind
1. **"25k ist dreimal schneller als 50k" war falsch.** Das war der *bedingte* Median (Tage bis Pass, gegeben dass bestanden wird) — zwischen Tiers unvergleichbar, weil die Zensierung völlig verschieden ist (25k: 49,4 % bestehen nie, 150k: 13 %). Zensierungsfrei ist **E[Tage je funded] = E[Tage/Versuch] / P(pass)**: 25k **1134 d**, 50k **512 d**, 100k 564 d, 150k 724 d. **50k ist mehr als doppelt so schnell, nicht langsamer.** Und die 87 % beim 150k sind ein **Horizont-Artefakt** (hm=24 → 67,3 %, hm=36 → 86,8 %, hm=60 → 91,8 %).
2. **Die Korrelation Eval↔Funded (r = −0,40) ist Rauschen.** CI90 [−0,78; +0,19], Permutations-p 0,26; ohne den Ausreißer NOISE_ORB r = −0,21, p = 0,59. Bei n=10 ist alles unter |r| = 0,55 nicht von Null trennbar; für |r| = 0,4 bräuchte es n ≈ 46 Beine. **Eine Zwei-Bücher-Strategie darauf zu stützen wäre Fitting an einen Ausreißer** — ich hatte sie eine Stunde vorher als "Hypothese bestätigt" präsentiert.

### Nebenbefunde
- **Buch-Sharpe ist 1,48 annualisiert, nicht 1,84** — die 1,84 rechnen mit 252 Tagen statt der echten apy = 178.
- **τ² ≈ 0 über die 10 Kandidaten-Beine** (Var_obs 0,00375 < E[Var_noise] 0,00450): die Beine sind untereinander statistisch ununterscheidbar. **Bein-Selektion innerhalb dieses Pools ist Rauschen** — das trifft rückwirkend auch die LOO-Deltas aus AP104.
- Die LOO-Basis-sd von 0,2–1,0pp misst nur MC-Rauschen und **unterschätzt die echte Unsicherheit um Faktor 7–10** (Outer-Block-Bootstrap: 5,1pp auf 25k, 7,2pp auf 50k). Gepaart überleben nur zwei Deltas (ohne LastHour +6,1, ohne VWAP +5,2, beide nur auf 25k); **ORB-fade ist mit +0,6 [−3,1; +4,1] nicht von Null trennbar.**
- Die 25k-LOO-Deltas summieren sich auf +18,5pp, sind also stark nicht-additiv — sie messen "weniger Kontrakte gegen $1.000 Trailing-DD" (Lehre 82), nicht Bein-Qualität. Das erklärt den Vorzeichenwechsel auf 100k/150k.
- **64-Teilmengen-Suche gestrichen, weil gemessen:** IS-Sieger schlägt das Buch um +23,6pp, verliert −35,0pp ins Out-of-Bag und landet dort **12,4pp unter dem Buch**; 13 verschiedene Sieger in 25 Wiederholungen, PBO-Anteil 1,00.
- **Bug gefunden:** `eval_marginal` mischt LOO- und Add-one-Vorzeichen (ohne Korrektur kommt r = −0,14 statt −0,40).

### Gesamtverdikt
Die Sizing-Frage ist sauber beantwortet und die Antwort lautet **nichts ändern** — Min-Size ist in allen vier Kombinationen (2 Tiers × 2 Floor-Varianten) und über alle Drift-Szenarien optimal. Aber sie war nie die entscheidende Frage. **Die entscheidende Frage ist, ob das Post-2021-Regime hält**: bei In-Sample-Drift ist ein Kauf +$325 wert, im 2016-21-Regime −$138. Kein Sizing-Hebel und keine Bein-Auswahl ändert daran etwas — der Wert je Kauf fällt in k in *jedem* Szenario, und die Beine sind untereinander ununterscheidbar.

### Lehren
117. **Ein bedingter Median ist zwischen zwei Optionen mit unterschiedlicher Ausfallquote wertlos.** "50 % bestehen in 49 Tagen" und "87 % bestehen in 539 Tagen" lassen sich nicht vergleichen, weil die erste Zahl die 49,4 % Nie-Besteher wegdefiniert. Die vergleichbare Größe ist **E[Zeit je Erfolg] = E[Zeit je Versuch] / P(Erfolg)**. Ich habe darauf eine Tier-Empfehlung gestützt, die sich exakt umgekehrt hat. Ab jetzt bei jeder Zeit-Aussage prüfen, ob sie auf Erfolg konditioniert ist.
118. **Eine Kennzahl, die mit dem Rechenhorizont wächst, ist eine Eigenschaft des Horizonts.** Die 87 % Passquote auf 150k sind bei 24 Monaten 67 %, bei 60 Monaten 92 %. Bei jeder Passquote den Horizont mitnennen — oder eine horizontfreie Größe verwenden.
119. **Bei n ≈ 10 Kandidaten ist eine Korrelation um 0,4 nicht von Null zu trennen, egal wie gut die Geschichte dazu passt.** Ich hatte r = −0,40 als "Hypothese bestätigt" verkauft, weil die kausale Story (Eval belohnt Sprünge, Funded bestraft sie) so überzeugend war. Die Story kann trotzdem stimmen — belegt ist sie damit nicht. Vor jeder Korrelations-Aussage: welches n, und was ist die Trennschärfe bei diesem n?
120. **Wenn die Edge nur in der zweiten Hälfte der Historie existiert und die Beine in genau dieser Hälfte gefunden wurden, sind Shrinkage und Regime-Risiko dieselbe Unsicherheit — nicht zwei getrennte Abschläge.** Man darf sie nicht nacheinander abziehen (doppelt bestraft) und nicht gegeneinander ausspielen ("das Regime hält ja, also brauche ich keinen Shrinkage"). Die ehrlichere Basis ist, den Käfig direkt auf dem jüngeren Pool zu rechnen, statt einen µ-Faktor zu wählen.
121. **Wenn eine Auszahlung gedeckelt ist, ist Positionsgröße kein Wachstumshebel mehr.** Der ganze Kelly-/Sizing-Instinkt setzt voraus, dass mehr Einsatz mehr Ertrag bringen kann. Bei einem Dollar-Cap holt die größere Position denselben Betrag nur schneller und zahlt dafür mit Ruinrisiko — das Optimum liegt zwangsläufig am unteren Rand. Vor jeder Sizing-Optimierung prüfen, ob der Ertrag überhaupt in der Größe skaliert.

## #118 — Discovery-Runner v2: die Suche wird ein Dauerprozess mit Gedächtnis (18.08.2026)
- **Anstoß (Max):** „Die Discovery-Batches haben noch nie was gebracht — wie kann ich dich durchgehend suchen lassen?" Diagnose (siehe [[Discovery-Prozess (wie wir Alpha finden)]]): abgegraster Suchraum, Filter zu grob und das Buch-Kriterium erst am Ende, kein globales Gedächtnis (~20 Einzelskripte). Antwort: **Rechnen macht die Maschine, entscheiden macht Claude** — [[Discovery-Runner v2]].
- **Gebaut (`engine/discovery/`):** Daemon mit Queue, drei Stufen (Prämisse nach Lehre 113 → Grid mit Gates IS/OOS-fix, Top-5 ≤ 60 %, letzte 3 J ≥ 0, Block-Bootstrap P(>0) ≥ 0,85, **Plateau** über Grid-Nachbarn, PBO/DSR/Reality-Check → **Buch-Marginal** über `developer_run.book_contribution`, bei Exit-Sweeps gegen das Original-Bein), Trial-**Register** (Backfill **1390 Alt-Trials** aus 22 Ergebnisdateien → Zufallsdecke E[max SR | Null] ≈ 1,5 bei n≈1460, gerechnet mit theoretischer SR-Streuung 1/√Jahre statt der gemessenen — Exit-Varianten sind korreliert, gemessen wäre eine Scheindecke), Inbox + Morgen-Check (`inbox_tool.py`), job-freier Start per WMI, STOP/Lock/Heartbeat, Box-Provisionierungsskript (nicht ausgeführt, Live-Box). Der Runner schreibt nie ins Buch.
- **Smoke-Test:** 4 Configs, alle Stufen grün. **Nebenbefund:** NQ_Momentum als Bein macht das aktuelle 6er-Buch um **−1,8 pp schlechter** (Basis ohne 77,0 % → mit 75,2 %, Rauschen 0,7) — deckt sich mit AP104 Leave-one-out; gehört in die Next-Week-Entscheidung (Ticket AP109).
- **Erster Nachtlauf:** Exit-Sweep über 5 Buch-Beine (336 Configs; ORB-fade bewusst nicht: fliegt per Next-Week raus, `orb_exec`-Falle). Erster Job (NQ_Momentum, 72 Configs): 19 Survivors, Selektion „ok", Job-Decke 1,1 / global 1,53. Auswertung morgen früh mit Quant-Team + Auditor — Kandidaten aus 8 Buch-Marginal-Picks sind selbst wieder Multiple Testing, „vs Original +2 pp" ist noch kein Beweis.
- **Ehrliche Grenze:** der Runner macht die Suche sauber und billig, aber neue Mechanismen kommen nur mit neuen Inputs (Tick/L2, Optionen-Positionierung, Breadth). Nächste Job-Typen: Regime-Conditioning bestehender Beine, Event-Bein.

## #119 — NOISE_ORB_NQ als Zusatz-Bein verworfen: kein Qualitäts-, sondern ein Größenproblem (20.08.2026)
**Anstoß:** Max fragte im Rahmen von AP104 nach, warum Ticket AP58 NOISE_ORB_NQ noch als Gewinn (+2,0pp, Logbuch #095) führt, während der Tausch-Test vom 18.08. (#116/AP104) −7,5pp (25k) / −11,7pp (50k) zeigt. Berechtigter Widerspruch.

**Auflösung:** Die +2,0pp aus #095 (15.08.) wurden unter dem seit #106 (16.08.) verworfenen Zeit-Score-Kriterium (P(funded) pro Zeit, rollender Nachkauf) gerechnet. Dasselbe #095 zeigt im selben Atemzug, dass sogar ein bestätigt totes Bein (RV_leadlag, PF 0,91) dort +4,6pp brachte, rein weil mehr Handelstage das Konto schneller durchrechnen. Kein Edge-Effekt, ein Artefakt des alten Kriteriums.

**Fehlender Test nachgeholt:** unter der aktuell gültigen v2-Methodik (Min-Size, Intraday-Bust, Block-Bootstrap, 5 Seeds, Skript `ap104b_add_noiseorb.py`) NOISE_ORB als reines **Zusatz-Bein** zum 5-Bein-Next-Week-Buch gerechnet (nicht Tausch, echte Addition):

| Tier | Basis (5 Beine) | +NOISE_ORB (6 Beine) | Delta |
|---|---|---|---|
| 25k | 59,7 % | 47,9 % | **−11,8pp** |
| 50k (gekauft) | 85,8 % | 70,4 % | **−15,4pp** |
| 100k | 90,1 % | 84,0 % | −6,0pp |
| 150k | 86,0 % | 93,0 % | +6,9pp |

**Quant-Team-Gegenprobe (beide bestätigen, kein Rechenfehler):**
- **Statistiker:** selbst wenn die reale Streuung wie in #117 um Faktor 7-10 größer ist als die 5-Seed-sd (0,58-0,69pp hier), bleibt das Delta auf 25k/50k einseitig bei p ≈ 0,02-0,013 von Null trennbar. Drei unabhängige Stützen: Replikation über den Tausch-Test (gleiches Vorzeichen, gleiche Größenordnung), ein geordneter Dosis-Gradient über die vier Käfig-Größen, und mechanistische Kohärenz (Median-Dauer halbiert sich, APY steigt, Passquote fällt — exakt das RV_leadlag-Muster aus #095, jetzt korrekt bestraft statt belohnt).
- **Mathematiker:** First-Passage-Formel (Taylor 1975, P ∝ exp(−T·θ/(exp(θD)−1)), θ = 2µ/σ²) reproduziert alle vier Tiers mit einem einzigen Parameter (rmse 0,8pp). θ fällt um 29 %, weil NOISE_ORB bei Min-Size (1 Kontrakt durchgehend) **~52 % der gesamten Buch-Varianz** trägt — „ein Bein mehr" ist hier faktisch „Buch-Größe verdoppeln". Der 150k-Umschlag ins Positive ist ein reiner **Uhr-Effekt** (Zeitlimit bindet dort: Basis-Median 633 Tage, das Bein halbiert die Dauer und gewinnt so 10,3pp zurück), der zugrunde liegende Risiko-Effekt bleibt auch bei 150k negativ (−3,4pp). Eigene diskrete MC-Gegenrechnung bestätigt Vorzeichen und Größenordnung.

**Verdikt:** NOISE_ORB_NQ ist keine schlechte Strategie (Solo weiterhin sauber: expR +0,094, IS=OOS, 9/11 Jahre positiv), aber bei 1-Kontrakt-Sizing für die gekauften Käfige (25k/50k) **zu groß** — Größen-, kein Qualitätsproblem. Weder Tausch noch Zusatz-Aufnahme verbessert das Buch an den relevanten Tiers.

**Entscheidung Max:** NOISE_ORB_NQ bleibt draußen (weder Tausch für ORB-fade noch Zusatz-Bein), solange 25k/50k die Betriebs-Tiers sind. Next-Week-Buch bleibt bei 5 Beinen. **Ticket AP58 geschlossen** (Grundlage war die überholte #095-Zahl).

**Offene Idee, kein Ticket:** die Formel sagt, dass θ bei halbierter Bein-Größe (MNQ statt NQ, oder Teil-Size/engerer Stop) wieder steigen könnte — NOISE_ORB wäre dann evtl. doch aufnehmbar. Nicht verfolgt, nur vermerkt, falls Max das später prüfen will.

### Lehre
122. **Ein Bein mit sauberer Solo-Kante kann das Buch trotzdem schädigen, wenn es bei Min-Size einen unverhältnismäßig großen Anteil der Buch-Varianz trägt.** Das ist kein Qualitäts-, sondern ein Größenproblem gegen den fixen Dollar-Trailing-DD (θ = 2µ/σ² fällt, wenn σ² überproportional wächst). Vor jeder „Bein dazu"-Entscheidung am Min-Size-Betriebspunkt den Varianz-Anteil des Kandidaten am Gesamtbuch schätzen, nicht nur seine Solo-Kennzahlen.

## #120 — Baseline-Diskrepanz cage_v2 geklärt: 73,79 %/203$ ist die aktuell gültige 50k-Zahl, nicht 59 % (#106) oder 75,5 % (18.08.) (20.08.2026)

**Anstoß:** offenes Ticket seit AP102 (18.08.): `cage_v2_weights.py` zeigte 75,55 % / 199$ (50k, volle Historie), Logbuch #106 dokumentiert 59,44 % / 255$ — beide sollen denselben Käfig auf demselben Buch messen. Vor der nächsten Käfig-/Bein-Entscheidung (hier: AP69 Portfolio-Gewichtung) musste geklärt werden, welche Zahl gilt.

**Auflösung, per backtest-runner frisch nachgerechnet — zwei getrennte Ursachen, kein Config- oder Cache-Bug:**
1. **59,44 % (16.08., #106) → 75,55 % (18.08. Nachmittag):** komplett durch die Engine-Fixes AP74/75 (qbt.py, Slippage-Split + Fake-Target-Hit-Fix) erklärt, gleiches 6-Bein-Buch.
2. **75,55 % (18.08. Nachmittag) → 73,79 % (heute):** `book_state.json` bekam erst um 23:20 Uhr am 18.08. das 7. Bein `NQ_Momentum_d260818` dazu — Stunden NACH dem `cage_v2_weights.py`-Lauf (17:24–17:27 Uhr). Die 75,55 %-Zahl galt also nur für ein kurzlebiges 6-Bein-Zwischenstadium, nicht für das aktuelle Buch. Das 7. Bein drückt die v2-Passquote real (kein Rauschen, Delta > 2×sd) um ~1,8pp / +5$ pro funded.

**Aktuell gültige Baseline (50k, 7 Beine, fixe Engine, Stand 20.08., 5 Seeds):** **73,79 % ± 0,73 sd Pass, 203$/funded.** Diese Zahl gilt ab jetzt als Referenz, bis sich Buch oder Engine wieder ändern.

**Nebenbefund für AP69:** ob `NQ_Momentum_d260818` die richtige Ergänzung war, wurde nie explizit gegen das 6-Bein-Buch marginal getestet (`cage_v2_weights_results.json` enthält es in keiner Zeile) — offener Punkt für die laufende Gewichtungs-Analyse.

### Lehre
123. **Ein Skript-Ergebnis ist nur so aktuell wie der `book_state.json`-Stand zum Zeitpunkt des Laufs — bei parallelen Änderungen am selben Tag (hier: Engine-Fix UND neues Bein binnen Stunden) reicht ein Blick auf "wurde heute gelaufen" nicht, sondern nur ein Abgleich der `legs`-Liste im Ergebnis-JSON gegen den aktuellen `book_state.json`-Stand.

## #121 — AP69 beantwortet: Gewichtung gibt es unter Min-Size nicht, dafür ein LIVE-Buch-Bug gefunden (NQ_Momentum-Duplikat) (20.08.2026)

**Auftrag:** AP69, Befund #074: die Tages-Sharpes der Beine unterscheiden sich stark, das Buch läuft aber stillschweigend gleichgewichtet (alle 1 Kontrakt) — sollten Beine mit besserem Sharpe stärker gewichtet werden (w ∝ Σ⁻¹μ)? Quant-Team (Mathematiker + Statistiker) parallel gerechnet, danach `strategy-auditor` gegengelesen.

### Kernbefund: die Prämisse war falsch, strukturell begründet

Unter dem aktuellen Min-Size-Betriebspunkt (#106: frac so klein, dass effektiv 1 Kontrakt = die gehandelte Einheit) ist die First-Passage-Formel `P(pass) ∝ f(θ)`, `θ = 2·w'μ/(w'Σw)` **skalendegeneriert**: der Fixpunkt von `w ∝ Σ⁻¹μ` will die Gesamtgröße gegen null schicken, nicht auf einen endlichen optimalen Wert. Praktisch heißt das: **jedes Gewicht über 1x macht das Buch schlechter**, egal wie die Verteilung aussieht (2x LastHour: −11,0pp; 2x LastHour+VWAP: −17,5pp). Der Statistiker bestätigt das empirisch von der anderen Seite: kein paarweiser Bein-Sharpe-Unterschied ist signifikant (CIs überlappen fast komplett), die Bein-Rangfolge dreht sich zwischen erster und zweiter Hälfte der Historie fast komplett um (Spearman −0,75), und ein aus einer Hälfte gefitteter Gewichtsvektor crasht out-of-sample (71,8 %→39,3 %). Eine Σ⁻¹μ-Gewichtung ist auf dieser Datenlage nicht robust umsetzbar.

**Der einzig wirksame Hebel im Min-Size-Regime ist binär (Bein-Selektion, keine Gewichtung):** vollständiger MC-Scan über alle 127 Teilmengen des 7-Bein-Buchs zeigt `NQ_Momentum` in 0 von 20 Top-Kandidaten, `NQ_Momentum_d260818` in 18 von 20.

### 🚨 Nebenfund, wichtiger als die eigentliche Frage: LIVE-Buch-Bug

`NQ_Momentum` und `NQ_Momentum_d260818` korrelieren mit r=0,64 bei identischen 798 Handelstagen — kein Zufall: Params-Diff zeigt **identischen Mechanismus** (`ts_reversal`/`momentum`), nur der Exit-Raum unterscheidet sich (`rev_stop_mult` 0,4→0,3). Im Discovery-Register ist der Job explizit als `"replaces_leg": "NQ_Momentum"` markiert — als 1:1-Ersatz gedacht, keine Ergänzung. `book_state_next.json` hat den Tausch am 17.08. korrekt vollzogen (nur `d260818` drin). **`book_state.json` (LIVE) enthält aber BEIDE Beine gleichzeitig**, mtime exakt 4 Minuten nach dem Next-Buch-Promote-Event (18.08. 23:20) — Runner-Bug oder eine Session hat versehentlich ins Live- statt Next-Buch geschrieben. Das Buch handelt seit mindestens 2 Tagen mit echtem Geld die doppelte Exposure auf denselben Momentum-Mechanismus.

**Einzel-Drop-Test (Momentum raus, Rest bei 1x, E8 50k, volle Historie, 5 Seeds):** 73,79 %→81,08 % (+7,3pp, sd 0,53 — klar über dem Rauschband), $203→$185/funded, Inaktivitäts-Lücken unverändert bei 4. **Regime-Split-Gegenprobe (Auditor):** H1 (<2021) neutral −0,36pp (Rauschen), H2 (≥2021) klar positiv +8,23pp — **kein Vorzeichenwechsel**, anders als bei OR_DELTA_BIAS (#079) oder NOISE_ORB (#119). Kausal plausibel: deckt sich mit AP101 (Momentum-Crowding/Decay, 28 % Drift-Rückgang bei +42 % Vola in der jüngeren Hälfte).

**Ticket angelegt** (`live-momentum-duplikat`, rot, sofort): `NQ_Momentum` aus `book_state.json` entfernen, `funded_finalize.py`/`live_finalize.py` nachziehen, NT8-Strategie-Instanz deaktivieren — braucht Max' O.K. vor dem Deploy, da echtes Geld betroffen.

### Gesamtverdikt
AP69 als Gewichtungs-Ticket ist **negativ beantwortet und geschlossen**: keine Sharpe-Gewichtung umsetzen, alle Beine bleiben bei 1x. Der eigentliche Hebel war die Bein-Selektion, und die eigentliche Aktion ist ein Bugfix am Live-Buch, kein neues Next-Week-Experiment.

### Lehre
124. **"Bein-Gewichtung erhöhen" und "Bein-Selektion" sind unter Min-Size zwei verschiedene Fragen mit entgegengesetzter Antwort.** Gewichte >1x schaden strukturell (Skalendegeneration der First-Passage-Zielfunktion), während 0/1-Auswahl der einzige echte Hebel ist. Eine „Gewichtungs"-Anfrage sollte deshalb zuerst prüfen, ob der Betriebspunkt Min-Size ist — dann ist die Antwort fast immer „nicht hochgewichten, sondern selektieren".
125. **Ein Parent/Child-Ersatz im Next-Week-Buch ist erst abgeschlossen, wenn auch das Live-Buch nachgezogen hat.** `book_state_next.json` korrekt zu haben reicht nicht als Beleg, dass `book_state.json` denselben Stand hat — ein Abgleich beider Dateien gehört zur Routine-Prüfung vor jeder Buch-Entscheidung, nicht nur bei explizitem Verdacht.

## #122 — Max' Tempo-These durchgerechnet: Geld-über-Zeit ist die richtige Zielfunktion, aber Size ist der falsche Hebel (20.08.2026)

**Auftrag (Max):** Die Passquoten-Optimierung dauert zu lange (gefühlt „89 % in 180 Tagen", dann nochmal Monate bis zum ersten Payout). These: größere Size → schneller passen → früher funded → Payouts 50 % reinvestieren (bis 5 parallel) → summiert sich trotz niedrigerer Passquote zu mehr Geld. Quant-Team parallel: Mathematiker (Renewal-Reward-Modell der kompletten Pipeline Eval→Funded→Payout→Reinvest) + Statistiker (Unsicherheit, Shrinkage, Lotterie-Test). Voller Rechenstand: `engine\_scratch_money_model\` und `engine\_scratch_money_stats\`.

### Kernbefunde

1. **„89 %/180 Tage" existiert als Paar nicht** — 89,7 % ist der 100k-Tier (Median dort 419 Tage), ~186 Tage ist der 50k-Tier (Passquote dort 85–86 %). Beides 36-Monats-Horizonte; auf 12 Monate hat 50k nur **76 %**, Outer-Bootstrap-CI90 [64; 94] (Seed-Rauschen ±0,2 pp ist irrelevant dagegen).
2. **Die Geld-Zielfunktion ist sauber** (anders als der beerdigte Zeit-Score #106): bei Edge 0 und −0,02R ist jede Tempo-Variante in allen 64 getesteten Zellen strikt negativer und monoton schlechter in k. Geld-EV darf als Zielfunktion verwendet werden.
3. **Max' Zeitgefühl stimmt:** erster Euro auf 50k im Median nach ~14 Monaten (k=1), ~7,6 (k=2), ~5,5 (k=3). Der Tempo-Gewinn ist real — Faktor 2–2,5 auf „erstes Geld".
4. **Aber der EV-Vorsprung von Tempo ist kurzlebig und tail-getragen:** k=2 führt auf 50k im Mittel nur bei 6–12M; Crossover bei ~18–24M, bei 60M liegt Min-Size +50 % vorn (32,6k vs. 21,8k $). Im **Median** gewinnt Min-Size ab Monat 12 durchgehend (24M: +4.250 $ vs. −350 $). P(im Minus @24M): 30 % vs. 53 % vs. 71 % (k=1/2/3). Der frühe Mittelwertvorsprung ist die Nachkauf-Lotterie in schwächerer Form.
5. **Mechanik dahinter (Kassen-Effekt, kein Zeit-Effekt):** Geld-Multiple je gekaufter Eval fällt 35× (k=1) → 16× (k=2) → 9× (k=3); je eingesetztem Dollar gewinnt Min-Size in **jedem** Szenario. Der Reinvest-Motor — Herz der These — läuft in den ersten 12 Monaten praktisch nicht an (Reinvest 0 % vs. 100 % ändert <0,1 %); bindend sind Slots und früher Cashflow, nicht die Size.
6. **Kipppunkt und Unentscheidbarkeit:** Tempo (k=2 auf 50k) lohnt ab wahrer Drift µ* ≈ 19–20 $/Handelstag. In-Sample sind es 25,8, ehrlich geschrumpft (n_trials=1730, James-Stein λ=0,736 bzw. DSR) **9–19**. µ* liegt mitten im Unsicherheitsintervall; Auflösung bräuchte ~33 Jahre Vorwärtsdaten. Minimax spricht für Min-Size (Verlustseite von Tempo größer und wahrscheinlicher).
7. **Semi-analytisch (Mathematiker):** Renewal-Reward-Rate je Slot mit Tempo-Optimum **k\* = max(1, round(1,7·DD·µ/σ²))** (~1,7× Voll-Kelly aufs Startpolster, weil Payouts gedeckelt sind; trifft 10/12 gemessene Rate-Maxima). Mit geschrumpfter Drift auf 50k: k\* = 1. Die Rate-Kurve ist am Optimum flach (±12 %), der Rand (k≥3) klar schlecht.
8. **Die echten Tempo-Hebel, die nichts kosten:** (a) **Start-Staffelung** der Evals um ~2 Monate statt gleichzeitig: P(≥1 von 5 besteht) 75,9 → 83,2 % — gleichzeitige Evals auf demselben Buch sind perfekt korreliert, Parallelität ist keine Diversifikation; (b) **Kaufrate/Budget in den ersten Monaten erhöhen** (300→600 $/M hebt 12M-EV um ~50–80 %); (c) **Käfiggröße statt Size**: 100k@k=2 / 150k@k=2–3 schlagen 50k@k=1 im Mittel um 20–60 % — steht und fällt aber mit den **unbestätigten** 100k/150k-Payout-Caps (extrapoliert als 2×/3× der 50k-Caps; erst schriftlich bei E8 bestätigen lassen, Ticket angelegt).
9. Funded-Annahmen (Konsistenz-Regel, Gewinntage, Payout-Politik) verschieben nur das Niveau, nie die k-Rangfolge — einzige Ausnahme Floor-Lock (ist primärquellenbestätigt, 18.08.). Die Betriebspunkt-Entscheidung hängt allein an µ.

### Verdikt
**Betriebspunkt bleibt Min-Size auf 50k** (#106 bestätigt, jetzt auch unter der Geld-über-Zeit-Brille). Tempo nicht über Kontraktzahl kaufen — das ist eine Wette auf µ>19 mit P≈0,15–0,5 und dickem linken Tail. Stattdessen: Start-Staffelung einführen, frühe Kaufrate prüfen, E8-Caps für 100k/150k schriftlich klären und dann die Käfig-Frage (nicht die Size-Frage) neu aufmachen. Optionaler Engine-Patch (v3-Geldrate + k\*-Kontext neben v2, nie als Ersatz) liegt als Vorschlag im Mathematiker-Report.

### Lehre
126. **„Schneller reich durch mehr Size" scheitert nicht an der Passquote, sondern an der Kasse:** das Geld-Multiple je Eval fällt schneller als die Zykluszeit — der Reinvest-Motor, der die These tragen soll, wird durch Size ausgehungert. Tempo-Hebel, die bei Edge 0 nicht bestraft werden (Staffelung, frühe Kaufrate, Käfigwahl), immer zuerst ausschöpfen.
127. **Mittelwert-Vorsprünge auf kurzen Horizonten immer gegen den Median stellen:** der 12M-EV-Vorteil von k=2 war tail-getragen (Median negativ) — dieselbe Selbstbetrugs-Stelle wie beim Zeit-Score (#106), nur subtiler.

## #123 — E8 vs. FundedNext: volle Pipeline-Simulation, Regelwerk-Arbitrage-Runde (21.08.2026)

**Auftrag:** Nach der Firmen-Recherche vom 20.08. (9 Support-Mails, [[Research-Cache]]) bleiben zwei für unser Setup taugliche Firmen: E8 (bisherige, dreirundig bestätigt) und FundedNext Flex (neu, eine ausführliche Support-Mail). Max: "rechne E8 vs FundedNext mit den 50k-Zahlen durch" → Quant-Team parallel (Mathematiker: volle Eval→Funded→Payout→Reinvest-Pipeline + Kombi-Szenario; Statistiker: Beweislage/Unsicherheit). Basis beider Rechnungen: aktuelles Live-Buch (6 Beine, Min-Size), `eval_plan.evaluate_v2`-Mechanik, ehrliche Zahlen aus [[Strategie-Logbuch]] #122 wiederverwendet.

### Eval-Seite: FundedNext-Vorteil ist statistisch robust, aber winzig
FN ist bei $/funded 33-45% günstiger als E8 (100% von 200 gepaarten Block-Bootstrap-Resamples, drift-invariant 0-38$/Tag, vola-invariant 0,5-3x, regime-invariant in 5/5 Fenstern — Statistiker). **Aber:** der Vorteil ist $75-91 je funded Konto, während die Payout-Decke $2.200 (netto) auseinanderliegt — 1:24 im Verhältnis. Die Eval-Seite darf die Firmenwahl nicht tragen.

### Payout-Seite: E8 gewinnt langfristig, FN gewinnt kurzfristig
Volle Pipeline (5 Slots, Min-Size, 50% Reinvest, IS-Drift 27,79$/Tag): **12M-Median E8 −750$ vs. FN +2.400$** (FN 4x schneller zum ersten Geld). **Crossover im Mittel ~65 Monate, im Median zwischen 24-60 Monaten** — danach zieht E8 klar vorn (60M-Median 34.317$ vs. 30.065$, 120M-Median 77.694$ vs. 66.685$). Kapitaleffizienz (Geld je Eval-Dollar) gehört E8 in jedem Szenario (50,0 vs. 12,7 bei IS-Drift) — E8s Gratis-Reset nach 5 Payouts ist strukturell mehr wert als FNs halber Preis.

**Warum FN langfristig verliert — nicht die Caps, sondern die "Überlebensleiter":** FN erlaubt nur 50% des akkumulierten Profits auszuzahlen (Rest bleibt Polster), E8s Floor rastet komplett bei der Startbilanz ein (fixes Polster $2.000). Das macht E8s Weg zum 2.-5. Payout deutlich robuster (Survival-Wahrscheinlichkeit je Zyklus s≈0,87-0,93 bei E8 vs. ≈0,66-0,76 bei FN) — nicht die Cap-Höhe ist bindend, sondern ob man überhaupt bis dahin überlebt.

### Nulldrift-Kontrolle: ein Warnsignal bei FundedNext
E8 sauber bestraft bei Edge 0 (m60 −578$, Hausvorteil-Ratio p·R_f/Preis = 0,53 — plausibles Geschäftsmodell). **FN liegt bei Edge 0 im Mittel nur bei −15$, Ratio 1,03** — mathematisch heißt das: ein Könner mit Edge NULL würde im Mittel Geld von FundedNext bekommen. Das ist entweder ein Fehler in der (single-source) FN-Regelauslegung, oder ein Produkt, das so nicht überlebensfähig wäre. **Folge: bei FN nie über den Mittelwert urteilen, nur über den Median** (der bleibt bei −880$ sauber negativ).

### Kombi-Szenario: kein Diversifikationsgewinn, aber ein Slot-Hebel
Mathematisch bewiesen: bei getrennten Kassen ist E[Geld] exakt linear in der Firmen-Mischung (0,08% Krümmung = Rauschen) — **Diversifikation über Firmen bringt am Mittelwert nichts**. Was sie bringt: (1) die gemeinsame Kasse profitiert leicht von den billigen FN-Käufen als Cashflow-Beschleuniger (E1F4/E2F3 optimal, +1.300$ auf 60M, −7pp P(Verlust)); (2) das 5-Konten-Limit gilt **je Firma** — beide zusammen verdoppeln die Slot-Decke, was bei IS-Drift alles verdoppelt, aber bei unsicherer Drift (µ=19) den Median kippt (245$ → −830$) — dieselbe Falle wie Size-Skalierung in #122 (Lehre 127).

### Der eine ungeklärte Punkt, der alles kippen kann
FN-Support sagt "Max-Loss ist EOD-basiert, nicht intraday". Wenn wörtlich gemeint (kein Intraday-Check überhaupt), schlägt FN E8 auf **allen** Horizonten (Rate 172 vs. 158 $/Monat/Slot). Wenn wie bei E8 gemeint (Floor rastet EOD ein, aber laufende Positionsverluste zählen kontinuierlich gegen den Floor), bleibt die Basis-Rechnung gültig (E8 langfristig vorn). Der Nulldrift-Test stützt die vorsichtige Lesart (wörtlich wäre EV-Ratio 1,67 — kein Anbieter würde das verkaufen).

### Verdikt
- **Eine Firma, lange gedacht → E8.** Höhere Rate je Slot bei jeder Drift, 4x bessere Kapitaleffizienz, sauberer Nulldrift-Test, dreifach gegengeprüftes Regelwerk.
- **Eine Firma, kurzer Horizont/schneller Cashflow → FundedNext.**
- **Empfehlung Quant-Team:** E8 als Basis behalten, 1-2 FN-Slots als Tempo-/Cashflow-Beschleuniger UND als billiger Regelverifikations-Test (80$ Einsatz) dazu — nicht 5 FN-Slots und nicht 10 Slots gleichzeitig, solange die Drift zwischen 9-28$/Tag unentschieden ist und die EOD/Intraday-Frage offen ist.
- **Vor jedem größeren FN-Einsatz:** die EOD/Intraday-Frage schriftlich klären (konkretes Rechenbeispiel wie beim E8-Cap-Widerspruch #073-090), Payout-Buffer erfragen, Praktiker-/Trustpilot-Recherche zu FN nachholen (im Vault noch komplett offen).

### Lehre
128. **Bei einem Firmenvergleich ist die Eval-Seite (Passquote/$-pro-funded) nur die Vorrunde — die Payout-Struktur (Split, Cap-Leiter, vor allem die "Überlebensleiter" zwischen den Auszahlungen) entscheidet das Rennen, meist mit 10-25x größerem Hebel.** Nicht am Eval-Vergleich stehenbleiben, wenn eine neue Firma auf den Prüfstand kommt.
129. **Der Nulldrift-Test ist auch ein Plausibilitätsfilter für Firmenregeln:** ergibt eine Regelauslegung bei Edge 0 einen positiven Erwartungswert für den Trader (EV-Ratio p·R_f/Preis > 1), ist entweder die Regel falsch gelesen oder das Produkt nicht so gemeint — beides ein Signal, genauer nachzufragen statt zu rechnen.

## #124 — HF-Serie Runde 2: leicht verdorrt, zwei „neue" Mechanismus-Ideen waren schon Grabsteine (21.08.2026)

**Kontext:** Runde 1 der HF-Discovery (#122, 20.08.) fand nur beim NQ-Momentum ein echtes Frequenz-Signal. Am 21.08. lief eine zweite Runde (9 Jobs: `hf_combo_Mom_d260818`, `hf_volbrk_NQ`, `hf_orb_scalp_close_NQ`, `hf_gap_fade_ES/YM`, `hf_lasthour_thr_NQ`, `hf_asian_thr_NQ`, `hf_revfade_RTY/YM`) plus ein `hf_combo_Mom_d260818`-Job, der niedrige Schwelle **mit** dem next-week Exit-Profil (d260818) kombiniert.

**Ergebnis: fast alles tot.** Kombo-Job 0 Kandidaten (schlägt selbst mit besserem Exit nicht die aktuelle Next-Week-Baseline, Selektion „dünn"). Vol-Breakout, LastHour-Schwelle, Asian-Schwelle: Selektion „kaputt" (PBO 46-47% im Zufallsband — reines Rauschen gewählt). ORB-Scalp, Gap-Fade ES/YM, Reversal-Fade RTY/YM: alle an der Prämisse gescheitert (Edge klar negativ), billig gestorben wie geplant.

**Vor Runde 3 kurz gegen den Friedhof geprüft** (`qbt.py`-Modi `pivot`, `vwap_trend`/„continuation"), bevor neue Jobs geschrieben wurden: beide bereits tot — `pivot` in #051 (52 Configs, 47 sterben IS, 2 Survivors = Multiple-Testing-Bodensatz), `vwap_trend`/Zarattini-Cross zweimal Grade F. Keine neuen Jobs daraus gebaut.

**Einordnung:** Nach 2 Runden (14 Jobs) auf den 4 bestehenden Instrumenten (NQ/RTY/ES/YM) und den bekannten Engine-Modi ist der leicht erreichbare Frequenz-Raum ziemlich ausgeschöpft — bestätigt die Grid-zuerst-vs-Mechanismus-zuerst-Lehre (#122): Parameter-Variationen bekannter Mechanismen liefern kaum noch etwas Neues. Queue ist leer, Runner wartet auf neue Job-Ideen.

### Lehre
130. **Vor jedem neuen „frischen" Mechanismus-Job kurz gegen den Friedhof prüfen** (Logbuch-Grep auf Modul-/Modus-Namen), bevor ein Job geschrieben wird — spart Rechenzeit auf Ideen, die schon mit Grab-Stein dastehen (hier: `pivot`, `vwap_trend`).

## #125 — HF-Fundament: Kosten-Stress-Gate gebaut, `volshock` vor dem Bau falsifiziert, VWAP-Re-Arm unnötig (21.08.2026)

**Auftrag (Max):** die drei übergreifenden Lücken der HF-Serie „alle drei testen": (1) Kosten-Stress-Gate, (2) Multi-Entry-Module (Re-Arm im VWAP-Pullback, `volshock`), (3) Wochenend-Ticket `next-week-2026-33` (d260818/d260821, LastHour_v3, ORB-fade, Asia_d260821) — (3) läuft mit Quant-Team + Auditor, Ergebnis in #126.

### (1) Kosten-Stress-Gate — gebaut, scharf
- `discovery_lib.stress_costs(tr, ticks)`: rechnet `r_net` analytisch auf `ticks` Slippage je Seite um (gleiche Ordertyp-Logik wie AP74: Limit-Entry bei ORB book/stop_honest und Target-Exit zahlen keinen Spread), kein zweiter Backtest. Neues Gate `cost_stress_ticks=2.0` in `DEFAULT_GATES`: expR gesamt **und** OOS-expR/OOS-USD müssen bei 2 Ticks positiv bleiben, sonst `fails=["cost2t"]`. Kandidaten-Einträge in der Inbox zeigen die Stress-Zahl mit.
- **Test auf 12 Configs** (`engine/_scratch_volshock/stress_test.txt`): alle 6 Live-Buch-Beine stabil (Momentum 0,293→0,274 @2t, LastHour 0,089→0,075, Asia 0,217→0,198, VWAP 0,064→0,058); volbrk-Survivors stabil (0,142→0,119 @2t, 0,095 @3t); Momentum_hf 0,314→0,286. **Einziger Wackelkandidat: `NQ_Momentum_d260821` aus dem Next-Buch** — expR 0,102 @1t, 0,048 @2t, **−0,005 @3t** (201 tpy, Schwelle 0,15 %). Die Frequenz-Variante kauft Trades mit dünner Edge, und ein Tick mehr Slippage frisst davon die Hälfte. VWAP dist 1,5 (185 tpy) fällt ohnehin an OOS.
- Engine per `-SyncOnly` auf die Box, Runner neu gestartet → alle weiteren Jobs laufen mit dem Gate.

### (2a) VWAP-Pullback Re-Arm — nicht nötig, Register hat die Antwort
- Der Tages-Cap `vwap_max_trades_day` 4/6/8 liefert **identische** Zahlen (greift nie), Re-Entry nach Exit ist im Modul schon drin. Der einzige Frequenz-Hebel ist `vwap_dist_min_atr`, und der verdünnt monoton: 2,5 ATR → 120 tpy / expR 0,064 / SR 1,48; 2,0 → 144 / 0,054; 1,5 → 185 / 0,042 (und 180 tpy-Variante OOS negativ). Exit-Sweep bis 250 tpy bei expR ≈ 0. **Mehr Trades aus diesem Mechanismus = proportional weniger Edge je Trade**, ein Re-Arm-Modul würde dieselbe Kurve abfahren. Bein bleibt bei 120 tpy.

### (2b) `volshock` (Scout-Spec A) — Vorab-Falsifikation, Modul NICHT gebaut
- Raster wie #112-#115 (`engine/_scratch_volshock/falsify.py`, NQ 15- und 30-min-Buckets, 52k/26k Buckets 2016-2026): RVOL = Bucket-Volumen / 20-Tage-Median desselben Buckets (nur Vortage), Move in ATR20, Forward 30/60 min ab Open der Folgebar, signiert mit der Bucket-Richtung, Terzile + Placebo (gleiche |Move|-Klasse, RVOL < 1).
- **Kein Trefferquoten-Shift.** Trefferquote High-RVOL-Terzil liegt **1 bis 3 pp unter** dem Low-Terzil in jeder |Move|-Klasse (15 min: −1,0 bis −2,6 pp; 30 min: −0,8 bis −3,4 pp). Mittelwert-Differenzen < 1 Punkt bei 1,5 Punkt Kostenhürde, t < 1,6. Echte Schocks (RVOL ≥ 2/3, |Move| ≥ 0,10 ATR): Hit 48,8-50,7 % vs Placebo 49,9-51,5 %.
- Einzige positive Zelle: OOS ≥ 2023-09 mit n=396 (15 min) bzw. 153 (30 min), mean +17/+24 Punkte, t 3,2/2,7 — IS davor negativ bzw. null. Das ist der Tail-Effekt aus #112, kein Mechanismus. Nicht bauen; falls der 2023+-Effekt in einem Jahr noch steht, Thema neu öffnen.
- Konsequenz für den HF-Fokus: von den 4 Scout-Modul-Specs ist der einzige Multi-Entry-Kandidat tot. Mehr Trades/Jahr im Buch kommen damit weiterhin nur über **neue Beine**, nicht über mehr Entries eines Beins.

### Lehre
131. **Frequenz-Hebel immer erst im Register ablesen, bevor man ein Modul baut:** beim VWAP-Pullback stand die Antwort (Cap greift nie, Distanz verdünnt monoton) schon in 36 gerechneten Trials.
132. **Kosten-Stress gehört zu jedem HF-Kandidaten als Gate, nicht als Nachfrage:** ein Bein mit 200 tpy und expR 0,10 ist bei 2 Ticks ein halbes Bein und bei 3 Ticks keins mehr — das hätte ohne Gate erst im Live-Vergleich auffallen können.

## #126 — Box rechnete drei Tage gegen das falsche Buch: Kontamination, zwei Runner-Bugs, Wochenend-Ticket neu bewertet (21.08.2026)

**Auslöser:** Quant-Team + `strategy-auditor` über das Wochenend-Ticket `next-week-2026-33` (Teil 3 von #125). Der Auditor fand zuerst, Statistiker und Mathematiker bestätigten unabhängig.

### Kontamination
- **Alle Box-Buch-Marginals vom 18.08. bis 21.08. 21:16 tragen `book_fingerprint 43d7dafe`** = `book_state.json.bak-20260820-fix-momentum-doppel`, das 7-Bein-Buch mit dem Momentum-Duplikat. Zwei Ursachen: (a) der Fix vom 20.08. (Duplikat raus) wurde am PC gemacht, aber **nie auf die Box gepusht** — die Box rechnete mit der alten Kopie weiter; (b) `discovery_lib.load_book()` cachte das Buch im Prozess ohne Reload, selbst ein Push hätte erst beim Neustart gewirkt. Alle vier Auto-Promotionen (d260818, d260820, beide d260821) sind davon betroffen; die Runner-Zahlen (80,85 / 80,33 / 69,98 / 74,03) reproduzieren mit dem 7-Bein-Buch auf die zweite Nachkommastelle.
- **Fix:** `load_book()` prüft jetzt die mtime von `book_state.json` und lädt neu; CLAUDE.md-Regel: jede Änderung an `book_state.json` → sofort `inbox_tool.py --push-next`. Box neu gestartet (21:26 und 21:42), Inbox-Warnung auf der Box geschrieben.

### Zwei Runner-Bugs (Statistiker, Mathematiker unabhängig)
1. **Vergleichslatte „Original-Bein" war `prem_rows[0]`** (erste Prämissen-Config des Jobs), nicht das Buch-Bein. Bei Generator-Jobs ist das die Vorlagen-Basis (Momentum: n=2110 vs Buch-Bein n=798, Tages-PnL-Korrelation 0,26). „vs Original +10,2 pp" bei d260821 hieß wörtlich: *einem Buch, das schon Momentum hat, ein zweites hinzuzufügen schadet mit d260821 um 10 pp weniger als mit der Vorlagen-Basis*. Fix: Latte = echtes Bein aus `book_state.json` (eigener Backtest, `orig_book.source`).
2. **Ersatz-Kandidat brauchte nur `vs_original == besser`**, das absolute Buch-Urteil wurde ignoriert — so wurde „Buch neutral −0,5 pp" promotet. Fix: Kandidat nur bei absolut „besser" **und** vs Original „besser"; `promote_next.py` gleichgezogen (vorher reichte „neutral").

### Nachrechnung gegen das echte 6-Bein-Buch (PC, 50k, Basis 75,41 %)
| Kandidat | Buch-Marginal | vs Original | Statistiker (12 gepaarte Seeds) |
|---|---|---|---|
| NQ_Momentum Original | **−1,9 pp** (Buch ohne Momentum 77,3 > mit 75,4) | Anker | — |
| Momentum_d260818 (stop 0,3 + BE 0,5) | besser +3,6 pp → 80,85 | +5,5 | +5,0 [+4,8; +5,3], DSR 0,44, kostenstabil bis 3 Ticks |
| Momentum_d260821 (201 tpy) | neutral +1,4 pp | +3,3 | +2,9, aber SR 0,75 < Decke 1,08, DSR 0,07, geschrumpft negativ |
| Asia-Dir Original | neutral +1,6 pp | Anker | — |
| Asia_d260820 (thr 0,8 + Target 2R) | besser +3,4 pp | +1,8 (knapp) | — |
| Asia_d260821 (thr 0,725 + Target 2R) | besser +2,5 pp | **+0,9 = neutral** | +0,3 [−0,1; +0,6], White-RC p 0,13 |
| volbrk als 7. Bein | **−14,2 pp** | — | Lehre 82 |

### Verdikte (alle drei Agents einig)
1. **LastHour_v3: übernehmen** (+1,9/+2,0 pp, 7/7 Seed-Paare positiv, κ 7,0→8,4). Filter selbst nicht bewiesen (n=129, p_FWER ≈ 1), aber billig. **Voraussetzung AP113:** FOMC-Liste in `news_calendar.py` endet 17.06.2026, live würde der Filter ab sofort nichts mehr ausschließen; `MaxLastHourNQ.cs` auf Kalender prüfen.
2. **ORB-fade raus: übernehmen** (Quote +0,3 bis +0,6 pp, DSR 0,008, top5 = 207 % des Nettos). Einzige Änderung ohne methodischen Vorbehalt.
3. **Momentum_d260821: verwerfen.** Kauft Frequenz mit dünner Kante (Jahres-Drift 711 $ vs 1277 Original vs 952 d260818; κ 6,3 vs 7,0), Kosten-Cliff aus #125; im Buch 80,9 % @1 Tick → 79,3 @2 → 77,5 @3, **ab 2 Ticks unter dem Buch ohne Momentum (80,5 %)**. d260818 bleibt bei 84,3/83,7/83,2. → **d260818 zurück ins Next-Buch.** Offen: nested-OOS-Marginaltest + Shrinkage (12er-Sweep), Why muss BE als Vola-Regler führen.
4. **Asia_d260821: verwerfen.** Schwellensenkung 0,8→0,725 ist der schädliche Teil (κ 6,1→4,5), Target 2R der gute (Mittel +6 %, sd −15 %, Exit-Mix 32 % Target; nach dem Impuls ist die Rest-Drift bis EOD ~0, Stoppen bei 2R ist gratis). → **d260820 zurück ins Next-Buch, beobachten.**

**Mathematiker-Modell:** log P ≈ −T/D_eff + T·κ mit κ = μ/σ² — bei Min-Size ist der Geometrie-Term praktisch konstant (D_eff 1864-1904), das Buch ist am 50k **κ-limitiert**, nicht pfad-limitiert. Spearman(Drift-Term, MC) 0,87 über 25 Buchvarianten. **BE-Overlay ist ein reiner Varianz-Transfer:** auf den Entries Gewinner −39,4k $, Verlierer +39,8k $, sd 129→95, κ 2,8→5,4; #046 hat expR gemessen (und BE kappt Gewinner), v2 misst κ — kein Widerspruch, aber das Why muss es so sagen. BE und Stop 0,3 sind additiv (2×2: 78,6 / 81,7 / 83,1 / 84,3 %).

**Empfohlenes Buch:** d260818 + LastHour_v3 + RTY_Gap + Asia_d260820 + VWAP, ohne ORB = **85,8 % / $175 / Median 190 d** (Live 75,7 % / $198; Next-Buch wie es heute steht 80,9 % / $185). Nebenbefund für AP107: Buch am 50k überbesetzt (LOO ohne VWAP 88,9 %, ohne LastHour 87,6 %, bestes 3-Bein-Buch 90,0 % bei Median 372 d) — v2-Eigenschaft, nicht hier entscheiden.

**Rauschmaß-Bug (AP112):** `book_contribution()` bildet `hypot(sd_base, sd_plus)` über unabhängige Seeds, der gemeinsame MC-Anteil fällt nicht heraus → Rauschen 3-5× überschätzt. Auf gepaarte Seed-Differenzen umstellen.

### Next-Buch umgebaut (23.08. 15:50, Max' Auftrag)
`book_state_next.json` = Momentum_d260818 + LastHour_v3 + RTY_Gap-fade + Asia_d260820 + VWAP-Pullback (ORB raus), `funded_finalize --next` + `live_finalize --next`, `--push-next`. **Ergebnis 50k: 85,9 % / $175 / Median 188 d** (Live 75,4 % / $199 / 144 d); 25k 59,6 % / $168 (Live 50,7 % / $197); 100k 90,1 %; 150k 86,1 % (−1,1 pp, einziger Tier mit Minus). Rollend: P(funded) 12M 74,3 % (Live 66,8 %), aber 3M 13,1 % (Live 21,1 %) und Median 174 statt 126 Tage — das Buch ist **besser, aber langsamer** (weniger Trades, BE kappt Pfade). Alle 5 Beine bestehen alle Gates inkl. Kosten-Stress (RTY_Gap top5 0,64 wie gehabt). Höchste Paar-Korrelation LastHour_v3 ↔ VWAP 0,40, Rest < 0,12. Jahres-PnL (1 Micro je Bein): 2016-20 dünn (2020 −422 $), 2021-22 Ausreißer (7,5k / 16,9k), 2023-26 stabil ~5k. Schlechtester Tag −886 $ (12.03.2020), kein Tag unter −1000 $.
**Falle erlebt:** 16 Minuten nach dem Edit hat `auto_check.py --pull` den Box-Stand (d260821) über die PC-Datei gespiegelt — `live_finalize --next` lief damit falsch. Regel bleibt hart: Next-Buch-Edit → **sofort** `--push-next`, vor jedem Finalize.

### Lehren
133. **Buch-Fingerprint gehört in jede Entscheidung:** ein Buch-Marginal ohne Abgleich des `book_fingerprint` gegen das aktuelle `book_state.json` ist keine Zahl. Drei Tage, vier Promotionen, niemand hat hingeschaut.
134. **Die Vergleichslatte ist Teil des Tests:** „vs Original" gegen eine Job-Prämisse statt gegen das Buch-Bein macht aus einem schlechteren Kandidaten einen Sieger. Latte immer aus derselben Quelle wie das Buch.
135. **Ersatz braucht zwei Ja:** absolut besser als ohne das Bein **und** besser als mit dem alten Bein. Ein „neutral" im ersten Test ist ein Nein, egal wie groß das zweite Delta ist.

## #127 — Hypothesen-Apparat: ein Weg statt zwanzig Skripte, Fallen als Vorbedingung (23.08.2026)

**Auftrag Max:** alle Hypothesen der Momentum-Bank auf der Box testen, je Hypothese mindestens zehn Implementierungen (Volumen / Delta / EMA12 / EMA20 / Stop / Exit), tagelang, PC darf aus sein — und alles, was uns bisher umgebracht hat, soll als Vorbedingung mitlaufen, damit ein Fund direkt einbaubar ist.

### Gebaut
- **`sigcore.py`** — gemeinsame Signal-/Ausführungsschicht: Bars und Zeitrahmen als DURCHGEHENDE Serie, Averages (sma/ema/wma/hull/dema/tema/median/trimmed), RVOL gegen den Uhrzeit-Median der Vortage, Delta-Proxy aus OHLCV, Tageskontext (ATR/Sigma/Gap/Overnight/Panik — alles um einen Tag verschoben), ehrliche Trade-Simulation, ALLE Gates an einer Stelle.
- **`tsmom.py`** (`mode="tsmom"`) — verallgemeinertes TSM: Fenster frei, Signaltyp ret/zscore/rank/rangepos/signratio/accel/jerk/wins, Basis open/prev_close/prev_rth/overnight, Schwelle in % oder σ. **Reproduziert `ts_reversal` exakt** (798 Trades, expR 0,293, 100 % gleiche Tage) — die Verallgemeinerung bringt kein neues Backtest-Gerüst mit.
- **`maband.py`** (`mode="maband"`) — Averages, Crossover, Geschwindigkeiten, Bollinger/Keltner/Donchian, Anker-VWAP. Teilt sich Ausführung und Gates mit tsmom, damit ein Vergleich der Familien ein Vergleich der SIGNALE ist.
- **`discovery/controls.py`** — die Lehren als automatische Batterie je Kandidat: Look-ahead-Delay (#066/#067), Long-Bias (#108), Nulldrift mit gewürfelter Richtung, Multi-Markt (#051), Epochen-Split 2016-19 vs. 2022-26 (#057), Zufallslevel bei Level-Strategien, Buch-Korrelation ≤ 0,70 (#079). Ergebnis ist ein `deploy_ready`-Verdikt; `promote_next.py` promotet nur noch das automatisch.
- **`discovery/hypothesis_bank.py`** — Hypothese → Job. Erzwingt per `assert`: Why vorhanden, **≥ 10 Implementierungen**, ≤ 400 Configs. Gates härter als der Hausdefault (top5 ≤ 0,50 statt 0,60, Bootstrap-P ≥ 0,90 statt 0,85).

### Auf der Box
126 Jobs, 5.400 Configs, im Schnitt 44 Implementierungen je Hypothese. Priorität 95 zuerst: die Kontrollen, die über ganze Blöcke entscheiden (TS-01/AK-01 Filter-Äquivalenz, TV-01 Buy-and-Hold-Latte, TK-01 Long-Bias, AB-12/AW-14 Zufallslevel, AR-04/AR-14 Gate-Kontrollen).

### Zwei Funde noch vor dem ersten Job
1. **Bollinger-Break gegen Zufallslevel gleicher Distanz: expR +0,007 gegen +0,007.** Das Level trägt nichts, die Distanz alles. AB-12 hat damit schon vor dem Sweep geliefert.
2. **`qbt.run_strategy` fiel bei unbekanntem `mode` still auf die Default-Strategie zurück.** Der Box-Runner lief seit dem Morgen und hatte `qbt` importiert, bevor tsmom/maband im Dispatch standen — die ersten maband-Jobs rechneten deshalb `continuation` und meldeten 142.742 statt 2.460 Trades. Betroffene Jobs zurückgesetzt, 17 Register-Einträge entfernt, Runner neu gestartet. **`KNOWN_MODES` wirft jetzt einen harten Fehler.**

### Lehren
136. **Ein stiller Fallback ist schlimmer als ein Absturz.** Ein unbekannter Modus, ein Tippfehler, ein veralteter Prozess — alles landete im `else`-Zweig und rechnete eine fremde Strategie, die brav ins Register wanderte. Jeder Dispatch braucht eine Whitelist mit hartem Fehler.
137. **Ein laufender Prozess kennt neuen Code nicht.** Modul-Dateien auf die Box zu kopieren reicht nicht, wenn der Daemon das betroffene Modul schon importiert hat. Nach jeder Engine-Änderung: Runner neu starten, nicht nur syncen.
138. **Die Warmup-Phase gehört zur Ehrlichkeit.** Ein EMA(20) auf 5m-Bars, je Session neu gestartet, ist bis 11:10 undefiniert — die erste Version lieferte 0 Trades statt eines Signals. Averages laufen über die durchgehende Serie, nicht pro Tag.

## #128 — Buch KW34 ins Live-Buch übernommen, NT8-Deploy vorbereitet: der News-Filter lässt sich live nicht 1:1 nachbauen (23.08.2026)

**Auftrag Max:** Next-Week-Buch ins aktuelle Buch übernehmen und bereit machen, es am selben Abend live zu deployen.

**Abweichung von der Regel, bewusst:** das Next-Week-Buch war erst seit 15:50 desselben Tages im Staging, die vorgesehene Sim-Woche (Ticket `next-week-2026-33`) entfällt damit. Max' Entscheidung, hier festgehalten, damit die Herkunft später nachvollziehbar bleibt. Die Zahlen selbst sind aus #126 gegengelesen (Quant-Team + Auditor), nur die Beobachtungszeit fehlt.

### Übernommen
- `book_state.json` = **Momentum_d260818 + LastHour_v3 + RTY_Gap-fade + Asia_d260820 + VWAP-Pullback**, ORB-fade raus. Fingerprint `ca73aecf`, 5 Beine, Plan-Block unverändert. Backups beider Bücher unter `book_state*.json.bak-20260823-1759-promote`.
- `funded_finalize.py` + `live_finalize.py` frisch gerechnet: **50k 85,9 % Passquote / $175 pro funded / Median 188 d** (25k 59,6 % / $168, 100k 90,1 % / $288, 150k 86,1 % / $453). Buch 338 Trades/Jahr, PF 1,38, Sharpe 1,83, |corr| 0,09. Live-Buch 8 Beine (5 Buch + 3 Bank), 371/yr, PF 1,40, Sharpe 1,95.
- Next-Buch auf den neuen Stand zurückgesetzt (`changes: []`, `base_fingerprint ca73aecf`), PC und Box verifiziert synchron.

### Der eigentliche Befund: der Makro-Filter ist live ein anderer Filter
`NQ_LastHour_v3` handelt an FOMC/NFP/CPI-Tagen nicht. Im Backtest kommen diese Tage aus `news_calendar.build_calendar`, und das leitet **NFP und CPI aus dem 08:30-Volumenspike der Kursdaten ab** — ein Proxy, der den Tag erst im Nachhinein kennt. Live muss der Tag vor dem Handel feststehen, also ist der Proxy dort grundsätzlich nicht nachbaubar.
- Gemessen, wie regelmäßig der Proxy überhaupt ist: **NFP trifft nur in 101 von 127 Fällen den ersten Freitag** (25× den zweiten, 1× einen anderen Tag); CPI verteilt sich über die Monatstage 8–16 und alle fünf Wochentage. Eine einfache Kalenderregel bildet ihn also nicht ab.
- Konsequenz für NT8: hartkodierte Liste der **echten** Fed-/BLS-Termine (FOMC aus `news_calendar.py`, NFP + CPI aus dem Research-Cache-Eintrag von heute, AP113). Beide Mengen zielen auf dieselben ~29 Tage/Jahr, decken sich aber nicht tagesgenau — der Proxy wählte z.B. den 10.08.2026 als CPI-Tag, der echte Release war der 12.08.
- **Das ist eine Abweichung zwischen Backtest und Live, keine Übersetzung.** Der Filter trägt im Buch-Marginal +1,9 bis +2,0 pp und ist laut Statistiker ohnehin nicht bewiesen (n=129, p_FWER ≈ 1), nur billig. Deshalb bewusst in Kauf genommen und im Code dokumentiert, statt eine Deckungsgleichheit zu behaupten, die es nicht gibt.
- **Wiedervorlage:** die Liste endet am 10.12.2026, für 2027 hat BLS noch keinen Kalender. Läuft sie ab, handelt die Strategie wie ohne Filter weiter und schreibt täglich eine Warnung ins NT8-Log — bewusst so herum, weil blindes Aussetzen der teurere Fehler wäre.

### Für den Deploy gebaut (drei NinjaScript-Änderungen, Pre-Flight sauber)
- **`MaxMomentumNQ.cs`**: Stop 0.4 → 0.30 und neues Break-Even-Overlay (`BeTriggerR = 0.5`, Offset 0), 1:1-Port von `qbt._trail_stop`. Das günstige Extrem wird nur aus abgeschlossenen Bars gebildet, der nachgezogene Stop wirkt frühestens ab der Folge-Bar — dieselbe Look-ahead-Freiheit wie im Backtest.
- **`MaxPowerHourNQ.cs`**: `ExcludeNewsDays` mit dem Kalender oben.
- **`MaxAsiaDirNQ.cs`**: `TargetRMult = 2.0`, also Target = 2 × Stopabstand = 1,0 × Asien-Range. Bekannter Restunterschied: trifft eine Bar Stop und Target, zählt der Backtest konservativ den Stop, live entscheidet die Marktreihenfolge.
- Pre-Flight-Compile des kompletten Zielzustands (8 Dateien) auf der Box: **COMPILE OK**. Staging enthält genau diese drei Dateien; die sechs Leichen vom 20.08. lagen noch drin, waren byte-identisch zum installierten Stand und liegen jetzt im Archiv.

### Zwei Fallen, wieder dieselbe Familie
1. **`auto_check.py` hat den Next-Buch-Reset erneut überschrieben** (gleiche Falle wie heute Mittag, Daily Note): der PC-Spiegel zog den alten Box-Stand zurück, während `funded_finalize` lief. `inbox_tool.py --push-next` pusht nur und pullt nicht — der Reset musste danach ein zweites Mal geschrieben und sofort gepusht werden. **Regel bleibt: Buch-Edit → sofort pushen, erst dann etwas anderes starten.**
2. **Scheinbar abweichender Fingerprint zwischen PC und Box** (`ca73aecf` vs. `e6e33c74`) war ein Lesefehler: Python auf der Box öffnet ohne `encoding=` in cp1252, und die Bein-Namen enthalten `·` (U+00B7). Mit `encoding='utf-8'` gelesen stimmen beide überein. Beim nächsten Buch-Vergleich über SSH also immer explizit utf-8 lesen, sonst jagt man eine Kontamination, die es nicht gibt.

### Deployt am selben Abend, 22:23 (Ticket `nt8-deploy-buch-kw34` / AP114)
- Vorher kontrolliert: keine offene Position (letzter Fill 21.08., glatt zu), NT8-Tageslog ohne Trade-Zeilen, Sonntag also Markt zu. Dann NT8 beendet, `box_deploy.ps1`: Backup `deploy-20260823-2222`, drei Dateien installiert, Pre-Flight + `dotnet build` sauber (0 Errors), DLL gesetzt 22:23:09, `obj`/`bin` wieder entfernt. Installierter Stand per SHA256 gegen die Referenz verifiziert, alle drei byte-identisch.
- **Nicht automatisch startbar:** NT8 braucht die interaktive Session (AP86), der Start aus der Session heraus wurde zusätzlich vom Sicherheitsfilter geblockt. Ist ohnehin die bessere Reihenfolge, weil die Handarbeit direkt danach kommt.
- **Offen, in NT8 von Hand:** `StopRangeMult` 0.4 → 0.30 bei MaxMomentumNQ. Das ist der einzige Wert, der wirklich muss: NT8 hat ihn in der Instanz gespeichert, ein neuer Code-Default zieht nur bei Properties, die es vorher nicht gab (BeTriggerR, ExcludeNewsDays, TargetRMult kommen also von allein). Dazu ORB-fade-Instanz deaktivieren und RiskGuard-Telegram nachtragen (`riskguard-telegram-20260820`).
- **Lab-Falle nebenbei gefunden:** `portfolio_next.json` trug noch die **verworfenen d260821-Beine** — ein altes Box-Artefakt vom 21.08., das `auto_check.py` brav zurückgespiegelt hatte, während `book_state_next.json` längst korrekt war. Der Next-Week-Reiter zeigte also ein Buch, das es nicht mehr gab. Nach `funded_finalize --next` + `live_finalize --next` tragen alle vier Portfolio-Dateien dasselbe Buch. **Lehre: nach einer Übernahme nicht nur die Bücher abgleichen, sondern auch die daraus gerechneten Portfolio-Dateien** — die Bücher waren synchron, die Auswertung nicht.


## #129 — „0 Kandidaten" war ein kaputter Filter, nicht leere Suche: corr_book-Ersatz-Bug, Buch-Drift Nr. 3, und warum korrelierte Beine mathematisch nie „dazu" dürfen (24.08.2026)

**Anlass:** Max' berechtigter Einwand — 190+ Hypothesen-Jobs, 865 Survivors, exakt 0 Kandidaten „kann nicht sein". Stimmte. Drei unabhängige Fehler stapelten sich; keiner davon war in der Inbox sichtbar.

### Fehler 1: `ctl_corr_book` disqualifizierte jeden Ersatz-Kandidaten an sich selbst
Die Kontroll-Batterie (#127) rechnete die Buch-Korrelation gegen **alle** Beine aus `book_state.json` — auch gegen das Bein, das der Kandidat per `replaces_leg` ersetzen soll. Ein besserer Exit auf demselben Signal (corr 0,9+ zum Original, logisch zwingend) konnte die Kontrolle **prinzipiell nie** bestehen. 10 Funde (TE-02/TE-04/TE-15, nominell +2,5 bis +4,9 pp Buch-Marginal) lagen deshalb zwei Tage stumm in `results/`. **Fix:** `run_controls(..., replaces_leg=...)` nimmt das abgelöste Bein aus dem Vergleich; der Runner reicht es durch.

### Fehler 2: Geblockte Buch-Verbesserer waren unsichtbar
Die Inbox kannte nur „Kandidat" oder Schweigen. Ein Fund, der das Buch verbessert und an genau einer Kontrolle scheitert, ist aber die wertvollste Information des Laufs — dort muss ein Mensch entscheiden, nicht der Filter. **Fix:** neuer Inbox-Kind **`blocked`** (Runner schreibt ihn, `inbox_tool`/`inbox.md` rendern ihn, Hub-Discovery-Tab zeigt Warnbanner + eigene Tabelle; `discovery_api.py` liefert `blocked_neu`/`blocked_ungelesen`, Hub neu gebaut). Die 10 Alt-Funde per Backfill nachgetragen.

### Fehler 3: Buch-Drift Nr. 3 (nach #126 und 23.08.) — diesmal 24 h lang
Das Wochenend-Buch-Update vom 23.08. **17:59** wurde nie per `--push-next` gepusht; um **18:01** starteten die TE-Jobs. Alle Buch-Marginals vom 23.08. 18:00 bis 24.08. 18:40 (Sync) liefen gegen das alte Buch (Fingerprint `f042e838`, noch mit `NQ_ORB-fade`, ohne `_v3`/`_d26...`-Beine). Obendrein: die Hypothesen-Jobs sagen `replaces_leg: "NQ_Momentum"`, das Bein heißt aber `NQ_Momentum_d260818` — im aktuellen Buch hätte der „Ersatz"-Test still nichts ersetzt. **Fixes:** (a) Namens-Auflösung im Runner (exakter Treffer, sonst eindeutiger Präfix, sonst laute Warnung), (b) **Buch-Drift-Wächter** in `inbox_tool.py --pull` (vergleicht Legs-Fingerprint PC vs. Box bei jedem Pull und schreit). Die „schlechter"-Verdicts der Nacht 23./24.08. sind gegen das falsche Buch gerechnet — für Verdicts zählt ab jetzt nur der Stand nach 24.08. 18:40; die PBO/Selektions-Urteile bleiben gültig (buchunabhängig).

### Die eigentliche Antwort auf Max' Portfolio-Frage (Quant-Mathematiker, MC-verifiziert)
Frage: mehrere hochkorrelierte Momentum-Beine **gleichzeitig** statt Ersatz? Antwort: **nein, nie auf diesem Käfig.**
- Bei Min-Size ist „korreliertes Bein dazu" exakt Positions-Skalierung k>1, und es gilt die Skalen-Invarianz **P_k(T,D) = P_1(T/k,D/k)** — größer werden = Käfig schrumpfen. P(pass) ist bei positiver Drift **streng monoton fallend in k** (Lundberg: θ_k = θ/k, exakt auch bei Fat Tails). Das 50k-Buch steht schon **rechts** vom Optimum (k=0,75 wäre besser, ist aber nicht handelbar).
- Add-Kriterium in Zahlen: Bein dazu hilft ⟺ **μ_c > (θ_b/2)·(σ_c² + 2ρ·σ_b·σ_c)**. Bei ρ≈0,9 liegt die Latte bei ~2,8× θ_Buch — praktisch unerreichbar. Das ist der formale Kern von Lehre 82.
- Konkret TE-02 (beste Config, gegen das **aktuelle** Buch, 5 Seeds): Nur-Original 85,8 % · **Beides drin 83,7 % (−2,2 pp, echt schlechter)** · Ersatz 86,2 % (+0,4 pp = neutral, unter Schwelle). Die nominellen „+4,9 pp" aus dem Lauf waren Drift-Artefakt (altes Buch + Basis „Buch mit Loch"). ρ(Kandidat, NQ_Momentum) echt gemessen: 0,665, nicht 0,97; ρ zum Restbuch 0,35.
- **Entscheidung: Buch bleibt wie es ist.** Kein Next-Week-Eintrag aus dieser Runde. TE-02-Ersatz nur wieder anfassen, wenn ein OOS-only-Marginal gegen den aktuellen Fingerprint die 1,5-pp-Schwelle nimmt.

### Offene Patch-Vorschläge des Mathematikers (bewusst NICHT nebenbei umgesetzt)
1. `theta_gate()` als billiger Vorfilter vor dem 5-Seed-MC in `eval_plan.py` (Lundberg-Schwelle; hätte hier ~90 % der Marginal-Läufe gespart — TE-02 „füllt" nur 49 % der nötigen Drift).
2. Ersatz-Basis-Semantik: `bm.verdict` misst bei `replaces_leg` „besser als ein Loch" — die tragende Zahl ist `vs_original`, sauberer wäre base = Buch-wie-es-ist vs. Buch-mit-Swap.
3. `evaluate_v2` `horizon_months=36` zensiert 100k/150k (E8 hat kein Zeitlimit) und kann die Tier-Rangfolge kippen — Entscheidung für Max, kein stiller Fix.

**Meta-Lehre (die wichtigste):** „0 Kandidaten" bei 865 Survivors ist kein Ergebnis, sondern ein Alarmsignal. Token-Disziplin („nur Inbox lesen") gilt für den Alltag — bei einem statistisch unplausiblen Muster ist der Blick in die `results/` Pflicht, nicht Kür. Und: **jede** Buch-Änderung am PC heißt im selben Atemzug `--push-next`, der Wächter erinnert jetzt automatisch.


## #130 — Payout-Plan-Nacht: Ziel „erster Payout + 10k€" komplett durchgerechnet, drei Tempo-Mythen beerdigt, RTY_Gap-fade zum Abschuss freigegeben (24.08.2026, Loop-Session)

**Auftrag Max (abends, dann abwesend):** Tempo = einzelnes Konto schneller durchbringen; 50 % jedes Payouts reinvestieren; auch andere Prop-Firms prüfen; kooperativ mit Agents das Ziel verfolgen, ohne Overfitting. Ergebnis-Notiz: [[Payout-Plan (Erster Payout + 10k)]]. Gerechnet haben quant-mathematician (Kaskaden-MC, Firmen-Käfige), quant-statistician (Unsicherheit, Purged-WF, DSR/PBO), strategy-auditor (operative Machbarkeit, Gegenlese), Pool-Agent (2.643 Kombinationen).

### Die Kernzahlen
- E8 50k, aktuelles Buch, k=1: Median erster Netto-Payout **Monat ~15**, reine Driftstrecke 14,6 Monate (3.000 Eval + 2.625 Funded-Schwelle bei 25,8 $/Tag). 12-Monats-Median der Entnahme: **0 $ in allen Szenarien** (Mittelwert 721 $) — das Einkommen ist ein Klumpen, kein Strom (>90 % Null-Monate).
- **Purged-Walk-Forward (neu):** ehrliche Forward-Drift **10-14 $/Tag** statt 25,8. Fit-Prämie kippt von −31 % (2016-19) auf +61 % (2022-26) — die Params sind ins junge Regime gefittet. Vier unabhängige Methoden (DSR, Vor-Discovery-Epoche, WF+Restdeflation, Forward-Folds 24-26) konvergieren auf ~10.
- **Firmen-Vergleich (FundedNext Flex 50k, Support-Mails primärquellen-fest im [[Research-Cache]]):** „EOD"-DD ist bei offenen Positionen in Wahrheit **Floating-Equity-Breach** (bestätigt, Antwort „(a)"), Käfig effektiv 1.500 $ intraday → Buch-Passquote dort 76,1 %. ABER Payout ab 500 $ Zyklusprofit + 5 Benchmark-Tagen: **Ziel 1 Median 318 statt 461 Tage (µ=13: 546 statt 918)**. Langfristig gewinnt E8 (Gratis-Challenge-Recycling). Plan: E8 behalten, FN als schnellen ersten Slot (~80 $). Tradeify raus: „exclusive to Tradeify"-Klausel + Wohnsitz-Login nach jedem VPS-Neustart.

### Drei Tempo-Mythen beerdigt (jeweils doppelt: Statistik + Operativ)
1. **k_eval=3 („Tempo-Slot"):** halbiert zwar die Zeit auf dem Papier (15,2→9,4 M), aber P(µ>19-Kipppunkt) nur **12-16 %**, UND E8s 4-Mini-Kombicap würde an **47 % der Tage** gerissen, UND RiskGuard kennt kein Per-Leg-Sizing (eine `liveQty` für alle Beine aus `maxlab_size_*.txt`), UND `DailyLossLimit=900` ist nie für 3× Size kalibriert. Verdikt Auditor: **Papierrechnung**.
2. **„Nach Floor-Lock rausquetschen" (Max' Hypothese):** falsifiziert — auszahlbar ist nur was über Start+Buffer liegt, das Polster ist nach jedem Abruf strukturell ~2.000-3.250 $ = bereits 1,16× Voll-Kelly bei k=1. k>1 in der Funded-Phase ist monoton schlechter, auch polsterabhängige Regeln finden nichts.
3. **Portfolio-Neubau unter Tempo-Ziel:** 2.643 Kombis aus dem 21er-Pool, Selektion auf 70 %, Endbewertung auf 30 %: **keine schlägt das Buch OOS**. IS→OOS-Rangkorrelation **−0,18** (11k-Ziel: −0,65), PBO **71 %** — die Selektion ist kontraproduktiv. Der IS-Sieger (VWAP-Pullback ×3) bricht OOS auf Rang 87/121; das aktuelle Buch: Rang 10/121. Einziger Überlebender „Asia-Dir ×2" starb in der Gegenlese: doppelter Fit (Params #126 + post-hoc-7er-Referenzmenge), 85 OOS-Tage unterbestimmt (Nachweisgrenze 64 $/Tag), 31 % des Gewinns auch bei Edge null, kostet −3,7 pp auf der v2-Zielgröße. Merksatz des Statistikers: **dieselbe Tempo-Metrik gibt dem toten RTY-Bein t=−7,3 — Tempo-Metriken allein sind kein Beweisinstrument.**

### Was TATSÄCHLICH bleibt (die drei robusten Hebel)
1. **FN-Flex-Slot** für Ziel 1 (Details oben; vor Kauf 2 Klärfragen: Floor-Lock-Zeitpunkt, Parallelbetrieb zu E8).
2. **Auszahlungs-Politik „sofort ab Minimum"**: 1-2 Monate früheres erstes Geld für ~10 % auf 24 M, Ziel 2 unberührt. Nach Payout 1 auf halben Cap.
3. **Kaskaden-Disziplin: nie bei null Konten stehen** — größter Einzelhebel überhaupt (wörtliches „nur Reinvest" endet in 35-53 % der Pfade bei 0 $ für immer).

### RTY_Gap-fade: zum Abschuss freigegeben
Auditor-Gegenlese nach dem PWF-Fund: Buch-Config besteht das eigene Top5-Gate nicht (0,638), 2/3 Epochen negativ, ATR-Band ohne dokumentiertes Why, schlechter als die eigenen Grid-Nachbarn; kanonischer Mechanismus in ALLEN Epochen signifikant negativ. **Umsetzung über den regulären Kanal:** Entfernung in `book_state_next.json` (4-Bein-Buch: 86,1 % / 174 $ / 195 d — praktisch identisch zum 5-Bein-Buch), Ticket `next-week-2026-35-gapfade`, Retune-Job `gapfade_retune_RTY_260824` lief noch am Abend auf der Box: Selektion sauber (PBO 3 %), aber **0 Kandidaten** — auch die Nachbar-Fläche verdient keinen Ersatz, Original gegen das aktuelle Buch −0,1 pp (neutral). Wochenend-Entscheidung läuft auf „raus ohne Ersatz" zu.

### Für die Werkzeuge vorgemerkt (Entscheidungen Max, kein Auto-Fix)
- `contracts`-Feld je Bein in `book_state.json` + Ein-Zeilen-Übersetzung in `funded_finalize`/`eval_plan` (`dc = C@w`) — falls je wieder ein Gewichtsvektor geprüft wird.
- Pool-Suche-Maschinerie behalten, aber Zielspalte auf `pass_pct`/$-pro-funded, Nulldrift-Spalte fest in jede Variantenprüfung.
- `theta_gate()`-Vorfilter (Lundberg) vor teuren Marginal-MCs; `horizon_months=36`-Zensur; Historien-Bootstrap ins `book_contribution`-Rauschmaß (Faktor ~25 unterschätzt).
- Echte Vorwärtszeit läuft seit 20.08. — erst nach ~12 Monaten Live trennt sie 10 von 19 $/Tag (Power-Grenze, kein Ungeduldsproblem).


## #131 — FA-01 Fast-Alpha-Overlay in die Pipeline + Sync-Vorfall: Box rechnete mit Code vom Vortag, Skript meldete trotzdem „fertig" (25.08.2026)

**Anlass:** Paper Zarattini/Pagani „Improving Performance with Fast Alphas" (Concretum QuanTips #2, Feb 2026; Research-Cache-Abschnitt vom 25.08.). Kernidee: standalone tote Kurzhorizont-Mean-Reversion als Execution-Overlay — Trend-Entry erst nach 1 abgeschlossener Gegen-Bar ausführen.

**Was gebaut wurde (der EINE Weg, #127):**
- Engine: `sigcore.pullback_entry()` (Entry-Verzögerung, Fill am Open der Folge-1m-Bar, Timeout enter/skip), `sigcore._pb_exit()` (Stop als Alarm — von FA-01 bewusst NICHT benutzt), `simulate_trade(stop_px=…)` (Anker-Stop bleibt beim Basis-Entry, sonst kippt die R-Definition; Guard: Anker schon gerissen → kein Entry). `tsmom`: `tm_pb_entry/tm_pb_maxwait/tm_pb_timeout(+exit)`. `overfit.paired_delta_report()` (gepaarter Trade-Join, Block-Bootstrap auf der Differenzreihe, Tages-Blöcke, sd_d/mde_80/flip_rate).
- Hypothese FA-01 in `hypothesis_bank.py`: NQ+ES, 72 Configs je Symbol, `kein_overlay`-Kontrolle im Grid, `pb10_w45` als erwartete Totzone (Plateau-Kontrolle). Deckt TE-11 aus der Coverage-Karte ab.

**Quant-Team-Befunde vorab (beide Agents, 25.08.):**
1. **Entry-Overlay hat auf NQ-Breakouts echten Platz:** Post-Signal-Drift von ORB-30-Signalen ist die ersten 15–20 Min NEGATIV (−0,76 Pkt bei 15 min), erst danach läuft der Trend — Mechanismus: der Ausbruchs-Impuls wird von Stop-Runs getragen, wer am Break-Close kauft, zahlt die Stop-Run-Prämie. Gepaart gemessen +0,85 Pkt/Trade (P>0=0,97), nach Shrinkage eher +0,4–0,6.
2. **Auf tsmom-Zeitfenster-Momentum ist dasselbe Overlay klar negativ** (lokal −0,02..−0,05 R, boot_p<0,05) — Drift-Identität Delta = −d·E[τ]: das Overlay gewinnt NUR, wo der Preis nach dem Signal erst gegen die Richtung läuft. Vor jedem Einbau den Drift des konkreten Beins messen, nie annehmen.
3. **Exit-Overlay tot für Evals:** E[PnL]≈0, aber −13..−20 Pkt Zusatz-MAE je Stop-Touch, Skew −1,0, 1%-Tail −133 Pkt = 10% des 50k-Puffers in einem Ereignis. Der Käfig bestraft Pfad-Varianz, nicht Erwartungswert.
4. **Skip-Timeout tot:** wirft genau die Runner weg, sd(d) explodiert (Faktor 10–17 mehr Stichprobe nötig). Overlay verzögert Entries, lässt nie welche aus.
5. **Gepaart auswerten ist Pflicht:** zwei getrennte Equity-Kurven verschenken 90–99 % der Power. Ticket `fa01-paired-eval-runner` (Runner-Integration + `ctl_placebo_overlay`).

**Der Vorfall (Lehre, #126-Klasse — diesmal Code statt Buch):** `box_provision_discovery.ps1 -SyncOnly` meldete „fertig", aber der scp-Aufruf mit Backslash-Glob (`"$tmp\*"`) schlug still fehl — die Box rechnete den ersten FA-01-Job mit dem Engine-Stand vom Vortag, der `tm_pb_entry` gar nicht kannte. `qbt` validiert nur den `mode` und ignoriert unbekannte Params still: 72 „verschiedene" Configs, alle identische Baseline-Trades, Schein-Plateau inklusive. Gefunden vom neuen **`pipeline-auditor`**-Agent (erster Einsatz, per SSH-mtime-Vergleich). Fix: Teillauf verworfen, Sync repariert (Verzeichnis-Inhalt statt Glob, harter Exit-Code-Check, Zeitstempel-Marker wird zurückgelesen), Runner neu gestartet. **Lehren:** (1) Ein Sync-Skript, das den Exit-Code seiner Kopier-Befehle nicht prüft, ist kein Sync-Skript. (2) Unbekannte Params müssten laut werden — Kandidat für ein Gate: Job-Params gegen Modul-DEFAULTS validieren. (3) Der Pipeline-Auditor gehört ab jetzt VOR jeden neuen Job-Typ (steht so in CLAUDE.md).

**Stand:** FA-01 (NQ+ES, 144 Configs) liegt mit Prio 88 auf der Box, Runner läuft mit verifiziertem Code. Auswertung beim Rücklauf NICHT über Einzelzellen-Ranking, sondern `paired_delta_report` je pb_profile gegen `kein_overlay` (Runner kann das noch nicht — Ticket). MultiCharts-Port `FastAlpha_ATR_Breakout.txt` für Max' Handtest liegt in `Projects/trading-data/multicharts/`.

## #132 — ES-Offensive: GEX-Buch-Gate ehrlich beerdigt, drei ES-Flow-Jobs in die Queue, zwei stille Pipeline-Löcher gestopft (25.08.2026)

**Auftrag Max:** ES fehlt im Buch — Mechanismen finden, die dort laufen können, alle Kandidaten durch die Queue schicken, plus: welche anderen Futures wären attraktiv.

**1. Warum ES bisher leer ausging (Scout-Kernbefund):** MES zahlt pro Einheit Bewegung das **3,6-fache** von MNQ (Round-Trip 0,90 % der Median-Tagesrange vs. 0,25 %; im 2-Tick-Stress 1,54 %). Die 823 ES-Register-Trials sind an Mechanik gestorben, nicht an Ideenmangel. Konsequenz: auf ES zählt **$/Trade statt Frequenz** — die besten ES-Survivors sind Event-Trades (EVENT_ES ~47 $/Trade), gescheitert nur an ~11 Trades/Jahr. Bewusste Ausnahme vom HF-Fokus, nur für ES.

**2. GEX-Buch-Gate ist tot.** Der vergessene Lauf vom 16.08. (Quintil +2,67 pp „besser") wurde gegen das aktuelle 5-Bein-Buch neu gerechnet: Quintil nur noch **+1,21 pp bei Schwelle ±1,30 = neutral**, Vorzeichen-Gate schlechter, GEX-Residuum-nach-VIX neutral (+0,11). Der 16.08.-Effekt war buchabhängiges Rauschen. Die heute gebauten Engine-Gates (`tm_gex_min/max`, `tm_vix_min/max`, `tm_vix_rank_min/max` in `sigcore.gates_pass`, Daten `DIX_GEX_daily.csv`/`VIXCLS.csv`, 250d-Rang, t−1) bleiben als Werkzeug für Discovery-Jobs. Alt-Ergebnis gesichert als `gex_gate_results_260816.json`.

**3. Drei ES-Jobs eingereiht** (alpha-scout, Audit „sauber mit Auflagen"): `wexp_charm_ES` (Charm-Unwind an ALLEN Freitagen statt nur Monats-OpEx, tsmom + `tm_dow`, Mo-Do-Kontrollzelle, Prio 68) · `eusession_break_ES` (Europa-Fenster 03:00-09:25 als Breakout-Range, asian-Modus, Prio 64; Prämisse stirbt vermutlich ehrlich — Basis-expR lokal −0,05) · `vixrev_ES_wide` (VRP nach Angst-Spike, vix_bias, mit Momentum-Kontrollzelle, Prio 60). FA-01-Stand: ES 0 Survivors (Basis scheitert einheitlich an top5+cost2t — kein Filter-Bug), **NQ 30 Survivors / 0 Kandidaten**; die eigentliche Overlay-Frage klärt die gepaarte Auswertung am Wochenende (Ticket).

**4. Zwei stille Pipeline-Löcher (pipeline-auditor, zweiter Einsatz, wieder Volltreffer):**
- **B1 Stale-Cache:** `qbt.load_rth`/`asian.load_full` nutzten `engine/cache/*.parquet` ohne mtime-Check — ALLE Backtests endeten still am 06.07., obwohl Daten bis 10.08. da sind; der Cache wurde auch noch auf die Box gesynct (PC und Box rechneten auf verschiedenen Samples ins selbe Register). Fix: mtime-Check in beiden Loadern, `cache` aus dem Box-Sync raus, Box-Cache gelöscht.
- **B2 deploy_ready-Loch:** `controls.py` übersprang Delay-/Nulldrift-Kontrolle für Modi ohne Schalter (`asian`, `vix_bias`, …) mit `ok=None` — und `run_controls` zählte nur `ok=False` als Fehlschlag → **deploy_ready ohne je einen Look-ahead-Test**, und `promote_next` promotet auf genau dieses Flag. Fix: Pflichtkontrollen (delay, null), übersprungen = nicht deploy_ready. Folge-Arbeit: Delay-Schalter für asian/vix_bias nachrüsten, sonst bleiben deren Funde dauerhaft (korrekt) gesperrt.
- Dazu **B3**: Kontrollzellen (Label „*kontrolle*" bzw. `control_labels`) sind jetzt vom Survivor-Ranking/Kandidatur ausgeschlossen — ein Falsifikations-Zwilling darf das Why widerlegen, aber nie selbst promotet werden. Und ein Zombie-`running`-Status (hyp_FA01_NQ) auf der Box bereinigt.

**5. Andere Futures (research-scout):** Ranking MCL (EIA-Inventory-Flows) > MNG (EIA Storage) > MGC (London PM Fix, peer-reviewed) > Micro-Yield 10Y (Auktions-Flows) > M6E > MBT (Weekend-Gap seit CME-24/7 am 30.05.2026 strukturell TOT). **Aber: für keinen einzigen ist die E8-Handelbarkeit primärquellen-belegt** (Terms/ESPA enthalten keine Instrumentenliste), für keinen liegt 1m-Historie vor, und der Datenexport-Weg ist undokumentiert. Tickets: `e8-instrumente-anfrage`, `futures-datenexport-doku`, `cal-macro-post-modul` (CPI/NFP-Event-Modul = aussichtsreichster ES-Buch-Weg, braucht harte BLS-Datumslisten statt Volumen-Spike-Erkennung), `spx-csv-refresh`.

**Lehren:** (1) Ein Regime-Gate, das nur auf einem bestimmten Buchstand „besser" ist, ist kein Gate, sondern Rauschen — Buch-Gates immer gegen den aktuellen Stand rechnen, bevor irgendwas gebaut wird. (2) Caches ohne Quell-mtime-Check sind Zeitbomben (dritte Stale-State-Klasse nach Buch #126 und Code heute Mittag — jetzt alle drei mit Automatik geschlossen). (3) Eine übersprungene Pflichtkontrolle ist ein Fehlschlag, kein „n/a".

## #133 — CVD-Divergenz nach Session-Open: in >250 Arten gemessen, Friedhof — und die billige Familien-Messung VOR dem Grid als neues Muster (28.08.2026)

**Auftrag Max:** CVD-Divergenzen (Preis macht neues Extrem, kumuliertes Aggressor-Delta bestätigt nicht) nach Session-Open in mindestens 100 Arten testen, Timeframes 1m-15m, Trade in die Gegenrichtung zurück zum Ursprungspunkt.

**Gebaut (bleibt in der Engine):** `tm_signal="cvddiv"` in `tsmom.py` (3 Divergenz-Arten extreme/close/slope, CVD seit Open auf tf-Bars, Null-Delta- und Abdeckungs-Guards), `sigcore.load_delta_1m()` (echtes Bid/Ask-Delta aus Orderflow v2 mit mtime-bewusstem Cache), Block CVD in `hypothesis_bank.py` (5 Hypothesen, 188 Arten / 436 Configs — **stillgelegt per `CVD_ENABLED=False`, nie eingereiht**). Orderflow v2 liegt jetzt auch auf der Box (`trading-data/orderflow/v2`, 323 Parquets).

**Warum nie eingereiht: das Quant-Duo hat die komplette Familie VOR dem Enqueue direkt gemessen** (0 Registry-Trials, ~15 Min Rechenzeit, Skripte im Session-Scratchpad):
- **Statistiker:** 63 Zellen (TF × Fenster × 3 Definitionen × 3 Schwellen) × 2 Symbole × echt/Proxy × 3 Horizonte, mit familienweitem Permutations-Null. Bestes |t| = 1,81 (NQ) / 2,49 (ES) bei Rauschdecke ~2,6 der eigenen Suchbreite → **FW-p 0,32-0,995, kein Ansatz auffällig.** Rückkehr-zum-Open-Quote hängt fast nur an der Extension (Basisrate NQ 56,7 %, ES 63,4 %), nicht am Delta.
- **Mathematiker:** 18 Prämissen-Zellen + symmetrisches ±q-Bracket (Null exakt 50 %): kein |z| > 2, Vorzeichen kippen zwischen L=15/30/60. Strukturell: corr(1m-Return, 1m-Delta) = **0,68** → jede Divergenz ist 1 Bit eines kleinen Residuums; die drei Definitionen sind mathematisch dieselbe Größe auf drei Intervallen (extreme = close auf endogenem Intervall). Fade-zum-Open trägt eine **negative Trägerdrift von −0,13 R netto** (NQ trendet bei großer Distanz vom Open weg, kein OU).
- **Echtes Delta vs. Proxy:** gepaart je Tag, max t für Zusatzinfo des echten Deltas 1,1 (NQ) / 2,1 (ES) bei Decke ~2,4 → **das echte Bid/Ask-Delta trägt keine messbare Information über den Tick-Rule-Proxy hinaus.** Die teure Orderflow-Achse ist damit generell verzichtbar.
- Bestätigt Archiv #021 (damals 2021-2025) auf 10,5 Jahren und beerdigt die Familie inklusive der offenen Frage „lag es am Proxy?": nein.

**Pipeline-Funde nebenbei (pipeline-auditor, STOPP vor dem Push — alle drei wären ohne ihn ins Register gelaufen):**
1. **`tm_exit="base"` (Level-Target) hatte keinen Target-Seiten-Guard** in `sigcore.simulate_trade`: liegt das Ziel hinter dem Entry, feuerte es sofort auf der Entry-Bar → bis 43 % der Trades mit r < −1R (bei korrektem Stop unmöglich). Gefixt analog zum Stop-Guard. Ganze Fehlerklasse „Level-Ziel hinter Entry" geschlossen.
2. **Orderflow v2 ist 2016 zu 100 % und 2017 zu ~39 % NULL (nicht NaN)** — ein NaN-Abdeckungs-Guard sieht das nicht, und Null-Flow erzeugt exakt das Muster, das die Divergenz-Hypothese sucht. Guard erweitert (Tag mit >10 % Null-Minuten fällt raus). YM endet 2020-05, RTY-Orderflow ist mit dem Loader gar nicht lesbar (RangeIndex).
3. **Ein Falsifikations-Arm stirbt am Rentabilitäts-Premise:** CVD-04 (Continuation-Kontrolle) wäre als premise_failed verworfen worden, BEVOR er irgendwas kontrolliert — Kontroll-Jobs (`book=False`) dürfen nicht an `expR>0` hängen. Als Ticket `pipeline-haertung-cvd-funde` festgehalten (mit DSR-Gate-Vorschlag des Statistikers und Daten-Integritäts-Gate je externer Zeitreihe).

**Buch-Lücke in einer Zeile:** CVD-Divergenz hängt an **Stufe 1 (Prämisse)** und kommt da nach zwei unabhängigen Messungen (hier + #021) nicht durch. Was sie bräuchte: eine Zelle mit |z| ≥ 2 im symmetrischen Bracket, stabil über beide Epochen und beide Märkte — nichts im getesteten Raum ist in der Nähe. Familie geschlossen; Reaktivierung nur auf ausdrückliche Ansage.

### Lehren
139. **Die billige Familien-Messung VOR dem Grid ist das schärfere Instrument.** Statt 436 Configs auf der Box zu rechnen, haben zwei lokale Messungen (Familien-Permutations-Null + Prämissen-Zellen) die Frage in ~15 Minuten ohne einen Registry-Trial beantwortet — schärfer als der Job es gekonnt hätte, weil familienweit statt Zelle-für-Zelle. Bei jeder neuen Hypothesen-Familie mit niedrigem Prior: erst diese Messung, dann (nur bei Signal) das Grid.
140. **Ein Level-Target braucht denselben Seiten-Guard wie ein Stop.** „Ziel hinter dem Entry" ist ein Ausführungsfehler (r < −1R), kein schlechter Trade — und er blieb unsichtbar, weil die Fehlerrichtung konservativ war. Invariante: r kann ohne Trailing nie unter −1R liegen; Verletzungen sind exec_bug, nicht Ergebnis.
141. **Null ist nicht NaN.** Eine externe Zeitreihe kann vorhanden, aber entartet sein (Orderflow 2016: 100 % Nullen) — Abdeckungs-Guards müssen Entartung (Null-/Konstant-Anteil) prüfen, nicht nur Lücken. Sonst produziert die Datenlücke genau das Signal, das die Hypothese sucht.

## #134 — Value-Area-Migration (Valentini Baustein 1) auf Tages- UND Candle-Ebene falsifiziert; zwei Schätzer-Fallen formal bewiesen (28.08.2026)

**Anlass (Max):** Valentini-Interview (YouTube HUYBdYnXUNc, "NASDAQ Effort"-Modell, siehe [[Research-Cache]]) — Ansage: die Bausteine EINZELN testen, zuerst nur die Value-Area-Migration (VA70, immer Volumen), verschiedene Shift-Definitionen, Referenzen (Vortag / 3 Tage), Kerzenfarbe als Filter. Erst Tagesebene (D vs. D−1 → D+1), dann intraday (Candle vs. Candle, TF 5/15/30).

**Werkzeuge (bleiben):** `developer/amt_va_migration.py` (Tagesebene, baut auf `amt_daily_{NQ,ES}.parquet` aus #112) und `developer/amt_va_migration_intraday.py` (Candle-Profile aus 1m-Bars, tages-geclustert, slot-demeant) — beide mit fest eingebauten Placebo-Armen und (intraday) dem korrigierten Martingal-Schätzer.

### Teil 1: Tagesebene — null, und der "Effekt" war der Tages-Return
- 11 Shift-Definitionen × 2 Outcomes (Folgetag Open→Close, Close→Close) × NQ/ES × 3 Epochen: **max|t| 1,95 bei Null-Median 2,63 der eigenen Zellfamilie (FW-p 0,94)** — ruhiger als Zufall. Effektive Tests ~81 von 396 Zellen.
- **Confound (Mathematiker):** corr(ΔPOC, Tages-Return) = **0,76** — die Migration ist eine verrauschte Umkodierung der Kerzenfarbe des Tages. Der Placebo (Return-Vorzeichen) trennt dieselben Tage BESSER als die POC-Migration; konditional auf den Return trägt ΔPOC exakt null. Die scheinbare Fade-Tendenz war die Long-Drift-Aufteilung (mehr Up- als Down-Tage → Spread ist netto short).
- **Power belastbar:** alles ab Solo-Sharpe ~0,9-1,0 ausgeschlossen; was theoretisch übrig bleiben könnte (δ 0,02-0,04 ATR) bräuchte 40-70 Jahre Daten — für Entscheidungen nicht existent. **Kein Signal, kein Filter.**

### Teil 2: Intraday — die spektakulären t-Werte waren ein Schätzer-Artefakt
- Rohlauf: alle Migrations-Spreads stark negativ, |t| bis 48 bei "bis Session-Close". **Mathematiker hat den Bias geschlossen hergeleitet: E[Spread_eod] = −E|Kerzenkörper|** (und −2h·E|body|/n für fwd_h) — der Tages-Verhältnis-Schätzer über preisabhängig selektierte Candles mit gemeinsamem Endpunkt erzeugt das Signal selbst. Auf einem reinen Random Walk liefert derselbe Code **t = −60**. Realdaten: 82-102 % der beobachteten Werte durch die Formel erklärt.
- **Korrigierter Schätzer** (Tages-Summe z·e mit slot-zentriertem Signal, E=0 exakt unter Martingal, jetzt fest im Skript): alle Migrations-Signale (poc_up, va_shift, poc_up3, ± Kerzenfarbe) fallen auf t ≈ +1,9…+2,9 — **gleichauf mit dem Placebo und unter der Zufallsdecke (~3 bei 108 korrelierten Zellen)**. Valentinis Continuation-These ist auf Candle-Ebene exakt null.
- Einziger statistisch echter Rest: `poc_vs_ret` (POC hoch bei roter Kerze) tf5, korrigiert t 4-7,5. Zerlegt: **abgeschwächtes "fade die Kerzenfarbe" + Range-Position** (POC-Bedingung SUBTRAHIERT Information), Amplitude 0,2-1,2 Ticks, Zerfall in 1-3 Minuten, **Faktor 3-5 unter Round-Trip-Kosten selbst am optimistischen CI-Rand** (NQ netto −0,4 bis −0,7 Pkt/Trade). Mikrostruktur, nicht handelbar.
- Power: Auflösung 5-8× feiner als die Kostenschwelle — das Null ist ein echtes Null, kein Datenmangel.

### Verdikt
**VA-Migration trägt weder auf Tages- noch auf Candle-Ebene handelbare Richtungsinformation — Friedhof, AMT-Reihe #112-#114 + #134.** Buch-Lücke: Stufe 1 (Prämisse), geschlossen. Bewusst NICHT getestet (einzige offene Rest-Formulierung): session-entwickelndes Profil vs. Vortags-VA über Stunden mit Open-Type-Kontext — nach zwei unabhängigen Nullmessungen + #113/#114 nur auf ausdrückliche Ansage wieder aufmachen. Register: +164 Trials (56 Tages- + 108 Intraday-Zellen).

### Nebenfunde
1. **ES-Datenleck:** der #075-Guard (`qbt.py`, Preis ≤ 0) übersieht 14 Dezember/Juni-Roll-Tage mit POSITIVEN Spread-Quote-Preisen (Close 2,9 / 52,5 / 73,8 statt ~2600-6100) — sprengt jede Close-zu-Close-Statistik um Faktor 100+. In beiden Studien per Median-Band-Guard neutralisiert; Engine-Fix als Task-Chip angelegt.
2. **Register-Race:** der Runner lädt `registry.json` am Job-Anfang und schreibt sie während des Jobs mehrfach zurück — **externe Backfill-Einträge während eines laufenden Jobs werden still überschrieben** (zweimal passiert: +56 und +164 verschwanden). Backfill nur bei gestopptem Runner (STOP → warten auf Lock-Freigabe → Backfill → Neustart per WMI); langfristig Merge-Semantik.

### Lehren
142. **Jede Statistik der Form "Outcome bis Session-Ende, innerhalb des Tages über preisabhängig selektierte Candles gemittelt" ist um −E|Kerzenkörper| verzerrt** — der Verhältnis-Schätzer erzeugt t-Werte von 40+ aus purem Rauschen. Gegenmittel: Martingal-orthogonaler Summen-Schätzer (Tages-Summe z·e, z slot-zentriert und F_k-messbar) UND als Pflicht-Selbsttest dieselbe Statistik auf einem simulierten driftlosen Pfad mit gematchter Body-Verteilung (muss 0 liefern).
143. **Signal-Redundanz-Kontrolle vor jeder Interpretation:** hat ein Kandidaten-Signal |corr| > 0,7 zum rohen Return derselben Periode, ist es dessen Umkodierung — der Rohreturn muss automatisch als Placebo-Arm mitlaufen, sonst wird Return-Autokorrelation als "neuer Mechanismus" fehlgelesen (hier: ΔPOC ≈ Tages-Return mit 0,76, Placebo schlug das "Signal").
144. **Ein externer Schreiber verliert gegen einen laufenden Prozess, der dieselbe JSON im Speicher hält** (Read-Modify-Write ohne Sperre) — vor jedem Register-/State-Backfill den Besitzer-Prozess stoppen oder Merge-Semantik bauen; ein "erfolgreich" gemeldeter Write beweist nicht, dass er überlebt.

## #135 — Roll-Garbage in den 1m-Parquets: 83 Fremdkontrakt-Sessions entfernt, alle vier 1d-Ratio-Serien repariert (30.08.2026)

**Root Cause der ältesten bekannten Daten-Falle gefunden und behoben.** Der QuantPad-Export hat an den Quartals-Rolls 1-2 KOMPLETTE Tage Kalender-Spread-Quotes statt echter Preise in die Continuous-1m-Serien geliefert. Die Quotes sind der Carry (ES ~50-70 Punkte in der 5%-Zins-Ära, negativ 2020/21 als Dividenden > Zinsen) — d.h. ein Teil ist **positiv** und rutschte durch den #075-Guard (Preis ≤ 0) in jeden Backtest, auch auf der Box.

**Befund (Scan: Session-Median-Close >30% vom Nachbar-Median, iterativ):**
- **ES: 16 Garbage-Sessions** (2017-2026; nur 2 davon negativ, 14 liefen ungefiltert mit — u.a. ALLE Rolls 2023-09 bis 2026-06), 18.530 Bars.
- **RTY: 67 Garbage-Sessions** (praktisch jeder Roll seit 2017, inkl. einer 8-Tage-Strecke Sept 2017), 45.691 Bars.
- **NQ/YM 1m: clean.** Kein einziger Mixed-Day — Garbage ist immer die komplette Session (die echten Bars fehlen an diesen Tagen ersatzlos).
- Bereinigt 30.08.2026, Backups `*.bak-20260828`, `manifest.json` neu erzeugt (war seit 06.07. stale).

**1d-Reparatur — zwei Fehlermechanismen, beide über r(t) = adj_1d/unadj_1m sichtbar** (r ist marktimmun, echte Bewegung kürzt sich raus):
1. **Falsche Ratio-Faktoren an Garbage-Rolls:** QuantPad bildete den Roll-Faktor aus der Spread-Quote statt aus Preisen. Negativer Faktor = Vorzeichen-Flip der GESAMTEN Historie davor — genau das war die bekannte „ES 1d vor Mitte 2021 unbrauchbar"-Falle (copilot.py, 17.08.); Spread/Spread-Faktoren erzeugten zusätzlich moderate 17-41%-Verschiebungen.
2. **Chunk-Naht-Brüche:** der 1d-Export lief in 180-Tage-Chunks, jeder Chunk wurde EINZELN ratio-adjustiert. An den Nähten springt r — meist ~1%, aber an der Covid-Naht März 2020 **8-10% auch bei NQ und YM**, die nie als kaputt galten.

Reparatur segmentweise: Boundaries = Vorzeichenwechsel / Einzelsprung >10% / geglättete 5-Tage-Median-Stufe >3%; wahre Faktoren aus den Spread-Quotes der Garbage-Tage rekonstruiert (f = 1 + spread/P), an Nähten Kontinuität. 1d-Zeilen, die selbst Spread-Quotes waren oder in reparierten Segmenten nicht gegen die 1m verifizierbar sind, entfernt (ES 5, RTY 65). Validiert: keine Rest-Stufen (geglättet <2,9%, Einzeltag <4,2% = Settle-Rauschen), Level plausibel (ES 2016 adjustiert 2441 vs. raw 2012 = kumulierter Carry +21%). ES/NQ/YM/RTY-1d sind damit **ab 2016/2017 durchgehend brauchbar**; `_SPX_PROXY_MIN_DATE` in copilot.py bleibt vorerst bewusst auf 2021-06-14 (nur Report-Fenster, kann jetzt zurückgesetzt werden).

**Engine-Impact (Golden-Master-Regression):** alle 5 NQ-Fälle + VIX_spike_rev bit-identisch, beide Kanarien sterben korrekt → Sync frei. **RTY_Gap-fade (Buch-Bein): 222→211 Trades, expR 0.0551→0.0595 (+8%), Sharpe 1.114→1.211 (+8,7%)** — die Garbage-Tage hatten das Bein UNTERSCHÄTZT. Golden Master dokumentiert aktualisiert. `asian.py:load_full` hatte bis heute GAR keinen Korrupt-Filter und trägt jetzt denselben Guard wie `qbt.load_rth` (der Median-Band-Guard selbst kam in der Nacht-Session 03:05, #134-Nachtrag). Box: Runner sauber gestoppt, Engine + bereinigte Daten gesynct, Runner neu gestartet. Portfolio via `funded_finalize`/`live_finalize` nachgezogen.

**Lehren:**
1. **≤0-Checks fangen nur die halbe Garbage-Welt.** Fremdkontrakt-Daten können auf beliebigem positiven Level liegen; Pflicht ist ein Median-Band gegen die Nachbar-Sessions (steht jetzt in `qbt._drop_corrupt_sessions`).
2. **Adjustierte Serien immer im r-Raum gegen die unadjustierte Basis prüfen** — r = adj/unadj ist marktimmun und macht Faktor-Brüche sichtbar, die in Preis- oder Return-Charts im Rauschen verschwinden (NQ/YM sahen 6 Jahre lang „clean" aus).
3. **Chunked Exporte nie per Chunk adjustieren lassen** — das „ratio"-Label der QuantPad-1d war nie global konsistent.

Siehe [[Backtest-Engine]], [[Discovery-Runner v2]]; Guard: `qbt.py::_drop_corrupt_sessions`, Details/Skripte im Session-Scratchpad 30.08.

## #136 — AR-15: 200d-MA-Regime-Filter in 100 Varianten getestet — kein Kandidat, Mechanismus nicht widerlegt; dazu zwei Pipeline-Lehren (Näherungs-Ranking, Masken-Rauschen) (30.08.2026)

**Auftrag Max:** den 200-Tage-MA als Regime-Filter über die Buch-Beine legen (an/aus unter dem MA, ~100 Arten), plus Breakout-Familie und den NQ_LastHour-Nebenbefund. Vorher Recherche (10 Papers, [[Research-Cache]] Abschnitt „MA-200d/Regime-Filter"), Hypothese als AR-15 in der [[Hypothesen-Bank (Momentum & Averages)]].

**Getestet:** 25 vorab fixierte Signale (SMA/EMA × 50-252 Tage × eigen/ES × Level/Steigung/4-Regime/z-Quantil × Hysterese/Bestätigung) × 4 Aktionen (alle aus / nur MR aus / nur Momentum an / invertiert) = **100 Varianten**, Signale strikt aus t−1, Min-Size an/aus je Tag, auf dem 5-Bein-Buch `f5330057adfa`. Kanonischer Rechenweg = `cage_policy_lib.evaluate_v2`-Konfiguration (36 Monate, 6000 Sims × 5 Seeds, Block-Bootstrap Ø10, Intraday-Bust). Design-Audit (`pipeline-auditor`) vorab, Urteil-Audit (`verdict-auditor`) vor diesem Eintrag; Lauf lokal (Scratchpad 30.08.), Register-Backfill **353 Trials** (Register 15.457 → 15.810).

**Ergebnis — kein Kandidat:**
- **Familien-Null auf der MC-Metrik** (100 Circular-Shift-Ziehungen × alle 100 Varianten, common random numbers): beobachtetes Max innerhalb der Decke, **p = 0,16**. Bester kanonischer Fund der ganzen Schar: **+2,74 pp** — die tage-matched Shift-Placebo-Verteilung einer einzelnen Variante erreicht p95 ≈ **+9,6 pp** (Median ≈ 0).
- **Präspezifizierte Pflichtvariante** (200d-SMA, Level, alle Beine aus unter MA): ΔP **+2,37 pp** (36 M; hätte die 1,5-pp/2×Seed-Schwelle bestanden!), aber: eigener Shift-Placebo **p = 0,25** · **Episoden-Jackknife kippt das Vorzeichen** (ohne die 21 Corona-Tage 2020: +2,37 → **−5,86**, eine Episode trägt 348 %) · **Leave-one-leg-out kippt in 3 von 5 Büchern** (−0,47 / −1,20 / −4,41) · Delay 1→2 Tage: **−61 %** · **Vola-Confound:** matched RV20-Gate mit exakt gleicher Off-Tage-Zahl ist 3× stärker (+6,98 vs. +2,37) — der MA trägt nichts über die Vola hinaus. Zeitpreis: Median 184 → 323 Tage, **P(≤12M) 73,6 % → 49,9 %**, längste Off-Strecke **78 Handelstage** (E8-Aktivitätsproblem).
- **Gegenprobe nach Lehre 10 (#070) bestanden:** invertiertes Gate (über MA aus) ist klar negativ (−10,23 pp bei 36 M, −4,51 bei 120 M) — das Signal ist also nicht richtungslos, es reicht nur nicht über die Decke und ist mechanisch instabil.
- **Breakout-Familie (nur Prämissen-Tafel, `orb_exec=close`, kein Sweep):** alle Zellen negativ; „unter MA" macht Breakouts nur *weniger schlecht* (ES +0,129 CI [0,03; 0,23] signifikant, NQ −0,008, RTY CI über Null) — Multi-Markt-Kontrolle #051 gegen die Prämisse. Der Filter macht aus keinem toten Breakout einen lebenden.
- **Reichweite:** getestet ist „MA-**Tagesmaske** auf diesem Buch" — nicht Regime-Filter generell (Entry-Filter in der Bein-Logik, andere Regime-Quellen, andere Bücher: offen). Deshalb **➖, nicht ❌**.

**Nebenbefund NQ_LastHour_v3 (offen, nicht beerdigt):** Unter-MA-Überschuss real (+27,7 $/Tag, Block-Bootstrap CI95 [11,9; 44,1], 12 von 16 Episoden positiv), aber zu 93 % in 3 Bärenmarkt-Episoden konzentriert und **mit Vola konfundiert** — als eigenständige Prämisse nicht separierbar. Erste Einordnung „Gamma-Prämisse nicht gestützt" wurde vom `verdict-auditor` gekippt (stand auf n=7 Über-MA-Tagen in 2022). Nächster sinnvoller Blick: RV20-Terzile statt MA-Seite, `strategy-auditor` auf die 2022/2025-Konzentration.

**Datenfußnote:** 1d-Parquets ratio-adjustiert, Lauf lief auf dem in #135 reparierten Stand; Regime-Flag gegen unadjustierte 1m-Splices 96-98 % identisch, kein urteilsrelevanter Einfluss.

**Lehren:**
1. **Eine Näherung darf erst ranken, wenn ihre Rangkorrelation zur Entscheidungsmetrik gemessen und > 0 ist.** Die Δθ-Näherung (Drift/Varianz) war zur Zellen-MC **Spearman −0,165** (Vorzeichen 57/100) — die Stufe-A-Auswahl war faktisch adversarisch, der Näherungs-Sieger war der MC-Letzte. Ursache inhaltlich: θ sieht die Intraday-Tail-Asymmetrie nicht, auf die ein Tages-Gate gerade wirkt. Erst der `verdict-auditor` hat das gefangen — die erste Familien-Null (p=0,46) war auf der falschen Größe gerechnet und wurde zurückgezogen.
2. **Für Tages-Gates ist Seed-Streuung das falsche Rauschmaß.** Die Pflichtvariante hätte die Buch-Beitrags-Schwelle „≥1,5 pp und 2× Seed-Rauschen" bestanden (+2,37 bei sd 0,35) und wäre auto-promotet worden; ihr echtes Rauschen (Shift-Placebo) ist ±~5 pp mit p95 ~+9,6. **Offen (Entscheidung Max):** Circular-Shift-Placebo + matched-Vola-Kontrolle + Episoden-Jackknife + LOLO-Vorzeichencheck als Pflichtkontrollen für Tages-/Regime-Gates in `controls.py` codieren; bis dahin gilt die Schwelle für Tages-Gates als nicht kalibriert.
3. **Episoden-artige Signale brauchen Episoden-Statistik:** ~6-16 Unter-MA-Episoden in 10 Jahren, der #057-Epochen-Split ist dafür strukturell ungültig (Epoche 1 fast ohne Off-Tage) — Leave-one-episode-out ist der Ersatz.

Belege: Scratchpad 30.08. (`AR15_nachtrag.json`, `AR15_nachtrag2.json`, `stageB_all100_mc.json`, `stageC_premise.json`, `AR15_lasthour.json`); veraltet/nicht zitieren: `family_null`-Block in `AR15_stageB_results.json`, Ränge in `stageA_results.json`.

## #137 — AP116: Bestands-Durchlauf über alte Urteile (verdict-auditor, 8 Batches), zwei echte Bugs gefunden und gefixt, Queue-Betrieb nebenbei repariert (30.-31.08.2026)

**Auftrag Max (30.08.2026, Ticket AP116):** einmaliger Bestandscheck, ob wir in der Vergangenheit Mechanismen vorschnell für tot erklärt haben (nur 1-2 Varianten statt ≥10, Prior statt Test, Gate-Artefakt) oder Dinge vorschnell für gut/fertig befunden haben. Erwartung laut Ticket: die meisten Urteile halten — Ziel ist die kurze Liste der voreiligen.

**Umfang:** 46 Urteile/Bausteine in 8 Batches durch `verdict-auditor` geprüft — 32 Karten aus dem `ideas.json`-Friedhof, 5 Buch-Bein-Entfernungen/Ablehnungen (NOISE_ORB, OR_DELTA_BIAS, RTY_Gap-fade, ORB-VIX-Band, Coni-VWAP), 4 jüngere Logbuch-Urteile (GEX-Gate, Tempo-Mythen, Exit-Overlay, Skip-Timeout, CVD-Divergenz) und 5 kürzlich für „fertig/läuft" erklärte Pipeline-Bausteine (Gate-Batterie, `job_generator`-Auto-Fill, `promote_next`, `engine-regression-tester` selbst, 24/7-Box-Betrieb).

**Ergebnis: 13 von 46 Urteilen waren voreilig**, 6 weitere halten nur mit Doku-Auflagen (Text zu absolut/veraltet, Kernurteil aber richtig), der Rest (27) hält sauber und wurde nicht weiter dokumentiert (Regel: haltende Urteile nur zählen).

**Die 13 voreiligen Urteile — Begründung + Nachtest/Fix:**

1. **VWAP Mean-Reversion (Z-Stretch)** — Alt-Kill war ein Win-Rate-Vergleich ohne Payoff; moderner Nachtest lief mit Modul-Default k=1,0 (schwache Überdehnung) statt der These „ab STARKER Überdehnung". → `hypothesis_bank.py` AW-09b, Prämisse jetzt explizit auf k=2,0/2,5.
2. **VPIN Order-Flow-Toxizität** — nur 1 Implementierung (#022, 15.07.), nie in den modernen Weg überführt. → keine Job-Empfehlung (Prior niedrig nach #133), sondern eine billige lokale Familienmessung nach Lehre 139, noch offen.
3. **Gap-Fade klein (NQ)** — Friedhofszahl „-14 bis -36%" stammt aus einem Test ohne Bestätigungsachse; Register zeigt 45 NQ-Survivors mit `gap_confirm_min=10`. → Buch-Marginal `NQ_Gap-fade_hf` gegen aktuelles Buch gerechnet (backtest-runner): **schlechter/neutral an den relevanten Tiers** — Ablehnung damit erstmals unter heutiger Methodik sauber bestätigt.
4. **NQ-ES Lead-Lag / RV_leadlag_NQES** — der Tod-Beweis #090 stand auf einer bis 23.08. weiterhin falschen Kostenbasis; die 15 eigens gebauten Nachtest-Jobs (LL01/04/07/14) liefen alle mit n=0 (Prämisse crashte mit `KeyError('rv_thr')`, weil der Wert nur im Grid stand, nie in `base`). → 15 Job-Dateien repariert (Prämisse jetzt als Bracket, neue `_v2`-IDs wegen Register-Ehrlichkeit) und in die Queue eingereiht.
5. **EOD-Konvergenz + Gap-Divergenz (RV)** — `gap_div` stand als „Getötet" in `ideas.json`, war aber nie gewertet: Mini-Risiko-Divisions-Bug in `rv.py` (`risk_d` kollabiert, wenn die Intraday-Bewegung den Overnight-Gap bis Entry zurückholt; reproduziert r=-349 auf Einzeltrades). `eod_conv` (gleiche Karte, anderer `rv_mode`) bleibt tot, gestützt durch #087. → **Bug gefixt** (Design von `quant-mathematician`, Risiko jetzt auf die Trigger-Größe `|gd|` normiert statt auf den kollabierbaren Rest-Zustand; `engine-regression-tester`: 6/6 Referenzfälle + 2/2 Kanarien unverändert, Sync frei). Drei neue Hypothesen RV-08/09/10 (NQ/ES, RTY/ES, NQ/YM) enqueued.
6. **Sizing-Policy-Suche** — Friedhofstext veraltet: #106 fand später mit dem kontinuierlichen Endspurt-Deckel doch einen OOS-haltbaren Sizing-Hebel, der aber unter dem seit #106 geltenden Min-Size-Betriebspunkt inert ist. Echt offen: „Coast-to-Target" (Aussetzen statt Verkleinern) bei Min-Size wurde nie geprüft (`cage_policy_lib.py:316` erlaubt keine Größe 0). Nachtest steht noch aus, kein Job gebaut.
7. **Matteo Coni „Drift VWAP Pullback"** — reines Doku-Problem: `ideas.json` zeigt „Getötet", der Mechanismus lebt seit #096-#101 als Grade-A-Version live im Buch (`NQ_VWAP-Pullback`). → `ideas.json`-Eintrag korrigiert.
8. **OR_DELTA_BIAS_NQ** — größter Einzelfund: nie ein Tod-Urteil über den Mechanismus, sondern eine Buch-Ablehnung (10.08., #079) unter dem seit #106 verworfenen Zeit-Score-Kriterium, Vor-Fix-Engine (AP74/75 bewegten das Buch seither um +16pp) und einem 5-Bein-Buch, das es nicht mehr gibt. Register: 0 Trials unter den heutigen Regeln. → Buch-Marginal (backtest-runner) gegen das aktuelle 4-Bein-Buch gerechnet: **schlechter an fast allen Tiers** (Lehre-82-Muster: höhere Edge/Exposure frisst die Passquote) — die Ablehnung ist damit zum ersten Mal für die LONG-Seite sauber unter heutiger v2-Methodik bestätigt, nicht nur vermutet.
9. **GEX-Buch-Gate** — das „ehrlich beerdigt"-Urteil (#132) ist für die enge Buch-Gate-Frage korrekt, aber zwei Tage später liefen `hyp_GEX01/02` (94 Trials) nirgends dokumentiert nach, und die Gate-Zellen sterben mutmaßlich an einem Trade-Zahl-Artefakt (`top5`/`freq`-Gates skalieren mit der Trade-Zahl, falsche Messlatte für einen Filter). Nachtest: gepaarter Vergleich auf den bereits vorhandenen Ergebnisdateien, noch nicht durchgeführt.
10. **Exit-Overlay tot für Evals** — nur die VERZÖGERNDE Richtung wurde diskutiert/verworfen (0 Register-Trials mit `pb_exit`), eine BESCHLEUNIGENDE Variante (raus auf erster Gegen-Bar) hat das umgekehrte MAE-Vorzeichen und wurde nie gemessen. → Scope-Ergänzung im bereits offenen Ticket `fa01-paired-eval-runner`.
11. **`job_generator.py`-Auto-Queue-Fill** — akut kaputt angetroffen: Queue lief seit 30.08. 07:56 leer, Runner ~12h idle, weil Coverage (130/130 Vorlage×Markt) und alle Follow-ups an Tiefe 3 erschöpft waren — die CLAUDE.md-Aussage „darf nie leerlaufen" beschrieb den Plan, nicht den Ist-Zustand. → `alpha-scout` Runde 6 gestartet (6 neue HF-Mikrostruktur-Jobs, s.u.), Queue außerdem sofort mit den AP116-Nachtests gefüllt.
12. **`promote_next.py`-Automatik** — der #126-Fix (mtime-Check + `verdict==vs_original==besser`) ist im Code belegt, aber seit dem Fix (21.08. 21:16) hat nie eine reale Auto-Promotion mehr stattgefunden (letzte `PROMOTE:`-Zeile 21.08. 20:09, davor). Verifiziert ist nur der Nicht-Fall. Kanarien-Dry-Run (synthetischer Kandidat mit `verdict neutral, vs_original besser`) empfohlen, noch nicht durchgeführt.
13. **„24/7 ohne Pause, BELOW_NORMAL schützt NT8"** — auf der Box gemessen: laufender Runner-Prozess hatte `PriorityClass = Normal`, nicht `BelowNormal`. Die Schutzannahme in der CLAUDE.md war für den tatsächlich laufenden Prozess schlicht falsch. Fix im Start-Skript noch offen (nicht sicherheitskritisch, da Runner aktuell ohnehin oft idle).

**Zusätzlich mit Doku-Auflage bestätigt (Kernurteil hält, Formulierung korrigiert in `ideas.json`/Ticket):** MOC-Imbalanz #087 (Preis-These falsifiziert, Imbalanz-Variable nie geprüft → neue Hypothese TS-21 mit `tm_delta_src="real"` enqueued), Boyarchenko-Overnight-Drift (nur 3 Varianten, Mechanismus nie im richtigen Fenster im Register), RTY_Gap-fade-Entfernung (Buch-Delta war laut #130 neutral, nicht „verbessert"), Payout-Tempo-Mythen (nur Mythos 1 wirklich doppelt belegt), Skip-Timeout (power-limited, nicht falsifiziert — nicht dasselbe wie „tot").

**Nebenbefund von `alpha-scout` Runde 6 (queue_empty-Reaktion):** 11 fertig gebaute Job-Dateien in `jobs_proposed/` (~700 Configs, u.a. `260830_lunch_fade_*`, `260827_gex01/02_*`) wurden nie eingereiht, dazu `CVD-01..05` weiter mit `CVD_ENABLED`-Flag unbenutzt (0 Trials). Der Engpass ist aktuell nicht Ideenfindung, sondern Einreihen selbst — neues Ticket `jobs-proposed-backlog-260831` angelegt, nicht mehr Teil von AP116.

**Was heute Nacht eingereiht wurde:** TS-21, AW-09b, AW-11b, RV-08/09/10 (`hypothesis_bank.py`, letztere drei erst nach dem `rv.py`-Fix und grünem Regressionstest), 15× LL01/04/07/14_v2, 6× alpha-scout-Runde-6 (LQ-01/FB-01/WB-01 auf NQ/RTY/ES) — Queue war leer, ist jetzt wieder gut gefüllt.

**Code-Fixes (beide regressionsgeprüft):** `job_generator.py::mk_job` bekommt jetzt `"gates": dict(HB.GATES_HARD)` (vorher liefen generierte Jobs mit den weicheren Hausdefaults top5 0,60/boot_p 0,85 statt 0,50/0,90 — die 324 bereits fertigen Generator-Jobs bleiben davon unberührt, das ist eine offene Nacharbeit). `rv.py` gap_div-Fix s.o.

**Pipeline-Härtung nebenbei (auf Zuruf von `pipeline-auditor`):** `H()`/`build_jobs()` in `hypothesis_bank.py` haben jetzt ein `hold="Grund"`-Flag — eine zurückgehaltene Hypothese wird jetzt mechanisch übersprungen statt sich auf einen Blockkommentar zu verlassen (der reine Kommentar hätte RV-08/09/10 beim nächsten nackten `--enqueue` trotzdem mitgepusht). Bekannt, nicht gefixt: der Prämissen-Loop in `discovery_runner.py` expandiert `AX_CONFIRM`/`AX_EXITS`-Profile nicht wie der Grid-Pfad (führte zum stillen No-Op bei der ersten TS-21-Fassung, korrigiert auf flache Prämissen-Dicts) — verdient eine dauerhafte Lösung, eigenes Ticket wert. `controls.py::ctl_delay` kennt keinen Delay-Schalter für `mode="rv"` (Look-ahead-Selbsttest überspringt RV-Configs komplett) — relevant, bevor RV-08/09/10 durchlaufen, an `pipeline-auditor` zur Vertiefung übergeben. `golden_masters.json` hat keinen `mode="rv"`-Referenzfall und keine `gap_div`-Kanarie — Empfehlung vom `engine-regression-tester`, noch nicht umgesetzt.

**Lehren:**
1. **Ein Blockkommentar ist kein Gate.** Sowohl die stillen ID-Kollisions-No-Ops (AW-09/AW-11 wären beim Enqueue wirkungslos geblieben) als auch die per Kommentar „zurückgehaltenen" RV-08/09/10 wären ohne den `pipeline-auditor`-Zwischencheck durchgerutscht — Absicht, die nirgends mechanisch durchgesetzt wird, hält nicht. Deshalb jetzt `hold=`.
2. **Ein Tod-Urteil ist nur so aktuell wie die Pipeline, auf der es stand.** OR_DELTA_BIAS_NQ und die Gap-Fade-Ablehnung standen beide auf längst überholten Ständen (altes Kriterium, alte Engine, altes Buch) — das war weder geprüft noch widerlegt, sondern schlicht nie unter den heutigen Regeln nachgerechnet. Derselbe Fund wie in #136 (Lehre 1), nur diesmal am Urteil selbst statt an einer Näherung.
3. **„Getötet" in `ideas.json` ist ein Status für die ganze Karte, nicht für jeden Mechanismus darauf.** Die Karte „EOD-Konvergenz + Gap-Divergenz" hatte zwei Mechanismen mit unterschiedlichem Schicksal unter einem Status — das hat `gap_div` faktisch unsichtbar gemacht für `alpha-scout`, der den Friedhof als Ausschlussliste liest.
4. **Ein Bug, der ein einzelnes Extremergebnis produziert, tarnt sich als Ergebnis, nicht als Fehler.** Der `gap_div`-Bug wurde nie als Bug erkannt, weil r=-349 auf einem einzelnen Trade in einer aggregierten Kennzahl (mean expR) einfach als "schlecht" durchgeht — erst der Blick auf die Verteilung (Top-5-Konzentration, #038-Gate) hätte es früher gefangen, wenn die Karte je gewertet worden wäre.

Belege: `ap116_marginal_recheck.py`/`ap116_marginal_recheck_results.json` (Engine-Ordner, OR_DELTA + Gap-fade Buch-Marginal), `discovery/scout_reports/260831_hf_mikrostruktur.md` (alpha-scout Runde 6), `discovery/golden_masters.json` (Regressionslauf), Scratchpad-Skripte des `quant-mathematician` unter der Session-ID (gap_div-Herleitung + Numerik). Ticket AP116 nach diesem Eintrag gelöscht (Regel: erledigte Tickets löschen, nicht abhaken).

## #138 — Breakout VORHERSAGEN statt hinterherlaufen: 4 Bank-Vorläufer als Prämisse getötet, κ ehrlich vermessen, Pre-Positioning-Mathematik geschlossen (31.08.2026)
Max' Auftrag: die #068-Kaskade (Edge sitzt IN der Ausbruchs-Bar, danach nichts) doch noch ernten — erst die 4 Bank-Vorläufer (AB-14, TB-03, VV-29, VV-57) testen, sonst mathematischer Weg. Werkzeug: `prebreak_precursors.py` (Event-Study auf Prämissen-Stufe, NQ+ES 1m 2016-2026, ~2.600 Tage je Markt) mit First-Passage-Null `MatchedBase` (z=Distanz/(σ·√T) × Tagesminute), Zufallslevel-Kontrolle, Tages-Block-Bootstrap, #057-Epochen-Split. **3 Iterationen nötig** — `pipeline-auditor` fand 4 Blocker (P(A∪B)-gegen-P(A)-Null, Fixwert statt rollierendem λ-Dezil, degenerierte Session-Extreme, tautologischer Range-Puffer), `quant-statistician` erledigte den Rest per Placebo. Volle Kette lief: pipeline-auditor → quant-mathematician + quant-statistician → verdict-auditor.

**Stempel (alle: „Prämisse gescheitert am präregistrierten Kill-Kriterium, KEIN Grid gerechnet" — nicht „Mechanismus-Familie tot"):**
- **AB-14 Berührungszähler ❌:** keine k-Monotonie (k1-k4: 0,365/0,376/0,358/0,317), Verhalten am Zufallslevel identisch, 0/11 Jahre. Weder Erosions-These (Bank) noch Akkumulations-These (Osler 2005) sichtbar. **Achtung:** nur OR30-Level getestet — Oslers Round Numbers/Vortages-Extreme sind damit NICHT widerlegt (nur als Mitnahme in künftigen Level-Jobs prüfen, kein eigener Job).
- **TB-03 Kompression ❌ (eng gestempelt):** kein Vola-Überschuss nach Squeeze — Bewegung danach in ATR-Einheiten KLEINER (NQ 0,274 vs 0,355; ES 0,252 vs 0,354; CI klar getrennt, beide Epochen), ehrlicher ATR-Puffer-Bruch ebenfalls seltener (0,39 vs 0,45). Kompression sagt Kontraktions-Persistenz voraus. **Gilt nur für Intraday-Kompression bis 11:00** — NR7/Tages-Kompression (Crabel-Stretch validiert, ORB-Fade+NR7 im Buch!) ist eine andere, lebende Sache; der Befund BESTÄTIGT das Fade-Bein indirekt. AB-02 (Trend-vs-Fade je Bandbreiten-Quartil) wurde hier NICHT getestet und bleibt offen.
- **VV-29 Absorption ❌:** Richtung via Delta = Münzwurf (0,456/0,49 bei 88% Coverage) → Bank-Kill wörtlich erfüllt. Der Rest-Uplift (+3,1/+2,5pp „nähere Seite bricht öfter") ist **Bin-Artefakt**: Zufalls-Bucket-Placebo durch dieselbe Pipeline liefert MEHR (+3,5/+4,3pp), bei feinen z-Bins enthält jedes CI die Null, saubere Fenster-Null −0,2/+0,4pp, keine Dosis-Wirkung über λ-Dezile. Geschrumpfte Schätzung 0,0-0,3pp. Nebenfund: λ=|ΔP|/Vol wird bei „Bucket schließt auf Open" exakt 0 — bei ES waren 45% der „Absorptions"-Events dieser Degenerationsfall.
- **VV-57 Übergabe-Zone ❌ (nachspezifizierter Kill):** 92,5% Richtungs-Treffer sind vollständig Mechanik — „nähere Seite bricht zuerst" (Null 0,932) erklärt alles, Trend==nähere Seite in 97%. Far-Zelle (Trend zeigt zur ferneren Seite, n=32+40): beobachtet 0,375/0,325 gegen die korrekte Gambler's-Ruin-Null 0,396/0,368 → exakt auf der Null, keine Information. **Nach Bank-Wortlaut („50/50") wäre VV-57 als Volltreffer durchgegangen** — siehe Lehre 1.

**Die Mathematik dazu (quant-mathematician, Formeln gegen MC verifiziert <0,005):**
- **EV-Kernidentität `EV = q_up·κ − C`** (Optional Stopping): der bessere Einstiegspreis beim Pre-Positioning ist im Erwartungswert exakt wertlos — die gesparte Distanz kürzt sich gegen Stops/Zeit-Exits an Nicht-Break-Tagen weg. Einzige EV-Quelle ist die Kaskade κ. Deckel-Satz: `q_up ≤ s/(d+s)` unter Martingal-Dynamik; kein verfügbares Bar-Feature ist ein Drift-Signal (SNR-Satz: aus Lookback < Horizont ist der relevante Drift nicht schätzbar — Approach-Velocity gemessen AUC +0,0000).
- **⭐ κ ehrlich = 0,15·σ_1m** (placebo-kontrolliert, t=5,2, nur IN der Ausbruchsminute; +5min t=2,0, +30min t=0,4). Die #068-Zahl „+6,4 Pkt" ist die Look-ahead-Zahl (Bar-Max) — ehrlich realisierbar sind 2026 ~1,5 Pkt, 2016 ~0,2 Pkt. **Damit ist κ ≥ Kosten nur im 2026-Vola-Regime überhaupt möglich** (5 von 6 Ären bräuchten q_up>1) und dort nur mit s≥2,9·d, was den Intraday-DD (#077) maximal belastet. Diese Zahl gilt ab jetzt für JEDE Level-Strategie-Bewertung.
- **Das Level ist nicht „hart":** empirische Berührungsraten am echten ORB-Level und am Placebo-Level sind deckungsgleich (Ratio-Profile identisch über alle z-Bins). Es gibt keine messbare Barrieren-Härte, also nichts zu erodieren und nichts zu akkumulieren.
- **Einziger Rettungspfad** wäre Slippage-Differenz passiver Limit-Fill vs. Stop-Fill ≥ ~1 Punkt — eine Aussage über UNSERE Ausführung, im Backtest frei wählbar (= #066-Selbstbetrugs-Klasse in der Kostenzeile). Nur mit echten NT8-Fills messbar; bis dahin bleibt Pre-Positioning auf Stufe Prämisse geparkt.
- Einziges echtes Vorläufer-Feature: Bandbreiten-Kompression verbessert die **Varianz**-Prognose (+0,009 CV-AUC, day-clustered CI [+0,006;+0,013]) — Korrektur für V(t,T), kein Richtungssignal, kein Trade.

**Lehren:**
1. **Bank-weit: jedes „Richtung 50/50"-Kill-Kriterium ist wertlos, wo die Geometrie eine andere Null erzwingt.** VV-57 hätte nach eigenem Wortlaut den Weg Richtung Buch angetreten. Jede Level-/Richtungs-Hypothese braucht die mechanische Null (nähere Seite, Gambler's Ruin) explizit im Kill-Kriterium.
2. **Gematchte Nullen sind selbst ein Messgerät und brauchen Kalibrier-Kontrollen:** (a) Bin-Artefakt-Selbsttest (Event-Masse >50% in einem Bin + Hazard-Spread >10pp im Bin → nicht berichten), (b) Zufalls-Event-Placebo durch die identische Pipeline als Pflicht-Arm, (c) Null und Outcome müssen dieselbe Level-Definition messen. Derselbe Fehler kam in EINER Studie zweimal vor (AB-14 −25pp Versatz, VV-29 +3pp Schein-Uplift).
3. **Erste-Passage-Normierung: Plug-in σ²·T ist systematisch falsch** (Faktor 0,7-0,8 Mitte, 5× Tail, weil σ mean-revertiert und Vol-of-Vol konvex eingeht) — Vorwärtsvarianz V(t,T) benutzen.
4. λ-/Aktivitäts-Proxys: Degenerationsfälle (λ==0) abfangen, bevor ein Perzentil-Filter sie als Extrem-Dezil einsammelt.
5. Respezifikationen zählen: 3 Studien-Versionen + ~20 fixe Freiheitsgrade heißt, ein knapp positiver Befund ist per Selektion erklärbar (E[max|H0] ≈ 1,6-1,8pp bei se 0,7) — Kills sind davon unberührt, positive Funde nicht.

**Register:** +24 Trials nachgetragen (4 Hypothesen × 2 Märkte × 3 Spezifikationen, Keys `prebreak138|…`). Belege: `prebreak_precursors.py` + `prebreak_precursors_results.json` (Engine), Statistiker-Parquets (63k Buckets je Markt) im Session-Scratch, Research-Cache-Block „Level-Bruch vor dem Ereignis prognostizieren" (Osler 2005, First-Passage-Lücke, Hawkes, Bollinger-Squeeze-Negativbefund).

**Nachtrag (logbook-distiller, 31.08. abends):** Die 50/50-Falle (Lehre 1) betrifft weitere ungebaute Bank-Zeilen — hart: **MS-18** (Kill sogar 10 pp ZU STRENG, Martingal-Deckel bei R=1,5 ist 0,40), **MS-03**, **VV-21**, **SZ-01**, **TN-01** (als Runner-Job durch ctl_null entschärft, bei Hand-Auswertung nicht); weich (fixe Schwelle statt gematchter Basisrate): MO-56, XA-58, MO-51, LL-03. Muster-Vorbild für richtige Kill-Formulierung: HV-21 (matcht die Geometrie explizit). Alle harten Zeilen in den Bank-Dateien mit ⚠-Marker versehen. Sofort erledigt: λ==0-Guard im Studien-Skript, die 4 Kills nach `ideas.json` zurückgeschrieben (sonst sieht alpha-scout den Friedhof nicht, #137-Lehre-3-Falle). Strukturbefund: `H()` in `hypothesis_bank.py` hat KEIN Kill-Feld — Kill-Kriterien leben nur in den Vault-Tabellen und sind mechanisch nicht prüfbar; Fix (Pflichtfeld `null_ref` + Assert) liegt mit Bin-Selbsttest, Event-Placebo, V(t,T) und ORB-Zufallslevel im Task-Chip „Pipeline-Härtung #138".

**Wo es weitergeht:** Die #068-Frage („Kaskade ernten") ist NICHT beantwortet — beerdigt sind nur diese 4 Vorläufer und das Pre-Positioning ohne Richtungsinfo. Was fehlt, ist ein Vorläufer mit **Richtungsinformation**; ohne die ist selbst +5pp Bruchwahrscheinlichkeit ökonomisch wertlos (Klammer zahlt beide Seiten). Kandidaten-Reihenfolge laut Mathematik: alles, was μ bewegt (nicht σ) — und der Displacement-Befund (#068: +13,6 Pkt bei ≥0,3%/15min) bleibt der einzige belegte μ-Kanal, der lebt schon im Momentum-Bein.

## #139 — AR-17: Vola-Konditional als Tages-Gate — Mechanismus trägt im Modell, ist aber mit diesem Sample nicht auflösbar; Achse geschlossen, drei neue Pipeline-Lehren (31.08.2026)

**Herkunft (deklariert):** Idee stammt aus dem Kontrollarm von AR-15 (#136, RV20-matched schlug dort das MA-Gate) — Selektion auf der Kontrolle, deshalb als eigene Hypothese AR-17 mit eigener Familien-Null getestet. Max' Go nach Empfehlung. Grid vorab fixiert: {RV20, RV5, EWMA λ0,94, VIX} × expandierendes Quantil q70/80/90 (756d Warmup) × beide Richtungen = **24 Varianten** (VXN nicht im Datenbestand), Signale aus t−1, präspezifizierte Hauptvariante RV20|q80|aus-über, volle #136-Batterie, kanonisch 36M/6000 Sims/5 Seeds. Audit-Kette: Lauf → `verdict-auditor` (kippte zwei tragende Belege) → Abschluss-Analytik `quant-mathematician`. Register: **180 Trials** nachgetragen (120 Grid + 60 gematchte Gegenrichtung), n_global ≈ 16.280.

**Die audit-feste Beweiskette:**
- **Hauptvariante RV20|q80** (19,9 % Off-Tage): kanonisch **+7,46 pp** (82,78 → 90,24 %), eigener Circular-Shift-Placebo **p = 0,025** (besteht!), LOLO 5/5 positiv, Delay-2 hält (−7 %), gematchte Gegenrichtung ≈ 0 (Mittel −0,36 pp). Strukturell deutlich sauberer als AR-15 (dort: Placebo p 0,25, LOLO-Kippe 3/5, Delay −61 %).
- **Aber COVID trägt alles:** Episoden-Jackknife-Anteil 1,08 (ohne 2020-Episode −0,58). **COVID-freie Familien-Null über alle 24** (beobachtet UND Null im selben Universum): obs +7,07 vs. Null-Median +5,67, **p = 0,30** (Jackknife-Fenster p = 0,315, ändert nichts). Außerhalb der Krise bleiben +1,4 pp über der Shift-Null — innerhalb ihrer Streuung.
- **Analytik (Zwei-Phasen-First-Passage, #136-Modell):** Off-Schalten einer Hochvola-Klasse hebt P(pass) **gdw r_µ < r_σ²** (äquivalent θ_off < θ_on) — die Drift darf auf Off-Tagen sogar höher sein, sie muss nur langsamer wachsen als die Varianz. Gemessen: r_µ 1,21 < r_σ² 2,26 → erfüllt; Modellvorhersage **+6,7 pp** vs. MC-Messung **+6,63 pp** — der Mechanismus ist kohärent, kein Artefakt. Mechanische Mindest-Hürde für jedes Vola-Gate: **r_σ ≳ 1,16**.
- **Warum trotzdem zu:** COVID-frei bräuchte es zur Beweisbarkeit r_σ ≥ 1,58 (einzeln) bzw. 1,82 (Familie); gemessen 1,47 mit **CI [1,24; 1,88] — überlappt**. Die Daten schließen ein tragfähiges Vola-Gate nicht aus, sie lösen es nicht auf: bindend ist die Zahl unabhängiger Hochvola-Episoden (16-20 in 10 Jahren), nicht die Tageszahl. **Mehr Grid hilft nicht, nur mehr Jahre.**
- **Prämissen-Korrektur (der eigentliche Erkenntnisgewinn):** Das Buch **blutet in Hochvola nicht** — µ_off 29,87 $/Tag **>** µ_on 24,67 $/Tag (auch COVID-frei), signifikant ist allein sd_off/sd_on = **1,50** (CI [1,24; 1,88], P(>1)=1,0). Ein An/Aus-Gate verkauft also Drift gegen Varianz. Die saubere Antwort darauf wäre **vola-skaliertes Sizing** (Drift behalten, Varianz kappen) — unter Min-Size 1 Kontrakt (#106) **nicht ausführbar**, Achse GESCHLOSSEN (nicht „offen"); wieder auf erst bei mehreren Kontrakten je Bein oder feinerer Kontraktgröße.
- v2-Ehrlichkeit: $/funded 181 → 166 nominell besser, aber Median 184 → 268 Tage, P(≤12M) 73,6 → 64,2 % — und genau deshalb entscheidet der COVID-freie Test, nicht die nominelle v2-Zahl.

**Urteil:** ❌ für die konkrete Aussage „Vola-Tages-Gate an/aus über das 5-Bein-Buch, 2016-2026" (kein Buch-Kandidat; Prämisse „Hochvola kostet Drift" positiv falsifiziert). ➖ für den Mechanismus (im Modell gestützt, mit diesem Sample nicht auflösbar). Nicht getestet: vola-skaliertes Sizing (geschlossen wegen Min-Size), per-Bein-Gating, andere Bücher.

**Zurückgezogen (nicht zitieren):** (a) „+5,8 pp mechanischer Zeitpuffer durch Zufalls-Off-Blöcke" — das war der Median des **Maximums über 24 Varianten** (Selektionsstatistik); die echte Per-Varianten-Mechanik von Off-Tagen ist **negativ und monoton** (Shift-Null-Median −0,33 pp bei 20 % Off, −1,47 bei 32 %, bis −44,8 bei 85 %). (b) „Alle 12 invertierten Varianten negativ = Signal trennt" — off-Anteil-konfundiert; bei gematchtem Off-Anteil ist die Gegenrichtung ≈ 0.

**Lehren:**
1. **Placebo pro Variante rechnen; die Max-über-alle-Varianten-Null misst Selektion, nicht Mechanik.** Die Verwechslung erzeugte den falschen „+5,8-pp-Puffer"-Befund, der jeden künftigen Gate-Fund unter +6 pp fälschlich als Artefakt entwertet hätte. Beide Nullen haben ihren Platz: Familien-max-T gegen Multiple Testing, Per-Varianten-Placebo für die Mechanik-Frage.
2. **Off-Tage-Malus-Kurve dokumentiert:** unter dem Trailing-DD-Käfig kostet zufälliges Abschalten monoton (−0,8 pp @ 5 % Off bis −44,8 pp @ 85 %). Jedes Gate muss diesen Malus erst überwinden, bevor es Information beweisen kann.
3. **θ-Vorfilter geschlossen hergeleitet:** ein Tages-Gate kann nur tragen, wenn **r_σ² > r_µ** (Varianz-Spreizung schlägt Drift-Spreizung); mechanische Hürde r_σ ≳ 1,16, Beweisbarkeits-Hürde bei unserem Sample r_σ ≥ ~1,6. Gehört als Vorab-Check in den Job-Bau → in AP117 aufgenommen.
4. Prozess: zweiter Lauf in Folge, in dem der `verdict-auditor` tragende Zahlen gekippt hat (hier: beide „Ersatz-Belege" des Rechners), bevor sie ins Logbuch gingen. Die Kette Design-Audit → Lauf → Urteil-Audit → Analytik-Abschluss hat sich als Standard bewährt.

Belege: Scratchpad 31.08. (`AR17_stageA.json`, `AR17_full.json`, `AR17_abschluss.json`, `AR17_theta_covid.json`, `AR17_va_check.json`, Skripte `ar17*.py`, `va_check*.py`); Hypothese: [[Hypothesen-Bank (Momentum & Averages)]] AR-17.

## #139 — 🚨 Pipeline sucht seit 23.08. pro forma: kein Modus außer tsmom/maband/orb kann deploy_ready werden, Referenzbuch schlechter als sein Subset, 3 begrabene TE-Funde (01.09.2026)
Anstoß: alpha-scout hatte in Runde 5 UND 6 denselben Verdacht angemahnt („Survivors mit sauberem PBO, aber seit 21.08. produziert kein Job mehr Kandidaten") — nie geprüft. Regel „Null-Ergebnis = Verdacht" griff, `pipeline-auditor` hat den Trichter zerlegt: **seit 25.08. 167 Jobs · 9.010 Grid-Zellen · 699 Survivors · 289 Buch-Evals · 0× „besser" · 0 deploy_ready.** Kein Rechenfehler — drei strukturelle Löcher:

- **B1 — Modus-Loch:** `controls.py` (ctl_delay/ctl_null) kennt nur `tsmom`/`maband`/`orb`. Jeder andere Modus (rv, gap, cal, ts_reversal, asian) → `ok=None` → `skipped_required` → **kann NIE deploy_ready werden**, egal wie gut er rechnet. Der komplette LL-Batch (mode rv) war per Konstruktion chancenlos. Verschärfend: die Skip-Meldung aus dem 30.08.-Fix feuert nur bei `is_cand=true` — der Skip ist also stumm.
- **B2 — Referenzbuch kaputt:** Leave-one-out zeigt das 5-Bein-Buch (82,97 %) ist schlechter als sein bestes 4-Bein-Subset ohne `NQ_LastHour_v3` (87,25 %; LastHour −4,3 pp, VWAP-Pullback −3,1 pp). **Alle Marginals messen gegen die kaputte Basis** — derselbe LL04-Kandidat: +0,8 pp (neutral) gegen das volle Buch, +2,7 pp (Kandidat!) gegen das gestutzte. Für Subtraktionen gibt es keinen Job-Typ. Vorbehalt: der Scan war In-Sample, Streichung braucht nested OOS (Ticket `buch-komposition-lasthour-260901`).
- **B3 — Weg „neues Bein" hat NIE funktioniert:** 577 Buch-Evals mit `replaces_leg=None`: Median −12,3 pp, Max +0,8 pp, 0 Treffer jemals. Alle 14 Kandidaten-Jobs der Historie waren Ersatz/Exit. Spearman(Buch-Score, Trades/Jahr) = **−0,81** — der HF-Fokus des `job_generator` klettert exakt den Hang hoch, den die v2-Zielfunktion bestraft (Lehre 82/#079).
- **B4 — 3 begrabene Funde:** `hyp_TE02/TE04/TE15_NQ` (23.08., +2,5 bis +4,9 pp Buch, vs Original +4,4 bis +6,8 pp) starben am corr_book-Bug, der am **24.08.** gefixt wurde — nie neu gerechnet. Seit 23.08. 18:34 hat kein Config mehr „Buch besser" erreicht. **Sofort behoben: als `hyp_TE0x_NQ_v2` mit korrektem `replaces_leg` neu eingereiht (01.09.).**
- **B5 — Stiller No-Op:** `replaces_leg="NQ_Momentum"` matcht nicht (Buch-Bein heißt `NQ_Momentum_d260818`) → 39 Läufe rechneten „Buch + Duplikat". 84 von 138 Ersatz-Jobs in der Queue tragen tote Bein-Namen. Kein Assert.
- **B6 — Mess-Schiefen:** Rauschmaß `hypot(sd1,sd0)` trotz gemeinsamer Seeds (Schwelle auf 1,8-2,2 pp aufgebläht, 35 Evals im Graubereich); `null_ceiling` nimmt `sr_std` des Jobs statt der Theorie (Decke SR 13,08 statt ~1,35 — eine Zufallsvariable als Nullverteilung).

**Sofort umgesetzt (01.09.):** 14 liegengebliebene validierte Jobs eingereiht (Box war leergelaufen; Scout-Runde-6-Mikrostruktur + 27.-30.08.-Backlog, ~700 Configs, 12 davon tsmom/maband = voll deploy-fähig), TE-v2-Re-Runs eingereiht, CVD bewusst NICHT (Grabplatte `CVD_ENABLED=False`, Reaktivierung nur auf Max' Ansage — Scout-Empfehlung war stale), Backlog-Ticket gelöscht, 2 neue Tickets: `buch-komposition-lasthour-260901` (Wochenende, nested-OOS-Streichungs-Prüfung) und `pipeline-fixes-139-260901` (Modus-Zulassungs-Gate, replaces_leg-Assert, gepaartes Rauschmaß, ehrliche Decke).

**Nachtrag B7 (01.09. abends):** Beim Re-Run der TE-Funde ist ein viertes Loch aufgeflogen — **`queue.json` hat ein Lost-Update-Fenster**: `inbox_tool --add-job` pusht die Queue auf die Box, aber ein Runner, der gerade mitten in einem Job steckt, schreibt am Job-Ende seine ältere In-Memory-Version zurück und löscht damit still alle zwischenzeitlich angehängten Jobs (die 3 TE-v2-Jobs verschwanden spurlos, das Runner-Log hat sie nie gesehen; die 14 Batch-Jobs überlebten nur, weil ihr Push ins Idle-Fenster fiel). Bis zum Fix (Runner muss beim Zurückschreiben unbekannte Job-IDs mergen statt überschreiben, siehe Ticket): **Einreihen nur, wenn der Runner idle ist**, und nach jedem Push auf der Box verifizieren, dass die IDs wirklich in der Queue stehen.

**Lehren:** (1) Ein Modus ohne Delay-/Null-Schalter darf gar nicht erst in die Queue — Zulassungs-Gate beim Job-Bau, nicht stille Nicht-Deploy-Fähigkeit im Runner. (2) Das Referenzbuch selbst braucht eine wiederkehrende Kompositions-Prüfung (Leave-one-out als Pipeline-Stufe); „Bein raus" muss ein erzeugbares Ticket sein, nicht nur „Bein rein/ersetzen". (3) Namens-Referenzen auf Buch-Beine (replaces_leg) brauchen ein Existenz-Assert — ein Tippfehler/Umbenennung wird sonst zum stillen Duplikat-Vergleich. (4) Wenn ein Gegenleser (Scout) denselben Verdacht ZWEIMAL meldet, ist das kein Rauschen — der Verdacht hätte am 30.08. geprüft gehört, nicht am 01.09.

## #140 — Zwei neue Pipeline-Agents (`variant-scout`, `strategy-auditor`-Batch-Modus) — erster Lauf fängt MS-61 vor jeder Box-Zeit ab, dazu ein stiller Engine-Bug gefunden (01.09.2026)

Max' Frage: prüft sich die Pipeline eigentlich selbst genug — Discovery → Testarten → Rechnen — oder fehlt eine Stelle? Antwort: die Kette hatte bereits `verdict-auditor`/`strategy-auditor` NACH dem Rechnen, aber keinen Check auf die ökonomische Story VOR dem Rechnen. Zwei Bausteine gebaut statt eines dritten Auditors:

1. **`variant-scout`** (neuer Subagent, `.claude/agents/variant-scout.md`, opus): vermisst zu jeder neuen Hypothese, in wie vielen ECHTEN Arten sie testbar ist (gegen `AX_CONFIRM`/`AX_RISK`/`AX_EXITS` und die bestehende Bank), bevor sie als Zeile/Job geschrieben wird. Trigger in CLAUDE.md verdrahtet.
2. **`strategy-auditor`-Batch-Vorprüfung** (neuer Modus in der bestehenden Agent-Datei, kein neuer Agent — Max' ausdrücklicher Wunsch, keine Opus-Kosten pro Einzelhypothese): EIN Call über eine ganze Gruppe frischer Hypothesen, reine Story-Prüfung (Why kausal? Look-ahead im Text? Familie eindeutig? zu gut um wahr zu sein? Kontamination mit Friedhof?), direkt nachdem `variant-scout` eine Gruppe als testbar einstuft — bevor Box-Rechenzeit für Configs verbrannt wird. Der bisherige Vollmodus (nach dem Backtest, vor Eval-Deploy) bleibt bestehen.

**Erster echter Lauf, aus der Volume-Informed-Trading-Recherche (10 Papers, `research-scout`) desselben Tages:** drei Kandidaten (Amihud-ILLIQ, Chan/Fong-Order-Imbalance, López-de-Prado-Volumenbars) durch `variant-scout` — nur einer (Chan/Fong) war ein echter neuer Mechanismus, als **MS-61** in die Bank geschrieben. Die Batch-Vorprüfung direkt danach: **MS-61 fällt durch, trotz „testbar, keine Engine-Lücke"-Einstufung von `variant-scout`.**

**Warum, konkret:**
- `tm_rvol_min`/`tm_delta_min` greifen nur im `tsmom`/`maband`-Pfad (`sigcore.gates_pass`); alle 10 als Basis genannten VV-Zeilen laufen aber auf `qbt`-Modi (orb/ts_reversal/fomc/vwap_pullback/rv/calendar) — die geplante Kreuztabelle war für keine einzige davon baubar. `variant-scout` hatte die Achse als ✅ eingestuft, aber nur gegen die AX_*-Definition geprüft, nicht gegen die tatsächlichen Modi der zehn Basis-Zeilen.
- `sigcore.delta_proxy` misst volumengewichtete Bar-Richtungs-Konsistenz, nicht Order-Imbalance — bei gleichem Signal-/Entry-Fenster mit dem Entry-Signal selbst konfundiert.
- Chan/Fong (2000) belegt die Volatilitäts-, nicht die Richtungs-Beziehung — das Why trug die Messgröße „Edge-Differenz" nicht.
- Verwandte Delta/CVD-Familie ist bereits zweimal beerdigt (#021, #133, „Reaktivierung nur auf ausdrückliche Ansage") — bei `variant-scout`s Verwandtschafts-Check als reiner ID-Overlap-Check übersehen, weil MS-61 Delta als Konditionierung statt als Richtungssignal nutzt.
- Chan/Fong (2000) stand ungeprüft im Why, ohne Research-Cache-Eintrag.

**Nebenbefund (Engine-Bug, nicht MS-61-spezifisch):** `tm_delta_src` kommt in `sigcore.py` kein einziges Mal vor — wer `tm_delta_src="real"` UND `tm_delta_min` gleichzeitig setzt, bekommt still ein Proxy-Gate statt eines Real-Delta-Gates, ohne Fehler und ohne Log. Betrifft bestehende Jobs, u.a. `hypothesis_bank.py` Z. 283 und 1548 (TS-21 aus #137 nutzt genau diese Kombination). Als Session-Chip an Max geflaggt, noch nicht gefixt.

**Vault-Korrekturen:** MS-61-Zeile in [[Hypothesen-Bank (Volumen & Flows)]] auf durchgefallen umgestempelt (🔧 statt ✅, Fix-Pfad in 4 Schritten notiert), Übersichtstabelle/Familien-Zähler zurückkorrigiert, VV-13 um die Dollar-Bars-Achse ergänzt (López de Prado stützt die Prämisse, kein neuer Eintrag), λ-Proxy-Baustein-Notiz um die Amihud-Formel-Parameter-Empfehlung + #138-Warnung ergänzt.

**Lehren:**
1. **„Engine-Status ✅" ohne Gegenprobe an den tatsächlich genannten Basis-Zeilen ist eine Falle.** `variant-scout` prüfte die Achsen-Existenz gegen die AX_*-Definitionen, nicht gegen die Modi der zehn konkret genannten VV-Zeilen — ein Fehler, der sich mit einem Grep pro Basis-Zeile vermeiden lässt. Rollendatei entsprechend nachschärfen (Achsen-Check muss den Modus JEDER genannten Basis-Zeile einzeln bestätigen, nicht nur die Achse abstrakt).
2. **Batch-Vorprüfung zahlt sich beim ersten Lauf sofort aus:** eine Hypothese, die als „sofort testbar" durchgewunken worden wäre, wäre auf der Box gelandet, bevor der Fehler auffiel — Kosten wären nicht riesig gewesen (ein Job), aber der Bug-Fund (`tm_delta_src`) hätte sich sonst gar nicht gezeigt, weil niemand die Konfundierung im Text geprüft hätte.
3. **Der Verwandtschafts-Check von `variant-scout` braucht eine explizite Friedhofs-Grep-Pflicht**, nicht nur „gibt es eine Bank-Zeile mit ähnlicher ID/ähnlichem Titel" — #133 wurde nur gefunden, weil `strategy-auditor` im Vollmodus zusätzlich das Logbuch durchsucht hat.

Folge-Ticket (noch nicht angelegt, siehe Session-Chip): `tm_delta_src`-Silent-Fallback fixen, `variant-scout`-Rollendatei um Punkt 1 schärfen.

## Nächste Kandidaten (noch offen)
- ~~Replace-Test: NQ_Momentum → MOMSEL_NQ_er0.3_s0.75~~ → in #080 ehrlich neu gerechnet: nur bei frac ≈0.10 sinnvoll; in #095 endgültig erledigt (Momentum ist im Leave-one-out neutral, bleibt drin) — **in #108 unter v2/Min-Size wieder aufgemacht als AP101** (nicht mehr als Buch-Frage, sondern als Vola-Senkung bei erhaltener Drift)
- ~~Momentum selektiver~~ → in #057 getestet, NQ 8/8 robust (siehe oben)
- ~~Intraday Time Series Reversal auf Index (SSRN 5807282)~~ → in #056 als on_rev/min30-Variante mitgetestet (eod-Variante war stärker)
- Overnight-Intraday Reversal (SSRN 2730304)
