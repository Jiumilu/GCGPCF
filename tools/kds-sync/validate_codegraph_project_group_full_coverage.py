#!/usr/bin/env python3
"""Validate full project-group CodeGraph coverage evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "governance/codegraph/repo-codegraph-registry.yaml"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-project-group-full-coverage-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-project-group-full-coverage-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-FULL-FABRIC-001.md"

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
    registry = read(REGISTRY)
    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require("repo_count: 14" in registry, "registry must declare repo_count 14")
    require("codegraph_role: code_intelligence_fabric" in registry, "registry must declare Code Intelligence Fabric role")
    require("GlobalCloud Studio" in registry, "registry must include Studio")
    require("WAS世界资产体系" in registry, "registry must include WAS")

    require(evidence.get("evidence_id") == "CODEGRAPH-PROJECT-GROUP-FULL-COVERAGE-20260621", "invalid evidence id")
    require(evidence.get("status") in {"evidence_ready", "review_required"}, "status must be evidence_ready or review_required")
    project_group = evidence["project_group"]
    require(project_group["repo_count"] == 14, "repo_count must be 14")
    require(project_group["indexed_repo_count"] == 14, "indexed_repo_count must be 14")
    require(project_group["git_protected_repo_count"] == 14, "git_protected_repo_count must be 14")
    require(project_group["codegraph_git_status_entries_total"] == 0, ".codegraph git entries must be zero")
    require(project_group["studio_included"] is True, "Studio must be included")
    require(project_group["was_included"] is True, "WAS must be included")
    require(project_group["policy_exception_repo_count"] >= 1, "GFIS policy exception must be recorded")

    repos = {repo["id"]: repo for repo in evidence["repositories"]}
    require(list(repos) == [repo_id for repo_id, _, _ in REPOS], "repository order mismatch")

    for repo_id, name, path in REPOS:
        require(path.exists(), f"{name} path missing")
        require((path / ".git").exists(), f"{name} git repo missing")
        require((path / ".codegraph").exists(), f"{name} .codegraph missing")
        require(f"id: {repo_id}" in registry, f"registry missing repo id: {repo_id}")
        require(str(path) in registry, f"registry missing path for {name}")

        status = run(["codegraph", "status", "--json", "."], cwd=path)
        require(status.returncode == 0, f"{name} codegraph status failed: {status.stderr}")
        live = json.loads(status.stdout)
        require(live.get("initialized") is True, f"{name} codegraph not initialized")
        require(live.get("version") == "1.0.1", f"{name} unexpected CodeGraph version")
        require(live.get("fileCount", 0) >= repos[repo_id]["file_count"], f"{name} live file count below evidence")
        require(live.get("nodeCount", 0) >= repos[repo_id]["node_count"], f"{name} live node count below evidence")
        require(live.get("edgeCount", 0) >= repos[repo_id]["edge_count"], f"{name} live edge count below evidence")

        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path)
        require(git_status.returncode == 0, f"{name} git status failed")
        require(git_status.stdout.strip() == "", f"{name} .codegraph appears in git status")
        require(repos[repo_id]["codegraph_git_status_entries"] == 0, f"{name} evidence git entries must be 0")

        pending = live.get("pendingChanges") or {}
        live_pending = sum(int(pending.get(key, 0)) for key in ("added", "modified", "removed"))
        if repos[repo_id]["index_status"] == "up_to_date":
            require(live_pending == 0, f"{name} expected up_to_date but live pending is {live_pending}")
        elif repos[repo_id]["index_status"] == "policy_exception":
            require(repo_id == "gfis", "only GFIS may be policy_exception in this round")
            require(live_pending >= 0, "GFIS policy exception must be live-readable")
        else:
            require(repos[repo_id]["index_status"] == "pending_sync", f"{name} invalid index_status")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"status boundary must be false: {key}")

    for phrase in ["14", "GlobalCloud Studio", "WAS", "Code Intelligence Fabric", "candidate", "GPCF-CODEGRAPH-PROJECT-GROUP-FULL-FABRIC-001"]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "codegraph_project_group_full_coverage=pass "
        "repo_count=14 indexed_repo_count=14 git_protected_repo_count=14 "
        "studio_included=true was_included=true status="
        f"{evidence.get('status')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
