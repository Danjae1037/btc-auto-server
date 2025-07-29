from core.state import state, record_profit, get_current_mode
from utils.telegram_utils import send_stop_alert

INITIAL_ASSETS = {"mock": 10000.0, "testnet": 10000.0, "live": 10000.0}
STOP_LOSS_INITIAL_RATIO = 0.5
STOP_LOSS_DAILY_RATIO = 0.7

def execute_trade(profit_rate: float):
    mode = get_current_mode()
    if not state.get("trading_on", False):
        return
    current_asset = state["asset"].get(mode, INITIAL_ASSETS[mode])
    start_asset = state["start_of_day_asset"].get(mode, current_asset)

    new_asset = current_asset * (1 + profit_rate)
    state["asset"][mode] = new_asset
    state["trade_count"][mode] = state["trade_count"].get(mode, 0) + 1

    record_profit(profit_rate)

    if new_asset <= INITIAL_ASSETS[mode] * STOP_LOSS_INITIAL_RATIO or new_asset <= start_asset * STOP_LOSS_DAILY_RATIO:
        state["trading_on"] = False
        send_stop_alert(new_asset)

def toggle_trading(on_off: bool):
    state["trading_on"] = on_off

def reset_start_of_day_asset():
    mode = get_current_mode()
    current_asset = state["asset"].get(mode, INITIAL_ASSETS[mode])
    state["start_of_day_asset"][mode] = current_asset

def get_asset_status():
    mode = get_current_mode()
    return {
        "mode": mode,
        "trading_on": state.get("trading_on", False),
        "current_asset": state["asset"].get(mode, INITIAL_ASSETS[mode]),
        "start_of_day_asset": state["start_of_day_asset"].get(mode, INITIAL_ASSETS[mode]),
        "trade_count": state["trade_count"].get(mode, 0),
    }
