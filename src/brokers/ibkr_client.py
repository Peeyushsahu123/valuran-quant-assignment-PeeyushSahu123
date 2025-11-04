# IBKR adapter stub using ib_insync. Requires IB Gateway running (paper) for real sandbox runs.
from ib_insync import IB

class IBClient:
    def __init__(self, cfg):
        self.cfg = cfg
        self.ib = IB()
        self.ib.connect(cfg.get('host','127.0.0.1'), int(cfg.get('port',7497)), clientId=1)

    def place_order(self, contract, order):
        trade = self.ib.placeOrder(contract, order)
        return trade

    def fetch_historical(self, contract, duration, barSize):
        bars = self.ib.reqHistoricalData(contract, endDateTime='', durationStr=duration, barSizeSetting=barSize, whatToShow='TRADES')
        return bars
