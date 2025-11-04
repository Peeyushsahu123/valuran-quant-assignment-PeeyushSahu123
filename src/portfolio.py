"""Portfolio manager: manage positions, risk, and integrate alphas.
This version adds simple P&L tracking and a finish summary writer.
"""
import importlib
import json
from src.utils.logger import setup_logger

logger = setup_logger('portfolio')

class PortfolioManager:
    def __init__(self, cfg, execution_simulator):
        self.cfg = cfg or {}
        self.exec = execution_simulator
        self.alphas = []
        self.positions = {}  # symbol -> position qty
        self.cash = float(self.cfg.get('starting_cash', 100000.0))
        self.trades = []
        self.pnl_history = []
        self._load_alphas(self.cfg.get('alpha_configs', []))

    def _load_alphas(self, alpha_configs):
        for ac in alpha_configs:
            try:
                module = importlib.import_module(ac['module'])
                AlphaClass = getattr(module, ac['class'])
                self.alphas.append(AlphaClass(ac.get('params', {})))
                logger.info('Loaded alpha: %s', ac['module'])
            except Exception as e:
                logger.exception('Failed to load alpha %s: %s', ac, e)

    def on_market_event(self, market_event):
        signals = []
        # Each alpha can return zero or multiple signals
        for alpha in self.alphas:
            try:
                s = alpha.generate_signal(market_event)
                if s:
                    signals.append(s)
            except Exception as e:
                logger.exception('Alpha generate_signal error: %s', e)
        return signals

    def on_signal(self, signal):
        # create order dictionary — position sizing can be improved
        order = {
            'timestamp': signal['timestamp'],
            'symbol': signal['symbol'],
            'side': signal['side'],
            'qty': float(signal.get('qty', 1.0)),
            'type': 'MARKET'
        }
        return order

    def on_fill(self, fill):
        if fill is None:
            return
        sym = fill['symbol']
        side = fill['side']
        qty = float(fill['qty'])
        signed_qty = qty if side == 'BUY' else -qty
        # update position
        self.positions[sym] = self.positions.get(sym, 0.0) + signed_qty
        # update cash (note: SELL increases cash)
        self.cash -= fill['price'] * signed_qty
        self.trades.append(fill)
        # record instantaneous portfolio value (simplified)
        self.pnl_history.append({'timestamp': fill['timestamp'], 'cash': self.cash, 'positions': dict(self.positions)})
        logger.info('Fill processed: %s %s %s at %s', side, qty, sym, fill['price'])

    def current_portfolio_value(self, price_lookup_fn):
        # price_lookup_fn(symbol) -> latest price
        value = self.cash
        for s, q in self.positions.items():
            p = price_lookup_fn(s)
            if p is not None:
                value += q * p
        return value

    def on_finish(self):
        # Write trade summary and simple results.json-compatible summary
        total_trades = len(self.trades)
        logger.info('Portfolio finished. Total trades: %d. Cash: %.2f', total_trades, self.cash)
        summary = {
            'total_trades': total_trades,
            'cash': self.cash,
            'positions': self.positions,
            'trades': self.trades[:1000],
        }
        out = self.cfg.get('output_path', 'results/logs/portfolio_summary.json')
        try:
            os.makedirs(os.path.dirname(out), exist_ok=True)
        except Exception:
            pass
        try:
            with open(out, 'w') as f:
                json.dump(summary, f, default=str, indent=2)
            logger.info('Wrote portfolio summary to %s', out)
        except Exception as e:
            logger.exception('Failed to write portfolio summary: %s', e)
