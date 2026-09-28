---
tags: [vorfall, nt8, box, live]
date: 2026-09-26
status: Befund fertig, Entscheidungen bei Max offen
---

Zusammenhang: [[Live-Setup (Algo auf Prop)]], [[VPS-Einrichtung Schritt für Schritt]], [[Daily Notes/2026-09-26]], Ticket AP86. Ermittelt per Workflow `wf_4a79cea0-e73` (box-ops, Trace-Forensik, Historie, Code-Risiko, Watchdog/AP86, Recherche, 3 Skeptiker).

# Befund: Verbindungsabriss E8 und FundedNext, Fr 25.09. / Sa 26.09.

**Kurz vorweg, Boss:** Du hast recht, es lag nicht an der Box. Die Firmen-Seite ist abgerissen: Tradovate hat Fr 18:16 ET E8 und FN gleichzeitig gekappt. Die 10 Stunden Ausfall kamen aber von NT8 und unserem Setup, nicht von Tradovate. Geschadet hat es nichts, weil der Markt zu war und alle Konten flat. Stand jetzt ist alles grün.

---

## 1) Was passiert ist

| ET | dt. Zeit | Was |
|---|---|---|
| Fr 15:55 | Fr 21:55 | Zeit-Exit: E8, FN71491 und FN89622 flat, alle Stops und Targets storniert |
| Fr 18:05:19 | Sa 00:05 | Der Aussetzer, den es jeden Freitag gibt, nach 1 s wieder da |
| Fr 18:16:05 und 18:16:12 | Sa 00:16 | Tradovate schließt erst den Kursdaten-Socket, dann den Order-Socket, bei E8 und FN mit 20 ms Abstand |
| Fr 18:17:06 | Sa 00:17 | Alle 12 Strategien gehen aus („will be restarted“, Schwelle 60 s) |
| Fr 18:18:03 und 18:18:19 | Sa 00:18 | Watchdog schickt den Alarm per Telegram. 16 s später meldet NT8 bei E8 und FN „Panic“ und versucht danach nie wieder zu verbinden |
| Fr 18:42 bis 19:50 | Sa 00:42 bis 01:50 | Der Login-Server von NinjaTrader lehnt die Token-Erneuerung ab und fängt sich dann von selbst |
| Sa 04:38:41 und 04:38:48 | Sa 10:38 | RDP-Anmeldung, je ein Connect-Klick für E8 und für FN. Von 04:39:01 bis 04:39:11 laufen alle 12 Strategien von selbst wieder an |
| Sa 05:02 | Sa 11:02 | NT8 wird von Hand geschlossen und neu gestartet (neue PID 7092). Um 05:07 sind wieder 12 Strategien aktiv, der Watchdog meldet ab 11:08 dt. ok |

## 2) Woher es kommt

**Auslöser ist das Tradovate-Backend, nicht die Box.** Dass die Gegenstelle aktiv geschlossen hat, ist sicher. Dass die Ursache bei Tradovate liegt, ist sehr wahrscheinlich.
- Im Trace steht „remote party closed the WebSocket connection without completing the close handshake“. Die Heartbeats waren bis zum Abriss 1 bis 5 s alt. Die 21.600.000 ms im Trace sind nur die 6 h Zeitzonen-Versatz zwischen Box und NT8, ein stiller Ausfall vorher war das nicht.
- Das Netz der Box lief: Der Telegram-Alarm ging um 18:18:03 ET raus, mitten in den Reconnect-Versuchen. Der Datenserver von NinjaTrader hat keinen Verlust gemeldet, und im Windows-Log gibt es keine Netz-Events.
- Stärkstes Indiz: Kursdaten- und Order-Socket laufen zur selben IP, sind aber 6 s versetzt gefallen. Ein Netzausfall hätte beide gleichzeitig getroffen. Das Bild passt nur zu einem Neustart einzelner Dienste auf der Serverseite.
- Das Muster wiederholt sich jeden Freitag gegen 18:05 ET (04., 11., 18. und 25.09.) und samstags gegen 03:00 ET (05., 12. und 19.09.). Das sieht nach einem Wartungsfenster aus, eine Primärquelle dafür fehlt aber (**offen**).
- **Zu deinem Hinweis:** E8 und FN laufen beide über dieselbe Tradovate-Demo-Umgebung (demo.tradovateapi.com, gleiche IP, Kontotyp Simulation). Dass beide gleichzeitig fallen, sind also keine zwei unabhängigen Zeugen, sondern ein und dasselbe Backend.

