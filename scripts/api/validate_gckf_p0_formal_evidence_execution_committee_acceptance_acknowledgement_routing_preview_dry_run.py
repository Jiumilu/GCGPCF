#!/usr/bin/env python3
"""Validate P0 committee acceptance acknowledgement routing preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-committee-acceptance-acknowledgement-routing-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceCommitteeAcceptanceAcknowledgementEnvelopePreview"])
    source = source_data["committeeAcceptanceAcknowledgementEnvelopePreview"]
    routing = data["committeeAcceptanceAcknowledgementRoutingPreview"]

    if data.get("committeeAcceptanceAcknowledgementRoutingPreviewStatus") != expected[
        "committeeAcceptanceAcknowledgementRoutingPreviewStatus"
    ]:
        failures.append("committeeAcceptanceAcknowledgementRoutingPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalCommitteeAcceptanceAcknowledgementRouting") is not expected[
        "notFinalCommitteeAcceptanceAcknowledgementRouting"
    ]:
        failures.append("routing preview must state notFinalCommitteeAcceptanceAcknowledgementRouting=true")
    if routing.get("previewType") != expected["previewType"]:
        failures.append("committee acceptance acknowledgement routing previewType mismatch")
    if routing.get("previewStatus") != expected["previewStatus"]:
        failures.append("committee acceptance acknowledgement routing previewStatus must remain candidate_preview")
    if routing.get("executionMode") != expected["executionMode"]:
        failures.append("committee acceptance acknowledgement routing executionMode mismatch")
    if routing.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("committee acceptance acknowledgement routing must remain dryRunOnly=true")

    for key in (
        "executionStatus",
        "acknowledgementRoutingExecutionStatus",
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
        if routing.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("committeeAcceptanceAcknowledgementEnvelopePreviewStatus") != expected[
        "sourceCommitteeAcceptanceAcknowledgementEnvelopePreviewStatus"
    ]:
        failures.append("source envelope preview must remain candidate_preview")
    source_status_map = {
        "executionStatus": "sourceEnvelopeExecutionStatus",
        "envelopeAssemblyExecutionStatus": "sourceEnvelopeAssemblyExecutionStatus",
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
        failures.append("source envelope preview must remain dryRunOnly=true")
    if routing.get("sourceCommitteeAcceptanceAcknowledgementEnvelopePreviewId") != source.get("id"):
        failures.append("sourceCommitteeAcceptanceAcknowledgementEnvelopePreviewId must match D68 preview id")
    if data.get("coveredCommitteeAcceptanceAcknowledgementEnvelopePreviewStatus") != source.get("previewStatus"):
        failures.append("covered envelope status must match D68 preview status")

    count_checks = {
        "routingRoles": "routingRoleCount",
        "routingSections": "routingSectionCount",
        "candidateRoutingFields": "candidateRoutingFieldCount",
        "routingReadinessPrerequisites": "routingReadinessPrerequisiteCount",
        "routingDecisionConstraints": "routingDecisionConstraintCount",
        "routingChecks": "routingCheckCount",
        "requiredRoutingRefs": "requiredRoutingRefCount",
        "forbiddenActions": "forbiddenActionCount",
    }
    for actual_key, expected_key in count_checks.items():
        if len(set(routing.get(actual_key, []))) != expected[expected_key]:
            failures.append(f"{actual_key} count mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(routing.get("routingSections", [])),
        {
            "candidate_routing_header",
            "candidate_recipient_routing_matrix",
            "candidate_acknowledgement_route_steps",
            "candidate_acl_boundary_snapshot",
            "candidate_quorum_snapshot",
            "candidate_conflict_of_interest_snapshot",
            "candidate_blocker_and_hold_snapshot",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "committee acceptance acknowledgement routing section",
        failures,
    )
    require_all(
        set(routing.get("routingDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "acknowledgement_routing_not_formal_route",
            "no_acknowledgement_routing_execution",
            "no_envelope_assembly_execution",
            "no_committee_acceptance_execution",
            "no_committee_acknowledgement_execution",
            "no_committee_case_opening",
            "no_committee_decision",
            "no_harness_evidence_write",
        },
        "committee acceptance acknowledgement routing constraint",
        failures,
    )
    require_all(
        set(routing.get("forbiddenActions", [])),
        {
            "execute_acknowledgement_routing",
            "execute_envelope_assembly",
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
        "executesAcknowledgementRouting",
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
        print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_routing_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_committee_acceptance_acknowledgement_routing_preview_dry_run=pass")
    print(f"status={routing['previewStatus']}")
    print(f"execution_mode={routing['executionMode']}")
    print("executes_acknowledgement_routing=0")
    print("executes_envelope_assembly=0")
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
