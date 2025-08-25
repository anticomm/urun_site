from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from urllib.parse import unquote, urlparse, parse_qs
import time

# Chrome ayarları
options = Options()
options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# ChromeDriver yolu
service = Service(r"C:\Users\erkan\Desktop\indirim uygulamaları\chromedriver.exe")  # kendi yolunu yaz

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://www.n11.com/super-firsatlar")
time.sleep(5)  # Sayfanın yüklenmesi için bekle

html = driver.page_source
driver.quit()
