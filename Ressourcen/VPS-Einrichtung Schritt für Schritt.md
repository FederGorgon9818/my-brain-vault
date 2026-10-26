---
tags:
  - ressource/anleitung
  - trading/live
erstellt: 2026-07-21
---
# 🖥️ VPS-Einrichtung: Klick-für-Klick

⬅️ [[Live-Setup (Algo auf Prop)]]

> [!tip] Ziel
> Contabo Windows-VPS (~€13-15/Mon.) mieten, absichern, NinjaTrader drauf. Danach läuft das Trading unabhängig vom eigenen PC. Dauer gesamt: ~1-2h + Wartezeit auf die Zugangs-Mail.

## Teil 1: Kaufen (contabo.com)
1. `contabo.com/de/vps/` → **Cloud VPS 6** (6 vCPU / 12 GB / €7,50) → Auswählen
2. Konfigurator: Laufzeit **1 Monat** · Region **US-Central (St. Louis)** · NVMe falls wählbar · Image **Windows Server 2022** (+~€5-6 = das "Windows-Addon") · sonst NICHTS anhaken
3. Warenkorb → Konto anlegen → zahlen → auf Mail **"Your login data"** warten (IP + Administrator-Passwort)

## Teil 2: Verbinden
4. Windows-Taste → `mstsc` → Enter → IP aus Mail → Verbinden → `Administrator` + Passwort → Zertifikat mit Ja bestätigen

## Teil 3: Passwort ändern
5. Im Server-Fenster **Strg+Alt+Ende** → "Kennwort ändern" → langes eigenes PW (Passwort-Manager!)

## Teil 4: Updates
6. Einstellungen → Windows Update → alles installieren (bei Neustart: warten, neu verbinden)
7. Windows Update → Erweiterte Optionen → **Nutzungszeit 14:00-23:00** (kein Auto-Reboot in der US-Session)

## Teil 5: Tailscale (RDP absichern)
8. Eigener PC: `tailscale.com` → mit Google anmelden → Client installieren
9. Server: `tailscale.com/download` → Client installieren → **gleiches Konto**
9b. **PFLICHT: Tailscale-Icon (Tray) → Settings → "Run unattended" anhaken!** Sonst verbindet Tailscale nur, solange ein Benutzer angemeldet ist → nach Reboot/Abmeldung ist der Server im Tailnet offline und man ist ausgesperrt (Rettung: Contabo-Panel → VNC-Konsole). Danach Reboot-Test: Server neu starten und prüfen, dass er OHNE Anmeldung in Tailscale "Connected" wird.
10. Tailscale-IP des Servers notieren (100.x.y.z)
11. **Test:** RDP neu verbinden über die 100er-IP → muss klappen
12. NUR DANN, auf dem Server in Admin-PowerShell:
    `Set-NetFirewallRule -DisplayGroup "Remote Desktop" -RemoteAddress 100.64.0.0/10`
    (Notausgang: Contabo-Panel → VNC-Konsole)

## Teil 6: NinjaTrader 8
13. Auf dem Server: `ninjatrader.com` → Konto anlegen → NT8 Desktop installieren + einloggen
14. Win+R → `shell:startup` → NT-Verknüpfung reinkopieren (Autostart)
15. Prop-Konto-Verbindung (Tradovate-Credentials) → **erst nach Eval-Kauf**

## Teil 7: Reboot-Test
16. Server neu starten → 3 Min → über Tailscale-IP verbinden → NT8 muss von allein offen sein ✅

## Teil 8: Handy (Aufsicht)
17. App Store: **"Windows App"** (Microsoft) + **"Tailscale"** → anmelden
18. Windows App → + → PC → 100er-IP → Administrator → Aufsicht aus der Hosentasche

> [!warning] Merken
> - RDP nie öffentlich lassen (Schritt 12 ist Pflicht, sonst kloppen Bots aufs Login)
> - Windows-Update-Neustarts NIE in die Session fallen lassen (Schritt 7)
> - Auto-Flat bei Disconnect wird zusammen mit den NinjaScript-Strategien konfiguriert

## Teil 9: Fernsteuerung & Watchdog (eingerichtet 09.08.2026)

Die Box (`vmd202078`, Tailscale `100.127.89.9`, Zeitzone = deutsche Zeit) ist voll fernsteuerbar:

