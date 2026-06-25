#!/usr/bin/env python3
"""Validate XWAIL minimal validator runtime evidence and references."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DOC = ROOT / "docs/harness/XWAIL/evidence/xwail-min-validator-runtime-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"

REQUIRED_EVIDENCE_TOKENS = [
    "XWAIL 最小 Validator/XAP 运行证据 2026-06-25",
    "XWAIL-MIN-VALIDATOR-001",
    "scripts/validate_xwail.py",
    "scripts/build_xap.py",
    "scripts/verify_xap.py",
    "can't open file",
    "scripts/xwail_common.py",
    "models/examples/warehouse-basic.xwail.json",
    "packages/examples/logistics/manifest.xap.json",
    "schemas-json/xwail-core.schema.json",
    "schemas-json/xap-manifest.schema.json",
    "Physical",
    "Rule",
    "Intellectual",
    "Data",
    "Economic",
    "Energy",
    "Organization",
    "SpaceTime",
    "ontologyRef",
    "python3 scripts/validate_xwail.py --all",
    "python3 scripts/build_xap.py --check",
    "python3 scripts/verify_xap.py --all",
    "issue_count=0",
    "high_count=0",
    "xwail_min_validator = verified_with_local_dev_boundary",
    "xwail_status_candidate = ready_for_review",
    "waes_status = Draft",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
]

REQUIRED_REFERENCE_TOKENS = [
    "xwail-min-validator-runtime-20260625.md",
    "XWAIL-MIN-VALIDATOR-001",
    "verified_with_local_dev_boundary",
    "WAES -> XWAIL -> AaaS",
    "ready_for_review",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "完整 XWAIL 工具链完成",
    "WAES 发布完成",
    "AaaS 绑定完成",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
]

ALLOWED_CONTEXTS = ["不声明", "不代表", "未", "没有", "Draft", "不得"]


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
    evidence_text = read(EVIDENCE_DOC, failures)
    refs_text = read(BOARD, failures) + "\n" + read(REGISTER, failures)

    for token in REQUIRED_EVIDENCE_TOKENS:
        if token not in evidence_text:
            failures.append(f"missing token in XWAIL min validator evidence: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in XWAIL references/register: {token}")

    check_forbidden(evidence_text + "\n" + refs_text, failures)

    result = {
        "gate": "xwail_min_validator_runtime",
        "status": "pass" if not failures else "fail",
        "runtime_status": "verified_with_local_dev_boundary",
        "failures": failures,
        "warnings": [
            "This validates minimum local validator evidence only; it does not prove full XWAIL tooling, WAES publication, AaaS binding, or customer acceptance.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
