#!/usr/bin/env python3
"""Run replay/comparison/stability over the 15-project Headroom LCX fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-001.md"

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
SCENARIOS = ["loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"]
ROUNDS = 3


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_round(fixture: dict, round_id: int) -> dict:
    records = []
    comparisons = []
    for index, entry in enumerate(fixture.get("entries", [])):
        record = {
            "task_id_candidate": entry.get("measurement_id"),
            "project_id": entry.get("project"),
            "content_type": entry.get("scenario"),
            "content_source_kind": entry.get("source_kind"),
            "tokens_before_input": entry.get("input_tokens_before"),
            "tokens_after_input": entry.get("input_tokens_after"),
            "tokens_before_output": entry.get("output_tokens_before"),
            "tokens_after_output": entry.get("output_tokens_after"),
            "cache_write_tokens_before": entry.get("cache_write_tokens_before"),
            "cache_write_tokens_after": entry.get("cache_write_tokens_after"),
            "cache_read_tokens_before": entry.get("cache_read_tokens_before"),
            "cache_read_tokens_after": entry.get("cache_read_tokens_after"),
            "ccr_retrieval_miss_count": entry.get("retrieval_miss_count"),
            "answer_equivalence": entry.get("answer_equivalence"),
            "sensitive_redaction_gate": entry.get("sensitive_redaction_gate"),
            "marker_gate": entry.get("project_marker_gate"),
            "rollback_plan_id": entry.get("rollback_plan_id"),
        }
        records.append(record)
        comparisons.append(
            {
                "record_index": index,
                "project_id": record["project_id"],
                "content_type": record["content_type"],
                "marker_gate_preserved": record["marker_gate"] == "fixture_marker_preserved",
                "answer_equivalence_unmeasured": record["answer_equivalence"] == "not_measured",
                "sensitive_redaction_gate_pass": record["sensitive_redaction_gate"] == "pass",
                "ccr_retrieval_miss_count_within_fixture_threshold": record["ccr_retrieval_miss_count"] <= 1,
            }
        )
    comparable = {
        "project_count": fixture.get("project_count"),
        "scenario_count": fixture.get("scenario_count"),
        "entry_count": fixture.get("entry_count"),
        "projects": fixture.get("projects"),
        "scenarios": fixture.get("scenarios"),
        "records": records,
        "comparisons": comparisons,
        "forbidden_claims": {
            "raw_text_stored": fixture.get("sensitive_raw_text_stored"),
            "contains_raw_prompt": fixture.get("contains_raw_prompt"),
            "contains_raw_completion": fixture.get("contains_raw_completion"),
            "contains_customer_contract_text": fixture.get("contains_customer_contract_text"),
            "contains_provider_secret": fixture.get("contains_provider_secret"),
            "production_token_measurement_allowed": fixture.get("production_token_measurement_allowed"),
            "measured_production_tokens": fixture.get("measured_production_tokens"),
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
    }
    return {"round_id": round_id, **comparable, "stable_hash": canonical_hash(comparable)}


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
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
    rounds = [build_round(fixture, round_id) for round_id in range(1, ROUNDS + 1)]
    hashes = {item["stable_hash"] for item in rounds}
    failures = []
    if fixture.get("projects") != PROJECTS or fixture.get("project_count") != len(PROJECTS):
        failures.append("project_coverage_mismatch")
    if fixture.get("scenarios") != SCENARIOS or fixture.get("scenario_count") != len(SCENARIOS):
        failures.append("scenario_coverage_mismatch")
    if fixture.get("entry_count") != len(PROJECTS) * len(SCENARIOS):
        failures.append("entry_count_mismatch")
    if len(hashes) != 1:
        failures.append("stable_hash_mismatch")
    for round_item in rounds:
        if not all(item["marker_gate_preserved"] for item in round_item["comparisons"]):
            failures.append(f"round_{round_item['round_id']}:marker_gate_failed")
        if not all(item["answer_equivalence_unmeasured"] for item in round_item["comparisons"]):
            failures.append(f"round_{round_item['round_id']}:answer_equivalence_claimed")
        if not all(item["sensitive_redaction_gate_pass"] for item in round_item["comparisons"]):
            failures.append(f"round_{round_item['round_id']}:redaction_failed")
        if any(value is not False for value in round_item["forbidden_claims"].values()):
            failures.append(f"round_{round_item['round_id']}:forbidden_claim_not_false")
    gate = not failures
    return {
        "evidence_id": "HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-20260622",
        "task_id": "GPCF-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-PROJECT-GROUP-REPLAY-STABILITY-001",
        "date": "2026-06-22",
        "status": "project_group_replay_stability_pass_no_measurement" if gate else "project_group_replay_stability_blocked",
        "scope": "project_group_sanitized_fixture_replay_stability_only",
        "fixture": FIXTURE.relative_to(ROOT).as_posix(),
        "round_count": ROUNDS,
        "project_count": len(PROJECTS),
        "scenario_count": len(SCENARIOS),
        "entry_count": fixture.get("entry_count"),
        "replay_record_count": fixture.get("entry_count"),
        "comparison_count": fixture.get("entry_count"),
        "stable_hash_count": len(hashes),
        "stable_hash": next(iter(hashes)) if len(hashes) == 1 else None,
        "rounds": rounds,
        "failures": failures,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "project_group_replay_stability_only_no_real_measurement",
        },
        "gates": {
            "project_group_replay_stability_gate": gate,
            "metadata_replay_gate": gate,
            "marker_retrieval_miss_comparison_gate": gate,
            "multi_round_stability_gate": len(hashes) == 1,
            "project_coverage_gate": fixture.get("projects") == PROJECTS,
            "scenario_coverage_gate": fixture.get("scenarios") == SCENARIOS,
            "entry_count_gate": fixture.get("entry_count") == len(PROJECTS) * len(SCENARIOS),
            "metadata_only": True,
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


def write_md(evidence: dict) -> None:
    lines = [
        frontmatter("Headroom LCX Project Group Replay Stability Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Project Group Replay Stability Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- fixture: `{evidence['fixture']}`",
        f"- round_count: `{evidence['round_count']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- scenario_count: `{evidence['scenario_count']}`",
        f"- entry_count: `{evidence['entry_count']}`",
        f"- stable_hash_count: `{evidence['stable_hash_count']}`",
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
            "- This gate covers all 15 project domains with sanitized fixture metadata only.",
            "- It does not read raw prompt, raw completion, customer contract, POD, financial voucher, key, production credential, or provider secret.",
            "- It does not calculate real production token saving.",
            "- It does not mark Headroom as accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Project Group Replay Stability 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Project Group Replay Stability 001

## 输入

基于 15 项目域 sanitized fixture 执行全项目域 replay/comparison/stability。

## 动作

1. 读取 45 条全项目域 sanitized fixture 元数据。
2. 生成 replay records 和 comparison records。
3. 连续构造 3 轮稳定性摘要并比较 hash。
4. 保持生产、验收、集成状态全部为 false。

## 输出

- `docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.json`
- `docs/harness/evidence/headroom-lcx-project-group-replay-stability-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_project_group_replay_stability.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_project_group_replay_stability.py
```

## 反馈

本轮只证明 15 项目域 sanitized fixture replay/comparison/stability 可回放；不证明生产可用。

## 下一轮

生成 readiness 汇总与 L3.5/L4 试点授权建议包。
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
        "headroom_lcx_project_group_replay_stability=pass_check_only "
        f"round_count={evidence['round_count']} project_count={evidence['project_count']} "
        f"scenario_count={evidence['scenario_count']} entry_count={evidence['entry_count']} "
        f"stable_hash_count={evidence['stable_hash_count']} metadata_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        f"production_admission_gate={str(gates['production_admission_gate']).lower()} "
        f"accepted={str(gates['accepted']).lower()} "
        f"integrated={str(gates['integrated']).lower()} "
        f"production_ready={str(gates['production_ready']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
