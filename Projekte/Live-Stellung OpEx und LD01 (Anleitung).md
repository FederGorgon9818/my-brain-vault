---
tags: [trading, box, nt8, deploy, anleitung, opex, ld01]
datum: 2026-10-24
status: Stufe 1 deployt (25.10.), OpEx live ab 20.11.; Deploy-Abend Mi 28.10. (Stop-Verzögerung, Sim-Host, Feiertage) vorbereitet; LD01 live frühestens Do 05.11.
tickets: [AP394, AP395]
---

# Live-Stellung OpEx und LD01 A

Die zwei Beine aus der [[Wochenend-Prüfung 24.10.2026]] gehen in zwei Stufen live:

| | Stufe 1: dieses Wochenende | Stufe 2: nach der Messwoche |
|---|---|---|
| **OpEx** (`NQ_OPEXMOM_fv4`) | Host-JSON aller 5 Konten bekommt das Modul. Erster Trade frühestens **Fr 20.11.** (12:00 ET = 18:00 Boxzeit) | nichts mehr |
| **LD01 A** (`NQ_LD01_vix16_fv4`) | Code deployen, VIX-Feed starten, Sim-Host auf Sim101 | Host-JSONs, frühestens Sa 31.10., wenn die Messwoche grün ist |

Alle Zeiten **Boxzeit**. Heute Nacht (Sa auf So, 03:00) stellt Europa auf Winterzeit um, die USA erst am 01.11. Diese Woche gilt also: ET plus 5 Stunden (Handel 14:30 bis 21:00 Boxzeit), ab 02.11. wieder plus 6.

**Hauptkanal** ist die Claude-Session, in der diese Anleitung entstanden ist (Seitenleiste, Session vom 24.10. abends). Die **fett** gedruckten Stichworte schreibst du dort hinein, Claude prüft per SSH und schreibt dir das Ergebnis.

> [!success] Stufe 1 deployt und geprüft, So 25.10. 00:30 Boxzeit (Claude per SSH)
> - Gesamt-Deploy von Max 00:12 bis 00:16 durchgelaufen, NT8 neu seit 00:16:41, DLL 00:16:34.
> - Code live: Momentum `1754238F`, PB3 `170970EB`, VixFilter `78CABE11`, OpEx `3565F4E9`, Host `C2C4B5A9`, Basis `582D56B5`. Backup `_bak_archiv\deploy-20261025-0016`.
> - **Alle 5 Hosts `HOST BEREIT` um 00:18 mit der neuen md5**, Module LH, OD, Asia, PB3 (FFN mit Stop-Verzögerung 10 s), **OpEx als letztes**. JSON-Backups `*.bak-20261025-vor-opex` liegen auf der Box.
> - 5 RiskGuards aktiv, Telegram an, Tagesstopp E8 900 $, FN 600 $, FFN 2.500 $, Inaktivitäts-Wächter aktiv.
> - VIX-Feed läuft (Task alle 15 min, Ergebnis 0), jüngste Zeile 23.10. mit 19,45. Damit würde LD01 am Montag ohnehin nicht handeln.
> - Register nachgezogen (Belegung jetzt PB3+LH+Asia+OD+OPEX auf allen 5 Konten), Kartenlauf angestoßen.
> - **Teil 4 Schritt 5 erledigt (25.10. 15:30):** Das Output-Fenster bleibt leer (Ursache offen, die Hosts laufen). Ersatzweise hat Max an allen Host-Charts Days to load 45 und US Equities RTH bestätigt: 26 Handelstage vor dem 16.10., 33 vor dem 20.11. nach einem Neustart, OpEx braucht 20. Echte Kontrolle am Fr 20.11. ab 18:01 Boxzeit im NT8-Log (Zeile `OpexMom 2026-11-20`).
> - **Noch offen von dir:** Schritt 6 (Sim-Host Sim101, bisher kein `HOST BEREIT` für Sim101) und Schritt 7 (Feiertags-Bars).

## Schon erledigt (Claude, Sa 24.10. ca. 17:30)

