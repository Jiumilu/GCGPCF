#!/usr/bin/env python3
"""Validate Headroom LCX fixture extension negative gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEGATIVE_FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_fixture_extension_negative_gate.py"

EXPECTED_REASONS = {
    "raw_prompt_forbidden",
    "raw_completion_forbidden",
    "sensitive_material_forbidden",
    "production_measurement_forbidden",
    "kds_api_write_forbidden",
    "production_proxy_forbidden",
    "accepted_status_forbidden",
    "integrated_status_forbidden",
    "production_ready_forbidden",
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
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    fixture = load_json(NEGATIVE_FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("--check-only is required" in runner, "runner must require --check-only")
    require("reject_reason" in runner, "runner must define reject_reason")

    require(fixture.get("fixture_id") == "HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-FIXTURES-20260622", "invalid fixture id")
    require(fixture.get("case_count") == 9, "case count mismatch")
    cases = fixture.get("cases", [])
    require(isinstance(cases, list) and len(cases) == 9, "cases mismatch")
    require({case.get("expected_rejection_reason") for case in cases} == EXPECTED_REASONS, "expected reasons mismatch")
    expected_result = fixture.get("expected_result", {})
    require(expected_result.get("rejected") == 9, "expected rejected mismatch")
    require(expected_result.get("accepted") == 0, "expected accepted mismatch")
    for key in ["production_token_measurement_allowed", "production_admission_gate", "accepted_status", "integrated", "production_ready"]:
        require(expected_result.get(key) is False, f"expected result must be false: {key}")

    require(evidence.get("evidence_id") == "HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622", "invalid evidence id")
    require(evidence.get("status") == "negative_gate_pass_no_measurement", "invalid status")
    require(evidence.get("scope") == "fixture_extension_negative_boundary_cases", "invalid scope")
    require(evidence.get("case_count") == 9, "evidence case count mismatch")
    require(evidence.get("rejected") == 9, "rejected count mismatch")
    require(evidence.get("accepted_count") == 0, "accepted count mismatch")
    results = evidence.get("results", [])
    require(isinstance(results, list) and len(results) == 9, "results mismatch")
    require({result.get("actual_rejection_reason") for result in results} == EXPECTED_REASONS, "actual reasons mismatch")
    require(all(result.get("rejected") is True for result in results), "all cases must be rejected")
    require(all(result.get("accepted") is False for result in results), "accepted must be false for all cases")

    gates = evidence.get("gates", {})
    for key in [
        "negative_fixture_gate",
        "raw_prompt_rejected",
        "raw_completion_rejected",
        "sensitive_material_rejected",
        "production_measurement_rejected",
        "kds_api_write_rejected",
        "production_proxy_rejected",
        "status_upgrade_rejected",
    ]:
        require(gates.get(key) is True, f"gate must be true: {key}")
    for key in [
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
        "HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622",
        "negative_fixture_gate | true",
        "raw_prompt_rejected | true",
        "production_measurement_rejected | true",
        "kds_api_write_rejected | true",
        "production_proxy_rejected | true",
        "status_upgrade_rejected | true",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("build_headroom_lcx_fixture_extension_negative_gate.py --check-only" in loop_round, "loop round missing runner command")
    require("validate_headroom_lcx_fixture_extension_negative_gate.py" in loop_round, "loop round missing validator")

    print(
        "headroom_lcx_fixture_extension_negative_gate=pass_check_only "
        "case_count=9 rejected=9 accepted=0 production_admission_gate=false "
        "measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
