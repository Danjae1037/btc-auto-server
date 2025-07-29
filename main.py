# main.py

from fastapi import FastAPI, HTTPException
from trade_engine import toggle_trading, get_asset_status, reset_start_of_day_asset
from core.state import set_mode, get_current_mode
from telegram_utils import send_control_status
import threading
import uvicorn

app = FastAPI()

# 모드 변경 API (mock, testnet, live)
@app.post("/mode/{mode_name}")
def change_mode(mode_name: str):
    mode_name = mode_name.lower()
    if mode_name not in ["mock", "testnet", "live"]:
        raise HTTPException(status_code=400, detail="Invalid mode")
    set_mode(mode_name)
    send_control_status(mode_name, "모드 변경됨")
    return {"message": f"Mode changed to {mode_name}"}

# 거래 시작/중지 API
@app.post("/trade/{action}")
def trade_control(action: str):
    if action not in ["on", "off"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    toggle_trading(action == "on")
    status = "ON" if action == "on" else "OFF"
    mode = get_current_mode()
    send_control_status(mode, status)
    return {"message": f"Trading turned {status}"}

# 현재 자산 상태 조회
@app.get("/status")
def status():
    return get_asset_status()

# 매일 자정에 일일 시작 자산 초기화 (외부 스케줄러나 다른 방법으로 호출 필요)
@app.post("/reset_start_asset")
def reset_asset():
    reset_start_of_day_asset()
    return {"message": "Start of day asset reset"}

# 서버 시작 시 스케줄러 쓰레드 실행 (예: 일별 자산 초기화 등)
def run_scheduler_forever():
    import schedule
    import time

    # 매일 자정에 시작 자산 초기화
    schedule.every().day.at("00:00").do(reset_start_of_day_asset)

    while True:
        schedule.run_pending()
        time.sleep(30)

@app.on_event("startup")
def start_background_tasks():
    thread = threading.Thread(target=run_scheduler_forever, daemon=True)
    thread.start()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