- **Box-Stand:** Hosts laufen seit 24.10. 11:13 auf allen 5 Konten mit den 4 alten Beinen, alle flat. OpEx-Code `3565F4E9` ist seit 22.10. auf der Box. Die 5 Live-JSONs auf der Box sind byte-gleich mit den Staging-Kopien.
- **Pre-Flight LD01** (`deploy_ld01_20261024.ps1 -PreflightOnly`): alle Konten flat, `COMPILE OK - keine Fehler`, `Pre-Flight OK.`, nichts deployt.
- **Prüflauf JSON** (`deploy_json_20261025.ps1 -Check`): alle 6 Dateien `[OK]`, Box-Stand gleich dem erwarteten Ausgangsstand.
- **konto-analyst** (Konto-Sperre): kein Konto spricht formal gegen OpEx mit 1 MNQ. FN1/FN2 sind das schwächste Glied (Puffer etwa 2 Tagesschwankungen), das ist bekannt und deine Entscheidung vom 24.10. Die Konto-Karten kennen OpEx und LD01 noch nicht, das wird nach dem Aktivieren nachgezogen (siehe Teil 5).

- **Freigabe (25.10., deine Ansage):** OpEx steht in `engine/konten/rules.json` unter `freigegebene_beine` bei E8, FN und FFN (Backup `rules.json.bak-20261025-vor-opex`). Die Konto-Karten zeigen nach dem Deploy also kein Gelb wegen OpEx. LD01 kommt dort erst in Stufe 2 dazu.

### Was in den neuen JSONs steht

- Die vier alten Module bleiben **unverändert und in derselben Reihenfolge**. OpEx hängt als 5. Modul hinten dran, Parameter genau wie im echten Buch und in der Paritätsprüfung (78/78): Signal 12:00 ET, Schwelle 0,225 × ATR20, Stop 0,75 × ATR20, kein Ziel, `skip_dates` 18.06.2027.
- **Zeit-Exit:** Der Host flattet ab 15:55 ET nur die offenen Module, eins nach dem anderen im Abstand von 15 s, in der JSON-Reihenfolge. OpEx ist das letzte. Selbst wenn alle 5 offen sind, ist OpEx um 15:56:00 ET draußen, das Sicherheitsnetz liegt bei 15:58:00. Mit LD01 als 6. Modul (Stufe 2) wäre es spätestens 15:56:15.
- **FFN-HFT-Regel (Haltedauer über 5 s):** OpEx läuft auch auf FFN **ohne** Stop-Verzögerung. Grund (per Code aus der Paritäts-Datei gerechnet): Der Stop liegt seit 2024 nie näher als 129,6 NQ-Punkte am Entry, in 78 Trades gab es genau einen Stop, und der kam 213 Minuten nach dem Entry. Zum Entry um 12:00:00 ET handelt sonst kein Bein. Ein Rest bleibt nur, wenn genau in diesen 5 Sekunden ein Stop oder Ziel eines anderen Beins in Gegenrichtung fällt, das ist vernachlässigbar.
- **Feiertage OpEx:** Die dritten Freitage bis Ende 2027 sind per Code geprüft. Nur der 18.06.2027 ist ein Börsenfeiertag (Juneteenth fällt auf einen Samstag) und steht in `skip_dates`.
- **Sim-JSON für LD01:** `maxlab_book_host.sim_ld01.json`, Konto Sim101, nur MNQ-Chart, nur LD01 A mit `vix_max` 16. Der M2K-Eintrag auf Sim101 (`sim_rtygap`) bleibt davon unberührt.

## Was du brauchst

PC mit PowerShell, RDP zur Box (`100.127.89.9`), Handy mit Telegram. Zeitfenster: heute Abend oder So 25.10. **bis spätestens 22:00 Boxzeit** (Globex-Open So 23:00). Alles ist Wochenende, die Skripte prüfen Uhrzeit und flat trotzdem selbst.

