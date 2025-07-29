from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class TradeMode(str, Enum):
    mock = "모의거래"
    testnet = "테스트넷"
    live = "실거래"

class ControlRequest(BaseModel):
    mode: TradeMode = TradeMode.mock
    trading_on: bool = False

state = {
    "mode": TradeMode.mock,
    "trading_on": False,
    "profit_rate": 0.0,
    "trade_count": 0
}

@app.get("/status")
def get_status():
    return state

@app.post("/control")
def control(req: ControlRequest):
    state["mode"] = req.mode
    state["trading_on"] = req.trading_on
    return {"message": "상태가 변경되었습니다.", "new_state": state}

@app.get("/metrics")
def get_metrics():
    return {
        "profit_rate": state["profit_rate"],
        "trade_count": state["trade_count"]
    }
