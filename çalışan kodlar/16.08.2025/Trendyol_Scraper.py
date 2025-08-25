import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_product_links(category_url):
    product_links = []
    for page in range(1, 5):
        url = f"{category_url}?pi={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "/urun/" in href:
                full_url = "https://www.trendyol.com" + href
                product_links.append(full_url)
        time.sleep(1)
    return list(set(product_links))

def analyze_product(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="pr-new-br")
    title = title_tag.text.strip() if title_tag else "Ürün adı yok"

    discounted_price_tag = soup.find("span", class_="prc-dsc")
    original_price_tag = soup.find("span", class_="prc-org")

    try:
        discounted_price = float(discounted_price_tag.text.replace("TL", "").replace(".", "").replace(",", ".").strip())
        original_price = float(original_price_tag.text.replace("TL", "").replace(".", "").replace(",", ".").strip())
        discount_rate = round((original_price - discounted_price) / original_price * 100, 2)
    except:
        return None

    if discount_rate >= 50:
        return {
            "title": title,
            "original_price": original_price,
            "discounted_price": discounted_price,
            "discount_rate": discount_rate,
            "url": url
        }
    return None

if __name__ == "__main__":
    category_url = "https://www.trendyol.com/erkek-tisort"
    product_links = get_product_links(category_url)
    print(f"{len(product_links)} ürün bulundu.")

    for link in product_links:
        result = analyze_product(link)
        if result:
            print(f"🔥 % {result['discount_rate']} indirim: {result['title']}")
            print(f"Fiyat: {result['discounted_price']} TL (Önceki: {result['original_price']} TL)")
            print(f"Link: {result['url']}\n")
