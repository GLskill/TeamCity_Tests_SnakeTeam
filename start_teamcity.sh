#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/infra/docker_compose/docker-compose.yml"

echo "[start] Очищаем старое окружение..."
docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true

echo "[start] Запускаем окружение..."
docker compose -f "$COMPOSE_FILE" up -d --wait

echo "[start] Стримим логи тестов..."
docker compose -f "$COMPOSE_FILE" logs -f tests

EXIT_CODE=$(docker inspect teamcity-tests --format='{{.State.ExitCode}}')

echo "[start] Останавливаем окружение..."
docker compose -f "$COMPOSE_FILE" down -v

exit "$EXIT_CODE"
