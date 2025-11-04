"""Multi-timeframe confirmation alpha (simple RSI check on 1m & 1h)
This alpha assumes DataHandler can supply multi-timeframe bars in same event.
"""
import numpy as np

class MTFAlpha:
    def __init__(self, params):
        self.symbol = params.get('symbol','ETH/USDT')
        self.short_window = params.get('short',14)
        self.long_window = params.get('long',14)
        self.history = {self.symbol:[]}

    def _rsi(self, prices, window):
        deltas = np.diff(prices)
        seed = deltas[:window]
        up = seed[seed>=0].sum()/window
        down = -seed[seed<0].sum()/window
        rs = up/down if down != 0 else np.inf
        return 100 - 100/(1+rs)

    def generate_signal(self, market_event):
        ts, bars = market_event.timestamp, market_event.bars
        bar = bars.get(self.symbol)
        if not bar:
            return None
        self.history[self.symbol].append(bar['close'])
        if len(self.history[self.symbol]) < max(self.short_window,self.long_window)+1:
            return None
        rsi_short = self._rsi(self.history[self.symbol][-self.short_window-1:], self.short_window)
        rsi_long = self._rsi(self.history[self.symbol][-self.long_window-1:], self.long_window)
        if rsi_short > 70 and rsi_long > 70:
            return {'timestamp': ts, 'symbol': self.symbol, 'side':'BUY', 'qty':1}
        if rsi_short < 30 and rsi_long < 30:
            return {'timestamp': ts, 'symbol': self.symbol, 'side':'SELL', 'qty':1}
        return None
