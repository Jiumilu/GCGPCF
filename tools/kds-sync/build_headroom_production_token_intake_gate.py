#!/usr/bin/env python3
"""Build the Headroom production-token intake gate evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADMISSION_JSON = ROOT / "docs/harness/evidence/headroom-project-group-admission-20260621.json"
INDEPENDENT_REPLAY_JSON = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json"
LEDGER_TEMPLATE_JSON = ROOT / "fixtures/headroom/headroom-production-token-ledger-template.json"
LEDGER_TEMPLATE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_template.py"
LEDGER_EVALUATOR = ROOT / "tools/kds-sync/evaluate_headroom_production_token_ledger.py"
LEDGER_NEGATIVE_FIXTURES = ROOT / "fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json"
LEDGER_NEGATIVE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py"
AUTHORIZATION_PACKAGE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-package-20260621.json"
AUTHORIZATION_PACKAGE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_package.py"
AUTHORIZATION_ACTION_QUEUE_JSON = ROOT / "docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json"
AUTHORIZATION_ACTION_QUEUE_VALIDATOR = ROOT / "tools/kds-sync/validate_headroom_production_token_authorization_action_queue.py"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-production-token-intake-gate-20260621.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_markdown(result: dict) -> str:
    gate = result["gate"]
    return f"""---
