#!/usr/bin/env python3
"""Validate Brain team authorization contract C-baseline evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "docs/harness/Brain/evidence/brain-team-authorization-contract-drift-20260624.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EVIDENCE_TOKENS = [
    "Brain team 空间授权契约 C 口径确认证据 2026-06-24",
    "brain_team_authorization_contract = confirmed_c_read_write_split",
    "browser_runtime_smoke_status = pass_with_boundaries_after_c_alignment",
    "current_chrome_visible_signals = confirmed",
    "team 空间可读 KDS dashboard/graph/search",
    "写入、prompt、secret 和持久化操作继续受授权边界控制",
    "用户已确认 C",
    "不代表 `read-closure`、`status-audit`、`harness-evidence` 或整体集成闭合",
]

REQUIRED_REGISTER_TOKENS = [
    "brain-team-authorization-contract-drift-20260624.md",
    "brain_team_authorization_contract",
    "confirmed_c_read_write_split",
    "team authorization",
    "读写分层",
]

FORBIDDEN_CLAIMS = [
    "Brain 真实集成完成",
    "真实交付完成",
    "客户验收通过",
]

ALLOWED_CONTEXTS = [
    "不声明",
    "不能",
    "不得",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def check_forbidden(text: str, failures: list[str]) -> None:
    for token in FORBIDDEN_CLAIMS:
        start = 0
        while True:
            idx = text.find(token, start)
            if idx == -1:
                break
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if not any(context in line for context in ALLOWED_CONTEXTS):
                failures.append(f"forbidden claim without boundary: {line}")
            start = idx + len(token)


def main() -> int:
    failures: list[str] = []
    evidence_text = read(EVIDENCE, failures)
    register_text = read(REGISTER, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in drift evidence: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(evidence_text + "\n" + register_text, failures)

    result = {
        "gate": "brain_team_authorization_contract_drift",
        "status": "pass" if not failures else "fail",
        "contract_status": "confirmed_c_read_write_split",
        "failures": failures,
        "warnings": [
            "This evidence confirms the read/write split only; it does not prove full Brain integration closure.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
