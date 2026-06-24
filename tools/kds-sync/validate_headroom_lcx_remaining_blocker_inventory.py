#!/usr/bin/env python3
"""Validate the Headroom LCX remaining blocker inventory evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
E_JSON = ROOT / "docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.json"
E_MD = ROOT / "docs/harness/evidence/headroom-lcx-remaining-blocker-inventory-20260623.md"
LOOP = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-001.md"
BUILDER = ROOT / "tools/kds-sync/build_headroom_lcx_remaining_blocker_inventory.py"
GAP = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-gap-matrix-20260623.json"
TRANSITION = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-transition-graph-20260623.json"
WINDOW_REQUEST = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json"
WINDOW_GRANT = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-grant-20260623.json"

EXPECTED_BLOCKERS = {
    "real_measurement_authorization_window",
    "real_measurement_waes_harness_decision",
    "real_measurement_token_ledger",
    "production_proxy_or_sdk_enablement",
    "real_business_equivalence_measurement",
}


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
    inventory = load_json(E_JSON)
    gap = load_json(GAP)
    transition = load_json(TRANSITION)
    window_request = load_json(WINDOW_REQUEST)
    window_grant = load_json(WINDOW_GRANT)
    md = read(E_MD)
    loop = read(LOOP)
    builder = read(BUILDER)

    require_frontmatter(E_MD, md)
    require_frontmatter(LOOP, loop)
    require("remaining_blocker_inventory" in builder, "builder must mention remaining blocker inventory")

    require(inventory.get("evidence_id") == "HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623", "invalid evidence id")
    require(inventory.get("status") == "remaining_blocker_inventory_defined_precheck_only", "invalid status")
    require(inventory.get("scope", {}).get("project_count") == 15, "project count mismatch")

    blockers = inventory.get("blockers", [])
    require(isinstance(blockers, list) and len(blockers) == 5, "blocker count mismatch")
    require({row.get("requirement_id") for row in blockers} == EXPECTED_BLOCKERS, "blocker coverage mismatch")

    summary = inventory.get("blocker_summary", {})
    require(summary.get("blocker_count") == 5, "blocker summary mismatch")
    require(summary.get("global_loop_document_gate_pass") is True, "global loop gate pass must be true")
    require(summary.get("window_request_granted") is False, "window request granted must remain false")

    current_state = inventory.get("current_state", {})
    require(current_state.get("real_measurement_open") is False, "real measurement must remain closed")
    require(current_state.get("global_loop_document_gate") == "pass", "global loop gate must pass")
    require(current_state.get("production_branch_blocked") is True, "production branch must remain blocked")
    require(current_state.get("production_token_measurement_allowed") is False, "token measurement must remain false")
    require(current_state.get("measured_production_tokens") is False, "measured tokens must remain false")
    require(current_state.get("production_admission_gate") is False, "production gate must remain false")
    require(current_state.get("accepted") is False, "accepted must remain false")
    require(current_state.get("integrated") is False, "integrated must remain false")
    require(current_state.get("production_ready") is False, "production_ready must remain false")
    require(current_state.get("authorization_window_request_status") == "real_measurement_authorization_window_requested_not_granted", "window request status mismatch")
    require(current_state.get("authorization_window_grant_status") == "granted_precheck_only", "window grant status mismatch")

    require(gap.get("status") == "real_measurement_gap_matrix_defined_no_measurement", "gap matrix status mismatch")
    require(transition.get("status") == "transition_graph_defined_blocked_real_measurement", "transition graph status mismatch")
    require(window_request.get("status") == "real_measurement_authorization_window_requested_not_granted", "window request evidence mismatch")
    require(window_grant.get("real_measurement_window_granted") is True, "window grant evidence must be granted")
    require(window_grant.get("real_measurement_open") is False, "window grant evidence must remain precheck-only")
    require(window_grant.get("status") == "real_measurement_authorization_window_granted_precheck_only", "window grant status mismatch")

    for phrase in [
        "HEADROOM-LCX-REMAINING-BLOCKER-INVENTORY-20260623",
        "remaining_blocker_inventory_defined_precheck_only",
        "global_loop_document_gate: `pass`",
        "real_measurement_authorization_window_requested_not_granted",
        "granted_precheck_only",
        "production_branch_blocked: `true`",
        "accepted: `false`",
        "integrated: `false`",
        "production_ready: `false`",
    ]:
        require(phrase in md, f"md missing phrase: {phrase}")

    for phrase in [
        "remaining blocker inventory",
        "build_headroom_lcx_remaining_blocker_inventory.py",
        "validate_headroom_lcx_remaining_blocker_inventory.py",
    ]:
        require(phrase in loop, f"loop missing phrase: {phrase}")

    print(
        "headroom_lcx_remaining_blocker_inventory=pass "
        "project_count=15 blocker_count=5 "
        "real_measurement_open=false production_branch_blocked=true "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
