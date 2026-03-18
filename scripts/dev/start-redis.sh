#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
RUNTIME_REDIS_DATA_DIR="${REPO_ROOT}/.runtime/redis/data"
VERSION_FILE="${SCRIPT_DIR}/redis-version.json"

read_json_string() {
  local key="$1"
  sed -nE "s/^[[:space:]]*\"${key}\"[[:space:]]*:[[:space:]]*\"([^\"]+)\"[[:space:]]*,?[[:space:]]*$/\1/p" "${VERSION_FILE}" | head -n 1
}

read_json_number() {
  local key="$1"
  sed -nE "s/^[[:space:]]*\"${key}\"[[:space:]]*:[[:space:]]*([0-9]+)[[:space:]]*,?[[:space:]]*$/\1/p" "${VERSION_FILE}" | head -n 1
}

default_image="redis:7.4.8"
default_container_name="ruoyi-redis-local"
default_port="6379"

if [[ -f "${VERSION_FILE}" ]]; then
  default_image="$(read_json_string image || true)"
  default_container_name="$(read_json_string containerName || true)"
  default_port="$(read_json_number port || true)"
fi

IMAGE="${1:-${default_image:-redis:7.4.8}}"
CONTAINER_NAME="${2:-${default_container_name:-ruoyi-redis-local}}"
PORT="${3:-${default_port:-6379}}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker 未安装或未加入 PATH，请先安装 Docker Desktop / Docker Engine。" >&2
  exit 1
fi

mkdir -p "${RUNTIME_REDIS_DATA_DIR}"

existing_status="$(docker ps -a --filter "name=^/${CONTAINER_NAME}$" --format '{{.Status}}')"
if [[ -n "${existing_status}" ]]; then
  if [[ "${existing_status}" == Up* ]]; then
    echo "OK: redis already running in container ${CONTAINER_NAME} (127.0.0.1:${PORT})"
    exit 0
  fi
  docker start "${CONTAINER_NAME}" >/dev/null
else
  docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:6379" \
    -v "${RUNTIME_REDIS_DATA_DIR}:/data" \
    "${IMAGE}" \
    redis-server --appendonly yes >/dev/null
fi

for _ in $(seq 1 20); do
  if [[ "$(docker exec "${CONTAINER_NAME}" redis-cli ping 2>/dev/null || true)" == "PONG" ]]; then
    echo "OK: redis started in container ${CONTAINER_NAME} (127.0.0.1:${PORT})"
    exit 0
  fi
  sleep 0.5
done

echo "Redis 容器已启动，但健康检查未通过：${CONTAINER_NAME}" >&2
exit 1
