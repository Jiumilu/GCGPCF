#!/usr/bin/env python3
"""Validate the project-group ready-for-review advancement queue."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUEUE = ROOT / "docs/harness/evidence/globalcloud-project-group-ready-for-review-advancement-queue-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
CORE_REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
TASK_PACKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
STATUS_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

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

REQUIRED_QUEUE_TOKENS = [
    "GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001",
    "project_group_ready_for_review_advancement_queue_20260626 = controlled",
    "ready_for_review_advancement_queue_ready",
    "project_count | `17`",
    "already_ready_or_review_boundary | `5`",
    "review_candidate_or_precheck | `4`",
    "blocked_by_repair_or_external_evidence | `4`",
    "blocked_by_owner_or_authorization | `4`",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "auto_ready_for_review_upgrade=false",
    "accepted=false",
    "integrated=false",
    "production_ready=false",
    "customer_accepted=false",
    "WAES-LINT-RUNTIME-001",
    "GFIS-REAL-SOR-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "AAAS-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "SOP-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001",
    "pre-wave1 review authorization gate",
    "next-stage authorization package gate",
    "next-stage chain loop-round gate",
    "external delegate baseline gate",
]

REQUIRED_GOVERNANCE_TOKENS = [
    "GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001",
    "globalcloud-project-group-ready-for-review-advancement-queue-20260626.md",
    "validate_project_group_ready_for_review_advancement_queue_20260626.py",
    "project_group_ready_for_review_advancement_queue_20260626 = controlled",
    "ready_for_review_advancement_queue_ready",
]

FORBIDDEN_TOKENS = [
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
    "auto_ready_for_review_upgrade=true",
    "可自动进入 ready_for_review | `true`",
]

GFIS_ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "formal_confirmation_files",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def require_tokens(label: str, text: str, tokens: list[str], failures: list[str]) -> None:
    for token in tokens:
        if token not in text:
            failures.append(f"{label} missing token: {token}")


def parse_kv_output(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for part in output.replace("\n", " ").split():
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        parsed[key.strip()] = value.strip().strip(",")
    return parsed


def validate_gfis_real_fact_entry(failures: list[str]) -> dict[str, str]:
    cached = os.environ.get("GPCF_GFIS_REAL_FACT_ENTRY_GATE_OUTPUT")
    if cached:
        values = parse_kv_output(cached)
    else:
        result = subprocess.run(
            ["python3", "tools/kds-sync/validate_gfis_real_fact_entry_gate.py"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
        values = parse_kv_output(result.stdout)
        if result.returncode != 0:
            failures.append("GFIS real-fact entry gate failed: " + result.stdout.strip())
            return values
    if values.get("strong_block") != "true":
        failures.append("GFIS real-fact entry gate must keep strong_block=true")
    if values.get("status_ceiling") != "repair_required":
        failures.append("GFIS real-fact entry status ceiling must remain repair_required")
    for key in GFIS_ZERO_KEYS:
        if values.get(key) != "0":
            failures.append(f"GFIS real-fact entry must keep {key}=0, got {values.get(key)!r}")
    for key in ["accepted", "integrated", "production_ready"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    queue_text = read(QUEUE, failures)
    board_text = read(BOARD, failures)
    core_register_text = read(CORE_REGISTER, failures)
    task_packs_text = read(TASK_PACKS, failures)
    status_matrix_text = read(STATUS_MATRIX, failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    require_tokens("queue", queue_text, REQUIRED_QUEUE_TOKENS, failures)

    for project in PROJECTS:
        if project not in queue_text:
            failures.append(f"queue missing project: {project}")

    rows = [
        line
        for line in queue_text.splitlines()
        if line.startswith("| `") and any(project in line for project in PROJECTS)
    ]
    if len(rows) != 17:
        failures.append(f"queue must have 17 project rows, found {len(rows)}")
    if queue_text.count("| `false` |") < 17:
        failures.append("all project rows must explicitly disable automatic ready_for_review upgrade")

    for token in FORBIDDEN_TOKENS:
        if token in queue_text:
            failures.append(f"queue contains forbidden upgrade token: {token}")

    for label, text in [
        ("board", board_text),
        ("core register", core_register_text),
        ("task packs", task_packs_text),
        ("status matrix", status_matrix_text),
    ]:
        require_tokens(label, text, REQUIRED_GOVERNANCE_TOKENS, failures)

    result = {
        "gate": "project_group_ready_for_review_advancement_queue_20260626",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "auto_ready_for_review_upgrade": False,
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates advancement queue control only; it does not upgrade project status or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
