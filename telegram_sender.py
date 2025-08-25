import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(msg: str):
    url = f"https://api.telegram.org/bot{8424407061:AAGCMvS7wGZ-dAtLtbtdEZ3eqoDOkAWPIjI}/sendMessage"
    payload = {
        "chat_id": 1390108995,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Telegram hatası: {response.text}")
