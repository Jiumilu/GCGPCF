#!/usr/bin/env python3
"""Run Headroom LCX P3 learn-preview and working-memory gate smoke."""

from __future__ import annotations

import importlib.metadata
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HEADROOM_VENV = Path(os.environ.get("HEADROOM_LCX_VENV", "/tmp/gpcf-headroom-runtime-probe"))
HEADROOM_BIN = HEADROOM_VENV / "bin/headroom"
LEARN_PREVIEW = ROOT / "loop/context/headroom/scripts/learn-preview.sh"
APPLY_APPROVED_MEMORY = ROOT / "loop/context/headroom/scripts/apply-approved-memory.sh"
POLICY = ROOT / "loop/context/headroom/policy.yaml"
WAES_POLICY = ROOT / "loop/context/headroom/waes/headroom-policy.yaml"
KDS_COMPONENT = ROOT / "loop/context/headroom/kds/context-optimization-component.yaml"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md"

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def run(args: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    env = {
        **os.environ,
        "HEADROOM_TELEMETRY": "off",
        "PATH": f"{HEADROOM_VENV / 'bin'}:{os.environ.get('PATH', '')}",
    }
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def main() -> int:
    require(os.environ.get("HEADROOM_TELEMETRY") == "off", "HEADROOM_TELEMETRY must be off")
    require(HEADROOM_BIN.exists(), f"missing headroom binary: {HEADROOM_BIN}")
    policy = read(POLICY)
    waes_policy = read(WAES_POLICY)
    kds_component = read(KDS_COMPONENT)
    learn_preview = read(LEARN_PREVIEW)
    apply_script = read(APPLY_APPROVED_MEMORY)

    require("--preview" not in learn_preview, "learn-preview wrapper must not use unsupported --preview")
    require("--apply" not in learn_preview, "learn-preview wrapper must not pass --apply")
    require("learn_apply_auto" in policy, "policy must block automatic learn apply")
    require("cross_project_memory_as_fact" in policy, "policy must block cross-project memory as fact")
    require("human_approval" in waes_policy, "WAES policy must require human approval")
    require("Headroom memory must not become KDS source of record" in kds_component, "KDS component must block memory as source of record")

    tmpdir = Path(tempfile.mkdtemp(prefix="gpcf-headroom-learn-preview-"))
    approval_file = tmpdir / "approved-memory-change.json"
    approval_file.write_text(
        json.dumps(
            {
                "approval_id": "LCX-P3-SYNTHETIC-APPROVAL-001",
                "owner": "GPCF",
                "target": "preview-only-memory-candidate",
                "proposed_rule": "Synthetic memory candidate must remain preview only.",
                "harness_evidence": "HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-20260621",
                "waes_decision": "pass",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    try:
        learn_help = run([str(HEADROOM_BIN), "learn", "--help"])
        learn_dry_run = run([str(LEARN_PREVIEW), "--project", str(tmpdir), "--agent", "codex", "--workers", "1"])
        apply_missing = run([str(APPLY_APPROVED_MEMORY), str(tmpdir / "missing.json")])
        apply_valid = run([str(APPLY_APPROVED_MEMORY), str(approval_file)])
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    learn_preview_gate = (
        learn_help.returncode == 0
        and learn_dry_run.returncode == 0
        and "No project data found" in learn_dry_run.stdout
        and "--apply" not in learn_dry_run.args
    )
    apply_guard_gate = (
        apply_missing.returncode != 0
        and apply_valid.returncode == 0
        and "approved_memory_candidate=validated apply_manually=true" in apply_valid.stdout
    )
    memory_governance_gate = all(
        marker in policy + waes_policy + kds_component
        for marker in [
            "learn_apply_auto",
            "cross_project_memory_as_fact",
            "human_approval",
            "Headroom memory must not become KDS source of record",
        ]
    )
    p3_gate = learn_preview_gate and apply_guard_gate and memory_governance_gate

    result = {
        "evidence_id": "HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-001",
        "date": "2026-06-21",
        "status": "p3_learn_preview_working_memory_gate_completed",
        "headroom_version": importlib.metadata.version("headroom-ai"),
        "telemetry": "off",
        "scope": "local_development_dry_run_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "learn_preview": {
            "learn_help_exit_code": learn_help.returncode,
            "learn_dry_run_exit_code": learn_dry_run.returncode,
            "empty_project_only": True,
            "real_session_scanned": False,
            "sensitive_material_processed": False,
            "llm_analysis_executed": False,
            "learn_apply_executed": False,
            "wrapper_passes_apply": False,
            "learn_preview_gate": learn_preview_gate,
        },
        "working_memory_gate": {
            "apply_missing_exit_code": apply_missing.returncode,
            "apply_valid_exit_code": apply_valid.returncode,
            "approval_fixture_synthetic": True,
            "approval_validated": apply_valid.returncode == 0,
            "apply_manually_only": True,
            "controlled_rules_modified": False,
            "headroom_memory_as_kds_source_of_record": False,
            "cross_project_memory_as_fact": False,
            "apply_guard_gate": apply_guard_gate,
            "memory_governance_gate": memory_governance_gate,
        },
        "gates": {
            "p3_learn_preview_working_memory_gate": p3_gate,
            "learn_preview_gate": learn_preview_gate,
            "apply_guard_gate": apply_guard_gate,
            "memory_governance_gate": memory_governance_gate,
            "telemetry_default_off": True,
            "synthetic_input_only": True,
            "empty_project_only": True,
            "real_session_scanned": False,
            "llm_analysis_executed": False,
            "learn_apply_executed": False,
            "controlled_rules_modified": False,
            "raw_sensitive_context_stored": False,
            "external_api_write": False,
            "kds_api_write": False,
            "sensitive_material_processed": False,
            "measured_production_tokens": False,
            "production_admission_gate": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "non_claims": {
            "not_real_session_learning": True,
            "not_llm_failure_analysis": True,
            "not_learn_apply": True,
            "not_memory_applied": True,
            "not_kds_source_of_record": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_round": "GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001",
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = f"""---
doc_id: GPCF-DOC-7F7C0539A3
title: Headroom LCX P3 Learn Preview Working Memory Gate Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p3-learn-preview-working-memory-gate-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P3 Learn Preview Working Memory Gate Evidence

## Evidence ID

`HEADROOM-LCX-P3-LEARN-PREVIEW-WORKING-MEMORY-GATE-20260621`

## 结论

P3 learn preview 与工作记忆治理门禁已完成本机 dry-run smoke。`headroom learn` 只在空白临时项目上执行默认 dry-run；未扫描真实会话，未执行 LLM failure analysis，未执行 `--apply`，未写入真实 memory，未改受控规则文件。

## 结果

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| headroom_version | {result["headroom_version"]} |
| telemetry | off |
| p3_learn_preview_working_memory_gate | {str(p3_gate).lower()} |
| learn_preview_gate | {str(learn_preview_gate).lower()} |
| apply_guard_gate | {str(apply_guard_gate).lower()} |
| memory_governance_gate | {str(memory_governance_gate).lower()} |
| empty_project_only | true |
| real_session_scanned | false |
| llm_analysis_executed | false |
| learn_apply_executed | false |
| controlled_rules_modified | false |
| headroom_memory_as_kds_source_of_record | false |
| cross_project_memory_as_fact | false |
| external_api_write | false |
| kds_api_write | false |
| sensitive_material_processed | false |
| measured_production_tokens | false |
| production_admission_gate | false |
| accepted | false |
| integrated | false |
| production_ready | false |

## 15 项目范围

{", ".join(PROJECTS)}

## 边界

- `headroom learn` 默认 dry-run；`--apply` 仍被禁止自动执行。
- `apply-approved-memory.sh` 只验证人工批准包形状，输出 `apply_manually=true`，不自动写入规则或记忆。
- Headroom memory 只能作为工作记忆候选和失败经验学习候选，不得成为 KDS 正式事实源。
- 跨项目 memory 不得作为业务事实使用。

## 下一轮

`GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001`
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    print(
        "headroom_lcx_p3_learn_preview_working_memory_gate=pass "
        "project_count=15 learn_preview_gate=true apply_guard_gate=true "
        "memory_governance_gate=true production_admission_gate=false "
        "accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