**Warum es 10 Stunden gedauert hat, liegt an NT8 und an uns (sicher).**
- NT8 hat ca. 2 Min lang neu verbunden. Das waren rund 11 Versuche je Kanal, und jeder hing ca. 9 s im Aufbau. Danach kam „Panic“ und bis zum Klick um 04:38 ET kein einziger Versuch mehr.
- Wie lange Tradovate wirklich weg war, weiß niemand: mindestens 2 Min, höchstens gut 10 h. Der Login-Server war ab 19:50 ET wieder gesund. Wenn NT8 über die 2 Min hinaus weiter versucht hätte, wäre der Ausfall vermutlich auf Minuten bis ca. 1,5 h geschrumpft. Getestet ist das nie.
- Dazu kommt: Der Auto-Restart ist per Flag pausiert, eine Reconnect-Funktion gibt es nicht, und bei dir war Nacht.

**Was an der ersten Ermittlung nicht stimmte:**
- Die Heilung war nicht automatisch, sondern zwei Klicks per RDP. Automatisch lief nur das Wiederanlaufen der Strategien nach dem Connect.
- NT8 läuft nicht mehr als PID 7500 seit 22.09., sondern seit Sa 11:02 dt. als PID 7092.
- Der Neustart der Strategien (Recalculate, 60 s, 20 Versuche in 60 Min) hat funktioniert und nicht versagt. Gefehlt hat nur die Verbindung.
- `connectAttempts=3` ist ein Zähler, kein Limit. Die Panic kommt nach Zeit, nach ca. 2 Minuten.
- Ein einzelner Connect reicht nicht, jede Verbindung braucht ihren eigenen (E8 und Tradovate/FN!).

## 3) Was es macht und wie groß das Risiko ist

**Gestern: kein Risiko (sicher).** Alle drei Konten waren um 15:55:01 ET flat. Zwischen 17:51 und dem Abriss lag keine Order.

**Worst Case, wenn intraday eine Position offen ist.** Das ist noch nie passiert, die Punkte sind aus der Konfiguration abgeleitet:
- Beim Abschalten bleibt der Stop stehen, weil `CancelExitsOnStrategyDisable=False` gesetzt ist und Stops und Targets echte Tradovate-Orders sind. PowerHour und Momentum haben nur einen Stop, AsiaDir hat Stop und Target. Die Konfiguration ist belegt, beobachtet wurde es nie (**mittel**).
- Ab dem Abschalten fällt weg: der Zeit-Exit 15:55, der Break-Even-Nachzug bei Momentum und der **komplette RiskGuard** (Tagesverlust, Trailing-DD, Consistency, News-Flat). RiskGuard geht im selben Block aus.
- Nach unten deckelt der Zwangsschluss durch die Firma um 16:10 ET (22:10 dt.). Für FN ist das über die Knowledge-Base belegt, für E8 gibt es nur eine Sekundärquelle.
- **Der eigentliche Worst Case ist das Wiederanlaufen.** Nach dem Reconnect starten alle Beine mit WaitUntilFlat neu und übernehmen die offene Position nicht mehr. Ob NT8 dabei den alten Stop beim Broker storniert, ist **ungeprüft** (die Funktion `SyncCancelOldLiveOrders` existiert). Dann läge die Position bis 16:10 ET ohne Stop.
- Startet RiskGuard mitten am Tag neu, setzt er die Basis für den Tagesverlust auf den Kontostand beim Neustart. Verluste vor dem Abriss zählen dann nicht mehr gegen die 900 $ (E8) bzw. 600 $ (FN). Scharf bleibt nur die Untergrenze aus dem gespeicherten Höchststand (sicher, `MaxRiskGuard.cs:371-395`).
- Einen Abriss mit offener Position gab es schon: Am 21.09. um 11:55 ET und am 23.09. um 15:51 ET fiel der Kursdaten-Kanal von FN, während Momentum offen war. Beide Male war er in unter 1 s zurück. Eine Panic mit offener Position gab es noch nie.

