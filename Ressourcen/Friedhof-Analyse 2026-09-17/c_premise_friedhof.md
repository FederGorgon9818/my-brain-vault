premise_failed Jobs: 427, ohne meta-Datei: []
Klassen: negativ_n>=100=369, knapp_0..schwelle_(nur_09.09-Fix)=24, fehler=18, negativ_n<100=10, knapp_0..schwelle_vor_fix(?)=4, kollaps_n<min_n=1, kollaps_n<30=1

Klasse x Modus:
  tsmom            n=174  negativ_n>=100=149, knapp_0..schwelle_(nur_09.09-Fix)=14, negativ_n<100=7, knapp_0..schwelle_vor_fix(?)=4
  maband           n=166  negativ_n>=100=149, knapp_0..schwelle_(nur_09.09-Fix)=10, negativ_n<100=3, fehler=2, kollaps_n<min_n=1, kollaps_n<30=1
  rv               n= 50  negativ_n>=100=35, fehler=15
  i2               n= 12  negativ_n>=100=12
  ts_reversal      n=  6  negativ_n>=100=6
  orb              n=  5  negativ_n>=100=5
  asian            n=  5  negativ_n>=100=5
  gap              n=  3  negativ_n>=100=3
  last_hour        n=  3  negativ_n>=100=3
  cal              n=  2  negativ_n>=100=2
  vix_bias         n=  1  fehler=1

Klasse x Markt:
  ES   n=118  negativ_n>=100=103, knapp_0..schwelle_(nur_09.09-Fix)=6, negativ_n<100=4, fehler=3, knapp_0..schwelle_vor_fix(?)=2
  NQ   n=112  negativ_n>=100=94, fehler=8, knapp_0..schwelle_(nur_09.09-Fix)=6, knapp_0..schwelle_vor_fix(?)=2, negativ_n<100=1, kollaps_n<min_n=1
  RTY  n=104  negativ_n>=100=91, knapp_0..schwelle_(nur_09.09-Fix)=8, fehler=4, kollaps_n<30=1
  YM   n= 93  negativ_n>=100=81, negativ_n<100=5, knapp_0..schwelle_(nur_09.09-Fix)=4, fehler=3

Anzahl Praemissen-Configs je Job: {1: 82, 2: 227, 3: 118}

Klasse je Tag (finished):
  2026-08-20: negativ_n>=100=1
  2026-08-21: negativ_n>=100=28
  2026-08-22: negativ_n>=100=3
  2026-08-23: knapp_0..schwelle_vor_fix(?)=1, negativ_n<100=1, negativ_n>=100=29
  2026-08-24: fehler=16, negativ_n>=100=20
  2026-08-25: negativ_n>=100=1
  2026-08-27: negativ_n<100=1, negativ_n>=100=3
  2026-08-28: negativ_n>=100=37
  2026-08-29: knapp_0..schwelle_vor_fix(?)=1, negativ_n<100=4, negativ_n>=100=17
  2026-08-30: negativ_n>=100=1
  2026-08-31: negativ_n>=100=1
  2026-09-01: fehler=2, kollaps_n<30=1, kollaps_n<min_n=1, negativ_n>=100=20
  2026-09-03: negativ_n>=100=10
  2026-09-06: negativ_n>=100=7
  2026-09-07: knapp_0..schwelle_vor_fix(?)=1, negativ_n<100=2, negativ_n>=100=31
  2026-09-08: knapp_0..schwelle_vor_fix(?)=1, negativ_n>=100=27
  2026-09-09: knapp_0..schwelle_(nur_09.09-Fix)=1, negativ_n>=100=15
  2026-09-10: knapp_0..schwelle_(nur_09.09-Fix)=7, negativ_n>=100=17
  2026-09-11: knapp_0..schwelle_(nur_09.09-Fix)=11, negativ_n<100=2, negativ_n>=100=84
  2026-09-12: knapp_0..schwelle_(nur_09.09-Fix)=3, negativ_n>=100=17
  2026-09-17: knapp_0..schwelle_(nur_09.09-Fix)=2

