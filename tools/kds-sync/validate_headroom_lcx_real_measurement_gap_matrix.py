#!/usr/bin/env python3
"""Validate the Headroom LCX real-measurement gap matrix evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_gap_matrix.py"
ROLLBACK_MD = ROOT / "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md"
WINDOW_GRANT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
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
    matrix = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)
    rollback = read(ROLLBACK_MD)
    window_grant = load_json(WINDOW_GRANT_JSON)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("real_measurement_gap_matrix" in runner, "runner must build gap matrix")
    require("Headroom LCX Rollback Plan 20260622-001" in rollback, "rollback plan must be detailed")

    require(matrix.get("gap_id") == "HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623", "invalid gap id")
    require(matrix.get("status") == "real_measurement_gap_matrix_defined_no_measurement", "invalid status")
    require(matrix.get("scope", {}).get("project_count") == 15, "project count mismatch")
    require("production_branch_open" in matrix.get("blocking_state", {}), "blocking state must expose production_branch_open")
    require(matrix.get("blocking_state", {}).get("production_branch_open") is False, "production branch must remain closed")
    require(matrix.get("blocking_state", {}).get("production_token_measurement_allowed") is False, "production token measurement must remain false")
    require(matrix.get("blocking_state", {}).get("measured_production_tokens") is False, "measured production tokens must remain false")
    require(matrix.get("blocking_state", {}).get("production_admission_gate") is False, "production admission gate must remain false")
    require(matrix.get("blocking_state", {}).get("real_measurement_window_granted") is True, "real measurement window must be granted")
    require(window_grant.get("real_measurement_window_granted") is True, "window grant evidence must be granted")
    require(window_grant.get("real_measurement_open") is False, "window grant evidence must remain precheck-only")
    require(matrix.get("rollback_plan_integrity", {}).get("rollback_plan_present") is True, "rollback plan must be present")
    require(matrix.get("rollback_plan_integrity", {}).get("rollback_runbook_written") is True, "rollback runbook must be written")
    require(len(matrix.get("missing_requirements", [])) >= 5, "missing requirements list too short")
    require(any(row.get("requirement_id") == "real_measurement_authorization_window" for row in matrix["missing_requirements"]), "missing authorization window gap")
    require(any(row.get("requirement_id") == "real_measurement_authorization_window" and row.get("current_status") == "granted_precheck_only" for row in matrix["missing_requirements"]), "authorization window must be granted_precheck_only")
    require(any(row.get("requirement_id") == "real_measurement_waes_harness_decision" for row in matrix["missing_requirements"]), "missing waes decision gap")
    require(any(row.get("requirement_id") == "real_measurement_token_ledger" for row in matrix["missing_requirements"]), "missing token ledger gap")
    require(any(row.get("requirement_id") == "production_proxy_or_sdk_enablement" for row in matrix["missing_requirements"]), "missing proxy/sdk gap")
    require(any(row.get("requirement_id") == "real_business_equivalence_measurement" for row in matrix["missing_requirements"]), "missing equivalence gap")

    for key, value in matrix.get("gates", {}).items():
        if key in {"gap_matrix_defined", "real_measurement_gap_present", "production_branch_blocked", "rollback_plan_present", "waes_precheck_only"}:
            require(value is True, f"gate must be true: {key}")
        if key in {"production_token_measurement_allowed", "measured_production_tokens", "production_admission_gate"}:
            require(value is False, f"gate must be false: {key}")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-GAP-MATRIX-20260623",
        "real_measurement_gap_matrix_defined_no_measurement",
        "headroom-lcx-real-measurement-authorization-window-request-20260623.json",
        "headroom-lcx-real-measurement-authorization-window-grant-20260623.json",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")
    require("production_branch_open: `false`" in md or "production_branch_open: false" in md, "evidence md missing production_branch_open")
    require("real_measurement_gap_present: `true`" in md or "real_measurement_gap_present: true" in md, "evidence md missing real_measurement_gap_present")
    require("real_measurement_window_granted: `true`" in md or "real_measurement_window_granted: true" in md, "evidence md missing real_measurement_window_granted")
    require("production_branch_blocked: `true`" in md or "production_branch_blocked: true" in md, "evidence md missing production_branch_blocked")
    require("production_token_measurement_allowed: `false`" in md or "production_token_measurement_allowed: false" in md, "evidence md missing production_token_measurement_allowed")
    require("production_ready: `false`" in md or "production_ready: false" in md, "evidence md missing production_ready")

    for phrase in [
        "real measurement gap matrix",
        "build_headroom_lcx_real_measurement_gap_matrix.py",
        "validate_headroom_lcx_real_measurement_gap_matrix.py",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "headroom_lcx_real_measurement_gap_matrix=pass "
        "project_count=15 real_measurement_gap_present=true "
        "production_branch_blocked=true real_measurement_window_granted=true "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
