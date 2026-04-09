# notifier.py
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message: str) -> bool:
    """텔레그램 메시지 발송 (requests 사용)"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("텔레그램 설정 없음")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"텔레그램 발송 실패: {e}")
        return False


def format_entry_signal(
    brent_result: dict,
    vix_result: dict,
    kospi_result: dict,
    conditions_met: int
) -> str:
    """진입 신호 메시지 포맷팅"""
    
    if conditions_met >= 2:
        header = "🚀 <b>【국장 진입 신호】</b> 🚀"
        status = f"✅ {conditions_met}/3 조건 충족 - 진입 고려!"
    elif conditions_met == 1:
        header = "📊 <b>【국장 모니터링】</b>"
        status = f"🟡 {conditions_met}/3 조건 충족 - 대기"
    else:
        header = "📊 <b>【국장 모니터링】</b>"
        status = f"❌ {conditions_met}/3 조건 충족 - 관망"
    
    lines = [
        header,
        "",
        status,
        "",
        "<b>📋 조건 상세:</b>",
        f"1️⃣ {brent_result['message']}",
        f"2️⃣ {vix_result['message']}",
        f"3️⃣ {kospi_result['message']}",
    ]
    
    if kospi_result.get('resistance_level'):
        lines.append("")
        lines.append(f"📍 코스피 박스 상단: {kospi_result['resistance_level']:.0f}")
    
    return "\n".join(lines)
