#!/usr/bin/env bash
# Script to build and start the compose stack from project root.
# Usage (from project root): sudo ./deploy/up.sh  OR ./deploy/up.sh (if your user is in docker group)

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/deploy/docker-compose.yml"

echo "==> Using compose file: $COMPOSE_FILE"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker not found. Please run deploy/setup_server.sh on the server first."
  exit 1
fi

echo "==> Building and starting containers"
docker compose -f "$COMPOSE_FILE" up -d --build

echo "==> Showing status (docker ps)"
docker ps --filter "name=$(basename $ROOT_DIR)" || docker ps

echo "If something fails, check logs: docker compose -f $COMPOSE_FILE logs -f web"
