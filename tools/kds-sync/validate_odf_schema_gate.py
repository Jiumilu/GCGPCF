#!/usr/bin/env python3
"""Validate ODF sample ledgers and metadata envelopes.

This gate is intentionally read-only. It validates metadata envelopes without
copying source document bodies, writing to KDS, or changing rollout status.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGERS = [
    ROOT / "docs/harness/evidence/odf-pilot-sample-ledger-20260617.json",
    ROOT / "docs/harness/evidence/odf-phase2-sample-ledger-20260617.json",
    ROOT / "docs/harness/evidence/odf-phase4-small-batch-ledger-20260617.json",
]
REQUIRED_FIELDS = {
    "source_uri",
    "source_hash",
    "odf_hash",
    "markdown_hash",
    "conversion_method",
    "conversion_actor",
    "owner",
    "source_path",
    "kds_path",
    "sensitivity_check",
    "status",
    "rollback_hint",
}
ALLOWED_LEDGER_STATUSES = {"pilot_closed", "phase2_closed", "phase4_small_batch_closed"}
ALLOWED_SAMPLE_STATUSES = {"pilot_sample", "phase2_sample", "phase4_sample"}
FORBIDDEN_STATUS_MARKERS = {"full_rollout", "accepted", "integrated"}
REQUIRED_BOUNDARY_FLAGS = {
    "does_not_replace_git",
    "does_not_replace_kds",
    "does_not_replace_okf",
    "does_not_replace_loop_evidence",
}
ENVELOPE_FIELDS_MATCH_LEDGER = REQUIRED_FIELDS - {"odf_hash"}


def fail(reason: str) -> None:
    raise SystemExit(f"odf_schema_gate=fail reason={reason}")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"missing_ledger:{rel(path)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid_json:{rel(path)}:{exc}")


def require_sample(sample: dict, ledger_path: Path, seen_sample_ids: set[str]) -> dict:
    sample_id = sample.get("sample_id", "")
    if not sample_id:
        fail(f"missing_sample_id:{rel(ledger_path)}")
    if sample_id in seen_sample_ids:
        fail(f"duplicate_sample_id:{sample_id}")
    seen_sample_ids.add(sample_id)

    missing = sorted(REQUIRED_FIELDS - sample.keys())
    if missing:
        fail(f"missing_fields:{sample_id}:{','.join(missing)}")

    if sample["conversion_method"] != "metadata-envelope-only":
        fail(f"invalid_conversion_method:{sample_id}")
    if sample["conversion_actor"] != "codex":
        fail(f"invalid_conversion_actor:{sample_id}")
    if not str(sample["sensitivity_check"]).startswith("pass_"):
        fail(f"sensitivity_check_not_pass:{sample_id}")
    if sample["status"] not in ALLOWED_SAMPLE_STATUSES:
        fail(f"invalid_sample_status:{sample_id}:{sample['status']}")
    if sample["status"] in FORBIDDEN_STATUS_MARKERS:
        fail(f"forbidden_sample_status:{sample_id}:{sample['status']}")
    if not str(sample["kds_path"]).startswith("开发/"):
        fail(f"kds_path_not_development_space:{sample_id}")

    source_path = ROOT / sample["source_path"]
    odf_path = ROOT / sample["odf_path"]
    if not source_path.exists():
        fail(f"missing_source:{sample_id}:{sample['source_path']}")
    if not odf_path.exists():
        fail(f"missing_odf:{sample_id}:{sample['odf_path']}")

    source_hash = sha256_file(source_path)
    odf_hash = sha256_file(odf_path)
    if source_hash != sample["source_hash"]:
        fail(f"source_hash_mismatch:{sample_id}")
    if source_hash != sample["markdown_hash"]:
        fail(f"markdown_hash_mismatch:{sample_id}")
    if odf_hash != sample["odf_hash"]:
        fail(f"odf_hash_mismatch:{sample_id}")

    odf = load_json(odf_path)
    for field in ENVELOPE_FIELDS_MATCH_LEDGER:
        if odf.get(field) != sample.get(field):
            fail(f"ledger_odf_field_mismatch:{sample_id}:{field}")
    if odf.get("source_path") != sample["source_path"]:
        fail(f"odf_source_path_mismatch:{sample_id}")
    if odf.get("kds_path") != sample["kds_path"]:
        fail(f"odf_kds_path_mismatch:{sample_id}")

    boundary = odf.get("boundary", {})
    missing_boundary = sorted(flag for flag in REQUIRED_BOUNDARY_FLAGS if boundary.get(flag) is not True)
    if missing_boundary:
        fail(f"missing_boundary_flags:{sample_id}:{','.join(missing_boundary)}")

    return {
        "sample_id": sample_id,
        "source_path": sample["source_path"],
        "kds_path": sample["kds_path"],
        "category": sample.get("category", "pilot"),
    }


def main() -> int:
    seen_sample_ids: set[str] = set()
    seen_sources: set[str] = set()
    seen_odf_paths: set[str] = set()
    source_overlaps: set[str] = set()
    categories: set[str] = set()
    ledger_statuses: list[str] = []
    samples: list[dict] = []

    for ledger_path in LEDGERS:
        ledger = load_json(ledger_path)
        status = ledger.get("status", "")
        if status not in ALLOWED_LEDGER_STATUSES:
            fail(f"invalid_ledger_status:{rel(ledger_path)}:{status}")
        if status in FORBIDDEN_STATUS_MARKERS:
            fail(f"forbidden_ledger_status:{rel(ledger_path)}:{status}")
        ledger_statuses.append(status)
        ledger_samples = ledger.get("samples", [])
        if not isinstance(ledger_samples, list) or not ledger_samples:
            fail(f"empty_samples:{rel(ledger_path)}")
        for sample in ledger_samples:
            validated = require_sample(sample, ledger_path, seen_sample_ids)
            if sample["source_path"] in seen_sources:
                source_overlaps.add(sample["source_path"])
            if sample["odf_path"] in seen_odf_paths:
                fail(f"duplicate_odf_path:{sample['odf_path']}")
            seen_sources.add(sample["source_path"])
            seen_odf_paths.add(sample["odf_path"])
            categories.add(validated["category"])
            samples.append(validated)

    print(
        "odf_schema_gate=pass "
        f"ledgers={len(LEDGERS)} "
        f"samples={len(samples)} "
        f"ledger_statuses={','.join(ledger_statuses)} "
        f"categories={','.join(sorted(categories))} "
        "source_hash=pass markdown_hash=pass odf_hash=pass "
        f"source_overlaps={len(source_overlaps)} "
        "duplicate_sample_ids=0 duplicate_odf_paths=0 forbidden_rollout=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
