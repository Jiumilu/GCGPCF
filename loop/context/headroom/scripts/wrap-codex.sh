#!/usr/bin/env bash
set -euo pipefail

if [[ "${HEADROOM_LEARN_APPLY:-false}" == "true" ]]; then
  echo "Refusing to run with automatic learn apply." >&2
  exit 2
fi

export HEADROOM_TELEMETRY="${HEADROOM_TELEMETRY:-off}"
export HEADROOM_OUTPUT_SHAPER="${HEADROOM_OUTPUT_SHAPER:-0}"
echo "Launching Codex through Headroom dry-run wrap. Production admission remains false."
exec headroom wrap codex "$@"
