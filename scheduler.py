import schedule
import time
from report_sender import generate_and_send_daily_reports

def run_scheduler_forever():
    schedule.every().day.at("00:00").do(generate_and_send_daily_reports)
    while True:
        schedule.run_pending()
        time.sleep(30)
