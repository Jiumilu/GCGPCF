#!/usr/bin/env python3
"""Validate the CodeGraph development execution authorization waiting state."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-authorization-waiting-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-authorization-waiting-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-006.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read(path))


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-006", "invalid scope")
    require(evidence["status"] == "authorization_waiting_blocked", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005", "invalid source round")

    candidate = evidence["candidate_task"]
    require(candidate["project"] == "GFIS", "candidate project must be GFIS")
    require(candidate["business_implementation_authorized"] is False, "business implementation must not be authorized")
    require(candidate["business_implementation_allowed"] is False, "business implementation must not be allowed")
    require(candidate["runtime_sop_e2e"] == "repair_required", "runtime SOP must remain repair_required")

    auth = evidence["authorization_state"]
    require(auth["authorization_complete"] is False, "authorization must be incomplete")
    require(auth["authorized"] is False, "authorized must be false")
    require(auth["required_authorization_phrase"] == "授权执行 GFIS CodeGraph first real candidate business implementation", "authorization phrase mismatch")
    require(auth["received_authorization_phrase"] == "", "received authorization phrase must be empty")
    require(set(auth["missing_authorization_fields"]) == {"authorized_by", "authorized_at", "authorization_phrase", "allowed_files", "rollback_plan"}, "missing authorization fields mismatch")

    drift = evidence["gfis_codegraph_drift_snapshot"]
    require(drift["initialized"] is True, "GFIS CodeGraph must be initialized in snapshot")
    require(drift["pending_changes"] == {"added": 1, "modified": 0, "removed": 0}, "GFIS drift snapshot mismatch")
    require(drift["dot_codegraph_git_isolated"] is True, "GFIS .codegraph isolation must be recorded")
    require(drift["sync_performed"] is False, "GFIS sync must not be performed")
    require(drift["sync_allowed_without_explicit_authorization"] is False, "GFIS sync must require authorization")

    for action in [
        "GFIS business implementation",
        "GFIS codegraph sync",
        "production write",
        "external API write",
        "real KDS write",
        "real WAES write",
        "deployment",
        "git commit",
        "git push",
    ]:
        require(action in evidence["current_forbidden_actions"], f"missing forbidden action: {action}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    require(evidence["next_round_if_authorized"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006", "authorized next round mismatch")
    require(evidence["next_round_if_still_waiting"] == "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-RECHECK-007", "waiting next round mismatch")

    for phrase in [
        "authorization_complete=false",
        "authorized=false",
        "business_implementation_allowed=false",
        "status=authorization_waiting_blocked",
        "pendingChanges.added=1",
        "sync_performed=false",
        "不进入 GFIS 业务实现",
        "不执行 GFIS CodeGraph sync",
        "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006",
        "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-RECHECK-007",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_authorization_waiting=pass "
        "status=authorization_waiting_blocked "
        "authorization_complete=false "
        "authorized=false "
        "business_implementation_allowed=false "
        "gfis_sync_performed=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-RECHECK-007"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
