"""Unit-Check run_funded_fn_x (fix/theta/lock_first) an Hand-Pfaden. Nur Lesen, nichts im Engine-Ordner."""
import sys, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-user-my-brain-vault/2b0199f9-58f2-5493-a89c-c32d14a7695f/scratchpad")
import fn_tempo_check as F

def run(seq, **kw):
    dc = np.array(seq, float); dw = np.minimum(dc, 0.0)
    paths = np.arange(len(dc))[None, :]
    r = F.run_funded_fn_x(paths, dc, dw, dd=4000, cap=4000, bench=250, k=1, max_pays=4, **kw)
    fl = r["flow"][0]; t = np.flatnonzero(fl > 0)
    return [(int(i)+1, round(fl[i]/0.95, 1)) for i in t], bool(r["ruin"][0]), int(r["npay"][0])

# 1) konstanter Gewinn 300/Tag: fix=False zahlt aus dem Polster, fix=True nur Zyklusgewinn
seq = [300.0]*120
print("A (alt)  :", run(seq))
print("C (fix)  :", run(seq, fix=True))
print("D (fix,th1,lock):", run(seq, fix=True, theta=1.0, lock_first=True))
# 2) Zyklus mit Verlust nach Auszahlung: 5x300 -> Payout, dann -400, dann 5x150 (<bench) -> darf nicht zahlen
seq2 = [300.0]*5 + [-400.0] + [150.0]*10 + [260.0]*5
print("A seq2   :", run(seq2))
print("C seq2   :", run(seq2, fix=True))
