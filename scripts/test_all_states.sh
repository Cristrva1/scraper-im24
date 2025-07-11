#!/usr/bin/env bash
# Lanza un contenedor por Estado, en segundo plano

estados=(
  "Jalisco"
  "Sinaloa"
  "Nuevo Leon"
  "Baja California Norte"
  "Baja California Sur"
  "Yucatan"
  "Queretaro"
  "Puebla"
)

for est in "${estados[@]}"; do
  echo "⏩ Lanzando $est …"
  docker compose run -d --rm \
    -e ESTADO="$est" \
    scraper --estado "$est"
done
