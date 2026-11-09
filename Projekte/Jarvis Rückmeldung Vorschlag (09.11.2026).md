---
tags: [projekt, jarvis, vorschlag]
datum: 2026-11-09
---

# Jarvis: sofortige Rückmeldung bei fertigen Sessions und Aufträgen (Vorschlag)

**Anlass (Max, 09.11.2026):** Fertige Session-Antworten kamen erst, wenn Max nachfragte. Jarvis hat dann zu spät gemeldet. Nur Vorschlag, nichts umgebaut. Einordnung im Projekt: [[Jarvis Sprachsteuerung]].

## Was schon da ist (geprüft im Code, `C:\Claude\projekte\jarvis`)

| Baustein | Was er kann | Lücke |
|---|---|---|
| `arbeiter.py` (Hintergrund-Aufträge) | meldet fertige Aufträge selbst über die Ereignis-Warteschlange, sagt sie, sobald niemand redet | geht nur für Aufträge, die Jarvis selbst gestartet hat |
| `beobachter.py` | prüft alle 5 s Transkripte, erkennt „Antwort fertig" und „Frage an Max" (AskUserQuestion), kurz oder lang je nach Länge, überspringt Antworten, die Max schon gesehen hat | **beobachtet nur Sessions, die Jarvis selbst per SESSION geöffnet hat** (`merke()` wird nur dort aufgerufen). Alles, was Max selbst startet, fällt durch |
| `kontext.py` `neue_antworten()` | findet alle laufenden Sessions mit fertiger Antwort | **läuft nur, wenn Max etwas sagt** (Pull). Genau das Verhalten, das Max stört |
| Zusteller in `jarvis.py` | spricht Meldungen erst, wenn niemand redet, mit Signalton | funktioniert, braucht nur mehr Ereignisse |
| Cockpit-Leiste (`seen.json`, `sessions.json`) | liefert Gelesen-Marken und Session-Liste | nutzbar, nichts Neues nötig |
| Claude-Code-Werkzeug `PushNotification` | Systemhinweis aufs Gerät | optional, falls Jarvis aus ist |

Neue Agents sind **nicht nötig**. Das ist reine Programmlogik, kein Modell-Job. Der „Wer meldet" Teil sitzt schon im Zusteller.

## Ursache in einem Satz
Die Push-Meldung gibt es, aber nur für die kleine Menge von Sessions, die Jarvis öffnet. Alle anderen warten, bis Max fragt.

## Vorschlag

### Stufe 1 (klein, löst das Problem)
1. `Beobachter.pruefe()` nimmt zusätzlich **alle laufenden Sessions** aus `~/.claude/sessions/*.json` (Prozess lebt, Ordner nicht Jarvis selbst) statt nur die gemerkten. Titel aus dem Session-Namen. Gleiche Logik wie bisher: Ruhe abwarten, einmal je Antwort-ID melden, schon gelesene (Cockpit-Marke) überspringen.
2. Beim ersten Lauf nur Antworten der letzten Stunde melden (wie `MAX_ALTER_S` in `neue_antworten()`), sonst Meldungsflut beim Start.
3. `neue_antworten()` bleibt als Sicherheitsnetz bei Max' Eingabe, teilt sich aber die „schon gemeldet"-Liste mit dem Beobachter, damit nichts doppelt kommt.
4. Mehrere Meldungen auf einmal **bündeln** („drei Sessions fertig: …") statt einzeln hintereinander zu sprechen.

### Stufe 2 (Komfort)
5. **Alles gebündelt ohne Mikrofon-Pause:** wenn Max gerade redet oder Jarvis spricht, bleibt es in der Warteschlange und kommt danach (gibt es schon, nur prüfen).
6. **Ruhige Zeiten:** Meldungen nur ab Länge/Priorität sprechen, sonst nur Ton plus Zeile im Fenster. Max legt fest, was er hören will.
7. **Fertige Hintergrund-Aufträge** zusätzlich als Zeile in der Cockpit-Leiste (Haken), damit nichts nur in der Sprachausgabe verschwindet.
8. **Wenn Jarvis aus ist:** `PushNotification` als Rückfall (nur Hinweis „Session X hat Antwort", kein Text).

### Stufe 3 (nur wenn gewünscht)
9. Beim Session-Ende ein Hook (`Stop`) in der Session selbst schreibt eine Marke in eine Datei, Jarvis liest sie sofort statt alle 5 s zu pollen. Sofort statt bis 13 s Verzögerung, aber ein Hook in `C:\Claude` greift in jede Session ein. Nach der Pflicht „Hooks zuerst fragen" nur mit Max' OK.

## Risiken
- **Flut:** viele Sessions plus Schleifen können Meldungen auslösen. Gegenmittel: Bündeln, Mindestruhe, einmal je Antwort-ID.
- **Doppelte Meldung:** Beobachter und `neue_antworten()` brauchen eine gemeinsame Merkdatei.
- **Eigene Session ausnehmen:** Jarvis' Haupt-Session und die Arbeiter-Sessions („Jarvis: …") nicht melden.
- Haiku-Gehirn muss nach der Änderung frisch starten, sonst kennt die Haupt-Session die neue Fähigkeit nicht (Merke vom 06.11.).

## Was Max entscheiden muss
1. Stufe 1 bauen lassen? (Empfohlen: ja, rund eine Stunde Arbeit.)
2. Alle laufenden Sessions melden oder nur ausgewählte (z. B. nur mit Namen, nur im Cockpit angepinnte)?
3. Vorlesen oder nur Ton plus Fenster, wenn die Antwort lang ist? Jetzt gilt: kurz sagen, lang „klick rein".
4. Rückfall per Push-Hinweis, wenn Jarvis nicht läuft: ja oder nein?
5. Stufe 3 (Stop-Hook für Sofort-Meldung): ja oder erstmal nicht?
