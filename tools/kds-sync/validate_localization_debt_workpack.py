#!/usr/bin/env python3
"""Validate the localization debt workpack evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/localization-debt-workpack-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/localization-debt-workpack-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D88-001.md"
BUILDER = ROOT / "tools/kds-sync/build_localization_debt_workpack.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, object]:
    data = json.loads(read(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return data


def require_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing frontmatter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} invalid frontmatter")
    meta = text[:end]
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {path.relative_to(ROOT).as_posix()}",
        "sync_direction: bidirectional",
        "last_reviewed: 2026-06-22",
    ]:
        require(phrase in meta, f"{path.relative_to(ROOT)} missing marker: {phrase}")


def current_localization_summary() -> dict[str, object]:
    result = subprocess.run(
        [
            sys.executable,
            "tools/kds-sync/check_chinese_localization_gate.py",
            "--json",
            "--max-findings",
            "10000",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        summary = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL: localization gate output is not JSON: {exc}") from exc
    require(isinstance(summary, dict), "localization summary must be object")
    return summary


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    builder = read(BUILDER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    for phrase in ["run_localization_gate", "work_items", "no_write_boundary", "gfis_real_business_lane"]:
        require(phrase in builder, f"builder missing marker: {phrase}")

    summary = current_localization_summary()
    require(evidence.get("evidence_id") == "LOCALIZATION-DEBT-WORKPACK-20260622", "invalid evidence id")
    require(evidence.get("localization_gate") == "fail", "evidence localization gate must fail")
    require(summary.get("localization_gate") == "fail", "current localization gate must still fail")
    require(int(evidence.get("docs_checked", 0)) > 0, "evidence docs_checked must be positive")
    require(int(evidence.get("software_files_checked", 0)) > 0, "evidence software_files_checked must be positive")
    require(int(evidence.get("findings", 0)) > 0, "evidence findings must be positive")
    require(int(summary.get("findings", 0)) > 0, "current findings must be positive")
    work_items = evidence.get("work_items")
    require(isinstance(work_items, list), "work_items must be list")
    require(evidence.get("work_item_count") == len(work_items), "work_item_count mismatch")
    require(evidence.get("bucket_count") == len(work_items), "bucket_count should match work item count")
    require(evidence.get("findings", 0) >= evidence.get("work_item_count", 0), "findings must cover work items")

    boundary = evidence.get("known_boundary", {})
    require(isinstance(boundary, dict), "known_boundary must be object")
    require(boundary.get("candidate_no_write") is True, "candidate_no_write must remain true")
    require(boundary.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{key} must remain false")

    for item in work_items:
        require(isinstance(item, dict), "work item must be object")
        for key in ["workpack_id", "bucket", "finding_count", "dominant_kind", "priority", "status", "repair_policy"]:
            require(key in item, f"work item missing {key}")
        no_write = item.get("no_write_boundary", {})
        require(isinstance(no_write, dict), "no_write_boundary must be object")
        for key in ["bulk_rewrite", "business_writeback", "real_kds_api_write", "status_upgrade"]:
            require(no_write.get(key) is False, f"{item['workpack_id']} no_write {key} must be false")

    for phrase in [
        "LOCALIZATION-DEBT-WORKPACK-20260622",
        "本 workpack 把中文化门禁的命中项按目录分组",
        "修复中文化债务不等于 GFIS 真实业务链路完成",
        "accepted | `False`",
        "integrated | `False`",
        "production_ready | `False`",
    ]:
        require(phrase in md, f"evidence markdown missing phrase: {phrase}")
    require("build_localization_debt_workpack.py" in loop_round, "loop round missing builder")
    require("validate_localization_debt_workpack.py" in loop_round, "loop round missing validator")

    print("localization_debt_workpack=pass")
    print(f"localization_gate={evidence.get('localization_gate')}")
    print(f"findings={evidence.get('findings')}")
    print(f"work_item_count={evidence.get('work_item_count')}")
    print("execution_mode=local_evidence_no_write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
