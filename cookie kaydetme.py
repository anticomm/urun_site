import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"  # ← Brave yolu

driver = webdriver.Chrome(options=options)
driver.get("https://www.amazon.com/")

input("🔐 Amazon'da oturum açtıysan Enter'a bas...")

all_cookies = driver.get_cookies()
amazon_cookies = [c for c in all_cookies if "amazon." in c.get("domain", "")]

with open("cookie.json", "w", encoding="utf-8") as f:
    json.dump(amazon_cookies, f, ensure_ascii=False, indent=2)

print(f"✅ {len(amazon_cookies)} cookie kaydedildi.")
