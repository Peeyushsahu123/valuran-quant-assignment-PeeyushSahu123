# Minimal Binance testnet adapter using ccxt. Fill in API keys in config.yaml
import ccxt

class BinanceClient:
    def __init__(self, cfg):
        self.cfg = cfg
        self.exchange = ccxt.binance({
            'apiKey': cfg.get('apiKey'),
            'secret': cfg.get('secret'),
            'enableRateLimit': True,
            'options': {'defaultType': 'future'}
        })
        # For testnet:
        if cfg.get('testnet'):
            self.exchange.set_sandbox_mode(True)

    def place_order(self, symbol, side, qty, price=None, order_type='MARKET'):
        if order_type == 'MARKET':
            return self.exchange.create_market_order(symbol, side, qty)
        else:
            return self.exchange.create_limit_order(symbol, side, qty, price)

    def fetch_order_book(self, symbol, limit=50):
        return self.exchange.fetch_order_book(symbol, limit)

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=1000):
        return self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)
