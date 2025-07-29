from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
import pandas as pd

app = FastAPI()

# 거래 모드
class TradeMode(str, Enum):
    mock = "모의거래"
    testnet = "테스트넷"
    live = "실거래"

# 제어 요청 모델
class ControlRequest(BaseModel):
    mode: TradeMode = TradeMode.mock
    trading_on: bool = False

# 서버 상태 저장
state = {
    "mode": TradeMode.mock,
    "trading_on": False,
    "csv_path": "/mnt/data/BTCUSDT-1m-2025-07-01.csv",  # 수동 지정 (예시)
    "initial_asset": 10000.0,
    "current_asset": 10000.0,
    "profit_rate": 0.0,
    "trade_count": 0
}

@app.get("/")
def root():
    return {"message": "✅ 자동매매 서버가 정상 작동 중입니다!"}

@app.get("/status")
def get_status():
    return state

@app.post("/control")
def control(req: ControlRequest):
    state["mode"] = req.mode
    state["trading_on"] = req.trading_on
    if req.trading_on and req.mode == TradeMode.mock:
        run_mock_strategy()
    return {
        "message": "상태가 변경되었습니다.",
        "new_state": state
    }

@app.get("/metrics")
def get_metrics():
    return {
        "profit_rate": state["profit_rate"],
        "trade_count": state["trade_count"],
        "current_asset": state["current_asset"]
    }

# 전략 실행 함수
def run_mock_strategy():
    try:
        df = pd.read_csv(
            state["csv_path"],
            header=None,
            names=[
                "Timestamp", "Open", "High", "Low", "Close", "Volume",
                "Close Time", "Quote Volume", "Num Trades",
                "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
            ]
        )

        asset = state["initial_asset"]
        trade_count = 0

        for _, row in df.iterrows():
            open_price = float(row["Open"])
            high_price = float(row["High"])

            # 진입 조건: 시가 대비 고가가 +0.16% 이상
            if high_price >= open_price * 1.0016:
                entry_price = open_price * 1.0011   # 진입가: 수수료(0.06%) + 슬리피지(0.05%)
                exit_price  = high_price * 0.9995    # 매도가: 고가에서 슬리피지(0.05%) 차감

                profit = (exit_price - entry_price) / entry_price
                asset *= (1 + profit)
                trade_count += 1

        state["current_asset"] = round(asset, 2)
        state["profit_rate"]   = round((asset / state["initial_asset"] - 1) * 100, 4)
        state["trade_count"]   = trade_count
        state["trading_on"]    = False

    except Exception as e:
        state["trading_on"] = False
        print("전략 실행 오류:", e)
