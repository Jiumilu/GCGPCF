#!/usr/bin/env python3
"""Build Headroom LCX marker/retrieval-miss comparison gate evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_REPLAY = ROOT / "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-001.md"

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

ALLOWED_COMPARE_FIELDS = [
    "marker_gate",
    "sensitive_redaction_gate",
    "ccr_retrieval_miss_count",
    "answer_equivalence",
]


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622
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
    source = load_json(SOURCE_REPLAY)
    records = source.get("replay_records", [])
    failures: list[str] = []
    comparisons = []

    if source.get("evidence_id") != "HEADROOM-LCX-METADATA-REPLAY-CHECK-20260622":
        failures.append("source_evidence_id_mismatch")
    if source.get("projects") != PROJECTS or source.get("project_count") != 15:
        failures.append("project_scope_mismatch")
    if source.get("gates", {}).get("check_only") is not True:
        failures.append("source_not_check_only")
    if source.get("gates", {}).get("measured_production_tokens") is not False:
        failures.append("source_claims_measured_production_tokens")

    for index, record in enumerate(records):
        comparison = {
            "record_index": index,
            "task_id_candidate": record.get("task_id_candidate"),
            "project_id": record.get("project_id"),
            "compared_fields": {field: record.get(field) for field in ALLOWED_COMPARE_FIELDS},
            "marker_gate_preserved": record.get("marker_gate") in {"pass", "not_measured"},
            "answer_equivalence_preserved": record.get("answer_equivalence") in {"pass", "not_measured"},
            "sensitive_redaction_gate_pass": record.get("sensitive_redaction_gate") == "pass",
            "ccr_retrieval_miss_count_zero": record.get("ccr_retrieval_miss_count") == 0,
            "raw_text_compared": False,
            "production_tokens_compared": False,
        }
        if not comparison["marker_gate_preserved"]:
            failures.append(f"record_{index}_marker_gate_not_preserved")
        if not comparison["answer_equivalence_preserved"]:
            failures.append(f"record_{index}_answer_equivalence_not_preserved")
        if not comparison["sensitive_redaction_gate_pass"]:
            failures.append(f"record_{index}_sensitive_redaction_gate_not_pass")
        if not comparison["ccr_retrieval_miss_count_zero"]:
            failures.append(f"record_{index}_ccr_retrieval_miss_count_not_zero")
        comparisons.append(comparison)

    return {
        "evidence_id": "HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-MARKER-RETRIEVAL-MISS-COMPARISON-GATE-001",
        "date": "2026-06-22",
        "status": "marker_retrieval_miss_comparison_gate_pass_no_measurement",
        "scope": "sanitized_metadata_comparison_only",
        "project_count": 15,
        "projects": PROJECTS,
        "source_replay": SOURCE_REPLAY.relative_to(ROOT).as_posix(),
        "allowed_compare_fields": ALLOWED_COMPARE_FIELDS,
        "entry_count": len(records),
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "comparison_failures": failures,
        "calculation": {
            "saving_rate": "not_calculated",
            "tokens_saved": "not_calculated",
            "reason": "marker_retrieval_miss_metadata_comparison_only",
        },
        "gates": {
            "marker_retrieval_miss_comparison_gate": not failures,
            "metadata_only": True,
            "raw_text_compared": False,
            "production_tokens_compared": False,
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
        frontmatter(
            "Headroom LCX Marker Retrieval Miss Comparison Gate Evidence",
            EVIDENCE_MD.relative_to(ROOT).as_posix(),
        ),
        "# Headroom LCX Marker Retrieval Miss Comparison Gate Evidence",
        "",
        "## Summary",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- source_replay: `{evidence['source_replay']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- entry_count: `{evidence['entry_count']}`",
        f"- comparison_count: `{evidence['comparison_count']}`",
        "",
        "## Allowed Compare Fields",
        "",
    ]
    for field in evidence["allowed_compare_fields"]:
        lines.append(f"- `{field}`")
    lines.extend(["", "## Gates", "", "| Gate | Value |", "|---|---|"])
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "| saving_rate | not_calculated |",
            "| tokens_saved | not_calculated |",
            "",
            "## Non-Claims",
            "",
            "- This evidence does not compare raw prompt, raw completion, customer contract text, POD, financial voucher, key, production credential, or provider secret.",
            "- This evidence does not calculate real production token saving.",
            "- This evidence does not start Headroom production proxy or enable production SDK.",
            "- This evidence does not mark Headroom as accepted, integrated, or production_ready.",
            "",
        ]
    )
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX Marker Retrieval Miss Comparison Gate 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX Marker Retrieval Miss Comparison Gate 001

## 输入

继续 Headroom LCX 项目群下一步，只允许使用脱敏 metadata replay evidence 建立 marker/retrieval miss comparison gate。

## 动作

1. 读取 `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`。
2. 只比较 `marker_gate`、`sensitive_redaction_gate`、`ccr_retrieval_miss_count`、`answer_equivalence`。
3. 生成 comparison gate evidence。
4. 保持所有生产、验收、集成状态为 false。

## 输出

- `docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.json`
- `docs/harness/evidence/headroom-lcx-marker-retrieval-miss-comparison-gate-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_marker_retrieval_miss_comparison_gate.py --check-only
python3 tools/kds-sync/validate_headroom_lcx_marker_retrieval_miss_comparison_gate.py
```

## 反馈

本轮只证明脱敏 metadata comparison gate 可回放；不证明真实生产 token 节省、真实 marker pass、真实 answer equivalence pass 或生产可用。

## 下一轮

建立 sanitized token fixture 扩展包，至少覆盖 5 个项目域和 3 类场景，但仍不读取原文、不进入生产。
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
        "headroom_lcx_marker_retrieval_miss_comparison_gate=pass_check_only "
        f"project_count={evidence['project_count']} entry_count={evidence['entry_count']} "
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
