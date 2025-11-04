"""Orderbook microstructure alpha using bid-ask imbalance.
This alpha expects tick or L2 snapshots in market_event.bars[symbol]['orderbook']
"""

class OrderbookAlpha:
    def __init__(self, params):
        self.symbol = params.get('symbol','BTC/USDT')
        self.threshold = params.get('threshold',0.6)

    def generate_signal(self, market_event):
        ts, bars = market_event.timestamp, market_event.bars
        b = bars.get(self.symbol)
        if not b:
            return None
        ob = b.get('orderbook')
        if not ob:
            return None
        bid_vol = sum([level[1] for level in ob['bids'][:5]])
        ask_vol = sum([level[1] for level in ob['asks'][:5]])
        imbalance = bid_vol / (bid_vol + ask_vol + 1e-9)
        if imbalance > self.threshold:
            return {'timestamp': ts, 'symbol': self.symbol, 'side':'BUY', 'qty':1}
        if imbalance < (1 - self.threshold):
            return {'timestamp': ts, 'symbol': self.symbol, 'side':'SELL', 'qty':1}
        return None
