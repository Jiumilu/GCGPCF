#!/usr/bin/env python3
"""Validate Studio workflow permissions recheck evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDIO_REPO = ROOT.parent / "GlobalCloud Studio"
DOC = ROOT / "docs/harness/Studio/evidence/studio-workflow-permissions-recheck-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

STUDIO_PLAN = STUDIO_REPO / "GlobalCloud Studio 实施方案.md"
STUDIO_PACKAGE = STUDIO_REPO / "package.json"
STUDIO_INDEX = STUDIO_REPO / "docs/harness/evidence/evidence-index.md"
STUDIO_LOOP_STATE = STUDIO_REPO / "docs/harness/loop-state.md"
STUDIO_LR_024 = STUDIO_REPO / "docs/harness/loops/loop-round-GPCF-STUDIO-LR-024.md"
STUDIO_HARDENING_JSON = STUDIO_REPO / "docs/harness/evidence/studio-workflow-permissions-hardening-20260621.json"
STUDIO_HARDENING_MD = STUDIO_REPO / "docs/harness/evidence/studio-workflow-permissions-hardening-20260621.md"

REQUIRED_DOC_TOKENS = [
    "STUDIO-WORKFLOW-PERMISSIONS-001",
    "studio_workflow_permissions_recheck = controlled",
    "target_status_candidate = release_boundary_recheck_passed / local_release_review_boundary",
    "harness_check = pass",
    "workflow_release_boundary = pass",
    "workflow_permissions_hardening = pass",
    "test = pass",
    "test_files = 256 passed",
    "tests = 1919 passed / 2 skipped / 1921 total",
    "build = pass",
    "evidence_index_repaired = true",
    "studio_dirty_files = docs/harness/evidence/evidence-index.md",
    "release_executed = false",
    "github_release_write_executed = false",
    "deployment_executed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "studio_workflow_release_boundary=pass",
    "studio_workflow_permissions_hardening=pass",
    "不声明 Studio 已发布",
    "不声明 GitHub release 已写入",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud Studio 实施方案",
    "project: Studio",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
]

REQUIRED_PACKAGE_TOKENS = [
    '"harness:check": "node scripts/harness-check.mjs"',
    '"test": "vitest run"',
    '"build": "npm run openapi:generate && vue-tsc -b && vite build && tsc --noEmit -p packages/server/tsconfig.json && node scripts/build-server.mjs"',
]

REQUIRED_INDEX_TOKENS = [
    "docs/harness/evidence/studio-workflow-permissions-hardening-20260621.json",
    "docs/harness/evidence/studio-workflow-permissions-hardening-20260621.md",
    "docs/harness/loops/loop-round-GPCF-STUDIO-LR-024.md",
]

REQUIRED_REF_TOKENS = [
    "STUDIO-WORKFLOW-PERMISSIONS-001",
    "studio-workflow-permissions-recheck-20260625.md",
    "validate_studio_workflow_permissions_recheck.py",
    "release_boundary_recheck_passed / local_release_review_boundary",
]

FORBIDDEN_CLAIMS = [
    "release_executed = true",
    "github_release_write_executed = true",
    "deployment_executed = true",
    "production_ready = true",
    "accepted = true",
    "integrated = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    plan_text = read(STUDIO_PLAN, failures)
    package_text = read(STUDIO_PACKAGE, failures)
    index_text = read(STUDIO_INDEX, failures)
    loop_state_text = read(STUDIO_LOOP_STATE, failures)
    hardening_json_text = read(STUDIO_HARDENING_JSON, failures)
    refs_text = "\n".join(
        [
            read(BOARD, failures),
            read(REGISTER, failures),
            read(STATUS, failures),
            read(BASELINE, failures),
            read(TASKS, failures),
        ]
    )

    for path in [STUDIO_REPO, STUDIO_LR_024, STUDIO_HARDENING_MD]:
        if not path.exists():
            failures.append(f"missing Studio path: {path}")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in Studio recheck evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in Studio implementation plan: {token}")

    for token in REQUIRED_PACKAGE_TOKENS:
        if token not in package_text:
            failures.append(f"missing script token in Studio package.json: {token}")

    for token in REQUIRED_INDEX_TOKENS:
        if token not in index_text:
            failures.append(f"missing token in Studio evidence-index: {token}")

    for token in [
        "current_round | `GPCF-STUDIO-LR-024`",
        "workflow_release_boundary_status | `permissions_hardened_release_review_required`",
        "production_ready | `false`",
    ]:
        if token not in loop_state_text:
            failures.append(f"missing token in Studio loop-state: {token}")

    if hardening_json_text:
        try:
            evidence = json.loads(hardening_json_text)
        except json.JSONDecodeError as exc:
            failures.append(f"invalid Studio hardening json: {exc}")
        else:
            if evidence.get("explicit_permissions_declared") is not True:
                failures.append("Studio hardening evidence must declare explicit permissions")
            boundaries = evidence.get("status_boundaries", {})
            for key in ["accepted", "integrated", "production_ready", "release_executed"]:
                if boundaries.get(key) is not False:
                    failures.append(f"Studio hardening boundary must remain false: {key}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive Studio claim: {token}")

    result = {
        "gate": "studio_workflow_permissions_recheck",
        "status": "pass" if not failures else "fail",
        "task_id": "STUDIO-WORKFLOW-PERMISSIONS-001",
        "target_status_candidate": "release_boundary_recheck_passed / local_release_review_boundary",
        "harness_check": "pass",
        "workflow_permissions_hardening": "pass",
        "test_files": "256 passed",
        "tests": "1919 passed / 2 skipped",
        "build": "pass",
        "release_executed": False,
        "github_release_write_executed": False,
        "deployment_executed": False,
        "failures": failures,
        "warnings": [
            "This validates Studio local workflow permission recheck only; it does not validate release execution, GitHub release writes, deployment, accepted, integrated, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
