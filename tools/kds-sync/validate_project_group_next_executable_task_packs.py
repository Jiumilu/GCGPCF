#!/usr/bin/env python3
"""Validate GlobalCloud next executable task packs for all projects."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

TASKS = [
    "AAAS-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "AAAS-WAES-BINDING-PRECHECK-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "WAS-XWAIL-ONTOLOGY-MAPPING-001",
    "XIAOC-MODEL-ROUTING-DRYRUN-001",
    "WAES-LINT-RUNTIME-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "STUDIO-WORKFLOW-PERMISSIONS-001",
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
    "GPCF-DIRTY-DISPOSITION-QUEUE-001",
    "GPCF-LIVE-STATUS-SNAPSHOT-20260626-001",
    "GPCF-LOOP-GATE-READINESS-PASS-20260626-001",
    "GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-TEMPLATE-20260626-001",
    "GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001",
    "GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001",
    "GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001",
    "GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001",
    "GPCF-KDS-DIFFCHECK-BLOCKER-20260626-001",
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001",
    "GPCF-SCHEME-RECOGNITION-RULES-20260626-001",
    "GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "GPCF-EXTERNAL-LOOP-GATE-DELEGATE-BASELINE-20260627-001",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001",
    "GPCF-LOOP-DOCUMENT-GATE-READINESS-RETRY-HARDENING-20260626-001",
    "XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001",
    "GFIS-REAL-SOR-001",
    "MMC-GOVERNANCE-TEMPLATE-SMOKE-001",
    "KDS-BRAIN-REPORT-HOLD-REVIEW-001",
    "XIAOG-LIVE-API-AUTH-PACK-001",
    "PVAOS-RELEASE-REVIEW-001",
    "SOP-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "SOP-SCENARIO-OWNER-REVIEW-001",
    "PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001",
    "XGD-TICK-BRAIN-SMOKE-001",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-NEXT-TASK-PACKS-001",
    "next_executable_task_packs = controlled",
    "project_task_pack_count = 17",
    "task_row_count = 41",
    "trigger_layer_binding_count = 41",
    "dependency_edge_binding_count = 41",
    "任务级 Trigger Layer 与 Dependency Edge 绑定",
    "| task_id | trigger_layer | dependency_edge | authoritative_entry | 绑定说明 |",
    "project_group_git_clean = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "Wave 1",
    "Wave 2",
    "Wave 3",
    "Governance",
    "globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md",
    "validate_project_group_external_loop_gate_delegate_baseline_20260627.py",
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "第 `5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要`",
    "第 `5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要`",
    "第 `5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要`",
    "validate_project_group_pre_wave1_review_authorization_request_20260627.py",
    "需要真实业务 owner",
    "stage、commit、push、delete、deploy、release、merge",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-NEXT-TASK-PACKS-001",
    "globalcloud-project-group-next-executable-task-packs-20260625.md",
    "validate_project_group_next_executable_task_packs.py",
    "next_executable_task_packs = controlled",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in next task packs: {token}")

    for task in TASKS:
        rows = []
        for line in doc_text.splitlines():
            if not line.startswith("|") or f"`{task}`" not in line:
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) >= 2 and columns[1] == f"`{task}`":
                rows.append(line)
        if len(rows) != 1:
            failures.append(f"task must have exactly one row: {task}")
            continue
        row = rows[0]
        columns = [part.strip() for part in row.strip().strip("|").split("|")]
        if len(columns) != 12:
            failures.append(f"task row must have 12 columns: {task}")
            continue
        required_columns = {
            "commands": columns[5],
            "expected_evidence": columns[6],
            "gate": columns[7],
            "rollback_boundary": columns[8],
            "dependency_impact": columns[9],
            "forbidden_claims": columns[11],
        }
        for name, value in required_columns.items():
            if not value or value == "-":
                failures.append(f"task row missing {name}: {task}")
        if ".md" not in columns[6]:
            failures.append(f"task expected evidence must be markdown evidence: {task}")
        if "gate" not in columns[7]:
            failures.append(f"task gate column must include gate wording: {task}")
        if "不声明" not in columns[11]:
            failures.append(f"task forbidden claims column must include 不声明: {task}")

    binding_rows: dict[str, list[str]] = {}
    for line in doc_text.splitlines():
        if not line.startswith("|"):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) != 5:
            continue
        if not columns[0].startswith("`") or not columns[0].endswith("`"):
            continue
        task = columns[0].strip("`")
        if task not in TASKS:
            continue
        binding_rows.setdefault(task, []).append(line)

    if len(binding_rows) != len(TASKS):
        failures.append(
            f"task binding table must cover {len(TASKS)} tasks, found {len(binding_rows)}"
        )

    for task in TASKS:
        rows = binding_rows.get(task, [])
        if len(rows) != 1:
            failures.append(f"task binding must have exactly one row: {task}")
            continue
        columns = [part.strip() for part in rows[0].strip().strip("|").split("|")]
        trigger_layer, dependency_edge, authoritative_entry, note = columns[1:]
        if not trigger_layer.startswith("`") or not trigger_layer.endswith("`"):
            failures.append(f"task binding trigger_layer must be explicit: {task}")
        if not dependency_edge.startswith("`") or not dependency_edge.endswith("`"):
            failures.append(f"task binding dependency_edge must be explicit: {task}")
        if not authoritative_entry.startswith("`") or not authoritative_entry.endswith("`"):
            failures.append(f"task binding authoritative_entry must be explicit: {task}")
        if not note or note == "-":
            failures.append(f"task binding note must be non-empty: {task}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_next_executable_task_packs",
        "status": "pass" if not failures else "fail",
        "task_pack_count": len(TASKS),
        "failures": failures,
        "warnings": [
            "This validates task-pack control fields only; it does not execute project tasks or grant commit, push, accepted, integrated, production, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
