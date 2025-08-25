import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "extractors"))

from extractors.n11 import extract_n11 # extractors klasörü içindeki dosya
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

CHROMEDRIVER_PATH = r"C:\Users\erkan\Desktop\indirim uygulamaları\chromedriver.exe"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DISCOUNT_THRESHOLD = 5

import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(text: str):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        print("Telegram gönderim hatası:", e)
def parse_price(text: str) -> float:
    """
    '₺ 1.809,10', '1.659,17 TL' → 1809.10, 1659.17
    """
    cleaned = (
        text.replace("TL", "")
            .replace("₺", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
    )
    try:
        return float(cleaned)
    except:
        return 0.0
from bs4 import BeautifulSoup
import requests
from parse_price import parse_price
from config import DISCOUNT_THRESHOLD

def extract_n11(search_term: str):
    url = f"https://www.n11.com/arama?q={search_term}"
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    deals = []
    for card in soup.select("li.column"):
        a_tag = card.select_one("a.plink[data-id]")
        if not a_tag:
            continue

        title = a_tag.get("title") or card.select_one("h3.productName").text.strip()
        href  = a_tag["href"]
        link  = href if href.startswith("http") else "https://www.n11.com" + href

        # Fiyat işleme
        old_tag = card.select_one("span.oldPrice")
        new_tag = card.select_one("span.newPrice ins") or card.select_one("span.newPrice del")
        if not old_tag or not new_tag:
            continue

        old_price = parse_price(old_tag.text)
        new_price = parse_price(new_tag.text)

        if old_price > new_price:
            discount = round((old_price - new_price) / old_price * 100, 2)
            if discount >= DISCOUNT_THRESHOLD:
                deals.append((title, new_price, discount, link))

    return deals
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from parse_price import parse_price
from config import CHROMEDRIVER_PATH, HEADERS, DISCOUNT_THRESHOLD

def get_deal_links() -> list[str]:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.amazon.com.tr/deals?ref_=nav_cs_gb&bubble-id=deals-collection-home")

    time.sleep(5)
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")
    links = set()
    for card in cards:
        try:
            href = card.find_element(By.CSS_SELECTOR, "a[data-testid='product-card-link']").get_attribute("href")
            if href and "/dp/" in href:
                links.add(href.split("?")[0])
        except:
            continue

    driver.quit()
    return list(links)

def analyze_product(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    title_tag = soup.select_one("#productTitle")
    price_tag = soup.select_one("span.a-price > span.a-offscreen")
    orig_tag  = soup.select_one("span.a-text-price > span.a-offscreen")

    if not (title_tag and price_tag and orig_tag):
        return None

    title = title_tag.text.strip()
    new_price = parse_price(price_tag.text)
    old_price = parse_price(orig_tag.text)

    if old_price > new_price:
        discount = round((old_price - new_price) / old_price * 100, 2)
        if discount >= DISCOUNT_THRESHOLD:
            return (title, new_price, discount, url)
    return None

def extract_amazon_deals():
    deals = []
    links = get_deal_links()
    for link in links:
        result = analyze_product(link)
        if result:
            deals.append(result)
    return deals
import asyncio
from extractors.n11 import extract_n11
from extractors.amazon import extract_amazon_deals
from telegram_utils import send_telegram_message

SEARCH_TERMS = ["termos", "iphone 14", "ssd"]

async def main():
    # Test mesajı
    await send_telegram_message("✅ Bot bağlantısı başarılı! İndirimler yolda…")

    # N11 fırsatları
    for term in SEARCH_TERMS:
        for title, price, disc, link in extract_n11(term):
            msg = f"🛍️ *{title}*\n💸 {price} TL\n📉 İndirim: %{disc}\n🔗 {link}"
            await send_telegram_message(msg)

    # Amazon “Günün Fırsatları”
    amazon_deals = extract_amazon_deals()
    for title, price, disc, link in amazon_deals:
        msg = f"🔥 *{title}*\n💸 {price} TL\n📉 İndirim: %{disc}\n🔗 {link}"
        await send_telegram_message(msg)

if __name__ == "__main__":
    asyncio.run(main())
