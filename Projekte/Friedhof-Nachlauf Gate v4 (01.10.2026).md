---
tags: [projekt, trading, friedhof, gate-v4]
date: 2026-10-01
status: fertig (Urteile #179), Next-Week-Entscheidung am Wochenende
---

# Friedhof-Nachlauf Gate v4 (01.10.2026)

Volle Tabelle zu [[Strategie-Logbuch]] #179. Auftrag Max 01.10. (AP257 abgenommen). Vorgänger: #176 (Gate v2), [[Friedhof-Analyse (17.09.2026)]], [[Latte-Audit (25.09.2026)]].

**Kurz:** 240 Karten, 188 verschieden gemessen, **6 DURCH** (Erwartung unter Null 1,5 bis 5), alle 6 auf Max' Entscheid im Next-Week-Buch (Ticket AP295). Keine belastbare neue Edge. Echte Buch-Beine bringen als Neuzugang dSR 0,2 bis 0,3, die 6 DURCH 0,002 bis 0,065.

**Methode:** Prämisse (BASE, IS) → Stern-Grid ±25 % je Achse → Walk-Forward 2 J/1 J mit Neuauswahl → Gate v4 gegen das Next-Week-Buch (4 Beine). Lese-Regeln vorab vom Quant-Team festgelegt. Rechnung auf der Box, Daten bis Anfang August 2026, Engine 9cc1bcff.

**Spalten:** v4-Stufe = erste blockierende Stufe. dSR = Buch-Sharpe roh mit minus ohne. t_α = eigener Ertrag gegen das Next-Buch (Residual-Alpha). Jahre = positive / zählende WF-Testjahre. Buch-Lücke = was fehlt, damit es ins Buch kommt.

## Übersicht Familie × Kategorie

| Familie | DURCH | unentscheidbar | echt-aber-zu-klein | kein Tod | empirisch-nichts-gefunden | Dublette | nicht gemessen | gesamt |
|---|---|---|---|---|---|---|---|---|
| Trend Following | 5 | 25 | 0 | 16 | 79 | 9 | 16 | 150 |
| Mean Reversion | 0 | 5 | 0 | 0 | 11 | 7 | 5 | 28 |
| Intraday Bias | 1 | 8 | 0 | 4 | 19 | 4 | 4 | 40 |
| Swing | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 4 |
| Relative Value | 0 | 3 | 0 | 0 | 12 | 2 | 1 | 18 |

**Buch-Beine aus der v4-Abnahme** (übernommen, nicht neu gerechnet): NQ_Momentum_d260818 (Trend Following) DURCH dSR +0,20 · NQ_LastHour_v3 (Intraday Bias) DURCH dSR +0,31 · NQ_Asia-Dir-USopen_d260820 (Intraday Bias) Buch-Stufe, dSR +0,20, Passquote −5,2 pp.

## Trend Following (150)

| Kandidat | Teil | Modus | v4-Stufe | Kategorie | dSR | t_α | Jahre | Buch-Lücke / Grund |
|---|---|---|---|---|---|---|---|---|
| LD-01_NQ·regime_profile=vix_abs_max16,tm_stop_mult=0.5 | 1 | tsmom | DURCH | DURCH | +0.065 | +1.67 | 7/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart knapp; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| AC-06d Leg-Invalidierung als Stop (tm_stop_mode=leg) auf AC-06-Entry,  | c-Fibonacci Wege-Karte | maband | DURCH | DURCH | +0.034 | +1.19 | 7/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart Rauschverdacht; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| gen_maband_crossover_wide_tfm_ES·crossover_pair=20_50,mb_thr=1,tm_rvol | 1 | maband | DURCH | DURCH | +0.021 | +0.95 | 8/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart Rauschverdacht; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| FH_NQ_VWAP-Pullback_v8_BE05o02 | 1 | vwap_pullback | DURCH | DURCH | +0.018 | +1.30 | 7/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart Rauschverdacht; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| REFINE_ORB_2_close | 1 | orb | DURCH | DURCH | +0.002 | +0.57 | 8/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart Rauschverdacht; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| gen_maband_crossover_wide_atr_tfm_ES·crossover_pair=50_150,mb_thr=1,tm ⭐ | 1 | maband | Praemisse | unentscheidbar | +0.004 | +0.50 | 5/9 | Praemisse n 35 < 60 (Power) |
| SCALP_NQ_t0.5_hEOD ORB-Scalp enges Ziel (ehem. Bein 9), ohne Nacht-Bed | c-Overnight-Bias ORB Wege-Karte | orb | Praemisse | unentscheidbar | +0.003 | +0.34 | 2/9 | Praemisse n 34 < 60 (Power) |
| HF01_TAKT_NQ·takt=max2,signal=b5_f6_s20_thr0.60,risk_exit=atr0.45_rr1. | 1 | maband | Buch | unentscheidbar | -0.017 | +1.22 | 8/9 | ·dSR· < 1 SE (dSR -0.017, SE 0.139) gegen das Next-Buch |
| AC-02_NQ·mb_thr=1.2,mb_fast=6,mb_slow=26,tm_stop_mult=1 | 1 | maband | Buch | unentscheidbar | -0.018 | +0.21 | 7/9 | ·dSR· < 1 SE (dSR -0.0182, SE 0.0693) gegen das Next-Buch |
| gen_tsmom_ema_ladder_mom_c2_hf_NQ·tm_ema_confirm=110,tm_rvol_min=None, | 1 | tsmom | Buch | unentscheidbar | -0.020 | +0.86 | 7/9 | ·dSR· < 1 SE (dSR -0.0199, SE 0.0944) gegen das Next-Buch |
| AC-06b_NQ·mb_thr=0.15,mb_confirm=1,mb_slow=50,tm_stop_mult=0.8 | 1 | maband | Praemisse | unentscheidbar | -0.022 | +0.23 | 8/9 | Praemisse n 54 < 60 (Power) |
| AC-06d_NQ·stop_profile=atrRms_session1.0,tm_target_r=1.5 | 1 | maband | Buch | unentscheidbar | -0.028 | +0.98 | 7/9 | ·dSR· < 1 SE (dSR -0.0283, SE 0.1331) gegen das Next-Buch |
| FH_NQ_VWAP-Pullback_v8 | 1 | vwap_pullback | Buch | unentscheidbar | -0.031 | +0.94 | 7/9 | ·dSR· < 1 SE (dSR -0.0313, SE 0.1269) gegen das Next-Buch |
| maband_dist_NQ·mb_fast=12,mb_slow=26,mb_thr=0.5 | 1 | maband | Buch | unentscheidbar | -0.041 | +0.72 | 7/9 | ·dSR· < 1 SE (dSR -0.0409, SE 0.1261) gegen das Next-Buch |
| vt01_NQ·vol_gate=sq0.7,tm_dir=short_only,stop_profile=range0.5 | 1 | maband | Buch | unentscheidbar | -0.051 | +1.28 | 7/9 | ·dSR· < 1 SE (dSR -0.0511, SE 0.155) gegen das Next-Buch |
| AV-12_NQ·mb_slow=26,mb_fast=20,mb_bar_min=5 | 1 | maband | Buch | unentscheidbar | -0.057 | +0.61 | 8/9 | ·dSR· < 1 SE (dSR -0.0574, SE 0.1413) gegen das Next-Buch |
| ONORB-W24a Nacht-Richtung als Tor (tm_on_dir=agree) | c-Overnight-Bias ORB Wege-Karte | tsmom | Buch | unentscheidbar | -0.060 | +0.89 | 9/9 | ·dSR· < 1 SE (dSR -0.0605, SE 0.1486) gegen das Next-Buch |
| gen_tsmom_combo_mom_hf_NQ·tm_ema_confirm=None,tm_rvol_min=None,tm_delt | 1 | tsmom | Buch | unentscheidbar | -0.064 | +0.74 | 8/9 | ·dSR· < 1 SE (dSR -0.0638, SE 0.1046) gegen das Next-Buch |
| FH_NQ_VOLBRK_i2 | 2 | i2 | Vor-Gates | unentscheidbar | -0.065 | +0.24 | 6/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| AC-06 Kreuzungswinkel (mb_kind=slope) | c-VWAP-Offensive | maband | Buch | unentscheidbar | -0.086 | +0.60 | 8/9 | ·dSR· < 1 SE (dSR -0.0862, SE 0.1493) gegen das Next-Buch |
| NQ_VWAP-Pullback_hf·vwap_dist_min_atr=2,vwap_max_trades_day=8,vwap_min | 1 | vwap_pullback | Buch | unentscheidbar | -0.095 | +0.54 | 7/9 | ·dSR· < 1 SE (dSR -0.0949, SE 0.1374) gegen das Next-Buch |
| AW-15b_NQ·mb_vwap_k=2,confirm=delta0.15,stop_profile=range0.5,exit_pro | 1 | maband | Buch | unentscheidbar | -0.120 | +0.40 | 5/9 | ·dSR· < 1 SE (dSR -0.1196, SE 0.1443) gegen das Next-Buch |
| AC-06c Zieldistanz fest gegen atmend (bester atmender Arm) | c-VWAP-Offensive | maband | Buch | unentscheidbar | -0.129 | +0.36 | 8/9 | ·dSR· < 1 SE (dSR -0.1288, SE 0.1538) gegen das Next-Buch |
| AW-15b Continuation ab Ueberdehnung (ATR-normiert, Rerun) | c-VWAP-Offensive | maband | Buch | unentscheidbar | -0.154 | +0.08 | 8/9 | ·dSR· < 1 SE (dSR -0.1545, SE 0.1605) gegen das Next-Buch |
| FH_NQ_Gap-continuation | 1-gap | gap | Vor-Gates | unentscheidbar | -0.323 | -1.30 | 6/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| ADX-W24 ES-ADX-Rang als Fremdmarkt-Gate auf NQ-Momentum | c-ADX Wege-Karte | tsmom | Vor-Gates | unentscheidbar | -0.336 | -1.62 | 6/8 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| TS-05_NQ·tm_base=open,tm_sig_len=60,tm_thr=0.002,tm_stop_mult=0.8 | 1 | tsmom | Vor-Gates | unentscheidbar | -0.463 | -0.46 | 8/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| gen_maband_combo_channel_tfm_NQ·tm_ema_confirm=100,tm_rvol_min=1.2,tm_ | 1 | maband | Walk-Forward | unentscheidbar | -0.524 | -1.22 | 5/9 | WF OOS > 0, nur Mehrheit verfehlt (schwach) |
| ONORB-W31a Nacht-Volumen als Tor (on_rvol_min 1,2) | c-Overnight-Bias ORB Wege-Karte | tsmom | Vor-Gates | unentscheidbar | -0.532 | -1.33 | 6/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| REFINEAPEX_Momentum_3 | 1 | ts_reversal | Vor-Gates | unentscheidbar | -0.609 | -1.93 | 7/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| TE-02_NQ·rev_stop_mult=0.35,rev_thr=0.003,rev_er_min=0.3 | 1 | ts_reversal | Buch | kein Tod | -0.142 | -0.92 | 9/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.797): Variante des Beins, als Ersatz nicht besser |
| gen_maband_crossover_wide_tfm_NQ·crossover_pair=20_50,mb_thr=1,tm_rvol | 1 | maband | Buch | kein Tod | -0.143 | +0.70 | 9/9 | Klon von NQ_OpenDrive_maband2050 (r 0.752): Variante des Beins, als Ersatz nicht besser |
| TE-02_NQ_v2·rev_stop_mult=0.3,rev_thr=0.0035,rev_er_min=0.3 | 1 | ts_reversal | Buch | kein Tod | -0.143 | -0.69 | 9/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.737): Variante des Beins, als Ersatz nicht besser |
| TE-02_NQ_v2·rev_stop_mult=0.3,rev_thr=0.0025,rev_er_min=0.3 | 1 | ts_reversal | Buch | kein Tod | -0.157 | -0.85 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.76): Variante des Beins, als Ersatz nicht besser |
| ON01_CASHOPEN_NQ·nacht=on_min0.25,fenster=w15_thr0.30,risk_exit=rng0.3 | 1 | tsmom | Buch | kein Tod | -0.202 | -0.94 | 9/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.73): Variante des Beins, als Ersatz nicht besser |
| fa01b_NQ·pbentry_profile=e_3min,pbexit_profile=x_aus,tm_thr=0.003 | 1 | tsmom | Buch | kein Tod | -0.204 | -2.08 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.922): Variante des Beins, als Ersatz nicht besser |
| tsmom_erret_NQ·tm_thr=0.0008,tm_stop_mult=0.5,tm_sig_len=15 | 1 | tsmom | Buch | kein Tod | -0.289 | -1.63 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.822): Variante des Beins, als Ersatz nicht besser |
| TA-02_NQ·tm_er_min=0,confirm=delta0.15,tm_stop_mult=0.3 | 1 | tsmom | Buch | kein Tod | -0.355 | -2.02 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.723): Variante des Beins, als Ersatz nicht besser |
| VOLB-NULL-RVOL_NQ·tm_rvol_min=None,tm_sigma_q_min=None,tm_sig_len=15,t | 1 | tsmom | Buch | kein Tod | -0.377 | -2.02 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.765): Variante des Beins, als Ersatz nicht besser |
| TK-01_NQ·rev_signal_min=15,rev_thr=0.003,rev_stop_mult=0.3,rev_exit=eo | 1 | ts_reversal | Buch | kein Tod | -0.379 | -2.23 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.769): Variante des Beins, als Ersatz nicht besser |
| NIGHT_Momentum_2 | 1 | ts_reversal | Buch | kein Tod | -0.393 | -2.02 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.761): Variante des Beins, als Ersatz nicht besser |
| AW-13 VWAP-Seite als Richtungsfilter fuers Momentum-Bein | c-VWAP-Offensive | tsmom | Buch | kein Tod | -0.400 | -2.54 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.784): Variante des Beins, als Ersatz nicht besser |
| MOMSEL_NQ_er0.3_s0.75 | 1 | ts_reversal | Buch | kein Tod | -0.437 | -1.81 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.71): Variante des Beins, als Ersatz nicht besser |
| TE-15_NQ_v2·PREMISE0 | 1 | tsmom | Buch | kein Tod | -0.445 | -2.49 | 8/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.799): Variante des Beins, als Ersatz nicht besser |
| NQ_Momentum_hf·rev_thr=0.0015,rev_signal_min=15,rev_stop_mult=0.3,exit | 1 | ts_reversal | Buch | kein Tod | -0.475 | -2.32 | 6/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.735): Variante des Beins, als Ersatz nicht besser |
| tsmom_zscore_NQ·tm_thr=1.5,tm_stop_mult=0.3,tm_sig_len=15 | 1 | tsmom | Buch | kein Tod | -0.547 | -2.50 | 7/9 | Klon von NQ_Momentum_PB3_fa01b (r 0.711): Variante des Beins, als Ersatz nicht besser |
| ORB_nr7_close ⭐ | 1 | orb | Vor-Gates | empirisch-nichts-gefunden | +0.026 | +1.22 | 6/8 | Vor-Gates fallen (IS/OOS-leer, cost2t, n, sharpe_t), N = 1 (WF-deploy-Config) |
| SES-W16a Lunch-Linearitaet (er_ret) traegt in den Nachmittag | c-Session Momentum Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | +0.006 | +0.79 | 4/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| gen_maband_combo_vwap_NQ_exits_09221722·exit_trail_profile=time60+be1. | 1 | maband | Vor-Gates | empirisch-nichts-gefunden | -0.008 | +1.37 | 8/9 | Vor-Gates fallen (IS), N = 1 (WF-deploy-Config) |
| ORB_maxwin_close | 1 | orb | Praemisse | empirisch-nichts-gefunden | -0.012 | -0.22 | 6/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| Swing-Bruch (Donchian-Kanal, mb_kind=channel), bester Survivor ueber d | c-Fibonacci Wege-Karte | maband | Praemisse | empirisch-nichts-gefunden | -0.031 | +0.85 | 6/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| AC-06d Leg-Invalidierung als Stop (tm_stop_mode=leg) auf AC-06-Entry,  | c-Fibonacci Wege-Karte | maband | Praemisse | empirisch-nichts-gefunden | -0.046 | -0.59 | 4/8 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| SCALP_NQ_t0.5_hEOD ORB-Scalp enges Ziel (ehem. Bein 9), ohne Nacht-Bed | c-Overnight-Bias ORB Wege-Karte | orb | Praemisse | empirisch-nichts-gefunden | -0.048 | -0.79 | 3/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| TN-10 Momentum innerhalb der Globex-Nacht | c-Session Momentum Wege-Karte | asian | Praemisse | empirisch-nichts-gefunden | -0.060 | +0.55 | 6/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| SES-W42a ruhiger Vormittag -> Nachholen am Nachmittag (tm_rvol_max) | c-Session Momentum Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.077 | +0.18 | 6/9 | Praemisse traegt nicht (IS edge>=1.0), N = 1 (BASE, nur IS) |
| AC-06d Leg-Invalidierung als Stop (tm_stop_mode=leg) auf AC-06-Entry,  | c-Fibonacci Wege-Karte | maband | Praemisse | empirisch-nichts-gefunden | -0.084 | -1.14 | 3/9 | Praemisse traegt nicht (IS edge>=1.0), N = 1 (BASE, nur IS) |
| XD-12_NQ·tm_xref_min=0.5,tm_xref_len=5,tm_xref_base=prev_close | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.092 | -0.48 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.0917, -1.3 SE, t_alpha -0.48); allein WF-positiv ist kein Effektbeleg |
| FH_NQ_Momentum_d260821 | 1 | ts_reversal | Vor-Gates | empirisch-nichts-gefunden | -0.093 | +0.04 | 8/9 | Vor-Gates fallen (IS, cost2t, edge, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| ONORB-W33a Stop an realisierter Nacht-Vola (tm_stop_mode=on_sigma) | c-Overnight-Bias ORB Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.095 | -1.26 | 4/9 | Praemisse traegt nicht (IS edge>=1.0), N = 1 (BASE, nur IS) |
| FH_NQ_Momentum_BEo02_TE04v2 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.107 | -0.01 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.107, -1.1 SE, t_alpha -0.01); allein WF-positiv ist kein Effektbeleg |
| TS-11_NQ·tm_er_min=0.3,tm_sig_len=30,tm_thr=0.002,tm_stop_mult=0.3 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.116 | -0.06 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.116, -1.2 SE, t_alpha -0.06); allein WF-positiv ist kein Effektbeleg |
| ADX-W27 ADX-Peak-Exit (tf5, give 8) auf dem NQ-Momentum-Traeger | c-ADX Wege-Karte | tsmom | Buch | empirisch-nichts-gefunden | -0.127 | -0.47 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.127, -1.5 SE, t_alpha -0.47); allein WF-positiv ist kein Effektbeleg |
| FH_NQ_Momentum_long_TE15v2 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.138 | -0.42 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1375, -1.4 SE, t_alpha -0.42); allein WF-positiv ist kein Effektbeleg |
| TS-12_NQ·tm_thr=0.3,tm_sig_len=15,tm_stop_mult=0.3 | 1 | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.143 | -0.42 | 8/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| hf_combo_Mom_d260818·rev_thr=0.0015,rev_signal_min=20,rev_stop_mult=0. | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.150 | +0.18 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1505, -1.4 SE, t_alpha 0.18); allein WF-positiv ist kein Effektbeleg |
| NQ_Momentum_exit·exit_profile=eod,rev_stop_mult=0.5,be_trigger=0.5 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.151 | -0.23 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.151, -1.3 SE, t_alpha -0.23); allein WF-positiv ist kein Effektbeleg |
| NIGHT_Momentum_4 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.152 | -0.21 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1517, -1.2 SE, t_alpha -0.21); allein WF-positiv ist kein Effektbeleg |
| FH_NQ_MOM_lowVIX | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.159 | -0.06 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1587, -1.3 SE, t_alpha -0.06); allein WF-positiv ist kein Effektbeleg |
| AC-06b Grid um die AC-06-Survivors | c-VWAP-Offensive | maband | Buch | empirisch-nichts-gefunden | -0.162 | -0.23 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1621, -1.2 SE, t_alpha -0.23); allein WF-positiv ist kein Effektbeleg |
| TV-07_NQ·tm_sigma_q_max=0.7,tm_atr_exp_max=None,tm_gap_max=None,tm_sto | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.180 | -0.67 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1798, -1.8 SE, t_alpha -0.67); allein WF-positiv ist kein Effektbeleg |
| AXV-W26 ADX-Rang-Gate auf VWAP-Ueberdehnung (Continuation), ADX-Arm | c-ADX x VWAP Wege-Karte | maband | Buch | empirisch-nichts-gefunden | -0.185 | +0.75 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1848, -1.0 SE, t_alpha 0.75); allein WF-positiv ist kein Effektbeleg |
| AR-04_NQ·tm_dow=None,tm_ema_confirm=20,tm_rvol_min=None,tm_sigma_q_max | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.185 | -0.62 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1851, -1.7 SE, t_alpha -0.62); allein WF-positiv ist kein Effektbeleg |
| FH_NQ_Momentum_ON01_onret045 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.196 | -0.97 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1958, -1.8 SE, t_alpha -0.97); allein WF-positiv ist kein Effektbeleg |
| AW-15 Continuation ab Ueberdehnung (sigma-normiert) | c-VWAP-Offensive | maband | Vor-Gates | empirisch-nichts-gefunden | -0.196 | -0.10 | 7/9 | Vor-Gates fallen (IS), N = 1 (WF-deploy-Config) |
| FA-01_NQ·tm_sig_len=15,signal_profile=rangepos,tm_stop_mult=0.4,pb_pro | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.199 | -0.59 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1991, -1.7 SE, t_alpha -0.59); allein WF-positiv ist kein Effektbeleg |
| gen_tsmom_combo_prevclose_hf_NQ·tm_ema_confirm=150,tm_rvol_min=None,tm | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.199 | -0.68 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1993, -1.8 SE, t_alpha -0.68); allein WF-positiv ist kein Effektbeleg |
| TS-13_NQ·tm_wins_k=3,tm_thr=0.002,tm_sig_len=60,tm_stop_mult=0.3 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.204 | +0.56 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2039, -1.4 SE, t_alpha 0.56); allein WF-positiv ist kein Effektbeleg |
| hf_combo_Mom_d260818·rev_thr=0.0025,rev_signal_min=15,rev_stop_mult=0. | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.205 | -0.72 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2046, -1.9 SE, t_alpha -0.72); allein WF-positiv ist kein Effektbeleg |
| ON01_CASHOPEN_NQ·nacht=on_min0.25,fenster=w15_thr0.30,risk_exit=rng0.3 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.206 | -0.89 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2057, -1.8 SE, t_alpha -0.89); allein WF-positiv ist kein Effektbeleg |
| AB-06_NQ·tm_atr_exp_min=None,tm_atr_exp_max=1.1,tm_stop_mult=0.5 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.207 | -0.72 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2067, -2.0 SE, t_alpha -0.72); allein WF-positiv ist kein Effektbeleg |
| TV-09_NQ·vix_gate=low,vix_ref=abs,vix_thr=22,vix_win=30 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.211 | -1.01 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2108, -2.0 SE, t_alpha -1.01); allein WF-positiv ist kein Effektbeleg |
| AC-06d Leg-Invalidierung als Stop (tm_stop_mode=leg) auf AC-06-Entry,  | c-Fibonacci Wege-Karte | maband | Buch | empirisch-nichts-gefunden | -0.212 | -0.37 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2116, -1.5 SE, t_alpha -0.37); allein WF-positiv ist kein Effektbeleg |
| gen_maband_combo_channel_atr_tfm_NQ·tm_stop_mult=0.5,tm_ema_confirm=20 | 1 | maband | Praemisse | empirisch-nichts-gefunden | -0.214 | -0.36 | 4/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| TV-02_NQ·tm_sigma_q_max=0.9,tm_sigma_q_min=None,tm_stop_mult=0.5,tm_si | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.224 | -0.85 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2239, -2.0 SE, t_alpha -0.85); allein WF-positiv ist kein Effektbeleg |
| AW-05 'Baender als Ziel/Stop' (misst faktisch sigma-Stop + festes R) | c-VWAP-Offensive | maband | Praemisse | empirisch-nichts-gefunden | -0.227 | -2.05 | 2/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| vt01b_NQ·vol_gate=aus,sig_profile=len15_thr0.003,tm_dir=long_only | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.229 | +0.36 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2291, -1.2 SE, t_alpha 0.36); allein WF-positiv ist kein Effektbeleg |
| TE-04_NQ_v2·be_trigger=0.5,be_offset=0,trail_trigger=None,trail_dist=0 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.234 | -1.12 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2338, -2.1 SE, t_alpha -1.12); allein WF-positiv ist kein Effektbeleg |
| ONORB-W24a_NQ·PREMISE0 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.243 | -0.30 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2434, -1.7 SE, t_alpha -0.3); allein WF-positiv ist kein Effektbeleg |
| TV-13_NQ·tm_panic_veto=True,tm_sigma_q_max=None,tm_stop_mult=0.3,exit_ | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.246 | -1.14 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2457, -2.5 SE, t_alpha -1.14); allein WF-positiv ist kein Effektbeleg |
| ONORB-W7a Opening-Range-Form (rangepos) mit Nacht-Gate on_ret_min | c-Overnight-Bias ORB Wege-Karte | tsmom | Buch | empirisch-nichts-gefunden | -0.249 | -0.33 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2493, -1.6 SE, t_alpha -0.33); allein WF-positiv ist kein Effektbeleg |
| tsmom_erret_NQ·tm_thr=0.0015,tm_stop_mult=0.3,tm_sig_len=15 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.250 | -1.29 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2497, -2.5 SE, t_alpha -1.29); allein WF-positiv ist kein Effektbeleg |
| ON01 Opening-Drive nur nach Nacht-Preisfindung (on_ret_min 0,0025) | c-Overnight-Bias ORB Wege-Karte | tsmom | Buch | empirisch-nichts-gefunden | -0.261 | -1.41 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2611, -2.5 SE, t_alpha -1.41); allein WF-positiv ist kein Effektbeleg |
| NQ_Momentum_exit·exit_profile=rr2.0,rev_stop_mult=0.5,be_trigger=0.5 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.277 | -1.79 | 5/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2769, -2.2 SE, t_alpha -1.79); allein WF-positiv ist kein Effektbeleg |
| TS-17_NQ·tm_thr=0.4,tm_sig_len=60,tm_stop_mult=0.3,exit_profile=eod | 1 | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.282 | -0.03 | 5/9 | Vor-Gates fallen (top5), N = 1 (WF-deploy-Config) |
| REFINE_Momentum_4 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.282 | -1.91 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2821, -2.3 SE, t_alpha -1.91); allein WF-positiv ist kein Effektbeleg |
| TK-03_NQ·tm_sig_len=120,tm_thr=0.0015,tm_stop_mult=0.5 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.288 | +0.33 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2882, -1.7 SE, t_alpha 0.33); allein WF-positiv ist kein Effektbeleg |
| FH_NOISE_ORB_NQ | 2 | noise_orb | Buch | empirisch-nichts-gefunden | -0.289 | +0.02 | 9/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2887, -1.7 SE, t_alpha 0.02); allein WF-positiv ist kein Effektbeleg |
| Kontrollzelle: Opening-Drive nach RUHIGER Nacht (tm_on_ret_max 0,0025) | c-Overnight-Bias ORB Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.295 | -0.20 | 4/9 | Praemisse traegt nicht (IS edge>=1.0), N = 1 (BASE, nur IS) |
| GEX01_NQ·gex_regime=vix_rank_high,tm_sig_len=15,tm_stop_mult=0.3 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.296 | -1.61 | 5/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2962, -2.6 SE, t_alpha -1.61); allein WF-positiv ist kein Effektbeleg |
| NIGHT_Momentum_3 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.296 | -1.47 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2965, -2.4 SE, t_alpha -1.47); allein WF-positiv ist kein Effektbeleg |
| NQ Gap-Continuation (gap-Modus), bester Continuation-Arm | c-Gap Wege-Karte | gap | Buch | empirisch-nichts-gefunden | -0.306 | -1.09 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.3058, -2.0 SE, t_alpha -1.09); allein WF-positiv ist kein Effektbeleg |
| AK-01_NQ·mb_fast=1,mb_slow=15,mb_bar_min=5,tm_stop_mult=0.4 | 1 | maband | Vor-Gates | empirisch-nichts-gefunden | -0.405 | -0.08 | 6/9 | Vor-Gates fallen (top5), N = 1 (WF-deploy-Config) |
| ONORB-W29a weite Nacht (on_range_min 1,0) als Tor fuer den Opening-Dri | c-Overnight-Bias ORB Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.452 | -1.73 | 5/9 | Praemisse traegt nicht (IS usd>0), N = 1 (BASE, nur IS) |
| TS-14_NQ·tm_thr=0.3,tm_rank_win=120,tm_sig_len=15,tm_stop_mult=0.5 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.476 | -1.63 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4757, -3.0 SE, t_alpha -1.63); allein WF-positiv ist kein Effektbeleg |
| ONORB-W45a_NQ·tm_pre_ret_min=None,tm_on_ret_min=None,tm_pre_rvol_min=N | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.476 | -1.16 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4759, -2.3 SE, t_alpha -1.16); allein WF-positiv ist kein Effektbeleg |
| NQ_MOM_maxfreq_sig15_thr2_stop1.5 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.479 | -0.69 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4791, -2.5 SE, t_alpha -0.69); allein WF-positiv ist kein Effektbeleg |
| ORB_VIXBAND_NQ | 1 | orb | Vor-Gates | empirisch-nichts-gefunden | -0.481 | -1.67 | 5/9 | Vor-Gates fallen (IS, cost2t, edge, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| AW-14c Anker-Kontrolle mit rand_time-Placebo (bester echter Session-An | c-VWAP-Offensive | maband | Buch | empirisch-nichts-gefunden | -0.481 | -0.41 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4814, -2.6 SE, t_alpha -0.41); allein WF-positiv ist kein Effektbeleg |
| TE-01_NQ·tm_stop_mult=1.2,tm_sig_len=30,exit_profile=rr1.5 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.494 | -1.05 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4938, -2.7 SE, t_alpha -1.05); allein WF-positiv ist kein Effektbeleg |
| AW-14c_NQ·anchor=kontrolle_randt2,mb_side=against,mb_vwap_k=2,tm_stop_ | 1 | maband | Buch | empirisch-nichts-gefunden | -0.501 | -0.40 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.5015, -2.7 SE, t_alpha -0.4); allein WF-positiv ist kein Effektbeleg |
| AW-14b Anker-Kontrolle echter Anker vs mb_rand_level (bester echter An | c-VWAP-Offensive | maband | Vor-Gates | empirisch-nichts-gefunden | -0.520 | +0.01 | 6/9 | Vor-Gates fallen (IS, cost2t, edge, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| NQ_MOM_propbest_stop0.75 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.522 | -2.39 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.5221, -3.5 SE, t_alpha -2.39); allein WF-positiv ist kein Effektbeleg |
| TV-05_NQ·tm_stop_mode=atr,tm_stop_mult=0.3,exit_profile=eod | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.534 | -2.27 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.5338, -3.6 SE, t_alpha -2.27); allein WF-positiv ist kein Effektbeleg |
| REFINEAPEX_Momentum_4 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.540 | -1.40 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.5401, -2.9 SE, t_alpha -1.4); allein WF-positiv ist kein Effektbeleg |
| FH_ES_Momentum_s15 | 1 | ts_reversal | Vor-Gates | empirisch-nichts-gefunden | -0.542 | -2.40 | 4/9 | Vor-Gates fallen (IS, OOS, cost2t, dollar, edge, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| NQ_MOM_champion_sig15_thr3_stop1.5 | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.548 | -1.41 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.5481, -2.7 SE, t_alpha -1.41); allein WF-positiv ist kein Effektbeleg |
| RTH-Ausbruch durch Overnight-High/-Low (asian break_us), Seiten gemisc | c-Overnight-Bias ORB Wege-Karte | asian | Vor-Gates | empirisch-nichts-gefunden | -0.579 | -1.31 | 8/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| AW-02 Anker-VWAP ab Tagesextrem | c-VWAP-Offensive | maband | Praemisse | empirisch-nichts-gefunden | -0.606 | -0.47 | 7/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| NQ_Momentum | 1 | ts_reversal | Buch | empirisch-nichts-gefunden | -0.606 | -2.33 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.6059, -3.8 SE, t_alpha -2.33); allein WF-positiv ist kein Effektbeleg |
| asian_EUbreak_NQ·asia_stop_mult=0.5,asia_target_mult=None,asia_buffer_ | 1 | asian | Vor-Gates | empirisch-nichts-gefunden | -0.617 | -1.62 | 8/9 | Vor-Gates fallen (top5), N = 1 (WF-deploy-Config) |
| FH_NQ_Asia-Break-USsession | 1 | asian | Vor-Gates | empirisch-nichts-gefunden | -0.669 | -1.94 | 8/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| AW-11b VWAP-Reclaim gegen Pullback | c-VWAP-Offensive | maband | Vor-Gates | empirisch-nichts-gefunden | -0.699 | -0.48 | 6/9 | Vor-Gates fallen (IS, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| maband-Reparametrisierung VWAP-Pullback (nah am VWAP) | c-VWAP-Offensive | maband | Praemisse | empirisch-nichts-gefunden | -0.713 | -0.91 | 5/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| FLIP_NQ_b0.75_WINDOW | 2-flip | flip | Vor-Gates | empirisch-nichts-gefunden | -0.850 | -0.46 | 7/9 | Vor-Gates fallen (top5), N = 1 (WF-deploy-Config) |
| FLIP_NQ_b0.75_SIGNALS | 2-flip | flip | Vor-Gates | empirisch-nichts-gefunden | -0.862 | -0.28 | 5/9 | Vor-Gates fallen (IS, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| NOISE_ORB_NQ_m1.0 | 2 | noise_orb | Buch | Dublette | -0.289 | +0.02 | 9/9 | identische Messung wie a8ce3f72c7d03514, erbt dessen Urteil |
| XD-12 NQ-Momentum nur wenn ES mitzieht (z-Score-Gate) | c-ES-NQ-Divergenz Wege-Karte | ts_reversal | nicht messbar | Dublette | – | – | – | Duplikat von 833006ef56156695 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| London-Range (03:00-09:25) als RTH-Ausbruchsband (asian break_us) | c-Overnight-Bias ORB Wege-Karte | asian | nicht messbar | Dublette | – | – | – | Duplikat von a3163768bf46fd80 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| ONORB-W45a Vor-Open-Segment 08:30-09:30 (tm_pre_rvol_min 1,2) | c-Overnight-Bias ORB Wege-Karte | tsmom | nicht messbar | Dublette | – | – | – | Duplikat von b14a9192473401cb (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| Gap-Erweiterung grosse Gaps (NQ_GAP_cont, Bank-Fund), Volumen-Kopplung | c-Session Momentum Wege-Karte | gap | nicht messbar | Dublette | – | – | – | Duplikat von 69e67bc2739989e6 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| AW-01 Bestandsbein NQ_VWAP-Pullback (seit #161 raus) | c-VWAP-Offensive | vwap_pullback | nicht messbar | Dublette | – | – | – | Duplikat von 961ae1dffdc993bb (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| BE 0,5R + Offset 0,2R auf NQ_VWAP-Pullback | c-VWAP-Offensive | vwap_pullback | nicht messbar | Dublette | – | – | – | Duplikat von f89e9e6abbf2edb3 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| Gap-Erweiterung (Continuation) | c-Overnight-Bias ORB Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_GAP_W3, erbt dessen Urteil |
| Nacht-Range bricht am RTH-Open (break_us) | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ONORB_W15/W16, erbt dessen Urteil |
| ADX>25 bzw. Tages-ADX hoch als Momentum-Gate | c-ADX Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Die 533 Trials sind AR-15 (200d-MA-Tagesmaske) + AR-17 (Vola-Tagesmaske), mode regime_gate (Backfill, kein qbt-Modus), k |
| Messweg: ADX gegen Vola/ER (Feature-Ebene, Folgetag-Information) | c-ADX Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Feature-Studie, keine Handelsregel |
| Retracement-Tiefe kontinuierlich (Pullback-Tiefe) | c-Fibonacci Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Event-Studie (477k Events), keine Handelsregel |
| Fib-Level ~ Rundzahl, Bounce-Arm | c-Fibonacci Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Prescan (#149/#151), keine Handelsregel |
| Beruehrungszaehler k | c-Fibonacci Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Prescan AB-14 (prebreak_precursors.py), keine Handelsregel |
| Opening-Drive ohne Level: First-Bar-EMA-Trail (firstbar_ematrail) | c-Overnight-Bias ORB Wege-Karte | firstbar_ematrail | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: eigener Developer-Modus firstbar_ematrail (developer/firstbar_core.py), kein qbt-Modus |
| NY-OR-Bruch, Retest-Einstieg (Pineda) | c-Overnight-Bias ORB Wege-Karte | orb | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: orb_retest_068_results.json speichert nur Namen, keine Params |
| London-OR-Bruch ohne Nacht-Bedingung (Lore-Weg) | c-Overnight-Bias ORB Wege-Karte | asian | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: #028-Lauf (46 Configs, asian.py Juli) ohne gespeicherte Params |
| Hohes RVOL sagt Fortsetzung (long/short) | c-RVOL Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Event-Studie volshock (#125), keine Handelsregel |
| Level-Bruch mit hohem RVOL (ORB or_rvol_min) | c-RVOL Wege-Karte | orb | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: orb_inplay_068_results.json speichert nur Namen |
| RVOL-Gate auf maband-Signalen | c-RVOL Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: scheingemessen: maband-RVOL war bis AP206 (21.09.) ein Uhrzeit-Filter; 195 Survivors mit RVOL-Gate nie mit Fix nachgerec |
| Durchbruch durchs Rundzahl-Level (long/short) | c-Rundzahlen Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: kappa-Prescan, keine Handelsregel |
| Kaskade / Kompression vor / Expansion nach / synchroner Bruch | c-Rundzahlen Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: abgeleitet aus W5k, bewusst keine eigene Messung |
| Nacht-Range bricht beim London-Open | c-Session Momentum Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: #028-Lauf ohne gespeicherte Params |
| Segment->Segment spaeter Einstieg (tm_sig_start 120/210) | c-Session Momentum Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Generator-Achse ueber ~70 *_spaet-Jobs ohne Survivor; Bestwerte nur bei n<60 -> kein belastbarer Einzelkandidat |
| VWAP-Steigung als Signal | c-VWAP-Offensive | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Identitaets-Messung (Steigung = verrauschtes side-Signal), keine eigene Config |

## Mean Reversion (28)

| Kandidat | Teil | Modus | v4-Stufe | Kategorie | dSR | t_α | Jahre | Buch-Lücke / Grund |
|---|---|---|---|---|---|---|---|---|
| FH_NQ_ORB-fade_nr7_honest ⭐ | 1 | orb | Praemisse | unentscheidbar | +0.141 | +2.46 | 7/9 | IS-BASE (IS expR>0, IS edge>=1.0) widerspricht WF-OOS (7/9 Jahre, OOS 8075.82 $, dSR 0.1411, t_alpha 2.46): Nachtest |
| FH_RTY_Gap-fade_retune_RT ⭐ | 1-gap | gap | Vor-Gates | unentscheidbar | +0.083 | +2.32 | 7/8 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| Open ausserhalb Nacht-Range laeuft zurueck (asian fade_us) ⭐ | c-Overnight-Bias ORB Wege-Karte | asian | Praemisse | unentscheidbar | +0.049 | +1.94 | 5/9 | IS-BASE (IS expR>0, IS edge>=1.0) widerspricht WF-OOS (5/9 Jahre, OOS 5082.19 $, dSR 0.0486, t_alpha 1.94): Nachtest |
| NQ Gap-Fade klein (0,5-1,5 ATR, 10-min-Bestaetigung), Seiten gemischt | c-Gap Wege-Karte | gap | Buch | unentscheidbar | -0.071 | +1.02 | 6/9 | ·dSR· < 1 SE (dSR -0.0706, SE 0.1863) gegen das Next-Buch |
| FH_NQ_Gap-fade_hf | 1-gap | gap | Buch | unentscheidbar | -0.078 | +0.89 | 6/9 | ·dSR· < 1 SE (dSR -0.0784, SE 0.1617) gegen das Next-Buch |
| SZ-11 Mittags-Ausbruch dreht (RTY) | c-Session Momentum Wege-Karte | tsmom | Vor-Gates | empirisch-nichts-gefunden | +0.021 | +1.04 | 3/8 | Vor-Gates fallen (IS/OOS-leer, cost2t, dollar, edge, n, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| gen_tsmom_combo_fade_atr_spaet_RTY·tm_stop_mult=0.8,tm_ema_confirm=Non | 1 | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.007 | +0.24 | 5/8 | Vor-Gates fallen (IS/OOS-leer, cost2t, n, sharpe_t), N = 1 (WF-deploy-Config) |
| ADX-W6 Bar-ADX-Peak<25 Chop-Fenster, Fade-Traeger (ADX-Arm der Praemis | c-ADX Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.018 | +0.80 | 5/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| CR-01 Fade nach RVOL-Spike (ES) | c-RVOL Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.053 | -0.47 | 3/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| FH_NQ_ONREV_i2 | 2 | i2 | Vor-Gates | empirisch-nichts-gefunden | -0.240 | +1.75 | 5/9 | Vor-Gates fallen (IS, sharpe_t), N = 1 (WF-deploy-Config) |
| lp_prevday_NQ·tm_thr=0.005,risk_profile=atr0.8_eod,regime=vixrank70 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.245 | +0.56 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2446, -1.2 SE, t_alpha 0.56); allein WF-positiv ist kein Effektbeleg |
| lp_prevday Vortages-RTH -> heute (prev_rth-Fade nach Abverkauf, VIX-Ra | c-Session Momentum Wege-Karte | tsmom | Buch | empirisch-nichts-gefunden | -0.280 | +0.48 | 5/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2799, -1.4 SE, t_alpha 0.48); allein WF-positiv ist kein Effektbeleg |
| SZ-08 Europa-Close-Unwind 11:00-11:30 (Fade) | c-Session Momentum Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.462 | -1.79 | 0/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| ONORB-W30a enge Nacht -> NY-OR-Fade (asian break as_side=against) | c-Overnight-Bias ORB Wege-Karte | asian | Praemisse | empirisch-nichts-gefunden | -0.638 | -0.54 | 3/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| AW-09b Ueberdehnung zum VWAP als Fade (k=2) | c-VWAP-Offensive | maband | Praemisse | empirisch-nichts-gefunden | -0.649 | -1.49 | 0/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| TN-03 Tug-of-War: grosser Overnight-Move dreht den RTH-Tag | c-Overnight-Bias ORB Wege-Karte | tsmom | Praemisse | empirisch-nichts-gefunden | -0.744 | -0.14 | 5/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| Overnight-Gap-Reversal intraday (i2 on_rev), lebende Verwandte | c-Overnight-Bias ORB Wege-Karte | i2 | Vor-Gates | Dublette | -0.240 | +1.75 | 5/9 | identische Messung wie 36b9ec277938c367, erbt dessen Urteil |
| RTY Gap-Fade Retune (Plateau-Nachbar) | c-Gap Wege-Karte | gap | nicht messbar | Dublette | – | – | – | Duplikat von ccaa42620fc49957 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| ADX-Rollover als Exit eines VWAP-Trades (gemessen auf dem tsmom-Traege | c-ADX x VWAP Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ADX_W27, erbt dessen Urteil |
| Preis laeuft zum Vortages-Close (Gap-Fade) | c-Overnight-Bias ORB Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_GAP_W1/W2/W32, erbt dessen Urteil |
| S1-Richtung dreht am US-Open / Abprallen an Segment-Range (asian fade_ | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ONORB_W17_fadeus, erbt dessen Urteil |
| S8 dreht im RTH (TN-03, SES-W6a) | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ONORB_W40, erbt dessen Urteil |
| Rueckkehr zum Vortages-Close (Gap-Fill) | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_GAP_W1/W2/W32, erbt dessen Urteil |
| Tages-ADX niedrig -> MR/Fade an | c-ADX Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: nur als off-Anteil-gematchte Gegenrichtung in #139 gemessen (Tagesmaske auf Buch-Beinen), keine Einzelstrategie |
| hin zum VWAP bei ADX niedrig -> MR am VWAP | c-ADX x VWAP Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: tot ueber externe/alte Messungen (#002-005 QuantPad, #196 VWAP-Z-MR mit ADX<20-25 NO-GO, #211, #097), keine Engine-Confi |
| Overnight-VWAP als Level (on_frozen/globex) | c-Overnight-Bias ORB Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Placebo-Messung #108 (8 VWAP-Arten), keine Einzelconfig |
| Abprallen am Rundzahl-Level | c-Rundzahlen Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Prescan-Zellen AP153 (10 Zellen), keine Handelsregel |
| Halb-Level x.50 / Klassen-Dosis | c-Rundzahlen Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Close-Histogramm, keine Handelsregel |

## Intraday Bias (40)

| Kandidat | Teil | Modus | v4-Stufe | Kategorie | dSR | t_α | Jahre | Buch-Lücke / Grund |
|---|---|---|---|---|---|---|---|---|
| FH_OPEXMOM_NQ | 1 | cal | DURCH | DURCH | +0.048 | +1.47 | 8/9 | Next-Week-Buch (Max 01.10.), Vorab-Lesart ernst; fehlt: /wochenende, Original-Grid-Job, NT8-Bein |
| FH_OPEXMOM_ES ⭐ | 1 | cal | Vor-Gates | unentscheidbar | +0.043 | +1.58 | 7/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| FH_EVENT_ES_primary ⭐ | 1 | cal | Vor-Gates | unentscheidbar | +0.035 | +1.20 | 7/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| FH_CAL_fomcpost_ES ⭐ | 1 | cal | Praemisse | unentscheidbar | +0.022 | +0.62 | 3/4 | Praemisse n 44 < 60 (Power) |
| TS-21_NQ·tm_sig_start=330,tm_sig_len=30,confirm=delta0.15,tm_stop_mult | 1 | tsmom | Praemisse | unentscheidbar | +0.002 | – | 0/6 | 0 Trades in der Basis-Config: Mapping-Verdacht (Params passen nicht zur Engine) |
| NQ_Asia-Dir-USopen_exit·asia_target_mult=2,asia_stop_mult=0.5,tr_end=1 | 1 | asian | Vor-Gates | unentscheidbar | -0.104 | -0.26 | 6/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| FH_NQ_Asia-Dir_d260821_thr0725 | 1 | asian | Buch | unentscheidbar | -0.120 | -0.09 | 6/9 | ·dSR· < 1 SE (dSR -0.12, SE 0.1333) gegen das Next-Buch |
| hf_asian_thr_NQ·asia_dir_thr=0.8,asia_target_mult=None,tr_end=13:00 | 1 | asian | Vor-Gates | unentscheidbar | -0.154 | -0.19 | 6/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| FH_VIX_spike_rev_NQ | 2 | vix_bias | Vor-Gates | unentscheidbar | -0.258 | -0.66 | 5/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| gen_asian_us_dir_NQ_r2_08211916·asia_stop_mult=0.5,asia_target_mult=1. | 1 | asian | Buch | kein Tod | -0.027 | +0.25 | 7/9 | Klon von NQ_Asia-Dir-USopen_d260820 (r 0.829): Variante des Beins, als Ersatz nicht besser |
| TN-04_NQ·lh_ref_min=240,lh_thr=0.003,lh_stop_mult=0.4,lh_exclude_news= | 1 | last_hour | Buch | kein Tod | -0.038 | -0.11 | 7/9 | Klon von NQ_LastHour_v3 (r 0.933): Variante des Beins, als Ersatz nicht besser |
| NQ_LastHour_exit·target_mult=1.5,lh_stop_mult=0.4,be_trigger=None | 1 | last_hour | Buch | kein Tod | -0.060 | -0.16 | 7/9 | Klon von NQ_LastHour_v3 (r 0.903): Variante des Beins, als Ersatz nicht besser |
| gen_asian_us_dir_NQ_exits_08211923·asia_target_mult=2,tr_end=13:00 | 1 | asian | Buch | kein Tod | -0.070 | +0.04 | 6/9 | Klon von NQ_Asia-Dir-USopen_d260820 (r 0.726): Variante des Beins, als Ersatz nicht besser |
| FH_OPEXMOM_YM ⭐ | 1 | cal | Vor-Gates | empirisch-nichts-gefunden | +0.020 | +1.06 | 6/9 | Vor-Gates fallen (OOS, cost2t, sharpe_t), N = 1 (WF-deploy-Config) |
| FH_OPEXMOM_RTY ⭐ | 1 | cal | Vor-Gates | empirisch-nichts-gefunden | +0.008 | +0.60 | 5/8 | Vor-Gates fallen (IS, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| TS-21_NQ·tm_sig_start=330,tm_sig_len=30,confirm=rvol1.2,tm_stop_mult=0 | 1 | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.077 | -0.58 | 4/9 | Vor-Gates fallen (IS, OOS, cost2t, edge, sharpe_t), N = 1 (WF-deploy-Config) |
| hf_asian_thr_NQ·asia_dir_thr=0.8,asia_target_mult=1,tr_end=13:00 | 1 | asian | Vor-Gates | empirisch-nichts-gefunden | -0.084 | -0.22 | 7/9 | Vor-Gates fallen (IS, sharpe_t), N = 1 (WF-deploy-Config) |
| hf_asian_thr_NQ·asia_dir_thr=0.8,asia_target_mult=1,tr_end=15:55 | 1 | asian | Vor-Gates | empirisch-nichts-gefunden | -0.088 | -0.32 | 8/9 | Vor-Gates fallen (IS, sharpe_t), N = 1 (WF-deploy-Config) |
| ES Montags-Gap (cal_mongap, ungefiltert 0-5 ATR) | c-Gap Wege-Karte | gap | Praemisse | empirisch-nichts-gefunden | -0.096 | -1.28 | 4/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| gen_asian_us_dir_NQ_r2_08211800·asia_dir_thr=0.6875,asia_target_mult=1 | 1 | asian | Buch | empirisch-nichts-gefunden | -0.154 | -0.38 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.1545, -1.2 SE, t_alpha -0.38); allein WF-positiv ist kein Effektbeleg |
| TN-08 Europa-Segment (03:00-09:30) als RTH-Bias | c-Session Momentum Wege-Karte | asian | Vor-Gates | empirisch-nichts-gefunden | -0.185 | +0.53 | 6/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| FH_NQ_Asia-Dir_original_noTarget | 1 | asian | Buch | empirisch-nichts-gefunden | -0.226 | -0.64 | 5/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.2263, -1.8 SE, t_alpha -0.64); allein WF-positiv ist kein Effektbeleg |
| TN-01 Overnight-Return setzt sich im RTH fort | c-Session Momentum Wege-Karte | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.332 | -0.99 | 7/9 | Vor-Gates fallen (OOS, cost2t, dollar, edge, last3y, sharpe_t, top5), N = 1 (WF-deploy-Config) |
| FH_OR_DELTA_BIAS_NQ_long | 2 | or_delta | Buch | empirisch-nichts-gefunden | -0.333 | -0.09 | 8/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.3326, -1.9 SE, t_alpha -0.09); allein WF-positiv ist kein Effektbeleg |
| ONORB-W34a_NQ·PREMISE0 | 1 | asian | Buch | empirisch-nichts-gefunden | -0.341 | -0.18 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.3405, -2.1 SE, t_alpha -0.18); allein WF-positiv ist kein Effektbeleg |
| TN-09 Wochentags-Split des Overnight-Signals | c-Overnight-Bias ORB Wege-Karte | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.341 | -0.63 | 6/9 | Vor-Gates fallen (IS, sharpe_t), N = 1 (WF-deploy-Config) |
| TN-12 nur der grosse Overnight-Move (Schwelle) | c-Session Momentum Wege-Karte | tsmom | Vor-Gates | empirisch-nichts-gefunden | -0.344 | -0.52 | 6/9 | Vor-Gates fallen (OOS, cost2t, last3y, sharpe_t), N = 1 (WF-deploy-Config) |
| TS-15_NQ·tm_sig_start=0,tm_sig_len=30,tm_thr=0.002,tm_stop_mult=0.3 | 1 | tsmom | Buch | empirisch-nichts-gefunden | -0.376 | -1.26 | 6/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.3756, -3.0 SE, t_alpha -1.26); allein WF-positiv ist kein Effektbeleg |
| ONORB-W34a Lage des Opens in der Nacht-Range (as_dir_src=on_pos) | c-Overnight-Bias ORB Wege-Karte | asian | Buch | empirisch-nichts-gefunden | -0.423 | -0.38 | 7/9 | Rolle Zusatzbein: kein eigenes Alpha gegen das Next-Buch 14f59c90 (dSR -0.4226, -2.6 SE, t_alpha -0.38); allein WF-positiv ist kein Effektbeleg |
| first30 -> last30 (Gao/Han/Li/Zhou), Momentum-Seite | c-Session Momentum Wege-Karte | i2 | Praemisse | empirisch-nichts-gefunden | -0.441 | -1.68 | 3/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| ONORB-W27a Asien/Europa gleichgerichtet -> Fortsetzung | c-Overnight-Bias ORB Wege-Karte | asian | Vor-Gates | empirisch-nichts-gefunden | -0.498 | -0.79 | 6/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| AW-06 Zeitanteil ueber VWAP als Tagesbias | c-VWAP-Offensive | maband | Vor-Gates | empirisch-nichts-gefunden | -0.728 | -1.49 | 5/9 | Vor-Gates fallen (sharpe_t, top5), N = 1 (WF-deploy-Config) |
| TS-21 Schlussstunden-Signal mit Orderflow-Bestaetigung (Ersatz LastHou | c-RVOL Wege-Karte | tsmom | nicht messbar | Dublette | – | – | – | Duplikat von 8fa2a0126739bdb6 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| Gapgroesse als Tor auf ein Bein (ON01, gehoert ONORB W23/W7) | c-Gap Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ONORB_W7_ON01, erbt dessen Urteil |
| S7-intern 15:00-15:45 -> Close (TS-21) | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_RVOL_W20, erbt dessen Urteil |
| Wochentags-Struktur (TN-09) | c-Session Momentum Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ONORB_W42, erbt dessen Urteil |
| ES_TOM_F1_regime_cell | 2 | regime_cell | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: nicht messbar: regime_cell ist kein Engine-Modus (nur Scratch-Zellen _scratch_gc_od), Gate v4 braucht einen Trade-Satz |
| Clustering-Intensitaet als Regime | c-Rundzahlen Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Story-Tod + Zeitvariations-Messung (verdict-auditor), keine Handelsregel |
| Overnight-Segment als Filter auf die Schlussstunde | c-Session Momentum Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: gemessen als Tagesfilter am echten NQ_LastHour_v3 (976 Trades, Script), last_hour kennt kein on_ret-Gate; hyp_TN04_NQ li |
| Value-Area-Migration (Valentini Baustein 1) | c-VWAP-Offensive | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Tages-/Candle-Studie, keine Handelsregel |

## Swing (4)

| Kandidat | Teil | Modus | v4-Stufe | Kategorie | dSR | t_α | Jahre | Buch-Lücke / Grund |
|---|---|---|---|---|---|---|---|---|
| Swing: ADX-Rollover ueber Nacht jenseits Tages-VWAP | c-ADX x VWAP Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ADX_W38, erbt dessen Urteil |
| Swing: ADX-Niveau/Rollover ueber Nacht gehalten | c-ADX Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Mehrtages-Event-Studie (Overnight-Halten), qbt kann nicht ueber Nacht halten; Live-Buch-Merker |
| Swing: Overnight-Drift selbst ernten | c-Overnight-Bias ORB Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Overnight-Halten, Live-Buch-Merker; #028 nur 3 Varianten |
| Swing: Overnight-Segment selbst halten | c-Session Momentum Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: Overnight-Halten, Live-Buch-Merker |

## Relative Value (18)

| Kandidat | Teil | Modus | v4-Stufe | Kategorie | dSR | t_α | Jahre | Buch-Lücke / Grund |
|---|---|---|---|---|---|---|---|---|
| LL04_NQES_v2·rv_lead_win=20,rv_thr=0.003,rv_stop=0.3 | 2 | rv | Vor-Gates | unentscheidbar | -0.072 | -0.53 | 7/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| RS-01 Divergenz-Momentum NQ/ES (v2) | c-ES-NQ-Divergenz Wege-Karte | rv | Vor-Gates | unentscheidbar | -0.084 | -1.85 | 3/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| LL01_NQES_v2·rv_thr=0.003,rv_lag_ratio=0.7,rv_stop=0.3 | 2 | rv | Vor-Gates | unentscheidbar | -0.127 | -0.80 | 7/9 | Vor-Gates nur Power-Fails (sharpe_t); MDE nicht gerechnet (Annahme) |
| RV-08 Gap-Divergenz NQ/ES konvergiert | c-ES-NQ-Divergenz Wege-Karte | rv | Praemisse | empirisch-nichts-gefunden | +0.045 | +1.39 | 4/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| LL04_NQES_v2·rv_lead_win=60,rv_thr=0.003,rv_stop=0.3 | 2 | rv | Vor-Gates | empirisch-nichts-gefunden | -0.019 | +0.35 | 8/9 | Vor-Gates fallen (IS, sharpe_t), N = 1 (WF-deploy-Config) |
| RV-09 Gap-Divergenz RTY/ES | c-Gap Wege-Karte | rv | Praemisse | empirisch-nichts-gefunden | -0.024 | -0.45 | 3/8 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| LL04_NQES_v2·rv_lead_win=60,rv_thr=0.002,rv_stop=0.3 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.047 | -0.11 | 6/9 | Praemisse traegt nicht (IS edge>=1.0), N = 1 (BASE, nur IS) |
| LL07_NQES_v2·rv_thr=0.002,rv_lag_ratio=0.5,rv_stop=0.3 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.075 | -0.54 | 5/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| LL01_NQES_v2·rv_thr=0.001,rv_lag_ratio=0.7,rv_stop=0.3 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.099 | -0.31 | 7/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| LL01_NQES_v2·rv_thr=0.002,rv_lag_ratio=0.7,rv_stop=0.3 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.101 | -0.41 | 7/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| LL07_NQES_v2·rv_thr=0.0015,rv_lag_ratio=0.5,rv_stop=0.3 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.104 | -0.81 | 4/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| Spread NQ/ES konvergiert bis EOD | c-ES-NQ-Divergenz Wege-Karte | rv | Praemisse | empirisch-nichts-gefunden | -0.112 | -3.39 | 0/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| RV-10 Gap-Divergenz NQ/YM | c-Gap Wege-Karte | rv | Praemisse | empirisch-nichts-gefunden | -0.162 | -0.17 | 2/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| LL01_NQES_v2·rv_thr=0.002,rv_lag_ratio=0.5,rv_stop=0.75 | 2 | rv | Praemisse | empirisch-nichts-gefunden | -0.166 | -0.97 | 6/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0), N = 1 (BASE, nur IS) |
| SM-04 Divergenz-Fade NQ/ES (unbestaetigter Move faden) | c-ES-NQ-Divergenz Wege-Karte | rv | Praemisse | empirisch-nichts-gefunden | -0.421 | -2.51 | 0/9 | Praemisse traegt nicht (IS expR>0, IS edge>=1.0, IS usd>0), N = 1 (BASE, nur IS) |
| LL-01 Lead-Lag NQ fuehrt, ES hinkt (v2) | c-ES-NQ-Divergenz Wege-Karte | rv | nicht messbar | Dublette | – | – | – | Duplikat von 49868df2c3a4b7b0 (Friedhof-Liste, dort gemessen), erbt dessen Urteil |
| RV-08 Gap-Divergenz NQ/ES | c-Gap Wege-Karte | – | nicht messbar | Dublette | – | – | – | gleiche Messung wie WK_ESNQ_W21, erbt dessen Urteil |
| Intraday-Korrelation NQ/ES hoch/niedrig als Regime | c-ES-NQ-Divergenz Wege-Karte | – | nicht messbar | nicht gemessen | – | – | – | in #179 nicht gemessen, alte Urteile gelten unveraendert: gemessen, aber keine lauffaehigen Params: nur als Buch-Regime (AR-19, #141, ~7 Episoden) gemessen, Paar-Gate ungetestet |

⭐ = Beinahe-Treffer: besteht Walk-Forward und Buch-Stufe, scheitert an Prämisse oder Vor-Gates.

## Offene Wege der Wege-Karten (nur gelistet, nichts gebaut)

| Karte | achse | keine_story | kontrolle | offen | research_widerlegt | swing_merker | ungemessen_phantom | zurueckgehalten |
|---|---|---|---|---|---|---|---|---|
| ADX Wege-Karte | 0 | 8 | 0 | 18 | 0 | 2 | 0 | 2 |
| ADX x VWAP Wege-Karte | 0 | 5 | 2 | 25 | 0 | 1 | 0 | 0 |
| ES-NQ-Divergenz Wege-Karte | 2 | 7 | 1 | 10 | 2 | 1 | 0 | 0 |
| Fibonacci Wege-Karte | 0 | 4 | 0 | 11 | 4 | 1 | 0 | 0 |
| Gap Wege-Karte | 5 | 1 | 0 | 19 | 0 | 1 | 0 | 0 |
| Overnight-Bias ORB Wege-Karte | 0 | 1 | 1 | 22 | 0 | 2 | 1 | 0 |
| RVOL Wege-Karte | 0 | 5 | 1 | 23 | 0 | 5 | 0 | 0 |
| Rundzahlen Wege-Karte | 2 | 3 | 0 | 14 | 0 | 3 | 0 | 0 |
| Session Momentum Wege-Karte | 0 | 2 | 1 | 17 | 0 | 2 | 0 | 0 |
| VWAP-Offensive | 0 | 0 | 0 | 7 | 0 | 1 | 0 | 0 |

Einzelliste: `engine/_scratch_friedhof_v4/cands_wege_offen.json`. Auffällig: ONORB-W45a ist praktisch ungemessen (Gates `tm_pre_ret_min`/`tm_pre_rvol_min` liefern dieselben Zahlen wie ohne Gate, NaN-Verdacht) → Ticket.