**Montag 28.09. ohne Eingriff:**
- Beide Verbindungen sind grün, alle 12 Instanzen aktiv. Kommt bis Mo 09:30 ET (15:30 dt.) keine neue Panic, handeln E8, FN1 und FN2 normal. Genauso lief es schon am 21./22.09., mit demselben Start und der virtuellen 1L bei PowerHour. Montag ist kein Makro-Tag, der NFP kommt erst am 02.10. (**mittel bis hoch**)
- Das Fenster Samstag 03:00 ET ist vorbei. Am Sonntag oder Montag vor Handelsstart gab es noch nie eine Panic. Beobachtbar war das allerdings nur an 2 bis 3 Wochenenden.
- Zu erwarten ist ein kurzer Aussetzer jeden Tag gegen 05:04 ET (11:04 dt.), dazu zufällige während der Handelszeit. Bisher waren alle in unter 2 s weg.
- Restrisiken:
  1. Kommt doch eine Panic, heilt nichts automatisch.
  2. Stirbt nur FN, kann der Watchdog trotzdem „ok“ melden (siehe 5). Das fällt dann erst ab 09:30 ET auf.
  3. Ein Neustart durch Windows Update: Ein Neustart-Flag ist nicht gesetzt, aber `PendingFileRenameOperations=True`, und am 15.08. hat Windows die Box schon einmal selbst neu gestartet. Dann hängt NT8 im Login-Fenster und handelt nicht ohne dich. Unwahrscheinlich, aber möglich.
- Nebenpunkt: Beim Wiederanlaufen um 04:39 und 05:07 storniert NT8 auf jedem Konto eine „Stop loss“-Order. Laut Gegenprüfung sind das virtuelle Historien-Orders von PowerHour (IDs NT-000xx), die Konten sind flat. Ein Blick in den Tab Orders reicht (Schritt 6a.2).

## 4) Wie oft schon

| # | Tag | Zeit ET (dt.) | Markt | Konten | Ursache | Position | Wieder da | Verpasst |
|---|---|---|---|---|---|---|---|---|
| 1 | Di 01.09. | 08:18 (14:18) | offen, vor RTH | E8 | Netz bei Box oder Anbieter (Datenserver weg, Latenz 14,6 s) | keine | 10:24 ET per Klick | ca. 56 Min RTH |
| 2 | Mi 02.09. | 02:00 (08:00) | offen | E8 | kurzer Abriss, keine Panic | keine | 02:01 ET von selbst | nichts |
| 3 | Mi 02.09. | 18:38 (00:38) | offen | E8 | DNS-Ausfall auf der Box | keine | Do 17:26 ET per Neustart | ganzer RTH-Tag Do 03.09. |
| 4 | Sa 05.09. | 03:01 (09:01) | zu | E8 | Tradovate, Samstagsfenster | keine | So 06.09. ca. 17:30 ET | nichts |
| 5 | Sa 12.09. | 03:20 (09:20) | zu | E8 + FN | Tradovate, Samstagsfenster | keine | Mo 14.09. 08:34 ET per Klick | nichts |
| 6 | Fr 18.09. | 18:06 (00:06) | zu | E8 + FN | Tradovate, Freitagsfenster, nur der Order-Kanal (Typ B) | keine | Verbindung 18:56 ET per Klick, Strategien erst Sa 13:01 ET | nichts |
| 7 | Fr 25.09. | 18:16 (00:16) | zu | E8 + FN | Tradovate, Freitagsfenster (Typ A) | keine | Sa 04:38 ET per Klick | nichts |

