# indicators/brent.py
import yfinance as yf
from config import BRENT_TICKER, BRENT_THRESHOLD, BRENT_HOLD_DAYS


def check_brent_condition() -> dict:
    try:
        df = yf.download(BRENT_TICKER, period="10d", progress=False)
        
        if df.empty:
            return {
                'met': False,
                'current_price': None,
                'days_below': 0,
                'message': "❌ 브렌트유 데이터 조회 실패"
            }
        
        closes = df['Close'].dropna().values.flatten()
        current_price = float(closes[-1])
        
        # 연속으로 $95 이하인 일수 카운트
        days_below = 0
        for price in reversed(closes):
            if price <= BRENT_THRESHOLD:
                days_below += 1
            else:
                break
        
        met = days_below >= BRENT_HOLD_DAYS
        
        if met:
            msg = f"✅ 브렌트유 ${current_price:.2f} ({days_below}일 연속 ${BRENT_THRESHOLD} 이하)"
        elif current_price <= BRENT_THRESHOLD:
            msg = f"🟡 브렌트유 ${current_price:.2f} (${BRENT_THRESHOLD} 이하, {days_below}일/{BRENT_HOLD_DAYS}일)"
        else:
            msg = f"❌ 브렌트유 ${current_price:.2f} (${BRENT_THRESHOLD} 초과)"
        
        return {
            'met': met,
            'current_price': current_price,
            'days_below': days_below,
            'message': msg
        }
        
    except Exception as e:
        return {
            'met': False,
            'current_price': None,
            'days_below': 0,
            'message': f"❌ 브렌트유 체크 오류: {e}"
        }
