#!/usr/bin/env python3
"""Validate that UI quality gating is wired into Loop and enforce explicit UI-scoped rounds."""

from __future__ import annotations

import json
import re
from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
UI_SIGNAL_RE = re.compile(
    r"(界面|UI|工作台|控制塔|对话页|移动端|桌面端|notification preview|read receipt preview|dismissal preview|snooze preview|Playwright|前端回归|UI/build smoke|知识 UI)",
    re.IGNORECASE,
)
EXPLICIT_UI_SCOPE_RE = re.compile(r"\|\s*UI scope\s*\|\s*true\s*\|", re.IGNORECASE)
REQUIRED_SUMMARY_PHRASES = [
    "UI gate status:",
    "Surface:",
    "Repository/path:",
    "Scope:",
    "Tools used:",
    "Tools unavailable:",
    "Verification:",
    "Status ceiling:",
]
REQUIRED_GATE_ROWS = [
    "G1 Surface Structure",
    "G2 Design Tokens",
    "G3 Component Consistency",
    "G4 Evidence And Governance",
    "G5 AI Fact Separation",
    "G6 Accessibility",
    "G7 Responsive And Text Robustness",
    "G8 Runtime Verification",
    "G9 Scope Control",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, object]:
    require(path.exists(), f"missing required JSON: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must be a JSON object")
    return data


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    template = read(ROOT / "templates/LOOP_ROUND_TEMPLATE.md")
    for phrase in [
        "## 7.1 UI 质量门禁（涉及 UI 时必填）",
        "| UI scope | true / false |",
        "| Tool route | `@product-design -> WAES -> ui-ux-pro-max -> Figma -> Storybook -> impeccable -> Playwright/browser -> axe-core/Lighthouse -> GPCF UI Gate` / project-specific route / not_applicable |",
        "| Context package | completed / partial / missing / not_applicable |",
        "| Prompt profile | functional-accuracy / visual-quality / usability-experience / governance-evidence / scope-control / mixed / not_applicable |",
        "| Design options | 3 / 1_with_existing_selected_direction / not_applicable |",
        "| Selected option | 1 / 2 / 3 / existing / not_applicable |",
        "| WAES baseline reuse | shell / page-skeleton / core-components / full-stack / exception-approved / not_applicable |",
        "UI gate status: ui_ready | ui_partial | ui_blocked | ui_rework_required | not_applicable",
        "Tool route:",
        "Context package:",
        "Prompt profile:",
        "Design options:",
        "Selected option:",
        "WAES baseline reuse:",
        "runtime_not_verified / mobile_not_verified / a11y_manual_only / figma_not_verified / not_applicable",
    ]:
        require(phrase in template, f"LOOP_ROUND_TEMPLATE.md missing phrase: {phrase}")
    for phrase in REQUIRED_GATE_ROWS:
        require(phrase in template, f"LOOP_ROUND_TEMPLATE.md missing UI gate row: {phrase}")

    master_doc = read(ROOT / "04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md")
    for phrase in [
        "Loop 接入",
        "UI gate status",
        "G1 Surface Structure",
        "ui_evidence_candidate",
        "@product-design",
        "工具上下文包",
        "提示词能力",
        "三方案机制",
        "accepted",
        "integrated",
    ]:
        require(phrase in master_doc, f"UI master doc missing phrase: {phrase}")

    implementation_plan = read(ROOT / "04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md")
    for phrase in [
        "项目群 UI 工程总控文件",
        "Loop 接入规则",
        "分阶段实施方案",
        "UI gate",
        "@product-design",
        "工具上下文包",
        "提示词能力体系",
        "三方案机制",
        "accepted",
        "integrated",
    ]:
        require(phrase in implementation_plan, f"UI implementation plan missing phrase: {phrase}")

    ui_skill = read(ROOT / ".codex/skills/globalcloud-ui-quality-gate/SKILL.md")
    require(
        "04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md" in ui_skill,
        "globalcloud-ui-quality-gate skill must read the UI implementation plan",
    )
    require(
        "04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md" in ui_skill,
        "globalcloud-ui-quality-gate skill must read the UI master doc",
    )
    require(
        "@product-design" in ui_skill,
        "globalcloud-ui-quality-gate skill must route product-design for design-led UI work",
    )

    tool_routing = read(ROOT / ".codex/skills/globalcloud-ui-quality-gate/references/tool-routing.md")
    for phrase in [
        "@product-design",
        "Must run `get-context -> ideate -> select option`",
        "Professional workbench UI defaults to `WAES` parent-frame reuse",
    ]:
        require(phrase in tool_routing, f"tool-routing.md missing phrase: {phrase}")

    usability_gates = read(ROOT / ".codex/skills/globalcloud-loop-orchestrator/references/usability-gates.md")
    require(
        "validate_loop_ui_quality_baseline.py" in usability_gates,
        "usability-gates must mention validate_loop_ui_quality_baseline.py",
    )

    capability_registry = read(ROOT / "02-governance/loop/LOOP_CAPABILITY_REGISTRY.md")
    require(
        "| `skill.globalcloud-ui-quality-gate` | `pilot` |" in capability_registry,
        "LOOP_CAPABILITY_REGISTRY.md must promote skill.globalcloud-ui-quality-gate to pilot",
    )
    require(
        "`tool.validate_loop_ui_quality_baseline.py`" in capability_registry,
        "LOOP_CAPABILITY_REGISTRY.md missing tool.validate_loop_ui_quality_baseline.py",
    )

    evidence_json = load_json(ROOT / "docs/harness/evidence/loop-ui-governance-baseline-20260622.json")
    require(
        evidence_json.get("evidence_id") == "LOOP-UI-GOV-BASELINE-20260622",
        "UI governance evidence_id mismatch",
    )
    controls = evidence_json.get("controls")
    require(isinstance(controls, dict), "UI governance evidence missing controls")
    require(controls.get("template_ui_scope_required") is True, "UI governance evidence must require template_ui_scope")
    require(
        controls.get("broader_project_status_upgrade_requires_harness") is True,
        "UI governance evidence must preserve Harness upgrade boundary",
    )

    explicit_ui_scope_rounds = 0
    explicit_ui_scope_valid = 0
    historical_ui_signal_rounds_without_explicit_scope = 0
    for path in sorted((ROOT / "docs/harness/loops").glob("loop-round-*.md")):
        text = path.read_text(encoding="utf-8")
        has_ui_signal = UI_SIGNAL_RE.search(text) is not None
        has_explicit_ui_scope = EXPLICIT_UI_SCOPE_RE.search(text) is not None
        if has_explicit_ui_scope:
            explicit_ui_scope_rounds += 1
            for phrase in REQUIRED_SUMMARY_PHRASES + REQUIRED_GATE_ROWS:
                require(phrase in text, f"{path.relative_to(ROOT)} missing UI gate phrase: {phrase}")
            explicit_ui_scope_valid += 1
        elif has_ui_signal:
            historical_ui_signal_rounds_without_explicit_scope += 1

    print(
        "loop_ui_quality_baseline=pass "
        "template_ui_section=present "
        "master_spec=present "
        "capability_status=pilot "
        f"explicit_ui_scope_rounds={explicit_ui_scope_rounds} "
        f"explicit_ui_scope_valid={explicit_ui_scope_valid} "
        f"historical_ui_signal_rounds_without_explicit_scope={historical_ui_signal_rounds_without_explicit_scope} "
        "baseline_evidence=present "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
