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

1. **Gemeinsamer Golden Master und Box-Sync** (Session AP246/AP273, Abstimmung im geteilten Notizordner `AP246_operating_point_sync.md`). Er bringt diese Änderungen zusammen auf die Box:
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

## Entscheidungen für Max

| # | Thema | Stand | Empfehlung bisher | Was fürs echte Buch noch fehlt |
|---|---|---|---|---|
| 1 | **RTY-Gap r1** (`gen_gap_RTY_r1_08242126_v4re_d261002`), Ticket next-week-2026-39 | Next-Buch, live-Experiment FFN1 (11.10.) und FFN2 (12.10.). Stufe 2 am 12.10.: −2,5 ± 0,7 Monate. Bei echter Gebühr 1,90 $: 75,2 gegen 77,9 Monate, Sharpe-t 1,87 statt 2,07 (unter t 2 ab 1,34 $), erste Fassung z ≈ 0,68 (nicht belegt) | 12.10.: einfrieren und beobachten. Max 15.10.: bis Samstag live lassen, dann entscheiden | NT8-Modul `rtygap` und Parität (315/315) da. Für E8/FN je eine M2K-Instanz. Ausstiegsregel vom 11.10. noch nicht in `auto_check` |
| 2 | **OPEXMOM_fv4** (zurück im Next-Buch 15.10.) | AP286-Nachrechnung: fällt an den Vor-Gates (WF-Config t 1,80), PBO 0,82, Stempel „unentscheidbar, nach Selektion null-kompatibel“. Tempo-Tafel: −3,4 Monate [−7,7; −0,6], neuer schlimmster Buchtag −1.531 $ am 17.07. | Quant-Team 15.10.: nicht zurück. Max hat ihn trotzdem ins Next-Buch geholt | kein NT8-Modul (AP394), keine Parität, Minutenpfad 17.07. prüfen |
| 3 | **LD01_vix16_fv4** (zurück im Next-Buch 15.10.) | PB3 + LD01: −7,1 Monate roh, −4,0 [−9,2; −0,3] geschrumpft, als einzige Momentum-Ergänzung ohne Überlebenskosten. Handelt im heutigen Vola-Regime kaum (VIX-Filter 16) | Session 3a668066: ins Next-Buch (Umkehr 02.10.), Max hat zugestimmt | kein NT8-Modul: VIX-Feed auf der Box plus Filter im Momentum-Modul (AP395), Parität, Eintrag in `book_erstfassung.json` |
| 4 | **Asia-Dir auf den 50k-Konten** (AP387) | Risiko je Trade wächst mit der Vola (2026 Median 215 $, bis 686 $). Echter Pfad im 50k-Käfig: mit Asia Pass 84 %, MaxDD 3.283 $ über DD 2.000. Ohne Asia 100 %. Edge erst ab 2021 | Rechnung läuft in der Session „AP387 Asia auf den 50k-Konten“ | Ergebnis der Session: behalten oder nur auf 150k (E8 50k, FN1, FN2 sind 50k-Konten) |
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
- **Box:** kommt mit dem gemeinsamen Golden Master und Box-Sync (AP246), danach Dry-Run auf der Box.
- **Folge-Tickets:**
  - AP404: Engine-Stempel an den Kurven-Dateien, Kurven automatisch nachbauen, Alarm bei Schreibfehlern, Nachlauf-Jobs ins Passquoten-Budget.
  - AP405: Gate v4 Stufe 3 auch auf der gehandelten Config prüfen. Belegter Fall: die EMA-Leiter kam nur über die Testzeitraum-Kurve durch.
- **Queue:** laut box-ops seit 12.10. leer, die Queue-Session (AP273) füllt nach dem gemeinsamen Sync nach.
