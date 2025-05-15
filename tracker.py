from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time
import json

def get_book_price_casadellibro(query, ean13):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # 1. Navegar i buscar
        search_url = f"https://www.casadellibro.com/busqueda-generica?query={query}"
        driver.get(search_url)
        time.sleep(3)

        # 2. Obtenir primer resultat i accedir al llibre
        book = driver.find_element(By.CSS_SELECTOR, "div.product-card a")
        book_url = book.get_attribute("href")
        driver.get(book_url)
        time.sleep(3)

        # 3. Obtenir preu
        price_elem = driver.find_element(By.CSS_SELECTOR, "div.product-price span.price")
        price_text = price_elem.text.strip()
        price = float(price_text.replace("€", "").replace(",", "."))

        # 4. Obtenir estat de disponibilitat
        try:
            availability_elem = driver.find_element(By.CSS_SELECTOR, "div.product-main-details span.availability")
            status = availability_elem.text.lower()
        except:
            status = "available"  # Si no s'especifica, assumim disponible

        # Normalitzar status
        if "disponible" in status:
            normalized_status = "available"
        elif "no disponible" in status or "agotado" in status:
            normalized_status = "out_of_stock"
        else:
            normalized_status = "unknown"

        return {
            'EAN13': ean13,
            'url': book_url,
            'ecommerce': 'casadellibro',
            'status': normalized_status,
            'price': price
        }

    except Exception as e:
        print("Error:", e)
        return {
            'EAN13': ean13,
            'url': '',
            'ecommerce': 'casadellibro',
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
    # Entrada manual per consola
    query = input("Introdueix el títol, autor o ISBN del llibre: ").strip()
    ean13 = input("Introdueix l'EAN13 (si el tens, si no el pots deixar en blanc): ").strip()

    if not ean13:
        ean13 = query  # Suposem que és el mateix

    book_data = get_book_price_casadellibro(query, ean13)

    if book_data['status'] != 'not_found':
        print(f"Llibre trobat amb status '{book_data['status']}': {book_data['price']}€")
        send_to_api(book_data)
    else:
        print("Llibre no trobat. No s'envia res a l'API.")
