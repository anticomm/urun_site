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
