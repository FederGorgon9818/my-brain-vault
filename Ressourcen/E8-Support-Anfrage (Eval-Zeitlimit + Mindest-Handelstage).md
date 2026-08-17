---
tags:
  - ressource/anleitung
  - trading/prop
  - e8
erstellt: 2026-08-11
status: beantwortet
ticket: AP90 (gelöst, aus tasks.json gelöscht)
---
⬅️ [[Eval-Passing]] · [[Ticket-Epics]] · [[Research-Cache]] · [[Strategie-Logbuch]]

# 📧 E8-Support-Anfrage: Eval-Zeitlimit + Mindest-Handelstage + Inaktivität

> [!warning] Warum das vor dem Kauf geklärt sein musste
> Der Betriebspunkt-Plan aus Logbuch #089 (2x E8 25k, Sizing-Split 0,10/0,30, rollend nachkaufen) braucht ein langsames Bein (median 45-85 Tage) UND ein schnelles Bein (Pass möglich in 6-8 Tagen). Gäbe es ein Zeitlimit, wäre das langsame Bein wertlos. Gäbe es Mindest-Handelstage, könnte das schnelle Bein formal nicht bestehen. Keins von beidem stand bestätigt im Research-Cache.

## Kanal
Offizieller Support-Chat, Antwort von Laerte (E8 Markets Support-Team), Screenshot archiviert wie bei AP77.

## Text zum Rauskopieren (gestellte Fragen)

```
Hello E8 Team,

I have questions about the rules for evaluation accounts on E8 Signature
Futures, and I would like to have the answers in writing before I purchase.

1) Time limit
Is there a time limit or expiration date for the evaluation phase? Or can
an evaluation run indefinitely until the profit target is hit?

2) Minimum trading days
Is there a minimum number of trading days required before the evaluation
can be passed, even if the profit target is reached earlier?

3) Inactivity rule
Is there a rule that closes the account after a certain number of days
without a trade during the evaluation phase? If yes, how many days?

Thank you very much for the written confirmation.

Best regards,
Max
```

## ✅ Antwort erhalten (Laerte, E8 Markets Support-Chat, 11.08.2026)

> Es gibt zwar keine maximale oder minimale Zeitbegrenzung, bitte beachten Sie jedoch unsere Inaktivitätsregel, um Ihr Konto aktiv zu halten:
> - **Futures:** Mindestens einmal pro Woche muss eine Position eröffnet und geschlossen werden.
> - **Forex & Krypto:** Mindestens ein Trade muss alle 60 Tage eröffnet und geschlossen werden.
>
> Hinweis: Dies gilt für alle Konten, auch für neu erworbene Konten ohne Handelshistorie. Ein Mindesthandelsvolumen von 0,1 Lot genügt, um diese Anforderung zu erfüllen.

## Ergebnis, alle drei Fragen final geklärt

1. **Kein Zeitlimit / Ablaufdatum** für die Evaluation — bestätigt "keine maximale ... Zeitbegrenzung". Das langsame Bein (45-85 Tage) ist damit nicht gefährdet.
2. **Keine Mindest-Handelstage** — "keine ... minimale Zeitbegrenzung" deckt das mit ab, ein Pass in 6-8 Tagen ist formal gültig. Das schnelle Bein ist damit nicht gefährdet.
3. **Inaktivitätsregel existiert, ist aber niedrigschwellig**: mindestens 1 Trade (auf + zu) pro Woche, ab 0,1 Lot genügt, gilt für Futures-Konten inkl. neu erworbener ohne Historie.

Der Betriebspunkt-Plan aus #089 (2x25k, Split 0,10/0,30) ist damit **vollständig freigegeben**, keine Restriktion, die den Split verschiebt.

**Offener Nebenpunkt (kein Blocker, aber zu prüfen):** die Wochen-Inaktivitätsregel setzt voraus, dass jedes aktive Bein im Schnitt mindestens 1x pro Woche einen Trade auslöst. Für die meisten Beine unkritisch, aber selektive/seltene Setups (z.B. ORB-Fade mit NR7-Filter) sollten kurz gegen die tatsächliche Trade-Frequenz geprüft werden, bevor beide Konten laufen.

AP90 damit gelöst und aus `tasks.json` gelöscht. AP91 (Kauf-Ticket) ist jetzt nur noch von AP53 (Buch-Entscheidung) blockiert.
