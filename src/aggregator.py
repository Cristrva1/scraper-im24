#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Funde todos los Parquet de detalles en un
CSV maestro —ejecutado una sola vez al final del ciclo.
"""
import glob, datetime as dt, fcntl
from pathlib import Path

import pandas as pd

from config import TMP_DIR, BASE_DIR, PAGINA

CHUNK = 50_000  # filas por lote

def merge_tmp_parquet() -> Path:
    fecha = dt.date.today().isoformat()
    master_csv = BASE_DIR / f"{PAGINA}_{fecha}.csv"

    parquet_files = glob.glob(str(TMP_DIR / "details_*.parquet"))
    if not parquet_files:
        print("[WARN] No hay archivos Parquet temporales.")
        return master_csv

    # bloqueo exclusivo
    with open(master_csv, "a") as lockfile:
        fcntl.flock(lockfile, fcntl.LOCK_EX)

    first = True
    for pq in parquet_files:
        df = pd.read_parquet(pq)
        for i in range(0, len(df), CHUNK):
            df.iloc[i : i + CHUNK].to_csv(
                master_csv, mode="a", header=first, index=False
            )
            first = False
        Path(pq).unlink()  # borra Parquet

    print(f"[OK] CSV maestro → {master_csv}")
    return master_csv

if __name__ == "__main__":
    merge_tmp_parquet()
