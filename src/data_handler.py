"""Multi-symbol, multi-timeframe data handler.
Provides stream_demo(), stream_from_file(), and a simple live-socket placeholder which can be connected to a broker adapter.
All timestamps are returned as UTC epoch milliseconds (int).
"""
import pandas as pd
import numpy as np
import pytz

class DataHandler:
    def __init__(self, cfg):
        self.cfg = cfg or {}
        self.timezone = pytz.UTC
        # default symbols if not provided
        self.symbols = self.cfg.get('symbols', ['BTC/USDT','ETH/USDT'])

    def stream_demo(self):
        rng = np.random.default_rng(0)
        t0 = pd.Timestamp('2023-01-01T00:00:00Z')
        for i in range(200):
            ts = t0 + pd.Timedelta(minutes=i)
            bars = {}
            for s in self.symbols:
                price = 30000 + rng.normal(0, 100) + i*2 if 'BTC' in s else 2000 + rng.normal(0,10) + i*0.1
                bars[s] = {'open':price*0.999,'high':price*1.001,'low':price*0.998,'close':float(price),'volume':int(rng.integers(1,100))}
            yield int(ts.value//10**6), bars

    def stream_from_file(self, path):
        # Reads a CSV or parquet with columns: timestamp (ISO or epoch), symbol, open, high, low, close, volume
        if path.endswith('.parquet'):
            df = pd.read_parquet(path)
        else:
            df = pd.read_csv(path)
        # ensure timestamp is timezone-aware UTC
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        df = df.sort_values('timestamp')
        grouped = df.groupby('timestamp')
        for ts, g in grouped:
            bars = {}
            for _, row in g.iterrows():
                bars[row['symbol']] = {'open':float(row['open']),'high':float(row['high']),'low':float(row['low']),'close':float(row['close']),'volume':float(row.get('volume',0))}
            yield int(pd.Timestamp(ts).value//10**6), bars

    def stream_live(self):
        # Minimal placeholder to integrate with broker websockets.
        # For the purposes of this assignment scaffolding it simply raises NotImplementedError.
        raise NotImplementedError('Connect this to your broker websocket / streaming adapter to stream live data.')
