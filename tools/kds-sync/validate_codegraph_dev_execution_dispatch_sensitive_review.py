#!/usr/bin/env python3
"""Validate CodeGraph dispatch sensitive review evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-sensitive-review-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-dispatch-sensitive-review-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-SENSITIVE-REVIEW-027.md"
NO_SEND_PRECHECK = ROOT / "docs/harness/evidence/codegraph-dev-execution-no-send-dispatch-precheck-20260626.json"


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
    no_send = load_json(NO_SEND_PRECHECK)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-DISPATCH-SENSITIVE-REVIEW-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-SENSITIVE-REVIEW-027", "invalid scope")
    require(evidence["status"] == "sensitive_review_passed_actual_dispatch_blocked", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(no_send["status"] == "no_send_dispatch_precheck_passed_actual_dispatch_blocked", "no-send precheck source mismatch")

    no_send_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_no_send_dispatch_precheck.py"])
    require(no_send_gate.returncode == 0, f"no-send precheck gate failed: {no_send_gate.stdout}{no_send_gate.stderr}")

    subject = evidence["review_subject"]
    require(subject["recipient"] == "GPC_or_Liaoning_Yuanhang_order_owner", "recipient mismatch")
    require(subject["channel"] == "manual_controlled_channel_pending_confirmation", "channel mismatch")
    require("CustomerRequirementOrPlatformOrder" in subject["payload"], "payload must name target object")
    require("Reject quotation-only" in subject["payload"], "payload must reject weak substitutes")
    require("*.customer-requirement-platform-order.source-record.json" in subject["evidence_destination"], "evidence destination mismatch")

    review = evidence["sensitive_review"]
    require(review["sensitive_data_review_completed"] is True, "sensitive review must be completed")
    for key in [
        "contains_customer_personal_data",
        "contains_token_or_secret",
        "contains_production_credential",
        "contains_financial_amount_or_pricing",
        "contains_external_send_instruction",
        "contains_unverified_accepted_or_integrated_claim",
        "requires_payload_redaction",
    ]:
        require(review[key] is False, f"{key} must be false")
    require(review["review_result"] == "pass_for_no_send_payload_preview", "invalid review result")

    readiness = evidence["execution_readiness_after_review"]
    require(readiness["dispatch_precheck_authorized"] is True, "dispatch precheck must remain authorized")
    require(readiness["sensitive_data_review_completed"] is True, "sensitive review must be complete")
    for key in [
        "recipient_confirmed",
        "channel_confirmed",
        "actual_dispatch_authorized",
        "actual_dispatch_ready",
        "dispatch_allowed",
        "dispatch_performed",
    ]:
        require(readiness[key] is False, f"{key} must stay false")
    require("recipient/channel confirmation" in readiness["blocked_reason"], "blocked reason must mention recipient/channel confirmation")

    for phrase in ["recipient confirmation", "channel confirmation", "no-send dispatch readiness replay"]:
        require(phrase in evidence["allowed_next_action"], f"missing allowed action: {phrase}")
    for phrase in ["actual dispatch", "external API write", "real KDS write", "git push", "business status upgrade"]:
        require(phrase in evidence["forbidden_after_review"], f"missing forbidden action: {phrase}")

    benefit = evidence["benefit_proof_increment"]
    require(benefit["governance_to_execution_layer_step"] == "sensitive_review_gate_closed", "benefit step mismatch")
    require(benefit["manual_ambiguity_reduced"] is True, "manual ambiguity must be reduced")
    for blocker in ["recipient_confirmed=false", "channel_confirmed=false", "actual_dispatch_authorized=false"]:
        require(blocker in benefit["remaining_blockers"], f"missing remaining blocker: {blocker}")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "sensitive_review_passed_actual_dispatch_blocked",
        "sensitive_data_review_completed=true",
        "actual_dispatch_ready=false",
        "dispatch_performed=false",
        "GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-CHANNEL-CONFIRMATION-028",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "sensitive_review_passed_actual_dispatch_blocked"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_dispatch_sensitive_review=pass "
        "sensitive_data_review_completed=true "
        "actual_dispatch_ready=false "
        "dispatch_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-DISPATCH-CHANNEL-CONFIRMATION-028"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
