#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "config/project-group-projects.yaml"
MATRIX = ROOT / "09-status/globalcloud-project-group-openspec-applicability-matrix.md"
VALID_POLICIES = {"required", "conditional", "waived"}
VALID_LOOPS = {"Delivery", "Governance"}


def main() -> int:
    failures: list[str] = []
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    projects = registry.get("projects", [])
    expected = {item["id"]: item["slug"] for item in projects}
    if registry.get("current_project_count") != 18 or len(expected) != 18:
        failures.append("project registry must contain exactly 18 unique current projects")

    text = MATRIX.read_text(encoding="utf-8")
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "项目 | slug" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 8 and cells[0] in expected:
            rows[cells[0]] = cells

    missing = sorted(set(expected) - set(rows))
    extra = sorted(set(rows) - set(expected))
    if missing:
        failures.append(f"matrix missing projects: {missing}")
    if extra:
        failures.append(f"matrix has unexpected projects: {extra}")

    policy_counts = {key: 0 for key in sorted(VALID_POLICIES)}
    for project, slug in expected.items():
        row = rows.get(project)
        if not row:
            continue
        _, actual_slug, policy, entry, feature, loop, evidence, harness = row
        if actual_slug != slug:
            failures.append(f"{project} slug mismatch: {actual_slug} != {slug}")
        if policy not in VALID_POLICIES:
            failures.append(f"{project} invalid policy: {policy}")
            continue
        policy_counts[policy] += 1
        if policy in {"required", "conditional"}:
            if f"openspec/changes/{slug}-<change>/" not in entry:
                failures.append(f"{project} missing central OpenSpec entry")
        elif not all(token in entry for token in ["reason=", "owner=", "review_condition=", "review_date="]):
            failures.append(f"{project} waiver is not governed")
        if f"--project {slug}" not in feature:
            failures.append(f"{project} missing Feature mapping")
        if loop not in VALID_LOOPS:
            failures.append(f"{project} invalid Loop mapping: {loop}")
        if evidence != "required" or harness != "required":
            failures.append(f"{project} must require Evidence and Harness handoff")

        status_path = ROOT / "projects" / slug / "STATUS.md"
        if not status_path.exists():
            failures.append(f"{project} missing STATUS.md")
            continue
        status = status_path.read_text(encoding="utf-8")
        required_markers = [
            "## OpenSpec 入口",
            f"- 策略：`{policy}`",
            f"- 中央入口：`openspec/changes/{slug}-<change>/`",
            f"- Feature：`python scripts/gpcf_new_feature.py --project {slug}`",
            f"- 默认 Loop：`{loop}`",
            "- Evidence/Harness：`required/required`",
        ]
        for marker in required_markers:
            if marker not in status:
                failures.append(f"{project} STATUS missing marker: {marker}")

    result = {
        "gate": "project_group_openspec_coverage",
        "status": "pass" if not failures else "fail",
        "current_project_count": len(expected),
        "matrix_project_count": len(rows),
        "policy_counts": policy_counts,
        "central_entry": "openspec/config.yaml",
        "feature_required": True,
        "evidence_required": True,
        "harness_handoff_required": True,
        "accepted_allowed": False,
        "integrated_allowed": False,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
