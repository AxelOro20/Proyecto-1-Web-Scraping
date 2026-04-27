from playwright.sync_api import sync_playwright
import pandas as pd

def scrape_mercadolibre_playwright(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print(f"Abriendo Chrome para buscar: {query}...")
        page.goto(f"https://listado.mercadolibre.com.mx/{query}")
        
        # 1. Le damos 3 segundos al navegador para que renderice todo el texto
        page.wait_for_timeout(3000) 
        
        # 2. ¡Tomamos una foto de evidencia! (Excelente para depurar)
        page.screenshot(path="evidencia_scraping.png")
        print("📸 Foto tomada: Busca el archivo 'evidencia_scraping.png' en tu carpeta.")
        
        products = []
        
        # Capturamos todas las tarjetas
        tarjetas = page.locator('div.poly-card, div.ui-search-result__wrapper').all()
        print(f"🔍 Se detectaron {len(tarjetas)} tarjetas en la página.")
        
        for tarjeta in tarjetas:
            # 3. Solución: En lugar de solo 'h2', buscamos la clase específica del enlace que usa ML ahora
            elementos_titulo = tarjeta.locator('h2, a.poly-component__title')
            title = elementos_titulo.first.inner_text() if elementos_titulo.count() > 0 else 'N/A'
            
            # Extraemos el precio
            elementos_precio = tarjeta.locator('span.andes-money-amount__fraction, span.price-tag-fraction')
            price = elementos_precio.first.inner_text() if elementos_precio.count() > 0 else 'N/A'
            
            # Limpiamos los espacios en blanco (.strip()) y guardamos
            if title != 'N/A' and title.strip() != '':
                products.append({'Título': title.strip(), 'Precio': price.strip()})
                
        browser.close()
        return pd.DataFrame(products)

print("Iniciando extracción avanzada...")
df = scrape_mercadolibre_playwright('laptop')

if not df.empty:
    print("\n--- ¡Datos obtenidos con éxito! ---")
    print(df.head())
    df.to_excel('precios_laptops_playwright.xlsx', index=False)
    print("\n¡Guardado en Excel exitosamente!")
else:
    print("\nSigue sin extraer el texto. Abre la imagen 'evidencia_scraping.png' para investigar qué pasó.")