---
tags:
  - bereich/trading
  - bereich/business
erstellt: 2026-08-05
---
# 🧾 Steuer & Gewerbe (Prop-Payouts)

⬅️ [[Day Trading]] · gehört sachlich vor/parallel zu [[Funded-Phase]]

> [!info] Zweck
> Rechtlicher/steuerlicher Unterbau, damit der erste E8-Payout nicht auf ein administratives Loch trifft (Gewerbe, ELSTER, W-8BEN, Nebentätigkeit). Quelle: Opus-Review vom 05.08., von mir gegengeprüft. **Kein Steuerberater-Ersatz** — bei Gewerbeanmeldung/Fragebogen im Zweifel einmal kurz einen STB draufschauen lassen, gerade weil hier echtes Geld dranhängt.

## ✅ Mein Check: was stimmt, was ich korrigiert habe

**Stimmt, hab ich gegengeprüft (WebSearch 05.08.):**
- E8 = zwei Nicht-EU-Entities: **E8 Funding LLC** (Dallas, TX, USA) und **E8 Markets Ltd** (Saint Lucia, Reg.-Nr. 2025-00347). Kein EU-Sitz, keine Company-Registration möglich → deine Situation als Privatperson ist die einzig mögliche, kein Versäumnis.
- Damit ist die Steuerlogik im Text korrekt: **keine ZM** (nur EU-Empfänger), **keine USt-IdNr. nötig**, Leistungsort beim Empfänger im Drittland → **in Deutschland nicht steuerbar**. Das Kleinunternehmer-Zurückrudern am Ende des Texts ist schlüssig begründet (Sicherheitsnetz falls FA anders einordnet, kostet nix, bindet nicht).
- W-8BEN-Warnung (sonst 30% US-Quellensteuer) ist Standard-Praxis bei US-Zahlungen an Nicht-US-Personen, richtig.
- §13b Reverse-Charge bei ausländischen Services (VPS, TradingView) gilt auch als Kleinunternehmer — richtig, oft übersehen.
- 5-Jahres-Bindung gilt nur beim **Verzicht** auf §19, nicht bei der Wahl selbst — korrekt.

