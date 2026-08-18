#!/usr/bin/env python3
"""Validate the localization boundary for immutable Feature evidence."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GATE = ROOT / "tools/kds-sync/check_chinese_localization_gate.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"localization_feature_evidence_boundary=fail reason={message}")


def load_gate():
    spec = importlib.util.spec_from_file_location("localization_gate_boundary_test", GATE)
    require(spec is not None and spec.loader is not None, "gate_import_unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_markdown(root: Path, source_path: str) -> None:
    path = root / source_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# English only replay material\n\n"
        "This sentence intentionally contains enough English words to trigger the localization scanner today.\n",
        encoding="utf-8",
    )


def main() -> int:
    gate = load_gate()
    with tempfile.TemporaryDirectory(prefix="gpcf-localization-boundary-") as temp_dir:
        root = Path(temp_dir)
        excluded = {
            "features/active/F-TEST/evidence/replay.md",
            "features/done/F-DONE/evidence/replay.md",
            "docs/harness/evidence/replay.md",
        }
        included = {
            "features/active/F-TEST/artifacts/current.md",
            "features/active/F-TEST/journal.md",
            "03-data-ai-knowledge/current.md",
        }
        for source_path in excluded | included:
            write_markdown(root, source_path)

        gate.ROOT = root
        scanned = {gate.rel(path) for path in gate.iter_docs()}

        require(not (excluded & scanned), f"excluded_paths_scanned:{sorted(excluded & scanned)}")
        require(included <= scanned, f"current_paths_missing:{sorted(included - scanned)}")
        require(
            all(gate.doc_findings(root / source_path) for source_path in included),
            "included_paths_not_evaluated",
        )

    print("localization_feature_evidence_boundary=pass")
    print("immutable_feature_evidence_scanned=false")
    print("feature_journal_and_artifacts_scanned=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
