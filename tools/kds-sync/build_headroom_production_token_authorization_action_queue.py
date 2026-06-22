#!/usr/bin/env python3
"""Build the Headroom production-token authorization action queue."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUTHORIZATION_PACKAGE = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
LEDGER_TEMPLATE = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
LEDGER_NEGATIVE_FIXTURES = ROOT / "fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md"


ACTIONS = [
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-001",
        "title": "define authorized measurement window",
        "owner": "human_approver",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "authorized_window_id",
        "status": "pending_human_authorization",
        "gate": False,
    },
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-002",
        "title": "name approving owner and approval timestamp",
        "owner": "human_approver",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "authorized_by_and_authorized_at",
        "status": "pending_human_authorization",
        "gate": False,
    },
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-003",
        "title": "attach sanitized production token usage ledger",
        "owner": "KDS",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "provider_billing_export_or_sanitized_runtime_usage_ledger",
        "status": "pending_sanitized_ledger",
        "gate": False,
    },
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-004",
        "title": "attach rollback plan id",
        "owner": "WAES",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "rollback_plan_id",
        "status": "pending_rollback_plan",
        "gate": False,
    },
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-005",
        "title": "rerun production token ledger negative fixtures and evaluator",
        "owner": "GPCF",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "negative_fixture_validator_and_ledger_evaluator_output",
        "status": "pending_authorized_ledger",
        "gate": False,
    },
    {
        "action_id": "HEADROOM-PROD-TOKEN-AUTH-ACTION-006",
        "title": "confirm no telemetry, raw prompt, external write, or KDS write",
        "owner": "GPCF",
        "due_loop": "GPCF-HEADROOM-PRODUCTION-TOKEN-AUTHORIZED-MEASUREMENT-001",
        "required_evidence": "security_non_claims_confirmation",
        "status": "pending_authorized_window",
        "gate": False,
    },
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_markdown(result: dict) -> str:
    rows = "\n".join(
        "| {action_id} | {owner} | {status} | {gate} | {due_loop} |".format(
            action_id=action["action_id"],
            owner=action["owner"],
            status=action["status"],
            gate=str(action["gate"]).lower(),
            due_loop=action["due_loop"],
        )
        for action in result["actions"]
    )
    return f"""---
doc_id: GPCF-DOC-73DAD5F3AB
title: Headroom Production Token Authorization Action Queue
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md
source_path: docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Production Token Authorization Action Queue

## Evidence ID

`{result["evidence_id"]}`

## 结论

本队列把 Headroom 生产 token 授权采集包拆成可执行、可审计、可阻断的行动项。

`authorization_action_queue_gate | {str(result["gate"]["authorization_action_queue_gate"]).lower()}`，`production_admission_gate | false`，`measured_production_tokens | false`。

当前所有行动项仍需人工授权窗口或真实脱敏台账，因此本队列是阻断队列，不是授权证明。

## 行动队列

| action_id | owner | status | gate | due_loop |
|---|---|---|---|---|
{rows}

## 不允许声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不保存 raw prompt、raw completion、secret 或 authorization header。
- 不升级 accepted、integrated 或 production_ready。
"""


def main() -> int:
    authorization_package = load_json(AUTHORIZATION_PACKAGE)
    ledger_template = load_json(LEDGER_TEMPLATE)
    negative_fixtures = load_json(LEDGER_NEGATIVE_FIXTURES)
    require(authorization_package["authorization"]["status"] == "pending", "authorization package must remain pending")
    require(authorization_package["gate"]["authorization_package_gate"] is False, "authorization package gate must remain false")
    require(ledger_template["measured_production_tokens"] is False, "ledger template must not claim production tokens")
    require(len(negative_fixtures.get("cases", [])) >= 5, "negative fixture set too small")

    result = {
        "evidence_id": "HEADROOM-PRODUCTION-TOKEN-AUTHORIZATION-ACTION-QUEUE-20260621",
        "date": "2026-06-21",
        "status": "authorization_action_queue_defined_blocking",
        "source_evidence": [rel(AUTHORIZATION_PACKAGE), rel(LEDGER_TEMPLATE), rel(LEDGER_NEGATIVE_FIXTURES)],
        "actions": ACTIONS,
        "gate": {
            "action_count": len(ACTIONS),
            "all_actions_have_owner": all(bool(action["owner"]) for action in ACTIONS),
            "all_actions_have_due_loop": all(bool(action["due_loop"]) for action in ACTIONS),
            "all_actions_closed": False,
            "authorization_action_queue_gate": False,
            "production_admission_gate": False,
        },
        "decision": {
            "next_required_action": "complete all action queue items with human authorization before production token measurement",
            "production_admission_gate": False,
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_production_token_authorization_action_queue=pass "
        "action_count=6 authorization_action_queue_gate=false "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
