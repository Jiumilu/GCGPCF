#!/usr/bin/env python3
"""Validate P0 rejection archive path dry-run without writing archive records."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-rejection-archive-path-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    decision_template = load_json(data["sourceDecisionTemplate"])
    decision_cases = {case["outcome"]: case for case in decision_template["decisionTemplate"]["decisionCases"]}
    archive = data["archiveCandidate"]

    if data.get("archivePathStatus") != expected["archivePathStatus"]:
        failures.append("archivePathStatus must remain candidate")
    if archive.get("archiveType") != expected["archiveType"]:
        failures.append("archiveType mismatch")
    if archive.get("archiveStatus") != expected["archiveStatus"]:
        failures.append("archiveStatus must remain candidate")
    if decision_template.get("templateStatus") != expected["sourceDecisionTemplateStatus"]:
        failures.append("source decision template status mismatch")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("archive path must state notFinalAcceptance=true")

    covered = data["coveredDecisionOutcomes"]
    excluded = data["excludedDecisionOutcomes"]
    if covered != ["rejected"]:
        failures.append("coveredDecisionOutcomes must contain only rejected")
    if len(excluded) != expected["excludedDecisionOutcomeCount"]:
        failures.append("excludedDecisionOutcomeCount mismatch")
    if len(covered) != expected["coveredDecisionOutcomeCount"]:
        failures.append("coveredDecisionOutcomeCount mismatch")
    if set(covered).intersection(excluded):
        failures.append("covered and excluded decisions must not overlap")
    for outcome in covered + excluded:
        if outcome not in decision_cases:
            failures.append(f"decision outcome missing from D24 template: {outcome}")

    rejected_case = decision_cases.get("rejected", {})
    for required in ["rejectionReason", "evidenceRefs", "decisionRationale"]:
        if required not in rejected_case.get("requiredFields", []):
            failures.append(f"D24 rejected case missing required field: {required}")
        if required not in archive.get("requiredFields", []):
            failures.append(f"archive candidate missing required field: {required}")

    if len(archive["requiredFields"]) != expected["requiredFieldCount"]:
        failures.append("requiredFieldCount mismatch")
    if len(archive["requiredActions"]) != expected["requiredActionCount"]:
        failures.append("requiredActionCount mismatch")
    if len(archive["rebuildPreconditions"]) != expected["rebuildPreconditionCount"]:
        failures.append("rebuildPreconditionCount mismatch")
    if len(data["requiredSourceRefs"]) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    required_archive_actions = {
        "mark_candidate_packet_not_reusable",
        "record_rejection_basis",
        "require_new_candidate_packet_for_resubmission",
        "preserve_lineage_refs",
    }
    if set(archive["requiredActions"]) != required_archive_actions:
        failures.append("archive requiredActions mismatch")

    required_rebuild = {
        "new_or_repaired_source_evidence",
        "new_harness_review_input_packet",
        "new_harness_evidence_candidate_record",
        "new_harness_decision_template_review",
    }
    if set(archive["rebuildPreconditions"]) != required_rebuild:
        failures.append("rebuildPreconditions mismatch")

    forbidden_actions = set(archive.get("forbiddenActions", []))
    for forbidden in [
        "write_formal_evidence",
        "promote_lifecycle",
        "reuse_rejected_packet_as_accepted",
        "enable_business_writeback",
    ]:
        if forbidden not in forbidden_actions:
            failures.append(f"archive candidate must forbid {forbidden}")

    for source_ref in data["requiredSourceRefs"]:
        if not (ROOT / source_ref).exists():
            failures.append(f"required source ref missing: {source_ref}")

    forbidden_terms = [
        "\"writesArchiveRecord\": true",
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"archivePathStatus\": \"accepted\"",
        "\"archiveStatus\": \"archived\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden rejection archive term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_rejection_archive_path_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_rejection_archive_path_dry_run=pass "
        f"status={expected['archivePathStatus']} "
        f"archive_type={expected['archiveType']} "
        f"archive_status={expected['archiveStatus']} "
        f"source_template_status={expected['sourceDecisionTemplateStatus']} "
        f"covered_decisions={expected['coveredDecisionOutcomeCount']} "
        f"excluded_decisions={expected['excludedDecisionOutcomeCount']} "
        f"required_fields={expected['requiredFieldCount']} "
        f"required_actions={expected['requiredActionCount']} "
        f"rebuild_preconditions={expected['rebuildPreconditionCount']} "
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
        "writes_archive_record=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
