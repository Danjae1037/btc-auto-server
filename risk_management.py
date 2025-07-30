def check_risk_limits(current_balance, initial_balance, daily_start_balance=None):
    if current_balance < initial_balance * 0.5:
        return True  # 초기 자산 대비 50% 미만
    if daily_start_balance and current_balance < daily_start_balance * 0.7:
        return True  # 당일 시작 자산 대비 70% 미만
    return False
