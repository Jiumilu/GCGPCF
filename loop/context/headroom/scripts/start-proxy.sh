#!/usr/bin/env bash
set -euo pipefail

if [[ "${HEADROOM_PRODUCTION_PROXY:-false}" == "true" ]]; then
  echo "Refusing to start production proxy from local script." >&2
  exit 2
fi

export HEADROOM_TELEMETRY="${HEADROOM_TELEMETRY:-off}"
PORT="${HEADROOM_PROXY_PORT:-8787}"
NO_OPTIMIZE="${HEADROOM_PROXY_NO_OPTIMIZE:-true}"
NO_CCR_INJECT_TOOL="${HEADROOM_PROXY_NO_CCR_INJECT_TOOL:-true}"
ARGS=(proxy --port "${PORT}")

if [[ "${NO_OPTIMIZE}" == "true" ]]; then
  ARGS+=(--no-optimize)
fi

if [[ "${NO_CCR_INJECT_TOOL}" == "true" ]]; then
  ARGS+=(--no-ccr-inject-tool)
fi

echo "Starting Headroom dry-run proxy on port ${PORT}"
exec headroom "${ARGS[@]}"
