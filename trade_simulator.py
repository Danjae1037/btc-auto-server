import pandas as pd
from strategy import evaluate_trade_opportunity

def run_mock_trading(df=None, entry_threshold=0.0016, entry_cost_rate=0.0011, exit_slippage_rate=0.0005):
    if df is None:
        df = pd.read_csv("data/btc_1min.csv")

    balance = 10000.0
    in_position = False
    entry_info = {}
    trade_count = 0

    for index in range(len(df)):
        signals = evaluate_trade_opportunity(index, df, in_position, entry_info)

        if not in_position and 'entry' in signals:
            entry_info = signals['entry']
            in_position = True

        elif in_position and 'exit' in signals:
            exit_price = signals['exit']['exit_price']
            profit_rate = (exit_price - entry_info['entry_price']) / entry_info['entry_price']
            balance *= (1 + profit_rate)
            in_position = False
            entry_info = {}
            trade_count += 1

    return {
        'final_asset': balance,
        'return_rate': (balance / 10000.0) - 1,
        'trade_count': trade_count
    }
