#!/usr/bin/env python3
"""Validate KDS ACL and external-share view policy.

This validator reads local OKF, shared type and fixture files only. It does not
write ACL stores, publication approvals, KDS objects, external-share permissions,
business systems, ledgers, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "kds-acl-external-share-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "kds-acl-external-share.ts"
FIXTURE = ROOT / "fixtures" / "kds" / "acl-external-share-policy-smoke.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
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
    acl = fixture["aclRecords"][0]
    view = fixture["externalViews"][0]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("KdsAclSubjectType") != policy["subject_types"]:
        failures.append("KdsAclSubjectType union does not match policy")
    if union_literals("KdsAclAction") != policy["allowed_actions"]:
        failures.append("KdsAclAction union does not match policy")

    for field in policy["minimum_acl_fields"]:
        if camel_from_snake(field) not in acl:
            failures.append(f"sample ACL missing field: {field}")
    for field in policy["minimum_external_view_fields"]:
        if camel_from_snake(field) not in view:
            failures.append(f"sample external view missing field: {field}")

    if set(acl["allowedActions"]) != set(policy["external_account_default_actions"]):
        failures.append("sample external account actions do not match defaults")
    if "rawContent" in view["visibleFields"]:
        failures.append("rawContent leaked into visibleFields")
    if view["metadataOnly"] is not True:
        failures.append("sample external view must be metadata-only")

    checks = {
        "subjectTypeCount": len(policy["subject_types"]),
        "allowedActionCount": len(policy["allowed_actions"]),
        "minimumAclFieldCount": len(policy["minimum_acl_fields"]),
        "minimumExternalViewFieldCount": len(policy["minimum_external_view_fields"]),
        "externalAccountDefaultActionCount": len(policy["external_account_default_actions"]),
        "requiredGateCount": len(policy["required_gates_for_external_share"]),
        "sampleExternalAccountActions": acl["allowedActions"],
        "sampleDeniedActionCount": len(acl["deniedActions"]),
        "sampleMetadataOnly": view["metadataOnly"],
        "sampleVisibleRawContent": "rawContent" in view["visibleFields"],
        "sampleBlockedObjectCount": len(fixture["blockedObjects"]),
        "tenantIsolationRequired": hard["tenant_isolation_required"],
        "supplyChainPartitionRequired": hard["supply_chain_partition_required"],
        "externalAccountCrossUnitDetailDefaultDenied": hard["external_account_cross_unit_detail_default_denied"],
        "sensitiveMetadataOnlyRawContentDenied": hard["sensitive_metadata_only_raw_content_denied"],
        "blockedRagExternalShareDenied": hard["blocked_rag_external_share_denied"],
        "t5AiOnlyExternalFactDenied": hard["t5_ai_only_external_fact_denied"],
        "externalShareRequiresWaesGate": hard["external_share_requires_waes_gate"],
        "publicVisibilityRequiresPublicationApproval": hard["public_visibility_requires_publication_approval"],
        "aclPassIsNotRagStrongReference": hard["acl_pass_is_not_rag_strong_reference"],
        "aclPassIsNotBusinessWriteback": hard["acl_pass_is_not_business_writeback"],
        "aclPassIsNotRevenueOrScoreConfirmation": hard["acl_pass_is_not_revenue_or_score_confirmation"],
        "writesAclStore": no_write["writes_acl_store"],
        "writesExternalSharePermission": no_write["writes_external_share_permission"],
        "writesPublicationApproval": no_write["writes_publication_approval"],
        "writesKdsObject": no_write["writes_kds_object"],
        "writesBusinessSystem": no_write["writes_business_system"],
        "writesRevenueOrScoreConfirmation": no_write["writes_revenue_or_score_confirmation"],
        "writesExternalApi": no_write["writes_external_api"],
    }

    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("kds_acl_external_share_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "kds_acl_external_share_policy_smoke=pass "
        f"subject_types={checks['subjectTypeCount']} "
        f"actions={checks['allowedActionCount']} "
        f"acl_fields={checks['minimumAclFieldCount']} "
        f"external_view_fields={checks['minimumExternalViewFieldCount']} "
        f"required_gates={checks['requiredGateCount']} "
        "metadata_only=true visible_raw_content=false blocked_objects=1 "
        "writes_acl_store=0 writes_external_share_permission=0 "
        "writes_publication_approval=0 writes_kds_object=0 "
        "writes_business_system=0 writes_revenue_or_score_confirmation=0 "
        "writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
