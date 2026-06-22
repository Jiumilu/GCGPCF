#!/usr/bin/env python3
"""Run Headroom LCX sanitized metadata replay check.

This is a check-only replay over sanitized ledger metadata. It verifies field
mapping, project marker, gate marker, and evidence schema compatibility without
reading raw content or calculating production savings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER_JSON = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
DRY_RUN_JSON = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md"

PROJECTS = [
    "GPCF",
    "KDS",
    "Brain",
    "WAES",
    "GFIS",
    "GPC",
    "PVAOS",
    "Edge",
    "PKC",
    "XiaoC",
    "XGD",
    "XiaoG",
    "MMC",
    "Studio",
    "WAS",
]

FIELD_MAP = {
    "measurement_id": "task_id_candidate",
    "project": "project_id",
    "scenario": "content_type",
    "source_kind": "content_source_kind",
    "input_tokens_before": "tokens_before_input",
    "input_tokens_after": "tokens_after_input",
    "output_tokens_before": "tokens_before_output",
    "output_tokens_after": "tokens_after_output",
    "cache_write_tokens_before": "cache_write_tokens_before",
    "cache_write_tokens_after": "cache_write_tokens_after",
    "cache_read_tokens_before": "cache_read_tokens_before",
    "cache_read_tokens_after": "cache_read_tokens_after",
    "retrieval_miss_count": "ccr_retrieval_miss_count",
    "answer_equivalence": "answer_equivalence",
    "sensitive_redaction_gate": "sensitive_redaction_gate",
    "project_marker_gate": "marker_gate",
    "rollback_plan_id": "rollback_plan_id",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="required; replay does not calculate savings")
    args = parser.parse_args()
    require(args.check_only, "--check-only is required")

    ledger = load_json(LEDGER_JSON)
    dry_run = load_json(DRY_RUN_JSON)
    entries = ledger.get("entries", [])
    require(isinstance(entries, list), "ledger entries must be a list")

    replay_records = []
    mapping_failures = []
    marker_failures = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            mapping_failures.append(f"entry_{index}:not_object")
            continue
        missing = [field for field in FIELD_MAP if field not in entry]
        if missing:
            mapping_failures.append(f"entry_{index}:missing:{','.join(missing)}")
            continue
        if entry["project"] not in PROJECTS:
            marker_failures.append(f"entry_{index}:project_out_of_scope")
        if entry["sensitive_redaction_gate"] != "pass":
            marker_failures.append(f"entry_{index}:sensitive_redaction_gate_not_pass")
        if entry["project_marker_gate"] not in {"pass", "not_measured"}:
            marker_failures.append(f"entry_{index}:project_marker_gate_invalid")

        replay_records.append({mapped: entry[source] for source, mapped in FIELD_MAP.items()})

    schema_checks = {
        "ledger_is_sanitized_precheck_template": ledger.get("ledger_type") == "sanitized_production_token_usage_ledger_precheck_template",
        "dry_run_gate_passed": dry_run.get("gates", {}).get("sanitized_measurement_dry_run_gate") is True,
        "dry_run_check_only": dry_run.get("gates", {}).get("check_only") is True,
        "no_raw_prompt": ledger.get("contains_raw_prompt") is False,
        "no_raw_completion": ledger.get("contains_raw_completion") is False,
        "no_customer_contract_text": ledger.get("contains_customer_contract_text") is False,
        "no_provider_secret": ledger.get("contains_provider_secret") is False,
        "telemetry_off": ledger.get("telemetry") == "off",
    }
    replay_gate = all(schema_checks.values()) and not mapping_failures and not marker_failures
    result = {
        "evidence_id": "HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622",
        "task_id": "GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001",
        "date": "2026-06-22",
        "status": "metadata_replay_check_pass_no_measurement" if replay_gate else "metadata_replay_check_blocked",
        "scope": "sanitized_metadata_replay_check_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "source_ledger": LEDGER_JSON.relative_to(ROOT).as_posix(),
        "source_dry_run": DRY_RUN_JSON.relative_to(ROOT).as_posix(),
        "entry_count": len(entries),
        "replay_record_count": len(replay_records),
        "field_map": FIELD_MAP,
        "mapping_failures": mapping_failures,
        "marker_failures": marker_failures,
        "schema_checks": schema_checks,
        "replay_records": replay_records,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "metadata_replay_check_only",
        },
        "gates": {
            "metadata_replay_gate": replay_gate,
            "field_mapping_gate": not mapping_failures,
            "project_marker_gate": not marker_failures,
            "evidence_schema_gate": all(schema_checks.values()),
            "check_only": True,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""---
doc_id: GPCF-DOC-1F18B14E93
title: Headroom LCX Metadata Replay Check Evidence 20260622
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md
source_path: docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Metadata Replay Check Evidence 20260622

## Evidence ID

`HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622`

## 结论

本轮只执行 `--check-only` 元数据 replay 校验。已验证脱敏台账字段映射、项目标记、gate marker 和 evidence schema；未计算真实生产 token 节省，未读取原文，未启动 proxy。

## 门禁

| 项 | 当前值 |
|---|---|
| metadata_replay_gate | {str(replay_gate).lower()} |
| field_mapping_gate | {str(not mapping_failures).lower()} |
| project_marker_gate | {str(not marker_failures).lower()} |
| evidence_schema_gate | {str(all(schema_checks.values())).lower()} |
| check_only | true |
| entry_count | {len(entries)} |
| replay_record_count | {len(replay_records)} |
| saving_rate | not_calculated |
| tokens_saved | not_calculated |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一步

下一轮可建立 marker/retrieval miss 对比门禁，但仍不得读取原文、不得计算真实生产节省、不得启动生产代理。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    loop = """---
doc_id: GPCF-DOC-A7161F4187
title: Loop Round GPCF Headroom LCX Metadata Replay Check 001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Metadata Replay Check 001

## 输入

- 上轮已建立 sanitized measurement dry-run skeleton。
- 本轮只允许 check-only metadata replay。

## 动作

- 运行 `python3 tools/kds-sync/run_headroom_lcx_metadata_replay_check.py --check-only`。
- 校验字段映射、项目标记、gate marker 和 evidence schema。
- 不读取原文、不计算真实生产节省、不启动 production proxy。

## 输出

- `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`
- `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_metadata_replay_check.py`
- `python3 tools/kds-sync/validate_headroom_lcx_sanitized_measurement_dry_run.py`

## 反馈

- metadata replay 校验已建立。
- 当前仍不得进入生产 token 测量。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

建立 marker/retrieval miss 对比门禁；仍不得读取原文或启动生产代理。
"""
    LOOP_ROUND.write_text(loop, encoding="utf-8")

    print(
        "headroom_lcx_metadata_replay_check="
        f"{'pass_check_only' if replay_gate else 'blocked'} "
        f"project_count=15 entry_count={len(entries)} replay_record_count={len(replay_records)} "
        "check_only=true saving_rate=not_calculated measured_production_tokens=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
