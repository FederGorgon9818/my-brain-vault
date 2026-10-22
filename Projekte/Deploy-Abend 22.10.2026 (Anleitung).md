---
tags: [trading, box, nt8, deploy, export, anleitung]
datum: 2026-10-22
status: Anleitung fertig, Ausführung Max Do 22.10. abends
tickets: [AP319, AP394, AP290, AP415, AP427, AP422, AP433]
---

# Deploy-Abend 22.10.2026: alles in einem Durchgang

Alle Zeiten sind **Boxzeit**. Die Deploy-Skripte prüfen die US-Uhrzeit und ob alle Konten flat sind selbst und brechen sonst von allein ab. Der erste Trade am Freitag kommt um 15:30 Boxzeit (Asia), bis dahin muss alles wieder aktiv sein, besser heute Nacht.

**Hauptkanal** ist die Ticket-Session „Offene Tickets und Backlog-Prioritäten“. Die **fett** gedruckten Stichworte schreibst du dort hinein, Claude macht den Rest.

Stand vor dem Abend (Claude per SSH, 22.10. ca. 22:10): live RiskGuard `DBEAC7AF`, Host-Basis `582D56B5`, das OpEx-Modul ist noch nicht auf der Box. NT8 läuft seit 20.10. 17:41.

**Nicht dabei:** LD01 (die Port-Session baut gerade beide Varianten, das Staging ist noch nicht fertig) und AP413 (Wochenend-Abbruch, noch nicht gebaut).

## Was du brauchst

- PC mit PowerShell, RDP zur Box (`100.127.89.9`), Handy mit Telegram.

## Teil 1: Vorprüfung beider Deploys (NT8 läuft weiter, nichts wird verändert)

> [!success] Schon erledigt, 22.10. ca. 22:10 von Claude
> Beide Vorprüfungen sind grün: alle Konten flat, `COMPILE OK`, `Pre-Flight OK.`, nichts deployt. Du kannst direkt mit Teil 2 anfangen. Nur falls du erst viel später loslegst, die zwei Befehle unten noch einmal laufen lassen.

PowerShell am PC:
```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_ap319
powershell -ExecutionPolicy Bypass -File .\deploy_20261022_ap319.ps1 -PreflightOnly
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_opex
powershell -ExecutionPolicy Bypass -File .\deploy_20261024.ps1 -PreflightOnly
```
- **Erwartet:** je Skript `Paket: … MD5 … ok` (RiskGuard `312C74C9…`, OpEx `3565F4E9…`), je Konto `[OK] … flat` und am Ende `Nur Vorpruefung: Pre-Flight gruen, nichts deployt.`
- **Fehlerfall:** `PRE-FLIGHT FEHLGESCHLAGEN` oder ein `throw … MD5` → nichts weiter deployen, Ausgabe in den Hauptkanal.

## Teil 2: Deploy A = RiskGuard Trade-PnL-Fix (AP319)

> [!success] Schon erledigt, 22.10. 22:08 bis 22:10 (Session b547a17b, auf deine Freigabe)
> Live ist `MaxRiskGuard.cs` jetzt `312C74C9`, die DLL stammt von 22:10:23, alle 5 `commissionrt`-Zeilen stehen in der cfg (E8/FN 1.90, FFN 1.78). Claude hat das um 22:12 per SSH nachgeprüft. NT8 läuft seit 22:10:31 neu, **deshalb sind gerade alle Strategien aus**. **Teil 2 nicht nochmal starten**, sondern direkt mit Teil 3 weitermachen. Rollback: `_bak_archiv\deploy-20261022-2210` plus `_bak_archiv\d1022-20261022-2209\cfg`.

