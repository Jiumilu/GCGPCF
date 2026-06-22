#!/usr/bin/env python3
"""Validate the GFIS receiving-directory precheck for WAS source-record fields."""

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

EVIDENCE_JSON = ROOT / "docs/harness/evidence/gfis-was-source-record-submission-precheck-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/gfis-was-source-record-submission-precheck-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GFIS-WAS-SOURCE-RECORD-PRECHECK-001.md"
ADMISSION_GATE = ROOT / "docs/harness/evidence/gfis-was-source-record-admission-gate-20260621.json"
WAS_PROFILE = WAS_ROOT / "okf/examples/gfis-runtime-sop-e2e-was-profile.yaml"
GFIS_SCAN = GFIS_ROOT / "docs/harness/sop-e2e/evidence/gfis-customer-requirement-platform-order-source-record-scan.json"
RECEIVING_DIR = GFIS_ROOT / "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/customer-requirement-or-platform-order"
TEMPLATE = RECEIVING_DIR / "customer-requirement-platform-order.source-record.template.json"
EXPECTED_SUFFIX = ".customer-requirement-platform-order.source-record.json"

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
ZERO_RESULT_KEYS = [
    "real_source_records",
    "valid_source_records",
    "runtime_primary_key_ready",
    "review_queue",
    "runtime_intake",
    "waes_review",
    "verified",
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


def is_placeholder(value: Any) -> bool:
    if value in (None, "", [], {}):
        return True
    if isinstance(value, str) and value.strip().startswith("<"):
        return True
    return False


def validate_future_candidate(candidate: dict[str, Any], s01: dict[str, Any]) -> list[str]:
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
    return failures


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    admission_gate = load_json(ADMISSION_GATE)
    profile = load_yaml(WAS_PROFILE)
    gfis_scan = load_json(GFIS_SCAN)
    template = load_json(TEMPLATE)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    stages = profile.get("stages")
    require(isinstance(stages, list), "WAS stages must be a list")
    s01 = next((stage for stage in stages if stage.get("stageId") == "S01-customer-requirement-or-platform-order"), None)
    require(isinstance(s01, dict), "missing WAS S01 stage")

    require(evidence.get("evidence_id") == "GFIS-WAS-SOURCE-RECORD-SUBMISSION-PRECHECK-20260621", "invalid evidence id")
    require(evidence.get("status") == "gfis_was_source_record_submission_precheck_pass_with_empty_hold", "invalid evidence status")
    require(evidence.get("scope", {}).get("precheck_type") == "read_only_directory_scan_and_future_submission_gate", "precheck type mismatch")
    require(admission_gate.get("status") == "gfis_was_source_record_admission_gate_pass", "admission gate must pass")

    for source_name, source_path in evidence.get("sources", {}).items():
        require(Path(source_path).exists(), f"source missing for {source_name}: {source_path}")
    require(RECEIVING_DIR.exists() and RECEIVING_DIR.is_dir(), "GFIS receiving directory missing")
    require(template.get("template_only") is True, "GFIS source-record template must remain template_only")

    require(set(evidence.get("gfis_native_required_fields", [])) == GFIS_NATIVE_FIELDS, "GFIS native field set mismatch")
    require(set(evidence.get("was_required_fields", [])) == WAS_FIELDS, "WAS field set mismatch")
    required_values = evidence.get("required_was_values", {})
    require(required_values.get("objectFamily") == "CustomerRequirementOrPlatformOrder", "required objectFamily mismatch")
    require(required_values.get("assetDimension") == s01.get("assetDimension") == "data_asset", "required assetDimension mismatch")
    require(required_values.get("flowType") == s01.get("flowType") == "commerce_flow", "required flowType mismatch")
    require(required_values.get("lifecycle") == s01.get("lifecycle") == "pending_business_verification", "required lifecycle mismatch")
    require(required_values.get("trustLevel") == s01.get("trustLevel") == "T4", "required trustLevel mismatch")

    files = sorted(path for path in RECEIVING_DIR.glob(f"*{EXPECTED_SUFFIX}") if path.name != TEMPLATE.name)
    failures_by_file: dict[str, list[str]] = {}
    gfis_valid = 0
    was_valid = 0
    accepted = 0
    for path in files:
        candidate = load_json(path)
        failures = validate_future_candidate(candidate, s01)
        failures_by_file[path.name] = failures
        if not any(item.startswith("missing_gfis_field:") for item in failures):
            gfis_valid += 1
        if not any(item.startswith("missing_was_field:") for item in failures):
            was_valid += 1
        if not failures:
            accepted += 1

    scan = evidence.get("directory_scan", {})
    require(scan.get("expected_suffix") == EXPECTED_SUFFIX, "expected suffix mismatch")
    require(scan.get("template_files_excluded") == 1, "template exclusion mismatch")
    require(scan.get("submitted_files_found") == len(files), "submitted file count mismatch")
    require(scan.get("candidate_files_checked") == len(files), "candidate file count mismatch")
    require(scan.get("gfis_native_field_valid_submissions") == gfis_valid, "GFIS valid submission count mismatch")
    require(scan.get("was_field_valid_submissions") == was_valid, "WAS valid submission count mismatch")
    require(scan.get("accepted_for_next_gate") == accepted, "accepted submission count mismatch")
    require(scan.get("hold_required") == (0 if accepted else 1), "hold_required mismatch")
    require(not failures_by_file, f"future candidates failed precheck: {failures_by_file}")

    gfis_counts = gfis_scan.get("counts", {})
    require(gfis_counts.get("submitted_files_found") == 0, "GFIS scan submitted files must remain 0")
    require(gfis_counts.get("valid_source_records") == 0, "GFIS valid source records must remain 0")
    require(gfis_counts.get("runtime_primary_key_ready") == 0, "runtime primary key must remain 0")

    result = evidence.get("admission_result", {})
    for key in ZERO_RESULT_KEYS:
        require(result.get(key) == 0, f"admission_result.{key} must be 0")

    for phrase in [
        "预检结果为 `pass_with_empty_hold`",
        "GFIS 原生 source-record 字段 12 项齐全",
        "WAS/Ontology 字段 12 项齐全",
        "本 evidence 不升级 accepted、integrated 或 production_ready",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("GFIS source-of-record 接收目录已经具备 WAS/Ontology 提交前扫描基线" in loop_round, "loop round missing feedback")

    print(
        "gfis_was_source_record_submission_precheck=pass "
        f"submitted_files_found={len(files)} candidate_files_checked={len(files)} "
        f"gfis_native_fields=12 was_fields=12 accepted_for_next_gate={accepted} "
        f"hold_required={0 if accepted else 1} real_source_records=0 valid_source_records=0 "
        "runtime_primary_key_ready=0 review_queue=0 runtime_intake=0 waes_review=0 verified=0 "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
