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
