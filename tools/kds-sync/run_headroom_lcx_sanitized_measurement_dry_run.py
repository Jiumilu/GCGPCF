#!/usr/bin/env python3
"""Run Headroom LCX sanitized measurement dry-run precheck.

This runner is intentionally check-only. It validates the sanitized ledger
metadata boundary and writes Harness evidence, but it does not measure real
production token savings or start any Headroom proxy.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEDGER_JSON = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
ADMISSION_JSON = ROOT / "docs/harness/evidence/headroom-lcx-waes-harness-admission-decision-admitted-20260622.json"
AUTHORIZED_PRECHECK_JSON = ROOT / "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md"

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

REQUIRED_ENTRY_FIELDS = [
    "measurement_id",
    "project",
    "scenario",
    "source_kind",
    "input_tokens_before",
    "input_tokens_after",
    "output_tokens_before",
    "output_tokens_after",
    "cache_write_tokens_before",
    "cache_write_tokens_after",
    "cache_read_tokens_before",
    "cache_read_tokens_after",
    "retrieval_miss_count",
    "answer_equivalence",
    "sensitive_redaction_gate",
    "project_marker_gate",
    "rollback_plan_id",
]


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
    parser.add_argument("--check-only", action="store_true", help="required; do not execute measurement")
    args = parser.parse_args()
    require(args.check_only, "--check-only is required; measurement execution is not implemented")

    ledger = load_json(LEDGER_JSON)
    admission = load_json(ADMISSION_JSON)
    precheck = load_json(AUTHORIZED_PRECHECK_JSON)

    entries = ledger.get("entries", [])
    require(isinstance(entries, list), "ledger entries must be a list")
    missing_entry_fields = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            missing_entry_fields.append(f"entry_{index}:not_object")
            continue
        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                missing_entry_fields.append(f"entry_{index}:{field}")

    boundary = {
        "telemetry_off": ledger.get("telemetry") == "off",
        "sensitive_raw_text_stored": ledger.get("sensitive_raw_text_stored") is False,
        "contains_raw_prompt": ledger.get("contains_raw_prompt") is False,
        "contains_raw_completion": ledger.get("contains_raw_completion") is False,
        "contains_customer_contract_text": ledger.get("contains_customer_contract_text") is False,
        "contains_provider_secret": ledger.get("contains_provider_secret") is False,
        "contains_authorization_header": ledger.get("contains_authorization_header") is False,
        "ledger_production_measurement_allowed": ledger.get("production_token_measurement_allowed") is False,
        "ledger_measured_production_tokens": ledger.get("measured_production_tokens") is False,
        "waes_harness_admitted": admission.get("gates", {}).get("waes_harness_admitted") is True,
        "authorized_precheck_gate": precheck.get("gates", {}).get("authorized_measurement_precheck_gate") is True,
    }
    dry_run_gate = all(boundary.values()) and not missing_entry_fields

    result = {
        "evidence_id": "HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-20260622",
        "task_id": "GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001",
        "date": "2026-06-22",
        "status": "check_only_dry_run_ready_no_measurement" if dry_run_gate else "check_only_dry_run_blocked",
        "scope": "sanitized_ledger_metadata_check_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "ledger_id": ledger.get("ledger_id"),
        "source_ledger": LEDGER_JSON.relative_to(ROOT).as_posix(),
        "source_admission_decision": admission.get("evidence_id"),
        "source_authorized_measurement_precheck": precheck.get("evidence_id"),
        "entry_count": len(entries),
        "missing_entry_fields": missing_entry_fields,
        "boundary_checks": boundary,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "check_only_runner_does_not_measure_production_tokens",
        },
        "gates": {
            "sanitized_measurement_dry_run_gate": dry_run_gate,
            "check_only": True,
            "waes_harness_admitted": boundary["waes_harness_admitted"],
            "authorized_precheck_gate": boundary["authorized_precheck_gate"],
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
doc_id: GPCF-DOC-A1E6CF72D2
title: Headroom LCX Sanitized Measurement Dry Run Evidence 20260622
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md
source_path: docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX Sanitized Measurement Dry Run Evidence 20260622

## Evidence ID

`HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-20260622`

## 结论

本轮只执行 `--check-only` 脱敏台账结构检查。未计算真实生产 token 节省，未启动 Headroom proxy，未写入真实 KDS API，未触达外部 API。

## 输入

| artifact | path |
|---|---|
| sanitized ledger | `{LEDGER_JSON.relative_to(ROOT).as_posix()}` |
| WAES/Harness admitted decision | `{ADMISSION_JSON.relative_to(ROOT).as_posix()}` |
| authorized measurement precheck | `{AUTHORIZED_PRECHECK_JSON.relative_to(ROOT).as_posix()}` |

## 门禁

| 项 | 当前值 |
|---|---|
| sanitized_measurement_dry_run_gate | {str(dry_run_gate).lower()} |
| check_only | true |
| waes_harness_admitted | {str(boundary["waes_harness_admitted"]).lower()} |
| authorized_precheck_gate | {str(boundary["authorized_precheck_gate"]).lower()} |
| entry_count | {len(entries)} |
| saving_rate | not_calculated |
| tokens_saved | not_calculated |
| production_token_measurement_allowed | false |
| measured_production_tokens | false |
| production_proxy_started | false |
| kds_api_write | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 下一步

下一轮可增加只读 metadata replay 校验，但仍不得读取原文、不得计算真实生产节省、不得启动生产代理。
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    loop_round = """---
doc_id: GPCF-DOC-D83FE8C1B1
title: Loop Round GPCF Headroom LCX Sanitized Measurement Dry Run 001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Sanitized Measurement Dry Run 001

## 输入

- WAES/Harness 已准入 `admitted_for_sanitized_measurement_precheck`。
- 当前只允许脱敏台账元数据 dry-run。

## 动作

- 运行 `python3 tools/kds-sync/run_headroom_lcx_sanitized_measurement_dry_run.py --check-only`。
- 校验脱敏台账结构和安全边界。
- 不计算真实生产 token 节省，不启动 production proxy。

## 输出

- `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json`
- `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_sanitized_measurement_dry_run.py`
- `python3 tools/kds-sync/validate_headroom_lcx_authorized_measurement_precheck.py`

## 反馈

- dry-run runner 骨架已建立。
- 当前仍不得进入生产 token 测量。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

建立只读 metadata replay 校验；仍不得读取原文或启动生产代理。
"""
    LOOP_ROUND.write_text(loop_round, encoding="utf-8")

    print(
        "headroom_lcx_sanitized_measurement_dry_run="
        f"{'pass_check_only' if dry_run_gate else 'blocked'} "
        f"project_count=15 entry_count={len(entries)} check_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        "production_token_measurement_allowed=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
