state = {
    "mode": "mock",
    "asset": {"mock": 10000.0, "testnet": 10000.0, "live": 10000.0},
    "start_of_day_asset": {"mock": 10000.0, "testnet": 10000.0, "live": 10000.0},
    "trade_count": {"mock": 0, "testnet": 0, "live": 0},
    "trading_on": False,
}

def get_current_mode():
    return state["mode"]

def record_profit(profit_rate):
    # 여기에 수익률 기록 로직 추가 가능
    pass
