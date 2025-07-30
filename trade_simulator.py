from strategy import evaluate_trade_opportunity
from risk_manager import check_stop_loss

def run_mock_trading(df, initial_balance=10000):
    balance = initial_balance
    in_position = False
    entry_info = {}

    for index in range(len(df)):
        row = df.iloc[index]
        signals = evaluate_trade_opportunity(index, df, in_position, entry_info)

        if not in_position and 'entry' in signals:
            entry_info = signals['entry']
            in_position = True

        elif in_position and 'exit' in signals:
            exit_price = signals['exit']['exit_price']
            entry_price = entry_info['entry_price']
            profit_rate = (exit_price - entry_price) / entry_price
            balance *= (1 + profit_rate)
            in_position = False
            entry_info = {}

        if check_stop_loss(balance, initial_balance):
            print(f"Stop loss triggered at balance: {balance}")
            break

    return balance
