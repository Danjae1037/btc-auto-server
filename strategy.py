def evaluate_trade_opportunity(index, df, in_position, entry_info):
    row = df.iloc[index]
    open_price = row['open']
    high_price = row['high']
    low_price = row['low']
    close_price = row['close']
    timestamp = row['timestamp']

    entry_threshold = 0.0016  # 0.16%
    entry_cost_rate = 0.0011  # 수수료 + 슬리피지 0.11%
    exit_slippage_rate = 0.0005  # 청산 슬리피지 0.05%
    stop_loss_rate = 0.003    # 손절 -0.3%
    max_hold_bars = 10        # 최대 보유 시간 (분)

    signals = {}

    if not in_position:
        if (high_price - open_price) / open_price >= entry_threshold:
            entry_price = open_price * (1 + entry_cost_rate)
            target_price = high_price * (1 - exit_slippage_rate)
            stop_loss_price = entry_price * (1 - stop_loss_rate)
            signals['entry'] = {
                'entry_price': entry_price,
                'target_price': target_price,
                'stop_loss_price': stop_loss_price,
                'entry_index': index,
                'entry_time': timestamp,
            }

    else:
        hold_duration = index - entry_info['entry_index']
        target_price = entry_info['target_price']
        stop_loss_price = entry_info['stop_loss_price']
        entry_price = entry_info['entry_price']

        if high_price >= target_price:
            signals['exit'] = {
                'exit_price': target_price,
                'reason': 'target_hit',
            }
        elif low_price <= stop_loss_price:
            signals['exit'] = {
                'exit_price': stop_loss_price,
                'reason': 'stop_loss_hit',
            }
        elif hold_duration >= max_hold_bars:
            signals['exit'] = {
                'exit_price': close_price,
                'reason': 'timeout_exit',
            }

    return signals
