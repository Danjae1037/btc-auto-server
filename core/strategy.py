# strategy.py

from typing import Dict

FEE = 0.0006  # 0.06% (수수료)
SLIPPAGE = 0.0005  # 0.05% (슬리피지)
ENTRY_THRESHOLD = 0.0016  # 시가 대비 고가 +0.16% 이상이면 진입

def should_enter_position(open_price: float, high_price: float) -> bool:
    """
    진입 조건 판단: 고가가 시가 대비 0.16% 이상 상승했는지
    """
    return (high_price - open_price) / open_price >= ENTRY_THRESHOLD

def calculate_entry_price(open_price: float) -> float:
    """
    실제 체결되는 진입가 계산 (시가 + 수수료 + 슬리피지)
    """
    return open_price * (1 + FEE + SLIPPAGE)

def calculate_exit_price(high_price: float) -> float:
    """
    실제 체결되는 매도가 계산 (고가 - 슬리피지)
    """
    return high_price * (1 - SLIPPAGE)

def calculate_profit(entry_price: float, exit_price: float) -> float:
    """
    복리 수익률 계산 (단위: 1회 거래 기준의 수익률, 예: 0.018 == +1.8%)
    수수료 이미 반영된 진입/매도가 기준
    """
    return (exit_price / entry_price) - 1

def simulate_trade(open_price: float, high_price: float) -> Dict[str, float]:
    """
    1회의 거래를 시뮬레이션: 진입여부, 진입가, 매도가, 수익률 반환
    """
    if not should_enter_position(open_price, high_price):
        return {
            "entered": False,
            "entry_price": 0.0,
            "exit_price": 0.0,
            "profit_rate": 0.0
        }

    entry = calculate_entry_price(open_price)
    exit = calculate_exit_price(high_price)
    profit = calculate_profit(entry, exit)

    return {
        "entered": True,
        "entry_price": entry,
        "exit_price": exit,
        "profit_rate": profit
    }
