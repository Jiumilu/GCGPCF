#!/usr/bin/env python3
"""Validate project-group LOOP delivery efficiency control."""

from __future__ import annotations

from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
CONTROL_DOC = ROOT / "02-governance/loop/LOOP_DELIVERY_EFFICIENCY_CONTROL.md"
MASTER = ROOT / "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"
EXECUTION = ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"
UI_CONTROL = ROOT / "02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md"
ORCHESTRATOR_SKILL = ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md"
LOOP_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"

PROJECTS = [
    "AAAS",
    "Brain",
    "WAS",
    "XiaoC",
    "WAES",
    "GPC",
    "Studio",
    "GPCF",
    "XWAIL",
    "GFIS",
    "MMC",
    "KDS",
    "XiaoG",
    "PVAOS",
    "SOP",
    "PKC",
    "XGD",
]

CORE_PHRASES = [
    "LOOP Delivery Efficiency Control",
    "project_group_scope_17_projects",
    "high_compliance_low_product_progress",
    "product_delta",
    "user_visible_delta",
    "loop_cost_level",
    "substantive_round",
    "task_flow_e2e_status",
    "evidence_overexposure_gate",
    "delivery_efficiency_gate",
    "governance_progress",
    "product_progress",
    "single_label_copy_tweak_heavy_loop_blocked",
    "goal / changed / verified / risk / next",
    "DO NOT send optional commentary",
]

FORBIDDEN_CLAIMS = [
    "自动标记 accepted",
    "自动标记 integrated",
    "自动标记 production_ready",
    "真实 KDS API 已授权",
    "真实外部 API 已授权",
    "已接管项目本地目标",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_delivery_efficiency_control: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8", errors="ignore")


def require_controlled(text: str, source_path: str) -> None:
    for phrase in [
        "status: controlled",
        "kds_space: 开发",
        f"source_path: {source_path}",
        "sync_direction: bidirectional",
    ]:
        require(phrase in text, f"{source_path} missing controlled marker: {phrase}")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    control_doc = read(CONTROL_DOC)
    master = read(MASTER)
    execution = read(EXECUTION)
    ui_control = read(UI_CONTROL)
    orchestrator_skill = read(ORCHESTRATOR_SKILL)
    loop_gate = read(LOOP_GATE)

    require_controlled(control_doc, "02-governance/loop/LOOP_DELIVERY_EFFICIENCY_CONTROL.md")

    for project in PROJECTS:
        require(project in control_doc, f"control doc missing 17-project scope project: {project}")

    for phrase in CORE_PHRASES:
        require(phrase in control_doc, f"control doc missing phrase: {phrase}")
        require(
            phrase in master or phrase in execution or phrase in ui_control or phrase in orchestrator_skill,
            f"policy not propagated: {phrase}",
        )

    for phrase in [
        "LOOP_DELIVERY_EFFICIENCY_CONTROL.md",
        "validate_loop_delivery_efficiency_control.py",
        "连续 3 轮",
        "G0",
        "G1",
        "G2",
        "GPCF 只负责项目群 LOOP 防偏",
        "必须重新获得人工授权",
    ]:
        require(phrase in control_doc, f"control doc missing delivery governance phrase: {phrase}")

    require(
        "loop_delivery_efficiency_control" in loop_gate
        and "validate_loop_delivery_efficiency_control.py" in loop_gate,
        "loop_document_gate.py missing delivery efficiency validator",
    )
    require(
        "LOOP_DELIVERY_EFFICIENCY_CONTROL.md" in orchestrator_skill,
        "loop orchestrator skill missing delivery efficiency control",
    )
    require(
        "LOOP_DELIVERY_EFFICIENCY_CONTROL.md" in master,
        "master plan missing delivery efficiency control",
    )
    require(
        "LOOP_DELIVERY_EFFICIENCY_CONTROL.md" in ui_control,
        "UI product-first control must cross-reference delivery efficiency control",
    )

    combined = "\n".join([control_doc, master, execution, ui_control, orchestrator_skill])
    for phrase in FORBIDDEN_CLAIMS:
        require(phrase not in combined, f"forbidden claim present: {phrase}")

    print(
        "loop_delivery_efficiency_control=pass "
        "project_group_scope_17_projects=true "
        "delivery_efficiency_gate=required "
        "product_delta=required "
        "user_visible_delta=required "
        "loop_cost_level=required "
        "substantive_round=required "
        "high_compliance_low_product_progress=blocked "
        "single_label_copy_tweak_heavy_loop_blocked=true "
        "status_promotion_allowed=false "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
