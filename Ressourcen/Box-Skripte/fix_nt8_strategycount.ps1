# fix_nt8_strategycount.ps1  (01.10.2026)
#
# Behebt den Watchdog-Fehlalarm "NT8 laeuft und ist verbunden, aber KEINE Strategie ist aktiv".
#
# Ursache: Get-NT8StrategyCount in C:\Users\Administrator\nt8_control.ps1 liest seit dem Fix vom
# 08.09.2026 nur die letzten DREI NT8-Logdateien. NT8 legt aber jeden Tag eine neue Logdatei an,
# die "Enabling NinjaScript strategy"-Zeilen stehen nur im Log vom Aktivierungstag (zuletzt 26.09.).
# Laeuft NT8 laenger als ~2 Tage ohne Neu-Aktivierung, fallen sie aus dem Fenster -> 0 -> Alarm.
#
# Fix: alle Logdateien lesen, die seit dem Start der laufenden NT8-Instanz geschrieben wurden.
# Jede Aktivierung dieser Instanz steht zwingend darin, egal wie lange NT8 schon laeuft.
# Die neue Funktion wird ans ENDE von nt8_control.ps1 gehaengt und ueberschreibt damit die alte
# Definition weiter oben (alter Code bleibt unangetastet, Ruecknahme = Backup zurueckkopieren).
#
# Aufruf auf der Box (PowerShell als Administrator):
#   powershell -NoProfile -ExecutionPolicy Bypass -File fix_nt8_strategycount.ps1          # Probelauf, aendert nichts
#   powershell -NoProfile -ExecutionPolicy Bypass -File fix_nt8_strategycount.ps1 -Apply   # einbauen
#
# -Apply baut nur ein, wenn die neue Zaehlung > 0 ist, legt vorher ein Backup an, schreibt mit BOM
# (PS 5.1 liest UTF-8 ohne BOM als ANSI) und prueft danach in einem frischen PowerShell-Prozess.
# Klappt die Pruefung nicht, wird das Backup automatisch zurueckgespielt.

param([switch]$Apply)

$ErrorActionPreference = "Continue"   # Fehler werfen wir unten explizit
$ctl    = "C:\Users\Administrator\nt8_control.ps1"
$marker = "# --- Get-NT8StrategyCount v2 (01.10.2026) ---"

$newFunc = @'
# --- Get-NT8StrategyCount v2 (01.10.2026) ---
# Ersetzt die Fassung vom 08.09.2026 (letzte DREI Logdateien). NT8 schreibt jeden Tag eine neue
# Logdatei, die Enabling-Zeilen stehen aber nur im Log vom Aktivierungstag. Nach ~3 Tagen Laufzeit
# fielen sie aus dem Fenster -> 0 Strategien -> Fehlalarm "KEINE Strategie aktiv" (ab 29.09.2026).
# Jetzt: alle Logdateien seit dem Start der laufenden NT8-Instanz, letzter Zustand je Instanz-ID.
# Steht am Ende der Datei und ueberschreibt damit die alte Definition weiter oben.
# -Detail liefert die Herleitung (Start, Dateien, aktive Instanzen) statt nur der Zahl.
function Get-NT8StrategyCount {
    param([switch]$Detail)
    $logDir = "C:\Users\Administrator\Documents\NinjaTrader 8\log"
    $procs  = @(Get-Process -Name NinjaTrader -ErrorAction SilentlyContinue)
    $start  = $null
    if ($procs.Count -gt 0) {
        $start = ($procs | Where-Object { $_.StartTime } | Sort-Object StartTime | Select-Object -First 1).StartTime
    }
    # Fallback, falls die Startzeit nicht lesbar ist: 14 Tage zurueck (besser zu viel als zu wenig Log)
    $since = if ($start) { $start.AddMinutes(-1) } else { (Get-Date).AddDays(-14) }
    $files = @(Get-ChildItem (Join-Path $logDir "log.*.txt") -ErrorAction SilentlyContinue |
               Where-Object { $_.LastWriteTime -ge $since } | Sort-Object Name)
    $active = @{}   # Instanz-ID -> $true/$false (letzter bekannter Zustand)
    $names  = @{}   # Instanz-ID -> Klassenname
    $hits   = 0
    if ($procs.Count -gt 0 -and $files.Count -gt 0) {
        $rx = "(Enabling|Disabling) NinjaScript strategy '?([^'/]+)/(\d+)"
        foreach ($f in $files) {
            # Get-Content oeffnet mit FileShare.ReadWrite, geht also auch auf das Log, in das NT8 gerade schreibt
            foreach ($m in (Get-Content -LiteralPath $f.FullName -ErrorAction SilentlyContinue | Select-String -Pattern $rx)) {
                $g = $m.Matches[0].Groups
                $active[$g[3].Value] = ($g[1].Value -eq "Enabling")
                $names[$g[3].Value]  = $g[2].Value
                $hits++
            }
        }
    }
    $ids   = @($active.Keys | Where-Object { $active[$_] } | Sort-Object)
    $count = $ids.Count
    if ($Detail) {
        return [pscustomobject]@{
            Count     = $count
            NT8Start  = $start
            Files     = @($files | ForEach-Object { $_.Name })
            LogHits   = $hits
            Active    = @($ids | ForEach-Object { "{0}/{1}" -f $names[$_], $_ })
            Inactive  = @($active.Keys | Where-Object { -not $active[$_] } | Sort-Object | ForEach-Object { "{0}/{1}" -f $names[$_], $_ })
        }
    }
    return $count
}
'@

