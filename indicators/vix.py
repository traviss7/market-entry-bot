# indicators/vix.py
import yfinance as yf
import numpy as np
from config import VIX_TICKER, VIX_THRESHOLD, VIX_TREND_DAYS


def check_vix_condition() -> dict:
    try:
        df = yf.download(VIX_TICKER, period="1mo", progress=False)
        
        if df.empty:
            return {
                'met': False,
                'current_value': None,
                'is_below_threshold': False,
                'is_downtrend': False,
                'message': "❌ VIX 데이터 조회 실패"
            }
        
        closes = df['Close'].dropna().values.flatten()
        current_value = float(closes[-1])
        
        # 조건 1: VIX < 20
        is_below = current_value < VIX_THRESHOLD
        
        # 조건 2: 하락 추세 (최근 N일 선형회귀 기울기)
        recent = closes[-VIX_TREND_DAYS:]
        x = np.arange(len(recent))
        slope = np.polyfit(x, recent, 1)[0]
        is_downtrend = slope < 0
        
        met = is_below and is_downtrend
        
        trend_str = "↓하락" if is_downtrend else "↑상승"
        
        if met:
            msg = f"✅ VIX {current_value:.2f} ({trend_str}, {VIX_THRESHOLD} 미만)"
        elif is_below:
            msg = f"🟡 VIX {current_value:.2f} ({VIX_THRESHOLD} 미만이나 {trend_str} 추세)"
        else:
            msg = f"❌ VIX {current_value:.2f} ({VIX_THRESHOLD} 이상, {trend_str})"
        
        return {
            'met': met,
            'current_value': current_value,
            'is_below_threshold': is_below,
            'is_downtrend': is_downtrend,
            'message': msg
        }
        
    except Exception as e:
        return {
            'met': False,
            'current_value': None,
            'is_below_threshold': False,
            'is_downtrend': False,
            'message': f"❌ VIX 체크 오류: {e}"
        }
