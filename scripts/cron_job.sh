#!/usr/bin/env bash
cd "$(dirname "$0")"/..
docker compose pull
docker compose up --build --abort-on-container-exit
docker image prune -f

