---
name: token-usage
description: Zeigt einen kompakten Token-Verbrauchsreport direkt im Chat - aktuelle Anfrage, laufender 5h-Block, heute, diese Woche, jeweils mit Budget-Auslastung in %. Liest die lokalen Claude-Code-Logs (~/.claude/projects), gleiche Datenquelle wie die Token Tracker App. Nutzen, wenn Max nach Token-Verbrauch, Kontingent, Rate-Limit-Stand oder "wie viel hab ich noch" fragt, oder /token-usage aufruft.
---

# Skill: Token-Usage-Report im Chat

Ziel: Max auf Zuruf (oder per `/token-usage`) einen ehrlichen, log-basierten
Token-Verbrauchsreport direkt in den Chat liefern - keine geschätzten/erfundenen
Zahlen (siehe [[Agent-Architektur Token-Optimierung]] Punkt L/R: erfundene
Messwerte sind explizit unerwünscht). Alle Zahlen kommen aus den echten
Claude-Code-Session-Logs, gleiche Logik wie die Token Tracker App
([[Token Tracker App]]).

## Schritt 1: Report ausführen

```
python "C:\Users\maxlk\Projects\token-tracker\chat_report.py"
```

Bei Bedarf `--json` anhängen für Rohdaten (z.B. zur Weiterverarbeitung).

## Schritt 2: Ergebnis im Chat präsentieren

Zahlen kompakt übernehmen (keine Textwüste, siehe [[Schreibstil]]), immer einordnen:

- **Diese Anfrage bisher** = alles seit Max' letzter echter Texteingabe in dieser
  Session. Erfasst NICHT den gerade laufenden Report-Call selbst (der steht erst
  danach im Log) - kurz erwähnen, keine Krise draus machen.
- **Aktueller 5h-Block** = die wichtigste Zahl für "was hab ich JETZT noch"
  (rollierendes Fenster, ccusage-Stil, gleiche Definition wie im Dashboard).
- **Heute / Woche** = grobe Orientierung. Anthropic gibt für Pro/Max **kein
  hartes Tages-Limit** raus (nur 5h-Blocks + Wochenlimits) - nicht als offizielle
  Zahl verkaufen, sondern als Beobachtung labeln.
- Budgets (`block_token_budget`, `weekly_token_budget`) in `config.json` sind
  **Schätzwerte**, noch nicht an einem echten Rate-Limit-Treffer kalibriert.
  Falls Max mal tatsächlich gegen ein Limit läuft: Zeitpunkt + bis dahin
  verbrauchten Wert aus dem Log notieren und in `config.json` nachtragen
  (siehe [[Token Tracker App]], Abschnitt „Kalibrierung").

## Schritt 3: Bei Fehlern

- `python` nicht gefunden → `py` probieren.
- Keine Session-Datei gefunden → `$env:CLAUDE_CODE_SESSION_ID` in PowerShell
  prüfen. Sonst ehrlich sagen „diese Anfrage nicht messbar" - der Rest des
  Reports (heute/Woche/Block) bleibt trotzdem gültig, da er alle Logs liest.
- Nie Zahlen erfinden oder schätzen, wenn das Skript fehlschlägt - dann lieber
  nur sagen, was nicht ging.

## Verwandt

- Volles Dashboard mit Charts (Browser): `python "C:\Users\maxlk\Projects\token-tracker\server.py"`
  → http://localhost:8712, oder Doppelklick auf `TokenTracker.exe`.
- Native Claude-Code-Wege, Verbrauch zu sehen: `/cost`, `/context`, Statusline
  (`statusLine` in settings.json), rohe Logs unter `~/.claude/projects/**/*.jsonl`,
  Community-Tool `ccusage`. Anthropic Console + Admin-API zeigen nur
  API-Pay-as-you-go-Verbrauch, **nicht** das Pro/Max-Abo von Max.
