#!/usr/bin/env python3
"""Validate P0 committee acceptance acknowledgement envelope preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-envelope-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceCommitteeAcceptanceAcknowledgementPrecheckPreview"])
    source = source_data["committeeAcceptanceAcknowledgementPrecheckPreview"]
    envelope = data["committeeAcceptanceAcknowledgementEnvelopePreview"]

    if data.get("committeeAcceptanceAcknowledgementEnvelopePreviewStatus") != expected[
        "committeeAcceptanceAcknowledgementEnvelopePreviewStatus"
    ]:
        failures.append("committeeAcceptanceAcknowledgementEnvelopePreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCommitteeAcceptanceAcknowledgementEnvelope") is not expected[
        "notFinalCommitteeAcceptanceAcknowledgementEnvelope"
    ]:
        failures.append("envelope preview must state notFinalCommitteeAcceptanceAcknowledgementEnvelope=true")
    if envelope.get("previewType") != expected["previewType"]:
        failures.append("committee acceptance acknowledgement envelope previewType mismatch")
    if envelope.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee acceptance acknowledgement envelope previewStatus must remain candidate_preview")
    if envelope.get("executionMode") != expected["executionMode"]:
        failures.append("committee acceptance acknowledgement envelope executionMode mismatch")
    if envelope.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee acceptance acknowledgement envelope must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "envelopeAssemblyExecutionStatus",
        "committeeAcceptancePrecheckExecutionStatus",
        "committeeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus",
        "committeeDecisionExecutionStatus",
        "confirmationExecutionStatus",
        "unfreezeExecutionStatus",
        "formalWriteExecutionStatus",
    ):
        if envelope.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("committeeAcceptanceAcknowledgementPrecheckPreviewStatus") != expected[
        "sourceCommitteeAcceptanceAcknowledgementPrecheckPreviewStatus"
    ]:
        failures.append("source precheck preview must remain candidate_preview")
    source_status_map = {
        "committeeAcceptancePrecheckExecutionStatus": "sourcePrecheckExecutionStatus",
        "committeeAcceptanceExecutionStatus": "sourceCommitteeAcceptanceExecutionStatus",
        "committeeAcknowledgementExecutionStatus": "sourceCommitteeAcknowledgementExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source precheck preview must remain dryRunOnly=true")
    if envelope.get("sourceCommitteeAcceptanceAcknowledgementPrecheckPreviewId") != source.get("id"):
        failures.append("sourceCommitteeAcceptanceAcknowledgementPrecheckPreviewId must match D67 preview id")
    if data.get("coveredCommitteeAcceptanceAcknowledgementPrecheckPreviewStatus") != source.get("previewStatus"):
        failures.append("covered precheck status must match D67 preview status")

    count_checks = {
        "envelopeRoles": "envelopeRoleCount",
        "envelopeSections": "envelopeSectionCount",
        "candidateEnvelopeFields": "candidateEnvelopeFieldCount",
        "envelopeReadinessPrerequisites": "envelopeReadinessPrerequisiteCount",
        "envelopeDecisionConstraints": "envelopeDecisionConstraintCount",
        "envelopeChecks": "envelopeCheckCount",
        "requiredEnvelopeRefs": "requiredEnvelopeRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(envelope.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(envelope.get("envelopeSections", [])),
        {
            "candidate_envelope_header",
            "candidate_committee_roster_snapshot",
            "candidate_acl_boundary_snapshot",
            "candidate_quorum_snapshot",
            "candidate_conflict_of_interest_snapshot",
            "candidate_blocker_and_hold_snapshot",
            "envelope_integrity_check",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "committee acceptance acknowledgement envelope section",
        failures,
    )
    require_all(
        set(envelope.get("envelopeDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "envelope_preview_not_formal_acknowledgement",
            "no_envelope_assembly_execution",
            "no_committee_acceptance_precheck_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "committee acceptance acknowledgement envelope constraint",
        failures,
    )
    require_all(
        set(envelope.get("forbiddenActions", [])),
        {
            "execute_envelope_assembly",
            "execute_committee_acceptance_precheck",
            "execute_committee_acceptance",
            "execute_committee_acknowledgement",
            "open_committee_case",
            "write_harness_evidence",
            "write_kds",
            "write_business_system",
        },
        "forbidden action",
        failures,
    )
    for relative_path in data.get("requiredSourceRefs", []):
        if not (ROOT / relative_path).exists():
            failures.append(f"missing required source file: {relative_path}")
    for key in (
        "executesEnvelopeAssembly",
        "executesCommitteeAcceptancePrecheck",
        "executesCommitteeAcceptance",
        "executesCommitteeAcknowledgement",
        "opensCommitteeCase",
        "executesCommitteeDecision",
        "executesHumanConfirmation",
        "releasesFreeze",
        "executesUnfreeze",
        "executesIntakeGuard",
        "executesRoutingPackage",
        "executesRouting",
        "writesKds",
        "writesBusinessSystem",
        "writesHarnessEvidence",
        "writesFormalEvidence",
        "writesRevenueDistribution",
        "writesContributionScore",
    ):
        if expected[key] is not False:
            failures.append(f"{key} must be false in expectedSummary")

    if failures:
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_envelope_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_envelope_preview_dry_run=pass")
    print(f"status={envelope['previewStatus']}")
    print(f"execution_mode={envelope['executionMode']}")
    print("executes_envelope_assembly=0")
    print("executes_committee_acceptance_precheck=0")
    print("executes_committee_acceptance=0")
    print("executes_committee_acknowledgement=0")
    print("opens_committee_case=0")
    print("executes_intake_guard=0")
    print("executes_routing_package=0")
    print("executes_routing=0")
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
