#!/usr/bin/env python3
"""Validate that document_control.py preserves controlled frontmatter doc_id values."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DOCUMENT_CONTROL = ROOT / "tools/kds-sync/document_control.py"

OLD_IDS = {
    "GPCF-DOC-069DA1E028",
    "GPCF-DOC-870A0125E6",
    "GPCF-DOC-6A430F4A1E",
    "GPCF-DOC-F0A8F5191A",
    "GPCF-DOC-DFF3FFF2C7",
    "GPCF-DOC-8F5452F243",
    "GPCF-DOC-CBE91779AA",
    "GPCF-DOC-D77F85A0E5",
    "GPCF-DOC-61E3279D97",
    "GPCF-DOC-A8FBEBC228",
    "GPCF-DOC-627B373BE2",
    "GPCF-DOC-5A1131B14C",
    "GPCF-DOC-2D844CAF91",
    "GPCF-DOC-7B80D4EE72",
    "GPCF-DOC-6F7C536867",
    "GPCF-DOC-BCF513285F",
}

REQUIRED_FIXED_IDS = {
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRCOMPLETENESSPRECHECKV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRINTAKEACKV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGDELIVERYPRECHECKV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGREPAIROWNERNOTIFICATIONV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGREPAIROWNERNOTIFICATIONACKRECEIPTV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGREPAIROWNERNOTIFICATIONACKRECEIPTAGGREGATIONV01",
    "GPCF-DOC-GCKFCOMMITTEEACCEPTACKNOTIFICATIONRECEIPTAGGREGATIONREPAIRACKROUTINGREPAIROWNERNOTIFICATIONACKRECEIPTAGGREGATIONCOMPLETENESSPRECHECKV01",
    "GPCF-LOOP-GCKF-P0-D75-001",
    "GPCF-LOOP-GCKF-P0-D76-001",
    "GPCF-LOOP-GCKF-P0-D77-001",
    "GPCF-LOOP-GCKF-P0-D78-001",
    "GPCF-LOOP-GCKF-P0-D79-001",
    "GPCF-LOOP-GCKF-P0-D80-001",
    "GPCF-LOOP-GCKF-P0-D81-001",
    "GPCF-LOOP-GCKF-P0-D82-001",
}

SCAN_PATHS = [
    ROOT / "docs",
    ROOT / "09-status",
    ROOT / ".kds/development-space",
]


def all_markdown_text() -> str:
    parts: list[str] = []
    for base in SCAN_PATHS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(parts)


def main() -> int:
    failures: list[str] = []
    source = DOCUMENT_CONTROL.read_text(encoding="utf-8")
    if "def controlled_doc_id(" not in source:
        failures.append("missing_controlled_doc_id_function")
    if '"doc_id": controlled_doc_id(source_path, existing)' not in source:
        failures.append("build_records_not_using_controlled_doc_id")

    corpus = all_markdown_text()
    old_hits = sorted(old_id for old_id in OLD_IDS if old_id in corpus)
    missing_fixed = sorted(fixed_id for fixed_id in REQUIRED_FIXED_IDS if fixed_id not in corpus)
    if old_hits:
        failures.append("old_short_doc_ids_present:" + ",".join(old_hits))
    if missing_fixed:
        failures.append("fixed_doc_ids_missing:" + ",".join(missing_fixed))

    if failures:
        print("gckf_p0_document_control_preserves_fixed_doc_id=fail")
        for failure in failures:
            print(failure)
        return 1

    print("gckf_p0_document_control_preserves_fixed_doc_id=pass")
    print("frontmatter_doc_id_preservation=covered")
    print("old_short_doc_ids_present=0")
    print("fixed_doc_ids_present=16")
    print("execution_mode=read_only_validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
