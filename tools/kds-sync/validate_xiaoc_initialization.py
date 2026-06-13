#!/usr/bin/env python3
"""Validate XiaoC Loop initialization evidence for GPCF-XC-LR-001."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = {
    "loop_state": ROOT / "docs/harness/XiaoC/loop-state.md",
    "evidence_index": ROOT / "docs/harness/XiaoC/evidence/evidence-index.md",
    "loop_record": ROOT / "docs/harness/XiaoC/loops/loop-round-GPCF-XC-LR-001.md",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    loop_state = read(REQUIRED_FILES["loop_state"])
    evidence_index = read(REQUIRED_FILES["evidence_index"])
    loop_record = read(REQUIRED_FILES["loop_record"])

    for name, text in {
        "loop_state": loop_state,
        "evidence_index": evidence_index,
        "loop_record": loop_record,
    }.items():
        require("project: XiaoC" in text, f"{name} missing project: XiaoC")
        require("status: controlled" in text, f"{name} missing controlled status")
        require("kds_space: 开发" in text, f"{name} missing KDS development space")
        require("accepted" in text or "integrated" in text, f"{name} must preserve status boundary wording")

    for phrase in [
        "GPCF-XC-LR-001",
        "Current state remains `partial`",
        "substantive_rounds | 5/15",
        "batch_generated | false",
        "substance_gate | pass",
        "stop_type | none",
        "Wrangler",
        "模型路由",
    ]:
        require(phrase in loop_record, f"loop record missing phrase: {phrase}")

    require("loop.current_step | initialized_under_gpcf_control" in loop_state, "XiaoC loop-state not initialized")
    require("loop.gate_result | partial" in loop_state, "XiaoC loop-state must remain partial")
    require("蚁后" in loop_state, "XiaoC role positioning must remain documented")
    require("docs/harness/XiaoC/loop-state.md" in evidence_index, "evidence index missing loop state")

    print("xiaoc initialization validation passed")
    print("round=GPCF-XC-LR-001 substantive_rounds=5/15 batch_generated=false status=partial")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
