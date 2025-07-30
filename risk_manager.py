def check_stop_loss(current_balance, initial_balance):
    # 초기 자산 50% 미만이거나 당일 시작 대비 70% 미만일 경우 True 반환하여 거래 중단 권고
    if current_balance <= initial_balance * 0.5:
        return True
    # 당일 시작 대비 70% 미만 체크는 별도로 관리 필요 (예: 하루 시작 잔고 기준 추가 구현)
    return False
