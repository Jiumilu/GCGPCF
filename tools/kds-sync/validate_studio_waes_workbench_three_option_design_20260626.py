#!/usr/bin/env python3
"""Validate Studio WAES workbench three-option UI design evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_MD = ROOT / "docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.md"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/studio-waes-workbench-three-option-design-20260626.json"
ROUND_MD = ROOT / "docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-023.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    evidence = read(EVIDENCE_MD)
    loop_round = read(ROUND_MD)
    data = json.loads(read(EVIDENCE_JSON))

    required_tokens = [
        "product_design_tool_not_exposed",
        "get-context",
        "ideate",
        "select option",
        "Option 1",
        "Option 2",
        "Option 3",
        "Selected option = 1",
        "WAES Baseline Reuse",
        "UI gate status: ui_partial",
        "Status ceiling: ui_evidence_candidate",
        "runtime_not_verified",
        "mobile_not_verified",
        "figma_not_verified",
    ]
    for token in required_tokens:
        require(token in evidence, f"evidence missing token: {token}")

    loop_tokens = [
        "| UI scope | true |",
        "| Design options | 3 |",
        "| Selected option | 1 |",
        "| WAES baseline reuse | shell / page-skeleton / core-components |",
        "G1 Surface Structure",
        "G8 Runtime Verification",
        "Status ceiling: ui_evidence_candidate",
    ]
    for token in loop_tokens:
        require(token in loop_round, f"loop round missing token: {token}")

    require(data["selected_option"] == "1", "selected_option must be 1")
    require(len(data["design_options"]) == 3, "design_options must contain exactly 3 options")
    require(data["status_ceiling"] == "ui_evidence_candidate", "status ceiling mismatch")
    require(data["accepted"] is False, "accepted must remain false")
    require(data["integrated"] is False, "integrated must remain false")
    require(data["production_ready"] is False, "production_ready must remain false")

    print(
        "studio_waes_workbench_three_option_design=pass "
        "design_options=3 selected_option=1 "
        "waes_baseline_reuse=shell,page_skeleton,core_components "
        "ui_gate_status=ui_partial status_ceiling=ui_evidence_candidate "
        "runtime_not_verified=true product_design_tool_not_exposed=true"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
