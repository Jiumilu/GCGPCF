#!/usr/bin/env python3
"""Validate negative fixtures for the GFIS-WAS source-record precheck."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT.parent
WAS_ROOT = BASE / "WAS世界资产体系"
GFIS_ROOT = BASE / "GlobalCloud GFIS"

EVIDENCE_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-NEGATIVE-FIXTURES-001.md"
SUBMISSION_PRECHECK = ROOT / "docs/harness/evidence/gfis-was-source-record-submission-precheck-20260621.json"
WAS_PROFILE = WAS_ROOT / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
GFIS_SCAN = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-scan.json"
RECEIVING_DIR = GFIS_ROOT / "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order"

GFIS_NATIVE_FIELDS = {
    "object_family",
    "sop_stage",
    "source_kind",
    "customer_order_original_or_platform_order_receipt",
    "customer_confirmed_product_spec",
    "delivery_requirement",
    "source_of_record_backlink",
    "source_record_hash",
    "issuing_party",
    "owner_confirmation",
    "received_at",
    "runtime_site_context",
}
WAS_FIELDS = {
    "objectFamily",
    "sourceRecordId",
    "assetDimension",
    "flowType",
    "lifecycle",
    "trustLevel",
    "sourceRefs",
    "evidenceRefs",
    "waesGateRefs",
    "promotionBlockers",
    "nextAction",
    "kdsBacklink",
}
ALLOWED_SOURCE_KINDS = {"customer_order_original", "platform_order_receipt"}
FORBIDDEN_SOURCE_KINDS = {
    "formal_quotation",
    "contract_review_draft",
    "kds_candidate",
    "user_statement",
    "loop_document",
    "gfis_demo",
}
ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(read(path))
    require(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(read(path))
    require(isinstance(value, dict), f"{path} must contain a YAML mapping")
    return value


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid front matter")
    metadata = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def is_placeholder(value: Any) -> bool:
    if value in (None, "", [], {}):
        return True
    if isinstance(value, str) and value.strip().startswith("<"):
        return True
    return False


def reject_reasons(candidate: dict[str, Any], s01: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in GFIS_NATIVE_FIELDS:
        if is_placeholder(candidate.get(field)):
            failures.append(f"missing_gfis_field:{field}")
    for field in WAS_FIELDS:
        if is_placeholder(candidate.get(field)):
            failures.append(f"missing_was_field:{field}")
    if candidate.get("object_family") != "CustomerRequirementOrPlatformOrder":
        failures.append("gfis_object_family_mismatch")
    if candidate.get("objectFamily") != "CustomerRequirementOrPlatformOrder":
        failures.append("was_object_family_mismatch")
    if candidate.get("assetDimension") != s01.get("assetDimension"):
        failures.append("asset_dimension_mismatch")
    if candidate.get("flowType") != s01.get("flowType"):
        failures.append("flow_type_mismatch")
    if candidate.get("lifecycle") != s01.get("lifecycle"):
        failures.append("lifecycle_mismatch")
    if candidate.get("trustLevel") != s01.get("trustLevel"):
        failures.append("trust_level_mismatch")
    source_hash = str(candidate.get("source_record_hash", ""))
    if not re.fullmatch(r"[a-fA-F0-9]{64}", source_hash):
        failures.append("source_record_hash_not_sha256_hex_64")
    backlink = str(candidate.get("source_of_record_backlink", ""))
    if not backlink.startswith("开发/"):
        failures.append("gfis_kds_backlink_prefix_mismatch")
    if candidate.get("kdsBacklink") != backlink:
        failures.append("was_kds_backlink_mismatch")
    source_kind = str(candidate.get("source_kind", ""))
    if source_kind in FORBIDDEN_SOURCE_KINDS:
        failures.append(f"forbidden_source_kind:{source_kind}")
    elif source_kind and source_kind not in ALLOWED_SOURCE_KINDS:
        failures.append(f"source_kind_not_allowed:{source_kind}")
    return failures


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    precheck = load_json(SUBMISSION_PRECHECK)
    profile = load_yaml(WAS_PROFILE)
    gfis_scan = load_json(GFIS_SCAN)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    stages = profile.get("stages")
    require(isinstance(stages, list), "WAS stages must be a list")
    s01 = next((stage for stage in stages if stage.get("stageId") == "S01-customer-requirement-or-platform-order"), None)
    require(isinstance(s01, dict), "missing WAS S01 stage")

    require(evidence.get("evidence_id") == "GFIS-WAS-SOURCE-RECORD-NEGATIVE-FIXTURES-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_was_source_record_negative_fixtures_pass", "invalid evidence status")
    require(evidence.get("scope", {}).get("fixture_type") == "in_gpcf_only_no_gfis_directory_write", "fixture type mismatch")
    require(precheck.get("status") == "gfis_was_source_record_submission_precheck_pass_with_empty_hold", "submission precheck must be pass_with_empty_hold")

    for source_name, source_path in evidence.get("sources", {}).items():
        require(Path(source_path).exists(), f"source missing for {source_name}: {source_path}")
    before_files = sorted(RECEIVING_DIR.glob("*.customer-requirement-platform-order.source-record.json"))

    fixtures = evidence.get("negative_fixtures")
    require(isinstance(fixtures, list) and len(fixtures) == 6, "negative fixture count mismatch")
    rejected = 0
    accepted = 0
    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id")
        candidate = fixture.get("candidate")
        expected = fixture.get("expected_reject_reasons")
        require(isinstance(fixture_id, str) and fixture_id, "fixture id missing")
        require(isinstance(candidate, dict), f"{fixture_id}: candidate must be object")
        require(isinstance(expected, list) and expected, f"{fixture_id}: expected reject reasons missing")
        actual = reject_reasons(candidate, s01)
        for reason in expected:
            require(reason in actual, f"{fixture_id}: missing expected reject reason {reason}; actual={actual}")
        if actual:
            rejected += 1
        else:
            accepted += 1

    after_files = sorted(RECEIVING_DIR.glob("*.customer-requirement-platform-order.source-record.json"))
    require([path.name for path in before_files] == [path.name for path in after_files], "GFIS receiving directory changed")

    summary = evidence.get("fixture_summary", {})
    require(summary.get("negative_fixture_count") == len(fixtures), "summary negative count mismatch")
    require(summary.get("rejected_fixture_count") == rejected, "summary rejected count mismatch")
    require(summary.get("accepted_fixture_count") == accepted == 0, "summary accepted count mismatch")
    require(summary.get("gfis_directory_writes") == 0, "GFIS directory writes must be 0")
    for key in ZERO_KEYS:
        require(summary.get(key) == 0, f"summary.{key} must be 0")
    gfis_counts = gfis_scan.get("counts", {})
    require(gfis_counts.get("submitted_files_found") == 0, "GFIS submitted files must remain 0")
    require(gfis_counts.get("valid_source_records") == 0, "GFIS valid source records must remain 0")

    for phrase in [
        "6 个负例全部在 GPCF evidence 内部回放",
        "accepted_fixture_count=0",
        "本 evidence 不向 GFIS 接收目录写入 fixture",
        "本 evidence 不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GFIS-WAS source-record 提交前扫描器已具备负例拒收证据" in loop_round, "loop round missing feedback")

    print(
        "gfis_was_source_record_negative_fixtures=pass "
        f"negative_fixture_count={len(fixtures)} rejected_fixture_count={rejected} "
        f"accepted_fixture_count={accepted} gfis_directory_writes=0 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
