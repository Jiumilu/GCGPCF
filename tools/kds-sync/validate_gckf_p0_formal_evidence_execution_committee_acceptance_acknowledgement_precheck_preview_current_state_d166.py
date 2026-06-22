#!/usr/bin/env python3
"""Validate D166 GCKF P0 committee acceptance acknowledgement precheck preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-precheck-preview-current-state-d166-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-precheck-preview-current-state-d166-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-precheck-preview-current-state-d166-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D166-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_precheck_preview_current_state_d166="
        f"fail reason={message}"
    )
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalCommitteeAcceptanceAcknowledgementPrecheckPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentRoutingPackageIntakeGuardPreview"])
    precheck = fixture["committeeAcceptanceAcknowledgementPrecheckPreview"]
    historical_precheck = historical["committeeAcceptanceAcknowledgementPrecheckPreview"]
    source_guard = current_source["routingPackageIntakeGuardPreview"]

    require(
        fixture.get("committeeAcceptanceAcknowledgementPrecheckPreviewStatus")
        == expected["committeeAcceptanceAcknowledgementPrecheckPreviewStatus"],
        "precheck_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalCommitteeAcceptanceAcknowledgement")
        is expected["notFinalCommitteeAcceptanceAcknowledgement"],
        "not_final_committee_acceptance_mismatch",
    )
    require(precheck.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(precheck.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "committeeAcceptancePrecheckExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "intakeGuardExecutionStatus",
        "routingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus"
    ):
        require(precheck.get(key) == expected[key], f"{key}_mismatch")
    require(precheck.get("executionMode") == expected["executionMode"], "precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("committeeAcceptanceAcknowledgementPrecheckPreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_precheck.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_precheck.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("routingPackageIntakeGuardPreviewStatus")
        == expected["sourceRoutingPackageIntakeGuardPreviewStatus"],
        "source_intake_guard_status_mismatch",
    )
    for source_key, expected_key in (
        ("intakeGuardExecutionStatus", "sourceIntakeGuardExecutionStatus"),
        ("routingPackageExecutionStatus", "sourceRoutingPackageExecutionStatus"),
        ("reviewerAcceptanceAcknowledgementExecutionStatus", "sourceReviewerAcceptanceAcknowledgementExecutionStatus"),
        ("reviewerAcceptancePrecheckExecutionStatus", "sourceReviewerAcceptancePrecheckExecutionStatus"),
        ("reviewerAcceptanceExecutionStatus", "sourceReviewerAcceptanceExecutionStatus"),
        ("routingReceiptExecutionStatus", "sourceRoutingReceiptExecutionStatus"),
        ("assignmentAcknowledgementExecutionStatus", "sourceAssignmentAcknowledgementExecutionStatus"),
        ("reviewerNotificationExecutionStatus", "sourceReviewerNotificationExecutionStatus"),
        ("reviewerAssignmentExecutionStatus", "sourceReviewerAssignmentExecutionStatus"),
        ("routingExecutionStatus", "sourceRoutingExecutionStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus")
    ):
        require(source_guard.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_guard.get("dryRunOnly") is True, "source_guard_not_dry_run_only")
    require(
        precheck.get("sourceRoutingPackageIntakeGuardPreviewId") == source_guard.get("id"),
        "source_routing_package_intake_guard_preview_id_mismatch",
    )
    require(
        fixture.get("coveredRoutingPackageIntakeGuardPreviewStatus")
        == expected["coveredRoutingPackageIntakeGuardPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredRoutingPackageIntakeGuardPreviewStatus"] == source_guard.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(precheck.get("precheckRoles", []))
    sections = set(precheck.get("precheckSections", []))
    envelope_fields = set(precheck.get("candidateAcknowledgementEnvelopeFields", []))
    prerequisites = set(precheck.get("precheckReadinessPrerequisites", []))
    constraints = set(precheck.get("precheckDecisionConstraints", []))
    checks = set(precheck.get("precheckChecks", []))
    refs = set(precheck.get("requiredPrecheckRefs", []))
    blocking_conditions = set(precheck.get("blockingConditions", []))
    forbidden_actions = set(precheck.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["precheckRoleCount"], "precheck_role_count_mismatch")
    require(len(sections) == expected["precheckSectionCount"], "precheck_section_count_mismatch")
    require(len(envelope_fields) == expected["candidateAcknowledgementEnvelopeFieldCount"], "candidate_acknowledgement_envelope_field_count_mismatch")
    require(len(prerequisites) == expected["precheckReadinessPrerequisiteCount"], "precheck_prerequisite_count_mismatch")
    require(len(constraints) == expected["precheckDecisionConstraintCount"], "precheck_constraint_count_mismatch")
    require(len(checks) == expected["precheckCheckCount"], "precheck_check_count_mismatch")
    require(len(refs) == expected["requiredPrecheckRefCount"], "required_precheck_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "committee_secretariat",
            "committee_representative",
            "waes_gate_owner",
            "acl_owner",
            "harness_reviewer"
        },
        "precheck_role",
    )
    require_all(
        sections,
        {
            "candidate_committee_roster_visibility_check",
            "candidate_acl_boundary_check",
            "candidate_quorum_precheck",
            "candidate_conflict_of_interest_check",
            "candidate_acceptance_blocker_codes",
            "candidate_acceptance_hold_conditions",
            "candidate_acceptance_hold_context_refs",
            "candidate_committee_acknowledgement_pathways",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "precheck_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "committee_acceptance_acknowledgement_precheck_not_formal_acceptance",
            "no_committee_acceptance_precheck_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_intake_guard_execution",
            "no_routing_package_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write"
        },
        "precheck_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_committee_acceptance_precheck",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
            "open_committee_case",
            "execute_intake_guard",
            "execute_routing_package",
            "write_harness_evidence",
            "write_kds",
            "write_business_system"
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(evidence.get("current_committee_acceptance_acknowledgement_precheck_preview_status") == expected["committeeAcceptanceAcknowledgementPrecheckPreviewStatus"], "evidence_current_status_mismatch")
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(package_scope.get("precheck_roles") == expected["precheckRoleCount"], "evidence_role_count_mismatch")
    require(package_scope.get("precheck_checks") == expected["precheckCheckCount"], "evidence_check_count_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_precheck_preview_current_state_d166=pass")
    print("committee_acceptance_acknowledgement_precheck_preview_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("committee_acceptance_precheck_execution_status=not_executed")
    print("committee_acceptance_execution_status=not_executed")
    print("committee_acknowledgement_execution_status=not_executed")
    print("intake_guard_execution_status=not_executed")
    print("routing_package_execution_status=not_executed")
    print("reviewer_acceptance_acknowledgement_execution_status=not_executed")
    print("reviewer_acceptance_precheck_execution_status=not_executed")
    print("reviewer_acceptance_execution_status=not_executed")
    print("routing_receipt_execution_status=not_executed")
    print("assignment_acknowledgement_execution_status=not_executed")
    print("committee_case_execution_status=not_executed")
    print("committee_decision_execution_status=not_executed")
    print(f"precheck_roles={len(roles)}")
    print(f"precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
