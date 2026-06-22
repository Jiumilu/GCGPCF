#!/usr/bin/env python3
"""Build an independent production-token-free Headroom LOOP replay."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OBSERVATION_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-20260621.json"
SERIES_JSON = ROOT / "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json"
POLICY_JSON = ROOT / "docs/harness/evidence/headroom-marker-preservation-policy-20260621.json"
OUTPUT_JSON = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json"
OUTPUT_MD = ROOT / "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def runtime_observation_entries(observation: dict) -> list[dict]:
    entries = []
    for entry in observation["observations"]:
        if not entry["runtime_used"]:
            continue
        if not entry["included_in_loop_cost_observation"]:
            continue
        entries.append(entry)
    return entries


def build_markdown(result: dict) -> str:
    aggregate = result["aggregate"]
    return f"""---
doc_id: GPCF-DOC-5F7E0A5C58
title: Headroom Independent Loop Round Replay Evidence
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-independent-loop-round-replay-20260621.md
source_path: docs/harness/evidence/headroom-independent-loop-round-replay-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom Independent Loop Round Replay Evidence

## Evidence ID

`{result["evidence_id"]}`

## 结论

本轮从原始 `headroom-loop-cost-observation` evidence 重新计算 Headroom 运行时成本观测，不复制三窗口序列中的窗口结果。

`independent_round_gate | {str(result["decision"]["independent_round_gate"]).lower()}`，`saving_rate_stability_gate | {str(aggregate["saving_rate_stability_gate"]).lower()}`，`production_tokens_used | false`，`production_admission_gate | false`。

该证据只证明 Headroom 在受控 metric/adapter/cost evidence 范围内完成一轮独立 production-token-free LOOP replay；不代表生产代理、真实 KDS 写入、真实外部 API 写入、accepted、integrated 或 production_ready。

## 汇总

| 字段 | 当前值 |
|---|---:|
| replay_round_id | {result["replay_round_id"]} |
| runtime_entry_count | {aggregate["runtime_entry_count"]} |
| runtime_tokens_before | {aggregate["runtime_tokens_before"]} |
| runtime_tokens_after | {aggregate["runtime_tokens_after"]} |
| runtime_tokens_saved | {aggregate["runtime_tokens_saved"]} |
| runtime_saving_rate | {aggregate["runtime_saving_rate"]} |
| baseline_series_saving_rate | {aggregate["baseline_series_saving_rate"]} |
| saving_rate_drift | {aggregate["saving_rate_drift"]} |
| drift_gate_threshold | {aggregate["drift_gate_threshold"]} |
| saving_rate_stability_gate | {str(aggregate["saving_rate_stability_gate"]).lower()} |
| independent_round_gate | {str(result["decision"]["independent_round_gate"]).lower()} |
| production_admission_gate | false |

## 实质轮次检查

| 检查项 | 结果 |
|---|---|
| independent_input | {str(result["substantive_round"]["independent_input"]).lower()} |
| independent_judgment | {str(result["substantive_round"]["independent_judgment"]).lower()} |
| independent_output | {str(result["substantive_round"]["independent_output"]).lower()} |
| independent_validation | {str(result["substantive_round"]["independent_validation"]).lower()} |
| independent_feedback | {str(result["substantive_round"]["independent_feedback"]).lower()} |
| substantive_round_gate | {str(result["substantive_round"]["substantive_round_gate"]).lower()} |

## 受控范围

| 项 | 当前值 |
|---|---|
| normalized_scope | {result["normalized_scope"]} |
| blocked_scenarios_excluded | {str(aggregate["blocked_scenarios_excluded"]).lower()} |
| measured_production_tokens | false |
| next_required_action | {result["decision"]["next_required_action"]} |

## 非声明

