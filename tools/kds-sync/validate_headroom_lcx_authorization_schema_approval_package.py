#!/usr/bin/env python3
"""Validate Headroom LCX authorization schema and approval package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization.schema.json"
APPROVAL_PACKAGE_JSON = ROOT / "fixtures/headroom/headroom-lcx-human-approval-package-template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_authorization_schema_approval_package.py"

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


def main() -> int:
    schema = load_json(SCHEMA_JSON)
    approval_package = load_json(APPROVAL_PACKAGE_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("AUTH_TEMPLATE_JSON" in runner, "runner must read authorization template")
    require("NEGATIVE_FIXTURES_JSON" in runner, "runner must read negative fixtures")

    require(schema.get("schema_id") == "HEADROOM-LCX-AUTHORIZATION-SCHEMA-20260622", "invalid schema id")
    require(schema.get("scope", {}).get("project_count") == 15, "schema project count mismatch")
    require(schema.get("scope", {}).get("projects") == PROJECTS, "schema projects mismatch")
    require(schema.get("required_fields") == REQUIRED_FIELDS, "schema required fields mismatch")
    field_rules = schema.get("field_rules", {})
    require(set(field_rules) == set(REQUIRED_FIELDS), "schema field rules mismatch")
    for field in REQUIRED_FIELDS:
        rule = field_rules[field]
        require(rule.get("required") is True, f"field must be required: {field}")
        require(rule.get("must_not_equal") == "REQUIRED_USER_INPUT", f"field must reject placeholder: {field}")
    require(field_rules["sanitized_production_token_ledger"].get("reference_only") is True, "ledger must be reference-only")
    require(field_rules["sanitized_production_token_ledger"].get("forbid_inline_raw_text") is True, "ledger must forbid inline raw text")
    require(field_rules["authorized_by"].get("human_approver_required") is True, "human approver must be required")
    require("admitted_for_sanitized_measurement_precheck" in field_rules["waes_harness_admission_decision"].get("allowed_values", []), "WAES/Harness admitted value missing")

    hard_false = schema.get("hard_false_until_waes_harness_admits", [])
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
        require(key in hard_false, f"schema hard-false list missing: {key}")

    require(approval_package.get("schema_id") == schema.get("schema_id"), "approval package schema mismatch")
    require(approval_package.get("project_count") == 15, "approval package project count mismatch")
    require(approval_package.get("projects") == PROJECTS, "approval package projects mismatch")
    auth_fields = approval_package.get("authorization_fields", {})
    require(set(auth_fields) == set(REQUIRED_FIELDS), "approval package auth fields mismatch")
    for field in REQUIRED_FIELDS:
        require(auth_fields.get(field) == "REQUIRED_USER_INPUT", f"approval package must retain placeholder: {field}")
    attestations = approval_package.get("human_attestations", {})
    require(set(attestations) == set(REQUIRED_ATTESTATIONS), "approval package attestations mismatch")
    for key in REQUIRED_ATTESTATIONS:
        require(attestations.get(key) == "REQUIRED_USER_INPUT", f"attestation must retain placeholder: {key}")

    false_until_completed = approval_package.get("required_false_until_completed", {})
    for key in [
        "authorization_complete",
        "production_token_measurement_allowed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(false_until_completed.get(key) is False, f"approval package must keep false: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-20260622", "invalid evidence id")
    require(evidence.get("required_field_count") == len(REQUIRED_FIELDS), "evidence required field count mismatch")
    require(evidence.get("human_attestation_count") == len(REQUIRED_ATTESTATIONS), "evidence attestation count mismatch")
    gates = evidence.get("gates", {})
    require(gates.get("authorization_schema_gate") is True, "schema gate must be true")
    require(gates.get("approval_package_template_gate") is True, "approval package gate must be true")
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
        "HEADROOM-LCX-AUTHORIZATION-SCHEMA-APPROVAL-PACKAGE-20260622",
        "authorization_schema_gate | true",
        "approval_package_template_gate | true",
        "authorization_complete | false",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_authorization_schema_approval_package.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_authorization_schema_approval_package.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_authorization_schema_approval_package=pass "
        f"project_count=15 required_field_count={len(REQUIRED_FIELDS)} "
        f"human_attestation_count={len(REQUIRED_ATTESTATIONS)} "
        "authorization_complete=false production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
