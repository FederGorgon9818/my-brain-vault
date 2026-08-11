---
tags:
  - ressource/anleitung
  - trading/prop
  - e8
erstellt: 2026-08-11
status: beantwortet-beide-fragen-geklaert
ticket: AP77 (gelöst, aus tasks.json gelöscht)
---
⬅️ [[Eval-Passing]] · [[Ticket-Epics]] · [[Research-Cache]] · [[Strategie-Logbuch]]

# 📧 E8-Support-Anfrage: Sizing-Split zwischen zwei Evals

> [!warning] Warum das vor dem Kauf geklärt sein muss
> Der #076-Plan sind **zwei parallele 25k-Evals mit identischem Buch, aber unterschiedlichem frac** (0,10 / 0,80) → P(funded) 57,0% statt 48,4% auf einem Konto. E8s Copy-Trading-Regel verbietet laut Help-Center-Wortlaut aber explizit *copying trades between multiple E8 evaluation accounts*, jede Eval müsse unabhängig sein. Quelle nur über Suchmaschinen-Snippet erreichbar (Primärseite 403), **Konfidenz: Praktiker, nicht bestätigt**. Ohne Klarheit riskieren 2× ~255 $ plus Termination beider Konten.

## Kanal
Offizieller Support (Chat oder Ticket), **nicht** Forum/Discord/Community. Antwort als **Screenshot archivieren**, genau wie die VPS-Freigabe vom 27.07. (Support Mohamed).

## Text zum Rauskopieren

```
Hello E8 Team,

I have two questions about the rules for evaluation accounts, and I would
like to have the answers in writing before I purchase.

1) Sizing split across two evaluation accounts
I am running a fully automated system on NinjaTrader 8. I am considering
running two evaluation accounts in parallel with the SAME strategy logic,
but a DIFFERENT position size per account (for example 1 micro contract on
one account and a larger size on the other). The trades would therefore not
be identical 1:1 copies, they would differ in contract size.

Does this fall under your copy trading restriction between multiple E8
evaluation accounts, or is it permitted as long as the trades are not
copied 1:1 with identical sizing?

If it is not permitted, could you please confirm whether running the same
strategy on only ONE evaluation account at a time (sequentially, one attempt
after the other) is fine?

2) News trading restriction
Could you please confirm the exact restricted window around high impact news
events for funded accounts? I have seen two different values mentioned
(2 minutes before / 3 minutes after, and 5 minutes before / 5 minutes after).
Which one currently applies, and does the same window apply during the
evaluation phase as well?

Thank you very much for the written confirmation.

Best regards,
Max
```

## Was aus der Antwort folgt

| Antwort | Konsequenz |
|---|---|
| **erlaubt** | AP77 löschen, Kauf der zwei 25k-Konten freigeben, paralleler #076-Plan bleibt die bessere Wahl (57,0%) |
| **verboten** | #076-Parallelplan verwerfen, **nicht ersatzlos**: sequenziell zwei Versuche nacheinander auf einem Konto, kumulativ ≈73% (2× 48,4% unabhängig), 2× 100 $ auf 25k statt 2× 255 $, im schlechten Fall bis ~2,5 Monate. Kein Termination-Risiko, da immer nur ein Konto aktiv |

## ✅ Antwort erhalten (Fábio, E8 Markets Support-Chat, 11.08.2026)

**Erste Antwort (18:04):**
> 1 – Ja, Copy-Trading ist zwischen Ihren eigenen Konten erlaubt. Erlaubt: Kopieren zwischen Ihren eigenen Challenge-, Performance- oder persönlichen Konten mit beliebiger Software. Nicht erlaubt: Signaldienste oder "Team-Trading" (mehrere Nutzer führen dieselben Trades aus).
> Die Nachrichtenbeschränkung gilt nur für das E8-One-Programm. [Link auf `help.e8markets.com`, allgemeine/Forex-Seite]

War generisch formuliert (deckte das exakte Szenario "zwei GLEICHZEITIG aktive Evals, unterschiedliches Sizing" nicht explizit ab) und verlinkte für die News-Frage die falsche Programm-Domain (nicht Futures). Deshalb Nachfass-Frage gestellt, explizit für **E8 Signature FUTURES** und das **Parallel-Eval-Szenario**.

**Nachfass-Antwort (19:08):**
> Yes, if both challenge accounts will be only trade by you, it does count as copying your own trades.
> Regarding news trading, you can trade news with no restrictions in the Signature program. Therefore, we recommend that users avoid trading during high-impact news releases.
> [Link auf `helpfutures.e8markets.com/.../can-i-trade-news` — diesmal korrekte Futures-Domain]
> [Link auf `helpfutures.e8markets.com/.../e8-signature-futures` — vollständiges Regelwerk]

**Ergebnis, beide Fragen final geklärt:**
1. **Sizing-Split zwischen zwei gleichzeitig laufenden Evaluation-Accounts ist erlaubt**, solange Max selbst beide handelt (kein Signal-Dienst, kein Team-Trading). Der #076-Parallelplan (zwei 25k-Evals, frac 0,10/0,80, P(funded) 57,0%) ist damit **freigegeben**.
2. **Kein News-Trading-Verbot bei E8 Signature Futures** (weder Eval noch Funded) — nur eine Empfehlung, um Hochrisiko-News herum vorsichtig zu sein, keine harte Regel. Die vorher gefundenen Zahlen (5min/5min bzw. 2min/3min) waren entweder veraltet oder falsch zugeordnet — **es gibt keine feste Sperrzeit einzuhalten.**

AP77 damit gelöst und aus `tasks.json` gelöscht. Ergebnis dokumentiert in [[Strategie-Logbuch]] #085.

Nebenbefund News-Fenster: klärt den Widerspruch im [[Research-Cache]] (2min/3min vs. 5min/5min) und geht danach dort als bestätigter Claim rein.