Was er bringt: Telegram zeigt den Trade-Gewinn je Exit richtig an (aus den Fill-Preisen minus Kommission) statt der falschen −1 $. Die cfg bekommt je Konto eine Zeile `commissionrt`, und zwar nur dort, wo sie fehlt.

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_ap319
powershell -ExecutionPolicy Bypass -File .\deploy_20261022_ap319.ps1
```
- Frage `Jetzt deployen? (ja/nein)` → **`ja`**. Das beendet NT8.
- **Erwartet:** `ROLLBACK-BACKUP … deploy-<stamp>`, `im Baum ok`, `in DLL ok` …, `Start-NT8 ausgeloest.`, `=== FERTIG`.
- **Noch nicht einloggen.** Gleich weiter mit Teil 3, der beendet NT8 sowieso noch einmal.
- **Fehlerfall:** `ABBRUCH: ET-Zeit` → 5 Minuten warten, nochmal. `NICHT FLAT`, `FEHLER im Deploy-Schritt`, `NICHT IN DLL` oder `cfg NICHT ergaenzt` → NT8 NICHT starten, Teil 3 auslassen, Ausgabe in den Hauptkanal. Claude rollt dann über das Backup zurück.

## Teil 3: Deploy B = OpEx-Modul (AP394)

Was er bringt: Das Modul `opexmom` ist danach in der NT8-DLL. **Es handelt noch nicht**, weil es in keiner Host-Config steht. Live geht es erst nach deiner Wochenend-Entscheidung.

```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_opex
powershell -ExecutionPolicy Bypass -File .\deploy_20261024.ps1
```
- Frage `Jetzt deployen? (ja/nein)` → **`ja`**.
- **Erwartet:** `csproj: ergaenzt Strategies\MaxBookHost_Module_OpexMom.cs`, `csproj ok`, `ROLLBACK-BACKUP …`, `im Baum ok: MaxBookHost_Module_OpexMom.cs`, 7× `in DLL ok` (inklusive `MaxBookModuleOpexMom` und `MaxRiskGuard`), `Start-NT8 ausgeloest.`, `=== FERTIG`.
- **Fehlerfall:** wie Teil 2. Wichtig: Wenn Teil 2 grün war und Teil 3 scheitert, NT8 trotzdem nicht selbst starten, sondern in den Hauptkanal schreiben. Claude setzt dann nur das OpEx-Paket zurück, und der RiskGuard-Fix bleibt.

## Teil 4 (optional, ca. 15 Minuten): Auto-Login einspielen (AP415)

Danach loggt sich NT8 nach einem Neustart selbst ein. Wenn du heute keine Lust hast, überspring es, dann geht es direkt mit Teil 5 weiter.

1. PowerShell am PC:
   ```
   scp C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_autologin\nt8_autologin.ps1 C:\Users\maxlk\Projects\trading-data\nt8_staging_20261022_autologin\register_nt8_autologin_task.ps1 Administrator@100.127.89.9:C:/Users/Administrator/
   ```
   Erwartet: keine Ausgabe.
2. **RDP**, PowerShell auf der Box:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\Administrator\nt8_store_credential.ps1
   ```
   Die NT-Mail und das Passwort tippst du selbst ein. Das Skript zeigt nur die Länge an.
