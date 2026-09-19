## D1) Trial-Zahl je (mode, symbol)

| mode | NQ | ES | RTY | YM | andere | gesamt |
|---|---|---|---|---|---|---|
| tsmom | 19898 | 4428 | 9764 | 4908 | 0 | 38998 |
| maband | 9352 | 3326 | 1128 | 2600 | 0 | 16406 |
| firstbar_ematrail | 2880 | 0 | 0 | 0 | 0 | 2880 |
| ts_reversal | 851 | 87 | 5 | 88 | 0 | 1031 |
| rv | 477 | 101 | 152 | 9 | 0 | 739 |
| i2 | 244 | 109 | 85 | 109 | 0 | 547 |
| regime_gate | 419 | 0 | 111 | 0 | 0 | 530 |
| None | 82 | 82 | 0 | 0 | 358 | 522 |
| last_hour | 367 | 56 | 20 | 20 | 0 | 463 |
| gap | 116 | 29 | 225 | 27 | 0 | 397 |
| asian | 266 | 28 | 4 | 0 | 0 | 298 |
| cal | 74 | 45 | 27 | 54 | 0 | 200 |
| orb | 136 | 23 | 3 | 22 | 0 | 184 |
| vwap_pullback | 155 | 0 | 0 | 0 | 0 | 155 |
| continuation | 48 | 48 | 0 | 0 | 0 | 96 |
| vix_bias | 21 | 52 | 0 | 0 | 0 | 73 |
| pivot | 13 | 13 | 13 | 13 | 0 | 52 |
| orb_std | 45 | 0 | 0 | 0 | 0 | 45 |
| flip | 6 | 6 | 6 | 6 | 0 | 24 |
| event_study | 12 | 12 | 0 | 0 | 0 | 24 |
| prescan | 12 | 10 | 0 | 0 | 0 | 22 |
| regime_gate_subset | 16 | 0 | 4 | 0 | 0 | 20 |
| cage_daily_stop | 19 | 0 | 0 | 0 | 0 | 19 |
| reversion | 2 | 0 | 0 | 0 | 0 | 2 |

**Modi, die NIE auf einem Markt liefen:**
- NQ: (alle Modi haben Trials)
- ES: firstbar_ematrail, regime_gate, vwap_pullback, orb_std, regime_gate_subset, cage_daily_stop, reversion
- RTY: firstbar_ematrail, vwap_pullback, continuation, vix_bias, orb_std, event_study, prescan, cage_daily_stop, reversion
- YM: firstbar_ematrail, regime_gate, asian, vwap_pullback, continuation, vix_bias, orb_std, event_study, prescan, regime_gate_subset, cage_daily_stop, reversion

## D2) Param-Achsen je Modus, die NIE variiert wurden (nur 1 Wert ueber alle Trials)

**tsmom** (n=38998, 52 Param-Keys gesehen, 48 variiert, 4 konstant):
  Konstant: tm_delta_src='real'; tm_entry_delay=1; tm_on_ret_max=0.0025; tm_vix_max=16

**maband** (n=16406, 43 Param-Keys gesehen, 39 variiert, 4 konstant):
  Konstant: be_offset=0.0; mb_src='close'; mb_vwap_dnorm='atr_bar'; mb_walk_n=3

**firstbar_ematrail** (n=2880, 9 Param-Keys gesehen, 9 variiert, 0 konstant):
  Konstant: (keine)

**ts_reversal** (n=1031, 18 Param-Keys gesehen, 18 variiert, 0 konstant):
  Konstant: (keine)

**rv** (n=739, 11 Param-Keys gesehen, 10 variiert, 1 konstant):
  Konstant: rv_eod_min=385

**i2** (n=547, 23 Param-Keys gesehen, 20 variiert, 3 konstant):
  Konstant: on_hi=3.0; vp_cutoff=240; vp_min_start=45

**regime_gate** (n=530, 0 Param-Keys gesehen, 0 variiert, 0 konstant):
  Konstant: (keine)

**None** (n=522, 0 Param-Keys gesehen, 0 variiert, 0 konstant):
  Konstant: (keine)

**last_hour** (n=463, 10 Param-Keys gesehen, 10 variiert, 0 konstant):
  Konstant: (keine)

**gap** (n=397, 10 Param-Keys gesehen, 7 variiert, 3 konstant):
  Konstant: gap_atr_win=20; gap_cutoff_min=60; gap_dow='[0]'

**asian** (n=298, 15 Param-Keys gesehen, 14 variiert, 1 konstant):
  Konstant: slippage_ticks=2.0

**cal** (n=200, 6 Param-Keys gesehen, 6 variiert, 0 konstant):
  Konstant: (keine)

