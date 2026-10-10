---
tags:
  - ressourcen/regel
  - claude/prozess
  - trading/friedhof
erstellt: 2026-10-05
status: aktiv (Regel Max, 22.09.2026)
---
# ⚰️ Todesurteil-Regel: „Tot“ ist ein Urteil mit Reichweite, kein Stempel

Herkunft: aus der CLAUDE.md ausgelagert am 05.10.2026 ([[CLAUDE.md Verschlankung]])

⬅️ [[Strategie-Logbuch]] · [[Hooks-Referenz]]

In der CLAUDE.md bleiben die Kategorien-Tabelle und die Sperre gegen `strukturell-tot`. Hier steht der ganze Rest: Anlass, Pflichtfelder, Durchsetzung, Vorbilder.

## Der Anlass

Max' Einwand: *„Es gibt eine Milliarde Arten, eine Edge zu ziehen, die wir nie getestet haben. Wie könnt ihr dann Sachen für tot erklären?“*

Der `verdict-auditor` hat nachgezählt: **82 Todesurteile im Logbuch, nur 24 mit Wiedervorlage-Bedingung, 46 ohne Bedingung UND ohne Reichweite.**

Klarster Fehlfall: **#163** trägt „endgültig tot“ im Titel, während im Körper steht, man bräuchte 27 bis 29 Jahre Historie. Das ist unentscheidbar, kein Ergebnis.

Dazu kamen am selben Tag drei kaputte Messwerkzeuge: das maband-RVOL-Gate maß eine Uhrzeit, dazu Entry- und Exit-Freitick in `qbt.py`. **Im Friedhof liegt nachweislich Zeug, das mit kaputtem Lineal erschlagen wurde.**

## Die vier Pflichtangaben

Jedes Todesurteil trägt sie, sonst ist es kein Urteil, sondern eine Notiz:

1. **Reichweite:** Rolle (Signal/Filter/Exit/Sizing), Frequenz, Markt, Käfig, Kostenstruktur. **„Tot“ ohne Objekt ist verboten.**
2. **Kategorie**, eine von vier:

| Kategorie | heißt wirklich | Reichweite |
|---|---|---|
| `strukturell-tot` | eine Rechnung verbietet die ganze Klasse | ganze Familie |
| `empirisch-nichts-gefunden` | N Varianten gemessen, keine trug (N nennen) | nur diese N |
| `echt-aber-zu-klein` | Effekt belegt, Ökonomie trägt ihn nicht | stirbt bei anderen Kosten/Käfig wieder auf |
| `unentscheidbar` | MDE/Feasibility schlägt die Kill-Schwelle | **zählt nicht als Friedhof** |

3. **Wiedervorlage:** Datum oder prüfbare Bedingung. „Nur auf ausdrückliche Ansage“ ist zulässig, aber **nur bei `strukturell-tot`**.
4. **Stempel:** Engine-Fingerprint, Datenstand, Kriterium/Betriebspunkt zum Urteilszeitpunkt (Lehre 159, seit 17.09. Text, seit 22.09. Pflicht).

## Die Sperre gegen den eigentlichen Anlass

Wer `strukturell-tot` beansprucht, **muss die Rechnung zitieren**, die die Klasse verbietet (Hüllkurve, Kostenhürde, Algebra). Ohne zitierte Rechnung ist es automatisch `empirisch-nichts-gefunden` mit N.

## Durchgesetzt, nicht erinnert

- **`guard_chain.py`** lehnt einen Logbuch-Eintrag ohne diese Felder ab. Geprüft wird nur der Urteilsblock (`Verdikt:`/`Urteil:`/`Fazit:`), nicht der Fließtext, Rückblicke und Zitate fremder Urteile lösen nichts aus.
- Der Hook erzwingt, dass die Felder **da** sind, nicht dass sie stimmen. Genau das hätte bei #163 gereicht.
- Fehlalarm-Override: `python .claude/hooks/mark.py urteil_ok`
- Selbsttest: `python .claude/scripts/test_urteil_gate.py` (7 Fälle, inkl. der Fehlalarm-Quellen).
- **Wiedervorlagen gehören zusätzlich in `auto_check.py`** (läuft alle 30 Min), nicht nur ins Logbuch. Ein Feld, das niemand zurückliest, ist die #125-Falle ein zweites Mal. Stand: seit 03.10.2026 laufen die Wiedervorlagen über `engine/wiedervorlagen.json` (AP247, Auto-Check liest sie).

### Zwei Fälle, bei denen die Bedingung schon eingetreten war und es niemand merkte

- **#164:** Blocker „kein GC/CL im Bestand“. Einen Tag später brachte #165 die Daten.
- **#139:** Bedingung „mehrere Kontrakte je Bein“, seit 21.09. erfüllt.

## Die Gegenrichtung

Ein Friedhof, in dem alles „vielleicht doch“ ist, ist genauso wertlos wie einer, der zu früh schließt. Wo ein „tot“ sauber trägt, gehört das ausdrücklich hingeschrieben.

Vorbilder im Logbuch:
- **#133** (CVD-Divergenz): zwei unabhängige Messungen plus Strukturbeweis plus benannte Reaktivierungsbedingung.
- **#067/#068** (ORB-Breakout): strukturell über 2.685 Tage.
- **#136** und **#165**: beide mit expliziter „Nicht tot:“-Liste.

Weiter: [[Strategie-Logbuch]], [[Hooks-Referenz]], [[Social Media & Wissensprodukt]] (der Friedhof als Alleinstellungsmerkmal, siehe [[Großes Ziel]]).