3. In RDP:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\Administrator\register_nt8_autologin_task.ps1
   ```
   Erwartet: `Task 'MaxLab NT8 Login' angelegt.` und Log-Zeilen vom Wächter.
4. Test in RDP, nur zuschauen:
   ```
   powershell -NoProfile -ExecutionPolicy Bypass -Command ". C:\Users\Administrator\nt8_control.ps1; Stop-NT8Clean; Start-NT8; Wait-NT8Ready -TimeoutSeconds 240"
   ```
   **Grün:** NT8 loggt sich in etwa 30 s selbst ein, die Connections werden grün. Danach im Hauptkanal **„Auto-Login Test 1“** schreiben, Claude liest das Log.
   **Fehlerfall:** Loggt es sich nach 4 Minuten nicht ein, selbst einloggen und im Hauptkanal **„Auto-Login klappt nicht“** schreiben. Der Rest des Abends ist davon nicht betroffen.
   Der zweite Test (RDP getrennt, Neustart per SSH) kommt am Wochenende, nicht heute.

## Teil 5: RDP, alles wieder einschalten

1. NT8-Login (fällt weg, wenn der Auto-Login aus Teil 4 schon eingeloggt hat).
2. Control Center → **Connections:** Tradovate UND Rithmic grün.
3. Im Hauptkanal **„Telegram-Werte“** schreiben. Claude holt Token und ChatId per SSH und zeigt sie dir im Chat, nie im Vault.
4. Reiter **Strategies:** alle Hosts aktivieren (E8, FN1, FN2, FFN1, FFN2) und alle **5 RiskGuards**. Bei jedem RiskGuard `TelegramToken` und `TelegramChatId` mit den Werten aus dem Chat vergleichen.
   - **Erwartet:** alle Häkchen grün, je Konto eine Telegram-Startmeldung aufs Handy.
   - **Fehlerfall:** Springt eine Instanz sofort wieder auf deaktiviert, den Namen notieren, nicht ständig neu klicken, in den Hauptkanal schreiben.
5. Im Hauptkanal **„Deploy fertig“** schreiben. Claude prüft per SSH das NT8-Log, `HOST BEREIT` je Konto, im RiskGuard-Log je Konto die Zeile `CONFIG-KOMMISSION '<Konto>': commissionrt=… -> Trade-PnL je Exit netto` und `CONFIG-INAKTIVITAET aktiv=ja`.

## Teil 6: Downloads und Export (AP422/AP311, AP427)

Erst wenn Teil 5 grün ist.

a) Control Center → Reiter **Positions:** alle Konten flat.

b) **Tools → Historical Data → links „Load“**, Verbindung **Tradovate**, nur **Last**, Ende **22.10.2026**:

| Instrument (so eintippen) | Datentyp | Start | Wofür |
|---|---|---|---|
| `BTC ##-##` (alle Kontrakte) | Minute | 01.12.2017 | Krypto-Standbein (AP422) |
| `MBT ##-##` (alle Kontrakte) | Minute | 01.05.2021 | Krypto-Standbein (AP422) |
| `MNQ 12-26` | **Tick** | 05.10.2026 | 15:55-Sprung (AP427) |

- **Erwartet:** je Zeile ein paar Minuten, kein Fehler.
- **Fehlerfall:** Kommt bei MNQ Tick über Tradovate nichts an, dasselbe über **Rithmic** versuchen. Klappt es dort auch nicht, notieren und weitermachen.

c) **Tick-Datei exportieren:** im selben Fenster links **„Export“**: Instrument `MNQ 12-26`, Typ **Tick**, 05.10.2026 bis 22.10.2026, speichern als `C:\Users\Administrator\Desktop\NT8_Export\MNQ_12-26_tick.txt`.

d) **Erst wenn alle Downloads durch sind:** Control Center → New → **„Max Bulk Export (1m)“** (NICHT „TEST“). Er läuft still, letztes Mal etwa eine halbe Stunde. Am Ende liegt `C:\Users\Administrator\Desktop\NT8_Export\_DONE.txt`. **Fehlerfall:** NT8 hängt → NT8 NICHT beenden, in den Hauptkanal schreiben.

e) Im Hauptkanal **„Export fertig“**. Claude verteilt den Rest: BTC/MBT-Parquets an die Export-Session, die Tick-Auswertung `tick_burst.py` an AP427.

## Teil 7: Schluss

1. Reiter Strategies: alle Hosts und alle 5 RiskGuards aktiv, Telegram-Felder gefüllt.
2. Handy: Die Startmeldungen der RiskGuards sind angekommen.
3. **RDP nur trennen (Fenster schließen), NICHT abmelden.**

## Quellen

Deploy-Skripte in `trading-data/nt8_staging_20261022_ap319` (Session b547a17b) und `nt8_staging_20261022_opex` (Port-Session), Auto-Login aus der AP134-Session vom 18.10. (gesichert nach `nt8_staging_20261022_autologin`), Ablauf wie [[Einrichtung Fr 16.10.2026 (alles auf einen Schlag)]], Tickets AP319, AP394, AP415, AP427.
