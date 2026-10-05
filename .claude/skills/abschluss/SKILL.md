---
name: abschluss
description: Session-Ende-Ritual aus der CLAUDE.md als fester Ablauf - Daily Note ergänzen, Erkenntnisse in Projekt-/Bereichsnotizen, Inbox aufräumen, Buch-Push- und Regressions-Marker prüfen, Commit anbieten. Nutzen, wenn Max /abschluss aufruft oder sagt "mach Schluss", "Session beenden", "schreib alles weg".
---

# Skill: Session-Abschluss

## Schritte

1. **Was hat diese Session geändert?** Aus dem eigenen Verlauf sammeln: geänderte Dateien, Entscheidungen, Zahlen, offene Reste. Nichts erfinden, was nicht passiert ist.
2. **Daily Note** `Daily Notes/YYYY-MM-DD.md` (heute) anlegen oder ergänzen: eigener Abschnitt mit Überschrift (Thema, Modell/Session), darunter kurz: was gemacht, was geschafft, was offen, welche Dateien geschrieben. Wikilinks auf betroffene Notizen. Bestehende Abschnitte anderer Sessions nicht anfassen.
3. **Erkenntnisse ablegen:** neue Regel → [[Schreibstil]] oder CLAUDE.md (nur wenn Max es gesagt hat; ergab die Session eine neue dauerhafte Regel oder Lehre, vorher den Plugin-Skill `claude-md-management:revise-claude-md` nutzen, bevor sie von Hand in die CLAUDE.md geschrieben wird); neue Lehre aus einem Vorfall → [[Strategie-Logbuch]] (dann `logbook-distiller` einschalten); Projekt-Stand → passende Datei in `Projekte/` oder `Bereiche/`; externe Claims → [[Research-Cache]].
4. **Inbox:** `Inbox/Brain Dump.md` prüfen, Reste einsortieren oder anbieten.
5. **Marker-Check** (nur wenn der Engine-Ordner existiert): ist `book_state*.json` neuer als der letzte `--push-next`? Wurde Engine-Kern geändert ohne `engine-regression-tester`? Wurde Discovery-Code geändert ohne Runner-Neustart? Jeden offenen Punkt entweder erledigen oder als Ticket/Daily-Note-Zeile festhalten, nie still lassen.
6. **Git:** `git status` im Vault. Wenn Änderungen da sind, einen Commit mit sprechender Message vorschlagen (Vault ist geräteübergreifend nur per Git synchron). Commit und Push nur, wenn Max zustimmt oder es vorher schon gesagt hat.
7. **Schluss-Zeile:** Modell-/`/clear`-Hinweis und die Daily-Note-Bestätigung (Regel 09.09.2026).

Der Stop-Hook prüft Daily Note und Buch-Push ohnehin; dieser Skill soll dafür sorgen, dass er nichts mehr zu bemängeln hat.
