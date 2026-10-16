---
tags: [projekt, trading, gate-v4, stufe-2, buch, wochenende]
date: 2026-10-15
status: vorbereitet, Prüfung mit Max am Samstag 17.10. (/wochenende)
---

# Wochenend-Prüfung 17.10.2026

Eine Liste für Samstag: alle offenen Buch-Entscheidungen aus den Ticket-Sessions vom 14./15.10., dazu was je Bein noch fehlt. Auftrag Max (über die Ticket-Session): alles sammeln, die Übernahme ins echte Buch entscheidet Max am Samstag. Bis dahin ändert niemand am echten Buch etwas. Ablauf: [[Buch-Workflow]], Skill `/wochenende`. Vorgänger: [[Kombi-Suche Next-Week-Buch (02.10.2026)]].

## Ausgangslage

- **Echtes Buch** (`book_state.json`, md5 ff4710ef, seit 04.10. unverändert): PB3, LastHour_v3, Asia-Dir, OpenDrive.
  - Live über MaxBookHost auf E8 50k, FN1, FN2, FFN1, FFN2, alle k1.
  - FFN1 und FFN2 handeln zusätzlich RTY-Gap auf M2K, als Live-Experiment.
- **Next-Week-Buch** (seit 15.10. 23:09, 7 Beine): echtes Buch plus RTY-Gap r1, OPEXMOM_fv4 und LD01_vix16_fv4.
  - OPEXMOM und LD01 hat Max am 15.10. zurückgeholt.
  - Stufe 2 rechnet die Varianten getrennt: echt + RTY, + OpEx, + LD01, 7er.

## Vor Samstag muss passieren (Reihenfolge)

1. ✅ **erledigt 16.10. 00:35, Golden Master grün, Runner seit 15:51 neu: Gemeinsamer Golden Master und Box-Sync** (Session AP246/AP273, Abstimmung im geteilten Notizordner `AP246_operating_point_sync.md`). Er bringt diese Änderungen zusammen auf die Box:
   - **AP246:** Betriebspunkt zentral in `operating_point.py`. Die Passquoten-Leitplanke rechnet danach am E8-150k-Käfig (DD 3.999,90) statt 50k.
   - **AP384:** echte Gebühren je Micro, MNQ/M2K 1,90 $ bzw. 1,78 $ statt 1,02 $.
   - **AP260/AP245:** `tempo_plan`. E8 150k nur noch 4 Payouts, Gratis-Challenge erst nach dem letzten Payout.
   - **AP209:** Block-Regel im Auto-Promoter, Runner speichert die Testzeitraum-Kurve.
2. **Danach `weekend_check` frisch laufen lassen.** Die Läufe vom 12. und 14.10. rechneten noch mit 1,02 $ Gebühr und dem alten `tempo_plan`. Auch die Erste-Fassung-Spalte lief mit 1,02 $.
3. **AP392:** `weekend_check` auf die Kaufrunde (1 Konto je Monat) umstellen, falls bis dahin gebaut. Sonst die Zahlen mit diesem Vermerk lesen.
4. **Lesart des Laufs (Hinweise der Session AP275):**
   - Vier Varianten getrennt beurteilen: echt + RTY, + OpEx, + LD01 und das 7er.
   - Das z von LD01 ist geliehen (gleiche erste Fassung wie PB3), nicht als Empfehlung lesen.
   - FFN fehlt in der Flotte (AP325). Die FFN-Zahlen stehen in `engine/_scratch_latte/ueberopt/ap275_p2/quant_mathematician_1015/mq_05_tafel.txt`.
   - Minutenpfad 17.07. ist geprüft (`minutenpfad_1015/`).
   - Erste Fassungen für OpEx und LD01 stehen in `book_erstfassung.json`.
   - Den Lauf fährt die Wochenend-Session (AP209), einen Vorab-Lauf gibt es nicht.

## Ergebnis weekend_check vom 16.10. (neuer Stand)

Gerechnet nach dem gemeinsamen Sync: echte Gebühr 1,90 $, 150k-Käfig, neues `tempo_plan`. Bericht: `engine/weekend_check/2026-10-16_neustand_1016.md`. Bedingungen: Kalender-Modus, RiskGuard-Stopp, 600 Sims, Nulldrift 0 %, Modus-Check grün.

