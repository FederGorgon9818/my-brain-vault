Jobs gesamt 902; Status {'done': 474, 'premise_failed': 427, 'failed': 1}
finished-Spanne: 2026-08-18T22:36 .. 2026-09-17T01:33
Je Fehlerklasse (Job finished VOR dem Fix):
  pre_corrbook        305  (done 215, premise_failed 90)
  pre_rollgarbage     485  (done 322, premise_failed 163)
  pre_gatesfix_gen    280  (done 200, premise_failed 80)
  pre_modehole        253  (done 171, premise_failed 82)
  pre_premisefix      662  (done 394, premise_failed 268)
  pre_1555            891  (done 466, premise_failed 425)
Anzahl Klassen je Job: {0: 11, 1: 228, 2: 144, 3: 52, 4: 262, 5: 74, 6: 131}
Jobs OHNE eine der Klassen (auf aktuellem Stand): 11: hyp_FA01_NQ, hyp_GEX01_NQ, hyp_AW14c_NQ, hyp_AW15b_NQ, pbx01_stopdelay_NQ, fa01b_fastalpha_beidseitig_NQ, pbx01_stopdelay_RTY, pbx01_stopdelay_ES, gen_tsmom_combo_mom_NQ_exits_09170056, gen_tsmom_combo_mom_NQ_exits_09170057, gen_maband_combo_vwap_NQ_exits_09170057

Modus x Fehlerklasse:
  tsmom            pre_1555=354, pre_corrbook=60, pre_gatesfix_gen=66, pre_premisefix=222, pre_rollgarbage=139
  maband           pre_1555=277, pre_corrbook=51, pre_gatesfix_gen=65, pre_premisefix=181, pre_rollgarbage=121
  ts_reversal      pre_1555=69, pre_corrbook=60, pre_gatesfix_gen=56, pre_modehole=69, pre_premisefix=69, pre_rollgarbage=68
  rv               pre_1555=65, pre_corrbook=25, pre_modehole=65, pre_premisefix=65, pre_rollgarbage=35
  last_hour        pre_1555=27, pre_corrbook=27, pre_gatesfix_gen=23, pre_modehole=27, pre_premisefix=27, pre_rollgarbage=27
  gap              pre_1555=29, pre_corrbook=20, pre_gatesfix_gen=23, pre_modehole=29, pre_premisefix=29, pre_rollgarbage=28
  i2               pre_1555=26, pre_corrbook=26, pre_gatesfix_gen=25, pre_modehole=26, pre_premisefix=26, pre_rollgarbage=26
  asian            pre_1555=25, pre_corrbook=24, pre_gatesfix_gen=18, pre_modehole=25, pre_premisefix=25, pre_rollgarbage=25
  orb              pre_1555=7, pre_corrbook=7, pre_gatesfix_gen=4, pre_premisefix=7, pre_rollgarbage=7
  vix_bias         pre_1555=4, pre_corrbook=2, pre_modehole=4, pre_premisefix=4, pre_rollgarbage=4
  vwap_pullback    pre_1555=4, pre_corrbook=3, pre_modehole=4, pre_premisefix=3, pre_rollgarbage=3
  cal              pre_1555=4, pre_modehole=4, pre_premisefix=4, pre_rollgarbage=2

Jobs je Monat/Status: {('2026-08', 'done'): 329, ('2026-08', 'premise_failed'): 165, ('', 'done'): 2, ('2026-09', 'done'): 143, ('2026-09', 'premise_failed'): 262, ('2026-09', 'failed'): 1}
Jobs je Tag: :2, 2026-08-18:3, 2026-08-19:2, 2026-08-20:5, 2026-08-21:120, 2026-08-22:5, 2026-08-23:101, 2026-08-24:100, 2026-08-25:4, 2026-08-27:7, 2026-08-28:98, 2026-08-29:40, 2026-08-30:1, 2026-08-31:8, 2026-09-01:38, 2026-09-03:21, 2026-09-06:8, 2026-09-07:54, 2026-09-08:47, 2026-09-09:20, 2026-09-10:50, 2026-09-11:128, 2026-09-12:31, 2026-09-16:2, 2026-09-17:7

Jobs mit replaces_leg: 152; heutiges Buch: ['NQ_Momentum_d260818', 'NQ_LastHour_v3', 'NQ_Asia-Dir-USopen_d260820', 'NQ_VWAP-Pullback']
  Aufloesung gegen heutiges Buch: {'praefix:NQ_Momentum_d260818': 48, 'praefix:NQ_LastHour_v3': 18, 'TOT': 15, 'praefix:NQ_Asia-Dir-USopen_d260820': 17, 'exakt': 54}
  NQ_Momentum                      praefix:NQ_Momentum_d260818      48
  NQ_Momentum_d260818              exakt                            35
  NQ_LastHour                      praefix:NQ_LastHour_v3           18
  NQ_Asia-Dir-USopen               praefix:NQ_Asia-Dir-USopen_d260820 17
  RTY_Gap-fade                     TOT                              14
  NQ_VWAP-Pullback                 exakt                            10
  NQ_LastHour_v3                   exakt                            9
  NQ_ORB-fade                      TOT                              1

