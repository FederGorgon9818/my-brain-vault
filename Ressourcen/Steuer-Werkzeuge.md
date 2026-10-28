---
tags: [steuern, gewerbe, werkzeug]
created: 2026-10-28
---

# Steuer-Werkzeuge (Skill /steuer)

Eigener Steuer-Skill, gebaut am 28.10.2026. Vorlage war das öffentliche Paket
[neubauerwilli/steuer-skill](https://github.com/neubauerwilli/steuer-skill) (MIT, 11 Skills für
Arbeitnehmer DE/AT). Gesichtet und bewusst **nicht installiert**: es schließt Selbstständige aus,
sein Konto-Scan sortiert Claude/Anthropic als Werbungskosten ein (bei Max Betriebsausgabe), und 11
Skill-Beschreibungen kosten in jeder Session Kontext. Übernommen wurden nur die Ideen, die zu Max passen.

Code: `.claude/skills/steuer/` im Vault. Persönliche Daten nur in `C:\Users\maxlk\Documents\Steuer\`
und im [[Belegordner 2026]], nie im Vault.

## Die vier Abläufe

| Ablauf | Skript | Wofür |
| --- | --- | --- |
| abgleich | `abgleich.py` | Revolut-/Bank-CSV gegen `EUeR-<jahr>.csv`: Gewerbe-Abbuchung ohne Beleg, Payout ohne Eigenbeleg, PayPal ohne Händler, Betrag weicht ab, Beleg ohne Abbuchung, EÜR-Zeile ohne Datei. Private Umsätze bleiben draußen. Läuft beim Monats-Ticket am 28. mit. |
| rueckblick | `fristen.py rueckblick`, `werbungskosten.py` | Freiwillige Erklärungen der Ausbildungsjahre, siehe [[Steuererklärungen 2023 bis 2025 nachholen]] |
| bescheid | `fristen.py bescheid` | Einspruchsfrist (4 Tage ab 2025, Wochenende und Feiertage Bayern), Abgleich Bescheid gegen Erklärung, Einspruch-Entwurf |
| homeoffice | `homeoffice.py` | Homeoffice-Tage getrennt nach GEWO und Gewerbe als Nachweis, Pauschale je Kalendertag einmal |

Werte je Jahr (Pauschbetrag, Entfernungspauschale, Homeoffice, Grundfreibetrag) stehen zentral in
`steuerlib.py`, Stand 28.10.2026, vor jeder Abgabe gegen bmf/elster prüfen. Selbsttest:
`python test_steuer.py`.

## Abnahme (28.10.2026)

`verdict-auditor` fand in der ersten Fassung zwei stille Fehler im Abgleich (echte Doppelkäufe wie
FN1/FN2 am selben Tag fielen als Duplikat raus; PayPal-Zahlungen konnten fremde Belege über den
Betrag schnappen) und 13 kleinere (MFFU als FFN erkannt, „weicht ab" ohne Obergrenze, Schreibtisch
über 952 € voll angesetzt, Berufsschule fest mit Pkw-Satz, Jobticket nicht abgezogen, Gewerbe-Tage an
Bürotagen eingerechnet, Sonderausgaben doppelt, u. a.). Alle eingebaut, je Fall ein Testfall; jeder
der alten Fehler, testweise zurückgebaut, macht den Selbsttest rot. **Noch offen:** ein Lauf mit
einem echten Revolut-Export (Format ungeprüft), Gegenprobe der Treffer von Hand.

## Was der Skill nicht macht

- Nichts abschicken, nichts in ELSTER eintippen. Max reicht selbst ein.
- Keine Gewerbe-Steuerfragen entscheiden (USt, Einkunftsart, Verluste, Liebhaberei): die stehen in
  [[Fragen an Steuerberater (Gründung)]].
- Keine Erstattung versprechen. `werbungskosten.py` ordnet nur grob ein, die Zahl liefert die ELSTER-Vorschau.

## Verwandt

[[Belegordner 2026]] · [[Steuer & Gewerbe (Prop-Payouts)]] · [[Unternehmensgründung Entscheidung]] ·
[[Gründung Zeitplan]]
