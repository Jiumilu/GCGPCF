#!/usr/bin/env python3
"""Validate XGD Loop initialization evidence for GPCF-XD-LR-001."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = {
    "loop_state": ROOT / "docs/harness/XGD/loop-state.md",
    "evidence_index": ROOT / "docs/harness/XGD/evidence/evidence-index.md",
    "loop_record": ROOT / "docs/harness/XGD/loops/loop-round-GPCF-XD-LR-001.md",
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
        require("project: XGD" in text, f"{name} missing project: XGD")
        require("status: controlled" in text, f"{name} missing controlled status")
        require("kds_space: 开发" in text, f"{name} missing KDS development space")
        require("accepted" in text or "integrated" in text, f"{name} must preserve status boundary wording")

    for phrase in [
        "GPCF-XD-LR-001",
        "Current state remains `partial`",
        "substantive_rounds | 6/15",
        "batch_generated | false",
        "substance_gate | pass",
        "stop_type | none",
        "大象",
    ]:
        require(phrase in loop_record, f"loop record missing phrase: {phrase}")

    require("loop.current_step | initialized_under_gpcf_control" in loop_state, "XGD loop-state not initialized")
    require("loop.gate_result | partial" in loop_state, "XGD loop-state must remain partial")
    require("大象" in loop_state, "XGD role positioning must remain documented")
    require("docs/harness/XGD/loop-state.md" in evidence_index, "evidence index missing loop state")

    print("xgd initialization validation passed")
    print("round=GPCF-XD-LR-001 substantive_rounds=6/15 batch_generated=false status=partial")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
