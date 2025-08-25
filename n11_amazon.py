import asyncio
from selenium import webdriver
from extractors.n11 import extract_n11_super_deals
from extractors.amazon import extract_amazon_deals
from telegram_utils import send_to_telegram  # doğru fonksiyon adı

def format_message(p):
    new_price = p.get("new_price", "??")
    old_price = p.get("old_price", "??")
    return (
        f"🛍️ <b>{p.get('title', 'Ürün')}</b>\n"
        f"💸 <b>{new_price} TL</b> → {old_price} TL\n"
        f"📦 Kargo: Ücretsiz\n"
        f"🔗 <a href='{p.get('url', '#')}'>Ürünü Gör</a>"
    )

async def main():
    # Test mesajı gönder
    send_to_telegram(
        "<b>✅ Bot bağlantısı başarılı!</b>\n<i>💡 Sistem aktif durumda.</i>",
        "https://dummyimage.com/600x400/000/fff&text=Test"
    )

    # N11 ürünleri
    for p in extract_n11_super_deals():
        msg = format_message(p)
        send_to_telegram(msg, p.get("image_url"))

    # Amazon ürünleri için driver oluştur
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.amazon.com.tr/deals")

        amazon_products = extract_amazon_deals(driver)
        print(f"✅ Amazon'dan {len(amazon_products)} ürün bulundu.")

        for p in amazon_products:
            msg = format_message(p)
            send_to_telegram(msg, p.get("image_url"))
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
