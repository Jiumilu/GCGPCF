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
    "WAS世界资产体系": ["DISP-WAS-SYSTEM-NOISE-20260627", "noise_decision_required"],
    "GlobalCloud AAAS": ["DISP-AAAS-LOOP-GATE-DELEGATE-20260627", "loop_gate_delegate_review_candidate"],
    "GlobalCoud GPCF": ["DISP-GPCF-SCHEME-RECOGNITION-20260626", "current_baseline_replay_required"],
    "GlobalCloud XWAIL": ["DISP-XWAIL-LOOP-GATE-DELEGATE-20260627", "loop_gate_delegate_review_candidate"],
    "GlobalCloud GFIS": ["DISP-GFIS-SCHEME-RECOGNITION-20260626", "real_source_record_pending"],
    "GlobalCloud KDS": ["DISP-KDS-SCHEME-RECOGNITION-20260626", "sensitive_path_review_required"],
    "GlobalCloud SOP": ["DISP-SOP-LOOP-GATE-DELEGATE-20260627", "loop_gate_delegate_review_candidate"],
}

REQUIRED_DOC_TOKENS = [
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled",
    "dirty_disposition_queue_post_scheme_recognition_ready",
    "recheck_date | `2026-06-27`",
    "dirty_repo_count | `7`",
    "scheme_recognition_dirty_count | `1`",
    "review_candidate_count | `6`",
    "owner_decision_count | `1`",
    "noise_decision_count | `1`",
    "kds_sensitive_path_count | `1`",
    "review_allowed | `false`",
    "stage_allowed | `false`",
    "commit_allowed | `false`",
    "push_allowed | `false`",
    "delete_allowed | `false`",
    "accepted | `false`",
    "integrated | `false`",
    "production_ready | `false`",
    "customer_accepted | `false`",
    "run | 读取 7 个当前 dirty 仓 live Git 状态",
    "stop | 停止在 `authorization_boundary`",
    "verify | 通过 `validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`",
    "recover | 若队列与 live dirty 不一致",
    "debug | 当前主要阻塞是 KDS sensitive_path、GFIS 真实 SOR 阻塞、GPCF 治理 review 边界、WAS system noise cleanup，以及 AAAS/XWAIL/SOP delegated wrapper 的保留范围确认",
    "project_group_git_clean = blocked",
    "当前 KDS `git diff --check` 为 pass",
    "4.1 A 项单仓核对卡 / 4.2 A 项确认后状态传导摘要",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
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
