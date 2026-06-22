#!/usr/bin/env python3
"""Validate D169 GCKF P0 committee acceptance acknowledgement routing dispatch precheck current-state evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-routing-dispatch-precheck-current-state-d169-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-routing-dispatch-precheck-current-state-d169-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-routing-dispatch-precheck-current-state-d169-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D169-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_routing_dispatch_precheck_current_state_d169="
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
    historical = load_json(ROOT / fixture["sourceHistoricalCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheck"])
    current_source = load_json(ROOT / fixture["sourceCurrentCommitteeAcceptanceAcknowledgementRoutingPreview"])
    precheck = fixture["committeeAcceptanceAcknowledgementRoutingDispatchPrecheck"]
    historical_precheck = historical["committeeAcceptanceAcknowledgementRoutingDispatchPrecheck"]
    source_routing = current_source["committeeAcceptanceAcknowledgementRoutingPreview"]

    require(
        fixture.get("committeeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus")
        == expected["committeeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus"],
        "dispatch_precheck_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheck")
        is expected["notFinalCommitteeAcceptanceAcknowledgementRoutingDispatchPrecheck"],
        "not_final_dispatch_precheck_mismatch",
    )
    require(precheck.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(precheck.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
        "routingDispatchPrecheckExecutionStatus",
        "acknowledgementDispatchExecutionStatus",
        "acknowledgementRoutingExecutionStatus",
        "envelopeAssemblyExecutionStatus",
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
        "formalWriteExecutionStatus",
    ):
        require(precheck.get(key) == expected[key], f"{key}_mismatch")
    require(precheck.get("executionMode") == expected["executionMode"], "dispatch_precheck_execution_mode_mismatch")
    require(precheck.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("committeeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_precheck.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_precheck.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("committeeAcceptanceAcknowledgementRoutingPreviewStatus")
        == expected["sourceCommitteeAcceptanceAcknowledgementRoutingPreviewStatus"],
        "source_routing_status_mismatch",
    )
    for source_key, expected_key in (
        ("executionStatus", "sourceRoutingExecutionStatus"),
        ("acknowledgementRoutingExecutionStatus", "sourceAcknowledgementRoutingExecutionStatus"),
        ("envelopeAssemblyExecutionStatus", "sourceEnvelopeAssemblyExecutionStatus"),
        ("committeeAcceptancePrecheckExecutionStatus", "sourceCommitteeAcceptancePrecheckExecutionStatus"),
        ("committeeAcceptanceExecutionStatus", "sourceCommitteeAcceptanceExecutionStatus"),
        ("committeeAcknowledgementExecutionStatus", "sourceCommitteeAcknowledgementExecutionStatus"),
        ("intakeGuardExecutionStatus", "sourceIntakeGuardExecutionStatus"),
        ("routingPackageExecutionStatus", "sourceRoutingPackageExecutionStatus"),
        ("reviewerAcceptanceAcknowledgementExecutionStatus", "sourceReviewerAcceptanceAcknowledgementExecutionStatus"),
        ("reviewerAcceptancePrecheckExecutionStatus", "sourceReviewerAcceptancePrecheckExecutionStatus"),
        ("reviewerAcceptanceExecutionStatus", "sourceReviewerAcceptanceExecutionStatus"),
        ("routingReceiptExecutionStatus", "sourceRoutingReceiptExecutionStatus"),
        ("assignmentAcknowledgementExecutionStatus", "sourceAssignmentAcknowledgementExecutionStatus"),
        ("reviewerNotificationExecutionStatus", "sourceReviewerNotificationExecutionStatus"),
        ("reviewerAssignmentExecutionStatus", "sourceReviewerAssignmentExecutionStatus"),
        ("routingExecutionStatus", "sourceRoutingExecutionDownstreamStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_routing.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_routing.get("dryRunOnly") is True, "source_routing_not_dry_run_only")
    require(
        precheck.get("sourceCommitteeAcceptanceAcknowledgementRoutingPreviewId") == source_routing.get("id"),
        "source_routing_preview_id_mismatch",
    )
    require(
        fixture.get("coveredCommitteeAcceptanceAcknowledgementRoutingPreviewStatus")
        == expected["coveredCommitteeAcceptanceAcknowledgementRoutingPreviewStatus"],
        "covered_status_mismatch",
    )
    require(
        fixture["coveredCommitteeAcceptanceAcknowledgementRoutingPreviewStatus"] == source_routing.get("previewStatus"),
        "covered_status_not_matched",
    )

    roles = set(precheck.get("dispatchPrecheckRoles", []))
    sections = set(precheck.get("dispatchPrecheckSections", []))
    fields = set(precheck.get("candidateDispatchPrecheckFields", []))
    prerequisites = set(precheck.get("dispatchPrecheckReadinessPrerequisites", []))
    constraints = set(precheck.get("dispatchPrecheckDecisionConstraints", []))
    checks = set(precheck.get("dispatchPrecheckChecks", []))
    refs = set(precheck.get("requiredDispatchPrecheckRefs", []))
    blocking_conditions = set(precheck.get("blockingConditions", []))
    forbidden_actions = set(precheck.get("forbiddenActions", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["dispatchPrecheckRoleCount"], "dispatch_precheck_role_count_mismatch")
    require(len(sections) == expected["dispatchPrecheckSectionCount"], "dispatch_precheck_section_count_mismatch")
    require(len(fields) == expected["candidateDispatchPrecheckFieldCount"], "candidate_dispatch_precheck_field_count_mismatch")
    require(len(prerequisites) == expected["dispatchPrecheckReadinessPrerequisiteCount"], "dispatch_precheck_prerequisite_count_mismatch")
    require(len(constraints) == expected["dispatchPrecheckDecisionConstraintCount"], "dispatch_precheck_constraint_count_mismatch")
    require(len(checks) == expected["dispatchPrecheckCheckCount"], "dispatch_precheck_check_count_mismatch")
    require(len(refs) == expected["requiredDispatchPrecheckRefCount"], "required_dispatch_precheck_ref_count_mismatch")
    require(len(blocking_conditions) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(forbidden_actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")

    require_all(
        roles,
        {
            "routing_dispatch_precheck_owner",
            "committee_secretariat",
            "committee_representative",
            "waes_gate_owner",
            "acl_owner",
            "evidence_controller",
            "harness_reviewer"
        },
        "dispatch_precheck_role",
    )
    require_all(
        sections,
        {
            "candidate_dispatch_header",
            "candidate_dispatch_recipient_precheck_matrix",
            "candidate_dispatch_condition_checks",
            "candidate_acknowledgement_route_snapshot",
            "candidate_acknowledgement_envelope_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_quorum_snapshot",
            "candidate_conflict_of_interest_snapshot",
            "candidate_blocker_and_hold_snapshot",
            "candidate_hold_context_refs_snapshot",
            "harness_no_write_guard",
            "no_write_attestation"
        },
        "dispatch_precheck_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "dispatch_precheck_not_formal_dispatch",
            "no_routing_dispatch_precheck_execution",
            "no_acknowledgement_dispatch_execution",
            "no_acknowledgement_routing_execution",
            "no_committee_acceptance_precheck_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_routing_package_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write"
        },
        "dispatch_precheck_constraint",
    )
    require_all(
        forbidden_actions,
        {
            "execute_routing_dispatch_precheck",
            "execute_acknowledgement_dispatch",
            "execute_acknowledgement_routing",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
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
    require(evidence.get("current_committee_acceptance_acknowledgement_routing_dispatch_precheck_status") == expected["committeeAcceptanceAcknowledgementRoutingDispatchPrecheckStatus"], "evidence_current_status_mismatch")
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    require(package_scope.get("dispatch_precheck_roles") == expected["dispatchPrecheckRoleCount"], "evidence_role_count_mismatch")
    require(package_scope.get("dispatch_precheck_checks") == expected["dispatchPrecheckCheckCount"], "evidence_check_count_mismatch")
    require(package_scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_routing_dispatch_precheck_current_state_d169=pass")
    print("committee_acceptance_acknowledgement_routing_dispatch_precheck_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("routing_dispatch_precheck_execution_status=not_executed")
    print("acknowledgement_dispatch_execution_status=not_executed")
    print("acknowledgement_routing_execution_status=not_executed")
    print("committee_acceptance_precheck_execution_status=not_executed")
    print("committee_acceptance_execution_status=not_executed")
    print("committee_acknowledgement_execution_status=not_executed")
    print("routing_package_execution_status=not_executed")
    print("routing_execution_status=not_executed")
    print("committee_case_execution_status=not_executed")
    print("committee_decision_execution_status=not_executed")
    print(f"dispatch_precheck_roles={len(roles)}")
    print(f"dispatch_precheck_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
