import os
import csv
from datetime import datetime

BASE_DIR = "daily_summary"

def get_mode_dir(mode: str) -> str:
    dir_path = os.path.join(BASE_DIR, mode)
    os.makedirs(dir_path, exist_ok=True)
    return dir_path

def save_daily_profit(date: str, profit_percent: float, mode: str):
    """
    daily_summary/{mode}/YYYY-MM-DD.csv 형태로 저장
    """
    dir_path = get_mode_dir(mode)
    filepath = os.path.join(dir_path, f"{date}.csv")

    file_exists = os.path.isfile(filepath)
    if file_exists:
        # 중복 저장 방지
        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["date"] == date:
                    print(f"[INFO] {date} 데이터 이미 있음.")
                    return

    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "profit_percent"])
        writer.writerow([date, round(profit_percent, 4)])
    print(f"[Saved] {mode} {date} 수익률 저장됨.")
