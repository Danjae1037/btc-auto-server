import os

def calculate_entry_price(open_price):
    return open_price * 1.0011  # 수수료 0.06%, 슬리피지 0.05%

def calculate_exit_price(high_price):
    return high_price * 0.9995  # 슬리피지 -0.05%

def compound_return(balance, entry, exit):
    return balance * (exit / entry)

def get_csv_path():
    return "btc_1min_data.csv"  # 사용자가 올려야 함
