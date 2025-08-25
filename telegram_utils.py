import os
import requests
from dotenv import load_dotenv

# .env dosyasından BOT_TOKEN ve CHAT_ID'yi yükle
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_to_telegram(caption, image_url=None):
    """
    Telegram'a mesaj veya görsel + mesaj gönderir.
    caption: HTML formatlı mesaj içeriği
    image_url: varsa görsel URL'si
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN veya CHAT_ID .env dosyasında tanımlı değil.")
        return None

    # Gönderim türünü belirle
    if image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        data = {
            "chat_id": CHAT_ID,
            "caption": caption,
            "photo": image_url,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": caption,
            "parse_mode": "HTML"
        }

    # API isteği gönder
    try:
        response = requests.post(url, data=data)
        result = response.json()
        if not result.get("ok"):
            print("⚠️ Telegram API hatası:", result)
        return result
    except Exception as e:
        print("❌ Telegram gönderim hatası:", e)
        return None