KOLLAPS-Faelle (max n ueber alle Praemissen-Configs < min_n):
  lq01_liqprem_stretch_NQ                      maband         NQ  fin=2026-09-01 n=50 edge=-14.8 cfg=LQ01_LIQPREM_NQ|PREMISE0
  lq01_liqprem_stretch_RTY                     maband         RTY fin=2026-09-01 n=27 edge=-16.5 cfg=LQ01_LIQPREM_RTY|PREMISE0

KNAPP-Faelle (Edge 0..Schwelle, nach 09.09.):
  hyp_TA05_NQ                                  tsmom          NQ  fin=2026-08-23 n=1073 edge=0.0 expR=0.002 usd=-1973 [knapp_0..schwelle_vor_fix(?)]
  gen_tsmom_ema_ladder_fade_c1_NQ              tsmom          NQ  fin=2026-08-29 n=135 edge=0.0 expR=0.003 usd=33 [knapp_0..schwelle_vor_fix(?)]
  gen_tsmom_combo_fade_hf_ES                   tsmom          ES  fin=2026-09-07 n=241 edge=-0.0 expR=-0.004 usd=-244 [knapp_0..schwelle_vor_fix(?)]
  gen_tsmom_ema_ladder_fade_c2_hf_ES           tsmom          ES  fin=2026-09-08 n=242 edge=0.0 expR=0.002 usd=-218 [knapp_0..schwelle_vor_fix(?)]
  gen_maband_crossover_wide_tfm_YM             maband         YM  fin=2026-09-09 n=849 edge=0.6 expR=0.005 usd=1666 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_crossover_wide_atr_tfm_YM         maband         YM  fin=2026-09-10 n=849 edge=0.6 expR=0.005 usd=1666 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_combo_mom_tf_ES                    tsmom          ES  fin=2026-09-10 n=630 edge=0.5 expR=0.029 usd=-97 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_combo_mom_tf_RTY                   tsmom          RTY fin=2026-09-10 n=888 edge=0.3 expR=0.014 usd=404 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_combo_mom_atr_tf_RTY               tsmom          RTY fin=2026-09-10 n=888 edge=0.3 expR=0.014 usd=404 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c1_tf_ES            tsmom          ES  fin=2026-09-10 n=734 edge=0.7 expR=0.041 usd=402 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c2_tf_ES            tsmom          ES  fin=2026-09-10 n=664 edge=0.2 expR=0.01 usd=-647 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c2_tf_RTY           tsmom          RTY fin=2026-09-10 n=617 edge=0.7 expR=0.028 usd=564 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c3_tf_ES            tsmom          ES  fin=2026-09-11 n=636 edge=0.3 expR=0.019 usd=-387 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c3_tf_RTY           tsmom          RTY fin=2026-09-11 n=608 edge=0.9 expR=0.036 usd=660 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c4_tf_ES            tsmom          ES  fin=2026-09-11 n=630 edge=0.5 expR=0.029 usd=-97 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_mom_c4_tf_RTY           tsmom          RTY fin=2026-09-11 n=596 edge=0.6 expR=0.024 usd=370 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_vwap_gegen_NQ               maband         NQ  fin=2026-09-11 n=2552 edge=0.7 expR=0.01 usd=776 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_band_gegen_NQ               maband         NQ  fin=2026-09-11 n=2618 edge=0.7 expR=0.005 usd=8491 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_vwap_atr_gegen_NQ           maband         NQ  fin=2026-09-11 n=2552 edge=0.7 expR=0.01 usd=776 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_band_atr_gegen_NQ           maband         NQ  fin=2026-09-11 n=2618 edge=0.7 expR=0.005 usd=8491 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_combo_fade_spaet_YM                tsmom          YM  fin=2026-09-11 n=131 edge=0.8 expR=0.065 usd=45 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_tsmom_ema_ladder_fade_c1_spaet_YM        tsmom          YM  fin=2026-09-11 n=443 edge=0.6 expR=0.067 usd=220 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_vwap_spaet_NQ               maband         NQ  fin=2026-09-11 n=2565 edge=0.1 expR=0.002 usd=7463 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_band_spaet_RTY              maband         RTY fin=2026-09-12 n=2168 edge=0.3 expR=0.002 usd=1311 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_vwap_atr_spaet_NQ           maband         NQ  fin=2026-09-12 n=2565 edge=0.1 expR=0.002 usd=7463 [knapp_0..schwelle_(nur_09.09-Fix)]
  gen_maband_combo_band_atr_spaet_RTY          maband         RTY fin=2026-09-12 n=2168 edge=0.3 expR=0.002 usd=1311 [knapp_0..schwelle_(nur_09.09-Fix)]
  pbx01_stopdelay_RTY                          tsmom          RTY fin=2026-09-17 n=1127 edge=0.1 expR=0.007 usd=-1204 [knapp_0..schwelle_(nur_09.09-Fix)]
  pbx01_stopdelay_ES                           tsmom          ES  fin=2026-09-17 n=684 edge=0.6 expR=0.04 usd=-540 [knapp_0..schwelle_(nur_09.09-Fix)]

