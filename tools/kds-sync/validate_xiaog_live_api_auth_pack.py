#!/usr/bin/env python3
"""Validate XiaoG live API authorization pack evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
XIAOG_REPO = ROOT.parent / "GlobalCloud XiaoG"
DOC = ROOT / "docs/harness/XiaoG/evidence/xiaog-live-api-auth-pack-20260625.md"
BOARD = ROOT / "09-status/globalcloud-project-group-real-execution-governance-board.md"
REGISTER = ROOT / "09-status/globalcloud-core-chain-real-evidence-register.md"
STATUS = ROOT / "docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md"
BASELINE = ROOT / "docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md"
TASKS = ROOT / "docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md"

XIAOG_PLAN = XIAOG_REPO / "GlobalCloud XiaoG 实施方案.md"
XIAOG_PACKAGE = XIAOG_REPO / "package.json"
XIAOG_LOOP_STATE = XIAOG_REPO / "docs/harness/loop-state.md"
XIAOG_EVIDENCE_INDEX = XIAOG_REPO / "docs/harness/evidence/evidence-index.md"
XIAOG_VALIDATOR = XIAOG_REPO / "scripts/validate_xiaog_l4_readonly_audit_mock.py"
XIAOG_FIXTURE = XIAOG_REPO / "l4_execution/xiaog_l4_readonly_audit_notification_mock.fixture.json"

REQUIRED_DOC_TOKENS = [
    "XIAOG-LIVE-API-AUTH-PACK-001",
    "xiaog_live_api_auth_pack = controlled",
    "target_status_candidate = task_pack_ready / authorization_pack_ready",
    "harness_check = pass",
    "readonly_audit_mock = pass",
    "round = XiaoG-L4-011",
    "readonly_queries = 3",
    "pkc_notification_candidates = 1",
    "waes_audit_mocks = 2",
    "execution_traces = 1",
    "network_call_executed = false",
    "live_gfis_gpc_api_executed = false",
    "real_pkc_notification_sent = false",
    "real_waes_audit_write_executed = false",
    "device_ota_executed = false",
    "docker_deployment_executed = false",
    "token_access_executed = false",
    "production_write_executed = false",
    "accepted = false",
    "integrated = false",
    "production_ready = false",
    "customer_accepted = false",
    "xiaog_l4_readonly_audit_mock=pass",
    "不声明 live GFIS/GPC API 已验证",
    "不声明真实 WAES 审计写入已完成",
]

REQUIRED_PLAN_TOKENS = [
    "title: GlobalCloud XiaoG 实施方案",
    "project: XiaoG",
    "status: controlled",
    "master_control: GPCF:01-architecture/GlobalCloud项目群实施方案.md",
    "不声明业务实现完成、不声明客户交付完成、不声明 accepted、integrated 或 production_ready",
]

REQUIRED_PACKAGE_TOKENS = [
    '"harness:check": "node scripts/harness-check.mjs"',
    '"test": "vitest run"',
    '"build": "npm run openapi:generate && vue-tsc -b && vite build && tsc --noEmit -p packages/server/tsconfig.json && node scripts/build-server.mjs"',
]

REQUIRED_XIAOG_TOKENS = [
    "XiaoG-L4-011",
    "ReadOnlyQueryResult",
    "PkcNotificationCandidate",
    "WaesAuditWriteMock",
    "ExecutionTrace",
    "authorization_boundary",
    "network",
    "device_ota",
    "production_write",
]

REQUIRED_REF_TOKENS = [
    "XIAOG-LIVE-API-AUTH-PACK-001",
    "xiaog-live-api-auth-pack-20260625.md",
    "validate_xiaog_live_api_auth_pack.py",
    "task_pack_ready / authorization_pack_ready",
]

FORBIDDEN_CLAIMS = [
    "network_call_executed = true",
    "live_gfis_gpc_api_executed = true",
    "real_pkc_notification_sent = true",
    "real_waes_audit_write_executed = true",
    "device_ota_executed = true",
    "docker_deployment_executed = true",
    "token_access_executed = true",
    "production_write_executed = true",
    "production_ready = true",
    "accepted = true",
    "integrated = true",
    "customer_accepted = true",
]


def read(path: Path, failures: list[str]) -> str:
    if not path.exists():
        failures.append(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    failures: list[str] = []
    doc_text = read(DOC, failures)
    plan_text = read(XIAOG_PLAN, failures)
    package_text = read(XIAOG_PACKAGE, failures)
    loop_state_text = read(XIAOG_LOOP_STATE, failures)
    evidence_index_text = read(XIAOG_EVIDENCE_INDEX, failures)
    validator_text = read(XIAOG_VALIDATOR, failures)
    fixture_text = read(XIAOG_FIXTURE, failures)
    refs_text = "\n".join(
        [
            read(BOARD, failures),
            read(REGISTER, failures),
            read(STATUS, failures),
            read(BASELINE, failures),
            read(TASKS, failures),
        ]
    )

    if not XIAOG_REPO.exists():
        failures.append(f"missing XiaoG repo: {XIAOG_REPO}")

    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            failures.append(f"missing token in XiaoG auth pack evidence: {token}")

    for token in REQUIRED_PLAN_TOKENS:
        if token not in plan_text:
            failures.append(f"missing token in XiaoG implementation plan: {token}")

    for token in REQUIRED_PACKAGE_TOKENS:
        if token not in package_text:
            failures.append(f"missing script token in XiaoG package.json: {token}")

    xiaog_combined = "\n".join([loop_state_text, evidence_index_text, validator_text, fixture_text])
    for token in REQUIRED_XIAOG_TOKENS:
        if token not in xiaog_combined:
            failures.append(f"missing token in XiaoG source evidence: {token}")

    if fixture_text:
        try:
            fixture = json.loads(fixture_text)
        except json.JSONDecodeError as exc:
            failures.append(f"invalid XiaoG fixture json: {exc}")
        else:
            if fixture.get("round_id") != "XiaoG-L4-011":
                failures.append("XiaoG fixture round_id mismatch")
            expected = fixture.get("expected_outputs", {})
            if expected.get("readonly_queries") != 3:
                failures.append("XiaoG readonly query count mismatch")
            if expected.get("pkc_notification_candidates") != 1:
                failures.append("XiaoG PKC notification candidate count mismatch")
            if expected.get("waes_audit_write_mocks") != 2:
                failures.append("XiaoG WAES audit mock count mismatch")
            for key in [
                "production_write_allowed",
                "real_external_api_write_allowed",
                "network_call_allowed",
                "device_ota_allowed",
                "docker_deployment_allowed",
                "permission_change_allowed",
                "token_access_allowed",
                "accepted_integrated_allowed",
            ]:
                if fixture.get(key) is not False:
                    failures.append(f"XiaoG fixture boundary must remain false: {key}")

    for token in REQUIRED_REF_TOKENS:
        if token not in refs_text:
            failures.append(f"missing token in governance references: {token}")

    combined = doc_text + "\n" + refs_text
    for token in FORBIDDEN_CLAIMS:
        if token in combined:
            failures.append(f"forbidden positive XiaoG claim: {token}")

    result = {
        "gate": "xiaog_live_api_auth_pack",
        "status": "pass" if not failures else "fail",
        "task_id": "XIAOG-LIVE-API-AUTH-PACK-001",
        "target_status_candidate": "task_pack_ready / authorization_pack_ready",
        "harness_check": "pass",
        "readonly_queries": 3,
        "pkc_notification_candidates": 1,
        "waes_audit_mocks": 2,
        "network_call_executed": False,
        "device_ota_executed": False,
        "production_write_executed": False,
        "failures": failures,
        "warnings": [
            "This validates XiaoG authorization pack readiness only; it does not validate live API execution, device OTA, Docker deployment, production writes, accepted, integrated, or customer acceptance status.",
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
