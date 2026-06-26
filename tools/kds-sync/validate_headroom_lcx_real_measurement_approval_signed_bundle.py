#!/usr/bin/env python3
"""Validate the Headroom LCX real measurement approval signed bundle."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BUNDLE_JSON = ROOT / "fixtures/headroom/headroom-lcx-real-measurement-approval-signed-bundle.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-001.md"

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

AUTH_FIELDS = {
    "authorized_window_id": "LCX-MEASURE-20260623-001",
    "authorized_by": "lujunxiang / 总架构师",
    "authorized_at": "2026-06-23T14:30:00+08:00",
    "sanitized_production_token_ledger": "docs/harness/evidence/headroom-lcx-sanitized-production-usage-ledger-20260623.json",
    "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
    "waes_harness_admission_decision": "admitted_for_sanitized_measurement_precheck",
}

SIGNATURE_BLOCK = {
    "signer_name": "lujunxiang",
    "signer_role": "总架构师",
    "signed_at": "2026-06-23T14:30:00+08:00",
    "signature_method": "typed_approval",
    "signature_statement": "I approve opening the real measurement window under the stated precheck-only constraints.",
    "signature_intent": "approve_open_real_measurement_window_or_reject_or_defer",
}


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
    bundle = load_json(BUNDLE_JSON)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(bundle.get("bundle_id") == "HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623", "invalid bundle id")
    require(bundle.get("project_count") == 15, "project count mismatch")
    require(bundle.get("projects") == PROJECTS, "project list mismatch")
    require(bundle.get("source_templates") == [
        "HEADROOM-LCX-HUMAN-APPROVAL-PACKAGE-TEMPLATE-20260622",
        "HEADROOM-LCX-REAL-MEASUREMENT-AUTHORIZATION-SIGNOFF-TEMPLATE-20260623",
    ], "source template mismatch")
    require(bundle.get("authorization_fields") == AUTH_FIELDS, "authorization fields mismatch")
    require(bundle.get("signature_block") == SIGNATURE_BLOCK, "signature block mismatch")
    completion = bundle.get("completion_flags", {})
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
        require(key in completion, f"missing completion flag: {key}")
    require(completion.get("authorization_complete") is True, "authorization_complete must be true")
    for key in [
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
        require(completion.get(key) is False, f"completion flag must be false: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623", "invalid evidence id")
    require(evidence.get("bundle_id") == bundle.get("bundle_id"), "evidence bundle mismatch")
    require(evidence.get("project_count") == 15, "evidence project count mismatch")
    require(evidence.get("authorization_fields") == AUTH_FIELDS, "evidence authorization mismatch")
    require(evidence.get("signature_block") == SIGNATURE_BLOCK, "evidence signature mismatch")
    require(evidence.get("required_field_count") == 6, "required field count mismatch")
    require(evidence.get("required_signature_field_count") == 6, "required signature field count mismatch")
    require(evidence.get("human_attestation_count") == 7, "human attestation count mismatch")
    evidence_completion = evidence.get("completion_flags", {})
    require(evidence_completion.get("authorization_complete") is True, "evidence authorization_complete must be true")
    for key in [
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
        require(evidence_completion.get(key) is False, f"evidence completion must be false: {key}")

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-APPROVAL-SIGNED-BUNDLE-20260623",
        "authorization_complete | true",
        "real_measurement_window_open | false",
        "production_token_measurement_allowed | false",
        "production_proxy_started | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("validate_headroom_lcx_real_measurement_approval_signed_bundle.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_real_measurement_approval_signed_bundle=pass "
        "project_count=15 authorization_complete=true real_measurement_window_open=false "
        "production_token_measurement_allowed=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