EDGE OK aber expR/usd-Gate (2. Schwelle):

FEHLER/UNBEKANNT:
  hyp_TR10_NQ                                  vix_bias       NQ  fin=2026-08-24 note=TR-10_NQ|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_ES_NQ                               rv             ES  fin=2026-08-24 note=LL01_ESNQ|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_ES_RTY                              rv             ES  fin=2026-08-24 note=LL01_ESRTY|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_ES_YM                               rv             ES  fin=2026-08-24 note=LL01/LL13_ESYM|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_NQ_ES                               rv             NQ  fin=2026-08-24 note=LL01_NQES|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_NQ_RTY                              rv             NQ  fin=2026-08-24 note=LL01_NQRTY|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_NQ_YM                               rv             NQ  fin=2026-08-24 note=LL01/LL13_NQYM|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_RTY_ES                              rv             RTY fin=2026-08-24 note=LL01_RTYES|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_RTY_NQ                              rv             RTY fin=2026-08-24 note=LL01_RTYNQ|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_RTY_YM                              rv             RTY fin=2026-08-24 note=LL01/LL13_RTYYM|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_YM_ES                               rv             YM  fin=2026-08-24 note=LL01_YMES|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_YM_NQ                               rv             YM  fin=2026-08-24 note=LL01_YMNQ|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL01_YM_RTY                              rv             YM  fin=2026-08-24 note=LL01_YMRTY|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL04_NQ_ES                               rv             NQ  fin=2026-08-24 note=LL04_NQES|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL07_NQ_ES                               rv             NQ  fin=2026-08-24 note=LL07_NQES|PREMISE0: n=0 IS expR=None edge=Nonepp
  hyp_LL14_NQ_ES                               rv             NQ  fin=2026-08-24 note=LL14_NQES|PREMISE0: n=0 IS expR=None edge=Nonepp
  fb01_failbreak_session_NQ                    maband         NQ  fin=2026-09-01 note=FB01_FAILBRK_NQ|PREMISE0: n=0 IS expR=None edge=Nonepp; FB01_FAILBRK_NQ|PREMISE1: n=0 IS expR=None edge=Nonepp
  fb01_failbreak_session_RTY                   maband         RTY fin=2026-09-01 note=FB01_FAILBRK_RTY|PREMISE0: n=0 IS expR=None edge=Nonepp; FB01_FAILBRK_RTY|PREMISE1: n=0 IS expR=None edge=Nonepp

