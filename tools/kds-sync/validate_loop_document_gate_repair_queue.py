#!/usr/bin/env python3
"""Validate the Loop document gate repair queue evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_JSON = ROOT / "docs/harness/evidence/loop-document-gate-repair-queue-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/loop-document-gate-repair-queue-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-GCKF-P0-D87-001.md"
BUILDER = ROOT / "tools/kds-sync/build_loop_document_gate_repair_queue.py"


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


def current_gate_summary() -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, "tools/kds-sync/loop_document_gate.py", "--check-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        summary = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL: loop_document_gate output is not JSON: {exc}") from exc
    require(isinstance(summary, dict), "loop_document_gate summary must be object")
    return summary


def main() -> int:
    evidence = load_json(EVIDENCE_JSON)
    md = read(EVIDENCE_MD)
    loop_round = read(LOOP_ROUND)
    builder = read(BUILDER)
    require_frontmatter(EVIDENCE_MD, md)
    require_frontmatter(LOOP_ROUND, loop_round)
    for phrase in ["run_loop_gate", "gate_reasons", "no_write_boundary", "gfis_real_business_lane"]:
        require(phrase in builder, f"builder missing marker: {phrase}")

    summary = current_gate_summary()
    reasons = summary.get("gate_reasons")
    require(isinstance(reasons, list), "current gate_reasons must be list")
    require(evidence.get("evidence_id") == "LOOP-DOCUMENT-GATE-REPAIR-QUEUE-20260622", "invalid evidence id")
    require(evidence.get("gate") == summary.get("gate"), "gate mismatch with current summary")
    require(evidence.get("gate_reasons") == reasons, "gate_reasons mismatch with current summary")
    queue_items = evidence.get("queue_items")
    require(isinstance(queue_items, list), "queue_items must be list")
    require(evidence.get("queue_item_count") == len(queue_items), "queue_item_count mismatch")
    require(evidence.get("queue_item_count") == len(reasons), "queue count must match reasons")

    boundary = evidence.get("known_boundary", {})
    require(isinstance(boundary, dict), "known_boundary must be object")
    require(boundary.get("candidate_no_write") is True, "candidate_no_write must remain true")
    require(boundary.get("gfis_real_business_lane") == "repair_required", "GFIS lane must remain repair_required")
    for key in ["accepted", "integrated", "production_ready"]:
        require(boundary.get(key) is False, f"{key} must remain false")

    for item in queue_items:
        require(isinstance(item, dict), "queue item must be object")
        for key in ["queue_id", "reason", "category", "owner", "priority", "status", "repair_action"]:
            require(key in item, f"queue item missing {key}")
        no_write = item.get("no_write_boundary", {})
        require(isinstance(no_write, dict), "no_write_boundary must be object")
        for key in ["production_write", "business_writeback", "real_kds_api_write", "status_upgrade"]:
            require(no_write.get(key) is False, f"{item['queue_id']} no_write {key} must be false")

    for phrase in [
        "LOOP-DOCUMENT-GATE-REPAIR-QUEUE-20260622",
        "修复队列",
        "本 evidence 不证明 GFIS 真实业务链路完成",
        "accepted | `False`",
        "integrated | `False`",
        "production_ready | `False`",
    ]:
        require(phrase in md, f"evidence markdown missing phrase: {phrase}")
    require("build_loop_document_gate_repair_queue.py" in loop_round, "loop round missing builder")
    require("validate_loop_document_gate_repair_queue.py" in loop_round, "loop round missing validator")

    print("loop_document_gate_repair_queue=pass")
    print(f"gate={evidence.get('gate')}")
    print(f"gate_reasons={','.join(str(reason) for reason in reasons) if reasons else 'none'}")
    print(f"queue_item_count={evidence.get('queue_item_count')}")
    print("execution_mode=local_evidence_no_write")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
