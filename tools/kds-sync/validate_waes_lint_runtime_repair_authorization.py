#!/usr/bin/env python3
"""Validate WAES lint/runtime repair authorization package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTH_DOC = ROOT / "docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_AUTH_TOKENS = [
    "WAES lint runtime 修复授权包 2026-06-25",
    "WAES-LINT-RUNTIME-001",
    "waes/integration-release",
    "dirty = true",
    "npm run lint",
    "src/app/components/AppLazyImports.ts",
    "Parsing error: '>' expected",
    "src/app/plugin/PluginManager.tsx",
    "Parsing error: Identifier expected",
    "我确认执行 WAES-LINT-RUNTIME-001",
    "allowed_touches",
    "npm run check",
    "git_commit",
    "git_push",
    "deployment",
    "permission_change",
    "production_write",
    "waes_lint_runtime_repair_authorization = required",
    "waes_status = repair_required",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "waes-lint-runtime-repair-authorization-20260625.md",
    "WAES-LINT-RUNTIME-001",
    "authorization",
    "repair_required",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "WAES 真实运行闭环完成",
    "WAES 已通过 `npm run check`",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不是修复结果", "不得", "禁止"]


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
    auth_text = read(AUTH_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_AUTH_TOKENS:
        if token not in auth_text:
            failures.append(f"missing token in WAES authorization package: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in WAES references/register: {token}")

    check_forbidden(auth_text + "\n" + refs_text, failures)

    result = {
        "gate": "waes_lint_runtime_repair_authorization",
        "status": "pass" if not failures else "fail",
        "authorization_status": "required",
        "failures": failures,
        "warnings": [
            "This validates the authorization package only; it does not modify WAES source files.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
