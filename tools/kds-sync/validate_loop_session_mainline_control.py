#!/usr/bin/env python3
"""Validate LOOP session mainline and cross-session handoff control."""

from __future__ import annotations

from pathlib import Path

from gfis_real_fact_entry_guard import require_gfis_real_fact_entry


ROOT = Path(__file__).resolve().parents[2]
CONTROL_PACK = ROOT / "02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md"
MASTER = ROOT / "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md"
DECLARATION_TEMPLATE = ROOT / "templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md"
HANDOFF_TEMPLATE = ROOT / "templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md"
README = ROOT / "02-governance/loop/README.md"
TEMPLATES_README = ROOT / "templates/README.md"
LOOP_DOCUMENT_GATE = ROOT / "tools/kds-sync/loop_document_gate.py"
CURRENT_DECLARATION_VALIDATOR = ROOT / "tools/kds-sync/validate_current_session_mainline_declaration.py"
SESSION_REGISTRY = ROOT / "02-governance/loop/LOOP_SESSION_REGISTRY.md"
SESSION_REGISTRY_VALIDATOR = ROOT / "tools/kds-sync/validate_loop_session_registry.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_session_mainline_control: {message}")


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


def require_phrases(label: str, text: str, phrases: list[str]) -> None:
    for phrase in phrases:
        require(phrase in text, f"{label} missing phrase: {phrase}")


def main() -> int:
    gfis_real_fact_entry = require_gfis_real_fact_entry(ROOT)
    control_pack = read(CONTROL_PACK)
    master = read(MASTER)
    declaration_template = read(DECLARATION_TEMPLATE)
    handoff_template = read(HANDOFF_TEMPLATE)
    readme = read(README)
    templates_readme = read(TEMPLATES_README)
    loop_document_gate = read(LOOP_DOCUMENT_GATE)
    current_declaration_validator = read(CURRENT_DECLARATION_VALIDATOR)
    session_registry = read(SESSION_REGISTRY)
    session_registry_validator = read(SESSION_REGISTRY_VALIDATOR)

    require_controlled(control_pack, "02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md")
    require_controlled(declaration_template, "templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md")
    require_controlled(handoff_template, "templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md")

    require_phrases(
        "control pack",
        control_pack,
        [
            "LOOP 会话主线控制包",
            "启动/恢复前置门禁",
            "session_mainline",
            "owner_session",
            "handoff_source",
            "handoff_time",
            "scope_delta",
            "authorization_delta",
            "mainline_drift_detected",
            "没有完整交接证据，只能生成建议，不能执行写入",
            "validate_loop_session_mainline_control.py",
            "不授权真实 KDS API 写入",
            "不授权外部 API 写入",
            "不授权跨仓执行",
            "不授权 commit、push、deploy、accepted、integrated 或 production_ready",
            "DO NOT send optional commentary",
            "communication_boundary",
        ],
    )

    require_phrases(
        "master plan",
        master,
        [
            "会话主线与跨会话防偏离控制",
            "session_mainline",
            "owner session",
            "handoff evidence",
            "mainline_drift_detected",
            "会话主线边界",
        ],
    )

    require_phrases(
        "declaration template",
        declaration_template,
        [
            "LOOP 会话主线声明模板",
            "session_mainline",
            "objective",
            "owner_session",
            "scope_in",
            "scope_out",
            "allowed_actions",
            "forbidden_actions",
            "stop_conditions",
            "evidence_inputs",
            "mainline_drift_detected",
            "authorization_required",
            "communication_boundary",
            "DO NOT send optional commentary",
            "optional_commentary_blocked",
        ],
    )

    require_phrases(
        "handoff template",
        handoff_template,
        [
            "LOOP 跨会话交接模板",
            "handoff_id",
            "handoff_source",
            "handoff_time",
            "source_owner_session",
            "target_owner_session",
            "source_session_mainline",
            "target_session_mainline",
            "user_confirmation",
            "scope_delta",
            "authorization_delta",
            "remaining_risks",
            "只能生成建议",
            "communication_boundary",
            "DO NOT send optional commentary",
            "发送 optional commentary",
        ],
    )

    require(
        "LOOP 会话主线控制包 | 02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md" in readme,
        "loop README missing session mainline control pack entry",
    )
    require(
        "LOOP 会话主线声明模板 | templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md" in templates_readme,
        "templates README missing session mainline declaration template entry",
    )
    require(
        "LOOP 跨会话交接模板 | templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md" in templates_readme,
        "templates README missing cross-session handoff template entry",
    )
    require(
        "loop_session_mainline_control" in loop_document_gate
        and "validate_loop_session_mainline_control.py" in loop_document_gate,
        "loop document gate missing session mainline control validator",
    )
    require(
        "current_session_mainline_declaration" in loop_document_gate
        and "validate_current_session_mainline_declaration.py" in loop_document_gate,
        "loop document gate missing current session mainline declaration validator",
    )
    require(
        "loop_session_registry" in loop_document_gate
        and "validate_loop_session_registry.py" in loop_document_gate,
        "loop document gate missing session registry validator",
    )
    require(
        "current_session_mainline_declaration=pass" in current_declaration_validator
        and "mainline_drift_detected=false" in current_declaration_validator,
        "current session mainline declaration validator missing pass markers",
    )
    require(
        "LOOP 会话总账" in session_registry
        and "repo_recorded_loop_sessions_only" in session_registry,
        "session registry missing governance markers",
    )
    require("loop_session_registry=pass" in session_registry_validator, "session registry validator missing pass marker")

    forbidden = [
        "允许自动授权 commit",
        "允许自动授权 push",
        "允许自动授权 deploy",
        "允许自动升级 accepted",
        "允许自动升级 integrated",
        "无需 handoff 即可写入",
    ]
    combined = "\n".join([control_pack, declaration_template, handoff_template])
    for phrase in forbidden:
        require(phrase not in combined, f"forbidden claim present: {phrase}")

    print(
        "loop_session_mainline_control=pass "
        "session_mainline=required handoff_evidence=required "
        "mainline_drift_detected=hard_pause write_without_handoff=false "
        "commit_push_deploy_status_promotion_allowed=false "
        f"gfis_status_ceiling={gfis_real_fact_entry.get('status_ceiling')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
