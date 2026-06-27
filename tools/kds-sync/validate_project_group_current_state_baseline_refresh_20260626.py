#!/usr/bin/env python3
"""Validate the 2026-06-26 project-group current-state baseline refresh evidence."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"

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

REQUIRED_TOKENS = [
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "project_count = 17",
    "recheck_date = 2026-06-27",
    "git_gate = blocked",
    "dirty_repo_count = 7",
    "review_boundary_repo_count = 6",
    "noise_cleanup_repo_count = 1",
    "pass_repo_count = 10",
    "ahead_repos = 0",
    "behind_repos = 0",
    "sensitive_repos = 1",
    "dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP",
    "noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)",
    "sensitive_repos_current = GlobalCloud KDS(.env.production.example)",
    "diff_check = pass",
    "development_queue_ready = true",
    "trigger_layer_binding_count = 17",
    "dependency_edge_binding_count = 17",
    "auto_ready_for_review_upgrade = false",
    "authorization_granted = false",
    "action_executed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "dirty=231 / untracked=72 / diff_check=pass",
    "dirty=54 / untracked=0 / diff_check=pass",
    "dirty=38 / untracked=33 / diff_check=pass / sensitive_path=.env.production.example",
    "AAAS-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "SOP-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001",
    "4.1 A 项单仓核对卡 / 4.2 A 项确认后状态传导摘要",
    "5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要",
    "5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要",
    "5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要",
    "5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要",
    "WAES-LINT-RUNTIME-001",
    "GFIS-REAL-SOR-001",
    "GPC-EXTERNAL-RUNTIME-EVIDENCE-001",
    "BRAIN-HUMAN-REVIEW-DECISION-001",
    "GPCF-KDS-DIFFCHECK-CLEANUP-COMMAND-PACK-20260626-001",
    "GPCF-POST-SCHEME-RECOGNITION-REVIEW-AUTHORIZATION-REQUEST-20260626-001",
    "globalcloud-project-group-dev-task-queue-20260626.md",
]

FORBIDDEN_TOKENS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "auto_ready_for_review_upgrade = true",
    "authorization_granted = true",
    "action_executed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
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
    for key in ["accepted", "integrated", "production_ready", "customer_accepted"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    doc = read(DOC, failures)
    board = read(BOARD, failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in REQUIRED_TOKENS:
        if token not in doc:
            failures.append(f"missing token in current baseline refresh: {token}")

    for project in PROJECTS:
        if project not in doc:
            failures.append(f"missing project in current baseline refresh: {project}")

    for token in FORBIDDEN_TOKENS:
        if token in doc:
            failures.append(f"forbidden positive claim in current baseline refresh: {token}")

    if "globalcloud-project-group-current-state-baseline-refresh-20260626.md" not in board:
        failures.append("governance board missing current-state baseline refresh reference")

    result = {
        "gate": "project_group_current_state_baseline_refresh_20260626",
        "status": "pass" if not failures else "fail",
        "project_count": len(PROJECTS),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates current-state baseline refresh evidence only; it does not execute tasks, clean repos, stage, commit, push, deploy, sync KDS API, or grant accepted/integrated/customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
