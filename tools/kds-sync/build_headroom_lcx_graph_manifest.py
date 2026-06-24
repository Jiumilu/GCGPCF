#!/usr/bin/env python3
"""Build the Headroom LCX graph manifest from controlled source evidence."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover - environment dependency
    raise SystemExit(f"PyYAML is required: {exc}") from exc


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "docs/harness/evidence"
LOOPS_DIR = ROOT / "docs/harness/loops"
KDS_ROOT = ROOT / ".kds/development-space/开发/05-KDS"
KDS_EVIDENCE_DIR = KDS_ROOT / "docs/harness/evidence"
KDS_LOOPS_DIR = KDS_ROOT / "docs/harness/loops"
DOCS_DIR = ROOT / "loop/context/headroom/docs"

OUTPUT_JSON = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json"
OUTPUT_MD = EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.md"
OUTPUT_LOOP = LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-GRAPH-MANIFEST-001.md"

POLICY_PATH = ROOT / "loop/context/headroom/policy.yaml"
MEASUREMENT_REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-measurement-admission-request-20260622.json"
AUTH_PRECHECK_JSON = EVIDENCE_DIR / "headroom-lcx-authorized-measurement-precheck-20260621.json"
AUTH_SCHEMA_JSON = EVIDENCE_DIR / "headroom-lcx-authorization-schema-approval-package-20260622.json"
WINDOW_REQUEST_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-authorization-window-request-20260623.json"
NEXT_STAGE_PACKAGE_JSON = EVIDENCE_DIR / "headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json"
SANITIZED_LEDGER_JSON = ROOT / "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json"
METADATA_REPLAY_JSON = EVIDENCE_DIR / "headroom-lcx-metadata-replay-check-20260622.json"
LOOP_COST_SERIES_JSON = EVIDENCE_DIR / "headroom-loop-cost-observation-series-20260621.json"
INDEPENDENT_REPLAY_JSON = EVIDENCE_DIR / "headroom-independent-loop-round-replay-20260621.json"
P5_PACKAGE_JSON = EVIDENCE_DIR / "headroom-lcx-p5-production-admission-package-20260621.json"
COST_MODEL_JSON = EVIDENCE_DIR / "headroom-cost-sensitivity-model-20260621.json"
ROLLBACK_MD = EVIDENCE_DIR / "headroom-lcx-rollback-plan-20260622-001.md"
ANSWER_GATE_JSON = EVIDENCE_DIR / "headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json"
RUNTIME_GRAPH_JSON = EVIDENCE_DIR / "headroom-lcx-production-runtime-graph-20260623.json"

PROJECT_IDS = [
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


def read_text(path: Path) -> str:
    require(path.exists(), f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(read_text(path))
    require(isinstance(data, dict), f"{path.relative_to(ROOT)} must contain a YAML object")
    return data


def build_manifest() -> dict[str, Any]:
    policy = load_yaml(POLICY_PATH)
    routes = policy.get("project_routes", [])
    require(len(routes) == 15, "policy route count must remain 15")

    measurement_request = load_json(MEASUREMENT_REQUEST_JSON)
    precheck = load_json(AUTH_PRECHECK_JSON)
    auth_schema = load_json(AUTH_SCHEMA_JSON)
    window_request = load_json(WINDOW_REQUEST_JSON)
    next_stage_package = load_json(NEXT_STAGE_PACKAGE_JSON)
    sanitized_ledger = load_json(SANITIZED_LEDGER_JSON)
    metadata_replay = load_json(METADATA_REPLAY_JSON)
    p5_package = load_json(P5_PACKAGE_JSON)
    cost_model = load_json(COST_MODEL_JSON)
    loop_cost_series = load_json(LOOP_COST_SERIES_JSON)
    independent_replay = load_json(INDEPENDENT_REPLAY_JSON)
    answer_gate = load_json(ANSWER_GATE_JSON)
    runtime_graph = load_json(RUNTIME_GRAPH_JSON)

    routes_by_id = {route["project_id"]: route for route in routes}
    require(set(routes_by_id) == set(PROJECT_IDS), "policy project ids mismatch")

    project_routes = [
        {
            "project_id": route["project_id"],
            "source_path": route["source_path"],
            "allowed_modes": route["allowed_modes"],
            "blocked_modes": route["blocked_modes"],
            "requires_authorization": route["requires_authorization"],
            "cost_fields": route["cost_fields"],
            "sensitive_boundaries": route["sensitive_boundaries"],
            "owner": route["owner"],
            "current_gate": route["current_gate"],
        }
        for route in routes
    ]

    manifest = {
        "graph_id": "HEADROOM-LCX-GRAPH-MANIFEST-20260623",
        "status": "controlled_pending_real_measurement",
        "date": "2026-06-23",
        "scope": {
            "project_count": 15,
            "project_ids": PROJECT_IDS,
            "real_business_equivalence_scope": "sanitized_metadata_only_pending_real_measurement_authorization",
        },
        "layers": [
            {
                "layer_id": "route_layer",
                "status": "controlled",
                "purpose": "15_project_domain_lcx_route_coverage",
                "source_path": "loop/context/headroom/policy.yaml",
            },
            {
                "layer_id": "authorization_layer",
                "status": "admitted_for_sanitized_measurement_precheck",
                "purpose": "authorized_measurement_window_and_waes_harness_decision",
                "source_paths": [
                    "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
                    "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json",
                    "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json",
                    "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
                ],
            },
            {
                "layer_id": "authorization_bridge_layer",
                "status": next_stage_package.get("status"),
                "purpose": "next_stage_authorization_package_and_window_request_bridge",
                "source_path": "docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json",
            },
            {
                "layer_id": "token_ledger_bridge_layer",
                "status": metadata_replay.get("status"),
                "purpose": "sanitized_token_ledger_metadata_replay_only",
                "source_paths": [
                    "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json",
                    "docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json",
                    "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json",
                ],
            },
            {
                "layer_id": "cost_bridge_layer",
                "status": independent_replay.get("status"),
                "purpose": "sanitized_ledger_and_loop_cost_replay_bridge",
                "source_paths": [
                    "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
                    "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json",
                    "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json",
                ],
            },
            {
                "layer_id": "cost_layer",
                "status": "controlled",
                "purpose": "cost_sensitivity_and_loop_cost_observation",
                "source_paths": [
                    "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
                    "docs/harness/evidence/headroom-loop-cost-observation-20260621.json",
                    "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json",
                ],
            },
            {
                "layer_id": "runtime_layer",
                "status": runtime_graph.get("status"),
                "purpose": "production_runtime_cost_and_rollback_control",
                "source_path": "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json",
            },
            {
                "layer_id": "rollback_layer",
                "status": "controlled_no_production",
                "purpose": "rollback_plan_reference_and_no_write_boundary",
                "source_path": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            },
            {
                "layer_id": "equivalence_layer",
                "status": "synthetic_only",
                "purpose": "answer_equivalence_synthetic_gate_only",
                "source_path": "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json",
            },
            {
                "layer_id": "production_branch",
                "status": "blocked",
                "purpose": "production_measurement_and_admission_not_open",
                "source_path": "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json",
            },
        ],
        "project_routes": project_routes,
        "authorization": {
            "request_evidence_id": measurement_request.get("evidence_id"),
            "request_status": measurement_request.get("status"),
            "approval_package_evidence_id": auth_schema.get("evidence_id"),
            "approval_package_status": auth_schema.get("status"),
            "authorization_window_request_evidence_id": window_request.get("evidence_id"),
            "authorization_window_request_status": window_request.get("status"),
            "next_stage_authorization_package_evidence_id": next_stage_package.get("evidence_id"),
            "next_stage_authorization_package_status": next_stage_package.get("status"),
            "sanitized_token_ledger_id": sanitized_ledger.get("ledger_id"),
            "sanitized_token_ledger_type": sanitized_ledger.get("ledger_type"),
            "metadata_replay_check_evidence_id": metadata_replay.get("evidence_id"),
            "metadata_replay_check_status": metadata_replay.get("status"),
            "loop_cost_observation_series_evidence_id": loop_cost_series.get("evidence_id"),
            "loop_cost_observation_series_status": loop_cost_series.get("status"),
            "independent_replay_evidence_id": independent_replay.get("evidence_id"),
            "independent_replay_status": independent_replay.get("status"),
            "precheck_evidence_id": precheck.get("evidence_id"),
            "precheck_status": precheck.get("status"),
            "waes_harness_admission_decision": precheck.get("waes_harness_admission_decision"),
            "authorized_window_id": precheck.get("authorized_window_id", "LCX-MEASURE-20260622-001"),
            "authorized_by": precheck.get("authorized_by", "lujunxiang / GPCF owner"),
            "authorized_at": precheck.get("authorized_at", "2026-06-22T08:42:06+08:00"),
            "sanitized_production_token_ledger": measurement_request.get("sanitized_production_token_ledger"),
            "rollback_plan_id": measurement_request.get("rollback_plan_id", "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001"),
            "telemetry_default": policy.get("telemetry_default", "off"),
            "production_token_measurement_allowed": False,
            "measured_production_tokens": False,
            "production_proxy_started": False,
            "production_sdk_enabled": False,
            "production_external_api_write": False,
            "kds_api_write": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
        },
        "cost_graph": {
            "source_evidence_id": cost_model.get("evidence_id"),
            "status": cost_model.get("status"),
            "project_count": cost_model.get("project_count"),
            "profile_count": len(cost_model.get("profiles", [])),
            "saving_rate_floor": 0.2,
            "production_admission_gate": cost_model.get("decision", {}).get("production_admission_gate", False),
            "measured_production_tokens": cost_model.get("measured_production_tokens", False),
        },
        "rollback_graph": {
            "evidence_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "status": "rollback_plan_present_no_production_write",
            "rollback_plan_present": True,
            "rollback_plan_id": "HEADROOM-LCX-ROLLBACK-PLAN-20260622-001",
            "rollback_plan_source": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            "rollback_coverage": [
                "production_proxy_start_blocked",
                "production_sdk_enable_blocked",
                "real_kds_api_write_blocked",
                "external_api_write_blocked",
                "headroom_learn_apply_blocked",
                "memory_as_kds_fact_source_blocked",
            ],
        },
        "equivalence_graph": {
            "source_evidence_id": answer_gate.get("evidence_id"),
            "status": answer_gate.get("status"),
            "business_answer_equivalence_proven": answer_gate.get("gates", {}).get("business_answer_equivalence_proven", False),
            "answer_equivalence_gate": answer_gate.get("gates", {}).get("answer_equivalence_gate", False),
            "marker_preservation_gate": answer_gate.get("gates", {}).get("marker_preservation_gate", False),
            "citation_preservation_gate": answer_gate.get("gates", {}).get("citation_preservation_gate", False),
            "real_business_measurement_allowed": False,
        },
        "runtime_graph": {
            "source_evidence_id": runtime_graph.get("runtime_graph_id"),
            "status": runtime_graph.get("status"),
            "production_branch_blocked": runtime_graph.get("current_state", {}).get("production_branch_blocked", True),
            "production_token_measurement_allowed": runtime_graph.get("current_state", {}).get("production_token_measurement_allowed", False),
            "measured_production_tokens": runtime_graph.get("current_state", {}).get("measured_production_tokens", False),
            "production_admission_gate": runtime_graph.get("current_state", {}).get("production_admission_gate", False),
            "accepted": runtime_graph.get("current_state", {}).get("accepted", False),
            "integrated": runtime_graph.get("current_state", {}).get("integrated", False),
            "production_ready": runtime_graph.get("current_state", {}).get("production_ready", False),
        },
        "edges": [
            {
                "from": "route_layer",
                "to": "cost_layer",
                "relation": "project_routes_feed_cost_fields",
            },
            {
                "from": "route_layer",
                "to": "authorization_layer",
                "relation": "project_routes_require_measurement_authorization",
            },
            {
                "from": "authorization_layer",
                "to": "authorization_bridge_layer",
                "relation": "window_request_materializes_next_stage_authorization_package",
            },
            {
                "from": "authorization_bridge_layer",
                "to": "token_ledger_bridge_layer",
                "relation": "bridge_package_requires_sanitized_token_ledger_metadata_replay",
            },
            {
                "from": "token_ledger_bridge_layer",
                "to": "cost_bridge_layer",
                "relation": "sanitized_ledger_metadata_replay_feeds_cost_replay",
            },
            {
                "from": "cost_bridge_layer",
                "to": "cost_layer",
                "relation": "cost_bridge_materializes_cost_graph_from_replay_evidence",
            },
            {
                "from": "cost_layer",
                "to": "rollback_layer",
                "relation": "cost_graph_still_requires_rollback_plan",
            },
            {
                "from": "runtime_layer",
                "to": "rollback_layer",
                "relation": "runtime_graph_references_rollback_plan",
            },
            {
                "from": "authorization_layer",
                "to": "equivalence_graph",
                "relation": "only_sanitized_equivalence_evidence_admitted",
            },
            {
                "from": "equivalence_graph",
                "to": "production_branch",
                "relation": "synthetic_only_does_not_open_production",
            },
            {
                "from": "rollback_layer",
                "to": "production_branch",
                "relation": "rollback_plan_present_but_not_a_production_opening_signal",
            },
        ],
        "non_claims": {
            "real_kds_api_write": False,
            "production_proxy": False,
            "production_sdk": False,
            "production_external_api_write": False,
            "measured_production_tokens": False,
            "accepted": False,
            "integrated": False,
            "production_ready": False,
            "business_answer_equivalence_proven": False,
            "headroom_memory_as_kds_fact_source": False,
        },
        "source_refs": {
            "policy": "loop/context/headroom/policy.yaml",
            "measurement_request": "docs/harness/evidence/headroom-lcx-measurement-admission-request-20260622.json",
            "precheck": "docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json",
            "approval_package": "docs/harness/evidence/headroom-lcx-authorization-schema-approval-package-20260622.json",
            "authorization_window_request": "docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json",
            "next_stage_authorization_package": "docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json",
            "sanitized_token_ledger": "fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json",
            "metadata_replay_check": "docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json",
            "loop_cost_observation_series": "docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json",
            "independent_replay": "docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json",
            "p5_package": "docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json",
            "cost_model": "docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json",
            "rollback_plan": "docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md",
            "equivalence_gate": "docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json",
            "runtime_graph": "docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json",
        },
    }

    return manifest


def write_outputs(manifest: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    LOOPS_DIR.mkdir(parents=True, exist_ok=True)
    KDS_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    KDS_LOOPS_DIR.mkdir(parents=True, exist_ok=True)

    json_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    OUTPUT_JSON.write_text(json_text, encoding="utf-8")
    (KDS_EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.json").write_text(json_text, encoding="utf-8")

    md_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-GRAPH-MANIFEST-20260623",
            "title: Headroom LCX Graph Manifest Evidence",
            "project: GPCF",
            "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md",
            "source_path: docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Headroom LCX Graph Manifest Evidence",
            "",
            "## Evidence ID",
            "",
            "`HEADROOM-LCX-GRAPH-MANIFEST-20260623`",
            "",
            "## 结论",
            "",
            "Headroom 的项目群图谱已固化为受控 manifest：15 个项目/域路由、成本图、回滚图、授权图、等价性图全部可追踪。",
            "production runtime graph 已作为正式层接入 manifest。",
            "next-stage authorization bridge 已作为受控桥接层接入 manifest。",
            "next_stage_authorization_package_granted_precheck_only",
            "sanitized token ledger bridge 已作为 metadata replay only 层接入 manifest。",
            "cost bridge 已作为 replay only 层接入 manifest。",
            "当前 `production_token_measurement_allowed=false`，`measured_production_tokens=false`，`accepted=false`，`integrated=false`，`production_ready=false`。",
            "",
            "## 图谱层",
            "",
            "| layer_id | status | source |",
            "|---|---|---|",
            "| route_layer | controlled | `loop/context/headroom/policy.yaml` |",
            "| authorization_layer | admitted_for_sanitized_measurement_precheck | `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json` |",
            "| authorization_bridge_layer | next_stage_authorization_package_granted_precheck_only | `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json` |",
            "| token_ledger_bridge_layer | metadata_replay_check_pass_no_measurement | `fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json` |",
            "| cost_bridge_layer | independent_production_token_free_loop_replay_ready | `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json` |",
            "| cost_layer | controlled | `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json` |",
            f"| runtime_layer | {manifest['runtime_graph']['status']} | `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json` |",
            "| rollback_layer | controlled_no_production | `docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md` |",
            "| equivalence_layer | synthetic_only | `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json` |",
            "| production_branch | blocked | `docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json` |",
            "",
            "## 支撑证据",
            "",
            f"- `authorization_window_request`: `{manifest['source_refs']['authorization_window_request']}`",
            f"- `sanitized_token_ledger`: `{manifest['source_refs']['sanitized_token_ledger']}`",
            f"- `metadata_replay_check`: `{manifest['source_refs']['metadata_replay_check']}`",
            f"- `loop_cost_observation_series`: `{manifest['source_refs']['loop_cost_observation_series']}`",
            f"- `independent_replay`: `{manifest['source_refs']['independent_replay']}`",
            "",
            "## 15 项目域",
            "",
            "GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS",
            "",
            "## 门禁",
            "",
            "| 项 | 当前值 |",
            "|---|---|",
            f"| project_count | `{manifest['scope']['project_count']}` |",
            f"| graph_status | `{manifest['status']}` |",
            "| measurement_authorization_state | `admitted_for_sanitized_measurement_precheck` |",
            "| real_business_equivalence_measurement_allowed | `false` |",
            "| production_token_measurement_allowed | `false` |",
            "| measured_production_tokens | `false` |",
            "| production_admission_gate | `false` |",
            "| accepted | `false` |",
            "| integrated | `false` |",
            "| production_ready | `false` |",
            "",
            "## 非声明",
            "",
            "- 本证据不表示真实生产测量已执行。",
            "- 本证据不表示真实业务等价性已证明。",
            "- 本证据不表示生产代理、生产 SDK、真实 KDS 写入或真实外部 API 写入已开启。",
            "- 本证据不表示 accepted、integrated 或 production_ready。",
            "",
            "## 下一步",
            "",
            "只有在 WAES/Harness 另行裁决并补齐真实测量授权后，才可以把 production branch 从 blocked 推进到受控测量执行。",
        ]
    ) + "\n"
    OUTPUT_MD.write_text(md_text, encoding="utf-8")
    (KDS_EVIDENCE_DIR / "headroom-lcx-graph-manifest-20260623.md").write_text(md_text, encoding="utf-8")

    loop_text = "\n".join(
        [
            "---",
            "doc_id: GPCF-DOC-HEADROOM-LCX-GRAPH-MANIFEST-LOOP-001",
            "title: Loop Round GPCF Headroom LCX Graph Manifest 001",
            "project: GPCF",
            "related_projects: [GPCF, KDS, WAES, GFIS, GPC, PVAOS, Edge, PKC, Brain, XiaoC, XGD, XiaoG, MMC, Studio, WAS]",
            "domain: docs",
            "status: controlled",
            "version: v1.0",
            "owner: GPCF",
            "kds_space: 开发",
            "kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-GRAPH-MANIFEST-001.md",
            "source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-GRAPH-MANIFEST-001.md",
            "sync_direction: bidirectional",
            "last_reviewed: 2026-06-23",
            "supersedes: []",
            "superseded_by: []",
            "---",
            "",
            "# Loop Round GPCF Headroom LCX Graph Manifest 001",
            "",
            "## 输入",
            "",
            "- 当前目标是把 Headroom 的项目群图谱固化为统一 manifest，覆盖真实业务等价授权测量、生产级运行、成本和回滚边界。",
            "- 当前仍不得把生产 branch 打开为真实测量执行。",
            "",
            "## 动作",
            "",
            "1. 汇总 15 项目域路由、成本模型、授权前置、next-stage bridge、token ledger bridge、cost bridge、回滚计划和 synthetic equivalence evidence。",
            "2. 生成 graph manifest JSON 与 evidence Markdown。",
            "3. 生成 validator，检查 production 相关标志仍为 false。",
            "",
            "## 输出",
            "",
            "- `tools/kds-sync/build_headroom_lcx_graph_manifest.py`",
            "- `tools/kds-sync/validate_headroom_lcx_graph_manifest.py`",
            "- `docs/harness/evidence/headroom-lcx-graph-manifest-20260623.json`",
            "- `docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md`",
            "",
            "## 检查",
            "",
            "- `python3 tools/kds-sync/build_headroom_lcx_graph_manifest.py`",
            "- `python3 tools/kds-sync/validate_headroom_lcx_graph_manifest.py`",
            "- `python3 tools/kds-sync/check_document_pollution.py`",
            "- `python3 tools/kds-sync/validate_kds_token.py`",
            "- `python3 tools/kds-sync/loop_document_gate.py --check-only`",
            "",
            "## 反馈",
            "",
            "图谱对象将把路由、成本、回滚、授权、next-stage bridge、token ledger bridge、cost bridge、runtime graph 和等价性串成单一可审计 manifest，但 production branch 仍保持 blocked。",
            "next-stage authorization bridge 已作为受控桥接层接入 manifest，但不改变 production branch 的 blocked 状态。",
            "next_stage_authorization_package_granted_precheck_only",
            "sanitized token ledger bridge 已作为 metadata replay only 层接入 manifest，但不计算真实生产节省。",
            "cost bridge 已作为 replay only 层接入 manifest，但不产生真实生产 token 结论。",
            "",
            "## 下一轮",
            "",
            "若未来获得真实测量授权，再把 graph manifest 的 production branch 接到真实测量 runner；当前继续保持 no-write。",
        ]
    ) + "\n"
    OUTPUT_LOOP.write_text(loop_text, encoding="utf-8")
    (KDS_LOOPS_DIR / "loop-round-GPCF-HEADROOM-LCX-GRAPH-MANIFEST-001.md").write_text(loop_text, encoding="utf-8")


def main() -> int:
    manifest = build_manifest()
    write_outputs(manifest)
    print(
        "headroom_lcx_graph_manifest=generated "
        f"project_count={manifest['scope']['project_count']} "
        "production_token_measurement_allowed=false "
        "measured_production_tokens=false "
        "accepted=false integrated=false production_ready=false"
    )
    print(f"generated_at={datetime.now(timezone.utc).isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