- **SSH von Max' PC:** OpenSSH auf der Box, Key `C:\Users\maxlk\.ssh\id_ed25519`. Claude kann aus jeder Session per `ssh Administrator@100.127.89.9` deployen, kompilieren, Logs lesen. Genutzt auch von `sync_live.ps1` (Task "MaxLab Live Sync", alle 2 Min) und `vps_health.ps1`.
- **Watchdog auf der Box (Stand 14.10.2026, AP145/AP212):** `C:\Users\Administrator\maxlab_watchdog.ps1`, geplante Aufgabe **"MaxLab Watchdog"** (alle 5 Min, SYSTEM), Logik in `maxlab_heartbeat.ps1` (Gegenproben: `powershell -File C:\Users\Administrator\test_maxlab_heartbeat.ps1`, muss „ALLE GEGENPROBEN BESTANDEN“ melden). Alerts per Telegram (Config `maxlab_watchdog.json`, Bot maxbot), gleicher Alert max. 1×/h, Log `maxlab_watchdog_log.txt`. Prüft:
  - NT8-Prozess und Handelsbereitschaft (offene Sockets, Connection-Zeile), „keine Strategie aktiv“.
  - **Soll-Ist je Konto:** Kontoliste = Zeilen `<Konto>.maxdd` in `maxlab_riskguard.cfg`. Konto ohne `maxlab_position_snapshot_<Konto>.csv` → eigener Alarm, zu jeder Uhrzeit. Beendetes Konto: Block in der cfg auskommentieren.
  - **Instanzen je Konto:** laut NT8-Log und NT8-Datenbank müssen je Konto ein MaxBookHost (FFN: zwei, MNQ-Buch und RTY-Gap) und ein MaxRiskGuard aktiv sein, sonst „KONTO X: … deaktiviert seit HH:MM ET“ (zu jeder Uhrzeit, 10 Min Karenz nach einem NT8-Start). Anlass: FN1 am 13.10. um 15:58 ET still deaktiviert.
  - **Gegenrichtung:** aktive Host-/Guard-Instanz an einem echten Konto ohne cfg-Block → Alarm (Guard liefe ohne Kontowerte).
  - **Auffällige Log-Zeilen** (seit 15.10., Wunsch AP381): Host-Log „ANOMALIE: Position hat das Vorzeichen gedreht“, „Execution zu veralteter Order“, „EXIT HAENGT“ und RiskGuard-Log „ORPHAN-FLAT“/„ORPHAN-CHECK“ → einmal Telegram je Vorfall; „EXIT-SPERRE“ und harmlose ORPHAN-CHECK-Zeilen nur ins Watchdog-Log. Merkzettel `maxlab_watchdog_loglines.json`.
  - Bars je Konto in RTH (09:30 bis 16:00 ET, Feiertage aus `maxlab_cme_holidays.txt`; fehlt das laufende Jahr dort, gibt es einen eigenen Alarm, Wiedervorlage jedes Jahr am 01.12.), Chart-Template, Kontrakt-Roll, Disk.
  - **Auto-Restart:** bei totem/halbtotem NT8 (15 Min) und als enger Zweig bei Feed-Stillstand (alle Konten 25 Min still in RTH, alle flat laut Snapshot UND Fill-Datei, Telegram-Vorwarnung, 10 Min später Neustart, max. 3 in 120 Min). **Beides hängt an `nt8_autorestart_pause.flag`** (liegt seit 06.09.): solange es liegt, nur Alarm, weil NT8 nach jedem Neustart im Login-Fenster hängt („Remember me“ gibt es nicht, Weg: AP134). Erinnerung jeden Sonntag ab 18 Uhr. Nach jedem NT8-Neustart sind alle Hosts und RiskGuards aus und müssen per RDP aktiviert werden.
  - **Wartungs-Flag** `maxlab_watchdog_firefight.flag`: gewollte Pause (Deploy), macht Herzschlag-, Konto-, Instanz- und Strategie-Alarme stumm. Ab 12 Std Liegezeit alle 6 Std Erinnerung. Nach der Wartung löschen.
  - **Probealarm:** `powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\Administrator\maxlab_watchdog.ps1 -Probe` schickt eine echte Soll-Ist-Meldung für ein erfundenes Konto.
  - Überblick je Konto per SSH: `vps_health.ps1`. Am PC zusätzlich `auto_check.py` (Lab-Glocke): Live-Sync steht, Box-Watchdog läuft nicht mehr, Bars je Konto (mit Feiertagen), Fill-Logger eines Kontos bleibt hinter dem Host zurück, RiskGuard-Ereignisse je Konto. Nur Lab, kein Telegram, und nur wenn der PC an ist. Lokale Kopien aller Box-Skripte: `engine\maxlab_*.ps1`, `engine\vps_health.ps1`.
