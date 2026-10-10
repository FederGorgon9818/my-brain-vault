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
- **Watchdog auf der Box:** `C:\Users\Administrator\maxlab_watchdog.ps1`, geplante Aufgabe **"MaxLab Watchdog"** (alle 5 Min, SYSTEM). Prüft: NT8-Prozess (immer), Marktdaten-Frische via `bars_MNQ.csv` (Mo-Fr 15:35-22:00), Disk. Alerts per Telegram (Config `C:\Users\Administrator\maxlab_watchdog.json`, Token = gleicher Bot wie RiskGuard), gleicher Alert max. 1×/h. Log: `maxlab_watchdog_log.txt`. Bewusst **nur Alarm, kein Auto-Restart** (kein unbeaufsichtigter Eingriff). Lokale Kopie des Skripts: `engine\maxlab_watchdog.ps1`.
- **Claude Code auf der Box:** nativ installiert (`C:\Users\Administrator\.local\bin\claude.exe`, v2.1.226, PATH gesetzt). Login einmalig per RDP nötig. Für autonome Health-Checks/Mitdenken direkt auf der Box.

## Aus der CLAUDE.md (05.10.2026): Box-Fernzugriff, Regeln für Claude

Aus dem Abschnitt „Box-Fernzugriff" (Regel Max, 11.08.2026, „nie wieder vergessen") hierher übernommen, damit die CLAUDE.md schlank bleiben kann.

**Claude hat vollen SSH-Zugriff auf die Trading-Box und nutzt ihn immer selbst**, statt zu behaupten, er habe keinen Zugriff oder Max müsse das manuell machen.

- **Zugang:** `ssh Administrator@100.127.89.9` (Tailscale, Key lokal unter `C:\Users\maxlk\.ssh\id_ed25519`, kein Passwort nötig). Box-Hostname `vmd202078`, deutsche Zeitzone.
- **Laptop seit 03.09.2026 zweites, dauerhaftes Arbeitsgerät:** gleicher Weg wie vom PC, Vault per Git-Remote, Engine-/Box-Arbeit per SSH mit demselben Key. Kein eigener Discovery-Fallback und kein Hub/Lab-Server am Laptop, die Box bleibt die gemeinsame Instanz.
- **F5/manuelles Kompilieren ist tot.** Deploy läuft extern über `box_deploy.ps1`: NT8 beenden → Backup → Staging → Pre-Flight-Compile → `dotnet build` → DLL setzen → aufräumen. Details/Fallen: [[Strategie-Logbuch]] #084.
- **Vor jedem Deploy:** NT8-Log des Tages checken, danach `_check_compile.ps1 -SrcDir` in einem Wegwerf-Ordner, bevor NT8 überhaupt gestoppt wird. `box_deploy.ps1` sagt die Deploy-Kandidaten vorab an und warnt bei unbekannten Dateien (neues Bein oder Leiche?). Die Ansage immer lesen.
- **Wiederanlauf braucht aktuell eine angemeldete RDP-Session** (Autologon fehlt noch, **AP86**). Nach jedem Deploy kurz Bescheid geben.
- **Lab-Server ist multi-threaded** (`ThreadingTCPServer`). Port per `MAXLAB_PORT` überschreibbar. Wichtig zum Testen, sonst läuft eine zweite Instanz still auf demselben Port.
- **Geplant:** ein zentraler „Deployer", der Staging, Pre-Flight, Build, Deploy und Restart automatisch macht. Noch nicht gebaut, aber das Zielbild: künftige Deploy-Arbeit soll darauf einzahlen.

Ticket-Tracker (`tasks.json`, `--pull` vor neuen Tickets): siehe [[Ticket-Board (Jira-Stil)]].
