---
tags: [trading, box, nt8, deploy, anleitung]
datum: 2026-10-15
status: Anleitung fertig, Ausführung durch Max heute Abend
tickets: [AP381, AP382, AP376, AP330, AP356]
---

# Live-Stellung Do 15.10.2026 (Anleitung)

Geprüft um 20:00 Boxzeit von der geplanten Session (nur gelesen, nichts auf der Box geändert). Alle Zeiten Boxzeit (deutsche Zeit, heute ET + 6 h). Alle Beine sind ab 21:58 flat, Markt 23:00 bis 00:00 zu.

## Prüfergebnis 20:00 (Stopp-Punkte zuerst)

**Kein harter Stopp-Punkt.** Zwei Dinge musst du wissen:

1. **Host-Datei im Deploy-Paket ist `582D56B5`, nicht `fcbaa85c`.** Gewollt: AP381 hat am 15.10. 09:30 auf den AP382-Fix noch drei Härtungen gesetzt (kein Lost-Wakeup, kein Doppel-Exit über Tick-Retry, Exit-Storno von außen; 291/291 Tests). Das Deploy-Skript prüft genau diese MD5. Der RiskGuard im Paket ist weiter `5F45B10A`, damit passt v2 (`DBEAC7AF`) ohne Neuaufsetzen.
2. **Das Deploy-Skript erwähnt im Kopf noch AP330 und eine Datei `riskguard_cfg_ap330.txt`.** Die Datei liegt nicht im Ordner, also hängt das Skript nichts an die cfg. Im RiskGuard `5F45B10A` steckt keine alte AP330-Fassung (`RgActivityMath` 0 Treffer). Passt so. Taucht beim Lauf trotzdem die Zeile `Paket: riskguard_cfg_ap330.txt` auf: mit `nein` abbrechen.

| Prüfung | Ergebnis |
|---|---|
| Box erreichbar | ja, 20:01 |
| NT8 | läuft seit 11.10. 19:22, reagiert, RDP-Sitzung angemeldet (getrennt) |
| RiskGuard live | `205A1900` (wie erwartet, nichts deployt) |
| Host ModuleBase live | `6F21447A` (Basis des Pakets) |
| NT8-Log heute | 0 Fehler, 0 Exceptions, 0 disabled, 0 Disconnects, 0 Rejected. FN1 handelt wieder (PHLong 13:30) |
| Paket AP381/AP382 | Host `582D56B5`, RiskGuard `5F45B10A`, Skript `deploy_20261014.ps1` |
| Paket v2 | RiskGuard `DBEAC7AF`, enthält den Waisen-Fix, Tests `GESAMT: PASS` (Inaktivität 27/27) |
| cfg live | nur die alten `inactivityalarmdays=4`, noch keine v2-Zeilen. `maxlab_holidays.txt` liegt noch nicht auf der Box |
| Export | `Desktop\NT8_Export` gibt es nicht, ist also noch nicht gelaufen. Alt gesichert: `NT8_Export_20260919` |
| Teil-A-Daten | alle 13 Kontrakte müssen geladen werden (siehe Schritt 3) |
| Feiertagsliste | siehe Abschnitt unten |

## Bevor du anfängst (deine Entscheidungen)

- [ ] **AP381/AP382-Deploy freigeben.** Der strategy-auditor hat Host deploybar, RiskGuard deploybar mit Auflage gesagt: die neue Waisen-Schließung per Gegenorder ist live noch nie gelaufen (Sim101-Probe empfohlen, nicht gemacht).
- [ ] **Kaufdaten für `inactstart` bestätigen** (laut Belegen): E8 `E61803453048` **28.07.2026**, FN1 und FN2 **02.09.2026**, FFN1 `2D-150K394206247048` **05.10.2026**, FFN2 `2D-150K010602681476` **08.10.2026**. Zu spätes Datum = Frist zu spät = gefährlich. Unsicher bei einem Konto: lieber ein früheres Datum.
- [ ] **Ein oder zwei Deploys.** Empfehlung: zwei (erst AP381/AP382 per fertigem Skript, dann v2). Alternative: ein Deploy mit Host `582D56B5` plus RiskGuard v2 `DBEAC7AF`, weil v2 den AP381-Fix schon enthält. Vorteil: ein NT8-Neustart weniger, rund 20 Min gespart. Nachteil: das getestete Skript muss dafür umgebaut werden (erwartete MD5, cfg-Schritt), und geht etwas schief, weißt du nicht, welcher Teil es war.
- [ ] **Deploy-Session öffnen:** eine Claude-Session, die mit dir zusammen deployt. Dort läuft wegen der Konto-Sperre zuerst `konto-analyst` (Hook-Pflicht vor jeder cfg-Änderung). Deploy 2 fährt diese Session mit deinem OK, du schaust zu und klickst per RDP.

