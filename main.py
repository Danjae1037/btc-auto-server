import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from trade_engine import (
    toggle_trading,
    init_mode_state,
    get_asset_status,
    execute_trade,
    reset_start_of_day_asset,
)
from data_loader import load_price_data
from core.state import state
from utils import save_summary_to_csv
from telegram_utils import send_daily_summary
import schedule
import time
import threading

app = FastAPI()

# ======== API 모델 정의 ========
class TradingControlRequest(BaseModel):
    trading_on: bool

class ModeChangeRequest(BaseModel):
    mode: str

# ======== FastAPI 라우터 ========
@app.post("/control/trading")
def control_trading(req: TradingControlRequest):
    toggle_trading(req.trading_on)
    return {"message": f"Trading {'started' if req.trading_on else 'stopped'}."}

@app.post("/control/mode")
def control_mode(req: ModeChangeRequest):
    mode = req.mode.lower()
    if mode not in ["mock", "testnet", "live"]:
        raise HTTPException(status_code=400, detail="Invalid mode")
    init_mode_state(mode)
    state["mode"] = mode
    return {"message": f"Mode changed to {mode}."}

@app.get("/status")
def get_status():
    return get_asset_status()

# ======== 전략 실행 함수 ========
def run_backtest_strategy():
    df = load_price_data()
    for i in range(len(df)):
        row = df.iloc[i]
        open_price = row["open"]
        high_price = row["high"]

        # 전략 조건: 시가 대비 고가 +0.16% 이상이면 진입
        if (high_price - open_price) / open_price >= 0.0016:
            # 진입가: 시가 + 수수료(0.06%) + 슬리피지(0.05%) = 총 0.11%
            entry_price = open_price * 1.0011
            # 매도가: 고가 - 슬리피지(0.05%)
            exit_price = high_price * 0.9995
            profit_rate = (exit_price - entry_price) / entry_price
            execute_trade(profit_rate)

# ======== 스케줄러 스레드 ========
def start_scheduler():
    schedule.every().day.at("00:00").do(reset_start_of_day_asset)
    schedule.every().day.at("00:05").do(lambda: save_summary_to_csv(get_current_mode()))
    schedule.every().day.at("00:10").do(lambda: send_daily_summary(get_current_mode()))

    while True:
        schedule.run_pending()
        time.sleep(1)

# ======== 앱 실행 함수 ========
if __name__ == "__main__":
    # 기본 모드 초기화
    init_mode_state("mock")

    # 스케줄러 시작
    threading.Thread(target=start_scheduler, daemon=True).start()

    # 전략 실행 (1회성 백테스트로 테스트 중)
    run_backtest_strategy()

    # FastAPI 서버 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)
