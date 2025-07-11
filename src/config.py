# -*- coding: utf-8 -*-
"""
Configuración global del scraper.
Se carga una vez y la usan todos los módulos.
"""
import os
from pathlib import Path

# Ruta base donde se guardan CSV, Parquet y jobs.json
BASE_DIR = Path(os.getenv("BASE_DIR", "/data")).resolve()
TMP_DIR  = BASE_DIR / "tmp"

# Crea carpetas si no existen
BASE_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR.mkdir(parents=True, exist_ok=True)

# Nombre del portal (útil si en el futuro añades más sitios)
PAGINA = "inmuebles24.com"

# Lista de estados a raspar
ESTADOS = [
    "Jalisco",
    "Sinaloa",
    "Nuevo Leon",
    "Baja California Norte",
    "Baja California Sur",
    "Yucatan",
    "Queretaro",
    "Puebla",
]

# Operaciones comerciales
OPERACIONES = {
    "Venta": "en-venta",
    "Renta": "en-renta",
}

# Productos / categorías (slug → slug)
PRODUCTOS = {
    "departamentos": "departamentos",
    "casas": "casas",
    "terrenos": "terrenos",
    "casa_en_condominio": "casa-en-condominio",
    "locales_comerciales": "locales-comerciales",
    "bodegas_comerciales": "bodegas-comerciales",
    "casa_uso_de_suelo": "casa-uso-de-suelo",
    "departamento_compartido": "departamento-compartido",
    "desarrollo_horizontal": "desarrollo-horizontal",
    "desarrollo_horizontal_vertical": "desarrollo-horizontal-vertical",
    "desarrollo_vertical": "desarrollo-vertical",
    "duplex": "duplex",
    "edificio": "edificio",
    "huerta": "huerta",
    "inmueble_productivo_urbano": "inmueble-productivo-urbano",
    "local_en_centro_comercial": "local-en-centro-comercial",
    "nave_industrial": "nave-industrial",
    "oficinas": "oficinas",
    "quinta": "quinta",
    "terreno_comercial": "terreno-comercial",
    "terreno_industrial": "terreno-industrial",
    "villa": "villa",
}

# Frecuencia (días) con la que debe repetirse cada scrape
DAYS_DELTA = 15
