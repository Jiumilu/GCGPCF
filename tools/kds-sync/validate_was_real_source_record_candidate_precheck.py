#!/usr/bin/env python3
"""Validate WAS/Ontology P4 real source-record candidate precheck."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/was-real-source-record-candidate-precheck-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001.md"
TEMPLATE = ROOT / "docs/harness/intake/was-real-source-record-candidate-template.yaml"
INTAKE_DIR = ROOT / "docs/harness/intake"
FIXTURE_DIR = ROOT / "fixtures/was"
PREVIOUS_INTAKE_PACK = ROOT / "docs/harness/evidence/ontology-was-real-source-record-intake-pack-20260621.json"

PROJECT_GROUP = [
    "GFIS",
    "GPC",
    "PVAOS",
    "WAES",
    "KDS",
    "Brain",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "GPCF",
    "Studio",
    "WAS",
]
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
ACCEPTED_SOURCE_KINDS = {"customer_order_original", "platform_order_receipt"}
REQUIRED_PROMOTION_BLOCKERS = {"valid_source_record_missing", "customer_confirmation_missing"}
REQUIRED_WAES_GATE = "waes://gate/customer-order-source-record-review"


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
    parsed = yaml.safe_load(metadata.strip("-\n"))
    require(isinstance(parsed, dict), f"{path.relative_to(ROOT)} front matter must be a YAML mapping")
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in metadata, f"{path.relative_to(ROOT)} missing marker: {phrase}")
    require(
        "Studio" in metadata and "WAS" in metadata,
        f"{path.relative_to(ROOT)} frontmatter must include full project group scope",
    )
    require(
        parsed.get("related_projects") == PROJECT_GROUP,
        f"{path.relative_to(ROOT)} related_projects must match full project group scope",
    )
    require(
        parsed.get("domain") == "ontology-governance",
        f"{path.relative_to(ROOT)} domain must be ontology-governance",
    )


def is_missing(value: Any) -> bool:
    if value in (None, "", [], {}):
        return True
    return isinstance(value, str) and value.strip().startswith("<")


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for field in GFIS_NATIVE_FIELDS:
        if is_missing(candidate.get(field)):
            failures.append(f"missing_gfis_field:{field}")
    for field in WAS_FIELDS:
        if is_missing(candidate.get(field)):
            failures.append(f"missing_was_field:{field}")

    if candidate.get("source_kind") not in ACCEPTED_SOURCE_KINDS:
        failures.append("source_kind_not_customer_order_or_platform_receipt")
    if candidate.get("object_family") != "CustomerRequirementOrPlatformOrder":
        failures.append("gfis_object_family_mismatch")
    if candidate.get("objectFamily") != "CustomerRequirementOrPlatformOrder":
        failures.append("was_object_family_mismatch")
    if candidate.get("assetDimension") != "data_asset":
        failures.append("asset_dimension_mismatch")
    if candidate.get("flowType") != "commerce_flow":
        failures.append("flow_type_mismatch")
    if candidate.get("lifecycle") != "pending_business_verification":
        failures.append("lifecycle_mismatch")
    if candidate.get("trustLevel") != "T4":
        failures.append("trust_level_mismatch")

    source_hash = str(candidate.get("source_record_hash", ""))
    if not re.fullmatch(r"[a-fA-F0-9]{64}", source_hash):
        failures.append("source_record_hash_not_sha256_hex_64")

    backlink = str(candidate.get("source_of_record_backlink", ""))
    if not backlink.startswith("开发/"):
        failures.append("source_of_record_backlink_not_controlled_development_path")
    if candidate.get("kdsBacklink") != backlink:
        failures.append("kds_backlink_mismatch")

    waes_refs = set(candidate.get("waesGateRefs") or [])
    if REQUIRED_WAES_GATE not in waes_refs:
        failures.append("missing_required_waes_gate_ref")
    blockers = set(candidate.get("promotionBlockers") or [])
    if not REQUIRED_PROMOTION_BLOCKERS.issubset(blockers):
        failures.append("missing_required_promotion_blockers")

    if str(candidate.get("customer_order_original_or_platform_order_receipt", "")).startswith("llm://"):
        failures.append("llm_only_fact_claim")
    if str(candidate.get("customer_confirmed_product_spec", "")).startswith("llm://"):
        failures.append("llm_only_spec_claim")
    if str(candidate.get("delivery_requirement", "")).startswith("llm://"):
        failures.append("llm_only_delivery_claim")
    return failures


def candidate_files() -> list[Path]:
    files = []
    for pattern in ["gfis-was-real-source-record-candidate-*.json", "gfis-was-real-source-record-candidate-*.yaml"]:
        files.extend(INTAKE_DIR.glob(pattern))
    return sorted(path for path in files if path.name != TEMPLATE.name)


def load_candidate(path: Path) -> dict[str, Any]:
    if path.suffix == ".json":
        return load_json(path)
    return load_yaml(path)


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    template = load_yaml(TEMPLATE)
    previous = load_json(PREVIOUS_INTAKE_PACK)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-20260621", "invalid evidence id")
    require(evidence.get("status") == "was_real_source_record_candidate_precheck_pass_with_empty_hold", "invalid evidence status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001", "invalid round id")
    require(evidence.get("source_round") == previous.get("round_id"), "source round mismatch")
    require(evidence.get("project_group_coverage") == PROJECT_GROUP, "project group coverage mismatch")

    require(template.get("template_only") is True, "candidate template must be template_only")
    require(template.get("object_family") == "CustomerRequirementOrPlatformOrder", "template object family mismatch")
    require(template.get("project_group_scope") == PROJECT_GROUP, "template project group scope mismatch")
    require(set(template.get("required_source_kinds", [])) == ACCEPTED_SOURCE_KINDS, "template source kinds mismatch")
    require(set(evidence.get("required_inputs", [])) == {
        "real_customer_order_original_or_platform_order_receipt",
        "customer_confirmed_product_spec",
        "delivery_requirement",
        "issuing_party_and_owner_confirmation",
        "kds_source_backlink",
        "runtime_site_context",
    }, "P4 required inputs mismatch")
    require(set(evidence.get("gfis_native_required_fields", [])) == GFIS_NATIVE_FIELDS, "GFIS field set mismatch")
    require(set(evidence.get("was_required_fields", [])) == WAS_FIELDS, "WAS field set mismatch")

    positive_paths = sorted(FIXTURE_DIR.glob("p4-real-source-record-candidate-positive*.json"))
    negative_paths = sorted(FIXTURE_DIR.glob("p4-real-source-record-candidate-negative*.json"))
    require(len(positive_paths) == 1, "positive fixture count must be 1")
    require(len(negative_paths) == 4, "negative fixture count must be 4")

    positive_accepts = 0
    for path in positive_paths:
        fixture = load_json(path)
        require(fixture.get("fixture_only") is True, f"{path.name} must be fixture_only")
        failures = validate_candidate(fixture)
        require(not failures, f"{path.name} should pass but failed: {failures}")
        positive_accepts += 1

    negative_rejects = 0
    for path in negative_paths:
        fixture = load_json(path)
        require(fixture.get("fixture_only") is True, f"{path.name} must be fixture_only")
        failures = validate_candidate(fixture)
        require(failures, f"{path.name} should be rejected")
        negative_rejects += 1

    fixture_gate = evidence.get("fixture_gate", {})
    require(fixture_gate.get("positive_fixtures") == positive_accepts == 1, "positive fixture mismatch")
    require(fixture_gate.get("negative_fixtures") == negative_rejects == 4, "negative fixture mismatch")
    require(fixture_gate.get("expected_positive_acceptance") == 1, "expected positive acceptance mismatch")
    require(fixture_gate.get("expected_negative_rejection") == 4, "expected negative rejection mismatch")

    submitted = candidate_files()
    accepted = 0
    rejected = 0
    failures_by_file: dict[str, list[str]] = {}
    for path in submitted:
        failures = validate_candidate(load_candidate(path))
        if failures:
            rejected += 1
            failures_by_file[path.name] = failures
        else:
            accepted += 1

    scan = evidence.get("real_candidate_scan", {})
    require(scan.get("submitted_real_candidate_files") == len(submitted), "submitted candidate count mismatch")
    require(scan.get("candidate_files_checked") == len(submitted), "checked candidate count mismatch")
    require(scan.get("accepted_for_next_gate") == accepted, "accepted candidate count mismatch")
    require(scan.get("rejected_candidate_files") == rejected, "rejected candidate count mismatch")
    require(scan.get("hold_required") == (0 if accepted else 1), "hold_required mismatch")
    require(not failures_by_file, f"real candidates failed precheck: {failures_by_file}")

    boundary = evidence.get("boundary", {})
    for key in [
        "real_source_records",
        "valid_source_records",
        "runtime_primary_key_ready",
        "review_queue",
        "runtime_intake",
        "waes_review",
        "verified",
    ]:
        require(boundary.get(key) == 0, f"{key} must remain 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{key} must remain false")
    require(boundary.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")

    require(evidence.get("next_round") == "GPCF-ONTOLOGY-WAS-WAES-GATE-INPUT-CANDIDATE-001", "next round mismatch")
    require(evidence.get("next_round_condition") == "only_after_accepted_for_next_gate_greater_than_zero", "next condition mismatch")

    for phrase in [
        "预检结果为 `pass_with_empty_hold`",
        "submitted_real_candidate_files | `0`",
        "hold_required | `1`",
        "本 P4 precheck 面向整个 GlobalCloud 项目群",
        "本 evidence 不创建或标记",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("P4 candidate precheck 闭环已建立" in loop_round, "loop round missing feedback")

    print(
        "was_real_source_record_candidate_precheck=pass "
        f"positive_fixtures={positive_accepts} negative_fixtures={negative_rejects} "
        f"submitted_real_candidate_files={len(submitted)} candidate_files_checked={len(submitted)} "
        f"accepted_for_next_gate={accepted} hold_required={0 if accepted else 1} "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "waes_review=0 accepted=false integrated=false production_ready=false "
        "next_round_condition=only_after_accepted_for_next_gate_greater_than_zero"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
