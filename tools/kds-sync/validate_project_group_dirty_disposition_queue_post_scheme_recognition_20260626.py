#!/usr/bin/env python3
"""Validate the post-scheme-recognition dirty repository disposition queue."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
LIVE_SNAPSHOT = ROOT / "docs/harness/evidence/globalcloud-project-group-live-status-snapshot-20260626.md"

EXPECTED_REPOS = {
    "GlobalCloud AAAS": ["DISP-AAAS-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud Brain": ["DISP-BRAIN-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "WAS世界资产体系": ["DISP-WAS-SCHEME-RECOGNITION-20260626", "noise_decision_required"],
    "GlobalCloud XiaoC": ["DISP-XIAOC-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud WAES": ["DISP-WAES-SCHEME-RECOGNITION-20260626", "existing_repair_boundary"],
    "GlobalCloud GPC": ["DISP-GPC-SCHEME-RECOGNITION-20260626", "existing_review_candidate"],
    "GlobalCloud Studio": ["DISP-STUDIO-SCHEME-RECOGNITION-20260626", "existing_review_candidate"],
    "GlobalCoud GPCF": ["DISP-GPCF-SCHEME-RECOGNITION-20260626", "governance_evidence_review_candidate"],
    "GlobalCloud XWAIL": ["DISP-XWAIL-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud GFIS": ["DISP-GFIS-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud MMC": ["DISP-MMC-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud KDS": ["DISP-KDS-SCHEME-RECOGNITION-20260626", "diff_check_currently_pass"],
    "GlobalCloud XiaoG": ["DISP-XIAOG-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud PVAOS": ["DISP-PVAOS-SCHEME-RECOGNITION-20260626", "existing_review_candidate"],
    "GlobalCloud SOP": ["DISP-SOP-SCHEME-RECOGNITION-20260626", "owner_decision_required"],
    "GlobalCloud PKC": ["DISP-PKC-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
    "GlobalCloud XGD": ["DISP-XGD-SCHEME-RECOGNITION-20260626", "scheme_recognition_review_candidate"],
}

REQUIRED_DOC_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
    "dirty_disposition_queue_post_scheme_recognition_ready",
    "dirty_repo_count | `17`",
    "scheme_recognition_dirty_count | `17`",
    "review_candidate_count | `17`",
    "owner_decision_count | `2`",
    "noise_decision_count | `1`",
    "kds_diffcheck_blocker_count | `0`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "run | 读取 17 个 dirty 仓 live Git 状态",
    "stop | 停止在 `authorization_boundary`",
    "verify | 通过 `validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`",
    "recover | 若队列与 live dirty 不一致",
    "debug | 当前主要阻塞是 review/owner/cleanup 授权边界",
    "project_group_git_clean = partial",
    "当前 KDS `git diff --check` 为 pass",
]

REFERENCE_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md",
    "validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py",
    "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
    "dirty_disposition_queue_post_scheme_recognition_ready",
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
    "KDS diff check 已修复 = true",
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
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(TASKS, failures), read(LIVE_SNAPSHOT, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in post-scheme dirty queue: {token}")

    for repo_name, tokens in EXPECTED_REPOS.items():
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
            failures.append(f"repo is no longer dirty but remains in post-scheme queue: {repo_name}")
        if repo_name not in doc_text:
            failures.append(f"missing repo in post-scheme dirty queue: {repo_name}")
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
        "gate": "project_group_dirty_disposition_queue_post_scheme_recognition_20260626",
        "status": "pass" if not failures else "fail",
        "dirty_repo_count": len(EXPECTED_REPOS),
        "live_dirty_counts": live_dirty,
        "failures": failures,
        "warnings": [
            "This validates the post-scheme-recognition dirty repository disposition queue only; it does not delete files, stage, commit, push, sync KDS API, deploy, or grant accepted/integrated/customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
