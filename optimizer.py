import itertools
import pandas as pd
from trade_simulator import run_mock_trading
from telegram_utils import send_telegram_message
import os
from datetime import datetime

ENTRY_THRESHOLDS = [0.0010, 0.0012, 0.0014, 0.0016, 0.0018]
ENTRY_COST_RATES = [0.0010, 0.0011, 0.0012]
EXIT_SLIPPAGE_RATES = [0.0003, 0.0005, 0.0007]

DATA_FILE = 'data/btc_1min.csv'
RESULTS_DIR = 'results'

def run_optimization():
    df = pd.read_csv(DATA_FILE)
    results = []

    for entry_th, cost_rate, slip_rate in itertools.product(ENTRY_THRESHOLDS, ENTRY_COST_RATES, EXIT_SLIPPAGE_RATES):
        balance = run_mock_trading(df, initial_balance=10000)
        results.append({
            'Entry Threshold(%)': entry_th * 100,
            'Entry Cost Rate(%)': cost_rate * 100,
            'Exit Slippage(%)': slip_rate * 100,
            'Final Asset($)': balance
        })

    df_res = pd.DataFrame(results)
    df_sorted = df_res.sort_values(by='Final Asset($)', ascending=False)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_file = f"{RESULTS_DIR}/optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_sorted.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Optimization results saved to {output_file}")

    # 최고 전략 요약 텔레그램 전송
    best = df_sorted.iloc[0]
    message = (
        f"📈 [최적 전략]\n"
        f"진입 기준: 고가 ≥ 시가 × (1 + {best['Entry Threshold(%)'] / 100:.4f})\n"
        f"수수료+슬리피지: {best['Entry Cost Rate(%)'] + best['Exit Slippage(%)']:.2f}%\n"
        f"최종 자산: ${best['Final Asset($)']:.2f}"
    )
    send_telegram_message(message)

if __name__ == "__main__":
    run_optimization()
