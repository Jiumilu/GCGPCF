#!/usr/bin/env python3
"""Validate the GFIS-WAS source-record field crosswalk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT.parent
WAS_ROOT = BASE / "WAS世界资产体系"
GFIS_ROOT = BASE / "GlobalCloud GFIS"

EVIDENCE_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gfis-was-source-record-field-crosswalk-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-CROSSWALK-001.md"
SUBMISSION_PRECHECK = ROOT / "docs/harness/evidence/gfis-was-source-record-submission-precheck-20260621.json"
NEGATIVE_FIXTURES = ROOT / "docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.json"
WAS_PROFILE = WAS_ROOT / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
GFIS_TEMPLATE = GFIS_ROOT / "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order/customer-requirement-platform-order.source-record.template.json"
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
ZERO_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "accepted_integrated",
    "production_ready",
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


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    precheck = load_json(SUBMISSION_PRECHECK)
    negative = load_json(NEGATIVE_FIXTURES)
    profile = load_yaml(WAS_PROFILE)
    template = load_json(GFIS_TEMPLATE)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    stages = profile.get("stages")
    require(isinstance(stages, list), "WAS stages must be a list")
    s01 = next((stage for stage in stages if stage.get("stageId") == "S01-customer-requirement-or-platform-order"), None)
    require(isinstance(s01, dict), "missing WAS S01 stage")

    require(evidence.get("evidence_id") == "GFIS-WAS-SOURCE-RECORD-FIELD-CROSSWALK-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_was_source_record_field_crosswalk_pass", "invalid evidence status")
    require(evidence.get("scope", {}).get("crosswalk_type") == "future_real_submission_instruction_no_business_fact", "crosswalk type mismatch")
    require(precheck.get("status") == "gfis_was_source_record_submission_precheck_pass_with_empty_hold", "submission precheck must pass")
    require(negative.get("status") == "gfis_was_source_record_negative_fixtures_pass", "negative fixture gate must pass")
    require(template.get("template_only") is True, "GFIS template must remain template only")

    for source_name, source_path in evidence.get("sources", {}).items():
        require(Path(source_path).exists(), f"source missing for {source_name}: {source_path}")

    coverage = evidence.get("coverage", {})
    require(coverage.get("gfis_native_required_fields") == 12, "GFIS required count mismatch")
    require(coverage.get("was_required_fields") == 12, "WAS required count mismatch")
    require(coverage.get("crosswalk_entries") == 12, "crosswalk entry count mismatch")
    require(coverage.get("direct_equalities") == 2, "direct equalities mismatch")
    require(coverage.get("fixed_was_values") == 5, "fixed WAS values mismatch")
    require(coverage.get("explicit_submission_fields") == 5, "explicit submission fields mismatch")
    for key in ZERO_KEYS:
        require(coverage.get(key) == 0, f"coverage.{key} must be 0")

    require(set(evidence.get("gfis_native_required_fields", [])) == GFIS_NATIVE_FIELDS, "GFIS field set mismatch")
    require(set(evidence.get("was_required_fields", [])) == WAS_FIELDS, "WAS field set mismatch")

    crosswalk = evidence.get("crosswalk")
    require(isinstance(crosswalk, list) and len(crosswalk) == 12, "crosswalk must have 12 entries")
    by_field = {entry.get("was_field"): entry for entry in crosswalk}
    require(set(by_field) == WAS_FIELDS, "crosswalk must cover all WAS fields")

    require(by_field["objectFamily"].get("rule") == "must_equal_gfis_object_family", "objectFamily rule mismatch")
    require(by_field["objectFamily"].get("gfis_source") == "object_family", "objectFamily source mismatch")
    require(by_field["objectFamily"].get("required_value") == "CustomerRequirementOrPlatformOrder", "objectFamily required value mismatch")
    require(by_field["kdsBacklink"].get("rule") == "must_equal_gfis_source_of_record_backlink", "kdsBacklink rule mismatch")
    require(by_field["kdsBacklink"].get("required_prefix") == "开发/", "kdsBacklink prefix mismatch")
    require(by_field["assetDimension"].get("required_value") == s01.get("assetDimension") == "data_asset", "assetDimension fixed value mismatch")
    require(by_field["flowType"].get("required_value") == s01.get("flowType") == "commerce_flow", "flowType fixed value mismatch")
    require(by_field["lifecycle"].get("required_value") == s01.get("lifecycle") == "pending_business_verification", "lifecycle fixed value mismatch")
    require(by_field["trustLevel"].get("required_value") == s01.get("trustLevel") == "T4", "trustLevel fixed value mismatch")
    require(by_field["nextAction"].get("required_value") == s01.get("nextAction"), "nextAction fixed value mismatch")
    require(by_field["sourceRefs"].get("required_value") == s01.get("sourceRefs"), "sourceRefs mismatch")
    require(by_field["evidenceRefs"].get("required_value") == s01.get("evidenceRefs"), "evidenceRefs mismatch")
    require(by_field["waesGateRefs"].get("required_value") == s01.get("waesGateRefs"), "waesGateRefs mismatch")
    require(by_field["promotionBlockers"].get("required_value") == s01.get("promotionBlockers"), "promotionBlockers mismatch")

    submitted_files = sorted(RECEIVING_DIR.glob("*.customer-requirement-platform-order.source-record.json"))
    require(len(submitted_files) == 0, "GFIS receiving directory must remain empty of real source-record submissions")

    for phrase in [
        "GPCF 已建立 GFIS 原生 source-record 字段与 WAS/Ontology 字段的提交 crosswalk",
        "GFIS 原生必填字段 | `12`",
        "WAS/Ontology 必填字段 | `12`",
        "本 evidence 不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GFIS-WAS source-record crosswalk 已具备可填写和可审核基线" in loop_round, "loop round missing feedback")

    print(
        "gfis_was_source_record_field_crosswalk=pass "
        "gfis_native_required_fields=12 was_required_fields=12 crosswalk_entries=12 "
        "direct_equalities=2 fixed_was_values=5 explicit_submission_fields=5 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
