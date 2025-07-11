# Scraper Inmuebles24 · SeleniumBase + Docker

Proyecto de scraping inmobiliario optimizado para ejecutarse **cada 15 días** y generar un CSV maestro con todos los anuncios de 8 estados.

#Hardware:
Dell PowerEdge T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy).1~Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)Hardware: (Dell T710 · Xeon E5620 (8 hilos) · 24 GB RAM(6x4gb) · RAID0-10 HDDs + Router Asus RT-AX82U, Ubuntu Server 24, no proxy)

## Tecnologías
- **Python 3.10** + SeleniumBase  
- **Docker** / Docker Compose  
- **GitHub Actions** (build & push)  

## Estructura
scraper-im24/
├── src/… # código Python
├── docker/… # Dockerfile
├── data/ # CSVs y jobs.json (git-ignorado)
└── scripts/… # cron_job.sh
## Flujo de scraping

```mermaid
graph TD
    subgraph Ciclo automático cada 15 días
        JT[job_tracker.py<br/>• lee jobs.json<br/>• marca pendientes] -->|ID + metadatos| LS[listing_scraper.py<br/>Parquet .urls]
        LS --> DS[detail_scraper.py<br/>Parquet .details]
        DS -->|marca done| JT
        JT -->|¿todos listos?| AGG[aggregator.py<br/>fusiona Parquet → CSV maestro]
    end

    AGG --> CSV((CSV maestro<br/>inmuebles24_YYYY-MM-DD.csv))
    CSV --> Rclone[(rclone<br/>gdrive:scraper-im24)]


## Uso rápido
```bash
git clone https://github.com/tuusuario/scraper-im24.git
cd scraper-im24
cp .env.example .env      # añade PROXY_URL cuando lo compres
docker compose build
docker compose up

# scraper-im24
