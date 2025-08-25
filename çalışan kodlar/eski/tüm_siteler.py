import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# İndirim eşiği yüzde kaç olsun?
DISCOUNT_THRESHOLD = 5

def parse_price(text):
    """
    '1.809,10 TL' veya '1.659,17 TL' -> 1809.10 veya 1659.17
    """
    return float(text.replace("TL", "")
                     .replace(".", "")
                     .replace(",", ".")
                     .strip())

def scroll_page(driver, scroll_pause=1, scroll_times=10):
    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

def extract_products(soup):
    products = []
    for kart in soup.select("li.column"):
        a_tag = kart.select_one("a.plink[data-id]")
        if not a_tag:
            continue

        title = a_tag.get("title") or kart.select_one("h3.productName").text.strip()
        href  = a_tag["href"]
        link  = href if href.startswith("http") else "https://www.n11.com" + href

        # Fiyatı iki farklı yapıdan çek
        old_price, new_price = None, None

        # 1) span.oldPrice & span.newPrice ins
        old_span = kart.select_one("span.oldPrice")
        new_span = kart.select_one("span.newPrice ins")
        if old_span and new_span:
            old_price = parse_price(old_span.text)
            new_price = parse_price(new_span.text)
        else:
            # 2) span.newPrice del & span.newPrice ins
            del_tag = kart.select_one("span.newPrice del")
            ins_tag = kart.select_one("span.newPrice ins")
            if del_tag and ins_tag:
                old_price = parse_price(del_tag.text)
                new_price = parse_price(ins_tag.text)

        if old_price and new_price and old_price > new_price:
            discount = round(100 * (old_price - new_price) / old_price, 2)
            products.append({
                "title":       title,
                "link":        link,
                "old_price":   old_price,
                "new_price":   new_price,
                "discount":    discount
            })
    return products

def main():
    # 1) ChromeDriver'ı başlat
    service = Service(r"C:\Users\erkan\Desktop\indirim uygulamaları\chromedriver.exe")  # chromedriver yolunu düzelt
    driver  = webdriver.Chrome(service=service)
    driver.get("https://www.n11.com/arama?q=TERMOS")

    # 2) Sayfayı scroll edip tüm ürünleri yükle
    scroll_page(driver, scroll_pause=1, scroll_times=10)

    # 3) Sayfa kaynağını al, tarayıcıyı kapat
    html = driver.page_source
    driver.quit()

    # 4) BeautifulSoup ile parse et, ürün listesini al
    soup     = BeautifulSoup(html, "html.parser")
    products = extract_products(soup)

    # 5) Eşiği geçenleri yazdır
    for p in products:
        if p["discount"] >= DISCOUNT_THRESHOLD:
            print(f"🛍️ {p['title']}")
            print(f"💸 {p['new_price']} TL → {p['old_price']} TL")
            print(f"📉 İndirim: %{p['discount']}")
            print(f"🔗 {p['link']}\n")

if __name__ == "__main__":
    main()