## Ablauf heute Abend

### 1. Ab 22:05: Deploy 1 = AP381 + AP382

Das Skript bricht vor 22:05 (16:05 ET) von selbst ab, also nicht früher starten.

1. **PowerShell am PC:**
   ```
   cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261014_deploy
   .\deploy_20261014.ps1
   ```
   Ohne `-Yes`, dann fragt es vor dem NT8-Stopp nach.
   **Erwartet:** `Paket: MaxBookHost_ModuleBase.cs MD5 582D56B5… ok` und `Paket: MaxRiskGuard.cs MD5 5F45B10A… ok`, KEINE Zeile `riskguard_cfg_ap330.txt`. Schritt 1: `ET: Thu 2026-10-15 16:0x`, je Konto `[OK] … flat`. Schritt 3: `wird ersetzt (live 6F21447A)` und `wird ersetzt (live 205A1900)`, `COMPILE OK`, `Pre-Flight OK.`
   **Fehlerfall:** Abbruch in Schritt 1 oder 3 = nichts verändert. `NICHT FLAT` → im Control Center Positions prüfen, Claude melden. `ABBRUCH: ET-Zeit` → ein paar Minuten warten, neu starten. `PRE-FLIGHT FEHLGESCHLAGEN` → Claude melden, heute kein Deploy, weiter mit Schritt 3 (Export).
2. Frage `Jetzt deployen? (ja/nein)` → **`ja`**.
   **Erwartet:** `ROLLBACK-BACKUP … deploy-<stamp>` (Pfad notieren), `im Baum ok:` für beide Dateien, 9× `in DLL ok:` (u.a. `exitSending`, `CloseOrphans`, `RgOrphanConfirm`), keine `cfg:`-Zeile, dann `Start-NT8 ausgeloest.` und `=== FERTIG`.
   **Fehlerfall:** `FEHLER im Deploy-Schritt` oder `NICHT IN DLL` → NT8 NICHT starten, Claude melden. Rollback: aus dem genannten Backup-Ordner `MaxRiskGuard.cs`, `MaxBookHost_ModuleBase.cs`, `NinjaTrader.Custom.dll`, `NinjaTrader.Custom.csproj` zurück (macht die Deploy-Session).
3. **RDP auf die Box:** NT8-Login, Control Center → Connections: Tradovate UND Rithmic grün (FFN läuft über Rithmic).
4. **Reiter Strategies:** alle Hosts aktivieren (E8, FN1, FN2, FFN1 + RTY-Instanz, FFN2 + RTY-Instanz, dazu die Einzelinstanzen) und alle **5 RiskGuards**. Bei jedem RiskGuard in den Properties `TelegramToken` und `TelegramChatId` prüfen (Werte: `C:\Users\Administrator\maxlab_watchdog.json` auf der Box, die Session nennt sie dir im Chat, nie in den Vault).
   **Erwartet:** alle Häkchen grün, nach dem Aktivieren Telegram-Startmeldungen je Konto.
   **Fehlerfall:** eine Instanz springt sofort wieder auf deaktiviert → Name notieren, Claude melden, nicht wiederholt anklicken.
5. **Log-Check** (Deploy-Session macht das per SSH, oder du selbst):
   ```
   ssh Administrator@100.127.89.9 "powershell -NoProfile -Command \"Select-String -Path 'C:\Users\Administrator\Documents\NinjaTrader 8\log\log.20261015.00000.en.txt' -Pattern '\|ERROR\||Exception|disabled' | Select-Object -Last 10\""
   ```
   **Erwartet:** keine neuen Zeilen nach dem Neustart. **Fehlerfall:** Zeilen da → Claude zeigen, bevor Deploy 2 startet.
6. Ticket-Stand: AP381/AP382 bleiben offen bis zum ersten Tag mit offener Position um 15:55 ET (Beleg), dann mit AP340/AP315 schließen.

### 2. Danach (spätestens Start 22:40): Deploy 2 = Inaktivitäts-Paket v2

Startregel (meine Wahl, damit der Export nicht wieder kippt): ist Deploy 1 um 22:40 nicht sauber durch, Deploy 2 auf Freitag 16.10. ab 22:05 verschieben und direkt zu Schritt 3.

Grundlage: `C:\Users\maxlk\Projects\trading-data\nt8_staging_20261014_inaktivitaet\v2\DEPLOY.md` Abschnitte 1, 3, 4, 5. Die Deploy-Session führt aus, du gibst je Schritt OK:

1. **Basis prüfen:** MD5 von `MaxRiskGuard.cs` auf der Box muss jetzt **`5F45B10A…`** sein (Deploy 1 live).
   **Fehlerfall:** noch `205A1900` → Deploy 1 ist nicht durch, Deploy 2 nicht starten. Etwas Drittes → STOPP, v2 muss neu aufgesetzt werden.
2. **Pre-Flight im Wegwerf-Ordner wiederholen** (Host hat sich durch Deploy 1 geändert): alle `Max*.cs` außer RiskGuard plus v2-RiskGuard in `_preflight_inact2_20261015`, `_check_compile.ps1 -SrcDir …`. **Erwartet:** `COMPILE OK - keine Fehler`, Ordner danach löschen. **Fehlerfall:** Compile-Fehler → Deploy 2 abbrechen, Freitag.
3. **Staging:** `_staging` leer, v2-`MaxRiskGuard.cs` per scp nach `C:/Users/Administrator/_staging/`, MD5 auf der Box = **`DBEAC7AF…`**.
4. **NT8 stoppen und bauen:** `. C:\Users\Administrator\nt8_control.ps1`, `Stop-NT8Clean` (bis kein NinjaTrader-Prozess mehr da ist), `& C:\Users\Administrator\box_deploy.ps1`.
   **Erwartet:** `BACKUP -> …\_bak_archiv\deploy-<stamp>`, `DEPLOYED: MaxRiskGuard`, `Build succeeded`, `DLL gesetzt`, `Artefakt entfernt: obj\` und `bin\`.
   **Fehlerfall:** Build-Fehler → Rollback aus dem neuen Backup-Ordner, NT8 mit dem Stand von Deploy 1 starten.
5. **Solange NT8 gestoppt ist, die cfg ergänzen:**
   - Backup: `maxlab_riskguard.cfg` → `maxlab_riskguard.cfg.bak-20261015-vor-inact2`
   - die fünf Blöcke aus `cfg_inaktivitaet_vorschlag.md` anhängen, mit deinen bestätigten Kaufdaten, `inactminitrade=0` bei allen fünf (UTF-8 ohne BOM, CRLF). Die alten `inactivityalarmdays=4` bleiben stehen.
   - `maxlab_holidays.txt` (korrigierte Fassung, siehe Abschnitt Feiertage) nach `C:\Users\Administrator\Documents\NinjaTrader 8\`
   - Gegenprobe: `Select-String -Path <cfg> -Pattern 'inact'` zeigt pro Konto die alte Zeile plus 8 (FFN 9) neue, jede `inactminitrade=0`.
6. **`Start-NT8`, RDP:** Login, Connections grün, alle Hosts und alle 5 RiskGuards wieder aktivieren (die cfg wird beim Aktivieren gelesen), Telegram-Felder wie in 1.4 prüfen.
7. **Log-Check je Konto** (`maxlab_riskguard_log_<Konto>.txt`, die Session liest per `Select-String`):
   **Muss drinstehen:** `CONFIG-INAKTIVITAET '<Konto>': aktiv=ja … Start=<Kaufdatum> … Mini-Trade=aus`, `INAKTIVITAET: Feiertage N Schliesstage`, beim ersten Start `INAKTIVITAET-RUECKFUELLUNG: N qualifizierte Tage ab Kontostart`, nach ca. 20 s `INAKTIVITAET-STATUS: …`. Daneben die Dateien `maxlab_inact_<Konto>.txt` und `maxlab_inact_status_<Konto>.txt` (Feld 10 ändert sich mindestens alle 30 s).
   **Darf nicht drinstehen:** `CONFIG ABGEWIESEN`, `INAKTIVITAET-INIT-FEHLER`, `INAKTIVITAET-TICK-FEHLER`, `neue Regel NICHT aktiv`, `Feiertagsliste … FEHLT`, `nicht schreibbar`.
   **Plausibel:** E8 laut Konto-Karte vom 14.10.: Frist 20.10., 1 Tag fehlt (inzwischen evtl. erledigt). FFN1/FFN2 hatten am 13.10. noch keinen Tag ≥ 5 $.
   **Fehlerfall:** Rückfüllung falsch → `maxlab_inact_<Konto>.txt` löschen, Instanz neu aktivieren. Fehlerzeilen → schneller Rollback: inact-Zeilen raus (cfg-Backup zurück), RiskGuards deaktivieren und aktivieren, der alte Zähler läuft wieder.

### 3. 23:05 bis 23:50: NT8-Export Teil A (AP356)

**Stopp-Regel:** sind die Deploys um 23:05 nicht sauber durch (alle Hosts und RiskGuards aktiv, Log ohne Fehler), den Export auf Freitag 16.10. ab 23:05 verschieben, nicht über 00:00 laufen lassen. **Teil B (SI, HG, PL, 6J, BTC, MBT, MET, Tick-Test, Export 2) kommt am Wochenende, nicht heute** (Entscheidung 15.10. vormittags, gilt auch gegen die Ticket-Notiz von 09:30).

a) **RDP, Control Center, Reiter Positions:** alle Konten flat. **Fehlerfall:** offene Position → nicht exportieren, Claude melden.

b) **Tools → Historical Data → links „Load“:** diese 13 Kontrakte, **nur Minute, nur Last, Start 01.07.2026, Ende 15.10.2026**, Download:

| Kontrakt | Stand auf der Box 20:00 |
|---|---|
| NQ 12-26 | nur 30.09. bis 09.10. |
| ES 12-26 | nur 30.09. bis 09.10. |
| YM 12-26 | nur 30.09. bis 09.10. |
| RTY 12-26 | fehlt ganz |
| GC 12-26 | 24.07. bis 09.10., lückenhaft |
| CL 09-26 | nur 24.07. |
| CL 10-26 | fehlt |
| CL 11-26 | nur 30.09. bis 09.10. |
| CL 12-26 | fehlt |
| 6E 12-26 | fehlt |
| 6B 12-26 | fehlt |
| ZN 12-26 | fehlt |
| ZB 12-26 | fehlt |

**Erwartet:** wenige Minuten, kein Fehler. **Fehlerfall:** Kontrakt mit Fehler notieren und weitermachen. Verbindung grau → Tradovate-Verbindung prüfen, NICHT die Rithmic-Verbindung nehmen.

c) **Erst wenn alle Downloads durch sind:** Control Center → New → **„Max Bulk Export (1m)“** (NICHT „TEST“). **Erwartet:** läuft ca. 35 Min still, am Ende liegt `C:\Users\Administrator\Desktop\NT8_Export\_DONE.txt`. **Fehlerfall:** NT8 hängt oder `_DONE.txt` kommt bis 23:50 nicht → NT8 NICHT beenden, Claude melden.

d) In der Session **„NT8-Export Oktober (AP356 und Folgetickets)“** sagen: **„Export fertig“**. Rohdaten holen, Continuous mit Roll-Check, Vola und Konto-Karten macht Claude dort.

### 4. Vor 00:00: Schlusskontrolle

1. Reiter Strategies: alle Hosts und alle **5 RiskGuards** aktiv, Telegram-Felder gefüllt.
2. Kurz aufs Handy: Telegram-Startmeldungen der RiskGuards sind angekommen.
3. **RDP nur trennen (Fenster schließen), NICHT abmelden.** Der Wiederanlauf braucht die angemeldete Sitzung (AP86).

## Feiertagsliste `maxlab_holidays.txt`

Geprüft per research-scout am 15.10. (Research-Cache hatte nichts, neu eingetragen). **Die vier vollen Schließtage stimmen, es fehlt keiner. Die Datei kann so auf die Box.**

| Datum | Liste | Quellen |
|---|---|---|
| 25.12.2026 | zu | zu |
| 01.01.2027 | zu | zu |
| 26.03.2027 Karfreitag | zu | zu (kein NFP-Sonderfall 2027) |
| 24.12.2027 | zu | zu (Weihnachten beobachtet) |

Einschränkungen:
- Belegt nur über Praktiker-Quellen (financecalendar.com, mrtopstep.com, crosstrade.io). Die CME-Seite selbst lief zweimal in einen Timeout, 2027 ist nach der üblichen Regel abgeleitet.
- In den Kommentaren der Datei fehlen zwei Frühschlüsse: **27.11.2026** und **26.11.2027** (Tag nach Thanksgiving, 12:15 CT). Das sind Handelstage, also kein Fehler für den Guard, nur eine unvollständige Kommentarzeile.
- Thanksgiving 2026: eine Quelle sagt „Closed“, eine „Frühschluss 12:00“. Der Guard behandelt den Tag als Handelstag. Falls CME doch voll schließt, rechnet er dort eine Frist einen Handelstag zu früh, also auf der sicheren Seite.
- Silvester 31.12.2027 steht in keiner Quelle, als Handelstag angenommen. Vor Ende 2027 nachsehen.

## Quellen

Tickets AP381, AP382, AP376, AP330, AP356 (Stand 15.10. 09:32), `nt8_staging_20261014_deploy\deploy_20261014.ps1`, `nt8_staging_20261014_inaktivitaet\v2\DEPLOY.md` und `cfg_inaktivitaet_vorschlag.md`, Box per SSH 15.10. 20:01. Verwandt: [[Firm-Regeln je Konto]], [[VPS-Einrichtung Schritt für Schritt]], [[Neue Märkte (NT8-Daten) Plan]].
