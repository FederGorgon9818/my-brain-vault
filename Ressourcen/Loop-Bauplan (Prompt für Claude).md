---
tags:
  - ressource
  - trading/infrastruktur
erstellt: 2026-08-11
---
# 🔁 Loop-Bauplan (Prompt für Claude)

⬅️ [[Day Trading]] · [[Eval-Passing]] · Box-Regeln: [[VPS-Einrichtung Schritt für Schritt]]

> [!info] Wie benutzen
> 1. **Frische Session** starten (`/clear`), Modell **sonnet** reicht (Loops sind Routine, kein Frontier).
> 2. Den kompletten Prompt unten reinkopieren.
> 3. Claude baut die Loops, spielt jeden einmal trocken durch und dokumentiert sie hier im Vault.
>
> Stoppen geht jederzeit mit einer normalen Nachricht („stopp den Loop") oder per Escape. Loops leben nur innerhalb ihrer Session: Terminal zu = Loop weg. Für Dinge, die auch ohne offene Session laufen sollen, ist der Loop das falsche Werkzeug (steht so auch im Prompt).

---

## 📋 Der Prompt (ab hier kopieren)

```
Aufgabe: Richte für mich wiederkehrende Überwachungs-Loops mit /loop ein. Ziel: ich bekomme automatisch mit, wenn auf meiner Trading-Infrastruktur etwas hakt, mit so wenig Tokens wie möglich. Baue nicht blind, sondern in dieser Reihenfolge:

SCHRITT 1: BESTANDSAUFNAHME (nichts doppeln!)
Prüfe zuerst, was schon automatisch läuft, und liste es mir kurz auf:
- auto_check.py läuft alle 30 Min als Windows-Task „MaxLab Auto-Check" (Edge-Ampeln, Sync-Frische, RiskGuard-Kills, Discovery-Kadenz, Aufgaben in der Lab-Glocke). Quelle: C:\Users\maxlk\Projects\trading-data\engine\auto_check.py
- Fill-Sync von der Box läuft alle 2 Min.
- Auf der Box läuft ein Watchdog, der aber bekannte Bugs hat (Ticket AP87 in engine\tasks.json: meldet Datei-Frische ohne Datum und loggt „ok" trotz aktivem Problem).
- Strategy Lab (app_server.py, Port 8756) pollt selbst alle 4s und hat Hot-Reload.
Alles, was dort schon geprüft wird, wird NICHT zusätzlich geloopt.

SCHRITT 2: ENTSCHEIDUNGSREGEL PRO KANDIDAT
Für jede Überwachungsidee entscheide nach dieser Leiter und sag mir die Einordnung:
a) Rein mechanisch prüfbar (Datei-Alter, Prozess läuft, Zeile existiert) → gehört als Python-Check in auto_check.py, NICHT in einen Claude-Loop. Kostet dort 0 Tokens. Baue es dort ein, wenn es fehlt.
b) Braucht Urteilsvermögen (Log-Zeilen interpretieren, entscheiden ob ein Alert echt oder Fehlalarm ist, SSH-Forensik über mehrere Quellen) → /loop.
c) Hängt an einer Uhrzeit (Tagesabschluss, Morgenbriefing) → geplante Aufgabe / Cron, kein Loop. Loops takten in Intervallen, nicht nach Uhrzeit.
d) Ereignisgetrieben (Buch geändert → funded_finalize.py) → bleibt Regel in CLAUDE.md, kein Loop. Ein Loop, der pollt ob ich etwas geändert habe, ist Tokenverschwendung.

SCHRITT 3: DIESE LOOPS BAUEN (Vorschlag, prüfe kritisch und passe an)

LOOP 1 „Box-Watch" (der wichtige):
- Nur relevant, solange Sim oder Eval aktiv handelt. Aktuell ist FIREFIGHT (alles deaktiviert, siehe Bereiche/Eval-Passing.md): dann reicht ein Tick pro 60 Min oder der Loop bleibt aus, bis ich den Sim-Neustart melde. Frag mich das am Anfang.
- Pro Tick GENAU EIN gebündelter SSH-Aufruf (ssh Administrator@100.127.89.9, Key liegt lokal, kein Passwort), der in einem einzigen Remote-Befehl liefert:
  1. Läuft der NinjaTrader-Prozess (PID + RAM)?
  2. Letzte Zeile + Zeitstempel MIT DATUM der heutigen NT8-Logdatei (nur tail, nie die ganze Datei).
  3. LastWriteTime MIT DATUM der bars_*.csv-Dateien und von maxlab_equity.csv. WICHTIG (AP87-Falle): immer volles Datum vergleichen, nie nur Uhrzeit. Und wissen: bars_MNQ.csv ist tot (schrieb nur das entfernte ORBBreakout-Bein), die zählt nicht als Frische-Signal.
  4. Fehler-Grep über die letzten ~50 Logzeilen (Disconnect, Rejected, Error).
- Bewertung im Kopf, nicht im Chat: alles plausibel → ScheduleWakeup mit noop:true, KEINE Ausgabe an mich. Etwas faul → 3-5 Zeilen Diagnose, bei Handlungsbedarf PushNotification an mich und Ticket in engine\tasks.json anlegen.
- Harte Verbote im Loop: NIE NT8 selbst neu starten (Wiederanlauf braucht eine RDP-Anmeldung, AP86), NIE deployen, NIE Strategien enablen/disablen, NIE Dateien auf der Box ändern. Der Loop ist read-only, Eingriffe schlage ich vor und Max entscheidet.
- Intervall: während Handelszeiten (15:30-22:15 deutsche Zeit) 1800s, außerhalb 3600s. Session-Ende Freitagabend: Loop anbieten zu stoppen.

LOOP 2 „Sim-Abgleich" NUR falls die Sim-Phase wieder läuft, sonst weglassen:
- 1x pro Handelstag nach US-Close reicht → das ist Fall c) aus Schritt 2, also NICHT als Loop bauen, sondern als geplante Aufgabe oder als Erweiterung von auto_check.py (Fills des Tages vs. Backtest-Erwartung, Equity-Zeile für heute vorhanden). Sag mir, welchen Weg du nimmst, und bau ihn.

MEHR LOOPS NICHT. Wenn dir beim Bestandsaufnehmen etwas auffällt, das überwacht gehört: erst Einordnung nach Schritt 2, dann Vorschlag an mich, nicht einfach bauen.

SCHRITT 4: TOKEN-REGELN FÜR JEDEN LOOP-TICK (hart einhalten)
- Ein Tick = maximal ein SSH-Batch + eine kurze Bewertung. Keine Subagents im Tick (die kosten eigenen Kontext), es sei denn ein Alarmfall braucht echte Forensik, dann einmalig.
- Nur tail/Select-String, nie ganze Logs oder CSVs einlesen. Große Outputs bleiben auf der Box.
- Grüne Ticks sind stumm (noop:true). Ich will nur bei Abweichungen etwas lesen.
- Kein Tick schreibt in den Vault. Vault-Einträge nur bei echten Vorfällen (Daily Note + ggf. Ticket).

SCHRITT 5: ABNAHME
- Spiel Loop 1 einmal manuell durch (ein einzelner Tick, mit echtem SSH-Aufruf) und zeig mir das Ergebnis-Format.
- Dokumentiere die fertigen Loops in Ressourcen/Loop-Bauplan (Prompt für Claude).md unter „Aktive Loops" (was läuft, Intervall, wie stoppen).
- Sag mir am Ende: welche Checks du stattdessen in auto_check.py eingebaut hast, was bewusst NICHT geloopt wird und warum.
```

---

## 🟢 Aktive Loops (führt Claude beim Einrichten nach)

*Noch keine eingerichtet. Stand 11.08.2026: FIREFIGHT aktiv, nichts handelt live, Box-Watch lohnt erst ab dem Sim-Neustart (nach AP53).*

## 🧠 Warum so und nicht anders (Kurzbegründung)

- **Loops sind teuer pro Tick** (jeder Tick ist ein LLM-Aufruf mit vollem Sessionkontext). Deshalb wandert alles rein Mechanische in `auto_check.py` (0 Tokens) und der Loop macht nur das, wofür man ein Urteil braucht.
- **Loops leben nur in einer offenen Session.** Für „läuft auch wenn der Rechner zu ist" sind Windows-Tasks (gibt es schon) oder geplante Cloud-Agents das richtige Werkzeug.
- **Ein Loop, der stumm grün tickt, ist der beste Loop.** noop-Ticks werden im Terminal kollabiert und kosten fast nichts an Aufmerksamkeit.
