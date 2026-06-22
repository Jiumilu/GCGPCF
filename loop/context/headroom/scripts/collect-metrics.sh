#!/usr/bin/env bash
set -euo pipefail

INPUT_JSON="${1:-fixtures/headroom/headroom-cost-measurement-template.json}"
python3 tools/kds-sync/calculate_headroom_cost_model.py "${INPUT_JSON}"
