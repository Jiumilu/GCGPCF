#!/usr/bin/env python3
"""Validate PVAOS release review evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/PVAOS/evidence/pvaos-release-review-20260625.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
STATUS_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
DEPENDENCY_MATRIX = ROOT / "docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md"

REQUIRED_DOC_TOKENS = [
    "PVAOS-RELEASE-REVIEW-001",
    "pvaos_release_review = pass",
    "pvaos_status_candidate | `review_candidate`",
    "release_gate_status | `verified_with_local_release_gate_boundary`",
    "playwright_passed | 50",
    "playwright_skipped | 4",
    "vitest_files_passed | 80",
    "vitest_tests_passed | 547",
    "production_domain | `pvaos.csydsc.com`",
    "production_domain_probe | `pass`",
    "remote_ci | `false`",
    "pr_created | `false`",
    "merged | `false`",
    "production_release | `false`",
    "customer_accepted | `false`",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "pvaos-release-review-20260625.md",
    "validate_pvaos_release_review.py",
    "PVAOS-RELEASE-REVIEW-001",
    "review_candidate",
]

FORBIDDEN_CLAIMS = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "remote_ci = true",
    "pr_created = true",
    "merged = true",
    "production_release = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    refs_text = "\n".join(
        [
            read(REGISTER, failures),
            read(BOARD, failures),
            read(STATUS_MATRIX, failures),
            read(DEPENDENCY_MATRIX, failures),
        ]
    )

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in PVAOS release review evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for claim in FORBIDDEN_CLAIMS:
        if claim in combined:
            failures.append(f"forbidden positive claim: {claim}")

    result = {
        "gate": "pvaos_release_review",
        "status": "pass" if not failures else "fail",
        "candidate_status": "review_candidate" if not failures else "failed",
        "failures": failures,
        "warnings": [
            "This validates local PVAOS release review evidence only; it does not prove remote CI, PR, merge, production release, accepted, integrated, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
