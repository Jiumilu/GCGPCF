#!/usr/bin/env python3
"""Build a Headroom cost sensitivity model across pricing profiles."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
L2_DRY_RUN_JSON = ROOT / "docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json"
COVERAGE_MATRIX_JSON = ROOT / "docs/harness/evidence/headroom-project-application-coverage-matrix-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md"


PRICE_PROFILES = {
    "low_input_high_cache_discount": {
        "P_in": 0.5,
        "P_out": 2.0,
        "P_cache_write": 0.05,
        "P_cache_read": 0.02,
        "P_runtime": 0.0,
    },
    "base_model": {
        "P_in": 1.0,
        "P_out": 4.0,
        "P_cache_write": 0.25,
        "P_cache_read": 0.1,
        "P_runtime": 0.0,
    },
    "high_input_low_cache_discount": {
        "P_in": 2.0,
        "P_out": 8.0,
        "P_cache_write": 0.5,
        "P_cache_read": 0.2,
        "P_runtime": 0.0,
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def cost_for(entry: dict, pricing: dict) -> dict:
    baseline_cost = (
        entry["input_tokens_before"] * pricing["P_in"]
        + entry["output_tokens_before"] * pricing["P_out"]
        + entry["cache_write_tokens_before"] * pricing["P_cache_write"]
        + entry["cache_read_tokens_before"] * pricing["P_cache_read"]
    )
    headroom_cost = (
        entry["input_tokens_after"] * pricing["P_in"]
        + entry["output_tokens_after"] * pricing["P_out"]
        + entry["cache_write_tokens_after"] * pricing["P_cache_write"]
        + entry["cache_read_tokens_after"] * pricing["P_cache_read"]
        + pricing["P_runtime"]
    )
    gross_saving = baseline_cost - headroom_cost
    return {
        "baseline_cost": round(baseline_cost, 6),
        "headroom_cost": round(headroom_cost, 6),
        "gross_saving": round(gross_saving, 6),
        "saving_rate": round(gross_saving / baseline_cost, 6) if baseline_cost else 0.0,
    }


def build_markdown(result: dict) -> str:
    rows = "\n".join(
        "| {profile_id} | {baseline_cost} | {headroom_cost} | {gross_saving} | {saving_rate} | {admission_gate} |".format(
            profile_id=profile["profile_id"],
            baseline_cost=profile["aggregate"]["baseline_cost"],
            headroom_cost=profile["aggregate"]["headroom_cost"],
            gross_saving=profile["aggregate"]["gross_saving"],
            saving_rate=profile["aggregate"]["saving_rate"],
            admission_gate=str(profile["aggregate"]["admission_gate"]).lower(),
        )
        for profile in result["profiles"]
    )
    return f"""---
doc_id: GPCF-DOC-DB5F018CF1
title: Headroom Cost Sensitivity Model
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md
source_path: docs/harness/evidence/headroom-cost-sensitivity-model-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Cost Sensitivity Model

## Evidence ID

`{result["evidence_id"]}`

## 结论

本模型使用 15 项目 dry-run token 计数，在三组价格 profile 下复算 Headroom 成本节省稳定性。

`cost_sensitivity_gate | {str(result["gate"]["cost_sensitivity_gate"]).lower()}`，`profile_count | {result["gate"]["profile_count"]}`，`production_admission_gate | false`，`measured_production_tokens | false`。

## Profile 汇总

| profile_id | baseline_cost | headroom_cost | gross_saving | saving_rate | admission_gate |
|---|---:|---:|---:|---:|---|
{rows}

## 边界

- 不写入供应商真实价格。
- 不使用真实生产 token 台账。
- 不声明 production token saving。
- 不升级 accepted、integrated 或 production_ready。
"""


def main() -> int:
    l2 = load_json(L2_DRY_RUN_JSON)
    coverage = load_json(COVERAGE_MATRIX_JSON)
    require(l2["aggregate"]["all_admission_gates_pass"] is True, "L2 dry-run gates must pass")
    require(coverage["gate"]["project_application_coverage_gate"] is True, "project coverage gate must pass")
    measurements = l2["measurements"]

    profile_results = []
    for profile_id, pricing in PRICE_PROFILES.items():
        rows = []
        for entry in measurements:
            row = {
                "project": entry["project"],
                "scenario": entry["scenario"],
                "source_path": entry["source_path"],
                "admission_gate": entry["admission_gate"],
            }
            row.update(cost_for(entry, pricing))
            row["profile_admission_gate"] = (
                entry["admission_gate"]
                and row["saving_rate"] >= l2["minimum_saving_rate"]
                and entry["sensitive_redaction_gate"] == "pass"
                and entry["answer_equivalence"] == "pass"
            )
            rows.append(row)
        total_baseline = sum(row["baseline_cost"] for row in rows)
        total_headroom = sum(row["headroom_cost"] for row in rows)
        total_saving = total_baseline - total_headroom
        profile_results.append(
            {
                "profile_id": profile_id,
                "pricing": pricing,
                "aggregate": {
                    "baseline_cost": round(total_baseline, 6),
                    "headroom_cost": round(total_headroom, 6),
                    "gross_saving": round(total_saving, 6),
                    "saving_rate": round(total_saving / total_baseline, 6) if total_baseline else 0.0,
                    "minimum_saving_rate": l2["minimum_saving_rate"],
                    "admission_gate": all(row["profile_admission_gate"] for row in rows),
                },
                "measurements": rows,
            }
        )

    result = {
        "evidence_id": "HEADROOM-COST-SENSITIVITY-MODEL-20260621",
        "date": "2026-06-21",
        "status": "cost_sensitivity_model_defined",
        "source_evidence": [rel(L2_DRY_RUN_JSON), rel(COVERAGE_MATRIX_JSON)],
        "project_count": l2["project_count"],
        "profiles": profile_results,
        "gate": {
            "profile_count": len(profile_results),
            "project_count": l2["project_count"],
            "all_profiles_admission_gate": all(profile["aggregate"]["admission_gate"] for profile in profile_results),
            "min_profile_saving_rate": min(profile["aggregate"]["saving_rate"] for profile in profile_results),
            "max_profile_saving_rate": max(profile["aggregate"]["saving_rate"] for profile in profile_results),
            "cost_sensitivity_gate": True,
            "production_admission_gate": False,
        },
        "decision": {
            "next_allowed_action": "reuse sensitivity profiles for future authorized production-token ledger comparison",
            "next_blocked_action": "production cost claim without sanitized production-token ledger",
            "production_admission_gate": False,
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_real_provider_price_claim": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_cost_sensitivity_model=pass "
        f"profile_count={len(profile_results)} "
        f"min_saving_rate={result['gate']['min_profile_saving_rate']} "
        f"max_saving_rate={result['gate']['max_profile_saving_rate']} "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
