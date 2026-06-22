#!/usr/bin/env python3
"""Validate D165 GCKF P0 routing package acknowledgement preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-routing-package-acknowledgement-preview-current-state-d165-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-routing-package-acknowledgement-preview-current-state-d165-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence" / "gckf-p0-formal-evidence-execution-routing-package-acknowledgement-preview-current-state-d165-20260622.md"
LOOP_MD = ROOT / "docs/harness/loops" / "loop-round-GPCF-GCKF-P0-D165-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_routing_package_acknowledgement_preview_current_state_d165="
        f"fail reason={message}"
    )
    sys.exit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing_file:{path.relative_to(ROOT)}")
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        fail(f"command_failed:{' '.join(args)}:{stderr}")
    return result.stdout.strip()


def require_all(actual: set[str], expected_values: set[str], label: str) -> None:
    for value in expected_values:
        require(value in actual, f"missing_{label}:{value}")


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalRoutingPackageAcknowledgementPreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentReviewerAcceptanceAcknowledgementRoutingPackagePreview"])
    acknowledgement = fixture["routingPackageAcknowledgementPreview"]
    historical_ack = historical["routingPackageAcknowledgementPreview"]
    source_package = current_source["reviewerAcceptanceAcknowledgementRoutingPackagePreview"]

    require(
      fixture.get("routingPackageAcknowledgementPreviewStatus") == expected["routingPackageAcknowledgementPreviewStatus"],
      "routing_package_acknowledgement_preview_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalRoutingPackageAcknowledgement") is expected["notFinalRoutingPackageAcknowledgement"],
        "not_final_routing_package_acknowledgement_mismatch",
    )

    require(acknowledgement.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(acknowledgement.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")
    for key in (
        "executionStatus",
        "routingPackageAcknowledgementExecutionStatus",
        "routingPackageExecutionStatus",
        "routingPackageSubmissionStatus",
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
        "formalWriteExecutionStatus",
    ):
        require(acknowledgement.get(key) == expected[key], f"{key}_mismatch")
    require(acknowledgement.get("executionMode") == expected["executionMode"], "ack_execution_mode_mismatch")
    require(acknowledgement.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("routingPackageAcknowledgementPreviewStatus") == "candidate_preview",
        "historical_preview_status_mismatch",
    )
    require(historical_ack.get("previewStatus") == "candidate_preview", "historical_nested_preview_status_mismatch")
    require(historical_ack.get("executionMode") == "dry_run_no_write", "historical_execution_mode_mismatch")

    require(
        current_source.get("reviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus")
        == expected["sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus"],
        "source_current_preview_status_mismatch",
    )
    require(
        acknowledgement.get("sourceReviewerAcceptanceAcknowledgementRoutingPackagePreviewId") == source_package.get("id"),
        "source_preview_id_mismatch",
    )
    require(
        fixture.get("coveredReviewerAcceptanceAcknowledgementRoutingPackagePreviewStatus")
        == source_package.get("previewStatus"),
        "covered_status_mismatch",
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
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_package.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_package.get("dryRunOnly") is True, "source_package_not_dry_run_only")

    roles = set(acknowledgement.get("acknowledgementRoles", []))
    require(len(roles) == expected["acknowledgementRoleCount"], "acknowledgement_role_count_mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "routing_package_owner",
            "routing_package_acknowledgement_owner",
            "reviewer_acceptance_acknowledgement_owner",
            "reviewer_acceptance_precheck_owner",
            "reviewer_acceptance_owner",
            "routing_receipt_owner",
            "reviewer_assignment_owner",
            "routing_owner",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "governance_owner",
        },
        "acknowledgement_role",
    )

    sections = set(acknowledgement.get("acknowledgementSections", []))
    require(len(sections) == expected["acknowledgementSectionCount"], "acknowledgement_section_count_mismatch")
    require_all(
        sections,
        {
            "source_routing_package_lineage",
            "routing_package_acknowledgement_scope",
            "acknowledgement_envelope_fields",
            "acknowledgement_readiness_prerequisites",
            "candidate_acknowledgement_recipient_matrix",
            "candidate_package_to_acknowledgement_mapping",
            "candidate_acknowledgement_blocker_codes",
            "candidate_acknowledgement_hold_conditions",
            "candidate_access_boundary_snapshot",
            "authority_and_recusal_boundary",
            "freeze_retention_statement",
            "waes_negative_gate_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "acknowledgement_section",
    )

    envelope_fields = set(acknowledgement.get("acknowledgementEnvelopeFields", []))
    require(
        len(envelope_fields) == expected["acknowledgementEnvelopeFieldCount"],
        "acknowledgement_envelope_field_count_mismatch",
    )
    prerequisites = set(acknowledgement.get("acknowledgementReadinessPrerequisites", []))
    require(
        len(prerequisites) == expected["acknowledgementReadinessPrerequisiteCount"],
        "acknowledgement_readiness_prerequisite_count_mismatch",
    )
    constraints = set(acknowledgement.get("acknowledgementDecisionConstraints", []))
    require(
        len(constraints) == expected["acknowledgementDecisionConstraintCount"],
        "acknowledgement_decision_constraint_count_mismatch",
    )
    checks = set(acknowledgement.get("acknowledgementChecks", []))
    require(len(checks) == expected["acknowledgementCheckCount"], "acknowledgement_check_count_mismatch")
    refs = set(acknowledgement.get("requiredAcknowledgementRefs", []))
    require(len(refs) == expected["requiredAcknowledgementRefCount"], "required_acknowledgement_ref_count_mismatch")
    blocks = set(acknowledgement.get("blockingConditions", []))
    require(len(blocks) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    actions = set(acknowledgement.get("forbiddenActions", []))
    require(len(actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    outputs = set(fixture.get("forbiddenOutputs", []))
    require(len(outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")
    hold_refs = fixture.get("holdContextRefs", [])
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    require(hold_refs == ["B1", "B2", "B3", "B4", "B5", "B6"], "hold_context_refs_mismatch")

    require_all(
        actions,
        {
            "execute_routing_package_acknowledgement",
            "execute_routing_package",
            "submit_routing_package",
            "execute_reviewer_acceptance_acknowledgement",
            "execute_reviewer_acceptance_precheck",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )
    require_all(
        blocks,
        {
            "source_routing_package_preview_not_candidate_preview_with_hold",
            "missing_source_routing_package_preview_ref",
            "missing_hold_context_refs",
            "routing_package_acknowledgement_preview_attempts_formal_acknowledgement",
            "routing_package_acknowledgement_preview_attempts_harness_evidence_write",
        },
        "blocking_condition",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_ref:{relative_path}")
    require(
        len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"],
        "required_source_ref_count_mismatch",
    )

    require(evidence.get("routingPackageAcknowledgementPreviewStatus") == fixture["routingPackageAcknowledgementPreviewStatus"], "evidence_status_mismatch")
    require(evidence.get("maximumState") == fixture["maximumState"], "evidence_maximum_state_mismatch")
    require(evidence.get("executionStatus") == acknowledgement["executionStatus"], "evidence_execution_status_mismatch")
    require(evidence.get("holdContextRefs") == hold_refs, "evidence_hold_context_refs_mismatch")
    require(evidence.get("counts", {}).get("acknowledgementChecks") == expected["acknowledgementCheckCount"], "evidence_check_count_mismatch")
    require(evidence.get("counts", {}).get("forbiddenActions") == expected["forbiddenActionCount"], "evidence_forbidden_action_count_mismatch")
    for key in fixture["currentGateAssertions"]:
        require(evidence.get("gateAssertions", {}).get(key) is False, f"gate_assertion_not_false:{key}")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_failed")
    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_failed")

    print("gckf_p0_formal_evidence_execution_routing_package_acknowledgement_preview_current_state_d165=pass")
    print(f"routing_package_acknowledgement_preview_status={acknowledgement['previewStatus']}")
    print(f"maximum_state={fixture['maximumState']}")
    print(f"preview_status={acknowledgement['previewStatus']}")
    print(f"execution_status={acknowledgement['executionStatus']}")
    print(f"routing_package_acknowledgement_execution_status={acknowledgement['routingPackageAcknowledgementExecutionStatus']}")
    print(f"routing_package_execution_status={acknowledgement['routingPackageExecutionStatus']}")
    print(f"routing_package_submission_status={acknowledgement['routingPackageSubmissionStatus']}")
    print(f"reviewer_acceptance_acknowledgement_execution_status={acknowledgement['reviewerAcceptanceAcknowledgementExecutionStatus']}")
    print(f"reviewer_acceptance_precheck_execution_status={acknowledgement['reviewerAcceptancePrecheckExecutionStatus']}")
    print(f"reviewer_acceptance_execution_status={acknowledgement['reviewerAcceptanceExecutionStatus']}")
    print(f"routing_receipt_execution_status={acknowledgement['routingReceiptExecutionStatus']}")
    print(f"assignment_acknowledgement_execution_status={acknowledgement['assignmentAcknowledgementExecutionStatus']}")
    print(f"reviewer_assignment_execution_status={acknowledgement['reviewerAssignmentExecutionStatus']}")
    print(f"routing_precheck_execution_status={acknowledgement['routingPrecheckExecutionStatus']}")
    print(f"routing_execution_status={acknowledgement['routingExecutionStatus']}")
    print(f"acknowledgement_execution_status={acknowledgement['acknowledgementExecutionStatus']}")
    print(f"repair_request_execution_status={acknowledgement['repairRequestExecutionStatus']}")
    print(f"supplement_intake_execution_status={acknowledgement['supplementIntakeExecutionStatus']}")
    print(f"supplement_acceptance_execution_status={acknowledgement['supplementAcceptanceExecutionStatus']}")
    print(f"committee_reentry_execution_status={acknowledgement['committeeReentryExecutionStatus']}")
    print(f"committee_case_execution_status={acknowledgement['committeeCaseExecutionStatus']}")
    print(f"committee_decision_execution_status={acknowledgement['committeeDecisionExecutionStatus']}")
    print(f"acknowledgement_roles={len(roles)}")
    print(f"acknowledgement_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
