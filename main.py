from config import settings
from strategy import should_enter_trade
from trade_simulation import run_simulation
from binance_api import run_binance_trade
from telegram_utils import send_telegram_message
from risk_management import check_risk
from logger import log

def main():
    send_telegram_message("🚀 프로그램 실행됨")
    log(f"[모드: {settings.TRADE_MODE}] 자동매매 시작")

    if settings.TRADE_MODE == "simulation":
        run_simulation()

    elif settings.TRADE_MODE in ("testnet", "live"):
        if check_risk():
            run_binance_trade()
        else:
            send_telegram_message("⚠️ 위험 조건으로 자동매매 중단됨")

    else:
        log("❌ 잘못된 TRADE_MODE 설정")

if __name__ == "__main__":
    main()
