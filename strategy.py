def should_enter_trade(open_price, high_price):
    """
    시가 대비 고가 +0.16% 이상일 때 진입
    """
    target_ratio = 1.0016
    return high_price >= open_price * target_ratio
