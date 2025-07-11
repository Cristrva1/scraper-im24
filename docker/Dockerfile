###############################################################################
# Dockerfile – Scraper Inmuebles24
# • Basado en selenium/standalone-chrome (incluye Chrome, Driver, Xvfb)
# • Añade Python 3, pip y las librerías del requirements.txt
###############################################################################
FROM selenium/standalone-chrome:123.0

USER root

# --- Instala Python 3, pip y Xvfb ---
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip xvfb && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    ln -sf /usr/bin/pip3     /usr/local/bin/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

# ---------- Instala dependencias Python -------------------------------------
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# ---------- Copia el código --------------------------------------------------
COPY src/ /src/
WORKDIR /src

ENTRYPOINT ["python", "runner.py"]
