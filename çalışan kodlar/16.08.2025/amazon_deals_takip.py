import asyncio
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telegram import Bot

# 🔧 Ayarlar
CHROMEDRIVER_PATH = "C:/Users/erkan/Desktop/indirim uygulamaları/chromedriver.exe"
HEADERS = {"User-Agent": "Mozilla/5.0"}

TELEGRAM_TOKEN = "8424407061:AAGCMvS7wGZ-dAtLtbtdEZ3eqoDOkAWPIjI"
CHAT_ID = "1390108995"
bot = Bot(token=TELEGRAM_TOKEN)

# 📩 Telegram mesaj gönderimi (async)
async def send_telegram_message(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print("Telegram gönderim hatası:", e)

# 🔗 Amazon fırsat linklerini çek
def get_deal_links():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # İstersen açabilirsin
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.amazon.com.tr/deals?ref_=nav_cs_gb&bubble-id=deals-collection-home"
    driver.get(url)

    time.sleep(5)  # Sayfanın yüklenmesi için bekle

    # Sayfa kaynağını kaydet (isteğe bağlı)
    with open("amazon_deals_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    # Gerçek ürün kartlarını seç
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")
    links = []

    for card in cards:
        try:
            link_elem = card.find_element(By.CSS_SELECTOR, "a[data-testid='product-card-link']")
            href = link_elem.get_attribute("href")
            if href and "/dp/" in href:
                links.append(href.split("?")[0])
        except:
            continue

    driver.quit()
    return list(set(links))

# 🧮 Ürün analiz fonksiyonu
def analyze_product(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.select_one("#productTitle")
        title = title_tag.text.strip() if title_tag else "Ürün adı yok"

        disc_tag = soup.select_one("span.a-price > span.a-offscreen")
        orig_tag = soup.select_one("span.a-text-price > span.a-offscreen")

        disc = float(disc_tag.text.replace("TL", "").replace(".", "").replace(",", ".").strip())
        orig = float(orig_tag.text.replace("TL", "").replace(".", "").replace(",", ".").strip())
        rate = round((orig - disc) / orig * 100, 2)

        if rate >= 30:
            return {
                "title": title,
                "original_price": orig,
                "discounted_price": disc,
                "discount_rate": rate,
                "url": url
            }
    except:
        return None

# 🚀 Ana işlem (asenkron)
async def main():
    print("🔍 Amazon Türkiye Günün Fırsatları sayfası taranıyor...")
    product_links = get_deal_links()
    print(f"✅ {len(product_links)} ürün linki bulundu.\n")

    # Test mesajı
    await send_telegram_message("✅ Bot bağlantısı başarılı! İndirimler yakında burada olacak.")

    for link in product_links:
        result = analyze_product(link)
        if result:
            message = (
                f"🔥 %{result['discount_rate']} indirim!\n"
                f"{result['title']}\n"
                f"💸 {result['discounted_price']} TL → {result['original_price']} TL\n"
                f"🔗 {result['url']}"
            )
            await send_telegram_message(message)

            print(f"🔥 %{result['discount_rate']} indirim: {result['title']}")
            print(f"💸 {result['discounted_price']} TL (önceki: {result['original_price']} TL)")
            print(f"🔗 {result['url']}\n")

# 🧨 Scripti çalıştır
if __name__ == "__main__":
    asyncio.run(main())
