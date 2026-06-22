#!/usr/bin/env python3
"""Validate GFIS residual CodeGraph drift evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-residual-drift-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007.md"


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

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007", "invalid scope")
    require(evidence["status"] == "residual_drift_confirmed_no_cleanup_performed", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006", "invalid source round")

    snapshot = evidence["gfis_status_snapshot"]
    require(snapshot["pending_changes"] == {"added": 1, "modified": 0, "removed": 0}, "pending changes mismatch")
    require(snapshot["dot_codegraph_git_isolated"] is True, "GFIS .codegraph isolation must be recorded")
    require(snapshot["untracked_files_total"] == 226, "untracked file count mismatch")
    require(snapshot["untracked_codegraph_scannable_files"] == 73, "scannable untracked file count mismatch")

    scope = evidence["authorized_candidate_scope_status"]
    require(scope["project"] == "GFIS", "project must be GFIS")
    require(scope["candidate_validator"] == "pass", "candidate validator must pass")
    require(scope["runtime_sop_e2e"] == "failed_existing_kds_coverage_missing_controlled_sources", "runtime SOP failure must be recorded")
    require(len(scope["scoped_files"]) == 4, "scoped files must remain four")

    drift = evidence["drift_assessment"]
    require(drift["closure_possible_this_round"] is False, "closure must not be possible this round")
    require(drift["cleanup_performed"] is False, "cleanup must not be performed")

    forbidden = set(evidence["forbidden_next_actions_without_new_authorization"])
    for item in ["delete GFIS untracked files", "stage GFIS files", "commit GFIS changes", "push GFIS changes", "deploy GFIS"]:
        require(item in forbidden, f"missing forbidden action: {item}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "pendingChanges.added=1",
        "codegraph_sync_only_closure=false",
        "untracked_files_total=226",
        "untracked_codegraph_scannable_files=73",
        "FAIL: KDS coverage must not have missing controlled sources",
        "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008",
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
        "codegraph_dev_execution_gfis_residual_drift=pass "
        "gfis_pending_added=1 "
        "untracked_files_total=226 "
        "untracked_codegraph_scannable_files=73 "
        "cleanup_performed=false "
        "codegraph_sync_only_closure=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
