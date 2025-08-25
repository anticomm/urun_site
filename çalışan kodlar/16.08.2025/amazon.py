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
    driver.get("https://www.amazon.com.tr/deals")

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
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.select_one("#productTitle")
        price_tag = soup.select_one("span.a-price > span.a-offscreen")
        orig_tag  = soup.select_one("span.a-text-price > span.a-offscreen")

        img_tag = soup.select_one("meta[property='og:image']")
        if not img_tag:
            img_tag = soup.select_one("#imgTagWrapperId img")
        image_url = img_tag['content'] if img_tag and img_tag.has_attr('content') else img_tag['src'] if img_tag else ""

        if not (title_tag and price_tag and orig_tag):
            return None

        title = title_tag.text.strip()
        new_price = parse_price(price_tag.text)
        old_price = parse_price(orig_tag.text)

        if old_price > new_price:
            discount = round((old_price - new_price) / old_price * 100, 2)
            if discount >= DISCOUNT_THRESHOLD:
                return {
                    "title": title,
                    "new_price": new_price,
                    "old_price": old_price,
                    "discount": discount,
                    "url": url,
                    "image": image_url
                }
    except Exception as e:
        print(f"Hata: {e}")
    return None

def extract_amazon_deals():
    deals = []
    links = get_deal_links()
    for link in links:
        product = analyze_product(link)
        if product:
            deals.append(product)
    print(f"✅ {len(deals)} Amazon ürünü bulundu (%{DISCOUNT_THRESHOLD}+ indirimli).")
    return deals