## Der Deploy in einem Rutsch (ersetzt Teil 1 bis 3, Stand 25.10.)

Ein Skript ruft die drei getesteten Einzel-Skripte in der richtigen Reihenfolge auf und stoppt beim ersten Fehler. Vorher prüft es alles, ohne etwas zu ändern (JSON-Abgleich und Pre-Flight-Compile). PowerShell am PC:

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261025_live
powershell -ExecutionPolicy Bypass -File .\deploy_live_20261025.ps1
```
- Dauer etwa 5 bis 10 Minuten. Es gibt **eine** Rückfrage `Gesamt-Deploy starten? (ja/nein)` → **`ja`**. Danach laufen C) VIX-Feed, D) JSONs, E) LD01-Code (beendet NT8 und startet es neu) ohne weitere Fragen.
- **Erwartet:** viermal `Skript ok`, je Abschnitt eine grüne Zeile `---- … : ok`, am Ende `=== GESAMT-DEPLOY FERTIG`. Die Einzel-Ausgaben sind dieselben wie unten in Teil 1 bis 3 beschrieben (dort stehen sie im Detail).
- **Fehlerfall:** rote Zeile `!!! … endete mit Exit …`. Dann laufen die restlichen Schritte nicht. NT8 nicht selbst starten, in den Hauptkanal **„Deploy Fehler“** schreiben. Claude liest das Log `deploy_live_<Datum-Uhrzeit>.log` im selben Ordner.
- **Prüflauf schon grün** (Claude, So 25.10. 00:10 Boxzeit, `-Check`): alle Skripte im erwarteten Stand, 6× `[OK]` beim JSON-Abgleich, alle Konten flat, `COMPILE OK`, nichts geändert.
- Danach direkt weiter mit **Teil 4** (NT8 per RDP). Teil 1 bis 3 brauchst du nur, falls du einen Schritt einzeln wiederholen musst.

## Teil 1: VIX-Feed starten (startet die Messwoche, NT8 bleibt unberührt)

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_ld01
powershell -ExecutionPolicy Bypass -File .\install_vix_feed.ps1
```
- **Erwartet:** `Feed-Skript MD5 5E67E1052BC928E0C23F315CA0C651D1`, `Aufgabe angelegt: Ready`, eine Logzeile vom Feed, dann die letzten drei Zeilen von `maxlab_vix.csv` im Format `2026-10-23,<Schluss>`. **Die jüngste Zeile muss der 23.10. sein** (Freitag).
- **Fehlerfall:** `scp fehlgeschlagen` oder kein `Aufgabe angelegt` → nichts weiter tun, Ausgabe in den Hauptkanal. Fehlt nur der 23.10. in der CSV, trotzdem weitermachen und **„VIX fehlt“** schreiben, das ist genau, was die Messwoche klären soll.

