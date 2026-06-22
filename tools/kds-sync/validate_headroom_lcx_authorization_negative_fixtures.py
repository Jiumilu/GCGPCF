#!/usr/bin/env python3
"""Validate Headroom LCX authorization negative fixtures."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEGATIVE_FIXTURES_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-negative-fixtures.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-negative-fixtures-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_authorization_negative_fixtures.py"

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
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def reject_reason(candidate: dict) -> str | None:
    fields = candidate.get("authorization_fields", {})
    missing = [field for field in REQUIRED_FIELDS if field not in fields]
    if missing:
        return "missing_required_field"

    values = {field: fields[field].get("value") for field in REQUIRED_FIELDS}
    if any(value == "REQUIRED_USER_INPUT" for value in values.values()):
        return "placeholder_not_replaced"
    if not values["waes_harness_admission_decision"]:
        return "waes_harness_decision_required"
    if values["waes_harness_admission_decision"] not in {"admitted_for_sanitized_measurement_precheck", "blocked"}:
        return "waes_harness_decision_required"
    ledger_value = values["sanitized_production_token_ledger"]
    if not isinstance(ledger_value, str):
        return "sanitized_ledger_must_be_reference_only"
    if "inline" in ledger_value.lower() or "raw" in ledger_value.lower():
        return "sanitized_ledger_must_be_reference_only"

    false_until_completed = candidate.get("required_false_until_completed", {})
    for key in [
        "production_token_measurement_allowed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        if false_until_completed.get(key) is not False:
            return "template_cannot_grant_production"

    scope = candidate.get("scope", {})
    if scope.get("project_count") != 15 or scope.get("projects") != PROJECTS:
        return "project_group_scope_must_be_15"
    if scope.get("cross_project_memory_as_business_fact") is True:
        return "memory_cannot_be_business_fact_source"

    return None


def main() -> int:
    fixtures = load_json(NEGATIVE_FIXTURES_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("TEMPLATE_JSON" in runner, "runner must read authorization template")
    require(fixtures.get("fixture_id") == "HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622", "invalid fixture id")
    require(fixtures.get("project_count") == 15, "fixture project count mismatch")
    require(fixtures.get("projects") == PROJECTS, "fixture projects mismatch")
    cases = fixtures.get("cases", [])
    require(len(cases) == 7, "negative case count must be 7")

    rejected = 0
    for case in cases:
        case_id = case.get("case_id")
        expected = case.get("expected_rejection_reason")
        actual = reject_reason(case.get("candidate", {}))
        require(actual is not None, f"negative case was not rejected: {case_id}")
        require(actual == expected, f"case {case_id} expected {expected}, got {actual}")
        rejected += 1

    expected_result = fixtures.get("expected_result", {})
    require(expected_result.get("rejected") == rejected, "expected rejected count mismatch")
    require(expected_result.get("accepted") == 0, "negative fixtures must accept zero cases")
    for key in [
        "production_token_measurement_allowed",
        "production_admission_gate",
        "accepted_status",
        "integrated",
        "production_ready",
    ]:
        require(expected_result.get(key) is False, f"expected result must be false: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622", "invalid evidence id")
    require(evidence.get("case_count") == rejected, "evidence case count mismatch")
    require(evidence.get("expected_rejected") == rejected, "evidence rejected count mismatch")
    gates = evidence.get("gates", {})
    require(gates.get("negative_fixture_generation_gate") is True, "negative fixture generation gate must be true")
    for key in [
        "authorization_complete",
        "production_token_measurement_allowed",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "sensitive_material_processed",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(gates.get(key) is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-AUTHORIZATION-NEGATIVE-FIXTURES-20260622",
        "expected_rejected | 7",
        "expected_accepted | 0",
        "authorization_complete | false",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_authorization_negative_fixtures.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_authorization_negative_fixtures.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_authorization_negative_fixtures=pass "
        f"project_count=15 case_count={len(cases)} rejected={rejected} accepted=0 "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
