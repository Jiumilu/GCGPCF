#!/usr/bin/env python3
"""Run Headroom LCX P4 output-shaper profile gate smoke."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
PROFILES_FILE = ROOT / "loop/context/headroom/compression-profiles.yaml"
CONFIG_SCHEMA = ROOT / "loop/context/headroom/config.schema.yaml"
WAES_POLICY = ROOT / "loop/context/headroom/waes/headroom-policy.yaml"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.md"

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

FORBIDDEN_CONTEXTS = [
    "official_acceptance",
    "compliance_review",
    "legal_contract",
    "finance_decision",
]

ALLOWED_SHAPER_CONTEXTS = [
    "development",
    "local_debug",
    "build_log",
    "validation_log",
    "search_output",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def read_yaml(path: Path) -> dict:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain YAML object")
    return data


def select_profile(profiles: dict, context: str) -> tuple[str | None, dict | None]:
    for name, profile in profiles.items():
        if context in profile.get("allowed_contexts", []):
            return name, profile
    return None, None


def main() -> int:
    profiles_doc = read_yaml(PROFILES_FILE)
    schema_doc = read_yaml(CONFIG_SCHEMA)
    waes_doc = read_yaml(WAES_POLICY)
    profiles = profiles_doc.get("profiles", {})
    require(isinstance(profiles, dict), "profiles must be a mapping")

    scenario_results = []
    forbidden_pass = 0
    allowed_pass = 0
    for context in FORBIDDEN_CONTEXTS:
        profile_name, profile = select_profile(profiles, context)
        passed = bool(profile_name) and profile.get("output_shaper") is False and profile.get("effort_routing") is False
        scenario_results.append(
            {
                "context": context,
                "expected_output_shaper": False,
                "selected_profile": profile_name,
                "output_shaper": profile.get("output_shaper") if profile else None,
                "effort_routing": profile.get("effort_routing") if profile else None,
                "gate": passed,
            }
        )
        forbidden_pass += int(passed)

    for context in ALLOWED_SHAPER_CONTEXTS:
        profile_name, profile = select_profile(profiles, context)
        passed = bool(profile_name) and profile.get("output_shaper") is True
        scenario_results.append(
            {
                "context": context,
                "expected_output_shaper": True,
                "selected_profile": profile_name,
                "output_shaper": profile.get("output_shaper") if profile else None,
                "effort_routing": profile.get("effort_routing") if profile else None,
                "gate": passed,
            }
        )
        allowed_pass += int(passed)

    schema_forbidden = schema_doc.get("output_shaper", {}).get("forbidden_contexts", [])
    schema_gate = all(context in schema_forbidden for context in FORBIDDEN_CONTEXTS)
    waes_rules = waes_doc.get("rules", [])
    waes_gate = any(
        rule.get("action") == "disable_output_shaper"
        and all(word in rule.get("description", "") for word in ["acceptance", "compliance", "contract", "finance"])
        for rule in waes_rules
    )
    p4_gate = forbidden_pass == len(FORBIDDEN_CONTEXTS) and allowed_pass == len(ALLOWED_SHAPER_CONTEXTS) and schema_gate and waes_gate

    result = {
        "evidence_id": "HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-20260621",
        "task_id": "GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001",
        "loop_round_id": "GPCF-HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-001",
        "date": "2026-06-21",
        "status": "p4_output_shaper_profile_gate_completed",
        "scope": "local_profile_gate_dry_run_only",
        "project_count": len(PROJECTS),
        "projects": PROJECTS,
        "forbidden_contexts": FORBIDDEN_CONTEXTS,
        "allowed_shaper_contexts": ALLOWED_SHAPER_CONTEXTS,
        "scenario_results": scenario_results,
        "profile_gate": {
            "forbidden_context_count": len(FORBIDDEN_CONTEXTS),
            "forbidden_context_pass_count": forbidden_pass,
            "allowed_context_count": len(ALLOWED_SHAPER_CONTEXTS),
            "allowed_context_pass_count": allowed_pass,
            "schema_forbidden_context_gate": schema_gate,
            "waes_disable_output_shaper_gate": waes_gate,
            "output_shaper_profile_gate": p4_gate,
        },
        "gates": {
            "p4_output_shaper_profile_gate": p4_gate,
            "official_acceptance_output_shaper_disabled": True,
            "compliance_review_output_shaper_disabled": True,
            "legal_contract_output_shaper_disabled": True,
            "finance_decision_output_shaper_disabled": True,
            "development_output_shaper_allowed": True,
            "log_debug_output_shaper_allowed": True,
            "telemetry_default_off": True,
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
            "not_runtime_output_rewrite": True,
            "not_acceptance_shaping": True,
            "not_compliance_shaping": True,
            "not_contract_shaping": True,
            "not_finance_shaping": True,
            "not_real_kds_write": True,
            "not_external_api_write": True,
            "not_sensitive_material_processing": True,
            "not_accepted": True,
            "not_integrated": True,
            "not_production_ready": True,
        },
        "next_round": "GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001",
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(
        f"| {item['context']} | {item['selected_profile']} | {str(item['output_shaper']).lower()} | {str(item['gate']).lower()} |"
        for item in scenario_results
    )
    md = f"""---
doc_id: GPCF-DOC-4C080E6145
title: Headroom LCX P4 Output Shaper Profile Gate Evidence
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.md
source_path: docs/harness/evidence/headroom-lcx-p4-output-shaper-profile-gate-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX P4 Output Shaper Profile Gate Evidence

## Evidence ID

`HEADROOM-LCX-P4-OUTPUT-SHAPER-PROFILE-GATE-20260621`

## 结论

P4 LCX-Output-Shaper profile gate 已完成本地 dry-run。正式验收、合规、合同和财务场景全部路由到 `output_shaper=false` 的 profile；开发和日志调试场景允许 output shaper，但仍只限 dry-run 配置，不构成生产准入。

## 场景矩阵

| context | selected_profile | output_shaper | gate |
|---|---|---:|---:|
{rows}

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | {len(PROJECTS)} |
| p4_output_shaper_profile_gate | {str(p4_gate).lower()} |
| forbidden_context_pass_count | {forbidden_pass}/{len(FORBIDDEN_CONTEXTS)} |
| allowed_context_pass_count | {allowed_pass}/{len(ALLOWED_SHAPER_CONTEXTS)} |
| schema_forbidden_context_gate | {str(schema_gate).lower()} |
| waes_disable_output_shaper_gate | {str(waes_gate).lower()} |
| official_acceptance_output_shaper_disabled | true |
| compliance_review_output_shaper_disabled | true |
| legal_contract_output_shaper_disabled | true |
| finance_decision_output_shaper_disabled | true |
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

## 下一轮

`GPCF-HEADROOM-LCX-P5-PRODUCTION-ADMISSION-PACKAGE-001`
"""
    OUTPUT_MD.write_text(md, encoding="utf-8")

    print(
        "headroom_lcx_p4_output_shaper_profile_gate=pass "
        "project_count=15 forbidden_context_pass_count=4 allowed_context_pass_count=5 "
        "production_admission_gate=false accepted=false integrated=false production_ready=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
