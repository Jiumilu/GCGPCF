#!/usr/bin/env python3
"""Validate CodeGraph dispatch precheck detail intake evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-precheck-detail-intake-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-precheck-detail-intake-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-025.md"
RESUMED = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-authorization-answer-resumed-20260626.json"


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
    resumed = load_json(RESUMED)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-PRECHECK-DETAIL-INTAKE-025", "invalid scope")
    require(evidence["status"] == "detail_intake_supplied_no_send_precheck_ready", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(resumed["status"] == "actual_dispatch_later_intent_recorded_details_missing", "resumed source status mismatch")

    resumed_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_dispatch_authorization_answer_resumed.py"])
    require(resumed_gate.returncode == 0, f"resumed answer gate failed: {resumed_gate.stdout}{resumed_gate.stderr}")

    intake = evidence["detail_intake"]
    require(intake["recipient"] == "GPC_or_Liaoning_Yuanhang_order_owner", "recipient mismatch")
    require(intake["channel"] == "manual_controlled_channel_pending_confirmation", "channel mismatch")
    require("Request real source input for CustomerRequirementOrPlatformOrder" in intake["payload"], "payload missing request")
    require("Reject quotation-only" in intake["payload"], "payload missing rejection rule")
    require("*.customer-requirement-platform-order.source-record.json" in intake["evidence_destination"], "evidence destination mismatch")
    require("No-send precheck only" in intake["rollback_or_cancellation_path"], "rollback path missing no-send guard")
    require(intake["sensitive_data_review"] is False, "sensitive data review must be false")
    require(intake["owner_confirmation_required"] is True, "owner confirmation must be required")
    require(intake["no_send_precheck_only"] is True, "only no-send precheck is allowed")

    for key, value in evidence["completion_requirements"].items():
        require(value is True, f"{key} must be required")

    auth = evidence["current_authorization"]
    require(auth["selected_option"] == "authorize_actual_dispatch_later", "selected option mismatch")
    require(auth["dispatch_precheck_authorized"] is True, "precheck must be authorized")
    require(auth["actual_dispatch_authorized"] is False, "actual dispatch must not be authorized")
    require(auth["dispatch_allowed"] is False, "dispatch must not be allowed")
    require(auth["dispatch_performed"] is False, "dispatch must not be performed")

    require(evidence["allowed_next_action_after_details"] == "no_send_dispatch_precheck", "invalid next action")
    for phrase in ["actual dispatch", "external API write", "real KDS write", "git push", "business status upgrade"]:
        require(phrase in evidence["forbidden_until_details_validated"], f"missing forbidden action: {phrase}")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "detail_intake_supplied_no_send_precheck_ready",
        "recipient=GPC_or_Liaoning_Yuanhang_order_owner",
        "channel=manual_controlled_channel_pending_confirmation",
        "sensitive_data_review=false",
        "selected_option=authorize_actual_dispatch_later",
        "actual_dispatch_authorized=false",
        "dispatch_performed=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-NO-SEND-DISPATCH-PRECHECK-026",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "detail_intake_supplied_no_send_precheck_ready"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_dispatch_precheck_detail_intake=pass "
        "status=detail_intake_supplied_no_send_precheck_ready "
        "dispatch_precheck_authorized=true "
        "actual_dispatch_authorized=false "
        "dispatch_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-NO-SEND-DISPATCH-PRECHECK-026"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
