from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_text_or_none(elem, selectors):
    for sel in selectors:
        try:
            return elem.find_element(By.CSS_SELECTOR, sel).text.strip()
        except:
            continue
    return None

def extract_amazon_deals(driver):
    driver.get("https://www.amazon.com.tr/gp/goldbox")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    if "validateCaptcha" in driver.current_url:
        print("⚠️ CAPTCHA sayfasına yönlendirildin.")
        driver.save_screenshot("captcha.png")
        return []

    scroll_to_bottom(driver)
    time.sleep(5)  # Scroll sonrası yükleme için ekstra bekleme

    try:
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin], div.s-result-item, div.puis-card-container"))
        )
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-asin], div.s-result-item, div.puis-card-container")
    except:
        print("⚠️ Sayfa yüklenemedi veya ürün kutusu bulunamadı.")
        with open("amazon_dump.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return []

    products = []

    for elem in product_elements:
        try:
            title = get_text_or_none(elem, ["h2 a", "span.a-text-normal", "h2 span"])
            price = get_text_or_none(elem, [".a-price .a-offscreen", ".a-price-whole"])
            badge = get_text_or_none(elem, [".a-badge-text"])

            if title and price:
                products.append({
                    "title": title,
                    "price": price,
                    "badge": badge if badge else "Badge yok"
                })
            else:
                print("⚠️ Ürün eksik veri içeriyor, atlandı.")

        except Exception as e:
            print(f"⚠️ Ürün işlenemedi: {e}")
            continue

    print(f"✅ Amazon'dan {len(products)} ürün bulundu.")
    for p in products:
        print(f"📦 {p['title']} → 💰 {p['price']} | 🏷️ {p['badge']}")
    return products

# 🔧 Tarayıcı ayarları
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument("--lang=tr-TR")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

# 🚀 Scraper'ı çalıştır
extract_amazon_deals(driver)

# 🧹 Tarayıcıyı kapat
driver.quit()