- Verpasste Handelszeit insgesamt: 1 RTH-Tag plus 56 Min. Beides war Anfang September, nur E8, und beide Male lag es am Netz auf der Box- oder Anbieterseite. Seit FN live ist (06.09.) und seit den neuen Schwellen (09.09.) ging keine Minute Handelszeit mehr verloren.
- Seit 05.09. lagen alle 4 Panics am Wochenende, und alle kamen von der Tradovate-Seite.
- **Typ A** (Kursdaten zuerst über 60 s weg, „will be restarted“): Ein Connect je Verbindung genügt, die Strategien starten von selbst.
- **Typ B** (nur der Order-Kanal weg): Die Strategien bleiben auch nach dem Reconnect aus und brauchen die Haken von Hand.
- Die Logs vom 18.08. bis 31.08. existieren nicht mehr. Die vom 01. bis 05.09. gibt es nur noch lokal im Scratchpad.

## 5) Warum die Absicherung nicht gegriffen hat

| Baustein | Stand | Am 25.09. |
|---|---|---|
| Watchdog-Erkennung + Telegram | läuft | hat funktioniert: Alarm 00:18 dt., danach stündlich bis 09:38 (10 Pushes), kein Sendefehler. Ob sie am Handy ankamen, ist offen |
| Auto-Restart (AP86 Schritt 1) | gebaut, seit 06.09. 23:12 durch `nt8_autorestart_pause.flag` pausiert | lief nicht, **und das war richtig**: Ein Neustart endet im Login-Fenster (kein „Remember me“, SFT-5780, keine hinterlegten Zugangsdaten). Dass die Strategien danach von selbst zurückkommen, ist nicht belegt |
| Reconnect im laufenden NT8 | gibt es nicht, `nt8_control.ps1` kann nur Stop, Start, Test und Zählen | genau das hätte gereicht, ohne Passwort (am 26.09. bewiesen) |
| `MaxConnectionWatchdog.cs` (AddOn, verbindet mit Wartezeiten neu) | am 03.09. gebaut, nie deployed, steht in keinem Ticket und keiner Notiz | lief nie |
| Strategien wieder einschalten (AP86 Schritt 2, AP134, AP137-6) | nicht gebaut, die UIA-Skripte fehlen auf der Box | am 25.09. nicht nötig (Typ A), am 18.09. schon (Typ B) |
| Schwelle 60 s / 20 Versuche in 60 Min (AP86 Schritt 3) | läuft seit 09.09., im Ticket steht sie noch als offen | hat korrekt gearbeitet, hilft aber nicht gegen die Panic |

**Kern:** Wir haben einen Alarm, aber keine Heilung. Das einzige Heilmittel, der Neustart, passt nicht zu dieser Art Fehler und ist deshalb zu Recht pausiert. Das passende Werkzeug liegt halbfertig in `MaxConnectionWatchdog.cs`.

Schwächen im Watchdog:
- Die Bereitschaftsprüfung liest nur die letzte Connection-Zeile über beide Verbindungen. Ein toter FN kann hinter einem gesunden E8 verschwinden.
- Der Strategie-Zähler liest nur die letzten 3 Logdateien. Vor dem Vorfall meldete er deshalb 2 statt 12, und Alarm schlägt er erst bei 0.
- Die Log-Rotation greift nicht: Die Datei hat 2 MB statt 500 KB, weil ein Sperrfehler verschluckt wird.
- Dein Neustart um 11:02 hat einen Fehlalarm ausgelöst.

Veraltete oder falsche Tickets:
- AP86: guide[6] und guide[7] sind erledigt.
- AP134 guide[1] sagt, `nt8_uia_inspect.ps1` liegt auf der Box. Die Datei fehlt.
- AP145.why stützt sich auf einen Restart vom 06.09., der in Wahrheit fälschlich als „bereit“ gemeldet wurde. Die Entscheidung zu AP145 ist seit 17 Tagen offen.
- Der VPS-Leitfaden Teil 9 ist veraltet.

