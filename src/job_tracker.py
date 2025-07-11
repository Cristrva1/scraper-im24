# -*- coding: utf-8 -*-
"""Gestiona jobs pendientes y completados."""
import json, os, datetime as dt
from pathlib import Path
from config import ESTADOS, OPERACIONES, PRODUCTOS, PAGINA, DAYS_DELTA, BASE_DIR

TRACK_FILE = Path(BASE_DIR) / "jobs.json"

def _today() -> str:
    return dt.date.today().isoformat()

def _next_due() -> str:
    return (dt.date.today() + dt.timedelta(days=DAYS_DELTA)).isoformat()

def _default_jobs():
    jobs = {}
    for est in ESTADOS:
        for op in OPERACIONES:
            for prod in PRODUCTOS:
                jid = f"{PAGINA}|{est}|{op}|{prod}"
                jobs[jid] = {"last_run": None, "next_due": _today(), "status": "pending"}
    return jobs

def _load():
    if TRACK_FILE.exists():
        return json.loads(TRACK_FILE.read_text())
    data = _default_jobs()
    TRACK_FILE.write_text(json.dumps(data, indent=2))
    return data

def _save(data):
    TRACK_FILE.write_text(json.dumps(data, indent=2))

def due_jobs(state_filter=None):
    data = _load()
    today = _today()
    for jid, meta in data.items():
        _, est, *_ = jid.split("|")
        if state_filter and est != state_filter:
            continue
        if meta["next_due"] <= today and meta["status"] != "running":
            meta["status"] = "running"
            _save(data)
            yield jid.split("|")

def mark_done(jid):
    data = _load()
    meta = data[jid]
    meta["last_run"] = _today()
    meta["next_due"] = _next_due()
    meta["status"]  = "done"
    _save(data)

def mark_error(jid):
    data = _load()
    data[jid]["status"] = "error"
    _save(data)
