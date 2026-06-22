#!/usr/bin/env python3
"""Validate Headroom LCX authorized measurement precheck evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-001.md"
RUNNER = ROOT / "tools/kds-sync/run_headroom_lcx_authorized_measurement_precheck.py"


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
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("AUTH_REVIEW_JSON" in runner, "runner must read authorization review")
    require("APPROVAL_INSTANCE_JSON" in runner, "runner must read approval instance")
    require(evidence.get("evidence_id") == "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621", "invalid evidence id")
    require(evidence.get("project_count") == 15, "project count mismatch")
    precheck = evidence.get("precheck", {})
    require(precheck.get("authorization_signal_present") is True, "authorization signal must be present")
    require(precheck.get("authorization_complete") is True, "authorization fields must be complete")
    require(precheck.get("missing_required_field_count") == 0, "missing field count must be 0")
    require(precheck.get("waes_harness_admitted") is True, "WAES/Harness admission must be true for sanitized precheck")
    require(precheck.get("authorized_measurement_precheck_gate") is True, "authorized measurement precheck must pass for sanitized dry-run preparation")
    require(precheck.get("production_token_measurement_allowed") is False, "production token measurement must be blocked")
    gates = evidence.get("gates", {})
    require(gates.get("authorization_signal_present") is True, "authorization signal gate must be true")
    require(gates.get("authorization_complete") is True, "authorization_complete gate must be true")
    require(gates.get("missing_required_field_count_zero") is True, "missing field zero gate must be true")
    require(gates.get("waes_harness_admitted") is True, "WAES/Harness admission gate must be true")
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
    require(gates.get("authorized_measurement_precheck_gate") is True, "authorized measurement precheck gate must be true")
    for phrase in [
        "HEADROOM-LCX-AUTHORIZED-MEASUREMENT-PRECHECK-20260621",
        "authorized_measurement_precheck_gate | true",
        "authorization_signal_present | true",
        "authorization_complete | true",
        "missing_required_field_count | 0",
        "waes_harness_admitted | true",
        "production_token_measurement_allowed | false",
        "production_admission_gate | false",
        "accepted | false",
        "integrated | false",
        "production_ready | false",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("run_headroom_lcx_authorized_measurement_precheck.py" in loop_round, "loop round missing runner")
    require("validate_headroom_lcx_authorized_measurement_precheck.py" in loop_round, "loop round missing validator")
    print(
        "headroom_lcx_authorized_measurement_precheck=pass_precheck_only "
        "project_count=15 authorization_signal_present=true authorization_complete=true "
        "missing_required_field_count=0 waes_harness_admission_decision=admitted_for_sanitized_measurement_precheck production_token_measurement_allowed=false "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
