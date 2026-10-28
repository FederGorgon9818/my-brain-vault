---
name: steuer
description: >-
  Max' Steuer-Werkzeuge in vier Abläufen. abgleich: Revolut- oder Bank-CSV gegen Belegordner und
  EUeR-CSV, meldet Gewerbe-Abbuchungen ohne Beleg, Payouts ohne Eigenbeleg, Belege ohne Abbuchung.
  rueckblick: freiwillige Erklärungen der Ausbildungsjahre 2023 bis 2025 Jahr für Jahr vorbereiten
  (Fristen, Lohnsteuerbescheinigung, Werbungskosten, grobe Erstattung). bescheid: Einspruchsfrist
  rechnen, Bescheid gegen Erklärung abgleichen, Einspruch entwerfen. homeoffice: Homeoffice-Tage
  (GEWO und Gewerbe) als Nachweis führen und zählen. Nutzen bei /steuer, "Beleg-Abgleich",
  "Kontoauszug prüfen", "fehlen Belege", "Steuererklärung nachholen", "alte Jahre", "Lohnsteuer zurück",
  "Werbungskosten", "Bescheid ist da", "Einspruch", "Homeoffice-Tage", und beim Monats-Ticket Belege.
argument-hint: "[abgleich|rueckblick|bescheid|homeoffice] [Jahr oder Datei]"
---

# steuer

Eigene Fassung, Idee aus github.com/neubauerwilli/steuer-skill (MIT, gesichtet 28.10.2026), für Max'
Lage neu gebaut: Arbeitnehmer bei GEWO plus Nebengewerbe seit 01.10.2026, Zahlungen fürs Gewerbe über
Revolut, Erklärungen seit Ausbildungsbeginn 09/2023 nie abgegeben. Vault-Doku: [[Steuer-Werkzeuge]],
offene Jahre: [[Steuererklärungen 2023 bis 2025 nachholen]].

## Grundregeln

- **Keine Steuerberatung, nichts abschicken.** Max reicht in ELSTER selbst ein. Grenzfälle (Gewerbe,
  Umsatzsteuer, Verluste, Liebhaberei) gehen in [[Fragen an Steuerberater (Gründung)]], nicht raten.
- **Rechnen nur über die Skripte oder `python -c`**, nie im Kopf. Werte je Jahr stehen in
  `steuerlib.WERTE` (Stand 28.10.2026, vor Abgabe gegen bmf/elster prüfen). Neues Jahr: dort nachtragen.
