---
tags:
  - ressourcen/infra
  - github
  - claude/prozess
erstellt: 2026-10-05
status: aktiv (Umzug Max, 28.09.2026)
---
# 🐙 GitHub: Account, Repos, Schlüssel

Herkunft: aus der CLAUDE.md ausgelagert am 05.10.2026 ([[CLAUDE.md Verschlankung]])

⬅️ [[VPS-Einrichtung Schritt für Schritt]] · [[Hooks-Referenz]]

## Account

**GitHub-Account seit 28.09.2026: `FederGorgon9818`.** Der alte Account `mkmeboss` ist nicht mehr zugänglich. Grund bei Max offen: vergessen oder gehackt? Bei gehackt Secrets neu ziehen. Dort liegen noch Kopien aller drei Repos mit Stand 28.09., erst löschen, wenn der Zugang zurück ist.

## Repos

| Repo | Lokal (PC) | Branch | Inhalt |
|---|---|---|---|
| `FederGorgon9818/my-brain-vault` | dieser Vault | `master` (Standard) | Obsidian-Vault |
| `FederGorgon9818/hub` | `C:\Users\maxlk\Projects\hub` | `master` | Hub-App |
| `FederGorgon9818/trading-data` | `C:\Users\maxlk\Projects\trading-data` | `main` | Engine, Discovery, Lab, verschlüsselte Notfall-Secrets |

## Remotes und Schlüssel

- **Remotes am PC:** `origin` = neuer Account, `alt` = `mkmeboss` (über den SSH-Host `github-alt`).
- **Schlüssel:** GitHub erlaubt jeden SSH-Key nur auf einem Account. PC nutzt `~/.ssh/id_ed25519_github_neu` für `github.com`, der alte `id_ed25519_github` hängt nur noch an `github-alt` (Backup der alten Config: `~/.ssh/config.bak-20260928`). Der Box-Zugang `id_ed25519` hat mit GitHub nichts zu tun.

## Box (umgestellt 28.09.)

- Eigener Vault-Klon unter `C:\Users\Administrator\Projects\my-brain-vault`, zieht **und pusht** selbst.
- Deploy-Key `~/.ssh/id_ed25519_vault_neu` mit Schreibrecht im Repo `my-brain-vault`, `origin` = `FederGorgon9818`, `alt` = `mkmeboss` über `github-alt`.
- **Falle beim Testen per SSH von außen:** `ssh -T git@github.com` ohne Eingabe-Umleitung hängt in der nicht-interaktiven Sitzung. Immer `-o ConnectTimeout=10` und `< NUL` mitgeben.
- Mehrzeilige Here-Strings kommen über `powershell -Command -` nicht an. Skripte per `scp` kopieren und mit `-File` starten.

## Laptop

Trackt ebenfalls `origin/master`. **Umstellung offen:** eigener neuer Schlüssel am Laptop, im neuen Account eintragen, Remote auf `FederGorgon9818` umstellen.

## Cloud-Sessions

Sehen nur, was gepusht ist: vorher pushen, dann Repo `my-brain-vault` mit Branch `master` wählen. Die Claude-GitHub-App braucht Zugriff auf den neuen Account.

## trading-data ist ein Backup-Repo

Kein laufend gepflegtes Git, nur so aktuell wie der letzte Push.

- Rohmarktdaten (NT8-Exporte, Parquet-Caches und deren Backups) sind per `.gitignore` ausgenommen, weil sie aus NT8 neu erzeugbar sind.
- `registry.json` und `registry_box.json` (je ~90 MB) sind seit 03.10.2026 nicht mehr im Git (AP309, GitHub lehnt ab 100 MB ab). Stattdessen je eine gzip-Kopie (~5 MB) in `engine/discovery/registry_backup/`, geschrieben von `discovery/registry_backup.py`. Das ruft ein lokaler Pre-Commit-Hook in trading-data bei jedem Commit auf (nur bei geänderter md5).
- **Wiederherstellen:** `gzip -dc registry_backup/registry.json.gz > registry.json`
