---
tags:
  - kontext
  - stand
erstellt: 2026-11-11
---
# 📍 Stand: was gerade gilt

Wird per Import in jede Session geladen (CLAUDE.md). **Bei Widerspruch zu älteren Notizen, Daily Notes oder Memory gilt diese Datei.** Handteil kurz halten, erledigte Punkte rauslöschen statt durchstreichen. Die Konten-Tabelle schreibt der Auto-Check alle 30 min selbst (`engine/konten/stand_export.py`).

## Konten, die leben (automatisch aus der Box)

<!-- AUTO:KONTEN START (konten/stand_export.py, nicht von Hand aendern) -->

| Konto | Firma | ID | Beine | Kontostand | Hoch | Puffer bis Floor | Stand vom |
|---|---|---|---|---|---|---|---|
| E8 | E8 | `E62701907262` | 5 | 49.593 $ | 50.000 $ | 1.593 $ | 2026-11-17 |
| FN1 | FundedNext | `FNFTFAMAXIMILIANKHO29486` | 5 | 49.609 $ | 50.000 $ | 1.109 $ | 2026-11-17 |
| FN2 | FundedNext | `FNFTFAMAXIMILIANKHO22193` | 5 | 49.602 $ | 50.000 $ | 1.102 $ | 2026-11-16 |

Lebend = hat eine aktive `maxdd`-Zeile in der RiskGuard-cfg der Box. Puffer nach Guard-Formel, Firmen-Dashboard kann abweichen.

**Leichen auf der Box** (Host-Datei zeigt auf ein Konto ohne RiskGuard-Zeilen, bricht `account_sync` ab, aufräumen nur mit Max' OK):
- `maxlab_book_host.live_ffn150k.json` → `2D-150K394206247048`
- `maxlab_book_host.live_ffn150k_2.json` → `2D-150K010602681476`
- `maxlab_book_host.live_ffn150k_2_rtygap.json` → `2D-150K010602681476`
- `maxlab_book_host.live_ffn150k_rtygap.json` → `2D-150K394206247048`

<!-- AUTO:KONTEN ENDE -->

Alle drei sind **Funded** (seit 10.11.2026), Start je 50.000 $. FN: Floor 48.500 $, rastet erst bei 51.600 $ auf 50.100 $ ein. Regeln je Konto: [[Firm-Regeln je Konto]].

## Tot oder ersetzt (nicht mehr als aktiv behandeln)

- **FFN STEADY 150K** `2D-150K394206247048` und Nr. 2 `2D-150K010602681476`: **geschlossen am 26.10.2026.** FFN-Freigaben, -Regeln und -Deckel sind damit Geschichte.
- **FundedNext-Challenges** `FNFTCHMAXIMILIANKHO71491` / `…89622` und **E8-Eval** `E61803453048`: bestanden, am 10.11.2026 durch die Funded-Konten oben ersetzt.

## Was Claude kann und was nicht

- **Kann:** per SSH auf die Box lesen und Dateien schreiben (RiskGuard-cfg, Host-JSONs, Skripte), Dienste prüfen, Deploys vorbereiten.
- **Kann nicht:** NT8-Strategie-Properties ändern, Instanzen anlegen, entfernen, aktivieren. **Das geht nur per RDP durch Max.** Deshalb gehört jeder Wert in die cfg, die der Guard beim Start liest; nach einer cfg-Änderung muss Max die Instanz per RDP einmal aus- und einschalten.
- **Kann nicht:** NT8 nach Deploy wieder hochfahren ohne angemeldete RDP-Session (Autologon fehlt, AP86).

## Offen

- RiskGuard: Default `EvalProfitTarget` 0 und cfg `target=0` sind im Quellcode umgebaut (11.11.), Deploy erst am Wochenende, wenn alle Konten flat sind, per RDP. Alte gespeicherte Instanzen danach einmal entfernen und neu hinzufügen.
- NT8: die **Market Data Subscriber Certification** lädt seit 11.11. nicht (NinjaTrader-Server liefert das Dokument nicht, „template is not available for preview“). Seit 16.11. drückt `nt8_autologin.ps1` dort automatisch Cancel (nur bei genau diesem Ladefehler), danach verbindet NT8 normal. Selbst unterschreiben ist offen: AP488.
- E8: Lücke zwischen den Handtrades (16.11. und 20.11.) im E8-Dashboard gegenprüfen. Der Guard kennt seit 22.11. den 20.11. als Handelstag (nachgetragen), nächste echte Frist 27.11.
- NT8-Instanzen brauchen **Trading hours `US Equities RTH`** (Hosts zusätzlich Days to load 45) direkt an der Instanz. Ohne Template stürzt NT8 beim Aktivieren ab (`GetTradingHours`, 17. und 22.11.). Ablauf: [[Wiedereinschalten 22.11.2026 (Anleitung)]].
- FN: HFT-Grenze unbekannt (PB3 ohne Stop-Verzögerung), Split im Dashboard nachsehen, FundedNext-Connector neu verbinden (AUTH_EXPIRED).
- FFN-Host-Leichen auf der Box (Liste oben) löschen, dann `account_sync --pull`. Nur mit Max' OK.

## Korrekturen von Max (schreibt der Hook automatisch)

Neue Zeilen kommen vom Korrektur-Reflex (`.claude/hooks/korrektur_reflex.py`), höchstens 12, die älteste fliegt raus. Claude sortiert sie danach in die Abschnitte oben ein und löscht die Zeile hier.

<!-- KORREKTUREN START -->
<!-- KORREKTUREN ENDE -->
