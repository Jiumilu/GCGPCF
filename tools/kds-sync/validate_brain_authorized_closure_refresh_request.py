#!/usr/bin/env python3
"""Validate Brain authorized closure refresh request boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REQUEST = ROOT / "docs/harness/Brain/evidence/brain-authorized-closure-refresh-request-20260625.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_REQUEST_TOKENS = [
    "Brain 授权型闭包证据刷新请求 2026-06-25",
    "brain_authorized_closure_refresh = authorization_required",
    "backend-write-closure-20260621.json",
    "bulk-fix-acceptance-execution",
    "chat-llm-prompt-20260621.json",
    "authorization_required",
    "local dev only",
    "production_write",
    "permission_change",
    "accepted_or_integrated_upgrade",
    "我确认执行 Brain 授权型闭包证据刷新 2026-06-25",
    "不得自动声明",
]

REQUIRED_REGISTER_TOKENS = [
    "brain-authorized-closure-refresh-request-20260625.md",
    "brain_authorized_closure_refresh",
    "用户已确认",
    "brain-authorized-closure-refresh-execution-20260625.md",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "Brain 真实集成完成",
    "Brain 真实交付完成",
    "客户验收通过",
    "production_ready",
]

ALLOWED_CONTEXTS = [
    "不得",
    "不表示",
    "不声明",
    "禁止",
    "仍不得",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def check_forbidden(text: str, failures: list[str]) -> None:
    for token in FORBIDDEN_POSITIVE_CLAIMS:
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
                failures.append(f"forbidden positive claim without boundary: {line}")
            start = idx + len(token)


def main() -> int:
    failures: list[str] = []
    request_text = read(REQUEST, failures)
    register_text = read(REGISTER, failures)

    for token in REQUIRED_REQUEST_TOKENS:
        if token not in request_text:
            failures.append(f"missing token in authorization request: {token}")

    for token in REQUIRED_REGISTER_TOKENS:
        if token not in register_text:
            failures.append(f"missing token in core-chain register: {token}")

    check_forbidden(request_text + "\n" + register_text, failures)

    result = {
        "gate": "brain_authorized_closure_refresh_request",
        "status": "pass" if not failures else "fail",
        "authorization_status": "authorization_required",
        "failures": failures,
        "warnings": [
            "This validates the authorization request only; it does not execute writes, bulk-fix, or LLM prompt.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
