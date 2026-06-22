#!/usr/bin/env python3
"""Validate P0 repair request intake completeness precheck preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-repair-request-intake-completeness-precheck-preview-dry-run-v0.1.json"
)


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    precheck = data["repairRequestIntakeCompletenessPrecheck"]
    failures: list[str] = []

    if data.get("repairRequestIntakeCompletenessPrecheckStatus") != "candidate_preview":
        failures.append("repairRequestIntakeCompletenessPrecheckStatus must remain candidate_preview")
    if data.get("executionMode") != "dry_run_no_write":
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRepairRequestCompletenessPrecheck") is not True:
        failures.append("notFinalRepairRequestCompletenessPrecheck must be true")
    if precheck.get("dryRunOnly") is not True:
        failures.append("precheck must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "completenessPrecheckPreviewExecutionStatus",
        "completenessPrecheckExecutionStatus",
        "repairRequestCreationStatus",
        "repairIntakeExecutionStatus",
        "aggregationCompletenessPrecheckExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if precheck.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    required_sections = {
        "candidate_required_material_checklist",
        "candidate_missing_material_matrix",
        "candidate_submitter_identity_boundary",
        "waes_negative_gate_snapshot",
        "harness_no_write_guard",
        "no_write_attestation",
    }
    if not required_sections.issubset(set(precheck.get("precheckSections", []))):
        failures.append("required completeness precheck sections missing")

    required_forbidden = {
        "execute_completeness_precheck",
        "create_repair_request",
        "execute_repair_intake",
        "open_committee_case",
        "write_harness_evidence",
        "write_kds",
        "write_business_system",
    }
    if not required_forbidden.issubset(set(precheck.get("forbiddenActions", []))):
        failures.append("required forbidden actions missing")

    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    if failures:
        print("gckf_p0_formal_evidence_execution_repair_request_intake_completeness_precheck_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_repair_request_intake_completeness_precheck_preview_dry_run=pass")
    print(f"status={precheck['previewStatus']}")
    print(f"execution_mode={precheck['executionMode']}")
    print("executes_completeness_precheck_preview=0")
    print("executes_completeness_precheck=0")
    print("creates_repair_request=0")
    print("executes_repair_intake=0")
    print("opens_committee_case=0")
    print("writes_kds=0")
    print("writes_business_system=0")
    print("writes_harness_evidence=0")
    print("writes_formal_evidence=0")
    print("writes_revenue_distribution=0")
    print("writes_contribution_score=0")
    print("no_write=covered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