## 6) Fix-Vorschlag

### a) SOFORT, vor So 18:00 ET (Mo 00:00 dt.)

Es ist alles grün. Die Schritte hier sichern ab, repariert werden muss nichts.

1. **Telegram prüfen** (Handy, 1 Min): Chat mit @maxbotalgobot öffnen.
   - Sehen solltest du am 26.09. Alarme um 00:18, 01:18, 02:18, 03:18, 04:23, 05:23, 06:23, 07:28, 08:33 und 09:38, dazu einen um 11:03 (dein Neustart).
   - Wenn sie fehlen: Dann ist der Alarmweg kaputt und du würdest eine Panic am Montag nicht mitbekommen. Sag Bescheid, dann prüfe ich den Versand per SSH.
2. **RDP auf die Box, NT8 Control Center:**
   - Unten links sind E8 und Tradovate/FN! grün (Connected).
   - Tab **Strategies**: 12 Zeilen (RiskGuard, PowerHourNQ, MomentumNQ und AsiaDirNQ, jeweils auf E8, FN71491 und FN89622), überall ein Haken bei Enabled. PowerHour mit virtueller Position 1L ist normal.
   - Tab **Positions**: alle drei Konten flat. Tab **Orders**: keine Order im Status Working auf den drei Konten.
   - Wenn eine Verbindung rot ist: weiter mit Schritt 5.
   - Wenn einer Strategie der Haken fehlt: Haken setzen. Das ist bei flachem Konto unkritisch (WaitUntilFlat).
   - Wenn eine Position offen ist oder eine Working-Order dasteht: nichts anklicken, Screenshot machen, Bescheid geben.
3. **Nicht anfassen:** Das Flag `C:\Users\Administrator\nt8_autorestart_pause.flag` bleibt liegen. NT8 nicht ohne Grund neu starten: Ein Neustart heißt Login-Fenster, ein Connect-Klick nicht.
4. **Optional, deine Entscheidung (siehe 6c):** Windows Update auf der Box pausieren, über Einstellungen → Windows Update → „Updates für 1 Woche aussetzen“. Danach sollte dort „Updates angehalten bis …“ stehen. Damit ist das Risiko eines Update-Neustarts bis Montag weg.
5. **Notfall-Ablauf**, falls bis Montag eine Telegram-Meldung „nicht handelsbereit“ kommt:
   1. RDP auf die Box, Control Center, Tab **Log**: Steht dort „Unable to re-establish the connection. (Panic)“?
   2. Menü **Connections** → **E8** klicken, danach **Tradovate/FN!** klicken. Jede Verbindung braucht ihren eigenen Klick.
   3. Nach ca. 30 s sollten beide grün sein und im Tab Strategies wieder 12 Haken stehen. Am 26.09. kamen sie rund 20 s nach dem Connect von selbst.
   - Fehlerfall A, die Verbindung fällt gleich wieder: 15 Min warten, nochmal klicken. Direkt nach einer Panic kann das Backend noch zu sein (am 25.09. war der Login bis 19:50 ET gestört).
   - Fehlerfall B, verbunden, aber die Haken fehlen (Typ B wie am 18.09.): alle 12 bei Enabled von Hand setzen.
   - Fehlerfall C, NT8 hängt im Login-Fenster (nach einem Windows-Neustart): Passwort eingeben, dann Schritt 2 und 3, Haken falls nötig von Hand.
   - **NT8 nicht als erste Maßnahme schließen.**
   - Zeitziel: am besten vor So 18:00 ET (Mo 00:00 dt.), spätestens Mo 09:25 ET (15:25 dt.). AsiaDir steigt um 09:30 ein, Momentum um 09:45 ET.
