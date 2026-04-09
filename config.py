# config.py
import os

# === 진입 조건 임계값 ===
BRENT_THRESHOLD = 95.0      # 브렌트유 상한 (달러)
BRENT_HOLD_DAYS = 3         # 유지 일수

VIX_THRESHOLD = 20.0        # VIX 상한
VIX_TREND_DAYS = 5          # 하락 추세 판단 기간

BOX_LOOKBACK_DAYS = 60      # 박스 상단 탐색 기간 (약 2개월)
BOX_RESISTANCE_COUNT = 2    # 저항 횟수 (2~3회)
BOX_TOLERANCE_PCT = 0.01    # 고점 근처 판단 범위 (±1%)
BOX_HOLD_DAYS = 2           # 돌파 후 유지 일수

# === 최소 충족 조건 수 ===
MIN_CONDITIONS = 2          # 3개 중 2개

# === 텔레그램 설정 (GitHub Secrets에서 가져옴) ===
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# === 티커 심볼 ===
BRENT_TICKER = "BZ=F"       # 브렌트유 선물
VIX_TICKER = "^VIX"         # VIX 지수
KOSPI_TICKER = "^KS11"      # 코스피 지수
