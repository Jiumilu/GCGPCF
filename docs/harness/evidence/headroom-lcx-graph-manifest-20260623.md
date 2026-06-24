---
doc_id: GPCF-DOC-HEADROOM-LCX-GRAPH-MANIFEST-20260623
title: Headroom LCX Graph Manifest Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md
source_path: docs/harness/evidence/headroom-lcx-graph-manifest-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom LCX Graph Manifest Evidence

## Evidence ID

`HEADROOM-LCX-GRAPH-MANIFEST-20260623`

## 结论

Headroom 的项目群图谱已固化为受控 manifest：15 个项目/域路由、成本图、回滚图、授权图、等价性图全部可追踪。
production runtime graph 已作为正式层接入 manifest。
next-stage authorization bridge 已作为受控桥接层接入 manifest。
next_stage_authorization_package_granted_precheck_only
sanitized token ledger bridge 已作为 metadata replay only 层接入 manifest。
cost bridge 已作为 replay only 层接入 manifest。
signed approval bundle 与 authorization boundary review 已作为受控支撑证据接入 manifest，但不改变 blocked 状态。
当前 `production_token_measurement_allowed=false`，`measured_production_tokens=false`，`accepted=false`，`integrated=false`，`production_ready=false`。

## 图谱层

| layer_id | status | source |
|---|---|---|
| route_layer | controlled | `loop/context/headroom/policy.yaml` |
| authorization_layer | admitted_for_sanitized_measurement_precheck | `docs/harness/evidence/headroom-lcx-authorized-measurement-precheck-20260621.json` |
| authorization_bridge_layer | next_stage_authorization_package_granted_precheck_only | `docs/harness/evidence/headroom-lcx-real-measurement-next-stage-authorization-package-20260623.json` |
| token_ledger_bridge_layer | metadata_replay_check_pass_no_measurement | `fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json` |
| cost_bridge_layer | independent_production_token_free_loop_replay_ready | `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json` |
| cost_layer | controlled | `docs/harness/evidence/headroom-cost-sensitivity-model-20260621.json` |
| runtime_layer | production_runtime_graph_defined_controlled_only | `docs/harness/evidence/headroom-lcx-production-runtime-graph-20260623.json` |
| rollback_layer | controlled_no_production | `docs/harness/evidence/headroom-lcx-rollback-plan-20260622-001.md` |
| equivalence_layer | synthetic_only | `docs/harness/evidence/headroom-lcx-l35-answer-equivalence-synthetic-gate-20260622.json` |
| production_branch | blocked | `docs/harness/evidence/headroom-lcx-p5-production-admission-package-20260621.json` |

## 支撑证据

- `authorization_window_request`: `docs/harness/evidence/headroom-lcx-real-measurement-authorization-window-request-20260623.json`
- `approval_signed_bundle`: `docs/harness/evidence/headroom-lcx-real-measurement-approval-signed-bundle-20260623.json`
- `authorization_boundary_review`: `docs/harness/evidence/headroom-lcx-authorization-boundary-review-20260623.json`
- `sanitized_token_ledger`: `fixtures/headroom/headroom-lcx-sanitized-production-token-ledger-precheck-20260622.json`
- `metadata_replay_check`: `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`
- `loop_cost_observation_series`: `docs/harness/evidence/headroom-loop-cost-observation-series-20260621.json`
- `independent_replay`: `docs/harness/evidence/headroom-independent-loop-round-replay-20260621.json`

## 15 项目域

GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS

## 门禁

| 项 | 当前值 |
|---|---|
| project_count | `15` |
| graph_status | `controlled_pending_real_measurement` |
| measurement_authorization_state | `admitted_for_sanitized_measurement_precheck` |
| real_business_equivalence_measurement_allowed | `false` |
| production_token_measurement_allowed | `false` |
| measured_production_tokens | `false` |
| production_admission_gate | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |

## 非声明

- 本证据不表示真实生产测量已执行。
- 本证据不表示真实业务等价性已证明。
- 本证据不表示生产代理、生产 SDK、真实 KDS 写入或真实外部 API 写入已开启。
- 本证据不表示 accepted、integrated 或 production_ready。

## 下一步

只有在 WAES/Harness 另行裁决并补齐真实测量授权后，才可以把 production branch 从 blocked 推进到受控测量执行。
