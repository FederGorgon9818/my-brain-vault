---
tags: [prozess, agents, hooks, workflow]
erstellt: 2026-09-21
status: aktiv
quelle-der-wahrheit: .claude/hooks/work_types.py
---

# Arbeits-Workflow: Auftrags-Typen und Pflichtketten

Der feste Ablauf, den **jede** Aufgabe durchläuft, damit nicht mehr Max ansagen muss,
welche Agents laufen sollen. Eingeführt 21.09.2026.

> [!info] Quelle der Wahrheit
> Die Typen und ihre Ketten stehen in `.claude/hooks/work_types.py`, nicht hier.
> Diese Notiz erklärt das **Warum** und den Ablauf. Neue Kette → zuerst dort,
> dann `kette.js` nachziehen (`test_chain.py` prüft, dass beide sich decken).

---

## Warum es das gibt

Max, 21.09.2026: *„Ich fühle mich, als müsste ich quasi immer sagen, dass alle Agents
eingeschaltet werden sollen und den genauen Prozess bei uns machen."*

Das Agent-Nutzungs-Audit über 14 Tage (121 Sessions) hat das bestätigt und beziffert:

| Agent | Aufrufe | Sessions mit Trigger, aber ohne Aufruf |
|---|---|---|
| quant-statistician / -mathematician | 39 / 36 | 6 / 6 |
| research-scout | 30 | 25 |
| engine-regression-tester | 19 | 15 |
| session-guard | 18 | 18 |
| verdict-auditor | 14 | 16 |
| design-guard | 8 | 22 |
| alpha-scout | 8 | 14 |
| **logbook-distiller** | **3** | **30** |

**Der entscheidende Befund:** der Unterschied lag nie am Agent, sondern an der
Durchsetzung. Das Quant-Team ist in den Workflows [[Der EINE Weg|ein-weg]] und
`konzept-weg` **fest verdrahtet** — und jede Session, die einen Workflow gefahren hat,
hatte im Audit **null Lücken**. Jede Session, die nur eine Text-Erinnerung bekam, hatte
welche.

Daraus die Konsequenz: nicht mehr Erinnerungen, sondern Ketten, die man nicht auslassen
kann, ohne es zu begründen.

---

## Die drei Stufen (was wirkt wie)

| Stufe | Mechanik | Wirkung |
|---|---|---|
| **Erinnerung** | Text im Kontext (`on_prompt.py`, `after_change.py`) | 9–56 % Befolgung → reicht nicht |
| **Hartes Gate** | `guard_*.py` lehnt die Aktion ab | greift zuverlässig |
| **Workflow** | Skript ruft die Agents selbst auf | greift zuverlässig, spart Denkarbeit |

Der Typ-Router nutzt alle drei, aber in der richtigen Reihenfolge: Workflow fährt die
Kette, Gate verhindert das Vorbeigehen, Erinnerung bleibt als zweite Spur.

---

## Der Ablauf, jedes Mal gleich

1. **Auftrag kommt rein.** `on_prompt.py` legt eine Quittung für die Session an und
   schlägt Typen vor (Regex — nur Vorschlag, keine Entscheidung).
2. **Typ festschreiben.**
   ```
   python .claude/hooks/receipt.py --sid <id> --type <typ>
   ```
   Erst damit steht die Pflichtkette fest. Die Kurz-ID steht in der Hook-Meldung, damit
   bei mehreren offenen Sessions die richtige Quittung getroffen wird.
3. **Kette fahren.** Workflow `kette` (Rechner parallel, Gegenleser danach **mit** deren
   Ergebnissen), bzw. `konzept-weg` / `ein-weg` für die beiden Typen mit eigenem Workflow.
4. **Gate lässt durch.** `guard_chain.py` gibt die schreibenden Aktionen erst frei, wenn
   die Kette gelaufen ist.
5. **Session endet erst sauber.** `on_stop.py` blockt bei offener Quittung.

---

## Die Typen

| Typ | Wofür | Pflichtkette |
|---|---|---|
| `konzept` | Konzept / grobe Edge zerlegen | Workflow `konzept-weg` |
| `hypothese` | Neue Hypothese vor dem Bank-Eintrag | Workflow `ein-weg` |
| `job` | Job in die Discovery-Queue | `pipeline-auditor` |
| `rechnen` | Rechnen / Ergebnis auswerten | `quant-mathematician` + `quant-statistician` |
| `urteil` | Stempel setzen (tot / gut / fertig) | `verdict-auditor` |
| `buch` | Buch / Portfolio ändern | Quant-Team + `strategy-auditor` |
| `deploy` | Deploy / Box-Sync / Live | `engine-regression-tester` |
| `ui` | Oberfläche (Hub / Lab / Report) | `design-guard` |
| `infra` | Box / Runner / Dienste | `box-ops` |
| `research` | Externe Recherche | `research-scout` |
| `logbuch` | Lehre ins [[Strategie-Logbuch]] | `logbook-distiller` |
| `meta` | Arbeit am Prozess selbst | `verdict-auditor` |
| `vault` | Notizen, Tickets, Doku | keine |
| `frage` | Reine Frage / Lookup | keine |

---

## Was hart blockt

**Aktions-Gates** greifen unabhängig von der Quittung, weil die Aktion ihren Typ selbst
verrät. Genau die drei schlechtesten Quoten aus dem Audit:

- `WebSearch` / `WebFetch` ohne `research-scout` → abgelehnt (Cache-Pflicht)
- Hub-/Lab-/Report-Datei oder `hot_reload.ps1` ohne `design-guard` → abgelehnt
- **Neuer** Logbuch-Eintrag ohne `logbook-distiller` → abgelehnt (Tippfehler-Korrektur nicht)
- `book_state*.json` ohne Quant-Team + `strategy-auditor` → abgelehnt

**Quittungs-Gate** greift bei Typen, die man nicht am Tool erkennt (`urteil`, `buch`,
`rechnen`): Typ gesetzt + Kette offen → schreibende Aktionen gesperrt. Frei bleiben immer
Daily Notes, `.claude/**`, `tasks.json` und das Scratchpad, damit der Prozess sich selbst
nicht aussperrt.

---

## Ausnahmen (Max' Entscheidung: blocken, aber Override möglich)

```
python .claude/hooks/receipt.py --sid <id> --skip <schritt> --why "<ein Satz>"
```

Ohne Grund keine Ausnahme — ein Ein-Wort-`--why` wird abgelehnt. Der Grund landet in der
Quittung und taucht damit im Retro auf. Das ist der Unterschied zur alten Text-Erinnerung:
Auslassen bleibt möglich, aber es hinterlässt eine Spur.

---

## Prüfen und pflegen

| Was | Wie |
|---|---|
| Selbsttest des Prozesses | `python .claude/scripts/test_chain.py` (aktuell 64 OK) |
| Rückblick: wo wurde ausgelassen? | `python .claude/scripts/agent_usage_audit.py --days 14` |
| Stand der eigenen Quittung | `python .claude/hooks/receipt.py --sid <id> --show` |
| Alle Typen + Ketten | `python .claude/hooks/receipt.py --types` |

**Neue Kette oder neuer Typ:** `.claude/hooks/work_types.py` ändern, dann `kette.js`
nachziehen, dann `test_chain.py` laufen lassen (er prüft, dass Hook und Workflow sich
decken — das Duplikat ist bewusst, aber abgesichert).

---

Verwandt: [[Hooks-Referenz]] · [[Strategie-Logbuch]] · [[Familien-Scout Agent]] · [[Agent-Architektur Token-Optimierung]]
