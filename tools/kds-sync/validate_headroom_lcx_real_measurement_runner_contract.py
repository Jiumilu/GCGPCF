#!/usr/bin/env python3
"""Validate the Headroom LCX real-measurement runner contract evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-real-measurement-runner-contract-20260623.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-001.md"
RUNNER = ROOT / "tools/kds-sync/build_headroom_lcx_real_measurement_runner_contract.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-23",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def main() -> int:
    contract = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    runner = read(RUNNER)

    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    require("real_measurement_runner_contract" in runner, "runner must build runner contract")
    require(contract.get("contract_id") == "HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623", "invalid contract id")
    require(contract.get("status") == "runner_contract_defined_precheck_only", "invalid contract status")
    require(contract.get("scope", {}).get("project_count") == 15, "project count mismatch")
    require(contract.get("current_state", {}).get("production_branch_blocked") is True, "production branch must remain blocked")
    require(contract.get("runner_contract", {}).get("execution_mode") == "precheck_only", "execution mode must be precheck_only")
    require(contract.get("runner_contract", {}).get("execution_allowed_now") is False, "execution must remain blocked")
    require(len(contract.get("runner_contract", {}).get("allowed_inputs", [])) == 6, "allowed input count mismatch")
    require(len(contract.get("runner_contract", {}).get("forbidden_inputs", [])) >= 10, "forbidden input count too short")
    require(contract.get("rollback_anchor", {}).get("rollback_plan_present") is True, "rollback plan must be present")
    require(contract.get("rollback_anchor", {}).get("rollback_runbook_written") is True, "rollback runbook must be written")
    require(contract.get("precheck_anchor", {}).get("authorization_complete") is True, "authorization complete must be true at precheck")
    require(contract.get("precheck_anchor", {}).get("missing_required_field_count_zero") is True, "missing required field count must be zero")

    binding = contract.get("field_binding", [])
    require(len(binding) == 6, "field binding count mismatch")
    for row in binding:
        require(row.get("binding_state") == "precheck_only", f"binding state must be precheck_only: {row.get('field')}")
        require(row.get("runner_input") == row.get("field"), f"runner input mismatch: {row.get('field')}")

    for phrase in [
        "HEADROOM-LCX-REAL-MEASUREMENT-RUNNER-CONTRACT-20260623",
        "runner_contract_defined_precheck_only",
        "execution_allowed_now: `false`",
        "production_branch_blocked: `true`",
        "production_token_measurement_allowed: `false`",
        "production_ready: `false`",
    ]:
        require(phrase in md, f"evidence md missing phrase: {phrase}")

    for phrase in [
        "runner contract",
        "build_headroom_lcx_real_measurement_runner_contract.py",
        "validate_headroom_lcx_real_measurement_runner_contract.py",
    ]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    print(
        "headroom_lcx_real_measurement_runner_contract=pass "
        "project_count=15 execution_allowed_now=false "
        "production_token_measurement_allowed=false measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
