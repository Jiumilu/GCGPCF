#!/usr/bin/env python3
"""Validate the Headroom LCX real measurement authorization request package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-request-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_authorization_request.py"

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

REQUIRED_FIELDS = [
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_token_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
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
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    builder = read(BUILDER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("EVIDENCE_CHAIN" in builder, "builder must define evidence chain")
    require("open_real_measurement_window" in builder, "builder must define requested future decision")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623", "invalid evidence id")
    require(evidence.get("status") == "real_measurement_authorization_request_blocked_until_real_window", "invalid status")
    require(evidence.get("scope") == "real_measurement_authorization_request_precheck_only", "invalid scope")
    require(evidence.get("project_count") == 15, "project count mismatch")
    require(evidence.get("projects") == PROJECTS, "project list mismatch")
    require(evidence.get("requested_future_decision") == "open_real_measurement_window", "requested future decision mismatch")
    require(evidence.get("current_waes_harness_admission_decision") == "admitted_for_sanitized_measurement_precheck", "current decision mismatch")

    bindings = evidence.get("field_bindings", [])
    require(isinstance(bindings, list) and len(bindings) == 6, "field binding count mismatch")
    require({item.get("field") for item in bindings} == set(REQUIRED_FIELDS), "field binding coverage mismatch")
    for item in bindings:
        require(item.get("binding_state") == "precheck_only", "binding state must be precheck_only")

    boundary = evidence.get("requested_boundary", {})
    for key in ["allowed_inputs", "forbidden_inputs", "allowed_actions", "forbidden_actions"]:
        require(isinstance(boundary.get(key), list) and boundary.get(key), f"boundary list missing: {key}")

    current_state = evidence.get("current_state", {})
    for key in [
        "real_measurement_gap_present",
        "production_branch_blocked",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(key in current_state, f"missing current state field: {key}")
    require(current_state.get("real_measurement_gap_present") is True, "real_measurement_gap_present must be true")
    require(current_state.get("production_branch_blocked") is True, "production_branch_blocked must be true")
    for key in [
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(current_state.get(key) is False, f"current state must be false: {key}")

    guard = evidence.get("execution_guard", {})
    require(guard.get("executable_now") is False, "execution must not be allowed now")
    for key in [
        "requires_real_measurement_authorization_window",
        "requires_waes_harness_decision",
        "requires_sanitized_token_ledger_metadata_only",
        "requires_rollback_plan_id",
        "requires_no_production_proxy",
        "requires_no_real_kds_write",
        "requires_no_external_api_write",
    ]:
        require(guard.get(key) is True, f"execution guard must be true: {key}")

    non_claims = evidence.get("non_claims", {})
    for key in [
        "real_measurement_open",
        "production_branch_open",
        "production_token_measurement_allowed",
        "measured_production_tokens",
        "accepted",
        "integrated",
        "production_ready",
        "business_answer_equivalence_proven",
    ]:
        require(non_claims.get(key) is False, f"non-claim must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-REQUEST-20260623",
        "requested_future_decision | open_real_measurement_window",
        "current_waes_harness_admission_decision | admitted_for_sanitized_measurement_precheck",
        "real_measurement_gap_present | true",
        "production_branch_blocked | true",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_real_measurement_authorization_request.py" in loop_round, "loop round missing builder command")
    require("validate_headroom_lcx_real_measurement_authorization_request.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_real_measurement_authorization_request=pass_check_only "
        "project_count=15 requested_future_decision=open_real_measurement_window "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
