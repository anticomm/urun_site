import asyncio
from extractors.n11 import extract_n11
from extractors.amazon import extract_amazon_deals
from telegram_utils import send_telegram_message

SEARCH_TERMS = ["termos", "iphone 14", "ssd"]

async def main():
    # Test mesajı
    await send_telegram_message("✅ Bot bağlantısı başarılı! İndirimler yolda…")

    # N11 fırsatları
    for term in SEARCH_TERMS:
        for title, price, disc, link in extract_n11(term):
            msg = f"🛍️ *{title}*\n💸 {price} TL\n📉 İndirim: %{disc}\n🔗 {link}"
            await send_telegram_message(msg)

    # Amazon “Günün Fırsatları”
    amazon_deals = extract_amazon_deals()
    for title, price, disc, link in amazon_deals:
        msg = f"🔥 *{title}*\n💸 {price} TL\n📉 İndirim: %{disc}\n🔗 {link}"
        await send_telegram_message(msg)

if __name__ == "__main__":
    asyncio.run(main())
for title, price, disc, link, kategori in extract_n11(term):
    msg = (
        f"🛍️ *{title}*\n"
        f"📦 Kategori: {kategori}\n"
        f"💸 {price} TL\n"
        f"📉 İndirim: %{disc}\n"
        f"🔗 {link}"
    )
    await send_telegram_message(msg)
from extractors.n11 import extract_n11_all_categories

urunler = extract_n11_all_categories()
for title, price, disc, link, kategori in urunler:
    msg = (
        f"🛍️ *{title}*\n"
        f"📦 Kategori: {kategori}\n"
        f"💸 {price} TL\n"
        f"📉 İndirim: %{disc}\n"
        f"🔗 {link}"
    )
    await send_telegram_message(msg)
