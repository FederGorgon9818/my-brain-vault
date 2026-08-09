---
tags:
  - bereich/trading
  - trading/live
erstellt: 2026-07-21
---
# 🚀 Live-Setup: Portfolio automatisiert auf Prop-Firm

⬅️ [[Day Trading]] · [[Eval-Passing]] · [[Portfolio-Simulator]]

> [!tip] Ziel
> Das 5-Bein-Buch (`PORTFOLIO_optimized`: NQ Momentum · NQ Power-Hour · NQ ORB-Breakout · NQ ORB-Fade · RTY Gap-Fade) automatisiert auf einem Eval → Funded fahren. Algo erlaubt, EOD-Drawdown, aus Deutschland handelbar.

## 1️⃣ Regel-Lage (Stand Juli 2026, vor Kauf IMMER neu prüfen!)

| Firma | Algo erlaubt? | Bedingungen | DD-Typ |
|---|---|---|---|
| **MyFundedFutures (MFFU)** | ✅ seit Juli 2025 auf ALLEN Konten | semi-auto, aktiv beaufsichtigt, <200 Trades/Tag, keine Sim-Exploits | je nach Plan EOD-Trailing (Core/Pro), Static-Variante prüfen (Flex/Builder) |
| **Tradeify** | ✅ persönliche Bots | Bot gehört NUR dir (kein gekauftes/geteiltes System!), Video-Nachweis vom Start auf deinem PC, kein HFT, >50% der Trades & Profite aus Trades >10s Haltezeit | Lightning = **EOD-Trailing** (nicht static!) |
| Apex | ❌ kein Algo | — | — |
| Topstep | ⚠️ restriktiv | — | — |

**Unser Buch erfüllt alles locker:** ~2 Trades/Tag (nicht 200), Haltezeit Minuten bis Stunden (nicht 10s), 100% selbstgebaut (Backtest-Beweise im Lab), läuft beaufsichtigt während RTH.

> [!warning] Static-DD-Realität
> Reine Static-DD-Futures-Konten sind rar. Unsere Frontier: Static 63%/~45d vs. EOD-Trailing 54-58%/43-70d (frac 0.18-0.22). EOD-Trailing ist immer noch gut (unsere ganze EOD-Rechnung gilt), Static wäre +5-9 Punkte Bonus. Beim Kauf checken: propfirmmatch.com → Filter "Static Drawdown" Futures.

## 2️⃣ Setup-Optionen im Vergleich

