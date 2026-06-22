#!/usr/bin/env python3
"""Validate P0 Harness decision template dry-run without final evidence writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-harness-decision-template-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_candidate = load_json(data["sourceCandidateRecord"])
    source_record = source_candidate["candidateRecord"]
    template = data["decisionTemplate"]
    decision_cases = template["decisionCases"]

    if data.get("templateStatus") != expected["templateStatus"]:
        failures.append("templateStatus must remain candidate")
    if template.get("templateType") != expected["templateType"]:
        failures.append("templateType mismatch")
    if source_candidate.get("candidateRecordStatus") != expected["sourceCandidateRecordStatus"]:
        failures.append("source candidate record status mismatch")
    if source_record.get("reviewStatus") != expected["sourceCandidateReviewStatus"]:
        failures.append("source candidate reviewStatus mismatch")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("decision template must state notFinalAcceptance=true")

    if template.get("defaultDecisionStatus") != "pending":
        failures.append("defaultDecisionStatus must be pending")
    if template.get("requiredReviewerType") != expected["requiredReviewerType"]:
        failures.append("requiredReviewerType mismatch")
    if template.get("requiresHumanReview") is not expected["requiresHumanReview"]:
        failures.append("requiresHumanReview mismatch")
    if template.get("requiresHarnessGovernance") is not expected["requiresHarnessGovernance"]:
        failures.append("requiresHarnessGovernance mismatch")
    if template.get("writesFormalEvidence") is not expected["writesFormalEvidence"]:
        failures.append("writesFormalEvidence must remain false")
    if template.get("writesAcceptedLifecycle") is not expected["writesAcceptedLifecycle"]:
        failures.append("writesAcceptedLifecycle must remain false")

    expected_outcomes = set(source_record["allowedDecisionOutcomes"])
    actual_outcomes = {case["outcome"] for case in decision_cases}
    if len(decision_cases) != expected["decisionCaseCount"]:
        failures.append("decisionCaseCount mismatch")
    if actual_outcomes != expected_outcomes:
        failures.append("decision cases must exactly match D23 allowedDecisionOutcomes")

    required_common_fields = {"reviewerId", "reviewedAt", "decisionRationale"}
    for case in decision_cases:
        required_fields = set(case.get("requiredFields", []))
        if not required_common_fields.issubset(required_fields):
            failures.append(f"{case['outcome']} missing common required decision fields")
        if not case.get("requiredEvidenceRefs"):
            failures.append(f"{case['outcome']} missing requiredEvidenceRefs")
        forbidden_actions = set(case.get("forbiddenActions", []))
        if "write_formal_evidence" not in forbidden_actions:
            failures.append(f"{case['outcome']} must forbid write_formal_evidence")
        if "promote_lifecycle" not in forbidden_actions:
            failures.append(f"{case['outcome']} must forbid promote_lifecycle")

    forbidden_final_statuses = {"accepted", "integrated", "production_ready", "business_write_enabled"}
    if data["templateStatus"] in forbidden_final_statuses:
        failures.append("templateStatus must not be final")
    if template["defaultDecisionStatus"] in forbidden_final_statuses:
        failures.append("defaultDecisionStatus must not be final")

    for forbidden in ["accepted", "integrated", "production_ready", "business_write_enabled", "kds_write_enabled"]:
        if forbidden not in data["forbiddenOutputs"]:
            failures.append(f"missing forbidden output marker: {forbidden}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"templateStatus\": \"accepted\"",
        "\"templateStatus\": \"integrated\"",
        "\"defaultDecisionStatus\": \"approved\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden decision template term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_harness_decision_template_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_harness_decision_template_dry_run=pass "
        f"status={expected['templateStatus']} "
        f"template_type={expected['templateType']} "
        f"source_candidate_status={expected['sourceCandidateRecordStatus']} "
        f"source_review_status={expected['sourceCandidateReviewStatus']} "
        f"decision_cases={expected['decisionCaseCount']} "
        "requires_human_review=covered "
        "requires_harness_governance=covered "
        "not_final_acceptance=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
