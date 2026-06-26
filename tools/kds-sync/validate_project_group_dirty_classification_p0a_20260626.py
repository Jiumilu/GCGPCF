#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group P0-A dirty classification evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = ROOT.parent

EVIDENCE = ROOT / "docs/harness/evidence/globalcloud-project-group-dirty-classification-p0a-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-DIRTY-CLASSIFICATION-P0A-001.md"
GIT_GATE = ROOT / ".codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py"

PROJECTS = [
    "GlobalCloud AAAS",
    "GlobalCloud Brain",
    "WAS世界资产体系",
    "GlobalCloud XiaoC",
    "GlobalCloud WAES",
    "GlobalCloud GPC",
    "GlobalCloud Studio",
    "GlobalCoud GPCF",
    "GlobalCloud XWAIL",
    "GlobalCloud GFIS",
    "GlobalCloud MMC",
    "GlobalCloud KDS",
    "GlobalCloud XiaoG",
    "GlobalCloud PVAOS",
    "GlobalCloud SOP",
    "GlobalCloud PKC",
    "GlobalCloud XGD",
]

REQUIRED_EVIDENCE_TOKENS = [
    "dirty_classification_ready = true",
    "development_start_allowed = true",
    "project_group_git_gate = partial",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "WAES 授权不是开发态全面启动的最大阻点",
]

REQUIRED_CLASSIFICATIONS = [
    "scheme_transmission_review_candidate",
    "governance_evidence_kds_mirror_queue",
    "knowledge_import_governance_queue",
    "release_review_readiness_candidate",
    "build_artifact_review_candidate",
    "sop_operations_owner_review_candidate",
]


def run(cmd: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def validate_git_gate(failures: list[str]) -> str:
    gate = run(["python3", str(GIT_GATE), "--root", str(PROJECT_ROOT)])
    if gate.returncode not in (0, 2):
        failures.append(f"unexpected git gate returncode: {gate.returncode}")
        return "unknown"
    try:
        data = json.loads(gate.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"git gate JSON parse failed: {exc}")
        return "unknown"

    gate_status = str(data.get("gate", "unknown"))
    if gate_status not in {"partial", "pass"}:
        failures.append(f"git gate not partial/pass: {gate_status}")

    if data.get("checked_repo_count") != len(PROJECTS):
        failures.append(f"checked repo count mismatch: {data.get('checked_repo_count')}")
    if data.get("expected_repo_count") != len(PROJECTS):
        failures.append(f"expected repo count mismatch: {data.get('expected_repo_count')}")

    summary = data.get("summary", {})
    for key in ["missing_repos", "ahead_repos", "behind_repos", "sensitive_repos"]:
        if summary.get(key) != []:
            failures.append(f"{key} present: {summary.get(key)}")

    seen = {repo.get("name") for repo in data.get("repos", [])}
    for project in PROJECTS:
        if project not in seen:
            failures.append(f"project missing from git gate: {project}")

    for repo in data.get("repos", []):
        if repo.get("diff_check") != "pass":
            failures.append(f"diff-check not pass: {repo.get('name')}")
        if repo.get("sensitive_paths"):
            failures.append(f"sensitive paths present: {repo.get('name')}")
        if not repo.get("exists") or not repo.get("is_git_repo"):
            failures.append(f"repo unavailable: {repo.get('name')}")
    return gate_status


def main() -> int:
    failures: list[str] = []
    evidence = read(EVIDENCE, failures)
    loop_round = read(LOOP_ROUND, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence:
            failures.append(f"missing evidence token: {token}")
    for token in REQUIRED_CLASSIFICATIONS:
        if token not in evidence:
            failures.append(f"missing classification token: {token}")
    for project in PROJECTS:
        if project not in evidence:
            failures.append(f"missing project in evidence: {project}")
    for section in ["run", "stop", "verify", "recover", "debug"]:
        if f"## {section}" not in loop_round:
            failures.append(f"missing loop section: {section}")

    git_gate = validate_git_gate(failures)

    result = {
        "project_group_dirty_classification_p0a": "pass" if not failures else "fail",
        "checked_projects": len(PROJECTS),
        "git_gate": git_gate,
        "hard_blockers_absent": not failures,
        "accepted": False,
        "integrated": False,
        "production_ready": False,
        "customer_accepted": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