- **Claude Code auf der Box:** nativ installiert (`C:\Users\Administrator\.local\bin\claude.exe`, v2.1.226, PATH gesetzt). Login einmalig per RDP nötig. Für autonome Health-Checks/Mitdenken direkt auf der Box.

## Teil 10: Automatischer NT8-Login (AP134, Stand 18.10.2026)

**Stand: gebaut, noch NICHT eingespielt und NICHT getestet.** Bis der Test unten grün ist, gilt weiter: Wiederanlauf braucht Max per RDP, `nt8_autorestart_pause.flag` bleibt liegen.

**Das Problem genau:** Windows meldet sich nach dem Boot seit 06.09. selbst an (Sysinternals Autologon, LSA-Secret), NT8 startet über `NinjaTrader.lnk` im Autostart von Administrator bzw. den Task „MaxLab NT8“. Dann hängt es im Login-Fenster. Beleg im NT8-Log: jeder Start ohne Max am Rechner bleibt bei genau einer Zeile („Session Break“), z.B. 01.10. 16:11 und 08.10. 19:43/19:47 ET. Mit Max dauert es vom Start bis „Connecting“ zwischen 20 s und 31 Min, je nachdem, wann er tippt. „Remember me“ hält das Passwort nicht (Max 14.10. und 18.10.), Login-Pflicht ist seit NT 8.1.1.0 Design, SFT-5780 ohne Termin, kein Startparameter und kein Lizenz-Weg am Login vorbei ([[Research-Cache]], Abschnitte 06.09. und 18.10.).

**Geprüfte Wege:**

| Weg | Urteil |
|---|---|
| „Remember me“ / Stay logged in | geht nicht, siehe oben |
| Startparameter, Offline-Modus, Lifetime-Lizenz | gibt es nicht |
| Windows-Autologon | steht schon seit 06.09., löst nur die Windows-Anmeldung |
| tscon nach Disconnect | löst nur ein Desktop-Problem, das Passwort fehlt trotzdem (AP86, 06.09. gemessen) |
| Fremd-Tools (Ilasorf, NJLogon, DeepSignalTech) | Download fremden Codes, teils Passwort im Klartext oder per Zwischenablage und Tastatur (scheitert in getrennter RDP-Sitzung) |
| **eigener UIA-Wächter** | **gewählt:** kein Download, Passwort per DPAPI, füllt per UI Automation statt Tastatur |

**Der Weg:** `C:\Users\Administrator\nt8_autologin.ps1`, gestartet vom Task **„MaxLab NT8 Login“** (bei Anmeldung von Administrator, Interactive, RunLevel Highest, kein Zeitlimit, nie doppelt). Er schaut alle 5 s, ob ein Fenster von `NinjaTrader.exe` ein Passwortfeld hat, trägt das Passwort per `ValuePattern.SetValue` ein und löst „Log In“ per `InvokePattern` aus. Deckt alle Startwege ab: Reboot, Watchdog-Neustart, Deploy, Handstart.
- **Passwort:** nur in `nt8_login.secret` (DPAPI, an Administrator und diese Box gebunden, ACL nur Administrator + SYSTEM). Max legt es selbst an mit `nt8_store_credential.ps1` (Get-Credential, Claude sieht es nie). Nie im Log, nie im Bericht, nie auf der Kommandozeile. Ehrlich: wer Administrator auf der Box ist und eine echte Anmeldung hat, kommt an das Passwort.
- **Genau ein Versuch je NT8-Start.** NT kann Rechenzentrums-IPs mit CAPTCHA belegen, jeder Fehlversuch setzt den Sperr-Timer neu. Kommt der Login nicht durch, meldet der Watchdog weiter „hängt im Login-Fenster“.
- **Notbremse:** `C:\Users\Administrator\nt8_autologin_off.flag` anlegen, der Wächter macht dann nichts mehr. Rückbau: `Unregister-ScheduledTask -TaskName "MaxLab NT8 Login" -Confirm:$false`.
- **Spuren:** `nt8_autologin_log.txt` (Ablauf), `nt8_uia_report.txt` (UIA-Baum des Login-Fensters beim ersten Treffer, ohne Werte), `nt8_autologin_heartbeat.txt` (lebt der Wächter, jede Minute).
- **Firmen-Regeln:** Login-Automatik ändert nichts an „nur ein Gerät gleichzeitig“ (FFN/Rithmic). Den NT-Account selbst darf man laut Forum auf zwei Rechnern nutzen, aber eine zweite Rithmic-Verbindung vom PC kann die der Box kappen. Am PC also keine Rithmic-Verbindung zu FFN-Konten öffnen.

