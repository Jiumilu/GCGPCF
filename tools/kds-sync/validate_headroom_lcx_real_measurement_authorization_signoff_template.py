#!/usr/bin/env python3
"""Validate the Headroom LCX real measurement authorization signoff template."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-authorization-signoff-template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-signoff-template-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-001.md"

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

REQUIRED_SIGNATURE_FIELDS = [
    "signer_name",
    "signer_role",
    "signed_at",
    "signature_method",
    "signature_statement",
    "signature_intent",
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
    template = load_json(TEMPLATE_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(template.get("template_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623", "invalid template id")
    require(template.get("purpose") == "collect_signable_human_authorization_for_open_real_measurement_window_under_precheck_only_constraints", "invalid purpose")
    scope = template.get("scope", {})
    require(scope.get("project_count") == 15, "project count mismatch")
    require(scope.get("projects") == PROJECTS, "project list mismatch")
    require(scope.get("allowed_next_action_after_signature") == "rerun_authorized_measurement_precheck_only", "allowed next action mismatch")

    auth_fields = template.get("authorization_fields", {})
    require(set(auth_fields) == set(REQUIRED_FIELDS), "authorization fields mismatch")
    for field in REQUIRED_FIELDS:
        field_spec = auth_fields[field]
        require(field_spec.get("value") == "REQUIRED_USER_INPUT", f"field placeholder mismatch: {field}")
        require(field_spec.get("required") is True, f"field required flag mismatch: {field}")
    require(auth_fields["sanitized_production_token_ledger"].get("must_not_include") == [
        "raw prompt",
        "raw completion",
        "secret",
        "credential",
        "customer contract text",
        "production token",
    ], "ledger exclusion list mismatch")
    require(auth_fields["waes_harness_admission_decision"].get("allowed_values") == [
        "admitted_for_sanitized_measurement_precheck",
        "blocked",
    ], "waes decision allowed values mismatch")

    signature_block = template.get("signature_block", {})
    require(set(signature_block) == set(REQUIRED_SIGNATURE_FIELDS), "signature block mismatch")
    for field in REQUIRED_SIGNATURE_FIELDS[:-1]:
        require(signature_block.get(field) == "REQUIRED_USER_INPUT", f"signature placeholder mismatch: {field}")
    require(signature_block.get("signature_intent") == "approve_open_real_measurement_window_or_reject_or_defer", "signature intent mismatch")

    required_false = template.get("required_false_until_completed", {})
    for key in [
        "authorization_complete",
        "real_measurement_window_open",
        "production_token_measurement_allowed",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(required_false.get(key) is False, f"required false mismatch: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623", "invalid evidence id")
    require(evidence.get("template_path") == TEMPLATE_JSON.relative_to(ROOT).as_posix(), "template path mismatch")
    require(evidence.get("required_field_count") == len(REQUIRED_FIELDS), "required field count mismatch")
    require(evidence.get("required_signature_field_count") == len(REQUIRED_SIGNATURE_FIELDS), "required signature field count mismatch")
    evidence_false = evidence.get("required_false_until_completed", {})
    for key in [
        "authorization_complete",
        "real_measurement_window_open",
        "production_token_measurement_allowed",
        "production_proxy_started",
        "production_sdk_enabled",
        "production_external_api_write",
        "kds_api_write",
        "measured_production_tokens",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(evidence_false.get(key) is False, f"evidence false mismatch: {key}")

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623",
        "需要签字的 6 个字段",
        "authorization_complete | `false`",
        "real_measurement_window_open | `false`",
        "production_token_measurement_allowed | `false`",
        "accepted | `false`",
        "integrated | `false`",
        "production_ready | `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_headroom_lcx_real_measurement_authorization_signoff_template.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_real_measurement_authorization_signoff_template=pass_check_only "
        "project_count=15 required_field_count=6 required_signature_field_count=6 "
        "authorization_complete=false real_measurement_window_open=false "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
