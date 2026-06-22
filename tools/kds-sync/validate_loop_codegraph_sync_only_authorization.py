#!/usr/bin/env python3
"""Validate CodeGraph sync-only authorization closure evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-sync-only-authorization-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-sync-only-authorization-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003.md"

REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
}


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
        f"command failed ({completed.returncode}): {' '.join(args)}\n{completed.stdout}\n{completed.stderr}",
    )
    return completed.stdout


def codegraph_status(path: Path) -> dict:
    return json.loads(run(["codegraph", "status", "--json", "."], cwd=path))


def main() -> int:
    require(shutil.which("codegraph") is not None, "codegraph CLI must be installed")
    require(run(["codegraph", "--version"]).strip() == "1.0.1", "codegraph version must be 1.0.1")

    evidence = json.loads(read(EVIDENCE_JSON))
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "LOOP-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-20260621", "invalid evidence id")
    require(evidence["status"] == "codegraph_sync_only_authorization_executed", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003", "invalid scope")
    require(evidence["authorization"]["authorized_by_user_message"] == "授权", "authorization message mismatch")
    require(evidence["next_loop_input"]["round"] == "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004", "invalid next loop input")

    sync_results = {item["project"]: item for item in evidence["sync_results"]}
    require(list(sync_results) == list(REPOS), "sync result project order mismatch")

    for name, path in REPOS.items():
        require(path.exists() and (path / ".git").exists(), f"{name} Git repo missing")
        require((path / ".codegraph").exists(), f"{name} .codegraph missing")
        exclude = path / ".git/info/exclude"
        require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), f"{name} missing .codegraph exclude")
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path).strip()
        require(git_status == "", f"{name} .codegraph appears in git status: {git_status}")
        status = codegraph_status(path)
        require(status["pendingChanges"] == {"added": 0, "modified": 0, "removed": 0}, f"{name} must be up to date")
        require(status["fileCount"] >= sync_results[name]["after"]["files"], f"{name} file count below evidence")
        require(status["nodeCount"] >= sync_results[name]["after"]["nodes"], f"{name} node count below evidence")
        require(status["edgeCount"] >= sync_results[name]["after"]["edges"], f"{name} edge count below evidence")
        require(sync_results[name]["codegraph_git_status_entries"] == 0, f"{name} evidence git entries must be 0")

    for key, value in evidence["boundaries"].items():
        require(value is False, f"boundary must remain false: {key}")

    for phrase in [
        "codegraph_sync_only_authorization_executed",
        "用户已授权",
        "modified=56",
        "added=2, modified=5",
        "pending=0",
        "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004",
        "不提交、不推送、不部署",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "loop_codegraph_sync_only_authorization=pass "
        "status=codegraph_sync_only_authorization_executed "
        "brain_pending=0 studio_pending=0 "
        "next=GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-VERIFY-004"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
