---
tags:
  - ressource
  - trading/infrastruktur
erstellt: 2026-08-11
---
# 🔁 Loop-Bauplan (Prompt für Claude)

⬅️ [[Day Trading]] · [[Eval-Passing]] · Box-Regeln: [[VPS-Einrichtung Schritt für Schritt]]

> [!info] Wie benutzen
> Für jeden Loop unten: **neue, frische Session** öffnen (`/clear`), Modell **sonnet** reicht. Dann `/loop` eintippen und den zugehörigen Prompt einfügen. Jeder Loop läuft in seiner eigenen Session, damit du sie einzeln starten, beobachten und stoppen kannst, ohne dass sie sich gegenseitig im Kontext stören.
>
> Stoppen geht jederzeit mit einer normalen Nachricht („stopp den Loop") oder per Escape. Ein Loop lebt nur innerhalb seiner Session: Terminal zu, Loop weg. Für Loop 3 (wöchentlicher Rhythmus) ist das ein echter Nachteil, steht unten beim Loop selbst vermerkt.

---

## 🖥️ Loop 1: Box-Watch (VPS/NT8-Gesundheit)

**Wofür:** merkt automatisch, wenn NT8, der Feed oder die Datenpipeline auf der Box hakt, mit minimalem Tokenverbrauch pro Check.

```
Du überwachst read-only die Trading-Box (SSH Administrator@100.127.89.9, Tailscale, Key liegt lokal unter C:\Users\maxlk\.ssh\id_ed25519, kein Passwort nötig, Hostname vmd202078, deutsche Zeitzone). Ziel: mitbekommen, wenn NT8, der Feed oder die Datenpipeline hakt, mit so wenig Tokens wie möglich pro Tick.

Pro Tick:
1. EIN gebündelter SSH-Befehl, der in einem Remote-Aufruf liefert: ob der NinjaTrader-Prozess läuft (PID, RAM), die letzten ca. 10 Zeilen des heutigen NT8-Logs, LastWriteTime MIT VOLLEM DATUM (nicht nur Uhrzeit) von bars_MES.csv, bars_M2K.csv und maxlab_equity.csv, sowie ein Grep über die letzten ca. 50 Logzeilen nach Disconnect, Rejected, Error.
   Ausnahme: bars_MNQ.csv NICHT als Frische-Signal werten, die Datei ist tot (schrieb nur das entfernte ORBBreakout-Bein).
2. Bewertung im Kopf: NT8 läuft, Feed laut Log connected, Dateien sind heute beschrieben (volles Datum vergleichen, nicht nur die Uhrzeit), keine Fehlerzeilen. Dann alles grün, keine Ausgabe an mich, ScheduleWakeup mit noop:true.
3. Bei Abweichung: 3 bis 5 Zeilen Diagnose an mich, dazu PushNotification, und falls es ein echtes neues Problem ist ein Ticket in C:\Users\maxlk\Projects\trading-data\engine\tasks.json anlegen (gleiches Format wie die bestehenden Einträge, nächste freie AP-Nummer verwenden).

Harte Regeln:
- Niemals NT8 selbst neu starten (der Wiederanlauf braucht eine angemeldete RDP-Session, siehe AP86), niemals deployen, niemals Strategien enablen oder disablen, niemals Dateien auf der Box ändern. Nur lesen und melden, Eingriffe schlage ich vor, ich entscheide.
- Nie ganze Logs oder CSVs einlesen, nur tail beziehungsweise grep auf der Box selbst ausführen und nur das Ergebnis übertragen.
- Prüfe zuerst in Bereiche/Eval-Passing.md, ob FIREFIGHT aktiv ist. Solange ja: ein Tick pro Stunde reicht. Ist FIREFIGHT aufgehoben oder ich melde den Sim-Neustart: während 15:30 bis 22:15 Uhr deutscher Zeit alle 30 Minuten prüfen, außerhalb alle 60 Minuten.

Lege selbst fest, wann der nächste Tick sinnvoll ist (dynamisches Self-Pacing), und starte jetzt mit dem ersten Tick.
```

---

## 🔄 Loop 2: Lab-Sync-Watch (Portfolio-Tab-Sicherheitsnetz)

**Wofür:** die CLAUDE.md-Regel „Buch geändert, sofort funded_finalize.py nachziehen" läuft eigentlich ereignisgetrieben mit. Dieser Loop ist das Backup, falls das mal übersprungen wird, er heilt Drift selbst.

```
Du bist ein Sicherheitsnetz für die Synchronisation zwischen dem Trading-Buch und dem Strategy Lab. Regel dazu steht in CLAUDE.md: jede Änderung an book_state.json soll sofort per funded_finalize.py in den Portfolio-Tab gezogen werden. Dieser Loop fängt den Fall ab, dass das mal vergessen wird.

Pro Tick, im Verzeichnis C:\Users\maxlk\Projects\trading-data\engine:
1. Vergleiche die Änderungszeit von book_state.json mit der von portfolio.json.
2. Ist book_state.json nicht neuer als portfolio.json: alles synchron, keine Ausgabe an mich, ScheduleWakeup mit noop:true.
3. Ist book_state.json neuer: Buch oder Plan wurden geändert, ohne dass der Tab nachgezogen wurde. Führe `python funded_finalize.py` aus, prüfe den Exit-Code und dass in der neuen portfolio.json jedes Bein ein gültiges report-Feld hat (Datei existiert unter reports/). Melde mir in 2 bis 3 Zeilen, was neu synchronisiert wurde (welche Beine, welcher Plan jetzt aktiv ist). Keine PushNotification nötig, das ist Routine-Selbstheilung, keine Störung.
4. Klappt der Rebuild nicht (Exit-Code ungleich 0 oder ein fehlendes report-Feld): das ist ein echter Fehler. Ausführlich melden und bei Bedarf ein Ticket in tasks.json anlegen.

Intervall: alle 30 bis 45 Minuten reicht, das ist eine reine Konsistenzprüfung, kein zeitkritischer Vorgang. Self-Pacing ist okay.

Starte jetzt mit dem ersten Tick.
```

---

## 🧪 Loop 3: Discovery-Batch mit Agents (wöchentlich)

**Wofür:** `auto_check.py` erinnert nur an die fällige wöchentliche Discovery-Runde, führt sie aber nicht aus. Dieser Loop lässt sie über den `backtest-runner`-Agenten tatsächlich laufen, damit kein Rohlog in deinem Chat landet.

> [!warning] Nachteil dieses Loops
> Er braucht eine über mehrere Tage offene Session, sonst pausiert er beim Terminal-Schließen einfach (kein Datenverlust, aber kein Fortschritt bis zum nächsten Öffnen). Wenn dir das zu wacklig ist, sag Bescheid, dann bauen wir das stattdessen mit `/schedule` (Cron-Job, läuft auch ohne offene Session) statt mit `/loop`.

```
Du sorgst dafür, dass der wöchentliche Discovery-Batch tatsächlich läuft, nicht nur als Erinnerung in der Lab-Glocke steht (siehe der Kommentar zur Discovery-Kadenz in auto_check.py). Nutze dafür den backtest-runner-Agenten, nicht dich selbst direkt, damit kein volles Log in diesem Chat landet.

Pro Tick:
1. Prüfe in Bereiche/Strategie-Logbuch.md den Zeitstempel des letzten Eintrags mit „Discovery-Batch" im Titel.
2. Liegt der letzte Batch weniger als 6 Tage zurück: nichts tun, ScheduleWakeup mit noop:true, Intervall ca. 20 Stunden (das ist reine Wartezeit, nicht öfter prüfen).
3. Liegt er 6 Tage oder länger zurück UND FIREFIGHT ist laut Bereiche/Eval-Passing.md nicht aktiv: starte über das Agent-Tool den backtest-runner mit dem Auftrag, den nächsten offenen Discovery-Kandidaten aus der Idea Engine beziehungsweise dem Backlog zu identifizieren, als Batch zu fahren und nur die verdichtete Zusammenfassung zurückzugeben, kein Rohlog.
4. Trage das Ergebnis als neuen Eintrag in Bereiche/Strategie-Logbuch.md ein, nächste freie #-Nummer, im gleichen Format wie die bestehenden Einträge. Findet sich ein bank- oder buchtauglicher Fund: lege ein Ticket in tasks.json an (analog zu bestehenden Discovery-Tickets), triff die Buch-Entscheidung nicht selbst.
5. Danach wieder auf ca. 20 Stunden Intervall zurückgehen.

Sag mir direkt beim ersten Tick, falls FIREFIGHT gerade aktiv ist, dann pausiert der Loop bis es aufgehoben ist, statt stur weiterzuzählen.

Starte jetzt mit dem ersten Tick (nur der Zeitstempel-Check, keinen Batch erzwingen, wenn er noch nicht fällig ist).
```

---

## 🧠 Warum so und nicht anders (Kurzbegründung)

- **Loops sind teuer pro Tick** (jeder Tick ist ein LLM-Aufruf mit vollem Sessionkontext). Rein Mechanisches (Datei-Alter, Prozess läuft) wandert deshalb in Loop 2 nur als einfacher Vergleich, nie als Interpretation.
- **Loops leben nur in ihrer Session.** Für „läuft auch ohne offene Session" ist `/schedule` (Cron) das richtige Werkzeug, siehe der Hinweis bei Loop 3.
- **Ein Loop, der stumm grün tickt, ist der beste Loop.** noop-Ticks werden im Terminal kollabiert und kosten fast nichts an Aufmerksamkeit.
- **Getrennte Sessions statt eine gemeinsame:** so kannst du jeden Loop einzeln starten, pausieren oder stoppen, ohne die anderen zu berühren, und jeder Loop hat nur den Kontext, den er wirklich braucht.

## 🟢 Aktive Loops (trägt Claude beim Einrichten nach)

*Noch keine gestartet. Stand 11.08.2026: FIREFIGHT aktiv, Loop 1 lohnt erst ab dem Sim-Neustart, Loop 2 kann sofort laufen, Loop 3 pausiert automatisch bis FIREFIGHT grün ist.*