**Offene Lücke, nur auf der Box klärbar:** ob das Login-Fenster ein normales WPF-Passwortfeld hat, das `SetValue` annimmt, und ob UI Automation auch in einer getrennten RDP-Sitzung füllt. Fällt Letzteres durch: vor dem Trennen die Sitzung per `tscon` auf die Konsole legen (Max selbst, Claude ist dafür gesperrt, AP136).

**Was danach noch fehlt:** die Strategien kommen nach jedem NT8-Neustart deaktiviert zurück (NT-Design, kein Enable per AddOn). Erst wenn auch das automatisch geht (AP134 Teil 2, UIA im Strategies-Tab, nur mit WaitUntilFlat und nach Test-NT8Ready), darf das Pause-Flag weg.

## Aus der CLAUDE.md (05.10.2026): Box-Fernzugriff, Regeln für Claude

Aus dem Abschnitt „Box-Fernzugriff" (Regel Max, 11.08.2026, „nie wieder vergessen") hierher übernommen, damit die CLAUDE.md schlank bleiben kann.

**Claude hat vollen SSH-Zugriff auf die Trading-Box und nutzt ihn immer selbst**, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.

- **Zugang:** `ssh Administrator@100.127.89.9` (Tailscale, Key lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, deutsche Zeitzone.
- **Laptop seit 03.09.2026 zweites, dauerhaftes Arbeitsgerät:** gleicher Weg wie vom PC, Vault per Git-Remote, Engine-/Box-Arbeit per SSH mit demselben Key. Kein eigener Discovery-Fallback und kein Hub/Lab-Server am Laptop, die Box bleibt die gemeinsame Instanz.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1`: NT8 beenden → Backup → Staging → Pre-Flight-Compile → `dotnet build` → DLL setzen → aufräumen. Details/Fallen: [[Strategie-Logbuch]] #084.
- **Vor jedem Deploy:** NT8-Log des Tages checken, danach `_check_compile.ps1 -SrcDir` in einem Wegwerf-Ordner, bevor NT8 überhaupt gestoppt wird. `box_deploy.ps1` sagt die Deploy-Kandidaten vorab an und warnt bei unbekannten Dateien (neues Bein oder Leiche?). Die Ansage immer lesen.
- **Wiederanlauf braucht Max per RDP** (Stand 14.10.2026): Autologon der Box steht seit 06.09., aber NT8 fragt bei jedem Start das Passwort ab („Remember me“ gibt es nicht, Max 14.10.), und die Strategien kommen nach jedem NT8-Neustart deaktiviert zurück. Automatischer Weg dafür ist **AP134** (UI-Automation: Login + Strategien aktivieren). Nach jedem Deploy kurz Bescheid geben.
- **Lab-Server ist multi-threaded** (`ThreadingTCPServer`). Port per `MAXLAB_PORT` überschreibbar. Wichtig zum Testen, sonst läuft eine zweite Instanz still auf demselben Port.
- **Geplant:** ein zentraler „Deployer", der Staging, Pre-Flight, Build, Deploy und Restart automatisch macht. Noch nicht gebaut, aber das Zielbild: künftige Deploy-Arbeit soll darauf einzahlen.

Ticket-Tracker (`tasks.json`, `--pull` vor neuen Tickets): siehe [[Ticket-Board (Jira-Stil)]].
