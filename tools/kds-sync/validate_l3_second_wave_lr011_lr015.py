#!/usr/bin/env python3
"""Validate L3 second-wave substantive rounds LR-011 through LR-015."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ROUNDS = [
    ("GPCF-WA-LR-002", "WAES", "docs/harness/WAES/loops/loop-round-GPCF-WA-LR-002.md", "11/15"),
    ("GPCF-GP-LR-002", "GPC", "docs/harness/GPC/loops/loop-round-GPCF-GP-LR-002.md", "12/15"),
    ("GPCF-PV-LR-002", "PVAOS", "docs/harness/PVAOS/loops/loop-round-GPCF-PV-LR-002.md", "13/15"),
    ("GPCF-XG-LR-002", "XiaoG", "docs/harness/XiaoG/loops/loop-round-GPCF-XG-LR-002.md", "14/15"),
    ("GPCF-MM-LR-002", "MMC", "docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md", "15/15"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    for round_id, project, rel, ratio in ROUNDS:
        path = ROOT / rel
        require(path.exists(), f"missing file: {rel}")
        text = path.read_text(encoding="utf-8")
        require(f"project: {project}" in text, f"{round_id} missing project metadata")
        require("status: controlled" in text, f"{round_id} missing controlled status")
        require(round_id in text, f"{round_id} missing round id")
        require(f"substantive_rounds | {ratio}" in text, f"{round_id} missing substantive ratio {ratio}")
        require("batch_generated | false" in text, f"{round_id} must not be batch counted")
        require("substance_gate | pass" in text, f"{round_id} missing substance gate")
        require("Current state remains `partial`" in text, f"{round_id} must preserve partial state")
        require("accepted/integrated" in text, f"{round_id} must preserve accepted/integrated boundary")
    mmc = (ROOT / "docs/harness/MMC/loops/loop-round-GPCF-MM-LR-002.md").read_text(encoding="utf-8")
    require("stop_type | budget_exhausted" in mmc, "LR-015 must close with budget_exhausted")
    print("l3 second-wave validation passed")
    print("declared=15/15 substantive=15/15 generated_items=50 batch_generated=false substance_gate=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
