#!/bin/bash
set -e

CONTAINER_NAME="teamcity-server-instance"
AGENT_CONTAINER_NAME="teamcity-agent-instance"
NETWORK_NAME="teamcity-net"
TC_URL="http://localhost:8111"
TC_INTERNAL_URL="http://teamcity-server-instance:8111"
ENV_FILE="$PWD/.env"

# 1. Полная очистка старых контейнеров, сети и данных

for NAME in "$CONTAINER_NAME" "$AGENT_CONTAINER_NAME"; do
    if [ "$(docker ps -a -q -f name=$NAME)" ]; then
        echo "[start] Удаляем старый контейнер: $NAME..."
        docker rm -fv "$NAME"
    fi
done

if [ "$(docker network ls -q -f name=$NETWORK_NAME)" ]; then
    echo "[start] Удаляем старую сеть: $NETWORK_NAME..."
    docker network rm "$NETWORK_NAME"
fi

echo "[start] Очищаем локальные папки данных..."
rm -rf teamcity_data teamcity_logs teamcity_agent_conf
mkdir -p teamcity_data teamcity_logs teamcity_agent_conf
chmod -R 777 teamcity_data teamcity_logs teamcity_agent_conf

# 2. Создаём сеть

echo "[start] Создаём Docker-сеть $NETWORK_NAME..."
docker network create "$NETWORK_NAME"

# 3. Запуск TeamCity Server

echo "[start] Запускаем TeamCity Server..."
docker run -d --name "$CONTAINER_NAME" \
    --network "$NETWORK_NAME" \
    -v "$PWD/teamcity_data:/data/teamcity_server/datadir" \
    -v "$PWD/teamcity_logs:/opt/teamcity/logs" \
    -p 8111:8111 \
    jetbrains/teamcity-server

echo "[start] Контейнер сервера запущен. Ждём появления UI ($TC_URL)..."

# 4. Ждём, пока TeamCity поднимет HTTP (до 120 сек)

DEADLINE=$(( $(date +%s) + 120 ))
until curl -sfL "$TC_URL/mnt" -o /dev/null 2>/dev/null; do
    if [ "$(date +%s)" -ge "$DEADLINE" ]; then
        echo "[start] TeamCity не ответил за 120 сек. Выход."
        exit 1
    fi
    echo "[start] UI ещё не готов, ждём 5 сек..."
    sleep 5
done
echo "[start] UI доступен ✓"

# 5. Запускаем TeamCity Agent

echo "[start] Запускаем TeamCity Agent..."
docker run -d --name "$AGENT_CONTAINER_NAME" \
    --network "$NETWORK_NAME" \
    -e SERVER_URL="$TC_INTERNAL_URL" \
    -v "$PWD/teamcity_agent_conf:/data/teamcity_agent/conf" \
    jetbrains/teamcity-minimal-agent

echo "[start] Контейнер агента запущен ✓"

# 6. Запускаем скрипт настройки (UI wizard + авторизация агента)

echo "[setup] Запускаем set_up.py..."
UI_BASE_URL="$TC_URL" \
ENV_FILE="$ENV_FILE" \
TC_LOG_FILE="$PWD/teamcity_logs/teamcity-server.log" \
PYTHONPATH="$PWD" \
python3 infra/docker_compose/set_up.py

echo ""
echo "----------------------------------------------------"
echo "TeamCity готов к работе: $TC_URL"
echo "Credentials записаны в: $ENV_FILE"
echo "----------------------------------------------------"