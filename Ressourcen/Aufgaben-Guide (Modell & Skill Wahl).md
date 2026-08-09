---
tags:
  - ressource/claude-code
  - ressource/tokens
erstellt: 2026-07-29
---
# 🧭 Aufgaben-Guide: Was mit welchem Modell

⬅️ [[_Ressourcen]] · verwandt: [[Modellwahl (Opus vs Sonnet vs Haiku)]], [[Claude Code Tools & Skills]], [[Agent-Architektur Token-Optimierung]]

> [!info] Zum Kopieren
> Das ist dein Spickzettel für „was gebe ich Claude, mit welchem Modell, und muss ich dafür clearen". Speicher dir das irgendwo (Notiz-App, Sticky, egal), damit du es beim Prompten immer griffbereit hast.

## Faustregel zuerst
- **Haiku 4.5:** mechanisch, viel Volumen, keine Abwägung nötig.
- **Sonnet 5:** dein Standard-Arbeitspferd. 90% aller Aufgaben laufen hierüber.
- **Opus/Fable:** nur wenn man wirklich abwägen muss (Architektur, Strategie-Entscheidung, fieser Bug, Paper-Bewertung).
- Nach jeder Opus/Fable-Aufgabe **aktiv zurück auf Sonnet** wechseln, sonst läuft die nächste Routine-Aufgabe unnötig teuer weiter.
- Umschalten in Claudian: `/model sonnet` · `/model opus` · `/model fable` · `/model haiku`.

---

## 🗂️ Vault & Alltag

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| Inbox/Brain Dump einsortieren | Haiku | | Nein, läuft eh am Session-Start mit |
| Daily Note schreiben/ergänzen | Haiku | | Nein |
| Notizen verschieben, umbenennen, verlinken, aufräumen | Haiku | obsidian-cli | Nein |
| Kurze Lookups, Zusammenfassungen, „wo steht X" | Haiku | | Nein |
| Briefing „was steht an" / „wo war ich stehengeblieben" | Sonnet (mehrere Notizen lesen) | | Ja, am besten frisch am Tagesanfang |
| Canvas / Base / Markdown-Spezialformat bauen | Sonnet | json-canvas · obsidian-bases · obsidian-markdown | Nein |

## 💻 Coden (allgemein & Token Tracker & Co.)

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| Normales Feature/Skript bauen | Sonnet | | Ja, ein Themenblock pro Session |
| Standard-Refactor, Aufräumen von Code | Sonnet | /simplify | Nein, wenn direkt im Anschluss |
| Code Review eines überschaubaren Diffs | Sonnet | /code-review | Nein |
| Kritischer Review (vor Live-Einsatz, Trading-Execution, Geld im Spiel) | Opus/Fable | /code-review (Effort high/max) | Ja |
| Security Review | Sonnet normal, Opus wenn Secrets/Execution betroffen | /security-review | Ja bei Opus-Fall |
| Änderung wirklich end-to-end testen | Sonnet | /verify | Nein |
| App starten und Ergebnis ansehen | Sonnet/Haiku | /run | Nein |
| Fieser Bug, subtile Ursache (Look-ahead, Fill-Logik, Race Conditions) | Opus/Fable | | Ja |

## 📈 Trading & Strategien

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| Neue Strategie in der Backtest-Engine implementieren (nach [[Strategie-Anatomie (Framework)]]) | Sonnet | | Ja |
| Strategie-Idee/Signal bewerten, Architektur-Entscheidung (Firmenwahl, Sizing-Logik, Portfolio-Mix) | Opus/Fable | | Ja, unbedingt frisch |
| Research-Paper (SSRN o.ä.) zu handelbarer Edge machen | Opus/Fable | paper-edge | Ja, immer frisch (Paper ist viel Content) |
| Discovery-Lauf/Sweep starten und auswerten | Sonnet | Background-Task + `summarize_results.py` (NIE volles Log lesen) | Nein zum Starten, ja wenn Auswertung ein eigener Block wird |
| Recherche zu Marktthema/Prop-Firma-Regeln | Sonnet, Haiku bei simplen Lookups | erst [[Research-Cache]] greppen, dann WebSearch/defuddle, Fund danach eintragen | Nein |
| Backtest-Ergebnis ins Logbuch schreiben | Haiku/Sonnet | | Nein |

## 🔁 Automatisierung

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| Wiederkehrenden Check einrichten (Auto-Check, Edge-Monitor) | Sonnet | schedule · loop · CronCreate | Ja |
| Bestehenden Cron/Loop anpassen | Sonnet | schedule · loop | Nein |

## 🌐 Web & Recherche

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| URL/Artikel lesen und zusammenfassen | Haiku/Sonnet | defuddle (nicht WebFetch, außer bei .md-URLs) | Nein |
| Breite Web-Recherche zu neuem Thema | Sonnet | WebSearch, danach Fund in [[Research-Cache]] eintragen | Ja, wenn eigener Block |

## ⏹️ Session-Ende

| Aufgabe | Modell | Skill/Tool | Session clearen? |
|---|---|---|---|
| Daily Note + neue Erkenntnisse einsortieren, Inbox aufräumen | Haiku | | War laufende Session, danach schließen |

---

## Wann wirklich clearen (Faustregel)
- Bei **Themenwechsel** (Trading → Coden → Vault-Pflege): neue Session.
- **Nach** einem abgeschlossenen Themenblock, nicht mittendrin. Sonst ist Cache/Kontext kalt und du zahlst doppelt.
- **Immer frisch** vor: Paper-Analyse, Architektur-/Strategie-Entscheidung, kritischem Review.
- **Nicht nötig** bei direkten Folgefragen im selben Thema oder kurzen Ergänzungen direkt danach.

## Subagenten (nur auf Zuruf)
- „Nimm einen Haiku-Scout dafür" für breite, mechanische Suche → `Explore`-Agent oder `Agent`-Tool mit `model: haiku`.
- Frontier (`fable`/`opus`) als Subagent nur für gezielte Zweitmeinungen (z.B. Code-Review-Gegencheck).
- Harness-Konvention: Subagenten starten nur, wenn Max explizit danach fragt, nicht automatisch.
