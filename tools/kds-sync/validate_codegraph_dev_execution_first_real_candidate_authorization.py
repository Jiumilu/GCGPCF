#!/usr/bin/env python3
"""Validate authorization package for the first real CodeGraph development candidate."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates/CODEGRAPH_DEV_EXECUTION_AUTHORIZATION_TEMPLATE.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-authorization-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-first-real-candidate-authorization-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005.md"


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
    template = load_json(TEMPLATE)
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-20260622", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZATION-005", "invalid scope")
    require(evidence["status"] == "authorization_package_ready_not_authorized", "invalid status")
    require(evidence["source_round"] == "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-004", "invalid source round")

    for field in [
        "authorization_id",
        "scope",
        "candidate_task_id",
        "authorized",
        "authorization_phrase",
        "allowed_files",
        "forbidden_paths",
        "allowed_commands",
        "forbidden_commands",
        "codegraph_sync_allowed",
        "business_implementation_allowed",
        "rollback_plan",
    ]:
        require(field in template, f"template missing field: {field}")

    candidate = evidence["candidate_task"]
    require(candidate["project"] == "GFIS", "candidate project must be GFIS")
    require(candidate["business_implementation_authorized"] is False, "candidate must not be authorized")
    require(candidate["runtime_sop_e2e"] == "repair_required", "runtime SOP must remain repair_required")

    auth = evidence["authorization_state"]
    require(auth["authorization_complete"] is False, "authorization must be incomplete")
    require(auth["authorized"] is False, "authorized must be false")
    require(auth["required_authorization_phrase"] == "授权执行 GFIS CodeGraph first real candidate business implementation", "authorization phrase mismatch")
    require(auth["received_authorization_phrase"] == "", "received authorization phrase must be empty")
    require(set(auth["missing_authorization_fields"]) == {"authorized_by", "authorized_at", "authorization_phrase", "allowed_files", "rollback_plan"}, "missing authorization fields mismatch")

    allowed = evidence["allowed_if_authorized"]
    require(allowed["repositories"] == ["/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"], "allowed repo mismatch")
    require(len(allowed["files"]) == 4, "allowed files must list four scoped files")
    require("requires explicit authorization" in allowed["codegraph_sync"], "GFIS codegraph sync must require explicit authorization")

    forbidden = evidence["forbidden_without_further_authorization"]
    for command in ["bench migrate", "schema sync", "production write", "real KDS write", "real WAES write", "external API write", "deployment", "git commit", "git push"]:
        require(command in forbidden["commands"], f"forbidden command missing: {command}")
    require("docs/harness/sop-e2e/intake-submissions/contract-chain/**" in forbidden["paths"], "real receipt intake path must be forbidden")

    gate = evidence["codegraph_gate_requirements"]
    for key in [
        "query_required",
        "node_required",
        "affected_required",
        "target_nodes_required",
        "affected_scope_required",
        "fallback_reason_required_when_affected_tests_empty",
        "post_change_status_required",
    ]:
        require(gate[key] is True, f"gate requirement must be true: {key}")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundaries must stay false")

    for phrase in [
        "authorization_complete=false",
        "authorized=false",
        "business_implementation_allowed=false",
        "授权执行 GFIS CodeGraph first real candidate business implementation",
        "GFIS CodeGraph sync 需要单独明确授权",
        "不进入 GFIS 业务实现",
        "GPCF-CODEGRAPH-DEV-EXECUTION-FIRST-REAL-CANDIDATE-AUTHORIZED-006",
        "GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-006",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_first_real_candidate_authorization=pass "
        "authorization_complete=false "
        "authorized=false "
        "business_implementation_allowed=false "
        "gfis_sync_requires_explicit_authorization=true "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-AUTHORIZATION-WAITING-006"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
