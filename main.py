import pandas as pd
from strategy import evaluate_trade_opportunity
from telegram_utils import send_telegram_message
from risk_manager import check_risk_limits

# 데이터 로드
df = pd.read_csv("data/btc_1min.csv")

initial_balance = 10000.0
balance = initial_balance
in_position = False
entry_info = {}
daily_returns = []

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

    # 위험 관리: 손실 한도 초과 시 거래 중단
    if check_risk_limits(balance, initial_balance):
        print(f"위험 관리: 거래 중단 - 현재 잔고 ${balance:.2f}")
        break

    # 일별 수익률 기록 (자정 기준)
    if index > 0:
        prev_date = df.iloc[index - 1]['timestamp'][:10]
        curr_date = df.iloc[index]['timestamp'][:10]
        if prev_date != curr_date:
            daily_returns.append((prev_date, balance))

print(f"초기 자산: ${initial_balance:.2f}, 최종 자산: ${balance:.2f}")
print(f"총 수익률: {(balance/initial_balance - 1)*100:.2f}%")

# 텔레그램으로 최종 수익률 전송
send_telegram_message(f"최종 수익률: {(balance/initial_balance - 1)*100:.2f}%, 자산: ${balance:.2f}")