| Variante | Monate bis 50k | gegen echt | erste Fassung (z) | Lesart |
|---|---|---|---|---|
| echtes Buch (4) | 83,0 ± 1,0 | | | |
| **Next-Week-Buch (7)** | **68,6 ± 0,9** | **−14,4 ± 0,8** | 2,98 | trägt, recent3y −9,5 |
| echt + LD01 | 73,8 | −9,2 | 2,16 | trägt, z geliehen von PB3 |
| echt + OpEx | 77,8 | −5,2 | 2,36 | trägt, aber die Vor-Gates sind gefallen |
| echt + RTY-Gap | 80,5 | −2,5 | 0,66 | nicht belegt |
| Next ohne RTY (6) | 71,5 | −11,5 | 3,05 | trägt |

- **Regel-Empfehlung des Tools:** Next-Week-Buch. RTY bringt im 7er nur 2,9 Monate, und die sind in der ersten Fassung nicht belegt.
- **Vorbehalte:**
  - FFN1/FFN2 fehlen in der Flotte (AP325).
  - Asia wird auf allen Konten gerechnet, obwohl AP387 sie nur auf 150k empfiehlt.
  - OpEx und LD01 haben kein NT8-Modul und sind deshalb noch nicht live-fähig (AP394, AP395).
- **Quant-Team (16.10., beide Gegenleser):**
  - **Vorsprung:** Next schlägt das echte Buch sicher, die Größe ist aber unsicher. Mit Trade-Unsicherheit liegen die −14,4 Monate bei 90 % zwischen −22,5 und −8,5. Die Zeit hängt fast nur an der Drift (Faustregel 1 $/Tag ≈ −2,2 Monate). Die Vault-Formel liegt mit der neuen Engine rund 5 % zu schnell.
  - **RTY-Gap: raus aus dem Übernahme-Paket**, beide sind einig. Erste Fassung t 0,60, Stufe 1 mit echter Gebühr gefallen. Die −2,9 Monate im 7er sind reiner Tuning-Gewinn, mit der ersten Fassung −1,0 (Band −3,9 bis +1,6).
  - **Empfohlenes Zielbuch: der 6er ohne RTY** (echt + LD01 + OpEx, 71,5 Monate, −11,5). Er trägt in jeder Lesart von LD01 (z 2,15 bis 3,05). Ehrliche Spanne −5,5 bis −11,5 Monate, mit Trade-Unsicherheit −18,9 bis −6,8.
  - **OpEx:** sauberste Herkunft (Grid-Mitte vorab festgelegt, kein Tuning-Zuwachs), Beitrag −3,6 Monate (−7,4 bis −1,1), korreliert −0,02 zu PB3. Statistisch nie entscheidbar (Live-Beleg ~16 Jahre), kostet aber bei Edge 0 nichts. Vorbehalt: schlimmster Tag −1.531 $ am 17.07.; auf FN 50k (DD 1.500) hält ihn nur der 600-$-Guard.
  - **LD01:** 75 % seiner Tage sind PB3-Tage, an diesen korrelieren beide mit 0,89. Seine erste Fassung ist die von PB3, eigene Evidenz gibt es kaum (t_alpha 1,7). Die Drift ist das 10-Jahres-Mittel, in den letzten 12 Monaten gab es nur 8 Trades, 2022 keinen. Bei heutiger Vola eher −5 Monate. Faktisch ist LD01 eine bewusste Wette auf mehr Momentum: fällt PB3, fällt LD01 mit.
  - **Widerspruch bei Stufe 1:** RTY fliegt bei t 1,87, OpEx bleibt mit WF-t 1,80. Das sollte Max am Samstag bewusst entscheiden.
- **Was das praktisch heißt:** OpEx und LD01 können ohnehin erst nach NT8-Port und Parität live (AP394, AP395).
  - Vorschlag: zuerst OpEx portieren (~0,5 Tag plus Sim).
  - Vor LD01 einmal „PB3 doppelt an Tagen mit VIX unter 16“ als Vergleich rechnen.
  - RTY auf FFN abschalten (Empfehlung AP384), das Next-Buch auf den 6er ohne RTY setzen.
  - Alles Entscheidung Max.

## Entscheidungen für Max

