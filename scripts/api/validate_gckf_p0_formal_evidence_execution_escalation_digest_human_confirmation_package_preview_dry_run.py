#!/usr/bin/env python3
"""Validate P0 escalation digest human confirmation package preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-escalation-digest-human-confirmation-package-preview-dry-run-v0.1.json"
)


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def require_all(actual: set[str], expected_values: set[str], label: str, failures: list[str]) -> None:
    for value in expected_values:
        if value not in actual:
            failures.append(f"missing {label}: {value}")


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_digest = load_json(data["sourceEscalationDigestPreview"])
    source = source_digest["escalationDigestPreview"]
    package = data["humanConfirmationPackagePreview"]

    if data.get("humanConfirmationPackagePreviewStatus") != expected["humanConfirmationPackagePreviewStatus"]:
        failures.append("humanConfirmationPackagePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("human confirmation package preview must state notFinalAcceptance=true")
    if package.get("previewType") != expected["previewType"]:
        failures.append("human confirmation package previewType mismatch")
    if package.get("previewStatus") != expected["previewStatus"]:
        failures.append("human confirmation package previewStatus must remain candidate_preview")
    for key in (
        "executionStatus",
        "confirmationExecutionStatus",
        "committeeExecutionStatus",
        "resendExecutionStatus",
        "escalationExecutionStatus",
        "approvalExecutionStatus",
        "retryExecutionStatus",
        "unfreezeExecutionStatus",
    ):
        if package.get(key) != expected[key]:
            failures.append(f"{key} must remain {expected[key]}")
    if package.get("executionMode") != expected["executionMode"]:
        failures.append("human confirmation package executionMode mismatch")
    if package.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("human confirmation package preview must remain dryRunOnly=true")

    if source_digest.get("escalationDigestPreviewStatus") != expected["sourceEscalationDigestPreviewStatus"]:
        failures.append("source escalation digest preview must remain candidate_preview")
    source_status_map = {
        "executionStatus": "sourceDigestExecutionStatus",
        "resendExecutionStatus": "sourceResendExecutionStatus",
        "escalationExecutionStatus": "sourceEscalationExecutionStatus",
        "approvalExecutionStatus": "sourceApprovalExecutionStatus",
        "retryExecutionStatus": "sourceRetryExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source escalation digest must remain dryRunOnly=true")
    if package.get("sourceEscalationDigestPreviewId") != source.get("id"):
        failures.append("sourceEscalationDigestPreviewId must match D44 escalation digest preview id")
    if data.get("coveredEscalationDigestPreviewStatus") != expected["coveredEscalationDigestPreviewStatus"]:
        failures.append("coveredEscalationDigestPreviewStatus mismatch")
    if data["coveredEscalationDigestPreviewStatus"] != source.get("previewStatus"):
        failures.append("covered escalation digest preview status must match D44 preview status")

    roles = set(package.get("reviewerRoles", []))
    if len(roles) != expected["reviewerRoleCount"]:
        failures.append("reviewerRoleCount mismatch")
    require_all(
        roles,
        {
            "request_owner",
            "repair_reviewer",
            "waes_gate_owner",
            "kwe_workflow_owner",
            "harness_reviewer",
            "committee_representative",
            "stop_authority_owner",
            "business_system_owner",
        },
        "reviewer role",
        failures,
    )
    if roles != set(source.get("digestAudienceRoles", [])):
        failures.append("reviewerRoles must mirror D44 digestAudienceRoles")

    sections = set(package.get("packageSections", []))
    if len(sections) != expected["packageSectionCount"]:
        failures.append("packageSectionCount mismatch")
    require_all(
        sections,
        {
            "source_lineage",
            "escalation_digest_summary",
            "receipt_exception_summary",
            "resend_candidate_review",
            "escalation_candidate_review",
            "human_decision_options",
            "committee_trigger_review",
            "responsibility_boundary",
            "required_evidence_refs",
            "negative_gate_result",
            "no_write_attestation",
        },
        "package section",
        failures,
    )

    decision_options = set(package.get("decisionOptions", []))
    if len(decision_options) != expected["decisionOptionCount"]:
        failures.append("decisionOptionCount mismatch")
    require_all(
        decision_options,
        {
            "approve_resend_candidate",
            "approve_escalation_candidate",
            "request_repair",
            "send_to_committee",
            "reject_candidate",
            "keep_frozen",
        },
        "decision option",
        failures,
    )

    committee_triggers = set(package.get("committeeTriggers", []))
    if len(committee_triggers) != expected["committeeTriggerCount"]:
        failures.append("committeeTriggerCount mismatch")
    require_all(
        committee_triggers,
        {
            "cross_unit_responsibility_dispute",
            "freeze_release_dispute",
            "formal_write_risk",
            "revenue_or_contribution_impact",
            "major_violation_suspected",
        },
        "committee trigger",
        failures,
    )

    checks = set(package.get("confirmationChecks", []))
    if len(checks) != expected["confirmationCheckCount"]:
        failures.append("confirmationCheckCount mismatch")
    require_all(
        checks,
        {
            "source_escalation_digest_preview_status_is_candidate_preview",
            "source_digest_execution_status_is_not_executed",
            "source_resend_execution_status_is_not_executed",
            "source_escalation_execution_status_is_not_executed",
            "source_approval_execution_status_is_not_executed",
            "source_retry_execution_status_is_not_executed",
            "source_unfreeze_execution_status_is_not_executed",
            "source_escalation_digest_is_dry_run_only",
            "human_confirmation_package_preview_status_is_candidate_preview",
            "all_reviewer_roles_covered",
            "source_lineage_section_present",
            "escalation_digest_summary_present",
            "receipt_exception_summary_present",
            "resend_candidate_review_present",
            "escalation_candidate_review_present",
            "human_decision_options_present",
            "committee_trigger_review_present",
            "responsibility_boundary_present",
            "required_evidence_refs_present",
            "negative_gate_result_present",
            "no_write_attestation_present",
            "approve_resend_candidate_option_present",
            "approve_escalation_candidate_option_present",
            "request_repair_option_present",
            "send_to_committee_option_present",
            "reject_candidate_option_present",
            "keep_frozen_option_present",
            "major_violation_trigger_present",
            "assert_confirmation_not_executed",
            "assert_no_write_boundary",
        },
        "confirmation check",
        failures,
    )

    refs = set(package.get("requiredConfirmationRefs", []))
    if len(refs) != expected["requiredConfirmationRefCount"]:
        failures.append("requiredConfirmationRefCount mismatch")
    require_all(
        refs,
        {
            "sourceEscalationDigestPreviewRef",
            "sourceSignerReceiptPreviewRef",
            "sourceApprovalPacketPreviewRef",
            "escalationDigestSummaryRef",
            "receiptExceptionSummaryRef",
            "resendCandidateReviewRef",
            "escalationCandidateReviewRef",
            "humanDecisionOptionsRef",
            "committeeTriggerReviewRef",
            "responsibilityBoundaryRef",
            "requiredEvidenceRefs",
            "requestOwnerReviewerRef",
            "repairReviewerRef",
            "waesGateOwnerReviewerRef",
            "kweWorkflowOwnerReviewerRef",
            "harnessReviewerRef",
            "committeeRepresentativeReviewerRef",
            "stopAuthorityOwnerReviewerRef",
            "businessSystemOwnerReviewerRef",
            "negativeGateResultRef",
            "noWriteAttestationRef",
        },
        "required confirmation ref",
        failures,
    )

    blocking_conditions = set(package.get("blockingConditions", []))
    if len(blocking_conditions) != expected["blockingConditionCount"]:
        failures.append("blockingConditionCount mismatch")
    forbidden_actions = set(package.get("forbiddenActions", []))
    if len(forbidden_actions) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    forbidden_outputs = set(data.get("forbiddenOutputs", []))
    if len(forbidden_outputs) != expected["forbiddenOutputCount"]:
        failures.append("forbiddenOutputCount mismatch")
    required_sources = set(data.get("requiredSourceRefs", []))
    if len(required_sources) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for relative_path in required_sources:
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")

    for key in (
        "executesHumanConfirmation",
        "executesCommitteeDecision",
        "sendsEscalationDigest",
        "sendsNotification",
        "executesResend",
        "executesEscalation",
        "executesApproval",
        "executesRetry",
        "executesUnfreeze",
        "writesFormalEvidence",
        "writesHarnessEvidence",
        "writesConfirmationResult",
        "writesCommitteeResult",
        "writesReceiptResult",
        "writesEscalationResult",
        "writesResendResult",
        "writesApprovalResult",
        "writesAcceptedLifecycle",
        "startsServer",
        "connectsDatabase",
        "callsExternalApi",
        "writesKds",
        "writesBusinessSystem",
    ):
        if expected[key] is not False:
            failures.append(f"expectedSummary.{key} must be false")
    if expected["noWrite"] is not True:
        failures.append("expectedSummary.noWrite must be true")

    if failures:
        print("gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "gckf_p0_formal_evidence_execution_escalation_digest_human_confirmation_package_preview_dry_run=pass "
        f"status={data['humanConfirmationPackagePreviewStatus']} "
        f"preview_type={package['previewType']} "
        f"preview_status={package['previewStatus']} "
        f"execution_status={package['executionStatus']} "
        f"confirmation_execution_status={package['confirmationExecutionStatus']} "
        f"committee_execution_status={package['committeeExecutionStatus']} "
        f"resend_execution_status={package['resendExecutionStatus']} "
        f"escalation_execution_status={package['escalationExecutionStatus']} "
        f"approval_execution_status={package['approvalExecutionStatus']} "
        f"retry_execution_status={package['retryExecutionStatus']} "
        f"unfreeze_execution_status={package['unfreezeExecutionStatus']} "
        f"execution_mode={data['executionMode']} "
        f"source_escalation_digest_status={source_digest['escalationDigestPreviewStatus']} "
        f"source_digest_execution_status={source['executionStatus']} "
        f"source_resend_execution_status={source['resendExecutionStatus']} "
        f"source_escalation_execution_status={source['escalationExecutionStatus']} "
        f"covered_escalation_digest_status={data['coveredEscalationDigestPreviewStatus']} "
        f"reviewer_roles={len(roles)} "
        f"package_sections={len(sections)} "
        f"decision_options={len(decision_options)} "
        f"committee_triggers={len(committee_triggers)} "
        f"confirmation_checks={len(checks)} "
        f"required_confirmation_refs={len(refs)} "
        f"blocking_conditions={len(blocking_conditions)} "
        f"forbidden_actions={len(forbidden_actions)} "
        f"forbidden_outputs={len(forbidden_outputs)} "
        f"required_sources={len(required_sources)} "
        "not_final_acceptance=covered dry_run_only=covered "
        "human_confirmation_boundary=covered committee_trigger_boundary=covered "
        "negative_gate_result=covered no_write_attestation=covered "
        "starts_server=0 connects_database=0 calls_external_api=0 "
        "executes_human_confirmation=0 executes_committee_decision=0 "
        "sends_escalation_digest=0 sends_notification=0 executes_resend=0 "
        "executes_escalation=0 executes_approval=0 executes_retry=0 executes_unfreeze=0 "
        "writes_kds=0 writes_business_system=0 writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 writes_formal_evidence=0 "
        "writes_confirmation_result=0 writes_committee_result=0 "
        "writes_receipt_result=0 writes_escalation_result=0 writes_resend_result=0 "
        "writes_approval_result=0 no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
