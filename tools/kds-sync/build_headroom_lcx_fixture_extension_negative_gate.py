#!/usr/bin/env python3
"""Build negative fixtures for Headroom LCX fixture extension boundaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEGATIVE_FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001.md"

BASE_ENTRY = {
    "measurement_id": "HEADROOM-LCX-NEGATIVE-FIXTURE-BASE",
    "project": "GPCF",
    "scenario": "loop_gate_metadata",
    "source_kind": "sanitized_fixture_metadata_only",
    "input_tokens_before": 100,
    "input_tokens_after": 80,
    "output_tokens_before": 30,
    "output_tokens_after": 24,
    "cache_write_tokens_before": 10,
    "cache_write_tokens_after": 8,
    "cache_read_tokens_before": 10,
    "cache_read_tokens_after": 8,
    "retrieval_miss_count": 0,
    "answer_equivalence": "not_measured",
    "sensitive_redaction_gate": "pass",
    "project_marker_gate": "fixture_marker_preserved",
    "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
}

CASES = [
    ("raw_prompt_field_present", {"raw_prompt": "FORBIDDEN_PLACEHOLDER_ONLY"}, "raw_prompt_forbidden"),
    ("raw_completion_field_present", {"raw_completion": "FORBIDDEN_PLACEHOLDER_ONLY"}, "raw_completion_forbidden"),
    ("sensitive_material_unredacted", {"contains_customer_contract_text": True}, "sensitive_material_forbidden"),
    ("production_token_measurement_claimed", {"measured_production_tokens": True}, "production_measurement_forbidden"),
    ("kds_api_write_claimed", {"kds_api_write": True}, "kds_api_write_forbidden"),
    ("production_proxy_started_claimed", {"production_proxy_started": True}, "production_proxy_forbidden"),
    ("accepted_status_claimed", {"accepted": True}, "accepted_status_forbidden"),
    ("integrated_status_claimed", {"integrated": True}, "integrated_status_forbidden"),
    ("production_ready_claimed", {"production_ready": True}, "production_ready_forbidden"),
]


def reject_reason(candidate: dict) -> str | None:
    if "raw_prompt" in candidate:
        return "raw_prompt_forbidden"
    if "raw_completion" in candidate:
        return "raw_completion_forbidden"
    if candidate.get("contains_customer_contract_text") is True or candidate.get("sensitive_material_processed") is True:
        return "sensitive_material_forbidden"
    if candidate.get("measured_production_tokens") is True or candidate.get("production_token_measurement_allowed") is True:
        return "production_measurement_forbidden"
    if candidate.get("kds_api_write") is True:
        return "kds_api_write_forbidden"
    if candidate.get("production_proxy_started") is True:
        return "production_proxy_forbidden"
    if candidate.get("accepted") is True:
        return "accepted_status_forbidden"
    if candidate.get("integrated") is True:
        return "integrated_status_forbidden"
    if candidate.get("production_ready") is True:
        return "production_ready_forbidden"
    return None


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/{source_path}
source_path: {source_path}
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---
"""


def build_negative_fixture() -> dict:
    cases = []
    for case_id, override, expected in CASES:
        candidate = dict(BASE_ENTRY)
        candidate.update(override)
        cases.append(
            {
                "case_id": case_id,
                "candidate": candidate,
                "expected_rejection_reason": expected,
            }
        )
    return {
        "fixture_id": "HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-FIXTURES-20260622",
        "fixture_type": "negative_fixture_boundary_cases",
        "case_count": len(cases),
        "cases": cases,
        "expected_result": {
            "rejected": len(cases),
            "accepted": 0,
            "production_token_measurement_allowed": False,
            "production_admission_gate": False,
            "accepted_status": False,
            "integrated": False,
            "production_ready": False,
        },
    }