| Setup | Pro | Contra | Urteil |
|---|---|---|---|
| **A: NinjaTrader 8 + NinjaScript (C#) auf Tradovate-Konto** | Offiziell von MFFU/Tradeify unterstützt (Login mit Tradovate-Credentials) · Bot läuft lokal auf DEINEM PC (= exakt Tradeify-Regel) · robuste Order-Engine: OCO-Brackets, Auto-Flat-Zeiten, Sim/Playback zum Validieren · Plattform kostenlos | 5 Strategien nach C# porten (mach ich) · NT8-Einarbeitung | ⭐ **EMPFEHLUNG** |
| B: Python direkt auf Tradovate REST/WebSocket-API | Kein Port nötig, volle Kontrolle, qbt-Logik 1:1 | API-Zugang auf Eval-Konten grau/firmenabhängig · Reconnects, Rate-Limits (500 req/min), Order-Safety alles selbst bauen · mehr Fehlerquellen am Anfang | Stufe 2 (auf Funded) |
| C: TradingView + PickMyTrade/TradersPost (Webhooks) | No-Code-Brücke, MFFU erlaubt TradersPost explizit | Logik müsste nach PineScript (= gleicher Aufwand wie C#, schlechtere Engine) · Drittanbieter + Monatskosten + Webhook-Latenz | ❌ unnötig, du kannst coden |
| D: Rithmic-Route (Sierra/Quantower/async_rithmic) | Alternative wenn Rithmic-Konto | C++/ACSIL bzw. Nischen-Python-Lib, mehr Reibung | nur falls Konto Rithmic-only |

**Warum A:** Es ist der einzige Weg, der gleichzeitig (1) offiziell supported ist, (2) die "persönlicher Bot auf eigenem PC"-Regel wörtlich erfüllt, (3) eine kampferprobte Order-Engine mitbringt statt Marke Eigenbau am echten Geld.

## 3️⃣ Die Anleitung (Schritt für Schritt)

### Phase 0: Konto & Plattform (1 Tag)
1. **Firma wählen:** MFFU oder Tradeify, 50k-Eval, **Tradovate-basiertes Konto wählen** (nicht Rithmic! Nur Tradovate verbindet mit NinjaTrader). Vor Kauf: aktuelle Algo-Policy + DD-Typ im Help-Center lesen, bei Static-Angebot Static nehmen.
2. **Bei Tradeify:** Video vom Bot-Start auf deinem PC aufnehmen können (Regel), Bot-Ownership dokumentieren (haben wir: ganzes Lab + Logbuch als Beweis).
3. **NinjaTrader 8 Desktop** installieren (kostenlos), mit den Tradovate-Credentials des Prop-Kontos verbinden. Marktdaten (CME Bundle) kommen übers Konto.

### Phase 1: Port der 5 Beine nach NinjaScript (Claude macht das)
4. Jedes Bein wird eine eigene NT8-Strategie (C#), Parameter exakt aus `asset_legs.json`:
   - Entry/Stop/Target/EOD-Exit identisch zur qbt-Engine
   - OCO-Bracket bei Entry (Stop + Target atomar)
   - Auto-Flat 15:55 ET (Notausgang Zeit)
5. Dazu ein **Risk-Guard** (NT8-AddOn): Cushion-Sizing (frac 0.18-0.22 → Kontrakte/Tag aus aktuellem Cushion), Tages-Verlustgrenze, Kill-Switch, Trade-Log als CSV (füttert später das Lab).

### Phase 2: Sim-Validierung (2-4 Wochen, NICHT überspringen)
6. Strategien auf **NT8 Sim-Konto** laufen lassen (Live-Marktdaten, simulierte Fills).
7. Wöchentlich: Sim-Trades vs. qbt-Backtest abgleichen (Win-Rate, expR, Slippage). **Regel: erst wenn der Tracking-Error klein ist (Sim ≈ Backtest ±20% auf expR), fließt Geld.** Wenn Sim deutlich schlechter: STOPP, Ursache finden (Fills? Zeiten? Bug?).

### Phase 3: Eval live (Ziel: ~45-70 Tage)
8. **1 Eval** starten (nicht 5 parallel — erst beweisen, dann skalieren).
9. Betriebspunkt: **frac 0.22** (Entscheid 29.07., 52%/~45d — RiskGuard CushionFrac 0.22 setzen!) laut [[Portfolio-Simulator]]-Frontier.
10. Betrieb NUR während RTH und nur wenn du erreichbar bist (Aufsichts-Regel + gesunder Menschenverstand). PC an, NT8 an, Strategien enabled, Disconnect-Schutz: NT8 "Auto-flatten on disconnect" aktivieren.
11. Jeden Abend: Trades ins [[Strategie-Logbuch]] (automatisch via CSV), einmal pro Woche Review: läuft das Buch im erwarteten Band?

### Phase 4: Funded
12. Nach dem Pass: **Consistency-Regel beachten** (Tradeify: 20% → 25% → 30% je Payout; MFFU planabhängig, Flex funded ohne Consistency). Heißt: kein Einzeltag > X% des Gesamtprofits → unser Portfolio mit vielen kleinen Tagen passt da gut rein, aber wir simulieren das noch (nächster Schritt im Lab).
13. Payout-Kadenz klein und regelmäßig (90% Split, Caps beachten).

> [!danger] ⚠️ VPS-VERBOT bestätigt (27.07.2026, Bulenox-Ticket #RAX-292098)
> **"The use of any VPN, VPS, proxy, or IP-masking technology is strictly prohibited"** — Verstoß = Kündigung + Verfall aller Rewards. Recherche zeigt: auch bei Apex/MFFU ist VPS mindestens genehmigungspflichtig; Datacenter-IPs sind branchenweit das Misstrauens-Signal.
> **Neuer Plan: HOME-TRADING-BOX** (Mini-PC/alter Laptop bei Max daheim, Wohnsitz-IP = überall regelkonform). Bulenox-Käfig bleibt erhalten. Einrichtung identisch zum VPS (Tailscale, NT8, Bridge, Sync) — Anleitung [[VPS-Einrichtung Schritt für Schritt]] gilt sinngemäß, nur ohne Contabo-Teil. VPS wird nach Migration gekündigt. Fernaufsicht per RDP/Tailscale bleibt (maskiert die Trading-IP nicht — NT verbindet von der Heim-IP).

## 🖥️ Betrieb ohne eigenen PC (VPS) — ⚠️ OBSOLET, siehe Warnung oben

**Wichtig zuerst:** Das 6-Bein-Buch handelt NUR die US-Session = **15:30-22:00 deutscher Zeit** (alle Nacht-Strategien wurden ehrlich gekillt). Es gibt keinen 3-Uhr-nachts-Bedarf.

**Stufenplan (Entscheidung 21.07.: direkt VPS, weil Max wegen Job um 15:30 nicht am PC ist und der Arbeits-PC frei bleiben muss):**
1. **Ab sofort (Sim + Eval): Contabo Cloud VPS, US-Central (St. Louis), 4-6 vCPU / 8-12 GB / NVMe + Windows-Server-2022-Addon → ~€15-20/Mon. gesamt.** (Vultr fällt raus: Windows $16/Core. Hetzner: kein offizielles Windows.)
   Einrichtung: RDP → PW ändern → Updates → **Tailscale + Port 3389 öffentlich zu** → Nutzungszeit 14-23 Uhr (keine Update-Reboots in der Session) → NT8 installieren + Autostart + Auto-Flat bei Disconnect → Reboot-Test → "Windows App" auf dem Handy für RDP-Aufsicht. Sim läuft damit schon auf der späteren Live-Infrastruktur = ehrlichere Validierung.
2. **Ab erstem Funded-Payout:** optional auf QuantVPS Lite upgraden ($59.99/Mon., $41.99 jährlich, Coupons ~30%) für managed Betrieb. NICHT die teuren Low-Latency-Pläne ($99+) — Minuten-Strategien brauchen keine Latenz.
3. **Stufe 2 (Funded, bewiesen):** Python-Executor auf Linux-Server via Tradovate-API (billiger + robuster).

**Alltag mit Job:** 15:30 US-Open → Telegram-Push bei jedem Fill (Kaffeepausen-Blick = Aufsicht), abends RDP-Check vom Handy/Laptop. Arbeits-PC bleibt unberührt.

**Pflicht-Sicherheitsnetz (unabhängig vom VPS):**
- Tradovate-seitige Risk-Limits / Auto-Liquidation (greift auch wenn der VPS stirbt)
- NT8 "Auto-Flat bei Disconnect"
- Risk-Guard mit **Telegram-Push-Alerts** (Fills, Tageslimit, Disconnect) → Aufsicht in der Hosentasche

**Regel-Haken:** MFFU/Tradeify = beaufsichtigte Automation, KEIN unbeaufsichtigter Vollautomat. Handy-Alerts + erreichbar sein = ok. Tradeify verlangt "Bot auf eigenem PC + Video" → **vor Kauf beim Support schriftlich klären, ob VPS ok ist** (üblich, aber absichern).

## 🔀 Netting-Konto & mehrere Beine auf MNQ (gemessen 30.07.2026)
Prop-Konten sind **Netting** (eine Netto-Position pro Instrument, kein gleichzeitig long+short). 6 der 9 Beine handeln MNQ, ORB-Break vs ORB-Fade sind sogar per Design gegenläufig. **Messung:** an 15% der Tage stehen sich zeitweise Beine gegenüber, aber nur **2,6% der Brutto-Exposure** wird real weggenettet (Beine handeln meist zu verschiedenen Zeiten oder an Trendtagen gleichgerichtet).
- **Sonderfall Bein 8+9 (beide ORB-Vol-Scalp, 30.07.):** identischer Entry, unterschiedliches Target (1,0R vs 0,5R) → **kein Netting-Konflikt möglich**, da immer gleiche Richtung (Scale-Out-Charakter). Zählt nicht in die 2,6%-Messung, ist aber strukturell der sauberste Fall.
- **Bewertung:** kein Blocker. 2,6% Drag liegt in der Sim-Toleranz (±20% expR). Kosten fallen auf weggenettete Trades trotzdem an → Live minimal < Backtest-Summe.
- **Echter Stolperstein = NT8-Order-Handling:** bei gegenläufigen Strategien auf einem Konto können sich Stop/Target-Orders auf die Netto-Position beziehen. **Phase-2-Sim (auch Netting) deckt das auf** — Sim-vs-Backtest-Tracking beobachten.
- **Saubere Lösung (optional, später):** Signal-Aggregator = eine Master-Strategie, die alle MNQ-Signale zu einer Netto-Zielposition + einem Stop-Set bündelt. Bei 2,6% Drag nicht dringend.

## 4️⃣ Ehrliche Erwartung (wichtig gegen Frust)
- P(pass) 54-63% heißt: **~40% Chance, dass Versuch 1 scheitert.** Das ist einkalkuliert: Budget für 2-3 Evals einplanen, dann ist die Gesamt-Passchance >85%.
- Sim-Fills ≠ echte Fills. Deshalb Phase 2. Erwarte, dass Live 10-20% unter Backtest liegt.
- Regeln der Firmen ändern sich ständig → vor jedem Kauf Help-Center lesen, nicht Blogs.

## 📚 Quellen (Juli 2026)
- [Tradeify Guidelines for Traders](https://help.tradeify.co/en/articles/10468318-guidelines-for-traders) (Bot-Regeln, 10s-Regel)
- [MFFU Fair Play / Prohibited Practices](https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices)
- [MFFU erlaubt Algo/Automation (Juli 2025)](https://www.quantvps.com/blog/myfundedfutures-now-permits-algo-trading-and-automation-tools-on-all-accounts)
- [Tradeify Supported Platforms](https://help.tradeify.co/en/articles/10468221-supported-platforms) (NT/TradingView nur via Tradovate)
- [Tradeify Consistency Rule](https://help.tradeify.co/en/articles/10468320-rules-consistency-rule)
- [Tradovate API](https://api.tradovate.com/) (Stufe 2)
- [Static-DD-Firmen-Liste](https://propfirmmatch.com/futures/prop-firm-lists/challenge-types/static-drawdown)
