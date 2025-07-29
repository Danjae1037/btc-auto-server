from config import settings
from strategy import should_enter_trade
from utils import calculate_entry_price, calculate_exit_price, compound_return
from telegram_utils import send_telegram_message
from logger import log
from binance.client import Client
import datetime

def get_client():
    testnet = settings.TRADE_MODE == "testnet"
    client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET)

    if testnet:
        client.API_URL = 'https://testnet.binance.vision/api'

    return client

def run_binance_trade():
    client = get_client()
    symbol = "BTCUSDT"
    candles = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=1)
    candle = candles[0]

    open_price = float(candle[1])
    high_price = float(candle[2])

    if should_enter_trade(open_price, high_price):
        entry_price = calculate_entry_price(open_price)
        exit_price = calculate_exit_price(high_price)

        if exit_price > entry_price:
            message = f"✅ 실시간 거래 조건 충족\n진입가: {entry_price:.2f}\n매도가: {exit_price:.2f}"
            log(message)
            send_telegram_message(message)
        else:
            log("진입 조건 불충족 - 이익 없음")
    else:
        log("진입 조건 불충족")
