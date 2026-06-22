#!/usr/bin/env python3
"""Validate P0 repair path workpack dry-run without creating KWE/LOOP records."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures" / "api" / "gckf-p0-repair-path-workpack-dry-run-v0.1.json"


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text())


def main() -> int:
    data = json.loads(FIXTURE.read_text())
    expected = data["expectedSummary"]
    failures: list[str] = []

    decision_template = load_json(data["sourceDecisionTemplate"])
    template = decision_template["decisionTemplate"]
    decision_cases = {case["outcome"]: case for case in template["decisionCases"]}

    if data.get("workpackStatus") != expected["workpackStatus"]:
        failures.append("workpackStatus must remain candidate")
    if decision_template.get("templateStatus") != expected["sourceDecisionTemplateStatus"]:
        failures.append("source decision template status mismatch")
    if data.get("notFinalAcceptance") is not expected["notFinalAcceptance"]:
        failures.append("workpack must state notFinalAcceptance=true")

    covered = data["coveredDecisionOutcomes"]
    excluded = data["excludedDecisionOutcomes"]
    work_items = data["candidateWorkItems"]
    if len(covered) != expected["coveredDecisionOutcomeCount"]:
        failures.append("coveredDecisionOutcomeCount mismatch")
    if len(excluded) != expected["excludedDecisionOutcomeCount"]:
        failures.append("excludedDecisionOutcomeCount mismatch")
    if len(work_items) != expected["candidateWorkItemCount"]:
        failures.append("candidateWorkItemCount mismatch")
    if len(data["requiredSourceRefs"]) != expected["requiredSourceRefCount"]:
        failures.append("requiredSourceRefCount mismatch")

    required_covered = {"repair_required", "scope_violation_found"}
    required_excluded = {"approved_for_formal_harness_evidence", "rejected"}
    if set(covered) != required_covered:
        failures.append("covered decisions must be repair_required and scope_violation_found")
    if set(excluded) != required_excluded:
        failures.append("excluded decisions must be approved_for_formal_harness_evidence and rejected")
    if not set(covered).isdisjoint(set(excluded)):
        failures.append("covered and excluded decisions must not overlap")

    for outcome in covered + excluded:
        if outcome not in decision_cases:
            failures.append(f"decision outcome missing from D24 template: {outcome}")

    work_item_ids = [item["id"] for item in work_items]
    if len(set(work_item_ids)) != len(work_item_ids):
        failures.append("candidate work item ids must be unique")
    for item in work_items:
        outcome = item["sourceDecisionOutcome"]
        if outcome not in required_covered:
            failures.append(f"{item['id']} must only derive from repair or violation outcomes")
        if item.get("targetStatus") != "candidate":
            failures.append(f"{item['id']} targetStatus must remain candidate")
        if not item.get("requiredActions"):
            failures.append(f"{item['id']} missing requiredActions")
        if not item.get("requiredRefs"):
            failures.append(f"{item['id']} missing requiredRefs")
        forbidden_actions = set(item.get("forbiddenActions", []))
        if "write_formal_evidence" not in forbidden_actions:
            failures.append(f"{item['id']} must forbid write_formal_evidence")
        if "promote_lifecycle" not in forbidden_actions:
            failures.append(f"{item['id']} must forbid promote_lifecycle")

    engines = {item["targetEngine"] for item in work_items}
    if engines != {"KWE", "LOOP"}:
        failures.append("candidate work items must cover KWE and LOOP follow-up")
    priorities = {item["sourceDecisionOutcome"]: item["priority"] for item in work_items}
    if priorities.get("scope_violation_found") != "P0":
        failures.append("scope_violation_found must be P0")
    if priorities.get("repair_required") != "P1":
        failures.append("repair_required must be P1")

    for source_ref in data["requiredSourceRefs"]:
        if not (ROOT / source_ref).exists():
            failures.append(f"required source ref missing: {source_ref}")

    forbidden_terms = [
        "\"writesFormalEvidence\": true",
        "\"writesHarnessEvidence\": true",
        "\"writesAcceptedLifecycle\": true",
        "\"createsKweWorkItem\": true",
        "\"createsLoopFollowUp\": true",
        "\"startsServer\": true",
        "\"connectsDatabase\": true",
        "\"callsExternalApi\": true",
        "\"writesKds\": true",
        "\"writesBusinessSystem\": true",
        "\"workpackStatus\": \"accepted\"",
        "\"targetStatus\": \"created\"",
    ]
    text = FIXTURE.read_text()
    for term in forbidden_terms:
        if term in text:
            failures.append(f"forbidden repair workpack term {term} in {FIXTURE}")

    if failures:
        print("gckf_p0_repair_path_workpack_dry_run=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "gckf_p0_repair_path_workpack_dry_run=pass "
        f"status={expected['workpackStatus']} "
        f"source_template_status={expected['sourceDecisionTemplateStatus']} "
        f"covered_decisions={expected['coveredDecisionOutcomeCount']} "
        f"excluded_decisions={expected['excludedDecisionOutcomeCount']} "
        f"candidate_work_items={expected['candidateWorkItemCount']} "
        f"required_sources={expected['requiredSourceRefCount']} "
        "kwe_loop_follow_up=covered "
        "not_final_acceptance=covered "
        "starts_server=0 "
        "connects_database=0 "
        "calls_external_api=0 "
        "writes_kds=0 "
        "writes_business_system=0 "
        "writes_accepted_lifecycle=0 "
        "writes_harness_evidence=0 "
        "writes_formal_evidence=0 "
        "creates_kwe_work_item=0 "
        "creates_loop_follow_up=0 "
        "no_write=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
