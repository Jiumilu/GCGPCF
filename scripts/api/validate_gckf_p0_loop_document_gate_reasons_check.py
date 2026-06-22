#!/usr/bin/env python3
"""Validate loop_document_gate reports structured gate reasons."""

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
    for marker in [
        "build_gate_reasons",
        "gate_reasons",
        "localization_debt",
        "fixed_doc_id_drift",
        "kds_mirror_coverage_gap",
    ]:
        if marker not in source:
            failures.append(f"loop_gate_missing_{marker}")

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

    reasons = summary.get("gate_reasons")
    if not isinstance(reasons, list):
        failures.append("gate_reasons_not_list")
        reasons = []

    if summary.get("gate") == "rework_required" and not reasons:
        failures.append("rework_required_without_gate_reasons")
    if summary.get("localization_debt") is True and "localization_debt" not in reasons:
        failures.append("localization_debt_missing_from_gate_reasons")
    if summary.get("fixed_doc_id_drift") is False and "fixed_doc_id_drift" in reasons:
        failures.append("fixed_doc_id_false_but_reason_present")

    if failures:
        print("gckf_p0_loop_document_gate_reasons_check=fail")
        for failure in failures:
            print(failure)
        return 1

    print("gckf_p0_loop_document_gate_reasons_check=pass")
    print(f"loop_gate_status={summary.get('gate')}")
    print(f"gate_reasons={','.join(str(reason) for reason in reasons) or 'none'}")
    print(f"fixed_doc_id_drift={str(summary.get('fixed_doc_id_drift')).lower()}")
    print("execution_mode=read_only_check_only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
