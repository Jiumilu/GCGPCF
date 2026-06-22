#!/usr/bin/env python3
"""Validate WAS status matrix and Loop Control Board refresh."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-status-matrix-control-board-refresh-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-status-matrix-control-board-refresh-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-STATUS-MATRIX-AND-CONTROL-BOARD-REFRESH-001.md"
CONTROL_BOARD = ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"
STATUS_MATRIX = ROOT / "09-status/gpcf-project-status-matrix.md"
FIXTURE_DIR = ROOT / "fixtures/was"

PROJECT_GROUP = ["GFIS", "GPC", "PVAOS", "WAES", "KDS", "Brain", "PKC", "XiaoC", "XGD", "XiaoG", "MMC", "GPCF", "Studio", "WAS"]
REQUIRED_MARKERS = [
    "was_project_group_ontology_registry=pass",
    "was_loop_context_coverage_refresh=pass",
    "hold_required=1",
    "real_source_records=0",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
]
ZERO_BOUNDARY_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]
FALSE_BOUNDARY_KEYS = ["accepted", "integrated", "production_ready"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


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
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def validate_fixture(value: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if value.get("control_board_round") != "GPCF-ONTOLOGY-WAS-STATUS-MATRIX-AND-CONTROL-BOARD-REFRESH-001":
        failures.append("control_board_round_mismatch")
    if value.get("status_matrix_version") != "v5.51":
        failures.append("status_matrix_version_mismatch")
    if value.get("project_group_scope_count") != 14:
        failures.append("project_group_scope_count_mismatch")
    if value.get("required_markers") != REQUIRED_MARKERS:
        failures.append("required_markers_mismatch")
    boundary = value.get("boundary", {})
    if not isinstance(boundary, dict):
        failures.append("boundary_not_object")
        boundary = {}
    for key in ZERO_BOUNDARY_KEYS:
        if boundary.get(key) != 0:
            failures.append(f"boundary_{key}_must_be_zero")
    for key in FALSE_BOUNDARY_KEYS:
        if boundary.get(key) is not False:
            failures.append(f"boundary_{key}_must_be_false")
    return failures


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_text = read(LOOP_ROUND)
    control_board = read(CONTROL_BOARD)
    status_matrix = read(STATUS_MATRIX)
    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_text)
    require_frontmatter(CONTROL_BOARD, control_board)
    require_frontmatter(STATUS_MATRIX, status_matrix)

    require(evidence.get("evidence_id") == "WAS-STATUS-MATRIX-CONTROL-BOARD-REFRESH-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_status_matrix_control_board_refresh_pass_with_hold", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-STATUS-MATRIX-AND-CONTROL-BOARD-REFRESH-001", "invalid round id")
    require(evidence.get("project_group_scope") == PROJECT_GROUP, "project group scope mismatch")
    require(evidence.get("required_markers") == REQUIRED_MARKERS, "required markers mismatch")

    for marker in REQUIRED_MARKERS:
        require(marker in control_board, f"control board missing marker: {marker}")
        require(marker in status_matrix, f"status matrix missing marker: {marker}")
    require("当前轮次 | `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-083`" in control_board, "control board current round not refreshed to monitor 080")
    require("状态：v5.51" in status_matrix, "status matrix version not refreshed")
    require("WAS-Ontology monitor 083 已完成" in status_matrix, "status matrix summary not refreshed")
    require("Monitor 083 已建立绿色供应链限制物质声明、RoHS 合规证书、REACH SVHC 声明、材料安全数据表、化学品清单记录、物质检测报告和供应商化学合规承诺证据边界" in control_board, "control board summary not refreshed")
    require("下一轮应进入 `GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-084`" in control_board, "control board next round missing")
    require("GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-084" in status_matrix, "status matrix next round missing")

    positive = load_json(FIXTURE_DIR / "status-matrix-control-board-refresh-positive.json")
    require(not validate_fixture(positive), "positive fixture should pass")
    negative_paths = sorted(FIXTURE_DIR.glob("status-matrix-control-board-refresh-negative-*.json"))
    require(len(negative_paths) == 3, "negative fixture count must be 3")
    for path in negative_paths:
        require(validate_fixture(load_json(path)), f"{path.name} should be rejected")

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == 1, "positive fixture count mismatch")
    require(fixture_gate.get("negative_fixtures") == 3, "negative fixture count mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 3, "negative rejection mismatch")

    boundary = evidence.get("boundary", {})
    for key in ZERO_BOUNDARY_KEYS:
        require(boundary.get(key) == 0, f"boundary.{key} must remain 0")
    for key in FALSE_BOUNDARY_KEYS:
        require(boundary.get(key) is False, f"boundary.{key} must remain false")

    for phrase in [
        "project_group_scope | `14/14`",
        "refreshed_documents | `2`",
        "real_source_records | `0`",
        "production_ready | `false`",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GPCF 状态矩阵和 Loop 控制板已刷新" in loop_text, "loop feedback missing")
    require("object_family: StatusMatrixControlBoardRefresh" in loop_text, "loop_was_context missing object family")

    print(
        "was_status_matrix_control_board_refresh=pass "
        "project_group_scope=14/14 refreshed_documents=2 positive_fixtures=1 negative_fixtures=3 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 waes_review=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-084"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
