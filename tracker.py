import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

BASE_URL = "https://www.llibreriablanquerna.cat"

def get_book_price_blanquerna(query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        # Cerca a la llibreria
        driver.get(f"{BASE_URL}/producto/listadobuscar?buscar={query}")
        time.sleep(3)

        try:
            product_link = driver.find_element(By.CSS_SELECTOR, "div.producto a")
            partial_url = product_link.get_attribute("href")
            full_url = partial_url if partial_url.startswith("http") else BASE_URL + partial_url
        except:
            return {
                "EAN13": query,
                "url": "",
                "ecommerce": "llibreriablanquerna",
                "status": "not_found",
                "price": None
            }

        # Intenta trobar l'EAN13 dins l'atribut `title`
        try:
            title_attr = product_link.get_attribute("title")
            match = re.search(r"\b(\d{13})\b", title_attr)
            ean13 = match.group(1) if match else query
        except:
            ean13 = query

        driver.get(full_url)
        time.sleep(3)

        # Preu
        try:
            price_text = driver.find_element(By.CSS_SELECTOR, "span.precio").text.strip()
            price = float(price_text.replace("€", "").replace(",", "."))
        except:
            price = None

        # Disponibilitat
        try:
            status_text = driver.find_element(By.CSS_SELECTOR, "span.disponibilidad").text.lower()
            if "disponible" in status_text:
                status = "available"
            elif "sense estoc" in status_text or "no disponible" in status_text:
                status = "out_of_stock"
            else:
                status = "unknown"
        except:
            status = "unknown"

        return {
            "EAN13": ean13,
            "url": full_url,
            "ecommerce": "llibreriablanquerna",
            "status": status,
            "price": price
        }

    except Exception:
        return {
            "EAN13": query,
            "url": "",
            "ecommerce": "llibreriablanquerna",
            "status": "error",
            "price": None
        }
    finally:
        driver.quit()


def send_to_api(data):
    url = "https://bookpricetracker.risusapp.com/api/bookPriceUpdate"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("Enviat a l'API:")
    print("Status:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    query = input("Introdueix el títol, autor o ISBN del llibre: ").strip()
    book_data = get_book_price_blanquerna(query)

    if book_data['status'] != 'not_found':
        print(f"Llibre trobat amb EAN {book_data['EAN13']} - Status: '{book_data['status']}' - Preu: {book_data['price']}€")
        send_to_api(book_data)
    else:
        print("Llibre no trobat. No s'envia res a l'API.")