**⚠️ Eine Sache am Text ist an deiner Realität vorbei:**
Der Text unterstellt eine "Farm" aus 10 EAs auf vermutlich 10 einzelnen Prop-Konten und warnt entsprechend scharf vor Multi-Account-/Copy-Trading-Sperren. Dein echtes Setup ist anders: **ein E8-50k-Konto mit einem Portfolio aus 8-9 unkorrelierten Strategie-Beinen** ([[Strategie-Logbuch]] #042-#049), kein Konto-Schwarm. Das Multi-Account-Risiko ist für dich aktuell **kaum relevant** — wird aber wichtig, sobald du (wie in #042 angedeutet: "2 Versuche kumulativ") einen zweiten E8-Versuch oder ein zweites Konto parallel laufen lässt. Dann: ESPA nochmal gezielt nach Multi-Account/Copy-Trading lesen (Ticket unten trotzdem drin, aber niedrigere Prio als im Original-Text).

**Ungeprüft von mir, weil nur in deinem Account einsehbar:** ob "E8 Signature Futures" (dein Produkt, Tradovate) über dieselbe Entity läuft wie "E8 Markets" (Forex, MT5/TradeLocker) oder eine dritte. Rechtlich zieht dieselbe Nicht-EU-Logik so oder so, aber für den Eigenbeleg willst du wissen, wen genau du da bezahlst.

## 🎫 Tickets (was noch offen ist)

### 🔴 Diese Woche — lange Vorlaufzeit / harte Deadlines
- [ ] **ELSTER-Zertifikat beantragen** (elster.de → Benutzerkonto). Aktivierungscode kommt per Post, 1-2 Wochen — deshalb JETZT starten, unabhängig vom Eval-Fortschritt.
- [ ] **Nebentätigkeit bei HR anzeigen UND genehmigen lassen** (REX-Portal, Workflow „Nebentätigkeit beantragen", Akte Maximilian Kho): Formular vorbereitet, wirksam ab 06.08.2026 — noch signieren & abschicken. **Laut Arbeitsvertrag §8.2 ist das zustimmungspflichtig, nicht nur anzeigepflichtig** — echte Aufnahme der Nebentätigkeit (Gewerbe/Trading) erst nach schriftlicher Genehmigung starten, siehe Details unten.
- [ ] **W-8BEN-Status im E8-Payout-Bereich checken** (Plane/Rise/RiseWorks-Onboarding) — bevor der erste Payout ansteht, nicht danach.

### 🟠 Vor/mit echtem Live-Start
- [ ] **E8-Vertragsdokumente (ESPA/Terms) als PDF sichern** (Datum im Dateinamen), gezielt lesen: welche Entity führt dein Futures-Konto, Copy-Trading/Multi-Account-Klausel, Inaktivitäts-Regeln (Futures i.d.R. alle 7 Tage ein Trade nötig, sonst Deaktivierung).
- [ ] **Gewerbeanmeldung** (online, 10-65€). Tätigkeitsbeschreibung Richtung „Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten; Dienstleistungen für ausländische Auftraggeber; Softwareentwicklung" — deckt sich mit E8s eigener Selbstbeschreibung als SaaS-Simulationsplattform (Lizenzierung von Performance-Daten, nicht „Trading").
- [ ] **Belegordner anlegen** (2026/Challenges, /Infrastruktur, /Hardware, /Payouts) und rückwirkend sammeln: E8-Fee(s), VPS-Rechnungen, TradingView, Kurse — vorweggenommene Betriebsausgaben.

### 🟢 Kann parallel/danach laufen
- [x] **Revolut Personal** eröffnet (09.08.2026) — dient als Fallback-Konto (Ausweichoption falls ein Konto wegen der Prop-Payouts mal Fragen stellt/eingefroren wird). Nicht kündigen.
- [ ] **Revolut Business** beantragen (Verifizierung 3-10 Tage), Tätigkeit neutral beschreiben. **⏳ Warten bis Gewerbe angemeldet ist** — Business-Konto braucht i.d.R. einen KYB-Nachweis der Geschäftstätigkeit, klappt sauberer mit Gewerbeschein.
- [ ] **Steuer-Unterkonto:** feste Regel „X% jedes Payouts sofort weg" (Text nennt 42% als Faustwert für hohen Grenzsteuersatz bei zusätzlichem Einkommen neben Anstellung — grob, aber als Startwert ok bis der STB genauer rechnet).
- [ ] **Fragebogen zur steuerlichen Erfassung** über ELSTER, zeitnah nach Gewerbeanmeldung. **⏳ Warten bis Gewerbe angemeldet ist.** Kleinunternehmerregelung: JA ankreuzen, USt-IdNr. trotzdem mitbeantragen (kostet nix, brauchst du sofort falls je eine EU-Firma wie FTMO dazukommt).
- [ ] **Logging-Skript pro Konto** (Anbieter, Entity, Kosten, Kontostand, Trades) — als EÜR-Grundlage. Bau ich dir, wenn du willst, sag einfach Bescheid.

### 🔁 Laufend, sobald erste Payouts kommen
- [ ] Pro Payout: Eigenbeleg (fortlaufende Nummer) + Payout-Zertifikat + Kontoauszug + Screenshot, USD→EUR zum Gutschrift-Kurs, Zufluss = Tag der Gutschrift.
- [ ] Ende Jahr 1: Kleinunternehmer vs. Regelbesteuerung neu rechnen; bei Gewinn Richtung 24.500€ Gewerbesteuer + §7g checken.
- [ ] Ab ~30.000€ Jahresgewinn absehbar: Steuerberater mit Prop-Trading-Erfahrung holen (ist Betriebsausgabe).

### ⏸️ Niedrige Prio bis Konto-Anzahl wächst
- [ ] ESPA/Terms gezielt auf Multi-Account-/Haushalts-IP-Regeln lesen, sobald ein zweites E8-Konto oder ein zweiter Versuch parallel zum ersten läuft.


## 🏛️ Gewerbeanmeldung — Fakten für Ottenhofen (recherchiert 21.08.2026)

- **Zuständig ist NICHT Stadt/Landratsamt Erding**, sondern das **Gewerbeamt der Verwaltungsgemeinschaft Oberneuching** (Ottenhofen + Neuching bilden die VG). Das Landratsamt macht nur erlaubnispflichtige Gewerbe.
- Adresse: St.-Martin-Str. 9, 85467 Neuching · Tel. 08123 9326-60 · info@vg-oberneuching.de · Mo–Fr 8–12, Mi 14–18 Uhr.
- **Gemeindekennzahl Ottenhofen: 09177134** (Landkreis Erding = 09177).
- Formular: bundeseinheitliches **GewA 1** (das Erdinger PDF ist dasselbe Formular). **Beiblatt nur nötig** bei weiteren gesetzlichen Vertretern, Erlaubnispflicht, Handwerksrolle oder Aufenthaltstitel → für Max entfällt es.
- Abgabe in Textform reicht (§ 14 Abs. 4 GewO): unterschriebenes PDF + Ausweiskopie per Mail/Post, oder persönlich mit Ausweis.
- Tätigkeitsbeschreibung (final, deckungsgleich mit HR-Anzeige): *„Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten und zur Erstellung von Handelsstrategien; Bereitstellung der daraus gewonnenen Daten und damit verbundene Dienstleistungen für ausländische Auftraggeber; Softwareentwicklung und IT-Dienstleistungen"* — Schwerpunkt = erster Halbsatz. Bewusst ohne „Anlageberatung/Vermögensverwaltung/Handel für Dritte" (KWG/WpIG-Erlaubnis).
- Ankreuzen: Nebenerwerb ja · Sonstiges · keine Beschäftigten · Hauptniederlassung · Neugründung · Erlaubnis nein.

## 📝 HR-Anzeige Nebentätigkeit — Formulierung fürs REX-Portal (Stand 09.08.2026)

**Vertragslage (§8 Arbeitsvertrag, per Foto geprüft 09.08.2026):**
- **8.1** Grundpflicht: keine Nebentätigkeit, die Arbeitsleistung oder Firmeninteressen beeinträchtigt.
- **8.2/8.3** Jede Nebentätigkeit muss **vor Aufnahme schriftlich angezeigt werden UND bedarf grundsätzlich der Zustimmung** der Firma (Art, Ort, Dauer, zeitlicher Umfang). Ablehnung möglich bei erheblicher Interessenkollision, Verstoß gegen Schutzgesetze oder Beeinträchtigung der Arbeitskraft.
- **8.4** Einmal erteilte Zustimmung ist **jederzeit widerruflich**, wenn betriebliche Gründe entgegenstehen — dauerhaft im Hinterkopf behalten, kein einmaliger Haken.
- **8.5** Ausnahme von der Zustimmungspflicht gilt nur für **ehrenamtliche** Tätigkeiten (karitativ/gesellschaftlich/konfessionell/politisch) — greift hier **nicht**, da gewerblich.
- **Konsequenz:** Formular abschicken reicht nicht — erst nach dem „Genehmigt durch"-Signatur-Feld unten im Dokument (= tatsächliche schriftliche Zustimmung von HR) gilt die Nebentätigkeit als freigegeben. Gewerbeanmeldung/erste Geschäftstätigkeit realistisch erst danach starten.
- **Argumente für die Genehmigung** (falls nachgefragt wird): automatisiert, nur ca. 5-8 Std./Woche neben Vollzeitstelle, kein Wettbewerbsverhältnis zu GEWO Feinmechanik (Finanzmarkt-Software vs. Feinmechanik), keine Berührung mit Betriebsgeheimnissen.

Für den Workflow „Nebentätigkeit beantragen" (Akte Maximilian Kho, Pers-Nr. 3370, GEWO Feinmechanik GmbH & Co. KG, Abteilung IT, Position Junior Fachinformatiker). Formulierung bewusst **neutral und deckungsgleich mit der geplanten Gewerbeanmeldung** gehalten (siehe Ticket oben: „Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten; Dienstleistungen für ausländische Auftraggeber; Softwareentwicklung"), damit HR-Meldung und Gewerbeanmeldung später nicht widersprüchlich klingen.

