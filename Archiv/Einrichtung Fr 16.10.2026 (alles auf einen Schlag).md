---
tags: [trading, box, nt8, deploy, export, anleitung]
datum: 2026-10-16
status: Anleitung fertig, Ausführung Max Fr 16.10. ab 22:05 Boxzeit
tickets: [AP159, AP381, AP382, AP376, AP330, AP356, AP313, AP196, AP311, AP367, AP371, AP386]
---

# Einrichtung Fr 16.10.2026: alles auf einen Schlag

Eine Liste für Freitagabend, zusammengeführt aus allen Ticket-Sessions vom 14./15.10. Alle Zeiten sind **Boxzeit** (deutsche Zeit, ET + 6 h). Details und alle Fehlerfälle zu Deploy 1 und 2 stehen in [[Live-Stellung 15.10.2026 (Anleitung)]], die Reihenfolge hier hat Vorrang.

**Hauptkanal ist die Ticket-Session** (Reiter „Ticket“, „Offene Tickets und Backlog-Prioritäten“). Dort schreibst du die fett gedruckten Stichworte, Claude macht den Rest und verteilt es an die Sessions.

**Dauer:** grob 22:05 bis 00:00. Nach 23:00 ist der Markt bis Sonntag zu, ab da gibt es keinen Zeitdruck mehr.

## Was du brauchst

- PC an, Claude-App offen, PowerShell, RDP-Verbindung zur Box (`100.127.89.9`).
- Handy mit Telegram (Startmeldungen der RiskGuards).

## 1. 22:05: Phantom-Zeilen bereinigen (AP159, 1 Minute)

PowerShell am PC:
```
ssh Administrator@100.127.89.9 "python C:\Users\Administrator\ap159_clean_executions.py --apply"
```
- **Erwartet:** am Ende `OK: Backup ...bak-...-vor-ap159, ... Datei ersetzt`.
- **Fehlerfall:** jede andere letzte Zeile → Ausgabe in den Hauptkanal kopieren, trotzdem mit Schritt 2 weitermachen (die Datei ist nicht im Deploy).

## 2. Direkt danach: Deploy 1 = FN1-Fix (AP381/AP382)

PowerShell am PC:
```
cd C:\Users\maxlk\Projects\trading-data\nt8_staging_20261014_deploy
.\deploy_20261014.ps1
```
- **Erwartet:** `Paket: MaxBookHost_ModuleBase.cs MD5 582D56B5… ok` und `Paket: MaxRiskGuard.cs MD5 5F45B10A… ok`, je Konto `[OK] … flat`, `COMPILE OK`, `Pre-Flight OK.`
- Frage `Jetzt deployen? (ja/nein)` → **`ja`**.
- **Erwartet danach:** `ROLLBACK-BACKUP … deploy-<stamp>` (Pfad notieren), `im Baum ok:` für beide Dateien, 9× `in DLL ok:`, `Start-NT8 ausgeloest.`, `=== FERTIG`.
- **Fehlerfall:** `ABBRUCH: ET-Zeit` → 5 Minuten warten, neu starten. `NICHT FLAT`, `PRE-FLIGHT FEHLGESCHLAGEN`, `FEHLER im Deploy-Schritt` oder `NICHT IN DLL` → NT8 NICHT starten, Ausgabe in den Hauptkanal, Deploy 2 fällt dann aus, weiter mit Schritt 5 (Export).

## 3. RDP: alles wieder einschalten (nach Deploy 1)

1. RDP auf die Box, NT8-Login.
2. Control Center → **Connections:** Tradovate UND Rithmic grün.
3. Im Hauptkanal **„Telegram-Werte“** schreiben. Claude holt Token und ChatId per SSH und zeigt sie dir im Chat (nie im Vault).
4. Reiter **Strategies:** alle Hosts aktivieren (E8, FN1, FN2, FFN1 plus RTY-Instanz, FFN2 plus RTY-Instanz) und alle **5 RiskGuards**. Bei jedem RiskGuard `TelegramToken` und `TelegramChatId` gegen die Werte aus dem Chat prüfen.
   - **Erwartet:** alle Häkchen grün, je Konto eine Telegram-Startmeldung aufs Handy.
   - **Fehlerfall:** eine Instanz springt sofort wieder auf deaktiviert → Name notieren, nicht wiederholt klicken, in den Hauptkanal schreiben.
5. Im Hauptkanal **„Deploy 1 fertig“** schreiben. Claude prüft das NT8-Log per SSH.

## 4. Deploy 2 = Inaktivitäts-Alarm v2 (AP376/AP330)

Das macht Claude komplett per SSH: Basis prüfen (RiskGuard `5F45B10A`), Pre-Flight, Staging (`DBEAC7AF`), NT8 stoppen, Build, cfg mit deinen bestätigten Kaufdaten (E8 28.07., FN1/FN2 02.09., FFN1 05.10., FFN2 08.10.), Feiertagsliste, NT8 starten. **Du wartest**, bis im Hauptkanal steht „NT8 läuft wieder“.

