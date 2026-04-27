import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mercadolibre(query):
    url = f"https://listado.mercadolibre.com.mx/{query}"
    
    # 1. El disfraz: Le decimos a la página que somos Google Chrome en Windows
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # Pasamos los headers en la petición
    response = requests.get(url, headers=headers)
    
    # Esto te dirá si la conexión fue exitosa (Debería imprimir 200)
    print(f"Estado de respuesta del servidor: {response.status_code}") 
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []
    
    # Buscamos las tarjetas de los productos
    resultados = soup.find_all('div', class_='ui-search-result__wrapper')
    
    if not resultados:
        print("Cuidado: No se encontraron productos. Mercado Libre pudo haber bloqueado la petición o cambiado sus clases HTML.")
        
    for item in resultados:
        # Extraer Título
        title_tag = item.find('h2')
        title = title_tag.text if title_tag else 'N/A'
        
        # Extraer Precio (intentamos con la clase nueva y la vieja por si acaso)
        price_tag = item.find('span', class_='andes-money-amount__fraction')
        if not price_tag:
            price_tag = item.find('span', class_='price-tag-fraction')
            
        price = price_tag.text if price_tag else 'N/A'
        
        products.append({'title': title, 'price': price})
    
    return pd.DataFrame(products)

# Uso
df = scrape_mercadolibre('laptop')

if not df.empty:
    df.to_excel('precios_laptops.xlsx', index=False)
    print("¡Scraping completado y guardado en Excel!")
else:
    print("No se creó el Excel porque la tabla está vacía.")