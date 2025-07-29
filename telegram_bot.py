# telegram_bot.py

import requests
from config import Config, TradeMode

def send_telegram_message(message: str, mode: TradeMode = Config.DEFAULT_MODE):
    """
    텔레그램 메시지 전송
    :param message: 보낼 메시지
    :param mode: 거래 모드(MOCK, TESTNET, REAL)
    """
    header = f"[{mode.upper()} MODE]\n"
    full_message = header + message

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": Config.TELEGRAM_CHAT_ID,
        "text": full_message
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[텔레그램 전송 실패] 코드 {response.status_code} / 응답: {response.text}")
    except Exception as e:
        print(f"[텔레그램 예외] {e}")
