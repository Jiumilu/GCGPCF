#!/usr/bin/env python3
"""Validate Headroom LCX authorized measurement authorization template."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-lcx-authorized-measurement-authorization-template.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-authorization-template-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_authorized_measurement_authorization_template.py"

REQUIRED_FIELDS = [
    "authorized_window_id",
    "authorized_by",
    "authorized_at",
    "sanitized_production_token_ledger",
    "rollback_plan_id",
    "waes_harness_admission_decision",
]
PLACEHOLDER = "REQUIRED_USER_INPUT"


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
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")
    require(
        "last_reviewed: 2026-06-21" in meta or "last_reviewed: 2026-06-22" in meta,
        f"{path.relative_to(ROOT)} missing current last_reviewed marker",
    )


def main() -> int:
    template = load_json(TEMPLATE_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("AUTH_REVIEW_JSON" in runner, "runner must read authorization review")
    require("PRECHECK_JSON" in runner, "runner must read authorized measurement precheck")
    require(template.get("template_id") == "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621", "invalid template id")
    require(template.get("scope", {}).get("project_count") == 15, "template project count mismatch")
    fields = template.get("authorization_fields", {})
    require(set(fields) == set(REQUIRED_FIELDS), "template field set mismatch")
    for field in REQUIRED_FIELDS:
        field_data = fields.get(field, {})
        require(field_data.get("required") is True, f"field must be required: {field}")
        require(field_data.get("value") == PLACEHOLDER, f"field must retain placeholder: {field}")

    false_until_completed = template.get("required_false_until_completed", {})
    for key in [
        "authorization_complete",
        "production_token_measurement_allowed",
        "production_admission_gate",
        "accepted",
        "integrated",
        "production_ready",
    ]:
        require(false_until_completed.get(key) is False, f"template must keep false until completed: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621", "invalid evidence id")
    require(evidence.get("project_count") == 15, "evidence project count mismatch")
    require(evidence.get("required_fields") == REQUIRED_FIELDS, "evidence required fields mismatch")
    gates = evidence.get("gates", {})
    require(gates.get("authorization_template_generated") is True, "template generation gate must be true")
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
        "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-AUTHORIZATION-TEMPLATE-20260621",
        "authorization_template_generated | true",
        "authorization_complete | false",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_headroom_lcx_authorized_measurement_authorization_template.py" in loop_round, "loop round missing validator")
    require("build_headroom_lcx_authorized_measurement_authorization_template.py" in loop_round, "loop round missing runner")

    print(
        "headroom_lcx_authorized_measurement_authorization_template=pass "
        "project_count=15 required_field_count=6 authorization_complete=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
