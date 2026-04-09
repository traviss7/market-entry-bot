#!/usr/bin/env python3
# main.py
"""
국장 진입 시점 모니터링 봇

진입 조건 (3개 중 2개 충족 시):
1. 브렌트유 $95↓ + 3일 유지
2. VIX 20↓ + 하락 추세  
3. 지수 박스 상단 돌파 + 유지
"""

from indicators import check_brent_condition, check_vix_condition, check_kospi_box_breakout
from notifier import send_telegram, format_entry_signal
from config import MIN_CONDITIONS


def main():
    print("=" * 50)
    print("📊 국장 진입 조건 체크 중...")
    print("=" * 50)
    
    # 각 조건 체크
    brent = check_brent_condition()
    print(f"\n[브렌트유] {brent['message']}")
    
    vix = check_vix_condition()
    print(f"[VIX] {vix['message']}")
    
    kospi = check_kospi_box_breakout()
    print(f"[코스피] {kospi['message']}")
    
    # 충족 조건 수
    conditions_met = sum([brent['met'], vix['met'], kospi['met']])
    entry_signal = conditions_met >= MIN_CONDITIONS
    
    print("\n" + "=" * 50)
    print(f"📋 결과: {conditions_met}/3 조건 충족")
    if entry_signal:
        print("🚀 진입 신호 발생!")
    else:
        print("⏸️ 대기 상태")
    print("=" * 50)
    
    # 텔레그램 알림
    message = format_entry_signal(brent, vix, kospi, conditions_met)
    success = send_telegram(message)
    print(f"\n📱 텔레그램 알림: {'발송 완료' if success else '발송 실패 (설정 확인)'}")


if __name__ == "__main__":
    main()
