"""Event-driven loop: emits MarketEvent -> Alphas -> Signals -> Orders -> Fills.
Deterministic, synchronous processing for demo/backtest/replay.
"""
from src.utils.logger import setup_logger
from src.utils.types import MarketEvent

logger = setup_logger('event_loop')

class EventLoop:
    def __init__(self, data_handler, portfolio, execution_simulator, cfg):
        self.dh = data_handler
        self.portfolio = portfolio
        self.exec = execution_simulator
        self.cfg = cfg

    def run_demo(self):
        """Synchronous demo run using synthetic data from DataHandler.stream_demo()."""
        for ts, market_bar in self.dh.stream_demo():
            evt = MarketEvent(ts, market_bar)
            signals = self.portfolio.on_market_event(evt)
            for sig in signals:
                order = self.portfolio.on_signal(sig)
                if order:
                    fill = self.exec.process_order(order, market_bar)
                    self.portfolio.on_fill(fill)
        self.portfolio.on_finish()

    def run_backtest(self, data_path):
        """Run backtest reading historical file produced in expected format."""
        for ts, market_bar in self.dh.stream_from_file(data_path):
            evt = MarketEvent(ts, market_bar)
            signals = self.portfolio.on_market_event(evt)
            for sig in signals:
                order = self.portfolio.on_signal(sig)
                if order:
                    fill = self.exec.process_order(order, market_bar)
                    self.portfolio.on_fill(fill)
        self.portfolio.on_finish()

    def run_replay(self, data_path):
        """Replay uses same logic as backtest because DataHandler.stream_from_file yields raw events.
        Ensure the raw file is the exact market_data_raw you recorded in sandbox.
        """
        return self.run_backtest(data_path)

    def run_sandbox(self):
        """Live/sandbox streaming. DataHandler.stream_live yields live events.
        ExecutionSimulator.send_order_to_broker is used to place and log orders.
        """
        for ts, market_bar in self.dh.stream_live():
            evt = MarketEvent(ts, market_bar)
            signals = self.portfolio.on_market_event(evt)
            for sig in signals:
                order = self.portfolio.on_signal(sig)
                if order:
                    fill = self.exec.send_order_to_broker(order)
                    self.portfolio.on_fill(fill)
