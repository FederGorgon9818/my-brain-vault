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
- Die Sprachausgabe ist die größte Einzelbremse, die Erkennung läuft ohne passende Grafikkarte auf dem Prozessor.

## Nächste Schritte
1. Max testet, ob sich das Tempo brauchbar anfühlt.
2. Stufe 2: Hintergrund-Arbeiter, „wie weit bist du", Fertig-Meldungen, Bestätigung per Taste. Vorher klären, wie sich Pflichtketten und Stop-Hook in Prozessen ohne Bildschirm verhalten.
3. Stufe 3: Status im Hub, bessere Stimme, Zugriff von Laptop oder Handy.

## Offene Punkte
- Abo: die Doku erlaubt `claude -p` mit Max-Login bei normaler Einzelnutzung, eigene Automatisierung ist nicht ausdrücklich genannt. Nur für Max selbst, nichts davon weitergeben oder verkaufen, ohne auf API-Key umzustellen.
- Haiku nennt trotz Anleitung noch Ticket-Nummern.
