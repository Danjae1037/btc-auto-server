# portfolio.py

import os
import json
from datetime import datetime

# 초기 자산 설정 (기본값: 10,000 USDT)
INITIAL_ASSET = 10000.0

# 손실 중단 조건
MIN_INITIAL_RATIO = 0.5   # 최초 자산의 50% 미만
MIN_DAILY_RATIO = 0.7     # 하루 시작 자산의 70% 미만

# 자산 저장 디렉토리
ASSET_DIR = "assets"
os.makedirs(ASSET_DIR, exist_ok=True)

def get_asset_path(mode: str) -> str:
    return os.path.join(ASSET_DIR, f"{mode}_asset.json")

def initialize_asset_file(mode: str):
    """
    모드별 자산 파일이 없을 경우 생성
    """
    asset_path = get_asset_path(mode)
    if not os.path.exists(asset_path):
        data = {
            "initial": INITIAL_ASSET,
            "current": INITIAL_ASSET,
            "daily_start": INITIAL_ASSET,
            "last_update": datetime.utcnow().date().isoformat()
        }
        with open(asset_path, "w") as f:
            json.dump(data, f)

def load_asset(mode: str) -> dict:
    initialize_asset_file(mode)
    with open(get_asset_path(mode), "r") as f:
        data = json.load(f)

    # 날짜가 바뀌었으면 daily_start 갱신
    today = datetime.utcnow().date().isoformat()
    if data["last_update"] != today:
        data["daily_start"] = data["current"]
        data["last_update"] = today
        with open(get_asset_path(mode), "w") as f:
            json.dump(data, f)

    return data

def save_asset(mode: str, data: dict):
    with open(get_asset_path(mode), "w") as f:
        json.dump(data, f)

def update_asset(mode: str, profit_rate: float) -> float:
    """
    복리 수익률 반영 자산 갱신
    """
    data = load_asset(mode)
    data["current"] *= (1 + profit_rate)
    data["current"] = round(data["current"], 2)
    save_asset(mode, data)
    return data["current"]

def check_stop_condition(mode: str) -> bool:
    """
    손실 중단 조건 확인
    """
    data = load_asset(mode)
    return (
        data["current"] < data["initial"] * MIN_INITIAL_RATIO or
        data["current"] < data["daily_start"] * MIN_DAILY_RATIO
    )

def reset_all_assets():
    """
    모든 모드 자산 초기화 (개발 중에만 사용)
    """
    for mode in ["mock", "testnet", "live"]:
        path = get_asset_path(mode)
        if os.path.exists(path):
            os.remove(path)
