---
tags:
  - ressource/trading
  - trading/alpha
  - trading/mikrostruktur
erstellt: 2026-08-21
quelle: research-scout (Web + Research-Cache), Auftrag Max 21.08.2026
---
# 🏦 Institutionelle Order-Execution im Futures-Markt (Theorie)

⬅️ [[Alpha-Suche]] · [[Idee-Generierung (wie Institutionen)]] · [[Research-Cache]]

> [!important] Zweck
> Reine Theorie, keine Strategie: **wie bringen große Marktteilnehmer (Hedgefonds, Asset Manager, Banken, CTAs, Dealer) Positionen in ES/NQ & Co., und welche Spur lässt das in Preis, Volumen und Zeit?** Grundlage für das *Why* vor jeder neuen Alpha-Hypothese (Edge-Quelle „Structural" + „Informational"). Belege mit Quelle im [[Research-Cache]] (Sektion 21.08.2026). Offener Faden dazu: Volumen horizontal/vertikal als Signal, siehe [[Alpha-Suche]].

## 1. Metaorders: wie eine große Order wirklich in den Markt kommt

**Mechanismus.** Eine institutionelle Order (Metaorder) ist fast immer zu groß fürs Orderbuch. Sie wird in viele Kinderorders zerlegt und über Minuten bis Tage gestreckt. Almgren/Chriss (2001) formalisieren das: schnell = viel Market Impact, langsam = viel Timing-Risiko (Preis läuft weg). Daraus die Standard-Algos:
- **TWAP**: gleichmäßig über Zeit.
- **VWAP**: proportional zum erwarteten Volumenprofil des Tages (U-Form: Open + Close schwer).
- **POV / Participation**: feste Quote am laufenden Marktvolumen (typisch 5-20 %).
- **Implementation Shortfall**: front-loaded, wenn Dringlichkeit hoch ist.

**Spur.** Gestrecktes, erhöhtes Volumen über die Dauer der Ausführung; Preisdrift in Ausführungsrichtung. Der Impact folgt dem **Square-Root-Law**: Impact ∝ √(Q / Tagesvolumen), nahezu unabhängig von Dauer und Stückelung. Für Futures empirisch bestätigt (Bershova/Rakhlin 2013). **Belegt.**

**Impact-Decay.** Nach Ende der Metaorder fällt der Preis teilweise zurück. Alte Sicht (Farmer et al. 2013): ~2/3 bleibt permanent. Neue Sicht (Bucci et al. 2019, ANcerno): Power-Law-Zerfall über Tage, konvergiert erst nach ~50 Tagen gegen ~1/2. **Belegt, aber Zeitskala umstritten**, nur US-Aktien, keine Futures-Studie.

**Wichtig fürs Verständnis von Volumen:** Ein VWAP-Algo *erzeugt* Volumen dort, wo er Volumen erwartet. Volumen-Spitzen am Open/Close sind deshalb zum großen Teil Selbstverstärkung der Algos, nicht neue Information. Vertikales Volumen (pro Zeit) ist damit nur relativ zum erwarteten Tagesprofil aussagekräftig (RVOL-Logik), nicht absolut.

## 2. Wer MUSS handeln, wann (vorhersagbare Flows)