if (-not (Test-Path $ctl)) { throw "nt8_control.ps1 nicht gefunden: $ctl" }
$text = [IO.File]::ReadAllText($ctl)

# 1) Alte Zaehlung (so wie der Watchdog sie gerade sieht)
. $ctl
$old = Get-NT8StrategyCount

# 2) Neue Zaehlung, ohne etwas zu schreiben
Invoke-Expression $newFunc
$d = Get-NT8StrategyCount -Detail

Write-Host ""
Write-Host "=== Get-NT8StrategyCount: alt vs. neu ==="
Write-Host ("alt (letzte 3 Logdateien):       {0}" -f $old)
Write-Host ("neu (alle Logs seit NT8-Start):  {0}" -f $d.Count)
Write-Host ("NT8-Start:   {0}" -f $d.NT8Start)
Write-Host ("Logdateien:  {0}  ({1})" -f $d.Files.Count, ($d.Files -join ", "))
Write-Host ("Treffer Enabling/Disabling: {0}" -f $d.LogHits)
Write-Host "Aktiv:"
$d.Active | ForEach-Object { Write-Host ("   + {0}" -f $_) }
if ($d.Inactive.Count -gt 0) {
    Write-Host "Zuletzt deaktiviert:"
    $d.Inactive | ForEach-Object { Write-Host ("   - {0}" -f $_) }
}
Write-Host ""

if (-not $Apply) {
    Write-Host "Probelauf, nichts geaendert. Passt die Liste 'Aktiv' zu dem, was in NT8 laeuft? Dann mit -Apply einbauen."
    exit 0
}

# 3) Einbauen
if ($text.Contains($marker)) { Write-Host "Fix ist schon eingebaut (Marker gefunden), nichts zu tun."; exit 0 }
if ($d.Count -le 0) { throw "Neue Zaehlung ist 0, Fix wird NICHT eingebaut. Ausgabe oben pruefen (Logformat? NT8-Start?)." }

$bak = "{0}.bak-{1}-stratcount-v2" -f $ctl, (Get-Date -Format "yyyyMMdd-HHmm")
Copy-Item $ctl $bak
$utf8Bom = New-Object System.Text.UTF8Encoding($true)
[IO.File]::WriteAllText($ctl, ($text.TrimEnd() + "`r`n`r`n" + ($newFunc -replace "`r?`n", "`r`n") + "`r`n"), $utf8Bom)

# 4) Gegenprobe in einem frischen Prozess, genau wie der Watchdog die Datei laedt
$check = & powershell -NoProfile -ExecutionPolicy Bypass -Command ". '$ctl'; Get-NT8StrategyCount" 2>&1
$checkNum = 0
if (-not ([int]::TryParse(("$($check | Select-Object -Last 1)").Trim(), [ref]$checkNum)) -or $checkNum -ne $d.Count) {
    Copy-Item $bak $ctl -Force
    throw ("Gegenprobe fehlgeschlagen (erwartet {0}, bekommen: {1}). Backup zurueckgespielt." -f $d.Count, ($check -join " | "))
}

Write-Host ("Eingebaut. Gegenprobe im frischen Prozess: {0} Strategien aktiv." -f $checkNum)
Write-Host ("Backup: {0}" -f $bak)
Write-Host "Naechster Watchdog-Lauf (alle 5 Min) sollte 'ok  NT8 handelsbereit, N Strategien aktiv' in maxlab_watchdog_log.txt schreiben:"
Write-Host "   Get-Content C:\Users\Administrator\maxlab_watchdog_log.txt -Tail 3"
