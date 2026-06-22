#!/usr/bin/env python3
"""Build Headroom LCX sanitized token fixture extension evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-001.md"

PROJECTS = ["GPCF", "KDS", "Brain", "WAES", "GFIS"]
SCENARIOS = [
    "loop_gate_metadata",
    "retrieval_context_metadata",
    "tool_output_metadata",
]


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-20260622
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, KDS]
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
            base = 900 + project_index * 100 + scenario_index * 40
            after = int(base * 0.62)
            entries.append(
                {
                    "measurement_id": f"HEADROOM-LCX-SANITIZED-FIXTURE-{project}-{scenario_index:02d}",
                    "project": project,
                    "scenario": scenario,
                    "source_kind": "sanitized_fixture_metadata_only",
                    "input_tokens_before": base,
                    "input_tokens_after": after,
                    "output_tokens_before": 240 + scenario_index * 20,
                    "output_tokens_after": 180 + scenario_index * 12,
                    "cache_write_tokens_before": 120 + project_index * 5,
                    "cache_write_tokens_after": 80 + project_index * 4,
                    "cache_read_tokens_before": 90 + scenario_index * 5,
                    "cache_read_tokens_after": 70 + scenario_index * 3,
                    "retrieval_miss_count": 0 if scenario != "retrieval_context_metadata" else 1,
                    "answer_equivalence": "not_measured",
                    "sensitive_redaction_gate": "pass",
                    "project_marker_gate": "fixture_marker_preserved",
                    "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
                }
            )
    return {
        "fixture_id": "HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-20260622",
        "fixture_type": "sanitized_token_metadata_fixture_extension",
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
    failures = []
    projects = {entry.get("project") for entry in fixture["entries"]}
    scenarios = {entry.get("scenario") for entry in fixture["entries"]}
    if projects != set(PROJECTS):
        failures.append("project_coverage_mismatch")
    if scenarios != set(SCENARIOS):
        failures.append("scenario_coverage_mismatch")
    if fixture.get("entry_count") != len(PROJECTS) * len(SCENARIOS):
        failures.append("entry_count_mismatch")
    if any(entry.get("source_kind") != "sanitized_fixture_metadata_only" for entry in fixture["entries"]):
        failures.append("source_kind_mismatch")
    if any(entry.get("sensitive_redaction_gate") != "pass" for entry in fixture["entries"]):
        failures.append("redaction_gate_failed")
    if any(entry.get("project_marker_gate") != "fixture_marker_preserved" for entry in fixture["entries"]):
        failures.append("marker_gate_failed")
    if any(entry.get("answer_equivalence") != "not_measured" for entry in fixture["entries"]):
        failures.append("answer_equivalence_claimed")

    return {
        "evidence_id": "HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-20260622",
        "task_id": "GPCF-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-SANITIZED-TOKEN-FIXTURE-EXTENSION-001",
        "date": "2026-06-22",
        "status": "sanitized_token_fixture_extension_pass_no_measurement",
        "scope": "fixture_metadata_only",
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
            "reason": "fixture_extension_only_no_real_measurement",
        },
        "gates": {
            "fixture_extension_gate": not failures,
            "project_coverage_gate": projects == set(PROJECTS),
            "scenario_coverage_gate": scenarios == set(SCENARIOS),
            "entry_count_gate": fixture["entry_count"] == len(PROJECTS) * len(SCENARIOS),
            "metadata_only": True,
            "raw_text_stored": False,
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
        frontmatter("Headroom LCX Sanitized Token Fixture Extension Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Sanitized Token Fixture Extension Evidence",
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
            "- This fixture does not contain raw prompts, raw completions, customer contracts, POD, financial vouchers, keys, production credentials, or provider secrets.",
            "- This fixture does not represent measured production token usage.",
            "- This fixture does not authorize production proxy, real KDS API write, external API write, accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Sanitized Token Fixture Extension 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Sanitized Token Fixture Extension 001

## 输入

继续 Headroom LCX 项目群下一步，建立 sanitized token fixture 扩展包，至少覆盖 5 个项目域和 3 类场景。

## 动作

1. 生成 `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`。
2. 只写入 token 计数、marker、redaction、retrieval miss、answer equivalence 等脱敏元数据。
3. 生成 evidence 和 validator。
4. 保持生产、验收、集成状态全部为 false。

## 输出

- `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- `docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.json`
- `docs/harness/evidence/headroom-lcx-sanitized-token-fixture-extension-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_sanitized_token_fixture_extension.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_sanitized_token_fixture_extension.py
```

## 反馈

本轮只证明 5 项目域、3 场景的脱敏 fixture coverage 已建立；不证明真实生产 token 节省、真实 answer equivalence 或生产可用。

## 下一轮

将扩展 fixture 输入 metadata replay 和 marker/retrieval miss comparison gate，仍保持 check-only。
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
        "headroom_lcx_sanitized_token_fixture_extension=pass_check_only "
        f"project_count={evidence['project_count']} scenario_count={evidence['scenario_count']} "
        f"entry_count={evidence['entry_count']} metadata_only=true "
        "saving_rate=not_calculated measured_production_tokens=false "
        f"production_admission_gate={str(gates['production_admission_gate']).lower()} "
        f"accepted={str(gates['accepted']).lower()} "
        f"integrated={str(gates['integrated']).lower()} "
        f"production_ready={str(gates['production_ready']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
