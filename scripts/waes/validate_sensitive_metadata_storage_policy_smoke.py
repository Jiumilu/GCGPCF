#!/usr/bin/env python3
"""Validate sensitive metadata-only storage policy.

This validator reads local OKF, shared type and fixture files only. It does not
write raw sensitive content, secrets, evidence, KDS records, or external APIs.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "okf" / "sensitive-metadata-storage-policy.yaml"
TYPE_FILE = ROOT / "packages" / "shared" / "src" / "knowledge" / "sensitive-metadata-storage.ts"
FIXTURE = ROOT / "fixtures" / "waes" / "sensitive-metadata-storage-policy-smoke.json"


def union_literals(type_name: str) -> list[str]:
    text = TYPE_FILE.read_text(encoding="utf-8")
    match = re.search(rf"export type {type_name} =(?P<body>.*?);", text, re.S)
    if not match:
        raise ValueError(f"{type_name} union not found")
    return re.findall(r'"([^"]+)"', match.group("body"))


def main() -> int:
    policy: dict[str, Any] = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected = fixture["expected"]
    hard = policy["hard_boundaries"]
    no_write = policy["no_write_assertions"]

    failures: list[str] = []
    if union_literals("SensitiveDataClass") != policy["sensitive_classes"]:
        failures.append("SensitiveDataClass union does not match policy")
    if union_literals("SensitiveStorageMode") != policy["storage_modes"]:
        failures.append("SensitiveStorageMode union does not match policy")

    pointer_rules = policy["controlled_original_pointer_rules"]
    for key, value in pointer_rules.items():
        if value is not True:
            failures.append(f"controlled pointer rule must be true: {key}")

    checks = {
        "sensitiveClassCount": len(policy["sensitive_classes"]),
        "storageModeCount": len(policy["storage_modes"]),
        "minimumMetadataFieldCount": len(policy["minimum_metadata_fields"]),
        "metadataOnlyRawContentAllowed": hard["metadata_only_raw_content_allowed"],
        "controlledOriginalRawContentAllowedInKds": hard["controlled_original_raw_content_allowed_in_kds"],
        "credentialOrTokenDefaultBlockedOrMetadataOnly": hard["credential_or_token_default_blocked_or_metadata_only"],
        "defaultRagAdmissionForSensitive": hard["default_rag_admission_for_sensitive"],
        "externalShareRequiresRedactionAclAndGate": hard["external_share_requires_redaction_acl_and_gate"],
        "rawOriginalStaysInControlledSpace": hard["raw_original_stays_in_controlled_space"],
        "writesRawContentToKds": no_write["writes_raw_content_to_kds"],
        "writesSecretToDocs": no_write["writes_secret_to_docs"],
        "writesSecretToEvidence": no_write["writes_secret_to_evidence"],
        "writesExternalApi": no_write["writes_external_api"],
    }
    for key, expected_value in expected.items():
        if checks.get(key) != expected_value:
            failures.append(f"{key}: expected={expected_value!r} actual={checks.get(key)!r}")

    if failures:
        print("sensitive_metadata_storage_policy_smoke=fail")
        for failure in failures:
            print(failure)
        return 1

    print(
        "sensitive_metadata_storage_policy_smoke=pass "
        f"sensitive_classes={checks['sensitiveClassCount']} "
        f"storage_modes={checks['storageModeCount']} "
        f"metadata_fields={checks['minimumMetadataFieldCount']} "
        "metadata_only_raw_content=false "
        "controlled_original_raw_content_in_kds=false "
        "default_rag=sensitive_metadata_only "
        "writes_raw_content_to_kds=0 writes_secret_to_docs=0 "
        "writes_secret_to_evidence=0 writes_external_api=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
