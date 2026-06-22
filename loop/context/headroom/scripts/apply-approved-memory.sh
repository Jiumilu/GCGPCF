#!/usr/bin/env bash
set -euo pipefail

APPROVAL_FILE="${1:-}"
if [[ -z "${APPROVAL_FILE}" || ! -f "${APPROVAL_FILE}" ]]; then
  echo "Usage: $0 <approved-memory-change.json>" >&2
  exit 2
fi

python3 - "$APPROVAL_FILE" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
required = ["approval_id", "owner", "target", "proposed_rule", "harness_evidence", "waes_decision"]
missing = [key for key in required if not data.get(key)]
if missing:
    raise SystemExit(f"missing required approval fields: {missing}")
if data.get("waes_decision") != "pass":
    raise SystemExit("WAES decision is not pass; refusing to apply memory")
print("approved_memory_candidate=validated apply_manually=true")
PY