6. **Montag vor 15:25 dt.** ein kurzer Blick auf unten links und den Tab Strategies, weil der Watchdog eine Panic nur bei FN verdecken kann. Alternativ prüfe ich das per SSH für jede Verbindung einzeln (siehe 6c.4).

### b) Dauerhaft (Reihenfolge = Priorität)

1. **Reconnect-AddOn.** Das schließt alle 4 Wochenend-Panics seit 05.09. Basis ist `C:\Users\maxlk\Projects\trading-data\engine\ninjascript\MaxConnectionWatchdog.cs`.
   - Erst auslösen, wenn der Status nach der Panic auf Disconnected steht. Heute greift es schon 15 s nach „ConnectionLost“ und kommt damit NT8s eigenen Versuchen in die Quere.
   - Jede Verbindung (E8 und Tradovate/FN!) einzeln neu verbinden (`Connection.Connect`), mit wachsenden Abständen, z.B. nach 5, 15 und 30 Min, dann alle 30 Min bis So 17:45 ET. Ein Passwort braucht es nicht.
   - Den `SetState`-Teil rauswerfen: Strategien per AddOn einschalten ist laut NT-Support nicht vorgesehen. Typ A braucht das auch nicht, Recalculate startet die Strategien selbst.
   - Erst einmal nur scharf, wenn der Markt zu ist und alle Konten flat sind. Wie das Wiederanlaufen mit offener Position abläuft, ist ungeprüft (Punkt 3).
   - Telegram bei jedem Versuch, bei Erfolg und beim Aufgeben.
   - Test: am Wochenende eine Sim-Verbindung trennen und zuschauen. Deploy über `box_deploy.ps1` braucht einen NT8-Neustart, also RDP. **Nicht vor Montag deployen.**
   - Aufwand: mittel, grob ein halber bis ganzer Tag plus ein Test-Wochenende. Ob `Connection.Connect` zur Laufzeit wirklich funktioniert, ist unbelegt, geprüft ist nur, dass es die Funktion gibt.
2. **Watchdog schärfen** (auf der Box, `nt8_control.ps1` und `maxlab_watchdog.ps1`). Aufwand klein, 1 bis 2 h.
   - `Test-NT8Ready` (`nt8_control.ps1:86-127`) für jede Verbindung einzeln auswerten.
   - Den Strategie-Zähler (Z.138-139) über die Logs der laufenden Instanz rechnen lassen. Soll ist 12, Alarm schon bei weniger als 12 (`maxlab_watchdog.ps1:48` steht heute auf 0).
   - Die Log-Rotation reparieren (Z.18-20) und eine Markierung für gewollte Neustarts einbauen.
3. **Wiederanlauf mit offener Position klären**, im Sim und bevor Punkt 1 auch intraday laufen darf: Position offen, Verbindung trennen bis zum Abschalten, dann wieder verbinden. Bleibt der Stop beim Broker stehen? Übernimmt die Strategie die Position? Dazu soll RiskGuard den Tagesstartwert speichern (`MaxRiskGuard.cs:371-395`), statt beim Neustart den aktuellen Kontostand zu nehmen. Aufwand mittel.
4. **Typ B** (Strategien bleiben nach dem Reconnect aus): Ohne Desktop gibt es keinen belegten Weg. Per AddOn ist Einschalten nicht vorgesehen, UIA in einer getrennten RDP-Session ist unbelegt, und tscon ist blockiert (AP136). Bis dahin reicht der schärfere Zähler aus Punkt 2 als Alarm. Aufwand unklar.
5. **Recherche** per research-scout: Wartet Tradovate fest am Freitag gegen 18:05 ET und am Samstag gegen 03:00 ET? Primärquelle suchen und in den Research-Cache eintragen. Bestätigt sich das, startet der Reconnect gezielt nach dem Fenster. Aufwand klein.
6. **Tickets und Doku:** AP86, AP134 guide[1], AP145.why und VPS-Leitfaden Teil 9 korrigieren, dazu ein neues Ticket für das Reconnect-AddOn (vorher `--pull`). Aufwand klein.

