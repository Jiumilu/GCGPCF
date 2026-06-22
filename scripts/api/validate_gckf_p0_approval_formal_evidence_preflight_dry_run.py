#!/usr/bin/env python3
"""Validate P0 approval-to-formal-evidence preflight dry-run without writes."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-approval-formal-evidence-preflight-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    source_template = load_json(data["sourceDecisionTemplate"])
    decision_template = source_template["decisionTemplate"]
    decision_cases = decision_template["decisionCases"]
    decision_by_outcome = {case["outcome"]: case for case in decision_cases}
    checklist = data["preflightChecklist"]

    covered = set(data["coveredDecisionOutcomes"])
    excluded = set(data["excludedDecisionOutcomes"])
    expected_covered = {"approved_for_formal_harness_evidence"}
    expected_excluded = {"repair_required", "rejected", "scope_violation_found"}

    if data.get("preflightStatus") != expected["preflightStatus"]:
        failures.append("preflightStatus must remain candidate")
    if checklist.get("preflightStatus") != expected["preflightStatus"]:
        failures.append("checklist preflightStatus must remain candidate")
    if checklist.get("preflightType") != expected["preflightType"]:
        failures.append("preflightType mismatch")
    if source_template.get("templateStatus") != expected["sourceDecisionTemplateStatus"]:
        failures.append("source decision template must remain candidate")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("preflight must state notFinalAcceptance=true")

    if covered != expected_covered:
        failures.append("covered decisions must only include approved_for_formal_harness_evidence")
    if excluded != expected_excluded:
        failures.append("excluded decisions mismatch")
    if covered & excluded:
        failures.append("covered and excluded decisions must not overlap")
    if not (covered | excluded).issubset(decision_by_outcome):
        failures.append("covered/excluded decisions must exist in D24 decision cases")

    approved_case = decision_by_outcome.get("approved_for_formal_harness_evidence", {})
    approved_required_fields = set(approved_case.get("requiredFields", []))
    inherited_required = {"reviewerId", "reviewedAt", "evidenceRefs", "sourceCandidateRecordRef", "decisionRationale"}
    if not inherited_required.issubset(approved_required_fields):
        failures.append("D24 approved case missing inherited required fields")

    required_fields = set(checklist.get("requiredFields", []))
    if len(required_fields) != expected["requiredFieldCount"]:
        failures.append("requiredFieldCount mismatch")
    if not inherited_required.issubset(required_fields):
        failures.append("preflight required fields must include D24 approved fields")
    if "targetHarnessEvidenceType" not in required_fields:
        failures.append("preflight must require targetHarnessEvidenceType")

    if len(checklist.get("requiredEvidenceRefs", [])) != expected["requiredEvidenceRefCount"]:
        failures.append("requiredEvidenceRefCount mismatch")
    if len(checklist.get("preflightChecks", [])) != expected["preflightCheckCount"]:
        failures.append("preflightCheckCount mismatch")

    preflight_checks = set(checklist.get("preflightChecks", []))
    required_checks = {
        "no_repair_required_open_for_same_candidate",
        "no_rejected_archive_for_same_candidate",
        "no_scope_violation_open_for_same_candidate",
        "formal_write_requires_separate_harness_action",
    }
    if not required_checks.issubset(preflight_checks):
        failures.append("preflight checks must guard repair/rejected/scope-violation and separate write action")

    forbidden_actions = set(checklist.get("forbiddenActions", []))
    required_forbidden_actions = {"write_formal_evidence", "promote_lifecycle", "enable_business_writeback", "mark_p0_accepted"}
    if not required_forbidden_actions.issubset(forbidden_actions):
        failures.append("preflight forbidden actions incomplete")

    if len(data.get("requiredSourceRefs", [])) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")
    for source_ref in data.get("requiredSourceRefs", []):
        if not (ROOT / source_ref).exists():
            failures.append(f"missing required source ref: {source_ref}")

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
        "\"preflightStatus\": \"accepted\"",
        "\"formalEvidenceWritten\": true",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden preflight term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_approval_formal_evidence_preflight_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_approval_formal_evidence_preflight_dry_run=pass "
        f"status={expected['preflightStatus']} "
        f"preflight_type={expected['preflightType']} "
        f"source_template_status={expected['sourceDecisionTemplateStatus']} "
        f"covered_decisions={expected['coveredDecisionOutcomeCount']} "
        f"excluded_decisions={expected['excludedDecisionOutcomeCount']} "
        f"required_fields={expected['requiredFieldCount']} "
        f"required_evidence_refs={expected['requiredEvidenceRefCount']} "
        f"preflight_checks={expected['preflightCheckCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
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
