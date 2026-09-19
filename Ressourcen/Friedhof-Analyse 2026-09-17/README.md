---
tags:
  - ressource/trading
  - trading/friedhof
erstellt: 2026-09-17
---
# Friedhof-Analyse 2026-09-17: Rohmaterial

Auswertung und Stempel stehen in [[Friedhof-Analyse (17.09.2026)]] (Projekte/). Hier liegt das Rohmaterial der sieben Extraktions-Agents und der Audits, damit einzelne Grabsteine nachschlagbar bleiben. Fehlerklassen (in allen Tabellen): F1 alte Engine/Daten, F2 altes Kriterium, F3 zu wenig Varianten, F4 Gate-Artefakt, F5 Prior-Kill, F6 Pipeline-Bug, F7 falsches Mass/Kontrollarm, F8 Karten-Status verdeckt Mechanismus, F9 liegengeblieben, F10 Nebenbefund nie verfolgt, F0 haelt.

| Datei | Inhalt |
|---|---|
| BRIEF.md | Auftrag, Fix-Zeitleiste, Ausgabeformat der Agents |
| logbuch_teil1.md | Logbuch #026-#095, 93 Grabsteine (T01-T93) |
| logbuch_teil2.md | Logbuch #096-#135, 104 Grabsteine (T2-01 bis T2-104) |
| logbuch_teil3.md | Logbuch #136-#157 + VWAP-Offensive + ES-Woche, 90 Grabsteine (G01-G90) |
| bank_momentum_twap_pca.md | Momentum-&-Averages-, TWAP-, PCA-Bank, 335 Zeilen |
| bank_volumen_pairs.md | Volumen-&-Flows- und Pairs-Bank, 579 Zeilen |
| karten_scouts_labs.md | Wege-Karten, Scout-Reports, Juli-Labs, Paper-Analysen, 236 Zeilen, 6 Widersprueche |
| engine_audit_ADEF.md, d_register_gaps.md, e_survivors_no_marginal.md, f_validiert_backlog.md | Engine-Audit: Fix-Zeitleiste am Code, Register-Achsen, unbewertete Survivors, Validiert-Karten. Achtung: zwei Aussagen darin sind widerlegt (gap nur montags: falsch; tm_dir nie getestet: Default ist both) |
| b_queue_audit.md, c_premise_friedhof.md | Queue-Timeline gegen die Fix-Daten; 427 Praemissen-Tode klassifiziert |
| top_vs_original.md | alle 1.971 Buch-Bewertungen je Zelle, Top-40 nach Delta |
| SYNTHESE_ZWISCHENSTAND.md, KANDIDATEN_ENTWURF.md | Zwischenstand der Hauptsession und der Stempel-Entwurf, wie er dem verdict-auditor vorlag |

Korrekturen der Hauptsession an den Agent-Berichten (gelten vor den Tabellen): Slippage nach Ordertyp ist im Kern (qbt.py:1397); TE-v2-Jobs liefen am 01.09.; gap lief auf allen Wochentagen; AW-15b bleibt tot (29 Survivors, aber Ersatz -8 bis -24 pp); orb/orb_std haben tatsaechlich keinen Null-Schalter.
