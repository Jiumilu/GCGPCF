#!/usr/bin/env python3
"""Validate external project loop gates delegate to the GPCF canonical gate."""

from __future__ import annotations

from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
PROJECT_GROUP_ROOT = ROOT.parent
DELEGATED_REPOS = [
    "GlobalCloud AAAS",
    "GlobalCloud XWAIL",
    "GlobalCloud SOP",
]
REQUIRED_TOKENS = [
    "Delegate project-group loop gate execution to the GPCF canonical gate",
    'GPCF_ROOT = ROOT.parent / "GlobalCoud GPCF"',
    'GPCF_GATE = GPCF_ROOT / "tools/kds-sync/loop_document_gate.py"',
    'env["GPCF_PROJECT_GROUP_GATE_DELEGATED"] = "1"',
    '[sys.executable, str(GPCF_GATE), "--check-only"]',
    "raise SystemExit(result.returncode)",
]
FORBIDDEN_TOKENS = [
    "accepted=true",
    "integrated=true",
    "production_ready=true",
    "customer_accepted=true",
    "status_promotion_allowed=true",
    "gate = \"pass\"",
    "gate='pass'",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_project_group_external_loop_gate_delegates: {message}")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    checked = 0

    for repo_name in DELEGATED_REPOS:
        gate = PROJECT_GROUP_ROOT / repo_name / "tools/kds-sync/loop_document_gate.py"
        require(gate.exists(), f"missing delegated gate: {repo_name}")
        text = gate.read_text(encoding="utf-8")
        for token in REQUIRED_TOKENS:
            require(token in text, f"{repo_name} delegated gate missing token: {token}")
        for token in FORBIDDEN_TOKENS:
            require(token not in text, f"{repo_name} delegated gate contains forbidden token: {token}")
        checked += 1

    print(
        "project_group_external_loop_gate_delegates=pass "
        f"checked_repos={checked} "
        "delegation_only=true "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')} "
        f"formal_confirmation_files={gfis_real_fact_entry.get('formal_confirmation_files')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
