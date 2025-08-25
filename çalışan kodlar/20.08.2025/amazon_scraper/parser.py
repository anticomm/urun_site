from bs4 import BeautifulSoup

def parse_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    for card in soup.select('div[data-asin][data-deal-id]'):
        asin = card['data-asin']

        # Başlık
        title_tag = card.select_one('.a-truncate-full')
        title = title_tag.text.strip() if title_tag else None

        # Fiyat
        price = extract_price(card)

        # Rozet
        badge_tag = card.select_one('div[data-component="dui-badge"] .a-size-mini')
        badge = badge_tag.text.strip() if badge_tag else None

        # Link
        link_tag = card.select_one('a[data-testid="product-card-link"]')
        link = link_tag['href'] if link_tag else None

        # Görsel
        image_tag = card.select_one('img')
        image = image_tag['src'] if image_tag else None

        # Renkler
        colors = []
        for swatch in card.select('li a[aria-label]'):
            colors.append({
                'color': swatch['aria-label'],
                'href': swatch['href']
            })

        if title and price:
            products.append({
                "asin": asin,
                "title": title,
                "price": price,
                "badge": badge,
                "link": link,
                "image": image,
                "colors": colors
            })

    return products

def extract_price(item):
    # Klasik yapı
    price_whole = item.select_one(".a-price-whole")
    price_fraction = item.select_one(".a-price-fraction")
    if price_whole:
        return f"{price_whole.text.strip()},{price_fraction.text.strip() if price_fraction else '00'} ₺"

    # aria-hidden fallback
    alt_price = item.select_one("span[aria-hidden='true']")
    if alt_price and ("TL" in alt_price.text or "₺" in alt_price.text):
        return alt_price.text.strip()

    # a-offscreen fallback (sadece fiyat içeren metinleri al)
    offscreen = item.select_one(".a-offscreen")
    if offscreen:
        text = offscreen.text.strip()
        if any(x in text for x in ["TL", "₺", "Fiyat"]):
            for prefix in ["Fırsatın Fiyatı:", "Fırsat kapsamında:", "İndirimli fiyat:", "Fiyat:"]:
                text = text.replace(prefix, "").strip()
            return text

    return "Fiyat bulunamadı"
def extract_price(product_box):
    try:
        price = product_box.select_one(".a-price-whole")
        if price:
            return price.text.strip()
        # Fallback: .a-offscreen
        fallback_price = product_box.select_one(".a-offscreen")
        if fallback_price:
            return fallback_price.text.strip()
    except Exception as e:
        print("Fiyat parse hatası:", e)
    return None
def extract_product_link(product_box):
    link_tag = product_box.select_one("a[href]")
    if link_tag:
        return "https://www.amazon.com.tr" + link_tag['href']
    return None
