#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
detail_scraper.py
Lee un Parquet de URLs, abre cada anuncio en Chrome (Xvfb),
extrae los campos y guarda otro Parquet comprimido.
"""
from __future__ import annotations
import random, time, argparse
from uuid import uuid4
from pathlib import Path

import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import TMP_DIR

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) "
    "Gecko/20100101 Firefox/126.0",
]
RANDOM_DELAY = (3, 7)
TIMEOUT      = 60

def get_driver(proxy_url: str | None) -> Driver:
    drv = Driver(uc=True, headless=True, block_images=True)   # headless=True
    if proxy_url:
        drv.driver.options.add_argument(f"--proxy-server={proxy_url}")
    drv.set_page_load_timeout(TIMEOUT)
    return drv


def close_cookie(driver: Driver):
    try:
        b = driver.find_element(By.CSS_SELECTOR, "[id^='qc-cmp2']")
        if b.is_displayed():
            driver.execute_script("arguments[0].remove();", b)
    except Exception:
        pass

def extract_details(driver: Driver) -> dict:
    # —— Ejemplo de 3 campos; añade los tuyos ——
    data = {}
    try:
        data["precio"] = driver.find_element(By.CSS_SELECTOR, "h2.price-tag").text
    except Exception:
        data["precio"] = ""
    try:
        data["titulo"] = driver.find_element(By.CSS_SELECTOR, "h1").text
    except Exception:
        data["titulo"] = ""
    data["recopilado"] = time.strftime("%Y-%m-%d")
    return data

def scrape_details(listing_parquet: Path, proxy_url: str | None = None) -> Path:
    out_parquet = TMP_DIR / f"details_{uuid4().hex}.parquet"
    df_urls     = pd.read_parquet(listing_parquet)
    results: list[dict] = []

    driver  = get_driver(proxy_url)
    actions = ActionChains(driver)

    for url in df_urls["url"]:
        try:
            driver.get(url)
            close_cookie(driver)
            actions.move_by_offset(30, 30).perform()  # “tocar” la página
            time.sleep(random.uniform(0.8, 1.4))
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            data = extract_details(driver)
            data["url"] = url
            results.append(data)
            time.sleep(random.uniform(*RANDOM_DELAY))
        except Exception:
            continue

    driver.quit()
    pd.DataFrame(results).to_parquet(
        out_parquet, compression="gzip", index=False
    )
    return out_parquet

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--parquet", required=True, help="Listado Parquet")
    args = ap.parse_args()
    path = scrape_details(Path(args.parquet))
    print(f"[OK] Guardado {path}")
