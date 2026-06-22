#!/usr/bin/env python3
"""Validate WAES/Harness admission decision checklist for Headroom LCX."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-checklist-20260622.md"
FIXTURES_JSON = ROOT / "fixtures/headroom/headroom-lcx-waes-harness-admission-decision-fixtures-20260622.json"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_waes_harness_admission_decision_checklist.py"

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

REQUIRED_CHECKS = [
    "authorization_complete",
    "missing_required_field_count_zero",
    "sanitized_ledger_exists",
    "sanitized_ledger_contains_no_raw_content",
    "rollback_plan_exists",
    "telemetry_off_required",
    "waes_harness_decision_required",
    "human_approval_required",
    "no_real_kds_write",
    "no_external_api_write",
    "no_sensitive_material_processing",
    "no_production_proxy",
    "accepted_false",
    "integrated_false",
    "production_ready_false",
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


def evaluate(candidate: dict) -> tuple[str, str]:
    if candidate.get("project_count") != 15 or candidate.get("projects") != PROJECTS:
        return "reject", "project_group_scope_must_be_15"
    checks = candidate.get("checks", {})
    for key in REQUIRED_CHECKS:
        if checks.get(key) is not True:
            if key == "human_approval_required":
                return "reject", "human_approval_required"
            if key == "no_real_kds_write":
                return "reject", "real_kds_write_not_allowed"
            if key == "no_external_api_write":
                return "reject", "external_api_write_not_allowed"
            if key == "no_sensitive_material_processing":
                return "reject", "sensitive_material_not_allowed"
            if key == "no_production_proxy":
                return "reject", "production_proxy_not_allowed"
            if key in {"accepted_false", "integrated_false", "production_ready_false"}:
                return "reject", "production_status_upgrade_not_allowed"
            return "reject", f"required_check_failed:{key}"
    actions = set(candidate.get("allowed_actions", []))
    forbidden_actions = set(candidate.get("forbidden_actions", []))
    for action in [
        "read_raw_prompt",
        "real_kds_api_write",
        "external_api_write",
        "production_proxy_start",
        "headroom_learn_apply",
    ]:
        if action in actions or action in forbidden_actions.intersection(actions):
            if action == "read_raw_prompt":
                return "reject", "sensitive_material_not_allowed"
            if action == "real_kds_api_write":
                return "reject", "real_kds_write_not_allowed"
            if action == "external_api_write":
                return "reject", "external_api_write_not_allowed"
            if action == "production_proxy_start":
                return "reject", "production_proxy_not_allowed"
            return "reject", "forbidden_action_not_allowed"
    if candidate.get("decision") != "admitted_for_sanitized_measurement_precheck":
        return "reject", "decision_must_match_requested_value"
    return "admit_for_next_precheck_only", "all_required_checks_pass"


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    fixtures = load_json(FIXTURES_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("REQUEST_JSON" in runner, "runner must read measurement admission request")
    require("APPROVAL_INSTANCE_JSON" in runner, "runner must read approval instance")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-20260622", "invalid evidence id")
    require(evidence.get("project_count") == 15 and evidence.get("projects") == PROJECTS, "evidence project scope mismatch")
    require(evidence.get("current_waes_harness_admission_decision") == "blocked", "current decision must remain blocked")
    require(evidence.get("required_checks") == REQUIRED_CHECKS, "required checks mismatch")
    require(fixtures.get("fixture_id") == "HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-FIXTURES-20260622", "invalid fixture id")
    require(fixtures.get("case_count") == 8, "fixture case count must be 8")
    require(fixtures.get("positive_case_count") == 1, "positive case count mismatch")
    require(fixtures.get("negative_case_count") == 7, "negative case count mismatch")
    require(fixtures.get("current_waes_harness_admission_decision") == "blocked", "fixtures must keep current decision blocked")

    admitted = 0
    rejected = 0
    for case in fixtures.get("cases", []):
        actual, reason = evaluate(case.get("candidate", {}))
        expected = case.get("expected")
        require(actual == expected, f"case {case.get('case_id')} expected {expected}, got {actual}:{reason}")
        if expected == "reject":
            require(reason == case.get("expected_reason"), f"case {case.get('case_id')} reason mismatch: {reason}")
            rejected += 1
        else:
            admitted += 1
    require(admitted == 1 and rejected == 7, "positive/negative result counts mismatch")

    gates = evidence.get("gates", {})
    require(gates.get("decision_checklist_gate") is True, "decision checklist gate must be true")
    require(gates.get("fixture_gate") is True, "fixture gate must be true")
    for key in [
        "waes_harness_admitted",
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

    for phrase in [
        "HEADROOM-LCX-WAES-HARNESS-ADMISSION-DECISION-CHECKLIST-20260622",
        "decision_checklist_gate | true",
        "fixture_gate | true",
        "positive_case_count | 1",
        "negative_case_count | 7",
        "current_waes_harness_admission_decision | blocked",
        "waes_harness_admitted | false",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_waes_harness_admission_decision_checklist.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_waes_harness_admission_decision_checklist.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_waes_harness_admission_decision_checklist=pass "
        "project_count=15 positive_case_count=1 negative_case_count=7 "
        "current_waes_harness_admission_decision=blocked "
        "waes_harness_admitted=false production_token_measurement_allowed=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
