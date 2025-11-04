"""Deterministic execution simulator for backtest & replay.
process_order(order, market_bar) -> returns Fill dict
send_order_to_broker(order) -> should call broker client and return the actual fill dict
"""
import time

class ExecutionSimulator:
    def __init__(self, cfg):
        self.cfg = cfg or {}
        # policy: use close price as deterministic fill price

    def process_order(self, order, market_bar):
        sym = order['symbol']
        price = market_bar.get(sym, {}).get('close', None)
        if price is None:
            return None
        qty = float(order.get('qty', 0))
        side = order.get('side')
        fill = {
            'timestamp': order['timestamp'],
            'symbol': sym,
            'qty': qty,
            'price': float(price),
            'side': side,
            'fee': 0.0,
            'exec_info': 'simulated'
        }
        return fill

    def send_order_to_broker(self, order):
        return {
            'timestamp': int(time.time()*1000),
            'symbol': order['symbol'],
            'qty': float(order.get('qty',0)),
            'price': float(order.get('price',0.0)),
            'side': order.get('side'),
            'fee': 0.0,
            'exec_info': 'sandbox-sim'
        }
