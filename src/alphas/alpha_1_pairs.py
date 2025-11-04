"""Pairs mean-reversion alpha using z-score of spread."""
import pandas as pd

class PairsAlpha:
    def __init__(self, params):
        self.window = params.get('window', 24)
        self.pair = params.get('pair', ['BTC/USDT','ETH/USDT'])
        self.history = {self.pair[0]:[], self.pair[1]:[]}

    def generate_signal(self, market_event):
        ts, bars = market_event.timestamp, market_event.bars
        s0 = bars.get(self.pair[0])
        s1 = bars.get(self.pair[1])
        if not s0 or not s1:
            return None
        p0, p1 = s0['close'], s1['close']
        self.history[self.pair[0]].append(p0)
        self.history[self.pair[1]].append(p1)
        if len(self.history[self.pair[0]]) < self.window:
            return None
        spread = pd.Series(self.history[self.pair[0]]) - pd.Series(self.history[self.pair[1]])
        z = (spread.iloc[-1] - spread.mean()) / spread.std()
        if z > 2.0:
            # short spread: sell p0, buy p1
            return {'timestamp': ts, 'symbol': self.pair[0], 'side':'SELL', 'qty':1}
        if z < -2.0:
            return {'timestamp': ts, 'symbol': self.pair[0], 'side':'BUY', 'qty':1}
        return None
