#!/usr/bin/env python3
"""Build Headroom LCX external receipt negative fixtures."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
FIXTURE_DIR = ROOT / "fixtures/headroom"

COMPLETION_PACKAGE = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json"
NEGATIVE_FIXTURES = FIXTURE_DIR / "headroom-lcx-real-measurement-external-receipt-negative-fixtures.json"
FORBIDDEN_COMPLETED_RECEIPT = FIXTURE_DIR / "headroom-lcx-real-measurement-external-authorization-receipt.completed.json"

OUT_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.json"
OUT_MD = EVIDENCE_DIR / "headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md"
OUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md"

NEGATIVE_CASES = [
    ("production_proxy_started_true", "production_proxy_started", True),
    ("production_sdk_enabled_true", "production_sdk_enabled", True),
    ("real_kds_write_true", "real_kds_write", True),
    ("external_api_write_true", "external_api_write", True),
    ("database_migration_true", "database_migration", True),
    ("permission_change_true", "permission_change", True),
    ("accepted_true", "accepted", True),
    ("integrated_true", "integrated", True),
    ("production_ready_true", "production_ready", True),
    ("telemetry_on", "telemetry", "on"),
    (
        "sensitive_material_attestation_unverified",
        "sensitive_material_attestation",
        "unverified_sensitive_material_may_be_present",
    ),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def build_fixtures(template: dict[str, Any]) -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = []
    for case_id, field, value in NEGATIVE_CASES:
        receipt = copy.deepcopy(template)
        receipt[field] = value
        fixtures.append(
            {
                "case_id": case_id,
                "mutated_field": field,
                "expected_result": "reject",
                "expected_reason": f"{field}_violates_headroom_lcx_receipt_boundary",
                "receipt": receipt,
            }
        )
    return fixtures


def build_evidence() -> dict[str, Any]:
    package = load_json(COMPLETION_PACKAGE)
    template = package.get("completed_template", {})
    require(isinstance(template, dict), "completion package template must be an object")
    fixtures = build_fixtures(template)
    return {
        "evidence_id": "HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623",
        "task_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001",
        "date": "2026-06-23",
        "status": "negative_fixtures_ready_no_completed_receipt_recorded",
        "scope": "negative_fixture_validation_only_no_measurement",
        "project_count": 15,
        "source_completion_package": COMPLETION_PACKAGE.relative_to(ROOT).as_posix(),
        "negative_fixture_path": NEGATIVE_FIXTURES.relative_to(ROOT).as_posix(),
        "forbidden_completed_receipt_path": FORBIDDEN_COMPLETED_RECEIPT.relative_to(ROOT).as_posix(),
        "fixture_count": len(fixtures),
        "expected_rejected_count": len(fixtures),
        "expected_accepted_count": 0,
        "fixtures": fixtures,
        "pre_execution_decision": {
            "completed_receipt_instance_created": False,
            "can_open_real_measurement": False,
            "real_measurement_open": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def write_outputs(evidence: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    NEGATIVE_FIXTURES.write_text(json.dumps(evidence["fixtures"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fixture_rows = [
        f"| {item['case_id']} | `{item['mutated_field']}` | `{item['expected_result']}` |"
        for item in evidence["fixtures"]
    ]
    decision_rows = [
        f"| {key} | `{str(value).lower()}` |"
        for key, value in evidence["pre_execution_decision"].items()
    ]
    md = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623",
            "title: Headroom LCX Real Measurement External Receipt Negative Fixtures",
            "project: KDS",
            "related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: KDS",
            "kds_space: 开发",
            "kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Real Measurement External Receipt Negative Fixtures",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-20260623`",
            "",
            "## 当前结论",
            "",
            "`negative_fixtures_ready_no_completed_receipt_recorded`",
            "",
            "本轮只生成 completed receipt 负向 fixtures，不生成正式 completed receipt，不打开真实测量窗口。",
            "",
            "## 负向样本",
            "",
            "| case_id | mutated_field | expected_result |",
            "|---|---|---|",
            *fixture_rows,
            "",
            "## 计数",
            "",
            "| item | value |",
            "|---|---|",
            f"| fixture_count | `{evidence['fixture_count']}` |",
            f"| expected_rejected_count | `{evidence['expected_rejected_count']}` |",
            f"| expected_accepted_count | `{evidence['expected_accepted_count']}` |",
            "",
            "## 执行前判定",
            "",
            "| item | value |",
            "|---|---|",
            *decision_rows,
            "",
            "## 非声明",
            "",
            "- 不声明正式外部回执已经记录。",
            "- 不声明真实测量已经执行。",
            "- 不声明生产代理、生产 SDK、真实 KDS 写入或外部 API 写入。",
            "- 不声明 accepted、integrated 或 production_ready。",
        ]
    ) + "\n"
    OUT_MD.write_text(md, encoding="utf-8")

    loop = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001",
            "title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Negative Fixtures 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Real Measurement External Receipt Negative Fixtures 001",
            "",
            "## run",
            "",
            "### 输入",
            "",
            "- completed receipt 填写包",
            "",
            "### 动作",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py`",
            "- 生成 completed receipt 负向 fixtures。",
            "- 不生成正式 completed receipt 实例。",
            "",
            "### 输出",
            "",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md`",
            "- `fixtures/headroom/headroom-lcx-real-measurement-external-receipt-negative-fixtures.json`",
            "",
            "## stop",
            "",
            "- stop_type: authorization_boundary",
            "- stop_reason: 负向 fixtures 只验证拒绝规则，不代表正式回执已经记录。",
            "",
            "## verify",
            "",
            "### 检查",
            "",
            "- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py`",
            "",
            "## recover",
            "",
            "- 删除本轮 negative fixtures、evidence 和 validator 即可回退。",
            "",
            "## debug",
            "",
            "### 反馈",
            "",
            "- 本轮预期 11 个负向样本全部 rejected，accepted=0。",
            "",
            "### 下一轮",
            "",
            "- 等待人工填写正式 completed receipt，或建立正式 receipt intake validator。",
        ]
    ) + "\n"
    OUT_LOOP.write_text(loop, encoding="utf-8")


def main() -> int:
    evidence = build_evidence()
    write_outputs(evidence)
    print(
        "headroom_lcx_real_measurement_external_receipt_negative_fixtures=generated "
        f"fixture_count={evidence['fixture_count']} expected_rejected_count={evidence['expected_rejected_count']} "
        "expected_accepted_count=0 completed_receipt_instance_created=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