doc_id: GPCF-DOC-8D2B6B6946
title: Headroom Production Token Intake Gate Evidence
project: KDS
related_projects: [WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-production-token-intake-gate-20260621.md
source_path: docs/harness/evidence/headroom-production-token-intake-gate-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Production Token Intake Gate Evidence

## Evidence ID

`{result["evidence_id"]}`

## 结论

本轮建立 Headroom 生产 token 实测采集前置门禁，定义真实采集前必须满足的输入、脱敏、安全、等价性、成本和回滚条件。

`production_token_intake_gate | {str(gate["production_token_intake_gate"]).lower()}`，`measured_production_tokens | false`，`production_admission_gate | false`。

当前没有受控生产 token 账单、脱敏调用日志或人工授权窗口，因此本门禁是可执行的阻断门禁，不是生产接入证明。

## 采集前置条件

| 条件 | 要求 |
|---|---|
| authorized_window_required | true |
| telemetry_required | off |
| raw_prompt_storage | forbidden |
| token_source | provider billing export or sanitized runtime usage ledger |
| project_marker_required | true |
| answer_equivalence_required | true |
| rollback_plan_required | true |
| kds_write_allowed | false |
| external_api_write_allowed | false |
| ledger_template | `fixtures/headroom/headroom-production-token-ledger-template.json` |
| ledger_template_validator | `tools/kds-sync/validate_headroom_production_token_ledger_template.py` |
| ledger_evaluator | `tools/kds-sync/evaluate_headroom_production_token_ledger.py` |
| negative_fixtures | `fixtures/headroom/headroom-production-token-ledger-negative-fixtures.json` |
| negative_validator | `tools/kds-sync/validate_headroom_production_token_ledger_negative_fixtures.py` |
| authorization_package | `docs/harness/evidence/headroom-production-token-authorization-package-20260621.json` |
| authorization_package_validator | `tools/kds-sync/validate_headroom_production_token_authorization_package.py` |
| authorization_action_queue | `docs/harness/evidence/headroom-production-token-authorization-action-queue-20260621.json` |
| authorization_action_queue_validator | `tools/kds-sync/validate_headroom_production_token_authorization_action_queue.py` |

## 当前门禁

| 字段 | 当前值 |
|---|---|
| production_source_present | {str(gate["production_source_present"]).lower()} |
| sanitized_usage_ledger_present | {str(gate["sanitized_usage_ledger_present"]).lower()} |
| authorized_window_present | {str(gate["authorized_window_present"]).lower()} |
| telemetry_off_enforced | {str(gate["telemetry_off_enforced"]).lower()} |
| no_sensitive_raw_text_stored | {str(gate["no_sensitive_raw_text_stored"]).lower()} |
| independent_replay_gate | {str(gate["independent_replay_gate"]).lower()} |
| authorization_action_queue_gate | {str(gate["authorization_action_queue_gate"]).lower()} |
| production_token_intake_gate | {str(gate["production_token_intake_gate"]).lower()} |
| production_admission_gate | false |

## 下一步

必须先取得人工授权的采集窗口和脱敏 token 使用台账，再运行生产 token 成本模型；未满足前不得申请 L3.5/L4 admission、accepted、integrated 或 production_ready。
"""


def main() -> int:
    admission = load_json(ADMISSION_JSON)
    replay = load_json(INDEPENDENT_REPLAY_JSON)
    authorization_action_queue = load_json(AUTHORIZATION_ACTION_QUEUE_JSON)
    require(admission["project_group"]["accepted"] is False, "accepted must remain false")
    require(admission["project_group"]["integrated"] is False, "integrated must remain false")
    require(admission["project_group"]["production_ready"] is False, "production_ready must remain false")
    require(replay["decision"]["independent_round_gate"] is True, "independent replay gate must pass first")
    require(replay["measured_production_tokens"] is False, "independent replay must not claim production tokens")
    require(authorization_action_queue["gate"]["authorization_action_queue_gate"] is False, "authorization action queue must remain blocked")
    require(authorization_action_queue["measured_production_tokens"] is False, "authorization action queue must not claim production tokens")

    prerequisites = {
        "authorized_window_required": True,
        "telemetry_required": "off",
        "raw_prompt_storage": "forbidden",
        "token_source": "provider_billing_export_or_sanitized_runtime_usage_ledger",
        "project_marker_required": True,
        "answer_equivalence_required": True,
        "rollback_plan_required": True,
        "kds_write_allowed": False,
        "external_api_write_allowed": False,
    }
    gate = {
        "production_source_present": False,
        "sanitized_usage_ledger_present": False,
        "authorized_window_present": False,
        "telemetry_off_enforced": True,
        "no_sensitive_raw_text_stored": True,
        "independent_replay_gate": True,
        "authorization_action_queue_gate": False,
        "production_token_intake_gate": False,
        "production_admission_gate": False,
    }
    result = {
        "evidence_id": "HEADROOM-PRODUCTION-TOKEN-INTAKE-GATE-20260621",
        "date": "2026-06-21",
        "status": "production_token_intake_gate_defined_blocking",
        "source_evidence": [rel(ADMISSION_JSON), rel(INDEPENDENT_REPLAY_JSON)],
        "ledger_template": rel(LEDGER_TEMPLATE_JSON),
        "ledger_template_validator": rel(LEDGER_TEMPLATE_VALIDATOR),
        "ledger_evaluator": rel(LEDGER_EVALUATOR),
        "ledger_negative_fixtures": rel(LEDGER_NEGATIVE_FIXTURES),
        "ledger_negative_validator": rel(LEDGER_NEGATIVE_VALIDATOR),
        "authorization_package": rel(AUTHORIZATION_PACKAGE_JSON),
        "authorization_package_validator": rel(AUTHORIZATION_PACKAGE_VALIDATOR),
        "authorization_action_queue": rel(AUTHORIZATION_ACTION_QUEUE_JSON),
        "authorization_action_queue_validator": rel(AUTHORIZATION_ACTION_QUEUE_VALIDATOR),
        "prerequisites": prerequisites,
        "required_measurement_fields": [
            "measurement_id",
            "project",
            "scenario",
            "authorized_window_id",
            "input_tokens_before",
            "input_tokens_after",
            "output_tokens_before",
            "output_tokens_after",
            "cache_write_tokens_before",
            "cache_write_tokens_after",
            "cache_read_tokens_before",
            "cache_read_tokens_after",
            "P_in",
            "P_out",
            "P_cache_write",
            "P_cache_read",
            "P_runtime",
            "answer_equivalence",
            "retrieval_miss_count",
            "sensitive_redaction_gate",
        ],
        "gate": gate,
        "decision": {
            "next_required_action": "collect an authorized sanitized production token usage ledger before any production admission claim",
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
        "headroom_production_token_intake_gate=pass "
        "production_token_intake_gate=false "
        "measured_production_tokens=false "
        "production_admission_gate=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
