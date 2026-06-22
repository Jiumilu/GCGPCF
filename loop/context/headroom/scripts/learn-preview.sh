#!/usr/bin/env bash
set -euo pipefail

export HEADROOM_TELEMETRY="${HEADROOM_TELEMETRY:-off}"
echo "Running Headroom learn in dry-run preview mode only."
exec headroom learn "$@"
