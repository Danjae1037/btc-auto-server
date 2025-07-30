import itertools
import pandas as pd
from trade_simulator import run_mock_trading
from telegram_utils import send_telegram_message

ENTRY_THRESHOLDS = [0.0010, 0.0012, 0.0014, 0.0016]
ENTRY_COST_RATES = [0.0008, 0.0010, 0.0012]
EXIT_SLIPPAGE_RATES = [0.0003, 0.0005, 0.0007]

def run_optimization():
    results = []
    for entry_th, cost_rate, slip_rate in itertools.product(ENTRY_THRESHOLDS, ENTRY_COST_RATES, EXIT_SLIPPAGE_RATES):
        res = run_mock_trading(entry_threshold=entry_th, entry_cost_rate=cost_rate, exit_slippage_rate=slip_rate)
        results.append({
            'entry_threshold': entry_th,
            'entry_cost_rate': cost_rate,
            'exit_slippage_rate': slip_rate,
            'final_asset': res['final_asset'],
            'return_rate': res['return_rate'],
        })
    df = pd.DataFrame(results)
    df.to_csv('results/optimization_results.csv', index=False)
    best = df.loc[df['final_asset'].idxmax()]
    summary = (f"📈 최적 전략 요약\n"
               f"진입 임계치: {best['entry_threshold']}\n"
               f"진입 비용률: {best['entry_cost_rate']}\n"
               f"청산 슬리피지: {best['exit_slippage_rate']}\n"
               f"최종 자산: ${best['final_asset']:.2f}\n"
               f"수익률: {best['return_rate']*100:.2f}%")
    send_telegram_message(summary)

if __name__ == "__main__":
    run_optimization()