| Akteur / Flow | Mechanismus | Spur | Beleg |
|---|---|---|---|
| **Pension-/Asset-Manager-Rebalancing** (Monats-/Quartalsende) | Aktien-/Anleihen-Quote wird kalendarisch zurückgesetzt; nach starkem Aktienmonat Verkauf ES/NQ, Kauf ZN/ZB | Sichtbar in CFTC-Positionsdaten; Preiseffekt bis ~17 bp am Folgetag, **temporär** | Belegt (NBER, Harvey et al.) |
| **Risk-Parity / Vol-Targeting** | Positionsgröße ∝ 1/Vola; Vola-Schock → mechanischer Abbau über Tage | Verstärkt Abwärtsbewegungen nach Vola-Sprung, verteilt über mehrere Sessions | Plausibel, Firmen-Schwellen proprietär |
| **CTA-Trendfolger** | Regelbasierte Trend-Signale, Vol-Targeting; Trigger firmenintern | Verstärken Trends, eher Front-Running als Arbitrage; Crowding-Kapazitätsgrenze empirisch **nicht** nachweisbar | Belegt für Crowding-Frage, **Folklore** für konkrete Trigger-Level |
| **Futures-Roll** (ES/NQ) | Roll-Datum = Montag vor 3. Freitag (H/M/U/Z); Volumen + OI wandern Front → Back | CME Quarterly Roll Analyzer zeigt es live; Calendar-Spread-Handel, nicht Outright | Belegt (Exchange-Doku) |
| **MOC / Closing-Auction-Imbalance** | NYSE veröffentlicht Imbalances ab 15:50 ET; Futures-Arbitrageure stellen gegen Kassa-Imbalance Liquidität | Verknüpfung zu ES-Preis nur in einem Working Paper; eigener NQ-Test tot ([[Strategie-Logbuch]] #087, 0/72) | **Dünn**, LETF-Mechanismus selbst umstritten (Cheng/Madhavan vs. Ivanov/Lenkey) |
| **Dealer-Gamma-Hedging** (0DTE, OpEx, GEX, Charm/Vanna) | Dealer hedgen Options-Bücher delta-neutral; Netto-Gamma bestimmt, ob Hedging Bewegungen dämpft (long Gamma) oder verstärkt (short Gamma) | Gamma-Imbalance als **stetiger** Vola-/Spread-Prädiktor belegt (Barbon/Buraschi, Baltussen et al. JFE 2021). Diskretes „Flip-Level" = Anbieter-Konstrukt | Belegt (stetig), **Folklore** (Flip-Level) |
| **Treasury-Basis-Trade** | Kassa-Anleihe long, Future short, Repo-finanziert, ~20x Hebel, ~$830 Mrd. brutto (Sept. 2025) | Bei Repo-Stress erzwungener Abbau → Treasury-Futures-Volatilität (März 2020) | Belegt (OFR/Fed) |
| **Block Trades / EFP / EFRP** | CME Rule 526/538: privat verhandelt, außerhalb des Buchs, Mindestgrößen, Meldepflicht | Erscheinen zeitversetzt in Time & Sales, kein Flag im Retail-Feed | Belegt (Regelwerk) |

## 3. Mikrostruktur: warum Volumen Information trägt (und warum oft nicht)

- **Kyle (1985):** Der Informierte tarnt sich, streckt sein Volumen, damit der Market Maker ihn nicht vom Noise trennen kann. Der MM sieht nur Netto-Orderflow und setzt den Preis mit λ (Impact pro Flow-Einheit). Folge: informierter Flow ist *designed*, unauffällig zu sein. Wer ihn im Volumen sehen will, sucht nach dem, was der Algo nicht verstecken kann: die Summe über Zeit, nicht die einzelne Bar.
- **Glosten/Milgrom (1985):** Spread = Preis der adversen Selektion. Breiter Spread / dünnes Buch = MM fürchtet Informierte.
- **Cont/Kukanov/Stoikov (2014):** Kurzfrist-Preisänderung ≈ linear in der Order-Flow-Imbalance am Best Bid/Ask, Steigung ∝ 1/Markttiefe. Dünne Bücher reagieren stärker auf gleiche Imbalance. Für Treasury-Futures von der Fed (2025) bestätigt, für ES/NQ auf Minutenebene **keine Studie** (Lücke, Logbuch #107).
- **Iceberg / Hidden Liquidity (CME Globex):** Existenz und algorithmische Erkennbarkeit aus Tiefe + Trade-Größe belegt (Christensen/Woodmansey 2013, Zotikov 2019). Kursierende Quote „15-25 % in ES" **nicht verifizierbar**, nicht verwenden.
- **Vertikal vs. horizontal:** Llorente et al. (2002): Volumen-Rendite-Zusammenhang unterscheidet informierten (Fortsetzung) von Liquiditäts-Flow (Umkehr), aber nur auf Tagesebene/Aktien belegt. Horizontales Volumen (Volume Profile, POC, Value Area, Market Profile/AMT) hat **keine akademische Grundlage** als Prädiktor (Cache-Fehlanzeige); Theorie dahinter ist Auktionslogik: wo viel Volumen pro Preis lag, wurde Position aufgebaut, dort liegen vermutlich Stops/Re-Entries der gleichen Akteure.

## 4. Beleg-Raster

| Stufe | Was |
|---|---|
| **Belegt** | Square-Root-Law, Almgren-Chriss, Kyle / Glosten-Milgrom, OFI (Cont et al.), CME-Roll-Mechanik, Block-Trade-Regeln, Basis-Trade-Größe, Monatsende-Rebalancing, Gamma-Imbalance als stetiger Vola-Prädiktor |
| **Dünn** | MOC-Imbalance → ES-Futures-Kausalkette, Impact-Decay-Zeitskala, Vol-Targeting-Schwellen |
| **Folklore** | Iceberg-Prozentzahl auf ES, Gamma-Flip-Level als Preis-Level, konkrete CTA-Trigger, Volume-Profile-Level als solche |

## 5. Theoretische Ansatzpunkte (Mechanismus-Ebene, keine Regeln)

1. **Impact-Decay ist messbar:** Preis, der durch fremden Druck gelaufen ist, gibt nach Ende des Drucks teilweise nach. Zeitskala offen (Stunden bis Wochen).
2. **OFI trägt kurzfristig lineare Preisinformation**, Sensitivität ∝ 1/Tiefe. Braucht L2, nicht Minuten-CVD (das war #021: tot, weil Look-ahead).
3. **Kalender-Fenster existieren strukturell** (Roll-Woche, Monats-/Quartalsende, OpEx). Das Fenster ist belegt, der handelbare Effekt darin jeweils einzeln zu prüfen und teils widerlegt (#087).
4. **Gamma-Regime ist stetig:** Dealer-Positionierung bestimmt, ob Intraday-Bewegungen gedämpft oder verstärkt werden. Ohne historische GEX-Zeitreihe nicht backtestbar (Cache #417-425).
5. **Volumen ist nur relativ zum erwarteten Profil informativ**, weil VWAP/POV-Algos selbst das Profil erzeugen. Abweichung vom Erwartungswert (vertikal) bzw. ungewöhnliche Konzentration pro Preis (horizontal) ist der einzige Kanal, über den eine Metaorder sich im Roh-Volumen verrät.

## 6. Was Max mit 1 Kontrakt auf NT8/Tradovate sehen kann

| Quelle | Verfügbar? |
|---|---|
| Preis/Volumen (Bars) | ✅ Echtzeit + Historie (1m, `NQ_full.parquet`) |
| L2 / Orderbuch-Tiefe | ✅ live über Tradovate-Feed, ❌ historisch nicht in der Engine → OFI nur live/forward beobachtbar |
| Iceberg-Erkennung | ⚠️ nur Näherung (Trade-Größe vs. resting Volumen), kein CME-Flag |
| Block-Trade-Reports | ⚠️ zeitversetzt öffentlich, für Intraday kaum nutzbar |
| Roll-Volumen/OI | ✅ CME Roll Analyzer, kostenlos |
| COT | ⚠️ Stichtag Di, Release Fr 15:30 ET → nur Wochen-/Regime-Kontext |
| Options-OI / GEX | ⚠️ live nur kostenpflichtig ($89-350/Monat), keine freie Historie → nicht backtestbar |
| EFP/EFRP | ❌ kein Flag im Retail-Feed |

## 7. Offene Lücken (aus der Recherche)
- Keine Futures-spezifische Impact-Decay-Studie.
- Keine ES/NQ-Minuten-Studie zu OFI/Kyle-λ (#107).
- Iceberg-Prävalenz auf CME unbekannt.
- CTA-Trigger-Mechanik proprietär.
- MOC → ES nur ein Working Paper.
