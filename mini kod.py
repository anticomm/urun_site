from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://www.amazon.com.tr/deals?ref_=nav_cs_gb")

time.sleep(5)  # Sayfanın yüklenmesini bekle

html = driver.page_source

# Dump dosyasına yaz
with open("dump.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()

