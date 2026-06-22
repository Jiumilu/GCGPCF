#!/usr/bin/env python3
"""Validate Headroom production-token authorization package evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-PACKAGE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_production_token_authorization_package.py"


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
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-21",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing controlled marker: {phrase}")


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("PROJECTS" in runner, "runner must define project group scope")
    require(evidence.get("evidence_id") == "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-PACKAGE-20260621", "invalid evidence id")
    require(evidence.get("status") == "authorization_package_defined_pending", "invalid status")
    require(evidence.get("measured_production_tokens") is False, "must not claim production tokens")
    requested_scope = evidence.get("requested_scope", {})
    require(len(requested_scope.get("projects", [])) == 15, "project count mismatch")
    require(requested_scope.get("telemetry") == "off", "telemetry must be off")
    require(requested_scope.get("raw_prompt_storage") == "forbidden", "raw prompt storage must be forbidden")
    require(requested_scope.get("external_api_write_allowed") is False, "external API write must remain false")
    require(requested_scope.get("kds_write_allowed") is False, "KDS write must remain false")
    authorization = evidence.get("authorization", {})
    require(authorization.get("status") == "pending", "authorization must remain pending")
    require(authorization.get("authorized_window_id") is None, "authorized window must not be claimed")
    require(authorization.get("authorized_by") is None, "approver must not be claimed")
    require(authorization.get("authorized_at") is None, "approval timestamp must not be claimed")
    gate = evidence.get("gate", {})
    for false_key in [
        "authorized_window_present",
        "approver_present",
        "approval_timestamp_present",
        "sanitized_ledger_present",
        "rollback_plan_present",
        "authorization_package_gate",
        "production_admission_gate",
    ]:
        require(gate.get(false_key) is False, f"{false_key} must remain false")
    require(gate.get("negative_fixture_gate_passed") is True, "negative fixture prerequisite must pass")
    for key, value in evidence.get("non_claims", {}).items():
        require(value is True, f"non-claim marker must be true: {key}")
    for phrase in [
        "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-PACKAGE-20260621",
        "authorization_package_gate | false",
        "authorization_status | pending",
        "production_admission_gate | false",
        "不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_production_token_authorization_package.py" in loop_round, "loop round missing runner")
    require("validate_headroom_production_token_authorization_package.py" in loop_round, "loop round missing validator")
    print(
        "headroom_production_token_authorization_package=pass "
        "authorization_status=pending authorization_package_gate=false "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
