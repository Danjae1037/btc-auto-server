# main.py

import pandas as pd
from strategy import evaluate_trade_opportunity
from telegram_utils import send_telegram_message
from risk_manager import check_risk_limits
from data_loader import load_data

def main():
    df = load_data("data/btc_1min.csv")
    initial_balance = 10000.0
    balance = initial_balance
    in_position = False
    entry_info = {}
    daily_returns = []

    for index in range(len(df)):
        row = df.iloc[index]
        signals = evaluate_trade_opportunity(index, df, in_position, entry_info)

        if not in_position and 'entry' in signals:
            entry_info = signals['entry']
            entry_info['entry_index'] = index
            entry_info['entry_time'] = row['timestamp']
            in_position = True

        elif in_position and 'exit' in signals:
            exit_price = signals['exit']['exit_price']
            reason = signals['exit']['reason']
            entry_price = entry_info['entry_price']
            profit_rate = (exit_price - entry_price) / entry_price
            balance *= (1 + profit_rate)
            print(f"[{row['timestamp']}] Exit - Reason: {reason}, Profit: {profit_rate:.5%}, Balance: ${balance:.2f}")
            in_position = False
            entry_info = {}

        # 위험 관리 체크 (손실 중단 조건)
        if not check_risk_limits(balance, initial_balance):
            send_telegram_message(f"⚠️ 위험 관리 경고: 자산이 허용 범위 미만으로 내려가 거래 중단됨. 현재 자산: ${balance:.2f}")
            break

        # 일자별 수익률 기록 (자정 기준)
        if index > 0:
            prev_date = df.iloc[index - 1]['timestamp'][:10]
            curr_date = row['timestamp'][:10]
            if prev_date != curr_date:
                daily_returns.append((prev_date, balance))

    print("\n✅ 최종 결과")
    print(f"초기 자산: ${initial_balance:.2f}")
    print(f"최종 자산: ${balance:.2f}")
    print(f"총 수익률: {(balance / initial_balance - 1) * 100:.2f}%")

    if daily_returns:
        last_day, last_balance = daily_returns[-1]
        return_rate = (last_balance / initial_balance - 1) * 100
        send_telegram_message(f"[{last_day}] 일일 수익률: {return_rate:.2f}%, 자산: ${last_balance:.2f}")

if __name__ == "__main__":
    send_telegram_message("🤖 자동매매 봇 실행됨!")
    main()
