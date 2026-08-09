---
tags:
  - ressource/paper
  - trading/orderflow
erstellt: 2026-07-15
---
# 🌊 Order-Flow: wo hat es predictive Value? (Recherche + Test)

⬅️ [[Alpha-Konzepte]] · [[Strategie-Logbuch]]

> [!important] Kern-Fazit
> Order-Flow hat echten Vorhersagewert — aber auf **Sekunden-Ebene mit L2-Daten**, nicht auf Minuten-Ebene mit unseren Daten. Die eine für uns baubare Ausnahme (VPIN) haben wir getestet: **kein sauberer Edge.** Damit ist der Order-Flow-Track auf unserer Datenauflösung ausgereizt.

## Die Konstrukte (aus der Literatur)
| Konstrukt | Was | Predictive? | Für uns baubar? |
|---|---|---|---|
| **OFI** (Cont/Kukanov/Stoikov 2011) | Signierte Queue-Größen-Änderungen an Best-Bid/Ask | Stark, aber **gleichzeitig** (erklärt Preis, R²~65%), kaum Vorlauf | braucht MBP-1/L2, Sekunden |
| **Multi-Level OFI** (Xu/Cont/Stavrinou, Oxford) | OFI über 10 Buch-Ebenen | Besser als Top-of-Book, aber Sekunden | braucht MBP-10 |
| **Deep-LOB** (Kolm et al. 2024) | Deep Learning auf L2-Tensor | Vorhersage „ubiquitär" — aber nur **Sekunden/Zehntelsekunden** OOS | braucht L2 + HFT-Latenz |
| **VPIN** (Easley/Lopez de Prado/O'Hara) | Order-Flow-**Toxizität** aus Buy/Sell-Volumen (Volumen-Clock) | Sagt **Volatilität/Regime** voraus (Flash-Crash-Warnung), NICHT Richtung | **JA, aus unseren Daten** ✅ |

**Muster:** Richtungs-Vorhersage aus Order-Flow lebt auf **Sekunden + L2**. Bei Retail-Latenz und Minuten-Auflösung ist sie weg (deckt sich mit unserem Test, Logbuch #021: Minuten-Delta corr ~0).

## Was wir gebaut + getestet haben: VPIN
- Aus echten Aggressor-Buy/Sell-Volumen, Volumen-Clock (~50 Buckets/Tag), VPIN über 50 Buckets, **kein Look-Ahead** (Minute nutzt Bucket davor).
- **Korrelation (distinkt von VIX):** VPIN↔VIX -0,32 · VPIN↔realisierte Vola -0,21 · VIX↔Vola +0,77. → VPIN misst etwas Eigenes, aber schwach.
- **Als Momentum-Regime-Filter:** Quintil-expR +0,14 / +0,23 / +0,33 / +0,11 / +0,22 → **nicht monoton, Rauschen** (N=481 ab 2021, kleine Buckets). Kein sauberer Filter wie VIX.

## Ehrliches Fazit (Insight #13)
- Order-Flow ist echt, aber die **handelbare Edge sitzt jenseits unserer Reichweite** (Sekunden/L2/Co-Location).
- VPIN als einziges baubares Regime-Signal bringt bei uns keinen klaren Edge (zu kleines Sample, schwaches Signal). Per **Simplex beats Komplex** NICHT ins Lab aufgenommen.
- **Nicht** ES/YM/RTY Order-Flow oder MBP-10 ziehen — die Literatur sagt selbst, es hilft nur auf Sekunden/L2.
- **Nächster echter Hebel = Cross-Asset / Relative Value** (VIX lief schon: +16 Punkte). Das ist buildbar und hat noch Luft.

## Quellen
[Cont/Kukanov/Stoikov – Price Impact of Order Book Events](https://arxiv.org/abs/1011.6402) · [Multi-Level OFI (Oxford)](https://www.tandfonline.com/doi/full/10.1080/14697688.2023.2236159) · [Deep-LOB Predictability (2024)](https://www.sciencedirect.com/science/article/pii/S0169207024000062) · [VPIN (Easley/LdP/O'Hara)](https://www.quantresearch.org/VPIN.pdf)