Startregel: Ist Deploy 1 um 22:40 nicht sauber durch, fällt Deploy 2 heute aus, dann direkt zu Schritt 5.

Danach **RDP: noch einmal wie Schritt 3.2 bis 3.4** (Connections, alle Hosts, alle 5 RiskGuards, Telegram-Felder). Die cfg wird beim Aktivieren gelesen. Dann im Hauptkanal **„Deploy 2 fertig“**. Claude prüft je Konto `CONFIG-INAKTIVITAET … aktiv=ja` und dass keine Fehlerzeile da ist.

## 5. Ab 23:00: NT8-Export (AP356, AP313, AP196, AP311, AP367)

Erst wenn nach den Deploys alle Strategien wieder aktiv sind.

a) Control Center → Reiter **Positions:** alle Konten flat. **Fehlerfall:** offene Position → nicht exportieren, Hauptkanal.

b) **Tools → Historical Data → links „Load“**, je Zeile: **nur Minute, nur Last, Ende 16.10.2026**, Download. Verbindung Tradovate, NICHT Rithmic.

| Teil | Instrument | Start |
|---|---|---|
| A | NQ 12-26, ES 12-26, YM 12-26, RTY 12-26 | 01.07.2026 |
| A | GC 12-26 | 01.07.2026 |
| A | CL 09-26, CL 10-26, CL 11-26, CL 12-26 | 01.07.2026 |
| A | 6E 12-26, 6B 12-26, ZN 12-26, ZB 12-26 | 01.07.2026 |
| B | SI, HG, PL, 6J (alle Kontrakte) | 01.12.2015 |
| B | BTC (alle Kontrakte) | 01.12.2017 |
| B | MBT (alle Kontrakte) | 01.05.2021 |
| B | MET (alle Kontrakte) | 01.12.2021 |

- **Erwartet:** je Zeile wenige Minuten, kein Fehler. **Fehlerfall:** Kontrakt mit Fehler notieren und weitermachen.

c) **Tick-Test:** im selben Fenster ES **Tick** ab 01.01.2016 anfordern. Nur anstoßen, Claude prüft danach, ab wann Dateien in `db\tick` ankommen. Hängt es länger als 10 Minuten, abbrechen, ist kein Muss.

d) **Erst wenn alle Downloads durch sind:** Control Center → New → **„Max Bulk Export (1m)“** (NICHT „TEST“). Läuft still, am Ende liegt `C:\Users\Administrator\Desktop\NT8_Export\_DONE.txt`. **Fehlerfall:** NT8 hängt → NT8 NICHT beenden, Hauptkanal.

e) Im Hauptkanal **„Export fertig“**. Rohdaten, Parquets, Roll-Check und Datenumstellung macht die Export-Session über Nacht. Danach rechnet die Gold-Tafel (AP371) ihren einen Lauf von selbst.

## 6. Optional, 10 Minuten: echter Alarm-Test (AP386)

Nur wenn noch Lust und alle Konten flat sind:
1. Reiter Strategies: den **RTY-Gap-Host auf FFN2** deaktivieren.
2. Warten. Nach spätestens etwa 10 Minuten muss ein Telegram kommen („Instanz aus“ o.ä.).
3. Host wieder aktivieren, im Hauptkanal **„Alarm kam“** oder **„kein Alarm“** schreiben.

## 7. Schluss

1. Reiter Strategies: alle Hosts und alle 5 RiskGuards aktiv, Telegram-Felder gefüllt.
2. Aufs Handy: Startmeldungen der RiskGuards sind angekommen.
3. **RDP nur trennen (Fenster schließen), NICHT abmelden.** Der Wiederanlauf braucht die angemeldete Sitzung (AP86).

## Samstag 17.10.: Wochenend-Prüfung

`/wochenende` (am besten in der Session „Wochenend-Buch“). Vorher macht Claude Golden Master, Box-Sync und `weekend_check` mit echten Gebühren. Du entscheidest die acht Punkte aus [[Wochenend-Prüfung 17.10.2026]]: RTY-Gap, OPEXMOM, LD01, Asia auf 50k, LIVE_EXTRA, Engine-Fix-Tickets, next-week-2026-40, Hochstufen.

## Sonst nur du (ohne Box)

- **Steuerberater:** Gründung, Kleinunternehmer ja/nein, BOS-Finanzplan (AP238). Der BOS-Plan gibt die Kaufrunde frei, die Kaufvorlage liegt in [[Kaufvorlage Kaufrunde 06.11.2026]].
- **AP252:** die API-Keys von Gemini, Groq und OpenRouter in den jeweiligen Konsolen löschen und neu erzeugen (standen am 22.09. im Chat).

## Quellen

Ticket-Sessions vom 14./15.10. (FN1-Ausfall, NT8-Altlasten, NT8-Export, Inaktivität, Live-Überwachung, Gold-Tafel, Wochenend-Buch), [[Live-Stellung 15.10.2026 (Anleitung)]], Notizen in AP356 und AP381, Box per SSH 16.10. 00:01 (Next-Week-Buch PC = Box, md5 b980dbff).
