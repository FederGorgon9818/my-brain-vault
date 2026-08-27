---
tags:
  - ressource/anleitung
  - trading/prop
  - e8
erstellt: 2026-08-23
status: erledigt
ticket: AP33
---
⬅️ [[Eval-Passing]] · [[Ticket-Epics]] · [[Research-Cache]] · [[Strategie-Logbuch]]

# 📧 AP33: E8 ESPA/Terms als PDF sichern + gezielt lesen

> [!info] Ausgangslage
> AP33 hatte zwei offene Fragen: (1) welche Entity führt das Futures-Konto? (2) Inaktivitäts-Regeln, weil das Konto seit dem Eval-Pass bewusst flat gehalten wird. Frage (2) war bereits über den Support-Chat (Laerte, 11.08.2026) geklärt und steht in [[Strategie-Logbuch]] #093: **keine Zeitgrenze für die Eval, nur eine Wochen-Inaktivitätsregel (Futures: mind. 1 Trade auf+zu pro Woche, ab 0,1 Lot genügt)**. Frage (1) war offen.

## Was gesichert wurde

- **[[Anhänge/E8_Terms_2026-08-23.pdf|E8_Terms_2026-08-23.pdf]]** — komplette "E8 Funding LLC Terms of Service" (Effective Date 11/03/2025), per Browser von `https://e8futures.com/e8-markets-terms-and-conditions` gezogen (das ist die Futures-Domain, gleicher Anbieter wie e8markets.com/Forex) und als PDF im Vault abgelegt (9 Seiten).
- Die Seite `e8markets.com` läuft inzwischen unter der Marke **„SimFi™"** (Rebranding, war im Research-Cache noch nicht vermerkt) — reiner Namens-/Marketing-Wechsel, keine inhaltliche Änderung an Produkt/Regeln erkennbar.

## Ergebnis: Entity (Frage 1, jetzt geklärt)

**E8 Funding LLC**, Sitz **Texas, USA** (Gerichtsstand explizit Dallas County, Texas — Terms §3.6, §15.1, §15.4). Das gilt laut Dokument für die **gesamte Plattform inkl. Futures-Produkt** (T&C ist unter der Futures-Domain e8futures.com genau dieselbe wie unter e8markets.com). Damit ist der alte Verdacht aus der 05.08.-Recherche (E8 Funding LLC vs. E8 Markets Ltd, Saint Lucia) aufgelöst: **für das Futures-Konto (Tradovate) gilt E8 Funding LLC**, nicht die Saint-Lucia-Entity. E8 Markets Ltd taucht in diesem Dokument gar nicht auf — vermutlich nur für ein anderes Produkt/Region relevant.

→ Für die Payout-Eigenbeleg-Führung: **Zahlungsempfänger/Vertragspartner = E8 Funding LLC, Texas.**

## Weitere gefundene Klauseln (Terms & Conditions, aus dem PDF)

- **Copy-Trading/Multi-Account:** kein explizites Copy-Trading-Verbot im Dokument selbst, aber §3.4 "One Account Per User" — nur 1 Plattform-Profil pro Person erlaubt, außer schriftlich von E8 autorisiert. Ergänzend im Help-Center-Artikel „Is verification required?" gefunden: **„Single User (E8X) Profile policy"** — alle Challenge-Käufe müssen über EIN registriertes Profil laufen, alle Konten müssen vom jeweiligen Inhaber selbst gehandelt werden; mehrere Profile unter verschiedenen E-Mails = Terms-Verstoß. Deckt sich mit der bereits archivierten Support-Antwort (Fábio, 11.08., [[E8-Support-Anfrage (Sizing-Split + News-Fenster)]]): zwei Eval-Konten unter demselben Profil, beide nur von Max gehandelt, zählt als "copying your own trades" und ist erlaubt.
- **Inaktivität:** im Terms-Dokument selbst nur als allgemeiner Kündigungsgrund genannt (§12.2d "Prolonged account inactivity"), keine konkrete Frist — die konkrete Zahl (1x/Woche für Futures) kommt weiterhin nur aus dem Support-Chat/#093, nicht aus einem offiziellen Dokument.
- **Payout-Bedingungen:** §5 (Proof of Eligibility, KYC vor Auszahlung, Auszahlung in USD/USDC/USDT/BTC/ETH, USD-Auszahlung per Wire/ACH über den Zahlungsdienstleister Aeropay, 7 Tage Bearbeitungszeit, keine Gewinngarantie/kein Erstattungsanspruch bei Disqualifikation).
- **Kein Geld-zurück:** §4.2 explizit — alle Gebühren sind in jedem Fall nicht erstattungsfähig, auch bei Disqualifikation wegen ESPA/Terms-Verstoß.

## ESPA selbst: NICHT als eigenständiges Dokument öffentlich auffindbar

