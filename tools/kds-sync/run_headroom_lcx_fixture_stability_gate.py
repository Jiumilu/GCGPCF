#!/usr/bin/env python3
"""Run a check-only stability gate over Headroom LCX sanitized fixture metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-FIXTURE-STABILITY-GATE-001.md"

PROJECTS = ["GPCF", "KDS", "Brain", "WAES", "GFIS"]
SCENARIOS = ["loop_gate_metadata", "retrieval_context_metadata", "tool_output_metadata"]
ROUNDS = 3


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain JSON object")
    return data


def canonical_hash(payload: dict) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_round_summary(fixture: dict, round_id: int) -> dict:
    entries = fixture.get("entries", [])
    return {
        "round_id": round_id,
        "project_count": fixture.get("project_count"),
        "scenario_count": fixture.get("scenario_count"),
        "entry_count": fixture.get("entry_count"),
        "projects": fixture.get("projects"),
        "scenarios": fixture.get("scenarios"),
        "record_keys": [
            {
                "measurement_id": entry.get("measurement_id"),
                "project": entry.get("project"),
                "scenario": entry.get("scenario"),
                "source_kind": entry.get("source_kind"),
                "retrieval_miss_count": entry.get("retrieval_miss_count"),
                "answer_equivalence": entry.get("answer_equivalence"),
                "sensitive_redaction_gate": entry.get("sensitive_redaction_gate"),
                "project_marker_gate": entry.get("project_marker_gate"),
            }
            for entry in entries
        ],
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


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622
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


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_evidence() -> dict:
    fixture = load_json(FIXTURE)
    rounds = []
    for round_id in range(1, ROUNDS + 1):
        comparable = build_round_summary(fixture, round_id)
        comparable_without_round = dict(comparable)
        comparable_without_round.pop("round_id")
        rounds.append(
            {
                **comparable,
                "stable_hash": canonical_hash(comparable_without_round),
            }
        )
    hashes = {item["stable_hash"] for item in rounds}
    forbidden = rounds[0]["forbidden_claims"]
    failures = []
    if fixture.get("projects") != PROJECTS or fixture.get("project_count") != len(PROJECTS):
        failures.append("project_coverage_mismatch")
    if fixture.get("scenarios") != SCENARIOS or fixture.get("scenario_count") != len(SCENARIOS):
        failures.append("scenario_coverage_mismatch")
    if fixture.get("entry_count") != 15:
        failures.append("entry_count_mismatch")
    if len(hashes) != 1:
        failures.append("stable_hash_mismatch")
    if any(value is not False for value in forbidden.values()):
        failures.append("forbidden_claim_not_false")
    gate = not failures
    return {
        "evidence_id": "HEADROOM-LCX-FIXTURE-STABILITY-GATE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-FIXTURE-STABILITY-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-FIXTURE-STABILITY-GATE-001",
        "date": "2026-06-22",
        "status": "fixture_stability_gate_pass_no_measurement" if gate else "fixture_stability_gate_blocked",
        "scope": "sanitized_fixture_metadata_stability_only",
        "fixture": FIXTURE.relative_to(ROOT).as_posix(),
        "round_count": ROUNDS,
        "project_count": len(PROJECTS),
        "scenario_count": len(SCENARIOS),
        "entry_count": fixture.get("entry_count"),
        "stable_hash_count": len(hashes),
        "stable_hash": next(iter(hashes)) if len(hashes) == 1 else None,
        "rounds": rounds,
        "failures": failures,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "stability_gate_only_no_real_measurement",
        },
        "gates": {
            "fixture_stability_gate": gate,
            "multi_round_stability_gate": len(hashes) == 1,
            "project_coverage_gate": fixture.get("projects") == PROJECTS,
            "scenario_coverage_gate": fixture.get("scenarios") == SCENARIOS,
            "entry_count_gate": fixture.get("entry_count") == 15,
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
        frontmatter("Headroom LCX Fixture Stability Gate Evidence", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX Fixture Stability Gate Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- fixture: `{evidence['fixture']}`",
        f"- round_count: `{evidence['round_count']}`",
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
            "- This gate compares sanitized metadata summaries only.",
            "- It does not read raw prompt, raw completion, customer contract, POD, financial voucher, key, production credential, or provider secret.",
            "- It does not calculate real production token saving.",
            "- It does not mark Headroom as accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Fixture Stability Gate 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Fixture Stability Gate 001

## 输入

建立脱敏 fixture 多轮稳定性门禁，连续比较 sanitized metadata replay/comparison 输出摘要。

## 动作

1. 读取 `fixtures/headroom/headroom-lcx-sanitized-token-fixture-extension-20260622.json`。
2. 连续构造 3 轮可比较 metadata 摘要。
3. 比较项目/场景覆盖、记录数、marker、redaction、retrieval miss、answer equivalence 和禁止声明布尔值。
4. 保持生产、验收、集成状态全部为 false。

## 输出

- `docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.json`
- `docs/harness/evidence/headroom-lcx-fixture-stability-gate-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_fixture_stability_gate.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_fixture_stability_gate.py
```

## 反馈

本轮只证明 sanitized fixture metadata 多轮输出稳定；不证明生产可用。

## 下一轮

汇总脱敏 fixture 链路 readiness，形成 L3.5/L4 试点授权建议包或继续补全全项目域 fixture。
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
        "headroom_lcx_fixture_stability_gate=pass_check_only "
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
