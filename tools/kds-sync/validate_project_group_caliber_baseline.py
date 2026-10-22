#!/usr/bin/env python3
"""Validate the GlobalCloud project-group caliber baseline (PG-01).

Checks:
1. config/project-group-projects.yaml declares current_project_count = 29.
2. 09-status/globalcloud-project-group-caliber-baseline-v1.0.md exists and
   carries the frozen caliber tokens.
3. The 11 legacy-17 projects are explicitly enumerated as in-scope for the
   29-project gate denominator.
4. No positive state-promotion claim (accepted/integrated/production_ready/
   customer_accepted) is present.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "config/project-group-projects.yaml"
DOC = ROOT / "09-status/globalcloud-project-group-caliber-baseline-v1.0.md"

REQUIRED_TOKENS = [
    "project_group_caliber_baseline_v1_0 = controlled",
    "project_count = 29",
    "project_count_source = config/project-group-projects.yaml",
    "dirty_source = single_live_git_status",
    "gate_denominator = 29",
    "legacy_gate_denominator_deprecated = 17, 20",
    "deprecated_dirty_values = 3, 5, 7, 21, 22",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

LEGACY_17_OUT_OF_SCOPE = [
    "ICP",
    "PQC",
    "SpaceAI",
    "SpaceAI Studio",
    "World",
    "GCMEM",
    "WAE",
    "Project(PMC)",
    "PDC",
    "SLC",
    "DRC",
]

FORBIDDEN_POSITIVE = [
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]


def fail(msg: str) -> int:
    print(f"project_group_caliber_baseline = fail")
    print(f"reason = {msg}")
    return 1


def main() -> int:
    if not CONFIG.exists():
        return fail(f"missing config: {CONFIG}")
    if not DOC.exists():
        return fail(f"missing baseline doc: {DOC}")

    config_text = CONFIG.read_text(encoding="utf-8")
    m = re.search(r"current_project_count:\s*(\d+)", config_text)
    if not m:
        return fail("current_project_count not found in config")
    if m.group(1) != "29":
        return fail(f"config current_project_count is {m.group(1)}, expected 29")

    doc = DOC.read_text(encoding="utf-8")
    missing = [t for t in REQUIRED_TOKENS if t not in doc]
    if missing:
        return fail("baseline doc missing tokens: " + "; ".join(missing))

    miss_projects = [p for p in LEGACY_17_OUT_OF_SCOPE if p not in doc]
    if miss_projects:
        return fail("legacy-17 out-of-scope projects not enumerated: " + ", ".join(miss_projects))

    forbidden = [t for t in FORBIDDEN_POSITIVE if t in doc]
    if forbidden:
        return fail("forbidden positive claims: " + "; ".join(forbidden))

    print("project_group_caliber_baseline = pass")
    print("project_count = 29")
    print("gate_denominator = 29")
    print("legacy_17_out_of_scope_projects = 11")
    print("deprecated_dirty_values = 3,5,7,21,22")
    print("deprecated_project_counts = 17,20")
    print("accepted = false")
    print("integrated = false")
    print("production_ready = false")
    print("customer_accepted = false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
