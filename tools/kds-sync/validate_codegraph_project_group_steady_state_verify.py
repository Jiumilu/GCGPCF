#!/usr/bin/env python3
"""Validate CodeGraph project-group steady-state evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-project-group-steady-state-verify-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-project-group-steady-state-verify-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004.md"

REPOS = [
    ("gfis", "GlobalCloud GFIS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS")),
    ("gpc", "GlobalCloud GPC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC")),
    ("pvaos", "GlobalCloud PVAOS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS")),
    ("waes", "GlobalCloud WAES", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES")),
    ("kds", "GlobalCloud KDS", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS")),
    ("brain", "GlobalCloud Brain", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain")),
    ("pkc", "GlobalCloud PKC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC")),
    ("xiaoc", "GlobalCloud XiaoC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC")),
    ("xgd", "GlobalCloud XGD", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD")),
    ("xiaog", "GlobalCloud XiaoG", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG")),
    ("mmc", "GlobalCloud MMC", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC")),
    ("gpcf", "GlobalCoud GPCF", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF")),
    ("studio", "GlobalCloud Studio", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio")),
    ("was", "WAS世界资产体系", Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系")),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-20260621", "invalid evidence id")
    require(evidence["status"] == "review_required", "steady-state evidence must remain review_required")
    require(evidence["scope"] == "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004", "invalid scope")

    project_group = evidence["project_group"]
    require(project_group["repo_count"] == 14, "repo_count must be 14")
    require(project_group["indexed_repo_count"] == 14, "indexed_repo_count must be 14")
    require(project_group["git_protected_repo_count"] == 14, "git_protected_repo_count must be 14")
    require(project_group["codegraph_git_status_entries_total"] == 0, ".codegraph git entries must be 0")
    require(project_group["studio_included"] is True, "Studio must be included")
    require(project_group["was_included"] is True, "WAS must be included")
    require(project_group["brain_watchlist_active"] is True, "Brain watchlist must be active")
    require(project_group["gfis_policy_exception_active"] is True, "GFIS policy exception must be active")

    repos = {repo["id"]: repo for repo in evidence["repositories"]}
    require(list(repos) == [repo_id for repo_id, _, _ in REPOS], "repository order mismatch")

    live_git_entries = 0
    for repo_id, name, path in REPOS:
        require(path.exists() and (path / ".git").exists(), f"{name} Git repo missing")
        require((path / ".codegraph").exists(), f"{name} .codegraph missing")

        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"{name} codegraph status failed: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{name} CodeGraph not initialized")
        require(live.get("version") == "1.0.1", f"{name} CodeGraph version mismatch")
        require(live.get("fileCount", 0) >= int(repos[repo_id]["file_count"]), f"{name} file count regressed")
        require(live.get("nodeCount", 0) >= int(repos[repo_id]["node_count"]), f"{name} node count regressed")
        require(live.get("edgeCount", 0) >= int(repos[repo_id]["edge_count"]), f"{name} edge count regressed")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"{name} git status failed")
        entries = [line for line in git_status.stdout.splitlines() if line.strip()]
        require(entries == [], f"{name} .codegraph appears in git status")
        live_git_entries += len(entries)

    require(live_git_entries == 0, "live .codegraph git entries must be 0")
    require(repos["gfis"]["index_status"] == "policy_exception", "GFIS must remain policy_exception")
    require(repos["brain"]["index_status"] == "pending_sync", "Brain must remain the active drift watchlist item")

    for value in evidence["status_boundaries"].values():
        require(value is False, "status boundary values must stay false")

    for key in [
        "registry",
        "authorization_model",
        "loop_schema",
        "harness_impact_template",
        "harness_evidence_template",
        "waes_gate_policy",
        "kds_okf_mapping",
    ]:
        require(key in evidence["integration_evidence"], f"missing integration evidence key: {key}")

    for key in ["coverage_value", "drift_value", "loop_value", "harness_value", "waes_value", "kds_okf_value", "cost_quality_value"]:
        require(key in evidence["operational_value_assessment"], f"missing operational value key: {key}")

    for phrase in ["稳态验证", "实际作用评估", "Brain 活动漂移", "GFIS policy exception", "GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_project_group_steady_state_verify=pass "
        "repo_count=14 git_protected_repo_count=14 status=review_required "
        "brain_watchlist=active gfis_policy_exception=active "
        "next=GPCF-CODEGRAPH-IMPACT-REPORT-DRY-RUN-005"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
