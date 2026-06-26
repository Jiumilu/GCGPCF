#!/usr/bin/env python3
"""Validate D182 GCKF P0 repair owner response requirement precheck."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/api/gckf-p0-repair-owner-response-requirement-precheck-current-state-d182-20260626.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-requirement-precheck-current-state-d182-20260626.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gckf-p0-repair-owner-response-requirement-precheck-current-state-d182-20260626.md"
LOOP_MD = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D182-001.md"


def fail(message: str) -> None:
    print(f"gckf_p0_repair_owner_response_requirement_precheck_current_state_d182=fail reason={message}")
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        fail(f"command_failed:{' '.join(args)}:{result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    source_evidence = load_json(ROOT / fixture["sourceEvidence"])
    require(source_evidence.get("current_acknowledgement_receipt_aggregation_preview_status") == "candidate_preview_with_hold", "source_status_mismatch")
    require(source_evidence.get("execution_mode") == "local_evidence_no_write", "source_execution_mode_mismatch")
    require(source_evidence.get("gateAssertions", {}).get("p1AdmissionAllowed") is False, "source_p1_boundary_not_false")

    precheck = fixture.get("responseRequirementPrecheck", {})
    require(fixture.get("executionMode") == "local_evidence_no_write", "execution_mode_mismatch")
    require(fixture.get("precheckStatus") == "repair_owner_response_requirement_precheck_with_hold", "precheck_status_mismatch")
    require(fixture.get("maximumState") == "review_ready_with_hold", "maximum_state_mismatch")
    require(fixture.get("holdRequired") is True, "hold_required_not_true")
    require(fixture.get("actualRepairOwnerResponseReceived") is False, "actual_response_boundary_not_false")
    require(precheck.get("precheckStatus") == "candidate_precheck_with_hold", "nested_precheck_status_mismatch")

    expected_counts = {
        "requiredRoles": 8,
        "requirementItems": 10,
        "blockingConditions": 5,
        "forbiddenActions": 11,
    }
    for key, expected in expected_counts.items():
        require(len(precheck.get(key, [])) == expected, f"fixture_count_mismatch:{key}")
        require(evidence.get("packageScope", {}).get(key) == expected, f"evidence_count_mismatch:{key}")

    for key in (
        "repairOwnerNotificationSendAllowed",
        "acknowledgementReceiptExecutionAllowed",
        "committeeCaseOpeningAllowed",
        "formalHarnessWriteAllowed",
        "lifecyclePromotionAllowed",
        "runtimeWritebackAllowed",
        "p1AdmissionAllowed",
        "v1UpgradeRecommended",
    ):
        require(fixture.get("gateAssertions", {}).get(key) is False, f"fixture_gate_not_false:{key}")
        require(evidence.get("gateAssertions", {}).get(key) is False, f"evidence_gate_not_false:{key}")

    evidence_md = EVIDENCE_MD.read_text(encoding="utf-8")
    loop_md = LOOP_MD.read_text(encoding="utf-8")
    require("repair_owner_response_requirement_precheck_with_hold" in evidence_md, "evidence_md_missing_status")
    require("actualRepairOwnerResponseReceived=false" in evidence_md, "evidence_md_missing_response_boundary")
    for marker in ("## LOOP 运行控制闭环", "### run", "### stop", "### verify", "### recover", "### debug"):
        require(marker in loop_md, f"loop_control_marker_missing:{marker}")
    require("hold_required" in loop_md, "loop_md_missing_hold_required")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_not_pass")
    require(localization.get("findings") == 0, "localization_findings_not_zero")
    require(run_command("python3", "tools/kds-sync/check_document_pollution.py") == "document_pollution=pass", "document_pollution_not_pass")
    require(run_command("python3", "tools/kds-sync/validate_kds_token.py").startswith("kds_token=pass"), "kds_token_not_pass")
    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_not_pass")

    print("gckf_p0_repair_owner_response_requirement_precheck_current_state_d182=pass")
    print(f"precheck_status={fixture.get('precheckStatus')}")
    print(f"maximum_state={fixture.get('maximumState')}")
    print(f"required_roles={len(precheck.get('requiredRoles', []))}")
    print(f"requirement_items={len(precheck.get('requirementItems', []))}")
    print(f"hold_required={fixture.get('holdRequired')}")
    print(f"execution_mode={fixture.get('executionMode')}")


if __name__ == "__main__":
    main()