## Teil 2: Host-JSONs auf die Box (NT8 läuft weiter, Hosts lesen sie erst beim Aktivieren)

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261025_live
powershell -ExecutionPolicy Bypass -File .\deploy_json_20261025.ps1
```
- Frage `JSONs jetzt auf die Box kopieren? (ja/nein)` → **`ja`**.
- **Erwartet:** sechsmal `[OK] … Box <alt> -> neu <neu>`, danach sechsmal `[OK] <datei> -> <neu>` und `=== FERTIG`. Die neuen md5 je Konto:

| Konto | Datei | neue md5 beginnt mit |
|---|---|---|
| E8 50k `E61803453048` | `live_e8_50k.json` | `07288260` |
| FN1 `…71491` | `live_fn1.json` | `0ec947d3` |
| FN2 `…89622` | `live_fn2.json` | `c3b71984` |
| FFN1 `2D-150K394206247048` | `live_ffn150k.json` | `4e87a34f` |
| FFN2 `2D-150K010602681476` | `live_ffn150k_2.json` | `c4d805c2` |
| Sim101 | `sim_ld01.json` | `f114c9f8` |

- **Fehlerfall:** `ABBRUCH: … Abweichung(en)` → jemand hat eine JSON seit 24.10. geändert, nichts wurde kopiert, Ausgabe in den Hauptkanal. `throw … MD5` mitten in Schritt 3 → nicht weitermachen, Hauptkanal; Claude setzt die Datei aus `*.bak-20261025-vor-opex` zurück.

## Teil 3: LD01-Code deployen (beendet NT8)

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_ld01
powershell -ExecutionPolicy Bypass -File .\deploy_ld01_20261024.ps1
```
- Frage `Jetzt deployen? (ja/nein)` → **`ja`**. Das beendet NT8.
- **Erwartet:** je Konto `[OK] … flat`, `COMPILE OK`, `Pre-Flight OK.`, `csproj: ergaenzt Strategies\MaxBookHost_VixFilter.cs`, `csproj ok: 3 Paketdatei(en) …`, `ROLLBACK-BACKUP … deploy-<stamp>`, dreimal `im Baum ok`, `Start-NT8 ausgeloest.`, `Repo-Spiegel engine\ninjascript nachgezogen.`, `=== FERTIG`.
- Was sich ändert: Momentum `1754238F` und MomentumPB3 `170970EB` können jetzt einen VIX-Filter. Ohne `vix_max` in der JSON läuft PB3 bitgleich wie bisher (Dump-Vergleich byte-gleich).
- **Fehlerfall:** `ABBRUCH: ET-Zeit` oder `NICHT FLAT` → nichts passiert, Hauptkanal. `FEHLER im Deploy-Schritt` oder `NACH DEPLOY FALSCH` → **NT8 NICHT selbst starten**, Hauptkanal. Claude rollt über das Backup zurück. Teil 2 bleibt davon unberührt (OpEx braucht keinen neuen Code).

## Teil 4: RDP, alles einschalten und den Sim-Host anlegen

1. NT8-Login (fällt weg, wenn der Auto-Login es selbst macht).
2. Control Center → **Connections:** Tradovate UND Rithmic grün.
3. Im Hauptkanal **„Telegram-Werte“** schreiben. Claude holt Token und ChatId per SSH und zeigt sie dir im Chat, nie im Vault.
4. Reiter **Strategies:** alle 5 Hosts (E8, FN1, FN2, FFN1, FFN2) und alle **5 RiskGuards** aktivieren. Bei jedem RiskGuard `TelegramToken` und `TelegramChatId` mit den Werten aus dem Chat vergleichen. Das deckt gleich den Sonntags-Check aus AP413 mit ab.
   - **Erwartet:** alle Häkchen grün, je Konto eine Telegram-Startmeldung.
   - **Fehlerfall:** Springt ein Host sofort wieder auf deaktiviert, Namen notieren, nicht ständig neu klicken, **„Host aus <Konto>“** in den Hauptkanal. Claude liest den Grund im Log; im Zweifel kommt die alte JSON zurück und das Konto läuft ohne OpEx wie bisher.
5. **Output-Fenster** (New → NinjaScript Output): Je Live-Host muss eine Zeile `MaxOpexMomNQ: OpexMom 2026-10-16: … dir=-1 R=… stop=…` auftauchen. Das ist der OpEx-Freitag vom 16.10. aus der geladenen Historie und beweist, dass der Chart genug Tage hat (ATR20). Im Backtest war das ein Short mit R rund 255 Punkten, auf dem MNQ-Chart weicht R um ein paar Punkte ab.
   - **Fehlerfall:** Steht dort `nicht warm`, den Host-Chart auf **Days to load 45** stellen (rechte Maustaste → Data Series), Host neu aktivieren.
6. **Sim-Host LD01 anlegen:** New → Chart, Instrument `MNQ 12-26`, 1 Minute, Trading hours **US Equities RTH**, **Days to load 60**. Rechte Maustaste → Strategies → `MaxBookHost` hinzufügen, **Account `Sim101`**, ConfigPath leer lassen (der Host findet `sim_ld01.json` über Konto und Instrument), aktivieren.
   - **Erwartet** im Output-Fenster: `HOST BEREIT [..] Konto Sim101, Instrument MNQ 12-26, … sim_ld01.json [per Konto+Instrument] (md5 f114c9f8…) … Module: NQ_LD01_vix16_fv4(MaxLD01VixNQ x1)`.
