#!/usr/bin/env python3
"""Build a 15-project Headroom LCX sanitized metadata fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001.md"

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


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622
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


def build_fixture() -> dict:
    entries = []
    for project_index, project in enumerate(PROJECTS, start=1):
        for scenario_index, scenario in enumerate(SCENARIOS, start=1):
            base = 900 + project_index * 80 + scenario_index * 35
            entries.append(
                {
                    "measurement_id": f"HEADROOM-LCX-PROJECT-GROUP-FIXTURE-{project}-{scenario_index:02d}",
                    "project": project,
                    "scenario": scenario,
                    "source_kind": "project_group_sanitized_fixture_metadata_only",
                    "input_tokens_before": base,
                    "input_tokens_after": int(base * 0.64),
                    "output_tokens_before": 220 + scenario_index * 20,
                    "output_tokens_after": 170 + scenario_index * 12,
                    "cache_write_tokens_before": 110 + project_index * 4,
                    "cache_write_tokens_after": 78 + project_index * 3,
                    "cache_read_tokens_before": 80 + scenario_index * 6,
                    "cache_read_tokens_after": 62 + scenario_index * 4,
                    "retrieval_miss_count": 1 if scenario == "retrieval_context_metadata" else 0,
                    "answer_equivalence": "not_measured",
                    "sensitive_redaction_gate": "pass",
                    "project_marker_gate": "fixture_marker_preserved",
                    "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
                }
            )
    return {
        "fixture_id": "HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622",
        "fixture_type": "project_group_sanitized_token_metadata_fixture",
        "authorization_scope": "fixture_only_no_production_measurement",
        "telemetry": "off",
        "project_count": len(PROJECTS),
        "scenario_count": len(SCENARIOS),
        "entry_count": len(entries),
        "projects": PROJECTS,
        "scenarios": SCENARIOS,
        "sensitive_raw_text_stored": False,
        "raw_prompt_storage": "forbidden",
        "raw_completion_storage": "forbidden",
        "contains_provider_secret": False,
        "contains_authorization_header": False,
        "contains_raw_prompt": False,
        "contains_raw_completion": False,
        "contains_customer_contract_text": False,
        "measured_production_tokens": False,
        "production_token_measurement_allowed": False,
        "entries": entries,
    }


def build_evidence(fixture: dict) -> dict:
    projects = {entry["project"] for entry in fixture["entries"]}
    scenarios = {entry["scenario"] for entry in fixture["entries"]}
    failures = []
    if projects != set(PROJECTS):
        failures.append("project_coverage_mismatch")
    if scenarios != set(SCENARIOS):
        failures.append("scenario_coverage_mismatch")
    if fixture["entry_count"] != len(PROJECTS) * len(SCENARIOS):
        failures.append("entry_count_mismatch")
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
            failures.append(f"boundary_not_false:{key}")
    return {
        "evidence_id": "HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-PROJECT-GROUP-SANITIZED-FIXTURE-001",
        "date": "2026-06-22",
        "status": "project_group_sanitized_fixture_pass_no_measurement" if not failures else "project_group_sanitized_fixture_blocked",
        "scope": "project_group_fixture_metadata_only",
        "fixture": FIXTURE.relative_to(ROOT).as_posix(),
        "project_count": fixture["project_count"],
        "scenario_count": fixture["scenario_count"],
        "entry_count": fixture["entry_count"],
        "projects": fixture["projects"],
        "scenarios": fixture["scenarios"],
        "coverage_failures": failures,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "project_group_fixture_only_no_real_measurement",
        },
        "gates": {
            "project_group_fixture_gate": not failures,
            "project_coverage_gate": projects == set(PROJECTS),
            "scenario_coverage_gate": scenarios == set(SCENARIOS),
            "entry_count_gate": fixture["entry_count"] == len(PROJECTS) * len(SCENARIOS),
            "metadata_only": True,
            "check_only": True,
            "raw_text_stored": False,
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
        frontmatter("Headroom LCX Project Group Sanitized Fixture Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Project Group Sanitized Fixture Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- fixture: `{evidence['fixture']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- scenario_count: `{evidence['scenario_count']}`",
        f"- entry_count: `{evidence['entry_count']}`",
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
            "- This fixture covers 15 project domains but still contains sanitized metadata only.",
            "- This fixture does not contain raw prompts, raw completions, customer contracts, POD, financial vouchers, keys, production credentials, or provider secrets.",
            "- This fixture does not represent measured production token usage.",
            "- This fixture does not authorize production proxy, KDS API write, accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Project Group Sanitized Fixture 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Project Group Sanitized Fixture 001

## 输入

用户选择补全 15 项目域 sanitized fixture，再做全项目域 replay/comparison/stability。

## 动作

1. 生成 15 项目域、3 场景、45 条 sanitized metadata fixture。
2. 保持 token 字段为 fixture 元数据，不声明生产实测。
3. 生成 evidence 和 validator。

## 输出

- `fixtures/headroom/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.json`
- `docs/harness/evidence/headroom-lcx-project-group-sanitized-fixture-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_project_group_sanitized_fixture.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_project_group_sanitized_fixture.py
```

## 反馈

本轮只证明全项目域 sanitized fixture coverage 已建立；不证明生产可用。

## 下一轮

执行全项目域 fixture replay/comparison/stability。
"""
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if not args.check_only:
        raise SystemExit("--check-only is required")
    fixture = build_fixture()
    evidence = build_evidence(fixture)
    write_json(FIXTURE, fixture)
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    gates = evidence["gates"]
    print(
        "headroom_lcx_project_group_sanitized_fixture=pass_check_only "
        f"project_count={evidence['project_count']} scenario_count={evidence['scenario_count']} "
        f"entry_count={evidence['entry_count']} metadata_only=true saving_rate=not_calculated "
        "measured_production_tokens=false "
        f"production_admission_gate={str(gates['production_admission_gate']).lower()} "
        f"accepted={str(gates['accepted']).lower()} "
        f"integrated={str(gates['integrated']).lower()} "
        f"production_ready={str(gates['production_ready']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
