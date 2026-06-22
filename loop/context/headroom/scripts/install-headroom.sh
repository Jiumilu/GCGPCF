#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${HEADROOM_LCX_VENV:-/tmp/gpcf-headroom-lcx}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "Installing Headroom into isolated environment: ${TARGET_DIR}"
"${PYTHON_BIN}" -m venv "${TARGET_DIR}"
"${TARGET_DIR}/bin/python" -m pip install --upgrade pip
HEADROOM_TELEMETRY=off "${TARGET_DIR}/bin/python" -m pip install "headroom-ai[all]"
echo "Headroom isolated install complete. Telemetry default remains off."
