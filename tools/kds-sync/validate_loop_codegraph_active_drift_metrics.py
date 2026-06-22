#!/usr/bin/env python3
"""Validate CodeGraph active drift metrics evidence."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-codegraph-active-drift-metrics-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002.md"
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

    require(evidence["evidence_id"] == "LOOP-CODEGRAPH-ACTIVE-DRIFT-METRICS-20260621", "invalid evidence id")
    require(evidence["status"] == "codegraph_active_drift_metrics_evidenced", "invalid status")
    require(evidence["scope"] == "GPCF-CODEGRAPH-ACTIVE-DRIFT-METRICS-002", "invalid scope")
    require(evidence["metrics_window"]["elapsed_minutes"] == 119, "elapsed minutes mismatch")
    require(evidence["metrics_window"]["mttd"] == "seeded", "MTTD must be seeded")
    require(evidence["metrics_window"]["mttr"] == "unavailable_until_drift_closes", "MTTR must be unavailable")

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

    brain_obs = observations["GlobalCloud Brain"]
    studio_obs = observations["GlobalCloud Studio"]
    require(brain_obs["delta"]["modified"] == 17, "Brain delta must be +17")
    require(brain["pendingChanges"]["modified"] >= brain_obs["current_pending_changes"]["modified"], "Brain current drift must not be below evidence")
    require(studio["pendingChanges"]["added"] >= studio_obs["current_pending_changes"]["added"], "Studio added drift must not be below evidence")
    require(studio["pendingChanges"]["modified"] >= studio_obs["current_pending_changes"]["modified"], "Studio modified drift must not be below evidence")
    require(gfis["pendingChanges"]["added"] >= 1, "GFIS controlled residual expected")
    require(gpcf["pendingChanges"] == {"added": 0, "modified": 0, "removed": 0}, "GPCF must be up to date after final sync")
    require("large_generated_validator_exception_candidate" in policy, "GFIS policy missing")

    boundary = evidence["authorization_boundary"]
    require(boundary["git_gate"] == "blocked", "git gate must be blocked")
    require(boundary["sync_only_authorized_for_brain_or_studio"] is False, "Brain/Studio sync-only must not be authorized")
    require(evidence["decision"]["result"] == "continue_read_only_metrics_until_sync_only_authorized", "invalid decision")
    require(evidence["next_loop_input"]["round"] == "GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003", "invalid next loop input")

    for key, value in evidence["boundaries"].items():
        require(value is False, f"boundary must remain false: {key}")

    for phrase in [
        "codegraph_active_drift_metrics_evidenced",
        "modified=56",
        "modified=+17",
        "GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003",
        "requires explicit authorization",
        "不提交、不推送、不部署",
    ]:
        require(phrase in evidence_md, f"evidence md missing phrase: {phrase}")
    for phrase in ["输入", "动作", "输出", "检查", "反馈", "GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "loop_codegraph_active_drift_metrics=pass "
        "status=codegraph_active_drift_metrics_evidenced "
        f"brain_modified={brain['pendingChanges']['modified']} "
        f"studio_added={studio['pendingChanges']['added']} "
        f"studio_modified={studio['pendingChanges']['modified']} "
        f"gfis_added={gfis['pendingChanges']['added']} "
        "decision=continue_read_only_metrics_until_sync_only_authorized "
        "next=GPCF-CODEGRAPH-SYNC-ONLY-AUTHORIZATION-003"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