- **Persönliche Daten nie in den Vault** (der wird gepusht). Ablage nur unter
  `C:\Users\maxlk\Documents\Steuer\` und `C:\Users\maxlk\Documents\Gewerbe\Belege\`.
- Skripte liegen in diesem Ordner, Aufruf mit `python "<skill-ordner>/<skript>.py"`. Selbsttest nach
  jeder Änderung: `python test_steuer.py`.

## Ablage

| Pfad | Inhalt |
| --- | --- |
| `Documents\Steuer\Kontoauszuege\` | Bank-Exporte als CSV (Revolut: App, Konto, Kontoauszug, Excel/CSV) |
| `Documents\Steuer\<jahr>\` | `profil.md`, `werbungskosten.csv/.md`, `homeoffice.csv`, `bescheid.md`, `einspruch.md`, Lohnsteuerbescheinigung |
| `Documents\Gewerbe\Belege\<jahr>\` | Belegordner + `EUeR-<jahr>.csv` (Regeln: [[Belegordner 2026]]), Abgleich-Berichte in `_Abgleich\` |

## Ablauf abgleich (beim Monats-Ticket am 28.)

1. Max legt den Revolut-Export nach `Documents\Steuer\Kontoauszuege\` (Zeitraum: seit letztem Abgleich).
2. `python abgleich.py <csv> [--von JJJJ-MM-TT] [--bis JJJJ-MM-TT] [--ohne-regel-ab 50]`. Standard:
   Zeitraum des Auszugs, alle EÜR-Dateien der berührten Jahre, Bericht nach
   `Belege\<jahr>\_Abgleich\abgleich_<bis>.md`. Revolut gibt es erst seit 09.08.2026, frühere Zahlungen
   liefen über ein anderes Konto: dann `--von 2026-08-09`. Überlappende Exporte darf man zusammen
   übergeben, echte Doppelkäufe (FN1/FN2 am selben Tag) bleiben trotzdem zwei.
3. Zuordnung in zwei Stufen: erst echte Anbieter (Name, Datum ±10 Tage, Betrag ±3 % oder 1 €),
   danach PayPal/Paddle/Stripe nur gegen die übrigen Belege und nur über den Betrag.
4. Bericht mit Max durchgehen, nach Abschnitt:
   - **Abbuchung ohne Beleg:** Rechnung im Postfach suchen (`webde_search`, Gmail), einsortieren nach
     [[Belegordner 2026]]. Privat? Dann ignorieren, nie in die EÜR.
   - **Eingang ohne Beleg:** Payout (Eigenbeleg, Zertifikat, Kurs am Gutschrifttag) oder Erstattung
     (Minderung gegen den Ursprungsbeleg). Die Spalte sagt, was es vermutlich ist.
   - **Nur über den Betrag zugeordnet:** immer im Dienst nachsehen, ob es wirklich dieser Kauf war.
   - **Zahlungsdienst unklar:** PayPal/Paddle/Stripe ohne Händler, Max fragt im Dienst nach.
   - **Betrag weicht ab (3 bis 25 %):** Gutschrift, Teilzahlung oder Kurs. Beleg prüfen, nichts passend
     rechnen. Mehr als 25 % daneben gibt kein Paar, dann stehen beide Seiten einzeln im Bericht.
   - **Beleg ohne Abbuchung:** anderes Konto oder noch nicht abgebucht. Zahlungsbeleg dazulegen.
   - **Jahreswechsel-Hinweis:** Abbuchung und Beleg in verschiedenen Jahren. In der EÜR zählt das
     Zahlungsdatum (§ 11 EStG), Ausnahme regelmäßige Zahlungen bis 10 Tage um Neujahr.
5. Neue Händler: Eintrag in `regeln.json` (`muster` für den Auszug, `euer` für die Spalte Anbieter).
   Spezielle Händler vor die Zahlungsdienste, und wer im Namen eines anderen steckt, davor (MFFU vor FFN).
   Zum Finden neuer Händler einmal mit `--ohne-regel-ab 50` laufen lassen.

Private Umsätze ohne Regel-Treffer stehen nicht im Bericht (außer mit `--ohne-regel-ab`).

## Ablauf rueckblick (Ausbildungsjahre)

1. `python fristen.py rueckblick --ab 2023 --bis 2025` zeigt Frist je Jahr. 2023 endet zuerst. Gilt nur
   ohne Abgabepflicht im Jahr (Max 28.10.2026: nur Kosten, keine Payouts, kein Broker). Je Jahr kurz
   gegen § 46 Abs. 2 EStG fragen: Nebeneinkommen über 410 €, Krankengeld oder anderer Lohnersatz über
   410 €, zweiter Arbeitgeber gleichzeitig (Steuerklasse VI), eingetragener Freibetrag. Trifft eins zu:
   stoppen, das ist keine freiwillige Erklärung mehr, Steuerberater.
2. Je Jahr `Documents\Steuer\<jahr>\profil.md`: Ausbildung ab wann, Betrieb, Berufsschule (Ort, km,
   Blockunterricht oder Tage, Verkehrsmittel), Arbeitstage am Betrieb, Arbeitsmittel, Kirchensteuer.
3. **Lohnsteuerbescheinigung zuerst:** Max holt sie in Mein ELSTER (Bescheinigungen, Belegabruf).
   Zeile 4 (Lohnsteuer), 5 (Soli), 6 (Kirchensteuer). Steht dort überall 0, bringt das Jahr kein Geld
   zurück: kurz sagen, Jahr zurückstellen.
4. `werbungskosten.csv` füllen (Kopf `art;beschreibung;menge;wert;anteil;beleg;mittel;kauf`, Arten
   im Skriptkopf), dann `python werbungskosten.py --jahr <jahr> --z17 <Z17> --z18 <Z18> --brutto <Z3>
   --lst <Z4> --soli <Z5> --kist <Z6> --rv <Z23a> --kv <Z25> --pv <Z26>`. Ergebnis `werbungskosten.md`
   mit grober Einordnung. Zeilen „nicht gerechnet" haben einen Hinweis, nie stehen lassen.
   - Fahrten zum Ausbildungsbetrieb: Entfernungspauschale (einfache Strecke, Arbeitstage), egal welches
     Verkehrsmittel. Jobticket oder Fahrgeld vom Betrieb (LSB Zeile 17/18) wird abgezogen.
   - Berufsschule: Auswärtstätigkeit, solange der Betrieb erste Tätigkeitsstätte ist. Spalte `mittel`
     ist Pflicht: pkw 0,30 €/km, moped 0,20 €/km (je hin und zurück), oepnv echte Ticketkosten,
     mitfahrer 0. Dazu `verpflegung` (14 € je Tag über 8 Stunden) und `erstattung` (was der Betrieb
     steuerfrei gezahlt hat). Von Max' Freundin (Steuerfachangestellte) gegenlesen lassen.
   - Laptop/PC/Software: 1 Jahr Nutzungsdauer, nur beruflicher Anteil. Anderes über 952 € brutto:
     Zeile `afa` mit Nutzungsdauer und Kaufdatum, monatsgenau.
5. Eval-Kosten 2024/2025 (ICT-Phase, nur Verluste) gehören nicht in Anlage N. Ob sich daraus ein
   Verlustvortrag machen lässt, ist eine Steuerberater-Frage (steht in der Liste), nicht selbst eintragen.
6. ELSTER: Einkommensteuererklärung des Jahres, Belegabruf übernehmen, Anlage N (Werbungskosten aus
   `werbungskosten.md`), Vorschau rechnen lassen, Max schickt selbst ab. Danach Bescheid-Ablauf.

## Ablauf bescheid

1. `python fristen.py bescheid --datum <Datum auf dem Bescheid>` (Bekanntgabe 4 Tage, vor 2025 3 Tage,
   Wochenende und Feiertage Bayern eingerechnet). Für den Kalender das ausgegebene sichere Datum
   nehmen (ohne Verschiebungen, liegt nie hinter der echten Frist). Als Wiedervorlage eintragen
   (`trading-data\engine\wiedervorlagen.json`, Board privat, Prio rot, `due` eine Woche vorher).
2. Bescheid (PDF/Foto) gegen Erklärung und `werbungskosten.md` legen: Lohn, Lohnsteuer, jede
   Werbungskosten-Zeile, Sonderausgaben, beim Gewerbe-Jahr der Verlust aus der EÜR. Erläuterungen lesen.
3. Je Abweichung: erklärt, angesetzt, Differenz, Begründung des Finanzamts in einfachen Worten, Urteil
   Fehler des Amts / strittig / berechtigt. Wirkung grob per Python, als Schätzung kennzeichnen.
4. Nur bei Fehler oder strittig: `einspruch.md` entwerfen (Steuernummer als Platzhalter, je Punkt was,
   warum, welcher Beleg). Max reicht über ELSTER ein. Ergebnis in `Documents\Steuer\<jahr>\bescheid.md`.

## Ablauf homeoffice

- Nachtragen: `python homeoffice.py fill --von 2026-07-01 --bis <heute> --wochentag <mo..fr> --seite gewo
  --ausser <Urlaub, Krank>` (Feiertage Bayern werden übersprungen). Einzeln: `add <datum> gewo|gewerbe`.
- Zählen: `python homeoffice.py summe --jahr 2026`. Pauschale 6 € je Kalendertag, höchstens 1.260 €,
  nur einmal je Tag.
- GEWO-Tage wirken nur über dem Pauschbetrag (1.230 €), bei kurzem Arbeitsweg meist nicht.
- Gewerbe-Tage an Wochenenden und Feiertagen zählen. Gewerbe-Tage an Werktagen sind vermutlich
  GEWO-Bürotage: die zeigt das Skript als strittig und rechnet sie **nicht** ein, bis der
  Steuerberater § 4 Abs. 5 Nr. 6c Satz 3 EStG bestätigt (Abschnitt 5 der Liste). Urlaubstag am Werktag:
  `--notiz urlaub` setzen, dann zählt er.
