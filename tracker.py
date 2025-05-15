import re
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_book_price_blanquerna(query):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Buscar el llibre a la web
        search_url = f"https://www.llibreriablanquerna.cat/producto/listadobuscar?buscar={query}"
        driver.get(search_url)
        time.sleep(3)

        # Trobar primer resultat de llibre
        book_elem = driver.find_element(By.CSS_SELECTOR, "div.producto a[href*='/products/']")
        partial_url = book_elem.get_attribute("href")
        book_url = partial_url if "http" in partial_url else "https://www.llibreriablanquerna.cat" + partial_url

        # Extreure EAN13 del títol (format: "TÍTOL | EAN13 | AUTOR")
        title_attr = book_elem.get_attribute("title")
        match = re.search(r'\b(\d{13})\b', title_attr)
        ean13 = match.group(1) if match else query  # Fallback si no troba

        # Anar a la pàgina del llibre
        driver.get(book_url)
        time.sleep(3)

        # Obtenir preu
        price_elem = driver.find_element(By.CSS_SELECTOR, "span.precio")
        price_text = price_elem.text.strip()
        price = float(price_text.replace("€", "").replace(",", ".").strip())

        # Obtenir disponibilitat
        try:
            availability_elem = driver.find_element(By.CSS_SELECTOR, "span.disponibilidad")
            status = availability_elem.text.lower()
        except:
            status = "available"

        if "disponible" in status:
            normalized_status = "available"
        elif "no disponible" in status or "agotado" in status:
            normalized_status = "out_of_stock"
        else:
            normalized_status = "unknown"

        return {
            'EAN13': ean13,
            'url': book_url,
            'ecommerce': 'llibreriablanquerna',
            'status': normalized_status,
            'price': price
        }

    except Exception as e:
        print("Error:", e)
        return {
            'EAN13': query,
            'url': '',
            'ecommerce': 'llibreriablanquerna',
            'status': 'not_found',
            'price': None
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
