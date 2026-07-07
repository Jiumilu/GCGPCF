#!/usr/bin/env python3
"""Create a GPCF 2.0 Feature Workspace."""

from __future__ import annotations

import argparse

from gpcf_feature_lib import ACTIVE, PRIORITIES, PROJECTS, default_feature, next_feature_id, render_journal, slugify, write_feature


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--priority", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--owner", default="agent-dev-01")
    args = parser.parse_args()

    project = args.project.lower()
    priority = args.priority.upper()
    if project not in PROJECTS:
        raise SystemExit(f"FAIL: unsupported project: {args.project}")
    if priority not in PRIORITIES:
        raise SystemExit(f"FAIL: unsupported priority: {args.priority}")

    feature_id = next_feature_id()
    slug = slugify(args.name)
    feature_dir = ACTIVE / f"{feature_id}-{slug}"
    if feature_dir.exists():
        raise SystemExit(f"FAIL: feature directory already exists: {feature_dir}")
    (feature_dir / "evidence").mkdir(parents=True)
    (feature_dir / "artifacts").mkdir(parents=True)
    (feature_dir / "evidence" / ".gitkeep").write_text("", encoding="utf-8")
    (feature_dir / "artifacts" / ".gitkeep").write_text("", encoding="utf-8")

    data = default_feature(
        feature_id=feature_id,
        name=args.name,
        project=project,
        goal=args.goal,
        owner=args.owner,
        priority=priority,
    )
    write_feature(feature_dir / "feature.yaml", data)
    (feature_dir / "journal.md").write_text(render_journal(feature_id, slug), encoding="utf-8")
    print(f"feature_created={feature_id} path={feature_dir.relative_to(ACTIVE.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