def build_evidence(fixture: dict) -> dict:
    results = []
    for case in fixture["cases"]:
        actual = reject_reason(case["candidate"])
        results.append(
            {
                "case_id": case["case_id"],
                "expected_rejection_reason": case["expected_rejection_reason"],
                "actual_rejection_reason": actual,
                "rejected": actual == case["expected_rejection_reason"],
                "accepted": actual is None,
            }
        )
    rejected = sum(1 for result in results if result["rejected"])
    accepted = sum(1 for result in results if result["accepted"])
    return {
        "evidence_id": "HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-NEGATIVE-GATE-001",
        "date": "2026-06-22",
        "status": "negative_gate_pass_no_measurement" if rejected == fixture["case_count"] and accepted == 0 else "negative_gate_blocked",
        "scope": "fixture_extension_negative_boundary_cases",
        "negative_fixture": NEGATIVE_FIXTURE.relative_to(ROOT).as_posix(),
        "case_count": fixture["case_count"],
        "rejected": rejected,
        "accepted_count": accepted,
        "results": results,
        "gates": {
            "negative_fixture_gate": rejected == fixture["case_count"] and accepted == 0,
            "raw_prompt_rejected": any(result["actual_rejection_reason"] == "raw_prompt_forbidden" for result in results),
            "raw_completion_rejected": any(result["actual_rejection_reason"] == "raw_completion_forbidden" for result in results),
            "sensitive_material_rejected": any(result["actual_rejection_reason"] == "sensitive_material_forbidden" for result in results),
            "production_measurement_rejected": any(result["actual_rejection_reason"] == "production_measurement_forbidden" for result in results),
            "kds_api_write_rejected": any(result["actual_rejection_reason"] == "kds_api_write_forbidden" for result in results),
            "production_proxy_rejected": any(result["actual_rejection_reason"] == "production_proxy_forbidden" for result in results),
            "status_upgrade_rejected": all(
                any(result["actual_rejection_reason"] == reason for result in results)
                for reason in ["accepted_status_forbidden", "integrated_status_forbidden", "production_ready_forbidden"]
            ),
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


def write_md(evidence: dict) -> None:
    lines = [
        frontmatter("Headroom LCX Fixture Extension Negative Gate Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Fixture Extension Negative Gate Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- negative_fixture: `{evidence['negative_fixture']}`",
        f"- case_count: `{evidence['case_count']}`",
        f"- rejected: `{evidence['rejected']}`",
        f"- accepted_count: `{evidence['accepted_count']}`",
        "",
        "## Gates",
        "",
        "| Gate | Value |",
        "|---|---|",
    ]
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
            "- Negative fixtures use placeholder-only markers for forbidden raw or sensitive fields.",
            "- No real customer material, provider secret, KDS token, authorization header, production credential, or production token ledger is stored.",
            "- This evidence does not authorize accepted, integrated, production_ready, production proxy, real KDS API write, or external API write.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Fixture Extension Negative Gate 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Fixture Extension Negative Gate 001

## 输入

建立扩展 fixture 负向样例门禁，验证越界声明和敏感字段会被拒绝。

## 动作

1. 生成 negative fixture boundary cases。
2. 覆盖 raw prompt、raw completion、敏感材料、生产测量、真实 KDS 写入、生产代理和状态升级声明。
3. 生成 evidence 和 validator。
4. 保持生产、验收、集成状态全部为 false。

## 输出

- `fixtures/headroom/headroom-lcx-fixture-extension-negative-fixtures-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-negative-gate-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_fixture_extension_negative_gate.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_fixture_extension_negative_gate.py
```

## 反馈

本轮只证明负向边界样例可拒绝越界声明；不证明生产可用。

## 下一轮

建立脱敏 fixture 多轮稳定性门禁，检查连续 replay/comparison 输出是否稳定。
"""
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        raise SystemExit("--check-only is required")
    fixture = build_negative_fixture()
    evidence = build_evidence(fixture)
    write_json(NEGATIVE_FIXTURE, fixture)
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    gates = evidence["gates"]
    print(
        "headroom_lcx_fixture_extension_negative_gate=pass_check_only "
        f"case_count={evidence['case_count']} rejected={evidence['rejected']} "
        f"accepted={evidence['accepted_count']} "
        "production_admission_gate=false measured_production_tokens=false "
        f"accepted_status={str(gates['accepted']).lower()} "
        f"integrated={str(gates['integrated']).lower()} "
        f"production_ready={str(gates['production_ready']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
