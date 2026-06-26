#!/usr/bin/env python3
"""Validate CodeGraph no-send dispatch precheck evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-no-send-dispatch-precheck-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-no-send-dispatch-precheck-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-NO-SEND-DISPATCH-PRECHECK-026.md"
DETAIL_INTAKE = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-precheck-detail-intake-20260626.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    intake = load_json(DETAIL_INTAKE)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-NO-SEND-DISPATCH-PRECHECK-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-NO-SEND-DISPATCH-PRECHECK-026", "invalid scope")
    require(evidence["status"] == "no_send_dispatch_precheck_passed_actual_dispatch_blocked", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(intake["status"] == "detail_intake_supplied_no_send_precheck_ready", "detail intake source mismatch")

    intake_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_dispatch_precheck_detail_intake.py"])
    require(intake_gate.returncode == 0, f"detail intake gate failed: {intake_gate.stdout}{intake_gate.stderr}")

    inputs = evidence["precheck_inputs"]
    require(inputs["recipient"] == "GPC_or_Liaoning_Yuanhang_order_owner", "recipient mismatch")
    require(inputs["channel"] == "manual_controlled_channel_pending_confirmation", "channel mismatch")
    require(inputs["payload_contains_real_input_request"] is True, "payload must contain real input request")
    require(inputs["payload_contains_rejected_substitutes"] is True, "payload must contain rejected substitutes")
    require("*.customer-requirement-platform-order.source-record.json" in inputs["evidence_destination"], "evidence destination mismatch")
    require(inputs["sensitive_data_review"] is False, "sensitive data review must remain false")
    require(inputs["rollback_or_cancellation_path_present"] is True, "rollback path must be present")

    results = evidence["precheck_results"]
    for key in [
        "recipient_present",
        "channel_is_manual_controlled_pending_confirmation",
        "payload_preview_available",
        "payload_has_no_external_send_instruction",
        "evidence_destination_is_controlled_intake_path",
        "rollback_or_cancellation_path_present",
        "sensitive_data_review_pending",
        "no_send_precheck_passed",
    ]:
        require(results[key] is True, f"{key} must be true")
    require(results["actual_dispatch_ready"] is False, "actual dispatch must not be ready")
    require("sensitive_data_review=false" in results["actual_dispatch_blocked_reason"], "blocked reason must mention sensitive review")

    for phrase in ["sensitive data review", "channel confirmation", "payload wording review"]:
        require(phrase in evidence["allowed_after_precheck"], f"missing allowed action: {phrase}")
    for phrase in ["actual dispatch", "external API write", "real KDS write", "git push", "business status upgrade"]:
        require(phrase in evidence["forbidden_after_precheck"], f"missing forbidden action: {phrase}")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "no_send_dispatch_precheck_passed_actual_dispatch_blocked",
        "sensitive_data_review=false",
        "channel_is_manual_controlled_pending_confirmation=true",
        "no_send_precheck_passed=true",
        "actual_dispatch_ready=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-SENSITIVE-REVIEW-027",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "no_send_dispatch_precheck_passed_actual_dispatch_blocked"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_no_send_dispatch_precheck=pass "
        "no_send_precheck_passed=true "
        "actual_dispatch_ready=false "
        "dispatch_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-SENSITIVE-REVIEW-027"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