| # | Thema | Stand | Empfehlung bisher | Was fürs echte Buch noch fehlt |
|---|---|---|---|---|
| 1 | **RTY-Gap r1** (`gen_gap_RTY_r1_08242126_v4re_d261002`), Ticket next-week-2026-39 | Next-Buch, live-Experiment FFN1 (11.10.) und FFN2 (12.10.). Stufe 2 am 12.10.: −2,5 ± 0,7 Monate. Bei echter Gebühr 1,90 $: 75,2 gegen 77,9 Monate, Sharpe-t 1,87 statt 2,07 (unter t 2 ab 1,34 $), erste Fassung z ≈ 0,68 (nicht belegt) | 12.10.: einfrieren und beobachten. Max 15.10.: bis Samstag live lassen, dann entscheiden | NT8-Modul `rtygap` und Parität (315/315) da. Für E8/FN je eine M2K-Instanz. Ausstiegsregel vom 11.10. noch nicht in `auto_check`. **Session AP384, 16.10.:** mit echter Gebühr fällt RTY-Gap durch Gate v4 Stufe 1 (t 1,87 bzw. 1,90, IS-PF 1,05, DSR 0,44), mit der Edge der ersten Fassung nur −1,1 Monate (Band −3,2 bis +1,1). Empfehlung: nicht ins echte Buch, auf FFN1/FFN2 abschalten |
| 2 | **OPEXMOM_fv4** (zurück im Next-Buch 15.10.) | AP286-Nachrechnung: fällt an den Vor-Gates (WF-Config t 1,80), PBO 0,82, Stempel „unentscheidbar, nach Selektion null-kompatibel“. Tempo-Tafel: −3,4 Monate [−7,7; −0,6], neuer schlimmster Buchtag −1.531 $ am 17.07. | Quant-Team 15.10.: nicht zurück. Max hat ihn trotzdem ins Next-Buch geholt | kein NT8-Modul (AP394), keine Parität, Minutenpfad 17.07. prüfen |
| 3 | **LD01_vix16_fv4** (zurück im Next-Buch 15.10.) | PB3 + LD01: −7,1 Monate roh, −4,0 [−9,2; −0,3] geschrumpft, als einzige Momentum-Ergänzung ohne Überlebenskosten. Handelt im heutigen Vola-Regime kaum (VIX-Filter 16) | Session 3a668066: ins Next-Buch (Umkehr 02.10.), Max hat zugestimmt | kein NT8-Modul: VIX-Feed auf der Box plus Filter im Momentum-Modul (AP395), Parität, Eintrag in `book_erstfassung.json` |
| 4 | **Asia-Dir auf den 50k-Konten** (AP387) | Stufe 2 (Kalender-Modus, RiskGuard-Stopp je Kontotyp, Gebühr 1,90 $): „nur 150k“ ist in allen Basen 0,6 bis 1,8 Monate schneller als „überall“ (P 0,93 bis 0,98). Ab 2024 E8 50k Pass 85 → 90 %, Ruin vor erstem Payout 17 → 6 %; FN Pass 77 → 83 %. Auf FFN hilft Asia (12-M-Payout 455 $ statt 177 $ ohne). Gegen „ganz raus“ bei heutiger Vola 1,9 bis 8,0 Monate schneller | Session AP387 (Quant-Team, konto-analyst, strategy-auditor „hält mit Auflagen“): **Asia nur auf 150k**, Modul runter von E8 50k, FN1, FN2, bleibt auf FFN1/FFN2 und künftigen 150k. `book_state.json` bleibt, nur die Belegung je Konto ändert sich | Auflagen vor Live: Nachlauf mit Oktober-Vola, live-reconciler Asia seit 11.08., konto-analyst + Host-JSONs live_e8_50k/fn1/fn2, E8-Inaktivität (ohne Asia 7 statt 5 Lücken-Strecken seit 2024, Hand-Alarm muss live sein), Buch je Kontotyp in der Engine (AP334, sonst rechnet weekend_check Asia wieder auf 50k). Volltext `engine/_scratch_ap387/ERGEBNIS.md` |
| 5 | **LIVE_EXTRA** (Live-Buch, `live_finalize.py`) | Bei 1,90 $ Gebühr, je 1 Micro: OPEXMOM_NQ 250 $/J, t 1,79, DD −353. EVENT_ES_primary 245 $/J, t 1,54, DD −1.481 (FOMC-Hälfte t 0,45). Gleiche Wette an 52 Tagen (Korrelation 0,87). Im Live-Buch: +OPEX dSR +0,047, +EVENT +0,046, +beide +0,076, DD dann −4.267 statt −3.781. Why-Texte zitieren noch „Grade A“ mit Look-ahead | Session Engine-Fixes: nur eine OpEx-Wette. Kommt NQ_OPEXMOM_fv4 ins echte Buch, beide aus LIVE_EXTRA raus. Sonst OPEXMOM_NQ behalten, EVENT_ES raus | Entscheidung Max, danach `live_finalize.py` samt Why-Texten. Hängt an #2 |
| 6 | **AP223, AP286, AP303** (Engine-Fixes) | Fixes auf der Box seit 13.10., Golden Master 15.10. grün. Asia ändert sich praktisch nicht (773 → 769 $/Jahr), VWAP bleibt draußen. AP223 Schritt 5 gemacht: Survivors 366 → 346 mit ehrlichem Tick, → 264 mit Gebühr 1,90 $; alte positive Urteile unter t ~2,3 sind danach nicht mehr belegt (RTY-Gap 12/6/0, Power-Hour 30/28/13, Opening-Drive 11/11/4), kein Buch-Bein betroffen | AP223 und AP303 schließen (done_when erfüllt), AP286 nach der LIVE_EXTRA-Entscheidung plus Logbuch-Urteil | Vorlagen: `engine/_scratch_ap223_286_303/live_extra/zusammenfassung.md`, `.../survivors/zusammenfassung.md` |
| 7 | **next-week-2026-40** | einzige Auto-Änderung (EMA-Leiter) am 10.10. wieder raus (AP339) | Ticket löschen | nichts |
| 8 | **Hochstufen auf k2** ([[Hochstuf-Regel je Konto (Entwurf)]]) | Schwelle 235 $ Tagesschwankung auf FFN. FFN steht bei 577 $ (σ60, Daten bis 10.08.), kein Konto darf heute auf k2 | Wochenend-Thema laut Notiz | NT8-Export Oktober (AP356) für frische Vola |

