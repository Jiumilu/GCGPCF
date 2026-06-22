#!/usr/bin/env python3
"""Validate Headroom LCX approval package instance precheck."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json"
INSTANCE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json"
NEGATIVE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json"
LEDGER_JSON = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
ROLLBACK_PLAN = ROOT / "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md"
WAES_DECISION = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py"

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

REQUIRED_ATTESTATIONS = [
    "telemetry_off_confirmed",
    "sanitized_ledger_reference_only",
    "no_sensitive_raw_material",
    "no_real_kds_write",
    "no_external_api_write",
    "rollback_plan_reviewed",
    "waes_harness_evidence_attached",
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
    if candidate.get("project_count") != 15 or candidate.get("projects") != PROJECTS:
        return "project_group_scope_must_be_15"

    fields = candidate.get("authorization_fields", {})
    missing = [field for field in REQUIRED_FIELDS if field not in fields]
    if missing:
        return "missing_required_field"
    if any(fields.get(field) == "REQUIRED_USER_INPUT" for field in REQUIRED_FIELDS):
        return "placeholder_not_replaced"
    if not str(fields.get("authorized_window_id", "")).startswith("LCX-MEASURE-"):
        return "invalid_authorized_window_id"
    ledger = fields.get("sanitized_production_token_ledger")
    if not isinstance(ledger, str):
        return "sanitized_ledger_must_be_reference_only"
    if "raw" in ledger.lower() or "inline" in ledger.lower():
        return "sanitized_ledger_must_be_reference_only"
    if fields.get("waes_harness_admission_decision") not in {"admitted_for_sanitized_measurement_precheck", "blocked"}:
        return "waes_harness_decision_required"

    attestations = candidate.get("human_attestations", {})
    if set(attestations) != set(REQUIRED_ATTESTATIONS):
        return "missing_required_attestation"
    if any(attestations.get(key) == "REQUIRED_USER_INPUT" for key in REQUIRED_ATTESTATIONS):
        return "placeholder_not_replaced"

    false_until_completed = candidate.get("required_false_until_completed", {})
    for key in ["production_token_measurement_allowed", "production_admission_gate", "accepted", "integrated", "production_ready"]:
        if false_until_completed.get(key) is not False:
            return "approval_package_cannot_grant_production"
    return None


def require_instance_complete(instance: dict) -> None:
    require(reject_reason(instance) is None, "approval instance must pass schema-level field validation")
    require(instance.get("instance_status") == "precheck_only_authorization_fields_complete_waes_harness_admitted", "instance status mismatch")
    require(
        instance.get("schema_validation_expected") == "pass_fields_complete_waes_harness_admitted_for_sanitized_precheck_no_measurement",
        "instance schema expectation mismatch",
    )
    fields = instance.get("authorization_fields", {})
    require(fields.get("authorized_window_id") == "LCX-MEASURE-20260622-001", "authorized window mismatch")
    require(fields.get("authorized_by") == "lujunxiang / GPCF owner", "authorized_by mismatch")
    require(fields.get("authorized_at") == "2026-06-22T08:42:06+08:00", "authorized_at mismatch")
    require(fields.get("sanitized_production_token_ledger") == LEDGER_JSON.relative_to(ROOT).as_posix(), "ledger reference mismatch")
    require(fields.get("rollback_plan_id") == "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001", "rollback plan id mismatch")
    require(
        fields.get("waes_harness_admission_decision") == "admitted_for_sanitized_measurement_precheck",
        "WAES/Harness decision must admit sanitized precheck",
    )


def main() -> int:
    schema = load_json(SCHEMA_JSON)
    instance = load_json(INSTANCE_JSON)
    negative = load_json(NEGATIVE_JSON)
    ledger = load_json(LEDGER_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    rollback_plan = read(ROLLBACK_PLAN)
    waes_decision = read(WAES_DECISION)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("SCHEMA_JSON" in runner and "PACKAGE_TEMPLATE_JSON" in runner, "runner must read schema and approval package template")
    require(schema.get("scope", {}).get("projects") == PROJECTS, "schema project scope mismatch")

    require(instance.get("instance_id") == "HEADROOM-LCX-HUMAN-APPROVAL-PACKAGE-INSTANCE-PENDING-20260622", "invalid pending instance id")
    require_instance_complete(instance)
    require(ledger.get("ledger_id") == "HEADROOM-LCX-SANITIZED-PRODUCTION-TOKEN-LEDGER-PRECHECK-20260622", "invalid ledger id")
    require(ledger.get("measured_production_tokens") is False, "ledger must not measure production tokens")
    require(ledger.get("production_token_measurement_allowed") is False, "ledger must block production token measurement")
    require("HEADROOM-LCX-ROLLBACK-PLAN-20260622-001" in rollback_plan, "rollback plan id missing")
    require(
        "waes_harness_admission_decision | admitted_for_sanitized_measurement_precheck" in waes_decision,
        "WAES/Harness decision evidence must admit sanitized precheck",
    )

    cases = negative.get("cases", [])
    require(negative.get("fixture_id") == "HEADROOM-LCX-APPROVAL-INSTANCE-NEGATIVE-FIXTURES-20260622", "invalid negative fixture id")
    require(len(cases) == 7, "negative case count must be 7")
    rejected = 0
    for case in cases:
        actual = reject_reason(case.get("candidate", {}))
        expected = case.get("expected_rejection_reason")
        require(actual == expected, f"case {case.get('case_id')} expected {expected}, got {actual}")
        rejected += 1

    require(evidence.get("evidence_id") == "HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622", "invalid evidence id")
    require(evidence.get("negative_case_count") == rejected, "evidence negative case count mismatch")
    gates = evidence.get("gates", {})
    require(gates.get("approval_instance_template_generated") is True, "approval instance template gate must be true")
    require(gates.get("approval_instance_precheck_gate") is True, "approval instance precheck gate must be true for completed fields")
    require(gates.get("negative_instance_fixture_gate") is True, "negative instance fixture gate must be true")
    require(gates.get("authorization_complete") is True, "authorization fields must be complete for precheck-only")
    for key in [
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
        "HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-20260622",
        "approval_instance_template_generated | true",
        "approval_instance_precheck_gate | true",
        "negative_instance_fixture_gate | true",
        "authorization_complete | true",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_approval_instance_precheck.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_approval_instance_precheck.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_approval_instance_precheck=pass_precheck_only "
        f"project_count=15 negative_case_count={rejected} rejected={rejected} "
        "approval_instance_precheck_gate=true authorization_complete=true waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
