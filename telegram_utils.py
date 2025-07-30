# telegram_utils.py

import os
import requests

# Replit Secrets 또는 환경변수에서 토큰과 챗 아이디 불러오기
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str) -> bool:
    """
    텔레그램 메시지 전송 함수

    :param message: 보낼 메시지 내용
    :return: 성공 여부 (True/False)
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("텔레그램 봇 토큰 또는 챗 ID가 설정되어 있지 않습니다.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return True
        else:
            print(f"텔레그램 메시지 전송 실패: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"텔레그램 메시지 전송 중 예외 발생: {e}")
        return False