Die ESPA ("Educational Simulation Participant Agreement") wird in den Terms mehrfach als eigenständiges, **vorrangiges** Dokument referenziert (§1.1, §14 — bei Widerspruch gewinnt die ESPA gegen die Terms). Trotz Suche in:
- Footer-Links von e8markets.com UND e8futures.com (nur Privacy Policy, Terms & Conditions, Cookies Policy, Affiliate Terms verlinkt — keine ESPA)
- Help Center Futures (helpfutures.e8markets.com), Volltextsuche nach "ESPA" und "Participant Agreement" → einziger Treffer ist der Artikel [„Is verification required?"](https://helpfutures.e8markets.com/en/articles/6463833-is-verification-required), der die ESPA nur erwähnt ("alle User müssen die neue ESPA lesen und unterschreiben"), aber selbst keinen Link/PDF dazu enthält
- direkte URL-Versuche (`/legal/espa`, `/educational-simulation-participant-agreement`) → 404
- Websuche → keine öffentlich indexierte Kopie

**Schluss:** die ESPA wird offenbar nur **inline beim Signup/Checkout im login-geschützten Bereich (e8x.e8markets.com)** angezeigt und dort per Klick akzeptiert — kein öffentlich verlinktes Dokument. Der Checkout-/Bestell-Link selbst war für mich nicht aufrufbar (von der Session als Kauf-/Formularseite geblockt, zu Recht — das ist eine Stelle, an der man aus Versehen einen echten Kauf antriggern könnte).

**Update 23.08.2026 (Max hat den Help-Artikel „Is verification required?" komplett selbst kopiert + das enthaltene Bild gesichert):** der Artikel bestätigt den genauen Mechanismus — Zitat: *"To sign ESPA, you need to access it with a password code that is automatically sent to your email."* Der Artikel selbst ist also **nur die Doku über den Zugriffsweg, nicht die ESPA selbst**. Der Artikeltext ist gute Zusatzdokumentation (KYC-Ablauf, Single-User-Policy, Aeropay-Telefonverifizierung), ersetzt aber nicht die eigentliche ESPA-PDF — die steckt hinter einem per E-Mail verschickten Einmal-Code.

## ESPA gefunden — Update 23.08.2026, AP33 abgeschlossen

Max hat die signierte ESPA aus seinem Postfach gezogen (DigiSigner-Mail von `externalplatforms@e8markets.com`, 28.07.2026) und als PDF geschickt → gesichert als **[[Anhänge/E8_ESPA_2026-08-23.pdf|E8_ESPA_2026-08-23.pdf]]** (10 Seiten inkl. DigiSigner-Audit-Trail). Das war exakt der Weg, den der ursprüngliche AP33-Guide vom 05.08. schon vermutet hatte ("Signup-Bestätigungsmail von E8, Ende Juli").

**Vertragsdetails aus der ESPA (offizieller, rechtlich bindender Text — sticht laut §14.1/§15 die allgemeinen Terms bei Widerspruch):**
- Vertragspartner: **E8 Funding LLC**, 4101 McEwen Road, Suite 205, Dallas, Texas 75244. Unterschrieben von Dylan Elchami (CEO) und Max (`max.kho@web.de`), beide am 28.07.2026.
- Rechtliche Einordnung: Plattform ist explizit als reine SaaS-Bildungssimulation positioniert (§1), **kein** Wertpapier/Investment/Future/Swap — bewusste Abgrenzung von SEC/CFTC-Regulierung (Howey-Test, CFTC Rule 4.13/4.5/4.41). Rewards sind rein diskretionär, kein Rechtsanspruch auch bei bestandener Eval (§3.2, §4.2).
- **⚠️ Inaktivität/Dormancy — WICHTIGER WIDERSPRUCH zur bisherigen Annahme:** §9.3 der ESPA sagt **30 aufeinanderfolgende Kalendertage ohne simulierten Trade** = "Dormant" → automatische Suspendierung möglich. Das ist eine **andere Zahl** als die bisher angenommene Wochenregel aus dem Support-Chat (Laerte, 11.08., [[Strategie-Logbuch]] #093: "mindestens 1 Trade pro Woche") und als die "Inaktivität nach 7 Tagen" aus dem Signature-Futures-Help-Artikel (Research-Cache Z. 86-ähnlich). Drei verschiedene Zahlen aus drei Quellen (7 Tage / 1x Woche / 30 Tage) — die ESPA ist die **rechtlich bindende Primärquelle mit Vorrang vor allen anderen**, aber Support-Mitarbeiter setzen in der Praxis evtl. strenger durch. **Empfehlung: bis zur Klärung weiter nach der strengsten Regel (1x/Woche) fahren** — kostet nichts, vermeidet aber jedes Risiko. Für die Buch-/Sizing-Rechnung (AP90/AP91-Split-Plan) ist das trotzdem eine gute Nachricht: der vertraglich bindende Puffer ist größer als angenommen (30 statt 7 Tage), falls die Wochenregel nur eine Kulanz-Auskunft war.
- Termination/Reset: E8 kann bei Verstoß jederzeit ohne Vorankündigung Trades löschen, Konto zurücksetzen, Rewards verweigern oder dauerhaft sperren (§10.4) — Entscheidungen sind laut §10.5 **final und nicht anfechtbar**, auch nicht per Schiedsverfahren.
- Datenrechte: alle Trading-/Verhaltensdaten gehen per unwiderruflicher, ewiger Lizenz an E8 (§4.1) — beim 100%-Payout-Tier sogar als Work-for-hire vollständig E8s Eigentum (§3.3).
- Vertraulichkeit: 5 Jahre Verschwiegenheitspflicht über Plattform-interne Prozesse (§6.2).

## Buch-Lücke / was noch fehlt

Kein Buch-Bezug — reine Vertrags-/Compliance-Recherche, kein Alpha-Ticket. **AP33 ist damit vollständig erledigt** (Terms + ESPA gesichert, Entity geklärt, Inaktivität geklärt — mit dem offenen Neben-Punkt der 7/Woche/30-Tage-Diskrepanz oben, die operativ aber keine Handlung erfordert, solange die strengste Regel eingehalten wird).
