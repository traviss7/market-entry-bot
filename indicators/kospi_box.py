# indicators/kospi_box.py
import yfinance as yf
import numpy as np
from config import (
    KOSPI_TICKER, 
    BOX_LOOKBACK_DAYS, 
    BOX_RESISTANCE_COUNT,
    BOX_TOLERANCE_PCT,
    BOX_HOLD_DAYS
)


def find_resistance_level(closes: np.ndarray, tolerance_pct: float = 0.01, min_count: int = 2) -> float:
    """저항선 찾기: 여러 번 막힌 고점대"""
    # 로컬 고점 찾기
    local_highs = []
    for i in range(5, len(closes) - 5):
        if closes[i] == max(closes[i-5:i+6]):
            local_highs.append(closes[i])
    
    if len(local_highs) < min_count:
        return float(np.max(closes))
    
    local_highs = np.array(local_highs)
    
    # 비슷한 가격대 그룹핑
    for high in sorted(local_highs, reverse=True):
        similar_count = np.sum(np.abs(local_highs - high) / high <= tolerance_pct)
        if similar_count >= min_count:
            return float(high)
    
    return float(np.max(closes))


def check_kospi_box_breakout() -> dict:
    try:
        df = yf.download(KOSPI_TICKER, period="3mo", progress=False)
        
        if df.empty or len(df) < BOX_LOOKBACK_DAYS:
            return {
                'met': False,
                'current_price': None,
                'resistance_level': None,
                'days_above': 0,
                'message': "❌ 코스피 데이터 조회 실패"
            }
        
        closes = df['Close'].dropna().values.flatten()
        current_price = float(closes[-1])
        
        # 박스 상단 (저항선) 찾기
        analysis_data = closes[:-BOX_HOLD_DAYS] if len(closes) > BOX_HOLD_DAYS else closes[:-1]
        resistance = find_resistance_level(
            analysis_data[-BOX_LOOKBACK_DAYS:],
            tolerance_pct=BOX_TOLERANCE_PCT,
            min_count=BOX_RESISTANCE_COUNT
        )
        
        # 돌파 후 유지 일수 체크
        days_above = 0
        for price in reversed(closes):
            if price > resistance:
                days_above += 1
            else:
                break
        
        met = days_above >= BOX_HOLD_DAYS
        
        if met:
            msg = f"✅ 코스피 {current_price:.0f} (박스 상단 {resistance:.0f} 돌파, {days_above}일 유지)"
        elif current_price > resistance:
            msg = f"🟡 코스피 {current_price:.0f} (박스 상단 {resistance:.0f} 돌파, {days_above}일/{BOX_HOLD_DAYS}일)"
        else:
            msg = f"❌ 코스피 {current_price:.0f} (박스 상단 {resistance:.0f} 미돌파)"
        
        return {
            'met': met,
            'current_price': current_price,
            'resistance_level': float(resistance),
            'days_above': days_above,
            'message': msg
        }
        
    except Exception as e:
        return {
            'met': False,
            'current_price': None,
            'resistance_level': None,
            'days_above': 0,
            'message': f"❌ 코스피 체크 오류: {e}"
        }
