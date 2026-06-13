#!/usr/bin/env python3
"""Validate GlobalCloud Loop governance control documents."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    ROOT / "02-governance/loop/README.md",
    ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md",
    ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md",
    ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md",
    ROOT / "02-governance/loop/LOOP_RISK_GATE.md",
    ROOT / "02-governance/loop/LOOP_METRICS.md",
    ROOT / "templates/LOOP_ROUND_TEMPLATE.md",
    ROOT / "templates/LOOP_EVIDENCE_TEMPLATE.md",
    ROOT / "templates/LOOP_HANDOFF_TEMPLATE.md",
]

REQUIRED_FRONTMATTER_KEYS = [
    "doc_id:",
    "title:",
    "project:",
    "related_projects:",
    "domain:",
    "status:",
    "version:",
    "owner:",
    "kds_space:",
    "kds_path:",
    "source_path:",
    "sync_direction:",
    "last_reviewed:",
    "supersedes:",
    "superseded_by:",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def read(path: Path) -> str:
    require(path.exists(), f"missing required doc: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate_frontmatter(path: Path, text: str) -> None:
    require(text.startswith("---\n"), f"{path.relative_to(ROOT)} missing front matter")
    end = text.find("\n---\n", 4)
    require(end > 0, f"{path.relative_to(ROOT)} has invalid front matter")
    frontmatter = text[:end]
    for key in REQUIRED_FRONTMATTER_KEYS:
        require(key in frontmatter, f"{path.relative_to(ROOT)} missing front matter key {key}")
    require("kds_space: 开发" in frontmatter, f"{path.relative_to(ROOT)} must use KDS 开发 space")


def main() -> int:
    texts: dict[Path, str] = {}
    for path in REQUIRED_DOCS:
        text = read(path)
        validate_frontmatter(path, text)
        texts[path] = text

    policy = texts[ROOT / "02-governance/loop/LOOP_AUTONOMY_POLICY.md"]
    for phrase in [
        "最多 15 轮或 2 小时",
        "Git push",
        "真实 API 写入",
        "真实 KDS TOKEN 写入",
        "accepted",
        "integrated",
    ]:
        require(phrase in policy, f"LOOP_AUTONOMY_POLICY.md missing phrase: {phrase}")

    control = texts[ROOT / "02-governance/loop/LOOP_CONTROL_BOARD.md"]
    for phrase in [
        "当前 Loop 模式",
        "当前轮次",
        "当前允许动作",
        "当前禁止动作",
        "下一轮候选任务队列",
    ]:
        require(phrase in control, f"LOOP_CONTROL_BOARD.md missing phrase: {phrase}")

    execution = texts[ROOT / "02-governance/loop/LOOP_EXECUTION_RULES.md"]
    for phrase in ["AGENTS.md", "LOOP_CONTROL_BOARD.md", "LOOP_AUTONOMY_POLICY.md", "Definition of Done"]:
        require(phrase in execution, f"LOOP_EXECUTION_RULES.md missing phrase: {phrase}")

    round_template = texts[ROOT / "templates/LOOP_ROUND_TEMPLATE.md"]
    for phrase in ["Round ID", "授权边界", "验证命令", "Evidence 清单", "状态判定"]:
        require(phrase in round_template, f"LOOP_ROUND_TEMPLATE.md missing phrase: {phrase}")

    skill = read(ROOT / ".codex/skills/globalcloud-loop-orchestrator/SKILL.md")
    for phrase in ["LOOP_CONTROL_BOARD.md", "LOOP_AUTONOMY_POLICY.md", "L3 托管冲刺模式"]:
        require(phrase in skill, f"loop orchestrator skill missing phrase: {phrase}")

    print("loop governance docs validation passed")
    print(f"docs={len(REQUIRED_DOCS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
