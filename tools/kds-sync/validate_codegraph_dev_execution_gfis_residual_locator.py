#!/usr/bin/env python3
"""Validate GFIS residual added locator evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
LOCATOR = ROOT / "tools/kds-sync/locate_gfis_codegraph_residual_added.py"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    locator_text = read(LOCATOR)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008", "invalid scope")
    require(evidence["status"] == "locator_completed_pending_added_not_mapped_to_untracked_scannable_file", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007", "invalid source round")

    result = evidence["locator_result"]
    require(result["pre_sync_pending_changes"] == {"added": 1, "modified": 0, "removed": 0}, "pre-sync pending mismatch")
    require(result["post_sync_pending_changes"] == {"added": 1, "modified": 0, "removed": 0}, "post-sync pending mismatch")
    require(result["indexed_file_count"] == 1022, "indexed file count mismatch")
    require(result["untracked_files_total"] == 226, "untracked file count mismatch")
    require(result["untracked_codegraph_scannable_files"] == 73, "scannable untracked count mismatch")
    require(result["untracked_codegraph_scannable_not_indexed_count"] == 0, "not-indexed count must be zero")
    require(result["untracked_codegraph_scannable_not_indexed"] == [], "not-indexed list must be empty")
    require(result["sync_probe_contains_added_one_zero_nodes"] is True, "sync probe must record Added: 1 / 0 nodes")
    require(result["exact_pending_file_identified"] is False, "exact pending file must not be identified")
    require(result["locator_conclusion"] == "pending_added_not_mapped_to_untracked_scannable_file", "locator conclusion mismatch")
    require(result["cleanup_performed"] is False, "cleanup must not be performed")
    require(result["git_write_performed"] is False, "git write must not be performed")

    interpretation = evidence["interpretation"]
    require(interpretation["closure_possible_this_round"] is False, "closure must not be possible this round")
    require(interpretation["likely_category"] == "codegraph_tool_state_or_non_git_scan_delta", "likely category mismatch")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    require(evidence["next_round_requires_authorization"] is True, "next round must require authorization")
    require("codegraph files" in locator_text and "git" in locator_text, "locator must compare CodeGraph files and Git files")

    for phrase in [
        "untracked_codegraph_scannable_not_indexed_count=0",
        "exact_pending_file_identified=false",
        "locator_conclusion=pending_added_not_mapped_to_untracked_scannable_file",
        "授权是否执行 GFIS CodeGraph clean reindex audit",
        "暂不授权 clean reindex",
        "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-009",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    gfis_dot_codegraph = run(["git", "status", "--short", "--", ".codegraph"], GFIS_ROOT)
    require(gfis_dot_codegraph.returncode == 0, f"GFIS .codegraph status failed: {gfis_dot_codegraph.stderr}")
    require(gfis_dot_codegraph.stdout.strip() == "", "GFIS .codegraph must remain git-isolated")

    gpcf_dot_codegraph = run(["git", "status", "--short", "--", ".codegraph"], ROOT)
    require(gpcf_dot_codegraph.returncode == 0, f"GPCF .codegraph status failed: {gpcf_dot_codegraph.stderr}")
    require(gpcf_dot_codegraph.stdout.strip() == "", "GPCF .codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_gfis_residual_locator=pass "
        "untracked_codegraph_scannable_not_indexed_count=0 "
        "exact_pending_file_identified=false "
        "locator_conclusion=pending_added_not_mapped_to_untracked_scannable_file "
        "cleanup_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-009"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
