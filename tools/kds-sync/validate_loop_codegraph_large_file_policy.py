#!/usr/bin/env python3
"""Validate CodeGraph large file policy evidence."""

from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GFIS = Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")
POLICY = ROOT / "02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-large-file-policy-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-large-file-policy-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-GFIS-LARGE-FILE-POLICY-001.md"
CANDIDATE_REL = "scripts/validate_gfis_runtime_sop_e2e.py"
CANDIDATE = GFIS / CANDIDATE_REL


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stderr}",
    )
    return completed.stdout


def indexed_path_exists(path: str) -> bool:
    db_path = GFIS / ".codegraph/codegraph.db"
    require(db_path.exists(), "GFIS CodeGraph DB missing")
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("select 1 from files where path = ?", (path,)).fetchone()
    return row is not None


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(run(["codegraph", "--version"]).strip() == "1.0.1", "codegraph version must be 1.0.1")

    policy = read(POLICY)
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence.get("evidence_id") == "LOOP-CODEGRAPH-LARGE-FILE-POLICY-20260621", "invalid evidence id")
    require(evidence.get("status") == "large_file_policy_defined", "invalid evidence status")
    require(evidence.get("policy", {}).get("large_file_threshold_bytes") == 1000000, "byte threshold mismatch")
    require(evidence.get("policy", {}).get("large_file_threshold_lines") == 15000, "line threshold mismatch")
    require(evidence.get("policy", {}).get("project_repo_changes_authorized") is False, "project repo changes must not be authorized")

    for phrase in [
        "large_or_generated_file_review",
        "residual_pending_notice_explained",
        "keep_residual_pending_notice_explained",
        "requires_authorization",
        "large_generated_validator_exception_candidate",
    ]:
        require(phrase in policy, f"policy missing phrase: {phrase}")

    gfis_case = evidence["gfis_case"]
    require(gfis_case["candidate_path"] == CANDIDATE_REL, "unexpected GFIS candidate")
    require(gfis_case["classification"] == "large_generated_validator_exception_candidate", "classification mismatch")
    require(gfis_case["decision"] == "keep_residual_pending_notice_explained", "decision mismatch")
    require(CANDIDATE.exists(), "GFIS candidate missing")
    require(CANDIDATE.stat().st_size == int(gfis_case["size_bytes"]), "candidate size drift")
    require(sum(1 for _ in CANDIDATE.open("r", encoding="utf-8")) == int(gfis_case["line_count"]), "candidate line count drift")
    require(not indexed_path_exists(CANDIDATE_REL), "candidate unexpectedly indexed in CodeGraph files table")
    require(run(["git", "status", "--short", "--", ".codegraph"], cwd=GFIS).strip() == "", "GFIS .codegraph appears in git status")
    require(run(["git", "status", "--short", "--", CANDIDATE_REL], cwd=GFIS).strip().startswith("M "), "candidate must remain tracked modified")

    rules = evidence["rules"]
    for key in [
        "business_code_edits_allowed",
        "validator_refactor_allowed",
        "delete_generated_validator_allowed",
        "project_codegraph_exclude_change_allowed",
        "accepted_or_integrated_upgrade_allowed",
    ]:
        require(rules.get(key) is False, f"rule must be false: {key}")
    require(rules.get("gpcf_policy_evidence_update_allowed") is True, "GPCF policy update must be allowed")

    for phrase in [
        "large_generated_validator_exception_candidate",
        "keep_residual_pending_notice_explained",
        "未修改 GFIS 业务代码",
        "未修改 GFIS 项目级 CodeGraph 排除规则",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-PROJECT-GROUP-MONITOR-001"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    for key, value in evidence.get("status_boundaries", {}).items():
        require(value is False, f"status boundary must be false: {key}")

    print(
        "loop_codegraph_large_file_policy=pass "
        "evidence=LOOP-CODEGRAPH-LARGE-FILE-POLICY-20260621 "
        "candidate=scripts/validate_gfis_runtime_sop_e2e.py "
        "decision=keep_residual_pending_notice_explained "
        "project_internal_development=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
