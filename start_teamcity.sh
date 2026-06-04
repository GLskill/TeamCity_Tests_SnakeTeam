#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/infra/docker_compose/docker-compose.yml"

echo "[start] Очищаем старое окружение..."
docker compose -f "$COMPOSE_FILE" down -v 2>/dev/null || true
rm -rf "$SCRIPT_DIR/allure-results" "$SCRIPT_DIR/allure-report"
mkdir -p "$SCRIPT_DIR/allure-results"

echo "[start] Запускаем окружение..."
docker compose -f "$COMPOSE_FILE" up -d --wait

echo "[start] Стримим логи тестов..."
docker compose -f "$COMPOSE_FILE" logs -f tests

EXIT_CODE=$(docker inspect teamcity-tests --format='{{.State.ExitCode}}')

echo "[start] Останавливаем окружение..."
docker compose -f "$COMPOSE_FILE" down -v

echo "[report] Генерируем Allure отчёт..."
if command -v allure &>/dev/null; then
    cd ~
    allure generate "$SCRIPT_DIR/allure-results" -o "$SCRIPT_DIR/allure-report" --clean
    echo "[report] ✅ Отчёт готов!"
    echo "[report]    Запускаем сервер отчёта..."
    cd "$SCRIPT_DIR/allure-report"
    python3 -m http.server 5050 &
    SERVER_PID=$!
    sleep 1
    cmd.exe /c start http://localhost:5050
    echo "[report]    Отчёт открыт: http://localhost:5050"
    echo "[report]    Для остановки сервера нажми Ctrl+C"
    wait $SERVER_PID
else
    echo "[report] ⚠️  Allure CLI не установлен. Результаты в папке: allure-results/"
    echo "[report]    Установи: https://allurereport.org/docs/install/"
fi

exit "$EXIT_CODE"
