"""Example Optuna tuning flow for BreakoutAlpha's lookback and PairsAlpha z-threshold.
This is a template — adapt the `objective` to run your backtest function.
"""
import optuna

# placeholder backtest function — implement to call your backtester and return metric
def run_backtest_with_params(params):
    # run backtest and return final portfolio sharpe or total pnl
    return params['lookback'] * 0.1  # dummy

def objective(trial):
    lookback = trial.suggest_int('lookback', 5, 50)
    z_th = trial.suggest_float('z_th', 1.0, 3.0)
    params = {'lookback': lookback, 'z_th': z_th}
    score = run_backtest_with_params(params)
    return score

if __name__ == '__main__':
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=50)
    print('Best params', study.best_params)
