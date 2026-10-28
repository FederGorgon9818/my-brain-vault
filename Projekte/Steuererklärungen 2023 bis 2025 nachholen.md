---
tags:
  - projekt
  - steuer
erstellt: 2026-10-28
status: vorbereitet (Werkzeuge stehen, Daten von Max offen)
---
# Steuererklärungen 2023 bis 2025 nachholen

⬅️ [[Steuer-Werkzeuge]] · [[Fragen an Steuerberater (Gründung)]] · [[Gründung Zeitplan]]

**Stand 28.10.2026 (Max):** seit Ausbildungsbeginn 09/2023 nie eine Steuererklärung abgegeben.
2023 bis 2025 keine Payouts, kein eigener Broker, nur Eval-Kosten. Damit sind es **freiwillige
Erklärungen** (Antragsveranlagung), kein Versäumnis.

## Fristen (gerechnet mit `fristen.py rueckblick --ab 2023`)

| Jahr | Frist | Wiedervorlage im Auto-Check |
| --- | --- | --- |
| 2023 | Fr 31.12.2027 | 30.09.2027 (`steuer_2023_frist`) |
| 2024 | Di 02.01.2029 (31.12. ist ein Sonntag) | 30.09.2028 (`steuer_2024_frist`) |
| 2025 | Mo 31.12.2029 | 30.09.2029 (`steuer_2025_frist`) |

2026 läuft getrennt: mit Gewerbe (Anlage G, EÜR, Verlust gegen Gehalt), geplant März 2027 mit
Steuerberater oder Freundin.

## Lohnt es sich?

Hängt an einer Zahl je Jahr: **einbehaltene Lohnsteuer** auf der Lohnsteuerbescheinigung (Zeile 4,
dazu Soli und Kirchensteuer). Bei Ausbildungsvergütung nahe am Grundfreibetrag wird oft wenig oder
nichts einbehalten, typisch ist ein Abzug im Monat mit Weihnachtsgeld. Liegt das Einkommen nach
Werbungskosten und Sozialversicherung unter dem Grundfreibetrag, kommt das Einbehaltene komplett
zurück. `werbungskosten.py` ordnet das grob ein, die genaue Zahl zeigt die ELSTER-Vorschau.

Werbungskosten, die bei Azubis typisch zählen: Fahrten zum Ausbildungsbetrieb (Entfernungspauschale),
Fahrten zur Berufsschule (Reisekosten, hin und zurück), Laptop und Arbeitsmittel (beruflicher Anteil),
Fachbücher, Kontoführung 16 €. Erst über 1.230 € im Jahr wirken sie extra.

## Nächste Schritte

- [ ] Max: Lohnsteuerbescheinigungen 2023, 2024, 2025 in Mein ELSTER abrufen, nach `Documents\Steuer\<jahr>\`
- [ ] Max: Angaben je Jahr in `profil.md` (Betrieb, km, Berufsschule, Arbeitsmittel)
- [ ] Claude: je Jahr `werbungskosten.csv` füllen, `werbungskosten.py` mit den Zeilen der Bescheinigung
- [ ] Reihenfolge nach Ergebnis: Jahr mit Erstattung zuerst, 2023 hat die früheste Frist
- [ ] Max: in ELSTER abgeben, danach Ablauf `/steuer bescheid`

**Nicht hier:** die Eval-Kosten 2024/2025 aus der ICT-Phase. Ob daraus ein Verlust festgestellt werden
kann, ist Frage an den Steuerberater (Abschnitt 6 der Liste).
