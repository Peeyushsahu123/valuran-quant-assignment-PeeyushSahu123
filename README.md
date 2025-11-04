# Valuran Quant Assignment — Track A (Full-Stack Quant)

my repository contains a full implementation scaffold for the Valuran multi-asset, multi-timeframe quantitative portfolio system (Track A). It includes:

- Event-driven engine
- Multi-timeframe DataHandler
- 5 example alphas
- Portfolio manager
- Deterministic execution simulator
- Logging and results generator
- HPT (Optuna) and WFO example scripts

##  start

1. Create virtualenv and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure `config.yaml` (see `src/config.example.yaml` for parameters).

3. Run a unit test-style demo (simulated data):

```bash
python src/main.py --mode demo
```

4. To run a backtest replay using saved market data:

```bash
python src/main.py --mode replay --data results/logs/market_data_raw.parquet
```

5. To generate `results.json` after backtest + sandbox logs:

```bash
python src/utils/results_generator.py --sandbox results/logs/sandbox_summary.json --backtest results/logs/backtest_summary.json
```

## Deliverables
- `results/results.json`
- `report.pdf` (rendered from `docs/report_outline.md`)

