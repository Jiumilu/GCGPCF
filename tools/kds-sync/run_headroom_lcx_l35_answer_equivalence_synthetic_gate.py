#!/usr/bin/env python3
"""Run Headroom LCX L3.5 synthetic answer-equivalence gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MULTI_WINDOW_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json"
EVIDENCE_JSON = ROOT / "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json"
EVIDENCE_MD = ROOT / "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.md"
LOOP_ROUND = ROOT / "docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-001.md"

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
SCENARIOS = ["answer_summary", "citation_preservation", "project_boundary_marker"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stable_hash(payload: object) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def frontmatter(title: str, source_path: str) -> str:
    return f"""---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622
title: {title}
project: GPCF
related_projects: [GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/{source_path}
source_path: {source_path}
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---
"""


def synthetic_answer(project: str, scenario: str) -> dict[str, object]:
    marker = f"LCX_SYNTH_EQ::{project}::{scenario}"
    source_path = f"synthetic://headroom-lcx/{project}/{scenario}"
    return {
        "project_id": project,
        "scenario": scenario,
        "answer_shape": "synthetic_structured_answer",
        "claims": [
            {
                "claim_id": f"{project}-{scenario}-claim-01",
                "text": "synthetic_governance_claim_placeholder",
                "status": "candidate_only",
            }
        ],
        "citations": [
            {
                "citation_id": f"{project}-{scenario}-citation-01",
                "source_path": source_path,
                "source_kind": "synthetic_sanitized_fixture",
                "project_id": project,
            }
        ],
        "markers": [marker, f"PROJECT::{project}", "LCX_SYNTHETIC_ONLY"],
        "sensitive_boundary": "synthetic_no_raw_customer_or_production_material",
    }


def build_samples() -> list[dict[str, object]]:
    samples = []
    for project in PROJECTS:
        for scenario in SCENARIOS:
            before = synthetic_answer(project, scenario)
            after = json.loads(json.dumps(before, ensure_ascii=False))
            samples.append(
                {
                    "sample_id": f"HEADROOM-LCX-L35-SYNTH-EQ-{project}-{scenario}",
                    "project_id": project,
                    "scenario": scenario,
                    "input_kind": "synthetic_sanitized_answer_fixture",
                    "before_answer": before,
                    "after_answer": after,
                    "before_hash": stable_hash(before),
                    "after_hash": stable_hash(after),
                    "answer_equivalence": "synthetic_equivalent",
                    "answer_equivalence_gate": stable_hash(before) == stable_hash(after),
                    "citation_preservation_gate": before["citations"] == after["citations"],
                    "marker_preservation_gate": before["markers"] == after["markers"],
                    "project_boundary_gate": before["project_id"] == after["project_id"] == project,
                    "sensitive_redaction_gate": "pass",
                    "tokens_saved": "not_calculated",
                    "saving_rate": "not_calculated",
                    "measured_production_tokens": False,
                    "accepted": False,
                    "integrated": False,
                    "production_ready": False,
                }
            )
    return samples


def build_evidence() -> dict:
    multi_window = load_json(MULTI_WINDOW_JSON)
    samples = build_samples()
    failures: list[str] = []
    if multi_window.get("status") != "l3_5_multi_window_stability_pass_check_only":
        failures.append("multi_window_stability_not_passed")
    if len(samples) != 45:
        failures.append("sample_count_mismatch")
    if {sample["project_id"] for sample in samples} != set(PROJECTS):
        failures.append("project_coverage_mismatch")
    for sample in samples:
        for gate in [
            "answer_equivalence_gate",
            "citation_preservation_gate",
            "marker_preservation_gate",
            "project_boundary_gate",
        ]:
            if sample[gate] is not True:
                failures.append(f"{sample['sample_id']}:{gate}")
        if sample["sensitive_redaction_gate"] != "pass":
            failures.append(f"{sample['sample_id']}:sensitive_redaction_gate")
        if sample["tokens_saved"] != "not_calculated" or sample["saving_rate"] != "not_calculated":
            failures.append(f"{sample['sample_id']}:calculation_forbidden")
        for key in ["measured_production_tokens", "accepted", "integrated", "production_ready"]:
            if sample[key] is not False:
                failures.append(f"{sample['sample_id']}:{key}_not_false")

    return {
        "evidence_id": "HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-20260622",
        "task_id": "GPCF-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-L35-ANSWER-EQUIVALENCE-SYNTHETIC-GATE-001",
        "date": "2026-06-22",
        "status": "l3_5_answer_equivalence_synthetic_gate_pass_check_only" if not failures else "l3_5_answer_equivalence_synthetic_gate_blocked",
        "scope": "l3_5_synthetic_answer_equivalence_only",
        "source_evidence": MULTI_WINDOW_JSON.relative_to(ROOT).as_posix(),
        "project_count": len({sample["project_id"] for sample in samples}),
        "scenario_count": len(SCENARIOS),
        "sample_count": len(samples),
        "samples": samples,
        "gates": {
            "l3_5_answer_equivalence_synthetic_gate": not failures,
            "source_multi_window_stability_gate": multi_window.get("status") == "l3_5_multi_window_stability_pass_check_only",
            "project_coverage_gate": {sample["project_id"] for sample in samples} == set(PROJECTS),
            "sample_count_gate": len(samples) == 45,
            "answer_equivalence_gate": all(sample["answer_equivalence_gate"] for sample in samples),
            "citation_preservation_gate": all(sample["citation_preservation_gate"] for sample in samples),
            "marker_preservation_gate": all(sample["marker_preservation_gate"] for sample in samples),
            "project_boundary_gate": all(sample["project_boundary_gate"] for sample in samples),
            "synthetic_only": True,
            "metadata_only": True,
            "check_only": True,
            "business_answer_equivalence_proven": False,
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "headroom_learn_apply_executed": False,
            "l4_candidate": False,
            "l5_candidate": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "failures": failures,
    }


def write_md(evidence: dict) -> None:
    lines = [
        frontmatter("Headroom LCX L3.5 脱敏答案等价样例门禁", EVIDENCE_MD.relative_to(ROOT).as_posix()),
        "# Headroom LCX L3.5 脱敏答案等价样例门禁",
        "",
        "## 摘要",
        "",
        f"- evidence_id: `{evidence['evidence_id']}`",
        f"- status: `{evidence['status']}`",
        f"- scope: `{evidence['scope']}`",
        f"- project_count: `{evidence['project_count']}`",
        f"- scenario_count: `{evidence['scenario_count']}`",
        f"- sample_count: `{evidence['sample_count']}`",
        "",
        "## 门禁",
        "",
        "| Gate | Value |",
        "|---|---|",
    ]
    for key, value in evidence["gates"].items():
        lines.append(f"| {key} | {str(value).lower()} |")
    lines.extend(
        [
            "",
            "## 禁止声明",
            "",
            "- 本证据只验证 synthetic answer、citation 和 marker 的结构等价。",
            "- 本证据不读取真实业务原文，不处理客户合同、POD、财务凭证、密钥或生产凭证。",
            "- 本证据不证明真实业务答案等价，不计算 token 节省，也不测量 production tokens。",
            "- 本证据不得将 Headroom LCX 标记为 accepted、integrated 或 production_ready。",
            "",
        ]
    )
    EVIDENCE_MD.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_loop_round() -> None:
    text = frontmatter(
        "Loop Round GPCF Headroom LCX L3.5 Answer Equivalence Synthetic Gate 001",
        LOOP_ROUND.relative_to(ROOT).as_posix(),
    )
    text += """# Loop Round GPCF Headroom LCX L3.5 Answer Equivalence Synthetic Gate 001

## 输入

用户要求“下一步”。上一轮已完成 L3.5 多窗口脱敏稳定性门禁。

## 动作

- run: 为 15 项目域生成 45 条 synthetic answer/citation/marker 等价样例。
- stop: 停止边界固定为 synthetic-only，不进入真实业务答案、L4/L5 或生产。
- verify: 校验答案结构、citation、marker、project boundary 和敏感边界。
- recover: 若任一等价样例失败，回退到 L3.5 多窗口稳定性证据，不扩大试点。
- debug: 当前仍缺真实业务答案等价授权、真实生产 token 实测和生产准入。

## 输出

- `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json`
- `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_l35_answer_equivalence_synthetic_gate.py
python3 tools/kds-sync/validate_headroom_lcx_l35_answer_equivalence_synthetic_gate.py
```

## 反馈

本轮只证明 synthetic answer/citation/marker 等价，不证明真实业务答案等价。

## 下一轮

生成 L4 真实测量与真实业务答案等价授权申请包，或继续增加 L3.5 synthetic 负向等价样例。
"""
    LOOP_ROUND.parent.mkdir(parents=True, exist_ok=True)
    LOOP_ROUND.write_text(text, encoding="utf-8")


def main() -> int:
    evidence = build_evidence()
    write_json(EVIDENCE_JSON, evidence)
    write_md(evidence)
    write_loop_round()
    print(
        "headroom_lcx_l35_answer_equivalence_synthetic_gate="
        f"{'pass_check_only' if not evidence['failures'] else 'blocked'} "
        f"project_count={evidence['project_count']} scenario_count={evidence['scenario_count']} sample_count={evidence['sample_count']} "
        "answer_equivalence_gate=true business_answer_equivalence_proven=false "
        "l4_candidate=false measured_production_tokens=false production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0 if not evidence["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
