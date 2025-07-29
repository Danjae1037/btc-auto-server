from logger import log

# 시뮬레이션이 아닌 경우엔 실제 위험 조건 판단 추가 필요
def check_risk():
    # 예시: 항상 통과
    log("✅ 위험 조건 검사 통과")
    return True
