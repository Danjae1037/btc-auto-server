def evaluate_trade_opportunity(index, df, in_position, entry_info):
    row = df.iloc[index]
    open_price = row['open']
    high_price = row['high']
    low_price = row['low']

    entry_threshold = 0.0016
    slippage_entry = 0.0011
    slippage_exit = 0.0005
    stop_loss_rate = 0.003
    max_hold_bars = 10

    signals = {}

    if not in_position:
        if (high_price - open_price) / open_price >= entry_threshold:
            signals['entry'] = {
                'entry_price': open_price * (1 + slippage_entry),
                'target_price': high_price * (1 - slippage_exit),
                'stop_loss_price': open_price * (1 + slippage_entry) * (1 - stop_loss_rate),
                'entry_index': index,
                'entry_time': row['timestamp'],
            }
    else:
        hold_duration = index - entry_info['entry_index']
        if high_price >= entry_info['target_price']:
            signals['exit'] = {'exit_price': entry_info['target_price'], 'reason': 'target_hit'}
        elif low_price <= entry_info['stop_loss_price']:
            signals['exit'] = {'exit_price': entry_info['stop_loss_price'], 'reason': 'stop_loss_hit'}
        elif hold_duration >= max_hold_bars:
            signals['exit'] = {'exit_price': row['close'], 'reason': 'timeout_exit'}

    return signals