**orb** (n=184, 15 Param-Keys gesehen, 12 variiert, 3 konstant):
  Konstant: nr7_filter=False; orb_exec='close'; vix_ref='rel'

**vwap_pullback** (n=155, 12 Param-Keys gesehen, 12 variiert, 0 konstant):
  Konstant: (keine)

**continuation** (n=96, 5 Param-Keys gesehen, 4 variiert, 1 konstant):
  Konstant: one_trade_per_day=False

**vix_bias** (n=73, 3 Param-Keys gesehen, 3 variiert, 0 konstant):
  Konstant: (keine)

**pivot** (n=52, 4 Param-Keys gesehen, 4 variiert, 0 konstant):
  Konstant: (keine)

**orb_std** (n=45, 4 Param-Keys gesehen, 3 variiert, 1 konstant):
  Konstant: orb_entry='first_candle'

**flip** (n=24, 5 Param-Keys gesehen, 2 variiert, 3 konstant):
  Konstant: fl_be_lock_r=0.05; fl_be_trigger_r=1.0; fl_stop_atr=0.5

**event_study** (n=24, 0 Param-Keys gesehen, 0 variiert, 0 konstant):
  Konstant: (keine)

**prescan** (n=22, 8 Param-Keys gesehen, 4 variiert, 4 konstant):
  Konstant: n_offsets=5; placebo='phase_unrounded'; tick_true=True; z_edges='fine'

**regime_gate_subset** (n=20, 0 Param-Keys gesehen, 0 variiert, 0 konstant):
  Konstant: (keine)

**cage_daily_stop** (n=19, 0 Param-Keys gesehen, 0 variiert, 0 konstant):
  Konstant: (keine)

**reversion** (n=2, 5 Param-Keys gesehen, 1 variiert, 4 konstant):
  Konstant: one_trade_per_day=False; regime='range'; stop_mult=1.5; target_mult=1.0

## D3) tsmom Achsen-Verteilung
- tm_signal: signratio=5122, wins=2607, ret=2472, rangepos=173, accel=107, zscore=61, rank=55, er_ret=39, jerk=1
- tm_base: open=32808, prev_close=3704, window=426, prev_rth=181, overnight=145
- tm_exit: eod=37931, time=635, rr=406, base=22
- tm_stop_mode: range=37947, atr=664, sigma=92
- tm_dir: both=513, long_only=250, short_only=38
- tm_side: momentum=29204, fade=7773

## D4) maband Achsen-Verteilung
- mb_kind: dist=11240, channel=4085, vwap=561, slope=213, band=175, cross=83, price_ma=35, speeds=6, fan=5
- mb_vwap_anchor: session=65, hi=26, lo=26
- mb_vwap_dnorm: atr_bar=162
- mb_side: with=3806, against=803
- tm_dir: both=48, long_only=48

## D5) Long/Short-Abdeckung je Modus (Feld tm_dir: both/long_only/short_only)
- tsmom: both=513, long_only=250, short_only=38
- maband: both=48, long_only=48
- firstbar_ematrail: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- ts_reversal: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- rv: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- i2: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- regime_gate: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- None: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- last_hour: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- gap: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- asian: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- cal: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- orb: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- vwap_pullback: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- continuation: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- vix_bias: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- pivot: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- orb_std: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- flip: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- event_study: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- prescan: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- regime_gate_subset: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- cage_daily_stop: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)
- reversion: kein tm_dir-Feld in Params (Default vermutlich 'both', nie explizit getestet)

## D6) Uhrzeit-Fenster-Abdeckung
- tsmom tm_sig_start (Minuten seit 09:30) in Modus tsmom: 14 verschiedene Werte, Werte: [0, 5, 10, 15, 30, 60, 120, 150, 180, 210, 285, 300, 315, 330]
- maband mb_start_min in Modus maband: 9 verschiedene Werte, Werte: [15, 30, 45, 60, 90, 120, 180, 210, 240]
- last_hour lh_ref_min in Modus last_hour: 15 verschiedene Werte, Werte: [232.5, 247.5, 251.25, 262.5, 180, 210, 225, 240, 255, 270, 285, 300, 330, 360, 375]
- asian tr_start in Modus asian: 2 verschiedene Werte, Werte: ['09:30', '23:00']

tsmom tm_sig_start abgedeckte Werte (sortiert): [0, 5, 10, 15, 30, 60, 120, 150, 180, 210, 285, 300, 315, 330]
  ab 12:00 (>=150min seit Open) abgedeckt: [150, 180, 210, 285, 300, 315, 330]
  letzte 90 Min (>=300min seit Open, RTH~390min) abgedeckt: [300, 315, 330]