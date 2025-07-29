import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERROR] Telegram credentials missing.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[ERROR] Telegram message failed: {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] Telegram message failed: {e}")

# 예시: 메시지 템플릿 함수들
def send_daily_summary(date: str, mode: str, start_balance: float, end_balance: float, trade_count: int):
    change = end_balance - start_balance
    rate = (change / start_balance) * 100
    message = (
        f"📅 {date} {mode} 보고\n"
        f"자산 변화: ${start_balance:,.2f} → ${end_balance:,.2f}\n"
        f"총 수익률: {rate:+.2f}%\n"
        f"총 거래 횟수: {trade_count}회"
    )
    send_telegram_message(message)

def send_stop_alert(current_balance: float):
    message = (
        f"⚠️ 거래 중단: 자산이 손실 한계 이하로 하락했습니다.\n"
        f"현재 자산: ${current_balance:,.2f}\n"
        f"자동매매가 중단되었습니다."
    )
    send_telegram_message(message)

def send_control_status(mode: str, status: str):
    message = (
        f"⚙️ 자동매매 상태 변경\n"
        f"현재 모드: {mode}\n"
        f"거래 상태: {status}"
    )
    send_telegram_message(message)
