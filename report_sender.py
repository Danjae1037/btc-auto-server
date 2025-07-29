import os
import datetime
from utils.telegram_utils import send_telegram_message
from summary_utils import save_daily_profit

def generate_and_send_daily_reports():
    today = datetime.date.today()
    date_str = today.isoformat()

    for mode in ["mock", "testnet", "live"]:
        # TODO: 수익률 계산 로직 필요
        # 임시 수익률 데이터 예시 (10,000 기준 1.5% 수익)
        start_balance = 10000.0
        end_balance = 10000.0 * 1.015
        trade_count = 5

        profit_pct = ((end_balance - start_balance) / start_balance) * 100
        save_daily_profit(date_str, profit_pct, mode)

        message = (
            f"📅 {date_str} [{mode.upper()}] 일일 수익률 보고\n"
            f"자산 변화: ${start_balance:,.2f} → ${end_balance:,.2f}\n"
            f"총 수익률: {profit_pct:+.2f}%\n"
            f"총 거래 횟수: {trade_count}회"
        )
        send_telegram_message(message)
