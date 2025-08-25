from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def extract_n11_super_deals():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless=new")  # Test sonrası açılabilir

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.n11.com/super-firsatlar")
    time.sleep(5)

    # Sayfa scroll işlemi
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(15):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    products = []
    items = driver.find_elements(By.CSS_SELECTOR, "a.plink")
    for item in items:
        try:
            title = item.get_attribute("title")
            url = item.get_attribute("href")
            name = item.find_element(By.CSS_SELECTOR, "h3.productName").text

            parent = item.find_element(By.XPATH, "./..")
            old_price_tag = parent.find_elements(By.CSS_SELECTOR, "del")
            new_price_tag = parent.find_elements(By.CSS_SELECTOR, "ins")

            if old_price_tag and new_price_tag:
                old_price = old_price_tag[0].text
                new_price = new_price_tag[0].text

                old_price_val = float(old_price.replace("TL", "").replace(".", "").replace(",", ".").strip())
                new_price_val = float(new_price.replace("TL", "").replace(".", "").replace(",", ".").strip())

                if old_price_val > new_price_val:
                    discount = round((old_price_val - new_price_val) / old_price_val * 100)

                    # Görsel URL varsa al
                    try:
                        image_tag = item.find_element(By.CSS_SELECTOR, "img")
                        image_url = image_tag.get_attribute("data-original") or image_tag.get_attribute("src")
                    except:
                        image_url = ""

                    products.append({
                        "title": title or name,
                        "name": name,
                        "url": url,
                        "old_price": old_price_val,
                        "new_price": new_price_val,
                        "discount": discount,
                        "image_url": image_url
                    })
        except Exception as e:
            print(f"Ürün hatası: {e}")

    driver.quit()
    print(f"✅ {len(products)} ürün bulundu (Süper Fırsatlar).")
    return products
