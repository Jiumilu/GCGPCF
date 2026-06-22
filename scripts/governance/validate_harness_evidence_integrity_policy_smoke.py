#!/usr/bin/env python3
"""Validate Harness evidence reference integrity policy.

This validator reads local OKF, shared type and fixture files only. It does not
write Harness evidence, KDS facts, WAES gate results, KWE work items, ledgers,
committee decisions, business systems, external share permissions, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "harness-evidence-integrity-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "harness-evidence-integrity.ts"
EVIDENCE_TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "evidence.ts"
FIXTURE = ROOT / "fixtures" / "governance" / "harness-evidence-integrity-policy-smoke.json"


def union_literals(path: Path, type_name: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def camel_from_snake(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]
    record = fixture["evidenceRecord"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals(TYPE_FILE, "HarnessEvidenceReferenceGroup") != policy["reference_groups"]:
        failures.append("HarnessEvidenceReferenceGroup union does not match policy")
    if union_literals(TYPE_FILE, "HarnessEvidenceIntegrityStatus") != policy["integrity_statuses"]:
        failures.append("HarnessEvidenceIntegrityStatus union does not match policy")
    if union_literals(EVIDENCE_TYPE_FILE, "EvidenceKind") != policy["evidence_kinds"]:
        failures.append("EvidenceKind union does not match policy evidence_kinds")

    for field in policy["minimum_evidence_fields"]:
        if camel_from_snake(field) not in record:
            failures.append(f"sample evidence record missing field: {field}")
    for rule in policy["integrity_rules"]:
        if rule["required"] is not True:
            failures.append(f"integrity rule must be required: {rule['id']}")
    if record["integrityStatus"] == "passed" and record["unresolvedRefs"]:
        failures.append("passed evidence must not contain unresolved refs")
    if record["sensitiveRawContentStored"] is not False:
        failures.append("sample evidence must not store sensitive raw content")
    if record["passedIsBusinessCompletion"] is not False:
        failures.append("passed integrity must not imply business completion")

    checks = {
        "minimumEvidenceFieldCount": len(policy["minimum_evidence_fields"]),
        "referenceGroupCount": len(policy["reference_groups"]),
        "evidenceKindCount": len(policy["evidence_kinds"]),
        "integrityStatusCount": len(policy["integrity_statuses"]),
        "integrityRuleCount": len(policy["integrity_rules"]),
        "sampleUnresolvedRefCount": len(record["unresolvedRefs"]),
        "sampleSensitiveRawContentStored": record["sensitiveRawContentStored"],
        "samplePassedIsBusinessCompletion": record["passedIsBusinessCompletion"],
        "evidenceCanCreateFormalFact": hard["evidence_can_create_formal_fact"],
        "evidenceCanWriteBusinessSystem": hard["evidence_can_write_business_system"],
        "evidenceCanDistributeRevenue": hard["evidence_can_distribute_revenue"],
        "evidenceCanConfirmScore": hard["evidence_can_confirm_score"],
        "evidenceCanTransferQuota": hard["evidence_can_transfer_quota"],
        "evidenceCanSettleBounty": hard["evidence_can_settle_bounty"],
        "evidenceCanCompleteCommitteeDecision": hard["evidence_can_complete_committee_decision"],
        "evidenceCanAllowExternalShare": hard["evidence_can_allow_external_share"],
        "sensitiveRawContentAllowed": hard["sensitive_raw_content_allowed"],
        "passedIsBusinessCompletion": hard["passed_is_business_completion"],
        "writesKdsFact": no_write["writes_kds_fact"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueDistribution": no_write["writes_revenue_distribution"],
        "writesScoreConfirmation": no_write["writes_score_confirmation"],
        "writesQuotaTransfer": no_write["writes_quota_transfer"],
        "writesBountySettlement": no_write["writes_bounty_settlement"],
        "writesCommitteeDecisionCompletion": no_write["writes_committee_decision_completion"],
        "writesExternalSharePermission": no_write["writes_external_share_permission"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("harness_evidence_integrity_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "harness_evidence_integrity_policy_smoke=pass "
        f"evidence_fields={checks['minimumEvidenceFieldCount']} "
        f"reference_groups={checks['referenceGroupCount']} "
        f"evidence_kinds={checks['evidenceKindCount']} "
        f"integrity_statuses={checks['integrityStatusCount']} "
        f"integrity_rules={checks['integrityRuleCount']} "
        "unresolved_refs=0 sensitive_raw_content=false "
        "passed_business_completion=false "
        "writes_kds_fact=0 writes_business_system=0 writes_revenue_distribution=0 "
        "writes_score_confirmation=0 writes_quota_transfer=0 writes_bounty_settlement=0 "
        "writes_committee_decision_completion=0 writes_external_share_permission=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
