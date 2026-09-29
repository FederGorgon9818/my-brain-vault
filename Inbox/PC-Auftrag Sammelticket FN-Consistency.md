---
tags:
  - system/inbox
  - trading/risk
erstellt: 2026-09-29
quelle: Cloud-Session 2b0199f9
---
⬅️ [[Brain Dump]] · [[Firm-Regeln je Konto]]

# 📌 PC-Auftrag: Sammelticket FN-Consistency anlegen

> [!todo] Für die nächste PC-Session
> Max hat am 29.09. in der Cloud entschieden: alles zur FN-Consistency kommt in **ein Sammelticket**, **AP255 bleibt wie es ist**. Die Cloud kommt nicht an die Box (Tailscale), deshalb liegt das Ticket hier fertig bereit. Ablauf: anlegen, verlinken, Notiz dran, dann diese Notiz löschen und in der Daily Note die AP-Nummer vermerken.

## Befehle (Engine-Ordner, `PYTHONIOENCODING=utf-8`, PowerShell oder Git-Bash)

`ticket_tool.py new` pullt vorher selbst und pusht danach (Nummernkollision 03./06.09.). Die neue Nummer aus der Ausgabe statt `APNEU` einsetzen.

```
python ticket_tool.py new "FN-Consistency komplett: Kauf-Checkliste neues FN-Konto + Regel in allen Rechnungen" --board trading --prio orange --type task --hours 5 --who max --why "Die 40-%-Regel der FN-Challenge ist live abgesichert (AP205, Deckel 0,36 seit 24.09.). Beim Kauf eines neuen FN-Kontos muss der Deckel vor dem ersten Trade stehen, und Workbench-P(Pass), Buch-Rechnung und Tempo-Plan rechnen die Regel noch nicht so, wie sie live läuft (FN-Passquote 2 bis 6 pp zu hoch, Rechnung 29.09.)." --guide "Kauf neues FN-Konto: Regeln der Größe aus der Primärquelle in Firm-Regeln je Konto (Target, MLL, Lock +100, Kontraktlimit, 40-%-Regel, Flat 15:10 CT)" --guide "Kauf: maxlab_riskguard.cfg <konto>.dailyprofitcap=0.36 und dailyprofitcapmargin=0 (50k 900 $, 100k 1.800 $, 150k 2.880 $), dazu EvalProfitTarget, MaxTrailingDD, DailyLossLimit der Größe" --guide "Kauf: RiskGuard-Instanz mit Telegram-Werten aus maxlab_watchdog.json neu starten, Log prüfen: 'Deckel 36% x Target ... = ...'" --guide "Kauf: book_state.json + funded_finalize.py + inbox_tool.py --push-next, erst danach der erste Trade" --guide "Rechnung: Consistency als EINE Definition in cage_policy_lib (Live-Deckel 0,36 x Target), evaluate_v2 und Workbench-P(Pass) FN darüber, Workbench-Hinweis 'FN ohne 40-%-Regel, also zu hoch' raus" --guide "Rechnung: tempo_plan FN-Lane auf den Live-Deckel umstellen (rechnet heute die reine 40-%-Regel, für FN innerhalb 12 Monaten leicht zu pessimistisch)" --guide "Rechnung: Cloud-Rechnung 29.09. (Tagesebene) am PC auf Trade-Ebene bestätigen, funded_finalize neu, FN-Punkt in AP255 abhaken" --guide "Entscheidung Max: Auslöser 0,36 -> 0,40 x Target? Mathematiker 29.09.: +0,4 bis +1,4 pp in allen Regimen, liegt aber im Rauschen der Historie (Firm-Regeln je Konto, Rechnung 29.09.)" --guide "Vor dem ersten FN-Pass: beim FN-Support schriftlich klären, ob Deckel aus im Funded als Strategie-/Risikowechsel zählt (Futures-Verbotsliste 14298337 nennt es nicht, CFD-Artikel 8388896 erwartet same strategy)"
python ticket_tool.py link APNEU relates AP255
python ticket_tool.py link APNEU relates AP248
python ticket_tool.py link APNEU relates AP258
python ticket_tool.py note APNEU "Rechnung 29.09. (Cloud, Tagesebene, Quant-Team gegengelesen): FN 50k k1 gesamt 81,8 -> 80,0 % (IS, 90-%-CI des Deltas -3,7 bis -0,2), bis 12 Monate 66,5 -> 63,3 %, letzte 3 J x0,58 53,5 -> 47,8 %. Deckel schlaegt die reine Regel beim Tempo (50k: 0,7 Monate schneller bis funded, 150k k2 gleich). Basis duenn: 8 Tage ueber 900 $ in 10 Jahren. Details: Firm-Regeln je Konto, Abschnitt Rechnung 29.09.2026. Script und Ergebnis: Vault Anhänge/2026-09-29 FN-Consistency/. Pass-Tag (Deckel-Zeile beim Funded raus) bleibt in AP258."
```

## Was drinsteckt

- **Beim Kauf eines neuen FN-Kontos** (Größe laut AP248): Regeln prüfen, Deckel-Zeile in die RiskGuard-cfg, Instanz mit Telegram neu, Log-Check, Buch nachziehen, erst dann handeln.
- **In den Rechnungen:** Workbench-P(Pass) und Buch-Rechnung kennen die Regel nicht, der Tempo-Plan rechnet die reine 40-%-Regel statt des Live-Deckels. Zahlen und Befund: [[Firm-Regeln je Konto]], Abschnitt „Rechnung 29.09.2026".
- **Zwei Punkte aus dem Quant-Team:** Entscheidung Max, ob der Auslöser von 0,36 auf 0,40 × Target geht, und eine Support-Frage vor dem ersten FN-Pass (Deckel aus im Funded = Strategiewechsel?).
- **Nicht drin:** Pass-Tag (Deckel-Zeile beim Funded-Konto raus) steht schon in AP258.

## Dateien zur Rechnung

- `Anhänge/2026-09-29 FN-Consistency/fn_consistency_passquote.py`: am PC nach `engine/_scratch_fn_consistency/` kopieren, läuft mit `MAXLAB_ENGINE=<engine>`.
- `Anhänge/2026-09-29 FN-Consistency/fn_consistency_results.json`: Ergebnis der Cloud-Rechnung, `run2.log` als Tabelle.
- `qm_*.py` (Mathematiker: Kern-Check, Überschießen, 0,40 gegen 0,36) und `stat_*.py` (Statistiker: äußerer Bootstrap, Jackknife, Zeit bis funded). Die großen Bootstrap-Ausgaben sind nicht mitgenommen, sie lassen sich neu erzeugen.