**Feldwerte:**

| Feld | Eintrag |
|---|---|
| Wirksam ab | 06.08.2026 |
| Nebentätigkeit (Art) | Gewerbliche Nebentätigkeit — Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten; Dienstleistungen für ausländische Auftraggeber |
| 2. Nebentätigkeit (Art) | leer lassen |
| Beschäftigungsart | Selbstständig / gewerblich (keine Anstellung) |
| Arbeitgeber der Nebentätigkeit | entfällt — selbstständige Tätigkeit auf eigene Rechnung (Gewerbeanmeldung in Vorbereitung) |
| Umfang der Nebenbeschäftigung (wöchentlicher Zeitaufwand) | ca. 5–8 Std./Woche (Strategieentwicklung & Monitoring; die eigentliche Ausführung läuft automatisiert) |
| Nebentätigkeit Bestätigung | Toggle AN (Höchstarbeitszeit-/Ruhezeiten-Bestätigung — gilt laut Formulartext ohnehin nicht bei Selbstständigkeit, Haken schadet aber nicht) |
| Signatur | Maximilian Kho |

**Fertiger Brief (Vorschau, so wie es im Dokument zusammenläuft):**

> **Nebentätigkeitsvereinbarung**
>
> VN, NN: Maximilian Kho
> Pers-Nr.: 3370
> FK: Schwinghammer, Alexander, Unterreitmaier, Martin
> Abteilung: IT
> Position: Junior Fachinformatiker
>
> Haupttätigkeit bei
> GEWO Feinmechanik GmbH & Co. KG
> Bahnhofstraße 45
> 85457 Wörth/Hörlkofen
>
> 06.08.2026
>
> Ich, Maximilian Kho, plane ab dem **06.08.2026** die Aufnahme einer Nebenbeschäftigung. Hiermit informiere ich sie darüber und bitte gleichzeitig darum, mir diese folgende Nebenbeschäftigung schriftlich zu genehmigen:
>
> **Art der Nebentätigkeit:** Gewerbliche Nebentätigkeit — Entwicklung und Betrieb automatisierter Software zur Analyse von Finanzmarktdaten; Dienstleistungen für ausländische Auftraggeber
> **Beschäftigungsart:** Selbstständig / gewerblich, keine Anstellung
> **Arbeitgeber der Nebentätigkeit:** entfällt — selbstständige Tätigkeit auf eigene Rechnung (Gewerbeanmeldung in Vorbereitung)
> **Umfang der Nebenbeschäftigung (wöchentlicher Zeitaufwand):** ca. 5–8 Std./Woche (Ausführung erfolgt automatisiert)
>
> Hiermit versichere ich, dass durch die Nebentätigkeit die gesetzlich vorgeschriebenen täglichen und die sich daraus ergebenden wöchentliche Höchstarbeitszeit im Sinne von § 3 ArbZG nicht überschritten wird und auch gesetzlich vorgeschriebene Ruhezeiten (§ 5 ArbZG) eingehalten werden. Sollten sich Änderungen insbesondere bezüglich der Arbeitszeit ergeben, werde ich Sie darüber umgehend informieren. Die Vereinbarung aus dem Arbeitsvertrag, insbesondere des § Nebentätigkeit bestehen fort.
> *(Höchstarbeitszeit gilt nicht bei Selbstständigkeit.)*
>
> Mit freundlichen Grüßen
>
> Maximilian Kho
>
> Ottenhofen, den 06.08.2026
> Maximilian Kho

**Hinweis:** Falls das Portal nur EIN Freitextfeld „Nebentätigkeit (Art)" anbietet und die anderen drei Zeilen (Beschäftigungsart, Arbeitgeber, Umfang) nicht separat abfragt, einfach alle vier Zeilen mit den fetten Labels wie oben als einen Textblock reinkopieren — die Vorschau rechts im Portal zieht sich das dann ohnehin in die passenden Zeilen.
