#!/usr/bin/env python3
"""Validate Brain authorized closure refresh execution evidence boundaries."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXECUTION = ROOT / "docs/harness/Brain/evidence/brain-authorized-closure-refresh-execution-20260625.md"
README = ROOT / "docs/harness/Brain/evidence/README.md"
INDEX = ROOT / "docs/harness/Brain/evidence/evidence-index.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EXECUTION_TOKENS = [
    "Brain 授权型闭包证据刷新执行结果 2026-06-25",
    "allowed_environment = local dev only",
    "backend-write-closure-20260621.json",
    "bulk-fix-acceptance-readback-20260622.json",
    "chat-llm-prompt-20260621.json",
    "project_id=project-16b83cc0",
    "execution_id=bulk-fix-exec-01249afa30ff",
    "model=deepseek-chat-gehua",
    "totalTokens=44",
    "npm run validate:completion-matrix",
    "brain_completion_matrix=pass",
    "npm run validate:harness-evidence",
    "brain_harness_evidence=pass",
    "npm run validate:loop-harness",
    "brain_loop_harness=pass",
    "ready_for_review / authorization_boundary",
    "brain_authorized_closure_refresh_result = verified_with_authorization_boundary",
    "不声明客户验收通过",
    "不升级为 `accepted`、`integrated` 或 `production_ready`",
]

REQUIRED_REFERENCE_TOKENS = [
    "brain-authorized-closure-refresh-execution-20260625.md",
    "brain_authorized_closure_refresh_result",
    "verified_with_authorization_boundary",
    "bulk-fix-exec-01249afa30ff",
    "ready_for_review / authorization_boundary",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "Brain 真实交付完成",
    "客户验收通过",
    "production_ready",
    "accepted",
    "integrated",
]

ALLOWED_CONTEXTS = [
    "不声明",
    "不升级",
    "不得",
    "禁止",
    "forbidden",
    "需人工确认",
    "not_claimed",
    "outside this authorization scope",
    "当前不得声明",
    "customer_acceptance_claim",
    "accepted_or_integrated_upgrade",
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
    execution_text = read(EXECUTION, failures)
    combined_refs = "\n".join(
        [
            read(README, failures),
            read(INDEX, failures),
            read(REGISTER, failures),
        ],
    )

    for token in REQUIRED_EXECUTION_TOKENS:
        if token not in execution_text:
            failures.append(f"missing token in Brain execution evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in combined_refs:
            failures.append(f"missing token in Brain references/register: {token}")

    check_forbidden(execution_text + "\n" + combined_refs, failures)

    result = {
        "gate": "brain_authorized_closure_refresh_execution",
        "status": "pass" if not failures else "fail",
        "execution_status": "verified_with_authorization_boundary",
        "failures": failures,
        "warnings": [
            "This validates local-dev authorization evidence only; it does not approve production, delivery, customer acceptance, accepted, integrated, or production_ready status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
