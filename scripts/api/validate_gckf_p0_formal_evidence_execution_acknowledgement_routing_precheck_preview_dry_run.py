#!/usr/bin/env python3
"""Validate P0 acknowledgement routing precheck preview dry-run."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "fixtures"
    / "api"
    / "gckf-p0-formal-evidence-execution-acknowledgement-routing-precheck-preview-dry-run-v0.1.json"
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
    source_data = load_json(data["sourceRepairRequestAcknowledgementPreview"])
    source = source_data["repairRequestAcknowledgementPreview"]
    routing = data["acknowledgementRoutingPrecheckPreview"]

    if data.get("acknowledgementRoutingPrecheckPreviewStatus") != expected[
        "acknowledgementRoutingPrecheckPreviewStatus"
    ]:
        failures.append("acknowledgementRoutingPrecheckPreviewStatus must remain candidate_preview")
    if data.get("executionMode") != expected["executionMode"]:
        failures.append("executionMode must remain dry_run_no_write")
    if data.get("notFinalRoutingPrecheck") is not expected["notFinalRoutingPrecheck"]:
        failures.append("routing precheck preview must state notFinalRoutingPrecheck=true")
    if routing.get("previewType") != expected["previewType"]:
        failures.append("routing precheck previewType mismatch")
    if routing.get("previewStatus") != expected["previewStatus"]:
        failures.append("routing precheck previewStatus must remain candidate_preview")
    if routing.get("executionMode") != expected["executionMode"]:
        failures.append("routing precheck preview executionMode mismatch")
    if routing.get("dryRunOnly") is not expected["dryRunOnly"]:
        failures.append("routing precheck preview must remain dryRunOnly=true")

    for key in (
        "executionStatus",
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
        if routing.get(key) != "not_executed":
            failures.append(f"{key} must remain not_executed")

    if source_data.get("repairRequestAcknowledgementPreviewStatus") != expected[
        "sourceRepairRequestAcknowledgementPreviewStatus"
    ]:
        failures.append("source repair request acknowledgement preview must remain candidate_preview")
    source_status_map = {
        "acknowledgementExecutionStatus": "sourceAcknowledgementExecutionStatus",
        "repairRequestExecutionStatus": "sourceRepairRequestExecutionStatus",
        "supplementIntakeExecutionStatus": "sourceSupplementIntakeExecutionStatus",
        "supplementAcceptanceExecutionStatus": "sourceSupplementAcceptanceExecutionStatus",
        "committeeReentryExecutionStatus": "sourceCommitteeReentryExecutionStatus",
        "committeeCaseExecutionStatus": "sourceCommitteeCaseExecutionStatus",
        "committeeDecisionExecutionStatus": "sourceCommitteeDecisionExecutionStatus",
        "confirmationExecutionStatus": "sourceConfirmationExecutionStatus",
        "unfreezeExecutionStatus": "sourceUnfreezeExecutionStatus",
    }
    for source_key, expected_key in source_status_map.items():
        if source.get(source_key) != expected[expected_key]:
            failures.append(f"source {source_key} must remain {expected[expected_key]}")
    if source.get("dryRunOnly") is not True:
        failures.append("source acknowledgement preview must remain dryRunOnly=true")
    if routing.get("sourceRepairRequestAcknowledgementPreviewId") != source.get("id"):
        failures.append("sourceRepairRequestAcknowledgementPreviewId must match D58 preview id")
    if data.get("coveredRepairRequestAcknowledgementPreviewStatus") != source.get("previewStatus"):
        failures.append("covered repair request acknowledgement status must match D58 preview status")

    if len(set(routing.get("routingPrecheckRoles", []))) != expected["routingPrecheckRoleCount"]:
        failures.append("routingPrecheckRoleCount mismatch")
    if not set(source.get("acknowledgementRoles", [])).issubset(set(routing.get("routingPrecheckRoles", []))):
        failures.append("routingPrecheckRoles must include D58 acknowledgementRoles")
    if len(set(routing.get("routingPrecheckSections", []))) != expected["routingPrecheckSectionCount"]:
        failures.append("routingPrecheckSectionCount mismatch")
    if len(set(routing.get("routingPrecheckEnvelopeFields", []))) != expected["routingPrecheckEnvelopeFieldCount"]:
        failures.append("routingPrecheckEnvelopeFieldCount mismatch")
    if len(set(routing.get("routingPrecheckReadinessPrerequisites", []))) != expected[
        "routingPrecheckReadinessPrerequisiteCount"
    ]:
        failures.append("routingPrecheckReadinessPrerequisiteCount mismatch")
    if len(set(routing.get("routingPrecheckDecisionConstraints", []))) != expected[
        "routingPrecheckDecisionConstraintCount"
    ]:
        failures.append("routingPrecheckDecisionConstraintCount mismatch")
    if len(set(routing.get("routingPrecheckChecks", []))) != expected["routingPrecheckCheckCount"]:
        failures.append("routingPrecheckCheckCount mismatch")
    if len(set(routing.get("requiredRoutingPrecheckRefs", []))) != expected["requiredRoutingPrecheckRefCount"]:
        failures.append("requiredRoutingPrecheckRefCount mismatch")
    if len(set(routing.get("forbiddenActions", []))) != expected["forbiddenActionCount"]:
        failures.append("forbiddenActionCount mismatch")
    if len(set(data.get("requiredSourceRefs", []))) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    require_all(
        set(routing.get("routingPrecheckSections", [])),
        {
            "routing_eligibility_candidates",
            "reviewer_lane_candidates",
            "blocked_routing_reason_candidates",
            "response_due_window_snapshot",
            "candidate_routing_path",
            "harness_no_write_guard",
            "no_write_attestation",
        },
        "routing precheck section",
        failures,
    )
    require_all(
        set(routing.get("routingPrecheckDecisionConstraints", [])),
        {
            "candidate_preview_only",
            "routing_precheck_preview_not_formal_routing_precheck",
            "no_routing_precheck_execution",
            "no_routing_execution",
            "no_acknowledgement_execution",
            "no_repair_request_execution",
            "no_committee_reentry",
            "no_committee_case_opening",
            "no_harness_evidence_write",
        },
        "routing precheck constraint",
        failures,
    )
    require_all(
        set(routing.get("forbiddenActions", [])),
        {
            "execute_routing_precheck",
            "execute_routing",
            "execute_acknowledgement",
            "execute_repair_request",
            "accept_supplement_material",
            "execute_committee_reentry",
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
        "executesRoutingPrecheck",
        "executesRouting",
        "executesAcknowledgement",
        "executesRepairRequest",
        "executesSupplementIntake",
        "acceptsSupplementMaterial",
        "executesCommitteeReentry",
        "opensCommitteeCase",
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
        print("gckf_p0_formal_evidence_execution_acknowledgement_routing_precheck_preview_dry_run=fail")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("gckf_p0_formal_evidence_execution_acknowledgement_routing_precheck_preview_dry_run=pass")
    print(f"status={routing['previewStatus']}")
    print(f"execution_mode={routing['executionMode']}")
    print("executes_routing_precheck=0")
    print("executes_routing=0")
    print("executes_acknowledgement=0")
    print("executes_repair_request=0")
    print("executes_supplement_intake=0")
    print("accepts_supplement_material=0")
    print("executes_committee_reentry=0")
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
