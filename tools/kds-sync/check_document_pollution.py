#!/usr/bin/env python3
"""Check GlobalCloud documents for forbidden legacy or polluted wording."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_PARTS = {".git", ".kds"}

PATTERNS = [
    ("old_gpc_native", re.compile(r"GPC-Native|gpc-native|GPC Native|GPC\\-Native|\bNative\b")),
    ("old_collaboration_platform", re.compile(r"协同中台")),
    ("old_prompt_service", re.compile(r"提示词工程服务|提示词工程\)")),
    ("old_digital_consciousness", re.compile(r"数字意识框架|Agent框架")),
    ("old_xiaoc_prompt_boundary", re.compile(r"XiaoC 管 prompt|XiaoC 提供提示词")),
    ("old_xgd_entry", re.compile(r"桌面/语音/社交 AI 入口")),
    ("old_ai_bundle", re.compile(r"XiaoC \+ Hermes \+ XGD|XiaoC、Hermes、XGD")),
]

ALLOWLIST_FILES = {
    ".codex/skills/globalcloud-document-governance/references/anti-pollution-rules.md",
    "02-governance/GlobalCloud项目群文档防污染规则.md",
    "09-status/globalcloud-document-health-report.md",
}


def iter_markdown() -> list[Path]:
    docs = []
    for path in ROOT.rglob("*.md"):
        if set(path.relative_to(ROOT).parts) & EXCLUDE_PARTS:
            continue
        docs.append(path)
    return sorted(docs)


def main() -> int:
    findings: list[str] = []
    for path in iter_markdown():
        rel = path.relative_to(ROOT).as_posix()
        if rel in ALLOWLIST_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            for name, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(f"{rel}:{line_no}: {name}: {line.strip()[:160]}")
    for path in ROOT.rglob("*"):
        if path.is_file() and set(path.relative_to(ROOT).parts) & EXCLUDE_PARTS:
            continue
        name = path.name
        rel = path.relative_to(ROOT).as_posix()
        if rel in ALLOWLIST_FILES:
            continue
        for rule_name, pattern in PATTERNS[:2]:
            if pattern.search(name):
                findings.append(f"{path.relative_to(ROOT).as_posix()}: filename: {rule_name}")
    if findings:
        print("document_pollution=fail")
        print("\n".join(findings))
        return 1
    print("document_pollution=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
