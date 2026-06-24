#!/usr/bin/env python3
"""Validate that the core-chain evidence baseline does not overclaim runtime or delivery."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

FORBIDDEN_CLAIMS = [
    "真实运行完成",
    "真实集成完成",
    "真实交付完成",
    "客户验收通过",
    "production_ready",
    "integrated",
    "accepted",
]

ALLOWED_CONTEXTS = [
    "不声明",
    "不得声明",
    "不把",
    "不能",
    "不可",
    "customer_accepted",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    text = REGISTER.read_text(encoding="utf-8") if REGISTER.exists() else ""

    if not text:
        failures.append(f"missing register: {REGISTER}")

    for forbidden in FORBIDDEN_CLAIMS:
        start = 0
        while True:
            idx = text.find(forbidden, start)
            if idx == -1:
                break
            line_start = text.rfind("\n", 0, idx) + 1
            line_end = text.find("\n", idx)
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if not any(context in line for context in ALLOWED_CONTEXTS):
                failures.append(f"forbidden positive claim appears without boundary: {line}")
            start = idx + len(forbidden)

    warnings.append("claim gate checks wording only; it does not prove runtime evidence")

    result = {
        "gate": "core_chain_runtime_claims",
        "status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
