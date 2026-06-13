#!/usr/bin/env python3
"""Validate KDS Loop initialization evidence for GPCF-KD-LR-001."""

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = {
    "loop_state": ROOT / "docs/harness/KDS/loop-state.md",
    "evidence_index": ROOT / "docs/harness/KDS/evidence/evidence-index.md",
    "loop_record": ROOT / "docs/harness/KDS/loops/loop-round-GPCF-KD-LR-001.md",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run_validator(script: str) -> str:
    result = subprocess.run(
        ["python3", str(ROOT / script)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    output = (result.stdout + result.stderr).strip()
    require(result.returncode == 0, f"{script} failed:\n{output}")
    return output


def main() -> int:
    loop_state = read(REQUIRED_FILES["loop_state"])
    evidence_index = read(REQUIRED_FILES["evidence_index"])
    loop_record = read(REQUIRED_FILES["loop_record"])

    for name, text in {
        "loop_state": loop_state,
        "evidence_index": evidence_index,
        "loop_record": loop_record,
    }.items():
        require("project: KDS" in text, f"{name} missing project: KDS")
        require("status: controlled" in text, f"{name} missing controlled status")
        require("kds_space: 开发" in text, f"{name} missing KDS development space")
        require("accepted" in text or "integrated" in text, f"{name} must preserve status boundary wording")

    for phrase in [
        "GPCF-KD-LR-001",
        "Current state remains `partial`",
        "substantive_rounds | 2/15",
        "batch_generated | false",
        "substance_gate | pass",
        "stop_type | none",
        "KDS Token",
    ]:
        require(phrase in loop_record, f"loop record missing phrase: {phrase}")

    require("loop.current_step | initialized_under_gpcf_control" in loop_state, "KDS loop-state not initialized")
    require("loop.gate_result | partial" in loop_state, "KDS loop-state must remain partial")
    require("docs/harness/KDS/loop-state.md" in evidence_index, "evidence index missing loop state")
    require("docs/harness/KDS/loops/loop-round-GPCF-KD-LR-001.md" in evidence_index, "evidence index missing loop record")

    token_output = run_validator("tools/kds-sync/validate_kds_token.py")
    require("kds_token=pass" in token_output, "KDS token validator did not pass")
    require("fingerprint=bfd9553d" in token_output, "KDS token fingerprint mismatch")

    print("kds initialization validation passed")
    print("round=GPCF-KD-LR-001 substantive_rounds=2/15 batch_generated=false status=partial")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
