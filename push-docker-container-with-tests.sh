#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${ENV_FILE:-.env}"
IMAGE_NAME="${IMAGE_NAME:-teamcity-tests-version1}"
TAG="${TAG:-latest}"

read_env_value() {
  local key="$1"
  awk -F= -v key="$key" '
    $0 !~ /^[[:space:]]*#/ && $1 ~ "^[[:space:]]*" key "[[:space:]]*$" {
      value = substr($0, index($0, "=") + 1)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
      print value
      exit
    }
  ' "$ENV_FILE"
}

DOCKERHUB_USERNAME="${DOCKERHUB_USERNAME:-$(read_env_value DOCKERHUB_USERNAME)}"
DOCKERHUB_TOKEN="${DOCKERHUB_TOKEN:-$(read_env_value DOCKERHUB_TOKEN)}"

if [[ -z "$DOCKERHUB_USERNAME" || -z "$DOCKERHUB_TOKEN" ]]; then
  echo "DOCKERHUB_USERNAME and DOCKERHUB_TOKEN must be set in env or $ENV_FILE" >&2
  exit 1
fi

FULL_IMAGE_PATH="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

echo
echo "[1/3] Login to Docker Hub"
printf '%s' "$DOCKERHUB_TOKEN" | docker login --username "$DOCKERHUB_USERNAME" --password-stdin

echo
echo "[2/3] Build image: $FULL_IMAGE_PATH"
docker build -t "$FULL_IMAGE_PATH" .

echo
echo "[3/3] Push image"
docker push "$FULL_IMAGE_PATH"

echo
echo "Done: https://hub.docker.com/r/${DOCKERHUB_USERNAME}/${IMAGE_NAME}"
