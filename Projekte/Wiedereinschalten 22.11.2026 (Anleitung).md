---
tags: [trading, box, nt8, anleitung]
datum: 2026-11-22
status: Anleitung fertig, Ausführung Max So 22.11. abends
konten: [E8 E62701907262, FN1 FNFTFAMAXIMILIANKHO29486, FN2 FNFTFAMAXIMILIANKHO22193]
---

# Wiedereinschalten So 22.11.2026: Strategien auf der Box wieder an

Alle Zeiten sind **Boxzeit** (deutsche Zeit). Der Markt öffnet um 00:00 Boxzeit (So 18:00 ET), das erste Bein kommt am Mo um 15:30 Boxzeit (Asia, 09:30 ET). Heute Abend einschalten ist laut Host-Code unkritisch, Claude prüft danach trotzdem auf den Template-Wächter.

**Hauptkanal** ist die Session, in der diese Anleitung entstanden ist. Die **fett** gedruckten Stichworte schreibst du dort hinein, Claude macht den Rest per SSH.

## Ausgangslage (Claude per SSH, 22.11. nachmittags, nur gelesen)

- **Seit Di 17.11. 10:22 ET ist keine Strategie mehr an.** Nach dem Neustart am 17.11. liefen der FN1-Host und die Guards von E8 und FN1 nur eine Minute, die Hosts von E8 und FN2 und der Guard von FN2 gar nicht. Seitdem fehlen alle Trades, auch der erste OpEx-Freitag (20.11.).
- **Einstellungen stimmen:** alle 5 Beine je Konto wie im Buch, Code gleich dem Stand aus den Paritäts-Tests, Host-Configs werden per Konto automatisch gefunden. Die bestehenden RiskGuards haben `EvalProfitTarget=0` und holen Telegram, Limits und Inaktivität aus der cfg. **An den Eigenschaften der Strategien musst du nichts ändern.**
- **Chart passt:** MNQ 12-26, 1 Minute, `US Equities RTH`, 45 Tage. Chart nicht anfassen.
- **Falle:** NT8 hat zusätzliche Instanzen gespeichert, nämlich je einen zweiten Host für E8 und FN2 und einen zweiten Guard für FN2. Zwei Hosts auf einem Konto handeln doppelt. Deshalb Schritt 3.
- **Nicht dabei:** RiskGuard-Fix `2D4819A3` (Ziel 0 als Standard), LD01. Beides bleibt für später.

| Kurzname | Konto in NT8 | Floor | Tagesstopp |
|---|---|---|---|
| E8 | `E62701907262` | 48.000 $ | 900 $ |
| FN1 | `FNFTFAMAXIMILIANKHO29486` | 48.500 $ | 600 $ |
| FN2 | `FNFTFAMAXIMILIANKHO22193` | 48.500 $ | 600 $ |

## Schritt 0: E8 noch aktiv? (Browser, 2 Minuten)

Der Guard hatte für E8 als Frist für einen geschlossenen Trade den 17.11. genannt, dein Handtrade kam am 20.11. E8 zählt 7 Kalendertage.

1. E8-Dashboard öffnen, Konto `E62701907262` ansehen.
   - **Erwartet:** Status aktiv, kein Breach, keine Inaktivitäts-Meldung.
   - **Fehlerfall:** Konto inaktiv, gesperrt oder breached → in Schritt 4 **E8 auslassen** (weder Host noch Guard einschalten) und im Hauptkanal **„E8 tot“** schreiben.

FN ist kein Thema, dort gelten 30 Kalendertage.

## Schritt 1: RDP und Verbindungen

1. RDP auf `100.127.89.9`. NT8 läuft seit 17.11., **nicht neu starten**.
2. Control Center → **Connections:**
   - **Erwartet:** `E8` und `Tradovate/FN!` grün. `FundetFuturesNetwork` rot ist normal (FFN ist seit 26.10. zu), ignorieren.
   - **Fehlerfall:** `E8` oder `Tradovate/FN!` nicht grün → rechtsklick, Connect. Bleibt es rot, im Hauptkanal **„Verbindung rot“** schreiben und nicht weitermachen.

## Schritt 2: Alles flat?

1. Control Center → Reiter **Positions**: für alle drei Konten keine Zeile mit Menge.
2. Reiter **Orders**: keine Order im Zustand `Working` oder `Accepted`.
   - **Fehlerfall:** offene Position oder Order → nichts schließen, im Hauptkanal **„nicht flat“** schreiben.

