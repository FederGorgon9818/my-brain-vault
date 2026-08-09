---
tags:
  - ressource/paper
  - trading/framework
erstellt: 2026-07-14
---
# ⚖️ Simplex beats Komplex

⬅️ [[Strategie-Anatomie (Framework)]] · [[Strategie-Familien]] · [[Strategie-Logbuch]]

> [!important] Grundregel für JEDE Strategie
> **Einfach schlägt komplex.** Wir starten immer so einfach wie möglich. Komplexität ist erlaubt, aber jede zusätzliche Regel muss sich **out-of-sample verdienen** UND ein **Why** haben, sonst fliegt sie raus. Mehr Regeln = fragiler.

## Woher kommt das
- **Occam's Razor** (William of Ockham, ~1300): von zwei Erklärungen die einfachere bevorzugen.
- **Einstein (Nuance):** „So einfach wie möglich, aber nicht einfacher." → nicht dumm-simpel, sondern minimal-hinreichend.
- **Nassim Taleb:** Komplexität = Fragilität. „Wer eigenes Geld riskiert, wählt Einfachheit; Akademiker haben Anreize zur Verkomplizierung."
- **Robert Pardo:** *„Ein Modell mit genug freien Parametern passt auf JEDEN historischen Datensatz, sogar auf Zufallsrauschen. Der Fit sagt nichts über die Zukunft."*
- **Lopez de Prado:** Overfitting ist ein Komplexitäts-Problem; zu flexible Modelle fitten Rauschen und brechen bei Regime-Wechsel.

## Der Mechanismus
Jede zusätzliche Regel/Parameter = ein **Freiheitsgrad** = mehr Möglichkeiten, zufällig zu passen = **schlechter out-of-sample**. Ein Warnzeichen für Overfitting ist **extreme Empfindlichkeit gegenüber Parameter-Änderungen** (Messerschneide statt Plateau).

## Meine Meinung (fürs Projekt)
Voll zugestimmt, als **Default**. Beleg aus unseren eigenen Tests: die über-gefilterten Configs (NR7, Efficiency-Ratio, hoher Volumen-Filter) wurden **dünn im Sample und fragil**, während die einfachen Configs saubere, robuste **Plateaus** in der Sensitivität zeigten. Aber: Komplexität pauschal verbieten wäre falsch, der VIX-Filter z.B. hat sich OOS klar verdient (+7,4%→+10,4%). Regel: **einfach starten, komplex nur mit OOS-Beweis + Why.**

## Wie wir es implementieren (überall)
1. **In jedem Lab-Report:** Anatomie-Zeile „Komplexität" zählt die aktiven Regeln und bewertet sie (sehr einfach / mittel / komplex-fragil).
2. **Im Explorer (`refine.py`):** Filter wird nur behalten, wenn er die OOS-Kennzahl hebt; harter **Komplexitäts-Cap** (max. Regeln) + stochastische Restarts gegen Overfitting.
3. **Als stehende Regel** in der CLAUDE.md → gilt für jede künftige Strategie.

## Quellen
[Simple vs Complex (QuantifiedStrategies)](https://www.quantifiedstrategies.com/simple-vs-complex-trading-strategies/) · [Occam's Razor im Trading](https://www.newtraderu.com/2018/09/24/how-to-simplify-your-trading-with-occams-razor/) · [Overfitting & Parameter Selection](https://harbourfrontquant.substack.com/p/overfitting-and-parameter-selection) · [Taleb / Skin in the Game](https://www.fool.com/investing/2018/02/03/5-things-you-can-learn-about-investing-from-nassim.aspx)
