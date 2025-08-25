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

def get_text_or_default(item, selector, default="??"):
    try:
        return item.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return default

def get_attr_or_default(item, selector, attr, default=None):
    try:
        return item.find_element(By.CSS_SELECTOR, selector).get_attribute(attr)
    except:
        return default

def get_price(item):
    try:
        return item.find_element(By.CSS_SELECTOR, ".a-price .a-offscreen").text.strip()
    except:
        try:
            return item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
        except:
            return "??"

# ✅ Yeni fonksiyon: detay sayfasından fiyat çekme
def get_price_from_detail_page(driver, url):
    driver.execute_script("window.open(arguments[0]);", url)
    driver.switch_to.window(driver.window_handles[1])

    price = "Fiyat alınamadı"
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.aok-offscreen"))
        )
        price_elem = driver.find_element(By.CSS_SELECTOR, "span.aok-offscreen")
        if price_elem:
            price = price_elem.text.strip().replace("\u00a0", " ")
    except Exception as e:
        print(f"Detay sayfasında fiyat alınamadı: {e}")

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return price

def extract_amazon_deals(driver):
    products = []
    seen_urls = set()

    scroll_to_bottom(driver)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-asin]"))
    )

    items = driver.find_elements(By.CSS_SELECTOR, "div[data-asin]")
    print(f"🔍 data-asin ile {len(items)} ürün kutusu bulundu.")

    for item in items:
        try:
            title = get_text_or_default(item, "span.a-truncate-cut")
            new_price = get_price(item)
            url = get_attr_or_default(item, "a", "href")
            url = url.split("?")[0] if url else "#"

            # ✅ Eğer fiyat "??" ise detay sayfasından çek
            if new_price == "??" and url.startswith("http"):
                new_price = get_price_from_detail_page(driver, url)

            old_price = get_text_or_default(item, "span.a-price-whole:nth-of-type(2)")
            discount = get_text_or_default(item, "div.style_filledRoundedBadgeLabel__Vo-4g")
            img = get_attr_or_default(item, "img", "src") or get_attr_or_default(item, "img", "data-src")


            if url in seen_urls:
                continue
            seen_urls.add(url)

            products.append({
                "title": title,
                "new_price": new_price,
                "old_price": old_price,
                "discount": discount,
                "url": url,
                "image_url": img
            })

        except Exception as e:
            continue

    badges = driver.find_elements(By.XPATH, "//div[contains(@class, 'BadgeLabel')]")
    print(f"🔍 Bağımsız badge ile {len(badges)} rozet bulundu.")

    for badge in badges:
        try:
            discount = badge.text.strip()
            product_box = badge.find_element(By.XPATH, "./ancestor::div[@data-asin]")
            title = get_text_or_default(product_box, "span.a-truncate-cut")
            new_price = get_price(product_box)
            url = get_attr_or_default(product_box, "a", "href")
            url = url.split("?")[0] if url else "#"

            # ✅ Detay sayfasından fiyat çekme (badge tarafı için)
            if new_price == "??" and url.startswith("http"):
                new_price = get_price_from_detail_page(driver, url)

            old_price = get_text_or_default(product_box, "span.a-price-whole:nth-of-type(2)")
            img = get_attr_or_default(product_box, "img", "src")

            if url in seen_urls:
                continue
            seen_urls.add(url)

            products.append({
                "title": title,
                "new_price": new_price,
                "old_price": old_price,
                "discount": discount,
                "url": url,
                "image_url": img
            })

        except:
            continue

    print(f"✅ Amazon'dan toplam {len(products)} ürün bulundu.")
    return products
