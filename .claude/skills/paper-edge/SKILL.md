---
name: paper-edge
description: Liest ein Trading-/Quant-Research-Paper (SSRN o.ä., PDF oder Link) komplett und prüft ehrlich, ob sich daraus eine handelbare Edge für Max' Prop-Firm-Intraday-Index-Trading bauen lässt. Gibt eine strukturierte Bewertung plus konkrete Bauanleitung für QuantPad aus. Nutzen, wenn Max ein Research Paper, eine Strategie-Idee oder einen SSRN-Link zur Analyse gibt.
---

# Skill: Research Paper → handelbare Edge

Ziel: Aus einem Research Paper eine **ehrliche** Einschätzung machen, ob eine echte,
handelbare Edge drinsteckt, und wenn ja, wie Max sie in **QuantPad** nachbaut.
Kein Hype, keine geschönten Ergebnisse. Lieber „keine nutzbare Edge" sagen als etwas
schönreden.

## Schritt 0: Kontext laden
1. Lies **immer zuerst** [[Trading-Profil]] (`Bereiche/Trading-Profil.md`) für Max'
   Instrumente und harte Constraints.
2. Aktuell gilt: **Intraday only, keine Overnight-/Multi-Day-Holds, prop-firm-tauglich.**

## Schritt 1: Paper vollständig lesen
- PDF im Vault → mit Read lesen. SSRN-Link → Abstract/Volltext holen (defuddle/WebFetch).
- Wenn nur der Abstract verfügbar ist: klar sagen, dass die Bewertung vorläufig ist.

## Schritt 2: Strukturierte Analyse (immer dieses Format)

### 1. Kernaussage
Was behauptet das Paper? Welche Anomalie / welcher Effekt wird beschrieben (in 2-3 Sätzen)?

### 2. Markt & Instrument
Worauf wurde getestet? Lässt es sich auf **Index (NQ/QQQ/SPY/SPX/ES)** übertragen?
Wenn es nur auf Einzelaktien/Emerging Markets/Krypto funktioniert → Übertragbarkeit ehrlich einschätzen.

### 3. Haltedauer (KRITISCHER FILTER)
Welcher Zeithorizont? **Intraday, Tage, Wochen, Monate?**
> ⚠️ Wenn Overnight / Multi-Day nötig ist → **passt aktuell NICHT** zu Max' Prop-Firm-Phase.
> Trotzdem bewerten, aber klar als „erst mit Eigenkapital" markieren.

### 4. Signal-Logik (Entry)
Exakte Regeln, so konkret wie das Paper es hergibt. Welche Indikatoren, Schwellen, Bedingungen?

### 5. Exit-Logik
Stop, Target, Zeit-Exit? Falls das Paper nichts sagt → sinnvolle intraday-taugliche Defaults vorschlagen.

### 6. Reported Edge & Robustheit
- Kennzahlen: Return, Sharpe, Win Rate, Sample-Zeitraum, Anzahl Trades.
- **Ehrliche Robustheits-Prüfung:**
  - Out-of-sample getestet? Oder nur in-sample?
  - **Transaktionskosten & Slippage** berücksichtigt? (Bei Intraday killt das viele „Edges".)
  - **Data-Mining / Multiple Testing**? Wurde 1 von 100 Varianten herausgepickt?
  - Regime-Abhängigkeit? Funktioniert nur in bestimmten Marktphasen?
  - **Decay:** Wie alt ist das Paper? Edge seit Veröffentlichung wahrscheinlich abgenutzt?

### 7. Prop-Firm-Check
Gegen [[Trading-Profil]] prüfen: Intraday? Stop definierbar? Risk pro Trade begrenzbar?
Passt es zu Daily Loss Limit & Max Drawdown?

### 8. Verdict
**Klares Urteil:** Edge plausibel / fraglich / keine — und warum. Für Max' aktuelle Phase
tauglich ja/nein.

### 9. „Daraus könnte man folgendes machen" (Bauanleitung QuantPad)
- Konkrete Strategie-Spezifikation: Entry, Exit, Stop, Target, Instrument, Timeframe, Parameter.
- Als **Pseudocode / klare Regelliste**, damit es direkt in QuantPad umsetzbar ist.
- Was zuerst backtesten, welche Parameter variieren.
- **Robustheits-Plan in QuantPad:** Monte Carlo, Drawdown, Out-of-sample-Split, Kosten realistisch ansetzen.

### 10. Red Flags & Caveats
Ehrliche Liste der Risiken: Overfitting, Kapazität, Regime, Kostenempfindlichkeit, Decay.

## Schritt 3: Speichern
- Analyse als Notiz in `Ressourcen/` ablegen (z.B. `Ressourcen/Paper-Analysen/<Titel>.md`)
  mit Wikilinks zu [[Trading-Profil]] und [[Backtesting & MultiCharts]].
- Bei echtem Edge-Kandidaten: als To-Do für QuantPad-Backtest vermerken.

## Wichtiger Hinweis zum QuantPad-Format
Um Max **direkt einbaubaren Code** zu liefern, muss klar sein, welche Sprache/Format QuantPad
erwartet (PineScript, NinjaScript, Python o.ä.). Wenn unbekannt → einmal nachfragen oder ein
Beispiel geben lassen. Default-Output ist eine sprachneutrale Regelliste + Pseudocode.
