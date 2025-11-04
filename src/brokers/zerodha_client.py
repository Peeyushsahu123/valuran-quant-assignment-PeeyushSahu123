# Zerodha Kite adapter stub. For the assignment i provide a mock implementation using CSV files.
class ZerodhaClient:
    def __init__(self, cfg):
        self.cfg = cfg

    def place_order(self, symbol, side, qty, price=None, order_type='MARKET'):
        # Mock: immediately return a fill
        return {'symbol':symbol,'side':side,'qty':qty,'price':price or 0.0,'status':'FILLED'}
