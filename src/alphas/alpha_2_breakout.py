"""Breakout momentum alpha: entry when price breaks moving high"""
import pandas as pd

class BreakoutAlpha:
    def __init__(self, params):
        self.lookback = params.get('lookback', 20)
        self.symbol = params.get('symbol','BTC/USDT')
        self.prices = []

    def generate_signal(self, market_event):
        ts, bars = market_event.timestamp, market_event.bars
        bar = bars.get(self.symbol)
        if not bar:
            return None
        self.prices.append(bar['close'])
        if len(self.prices) < self.lookback:
            return None
        high = max(self.prices[-self.lookback:])
        if bar['close'] > high:
            return {'timestamp': ts, 'symbol': self.symbol, 'side':'BUY', 'qty':1}
        return None
