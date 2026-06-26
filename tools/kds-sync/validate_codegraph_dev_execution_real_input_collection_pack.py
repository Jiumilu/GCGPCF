#!/usr/bin/env python3
"""Validate CodeGraph real-input collection pack evidence."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-collection-pack-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-collection-pack-20260626.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-018.md"
READINESS = ROOT / "docs/harness/evidence/codegraph-dev-execution-real-input-readiness-20260626.json"


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


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    readiness = load_json(READINESS)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require(evidence["evidence_id"] == "CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-20260626", "invalid evidence id")
    require(evidence["scope"] == "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-COLLECTION-PACK-018", "invalid scope")
    require(evidence["status"] == "real_input_collection_pack_prepared_not_dispatched", "invalid status")
    require(evidence["operation_mode"] == "development_state", "operation mode must be development_state")
    require(evidence["runtime_mode"] is False, "runtime mode must be false")
    require(readiness["status"] == "real_input_readiness_blocked", "readiness source must remain blocked")

    readiness_gate = run(["python3", "tools/kds-sync/validate_codegraph_dev_execution_real_input_readiness.py"])
    require(readiness_gate.returncode == 0, f"real input readiness gate failed: {readiness_gate.stdout}{readiness_gate.stderr}")

    status = evidence["collection_status"]
    require(status["prepared"] is True, "collection pack must be prepared")
    require(status["dispatched"] is False, "collection pack must not be dispatched")
    require(status["external_notifications_sent"] == 0, "external notifications must be zero")
    require(status["external_api_write"] is False, "external API write must be false")
    require(status["real_kds_write"] is False, "real KDS write must be false")
    require(status["real_waes_write"] is False, "real WAES write must be false")

    request = evidence["primary_owner_request"]
    require(request["owner"] == "GPC_or_Liaoning_Yuanhang_order_owner", "invalid owner")
    require(request["object_family"] == "CustomerRequirementOrPlatformOrder", "invalid object family")
    require("*.customer-requirement-platform-order.source-record.json" in request["target_path"], "target path must identify source-record JSON")
    for phrase in ["customer order original", "platform order receipt", "purchase order", "equivalent formal customer confirmation"]:
        require(phrase in request["accepted_inputs"], f"missing accepted input: {phrase}")
    for phrase in ["KDS candidate only", "user oral statement", "synthetic/dev-only fixture", "unverified accepted/integrated claim"]:
        require(phrase in request["rejected_substitutes"], f"missing rejected substitute: {phrase}")

    twelve = evidence["twelve_stage_real_input_request"]
    require(twelve["runtime_object_family_count"] == 12, "runtime object family count must be 12")
    for phrase in ["WAES confirmation", "KDS write receipt", "POD", "quality inspection record"]:
        require(phrase in twelve["required_inputs"], f"missing required input: {phrase}")
    for key, value in twelve["current_ready_counts"].items():
        require(value == 0, f"{key} must remain zero")

    codegraph = evidence["codegraph_usage_when_input_arrives"]
    require(codegraph["rerun_task_intake_gate"] is True, "task intake must be rerun")
    require(codegraph["rerun_affected"] is True, "affected must be rerun")
    require(codegraph["fallback_tests_required_if_affected_tests_empty"] is True, "fallback tests must be required")

    decision = evidence["decision"]
    require(decision["collection_pack"] == "prepared", "collection pack decision mismatch")
    require(decision["dispatch"] == "not_authorized", "dispatch must be not_authorized")
    require(decision["real_business_execution"] == "blocked_until_real_source_input_arrives", "real business execution must be blocked")
    require(decision["runtime_state"] == "not_verified", "runtime state must not be verified")
    require(decision["status_ceiling"] == "partial", "status ceiling must be partial")

    for key, value in evidence["status_boundaries"].items():
        require(value is False, f"{key} must stay false")

    for phrase in [
        "real_input_collection_pack_prepared_not_dispatched",
        "GPC_or_Liaoning_Yuanhang_order_owner",
        "CustomerRequirementOrPlatformOrder",
        "platform order receipt",
        "synthetic/dev-only fixture",
        "not_authorized",
        "GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-AUTHORIZATION-019",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")

    for phrase in ["run", "stop", "verify", "recover", "debug", "collection_pack_prepared_not_dispatched"]:
        require(phrase in loop_round, f"loop round missing phrase: {phrase}")

    git_status = run(["git", "status", "--short", "--", ".codegraph"])
    require(git_status.returncode == 0, f"git status .codegraph failed: {git_status.stderr}")
    require(git_status.stdout.strip() == "", ".codegraph must remain git-isolated")

    print(
        "codegraph_dev_execution_real_input_collection_pack=pass "
        "status=prepared_not_dispatched "
        "owner=GPC_or_Liaoning_Yuanhang_order_owner "
        "object_family=CustomerRequirementOrPlatformOrder "
        "dispatch=not_authorized "
        "real_business_execution=blocked_until_real_source_input_arrives "
        "next=GPCF-CODEGRAPH-DEV-EXECUTION-REAL-INPUT-DISPATCH-AUTHORIZATION-019"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
