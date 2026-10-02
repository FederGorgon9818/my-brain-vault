---
tags: [projekt, trading, gate-v4, stufe-2, buch]
date: 2026-10-02
status: gerechnet, Entscheidung Max am Wochenende
---

# Kombi-Suche Next-Week-Buch (02.10.2026)

Auftrag Max 02.10.: jedes Bein im Next-Week-Buch einzeln bewerten, Rauschen markieren, beste Kombination aller Beine nach Zeit bis 50k, keine Kopien (gleiche Strategie zweimal), einmal mit und einmal ohne Rausch-Beine. Ergänzt den Stufe-2-Bericht von heute Nacht (`engine/weekend_check/2026-10-02_flotteB_e8_150k.md`), der nur "hinzufügen / ersetzen / ohne X" rechnet, keine freie Kombination. Vorgänger: [[Friedhof-Nachlauf Gate v4 (01.10.2026)]], [[Latte-Audit (25.09.2026)]]. Kein Buch geändert.

**Kurz:** Das Next-Week-Buch fährt drei Kopien. Ohne sie kommen 7 bis 8 Beine gleich schnell an 50k (≈ 39 bis 40 Monate, echtes Buch 81) und halten jedes pessimistische Szenario deutlich besser aus. Belastbar ist nur "Kopien raus", ob ORB2 und RTY-Gap reinkommen, ist eine Wette auf deren Edge.

## Betriebspunkt und Methode

