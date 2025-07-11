#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
runner.py
Orquesta: job_tracker → listings → detalles → marcar done → fusión al final.
"""
import os, argparse, unicodedata
from pathlib import Path

from config import (
    OPERACIONES,
    PRODUCTOS,
    PAGINA,
)
import job_tracker as JT  # tu archivo permanece igual

from listing_scraper import scrape_listings
from detail_scraper import scrape_details
from aggregator import merge_tmp_parquet

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return text.lower().replace(" ", "-")

def build_url(est_slug: str, op_slug: str, prod_slug: str) -> str:
    return f"https://www.inmuebles24.com/{prod_slug}-{op_slug}-en-{est_slug}.html"

def main(estado_filtrado: str | None = None):
    proxy = os.getenv("PROXY_URL")  # vacío → IP host
    pendientes = list(JT.due_jobs(estado_filtrado))
    for pagina, estado, operacion, producto in pendientes:
        jid = f"{pagina}|{estado}|{operacion}|{producto}"
        try:
            url = build_url(
                slugify(estado),
                OPERACIONES[operacion],
                PRODUCTOS[producto],
            )
            listado = scrape_listings(url, proxy)
            scrape_details(listado, proxy)
            JT.mark_done(jid)
        except Exception as e:
            print(f"[ERR] {jid}: {e}")
            JT.mark_error(jid)

    # Si ya no quedan trabajos pendientes, fusiona Parquet → CSV
    if not list(JT.due_jobs(estado_filtrado)):
        merge_tmp_parquet()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--estado", help="Sólo este estado (para varios pods)")
    args = ap.parse_args()
    main(args.estado)
