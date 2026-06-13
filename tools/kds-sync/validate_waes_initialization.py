#!/usr/bin/env python3
"""Validate WAES Loop initialization evidence for GPCF-WA-LR-001."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(rel: str) -> str:
    path = ROOT / rel
    require(path.exists(), f"missing file: {rel}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    loop_state = read("docs/harness/WAES/loop-state.md")
    evidence_index = read("docs/harness/WAES/evidence/evidence-index.md")
    loop_record = read("docs/harness/WAES/loops/loop-round-GPCF-WA-LR-001.md")
    for name, text in {"loop_state": loop_state, "evidence_index": evidence_index, "loop_record": loop_record}.items():
        require("project: WAES" in text, f"{name} missing project: WAES")
        require("status: controlled" in text, f"{name} missing controlled status")
        require("accepted" in text or "integrated" in text, f"{name} missing status boundary")
    for phrase in ["GPCF-WA-LR-001", "substantive_rounds | 10/15", "batch_generated | false", "stop_type | none", "未改变验收裁决权"]:
        require(phrase in loop_record + loop_state, f"missing phrase: {phrase}")
    require("loop.gate_result | partial" in loop_state, "WAES must remain partial")
    print("waes initialization validation passed")
    print("round=GPCF-WA-LR-001 substantive_rounds=10/15 batch_generated=false status=partial")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