## Schritt 3: Doppelte Instanzen raus

Control Center → Reiter **Strategies**. Spalte **Account** ansehen und je Konto zählen.

- **Ziel:** je Konto **genau 1× `MaxBookHost` und 1× `MaxRiskGuard`**, also 6 Zeilen.
- **Laut NT8-Datenbank zu erwarten:** E8 2 Hosts, FN2 2 Hosts und 2 Guards, FN1 je einer. Zeigt der Reiter weniger Zeilen, umso besser: dann nur zählen und weiter.

So räumst du auf:

1. **Doppelter Host (E8, FN2):** egal welcher bleibt, beide lesen dieselbe Config-Datei. Den zweiten rechtsklicken → **Remove**.
2. **Doppelter Guard (FN2):** beide nacheinander rechtsklicken → **Edit Strategy** (geht nur, solange sie aus sind) und das Feld **`EvalProfitTarget`** ansehen.
   - Den mit **0** behalten, den mit **3000** (oder einem anderen Wert ungleich 0) per **Remove** entfernen.
   - Haben beide 0: einen davon entfernen.
   - Haben beide nicht 0: bei einem `EvalProfitTarget` auf **0** setzen, OK, den anderen entfernen.
   - Sonst nichts an den Eigenschaften ändern, auch nicht die Telegram-Felder (die kommen aus der cfg).
3. **Erwartet am Ende:** 6 Zeilen, je Konto ein Host und ein Guard, alle aus.
   - **Fehlerfall:** du bist unsicher, welche Zeile zu welchem Konto gehört → Screenshot vom Reiter in den Hauptkanal, nichts entfernen.

## Schritt 4: Einschalten

Reihenfolge wie immer: **erst die drei Guards, dann die drei Hosts.** Im Reiter Strategies das Häkchen in der Spalte **Enabled** setzen.

1. `MaxRiskGuard` für E8, FN1, FN2 aktivieren.
   - **Erwartet:** Häkchen bleibt, Zeile wird grün oder gelb. Je Konto eine Telegram-Startmeldung aufs Handy.
2. `MaxBookHost` für E8, FN1, FN2 aktivieren.
   - **Erwartet:** Häkchen bleibt.
   - **Fehlerfall (für beide):** springt eine Instanz sofort wieder auf aus, Konto und Name notieren, **nicht ständig neu klicken**, im Hauptkanal **„springt aus“** plus Konto schreiben.

## Schritt 5: Workspace sichern

1. NT8 → **File → Workspaces → Save** (aktiver Workspace heißt `1`).
   - **Erwartet:** keine Rückfrage, oder ein kurzer Speichern-Hinweis.
   - Damit merkt sich NT8 den aufgeräumten Stand ohne die doppelten Instanzen.

## Schritt 6: Claude prüft

Im Hauptkanal **„eingeschaltet“** schreiben. Claude prüft per SSH:

- NT8-Log: genau 6× `Enabling NinjaScript strategy` (3 Guards, 3 Hosts), danach kein `Disabling`.
- Je Konto genau **ein** `HOST BEREIT` mit 5 Modulen und der richtigen Config-Prüfsumme (E8 `2f5241f9…`, FN1 `b7f49fc7…`, FN2 `54c46ffb…`), **kein** `TEMPLATE FALSCH`. Die Warnung „erste Bar endet 93200“ ist die bekannte Fehlwarnung.
- Je Guard eine `CONFIG`-Zeile mit `EvalProfitTarget=0`, den Limits aus der Tabelle oben, `Telegram=an`, `Size 1`.

## Schritt 7: Schluss

1. **RDP nur trennen (Fenster schließen), NICHT abmelden.**
2. Am Mo nach 22:00 Boxzeit im Hauptkanal **„Montag-Check“** schreiben. Claude schaut dann, ob die Beine ihre PARITY-Zeilen geschrieben haben und ob OpenDrive sein ATR20 bereit hat.

## Quellen

SSH-Lesung vom 22.11.2026: NT8-Logs 17. bis 22.11., NT8-Datenbank (Tabelle `Strategies`), Host- und Guard-Logs je Konto, `maxlab_riskguard.cfg`, Host-JSONs, Code-Prüfsummen Box gegen `engine/ninjascript`. Format wie [[Deploy-Abend 22.10.2026 (Anleitung)]], Regeln je Konto in [[Firm-Regeln je Konto]], Stand der Konten in [[Stand]].
