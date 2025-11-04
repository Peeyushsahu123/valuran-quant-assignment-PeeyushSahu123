"""Main orchestration: demo, backtest, sandbox-run, replay."""
import argparse
from src.event_loop import EventLoop
from src.data_handler import DataHandler
from src.execution_simulator import ExecutionSimulator
from src.portfolio import PortfolioManager
from src.utils.logger import setup_logger
from src.utils.results_generator import generate_results_json
import yaml

logger = setup_logger('main')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['demo','backtest','sandbox','replay'], default='demo')
    parser.add_argument('--data', default=None)
    parser.add_argument('--config', default='src/config.example.yaml')
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    # Created components
    dh = DataHandler(cfg.get('data', {}))
    exec_sim = ExecutionSimulator(cfg.get('execution', {}))
    portfolio = PortfolioManager(cfg.get('portfolio', {}), exec_sim)
    loop = EventLoop(dh, portfolio, exec_sim, cfg)

    if args.mode == 'demo':
        logger.info('Running demo mode: synthetic data + simple alphas')
        loop.run_demo()
    elif args.mode == 'backtest':
        logger.info('Running backtest on historical files')
        loop.run_backtest(args.data)
    elif args.mode == 'sandbox':
        logger.info('Running sandbox live connectors (make sure API keys set)')
        loop.run_sandbox()
    elif args.mode == 'replay':
        logger.info('Running replay backtest from saved market data')
        loop.run_replay(args.data)

if __name__ == '__main__':
    main()
