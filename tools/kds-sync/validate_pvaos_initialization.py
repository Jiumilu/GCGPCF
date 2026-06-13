#!/usr/bin/env python3
"""Validate PVAOS Loop initialization evidence for GPCF-PV-LR-001."""

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
    loop_state = read("docs/harness/PVAOS/loop-state.md")
    evidence_index = read("docs/harness/PVAOS/evidence/evidence-index.md")
    loop_record = read("docs/harness/PVAOS/loops/loop-round-GPCF-PV-LR-001.md")
    for name, text in {"loop_state": loop_state, "evidence_index": evidence_index, "loop_record": loop_record}.items():
        require("project: PVAOS" in text, f"{name} missing project: PVAOS")
        require("status: controlled" in text, f"{name} missing controlled status")
        require("accepted" in text or "integrated" in text, f"{name} missing status boundary")
    for phrase in ["GPCF-PV-LR-001", "substantive_rounds | 9/15", "batch_generated | false", "stop_type | none"]:
        require(phrase in loop_record, f"loop record missing phrase: {phrase}")
    require("loop.gate_result | partial" in loop_state, "PVAOS must remain partial")
    print("pvaos initialization validation passed")
    print("round=GPCF-PV-LR-001 substantive_rounds=9/15 batch_generated=false status=partial")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
