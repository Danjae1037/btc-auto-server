from fastapi import FastAPI, BackgroundTasks from pydantic import BaseModel from enum import Enum import pandas as pd import json import os import datetime import csv import asyncio

app = FastAPI()

class TradeMode(str, Enum): mock = "모의거래" testnet = "테스트넷" live = "실거래"

class ControlRequest(BaseModel): mode: TradeMode = TradeMode.mock trading_on: bool = False

class ConfigRequest(BaseModel): entry_threshold: float slippage: float fee: float

CONFIG_PATH = "config.json" LOG_PATH = "trade_log.csv" INITIAL_BALANCE = 10000.0

초기 상태

state = { "mode": TradeMode.mock, "trading_on": False, "profit_rate": 0.0, "trade_count": 0, "balance": INITIAL_BALANCE, "initial_balance": INITIAL_BALANCE }

기본 설정값

config = { "entry_threshold": 0.16, "slippage": 0.05, "fee": 0.06 }

if os.path.exists(CONFIG_PATH): with open(CONFIG_PATH, 'r') as f: config.update(json.load(f))

@app.get("/") def root(): return {"message": "✅ 자동매매 서버가 정상 작동 중입니다!"}

@app.get("/status") def get_status(): return state

@app.get("/metrics") def get_metrics(): return { "profit_rate": state["profit_rate"], "trade_count": state["trade_count"], "balance": state["balance"] }

@app.post("/control") def control(req: ControlRequest, background_tasks: BackgroundTasks): state["mode"] = req.mode state["trading_on"] = req.trading_on if req.trading_on: background_tasks.add_task(run_strategy) return {"message": "상태가 변경되었습니다.", "new_state": state}

@app.get("/config") def get_config(): return config

@app.post("/config") def set_config(new_config: ConfigRequest): config.update(new_config.dict()) with open(CONFIG_PATH, 'w') as f: json.dump(config, f) return {"message": "설정이 변경되었습니다.", "new_config": config}

@app.get("/report/daily") def report_daily(): today = datetime.date.today().isoformat() rows = [] if os.path.exists(LOG_PATH): with open(LOG_PATH, newline='') as f: reader = csv.DictReader(f) rows = [r for r in reader if r['date'] == today] daily_profit = sum(float(r['profit']) for r in rows) return { "date": today, "trades": len(rows), "daily_profit": round(daily_profit, 4) }

def run_strategy(): today = datetime.date.today().strftime("%Y-%m-%d") file_path = f"/mnt/data/BTCUSDT-1m-{today}.csv" if not os.path.exists(file_path): print(f"⚠️ 데이터 파일 없음: {file_path}") return df = pd.read_csv(file_path)

trades = 0
balance = state['balance']
init_balance = balance

with open(LOG_PATH, 'a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(["date", "time", "entry_price", "exit_price", "profit", "balance"])

    for i in range(len(df)):
        row = df.iloc[i]
        open_price = float(row['Open'])
        high_price = float(row['High'])

        entry_threshold = 1 + (config['entry_threshold'] / 100)
        if high_price >= open_price * entry_threshold:
            entry_price = open_price * (1 + (config['fee'] + config['slippage']) / 100)
            exit_price = high_price * (1 - config['slippage'] / 100)
            profit_ratio = (exit_price - entry_price) / entry_price
            profit = balance * profit_ratio
            balance += profit

            writer.writerow([
                today,
                datetime.datetime.utcfromtimestamp(int(row['Timestamp'])/1000).strftime('%H:%M:%S'),
                round(entry_price, 2),
                round(exit_price, 2),
                round(profit, 4),
                round(balance, 2)
            ])

            trades += 1

            if balance < init_balance * 0.5 or balance < state['balance'] * 0.7:
                state['trading_on'] = False
                break

state['balance'] = balance
state['trade_count'] += trades
state['profit_rate'] = round((balance - state['initial_balance']) / state['initial_balance'] * 100, 2)

