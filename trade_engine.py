# trade_engine.py

from datetime import datetime
from core.state import state, record_profit, get_current_mode
from telegram_utils import send_stop_alert
import threading

# 초기 자산 설정 (모의 거래 기준 기본 10,000달러)
INITIAL_ASSETS = {
    "mock": 10000.0,
    "testnet": 10000.0,
    "live": 10000.0,  # 실거래는 아직 테스트용 기본값
}

# 자동 거래 중지 임계값
STOP_LOSS_INITIAL_RATIO = 0.5  # 초기 자산 대비 50%
STOP_LOSS_DAILY_RATIO = 0.7    # 당일 시작 자산 대비 70%

# 상태 초기화 함수
def init_mode_state(mode: str):
    mode_key = mode.lower()
    state["mode"] = mode_key
    state.setdefault("asset", {})
    state.setdefault("start_of_day_asset", {})
    state.setdefault("trade_count", {})
    state.setdefault("trading_on", False)

    state["asset"][mode_key] = INITIAL_ASSETS.get(mode_key, 10000.0)
    state["start_of_day_asset"][mode_key] = INITIAL_ASSETS.get(mode_key, 10000.0)
    state["trade_count"][mode_key] = 0
    state["trading_on"] = False

# 거래 실행 함수
def execute_trade(profit_rate: float):
    """
    주어진 수익률(profit_rate, e.g. 0.02 = 2%)에 따라 자산을 업데이트.
    자산 손실 임계점 도달 시 자동 중단 알림을 보냄.
    """

    mode = get_current_mode()
    if not state.get("trading_on", False):
        # 거래가 꺼져 있으면 무시
        return

    current_asset = state["asset"].get(mode, INITIAL_ASSETS.get(mode, 10000.0))
    start_asset = state["start_of_day_asset"].get(mode, current_asset)

    # 자산 갱신 (복리)
    new_asset = current_asset * (1 + profit_rate)
    state["asset"][mode] = new_asset

    # 거래 횟수 증가
    state["trade_count"][mode] = state.get("trade_count", {}).get(mode, 0) + 1

    # 수익률 기록
    record_profit(profit_rate)

    # 손실 임계점 체크
    if new_asset <= INITIAL_ASSETS[mode] * STOP_LOSS_INITIAL_RATIO or new_asset <= start_asset * STOP_LOSS_DAILY_RATIO:
        # 거래 중단
        state["trading_on"] = False
        send_stop_alert(new_asset)

# 일일 시작 자산 초기화 (예: 매일 자정에 호출)
def reset_start_of_day_asset():
    mode = get_current_mode()
    current_asset = state["asset"].get(mode, INITIAL_ASSETS.get(mode, 10000.0))
    state["start_of_day_asset"][mode] = current_asset

# 거래 상태 토글 (ON/OFF)
def toggle_trading(on_off: bool):
    state["trading_on"] = on_off

# 현재 자산 상태 조회
def get_asset_status():
    mode = get_current_mode()
    return {
        "mode": mode,
        "trading_on": state.get("trading_on", False),
        "current_asset": state["asset"].get(mode, INITIAL_ASSETS.get(mode, 10000.0)),
        "start_of_day_asset": state["start_of_day_asset"].get(mode, INITIAL_ASSETS.get(mode, 10000.0)),
        "trade_count": state["trade_count"].get(mode, 0),
    }

# 초기 상태 세팅 (모든 모드)
for m in INITIAL_ASSETS.keys():
    init_mode_state(m)
