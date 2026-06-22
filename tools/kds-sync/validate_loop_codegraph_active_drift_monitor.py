#!/usr/bin/env python3
"""Validate CodeGraph active drift monitor evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-active-drift-monitor-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001.md"
POLICY = ROOT / "02-governance/loop/LOOP_CODEGRAPH_LARGE_FILE_POLICY.md"

REPOS = {
    "GlobalCloud Brain": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain"),
    "GlobalCloud Studio": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio"),
    "GlobalCloud GFIS": Path("/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS"),
    "GlobalCoud GPCF": ROOT,
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
    policy = read(POLICY)

    require(evidence["evidence_id"] == "LOOP-CODEGRAPH-ACTIVE-DRIFT-MONITOR-20260621", "invalid evidence id")
    require(evidence["status"] == "codegraph_active_drift_monitor_evidenced", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001", "invalid scope")
    require(evidence["metrics_seed"]["mttd_seed_available"] is True, "MTTD seed must be available")
    require(evidence["metrics_seed"]["mttr_seed_available"] is False, "MTTR seed must remain unavailable")
    require(evidence["next_loop_input"]["round"] == "GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002", "invalid next loop input")

    observations = {item["project"]: item for item in evidence["observations"]}
    require(list(observations) == list(REPOS), "observation project order mismatch")

    for name, path in REPOS.items():
        require(path.exists() and (path / ".git").exists(), f"{name} Git repo missing")
        require((path / ".codegraph").exists(), f"{name} .codegraph missing")
        exclude = path / ".git/info/exclude"
        require(exclude.exists() and ".codegraph/" in exclude.read_text(encoding="utf-8"), f"{name} missing .codegraph exclude")
        git_status = run(["git", "status", "--short", "--", ".codegraph"], cwd=path).strip()
        require(git_status == "", f"{name} .codegraph appears in git status: {git_status}")

    brain = codegraph_status(REPOS["GlobalCloud Brain"])
    studio = codegraph_status(REPOS["GlobalCloud Studio"])
    gfis = codegraph_status(REPOS["GlobalCloud GFIS"])
    gpcf = codegraph_status(REPOS["GlobalCoud GPCF"])

    require(brain["pendingChanges"]["modified"] >= observations["GlobalCloud Brain"]["pending_changes"]["modified"], "Brain drift must not be below evidence")
    require(studio["pendingChanges"]["added"] >= 2, "Studio added drift expected")
    require(studio["pendingChanges"]["modified"] >= 2, "Studio modified drift expected")
    require(gfis["pendingChanges"]["added"] >= 1, "GFIS controlled residual expected")
    require(gpcf["pendingChanges"] == {"added": 0, "modified": 0, "removed": 0}, "GPCF must be up to date after final sync")
    require("large_generated_validator_exception_candidate" in policy, "GFIS large-file policy missing")

    for key, value in evidence["boundaries"].items():
        require(value is False, f"boundary must remain false: {key}")

    for phrase in [
        "codegraph_active_drift_monitor_evidenced",
        "Brain 与 Studio",
        "modified=36",
        "added=2, modified=2",
        "GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002",
        "不提交、不推送、不部署",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "loop_codegraph_active_drift_monitor=pass "
        "status=codegraph_active_drift_monitor_evidenced "
        f"brain_modified={brain['pendingChanges']['modified']} "
        f"studio_added={studio['pendingChanges']['added']} "
        f"studio_modified={studio['pendingChanges']['modified']} "
        f"gfis_added={gfis['pendingChanges']['added']} "
        "next=GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