- Wie Flotte B: tempo_plan Kalender-Modus, Bestand A E8 50k k1 + FN1/FN2 FN 50k k1, Kaufpolitik E8 150k k2, Deckel 2.500 $, RiskGuard-Tages-Stopp, Nulldrift-Zwilling. 12 Beine im Topf (3 echte + 9 neue inkl. RTY-Gap, heute auto-promotet).
- **Kein Schätz-Proxy.** Erster Anlauf mit Vorauswahl über eine Formel (log Monate ~ Buch-SR, Drift) abgebrochen: laut `quant-mathematician` sieht die Formel den Intraday-Stopp nicht und trennt an der Spitze nicht (Restfehler größer als der Abstand der Top 10).
- Stattdessen **Rückwärts-Streichen im echten Simulator**: ab jedem maximalen Buch ohne Kopien je Runde jedes Bein einmal raus (300 Sims), das beste Streichen übernehmen, Stopp, sobald jede Streichung belegt langsamer macht. 123 Such-Läufe. Finalisten mit **frischem Seed** (sonst läuft das Auswahlrauschen mit): 600 Sims, Nulldrift 300, Regime shrink058 und recent3y, dazu glücksbereinigt mit N_eff 30 je auffälligem Bein.
- Drei Töpfe: **A** alle Beine, **B** ohne auffällige neue Beine (Max' Regel), **C** nur Beine, die der Statistiker als echt oder knapp einstuft.

## Kopien: über alle Tage harmlos, an gemeinsamen Tagen nicht

Neue Regel: Kopie, wenn Korrelation über alle Tage > 0,5 **oder** mindestens 50 % der Tage des selteneren Beins gemeinsam sind **und** die Korrelation an diesen Tagen > 0,5. Über alle Tage verdünnt ein seltenes Bein die Korrelation (Faktor √(Tage klein / Tage groß)), deshalb sah alles harmlos aus.

| Paar | Überlapp | Korr. gemeinsame Tage | Korr. alle Tage |
|---|---|---|---|
| Momentum alt / PB3 | 100 % | 0,62 | 0,61 |
| Momentum alt / LD01 | 78 % | 0,61 | 0,21 |
| PB3 / LD01 | 75 % | **0,89** | 0,30 |
| NQ-OpenDrive / ES-OpenDrive | 67 % | **0,90** | 0,41 |
| ES-OpenDrive / ES-AC06d | 66 % | **0,90** | 0,43 |
| ES-AC06d / VWAP-PB | 54 % | 0,50 (Grenze) | 0,13 |

LD01 ist PB3 doppelt gefahren an Tagen mit VIX < 16. Das Next-Week-Buch (11 Beine) enthält damit drei Kopien.

## Die Beine einzeln

Max' Rausch-Regel "Herkunft auffällig" (Familie > 100 Configs oder > 3 × eigener Job) trifft **11 von 12 Beinen, auch alle drei Live-Beine**, nur OpEx nicht. Die Regel ist damit unkalibriert (gleicher Fehler wie Gate v3: das eigene Buch fällt durch). Grund laut `quant-statistician`: E[max SR | N] unterstellt unabhängige Versuche, Grid-Nachbarn sind stark korreliert, N_eff eher 10 bis 100 statt 20.673. In der anderen Richtung zählt die Regel die zweite Auslese der Friedhof-Beine (6 aus 188 Karten) nicht mit, deshalb rutscht OpEx als "sauber" durch.

| Bein | SR | t | Urteil Statistiker | Grund |
|---|---|---|---|---|
| NQ_OpenDrive_maband2050 | 1,60 | 5,2 | echt | auch bei rohem N noch +0,41 bereinigt |
| NQ_LastHour_v3 (live) | 1,11 | 3,6 | echt | bereinigt +0,23 / +0,47 bei N_eff 30 |
| NQ_Momentum_d260818 (live) | 0,86 | 2,8 | knapp | WF bestanden |
| NQ_Momentum_PB3_fa01b | 1,25 | 4,1 | knapp | Familie echt, Pullback-Aufschlag nicht belegt |
| NQ_Asia-Dir-USopen (live) | 0,79 | 2,6 | knapp | WF nur an der Passquote |
| NQ_VWAP-Pullback_v8BE | 0,98 | 3,2 | knapp | aus der Friedhof-Auslese |
| ES_OpenDrive_maband2050 | 0,97 | 3,1 | knapp | Markt-Replikation von NQ, aber Kopie |
| NQ_LD01_vix16 | 1,05 | 3,4 | Rauschen | VIX-Filter unbelegt, Kopie von PB3 |
| ES_AC06d_legstop | 0,84 | 2,7 | Rauschen | bereinigt negativ, Kopie |
| NQ_REFINE_ORB2_close | 0,76 | 2,5 | Rauschen | zusätzliche Filter-Parameter |
| NQ_OPEXMOM | 0,69 | 2,2 | Rauschen | nur 79 Trades, "unauffällig" ist Zählartefakt |
| gen_gap_RTY (02.10.) | 0,77 | 2,3 | Rauschen | sieht aus wie der erwartete Rauschkandidat der Null-Kampagne |

## Ergebnis Finalisten

Median Monate bis 50k (± MC-SE, frischer Seed), pessimistisch = P(50k in 10 Jahren).

| Buch | Beine | Median | vs Next | P36 | ök. Tod | recent3y | shrink058 | bereinigt (N_eff 30) |
|---|---|---|---|---|---|---|---|---|
| A bester: LastHour, Asia, PB3, NQ-OpenDrive, OpEx, VWAP-PB, ORB2, RTY-Gap | 8 | **39,0 ± 0,6** | −1,1 ± 0,5 | 40,3 % | 1,0 % | 32,1 | 44 % | 7 % |
| A kleinster im Plateau (ohne OpEx) | 7 | 40,2 ± 0,5 | +0,1 ± 0,5 | 37,8 % | 1,3 % | 32,1 | 45 % | 7 % |
| Next-Week-Buch (mit Kopien) | 11 | 40,1 ± 0,7 | | 38,8 % | 2,2 % | 33,8 | 31 % | 2 % |
| C: LastHour, Asia, PB3, NQ-OpenDrive, VWAP-PB | 5 | 45,1 ± 0,7 | +5,0 ± 0,6 | 23,3 % | 2,5 % | 40,9 | 34 % | 7 % |
| B: Momentum alt, LastHour, Asia, OpEx | 4 | 73,8 ± 1,3 | +33,7 | 0,7 % | 0,5 % | 57,6 | 27 % | 2 % |
| echtes Buch | 3 | 80,7 ± 1,3 | +40,6 | 0,3 % | 1,5 % | 64,0 | 19 % | 2 % |

Nulldrift überall 0 %, Auslage p90 überall ≤ 1.560 $. Median unter shrink058 und bereinigt bei allen Büchern > 120 Monate.

## Urteil Quant-Team

- **Gleichstand** zwischen A bester (8), A kleinster (7) und Next (11). OpEx zu streichen kostet +0,9 ± 0,6 M, nicht belegt. Nach [[Simplex beats Komplex]] gewinnt im Plateau das 7-Bein-Buch.
- **Belastbar ist nur der Schritt "Kopien raus"** (LD01, ES-OpenDrive, AC06d): roh gleich schnell, bereinigt 2 → 7 % (≈ 3σ), ök. Tod bereinigt 85 → 67 %, shrink058 31 → 45 %. Hält in jeder Spalte, die nicht gleich steht.
- **7 Beine gegen die 5 echten/knappen:** trägt roh (−4,9 M), recent3y (−8,8 M) und shrink058 (+10,7 pp), bereinigt nicht (7,0 gegen 6,7 %). Der Vorsprung hängt also genau daran, dass ORB2 und RTY-Gap echt sind. Wette mit kaum Abwärtsrisiko, Kosten nur zwei Beine mehr in NT8.
- **Winner's Curse:** MC-Teil durch frischen Seed abgefangen. Historien-Teil nicht: alle Läufe wählen auf denselben ~10 Jahren, Fehler des Niveaus grob ±10 M (Überschlag, kein Bootstrap). Unterschiede von 1 M sind nicht trennbar.

## Empfehlung (Entscheidung Max)

1. Kopien raus: LD01, ES-OpenDrive, ES-AC06d.
2. Kandidat fürs Buch: **7 Beine** LastHour, Asia, PB3, NQ-OpenDrive, VWAP-PB, ORB2, RTY-Gap. Konservative Variante: die 5 echten/knappen ohne ORB2 und RTY-Gap.
3. **Buch-Lücke:** alle neuen Beine (PB3, NQ-OpenDrive, VWAP-PB, ORB2, RTY-Gap) brauchen NT8-Port + Paritäts-Prüfung (AP290) vor der Übernahme, danach Live-Tracking.

## Offen

- Herkunfts-Regel kalibrieren: `overfit.effective_trials()` je Familie auf die Tages-PnL-Matrix, nur Versuche bis zum Auswahldatum, Friedhof-Auslese als zweite Stufe (Vorschlag Statistiker). Solange bleibt "Herkunft auffällig" nur Hinweis.
- Kopie-Regel mit Überlapp gehört in `weekend_check` und ins Gate v4 (Tages-Korrelation > 0,7 über alle Tage übersieht genau diese Fälle).
- Historien-Bootstrap der gepaarten Differenzen (macht aus ±10 M einen Messwert).
- Intraday-Tief des Buchs wird als Summe der Einzel-Tiefs gerechnet (Obergrenze), bremst große Bücher am RiskGuard-Stopp etwas (Hinweis Mathematiker).

## Dateien

`engine/weekend_check/2026-10-02_kombi/`: `kombi_v2.py` (Suche), `kombi_pess.py` (pessimistische Spalten), `meta.json` (Einzelbeine), `v2_final.json`, `v2_pess.json`, `v2_paths.json`, `v2.log`. Stempel: Daten 2016-01-04 bis 2026-08-06, Next-Buch-Hash `c14d5cb1`, Seeds 202 (Suche) / 303 (Finalisten).
