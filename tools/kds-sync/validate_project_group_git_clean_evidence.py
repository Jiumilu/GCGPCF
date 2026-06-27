#!/usr/bin/env python3
"""Validate project-group Git clean evidence and governance references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-git-clean-20260625.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/globalcloud-project-group-git-clean-20260625.json"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

EXPECTED_DIRTY_REPOS = {
    "WAS世界资产体系",
    "GlobalCloud GPC",
    "GlobalCoud GPCF",
    "GlobalCloud KDS",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
}

REQUIRED_DOC_TOKENS = [
    "GlobalCloud 项目群 17 仓 Git Clean 门禁证据 2026-06-25",
    "GPCF-GIT-CLEAN-001",
    "project_group_git_clean = blocked",
    "historical_project_group_git_clean_20260625 = partial",
    "live_recheck_gate_20260628 = blocked",
    "expected_repo_count = 17",
    "checked_repo_count = 17",
    "pass = 10",
    "partial_or_blocked = 7",
    "missing_repos = []",
    "ahead_repos = []",
    "behind_repos = []",
    "sensitive_repos = [GlobalCloud KDS]",
    "project_group_git_clean_pass = false",
    "project_group_git_sensitive_paths = true",
    "project_group_git_behind = false",
    "project_group_git_diff_check = pass",
    "不声明项目群 Git 全量 clean",
    "不声明项目群可提交",
    "不声明项目群可推送",
    "不声明项目群可验收",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-GIT-CLEAN-001",
    "globalcloud-project-group-git-clean-20260625.md",
    "globalcloud-project-group-git-clean-20260625.json",
    "validate_project_group_git_clean_evidence.py",
    "project_group_git_clean = blocked",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "项目群 Git 全量 clean",
    "项目群可提交",
    "项目群可推送",
    "项目群可验收",
    "项目群 ready_for_review",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不得", "false", "partial", "不能"]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def check_forbidden(text: str, failures: list[str]) -> None:
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        start = 0
        while True:
            idx = text.find(token, start)
            if idx == -1:
                break
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if not any(context in line for context in ALLOWED_CONTEXTS):
                failures.append(f"forbidden positive claim without boundary: {line}")
            start = idx + len(token)


def main() -> int:
    failures: list[str] = []
    doc_text = read(EVIDENCE_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in Git clean evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    if not EVIDENCE_JSON.exists():
        failures.append(f"missing JSON evidence: {EVIDENCE_JSON}")
        data = {}
    else:
        data = json.loads(EVIDENCE_JSON.read_text(encoding="utf-8"))

    if data:
        if data.get("gate") != "partial":
            failures.append(f"expected historical JSON gate partial, got {data.get('gate')}")
        if data.get("expected_repo_count") != 17 or data.get("checked_repo_count") != 17:
            failures.append("expected 17 checked repos in JSON evidence")
        summary = data.get("summary", {})
        if summary.get("missing_repos") != []:
            failures.append("expected no missing repos")
        if summary.get("ahead_repos") != []:
            failures.append("expected no ahead repos")
        if summary.get("behind_repos") != []:
            failures.append("expected no behind repos")
        if summary.get("sensitive_repos") != []:
            failures.append("expected no sensitive repos in historical JSON snapshot")
        if set(summary.get("dirty_repos", [])) != EXPECTED_DIRTY_REPOS:
            failures.append(f"dirty repo set mismatch: {summary.get('dirty_repos')}")
        repos = data.get("repos", [])
        if len(repos) != 17:
            failures.append(f"expected 17 repo entries, got {len(repos)}")
        for repo in repos:
            if repo.get("diff_check") != "pass":
                failures.append(f"repo diff_check not pass: {repo.get('name')}")
            if repo.get("sensitive_paths"):
                failures.append(f"repo has sensitive paths: {repo.get('name')}")
            if repo.get("behind") not in (0, None):
                failures.append(f"repo is behind upstream: {repo.get('name')}")

    check_forbidden(doc_text + "\n" + refs_text, failures)

    result = {
        "gate": "project_group_git_clean_evidence",
        "status": "pass" if not failures else "fail",
        "git_clean_status": "blocked",
        "failures": failures,
        "warnings": [
            "This validates read-only Git status evidence only; it does not clean, commit, push, or approve any repository.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