7. **Feiertags-Bars prüfen** (Auflage strategy-auditor), im Sim-Chart aus Schritt 6: zum **Mo 07.09.2026** (Labor Day) scrollen. **Erwartet:** zwischen Fr 04.09. 16:00 und Di 08.09. 09:31 gibt es keine einzige Bar. Für Thanksgiving 2025 reicht der Dezember-26-Kontrakt nicht zurück, deshalb ein zweiter Chart: Instrument `MNQ 12-25`, 1 Minute, US Equities RTH, Days to load **400**, zum **Do 27.11.2025** (Thanksgiving) scrollen. **Erwartet:** keine Bar am 27.11., am Fr 28.11. Bars nur bis 13:00. Den zweiten Chart danach wieder schließen.
   - Ergebnis als **„Feiertage ok“** oder **„Feiertage: Bars am <Datum>“** in den Hauptkanal. Bars an einem Feiertag heißen: LD01 könnte dort handeln, wo die Engine nicht handelt. Das wäre ein Blocker für Stufe 2, kein Grund zur Panik heute.
8. **RDP nur trennen (Fenster schließen), NICHT abmelden.**
9. Im Hauptkanal **„Deploy fertig“** schreiben.

## Teil 5: Was Claude danach prüft (per SSH, kein Schritt für dich)

- NT8-Log: je Live-Konto `HOST BEREIT` mit der **neuen md5** aus der Tabelle in Teil 2 und am Ende `NQ_OPEXMOM_fv4(MaxOpexMomNQ x1)`, die vier alten Module unverändert davor. Sim101 mit `f114c9f8`.
- Live-Code: Momentum `1754238F`, PB3 `170970EB`, VixFilter `78CABE11`, OpEx `3565F4E9`, Host `C2C4B5A9`, Basis `582D56B5`.
- RiskGuard-Log je Konto: Start, `CONFIG-INAKTIVITAET aktiv=ja`, `CONFIG-KOMMISSION` wie seit 22.10.
- VIX: Task `MaxLab VIX-Feed` läuft alle 15 Minuten, `maxlab_vix.csv` hat den 23.10.
- Danach: Register-Belegung um OpEx ergänzen und einen neuen Kartenlauf anstoßen (konto-analyst), damit die Konto-Karten das 5-Bein-Buch kennen. Tickets AP394 und AP395 fortschreiben.

> [!info] Zwischenstand Di 27.10. 17:26 Boxzeit (Claude per SSH)
> - **VIX-Feed bisher grün:** kein Alarm, Task fehlerfrei. Der Schluss vom 26.10. (18,39) war um 00:01 ET da, 9,65 h vor der LD01-Entscheidung. Der VIX liegt über 16, LD01 hätte nicht gehandelt.
> - **Sim-Host auf Sim101 läuft noch nicht.** Anleitung für Teil B und C ging an die Übersichts-Session (Fenster nach 21:05 oder vor 14:30 Boxzeit).
> - **Verschiebung Stufe 2:** a) volle 5 Sim-Tage 28.10. bis 03.11., Host-JSON frühestens Di 03.11. nach 22:05, erster Live-Trade Mi 04.11. 15:40 Boxzeit (Empfehlung). b) 3 Sim-Tage, dann bleibt es beim Wochenende 31.10./01.11. und Mo 02.11. 15:40.

## Deploy-Abend Mi 28.10.2026 (Entscheidungen Max 27.10.)

Max hat entschieden: volle 5 Sim-Tage, D1 = Stop-Verzögerung nachrüsten (LD01 auch auf FFN), RDP-Block Mi 28.10. etwa 22:30 bis 23:15 Boxzeit. Das passt gut: 22:00 bis 23:00 Boxzeit ist die tägliche Globex-Pause, kein Markt offen.

