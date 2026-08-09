---
tags:
  - ressource/claude-code
  - ressource/tokens
erstellt: 2026-07-05
---
# 🧭 Modellwahl: Opus vs Sonnet vs Haiku

Ziel: Kontingent schonen, indem man das kleinste Modell nimmt, das gut genug ist. Opus frisst mit Abstand am meisten.

## Faustregel
Klare, definierte Aufgabe → **Sonnet**. Stumpf/mechanisch/viel → **Haiku**. Kniffliges Denken, Architektur, subtile Bugs → **Opus**.

## Wann welches Modell
| Modell | Wofür | Beispiele (Max) |
|---|---|---|
| **Opus 4.8** | Schweres Denken, Architektur, lange autonome Läufe, subtile Bugs, echte Abwägungen | [[paper-edge]]-Analyse, PowerLanguage vs .NET, Strategie-Logik designen, fiese Bugs, komplexe Refactors |
| **Sonnet 5** | Arbeitspferd fürs Coden, nah an Opus, viel günstiger | [[Token Tracker App]] bauen, ORB in Python, normale Features, Standard-Skripte, Code Review klarer Diffs |
| **Haiku 4.5** | Schnell, mechanisch, viel Volumen | Inbox/Brain Dump einsortieren, Daily Notes, Dateien organisieren, kurze Fragen, Zusammenfassungen |

## Von Opus runterstufen
**→ Sonnet:** Token Tracker & ORB bauen, Standard-Python/C# schreiben & refactoren, Code Review überschaubarer Änderungen.
**→ Haiku:** Vault-Pflege (Inbox sortieren, Daily Notes, verlinken, aufräumen), kurze Lookups, Zusammenfassungen.
**→ Opus lassen:** Paper-Edge-Analyse, Architektur-/Strategie-Entscheidungen, fiese Debugging-Sessions.

## Heuristik „reicht kleiner?"
- „Nur Fleißarbeit / eh nur ein Weg" → kein Opus.
- „Muss man wirklich abwägen / ist tricky" → Opus.

## Umschalten
In Claudian pro Session mit `/model` (opus / sonnet / haiku). Vault-Kram und einfaches Coden auf Sonnet/Haiku starten, nur für harte Sachen bewusst auf Opus.

## Grobe Kosten-Relation (API-Preise, als Anhaltspunkt fürs Kontingent)
- Opus 4.8: ~5x Input / 5x Output von Haiku
- Sonnet 5: ~3x von Haiku (aktuell Intro-Preis günstiger)
- Haiku 4.5: Basis
