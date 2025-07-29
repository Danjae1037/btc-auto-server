# config.py

from enum import Enum

class TradeMode(str, Enum):
    MOCK = "mock"          # 모의거래
    TESTNET = "testnet"    # Binance Testnet
    REAL = "real"          # 실거래 (아직 미사용)

# 기본 환경 설정
class Config:
    # 초기 자산
    INITIAL_ASSET_KRW = 1_000_000   # 모의거래용 (100만원)
    INITIAL_ASSET_USDT = 10_000     # 테스트넷/실거래용

    # 슬리피지, 수수료
    ENTRY_SLIPPAGE = 0.0005         # 0.05%
    EXIT_SLIPPAGE = 0.0005
    MAKER_FEE = 0.0002              # 0.02%
    TAKER_FEE = 0.0004              # 0.04%
    TOTAL_FEE = MAKER_FEE + TAKER_FEE

    # 전략 조건
    ENTRY_THRESHOLD = 0.0016        # 시가 대비 고가 0.16%

    # 거래 모드
    DEFAULT_MODE = TradeMode.MOCK   # 기본 모드는 모의거래

    # Telegram
    TELEGRAM_TOKEN = "7361381815:AAHMKQcQaFgK3fw9Rx1vfFsBNwQSysOZgL8"
    TELEGRAM_CHAT_ID = "8375697528"

    # 데이터 저장 경로
    SAVE_DIR = "data"               # 디렉토리: ./data/{mode}/log.csv 등
    LOG_FILE_NAME = "log.csv"

    # 자동중단 조건
    STOP_LOSS_RATIO_INIT = 0.5      # 초기 자산의 50%
    STOP_LOSS_RATIO_DAY = 0.7       # 당일 시작 자산의 70%

    # 보고 시간 (24시 기준)
    REPORT_HOUR = 0
    REPORT_MINUTE = 0