**Was neu gebaut ist (Claude, 27.10.):** Das Modul `momentum` meldet beim Entry sein R, damit die Stop-Verzögerung wie bei PB3 erlaubt ist (`MaxBookHost_Module_Momentum.cs` `32406B6E` statt `1754238F`). Ohne Verzögerung ändert sich nichts: der LD01-Replay-Report ist byte-gleich zum alten Code (163 von 163), 15 von 15 neue Tests grün, Pre-Flight auf der Box grün. Die Sim-JSON bekommt die Verzögerung wie später auf FFN (10 s, Kat-Stop 2 R), damit der Sim-Lauf den neuen Codepfad mitprüft (`ecfe57a4` statt `f114c9f8`). Staging: `trading-data/nt8_staging_20261028_ld01_delay/`.

**Ablauf für Max:**

0. PowerShell am PC (ab 22:05 Boxzeit, beendet NT8 und startet es neu, etwa 5 Minuten):
   ```
   cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261028_ld01_delay
   powershell -ExecutionPolicy Bypass -File .\deploy_abend_20261028.ps1
   ```
   - Eine Rückfrage `Deploy-Abend starten? (ja/nein)` → **`ja`**.
   - **Erwartet:** dreimal `Paket ok`, `Sim-JSON … wird ersetzt`, `COMPILE OK`, `---- C) … ok`, `[OK] maxlab_book_host.sim_ld01.json -> ecfe57a4…`, `=== DEPLOY-ABEND FERTIG`.
   - **Fehlerfall:** rote Zeile `!!!` → nichts weiter tun, NT8 nicht selbst starten, Stichwort **„Deploy Fehler“**. Claude rollt über das Backup zurück.
1. RDP: NT8-Login (macht der Auto-Login meist selbst), Connections grün, alle 5 Hosts und 5 RiskGuards aktiv (Häkchen). Stichwort **„Hosts aktiv“**.
2. Teil B (Sim-Host auf Sim101) und Teil C (Feiertags-Bars) wie oben in Teil 4 Schritt 6 und 7. Erwartete Zeile für den Sim-Host jetzt mit md5 `ecfe57a4` und `NQ_LD01_vix16_fv4(MaxLD01VixNQ x1 stop_delay 10s cat 2.0R)`.
3. Stichworte **„Sim-Host läuft“** und **„Feiertage ok“** bzw. was zu sehen war.

**Neuer Zeitplan LD01:** Sim-Tage Do 29.10., Fr 30.10., Mo 02.11., Di 03.11., Mi 04.11. Host-JSONs mit LD01 frühestens Mi 04.11. nach 22:05 Boxzeit, erster Live-Trade frühestens **Do 05.11. 15:40 Boxzeit** (09:40 ET, ab 01.11. gilt ET plus 6 Stunden). Auf FFN mit Stop-Verzögerung 10 s / Kat-Stop 2 R, auf E8 und FN ohne.

## Die Messwoche Mo 26.10. bis Fr 30.10. (LD01, kein Schritt für dich außer den Stichworten)

| Auflage | Wer | Wie gemessen | Grün heißt |
|---|---|---|---|
| VIX-Feed eine Woche | Claude liest `maxlab_vix_feed.log` täglich ab 14:45 Boxzeit (Stichwort **„VIX-Check“**) | Uhrzeit, ab der der Vortag in der CSV steht | an allen 5 Tagen vor 09:40 ET (14:40 Boxzeit), kein Telegram-Alarm |
| externer Feed-Wächter | Claude baut ihn diese Woche | prüft unabhängig vom Feed die jüngste Zeile in `maxlab_vix.csv` (Box-Heartbeat oder `auto_check`), meldet per Telegram | Testalarm ist angekommen |
| Feiertags-Bars | du, Teil 4 Schritt 7 | Chart | keine Bars an Feiertagen |
| Sim-Host-Lauf | läuft von selbst auf Sim101 | Claude vergleicht die Sim-Trades am Fr 30.10. nach 22:00 mit der Engine (LD01 mit VIX) | gleiche Tage, gleiche Richtung, Entry und Stop auf ein paar Ticks gleich; Tage mit VIX über 16 ohne Trade |
| FFN-HFT bei LD01 | **du entscheidest** (siehe unten) | | |

