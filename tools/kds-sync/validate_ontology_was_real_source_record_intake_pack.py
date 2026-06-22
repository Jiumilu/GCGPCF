#!/usr/bin/env python3
"""Validate the WAS/Ontology real source-record intake package."""

from __future__ import annotations

import fnmatch
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
GFIS_RECEIVING_DIR = Path(
    "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/"
    "docs/harness/sop-e2e/intake-submissions/runtime-primary-key-source-records/"
    "customer-requirement-or-platform-order"
)

EVIDENCE_JSON = ROOT / "docs/harness/evidence/ontology-was-real-source-record-intake-pack-20260621.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/ontology-was-real-source-record-intake-pack-20260621.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001.md"
P3_JSON = ROOT / "docs/harness/evidence/ontology-was-3h-p3-closure-20260621.json"

ALLOWED_NON_REAL_PATTERNS = [
    "README.md",
    "*.template.json",
    "pending-business-verification/README.md",
    "pending-business-verification/*.schema.json",
    "rejected-examples/*.customer-requirement-platform-order.source-record.json",
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


def is_allowed_non_real_file(path: Path) -> bool:
    rel = path.relative_to(GFIS_RECEIVING_DIR).as_posix()
    return any(fnmatch.fnmatch(rel, pattern) for pattern in ALLOWED_NON_REAL_PATTERNS)


def count_real_source_record_files() -> int:
    require(GFIS_RECEIVING_DIR.exists(), f"GFIS receiving directory missing: {GFIS_RECEIVING_DIR}")
    count = 0
    for path in GFIS_RECEIVING_DIR.rglob("*"):
        if not path.is_file() or is_allowed_non_real_file(path):
            continue
        if path.name.endswith(".customer-requirement-platform-order.source-record.json"):
            count += 1
    return count


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    p3 = load_json(P3_JSON)
    evidence_md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)

    require_frontmatter(EVIDENCE_MD, evidence_md)
    require_frontmatter(LOOP_ROUND, loop_round)

    require(evidence.get("evidence_id") == "ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-20260621", "invalid evidence id")
    require(evidence.get("status") == "ontology_was_real_source_record_intake_pack_ready", "invalid status")
    require(evidence.get("round_id") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-INTAKE-PACK-001", "invalid round id")
    require(evidence.get("source_round") == p3.get("round_id"), "source round mismatch")
    require(evidence.get("target_owner") == "GPC_or_Liaoning_Yuanhang_order_owner", "target owner mismatch")
    require(evidence.get("target_object_family") == "CustomerRequirementOrPlatformOrder", "target object family mismatch")
    require(evidence.get("accepted_source_kinds") == ["customer_order_original", "platform_order_receipt"], "accepted source kinds mismatch")

    package = evidence.get("intake_package", {})
    items = package.get("required_original_artifacts", [])
    require(package.get("package_items") == len(items) == 6, "package item count mismatch")
    require(len(evidence.get("required_gfis_native_fields", [])) == 12, "GFIS native field count mismatch")
    require(len(evidence.get("required_was_fields", [])) == 12, "WAS field count mismatch")
    require(len(evidence.get("pre_submit_self_check", [])) == 10, "pre-submit self-check count mismatch")
    require(len(evidence.get("explicit_blocked_promotions", [])) == 8, "blocked promotion count mismatch")

    naming = evidence.get("file_naming_rule", {})
    require(naming.get("required_suffix") == ".customer-requirement-platform-order.source-record.json", "required suffix mismatch")
    require(naming.get("template_files_must_not_count") is True, "template files must not count")
    require(naming.get("rejected_examples_must_not_count") is True, "rejected examples must not count")

    boundary = evidence.get("current_boundary", {})
    require(boundary.get("gfis_real_source_record_files") == count_real_source_record_files() == 0, "GFIS real source-record files must be 0")
    require(boundary.get("submitted_files_found") == 0, "submitted files must be 0")
    require(boundary.get("accepted_for_next_gate") == 0, "accepted_for_next_gate must be 0")
    require(boundary.get("hold_required") == 1, "hold_required must be 1")
    require(boundary.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")
    for key in [
        "real_source_records",
        "valid_source_records",
        "runtime_primary_key_ready",
        "review_queue",
        "runtime_intake",
        "waes_review",
        "verified",
    ]:
        require(boundary.get(key) == 0, f"{key} must be 0")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{key} must be false")

    next_gate = evidence.get("next_gate_after_owner_submission", {})
    require(next_gate.get("next_round") == "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001", "next round mismatch")
    require("validate_gfis_was_source_record_submission_precheck.py" in next_gate.get("required_command", ""), "missing required precheck command")
    require(len(next_gate.get("additional_required_commands", [])) == 3, "additional command count mismatch")

    for phrase in [
        "gfis_real_source_record_files | `0`",
        "hold_required | `1`",
        "IP-001",
        "GFIS 原生字段 12 个",
        "WAS 字段 12 个",
        "GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001",
    ]:
        require(phrase in evidence_md, f"evidence markdown missing phrase: {phrase}")
    require("真实 source-record intake package 已建立" in loop_round, "loop round missing feedback")

    print(
        "ontology_was_real_source_record_intake_pack=pass "
        "package_items=6 gfis_native_fields=12 was_fields=12 pre_submit_self_check=10 "
        "blocked_promotions=8 gfis_real_source_record_files=0 hold_required=1 "
        "real_source_records=0 valid_source_records=0 runtime_primary_key_ready=0 "
        "accepted=false integrated=false production_ready=false "
        "next_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-CANDIDATE-PRECHECK-001"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
