from browser import get_html_from_brave, batch_price_fetch
from parser import parse_products
from telegram import send_to_telegram

html = get_html_from_brave()
products = parse_products(html)
products = batch_price_fetch(products)

if products:
    send_to_telegram(products)
    print(f"{len(products)} ürün Telegram'a gönderildi.")
else:
    print("🚫 Ürün bulunamadı veya sayfa boş geldi.")