### Deine Entscheidung D1: LD01 auf den FFN-Konten

Das Modul `momentum` kann keine Stop-Verzögerung. In der Historie endet 1 von 163 LD01-Trades in der Entry-Minute (das ist eine Obergrenze, nicht jeder davon dauert unter 5 s). Auf FFN reicht bei wenigen Trades am Tag schon ein einziger schneller Round-Trip.

| Option | was passiert | Aufwand |
|---|---|---|
| **a) Stop-Verzögerung nachrüsten (Empfehlung)** | Das Modul meldet sein R, dann gilt auf FFN dieselbe Regel wie bei PB3 (`stop_delay_seconds` 10, `cat_stop_r` 2,0). Neue Paritätsprüfung und Pre-Flight, Deploy in der Messwoche | ein halber Tag Claude, ein Deploy-Abend du |
| b) LD01 auf FFN ohne Schutz | Restrisiko bewusst tragen, wie bei Asia auf FFN | keiner |
| c) LD01 nur auf E8 und FN | FFN bekommt LD01 nicht | keiner, FFN verliert das Bein |

Warum a): Die FFN-Konten haben den meisten Puffer und tragen das Bein am leichtesten, und für PB3 hast du am 09.10. genau diese Regel gewählt. Die Messwoche wartet ohnehin, der Umbau kostet also keine Zeit.

## Stufe 2: LD01 in die Host-JSONs (frühestens Sa 31.10.)

Erst wenn alle Zeilen der Messwoche grün sind und D1 entschieden ist:

1. Claude baut die JSONs mit LD01 als 6. Modul (hinter OpEx), auf FFN je nach D1, lässt konto-analyst laufen und bereitet ein Kopier-Skript wie in Teil 2 vor. Bei Option a) vorher der Code-Deploy mit Pre-Flight.
2. Du startest das Skript und aktivierst die Hosts neu (Wochenende 31.10./01.11., **USA stellt am 01.11. auf Winterzeit um**, ab Mo 02.11. Handel 15:30 bis 22:00 Boxzeit).
3. Erster möglicher LD01-Live-Trade: Mo 02.11. um 09:40 ET (15:40 Boxzeit), nur wenn der VIX-Schluss vom Freitag höchstens 16 war.

## Was nachläuft (nicht dieses Wochenende)

- **OpEx:** Roll MNQ 12-26 auf 03-27 **vor Fr 18.12.** (der OpEx-Tag ist der Verfallstag). 2027-Feiertage im RTH-Template prüfen, betrifft alle Beine, im Dezember. Eigene Ausstiegsregel für das Tail-Bein vor dem 2. Live-Trade (die expR-Regel greift bei rund 7 Trades im Jahr erst nach Jahren), deine Entscheidung.
- **LD01:** eigene Ausstiegsregel (expR-Regel greift erst nach rund 3 Jahren), deine Entscheidung.
- **Nebenbei offen:** E8 50k braucht noch einen Handelstag. Die Konto-Karte nennt als Frist den **30.10.**, die Wochenend-Notiz den 28.10., der frühere Termin gilt bis zur Klärung. OpEx und LD01 helfen dort nicht.

## Quellen

Staging `trading-data/nt8_staging_20261025_live/` (neue JSONs, `deploy_json_20261025.ps1`, diese Session), `nt8_staging_20261022_ld01/` (LD01-Paket, VIX-Feed, Port-Session fa8ff501), `nt8_staging_20261022_opex/` (OpEx-Modul und Paritäts-Dateien). Tickets AP394, AP395. Vorgänger [[Deploy-Abend 22.10.2026 (Anleitung)]], Entscheidung [[Wochenend-Prüfung 24.10.2026]].
