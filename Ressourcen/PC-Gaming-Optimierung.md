---
tags: [pc, gaming, setup]
datum: 2026-10-09
---

# PC-Gaming-Optimierung (Stand 09.10.2026)

Ziel: mehr FPS und stabilere Frametimes, **ohne Grafikeinstellungen zu senken**.

## Hardware-Stand

| Teil | Was drin ist | Bedeutung |
|---|---|---|
| GPU | Radeon RX 570, 8 GB | Flaschenhals bei 1440p @ 144 Hz |
| CPU | Ryzen 5 3500X, 6 Kerne / 6 Threads | jedes Hintergrundprogramm kostet direkt FPS |
| RAM | 2× 8 GB Crucial Ballistix 2666 CL16 (BL8G26C16U4B) | langsam für Ryzen 3000, größter Hebel per BIOS |
| Board | Gigabyte B450 AORUS M, BIOS F67 (aktuell) | |
| Monitor | 2560×1440 @ 144 Hz | |

Realistisch per Software: ca. 5 bis 15 % mehr FPS und bessere 1%-Lows. Mehr geht nur mit neuer GPU.

## ✅ Schon erledigt per Skript (09.10.2026)

- Game Mode an
- Xbox Game DVR / Hintergrundaufnahme aus
- „Optimierungen für Spiele im Fenstermodus" an (Flip-Model, weniger Latenz in Borderless), VRR bleibt an
- Transparenzeffekte aus
- Autostart aus: **OneDrive, Medal, Overwolf** (bleiben installiert, nur nicht mehr beim Hochfahren)
- Energieplan: **AMD Ryzen High Performance**

Bewusst drin gelassen: Discord, Steam, FACEIT, LGHUB (Mauseinstellungen), Tailscale, Wispr Flow, claude-code-router, Riot Vanguard.

**Rückgängig machen:** `C:\Users\maxlk\PC-Tuning-Backup\undo_gaming_tuning.ps1` per Rechtsklick „Mit PowerShell ausführen". Backups der Registry liegen im selben Ordner.

**Wirkt komplett erst nach einem Neustart** (Autostart).

**Nachtrag 09.10. nach dem BIOS-Umbau:** RAM läuft auf **3000 MHz**, 0 Hardware-Fehler (WHEA) nach dem Boot. OneDrive kam trotzdem über eine eigene geplante Aufgabe hoch, die ist jetzt auch aus (Backup `OneDrive_Startup_Task.xml`, Undo-Skript ergänzt). Overwolf startet sich selbst, Autostart dort in den Overwolf-Einstellungen abschalten. Stabilitätstest (Punkt 1, Schritt 8) steht noch aus.

## 🛠️ Was du selbst machen musst, sortiert nach Wirkung

### 1. RAM übertakten im BIOS (größter Hebel, ~5 bis 15 % in CPU-lastigen Spielen wie R6, CS, Valorant)

Bei Ryzen 3000 läuft der interne Bus (Infinity Fabric) mit dem RAM-Takt mit. 2666 → 3200 bringt spürbar bessere 1%-Lows.

1. PC neu starten, **Entf** drücken → BIOS
2. Oben auf **Tweaker**
3. **Extreme Memory Profile (X.M.P.)**: auf Profile 1 lassen bzw. setzen
4. **System Memory Multiplier**: auf **30.00** (= 3000 MHz)
5. **DRAM Voltage**: **1.350V**
6. Timings (Advanced Memory Settings → Channel A/B Timing): **16-18-18-38** lassen (kommen vom XMP)
7. **F10** → speichern → neu starten
8. Stabilität testen: **OCCT** (Test „Memory", 30 Min) oder **TestMem5** mit Profil „anta777 extreme". Kein Fehler = stabil
9. Läuft stabil? Dasselbe mit Multiplier **32.00** (3200 MHz) probieren, wieder testen
10. **Fehlerfall:** PC bootet nicht → er setzt nach 3 Fehlstarts selbst zurück, oder Board-Jumper CLR_CMOS. Dann wieder auf 3000 zurück

Kontrolle in Windows: Task-Manager → Leistung → Arbeitsspeicher → „Geschwindigkeit".

### 2. Radeon-Treiber (AMD Software: Adrenalin), kostet keine Bildqualität

Rechtsklick Desktop → AMD Software → **Gaming → Grafik** (global):

| Einstellung | Wert | Warum |
|---|---|---|
| Radeon Anti-Lag | **An** | weniger Input-Lag |
| Radeon Chill | **Aus** | würde FPS absichtlich drosseln |
| Radeon Boost | **Aus** | senkt die Auflösung in Bewegung |
| Enhanced Sync | **Aus** | macht mit FreeSync eher Ruckler |
| Wait for Vertical Refresh | **Aus, außer App gibt es an** | |

**Anzeige** → **AMD FreeSync: An**.
**Aufnehmen & Streamen**: Instant Replay und In-Game-Overlay aus, falls an (sonst nimmt der Treiber im Hintergrund mit).

### 3. Overlays in den Apps aus

- **Discord:** Einstellungen → Spiel-Overlay → aus
- **Steam:** kann an bleiben, kostet wenig. Wer ganz sauber will: Steam → Einstellungen → Im Spiel → Overlay aus
- **Medal / Overwolf:** starten nicht mehr automatisch. Wenn du Clips willst, Medal von Hand starten

### 4. Vor dem Zocken schließen

- **Claude Desktop** (zusammen fast 2 GB RAM), Edge, alles was du nicht brauchst
- Beim Check liefen mit R6 nur noch 2,1 GB RAM frei, Windows hat schon komprimiert. Das gibt Ruckler

### 5. Optional: Virtualisierung (VBS) aus, kleiner Gewinn

VBS läuft, die Speicherintegrität (der teure Teil) ist aber schon aus. Der Rest kostet nur noch wenig.
**Nur machen, wenn du kein WSL, Docker, Windows Sandbox oder Hyper-V nutzt**, sonst geht das kaputt:
Eingabeaufforderung **als Administrator** → `bcdedit /set hypervisorlaunchtype off` → Neustart.
Rückgängig: `bcdedit /set hypervisorlaunchtype auto`.

### 6. Optional: PBO im BIOS

BIOS → Settings → AMD Overclocking → **Precision Boost Overdrive: Enabled**. Bringt ein paar Prozent Boost, aber mit dem Boxed-Kühler (Wraith Stealth) wird die CPU deutlich wärmer. Nur mit besserem Kühler, Temperatur mit HWiNFO prüfen (unter 85 °C bleiben).

## 💸 Der echte Hebel: GPU

Die RX 570 ist bei 1440p die Grenze. Eine RX 6600 / RX 7600 Klasse wäre grob doppelte Leistung. Kaufentscheidung immer gegen die BOS-Reserve rechnen (ab 04.07.2027 kein Gehalt mehr, siehe [[Gründung Zeitplan]]).
