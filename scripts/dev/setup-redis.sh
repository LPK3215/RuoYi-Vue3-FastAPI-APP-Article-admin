#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
RUNTIME_REDIS_DIR="${REPO_ROOT}/.runtime/redis"
RUNTIME_REDIS_DATA_DIR="${RUNTIME_REDIS_DIR}/data"
VERSION_FILE="${SCRIPT_DIR}/redis-version.json"

read_json_string() {
  local key="$1"
  sed -nE "s/^[[:space:]]*\"${key}\"[[:space:]]*:[[:space:]]*\"([^\"]+)\"[[:space:]]*,?[[:space:]]*$/\1/p" "${VERSION_FILE}" | head -n 1
}

default_image="redis:7.4.8"
default_container_name="ruoyi-redis-local"

if [[ -f "${VERSION_FILE}" ]]; then
  default_image="$(read_json_string image || true)"
  default_container_name="$(read_json_string containerName || true)"
fi

IMAGE="${1:-${default_image:-redis:7.4.8}}"
CONTAINER_NAME="${2:-${default_container_name:-ruoyi-redis-local}}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker 未安装或未加入 PATH，请先安装 Docker Desktop / Docker Engine。" >&2
  exit 1
fi

mkdir -p "${RUNTIME_REDIS_DATA_DIR}"

echo "Pulling Redis image ${IMAGE} ..."
docker pull "${IMAGE}"

printf '%s\n%s\n' "${IMAGE}" "${CONTAINER_NAME}" > "${RUNTIME_REDIS_DIR}/redis-image.txt"

echo "OK: Redis image is ready (${IMAGE})"
echo "Data directory: ${RUNTIME_REDIS_DATA_DIR}"
