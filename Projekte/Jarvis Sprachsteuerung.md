---
tags: [projekt, jarvis, sprache]
datum: 2026-11-04
---

# Jarvis Sprachsteuerung

**Ziel (Max, 04.11.2026):** per Taste mit Claude reden und die Antwort hören, während parallel Aufgaben laufen. Bei „was steht an" kommt der Überblick aus dem Ticket-System, sonst redet Jarvis nicht ungefragt darüber.

**Code:** `C:\Claude\projekte\jarvis\`, Start über `start_jarvis.cmd`.

## Entscheidungen
- Selbst gebaut: `/voice` in Claude Code kann nur diktieren, im Doku-Index der Claude-API steht keine Sprach-Schnittstelle (Stand 04.11.2026, Volltext nicht geprüft).
- **F8 schaltet um, kein Halten** (Max): einmal drücken startet, nochmal drücken schickt ab.
- Stimme kostenlos über edge-tts, später austauschbar.
- Jarvis redet und delegiert nur, die Arbeit machen später Hintergrund-Prozesse.
- Riskantes (Deploy, Mail, Buch, Kauf) nie allein per Stimme: Jarvis liest vor, Bestätigung per Taste. Gilt ab Stufe 2, im Durchstich hat Jarvis gar keine Werkzeuge.

## Stand
- **Stufe 1 Durchstich gebaut (04.11.2026):** Selbsttest grün, F8 per simulierter Taste getestet. Das Reden mit Max selbst steht noch aus.
- Gemessen in einer Runde (2,9 s Sprache): Erkennung 2,3 s, danach erster Satz nach 2,1 s und erster Ton nach 4,7 s, also rund 7 s bis zum ersten Ton.

## Tempo-Tuning (04.11.2026)
- Max: normale Runden zu lang, Ziel ist ein Gefühl wie am Telefon. Messung echter Runden: 6,3 bis 7,0 s, einmal 35,2 s (29,5 s Erkennung bei „test, hallo, hallo"). Vermutete Ursache: Whisper rechnet bei Wiederholungen mehrfach neu, im Test 12,3 s statt 2,0 s bei Rauschen.
- Geändert: Modell `base` statt `small`, keine Neuberechnung, Hilfesatz statt Wortliste, Stimme wird gestreamt, Vorlauf-Stille entfernt, sofortiges „Mhm" oder „Okay" nach F8.
- Vergleich mit 28 erzeugten Stimm-Proben: `base` 0,64 s bei Treffer 0,942, `small` alt 2,06 s bei 0,972. Mit Max' Mikro noch nicht geprüft. Zurück geht es mit Umgebungsvariable `JARVIS_WHISPER=small`.
- Dauerhaft offener Claude-Prozess bringt laut Messung keinen klaren Vorteil.
- Fertige Lösungen und Preise: [[Research-Cache]], Abschnitt „Sprach-Assistent". Echtes Telefonat geht nur mit bezahltem Sprachdienst, Entscheidung bei Max.

## Verstehen, Haupt-Session, Sessions (06.11.2026)
- Max: Abfragen klappt, aber er versteht oft falsch, und bei „offene Sessions, nicht die Tickets" kamen trotzdem Tickets.
- **Mikro-Test** (`mic_test.cmd`, 5 Sätze, alle Mikros gleichzeitig): Trust GXT 232 am besten (base 0,779, small 0,895, turbo 0,897 bei rund 8,8 s je Satz). Jabra und Webcam schlechter, Realtek liefert nichts.
- An Max' Aufnahmen mit `small`: Wortliste mit Session und Jarvis 0,919, Hilfesatz 0,835 bis 0,895. Nur 5 Sätze, der Abstand ist dünn. Eingestellt: `small` plus Wortliste. Erwartung rund 4 bis 6 s bis zum ersten Ton, an echten Runden noch nicht gemessen.
- **Eine Haupt-Session „Jarvis"**, ID in `%LOCALAPPDATA%\Jarvis\haupt_session.txt`, übersteht Neustarts. Ursache der vielen Sessions: Test-Läufe und Kopien beim Öffnen alter Jarvis-Sessions im Terminal. 13 alte Dateien nach `%LOCALAPPDATA%\Jarvislte_sessions` verschoben. Tests nutzen eine Wegwerf-Session und löschen sie. Wer die Haupt-Session im Terminal öffnet, während Jarvis läuft, erzeugt wieder eine Kopie.
- **Session-Übersicht:** Jarvis liest laufende Claude-Sessions (`~/.claude/sessions`, Thema, letzte Antwort, wartet oder arbeitet). „Nicht die Tickets" schaltet Tickets ab.

## Nächste Schritte
1. Max testet, ob sich das Tempo brauchbar anfühlt.
2. Stufe 2: Hintergrund-Arbeiter, „wie weit bist du", Fertig-Meldungen, Bestätigung per Taste. Vorher klären, wie sich Pflichtketten und Stop-Hook in Prozessen ohne Bildschirm verhalten.
3. Stufe 3: Status im Hub, bessere Stimme, Zugriff von Laptop oder Handy.

## Offene Punkte
- Abo: die Doku erlaubt `claude -p` mit Max-Login bei normaler Einzelnutzung, eigene Automatisierung ist nicht ausdrücklich genannt. Nur für Max selbst, nichts davon weitergeben oder verkaufen, ohne auf API-Key umzustellen.
- Haiku nennt trotz Anleitung noch Ticket-Nummern.
