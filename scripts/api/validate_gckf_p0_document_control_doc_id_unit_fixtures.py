#!/usr/bin/env python3
"""Unit-level fixtures for document_control.py doc_id preservation behavior."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_CONTROL = REPO_ROOT / "tools/kds-sync/document_control.py"


def load_document_control():
    spec = importlib.util.spec_from_file_location("document_control_under_test", DOCUMENT_CONTROL)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load document_control.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    module = load_document_control()
    with tempfile.TemporaryDirectory(prefix="gckf-doc-control-fixtures-") as tmp:
        root = Path(tmp)
        module.ROOT = root
        module.TODAY = "2026-06-22"

        fixed_path = root / "fixed.md"
        missing_path = root / "missing.md"
        external_path = root / "external.md"

        fixed_text = """---
doc_id: GPCF-DOC-FIXED-UNIT
title: Fixed ID Fixture
project: GPCF
---

# Fixed ID Fixture
"""
        missing_text = "# Missing ID Fixture\n"
        external_text = """---
doc_control: external
doc_id: GPCF-DOC-EXTERNAL-UNIT
title: External Fixture
---

# External Fixture
"""
        write(fixed_path, fixed_text)
        write(missing_path, missing_text)
        write(external_path, external_text)

        records = {record["source_path"]: record for record in module.build_records([fixed_path, missing_path, external_path])}
        if records["fixed.md"]["doc_id"] != "GPCF-DOC-FIXED-UNIT":
            failures.append("fixed_frontmatter_doc_id_not_preserved")
        if records["missing.md"]["doc_id"] != module.doc_id("missing.md"):
            failures.append("missing_doc_id_did_not_fallback_to_path_hash")
        if records["external.md"]["doc_id"] != "GPCF-DOC-EXTERNAL-UNIT":
            failures.append("external_doc_id_not_seen_in_build_records")

        before_external = external_path.read_text(encoding="utf-8")
        module.apply_frontmatter([records["fixed.md"], records["missing.md"], records["external.md"]])
        after_external = external_path.read_text(encoding="utf-8")
        if before_external != after_external:
            failures.append("external_frontmatter_was_rewritten")

        fixed_after = fixed_path.read_text(encoding="utf-8")
        missing_after = missing_path.read_text(encoding="utf-8")
        if "doc_id: GPCF-DOC-FIXED-UNIT" not in fixed_after:
            failures.append("fixed_doc_id_not_preserved_after_apply_frontmatter")
        if f"doc_id: {module.doc_id('missing.md')}" not in missing_after:
            failures.append("missing_doc_id_fallback_not_written_after_apply_frontmatter")

    if failures:
        print("gckf_p0_document_control_doc_id_unit_fixtures=fail")
        for failure in failures:
            print(failure)
        return 1

    print("gckf_p0_document_control_doc_id_unit_fixtures=pass")
    print("fixed_frontmatter_doc_id=preserved")
    print("missing_doc_id_fallback=path_hash")
    print("external_frontmatter=rewrite_skipped")
    print("execution_mode=tempdir_no_repo_write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
