#!/usr/bin/env python3
"""Validate clean reindex authorization boundary for GFIS CodeGraph."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_ROOT = ROOT.parent / "GlobalCloud GFIS"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-tool-state-audit-blocked-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-gfis-tool-state-audit-blocked-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-BLOCKED-009.md"


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

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-BLOCKED-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-BLOCKED-009", "invalid scope")
    require(evidence["status"] == "clean_reindex_not_authorized_tool_state_audit_blocked", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008", "invalid source round")

    decision = evidence["authorization_decision"]
    require(decision["user_response"] == "暂不授权 clean reindex", "authorization response mismatch")
    for key in ["authorized", "clean_reindex_allowed", "codegraph_uninit_allowed", "codegraph_reinit_allowed", "gfis_file_cleanup_allowed"]:
        require(decision[key] is False, f"{key} must be false")

    snapshot = evidence["gfis_status_snapshot"]
    require(snapshot["pending_changes"] == {"added": 1, "modified": 0, "removed": 0}, "pending changes mismatch")
    require(snapshot["dot_codegraph_git_isolated"] is True, "GFIS .codegraph isolation must be recorded")

    blocked = set(evidence["blocked_actions"])
    for action in ["codegraph uninit", "rm -rf .codegraph", "codegraph init", "clean reindex", "delete GFIS untracked files", "stage GFIS files", "commit GFIS changes", "push GFIS changes", "deploy GFIS"]:
        require(action in blocked, f"missing blocked action: {action}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "暂不授权 clean reindex",
        "pendingChanges.added=1",
        "不执行 clean reindex",
        "不得声明 GFIS CodeGraph sync-only closure 完成",
        "GPCF-CODEGRAPH-DEV-EXECUTION-PROJECT-GROUP-CLOSURE-010",
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
        "codegraph_dev_execution_gfis_tool_state_audit_blocked=pass "
        "clean_reindex_allowed=false "
        "gfis_pending_added=1 "
        "codegraph_sync_only_closure=false "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-PROJECT-GROUP-CLOSURE-010"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
