#!/usr/bin/env python3
"""Validate loop_document_gate exposes fixed doc_id drift as a gate field."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOOP_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"


def main() -> int:
    failures: list[str] = []
    source = LOOP_GATE.read_text(encoding="utf-8")
    if "fixed_doc_id_preservation" not in source:
        failures.append("loop_gate_missing_fixed_doc_id_preservation_check")
    if "fixed_doc_id_drift" not in source:
        failures.append("loop_gate_missing_fixed_doc_id_drift_summary")
    if "validate_gckf_p0_document_control_preserves_fixed_doc_id.py" not in source:
        failures.append("loop_gate_not_running_fixed_doc_id_validator")

    validator = subprocess.run(
        [sys.executable, "scripts/api/validate_gckf_p0_document_control_preserves_fixed_doc_id.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if validator.returncode != 0:
        failures.append("fixed_doc_id_validator_failed")

    gate = subprocess.run(
        [sys.executable, "tools/kds-sync/loop_document_gate.py", "--check-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        summary = json.loads(gate.stdout)
    except json.JSONDecodeError:
        failures.append("loop_gate_output_not_json")
        summary = {}

    if summary.get("fixed_doc_id_drift") is not False:
        failures.append("fixed_doc_id_drift_not_reported_false")
    if summary.get("gate") not in {"pass", "partial", "blocked", "rework_required"}:
        failures.append("loop_gate_status_unrecognized")

    if failures:
        print("gckf_p0_loop_document_gate_fixed_doc_id_check=fail")
        for failure in failures:
            print(failure)
        return 1

    print("gckf_p0_loop_document_gate_fixed_doc_id_check=pass")
    print(f"loop_gate_status={summary.get('gate')}")
    print("fixed_doc_id_drift=false")
    print("execution_mode=read_only_check_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
