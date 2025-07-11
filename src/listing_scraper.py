#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
listing_scraper.py
Genera un Parquet con las URLs listadas en una página de resultados.
Se usa como función desde runner.py, pero también puede ejecutarse suelto.
"""
from __future__ import annotations
import random, time, argparse, datetime as dt
from uuid import uuid4
from pathlib import Path
import os
import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import TMP_DIR

# —— Parámetros anti-bot —————————————————————————
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
]
RANDOM_DELAY = (2, 5)   # segundos
MAX_PAGES = int(os.getenv("MAX_PAGES", 75))   # ← ahora se lee de env
TIMEOUT      = 45

# —— Driver utilitario ———————————————————————————
def get_driver(proxy_url: str | None) -> Driver:
    drv = Driver(uc=True, headless=True, block_images=True)
    if proxy_url:
        drv.driver.options.add_argument(f"--proxy-server={proxy_url}")
    drv.set_page_load_timeout(TIMEOUT)
    return drv

# —— Función principal ———————————————————————————
def scrape_listings(start_url: str, proxy_url: str | None = None) -> Path:
    """
    Devuelve Ruta<Parquet> con la columna 'url'.
    """
    out_parquet = TMP_DIR / f"listings_{uuid4().hex}.parquet"
    driver      = get_driver(proxy_url)
    all_urls: list[str] = []

    for page in range(1, MAX_PAGES + 1):
        url = start_url.replace(".html", f"-pagina-{page}.html")
        try:
            driver.get(url)
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
            )
            cards = driver.find_elements(By.CSS_SELECTOR, "article")
            if not cards:
                break  # fin de paginación
            all_urls += [
                c.get_attribute("data-to-posting")
                for c in cards
                if c.get_attribute("data-to-posting")
            ]
            time.sleep(random.uniform(*RANDOM_DELAY))
        except Exception:
            break

    driver.quit()
    pd.DataFrame({"url": all_urls}).drop_duplicates().to_parquet(
        out_parquet, compression="gzip", index=False
    )
    return out_parquet

# —— CLI opcional ———————————————————————————————
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="URL página 1")
    args = ap.parse_args()
    path = scrape_listings(args.url)
    print(f"[OK] Guardado {path}")
