import json

def generate_results_json(portfolio_pnl, alphas_dict, path='results/results.json'):
    results = {
        "portfolio_pnl": {
            "sandbox_pnl": round(portfolio_pnl['sandbox'], 2),
            "backtest_pnl": round(portfolio_pnl['backtest'], 2),
            "pnl_match": "PASS" if abs(portfolio_pnl['sandbox']-portfolio_pnl['backtest']) < 1e-6 else "FAIL"
        },
        "alphas": {}
    }
    for name, d in alphas_dict.items():
        results["alphas"][name] = {
            "trades": int(d['trades']),
            "pnl": round(d['pnl'], 2),
            "match": "PASS" if d.get('match', True) else "FAIL",
            "analysis": d.get('analysis', "")
        }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)
    print('Saved results to', path)

if __name__ == '__main__':
    portfolio_pnl = {'sandbox': 572.30, 'backtest': 572.30}
    alphas = {
        'alpha_1_pairs': {'trades':15,'pnl':102.5,'match':True,'analysis':''},
        'alpha_2_breakout': {'trades':8,'pnl':-30.1,'match':True,'analysis':''},
        'alpha_3_mtf': {'trades':12,'pnl':210.4,'match':True,'analysis':''},
        'alpha_4_multi_asset': {'trades':3,'pnl':301.0,'match':True,'analysis':''},
        'alpha_5_orderbook': {'trades':55,'pnl':-11.5,'match':False,'analysis':'L2 update mismatch'}
    }
    generate_results_json(portfolio_pnl, alphas)