NEGATIV, aber nur leicht (Edge -1..0 pp, n>=100) -- Rauschen-Kandidaten:
  hf_revfade_YM                                ts_reversal    YM  n=443 edge=-0.9 expR=-0.039 usd=1017
  gen_i2_volbrk_ES                             i2             ES  n=1540 edge=-0.6 expR=-0.018 usd=-1598
  gen_i2_vwap_pull_RTY                         i2             RTY n=787 edge=-0.3 expR=-0.003 usd=-618
  gen_i2_on_rev_RTY                            i2             RTY n=1003 edge=-0.2 expR=-0.002 usd=-1722
  gen_asian_us_dir_RTY                         asian          RTY n=968 edge=-0.9 expR=-0.034 usd=598
  hyp_TA10_NQ                                  tsmom          NQ  n=1415 edge=-0.5 expR=-0.012 usd=-664
  hyp_TN03_NQ                                  tsmom          NQ  n=1547 edge=-0.7 expR=-0.015 usd=-5498
  hyp_AV02_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AV10_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AV14_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AC04_NQ                                  maband         NQ  n=2698 edge=-0.8 expR=-0.015 usd=-1607
  hyp_AC07_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AC11_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AC16_NQ                                  maband         NQ  n=2050 edge=-0.4 expR=-0.005 usd=-3548
  hyp_AS01_NQ                                  maband         NQ  n=2698 edge=-0.5 expR=-0.01 usd=2451
  hyp_AB01_NQ                                  maband         NQ  n=2460 edge=-0.1 expR=-0.001 usd=3823
  hyp_AW02_NQ                                  maband         NQ  n=2676 edge=-0.6 expR=-0.01 usd=6130
  hyp_AW11_NQ                                  maband         NQ  n=2676 edge=-0.6 expR=-0.01 usd=6130
  hyp_AW14_NQ                                  maband         NQ  n=2676 edge=-1.0 expR=-0.009 usd=1245
  hyp_AK03_NQ                                  maband         NQ  n=2648 edge=-0.4 expR=-0.003 usd=-2498
  hyp_AB11_NQ                                  maband         NQ  n=2460 edge=-0.1 expR=-0.001 usd=3823
  hyp_CE04_ES                                  cal            ES  n=126 edge=-1.0 expR=-0.014 usd=230
  hyp_LD02_NQ                                  maband         NQ  n=2699 edge=-1.0 expR=-0.015 usd=2662
  gen_tsmom_combo_fade_NQ                      tsmom          NQ  n=309 edge=-0.1 expR=-0.002 usd=1828
  gen_tsmom_combo_fade_YM                      tsmom          YM  n=448 edge=-0.9 expR=-0.039 usd=1017
  gen_maband_combo_vwap_NQ                     maband         NQ  n=2699 edge=-1.0 expR=-0.015 usd=2662
  gen_tsmom_combo_prevclose_YM                 tsmom          YM  n=1399 edge=-0.5 expR=-0.027 usd=-918
  gen_tsmom_combo_fade_atr_NQ                  tsmom          NQ  n=101 edge=-0.1 expR=-0.005 usd=974
  gen_tsmom_combo_fade_atr_YM                  tsmom          YM  n=448 edge=-0.9 expR=-0.039 usd=1017
  gen_maband_combo_vwap_atr_NQ                 maband         NQ  n=2699 edge=-1.0 expR=-0.015 usd=2662
  gen_tsmom_combo_prevclose_atr_YM             tsmom          YM  n=1399 edge=-0.5 expR=-0.027 usd=-918
  gen_tsmom_ema_ladder_fade_c2_NQ              tsmom          NQ  n=216 edge=-0.6 expR=-0.031 usd=236
  gen_tsmom_ema_ladder_fade_c3_NQ              tsmom          NQ  n=216 edge=-0.5 expR=-0.025 usd=419
  hyp_LL01_YM_NQ_v2                            rv             YM  n=172 edge=-1.0 expR=-0.017 usd=-31
  gen_maband_combo_vwap_mt_NQ                  maband         NQ  n=3318 edge=-0.4 expR=-0.006 usd=8023
  gen_maband_combo_channel_mt_RTY              maband         RTY n=2217 edge=-0.8 expR=-0.008 usd=-863
  gen_maband_combo_vwap_atr_mt_NQ              maband         NQ  n=3318 edge=-0.4 expR=-0.006 usd=8023
  gen_maband_combo_channel_atr_mt_RTY          maband         RTY n=2217 edge=-0.8 expR=-0.008 usd=-863
  gen_tsmom_combo_prevclose_hf_RTY             tsmom          RTY n=1862 edge=-0.4 expR=-0.032 usd=-55
  gen_tsmom_combo_prevclose_hf_YM              tsmom          YM  n=1856 edge=-0.3 expR=-0.03 usd=-444
  gen_tsmom_combo_prevclose_atr_hf_RTY         tsmom          RTY n=1862 edge=-0.4 expR=-0.032 usd=-55
  gen_tsmom_combo_prevclose_atr_hf_YM          tsmom          YM  n=1856 edge=-0.3 expR=-0.03 usd=-444
  gen_tsmom_ema_ladder_mom_c3_hf_YM            tsmom          YM  n=533 edge=-1.0 expR=-0.094 usd=-1059
  gen_tsmom_ema_ladder_fade_c1_hf_RTY          tsmom          RTY n=398 edge=-0.6 expR=-0.05 usd=114
  gen_tsmom_ema_ladder_fade_c2_hf_RTY          tsmom          RTY n=410 edge=-0.5 expR=-0.041 usd=-17
  gen_tsmom_ema_ladder_fade_c3_hf_ES           tsmom          ES  n=240 edge=-0.4 expR=-0.037 usd=-327
  gen_maband_combo_vwap_tfm_NQ                 maband         NQ  n=2721 edge=-0.3 expR=-0.004 usd=5834
  gen_maband_combo_channel_tfm_ES              maband         ES  n=2704 edge=-0.7 expR=-0.01 usd=2543
  gen_maband_combo_channel_tfm_RTY             maband         RTY n=2264 edge=-0.6 expR=-0.007 usd=-1269
  gen_maband_combo_band_tfm_NQ                 maband         NQ  n=2722 edge=-1.0 expR=-0.009 usd=-8829
  gen_maband_combo_band_tfm_RTY                maband         RTY n=2205 edge=-0.7 expR=-0.006 usd=1047
  gen_maband_combo_vwap_atr_tfm_NQ             maband         NQ  n=2721 edge=-0.3 expR=-0.004 usd=5834
  gen_maband_combo_channel_atr_tfm_ES          maband         ES  n=2704 edge=-0.7 expR=-0.01 usd=2543
  gen_maband_combo_channel_atr_tfm_RTY         maband         RTY n=2264 edge=-0.6 expR=-0.007 usd=-1269
  gen_maband_combo_band_atr_tfm_NQ             maband         NQ  n=2722 edge=-1.0 expR=-0.009 usd=-8829
  gen_maband_combo_band_atr_tfm_RTY            maband         RTY n=2205 edge=-0.7 expR=-0.006 usd=1047
  gen_tsmom_combo_fade_tf_ES                   tsmom          ES  n=277 edge=-0.3 expR=-0.011 usd=-64
  gen_tsmom_combo_prevclose_tf_ES              tsmom          ES  n=673 edge=-0.4 expR=-0.019 usd=-828
  gen_tsmom_combo_prevclose_atr_tf_ES          tsmom          ES  n=673 edge=-0.4 expR=-0.019 usd=-828
  gen_tsmom_ema_ladder_fade_c1_tf_ES           tsmom          ES  n=250 edge=-1.0 expR=-0.046 usd=786
  gen_maband_combo_band_gegen_YM               maband         YM  n=2629 edge=-0.4 expR=-0.003 usd=800
  gen_maband_combo_band_atr_gegen_YM           maband         YM  n=2629 edge=-0.4 expR=-0.003 usd=800
  gen_tsmom_combo_fade_spaet_NQ                tsmom          NQ  n=571 edge=-0.1 expR=-0.007 usd=-193
  gen_tsmom_combo_fade_spaet_ES                tsmom          ES  n=503 edge=-0.2 expR=-0.012 usd=275
  gen_tsmom_ema_ladder_fade_c1_spaet_NQ        tsmom          NQ  n=579 edge=-0.7 expR=-0.066 usd=-432
  gen_maband_combo_vwap_spaet_RTY              maband         RTY n=2144 edge=-1.0 expR=-0.011 usd=-1269
  gen_maband_combo_vwap_atr_spaet_RTY          maband         RTY n=2144 edge=-1.0 expR=-0.011 usd=-1269