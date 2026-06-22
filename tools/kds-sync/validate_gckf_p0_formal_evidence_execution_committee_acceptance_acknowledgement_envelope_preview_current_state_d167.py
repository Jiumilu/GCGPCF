#!/usr/bin/env python3
"""Validate D167 GCKF P0 committee acceptance acknowledgement envelope preview current-state evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-current-state-d167-20260622.json"
EVIDENCE_JSON = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-current-state-d167-20260622.json"
EVIDENCE_MD = ROOT / "docs" / "harness" / "evidence" / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-current-state-d167-20260622.md"
LOOP_MD = ROOT / "docs" / "harness" / "loops" / "loop-round-GPCF-GCKF-P0-D167-001.md"


def fail(message: str) -> None:
    print(
        "gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_envelope_preview_current_state_d167="
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


def main() -> None:
    fixture = load_json(FIXTURE)
    evidence = load_json(EVIDENCE_JSON)
    require(EVIDENCE_MD.exists(), "missing_evidence_md")
    require(LOOP_MD.exists(), "missing_loop_md")

    expected = fixture["expectedSummary"]
    historical = load_json(ROOT / fixture["sourceHistoricalCommitteeAcceptanceAcknowledgementEnvelopePreview"])
    current_source = load_json(ROOT / fixture["sourceCurrentCommitteeAcceptanceAcknowledgementPrecheckPreview"])
    envelope = fixture["committeeAcceptanceAcknowledgementEnvelopePreview"]
    historical_envelope = historical["committeeAcceptanceAcknowledgementEnvelopePreview"]
    source_precheck = current_source["committeeAcceptanceAcknowledgementPrecheckPreview"]

    require(
        fixture.get("committeeAcceptanceAcknowledgementEnvelopePreviewStatus")
        == expected["committeeAcceptanceAcknowledgementEnvelopePreviewStatus"],
        "envelope_status_mismatch",
    )
    require(fixture.get("maximumState") == expected["maximumState"], "maximum_state_mismatch")
    require(fixture.get("executionMode") == expected["executionMode"], "execution_mode_mismatch")
    require(
        fixture.get("notFinalCommitteeAcceptanceAcknowledgementEnvelope")
        is expected["notFinalCommitteeAcceptanceAcknowledgementEnvelope"],
        "not_final_envelope_mismatch",
    )
    require(envelope.get("previewType") == expected["previewType"], "preview_type_mismatch")
    require(envelope.get("previewStatus") == expected["previewStatus"], "preview_status_mismatch")

    for key in (
        "executionStatus",
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
        require(envelope.get(key) == expected[key], f"{key}_mismatch")
    require(envelope.get("executionMode") == expected["executionMode"], "envelope_execution_mode_mismatch")
    require(envelope.get("dryRunOnly") is expected["dryRunOnly"], "dry_run_only_mismatch")

    require(
        historical.get("committeeAcceptanceAcknowledgementEnvelopePreviewStatus") == "candidate_preview",
        "historical_status_mismatch",
    )
    require(historical_envelope.get("previewStatus") == "candidate_preview", "historical_preview_status_mismatch")
    require(historical_envelope.get("executionStatus") == "not_executed", "historical_execution_status_mismatch")

    require(
        current_source.get("committeeAcceptanceAcknowledgementPrecheckPreviewStatus")
        == expected["sourceCommitteeAcceptanceAcknowledgementPrecheckPreviewStatus"],
        "source_precheck_status_mismatch",
    )
    require(
        envelope.get("sourceCommitteeAcceptanceAcknowledgementPrecheckPreviewId") == source_precheck.get("id"),
        "source_precheck_id_mismatch",
    )
    require(
        fixture.get("coveredCommitteeAcceptanceAcknowledgementPrecheckPreviewStatus")
        == source_precheck.get("previewStatus"),
        "covered_status_mismatch",
    )

    for source_key, expected_key in (
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
        ("routingExecutionStatus", "sourceRoutingExecutionStatus"),
        ("committeeReentryExecutionStatus", "sourceCommitteeReentryExecutionStatus"),
        ("committeeCaseExecutionStatus", "sourceCommitteeCaseExecutionStatus"),
        ("committeeDecisionExecutionStatus", "sourceCommitteeDecisionExecutionStatus"),
        ("confirmationExecutionStatus", "sourceConfirmationExecutionStatus"),
        ("unfreezeExecutionStatus", "sourceUnfreezeExecutionStatus"),
    ):
        require(source_precheck.get(source_key) == expected[expected_key], f"{source_key}_source_mismatch")
    require(source_precheck.get("dryRunOnly") is True, "source_precheck_not_dry_run_only")

    roles = set(envelope.get("envelopeRoles", []))
    sections = set(envelope.get("envelopeSections", []))
    fields = set(envelope.get("candidateEnvelopeFields", []))
    prerequisites = set(envelope.get("envelopeReadinessPrerequisites", []))
    constraints = set(envelope.get("envelopeDecisionConstraints", []))
    checks = set(envelope.get("envelopeChecks", []))
    refs = set(envelope.get("requiredEnvelopeRefs", []))
    blocks = set(envelope.get("blockingConditions", []))
    actions = set(envelope.get("forbiddenActions", []))
    outputs = set(fixture.get("forbiddenOutputs", []))
    hold_refs = fixture.get("holdContextRefs", [])

    require(len(roles) == expected["envelopeRoleCount"], "envelope_role_count_mismatch")
    require(len(sections) == expected["envelopeSectionCount"], "envelope_section_count_mismatch")
    require(len(fields) == expected["candidateEnvelopeFieldCount"], "candidate_envelope_field_count_mismatch")
    require(len(prerequisites) == expected["envelopeReadinessPrerequisiteCount"], "envelope_prerequisite_count_mismatch")
    require(len(constraints) == expected["envelopeDecisionConstraintCount"], "envelope_constraint_count_mismatch")
    require(len(checks) == expected["envelopeCheckCount"], "envelope_check_count_mismatch")
    require(len(refs) == expected["requiredEnvelopeRefCount"], "required_envelope_ref_count_mismatch")
    require(len(blocks) == expected["blockingConditionCount"], "blocking_condition_count_mismatch")
    require(len(actions) == expected["forbiddenActionCount"], "forbidden_action_count_mismatch")
    require(len(outputs) == expected["forbiddenOutputCount"], "forbidden_output_count_mismatch")
    require(len(set(fixture.get("requiredSourceRefs", []))) == expected["requiredSourceRefCount"], "required_source_ref_count_mismatch")
    require(len(hold_refs) == expected["holdContextRefCount"], "hold_context_ref_count_mismatch")
    require(hold_refs == ["B1", "B2", "B3", "B4", "B5", "B6"], "hold_context_refs_mismatch")

    require_all(
        roles,
        {
            "committee_secretariat",
            "committee_representative",
            "waes_gate_owner",
            "harness_reviewer",
            "acl_owner",
            "evidence_controller",
        },
        "envelope_role",
    )
    require_all(
        sections,
        {
            "candidate_envelope_header",
            "candidate_committee_roster_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_quorum_snapshot",
            "candidate_conflict_of_interest_snapshot",
            "candidate_blocker_and_hold_snapshot",
            "candidate_hold_context_refs_snapshot",
            "candidate_acknowledgement_pathways_snapshot",
            "envelope_integrity_check",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "envelope_section",
    )
    require_all(
        constraints,
        {
            "candidate_preview_only",
            "envelope_preview_not_formal_acknowledgement",
            "no_envelope_assembly_execution",
            "no_committee_acceptance_precheck_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_intake_guard_execution",
            "no_routing_package_execution",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "envelope_constraint",
    )
    require_all(
        actions,
        {
            "execute_envelope_assembly",
            "execute_committee_acceptance_precheck",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
            "execute_intake_guard",
            "execute_routing_package",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
            "grant_p1_admission",
            "approve_v1_upgrade",
        },
        "forbidden_action",
    )

    for relative_path in fixture.get("requiredSourceRefs", []):
        require((ROOT / relative_path).exists(), f"missing_required_source_file:{relative_path}")

    require(
        evidence.get("current_committee_acceptance_acknowledgement_envelope_preview_status")
        == expected["committeeAcceptanceAcknowledgementEnvelopePreviewStatus"],
        "evidence_current_status_mismatch",
    )
    require(evidence.get("maximum_state") == expected["maximumState"], "evidence_maximum_state_mismatch")
    scope = evidence.get("package_scope", {})
    require(scope.get("envelope_roles") == expected["envelopeRoleCount"], "evidence_role_count_mismatch")
    require(scope.get("envelope_checks") == expected["envelopeCheckCount"], "evidence_check_count_mismatch")
    require(scope.get("hold_context_refs") == expected["holdContextRefCount"], "evidence_hold_ref_count_mismatch")
    for key in fixture["currentGateAssertions"]:
        require(evidence.get("gateAssertions", {}).get(key) is False, f"gate_assertion_not_false:{key}")

    require("candidate_preview_with_hold" in EVIDENCE_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_md")
    require("candidate_preview_with_hold" in LOOP_MD.read_text(encoding="utf-8"), "missing_candidate_preview_with_hold_in_loop")

    localization = json.loads(run_command("python3", "tools/kds-sync/check_chinese_localization_gate.py", "--json", "--max-findings", "10000"))
    require(localization.get("localization_gate") == "pass", "localization_gate_failed")
    loop_gate = json.loads(run_command("python3", "tools/kds-sync/loop_document_gate.py", "--check-only"))
    require(loop_gate.get("gate") == "pass", "loop_document_gate_failed")

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_envelope_preview_current_state_d167=pass")
    print("committee_acceptance_acknowledgement_envelope_preview_status=candidate_preview_with_hold")
    print("maximum_state=review_ready_with_hold")
    print("preview_status=candidate_preview_with_hold")
    print("execution_status=not_executed")
    print("envelope_assembly_execution_status=not_executed")
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
    print(f"envelope_roles={len(roles)}")
    print(f"envelope_checks={len(checks)}")
    print(f"hold_context_refs={len(hold_refs)}")
    print("localization_gate=pass")
    print("loop_document_gate=pass")
    print("execution_mode=local_evidence_no_write")


if __name__ == "__main__":
    main()
