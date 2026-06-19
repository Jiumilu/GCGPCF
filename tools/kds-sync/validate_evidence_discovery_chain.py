#!/usr/bin/env python3
"""Report evidence discovery drift across README, local index, and KDS mirror.

This validator is intentionally report-only by default. A KDS mirror lag is a
governance review signal, not proof that business status changed.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "docs/harness/evidence/README.md"
HARNESS_README = ROOT / "docs/harness/README.md"
LOCAL_INDEX = ROOT / "docs/harness/evidence/evidence-index.md"
MIRROR_INDEX = ROOT / ".kds/development-space/开发/12-GPCF/docs/harness/evidence/evidence-index.md"

TRACKED_PREFIXES = (
    "docs/harness/evidence/base-knowledge-",
    "docs/harness/evidence/kds-md-okf-odf-",
    "docs/harness/evidence/kds-phase10-",
    "docs/harness/evidence/odf-phase",
)


def read(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def extract_paths(text: str) -> set[str]:
    paths = set()
    for match in re.finditer(r"docs/harness/evidence/[^\s|`]+\.md", text):
        path = match.group(0)
        if path.startswith(TRACKED_PREFIXES):
            paths.add(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero when any discovery-chain drift is found",
    )
    args = parser.parse_args()

    readme_paths = extract_paths(read(README))
    harness_readme_paths = extract_paths(read(HARNESS_README))
    required_paths = sorted(readme_paths | harness_readme_paths)
    local_index_text = read(LOCAL_INDEX)
    mirror_index_text = read(MIRROR_INDEX)

    missing_local = [path for path in required_paths if path not in local_index_text]
    missing_mirror = [path for path in required_paths if path not in mirror_index_text]

    status = "pass" if not missing_local and not missing_mirror else "review_required"
    print(
        "evidence_discovery_chain="
        f"{status} required={len(required_paths)} "
        f"missing_local={len(missing_local)} missing_mirror={len(missing_mirror)} "
        "business_status_impact=none"
    )
    if missing_local:
        print("missing_local:")
        for path in missing_local:
            print(f"- {path}")
    if missing_mirror:
        print("missing_mirror:")
        for path in missing_mirror:
            print(f"- {path}")
    print("non_claims=does_not_prove_real_kds_writeback_or_accepted_integrated")

    if args.strict and (missing_local or missing_mirror):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
