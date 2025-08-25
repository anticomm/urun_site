import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "8424407061:AAGCMvS7wGZ-dAtLtbtdEZ3eqoDOkAWPIjI"
CHAT_ID = "1390108995"

async def send_test_message():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="✅ Test mesajı: Bot çalışıyor!")

if __name__ == "__main__":
    asyncio.run(send_test_message())