Ersatz-Jobs mit TOTEM Bein-Namen (15), nach Status: {'done': 14, 'premise_failed': 1}
  Kandidaten unter diesen: 0
  exit_RTY_Gap-fade                        done           fin=2026-08-18T22:42 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r1_08211925                  done           fin=2026-08-21T19:26 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r2_08211926                  done           fin=2026-08-21T19:27 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r3_08211927                  done           fin=2026-08-21T19:28 leg=RTY_Gap-fade cand=0
  gen_gap_RTY                              done           fin=2026-08-21T22:28 leg=RTY_Gap-fade cand=0
  gen_orb_break_close_NQ                   premise_failed fin=2026-08-21T22:33 leg=NQ_ORB-fade cand=None
  gen_gap_RTY_exits_08212228               done           fin=2026-08-21T22:31 leg=RTY_Gap-fade cand=0
  gapfade_retune_RTY_260824                done           fin=2026-08-24T21:26 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_exits_08242126               done           fin=2026-08-24T21:33 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r1_08242126                  done           fin=2026-08-24T21:28 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_exits_08242128               done           fin=2026-08-24T21:38 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r2_08242128                  done           fin=2026-08-24T21:31 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_exits_08242131               done           fin=2026-08-24T21:41 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_r3_08242133                  done           fin=2026-08-24T21:35 leg=RTY_Gap-fade cand=0
  gen_gap_RTY_exits_08242135               done           fin=2026-08-24T21:44 leg=RTY_Gap-fade cand=0

Doppelte IDs in queue.json: keine
results/-Dateien: 901 json, 901 meta; in Queue nicht als Datei: ['hyp_AW14c_NQ']; Dateien ohne Queue-Job: []
Status-Abweichung Queue vs meta: 0: []

Jobs mit candidates>0: 14, letzter: ('gen_asian_fade_break_NQ_r1_08212119', '2026-08-21T21:36', 2)
  exit_NQ_Momentum(2026-08-18:6), exit_NQ_Asia-Dir(2026-08-19:1), hf_NQ_Momentum_freq(2026-08-20:7), gen_asian_us_dir_NQ_r1_08211650(2026-08-21:2), gen_ts_momentum_NQ_r1_08211846(2026-08-21:1), gen_ts_momentum_NQ_r1_08211928(2026-08-21:1), gen_ts_momentum_NQ(2026-08-21:2), gen_ts_momentum_NQ_exits_08211946(2026-08-21:4), gen_ts_momentum_NQ_exits_08211951(2026-08-21:3), gen_ts_momentum_NQ_exits_08211956(2026-08-21:2), gen_ts_momentum_NQ_r3_08211958(2026-08-21:1), gen_ts_momentum_NQ_exits_08212000(2026-08-21:3), gen_ts_momentum_NQ_exits_08212114(2026-08-21:3), gen_asian_fade_break_NQ_r1_08212119(2026-08-21:2)
queue.json.bak_ap137_0909: 670 Jobs; nur im Backup (heute weg): [] (0)
queue.json.bak_ap137b4_0909: 679 Jobs; nur im Backup (heute weg): [] (0)
queue.json.bak_vwap_0911: 858 Jobs; nur im Backup (heute weg): [] (0)
registry_box.json (Snapshot 03.09.): 16667 Trials, 504 Jobs; Jobs dort, die heute nicht in queue.json sind: ['backfill:AR15_stageB_results.json (Scratchpad-Sweep, kein Kandidat ueber Familien-Null p=0.46)', 'backfill:AR17_stageA.json (Scratchpad-Sweep; Familien-Null MC p=0.130, obs_max +12.50 pp EWMA94|q70|aus_ueber)', 'backfill:AR17_va_check.json (Gegenrichtung gematcht; COVID-freie Familien-Null ueber 24 Varianten p=0.300, obs_max +7.07 pp EWMA94|q70|aus_ueber)', 'backfill:AR18', 'backfill:AR20', 'backfill:AR20subset', 'backfill:alpha_i2_results.json', 'backfill:alpha_i2b_results.json', 'backfill:amt_va_migration', 'backfill:amt_va_migration_intraday', 'backfill:asian_legs.json', 'backfill:asset_legs.json', 'backfill:cal_results.json', 'backfill:event_results.json', 'backfill:flip_window_results.json', 'backfill:freq_discovery_results.json', 'backfill:moc_vix_results.json', 'backfill:noise_orb_results.json', 'backfill:opex_mom_results.json', 'backfill:orb070_fade_results.json', 'backfill:orb070_noise_results.json', 'backfill:orb_discovery2_results.json', 'backfill:orb_honest_066_results.json', 'backfill:orb_honest_discovery_066_results.json', 'backfill:orb_inplay_068_results.json', 'backfill:orb_retest_068_results.json', 'backfill:pivot_discovery_results.json', 'backfill:rv_results.json', 'backfill:scalp_discovery_results.json', 'backfill:stageB_all100_mc.json (Scratchpad-Sweep; kein Kandidat: Familien-Null MC p=0.16, Pflichtvariante instabil: Episoden-Kippe, LOLO-Kippe 3/5, Vola-Confound)', 'backfill:tuned_legs.json']