## Draußen und nicht zur Entscheidung (Stand 15.10., Begründung im Next-Buch-Protokoll)

- **VWAP-Pullback und ORB2:** eingefroren, Module und Parität sind da. Wiedervorlage über AP341.
- **ES_AC06d:** Wiedervorlage bei Entry-Why plus erste Fassung mit t ≥ 2.
- **ES_OpenDrive:** nur als Ersatz oder Verdopplung von NQ-OpenDrive.
- **EMA-Leiter:** Wiedervorlage über AP339.

## Auto-Promoter seit 15.10. (AP209)

- **Regel:** Ein zweiter Discovery-Fund neben offenen Next-Beinen kommt nur rein, wenn zwei Bedingungen halten:
  - Der Buch-Sharpe steigt gegen echtes Buch plus offene Beine.
  - Die Passquote verliert zusammen höchstens 3 Punkte gegen das echte Buch.
- **Kopien:** Eine Kopie eines offenen Auto-Beins (Korrelation über 0,7) ersetzt es nur, wenn sie klar besser ist. Das gilt auf der Testzeitraum-Kurve und auf der gehandelten Config.
- **Hand-Beine** (OPEXMOM, LD01) zählen als offen und werden nie automatisch getauscht.
- **Rückstellungen:** werden neu geprüft, sobald sich echtes oder Next-Buch ändert.
- **Am heutigen Stand:** Die drei RTY-Varianten vom 12.10. bleiben zurückgestellt, weil sie als Ersatz auf der Testzeitraum-Kurve schlechter sind als das offene RTY-Bein.
- **Prüfungen:** pipeline-auditor „go mit Auflagen“, die Auflagen sind erledigt.
- **Box:** seit dem gemeinsamen Sync am 16.10. aktiv. Der erste echte Lauf um 15:53 hat die drei RTY-Varianten mit genau den erwarteten Zahlen zurückgestellt und nichts promotet. AP209 ist damit abgenommen.
- **Folge-Tickets:**
  - AP404: Engine-Stempel an den Kurven-Dateien, Kurven automatisch nachbauen, Alarm bei Schreibfehlern, Nachlauf-Jobs ins Passquoten-Budget.
  - AP405: Gate v4 Stufe 3 auch auf der gehandelten Config prüfen. Belegter Fall: die EMA-Leiter kam nur über die Testzeitraum-Kurve durch.
- **Queue:** laut box-ops seit 12.10. leer, die Queue-Session (AP273) füllt nach dem gemeinsamen Sync nach.
