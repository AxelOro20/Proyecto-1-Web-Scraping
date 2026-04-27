#!/usr/bin/env python
# Script de prueba simple para el scraper mejorado

import sys
sys.path.insert(0, r'c:\Users\OroCa\OneDrive\Escritorio\Portafolio\Proyecto-1-Web-Scraping')

# Importar y ejecutar
from scraper_ml_pro import scrape_tienda_generica
import pandas as pd

print("="*60)
print(" 🤖 PRUEBA DEL SCRAPER ANTIBOT MEJORADO (PLAYWRIGHT)")
print("="*60)

# Probar con Mercado Libre (sin Captcha)
print("\n🧪 Buscando 'laptop' en Mercado Libre...")

df = scrape_tienda_generica(
    query="laptop",
    url="https://listado.mercadolibre.com.mx/laptop",
    selector_tarjeta='div.poly-card, div.ui-search-result__wrapper',
    selector_titulo='h2, a.poly-component__title',
    selector_precio='span.andes-money-amount__fraction',
    tienda_nombre="Mercado Libre",
    selector_espera='div.poly-card'
)

if not df.empty:
    print(f"\n✅ ¡ÉXITO! Se extrajeron {len(df)} productos")
    print("\n📊 Primeros 5 resultados:")
    print(df.head())
    
    # Guardar
    nombre_archivo = "precios_mercadolibre_laptop_prueba.xlsx"
    df.to_excel(nombre_archivo, index=False)
    print(f"\n✅ Guardado en: {nombre_archivo}")
else:
    print("\n❌ No se extrajeron datos")
    print("Revisa la captura 'evidencia_mercado_libre.png' para diagnosticar")

