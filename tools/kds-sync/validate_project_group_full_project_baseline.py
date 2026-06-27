#!/usr/bin/env python3
"""Validate the GlobalCloud full project real-state baseline evidence."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
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
    "GPCF-FULL-PROJECT-BASELINE-001",
    "expected_project_count | 17",
    "checked_project_count | 17",
    "full_project_baseline = controlled",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
    "globalcloud-project-group-current-state-baseline-refresh-20260626.md",
    "globalcloud-project-group-dev-task-queue-20260626.md",
    "project_group_git_clean = blocked",
    "dirty_repo_count = 7",
    "sensitive_repos = GlobalCloud KDS(.env.production.example)",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "ready_for_review",
    "partial_or_repair",
    "governance_controlled",
    "baseline_only",
    "BASELINE-ONLY-PROJECT-TASK-PACKS",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-FULL-PROJECT-BASELINE-001",
    "globalcloud-project-group-full-project-baseline-20260625.md",
    "validate_project_group_full_project_baseline.py",
    "full_project_baseline = controlled",
    "project_group_current_state_baseline_refresh_20260626 = controlled",
    "development_queue_ready = true",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "project_group_git_clean = pass",
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
            failures.append(f"missing token in full project baseline: {token}")

    for project in PROJECTS:
        row_prefix = f"|"
        if project not in doc_text:
            failures.append(f"missing project in full project baseline: {project}")
            continue
        rows = [line for line in doc_text.splitlines() if line.startswith(row_prefix) and f"| {project} |" in line]
        if len(rows) != 1:
            failures.append(f"project must have exactly one baseline row: {project}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "project_group_full_project_baseline",
        "status": "pass" if not failures else "fail",
        "projects_checked": len(PROJECTS),
        "baseline": "controlled" if not failures else "failed",
        "gfis_real_fact_entry": gfis_real_fact_entry,
        "failures": failures,
        "warnings": [
            "This validates 17-project baseline coverage only; it does not grant accepted, integrated, production, customer acceptance, commit, or push authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
