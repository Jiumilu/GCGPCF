#!/usr/bin/env python3
"""Validate the GlobalCloud project-group status advancement matrix."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

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

REQUIRED_DOC_TOKENS = [
    "GPCF-STATUS-ADVANCEMENT-001",
    "status_advancement_matrix = controlled",
    "project_status_rule_count = 17",
    "ready_for_review_requires_gate = true",
    "accepted_requires_human_confirmation = true",
    "integrated_requires_human_confirmation = true",
    "customer_accepted_requires_human_confirmation = true",
    "live_project_group_git_gate = blocked",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001",
    "GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001",
    "pre-wave1 review authorization gate",
    "next-stage authorization package gate",
    "next-stage chain loop-round gate",
    "globalcloud-project-group-next-stage-authorization-package-20260627.md",
    "loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md",
    "globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "全局升级规则",
    "禁止升级条件",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-STATUS-ADVANCEMENT-001",
    "globalcloud-project-group-status-advancement-matrix-20260625.md",
    "validate_project_group_status_advancement_matrix.py",
    "status_advancement_matrix = controlled",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
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
    for key in ["accepted", "integrated", "production_ready"]:
        if values.get(key) != "false":
            failures.append(f"GFIS real-fact entry must keep {key}=false, got {values.get(key)!r}")
    return values


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)
    gfis_real_fact_entry = validate_gfis_real_fact_entry(failures)

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in status advancement matrix: {token}")

    for project in PROJECTS:
        rows = []
        for line in doc_text.splitlines():
            if not line.startswith("|") or f"| {project} |" not in line:
                continue
            columns = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(columns) == 11 and columns[1] == project:
                rows.append(line)
        if len(rows) != 1:
            failures.append(f"project must have exactly one status advancement row: {project}")
            continue
        columns = [part.strip() for part in rows[0].strip().strip("|").split("|")]
        required_columns = {
            "current_status": columns[2],
            "target_status": columns[3],
            "task": columns[4],
            "required_evidence": columns[5],
            "required_gate": columns[6],
            "blocker": columns[7],
            "rollback_or_downgrade": columns[8],
            "forbidden_claims": columns[10],
        }
        for name, value in required_columns.items():
            if not value or value == "-":
                failures.append(f"status row missing {name}: {project}")
        if "gate" not in columns[6]:
            failures.append(f"status row gate column must include gate wording: {project}")
        if "不声明" not in columns[10]:
            failures.append(f"status row forbidden claims must include 不声明: {project}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_status_advancement_matrix",
        "status": "pass" if not failures else "fail",
        "project_status_rule_count": len(PROJECTS),
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates advancement criteria only; it does not execute tasks or grant accepted, integrated, production, customer acceptance, commit, push, deploy, or release authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
