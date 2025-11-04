"""Simple cross-asset rotation: rank assets by momentum and allocate.
This alpha emits signals to move allocation (simplified for assignment).
"""

class MultiAssetAlpha:
    def __init__(self, params):
        self.symbols = params.get('symbols', ['NIFTY','GOLD'])
        self.lookback = params.get('lookback', 10)
        self.history = {s:[] for s in self.symbols}

    def generate_signal(self, market_event):
        ts, bars = market_event.timestamp, market_event.bars
        for s in self.symbols:
            b = bars.get(s)
            if b:
                self.history[s].append(b['close'])
        # when we have enough, pick the best performing and send a long signal
        if any(len(self.history[s]) < self.lookback for s in self.symbols):
            return None
        returns = {s: (self.history[s][-1]/self.history[s][-self.lookback] - 1) for s in self.symbols}
        best = max(returns, key=returns.get)
        return {'timestamp': ts, 'symbol': best, 'side':'BUY', 'qty':1}
