import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_cookies(driver, path="cookie.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            cookies = json.load(f)
        for cookie in cookies:
            if "expiry" in cookie:
                cookie["expiry"] = int(cookie["expiry"])
            driver.add_cookie(cookie)
        print("✅ Cookie.json yüklendi, oturumlu başlatıldı.")
    else:
        print("⚠️ Cookie.json bulunamadı, giriş yapılması gerekiyor.")

def save_cookies(driver, path="cookie.json"):
    cookies = driver.get_cookies()
    with open(path, "w") as f:
        json.dump(cookies, f, indent=2)
    print("💾 Cookie.json güncellendi.")

def normalize_link(link):
    if link and not link.startswith("https://"):
        return "https://www.amazon.com.tr" + link
    return link

def get_html_from_brave():
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.amazon.com.tr")
    time.sleep(2)

    load_cookies(driver)
    driver.refresh()
    time.sleep(2)

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "sp-cc-accept"))
        ).click()
    except:
        pass

    driver.execute_script("window.scrollTo(0, 300);")
    driver.execute_script("document.body.dispatchEvent(new Event('mousemove'));")
    time.sleep(1)

    driver.get("https://www.amazon.com.tr/deals?ref_=nav_cs_gb")
    time.sleep(10)

    for i in range(0, 5000, 500):
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.5)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
        )
    except:
        print("⚠️ Fiyat alanı DOM'da bulunamadı.")

    html = driver.page_source
    with open("amazon_brave_dump.html", "w", encoding="utf-8") as f:
        f.write(html)

    save_cookies(driver)
    driver.quit()
    return html

def batch_price_fetch(products):
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)

    for product in products:
        link = product.get("link")
        if not link or "None" in link:
            print(f"⛔ Link eksik veya bozuk: {product.get('title', 'Bilinmeyen ürün')}")
            continue

        full_link = normalize_link(link)
        product["link"] = full_link

        if not product.get("price") or "bulunamadı" in product["price"].lower():
            try:
                print(f"🔗 Açılıyor: {product['title']}")
                driver.get(full_link)
                time.sleep(3)

                if "captcha" in driver.title.lower() or "güvenli değil" in driver.page_source.lower():
                    print(f"🛑 CAPTCHA veya güvenlik engeli: {product['title']}")
                    product["price"] = "CAPTCHA engeli"
                    continue

                driver.execute_script("window.scrollTo(0, 100);")
                driver.execute_script("document.body.dispatchEvent(new Event('mousemove'));")

                price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                        "#priceblock_dealprice, #priceblock_ourprice, #priceblock_saleprice, .a-price .a-offscreen"))
                )
                product["price"] = price.text.strip()
                print(f"✅ Fiyat alındı: {product['title']} → {product['price']}")
            except Exception as e:
                print(f"❌ Fiyat alınamadı: {product['title']} → {e}")
                product["price"] = "Fiyat alınamadı"

    driver.quit()
    return products