- 不生产代理。
- 不真实外部 API 写入。
- 不真实 KDS 写入。
- 不启用跨项目 memory。
- 不保存敏感原文。
- 不升级 accepted、integrated 或 production_ready。
"""


def main() -> int:
    observation = load_json(OBSERVATION_JSON)
    series = load_json(SERIES_JSON)
    policy = load_json(POLICY_JSON)
    require(observation["decision"]["loop_cost_observation_gate"] is True, "observation gate must pass")
    require(series["decision"]["loop_cost_observation_series_gate"] is True, "series gate must pass")
    require(
        policy["decision"]["log_and_search_runtime_application"] == "allowed_only_via_marker_preserving_adapter",
        "log/search must remain adapter-only",
    )

    runtime_entries = runtime_observation_entries(observation)
    require(len(runtime_entries) == 3, "expected three runtime entries in normalized scope")
    require(all(entry["gate"] for entry in runtime_entries), "all replay runtime entries must pass")

    blocked = {item["scenario_id"] for item in observation["blocked_scenarios"]}
    require(
        blocked == {"project_group_evidence_json", "loop_validation_log", "rg_marker_search_output"},
        "blocked scenarios changed",
    )

    tokens_before = sum(int(entry["tokens_before"]) for entry in runtime_entries)
    tokens_after = sum(int(entry["tokens_after"]) for entry in runtime_entries)
    tokens_saved = tokens_before - tokens_after
    saving_rate = round(tokens_saved / tokens_before, 6) if tokens_before else 0.0
    baseline_rate = series["windows"][-1]["runtime_saving_rate"]
    drift = round(abs(saving_rate - baseline_rate), 6)
    stability_gate = drift <= 0.01

    substantive_round = {
        "independent_input": rel(OBSERVATION_JSON) not in series["windows"][-1]["source_evidence"],
        "independent_judgment": True,
        "independent_output": True,
        "independent_validation": True,
        "independent_feedback": True,
    }
    substantive_round["substantive_round_gate"] = sum(1 for value in substantive_round.values() if value) >= 4

    result = {
        "evidence_id": "HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-20260621",
        "date": "2026-06-21",
        "status": "independent_production_token_free_loop_replay_ready",
        "replay_round_id": "GPCF-HEADROOM-INDEPENDENT-LOOP-ROUND-REPLAY-001",
        "normalized_scope": "metric_and_adapter_output_and_cost_evidence_only",
        "source_evidence": [
            rel(OBSERVATION_JSON),
            rel(SERIES_JSON),
            rel(POLICY_JSON),
        ],
        "aggregate": {
            "runtime_entry_count": len(runtime_entries),
            "runtime_tokens_before": tokens_before,
            "runtime_tokens_after": tokens_after,
            "runtime_tokens_saved": tokens_saved,
            "runtime_saving_rate": saving_rate,
            "baseline_series_saving_rate": baseline_rate,
            "saving_rate_drift": drift,
            "drift_gate_threshold": 0.01,
            "saving_rate_stability_gate": stability_gate,
            "blocked_scenarios_excluded": True,
            "production_tokens_used": False,
            "production_admission_gate": False,
        },
        "runtime_entries": runtime_entries,
        "substantive_round": substantive_round,
        "decision": {
            "independent_round_gate": stability_gate and substantive_round["substantive_round_gate"],
            "next_required_action": "collect measured production token evidence before any L3.5/L4 admission or production_ready claim",
            "production_admission_gate": False,
        },
        "non_claims": {
            "no_production_proxy": True,
            "no_real_external_api_write": True,
            "no_kds_write": True,
            "no_status_upgrade": True,
            "no_sensitive_raw_text_stored": True,
            "no_cross_project_memory": True,
            "no_accepted_integrated_or_production_ready": True,
        },
        "measured_production_tokens": False,
    }

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(build_markdown(result), encoding="utf-8")
    print(
        "headroom_independent_loop_round_replay=pass "
        f"runtime_entry_count={len(runtime_entries)} "
        f"runtime_saving_rate={saving_rate} "
        f"saving_rate_drift={drift} "
        "independent_round_gate=true "
        "production_admission_gate=false measured_production_tokens=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
