#!/usr/bin/env python3
"""Validate the project-group dirty repository disposition queue."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

DIRTY_REPOS = {
    "WAS世界资产体系": ["DISP-WAS-SYSTEM-NOISE-20260625", ".DS_Store", "noise_decision_required"],
    "GlobalCoud GPCF": ["DISP-GPCF-GOVERNANCE-EVIDENCE-20260625", "PKG-GPCF-KDS-MIRROR-20260625", "review_candidate_with_mirror_boundary"],
    "GlobalCloud AAAS": ["DISP-AAAS-DELEGATE-REVIEW-20260628", "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md", "noise_or_review_boundary_confirmation_required"],
    "GlobalCloud XWAIL": ["DISP-XWAIL-DELEGATE-REVIEW-20260628", "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md", "noise_or_review_boundary_confirmation_required"],
    "GlobalCloud GFIS": ["DISP-GFIS-REAL-SOR-20260628", "gfis-real-runtime-baseline-20260624.md", "owner_decision_required"],
    "GlobalCloud KDS": ["DISP-KDS-FUNDING-SYNC-RUNS-20260625", "kds-brain-report-hold-review-20260625.md", "owner_decision_required"],
    "GlobalCloud SOP": ["DISP-SOP-WUHAN-SCENARIO-20260625", "sop-scenario-owner-review-20260625.md", "owner_decision_required"],
}

REQUIRED_DOC_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-001",
    "project_group_dirty_disposition_queue = controlled",
    "dirty_disposition_queue_ready",
    "dirty_repo_count | `7`",
    "review_candidate_count | `1`",
    "owner_decision_count | `2`",
    "noise_decision_count | `4`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "run | 读取 7 个 dirty 仓 live Git 状态",
    "stop | 停止在 `authorization_boundary`",
    "verify | 通过 `validate_project_group_dirty_disposition_queue.py`",
    "recover | 若队列与 live dirty 不一致",
    "debug | 当前主要阻塞不是技术不可执行",
]

REFERENCE_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-001",
    "globalcloud-project-group-dirty-disposition-queue-20260625.md",
    "validate_project_group_dirty_disposition_queue.py",
    "dirty_disposition_queue_ready",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "review_allowed | `true`",
    "stage_allowed | `true`",
    "commit_allowed | `true`",
    "push_allowed | `true`",
    "delete_allowed | `true`",
    "accepted | `true`",
    "integrated | `true`",
    "production_ready | `true`",
    "customer_accepted | `true`",
    "项目群 Git 全量 clean = true",
    "真实 KDS API 已同步 = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def git_status(repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    failures: list[str] = []
    live_dirty: dict[str, int] = {}
    doc_text = read(DOC, failures)
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(STATUS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in dirty disposition queue: {token}")

    for repo_name, tokens in DIRTY_REPOS.items():
        repo = PROJECT_ROOT / repo_name
        if not repo.exists():
            failures.append(f"missing repo: {repo_name}")
            continue
        try:
            status_lines = git_status(repo)
        except subprocess.CalledProcessError as exc:
            failures.append(f"git status failed for {repo_name}: {exc.stderr.strip()}")
            continue
        live_dirty[repo_name] = len(status_lines)
        if not status_lines:
            failures.append(f"repo is no longer dirty but remains in queue: {repo_name}")
        if repo_name not in doc_text:
            failures.append(f"missing repo in dirty disposition queue: {repo_name}")
        for token in tokens:
            if token not in doc_text:
                failures.append(f"missing queue token for {repo_name}: {token}")

    for token in REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing governance reference token: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive claim: {token}")

    result = {
        "gate": "project_group_dirty_disposition_queue",
        "status": "pass" if not failures else "fail",
        "dirty_repo_count": len(DIRTY_REPOS),
        "live_dirty_counts": live_dirty,
        "failures": failures,
        "warnings": [
            "This validates the dirty repository disposition queue only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
