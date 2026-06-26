#!/usr/bin/env python3
"""Validate project-group authorization routing evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/harness/evidence/globalcloud-project-group-authorization-routing-20260625.md"
REVIEW = ROOT / "docs/harness/evidence/globalcloud-project-group-review-packages-20260625.md"
CONFIRM = ROOT / "docs/harness/evidence/globalcloud-project-group-human-confirmation-request-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"

ROUTES = [
    "ROUTE-GPC-EVIDENCE-BROWSER-20260625",
    "ROUTE-PVAOS-RELEASE-GATE-20260625",
    "ROUTE-GPCF-GOVERNANCE-EVIDENCE-20260625",
    "ROUTE-GPCF-KDS-MIRROR-20260625",
    "ROUTE-WAS-SYSTEM-NOISE-20260625",
    "ROUTE-KDS-FUNDING-REPORT-20260625",
    "ROUTE-SOP-WUHAN-SCENARIO-20260625",
]

PACKAGES = [
    "PKG-GPC-EVIDENCE-BROWSER-20260625",
    "PKG-PVAOS-RELEASE-GATE-20260625",
    "PKG-GPCF-GOVERNANCE-EVIDENCE-20260625",
    "PKG-GPCF-KDS-MIRROR-20260625",
    "HOLD-WAS-SYSTEM-NOISE-20260625",
    "HOLD-KDS-FUNDING-REPORT-20260625",
    "HOLD-SOP-WUHAN-SCENARIO-20260625",
]

REQUIRED_DOC_TOKENS = [
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
    "project_group_authorization_routing = prepared",
    "authorization_routing_ready = true",
    "confirmation_item_count = 7",
    "review_package_count = 4",
    "hold_package_count = 3",
    "review_allowed = false",
    "stage_allowed = false",
    "commit_allowed = false",
    "push_allowed = false",
    "delete_allowed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "none_until_user_confirmation",
    "动作门禁",
    "状态传导规则",
    "回滚与降级",
]

REQUIRED_SOURCE_TOKENS = [
    "project_group_review_packages = controlled",
    "human_confirmation_request = prepared",
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
]

REQUIRED_REFERENCE_TOKENS = [
    "GPCF-AUTHORIZATION-PACKAGE-ROUTING-001",
    "globalcloud-project-group-authorization-routing-20260625.md",
    "validate_project_group_authorization_routing.py",
    "authorization_routing_ready",
]

FORBIDDEN_POSITIVE_CLAIMS = [
    "review_allowed = true",
    "stage_allowed = true",
    "commit_allowed = true",
    "push_allowed = true",
    "delete_allowed = true",
    "accepted = true",
    "integrated = true",
    "production_ready = true",
    "customer_accepted = true",
    "真实 KDS API 已同步 = true",
    "项目群可提交 = true",
    "项目群可推送 = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    sources_text = "\n".join([read(REVIEW, failures), read(CONFIRM, failures), read(TASKS, failures)])
    refs_text = "\n".join([read(BOARD, failures), read(REGISTER, failures), read(STATUS, failures)])

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in authorization routing evidence: {token}")

    for route in ROUTES:
        if route not in doc_text:
            failures.append(f"missing authorization route: {route}")

    for package in PACKAGES:
        if package not in doc_text:
            failures.append(f"missing package in authorization routing: {package}")
        if package not in sources_text:
            failures.append(f"missing package in source review/confirmation docs: {package}")

    for token in REQUIRED_SOURCE_TOKENS:
        if token not in sources_text:
            failures.append(f"missing token in routing source docs: {token}")

    for token in REQUIRED_REFERENCE_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_POSITIVE_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive authorization claim: {token}")

    result = {
        "gate": "project_group_authorization_routing",
        "status": "pass" if not failures else "fail",
        "authorization_routing": "prepared",
        "route_count": len(ROUTES),
        "failures": failures,
        "warnings": [
            "This validates authorization routing only; it does not grant review, stage, commit, push, delete, accepted, integrated, or customer acceptance authority.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
