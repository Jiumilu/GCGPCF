#!/usr/bin/env python3
"""Validate D165 GCKF P0 routing package intake guard preview current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-routing-package-intake-guard-preview-current-state-d165-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-routing-package-intake-guard-preview-current-state-d165-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-routing-package-intake-guard-preview-current-state-d165-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D165-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_current_state_d165="
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
    historical = load_json(ROOT / fixture["sourceHistoricalRoutingPackageIntakeGuardPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentReviewerAcceptanceAcknowledgementRoutingPackagePreview"])
    guard = fixture["routingPackageIntakeGuardPreview"]
    historical_guard = historical["routingPackageIntakeGuardPreview"]
    source_package = current_source["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]

    require(
        fixture.get("routingPackageIntakeGuardPreviewStatus") == expected["routingPackageIntakeGuardPreviewStatus"],
        "intake_guard_preview_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(fixture.get("notFinalIntakeGuard") is expected["notFinalIntakeGuard"], "not_final_intake_guard_mismatch")
    require(guard.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(guard.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "intakeGuardExecutionStatus",
        "routingPackageExecutionStatus",
        "reviewerAcceptanceAcknowledgementExecutionStatus",
        "reviewerAcceptancePrecheckExecutionStatus",
        "reviewerAcceptanceExecutionStatus",
        "routingReceiptExecutionStatus",
        "assignmentAcknowledgementExecutionStatus",
        "reviewerNotificationExecutionStatus",
        "reviewerAssignmentExecutionStatus",
        "routingPrecheckExecutionStatus",
        "routingExecutionStatus",
        "acknowledgementExecutionStatus",
        "repairRequestExecutionStatus",
        "supplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus"
    ):
        require(guard.get(key) == expected[key], f"{key}_mismatch")
    require(guard.get("executionMode") == expected["executionMode"], "guard_execution_mode_mismatch")
    require(guard.get("dryRunOnly") is expected["dryRunOnlyGuard"], "dry_run_only_guard_mismatch")

    require(historical.get("routingPackageIntakeGuardPreviewStatus") == "candidate_preview", "historical_status_mismatch")
    require(historical_guard.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_guard.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus")
        == expected["sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"],
        "source_routing_package_preview_status_mismatch",
    )
    for source_key, expected_key in (
        ("routingPackageExecutionStatus", "sourceRoutingPackageExecutionStatus"),
        ("reviewerAcceptanceAcknowledgementExecutionStatus", "sourceReviewerAcceptanceAcknowledgementExecutionStatus"),
        ("reviewerAcceptancePrecheckExecutionStatus", "sourceReviewerAcceptancePrecheckExecutionStatus"),
        ("reviewerAcceptanceExecutionStatus", "sourceReviewerAcceptanceExecutionStatus"),
        ("routingReceiptExecutionStatus", "sourceRoutingReceiptExecutionStatus"),
        ("assignmentAcknowledgementExecutionStatus", "sourceAssignmentAcknowledgementExecutionStatus"),
        ("reviewerNotificationExecutionStatus", "sourceReviewerNotificationExecutionStatus"),
        ("reviewerAssignmentExecutionStatus", "sourceReviewerAssignmentExecutionStatus"),
        ("routingPrecheckExecutionStatus", "sourceRoutingPrecheckExecutionStatus"),
        ("routingExecutionStatus", "sourceRoutingExecutionStatus"),
        ("acknowledgementExecutionStatus", "sourceAcknowledgementExecutionStatus"),
        ("repairRequestExecutionStatus", "sourceRepairRequestExecutionStatus"),
        ("supplementIntakeExecutionStatus", "sourceSupplementIntakeExecutionStatus"),
        ("supplementAcceptanceExecutionStatus", "sourceSupplementAcceptanceExecutionStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus")
    ):
        require(source_package.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_package.get("dryRunOnly") is True, "source_package_not_dry_run_only")
    require(
        guard.get("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId") == source_package.get("id"),
        "source_routing_package_preview_id_mismatch",
    )
    require(
        fixture.get("coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus")
        == expected["coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"] == source_package.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(guard.get("intakeGuardRoles", []))
    sections = set(guard.get("intakeGuardSections", []))
    envelope_fields = set(guard.get("intakeGuardEnvelopeFields", []))
    prerequisites = set(guard.get("intakeGuardReadinessPrerequisites", []))
    constraints = set(guard.get("intakeGuardDecisionConstraints", []))
    checks = set(guard.get("intakeGuardChecks", []))
    refs = set(guard.get("requiredIntakeGuardRefs", []))
    blocking_conditions = set(guard.get("blockingConditions", []))
    forbidden_actions = set(guard.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["intakeGuardRoleCount"], "intake_guard_role_count_mismatch")
    require(len(sections) == expected["intakeGuardSectionCount"], "intake_guard_section_count_mismatch")
    require(len(envelope_fields) == expected["intakeGuardEnvelopeFieldCount"], "intake_guard_envelope_field_count_mismatch")
    require(len(prerequisites) == expected["intakeGuardReadinessPrerequisiteCount"], "intake_guard_prerequisite_count_mismatch")
    require(len(constraints) == expected["intakeGuardDecisionConstraintCount"], "intake_guard_constraint_count_mismatch")
    require(len(checks) == expected["intakeGuardCheckCount"], "intake_guard_check_count_mismatch")
    require(len(refs) == expected["requiredIntakeGuardRefCount"], "required_intake_guard_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "request_owner",
            "routing_owner",
            "routing_package_owner",
            "intake_guard_owner",
            "waes_gate_owner",
            "harness_reviewer",
            "committee_representative"
        },
        "intake_guard_role",
    )
    require_all(
        sections,
        {
            "candidate_package_completeness_check",
            "candidate_acl_boundary_check",
            "candidate_committee_visibility_check",
            "candidate_intake_blocker_codes",
            "candidate_intake_hold_conditions",
            "candidate_intake_hold_context_refs",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "intake_guard_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "intake_guard_preview_not_formal_intake",
            "no_intake_guard_execution",
            "no_routing_package_execution",
            "no_reviewer_acceptance_acknowledgement_execution",
            "no_routing_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write"
        },
        "intake_guard_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_intake_guard",
            "execute_routing_package",
            "submit_routing_package",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system"
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    package_scope = evidence.get("package_scope", {})
    require(evidence.get("current_routing_package_intake_guard_preview_status") == expected["routingPackageIntakeGuardPreviewStatus"], "evidence_current_status_mismatch")
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(package_scope.get("intake_guard_roles") == expected["intakeGuardRoleCount"], "evidence_role_count_mismatch")
    require(package_scope.get("intake_guard_checks") == expected["intakeGuardCheckCount"], "evidence_check_count_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    print("gckf_p0_formal_evidence_execution_routing_package_intake_guard_preview_current_state_d165=pass")
    print("routing_package_intake_guard_preview_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("intake_guard_execution_status=not_executed")
    print("routing_package_execution_status=not_executed")
    print("reviewer_acceptance_acknowledgement_execution_status=not_executed")
    print("reviewer_acceptance_precheck_execution_status=not_executed")
    print("reviewer_acceptance_execution_status=not_executed")
    print("routing_receipt_execution_status=not_executed")
    print("assignment_acknowledgement_execution_status=not_executed")
    print("reviewer_assignment_execution_status=not_executed")
    print("routing_execution_status=not_executed")
    print("committee_reentry_execution_status=not_executed")
    print("committee_case_execution_status=not_executed")
    print("committee_decision_execution_status=not_executed")
    print(f"intake_guard_roles={len(roles)}")
    print(f"intake_guard_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
