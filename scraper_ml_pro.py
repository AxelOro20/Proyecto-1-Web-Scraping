from playwright.sync_api import sync_playwright
import pandas as pd
import re

def limpiar_nombre_archivo(nombre):
    nombre_limpio = re.sub(r'[^A-Za-z0-9_\-\s]', '', nombre)
    return nombre_limpio.strip().lower().replace(' ', '_')

def scroll_y_esperar(page, veces=5, pausa_ms=1200):
    """Hace scroll gradual para disparar lazy loading."""
    for _ in range(veces):
        page.evaluate("window.scrollBy(0, window.innerHeight)")
        page.wait_for_timeout(pausa_ms)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(800)

def scrape_tienda_generica(query, url, selector_tarjeta, selector_titulo, selector_precio,
                            tienda_nombre, pausa_extra=0, selector_espera=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security',
            ]
        )

        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768},
            locale='es-MX',
        )
        # Oculta que somos Playwright
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = context.new_page()
        print(f"\n🚀 Navegando a {tienda_nombre} buscando: '{query}'...")
        page.goto(url, timeout=60000)

        # ── Pausa manual para Captcha / Login ──────────────────────────────
        if pausa_extra > 0:
            segundos = (4000 + pausa_extra) / 1000
            print(f"⏳ Tienes {segundos:.0f} segundos. Resuelve el Captcha o cierra el login si aparece.")
            page.wait_for_timeout(4000 + pausa_extra)

        # ── Esperar que cargue el primer resultado real ─────────────────────
        if selector_espera:
            try:
                page.wait_for_selector(selector_espera, timeout=20000)
                print("✅ Contenido detectado en pantalla.")
            except Exception:
                print("⚠️  Timeout esperando el selector. Intentando igual...")

        # ── Scroll para lazy loading ────────────────────────────────────────
        scroll_y_esperar(page)

        page.screenshot(path=f"evidencia_{tienda_nombre.lower().replace(' ', '_')}.png")

        products = []
        tarjetas = page.locator(selector_tarjeta).all()
        print(f"🔍 Se detectaron {len(tarjetas)} artículos. Extrayendo datos...")

        for tarjeta in tarjetas:
            title_loc = tarjeta.locator(selector_titulo).first
            title = title_loc.inner_text() if title_loc.count() > 0 else 'N/A'

            price_loc = tarjeta.locator(selector_precio).first
            price = price_loc.inner_text() if price_loc.count() > 0 else 'N/A'

            if title != 'N/A' and title.strip() != '':
                products.append({'Tienda': tienda_nombre, 'Título': title.strip(), 'Precio': price.strip()})

        browser.close()
        return pd.DataFrame(products)


def iniciar_programa():
    print("=" * 50)
    print(" 🤖 BROWSER SCRAPER PRO v3.3 - Anti-Block Edition ")
    print("=" * 50)

    print("\n¿En qué tienda deseas buscar?")
    print("1. Mercado Libre")
    print("2. Amazon")
    print("3. AliExpress")
    print("4. Shein")
    print("5. Temu")

    opcion = input("Ingresa el número de tu opción (1-5): ")
    tiendas = {'1': 'Mercado Libre', '2': 'Amazon', '3': 'AliExpress', '4': 'Shein', '5': 'Temu'}

    if opcion not in tiendas:
        print("\n⚠️ Opción no válida.")
        return

    producto = input(f"\n¿Qué producto estás buscando en {tiendas[opcion]}?: ")
    df = pd.DataFrame()

    if opcion == '1':
        url = f"https://listado.mercadolibre.com.mx/{producto.replace(' ', '%20')}"
        df = scrape_tienda_generica(
            producto, url,
            selector_tarjeta='div.poly-card, div.ui-search-result__wrapper',
            selector_titulo='h2, a.poly-component__title',
            selector_precio='span.andes-money-amount__fraction',
            tienda_nombre=tiendas[opcion],
            selector_espera='div.poly-card'
        )

    elif opcion == '2':
        url = f"https://www.amazon.com.mx/s?k={producto.replace(' ', '+')}"
        df = scrape_tienda_generica(
            producto, url,
            selector_tarjeta='div[data-component-type="s-search-result"]',
            selector_titulo='h2 span',
            selector_precio='span.a-price > span.a-offscreen',
            tienda_nombre=tiendas[opcion],
            selector_espera='div[data-component-type="s-search-result"]'
        )

    elif opcion == '3':
        # ── AliExpress: selectores más robustos con [class*=] ──────────────
        url = f"https://es.aliexpress.com/w/wholesale-{producto.replace(' ', '-')}.html"
        df = scrape_tienda_generica(
            producto, url,
            # El contenedor cambia, pero siempre tiene "item" en el class
            selector_tarjeta='[class*="SearchResults"] [class*="item"], a[class*="search-card-item"]',
            selector_titulo='[class*="title--"]',       # ← Shein/Ali usan hash en el nombre
            selector_precio='[class*="price--"]',
            tienda_nombre=tiendas[opcion],
            pausa_extra=8000,                           # Más tiempo por si pide CAPTCHA
            selector_espera='[class*="title--"]'
        )

    elif opcion == '4':
        # ── Shein: las clases llevan hash, usamos atributos de dato ───────
        url = f"https://www.shein.com.mx/pdsearch/{producto.replace(' ', '%20')}/"
        df = scrape_tienda_generica(
            producto, url,
            selector_tarjeta='[class*="product-card"], section[class*="product-item"]',
            selector_titulo='[class*="goods-title-link"], [class*="title-inside"]',
            selector_precio='[class*="normal-price-ctn"], [class*="sale-price"]',
            tienda_nombre=tiendas[opcion],
            pausa_extra=30000,                          # 34 seg para resolver captcha
            selector_espera='[class*="product-card"]'
        )

    elif opcion == '5':
        # ── Temu: toda la página llega vía JS, hay que esperar más ────────
        url = f"https://www.temu.com/mx/search_result.html?search_key={producto.replace(' ', '%20')}"
        df = scrape_tienda_generica(
            producto, url,
            selector_tarjeta='[class*="goods-item"], [data-testid="goods-item"]',
            selector_titulo='[class*="goods-title"], [class*="item-title"]',
            selector_precio='[class*="price-text"], [class*="sale-price"]',
            tienda_nombre=tiendas[opcion],
            pausa_extra=30000,
            selector_espera='[class*="goods-item"]'
        )

    # ── Guardado ───────────────────────────────────────────────────────────
    if not df.empty:
        nombre_archivo_usuario = input("\n¿Cómo quieres llamar a tu Excel? (Enter para nombre automático): ")
        if nombre_archivo_usuario == "":
            nombre_archivo = f"precios_{tiendas[opcion].replace(' ', '').lower()}_{limpiar_nombre_archivo(producto)}.xlsx"
        else:
            nombre_archivo = f"{limpiar_nombre_archivo(nombre_archivo_usuario)}.xlsx"

        df.to_excel(nombre_archivo, index=False)
        print(f"\n✅ ¡Éxito! Se guardaron {len(df)} productos en: {nombre_archivo}")
    else:
        print(f"\n❌ Tabla vacía. Revisa la captura 'evidencia_*.png'")
        print("   Si los productos SÍ se ven en la foto → los selectores cambiaron de nuevo.")
        print("   Abre DevTools (F12) > inspecciona un producto > copia su clase CSS.")


if __name__ == "__main__":
    iniciar_programa()