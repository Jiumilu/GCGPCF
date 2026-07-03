#!/usr/bin/env python3
"""Validate the project-group LOOP optional commentary suppression policy."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "AGENTS.md",
    "GlobalCloud 项目群实施方案.md",
    "02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md",
    "02-governance/loop/LOOP_EXECUTION_RULES.md",
    "02-governance/loop/LOOP_AUTONOMY_POLICY.md",
    "02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md",
    "templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md",
    "templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md",
    ".codex/skills/globalcloud-document-governance/SKILL.md",
    ".codex/skills/globalcloud-loop-orchestrator/SKILL.md",
    ".codex/skills/globalcloud-project-group-git-clean/SKILL.md",
    ".codex/skills/globalcloud-ui-quality-gate/SKILL.md",
]

REQUIRED_GLOBAL_PHRASE = "DO NOT send optional commentary"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL validate_loop_optional_commentary_policy: {message}")


def read(relative_path: str) -> str:
    path = ROOT / relative_path
    require(path.exists(), f"missing file: {relative_path}")
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    for relative_path in REQUIRED_FILES:
        text = read(relative_path)
        require(
            REQUIRED_GLOBAL_PHRASE in text,
            f"{relative_path} missing required phrase: {REQUIRED_GLOBAL_PHRASE}",
        )

    master = read("02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md")
    execution = read("02-governance/loop/LOOP_EXECUTION_RULES.md")
    session_pack = read("02-governance/loop/LOOP_SESSION_MAINLINE_CONTROL_PACK.md")
    declaration_template = read("templates/LOOP_SESSION_MAINLINE_DECLARATION_TEMPLATE.md")
    handoff_template = read("templates/LOOP_CROSS_SESSION_HANDOFF_TEMPLATE.md")
    loop_document_gate = read("tools/kds-sync/loop_document_gate.py")

    for phrase in [
        "输出克制",
        "只输出必要结论、阻塞项、确认请求、执行结果、验证证据和下一步必要动作",
        "不得发送 optional commentary",
    ]:
        require(phrase in master or phrase in execution, f"missing master/execution policy phrase: {phrase}")

    for phrase in [
        "communication_boundary",
        "optional_commentary_blocked",
    ]:
        require(phrase in declaration_template, f"declaration template missing phrase: {phrase}")

    require("communication_boundary" in session_pack, "session control pack missing communication_boundary")
    require("发送 optional commentary" in handoff_template, "handoff template missing optional commentary prohibition")
    require(
        "loop_optional_commentary_policy" in loop_document_gate
        and "validate_loop_optional_commentary_policy.py" in loop_document_gate,
        "loop document gate missing optional commentary policy validator",
    )

    forbidden_positive_claims = [
        "允许发送 optional commentary",
        "optional commentary allowed",
        "可选 commentary 可替代确认",
    ]
    combined = "\n".join(read(path) for path in REQUIRED_FILES)
    for phrase in forbidden_positive_claims:
        require(phrase not in combined, f"forbidden positive claim present: {phrase}")

    print(
        "loop_optional_commentary_policy=pass "
        "required_phrase='DO NOT send optional commentary' "
        "project_group_scope=17_projects skills=covered templates=covered"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
