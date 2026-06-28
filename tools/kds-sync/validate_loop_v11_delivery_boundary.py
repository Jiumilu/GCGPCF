#!/usr/bin/env python3
"""Validate LOOP v1.1 Delivery/Governance boundary.

This gate is intentionally narrow: it only prevents Delivery Loop over-governance,
real-source-record misblocking, and unsafe status promotion claims.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

EXECUTION_RULES = ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"
GATE_CLASSIFICATION = ROOT / "02-governance/loop/LOOP_GATE_CLASSIFICATION.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
TASK = ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.md"
MULTI_AGENT_TASK = ROOT / "docs/harness/tasks/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001.multi-agent.md"
EVIDENCE = ROOT / "docs/harness/evidence/GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001-evidence.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL validate_loop_v11_delivery_boundary: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def require_all(text: str, phrases: list[str], label: str) -> None:
    for phrase in phrases:
        require(phrase in text, f"{label} missing: {phrase}")


def extract_delivery_loop(text: str) -> str:
    match = re.search(r"```yaml\s+delivery_loop:\n(?P<body>.*?)```", text, re.S)
    require(match is not None, "evidence missing delivery_loop yaml block")
    return match.group("body")


def validate_execution_boundary() -> None:
    text = read(EXECUTION_RULES)
    require_all(
        text,
        [
            "policy_version: v1.1",
            "Delivery Loop 不强制展开 `run / stop / verify / recover / debug`",
            "goal / changed / verified / risk / next",
            "Delivery Loop 的 `risk` 字段必须显式声明是否触发 P0/P1",
            "Governance Loop 才强制展开",
            "run / stop / verify / recover / debug",
        ],
        "LOOP_EXECUTION_RULES",
    )


def validate_gate_classification() -> None:
    text = read(GATE_CLASSIFICATION)
    require_all(
        text,
        [
            "policy_version: v1.1",
            "`real_source_records = 0` 的门禁含义必须按状态线分类，不得再解释为开发阻断。",
            "local_development",
            "fixture_e2e",
            "dry_run",
            "contract_validator",
            "development_ready_for_real_business_validation",
            "accepted = false",
            "integrated = false",
            "production_ready = false",
            "customer_accepted = false",
        ],
        "LOOP_GATE_CLASSIFICATION",
    )


def validate_status_transmission() -> None:
    combined = read(CONTROL_BOARD) + "\n" + read(STATUS_MATRIX) + "\n" + read(TASK) + "\n" + read(MULTI_AGENT_TASK)
    require_all(
        combined,
        [
            "development_lane=continue_allowed",
            "real_business_validation_lane=pending_source_of_record",
            "real_source_records_zero_is_not_dev_blocker=true",
            "current_mainline=GFIS-RUNTIME-SOP-E2E-DEV-COMPLETION-001",
            "acceptance_lane=not_started",
            "production_lane=not_started",
            "execution_mode=controlled_multi_agent",
            "default_loop=Delivery Loop",
            "governance_level=G1",
            "multi_agent_phase=orchestrator_summary",
            "mode: controlled_multi_agent",
            "phase: orchestrator_summary",
            "orchestrator: LOOP Orchestrator",
            "Contract Agent",
            "Runtime Intake Agent",
            "Primary Key / Source Validation Agent",
            "Review Queue Agent",
            "WAES Candidate / Artifact Agent",
            "Boundary Validator Agent",
            "file_lock_required: true",
            "same_file_parallel_write_allowed: false",
            "orchestrator_only_files:",
            "development_ready_for_real_business_validation",
            "contract_defined: true",
            "controlled_sample_exists: true",
            "fixture_contract_valid: true",
            "contract_validator_passed: true",
            "runtime_intake_development: true",
            "runtime_intake_dry_run_passed: true",
            "primary_key_candidate_generated: true",
            "source_validation_passed: true",
            "review_queue_item_generated: true",
            "waes_review_candidate_generated: true",
            "verified_artifact_candidate_by_fixture: true",
            "verified_artifact_candidate_by_fixture_generated: true",
            "local_e2e_dry_run_passed: true",
            "delivery_boundary_validator_passed: true",
            "development_ready_for_real_business_validation: candidate",
            "real_source_records: 0",
            "valid_source_records: 0",
            "runtime_intake: 0",
            "review_queue: 0",
            "waes_review: 0",
            "verified: 0",
            "status: pending_source_of_record",
        ],
        "status transmission",
    )


def validate_delivery_evidence() -> None:
    text = read(EVIDENCE)
    body = extract_delivery_loop(text)
    require_all(body, ["goal:", "changed:", "verified:", "risk:", "next:"], "delivery_loop evidence")
    for forbidden_key in ["run:", "stop:", "recover:", "debug:"]:
        require(forbidden_key not in body, f"Delivery Loop evidence must not expand Governance key: {forbidden_key}")
    require_all(
        text,
        [
            "real_business_source_of_record_verified=false",
            "real_business_verified=false",
            "accepted=false",
            "integrated=false",
            "production_ready=false",
            "customer_accepted=false",
            "production_writes=0",
            "real_external_api_writes=0",
            "real_kds_writes=0",
            "real_waes_writes=0",
            "development_ready_for_real_business_validation=candidate",
            "fixture_e2e_passed=true",
            "contract_validator_passed=true",
            "execution_mode=controlled_multi_agent",
            "agent_count=7",
            "phase_a_readonly_design=true",
            "phase_b_controlled_implementation=true",
            "same_file_parallel_write_allowed=false",
            "controlled_sample_exists=true",
            "runtime_intake_dry_run_passed=true",
            "delivery_boundary_validator_passed=true",
        ],
        "GFIS DEV-COMPLETION evidence",
    )


def main() -> None:
    validate_execution_boundary()
    validate_gate_classification()
    validate_status_transmission()
    validate_delivery_evidence()
    print(
        "loop_v11_delivery_boundary=pass "
        "delivery_loop_fields=goal_changed_verified_risk_next "
        "real_source_records_zero_is_not_dev_blocker=true "
        "status_promotion=false"
    )


if __name__ == "__main__":
    main()
