import csv
from strategy import should_enter_trade
from utils import calculate_entry_price, calculate_exit_price, compound_return, get_csv_path
from telegram_utils import send_telegram_message
from logger import log

def run_simulation():
    csv_path = get_csv_path()
    initial_balance = 10000
    balance = initial_balance
    trade_count = 0

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            open_price = float(row['open'])
            high_price = float(row['high'])

            if should_enter_trade(open_price, high_price):
                entry_price = calculate_entry_price(open_price)
                exit_price = calculate_exit_price(high_price)

                if exit_price > entry_price:
                    balance = compound_return(balance, entry_price, exit_price)
                    trade_count += 1

    result = f"📈 모의거래 완료 - 총 {trade_count}회 진입\n💰 최종 자산: ${balance:.2f}"
    log(result)
    send_telegram_message(result)
