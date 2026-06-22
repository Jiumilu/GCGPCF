#!/usr/bin/env python3
"""Validate the Headroom LCX sanitized measurement admission request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_measurement_admission_request.py"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("APPROVAL_INSTANCE_JSON" in runner, "runner must read approval instance")
    require("PRECHECK_JSON" in runner, "runner must read precheck evidence")
    require("LEDGER_JSON" in runner, "runner must read sanitized ledger")
    require("ROLLBACK_PLAN_MD" in runner, "runner must require rollback plan")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-20260622", "invalid evidence id")
    require(evidence.get("status") == "request_package_approved_for_sanitized_precheck_no_measurement", "invalid status")
    require(evidence.get("scope") == "waes_harness_admission_request_only_no_measurement", "invalid scope")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects") == PROJECTS, "project list mismatch")
    require(evidence.get("requested_decision") == "admitted_for_sanitized_measurement_precheck", "requested decision mismatch")
    require(
        evidence.get("current_waes_harness_admission_decision") == "admitted_for_sanitized_measurement_precheck",
        "current decision must be admitted for sanitized precheck",
    )

    preconditions = evidence.get("admission_preconditions", {})
    for key in [
        "authorization_complete",
        "missing_required_field_count_zero",
        "sanitized_ledger_exists",
        "sanitized_ledger_contains_no_raw_content",
        "rollback_plan_exists",
        "telemetry_off_required",
        "waes_harness_decision_required",
        "human_approval_required",
    ]:
        require(preconditions.get(key) is True, f"precondition must be true: {key}")

    boundary = evidence.get("requested_measurement_boundary", {})
    forbidden_content = set(boundary.get("forbidden_content", []))
    for item in ["raw_prompt", "raw_completion", "customer_contract", "pod", "financial_voucher", "secret", "production_credential"]:
        require(item in forbidden_content, f"forbidden content missing: {item}")
    forbidden_actions = set(boundary.get("forbidden_actions", []))
    for item in ["production_proxy_start", "real_kds_api_write", "external_api_write", "headroom_learn_apply", "memory_as_kds_fact_source"]:
        require(item in forbidden_actions, f"forbidden action missing: {item}")

    gates = evidence.get("gates", {})
    require(gates.get("request_package_generated") is True, "request package gate must be true")
    require(gates.get("authorization_complete") is True, "authorization_complete must be true")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")
    require(gates.get("waes_harness_admitted") is True, "WAES/Harness admission must be true for sanitized precheck")

    for phrase in [
        "HEADROOM-LCX-MEASUREMENT-ADMISSION-REQUEST-20260622",
        "request_package_generated | true",
        "authorization_complete | true",
        "waes_harness_admitted | true",
        "production_token_measurement_allowed | false",
        "measured_production_tokens | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
        "admitted_for_sanitized_measurement_precheck",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_measurement_admission_request.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_measurement_admission_request.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_measurement_admission_request=pass "
        "project_count=15 current_waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck "
        "waes_harness_admitted=true production_token_measurement_allowed=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
