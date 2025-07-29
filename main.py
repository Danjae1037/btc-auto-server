from fastapi import FastAPI
import threading
from scheduler import run_scheduler_forever
from core.trade_engine import get_asset_status, toggle_trading
from utils.telegram_utils import send_control_status

app = FastAPI()

@app.on_event("startup")
def start_scheduler():
    thread = threading.Thread(target=run_scheduler_forever, daemon=True)
    thread.start()

@app.get("/status")
def status():
    return get_asset_status()

@app.post("/control/{action}")
def control(action: str, mode: str):
    if action.lower() == "start":
        toggle_trading(True)
        send_control_status(mode, "ON")
        return {"message": "Trading started"}
    elif action.lower() == "stop":
        toggle_trading(False)
        send_control_status(mode, "OFF")
        return {"message": "Trading stopped"}
    else:
        return {"error": "Unknown action"}