### c) Was du entscheiden musst

1. Reconnect-AddOn bauen? Meine Empfehlung: ja, zuerst nur für „Markt zu und alle Konten flat“. Damit wäre auch AP145 entschieden.
2. Pause-Flag: bleibt es liegen, bis das AddOn läuft? Meine Empfehlung: ja.
3. Windows Update auf der Box für eine Woche pausieren (Schritt a4)?
4. Aufsicht, bis das AddOn steht: Soll ich Sonntagabend und Montag vor 15:30 dt. jede Verbindung per SSH prüfen, oder machst du das selbst?
5. FundedNext-Connector neu verbinden. Der steht auf `AUTH_EXPIRED`, deshalb kann ich Positionen gerade nicht unabhängig von NT8 gegenprüfen.
6. Tickets und Doku nachziehen lassen (6b.6)?

## 7) Offene Fragen

- Warst du das um 10:38 dt. (Connect) und um 11:02 (Neustart), oder eine Claude-Session mit Computer-Use? Das Log trennt das nicht, beide Anmeldungen kamen per RDP von DESKTOP-0N79A35. Und warum der Neustart?
- Sind die Telegram-Alarme angekommen? (Schritt a1)
- Hat Tradovate feste Wartungsfenster am Freitag gegen 18:05 und am Samstag gegen 03:00 ET? **Komplett unbeantwortet:** Der Hook hat die Websuche geblockt, weil der research-scout-Schritt in der Recherche-Kette nicht quittiert war.
- Ab wann hätte Tradovate wieder Verbindungen angenommen? Zwischen 18:18 und 04:38 ET hat niemand angefragt.
- Was passiert beim Wiederanlaufen mit einem noch offenen Stop beim Broker? Der NT8-Kern ist verschleiert und lässt sich nicht lesen, klären lässt sich das nur per Sim-Test.
- Wurden am 01.09. (09:30 bis 10:26 ET) oder am 03.09. Signale verpasst? Das zeigt nur ein Replay.
- Die Vorfälle vom 18.08. bis 31.08. lassen sich nicht mehr prüfen, die Logs sind weg.

**Nebenbefunde** (gehören nicht zum Vorfall):
- **21.09.:** FN1 und FN2 standen nach 15:55 ET netto Short 2 ohne Stop. Du hattest vorher per Limit-Sell von Hand geschlossen, und der Zeit-Exit hat trotzdem noch verkauft. Um 15:57 ET wurde dann per Chart Trader geschlossen. Die Lehre: Wer außerhalb der Strategie flattet, erzeugt beim Zeit-Exit eine ungeschützte Gegenposition. Also vorher die Strategie ausschalten und danach im Tab Orders nach verwaisten Stops schauen.
- **21.09. 13:01 ET:** E8 hat den Break-Even-Nachzug abgelehnt (InvalidPrice), der Stop blieb auf 30340. Der Break-Even kann also auch bei stehender Verbindung ausfallen.
- Die Discovery-Queue ist seit über 20 h leer, weil alle Vorlagen durchgerechnet sind. Das ist ein eigenes Thema für den alpha-scout.

---

**Kurzfassung:** Tradovate hat Fr 18:16 ET E8 und FN gleichzeitig gekappt. NT8 hat nach 2 Min aufgegeben, und erst ein Klick per RDP am Sa um 10:38 dt. hat die Verbindung zurückgebracht. Schaden gab es keinen, der Markt war zu und alles flat. Das ist die vierte Panic an einem Wochenende seit 05.09., jedes Mal kam sie von Tradovate. Unser Watchdog kann alarmieren, aber nicht heilen. Jetzt sind nur Telegram und Control Center kurz zu prüfen, und du solltest den Klickweg für den Notfall parat haben. Dauerhaft kommt ein Reconnect-AddOn aus dem schon gebauten `MaxConnectionWatchdog.cs` dazu, plus ein Watchdog, der jede Verbindung einzeln prüft und gegen 12 Strategien zählt.