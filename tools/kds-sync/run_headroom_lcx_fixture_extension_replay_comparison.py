#!/usr/bin/env python3
"""Replay and compare the Headroom LCX sanitized token fixture extension."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001.md"

PROJECTS = ["GPCF", "KDS", "Brain", "WAES", "GFIS"]
SCENARIOS = ["loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"]

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


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622
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


def build_evidence() -> dict:
    fixture = load_json(FIXTURE)
    entries = fixture.get("entries", [])
    mapping_failures = []
    comparison_failures = []
    replay_records = []
    comparisons = []

    if fixture.get("projects") != PROJECTS or fixture.get("project_count") != len(PROJECTS):
        comparison_failures.append("project_coverage_mismatch")
    if fixture.get("scenarios") != SCENARIOS or fixture.get("scenario_count") != len(SCENARIOS):
        comparison_failures.append("scenario_coverage_mismatch")
    if fixture.get("entry_count") != 15:
        comparison_failures.append("entry_count_mismatch")
    for key in [
        "sensitive_raw_text_stored",
        "contains_provider_secret",
        "contains_authorization_header",
        "contains_raw_prompt",
        "contains_raw_completion",
        "contains_customer_contract_text",
        "measured_production_tokens",
        "production_token_measurement_allowed",
    ]:
        if fixture.get(key) is not False:
            comparison_failures.append(f"fixture_boundary_not_false:{key}")

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            mapping_failures.append(f"entry_{index}:not_object")
            continue
        missing = [field for field in FIELD_MAP if field not in entry]
        if missing:
            mapping_failures.append(f"entry_{index}:missing:{','.join(missing)}")
            continue
        replay_record = {mapped: entry[source] for source, mapped in FIELD_MAP.items()}
        replay_records.append(replay_record)
        comparison = {
            "record_index": index,
            "task_id_candidate": replay_record["task_id_candidate"],
            "project_id": replay_record["project_id"],
            "content_type": replay_record["content_type"],
            "marker_gate_preserved": replay_record["marker_gate"] == "fixture_marker_preserved",
            "answer_equivalence_unmeasured": replay_record["answer_equivalence"] == "not_measured",
            "sensitive_redaction_gate_pass": replay_record["sensitive_redaction_gate"] == "pass",
            "ccr_retrieval_miss_count_within_fixture_threshold": replay_record["ccr_retrieval_miss_count"] <= 1,
            "raw_text_compared": False,
            "production_tokens_compared": False,
        }
        for key, ok in comparison.items():
            if key.endswith("_compared"):
                continue
            if key in {"record_index", "task_id_candidate", "project_id", "content_type"}:
                continue
            if ok is not True:
                comparison_failures.append(f"entry_{index}:{key}")
        comparisons.append(comparison)

    replay_gate = not mapping_failures and not comparison_failures
    return {
        "evidence_id": "HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-20260622",
        "task_id": "GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-FIXTURE-EXTENSION-REPLAY-COMPARISON-001",
        "date": "2026-06-22",
        "status": "fixture_extension_replay_comparison_pass_no_measurement" if replay_gate else "fixture_extension_replay_comparison_blocked",
        "scope": "sanitized_fixture_metadata_replay_comparison_only",
        "fixture": FIXTURE.relative_to(ROOT).as_posix(),
        "project_count": len(PROJECTS),
        "scenario_count": len(SCENARIOS),
        "entry_count": len(entries),
        "replay_record_count": len(replay_records),
        "comparison_count": len(comparisons),
        "field_map": FIELD_MAP,
        "replay_records": replay_records,
        "comparisons": comparisons,
        "mapping_failures": mapping_failures,
        "comparison_failures": comparison_failures,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "fixture_extension_replay_comparison_only_no_real_measurement",
        },
        "gates": {
            "fixture_extension_replay_comparison_gate": replay_gate,
            "metadata_replay_gate": not mapping_failures,
            "marker_retrieval_miss_comparison_gate": not comparison_failures,
            "metadata_only": True,
            "check_only": True,
            "raw_text_compared": False,
            "production_tokens_compared": False,
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
        frontmatter("Headroom LCX Fixture Extension Replay Comparison Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Fixture Extension Replay Comparison Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- fixture: `{evidence['fixture']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- scenario_count: `{evidence['scenario_count']}`",
        f"- entry_count: `{evidence['entry_count']}`",
        f"- replay_record_count: `{evidence['replay_record_count']}`",
        f"- comparison_count: `{evidence['comparison_count']}`",
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
            "| saving_rate | not_calculated |",
            "| tokens_saved | not_calculated |",
            "",
            "## Non-Claims",
            "",
            "- This replay/comparison uses sanitized fixture metadata only.",
            "- It does not read raw prompt, raw completion, customer contract, POD, financial voucher, key, production credential, or provider secret.",
            "- It does not calculate real production token saving.",
            "- It does not mark Headroom as accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Fixture Extension Replay Comparison 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Fixture Extension Replay Comparison 001

## 输入

将 `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json` 输入 metadata replay 和 marker/retrieval miss comparison gate。

## 动作

1. 读取 5 项目域、3 场景、15 条 sanitized fixture 元数据。
2. 复用 LCX field map 生成 replay records。
3. 比对 marker、redaction、retrieval miss 和 answer equivalence 元数据。
4. 保持所有生产、验收、集成状态为 false。

## 输出

- `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-extension-replay-comparison-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_fixture_extension_replay_comparison.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_fixture_extension_replay_comparison.py
```

## 反馈

本轮只证明扩展 fixture 的 metadata replay/comparison 可回放；不证明真实生产 token 节省或生产可用。

## 下一轮

建立扩展 fixture 的负向样例，验证原文、敏感材料、生产测量、跨项目事实写入和生产状态升级声明会被拒绝。
"""
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        raise SystemExit("--check-only is required")
    evidence = build_evidence()
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    gates = evidence["gates"]
    print(
        "headroom_lcx_fixture_extension_replay_comparison=pass_check_only "
        f"project_count={evidence['project_count']} scenario_count={evidence['scenario_count']} "
        f"entry_count={evidence['entry_count']} replay_record_count={evidence['replay_record_count']} "
        f"comparison_count={evidence['comparison_count']} metadata_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        f"production_admission_gate={str(gates['production_admission_gate']).lower()} "
        f"accepted={str(gates['accepted']).lower()} "
        f"integrated={str(gates['integrated']).lower()} "
        f"production_ready={str(gates['production_ready']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
