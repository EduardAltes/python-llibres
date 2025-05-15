# AA - Python + Selenium Base de dades de Llibres

## Descripció

Aquest projecte és un script en Python que utilitza Selenium per buscar el preu d’un llibre a Casa del Libro segons el títol, autor o ISBN, i envia la informació a una API externa (`bookpricetracker.risusapp.com`).  

L’objectiu és fer un seguiment automatitzat dels preus dels llibres.

---

## Autor

**Eduard Altes**  
GitHub: [https://github.com/EduardAltes](https://github.com/EduardAltes)

---

## Repositori

[https://github.com/EduardAltes/python-llibres](https://github.com/EduardAltes/python-llibres)

---

## Requisits

- Python 3.7 o superior  
- Google Chrome instal·lat  
- Chromedriver compatible amb la versió de Chrome  
- Paquets Python:  
  - selenium  
  - requests

---

## Instal·lació

1. Clona aquest repositori:
    ```bash
    git clone https://github.com/EduardAltes/python-llibres.git
    cd python-llibres
   ```
2. Crea i activa un entorn virtual:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3. Instal·la les dependències:
    ```bash
    pip install -r requirements.txt
    ```
---
## Executa l’script i segueix les instruccions per consola:
```bash
python tracker.py
```
Introduïu el títol, autor o ISBN del llibre inclòs, si en tens, l’EAN13.

El script mostrarà el preu i enviarà la informació a l’API si el llibre està disponible.


## Estructura de la resposta JSON enviada
```bash
{
  "EAN13": "9788418928949",
  "url": "https://www.casadellibro.com/...",
  "ecommerce": "casadellibro",
  "status": "available",
  "price": 28.40
}
```
