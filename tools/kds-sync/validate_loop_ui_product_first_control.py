#!/usr/bin/env python3
"""Validate LOOP UI product-first governance control."""

from __future__ import annotations

from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
CONTROL_DOC = ROOT / "02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md"
MASTER = ROOT / "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"
EXECUTION = ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"
UI_MASTER = ROOT / "04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md"
UI_SKILL = ROOT / ".codex/skills/globalcloud-ui-quality-gate/SKILL.md"
LOOP_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"

CORE_PHRASES = [
    "LOOP success must not reduce product usability.",
    "UI evidence is not UI structure.",
    "Governance evidence must be traceable, not dominant.",
    "Debug details must not become default product copy.",
    "A test-visible element is not automatically user-visible.",
    "product_first_ui_gate",
    "evidence_overexposure_gate",
    "debug_details_visibility",
    "task_flow_e2e_status",
    "audit_traceability_gate",
    "ui_rework_required",
]

FORBIDDEN_CLAIMS = [
    "GPCF 接管 Studio 开发",
    "自动升级 accepted",
    "自动升级 integrated",
    "真实 KDS API 已授权",
    "真实外部 API 已授权",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_ui_product_first_control: {message}")


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
    ui_master = read(UI_MASTER)
    ui_skill = read(UI_SKILL)
    loop_gate = read(LOOP_GATE)

    require_controlled(control_doc, "02-governance/loop/LOOP_UI_PRODUCT_FIRST_CONTROL.md")

    for phrase in CORE_PHRASES:
        require(phrase in control_doc, f"control doc missing phrase: {phrase}")
        require(phrase in master or phrase in execution or phrase in ui_master or phrase in ui_skill, f"policy not propagated: {phrase}")

    for phrase in [
        "不接管 Studio 当前开发目标",
        "GPCF 只控制 LOOP 防偏",
        "不得新增常驻 receipt/preflight/dry-run/boundary/readiness 条",
        "E2E 以用户流程完成为主",
        "继续 Studio 当前目标开发",
        "goal / changed / verified / risk / next",
    ]:
        require(phrase in control_doc, f"control doc missing Studio control phrase: {phrase}")

    require(
        "validate_loop_ui_product_first_control.py" in control_doc,
        "control doc missing validator reference",
    )
    require(
        "loop_ui_product_first_control" in loop_gate
        and "validate_loop_ui_product_first_control.py" in loop_gate,
        "loop_document_gate.py missing product-first validator",
    )
    require(
        "LOOP_UI_PRODUCT_FIRST_CONTROL.md" in ui_skill,
        "UI quality gate skill must read product-first control doc",
    )
    require(
        "LOOP_UI_PRODUCT_FIRST_CONTROL.md" in ui_master,
        "UI master spec must reference product-first control doc",
    )

    combined = "\n".join([control_doc, master, execution, ui_master, ui_skill])
    for phrase in FORBIDDEN_CLAIMS:
        require(phrase not in combined, f"forbidden claim present: {phrase}")

    print(
        "loop_ui_product_first_control=pass "
        "studio_control=governance_only "
        "product_first_ui_gate=required "
        "evidence_overexposure_gate=required "
        "debug_details_default_hidden=required "
        "task_flow_e2e_required=true "
        "status_promotion_allowed=false "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
