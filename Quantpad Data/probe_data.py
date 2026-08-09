import time
import quantpad_data as qpd

one_day = 86_400_000
now = int(time.time() * 1000)
start = now - 20 * one_day

df = qpd.get_bars_with_retry("NQ.FUT", "1m", start, now, roll_adjust="none")
print("rows:", len(df))
print("index tz:", df.index.tz)
print("first:", df.index[0], "last:", df.index[-1])

et = df.tz_convert("America/New_York")
print("ET sample around open:")
day = et.index[-1].date()
mask = (et.index.date == day)
sub = et[mask].between_time("09:28", "09:50")
print(sub[["o", "h", "l", "c", "v"]].to_string())
